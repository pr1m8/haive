from __future__ import annotations

import abc
import importlib.metadata as _md
import inspect
from typing import (
    Annotated,
    Any,
    ClassVar,
    Dict,
    Generic,
    List,
    Optional,
    Protocol,
    Type,
    TypeVar,
    runtime_checkable,
)

from pydantic import BaseModel, Field, computed_field, model_validator
from pydantic.functional_validators import BeforeValidator

# ────────────────────────────  Typing helpers  ─────────────────────────── #
BuildT = TypeVar("BuildT")
C = TypeVar("C")


@runtime_checkable
class Buildable(Protocol[BuildT]):
    def build(self) -> BuildT: ...


# ───────────────────────────── Registry Base  ───────────────────────────── #
class Registered(BaseModel, Generic[BuildT], abc.ABC):
    """
    Registry-aware base class for pluggable, composable components.
    """

    model_config = dict(
        extra="forbid",
        frozen=False,
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )

    NAME: ClassVar[str]
    VERSION: ClassVar[Optional[str]] = None
    DESCRIPTION: ClassVar[Optional[str]] = None
    ALIASES: ClassVar[set[str]] = set()

    _registry: ClassVar[Dict[str, Type[Registered]]] = {}
    _EP_GROUP: ClassVar[str] = "haive.plugins"

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if inspect.isabstract(cls):
            return
        if not hasattr(cls, "NAME"):
            raise TypeError(f"{cls.__name__} must define class attr NAME")

        cls._register_key(cls.NAME, cls)
        for alias in cls.ALIASES:
            cls._register_key(alias, cls)

    @classmethod
    def _register_key(cls, key: str, impl: Type[Registered]) -> None:
        if key in cls._registry and cls._registry[key] is not impl:
            raise ValueError(f"Duplicate registry key '{key}' for {impl.__name__}")
        cls._registry[key] = impl

    @classmethod
    def factory(cls, name: str, /, **data: Any) -> Registered:
        return cls.get_class(name)(**data)  # type: ignore

    @classmethod
    def get_class(cls, name: str) -> Type[Registered]:
        if name not in cls._registry:
            raise KeyError(
                f"Unknown component '{name}'. Choices: {cls.list_available()}"
            )
        return cls._registry[name]

    @classmethod
    def list_available(cls) -> List[str]:
        return sorted(cls._registry.keys())

    @classmethod
    def discover_entry_points(cls) -> None:
        for ep in _md.entry_points(group=cls._EP_GROUP):
            ep.load()

    @computed_field
    def summary(self) -> str:
        ver = self.VERSION or "0.0"
        desc = f" – {self.DESCRIPTION}" if self.DESCRIPTION else ""
        return f"{self.NAME} v{ver}{desc}"

    @abc.abstractmethod
    def build(self) -> BuildT: ...

    @model_serializer(mode="plain")
    def _serialize(self) -> Dict[str, Any]:
        # Use `__dict__` to avoid triggering serialization again
        data = dict(self.__dict__)
        data["type"] = self.__class__.NAME
        return data


# ───────────────────────────── Component Spec  ───────────────────────────── #
def _type_validator(value: str) -> str:
    Registered.get_class(value)
    return value


TypeKey = Annotated[str, BeforeValidator(_type_validator)]  # type: ignore


class ComponentSpec(BaseModel, Generic[C]):
    """
    Resolves either:
    (1) A registered component by type + params
    (2) An inline instance (fully defined)
    """

    model_config = dict(extra="forbid")

    type: Optional[TypeKey] = Field(
        default=None, description="Registry key / alias (exclusive with 'inline')"
    )
    params: Dict[str, Any] = Field(default_factory=dict)

    # NOTE: inline must be a real BaseModel (e.g. Registered[C]) for schema support
    inline: Optional[Registered[C]] = None

    @model_validator(mode="after")
    def _exclusive(self) -> ComponentSpec:
        if bool(self.type) == bool(self.inline):
            raise ValueError("Must provide exactly one of 'type' or 'inline'")
        return self

    def build(self) -> C:
        if self.inline is not None:
            return self.inline.build()
        cls = Registered.get_class(self.type)  # type: ignore
        instance = cls(**self.params)
        return instance.build()


# ──────────────────────────── Example Components ─────────────────────────── #
class Tokenizer(Registered[List[str]]):
    NAME = "whitespace-tokenizer"
    DESCRIPTION = "Splits input text by whitespace"
    text: str

    def build(self) -> List[str]:
        return self.text.split()


class Lowercaser(Registered[str]):
    NAME = "lowercaser"
    DESCRIPTION = "Converts input text to lowercase"
    text: str

    def build(self) -> str:
        return self.text.lower()


# ───────────────────────────── Composite Pipeline ─────────────────────────── #
class TextPipeline(Registered[List[str]]):
    NAME = "basic-text-pipeline"
    DESCRIPTION = "Applies tokenization and normalization"

    tokenizer: ComponentSpec[List[str]]
    normaliser: ComponentSpec[str]

    def build(self) -> List[str]:
        tokens = self.tokenizer.build()
        norm = self.normaliser.build()
        return [t.lower() for t in tokens] + [norm]


# ───────────────────────────── Smoke Test Runner ─────────────────────────── #
if __name__ == "__main__":
    print("Registered:", Registered.list_available())

    cfg = dict(
        tokenizer=dict(type="whitespace-tokenizer", params={"text": "Hello WORLD"}),
        normaliser=dict(type="lowercaser", params={"text": "MiXeD CaSe"}),
    )

    pipeline = TextPipeline(**cfg)

    print("Summary:", pipeline.summary)
    print("Output :", pipeline.build())
