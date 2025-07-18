# MetaStateSchema Pattern Documentation

**Version**: 1.0  
**Purpose**: Guide for using MetaStateSchema for meta-capable agents  
**Last Updated**: 2025-01-15

## 🎯 Overview

MetaStateSchema is the foundation for creating "meta-capable" agents in Haive. It provides:

- **Agent Embedding**: Any agent can be embedded in a MetaStateSchema
- **Execution Tracking**: Full execution history and status monitoring
- **Recompilation Management**: Track when agents need rebuilding
- **Graph Composition**: Support for dynamic graph modifications
- **State Management**: Maintain agent state across executions

## 📋 Core Concept

**Key Insight**: MetaStateSchema IS the meta capability. We don't need a separate MetaAgent class - any agent becomes meta-capable by being embedded in MetaStateSchema.

```python
# Any agent can become meta-capable
simple_agent = SimpleAgent(name="worker", engine=config)
meta_state = MetaStateSchema.from_agent(agent=simple_agent)

# Execute through meta state with full tracking
result = await meta_state.execute_agent(input_data)
```

## 🏗️ Architecture

### MetaStateSchema Structure

```python
class MetaStateSchema(StateSchema, RecompileMixin):
    # Core fields
    agent: Any                          # The embedded agent
    agent_state: dict[str, Any]         # Agent's internal state
    graph_context: dict[str, Any]       # Graph composition context
    execution_result: dict[str, Any]    # Last execution result
    composition_metadata: dict[str, Any] # Metadata about composition

    # Tracking fields
    agent_name: str                     # Agent identifier
    agent_type: str                     # Agent class name
    execution_status: str               # ready/running/completed/error

    # From RecompileMixin
    needs_recompile: bool               # Recompilation flag
    last_recompile_reason: str          # Why recompilation needed
```

### Key Methods

- `from_agent(agent, initial_state, graph_context)` - Create from any agent
- `async execute_agent(input_data, config, update_state)` - Execute embedded agent
- `update_agent(new_agent)` - Dynamically replace agent
- `check_agent_recompilation()` - Check if agent needs rebuilding
- `get_execution_summary()` - Get comprehensive status

## 💻 Usage Patterns

### 1. Basic Meta-Capable Agent

```python
from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.prebuilt.meta_state import MetaStateSchema

# Create any agent
agent = SimpleAgent(
    name="analyzer",
    engine=AugLLMConfig(temperature=0.7)
)

# Make it meta-capable
meta_state = MetaStateSchema.from_agent(
    agent=agent,
    initial_state={"ready": True},
    graph_context={"purpose": "analysis"}
)

# Execute with tracking
result = await meta_state.execute_agent(
    input_data={"messages": [{"role": "user", "content": "Analyze this"}]},
    update_state=True
)

# Check status
summary = meta_state.get_execution_summary()
print(f"Executions: {summary['execution_count']}")
print(f"Status: {summary['current_status']}")
```

### 2. Dynamic Agent Replacement

```python
# Start with one agent
agent_v1 = SimpleAgent(name="v1", engine=config1)
meta_state = MetaStateSchema.from_agent(agent_v1)

# Execute with v1
await meta_state.execute_agent({"query": "Hello"})

# Dynamically update to v2
agent_v2 = SimpleAgent(name="v2", engine=config2)
meta_state.update_agent(agent_v2)  # Triggers recompilation

# Continue with v2
await meta_state.execute_agent({"query": "Hello again"})
```

### 3. Recompilation Tracking

```python
# Create meta-capable agent
meta_state = MetaStateSchema.from_agent(agent)

# Check recompilation status
if meta_state.needs_recompile:
    print(f"Recompile needed: {meta_state.last_recompile_reason}")

# Mark for recompilation
meta_state.mark_for_recompile("Configuration changed")

# Resolve after recompilation
meta_state.resolve_recompile(success=True)
```

### 4. Graph Composition Pattern

```python
# Add custom nodes to graph context
meta_state.graph_context["custom_nodes"] = {
    "validator": validation_node,
    "transformer": transform_node
}

# Mark for recompilation to rebuild graph
meta_state.mark_for_recompile("Added custom nodes")

# Graph rebuilds on next execution
result = await meta_state.execute_agent(input_data)
```

## 🔄 Multi-Agent Coordination

### Sequential Pattern

```python
# Create meta-capable agents
planner_meta = MetaStateSchema.from_agent(
    ReactAgent(name="planner", tools=[research_tool])
)

executor_meta = MetaStateSchema.from_agent(
    SimpleAgent(name="executor", structured_output_model=ResultModel)
)

# Sequential execution
plan_result = await planner_meta.execute_agent({"task": "Create report"})
exec_result = await executor_meta.execute_agent(plan_result["output"])
```

### Shared Context Pattern

```python
# Shared graph context
shared_context = {
    "workflow_id": "report_generation",
    "shared_memory": {}
}

# Create agents with shared context
agent1_meta = MetaStateSchema.from_agent(
    agent1,
    graph_context=shared_context
)

agent2_meta = MetaStateSchema.from_agent(
    agent2,
    graph_context=shared_context
)

# Updates to shared context are visible to both
agent1_meta.graph_context["shared_memory"]["key"] = "value"
# agent2_meta can access this
```

## 🧪 Testing Pattern

```python
import asyncio
import pytest
from haive.agents.simple import SimpleAgent
from haive.core.schema.prebuilt.meta_state import MetaStateSchema

@pytest.mark.asyncio
async def test_meta_capable_agent():
    """Test agent with meta capabilities."""
    # Create and wrap agent
    agent = SimpleAgent(name="test", engine=AugLLMConfig())
    meta_state = MetaStateSchema.from_agent(agent)

    # Execute
    result = await meta_state.execute_agent(
        {"messages": [{"role": "user", "content": "Test"}]}
    )

    # Verify
    assert result["status"] == "success"
    assert meta_state.execution_count == 1
    assert not meta_state.needs_recompile
```

## 🎯 Best Practices

### 1. Always Use Async Execution

```python
# ✅ CORRECT - Use async
result = await meta_state.execute_agent(input_data)

# ❌ WRONG - Don't use sync patterns
result = meta_state.execute_agent(input_data)  # This won't work
```

### 2. Handle Recompilation Properly

```python
# Check before execution
if meta_state.check_agent_recompilation():
    # Agent needs rebuilding
    meta_state.mark_for_recompile("Agent requested recompilation")
    # Trigger graph rebuild...
```

### 3. Use Factory Method

```python
# ✅ CORRECT - Use from_agent factory
meta_state = MetaStateSchema.from_agent(agent)

# ❌ AVOID - Direct construction
meta_state = MetaStateSchema(agent=agent)  # Less convenient
```

### 4. Track Execution History

```python
# Get comprehensive summary
summary = meta_state.get_execution_summary()

# Access specific tracking
print(f"Total executions: {summary['execution_count']}")
print(f"Last execution: {summary['last_execution']}")
print(f"Current status: {summary['current_status']}")
```

## 🚨 Common Pitfalls

### 1. Forgetting Async

```python
# ❌ WRONG - Sync execution
def run_agent():
    result = meta_state.execute_agent(input)  # Will fail

# ✅ CORRECT - Async execution
async def run_agent():
    result = await meta_state.execute_agent(input)
```

### 2. Not Checking Recompilation

```python
# ❌ WRONG - Ignoring recompilation
await meta_state.execute_agent(input)

# ✅ CORRECT - Check and handle
if meta_state.needs_recompile:
    # Handle recompilation
    pass
await meta_state.execute_agent(input)
```

### 3. Direct State Mutation

```python
# ❌ WRONG - Direct mutation
meta_state.agent = new_agent

# ✅ CORRECT - Use update method
meta_state.update_agent(new_agent)
```

## 📊 Execution Record Structure

After execution, the result contains:

```python
{
    "timestamp": "2025-01-15T10:30:00",
    "input": {...},                    # Input data sent
    "output": {...},                    # Agent output
    "config": {...},                    # Execution config
    "status": "success|error"           # Execution status
}
```

## 🔗 Integration Points

### With Graphs

```python
# In a graph node
async def meta_agent_node(state):
    meta_state = state.get("meta_state")
    result = await meta_state.execute_agent(state)
    return {"execution_result": result}
```

### With Tools

```python
@tool
def execute_meta_agent(agent_name: str, input_data: dict) -> dict:
    """Execute a meta-capable agent."""
    meta_state = get_meta_state(agent_name)
    result = asyncio.run(meta_state.execute_agent(input_data))
    return result
```

## 🎯 Next Steps

1. **Multi-Agent Coordinator** - Build MultiAgent to coordinate meta-capable agents
2. **Graph Recompilation** - Implement dynamic node addition/removal
3. **State Persistence** - Add checkpointing for long-running workflows
4. **Performance Optimization** - Cache compiled graphs

---

**Remember**: MetaStateSchema is the foundation for all meta-capability in Haive. Any agent can become meta-capable by being embedded in MetaStateSchema.
