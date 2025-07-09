"""
Protocol definitions for extending the schema compatibility system.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Protocol,
    Tuple,
    Type,
    TypeVar,
    runtime_checkable,
)

from pydantic import BaseModel

from haive.core.schema.compatibility.types import (
    CompatibilityLevel,
    ConversionContext,
    ConversionQuality,
    FieldInfo,
    SchemaInfo,
)

T = TypeVar("T")
U = TypeVar("U")


@runtime_checkable
class SchemaConvertible(Protocol):
    """Protocol for objects that can be converted to/from schemas."""

    def to_schema(self) -> Type[BaseModel]:
        """Convert to a Pydantic schema."""
        ...

    @classmethod
    def from_schema(cls: Type[T], schema: Type[BaseModel]) -> T:
        """Create instance from a Pydantic schema."""
        ...


@runtime_checkable
class FieldTransformer(Protocol):
    """Protocol for field transformation functions."""

    def __call__(self, value: Any, context: Optional[Dict[str, Any]] = None) -> Any:
        """Transform a field value."""
        ...


@runtime_checkable
class SchemaValidator(Protocol):
    """Protocol for schema validators."""

    def validate_schema(self, schema: SchemaInfo) -> List[str]:
        """Validate a schema and return list of issues."""
        ...

    def validate_compatibility(
        self,
        source: SchemaInfo,
        target: SchemaInfo,
    ) -> List[str]:
        """Validate compatibility between schemas."""
        ...


@runtime_checkable
class ConversionStrategy(Protocol):
    """Protocol for conversion strategies."""

    @property
    def name(self) -> str:
        """Strategy name."""
        ...

    def can_convert(self, source: Type, target: Type) -> bool:
        """Check if strategy can handle conversion."""
        ...

    def convert(
        self,
        value: Any,
        source_type: Type,
        target_type: Type,
        context: ConversionContext,
    ) -> Any:
        """Perform conversion."""
        ...


@runtime_checkable
class FieldResolver(Protocol):
    """Protocol for resolving field mappings."""

    def resolve_field(
        self,
        source_fields: Dict[str, FieldInfo],
        target_field: FieldInfo,
    ) -> Optional[str]:
        """Resolve source field for a target field."""
        ...

    def suggest_mapping(
        self,
        source_schema: SchemaInfo,
        target_schema: SchemaInfo,
    ) -> Dict[str, str]:
        """Suggest field mappings."""
        ...


@runtime_checkable
class TypeInspector(Protocol):
    """Protocol for custom type inspection."""

    def can_inspect(self, type_hint: Type) -> bool:
        """Check if this inspector can handle the type."""
        ...

    def inspect(self, type_hint: Type) -> Dict[str, Any]:
        """Inspect the type and return metadata."""
        ...

    def extract_constraints(self, type_hint: Type) -> Dict[str, Any]:
        """Extract validation constraints from type."""
        ...


@runtime_checkable
class SchemaEvolution(Protocol):
    """Protocol for schema evolution/migration."""

    @property
    def version(self) -> str:
        """Schema version."""
        ...

    def can_migrate(self, from_version: str, to_version: str) -> bool:
        """Check if migration is possible."""
        ...

    def migrate(
        self,
        data: Dict[str, Any],
        from_version: str,
        to_version: str,
    ) -> Dict[str, Any]:
        """Migrate data between schema versions."""
        ...


@runtime_checkable
class CompatibilityPlugin(Protocol):
    """Protocol for compatibility checker plugins."""

    @property
    def name(self) -> str:
        """Plugin name."""
        ...

    @property
    def priority(self) -> int:
        """Plugin priority (higher = runs first)."""
        ...

    def check_compatibility(
        self,
        source_type: Type,
        target_type: Type,
    ) -> Optional[CompatibilityLevel]:
        """Check compatibility between types."""
        ...

    def enhance_report(
        self,
        report: Any,  # CompatibilityReport
        source: SchemaInfo,
        target: SchemaInfo,
    ) -> None:
        """Enhance compatibility report with additional info."""
        ...


@runtime_checkable
class AsyncConverter(Protocol):
    """Protocol for async converters."""

    async def aconvert(
        self,
        value: Any,
        context: ConversionContext,
    ) -> Any:
        """Async conversion."""
        ...

    @property
    def supports_sync(self) -> bool:
        """Whether sync conversion is also supported."""
        ...


@runtime_checkable
class SchemaRegistry(Protocol):
    """Protocol for schema registries."""

    def register(self, name: str, schema: Type[BaseModel]) -> None:
        """Register a schema."""
        ...

    def get(self, name: str) -> Optional[Type[BaseModel]]:
        """Get a schema by name."""
        ...

    def list_schemas(self) -> List[str]:
        """List all registered schema names."""
        ...

    def find_compatible(
        self,
        target: Type[BaseModel],
        min_score: float = 0.7,
    ) -> List[Tuple[str, float]]:
        """Find compatible schemas with scores."""
        ...


class PluginManager:
    """Manages plugins for the compatibility system."""

    def __init__(self):
        self._plugins: Dict[str, List[Any]] = {
            "converters": [],
            "validators": [],
            "inspectors": [],
            "compatibility": [],
            "resolvers": [],
        }

    def register_converter(self, converter: ConversionStrategy) -> None:
        """Register a conversion strategy."""
        self._plugins["converters"].append(converter)

    def register_validator(self, validator: SchemaValidator) -> None:
        """Register a schema validator."""
        self._plugins["validators"].append(validator)

    def register_inspector(self, inspector: TypeInspector) -> None:
        """Register a type inspector."""
        self._plugins["inspectors"].append(inspector)

    def register_compatibility_plugin(self, plugin: CompatibilityPlugin) -> None:
        """Register a compatibility plugin."""
        self._plugins["compatibility"].append(plugin)
        # Sort by priority
        self._plugins["compatibility"].sort(
            key=lambda p: p.priority,
            reverse=True,
        )

    def register_resolver(self, resolver: FieldResolver) -> None:
        """Register a field resolver."""
        self._plugins["resolvers"].append(resolver)

    def get_converters(self) -> List[ConversionStrategy]:
        """Get all registered converters."""
        return self._plugins["converters"].copy()

    def get_validators(self) -> List[SchemaValidator]:
        """Get all registered validators."""
        return self._plugins["validators"].copy()

    def get_inspectors(self) -> List[TypeInspector]:
        """Get all registered inspectors."""
        return self._plugins["inspectors"].copy()

    def get_compatibility_plugins(self) -> List[CompatibilityPlugin]:
        """Get all registered compatibility plugins."""
        return self._plugins["compatibility"].copy()

    def get_resolvers(self) -> List[FieldResolver]:
        """Get all registered resolvers."""
        return self._plugins["resolvers"].copy()


# Global plugin manager
_plugin_manager = PluginManager()


# Decorator for registering plugins
def converter_plugin(cls):
    """Decorator to register a converter plugin."""
    _plugin_manager.register_converter(cls())
    return cls


def validator_plugin(cls):
    """Decorator to register a validator plugin."""
    _plugin_manager.register_validator(cls())
    return cls


def compatibility_plugin(priority: int = 0):
    """Decorator to register a compatibility plugin."""

    def decorator(cls):
        instance = cls()
        if not hasattr(instance, "priority"):
            instance.priority = priority
        _plugin_manager.register_compatibility_plugin(instance)
        return cls

    return decorator


# Example plugin implementations
class ExampleFieldResolver:
    """Example field resolver using similarity matching."""

    def resolve_field(
        self,
        source_fields: Dict[str, FieldInfo],
        target_field: FieldInfo,
    ) -> Optional[str]:
        """Resolve by name similarity."""
        target_name = target_field.name.lower()

        # Exact match
        if target_field.name in source_fields:
            return target_field.name

        # Case-insensitive match
        for source_name in source_fields:
            if source_name.lower() == target_name:
                return source_name

        # Partial match
        for source_name in source_fields:
            if target_name in source_name.lower() or source_name.lower() in target_name:
                return source_name

        return None

    def suggest_mapping(
        self,
        source_schema: SchemaInfo,
        target_schema: SchemaInfo,
    ) -> Dict[str, str]:
        """Suggest mappings for all fields."""
        suggestions = {}

        for target_name, target_field in target_schema.fields.items():
            source_name = self.resolve_field(source_schema.fields, target_field)
            if source_name:
                suggestions[target_name] = source_name

        return suggestions


class ExampleTypeInspector:
    """Example type inspector for custom types."""

    def can_inspect(self, type_hint: Type) -> bool:
        """Check if type has custom metadata."""
        return hasattr(type_hint, "__metadata__")

    def inspect(self, type_hint: Type) -> Dict[str, Any]:
        """Extract custom metadata."""
        return {
            "has_metadata": True,
            "metadata": getattr(type_hint, "__metadata__", {}),
        }

    def extract_constraints(self, type_hint: Type) -> Dict[str, Any]:
        """Extract validation constraints."""
        metadata = getattr(type_hint, "__metadata__", {})
        constraints = {}

        # Example: extract min/max constraints
        if "min" in metadata:
            constraints["minimum"] = metadata["min"]
        if "max" in metadata:
            constraints["maximum"] = metadata["max"]
        if "pattern" in metadata:
            constraints["pattern"] = metadata["pattern"]

        return constraints
