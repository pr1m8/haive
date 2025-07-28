"""Core pattern for dynamic agent execution in supervisors.

This demonstrates the key insight: instead of pre-compiled handoff tools,
use a general agent execution node that can run any agent dynamically.
"""

from typing import Any, Literal

from haive.core.graph import BaseGraph
from haive.core.schema import StateSchema
from pydantic import Field


class SupervisorState(StateSchema):
    """State that includes agent routing information."""

    messages: List[dict[str, Any]] = Field(default_factory=list)
    agent_route: str | None = Field(default=None)  # Which agent to execute
    agent_task: str | None = Field(default=None)  # Task for the agent
    agent_response: str | None = Field(default=None)  # Response from agent


class AgentExecutionNodePattern:
    """Pattern for building supervisors with dynamic agent execution."""

    def __init__(self, agent_registry: dict[str, Any]):
        self.agent_registry = agent_registry

    def build_graph(self) -> BaseGraph:
        """Build graph with agent execution node pattern."""
        graph = BaseGraph()

        # 1. Supervisor node decides routing
        graph.add_node("supervisor", self.supervisor_node)

        # 2. Agent execution node (general purpose)
        graph.add_node("agent_execution", self.agent_execution_node)

        # 3. Conditional routing
        graph.add_conditional_edges(
            "supervisof",
            self.route_decision,
            {
                "execute_agent": "agent_execution",
                "continue": "supervisor",
                "end": graph.END,
            },
        )

        # 4. Loop back for multi-step
        graph.add_edge("agent_execution", "supervisor")

        return graph.compile()

    async def supervisor_node(self, state: SupervisorState) -> dict[str, Any]:
        """Supervisor analyzes and sets routing."""
        # Supervisor logic here:
        # - Analyze task
        # - Check available agents
        # - Set state.agent_route and state.agent_task
        # - Or decide to end

        # Example: route to math_agent
        if "calculate" in state.messages[-1]["content"].lower():
            state.agent_route = "math_agent"
            state.agent_task = state.messages[-1]["content"]

        return {"state": state}

    async def agent_execution_node(self, state: SupervisorState) -> dict[str, Any]:
        """Execute ANY agent based on routing - this is the key pattern!"""
        if not state.agent_route:
            return {"state": state}

        # Get agent from registry dynamically
        agent = self.agent_registry.get(state.agent_route)
        if not agent:
            state.agent_response = f"Agent {state.agent_route} not found"
            return {"state": state}

        try:
            # Execute the agent
            result = await agent.arun(state.agent_task)
            state.agent_response = result
        except Exception as e:
            state.agent_response = f"Error: {e!s}"

        # Clear routing for next iteration
        state.agent_route = None
        state.agent_task = None

        return {"state": state}

    def route_decision(
        self, state: SupervisorState
    ) -> Literal["execute_agent", "continue", "end"]:
        """Routing logic."""
        if state.agent_route:
            return "execute_agent"
        if state.agent_response and "DONE" in state.agent_response:
            return "end"
        return "continue"


# Key insight comparison:

# ❌ OLD WAY (Pre-compiled handoff tools):
"""
# Tools must be created before graph compilation
assign_to_math = create_handoff_tool("math_agent", math_agent)
assign_to_research = create_handoff_tool("research_agent", research_agent)

# Can't add new agents after compilation!
graph = StateGraph()
  .add_node(supervisor, tools=[assign_to_math, assign_to_research])
  .add_node(math_agent)
  .add_node(research_agent)
  .compile()  # FROZEN - can't add essay_agent later
"""

# ✅ NEW WAY (Agent execution node):
"""
# Single execution node handles ANY agent
graph = StateGraph()
  .add_node("supervisor")
  .add_node("agent_execution")  # General purpose node
  .compile()

# Can add/remove agents at runtime!
supervisor.agent_registry["essay_agent"] = essay_agent  # Works!
supervisor.agent_registry["new_agent"] = new_agent     # Also works!
"""
