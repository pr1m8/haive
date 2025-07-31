"""Path resolver for extracting values from objects using path notation.

This module provides path-based value extraction from objects, supporting simple field
access initially, with progressive enhancement for complex paths.
"""

from typing import Any


class PathResolver:
    """Resolver for extracting values from objects using path notation.

    This class handles path-based extraction from objects, supporting:

    Phase 1: Simple field access (e.g., "messages", "temperature")
    Phase 2: Dot notation (e.g., "config.temperature")
    Phase 2: Array access (e.g., "messages[0]", "messages[-1]")
    Phase 3: Advanced patterns (wildcards, method calls, etc.)
    """

    def extract_value(self, obj: Any, path: str, default: Any = None) -> Any:
        """Extract value from object using path notation.

        Args:
            obj: Object to extract from (dict, Pydantic model, etc.)
            path: Path string (e.g., "messages", "config.temp", "messages[0]")
            default: Default value if path not found or None

        Returns:
            Extracted value or default

        Examples:
            # Simple field access (Phase 1)
            resolver = PathResolver()
            state = {"messages": ["hello"], "temp": 0.7}

            value = resolver.extract_value(state, "messages")
            # Returns: ["hello"]

            # Dot notation (Phase 2)
            value = resolver.extract_value(state, "config.temperature")
            # Returns: 0.7

            # Array access (Phase 2)
            value = resolver.extract_value(state, "messages[0]")
            # Returns: "hello"
        """
        if not obj or not path:
            return default

        # Phase 2: Check if this is a complex path
        if "." in path or "[" in path:
            return self._extract_complex_path(obj, path, default)

        # Phase 1: Simple field access (preserved for compatibility)
        return self._extract_simple_field(obj, path, default)

    def _extract_simple_field(
        self, obj: Any, field_name: str, default: Any = None
    ) -> Any:
        """Extract a simple field from an object (Phase 1 logic)."""
        try:
            # Try dict-like access first for dictionaries to avoid conflicts
            # with built-in methods like 'items', 'keys', 'values'
            if hasattr(obj, "__getitem__") and hasattr(obj, "get"):
                # This is likely a dictionary
                try:
                    return obj.get(field_name, default)
                except (KeyError, RuntimeError):
                    return default

            # Try other dict-like access (lists, tuples, etc.)
            if hasattr(obj, "__getitem__"):
                try:
                    return obj[field_name]
                except (KeyError, IndexError, RuntimeError):
                    pass  # Continue to attribute access

            # Try object attribute access for non-dict objects
            try:
                if hasattr(obj, field_name):
                    # Object attribute access (Pydantic models, dataclasses)
                    return getattr(obj, field_name, default)
            except (AttributeError, RuntimeError):
                # hasattr or getattr failed
                pass

            return default

        except (KeyError, AttributeError, TypeError, RuntimeError):
            return default

    def _extract_complex_path(self, obj: Any, path: str, default: Any = None) -> Any:
        """Extract value using complex path notation (Phase 2)."""
        try:
            current = obj

            # Split path into segments, handling both dots and brackets
            segments = self._parse_path_segments(path)

            for segment in segments:
                if segment.endswith("]") and "[" in segment:
                    # Array access: "messages[0]" or "items[-1]"
                    current = self._extract_array_access(current, segment, default)
                else:
                    # Simple field access
                    current = self._extract_simple_field(current, segment, default)

                # If we got the default value, the path failed
                if current is default:
                    return default

            return current

        except (KeyError, AttributeError, TypeError, IndexError, ValueError):
            return default

    def _parse_path_segments(self, path: str) -> list[str]:
        """Parse a complex path into segments.

        Examples:
            "config.temperature" → ["config", "temperature"]
            "messages[0].content" → ["messages[0]", "content"]
            "data.items[-1].value" → ["data", "items[-1]", "value"]
            "matrix[0][1].field" → ["matrix[0]", "[1]", "field"]
        """
        segments = []
        current_segment = ""
        bracket_depth = 0

        i = 0
        while i < len(path):
            char = path[i]

            if char == "." and bracket_depth == 0:
                if current_segment:
                    segments.append(current_segment)
                    current_segment = ""
            elif char == "[":
                if bracket_depth > 0:
                    # This is a nested bracket like [1] in matrix[0][1]
                    # Split here - finish current segment and start new one
                    if current_segment:
                        segments.append(current_segment)
                    current_segment = "["
                    bracket_depth = 1
                else:
                    # First bracket - start building array access
                    current_segment += char
                    bracket_depth += 1
            elif char == "]":
                bracket_depth -= 1
                current_segment += char

                # If we just closed all brackets and there's more content,
                # this segment is complete
                if bracket_depth == 0 and i + 1 < len(path) and path[i + 1] == "[":
                    segments.append(current_segment)
                    current_segment = ""
            else:
                current_segment += char

            i += 1

        if current_segment:
            segments.append(current_segment)

        return segments

    def _extract_array_access(self, obj: Any, segment: str, default: Any = None) -> Any:
        """Extract value using array access notation.

        Examples:
            "messages[0]" → first item
            "items[-1]" → last item
            "data[1]" → second item
            "[1]" → direct array access on obj
        """
        try:
            # Check if this is a direct array access like "[1]"
            if segment.startswith("[") and segment.endswith("]"):
                # Direct array access on the current object
                index_str = segment[1:-1]  # Remove [ and ]
                try:
                    index = int(index_str)
                    if hasattr(obj, "__getitem__"):
                        return obj[index]
                    return default
                except (ValueError, IndexError, TypeError):
                    return default

            # Parse field name and index for "field[index]" format
            bracket_pos = segment.find("[")
            if bracket_pos == -1:
                return default

            field_name = segment[:bracket_pos]
            index_str = segment[bracket_pos + 1 : -1]  # Remove [ and ]

            # Get the array/list
            array = self._extract_simple_field(obj, field_name, None)
            if array is None or not hasattr(array, "__getitem__"):
                return default

            # Parse and apply index
            try:
                index = int(index_str)
                return array[index]
            except (ValueError, IndexError, TypeError):
                return default

        except (AttributeError, KeyError, TypeError):
            return default
