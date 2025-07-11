# Comprehensive Guide to Graph Recompilation in Haive

## Overview

Haive provides sophisticated graph recompilation capabilities that allow dynamic modification of agent graphs while maintaining performance through intelligent change detection. This guide covers everything you need to know about recompilation in Haive.

## Quick Start: Do I Need to Recompile?

```python
# Always check before compiling
if graph.needs_recompile():
    compiled_graph = graph.to_langgraph()
    app = compiled_graph.compile(checkpointer=checkpointer)
```

## Core Recompilation System

### BaseGraph2 Recompilation Tracking

The foundation is in `BaseGraph2`:

```python
from haive.core.graph.state_graph.base_graph2 import BaseGraph

graph = BaseGraph(name="my_graph")

# Structural changes automatically mark for recompilation
graph.add_node("agent", agent_func)  # Marks needs_recompile
graph.add_edge("agent", "tool")      # Marks needs_recompile

# Check if recompilation needed
if graph.needs_recompile():
    print(f"Reason: {graph.get_compilation_info()['reason']}")
    compiled = graph.to_langgraph()
    graph.mark_compiled()  # Reset flag
```

### What Triggers Recompilation?

**Requires Recompilation** ✅:

- `add_node()` / `remove_node()`
- `add_edge()` / `remove_edge()`
- `add_conditional_edges()`
- `set_state_schema()`
- `add_branch()`
- Any structural graph changes

**Does NOT Require Recompilation** ❌:

- `interrupt_before` / `interrupt_after`
- Checkpointer configuration
- Thread configuration
- Runtime config parameters
- Debug flags
- Cache/store settings

## Recompilation Detection Methods

### 1. Simple Flag Check

```python
# Most basic check
if graph.needs_recompile():
    # Recompile needed
```

### 2. Detailed Compilation Info

```python
info = graph.get_compilation_info()
# Returns:
{
    "needs_recompile": True,
    "reason": "Node added: agent_node",
    "last_compiled": "2025-01-09T10:30:00",
    "compilation_count": 3,
    "current_state_hash": "abc123...",
    "compiled_state_hash": "def456..."
}
```

### 3. Specific Change Detection

```python
# Check for schema changes
if graph.needs_recompile_for_schemas():
    # Schema changed, recompile

# Check for interrupt changes
if graph.needs_recompile_for_interrupts():
    # Interrupts changed, recompile

# Comprehensive check
changes = graph.check_full_recompilation_needed()
if changes["needs_recompile"]:
    print(f"Changes detected: {changes['changes']}")
```

## Dynamic Tool Routing Pattern

### Single Agent with Dynamic Tools

```python
from haive.agents.simple import SimpleAgent
from haive.core.common.mixins import RecompilationMixin

class RecompilableAgent(RecompilationMixin, SimpleAgent):
    """Agent that tracks when tools change"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tool_route_hash = self._compute_tool_hash()

    def add_tool_dynamically(self, tool, route="tool_node"):
        """Add tool and mark for recompilation"""
        self.engine.add_tool(tool, route)
        self._mark_needs_recompile(f"Tool added: {tool.name}")

    def needs_recompilation(self) -> bool:
        """Check if tools changed"""
        current_hash = self._compute_tool_hash()
        return current_hash != self._tool_route_hash

    def recompile_if_needed(self):
        """Recompile graph if tools changed"""
        if self.needs_recompilation():
            # Rebuild graph with new tools
            self.graph = self.build_graph()
            self._tool_route_hash = self._compute_tool_hash()
            self.mark_compiled("Tools updated")
            return True
        return False
```

### Using Dynamic Tools

```python
# Create agent
agent = RecompilableAgent(name="dynamic_agent", engine=engine)

# Add tool dynamically
from langchain_core.tools import tool

@tool
def calculate(expression: str) -> float:
    """Calculate expression"""
    return eval(expression)

# Add and recompile
agent.add_tool_dynamically(calculate, "tool_node")

if agent.needs_recompilation():
    agent.recompile_if_needed()
    print("Agent recompiled with new tool!")
```

## Recompilation Mixin Pattern

### Generalized RecompilationMixin

```python
from typing import Callable, Optional, Dict, Any
import hashlib

class RecompilationMixin:
    """Mix this into any component needing recompilation tracking"""

    def __init__(self):
        self._state_hash: Optional[str] = None
        self._needs_recompile: bool = False
        self._recompile_reason: Optional[str] = None
        self._change_callbacks: List[Callable] = []

    def _compute_state_hash(self) -> str:
        """Override to compute current state hash"""
        raise NotImplementedError

    def needs_recompilation(self) -> bool:
        """Check if recompilation needed"""
        if self._needs_recompile:
            return True

        current_hash = self._compute_state_hash()
        return current_hash != self._state_hash

    def mark_compiled(self, reason: Optional[str] = None):
        """Mark as compiled and update hash"""
        self._state_hash = self._compute_state_hash()
        self._needs_recompile = False
        self._recompile_reason = None

    def _mark_needs_recompile(self, reason: str):
        """Mark for recompilation with reason"""
        self._needs_recompile = True
        self._recompile_reason = reason
        self._notify_change("recompile_needed", reason=reason)

    def register_change_callback(self, callback: Callable):
        """Register callback for changes"""
        self._change_callbacks.append(callback)

    def _notify_change(self, change_type: str, **kwargs):
        """Notify observers of changes"""
        for callback in self._change_callbacks:
            callback(change_type, **kwargs)
```

### Using the Mixin

```python
class MyDynamicComponent(RecompilationMixin):
    def __init__(self):
        super().__init__()
        self.items = []

    def _compute_state_hash(self) -> str:
        """Hash current items"""
        state_str = str(sorted(self.items))
        return hashlib.md5(state_str.encode()).hexdigest()

    def add_item(self, item):
        """Add item and mark for recompilation"""
        self.items.append(item)
        self._mark_needs_recompile(f"Item added: {item}")
```

## Batch Operations Pattern

### Efficient Multiple Changes

```python
# Start batch mode to delay recompilation
graph.start_batch_mode()

# Make multiple changes
for i in range(10):
    graph.add_node(f"node_{i}", node_funcs[i])

for i in range(9):
    graph.add_edge(f"node_{i}", f"node_{i+1}")

# End batch mode - single recompilation
graph.end_batch_mode()

# Now check once
if graph.needs_recompile():
    compiled = graph.to_langgraph()
```

### DynamicToolRouteMixin Batch Operations

```python
from haive.core.common.mixins import DynamicToolRouteMixin

class BatchToolManager(DynamicToolRouteMixin):
    def update_multiple_tools(self, tool_updates: Dict[str, str]):
        """Update multiple tools efficiently"""
        with self.batch_update_tools():
            for tool_name, new_route in tool_updates.items():
                self.update_tool_route(tool_name, new_route)
        # Single notification after all updates
```

## Advanced Patterns

### 1. Lazy Compilation

```python
class LazyCompiledGraph:
    """Only compile when actually needed"""

    def __init__(self, graph: BaseGraph):
        self.graph = graph
        self._compiled = None
        self._last_hash = None

    def get_or_compile(self) -> CompiledGraph:
        """Get compiled graph, recompiling if needed"""
        current_hash = self.graph._compute_state_hash()

        if self._compiled is None or current_hash != self._last_hash:
            self._compiled = self.graph.to_langgraph().compile()
            self._last_hash = current_hash

        return self._compiled
```

### 2. Change Observer Pattern

```python
class GraphChangeLogger:
    """Log all graph changes"""

    def __init__(self, graph: BaseGraph):
        self.graph = graph
        self.change_log = []

        # Register for changes
        graph.register_change_callback(self.on_change)

    def on_change(self, change_type: str, **kwargs):
        """Log changes"""
        self.change_log.append({
            "timestamp": datetime.now(),
            "type": change_type,
            "details": kwargs
        })
```

### 3. Multi-Agent Recompilation

```python
class MultiAgentSystem:
    """Manage recompilation across multiple agents"""

    def __init__(self):
        self.agents: Dict[str, RecompilableAgent] = {}

    def add_tool_to_all(self, tool, route="tool_node"):
        """Add tool to all agents"""
        for agent in self.agents.values():
            agent.add_tool_dynamically(tool, route)

    def recompile_all_if_needed(self) -> Dict[str, bool]:
        """Recompile all agents that need it"""
        results = {}

        for name, agent in self.agents.items():
            if agent.needs_recompilation():
                results[name] = agent.recompile_if_needed()
            else:
                results[name] = False

        return results
```

## Best Practices

### 1. Always Check Before Compiling

```python
# Good
if graph.needs_recompile():
    compiled = graph.to_langgraph()

# Bad - wasteful
compiled = graph.to_langgraph()  # Compiles every time
```

### 2. Track Recompilation Reasons

```python
# Good - provides context
graph._mark_needs_recompile("Added error handling node")

# Less helpful
graph._mark_needs_recompile("Changes made")
```

### 3. Use Batch Operations

```python
# Good - single recompilation
with graph.batch_operations():
    for node in nodes:
        graph.add_node(node.name, node.func)

# Bad - recompiles after each addition
for node in nodes:
    graph.add_node(node.name, node.func)
    if graph.needs_recompile():
        graph.to_langgraph()
```

### 4. Implement Proper Hash Functions

```python
def _compute_state_hash(self) -> str:
    """Good hash function"""
    # Include all state that affects compilation
    state = {
        "nodes": sorted(self.nodes.keys()),
        "edges": sorted(self.edges),
        "tool_routes": sorted(self.tool_routes.items()),
        "schema": str(self.state_schema)
    }

    state_str = json.dumps(state, sort_keys=True)
    return hashlib.sha256(state_str.encode()).hexdigest()
```

## Common Pitfalls

1. **Forgetting to Check**: Always check `needs_recompile()` before compiling
2. **Over-Recompiling**: Don't recompile for runtime config changes
3. **Hash Collisions**: Ensure hash functions capture all relevant state
4. **Batch Mode Leaks**: Always use context managers or try/finally
5. **Circular Dependencies**: Be careful with change callbacks

## Performance Considerations

- **Hash Computation**: Keep hash functions efficient
- **Lazy Loading**: Only compile when actually invoking
- **Caching**: Cache compiled graphs when possible
- **Batch Operations**: Group structural changes
- **Change Granularity**: Don't track unnecessarily fine changes

## Future Directions

1. **Incremental Compilation**: Only recompile changed parts
2. **Compilation Optimization**: Detect and optimize common patterns
3. **Hot Reloading**: Update running graphs without restart
4. **Compilation Profiling**: Track compilation performance
5. **Visual Diff Tools**: Show what changed between compilations
