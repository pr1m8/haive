"""
T003 - Unified Tool Management Implementation
This shows the complete unified approach for ToolRouteMixin and AugLLMConfig

Part 1: Enhanced ToolRouteMixin (add to existing class)
Location: /haive-core/src/haive/core/common/mixins/tool_route_mixin.py
"""

from typing import Any, Callable, Dict, List, Optional, Type, Union
from langchain_core.tools import BaseTool, Tool, StructuredTool
from pydantic import BaseModel, Field

# Add to ToolRouteMixin class:

# NEW: Actual tool storage
tools: List[Any] = Field(
    default_factory=list,
    description="List of tools (BaseTool, StructuredTool, Pydantic models, callables)"
)

# NEW: Tool instance mapping for quick lookup  
tool_instances: Dict[str, Any] = Field(
    default_factory=dict,
    description="Mapping of tool names to actual tool instances"
)

def add_tool(
    self, 
    tool: Any,
    route: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> "ToolRouteMixin":
    """Add a tool with automatic routing and metadata.
    
    Args:
        tool: Tool instance to add
        route: Optional explicit route (auto-detected if not provided)
        metadata: Optional metadata for the tool
        
    Returns:
        Self for method chaining
    """
    # Get tool name
    tool_name = self._get_tool_name(tool)
    
    # Add to tools list if not already there
    if tool not in self.tools:
        self.tools.append(tool)
    
    # Store tool instance
    self.tool_instances[tool_name] = tool
    
    # Determine route if not provided
    if route is None:
        route, auto_metadata = self._analyze_tool(tool)
        if metadata:
            metadata.update(auto_metadata or {})
        else:
            metadata = auto_metadata
    
    # Set route and metadata
    self.set_tool_route(tool_name, route, metadata)
    
    logger.debug(f"Added tool '{tool_name}' with route '{route}'")
    return self

def get_tool(self, tool_name: str) -> Optional[Any]:
    """Get a tool instance by name."""
    return self.tool_instances.get(tool_name)

def get_tools_by_route(self, route: str) -> List[Any]:
    """Get all tools with a specific route."""
    tools = []
    for name, tool_route in self.tool_routes.items():
        if tool_route == route:
            tool = self.get_tool(name)
            if tool:
                tools.append(tool)
    return tools

def clear_tools(self) -> "ToolRouteMixin":
    """Clear all tools and routes."""
    self.tools.clear()
    self.tool_instances.clear()
    self.tool_routes.clear()
    self.tool_metadata.clear()
    return self

"""
Part 2: AugLLMConfig Modifications
Location: /haive-core/src/haive/core/engine/aug_llm/config.py
"""

# Change the tools field to use property pattern:

# Remove the existing tools field definition and replace with:
_tools: List[Any] = Field(default_factory=list, alias="tools")

@property
def tools(self) -> List[Any]:
    """Get all tools from unified storage."""
    # Return the tools from ToolRouteMixin
    return list(self.tool_instances.values()) if self.tool_instances else []

@tools.setter
def tools(self, value: List[Any]):
    """Set tools through unified routing system."""
    # Clear existing tools
    self.clear_tools()
    
    # Add each tool through the routing system
    if value:
        for tool in value:
            self.add_tool(tool)
            
    # Store original list for backward compatibility
    self._tools = list(value) if value else []

# Update _process_tools to use unified routing:
def _process_tools(self):
    """Process and validate tools using unified routing."""
    debug_print("🔧 [blue]Processing tools with unified routing...[/blue]")
    
    # Tools are already in the routing system from setter
    # Just need to do AugLLM-specific processing
    
    # Track tool names for bind_tools
    tool_names = []
    basemodel_tools = []
    
    for tool_name, tool in self.tool_instances.items():
        tool_names.append(tool_name)
        
        # Check if it's a BaseModel for special handling
        route = self.tool_routes.get(tool_name)
        if route in ["pydantic_model", "pydantic_tool", "structured_output_tool"]:
            if isinstance(tool, type) and issubclass(tool, BaseModel):
                basemodel_tools.append(tool)
    
    # Update metadata
    self.metadata["tool_names"] = tool_names
    self.metadata["has_basemodel_tools"] = bool(basemodel_tools)
    self.metadata["basemodel_tool_count"] = len(basemodel_tools)
    
    debug_print(f"✅ [green]Processed {len(tool_names)} tools with routes[/green]")

# Override _analyze_tool for AugLLM-specific logic:
def _analyze_tool(self, tool: Any) -> Tuple[str, Optional[Dict[str, Any]]]:
    """Analyze tool with AugLLM-specific routing logic."""
    # Check if this is the structured output model
    if self.structured_output_model and tool == self.structured_output_model:
        route = "structured_output_tool" if self.structured_output_version == "v2" else "parser"
        metadata = {
            "purpose": "structured_output",
            "version": self.structured_output_version,
            "force_choice": self.structured_output_version == "v2"
        }
        return route, metadata
    
    # Use parent implementation
    return super()._analyze_tool(tool)

# Add structured output setup:
def _setup_structured_output_as_tool(self):
    """Add structured output model to tools with proper routing."""
    if not self.structured_output_model:
        return
        
    # Check if already added
    model_name = self.structured_output_model.__name__
    if model_name in self.tool_instances:
        # Update metadata if needed
        existing_metadata = self.tool_metadata.get(model_name, {})
        existing_metadata.update({
            "is_structured_output": True,
            "version": self.structured_output_version,
            "force_choice": self.structured_output_version == "v2"
        })
        self.tool_metadata[model_name] = existing_metadata
    else:
        # Add as new tool
        route = "structured_output_tool" if self.structured_output_version == "v2" else "parser"
        self.add_tool(
            self.structured_output_model,
            route=route,
            metadata={
                "purpose": "structured_output",
                "version": self.structured_output_version,
                "force_choice": self.structured_output_version == "v2"
            }
        )

# Update tool filtering methods:
def get_tools_for_binding(self) -> List[Any]:
    """Get tools appropriate for LLM binding using routes."""
    bindable_routes = [
        "langchain_tool", 
        "function", 
        "pydantic_tool",
        "structured_output_tool"
    ]
    
    return [
        tool for tool_name, tool in self.tool_instances.items()
        if self.tool_routes.get(tool_name) in bindable_routes
    ]

@property
def pydantic_tools(self) -> List[Type[BaseModel]]:
    """Get Pydantic model tools using routes."""
    pydantic_routes = ["pydantic_model", "pydantic_tool", "parser", "structured_output_tool"]
    tools = []
    
    for tool_name, route in self.tool_routes.items():
        if route in pydantic_routes:
            tool = self.tool_instances.get(tool_name)
            if tool and isinstance(tool, type) and issubclass(tool, BaseModel):
                tools.append(tool)
                
    return tools

# Update comprehensive_validation_and_setup:
def comprehensive_validation_and_setup(self):
    """Comprehensive validation using unified tool routing."""
    # ... existing validation ...
    
    # Process tools through unified system
    self._process_tools()
    
    # Setup structured output if configured
    if self.structured_output_model:
        self._setup_structured_output_as_tool()
    
    # ... rest of validation ...

# Add response schema support:
def setup_response_schema(self, schema: Union[Dict, Type[BaseModel]]):
    """Setup response schema for providers that support it.
    
    Args:
        schema: Response schema as dict or Pydantic model
    """
    if not self.llm_config.supports_response_schema:
        logger.warning(
            f"Provider {self.llm_config.provider} doesn't support response_schema"
        )
        return
    
    if isinstance(schema, type) and issubclass(schema, BaseModel):
        # Add as special schema tool
        self.add_tool(
            schema,
            route="response_schema",
            metadata={
                "purpose": "response_format",
                "provider_specific": True,
                "provider": str(self.llm_config.provider)
            }
        )
    else:
        # Store dict schema in metadata
        self.tool_metadata["_response_schema"] = {
            "schema": schema,
            "type": "dict",
            "provider": str(self.llm_config.provider)
        }