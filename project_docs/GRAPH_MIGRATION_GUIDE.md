# Graph Migration Guide: DynamicGraphBuilder → BaseGraph2

## Overview

This guide shows how to migrate agents from the deprecated `DynamicGraphBuilder` to the current `BaseGraph2` implementation.

## Key Differences

### Deprecated Pattern (DynamicGraphBuilder)

```python
from haive.core.graph.dynamic_graph_builder import DynamicGraph

class OldAgent(Agent):
    def build_graph(self) -> CompiledGraph:
        builder = DynamicGraph(name="my_agent")

        # Instance-based building
        builder.add_node("start", self.start_function)
        builder.add_node("process", self.process_function)
        builder.add_edge("start", "process")

        return builder.compile()
```

### Modern Pattern (BaseGraph2)

```python
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.graph.node.engine_node import EngineNodeConfig

class ModernAgent(Agent):
    def build_graph(self) -> BaseGraph:
        graph = BaseGraph(name="my_agent")

        # Functional building with proper node configs
        graph.add_node("start", self.start_function)
        graph.add_node("process", self.process_function)
        graph.add_edge("start", "process")
        graph.set_entry_point("start")
        graph.set_finish_point("process")

        return graph
```

## Migration Steps

### 1. Update Imports

**Before:**

```python
from haive.core.graph.dynamic_graph_builder import DynamicGraph
```

**After:**

```python
from haive.core.graph.state_graph.base_graph2 import BaseGraph
```

### 2. Update Graph Building Method

**Before:**

```python
def build_graph(self) -> CompiledGraph:
    builder = DynamicGraph(name=self.name)
    # ... build logic
    return builder.compile()
```

**After:**

```python
def build_graph(self) -> BaseGraph:
    graph = BaseGraph(name=self.name)
    # ... build logic
    return graph
```

### 3. Update Node Configuration (if using advanced features)

**Before:**

```python
builder.add_node_with_config("llm", {
    "function": self.llm_function,
    "retry_policy": retry_policy,
    "timeout": 30
})
```

**After:**

```python
from haive.core.graph.node.engine_node import EngineNodeConfig

config = EngineNodeConfig(
    engine=self.engine,
    retry_policy=retry_policy,
    timeout_seconds=30
)
graph.add_node_from_config("llm", config)
```

### 4. Update Entry/Exit Points

**Before:**

```python
builder.set_entry("start")
builder.set_finish("end")
```

**After:**

```python
graph.set_entry_point("start")
graph.set_finish_point("end")
```

## Node Config Types

BaseGraph2 provides specific node configuration types:

- `EngineNodeConfig` - For LLM engine nodes
- `ToolNodeConfig` - For tool execution nodes
- `ParserNodeConfig` - For output parsing nodes
- `ValidationNodeConfig` - For validation nodes

## Example Migration

### Before (ReactAgent with DynamicGraphBuilder)

```python
from haive.core.graph.dynamic_graph_builder import DynamicGraph

class ReactAgent(Agent):
    def build_graph(self) -> CompiledGraph:
        builder = DynamicGraph(name="react_agent")

        builder.add_node("reasoning", self.reasoning_step)
        builder.add_node("action", self.action_step)
        builder.add_node("observation", self.observation_step)

        builder.add_edge("reasoning", "action")
        builder.add_edge("action", "observation")
        builder.add_conditional_edge("observation", self.should_continue, {
            True: "reasoning",
            False: END
        })

        builder.set_entry("reasoning")

        return builder.compile()
```

### After (ReactAgent with BaseGraph2)

```python
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langgraph.graph import END

class ReactAgent(Agent):
    def build_graph(self) -> BaseGraph:
        graph = BaseGraph(name="react_agent")

        graph.add_node("reasoning", self.reasoning_step)
        graph.add_node("action", self.action_step)
        graph.add_node("observation", self.observation_step)

        graph.add_edge("reasoning", "action")
        graph.add_edge("action", "observation")
        graph.add_conditional_edge("observation", self.should_continue, {
            True: "reasoning",
            False: END
        })

        graph.set_entry_point("reasoning")

        return graph
```

## Testing Migration

After migration, verify:

1. All node functions are properly connected
2. Entry and exit points are correctly set
3. Conditional edges work as expected
4. State flow matches original behavior

## Notes

- BaseGraph2 is the current standard and actively maintained
- DynamicGraphBuilder is deprecated and will be removed
- BaseGraph2 provides better validation and debugging capabilities
- Node configurations are more strongly typed in BaseGraph2
