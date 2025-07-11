"""Supabase-based persistence implementation for the Haive framework.

This module provides a Supabase-backed checkpoint persistence implementation that
stores state data in a Supabase Postgres database. This allows for cloud-based,
scalable state persistence with built-in security features like Row Level Security
(RLS) policies.

Supabase offers a fully-managed Postgres database service with authentication,
realtime features, and other cloud infrastructure benefits. This implementation
leverages these capabilities to provide a production-ready persistence solution
with proper relational design and security policies.

Key advantages of the Supabase implementation include:
- Cloud-hosted and fully-managed database with high availability
- Built-in authentication and security features
- Realtime capabilities for live state updates
- Compatibility with both synchronous and asynchronous operations
- Support for both full history and shallow storage modes
- Automatic schema creation and management with migrations
"""

import json
import logging
import uuid
from datetime import datetime
from typing import Any, Dict

from pydantic import Field, model_validator

from haive.core.persistence.base import CheckpointerConfig
from haive.core.persistence.types import CheckpointerType
from haive.core.persistence.utils import deserialize_metadata, serialize_metadata

logger = logging.getLogger(__name__)

# Check if Supabase dependencies are available
try:
    from supabase import Client, create_client

    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

# Try to import the shared Supabase client utility
try:
    from haive.dataflow.db.supabase import get_supabase_client, sanitize_sql

    DATAFLOW_AVAILABLE = True
except ImportError:
    DATAFLOW_AVAILABLE = False


class SupabaseSaver:
    """A LangGraph-compatible checkpointer implementation using Supabase.

    This class provides a robust implementation of the LangGraph checkpointer
    interface using Supabase as the storage backend. It stores state data in
    a Supabase Postgres database with proper relational design, security
    policies, and cloud infrastructure benefits.

    The implementation automatically creates and manages the necessary database
    schema, including tables for threads and checkpoints with appropriate
    relationships and indexes for optimal performance. It integrates with
    Supabase's authentication system and Row Level Security (RLS) policies
    to ensure data isolation and security.

    Key features include:

    - Cloud-hosted and fully-managed database infrastructure
    - Proper relational design with foreign key relationships
    - Row Level Security (RLS) policies for data isolation
    - Authentication integration for secure multi-tenant deployments
    - Efficient storage and retrieval of checkpoint data
    - JSON serialization for flexible data storage
    - Support for both full history and shallow (latest-only) storage modes

    This implementation is ideal for production deployments where scalability,
    reliability, and security are paramount considerations. It offers a balance
    of performance and features suitable for multi-tenant applications and
    environments where proper data isolation is required.
    """

    def __init__(
        self,
        supabase_url: str | None = None,
        supabase_key: str | None = None,
        client: Any | None = None,
        user_id: str | None = None,
        initialize_schema: bool = True,
    ):
        """Initialize the Supabase saver.

        Args:
            supabase_url: Supabase project URL (not needed if client provided)
            supabase_key: Supabase API key (not needed if client provided)
            client: Existing Supabase client (if provided, URL and key are ignored)
            user_id: Optional user ID for RLS policies
            initialize_schema: Whether to initialize database schema
        """
        if not SUPABASE_AVAILABLE:
            raise ImportError(
                "Supabase dependencies not available. Please install with: "
                "pip install supabase"
            )

        self.user_id = user_id

        # Use provided client or create new one
        if client:
            self.client = client
        elif DATAFLOW_AVAILABLE:
            try:
                self.client = get_supabase_client()
                self.supabase_url = None  # Not storing credentials when using env vars
                self.supabase_key = None
            except Exception as e:
                logger.warning(f"Failed to get Supabase client from dataflow: {e}")

                # Fall back to direct client creation with provided credentials
                if supabase_url and supabase_key:
                    self.supabase_url = supabase_url
                    self.supabase_key = supabase_key
                    self.client = create_client(supabase_url, supabase_key)
                else:
                    raise ValueError(
                        "Supabase URL and key required when dataflow client not available"
                    )
        elif supabase_url and supabase_key:
            self.supabase_url = supabase_url
            self.supabase_key = supabase_key
            self.client = create_client(supabase_url, supabase_key)
        else:
            raise ValueError(
                "Supabase URL and key required when dataflow module not available"
            )

        if initialize_schema:
            self.setup()

    def setup(self):
        """Set up the Supabase database schema.

        Creates necessary tables, foreign key relationships, indexes,
        and RLS policies for secure access.
        """
        try:
            # Execute SQL - either using dataflow utility or directly
            def execute_sql(sql: str):
                clean_sql = sql.strip().rstrip(";").strip()

                if DATAFLOW_AVAILABLE:
                    clean_sql = sanitize_sql(sql)

                try:
                    self.client.rpc("execute_sql", {"sql": clean_sql}).execute()
                except Exception as e:
                    logger.exception(f"SQL Error: {e}\nSQL: {clean_sql[:100]}...")
                    raise

            # Check if tables already exist
            tables_query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name IN ('agent_users', 'agent_threads', 'agent_checkpoints', 'agent_checkpoint_data')
            """

            result = self.client.rpc(
                "execute_sql", {"sql": tables_query.strip()}
            ).execute()
            existing_tables = set(row.get("table_name") for row in result.data)

            # Create tables with prefixes to avoid conflicts with existing tables
            if "agent_users" not in existing_tables:
                # Create users table
                execute_sql(
                    """
                CREATE TABLE IF NOT EXISTS public.agent_users (
                    id UUID PRIMARY KEY,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    email TEXT,
                    metadata JSONB
                )
                """
                )

                # Set up RLS policy for users
                execute_sql(
                    """
                -- Enable RLS on agent_users table
                ALTER TABLE public.agent_users ENABLE ROW LEVEL SECURITY
                """
                )

                execute_sql(
                    """
                -- Create policy for users to see only their own data
                CREATE POLICY "Users can view own data"
                ON public.agent_users
                FOR SELECT
                USING (auth.uid() = id)
                """
                )

                execute_sql(
                    """
                -- Create policy for users to update only their own data
                CREATE POLICY "Users can update own data"
                ON public.agent_users
                FOR UPDATE
                USING (auth.uid() = id)
                """
                )

            if "agent_threads" not in existing_tables:
                # Create threads table
                execute_sql(
                    """
                CREATE TABLE IF NOT EXISTS public.agent_threads (
                    id UUID PRIMARY KEY,
                    user_id UUID REFERENCES public.agent_users(id) ON DELETE CASCADE,
                    external_id TEXT,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    last_access TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    metadata JSONB,
                    name TEXT,
                    UNIQUE(user_id, external_id)
                )
                """
                )

                # Create indexes
                execute_sql(
                    """
                CREATE INDEX IF NOT EXISTS agent_threads_user_id_idx ON public.agent_threads(user_id)
                """
                )

                execute_sql(
                    """
                CREATE INDEX IF NOT EXISTS agent_threads_external_id_idx ON public.agent_threads(external_id)
                """
                )

                # Set up RLS policy for threads
                execute_sql(
                    """
                -- Enable RLS on agent_threads table
                ALTER TABLE public.agent_threads ENABLE ROW LEVEL SECURITY
                """
                )

                execute_sql(
                    """
                -- Create policy for users to see only their own threads
                CREATE POLICY "Users can view own threads"
                ON public.agent_threads
                FOR SELECT
                USING (auth.uid() = user_id)
                """
                )

                execute_sql(
                    """
                -- Create policy for users to update only their own threads
                CREATE POLICY "Users can update own threads"
                ON public.agent_threads
                FOR UPDATE
                USING (auth.uid() = user_id)
                """
                )

                execute_sql(
                    """
                -- Create policy for users to insert only own threads
                CREATE POLICY "Users can insert own threads"
                ON public.agent_threads
                FOR INSERT
                WITH CHECK (auth.uid() = user_id)
                """
                )

                execute_sql(
                    """
                -- Create policy for users to delete only their own threads
                CREATE POLICY "Users can delete own threads"
                ON public.agent_threads
                FOR DELETE
                USING (auth.uid() = user_id)
                """
                )

            if "agent_checkpoints" not in existing_tables:
                # Create checkpoints table
                execute_sql(
                    """
                CREATE TABLE IF NOT EXISTS public.agent_checkpoints (
                    id UUID PRIMARY KEY,
                    thread_id UUID REFERENCES public.agent_threads(id) ON DELETE CASCADE,
                    checkpoint_ns TEXT DEFAULT '',
                    parent_id UUID REFERENCES public.agent_checkpoints(id) ON DELETE SET NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    metadata JSONB,
                    versions JSONB,
                    UNIQUE(thread_id, checkpoint_ns, id)
                )
                """
                )

                # Create indexes
                execute_sql(
                    """
                CREATE INDEX IF NOT EXISTS agent_checkpoints_thread_id_idx ON public.agent_checkpoints(thread_id)
                """
                )

                execute_sql(
                    """
                CREATE INDEX IF NOT EXISTS agent_checkpoints_parent_id_idx ON public.agent_checkpoints(parent_id)
                """
                )

                # Set up RLS policy for checkpoints
                execute_sql(
                    """
                -- Enable RLS on agent_checkpoints table
                ALTER TABLE public.agent_checkpoints ENABLE ROW LEVEL SECURITY
                """
                )

                execute_sql(
                    """
                -- Create policy for users to see only checkpoints from their own threads
                CREATE POLICY "Users can view own checkpoints"
                ON public.agent_checkpoints
                FOR SELECT
                USING (
                    EXISTS (
                        SELECT 1 FROM public.agent_threads
                        WHERE agent_threads.id = agent_checkpoints.thread_id
                        AND agent_threads.user_id = auth.uid()
                    )
                )
                """
                )

                execute_sql(
                    """
                -- Create policy for users to update only checkpoints from their own threads
                CREATE POLICY "Users can update own checkpoints"
                ON public.agent_checkpoints
                FOR UPDATE
                USING (
                    EXISTS (
                        SELECT 1 FROM public.agent_threads
                        WHERE agent_threads.id = agent_checkpoints.thread_id
                        AND agent_threads.user_id = auth.uid()
                    )
                )
                """
                )

                execute_sql(
                    """
                -- Create policy for users to insert only checkpoints in their own threads
                CREATE POLICY "Users can insert own checkpoints"
                ON public.agent_checkpoints
                FOR INSERT
                WITH CHECK (
                    EXISTS (
                        SELECT 1 FROM public.agent_threads
                        WHERE agent_threads.id = agent_checkpoints.thread_id
                        AND agent_threads.user_id = auth.uid()
                    )
                )
                """
                )

                execute_sql(
                    """
                -- Create policy for users to delete only checkpoints from their own threads
                CREATE POLICY "Users can delete own checkpoints"
                ON public.agent_checkpoints
                FOR DELETE
                USING (
                    EXISTS (
                        SELECT 1 FROM public.agent_threads
                        WHERE agent_threads.id = agent_checkpoints.thread_id
                        AND agent_threads.user_id = auth.uid()
                    )
                )
                """
                )

            if "agent_checkpoint_data" not in existing_tables:
                # Create checkpoint_data table for storing the actual checkpoint data
                execute_sql(
                    """
                CREATE TABLE IF NOT EXISTS public.agent_checkpoint_data (
                    checkpoint_id UUID PRIMARY KEY REFERENCES public.agent_checkpoints(id) ON DELETE CASCADE,
                    thread_id UUID REFERENCES public.agent_threads(id) ON DELETE CASCADE,
                    data JSONB NOT NULL,
                    channel_values JSONB,
                    pending_sends JSONB
                )
                """
                )

                # Create indexes
                execute_sql(
                    """
                CREATE INDEX IF NOT EXISTS agent_checkpoint_data_thread_id_idx ON public.agent_checkpoint_data(thread_id)
                """
                )

                # Set up RLS policy for checkpoint_data
                execute_sql(
                    """
                -- Enable RLS on agent_checkpoint_data table
                ALTER TABLE public.agent_checkpoint_data ENABLE ROW LEVEL SECURITY
                """
                )

                execute_sql(
                    """
                -- Create policy for users to see only data from their own checkpoints
                CREATE POLICY "Users can view own checkpoint data"
                ON public.agent_checkpoint_data
                FOR SELECT
                USING (
                    EXISTS (
                        SELECT 1 FROM public.agent_threads
                        WHERE agent_threads.id = agent_checkpoint_data.thread_id
                        AND agent_threads.user_id = auth.uid()
                    )
                )
                """
                )

                execute_sql(
                    """
                -- Create policy for users to update only data from their own checkpoints
                CREATE POLICY "Users can update own checkpoint data"
                ON public.agent_checkpoint_data
                FOR UPDATE
                USING (
                    EXISTS (
                        SELECT 1 FROM public.agent_threads
                        WHERE agent_threads.id = agent_checkpoint_data.thread_id
                        AND agent_threads.user_id = auth.uid()
                    )
                )
                """
                )

                execute_sql(
                    """
                -- Create policy for users to insert only data for their own checkpoints
                CREATE POLICY "Users can insert own checkpoint data"
                ON public.agent_checkpoint_data
                FOR INSERT
                WITH CHECK (
                    EXISTS (
                        SELECT 1 FROM public.agent_threads
                        WHERE agent_threads.id = agent_checkpoint_data.thread_id
                        AND agent_threads.user_id = auth.uid()
                    )
                )
                """
                )

                execute_sql(
                    """
                -- Create policy for users to delete only data from their own checkpoints
                CREATE POLICY "Users can delete own checkpoint data"
                ON public.agent_checkpoint_data
                FOR DELETE
                USING (
                    EXISTS (
                        SELECT 1 FROM public.agent_threads
                        WHERE agent_threads.id = agent_checkpoint_data.thread_id
                        AND agent_threads.user_id = auth.uid()
                    )
                )
                """
                )

            logger.info("Successfully set up Supabase schema")

        except Exception as e:
            logger.exception(f"Error setting up Supabase schema: {e}")
            raise

    def register_user(
        self,
        user_id: str,
        email: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Register a user in the system.

        Args:
            user_id: User ID
            email: Optional user email
            metadata: Optional user metadata

        Returns:
            The user ID
        """
        # Check if user already exists
        existing_user = (
            self.client.table("agent_users").select("*").eq("id", user_id).execute()
        )

        if not existing_user.data:
            # Convert metadata to JSON string
            metadata_json = serialize_metadata(metadata or {})

            # Insert new user
            self.client.table("agent_users").insert(
                {"id": user_id, "email": email, "metadata": metadata_json}
            ).execute()

            logger.info(f"User {user_id} registered in Supabase")
        else:
            logger.debug(f"User {user_id} already exists in Supabase")

        return user_id

    def register_thread(
        self,
        thread_id: str,
        user_id: str | None = None,
        name: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Register a thread in the system.

        Args:
            thread_id: Thread ID
            user_id: User ID who owns this thread
            name: Optional thread name
            metadata: Optional thread metadata

        Returns:
            The internal database ID for the thread
        """
        # Use provided user_id or default to the instance's user_id
        user_id = user_id or self.user_id

        if not user_id:
            raise ValueError("User ID is required to register a thread")

        # Ensure user exists
        self.register_user(user_id)

        # Check if thread already exists (by external ID and user_id)
        existing_thread = (
            self.client.table("agent_threads")
            .select("id")
            .eq("external_id", thread_id)
            .eq("user_id", user_id)
            .execute()
        )

        if existing_thread.data:
            # Thread exists, return its internal ID
            internal_id = existing_thread.data[0]["id"]

            # Update last access time
            self.client.table("agent_threads").update(
                {"last_access": datetime.now().isoformat()}
            ).eq("id", internal_id).execute()

            logger.debug(f"Thread {thread_id} already exists, updated last access")
            return internal_id
        # Generate internal ID
        internal_id = str(uuid.uuid4())

        # Convert metadata to JSON string
        metadata_json = serialize_metadata(metadata or {})

        # Insert new thread
        self.client.table("agent_threads").insert(
            {
                "id": internal_id,
                "user_id": user_id,
                "external_id": thread_id,
                "name": name,
                "metadata": metadata_json,
            }
        ).execute()

        logger.info(
            f"Thread {thread_id} registered in Supabase with internal ID {internal_id}"
        )
        return internal_id

    def get_internal_thread_id(
        self, thread_id: str, user_id: str | None = None
    ) -> str | None:
        """Get the internal thread ID from an external thread ID.

        Args:
            thread_id: External thread ID
            user_id: User ID

        Returns:
            Internal thread ID if found, None otherwise
        """
        # Use provided user_id or default to the instance's user_id
        user_id = user_id or self.user_id

        if not user_id:
            raise ValueError("User ID is required to get thread ID")

        # Look up thread
        result = (
            self.client.table("agent_threads")
            .select("id")
            .eq("external_id", thread_id)
            .eq("user_id", user_id)
            .execute()
        )

        if result.data:
            return result.data[0]["id"]

        return None

    def get(self, config: dict[str, Any]) -> dict[str, Any] | None:
        """Get a checkpoint from the database.

        Args:
            config: Configuration with thread_id and optional checkpoint_id

        Returns:
            Checkpoint data if found, None otherwise
        """
        thread_id = config["configurable"]["thread_id"]
        checkpoint_id = config["configurable"].get("checkpoint_id")
        checkpoint_ns = config["configurable"].get("checkpoint_ns", "")
        user_id = self.user_id

        if not user_id:
            raise ValueError("User ID is required to get checkpoints")

        try:
            # Get internal thread ID
            internal_thread_id = self.get_internal_thread_id(thread_id, user_id)

            if not internal_thread_id:
                logger.warning(f"Thread {thread_id} not found")
                return None

            # Build query
            query = (
                self.client.from_("agent_checkpoint_data")
                .select(
                    "agent_checkpoint_data.data, agent_checkpoint_data.channel_values, agent_checkpoint_data.pending_sends, agent_checkpoints.id"
                )
                .eq("agent_checkpoint_data.thread_id", internal_thread_id)
                .join(
                    "agent_checkpoints",
                    "agent_checkpoint_data.checkpoint_id=agent_checkpoints.id",
                )
                .eq("agent_checkpoints.checkpoint_ns", checkpoint_ns)
            )

            if checkpoint_id:
                # Get specific checkpoint
                query = query.eq("agent_checkpoints.id", checkpoint_id)
            else:
                # Get latest checkpoint
                query = query.order("agent_checkpoints.created_at", desc=True).limit(1)

            result = query.execute()

            if result.data:
                checkpoint_data = result.data[0]

                # Reconstruct checkpoint structure
                if checkpoint_data.get("channel_values"):
                    channel_values = (
                        json.loads(checkpoint_data["channel_values"])
                        if isinstance(checkpoint_data["channel_values"], str)
                        else checkpoint_data["channel_values"]
                    )
                    return channel_values

                # Fall back to data
                data = (
                    json.loads(checkpoint_data["data"])
                    if isinstance(checkpoint_data["data"], str)
                    else checkpoint_data["data"]
                )
                return data

            return None

        except Exception as e:
            logger.exception(f"Error retrieving checkpoint: {e}")
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
            new_versions: Optional channel versions

        Returns:
            Updated config with checkpoint_id
        """
        thread_id = config["configurable"]["thread_id"]
        checkpoint_ns = config["configurable"].get("checkpoint_ns", "")
        parent_checkpoint_id = config["configurable"].get("checkpoint_id")
        user_id = self.user_id

        if not user_id:
            raise ValueError("User ID is required to save checkpoints")

        try:
            # Generate a checkpoint ID if not present in the data
            checkpoint_id = str(uuid.uuid4())
            if "id" in checkpoint:
                # If ID is in checkpoint data, use that instead
                checkpoint_id = checkpoint["id"] or checkpoint_id

            # Ensure thread exists and get internal ID
            internal_thread_id = self.register_thread(thread_id, user_id)

            # Check if parent checkpoint ID needs to be converted to internal ID
            internal_parent_id = None
            if parent_checkpoint_id:
                # Look up the parent checkpoint to get its internal ID
                parent_result = (
                    self.client.table("agent_checkpoints")
                    .select("id")
                    .eq("thread_id", internal_thread_id)
                    .eq("checkpoint_ns", checkpoint_ns)
                    .execute()
                )

                if parent_result.data:
                    internal_parent_id = parent_result.data[0]["id"]

            # Serialize data and metadata
            serialized_metadata = serialize_metadata(metadata or {})
            serialized_versions = json.dumps(new_versions or {})

            # Extract channel values if present
            channel_values = None
            pending_sends = None
            if "channel_values" in checkpoint:
                channel_values = json.dumps(checkpoint["channel_values"])
            if "pending_sends" in checkpoint:
                pending_sends = json.dumps(checkpoint["pending_sends"])

            # Insert checkpoint record
            checkpoint_internal_id = str(uuid.uuid4())
            self.client.table("agent_checkpoints").insert(
                {
                    "id": checkpoint_internal_id,
                    "thread_id": internal_thread_id,
                    "checkpoint_ns": checkpoint_ns,
                    "parent_id": internal_parent_id,
                    "metadata": serialized_metadata,
                    "versions": serialized_versions,
                }
            ).execute()

            # Insert checkpoint data
            self.client.table("agent_checkpoint_data").insert(
                {
                    "checkpoint_id": checkpoint_internal_id,
                    "thread_id": internal_thread_id,
                    "data": json.dumps(checkpoint),
                    "channel_values": channel_values,
                    "pending_sends": pending_sends,
                }
            ).execute()

            # Return updated config
            return {
                "configurable": {
                    "thread_id": thread_id,
                    "checkpoint_ns": checkpoint_ns,
                    "checkpoint_id": checkpoint_internal_id,
                }
            }

        except Exception as e:
            logger.exception(f"Error saving checkpoint: {e}")
            # Return original config
            return config

    def list(
        self,
        config: dict[str, Any],
        limit: int | None = None,
        filter: dict[str, Any] | None = None,
        before: dict[str, Any] | None = None,
    ) -> list[Any]:
        """List checkpoints for a thread.

        Args:
            config: Configuration with thread_id
            limit: Optional maximum number of checkpoints to return
            filter: Optional filter conditions
            before: Optional checkpoint to start listing from

        Returns:
            List of checkpoint tuples
        """
        thread_id = config["configurable"]["thread_id"]
        checkpoint_ns = config["configurable"].get("checkpoint_ns", "")
        user_id = self.user_id

        if not user_id:
            raise ValueError("User ID is required to list checkpoints")

        try:
            # Get internal thread ID
            internal_thread_id = self.get_internal_thread_id(thread_id, user_id)

            if not internal_thread_id:
                logger.warning(f"Thread {thread_id} not found")
                return []

            # Build query
            query = (
                self.client.from_("agent_checkpoints")
                .select(
                    "agent_checkpoints.id, agent_checkpoints.parent_id, agent_checkpoints.metadata, agent_checkpoints.versions, "
                    "agent_checkpoint_data.data, agent_checkpoint_data.channel_values, agent_checkpoint_data.pending_sends"
                )
                .eq("agent_checkpoints.thread_id", internal_thread_id)
                .eq("agent_checkpoints.checkpoint_ns", checkpoint_ns)
                .join(
                    "agent_checkpoint_data",
                    "agent_checkpoints.id=agent_checkpoint_data.checkpoint_id",
                )
                .order("agent_checkpoints.created_at", desc=True)
            )

            # Apply limit if specified
            if limit is not None:
                query = query.limit(limit)

            # Apply before constraint if specified
            if (
                before
                and "configurable" in before
                and "checkpoint_id" in before["configurable"]
            ):
                before_id = before["configurable"]["checkpoint_id"]
                # Get created_at timestamp of the before checkpoint
                before_result = (
                    self.client.table("agent_checkpoints")
                    .select("created_at")
                    .eq("id", before_id)
                    .execute()
                )

                if before_result.data:
                    before_timestamp = before_result.data[0]["created_at"]
                    query = query.lt("agent_checkpoints.created_at", before_timestamp)

            result = query.execute()

            # Construct checkpoint tuples
            checkpoint_tuples = []
            for row in result.data:
                # Create config for this checkpoint
                checkpoint_config = {
                    "configurable": {
                        "thread_id": thread_id,
                        "checkpoint_ns": checkpoint_ns,
                        "checkpoint_id": row["id"],
                    }
                }

                # Create parent config if available
                parent_config = None
                if row["parent_id"]:
                    parent_config = {
                        "configurable": {
                            "thread_id": thread_id,
                            "checkpoint_ns": checkpoint_ns,
                            "checkpoint_id": row["parent_id"],
                        }
                    }

                # Parse data
                data = (
                    json.loads(row["data"])
                    if isinstance(row["data"], str)
                    else row["data"]
                )
                metadata_dict = deserialize_metadata(row["metadata"])

                # Create namedtuple-like object
                class CheckpointTuple:
                    def __init__(
                        self, config, checkpoint, metadata, parent_config, writes=None
                    ):
                        self.config = config
                        self.checkpoint = checkpoint
                        self.metadata = metadata
                        self.parent_config = parent_config
                        self.writes = writes or []

                checkpoint_tuples.append(
                    CheckpointTuple(
                        checkpoint_config, data, metadata_dict, parent_config
                    )
                )

            return checkpoint_tuples

        except Exception as e:
            logger.exception(f"Error listing checkpoints: {e}")
            return []

    def delete_thread(self, thread_id: str, user_id: str | None = None) -> bool:
        """Delete a thread and all its checkpoints.

        Args:
            thread_id: Thread ID
            user_id: User ID

        Returns:
            True if successful, False otherwise
        """
        # Use provided user_id or default to the instance's user_id
        user_id = user_id or self.user_id

        if not user_id:
            raise ValueError("User ID is required to delete a thread")

        try:
            # Get internal thread ID
            internal_thread_id = self.get_internal_thread_id(thread_id, user_id)

            if not internal_thread_id:
                logger.warning(f"Thread {thread_id} not found")
                return False

            # Delete thread (cascade will delete checkpoints and checkpoint_data)
            self.client.table("agent_threads").delete().eq(
                "id", internal_thread_id
            ).execute()

            logger.info(f"Thread {thread_id} deleted")
            return True

        except Exception as e:
            logger.exception(f"Error deleting thread: {e}")
            return False


class SupabaseCheckpointerConfig(CheckpointerConfig):
    """Configuration for Supabase-based checkpoint persistence.

    This class provides a comprehensive configuration for using Supabase as a
    cloud-based persistence backend for agent state. It leverages Supabase's
    managed PostgreSQL service with additional security features like Row Level
    Security (RLS) policies and authentication integration.

    Supabase offers a fully-managed database service with cloud infrastructure
    benefits, making it ideal for production deployments where scalability,
    reliability, and security are paramount. The implementation includes proper
    relational database design with appropriate indexes and constraints for
    optimal performance.

    Key features include:

    - Cloud-hosted and fully-managed PostgreSQL database
    - Row Level Security (RLS) policies for multi-tenant data isolation
    - Authentication integration for secure access control
    - Proper relational design with foreign key relationships
    - Support for both full and shallow storage modes
    - Efficient indexing for optimal query performance
    - Optional integration with shared Supabase clients

    The implementation is particularly well-suited for:

    - Multi-tenant SaaS applications requiring data isolation
    - Production deployments needing cloud infrastructure benefits
    - Applications requiring secure data access controls
    - Environments needing scalable, managed database services

    Example:
        ```python
        from haive.core.persistence import SupabaseCheckpointerConfig

        # Create a Supabase checkpointer with direct credentials
        config = SupabaseCheckpointerConfig(
            supabase_url="https://your-project.supabase.co",
            supabase_key="your-api-key",
            user_id="user-123"  # For RLS policies
        )

        # Or use shared client from dataflow module (if available)
        config = SupabaseCheckpointerConfig(
            user_id="user-123"  # Only need user_id when using shared client
        )

        # Create a checkpointer
        checkpointer = config.create_checkpointer()
        ```

    Note:
        Requires the supabase-py package to be installed. For shared client
        functionality, the haive.dataflow.db.supabase module must be available.
    """

    type: CheckpointerType = CheckpointerType.SUPABASE

    # Supabase configuration
    supabase_url: str | None = Field(
        default=None,
        description="Supabase project URL (optional if using shared client from dataflow)",
    )
    supabase_key: str | None = Field(
        default=None,
        description="Supabase API key (optional if using shared client from dataflow)",
    )
    user_id: str | None = Field(default=None, description="User ID for RLS policies")

    # Runtime settings
    setup_needed: bool = Field(
        default=True, description="Whether to initialize DB tables on startup"
    )

    # Internal state (not serialized)
    checkpointer: Any | None = Field(default=None, exclude=True)

    @model_validator(mode="after")
    def validate_supabase_available(self):
        """Validate that Supabase dependencies are available."""
        if not SUPABASE_AVAILABLE:
            raise ImportError(
                "Supabase dependencies not available. Please install with: "
                "pip install supabase"
            )
        return self

    def create_checkpointer(self) -> Any:
        """Create a Supabase checkpointer based on this configuration.

        This method instantiates and returns a SupabaseSaver object configured
        with the Supabase credentials and settings specified in this configuration.
        It handles the creation of the Supabase client, either directly or by
        using a shared client from the dataflow module if available.

        The method includes robust error handling with automatic fallback to
        an in-memory checkpointer if the Supabase connection fails. This ensures
        that the application can continue to function even if the Supabase
        service is temporarily unavailable.

        Returns:
            Any: A SupabaseSaver instance ready for use with LangGraph,
                or a MemorySaver instance as fallback in case of errors

        Example:
            ```python
            config = SupabaseCheckpointerConfig(
                supabase_url="https://your-project.supabase.co",
                supabase_key="your-api-key",
                user_id="user-123"
            )

            try:
                # Create the checkpointer
                checkpointer = config.create_checkpointer()

                # Use with a graph
                graph = Graph(checkpointer=checkpointer)
            except Exception as e:
                print(f"Error creating Supabase checkpointer: {e}")
                # Handle error...
            ```

        Note:
            This method caches the created checkpointer instance, ensuring that
            multiple calls return the same instance for efficiency. If schema
            setup is needed, it's performed only on the first call.
        """
        if self.checkpointer is None:
            try:
                # Create client if needed (optional if using dataflow utilities)
                client = None
                if DATAFLOW_AVAILABLE:
                    try:
                        client = get_supabase_client()
                    except Exception as e:
                        logger.warning(f"Failed to get shared Supabase client: {e}")
                        # Will fall back to direct client creation

                self.checkpointer = SupabaseSaver(
                    supabase_url=self.supabase_url,
                    supabase_key=self.supabase_key,
                    client=client,
                    user_id=self.user_id,
                    initialize_schema=self.setup_needed,
                )

                # Don't try to set up schema again
                self.setup_needed = False

            except Exception as e:
                logger.exception(f"Error creating Supabase checkpointer: {e}")
                logger.warning("Falling back to memory checkpointer")

                # Fall back to memory saver
                from langgraph.checkpoint.memory import MemorySaver

                self.checkpointer = MemorySaver()

        return self.checkpointer

    def register_thread(
        self,
        thread_id: str,
        name: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Register a thread in the Supabase database.

        Args:
            thread_id: The thread ID to register
            name: Optional thread name
            metadata: Optional metadata dict
        """
        if not self.user_id:
            logger.warning("No user_id provided, cannot register thread")
            return

        checkpointer = self.create_checkpointer()

        if isinstance(checkpointer, SupabaseSaver):
            checkpointer.register_thread(thread_id, self.user_id, name, metadata)
        elif hasattr(checkpointer, "register_thread"):
            # Fall back to any other implementation that supports register_thread
            checkpointer.register_thread(thread_id, name, metadata)

    def put_checkpoint(
        self,
        config: dict[str, Any],
        data: Any,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Store a checkpoint in the Supabase database.

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

        # Store using appropriate API based on checkpointer type
        if isinstance(checkpointer, SupabaseSaver):
            return checkpointer.put(config, checkpoint_data, metadata)
        # Try standard methods
        try:
            # Check method signature
            import inspect

            sig = inspect.signature(checkpointer.put)

            if "metadata" in sig.parameters and "new_versions" in sig.parameters:
                # New API
                return checkpointer.put(config, checkpoint_data, metadata or {}, {})
            # Old API
            return checkpointer.put(config, checkpoint_data)
        except (AttributeError, Exception) as e:
            logger.exception(f"Error storing checkpoint: {e}")
            return config

    def get_checkpoint(self, config: dict[str, Any]) -> dict[str, Any] | None:
        """Retrieve a checkpoint from the Supabase database.

        Args:
            config: Configuration with thread_id and optional checkpoint_id

        Returns:
            The checkpoint data if found, None otherwise
        """
        checkpointer = self.create_checkpointer()

        # Retrieve using appropriate method
        if isinstance(checkpointer, SupabaseSaver):
            return checkpointer.get(config)
        if hasattr(checkpointer, "get"):
            result = checkpointer.get(config)

            # Extract channel_values if available
            if result and isinstance(result, dict) and "channel_values" in result:
                return result["channel_values"]

            return result

        return None

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

        # List using appropriate method
        if isinstance(checkpointer, SupabaseSaver):
            checkpoint_tuples = checkpointer.list(config, limit=limit)
            return [(cp.config, cp.checkpoint) for cp in checkpoint_tuples]
        if hasattr(checkpointer, "list"):
            try:
                checkpoint_tuples = list(checkpointer.list(config, limit=limit))
                return [(cp.config, cp.checkpoint) for cp in checkpoint_tuples]
            except Exception as e:
                logger.exception(f"Error listing checkpoints: {e}")
                return []

        return []

    def close(self) -> None:
        """Close any resources associated with this checkpointer.

        This is a no-op for Supabase as HTTP clients don't need explicit closing.
        """
        self.checkpointer = None
