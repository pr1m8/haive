"""Simple test to confirm the key findings about parser field requirements."""

from typing import Optional

from pydantic import BaseModel, Field, create_model


def test_key_insight():
    """Test the key insight about Pydantic field handling."""

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


    # The critical test: Can we update state with a field that doesn't exist?
    try:
        update_dict = {"taskresult": structured_result, "messages": ["updated"]}

        # This is what parser node essentially does
        updated_state = MinimalState(**{**state.model_dump(), **update_dict})


        # Check if the structured result is actually there
        if hasattr(updated_state, "taskresult"):
            pass
        else:
            pass")

    except Exception as e:
        pass")



def test_schema_composer_approach():
    """Test if SchemaComposer approach would work."""

    class TaskResult(BaseModel):
        summary: str
        completed: bool

    # Simulate what SchemaComposer does automatically
    mock_engine_fields = {"messages": (list, Field(default_factory=list))}


    # This is what SchemaComposer.add_fields_from_engine() does
    final_fields = {**mock_engine_fields}
    final_fields["taskresult"] = (Optional[TaskResult], Field(default=None))

    ComposedState = create_model("ComposedState", **final_fields)


    # Test if this works
    state = ComposedState(messages=["test"])
    structured_result = TaskResult(summary="Auto-composed", completed=True)

    update_dict = {"taskresult": structured_result}
    updated_state = ComposedState(**{**state.model_dump(), **update_dict})




if __name__ == "__main__":
    test_key_insight()
    test_schema_composer_approach()

