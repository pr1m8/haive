# Multi-Agent Msgpack Serialization Issue Summary

## Current Status

The multi-agent system compiles successfully but fails at runtime with:

```
TypeError: Type is not msgpack serializable: ModelMetaclass
```

## Key Findings

### 1. The Issue is NOT with Multi-Agent State

- We successfully serialize engines in multi-agent state to dicts
- The serialization properly handles SecretStr and attempts to handle Pydantic classes
- But this doesn't matter because...

### 2. AgentNodeConfig Uses Agent's Own Engines

- Line 234: `agent_input['engines'] = agent.engines.copy()`
- This means the serialized engines in state are overridden
- Each agent uses its own engine objects, not the ones from state

### 3. The Error Occurs Inside ReactAgent's Execution

- The error happens when ReactAgent runs its own graph
- ReactAgent's engines contain Pydantic ModelMetaclass objects (tools, schemas)
- LangGraph's checkpointer can't serialize these when saving state

### 4. Works Standalone, Fails in Multi-Agent

- ReactAgent with tools works fine when run directly
- Same ReactAgent fails when run inside SequentialAgent
- This suggests different checkpointing configurations

## Root Cause

Engines contain non-serializable Pydantic model classes in fields like:

- `tools` - Contains tool classes with Pydantic args_schema
- `schemas` - Contains Pydantic model classes
- `pydantic_tools` - Contains Pydantic model classes
- `structured_output_model` - Contains Pydantic model class

When LangGraph tries to checkpoint the state, msgpack can't serialize these Python class objects.

## Possible Solutions

### 1. Disable Checkpointing for Agents with Tools

- Detect if agent has tools/schemas
- Compile without checkpointer for those agents

### 2. Custom Serialization at Engine Level

- Modify how engines are stored in agent state
- Convert non-serializable fields to serializable representations
- Reconstruct them when needed

### 3. Use Different Checkpointer

- Investigate if other checkpointer implementations handle this better
- Or configure msgpack to handle these types

### 4. Store Engine References Instead of Objects

- Store engine IDs in state
- Retrieve from EngineRegistry when needed
- But this requires significant refactoring

## Next Steps

Need to understand why checkpointing behavior differs between standalone and multi-agent execution.
