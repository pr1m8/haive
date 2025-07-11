"""Persistence module for state management and checkpointing in the Haive framework.

This module provides a comprehensive system for persisting agent state across sessions,
allowing for stateful agents that can continue conversations and maintain context
over time. It offers multiple storage backends and configuration options to balance
performance, durability, and scalability.

Key components:
- CheckpointerConfig: Base configuration for all persistence providers
- MemoryCheckpointerConfig: In-memory persistence for development and testing
- PostgresCheckpointerConfig: PostgreSQL-backed persistence for production
- SQLiteCheckpointerConfig: SQLite-backed persistence for local development
- SupabaseCheckpointerConfig: Supabase-backed persistence for cloud deployments

The module integrates with LangGraph's checkpoint system while providing enhanced
features like connection pooling, automatic retry with exponential backoff, and
thread registration for tracking agent sessions.

Usage:
    ```python
    from haive.core.persistence import MemoryCheckpointerConfig

    # Create a memory-based checkpointer
    config = MemoryCheckpointerConfig()
    checkpointer = config.create_checkpointer()

    # Use in an agent configuration
    agent_config = AgentConfig(
        persistence=config,
        # other configuration...
    )
    ```

For more advanced usage with PostgreSQL:
    ```python
    from haive.core.persistence import PostgresCheckpointerConfig
    from haive.core.persistence.types import CheckpointerMode, CheckpointStorageMode

    # Create a PostgreSQL checkpointer
    postgres_config = PostgresCheckpointerConfig(
        mode=CheckpointerMode.ASYNC,  # Use async operations
        storage_mode=CheckpointStorageMode.SHALLOW,  # Only store latest state
        db_host="localhost",
        db_port=5432,
        db_name="haive",
        db_user="postgres",
        db_pass="password"
    )

    # For async usage
    async def setup():
        async_checkpointer = await postgres_config.create_async_checkpointer()
        # Use the checkpointer...
    ```

This module is designed to work seamlessly with both synchronous and asynchronous
code, providing appropriate interfaces for each context.
"""

# Base persistence classes
from haive.core.persistence.base import CheckpointerConfig

# Factory functions
from haive.core.persistence.factory import (
    acreate_postgres_checkpointer,
    create_postgres_checkpointer,
)

# Handler utilities
from haive.core.persistence.handlers import setup_checkpointer

# Persistence implementations
from haive.core.persistence.memory import MemoryCheckpointerConfig
from haive.core.persistence.postgres_config import PostgresCheckpointerConfig
from haive.core.persistence.sqlite_config import SQLiteCheckpointerConfig
from haive.core.persistence.supabase_config import SupabaseCheckpointerConfig

# Type definitions
from haive.core.persistence.types import (
    CheckpointerMode,
    CheckpointerType,
    CheckpointStorageMode,
)

__all__ = [
    "CheckpointStorageMode",
    # Base classes
    "CheckpointerConfig",
    # Types
    "CheckpointerMode",
    "CheckpointerType",
    # Implementations
    "MemoryCheckpointerConfig",
    "PostgresCheckpointerConfig",
    "SQLiteCheckpointerConfig",
    "SupabaseCheckpointerConfig",
    "acreate_postgres_checkpointer",
    # Factory functions
    "create_postgres_checkpointer",
    # Handlers
    "setup_checkpointer",
]
