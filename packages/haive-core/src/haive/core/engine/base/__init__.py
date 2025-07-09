"""
Base abstractions for the Haive engine system.

This package provides the core abstractions and base classes for all engine types
in the Haive framework. Engines are configurable factory objects that create and
manage runtime components like LLMs, vector stores, retrievers, and tools.

The main components include:
- Engine: The base class for all engine types
- EngineType: Enumeration of supported engine types
- EngineRegistry: Centralized registry for engine instances
- Invokable/AsyncInvokable: Protocols for objects that can be invoked
- ComponentRef: Reference mechanism for lazy loading of components
- ComponentFactory: Factory pattern for creating runtime components

The engine system follows a configuration/factory pattern that separates:
1. Serializable configuration (Engine and its subclasses)
2. Runtime components (created by engines with create_runnable)

This enables configuration management, serialization, and runtime optimization.
"""

from haive.core.engine.base.base import Engine, InvokableEngine, NonInvokableEngine
from haive.core.engine.base.factory import ComponentFactory
from haive.core.engine.base.protocols import AsyncInvokable, Invokable
from haive.core.engine.base.reference import ComponentRef
from haive.core.engine.base.registry import EngineRegistry
from haive.core.engine.base.types import EngineType

__all__ = [
    # Base engine classes
    "Engine",
    "InvokableEngine",
    "NonInvokableEngine",
    # Registry and type system
    "EngineRegistry",
    "EngineType",
    # Factory and reference patterns
    "ComponentFactory",
    "ComponentRef",
    # Protocols
    "Invokable",
    "AsyncInvokable",
]
