# src/haive/core/runtime/base/protocols.py
from typing import Protocol, TypeVar, runtime_checkable

from langchain_core.runnables import RunnableConfig

from haive.core.engine.base.protocols import ExtensibleProtocol

# Type variables
I = TypeVar("I")  # Input type
O = TypeVar("O")  # Output type


@runtime_checkable
class RuntimeComponentProtocol(Protocol[I, O], ExtensibleProtocol):
    """Protocol for runtime components built from engine configs."""

    def initialize(self, **kwargs) -> None: ...
    def invoke(
        self, input_data: I, config: RunnableConfig | None = None, **kwargs
    ) -> O: ...
    async def ainvoke(
        self, input_data: I, config: RunnableConfig | None = None, **kwargs
    ) -> O: ...
