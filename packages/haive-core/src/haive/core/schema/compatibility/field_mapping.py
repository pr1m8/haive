"""
Advanced field mapping with path resolution and transformations.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

from haive.core.schema.compatibility.types import ConversionContext, FieldInfo


@dataclass
class FieldMapping:
    """Represents a mapping between fields with transformation."""

    source_path: str  # Can be nested: "user.profile.name"
    target_field: str
    transformer: Optional[Callable[[Any], Any]] = None
    condition: Optional[Callable[[Dict[str, Any]], bool]] = None
    default_value: Any = None
    default_factory: Optional[Callable[[], Any]] = None
    validator: Optional[Callable[[Any], bool]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Path patterns
    is_computed: bool = False  # No source, generated value
    is_aggregate: bool = False  # Multiple sources to one target
    aggregator: Optional[Callable[[List[Any]], Any]] = None

    def apply(self, source_data: Dict[str, Any]) -> Tuple[bool, Any]:
        """
        Apply mapping to source data.

        Returns:
            Tuple of (success, value)
        """
        # Check condition first
        if self.condition and not self.condition(source_data):
            return False, None

        # Handle computed fields
        if self.is_computed:
            if self.default_factory:
                value = self.default_factory()
            else:
                value = self.default_value

        # Handle aggregate fields
        elif self.is_aggregate and self.aggregator:
            # Source path contains multiple paths separated by |
            paths = self.source_path.split("|")
            values = []
            for path in paths:
                path_value = self._extract_path_value(source_data, path.strip())
                if path_value is not None:
                    values.append(path_value)

            if not values and self.default_value is not None:
                value = self.default_value
            else:
                value = self.aggregator(values)

        # Normal field extraction
        else:
            value = self._extract_path_value(source_data, self.source_path)

            # Use default if not found
            if value is None:
                if self.default_factory:
                    value = self.default_factory()
                elif self.default_value is not None:
                    value = self.default_value
                else:
                    return False, None

        # Apply transformer
        if self.transformer and value is not None:
            try:
                value = self.transformer(value)
            except Exception as e:
                return False, f"Transform error: {e}"

        # Validate
        if self.validator and not self.validator(value):
            return False, f"Validation failed for {self.target_field}"

        return True, value

    def _extract_path_value(self, data: Dict[str, Any], path: str) -> Any:
        """Extract value from nested path."""
        # Handle array notation: messages[0].content
        array_pattern = re.compile(r"(\w+)\[(\d+)\]")

        # Handle filter notation: messages[?type=="human"].content
        filter_pattern = re.compile(r'(\w+)\[\?(\w+)==["\']([^"\']+)["\']\]')

        current = data
        parts = path.split(".")

        for i, part in enumerate(parts):
            if current is None:
                return None

            # Check for array access
            array_match = array_pattern.match(part)
            if array_match:
                field_name = array_match.group(1)
                index = int(array_match.group(2))

                if isinstance(current, dict) and field_name in current:
                    array = current[field_name]
                    if isinstance(array, list) and 0 <= index < len(array):
                        current = array[index]
                    else:
                        return None
                else:
                    return None
                continue

            # Check for filter
            filter_match = filter_pattern.match(part)
            if filter_match:
                field_name = filter_match.group(1)
                filter_field = filter_match.group(2)
                filter_value = filter_match.group(3)

                if isinstance(current, dict) and field_name in current:
                    array = current[field_name]
                    if isinstance(array, list):
                        filtered = [
                            item
                            for item in array
                            if isinstance(item, dict)
                            and item.get(filter_field) == filter_value
                        ]
                        current = filtered[0] if filtered else None
                    else:
                        return None
                else:
                    return None
                continue

            # Normal field access
            if isinstance(current, dict):
                current = current.get(part)
            elif hasattr(current, part):
                current = getattr(current, part)
            else:
                return None

        return current


class FieldMapper:
    """Manages field mappings between schemas."""

    def __init__(self):
        self.mappings: Dict[str, FieldMapping] = {}
        self._source_index: Dict[str, Set[str]] = {}  # source -> targets

    def add_mapping(
        self,
        source: Union[str, List[str]],
        target: str,
        transformer: Optional[Callable[[Any], Any]] = None,
        condition: Optional[Callable[[Dict[str, Any]], bool]] = None,
        default: Any = None,
        validator: Optional[Callable[[Any], bool]] = None,
    ) -> FieldMapping:
        """Add a field mapping."""
        # Handle multiple sources (aggregate)
        if isinstance(source, list):
            source_path = " | ".join(source)
            is_aggregate = True
        else:
            source_path = source
            is_aggregate = False

        mapping = FieldMapping(
            source_path=source_path,
            target_field=target,
            transformer=transformer,
            condition=condition,
            default_value=default,
            validator=validator,
            is_aggregate=is_aggregate,
        )

        self.mappings[target] = mapping

        # Update index
        if isinstance(source, list):
            for s in source:
                if s not in self._source_index:
                    self._source_index[s] = set()
                self._source_index[s].add(target)
        else:
            if source not in self._source_index:
                self._source_index[source] = set()
            self._source_index[source].add(target)

        return mapping

    def add_computed_field(
        self,
        target: str,
        generator: Callable[[], Any],
        condition: Optional[Callable[[Dict[str, Any]], bool]] = None,
    ) -> FieldMapping:
        """Add a computed field with no source."""
        mapping = FieldMapping(
            source_path="",
            target_field=target,
            default_factory=generator,
            condition=condition,
            is_computed=True,
        )

        self.mappings[target] = mapping
        return mapping

    def add_aggregate_field(
        self,
        sources: List[str],
        target: str,
        aggregator: Callable[[List[Any]], Any],
        default: Any = None,
    ) -> FieldMapping:
        """Add an aggregate field from multiple sources."""
        mapping = FieldMapping(
            source_path=" | ".join(sources),
            target_field=target,
            is_aggregate=True,
            aggregator=aggregator,
            default_value=default,
        )

        self.mappings[target] = mapping

        # Update index
        for source in sources:
            if source not in self._source_index:
                self._source_index[source] = set()
            self._source_index[source].add(target)

        return mapping

    def map_data(
        self,
        source_data: Dict[str, Any],
        target_fields: Optional[Set[str]] = None,
        include_unmapped: bool = False,
        context: Optional[ConversionContext] = None,
    ) -> Dict[str, Any]:
        """
        Map source data to target schema.

        Args:
            source_data: Source data dictionary
            target_fields: Specific fields to map (None = all)
            include_unmapped: Include unmapped source fields
            context: Conversion context for tracking

        Returns:
            Mapped data dictionary
        """
        result = {}
        mapped_sources = set()

        # Apply mappings
        for target_field, mapping in self.mappings.items():
            if target_fields and target_field not in target_fields:
                continue

            success, value = mapping.apply(source_data)

            if success:
                result[target_field] = value
                # Track mapped source fields
                if not mapping.is_computed:
                    if mapping.is_aggregate:
                        sources = mapping.source_path.split("|")
                        mapped_sources.update(s.strip() for s in sources)
                    else:
                        mapped_sources.add(mapping.source_path)
            elif context:
                context.add_warning(f"Failed to map field '{target_field}': {value}")

        # Include unmapped fields if requested
        if include_unmapped:
            for key, value in source_data.items():
                if key not in mapped_sources and key not in result:
                    result[key] = value

        return result

    def get_mapping_for_target(self, target_field: str) -> Optional[FieldMapping]:
        """Get mapping for a target field."""
        return self.mappings.get(target_field)

    def get_targets_for_source(self, source_field: str) -> Set[str]:
        """Get all target fields that use a source field."""
        return self._source_index.get(source_field, set())

    def validate_mappings(
        self,
        source_fields: Set[str],
        target_fields: Set[str],
    ) -> Tuple[bool, List[str]]:
        """
        Validate that mappings are complete and valid.

        Returns:
            Tuple of (is_valid, issues)
        """
        issues = []

        # Check all required target fields have mappings
        for target in target_fields:
            if target not in self.mappings:
                issues.append(f"No mapping for required field '{target}'")

        # Check all source references exist
        for mapping in self.mappings.values():
            if not mapping.is_computed:
                if mapping.is_aggregate:
                    sources = [s.strip() for s in mapping.source_path.split("|")]
                else:
                    sources = [mapping.source_path]

                for source in sources:
                    # Extract base field (before any dots or brackets)
                    base_field = source.split(".")[0].split("[")[0]
                    if base_field not in source_fields:
                        issues.append(
                            f"Mapping references non-existent source '{base_field}'"
                        )

        return len(issues) == 0, issues

    def to_dict(self) -> Dict[str, Dict[str, Any]]:
        """Export mappings as dictionary."""
        return {
            target: {
                "source": mapping.source_path,
                "is_computed": mapping.is_computed,
                "is_aggregate": mapping.is_aggregate,
                "has_transformer": mapping.transformer is not None,
                "has_condition": mapping.condition is not None,
                "has_default": mapping.default_value is not None,
            }
            for target, mapping in self.mappings.items()
        }


# Convenience function
def create_mapping(
    mappings: Dict[str, Union[str, Tuple[str, Callable]]],
    computed_fields: Optional[Dict[str, Callable]] = None,
) -> FieldMapper:
    """
    Create a field mapper from simple mapping dict.

    Args:
        mappings: Dict of target -> source or (source, transformer)
        computed_fields: Dict of target -> generator function
    """
    mapper = FieldMapper()

    # Add simple mappings
    for target, source_spec in mappings.items():
        if isinstance(source_spec, tuple):
            source, transformer = source_spec
            mapper.add_mapping(source, target, transformer=transformer)
        else:
            mapper.add_mapping(source_spec, target)

    # Add computed fields
    if computed_fields:
        for target, generator in computed_fields.items():
            mapper.add_computed_field(target, generator)

    return mapper
