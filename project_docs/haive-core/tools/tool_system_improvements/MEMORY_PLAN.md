# Tool System Improvements Memory Plan

**Created**: 2025-01-05
**Project**: Haive Tool System Enhancement
**Status**: Active Development

## 📋 Memory Organization

### M001 - Current State Analysis

- **Alias**: TOOL_ANALYSIS
- **Location**: `/analysis/current_system_understanding.md`
- **Purpose**: Document existing tool routing system
- **Status**: ✅ Complete

### M002 - Structured Output Mixin Design

- **Alias**: STRUCT_OUTPUT_DESIGN
- **Location**: `/implementation/structured_output_mixin.py`
- **Purpose**: Design for handling LLM structured output patterns
- **Status**: ✅ Draft Complete

### M003 - Enhanced Tool Route Mixin Design

- **Alias**: ENHANCED_ROUTE_DESIGN
- **Location**: `/implementation/enhanced_tool_route_mixin.py`
- **Purpose**: Improvements to ToolRouteMixin
- **Status**: ✅ Draft Complete

### M004 - Integration Plan

- **Alias**: INTEGRATION_PLAN
- **Location**: `/planning/integration_plan.md`
- **Purpose**: Step-by-step integration approach
- **Status**: ✅ Complete

### M005 - Code Modifications

- **Alias**: CODE_MODS
- **Location**: `/implementation/code_modifications/`
- **Purpose**: Actual code changes to be made
- **Status**: 🔄 In Progress

## 🎯 Implementation Tasks

### T001 - Enhance ToolRouteMixin

**File**: `/haive-core/src/haive/core/common/mixins/tool_route_mixin.py`
**Changes**:

1. Add actual tool storage with `tools: List[ToolType]` field
2. Add `tool_instances: Dict[str, ToolType]` for quick lookup
3. Add `add_tool()` method with validation
4. Add `get_tool()`, `get_tools_by_route()` methods
5. Add `update_tool_route()` method
6. Enhance `_analyze_tool()` with better callable analysis
7. Add tool type validation following LangGraph patterns

### T002 - Update AugLLMConfig

**File**: `/haive-core/src/haive/core/engine/aug_llm/config.py`
**Changes**:

1. Integrate StructuredOutputMixin properly
2. Override `_analyze_tool()` for context-aware routing
3. Handle structured output model routing

### T003 - Update ToolState

**File**: `/haive-core/src/haive/core/schema/prebuilt/tool_state.py`
**Changes**:

1. Add "structured_output_tool" to engine_route_config
2. Update route synchronization logic

### T004 - Create Tests

**Location**: `/haive-agents/tests/tool_improvements/`
**Tests**:

1. test_enhanced_routing.py
2. test_structured_output.py
3. test_dynamic_updates.py

## 📝 Code Snippets

### S001 - update_tool_route Method

```python
def update_tool_route(self, tool_name: str, new_route: str) -> "ToolRouteMixin":
    """Update an existing tool's route dynamically."""
    if tool_name not in self.tool_routes:
        logger.warning(f"Tool '{tool_name}' not found")
        return self

    old_route = self.tool_routes[tool_name]
    self.tool_routes[tool_name] = new_route

    # Update metadata
    if tool_name not in self.tool_metadata:
        self.tool_metadata[tool_name] = {}
    self.tool_metadata[tool_name].update({
        "route_updated": True,
        "previous_route": old_route,
        "update_timestamp": datetime.now().isoformat()
    })

    return self
```

### S002 - Enhanced Callable Analysis

```python
def _get_callable_metadata(self, callable_obj: Callable) -> Dict[str, Any]:
    """Get enhanced metadata for callables."""
    import inspect
    from typing import get_type_hints

    metadata = {
        "is_async": inspect.iscoroutinefunction(callable_obj),
        "parameter_count": len(inspect.signature(callable_obj).parameters),
    }

    try:
        hints = get_type_hints(callable_obj)
        metadata["has_type_hints"] = bool(hints)
        metadata["has_return_type"] = "return" in hints
    except:
        metadata["has_type_hints"] = False

    return metadata
```

### S003 - Context-Aware Pydantic Routing

```python
def route_pydantic_model(self, model: Type[BaseModel], context: Optional[str] = None) -> str:
    """Route Pydantic model based on context."""
    # Check structured output context
    if hasattr(self, "structured_output_model") and model == self.structured_output_model:
        if self.structured_output_version == "v2":
            return "structured_output_tool"
        else:
            return "parser"

    # Check if executable
    if hasattr(model, "__call__") and callable(getattr(model, "__call__")):
        return "pydantic_model"

    # Context hints
    if context == "output":
        return "parser"
    elif context == "tool":
        return "pydantic_model"

    return "pydantic_model"  # default
```

## 🔄 Progress Tracking

- [x] M001 - System Analysis
- [x] M002 - Structured Output Design
- [x] M003 - Enhanced Route Design
- [x] M004 - Integration Planning
- [ ] T001 - Enhance ToolRouteMixin
- [ ] T002 - Update AugLLMConfig
- [ ] T003 - Update ToolState
- [ ] T004 - Create Tests

## 📌 Important Notes

1. **No Breaking Changes**: All modifications must be backward compatible
2. **Type Safety**: Maintain proper type hints throughout
3. **Performance**: Cache expensive operations (callable analysis)
4. **Testing**: Use real components, no mocks

## 🚀 Next Actions

1. **A001**: Add methods to ToolRouteMixin (T001)
2. **A002**: Test with simple callable
3. **A003**: Integrate with AugLLMConfig (T002)
4. **A004**: Create integration test

## 📊 Decision Log

### D001 - Extend vs Replace

**Date**: 2025-01-05
**Decision**: Extend existing mixins rather than create new ones
**Rationale**: Maintains compatibility, easier integration

### D002 - Structured Output Routes

**Date**: 2025-01-05
**Decision**: Add "structured_output_tool" as new route type
**Rationale**: Clear distinction from regular tools

### D003 - Callable Analysis Caching

**Date**: 2025-01-05
**Decision**: Cache callable metadata to avoid repeated analysis
**Rationale**: Performance optimization for large tool sets
