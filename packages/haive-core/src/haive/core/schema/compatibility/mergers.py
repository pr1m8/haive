"""
Schema merging strategies for combining multiple schemas.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union

from pydantic import BaseModel, Field, create_model

from haive.core.schema.compatibility.analyzer import TypeAnalyzer
from haive.core.schema.compatibility.compatibility import CompatibilityChecker
from haive.core.schema.compatibility.types import (
    CompatibilityLevel,
    FieldInfo,
    MergeStrategy,
    SchemaInfo,
)


class ConflictResolution(str, Enum):
    """How to resolve field conflicts during merge."""

    FIRST_WINS = "first_wins"
    LAST_WINS = "last_wins"
    TYPE_UNION = "type_union"
    MOST_SPECIFIC = "most_specific"
    MOST_GENERAL = "most_general"
    CUSTOM = "custom"


class MergeContext:
    """Context for merge operations."""

    def __init__(self):
        self.conflicts: List[Dict[str, Any]] = []
        self.warnings: List[str] = []
        self.field_sources: Dict[str, List[str]] = {}  # field -> [schema_names]
        self.resolution_log: List[str] = []

    def add_conflict(
        self,
        field_name: str,
        schemas: List[str],
        reason: str,
        resolution: str,
    ) -> None:
        """Log a conflict."""
        self.conflicts.append(
            {
                "field": field_name,
                "schemas": schemas,
                "reason": reason,
                "resolution": resolution,
            }
        )
        self.resolution_log.append(
            f"Conflict in '{field_name}': {reason}. Resolution: {resolution}"
        )

    def add_warning(self, warning: str) -> None:
        """Add a warning."""
        self.warnings.append(warning)

    def track_field_source(self, field_name: str, schema_name: str) -> None:
        """Track which schema a field came from."""
        if field_name not in self.field_sources:
            self.field_sources[field_name] = []
        self.field_sources[field_name].append(schema_name)


class MergeStrategy(ABC):
    """Abstract base for merge strategies."""

    @abstractmethod
    def merge_fields(
        self,
        field_infos: List[Tuple[str, FieldInfo]],  # (schema_name, field_info)
        context: MergeContext,
    ) -> Optional[FieldInfo]:
        """Merge multiple field definitions."""
        pass

    @abstractmethod
    def should_include_field(
        self,
        field_name: str,
        schemas_with_field: List[str],
        total_schemas: int,
    ) -> bool:
        """Determine if field should be included in merged schema."""
        pass


class UnionMergeStrategy(MergeStrategy):
    """Include all fields from all schemas."""

    def __init__(
        self, conflict_resolution: ConflictResolution = ConflictResolution.LAST_WINS
    ):
        self.conflict_resolution = conflict_resolution

    def should_include_field(
        self,
        field_name: str,
        schemas_with_field: List[str],
        total_schemas: int,
    ) -> bool:
        """Include all fields."""
        return True

    def merge_fields(
        self,
        field_infos: List[Tuple[str, FieldInfo]],
        context: MergeContext,
    ) -> Optional[FieldInfo]:
        """Merge field definitions."""
        if not field_infos:
            return None

        if len(field_infos) == 1:
            return field_infos[0][1]

        # Check for conflicts
        field_name = field_infos[0][1].name
        types = [(name, info.type_info.type_hint) for name, info in field_infos]
        unique_types = list(set(t[1] for t in types))

        if len(unique_types) > 1:
            # Type conflict
            context.add_conflict(
                field_name,
                [name for name, _ in field_infos],
                f"Different types: {unique_types}",
                self.conflict_resolution.value,
            )

            if self.conflict_resolution == ConflictResolution.FIRST_WINS:
                return field_infos[0][1]
            elif self.conflict_resolution == ConflictResolution.LAST_WINS:
                return field_infos[-1][1]
            elif self.conflict_resolution == ConflictResolution.TYPE_UNION:
                # Create union type
                from typing import Union

                union_type = Union[tuple(unique_types)]
                merged = field_infos[-1][1]
                merged.type_info.type_hint = union_type
                return merged

        # Merge other properties
        # Use the most restrictive settings
        is_required = any(info.is_required for _, info in field_infos)
        has_default = all(info.has_default for _, info in field_infos)

        # Take the last definition as base
        merged = field_infos[-1][1]
        merged.is_required = is_required

        # Merge metadata
        merged.is_shared = any(info.is_shared for _, info in field_infos)

        # Combine engine mappings
        for _, info in field_infos:
            merged.input_for_engines.update(info.input_for_engines)
            merged.output_from_engines.update(info.output_from_engines)

        return merged


class IntersectionMergeStrategy(MergeStrategy):
    """Include only fields present in all schemas."""

    def should_include_field(
        self,
        field_name: str,
        schemas_with_field: List[str],
        total_schemas: int,
    ) -> bool:
        """Include only if in all schemas."""
        return len(schemas_with_field) == total_schemas

    def merge_fields(
        self,
        field_infos: List[Tuple[str, FieldInfo]],
        context: MergeContext,
    ) -> Optional[FieldInfo]:
        """Merge field definitions."""
        if not field_infos:
            return None

        # For intersection, ensure types are compatible
        analyzer = TypeAnalyzer()
        base_type = field_infos[0][1].type_info.type_hint

        for schema_name, field_info in field_infos[1:]:
            if not analyzer.is_subtype(field_info.type_info.type_hint, base_type):
                context.add_warning(
                    f"Type incompatibility in intersection for '{field_info.name}'"
                )
                # Use most general type
                base_type = Any

        # Use first definition as base
        merged = field_infos[0][1]
        merged.type_info.type_hint = base_type

        # Use most permissive settings
        merged.is_required = all(info.is_required for _, info in field_infos)
        merged.is_shared = all(info.is_shared for _, info in field_infos)

        return merged


class SchemaMerger:
    """Main schema merging engine."""

    def __init__(
        self,
        strategy: Union[MergeStrategy, str] = "union",
        analyzer: Optional[TypeAnalyzer] = None,
        compatibility_checker: Optional[CompatibilityChecker] = None,
    ):
        self.analyzer = analyzer or TypeAnalyzer()
        self.compatibility_checker = compatibility_checker or CompatibilityChecker()

        # Set strategy
        if isinstance(strategy, str):
            if strategy == "union":
                self.strategy = UnionMergeStrategy()
            elif strategy == "intersection":
                self.strategy = IntersectionMergeStrategy()
            else:
                raise ValueError(f"Unknown strategy: {strategy}")
        else:
            self.strategy = strategy

    def merge_schemas(
        self,
        schemas: List[Union[Type[BaseModel], SchemaInfo]],
        name: Optional[str] = None,
        base_class: Optional[Type[BaseModel]] = None,
    ) -> Type[BaseModel]:
        """
        Merge multiple schemas into one.

        Args:
            schemas: List of schemas to merge
            name: Name for the merged schema
            base_class: Base class for the merged schema

        Returns:
            Merged schema class
        """
        if not schemas:
            raise ValueError("No schemas to merge")

        # Convert all to SchemaInfo
        schema_infos = []
        for i, schema in enumerate(schemas):
            if isinstance(schema, type) and issubclass(schema, BaseModel):
                info = self.analyzer.analyze_schema(schema)
                info.name = schema.__name__
            else:
                info = schema
            schema_infos.append(info)

        # Merge
        context = MergeContext()
        merged_info = self._merge_schema_infos(schema_infos, context)

        # Generate name
        if not name:
            name = f"Merged{''.join(s.name for s in schema_infos[:3])}"
            if len(schema_infos) > 3:
                name += f"And{len(schema_infos) - 3}More"

        # Create model
        return self._create_model_from_info(merged_info, name, base_class)

    def _merge_schema_infos(
        self,
        schema_infos: List[SchemaInfo],
        context: MergeContext,
    ) -> SchemaInfo:
        """Merge SchemaInfo objects."""
        # Group fields by name
        field_groups: Dict[str, List[Tuple[str, FieldInfo]]] = {}

        for schema_info in schema_infos:
            for field_name, field_info in schema_info.fields.items():
                if field_name not in field_groups:
                    field_groups[field_name] = []
                field_groups[field_name].append((schema_info.name, field_info))
                context.track_field_source(field_name, schema_info.name)

        # Create merged schema info
        merged = SchemaInfo(
            name="MergedSchema",
            type_info=schema_infos[0].type_info,  # Use first as template
        )

        # Merge fields
        total_schemas = len(schema_infos)

        for field_name, field_list in field_groups.items():
            schemas_with_field = [name for name, _ in field_list]

            if self.strategy.should_include_field(
                field_name, schemas_with_field, total_schemas
            ):
                merged_field = self.strategy.merge_fields(field_list, context)
                if merged_field:
                    merged.fields[field_name] = merged_field

        # Merge metadata
        for schema_info in schema_infos:
            merged.shared_fields.update(schema_info.shared_fields)

            # Merge reducers with conflict detection
            for field, reducer in schema_info.reducer_fields.items():
                if (
                    field in merged.reducer_fields
                    and merged.reducer_fields[field] != reducer
                ):
                    context.add_conflict(
                        field,
                        [schema_info.name],
                        "Different reducers",
                        "Keeping existing",
                    )
                else:
                    merged.reducer_fields[field] = reducer

            # Merge engine mappings
            for engine, mapping in schema_info.engine_io_mappings.items():
                if engine not in merged.engine_io_mappings:
                    merged.engine_io_mappings[engine] = {"inputs": [], "outputs": []}

                merged.engine_io_mappings[engine]["inputs"].extend(
                    mapping.get("inputs", [])
                )
                merged.engine_io_mappings[engine]["outputs"].extend(
                    mapping.get("outputs", [])
                )

        # Deduplicate engine mappings
        for engine, mapping in merged.engine_io_mappings.items():
            mapping["inputs"] = list(set(mapping["inputs"]))
            mapping["outputs"] = list(set(mapping["outputs"]))

        return merged

    def _create_model_from_info(
        self,
        schema_info: SchemaInfo,
        name: str,
        base_class: Optional[Type[BaseModel]] = None,
    ) -> Type[BaseModel]:
        """Create a Pydantic model from SchemaInfo."""
        # Build field definitions
        field_definitions = {}

        for field_name, field_info in schema_info.fields.items():
            # Create field kwargs
            field_kwargs = {}

            if not field_info.is_required:
                if field_info.default_factory:
                    field_kwargs["default_factory"] = field_info.default_factory
                elif field_info.default_value is not None:
                    field_kwargs["default"] = field_info.default_value
                else:
                    field_kwargs["default"] = None

            if field_info.description:
                field_kwargs["description"] = field_info.description

            if field_info.alias:
                field_kwargs["alias"] = field_info.alias

            # Create field
            field_definitions[field_name] = (
                field_info.type_info.type_hint,
                Field(**field_kwargs) if field_kwargs else ...,
            )

        # Choose base class
        if base_class is None:
            # Try to detect appropriate base class
            if "messages" in schema_info.fields:
                try:
                    from haive.core.schema.prebuilt.messages_state import MessagesState

                    base_class = MessagesState
                except ImportError:
                    base_class = BaseModel
            else:
                base_class = BaseModel

        # Create model
        model = create_model(
            name,
            __base__=base_class,
            **field_definitions,
        )

        # Add metadata as class attributes
        if schema_info.shared_fields:
            model.__shared_fields__ = list(schema_info.shared_fields)

        if schema_info.reducer_fields:
            model.__reducer_fields__ = dict(schema_info.reducer_fields)

        if schema_info.engine_io_mappings:
            model.__engine_io_mappings__ = dict(schema_info.engine_io_mappings)

        return model


# Convenience functions
def merge_schemas(
    schemas: List[Union[Type[BaseModel], SchemaInfo]],
    strategy: str = "union",
    name: Optional[str] = None,
) -> Type[BaseModel]:
    """Merge multiple schemas using specified strategy."""
    merger = SchemaMerger(strategy=strategy)
    return merger.merge_schemas(schemas, name=name)


def create_union_schema(
    *schemas: Union[Type[BaseModel], SchemaInfo],
    name: Optional[str] = None,
) -> Type[BaseModel]:
    """Create a union of multiple schemas."""
    return merge_schemas(list(schemas), strategy="union", name=name)


def create_intersection_schema(
    *schemas: Union[Type[BaseModel], SchemaInfo],
    name: Optional[str] = None,
) -> Type[BaseModel]:
    """Create an intersection of multiple schemas."""
    return merge_schemas(list(schemas), strategy="intersection", name=name)
