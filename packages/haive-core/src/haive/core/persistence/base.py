"""Base classes and interfaces for the Haive persistence system.

This module defines the core abstractions and interfaces for the persistence
system used throughout the Haive framework. It provides the foundation for
various persistence implementations, ensuring a consistent interface regardless
of the underlying storage technology.

The central component is the CheckpointerConfig abstract base class, which
defines the configuration interface that all persistence providers must implement.
This allows different storage backends to be used interchangeably while providing
a unified API for state persistence.
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

from haive.core.persistence.types import (
    CheckpointerMode,
    CheckpointerType,
    CheckpointStorageMode,
)

# Type variable for different connection types
T = TypeVar("T")


class CheckpointerConfig(BaseModel, ABC, Generic[T]):
    """Base configuration for checkpoint persistence implementations.

    This abstract base class defines the interface for all checkpointer
    configurations in the Haive framework. It provides a standardized way
    to configure and create checkpointer instances, regardless of the underlying
    storage technology.

    The CheckpointerConfig class is generic over the connection type T, allowing
    different implementations to use appropriate connection objects (e.g.,
    connection pools for databases, client objects for cloud services).

    All concrete implementations must provide methods for creating both synchronous
    and asynchronous checkpointer instances, ensuring compatibility with both
    programming models.

    Attributes:
        type: The type of checkpointer (e.g., memory, postgres, sqlite)
        mode: Operational mode - synchronous or asynchronous
        storage_mode: Storage mode - full history or just the latest state
        setup_needed: Whether tables/structures need to be created on first use
    """

    type: CheckpointerType = Field(description="Type of checkpointer to use")
    mode: CheckpointerMode = Field(
        default=CheckpointerMode.SYNC,
        description="Operational mode - synchronous or asynchronous",
    )
    storage_mode: CheckpointStorageMode = Field(
        default=CheckpointStorageMode.FULL,
        description="Storage mode - full history or shallow (latest only)",
    )
    setup_needed: bool = Field(
        default=True, description="Whether tables need to be setup on first use"
    )

    class Config:
        arbitrary_types_allowed = True

    def is_async_mode(self) -> bool:
        """Check if this configuration is set to operate in asynchronous mode.

        This method determines whether the checkpointer should use asynchronous
        operations based on the configured mode. It's used internally to choose
        between synchronous and asynchronous implementations.

        Returns:
            bool: True if configured for async operations, False for synchronous

        Example:
            ```python
            config = PostgresCheckpointerConfig(mode=CheckpointerMode.ASYNC)
            if config.is_async_mode():
                # Use async methods
                checkpointer = await config.create_async_checkpointer()
            else:
                # Use sync methods
                checkpointer = config.create_checkpointer()
            ```
        """
        return self.mode == CheckpointerMode.ASYNC

    @abstractmethod
    def create_checkpointer(self) -> Any:
        """Create a synchronous checkpointer instance based on this configuration.

        This method instantiates and configures a synchronous checkpointer that
        matches the settings in this configuration. The returned object will be
        a compatible checkpointer implementation (typically a LangGraph Saver)
        that can be used for storing and retrieving state.

        Implementations should handle connection management, setup of required
        database structures, and proper error handling with fallbacks.

        Returns:
            Any: A configured synchronous checkpointer instance

        Raises:
            RuntimeError: If the checkpointer cannot be created due to missing
                dependencies or connection issues

        Example:
            ```python
            config = MemoryCheckpointerConfig()
            checkpointer = config.create_checkpointer()
            # Use checkpointer with a graph
            graph = Graph(checkpointer=checkpointer)
            ```
        """

    @abstractmethod
    async def create_async_checkpointer(self) -> Any:
        """Create an asynchronous checkpointer instance.

        This method instantiates and configures an asynchronous checkpointer
        that matches the settings in this configuration. The returned object
        will be a compatible async checkpointer implementation that can be used
        for storing and retrieving state in asynchronous contexts.

        Implementations should handle async connection management, setup of required
        database structures, and proper error handling with fallbacks.

        Returns:
            Any: A configured asynchronous checkpointer instance

        Raises:
            RuntimeError: If the async checkpointer cannot be created due to
                missing dependencies or connection issues

        Example:
            ```python
            config = PostgresCheckpointerConfig(mode=CheckpointerMode.ASYNC)
            async_checkpointer = await config.create_async_checkpointer()
            # Use with async graph
            graph = AsyncGraph(checkpointer=async_checkpointer)
            ```
        """

    @abstractmethod
    async def initialize_async_checkpointer(self) -> Any:
        """Initialize an async checkpointer with proper resource management.

        This method creates and initializes an asynchronous checkpointer with
        appropriate resource management. Unlike create_async_checkpointer,
        this method may return an async context manager that properly handles
        the lifecycle of resources like connection pools.

        This is particularly important for database-backed checkpointers to
        ensure connections are properly closed when they're no longer needed.

        Returns:
            Any: An async context manager or the checkpointer itself, depending
                on implementation requirements

        Example:
            ```python
            config = PostgresCheckpointerConfig(mode=CheckpointerMode.ASYNC)
            async with await config.initialize_async_checkpointer() as checkpointer:
                # Use checkpointer with async code
                # Resources will be properly closed after this block
            ```
        """

    def to_dict(self) -> dict[str, Any]:
        """Convert this configuration to a dictionary.

        This method serializes the configuration to a dictionary format,
        which is useful for persistence, logging, or passing to external
        systems. It automatically handles both Pydantic v1 and v2 models
        and excludes sensitive fields like passwords.

        Returns:
            Dict[str, Any]: Dictionary representation of this configuration

        Example:
            ```python
            config = PostgresCheckpointerConfig(db_host="localhost")
            config_dict = config.to_dict()
            print(config_dict)  # {'type': 'postgres', 'db_host': 'localhost', ...}
            ```
        """
        # Use Pydantic v2 serialization if available
        if hasattr(self, "model_dump"):
            # Exclude SecretStr fields for security
            return self.model_dump(exclude={"db_pass"})

        # Fall back to Pydantic v1
        return self.dict(exclude={"db_pass"})

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CheckpointerConfig":
        """Create a checkpointer configuration from a dictionary.

        This factory method deserializes a configuration from a dictionary,
        automatically selecting the appropriate implementation class based on
        the 'type' field. It provides a convenient way to create configurations
        from serialized data or configuration files.

        The method dynamically imports the appropriate configuration class based
        on the specified type, ensuring minimal dependencies are loaded when not needed.

        Args:
            data: Dictionary containing configuration parameters, must include a
                'type' field specifying which checkpointer implementation to use

        Returns:
            CheckpointerConfig: An instantiated checkpointer configuration of the
                appropriate subclass

        Raises:
            ValueError: If the 'type' field is missing or specifies an unsupported
                checkpointer type

        Example:
            ```python
            config_dict = {
                "type": "postgres",
                "db_host": "localhost",
                "db_port": 5432
            }
            config = CheckpointerConfig.from_dict(config_dict)
            # Returns a PostgresCheckpointerConfig instance
            ```
        """
        # Ensure type is specified
        if "type" not in data:
            raise ValueError("Checkpointer type must be specified")

        # Get appropriate subclass based on type
        checkpointer_type = data["type"]
        if checkpointer_type == CheckpointerType.MEMORY:
            from haive.core.persistence.memory import MemoryCheckpointerConfig

            return MemoryCheckpointerConfig(**data)
        if checkpointer_type == CheckpointerType.POSTGRES:
            from haive.core.persistence.postgres_config import (
                PostgresCheckpointerConfig,
            )

            return PostgresCheckpointerConfig(**data)
        raise ValueError(f"Unsupported checkpointer type: {checkpointer_type}")
