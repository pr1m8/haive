"""Update function library for NodeSchemaComposer.

This module provides common update patterns identified from node analysis, offering
pluggable update functions for flexible I/O configuration.

Based on analysis of 6 node types, these functions handle the most common state update
patterns found in actual Haive nodes.
"""

from typing import Any

from haive.core.graph.node.composer.path_resolver import PathResolver
from haive.core.graph.node.composer.protocols import UpdateFunction


class UpdateFunctions:
    """Library of common update functions for node I/O composition."""

    def __init__(self) -> None:
        """Initialize with shared PathResolver instance."""
        self._path_resolver = PathResolver()

    def update_simple_field(
        self, field_name: str, merge_mode: str = "replace"
    ) -> UpdateFunction:
        """Create update function for simple field updates.

        Pattern from: ValidationNodeV2, EngineNode simple cases
        Usage: Update single field in state

        Args:
            field_name: Name of field to update
            merge_mode: How to handle updates ("replace", "append", "merge")

        Returns:
            Update function that sets the specified field

        Examples:
            # Replace field value
            update_result = update_simple_field("result")
            updates = update_result("new_value", state, {})

            # Append to list field
            update_messages = update_simple_field("messages", "append")
            updates = update_messages("new message", state, {})
        """

        def _update(result: Any, state: Any, config: dict[str, Any]) -> dict[str, Any]:
            """Update simple field in state."""
            if merge_mode == "append":
                # Append to existing list
                current = self._path_resolver.extract_value(state, field_name, [])
                if not isinstance(current, list):
                    current = [current] if current is not None else []
                updated_value = [*current, result]
            elif merge_mode == "merge" and isinstance(result, dict):
                # Merge dictionaries
                current = self._path_resolver.extract_value(state, field_name, {})
                if not isinstance(current, dict):
                    current = {}
                updated_value = {**current, **result}
            else:
                # Replace (default)
                updated_value = result

            return {field_name: updated_value}

        return _update

    def update_with_path(
        self, target_path: str, merge_mode: str = "replace"
    ) -> UpdateFunction:
        """Create update function for complex path updates.

        Pattern from: AgentNodeV3 hierarchical updates, EngineNode complex cases
        Usage: Update using dot notation, array access, nested paths

        Args:
            target_path: Path string for update target
            merge_mode: How to handle updates ("replace", "append", "merge")

        Returns:
            Update function that updates value at the specified path

        Examples:
            # Update nested config value
            update_temp = update_with_path("config.temperature")
            updates = update_temp(0.8, state, {})

            # Append to nested list
            update_msgs = update_with_path("agents[0].messages", "append")
            updates = update_msgs("new message", state, {})
        """

        def _update(result: Any, state: Any, config: dict[str, Any]) -> dict[str, Any]:
            """Update value using complex path."""
            # For complex paths, we need to build the update structure
            path_parts = target_path.split(".")

            if len(path_parts) == 1 and "[" not in path_parts[0]:
                # Simple field, use simple update
                return self.update_simple_field(target_path, merge_mode)(
                    result, state, config
                )

            # Handle complex nested updates
            updates = {}
            current_dict = updates

            # Build nested dictionary structure
            for _i, part in enumerate(path_parts[:-1]):
                if "[" in part:
                    # Array access - for now, treat as simple key
                    key = part.split("[")[0]
                else:
                    key = part
                current_dict[key] = {}
                current_dict = current_dict[key]

            # Set final value
            final_key = path_parts[-1]
            if merge_mode == "append":
                current = self._path_resolver.extract_value(state, target_path, [])
                if not isinstance(current, list):
                    current = [current] if current is not None else []
                current_dict[final_key] = [*current, result]
            elif merge_mode == "merge" and isinstance(result, dict):
                current = self._path_resolver.extract_value(state, target_path, {})
                if not isinstance(current, dict):
                    current = {}
                current_dict[final_key] = {**current, **result}
            else:
                current_dict[final_key] = result

            return updates

        return _update

    def update_messages_append(
        self, messages_field: str = "messages"
    ) -> UpdateFunction:
        """Create update function for appending to messages.

        Pattern from: Multiple nodes working with MessagesState
        Usage: Append new message to conversation history

        Args:
            messages_field: Name of field containing messages list

        Returns:
            Update function that appends message to list

        Examples:
            # Append AI message to conversation
            update_msgs = update_messages_append()
            updates = update_msgs(ai_message, state, {})
        """

        def _update(result: Any, state: Any, config: dict[str, Any]) -> dict[str, Any]:
            """Append message to messages list."""
            current_messages = self._path_resolver.extract_value(
                state, messages_field, []
            )

            # Ensure we have a list
            if not isinstance(current_messages, list):
                current_messages = []

            # Append new message
            updated_messages = [*list(current_messages), result]

            return {messages_field: updated_messages}

        return _update

    def update_type_aware(self, field_name: str, expected_type: type) -> UpdateFunction:
        """Create update function with type validation.

        Pattern from: ParserNodeV2 safety nets
        Usage: Update field ensuring result matches expected type

        Args:
            field_name: Name of field to update
            expected_type: Expected type of update value

        Returns:
            Update function that validates type before updating

        Examples:
            # Update with int validation
            update_count = update_type_aware("iteration_count", int)
            updates = update_count(5, state, {})
        """

        def _update(result: Any, state: Any, config: dict[str, Any]) -> dict[str, Any]:
            """Update with type validation."""
            # Validate type
            if not isinstance(result, expected_type):
                # Try to convert if possible
                try:
                    if expected_type is int:
                        result = int(result)
                    elif expected_type is float:
                        result = float(result)
                    elif expected_type is str:
                        result = str(result)
                    elif expected_type is bool:
                        result = bool(result)
                    else:
                        # Can't convert, skip update
                        return {}
                except (ValueError, TypeError):
                    # Conversion failed, skip update
                    return {}

            return {field_name: result}

        return _update

    def update_conditional(
        self, condition_path: str, true_field: str, false_field: str
    ) -> UpdateFunction:
        """Create update function with conditional logic.

        Pattern from: EngineNode multi-strategy selection
        Usage: Update different fields based on state condition

        Args:
            condition_path: Path to condition value
            true_field: Field to update if condition is truthy
            false_field: Field to update if condition is falsy

        Returns:
            Update function that conditionally updates fields

        Examples:
            # Update different fields based on mode
            update_output = update_conditional(
                "config.save_history",
                "conversation_history",
                "current_response"
            )
            updates = update_output(result, state, {})
        """

        def _update(result: Any, state: Any, config: dict[str, Any]) -> dict[str, Any]:
            """Update conditionally based on state."""
            condition = self._path_resolver.extract_value(state, condition_path, False)

            if condition:
                return {true_field: result}
            return {false_field: result}

        return _update

    def update_multi_field(self, field_mappings: dict[str, str]) -> UpdateFunction:
        """Create update function for multiple field updates.

        Pattern from: OutputParserNode, AgentNodeV3 complex outputs
        Usage: Update multiple fields from single result

        Args:
            field_mappings: Mapping of result keys to target field names

        Returns:
            Update function that updates multiple fields

        Examples:
            # Split result into multiple fields
            update_multi = update_multi_field({
                "response": "ai_response",
                "confidence": "response_confidence",
                "tokens": "token_usage"
            })

            result = {"response": "Hello", "confidence": 0.9, "tokens": 25}
            updates = update_multi(result, state, {})
        """

        def _update(result: Any, state: Any, config: dict[str, Any]) -> dict[str, Any]:
            """Update multiple fields from result."""
            updates = {}

            if not isinstance(result, dict):
                # If result is not a dict, can't split it
                return {}

            for result_key, target_field in field_mappings.items():
                if result_key in result:
                    updates[target_field] = result[result_key]

            return updates

        return _update

    def update_with_transform(
        self, field_name: str, transform_func: callable
    ) -> UpdateFunction:
        """Create update function with value transformation.

        Pattern from: OutputParserNode value processing
        Usage: Transform result before updating field

        Args:
            field_name: Name of field to update
            transform_func: Function to transform the result

        Returns:
            Update function that transforms then updates

        Examples:
            # Transform to uppercase before updating
            update_upper = update_with_transform("title", str.upper)
            updates = update_upper("hello world", state, {})

            # Parse JSON before updating
            import json
            update_parsed = update_with_transform("data", json.loads)
            updates = update_parsed('{"key": "value"}', state, {})
        """

        def _update(result: Any, state: Any, config: dict[str, Any]) -> dict[str, Any]:
            """Update with transformation."""
            try:
                transformed_result = transform_func(result)
                return {field_name: transformed_result}
            except Exception:
                # Transformation failed, skip update
                return {}

        return _update

    def update_hierarchical(
        self, base_field: str, projection_fields: list[str] | None = None
    ) -> UpdateFunction:
        """Create update function for hierarchical state updates.

        Pattern from: AgentNodeV3 hierarchical projections
        Usage: Update nested objects with field projections

        Args:
            base_field: Base field containing the object to update
            projection_fields: List of fields to include in update (None = all)

        Returns:
            Update function that updates hierarchical structure

        Examples:
            # Update agent with specific fields only
            update_agent = update_hierarchical("current_agent", ["status", "last_action"])
            agent_update = {"status": "active", "last_action": "search", "other": "ignored"}
            updates = update_agent(agent_update, state, {})
        """

        def _update(result: Any, state: Any, config: dict[str, Any]) -> dict[str, Any]:
            """Update hierarchical structure."""
            if not isinstance(result, dict):
                return {base_field: result}

            # Get current value
            current = self._path_resolver.extract_value(state, base_field, {})
            if not isinstance(current, dict):
                current = {}

            # Apply projection if specified
            if projection_fields:
                projected_result = {}
                for field in projection_fields:
                    if field in result:
                        projected_result[field] = result[field]
                result = projected_result

            # Merge with current
            updated = {**current, **result}

            return {base_field: updated}

        return _update


# Create singleton instance for common usage
update_functions = UpdateFunctions()

# Expose common patterns as module-level functions
update_simple_field = update_functions.update_simple_field
update_with_path = update_functions.update_with_path
update_messages_append = update_functions.update_messages_append
update_type_aware = update_functions.update_type_aware
update_conditional = update_functions.update_conditional
update_multi_field = update_functions.update_multi_field
update_with_transform = update_functions.update_with_transform
update_hierarchical = update_functions.update_hierarchical

__all__ = [
    "UpdateFunctions",
    "update_conditional",
    "update_functions",
    "update_hierarchical",
    "update_messages_append",
    "update_multi_field",
    "update_simple_field",
    "update_type_aware",
    "update_with_path",
    "update_with_transform",
]
