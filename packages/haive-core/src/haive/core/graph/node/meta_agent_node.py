"""Meta agent node for executing embedded agents from meta state.

This module provides MetaAgentNodeConfig, a specialized node configuration
for executing agents that are embedded within MetaStateSchema instances.
This enables sophisticated agent composition patterns and nested execution.

The meta agent node can:
- Extract agents from meta state
- Prepare input data for embedded agent execution
- Execute the embedded agent with proper configuration
- Handle agent output and update meta state
- Manage execution context and error handling

Example:
    ```python
    from haive.core.graph.node.meta_agent_node import MetaAgentNodeConfig
    from haive.core.schema.prebuilt.meta_state import MetaStateSchema
    from haive.agents.simple.agent import SimpleAgent

    # Create a meta agent node
    meta_node = MetaAgentNodeConfig(
        name="execute_embedded_agent",
        input_preparation="auto",  # Automatically prepare input
        output_handling="merge",   # Merge output back to meta state
        error_handling="capture"   # Capture errors in meta state
    )

    # Use in a graph with meta state
    # The node will automatically execute the embedded agent
    ```
"""

from __future__ import annotations

import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from langgraph.types import Command, Send
from pydantic import BaseModel, Field

from haive.core.graph.common.types import ConfigLike, StateLike
from haive.core.graph.node.base_config import NodeConfig
from haive.core.graph.node.types import NodeType
from haive.core.logging.rich_logger import LogLevel, get_logger

# Get module logger
logger = get_logger(__name__)
logger.set_level(LogLevel.DEBUG)


class MetaAgentNodeConfig(NodeConfig):
    """Specialized node for executing agents embedded in meta state.

    This node configuration is designed to work with MetaStateSchema instances
    that contain embedded agents. It handles the complete lifecycle of embedded
    agent execution including input preparation, execution, output handling,
    and error management.

    Key Features:
        - Automatic agent extraction from meta state
        - Flexible input preparation strategies
        - Multiple output handling modes
        - Comprehensive error handling and logging
        - Execution context management
        - State synchronization between meta and embedded agents

    Input Preparation Modes:
        - "auto": Automatically prepare input from meta state
        - "agent_input": Use only the agent_input field
        - "messages": Use only messages from meta state
        - "full_state": Use the entire meta state as input
        - "custom": Use custom input preparation logic

    Output Handling Modes:
        - "merge": Merge agent output back to meta state
        - "replace": Replace agent_output field with new output
        - "append": Append output to execution history only
        - "custom": Use custom output handling logic

    Error Handling Modes:
        - "capture": Capture errors in meta state error_info
        - "raise": Re-raise errors after capturing
        - "ignore": Log errors but continue execution
        - "custom": Use custom error handling logic
    """

    # Core node configuration
    node_type: NodeType = Field(default=NodeType.AGENT)

    # Meta agent execution configuration
    input_preparation: str = Field(
        default="auto", description="How to prepare input for the embedded agent"
    )

    output_handling: str = Field(
        default="merge", description="How to handle output from the embedded agent"
    )

    error_handling: str = Field(
        default="capture", description="How to handle errors during agent execution"
    )

    # Execution options
    include_messages: bool = Field(
        default=True, description="Whether to include messages in agent input"
    )

    include_meta_context: bool = Field(
        default=False, description="Whether to include meta context in agent input"
    )

    update_execution_history: bool = Field(
        default=True, description="Whether to update execution history in meta state"
    )

    sync_messages: bool = Field(
        default=True, description="Whether to sync messages back from agent output"
    )

    # Agent selection (if multiple agents in state)
    agent_field: str = Field(
        default="agent", description="Field name containing the agent to execute"
    )

    # Custom configuration
    custom_input_fields: list[str] = Field(
        default_factory=list, description="Additional fields to include in agent input"
    )

    exclude_fields: list[str] = Field(
        default_factory=list, description="Fields to exclude from agent input"
    )

    # Execution control
    max_execution_time: float | None = Field(
        default=None, description="Maximum execution time in seconds"
    )

    timeout_behavior: str = Field(
        default="error",
        description="Behavior when execution times out (error, continue, retry)",
    )

    def __call__(
        self, state: StateLike, config: ConfigLike | None = None
    ) -> Command | Send:
        """Execute the embedded agent from meta state.

        Args:
            state: Meta state containing the embedded agent
            config: Optional execution configuration

        Returns:
            Command or Send with updated state
        """
        logger.info("=" * 80)
        logger.info(f"META AGENT NODE EXECUTION: {self.name}")
        logger.info("=" * 80)

        with logger.track_time(f"Executing meta agent node {self.name}"):
            try:
                # Validate state is meta state
                if not self._is_meta_state(state):
                    raise ValueError(
                        f"State must be a MetaStateSchema instance, got {type(state)}"
                    )

                # Extract the embedded agent
                agent = self._extract_agent(state)
                if agent is None:
                    raise ValueError(
                        f"No agent found in state field '{self.agent_field}'"
                    )

                logger.info(f"✅ Found embedded agent: {type(agent).__name__}")

                # Prepare input for the embedded agent
                agent_input = self._prepare_agent_input(state, config)
                logger.debug(f"Prepared agent input with {len(agent_input)} fields")

                # Prepare execution configuration
                execution_config = self._prepare_execution_config(state, config)

                # Execute the embedded agent
                execution_result = self._execute_embedded_agent(
                    state, agent, agent_input, execution_config
                )

                # Handle the execution output
                updated_state = self._handle_agent_output(state, execution_result)

                # Create response
                response = self._create_response(updated_state)

                logger.info(f"✅ META AGENT NODE COMPLETED: {self.name}")
                return response

            except Exception as e:
                return self._handle_execution_error(state, e, config)

    def _is_meta_state(self, state: StateLike) -> bool:
        """Check if state is a MetaStateSchema instance."""
        # Check by class name to avoid import issues
        return (
            hasattr(state, "agent")
            and hasattr(state, "agent_input")
            and hasattr(state, "agent_output")
        )

    def _extract_agent(self, state: StateLike) -> Any | None:
        """Extract the embedded agent from meta state."""
        if hasattr(state, self.agent_field):
            return getattr(state, self.agent_field)
        return None

    def _prepare_agent_input(
        self, state: StateLike, config: ConfigLike | None = None
    ) -> dict[str, Any]:
        """Prepare input data for the embedded agent based on configuration."""
        logger.debug(f"Preparing agent input using strategy: {self.input_preparation}")

        if self.input_preparation == "auto":
            return self._prepare_auto_input(state)
        if self.input_preparation == "agent_input":
            return getattr(state, "agent_input", {})
        if self.input_preparation == "messages":
            return {"messages": getattr(state, "messages", [])}
        if self.input_preparation == "full_state":
            return state.model_dump() if hasattr(state, "model_dump") else dict(state)
        if self.input_preparation == "custom":
            return self._prepare_custom_input(state, config)
        else:
            raise ValueError(
                f"Unknown input preparation strategy: {self.input_preparation}"
            )

    def _prepare_auto_input(self, state: StateLike) -> dict[str, Any]:
        """Automatically prepare input from meta state."""
        input_data = {}

        # Include messages if requested and available
        if self.include_messages and hasattr(state, "messages") and state.messages:
            input_data["messages"] = state.messages

        # Include meta context if requested
        if self.include_meta_context and hasattr(state, "meta_context"):
            input_data["meta_context"] = state.meta_context

        # Include agent_input
        if hasattr(state, "agent_input"):
            input_data.update(state.agent_input)

        # Add custom fields
        for field_name in self.custom_input_fields:
            if hasattr(state, field_name):
                input_data[field_name] = getattr(state, field_name)

        # Remove excluded fields
        for field_name in self.exclude_fields:
            input_data.pop(field_name, None)

        logger.debug(f"Auto-prepared input with fields: {list(input_data.keys())}")
        return input_data

    def _prepare_custom_input(
        self, state: StateLike, config: ConfigLike | None = None
    ) -> dict[str, Any]:
        """Prepare custom input - override this method for custom logic."""
        # Default implementation uses auto strategy
        logger.warning("Custom input preparation not implemented, falling back to auto")
        return self._prepare_auto_input(state)

    def _prepare_execution_config(
        self, state: StateLike, config: ConfigLike | None = None
    ) -> dict[str, Any]:
        """Prepare execution configuration for the embedded agent."""
        execution_config = {}

        # Include base config
        if config:
            execution_config.update(config)

        # Include agent_config from meta state
        if hasattr(state, "agent_config"):
            execution_config.update(state.agent_config)

        # Add execution control
        if self.max_execution_time:
            execution_config["timeout"] = self.max_execution_time

        return execution_config

    def _execute_embedded_agent(
        self,
        state: StateLike,
        agent: Any,
        agent_input: dict[str, Any],
        execution_config: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute the embedded agent and return execution result."""
        logger.info(f"Executing embedded agent with input: {list(agent_input.keys())}")

        start_time = datetime.now()

        try:
            # Execute the agent using available methods
            if hasattr(agent, "run"):
                logger.debug("Using agent.run() method")
                result = agent.run(agent_input, **execution_config)
            elif hasattr(agent, "invoke"):
                logger.debug("Using agent.invoke() method")
                result = agent.invoke(agent_input, execution_config)
            elif callable(agent):
                logger.debug("Using agent as callable")
                result = agent(agent_input)
            else:
                raise RuntimeError(f"Agent {type(agent).__name__} is not executable")

            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()

            # Create execution result
            execution_result = {
                "status": "success",
                "result": result,
                "execution_time": execution_time,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "input": agent_input,
                "config": execution_config,
            }

            logger.info(f"✅ Agent execution completed in {execution_time:.2f}s")
            return execution_result

        except Exception as e:
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()

            logger.exception(
                f"❌ Agent execution failed after {execution_time:.2f}s: {e}"
            )

            # Create error result
            execution_result = {
                "status": "error",
                "error": str(e),
                "error_type": type(e).__name__,
                "traceback": traceback.format_exc(),
                "execution_time": execution_time,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "input": agent_input,
                "config": execution_config,
            }

            # Handle error based on error handling strategy
            if self.error_handling == "raise":
                raise
            if self.error_handling == "capture":
                # Return error result for capturing in state
                return execution_result
            if self.error_handling == "ignore":
                # Log and return empty result
                logger.warning("Ignoring agent execution error per configuration")
                return {"status": "ignored", "error": str(e)}
            if self.error_handling == "custom":
                return self._handle_custom_error(state, e, execution_result)
            # Default to capture
            return execution_result

    def _handle_custom_error(
        self, state: StateLike, error: Exception, execution_result: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle custom error - override this method for custom logic."""
        logger.warning("Custom error handling not implemented, falling back to capture")
        return execution_result

    def _handle_agent_output(
        self, state: StateLike, execution_result: dict[str, Any]
    ) -> StateLike:
        """Handle agent execution output and update meta state."""
        logger.debug(f"Handling agent output using strategy: {self.output_handling}")

        # Create a copy of the state to avoid modifying the original
        if hasattr(state, "model_copy"):
            updated_state = state.model_copy()
        else:
            # Fallback for dict-like states
            updated_state = dict(state)

        if self.output_handling == "merge":
            return self._merge_output(updated_state, execution_result)
        if self.output_handling == "replace":
            return self._replace_output(updated_state, execution_result)
        if self.output_handling == "append":
            return self._append_output(updated_state, execution_result)
        if self.output_handling == "custom":
            return self._handle_custom_output(updated_state, execution_result)
        raise ValueError(f"Unknown output handling strategy: {self.output_handling}")

    def _merge_output(
        self, state: StateLike, execution_result: dict[str, Any]
    ) -> StateLike:
        """Merge agent output back to meta state."""
        result = execution_result.get("result", {})

        # Update agent_output
        if hasattr(state, "agent_output"):
            if isinstance(result, dict):
                # Merge dictionaries
                current_output = getattr(state, "agent_output", {})
                merged_output = {**current_output, **result}
                state.agent_output = merged_output
            else:
                # Store non-dict results
                state.agent_output = {"result": result}

        # Update execution status
        if hasattr(state, "execution_status"):
            state.execution_status = execution_result["status"]

        # Update last execution result
        if hasattr(state, "last_execution_result"):
            state.last_execution_result = execution_result

        # Handle error info
        if execution_result["status"] == "error" and hasattr(state, "error_info"):
            state.error_info = {
                "error": execution_result.get("error"),
                "error_type": execution_result.get("error_type"),
                "timestamp": execution_result.get("end_time"),
            }
        elif hasattr(state, "error_info"):
            state.error_info = None

        # Sync messages if requested and available
        if (
            self.sync_messages
            and isinstance(result, dict)
            and "messages" in result
            and hasattr(state, "add_messages")
        ):
            state.add_messages(result["messages"])

        # Update execution history
        if self.update_execution_history and hasattr(state, "execution_history"):
            history = getattr(state, "execution_history", [])
            history.append(execution_result)
            state.execution_history = history

        logger.debug("✅ Successfully merged agent output to meta state")
        return state

    def _replace_output(
        self, state: StateLike, execution_result: dict[str, Any]
    ) -> StateLike:
        """Replace agent_output field with new output."""
        result = execution_result.get("result", {})

        if hasattr(state, "agent_output"):
            if isinstance(result, dict):
                state.agent_output = result
            else:
                state.agent_output = {"result": result}

        # Update other fields similar to merge
        self._update_execution_metadata(state, execution_result)

        logger.debug("✅ Successfully replaced agent output in meta state")
        return state

    def _append_output(
        self, state: StateLike, execution_result: dict[str, Any]
    ) -> StateLike:
        """Append output to execution history only."""
        if self.update_execution_history and hasattr(state, "execution_history"):
            history = getattr(state, "execution_history", [])
            history.append(execution_result)
            state.execution_history = history

        # Update execution status and metadata
        self._update_execution_metadata(state, execution_result)

        logger.debug("✅ Successfully appended agent output to execution history")
        return state

    def _handle_custom_output(
        self, state: StateLike, execution_result: dict[str, Any]
    ) -> StateLike:
        """Handle custom output - override this method for custom logic."""
        logger.warning("Custom output handling not implemented, falling back to merge")
        return self._merge_output(state, execution_result)

    def _update_execution_metadata(
        self, state: StateLike, execution_result: dict[str, Any]
    ) -> None:
        """Update execution metadata in the state."""
        if hasattr(state, "execution_status"):
            state.execution_status = execution_result["status"]

        if hasattr(state, "last_execution_result"):
            state.last_execution_result = execution_result

        # Handle error info
        if execution_result["status"] == "error" and hasattr(state, "error_info"):
            state.error_info = {
                "error": execution_result.get("error"),
                "error_type": execution_result.get("error_type"),
                "timestamp": execution_result.get("end_time"),
            }
        elif hasattr(state, "error_info"):
            state.error_info = None

    def _create_response(self, updated_state: StateLike) -> Command | Send:
        """Create the appropriate response with updated state."""
        # Convert state to update dictionary
        if hasattr(updated_state, "model_dump"):
            update_dict = updated_state.model_dump()
        else:
            update_dict = dict(updated_state)

        # Return appropriate response type
        if self.use_send and self.command_goto:
            logger.debug(f"Creating Send to {self.command_goto}")
            return Send(node=self.command_goto, arg=update_dict)
        logger.debug(f"Creating Command with goto={self.command_goto}")
        return Command(update=update_dict, goto=self.command_goto)

    def _handle_execution_error(
        self, state: StateLike, error: Exception, config: ConfigLike | None = None
    ) -> Command | Send:
        """Handle errors that occur during node execution."""
        logger.error(f"Meta agent node execution failed: {error}")

        # Create error state update
        error_update = {}

        error_update = (
            state.model_dump() if hasattr(state, "model_dump") else dict(state)
        )

        # Update error information
        error_update.update(
            {
                "execution_status": "error",
                "error_info": {
                    "error": str(error),
                    "error_type": type(error).__name__,
                    "timestamp": datetime.now().isoformat(),
                    "node": self.name,
                },
            }
        )

        # Return error response
        if self.use_send and self.command_goto:
            return Send(node=self.command_goto, arg=error_update)
        return Command(update=error_update, goto=self.command_goto)

    def __repr__(self) -> str:
        """String representation of the meta agent node."""
        return (
            f"MetaAgentNodeConfig("
            f"name='{self.name}', "
            f"input_preparation='{self.input_preparation}', "
            f"output_handling='{self.output_handling}', "
            f"error_handling='{self.error_handling}'"
            f")"
        )
