# src/haive/core/persistence/store/connection.py
"""Connection management for shared database connections.

This module provides centralized connection pool management to ensure
efficient resource usage and prevent connection exhaustion.
"""

import asyncio
import logging
import threading
from contextlib import asynccontextmanager, contextmanager
from typing import Any, Dict, Optional, Union

logger = logging.getLogger(__name__)

# Global connection registries
_sync_connections: Dict[str, Any] = {}
_async_connections: Dict[str, Any] = {}
_sync_lock = threading.Lock()
_async_lock = asyncio.Lock()


class ConnectionManager:
    """Manages shared connections and pools for stores.

    This class ensures that stores with the same connection_id share
    the same connection pool, preventing resource exhaustion and
    improving performance.
    """

    @staticmethod
    def get_or_create_sync_pool(
        connection_id: str,
        connection_params: Dict[str, Any],
        pool_config: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Get or create a synchronous connection pool.

        Args:
            connection_id: Unique identifier for the connection
            connection_params: Connection parameters
            pool_config: Pool configuration

        Returns:
            Connection pool instance
        """
        with _sync_lock:
            if connection_id in _sync_connections:
                logger.debug(f"Reusing existing sync pool for {connection_id}")
                return _sync_connections[connection_id]

            # Create new pool
            from psycopg_pool import ConnectionPool

            # Build connection string
            conn_str = ConnectionManager._build_postgres_uri(connection_params)

            # Create pool
            pool_config = pool_config or {}
            pool = ConnectionPool(
                conninfo=conn_str,
                min_size=pool_config.get("min_size", 1),
                max_size=pool_config.get("max_size", 10),
                kwargs={
                    "autocommit": True,
                    "prepare_threshold": None,  # Disable prepared statements
                },
                open=True,
            )

            _sync_connections[connection_id] = pool
            logger.info(f"Created new sync pool for {connection_id}")
            return pool

    @staticmethod
    async def get_or_create_async_pool(
        connection_id: str,
        connection_params: Dict[str, Any],
        pool_config: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Get or create an asynchronous connection pool.

        Args:
            connection_id: Unique identifier for the connection
            connection_params: Connection parameters
            pool_config: Pool configuration

        Returns:
            Async connection pool instance
        """
        async with _async_lock:
            if connection_id in _async_connections:
                logger.debug(f"Reusing existing async pool for {connection_id}")
                return _async_connections[connection_id]

            # Create new pool
            from psycopg_pool import AsyncConnectionPool

            # Build connection string
            conn_str = ConnectionManager._build_postgres_uri(connection_params)

            # Create pool
            pool_config = pool_config or {}
            pool = AsyncConnectionPool(
                conninfo=conn_str,
                min_size=pool_config.get("min_size", 1),
                max_size=pool_config.get("max_size", 10),
                kwargs={
                    "autocommit": True,
                    "prepare_threshold": None,  # Disable prepared statements
                },
            )

            await pool.open()

            _async_connections[connection_id] = pool
            logger.info(f"Created new async pool for {connection_id}")
            return pool

    @staticmethod
    def _build_postgres_uri(params: Dict[str, Any]) -> str:
        """Build PostgreSQL connection URI."""
        import urllib.parse

        host = params.get("host", "localhost")
        port = params.get("port", 5432)
        database = params.get("database", "postgres")
        user = params.get("user", "postgres")
        password = params.get("password", "postgres")

        encoded_pass = urllib.parse.quote_plus(str(password))
        base_uri = f"postgresql://{user}:{encoded_pass}@{host}:{port}/{database}"

        # Add optional parameters
        extra_params = []
        for key in ["sslmode", "connect_timeout", "application_name"]:
            if key in params:
                extra_params.append(f"{key}={params[key]}")

        if extra_params:
            return f"{base_uri}?{'&'.join(extra_params)}"
        return base_uri

    @staticmethod
    def close_sync_pool(connection_id: str) -> None:
        """Close and remove a sync connection pool."""
        with _sync_lock:
            if connection_id in _sync_connections:
                pool = _sync_connections[connection_id]
                try:
                    pool.close()
                    logger.info(f"Closed sync pool for {connection_id}")
                except Exception as e:
                    logger.error(f"Error closing sync pool: {e}")
                del _sync_connections[connection_id]

    @staticmethod
    async def close_async_pool(connection_id: str) -> None:
        """Close and remove an async connection pool."""
        async with _async_lock:
            if connection_id in _async_connections:
                pool = _async_connections[connection_id]
                try:
                    await pool.close()
                    logger.info(f"Closed async pool for {connection_id}")
                except Exception as e:
                    logger.error(f"Error closing async pool: {e}")
                del _async_connections[connection_id]
