"""Tool list mixin for managing LangChain tools.

This module provides a mixin that adds LangChain tool management capabilities
to Pydantic models. It defines a ToolList class that manages various tool types
with automatic expansion of toolkits, type tracking, and convenient querying.

Usage:
    ```python
    from pydantic import BaseModel
    from haive.core.common.mixins.tool_list_mixin import ToolListMixin
    from langchain_core.tools import BaseTool, Tool

    class MyAgent(ToolListMixin, BaseModel):
        name: str

        def run(self, query: str):
            # Access tools by name
            calculator = self.tools.get_tool("calculator")
            result = calculator.run(query)
            return result

    # Create tools
    search_tool = Tool(name="search", func=lambda x: f"Searched for {x}")
    calculator = Tool(name="calculator", func=lambda x: f"Calculated {x}")

    # Create agent with tools
    agent = MyAgent(name="MyAgent", tools=[search_tool, calculator])

    # Get all tools of a specific type
    base_tools = agent.tools.get_by_tool_type("base_tool_instance")
    ```
"""

import inspect
from typing import Any, Callable, Dict, List, Optional, Sequence, Type, Union

from langchain_core.tools import BaseTool, BaseToolkit, StructuredTool
from pydantic import BaseModel, Field, model_validator

from haive.core.common.structures.named_dict import NamedDict


class ToolList(NamedDict):
    """A specialized collection for managing LangChain tools.

    This class extends NamedDict to provide comprehensive tool management
    capabilities with specialized handling for different tool types:
    - BaseTool classes and instances
    - BaseToolkit instances (automatically expands tools)
    - StructuredTool instances
    - Pydantic BaseModel classes (kept as classes)
    - Callable functions

    Attributes:
        name_attrs: Attributes to check for tool names.
        tool_types: Dictionary mapping tool names to their types.
        tools: Sequence of tool objects for proper typing.
    """

    # Override default name attributes to include function names
    name_attrs: list[str] = Field(default=["name", "__name__", "func_name"])

    # Define tool types field
    tool_types: dict[str, str] = Field(
        default_factory=dict, description="Type information for each tool"
    )

    # Define tools field for clear typing and validation
    tools: Sequence[
        type[BaseTool]
        | type[BaseModel]
        | Callable
        | StructuredTool
        | BaseModel
        | BaseTool
        | BaseToolkit
    ] = Field(
        default_factory=list,
        description="The tools to use (BaseTool, BaseToolkit, BaseModel, or Callable)",
    )

    model_config = {"arbitrary_types_allowed": True}

    # Add a custom __new__ method to handle positional arguments
    def __new__(cls, arg=None, **kwargs):
        """Custom constructor to handle positional tool arguments.

        Args:
            arg: Optional positional argument (treated as tools if provided).
            **kwargs: Keyword arguments for initialization.

        Returns:
            New ToolList instance.
        """
        if arg is not None and not isinstance(arg, dict) and "tools" not in kwargs:
            kwargs["tools"] = arg
        return super().__new__(cls)

    @model_validator(mode="before")
    @classmethod
    def process_tools(cls, data: Any) -> Any:
        """Process tools input and expand toolkits.

        This validator handles different tool input formats and expands
        any toolkit instances into their component tools. It works with
        both sequence inputs and dictionary inputs with a 'tools' key.

        Args:
            data: Input data for validation.

        Returns:
            Processed data with expanded tools.
        """
        # If this is a sequence without proper names, convert to dictionary form
        if isinstance(data, list | tuple):
            # Expand toolkits and extract tools
            expanded_tools = []

            for tool in data:
                # Handle toolkits by expanding their tools
                if isinstance(tool, BaseToolkit):
                    try:
                        toolkit_tools = tool.get_tools()
                        expanded_tools.extend(toolkit_tools)
                    except Exception:
                        pass
                else:
                    expanded_tools.append(tool)

            # Now let NamedDict's validator build the dictionary from the expanded tools
            return expanded_tools

        # If we have a dictionary with 'tools' key
        if (
            isinstance(data, dict)
            and "tools" in data
            and isinstance(data["tools"], list | tuple)
        ):
            # Extract the tools
            tools_list = data["tools"]

            # Expand toolkits
            expanded_tools = []
            for tool in tools_list:
                if isinstance(tool, BaseToolkit):
                    try:
                        toolkit_tools = tool.get_tools()
                        expanded_tools.extend(toolkit_tools)
                    except Exception:
                        pass
                else:
                    expanded_tools.append(tool)

            # Replace original tools with expanded ones
            data["tools"] = expanded_tools

            # Keep values field if already present for NamedDict
            if "values" not in data:
                # Create values dictionary from tools
                values = {}
                name_attrs = data.get("name_attrs", ["name", "__name__", "func_name"])

                for tool in expanded_tools:
                    # Extract name
                    name = cls._extract_key(tool, name_attrs)
                    if name:
                        values[name] = tool

                data["values"] = values

        return data

    def model_post_init(self, __context) -> None:
        """Build tool type information after initialization.

        This method runs after model initialization to set up the tool type
        tracking system and process any toolkit tools.
        """
        # Initialize tool_types
        self.tool_types = {}

        # Map all tools to their types
        for name, tool in self.values.items():
            self.tool_types[name] = self._determine_tool_type(tool)

        # Set tools field to match values for proper typing
        self.tools = list(self.values.values())

        # Process tool-specific operations (expand toolkits but keep model classes as classes)
        self._process_tool_types()

    @classmethod
    def _determine_tool_type(cls, tool: Any) -> str:
        """Determine the type of a tool.

        This method analyzes a tool object and determines its type category
        based on class hierarchy and instance type.

        Args:
            tool: The tool to analyze.

        Returns:
            String representing the tool type.
        """
        # Check tool instance types
        if isinstance(tool, BaseTool):
            return "base_tool_instance"

        if isinstance(tool, StructuredTool):
            return "structured_tool_instance"

        if isinstance(tool, BaseModel):
            return "model_instance"

        if isinstance(tool, BaseToolkit):
            return "toolkit"

        # Check tool class types
        if inspect.isclass(tool):
            if issubclass(tool, BaseTool):
                return "base_tool_class"

            if issubclass(tool, BaseModel):
                return "model_class"

            if issubclass(tool, BaseToolkit):
                return "toolkit_class"

        # Check callable
        if callable(tool):
            return "callable"

        return "unknown"

    def _process_tool_types(self) -> None:
        """Process tools based on their types.

        This method handles special tool types like toolkits by expanding
        them into their component tools. It preserves model classes as classes
        rather than instantiating them.
        """
        # Process toolkit classes and instances by expanding their tools
        for name, tool_type in list(self.tool_types.items()):
            if tool_type in ["toolkit", "toolkit_class"] and name in self.values:
                tool = self.values[name]

                try:
                    # Instantiate if it's a class
                    toolkit = tool() if tool_type == "toolkit_class" else tool

                    # Get tools from the toolkit
                    toolkit_tools = toolkit.get_tools()

                    # Remove the toolkit
                    del self.values[name]
                    del self.tool_types[name]

                    # Add the toolkit's tools
                    for t in toolkit_tools:
                        self.add(t)
                except Exception:
                    pass

        # Update tools list to match values
        self.tools = list(self.values.values())

    def add(self, tool: Any, key: str | None = None) -> str:
        """Add a tool with automatic or explicit key.

        This method adds a tool to the collection, automatically expanding
        toolkits into their component tools.

        Args:
            tool: Tool to add.
            key: Optional explicit key to use.

        Returns:
            Key used for the tool.
        """
        # Handle toolkit by expanding its tools
        if isinstance(tool, BaseToolkit):
            added_keys = []
            try:
                toolkit_tools = tool.get_tools()
                for t in toolkit_tools:
                    added_key = self.add(t)
                    added_keys.append(added_key)
                return added_keys[0] if added_keys else ""
            except Exception:
                pass

        # Use parent add method for normal tools
        tool_key = super().add(tool, key)

        # Store tool type
        self.tool_types[tool_key] = self._determine_tool_type(tool)

        # Update tools list to match values
        self.tools = list(self.values.values())

        return tool_key

    def update(self, items: Any) -> None:
        """Update with new tools.

        This method adds multiple tools at once, handling both dictionary
        and sequence inputs, and automatically expanding toolkits.

        Args:
            items: Dictionary or sequence of tools to add.
        """
        # Expand toolkits if this is a sequence
        if isinstance(items, list | tuple):
            expanded_items = []
            for item in items:
                if isinstance(item, BaseToolkit):
                    try:
                        toolkit_tools = item.get_tools()
                        expanded_items.extend(toolkit_tools)
                    except Exception:
                        pass
                else:
                    expanded_items.append(item)

            # Update with expanded items
            super().update(expanded_items)
        else:
            # Use parent update method
            super().update(items)

        # Update tool types for new items
        for key, value in self.values.items():
            if key not in self.tool_types:
                self.tool_types[key] = self._determine_tool_type(value)

        # Update tools list to match values
        self.tools = list(self.values.values())

        # Process toolkits but keep model classes as classes
        self._process_tool_types()

    def get_tool_type(self, name: str) -> str | None:
        """Get type of a specific tool.

        Args:
            name: Tool name to look up.

        Returns:
            Tool type string or None if not found.
        """
        return self.tool_types.get(name)

    def get_by_tool_type(self, tool_type: str) -> list[Any]:
        """Get all tools of a specified type.

        Args:
            tool_type: Type to filter by.

        Returns:
            List of tools matching the type.
        """
        result = []
        for name, type_value in self.tool_types.items():
            if type_value == tool_type and name in self.values:
                result.append(self.values[name])
        return result

    def get_tool_type_mapping(self) -> dict[str, list[str]]:
        """Get mapping of tool types to tool names.

        Returns:
            Dictionary mapping tool types to lists of tool names.
        """
        result = {}
        for name, tool_type in self.tool_types.items():
            if tool_type not in result:
                result[tool_type] = []
            result[tool_type].append(name)
        return result

    def get_tool(self, name: str) -> Any | None:
        """Get a tool by name.

        Args:
            name: Tool name to retrieve.

        Returns:
            Tool if found, None otherwise.
        """
        return self.get(name)

    def get_tool_info(self, name: str) -> dict[str, Any]:
        """Get comprehensive information about a tool.

        This method retrieves detailed information about a tool,
        including its type, description, schema (if available),
        and field information for model classes.

        Args:
            name: Tool name to look up.

        Returns:
            Dictionary with tool information.
        """
        if name not in self.values:
            return {"found": False}

        tool = self.values[name]
        tool_type = self.tool_types.get(name, "unknown")

        info = {"found": True, "name": name, "tool_type": tool_type, "tool": tool}

        # Add tool-specific information
        if hasattr(tool, "description"):
            info["description"] = tool.description

        if hasattr(tool, "args_schema"):
            info["has_schema"] = True
            info["schema"] = tool.args_schema

        if tool_type in ["model_class", "model_instance"]:
            info["is_model"] = True

            # For model classes, get field info
            if (
                tool_type == "model_class"
                and inspect.isclass(tool)
                and issubclass(tool, BaseModel)
            ):
                fields = {}
                for field_name, field in tool.model_fields.items():
                    fields[field_name] = {
                        "type": str(field.annotation),
                        "required": field.is_required(),
                        "description": field.description or "",
                    }
                info["fields"] = fields

        return info

    def get_model_classes(self) -> dict[str, type[BaseModel]]:
        """Get all model classes in the tool list.

        Returns:
            Dictionary mapping name to model class.
        """
        result = {}
        for name, tool_type in self.tool_types.items():
            if tool_type == "model_class" and name in self.values:
                result[name] = self.values[name]
        return result

    def get_model_instances(self) -> dict[str, BaseModel]:
        """Get all model instances in the tool list.

        Returns:
            Dictionary mapping name to model instance.
        """
        result = {}
        for name, tool_type in self.tool_types.items():
            if tool_type == "model_instance" and name in self.values:
                result[name] = self.values[name]
        return result

    def get_tools_by_category(self) -> dict[str, dict[str, Any]]:
        """Get tools organized by category.

        Returns:
            Dictionary with tools grouped by type category.
        """
        categories = {
            "tools": {},  # BaseTool instances
            "models": {},  # Model classes and instances
            "callables": {},  # Function callables
        }

        for name, tool in self.values.items():
            tool_type = self.tool_types.get(name)

            if tool_type in [
                "base_tool_instance",
                "structured_tool_instance",
                "base_tool_class",
            ]:
                categories["tools"][name] = tool
            elif tool_type in ["model_class", "model_instance"]:
                categories["models"][name] = tool
            elif tool_type == "callable":
                categories["callables"][name] = tool

        return categories

    def to_list(self) -> list[Any]:
        """Convert to a simple list of tools.

        Returns:
            List of all tool objects.
        """
        return list(self.values.values())

    def __delitem__(self, key: str) -> None:
        """Delete tool by name.

        Args:
            key: Name of the tool to delete.
        """
        super().__delitem__(key)

        # Also cleanup tool_types
        if key in self.tool_types:
            del self.tool_types[key]

        # Update tools list to match values
        self.tools = list(self.values.values())


class ToolListMixin(BaseModel):
    """Mixin that adds a ToolList for managing LangChain tools.

    This mixin adds a tools attribute to any Pydantic model, providing
    comprehensive tool management capabilities.

    Attributes:
        tools: A ToolList instance for managing tools.
    """

    tools: ToolList = Field(default_factory=ToolList, description="Collection of tools")

    model_config = {"arbitrary_types_allowed": True}
