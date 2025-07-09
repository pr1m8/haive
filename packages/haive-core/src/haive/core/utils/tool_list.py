"""
Tool list implementation for Haive Core.

This module provides specialized tool collection management and utilities.
"""

import inspect
from typing import Any, Callable, Dict, List, Optional, Sequence, Type, Union

from langchain_core.tools import BaseTool, BaseToolkit, StructuredTool
from pydantic import BaseModel, Field, model_validator

from haive.core.utils.collections import NamedDict


class ToolList(NamedDict):
    """
    A collection of tools that inherits from NamedDict.
    
    Provides specialized handling for:
    - BaseTool classes and instances
    - BaseToolkit instances (automatically expands tools)
    - StructuredTool instances
    - Pydantic BaseModel classes (kept as classes)
    - Callable functions
    """
    # Override default name attributes to include function names
    name_attrs: List[str] = Field(default=["name", "__name__", "func_name"])
    
    # Define tool types field
    tool_types: Dict[str, str] = Field(default_factory=dict, description="Type information for each tool")
    
    # Define tools field for clear typing and validation
    tools: Sequence[
        Union[Type[BaseTool], Type[BaseModel], Callable, StructuredTool, BaseModel, BaseTool, BaseToolkit]
    ] = Field(
        default_factory=list,
        description="The tools to use (BaseTool, BaseToolkit, BaseModel, or Callable)"
    )
    
    model_config = {
        "arbitrary_types_allowed": True
    }
    
    # Add a custom __new__ method to handle positional arguments
    def __new__(cls, arg=None, **kwargs):
        if arg is not None and not isinstance(arg, dict) and "tools" not in kwargs:
            kwargs["tools"] = arg
        return super().__new__(cls)
    
    @model_validator(mode='before')
    @classmethod
    def process_tools(cls, data: Any) -> Any:
        """Process tools input and expand toolkits."""
        # If this is a sequence without proper names, convert to dictionary form
        if isinstance(data, (list, tuple)):
            # Expand toolkits and extract tools
            expanded_tools = []
            
            for tool in data:
                # Handle toolkits by expanding their tools
                if isinstance(tool, BaseToolkit):
                    try:
                        toolkit_tools = tool.get_tools()
                        expanded_tools.extend(toolkit_tools)
                    except Exception as e:
                        print(f"Error extracting tools from toolkit: {e}")
                else:
                    expanded_tools.append(tool)
            
            # Now let NamedDict's validator build the dictionary from the expanded tools
            return expanded_tools
            
        # If we have a dictionary with 'tools' key
        if isinstance(data, dict) and 'tools' in data and isinstance(data['tools'], (list, tuple)):
            # Extract the tools
            tools_list = data['tools']
            
            # Expand toolkits
            expanded_tools = []
            for tool in tools_list:
                if isinstance(tool, BaseToolkit):
                    try:
                        toolkit_tools = tool.get_tools()
                        expanded_tools.extend(toolkit_tools)
                    except Exception as e:
                        print(f"Error extracting tools from toolkit: {e}")
                else:
                    expanded_tools.append(tool)
                    
            # Replace original tools with expanded ones
            data['tools'] = expanded_tools
            
            # Keep values field if already present for NamedDict
            if 'values' not in data:
                # Create values dictionary from tools
                values = {}
                name_attrs = data.get('name_attrs', ["name", "__name__", "func_name"])
                
                for tool in expanded_tools:
                    # Extract name
                    name = cls._extract_key(tool, name_attrs)
                    if name:
                        values[name] = tool
                        
                data['values'] = values
        
        return data
    
    def model_post_init(self, __context) -> None:
        """Build tool type information after initialization."""
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
        """
        Determine the type of a tool.
        
        Args:
            tool: The tool to analyze
            
        Returns:
            String representing tool type
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
        """
        Process tools based on their types.
        
        Expands toolkits but keeps model classes as classes.
        """
        # Process toolkit classes and instances by expanding their tools
        for name, tool_type in list(self.tool_types.items()):
            if tool_type in ["toolkit", "toolkit_class"] and name in self.values:
                tool = self.values[name]
                
                try:
                    # Instantiate if it's a class
                    if tool_type == "toolkit_class":
                        toolkit = tool()
                    else:
                        toolkit = tool
                    
                    # Get tools from the toolkit
                    toolkit_tools = toolkit.get_tools()
                    
                    # Remove the toolkit
                    del self.values[name]
                    del self.tool_types[name]
                    
                    # Add the toolkit's tools
                    for t in toolkit_tools:
                        self.add(t)
                except Exception as e:
                    print(f"Error processing toolkit {name}: {str(e)}")
        
        # Update tools list to match values
        self.tools = list(self.values.values())
    
    def add(self, tool: Any, key: Optional[str] = None) -> str:
        """
        Add a tool with automatic or explicit key.
        
        Args:
            tool: Tool to add
            key: Optional explicit key
            
        Returns:
            Key used for the tool
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
            except Exception as e:
                print(f"Error extracting tools from toolkit: {e}")
                
        # Use parent add method for normal tools
        tool_key = super().add(tool, key)
        
        # Store tool type
        self.tool_types[tool_key] = self._determine_tool_type(tool)
        
        # Update tools list to match values
        self.tools = list(self.values.values())
        
        return tool_key
    
    def update(self, items: Any) -> None:
        """
        Update with new tools.
        
        Args:
            items: Dictionary or sequence of tools
        """
        # Expand toolkits if this is a sequence
        if isinstance(items, (list, tuple)):
            expanded_items = []
            for item in items:
                if isinstance(item, BaseToolkit):
                    try:
                        toolkit_tools = item.get_tools()
                        expanded_items.extend(toolkit_tools)
                    except Exception as e:
                        print(f"Error extracting tools from toolkit: {e}")
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
    
    def get_tool_type(self, name: str) -> Optional[str]:
        """
        Get type of a specific tool.
        
        Args:
            name: Tool name
            
        Returns:
            Tool type string or None if not found
        """
        return self.tool_types.get(name)
    
    def get_by_tool_type(self, tool_type: str) -> List[Any]:
        """
        Get all tools of a specified type.
        
        Args:
            tool_type: Type to filter by
            
        Returns:
            List of tools matching the type
        """
        result = []
        for name, type_value in self.tool_types.items():
            if type_value == tool_type and name in self.values:
                result.append(self.values[name])
        return result
    
    def get_tool_type_mapping(self) -> Dict[str, List[str]]:
        """
        Get mapping of tool types to tool names.
        
        Returns:
            Dictionary mapping tool types to lists of tool names
        """
        result = {}
        for name, tool_type in self.tool_types.items():
            if tool_type not in result:
                result[tool_type] = []
            result[tool_type].append(name)
        return result
    
    def get_tool(self, name: str) -> Optional[Any]:
        """
        Get a tool by name.
        
        Args:
            name: Tool name
            
        Returns:
            Tool if found, None otherwise
        """
        return self.get(name)
    
    def get_tool_info(self, name: str) -> Dict[str, Any]:
        """
        Get comprehensive information about a tool.
        
        Args:
            name: Tool name
            
        Returns:
            Dictionary with tool information
        """
        if name not in self.values:
            return {"found": False}
            
        tool = self.values[name]
        tool_type = self.tool_types.get(name, "unknown")
        
        info = {
            "found": True,
            "name": name,
            "tool_type": tool_type,
            "tool": tool
        }
        
        # Add tool-specific information
        if hasattr(tool, "description"):
            info["description"] = tool.description
        
        if hasattr(tool, "args_schema"):
            info["has_schema"] = True
            info["schema"] = tool.args_schema
            
        if tool_type in ["model_class", "model_instance"]:
            info["is_model"] = True
            
            # For model classes, get field info
            if tool_type == "model_class" and inspect.isclass(tool) and issubclass(tool, BaseModel):
                fields = {}
                for field_name, field in tool.model_fields.items():
                    fields[field_name] = {
                        "type": str(field.annotation),
                        "required": field.is_required(),
                        "description": field.description or ""
                    }
                info["fields"] = fields
        
        return info
    
    def get_model_classes(self) -> Dict[str, Type[BaseModel]]:
        """
        Get all model classes in the tool list.
        
        Returns:
            Dictionary mapping name to model class
        """
        result = {}
        for name, tool_type in self.tool_types.items():
            if tool_type == "model_class" and name in self.values:
                result[name] = self.values[name]
        return result
    
    def get_model_instances(self) -> Dict[str, BaseModel]:
        """
        Get all model instances in the tool list.
        
        Returns:
            Dictionary mapping name to model instance
        """
        result = {}
        for name, tool_type in self.tool_types.items():
            if tool_type == "model_instance" and name in self.values:
                result[name] = self.values[name]
        return result
    
    def get_tools_by_category(self) -> Dict[str, Dict[str, Any]]:
        """
        Get tools organized by category.
        
        Returns:
            Dictionary with tools grouped by type
        """
        categories = {
            "tools": {},  # BaseTool instances
            "models": {}, # Model classes and instances
            "callables": {} # Function callables
        }
        
        for name, tool in self.values.items():
            tool_type = self.tool_types.get(name)
            
            if tool_type in ["base_tool_instance", "structured_tool_instance", "base_tool_class"]:
                categories["tools"][name] = tool
            elif tool_type in ["model_class", "model_instance"]:
                categories["models"][name] = tool
            elif tool_type == "callable":
                categories["callables"][name] = tool
        
        return categories
    
    def to_list(self) -> List[Any]:
        """
        Convert to a simple list of tools.
        
        Returns:
            List of all tools
        """
        return list(self.values.values())
    
    def __delitem__(self, key: str) -> None:
        """Delete tool by name."""
        super().__delitem__(key)
        
        # Also cleanup tool_types
        if key in self.tool_types:
            del self.tool_types[key]
            
        # Update tools list to match values
        self.tools = list(self.values.values())
"""