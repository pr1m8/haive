# Multi-Agent Engine State Issues

## Current Status (2025-06-25)

### What's Working ✅

1. **Tool contamination is fixed** - Each agent only sees its own tools
2. **Engines are being found** - tool_node can find engines in state
3. **Base ReactAgent works alone** - Single agent execution works fine
4. **Validation passes** - Tools are correctly routed

### What's Breaking ❌

1. **msgpack serialization error** - "Type is not msgpack serializable: ModelMetaclass"
   - Happens when storing Pydantic engine objects in state
   - Only occurs in multi-agent context

## Key Files

### Core Schema Files

- `/packages/haive-core/src/haive/core/schema/schema_composer.py`
  - Builds state schemas dynamically
  - Adds `engines` field with default_factory
  - Stores engines on schema class

- `/packages/haive-core/src/haive/core/schema/agent_schema_composer.py`
  - Extends SchemaComposer for multi-agent
  - Currently skips engine copying to prevent contamination

### Node Configurations

- `/packages/haive-core/src/haive/core/graph/node/agent_node.py`
  - AgentNodeConfig - executes agents within multi-agent
  - Extracts agent-specific state from multi-agent state
  - Ensures engines are included in agent state

- `/packages/haive-core/src/haive/core/graph/node/tool_node_config.py`
  - Looks for engines in `state.engines[engine_name]`
  - Successfully finds engines now

- `/packages/haive-core/src/haive/core/graph/node/validation_node_config.py`
  - Routes tool calls
  - Can get engine from state or EngineRegistry

### Agent Files

- `/packages/haive-agents/src/haive/agents/base/agent.py`
  - Base agent class
  - Uses SchemaComposer.from_components() for single agents

- `/packages/haive-agents/src/haive/agents/multi/base.py`
  - MultiAgent base class
  - `_prepare_input()` populates engines in state
  - Uses AgentSchemaComposer.from_agents()

### Test Files

- `/packages/haive-agents/src/haive/agents/multi/test.py`
  - Simple test: ReactAgent → SimpleAgent
  - ReactAgent has 'add' tool
  - SimpleAgent has 'Plan' schema

## The Issue in Detail

### Single Agent (Works ✅)

```python
# ReactAgent alone
agent = ReactAgent(name="Test")
agent.compile()
result = agent.run({"messages": [...]})  # Works!
```

### Multi-Agent (Breaks ❌)

```python
# SequentialAgent with ReactAgent → SimpleAgent
structured_react = SequentialAgent(
    agents=[react_agent, simple_agent]
)
structured_react.compile()
result = structured_react.run({"messages": [...]})  # msgpack error!
```

## Key Observations

1. **State Schema Differences**
   - ReactAgentState has `engines` field (Dict[str, Any])
   - Engines field has empty dict as default
   - In multi-agent, we populate this with actual engine objects

2. **Engine Storage**
   - Engines are Pydantic models (AugLLMConfig)
   - Stored on schema class: `schema.engines = {...}`
   - Also stored in state instance when running

3. **Serialization Issue**
   - LangGraph uses msgpack for checkpointing
   - msgpack can't serialize Pydantic model classes
   - Error happens after tool_node executes

## Questions to Resolve

1. **Should engines be in state at all?**
   - Pro: tool_node needs them
   - Con: Serialization issues

2. **Alternative approaches?**
   - Store only engine names in state?
   - Use EngineRegistry exclusively?
   - Mark engines field as non-serializable?

3. **Why does single agent work?**
   - Maybe because engines field is empty dict?
   - Or single agent doesn't checkpoint same way?

## Possible Solutions

### Option 1: Store Engine Names Only

```python
# In state
engines: Dict[str, str] = {"aug_llm_123": "aug_llm_123"}
# Then lookup from EngineRegistry when needed
```

### Option 2: Exclude Engines from Serialization

```python
engines: Dict[str, Any] = Field(exclude=True)
```

### Option 3: Custom Serialization

- Override state serialization to handle engines specially
- Convert to dict representation for msgpack

### Option 4: Different Architecture

- Don't store engines in state
- Pass through graph differently
- Use thread-local or context storage?

## Next Steps

1. Understand why single agent doesn't hit serialization issue
2. Test if empty engines dict vs populated makes difference
3. Decide on architectural approach
4. Implement solution that preserves working functionality
