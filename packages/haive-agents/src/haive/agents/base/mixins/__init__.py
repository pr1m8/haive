"""Agent Mixins - Modular capabilities for Haive agents.

This module provides mixins that add specific capabilities to agent classes:
- ExecutionMixin: Run, stream, and invocation functionality
- StateMixin: State management and persistence operations
- PersistenceMixin: Checkpointer and store configuration

Example:
    Basic usage::

        from haive.agents.base.mixins import ExecutionMixin, StateMixin, PersistenceMixin

        class MyAgent(PersistenceMixin, ExecutionMixin, StateMixin):
            def setup_agent(self):
                # Configure persistence
                self.persistence = PostgresCheckpointerConfig()
                self.checkpoint_mode = "async"
"""

from .execution_mixin import ExecutionMixin
from .persistence_mixin import PersistenceMixin
from .state_mixin import StateMixin

__all__ = [
    "ExecutionMixin",
    "StateMixin",
    "PersistenceMixin",
]
