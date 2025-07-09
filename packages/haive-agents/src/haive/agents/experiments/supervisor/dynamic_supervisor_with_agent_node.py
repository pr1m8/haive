"""
Dynamic supervisor with general agent execution node.

This implementation uses a single agent_execution_node that can execute any agent
dynamically based on the supervisor's routing decision, similar to how tool_node works.
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

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


# Enhanced Agent Registry with activation
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
        capabilities: List[str],
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

    def get_active_agents(self) -> Dict[str, Any]:
        """Get only active agents with their metadata."""
        return {
            name: {"agent": self.agents[name], "metadata": self.agent_metadata[name]}
            for name in self.active_agents
        }

    def get_agent(self, name: str) -> Optional[Any]:
        """Get an agent if it exists and is active."""
        if name in self.active_agents:
            return self.agents[name]
        return None

    def find_agents_by_capability(self, capability: str) -> List[str]:
        """Find all agents (active or inactive) with a specific capability."""
        matching_agents = []
        for name, metadata in self.agent_metadata.items():
            if capability in metadata["capabilities"]:
                matching_agents.append(name)
        return matching_agents


# Supervisor State with agent routing
class DynamicSupervisorState(StateSchema):
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    current_task: str = Field(default="")
    agent_route: Optional[str] = Field(default=None)  # Which agent to route to
    agent_response: Optional[str] = Field(default=None)  # Response from agent
    required_capabilities: List[str] = Field(default_factory=list)
    execution_history: List[Dict[str, Any]] = Field(default_factory=list)


# Dynamic Supervisor with Agent Execution Node
class DynamicNodeSupervisor(ReactAgent):
    """Supervisor that uses a general agent execution node instead of pre-compiled handoffs."""

    agent_registry: DynamicAgentRegistry = Field(default_factory=DynamicAgentRegistry)
    agent_choice_model: Optional[DynamicChoiceModel] = Field(default=None)

    @model_validator(mode="after")
    def setup_dynamic_supervisor(self):
        """Setup supervisor with dynamic routing capabilities."""
        # Initialize choice model
        self._update_choice_model()

        # Setup tools
        self._setup_supervisor_tools()

        return self

    def _update_choice_model(self):
        """Update the dynamic choice model based on active agents."""
        active_agents = list(self.agent_registry.active_agents)

        if active_agents:
            # Create choices including "none" option
            choices = active_agents + ["none"]
            self.agent_choice_model = DynamicChoiceModel.from_choices(
                choices,
                name="AgentRouting",
                description="Select which agent to route the task to, or 'none' to handle it yourself",
            )

    def _setup_supervisor_tools(self):
        """Setup supervisor-specific tools."""
        tools = []

        # Tool to analyze task requirements
        @tool
        def analyze_task_requirements(task: str) -> Dict[str, Any]:
            """Analyze a task to determine required capabilities."""
            capabilities = []

            # Simple capability detection
            task_lower = task.lower()
            if any(
                word in task_lower
                for word in ["research", "search", "find", "investigate"]
            ):
                capabilities.append("research")
            if any(
                word in task_lower
                for word in ["calculate", "compute", "math", "sum", "multiply"]
            ):
                capabilities.append("math")
            if any(
                word in task_lower for word in ["write", "essay", "document", "compose"]
            ):
                capabilities.append("writing")
            if any(word in task_lower for word in ["analyze", "data", "statistics"]):
                capabilities.append("analysis")

            return {
                "task": task,
                "required_capabilities": capabilities,
                "complexity": "simple" if len(capabilities) <= 1 else "complex",
            }

        # Tool to check agent availability
        @tool
        def check_agent_availability(capability: str) -> Dict[str, Any]:
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

        # Tool to activate an agent
        @tool
        def activate_agent(agent_name: str) -> str:
            """Activate an inactive agent to make it available for tasks."""
            if agent_name not in self.agent_registry.agents:
                return f"Error: Agent '{agent_name}' not found in registry"

            if agent_name in self.agent_registry.active_agents:
                return f"Agent '{agent_name}' is already active"

            success = self.agent_registry.activate_agent(agent_name)
            if success:
                # Update choice model after activation
                self._update_choice_model()
                return f"Successfully activated agent '{agent_name}'"
            else:
                return f"Failed to activate agent '{agent_name}'"

        # Tool to route to agent (sets the routing decision)
        @tool
        def route_to_agent(agent_name: str, task_description: str) -> str:
            """Route a task to a specific agent for execution."""
            if agent_name not in self.agent_registry.active_agents:
                return f"Error: Agent '{agent_name}' is not active. Activate it first."

            # This tool just sets the routing decision
            # The actual execution happens in the agent_execution_node
            return f"Task routed to {agent_name}: {task_description}"

        # Tool to list agents
        @tool
        def list_agents() -> Dict[str, Any]:
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

        # Add tools to engine
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

        # Supervisor decision node
        graph.add_node("supervisor", self._supervisor_node)

        # Agent execution node (general purpose)
        graph.add_node("agent_execution", self._agent_execution_node)

        # Result processing node
        graph.add_node("process_result", self._process_result_node)

        # Add edges
        graph.set_entry_point("supervisor")

        # Conditional edge from supervisor
        graph.add_conditional_edges(
            "supervisor",
            self._route_decision,
            {"execute_agent": "agent_execution", "end": END},
        )

        # From agent execution to result processing
        graph.add_edge("agent_execution", "process_result")

        # From result processing back to supervisor (for multi-step tasks)
        graph.add_edge("process_result", "supervisor")

        return graph.compile()

    async def _supervisor_node(self, state: DynamicSupervisorState) -> Dict[str, Any]:
        """Supervisor node that makes routing decisions."""
        # Use the engine to analyze and decide
        task = (
            state.current_task or state.messages[-1]["content"]
            if state.messages
            else ""
        )

        # Create prompt for supervisor
        prompt = f"""
You are a supervisor managing multiple specialized agents. 

Current task: {task}

Available agents: {list(self.agent_registry.active_agents)}

Your job:
1. Analyze the task requirements
2. Check which agents are available
3. If a required agent is inactive, activate it
4. Route the task to the appropriate agent
5. If you can handle it yourself, don't route to any agent

Use the tools provided to analyze, check availability, activate agents, and route tasks.
"""

        result = await self.engine.ainvoke({"messages": [HumanMessage(content=prompt)]})

        # Extract routing decision from result
        if hasattr(result, "agent_route"):
            state.agent_route = result.agent_route

        return {"state": state}

    async def _agent_execution_node(
        self, state: DynamicSupervisorState
    ) -> Dict[str, Any]:
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
            # Execute the agent with the current task
            result = await agent.arun(state.current_task)
            state.agent_response = result

            # Record execution
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
            state.agent_response = f"Error executing {state.agent_route}: {str(e)}"
            state.execution_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "agent": state.agent_route,
                    "task": state.current_task,
                    "error": str(e),
                    "success": False,
                }
            )

        # Clear route after execution
        state.agent_route = None

        return {"state": state}

    async def _process_result_node(
        self, state: DynamicSupervisorState
    ) -> Dict[str, Any]:
        """Process results from agent execution."""
        if state.agent_response:
            # Add response to messages
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


# Test the dynamic supervisor
async def test_dynamic_node_supervisor():
    """Test the supervisor with dynamic agent activation."""

    print("Creating specialized agents...")

    # Create test agents
    from haive.tools.tools.search_tools import tavily_search_tool

    # Research agent
    research_engine = AugLLMConfig(
        name="research_engine",
        model="gpt-4",
        tools=[tavily_search_tool],
        system_message="You are a research specialist.",
    ).create()

    research_agent = ReactAgent(name="research_agent", engine=research_engine)

    # Math agent
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

    # Essay writer (INACTIVE)
    from haive.core.structured_output import create_structured_output_engine

    class Essay(BaseModel):
        title: str
        introduction: str
        body: List[str]
        conclusion: str

    essay_engine = create_structured_output_engine(
        model_config=LLMConfig(model="gpt-4"),
        output_schema=Essay,
        system_message="You are an essay writer.",
    )

    essay_agent = SimpleAgent(name="essay_agent", engine=essay_engine)

    # Create supervisor
    print("\nCreating dynamic supervisor...")

    supervisor_engine = AugLLMConfig(
        name="supervisor_engine",
        model="gpt-4",
        tools=[],  # Tools added dynamically
        system_message="You are a dynamic task supervisor.",
    ).create()

    supervisor = DynamicNodeSupervisor(
        name="dynamic_supervisor",
        engine=supervisor_engine,
        state_schema=DynamicSupervisorState,
    )

    # Register agents
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
        active=False,  # STARTS INACTIVE
    )

    # Test 1: Task needing only active agents
    print("\n--- Test 1: Math calculation ---")
    result1 = await supervisor.arun(
        "Calculate the compound interest on $10,000 at 5% for 10 years"
    )
    print(f"Result: {result1}")

    # Test 2: Task needing inactive agent
    print("\n--- Test 2: Essay writing (needs activation) ---")
    result2 = await supervisor.arun(
        "Write an essay about the benefits of renewable energy"
    )
    print(f"Result: {result2}")

    # Check final state
    print("\n--- Final State ---")
    print(f"Active agents: {list(supervisor.agent_registry.active_agents)}")
    print(f"Execution history: {len(supervisor.state.execution_history)} entries")


if __name__ == "__main__":
    asyncio.run(test_dynamic_node_supervisor())
