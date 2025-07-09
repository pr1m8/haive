# src/haive/core/runtime/extensions/protocols.py
from typing import Protocol, TypeVar, runtime_checkable

T = TypeVar("T")  # Target type


@runtime_checkable
class ExtensionProtocol(Protocol[T]):
    """Protocol for component extensions."""

    def apply_to(self, target: T) -> T: ...
    def apply(self, target: T) -> None: ...
