"""
Component reference implementation for the Haive engine system.

This module provides a reference mechanism that allows components to be referenced
by their ID, name, or type, and resolved at runtime. This enables lazy loading,
serialization of references, and dynamic resolution of components.
"""

# Forward declaration to avoid circular import
from typing import TYPE_CHECKING, Any, Dict, Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr

# Import EngineType directly from types to avoid circular import
from haive.core.engine.base.types import EngineType

if TYPE_CHECKING:
    from haive.core.engine.base.base import Engine

T = TypeVar("T")  # Resolved component type


class ComponentRef(BaseModel, Generic[T]):
    """
    Reference to a component that can be resolved at runtime.

    This class provides a way to reference components (engines, tools, etc.) without
    directly holding the instance. References can be resolved to the actual component
    when needed, enabling serialization, lazy loading, and runtime configuration.

    Attributes:
        id (Optional[str]): Unique identifier of the referenced component.
        name (Optional[str]): Name of the referenced component.
        type (Optional[Union[str, EngineType]]): Type of the referenced component.
        config_overrides (Dict[str, Any]): Configuration overrides to apply when resolving.
        extensions (List[Dict[str, Any]]): Extensions to apply to the component.
        _resolved (Optional[T]): Private cache for the resolved component instance.

    Type Parameters:
        T: The type of the component that will be resolved.
    """

    # Reference fields
    id: Optional[str] = Field(
        default=None, description="Unique identifier of the referenced component"
    )
    name: Optional[str] = Field(
        default=None, description="Name of the referenced component"
    )
    type: Optional[Union[str, EngineType]] = Field(
        default=None, description="Type of the referenced component"
    )

    # Configuration and extensions
    config_overrides: Dict[str, Any] = Field(
        default_factory=dict,
        description="Configuration overrides to apply when resolving",
    )
    extensions: List[Dict[str, Any]] = Field(
        default_factory=list, description="Extensions to apply to the component"
    )

    # Cache for resolved instance
    _resolved: Optional[T] = PrivateAttr(default=None)

    # Configuration
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def resolve(self) -> Optional[T]:
        """
        Resolve this reference to the actual component.

        Attempts to find and return the referenced component. If the component
        has been previously resolved and cached, returns the cached instance.

        Returns:
            Optional[T]: The resolved component instance, or None if not found.

        Examples:
            >>> # Create a reference to an LLM engine
            >>> ref = ComponentRef(name="gpt-4", type=EngineType.LLM)
            >>> # Resolve the reference to get the actual engine
            >>> llm_engine = ref.resolve()
            >>> if llm_engine:
            ...     response = llm_engine.generate("Hello, world!")
        """
        # Implementation details...
        pass

    def invalidate_cache(self) -> None:
        """
        Clear the cached resolved component.

        Forces the next call to resolve() to fetch the component fresh
        rather than using the cached instance.

        Examples:
            >>> ref = ComponentRef(name="gpt-4", type=EngineType.LLM)
            >>> engine1 = ref.resolve()  # Resolves and caches
            >>> ref.invalidate_cache()
            >>> engine2 = ref.resolve()  # Re-resolves fresh
        """
        self._resolved = None

    @classmethod
    def from_engine(cls, engine: "Any") -> "ComponentRef":
        """
        Create a reference from an engine instance.

        Factory method to create a component reference that points to
        the given engine.

        Args:
            engine: The engine to reference.

        Returns:
            ComponentRef: A new component reference pointing to the engine.

        Examples:
            >>> from haive.core.engine.base import Engine, EngineType
            >>> engine = Engine(name="my_engine", engine_type=EngineType.LLM)
            >>> ref = ComponentRef.from_engine(engine)
            >>> ref.name
            'my_engine'
            >>> ref.type
            <EngineType.LLM: 'llm'>
        """
        return cls(id=engine.id, name=engine.name, type=engine.engine_type)
