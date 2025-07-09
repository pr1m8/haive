"""
Persistence module for the Haive framework.

This module provides components for state persistence in agents and workflow graphs,
with implementations for various storage backends.
"""

from haive.core.persistence.base import CheckpointerConfig
from haive.core.persistence.memory import MemoryCheckpointerConfig
from haive.core.persistence.postgres_config import PostgresCheckpointerConfig
from haive.core.persistence.types import (
    CheckpointerMode,
    CheckpointerType,
    CheckpointStorageMode,
)

# Utility functions
from haive.core.persistence.utils import (
    ensure_async_pool_open,
    ensure_pool_open,
    register_thread,
    register_thread_async,
)

# Default exports
__all__ = [
    # Main classes
    "CheckpointerConfig",
    "MemoryCheckpointerConfig",
    "PostgresCheckpointerConfig",
    # Enums & Types
    "CheckpointerType",
    "CheckpointerMode",
    "CheckpointStorageMode",
    # Utility functions
    "ensure_pool_open",
    "ensure_async_pool_open",
    "register_thread",
    "register_thread_async",
]
