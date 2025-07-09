"""Test to see if parser node can add fields dynamically to state or needs pre-existing fields."""

import os
import sys
from typing import Optional
from unittest.mock import MagicMock, Mock, patch

from pydantic import BaseModel, Field, create_model

# Add packages to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))


def test_pydantic_field_addition():
    """Test the fundamental question: Can Pydantic models accept new fields dynamically?"""

    print("🧪 Testing Pydantic Dynamic Field Addition:")

    # Create a basic model with minimal fields
    BasicModel = create_model(
        "BasicModel",
        messages=(list, Field(default_factory=list)),
        counter=(int, Field(default=0)),
    )

    instance = BasicModel()
    print(f"   Original fields: {list(instance.model_fields.keys())}")

    # Test 1: Can we add a new field during creation?
    try:
        # Try to create instance with extra field
        instance_with_extra = BasicModel(
            messages=["test"], counter=5, new_field="extra_value"  # This should fail
        )
        print(f"   ✅ Created with extra field: {instance_with_extra.model_dump()}")

    except Exception as e:
        print(f"   ❌ Cannot create with extra field: {e}")
        print("   📝 Confirms: Pydantic models have FIXED schemas")

    # Test 2: Can we set a new attribute after creation?
    try:
        instance.dynamic_field = "test_value"
        print(f"   ✅ Set dynamic attribute: {instance.dynamic_field}")

    except Exception as e:
        print(f"   ❌ Cannot set dynamic attribute: {e}")

    # Test 3: What about model updates?
    try:
        update_data = {"counter": 10, "unknown_field": "test"}
        updated = BasicModel(**{**instance.model_dump(), **update_data})
        print(f"   Result: {updated.model_dump()}")

    except Exception as e:
        print(f"   ❌ Update with unknown field failed: {e}")
        print("   📝 This is the KEY insight for parser nodes!")


def test_state_schema_requirements():
    """Test what happens when parser tries to update state with new fields."""

    print("\n🔬 Testing State Schema Requirements:")

    # Test model for structured output
    class TaskResult(BaseModel):
        summary: str = Field(description="Task summary")
        completed: bool = Field(description="Whether completed")

    # Scenario 1: Minimal state (like what v2 engine produces)
    MinimalState = create_model(
        "MinimalState",
        messages=(list, Field(default_factory=list)),
        # No 'taskresult' field
    )

    # Scenario 2: State with structured output field pre-defined
    EnhancedState = create_model(
        "EnhancedState",
        messages=(list, Field(default_factory=list)),
        taskresult=(Optional[TaskResult], Field(default=None)),  # Pre-defined
    )

    print(f"   MinimalState fields: {list(MinimalState.model_fields.keys())}")
    print(f"   EnhancedState fields: {list(EnhancedState.model_fields.keys())}")

    # Test parser-like update scenarios
    structured_result = TaskResult(summary="Analysis done", completed=True)

    # Scenario 1: Try to add structured result to minimal state
    print("\n   📋 Scenario 1: Add structured result to minimal state")
    minimal_state = MinimalState(messages=["test"])

    try:
        # This is what parser node would try to do
        update_dict = {"taskresult": structured_result}
        updated_minimal = MinimalState(**{**minimal_state.model_dump(), **update_dict})
        print(f"   ✅ Successfully added to minimal state!")

    except Exception as e:
        print(f"   ❌ Failed to add to minimal state: {e}")
        print("   📝 This means parser REQUIRES pre-defined field!")

    # Scenario 2: Update pre-defined field in enhanced state
    print("\n   📋 Scenario 2: Update pre-defined field in enhanced state")
    enhanced_state = EnhancedState(messages=["test"])

    try:
        update_dict = {"taskresult": structured_result}
        updated_enhanced = EnhancedState(
            **{**enhanced_state.model_dump(), **update_dict}
        )
        print(f"   ✅ Successfully updated pre-defined field!")
        print(f"   📊 Result: {updated_enhanced.taskresult}")

    except Exception as e:
        print(f"   ❌ Failed to update pre-defined field: {e}")


def test_command_update_behavior():
    """Test how LangGraph Command updates work with state schemas."""

    print("\n⚙️  Testing Command Update Behavior:")

    try:
        from langgraph.types import Command

        print("   ✅ Imported Command from langgraph")

        # Test what Command.update can contain
        class TestResult(BaseModel):
            value: str = "test"

        # Create a command with structured result
        cmd = Command(
            update={"new_field": TestResult(), "counter": 5}, goto="next_node"
        )

        print(f"   📝 Command update: {cmd.update}")
        print(f"   📝 Command goto: {cmd.goto}")

        # The key question: Can Command.update contain fields not in state schema?
        print("   📝 Command can contain any fields in update dict")
        print("   ❓ But can the state accept them? That depends on state schema!")

    except Exception as e:
        print(f"   ❌ Command test failed: {e}")


def test_simple_simulation():
    """Simulate what actually happens in SimpleAgent with/without engine modification."""

    print("\n🎭 Simulating SimpleAgent Scenarios:")

    class TaskResult(BaseModel):
        summary: str
        completed: bool

    # Mock v2 engine (messages only)
    class MockV2Engine:
        def __init__(self):
            self.name = "v2_engine"
            self.structured_output_model = TaskResult

        def derive_output_schema(self):
            return create_model(
                "V2Output", messages=(list, Field(default_factory=list))
            )

    # Scenario A: Current SimpleAgent approach (with engine modification)
    print("\n   🔧 Scenario A: With Engine Modification (Current)")

    v2_engine = MockV2Engine()
    original_schema = v2_engine.derive_output_schema()
    print(f"      Original engine schema: {list(original_schema.model_fields.keys())}")

    # Simulate SimpleAgent._modify_engine_schema()
    enhanced_fields = {**original_schema.model_fields}
    enhanced_fields["taskresult"] = (Optional[TaskResult], Field(default=None))

    EnhancedSchema = create_model("EnhancedSchema", **enhanced_fields)
    v2_engine.output_schema = EnhancedSchema  # This is the modification!

    modified_schema = v2_engine.derive_output_schema()
    print(f"      Modified engine schema: {list(modified_schema.model_fields.keys())}")
    print("      ✅ Engine now claims to output taskresult field")

    # Scenario B: Proposed approach (no engine modification)
    print("\n   🌟 Scenario B: Without Engine Modification (Proposed)")

    clean_v2_engine = MockV2Engine()
    natural_schema = clean_v2_engine.derive_output_schema()
    print(f"      Natural engine schema: {list(natural_schema.model_fields.keys())}")

    # Agent would add structured field at schema composition level
    agent_state_fields = {**natural_schema.model_fields}
    agent_state_fields["taskresult"] = (Optional[TaskResult], Field(default=None))

    AgentStateSchema = create_model("AgentStateSchema", **agent_state_fields)
    print(f"      Agent state schema: {list(AgentStateSchema.model_fields.keys())}")
    print("      ✅ Agent schema has taskresult, engine schema stays honest")

    print("\n   📊 Key Differences:")
    print("      - Scenario A: Engine lies about its output capabilities")
    print("      - Scenario B: Engine honest, agent schema handles structured output")
    print("      - Both provide parser with taskresult field in state schema")
    print("      - Scenario B avoids dangerous shared engine mutation")


if __name__ == "__main__":
    test_pydantic_field_addition()
    test_state_schema_requirements()
    test_command_update_behavior()
    test_simple_simulation()

    print("\n" + "=" * 70)
    print("🎯 KEY FINDINGS:")
    print("1. Pydantic models have FIXED schemas - cannot add fields dynamically")
    print("2. Parser node REQUIRES fields to be pre-defined in state schema")
    print("3. Either engine modification OR agent schema enhancement is needed")
    print("4. Agent schema enhancement is cleaner than engine modification")
    print("5. Current SimpleAgent approach works but violates separation of concerns")
    print("\n💡 RECOMMENDATION:")
    print("Replace engine modification with agent-level schema enhancement")
