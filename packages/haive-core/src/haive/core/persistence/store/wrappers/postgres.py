# src/haive/core/persistence/store/wrappers/postgres.py
"""PostgreSQL store wrapper implementations."""

import logging

from langgraph.store.base import BaseStore
from langgraph.store.postgres import PostgresStore
from langgraph.store.postgres.aio import AsyncPostgresStore

from ..base import SerializableStoreWrapper
from ..connection import ConnectionManager
from ..embeddings import EmbeddingAdapter
from ..types import StoreType

logger = logging.getLogger(__name__)


class PostgresStoreWrapper(SerializableStoreWrapper):
    """Wrapper for LangGraph's PostgresStore with connection sharing.

    This wrapper provides persistent storage using PostgreSQL with
    support for connection pooling, semantic search, and proper
    resource management.
    """

    def _create_store(self) -> BaseStore:
        """Create PostgresStore instance."""
        # Get or create shared connection pool
        pool = ConnectionManager.get_or_create_sync_pool(
            self.config.connection_id,
            self.config.connection_params,
            self.config.pool_config,
        )

        # Prepare index config
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
            logger.info(
                f"Creating PostgresStore with semantic search for {self.config.connection_id}"
            )
            store = PostgresStore(pool, index=index_config)
        else:
            logger.info(
                f"Creating PostgresStore without semantic search for {self.config.connection_id}"
            )
            store = PostgresStore(pool)

        # Setup if needed
        if self.config.setup_on_init:
            try:
                store.setup()
                logger.info("PostgresStore tables initialized")
            except Exception as e:
                logger.warning(f"Store setup error (may be already initialized): {e}")

        return store

    async def _create_async_store(self) -> BaseStore:
        """Create sync store for async fallback."""
        # For sync postgres wrapper, just return sync store
        return self._create_store()


class AsyncPostgresStoreWrapper(SerializableStoreWrapper):
    """Wrapper for LangGraph's AsyncPostgresStore with connection sharing.

    This wrapper provides async persistent storage using PostgreSQL with
    support for connection pooling, semantic search, and proper
    resource management.
    """

    def _create_store(self) -> BaseStore:
        """Create sync store (fallback)."""
        # Change type temporarily to create sync store
        original_type = self.config.type
        self.config.type = StoreType.POSTGRES_SYNC

        wrapper = PostgresStoreWrapper(config=self.config)
        store = wrapper._create_store()

        # Restore type
        self.config.type = original_type
        return store

    async def _create_async_store(self) -> BaseStore:
        """Create AsyncPostgresStore instance."""
        # Get or create shared async connection pool
        pool = await ConnectionManager.get_or_create_async_pool(
            self.config.connection_id,
            self.config.connection_params,
            self.config.pool_config,
        )

        # Prepare index config
        index_config = None
        if self.config.embedding_provider:
            embed_func = EmbeddingAdapter.create_async_embedding_function(
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
            logger.info(
                f"Creating AsyncPostgresStore with semantic search for {self.config.connection_id}"
            )
            store = AsyncPostgresStore(pool, index=index_config)
        else:
            logger.info(
                f"Creating AsyncPostgresStore without semantic search for {self.config.connection_id}"
            )
            store = AsyncPostgresStore(pool)

        # Setup if needed
        if self.config.setup_on_init:
            try:
                await store.setup()
                logger.info("AsyncPostgresStore tables initialized")
            except Exception as e:
                logger.warning(
                    f"Async store setup error (may be already initialized): {e}"
                )

        return store
