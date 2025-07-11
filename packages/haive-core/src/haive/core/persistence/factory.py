# Factory functions for PostgreSQL checkpointer operations
import asyncio
import json
import logging
import random
import time
from typing import Any, Dict

# Check if PostgreSQL is available
try:
    from langgraph.checkpoint.postgres import ShallowPostgresSaver
    from langgraph.checkpoint.postgres.aio import AsyncShallowPostgresSaver

    from haive.core.persistence.postgres_saver_override import (
        AsyncPostgresSaverNoPreparedStatements as AsyncPostgresSaver,
    )
    from haive.core.persistence.postgres_saver_override import (
        PostgresSaverNoPreparedStatements as PostgresSaver,
    )

    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

from haive.core.persistence.postgres_config import PostgresCheckpointerConfig

logger = logging.getLogger(__name__)


def create_postgres_checkpointer(config: PostgresCheckpointerConfig) -> Any:
    """Create a PostgreSQL checkpointer with retry logic.

    Args:
        config: PostgreSQL checkpointer configuration

    Returns:
        A PostgresSaver instance or fallback MemorySaver
    """
    if not POSTGRES_AVAILABLE:
        logger.warning(
            "PostgreSQL dependencies not available, falling back to memory checkpointer"
        )
        from langgraph.checkpoint.memory import MemorySaver

        return MemorySaver()

    # Check if we already have a checkpointer for this config
    config_key = config.get_config_key()
    if config_key in PostgresCheckpointerConfig._sync_checkpointers:
        return PostgresCheckpointerConfig._sync_checkpointers[config_key]

    try:
        # Check if we have a pool for this config
        pool = None
        if config_key in PostgresCheckpointerConfig._sync_pools:
            pool = PostgresCheckpointerConfig._sync_pools[config_key]
        else:
            logger.info("Creating new PostgreSQL connection pool")

            # Get connection URI
            db_uri = config.get_connection_uri()

            # Create connection pool with retries
            for retry in range(config.max_retries):
                try:
                    from psycopg_pool import ConnectionPool

                    pool = ConnectionPool(
                        conninfo=db_uri,
                        min_size=config.min_pool_size,
                        max_size=config.max_pool_size,
                        kwargs={
                            "autocommit": config.auto_commit,
                            "prepare_threshold": config.prepare_threshold,
                            "connect_timeout": config.connect_timeout,
                        },
                        open=True,  # Explicitly open the pool
                    )
                    # Store in class cache
                    PostgresCheckpointerConfig._sync_pools[config_key] = pool
                    break
                except Exception as e:
                    if retry < config.max_retries - 1:
                        delay = config.retry_delay * (config.retry_backoff**retry)
                        if config.retry_jitter:
                            delay *= 0.5 + random.random()
                        logger.warning(
                            f"Connection attempt {retry+1} failed: {e}. Retrying in {delay:.2f}s"
                        )
                        time.sleep(delay)
                    else:
                        raise

        # Create appropriate PostgresSaver
        checkpointer = None
        checkpointer = (
            ShallowPostgresSaver(pool) if config.shallow_mode else PostgresSaver(pool)
        )

        # Initialize tables if needed
        if config.setup_needed:
            try:
                checkpointer.setup()
                config.setup_needed = False
            except Exception as e:
                logger.exception(f"Error setting up PostgreSQL tables: {e}")

        # Store in class cache
        PostgresCheckpointerConfig._sync_checkpointers[config_key] = checkpointer
        return checkpointer

    except Exception as e:
        logger.exception(f"Error creating PostgreSQL checkpointer: {e}")
        logger.warning("Falling back to memory checkpointer")
        from langgraph.checkpoint.memory import MemorySaver

        return MemorySaver()


async def acreate_postgres_checkpointer(config: PostgresCheckpointerConfig) -> Any:
    """Create an asynchronous PostgreSQL checkpointer with retry logic.

    Args:
        config: PostgreSQL checkpointer configuration

    Returns:
        An AsyncPostgresSaver instance or fallback MemorySaver
    """
    if not POSTGRES_AVAILABLE:
        logger.warning(
            "PostgreSQL dependencies not available, falling back to memory checkpointer"
        )
        from langgraph.checkpoint.memory import MemorySaver

        return MemorySaver()

    # Check if we already have an async checkpointer for this config
    config_key = config.get_config_key()
    if config_key in PostgresCheckpointerConfig._async_checkpointers:
        return PostgresCheckpointerConfig._async_checkpointers[config_key]

    try:
        # Check if we have an async pool for this config
        async_pool = None
        if config_key in PostgresCheckpointerConfig._async_pools:
            async_pool = PostgresCheckpointerConfig._async_pools[config_key]
        else:
            logger.info("Creating new PostgreSQL async connection pool")

            # Get connection URI
            db_uri = config.get_connection_uri()

            # Connection parameters
            conn_kwargs = {
                "autocommit": config.auto_commit,
                "prepare_threshold": config.prepare_threshold,
                "connect_timeout": config.connect_timeout,
            }

            # Create async pool with retries
            for retry in range(config.max_retries):
                try:
                    # Create pool
                    from psycopg_pool import AsyncConnectionPool

                    async_pool = AsyncConnectionPool(
                        conninfo=db_uri,
                        min_size=config.min_pool_size,
                        max_size=config.max_pool_size,
                        kwargs=conn_kwargs,
                        open=False,  # Don't open during init
                    )

                    # Explicitly open the pool
                    await async_pool.open()

                    # Store in class cache
                    PostgresCheckpointerConfig._async_pools[config_key] = async_pool
                    break
                except Exception as e:
                    if retry < config.max_retries - 1:
                        delay = config.retry_delay * (config.retry_backoff**retry)
                        if config.retry_jitter:
                            delay *= 0.5 + random.random()
                        logger.warning(
                            f"Async connection attempt {retry+1} failed: {e}. Retrying in {delay:.2f}s"
                        )
                        await asyncio.sleep(delay)
                    else:
                        raise

        # Create appropriate async checkpoint saver
        async_checkpointer = None
        if config.shallow_mode:
            async_checkpointer = AsyncShallowPostgresSaver(async_pool)
        else:
            async_checkpointer = AsyncPostgresSaver(async_pool)

        # Initialize tables if needed
        if config.setup_needed:
            try:
                await async_checkpointer.setup()
                config.setup_needed = False
            except Exception as e:
                logger.exception(
                    f"Error setting up PostgreSQL tables asynchronously: {e}"
                )

        # Store in class cache
        PostgresCheckpointerConfig._async_checkpointers[config_key] = async_checkpointer
        return async_checkpointer

    except Exception as e:
        logger.exception(f"Error creating async PostgreSQL checkpointer: {e}")
        logger.warning("Falling back to memory checkpointer")
        from langgraph.checkpoint.memory import MemorySaver

        return MemorySaver()


def register_postgres_thread(
    config: PostgresCheckpointerConfig,
    thread_id: str,
    metadata: dict[str, Any] | None = None,
) -> None:
    """Register a thread in the PostgreSQL database with retry logic.

    Args:
        config: PostgreSQL checkpointer configuration
        thread_id: Thread ID to register
        metadata: Optional metadata dict
    """
    if not POSTGRES_AVAILABLE:
        logger.debug("PostgreSQL not available, skipping thread registration")
        return

    try:
        # Create checkpointer if not already created
        checkpointer = create_postgres_checkpointer(config)

        # Skip if we got a MemorySaver fallback
        from langgraph.checkpoint.memory import MemorySaver

        if isinstance(checkpointer, MemorySaver):
            return

        # Ensure pool is usable
        pool = getattr(checkpointer, "conn", None)
        if pool is None:
            logger.warning("No connection pool available for thread registration")
            return

        # Ensure pool is open
        if hasattr(pool, "is_open") and callable(pool.is_open) and not pool.is_open():
            try:
                pool.open()
            except Exception as e:
                logger.exception(f"Could not open pool for thread registration: {e}")
                return

        # Register thread with retry mechanism
        for retry in range(config.max_retries):
            try:
                with pool.connection() as conn, conn.cursor() as cursor:
                    # Get threads table columns
                    cursor.execute(
                        """
                            SELECT EXISTS (
                                SELECT FROM information_schema.tables
                                WHERE table_name = 'threads'
                            );
                        """
                    )
                    table_exists = cursor.fetchone()[0]

                    # Create threads table if needed
                    if not table_exists:
                        cursor.execute(
                            """
                                CREATE TABLE IF NOT EXISTS threads (
                                    thread_id VARCHAR(255) PRIMARY KEY,
                                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                                    last_access TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                                    metadata JSONB DEFAULT '{}'::jsonb
                                );
                            """
                        )

                    # Check columns
                    cursor.execute(
                        """
                            SELECT column_name FROM information_schema.columns
                            WHERE table_name = 'threads';
                        """
                    )
                    columns = [row[0] for row in cursor.fetchall()]

                    # Convert metadata to JSON
                    metadata_json = "{}"
                    if metadata:
                        metadata_json = json.dumps(metadata)

                    # Insert thread with appropriate columns
                    if "metadata" in columns:
                        cursor.execute(
                            """
                                INSERT INTO threads (thread_name, metadata, last_access)
                                VALUES (%s, %s, CURRENT_TIMESTAMP)
                                ON CONFLICT (thread_name)
                                DO UPDATE SET
                                    last_access = CURRENT_TIMESTAMP,
                                    metadata = COALESCE(threads.metadata, '{}'::jsonb) || %s::jsonb
                            """,
                            (thread_id, metadata_json, metadata_json),
                        )
                    else:
                        cursor.execute(
                            """
                                INSERT INTO threads (thread_id, last_access)
                                VALUES (%s, CURRENT_TIMESTAMP)
                                ON CONFLICT (thread_id)
                                DO UPDATE SET last_access = CURRENT_TIMESTAMP
                            """,
                            (thread_id,),
                        )

                logger.info(f"Thread {thread_id} registered in PostgreSQL")
                break
            except Exception as e:
                if retry < config.max_retries - 1:
                    delay = config.retry_delay * (config.retry_backoff**retry)
                    if config.retry_jitter:
                        delay *= 0.5 + random.random()
                    logger.warning(
                        f"Thread registration attempt {retry+1} failed: {e}. Retrying in {delay:.2f}s"
                    )
                    time.sleep(delay)
                else:
                    logger.exception(f"All thread registration attempts failed: {e}")

    except Exception as e:
        logger.exception(f"Error in thread registration: {e}")


async def aregister_postgres_thread(
    config: PostgresCheckpointerConfig,
    thread_id: str,
    metadata: dict[str, Any] | None = None,
) -> None:
    """Asynchronously register a thread in the PostgreSQL database.

    Args:
        config: PostgreSQL checkpointer configuration
        thread_id: Thread ID to register
        metadata: Optional metadata dict
    """
    if not POSTGRES_AVAILABLE:
        logger.debug("PostgreSQL not available, skipping async thread registration")
        return

    try:
        # Create async checkpointer if not already created
        checkpointer = await acreate_postgres_checkpointer(config)

        # Skip if we got a MemorySaver fallback
        from langgraph.checkpoint.memory import MemorySaver

        if isinstance(checkpointer, MemorySaver):
            return

        # Get connection pool
        pool = getattr(checkpointer, "conn", None)
        if pool is None:
            logger.warning("No async connection pool available for thread registration")
            return

        # Register thread with retry mechanism
        for retry in range(config.max_retries):
            try:
                async with pool.connection() as conn, conn.cursor() as cursor:
                    # Check if threads table exists
                    await cursor.execute(
                        """
                            SELECT EXISTS (
                                SELECT FROM information_schema.tables
                                WHERE table_name = 'threads'
                            );
                        """
                    )
                    table_exists = (await cursor.fetchone())[0]

                    # Create threads table if needed
                    if not table_exists:
                        await cursor.execute(
                            """
                                CREATE TABLE IF NOT EXISTS threads (
                                    thread_id VARCHAR(255) PRIMARY KEY,
                                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                                    last_access TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                                    metadata JSONB DEFAULT '{}'::jsonb
                                );
                            """
                        )

                    # Get columns
                    await cursor.execute(
                        """
                            SELECT column_name FROM information_schema.columns
                            WHERE table_name = 'threads';
                        """
                    )
                    columns = [row[0] for row in await cursor.fetchall()]

                    # Convert metadata to JSON
                    metadata_json = "{}"
                    if metadata:
                        metadata_json = json.dumps(metadata)

                    # Insert thread with appropriate columns
                    if "metadata" in columns:
                        await cursor.execute(
                            """
                                INSERT INTO threads (thread_id, metadata, last_access)
                                VALUES (%s, %s, CURRENT_TIMESTAMP)
                                ON CONFLICT (thread_id)
                                DO UPDATE SET
                                    last_access = CURRENT_TIMESTAMP,
                                    metadata = COALESCE(threads.metadata, '{}'::jsonb) || %s::jsonb
                            """,
                            (thread_id, metadata_json, metadata_json),
                        )
                    else:
                        await cursor.execute(
                            """
                                INSERT INTO threads (thread_id, last_access)
                                VALUES (%s, CURRENT_TIMESTAMP)
                                ON CONFLICT (thread_id)
                                DO UPDATE SET last_access = CURRENT_TIMESTAMP
                            """,
                            (thread_id,),
                        )

                logger.info(
                    f"Thread {thread_id} registered asynchronously in PostgreSQL"
                )
                break
            except Exception as e:
                if retry < config.max_retries - 1:
                    delay = config.retry_delay * (config.retry_backoff**retry)
                    if config.retry_jitter:
                        delay *= 0.5 + random.random()
                    logger.warning(
                        f"Async thread registration attempt {retry+1} failed: {e}. Retrying in {delay:.2f}s"
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.exception(
                        f"All async thread registration attempts failed: {e}"
                    )

    except Exception as e:
        logger.exception(f"Error in async thread registration: {e}")


def put_postgres_checkpoint(
    config: PostgresCheckpointerConfig,
    runnable_config: dict[str, Any],
    data: Any,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Store a checkpoint in the PostgreSQL database with retry logic.

    Args:
        config: PostgreSQL checkpointer configuration
        runnable_config: Configuration with thread_id and optional checkpoint_id
        data: The checkpoint data to store
        metadata: Optional metadata to associate with the checkpoint

    Returns:
        Updated config with checkpoint_id
    """
    if not POSTGRES_AVAILABLE:
        logger.warning("PostgreSQL dependencies not available, checkpoint not stored")
        return runnable_config

    # Create checkpointer
    checkpointer = create_postgres_checkpointer(config)

    # Ensure config has required fields
    config_dict = config._ensure_config_fields(runnable_config)

    # Basic checkpoint structure
    checkpoint_data = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime()),
        "id": config_dict["configurable"].get("checkpoint_id", ""),
        "channel_values": data,
    }

    # Metadata structure expected by LangGraph
    checkpoint_metadata = metadata or {
        "source": "update",
        "step": 0,
        "writes": {},
        "parents": {},
    }

    # Channel versions (required by newer LangGraph API)
    channel_versions = {}

    # Try to store with retries
    for retry in range(config.max_retries):
        try:
            # Call the appropriate put method
            next_config = checkpointer.put(
                config_dict, checkpoint_data, checkpoint_metadata, channel_versions
            )

            # Return updated config
            return next_config
        except Exception as e:
            if retry < config.max_retries - 1:
                delay = config.retry_delay * (config.retry_backoff**retry)
                if config.retry_jitter:
                    delay *= 0.5 + random.random()
                logger.warning(
                    f"Checkpoint storage attempt {retry+1} failed: {e}. Retrying in {delay:.2f}s"
                )
                time.sleep(delay)
            else:
                logger.exception(f"All checkpoint storage attempts failed: {e}")
                return config_dict

    # Should not reach here
    return config_dict


async def aput_postgres_checkpoint(
    config: PostgresCheckpointerConfig,
    runnable_config: dict[str, Any],
    data: Any,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Asynchronously store a checkpoint in the PostgreSQL database with retry logic.

    Args:
        config: PostgreSQL checkpointer configuration
        runnable_config: Configuration with thread_id and optional checkpoint_id
        data: The checkpoint data to store
        metadata: Optional metadata to associate with the checkpoint

    Returns:
        Updated config with checkpoint_id
    """
    if not POSTGRES_AVAILABLE:
        logger.warning(
            "PostgreSQL dependencies not available, async checkpoint not stored"
        )
        return runnable_config

    # Create async checkpointer
    checkpointer = await acreate_postgres_checkpointer(config)

    # Ensure config has required fields
    config_dict = config._ensure_config_fields(runnable_config)

    # Log complete config for debugging
    logger.debug(
        f"Writing checkpoint with config: {json.dumps(config_dict, default=str)}"
    )
    logger.debug(f"Data type: {type(data)}, Data preview: {str(data)[:100]}")

    # Skip for MemorySaver fallback
    from langgraph.checkpoint.memory import MemorySaver

    if isinstance(checkpointer, MemorySaver):
        logger.info("Using MemorySaver fallback for checkpoint storage")
        return checkpointer.put(config_dict, {"channel_values": data})

    # Basic checkpoint structure
    checkpoint_data = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime()),
        "id": config_dict["configurable"].get("checkpoint_id", ""),
        "v": 1,  # Make sure version is included
        "channel_values": data,
    }

    # Metadata structure expected by LangGraph
    checkpoint_metadata = metadata or {
        "source": "update",
        "step": 0,
        "writes": {},
        "parents": {},
    }

    # Channel versions (required by newer LangGraph API)
    channel_versions = {}

    # Try to store with retries
    for retry in range(config.max_retries):
        try:
            # Call the appropriate aput method
            if hasattr(checkpointer, "aput") and callable(checkpointer.aput):
                try:
                    # Log exactly what we're passing to aput
                    logger.debug(
                        f"Calling aput with config: {json.dumps(config_dict, default=str)}"
                    )
                    logger.debug(
                        f"Checkpoint data: {json.dumps(checkpoint_data, default=str)[:200]}"
                    )

                    next_config = await checkpointer.aput(
                        config_dict,
                        checkpoint_data,
                        checkpoint_metadata,
                        channel_versions,
                    )

                    # Log the returned config
                    logger.debug(
                        f"aput returned config: {json.dumps(next_config, default=str)}"
                    )
                    return next_config
                except TypeError as te:
                    logger.exception(f"Type error in aput: {te}")
                    # Try with simpler arguments if TypeError (could be API mismatch)
                    logger.info("Trying simplified aput call")
                    next_config = await checkpointer.aput(
                        config_dict, {"channel_values": data}
                    )
                    return next_config
            else:
                # Fallback to sync put for MemorySaver
                logger.info("No aput method, using synchronous put")
                return checkpointer.put(config_dict, {"channel_values": data})
        except Exception as e:
            if retry < config.max_retries - 1:
                delay = config.retry_delay * (config.retry_backoff**retry)
                if config.retry_jitter:
                    delay *= 0.5 + random.random()
                logger.warning(
                    f"Async checkpoint storage attempt {retry+1} failed: {e!s}. Retrying in {delay:.2f}s"
                )
                await asyncio.sleep(delay)
            else:
                logger.exception(f"All async checkpoint storage attempts failed: {e!s}")
                return config_dict

    # Should not reach here
    return config_dict


def get_postgres_checkpoint(
    config: PostgresCheckpointerConfig, runnable_config: dict[str, Any]
) -> Any | None:
    """Retrieve a checkpoint from the PostgreSQL database with retry logic.

    Args:
        config: PostgreSQL checkpointer configuration
        runnable_config: Configuration with thread_id and optional checkpoint_id

    Returns:
        The checkpoint data if found, None otherwise
    """
    if not POSTGRES_AVAILABLE:
        logger.warning(
            "PostgreSQL dependencies not available, checkpoint not retrieved"
        )
        return None

    # Create checkpointer
    checkpointer = create_postgres_checkpointer(config)

    # Ensure config has required fields
    config_dict = config._ensure_config_fields(runnable_config)

    # Try to retrieve with retries
    for retry in range(config.max_retries):
        try:
            # Get the checkpoint
            result = checkpointer.get(config_dict)

            # Extract channel values if present
            if result is not None and "channel_values" in result:
                return result["channel_values"]

            return result
        except Exception as e:
            if retry < config.max_retries - 1:
                delay = config.retry_delay * (config.retry_backoff**retry)
                if config.retry_jitter:
                    delay *= 0.5 + random.random()
                logger.warning(
                    f"Checkpoint retrieval attempt {retry+1} failed: {e}. Retrying in {delay:.2f}s"
                )
                time.sleep(delay)
            else:
                logger.exception(f"All checkpoint retrieval attempts failed: {e}")
                return None

    # Should not reach here
    return None


async def aget_postgres_checkpoint(
    config: PostgresCheckpointerConfig, runnable_config: dict[str, Any]
) -> Any | None:
    """Asynchronously retrieve a checkpoint from the PostgreSQL database with retry logic.

    Args:
        config: PostgreSQL checkpointer configuration
        runnable_config: Configuration with thread_id and optional checkpoint_id

    Returns:
        The checkpoint data if found, None otherwise
    """
    if not POSTGRES_AVAILABLE:
        logger.warning(
            "PostgreSQL dependencies not available, async checkpoint not retrieved"
        )
        return None

    # Create async checkpointer
    checkpointer = await acreate_postgres_checkpointer(config)

    # Ensure config has required fields
    config_dict = config._ensure_config_fields(runnable_config)

    # Log complete config for debugging
    logger.debug(
        f"Reading checkpoint with config: {json.dumps(config_dict, default=str)}"
    )

    # Skip for MemorySaver fallback
    from langgraph.checkpoint.memory import MemorySaver

    if isinstance(checkpointer, MemorySaver):
        logger.info("Using MemorySaver fallback for checkpoint retrieval")
        result = checkpointer.get(config_dict)
        if result and "channel_values" in result:
            return result["channel_values"]
        return result

    # Try to retrieve with retries
    for retry in range(config.max_retries):
        try:
            # Get the checkpoint asynchronously
            if hasattr(checkpointer, "aget") and callable(checkpointer.aget):
                logger.debug(
                    f"Using async aget with config: {json.dumps(config_dict, default=str)}"
                )
                result = await checkpointer.aget(config_dict)

                # Log the result structure
                if result is not None:
                    logger.debug(
                        f"aget result type: {type(result)}, keys: {result.keys() if isinstance(result, dict) else 'not a dict'}"
                    )
                else:
                    logger.warning("aget returned None")

                # Extract channel values if present
                if result is not None and "channel_values" in result:
                    return result["channel_values"]

                return result
            # Try with aget_tuple
            if hasattr(checkpointer, "aget_tuple") and callable(
                checkpointer.aget_tuple
            ):
                logger.debug("Trying aget_tuple method")
                tuple_result = await checkpointer.aget_tuple(config_dict)
                if tuple_result and hasattr(tuple_result, "checkpoint"):
                    result = tuple_result.checkpoint
                    if result and "channel_values" in result:
                        return result["channel_values"]
                    return result

            # Fallback to sync get for MemorySaver
            logger.info("No async get methods, using synchronous get")
            result = checkpointer.get(config_dict)
            if result and "channel_values" in result:
                return result["channel_values"]
            return result
        except Exception as e:
            if retry < config.max_retries - 1:
                delay = config.retry_delay * (config.retry_backoff**retry)
                if config.retry_jitter:
                    delay *= 0.5 + random.random()
                logger.warning(
                    f"Async checkpoint retrieval attempt {retry+1} failed: {e!s}. Retrying in {delay:.2f}s"
                )
                await asyncio.sleep(delay)
            else:
                logger.exception(
                    f"All async checkpoint retrieval attempts failed: {e!s}"
                )
                return None

    # Should not reach here
    return None


def close_postgres_pool(config: PostgresCheckpointerConfig) -> None:
    """Close any connection pools created by a specific configuration.

    Args:
        config: PostgreSQL checkpointer configuration
    """
    config_key = config.get_config_key()

    # Close sync pool if it exists
    if config_key in PostgresCheckpointerConfig._sync_pools:
        pool = PostgresCheckpointerConfig._sync_pools[config_key]
        try:
            if hasattr(pool, "is_open") and pool.is_open():
                logger.info(f"Closing PostgreSQL connection pool for {config_key}")
                pool.close()

            # Remove from caches
            PostgresCheckpointerConfig._sync_pools.pop(config_key, None)
            PostgresCheckpointerConfig._sync_checkpointers.pop(config_key, None)
        except Exception as e:
            logger.exception(f"Error closing PostgreSQL connection pool: {e}")


async def aclose_postgres_pool(config: PostgresCheckpointerConfig) -> None:
    """Asynchronously close any connection pools created by a specific configuration.

    Args:
        config: PostgreSQL checkpointer configuration
    """
    config_key = config.get_config_key()

    # Close async pool if it exists
    if config_key in PostgresCheckpointerConfig._async_pools:
        pool = PostgresCheckpointerConfig._async_pools[config_key]
        try:
            is_open = False
            # Check if pool is open
            if hasattr(pool, "is_closed"):
                is_open = not await pool.is_closed()
            elif hasattr(pool, "_opened"):
                is_open = pool._opened

            if is_open:
                logger.info(
                    f"Closing async PostgreSQL connection pool for {config_key}"
                )
                await pool.close()

            # Remove from caches
            PostgresCheckpointerConfig._async_pools.pop(config_key, None)
            PostgresCheckpointerConfig._async_checkpointers.pop(config_key, None)
        except Exception as e:
            logger.exception(f"Error closing async PostgreSQL connection pool: {e}")


def close_all_postgres_pools() -> None:
    """Close all PostgreSQL connection pools."""
    # Close sync pools
    for key, pool in PostgresCheckpointerConfig._sync_pools.items():
        try:
            if hasattr(pool, "is_open") and pool.is_open():
                logger.info(f"Closing PostgreSQL connection pool for {key}")
                pool.close()
        except Exception as e:
            logger.exception(f"Error closing PostgreSQL connection pool: {e}")

    # Clear caches
    PostgresCheckpointerConfig._sync_pools.clear()
    PostgresCheckpointerConfig._sync_checkpointers.clear()


async def aclose_all_postgres_pools() -> None:
    """Asynchronously close all PostgreSQL connection pools."""
    # Close async pools
    for key, pool in PostgresCheckpointerConfig._async_pools.items():
        try:
            is_open = False
            # Check if pool is open
            if hasattr(pool, "is_closed"):
                is_open = not await pool.is_closed()
            elif hasattr(pool, "_opened"):
                is_open = pool._opened

            if is_open:
                logger.info(f"Closing async PostgreSQL connection pool for {key}")
                await pool.close()
        except Exception as e:
            logger.exception(f"Error closing async PostgreSQL connection pool: {e}")

    # Clear caches
    PostgresCheckpointerConfig._async_pools.clear()
    PostgresCheckpointerConfig._async_checkpointers.clear()
