import logging
import time
from typing import Any

import numpy as np
from haive.core.engine.agent.agent import register_agent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.types import Command

from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.rag.llm_rag.agent import LLMRAGAgent
from haive.agents.react_class.react.agent import ReactAgent
from haive.agents.react_class.react_many_tools.config import ReactManyToolsConfig

logger = logging.getLogger(__name__)


@register_agent(ReactManyToolsConfig)
class ReactManyToolsAgent(ReactAgent):
    """React Agent implementation that can handle many tools efficiently.

    Extends ReactAgent with advanced tool filtering and selection
    to manage large numbers of tools, and integrates RAG capabilities.
    """

    def __init__(self, config: ReactManyToolsConfig):
        """Initialize the agent with its configuration."""
        super().__init__(config)
        self.config = config

        # Set up tool embeddings if semantic search is enabled
        if (
            self.config.tool_selection_mode == "semantic"
            and self.config.embeddings_model
        ):
            self._create_tool_embeddings()

        # Initialize RAG components if enabled
        if self.config.use_rag:
            self._initialize_rag_components()

    def _initialize_rag_components(self) -> None:
        """Initialize RAG components from configuration."""
        self._retriever = None

        # If we have a RAG config, use that directly
        if self.config.rag_config:
            # Try to use BaseRAGAgent directly
            try:
                self.rag_agent = BaseRAGAgent(self.config.rag_config)
                # If it's a LLMRAGAgent, we can also use its answer generation
                if isinstance(self.rag_agent, LLMRAGAgent):
                    self.has_answer_generation = True
                else:
                    self.has_answer_generation = False
            except Exception as e:
                logger.error(f"Error initializing RAG agent: {e}")
                self.rag_agent = None

        # If we have a retriever config, use that directly
        elif self.config.retriever_config:
            try:
                # Initialize retriever from config
                self._retriever = self.config.retriever_config.create_runnable()
                self.has_answer_generation = False
            except Exception as e:
                logger.error(f"Error initializing retriever: {e}")
                self._retriever = None

    @property
    def retriever(self):
        """Lazy initialization of retriever."""
        if self._retriever is None:
            # If we have a RAG agent, use its retriever
            if hasattr(self, "rag_agent") and self.rag_agent:
                self._retriever = self.rag_agent.retriever
            # Otherwise try to initialize from config
            elif self.config.retriever_config:
                try:
                    self._retriever = self.config.retriever_config.create_runnable()
                except Exception as e:
                    logger.error(f"Error creating retriever: {e}")
                    # Return a dummy retriever
                    self._retriever = lambda x: []
            else:
                # Return a dummy retriever
                self._retriever = lambda x: []
        return self._retriever

    def _create_tool_embeddings(self) -> None:
        """Create embeddings for tools for semantic filtering."""
        self.tool_embeddings = {}
        embeddings_model = self.config.embeddings_model

        if not embeddings_model:
            logger.warning("No embeddings model provided for semantic tool filtering")
            return

        for tool in self.tools:
            # Create a rich description for embedding
            description = f"{tool.name}: {tool.description}"

            # Generate and store the embedding
            try:
                embedding = embeddings_model.embed_query(description)
                self.tool_embeddings[tool.name] = embedding
            except Exception as e:
                logger.warning(f"Error creating embedding for tool {tool.name}: {e}")

    def setup_workflow(self) -> None:
        """Set up the workflow with tool filtering nodes and RAG integration."""
        logger.debug(f"Setting up workflow for ReactManyToolsAgent {self.config.name}")

        # Create dynamic graph builder
        gb = DynamicGraph(
            components=[self.config.engine], state_schema=self.config.state_schema
        )

        # Add query extraction node first
        gb.add_node("extract_query", self._extract_query, "filter_tools")
        gb.set_entry_point("extract_query")

        # Add tool filtering node after query extraction
        gb.add_node("filter_tools", self._filter_tools, "add_system")

        # Add document retrieval if RAG is enabled
        if self.config.use_rag:
            gb.add_node("retrieve_documents", self._retrieve_documents, "add_system")

            # Add a conditional edge to decide whether to retrieve documents
            gb.add_conditional_edges(
                "filter_tools",
                self._should_retrieve_documents,
                {
                    "retrieve_documents": "retrieve_documents",
                    "add_system": "add_system",
                },
            )

            # Add answer generation if available
            if hasattr(self, "has_answer_generation") and self.has_answer_generation:
                gb.add_node("generate_answer", self._generate_answer, "add_system")
                gb.overwrite_edge("retrieve_documents", "generate_answer")

        # Add system message if provided
        if self.config.system_prompt:
            self._add_system_message_node(gb)

        # Set up the LLM with tool binding
        self._setup_llm_node(gb)

        # Set up tool execution
        if self.version == "v1":
            self._setup_tools_v1(gb)
        else:
            self._setup_tools_v2(gb)

        # Add structured output node if schema provided
        if self.config.structured_output_schema:
            self._add_structured_output_node(gb)

        # Build the graph
        self.graph = gb.build()
        logger.info(f"Set up React Many Tools workflow for {self.config.name}")

    def _extract_query(self, state: dict[str, Any]) -> dict[str, Any]:
        """Extract query from messages and store in state.

        Args:
            state: Current state with messages

        Returns:
            Updated state with extracted query
        """
        # Extract the query from messages
        query = self._extract_query_from_state(state)

        # Only update if we found a query
        if query:
            return {"query": query}

        return {}

    def _should_retrieve_documents(self, state: dict[str, Any]) -> str:
        """Decide whether to retrieve documents based on state.

        Args:
            state: Current state

        Returns:
            Next node name
        """
        # Skip retrieval if RAG is disabled
        if not self.config.use_rag:
            return "add_system"

        # Skip if no query
        if not state.get("query"):
            return "add_system"

        # Skip if already have documents
        if state.get("retrieved_documents"):
            return "add_system"

        # Perform retrieval
        return "retrieve_documents"

    def _retrieve_documents(self, state: dict[str, Any]) -> Command:
        """Retrieve relevant documents based on the query.

        Args:
            state: Current state with query

        Returns:
            Command for updating state with retrieved documents
        """
        query = state.get("query")
        if not query:
            return Command(update={"retrieved_documents": []}, goto="add_system")

        logger.info(f"Retrieving documents for query: {query}")
        start_time = time.time()

        try:
            # Use the retriever
            documents = self.retriever(query)

            if not isinstance(documents, list):
                documents = [documents]

            # Process documents to ensure they're in expected format
            processed_docs = []
            for doc in documents:
                if isinstance(doc, Document):
                    # Convert to dictionary
                    processed_docs.append(
                        {"page_content": doc.page_content, "metadata": doc.metadata}
                    )
                elif isinstance(doc, dict) and "page_content" in doc:
                    # Already in expected format
                    processed_docs.append(doc)
                else:
                    # Unknown format, convert to simple document
                    processed_docs.append({"page_content": str(doc), "metadata": {}})

            logger.info(
                f"Retrieved {len(processed_docs)} documents in {time.time() - start_time:.2f}s"
            )

            # If we have answer generation capability, route there
            next_node = (
                "generate_answer"
                if (
                    hasattr(self, "has_answer_generation")
                    and self.has_answer_generation
                )
                else "add_system"
            )

            # Update state with retrieved documents
            return Command(
                update={
                    "retrieved_documents": processed_docs,
                    "retrieval_metadata": {
                        "time_taken": time.time() - start_time,
                        "document_count": len(processed_docs),
                    },
                },
                goto=next_node,
            )

        except Exception as e:
            logger.error(f"Error retrieving documents: {e!s}")
            return Command(
                update={"error": f"Error retrieving documents: {e!s}"},
                goto="add_system",
            )

    def _generate_answer(self, state: dict[str, Any]) -> Command:
        """Generate an answer based on retrieved documents.

        Args:
            state: Current state with query and retrieved documents

        Returns:
            Command with generated answer
        """
        query = state.get("query")
        documents = state.get("retrieved_documents", [])

        if not documents:
            return Command(update={"answer": None}, goto="add_system")

        try:
            # If we have a RAG agent with answer generation
            if hasattr(self, "rag_agent") and hasattr(
                self.rag_agent, "generate_answer"
            ):
                # Convert documents to expected format if needed
                rag_documents = []
                for doc in documents:
                    if isinstance(doc, dict) and "page_content" in doc:
                        rag_documents.append(
                            Document(
                                page_content=doc["page_content"],
                                metadata=doc.get("metadata", {}),
                            )
                        )
                    elif isinstance(doc, Document):
                        rag_documents.append(doc)

                # Call the RAG agent's answer generation
                rag_state = {"query": query, "retrieved_documents": rag_documents}
                result = self.rag_agent.generate_answer(rag_state)

                # Extract answer
                answer = (
                    result.update.get("answer") if hasattr(result, "update") else None
                )

            # Otherwise use our answer generator
            elif self.config.answer_generator:
                # Create answer generator
                answer_gen = self.config.answer_generator.create_runnable()

                # Format context from documents
                context = "\n\n".join(
                    [
                        (
                            doc.get("page_content", str(doc))
                            if isinstance(doc, dict)
                            else (
                                doc.page_content
                                if hasattr(doc, "page_content")
                                else str(doc)
                            )
                        )
                        for doc in documents
                    ]
                )

                # Generate answer
                messages = [
                    SystemMessage(
                        content="You are a helpful assistant that answers questions based on provided context."
                    ),
                    HumanMessage(
                        content=f"Context:\n{context}\n\nQuery: {query}\n\nAnswer the query based on the context provided."
                    ),
                ]

                response = answer_gen.invoke(messages)

                # Extract answer
                answer = (
                    response.content if hasattr(response, "content") else str(response)
                )

            # Fallback to simple concatenation
            else:
                # Just combine document contents
                answer = "Based on the retrieved information:\n\n"
                for i, doc in enumerate(documents[:3]):  # Limit to 3 documents
                    content = (
                        doc.get("page_content", str(doc))
                        if isinstance(doc, dict)
                        else str(doc)
                    )
                    answer += f"Source {i+1}: {content[:200]}...\n\n"

            # Update state with answer
            return Command(update={"answer": answer}, goto="add_system")

        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return Command(
                update={"answer": f"Error generating answer: {e}"}, goto="add_system"
            )

    def _filter_tools(self, state: dict[str, Any]) -> dict[str, Any]:
        """Filter tools based on the query.

        Args:
            state: Current state with query or messages

        Returns:
            Updated state with filtered tools
        """
        # Get query from state
        query = state.get("query") or self._extract_query_from_state(state)

        if not query:
            # No query, use all tools
            logger.debug("No query found, using all tools")
            return {"filtered_tools": [tool.name for tool in self.tools]}

        # Determine which filtering strategy to use
        if self.config.tool_selection_mode == "auto":
            # Choose strategy based on query and available methods
            if self.config.embeddings_model and len(query.split()) > 3:
                strategy = "semantic"
            elif self.config.tool_categories:
                strategy = "categorical"
            else:
                strategy = "keyword"
        else:
            strategy = self.config.tool_selection_mode

        # Apply the chosen strategy
        if strategy == "semantic":
            filtered_tools = self._filter_tools_semantic(query)
        elif strategy == "categorical":
            filtered_tools = self._filter_tools_categorical(query)
        else:  # keyword
            filtered_tools = self._filter_tools_keyword(query)

        # Ensure we don't exceed the max tools limit
        if len(filtered_tools) > self.config.max_tools_per_request:
            filtered_tools = filtered_tools[: self.config.max_tools_per_request]

        # If filtering resulted in no tools, fall back to a minimal set
        if not filtered_tools:
            logger.warning(f"Filtering resulted in no tools for query: {query}")

            # Use the most general tools or a small sample
            if len(self.tools) <= 5:
                filtered_tools = [tool.name for tool in self.tools]
            else:
                # Take a sample of tools
                import random

                sample_size = min(5, len(self.tools))
                sampled_tools = random.sample(self.tools, sample_size)
                filtered_tools = [tool.name for tool in sampled_tools]

        # Store the filtered tool names in state
        return {"filtered_tools": filtered_tools, "tool_filter_query": query}

    def _extract_query_from_state(self, state: dict[str, Any]) -> str:
        """Extract query from state.

        Args:
            state: Current state

        Returns:
            Extracted query
        """
        # Try direct query field
        if "query" in state:
            return state["query"]

        # Try getting from messages
        messages = state.get("messages", [])
        if messages:
            # Look for the last user message
            for msg in reversed(messages):
                if isinstance(msg, HumanMessage) or (
                    isinstance(msg, tuple) and msg[0] == "human"
                ):
                    content = msg.content if hasattr(msg, "content") else msg[1]
                    return str(content)

        # Fall back to empty string
        return ""

    def _filter_tools_semantic(self, query: str) -> list[str]:
        """Filter tools using semantic similarity.

        Args:
            query: User query

        Returns:
            List of tool names
        """
        if not hasattr(self, "tool_embeddings") or not self.config.embeddings_model:
            logger.warning("Semantic filtering requested but embeddings not available")
            return self._filter_tools_keyword(query)

        try:
            # Generate query embedding
            query_embedding = self.config.embeddings_model.embed_query(query)

            # Calculate similarity with all tools
            similarities = {}
            for tool_name, tool_embedding in self.tool_embeddings.items():
                # Calculate cosine similarity
                similarity = np.dot(query_embedding, tool_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(tool_embedding)
                )
                similarities[tool_name] = similarity

            # Sort tools by similarity
            sorted_tools = sorted(
                similarities.items(), key=lambda x: x[1], reverse=True
            )

            # Return top N tool names
            return [
                tool_name
                for tool_name, _ in sorted_tools[: self.config.max_tools_per_request]
            ]

        except Exception as e:
            logger.error(f"Error in semantic tool filtering: {e}")
            return self._filter_tools_keyword(query)

    def _filter_tools_categorical(self, query: str) -> list[str]:
        """Filter tools using category matching.

        Args:
            query: User query

        Returns:
            List of tool names
        """
        if not self.config.tool_categories:
            logger.warning("Categorical filtering requested but no categories defined")
            return self._filter_tools_keyword(query)

        # Try to match query to categories
        query_lower = query.lower()
        matched_categories = []

        for category in self.config.tool_categories:
            category_lower = category.lower()
            if category_lower in query_lower:
                matched_categories.append(category)

        # If no categories matched, try keyword matching within categories
        if not matched_categories:
            for category, tools in self.config.tool_categories.items():
                # Check if any tool in the category has a keyword match
                category_tools = [t for t in self.tools if t.name in tools]
                for tool in category_tools:
                    if tool.name.lower() in query_lower or (
                        tool.description and tool.description.lower() in query_lower
                    ):
                        matched_categories.append(category)
                        break

        # Get tools from matched categories
        matched_tools: set[str] = set()
        for category in matched_categories:
            matched_tools.update(self.config.tool_categories.get(category, []))

        # If still no matches, fall back to keyword matching
        if not matched_tools:
            return self._filter_tools_keyword(query)

        return list(matched_tools)

    def _filter_tools_keyword(self, query: str) -> list[str]:
        """Filter tools using keyword matching.

        Args:
            query: User query

        Returns:
            List of tool names
        """
        query_terms = query.lower().split()
        scored_tools = []

        for tool in self.tools:
            # Score is based on keyword matches in name and description
            score = 0

            # Check name
            for term in query_terms:
                if term in tool.name.lower():
                    score += 3

            # Check description
            if tool.description:
                for term in query_terms:
                    if term in tool.description.lower():
                        score += 1

            scored_tools.append((tool.name, score))

        # Sort by score and return tools
        sorted_tools = [
            tool
            for tool, score in sorted(scored_tools, key=lambda x: x[1], reverse=True)
            if score > 0
        ]

        # If we have very few matches, include some default tools
        if len(sorted_tools) < 3:
            # Add a few general-purpose tools if available
            general_tools = [
                t.name
                for t in self.tools
                if "search" in t.name.lower()
                or "find" in t.name.lower()
                or "get" in t.name.lower()
            ]

            # Add general tools that aren't already in our list
            for tool in general_tools:
                if tool not in sorted_tools:
                    sorted_tools.append(tool)

            # If still too few, add some random tools
            if len(sorted_tools) < 3 and len(self.tools) > 3:
                import random

                remaining_tools = [
                    t.name for t in self.tools if t.name not in sorted_tools
                ]
                random_tools = random.sample(
                    remaining_tools, min(3, len(remaining_tools))
                )
                sorted_tools.extend(random_tools)

        return sorted_tools

    def _add_system_message_node(self, gb: DynamicGraph) -> None:
        """Add a node for adding a system message to the state."""

        def add_system_message(state: dict[str, Any]) -> dict[str, Any]:
            """Add system message if none exists yet, with context from retrieved documents."""
            messages = state.get("messages", [])

            # Check if we already have a system message
            has_system = any(
                isinstance(m, SystemMessage)
                for m in messages
                if isinstance(m, BaseMessage)
            )

            # Add system message if none exists
            if not has_system:
                base_content = (
                    self.config.system_prompt or "You are a helpful assistant."
                )

                # Add context from retrieved documents if available
                documents = state.get("retrieved_documents", [])
                answer = state.get("answer")

                if documents and answer:
                    # Enhanced system message with RAG context
                    system_content = f"{base_content}\n\nI've analyzed the following information to help with your questions:\n\n{answer}"
                    system_msg = SystemMessage(content=system_content)
                else:
                    # Standard system message
                    system_msg = SystemMessage(content=base_content)

                # Return the updated messages list
                return {"messages": [system_msg]}

            # No change needed
            return {}

        # Add the node and connect it
        gb.add_node("add_system", add_system_message, self.config.llm_node_name)

    def _setup_llm_node(self, gb: DynamicGraph) -> None:
        """Set up the LLM node with filtered tool binding."""
        # Override parent method to use filtered tools
        llm_engine = self.config.engine

        # Create a wrapper for the LLM that binds only the filtered tools
        def llm_with_filtered_tools(state: dict[str, Any]) -> dict[str, Any]:
            # Get filtered tool names
            filtered_tool_names = state.get("filtered_tools", [])

            # Get the corresponding tool objects
            tool_name_map = {tool.name: tool for tool in self.tools}
            filtered_tools = [
                tool_name_map[name]
                for name in filtered_tool_names
                if name in tool_name_map
            ]

            # If no tools were filtered, use a few default tools
            if not filtered_tools and self.tools:
                # Use a small set of tools (either all or a sample)
                if len(self.tools) <= 5:
                    filtered_tools = self.tools
                else:
                    # Take a sample
                    import random

                    filtered_tools = random.sample(self.tools, 5)

            # Create a copy of the engine with the filtered tools
            if isinstance(llm_engine, AugLLMConfig):
                # Create a copy of the config
                import copy

                modified_engine = copy.deepcopy(llm_engine)

                # Update with filtered tools
                modified_engine.tools = filtered_tools

                # Create a runnable
                llm_runnable = modified_engine.create_runnable()
            # Assume it's already a runnable
            elif hasattr(llm_engine, "bind_tools"):
                # Try to bind the filtered tools
                llm_runnable = llm_engine.bind_tools(filtered_tools)
            else:
                # Can't bind tools, use as-is
                llm_runnable = llm_engine

            # Get messages from state
            messages = state.get("messages", [])

            # Add retrieved document information if available and not already in messages
            documents = state.get("retrieved_documents", [])
            answer = state.get("answer")

            if (
                documents
                and answer
                and not any(
                    isinstance(m, SystemMessage)
                    and "analyzed the following information" in m.content
                    for m in messages
                    if isinstance(m, BaseMessage)
                )
            ):
                # Look for system message to enhance
                for i, msg in enumerate(messages):
                    if isinstance(msg, SystemMessage):
                        # Enhance existing system message
                        original_content = msg.content
                        enhanced_content = f"{original_content}\n\nI've analyzed the following information to help with your questions:\n\n{answer}"
                        messages[i] = SystemMessage(content=enhanced_content)
                        break

            # Invoke the LLM
            response = llm_runnable.invoke(messages)

            # Return the response
            return {"messages": [response]}

        # Add the wrapped LLM node
        gb.add_node(
            name=self.config.llm_node_name,
            config=llm_with_filtered_tools,
            # Router function will handle routing decision
            command_goto=None,
        )

    def run(self, input_data: str | dict[str, Any], **kwargs) -> dict[str, Any]:
        """Run the agent with dynamic tool filtering and RAG capabilities.

        Args:
            input_data: Input query or state
            **kwargs: Additional parameters

        Returns:
            Result from agent execution
        """
        # Process input data to ensure it includes messages
        if isinstance(input_data, str):
            input_data = {"messages": [HumanMessage(content=input_data)]}

        # Add query if it's not already present
        if "query" not in input_data and "messages" in input_data:
            messages = input_data["messages"]
            if messages:
                # Find the last human message
                for msg in reversed(messages):
                    if isinstance(msg, HumanMessage) or (
                        isinstance(msg, tuple) and msg[0] == "human"
                    ):
                        content = msg.content if hasattr(msg, "content") else msg[1]
                        input_data["query"] = str(content)
                        break

        # Run the agent
        return super().run(input_data, **kwargs)
