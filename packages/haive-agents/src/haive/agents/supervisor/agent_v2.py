"""Haive Supervisor Agent - ReactAgent with Dynamic Routing and Agent Registry.

ReactAgent-based supervisor with:
1. Agent registry with add_agent tool
2. Dynamic routing tool that creates base model with agents in state
3. Prompt template showing available agents
4. Generic agent execution node for running selected agents
"""

import logging
import time
from typing import Any, Dict, List, Literal, Optional

from haive.core.common.models.dynamic_choice_model import DynamicChoiceModel
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.base.base import Engine
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.prebuilt.messages_state import MessagesState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import END, START
from langgraph.types import Command
from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel

from haive.agents.base.agent import Agent
from haive.agents.react.agent import ReactAgent

logger = logging.getLogger(__name__)
console = Console()


class SupervisorState(MessagesState):
    """State schema extending MessagesState with supervisor-specific fields."""

    # Engine registry for node lookups
    engines: dict[str, Engine] = Field(
        default_factory=dict, description="Engines indexed by name"
    )

    # Agent registry in state
    agents: dict[str, Agent] = Field(
        default_factory=dict, description="Available agents in state"
    )

    # Routing information
    next_agent: str | None = Field(None, description="Next agent to route to")
    routing_decision: str | None = Field(None, description="Routing reasoning")

    # Execution metadata
    last_agent: str | None = Field(None, description="Previously active agent")
    routing_timestamp: float | None = Field(None, description="When routing occurred")


class SupervisorAgent(ReactAgent):
    """ReactAgent-based supervisor with dynamic routing and agent registry.

    Architecture:
    1. ReactAgent with add_agent tool for dynamic agent registration
    2. Dynamic routing tool creates base model with agents in state
    3. Prompt template shows available agents and gets routing decision
    4. Generic agent execution node runs the selected agent
    """

    def __init__(
        self, name: str = "supervisor", engine: AugLLMConfig | None = None, **kwargs
    ):
        """Initialize supervisor agent.

        Args:
            name: Supervisor name
            engine: LLM engine for routing decisions
            **kwargs: Additional ReactAgent arguments
        """
        # Create tools for supervisor
        tools = self._create_supervisor_tools()

        # Add tools to engine config
        if engine:
            engine.tools = (engine.tools or []) + tools
        else:
            from haive.core.models.llm.base import LLMConfig

            engine = AugLLMConfig(
                llm_config=LLMConfig(provider="openai", model="gpt-4o-mini"),
                system_message=self._create_supervisor_prompt(),
                tools=tools,
            )

        # Set state schema
        kwargs.setdefault("state_schema", SupervisorState)

        super().__init__(name=name, engine=engine, **kwargs)

        # Agent registry
        self._agent_registry: dict[str, Agent] = {}

        logger.info(f"SupervisorAgent '{name}' initialized as ReactAgent")

    def setup_agent(self) -> None:
        """Register engine in state engines dict for proper node lookup."""
        super().setup_agent()

        # Add main engine to engines registry for node lookups
        if self.main_engine:
            # Ensure engines dict exists
            if not hasattr(self, "engines"):
                self.engines = {}
            self.engines[self.main_engine.name] = self.main_engine
            logger.debug(
                f"Registered engine '{self.main_engine.name}' in agent engines dict"
            )

    def build_graph(self) -> BaseGraph:
        """Build supervisor graph with proper nodes for dynamic routing."""
        # Create graph with our supervisor state schema
        graph = BaseGraph(name="SupervisorGraph", state_schema=self.state_schema)

        # Add agent node (standard ReactAgent functionality)
        from haive.core.graph.node.engine_node import EngineNodeConfig

        agent_node = EngineNodeConfig(
            name="agent_node",
            engine_name=self.main_engine.name,  # Use engine name like SimpleAgent
        )
        graph.add_node("agent_node", agent_node)

        # Add tool node if we have tools
        if self.main_engine and self.main_engine.tools:
            from haive.core.graph.node.tool_node_config import ToolNodeConfig

            tool_node = ToolNodeConfig(
                name="tool_node",
                engine_name=self.main_engine.name,  # Use engine name like SimpleAgent
            )
            graph.add_node("tool_node", tool_node)

            # Add conditional edges for tool routing
            def should_continue(state):
                last_message = (
                    getattr(state, "messages", [])[-1]
                    if hasattr(state, "messages") and state.messages
                    else None
                )
                if (
                    last_message
                    and hasattr(last_message, "tool_calls")
                    and last_message.tool_calls
                ):
                    return "tool_node"
                return END

            graph.add_conditional_edges(
                "agent_node", should_continue, ["tool_node", END]
            )
            graph.add_edge("tool_node", "agent_node")  # ReactAgent loop
        else:
            graph.add_edge("agent_node", END)

        # Add generic agent execution node for routing to worker agents
        generic_node = self.create_generic_agent_execution_node()
        graph.add_node("execute_agent", generic_node)

        # Set entry point
        graph.set_entry_point("agent_node")

        return graph

    def _create_supervisor_tools(self):
        """Create tools for supervisor agent."""

        def add_agent_impl(agent_name: str, agent_description: str) -> str:
            """Add an agent to the registry."""
            # For now, just track the agent info
            # In a real implementation, you'd create the actual agent
            self._agent_registry[agent_name] = {
                "name": agent_name,
                "description": agent_description,
                "type": "placeholder",  # Would be real agent type
            }
            return f"Agent '{agent_name}' added to registry with description: {agent_description}"

        def get_dynamic_routing_model() -> str:
            """Create dynamic choice model with current agents in state."""
            if not self._agent_registry:
                return "No agents available for routing"

            # Create base model with available agents
            agent_options = list(self._agent_registry.keys())
            routing_info = {
                "available_agents": agent_options,
                "agent_descriptions": {
                    name: info.get("description", "No description")
                    for name, info in self._agent_registry.items()
                },
            }

            return f"Available agents for routing: {routing_info}"

        # Convert to langchain tools
        add_agent_tool = tool(add_agent_impl)
        add_agent_tool.name = "add_agent"
        add_agent_tool.description = "Add a new agent to the supervisor registry"

        routing_tool = tool(get_dynamic_routing_model)
        routing_tool.name = "get_routing_options"
        routing_tool.description = "Get current agent routing options with base model"

        return [add_agent_tool, routing_tool]

    def _create_supervisor_prompt(self) -> str:
        """Create supervisor prompt template."""
        return """You are a task supervisor managing a team of specialist agents.

Your responsibilities:
1. Use add_agent tool to register new agents when needed
2. Use get_routing_options tool to see available agents
3. Route tasks to the most appropriate agent based on the request
4. Provide clear reasoning for routing decisions

When you receive a task:
1. First check available agents using get_routing_options
2. Analyze the task requirements
3. Choose the best agent for the task
4. Respond with: "ROUTE_TO: [agent_name] - [reasoning]"

If no suitable agent exists, use add_agent to create one first.
"""

    def add_worker_agent(
        self, agent: Agent, capability_description: str | None = None
    ) -> bool:
        """Add a worker agent to the supervisor registry.

        Args:
            agent: Worker agent to add
            capability_description: Description of agent capabilities

        Returns:
            bool: True if added successfully
        """
        if not agent.name:
            raise ValueError("Agent must have a name")

        # Add to registry
        self._agent_registry[agent.name] = agent

        # Store capability if provided
        if capability_description and hasattr(agent, "description"):
            agent.description = capability_description

        console.print(f"[green]✅ Added worker agent:[/green] {agent.name}")
        return True

    def remove_worker_agent(self, agent_name: str) -> bool:
        """Remove a worker agent.

        Args:
            agent_name: Name of agent to remove

        Returns:
            bool: True if removed successfully
        """
        if agent_name not in self._agent_registry:
            return False

        # Remove from registry
        del self._agent_registry[agent_name]

        console.print(f"[red]❌ Removed worker agent:[/red] {agent_name}")
        return True

    def get_worker_agents(self) -> list[str]:
        """Get list of worker agent names."""
        return list(self._agent_registry.keys())

    def create_generic_agent_execution_node(self):
        """Create generic agent execution node that takes routing output and runs selected agent."""

        async def generic_agent_node(state, config=None):
            """Generic node that executes the selected agent."""
            # Get routing decision from state
            next_agent = getattr(state, "next_agent", None)

            if not next_agent or next_agent not in self._agent_registry:
                return {
                    "messages": [
                        *getattr(state, "messages", []),
                        AIMessage(
                            content=f"No valid agent found for routing: {next_agent}"
                        ),
                    ]
                }

            # Get the selected agent
            selected_agent = self._agent_registry[next_agent]

            try:
                # Prepare state for agent execution
                agent_state = self._prepare_agent_state(state, selected_agent)

                # Execute agent
                result = await selected_agent.ainvoke(agent_state, config)

                # Extract messages from result
                result_messages = []
                if hasattr(result, "messages"):
                    result_messages = result.messages
                elif isinstance(result, dict) and "messages" in result:
                    result_messages = result["messages"]

                # Update state
                current_messages = list(getattr(state, "messages", []))
                current_messages.extend(result_messages)

                return {
                    "messages": current_messages,
                    "last_agent": next_agent,
                    "routing_timestamp": time.time(),
                }

            except Exception as e:
                logger.exception(f"Agent execution failed for {next_agent}: {e}")

                current_messages = list(getattr(state, "messages", []))
                current_messages.append(
                    AIMessage(content=f"Agent {next_agent} failed: {e!s}")
                )

                return {"messages": current_messages, "last_agent": next_agent}

        return generic_agent_node

    def _prepare_agent_state(self, supervisor_state, agent: Agent):
        """Prepare state for agent execution."""
        # Extract messages
        messages = getattr(supervisor_state, "messages", [])

        # If agent has specific state schema, try to use it
        if hasattr(agent, "state_schema") and agent.state_schema:
            try:
                return agent.state_schema(messages=messages)
            except Exception as e:
                logger.warning(f"Could not create state for {agent.name}: {e}")

        # Fallback to basic state
        return type("AgentState", (), {"messages": messages})()

    def print_supervisor_status(self):
        """Print supervisor status."""
        panel_content = f"""
[bold]Supervisor:[/bold] {self.name} (ReactAgent)
[bold]Worker Agents:[/bold] {len(self._agent_registry)}
[bold]Available Routes:[/bold] {', '.join(self._agent_registry.keys())}
[bold]Tools:[/bold] add_agent, get_routing_options
        """

        console.print(Panel(panel_content, title="🔧 Supervisor Status", style="blue"))
