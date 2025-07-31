# Generalized Recompilation System

**Version**: 1.0  
**Purpose**: Complete implementation of the generalized recompilation mixin  
**Last Updated**: 2025-01-15  
**Status**: Implemented and Integrated

## 🎯 Overview

The Generalized Recompilation System provides a flexible, hash-based change detection and recompilation framework for Haive agents. It integrates with MetaStateSchema to enable dynamic graph modifications and agent recompilation.

## 📋 Core Implementation

The complete RecompilationMixin implementation is located in:
`/home/will/Projects/haive/backend/haive/packages/haive-agents/tests/test_proper_recompilation_system.py`

This implementation includes:

1. **Hash-based Change Detection**: Detect when components need rebuilding
2. **Observer Pattern**: Register callbacks for change notifications
3. **Batch Operations**: Handle multiple changes efficiently
4. **Integration Points**: Works with ValidationNodeConfigV2

## 🏗️ Architecture

### RecompilationMixin Features

```python
class RecompilationMixin:
    """Generalized recompilation support for any agent."""

    # Core tracking
    needs_recompile: bool
    last_recompile_reason: str
    recompile_metadata: dict

    # Observer pattern
    def register_change_callback(callback: Callable)
    def notify_changes()

    # Hash-based detection
    def compute_configuration_hash() -> str
    def has_configuration_changed() -> bool

    # Batch operations
    def batch_mark_for_recompile(reasons: List[str])
    def get_recompile_history() -> List[dict]
```

### Integration with MetaStateSchema

MetaStateSchema inherits from both StateSchema and RecompileMixin:

```python
class MetaStateSchema(StateSchema, RecompileMixin):
    """State schema with embedded agent and recompilation support."""

    # Inherits all RecompileMixin functionality
    # Plus agent embedding and graph composition
```

## 💻 Usage Examples

### 1. Basic Recompilation Tracking

```python
# Any class with RecompileMixin
agent = GraphRecompilableSimpleAgent()

# Mark for recompilation
agent.mark_for_recompile("Configuration changed")

# Check status
if agent.needs_recompile:
    print(f"Reason: {agent.last_recompile_reason}")

# Resolve after recompilation
agent.resolve_recompile(success=True)
```

### 2. Hash-based Change Detection

```python
# Compute initial hash
initial_hash = agent.compute_configuration_hash()

# Make changes
agent.add_tool(new_tool)

# Check if configuration changed
if agent.has_configuration_changed():
    agent.mark_for_recompile("Tool configuration changed")
```

### 3. Observer Pattern

```python
# Register callback
def on_recompile_needed(reason: str):
    print(f"Recompilation needed: {reason}")
    # Trigger graph rebuild

agent.register_change_callback(on_recompile_needed)

# Changes will notify observers
agent.mark_for_recompile("Dynamic change")
```

### 4. Batch Operations

```python
# Multiple changes at once
reasons = [
    "Tool added: calculator",
    "Tool added: web_search",
    "Configuration updated"
]

agent.batch_mark_for_recompile(reasons)
# Single recompilation for all changes
```

### 5. With ValidationNodeConfigV2

```python
from haive.core.schema.node_schema import ValidationNodeConfigV2

# Create validation node with recompilation support
validation_config = ValidationNodeConfigV2(
    output_schema=OutputSchema,
    validation_mode="strict",
    allow_partial=False,
    retry_on_failure=True,
    max_retries=3
)

# Track validation node changes
if validation_config.needs_recompile:
    # Rebuild validation logic
    pass
```

## 🎯 Graph Recompilation Pattern

### Dynamic Node Addition

```python
class GraphRecompilableSimpleAgent(SimpleAgent, RecompilationMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._custom_nodes = {}

    def add_custom_node(self, name: str, node: Callable):
        """Add a custom node to the graph."""
        self._custom_nodes[name] = node
        self.mark_for_recompile(f"Added custom node: {name}")

    def build_graph(self):
        """Build graph with dynamic nodes."""
        graph = super().build_graph()

        # Add custom nodes if any
        for name, node in self._custom_nodes.items():
            graph.add_node(name, node)

        return graph.compile()
```

### Automatic Recompilation

```python
# Agent automatically rebuilds when needed
agent = GraphRecompilableSimpleAgent()

# Add node triggers recompilation
agent.add_custom_node("validator", validation_node)

# Next execution will use rebuilt graph
result = await agent.arun("Process this")
```

## 🔗 Integration Points

### 1. MetaStateSchema Integration

```python
# MetaStateSchema inherits RecompileMixin
meta_state = MetaStateSchema.from_agent(agent)

# All recompilation features available
meta_state.mark_for_recompile("Agent configuration changed")
meta_state.needs_recompile  # True
```

### 2. Multi-Agent Coordination

```python
# Coordinate recompilation across agents
agents = [agent1, agent2, agent3]

# Check if any need recompilation
if any(agent.needs_recompile for agent in agents):
    # Trigger coordinated rebuild
    for agent in agents:
        if agent.needs_recompile:
            agent.recompile()
```

### 3. Graph Context Updates

```python
# Update graph context triggers recompilation
meta_state.graph_context["custom_nodes"] = {
    "preprocessor": preprocess_node,
    "postprocessor": postprocess_node
}

meta_state.mark_for_recompile("Graph context updated")
```

## 🧪 Testing

The complete test suite demonstrates:

1. **Basic recompilation tracking**
2. **Hash-based change detection**
3. **Observer pattern notifications**
4. **Batch operations**
5. **Integration with agents**
6. **Real component testing (no mocks)**

See: `/home/will/Projects/haive/backend/haive/packages/haive-agents/tests/test_proper_recompilation_system.py`

## 🎯 Best Practices

### 1. Clear Recompilation Reasons

```python
# ✅ GOOD - Specific reason
agent.mark_for_recompile("Added calculator tool to tool registry")

# ❌ BAD - Vague reason
agent.mark_for_recompile("Changed")
```

### 2. Batch Related Changes

```python
# ✅ GOOD - Batch multiple changes
changes = []
for tool in new_tools:
    agent.add_tool(tool)
    changes.append(f"Added tool: {tool.name}")
agent.batch_mark_for_recompile(changes)

# ❌ BAD - Individual recompilations
for tool in new_tools:
    agent.add_tool(tool)
    agent.mark_for_recompile(f"Added tool: {tool.name}")
```

### 3. Use Callbacks for Automation

```python
# ✅ GOOD - Automated response
agent.register_change_callback(lambda r: rebuild_graph())

# ❌ BAD - Manual checking
while True:
    if agent.needs_recompile:
        rebuild_graph()
    time.sleep(1)
```

## 🚨 Common Pitfalls

### 1. Forgetting to Resolve

```python
# ❌ BAD - Never resolved
agent.mark_for_recompile("Change")
# needs_recompile stays True forever

# ✅ GOOD - Properly resolved
agent.mark_for_recompile("Change")
do_recompilation()
agent.resolve_recompile(success=True)
```

### 2. Not Checking Hash Changes

```python
# ❌ BAD - Unnecessary recompilation
agent.mark_for_recompile("Maybe changed")

# ✅ GOOD - Check if actually changed
if agent.has_configuration_changed():
    agent.mark_for_recompile("Configuration actually changed")
```

## 📊 Metadata Structure

Recompilation metadata includes:

```python
{
    "history": [
        {
            "timestamp": "2025-01-15T10:00:00",
            "reason": "Tool added: calculator",
            "resolved": True,
            "success": True
        }
    ],
    "total_recompilations": 5,
    "last_successful": "2025-01-15T10:00:00",
    "configuration_hash": "abc123...",
    "registered_callbacks": 2
}
```

## 🔗 Related Documentation

- [MetaStateSchema Pattern](meta_state_pattern.md) - How recompilation integrates with meta state
- [Multi-Agent Memory Hub](multi_agent_meta_agent_memory_hub.md) - Overall architecture
- [Dynamic Tool Routing](../../dynamic_tool_routing_system/) - Original design docs

---

**Remember**: The recompilation system is the foundation for dynamic agent modification in Haive. Use it to build adaptive, self-modifying agent systems.
