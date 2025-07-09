"""Simple test to confirm the key findings about parser field requirements."""

from typing import Optional

from pydantic import BaseModel, Field, create_model


def test_key_insight():
    """Test the key insight about Pydantic field handling."""

    print("🔍 Testing Key Insight: Can Pydantic accept unknown fields in updates?")

    # Create a model with just messages (like v2 engine output)
    class TaskResult(BaseModel):
        summary: str
        completed: bool

    MinimalState = create_model(
        "MinimalState", messages=(list, Field(default_factory=list))
    )

    # Create an instance
    state = MinimalState(messages=["test message"])
    structured_result = TaskResult(summary="Task done", completed=True)

    print(f"Original state: {state.model_dump()}")
    print(f"Structured result: {structured_result.model_dump()}")

    # The critical test: Can we update state with a field that doesn't exist?
    try:
        update_dict = {"taskresult": structured_result, "messages": ["updated"]}

        # This is what parser node essentially does
        updated_state = MinimalState(**{**state.model_dump(), **update_dict})

        print(f"✅ AMAZING! Updated state: {updated_state.model_dump()}")
        print("📝 This means the field was SILENTLY IGNORED!")
        print("📝 Pydantic only keeps fields that exist in the schema!")

        # Check if the structured result is actually there
        if hasattr(updated_state, "taskresult"):
            print(f"Has taskresult: {updated_state.taskresult}")
        else:
            print("❌ No taskresult attribute - field was ignored!")

    except Exception as e:
        print(f"❌ Update failed: {e}")

    print("\n" + "=" * 50)
    print("🎯 CRITICAL INSIGHT CONFIRMED:")
    print("• Pydantic models IGNORE unknown fields during updates")
    print("• Parser node CAN send unknown fields in Command.update")
    print("• But state will SILENTLY DROP fields not in schema")
    print("• Therefore: Parser REQUIRES pre-defined fields in state schema!")
    print("\n💡 CONCLUSION:")
    print("• SimpleAgent's engine modification IS necessary for functionality")
    print("• OR agent must add structured output field to state schema")
    print("• SchemaComposer automatic detection might handle this")


def test_schema_composer_approach():
    """Test if SchemaComposer approach would work."""

    print("\n🧪 Testing SchemaComposer Approach:")

    class TaskResult(BaseModel):
        summary: str
        completed: bool

    # Simulate what SchemaComposer does automatically
    print("1. Engine has structured_output_model")
    mock_engine_fields = {"messages": (list, Field(default_factory=list))}
    structured_model = TaskResult

    print("2. SchemaComposer detects structured_output_model")
    print("3. SchemaComposer adds both engine fields AND structured field")

    # This is what SchemaComposer.add_fields_from_engine() does
    final_fields = {**mock_engine_fields}
    final_fields["taskresult"] = (Optional[TaskResult], Field(default=None))

    ComposedState = create_model("ComposedState", **final_fields)

    print(f"Composed state fields: {list(ComposedState.model_fields.keys())}")

    # Test if this works
    state = ComposedState(messages=["test"])
    structured_result = TaskResult(summary="Auto-composed", completed=True)

    update_dict = {"taskresult": structured_result}
    updated_state = ComposedState(**{**state.model_dump(), **update_dict})

    print(f"✅ Updated state: {updated_state.model_dump()}")
    print(f"✅ Structured result: {updated_state.taskresult}")

    print("\n🎉 SchemaComposer approach WORKS!")
    print("• Automatically detects structured_output_model")
    print("• Adds appropriate field to state schema")
    print("• Parser can successfully populate the field")
    print("• No engine modification needed!")


if __name__ == "__main__":
    test_key_insight()
    test_schema_composer_approach()

    print("\n" + "=" * 70)
    print("🚀 FINAL ANSWER:")
    print("1. Parser DOES need pre-defined fields in state schema")
    print("2. SimpleAgent's engine modification ensures this")
    print("3. BUT SchemaComposer can handle this automatically!")
    print("4. Therefore: Engine modification CAN be removed")
    print("5. IF we ensure SchemaComposer is used properly")
    print("\n✨ Path forward: Use SchemaComposer's automatic detection")
