"""Processors graph module.

This module provides processors functionality for the Haive framework.

Classes:
    name: name implementation.
    InvokableNodeProcessor: InvokableNodeProcessor implementation.
    AsyncInvokableNodeProcessor: AsyncInvokableNodeProcessor implementation.

Functions:
    process_state: Process State functionality.
    merge_configs: Merge Configs functionality.
    ensure_engine_id_targeting: Ensure Engine Id Targeting functionality.
"""

# src/haive/core/graph/node/processors.py

import asyncio
import inspect
import logging
import traceback
from collections.abc import Callable
from datetime import datetime

# Setup detailed logging
from typing import Any

from langchain_core.messages import BaseMessage
from langgraph.types import Command, Send
from pydantic import BaseModel

from haive.core.config.runnable import RunnableConfigManager
from haive.core.engine.base import EngineType
from haive.core.graph.node.config import NodeConfig
from haive.core.graph.node.registry import register_node_processor

logger = logging.getLogger(__name__)


# Common utility functions used by processors
def process_state(state: Any) -> Any:
    """Process state into a standardized format, preserving BaseModels by default.

    Args:
        state: The state to process

    Returns:
        Processed state (BaseModel preserved, dict copied, other types wrapped)
    """
    logger.debug(f"Processing state of type: {type(state).__name__}")

    # Preserve BaseModel instances directly
    if isinstance(state, BaseModel):
        logger.debug(
            f"Preserving BaseModel instance: {
                state.__class__.__name__}"
        )
        return state

    # Handle different state types
    if isinstance(state, dict):
        return state.copy()  # Make a copy to avoid modifying the original
    if hasattr(state, "__dict__"):  # Object with __dict__
        # Filter out private attributes
        return {k: v for k, v in state.__dict__.items() if not k.startswith("_")}
    # Unknown state type - wrap as value
    logger.debug(
        f"Unknown state type {
            type(state).__name__}, wrapping as 'value'"
    )
    return {"value": state}


def merge_configs(
    base_config: dict[str, Any] | None, override_config: dict[str, Any] | None
) -> dict[str, Any] | None:
    """Merge two configs with smart handling."""
    logger.debug(
        f"Merging configs: base={
            base_config is not None}, override={
            override_config is not None}"
    )

    # Handle None cases
    if base_config is None and override_config is None:
        return None
    if base_config is None:
        return override_config
    if override_config is None:
        return base_config

    # Use RunnableConfigManager for proper merging
    merged = RunnableConfigManager.merge(base_config, override_config)
    logger.debug(
        f"Merged config keys: {
            list(
                merged.keys() if isinstance(
                    merged,
                    dict) else [])}"
    )
    return merged


def ensure_engine_id_targeting(
    config: dict[str, Any], engine_id: str
) -> dict[str, Any]:
    """Ensure config includes targeting for a specific engine ID."""
    logger.debug(f"Ensuring engine ID targeting for: {engine_id}")

    if not config:
        config = {}

    if "configurable" not in config:
        config["configurable"] = {}

    if "engine_configs" not in config["configurable"]:
        config["configurable"]["engine_configs"] = {}

    if engine_id not in config["configurable"]["engine_configs"]:
        config["configurable"]["engine_configs"][engine_id] = {}

    return config


def apply_config_overrides(
    config: dict[str, Any], engine_id: str | None, overrides: dict[str, Any]
) -> dict[str, Any]:
    """Apply node-specific configuration overrides."""
    logger.debug(f"Applying config overrides: {list(overrides.keys())}")

    # Make a copy to avoid modifying the original
    config = config.copy()

    if "configurable" not in config:
        config["configurable"] = {}

    if engine_id:
        # Target engine-specific config
        logger.debug(f"Targeting engine ID: {engine_id}")
        if "engine_configs" not in config["configurable"]:
            config["configurable"]["engine_configs"] = {}

        if engine_id not in config["configurable"]["engine_configs"]:
            config["configurable"]["engine_configs"][engine_id] = {}

        # Apply overrides to this engine's config
        for key, value in overrides.items():
            config["configurable"]["engine_configs"][engine_id][key] = value
    else:
        # Apply to top-level configurable
        logger.debug("Applying overrides to top-level configurable")
        for key, value in overrides.items():
            config["configurable"][key] = value

    return config


def extract_input(state: Any, config: NodeConfig) -> Any:
    """Extract input based on configuration.

    Args:
        state: The current state (can be BaseModel or dict)
        config: Node configuration

    Returns:
        Extracted input data
    """
    logger = logging.getLogger("input_extraction")
    logger.debug(f"Extracting input for node: {config.name}")

    # For BaseModel state, handle specially
    is_base_model = isinstance(state, BaseModel)
    if is_base_model:
        logger.debug(f"Processing BaseModel state: {state.__class__.__name__}")
    else:
        logger.debug(
            f"State keys: {
                list(
                    state.keys()) if isinstance(
                    state,
                    dict) else 'non-dict state'}"
        )

    logger.debug(f"Input mapping: {config.input_mapping}")
    logger.debug(f"Use direct messages: {config.use_direct_messages}")

    # Special handling for retriever nodes
    is_retriever = (
        hasattr(config.engine, "engine_type")
        and getattr(config.engine, "engine_type", None) == EngineType.RETRIEVER
    )
    if is_retriever:
        logger.debug("Detected retriever engine, using specialized extraction")

    # Apply mapping if it exists
    if config.input_mapping:
        logger.debug(f"Applying input mapping: {config.input_mapping}")
        mapped_input = {}

        for state_key, input_key in config.input_mapping.items():
            # Extract from BaseModel if needed
            if is_base_model:
                if hasattr(state, state_key):
                    mapped_input[input_key] = getattr(state, state_key)
                    logger.debug(
                        f"Mapped BaseModel attribute {state_key} → {input_key}"
                    )
                else:
                    logger.warning(f"BaseModel has no attribute '{state_key}'")
            # Extract from dict
            elif isinstance(state, dict) and state_key in state:
                mapped_input[input_key] = state[state_key]
                logger.debug(
                    f"Mapped {state_key} → {input_key}: {
                        type(
                            state[state_key]).__name__}"
                )
            else:
                logger.warning(f"State key '{state_key}' not found in state")

        # For retrievers, if we mapped to a "query" key, simplify to just the
        # query string
        if is_retriever and "query" in mapped_input and len(mapped_input) == 1:
            logger.debug(
                f"Simplified retriever input to just query string: {
                    mapped_input['query']}"
            )
            return mapped_input["query"]

        # Return mapped dict if we have any values
        if mapped_input:
            # If only one mapping exists and one value extracted, return the
            # value directly
            if len(config.input_mapping) == 1 and len(mapped_input) == 1:
                single_value = next(iter(mapped_input.values()))
                logger.debug(
                    f"Returning single mapped value: {
                        type(single_value).__name__}"
                )
                return single_value

            logger.debug(
                f"Returning mapped input with keys: {
                    list(
                        mapped_input.keys())}"
            )
            return mapped_input

        # If mapping exists but resulted in empty dict, log warning
        if not mapped_input:
            logger.warning("Mapping resulted in empty input dictionary")

    # For retrievers with no mapping, get query from state
    if is_retriever:
        # From BaseModel
        if is_base_model and hasattr(state, "query"):
            logger.debug("No mapping for retriever, using direct query from BaseModel")
            return state.query
        # From dict
        if isinstance(state, dict) and "query" in state:
            logger.debug(
                f"No mapping for retriever, using direct query: {
                    state['query']}"
            )
            return state["query"]

    # If using direct messages and they exist
    if config.use_direct_messages:
        # From BaseModel
        if is_base_model and hasattr(state, "messages"):
            messages = state.messages
            logger.debug(
                f"Using direct messages from BaseModel (count: {
                    len(messages) if messages else 0})"
            )
            return messages
        # From dict
        if isinstance(state, dict) and "messages" in state:
            logger.debug(f"Using direct messages (count: {len(state['messages'])})")
            return state["messages"]

    # If we get here with a mapping but no matches, log a clear error
    if config.input_mapping and len(config.input_mapping) > 0:
        msg = f"No input fields could be extracted using mapping: {
                config.input_mapping}"
        logger.error(msg)

        # Check for common errors
        if is_base_model:
            available_attrs = [
                attr
                for attr in dir(state)
                if not attr.startswith("_") and not callable(getattr(state, attr))
            ]
            missing_attrs = [
                k for k in config.input_mapping if k not in available_attrs
            ]
            if missing_attrs:
                logger.error(
                    f"BaseModel is missing these attributes defined in mapping: {missing_attrs}"
                )
                logger.error(
                    f"Available attributes: {
                        available_attrs[
                            :10]}{
                        '...' if len(available_attrs) > 10 else ''}"
                )
        elif isinstance(state, dict):
            missing_keys = [k for k in config.input_mapping if k not in state]
            if missing_keys:
                logger.error(
                    f"State is missing these keys defined in mapping: {missing_keys}"
                )
                logger.error(f"Available state keys: {list(state.keys())}")

    # Default to returning the state as-is (preserving BaseModel if present)
    logger.debug(f"Returning full state: {type(state).__name__}")
    return state


def process_output(result: Any, config: NodeConfig, original_state: Any) -> Any:
    """Process output according to configuration, preserving BaseModels when appropriate.

    Args:
        result: The result from the node function
        config: Node configuration
        original_state: The original state before node execution

    Returns:
        Processed output
    """
    logger = logging.getLogger("output_processing")
    logger.debug(f"Processing output for node: {config.name}")
    logger.debug(f"Result type: {type(result).__name__}")
    logger.debug(f"Output mapping: {config.output_mapping}")
    logger.debug(f"Preserve state: {config.preserve_state}")
    logger.debug(f"Preserve model: {getattr(config, 'preserve_model', True)}")

    # If result is already a BaseModel and we're preserving models, return it directly
    # unless we explicitly have an output mapping or are using a retriever
    # (special handling)
    is_retriever = (
        hasattr(config.engine, "engine_type")
        and getattr(config.engine, "engine_type", None) == EngineType.RETRIEVER
    )

    if (
        isinstance(result, BaseModel)
        and getattr(config, "preserve_model", True)
        and not config.output_mapping
        and not is_retriever
    ):
        logger.debug(
            f"Preserving BaseModel result directly: {
                result.__class__.__name__}"
        )
        return result

    # Special handling for retriever nodes
    if is_retriever:
        logger.debug("Detected retriever engine, using specialized output processing")

    # Get output processor from registry
    registry = config.registry
    if registry:
        # Use structured processor for BaseModel results, otherwise standard
        processor_type = "structured" if isinstance(result, BaseModel) else "standard"
        processor = registry.get_output_processor(processor_type)
        if processor:
            logger.debug(f"Using processor: {processor_type}")
            processed = processor.process_output(result, config, original_state)
            logger.debug(f"Processed output: {type(processed).__name__}")
            return processed

    # Fallback implementation if no processor or registry
    logger.debug("Using fallback implementation")

    # If original state is a BaseModel and we want to preserve it
    is_original_model = isinstance(original_state, BaseModel)
    updates = None

    if is_original_model and getattr(config, "preserve_model", True):
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
    else:
        # Start with empty dict or original state dict if preserving
        updates = {}
        if config.preserve_state and isinstance(original_state, dict):
            updates = original_state.copy()
            logger.debug("Preserving original state dict")

    # Handle retriever returning a list of documents
    if is_retriever and isinstance(result, list):
        logger.debug(
            f"Processing retriever document list (count: {
                len(result)})"
        )

        # Check for Document-like objects
        has_page_content = all(hasattr(item, "page_content") for item in result)
        if has_page_content:
            logger.debug("Detected Document objects in retriever result")

        # Determine output key based on mapping
        output_key = "retrieved_documents"
        if config.output_mapping and "documents" in config.output_mapping:
            output_key = config.output_mapping["documents"]
            logger.debug(f"Using mapped output key: {output_key}")

        # Handle updates for BaseModel vs dict
        if is_original_model and updates is not None:
            # For BaseModel, set attribute directly
            try:
                setattr(updates, output_key, result)
                logger.debug(
                    f"Set BaseModel attribute {output_key} with {
                        len(result)} documents"
                )

                # Preserve query if available
                if hasattr(original_state, "query"):
                    query_val = original_state.query
                    updates.query = query_val
                    logger.debug("Preserved query from original state")

                # Initialize answer field if not present
                if not hasattr(updates, "answer"):
                    updates.answer = ""
                    logger.debug("Initialized empty answer field")
            except AttributeError as e:
                logger.exception(f"Cannot update BaseModel: {e}")
                # Fall back to dictionary if we can't update the model
                updates = {
                    output_key: result,
                    "query": getattr(original_state, "query", ""),
                    "answer": "",
                }
        else:
            # For dict, store the result in the appropriate key
            updates[output_key] = result
            logger.debug(f"Stored {len(result)} documents in '{output_key}'")

            # Preserve query if available
            if isinstance(original_state, dict) and "query" in original_state:
                updates["query"] = original_state["query"]
                logger.debug("Preserved query from original state")

            # Initialize answer field if not present
            if "answer" not in updates:
                updates["answer"] = ""
                logger.debug("Initialized empty answer field")

        return updates

    # Handle different result types
    if isinstance(result, dict):
        logger.debug(f"Result is dictionary with keys: {list(result.keys())}")

        # Apply output mapping if exists
        if config.output_mapping:
            logger.debug("Applying output mapping")

            # Handle BaseModel updates if original state is a model
            if is_original_model and updates is not None:
                for output_key, state_key in config.output_mapping.items():
                    if output_key in result:
                        try:
                            setattr(updates, state_key, result[output_key])
                            logger.debug(
                                f"Mapped {output_key} → {state_key} in BaseModel"
                            )
                        except AttributeError as e:
                            logger.exception(
                                f"Cannot set attribute {state_key} on BaseModel: {e}"
                            )
            else:
                # Regular dictionary mapping
                for output_key, state_key in config.output_mapping.items():
                    if output_key in result:
                        updates[state_key] = result[output_key]
                        logger.debug(f"Mapped {output_key} → {state_key}")
                    else:
                        logger.warning(f"Output key '{output_key}' not found in result")

                        # Special case for retrievers returning a 'documents'
                        # key
                        if (
                            is_retriever
                            and output_key == "documents"
                            and "documents" not in result
                        ):
                            # Check if the result itself is a list of documents
                            if isinstance(result, list) and all(
                                hasattr(doc, "page_content") for doc in result
                            ):
                                updates[state_key] = result
                                logger.debug(
                                    f"Mapped document list directly to {state_key}"
                                )
        elif is_original_model and updates is not None:
            # For BaseModel, try to set each result key as an attribute
            for key, value in result.items():
                try:
                    setattr(updates, key, value)
                    logger.debug(f"Set BaseModel attribute: {key}")
                except AttributeError:
                    logger.warning(f"Could not set attribute '{key}' on BaseModel")
        else:
            # Update dictionary directly
            logger.debug("No mapping - updating with all result keys")
            updates.update(result)

    elif isinstance(result, BaseModel):
        logger.debug(f"Result is BaseModel: {result.__class__.__name__}")

        # Get model as dict
        result_dict = (
            result.model_dump() if hasattr(result, "model_dump") else result.dict()
        )

        logger.debug(f"Model keys: {list(result_dict.keys())}")

        # Get model name for referencing
        model_name = result.__class__.__name__.lower()

        # Handle original state as BaseModel
        if is_original_model and updates is not None:
            # If output mapping exists, apply it
            if config.output_mapping:
                logger.debug("Applying output mapping to BaseModel")
                for output_key, state_key in config.output_mapping.items():
                    if output_key in result_dict:
                        try:
                            setattr(updates, state_key, result_dict[output_key])
                            logger.debug(
                                f"Mapped {output_key} → {state_key} in BaseModel"
                            )
                        except AttributeError as e:
                            logger.exception(
                                f"Cannot set attribute {state_key} on BaseModel: {e}"
                            )
            else:
                # Try to store the model itself as an attribute if possible
                try:
                    setattr(updates, model_name, result)
                    logger.debug(
                        f"Set BaseModel attribute '{model_name}' to result model"
                    )
                except AttributeError:
                    logger.warning(f"Could not set model as attribute '{model_name}'")
                    # Try to set individual attributes instead
                    for key, value in result_dict.items():
                        try:
                            setattr(updates, key, value)
                            logger.debug(f"Set individual attribute: {key}")
                        except AttributeError:
                            logger.warning(
                                f"Could not set attribute '{key}' on BaseModel"
                            )
        elif config.output_mapping:
            logger.debug("Applying output mapping")
            for output_key, state_key in config.output_mapping.items():
                if output_key in result_dict:
                    updates[state_key] = result_dict[output_key]
                    logger.debug(f"Mapped {output_key} → {state_key}")
                else:
                    logger.warning(f"Output key '{output_key}' not found in model")
        else:
            # No mapping - add the model under its class name
            updates[model_name] = result
            logger.debug(f"Added model as {model_name}")

            # Also add individual model fields to the state
            updates.update(result_dict)
            logger.debug("Added all model fields to state")

        # Special handling for BaseMessage subtypes
        if isinstance(result, BaseMessage):
            logger.debug(f"Result is BaseMessage: {result.__class__.__name__}")

            # For BaseModel original state
            if is_original_model and updates is not None:
                if hasattr(updates, "messages") and isinstance(
                    getattr(updates, "messages", None), list
                ):
                    messages = updates.messages
                    messages.append(result)
                    logger.debug(
                        f"Added message to existing messages list (now {
                            len(messages)})"
                    )
                else:
                    try:
                        updates.messages = [result]
                        logger.debug("Created new messages list in BaseModel")
                    except AttributeError:
                        logger.warning("Could not set messages list on BaseModel")

                # Extract content if needed
                if config.extract_content:
                    try:
                        updates.content = result.content
                        logger.debug("Extracted content from message to BaseModel")
                    except AttributeError:
                        logger.warning("Could not set content on BaseModel")
            else:
                # For dictionary state
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

    elif isinstance(result, BaseMessage):
        logger.debug(
            f"Result is BaseMessage directly: {
                result.__class__.__name__}"
        )

        # For BaseModel original state
        if is_original_model and updates is not None:
            if hasattr(updates, "messages") and isinstance(
                getattr(updates, "messages", None), list
            ):
                messages = updates.messages
                messages.append(result)
                logger.debug(
                    f"Added message to existing messages list (now {
                        len(messages)})"
                )
            else:
                try:
                    updates.messages = [result]
                    logger.debug("Created new messages list in BaseModel")
                except AttributeError:
                    logger.warning("Could not set messages list on BaseModel")

            # Extract content if needed
            if config.extract_content:
                try:
                    updates.content = result.content
                    logger.debug("Extracted content from message to BaseModel")
                except AttributeError:
                    logger.warning("Could not set content on BaseModel")
        else:
            # For dictionary state
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

    elif isinstance(result, list):
        # Check if this is a list of Document-like objects
        if result and all(hasattr(item, "page_content") for item in result):
            logger.debug(
                f"Result is a list of Document-like objects (count: {
                    len(result)})"
            )

            # Determine output key based on mapping
            output_key = "retrieved_documents"
            if config.output_mapping and "documents" in config.output_mapping:
                output_key = config.output_mapping["documents"]
                logger.debug(f"Using mapped output key: {output_key}")

            # For BaseModel original state
            if is_original_model and updates is not None:
                try:
                    setattr(updates, output_key, result)
                    logger.debug(f"Set documents in BaseModel attribute: {output_key}")
                except AttributeError:
                    logger.warning(
                        f"Could not set documents on BaseModel attribute: {output_key}"
                    )
            else:
                # For dictionary state
                updates[output_key] = result
                logger.debug(f"Stored document list in '{output_key}'")
        else:
            # Regular list
            logger.debug(f"Result is a regular list (count: {len(result)})")

            # For BaseModel original state
            if is_original_model and updates is not None:
                try:
                    updates.result = result
                    logger.debug("Set list result in BaseModel attribute: result")
                except AttributeError:
                    logger.warning("Could not set list result on BaseModel")
            else:
                # For dictionary state
                updates["result"] = result
                logger.debug("Stored list in 'result'")
    else:
        # Non-dict, non-model, non-list result
        logger.debug(
            f"Result is not dict, model, or list: {
                type(result).__name__}"
        )

        # For BaseModel original state
        if is_original_model and updates is not None:
            try:
                updates.result = result
                logger.debug("Set result in BaseModel attribute: result")
            except AttributeError:
                logger.warning("Could not set result on BaseModel")
        else:
            # For dictionary state
            updates["result"] = result
            logger.debug("Stored as 'result'")

    logger.debug(f"Final result type: {type(updates).__name__}")
    return updates


def handle_command_pattern(result: Any, config: NodeConfig) -> Any:
    """Handle Command/Send pattern for results, preserving BaseModels when appropriate."""
    logger = logging.getLogger("CommandHandler")
    logger.debug(
        f"Handling command pattern for result type: {
            type(result).__name__}"
    )
    preserve_model = getattr(config, "preserve_model", True)

    # Check if result is already a Command or Send
    if isinstance(result, Command):
        logger.debug(f"Result is already a Command: goto={result.goto}")
        # Only override goto if not set but config has one
        if result.goto is None and config.command_goto is not None:
            logger.debug(f"Overriding Command goto: {config.command_goto}")

            # Get update data safely
            if hasattr(result, "update"):
                # Check if update is callable
                if callable(result.update):
                    try:
                        # Call update() to get actual data
                        update_data = result.update()
                        logger.debug(
                            f"Called callable update, got type: {
                                type(update_data).__name__}"
                        )
                    except Exception as e:
                        logger.exception(f"Error calling update(): {e}")
                        update_data = {"error": str(e)}
                else:
                    # Use as attribute
                    update_data = result.update
                    logger.debug(
                        f"Used update attribute, type: {
                            type(update_data).__name__}"
                    )
            else:
                update_data = {}
                logger.debug("No update data found, using empty dict")

            # Create new Command with correct goto
            new_command = Command(
                update=update_data,
                goto=config.command_goto,
                resume=getattr(result, "resume", None),
                graph=getattr(result, "graph", None),
            )
            logger.debug(f"Created new Command: {new_command}")
            return new_command
        return result

    # Handle Send objects
    if isinstance(result, Send):
        logger.debug(f"Result is a Send object: node={result.node}")
        return result
    if isinstance(result, list) and all(isinstance(item, Send) for item in result):
        logger.debug(f"Result is a list of Send objects: count={len(result)}")
        return result

    # Special handling for BaseModel if preserving and command_goto is set
    if (
        isinstance(result, BaseModel)
        and preserve_model
        and config.command_goto is not None
    ):
        logger.debug(
            f"Wrapping preserved BaseModel in Command with goto: {
                config.command_goto}"
        )
        return Command(update=result, goto=config.command_goto)

    # Not Command/Send - apply command_goto if specified
    if config.command_goto is not None:
        logger.debug(f"Creating Command with goto: {config.command_goto}")

        # Return result directly wrapped in Command
        new_command = Command(update=result, goto=config.command_goto)
        logger.debug(f"Created Command: {new_command}")
        return new_command

    # Return as-is
    logger.debug(f"Returning result as-is: {type(result).__name__}")
    return result


def create_error_result(e: Exception, config: NodeConfig) -> Any:
    """Create standardized error result."""
    logger = logging.getLogger("error_handling")
    logger.debug(f"Creating error result for: {type(e).__name__}: {e!s}")

    # Create error data
    error_data = {
        "error": str(e),
        "error_type": type(e).__name__,
        "timestamp": datetime.now().isoformat(),
    }

    # Add traceback if debugging
    if config.debug:
        error_data["traceback"] = traceback.format_exc()
        logger.debug("Added traceback to error data")

    # Apply Command pattern if needed
    if config.command_goto is not None:
        logger.debug(
            f"Creating Command with error and goto: {
                config.command_goto}"
        )
        return Command(update={"error": error_data}, goto=config.command_goto)

    # Return as dict
    logger.debug("Returning error data as dict")
    return {"error": error_data}


# Node processor implementations
@register_node_processor("invokable")
class InvokableNodeProcessor:
    """Processor for invokable engines."""

    def can_process(self, engine: Any) -> bool:
        """Check if this processor can handle the engine."""
        can_invoke = hasattr(engine, "invoke") and callable(engine.invoke)
        logger.debug(f"InvokableNodeProcessor.can_process: {can_invoke}")
        return can_invoke

    def create_node_function(self, engine: Any, config: NodeConfig) -> Callable:
        """Create a node function for an invokable engine."""
        logger.debug(
            f"Creating node function for invokable engine: {
                config.name}"
        )

        def node_function(
            state: dict[str, Any], runtime_config: dict[str, Any] | None = None
        ):
            """Node function for invokable engines."""
            try:
                # Process state - preserving BaseModel if present
                processed_state = process_state(state)

                # Merge configs
                merged_config = merge_configs(config.runnable_config, runtime_config)

                # Apply engine ID targeting
                if engine_id := getattr(engine, "id", None):
                    merged_config = ensure_engine_id_targeting(merged_config, engine_id)

                # Apply config overrides
                if config.config_overrides and merged_config:
                    merged_config = apply_config_overrides(
                        merged_config, engine_id, config.config_overrides
                    )

                # Extract input based on mapping
                input_data = extract_input(processed_state, config)

                # Special handling for LLM engines
                is_llm = (
                    hasattr(engine, "engine_type")
                    and getattr(engine, "engine_type", None) == EngineType.LLM
                )
                if is_llm:
                    logger.debug(
                        "Detected LLM engine, ensuring proper message formatting"
                    )

                    # If input_data is a dict with 'messages' key, extract the
                    # messages
                    if isinstance(input_data, dict) and "messages" in input_data:
                        input_data = input_data["messages"]
                        logger.debug("Extracted messages list from input dict")

                # Invoke engine
                logger.debug(f"Invoking engine: {engine.__class__.__name__}")
                result = engine.invoke(input_data, merged_config)
                logger.debug(
                    f"Engine returned result of type: {
                        type(result).__name__}"
                )

                # Process output
                processed_output = process_output(result, config, processed_state)

                # Handle command pattern
                return handle_command_pattern(processed_output, config)

            except Exception as e:
                logger.exception(
                    f"Error in invokable node {
                        config.name}: {
                        e!s}"
                )
                logger.exception(traceback.format_exc())

                # Create error result
                return create_error_result(e, config)

        return node_function


@register_node_processor("async_invokable")
class AsyncInvokableNodeProcessor:
    """Processor for async invokable engines."""

    def can_process(self, engine: Any) -> bool:
        """Check if this processor can handle the engine."""
        can_ainvoke = hasattr(engine, "ainvoke") and callable(engine.ainvoke)
        logger.debug(f"AsyncInvokableNodeProcessor.can_process: {can_ainvoke}")
        return can_ainvoke

    def create_node_function(self, engine: Any, config: NodeConfig) -> Callable:
        """Create a node function for an async invokable engine."""
        logger.debug(f"Creating async node function for engine: {config.name}")

        def node_function(
            state: dict[str, Any], runtime_config: dict[str, Any] | None = None
        ):
            """Node function that internally handles async execution."""
            logger.debug(f"Called async invokable node: {config.name}")

            try:
                # Process state - preserving BaseModel if present
                processed_state = process_state(state)
                logger.debug(f"Processed state type: {type(processed_state)}")

                # Merge configs
                merged_config = merge_configs(config.runnable_config, runtime_config)

                # Apply engine ID targeting
                if engine_id := getattr(engine, "id", None):
                    merged_config = ensure_engine_id_targeting(merged_config, engine_id)

                # Apply config overrides
                if config.config_overrides and merged_config:
                    merged_config = apply_config_overrides(
                        merged_config, engine_id, config.config_overrides
                    )

                # Extract input based on mapping
                input_data = extract_input(processed_state, config)
                logger.debug(f"Input data type: {type(input_data)}")

                # Special handling for LLM engines
                is_llm = (
                    hasattr(engine, "engine_type")
                    and getattr(engine, "engine_type", None) == EngineType.LLM
                )
                if is_llm:
                    logger.debug(
                        "Detected LLM engine, ensuring proper message formatting"
                    )

                    # If input_data is a dict with 'messages' key, extract the
                    # messages
                    if isinstance(input_data, dict) and "messages" in input_data:
                        input_data = input_data["messages"]
                        logger.debug("Extracted messages list from input dict")

                # Try to use ainvoke, fall back to invoke
                try:
                    if hasattr(engine, "ainvoke") and callable(engine.ainvoke):
                        # For ainvoke, we need to run in an event loop
                        try:
                            loop = asyncio.get_event_loop()
                        except RuntimeError:
                            logger.debug("Creating new event loop")
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)

                        # Run the coroutine
                        logger.debug("Running ainvoke coroutine")
                        result = loop.run_until_complete(
                            engine.ainvoke(input_data, merged_config)
                        )
                    else:
                        # Fall back to synchronous invoke
                        logger.debug("Falling back to synchronous invoke")
                        result = engine.invoke(input_data, merged_config)

                    logger.debug(
                        f"Async engine returned result of type: {
                            type(result).__name__}"
                    )

                    # Process output
                    processed_output = process_output(result, config, processed_state)

                    # Handle command pattern
                    return handle_command_pattern(processed_output, config)

                except Exception as e:
                    logger.exception(f"Error in async invocation: {e!s}")
                    logger.exception(traceback.format_exc())

                    # Try the sync method if ainvoke failed
                    if hasattr(engine, "invoke") and callable(engine.invoke):
                        logger.warning(
                            "Attempting fallback to sync invoke after async error"
                        )
                        result = engine.invoke(input_data, merged_config)

                        # Process output
                        processed_output = process_output(
                            result, config, processed_state
                        )

                        # Handle command pattern
                        return handle_command_pattern(processed_output, config)
                    # Re-raise the original error
                    raise

            except Exception as e:
                logger.exception(
                    f"Error in async invokable node {
                        config.name}: {
                        e!s}"
                )
                logger.exception(traceback.format_exc())

                # Create error result
                return create_error_result(e, config)

        return node_function


@register_node_processor("callable")
class CallableNodeProcessor:
    """Processor for callable functions."""

    def can_process(self, engine: Any) -> bool:
        """Check if this processor can handle the engine."""
        is_callable = callable(engine) and not asyncio.iscoroutinefunction(engine)
        logger.debug(f"CallableNodeProcessor.can_process: {is_callable}")
        return is_callable

    def create_node_function(self, engine: Any, config: NodeConfig) -> Callable:
        """Create a node function from a callable function."""
        logger.debug(f"Creating callable node function: {config.name}")

        def node_function(
            state: dict[str, Any], runtime_config: dict[str, Any] | None = None
        ):
            """Node function for callable."""
            logger.debug(f"Called callable node: {config.name}")

            try:
                # Process state - preserving BaseModel if present
                processed_state = process_state(state)

                # Merge configs
                merged_config = merge_configs(config.runnable_config, runtime_config)

                # Detect function signature
                sig = inspect.signature(engine)
                accepts_config = "config" in sig.parameters
                logger.debug(f"Function accepts config: {accepts_config}")

                # Call function with appropriate arguments
                if accepts_config:
                    logger.debug("Calling with state and config")
                    result = engine(processed_state, merged_config)
                else:
                    logger.debug("Calling with state only")
                    result = engine(processed_state)

                logger.debug(f"Function returned: {type(result).__name__}")

                # For callable functions, we assume they might directly return Command/Send
                # so we don't process the output further unless it's a dict
                if isinstance(result, Command | Send) or (
                    isinstance(result, list)
                    and all(isinstance(x, Send) for x in result)
                ):
                    logger.debug("Returning Command/Send directly")
                    return result

                # Process output for other result types
                processed_output = process_output(result, config, processed_state)

                # Handle command pattern
                return handle_command_pattern(processed_output, config)

            except Exception as e:
                logger.exception(
                    f"Error in callable node {
                        config.name}: {
                        e!s}"
                )
                logger.exception(traceback.format_exc())

                # Create error result
                return create_error_result(e, config)

        return node_function


@register_node_processor("async")
class AsyncNodeProcessor:
    """Processor for async functions."""

    def can_process(self, engine: Any) -> bool:
        """Check if this processor can handle the engine."""
        is_async = asyncio.iscoroutinefunction(engine)
        logger.debug(f"AsyncNodeProcessor.can_process: {is_async}")
        return is_async

    def create_node_function(self, engine: Any, config: NodeConfig) -> Callable:
        """Create a node function for an async function."""
        logger.debug(f"Creating async function node: {config.name}")

        def node_function(
            state: dict[str, Any], runtime_config: dict[str, Any] | None = None
        ):
            """Node function for async callable."""
            logger.debug(f"Called async node: {config.name}")

            try:
                # Process state - preserving BaseModel if present
                processed_state = process_state(state)

                # Merge configs
                merged_config = merge_configs(config.runnable_config, runtime_config)

                # Detect function signature
                sig = inspect.signature(engine)
                accepts_config = "config" in sig.parameters
                logger.debug(f"Async function accepts config: {accepts_config}")

                # Setup asyncio event loop
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    logger.debug("Creating new event loop")
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                # Call function with appropriate arguments and run in event
                # loop
                if accepts_config:
                    logger.debug("Calling async function with state and config")
                    coro = engine(processed_state, merged_config)
                else:
                    logger.debug("Calling async function with state only")
                    coro = engine(processed_state)

                # Run coroutine in event loop
                logger.debug("Running coroutine in event loop")
                result = loop.run_until_complete(coro)
                logger.debug(
                    f"Async function returned: {
                        type(result).__name__}"
                )

                # Handle Command/Send directly
                if isinstance(result, Command | Send) or (
                    isinstance(result, list)
                    and all(isinstance(x, Send) for x in result)
                ):
                    logger.debug("Returning Command/Send from async function directly")
                    return result

                # Process output
                processed_output = process_output(result, config, processed_state)

                # Handle command pattern
                return handle_command_pattern(processed_output, config)

            except Exception as e:
                logger.exception(f"Error in async node {config.name}: {e!s}")
                logger.exception(traceback.format_exc())

                # Create error result
                return create_error_result(e, config)

        return node_function


@register_node_processor("mapping")
class MappingNodeProcessor:
    """Processor for mapping functions that return Send objects."""

    def can_process(self, engine: Any) -> bool:
        """Check if this processor can handle the engine."""
        # Check for functions with Send return annotation or explicit marker
        if callable(engine):
            if hasattr(engine, "__mapping_node__") and engine.__mapping_node__:
                return True

            if hasattr(engine, "__annotations__"):
                if "return" in engine.__annotations__:
                    return_type = str(engine.__annotations__["return"])
                    has_send = (
                        "List[Send]" in return_type or "list[Send]" in return_type
                    )
                    logger.debug(
                        f"MappingNodeProcessor.can_process (annotations): {has_send}"
                    )
                    return has_send
        return False

    def create_node_function(self, engine: Any, config: NodeConfig) -> Callable:
        """Create a node function for a mapping function."""
        logger.debug(f"Creating mapping node function: {config.name}")

        def node_function(
            state: dict[str, Any], runtime_config: dict[str, Any] | None = None
        ):
            """Node function for mapping."""
            logger.debug(f"Called mapping node: {config.name}")

            try:
                # Process state - preserving BaseModel if present
                processed_state = process_state(state)

                # Handle async mapping functions
                if asyncio.iscoroutinefunction(engine):
                    logger.debug("Handling async mapping function")
                    try:
                        loop = asyncio.get_event_loop()
                    except RuntimeError:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)

                    # Run coroutine
                    logger.debug("Running async mapping function in event loop")
                    result = loop.run_until_complete(engine(processed_state))
                else:
                    # For mapping functions, we don't apply normal input/output processing
                    # since they are expected to return Send objects directly
                    logger.debug("Calling sync mapping function")
                    result = engine(processed_state)

                logger.debug(
                    f"Mapping function returned: {
                        type(result).__name__}"
                )

                # Return Send objects as-is
                return result

            except Exception as e:
                logger.exception(f"Error in mapping node {config.name}: {e!s}")
                logger.exception(traceback.format_exc())

                # For mapping nodes, return empty list on error
                logger.debug("Returning empty list due to error")
                return []

        return node_function


@register_node_processor("generic")
class GenericNodeProcessor:
    """Fallback processor for any engine type."""

    def can_process(self, engine: Any) -> bool:
        """This processor can handle any engine."""
        return True

    def create_node_function(self, engine: Any, config: NodeConfig) -> Callable:
        """Create a node function for a generic object."""
        logger.debug(f"Creating generic node function: {config.name}")

        def node_function(
            state: dict[str, Any], runtime_config: dict[str, Any] | None = None
        ):
            """Node function for generic engine."""
            logger.debug(f"Called generic node: {config.name}")

            try:
                # Process state - preserving BaseModel if present
                process_state(state)

                # Return the engine as the result
                result = {"result": engine}
                logger.debug("Created result with engine as 'result' key")

                # Handle command pattern
                return handle_command_pattern(result, config)

            except Exception as e:
                logger.exception(f"Error in generic node {config.name}: {e!s}")
                logger.exception(traceback.format_exc())

                # Create error result
                return create_error_result(e, config)

        return node_function
