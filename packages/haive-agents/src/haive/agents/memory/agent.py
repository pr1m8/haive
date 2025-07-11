import json
import logging
from datetime import datetime
from typing import Any

from agents.memory_agent.memory_utils import (
    create_memory_vectorstore,
    get_user_id_from_state,
    retrieve_memories,
    save_structured_memories,
    save_unstructured_memories,
)
from agents.react.memory.config import MemoryAgentConfig
from agents.react.react.agent import ReactAgent
from haive.core.engine.agent.agent import register_agent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import END

logger = logging.getLogger(__name__)


@register_agent(MemoryAgentConfig)
class MemoryAgent(ReactAgent):
    """Memory Agent implementation that extends ReactAgent.

    Adds long-term memory capabilities for persisting information
    about users across conversations.
    """

    def __init__(self, config: MemoryAgentConfig):
        """Initialize the Memory Agent with its configuration."""
        # Initialize vector store if not provided
        if not config.vector_store:
            config.vector_store = create_memory_vectorstore()

        super().__init__(config)
        self.config = config

        # Initialize memory tools
        self._init_memory_tools()

    def _init_memory_tools(self):
        """Initialize memory-related tools."""
        # Add memory tools to the existing tools
        from langchain_core.tools import StructuredTool

        def save_memory(memory: str) -> str:
            """Tool to save a memory."""
            # Extract user_id from runtime config
            try:
                user_id = self._get_current_user_id()
                save_unstructured_memories([memory], self.config.vector_store, user_id)
                return f"Memory saved: {memory}"
            except Exception as e:
                logger.exception(f"Error saving memory: {e}")
                return f"Error saving memory: {e!s}"

        def save_structured_memory(subject: str, predicate: str, object_: str) -> str:
            """Tool to save a structured memory."""
            try:
                user_id = self._get_current_user_id()
                triple = {
                    "subject": subject,
                    "predicate": predicate,
                    "object_": object_,
                }
                save_structured_memories([triple], self.config.vector_store, user_id)
                return f"Structured memory saved: {subject} {predicate} {object_}"
            except Exception as e:
                logger.exception(f"Error saving structured memory: {e}")
                return f"Error saving structured memory: {e!s}"

        def recall_memory(query: str) -> list[str]:
            """Tool to recall memories."""
            try:
                user_id = self._get_current_user_id()
                memories = retrieve_memories(
                    query,
                    self.config.vector_store,
                    user_id,
                    limit=self.config.max_memories_per_retrieval,
                )
                return memories
            except Exception as e:
                logger.exception(f"Error recalling memories: {e}")
                return []

        # Create structured tools
        memory_save_tool = StructuredTool.from_function(
            func=save_memory,
            name="save_memory",
            description="Save an important fact or detail about the user for future reference",
            return_direct=False,
        )

        structured_memory_save_tool = StructuredTool.from_function(
            func=save_structured_memory,
            name="save_structured_memory",
            description="Save a structured fact as a knowledge triple (subject, predicate, object)",
            return_direct=False,
        )

        memory_recall_tool = StructuredTool.from_function(
            func=recall_memory,
            name="recall_memories",
            description="Search for relevant memories about the current user",
            return_direct=False,
        )

        # Add memory tools to existing tools
        memory_tools = [memory_save_tool, memory_recall_tool]

        # Add structured memory tool if configured
        if self.config.memory_type in ["structured", "both"]:
            memory_tools.append(structured_memory_save_tool)

        # Extend tools list with memory tools
        self.tools.extend(memory_tools)

        # Rebuild the tool mapping
        self.tool_mapping = {tool.name: tool for tool in self.tools}

    def _get_current_user_id(self) -> str:
        """Get the current user ID from runtime config."""
        # First check if it's in the runtime config
        if hasattr(self, "current_user_id") and self.current_user_id:
            return self.current_user_id

        # Try to get from config
        try:
            runtime_config = self.config.runnable_config
            if runtime_config and "configurable" in runtime_config:
                user_id = runtime_config["configurable"].get("user_id")
                if user_id:
                    self.current_user_id = user_id
                    return user_id
        except Exception:
            pass

        # Default user ID
        default_id = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.current_user_id = default_id
        return default_id

    def setup_workflow(self) -> None:
        """Set up the workflow graph with memory management nodes."""
        logger.debug(f"Setting up workflow for MemoryAgent {self.config.name}")

        # Create dynamic graph builder
        gb = DynamicGraph(
            components=[self.config.engine], state_schema=self.config.state_schema
        )

        # Add memory loading node
        gb.add_node(
            name=self.config.memory_load_node_name,
            config=self._load_memories,
            command_goto="extract_query",
        )
        gb.set_entry_point(self.config.memory_load_node_name)

        # Add query extraction node
        gb.add_node(
            "extract_query", self._extract_query, self.config.memory_extract_node_name
        )

        # Add memory extraction node
        gb.add_node(
            name=self.config.memory_extract_node_name,
            config=self._extract_memories,
            command_goto="add_system",
        )

        # Add system message if provided
        if self.config.system_prompt or self.config.memory_system_prompt:
            self._add_memory_system_message_node(gb)

        # Set up the LLM with tool binding
        self._setup_llm_node(gb)

        # Set up tool execution
        if self.version == "v1":
            self._setup_tools_v1(gb)
        else:
            self._setup_tools_v2(gb)

        # Add memory saving node
        gb.add_node(
            name=self.config.memory_save_node_name,
            config=self._save_memories,
            command_goto=END,
        )

        # Modify the standard flow to include memory saving
        # We want the LLM to return to memory extraction after tool execution
        try:
            gb.remove_edge(self.config.tool_node_name, self.config.llm_node_name)
            gb.add_edge(
                self.config.tool_node_name, self.config.memory_extract_node_name
            )
        except Exception as e:
            logger.warning(f"Error modifying tool flow: {e}")

        # Add edge from LLM to memory saving
        gb.add_conditional_edges(
            self.config.llm_node_name,
            self._route_after_llm,
            {
                self.config.tool_node_name: self.config.tool_node_name,
                self.config.memory_save_node_name: self.config.memory_save_node_name,
            },
        )

        # Add structured output node if schema provided
        if self.config.structured_output_schema:
            self._add_structured_output_node(gb)

            # Ensure structured output node is after memory saving
            try:
                gb.remove_edge(self.config.llm_node_name, self.config.output_node_name)
                gb.add_edge(
                    self.config.memory_save_node_name, self.config.output_node_name
                )
            except Exception as e:
                logger.warning(f"Error modifying structured output flow: {e}")

        # Build the graph
        self.graph = gb.build()
        logger.info(f"Set up Memory Agent workflow for {self.config.name}")

    def _load_memories(self, state: dict[str, Any]) -> dict[str, Any]:
        """Load relevant memories for the current user.

        Args:
            state: Current state

        Returns:
            Updated state with loaded memories
        """
        try:
            # Extract user ID from state or config
            user_id = get_user_id_from_state(state)
            if not user_id:
                user_id = self._get_current_user_id()

            # Save user ID in state
            result = {"user_id": user_id}

            # Check if we have messages or a query to search with
            query = state.get("query", "")
            messages = state.get("messages", [])

            # If we have messages but no query, extract query from last message
            if not query and messages:
                # Get the last message content
                for msg in reversed(messages):
                    if isinstance(msg, HumanMessage) or (
                        isinstance(msg, tuple) and msg[0] == "human"
                    ):
                        content = msg.content if hasattr(msg, "content") else msg[1]
                        query = str(content)
                        break

            # If we have a query, retrieve relevant memories
            if query:
                memories = retrieve_memories(
                    query,
                    self.config.vector_store,
                    user_id,
                    limit=self.config.max_memories_per_retrieval,
                )

                # Add to result
                result["recall_memories"] = memories
                logger.info(f"Loaded {len(memories)} memories for user {user_id}")
            else:
                # No query, set empty memories
                result["recall_memories"] = []

            return result

        except Exception as e:
            logger.exception(f"Error loading memories: {e}")
            return {"recall_memories": [], "user_id": self._get_current_user_id()}

    def _extract_query(self, state: dict[str, Any]) -> dict[str, Any]:
        """Extract query from messages and store in state.

        Args:
            state: Current state with messages

        Returns:
            Updated state with extracted query
        """
        # Extract the query from messages
        query = ""
        messages = state.get("messages", [])

        if messages:
            # Look for the last human message
            for msg in reversed(messages):
                if isinstance(msg, HumanMessage) or (
                    isinstance(msg, tuple) and msg[0] == "human"
                ):
                    content = msg.content if hasattr(msg, "content") else msg[1]
                    query = str(content)
                    break

        # Only update if we found a query
        if query:
            return {"query": query}

        return {}

    def _extract_memories(self, state: dict[str, Any]) -> dict[str, Any]:
        """Extract memories from conversation.

        Args:
            state: Current state with messages

        Returns:
            Updated state with extracted memories
        """
        # Skip if memory extraction is disabled
        if not state.get("should_save_memories", True):
            return {}

        # Check if we have messages
        messages = state.get("messages", [])
        if not messages:
            return {}

        memory_type = state.get("memory_type", self.config.memory_type)

        # Use the memory extraction engine if provided, otherwise use the main engine
        extraction_engine = self.config.memory_extraction_engine or self.config.engine

        try:
            # Create a prompt for memory extraction
            if memory_type == "structured":
                prompt_template = (
                    self.config.memory_extraction_prompt
                    or """
                Extract important information from the conversation as structured knowledge triples.
                Format: [{"subject": "entity1", "predicate": "relation", "object_": "entity2"}]

                Extract only facts that would be useful to remember for future conversations.
                Focus on personal preferences, facts about the user, important events, etc.
                """
                )
            else:
                prompt_template = (
                    self.config.memory_extraction_prompt
                    or """
                Extract important information from the conversation as natural language statements.
                Format each memory as a separate, self-contained statement.

                Extract only facts that would be useful to remember for future conversations.
                Focus on personal preferences, facts about the user, important events, etc.
                """
                )

            # Create a complete prompt with conversation history
            conversation_str = "\n".join(
                [
                    f"{msg.type if hasattr(msg, 'type') else msg[0]}: {msg.content if hasattr(msg, 'content') else msg[1]}"
                    for msg in messages
                ]
            )

            full_prompt = f"{prompt_template}\n\nConversation:\n{conversation_str}"

            # Extract memories using the engine
            if isinstance(extraction_engine, AugLLMConfig):
                llm = extraction_engine.create_runnable()
                extraction_result = llm.invoke(full_prompt)
            else:
                # Assume it's already a runnable
                extraction_result = extraction_engine.invoke(full_prompt)

            # Process the extraction result
            extracted_content = (
                extraction_result.content
                if hasattr(extraction_result, "content")
                else str(extraction_result)
            )

            # Parse the extracted memories
            if memory_type == "structured":
                # Try to parse as JSON
                try:
                    # Look for JSON array in the output
                    import re

                    json_match = re.search(r"\[.*\]", extracted_content, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(0)
                        structured_memories = json.loads(json_str)

                        # Ensure they're in the right format
                        valid_memories = []
                        for memory in structured_memories:
                            if isinstance(memory, dict) and all(
                                k in memory for k in ["subject", "predicate", "object_"]
                            ):
                                valid_memories.append(memory)

                        if valid_memories:
                            return {"extracted_memories": valid_memories}
                except Exception as e:
                    logger.exception(f"Error parsing structured memories: {e}")
                    # Fall back to unstructured extraction

            # Unstructured memory extraction
            # Split by newlines and filter out empty lines
            unstructured_memories = [
                line.strip()
                for line in extracted_content.split("\n")
                if line.strip()
                and not line.strip().startswith("```")
                and not line.strip().endswith("```")
            ]

            if unstructured_memories:
                return {"extracted_memories": unstructured_memories}

        except Exception as e:
            logger.exception(f"Error extracting memories: {e}")

        return {}

    def _save_memories(self, state: dict[str, Any]) -> dict[str, Any]:
        """Save extracted memories to vector store.

        Args:
            state: Current state with extracted memories

        Returns:
            Updated state
        """
        # Skip if memory saving is disabled
        if not state.get("should_save_memories", True):
            return {}

        # Get extracted memories
        extracted_memories = state.get("extracted_memories", [])
        if not extracted_memories:
            return {}

        # Get user ID
        user_id = state.get("user_id") or self._get_current_user_id()

        try:
            # Determine memory type
            memory_type = state.get("memory_type", self.config.memory_type)

            # Save memories based on type
            if memory_type == "structured":
                # Save as structured memories
                structured_memories = []

                for memory in extracted_memories:
                    if isinstance(memory, dict) and all(
                        k in memory for k in ["subject", "predicate", "object_"]
                    ):
                        structured_memories.append(memory)
                    elif isinstance(memory, str):
                        # Try to parse string as JSON
                        try:
                            memory_dict = json.loads(memory)
                            if all(
                                k in memory_dict
                                for k in ["subject", "predicate", "object_"]
                            ):
                                structured_memories.append(memory_dict)
                        except:
                            # Skip invalid memories
                            pass

                if structured_memories:
                    save_structured_memories(
                        structured_memories, self.config.vector_store, user_id
                    )
                    logger.info(f"Saved {len(structured_memories)} structured memories")

            else:  # unstructured
                # Save as unstructured memories
                unstructured_memories = []

                for memory in extracted_memories:
                    if isinstance(memory, str):
                        unstructured_memories.append(memory)
                    elif isinstance(memory, dict) and "content" in memory:
                        unstructured_memories.append(memory["content"])

                if unstructured_memories:
                    save_unstructured_memories(
                        unstructured_memories, self.config.vector_store, user_id
                    )
                    logger.info(
                        f"Saved {len(unstructured_memories)} unstructured memories"
                    )

        except Exception as e:
            logger.exception(f"Error saving memories: {e}")

        # Clear extracted memories to avoid re-saving
        return {"extracted_memories": []}

    def _add_memory_system_message_node(self, gb: DynamicGraph) -> None:
        """Add a node for adding a memory-enhanced system message."""

        def add_system_message(state: dict[str, Any]) -> dict[str, Any]:
            """Add system message with memory context."""
            messages = state.get("messages", [])

            # Check if we already have a system message
            has_system = any(
                isinstance(m, SystemMessage)
                for m in messages
                if isinstance(m, BaseMessage)
            )

            if not has_system:
                # Get memories
                memories = state.get("recall_memories", [])
                memories_str = (
                    "\n".join([f"- {memory}" for memory in memories])
                    if memories
                    else "No relevant memories."
                )

                # Create system message with memories
                system_prompt = (
                    self.config.memory_system_prompt or self.config.system_prompt
                )
                if not system_prompt:
                    system_prompt = (
                        "You are a helpful assistant with memory capabilities."
                    )

                # Replace memory placeholder
                system_content = system_prompt.replace(
                    "{recall_memories}", memories_str
                )

                # Create system message
                system_msg = SystemMessage(content=system_content)

                # Return updated messages list
                return {"messages": [system_msg]}

            return {}

        # Add the node and connect it
        gb.add_node("add_system", add_system_message, self.config.llm_node_name)

    def _route_after_llm(self, state: dict[str, Any]) -> str:
        """Determine where to route after the LLM node.

        Args:
            state: Current state

        Returns:
            Next node name
        """
        # Check if the last message has tool calls
        messages = state.get("messages", [])
        if not messages:
            return self.config.memory_save_node_name

        last_message = messages[-1]
        if isinstance(last_message, AIMessage) and getattr(
            last_message, "tool_calls", None
        ):
            return self.config.tool_node_name

        # No tool calls, go to memory saving
        return self.config.memory_save_node_name

    def run(
        self, input_data: str | dict[str, Any], user_id: str | None = None, **kwargs
    ) -> dict[str, Any]:
        """Run the memory agent.

        Args:
            input_data: Input query or state
            user_id: Optional user ID for memory context
            **kwargs: Additional parameters

        Returns:
            Result from agent execution
        """
        # Store current user ID
        self.current_user_id = user_id

        # Ensure we have a configurable section in runtime config
        runtime_config = kwargs.get("runtime_config", {}) or self.config.runnable_config
        if "configurable" not in runtime_config:
            runtime_config["configurable"] = {}

        # Add user ID to runtime config
        if user_id:
            runtime_config["configurable"]["user_id"] = user_id

        # Convert string to messages if needed
        if isinstance(input_data, str):
            input_data = {"messages": [HumanMessage(content=input_data)]}

        # Add memory configuration if needed
        if "should_save_memories" not in input_data:
            input_data["should_save_memories"] = True

        if "memory_type" not in input_data:
            input_data["memory_type"] = self.config.memory_type

        # Run agent with memory context
        return super().run(input_data, runtime_config=runtime_config, **kwargs)
