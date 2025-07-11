# src/haive/core/engine/agent/utils/input_handling.py

import logging
from typing import Any, TypeVar

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


def process_input(
    input_data: str | list[str] | dict[str, Any] | BaseModel,
    input_schema: type[T] | None = None,
    runtime_config: RunnableConfig | None = None,
) -> dict[str, Any]:
    """Process input for the agent based on the input schema.

    Args:
        input_data: Input in various formats
        input_schema: Schema for validation
        runtime_config: Optional runtime configuration to include

    Returns:
        Processed input compatible with the graph
    """
    # Extract schema field information if available
    schema_fields = {}

    if input_schema:
        if hasattr(input_schema, "model_fields"):
            # Pydantic v2
            schema_fields = input_schema.model_fields
        elif hasattr(input_schema, "__fields__"):
            # Pydantic v1
            schema_fields = input_schema.__fields__

    # Handle string input
    if isinstance(input_data, str):
        prepared_input = {"messages": [HumanMessage(content=input_data)]}

        # Add runtime config if provided
        if runtime_config:
            prepared_input["__runnable_config__"] = runtime_config

        # Add to other text fields based on schema
        for field_name, field_info in schema_fields.items():
            if field_name not in ["messages", "__runnable_config__"]:
                # Check if field is a string type
                field_type = getattr(field_info, "annotation", None) or getattr(
                    field_info, "type_", None
                )
                if field_type and (
                    "str" in str(field_type) or "String" in str(field_type)
                ):
                    prepared_input[field_name] = input_data

    # Handle list of strings
    elif isinstance(input_data, list) and all(
        isinstance(item, str) for item in input_data
    ):
        # Create messages list
        messages = [HumanMessage(content=item) for item in input_data]
        prepared_input = {"messages": messages}

        # Add runtime config if provided
        if runtime_config:
            prepared_input["__runnable_config__"] = runtime_config

        # Join strings for other text fields
        joined_text = "\n".join(input_data)
        for field_name, field_info in schema_fields.items():
            if field_name not in ["messages", "__runnable_config__"]:
                # Check if field is a string type
                field_type = getattr(field_info, "annotation", None) or getattr(
                    field_info, "type_", None
                )
                if field_type and (
                    "str" in str(field_type) or "String" in str(field_type)
                ):
                    prepared_input[field_name] = joined_text

    # Handle dictionary input
    elif isinstance(input_data, dict):
        # Create a copy to avoid modifying the original
        prepared_input = input_data.copy()

        # Add runtime config if provided
        if runtime_config:
            prepared_input["__runnable_config__"] = runtime_config

        # Ensure there's a messages field if required by schema
        if "messages" not in prepared_input and "messages" in schema_fields:
            # Try to create messages from other fields
            for field in ["input", "query", "content", "text"]:
                if field in prepared_input and isinstance(prepared_input[field], str):
                    prepared_input["messages"] = [
                        HumanMessage(content=prepared_input[field])
                    ]
                    break

    # Handle Pydantic model input
    elif isinstance(input_data, BaseModel):
        # Convert to dict
        if hasattr(input_data, "model_dump"):
            # Pydantic v2
            prepared_input = input_data.model_dump()
        elif hasattr(input_data, "dict"):
            # Pydantic v1
            prepared_input = input_data.dict()
        else:
            # Manual extraction
            prepared_input = {}
            for field in getattr(input_data, "__annotations__", {}):
                if hasattr(input_data, field):
                    prepared_input[field] = getattr(input_data, field)

        # Add runtime config if provided
        if runtime_config:
            prepared_input["__runnable_config__"] = runtime_config

        # Ensure there's a messages field if needed by schema
        if "messages" not in prepared_input and "messages" in schema_fields:
            # Try to create messages from other fields
            for field in ["input", "query", "content", "text"]:
                if field in prepared_input and isinstance(prepared_input[field], str):
                    prepared_input["messages"] = [
                        HumanMessage(content=prepared_input[field])
                    ]
                    break

    # Fallback for other types
    else:
        prepared_input = {"messages": [HumanMessage(content=str(input_data))]}

        # Add runtime config if provided
        if runtime_config:
            prepared_input["__runnable_config__"] = runtime_config

    # Validate against schema if available
    if input_schema:
        try:
            validated = input_schema(**prepared_input)
            # Convert back to dict if validation passed
            if hasattr(validated, "model_dump"):
                return validated.model_dump()
            if hasattr(validated, "dict"):
                return validated.dict()
            return prepared_input
        except Exception as e:
            logger.warning(f"Schema validation failed: {e}")

    return prepared_input


def prepare_merged_input(
    input_data: str | list[str] | dict[str, Any] | BaseModel,
    previous_state: Any | None = None,
    runtime_config: RunnableConfig | None = None,
    input_schema: type[BaseModel] | None = None,
    state_schema: type[BaseModel] | None = None,
) -> Any:
    """Process input data and merge with previous state if available.

    Args:
        input_data: Input data in various formats
        previous_state: Previous state from checkpointer
        runtime_config: Runtime configuration
        input_schema: Schema for input validation
        state_schema: Schema for state validation

    Returns:
        Processed input data merged with previous state
    """
    logger.debug(
        f"Preparing merged input with schemas - Input: {input_schema.__name__ if hasattr(input_schema, '__name__') else type(input_schema)}, State: {state_schema.__name__ if hasattr(state_schema, '__name__') else type(state_schema)}"
    )

    # Process the input based on schema
    processed_input = process_input(input_data, input_schema, runtime_config)

    # Return as is if no previous state
    if not previous_state:
        return processed_input

    # Extract values from StateSnapshot if needed
    previous_values = None

    if hasattr(previous_state, "values"):
        # For StateSnapshot objects
        previous_values = previous_state.values
    elif hasattr(previous_state, "channel_values") and previous_state.channel_values:
        # Alternative attribute name
        previous_values = previous_state.channel_values
    elif isinstance(previous_state, dict):
        # Dictionary state
        previous_values = previous_state

    # Return processed input if no valid previous values
    if not previous_values:
        return processed_input

    # Merge with previous state

    # Special handling for messages to append rather than replace
    if "messages" in processed_input and "messages" in previous_values:
        # Start with all previous messages
        merged_messages = list(previous_values["messages"])

        # Add new messages
        new_messages = processed_input["messages"]
        # Handle both lists of objects and lists of tuples/other formats
        for msg in new_messages:
            merged_messages.append(msg)

        # Update processed input with merged messages
        processed_input["messages"] = merged_messages

        # Log the message count
        logger.debug(f"Merged messages: {len(merged_messages)} total")

    # Merge other fields, starting with previous state
    merged_input = dict(previous_values)

    # Update with new input values
    for key, value in processed_input.items():
        merged_input[key] = value

    # Handle shared fields and reducers if using StateSchema
    if state_schema:
        if hasattr(state_schema, "__shared_fields__"):
            for field in state_schema.__shared_fields__:
                if field in previous_values and field not in processed_input:
                    merged_input[field] = previous_values[field]

        if hasattr(state_schema, "__reducer_fields__"):
            for field, reducer in state_schema.__reducer_fields__.items():
                if field in merged_input and field in previous_values:
                    try:
                        merged_input[field] = reducer(
                            previous_values[field], merged_input[field]
                        )
                    except Exception as e:
                        logger.warning(f"Reducer for {field} failed: {e}")

    # Validate against state schema if available
    if state_schema:
        try:
            validated = state_schema(**merged_input)
            # Return validated instance
            return validated
        except Exception as e:
            logger.warning(f"Schema validation failed when merging: {e}")

    return merged_input
