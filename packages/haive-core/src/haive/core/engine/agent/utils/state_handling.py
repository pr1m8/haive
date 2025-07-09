# src/haive.core/engine/agent/utils/state_handling.py

"""
State handling utilities for agent inputs and outputs.

This module provides functions for processing and transforming state data
during agent execution, focusing on output extraction and state validation.
"""

import logging
from typing import Any, Dict, List, Optional, Union

from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel

logger = logging.getLogger(__name__)


def extract_output(output_data: Any, output_schema=None) -> Dict[str, Any]:
    """
    Extract and validate output from agent result.

    Args:
        output_data: Agent output data
        output_schema: Optional schema for validation

    Returns:
        Processed output data
    """
    # Handle different output types
    if isinstance(output_data, dict):
        processed_output = output_data
    elif hasattr(output_data, "model_dump"):
        # Pydantic v2
        processed_output = output_data.model_dump()
    elif hasattr(output_data, "dict"):
        # Pydantic v1
        processed_output = output_data.dict()
    else:
        # Convert to dict as best we can
        processed_output = {"output": str(output_data)}

    # Validate against output schema if available
    if output_schema:
        try:
            validated = output_schema(**processed_output)
            if hasattr(validated, "model_dump"):
                return validated.model_dump()
            elif hasattr(validated, "dict"):
                return validated.dict()
            return validated
        except Exception as e:
            logger.warning(f"Output schema validation failed: {e}")

    return processed_output


def extract_state_snapshot(snapshot: Any) -> Dict[str, Any]:
    """
    Extract state values from a state snapshot.

    Args:
        snapshot: State snapshot from checkpointer

    Returns:
        Dictionary of state values
    """
    if snapshot is None:
        return {}

    # Extract values based on object type
    if hasattr(snapshot, "values"):
        # Standard StateSnapshot
        return snapshot.values if hasattr(snapshot.values, "items") else {}
    elif hasattr(snapshot, "channel_values") and snapshot.channel_values:
        # Alternative attribute name in some versions
        return (
            snapshot.channel_values if hasattr(snapshot.channel_values, "items") else {}
        )
    elif isinstance(snapshot, dict):
        # Dictionary state
        return snapshot

    # Fallback - try to convert to dict
    try:
        if hasattr(snapshot, "model_dump"):
            # Pydantic v2
            return snapshot.model_dump()
        elif hasattr(snapshot, "dict"):
            # Pydantic v1
            return snapshot.dict()
    except Exception:
        pass

    # Last resort - empty dict
    logger.warning(f"Couldn't extract state from snapshot of type {type(snapshot)}")
    return {}


def prepare_merged_input(
    input_data: Any,
    previous_state: Optional[Any] = None,
    runtime_config: Optional[Dict[str, Any]] = None,
    input_schema=None,
    state_schema=None,
) -> Any:
    """
    Process input data and merge with previous state if available.

    Args:
        input_data: Input data in various formats
        previous_state: Previous state from checkpointer
        runtime_config: Runtime configuration
        input_schema: Schema for input validation
        state_schema: Schema for state validation

    Returns:
        Processed input data merged with previous state
    """
    # Process the input based on schema
    processed_input = process_input(input_data, input_schema)

    # Return as is if no previous state
    if not previous_state:
        return processed_input

    # Extract values from previous state
    previous_values = extract_state_snapshot(previous_state)

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
        merged_messages.extend(new_messages)

        # Update processed input with merged messages
        processed_input["messages"] = merged_messages

        # Log the message count
        logger.debug(f"Merged messages: {len(merged_messages)} total")

    # Merge other fields, keeping processed_input as priority
    merged_input = dict(previous_values)

    # Update with new input values
    for key, value in processed_input.items():
        merged_input[key] = value

    # Handle shared fields and reducers if using StateSchema
    if state_schema and hasattr(state_schema, "__shared_fields__"):
        for field in state_schema.__shared_fields__:
            if field in previous_values and field not in processed_input:
                merged_input[field] = previous_values[field]

    if state_schema and hasattr(state_schema, "__reducer_fields__"):
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
            return state_schema(**merged_input)
        except Exception as e:
            logger.warning(f"Schema validation failed: {e}")

    return merged_input


def process_input(
    input_data: Union[str, List[str], Dict[str, Any], BaseModel], input_schema=None
) -> Dict[str, Any]:
    """
    Process input for the agent based on the input schema.

    Args:
        input_data: Input in various formats
        input_schema: Schema for validation

    Returns:
        Processed input compatible with the graph
    """
    # Extract schema field information if available
    schema_fields = {}
    if input_schema and hasattr(input_schema, "model_fields"):
        schema_fields = input_schema.model_fields
    elif input_schema and hasattr(input_schema, "__fields__"):
        schema_fields = input_schema.__fields__

    # Handle string input
    if isinstance(input_data, str):
        # Initialize with messages
        from langchain_core.messages import HumanMessage

        prepared_input = {"messages": [HumanMessage(content=input_data)]}

        # Add to other input fields based on schema
        for field_name, field_info in schema_fields.items():
            if field_name != "messages" and field_name != "__runnable_config__":
                # Only add to text fields
                field_type = getattr(field_info, "annotation", None) or getattr(
                    field_info, "type_", None
                )
                type_name = str(field_type)
                if "str" in type_name or "String" in type_name:
                    prepared_input[field_name] = input_data

        # Validate against schema if available
        if input_schema:
            try:
                validated = input_schema(**prepared_input)
                return (
                    validated.model_dump()
                    if hasattr(validated, "model_dump")
                    else validated.dict()
                )
            except Exception as e:
                logger.warning(f"Schema validation failed: {e}")

        return prepared_input

    # Handle list of strings
    elif isinstance(input_data, list) and all(
        isinstance(item, str) for item in input_data
    ):
        # Create messages list
        from langchain_core.messages import HumanMessage

        messages = [HumanMessage(content=item) for item in input_data]
        prepared_input = {"messages": messages}

        # Join strings for other text fields
        joined_text = "\n".join(input_data)
        for field_name, field_info in schema_fields.items():
            if field_name != "messages" and field_name != "__runnable_config__":
                # Only add to text fields
                field_type = getattr(field_info, "annotation", None) or getattr(
                    field_info, "type_", None
                )
                type_name = str(field_type)
                if "str" in type_name or "String" in type_name:
                    prepared_input[field_name] = joined_text

        # Validate against schema
        if input_schema:
            try:
                validated = input_schema(**prepared_input)
                return (
                    validated.model_dump()
                    if hasattr(validated, "model_dump")
                    else validated.dict()
                )
            except Exception as e:
                logger.warning(f"Schema validation failed: {e}")

        return prepared_input

    # Handle dictionary input
    elif isinstance(input_data, dict):
        # Create a copy to avoid modifying the original
        input_dict = input_data.copy()

        # Ensure there's a messages field if not present and required
        if "messages" not in input_dict and "messages" in schema_fields:
            # Try to create messages from other fields
            from langchain_core.messages import HumanMessage

            for field in ["input", "query", "content", "text"]:
                if field in input_dict and isinstance(input_dict[field], str):
                    input_dict["messages"] = [HumanMessage(content=input_dict[field])]
                    break

        # Validate against schema if available
        if input_schema:
            try:
                validated = input_schema(**input_dict)
                return (
                    validated.model_dump()
                    if hasattr(validated, "model_dump")
                    else validated.dict()
                )
            except Exception as e:
                logger.warning(f"Schema validation failed: {e}")

        return input_dict

    # Handle Pydantic model input
    elif isinstance(input_data, BaseModel):
        # Convert to dict
        if hasattr(input_data, "model_dump"):
            # Pydantic v2
            model_dict = input_data.model_dump()
        elif hasattr(input_data, "dict"):
            # Pydantic v1
            model_dict = input_data.dict()
        else:
            # Manual extraction
            model_dict = {}
            for field in input_data.__annotations__:
                if hasattr(input_data, field):
                    model_dict[field] = getattr(input_data, field)

        # Ensure there's a messages field if needed by schema
        if "messages" not in model_dict and "messages" in schema_fields:
            # Try to create messages from other fields
            from langchain_core.messages import HumanMessage

            for field in ["input", "query", "content", "text"]:
                if field in model_dict and isinstance(model_dict[field], str):
                    model_dict["messages"] = [HumanMessage(content=model_dict[field])]
                    break

        # Validate against schema if available
        if input_schema:
            try:
                validated = input_schema(**model_dict)
                return (
                    validated.model_dump()
                    if hasattr(validated, "model_dump")
                    else validated.dict()
                )
            except Exception as e:
                logger.warning(f"Schema validation failed: {e}")

        return model_dict

    # Fallback for other types - convert to string message
    from langchain_core.messages import HumanMessage

    fallback_input = {"messages": [HumanMessage(content=str(input_data))]}

    # Validate against schema if available
    if input_schema:
        try:
            validated = input_schema(**fallback_input)
            return (
                validated.model_dump()
                if hasattr(validated, "model_dump")
                else validated.dict()
            )
        except Exception as e:
            logger.warning(f"Schema validation failed: {e}")

    return fallback_input


def save_state_history(
    app: Any, state_filename: str, runnable_config: RunnableConfig
) -> bool:
    """
    Save the current agent state to a JSON file.

    Args:
        app: Compiled agent application
        state_filename: Path to save state history
        runnable_config: Runnable configuration

    Returns:
        True if successful, False otherwise
    """
    import json

    if not app:
        logger.error("Cannot save state history: No application provided")
        return False

    try:
        # Get state from app
        state_json = app.get_state(runnable_config)

        if not state_json:
            logger.warning("No state history available")
            return False

        # Ensure state is JSON serializable
        from haive.core.utils.pydantic_utils import ensure_json_serializable

        state_json = ensure_json_serializable(state_json)

        # Save to file
        with open(state_filename, "w", encoding="utf-8") as f:
            json.dump(state_json, f, indent=4)

        logger.info(f"State history saved to: {state_filename}")
        return True
    except Exception as e:
        logger.error(f"Error saving state history: {str(e)}")
        return False
