"""Agentic RAG Multi-Agent System.

This implements an advanced RAG system with document grading, query rewriting,
and conditional routing between retrieval and web search.
"""

from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.retriever import BaseRetrieverConfig
from haive.core.engine.vectorstore import VectorStoreConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.prebuilt.messages_state import MessagesState
from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langgraph.graph import END, START
from pydantic import Field

from haive.agents.rag.agentic.document_grader import create_document_grader_agent
from haive.agents.rag.agentic.query_rewriter import create_query_rewriter_agent
from haive.agents.rag.agentic.react_rag_agent import ReactRAGAgent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.simple import SimpleAgent


class AgenticRAGState(MessagesState):
    """State for the Agentic RAG workflow."""

    # Query and refinement
    original_query: str = Field(default="", description="Original user query")
    refined_query: str = Field(default="", description="Refined query after rewriting")
    query_rewrite_count: int = Field(default=0, description="Number of query rewrites")

    # Retrieved documents
    retrieved_documents: list[dict[str, Any]] = Field(
        default_factory=list, description="Documents retrieved from vector store"
    )

    # Graded documents
    graded_documents: list[dict[str, Any]] = Field(
        default_factory=list, description="Documents after relevance grading"
    )

    relevant_documents: list[dict[str, Any]] = Field(
        default_factory=list, description="Only the relevant documents"
    )

    # Web search results
    web_search_results: list[dict[str, Any]] = Field(
        default_factory=list, description="Results from web search if needed"
    )

    # Control flow
    all_documents_relevant: bool = Field(
        default=True, description="Whether all retrieved documents are relevant"
    )

    use_web_search: bool = Field(default=False, description="Whether to use web search")

    # Final answer
    final_answer: str = Field(default="", description="Final generated answer")


class AgenticRAGAgent(SimpleAgent):
    """Advanced Agentic RAG system with document grading and query refinement.

    This agent implements a sophisticated RAG workflow that includes:
    1. Initial retrieval from vector store
    2. Document relevance grading
    3. Query rewriting if documents aren't relevant
    4. Web search fallback
    5. Final answer generation

    Example:
        .. code-block:: python

            # Create agentic RAG agent
            agent = AgenticRAGAgent.create_default(
            name="agentic_rag",
            retriever_config=vector_store_config,
            use_web_search=True
            )

            # Process a query
            result = await agent.arun("What are the latest advances in quantum computing?")

            # The agent will:
            # 1. Retrieve documents from vector store
            # 2. Grade them for relevance
            # 3. Rewrite query if needed
            # 4. Use web search if local docs aren't sufficient
            # 5. Generate comprehensive answer

    """

    # Component configurations
    retriever_config: BaseRetrieverConfig | VectorStoreConfig = Field(
        ..., description="Retriever configuration for document retrieval"
    )

    grader_agent: Any | None = Field(
        default=None, description="Agent for grading document relevance"
    )

    rewriter_agent: Any | None = Field(
        default=None, description="Agent for query refinement"
    )

    generator_agent: SimpleAgent | None = Field(
        default=None, description="Agent for final answer generation"
    )

    web_search_agent: ReactRAGAgent | None = Field(
        default=None, description="Agent for web search fallback"
    )

    # Workflow configuration
    max_query_rewrites: int = Field(
        default=1, description="Maximum number of query rewrite attempts"
    )

    use_web_search: bool = Field(
        default=True, description="Whether to use web search as fallback"
    )

    relevance_threshold: float = Field(
        default=0.7, description="Minimum relevance score for documents"
    )

    @classmethod
    def create_default(cls, **kwargs) -> "AgenticRAGAgent":
        """Create a default Agentic RAG agent.

        Args:
            **kwargs: Configuration options
                - name: Agent name
                - retriever_config: Retriever or vector store config (required)
                - use_web_search: Whether to enable web search fallback
                - temperature: LLM temperature
                - engine: Custom AugLLMConfig if needed

        Returns:
            AgenticRAGAgent configured for advanced RAG
        """
        # Extract required config
        name = kwargs.pop("name", "agentic_rag")
        retriever_config = kwargs.pop("retriever_config")
        if not retriever_config:
            raise ValueError("retriever_config is required for AgenticRAGAgent")

        # Extract optional config
        temperature = kwargs.pop("temperature", 0.1)
        use_web_search = kwargs.pop("use_web_search", True)

        # Create component agents
        grader_agent = create_document_grader_agent(
            name=f"{name}_grader", temperature=0.0  # Consistent grading
        )

        rewriter_agent = create_query_rewriter_agent(
            name=f"{name}_rewriter", temperature=0.7  # Creative rewriting
        )

        # Create generator agent
        generator_engine = AugLLMConfig(
            temperature=temperature,
            system_message=(
                "You are an expert at generating comprehensive answers based on retrieved information.\n\n"
                "Guidelines:\n"
                "1. Use the provided documents to answer the query\n"
                "2. Synthesize information from multiple sources\n"
                "3. Be accurate and cite sources when possible\n"
                "4. If information is incomplete, acknowledge limitations\n"
                "5. Provide a clear, well-structured response"
            ),
        )

        generator_agent = SimpleAgent(name=f"{name}_generator", engine=generator_engine)

        # Create web search agent if enabled
        web_search_agent = None
        if use_web_search:
            web_search_tool = cls._create_web_search_tool()
            web_search_agent = ReactRAGAgent.create_default(
                name=f"{name}_web_search", tools=[web_search_tool], temperature=0.3
            )

        # Create main engine
        engine = kwargs.pop("engine", None)
        if engine is None:
            engine = AugLLMConfig(
                temperature=temperature,
                system_message="You are an advanced RAG system coordinator.",
            )

        return cls(
            name=name,
            engine=engine,
            retriever_config=retriever_config,
            grader_agent=grader_agent,
            rewriter_agent=rewriter_agent,
            generator_agent=generator_agent,
            web_search_agent=web_search_agent,
            use_web_search=use_web_search,
            **kwargs,
        )

    @staticmethod
    def _create_web_search_tool():
        """Create a mock web search tool for demonstration."""

        @tool
        def web_search(query: str) -> str:
            """Search the web for current information.

            Args:
                query: Search query

            Returns:
                Search results as a string
            """
            # In a real implementation, this would call a web search API
            return (
                f"Web search results for '{query}':\n\n"
                "1. Recent developments in the field (2024)\n"
                "2. Latest research papers and findings\n"
                "3. Current industry applications\n"
                "4. Expert opinions and analysis\n\n"
                "Note: This is a mock implementation. "
                "Replace with actual web search API integration."
            )

        return web_search

    def build_graph(self) -> BaseGraph:
        """Build the Agentic RAG workflow graph."""
        # Create base graph
        graph = BaseGraph(name=f"{self.name}_graph")

        # Add nodes
        graph.add_node("retrieve", self._retrieve_documents)
        graph.add_node("grade_documents", self._grade_documents)
        graph.add_node("rewrite_query", self._rewrite_query)
        graph.add_node("web_search", self._web_search)
        graph.add_node("generate_answer", self._generate_answer)

        # Add edges
        graph.add_edge(START, "retrieve")
        graph.add_edge("retrieve", "grade_documents")

        # Conditional routing after grading
        graph.add_conditional_edges(
            "grade_documents",
            self._route_after_grading,
            {
                "generate": "generate_answer",
                "rewrite": "rewrite_query",
                "web_search": "web_search",
            },
        )

        # After rewriting, retrieve again
        graph.add_edge("rewrite_query", "retrieve")

        # After web search, generate answer
        graph.add_edge("web_search", "generate_answer")

        # End after generating answer
        graph.add_edge("generate_answer", END)

        return graph

    async def _retrieve_documents(self, state: AgenticRAGState) -> dict[str, Any]:
        """Retrieve documents using the RAG agent."""
        # Use refined query if available, otherwise original
        query = state.refined_query or state.original_query

        # Create retriever agent
        retriever = BaseRAGAgent(name="retriever", engine=self.retriever_config)

        # Retrieve documents
        result = await retriever.arun({"query": query})

        # Extract documents from result
        documents = []
        if isinstance(result, dict):
            documents = result.get("documents", result.get("retrieved_documents", []))

        return {
            "retrieved_documents": documents,
            "messages": [
                *state.messages,
                AIMessage(
                    content=f"Retrieved {len(documents)} documents for query: {query}"
                ),
            ],
        }

    async def _grade_documents(self, state: AgenticRAGState) -> dict[str, Any]:
        """Grade retrieved documents for relevance."""
        if not self.grader_agent:
            # Skip grading if no grader agent
            return {
                "graded_documents": state.retrieved_documents,
                "relevant_documents": state.retrieved_documents,
                "all_documents_relevant": True,
            }

        # Grade documents
        query = state.refined_query or state.original_query
        grading_result = await self.grader_agent.grade_documents(
            query=query,
            documents=[
                {
                    "id": f"doc_{i}",
                    "content": doc.get("content", doc.get("page_content", "")),
                }
                for i, doc in enumerate(state.retrieved_documents)
            ],
        )

        # Process grading results
        relevant_docs = []
        all_relevant = True

        for i, decision in enumerate(grading_result.document_decisions):
            if decision.decision == "pass":
                relevant_docs.append(state.retrieved_documents[i])
            else:
                all_relevant = False

        return {
            "graded_documents": state.retrieved_documents,
            "relevant_documents": relevant_docs,
            "all_documents_relevant": all_relevant,
            "messages": [
                *state.messages,
                AIMessage(
                    content=f"Graded {len(state.retrieved_documents)} documents. {len(relevant_docs)} are relevant."
                ),
            ],
        }

    def _route_after_grading(self, state: AgenticRAGState) -> str:
        """Determine next step after document grading."""
        # If we have relevant documents, generate answer
        if state.relevant_documents and len(state.relevant_documents) >= 2:
            return "generate"

        # If we haven't rewritten query yet, try that
        if state.query_rewrite_count < self.max_query_rewrites:
            return "rewrite"

        # If web search is enabled, use it
        if self.use_web_search:
            return "web_search"

        # Otherwise, generate with what we have
        return "generate"

    async def _rewrite_query(self, state: AgenticRAGState) -> dict[str, Any]:
        """Rewrite the query for better retrieval."""
        if not self.rewriter_agent:
            return {"query_rewrite_count": state.query_rewrite_count + 1}

        # Rewrite query
        query = state.refined_query or state.original_query
        rewrite_result = await self.rewriter_agent.rewrite_query(
            query=query,
            context="Previous retrieval returned insufficient relevant documents.",
        )

        return {
            "refined_query": rewrite_result.best_refined_query,
            "query_rewrite_count": state.query_rewrite_count + 1,
            "messages": [
                *state.messages,
                AIMessage(
                    content=f"Rewrote query from '{query}' to '{rewrite_result.best_refined_query}'"
                ),
            ],
        }

    async def _web_search(self, state: AgenticRAGState) -> dict[str, Any]:
        """Perform web search as fallback."""
        if not self.web_search_agent:
            return {"web_search_results": []}

        # Search with the best query we have
        query = state.refined_query or state.original_query
        search_result = await self.web_search_agent.arun(f"Search for: {query}")

        # Parse search results
        web_results = [
            {
                "content": search_result,
                "source": "web_search",
                "metadata": {"query": query},
            }
        ]

        return {
            "web_search_results": web_results,
            "messages": [
                *state.messages,
                AIMessage(content=f"Performed web search for: {query}"),
            ],
        }

    async def _generate_answer(self, state: AgenticRAGState) -> dict[str, Any]:
        """Generate final answer using all available information."""
        if not self.generator_agent:
            return {"final_answer": "No generator agent available."}

        # Combine all available documents
        all_docs = state.relevant_documents + state.web_search_results

        # Format context for generation
        context = "Based on the following information:\n\n"
        for i, doc in enumerate(all_docs, 1):
            content = doc.get("content", doc.get("page_content", ""))
            source = doc.get("source", doc.get("metadata", {}).get("source", "Unknown"))
            context += f"[{i}] Source: {source}\n{content}\n\n"

        # Generate answer
        query = state.refined_query or state.original_query
        generation_prompt = (
            f"Query: {query}\n\n"
            f"{context}\n"
            "Please provide a comprehensive answer to the query based on the above information."
        )

        answer = await self.generator_agent.arun(generation_prompt)

        return {
            "final_answer": answer,
            "messages": [*state.messages, AIMessage(content=answer)],
        }
