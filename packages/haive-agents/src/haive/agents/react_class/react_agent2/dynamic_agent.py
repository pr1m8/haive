# src/haive/agents/react_agent2/dynamic_agent.py

"""Dynamic React Agent - an extension of React agent with tool selection capabilities."""
import logging
import uuid
from typing import Any

from agents.react_agent2.agent2 import ReactAgent
from agents.react_agent2.config2 import ReactAgentConfig
from agents.react_agent2.state2 import ReactAgentState
from haive.core.engine.agent.agent import register_agent
from haive.core.graph.branches import Branch
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from haive.core.models.vectorstore.base import VectorStoreConfig
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import BaseTool
from langchain_openai import AzureOpenAIEmbeddings, OpenAIEmbeddings
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END
from pydantic import BaseModel, Field

# Set up logging
logger = logging.getLogger(__name__)


# Define a schema extension for DynamicReactAgent
class DynamicReactAgentState(ReactAgentState):
    """Extended schema for dynamic tool selection."""

    selected_tools: list[str] = Field(
        default_factory=list,
        description="IDs of tools selected for the current interaction",
    )
    tool_registry: dict[str, Any] = Field(
        default_factory=dict, description="Registry of all available tools"
    )
    # Pass through tool call ID to fix the bug in the original implementation
    tool_call_id: str | None = Field(default=None, description="Current tool call ID")

    model_config = {"arbitrary_types_allowed": True}


class DynamicReactAgentConfig(ReactAgentConfig):
    """Configuration for a React agent with dynamic tool selection.

    This agent can handle a large number of tools by dynamically selecting
    which tools to make available to the LLM based on the context.
    """

    # Node configuration - Define our additional node
    tool_selection_node_name: str = Field(
        default="select_tools", description="Name for the tool selection node."
    )

    # Tool selection configuration
    tool_embedding_model: str = Field(
        default="text-embedding-ada-002",
        description="Embedding model for tool descriptions.",
    )

    max_tools_per_turn: int = Field(
        default=5, description="Maximum number of tools to select per interaction."
    )

    # Override state schema to use our extended schema
    state_schema: type[BaseModel] = Field(
        default=DynamicReactAgentState, description="Schema for the agent state."
    )

    # Repeat tool selection behavior
    repeat_selection: bool = Field(
        default=True,
        description="Whether to repeat tool selection after getting tool results.",
    )

    # Vector store configuration
    vector_store_config: VectorStoreConfig | None = Field(
        default=None, description="Vector store configuration for tool embeddings."
    )

    # Tool documents (stored separately from vector store config to avoid validation issues)
    tool_documents: list[Document] | None = Field(
        default=None,
        description="Documents for tool descriptions to be stored in vector store.",
    )

    # Model config to allow arbitrary types
    model_config = {"arbitrary_types_allowed": True}

    @classmethod
    def from_tools(
        cls,
        tools: list[BaseTool],
        system_prompt: str | None = None,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        name: str | None = None,
        max_tools_per_turn: int = 5,
        max_iterations: int = 10,
        response_format: type[BaseModel] | dict[str, Any] | None = None,
        use_memory: bool = True,
        visualize: bool = True,
        repeat_selection: bool = True,
        **kwargs,
    ) -> "DynamicReactAgentConfig":
        """Create a DynamicReactAgentConfig from a list of tools.

        Args:
            tools: List of tools to use
            system_prompt: Optional system prompt
            model: Model name
            temperature: Temperature for generation
            name: Optional agent name
            max_tools_per_turn: Maximum number of tools to select per turn
            max_iterations: Maximum iterations for React agent
            response_format: Optional structured output model
            use_memory: Whether to use memory
            visualize: Whether to visualize the graph
            repeat_selection: Whether to repeat tool selection after each tool invocation
            **kwargs: Additional kwargs for the config

        Returns:
            DynamicReactAgentConfig instance
        """
        # Get a base React agent config first
        base_config = ReactAgentConfig.from_tools(
            tools=tools,
            system_prompt=system_prompt,
            model=model,
            temperature=temperature,
            name=name or f"dynamic_react_agent_{uuid.uuid4().hex[:8]}",
            max_iterations=max_iterations,
            response_format=response_format,
            use_memory=use_memory,
            visualize=visualize,
            **kwargs,
        )

        # Convert to our config type by using the dict
        config_dict = base_config.model_dump()

        # Add our specific fields
        config_dict.update(
            {
                "max_tools_per_turn": max_tools_per_turn,
                "repeat_selection": repeat_selection,
                "state_schema": DynamicReactAgentState,
            }
        )

        # Create our config
        return cls(**config_dict)


@register_agent(DynamicReactAgentConfig)
class DynamicReactAgent(ReactAgent):
    """A React agent with dynamic tool selection.

    This agent extends the React pattern with dynamic tool selection,
    making it efficient when dealing with a large number of tools.
    """

    def __init__(self, config: DynamicReactAgentConfig):
        """Initialize the dynamic react agent."""
        # Set up tool registry and embeddings before initializing parent
        self.tools = config.tools
        self.tool_registry = {}
        self._vector_store = None
        self.vector_store_config = config.vector_store_config

        # Initialize embeddings for tool selection
        if self.vector_store_config:
            # We'll initialize the vector store later
            self.embeddings = None
        else:
            # Default OpenAI embeddings if no config provided
            self.embeddings = OpenAIEmbeddings()

        # Initialize parent class
        super().__init__(config)

        # Register tools if not done yet
        if not self.tool_registry and self.tools:
            self.register_tools(self.tools)

    def setup_workflow(self) -> None:
        """Set up the workflow with dynamic tool selection."""
        logger.info(f"Setting up workflow for DynamicReactAgent {self.config.name}")

        # Create DynamicGraph with our state schema
        graph_builder = DynamicGraph(state_schema=self.state_schema)

        # 1. Add the tool selection node first
        graph_builder.add_node(
            name=self.config.tool_selection_node_name,
            config=self._create_tool_selection_function,
            command_goto=self.config.agent_node_name,
        )

        # 2. Add agent node (LLM reasoning)
        graph_builder.add_node(
            name=self.config.agent_node_name, config=self.config.engine
        )

        # 3. Create a ToolNode to handle tool execution
        # Fix the tool_call_id handling issue in the original implementation
        tool_node = self._create_fixed_tool_node()

        # Add the tool node to the graph
        graph_builder.add_node(name=self.config.tools_node_name, config=tool_node)

        # 4. Create structure output node if needed
        if self.config.response_format:
            structured_node = self._create_structured_output_node()
            graph_builder.add_node(
                name="structured_output_node", config=structured_node, command_goto=END
            )

        # 5. Define branch for conditional routing
        def has_tool_calls(state):
            """Check if the last message has tool calls."""
            messages = state.get("messages", [])
            if not messages:
                return False

            last_message = messages[-1]

            if isinstance(last_message, AIMessage):
                # Check direct tool_calls attribute
                if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                    return True

                # Check in additional_kwargs
                if (
                    hasattr(last_message, "additional_kwargs")
                    and "tool_calls" in last_message.additional_kwargs
                    and last_message.additional_kwargs["tool_calls"]
                ):
                    return True

            # Dict format
            elif isinstance(last_message, dict) and last_message.get("type") == "ai":
                if (
                    "tool_calls" in last_message.get("additional_kwargs", {})
                    and last_message["additional_kwargs"]["tool_calls"]
                ):
                    return True

            return False

        branch = Branch(
            function=lambda state: (
                self.config.tools_node_name
                if has_tool_calls(state)
                else "structured_output_node" if self.config.response_format else END
            ),
            destinations={
                self.config.tools_node_name: self.config.tools_node_name,
                "structured_output_node": (
                    "structured_output_node" if self.config.response_format else END
                ),
                END: END,
            },
            default=END,
        )

        # 6. Add conditional edge from agent to tools or end
        graph_builder.add_conditional_edges(self.config.agent_node_name, branch)

        # 7. Add edge from tools back to either agent or tool selection based on config
        if self.config.repeat_selection:
            graph_builder.add_edge(
                self.config.tools_node_name, self.config.tool_selection_node_name
            )
        else:
            graph_builder.add_edge(
                self.config.tools_node_name, self.config.agent_node_name
            )

        # 8. Set entry point to the tool selection node
        graph_builder.set_entry_point(self.config.tool_selection_node_name)

        # 9. Build and compile the graph
        self.graph = graph_builder.build()

        # 10. Use memory saver if specified
        checkpointer = MemorySaver() if self.config.use_memory else None
        self.compile(checkpointer=checkpointer)

        logger.info(f"Workflow set up successfully for {self.config.name}")

    def register_tools(self, tools: list[BaseTool]) -> None:
        """Register tools with the agent and create tool embeddings.

        Args:
            tools: List of tools to register
        """
        self.tools = tools

        # Create tool registry with unique IDs
        self.tool_registry = {str(uuid.uuid4()): tool for tool in tools}

        # Create documents for embedding if not provided in config
        if self.config.tool_documents:
            tool_documents = self.config.tool_documents
            logger.info(
                f"Using {len(tool_documents)} pre-created tool documents from src.config"
            )
        else:
            tool_documents = [
                Document(
                    page_content=tool.description, metadata={"tool_name": tool.name}
                )
                for tool in tools
            ]
            logger.info(f"Created {len(tool_documents)} tool documents from tools")

        # Initialize vector store
        if self.vector_store_config:
            # Create vector store using the config
            try:
                # Create the embeddings model if needed
                if not self.embeddings:
                    embedding_model = self.vector_store_config.embedding_model
                    # Use the model from the config
                    self.embeddings = AzureOpenAIEmbeddings(
                        model=embedding_model.model,
                        api_key=embedding_model.api_key,
                        azure_endpoint=embedding_model.api_base,
                        api_version=embedding_model.api_version,
                    )
                    logger.info(
                        f"Created Azure OpenAI embeddings with model {embedding_model.model}"
                    )

                # Create a new in-memory vector store with the embeddings
                from langchain_community.vectorstores import Chroma

                self._vector_store = Chroma.from_documents(
                    documents=tool_documents,
                    embedding=self.embeddings,
                    collection_name="dynamic_react_agent_tools",
                )
                logger.info(
                    "Created vector store for tool selection using provided config"
                )

            except Exception as e:
                logger.error(f"Error creating vector store from src.config: {e}")
                # Fall back to in-memory vector store
                self._initialize_in_memory_vector_store(tool_documents)
        else:
            # Create in-memory vector store
            self._initialize_in_memory_vector_store(tool_documents)

        logger.info(f"Registered {len(tools)} tools with {self.config.name}")

    def _initialize_in_memory_vector_store(self, tool_documents: list[Document]):
        """Initialize an in-memory vector store with the tool documents."""
        from langchain_core.vectorstores import InMemoryVectorStore

        # Create embeddings if needed
        if not self.embeddings:
            self.embeddings = OpenAIEmbeddings()

        # Create vector store
        self._vector_store = InMemoryVectorStore(embedding=self.embeddings)

        # Add documents to vector store
        for tool_id, document in zip(
            self.tool_registry.keys(), tool_documents, strict=False
        ):
            self._vector_store.add_texts(
                texts=[document.page_content],
                metadatas=[
                    {"tool_id": tool_id, "tool_name": document.metadata["tool_name"]}
                ],
            )

        logger.info("Initialized in-memory vector store for tool selection")

    @property
    def vector_store(self):
        """Get the vector store property."""
        return self._vector_store

    def _create_tool_selection_function(self, state):
        """Create a function that selects tools based on the context."""
        # Return if no vector store
        if self.vector_store is None:
            logger.warning("No vector store available for tool selection")
            return state

        # Extract user query from last message
        last_message = None
        if state.get("messages") and len(state["messages"]) > 0:
            for message in reversed(state["messages"]):
                if isinstance(message, HumanMessage) or (
                    isinstance(message, dict) and message.get("type") == "human"
                ):
                    last_message = message
                    break

        # If no human message found, return state
        if not last_message:
            logger.warning("No human message found for tool selection")
            return state

        # Get query content
        query = (
            last_message.content
            if hasattr(last_message, "content")
            else last_message.get("content", "")
        )
        logger.info(f"Selecting tools based on query: {query[:50]}...")

        # Perform similarity search
        try:
            tool_results = self.vector_store.similarity_search(
                query, k=self.config.max_tools_per_turn
            )

            # Extract tool IDs
            selected_tool_ids = []
            for result in tool_results:
                tool_id = result.metadata.get("tool_id")
                if tool_id and tool_id in self.tool_registry:
                    selected_tool_ids.append(tool_id)

            # Update state with selected tools
            state_update = state.copy()
            state_update["selected_tools"] = selected_tool_ids
            state_update["tool_registry"] = self.tool_registry

            # Get names of selected tools for logging
            selected_tool_names = [
                self.tool_registry[tid].name
                for tid in selected_tool_ids
                if tid in self.tool_registry
            ]

            logger.info(
                f"Selected {len(selected_tool_ids)} tools: {', '.join(selected_tool_names)}"
            )

            return state_update

        except Exception as e:
            logger.error(f"Error during tool selection: {e}")
            return state

    def _create_fixed_tool_node(self):
        """Create a fixed version of the tool node that handles tool_call_id properly."""

        def fixed_tool_node(state):
            """Process tool calls properly with tool_call_id."""
            # Extract messages and tool registry
            messages = state.get("messages", [])
            selected_tool_ids = state.get("selected_tools", [])
            tool_registry = state.get("tool_registry", {})

            if not messages:
                # Nothing to process
                logger.warning("No messages to process in tool node")
                return state

            # Get the last message
            last_message = messages[-1]

            # Extract tool calls from the last message
            tool_calls = []
            if isinstance(last_message, AIMessage):
                if hasattr(last_message, "tool_calls"):
                    tool_calls = last_message.tool_calls
                elif (
                    hasattr(last_message, "additional_kwargs")
                    and "tool_calls" in last_message.additional_kwargs
                ):
                    tool_calls = last_message.additional_kwargs["tool_calls"]

            # No tool calls to process
            if not tool_calls:
                logger.warning("No tool calls found in last message")
                return state

            # Get the actual tool objects from registry
            if selected_tool_ids:
                # Use only the selected tools
                selected_tools = [
                    tool_registry[tool_id]
                    for tool_id in selected_tool_ids
                    if tool_id in tool_registry
                ]
            else:
                # Use all tools if no selection
                selected_tools = (
                    list(tool_registry.values()) if tool_registry else self.tools
                )

            # Create a mapping of tool names to actual tools
            tool_map = {tool.name: tool for tool in selected_tools}

            # Process each tool call
            results = []
            for tool_call in tool_calls:
                tool_name = tool_call.get("name")
                tool_args = tool_call.get("args", {})
                tool_call_id = tool_call.get("id")

                if tool_name in tool_map:
                    tool = tool_map[tool_name]
                    try:
                        # Execute the tool
                        tool_result = tool(**tool_args)

                        # Create a ToolMessage with the result and tool_call_id
                        tool_message = ToolMessage(
                            content=str(tool_result),
                            name=tool_name,
                            tool_call_id=tool_call_id,
                        )

                        # Add to results
                        results.append(tool_message)
                        logger.info(f"Successfully executed tool {tool_name}")
                    except Exception as e:
                        error_msg = f"Error executing tool {tool_name}: {e!s}"
                        logger.error(error_msg)
                        tool_message = ToolMessage(
                            content=error_msg, name=tool_name, tool_call_id=tool_call_id
                        )
                        results.append(tool_message)
                else:
                    # Tool not found
                    error_msg = f"Tool {tool_name} not found or not available."
                    logger.warning(error_msg)
                    tool_message = ToolMessage(
                        content=error_msg, name=tool_name, tool_call_id=tool_call_id
                    )
                    results.append(tool_message)

            # Update the state with tool results
            state_update = state.copy()
            state_update["messages"] = list(state["messages"]) + results

            return state_update

        return fixed_tool_node

    def run(
        self, input_data: str | list[str] | dict[str, Any] | BaseModel, **kwargs
    ) -> dict[str, Any]:
        """Run the agent with the given input.

        Args:
            input_data: Input data in various formats
            **kwargs: Additional runtime configuration

        Returns:
            Final state or output
        """
        # Register tools if provided
        tools = kwargs.pop("tools", None)
        if tools:
            self.register_tools(tools)

        # Ensure we have tools
        if not self.tool_registry:
            logger.warning("No tools registered. Agent may not function properly.")

        # Run the agent
        return super().run(input_data, **kwargs)


# Helper function to create a dynamic react agent
def create_dynamic_react_agent(
    tools: list[BaseTool],
    system_prompt: str | None = None,
    model: str = "gpt-4o",
    temperature: float = 0.7,
    name: str | None = None,
    max_tools_per_turn: int = 5,
    max_iterations: int = 10,
    response_format: type[BaseModel] | dict[str, Any] | None = None,
    use_memory: bool = True,
    visualize: bool = True,
    repeat_selection: bool = True,
    vector_store_config: VectorStoreConfig | None = None,
    tool_documents: list[Document] | None = None,
    **kwargs,
) -> DynamicReactAgent:
    """Create a dynamic react agent with minimal configuration.

    Args:
        tools: List of tools the agent can use
        system_prompt: Optional system prompt
        model: Model name to use
        temperature: Temperature for generation
        name: Optional agent name
        max_tools_per_turn: Maximum number of tools to select per turn
        max_iterations: Maximum iterations for React agent
        response_format: Optional structured output model
        use_memory: Whether to use memory
        visualize: Whether to visualize the graph
        repeat_selection: Whether to repeat tool selection after each tool invocation
        vector_store_config: Optional vector store configuration
        tool_documents: Optional pre-created tool documents
        **kwargs: Additional configuration parameters

    Returns:
        DynamicReactAgent instance
    """
    # Create config
    config = DynamicReactAgentConfig.from_tools(
        tools=tools,
        system_prompt=system_prompt,
        model=model,
        temperature=temperature,
        name=name,
        max_tools_per_turn=max_tools_per_turn,
        max_iterations=max_iterations,
        response_format=response_format,
        use_memory=use_memory,
        visualize=visualize,
        repeat_selection=repeat_selection,
        **kwargs,
    )

    # Add vector store config if provided
    if vector_store_config:
        config.vector_store_config = vector_store_config

    # Add tool documents if provided
    if tool_documents:
        config.tool_documents = tool_documents

    # Build agent
    agent = config.build_agent()

    # Register tools if not done during initialization
    if not agent.tool_registry and tools:
        agent.register_tools(tools)

    return agent
