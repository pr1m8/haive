# src/haive/core/persistence/store/base.py
"""Base store wrapper for LangGraph stores with serialization support.

This module provides the base class for all store wrappers, ensuring
consistent behavior, serialization support, and proper lifecycle management.
"""

import logging
import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union

from langgraph.store.base import BaseStore
from pydantic import BaseModel, Field, PrivateAttr

from .connection import ConnectionManager
from .embeddings import EmbeddingAdapter
from .types import StoreConfig, StoreType

logger = logging.getLogger(__name__)


class SerializableStoreWrapper(BaseModel, ABC):
    """Base wrapper for LangGraph stores with serialization support.

    This abstract base class provides:
    - Serialization support for store configurations
    - Connection lifecycle management
    - Embedding integration
    - Namespace prefixing
    - Proper cleanup on deletion

    All store implementations should inherit from this class.
    """

    # Configuration (serialized)
    config: StoreConfig = Field(description="Store configuration")

    # Runtime state (not serialized)
    _store: Optional[BaseStore] = PrivateAttr(default=None)
    _initialized: bool = PrivateAttr(default=False)

    class Config:
        """Pydantic configuration."""

        arbitrary_types_allowed = True

    def __init__(self, **data):
        """Initialize store wrapper."""
        super().__init__(**data)
        # Generate connection ID if not provided
        if not self.config.connection_id:
            self.config.connection_id = f"{self.config.type}_{uuid.uuid4().hex[:8]}"

    @abstractmethod
    def _create_store(self) -> BaseStore:
        """Create the underlying LangGraph store.

        Returns:
            LangGraph store instance
        """
        pass

    @abstractmethod
    async def _create_async_store(self) -> BaseStore:
        """Create the underlying async LangGraph store.

        Returns:
            Async LangGraph store instance
        """
        pass

    def get_store(self) -> BaseStore:
        """Get or create the underlying store.

        Returns:
            LangGraph store instance
        """
        if not self._initialized or not self._store:
            self._store = self._create_store()
            self._initialized = True
        return self._store

    async def get_async_store(self) -> BaseStore:
        """Get or create the underlying async store.

        Returns:
            Async LangGraph store instance
        """
        if not self._initialized or not self._store:
            self._store = await self._create_async_store()
            self._initialized = True
        return self._store

    def _apply_namespace_prefix(self, namespace: Tuple[str, ...]) -> Tuple[str, ...]:
        """Apply namespace prefix if configured.

        Args:
            namespace: Original namespace tuple

        Returns:
            Namespace with prefix applied
        """
        if self.config.namespace_prefix:
            return (self.config.namespace_prefix,) + namespace
        return namespace

    # Synchronous methods
    def put(self, namespace: Tuple[str, ...], key: str, value: Dict[str, Any]) -> None:
        """Store a value."""
        store = self.get_store()
        namespace = self._apply_namespace_prefix(namespace)
        store.put(namespace, key, value)

    def get(self, namespace: Tuple[str, ...], key: str) -> Optional[Dict[str, Any]]:
        """Retrieve a value."""
        store = self.get_store()
        namespace = self._apply_namespace_prefix(namespace)
        return store.get(namespace, key)

    def delete(self, namespace: Tuple[str, ...], key: str) -> None:
        """Delete a value."""
        store = self.get_store()
        namespace = self._apply_namespace_prefix(namespace)
        store.delete(namespace, key)

    def search(
        self,
        namespace: Tuple[str, ...],
        query: str,
        limit: int = 10,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Any]:
        """Search for values using semantic similarity."""
        store = self.get_store()
        namespace = self._apply_namespace_prefix(namespace)

        if hasattr(store, "search"):
            return store.search(namespace, query=query, limit=limit, filter=filter)
        else:
            logger.warning(f"Store {type(store).__name__} doesn't support search")
            return []

    # Asynchronous methods
    async def aput(
        self, namespace: Tuple[str, ...], key: str, value: Dict[str, Any]
    ) -> None:
        """Async store a value."""
        store = await self.get_async_store()
        namespace = self._apply_namespace_prefix(namespace)

        if hasattr(store, "aput"):
            await store.aput(namespace, key, value)
        else:
            # Fallback to sync
            store.put(namespace, key, value)

    async def aget(
        self, namespace: Tuple[str, ...], key: str
    ) -> Optional[Dict[str, Any]]:
        """Async retrieve a value."""
        store = await self.get_async_store()
        namespace = self._apply_namespace_prefix(namespace)

        if hasattr(store, "aget"):
            return await store.aget(namespace, key)
        else:
            # Fallback to sync
            return store.get(namespace, key)

    async def adelete(self, namespace: Tuple[str, ...], key: str) -> None:
        """Async delete a value."""
        store = await self.get_async_store()
        namespace = self._apply_namespace_prefix(namespace)

        if hasattr(store, "adelete"):
            await store.adelete(namespace, key)
        else:
            # Fallback to sync
            store.delete(namespace, key)

    async def asearch(
        self,
        namespace: Tuple[str, ...],
        query: str,
        limit: int = 10,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Any]:
        """Async search for values using semantic similarity."""
        store = await self.get_async_store()
        namespace = self._apply_namespace_prefix(namespace)

        if hasattr(store, "asearch"):
            return await store.asearch(
                namespace, query=query, limit=limit, filter=filter
            )
        elif hasattr(store, "search"):
            # Fallback to sync
            return store.search(namespace, query=query, limit=limit, filter=filter)
        else:
            logger.warning(f"Store {type(store).__name__} doesn't support search")
            return []

    # Serialization
    def __reduce__(self):
        """Support for pickle serialization."""
        return (self.__class__, (), self.config.model_dump())

    def __setstate__(self, state):
        """Restore from pickle."""
        self.config = StoreConfig(**state)
        self._store = None
        self._initialized = False

    # Cleanup
    def __del__(self):
        """Cleanup when wrapper is deleted."""
        # Note: Connection pools are managed centrally
        # and not closed here to allow sharing
        pass
