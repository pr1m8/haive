# haive/core/engine/agent/mixins/execution_mixin.py

import asyncio
import logging
import uuid
from collections.abc import AsyncGenerator, Generator
from typing import Any

from haive.core.config.runnable import RunnableConfigManager
from haive.core.persistence.handlers import (
    prepare_merged_input,
    register_thread_if_needed,
)
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel

# Import debug utilities
from haive.agents.base.debug_utils import debug_logger, get_agent_debugger

logger = logging.getLogger(__name__)


class ExecutionMixin:
    """Mixin for agent execution functionality including run, stream, and state management."""

    def _prepare_input(self, input_data: Any) -> Any:
        """Prepare input for the agent based on the input schema.

        Args:
            input_data: Input in various formats

        Returns:
            Processed input compatible with the graph
        """
        # Debug: Log what type of input we're receiving for ToolMessage issues
        if hasattr(input_data, "messages") and input_data.messages:
            for i, msg in enumerate(input_data.messages):
                if hasattr(msg, "tool_call_id"):
                    logger.debug(
                        f"Input message {i}: {type(msg).__name__} with tool_call_id={getattr(msg, 'tool_call_id', 'None')}"
                    )

        # Get input schema from agent
        input_schema = getattr(self, "input_schema", None)

        # Handle simple string input
        if isinstance(input_data, str):
            if input_schema:
                schema_fields = {}
                if hasattr(input_schema, "model_fields"):
                    schema_fields = input_schema.model_fields
                elif hasattr(input_schema, "__fields__"):
                    schema_fields = input_schema.__fields__

                prepared_input = {}

                # Detect message field and populate if found
                if "messages" in schema_fields:
                    prepared_input["messages"] = [HumanMessage(content=input_data)]

                # Populate common text fields with input string
                for field_name in ["input", "query", "question", "text", "content"]:
                    if field_name in schema_fields:
                        prepared_input[field_name] = input_data

                # If no matches, use first field or create minimal dict
                if not prepared_input:
                    if schema_fields:
                        first_field = next(iter(schema_fields))
                        prepared_input[first_field] = input_data
                    else:
                        prepared_input = {"input": input_data}

                # Create instance or return dict
                try:
                    result = input_schema(**prepared_input)
                    logger.debug(
                        f"Created input schema instance with {len(prepared_input)} fields"
                    )
                    return result
                except Exception as e:
                    logger.warning(f"Error creating input schema instance: {e}")
                    return prepared_input
            else:
                return {"messages": [HumanMessage(content=input_data)]}

        # Handle list of strings
        elif isinstance(input_data, list) and all(
            isinstance(item, str) for item in input_data
        ):
            if input_schema:
                schema_fields = {}
                if hasattr(input_schema, "model_fields"):
                    schema_fields = input_schema.model_fields
                elif hasattr(input_schema, "__fields__"):
                    schema_fields = input_schema.__fields__

                prepared_input = {}

                if "messages" in schema_fields:
                    prepared_input["messages"] = [
                        HumanMessage(content=text) for text in input_data
                    ]

                joined_text = "\n".join(input_data)
                for field_name in ["input", "query", "question", "text", "content"]:
                    if field_name in schema_fields:
                        prepared_input[field_name] = joined_text

                for field_name, field_info in schema_fields.items():
                    field_type = str(
                        getattr(
                            field_info, "annotation", getattr(field_info, "type_", "")
                        )
                    )
                    if (
                        "list" in field_type.lower()
                        and field_name not in prepared_input
                    ):
                        prepared_input[field_name] = input_data

                if not prepared_input:
                    if schema_fields:
                        first_field = next(iter(schema_fields))
                        prepared_input[first_field] = input_data
                    else:
                        prepared_input = {"input": input_data}

                try:
                    result = input_schema(**prepared_input)
                    logger.debug(
                        f"Created input schema instance with {len(prepared_input)} fields"
                    )
                    return result
                except Exception as e:
                    logger.warning(f"Error creating input schema instance: {e}")
                    return prepared_input
            else:
                return {"messages": [HumanMessage(content=text) for text in input_data]}

        # Handle dictionary input
        elif isinstance(input_data, dict):
            if input_schema:
                if "messages" in input_data and isinstance(
                    input_data["messages"], list
                ):
                    messages = input_data["messages"]
                    # Convert string messages to HumanMessage, but preserve BaseMessage objects
                    for i, msg in enumerate(messages):
                        if isinstance(msg, str):
                            messages[i] = HumanMessage(content=msg)

                try:
                    # CRITICAL FIX: If messages are already BaseMessage objects, don't let Pydantic
                    # try to reconstruct them from dicts, as this can lose important fields like tool_call_id
                    if input_data.get("messages"):
                        # Check if messages are already BaseMessage objects
                        all_base_messages = all(
                            isinstance(msg, BaseMessage)
                            for msg in input_data["messages"]
                        )
                        logger.debug(
                            f"Messages validation: count={len(input_data['messages'])}, all_base_messages={all_base_messages}"
                        )
                        for i, msg in enumerate(input_data["messages"]):
                            logger.debug(
                                f"  Message {i}: {type(msg)} (is BaseMessage: {isinstance(msg, BaseMessage)})"
                            )

                        if all_base_messages:
                            # Create a copy of input_data without messages for validation
                            validation_data = {
                                k: v for k, v in input_data.items() if k != "messages"
                            }
                            logger.debug(
                                f"Creating schema instance without messages, remaining fields: {list(validation_data.keys())}"
                            )
                            # Create the schema instance
                            result = input_schema(**validation_data)
                            # Directly set the messages field to preserve BaseMessage objects
                            result.messages = input_data["messages"]
                            logger.debug(
                                "Created input schema instance with preserved BaseMessage objects"
                            )
                            return result

                    # Fallback to normal validation
                    result = input_schema(**input_data)
                    logger.debug(
                        f"Created input schema instance from dict with {len(input_data)} fields"
                    )
                    return result
                except Exception as e:
                    logger.warning(
                        f"Error creating input schema instance from dict: {e}"
                    )
                    return input_data
            else:
                return input_data

        # Handle BaseModel input
        elif isinstance(input_data, BaseModel):
            if input_schema and not isinstance(input_data, input_schema):
                if hasattr(input_data, "model_dump"):
                    data_dict = input_data.model_dump(
                        exclude_none=False, exclude_unset=False
                    )
                else:
                    data_dict = input_data.dict(exclude_none=False, exclude_unset=False)

                try:
                    # CRITICAL FIX: Same as dict case - preserve BaseMessage objects
                    if data_dict.get("messages"):
                        # Check if the original input_data has BaseMessage objects
                        if hasattr(input_data, "messages") and input_data.messages:
                            original_messages = input_data.messages
                            # Get actual BaseMessage objects, not their dict representations
                            if hasattr(original_messages, "root"):
                                actual_messages = original_messages.root
                            elif isinstance(original_messages, (list, tuple)):
                                actual_messages = list(original_messages)
                            else:
                                try:
                                    actual_messages = list(original_messages)
                                except:
                                    actual_messages = []

                            # Check if they're BaseMessage objects
                            if actual_messages and all(
                                isinstance(msg, BaseMessage) for msg in actual_messages
                            ):
                                logger.debug(
                                    f"PRESERVING {len(actual_messages)} BaseMessage objects during input schema conversion"
                                )
                                # Log any ToolMessages
                                for i, msg in enumerate(actual_messages):
                                    if hasattr(msg, "tool_call_id"):
                                        logger.debug(
                                            f"  Preserving ToolMessage {i} with tool_call_id={getattr(msg, 'tool_call_id', 'None')}"
                                        )

                                # Create schema instance without messages first
                                validation_data = {
                                    k: v
                                    for k, v in data_dict.items()
                                    if k != "messages"
                                }
                                result = input_schema(**validation_data)
                                # Directly set the actual BaseMessage objects
                                result.messages = actual_messages
                                logger.debug(
                                    "Converted BaseModel to input schema with preserved BaseMessage objects"
                                )
                                return result

                    # Fallback to normal conversion
                    result = input_schema(**data_dict)
                    logger.debug("Converted BaseModel to input schema instance")
                    return result
                except Exception as e:
                    logger.warning(f"Error converting BaseModel to input schema: {e}")
                    return input_data
            else:
                return input_data

        # Other types - convert to string and handle
        else:
            logger.warning(
                f"Unsupported input type {type(input_data).__name__}, converting to string"
            )
            return self._prepare_input(str(input_data))

    def _prepare_runnable_config(
        self,
        thread_id: str | None = None,
        config: RunnableConfig | None = None,
        **kwargs,
    ) -> RunnableConfig:
        """Prepare a runnable config with thread ID and other parameters.

        Args:
            thread_id: Optional thread ID for persistence
            config: Optional runtime configuration
            **kwargs: Additional configuration parameters

        Returns:
            Prepared runnable configuration
        """
        # Get debugger for this agent
        agent_name = getattr(self, "name", "Agent")
        debugger = get_agent_debugger(agent_name)

        # Enable debugging if debug logger is active
        if debug_logger.level <= logging.DEBUG:
            debugger.enable()

        # Get base config from agent
        base_config = getattr(self, "runnable_config", None)
        if (
            not base_config
            and hasattr(self, "config")
            and hasattr(self.config, "runnable_config")
        ):
            base_config = self.config.runnable_config

        debugger.log_recursion_limit_flow(
            "Initial base_config",
            (
                base_config.get("configurable", {}).get("recursion_limit")
                if base_config
                else None
            ),
            "agent.runnable_config or agent.config.runnable_config",
        )

        # Create new config with thread_id if provided
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
        elif base_config:
            runtime_config = base_config
        else:
            runtime_config = RunnableConfigManager.create()

        # Ensure configurable section exists
        if "configurable" not in runtime_config:
            runtime_config["configurable"] = {}

        # Ensure thread_id exists
        if "thread_id" not in runtime_config["configurable"]:
            runtime_config["configurable"]["thread_id"] = str(uuid.uuid4())

        # Add debug flag if specified
        if "debug" in kwargs:
            runtime_config["configurable"]["debug"] = kwargs.pop("debug")

        # Add save_history flag if specified
        if "save_history" in kwargs:
            runtime_config["configurable"]["save_history"] = kwargs.pop("save_history")

        # Add checkpoint_mode flag if needed
        checkpoint_mode = getattr(self, "_checkpoint_mode", "sync")
        runtime_config["configurable"]["checkpoint_mode"] = kwargs.pop(
            "checkpoint_mode", checkpoint_mode
        )

        # Add other kwargs
        for key, value in kwargs.items():
            if key.startswith("configurable_"):
                param_name = key.replace("configurable_", "")
                runtime_config["configurable"][param_name] = value
            elif key == "configurable" and isinstance(value, dict):
                for k, v in value.items():
                    runtime_config["configurable"][k] = v
            elif key == "engine_configs" and isinstance(value, dict):
                if "engine_configs" not in runtime_config["configurable"]:
                    runtime_config["configurable"]["engine_configs"] = {}
                for engine_id, engine_params in value.items():
                    if (
                        engine_id
                        not in runtime_config["configurable"]["engine_configs"]
                    ):
                        runtime_config["configurable"]["engine_configs"][engine_id] = {}
                    runtime_config["configurable"]["engine_configs"][engine_id].update(
                        engine_params
                    )
            else:
                runtime_config[key] = value

        return runtime_config

    def _process_output(self, output_data: Any) -> Any:
        """Process and validate output data.

        Args:
            output_data: Raw output data from the graph

        Returns:
            Processed output data
        """
        output_schema = getattr(self, "output_schema", None)

        if output_schema and not isinstance(output_data, output_schema):
            try:
                if isinstance(output_data, dict):
                    data_dict = output_data
                elif hasattr(output_data, "model_dump"):
                    data_dict = output_data.model_dump()
                elif hasattr(output_data, "dict"):
                    data_dict = output_data.dict()
                else:
                    data_dict = {}
                    for key, value in output_data.__dict__.items():
                        if not key.startswith("_"):
                            data_dict[key] = value

                result = output_schema(**data_dict)
                logger.debug("Validated output with schema")
                return result
            except Exception as e:
                logger.warning(f"Error validating output with schema: {e}")
                return output_data

        return output_data

    def run(
        self,
        input_data: Any,
        thread_id: str | None = None,
        debug: bool = None,
        config: RunnableConfig | None = None,
        **kwargs,
    ) -> Any:
        """Synchronously run the agent with input data."""
        # Ensure we have compiled app
        if not hasattr(self, "_app") or self._app is None:
            self.compile()

        # Default debug to verbose if available
        if debug is None:
            debug = getattr(self, "verbose", False)

        # Prepare input data
        processed_input = self._prepare_input(input_data)

        # Prepare runtime configuration
        runtime_config = self._prepare_runnable_config(
            thread_id=thread_id, config=config, debug=debug, **kwargs
        )

        # Extract thread_id for persistence
        thread_id = runtime_config["configurable"].get("thread_id")

        # IMPORTANT: Extract recursion limit from configurable and set it at top level
        if "recursion_limit" in runtime_config["configurable"]:
            runtime_config["recursion_limit"] = runtime_config["configurable"][
                "recursion_limit"
            ]
        elif not runtime_config.get("recursion_limit"):
            # Set a default if not present
            runtime_config["recursion_limit"] = 100

        # Register thread if needed - use async checkpointer if available and in async mode
        # Only set up checkpointing if explicitly enabled
        checkpointer = getattr(self, "checkpointer", None)
        async_checkpointer = getattr(self, "_async_checkpointer", None)
        disable_checkpointing = getattr(self, "_disable_checkpointing", False)

        # Choose appropriate checkpointer based on mode
        active_checkpointer = None
        if not disable_checkpointing:
            active_checkpointer = checkpointer
            if self._checkpoint_mode == "async" and async_checkpointer:
                active_checkpointer = async_checkpointer

        if active_checkpointer and thread_id:
            try:
                register_thread_if_needed(active_checkpointer, thread_id)
            except Exception as e:
                logger.warning(f"Failed to register thread for checkpointing: {e}")
                # Disable checkpointing for this session if it fails
                active_checkpointer = None

        # Get previous state if available
        previous_state = None
        try:
            if active_checkpointer and thread_id:
                previous_state = self._app.get_state(runtime_config)
                if previous_state and debug:
                    logger.debug(f"Retrieved previous state for thread {thread_id}")
        except Exception as e:
            logger.warning(f"Error retrieving previous state: {e}")

        # Prepare merged input with previous state if available
        if previous_state:
            try:
                input_schema = getattr(self, "input_schema", None)
                state_schema = getattr(self, "state_schema", None)
                full_input = prepare_merged_input(
                    processed_input,
                    previous_state,
                    runtime_config,
                    input_schema,
                    state_schema,
                )
                logger.debug("Merged input with previous state")
                processed_input = full_input
            except Exception as e:
                logger.warning(f"Error merging with previous state: {e}")

        # Run the agent with proper connection cleanup
        pool_to_cleanup = None
        try:
            # Ensure PostgreSQL connection pool is properly opened if needed
            if active_checkpointer and hasattr(active_checkpointer, "conn"):
                from haive.core.persistence.handlers import ensure_pool_open

                pool_to_cleanup = ensure_pool_open(active_checkpointer)

            # Convert to dict if it's a Pydantic model
            if hasattr(processed_input, "model_dump"):
                processed_input = processed_input.model_dump()

            result = self._app.invoke(
                processed_input, config=runtime_config, debug=debug
            )
            logger.debug("Agent execution completed successfully")

            # Process the result
            output = self._process_output(result)

            # Save state history if configured
            if runtime_config["configurable"].get("save_history", True):
                self.save_state_history(runtime_config)

            return output

        except Exception as e:
            logger.error(f"Error during agent execution: {e}")
            raise
        finally:
            # Clean up connection pool if we opened it
            if pool_to_cleanup:
                try:
                    from haive.core.persistence.handlers import close_pool_if_needed

                    close_pool_if_needed(active_checkpointer, pool_to_cleanup)
                except Exception as cleanup_error:
                    logger.warning(f"Error during connection cleanup: {cleanup_error}")

    async def arun(
        self,
        input_data: Any,
        thread_id: str | None = None,
        config: RunnableConfig | None = None,
        debug: bool = None,
        **kwargs,
    ) -> Any:
        """Asynchronously run the agent with input data.

        Args:
            input_data: Input data for the agent
            thread_id: Optional thread ID for persistence
            config: Optional runtime configuration
            debug: Whether to enable debug mode
            **kwargs: Additional runtime configuration

        Returns:
            Output from the agent
        """
        # Check if we have async persistence setup
        async_checkpointer = getattr(self, "_async_checkpointer", None)

        # If we have async checkpointer, use full async implementation
        if async_checkpointer and self._checkpoint_mode == "async":
            # Ensure we have compiled app
            if not hasattr(self, "_app") or self._app is None:
                self.compile()

            # Default debug to verbose if available
            if debug is None:
                debug = getattr(self, "verbose", False)

            # Prepare input data
            processed_input = self._prepare_input(input_data)

            # Prepare runtime configuration
            runtime_config = self._prepare_runnable_config(
                thread_id=thread_id, config=config, debug=debug, **kwargs
            )

            # Extract thread_id for persistence
            thread_id = runtime_config["configurable"].get("thread_id")

            # Register thread if needed with async checkpointer
            if async_checkpointer and thread_id:
                from haive.core.persistence.handlers import (
                    register_async_thread_if_needed,
                )

                await register_async_thread_if_needed(async_checkpointer, thread_id)

            # Get previous state if available using async checkpointer
            previous_state = None
            try:
                if async_checkpointer and thread_id:
                    # Create async app with async checkpointer for state retrieval
                    async_app = self.graph.to_langgraph(
                        state_schema=self.state_schema
                    ).compile(checkpointer=async_checkpointer, store=self.store)
                    previous_state = await async_app.aget_state(runtime_config)
                    if previous_state and debug:
                        logger.debug(f"Retrieved previous state for thread {thread_id}")
            except Exception as e:
                logger.warning(f"Error retrieving async previous state: {e}")

            # Prepare merged input with previous state if available
            if previous_state:
                try:
                    input_schema = getattr(self, "input_schema", None)
                    state_schema = getattr(self, "state_schema", None)
                    full_input = prepare_merged_input(
                        processed_input,
                        previous_state,
                        runtime_config,
                        input_schema,
                        state_schema,
                    )
                    logger.debug("Merged input with previous state")
                    processed_input = full_input
                except Exception as e:
                    logger.warning(f"Error merging with previous state: {e}")

            # Run the agent asynchronously with proper connection cleanup
            pool_to_cleanup = None
            try:
                # Ensure async PostgreSQL connection pool is properly opened if needed
                if async_checkpointer and hasattr(async_checkpointer, "conn"):
                    from haive.core.persistence.handlers import ensure_async_pool_open

                    pool_to_cleanup = await ensure_async_pool_open(async_checkpointer)

                # Convert to dict if it's a Pydantic model
                if hasattr(processed_input, "model_dump"):
                    processed_input = processed_input.model_dump()

                # Create async app with async checkpointer
                async_app = self.graph.to_langgraph(
                    state_schema=self.state_schema
                ).compile(checkpointer=async_checkpointer, store=self.store)

                result = await async_app.ainvoke(processed_input, config=runtime_config)
                logger.debug("Async agent execution completed successfully")

                # Process the result
                output = self._process_output(result)

                # Save state history if configured
                if runtime_config["configurable"].get("save_history", True):
                    self.save_state_history(runtime_config)

                return output

            except Exception as e:
                logger.error(f"Error during async agent execution: {e}")
                raise
            finally:
                # Clean up async connection pool if we opened it
                if pool_to_cleanup:
                    try:
                        from haive.core.persistence.handlers import (
                            close_async_pool_if_needed,
                        )

                        await close_async_pool_if_needed(
                            async_checkpointer, pool_to_cleanup
                        )
                    except Exception as cleanup_error:
                        logger.warning(
                            f"Error during async connection cleanup: {cleanup_error}"
                        )
        else:
            # Fall back to sync execution in executor
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None,
                lambda: self.run(
                    input_data,
                    thread_id=thread_id,
                    config=config,
                    debug=debug,
                    **kwargs,
                ),
            )

    def stream(
        self,
        input_data: Any,
        thread_id: str | None = None,
        stream_mode: str = "values",
        config: RunnableConfig | None = None,
        debug: bool = None,
        **kwargs,
    ) -> Generator[dict[str, Any], None, None]:
        """Stream agent execution with input data.

        Args:
            input_data: Input data for the agent
            thread_id: Optional thread ID for persistence
            stream_mode: Stream mode (values, updates, debug, etc.)
            config: Optional runtime configuration
            debug: Whether to enable debug mode
            **kwargs: Additional runtime configuration

        Yields:
            State updates during execution
        """
        # Ensure we have compiled app
        if not hasattr(self, "_app") or self._app is None:
            self.compile()

        # Default debug to verbose if available
        if debug is None:
            debug = getattr(self, "verbose", False)

        # Prepare input data
        processed_input = self._prepare_input(input_data)

        # Add stream_mode to runtime config
        kwargs["stream_mode"] = stream_mode

        # Prepare runtime configuration
        runtime_config = self._prepare_runnable_config(
            thread_id=thread_id, config=config, debug=debug, **kwargs
        )

        # Extract thread_id for persistence
        thread_id = runtime_config["configurable"].get("thread_id")

        # IMPORTANT: Extract recursion limit from configurable and set it at top level
        if "recursion_limit" in runtime_config["configurable"]:
            runtime_config["recursion_limit"] = runtime_config["configurable"][
                "recursion_limit"
            ]
        elif not runtime_config.get("recursion_limit"):
            # Set a default if not present
            runtime_config["recursion_limit"] = 100

        # Register thread if needed - use async checkpointer if available and in async mode
        # Only set up checkpointing if explicitly enabled
        checkpointer = getattr(self, "checkpointer", None)
        async_checkpointer = getattr(self, "_async_checkpointer", None)
        disable_checkpointing = getattr(self, "_disable_checkpointing", False)

        # Choose appropriate checkpointer based on mode
        active_checkpointer = None
        if not disable_checkpointing:
            active_checkpointer = checkpointer
            if self._checkpoint_mode == "async" and async_checkpointer:
                active_checkpointer = async_checkpointer

        if active_checkpointer and thread_id:
            try:
                register_thread_if_needed(active_checkpointer, thread_id)
            except Exception as e:
                logger.warning(f"Failed to register thread for checkpointing: {e}")
                # Disable checkpointing for this session if it fails
                active_checkpointer = None

        # Get previous state if available
        previous_state = None
        try:
            if active_checkpointer and thread_id:
                previous_state = self._app.get_state(runtime_config)
                if previous_state and debug:
                    logger.debug(f"Retrieved previous state for thread {thread_id}")
        except Exception as e:
            logger.warning(f"Error retrieving previous state: {e}")

        # Prepare merged input with previous state if available
        if previous_state:
            try:
                input_schema = getattr(self, "input_schema", None)
                state_schema = getattr(self, "state_schema", None)
                full_input = prepare_merged_input(
                    processed_input,
                    previous_state,
                    runtime_config,
                    input_schema,
                    state_schema,
                )
                logger.debug("Merged input with previous state")
                processed_input = full_input
            except Exception as e:
                logger.warning(f"Error merging with previous state: {e}")

        # Stream execution
        try:
            # Convert to dict if it's a Pydantic model
            if hasattr(processed_input, "model_dump"):
                processed_input = processed_input.model_dump()

            stream_gen = self._app.stream(processed_input, runtime_config)

            final_result = None
            chunk_count = 0

            for chunk in stream_gen:
                chunk_count += 1
                final_result = chunk
                processed_chunk = self._process_stream_chunk(chunk, stream_mode)
                yield processed_chunk

            # Save state history if configured and we have a final result
            if (
                runtime_config["configurable"].get("save_history", True)
                and final_result is not None
            ):
                self.save_state_history(runtime_config)

        except Exception as e:
            logger.error(f"Error during streaming execution: {e}")
            raise

    def _process_stream_chunk(self, chunk: Any, stream_mode: str) -> dict[str, Any]:
        """Process a stream chunk based on stream mode.

        Args:
            chunk: The raw stream chunk
            stream_mode: Stream mode (values, updates, debug, etc.)

        Returns:
            Processed stream chunk
        """
        if stream_mode == "custom":
            return chunk
        if stream_mode == "values":
            # First check for standard LangChain format
            if isinstance(chunk, dict) and "values" in chunk:
                return chunk["values"]

            # Handle LangGraph AddableUpdatesDict format - extract actual state values
            if isinstance(chunk, dict):
                # LangGraph returns {node_name: state_data}
                for node_name, node_data in chunk.items():
                    if isinstance(node_data, dict) and node_data:
                        # Return the actual state data instead of node metadata
                        return node_data

            return chunk
        if stream_mode == "updates":
            if isinstance(chunk, dict) and "updates" in chunk:
                return chunk["updates"]
            if isinstance(chunk, dict) and "node" in chunk:
                return chunk
            return chunk
        if stream_mode == "messages":
            if isinstance(chunk, dict):
                if "values" in chunk and "messages" in chunk["values"]:
                    return {"messages": chunk["values"]["messages"]}
                if "updates" in chunk and "messages" in chunk["updates"]:
                    return {"messages": chunk["updates"]["messages"]}
                if "messages" in chunk:
                    return {"messages": chunk["messages"]}
            return chunk
        return chunk

    async def astream(
        self,
        input_data: Any,
        thread_id: str | None = None,
        stream_mode: str = "values",
        config: RunnableConfig | None = None,
        debug: bool = None,
        **kwargs,
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Asynchronously stream agent execution with input data.

        Args:
            input_data: Input data for the agent
            thread_id: Optional thread ID for persistence
            stream_mode: Stream mode (values, updates, debug, etc.)
            config: Optional runtime configuration
            debug: Whether to enable debug mode
            **kwargs: Additional runtime configuration

        Yields:
            Async iterator of state updates during execution
        """
        # For now, wrap sync generator
        # TODO: Implement full async support
        sync_gen = self.stream(
            input_data,
            thread_id=thread_id,
            stream_mode=stream_mode,
            config=config,
            debug=debug,
            **kwargs,
        )

        for chunk in sync_gen:
            yield chunk
