# src/haive/core/persistence/store/wrappers/memory.py
"""In-memory store wrapper implementation."""

import logging
from typing import Any, Dict, Optional

from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore

from ..base import SerializableStoreWrapper
from ..embeddings import EmbeddingAdapter

logger = logging.getLogger(__name__)


class MemoryStoreWrapper(SerializableStoreWrapper):
    """Wrapper for LangGraph's InMemoryStore with serialization support.

    This wrapper provides an in-memory store that's perfect for development
    and testing. It supports semantic search when configured with embeddings.

    Note: Data is lost when the process ends.
    """

    def _create_store(self) -> BaseStore:
        """Create InMemoryStore instance."""
        # Prepare index config if embeddings are configured
        index_config = None
        if self.config.embedding_provider:
            embed_func = EmbeddingAdapter.create_embedding_function(
                self.config.embedding_provider, self.config.embedding_dims or 1536
            )

            if embed_func:
                index_config = {
                    "embed": embed_func,
                    "dims": self.config.embedding_dims or 1536,
                }

                if self.config.embedding_fields:
                    index_config["fields"] = self.config.embedding_fields

        # Create store
        if index_config:
            logger.info("Creating InMemoryStore with semantic search")
            return InMemoryStore(index=index_config)
        else:
            logger.info("Creating InMemoryStore without semantic search")
            return InMemoryStore()

    async def _create_async_store(self) -> BaseStore:
        """Create async InMemoryStore (same as sync for memory)."""
        return self._create_store()
