# haive/core/engine/agent/mixins/state_mixin.py

import json
import logging
import os
import uuid
from datetime import datetime
from typing import Any

from haive.core.persistence.handlers import ensure_pool_open
from haive.core.utils.pydantic_utils import ensure_json_serializable
from langchain_core.runnables import RunnableConfig

logger = logging.getLogger(__name__)


class StateMixin:
    """Mixin for agent state management functionality."""

    def __init__(self, *args, **kwargs):
        """Initialize the mixin with state tracking attributes."""
        super().__init__(*args, **kwargs)
        # Use regular attributes instead of trying to add Pydantic fields
        self._state_filename = None

    def save_state_history(self, runnable_config: RunnableConfig | None = None) -> bool:
        """Save the current agent state to a JSON file.

        Args:
            runnable_config: Optional runnable configuration

        Returns:
            True if successful, False otherwise
        """
        if not hasattr(self, "_app") or not self._app:
            logger.error("Cannot save state history: Workflow graph not compiled")
            return False

        # Use provided runnable config or create default
        if not runnable_config:
            runnable_config = (
                self._prepare_runnable_config()
                if hasattr(self, "_prepare_runnable_config")
                else {}
            )

        try:
            # Get state from app
            state_json = self._app.get_state(runnable_config)

            if not state_json:
                logger.warning(f"No state history available for {self.name}")
                return False

            # Ensure state is JSON serializable
            state_json = ensure_json_serializable(state_json)

            # Create state filename if not exists
            if not hasattr(self, "_state_filename") or self._state_filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                # Get output directory from config or use default
                output_dir = "resources/state_history"
                if hasattr(self, "config") and self.config:
                    output_dir = getattr(self.config, "output_dir", output_dir)

                # Create directory if it doesn't exist
                os.makedirs(output_dir, exist_ok=True)

                # Generate filename
                agent_name = getattr(self, "name", "agent")
                safe_name = agent_name.replace(" ", "_").replace("/", "_")
                self._state_filename = os.path.join(
                    output_dir, f"{safe_name}_{timestamp}.json"
                )

            # Save to file
            with open(self._state_filename, "w", encoding="utf-8") as f:
                json.dump(state_json, f, indent=4)

            logger.info(f"State history saved to: {self._state_filename}")
            return True

        except Exception as e:
            logger.exception(f"Error saving state history: {e}")
            return False

    async def save_state_history_async(
        self, runnable_config: RunnableConfig | None = None
    ) -> bool:
        """Asynchronously save the current agent state to a JSON file.

        Args:
            runnable_config: Optional runnable configuration

        Returns:
            True if successful, False otherwise
        """
        import asyncio

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, lambda: self.save_state_history(runnable_config)
        )

    def inspect_state(
        self, thread_id: str | None = None, config: RunnableConfig | None = None
    ) -> None:
        """Inspect the current state of the agent.

        Args:
            thread_id: Optional thread ID for persistence
            config: Optional runtime configuration
        """
        if not hasattr(self, "_app") or not self._app:
            logger.error("Cannot inspect state: Workflow graph not compiled")
            return

        # Prepare runtime configuration
        runtime_config = (
            self._prepare_runnable_config(thread_id=thread_id, config=config)
            if hasattr(self, "_prepare_runnable_config")
            else config
        )

        try:
            # Get current state
            state = self._app.get_state(runtime_config)

            if not state:
                logger.warning("No state available")
                return

            # Extract thread ID from config
            thread_id = (
                runtime_config["configurable"].get("thread_id", "unknown")
                if runtime_config
                else "unknown"
            )

            # Log the state
            logger.info(f"State inspection for thread {thread_id}")

            # Handle different state formats
            if hasattr(state, "values"):
                values = state.values
                metadata = getattr(state, "metadata", {})
                created_at = getattr(state, "created_at", "unknown")

                logger.info(f"State values: {values}")
                if metadata:
                    logger.info(f"Metadata: {metadata}")
                logger.info(f"Created at: {created_at}")

            elif isinstance(state, dict):
                logger.info(f"State dictionary: {state}")
            else:
                logger.info(f"State (Type: {type(state).__name__}): {state}")

        except Exception as e:
            logger.exception(f"Error inspecting state: {e}")

    async def inspect_state_async(
        self, thread_id: str | None = None, config: RunnableConfig | None = None
    ) -> None:
        """Asynchronously inspect the current state of the agent.

        Args:
            thread_id: Optional thread ID for persistence
            config: Optional runtime configuration
        """
        import asyncio

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: self.inspect_state(thread_id, config))

    def reset_state(
        self, thread_id: str | None = None, config: RunnableConfig | None = None
    ) -> bool:
        """Reset the agent's state for a thread.

        Args:
            thread_id: Optional thread ID for persistence
            config: Optional runtime configuration

        Returns:
            True if successful, False otherwise
        """
        checkpointer = getattr(self, "checkpointer", None)
        if not checkpointer:
            logger.warning("Cannot reset state: No checkpointer configured")
            return False

        # Prepare runtime configuration
        runtime_config = (
            self._prepare_runnable_config(thread_id=thread_id, config=config)
            if hasattr(self, "_prepare_runnable_config")
            else config
        )

        # Extract thread ID from config
        thread_id = (
            runtime_config["configurable"].get("thread_id", None)
            if runtime_config
            else thread_id
        )
        if not thread_id:
            logger.warning("Cannot reset state: No thread ID provided")
            return False

        try:
            # Connect to checkpointer
            ensure_pool_open(checkpointer)

            # Reset state based on checkpointer type
            if hasattr(checkpointer, "delete"):
                checkpointer.delete(thread_id)
            elif hasattr(checkpointer, "conn") and checkpointer.conn:
                conn = checkpointer.conn
                with conn.connection() as db_conn, db_conn.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM checkpoints WHERE thread_id = %s", (thread_id,)
                    )

            logger.info(f"State reset successfully for thread {thread_id}")
            return True

        except Exception as e:
            logger.exception(f"Error resetting state: {e}")
            return False

    async def reset_state_async(
        self, thread_id: str | None = None, config: RunnableConfig | None = None
    ) -> bool:
        """Asynchronously reset the agent's state for a thread.

        Args:
            thread_id: Optional thread ID for persistence
            config: Optional runtime configuration

        Returns:
            True if successful, False otherwise
        """
        import asyncio

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, lambda: self.reset_state(thread_id, config)
        )

    def load_from_state(
        self, state_data: dict[str, Any] | str, thread_id: str | None = None
    ) -> bool:
        """Load agent state from a saved state file or dictionary.

        Args:
            state_data: Dictionary or path to JSON file containing state data
            thread_id: Optional thread ID for persistence

        Returns:
            True if successful, False otherwise
        """
        checkpointer = getattr(self, "checkpointer", None)
        if not checkpointer:
            logger.warning("Cannot load state: No checkpointer configured")
            return False

        # Generate thread ID if not provided
        if not thread_id:
            thread_id = str(uuid.uuid4())

        # Load state from string path if provided
        if isinstance(state_data, str) and os.path.exists(state_data):
            try:
                with open(state_data) as f:
                    state_data = json.load(f)
            except Exception as e:
                logger.exception(f"Error loading state file: {e}")
                return False

        # Ensure state is a dictionary
        if not isinstance(state_data, dict):
            logger.error(f"Invalid state data type: {type(state_data)}")
            return False

        try:
            # Connect to checkpointer
            ensure_pool_open(checkpointer)

            # Create runtime config with thread ID
            runtime_config = (
                self._prepare_runnable_config(thread_id=thread_id)
                if hasattr(self, "_prepare_runnable_config")
                else {"configurable": {"thread_id": thread_id}}
            )
            runtime_config["configurable"]["recursion_limit"] = 100
            # Process state based on its format
            values = state_data.get("values", state_data)

            # Use checkpoint save mechanism
            if hasattr(self._app, "checkpoint_save"):
                config = runtime_config.copy()
                self._app.checkpoint_save(thread_id, values, config)
            elif hasattr(checkpointer, "save"):
                checkpointer.save(thread_id, values)
            else:
                raise NotImplementedError("No checkpoint save mechanism available")

            logger.info(f"State loaded successfully for thread {thread_id}")
            return True

        except Exception as e:
            logger.exception(f"Error loading state: {e}")
            return False

    async def load_from_state_async(
        self, state_data: dict[str, Any] | str, thread_id: str | None = None
    ) -> bool:
        """Asynchronously load agent state from a saved state file or dictionary.

        Args:
            state_data: Dictionary or path to JSON file containing state data
            thread_id: Optional thread ID for persistence

        Returns:
            True if successful, False otherwise
        """
        import asyncio

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, lambda: self.load_from_state(state_data, thread_id)
        )

    def get_state_filename(self) -> str | None:
        """Get the current state filename if one has been generated."""
        return getattr(self, "_state_filename", None)

    def set_state_filename(self, filename: str) -> None:
        """Set a custom state filename."""
        self._state_filename = filename
