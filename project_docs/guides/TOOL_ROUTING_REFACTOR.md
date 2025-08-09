# Tool Routing Refactor Guide

**Created**: 2025-01-08
**Updated**: 2025-01-29
**Purpose**: Document the tool routing system for BaseModel tools and structured output
**Status**: Implemented with clarifications

## Summary

The tool routing system distinguishes between three use cases for BaseModel:

1. **BaseModel without `__call__`** → `pydantic_model` route (error case for tools)
2. **BaseModel with `__call__`** → `pydantic_tool` route (executable tool)
3. **Structured output model** → `parse_output` route (LLM response parsing)

## Key Insight

BaseModel can serve two different purposes:

- **As a tool**: Requires `__call__` method for execution
- **As structured output**: Used for parsing/validating LLM responses

These need different routes because they have different execution paths.

## Route Definitions

### 1. `pydantic_model` Route

- **Purpose**: BaseModel classes passed as tools but lacking `__call__` method
- **Behavior**: Generates error - cannot be executed as tool
- **Example**: `tools=[MyModel]` where MyModel has no `__call__`

### 2. `pydantic_tool` Route

- **Purpose**: BaseModel classes with `__call__` method - executable tools
- **Behavior**: Converted to StructuredTool and executed
- **Example**: `tools=[StatefulTool]` where StatefulTool has `__call__(self, input)`

### 3. `parse_output` Route

- **Purpose**: BaseModel for structured output parsing
- **Behavior**: Used to validate/parse LLM responses
- **Example**: `structured_output_model=ResponseModel`

## Key Changes

### 1. Route Assignment in AugLLMConfig

**File**: `/packages/haive-core/src/haive/core/engine/aug_llm/config.py`
**Line**: 362

```python
# Route to parse_output for structured output models
self.set_tool_route(structured_model_name, "parse_output", metadata)
```

### 2. ValidationNodeV2 Updates

**File**: `/packages/haive-core/src/haive/core/graph/node/validation_node_v2.py`
**Lines**: 320-368

Now handles all three routes:

```python
if route == "parse_output":
    # Handle structured output model
    # Creates ToolMessage with validation result
elif route == "pydantic_model":
    # BaseModel without __call__ - error case
    # Cannot be used as tool
elif route == "pydantic_tool":
    # BaseModel with __call__ - executable
    # Let tool_node handle execution
```

### 3. ToolRouteMixin Analysis

**File**: `/packages/haive-core/src/haive/core/common/mixins/tool_route_mixin.py`
**Lines**: 354-369

Detects executable BaseModel:

```python
if isinstance(tool, type) and issubclass(tool, BaseModel):
    route = "pydantic_model"
    # Check for explicit __call__ method
    if has_explicit_call and callable(tool.__call__):
        metadata["is_executable"] = True
        route = "pydantic_tool"
```

## BaseModel Tool Schema

When a BaseModel has `__call__`, it creates a stateful tool:

```python
class ConfigurableTool(BaseModel):
    prefix: str = "Result"  # Configuration state

    def __call__(self, query: str) -> str:
        return f"{self.prefix}: {query}"

# Each instance has its own state
tool1 = ConfigurableTool(prefix="Answer")
tool2 = ConfigurableTool(prefix="Response")

# Tool schema only includes __call__ parameters (query)
# BaseModel fields (prefix) are internal state
```

## Routing Flow

### BaseModel as Tool

```
tools=[MyModel]
→ Check for __call__
→ Has __call__: "pydantic_tool" route → Convert to StructuredTool → Execute
→ No __call__: "pydantic_model" route → Error (cannot execute)
```

### BaseModel for Output

```
structured_output_model=MyModel
→ "parse_output" route
→ Use for LLM response validation
```

## Testing

Verify routing with:

```python
from haive.core.engine.aug_llm import AugLLMConfig
from pydantic import BaseModel

class NonExecutable(BaseModel):
    name: str

class Executable(BaseModel):
    multiplier: int = 2

    def __call__(self, value: int) -> int:
        return value * self.multiplier

# Non-executable gets pydantic_model route
config1 = AugLLMConfig(tools=[NonExecutable])
assert config1.tool_routes["NonExecutable"] == "pydantic_model"

# Executable gets pydantic_tool route (once ToolRouteMixin is updated)
config2 = AugLLMConfig(tools=[Executable])
# Currently still "pydantic_model" but should be "pydantic_tool"

# Structured output gets parse_output route
config3 = AugLLMConfig(structured_output_model=NonExecutable)
assert config3.tool_routes["NonExecutable"] == "parse_output"
```

## Migration Guide

```python
# ✅ Correct usage patterns

# 1. BaseModel for structured output
config = AugLLMConfig(structured_output_model=ResponseModel)

# 2. BaseModel as tool (must have __call__)
class StatefulTool(BaseModel):
    def __call__(self, input: str) -> str:
        return process(input)

config = AugLLMConfig(tools=[StatefulTool])

# ❌ Incorrect - BaseModel without __call__ as tool
config = AugLLMConfig(tools=[ResponseModel])  # Will error
```

## Key Takeaways

1. **`pydantic_model` is NOT deprecated** - it identifies non-executable BaseModels
2. **`pydantic_tool` is for executable BaseModels** - those with `__call__`
3. **`parse_output` is for structured output** - parsing LLM responses
4. **BaseModel tools are stateful** - each instance maintains configuration
5. **Tool schema != BaseModel schema** - only `__call__` params are tool inputs

## Related Files

- `/packages/haive-core/tests/engine/tool/test_comprehensive_tool_integration.py` - Integration tests
- `/packages/haive-core/src/haive/core/common/mixins/tool_route_mixin.py` - Route determination logic
- `/packages/haive-core/src/haive/core/graph/node/validation_node_v2.py` - Route handling
