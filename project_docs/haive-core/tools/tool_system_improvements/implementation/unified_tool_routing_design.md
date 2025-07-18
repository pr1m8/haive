# Unified Tool Routing Design

**Date**: 2025-01-05
**Goal**: Unify tool management between ToolRouteMixin and AugLLMConfig

## 🎯 Design Overview

### 1. ToolRouteMixin as Central Tool Store

```python
class ToolRouteMixin:
    # Single source of truth for tools
    tools: List[ToolType] = Field(default_factory=list)
    tool_instances: Dict[str, ToolType] = Field(default_factory=dict)
    tool_routes: Dict[str, str] = Field(default_factory=dict)
    tool_metadata: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
```

### 2. AugLLMConfig Tool Properties

```python
class AugLLMConfig(ToolRouteMixin):
    # Make tools a property that uses ToolRouteMixin storage
    @property
    def tools(self) -> List[Any]:
        """Get all tools from mixin storage."""
        return super().tools

    @tools.setter
    def tools(self, value: List[Any]):
        """Set tools through mixin methods."""
        # Clear existing
        super().tools.clear()
        self.tool_instances.clear()

        # Add each tool properly
        for tool in value:
            self.add_tool(tool)

    # Computed properties for specific tool types
    @property
    def pydantic_tools(self) -> List[Type[BaseModel]]:
        """Get Pydantic model tools."""
        return self.get_tools_by_route("pydantic_model") + \
               self.get_tools_by_route("pydantic_tool")
```

### 3. Tool Processing Flow

```python
def _process_tools(self):
    """Process tools using unified routing."""
    # Clear any stale data
    self.tool_instances.clear()
    self.tool_routes.clear()

    # Process each tool through mixin
    for tool in self.tools:
        # This adds to tool_instances, sets routes, etc.
        self.add_tool(tool)

    # Special handling for structured output
    if self.structured_output_model:
        self._setup_structured_output_tool()
```

### 4. Structured Output Integration

```python
def _setup_structured_output_tool(self):
    """Setup structured output model as a special tool."""
    if not self.structured_output_model:
        return

    # Determine route based on version
    if self.structured_output_version == "v2":
        route = "structured_output_tool"
    else:
        route = "parser"

    # Add with special metadata
    self.add_tool(
        self.structured_output_model,
        route=route,
        metadata={
            "purpose": "structured_output",
            "version": self.structured_output_version,
            "force_choice": self.structured_output_version == "v2",
            "include_format_instructions": self.include_format_instructions
        }
    )
```

### 5. Response Schema Support

```python
def setup_response_schema(self, schema: Union[Dict, Type[BaseModel]]):
    """Setup response schema for providers that support it."""
    # Check if provider supports response_schema
    if not self.llm_config.supports_response_schema:
        logger.warning(f"{self.llm_config.provider} doesn't support response_schema")
        return

    # Add as special tool/schema
    if isinstance(schema, type) and issubclass(schema, BaseModel):
        self.add_tool(
            schema,
            route="response_schema",
            metadata={
                "purpose": "response_format",
                "provider_specific": True
            }
        )
    else:
        # Handle dict schemas
        self.tool_metadata["response_schema"] = {
            "schema": schema,
            "type": "dict"
        }
```

### 6. Tool Filtering for Binding

```python
def get_tools_for_binding(self) -> List[Any]:
    """Get tools appropriate for LLM binding."""
    # Routes that should be bound as tools
    bindable_routes = [
        "langchain_tool",
        "function",
        "pydantic_tool",
        "structured_output_tool"
    ]

    binding_tools = []
    for tool_name, route in self.tool_routes.items():
        if route in bindable_routes:
            tool = self.tool_instances.get(tool_name)
            if tool:
                binding_tools.append(tool)

    return binding_tools

def get_tools_for_parsing(self) -> List[Type[BaseModel]]:
    """Get tools/models for output parsing."""
    parsing_routes = ["parser", "pydantic_model"]

    parsing_tools = []
    for tool_name, route in self.tool_routes.items():
        if route in parsing_routes:
            tool = self.tool_instances.get(tool_name)
            if tool and isinstance(tool, type) and issubclass(tool, BaseModel):
                parsing_tools.append(tool)

    return parsing_tools
```

## 🔄 Migration Steps

### Phase 1: Add Methods to ToolRouteMixin

1. Add `tools` field for actual storage
2. Add `add_tool()` with validation
3. Add `get_tools_by_route()` filtering
4. Keep existing fields for compatibility

### Phase 2: Update AugLLMConfig

1. Make `tools` a property using mixin storage
2. Update `_process_tools()` to use `add_tool()`
3. Add structured output routing
4. Update tool filtering to use routes

### Phase 3: Test & Refine

1. Test with existing code
2. Ensure backward compatibility
3. Add response schema support
4. Test structured output v1/v2

## 📊 Benefits

1. **Single Source of Truth**: All tools in ToolRouteMixin
2. **Consistent Routing**: Every tool has a route
3. **Better Filtering**: Use routes instead of type checking
4. **Metadata Rich**: Each tool has associated metadata
5. **Extensible**: Easy to add new tool types/routes

## 🚨 Considerations

1. **Backward Compatibility**: Existing code expects `tools` to be a list
2. **Performance**: Tool analysis happens once during setup
3. **Validation**: Tools validated when added
4. **Structured Output**: Special handling for v1/v2 versions
