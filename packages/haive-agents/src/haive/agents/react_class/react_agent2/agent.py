# src/haive/agents/react/agent.py

import logging
import os
import uuid
from collections.abc import Callable
from datetime import datetime
from typing import Any, Literal

from haive.core.engine.agent.agent import register_agent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.graph.tool_config import ToolConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool, StructuredTool
from langgraph.graph import END
from langgraph.prebuilt import ToolNode
from langgraph.store.base import BaseStore
from langgraph.types import Checkpointer, Command
from pydantic import BaseModel, Field

from haive.agents.simple.agent import SimpleAgent, SimpleAgentConfig, SimpleAgentState

# Set up logging
logger = logging.getLogger(__name__)

# =============================================
# React Agent Schema - Extends SimpleAgentSchema
# =============================================


class ReactAgentSchema(SimpleAgentState):
    """Schema for React Agent State, extending SimpleAgentSchema."""

    # Inherit messages field from SimpleAgentSchema

    # Add ReAct-specific fields
    tool_results: list[dict[str, Any]] = Field(
        default_factory=list, description="Results from tool executions"
    )

    current_step: int = Field(default=0, description="Current step in the execution")

    remaining_steps: int = Field(
        default=10, description="Number of remaining steps in the execution"
    )

    is_last_step: bool = Field(
        default=False, description="Whether this is the last step in the execution"
    )


# Optional schema for structured output
class ReactAgentSchemaWithStructuredResponse(ReactAgentSchema):
    """Schema for React Agent with structured response."""

    structured_response: Any = Field(
        default=None, description="Structured response from the agent"
    )


# =============================================
# React Agent Config - Extends SimpleAgentConfig
# =============================================


class ReactAgentConfig(SimpleAgentConfig):
    """Configuration for a React agent, extending SimpleAgentConfig.

    This agent implements the ReAct pattern with Tool usage:
    - Reasoning (R): LLM reasoning step
    - Action (A): Tool execution
    - Observation (O): Tool response processing
    """

    # Tool configuration
    tools: list[BaseTool | StructuredTool | Callable | ToolConfig] = Field(
        default_factory=list, description="Tools available to this agent"
    )

    # Node names
    tool_node_name: str = Field(
        default="tools", description="Name for the tool execution node"
    )

    router_node_name: str = Field(
        default="router", description="Name for the router node"
    )

    # Execution control
    max_iterations: int = Field(
        default=10, description="Maximum number of iterations to run"
    )

    # Response format
    response_format: type[BaseModel] | dict[str, Any] | None = Field(
        default=None, description="Schema for structured output"
    )

    # Interruption configuration
    interrupt_before: list[str] | None = Field(
        default=None, description="Node names to interrupt before execution"
    )

    interrupt_after: list[str] | None = Field(
        default=None, description="Node names to interrupt after execution"
    )

    # Graph version
    version: Literal["v1", "v2"] = Field(
        default="v1",
        description="Graph version: v1 (single tool node) or v2 (distributed tool execution)",
    )

    # Visualization
    visualize: bool = Field(
        default=True,
        description="Whether to generate a visualization of the agent graph",
    )

    # Custom tool routing
    tool_routing: dict[str, str] | None = Field(
        default=None,
        description="Custom tool routing: map from tool name to destination node",
    )

    # Override state_schema with ReAct-specific schema
    state_schema: type[BaseModel] = Field(
        default=ReactAgentSchema, description="Schema for the agent state"
    )

    @classmethod
    def from_tools_and_llm(
        cls,
        tools: list[BaseTool | StructuredTool | Callable],
        model: str = "gpt-4o",
        temperature: float = 0.7,
        system_prompt: str | None = None,
        name: str | None = None,
        response_format: type[BaseModel] | dict[str, Any] | None = None,
        **kwargs,
    ) -> "ReactAgentConfig":
        """Create a ReactAgentConfig from tools and an LLM.

        Args:
            tools: List of tools to use
            model: Model name to use
            temperature: Temperature for generation
            system_prompt: Optional system prompt text
            name: Optional name for the agent
            response_format: Optional schema for structured output
            **kwargs: Additional kwargs for configuration

        Returns:
            ReactAgentConfig instance
        """
        # Default ReAct system prompt if none provided
        default_system_prompt = """You are an assistant that can use tools to help answer user questions.

Follow this process:
1. Analyze what the user is asking for
2. If appropriate, select a tool that can help you obtain the information
3. Use the tool by calling it with the right parameters
4. Review the tool's response
5. Decide if you need another tool to continue your research
6. Once you have all the information you need, respond to the user

Always give your reasoning before using a tool, explaining why you're choosing it and what you hope to learn.
"""

        # Create LLM config
        llm_config = AzureLLMConfig(
            model=model, parameters={"temperature": temperature}
        )

        # Create prompt template with system prompt
        system_prompt = system_prompt or default_system_prompt
        messages = [
            SystemMessage(content=system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ]
        prompt_template = ChatPromptTemplate.from_messages(messages)

        # Create AugLLM config with tools
        aug_llm = AugLLMConfig(
            name=f"{name or 'react'}_llm",
            llm_config=llm_config,
            prompt_template=prompt_template,
            tools=tools,
            system_prompt=system_prompt,
        )

        # Determine which state schema to use
        state_schema = (
            ReactAgentSchemaWithStructuredResponse
            if response_format
            else ReactAgentSchema
        )

        # Create and return the config
        return cls(
            name=name or f"react_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            engine=aug_llm,
            tools=tools,
            system_prompt=system_prompt,
            state_schema=state_schema,
            response_format=response_format,
            **kwargs,
        )


# =============================================
# React Agent Implementation - Extends SimpleAgent
# =============================================


@register_agent(ReactAgentConfig)
class ReactAgent(SimpleAgent):
    """A React agent implementing the Reasoning-Action-Observation pattern.

    This agent extends SimpleAgent with:
    1. Tool execution capability
    2. A router to determine when to use tools vs. finish
    3. Optional structured output generation
    """

    def setup_workflow(self) -> None:
        """Set up the React agent workflow graph."""
        logger.debug(f"Setting up workflow for ReactAgent {self.config.name}")

        # Create BaseGraph with proper component registration
        gb = BaseGraph(
            name=f"{self.config.name}_react_agent",
            state_schema=self.state_schema,
        )

        # Add the main agent/LLM node
        gb.add_node(self.config.node_name, self.config.engine)

        # Add the tool execution node
        tool_node = ToolNode(tools=self.config.tools)
        gb.add_node(self.config.tool_node_name, tool_node)

        # Add the router node
        gb.add_node(self.config.router_node_name, self._create_router_function())

        # If structured output is requested, add that node
        if self.config.response_format:
            gb.add_node(
                "generate_structured_response",
                self._create_structured_output_node(),
            )

        # Add any custom tool-specific nodes
        custom_nodes = {}
        if self.config.tool_routing:
            for tool_name, destination in self.config.tool_routing.items():
                # Skip built-in destinations
                if destination in ["tools", "end", "structured_response"]:
                    continue

                # If the destination doesn't exist yet as a node, create it
                if destination not in custom_nodes and not gb.nodes.get(destination):
                    # Create a specialized tool node that only processes this tool
                    for tool in self.config.tools:
                        tool_obj = tool
                        if hasattr(tool, "tool"):
                            tool_obj = tool.tool

                        if getattr(tool_obj, "name", "") == tool_name:
                            specialized_tool_node = ToolNode(tools=[tool])
                            gb.add_node(destination, specialized_tool_node)
                            custom_nodes[destination] = tool_name
                            # Connect back to the agent
                            gb.add_edge(
                                source=destination, target=self.config.node_name
                            )
                            break

        # Add edges between main nodes
        gb.add_edge(source=self.config.node_name, target=self.config.router_node_name)
        gb.add_edge(source=self.config.tool_node_name, target=self.config.node_name)

        # Add conditional edges from router
        route_map = {"tools": self.config.tool_node_name, "end": END}

        # Add structured response destination if needed
        if self.config.response_format:
            route_map["structured_response"] = "generate_structured_response"
            gb.add_edge(source="generate_structured_response", target=END)

        # Add custom tool routing destinations to the route map
        if self.config.tool_routing:
            for tool_name, destination in self.config.tool_routing.items():
                if destination not in route_map:
                    route_map[destination] = destination

        gb.add_conditional_edges(
            source_node=self.config.router_node_name,
            condition=self._route_based_on_messages,
            destinations=route_map,
        )

        # Set entry point
        gb.set_entry_point(self.config.node_name)

        # Build the graph
        self.graph = gb.compile()

        # Generate visualization if requested
        if self.config.visualize:
            try:
                self.compile()
                output_dir = self.config.output_dir or "outputs"
                os.makedirs(output_dir, exist_ok=True)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                graph_filename = f"{self.config.name}_{timestamp}.png"
                graph_path = os.path.join(output_dir, graph_filename)

                from haive.core.utils.visualize_graph_utils import (
                    render_and_display_graph,
                )

                render_and_display_graph(self.app, output_name=graph_path)
                logger.info(f"Graph visualization saved to {graph_path}")
            except Exception as e:
                logger.exception(f"Error generating graph visualization: {e}")

        # Ensure the graph is compiled

        logger.info(f"Set up React workflow for {self.config.name}")

    def _create_router_function(self) -> Callable:
        """Create the router function for determining next steps."""

        def router_function(state: dict[str, Any]) -> dict[str, Any]:
            """Router function to decide next steps."""
            # Increment step counter
            current_step = state.current_step
            remaining_steps = self.config.max_iterations - (current_step + 1)
            is_last_step = remaining_steps <= 0

            # Update state with step information
            updated_state = Command(
                update={
                    # **state,
                    "current_step": current_step + 1,
                    "remaining_steps": remaining_steps,
                    "is_last_step": is_last_step,
                }
            )

            return updated_state

        return router_function

    def _route_based_on_messages(self, state: dict[str, Any]) -> str:
        """Determine the routing based on message content.

        Args:
            state: Current state

        Returns:
            Routing decision: "tools", "structured_response", or "end"
        """
        # Check if we've reached the maximum number of iterations
        if state.is_last_step:
            if self.config.response_format:
                return "structured_response"
            return "end"

        # Get the last message
        messages = state.messages
        if not messages:
            return "end"

        last_message = messages[-1]

        # If the last message has tool calls, route based on tools
        if (
            isinstance(last_message, AIMessage)
            and hasattr(last_message, "tool_calls")
            and last_message.tool_calls
        ):
            # Check that we have enough steps left
            if state.remaining_steps >= 2:
                # If we have custom tool routing, check for matching tools
                if self.config.tool_routing:
                    for tool_call in last_message.tool_calls:
                        tool_name = tool_call.get("name", "")
                        if tool_name in self.config.tool_routing:
                            # Return the custom destination for this tool
                            destination = self.config.tool_routing[tool_name]
                            logger.info(
                                f"Custom routing for tool {tool_name} to {destination}"
                            )
                            return destination

                # Default tool routing
                return "tools"
            # Not enough steps left for tool execution + LLM response
            if self.config.response_format:
                return "structured_response"
            return "end"

        # No tool calls, we're done
        if self.config.response_format:
            return "structured_response"
        return "end"

    def _create_structured_output_node(self) -> Callable:
        """Create a node that generates structured output."""

        def generate_structured_response(
            state: dict[str, Any], config: RunnableConfig
        ) -> dict[str, Any]:
            """Generate structured response from the conversation."""
            try:
                # Get the LLM from the engine
                llm = None
                if (
                    isinstance(self.config.engine, AugLLMConfig)
                    and self.config.engine.llm_config
                ):
                    llm = self.config.engine.llm_config.instantiate()

                if not llm:
                    logger.error("Could not get LLM for structured output generation")
                    return {
                        "structured_response": {
                            "error": "Could not generate structured response"
                        }
                    }

                # Create structured output LLM
                llm_with_structured_output = llm.with_structured_output(
                    self.config.response_format
                )

                # Get messages (excluding the last one if it contains tool calls)
                messages = state.get("messages", [])
                if (
                    messages
                    and isinstance(messages[-1], AIMessage)
                    and hasattr(messages[-1], "tool_calls")
                    and messages[-1].tool_calls
                ):
                    messages = messages[:-1]

                # Generate the structured response
                response = llm_with_structured_output.invoke(messages, config)

                return {"structured_response": response}
            except Exception as e:
                logger.exception(f"Error generating structured response: {e}")
                return {"structured_response": {"error": str(e)}}

        return generate_structured_response

    def run(self, input_data: Any) -> dict[str, Any]:
        """Run the agent with the given input."""
        logger.debug(f"Running ReactAgent with input: {input_data}")

        # Prepare the input
        inputs = self._prepare_input(input_data)

        # Ensure the app is compiled
        if not self.app:
            self.compile()

        # Run the app
        thread_id = str(uuid.uuid4())
        result = self.app.invoke(
            inputs,
            config={"configurable": {"thread_id": thread_id}},
            debug=self.config.debug,
        )

        # Log results
        if "messages" in result:
            messages = result["messages"]
            if messages and len(messages) > 0:
                last_message = messages[-1]
                if hasattr(last_message, "content"):
                    logger.debug(f"Output: {last_message.content[:100]}...")

        return result

    def _prepare_input(self, input_data: Any) -> dict[str, Any]:
        """Prepare input data for the agent."""
        # Use parent's method as base
        state = super()._prepare_input(input_data)

        # Add ReAct-specific fields
        if not hasattr(state, "tool_results"):
            state.tool_results = []

        if not hasattr(state, "current_step"):
            state.current_step = 0

        if not hasattr(state, "remaining_steps"):
            state.remaining_steps = self.config.max_iterations

        if not hasattr(state, "is_last_step"):
            state.is_last_step = False

        return state


# =============================================
# Helper function to create a React agent
# =============================================


def create_react_agent(
    tools: list[BaseTool | StructuredTool | Callable],
    model: str = "gpt-4o",
    temperature: float = 0.7,
    system_prompt: str | None = None,
    name: str | None = None,
    response_format: type[BaseModel] | dict[str, Any] | None = None,
    max_iterations: int = 10,
    checkpointer: Checkpointer | None = None,
    store: BaseStore | None = None,
    interrupt_before: list[str] | None = None,
    interrupt_after: list[str] | None = None,
    debug: bool = False,
    version: Literal["v1", "v2"] = "v1",
    visualize: bool = True,
    tool_routing: dict[str, str] | None = None,
    **kwargs,
) -> ReactAgent:
    """Create a React agent that follows the reasoning-action-observation pattern.

    Args:
        tools: List of tools available to the agent
        model: LLM model name to use
        temperature: Temperature for generation
        system_prompt: System prompt text
        name: Optional name for the agent
        response_format: Schema for structured output
        max_iterations: Maximum number of reasoning steps
        checkpointer: Optional checkpointer for persistence
        store: Optional store for cross-thread data
        interrupt_before: List of node names to interrupt before
        interrupt_after: List of node names to interrupt after
        debug: Whether to enable debug mode
        version: Graph version (v1 or v2)
        **kwargs: Additional configuration parameters

    Returns:
        ReactAgent instance
    """
    # Create config
    config = ReactAgentConfig.from_tools_and_llm(
        tools=tools,
        model=model,
        temperature=temperature,
        system_prompt=system_prompt,
        name=name,
        response_format=response_format,
        max_iterations=max_iterations,
        interrupt_before=interrupt_before,
        interrupt_after=interrupt_after,
        debug=debug,
        version=version,
        visualize=visualize,
        tool_routing=tool_routing,
        **kwargs,
    )

    # Build the agent
    agent = config.build_agent()

    # Override memory and store if provided
    if checkpointer:
        agent.memory = checkpointer
    if store:
        agent.store = store

    return agent


# =============================================
# Tools condition helper function for external use
# =============================================


def tools_condition(
    state: dict[str, Any], messages_key: str = "messages"
) -> Literal["tools", "__end__"]:
    """Determine if the state should route to tools or end based on the last message.

    Args:
        state: State to check for tool calls
        messages_key: Key to find messages in state

    Returns:
        "tools" if tool calls present, "__end__" otherwise
    """
    # Extract the messages
    messages = state.get(messages_key, [])
    if not messages:
        return "__end__"

    # Check the last message for tool calls
    last_message = messages[-1]
    if (
        isinstance(last_message, AIMessage)
        and hasattr(last_message, "tool_calls")
        and last_message.tool_calls
    ):
        return "tools"

    return "__end__"
