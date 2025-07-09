from __future__ import annotations

from enum import Enum
from typing import Any, ClassVar, Iterable, Type, TypeVar

from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

# ─── Type variable for enum subclasses ─── #
E = TypeVar("E", bound=Enum)


class _DynEnumMeta(type):
    """
    Metaclass for managing DynamicEnum initialization and schema enforcement.
    """

    def __new__(mcls, name, bases, ns, **kwargs):
        cls = super().__new__(mcls, name, bases, ns, **kwargs)
        if not ns.get("__abstract__", False):
            if not hasattr(cls, "START_VALUES"):
                raise TypeError(f"{name} must define START_VALUES")
            cls._initialize_enum()
        return cls


class DynamicEnum(str, metaclass=_DynEnumMeta):
    """
    A runtime-extensible enum string type for Pydantic validation.
    """

    __abstract__ = True
    START_VALUES: ClassVar[Iterable[str]]
    _values: ClassVar[set[str]]
    _enum_type: ClassVar[Type[Enum]]

    # ─── Enum Lifecycle ─── #
    @classmethod
    def _initialize_enum(cls) -> None:
        cls._values = set(cls.START_VALUES)
        cls._refresh_enum_type()

    @classmethod
    def _refresh_enum_type(cls) -> None:
        cls._enum_type = Enum(f"_{cls.__name__}Enum", {v: v for v in cls._values})

    # ─── Runtime Value Management ─── #
    @classmethod
    def register(cls, *vals: str) -> None:
        cls._values.update(vals)
        cls._refresh_enum_type()

    @classmethod
    def unregister(cls, *vals: str) -> None:
        cls._values.difference_update(vals)
        cls._refresh_enum_type()

    @classmethod
    def choices(cls) -> tuple[str, ...]:
        return tuple(sorted(cls._values))

    @classmethod
    def enum_type(cls) -> Type[Enum]:
        return cls._enum_type

    # ─── Pydantic Core Schema Hook ─── #
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source: type[Any], _handler: Any
    ) -> core_schema.CoreSchema:
        def validate(v: Any) -> str:
            if not isinstance(v, str):
                raise TypeError("string required")
            if v not in cls._values:
                raise ValueError(f"invalid enum value; allowed = {sorted(cls._values)}")
            return v

        return core_schema.no_info_plain_validator_function(validate)

    # ─── JSON Schema for OpenAPI / docs ─── #
    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, _handler: Any
    ) -> JsonSchemaValue:
        return {"type": "string", "enum": list(cls._values)}


# ─── Helper: Dynamically create a new DynamicEnum type ─── #
def create_dynamic_enum(name: str, values: Iterable[str]) -> type[DynamicEnum]:
    return type(
        name, (DynamicEnum,), {"START_VALUES": tuple(values), "__qualname__": name}
    )
