import logging
from collections.abc import Callable

from agents.react_agent2.config2 import ReactAgentConfig
from haive.core.engine.agent.agent import Agent, register_agent
from haive.core.graph.branches import Branch
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from langchain_core.messages import AIMessage
from langchain_core.tools import BaseTool
from langgraph.graph import END
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field

# Set up logging
logger = logging.getLogger(__name__)


class AdvancedReactAgentConfig(ReactAgentConfig):
    """Extended configuration for the Advanced React Agent."""

    # Tool-specific routing configuration
    tool_routing: dict[str, str] = Field(
        default_factory=dict,
        description="Mapping from tool names to node names for custom routing",
    )

    # Node names
    agent_node_name: str = Field(
        default="agent_node", description="Name for the agent node"
    )

    # Default tool node name (for tools without specific routing)
    default_tool_node_name: str = Field(
        default="default_tool_node", description="Name for the default tool node"
    )

    # Custom processing functions for different tool types
    tool_processors: dict[str, Callable] = Field(
        default_factory=dict,
        description="Custom processing functions for different tool nodes",
    )

    # Whether to capture and analyze tool calls for improvement
    analyze_tool_usage: bool = Field(
        default=False, description="Whether to analyze tool usage patterns"
    )


@register_agent(AdvancedReactAgentConfig)
class AdvancedReactAgent(Agent[AdvancedReactAgentConfig]):
    """Advanced React agent with specialized tool routing.

    Features:
    - Tool-specific routing based on tool name
    - Custom processing for different tool types
    - Support for specialized tool nodes
    - Optional tool usage analysis
    """

    def __init__(self, config: AdvancedReactAgentConfig):
        """Initialize the Advanced React Agent with its configuration."""
        # Set up tools
        self.tools = config.tools

        # Group tools by their routing destination
        self.tool_groups = {}
        self.tool_nodes = {}

        # Call parent constructor
        super().__init__(config)

        # Group the tools if we have a tool routing configuration
        if self.tools and config.tool_routing:
            self._group_tools_by_routing()

    def _group_tools_by_routing(self):
        """Group tools based on their routing destination."""
        # Initialize with empty lists
        self.tool_groups = {self.config.default_tool_node_name: []}

        # Add tool routing destinations
        for _tool_name, node_name in self.config.tool_routing.items():
            if node_name not in self.tool_groups:
                self.tool_groups[node_name] = []

        # Assign tools to their groups
        for tool in self.tools:
            node_name = self.config.tool_routing.get(
                tool.name, self.config.default_tool_node_name
            )
            self.tool_groups[node_name].append(tool)

        # Create tool nodes for each group
        for node_name, tools in self.tool_groups.items():
            if tools:  # Only create nodes for non-empty tool groups
                self.tool_nodes[node_name] = ToolNode(tools)

        logger.info(f"Grouped tools into {len(self.tool_groups)} categories")

    def setup_workflow(self) -> None:
        """Set up the workflow graph with specialized tool routing."""
        logger.info(f"Setting up workflow for AdvancedReactAgent: {self.config.name}")

        # Create a dynamic graph with the engine component
        gb = DynamicGraph(
            components=[self.config.engine], state_schema=self.config.state_schema
        )

        # Add the agent node
        gb.add_node(
            name=self.config.agent_node_name,
            config=self.config.engine,
            command_goto=None,  # Will be determined by Branch
        )

        # If we have tools, set up tool execution nodes
        if self.tools:
            # Set up tool nodes for each routing destination
            if not self.tool_groups:
                self._group_tools_by_routing()

            # Default function for tool execution with step increment
            def create_tool_executor(node_name):
                """Create a function that executes a specific tool node."""
                tool_node = self.tool_nodes.get(node_name)
                if not tool_node:
                    logger.warning(f"No tools found for node: {node_name}")
                    return lambda state: state

                # Check if we have a custom processor
                custom_processor = self.config.tool_processors.get(node_name)

                def execute_tool(state):
                    """Execute the tool and update state."""
                    # Convert to dictionary if needed
                    state_dict = (
                        state.model_dump() if hasattr(state, "model_dump") else state
                    )

                    try:
                        # Execute the tool node
                        result = tool_node.invoke(state)
                        result_dict = (
                            result.model_dump()
                            if hasattr(result, "model_dump")
                            else result
                        )

                        # Apply custom processing if available
                        if custom_processor:
                            result_dict = custom_processor(result_dict)

                        # Increment step counter
                        if "current_step" in state_dict:
                            result_dict["current_step"] = state_dict["current_step"] + 1

                        # Track tool usage if enabled
                        if (
                            self.config.analyze_tool_usage
                            and "tool_usage_stats" in state_dict
                        ):
                            # Extract the tool that was called
                            last_message = (
                                state_dict.get("messages", [])[-1]
                                if state_dict.get("messages")
                                else None
                            )
                            if (
                                isinstance(last_message, AIMessage)
                                and last_message.tool_calls
                            ):
                                for tool_call in last_message.tool_calls:
                                    tool_name = tool_call.get("name", "unknown")
                                    stats = state_dict["tool_usage_stats"]
                                    if tool_name in stats:
                                        stats[tool_name] += 1
                                    else:
                                        stats[tool_name] = 1
                                    result_dict["tool_usage_stats"] = stats

                        return result_dict
                    except Exception as e:
                        logger.exception(
                            f"Error executing tool node '{node_name}': {e!s}"
                        )
                        state_dict["error"] = f"Tool execution error: {e!s}"
                        state_dict["status"] = "error"
                        return state_dict

                return execute_tool

            # Add all tool nodes to the graph
            for node_name in self.tool_groups:
                if node_name in self.tool_nodes:
                    gb.add_node(
                        name=node_name,
                        config=create_tool_executor(node_name),
                        command_goto=self.config.agent_node_name,  # Return to agent
                    )

            # Create a single Branch for checking max iterations
            max_iterations_branch = Branch(
                key="current_step",
                value=self.config.max_iterations,
                comparison=">=",
                destinations={True: END, False: None},  # None allows falling through
                default=None,
            )

            # Create a Branch for tool routing based on the tool name in the last message
            def route_by_tool_name(state):
                """Route to the appropriate tool node based on the tool name."""
                # Extract messages
                messages = (
                    state.messages
                    if hasattr(state, "messages")
                    else state.get("messages", [])
                )
                if not messages:
                    return END

                # Get last message
                last_message = messages[-1]

                # Check for tool calls
                if (
                    not isinstance(last_message, AIMessage)
                    or not hasattr(last_message, "tool_calls")
                    or not last_message.tool_calls
                ):
                    return END

                # Get the tool name
                tool_name = last_message.tool_calls[0].get("name", "")

                # Get the node for this tool
                node_name = self.config.tool_routing.get(
                    tool_name, self.config.default_tool_node_name
                )

                # If we don't have a node for this tool, use default
                if node_name not in self.tool_nodes:
                    logger.warning(
                        f"No node found for tool '{tool_name}', using default"
                    )
                    return self.config.default_tool_node_name

                logger.info(f"Routing tool '{tool_name}' to node '{node_name}'")
                return node_name

            # Create the destinations dictionary for tool routing
            tool_destinations = {node_name: node_name for node_name in self.tool_nodes}
            tool_destinations[END] = END  # Add END destination

            # Create the main router function that combines max iterations check and tool routing
            def agent_router(state):
                """Main router from agent node."""
                # First check max iterations
                max_iter_result = max_iterations_branch.evaluate(state)
                if max_iter_result == END:
                    return END

                # Then route by tool name
                return route_by_tool_name(state)

            # Add the conditional edge from agent to tool nodes
            gb.add_conditional_edges(
                self.config.agent_node_name, agent_router, tool_destinations
            )
        else:
            # Without tools, simply route to END
            gb.add_edge(self.config.agent_node_name, END)

        # Set entry point to agent node
        gb.set_entry_point(self.config.agent_node_name)

        # Build graph
        self.graph = gb.build()

        # Compile graph
        if self.config.should_compile:
            self.compile()

        # Generate visualization if requested
        if self.config.visualize and self.app:
            self.visualize_graph()

        logger.info(
            f"Workflow setup complete for AdvancedReactAgent: {self.config.name}"
        )

    def add_tool(
        self, tool: BaseTool, routing: str | None = None
    ) -> "AdvancedReactAgent":
        """Add a tool to the agent with optional custom routing.

        Args:
            tool: The tool to add
            routing: Optional node name for routing this tool

        Returns:
            Self for chaining
        """
        # Add to tools list
        self.config.tools.append(tool)

        # Add routing if specified
        if routing:
            self.config.tool_routing[tool.name] = routing

        # Regroup tools and rebuild workflow
        self._group_tools_by_routing()
        self.setup_workflow()

        return self

    def create_custom_tool_node(
        self, node_name: str, processor: Callable
    ) -> "AdvancedReactAgent":
        """Create a custom tool node with a specialized processor.

        Args:
            node_name: Name for the node
            processor: Function to process tool results

        Returns:
            Self for chaining
        """
        self.config.tool_processors[node_name] = processor

        # Rebuild workflow if it exists
        if hasattr(self, "graph"):
            self.setup_workflow()

        return self


def create_advanced_react_agent(
    system_prompt: str | None = None,
    model: str = "gpt-4o",
    temperature: float = 0.7,
    tools: list[BaseTool] | None = None,
    tool_routing: dict[str, str] | None = None,
    name: str | None = None,
    structured_output_model: type[BaseModel] | None = None,
    **kwargs,
) -> AdvancedReactAgent:
    """Create an advanced React agent with tool-specific routing.

    Args:
        system_prompt: Optional system prompt
        model: Model name to use
        temperature: Temperature for generation
        tools: List of tools to use
        tool_routing: Mapping from tool names to node names
        name: Optional name for the agent
        structured_output_model: Optional schema for structured output
        **kwargs: Additional configuration parameters

    Returns:
        AdvancedReactAgent instance
    """
    # Create the configuration
    config = AdvancedReactAgentConfig.from_scratch(
        prompt_template=Csystem_prompt,
        model=model,
        temperature=temperature,
        tools=tools or [],
        name=name,
        structured_output_model=structured_output_model,
        **kwargs,
    )

    # Add tool routing if provided
    if tool_routing:
        config.tool_routing = tool_routing

    # Build and return the agent
    return AdvancedReactAgent(config=config)
