"""Test MultiAgentV2 with proper state management."""

from typing import List
from pydantic import Field
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from haive.core.schema.state_schema import StateSchema
from haive.core.engine.aug_llm import AugLLMConfig
from haive.agents.simple.agent import SimpleAgent
from haive.agents.multi.multi_agent_v2 import MultiAgentV2, ExecutionMode
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState


# Define specific agent state schemas
class PlannerState(StateSchema):
    """State for planner agent."""
    messages: List[BaseMessage] = Field(default_factory=list)
    plan: str = Field(default="")
    steps: List[str] = Field(default_factory=list)


class ExecutorState(StateSchema):
    """State for executor agent."""
    messages: List[BaseMessage] = Field(default_factory=list)
    execution_result: str = Field(default="")
    success: bool = Field(default=False)


async def test_multi_agent_v2():
    """Test MultiAgentV2 functionality."""
    
    print("=== Testing MultiAgentV2 ===\n")
    
    # Create agents with specific state schemas
    planner = SimpleAgent(
        name="planner",
        engine=AugLLMConfig(),
        state_schema=PlannerState
    )
    
    executor = SimpleAgent(
        name="executor", 
        engine=AugLLMConfig(),
        state_schema=ExecutorState
    )
    
    # Test 1: Create from list of agents
    print("Test 1: Create MultiAgent from list")
    multi_agent = MultiAgentV2.from_agents(
        agents=[planner, executor],
        name="plan_execute_system",
        execution_mode=ExecutionMode.SEQUENCE
    )
    print(f"✓ Created: {multi_agent.name}")
    print(f"✓ Agents: {list(multi_agent.agents.keys())}")
    print(f"✓ State schema: {multi_agent.state_schema.__name__}")
    
    # Test 2: Create from dict
    print("\nTest 2: Create MultiAgent from dict")
    multi_agent2 = MultiAgentV2.from_agents(
        agents={"plan": planner, "exec": executor},
        execution_mode=ExecutionMode.PARALLEL
    )
    print(f"✓ Agents: {list(multi_agent2.agents.keys())}")
    
    # Test 3: Add agent
    print("\nTest 3: Add agent dynamically")
    reviewer = SimpleAgent(name="reviewer", engine=AugLLMConfig())
    multi_agent3 = multi_agent.add_agent(reviewer, rebuild=False)
    print(f"✓ Agents after add: {list(multi_agent3.agents.keys())}")
    
    # Test 4: Remove agent
    print("\nTest 4: Remove agent")
    multi_agent4 = multi_agent3.remove_agent("reviewer", rebuild=False)
    print(f"✓ Agents after remove: {list(multi_agent4.agents.keys())}")
    
    # Test 5: Build graph
    print("\nTest 5: Build graph")
    graph = multi_agent.build_graph()
    print(f"✓ Graph built successfully")
    
    # Test 6: State projection (simulate)
    print("\nTest 6: State projection")
    state = MultiAgentState(agents=multi_agent.agents)
    
    # Update planner's isolated state
    state.update_agent_state("planner", {
        "plan": "Step 1: Analyze\nStep 2: Execute", 
        "steps": ["analyze", "execute"]
    })
    
    planner_state = state.get_agent_state("planner")
    print(f"✓ Planner state: {planner_state}")
    print(f"✓ Executor state: {state.get_agent_state('executor')}")
    
    # Test 7: Rebuild with new agents
    print("\nTest 7: Rebuild with new agents")
    new_planner = SimpleAgent(name="planner_v2", engine=AugLLMConfig())
    multi_agent5 = MultiAgentV2.rebuild_with_agents(
        multi_agent,
        new_agents=[new_planner, executor]
    )
    print(f"✓ Rebuilt with agents: {list(multi_agent5.agents.keys())}")
    
    print("\n✅ All tests passed!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_multi_agent_v2())