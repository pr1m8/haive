"""
Advanced type analysis engine for deep type introspection.
"""

from __future__ import annotations

import inspect
import sys
from functools import lru_cache
from typing import (
    Any,
    Dict,
    ForwardRef,
    List,
    Optional,
    Protocol,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    _GenericAlias,
    get_args,
    get_origin,
    get_type_hints,
)

from pydantic import BaseModel
from pydantic.fields import FieldInfo as PydanticFieldInfo

from haive.core.schema.compatibility.types import FieldInfo, SchemaInfo, TypeInfo

# Handle different Python versions
if sys.version_info >= (3, 10):
    from types import UnionType
else:
    UnionType = type(None)


class TypeAnalyzer:
    """Advanced type analysis with caching and deep introspection."""

    def __init__(self, cache_size: int = 1000):
        """Initialize analyzer with cache."""
        self._cache_size = cache_size
        self._clear_cache()

    def _clear_cache(self):
        """Clear all caches."""
        # Create cached versions of methods
        self.analyze_type = lru_cache(maxsize=self._cache_size)(self._analyze_type_impl)
        self.get_type_info = lru_cache(maxsize=self._cache_size)(
            self._get_type_info_impl
        )

    def analyze_schema(self, schema_type: Type[BaseModel]) -> SchemaInfo:
        """Analyze a Pydantic BaseModel schema."""
        if not inspect.isclass(schema_type) or not issubclass(schema_type, BaseModel):
            raise ValueError(f"{schema_type} is not a BaseModel subclass")

        # Get type info
        type_info = self.get_type_info(schema_type)

        # Create schema info
        schema_info = SchemaInfo(
            name=schema_type.__name__,
            type_info=type_info,
            base_classes=list(schema_type.__bases__),
        )

        # Analyze fields
        for field_name, field_info in schema_type.model_fields.items():
            schema_info.fields[field_name] = self._analyze_field(field_name, field_info)

        # Extract Haive-specific metadata
        if hasattr(schema_type, "__shared_fields__"):
            schema_info.shared_fields = set(schema_type.__shared_fields__)

        if hasattr(schema_type, "__reducer_fields__"):
            schema_info.reducer_fields = dict(schema_type.__reducer_fields__)

        if hasattr(schema_type, "__engine_io_mappings__"):
            schema_info.engine_io_mappings = dict(schema_type.__engine_io_mappings__)

        # Extract methods
        for name, method in inspect.getmembers(schema_type, inspect.ismethod):
            if not name.startswith("_"):
                schema_info.methods[name] = method

        return schema_info

    def _analyze_field(self, name: str, pydantic_field: PydanticFieldInfo) -> FieldInfo:
        """Analyze a single field."""
        # Get type information
        type_info = self.get_type_info(pydantic_field.annotation)

        # Determine if required
        is_required = pydantic_field.is_required()

        # Extract default information
        has_default = not is_required
        default_value = None
        default_factory = None

        if hasattr(pydantic_field, "default") and pydantic_field.default is not ...:
            has_default = True
            default_value = pydantic_field.default
        elif (
            hasattr(pydantic_field, "default_factory")
            and pydantic_field.default_factory
        ):
            has_default = True
            default_factory = pydantic_field.default_factory

        # Create field info
        field_info = FieldInfo(
            name=name,
            type_info=type_info,
            is_required=is_required,
            has_default=has_default,
            default_value=default_value,
            default_factory=default_factory,
            description=pydantic_field.description,
            alias=pydantic_field.alias,
        )

        # Extract validators if available
        if hasattr(pydantic_field, "validators"):
            field_info.validators = list(pydantic_field.validators)

        return field_info

    def _analyze_type_impl(self, type_hint: Type[Any]) -> Dict[str, Any]:
        """Implementation of type analysis (cached)."""
        origin = get_origin(type_hint)
        args = get_args(type_hint)

        analysis = {
            "type": type_hint,
            "origin": origin,
            "args": args,
            "is_generic": origin is not None,
            "is_union": self._is_union(type_hint),
            "is_optional": self._is_optional(type_hint),
            "is_protocol": self._is_protocol(type_hint),
            "is_typeddict": self._is_typeddict(type_hint),
            "is_literal": origin is not None
            and hasattr(origin, "__name__")
            and origin.__name__ == "Literal",
            "is_forward_ref": isinstance(type_hint, (ForwardRef, str)),
            "is_basemodel": self._is_basemodel(type_hint),
            "is_callable": callable(type_hint),
        }

        # Get module and qualname
        if hasattr(type_hint, "__module__"):
            analysis["module"] = type_hint.__module__
        if hasattr(type_hint, "__qualname__"):
            analysis["qualname"] = type_hint.__qualname__
        elif hasattr(type_hint, "__name__"):
            analysis["qualname"] = type_hint.__name__

        return analysis

    def _get_type_info_impl(self, type_hint: Type[Any]) -> TypeInfo:
        """Implementation of get_type_info (cached)."""
        analysis = self.analyze_type(type_hint)

        return TypeInfo(
            type_hint=type_hint,
            origin=analysis.get("origin"),
            args=analysis.get("args", ()),
            is_generic=analysis.get("is_generic", False),
            is_union=analysis.get("is_union", False),
            is_optional=analysis.get("is_optional", False),
            is_protocol=analysis.get("is_protocol", False),
            is_typeddict=analysis.get("is_typeddict", False),
            is_literal=analysis.get("is_literal", False),
            is_forward_ref=analysis.get("is_forward_ref", False),
            is_basemodel=analysis.get("is_basemodel", False),
            module=analysis.get("module"),
            qualname=analysis.get("qualname"),
        )

    def _is_union(self, type_hint: Type[Any]) -> bool:
        """Check if type is a Union."""
        origin = get_origin(type_hint)
        return origin is Union or (sys.version_info >= (3, 10) and origin is UnionType)

    def _is_optional(self, type_hint: Type[Any]) -> bool:
        """Check if type is Optional (Union[X, None])."""
        if not self._is_union(type_hint):
            return False

        args = get_args(type_hint)
        return type(None) in args

    def _is_protocol(self, type_hint: Type[Any]) -> bool:
        """Check if type is a Protocol."""
        if not inspect.isclass(type_hint):
            return False

        # Check if it's a Protocol
        return any(
            base.__name__ == "Protocol"
            for base in inspect.getmro(type_hint)
            if hasattr(base, "__module__") and "typing" in base.__module__
        )

    def _is_typeddict(self, type_hint: Type[Any]) -> bool:
        """Check if type is a TypedDict."""
        if not hasattr(type_hint, "__annotations__"):
            return False

        # Check for TypedDict in MRO
        mro = getattr(type_hint, "__mro__", [])
        return any(
            base.__name__ == "TypedDict"
            for base in mro
            if hasattr(base, "__module__") and "typing" in base.__module__
        )

    def _is_basemodel(self, type_hint: Type[Any]) -> bool:
        """Check if type is a Pydantic BaseModel."""
        if not inspect.isclass(type_hint):
            return False

        try:
            return issubclass(type_hint, BaseModel)
        except TypeError:
            return False

    def resolve_forward_refs(
        self,
        type_hint: Type[Any],
        globalns: Optional[Dict[str, Any]] = None,
        localns: Optional[Dict[str, Any]] = None,
    ) -> Type[Any]:
        """Resolve forward references in a type hint."""
        if isinstance(type_hint, str):
            # It's a string forward reference
            try:
                return eval(type_hint, globalns or {}, localns or {})
            except Exception:
                return type_hint

        elif isinstance(type_hint, ForwardRef):
            # It's a ForwardRef object
            try:
                return type_hint._evaluate(globalns or {}, localns or {})
            except Exception:
                return type_hint

        # Check if it's a generic with forward refs
        origin = get_origin(type_hint)
        if origin is not None:
            args = get_args(type_hint)
            if args:
                # Recursively resolve args
                resolved_args = tuple(
                    self.resolve_forward_refs(arg, globalns, localns) for arg in args
                )
                # Reconstruct the generic
                return origin[resolved_args]

        return type_hint

    def get_generic_parameters(self, type_hint: Type[Any]) -> Dict[str, Type[Any]]:
        """Extract generic type parameters."""
        params = {}

        # Get type parameters if it's a generic class
        if hasattr(type_hint, "__parameters__"):
            for i, param in enumerate(type_hint.__parameters__):
                params[f"T{i}"] = param

        # Get actual type arguments if it's a generic instance
        origin = get_origin(type_hint)
        if origin is not None:
            args = get_args(type_hint)
            if hasattr(origin, "__parameters__"):
                for param, arg in zip(origin.__parameters__, args):
                    param_name = getattr(param, "__name__", f"T{id(param)}")
                    params[param_name] = arg

        return params

    def is_subtype(self, subtype: Type[Any], supertype: Type[Any]) -> bool:
        """Check if subtype is a subtype of supertype."""
        # Handle None
        if subtype is type(None):
            return self._is_optional(supertype)

        # Direct subclass check
        if inspect.isclass(subtype) and inspect.isclass(supertype):
            try:
                return issubclass(subtype, supertype)
            except TypeError:
                pass

        # Handle generics
        sub_origin = get_origin(subtype)
        super_origin = get_origin(supertype)

        if sub_origin and super_origin:
            # Check origins match
            if not self.is_subtype(sub_origin, super_origin):
                return False

            # Check args
            sub_args = get_args(subtype)
            super_args = get_args(supertype)

            if len(sub_args) != len(super_args):
                return False

            # Check each argument
            for sub_arg, super_arg in zip(sub_args, super_args):
                if not self.is_subtype(sub_arg, super_arg):
                    return False

            return True

        # Handle Union types
        if self._is_union(supertype):
            super_args = get_args(supertype)
            return any(self.is_subtype(subtype, arg) for arg in super_args)

        return False


# Module-level convenience functions
_default_analyzer = TypeAnalyzer()

analyze_type = _default_analyzer.analyze_type
get_type_info = _default_analyzer.get_type_info
analyze_schema = _default_analyzer.analyze_schema
