"""Handlers graph module.

This module provides handlers functionality for the Haive framework.

Classes:
    StandardCommandHandler: StandardCommandHandler implementation.
    DirectInputProcessor: DirectInputProcessor implementation.
    MappedInputProcessor: MappedInputProcessor implementation.

Functions:
    process_result: Process Result functionality.
    extract_input: Extract Input functionality.
    extract_input: Extract Input functionality.
"""

# src/haive/core/graph/node/handlers.py

import logging
from typing import Any

from langchain_core.messages import BaseMessage
from langgraph.types import Command, Send
from pydantic import BaseModel

from haive.core.graph.node.registry import (
    register_command_handler,
    register_input_processor,
    register_output_processor,
)

logger = logging.getLogger(__name__)


@register_command_handler("standard")
class StandardCommandHandler:
    """Standard handler for Command/Send pattern."""

    def process_result(
        self, result: Any, config: Any, original_state: dict[str, Any]
    ) -> Any:
        """Process result to handle Command/Send pattern."""
        logger.debug(f"Processing result type: {type(result)}")

        # Handle BaseModel results directly if preserve_model is True
        preserve_model = getattr(config, "preserve_model", True)
        if (
            isinstance(result, BaseModel)
            and preserve_model
            and hasattr(config, "command_goto")
            and config.command_goto is not None
        ):
            logger.debug(
                f"Wrapping preserved BaseModel in Command: {
                    result.__class__.__name__}"
            )
            return Command(update=result, goto=config.command_goto)

        # Already using Command/Send pattern
        if isinstance(result, Command):
            logger.debug(f"Command object detected: {result}")

            # Only modify if it has no goto but config does
            if result.goto is None and config.command_goto is not None:
                logger.debug(
                    f"Modifying Command to add goto: {
                        config.command_goto}"
                )

                # Handle the update attribute carefully
                if hasattr(result, "update") and not callable(result.update):
                    update_data = result.update
                else:
                    logger.warning(
                        "Command.update is callable or missing, creating empty dict"
                    )
                    update_data = {}

                new_command = Command(
                    update=update_data,
                    goto=config.command_goto,
                    resume=result.resume if hasattr(result, "resume") else None,
                    graph=result.graph if hasattr(result, "graph") else None,
                )

                logger.debug(f"Created new Command: {new_command}")
                return new_command
            return result

        if isinstance(result, Send):
            logger.debug(f"Send object detected: {result}")
            return result

        if isinstance(result, list) and all(isinstance(item, Send) for item in result):
            logger.debug(f"List of Send objects detected: {result}")
            return result

        # Not Command/Send - apply command_goto if specified
        if config.command_goto is not None:
            logger.debug(
                f"Creating new Command with goto: {
                    config.command_goto}"
            )

            new_command = Command(update=result, goto=config.command_goto)
            logger.debug(f"Created new Command: {new_command}")

            return new_command

        # Return as-is
        logger.debug(f"Returning result as-is: {result}")
        return result


@register_input_processor("direct")
class DirectInputProcessor:
    """Processor for direct input (no mapping)."""

    def extract_input(self, state: dict[str, Any], config: Any) -> Any:
        """Extract input without mapping."""
        logger.debug(f"Direct input processor for {config.name}")

        # Preserve BaseModel state directly
        if isinstance(state, BaseModel) and getattr(config, "preserve_model", True):
            logger.debug(
                f"Preserving BaseModel state directly: {
                    state.__class__.__name__}"
            )
            return state

        # If using direct messages and they exist, return them
        if (
            config.use_direct_messages
            and isinstance(state, dict)
            and "messages" in state
        ):
            logger.debug(f"Using direct messages: {len(state['messages'])} messages")
            return state["messages"]
        if (
            config.use_direct_messages
            and isinstance(state, BaseModel)
            and hasattr(state, "messages")
        ):
            messages = state.messages
            logger.debug(
                f"Using direct messages from BaseModel: {
                    len(messages) if messages else 0}"
            )
            return messages

        # Otherwise return the full state
        logger.debug(f"Returning full state of type: {type(state).__name__}")
        return state


@register_input_processor("mapped")
class MappedInputProcessor:
    """Processor for mapped input."""

    def extract_input(self, state: dict[str, Any], config: Any) -> Any:
        """Extract input using mapping."""
        logger.debug(f"Mapped input processor for {config.name}")

        # No mapping - fallback to direct
        if not config.input_mapping:
            logger.debug("No input mapping, using full state")
            return state

        # Apply mapping - handle BaseModel state specially
        mapped_input = {}
        if isinstance(state, BaseModel):
            logger.debug(
                f"Mapping from BaseModel state: {
                    state.__class__.__name__}"
            )
            for state_key, input_key in config.input_mapping.items():
                if hasattr(state, state_key):
                    mapped_input[input_key] = getattr(state, state_key)
                    logger.debug(f"Mapped BaseModel attr {state_key} → {input_key}")
        else:
            # Apply mapping for dict state
            for state_key, input_key in config.input_mapping.items():
                if isinstance(state, dict) and state_key in state:
                    mapped_input[input_key] = state[state_key]
                    logger.debug(f"Mapped {state_key} → {input_key}")

        # If only one field was mapped and we have that value, return it
        # directly
        if len(config.input_mapping) == 1 and len(mapped_input) == 1:
            result = next(iter(mapped_input.values()))
            logger.debug(
                f"Returning single mapped value: {
                    type(result).__name__}"
            )
            return result

        logger.debug(
            f"Returning mapped input with keys: {
                list(
                    mapped_input.keys())}"
        )
        return mapped_input


@register_output_processor("standard")
class StandardOutputProcessor:
    """Standard processor for output."""

    def process_output(
        self, result: Any, config: Any, original_state: dict[str, Any]
    ) -> dict[str, Any]:
        """Process standard output."""
        logger.debug(f"Processing output for {config.name}")
        logger.debug(f"Result type: {type(result).__name__}")

        preserve_model = getattr(config, "preserve_model", True)

        # Return BaseModel results directly if preserve_model is True
        if (
            isinstance(result, BaseModel)
            and preserve_model
            and not config.output_mapping
        ):
            logger.debug(
                f"Returning BaseModel directly: {
                    result.__class__.__name__}"
            )
            return result

        # If original state is a BaseModel and we want to preserve, make a copy
        if isinstance(original_state, BaseModel) and preserve_model:
            if hasattr(original_state, "model_copy"):
                # Pydantic v2
                updates = original_state.model_copy(deep=True)
                logger.debug(
                    f"Created deep copy of original BaseModel: {
                        updates.__class__.__name__}"
                )
            else:
                # Pydantic v1
                updates = original_state.copy(deep=True)
                logger.debug(
                    f"Created deep copy of original BaseModel: {
                        updates.__class__.__name__}"
                )

            # Handle string result with output mapping
            if isinstance(result, str) and config.output_mapping:
                logger.debug(
                    f"Processing string result with output mapping: {
                        config.output_mapping}"
                )
                for output_key, state_key in config.output_mapping.items():
                    if output_key == "output":
                        try:
                            setattr(updates, state_key, result)
                            logger.debug(f"Mapped string result to {state_key}")
                            return updates
                        except AttributeError:
                            logger.warning(
                                f"Cannot set attribute {state_key} on BaseModel"
                            )

            # Handle different result types
            if isinstance(result, dict):
                logger.debug(
                    f"Processing dict result with keys: {
                        list(
                            result.keys())}"
                )

                # Apply output mapping if exists
                if config.output_mapping:
                    logger.debug(
                        f"Applying output mapping: {
                            config.output_mapping}"
                    )
                    for output_key, state_key in config.output_mapping.items():
                        if output_key in result:
                            try:
                                setattr(updates, state_key, result[output_key])
                                logger.debug(f"Mapped {output_key} → {state_key}")
                            except AttributeError:
                                logger.warning(
                                    f"Cannot set attribute {state_key} on BaseModel"
                                )
                else:
                    # No mapping - update BaseModel with dict keys
                    for key, value in result.items():
                        try:
                            setattr(updates, key, value)
                            logger.debug(f"Set BaseModel attribute: {key}")
                        except AttributeError:
                            logger.warning(f"Cannot set attribute {key} on BaseModel")
            elif isinstance(result, BaseModel):
                # Try to copy attributes from result to updates
                logger.debug(
                    f"Processing BaseModel result: {result.__class__.__name__}"
                )

                # If it's a message, handle it specially
                if isinstance(result, BaseMessage):
                    if hasattr(updates, "messages"):
                        messages = updates.messages
                        if isinstance(messages, list):
                            messages.append(result)
                            logger.debug("Added message to BaseModel messages list")
                        else:
                            try:
                                updates.messages = [result]
                                logger.debug("Created new messages list on BaseModel")
                            except AttributeError:
                                logger.warning("Cannot set messages on BaseModel")

                    # Also try to set message content
                    if config.extract_content:
                        try:
                            updates.content = result.content
                            logger.debug("Set content from message on BaseModel")
                        except AttributeError:
                            logger.warning("Cannot set content on BaseModel")

                # Apply output mapping if exists
                if config.output_mapping:
                    logger.debug(
                        f"Applying output mapping: {
                            config.output_mapping}"
                    )
                    for output_key, state_key in config.output_mapping.items():
                        if hasattr(result, output_key):
                            try:
                                setattr(updates, state_key, getattr(result, output_key))
                                logger.debug(f"Mapped {output_key} → {state_key}")
                            except AttributeError:
                                logger.warning(
                                    f"Cannot set attribute {state_key} on BaseModel"
                                )
                else:
                    # No mapping - try to set result model as attribute
                    model_name = result.__class__.__name__.lower()

                    # Check if model has the field before trying to set it
                    has_field = False
                    if hasattr(updates, "model_fields"):
                        has_field = model_name in updates.model_fields
                    elif hasattr(updates, "__fields__"):
                        has_field = model_name in updates.__fields__

                    if has_field:
                        try:
                            setattr(updates, model_name, result)
                            logger.debug(f"Set result model as attribute: {model_name}")
                        except AttributeError:
                            logger.warning(f"Cannot set model attribute: {model_name}")
                    else:
                        logger.debug(
                            f"Skipping model attribute {model_name} as field doesn't exist"
                        )

                        # Try to copy all attributes from result to updates
                        if hasattr(result, "model_fields"):
                            # Pydantic v2
                            for key in result.model_fields:
                                if hasattr(result, key):
                                    # Check if target model has this field
                                    has_key = False
                                    if hasattr(updates, "model_fields"):
                                        has_key = key in updates.model_fields
                                    elif hasattr(updates, "__fields__"):
                                        has_key = key in updates.__fields__

                                    if has_key:
                                        try:
                                            value = getattr(result, key)
                                            setattr(updates, key, value)
                                            logger.debug(
                                                f"Copied attribute {key} from result model"
                                            )
                                        except AttributeError:
                                            logger.warning(
                                                f"Cannot set attribute {key} on BaseModel"
                                            )
                        elif hasattr(result, "__fields__"):
                            # Pydantic v1
                            for key in result.__fields__:
                                if hasattr(result, key):
                                    # Check if target model has this field
                                    has_key = False
                                    if hasattr(updates, "model_fields"):
                                        has_key = key in updates.model_fields
                                    elif hasattr(updates, "__fields__"):
                                        has_key = key in updates.__fields__

                                    if has_key:
                                        try:
                                            value = getattr(result, key)
                                            setattr(updates, key, value)
                                            logger.debug(
                                                f"Copied attribute {key} from result model"
                                            )
                                        except AttributeError:
                                            logger.warning(
                                                f"Cannot set attribute {key} on BaseModel"
                                            )
            elif isinstance(result, BaseMessage):
                logger.debug(
                    f"Processing direct BaseMessage: {
                        result.__class__.__name__}"
                )

                # Add to messages list if it exists
                if hasattr(updates, "messages"):
                    messages = updates.messages
                    if isinstance(messages, list):
                        messages.append(result)
                        logger.debug("Added message to BaseModel messages list")
                    else:
                        try:
                            updates.messages = [result]
                            logger.debug("Created new messages list on BaseModel")
                        except AttributeError:
                            logger.warning("Cannot set messages on BaseModel")

                # Also set specific message type attribute if possible
                message_type = result.__class__.__name__.lower()
                try:
                    setattr(updates, message_type, result)
                    logger.debug(f"Set message as {message_type} on BaseModel")
                except AttributeError:
                    logger.warning(f"Cannot set {message_type} on BaseModel")

                # Set content if requested
                if config.extract_content:
                    try:
                        updates.content = result.content
                        logger.debug("Set content from message on BaseModel")
                    except AttributeError:
                        logger.warning("Cannot set content on BaseModel")
            else:
                # String or other result types - try to use output mapping
                if config.output_mapping:
                    logger.debug("Applying output mapping for string/other result")
                    for output_key, state_key in config.output_mapping.items():
                        if output_key == "output":
                            try:
                                setattr(updates, state_key, result)
                                logger.debug(f"Mapped result to {state_key}")
                                break
                            except AttributeError:
                                logger.warning(
                                    f"Cannot set attribute {state_key} on BaseModel"
                                )

                # If mapping didn't work, try common field names
                for field_name in ["output", "result", "content", "response"]:
                    # Check if field exists in the model
                    has_field = False
                    if hasattr(updates, "model_fields"):
                        has_field = field_name in updates.model_fields
                    elif hasattr(updates, "__fields__"):
                        has_field = field_name in updates.__fields__

                    if has_field:
                        try:
                            setattr(updates, field_name, result)
                            logger.debug(f"Set result on {field_name} field")
                            break
                        except AttributeError:
                            logger.warning(f"Cannot set {field_name} on BaseModel")

            # Return the updated model
            return updates

        # Dictionary-based state handling
        updates = {}

        # Start with original state if preserving
        if config.preserve_state and isinstance(original_state, dict):
            logger.debug("Preserving original state")
            updates = original_state.copy()

        # Handle BaseMessage result
        if isinstance(result, BaseMessage):
            logger.debug(
                f"Processing BaseMessage result: {
                    type(result).__name__}"
            )

            # Add message to existing messages if present
            if "messages" in updates and isinstance(updates["messages"], list):
                updates["messages"].append(result)
                logger.debug(
                    f"Added message to existing messages list (now {
                        len(
                            updates['messages'])})"
                )
            else:
                updates["messages"] = [result]
                logger.debug("Created new messages list with message")

            # Save as specific message type (e.g., aimessage for AIMessage)
            message_type = result.__class__.__name__.lower()
            updates[message_type] = result
            logger.debug(f"Added message as {message_type}")

            # Extract content if needed
            if config.extract_content:
                updates["content"] = result.content
                logger.debug("Extracted content from message")

            return updates

        # Handle dictionary result
        if isinstance(result, dict):
            logger.debug(
                f"Processing dict result with keys: {
                    list(
                        result.keys())}"
            )

            # Apply output mapping if exists
            if config.output_mapping:
                logger.debug(
                    f"Applying output mapping: {
                        config.output_mapping}"
                )
                # src/haive/core/graph/node/handlers.py (continued)

                for output_key, state_key in config.output_mapping.items():
                    # Handle nested keys with dot notation
                    if "." in output_key:
                        parts = output_key.split(".")
                        current = result
                        valid_path = True

                        # Navigate through nested structure
                        for part in parts[:-1]:
                            if part in current and isinstance(current, dict):
                                current = current[part]
                            elif hasattr(current, part):
                                current = getattr(current, part)
                            else:
                                valid_path = False
                                break

                        # Set value if path exists
                        if valid_path:
                            last_part = parts[-1]
                            if isinstance(current, dict) and last_part in current:
                                updates[state_key] = current[last_part]
                                logger.debug(
                                    f"Mapped nested {output_key} → {state_key}"
                                )
                            elif hasattr(current, last_part):
                                updates[state_key] = getattr(current, last_part)
                                logger.debug(
                                    f"Mapped nested attr {output_key} → {state_key}"
                                )

                    # Direct key mapping
                    elif output_key in result:
                        updates[state_key] = result[output_key]
                        logger.debug(f"Mapped {output_key} → {state_key}")
                    else:
                        logger.warning(f"Output key '{output_key}' not found in result")
            else:
                # No mapping - update with all result keys
                logger.debug("No mapping, updating with all result keys")
                updates.update(result)

            return updates

        # Handle string result with output mapping
        if isinstance(result, str) and config.output_mapping:
            logger.debug("Processing string result with output mapping")
            for output_key, state_key in config.output_mapping.items():
                if output_key == "output":
                    updates[state_key] = result
                    logger.debug(f"Mapped string result to {state_key}")
                    return updates

        # Fallback - store as a field based on output mapping or common field
        # names
        if config.output_mapping:
            # Try to use the first state_key in output mapping
            state_key = next(iter(config.output_mapping.values()), "output")
            updates[state_key] = result
            logger.debug(f"Using fallback mapping to {state_key}")
            return updates

        # Set output if it exists in state already
        if "output" in updates:
            updates["output"] = result
            logger.debug("Set result to existing 'output' field")
            return updates

        # Last resort fallback
        updates["result"] = result
        logger.debug("Set generic 'result' field as fallback")
        return updates


# This is a targeted fix for the StructuredOutputProcessor in handlers.py


@register_output_processor("structured")
class StructuredOutputProcessor:
    """Processor for structured output models."""

    def process_output(
        self, result: Any, config: Any, original_state: dict[str, Any]
    ) -> Any:
        """Process output from structured output models."""
        logger.debug(f"Processing structured output for {config.name}")
        logger.debug(f"Result type: {type(result).__name__}")

        # Check for preserve_model flag with default to True
        preserve_model = getattr(config, "preserve_model", True)

        # Special handling for string results when output mapping is provided
        if isinstance(result, str) and config.output_mapping:
            logger.debug(
                f"Processing string result with output mapping: {
                    config.output_mapping}"
            )

            # Handle BaseModel original state specially
            if isinstance(original_state, BaseModel) and preserve_model:
                # Make a copy of the original model
                if hasattr(original_state, "model_copy"):
                    updates = original_state.model_copy(deep=True)
                else:
                    updates = original_state.copy(deep=True)

                # Apply output mapping directly for string result
                for output_key, state_key in config.output_mapping.items():
                    # For simple strings, we can assume the "output" key maps
                    # to the string content
                    if output_key == "output":
                        try:
                            setattr(updates, state_key, result)
                            logger.debug(f"Mapped string result to {state_key}")
                        except AttributeError:
                            logger.warning(
                                f"Cannot set attribute {state_key} on BaseModel"
                            )

                return updates

            # For dictionary state
            updates = {}
            # Start with original state if preserving
            if config.preserve_state and isinstance(original_state, dict):
                updates = original_state.copy()

            # Apply output mapping directly for string result
            for output_key, state_key in config.output_mapping.items():
                if output_key == "output":
                    updates[state_key] = result
                    logger.debug(f"Mapped string result to {state_key}")

            return updates

        # Special handling for BaseMessages (like AIMessage)
        if isinstance(result, BaseMessage):
            logger.debug(
                f"Processing BaseMessage (structured): {
                    result.__class__.__name__}"
            )

            # Handle BaseModel original state specially
            if isinstance(original_state, BaseModel) and preserve_model:
                # Make a copy of the original model
                if hasattr(original_state, "model_copy"):
                    updates = original_state.model_copy(deep=True)
                else:
                    updates = original_state.copy(deep=True)

                # Check if there's a messages list to append to
                if hasattr(updates, "messages"):
                    messages = updates.messages
                    if isinstance(messages, list):
                        messages.append(result)
                        logger.debug(
                            "Added message to existing messages list in BaseModel"
                        )
                    else:
                        try:
                            # Try to create a new messages list
                            updates.messages = [result]
                            logger.debug("Created new messages list in BaseModel")
                        except AttributeError:
                            logger.warning("Cannot set messages on BaseModel")

                # Extract content if needed
                if config.extract_content and hasattr(result, "content"):
                    try:
                        updates.content = result.content
                        logger.debug("Extracted content from message to BaseModel")
                    except AttributeError:
                        logger.warning("Cannot set content on BaseModel")

                # Apply output mapping if exists
                if config.output_mapping:
                    logger.debug(
                        f"Applying output mapping: {
                            config.output_mapping}"
                    )
                    for output_key, state_key in config.output_mapping.items():
                        if output_key == "output" and hasattr(result, "content"):
                            try:
                                setattr(updates, state_key, result.content)
                                logger.debug(f"Mapped message content to {state_key}")
                            except AttributeError:
                                logger.warning(
                                    f"Cannot set attribute {state_key} on BaseModel"
                                )

                return updates

            # For dictionary state
            updates = {}

            # Start with original state if preserving
            if config.preserve_state and isinstance(original_state, dict):
                updates = original_state.copy()

            # Add to messages list if it exists
            if "messages" in updates and isinstance(updates["messages"], list):
                updates["messages"].append(result)
                logger.debug("Added message to existing messages list")
            else:
                updates["messages"] = [result]
                logger.debug("Created new messages list")

            # Extract content if needed
            if config.extract_content and hasattr(result, "content"):
                updates["content"] = result.content
                logger.debug("Extracted content from message")

            # Apply output mapping if exists
            if config.output_mapping:
                logger.debug(
                    f"Applying output mapping: {
                        config.output_mapping}"
                )
                for output_key, state_key in config.output_mapping.items():
                    if output_key == "output" and hasattr(result, "content"):
                        updates[state_key] = result.content
                        logger.debug(f"Mapped message content to {state_key}")

            # Save as message type if we know it's safe (i.e., not trying with
            # original BaseModel)
            message_type = result.__class__.__name__.lower()
            updates[message_type] = result
            logger.debug(f"Added message as {message_type}")

            return updates

        # Return BaseModel result directly if configured and no output mapping
        if (
            isinstance(result, BaseModel)
            and preserve_model
            and not config.output_mapping
        ):
            logger.debug(
                f"Returning BaseModel result directly: {
                    result.__class__.__name__}"
            )
            return result

        # Handle BaseModel original state specially
        if isinstance(original_state, BaseModel) and preserve_model:
            # Create a copy of the original model
            if hasattr(original_state, "model_copy"):
                # Pydantic v2
                updates = original_state.model_copy(deep=True)
                logger.debug(
                    f"Created deep copy of original BaseModel: {
                        updates.__class__.__name__}"
                )
            else:
                # Pydantic v1
                updates = original_state.copy(deep=True)
                logger.debug(
                    f"Created deep copy of original BaseModel: {
                        updates.__class__.__name__}"
                )

            # Handle BaseModel result
            if isinstance(result, BaseModel):
                model_name = result.__class__.__name__.lower()
                logger.debug(f"Processing BaseModel result: {model_name}")

                # Check if model has the field before trying to set it
                has_field = False
                if hasattr(updates, "model_fields"):
                    has_field = model_name in updates.model_fields
                elif hasattr(updates, "__fields__"):
                    has_field = model_name in updates.__fields__

                # Try to set the entire model as an attribute ONLY if the field
                # exists
                if has_field:
                    try:
                        setattr(updates, model_name, result)
                        logger.debug(f"Set result model as attribute: {model_name}")
                    except AttributeError:
                        logger.warning(f"Cannot set model attribute: {model_name}")
                else:
                    logger.debug(
                        f"Skipping model attribute {model_name} as field doesn't exist"
                    )

                # Handle specific output mapping
                if config.output_mapping:
                    logger.debug("Applying output mapping to BaseModel result")
                    for output_key, state_key in config.output_mapping.items():
                        if hasattr(result, output_key):
                            try:
                                value = getattr(result, output_key)
                                setattr(updates, state_key, value)
                                logger.debug(f"Mapped {output_key} → {state_key}")
                            except AttributeError:
                                logger.warning(
                                    f"Cannot set attribute {state_key} on BaseModel"
                                )
                # No mapping - copy all attributes if they exist on the target
                # model
                elif hasattr(result, "model_fields"):
                    # Pydantic v2
                    for key in result.model_fields:
                        if hasattr(result, key):
                            # Check if target model has this field
                            has_key = False
                            if hasattr(updates, "model_fields"):
                                has_key = key in updates.model_fields
                            elif hasattr(updates, "__fields__"):
                                has_key = key in updates.__fields__

                            if has_key:
                                try:
                                    value = getattr(result, key)
                                    setattr(updates, key, value)
                                    logger.debug(
                                        f"Copied attribute {key} from result model"
                                    )
                                except AttributeError:
                                    logger.warning(
                                        f"Cannot set attribute {key} on BaseModel"
                                    )
                elif hasattr(result, "__fields__"):
                    # Pydantic v1
                    for key in result.__fields__:
                        if hasattr(result, key):
                            # Check if target model has this field
                            has_key = False
                            if hasattr(updates, "model_fields"):
                                has_key = key in updates.model_fields
                            elif hasattr(updates, "__fields__"):
                                has_key = key in updates.__fields__

                            if has_key:
                                try:
                                    value = getattr(result, key)
                                    setattr(updates, key, value)
                                    logger.debug(
                                        f"Copied attribute {key} from result model"
                                    )
                                except AttributeError:
                                    logger.warning(
                                        f"Cannot set attribute {key} on BaseModel"
                                    )

                return updates

            # Handle other result types with BaseModel original state
            # For string results, map them according to output_mapping
            if isinstance(result, str) and config.output_mapping:
                logger.debug(
                    f"Processing string result with output mapping: {
                        config.output_mapping}"
                )
                for output_key, state_key in config.output_mapping.items():
                    if output_key == "output" and hasattr(updates, state_key):
                        try:
                            setattr(updates, state_key, result)
                            logger.debug(f"Mapped string result to {state_key}")
                            return updates
                        except AttributeError:
                            logger.warning(
                                f"Cannot set attribute {state_key} on BaseModel"
                            )

            # Check if we have a field that matches our expected output field
            if config.output_mapping:
                for output_key, state_key in config.output_mapping.items():
                    # Check if field exists in the model
                    has_field = False
                    if hasattr(updates, "model_fields"):
                        has_field = state_key in updates.model_fields
                    elif hasattr(updates, "__fields__"):
                        has_field = state_key in updates.__fields__

                    if has_field:
                        try:
                            setattr(updates, state_key, result)
                            logger.debug(f"Set generic result on {state_key} field")
                            return updates
                        except AttributeError:
                            logger.warning(f"Cannot set {state_key} on BaseModel")

            # If all else fails, try to use a known field from the schema
            for common_field in ["result", "output", "content", "response"]:
                # Check if field exists in the model
                has_field = False
                if hasattr(updates, "model_fields"):
                    has_field = common_field in updates.model_fields
                elif hasattr(updates, "__fields__"):
                    has_field = common_field in updates.__fields__

                if has_field:
                    try:
                        setattr(updates, common_field, result)
                        logger.debug(f"Set generic result on {common_field} field")
                        return updates
                    except AttributeError:
                        logger.warning(f"Cannot set {common_field} on BaseModel")

            # If we reach here, we couldn't find a suitable field
            logger.warning(
                "Could not find a suitable field for the result in BaseModel"
            )
            return updates

        # Standard dictionary handling for non-BaseModel original state
        updates = {}

        # Start with original state if preserving
        if config.preserve_state:
            logger.debug("Preserving original state")
            updates = original_state.copy() if isinstance(original_state, dict) else {}

        # Handle Pydantic model result
        if isinstance(result, BaseModel):
            # Get model name (lowercase)
            model_name = result.__class__.__name__.lower()
            logger.debug(f"Processing BaseModel: {model_name}")

            # Add the full model to updates
            updates[model_name] = result
            logger.debug(f"Added model as {model_name}")

            # Convert to dict if needed for additional processing
            result_dict = (
                result.model_dump() if hasattr(result, "model_dump") else result.dict()
            )

            # Handle specific case for BaseMessage subtypes
            if isinstance(result, BaseMessage):
                # If we have messages field in state, append the message
                if "messages" in updates and isinstance(updates["messages"], list):
                    updates["messages"].append(result)
                    logger.debug(
                        f"Added message to existing messages list (now {
                            len(
                                updates['messages'])})"
                    )
                else:
                    # Create a new messages list
                    updates["messages"] = [result]
                    logger.debug("Created new messages list with message")

                # Extract content if needed
                if config.extract_content:
                    updates["content"] = result.content
                    logger.debug("Extracted content from message")

            # Extract fields if output mapping exists
            if config.output_mapping:
                logger.debug(
                    f"Applying output mapping: {
                        config.output_mapping}"
                )
                for output_key, state_key in config.output_mapping.items():
                    if hasattr(result, output_key):
                        updates[state_key] = getattr(result, output_key)
                        logger.debug(f"Mapped {output_key} → {state_key}")
            else:
                # No specific mapping, also add all fields
                updates.update(result_dict)
                logger.debug("Added all model fields to updates")

            return updates

        # Handle string results with output mapping
        if isinstance(result, str) and config.output_mapping:
            logger.debug(
                f"Processing string result with output mapping: {
                    config.output_mapping}"
            )
            for output_key, state_key in config.output_mapping.items():
                if output_key == "output":
                    updates[state_key] = result
                    logger.debug(f"Mapped string result to {state_key}")
                    return updates

        # Fallback - here we map to output instead of result if output exists
        # in mapping
        if isinstance(result, str) and config.output_mapping:
            for output_key, state_key in config.output_mapping.items():
                updates[state_key] = result
                logger.debug(f"Used fallback mapping to {state_key}")
                return updates

        # Last resort fallback - try common field names for any result
        for common_field in ["output", "result", "content", "response"]:
            if common_field in updates:
                updates[common_field] = result
                logger.debug(f"Set result to existing field: {common_field}")
                return updates

        # If no mapping or common fields, set generic result field
        updates["result"] = result
        logger.debug("Set generic result field as fallback")
        return updates
