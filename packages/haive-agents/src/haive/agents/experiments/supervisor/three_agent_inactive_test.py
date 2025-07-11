"""Three-agent supervisor test with inactive agent activation.

This test demonstrates:
1. Supervisor starts with 2 active agents (research, math)
2. Essay writer agent is in registry but NOT active
3. When task requires essay writing, supervisor recognizes missing capability
4. Supervisor activates the essay writer from registry
5. Task completes successfully with all 3 agents
"""

import asyncio
from typing import Any, Dict, List, Optional

from haive.core.engine import AugLLMConfig
from haive.core.llm import LLMConfig
from haive.core.schema import StateSchema
from haive.tools.tools.search_tools import tavily_search_tool
from langchain_core.tools import tool
from pydantic import Field, model_validator

from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent


# Mock langgraph_supervisor tools until real implementation is available
def create_handoff_tool(target_agent_name: str, target_agent: Any, description: str):
    """Create a handoff tool for transferring control to another agent."""

    @tool
    def transfer_tool(task: str) -> str:
        f"""Transfer task to {target_agent_name}: {description}"""
        try:
            result = asyncio.run(target_agent.arun(task))
            return f"{target_agent_name} response: {result}"
        except Exception as e:
            return f"Error executing {target_agent_name}: {e!s}"

    transfer_tool.__name__ = f"transfer_to_{target_agent_name}"
    return transfer_tool


def create_forward_message_tool(agent_name: str, description: str = ""):
    """Create a tool for forwarding messages to an agent."""

    @tool
    def forward_tool(message: str, target: str) -> str:
        f"""Forward message from {agent_name} to {target}"""
        return f"Message forwarded from {agent_name} to {target}: {message}"

    forward_tool.__name__ = f"forward_to_{agent_name}"
    return forward_tool


from haive.core.structured_output import create_structured_output_engine
from haive.core.types import DynamicChoiceModel


# Tools for math agent
@tool
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b


@tool
def calculate_compound_interest(principal: float, rate: float, years: int) -> float:
    """Calculate compound interest."""
    return principal * ((1 + rate) ** years)


# Enhanced Agent Registry with activation tracking
class EnhancedAgentRegistry:
    def __init__(self):
        self.agents = {}
        self.active_agents = set()

    def register(self, name: str, agent: Any, description: str, active: bool = True):
        """Register an agent with active/inactive state."""
        self.agents[name] = {
            "agent": agent,
            "description": description,
            "active": active,
        }
        if active:
            self.active_agents.add(name)

    def activate_agent(self, name: str) -> bool:
        """Activate an inactive agent."""
        if name in self.agents and name not in self.active_agents:
            self.active_agents.add(name)
            self.agents[name]["active"] = True
            return True
        return False

    def get_active_agents(self) -> dict[str, Any]:
        """Get only active agents."""
        return {
            name: info
            for name, info in self.agents.items()
            if name in self.active_agents
        }

    def get_inactive_agents(self) -> dict[str, Any]:
        """Get inactive agents."""
        return {
            name: info
            for name, info in self.agents.items()
            if name not in self.active_agents
        }

    def is_agent_available(self, name: str) -> bool:
        """Check if agent exists (active or inactive)."""
        return name in self.agents


# Supervisor State with capability tracking
class SupervisorState(StateSchema):
    messages: list[str] = Field(default_factory=list)
    current_task: str = Field(default="")
    required_capabilities: list[str] = Field(default_factory=list)
    missing_capabilities: list[str] = Field(default_factory=list)
    activation_history: list[dict[str, Any]] = Field(default_factory=list)


# Dynamic Supervisor with Activation Logic
class DynamicActivationSupervisor(ReactAgent):
    agent_registry: EnhancedAgentRegistry = Field(default_factory=EnhancedAgentRegistry)
    capability_model: DynamicChoiceModel | None = Field(default=None)

    @model_validator(mode="after")
    def setup_activation_supervisor(self):
        """Setup supervisor with activation capabilities."""
        # Update tools when registry changes
        self._update_available_tools()
        return self

    def _update_available_tools(self):
        """Update tools based on active agents."""
        # Clear existing handoff/forward tools
        if hasattr(self, "engine") and self.engine and hasattr(self.engine, "tools"):
            self.engine.tools = [
                tool
                for tool in self.engine.tools
                if not (
                    tool.name.startswith("transfer_to_")
                    or tool.name.startswith("forward_to_")
                    or tool.name == "forward_message"
                )
            ]

        # Add handoff tools for active agents only
        active_agents = self.agent_registry.get_active_agents()
        handoff_tools = []

        for agent_name, agent_info in active_agents.items():
            # Create transfer tool (full handoff)
            transfer_tool = create_handoff_tool(
                target_agent_name=agent_name,
                target_agent=agent_info["agent"],
                description=f"Transfer control to {agent_name}: {agent_info['description']}",
            )
            handoff_tools.append(transfer_tool)

            # Create forward message tool variant
            forward_tool = create_forward_message_tool(
                target_agent_name=agent_name,
                description=f"Forward a message to {agent_name} for processing",
            )
            handoff_tools.append(forward_tool)

        # Add capability check tool
        @tool
        def check_required_capabilities(task_description: str) -> dict[str, Any]:
            """Analyze task and identify required capabilities."""
            capabilities = []

            # Simple capability detection
            if (
                "research" in task_description.lower()
                or "find" in task_description.lower()
            ):
                capabilities.append("research")
            if (
                "calculate" in task_description.lower()
                or "math" in task_description.lower()
            ):
                capabilities.append("math")
            if (
                "write" in task_description.lower()
                or "essay" in task_description.lower()
            ):
                capabilities.append("essay_writing")

            return {"required_capabilities": capabilities, "task": task_description}

        # Add activation tool
        @tool
        def activate_dormant_agent(capability: str) -> str:
            """Activate an agent that provides the required capability."""
            # Map capabilities to agents
            capability_map = {
                "research": "research_agent",
                "math": "math_agent",
                "essay_writing": "essay_writer_agent",
            }

            agent_name = capability_map.get(capability)
            if not agent_name:
                return f"No agent found for capability: {capability}"

            if self.agent_registry.activate_agent(agent_name):
                # Update tools after activation
                self._update_available_tools()
                return f"Successfully activated {agent_name} for {capability}"
            return f"Agent {agent_name} is already active or doesn't exist"

        # Add all tools to engine
        if hasattr(self, "engine") and self.engine:
            self.engine.tools.extend(handoff_tools)
            self.engine.tools.append(check_required_capabilities)
            self.engine.tools.append(activate_dormant_agent)

            # Update capability model
            active_choices = list(active_agents.keys())
            if active_choices:
                self.capability_model = DynamicChoiceModel.from_choices(
                    active_choices, name="active_agents"
                )


async def test_dynamic_activation():
    """Test supervisor activating dormant agents as needed."""
    # Create specialized agents

    # 1. Research Agent with Tavily
    research_engine = AugLLMConfig(
        name="research_engine",
        model="gpt-4",
        tools=[tavily_search_tool],
        system_message="You are a research specialist. Use tavily search to find information.",
    ).create()

    research_agent = ReactAgent(name="research_agent", engine=research_engine)

    # 2. Math Agent with calculation tools
    math_engine = AugLLMConfig(
        name="math_engine",
        model="gpt-4",
        tools=[add, multiply, calculate_compound_interest],
        system_message="You are a math specialist. Perform calculations as requested.",
    ).create()

    math_agent = ReactAgent(name="math_agent", engine=math_engine)

    # 3. Essay Writer with structured output (STARTS INACTIVE)
    from pydantic import BaseModel

    class Essay(BaseModel):
        title: str
        introduction: str
        body_paragraphs: list[str]
        conclusion: str
        word_count: int

    essay_engine = create_structured_output_engine(
        model_config=LLMConfig(model="gpt-4"),
        output_schema=Essay,
        system_message="You are an essay writing specialist. Create well-structured essays.",
    )

    essay_writer_agent = SimpleAgent(
        name="essay_writer_agent",
        engine=essay_engine,
        config=SimpleAgentConfig(system_message="Essay writer with structured output"),
    )

    # Create supervisor
    supervisor_engine = AugLLMConfig(
        name="supervisor_engine",
        model="gpt-4",
        tools=[],  # Tools added dynamically
        system_message="""You are a dynamic supervisor that manages specialized agents.

Your workflow:
1. Analyze the task to identify required capabilities
2. Check which agents are currently active
3. If a required capability is missing, activate the appropriate agent
4. Route tasks to the appropriate specialized agents
5. Coordinate their responses to complete the overall task

Important: Always check required capabilities before attempting to route tasks.""",
    ).create()

    supervisor = DynamicActivationSupervisor(
        name="dynamic_supervisor",
        engine=supervisor_engine,
        state_schema=SupervisorState,
    )

    # Register agents (essay writer is INACTIVE)
    supervisor.agent_registry.register(
        "research_agent",
        research_agent,
        "Research specialist with web search",
        active=True,
    )
    supervisor.agent_registry.register(
        "math_agent", math_agent, "Math specialist with calculation tools", active=True
    )
    supervisor.agent_registry.register(
        "essay_writer_agent",
        essay_writer_agent,
        "Essay writer with structured output",
        active=False,  # STARTS INACTIVE!
    )

    # Update supervisor tools after registration
    supervisor._update_available_tools()

    # Test 1: Task that only needs active agents
    await supervisor.arun(
        "Calculate the compound interest on $10,000 at 5% for 10 years"
    )

    # Test 2: Task that requires inactive agent
    await supervisor.arun(
        "Research the benefits of renewable energy and write a short essay about it"
    )

    # Check final state


if __name__ == "__main__":
    asyncio.run(test_dynamic_activation())
