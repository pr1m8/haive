"""Haive-specific extension of runnable config management with PostgreSQL integration.

This module extends RunnableConfigManager to provide both Supabase authentication
integration and PostgreSQL persistence support for the Haive framework. It creates
a unified configuration system that handles authentication, session management,
and database persistence in a cohesive manner.

The HaiveRunnableConfigManager inherits all functionality from the base RunnableConfigManager
while adding specialized methods for Supabase user authentication, thread persistence,
and PostgreSQL integration. This design ensures proper user context is maintained
throughout conversation threads and persisted correctly in PostgreSQL.

Classes:
    HaiveRunnableConfigManager: Extended config manager with Supabase auth and PostgreSQL integration

Example:
    ```python
    # Create a config with Supabase authentication
    config = HaiveRunnableConfigManager.create_with_auth(
        supabase_user_id="auth0|1234567890",
        username="john.doe",
        email="john.doe@example.com"
    )

    # Add PostgreSQL persistence information
    config = HaiveRunnableConfigManager.add_persistence_info(
        config,
        db_session_id="pgsql-session-123",
        persistence_type="postgres"
    )

    # Add engine-specific configuration
    config = HaiveRunnableConfigManager.add_engine_config(
        config,
        "my_llm_engine",
        temperature=0.7
    )
    ```
"""

import copy
import json
import uuid
from datetime import datetime
from typing import Any

from langchain_core.runnables import RunnableConfig

from haive.core.config.runnable import RunnableConfigManager


class HaiveRunnableConfigManager(RunnableConfigManager):
    """Enhanced runnable config manager with Supabase authentication and PostgreSQL integration.

    Extends the base RunnableConfigManager with methods for Supabase user
    authentication, enhanced session management, and PostgreSQL persistence
    configuration. This class provides a unified interface for managing authentication
    context and database persistence throughout the Haive framework.

    Key capabilities:
    - Authentication context management with Supabase user IDs
    - Session tracking with user-agent associations
    - Thread persistence configuration for PostgreSQL
    - Permission and authorization management
    - Serialization utilities for database storage
    """

    @staticmethod
    def create_with_auth(
        supabase_user_id: str,
        username: str | None = None,
        email: str | None = None,
        tenant_id: str | None = None,
        permissions: list[str] | None = None,
        thread_id: str | None = None,
        **kwargs,
    ) -> RunnableConfig:
        """Create a RunnableConfig with Supabase authentication information.

        Args:
            supabase_user_id: The Supabase/Auth0 user ID
            username: Optional username for user identification
            email: Optional email address for user identification
            tenant_id: Optional tenant/organization ID for multi-tenant systems
            permissions: Optional list of user permissions
            thread_id: Optional thread ID for persistence (generated if not provided)
            **kwargs: Additional parameters to include in configurable section

        Returns:
            A properly structured RunnableConfig with authentication information
        """
        # Initialize with base configuration
        config = RunnableConfigManager.create(thread_id=thread_id, **kwargs)

        # Add authentication information
        auth_info = {
            "supabase_user_id": supabase_user_id,
            "auth_timestamp": datetime.now().isoformat(),
        }

        # Add optional fields if provided
        if username:
            auth_info["username"] = username
        if email:
            auth_info["email"] = email
        if tenant_id:
            auth_info["tenant_id"] = tenant_id
        if permissions:
            auth_info["permissions"] = permissions

        # Add to configurable section
        config["configurable"]["auth"] = auth_info
        config["configurable"]["user_id"] = supabase_user_id

        # Add metadata for tracing
        if "metadata" not in config:
            config["metadata"] = {}
        config["metadata"]["auth_provider"] = "supabase"

        return config

    @staticmethod
    def update_auth_info(config: RunnableConfig, **auth_updates) -> RunnableConfig:
        """Update authentication information in an existing config.

        Args:
            config: Existing RunnableConfig to update
            **auth_updates: Authentication information to update

        Returns:
            Updated RunnableConfig
        """
        result = copy.deepcopy(config)

        # Ensure configurable and auth sections exist
        if "configurable" not in result:
            result["configurable"] = {}
        if "auth" not in result["configurable"]:
            result["configurable"]["auth"] = {}

        # Update auth information
        for key, value in auth_updates.items():
            result["configurable"]["auth"][key] = value

        # Update timestamp
        result["configurable"]["auth"]["auth_timestamp"] = datetime.now().isoformat()

        return result

    @staticmethod
    def create_agent_session(
        supabase_user_id: str,
        agent_id: str,
        agent_type: str | None = None,
        session_data: dict[str, Any] | None = None,
        thread_id: str | None = None,
        **kwargs,
    ) -> RunnableConfig:
        """Create a session configuration for agent interaction.

        Args:
            supabase_user_id: The Supabase/Auth0 user ID
            agent_id: Unique identifier for the agent
            agent_type: Optional type of agent
            session_data: Optional additional session data
            thread_id: Optional thread ID (generated if not provided)
            **kwargs: Additional parameters

        Returns:
            RunnableConfig with session information
        """
        # Create base config with auth
        config = HaiveRunnableConfigManager.create_with_auth(
            supabase_user_id=supabase_user_id,
            thread_id=thread_id or str(uuid.uuid4()),
            **kwargs,
        )

        # Add session information
        session_info = {
            "agent_id": agent_id,
            "session_id": str(uuid.uuid4()),
            "started_at": datetime.now().isoformat(),
            "status": "active",
        }

        # Add optional fields
        if agent_type:
            session_info["agent_type"] = agent_type
        if session_data:
            session_info["data"] = session_data

        # Add to configurable section
        config["configurable"]["session"] = session_info

        return config

    @staticmethod
    def get_auth_info(config: RunnableConfig) -> dict[str, Any]:
        """Extract authentication information from a RunnableConfig.

        Args:
            config: RunnableConfig to extract from

        Returns:
            Authentication information dictionary or empty dict if not found
        """
        if config and "configurable" in config and "auth" in config["configurable"]:
            return config["configurable"]["auth"]
        return {}

    @staticmethod
    def get_supabase_user_id(config: RunnableConfig) -> str | None:
        """Extract Supabase user ID from a RunnableConfig.

        Args:
            config: RunnableConfig to extract from

        Returns:
            Supabase user ID if present, otherwise None
        """
        auth_info = HaiveRunnableConfigManager.get_auth_info(config)
        return auth_info.get("supabase_user_id")

    @staticmethod
    def has_permission(config: RunnableConfig, permission: str) -> bool:
        """Check if the configuration has a specific permission.

        Args:
            config: RunnableConfig to check
            permission: Permission to check for

        Returns:
            True if the permission is present, False otherwise
        """
        auth_info = HaiveRunnableConfigManager.get_auth_info(config)
        permissions = auth_info.get("permissions", [])
        return permission in permissions

    @staticmethod
    def add_permissions(config: RunnableConfig, *permissions: str) -> RunnableConfig:
        """Add permissions to the configuration.

        Args:
            config: RunnableConfig to update
            *permissions: Permissions to add

        Returns:
            Updated RunnableConfig
        """
        result = copy.deepcopy(config)

        # Ensure auth section exists
        if "configurable" not in result:
            result["configurable"] = {}
        if "auth" not in result["configurable"]:
            result["configurable"]["auth"] = {}
        if "permissions" not in result["configurable"]["auth"]:
            result["configurable"]["auth"]["permissions"] = []

        # Add permissions
        current_permissions = result["configurable"]["auth"]["permissions"]
        for permission in permissions:
            if permission not in current_permissions:
                current_permissions.append(permission)

        return result

    @staticmethod
    def get_session_info(config: RunnableConfig) -> dict[str, Any]:
        """Extract session information from a RunnableConfig.

        Args:
            config: RunnableConfig to extract from

        Returns:
            Session information dictionary or empty dict if not found
        """
        if config and "configurable" in config and "session" in config["configurable"]:
            return config["configurable"]["session"]
        return {}

    @staticmethod
    def update_session_status(config: RunnableConfig, status: str) -> RunnableConfig:
        """Update session status in the configuration.

        Args:
            config: RunnableConfig to update
            status: New session status

        Returns:
            Updated RunnableConfig
        """
        result = copy.deepcopy(config)

        # Ensure session section exists
        if "configurable" not in result:
            result["configurable"] = {}
        if "session" not in result["configurable"]:
            result["configurable"]["session"] = {}

        # Update status
        result["configurable"]["session"]["status"] = status
        result["configurable"]["session"]["updated_at"] = datetime.now().isoformat()

        return result

    @staticmethod
    def add_engine_by_id(
        config: RunnableConfig, engine_id: str, **params
    ) -> RunnableConfig:
        """Add configuration specifically targeting an engine by ID.

        Args:
            config: RunnableConfig to update
            engine_id: Engine ID to target
            **params: Parameters for the engine

        Returns:
            Updated RunnableConfig
        """
        return RunnableConfigManager.add_engine_config(config, engine_id, **params)

    @staticmethod
    def add_persistence_info(
        config: RunnableConfig,
        db_session_id: str | None = None,
        persistence_type: str = "postgres",
        db_pool_id: str | None = None,
        checkpoint_ns: str = "",
        **persistence_params,
    ) -> RunnableConfig:
        """Add PostgreSQL persistence information to a config.

        Args:
            config: Existing RunnableConfig to update
            db_session_id: Optional database session identifier
            persistence_type: Type of persistence (postgres, memory, etc.)
            db_pool_id: Optional connection pool identifier
            checkpoint_ns: Checkpoint namespace for organizing checkpoints
            **persistence_params: Additional persistence parameters

        Returns:
            Updated RunnableConfig with persistence information
        """
        result = copy.deepcopy(config)

        # Ensure configurable section exists
        if "configurable" not in result:
            result["configurable"] = {}

        # Set up persistence section
        if "persistence" not in result["configurable"]:
            result["configurable"]["persistence"] = {}

        # Add persistence information
        persistence_info = {
            "type": persistence_type,
            "timestamp": datetime.now().isoformat(),
        }

        # Add optional fields if provided
        if db_session_id:
            persistence_info["db_session_id"] = db_session_id
        if db_pool_id:
            persistence_info["db_pool_id"] = db_pool_id

        # Add checkpoint namespace
        result["configurable"]["checkpoint_ns"] = checkpoint_ns

        # Add additional parameters
        for key, value in persistence_params.items():
            persistence_info[key] = value

        # Update the persistence section
        result["configurable"]["persistence"].update(persistence_info)

        return result

    @staticmethod
    def get_persistence_info(config: RunnableConfig) -> dict[str, Any]:
        """Extract persistence information from a RunnableConfig.

        Args:
            config: RunnableConfig to extract from

        Returns:
            Persistence information dictionary or empty dict if not found
        """
        if (
            config
            and "configurable" in config
            and "persistence" in config["configurable"]
        ):
            return config["configurable"]["persistence"]
        return {}

    @staticmethod
    def is_postgres_persistence(config: RunnableConfig) -> bool:
        """Check if a config is using PostgreSQL persistence.

        Args:
            config: RunnableConfig to check

        Returns:
            True if PostgreSQL persistence is configured, False otherwise
        """
        persistence_info = HaiveRunnableConfigManager.get_persistence_info(config)
        return persistence_info.get("type", "").lower() == "postgres"

    @staticmethod
    def create_with_postgres(
        thread_id: str | None = None,
        user_id: str | None = None,
        db_connection_info: dict[str, Any] | None = None,
        checkpoint_ns: str = "",
        **kwargs,
    ) -> RunnableConfig:
        """Create a config with PostgreSQL persistence configuration.

        Args:
            thread_id: Optional thread ID (generated if not provided)
            user_id: Optional user ID for authentication context
            db_connection_info: Optional database connection parameters
            checkpoint_ns: Checkpoint namespace for organizing checkpoints
            **kwargs: Additional parameters to include in configurable section

        Returns:
            RunnableConfig with PostgreSQL persistence configuration
        """
        # Create base config
        config = RunnableConfigManager.create(
            thread_id=thread_id, user_id=user_id, **kwargs
        )

        # Add persistence information
        db_info = db_connection_info or {}
        persistence_info = {
            "type": "postgres",
            "db_session_id": db_info.get("session_id", str(uuid.uuid4())),
            "db_host": db_info.get("host", "localhost"),
            "db_port": db_info.get("port", 5432),
            "db_name": db_info.get("database", "postgres"),
            "db_user": db_info.get("user", "postgres"),
            "setup_needed": db_info.get("setup_needed", True),
            "timestamp": datetime.now().isoformat(),
        }

        # Add to configurable section
        config["configurable"]["persistence"] = persistence_info
        config["configurable"]["checkpoint_ns"] = checkpoint_ns

        return config

    @staticmethod
    def update_checkpoint_id(
        config: RunnableConfig, checkpoint_id: str
    ) -> RunnableConfig:
        """Update the checkpoint ID in a config.

        Args:
            config: RunnableConfig to update
            checkpoint_id: New checkpoint ID

        Returns:
            Updated RunnableConfig
        """
        result = copy.deepcopy(config)

        # Ensure configurable section exists
        if "configurable" not in result:
            result["configurable"] = {}

        # Update checkpoint ID
        result["configurable"]["checkpoint_id"] = checkpoint_id

        return result

    @staticmethod
    def get_checkpoint_id(config: RunnableConfig) -> str | None:
        """Extract checkpoint ID from a RunnableConfig.

        Args:
            config: RunnableConfig to extract from

        Returns:
            Checkpoint ID if present, otherwise None
        """
        return HaiveRunnableConfigManager.extract_value(config, "checkpoint_id")

    @staticmethod
    def get_checkpoint_ns(config: RunnableConfig) -> str:
        """Extract checkpoint namespace from a RunnableConfig.

        Args:
            config: RunnableConfig to extract from

        Returns:
            Checkpoint namespace or empty string if not found
        """
        return HaiveRunnableConfigManager.extract_value(config, "checkpoint_ns", "")

    @staticmethod
    def create_thread_checkpoint_config(
        thread_id: str,
        checkpoint_id: str | None = None,
        checkpoint_ns: str = "",
        **kwargs,
    ) -> RunnableConfig:
        """Create a minimal config for checkpoint operations with thread ID.

        Args:
            thread_id: Thread ID for the conversation
            checkpoint_id: Optional specific checkpoint ID
            checkpoint_ns: Checkpoint namespace
            **kwargs: Additional parameters

        Returns:
            RunnableConfig suitable for checkpoint operations
        """
        config = {
            "configurable": {"thread_id": thread_id, "checkpoint_ns": checkpoint_ns}
        }

        if checkpoint_id:
            config["configurable"]["checkpoint_id"] = checkpoint_id

        # Add any additional parameters
        for key, value in kwargs.items():
            config["configurable"][key] = value

        return config

    @staticmethod
    def serialize_to_json(config: RunnableConfig) -> str:
        """Serialize a RunnableConfig to a JSON string.

        Args:
            config: RunnableConfig to serialize

        Returns:
            JSON string representation
        """

        # Use a custom encoder function to handle datetime objects
        def encoder(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

        return json.dumps(config, default=encoder)

    @staticmethod
    def deserialize_from_json(json_str: str) -> RunnableConfig:
        """Deserialize a RunnableConfig from a JSON string.

        Args:
            json_str: JSON string to deserialize

        Returns:
            Deserialized RunnableConfig
        """
        return json.loads(json_str)
