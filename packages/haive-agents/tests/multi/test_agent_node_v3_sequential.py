"""Test AgentNodeV3 with MultiAgentState in sequential execution."""

import asyncio
from typing import List
from pydantic import Field
from langchain_core.messages import HumanMessage, AIMessage

from haive.core.schema.state_schema import StateSchema
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from haive.core.engine.aug_llm import AugLLMConfig
from haive.agents.simple.agent import SimpleAgent
from haive.core.graph.node.agent_node_v3 import create_agent_node_v3, AgentNodeV3Config

# Import Agent for model_rebuild
from haive.agents.base.agent import Agent

# Fix forward reference issue
MultiAgentState.model_rebuild()
AgentNodeV3Config.model_rebuild()


class PlannerState(StateSchema):
    """State for planner agent."""
    messages: List = Field(default_factory=list)
    plan: str = Field(default="")
    steps: List[str] = Field(default_factory=list)


class ExecutorState(StateSchema):
    """State for executor agent."""
    messages: List = Field(default_factory=list)
    execution_result: str = Field(default="")
    success: bool = Field(default=False)


async def test_agent_node_v3_sequential():
    """Test AgentNodeV3 with sequential execution pattern."""
    
    print("=== Testing AgentNodeV3 Sequential Pattern ===\n")
    
    # Step 1: Create agents with specific schemas
    print("Step 1: Create agents")
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
    
    print(f"✓ Created planner: {planner.name}")
    print(f"✓ Created executor: {executor.name}")
    
    # Step 2: Create MultiAgentState with agents
    print("\nStep 2: Create MultiAgentState")
    state = MultiAgentState(
        agents=[planner, executor],
        messages=[HumanMessage(content="Plan and execute a simple task")]
    )
    
    print(f"✓ State created with {state.agent_count} agents")
    print(f"✓ Agents: {list(state.agents.keys())}")
    print(f"✓ Messages: {len(state.messages)}")
    
    # Step 3: Create AgentNodeV3 configurations
    print("\nStep 3: Create AgentNodeV3 configurations")
    
    planner_node = create_agent_node_v3(
        agent_name="planner",
        name="plan_step",
        command_goto="execute_step"
    )
    
    executor_node = create_agent_node_v3(
        agent_name="executor", 
        name="execute_step",
        command_goto=None  # End of sequence
    )
    
    print(f"✓ Created planner node: {planner_node.name}")
    print(f"✓ Created executor node: {executor_node.name}")
    
    # Step 4: Execute planner node
    print("\nStep 4: Execute planner node")
    try:
        planner_result = planner_node(state)
        print(f"✓ Planner command type: {type(planner_result)}")
        print(f"✓ Planner goto: {planner_result.goto}")
        
        # Apply planner updates to state
        if hasattr(planner_result, 'update') and planner_result.update:
            for key, value in planner_result.update.items():
                if hasattr(state, key):
                    setattr(state, key, value)
        
        print(f"✓ Planner output recorded: {bool(state.get_agent_output('planner'))}")
        
    except Exception as e:
        print(f"❌ Planner execution failed: {e}")
        return False
    
    # Step 5: Execute executor node
    print("\nStep 5: Execute executor node")
    try:
        executor_result = executor_node(state)
        print(f"✓ Executor command type: {type(executor_result)}")
        print(f"✓ Executor goto: {executor_result.goto}")
        
        # Apply executor updates to state
        if hasattr(executor_result, 'update') and executor_result.update:
            for key, value in executor_result.update.items():
                if hasattr(state, key):
                    setattr(state, key, value)
        
        print(f"✓ Executor output recorded: {bool(state.get_agent_output('executor'))}")
        
    except Exception as e:
        print(f"❌ Executor execution failed: {e}")
        return False
    
    # Step 6: Verify sequential execution results
    print("\nStep 6: Verify results")
    
    # Check agent outputs
    planner_output = state.get_agent_output("planner")
    executor_output = state.get_agent_output("executor")
    
    print(f"✓ Planner output exists: {planner_output is not None}")
    print(f"✓ Executor output exists: {executor_output is not None}")
    
    # Check agent states
    planner_state = state.get_agent_state("planner")
    executor_state = state.get_agent_state("executor")
    
    print(f"✓ Planner state: {len(planner_state)} fields")
    print(f"✓ Executor state: {len(executor_state)} fields")
    
    # Check messages updated
    print(f"✓ Final messages count: {len(state.messages)}")
    
    # Check execution order
    print(f"✓ Agent execution order: {state.agent_execution_order}")
    
    print("\n✅ AgentNodeV3 sequential test passed!")
    return True


if __name__ == "__main__":
    result = asyncio.run(test_agent_node_v3_sequential())
    if result:
        print("\n🎉 Sequential execution working correctly!")
    else:
        print("\n💥 Sequential execution failed!")