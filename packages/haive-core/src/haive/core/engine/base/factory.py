"""Factory implementation for creating runtime components in the Haive system.

This module provides a factory pattern implementation that separates the serializable
configuration of components from their non-serializable runtime instances. This enables
lazy instantiation, caching, and runtime configuration of components.
"""

from typing import TYPE_CHECKING, Any, Dict, Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr

# Forward reference to avoid circular imports
if TYPE_CHECKING:
    from haive.core.engine.base.reference import ComponentRef

T = TypeVar("T")  # Type variable for the created component


class ComponentFactory(BaseModel, Generic[T]):
    """Factory for creating runtime components from engine configurations.

    This class implements the factory pattern to separate serializable configurations
    from non-serializable runtime components. It provides lazy instantiation,
    caching, and the ability to override configuration at runtime.

    Attributes:
        engine_ref (ComponentRef): Reference to the engine configuration that will
            be used to create the component.
        runtime_config (Optional[Dict[str, Any]]): Runtime configuration overrides
            that will be applied when creating the component.
        _component (Optional[T]): Private cache for the created component instance.

    Type Parameters:
        T: The type of component that will be created by this factory.

    Examples:
        >>> from haive.core.engine.base import Engine, EngineType
        >>> from haive.core.engine.base.factory import ComponentFactory
        >>> # Create an engine
        >>> engine = Engine(name="my_engine", engine_type=EngineType.LLM)
        >>> # Create a factory for the engine
        >>> factory = ComponentFactory.for_engine(engine, {"temperature": 0.7})
        >>> # Create the runtime component
        >>> component = factory.create()
    """

    # Reference to the engine configuration
    engine_ref: "ComponentRef" = Field(
        description="Reference to the engine configuration"
    )

    # Runtime configuration
    runtime_config: dict[str, Any] | None = Field(
        default=None, description="Runtime configuration overrides"
    )

    # Private attribute for component cache
    _component: T | None = PrivateAttr(default=None)

    # Configuration for model serialization
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def create(self) -> T:
        """Create the runtime component.

        Resolves the engine reference and creates a runnable component instance
        using the engine's create_runnable method. Caches the created component
        for future calls.

        Returns:
            T: The created runtime component.

        Raises:
            ValueError: If the engine reference cannot be resolved.

        Examples:
            >>> # Import inline to avoid circular imports in examples
            >>> from haive.core.engine.base.reference import ComponentRef
            >>> from haive.core.engine.base.types import EngineType
            >>> factory = ComponentFactory(engine_ref=ComponentRef(name="gpt-4", type=EngineType.LLM))
            >>> llm = factory.create()
            >>> response = llm.generate("Hello, world!")
        """
        # Return cached component if available
        if self._component is not None:
            return self._component

        # Resolve the engine
        engine = self.engine_ref.resolve()
        if not engine:
            raise ValueError(f"Failed to resolve engine reference: {self.engine_ref}")

        # Create the runtime component
        component = engine.create_runnable(self.runtime_config)

        # Cache the component
        self._component = component

        return component

    def invalidate_cache(self) -> None:
        """Invalidate the cached component.

        Clears the cached component instance and invalidates the engine reference cache.
        This forces the next call to create() to instantiate a fresh component.

        Examples:
            >>> factory = ComponentFactory.for_engine(some_engine)
            >>> component1 = factory.create()  # Creates and caches
            >>> factory.invalidate_cache()
            >>> component2 = factory.create()  # Creates fresh
            >>> component1 is component2
            False
        """
        self._component = None
        self.engine_ref.invalidate_cache()

    @classmethod
    def for_engine(
        cls, engine: Any, runtime_config: dict[str, Any] | None = None
    ) -> "ComponentFactory[T]":
        """Create a factory for a specific engine.

        Factory method to create a component factory that will use the specified
        engine and runtime configuration.

        Args:
            engine (Any): The engine instance to use for component creation.
            runtime_config (Optional[Dict[str, Any]]): Optional runtime configuration
                overrides to apply when creating the component.

        Returns:
            ComponentFactory[T]: A new component factory configured for the engine.

        Examples:
            >>> from haive.core.engine.base import Engine, EngineType
            >>> engine = Engine(name="text-embedding-ada-002", engine_type=EngineType.EMBEDDINGS)
            >>> factory = ComponentFactory.for_engine(
            ...     engine,
            ...     {"batch_size": 10}
            ... )
            >>> embeddings = factory.create()
        """
        # Import here to avoid circular imports
        from haive.core.engine.base.reference import ComponentRef

        return cls(
            engine_ref=ComponentRef.from_engine(engine), runtime_config=runtime_config
        )
