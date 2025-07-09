"""Checkpointer mixin for stateful graphs and execution persistence.

This module provides a mixin that adds checkpointing capabilities to any class
that uses LangGraph or LangChain for stateful execution. It handles both
synchronous and asynchronous checkpointing patterns, state restoration, and
runtime configuration management.

Usage:
    ```python
    from pydantic import BaseModel, Field
    from langgraph.graph import StateGraph
    from haive.core.common.mixins import CheckpointerMixin
    from haive.core.persistence.config import CheckpointerConfig

    class MyAgent(CheckpointerMixin, BaseModel):
        # Define the required fields
        persistence: Optional[CheckpointerConfig] = Field(default=None)
        checkpoint_mode: str = Field(default="sync")

        def __init__(self, **data):
            super().__init__(**data)
            # Create graph
            builder = StateGraph(...)
            self.app = builder.compile()

        # Use run with automatic checkpointing
        def process(self, input_data, thread_id=None):
            return self.run(input_data, thread_id=thread_id)

        # Use streaming with automatic checkpointing
        def process_stream(self, input_data, thread_id=None):
            return self.stream(input_data, thread_id=thread_id)
    ```
"""

import asyncio
import logging
import uuid
from abc import ABC
from collections.abc import AsyncGenerator
from typing import Any, Dict, Generator, Optional, Union

from langchain_core.runnables import RunnableConfig
from langgraph.graph.graph import CompiledGraph
from pydantic import BaseModel, PrivateAttr

from haive.core.config.runnable import RunnableConfigManager
from haive.core.persistence.handlers import (
    ensure_async_pool_open,
    ensure_pool_open,
    prepare_merged_input,
    register_async_thread_if_needed,
    register_thread_if_needed,
)

logger = logging.getLogger(__name__)


class CheckpointerMixin(BaseModel):
    """Mixin that provides checkpointing capabilities for stateful graph execution.

    This mixin adds methods for running stateful graph executions with
    checkpointing support, including automatic state restoration, thread
    management, and proper configuration handling for both synchronous and
    asynchronous execution patterns.

    The mixin expects the host class to provide:
    - persistence: Optional[CheckpointerConfig] - Configuration for the checkpointer
    - checkpoint_mode: str - Mode of checkpointing ("sync", "async", or "none")
    - runnable_config: RunnableConfig - Base configuration for runnables
    - input_schema, state_schema (optional) - Schemas for input and state validation
    - app or compile() method - The LangGraph compiled application

    Attributes:
        None publicly, but requires the above attributes from the host class.
    """

    # Private attributes for runtime checkpointer instances (not serialized)
    _sync_checkpointer: Any = PrivateAttr(default=None)
    _async_checkpointer: Any = PrivateAttr(default=None)
    _checkpointer_initialized: bool = PrivateAttr(default=False)
    _async_setup_pending: bool = PrivateAttr(default=False)

    def _ensure_checkpointer_initialized(self) -> None:
        """Initialize checkpointers if not already done.

        This method creates the appropriate checkpointer instances
        based on the persistence configuration and checkpoint mode.
        """
        if self._checkpointer_initialized:
            return

        # Get persistence config
        persistence = getattr(self, "persistence", None)
        checkpoint_mode = getattr(self, "checkpoint_mode", "sync")

        if persistence is None or checkpoint_mode == "none":
            self._sync_checkpointer = None
            self._async_checkpointer = None
        else:
            # Create sync checkpointer
            self._sync_checkpointer = persistence.create_checkpointer()

            # Mark async setup as pending if needed
            if checkpoint_mode == "async":
                self._async_setup_pending = True

        self._checkpointer_initialized = True

    async def _ensure_async_checkpointer_initialized(self) -> None:
        """Initialize async checkpointer if needed.

        This method creates the asynchronous checkpointer instance
        if async mode is enabled and setup is pending.
        """
        if not self._async_setup_pending:
            return

        persistence = getattr(self, "persistence", None)
        if persistence and hasattr(persistence, "create_async_checkpointer"):
            try:
                self._async_checkpointer = await persistence.create_async_checkpointer()
                logger.debug(
                    f"Initialized async checkpointer: {type(self._async_checkpointer).__name__}"
                )
            except Exception as e:
                logger.warning(f"Failed to create async checkpointer: {e}")
                self._async_checkpointer = None

        self._async_setup_pending = False

    def get_checkpointer(self, async_mode: bool = False) -> Any:
        """Get the appropriate checkpointer.

        Args:
            async_mode: Whether to return the async checkpointer.

        Returns:
            The appropriate checkpointer instance or None if not available.
        """
        self._ensure_checkpointer_initialized()

        if async_mode:
            return self._async_checkpointer
        return self._sync_checkpointer

    def _prepare_runnable_config(
        self,
        thread_id: Optional[str] = None,
        config: Optional[RunnableConfig] = None,
        **kwargs,
    ) -> RunnableConfig:
        """Prepare runnable config with thread management.

        This method creates or merges runnable configurations with
        appropriate thread management and checkpointing settings.

        Args:
            thread_id: Optional thread ID for the execution.
            config: Optional base configuration to extend.
            **kwargs: Additional configuration parameters.

        Returns:
            The prepared runnable configuration.
        """
        # Get base config from the class
        base_config = getattr(self, "runnable_config", None)

        # Create or merge configs
        if thread_id:
            runtime_config = RunnableConfigManager.create(
                thread_id=thread_id, user_id=kwargs.pop("user_id", None)
            )
            if base_config:
                runtime_config = RunnableConfigManager.merge(
                    base_config, runtime_config
                )
            if config:
                runtime_config = RunnableConfigManager.merge(runtime_config, config)
        elif config:
            if base_config:
                runtime_config = RunnableConfigManager.merge(base_config, config)
            else:
                runtime_config = config
        else:
            runtime_config = base_config or RunnableConfigManager.create()

        # Ensure required fields
        if "configurable" not in runtime_config:
            runtime_config["configurable"] = {}
        if "thread_id" not in runtime_config["configurable"]:
            runtime_config["configurable"]["thread_id"] = str(uuid.uuid4())

        # Add checkpoint mode
        checkpoint_mode = getattr(self, "checkpoint_mode", "sync")
        runtime_config["configurable"]["checkpoint_mode"] = kwargs.pop(
            "checkpoint_mode", checkpoint_mode
        )

        # Add other kwargs
        for key, value in kwargs.items():
            if key.startswith("configurable_"):
                param_name = key.replace("configurable_", "")
                runtime_config["configurable"][param_name] = value
            elif key == "configurable" and isinstance(value, dict):
                runtime_config["configurable"].update(value)
            else:
                runtime_config[key] = value

        return runtime_config

    def run(
        self,
        input_data: Any,
        thread_id: Optional[str] = None,
        config: Optional[RunnableConfig] = None,
        **kwargs,
    ) -> Any:
        """Run with checkpointer support.

        This method runs a graph execution with checkpointing support,
        automatically handling state restoration and persistence.

        Args:
            input_data: The input data for the execution.
            thread_id: Optional thread ID for state tracking.
            config: Optional configuration override.
            **kwargs: Additional configuration parameters.

        Returns:
            The result of the graph execution.
        """
        self._ensure_checkpointer_initialized()

        # Get the compiled app - this should be implemented by the class using the mixin
        app = self.compile() if hasattr(self, "compile") else self.app

        # Prepare runtime config
        runtime_config = self._prepare_runnable_config(
            thread_id=thread_id, config=config, **kwargs
        )

        thread_id = runtime_config["configurable"]["thread_id"]
        checkpointer = self.get_checkpointer(async_mode=False)

        # Register thread if needed
        if checkpointer and thread_id:
            register_thread_if_needed(checkpointer, thread_id)

        # Get previous state if available
        previous_state = None
        try:
            if checkpointer and thread_id:
                previous_state = app.get_state(runtime_config)
        except Exception as e:
            logger.warning(f"Error retrieving previous state: {e}")

        # Prepare merged input
        if previous_state:
            try:
                input_schema = getattr(self, "input_schema", None)
                state_schema = getattr(self, "state_schema", None)

                input_data = prepare_merged_input(
                    input_data,
                    previous_state,
                    runtime_config,
                    input_schema,
                    state_schema,
                )
            except Exception as e:
                logger.warning(f"Error merging with previous state: {e}")

        # Invoke the app
        return app.invoke(input_data, runtime_config)

    async def arun(
        self,
        input_data: Any,
        thread_id: Optional[str] = None,
        config: Optional[RunnableConfig] = None,
        **kwargs,
    ) -> Any:
        """Async run with checkpointer support.

        This method runs a graph execution asynchronously with checkpointing
        support, automatically handling state restoration and persistence.

        Args:
            input_data: The input data for the execution.
            thread_id: Optional thread ID for state tracking.
            config: Optional configuration override.
            **kwargs: Additional configuration parameters.

        Returns:
            The result of the graph execution.
        """
        self._ensure_checkpointer_initialized()
        await self._ensure_async_checkpointer_initialized()

        # Get the compiled app
        app = self.compile() if hasattr(self, "compile") else self.app

        # Check if we should use async mode
        checkpoint_mode = kwargs.get(
            "checkpoint_mode", getattr(self, "checkpoint_mode", "sync")
        )
        use_async = checkpoint_mode == "async" and self._async_checkpointer

        # Prepare runtime config
        runtime_config = self._prepare_runnable_config(
            thread_id=thread_id,
            config=config,
            checkpoint_mode=checkpoint_mode,
            **kwargs,
        )

        thread_id = runtime_config["configurable"]["thread_id"]

        if use_async:
            # Use async checkpointer - recompile app with it
            await register_async_thread_if_needed(self._async_checkpointer, thread_id)

            # Get store if available
            store = (
                getattr(app, "store", None)
                if hasattr(app, "store")
                else getattr(self, "store", None)
            )

            # Recompile with async checkpointer
            async_app = app.graph.compile(
                checkpointer=self._async_checkpointer, store=store
            )

            # Get previous state
            previous_state = None
            try:
                previous_state = await async_app.aget_state(runtime_config)
            except Exception as e:
                logger.warning(f"Error retrieving previous state: {e}")

            # Prepare merged input
            if previous_state:
                try:
                    input_schema = getattr(self, "input_schema", None)
                    state_schema = getattr(self, "state_schema", None)

                    input_data = prepare_merged_input(
                        input_data,
                        previous_state,
                        runtime_config,
                        input_schema,
                        state_schema,
                    )
                except Exception as e:
                    logger.warning(f"Error merging with previous state: {e}")

            # Invoke async app
            return await async_app.ainvoke(input_data, runtime_config)
        else:
            # Use sync checkpointer
            checkpointer = self.get_checkpointer(async_mode=False)

            if checkpointer and thread_id:
                register_thread_if_needed(checkpointer, thread_id)

            # Get previous state
            previous_state = None
            try:
                if checkpointer and thread_id:
                    previous_state = app.get_state(runtime_config)
            except Exception as e:
                logger.warning(f"Error retrieving previous state: {e}")

            # Prepare merged input
            if previous_state:
                try:
                    input_schema = getattr(self, "input_schema", None)
                    state_schema = getattr(self, "state_schema", None)

                    input_data = prepare_merged_input(
                        input_data,
                        previous_state,
                        runtime_config,
                        input_schema,
                        state_schema,
                    )
                except Exception as e:
                    logger.warning(f"Error merging with previous state: {e}")

            # Use ainvoke if available, otherwise thread pool
            if hasattr(app, "ainvoke"):
                return await app.ainvoke(input_data, runtime_config)
            else:
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(
                    None, lambda: app.invoke(input_data, runtime_config)
                )

    def stream(
        self,
        input_data: Any,
        thread_id: Optional[str] = None,
        stream_mode: str = "values",
        config: Optional[RunnableConfig] = None,
        **kwargs,
    ) -> Generator[Dict[str, Any], None, None]:
        """Stream with checkpointer support.

        This method streams graph execution results with checkpointing support,
        automatically handling state restoration and persistence.

        Args:
            input_data: The input data for the execution.
            thread_id: Optional thread ID for state tracking.
            stream_mode: The streaming mode to use (values, actions, etc.).
            config: Optional configuration override.
            **kwargs: Additional configuration parameters.

        Returns:
            A generator yielding execution chunks.
        """
        self._ensure_checkpointer_initialized()

        # Get the compiled app
        app = self.compile() if hasattr(self, "compile") else self.app

        # Prepare runtime config
        runtime_config = self._prepare_runnable_config(
            thread_id=thread_id, config=config, stream_mode=stream_mode, **kwargs
        )

        thread_id = runtime_config["configurable"]["thread_id"]
        checkpointer = self.get_checkpointer(async_mode=False)

        # Register thread if needed
        if checkpointer and thread_id:
            register_thread_if_needed(checkpointer, thread_id)

        # Get previous state if available
        previous_state = None
        try:
            if checkpointer and thread_id:
                previous_state = app.get_state(runtime_config)
        except Exception as e:
            logger.warning(f"Error retrieving previous state: {e}")

        # Prepare merged input
        if previous_state:
            try:
                input_schema = getattr(self, "input_schema", None)
                state_schema = getattr(self, "state_schema", None)

                input_data = prepare_merged_input(
                    input_data,
                    previous_state,
                    runtime_config,
                    input_schema,
                    state_schema,
                )
            except Exception as e:
                logger.warning(f"Error merging with previous state: {e}")

        # Stream execution
        yield from app.stream(input_data, runtime_config)

    async def astream(
        self,
        input_data: Any,
        thread_id: Optional[str] = None,
        stream_mode: str = "values",
        config: Optional[RunnableConfig] = None,
        **kwargs,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Async stream with checkpointer support.

        This method streams graph execution results asynchronously with
        checkpointing support, automatically handling state restoration
        and persistence.

        Args:
            input_data: The input data for the execution.
            thread_id: Optional thread ID for state tracking.
            stream_mode: The streaming mode to use (values, actions, etc.).
            config: Optional configuration override.
            **kwargs: Additional configuration parameters.

        Yields:
            Execution chunks as they become available.
        """
        self._ensure_checkpointer_initialized()
        await self._ensure_async_checkpointer_initialized()

        # Get the compiled app
        app = self.compile() if hasattr(self, "compile") else self.app

        # Check if we should use async mode
        checkpoint_mode = kwargs.get(
            "checkpoint_mode", getattr(self, "checkpoint_mode", "sync")
        )
        use_async = checkpoint_mode == "async" and self._async_checkpointer

        # Prepare runtime config
        runtime_config = self._prepare_runnable_config(
            thread_id=thread_id,
            config=config,
            stream_mode=stream_mode,
            checkpoint_mode=checkpoint_mode,
            **kwargs,
        )

        thread_id = runtime_config["configurable"]["thread_id"]

        if use_async:
            # Use async checkpointer
            await register_async_thread_if_needed(self._async_checkpointer, thread_id)

            # Get store if available
            store = (
                getattr(app, "store", None)
                if hasattr(app, "store")
                else getattr(self, "store", None)
            )

            # Recompile with async checkpointer
            async_app = app.graph.compile(
                checkpointer=self._async_checkpointer, store=store
            )

            # Get previous state
            previous_state = None
            try:
                previous_state = await async_app.aget_state(runtime_config)
            except Exception as e:
                logger.warning(f"Error retrieving previous state: {e}")

            # Prepare merged input
            if previous_state:
                try:
                    input_schema = getattr(self, "input_schema", None)
                    state_schema = getattr(self, "state_schema", None)

                    input_data = prepare_merged_input(
                        input_data,
                        previous_state,
                        runtime_config,
                        input_schema,
                        state_schema,
                    )
                except Exception as e:
                    logger.warning(f"Error merging with previous state: {e}")

            # Stream async app
            if hasattr(async_app, "astream"):
                async for chunk in async_app.astream(input_data, runtime_config):
                    yield chunk
            else:
                # Convert sync to async
                for chunk in async_app.stream(input_data, runtime_config):
                    yield chunk
        else:
            # Use sync checkpointer
            checkpointer = self.get_checkpointer(async_mode=False)

            if checkpointer and thread_id:
                register_thread_if_needed(checkpointer, thread_id)

            # Get previous state
            previous_state = None
            try:
                if checkpointer and thread_id:
                    previous_state = app.get_state(runtime_config)
            except Exception as e:
                logger.warning(f"Error retrieving previous state: {e}")

            # Prepare merged input
            if previous_state:
                try:
                    input_schema = getattr(self, "input_schema", None)
                    state_schema = getattr(self, "state_schema", None)

                    input_data = prepare_merged_input(
                        input_data,
                        previous_state,
                        runtime_config,
                        input_schema,
                        state_schema,
                    )
                except Exception as e:
                    logger.warning(f"Error merging with previous state: {e}")

            # Stream with astream if available, otherwise convert sync to async
            if hasattr(app, "astream"):
                async for chunk in app.astream(input_data, runtime_config):
                    yield chunk
            else:
                for chunk in app.stream(input_data, runtime_config):
                    yield chunk

    model_config = {"arbitrary_types_allowed": True}
