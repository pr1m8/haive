"""ReactAgent implementation that extends SimpleAgent with tool usage capabilities."""

import logging
from typing import Any

from haive.core.engine.agent.agent import Agent, register_agent
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from langchain_core.messages import AIMessage
from langchain_core.tools import BaseTool, StructuredTool, Tool
from langgraph.graph import END
from langgraph.prebuilt.tool_node import ToolNode
from langgraph.pregel import RetryPolicy
from langgraph.types import Send
from pydantic import BaseModel

from haive.agents.react_class.react_v2.config import ReactAgentConfig

# Set up logging
logger = logging.getLogger(__name__)


@register_agent(ReactAgentConfig)
class ReactAgent(Agent[ReactAgentConfig]):
    """A React agent that enhances SimpleAgent with tool-using capabilities.

    This agent implements the ReAct (Reasoning + Acting) pattern which allows
    multi-step reasoning and tool usage for complex tasks.
    """

    def __init__(self, config: ReactAgentConfig):
        # Process tools before initialization
        self.tools_map = self._prepare_tools(config.tools)
        self.tool_nodes = self._create_tool_nodes()
        try:
            # Try with the correct langgraph.types RetryPolicy parameter
            self.retry_policy = RetryPolicy(
                max_attempts=config.max_retries,  # Use max_attempts instead of max_retries
                backoff_factor=2.0,
                initial_interval=(
                    config.retry_delay if hasattr(config, "retry_delay") else 0.5
                ),
            )
        except TypeError:
            # Fallback to the old parameter names if needed
            try:
                self.retry_policy = RetryPolicy(
                    max_retries=config.max_retries,
                    retry_on_error=True,
                    retry_delay=(
                        config.retry_delay if hasattr(config, "retry_delay") else 0.5
                    ),
                )
            except Exception as e2:
                # Last resort - use a minimal RetryPolicy with only required params
                logger.warning(
                    f"Error creating RetryPolicy: {e2!s} - using minimal configuration"
                )
                self.retry_policy = RetryPolicy(max_attempts=3)
        super().__init__(config)

    def _prepare_tools(self, tools_input):
        """Convert various tool formats to LangChain tools."""
        from langchain_core.tools import tool

        tools_map = {}

        # Handle different input formats
        if isinstance(tools_input, dict):
            # Dict mapping - {node_name: tool or [tools]}
            for node_name, tools in tools_input.items():
                if isinstance(tools, list | tuple):
                    # List of tools for this node
                    tools_map[node_name] = self._convert_tools_list(tools)
                else:
                    # Single tool for this node
                    tools_map[node_name] = self._convert_tools_list([tools])
        elif isinstance(tools_input, list | tuple):
            # Simple list - map to default node names
            tools_list = self._convert_tools_list(tools_input)
            if len(tools_list) == 1:
                # Single tool - single node
                tools_map["tools"] = tools_list
            else:
                # Multiple tools - one node per tool
                for i, tool in enumerate(tools_list):
                    node_name = (
                        f"tool_{i}_{tool.name}"
                        if hasattr(tool, "name")
                        else f"tool_{i}"
                    )
                    tools_map[node_name] = [tool]
        else:
            logger.error(f"Unsupported tools format: {type(tools_input)}")

        logger.info(
            f"Prepared {sum(len(tools) for tools in tools_map.values())} tools across {len(tools_map)} nodes"
        )
        return tools_map

    def _convert_tools_list(self, tools_list):
        """Convert a list of mixed tool formats to LangChain tools."""
        from langchain_core.tools import tool

        converted_tools = []

        for t in tools_list:
            if isinstance(t, BaseTool | StructuredTool | Tool):
                # Already a valid tool
                converted_tools.append(t)
            elif callable(t) and not isinstance(t, type):
                # Function - convert to tool
                if hasattr(t, "__name__"):
                    tool_name = t.__name__
                    tool_desc = t.__doc__ or f"Tool {tool_name}"
                    converted_tools.append(
                        tool(name=tool_name, description=tool_desc)(t)
                    )
                else:
                    logger.warning(f"Skipping unnamed callable: {t}")
            elif isinstance(t, type) and issubclass(t, BaseModel):
                # Pydantic model - convert to structured tool
                logger.warning(f"Pydantic model tools not implemented: {t}")
                # This would require more complex implementation
            else:
                logger.warning(f"Unsupported tool type: {type(t).__name__}")

        return converted_tools

    def _create_tool_nodes(self):
        """Create ToolNodes from the prepared tools map."""
        if not self.tools_map:
            logger.warning("No tools available to create ToolNodes")
            return {}

        tool_nodes = {}
        for node_name, tools in self.tools_map.items():
            if tools:
                tool_nodes[node_name] = ToolNode(tools)

        return tool_nodes

    def setup_workflow(self) -> None:
        """Set up the React agent workflow with tool support."""
        logger.debug(f"Setting up workflow for ReactAgent {self.config.name}")

        # Update the engine to use all tools if needed
        if hasattr(self.config.engine, "tools") and not self.config.engine.tools:
            all_tools = []
            for tools_list in self.tools_map.values():
                all_tools.extend(tools_list)
            self.config.engine.tools = all_tools

        # Create DynamicGraph with proper component registration
        gb = DynamicGraph(
            components=[self.config.engine], state_schema=self.state_schema
        )

        # Add the LLM node
        gb.add_node(name="agent", config=self.config.engine)

        # Add tool nodes
        for node_name, tool_node in self.tool_nodes.items():
            gb.add_node(name=node_name, config=tool_node)

            # Add retry policy to the node
            gb.graph.add_retry_policy(node_name, self.retry_policy)

            # Edge from tool back to agent
            gb.add_edge(node_name, "agent")

        # Add structured output node if configured
        use_structured_output = getattr(
            self.config, "use_structured_output_node", False
        )
        structured_output_model = getattr(self.config, "structured_output_model", None)

        if use_structured_output and structured_output_model:
            gb.add_structured_output_node(
                name="structured_output",
                model=structured_output_model,
                command_goto=END,
            )

            # Set up advanced routing with structured output
            gb.add_conditional_edges(
                from_node="agent",
                condition_or_branch=self._route_agent_output,
                routes={
                    "end": END,
                    "structured_output": "structured_output",
                    **{name: name for name in self.tool_nodes},
                },
            )
        elif self.tool_nodes:
            # Set up routing without structured output
            gb.add_conditional_edges(
                from_node="agent",
                condition_or_branch=self._route_agent_output,
                routes={"end": END, **{name: name for name in self.tool_nodes}},
            )
        else:
            # No tools, just add edge to END
            gb.add_edge("agent", END)

        # Set entry point
        gb.set_entry_point("agent")

        # Build the graph
        self.graph = gb.build()

        logger.info(
            f"Set up ReactAgent workflow for {self.config.name} with {len(self.tool_nodes)} tool nodes"
        )

    def _route_agent_output(self, state: Any) -> str | list[Send]:
        """Route output from agent to appropriate next node(s).

        This function implements complex routing, supporting:
        1. Single tool execution (returns the node name)
        2. Parallel tool execution (returns list of Send objects)
        3. End of reasoning (returns "end")
        4. Structured output (returns "structured_output")
        """
        # Early termination for completed tasks
        # If the last message contains completion indicators, skip further processing
        messages = getattr(state, "messages", [])
        if messages:
            last_message = messages[-1]
            if isinstance(last_message, AIMessage):
                # Check for completion indicators in the message
                content = getattr(last_message, "content", "").lower()
                if content and any(
                    marker in content
                    for marker in [
                        "task completed",
                        "completed successfully",
                        "final answer:",
                        "conclusion:",
                        "final response:",
                        "completed the task",
                    ]
                ):
                    logger.info(
                        "Task completion detected in message content, ending workflow"
                    )
                    return (
                        "structured_output"
                        if getattr(self.config, "use_structured_output_node", False)
                        else "end"
                    )

        # Check for remaining steps
        if hasattr(state, "remaining_steps"):
            if state.remaining_steps <= 0:
                logger.info("No remaining steps, ending")
                return (
                    "structured_output"
                    if getattr(self.config, "use_structured_output_node", False)
                    else "end"
                )
            # Decrement the steps counter
            state.remaining_steps -= 1

        # Check if there's any message
        if not messages:
            logger.warning("No messages in state")
            return "end"

        # Get the last message
        last_message = messages[-1]

        # If not an AIMessage or no tool calls, return end or structured output
        if not isinstance(last_message, AIMessage) or not getattr(
            last_message, "tool_calls", None
        ):
            # Check if this appears to be a final answer
            if isinstance(last_message, AIMessage) and getattr(
                last_message, "content", None
            ):
                # If we have structured output node, use it
                if getattr(self.config, "use_structured_output_node", False):
                    return "structured_output"
            return "end"

        # Extract tool calls
        tool_calls = last_message.tool_calls

        # Map each tool call to its appropriate node
        tools_to_nodes = {}

        # Create mapping of tool names to node names
        tool_to_node_map = {}
        for node_name, tools_list in self.tools_map.items():
            for tool in tools_list:
                if hasattr(tool, "name"):
                    tool_to_node_map[tool.name] = node_name

        # Group tool calls by node
        for tool_call in tool_calls:
            tool_name = tool_call.get("name")
            if tool_name in tool_to_node_map:
                node_name = tool_to_node_map[tool_name]
                if node_name not in tools_to_nodes:
                    tools_to_nodes[node_name] = []
                tools_to_nodes[node_name].append(tool_call)

        # If no valid tool calls found but the message has content, treat as a final answer
        if (
            not tools_to_nodes
            and isinstance(last_message, AIMessage)
            and getattr(last_message, "content", None)
        ):
            if getattr(self.config, "use_structured_output_node", False):
                return "structured_output"
            return "end"

        # Check if we need parallel execution
        if self.config.parallel_tool_execution and len(tools_to_nodes) > 1:
            # Return Send objects for parallel execution
            return [
                Send(node, [tool_call])
                for node, tool_calls in tools_to_nodes.items()
                for tool_call in tool_calls
            ]
        if tools_to_nodes:
            # Return the first node (sequential execution)
            return next(iter(tools_to_nodes.keys()))
        # No valid tool calls, end
        if getattr(self.config, "use_structured_output_node", False):
            return "structured_output"
        return "end"

    def run(self, input_data, thread_id=None, **kwargs):
        """Override run to handle tool-based workflows and proper state preparation."""
        # Add remaining_steps to input if not present but in our schema
        if hasattr(self.state_schema, "remaining_steps"):
            if isinstance(input_data, dict) and "remaining_steps" not in input_data:
                input_data["remaining_steps"] = getattr(
                    self.config, "max_iterations", 10
                )

        # Call parent run method
        return super().run(input_data, thread_id, **kwargs)
