# src/haive/core/engine/agent/persistence/postgres_config.py

import json
import logging
import urllib.parse
from typing import Any, Dict, List, Optional, Tuple

from pydantic import Field, model_validator

from haive.core.engine.agent.persistence.base import CheckpointerConfig
from haive.core.engine.agent.persistence.types import CheckpointerType

# Check if PostgreSQL dependencies are installed
try:
    from langgraph.checkpoint.postgres import PostgresSaver
    from psycopg_pool import ConnectionPool

    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

logger = logging.getLogger(__name__)


class PostgresCheckpointerConfig(CheckpointerConfig):
    """
    Configuration for PostgreSQL-based checkpointing.

    This class handles creation and configuration of a PostgreSQL-based
    checkpointer for LangGraph agents, with thread registration and pool
    management.
    """

    type: CheckpointerType = CheckpointerType.postgres

    # Database connection settings
    db_host: str = Field(default="localhost", description="PostgreSQL host")
    db_port: int = Field(default=5432, description="PostgreSQL port")
    db_name: str = Field(default="postgres", description="PostgreSQL database name")
    db_user: str = Field(default="postgres", description="PostgreSQL username")
    db_pass: str = Field(default="postgres", description="PostgreSQL password")
    ssl_mode: str = Field(default="disable", description="SSL mode for connection")

    # Pool settings
    min_pool_size: int = Field(default=1, description="Minimum pool size")
    max_pool_size: int = Field(default=5, description="Maximum pool size")
    auto_commit: bool = Field(default=True, description="Auto-commit transactions")
    prepare_threshold: int = Field(default=0, description="Prepare threshold")

    # Runtime settings
    setup_needed: bool = Field(
        default=True, description="Whether to initialize DB tables"
    )
    use_async: bool = Field(default=False, description="Whether to use async mode")

    # Internal state (not serialized)
    _pool: Optional[Any] = None
    _checkpointer: Optional[Any] = None

    @model_validator(mode="after")
    def validate_postgres_available(self):
        """Validate that postgres dependencies are available if this config is used."""
        if not POSTGRES_AVAILABLE:
            raise ImportError(
                "PostgreSQL dependencies not available. Please install with: "
                "pip install psycopg[binary] langgraph[postgres]"
            )
        return self

    def create_checkpointer(self) -> Any:
        """
        Create a PostgreSQL checkpointer with the specified configuration.

        Returns:
            A PostgresSaver instance for use with LangGraph
        """
        if not POSTGRES_AVAILABLE:
            logger.warning(
                "PostgreSQL dependencies not available, falling back to memory checkpointer"
            )
            from langgraph.checkpoint.memory import MemorySaver

            return MemorySaver()

        try:
            # Create or reuse connection pool
            if self._pool is None:
                logger.info("Creating new PostgreSQL connection pool")
                # Build connection URI
                encoded_pass = urllib.parse.quote_plus(str(self.db_pass))
                db_uri = f"postgresql://{self.db_user}:{encoded_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
                if self.ssl_mode:
                    db_uri += f"?sslmode={self.ssl_mode}"

                # Create pool
                self._pool = ConnectionPool(
                    conninfo=db_uri,
                    min_size=self.min_pool_size,
                    max_size=self.max_pool_size,
                    kwargs={
                        "autocommit": self.auto_commit,
                        "prepare_threshold": self.prepare_threshold,
                    },
                    open=True,  # Explicitly open the pool
                )

            # Create PostgresSaver with the pool
            self._checkpointer = PostgresSaver(self._pool)

            # Initialize tables if needed
            if self.setup_needed:
                self._checkpointer.setup()
                self.setup_needed = False

            return self._checkpointer

        except Exception as e:
            logger.error(f"Error creating PostgreSQL checkpointer: {e}")
            logger.warning("Falling back to memory checkpointer")
            from langgraph.checkpoint.memory import MemorySaver

            return MemorySaver()

    def close(self):
        """Close the connection pool if it exists and is open."""
        if self._pool is not None:
            try:
                if hasattr(self._pool, "is_open") and self._pool.is_open():
                    logger.info("Closing PostgreSQL connection pool")
                    self._pool.close()
                elif hasattr(self._pool, "_opened") and self._pool._opened:
                    logger.info("Closing PostgreSQL connection pool")
                    self._pool.close()
            except Exception as e:
                logger.error(f"Error closing PostgreSQL connection pool: {e}")

    def register_thread(
        self,
        thread_id: str,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Register a thread in the PostgreSQL database.

        This ensures that the thread exists in the database before
        any checkpoints are created that reference it.

        Args:
            thread_id: The thread ID to register
            name: Optional thread name (not used, included for API compatibility)
            metadata: Optional metadata dict
        """
        if not POSTGRES_AVAILABLE or self._pool is None:
            logger.debug("PostgreSQL not available or pool not initialized")
            return

        try:
            # Create checkpointer if not already created
            if self._checkpointer is None:
                self._checkpointer = self.create_checkpointer()

            # Ensure pool is open
            if hasattr(self._pool, "is_open"):
                try:
                    if not self._pool.is_open():
                        self._pool.open()
                except (AttributeError, Exception) as e:
                    logger.warning(f"Could not check if pool is open: {e}")
                    # Try direct access to internal attribute
                    if hasattr(self._pool, "_opened") and not self._pool._opened:
                        self._pool._pool = (
                            [] if not hasattr(self._pool, "_pool") else self._pool._pool
                        )
                        self._pool._opened = True

            # Register thread
            with self._pool.connection() as conn:
                with conn.cursor() as cursor:
                    # First check the actual schema of the threads table
                    cursor.execute(
                        "SELECT column_name FROM information_schema.columns WHERE table_name='threads'"
                    )
                    columns = [row[0] for row in cursor.fetchall()]
                    logger.debug(f"Threads table columns: {columns}")

                    # Check if thread already exists
                    cursor.execute(
                        "SELECT 1 FROM threads WHERE thread_id = %s", (thread_id,)
                    )
                    thread_exists = cursor.fetchone() is not None

                    if not thread_exists:
                        # Convert metadata to JSON string if provided
                        metadata_json = "{}"
                        if metadata:
                            metadata_json = json.dumps(metadata)

                        # Insert thread - using only columns that exist
                        if "metadata" in columns:
                            cursor.execute(
                                "INSERT INTO threads (thread_id, metadata) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                                (thread_id, metadata_json),
                            )
                        else:
                            cursor.execute(
                                "INSERT INTO threads (thread_id) VALUES (%s) ON CONFLICT DO NOTHING",
                                (thread_id,),
                            )
                        logger.info(f"Thread {thread_id} registered successfully")
                    else:
                        logger.debug(f"Thread {thread_id} already exists in database")

        except Exception as e:
            logger.error(f"Error registering thread in PostgreSQL: {e}")

    def put_checkpoint(
        self,
        config: Dict[str, Any],
        data: Any,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Store a checkpoint in the database.

        Args:
            config: Configuration with thread_id and optional checkpoint_id
            data: The checkpoint data to store
            metadata: Optional metadata to associate with the checkpoint

        Returns:
            Updated config with checkpoint_id
        """
        if not POSTGRES_AVAILABLE:
            logger.warning(
                "PostgreSQL dependencies not available, checkpoint not stored"
            )
            return config

        checkpointer = self.create_checkpointer()

        # Structure the data as expected by PostgresSaver.put
        config["configurable"]["thread_id"]
        config["configurable"].get("checkpoint_ns", "")

        # Create a checkpoint structure with correct fields and then store it
        checkpoint_data = {
            "id": config["configurable"].get(
                "checkpoint_id", ""
            ),  # Will be auto-generated if empty
            "channel_values": data,
        }

        # Prepare metadata
        checkpoint_metadata = metadata or {}

        # Get existing channel versions (required by newer API)
        channel_versions = {}

        # Call the appropriate put method based on the available API
        if hasattr(checkpointer, "put") and callable(checkpointer.put):
            # Determine the method signature
            import inspect

            sig = inspect.signature(checkpointer.put)
            param_names = list(sig.parameters.keys())

            if "metadata" in param_names and "new_versions" in param_names:
                # New API pattern: put(config, checkpoint, metadata, new_versions)
                next_config = checkpointer.put(
                    config, checkpoint_data, checkpoint_metadata, channel_versions
                )
                return next_config
            else:
                # Older API pattern without new_versions parameter (legacy)
                next_config = checkpointer.put(config, checkpoint_data)
                return next_config
        else:
            # Fallback to a memory saver
            from langgraph.checkpoint.memory import MemorySaver

            memory_saver = MemorySaver()
            return memory_saver.put(config, checkpoint_data)

    def get_checkpoint(self, config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Retrieve a checkpoint from the database.

        Args:
            config: Configuration with thread_id and optional checkpoint_id

        Returns:
            The checkpoint data if found, None otherwise
        """
        if not POSTGRES_AVAILABLE:
            logger.warning(
                "PostgreSQL dependencies not available, checkpoint not retrieved"
            )
            return None

        checkpointer = self.create_checkpointer()

        # Get the checkpoint
        if hasattr(checkpointer, "get") and callable(checkpointer.get):
            result = checkpointer.get(config)
            return result

        return None

    def list_checkpoints(
        self, config: Dict[str, Any], limit: Optional[int] = None
    ) -> List[Tuple[Dict[str, Any], Any]]:
        """
        List checkpoints for a thread.

        Args:
            config: Configuration with thread_id
            limit: Optional maximum number of checkpoints to return

        Returns:
            List of (config, checkpoint) tuples
        """
        if not POSTGRES_AVAILABLE:
            logger.warning(
                "PostgreSQL dependencies not available, no checkpoints listed"
            )
            return []

        checkpointer = self.create_checkpointer()

        # List checkpoints
        if hasattr(checkpointer, "list") and callable(checkpointer.list):
            try:
                checkpoint_tuples = list(checkpointer.list(config, limit=limit))
                return [(cp.config, cp.checkpoint) for cp in checkpoint_tuples]
            except Exception as e:
                logger.error(f"Error listing checkpoints: {e}")
                return []

        return []
