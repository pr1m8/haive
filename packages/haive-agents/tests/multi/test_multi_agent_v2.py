"""Test MultiAgentV2 with proper state management."""

from typing import List

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from haive.core.schema.state_schema import StateSchema
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from pydantic import Field

from haive.agents.multi.multi_agent_v2 import ExecutionMode, MultiAgentV2
from haive.agents.simple.agent import SimpleAgent


# Define specific agent state schemas
class PlannerState(StateSchema):
    """State for planner agent."""

    messages: list[BaseMessage] = Field(default_factory=list)
    plan: str = Field(default="")
    steps: list[str] = Field(default_factory=list)


class ExecutorState(StateSchema):
    """State for executor agent."""

    messages: list[BaseMessage] = Field(default_factory=list)
    execution_result: str = Field(default="")
    success: bool = Field(default=False)


async def test_multi_agent_v2():
    """Test MultiAgentV2 functionality."""
    # Create agents with specific state schemas
    planner = SimpleAgent(
        name="planner", engine=AugLLMConfig(), state_schema=PlannerState
    )

    executor = SimpleAgent(
        name="executor", engine=AugLLMConfig(), state_schema=ExecutorState
    )

    # Test 1: Create from list of agents
    multi_agent = MultiAgentV2.from_agents(
        agents=[planner, executor],
        name="plan_execute_system",
        execution_mode=ExecutionMode.SEQUENCE,
    )

    # Test 2: Create from dict
    MultiAgentV2.from_agents(
        agents={"plan": planner, "exec": executor},
        execution_mode=ExecutionMode.PARALLEL,
    )

    # Test 3: Add agent
    reviewer = SimpleAgent(name="reviewer", engine=AugLLMConfig())
    multi_agent3 = multi_agent.add_agent(reviewer, rebuild=False)

    # Test 4: Remove agent
    multi_agent3.remove_agent("reviewer", rebuild=False)

    # Test 5: Build graph
    multi_agent.build_graph()

    # Test 6: State projection (simulate)
    state = MultiAgentState(agents=multi_agent.agents)

    # Update planner's isolated state
    state.update_agent_state(
        "planner",
        {"plan": "Step 1: Analyze\nStep 2: Execute", "steps": ["analyze", "execute"]},
    )

    state.get_agent_state("planner")

    # Test 7: Rebuild with new agents
    new_planner = SimpleAgent(name="planner_v2", engine=AugLLMConfig())
    MultiAgentV2.rebuild_with_agents(multi_agent, new_agents=[new_planner, executor])


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_multi_agent_v2())
