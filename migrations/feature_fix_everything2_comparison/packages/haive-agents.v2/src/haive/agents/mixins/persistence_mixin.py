"""Persistence Mixin for Agent classes.

This mixin provides persistence functionality including checkpointer setup,
store management, and configuration handling. It separates persistence
concerns from the main Agent class while ensuring proper serialization.
"""

import logging
from typing import Any

from haive.core.persistence.types import CheckpointerMode
from langchain_core.runnables import RunnableConfig

logger = logging.getLogger(__name__)


class PersistenceMixin:
    """Mixin for agent persistence functionality.

    Provides methods for setting up checkpointers, stores, and managing
    persistence configuration in a serializable way.
    """

    def _setup_persistence_from_config(self) -> None:
        """Set up persistence using the agent's serializable fields.

        This method sets up checkpointer and store based on the Agent's
        serializable persistence fields.

        Persistence behavior:
        - persistence=False: Persistence is explicitly disabled
        - persistence=None: Use memory persistence (safe default for testing)
        - persistence=True: Use default persistence (PostgreSQL if available)
        - persistence=<config>: Use specific configuration
        """
        # Check if persistence is explicitly disabled (False)
        if self.persistence is False:
            logger.debug(
                f"Persistence explicitly disabled for {
                    getattr(
                        self,
                        'name',
                        'Agent')}"
            )
            self.checkpointer = None
            self.store = None
            # Still set up runnable config for recursion limit
            if not self.runnable_config:
                self.runnable_config = {
                    "configurable": {
                        "thread_id": self._generate_default_thread_id(),
                        "recursion_limit": 100,
                    }
                }
            return

        # If persistence is None, use memory persistence as a safe default
        if self.persistence is None:
            logger.debug(
                f"Using memory persistence for {
                    getattr(
                        self,
                        'name',
                        'Agent')} (persistence=None)"
            )
            try:
                from haive.core.persistence.memory import MemoryCheckpointerConfig

                self.persistence = MemoryCheckpointerConfig()
            except ImportError:
                logger.warning(
                    "Could not import MemoryCheckpointerConfig, persistence disabled"
                )
                self.checkpointer = None
                self.store = None
                return

        # Set up defaults if persistence=True
        elif self.persistence is True:
            self._setup_default_persistence()

        # Now set up the actual persistence objects
        self._setup_checkpointer_from_fields()
        self._setup_store_from_fields()

    def _sync_persistence_fields_from_config(self) -> None:
        """Sync serializable persistence fields from config."""
        if not self.config:
            return

        # Sync persistence config
        if hasattr(self.config, "persistence") and self.config.persistence:
            self.persistence = self.config.persistence

        # Sync checkpoint mode
        if hasattr(self.config, "checkpoint_mode"):
            self.checkpoint_mode = self.config.checkpoint_mode
        elif hasattr(self.config, "persistence") and hasattr(
            self.config.persistence, "mode"
        ):
            # Convert from CheckpointerMode enum to string
            mode = self.config.persistence.mode
            if hasattr(mode, "value"):
                self.checkpoint_mode = (
                    "async" if mode == CheckpointerMode.ASYNC else "sync"
                )
            else:
                self.checkpoint_mode = "async" if mode == "async" else "sync"

        # Sync other flags
        if hasattr(self.config, "add_store"):
            self.add_store = self.config.add_store
        if hasattr(self.config, "debug"):
            self.debug = self.config.debug
        if hasattr(self.config, "save_history"):
            self.save_history = self.config.save_history
        if hasattr(self.config, "visualize"):
            self.visualize = self.config.visualize

        # Sync runnable config
        if hasattr(self.config, "runnable_config") and not self.runnable_config:
            self.runnable_config = self.config.runnable_config

    def _setup_default_persistence(self) -> None:
        """Set up default persistence configuration.

        Creates default PostgreSQL persistence with recursion limit 100,
        using Supabase connection string from environment if available,
        falling back to memory persistence if PostgreSQL unavailable.
        """
        # Set up default runnable config with recursion limit 100
        if not self.runnable_config:

            self.runnable_config = {
                "configurable": {
                    "thread_id": self._generate_default_thread_id(),
                    "recursion_limit": 100,
                }
            }
        elif "configurable" not in self.runnable_config:
            self.runnable_config["configurable"] = {"recursion_limit": 100}
        elif "recursion_limit" not in self.runnable_config["configurable"]:
            self.runnable_config["configurable"]["recursion_limit"] = 100

        # Try to set up default PostgreSQL persistence
        try:
            from haive.core.engine.agent.config import POSTGRES_AVAILABLE

            if POSTGRES_AVAILABLE:
                import os

                from haive.core.persistence.postgres_config import (
                    PostgresCheckpointerConfig,
                )
                from haive.core.persistence.types import (
                    CheckpointerMode,
                    CheckpointStorageMode,
                )

                # Check for connection string from environment
                connection_string = os.getenv("POSTGRES_CONNECTION_STRING")

                if connection_string:
                    # Use the connection string from environment (likely Supabase)
                    # Create unique pool per agent to avoid prepared statement
                    # conflicts
                    agent_name = getattr(self, "name", "Agent")
                    app_name = f"haive_{agent_name}_{id(self)}"

                    self.persistence = PostgresCheckpointerConfig(
                        connection_string=connection_string,
                        mode=CheckpointerMode.SYNC,
                        storage_mode=CheckpointStorageMode.FULL,
                        prepare_threshold=None,  # Disable prepared statements completely
                        auto_commit=True,  # Ensure auto-commit is enabled
                        min_pool_size=1,  # Minimal pool to reduce conflicts
                        max_pool_size=2,  # Very small pool for isolation
                        connection_kwargs={
                            "prepare_threshold": None,  # Extra explicit disable
                            "application_name": app_name,  # Unique app name for identification
                        },
                    )
                    logger.info(
                        f"Set up PostgreSQL persistence for {app_name} (prepared statements disabled)"
                    )
                else:
                    # Use default local PostgreSQL config
                    agent_name = getattr(self, "name", "Agent")
                    app_name = f"haive_{agent_name}_{id(self)}"

                    self.persistence = PostgresCheckpointerConfig(
                        mode=CheckpointerMode.SYNC,
                        storage_mode=CheckpointStorageMode.FULL,
                        prepare_threshold=None,  # Disable prepared statements completely
                        auto_commit=True,  # Ensure auto-commit is enabled
                        min_pool_size=1,  # Minimal pool to reduce conflicts
                        max_pool_size=2,  # Very small pool for isolation
                        connection_kwargs={
                            "prepare_threshold": None,  # Extra explicit disable
                            "application_name": app_name,  # Unique app name for identification
                        },
                    )
                    logger.info(
                        f"Set up default PostgreSQL persistence for {app_name} (prepared statements disabled)"
                    )
            else:
                from haive.core.persistence.memory import MemoryCheckpointerConfig

                self.persistence = MemoryCheckpointerConfig()
                logger.debug(
                    f"Set up default memory persistence for {
                        getattr(
                            self, 'name', 'Agent')}"
                )

        except Exception as e:
            logger.warning(f"Failed to set up default persistence: {e}")
            # Fallback to memory
            try:
                from haive.core.persistence.memory import MemoryCheckpointerConfig

                self.persistence = MemoryCheckpointerConfig()
                logger.debug(
                    f"Using memory persistence fallback for {
                        getattr(
                            self, 'name', 'Agent')}"
                )
            except Exception as e2:
                logger.exception(f"Failed to set up memory persistence fallback: {e2}")
                self.persistence = None

    def _setup_checkpointer_from_fields(self) -> None:
        """Set up checkpointer using the persistence field."""
        if not self.persistence:
            logger.warning(
                f"No persistence config found for {
                    getattr(
                        self,
                        'name',
                        'Agent')}"
            )
            return

        try:
            from haive.core.persistence.handlers import setup_checkpointer

            # Create a minimal config-like object for the handler
            class PersistenceConfig:
                def __init__(self, persistence, checkpoint_mode="sync") -> None:
                    self.persistence = persistence
                    self.checkpoint_mode = checkpoint_mode

            temp_config = PersistenceConfig(self.persistence, self.checkpoint_mode)
            self.checkpointer = setup_checkpointer(temp_config)

            # Set up private checkpoint mode tracking
            self._checkpoint_mode = self.checkpoint_mode

            logger.debug(
                f"Checkpointer set up for {getattr(self, 'name', 'Agent')}: "
                f"{type(self.checkpointer).__name__}"
            )

        except Exception as e:
            logger.exception(f"Failed to set up checkpointer: {e}")
            # Set up memory fallback
            try:
                from langgraph.checkpoint.memory import MemorySaver

                self.checkpointer = MemorySaver()
                logger.debug("Using MemorySaver fallback")
            except ImportError:
                logger.exception("Could not import MemorySaver, persistence disabled")
                self.checkpointer = None

    def _setup_async_checkpointer_from_fields(self) -> None:
        """Set up async checkpointer using the persistence field."""
        if not self.persistence:
            return

        try:

            # Create a minimal config-like object for the handler
            class PersistenceConfig:
                def __init__(self, persistence, checkpoint_mode="async") -> None:
                    self.persistence = persistence
                    self.checkpoint_mode = checkpoint_mode

            PersistenceConfig(self.persistence, "async")

            # Note: This would need to be called in an async context
            # For now, we'll set a flag to set it up later
            self._async_setup_pending = True

            logger.debug(
                f"Async checkpointer setup pending for {
                    getattr(
                        self,
                        'name',
                        'Agent')}"
            )

        except Exception as e:
            logger.exception(f"Failed to prepare async checkpointer setup: {e}")

    def _setup_store_from_fields(self) -> None:
        """Set up store using the add_store field."""
        self.store = None

        if not self.add_store:
            return

        try:
            # Check if we have a PostgreSQL checkpointer for store
            # compatibility
            if (
                hasattr(self, "checkpointer")
                and self.checkpointer
                and "Postgres" in type(self.checkpointer).__name__
            ):
                # Try to use PostgreSQL store if available
                try:
                    from haive.core.persistence.store.factory import create_store
                    from haive.core.persistence.store.types import StoreType

                    # Get connection info from persistence config if available
                    if hasattr(self, "persistence") and hasattr(
                        self.persistence, "get_connection_uri"
                    ):
                        connection_string = self.persistence.get_connection_uri()

                        # Determine if we need sync or async store
                        store_type = (
                            StoreType.POSTGRES_ASYNC
                            if self.checkpoint_mode == "async"
                            else StoreType.POSTGRES_SYNC
                        )

                        # Create PostgreSQL store
                        self.store = create_store(
                            store_type=store_type, connection_string=connection_string
                        )
                        logger.info(
                            f"PostgreSQL store added successfully ({
                                store_type.value})"
                        )
                    else:
                        # Fall back to memory store if no connection info
                        from langgraph.store.memory import InMemoryStore

                        self.store = InMemoryStore()
                        logger.debug(
                            "InMemoryStore added (no PostgreSQL connection info)"
                        )

                except ImportError:
                    # PostgreSQL store not available, use memory store
                    from langgraph.store.memory import InMemoryStore

                    self.store = InMemoryStore()
                    logger.debug("InMemoryStore added (PostgreSQL store not available)")
                except Exception as e:
                    logger.warning(f"Failed to create PostgreSQL store: {e}")
                    from langgraph.store.memory import InMemoryStore

                    self.store = InMemoryStore()
                    logger.debug("InMemoryStore added (fallback from PostgreSQL error)")
            else:
                # Use InMemoryStore for other checkpointer types
                from langgraph.store.memory import InMemoryStore

                self.store = InMemoryStore()
                logger.debug("InMemoryStore added")

        except ImportError:
            try:
                from langgraph.store.base import BaseStore

                self.store = BaseStore()
                logger.debug("BaseStore added")
            except ImportError:
                logger.warning(
                    "Could not import any Store class, store functionality disabled"
                )
        except Exception as e:
            logger.warning(f"Failed to set up store: {e}")

    async def _asetup_persistence_from_fields(self) -> None:
        """Set up async persistence using the persistence field."""
        # First ensure sync persistence is set up
        if not hasattr(self, "checkpointer") or self.checkpointer is None:
            self._setup_persistence_from_config()

        # Now set up async checkpointer
        if not self.persistence:
            return

        try:
            from haive.core.persistence.handlers import setup_async_checkpointer

            # Create a minimal config-like object for the handler
            class PersistenceConfig:
                def __init__(self, persistence) -> None:
                    self.persistence = persistence
                    self.checkpoint_mode = "async"

            temp_config = PersistenceConfig(self.persistence)
            self._async_checkpointer = await setup_async_checkpointer(temp_config)
            self._checkpoint_mode = "async"

            logger.debug(
                f"Async checkpointer set up for {
                    getattr(
                        self,
                        'name',
                        'Agent')}: "
                f"{
                    type(
                        self._async_checkpointer).__name__}"
            )

        except Exception as e:
            logger.exception(f"Failed to set up async checkpointer: {e}")

    def get_persistence_config(self) -> dict[str, Any]:
        """Get the current persistence configuration as a serializable dict."""
        return {
            "persistence": self.persistence,
            "checkpoint_mode": self.checkpoint_mode,
            "add_store": self.add_store,
            "debug": self.debug,
            "save_history": self.save_history,
            "visualize": self.visualize,
        }

    def update_persistence_config(self, **config_updates) -> None:
        """Update persistence configuration and re-setup if needed."""
        # Update the serializable fields
        for key, value in config_updates.items():
            if hasattr(self, key):
                setattr(self, key, value)

        # Re-setup persistence if checkpointer-related fields changed
        checkpointer_fields = {"persistence", "checkpoint_mode"}
        if any(field in config_updates for field in checkpointer_fields):
            self._setup_checkpointer_from_fields()

        # Re-setup store if store-related fields changed
        if "add_store" in config_updates:
            self._setup_store_from_fields()

    def get_effective_runnable_config(self, **overrides) -> RunnableConfig:
        """Get the effective runnable config with defaults and overrides."""
        # Start with agent's runnable config
        config = self.runnable_config.copy() if self.runnable_config else {}

        # Ensure configurable section exists
        if "configurable" not in config:
            config["configurable"] = {}

        # Add default values
        if "thread_id" not in config["configurable"]:
            # Generate consistent thread_id based on agent identity for
            # automatic persistence
            config["configurable"]["thread_id"] = self._generate_default_thread_id()
        if "recursion_limit" not in config["configurable"]:
            config["configurable"]["recursion_limit"] = 100

        # Add checkpoint mode
        config["configurable"]["checkpoint_mode"] = self.checkpoint_mode

        # Apply overrides
        for key, value in overrides.items():
            if key == "configurable" and isinstance(value, dict):
                config["configurable"].update(value)
            else:
                config[key] = value

        return config

    def _generate_default_thread_id(self) -> str:
        """Generate a unique thread_id for each agent instance.

        This method now generates truly unique thread IDs using UUIDs to prevent
        collisions when multiple instances of the same agent run concurrently.

        For cases where you need consistent thread IDs (e.g., resuming conversations),
        explicitly pass a thread_id to the run() method.
        """
        import uuid

        # Generate a unique UUID for this agent instance
        unique_id = str(uuid.uuid4())

        # Include agent name for readability in logs/debugging
        agent_name = getattr(self, "name", "agent")

        # Create thread_id with format: {agent_name}_{uuid}
        # This ensures uniqueness while maintaining readability
        thread_id = f"{agent_name}_{unique_id}"

        return thread_id
