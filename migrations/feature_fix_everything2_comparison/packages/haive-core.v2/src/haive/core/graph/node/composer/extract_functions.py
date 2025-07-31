"""Extract function library for NodeSchemaComposer.

This module provides common extract patterns identified from node analysis, offering
pluggable extract functions for flexible I/O configuration.

Based on analysis of 6 node types, these functions handle the most common extraction
patterns found in actual Haive nodes.
"""

from typing import Any

from haive.core.graph.node.composer.path_resolver import PathResolver
from haive.core.graph.node.composer.protocols import ExtractFunction


class ExtractFunctions:
    """Library of common extract functions for node I/O composition."""

    def __init__(self) -> None:
        """Initialize with shared PathResolver instance."""
        self._path_resolver = PathResolver()

    def extract_simple_field(
        self, field_name: str, default: Any = None
    ) -> ExtractFunction:
        """Create extract function for simple field access.

        Pattern from: ValidationNodeV2, EngineNode simple cases
        Usage: Extract single field from state

        Args:
            field_name: Name of field to extract
            default: Default value if field not found

        Returns:
            Extract function that gets the specified field

        Examples:
            # Extract messages field
            extract_msgs = extract_simple_field("messages")
            messages = extract_msgs(state, {})

            # Extract with default
            extract_temp = extract_simple_field("temperature", 0.7)
            temp = extract_temp(state, {})
        """

        def _extract(state: Any, config: dict[str, Any]) -> Any:
            """Extract simple field from state."""
            return self._path_resolver.extract_value(state, field_name, default)

        return _extract

    def extract_with_path(self, path: str, default: Any = None) -> ExtractFunction:
        """Create extract function for complex path access.

        Pattern from: EngineNode complex cases, AgentNodeV3 projections
        Usage: Extract using dot notation, array access, nested paths

        Args:
            path: Path string (e.g., "messages[-1].content", "config.temperature")
            default: Default value if path not found

        Returns:
            Extract function that gets value at the specified path

        Examples:
            # Extract last message content
            extract_last = extract_with_path("messages[-1].content")
            content = extract_last(state, {})

            # Extract nested config
            extract_temp = extract_with_path("config.llm.temperature", 0.7)
            temp = extract_temp(state, {})
        """

        def _extract(state: Any, config: dict[str, Any]) -> Any:
            """Extract value using complex path."""
            return self._path_resolver.extract_value(state, path, default)

        return _extract

    def extract_with_projection(
        self, field_name: str, projection_fields: list[str]
    ) -> ExtractFunction:
        """Create extract function with field projection.

        Pattern from: AgentNodeV3 hierarchical updates
        Usage: Extract object but only include specified fields

        Args:
            field_name: Name of field containing object to project
            projection_fields: List of fields to include in projection

        Returns:
            Extract function that projects only specified fields

        Examples:
            # Project only name and status from agents
            extract_agents = extract_with_projection("agents", ["name", "status"])
            projected = extract_agents(state, {})
        """

        def _extract(state: Any, config: dict[str, Any]) -> dict[str, Any]:
            """Extract with field projection."""
            obj = self._path_resolver.extract_value(state, field_name, {})

            if not obj or not hasattr(obj, "__getitem__"):
                return {}

            # Project only specified fields
            projected = {}
            for field in projection_fields:
                if hasattr(obj, "get"):
                    # Dictionary-like object
                    projected[field] = obj.get(field)
                else:
                    # Object with attributes
                    projected[field] = getattr(obj, field, None)

            return projected

        return _extract

    def extract_messages_content(
        self, messages_field: str = "messages"
    ) -> ExtractFunction:
        """Create extract function for message content.

        Pattern from: Multiple nodes working with MessagesState
        Usage: Extract content from all messages in conversation

        Args:
            messages_field: Name of field containing messages list

        Returns:
            Extract function that gets content from all messages

        Examples:
            # Extract all message content
            extract_content = extract_messages_content()
            contents = extract_content(messages_state, {})
            # Returns: ["Hello", "Hi there", "How are you?"]
        """

        def _extract(state: Any, config: dict[str, Any]) -> list[str]:
            """Extract content from all messages."""
            messages = self._path_resolver.extract_value(state, messages_field, [])

            if not messages:
                return []

            contents = []
            for msg in messages:
                if hasattr(msg, "content"):
                    contents.append(msg.content)
                elif isinstance(msg, dict) and "content" in msg:
                    contents.append(msg["content"])
                else:
                    # Fallback: convert to string
                    contents.append(str(msg))

            return contents

        return _extract

    def extract_conditional(
        self,
        condition_path: str,
        true_path: str,
        false_path: str,
        true_default: Any = None,
        false_default: Any = None,
    ) -> ExtractFunction:
        """Create extract function with conditional logic.

        Pattern from: EngineNode multi-strategy selection
        Usage: Extract different values based on condition

        Args:
            condition_path: Path to condition value
            true_path: Path to extract if condition is truthy
            false_path: Path to extract if condition is falsy
            true_default: Default for true case
            false_default: Default for false case

        Returns:
            Extract function that conditionally extracts values

        Examples:
            # Use different fields based on mode
            extract_input = extract_conditional(
                "config.use_history",
                "full_conversation",
                "current_message"
            )
            input_data = extract_input(state, {})
        """

        def _extract(state: Any, config: dict[str, Any]) -> Any:
            """Extract conditionally based on state."""
            condition = self._path_resolver.extract_value(state, condition_path, False)

            if condition:
                return self._path_resolver.extract_value(state, true_path, true_default)
            return self._path_resolver.extract_value(state, false_path, false_default)

        return _extract

    def extract_multi_field(
        self, field_paths: dict[str, str], defaults: dict[str, Any] | None = None
    ) -> ExtractFunction:
        """Create extract function for multiple fields.

        Pattern from: OutputParserNode, AgentNodeV3 complex inputs
        Usage: Extract multiple fields into a single dictionary

        Args:
            field_paths: Mapping of output keys to source paths
            defaults: Default values for each output key

        Returns:
            Extract function that extracts multiple fields

        Examples:
            # Extract multiple fields for tool input
            extract_tool_input = extract_multi_field({
                "query": "current_query",
                "context": "messages[-1].content",
                "temperature": "config.temperature"
            }, defaults={"temperature": 0.7})

            tool_input = extract_tool_input(state, {})
            # Returns: {"query": "...", "context": "...", "temperature": 0.7}
        """

        def _extract(state: Any, config: dict[str, Any]) -> dict[str, Any]:
            """Extract multiple fields."""
            result = {}
            default_values = defaults or {}

            for output_key, source_path in field_paths.items():
                default_value = default_values.get(output_key)
                result[output_key] = self._path_resolver.extract_value(
                    state, source_path, default_value
                )

            return result

        return _extract

    def extract_typed(
        self, path: str, expected_type: type, default: Any = None
    ) -> ExtractFunction:
        """Create extract function with type validation.

        Pattern from: ParserNodeV2 safety nets
        Usage: Extract value and ensure it matches expected type

        Args:
            path: Path to extract from
            expected_type: Expected type of extracted value
            default: Default value if extraction fails or type doesn't match

        Returns:
            Extract function that validates type

        Examples:
            # Extract with type validation
            extract_count = extract_typed("iteration_count", int, 0)
            count = extract_count(state, {})  # Always returns int
        """

        def _extract(state: Any, config: dict[str, Any]) -> Any:
            """Extract with type validation."""
            value = self._path_resolver.extract_value(state, path, default)

            # Type validation
            if not isinstance(value, expected_type):
                return default

            return value

        return _extract


# Create singleton instance for common usage
extract_functions = ExtractFunctions()

# Expose common patterns as module-level functions
extract_simple_field = extract_functions.extract_simple_field
extract_with_path = extract_functions.extract_with_path
extract_with_projection = extract_functions.extract_with_projection
extract_messages_content = extract_functions.extract_messages_content
extract_conditional = extract_functions.extract_conditional
extract_multi_field = extract_functions.extract_multi_field
extract_typed = extract_functions.extract_typed

__all__ = [
    "ExtractFunctions",
    "extract_conditional",
    "extract_functions",
    "extract_messages_content",
    "extract_multi_field",
    "extract_simple_field",
    "extract_typed",
    "extract_with_path",
    "extract_with_projection",
]
