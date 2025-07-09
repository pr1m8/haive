# src/haive/core/node/NodeFactory.py

import asyncio
import inspect
import logging
import time
from collections.abc import Callable
from enum import Enum
from typing import (
    Any,
    TypeVar,
)

from langgraph.graph import END
from langgraph.types import Command, Send
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from haive.core.graph.ToolManager import tool_manager

# Import our components
from haive.core.registry.registy import register_node

# from haive.core.graph.GraphBuilder import NodeType, NodeConfig
# Set up logging
logger = logging.getLogger(__name__)

# Type variables
T = TypeVar("T", bound=Callable)
R = TypeVar("R")


class RetryPolicy(BaseModel):
    """Policies for retrying node execution on failure."""

    max_retries: int = Field(default=3, description="Maximum number of retry attempts")
    retry_delay: float = Field(
        default=0.5, description="Delay between retries in seconds"
    )
    retry_backoff: bool = Field(
        default=False, description="Whether to use exponential backoff"
    )
    retry_on_exceptions: list[str] = Field(
        default_factory=list, description="Exception types to retry on"
    )
    retry_status_codes: list[int] = Field(
        default_factory=list, description="HTTP status codes to retry on"
    )
    retry_condition: Callable[[Any, Exception], bool] | None = Field(
        default=None, description="Custom condition for retry"
    )


class ValidationMode(str, Enum):
    """Validation modes for node input/output."""

    NONE = "none"  # No validation
    WARN = "warn"  # Log warnings but continue
    STRICT = "strict"  # Raise exceptions on validation failures


class NodeType(str, Enum):
    """Types of nodes for different purposes."""

    PROCESSING = "processing"  # Standard processing node
    TOOL = "tool"  # Tool execution node
    ROUTER = "router"  # Routing decision node
    INTERRUPT = "interrupt"  # Interrupt handler node
    COMPOSITE = "composite"  # Node containing a subgraph


class RoutingConfig(BaseModel):
    """Configuration for node routing behavior."""

    default_destination: str = Field(
        ..., description="Default destination if no other routing applies"
    )
    condition_map: dict[Any, str] = Field(
        default_factory=dict, description="Map of condition values to destinations"
    )
    condition_function: Callable[[dict[str, Any]], Any] | None = Field(
        default=None, description="Function that determines routing"
    )
    allowed_destinations: list[str] = Field(
        default_factory=list,
        description="List of allowed destinations (for validation)",
    )
    is_dynamic: bool = Field(
        default=False, description="Whether routing is determined at runtime"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional routing metadata"
    )


class ToolInjectionConfig(BaseModel):
    """Configuration for tool injection into nodes."""

    tool_names: list[str] = Field(
        default_factory=list, description="Names of tools to inject"
    )
    tool_filter: Callable[[dict[str, Any]], list[str]] | None = Field(
        default=None, description="Dynamic filter for tools based on state"
    )
    inject_descriptions: bool = Field(
        default=True, description="Whether to inject tool descriptions"
    )
    pass_metadata: bool = Field(
        default=False, description="Whether to pass tool metadata to the node"
    )
    execution_mode: str = Field(
        default="async", description="Tool execution mode: sync or async"
    )
    state_key: str = Field(default="tools", description="State key for tool results")


class InputTransform(BaseModel):
    """Transform for node input mapping."""

    source_key: str = Field(..., description="Source key in state")
    target_key: str = Field(..., description="Target key for node function")
    transform_function: Callable[[Any], Any] | None = Field(
        default=None, description="Function to transform the value"
    )
    required: bool = Field(default=True, description="Whether this input is required")
    default_value: Any = Field(
        default=None, description="Default value if key is missing"
    )


class OutputTransform(BaseModel):
    """Transform for node output mapping."""

    source_key: str = Field(..., description="Source key from node output")
    target_key: str = Field(..., description="Target key in state")
    transform_function: Callable[[Any], Any] | None = Field(
        default=None, description="Function to transform the value"
    )
    condition: Callable[[dict[str, Any]], bool] | None = Field(
        default=None,
        description="Condition to determine whether to apply this transform",
    )


class NodeHooks(BaseModel):
    """Lifecycle hooks for node execution."""

    before_execution: Callable[[dict[str, Any]], dict[str, Any]] | None = Field(
        default=None, description="Hook called before node execution"
    )
    after_execution: Callable[[dict[str, Any], Any], dict[str, Any]] | None = Field(
        default=None, description="Hook called after successful execution"
    )
    on_error: Callable[[dict[str, Any], Exception], dict[str, Any]] | None = Field(
        default=None, description="Hook called on execution error"
    )
    on_timeout: Callable[[dict[str, Any]], dict[str, Any]] | None = Field(
        default=None, description="Hook called on execution timeout"
    )


class NodeConfig(BaseModel):
    """Comprehensive configuration for a node."""

    name: str = Field(..., description="Name of the node")
    description: str | None = Field(default=None, description="Description of the node")
    function: Callable = Field(..., description="Node function")
    node_type: NodeType = Field(default=NodeType.PROCESSING, description="Type of node")

    # Input/output configuration
    input_mapping: list[InputTransform] = Field(
        default_factory=list, description="Input mapping configuration"
    )
    output_mapping: list[OutputTransform] = Field(
        default_factory=list, description="Output mapping configuration"
    )

    # State validation
    validation_mode: ValidationMode = Field(
        default=ValidationMode.WARN, description="Validation mode"
    )
    validate_schema: type[BaseModel] | None = Field(
        default=None, description="Schema for validation"
    )

    # Routing configuration
    routing: RoutingConfig | None = Field(
        default=None, description="Routing configuration"
    )

    # Tool integration
    tool_injection: ToolInjectionConfig | None = Field(
        default=None, description="Tool injection configuration"
    )

    # Execution controls
    timeout: float | None = Field(
        default=None, description="Timeout for node execution in seconds"
    )
    retry_policy: RetryPolicy | None = Field(
        default=None, description="Retry policy for node execution"
    )
    is_async: bool = Field(
        default=False, description="Whether the node function is async"
    )
    requires_state: bool = Field(
        default=False, description="Whether the node requires state injection"
    )
    requires_store: bool = Field(
        default=False, description="Whether the node requires store injection"
    )

    # Lifecycle hooks
    hooks: NodeHooks | None = Field(default=None, description="Node lifecycle hooks")

    # Additional metadata
    tags: list[str] = Field(default_factory=list, description="Tags for the node")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


model_config = ConfigDict(
    arbitrary_types_allowed=True,
)


# Factory for creating different node types
class EnhancedNodeFactory:
    """Enhanced factory for creating and managing nodes with advanced capabilities.

    This factory supports:
    - Different node types (processing, tool, router, etc.)
    - Input/output transformation
    - State validation
    - Tool injection
    - Advanced routing
    - Retry policies
    - State and store injection
    - Lifecycle hooks
    """

    def __init__(self):
        """Initialize the node factory."""
        # Initialize internal tracking
        self._node_configs: dict[str, NodeConfig] = {}
        self._custom_node_types: dict[str, Callable] = {}

    def create_node(self, config: NodeConfig) -> Callable:
        """Create a node function based on the provided configuration.

        Args:
            config: Configuration for the node

        Returns:
            Node function compatible with LangGraph
        """
        # Store the config
        self._node_configs[config.name] = config

        # Register the node
        register_node(
            config.name,
            tags=config.tags,
            metadata={
                "description": config.description or "",
                "node_type": config.node_type,
                **config.metadata,
            },
        )

        # Create node based on type
        if config.node_type == NodeType.PROCESSING:
            node_func = self._create_processing_node(config)
        elif config.node_type == NodeType.TOOL:
            node_func = self._create_tool_node(config)
        elif config.node_type == NodeType.ROUTER:
            node_func = self._create_router_node(config)
        elif config.node_type == NodeType.INTERRUPT:
            node_func = self._create_interrupt_node(config)
        elif config.node_type == NodeType.COMPOSITE:
            node_func = self._create_composite_node(config)
        elif config.node_type in self._custom_node_types:
            # Custom node type
            node_func = self._custom_node_types[config.node_type](config)
        else:
            logger.warning(
                f"Unknown node type: {config.node_type}. Using processing node."
            )
            node_func = self._create_processing_node(config)

        logger.info(f"Created node: {config.name} ({config.node_type})")
        return node_func

    def _create_processing_node(self, config: NodeConfig) -> Callable:
        """Create a standard processing node."""
        # Determine if we need async
        if config.is_async:

            async def node_function(state: dict[str, Any]) -> Command:
                """Async node function wrapper."""
                return await self._execute_node_async(state, config)

            return node_function

        def node_function(state: dict[str, Any]) -> Command:
            """Sync node function wrapper."""
            return self._execute_node_sync(state, config)

        return node_function

    def _create_tool_node(self, config: NodeConfig) -> Callable:
        """Create a tool execution node."""
        # Ensure tool injection config is present
        if not config.tool_injection:
            config.tool_injection = ToolInjectionConfig()

        # Determine if we need async
        if config.is_async:

            async def node_function(state: dict[str, Any]) -> Command:
                """Async tool node function wrapper."""
                return await self._execute_tool_node_async(state, config)

            return node_function

        def node_function(state: dict[str, Any]) -> Command:
            """Sync tool node function wrapper."""
            return self._execute_tool_node_sync(state, config)

        return node_function

    def _create_router_node(self, config: NodeConfig) -> Callable:
        """Create a routing decision node."""
        # Ensure routing config is present
        if not config.routing:
            raise ValueError(
                f"Router node {config.name} requires routing configuration"
            )

        def node_function(state: dict[str, Any]) -> str | Send | Command:
            """Router node function wrapper."""
            try:
                # Apply before execution hook if present
                if config.hooks and config.hooks.before_execution:
                    try:
                        state = config.hooks.before_execution(state) or state
                    except Exception as e:
                        logger.error(
                            f"Error in before_execution hook for node {config.name}: {e}"
                        )

                # Process inputs
                inputs = self._process_inputs(state, config)

                # Determine routing based on the configuration
                if config.routing.condition_function:
                    # Use condition function to get routing value
                    route_key = config.routing.condition_function(state)

                    # Look up in condition map or use default
                    if route_key in config.routing.condition_map:
                        destination = config.routing.condition_map[route_key]
                    else:
                        destination = config.routing.default_destination
                else:
                    # No condition function, just call the node function
                    result = config.function(inputs if inputs else state)

                    # If result is already a routing command, return it directly
                    if isinstance(result, (str, Send, Command)):
                        return result

                    # Otherwise, look up in condition map or use default
                    if result in config.routing.condition_map:
                        destination = config.routing.condition_map[result]
                    else:
                        destination = config.routing.default_destination

                # Validate destination if allowed destinations specified
                if (
                    config.routing.allowed_destinations
                    and destination not in config.routing.allowed_destinations
                ):
                    logger.warning(
                        f"Router {config.name} routed to invalid destination: {destination}. "
                        f"Using default: {config.routing.default_destination}"
                    )
                    destination = config.routing.default_destination

                # Apply after execution hook if present
                if config.hooks and config.hooks.after_execution:
                    try:
                        hook_result = config.hooks.after_execution(state, destination)
                        if hook_result and isinstance(hook_result, dict):
                            # Return Command with updated state and destination
                            return Command(update=hook_result, goto=destination)
                    except Exception as e:
                        logger.error(
                            f"Error in after_execution hook for node {config.name}: {e}"
                        )

                # Return the destination
                return destination

            except Exception as e:
                logger.error(f"Error in router node {config.name}: {e}")

                # Apply error hook if present
                if config.hooks and config.hooks.on_error:
                    try:
                        error_result = config.hooks.on_error(state, e)
                        if error_result:
                            return Command(
                                update=error_result,
                                goto=config.routing.default_destination,
                            )
                    except Exception as hook_error:
                        logger.error(
                            f"Error in on_error hook for node {config.name}: {hook_error}"
                        )

                # Return default destination
                return config.routing.default_destination

        return node_function

    def _create_interrupt_node(self, config: NodeConfig) -> Callable:
        """Create an interrupt handler node."""
        # Ensure routing config is present for exit path
        if not config.routing:
            config.routing = RoutingConfig(default_destination=END)

        # Use processing node with added interrupt handling
        return self._create_processing_node(config)

    def _create_composite_node(self, config: NodeConfig) -> Callable:
        """Create a composite node containing a subgraph."""
        # This is a placeholder for future implementation
        # A composite node would execute a subgraph and return the result

        logger.warning(f"Composite nodes not fully implemented yet: {config.name}")

        # For now, just use a processing node
        return self._create_processing_node(config)

    def _execute_node_sync(self, state: dict[str, Any], config: NodeConfig) -> Command:
        """Execute a synchronous node with all the configured behaviors."""
        start_time = time.time()
        retries = 0

        try:
            # Validate state if schema provided
            if config.validate_schema and config.validation_mode != ValidationMode.NONE:
                self._validate_state(
                    state, config.validate_schema, config.validation_mode
                )

            # Apply before execution hook if present
            if config.hooks and config.hooks.before_execution:
                try:
                    modified_state = config.hooks.before_execution(state)
                    if modified_state:
                        state = modified_state
                except Exception as e:
                    logger.error(
                        f"Error in before_execution hook for node {config.name}: {e}"
                    )

            # Process inputs
            inputs = self._process_inputs(state, config)

            # Execute with retry policy if configured
            result = None
            error = None
            max_retries = config.retry_policy.max_retries if config.retry_policy else 0

            for attempt in range(max_retries + 1):
                try:
                    # Execute with timeout if configured
                    if config.timeout:
                        result = self._execute_with_timeout(
                            config.function,
                            config.timeout,
                            inputs if inputs is not None else state,
                        )
                    else:
                        result = config.function(
                            inputs if inputs is not None else state
                        )

                    # Execution succeeded
                    break

                except Exception as e:
                    error = e
                    retries = attempt + 1

                    # Check if we should retry
                    if attempt < max_retries and config.retry_policy:
                        logger.warning(
                            f"Node {config.name} execution failed, "
                            f"retrying ({retries}/{max_retries}): {error}"
                        )

                        # Check if we should retry this exception
                        should_retry = True
                        if config.retry_policy.retry_on_exceptions:
                            exception_name = type(e).__name__
                            if (
                                exception_name
                                not in config.retry_policy.retry_on_exceptions
                            ):
                                should_retry = False

                        # Custom retry condition
                        if should_retry and config.retry_policy.retry_condition:
                            should_retry = config.retry_policy.retry_condition(state, e)

                        if not should_retry:
                            logger.info(
                                f"Not retrying node {config.name}: condition not met"
                            )
                            break

                        # Wait before retrying
                        retry_delay = config.retry_policy.retry_delay
                        if config.retry_policy.retry_backoff:
                            # Exponential backoff
                            retry_delay = retry_delay * (2**attempt)

                        if retry_delay > 0:
                            time.sleep(retry_delay)
                    else:
                        # Last attempt failed or no retry policy
                        logger.error(
                            f"Node {config.name} execution failed "
                            f"after {retries} retries: {error}"
                        )

            # Process result if execution succeeded
            if error is None:
                # Apply output transformations
                updated_state = self._process_output(state, result, config)

                # Apply after execution hook if present
                if config.hooks and config.hooks.after_execution:
                    try:
                        hook_result = config.hooks.after_execution(
                            updated_state, result
                        )
                        if hook_result:
                            updated_state = hook_result
                    except Exception as e:
                        logger.error(
                            f"Error in after_execution hook for node {config.name}: {e}"
                        )

                # Determine next node
                goto = self._get_next_node(updated_state, result, config)

                # Return command with updated state
                return Command(update=updated_state, goto=goto)
            # Execution failed
            # Apply error hook if present
            error_state = dict(state)
            error_state["error"] = str(error)

            if config.hooks and config.hooks.on_error:
                try:
                    hook_result = config.hooks.on_error(error_state, error)
                    if hook_result:
                        error_state = hook_result
                except Exception as hook_error:
                    logger.error(
                        f"Error in on_error hook for node {config.name}: {hook_error}"
                    )

            # Determine error routing
            goto = END
            if config.routing:
                goto = config.routing.default_destination

            # Return command with error state
            return Command(update=error_state, goto=goto)

        except Exception as e:
            # Unexpected error in node execution wrapper
            logger.error(f"Unexpected error in node {config.name} execution: {e}")

            # Return error state
            error_state = dict(state)
            error_state["error"] = f"Node execution failed: {e!s}"

            # Determine error routing
            goto = END
            if config.routing:
                goto = config.routing.default_destination

            return Command(update=error_state, goto=goto)

        finally:
            # Log execution time
            execution_time = time.time() - start_time
            logger.debug(
                f"Node {config.name} executed in {execution_time:.4f}s "
                f"with {retries} retries"
            )

    async def _execute_node_async(
        self, state: dict[str, Any], config: NodeConfig
    ) -> Command:
        """Execute an asynchronous node with all the configured behaviors."""
        start_time = time.time()
        retries = 0

        try:
            # Validate state if schema provided
            if config.validate_schema and config.validation_mode != ValidationMode.NONE:
                self._validate_state(
                    state, config.validate_schema, config.validation_mode
                )

            # Apply before execution hook if present
            if config.hooks and config.hooks.before_execution:
                try:
                    modified_state = config.hooks.before_execution(state)
                    if modified_state:
                        state = modified_state
                except Exception as e:
                    logger.error(
                        f"Error in before_execution hook for node {config.name}: {e}"
                    )

            # Process inputs
            inputs = self._process_inputs(state, config)

            # Execute with retry policy if configured
            result = None
            error = None
            max_retries = config.retry_policy.max_retries if config.retry_policy else 0

            for attempt in range(max_retries + 1):
                try:
                    # Execute with timeout if configured
                    if config.timeout:
                        result = await self._execute_async_with_timeout(
                            config.function,
                            config.timeout,
                            inputs if inputs is not None else state,
                        )
                    else:
                        result = await config.function(
                            inputs if inputs is not None else state
                        )

                    # Execution succeeded
                    break

                except Exception as e:
                    error = e
                    retries = attempt + 1

                    # Check if we should retry
                    if attempt < max_retries and config.retry_policy:
                        logger.warning(
                            f"Node {config.name} execution failed, "
                            f"retrying ({retries}/{max_retries}): {error}"
                        )

                        # Check if we should retry this exception
                        should_retry = True
                        if config.retry_policy.retry_on_exceptions:
                            exception_name = type(e).__name__
                            if (
                                exception_name
                                not in config.retry_policy.retry_on_exceptions
                            ):
                                should_retry = False

                        # Custom retry condition
                        if should_retry and config.retry_policy.retry_condition:
                            should_retry = config.retry_policy.retry_condition(state, e)

                        if not should_retry:
                            logger.info(
                                f"Not retrying node {config.name}: condition not met"
                            )
                            break

                        # Wait before retrying
                        retry_delay = config.retry_policy.retry_delay
                        if config.retry_policy.retry_backoff:
                            # Exponential backoff
                            retry_delay = retry_delay * (2**attempt)

                        if retry_delay > 0:
                            await asyncio.sleep(retry_delay)
                    else:
                        # Last attempt failed or no retry policy
                        logger.error(
                            f"Node {config.name} execution failed "
                            f"after {retries} retries: {error}"
                        )

            # Process result if execution succeeded
            if error is None:
                # Apply output transformations
                updated_state = self._process_output(state, result, config)

                # Apply after execution hook if present
                if config.hooks and config.hooks.after_execution:
                    try:
                        hook_result = config.hooks.after_execution(
                            updated_state, result
                        )
                        if hook_result:
                            updated_state = hook_result
                    except Exception as e:
                        logger.error(
                            f"Error in after_execution hook for node {config.name}: {e}"
                        )

                # Determine next node
                goto = self._get_next_node(updated_state, result, config)

                # Return command with updated state
                return Command(update=updated_state, goto=goto)
            # Execution failed
            # Apply error hook if present
            error_state = dict(state)
            error_state["error"] = str(error)

            if config.hooks and config.hooks.on_error:
                try:
                    hook_result = config.hooks.on_error(error_state, error)
                    if hook_result:
                        error_state = hook_result
                except Exception as hook_error:
                    logger.error(
                        f"Error in on_error hook for node {config.name}: {hook_error}"
                    )

            # Determine error routing
            goto = END
            if config.routing:
                goto = config.routing.default_destination

            # Return command with error state
            return Command(update=error_state, goto=goto)

        except Exception as e:
            # Unexpected error in node execution wrapper
            logger.error(f"Unexpected error in node {config.name} execution: {e}")

            # Return error state
            error_state = dict(state)
            error_state["error"] = f"Node execution failed: {e!s}"

            # Determine error routing
            goto = END
            if config.routing:
                goto = config.routing.default_destination

            return Command(update=error_state, goto=goto)

        finally:
            # Log execution time
            execution_time = time.time() - start_time
            logger.debug(
                f"Node {config.name} executed in {execution_time:.4f}s "
                f"with {retries} retries"
            )

    def _execute_tool_node_sync(
        self, state: dict[str, Any], config: NodeConfig
    ) -> Command:
        """Execute a synchronous tool node."""
        try:
            # Validate state if schema provided
            if config.validate_schema and config.validation_mode != ValidationMode.NONE:
                self._validate_state(
                    state, config.validate_schema, config.validation_mode
                )

            # Apply before execution hook if present
            if config.hooks and config.hooks.before_execution:
                try:
                    modified_state = config.hooks.before_execution(state)
                    if modified_state:
                        state = modified_state
                except Exception as e:
                    logger.error(
                        f"Error in before_execution hook for node {config.name}: {e}"
                    )

            # Get tools to inject
            tool_names = self._get_tool_names(state, config)

            # Get tool descriptions if configured
            tool_descriptions = None
            if (
                config.tool_injection
                and config.tool_injection.inject_descriptions
                and tool_names
            ):
                tool_descriptions = tool_manager.get_tool_descriptions(tool_names)

            # Process inputs
            inputs = self._process_inputs(state, config)
            if inputs is None:
                inputs = dict(state)

            # Add tool information to inputs
            if tool_names:
                tool_key = (
                    config.tool_injection.state_key
                    if config.tool_injection
                    else "tools"
                )
                inputs[tool_key] = {
                    "names": tool_names,
                    "descriptions": tool_descriptions,
                }

                # Add tool metadata if configured
                if config.tool_injection and config.tool_injection.pass_metadata:
                    tool_metadata = {}
                    for name in tool_names:
                        metadata = tool_manager.get_tool_metadata(name)
                        if metadata:
                            tool_metadata[name] = metadata
                    inputs[f"{tool_key}_metadata"] = tool_metadata

            # Execute the function
            if config.timeout:
                result = self._execute_with_timeout(
                    config.function, config.timeout, inputs
                )
            else:
                result = config.function(inputs)

            # Process result
            updated_state = self._process_output(state, result, config)

            # Apply after execution hook if present
            if config.hooks and config.hooks.after_execution:
                try:
                    hook_result = config.hooks.after_execution(updated_state, result)
                    if hook_result:
                        updated_state = hook_result
                except Exception as e:
                    logger.error(
                        f"Error in after_execution hook for node {config.name}: {e}"
                    )

            # Determine next node
            goto = self._get_next_node(updated_state, result, config)

            # Return command with updated state
            return Command(update=updated_state, goto=goto)

        except Exception as e:
            # Error in tool node execution
            logger.error(f"Error in tool node {config.name}: {e}")

            # Apply error hook if present
            error_state = dict(state)
            error_state["error"] = str(e)

            if config.hooks and config.hooks.on_error:
                try:
                    hook_result = config.hooks.on_error(error_state, e)
                    if hook_result:
                        error_state = hook_result
                except Exception as hook_error:
                    logger.error(
                        f"Error in on_error hook for node {config.name}: {hook_error}"
                    )

            # Determine error routing
            goto = END
            if config.routing:
                goto = config.routing.default_destination

            return Command(update=error_state, goto=goto)

    async def _execute_tool_node_async(
        self, state: dict[str, Any], config: NodeConfig
    ) -> Command:
        """Execute an asynchronous tool node."""
        try:
            # Validate state if schema provided
            if config.validate_schema and config.validation_mode != ValidationMode.NONE:
                self._validate_state(
                    state, config.validate_schema, config.validation_mode
                )

            # Apply before execution hook if present
            if config.hooks and config.hooks.before_execution:
                try:
                    modified_state = config.hooks.before_execution(state)
                    if modified_state:
                        state = modified_state
                except Exception as e:
                    logger.error(
                        f"Error in before_execution hook for node {config.name}: {e}"
                    )

            # Get tools to inject
            tool_names = self._get_tool_names(state, config)

            # Get tool descriptions if configured
            tool_descriptions = None
            if (
                config.tool_injection
                and config.tool_injection.inject_descriptions
                and tool_names
            ):
                tool_descriptions = tool_manager.get_tool_descriptions(tool_names)

            # Process inputs
            inputs = self._process_inputs(state, config)
            if inputs is None:  # Add tool information to inputs
                inputs = dict(state)
            if tool_names:
                tool_key = (
                    config.tool_injection.state_key
                    if config.tool_injection
                    else "tools"
                )
                inputs[tool_key] = {
                    "names": tool_names,
                    "descriptions": tool_descriptions,
                }

                # Add tool metadata if configured
                if config.tool_injection and config.tool_injection.pass_metadata:
                    tool_metadata = {}
                    for name in tool_names:
                        metadata = tool_manager.get_metadata(name)
                        if metadata:
                            tool_metadata[name] = metadata
                    inputs[f"{tool_key}_metadata"] = tool_metadata

            # Execute the function
            if config.timeout:
                result = await self._execute_async_with_timeout(
                    config.function, config.timeout, inputs
                )
            else:
                result = await config.function(inputs)

            # Process result
            updated_state = self._process_output(state, result, config)

            # Apply after execution hook if present
            if config.hooks and config.hooks.after_execution:
                try:
                    hook_result = config.hooks.after_execution(updated_state, result)
                    if hook_result:
                        updated_state = hook_result
                except Exception as e:
                    logger.error(
                        f"Error in after_execution hook for node {config.name}: {e}"
                    )

            # Determine next node
            goto = self._get_next_node(updated_state, result, config)

            # Return command with updated state
            return Command(update=updated_state, goto=goto)

        except Exception as e:
            # Error in tool node execution
            logger.error(f"Error in async tool node {config.name}: {e}")

            # Apply error hook if present
            error_state = dict(state)
            error_state["error"] = str(e)

            if config.hooks and config.hooks.on_error:
                try:
                    hook_result = config.hooks.on_error(error_state, e)
                    if hook_result:
                        error_state = hook_result
                except Exception as hook_error:
                    logger.error(
                        f"Error in on_error hook for node {config.name}: {hook_error}"
                    )

            # Determine error routing
            goto = END
            if config.routing:
                goto = config.routing.default_destination

            return Command(update=error_state, goto=goto)

    # Helper methods
    def _process_inputs(
        self, state: dict[str, Any], config: NodeConfig
    ) -> dict[str, Any] | None:
        """Process inputs according to input mapping configuration.

        Args:
            state: Current state
            config: Node configuration

        Returns:
            Processed inputs or None if no mapping
        """
        # If no input mapping, return None to use full state
        if not config.input_mapping:
            return None

        # Create input dict
        inputs = {}

        # Apply mappings
        for mapping in config.input_mapping:
            # Check if source exists in state
            if mapping.source_key in state:
                value = state[mapping.source_key]

                # Apply transform if configured
                if mapping.transform_function:
                    try:
                        value = mapping.transform_function(value)
                    except Exception as e:
                        logger.error(
                            f"Error in input transform for {mapping.source_key}: {e}"
                        )

                # Add to inputs
                inputs[mapping.target_key] = value
            elif mapping.required:
                # Missing required input
                if mapping.default_value is not None:
                    # Use default value
                    inputs[mapping.target_key] = mapping.default_value
                else:
                    logger.warning(
                        f"Missing required input {mapping.source_key} "
                        f"for node {config.name} with no default value"
                    )
            elif mapping.default_value is not None:
                # Use default value for optional input
                inputs[mapping.target_key] = mapping.default_value

        return inputs

    def _process_output(
        self, state: dict[str, Any], result: Any, config: NodeConfig
    ) -> dict[str, Any]:
        """Process outputs according to output mapping configuration.

        Args:
            state: Current state
            result: Function result
            config: Node configuration

        Returns:
            Updated state
        """
        # Create updated state copy
        updated_state = dict(state)

        # Check for Command result which might already have updates
        if isinstance(result, Command):
            if result.update:
                updated_state.update(result.update)
            return updated_state

        # If no output mapping, try to auto-detect appropriate updates
        if not config.output_mapping:
            # Handle different output types
            if isinstance(result, dict):
                # Update state with keys from result dict
                updated_state.update(result)
            elif isinstance(result, str):
                # Add string result to output field
                updated_state["output"] = result

                # If we have messages field, add as AI message
                if "messages" in updated_state:
                    from langchain_core.messages import AIMessage

                    updated_state["messages"] = list(updated_state["messages"])
                    updated_state["messages"].append(AIMessage(content=result))
            elif hasattr(result, "content"):
                # Message-like object with content attribute
                updated_state["output"] = result.content

                # Add to messages
                if "messages" in updated_state:
                    updated_state["messages"] = list(updated_state["messages"])
                    updated_state["messages"].append(result)
            else:
                # Default to adding in "result" field
                updated_state["result"] = result

            return updated_state

        # Apply output mappings
        for mapping in config.output_mapping:
            # Check condition if present
            if mapping.condition and not mapping.condition(result):
                continue

            # Get source value
            if mapping.source_key == "*":
                # Special case: use entire result
                value = result
            elif isinstance(result, dict) and mapping.source_key in result:
                # Extract from result dict
                value = result[mapping.source_key]
            elif hasattr(result, mapping.source_key):
                # Extract from result object attribute
                value = getattr(result, mapping.source_key)
            else:
                # Skip this mapping
                continue

            # Apply transform if configured
            if mapping.transform_function:
                try:
                    value = mapping.transform_function(value)
                except Exception as e:
                    logger.error(
                        f"Error in output transform for {mapping.source_key}: {e}"
                    )
                    continue

            # Update state
            updated_state[mapping.target_key] = value

        return updated_state

    def _get_next_node(
        self, state: dict[str, Any], result: Any, config: NodeConfig
    ) -> str:
        """Determine the next node based on routing configuration.

        Args:
            state: Current state
            result: Function result
            config: Node configuration

        Returns:
            Next node name or END
        """
        # Check for Command result with explicit routing
        if isinstance(result, Command) and result.goto:
            return result.goto

        # Check routing configuration
        if config.routing:
            # Check if result is a routing value in condition_map
            if result in config.routing.condition_map:
                return config.routing.condition_map[result]

            # Use default destination
            return config.routing.default_destination

        # Default to END
        return END

    def _get_tool_names(self, state: dict[str, Any], config: NodeConfig) -> list[str]:
        """Get the names of tools to inject based on configuration.

        Args:
            state: Current state
            config: Node configuration

        Returns:
            List of tool names
        """
        if not config.tool_injection:
            return []

        # Start with configured tools
        tool_names = list(config.tool_injection.tool_names)

        # Apply dynamic filter if configured
        if config.tool_injection.tool_filter:
            try:
                filtered_tools = config.tool_injection.tool_filter(state)
                if filtered_tools:
                    tool_names = filtered_tools
            except Exception as e:
                logger.error(f"Error in tool filter for node {config.name}: {e}")

        return tool_names

    def _validate_state(
        self,
        state: dict[str, Any],
        schema: type[BaseModel],
        validation_mode: ValidationMode,
    ) -> None:
        """Validate state against a schema.

        Args:
            state: State to validate
            schema: Validation schema
            validation_mode: Validation mode

        Raises:
            ValidationError: If validation fails and mode is STRICT
        """
        try:
            schema.model_validate(state)
        except ValidationError as e:
            if validation_mode == ValidationMode.STRICT:
                raise e
            if validation_mode == ValidationMode.WARN:
                logger.warning(f"State validation warning: {e}")

    def _execute_with_timeout(self, func: Callable, timeout: float, arg: Any) -> Any:
        """Execute a function with a timeout."""
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(func, arg)
            return future.result(timeout=timeout)

    async def _execute_async_with_timeout(
        self, func: Callable, timeout: float, arg: Any
    ) -> Any:
        """Execute an async function with a timeout."""
        return await asyncio.wait_for(func(arg), timeout=timeout)

    # Custom node type registration
    def register_node_type(
        self, node_type: str, factory: Callable[[NodeConfig], Callable]
    ) -> None:
        """Register a custom node type.

        Args:
            node_type: Name of the node type
            factory: Factory function to create nodes of this type
        """
        self._custom_node_types[node_type] = factory
        logger.info(f"Registered custom node type: {node_type}")

    # Node configurator methods
    def create_processing_config(
        self, name: str, function: Callable, description: str | None = None, **kwargs
    ) -> NodeConfig:
        """Create a processing node configuration.

        Args:
            name: Node name
            function: Node function
            description: Optional description
            **kwargs: Additional configuration

        Returns:
            NodeConfig instance
        """
        return NodeConfig(
            name=name,
            function=function,
            description=description,
            node_type=NodeType.PROCESSING,
            **kwargs,
        )

    def create_tool_config(
        self,
        name: str,
        function: Callable,
        tool_names: list[str],
        description: str | None = None,
        **kwargs,
    ) -> NodeConfig:
        """Create a tool node configuration.

        Args:
            name: Node name
            function: Node function
            tool_names: Names of tools to inject
            description: Optional description
            **kwargs: Additional configuration

        Returns:
            NodeConfig instance
        """
        tool_injection = ToolInjectionConfig(tool_names=tool_names)
        return NodeConfig(
            name=name,
            function=function,
            description=description,
            node_type=NodeType.TOOL,
            tool_injection=tool_injection,
            **kwargs,
        )

    def create_router_config(
        self,
        name: str,
        function: Callable,
        default_destination: str,
        condition_map: dict[Any, str] | None = None,
        description: str | None = None,
        **kwargs,
    ) -> NodeConfig:
        """Create a router node configuration.

        Args:
            name: Node name
            function: Router function
            default_destination: Default destination
            condition_map: Optional mapping from result values to destinations
            description: Optional description
            **kwargs: Additional configuration

        Returns:
            NodeConfig instance
        """
        routing = RoutingConfig(
            default_destination=default_destination, condition_map=condition_map or {}
        )
        return NodeConfig(
            name=name,
            function=function,
            description=description,
            node_type=NodeType.ROUTER,
            routing=routing,
            **kwargs,
        )

    def create_conditional_router_config(
        self,
        name: str,
        condition_function: Callable[[dict[str, Any]], Any],
        default_destination: str,
        condition_map: dict[Any, str],
        description: str | None = None,
        **kwargs,
    ) -> NodeConfig:
        """Create a conditional router node configuration.

        Args:
            name: Node name
            condition_function: Function to determine routing
            default_destination: Default destination
            condition_map: Mapping from condition values to destinations
            description: Optional description
            **kwargs: Additional configuration

        Returns:
            NodeConfig instance
        """
        routing = RoutingConfig(
            default_destination=default_destination,
            condition_map=condition_map,
            condition_function=condition_function,
        )

        # For conditional routers, the function is simple - it just returns the condition result
        def router_func(state: dict[str, Any]) -> Any:
            return condition_function(state)

        return NodeConfig(
            name=name,
            function=router_func,
            description=description
            or f"Conditional router based on {condition_function.__name__}",
            node_type=NodeType.ROUTER,
            routing=routing,
            **kwargs,
        )

    def create_interrupt_config(
        self,
        name: str,
        function: Callable,
        return_to: str,
        description: str | None = None,
        **kwargs,
    ) -> NodeConfig:
        """Create an interrupt handler node configuration.

        Args:
            name: Node name
            function: Handler function
            return_to: Node to return to after handling
            description: Optional description
            **kwargs: Additional configuration

        Returns:
            NodeConfig instance
        """
        routing = RoutingConfig(default_destination=return_to)
        return NodeConfig(
            name=name,
            function=function,
            description=description,
            node_type=NodeType.INTERRUPT,
            routing=routing,
            **kwargs,
        )


# Create a global instance
node_factory = EnhancedNodeFactory()


# Decorator for registering nodes
def node(name: str | None = None, **config_kwargs):
    """Decorator to create and register a node.

    Args:
        name: Optional name for the node (defaults to function name)
        **config_kwargs: Additional configuration for the node

    Returns:
        Decorator function
    """

    def decorator(func: Callable) -> Callable:
        # Determine name
        node_name = name or func.__name__

        # Create description from docstring
        description = inspect.getdoc(func) or ""

        # Create node config
        config = NodeConfig(
            name=node_name, function=func, description=description, **config_kwargs
        )

        # Create and register the node
        node_func = node_factory.create_node(config)

        return node_func

    return decorator


# Specialized decorators for specific node types
def processing_node(name: str | None = None, **config_kwargs):
    """Decorator to create a processing node.

    Args:
        name: Optional name for the node
        **config_kwargs: Additional configuration

    Returns:
        Decorator function
    """
    config_kwargs["node_type"] = NodeType.PROCESSING
    return node(name, **config_kwargs)


def tool_node(tool_names: list[str], name: str | None = None, **config_kwargs):
    """Decorator to create a tool node.

    Args:
        tool_names: Names of tools to inject
        name: Optional name for the node
        **config_kwargs: Additional configuration

    Returns:
        Decorator function
    """
    config_kwargs["node_type"] = NodeType.TOOL
    config_kwargs["tool_injection"] = ToolInjectionConfig(tool_names=tool_names)
    return node(name, **config_kwargs)


def router_node(
    default_destination: str,
    condition_map: dict[Any, str] | None = None,
    name: str | None = None,
    **config_kwargs,
):
    """Decorator to create a router node.

    Args:
        default_destination: Default destination
        condition_map: Optional mapping from values to destinations
        name: Optional name for the node
        **config_kwargs: Additional configuration

    Returns:
        Decorator function
    """
    config_kwargs["node_type"] = NodeType.ROUTER
    config_kwargs["routing"] = RoutingConfig(
        default_destination=default_destination, condition_map=condition_map or {}
    )
    return node(name, **config_kwargs)


def interrupt_node(return_to: str, name: str | None = None, **config_kwargs):
    """Decorator to create an interrupt handler node.

    Args:
        return_to: Node to return to after handling
        name: Optional name for the node
        **config_kwargs: Additional configuration

    Returns:
        Decorator function
    """
    config_kwargs["node_type"] = NodeType.INTERRUPT
    config_kwargs["routing"] = RoutingConfig(default_destination=return_to)
    return node(name, **config_kwargs)
