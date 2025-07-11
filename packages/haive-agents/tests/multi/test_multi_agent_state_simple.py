"""Test MultiAgentState without circular imports."""

from typing import List

from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from haive.core.schema.state_schema import StateSchema
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from pydantic import Field

# Fix the forward reference issue
MultiAgentState.model_rebuild()


# Test basic MultiAgentState functionality
def test_multi_agent_state():
    """Test MultiAgentState functionality."""
    # Test 1: Create empty MultiAgentState
    state = MultiAgentState()

    # Test 2: Test agent states
    state.update_agent_state("planner", {"plan": "Step 1", "status": "planning"})
    state.update_agent_state("executor", {"result": None, "status": "waiting"})

    # Test 3: Test recompilation tracking
    state.mark_agent_for_recompile("planner", "Tools changed")

    state.resolve_agent_recompile("planner")

    # Test 4: Test agent outputs
    state.record_agent_output("planner", {"plan": "Complete plan", "steps": 3})
    state.record_agent_output("executor", {"result": "Success", "data": [1, 2, 3]})

    # Test 5: Test messages (inherited from ToolState)
    state.messages = [HumanMessage(content="Hello"), AIMessage(content="Hi there!")]

    # Test 6: Test computed properties

    return state


if __name__ == "__main__":
    state = test_multi_agent_state()
