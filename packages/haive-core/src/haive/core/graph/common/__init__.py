"""
Common utilities for the graph system.
"""

from haive.core.graph.common.field_utils import (
    extract_base_field,
    extract_field,
    extract_fields_from_function,
    get_field_value,
    get_last_message_content,
)
from haive.core.graph.common.references import CallableReference, TypeReference
from haive.core.graph.common.serialization import (
    ensure_serializable,
    from_json,
    to_json,
)

__all__ = [
    "CallableReference",
    "TypeReference",
    "extract_field",
    "get_field_value",
    "extract_fields_from_function",
    "extract_base_field",
    "get_last_message_content",
    "ensure_serializable",
    "to_json",
    "from_json",
]
