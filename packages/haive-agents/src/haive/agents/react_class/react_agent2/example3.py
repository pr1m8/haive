# src/haive/agents/react/agent.py
import logging
import os
import uuid
from collections.abc import Callable
from datetime import datetime
from typing import Any, Literal

from haive.core.config.runnable import RunnableConfigManager
from haive.core.engine.agent.agent import register_agent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.branches import Branch
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from haive.core.graph.node.config import NodeConfig
from haive.core.graph.tool_config import ToolConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import BaseTool, StructuredTool
from langgraph.graph import END
from langgraph.prebuilt import ToolNode
from langgraph.store.base import BaseStore
from langgraph.types import Checkpointer, Command, Send
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
            id=f"llm-{uuid.uuid4().hex[:8]}",
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

        # Create DynamicGraph with proper component registration
        gb = DynamicGraph(
            name=f"{self.config.name}_graph",
            components=[self.config.engine] + self.config.tools,
            state_schema=self.config.state_schema,
        )

        # Add the main agent/LLM node
        agent_node_config = NodeConfig(
            name=self.config.node_name,
            engine=self.config.engine,
            config_overrides={"temperature": getattr(self.config, "temperature", 0.7)},
        )

        gb.add_node(
            name=self.config.node_name,
            config=agent_node_config,
            input_mapping={"messages": "messages"},
        )

        # Add the router node
        router_node_config = NodeConfig(
            name=self.config.router_node_name, engine=self._create_router_function()
        )

        gb.add_node(name=self.config.router_node_name, config=router_node_config)

        # Add the tool execution node
        if self.config.version == "v1":
            # v1: Single tool node for all tools
            tool_node = ToolNode(tools=self.config.tools)

            gb.add_node(name=self.config.tool_node_name, config=tool_node)

            # Add edge from tool node back to agent
            gb.add_edge(self.config.tool_node_name, self.config.node_name)
        else:
            # v2: Individual nodes for tools or custom routing
            self._setup_tool_nodes(gb)

        # If structured output is requested, add that node
        if self.config.response_format:
            structured_output_node_config = NodeConfig(
                name="generate_structured_response",
                engine=self._create_structured_output_node(),
                command_goto=END,
            )

            gb.add_node(
                name="generate_structured_response",
                config=structured_output_node_config,
            )

        # Add edge from agent to router
        gb.add_edge(self.config.node_name, self.config.router_node_name)

        # Add conditional edges from router
        route_destinations = {"tools": self.config.tool_node_name, "end": END}

        # Add structured response destination if needed
        if self.config.response_format:
            route_destinations["structured_response"] = "generate_structured_response"

        # Add custom tool routing if needed
        if self.config.tool_routing and self.config.version == "v2":
            for tool_name, destination in self.config.tool_routing.items():
                if (
                    destination not in route_destinations
                    and destination != self.config.tool_node_name
                ):
                    route_destinations[destination] = destination

        # Create routing branch
        router_branch = Branch.from_function(
            self._route_based_on_messages, destinations=route_destinations
        )

        gb.add_conditional_edges(self.config.router_node_name, router_branch.evaluator)

        # Set entry point
        gb.set_entry_point(self.config.node_name)

        # Set default runnable config
        default_config = RunnableConfigManager.create(
            temperature=getattr(self.config, "temperature", 0.7),
            model=getattr(self.config, "model", "gpt-4o"),
        )
        gb.set_default_runnable_config(default_config)

        # Build the graph
        self.graph = gb.build()

        # Generate visualization if requested
        if self.config.visualize:
            try:
                self.compile()
                output_dir = self.config.output_dir or "resources/Graphs"
                os.makedirs(output_dir, exist_ok=True)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                graph_filename = f"{self.config.name}_{timestamp}.png"
                graph_path = os.path.join(output_dir, graph_filename)

                from haive.core.utils.visualize_graph_utils import (
                    render_and_display_graph,
                )

                render_and_display_graph(self.app, output_name=graph_path)
                logger.info(f"Graph visualization saved to: {graph_path}")
            except Exception as e:
                logger.error(f"Error generating graph visualization: {e}")

        logger.info(f"Set up React workflow for {self.config.name}")

    def _setup_tool_nodes(self, gb: DynamicGraph) -> None:
        """Set up individual tool nodes for the v2 graph version."""
        # Track tool groupings for custom routing
        tool_groups = {}

        # Handle custom tool routing first
        if self.config.tool_routing:
            # Group tools by their routing destination
            for tool in self.config.tools:
                tool_name = getattr(tool, "name", None)
                if not tool_name and hasattr(tool, "tool"):
                    tool_name = getattr(tool.tool, "name", None)

                if not tool_name:
                    continue

                # Check if this tool has custom routing
                destination = self.config.tool_routing.get(tool_name)
                if destination:
                    # Add to existing group or create new one
                    if destination not in tool_groups:
                        tool_groups[destination] = []
                    tool_groups[destination].append(tool)
                else:
                    # Default to general tools node
                    if self.config.tool_node_name not in tool_groups:
                        tool_groups[self.config.tool_node_name] = []
                    tool_groups[self.config.tool_node_name].append(tool)

            # Create a node for each tool group
            for node_name, group_tools in tool_groups.items():
                # Create the tool node
                tool_node = ToolNode(tools=group_tools)

                gb.add_node(name=node_name, config=tool_node)

                # Add edge back to agent
                gb.add_edge(node_name, self.config.node_name)
        else:
            # No custom routing, just add the default tools node
            tool_node = ToolNode(tools=self.config.tools)

            gb.add_node(name=self.config.tool_node_name, config=tool_node)

            # Add edge back to agent
            gb.add_edge(self.config.tool_node_name, self.config.node_name)

    def _create_router_function(self) -> Callable:
        """Create the router function for determining next steps."""

        def router_function(state: ReactAgentSchema) -> Command:
            """Router function to decide next steps."""
            # Increment step counter
            current_step = state.current_step
            remaining_steps = self.config.max_iterations - (current_step + 1)
            is_last_step = remaining_steps <= 0

            # Update state with step information
            return Command(
                update={
                    "current_step": current_step + 1,
                    "remaining_steps": remaining_steps,
                    "is_last_step": is_last_step,
                }
            )

        return router_function

    def _route_based_on_messages(
        self, state: ReactAgentSchema
    ) -> str | Send | list[Send]:
        """Determine the routing based on message content.

        Args:
            state: Current state

        Returns:
            Routing decision: "tools", "structured_response", "end", or Send objects
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
                # Handle v2 mode with parallel tool execution
                if self.config.version == "v2" and self.config.tool_routing:
                    # Group tool calls by their destination nodes
                    sends_by_node = {}

                    for tool_call in last_message.tool_calls:
                        tool_name = tool_call.get("name", "")
                        # Determine which node should handle this tool
                        node_name = self.config.tool_routing.get(tool_name)

                        if not node_name:
                            # Fall back to default tools node
                            node_name = self.config.tool_node_name

                        # Add to the sends for this node
                        if node_name not in sends_by_node:
                            sends_by_node[node_name] = []
                        sends_by_node[node_name].append(tool_call)

                    # Create Send objects for each node
                    sends = []
                    for node_name, tool_calls in sends_by_node.items():
                        for tool_call in tool_calls:
                            sends.append(Send(node_name, [tool_call]))

                    if sends:
                        return sends

                # For v1 or fallback to regular tool node
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

        def generate_structured_response(state: ReactAgentSchema) -> dict[str, Any]:
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
                messages = list(state.messages)
                if (
                    messages
                    and isinstance(messages[-1], AIMessage)
                    and hasattr(messages[-1], "tool_calls")
                    and messages[-1].tool_calls
                ):
                    messages = messages[:-1]

                # Add a final instruction to format the response
                model_name = (
                    self.config.response_format.__name__
                    if hasattr(self.config.response_format, "__name__")
                    else "Structured"
                )
                messages.append(
                    HumanMessage(
                        content=f"Based on our conversation, please provide a final response in the required {model_name} format."
                    )
                )

                # Generate the structured response
                response = llm_with_structured_output.invoke(messages)

                return {"structured_response": response}
            except Exception as e:
                logger.error(f"Error generating structured response: {e}")
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
        config = RunnableConfigManager.create(
            thread_id=thread_id,
            temperature=getattr(self.config, "temperature", 0.7),
            model=getattr(self.config, "model", "gpt-4o"),
        )

        # Apply agent-specific config if needed
        if hasattr(self.config.engine, "id"):
            config = RunnableConfigManager.add_engine_config(
                config,
                self.config.engine.id,
                temperature=getattr(self.config, "temperature", 0.7),
            )

        result = self.app.invoke(inputs, config=config, debug=self.config.debug)

        # Save state history if configured
        if self.config.save_history:
            try:
                output_dir = self.config.output_dir or "resources/State_History"
                os.makedirs(output_dir, exist_ok=True)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                state_filename = os.path.join(
                    output_dir, f"{self.config.name}_{timestamp}.json"
                )

                # Save state history
                # from haive.core.engine.agent.state_handling import save_state_history
                # save_state_history(self.app, state_filename, config)
                logger.info(f"State history saved to: {state_filename}")
            except Exception as e:
                logger.error(f"Error saving state history: {e}")

        # Log results
        if "messages" in result:
            messages = result["messages"]
            if messages and len(messages) > 0:
                last_message = messages[-1]
                if hasattr(last_message, "content"):
                    logger.debug(f"Output: {last_message.content[:100]}...")

        # Apply post-processing if configured
        if hasattr(self.config, "postprocess") and callable(self.config.postprocess):
            try:
                result = self.config.postprocess(result)
            except Exception as e:
                logger.error(f"Error in post-processing: {e}")

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
    save_history: bool = True,
    output_dir: str | None = None,
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
        visualize: Whether to generate graph visualization
        tool_routing: Custom routing map for tools
        save_history: Whether to save state history
        output_dir: Directory for output files
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
        save_history=save_history,
        output_dir=output_dir,
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
) -> Literal["tools", "end"]:
    """Determine if the state should route to tools or end based on the last message.

    Args:
        state: State to check for tool calls
        messages_key: Key to find messages in state

    Returns:
        "tools" if tool calls present, "end" otherwise
    """
    # Extract the messages
    messages = state.get(messages_key, [])
    if not messages:
        return "end"

    # Check the last message for tool calls
    last_message = messages[-1]
    if (
        isinstance(last_message, AIMessage)
        and hasattr(last_message, "tool_calls")
        and last_message.tool_calls
    ):
        return "tools"

    return "end"
