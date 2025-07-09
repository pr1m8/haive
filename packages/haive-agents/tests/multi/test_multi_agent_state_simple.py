"""Test MultiAgentState without circular imports."""

from typing import List
from pydantic import Field
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from haive.core.schema.state_schema import StateSchema
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState

# Fix the forward reference issue
MultiAgentState.model_rebuild()

# Test basic MultiAgentState functionality
def test_multi_agent_state():
    """Test MultiAgentState functionality."""
    
    print("=== Testing MultiAgentState ===\n")
    
    # Test 1: Create empty MultiAgentState
    print("Test 1: Create empty MultiAgentState")
    state = MultiAgentState()
    print(f"✓ Created state with fields: {list(state.model_fields.keys())}")
    
    # Test 2: Test agent states
    print("\nTest 2: Test agent states")
    state.update_agent_state("planner", {"plan": "Step 1", "status": "planning"})
    state.update_agent_state("executor", {"result": None, "status": "waiting"})
    
    print(f"✓ Planner state: {state.get_agent_state('planner')}")
    print(f"✓ Executor state: {state.get_agent_state('executor')}")
    
    # Test 3: Test recompilation tracking
    print("\nTest 3: Test recompilation tracking")
    state.mark_agent_for_recompile("planner", "Tools changed")
    print(f"✓ Agents needing recompile: {state.agents_needing_recompile}")
    
    state.resolve_agent_recompile("planner")
    print(f"✓ After resolve: {state.agents_needing_recompile}")
    print(f"✓ Recompile count: {state.recompile_count}")
    
    # Test 4: Test agent outputs
    print("\nTest 4: Test agent outputs")
    state.record_agent_output("planner", {"plan": "Complete plan", "steps": 3})
    state.record_agent_output("executor", {"result": "Success", "data": [1, 2, 3]})
    
    print(f"✓ Planner output: {state.get_agent_output('planner')}")
    print(f"✓ Executor output: {state.get_agent_output('executor')}")
    
    # Test 5: Test messages (inherited from ToolState)
    print("\nTest 5: Test messages")
    state.messages = [HumanMessage(content="Hello"), AIMessage(content="Hi there!")]
    print(f"✓ Messages: {len(state.messages)} messages")
    
    # Test 6: Test computed properties
    print("\nTest 6: Test computed properties")
    print(f"✓ Agent count: {state.agent_count}")
    print(f"✓ Has active agent: {state.has_active_agent}")
    print(f"✓ Needs any recompile: {state.needs_any_recompile}")
    
    print("\n✅ All tests passed!")
    return state


if __name__ == "__main__":
    state = test_multi_agent_state()