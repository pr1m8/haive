# src/haive/core/persistence/store/factory.py
"""Store factory for creating store instances."""

import logging
from contextlib import asynccontextmanager, contextmanager
from typing import Any, Dict, Optional, Union

from .base import SerializableStoreWrapper
from .types import StoreConfig, StoreType
from .wrappers.memory import MemoryStoreWrapper
from .wrappers.postgres import AsyncPostgresStoreWrapper, PostgresStoreWrapper

logger = logging.getLogger(__name__)


class StoreFactory:
    """Factory for creating store instances."""

    @staticmethod
    def create(config: Union[StoreConfig, Dict[str, Any]]) -> SerializableStoreWrapper:
        """Create a store wrapper from configuration.

        Args:
            config: Store configuration

        Returns:
            Store wrapper instance
        """
        # Convert dict to config if needed
        if isinstance(config, dict):
            config = StoreConfig(**config)

        # Create appropriate wrapper
        if config.type == StoreType.MEMORY:
            return MemoryStoreWrapper(config=config)
        elif config.type == StoreType.POSTGRES_SYNC:
            return PostgresStoreWrapper(config=config)
        elif config.type == StoreType.POSTGRES_ASYNC:
            return AsyncPostgresStoreWrapper(config=config)
        else:
            raise ValueError(f"Unknown store type: {config.type}")

    @staticmethod
    @contextmanager
    def create_with_lifecycle(config: Union[StoreConfig, Dict[str, Any]]):
        """Create store with lifecycle management.

        Args:
            config: Store configuration

        Yields:
            Store wrapper instance
        """
        store = StoreFactory.create(config)
        try:
            yield store
        finally:
            # Cleanup if needed
            pass

    @staticmethod
    @asynccontextmanager
    async def create_async_with_lifecycle(config: Union[StoreConfig, Dict[str, Any]]):
        """Create async store with lifecycle management.

        Args:
            config: Store configuration

        Yields:
            Store wrapper instance
        """
        store = StoreFactory.create(config)
        try:
            yield store
        finally:
            # Cleanup if needed
            pass


# Convenience functions
def create_store(
    store_type: Union[str, StoreType] = StoreType.MEMORY, **kwargs
) -> SerializableStoreWrapper:
    """Create a store with simplified parameters.

    Args:
        store_type: Type of store
        **kwargs: Additional parameters

    Returns:
        Store wrapper instance
    """
    if isinstance(store_type, str):
        store_type = StoreType(store_type)

    # Handle common parameters
    config_dict = {"type": store_type}

    # Connection parameters
    if "host" in kwargs:
        config_dict["connection_params"] = {
            "host": kwargs.pop("host"),
            "port": kwargs.pop("port", 5432),
            "database": kwargs.pop("database", "postgres"),
            "user": kwargs.pop("user", "postgres"),
            "password": kwargs.pop("password", "postgres"),
        }

    # Embedding parameters
    if "embedding_provider" in kwargs:
        config_dict["embedding_provider"] = kwargs.pop("embedding_provider")
        config_dict["embedding_dims"] = kwargs.pop("embedding_dims", 1536)
        config_dict["embedding_fields"] = kwargs.pop("embedding_fields", None)

    # Add remaining kwargs
    config_dict.update(kwargs)

    config = StoreConfig(**config_dict)
    return StoreFactory.create(config)
