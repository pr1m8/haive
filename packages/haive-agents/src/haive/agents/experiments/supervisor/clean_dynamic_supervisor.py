"""Clean implementation of dynamic supervisor with agent execution node.

Key insight: Instead of pre-compiled handoff tools that are fixed at graph compile time,
we use a general agent_execution_node that can execute any agent based on state routing.
"""

import asyncio
from datetime import datetime
from typing import Annotated, Any, Dict, List, Literal, Optional

from haive.core.common.models.dynamic_choice_model import DynamicChoiceModel
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import LLMConfig
from haive.core.schema import StateSchema
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import END
from pydantic import BaseModel, Field, model_validator

from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent


class AgentRegistry:
    """Registry for managing agents dynamically."""

    def __init__(self):
        self.agents: dict[str, Any] = {}
        self.metadata: dict[str, dict[str, Any]] = {}
        self.active_agents: set = set()

    def register(
        self,
        name: str,
        agent: Any,
        description: str,
        capabilities: list[str],
        active: bool = True,
    ):
        """Register an agent with metadata."""
        self.agents[name] = agent
        self.metadata[name] = {
            "description": description,
            "capabilities": capabilities,
            "registered_at": datetime.now(),
        }
        if active:
            self.active_agents.add(name)

    def activate(self, name: str) -> bool:
        """Activate an inactive agent."""
        if name in self.agents and name not in self.active_agents:
            self.active_agents.add(name)
            return True
        return False

    def get_active_agent(self, name: str) -> Any | None:
        """Get agent if active."""
        if name in self.active_agents:
            return self.agents[name]
        return None

    def find_by_capability(self, capability: str) -> list[str]:
        """Find agents with a capability."""
        return [
            name
            for name, meta in self.metadata.items()
            if capability in meta["capabilities"]
        ]


class SupervisorState(StateSchema):
    """State for dynamic supervisor."""

    messages: list[dict[str, Any]] = Field(default_factory=list)
    current_task: str = Field(default="")
    agent_route: str | None = Field(default=None)  # Key field for routing
    agent_response: str | None = Field(default=None)
    required_capabilities: list[str] = Field(default_factory=list)


class DynamicSupervisor(ReactAgent):
    """Supervisor using agent execution node pattern."""

    registry: AgentRegistry = Field(default_factory=AgentRegistry)
    choice_model: DynamicChoiceModel | None = Field(default=None)

    @model_validator(mode="after")
    def setup_supervisor(self):
        """Initialize supervisor."""
        self._update_choice_model()
        self._setup_tools()
        return self

    def _update_choice_model(self):
        """Update choices based on active agents."""
        active = list(self.registry.active_agents)
        if active:
            self.choice_model = DynamicChoiceModel.from_choices(
                [*active, "none"], name="AgentSelection"
            )

    def _setup_tools(self):
        """Create supervisor tools."""

        @tool
        def analyze_task(task: str) -> dict[str, Any]:
            """Analyze task to determine required capabilities."""
            caps = []
            if "search" in task.lower() or "find" in task.lower():
                caps.append("search")
            if "calculate" in task.lower() or "math" in task.lower():
                caps.append("math")
            if "write" in task.lower() or "essay" in task.lower():
                caps.append("writing")
            return {"task": task, "capabilities": caps}

        @tool
        def check_capability(capability: str) -> dict[str, Any]:
            """Check which agents have a capability."""
            agents = self.registry.find_by_capability(capability)
            active = [a for a in agents if a in self.registry.active_agents]
            inactive = [a for a in agents if a not in self.registry.active_agents]
            return {"capability": capability, "active": active, "inactive": inactive}

        @tool
        def activate_agent(name: str) -> str:
            """Activate an inactive agent."""
            if self.registry.activate(name):
                self._update_choice_model()
                return f"Activated {name}"
            return f"Could not activate {name}"

        @tool
        def select_agent(name: str, task: str) -> str:
            """Select an agent to handle a task. This sets the routing."""
            if name not in self.registry.active_agents:
                return f"Agent {name} is not active"
            # This is the key - we just set routing, not execute
            return f"Selected {name} for task: {task}"

        if hasattr(self, "engine") and self.engine:
            self.engine.tools.extend(
                [analyze_task, check_capability, activate_agent, select_agent]
            )

    def build_graph(self) -> BaseGraph:
        """Build graph with agent execution node."""
        graph = BaseGraph()

        # Main supervisor node
        graph.add_node("supervisor", self._supervisor_node)

        # General agent execution node - THE KEY PATTERN
        graph.add_node("agent_node", self._agent_execution_node)

        # Entry point
        graph.set_entry_point("supervisor")

        # Routing from supervisor
        graph.add_conditional_edges(
            "supervisor", self._check_routing, {"agent": "agent_node", "end": END}
        )

        # Loop back for continued processing
        graph.add_edge("agent_node", "supervisor")

        return graph.compile()

    async def _supervisor_node(self, state: SupervisorState) -> dict[str, Any]:
        """Supervisor analyzes and decides routing."""
        # Get current task
        task = state.messages[-1].get("content", "") if state.messages else state.current_task

        # Use LLM to decide
        prompt = f"""
You are a supervisor. Analyze this task and decide which agent to use.

Task: {task}

Active agents: {list(self.registry.active_agents)}

Steps:
1. Use analyze_task to understand requirements
2. Use check_capability to see available agents
3. If needed agent is inactive, use activate_agent
4. Use select_agent to route the task
5. Set state.agent_route to the selected agent name

If you can handle it yourself, don't select any agent.
"""

        result = await self.engine.ainvoke({"messages": [HumanMessage(content=prompt)]})

        # Extract agent selection from LLM response
        # In a real implementation, this would parse the actual selection
        # For now, we'll simulate it
        if "math_agent" in str(result).lower():
            state.agent_route = "math_agent"
        elif "search_agent" in str(result).lower():
            state.agent_route = "search_agent"
        elif "writer_agent" in str(result).lower():
            state.agent_route = "writer_agent"

        state.current_task = task
        return {"state": state}

    async def _agent_execution_node(self, state: SupervisorState) -> dict[str, Any]:
        """Execute ANY agent based on routing - the key pattern!"""
        if not state.agent_route:
            return {"state": state}

        # Get agent from registry
        agent = self.registry.get_active_agent(state.agent_route)
        if not agent:
            state.agent_response = f"Agent {state.agent_route} not available"
            state.agent_route = None
            return {"state": state}

        try:
            # Execute the selected agent
            result = await agent.arun(state.current_task)
            state.agent_response = result

            # Add to message history
            state.messages.append(
                {"role": "assistant", "content": result, "agent": state.agent_route}
            )
        except Exception as e:
            state.agent_response = f"Error: {e!s}"

        # Clear routing for next iteration
        state.agent_route = None

        return {"state": state}

    def _check_routing(self, state: SupervisorState) -> Literal["agent", "end"]:
        """Determine next step based on state."""
        if state.agent_route:
            return "agent"
        return "end"


# Example usage
async def demo_dynamic_supervisor():
    """Demonstrate the dynamic supervisor pattern."""

    # Create agents
    @tool
    def calculate(expr: str) -> str:
        """Calculate mathematical expression."""
        try:
            return str(eval(expr))
        except:
            return "Invalid expression"

    # Math agent
    math_engine = AugLLMConfig(
        name="math_engine",
        model="gpt-4",
        tools=[calculate],
        system_message="You are a math assistant. Use the calculate tool.",
    ).create()

    math_agent = SimpleAgent(name="math_agent", engine=math_engine)

    # Search agent (mock)
    search_engine = AugLLMConfig(
        name="search_engine",
        model="gpt-4",
        system_message="You are a search assistant. Pretend to search for information.",
    ).create()

    search_agent = SimpleAgent(name="search_agent", engine=search_engine)

    # Writer agent (starts INACTIVE)
    writer_engine = AugLLMConfig(
        name="writer_engine",
        model="gpt-4",
        system_message="You are a writing assistant.",
    ).create()

    writer_agent = SimpleAgent(name="writer_agent", engine=writer_engine)

    # Create supervisor
    supervisor_engine = AugLLMConfig(
        name="supervisor",
        model="gpt-4",
        tools=[],  # Tools added by supervisor
        system_message="You are a task supervisor.",
    ).create()

    supervisor = DynamicSupervisor(
        name="supervisor", engine=supervisor_engine, state_schema=SupervisorState
    )

    # Register agents
    supervisor.registry.register(
        "math_agent",
        math_agent,
        "Mathematical calculations",
        ["math", "calculate"],
        active=True,
    )

    supervisor.registry.register(
        "search_agent",
        search_agent,
        "Information search",
        ["search", "research"],
        active=True,
    )

    supervisor.registry.register(
        "writer_agent",
        writer_agent,
        "Essay and document writing",
        ["writing", "essay"],
        active=False,  # STARTS INACTIVE!
    )


    # Test 1: Math task (active agent)
    result1 = await supervisor.arun("Calculate 25 * 4")

    # Test 2: Writing task (needs activation)
    result2 = await supervisor.arun("Write a haiku about coding")




if __name__ == "__main__":
    # For testing, you can run this directly

    # Uncomment to run the demo:
