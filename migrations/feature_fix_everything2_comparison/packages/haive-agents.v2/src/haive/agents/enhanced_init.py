"""Enhanced Base Agent Module - Exports enhanced agent classes.

This module exports the enhanced agent classes with engine-focused generics.
Use this instead of the regular base/__init__.py when you want the enhanced pattern.
"""

# Export enhanced classes
from haive.agents.base.enhanced_agent import (
    Agent,
    EngineT,
    TypedInvokableEngine,
    Workflow,
)

# Also export regular mixins - they work with enhanced pattern
from haive.agents.base.mixins import ExecutionMixin, PersistenceMixin, StateMixin
from haive.agents.base.serialization_mixin import SerializationMixin
from haive.agents.base.types import AgentInput, AgentOutput, AgentState

__all__ = [
    # Enhanced classes
    "Agent",
    # Regular mixins and types
    "AgentInput",
    "AgentOutput",
    "AgentState",
    "EngineT",
    "ExecutionMixin",
    "PersistenceMixin",
    "SerializationMixin",
    "StateMixin",
    "TypedInvokableEngine",
    "Workflow",
]
