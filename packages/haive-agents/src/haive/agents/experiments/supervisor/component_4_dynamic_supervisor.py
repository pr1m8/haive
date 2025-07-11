"""Component 4: Dynamic Supervisor using ReactAgent with state-based tools."""

from typing import Any, Dict, Optional

from haive.core.engine import AugLLMConfig
from haive.core.graph import BaseGraph
from haive.core.models.llm.base import AzureLLMConfig
from pydantic import Field, model_validator

from haive.agents.experiments.supervisor.component_2_tools import (
    SupervisorStateWithTools,
)
from haive.agents.experiments.supervisor.component_3_agent_execution import (
    AgentExecutionNode,
)
from haive.agents.react.agent import ReactAgent


class DynamicSupervisor(ReactAgent):
    """Dynamic supervisor that can add/remove agents at runtime.

    Key architecture:
    - Uses ReactAgent as base for reasoning capabilities
    - SupervisorStateWithTools provides dynamic tool generation
    - Agent execution node mirrors tool_node pattern
    - Tools are generated from state.agents at runtime
    """

    # Agent execution node for runtime agent execution
    agent_execution_node: AgentExecutionNode = Field(
        default_factory=lambda: AgentExecutionNode("agent_execution"),
        description="Node that executes agents from state at runtime",
    )

    def __init__(self, **data):
        """Initialize dynamic supervisor with proper setup."""
        # Set state schema to our dynamic state
        if "state_schema" not in data:
            data["state_schema"] = SupervisorStateWithTools

        # Default engine if not provided
        if "engine" not in data:
            data["engine"] = self._create_default_engine()

        super().__init__(**data)

    @classmethod
    def _create_default_engine(cls) -> AugLLMConfig:
        """Create default supervisor engine with reasoning capabilities."""
        return AugLLMConfig(
            name="supervisor_engine",
            llm_config=AzureLLMConfig(model="gpt-4o"),
            system_message=(
                "You are a dynamic supervisor that coordinates multiple AI agents. "
                "Your role is to:\n"
                "1. Analyze incoming tasks and determine which agent should handle them\n"
                "2. Route tasks to the appropriate agents using handoff tools\n"
                "3. Use the choose_agent tool to make validated routing decisions\n"
                "4. Always ensure tasks are handled by the most suitable agent\n"
                "5. You can END the conversation when the task is complete\n\n"
                "Available agents are dynamically updated based on the current state. "
                "Use the choose_agent tool to see current options and make decisions."
            ),
            tools=[],  # Tools will be populated dynamically from state
        )

    @model_validator(mode="after")
    def setup_dynamic_supervisor(self):
        """Setup supervisor with dynamic tool integration."""

        # Sync tools from state to engine
        self._sync_tools_from_state()

        # Setup schemas and build graph
        self._sync_fields_from_engine()
        self._setup_schemas()
        self._build_initial_graph()

        return self

    def _sync_tools_from_state(self):
        """Sync tools from state.agents to engine (key dynamic behavior)."""

        # Get current state
        if hasattr(self, "_current_state") and self._current_state:
            state = self._current_state
        else:
            # Create initial empty state
            state = self.state_schema()

        # Get tools from state
        if hasattr(state, "get_all_tools"):
            dynamic_tools = state.get_all_tools()

            # Update engine tools
            self.engine.tools = dynamic_tools

            # Update tool routes (all dynamic tools use default routing)
            self.engine.tool_routes = {
                tool.name: "langchain_tool" for tool in dynamic_tools
            }

        else:
            passod")

    def build_graph(self) -> BaseGraph:
        """Build supervisor graph with agent execution capabilities.

        Architecture:
        supervisor (reasoning) → agent_execution | END

        The supervisor uses dynamic tools to make routing decisions,
        then the agent_execution node handles the actual execution.
        """

        graph = BaseGraph()

        # Add supervisor reasoning node
        graph.add_node("supervisor", self._supervisor_reasoning_node)

        # Add agent execution node
        graph.add_node("agent_execution", self.agent_execution_node)

        # Add routing logic
        graph.add_conditional_edges(
            "supervisor",
            self._route_supervisor_decision,
            {"execute": "agent_execution", "end": "__end__"},
        )

        # Agent execution always returns to supervisor
        graph.add_edge("agent_execution", "supervisor")

        # Set entry point
        graph.set_entry_point("supervisor")

        return graph.compile()

    async def _supervisor_reasoning_node(
        self, state: SupervisorStateWithTools
    ) -> dict[str, Any]:
        """Supervisor reasoning node that uses dynamic tools for decision making.

        This node:
        1. Updates engine tools from current state
        2. Uses ReactAgent reasoning with dynamic tools
        3. Sets routing decisions in state
        """

        # Update tools from current state before reasoning
        self._sync_tools_from_state_instance(state)

        # Use ReactAgent's reasoning capabilities
        # This will use the dynamic tools (handoff_to_X, choose_agent)
        result = await self.engine.ainvoke(state.model_dump())

        # Extract routing decision from result
        # The tools should have set next_agent and agent_task
        if isinstance(result, dict):
            return result
        # Handle AIMessage or other result types
        return {"messages": [result]}

    def _sync_tools_from_state_instance(self, state: SupervisorStateWithTools):
        """Sync tools from a specific state instance."""
        dynamic_tools = state.get_all_tools()
        self.engine.tools = dynamic_tools
        self.engine.tool_routes = {
            tool.name: "langchain_tool" for tool in dynamic_tools
        }

    def _route_supervisor_decision(self, state: SupervisorStateWithTools) -> str:
        """Route based on supervisor's decision in state."""
        if state.next_agent and state.next_agent != "END":
            return "execute"
        print(f"🏁 Routing to end")
        return "end"

    # Convenience methods for agent management
    def add_agent(self, name: str, agent: Any, description: str, active: bool = True):
        """Add an agent to the supervisor's registry."""
        if hasattr(self, "_current_state") and self._current_state:
            self._current_state.add_agent(name, agent, description, active)
            self._sync_tools_from_state()
        else:
            passed")

    def remove_agent(self, name: str) -> bool:
        """Remove an agent from the supervisor's registry."""
        if hasattr(self, "_current_state") and self._current_state:
            result = self._current_state.remove_agent(name)
            if result:
                self._sync_tools_from_state()
            return result
        return False

    def list_agents(self) -> dict[str, str]:
        """List all agents in the registry."""
        if hasattr(self, "_current_state") and self._current_state:
            return self._current_state.list_all_agents()
        return {}

    def get_agent_tools(self) -> list:
        """Get current dynamic tools generated from agents."""
        if hasattr(self, "_current_state") and self._current_state:
            return self._current_state.get_all_tools()
        return []


# Factory function for easy creation
def create_dynamic_supervisor(
    name: str = "dynamic_supervisor",
    engine: AugLLMConfig | None = None,
    initial_agents: Dict[str, Any] | None = None,
) -> DynamicSupervisor:
    """Create a dynamic supervisor with optional initial agents.

    Args:
        name: Supervisor name
        engine: Optional custom engine (uses default if not provided)
        initial_agents: Dict of {agent_name: {"agent": agent, "description": str, "active": bool}}

    Returns:
        Configured DynamicSupervisor ready for use
    """

    supervisor = DynamicSupervisor(name=name, engine=engine)

    # Add initial agents if provided
    if initial_agents:
        state = supervisor.state_schema()
        for agent_name, agent_config in initial_agents.items():
            state.add_agent(
                agent_name,
                agent_config["agent"],
                agent_config["description"],
                agent_config.get("active", True),
            )
        supervisor._current_state = state
        supervisor._sync_tools_from_state()

    return supervisor
