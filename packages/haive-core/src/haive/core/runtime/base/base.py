# src/haive/core/runtime/base.py

from abc import abstractmethod
from typing import Any, Generic, Optional, TypeVar

from langchain_core.runnables import Runnable, RunnableConfig

from haive.core.engine import Engine

# Engine config type - must be bound to Engine
EC = TypeVar("EC", bound=Engine)
# Input and output types for better type checking
I = TypeVar("I")
O = TypeVar("O")


class RuntimeComponent(Runnable[I, O], Generic[EC, I, O]):
    """Base class for runtime components built from engine configs."""

    def __init__(self, config: EC, **kwargs):
        """Initialize with engine configuration."""
        super().__init__()  # Initialize Runnable base class
        self.config = config
        self.initialize(**kwargs)

    def initialize(self, **kwargs):
        """Initialize the component.

        This method can be overridden by subclasses.

        Args:
            **kwargs: Additional parameters
        """
        pass

    @abstractmethod
    def invoke(
        self, input_data: I, config: Optional[RunnableConfig] = None, **kwargs
    ) -> O:
        """Invoke the component."""
        pass

    async def ainvoke(
        self, input_data: I, config: Optional[RunnableConfig] = None, **kwargs
    ) -> O:
        """Asynchronously invoke the component.

        By default, this calls invoke in a thread. Override for true async implementation.
        """
        import asyncio

        return await asyncio.to_thread(self.invoke, input_data, config, **kwargs)

    # Method to implement ExtensibleProtocol
    def apply_extensions(self, extensions: list[Any]) -> None:
        """Apply extensions to this component.

        Args:
            extensions: List of extensions to apply
        """
        for extension in extensions:
            if hasattr(extension, "apply") and callable(extension.apply):
                extension.apply(self)
