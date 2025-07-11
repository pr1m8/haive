"""
Typed State Schema with Generic Engine Support.

This module provides enhanced state schema classes that use generics for proper
engine typing while maintaining backward compatibility with existing code.
"""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

from pydantic import BaseModel, Field, PrivateAttr, field_validator, model_validator

from haive.core.schema.state_schema import StateSchema

if TYPE_CHECKING:
    from haive.core.engine.base import Engine

# Type variables for engines
TEngine = TypeVar("TEngine", bound="Engine")
TEngines = TypeVar("TEngines", bound=Dict[str, "Engine"])


class TypedStateSchema(StateSchema, Generic[TEngine]):
    """
    State schema with optional engine typing for better type safety.

    This class extends StateSchema with generic type support for engines,
    allowing for better type checking while maintaining backward compatibility.

    Example:
        ```python
        from haive.core.engine.llm import LLMEngine

        # Typed usage - engine type is known
        class MyState(TypedStateSchema[LLMEngine]):
            query: str = Field(default="")

        state = MyState()
        state.engine = my_llm_engine  # Type checked!

        # Backward compatible - no type specified
        class LegacyState(TypedStateSchema):
            query: str = Field(default="")

        # Also works with base StateSchema
        class OldState(StateSchema):
            query: str = Field(default="")
        ```
    """

    # Override engine field with generic type
    engine: Optional[Union[TEngine, Dict[str, Any]]] = Field(
        default=None, description="Optional main/primary engine (typed)"
    )

    # Private attribute to store the actual engine type
    _engine_type: Optional[Type[TEngine]] = PrivateAttr(default=None)

    def __class_getitem__(cls, engine_type: Type[TEngine]) -> Type["TypedStateSchema"]:
        """
        Create a typed version of this schema with specific engine type.

        This allows for syntax like TypedStateSchema[LLMEngine].
        """

        # Create a new class that remembers its engine type
        class _TypedSchema(cls):
            _engine_type = engine_type

            # Override the engine field with the specific type
            engine: Optional[Union[engine_type, Dict[str, Any]]] = Field(
                default=None, description=f"Optional {engine_type.__name__} engine"
            )

        # Set proper name for debugging
        _TypedSchema.__name__ = f"{cls.__name__}[{engine_type.__name__}]"
        _TypedSchema.__qualname__ = f"{cls.__qualname__}[{engine_type.__name__}]"

        return _TypedSchema

    @field_validator("engine", mode="before")
    @classmethod
    def validate_typed_engine(cls, v):
        """
        Enhanced engine validation that checks type if specified.

        Maintains backward compatibility while adding type checking.
        """
        # First do the base validation
        if v is None or isinstance(v, dict):
            return v

        # If we have a type specified, check it
        if hasattr(cls, "_engine_type") and cls._engine_type is not None:
            # Import here to avoid circular imports
            from haive.core.engine.base import Engine

            # Check if it's the right type of engine
            if isinstance(v, Engine) and not isinstance(v, cls._engine_type):
                # Log warning but don't fail for backward compatibility
                import logging

                logger = logging.getLogger(__name__)
                logger.warning(
                    f"Engine type mismatch: expected {cls._engine_type.__name__}, "
                    f"got {type(v).__name__}"
                )

        return v


class MultiEngineStateSchema(StateSchema):
    """
    State schema optimized for multiple engines with clear typing.

    This schema provides better support for agents with multiple engines,
    with clear field naming and type safety.

    Example:
        ```python
        class RAGState(MultiEngineStateSchema):
            query: str = Field(default="")

            # Engines are defined with clear types
            def __init__(self, **data):
                super().__init__(**data)
                self.register_engine("llm", llm_engine)
                self.register_engine("retriever", retriever_engine)
        ```
    """

    # Override engines with better typing
    engines: Dict[str, Union["Engine", Dict[str, Any]]] = Field(
        default_factory=dict, description="Registry of named engines with proper typing"
    )

    # Track engine types for validation
    _engine_types: Dict[str, Type["Engine"]] = PrivateAttr(default_factory=dict)

    def register_engine(
        self, name: str, engine: "Engine", engine_type: Optional[Type["Engine"]] = None
    ) -> None:
        """
        Register an engine with optional type tracking.

        Args:
            name: Name to register engine under
            engine: Engine instance to register
            engine_type: Optional specific engine type for validation
        """
        self.engines[name] = engine

        # Set as main engine if first one
        if self.engine is None:
            self.engine = engine

        # Track type if provided
        if engine_type:
            self._engine_types[name] = engine_type

    def get_typed_engine(
        self, name: str, engine_type: Type[TEngine]
    ) -> Optional[TEngine]:
        """
        Get an engine with type checking.

        Args:
            name: Name of engine to retrieve
            engine_type: Expected type of engine

        Returns:
            Typed engine instance or None
        """
        engine = self.engines.get(name)

        if engine is None:
            return None

        # Handle dict representation
        if isinstance(engine, dict):
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(f"Engine '{name}' is serialized dict, cannot type check")
            return engine  # type: ignore

        # Check type
        if not isinstance(engine, engine_type):
            raise TypeError(
                f"Engine '{name}' is {type(engine).__name__}, "
                f"expected {engine_type.__name__}"
            )

        return engine

    @property
    def llm_engine(self) -> Optional["Engine"]:
        """Typed accessor for LLM engine."""
        # Try standard names first
        for name in ["llm", "llm_engine", "main"]:
            if name in self.engines:
                return self.engines[name]

        # Check by engine type
        for name, engine in self.engines.items():
            if hasattr(engine, "engine_type"):
                from haive.core.engine.base import EngineType

                if engine.engine_type == EngineType.LLM:
                    return engine

        return None

    @property
    def retriever_engine(self) -> Optional["Engine"]:
        """Typed accessor for retriever engine."""
        # Try standard names first
        for name in ["retriever", "retriever_engine", "rag"]:
            if name in self.engines:
                return self.engines[name]

        # Check by engine type
        for name, engine in self.engines.items():
            if hasattr(engine, "engine_type"):
                from haive.core.engine.base import EngineType

                if engine.engine_type == EngineType.RETRIEVER:
                    return engine

        return None


class HierarchicalStateSchema(BaseModel):
    """
    Hierarchical state schema for proper multi-agent isolation.

    This schema provides a hierarchical structure that prevents field
    conflicts and enables proper agent isolation.

    Example:
        ```python
        class MultiAgentState(HierarchicalStateSchema):
            # Shared fields accessible by all agents
            shared = SharedState()

            # Per-agent isolated state
            agents = Dict[str, AgentState]

            # Routing and control
            routing = RoutingState()
        ```
    """

    class SharedState(BaseModel):
        """State shared across all agents."""

        messages: List[Any] = Field(default_factory=list, description="Shared messages")
        context: Dict[str, Any] = Field(
            default_factory=dict, description="Shared context"
        )

    class AgentState(BaseModel):
        """Isolated state for individual agent."""

        working_memory: Dict[str, Any] = Field(default_factory=dict)
        local_tools: List[Any] = Field(default_factory=list)
        engine: Optional[Dict[str, Any]] = None

    class RoutingState(BaseModel):
        """Routing control state."""

        current_agent: Optional[str] = None
        next_agent: Optional[str] = None
        execution_history: List[str] = Field(default_factory=list)

    # Main fields
    shared: SharedState = Field(default_factory=SharedState, description="Shared state")
    agents: Dict[str, AgentState] = Field(
        default_factory=dict, description="Per-agent state"
    )
    routing: RoutingState = Field(
        default_factory=RoutingState, description="Routing state"
    )

    def get_agent_view(self, agent_name: str) -> "AgentView":
        """
        Get an isolated view for a specific agent.

        Args:
            agent_name: Name of agent to create view for

        Returns:
            Agent-specific view of the state
        """
        from haive.core.schema.agent_view import AgentView

        # Ensure agent state exists
        if agent_name not in self.agents:
            self.agents[agent_name] = self.AgentState()

        return AgentView(
            agent_name=agent_name,
            shared=self.shared,  # Read-only reference
            private=self.agents[agent_name],
            parent_state=self,
        )

    def merge_agent_results(self, agent_name: str, results: Dict[str, Any]) -> None:
        """
        Merge results from an agent back into the state.

        Args:
            agent_name: Name of agent that produced results
            results: Results to merge
        """
        # Update agent's private state
        if agent_name in self.agents:
            self.agents[agent_name].working_memory.update(results)

        # Handle shared fields (like messages)
        if "messages" in results:
            self.shared.messages.extend(results["messages"])


# Backward compatibility helpers
def create_typed_state_schema(
    base_schema: Type[StateSchema], engine_type: Optional[Type[TEngine]] = None
) -> Type[StateSchema]:
    """
    Create a typed version of an existing state schema.

    Args:
        base_schema: Base schema class to extend
        engine_type: Optional engine type for typing

    Returns:
        New schema class with engine typing

    Example:
        ```python
        # Take existing schema and add typing
        TypedConversationState = create_typed_state_schema(
            ConversationState,
            LLMEngine
        )
        ```
    """
    if engine_type is None:
        return base_schema

    class _TypedSchema(TypedStateSchema[engine_type], base_schema):
        """Typed version of the schema."""

        pass

    # Set proper name
    _TypedSchema.__name__ = f"Typed{base_schema.__name__}"
    _TypedSchema.__qualname__ = f"Typed{base_schema.__qualname__}"

    return _TypedSchema
