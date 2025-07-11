# src/haive/core/engine/tool/base.py

import logging
from typing import Any, Dict, List, Optional, Union

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import StructuredTool, Tool
from langchain_core.tools.base import BaseTool, BaseToolkit
from langgraph.types import RetryPolicy
from pydantic import BaseModel, Field, field_validator

from haive.core.engine.base import EngineType, InvokableEngine

logger = logging.getLogger(__name__)


class ToolEngine(InvokableEngine[dict[str, Any], dict[str, Any]]):
    """Engine for tools and toolkits.

    ToolEngine manages the execution of tools based on input state,
    supporting individual tools, collections of tools, and toolkits.

    Attributes:
        tools: Optional list of BaseTool, Tool, StructuredTool, or BaseModel tools
        toolkit: Optional BaseToolkit or list of BaseToolkit objects
        retry_policy: Optional retry policy for tools
        parallel: Whether to execute tools in parallel when possible
        auto_route: Whether to automatically route to the appropriate tool
        messages_key: Key for messages in the state
        tool_choice: Strategy for selecting tools ("auto", "required", or "none")
        return_source: Whether to include source information with tool results
    """

    engine_type: EngineType = EngineType.TOOL

    # Tool sources with proper type enforcement
    tools: list[BaseTool | Tool | StructuredTool | BaseModel] | None = None
    toolkit: BaseToolkit | list[BaseToolkit] | None = None

    # Configuration
    retry_policy: RetryPolicy | None = None
    parallel: bool = Field(
        default=False, description="Execute tools in parallel when possible"
    )
    auto_route: bool = Field(
        default=True, description="Auto-route to appropriate tool based on calls"
    )
    messages_key: str = Field(
        default="messages", description="Key for messages in the state"
    )
    tool_choice: str = Field(
        default="auto",
        description="Tool choice strategy: 'auto', 'required', or 'none'",
    )
    return_source: bool = Field(
        default=True, description="Include source information with tool results"
    )

    # Advanced options
    timeout: float | None = Field(
        default=None, description="Timeout for tool execution in seconds"
    )
    max_iterations: int | None = Field(
        default=None, description="Maximum number of tool iterations"
    )

    class Config:
        arbitrary_types_allowed = True

    def create_runnable(self, runnable_config=None) -> Any:
        """Create a runnable tool node.

        Args:
            runnable_config: Optional runtime configuration

        Returns:
            A runnable tool node
        """
        from langgraph.prebuilt import ToolNode

        # Extract params from config
        params = self.apply_runnable_config(runnable_config)

        # Get tools from different sources
        all_tools = self._get_all_tools()

        # Create ToolNode with these tools
        kwargs = {
            "tools": all_tools,
            "retry_policy": params.get("retry_policy", self.retry_policy),
        }

        # Add optional parameters if specified
        if self.timeout is not None:
            kwargs["timeout"] = params.get("timeout", self.timeout)
        if self.max_iterations is not None:
            kwargs["max_iterations"] = params.get("max_iterations", self.max_iterations)

        # Create ToolNode
        tool_node = ToolNode(**kwargs)

        return tool_node

    def _get_all_tools(self) -> list[BaseTool | Tool | StructuredTool]:
        """Get all tools from the various sources.

        Returns:
            List of all tools
        """
        all_tools = []

        # Add directly specified tools
        if self.tools:
            for tool in self.tools:
                # Process BaseModel tools (convert to StructuredTool if needed)
                if isinstance(tool, BaseModel) and not isinstance(
                    tool, BaseTool | Tool | StructuredTool
                ):
                    try:
                        # Try to convert BaseModel to StructuredTool
                        structured_tool = self._convert_model_to_tool(tool)
                        if structured_tool:
                            all_tools.append(structured_tool)
                        else:
                            logger.warning(
                                f"Could not convert model to tool: {type(tool).__name__}"
                            )
                    except Exception as e:
                        logger.warning(f"Error converting model to tool: {e}")
                else:
                    all_tools.append(tool)

        # Add tools from toolkits
        if self.toolkit:
            if isinstance(self.toolkit, list):
                # Handle list of toolkits
                for tk in self.toolkit:
                    if hasattr(tk, "get_tools"):
                        all_tools.extend(tk.get_tools())
                    elif isinstance(tk, BaseToolkit):
                        all_tools.extend(tk.tools)
            elif hasattr(self.toolkit, "get_tools"):
                all_tools.extend(self.toolkit.get_tools())
            elif isinstance(self.toolkit, BaseToolkit):
                all_tools.extend(self.toolkit.tools)

        return all_tools

    def _convert_model_to_tool(self, model: BaseModel) -> StructuredTool | None:
        """Convert a Pydantic model to a StructuredTool.

        Args:
            model: BaseModel to convert

        Returns:
            StructuredTool if conversion was successful, None otherwise
        """
        # Check if model has a __call__ method
        if not callable(model) or not callable(model.__call__):
            return None

        # Get call method
        call_method = model.__call__

        # Get model name
        name = getattr(model, "name", model.__class__.__name__.lower())

        # Get description from docstring
        description = call_method.__doc__ or f"Tool for {name}"

        # Create tool from model
        from langchain_core.tools import tool

        @tool(name=name, description=description)
        def model_tool(*args, **kwargs):
            return call_method(*args, **kwargs)

        return model_tool

    def apply_runnable_config(
        self, runnable_config: RunnableConfig | None = None
    ) -> dict[str, Any]:
        """Extract parameters from runnable_config relevant to this tool engine.

        Args:
            runnable_config: Runtime configuration

        Returns:
            Dictionary of relevant parameters
        """
        # Start with common parameters
        params = super().apply_runnable_config(runnable_config)

        if runnable_config and "configurable" in runnable_config:
            configurable = runnable_config["configurable"]

            # Extract tool-specific parameters
            if "retry_policy" in configurable:
                params["retry_policy"] = configurable["retry_policy"]
            if "parallel" in configurable:
                params["parallel"] = configurable["parallel"]
            if "timeout" in configurable:
                params["timeout"] = configurable["timeout"]
            if "max_iterations" in configurable:
                params["max_iterations"] = configurable["max_iterations"]
            if "tool_choice" in configurable:
                params["tool_choice"] = configurable["tool_choice"]

        return params

    def invoke(
        self,
        input_data: dict[str, Any],
        runnable_config: RunnableConfig | None = None,
    ) -> dict[str, Any]:
        """Invoke the tool engine with input data.

        Args:
            input_data: Input state dictionary
            runnable_config: Optional runtime configuration

        Returns:
            Updated state with tool execution results
        """
        # Create the tool node
        tool_node = self.create_runnable(runnable_config)

        # Process messages key if specified
        if isinstance(input_data, dict) and self.messages_key != "messages":
            # If state has custom messages key but tool expects "messages"
            messages = input_data.get(self.messages_key, [])
            if messages:
                # Create a copy to avoid modifying the original
                input_data = input_data.copy()
                input_data["messages"] = messages

        # Invoke the tool node
        result = tool_node.invoke(input_data, config=runnable_config)

        # Post-process the result if needed
        if isinstance(result, dict) and not self.return_source:
            # Remove source information if not wanted
            if "messages" in result:
                for msg in result["messages"]:
                    if hasattr(msg, "tool_calls"):
                        for tool_call in msg.tool_calls:
                            if hasattr(tool_call, "source") and tool_call.source:
                                tool_call.source = None

        return result

    @field_validator("engine_type")
    def validate_engine_type(self, v):
        """Validate engine type is TOOL."""
        if v != EngineType.TOOL:
            raise ValueError("engine_type must be TOOL")
        return v

    @field_validator("tools")
    def validate_tools(self, v):
        """Validate tools are of the correct type."""
        if v is None:
            return v

        valid_tools = []
        for tool in v:
            if isinstance(tool, BaseTool | Tool | StructuredTool | BaseModel):
                valid_tools.append(tool)
            else:
                logger.warning(f"Ignoring invalid tool type: {type(tool).__name__}")

        return valid_tools

    @field_validator("toolkit")
    def validate_toolkit(self, v):
        """Validate toolkit is of the correct type."""
        if v is None:
            return v

        if isinstance(v, list):
            valid_toolkits = []
            for tk in v:
                if isinstance(tk, BaseToolkit) or hasattr(tk, "get_tools"):
                    valid_toolkits.append(tk)
                else:
                    logger.warning(
                        f"Ignoring invalid toolkit type: {type(tk).__name__}"
                    )
            return valid_toolkits
        if isinstance(v, BaseToolkit) or hasattr(v, "get_tools"):
            return v
        logger.warning(f"Ignoring invalid toolkit type: {type(v).__name__}")
        return None

    @field_validator("tool_choice")
    def validate_tool_choice(self, v):
        """Validate tool_choice has a valid value."""
        valid_choices = ["auto", "required", "none"]
        if v not in valid_choices:
            raise ValueError(f"tool_choice must be one of {valid_choices}")
        return v
