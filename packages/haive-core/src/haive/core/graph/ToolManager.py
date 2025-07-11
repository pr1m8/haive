# src/haive/core/tools/ToolManager.py

import asyncio
import functools
import inspect
import logging
import time
from collections.abc import Callable
from typing import Any, TypeVar, get_type_hints

from langchain_core.tools import BaseTool, StructuredTool
from langgraph.prebuilt.tool_node import InjectedState, InjectedStore
from pydantic import BaseModel, Field

# Import our registry system

# Set up logging
logger = logging.getLogger(__name__)

# Type variables
T = TypeVar("T", bound=Callable)
R = TypeVar("R")


class ToolConfig(BaseModel):
    """Configuration for a tool with execution parameters."""

    name: str = Field(..., description="Name of the tool")
    description: str | None = Field(default=None, description="Description of the tool")
    return_direct: bool = Field(
        default=False, description="Whether to return directly to user"
    )
    single_use: bool = Field(
        default=False, description="Whether the tool can only be used once"
    )
    timeout: float | None = Field(
        default=None, description="Timeout in seconds for tool execution"
    )
    max_retries: int = Field(default=0, description="Maximum number of retries")
    retry_delay: float = Field(
        default=0.5, description="Delay between retries in seconds"
    )
    tags: list[str] = Field(
        default_factory=list, description="Tags for categorizing this tool"
    )
    allowed_in_states: list[str] = Field(
        default_factory=list, description="States where this tool is allowed"
    )
    denied_in_states: list[str] = Field(
        default_factory=list, description="States where this tool is not allowed"
    )
    cost: float = Field(default=0.0, description="Cost associated with using this tool")
    dependencies: list[str] = Field(
        default_factory=list, description="Other tools this tool depends on"
    )
    is_async: bool = Field(default=False, description="Whether this tool is async")
    requires_state: bool = Field(
        default=False, description="Whether this tool requires state injection"
    )
    requires_store: bool = Field(
        default=False, description="Whether this tool requires store injection"
    )


class ToolResult(BaseModel):
    """Result of a tool execution."""

    tool_name: str = Field(..., description="Name of the tool")
    success: bool = Field(..., description="Whether the execution was successful")
    result: Any = Field(
        default=None, description="Result of the execution if successful"
    )
    error: str | None = Field(
        default=None, description="Error message if execution failed"
    )
    execution_time: float = Field(..., description="Execution time in seconds")
    retries: int = Field(default=0, description="Number of retries performed")


class ToolManager:
    """Manager for tools with registration, injection, and execution capabilities.

    The ToolManager provides:
    - Registration and discovery of tools
    - State and store injection for tools
    - Execution with timeouts and retries
    - Tool validation and verification
    - Tool filtering based on context
    """

    def __init__(self):
        """Initialize the tool manager."""
        # Initialize internal tracking
        self._executed_tools: set[str] = set()
        self._execution_history: list[ToolResult] = []
        self._cached_tool_configs: dict[str, ToolConfig] = {}

    # Tool registration methods
    def register_tool(
        self,
        tool_obj: BaseTool | StructuredTool | Callable,
        config: ToolConfig | None = None,
    ) -> BaseTool | StructuredTool:
        """Register a tool with the tool manager.

        Args:
            tool_obj: The tool to register
            config: Optional tool configuration

        Returns:
            The registered tool
        """
        # Get or create tool name
        tool_name = self._get_tool_name(tool_obj)

        # Create default config if not provided
        if config is None:
            config = ToolConfig(name=tool_name)

        # Register with our registry
        metadata = config.model_dump()
        register_tool(tool_name, tags=config.tags, metadata=metadata)(tool_obj)

        # Cache the config
        self._cached_tool_configs[tool_name] = config

        logger.info(f"Registered tool: {tool_name}")
        return tool_obj

    def create_and_register_tool(
        self,
        func: Callable,
        name: str | None = None,
        description: str | None = None,
        return_direct: bool = False,
        config: ToolConfig | None = None,
    ) -> BaseTool:
        """Create a tool from a function and register it.

        Args:
            func: Function to convert to a tool
            name: Optional name for the tool
            description: Optional description
            return_direct: Whether to return directly to user
            config: Optional additional tool configuration

        Returns:
            The created and registered tool
        """
        # Determine name and description
        tool_name = name or func.__name__
        tool_desc = description or (func.__doc__ or "").strip()

        # Create the tool
        tool_obj = ToolConfig(
            name=tool_name, description=tool_desc, return_direct=return_direct
        )

        # Create config if not provided
        if config is None:
            config = ToolConfig(
                name=tool_name, description=tool_desc, return_direct=return_direct
            )
        else:
            # Update provided config with name and description if not set
            if config.name == "" or config.name is None:
                config.name = tool_name
            if config.description is None:
                config.description = tool_desc

        # Register the tool
        return self.register_tool(tool_obj, config)

    # State and store injection methods
    def create_state_tool(
        self, func: Callable, state_field: str | None = None, **tool_kwargs
    ) -> BaseTool:
        """Create a tool that automatically injects state.

        Args:
            func: Function to convert to a tool
            state_field: Optional specific state field to inject
            **tool_kwargs: Additional tool kwargs

        Returns:
            Tool with state injection
        """
        # Get the function signature
        sig = inspect.signature(func)

        # Find a suitable parameter for state injection
        state_param = None
        for param_name, _param in sig.parameters.items():
            if param_name == "state" or param_name.endswith("_state"):
                state_param = param_name
                break

        if state_param is None:
            raise ValueError(
                f"Function {func.__name__} must have a parameter named 'state' or ending with '_state'"
            )

        # Create wrapper function with state injection
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        # Annotate the state parameter
        type_hints = get_type_hints(func)
        type_hints[state_param] = Any, InjectedState(state_field)
        wrapped_func.__annotations__ = type_hints

        # Create tool config
        tool_name = tool_kwargs.get("name", func.__name__)
        description = tool_kwargs.get("description", (func.__doc__ or "").strip())
        return_direct = tool_kwargs.get("return_direct", False)

        config = ToolConfig(
            name=tool_name,
            description=description,
            return_direct=return_direct,
            requires_state=True,
        )

        # Create and register the tool
        return self.create_and_register_tool(
            wrapped_func,
            name=tool_name,
            description=description,
            return_direct=return_direct,
            config=config,
        )

    def create_store_tool(self, func: Callable, **tool_kwargs) -> BaseTool:
        """Create a tool that automatically injects store.

        Args:
            func: Function to convert to a tool
            **tool_kwargs: Additional tool kwargs

        Returns:
            Tool with store injection
        """
        # Get the function signature
        sig = inspect.signature(func)

        # Find a suitable parameter for store injection
        store_param = None
        for param_name, _param in sig.parameters.items():
            if param_name == "store" or param_name.endswith("_store"):
                store_param = param_name
                break

        if store_param is None:
            raise ValueError(
                f"Function {func.__name__} must have a parameter named 'store' or ending with '_store'"
            )

        # Create wrapper function with store injection
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        # Annotate the store parameter
        type_hints = get_type_hints(func)
        type_hints[store_param] = Any, InjectedStore()
        wrapped_func.__annotations__ = type_hints

        # Create tool config
        tool_name = tool_kwargs.get("name", func.__name__)
        description = tool_kwargs.get("description", (func.__doc__ or "").strip())
        return_direct = tool_kwargs.get("return_direct", False)

        config = ToolConfig(
            name=tool_name,
            description=description,
            return_direct=return_direct,
            requires_store=True,
        )

        # Create and register the tool
        return self.create_and_register_tool(
            wrapped_func,
            name=tool_name,
            description=description,
            return_direct=return_direct,
            config=config,
        )

    def create_hybrid_tool(
        self, func: Callable, state_field: str | None = None, **tool_kwargs
    ) -> BaseTool:
        """Create a tool that automatically injects both state and store.

        Args:
            func: Function to convert to a tool
            state_field: Optional specific state field to inject
            **tool_kwargs: Additional tool kwargs

        Returns:
            Tool with state and store injection
        """
        # Get the function signature
        sig = inspect.signature(func)

        # Find suitable parameters
        state_param = None
        store_param = None

        for param_name, _param in sig.parameters.items():
            if param_name == "state" or param_name.endswith("_state"):
                state_param = param_name
            elif param_name == "store" or param_name.endswith("_store"):
                store_param = param_name

        if state_param is None:
            raise ValueError(
                f"Function {func.__name__} must have a parameter named 'state' or ending with '_state'"
            )

        if store_param is None:
            raise ValueError(
                f"Function {func.__name__} must have a parameter named 'store' or ending with '_store'"
            )

        # Create wrapper function with injections
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        # Annotate the parameters
        type_hints = get_type_hints(func)
        type_hints[state_param] = Any, InjectedState(state_field)
        type_hints[store_param] = Any, InjectedStore()
        wrapped_func.__annotations__ = type_hints

        # Create tool config
        tool_name = tool_kwargs.get("name", func.__name__)
        description = tool_kwargs.get("description", (func.__doc__ or "").strip())
        return_direct = tool_kwargs.get("return_direct", False)

        config = ToolConfig(
            name=tool_name,
            description=description,
            return_direct=return_direct,
            requires_state=True,
            requires_store=True,
        )

        # Create and register the tool
        return self.create_and_register_tool(
            wrapped_func,
            name=tool_name,
            description=description,
            return_direct=return_direct,
            config=config,
        )

    # Tool execution methods
    def execute_tool(
        self,
        tool_name: str,
        args: list[Any] | None = None,
        kwargs: dict[str, Any] | None = None,
    ) -> ToolResult:
        """Execute a tool by name with arguments.

        Args:
            tool_name: Name of the tool to execute
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            ToolResult with execution results
        """
        # Get defaults
        args = args or []
        kwargs = kwargs or {}

        # Get the tool
        tool_obj = tool_registry.get(tool_name)
        if tool_obj is None:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                error=f"Tool not found: {tool_name}",
                execution_time=0.0,
            )

        # Get config
        config = self._get_tool_config(tool_name)

        # Check if single use and already executed
        if config.single_use and tool_name in self._executed_tools:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                error=f"Tool {tool_name} can only be used once",
                execution_time=0.0,
            )

        # Execute with timeout and retries
        start_time = time.time()
        result = None
        error = None
        success = False
        retries = 0

        # Handle async tools
        if config.is_async:
            # Create a synchronous wrapper for async tools
            result, success, error, retries = asyncio.run(
                self._execute_async_tool(tool_obj, config, args, kwargs)
            )
        else:
            # Execute synchronous tool
            result, success, error, retries = self._execute_sync_tool(
                tool_obj, config, args, kwargs
            )

        # Calculate execution time
        execution_time = time.time() - start_time

        # Create result
        tool_result = ToolResult(
            tool_name=tool_name,
            success=success,
            result=result,
            error=error,
            execution_time=execution_time,
            retries=retries,
        )

        # Record execution
        if success:
            self._executed_tools.add(tool_name)
        self._execution_history.append(tool_result)

        return tool_result

    async def execute_tool_async(
        self,
        tool_name: str,
        args: list[Any] | None = None,
        kwargs: dict[str, Any] | None = None,
    ) -> ToolResult:
        """Execute a tool asynchronously.

        Args:
            tool_name: Name of the tool to execute
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            ToolResult with execution results
        """
        # Get defaults
        args = args or []
        kwargs = kwargs or {}

        # Get the tool
        tool_obj = tool_registry.get(tool_name)
        if tool_obj is None:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                error=f"Tool not found: {tool_name}",
                execution_time=0.0,
            )

        # Get config
        config = self._get_tool_config(tool_name)

        # Check if single use and already executed
        if config.single_use and tool_name in self._executed_tools:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                error=f"Tool {tool_name} can only be used once",
                execution_time=0.0,
            )

        # Execute with timeout and retries
        start_time = time.time()

        # Handle sync or async tools
        if config.is_async:
            result, success, error, retries = await self._execute_async_tool(
                tool_obj, config, args, kwargs
            )
        else:
            # For sync tools, run in a thread pool
            result, success, error, retries = await asyncio.to_thread(
                self._execute_sync_tool, tool_obj, config, args, kwargs
            )

        # Calculate execution time
        execution_time = time.time() - start_time

        # Create result
        tool_result = ToolResult(
            tool_name=tool_name,
            success=success,
            result=result,
            error=error,
            execution_time=execution_time,
            retries=retries,
        )

        # Record execution
        if success:
            self._executed_tools.add(tool_name)
        self._execution_history.append(tool_result)

        return tool_result

    # Tool filtering and selection methods
    def get_allowed_tools(
        self,
        current_state: str | None = None,
        tags: list[str] | None = None,
        require_all_tags: bool = False,
    ) -> dict[str, BaseTool]:
        """Get tools allowed in the current state or with specific tags.

        Args:
            current_state: Optional current state name
            tags: Optional tags to filter by
            require_all_tags: Whether to require all tags

        Returns:
            Dictionary of allowed tools
        """
        # Get all tools
        all_tools = tool_registry.get_all()

        # Filter tools
        allowed_tools = {}

        for tool_name, tool_obj in all_tools.items():
            # Get config
            config = self._get_tool_config(tool_name)

            # Check state restrictions
            if current_state is not None:
                # Excluded by denied states
                if current_state in config.denied_in_states:
                    continue

                # Not included in allowed states (if specified)
                if (
                    config.allowed_in_states
                    and current_state not in config.allowed_in_states
                ):
                    continue

            # Check single use restriction
            if config.single_use and tool_name in self._executed_tools:
                continue

            # Check tags if specified
            if tags:
                tool_tags = config.tags

                if require_all_tags:
                    # Tool must have all specified tags
                    if not all(tag in tool_tags for tag in tags):
                        continue
                # Tool must have at least one specified tag
                elif not any(tag in tool_tags for tag in tags):
                    continue

            # Tool passed all filters, add to allowed tools
            allowed_tools[tool_name] = tool_obj

        return allowed_tools

    def get_tool_descriptions(
        self, tool_names: list[str] | None = None
    ) -> list[dict[str, str]]:
        """Get descriptions for tools.

        Args:
            tool_names: Optional list of tool names to get descriptions for
                        If None, get descriptions for all tools

        Returns:
            List of tool description dictionaries
        """
        if tool_names is None:
            # Get all tool names
            tool_names = list(tool_registry.get_all().keys())

        descriptions = []

        for name in tool_names:
            if not tool_registry.has(name):
                continue

            # Get tool and config
            tool_obj = tool_registry.get(name)
            config = self._get_tool_config(name)

            # Build description
            description = {
                "name": name,
                "description": config.description
                or getattr(tool_obj, "description", ""),
                "tags": config.tags,
            }

            # Add to list
            descriptions.append(description)

        return descriptions

    # Helper methods
    def _get_tool_name(self, tool_obj: BaseTool | StructuredTool | Callable) -> str:
        """Get the name of a tool."""
        if hasattr(tool_obj, "name"):
            return tool_obj.name
        if hasattr(tool_obj, "__name__"):
            return tool_obj.__name__
        # Generate a unique name
        return f"tool_{id(tool_obj)}"

    def _get_tool_config(self, tool_name: str) -> ToolConfig:
        """Get the configuration for a tool."""
        # Check cache first
        if tool_name in self._cached_tool_configs:
            return self._cached_tool_configs[tool_name]

        # Try to get from registry metadata
        metadata = tool_registry.get_metadata(tool_name)

        if metadata:
            # Create from metadata
            config = ToolConfig(**metadata)
            self._cached_tool_configs[tool_name] = config
            return config

        # Create default config
        config = ToolConfig(name=tool_name)
        self._cached_tool_configs[tool_name] = config
        return config

    def _execute_sync_tool(
        self, tool_obj: Any, config: ToolConfig, args: list[Any], kwargs: dict[str, Any]
    ) -> tuple[Any, bool, str | None, int]:
        """Execute a synchronous tool with retries."""
        max_retries = config.max_retries
        retry_delay = config.retry_delay
        timeout = config.timeout

        result = None
        success = False
        error = None
        retries = 0

        # Try execution with retries
        for attempt in range(max_retries + 1):
            try:
                # Execute with timeout if specified
                if timeout:
                    # Use function executor with timeout
                    result = self._execute_with_timeout(tool_obj, timeout, args, kwargs)
                # Call directly
                elif hasattr(tool_obj, "run"):
                    # BaseTool or StructuredTool
                    if args and kwargs:
                        # Both args and kwargs - use first arg and merge with kwargs
                        result = tool_obj.run(args[0], **kwargs)
                    elif args:
                        # Just args
                        if len(args) == 1:
                            result = tool_obj.run(args[0])
                        else:
                            # Multiple args - this may fail depending on the tool
                            result = tool_obj.run(*args)
                    else:
                        # Just kwargs
                        result = tool_obj.run(**kwargs)
                else:
                    # Function
                    result = tool_obj(*args, **kwargs)

                # Execution succeeded
                success = True
                break

            except Exception as e:
                # Record error
                error = str(e)

                # Check if we should retry
                if attempt < max_retries:
                    retries += 1
                    logger.warning(
                        f"Tool execution failed, retrying ({retries}/{max_retries}): {error}"
                    )

                    # Wait before retrying
                    if retry_delay > 0:
                        time.sleep(retry_delay)
                else:
                    # Last attempt failed
                    logger.exception(
                        f"Tool execution failed after {retries} retries: {error}"
                    )

        return result, success, error, retries

    async def _execute_async_tool(
        self, tool_obj: Any, config: ToolConfig, args: list[Any], kwargs: dict[str, Any]
    ) -> tuple[Any, bool, str | None, int]:
        """Execute an asynchronous tool with retries."""
        max_retries = config.max_retries
        retry_delay = config.retry_delay
        timeout = config.timeout

        result = None
        success = False
        error = None
        retries = 0

        # Try execution with retries
        for attempt in range(max_retries + 1):
            try:
                # Execute with timeout if specified
                if timeout:
                    # Use asyncio timeout
                    result = await self._execute_async_with_timeout(
                        tool_obj, timeout, args, kwargs
                    )
                # Call directly
                elif hasattr(tool_obj, "arun"):
                    # Async BaseTool or StructuredTool
                    if args and kwargs:
                        # Both args and kwargs - use first arg and merge with kwargs
                        result = await tool_obj.arun(args[0], **kwargs)
                    elif args:
                        # Just args
                        if len(args) == 1:
                            result = await tool_obj.arun(args[0])
                        else:
                            # Multiple args - this may fail depending on the tool
                            result = await tool_obj.arun(*args)
                    else:
                        # Just kwargs
                        result = await tool_obj.arun(**kwargs)
                else:
                    # Async function
                    result = await tool_obj(*args, **kwargs)

                # Execution succeeded
                success = True
                break

            except Exception as e:
                # Record error
                error = str(e)

                # Check if we should retry
                if attempt < max_retries:
                    retries += 1
                    logger.warning(
                        f"Async tool execution failed, retrying ({retries}/{max_retries}): {error}"
                    )

                    # Wait before retrying
                    if retry_delay > 0:
                        await asyncio.sleep(retry_delay)
                else:
                    # Last attempt failed
                    logger.exception(
                        f"Async tool execution failed after {retries} retries: {error}"
                    )

        return result, success, error, retries

    def _execute_with_timeout(
        self, tool_obj: Any, timeout: float, args: list[Any], kwargs: dict[str, Any]
    ) -> Any:
        """Execute a function with a timeout."""
        # This requires Python 3.11+ for asyncio.timeout
        # Older Python versions can use concurrent.futures with timeout
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self._execute_func, tool_obj, args, kwargs)
            return future.result(timeout=timeout)

    async def _execute_async_with_timeout(
        self, tool_obj: Any, timeout: float, args: list[Any], kwargs: dict[str, Any]
    ) -> Any:
        """Execute an async function with a timeout."""
        try:
            # Use asyncio.timeout or wait_for
            return await asyncio.wait_for(
                self._execute_async_func(tool_obj, args, kwargs), timeout=timeout
            )
        except TimeoutError:
            raise TimeoutError(f"Tool execution timed out after {timeout} seconds")

    def _execute_func(
        self, tool_obj: Any, args: list[Any], kwargs: dict[str, Any]
    ) -> Any:
        """Execute a function or tool."""
        if hasattr(tool_obj, "run"):
            # BaseTool or StructuredTool
            if args and kwargs:
                # Both args and kwargs - use first arg and merge with kwargs
                return tool_obj.run(args[0], **kwargs)
            if args:
                # Just args
                if len(args) == 1:
                    return tool_obj.run(args[0])
                # Multiple args - this may fail depending on the tool
                return tool_obj.run(*args)
            # Just kwargs
            return tool_obj.run(**kwargs)
        # Function
        return tool_obj(*args, **kwargs)

    async def _execute_async_func(
        self, tool_obj: Any, args: list[Any], kwargs: dict[str, Any]
    ) -> Any:
        """Execute an async function or tool."""
        if hasattr(tool_obj, "arun"):
            # Async BaseTool or StructuredTool
            if args and kwargs:
                # Both args and kwargs - use first arg and merge with kwargs
                return await tool_obj.arun(args[0], **kwargs)
            if args:
                # Just args
                if len(args) == 1:
                    return await tool_obj.arun(args[0])
                # Multiple args - this may fail depending on the tool
                return await tool_obj.arun(*args)
            # Just kwargs
            return await tool_obj.arun(**kwargs)
        # Async function
        return await tool_obj(*args, **kwargs)

    # Instance management and state
    def reset(self) -> None:
        """Reset execution history and tool usage."""
        self._executed_tools.clear()
        self._execution_history.clear()

    def get_execution_history(self) -> list[ToolResult]:
        """Get the tool execution history."""
        return list(self._execution_history)

    @property
    def executed_tools(self) -> set[str]:
        """Get the set of executed tools."""
        return set(self._executed_tools)


# Create a global instance
tool_manager = ToolManager()


# Decorator for registering state-injected tools
def state_tool(state_field: str | None = None, **tool_kwargs):
    """Decorator to create a tool that injects state.

    Args:
        state_field: Optional specific state field to inject
        **tool_kwargs: Additional tool kwargs
    """

    def decorator(func: T) -> BaseTool:
        return tool_manager.create_state_tool(func, state_field, **tool_kwargs)

    return decorator


# Decorator for registering store-injected tools
def store_tool(**tool_kwargs):
    """Decorator to create a tool that injects store.

    Args:
        **tool_kwargs: Additional tool kwargs
    """

    def decorator(func: T) -> BaseTool:
        return tool_manager.create_store_tool(func, **tool_kwargs)

    return decorator


# Decorator for registering hybrid tools
def hybrid_tool(state_field: str | None = None, **tool_kwargs):
    """Decorator to create a tool that injects both state and store.

    Args:
        state_field: Optional specific state field to inject
        **tool_kwargs: Additional tool kwargs
    """

    def decorator(func: T) -> BaseTool:
        return tool_manager.create_hybrid_tool(func, state_field, **tool_kwargs)

    return decorator
