"""Dynamic supervisor with general agent execution node.

This implementation uses a single agent_execution_node that can execute any agent
dynamically based on the supervisor's routing decision, similar to how tool_node works.
"""

import asyncio
from datetime import datetime
from typing import Any, Literal

from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent
from haive.core.common.models.dynamic_choice_model import DynamicChoiceModel
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import LLMConfig
from haive.core.schema import StateSchema
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.graph import END
from pydantic import BaseModel, Field, model_validator


class DynamicAgentRegistry:
    """Registry that tracks agents and their activation status."""

    def __init__(self):
        self.agents = {}
        self.active_agents = set()
        self.agent_metadata = {}

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
        self.agent_metadata[name] = {
            "description": description,
            "capabilities": capabilities,
            "registered_at": datetime.now(),
            "activation_count": 0,
        }
        if active:
            self.active_agents.add(name)

    def activate_agent(self, name: str) -> bool:
        """Activate an inactive agent."""
        if name in self.agents and name not in self.active_agents:
            self.active_agents.add(name)
            self.agent_metadata[name]["activation_count"] += 1
            self.agent_metadata[name]["last_activated"] = datetime.now()
            return True
        return False

    def deactivate_agent(self, name: str) -> bool:
        """Deactivate an active agent."""
        if name in self.active_agents:
            self.active_agents.remove(name)
            return True
        return False

    def get_active_agents(self) -> dict[str, Any]:
        """Get only active agents with their metadata."""
        return {
            name: {"agent": self.agents[name], "metadata": self.agent_metadata[name]}
            for name in self.active_agents
        }

    def get_agent(self, name: str) -> Any | None:
        """Get an agent if it exists and is active."""
        if name in self.active_agents:
            return self.agents[name]
        return None

    def find_agents_by_capability(self, capability: str) -> list[str]:
        """Find all agents (active or inactive) with a specific capability."""
        matching_agents = []
        for name, metadata in self.agent_metadata.items():
            if capability in metadata["capabilities"]:
                matching_agents.append(name)
        return matching_agents


class DynamicSupervisorState(StateSchema):
    messages: list[dict[str, Any]] = Field(default_factory=list)
    current_task: str = Field(default="")
    agent_route: str | None = Field(default=None)
    agent_response: str | None = Field(default=None)
    required_capabilities: list[str] = Field(default_factory=list)
    execution_history: list[dict[str, Any]] = Field(default_factory=list)


class DynamicNodeSupervisor(ReactAgent):
    """Supervisor that uses a general agent execution node instead of pre-compiled handoffs."""

    agent_registry: DynamicAgentRegistry = Field(default_factory=DynamicAgentRegistry)
    agent_choice_model: DynamicChoiceModel | None = Field(default=None)

    @model_validator(mode="after")
    def setup_dynamic_supervisor(self):
        """Setup supervisor with dynamic routing capabilities."""
        self._update_choice_model()
        self._setup_supervisor_tools()
        return self

    def _update_choice_model(self):
        """Update the dynamic choice model based on active agents."""
        active_agents = list(self.agent_registry.active_agents)
        if active_agents:
            choices = [*active_agents, "none"]
            self.agent_choice_model = DynamicChoiceModel.from_choices(
                choices,
                name="AgentRouting",
                description="Select which agent to route the task to, or 'none' to handle it yourself",
            )

    def _setup_supervisor_tools(self):
        """Setup supervisor-specific tools."""

        @tool
        def analyze_task_requirements(task: str) -> dict[str, Any]:
            """Analyze a task to determine required capabilities."""
            capabilities = []
            task_lower = task.lower()
            if any(
                (
                    word in task_lower
                    for word in ["research", "search", "find", "investigate"]
                )
            ):
                capabilities.append("research")
            if any(
                (
                    word in task_lower
                    for word in ["calculate", "compute", "math", "sum", "multiply"]
                )
            ):
                capabilities.append("math")
            if any(
                (
                    word in task_lower
                    for word in ["write", "essay", "document", "compose"]
                )
            ):
                capabilities.append("writing")
            if any((word in task_lower for word in ["analyze", "data", "statistics"])):
                capabilities.append("analysis")
            return {
                "task": task,
                "required_capabilities": capabilities,
                "complexity": "simple" if len(capabilities) <= 1 else "complex",
            }

        @tool
        def check_agent_availability(capability: str) -> dict[str, Any]:
            """Check which agents can handle a specific capability."""
            matching_agents = self.agent_registry.find_agents_by_capability(capability)
            active_matches = [
                a for a in matching_agents if a in self.agent_registry.active_agents
            ]
            inactive_matches = [
                a for a in matching_agents if a not in self.agent_registry.active_agents
            ]
            return {
                "capability": capability,
                "active_agents": active_matches,
                "inactive_agents": inactive_matches,
                "total_matches": len(matching_agents),
            }

        @tool
        def activate_agent(agent_name: str) -> str:
            """Activate an inactive agent to make it available for tasks."""
            if agent_name not in self.agent_registry.agents:
                return f"Error: Agent '{agent_name}' not found in registry"
            if agent_name in self.agent_registry.active_agents:
                return f"Agent '{agent_name}' is already active"
            success = self.agent_registry.activate_agent(agent_name)
            if success:
                self._update_choice_model()
                return f"Successfully activated agent '{agent_name}'"
            return f"Failed to activate agent '{agent_name}'"

        @tool
        def route_to_agent(agent_name: str, task_description: str) -> str:
            """Route a task to a specific agent for execution."""
            if agent_name not in self.agent_registry.active_agents:
                return f"Error: Agent '{agent_name}' is not active. Activate it first."
            return f"Task routed to {agent_name}: {task_description}"

        @tool
        def list_agents() -> dict[str, Any]:
            """List all registered agents and their status."""
            all_agents = {}
            for name in self.agent_registry.agents:
                metadata = self.agent_registry.agent_metadata[name]
                all_agents[name] = {
                    "active": name in self.agent_registry.active_agents,
                    "description": metadata["description"],
                    "capabilities": metadata["capabilities"],
                    "activation_count": metadata["activation_count"],
                }
            return all_agents

        if hasattr(self, "engine") and self.engine:
            self.engine.tools.extend(
                [
                    analyze_task_requirements,
                    check_agent_availability,
                    activate_agent,
                    route_to_agent,
                    list_agents,
                ]
            )

    def build_graph(self) -> BaseGraph:
        """Build graph with dynamic agent execution node."""
        graph = BaseGraph()
        graph.add_node("supervisor", self._supervisor_node)
        graph.add_node("agent_execution", self._agent_execution_node)
        graph.add_node("process_result", self._process_result_node)
        graph.set_entry_point("supervisor")
        graph.add_conditional_edges(
            "supervisor",
            self._route_decision,
            {"execute_agent": "agent_execution", "end": END},
        )
        graph.add_edge("agent_execution", "process_result")
        graph.add_edge("process_result", "supervisor")
        return graph.compile()

    async def _supervisor_node(self, state: DynamicSupervisorState) -> dict[str, Any]:
        """Supervisor node that makes routing decisions."""
        task = (
            state.current_task or state.messages[-1]["content"]
            if state.messages
            else ""
        )
        prompt = f"\nYou are a supervisor managing multiple specialized agents.\n\nCurrent task: {task}\n\nAvailable agents: {list(self.agent_registry.active_agents)}\n\nYour job:\n1. Analyze the task requirements\n2. Check which agents are available\n3. If a required agent is inactive, activate it\n4. Route the task to the appropriate agent\n5. If you can handle it yourself, don't route to any agent\n\nUse the tools provided to analyze, check availability, activate agents, and route tasks.\n"
        result = await self.engine.ainvoke({"messages": [HumanMessage(content=prompt)]})
        if hasattr(result, "agent_route"):
            state.agent_route = result.agent_route
        return {"state": state}

    async def _agent_execution_node(
        self, state: DynamicSupervisorState
    ) -> dict[str, Any]:
        """General node that executes any routed agent."""
        if not state.agent_route:
            state.agent_response = "No agent route specified"
            return {"state": state}
        agent = self.agent_registry.get_agent(state.agent_route)
        if not agent:
            state.agent_response = (
                f"Agent '{state.agent_route}' not found or not active"
            )
            return {"state": state}
        try:
            result = await agent.arun(state.current_task)
            state.agent_response = result
            state.execution_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "agent": state.agent_route,
                    "task": state.current_task,
                    "response_length": len(str(result)),
                    "success": True,
                }
            )
        except Exception as e:
            state.agent_response = f"Error executing {state.agent_route}: {e!s}"
            state.execution_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "agent": state.agent_route,
                    "task": state.current_task,
                    "error": str(e),
                    "success": False,
                }
            )
        state.agent_route = None
        return {"state": state}

    async def _process_result_node(
        self, state: DynamicSupervisorState
    ) -> dict[str, Any]:
        """Process results from agent execution."""
        if state.agent_response:
            state.messages.append(
                {
                    "role": "assistant",
                    "content": state.agent_response,
                    "metadata": {
                        "source": "agent_execution",
                        "timestamp": datetime.now().isoformat(),
                    },
                }
            )
        return {"state": state}

    def _route_decision(
        self, state: DynamicSupervisorState
    ) -> Literal["execute_agent", "end"]:
        """Decide whether to execute an agent or end."""
        if state.agent_route and state.agent_route != "none":
            return "execute_agent"
        return "end"


async def test_dynamic_node_supervisor():
    """Test the supervisor with dynamic agent activation."""
    from haive.tools.tools.search_tools import tavily_search_tool

    research_engine = AugLLMConfig(
        name="research_engine",
        model="gpt-4",
        tools=[tavily_search_tool],
        system_message="You are a research specialist.",
    ).create()
    research_agent = ReactAgent(name="research_agent", engine=research_engine)

    @tool
    def calculate(expression: str) -> float:
        """Calculate a mathematical expression."""
        return eval(expression)

    math_engine = AugLLMConfig(
        name="math_engine",
        model="gpt-4",
        tools=[calculate],
        system_message="You are a math specialist.",
    ).create()
    math_agent = ReactAgent(name="math_agent", engine=math_engine)
    from haive.core.structured_output import create_structured_output_engine

    class Essay(BaseModel):
        title: str
        introduction: str
        body: list[str]
        conclusion: str

    essay_engine = create_structured_output_engine(
        model_config=LLMConfig(model="gpt-4"),
        output_schema=Essay,
        system_message="You are an essay writer.",
    )
    essay_agent = SimpleAgent(name="essay_agent", engine=essay_engine)
    supervisor_engine = AugLLMConfig(
        name="supervisor_engine",
        model="gpt-4",
        tools=[],
        system_message="You are a dynamic task supervisor.",
    ).create()
    supervisor = DynamicNodeSupervisor(
        name="dynamic_supervisor",
        engine=supervisor_engine,
        state_schema=DynamicSupervisorState,
    )
    supervisor.agent_registry.register(
        "research_agent",
        research_agent,
        "Web research and information gathering",
        ["research", "search", "information"],
        active=True,
    )
    supervisor.agent_registry.register(
        "math_agent",
        math_agent,
        "Mathematical calculations and analysis",
        ["math", "calculation", "analysis"],
        active=True,
    )
    supervisor.agent_registry.register(
        "essay_agent",
        essay_agent,
        "Essay writing and document composition",
        ["writing", "essay", "documentation"],
        active=False,
    )
    await supervisor.arun(
        "Calculate the compound interest on $10,000 at 5% for 10 years"
    )
    await supervisor.arun("Write an essay about the benefits of renewable energy")


if __name__ == "__main__":
    asyncio.run(test_dynamic_node_supervisor())
