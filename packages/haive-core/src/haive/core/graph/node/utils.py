# src/haive/core/graph/node/utils.py
"""Utility functions for creating and working with nodes.

This module provides convenience functions for creating different types of nodes
and extracting information from schemas for node integration.
"""

import logging
from typing import Any, Callable, Dict, List, Optional, Type, Union

from langgraph.types import RetryPolicy
from pydantic import BaseModel

from haive.core.graph.node.config import NodeConfig
from haive.core.graph.node.factory import NodeFactory
from haive.core.graph.node.types import CommandGoto, NodeType

logger = logging.getLogger(__name__)


def create_node(
    engine_or_callable: Any,
    name: str | None = None,
    command_goto: CommandGoto | None = None,
    input_mapping: dict[str, str] | None = None,
    output_mapping: dict[str, str] | None = None,
    retry_policy: RetryPolicy | None = None,
    **kwargs,
) -> Callable:
    """Create a node from an engine or callable.

    Args:
        engine_or_callable: Engine, engine name, or callable function
        name: Optional name for the node (defaults to engine name or function name)
        command_goto: Next node to go to after this node
        input_mapping: Mapping from state keys to engine input keys
        output_mapping: Mapping from engine output keys to state keys
        retry_policy: Retry policy for node execution
        **kwargs: Additional options for the node configuration

    Returns:
        Node function that can be added to a graph
    """
    # Get node name if not provided
    if name is None:
        name = getattr(engine_or_callable, "name", None)
        if name is None and callable(engine_or_callable):
            name = getattr(engine_or_callable, "__name__", None)

    # Create node config
    config = NodeConfig(
        name=name or "unnamed_node",
        engine=engine_or_callable if not isinstance(engine_or_callable, str) else None,
        engine_name=engine_or_callable if isinstance(engine_or_callable, str) else None,
        callable_func=(
            engine_or_callable
            if callable(engine_or_callable)
            and not hasattr(engine_or_callable, "engine_type")
            else None
        ),
        command_goto=command_goto,
        input_fields=input_mapping,
        output_fields=output_mapping,
        retry_policy=retry_policy,
        **kwargs,
    )

    # Create node function
    return NodeFactory.create_node_function(config)


def create_validation_node(
    schemas: list[type[BaseModel] | Callable],
    name: str | None = None,
    command_goto: CommandGoto | None = None,
    messages_field: str = "messages",
    **kwargs,
) -> Callable:
    """Create a validation node.

    Args:
        schemas: List of validation schemas or functions
        name: Optional name for the node
        command_goto: Next node to go to after this node
        messages_field: Name of the messages key in the state
        **kwargs: Additional options for the node configuration

    Returns:
        Validation node function
    """
    return create_node(
        engine_or_callable=None,
        name=name or "validation_node",
        node_type=NodeType.VALIDATION,
        command_goto=command_goto,
        input_mapping=(
            {"messages": messages_field} if messages_field != "messages" else None
        ),
        validation_schemas=schemas,
        messages_field=messages_field,
        **kwargs,
    )


def create_branch_node(
    condition: Callable,
    routes: dict[Any, str],
    name: str | None = None,
    input_mapping: dict[str, str] | None = None,
    **kwargs,
) -> Callable:
    """Create a branch node.

    Args:
        condition: Function that evaluates the state and returns a key for routing
        routes: Mapping from condition outputs to node names
        name: Optional name for the node
        input_mapping: Mapping from state keys to condition function input keys
        **kwargs: Additional options for the node configuration

    Returns:
        Branch node function
    """
    return create_node(
        engine_or_callable=None,
        name=name or "branch_node",
        node_type=NodeType.BRANCH,
        input_fields=input_mapping,
        condition=condition,
        routes=routes,
        **kwargs,
    )


def create_send_node(
    send_targets: list[str],
    send_field: str | None = None,
    name: str | None = None,
    input_mapping: dict[str, str] | None = None,
    distribution: str = "round_robin",
    payload_extractor: Callable | None = None,
    send_all_to_each: bool = False,
    **kwargs,
) -> Callable:
    """Create a send node for fan-out operations.

    Args:
        send_targets: List of target node names to send items to
        send_field: Key in the state containing items to distribute (not required if using payload_extractor)
        name: Optional name for the node
        input_mapping: Mapping from state keys to node input keys
        distribution: Strategy for distributing items ("round_robin", "all", "balanced")
        payload_extractor: Optional function to extract payloads from state (overrides send_field)
        send_all_to_each: If True, sends all items to each target (instead of distributing)
        **kwargs: Additional options for the node configuration

    Returns:
        Send node function
    """
    if not send_targets:
        raise ValueError("Must provide at least one send target")

    if not send_field and not payload_extractor:
        raise ValueError("Must provide either send_field or payload_extractor")

    # Create node config with all parameters
    return create_node(
        engine_or_callable=None,
        name=name or "send_node",
        node_type=NodeType.SEND,
        input_fields=input_mapping,
        send_targets=send_targets,
        send_field=send_field,
        distribution=distribution,
        payload_extractor=payload_extractor,
        send_all_to_each=send_all_to_each,
        **kwargs,
    )


def extract_io_mapping_from_schema(
    schema: type, engine_id: str
) -> dict[str, dict[str, str]]:
    """Extract input and output mappings from a schema for a specific engine.

    Args:
        schema: StateSchema class
        engine_id: ID or name of the engine to extract mappings for

    Returns:
        Dictionary with "inputs" and "outputs" mappings
    """
    result = {"inputs": {}, "outputs": {}}

    # Check if schema has engine I/O mappings
    if not hasattr(schema, "__engine_io_mappings__"):
        logger.warning(
            f"Schema {schema.__name__} has no __engine_io_mappings__ attribute"
        )
        return result

    mappings = schema.__engine_io_mappings__

    # Handle various engine ID formats (full ID, short ID, name)
    matched_key = None
    if engine_id in mappings:
        matched_key = engine_id
    else:
        # Try partial matches
        for key in mappings:
            if isinstance(key, str) and (
                key == engine_id or engine_id.endswith(key) or key.endswith(engine_id)
            ):
                matched_key = key
                break

    if not matched_key:
        # Check model fields directly for metadata matching this engine
        model_fields = getattr(schema, "model_fields", {})
        for field_name, field_info in model_fields.items():
            metadata = getattr(field_info, "metadata", [])

            # Check metadata for source or input_for/output_from entries
            for meta in metadata:
                if isinstance(meta, dict):
                    # Check if field is input for this engine
                    if "input_for" in meta and engine_id in meta["input_for"]:
                        result["inputs"][field_name] = field_name

                    # Check if field is output from this engine
                    if "output_from" in meta and engine_id in meta["output_from"]:
                        result["outputs"][field_name] = field_name

        return result

    engine_mappings = mappings[matched_key]

    # Create identity mappings (field_name -> field_name)
    if "inputs" in engine_mappings:
        for field in engine_mappings["inputs"]:
            result["inputs"][field] = field

    if "outputs" in engine_mappings:
        for field in engine_mappings["outputs"]:
            result["outputs"][field] = field

    return result
