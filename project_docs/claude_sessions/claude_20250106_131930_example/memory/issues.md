# Issues & Solutions

## Issue: Schema Generation Conflicts

**Encountered**: When creating agents with multiple engines
**Symptoms**:

- FieldError: duplicate field names
- Schema validation failures
  **Root Cause**: Engines may have overlapping output field names
  **Solution**:

```python
# Use field prefixing in SchemaComposer
composer = SchemaComposer(
    base_state_schema=MyState,
    field_prefix_strategy="engine_name"  # Prefix fields with engine name
)
```

**Prevention**: Always check engine output fields before combining

## Issue: Tool Routing Failures

**Encountered**: During multi-engine agent setup
**Symptoms**:

- Tools not found by router
- "No engine handles this tool" errors
  **Root Cause**: Tool routes not properly configured
  **Solution**:

```python
# Explicit tool routing in engine config
engine_config = AugLLMConfig(
    tools=[calculator, web_search],
    tool_route="math_engine"  # Route these tools to specific engine
)
```

**Prevention**: Define clear tool routing strategy upfront

## Issue: Engine Registration Missing

**Encountered**: When using engine in graph nodes
**Symptoms**:

- "Engine not found in registry" errors
- Nodes fail to initialize
  **Root Cause**: Engines must be registered globally
  **Solution**:

```python
from haive.core.engine.base import EngineRegistry

registry = EngineRegistry.get_instance()
registry.register(my_engine)
```

**Prevention**: Register engines immediately after creation

## Issue: State Persistence Confusion

**Encountered**: When implementing conversation memory
**Symptoms**:

- State not persisting between calls
- Conversation context lost
  **Root Cause**: Missing thread_id in configuration
  **Solution**:

```python
config = {"configurable": {"thread_id": "unique-conversation-id"}}
result = await agent.arun(input, config=config)
```

**Prevention**: Always use thread_id for stateful conversations
