"""SQLite-based persistence implementation for the Haive framework.

This module provides a SQLite-backed checkpoint persistence implementation that
stores state data in a local SQLite database file. This allows for durable state
persistence without requiring external database services, making it ideal for
local development, testing, and single-instance deployments.

The SQLite implementation strikes a balance between the simplicity of in-memory
storage and the durability of full database solutions like PostgreSQL. It offers
file-based persistence with minimal setup, while still providing basic thread
tracking and checkpoint management capabilities.

Key advantages of the SQLite implementation include:
- No external dependencies beyond the Python standard library
- Simple file-based storage requiring no separate database service
- Compatibility with both synchronous and asynchronous operations
- Support for both full history and shallow (latest-only) storage modes
- Automatic schema creation and management
"""

import json
import logging
import os
import sqlite3
import uuid
from typing import Any, Dict

from pydantic import Field

from haive.core.persistence.base import CheckpointerConfig
from haive.core.persistence.types import CheckpointerType
from haive.core.persistence.utils import deserialize_metadata, serialize_metadata

logger = logging.getLogger(__name__)


class SQLiteSaver:
    """A LangGraph-compatible checkpointer implementation using SQLite.

    This class provides a simple but effective implementation of the LangGraph
    checkpointer interface using SQLite as the storage backend. It handles state
    persistence, thread tracking, and checkpoint management through a local
    SQLite database file.

    The implementation automatically creates and manages the necessary database
    schema, including tables for threads and checkpoints. It provides methods
    for storing and retrieving checkpoint data, managing thread information,
    and tracking checkpoint relationships.

    Key features include:

    - File-based persistence with minimal setup requirements
    - Support for tracking parent-child relationships between checkpoints
    - Thread management with metadata and activity tracking
    - Automatic schema creation and database directory management
    - Efficient storage and retrieval of checkpoint data
    - JSON serialization for flexible data storage

    This implementation is ideal for local development, testing, and single-instance
    deployments where a full database service like PostgreSQL would be overkill.
    """

    def __init__(self, db_path: str):
        """Initialize the SQLite saver with a database file path.

        This constructor sets up the SQLite checkpointer, ensuring the database
        directory exists and initializing the required schema. It automatically
        creates the database file if it doesn't exist.

        Args:
            db_path: Path to the SQLite database file where state will be stored.
                This can be an absolute or relative path. The directory structure
                will be created if it doesn't exist.

        Example:
            ```python
            # Create a SQLite checkpointer in the 'data' directory
            saver = SQLiteSaver("data/agent_state.db")

            # Use with a graph
            from langgraph.graph import Graph
            graph = Graph(checkpointer=saver)
            ```
        """
        self.db_path = db_path
        self._ensure_db_dir()
        self.setup()

    def _ensure_db_dir(self):
        """Ensure the database directory exists."""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

    def setup(self):
        """Set up the SQLite database schema.

        This method creates the necessary database tables for storing checkpoints
        and thread information if they don't already exist. It establishes the
        schema structure with appropriate relationships and constraints.

        The schema includes:

        1. A 'threads' table for tracking conversation threads with:
           - thread_id: Unique identifier for each thread
           - created_at: Timestamp when the thread was created
           - last_access: Timestamp of the most recent activity
           - metadata: JSON blob for storing additional thread information

        2. A 'checkpoints' table for storing state checkpoints with:
           - checkpoint_id: Unique identifier for each checkpoint
           - thread_id: Foreign key linking to the thread
           - checkpoint_ns: Namespace for organizing checkpoints
           - parent_checkpoint_id: For tracking checkpoint relationships
           - created_at: Timestamp when the checkpoint was created
           - data: The serialized checkpoint data
           - metadata: JSON blob for storing additional checkpoint information

        The method is automatically called during initialization but can also
        be called explicitly to recreate or validate the schema.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Create threads table
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS threads (
                thread_id TEXT PRIMARY KEY,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_access TEXT DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT DEFAULT '{}'
            )
            """
            )

            # Create checkpoints table
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS checkpoints (
                checkpoint_id TEXT,
                thread_id TEXT,
                checkpoint_ns TEXT DEFAULT '',
                parent_checkpoint_id TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                data TEXT,
                metadata TEXT DEFAULT '{}',
                PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id),
                FOREIGN KEY (thread_id) REFERENCES threads (thread_id) ON DELETE CASCADE
            )
            """
            )

            conn.commit()

    def get(self, config: dict[str, Any]) -> dict[str, Any] | None:
        """Retrieve a checkpoint from the SQLite database.

        This method retrieves a specific checkpoint from the database based on the
        provided configuration. It handles extracting the necessary identifiers
        from the configuration, constructing and executing the appropriate query,
        and deserializing the retrieved data.

        The method can retrieve either a specific checkpoint (if checkpoint_id is
        provided) or the most recent checkpoint for a thread (if only thread_id
        is specified).

        Args:
            config: Configuration dictionary containing:
                - thread_id: The thread identifier (required)
                - checkpoint_id: Optional specific checkpoint to retrieve
                - configurable: Optional nested dictionary with additional parameters

        Returns:
            Dict[str, Any]: The checkpoint data if found, including:
                - channel_values: The actual state data
                - metadata: Additional information about the checkpoint
                - id: The checkpoint identifier
                Or None if no matching checkpoint is found

        Example:
            ```python
            # Get the latest checkpoint for a thread
            checkpoint = saver.get({"thread_id": "user_123"})

            # Get a specific checkpoint
            checkpoint = saver.get({
                "thread_id": "user_123",
                "checkpoint_id": "checkpoint_456"
            })

            if checkpoint:
                # Use the state data
                state_data = checkpoint["channel_values"]
            ```
        """
        thread_id = config["configurable"]["thread_id"]
        checkpoint_id = config["configurable"].get("checkpoint_id")
        checkpoint_ns = config["configurable"].get("checkpoint_ns", "")

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            if checkpoint_id:
                # Get specific checkpoint
                cursor.execute(
                    """
                    SELECT data FROM checkpoints
                    WHERE thread_id = ? AND checkpoint_ns = ? AND checkpoint_id = ?
                    """,
                    (thread_id, checkpoint_ns, checkpoint_id),
                )
            else:
                # Get latest checkpoint
                cursor.execute(
                    """
                    SELECT data FROM checkpoints
                    WHERE thread_id = ? AND checkpoint_ns = ?
                    ORDER BY created_at DESC LIMIT 1
                    """,
                    (thread_id, checkpoint_ns),
                )

            row = cursor.fetchone()

            if row:
                return json.loads(row["data"])

            return None

    def put(
        self,
        config: dict[str, Any],
        checkpoint: dict[str, Any],
        metadata: dict[str, Any] | None = None,
        new_versions: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Save a checkpoint to the database.

        Args:
            config: Configuration with thread_id and optional checkpoint_id
            checkpoint: The checkpoint data to save
            metadata: Optional metadata to associate with the checkpoint
            new_versions: Optional channel versions (ignored in SQLite implementation)

        Returns:
            Updated config with checkpoint_id
        """
        thread_id = config["configurable"]["thread_id"]
        checkpoint_ns = config["configurable"].get("checkpoint_ns", "")
        parent_checkpoint_id = config["configurable"].get("checkpoint_id")

        # Generate a checkpoint ID if not present in the data
        checkpoint_id = checkpoint.get("id")
        if not checkpoint_id:
            checkpoint_id = str(uuid.uuid4())
            checkpoint["id"] = checkpoint_id

        # Serialize data and metadata
        serialized_data = json.dumps(checkpoint)
        serialized_metadata = serialize_metadata(metadata or {})

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Ensure thread exists
            cursor.execute(
                """
                INSERT OR IGNORE INTO threads (thread_id, last_access)
                VALUES (?, CURRENT_TIMESTAMP)
                """,
                (thread_id,),
            )

            # Update last access time if thread already exists
            cursor.execute(
                """
                UPDATE threads SET last_access = CURRENT_TIMESTAMP
                WHERE thread_id = ?
                """,
                (thread_id,),
            )

            # Insert checkpoint
            cursor.execute(
                """
                INSERT INTO checkpoints
                (checkpoint_id, thread_id, checkpoint_ns, parent_checkpoint_id, data, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    checkpoint_id,
                    thread_id,
                    checkpoint_ns,
                    parent_checkpoint_id,
                    serialized_data,
                    serialized_metadata,
                ),
            )

            conn.commit()

        # Return updated config
        return {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_ns": checkpoint_ns,
                "checkpoint_id": checkpoint_id,
            }
        }

    def list(
        self,
        config: dict[str, Any],
        limit: int | None = None,
        filter: dict[str, Any] | None = None,
        before: dict[str, Any] | None = None,
    ) -> list[tuple[dict[str, Any], dict[str, Any]]]:
        """List checkpoints for a thread.

        Args:
            config: Configuration with thread_id
            limit: Optional maximum number of checkpoints to return
            filter: Optional filter conditions (not implemented)
            before: Optional checkpoint to start listing from (not implemented)

        Returns:
            List of (config, checkpoint) tuples
        """
        thread_id = config["configurable"]["thread_id"]
        checkpoint_ns = config["configurable"].get("checkpoint_ns", "")

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            query = """
            SELECT checkpoint_id, parent_checkpoint_id, data, metadata
            FROM checkpoints
            WHERE thread_id = ? AND checkpoint_ns = ?
            ORDER BY created_at DESC
            """

            params = [thread_id, checkpoint_ns]

            if limit is not None:
                query += " LIMIT ?"
                params.append(limit)

            cursor.execute(query, params)
            rows = cursor.fetchall()

            result = []
            for row in rows:
                checkpoint_data = json.loads(row["data"])
                checkpoint_config = {
                    "configurable": {
                        "thread_id": thread_id,
                        "checkpoint_ns": checkpoint_ns,
                        "checkpoint_id": row["checkpoint_id"],
                    }
                }

                # Create parent config if available
                parent_config = None
                if row["parent_checkpoint_id"]:
                    parent_config = {
                        "configurable": {
                            "thread_id": thread_id,
                            "checkpoint_ns": checkpoint_ns,
                            "checkpoint_id": row["parent_checkpoint_id"],
                        }
                    }

                # Use a namedtuple-like structure to match LangGraph's API
                class CheckpointTuple:
                    def __init__(
                        self, config, checkpoint, metadata, parent_config, writes=None
                    ):
                        self.config = config
                        self.checkpoint = checkpoint
                        self.metadata = metadata
                        self.parent_config = parent_config
                        self.writes = writes or []

                metadata = deserialize_metadata(row["metadata"])

                result.append(
                    CheckpointTuple(
                        checkpoint_config, checkpoint_data, metadata, parent_config
                    )
                )

            return result


class SQLiteCheckpointerConfig(CheckpointerConfig):
    """Configuration for SQLite-based checkpoint persistence.

    This class provides a comprehensive configuration for using SQLite as a
    persistence backend for agent state. It offers the simplicity of file-based
    storage without requiring external database services, making it ideal for
    local development, testing, and single-instance deployments.

    SQLite persistence strikes a balance between the simplicity of in-memory
    storage and the durability of full database solutions like PostgreSQL. It
    provides persistent storage across application restarts while requiring
    minimal setup and configuration.

    Key features include:

    - File-based persistence with no external database dependencies
    - Support for both full and shallow storage modes
    - Thread registration and tracking with metadata
    - Checkpoint management with parent-child relationships
    - Simple configuration with minimal required parameters
    - Automatic database file and directory creation

    The implementation is particularly well-suited for:

    - Local development and testing environments
    - Single-instance deployments where simplicity is preferred
    - Applications with modest concurrency requirements
    - Scenarios where file-based persistence is sufficient

    Example:
        ```python
        from haive.core.persistence import SQLiteCheckpointerConfig

        # Create a basic SQLite checkpointer
        config = SQLiteCheckpointerConfig(
            db_path="data/agent_state.db"
        )

        # Create a checkpointer
        checkpointer = config.create_checkpointer()

        # Use with a graph
        from langgraph.graph import Graph
        graph = Graph(checkpointer=checkpointer)
        ```

    Note:
        While SQLite supports concurrent readers, it has limitations for
        concurrent writers. For high-concurrency production environments,
        consider using PostgresCheckpointerConfig instead.
    """

    type: CheckpointerType = CheckpointerType.SQLITE

    # SQLite configuration
    db_path: str = Field(
        default="./checkpoints.db", description="Path to SQLite database file"
    )

    # Runtime settings
    setup_needed: bool = Field(
        default=True, description="Whether to initialize DB tables on startup"
    )

    # Internal state (not serialized)
    checkpointer: Any | None = Field(default=None, exclude=True)

    def create_checkpointer(self) -> Any:
        """Create a SQLite checkpointer based on this configuration.

        This method instantiates and returns a SQLiteSaver object configured
        with the database path specified in this configuration. It caches the
        created checkpointer instance for reuse, ensuring that multiple calls
        to this method return the same instance.

        The method handles the creation of the database file and directory
        structure if they don't already exist, and initializes the database
        schema with the required tables.

        Returns:
            Any: A SQLiteSaver instance ready for use with LangGraph

        Example:
            ```python
            config = SQLiteCheckpointerConfig(db_path="data/state.db")
            checkpointer = config.create_checkpointer()

            # Use with a graph
            graph = Graph(checkpointer=checkpointer)
            ```
        """
        if self.checkpointer is None:
            self.checkpointer = SQLiteSaver(self.db_path)

        return self.checkpointer

    def register_thread(
        self,
        thread_id: str,
        name: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Register or update a thread in the SQLite database.

        This method registers a new thread in the database or updates an existing
        thread's metadata and last access time. It ensures that the thread entry
        exists before any checkpoints are created for that thread, maintaining
        proper database integrity.

        Thread registration is important for tracking agent conversations and
        associating metadata with them, such as user information, session data,
        or other contextual information that might be useful for analytics or
        debugging.

        Args:
            thread_id: Unique identifier for the thread to register or update
            name: Optional human-readable name for the thread (currently unused)
            metadata: Optional dictionary of metadata to associate with the thread,
                which can include any JSON-serializable information relevant to
                the thread (user info, session data, etc.)

        Example:
            ```python
            config = SQLiteCheckpointerConfig(db_path="data/state.db")

            # Register a new thread with metadata
            config.register_thread(
                thread_id="user_123",
                name="John's Conversation",
                metadata={
                    "user_id": "user_123",
                    "session_start": "2023-04-01T12:00:00Z",
                    "source": "web_app"
                }
            )

            # Later, you can use this thread_id with checkpoints
            config.put_checkpoint(
                {"configurable": {"thread_id": "user_123"}},
                {"key": "value"}
            )
            ```
        """
        self.create_checkpointer()

        # Convert metadata to JSON string if provided
        metadata_json = serialize_metadata(metadata or {})

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Check if thread already exists
            cursor.execute("SELECT 1 FROM threads WHERE thread_id = ?", (thread_id,))

            thread_exists = cursor.fetchone() is not None

            if not thread_exists:
                # Insert new thread
                cursor.execute(
                    """
                    INSERT INTO threads (thread_id, metadata)
                    VALUES (?, ?)
                    """,
                    (thread_id, metadata_json),
                )
                logger.info(f"Thread {thread_id} registered in SQLite")
            else:
                # Update last access time
                cursor.execute(
                    """
                    UPDATE threads
                    SET last_access = CURRENT_TIMESTAMP
                    WHERE thread_id = ?
                    """,
                    (thread_id,),
                )
                logger.debug(f"Thread {thread_id} already exists in SQLite")

    def put_checkpoint(
        self,
        config: dict[str, Any],
        data: Any,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Store a checkpoint in the SQLite database.

        Args:
            config: Configuration with thread_id and optional checkpoint_id
            data: The checkpoint data to store
            metadata: Optional metadata to associate with the checkpoint

        Returns:
            Updated config with checkpoint_id
        """
        checkpointer = self.create_checkpointer()

        # Structure the data as expected
        checkpoint_data = {
            "id": config["configurable"].get(
                "checkpoint_id", ""
            ),  # Will be auto-generated if empty
            "channel_values": data,
        }

        # Store the checkpoint
        return checkpointer.put(config, checkpoint_data, metadata)

    def get_checkpoint(self, config: dict[str, Any]) -> dict[str, Any] | None:
        """Retrieve a checkpoint from the SQLite database.

        Args:
            config: Configuration with thread_id and optional checkpoint_id

        Returns:
            The checkpoint data if found, None otherwise
        """
        checkpointer = self.create_checkpointer()

        # Get the checkpoint
        result = checkpointer.get(config)

        # Extract and return channel_values if available
        if result and "channel_values" in result:
            return result["channel_values"]

        return result

    def list_checkpoints(
        self, config: dict[str, Any], limit: int | None = None
    ) -> list[tuple[dict[str, Any], Any]]:
        """List checkpoints for a thread.

        Args:
            config: Configuration with thread_id
            limit: Optional maximum number of checkpoints to return

        Returns:
            List of (config, checkpoint) tuples
        """
        checkpointer = self.create_checkpointer()

        # List checkpoints
        checkpoint_tuples = checkpointer.list(config, limit=limit)

        # Extract and return (config, channel_values) tuples
        result = []
        for cp in checkpoint_tuples:
            checkpoint_data = cp.checkpoint
            channel_values = checkpoint_data.get("channel_values", checkpoint_data)
            result.append((cp.config, channel_values))

        return result

    def close(self) -> None:
        """Close any resources associated with this checkpointer."""
        # SQLite connections are closed automatically after each operation
        self.checkpointer = None
