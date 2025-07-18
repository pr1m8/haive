# Integration Plan for Tool System Improvements

**Date**: 2025-01-05
**Status**: Planning Phase

## 📋 Overview

This document outlines the plan for integrating the structured output mixin and enhanced tool route mixin into the existing Haive system.

## 🎯 Goals

1. **Seamless Integration**: Work with existing code without breaking changes
2. **Enhanced Capabilities**: Add new features while maintaining compatibility
3. **Smart Routing**: Context-aware tool routing for Pydantic models
4. **Dynamic Updates**: Allow runtime tool route modifications

## 🔧 Implementation Steps

### Phase 1: Enhance Existing ToolRouteMixin ✅

Instead of creating a new class, we should enhance the existing `ToolRouteMixin` with:

```python
# Add to existing ToolRouteMixin
def update_tool_route(self, tool_name: str, new_route: str) -> "ToolRouteMixin":
    """Update existing tool route dynamically."""

def _analyze_callable_enhanced(self, callable_obj: Callable) -> Dict[str, Any]:
    """Enhanced callable analysis with async, type hints, etc."""
```

### Phase 2: Integrate with StructuredOutputMixin

The existing `StructuredOutputMixin` needs to work with enhanced routing:

```python
# In AugLLMConfig
class AugLLMConfig(ToolRouteMixin, StructuredOutputMixin, InvokableEngine):
    def _analyze_tool(self, tool: Any) -> Tuple[str, Optional[Dict[str, Any]]]:
        # Check structured output context first
        if isinstance(tool, type) and issubclass(tool, BaseModel):
            if self._detect_structured_output_usage(tool):
                return "structured_output_tool", {"context": "structured_output"}
        # Fall back to parent implementation
        return super()._analyze_tool(tool)
```

### Phase 3: Update ToolState Integration

Ensure `ToolState` respects new routing patterns:

```python
# Add new route to engine_route_config
engine_route_config = {
    "llm": ["langchain_tool", "function", "pydantic_model", "structured_output_tool"],
    "aug_llm": ["langchain_tool", "function", "pydantic_model", "structured_output_tool"],
    "parser": ["pydantic_model", "parser", "structured_output_tool"],
}
```

## 🚀 Incremental Implementation

### Step 1: Enhance \_analyze_tool in ToolRouteMixin

Add better callable analysis without breaking existing behavior:

```python
def _analyze_tool(self, tool: Any) -> Tuple[str, Optional[Dict[str, Any]]]:
    """Analyze a tool to determine its route and metadata."""
    metadata = {}

    # Existing logic...
    if callable(tool):
        route = "function"
        # NEW: Enhanced metadata
        metadata.update(self._get_callable_metadata(tool))
```

### Step 2: Add Dynamic Route Updates

Add methods to existing mixin:

```python
def update_tool_route(self, tool_name: str, new_route: str) -> "ToolRouteMixin":
    """Update an existing tool's route."""
    if tool_name in self.tool_routes:
        old_route = self.tool_routes[tool_name]
        self.tool_routes[tool_name] = new_route
        # Track in metadata
        if tool_name not in self.tool_metadata:
            self.tool_metadata[tool_name] = {}
        self.tool_metadata[tool_name]["route_updated"] = True
        self.tool_metadata[tool_name]["previous_route"] = old_route
```

### Step 3: Smart Pydantic Routing

Add context-aware routing:

```python
def route_pydantic_model(self, model: Type[BaseModel], context: str = None) -> str:
    """Route Pydantic model based on context."""
    # Check if used for structured output
    if hasattr(self, "structured_output_model") and model == self.structured_output_model:
        return "structured_output_tool" if self.structured_output_version == "v2" else "parser"

    # Check if executable
    if hasattr(model, "__call__") and callable(getattr(model, "__call__")):
        return "pydantic_model"

    # Default
    return "parser" if context == "output" else "pydantic_model"
```

## 🧪 Testing Strategy

### 1. Unit Tests

- Test enhanced callable analysis
- Test dynamic route updates
- Test Pydantic model routing

### 2. Integration Tests

- Test with AugLLMConfig
- Test with SimpleAgent
- Test state history persistence

### 3. Real Component Tests

- NO MOCKS
- Use actual tools and models
- Save state history for verification

## 📝 Code Changes Summary

### Files to Modify:

1. `/haive-core/src/haive/core/common/mixins/tool_route_mixin.py` - Add enhancements
2. `/haive-core/src/haive/core/engine/aug_llm/config.py` - Integrate routing
3. `/haive-core/src/haive/core/schema/prebuilt/tool_state.py` - Update route config

### New Capabilities:

1. `update_tool_route()` - Dynamic route updates
2. `_analyze_callable_enhanced()` - Better callable metadata
3. `route_pydantic_model()` - Context-aware routing

## ⚠️ Considerations

1. **Backward Compatibility**: All changes must be additive
2. **Performance**: Cache callable analysis results
3. **Type Safety**: Maintain proper type hints
4. **Documentation**: Update docstrings and examples

## 🔄 Next Steps

1. Create patch files for each modification
2. Test incrementally with real components
3. Update documentation
4. Create migration guide if needed
