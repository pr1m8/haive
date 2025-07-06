# Tool System Analysis - Current State & Improvements Needed

**Date**: 2025-01-05  
**Status**: Analysis Phase  
**Goal**: Improve tool routing, structured output, and Pydantic model handling

## 🎯 User Requirements

### 1. Structured Output Mixin

- Help create a mixin that handles `with_structured_output` properly
- Should work with the `bind_tools` and `with_structured_output` pattern from BaseChatModel
- Integrate with AugLLMConfig's existing tool system

### 2. Tool Route Mixin Improvements

- Better support for callables (functions, methods, lambdas)
- Dynamic route addition capability
- Support for `add_routed_tool(tool, route)` pattern
- Better handling of tool type detection

### 3. Pydantic Model Dual Purpose

- When used as structured output → acts as parser
- When used as tool → acts as executable tool
- Smart detection of usage context

## 📊 Current System Analysis

### ToolRouteMixin Current State

```python
# From tool_route_mixin.py
class ToolRouteMixin(BaseModel):
    tool_routes: Dict[str, str]  # tool_name → route
    tool_metadata: Dict[str, Dict[str, Any]]
    tools_dict: Dict[str, List[Any]]  # category → tools
    routed_tools: List[Tuple[Any, str]]  # (tool, route) pairs

    def _analyze_tool(self, tool: Any) -> Tuple[str, Optional[Dict[str, Any]]]:
        # Current detection:
        # - BaseModel subclass → "pydantic_model"
        # - BaseTool → "langchain_tool"
        # - callable → "function"
        # - else → "unknown"
```

### Problems with Current System

1. **Callable Detection**: Too simplistic - just checks `callable(tool)`
2. **No Structured Output Integration**: Doesn't understand `with_structured_output` context
3. **Static Routes**: Once set, routes are fixed - no dynamic updating
4. **Pydantic Model Confusion**: Always treats as "pydantic_model" route, doesn't distinguish usage

### AugLLMConfig Tool Handling

```python
# From aug_llm/config.py
class AugLLMConfig(ToolRouteMixin, InvokableEngine):
    tools: List[Any] = Field(default_factory=list)
    structured_output_model: Optional[Type[BaseModel]] = None

    # Two approaches for structured output:
    # v1: Parser-based (output_parser)
    # v2: Tool-based (bind_tools + with_structured_output)
```

## 🔍 Key Relationships to Understand

### 1. Tool State & Schema Relationship

```python
# ToolState manages tools at the state level
class ToolState(MessagesState):
    tools: List[Any]
    tool_routes: Dict[str, str]
    engine_route_config: Dict[str, List[str]] = {
        "llm": ["langchain_tool", "function", "pydantic_model"],
        "aug_llm": ["langchain_tool", "function", "pydantic_model"],
        "retriever": ["retriever"],
        "parser": ["pydantic_model"],
    }
```

### 2. Tool Node & Validation Relationship

```python
# ValidationNodeConfig gets tools from state.engines
# ToolNodeConfig executes tools based on routes
# Both use ToolRouteMixin for routing logic
```

### 3. BaseChatModel Integration Points

```python
# From langchain_core
def bind_tools(self, tools: Sequence[Union[Dict, type, Callable, BaseTool]]) -> Runnable:
    """Bind tools to the model."""

def with_structured_output(self, schema: Union[Dict, type]) -> Runnable:
    """Returns outputs formatted to match schema."""
    # Uses bind_tools internally with tool_choice="any"
```

## 🎯 Proposed Improvements

### 1. Enhanced Tool Route Mixin

```python
class EnhancedToolRouteMixin(ToolRouteMixin):
    # New fields
    dynamic_routes: bool = Field(default=True, description="Allow dynamic route updates")
    structured_output_routes: Dict[str, str] = Field(
        default_factory=dict,
        description="Routes for structured output models"
    )

    def add_routed_tool(self, tool: Any, route: str, metadata: Optional[Dict] = None):
        """Add tool with explicit route dynamically."""

    def update_tool_route(self, tool_name: str, new_route: str):
        """Update existing tool route dynamically."""

    def _analyze_callable(self, callable_obj: Callable) -> Tuple[str, Dict[str, Any]]:
        """Enhanced callable analysis."""
        # Check for:
        # - Function vs method vs lambda
        # - Type hints
        # - Async vs sync
        # - Parameter inspection
```

### 2. Structured Output Mixin

```python
class StructuredOutputMixin(BaseModel):
    """Mixin for handling structured output with LLMs."""

    structured_output_model: Optional[Type[BaseModel]] = None
    structured_output_method: Literal["parser", "tool_calling"] = "tool_calling"
    include_raw: bool = False

    def with_structured_output(
        self,
        schema: Union[Dict, Type[BaseModel]],
        **kwargs
    ) -> Runnable:
        """Configure LLM for structured output."""

    def _detect_structured_output_usage(self) -> bool:
        """Detect if in structured output context."""
```

### 3. Smart Pydantic Model Handling

```python
def _route_pydantic_model(self, model: Type[BaseModel], context: str) -> str:
    """Smart routing based on usage context."""
    if context == "structured_output":
        return "parser"
    elif hasattr(model, "__call__") and callable(getattr(model, "__call__")):
        return "tool"
    else:
        return "pydantic_model"
```

## 🚧 Implementation Considerations

### 1. Backward Compatibility

- Must not break existing tool routing
- Should enhance, not replace current behavior
- Maintain existing API surface

### 2. Integration Points

- AugLLMConfig needs structured output mixin
- ToolState needs to understand new routes
- ValidationNodeConfig needs to handle dynamic routes

### 3. Type Safety

- Proper type hints for all callable types
- Union types for tool definitions
- Runtime type checking for safety

## 📝 Next Steps

1. **Create StructuredOutputMixin** - New file in `haive-core/src/haive/core/common/mixins/`
2. **Enhance ToolRouteMixin** - Add dynamic routing capabilities
3. **Update AugLLMConfig** - Integrate structured output mixin
4. **Test with Real Tools** - No mocks, real validation

## 🔗 Key Files to Modify

1. `/haive-core/src/haive/core/common/mixins/tool_route_mixin.py` - Enhance routing
2. `/haive-core/src/haive/core/common/mixins/structured_output_mixin.py` - Create new
3. `/haive-core/src/haive/core/engine/aug_llm/config.py` - Integrate mixins
4. `/haive-core/src/haive/core/schema/prebuilt/tool_state.py` - Update route handling

---

**Critical**: Make changes carefully, test with real components, track with git diff
