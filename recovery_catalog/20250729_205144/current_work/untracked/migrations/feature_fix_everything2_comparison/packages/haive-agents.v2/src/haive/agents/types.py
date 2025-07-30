# haive/agents/base/types.py

"""Core type system for the Haive agent framework.

Defines type variables, constraints, and base protocols for type-safe agent design.
"""

from enum import Enum
from typing import (
    Any,
    Generic,
    Protocol,
    TypeVar,
    runtime_checkable,
)

from haive.core.engine.base import Engine, InvokableEngine
from haive.core.schema.state_schema import StateSchema
from pydantic import BaseModel

# ============================================================================
# CORE TYPE VARIABLES
# ============================================================================

# Engine types - properly constrained
TEngine = TypeVar("TEngine", bound=Engine)
TInvokableEngine = TypeVar("TInvokableEngine", bound=InvokableEngine)

# Input/Output types - must be BaseModel for serialization
TInput = TypeVar("TInput", bound=BaseModel)
TOutput = TypeVar("TOutput", bound=BaseModel)

# State type - must extend StateSchema for proper state management
TState = TypeVar("TState", bound=StateSchema)

# Config type - for configuration
TConfig = TypeVar("TConfig", bound=BaseModel)

# Node type - for graph nodes
TNode = TypeVar("TNode")

# ============================================================================
# BASE PROTOCOLS
# ============================================================================


@runtime_checkable
class GraphProvider(Protocol[TState]):
    """Protocol for objects that provide graphs."""

    def build_graph(self) -> Any:  # Returns BaseGraph
        """Build and return the graph."""
        ...


@runtime_checkable
class StateProvider(Protocol[TState]):
    """Protocol for objects that provide state schemas."""

    @property
    def state_schema(self) -> type[TState]:
        """Get the state schema type."""
        ...


@runtime_checkable
class Invokable(Protocol[TInput, TOutput]):
    """Protocol for objects that can be invoked."""

    def invoke(
        self, input_data: TInput, config: dict[str, Any] | None = None
    ) -> TOutput:
        """Invoke with input data."""
        ...

    async def ainvoke(
        self, input_data: TInput, config: dict[str, Any] | None = None
    ) -> TOutput:
        """Async invoke with input data."""
        ...


@runtime_checkable
class EngineProvider(Protocol[TEngine]):
    """Protocol for objects that provide engines."""

    @property
    def engine(self) -> TEngine:
        """Get the primary engine."""
        ...

    @property
    def engines(self) -> dict[str, Engine]:
        """Get all engines."""
        ...


# ============================================================================
# COMPOSITE PROTOCOLS
# ============================================================================


class Agent(
    GraphProvider[TState],
    StateProvider[TState],
    Invokable[TInput, TOutput],
    EngineProvider[TEngine],
    Protocol[TEngine, TInput, TOutput, TState],
):
    """Complete agent protocol combining all capabilities."""


# ============================================================================
# GRAPH TOPOLOGY TYPES
# ============================================================================


class NodeConnection(BaseModel, Generic[TState]):
    """Represents a connection between nodes in a graph."""

    source: str
    target: str
    condition: Any | None = None  # Callable[[TState], bool]
    metadata: dict[str, Any] = {}


class GraphSegment(BaseModel, Generic[TState]):
    """Represents a segment of a graph that can be composed."""

    nodes: dict[str, Any]  # node_name -> NodeConfig
    edges: list[NodeConnection[TState]]
    entry_point: str
    exit_points: list[str]
    metadata: dict[str, Any] = {}


# ============================================================================
# HOOK TYPES
# ============================================================================


class HookPoint(str, Enum):
    """Standard hook points in agent lifecycle."""

    # Initialization
    BEFORE_INIT = "before_init"
    AFTER_INIT = "after_init"

    # Setup
    BEFORE_SETUP = "before_setup"
    AFTER_SETUP = "after_setup"

    # Schema
    BEFORE_SCHEMA_BUILD = "before_schema_build"
    AFTER_SCHEMA_BUILD = "after_schema_build"

    # Graph
    BEFORE_GRAPH_BUILD = "before_graph_build"
    AFTER_GRAPH_BUILD = "after_graph_build"
    BEFORE_GRAPH_COMPILE = "before_graph_compile"
    AFTER_GRAPH_COMPILE = "after_graph_compile"

    # Nodes
    BEFORE_NODE_ADD = "before_node_add"
    AFTER_NODE_ADD = "after_node_add"

    # Execution
    BEFORE_INVOKE = "before_invoke"
    AFTER_INVOKE = "after_invoke"

    # State
    BEFORE_STATE_UPDATE = "before_state_update"
    AFTER_STATE_UPDATE = "after_state_update"


class HookContext(BaseModel, Generic[TState]):
    """Context passed to hooks."""

    hook_point: HookPoint
    agent_id: str
    agent_type: str
    state_type: type[TState] | None = None
    metadata: dict[str, Any] = {}


# Type for hook functions
# Callable[[Any, HookContext], Any]
HookFunction = TypeVar("HookFunction", bound=Any)


# ============================================================================
# DEFAULT AGENT SCHEMAS
# ============================================================================


class AgentInput(BaseModel):
    """Default input schema for agents."""

    messages: list[Any] = []


class AgentOutput(BaseModel):
    """Default output schema for agents."""

    messages: list[Any] = []


class AgentState(BaseModel):
    """Default state schema for agents."""

    messages: list[Any] = []
