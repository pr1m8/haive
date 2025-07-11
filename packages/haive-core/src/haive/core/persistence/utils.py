"""Utility functions for the Haive persistence system.

This module provides helper functions for working with checkpointers and their
associated resources. It includes utilities for connection pool management,
serialization/deserialization of metadata, and other common operations needed
across different persistence implementations.

The utilities are designed to be used by the persistence system internals and
generally aren't intended to be used directly by application code. They provide
consistent behavior across different checkpointer implementations and handle
edge cases and error conditions gracefully.
"""

import json
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def serialize_metadata(metadata: dict[str, Any]) -> str:
    """Serialize metadata dictionary to JSON string.

    Args:
        metadata: Dictionary containing metadata to serialize

    Returns:
        str: JSON string representation of the metadata
    """
    return json.dumps(metadata)


def deserialize_metadata(metadata_str: str) -> dict[str, Any]:
    """Deserialize metadata from JSON string to dictionary.

    Args:
        metadata_str: JSON string containing serialized metadata

    Returns:
        Dict[str, Any]: Deserialized metadata dictionary
    """
    return json.loads(metadata_str) if metadata_str else {}


def ensure_pool_open(checkpointer: Any) -> Any | None:
    """Ensure that a PostgreSQL connection pool is properly opened.

    This function checks if a checkpointer has an associated connection pool
    and ensures that it's properly opened. It handles different pool
    implementations and versions, checking appropriate attributes and calling
    the open method if needed.

    The function is used to ensure that connection pools are ready for use
    before attempting database operations, preventing errors from closed
    or unopened pools.

    Args:
        checkpointer: The checkpointer instance to check for a connection pool

    Returns:
        Optional[Any]: The opened connection pool if one was found and opened,
            None otherwise

    Note:
        This function gracefully handles the case where psycopg_pool is not
        available, making it safe to call even if the PostgreSQL dependencies
        are not installed.
    """
    if not hasattr(checkpointer, "conn"):
        return None

    conn = checkpointer.conn

    try:
        from psycopg_pool import ConnectionPool

        if isinstance(conn, ConnectionPool):
            # Check if opened using the _opened attribute
            is_open = getattr(conn, "_opened", False)
            if not is_open:
                logger.info("Opening PostgreSQL connection pool")
                conn.open()
                logger.info("Pool opened successfully")
            return conn
    except ImportError:
        logger.debug("psycopg_pool not available")

    # Make sure setup is called
    if hasattr(checkpointer, "setup"):
        try:
            checkpointer.setup()
        except Exception as e:
            logger.exception(f"Error setting up checkpointer: {e}")

    return None


async def ensure_async_pool_open(checkpointer: Any) -> Any | None:
    """Ensure that an async PostgreSQL connection pool is properly opened.

    This asynchronous function checks if an async checkpointer has an associated
    connection pool and ensures that it's properly opened. It handles different
    async pool implementations and versions, checking appropriate attributes and
    calling the async open method if needed.

    The function is particularly important for async contexts, where proper
    connection management is critical for maintaining good performance and
    resource utilization. It prevents errors from closed or unopened pools
    in async code.

    Args:
        checkpointer: The async checkpointer instance to check for a connection pool

    Returns:
        Optional[Any]: The opened async connection pool if one was found and
            opened, None otherwise

    Note:
        This function gracefully handles the case where the async PostgreSQL
        dependencies are not available, making it safe to call even if the
        async database modules are not installed.

    Example:
        ```python
        async def prepare_checkpointer(checkpointer):
            # Ensure the pool is open before using it
            pool = await ensure_async_pool_open(checkpointer)
            if pool:
                print("Pool is ready for use")
            # Continue with checkpointer operations...
        ```
    """
    opened_pool = None
    try:
        # Check for connection pools in the checkpointer
        if hasattr(checkpointer, "conn"):
            conn = checkpointer.conn

            # Import here to avoid dependency issues
            try:
                from psycopg_pool.base import AsyncPool

                # Check if it's an async pool
                if isinstance(conn, AsyncPool):
                    # Check if the pool is already open
                    try:
                        if hasattr(conn, "is_open"):
                            is_open = conn.is_open()
                        else:
                            # Older versions might not have is_open()
                            is_open = getattr(conn, "_opened", False)

                        # Open the pool if needed
                        if not is_open:
                            logger.info("Opening async PostgreSQL connection pool")
                            try:
                                await conn.open()
                                opened_pool = conn
                                logger.info("Successfully opened async pool")
                            except Exception as e:
                                logger.exception(f"Error opening async pool: {e}")
                    except Exception as e:
                        logger.exception(f"Error checking if async pool is open: {e}")
            except ImportError:
                logger.debug("psycopg_pool AsyncPool not available")

        # Additional check for other types of pools or connections
        if not opened_pool and hasattr(checkpointer, "setup"):
            # If the checkpointer has a setup method but no connection was found,
            # just make sure tables are set up
            logger.debug("No async pool found but checkpointer has setup method")
            try:
                await checkpointer.setup()
            except Exception as e:
                logger.exception(f"Error setting up async checkpointer: {e}")

    except Exception as e:
        logger.exception(f"Error ensuring async pool is open: {e}")

    return opened_pool


# In utils.py
def register_thread(
    checkpointer: Any, thread_id: str, metadata: dict[str, Any] | None = None
) -> bool:
    """Register a thread in the PostgreSQL database if needed."""
    try:
        if hasattr(checkpointer, "conn"):
            pool = checkpointer.conn
            if pool:
                # Ensure connection pool is usable
                ensure_pool_open(checkpointer)

                # Register the thread
                with pool.connection() as conn, conn.cursor() as cursor:
                    # Check if threads table exists
                    cursor.execute(
                        """
                            SELECT EXISTS (
                                SELECT FROM information_schema.tables
                                WHERE table_name = 'threads'
                            );
                        """
                    )
                    table_exists = cursor.fetchone()[0]

                    if not table_exists:
                        logger.debug("Creating threads table")
                        cursor.execute(
                            """
                                CREATE TABLE IF NOT EXISTS threads (
                                    thread_id VARCHAR(255) PRIMARY KEY,
                                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                                    last_access TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                                    metadata JSONB DEFAULT '{}'::jsonb,
                                    user_id VARCHAR(255)
                                );
                            """
                        )

                    # Convert metadata to JSON string first
                    import json

                    metadata_json = json.dumps(metadata) if metadata else "{}"

                    # Insert the thread if not exists, or update last_access
                    cursor.execute(
                        """
                            INSERT INTO threads (thread_id, last_access, metadata)
                            VALUES (%s, CURRENT_TIMESTAMP, %s::jsonb)
                            ON CONFLICT (thread_id)
                            DO UPDATE SET last_access = CURRENT_TIMESTAMP, metadata = %s::jsonb
                        """,
                        (thread_id, metadata_json, metadata_json),
                    )

                    logger.info(f"Thread {thread_id} registered/updated in PostgreSQL")
                    return True
    except Exception as e:
        logger.warning(f"Error registering thread: {e}")

    return False


async def register_thread_async(
    checkpointer: Any, thread_id: str, metadata: dict[str, Any] | None = None
) -> bool:
    """Register a thread in the PostgreSQL database asynchronously."""
    if not hasattr(checkpointer, "conn"):
        return False

    try:
        import json

        metadata_json = json.dumps(metadata) if metadata else "{}"

        async with checkpointer.conn.connection() as conn, conn.cursor() as cursor:
            # Check if table exists
            await cursor.execute(
                """
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables
                        WHERE table_name = 'threads'
                    );
                """
            )
            table_exists = (await cursor.fetchone())[0]

            if not table_exists:
                await cursor.execute(
                    """
                        CREATE TABLE IF NOT EXISTS threads (
                            thread_id VARCHAR(255) PRIMARY KEY,
                            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                            last_access TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                            metadata JSONB DEFAULT '{}'::jsonb,
                            user_id VARCHAR(255)
                        );
                    """
                )

            # Use parameterized query with proper JSONB handling
            await cursor.execute(
                """
                    INSERT INTO threads (thread_id, last_access, metadata)
                    VALUES (%s, CURRENT_TIMESTAMP, %s::jsonb)
                    ON CONFLICT (thread_id)
                    DO UPDATE SET last_access = CURRENT_TIMESTAMP, metadata = %s::jsonb
                """,
                (thread_id, metadata_json, metadata_json),
            )

            logger.info(f"Thread {thread_id} registered/updated in PostgreSQL (async)")
            return True
    except Exception as e:
        logger.warning(f"Error registering thread asynchronously: {e}")

    return False
