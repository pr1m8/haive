"""In-memory persistence implementation for the Haive framework.

This module provides an in-memory checkpointer implementation that stores state
data temporarily in memory. It's primarily intended for development, testing,
and demonstration purposes where persistence across application restarts is
not required.

The memory checkpointer is the simplest implementation, requiring no external
dependencies or infrastructure. It supports both synchronous and asynchronous
operation modes, making it suitable for a wide range of use cases where
temporary state management is sufficient.
"""

import logging
from typing import Any, Dict

from pydantic import Field

from haive.core.persistence.base import CheckpointerConfig
from haive.core.persistence.types import (
    CheckpointerMode,
    CheckpointerType,
    CheckpointStorageMode,
)

logger = logging.getLogger(__name__)


class MemoryCheckpointerConfig(CheckpointerConfig[Dict[str, Any]]):
    """Configuration for in-memory checkpoint persistence.

    This implementation provides a simple non-persistent memory-based
    checkpointer suitable for development, testing, and demonstration purposes.
    It stores all state data in memory, which means that state is lost when
    the application is restarted.

    The memory checkpointer is the simplest and most lightweight option,
    requiring no external dependencies, connection setup, or infrastructure.
    It's ideal for:

    - Development environments
    - Testing scenarios
    - Quick prototyping
    - Demonstration purposes
    - Stateless applications that don't need persistence

    It supports both synchronous and asynchronous operation modes, with
    the same underlying implementation since the memory checkpointer is
    inherently thread-safe.

    Example:
        ```python
        from haive.core.persistence import MemoryCheckpointerConfig

        # Create a basic memory checkpointer
        config = MemoryCheckpointerConfig()
        checkpointer = config.create_checkpointer()

        # Use with a graph
        from langgraph.graph import Graph
        graph = Graph(checkpointer=checkpointer)
        ```
    """

    type: CheckpointerType = CheckpointerType.MEMORY
    mode: CheckpointerMode = Field(
        default=CheckpointerMode.SYNC,
        description="Memory checkpointer supports both sync and async modes",
    )
    storage_mode: CheckpointStorageMode = Field(
        default=CheckpointStorageMode.FULL,
        description="Storage mode - memory checkpointer always stores full history",
    )

    class Config:
        arbitrary_types_allowed = True

    def is_async_mode(self) -> bool:
        """Check if this configuration is set to operate in asynchronous mode.

        This method determines whether the memory checkpointer should use
        asynchronous operations based on the configured mode. For memory
        checkpointers, this is primarily a compatibility feature since
        the underlying implementation is the same for both modes.

        Returns:
            bool: True if configured for async operations, False for synchronous
        """
        return self.mode == CheckpointerMode.ASYNC

    def create_checkpointer(self) -> Any:
        """Create a synchronous memory checkpointer.

        This method creates a LangGraph MemorySaver instance that stores
        all state data in memory. The memory checkpointer is thread-safe
        and can be shared between multiple graph instances if needed.

        The implementation is very lightweight, simply instantiating a
        MemorySaver object with no additional configuration needed.

        Returns:
            Any: A LangGraph MemorySaver instance ready for use

        Raises:
            RuntimeError: If the MemorySaver class cannot be imported or
                instantiated, typically due to a missing dependency

        Example:
            ```python
            config = MemoryCheckpointerConfig()
            checkpointer = config.create_checkpointer()
            # Use with a synchronous graph
            graph = Graph(checkpointer=checkpointer)
            ```
        """
        try:
            from langgraph.checkpoint.memory import MemorySaver

            # Create checkpointer - no additional configuration needed
            checkpointer = MemorySaver()

            logger.info("Memory checkpointer created successfully")
            return checkpointer

        except Exception as e:
            logger.error(f"Failed to create memory checkpointer: {e}")
            raise RuntimeError(f"Failed to create memory checkpointer: {e}")

    async def create_async_checkpointer(self) -> Any:
        """Create an asynchronous memory checkpointer.

        For memory checkpointers, this method returns the same synchronous
        MemorySaver instance since it's inherently thread-safe and can be
        used in asynchronous contexts without modification. This simplifies
        the implementation while still providing the expected interface.

        The method sets the mode to ASYNC for consistency, but the underlying
        implementation remains the same as the synchronous version.

        Returns:
            Any: A LangGraph MemorySaver instance ready for async use

        Example:
            ```python
            config = MemoryCheckpointerConfig(mode=CheckpointerMode.ASYNC)
            async_checkpointer = await config.create_async_checkpointer()
            # Use with an async graph
            graph = AsyncGraph(checkpointer=async_checkpointer)
            ```
        """
        # Force async mode for consistency
        self.mode = CheckpointerMode.ASYNC

        # Return the regular memory saver - it's thread-safe for async use
        return self.create_checkpointer()

    async def initialize_async_checkpointer(self) -> Any:
        """Initialize an async checkpointer with resource management.

        For memory checkpointers, this method simply returns the checkpointer
        directly since there are no external resources (like database connections)
        to manage. Unlike database-backed implementations, the memory checkpointer
        doesn't need an async context manager for resource lifecycle management.

        This method exists primarily for interface compatibility with other
        checkpointer implementations that do require resource management.

        Returns:
            Any: A LangGraph MemorySaver instance ready for async use

        Example:
            ```python
            config = MemoryCheckpointerConfig(mode=CheckpointerMode.ASYNC)
            # Simple usage without context management
            checkpointer = await config.initialize_async_checkpointer()
            # Use the checkpointer...
            ```
        """
        # Simply create and return - no resource management needed
        return await self.create_async_checkpointer()
