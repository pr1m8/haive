from __future__ import annotations

import inspect
from typing import (
    Any,
    ClassVar,
    Generic,
    Iterable,
    Literal,
    TypeVar,
    cast,
    get_args,
    get_origin,
)

from pydantic import BaseModel
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

T = TypeVar("T", bound=str)


class _DynLitMeta(type):
    def __new__(mcls, name, bases, ns, **kw):
        cls = super().__new__(mcls, name, bases, ns, **kw)
        if not ns.get("__abstract__", False):
            if not hasattr(cls, "START_VALUES"):
                raise TypeError(f"{name} must define class attr START_VALUES")
            cls._values = set(cls.START_VALUES)
        return cls


class DynamicLiteral(str, Generic[T], metaclass=_DynLitMeta):
    """
    Dynamic "Literal-like" type with runtime-extensible allowed values.
    Meant to be used as a Pydantic field type.
    """

    __abstract__ = True
    _values: ClassVar[set[str]]
    START_VALUES: ClassVar[Iterable[str]]

    @classmethod
    def register(cls, *vals: str) -> None:
        cls._values.update(vals)

    @classmethod
    def unregister(cls, *vals: str) -> None:
        cls._values.difference_update(vals)

    @classmethod
    def choices(cls) -> tuple[str, ...]:
        return tuple(sorted(cls._values))

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source: type[Any], _handler: Any
    ) -> core_schema.CoreSchema:
        def _validate(v: Any) -> str:
            caller = inspect.stack()[2].function
            if not isinstance(v, str):
                print(
                    f"[Validation ❌] {caller}: Expected str, got {type(v).__name__} → {v!r}"
                )
                raise TypeError("string required")
            if v not in cls._values:
                print(
                    f"[Validation ❌] {caller}: '{v}' not in allowed values {sorted(cls._values)}"
                )
                raise ValueError(f"invalid literal; allowed = {sorted(cls._values)!r}")
            print(f"[Validation ✅] {caller}: accepted → {v!r}")
            return v

        return core_schema.no_info_plain_validator_function(_validate)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, _handler: Any
    ) -> JsonSchemaValue:
        return {"type": "string", "enum": list(cls._values)}

    @classmethod
    def literal_type(cls) -> Any:
        return cast(Any, Literal[tuple(cls._values)])


def create_dynamic_literal(name: str, values: Iterable[str]) -> type[DynamicLiteral]:
    attrs = {"START_VALUES": tuple(values), "__qualname__": name}
    return type(name, (DynamicLiteral,), attrs)


# ──────────────────────────────── Demo Subclass ────────────────────────────────


class Colour(DynamicLiteral):
    START_VALUES = ("red", "green", "blue")


class PaintJob(BaseModel):
    base: Colour
    accent: Colour

    class Config:
        extra = "forbid"


if __name__ == "__main__":
    pj1 = PaintJob(base="red", accent="green")
    print("✅ OK:", pj1.model_dump())

    Colour.register("purple")
    pj2 = PaintJob(base="purple", accent="blue")
    print("✅ OK:", pj2.model_dump())

    try:
        PaintJob(base="chartreuse", accent="green")
    except Exception as e:
        print("❌ Expected error →", e)

    print(
        "📜 JSON schema enum:",
        PaintJob.model_json_schema()["properties"]["base"]["enum"],
    )
    print(
        "🔎 Literal type:",
        get_origin(Colour.literal_type()),
        "→",
        get_args(Colour.literal_type()),
    )
