# State Schema Research Notes

**Created**: 2026-04-06
**Purpose**: Research findings on state schema composition, engine injection, and tool routing

## How State Flows Through Agents

```
Agent.__init__()
  → _setup_schemas() → SchemaComposer → auto-composed state (MISSING engines)
  → build_graph() → BaseGraph with state_schema
  → compile() → _app = LangGraph CompiledGraph

Agent.run(input)
  → _prepare_input(input) → {"messages": [HumanMessage(...)]}
  → execution_mixin injects engines into invoke_input  ← FIX APPLIED
  → _app.invoke(invoke_input)
    → agent_node: GenericEngineNodeConfig.__call__(state)
      → self.engine (direct ref, works)
      → LLM generates AIMessage with tool_calls
    → routing: conditional edges check tool_calls
    → tool_node: ToolNodeConfig.__call__(state)
      → _get_tools(state): looks up state.engines[engine_name].tools
      → _execute_tools: ToolNode.invoke({messages: [...]})
```

## Three Bugs Found & Fixed

### 1. _prepare_input returns empty dict
**Root**: Auto-composed input_schema has no model_fields
**Fix**: Fall back to `{"messages": [HumanMessage(content=input_data)]}` when schema is empty
**File**: `execution_mixin.py` line ~60

### 2. _execute_tools serializes messages to dicts
**Root**: `state.dict()` / `model_dump()` converts BaseMessage objects to plain dicts
**Fix**: Pass `{messages_field: messages}` directly instead of full state serialization
**File**: `tool_node_config_v2.py` line ~251

### 3. engines not in runtime state
**Root**: Auto-composed schema doesn't include `engines` field (SchemaComposer gap)
**Fix**: Runtime injection in execution_mixin before `_app.invoke()`
**Proper fix needed**: SchemaComposer.build() should always call add_engine_management()
**File**: `execution_mixin.py` line ~583

## Schema Composition Deep Dive

### What SchemaComposer Does
1. Creates dynamic Pydantic model with name like "ReactAgentState"
2. Calls `add_fields_from_engine(engine)` → extracts input/output schemas
3. Calls `build()` → assembles fields into new BaseModel subclass
4. Does NOT call `add_engine_management()` unless base is StateSchema

### What add_engine_management() Adds
- `tools`: list field
- `tool_instances`: dict field
- `tool_routes`: dict field
- `tool_metadata`: dict field
- `engines`: dict[str, Engine] field ← THE CRITICAL ONE

### Pre-built vs Auto-composed

| Schema | Has engines | Has tools | Has messages | Source |
|--------|-------------|-----------|--------------|--------|
| StateSchema | ✅ | ❌ | ❌ | Base class |
| MessagesState | ✅ | ❌ | ✅ | Prebuilt |
| ToolState | ✅ | ✅ | ✅ | Prebuilt |
| LLMState | ✅ | ✅ | ✅ | Prebuilt |
| ReactAgentState | ✅ | ✅ | ✅ | Prebuilt |
| MultiAgentState | ✅ | ✅ | ✅ | Prebuilt |
| Auto-composed | ❌ | ❌ | ✅ | SchemaComposer |

## MultiAgent State Patterns

### How MultiAgent Handles Engines
- MultiAgentState has explicit `agents: dict[str, Agent]` field
- `setup_agent_hierarchy()` validator syncs engines from all children
- Namespacing: `engines["agent_name.main"]` + fallback `engines["main"]`

### How Child Agents Execute
- `_create_agent_wrapper()` creates closure over agent instance
- Extracts ONLY messages from parent state
- Invokes child `agent._app.invoke({"messages": [...]})`
- Returns dict with updated messages + agent_states + agent_outputs
- **Tools NOT transferred** between agents

### State Isolation
- Each child agent has isolated state in `agent_states: dict[str, dict]`
- No schema flattening — agents maintain independence
- Error isolation per agent

## Recommendations

### Short-term (done)
- ✅ Runtime engine injection in execution_mixin
- ✅ Fix _prepare_input for empty schemas
- ✅ Fix _execute_tools serialization

### Medium-term (needed)
- Make SchemaComposer always include engine management when engines present
- Or default to LLMState instead of auto-composing
- Fix MultiAgent wrapper to pass engines to children

### Long-term
- Unify state schema approach — all agents should use LLMState-based schemas
- Remove auto-composition for agents (keep for generic workflows only)
- Add tool transfer protocol for MultiAgent child communication
