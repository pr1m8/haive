# State Schema Engine Gap - Architecture Analysis

**Created**: 2026-04-06
**Status**: Partially fixed (runtime workaround), needs architectural fix
**Impact**: All agents with tools — tool_node can't find tools at runtime

## Problem Summary

Auto-composed agent state schemas (created by SchemaComposer) do NOT include the `engines` dict field. This means `tool_node` can't find tools at runtime because `state.engines[engine_name]` is always empty.

## Root Cause Chain

1. **Agent._setup_schemas()** creates a SchemaComposer and calls `add_fields_from_engine()` for each engine
2. `add_fields_from_engine()` extracts input/output schema fields but **never adds engine management fields** (engines, tools, tool_routes)
3. `SchemaComposer.add_engine_management()` exists (~line 1822) but is **only called** when the base class is StateSchema
4. Auto-composed schemas are built from scratch without a StateSchema base, so the condition never triggers
5. Result: compiled state has NO `engines` field → tool_node gets empty dict → "No tools available"

## Schema Hierarchy

All pre-built schemas properly inherit `engines` from StateSchema:

```
StateSchema (has engines: dict[str, Engine])
├── MessagesState
│   ├── ToolState (+ ToolRouteMixin)
│   │   ├── LLMState (full engine mgmt)
│   │   │   └── ReactAgentState
│   │   └── MultiAgentState (explicit engines + agent hierarchy)
│   └── MemoryAgentState (via ReactAgentState)
└── Auto-composed schemas → ❌ MISSING engines field
```

## Fixes Applied (Runtime Workarounds)

### Fix 1: Inject engines into invoke_input
**File**: `packages/haive-agents/src/haive/agents/base/mixins/execution_mixin.py`

```python
# Before _app.invoke(), inject engines so tool_node can find them
if isinstance(invoke_input, dict) and hasattr(self, "engines") and self.engines:
    invoke_input.setdefault("engines", self.engines)
```

### Fix 2: Fix _prepare_input for empty schemas
**File**: `packages/haive-agents/src/haive/agents/base/mixins/execution_mixin.py`

When `input_schema` has no `model_fields`, fall back to `{"messages": [HumanMessage(...)]}` instead of returning empty dict.

### Fix 3: Fix _execute_tools serialization
**File**: `packages/haive-core/src/haive/core/graph/node/tool_node_config_v2.py`

```python
# Before (broken): state.dict() serializes BaseMessage to plain dicts
state_dict = state if isinstance(state, dict) else state.dict()

# After (fixed): pass only messages to preserve BaseMessage objects
state_dict = {self.messages_field: messages}
```

## Architectural Fix Needed

### Option A: SchemaComposer always adds engine management
In `SchemaComposer.build()`, always call `add_engine_management()` when engines are present:

```python
def build(self):
    # ... existing build logic ...
    if self.engines:
        self.add_engine_management()  # Always, not just for StateSchema subclasses
```

### Option B: Agent._setup_schemas() explicitly adds engines
```python
def _setup_schemas(self):
    composer = SchemaComposer(name=f"{self.__class__.__name__}State")
    for engine in engine_list:
        composer.add_engine(engine)
        composer.add_fields_from_engine(engine)
    composer.add_engine_management()  # Explicitly add engine fields
    self.state_schema = composer.build()
```

### Option C: Use pre-built LLMState as default
Instead of auto-composing, default to `LLMState` which already has everything:
```python
if not self.state_schema:
    self.state_schema = LLMState  # Has engines, tools, messages
```

## MultiAgent State Patterns

- **MultiAgentState** uses pre-built state (has engines via ToolState)
- Child agents execute via `_create_agent_wrapper()` — only passes **messages**, NOT engines
- Engine syncing happens in `setup_agent_hierarchy()` validator with namespacing: `engines["agent_name.main"]`
- Tools are **NOT dynamically transferred** between agents — each agent pre-compiles its own

## Key Files

| File | What | Lines |
|------|------|-------|
| `haive-agents/base/agent.py` | _setup_schemas() | 313-397 |
| `haive-agents/base/mixins/execution_mixin.py` | invoke with engines | 575-588 |
| `haive-core/schema/schema_composer.py` | add_engine_management | ~1822 |
| `haive-core/schema/state_schema.py` | engines field | 211 |
| `haive-core/graph/node/tool_node_config_v2.py` | _get_tools, _execute_tools | 177-268 |
| `haive-agents/multi/agent.py` | MultiAgent state | 313-382 |
| `haive-core/schema/prebuilt/multi_agent_state.py` | MultiAgentState | full file |

## Testing

```python
# Verify engines are in state at runtime
from haive.agents.react.agent import ReactAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    '''Calculate.'''
    return str(eval(expression))

agent = ReactAgent(
    name="test",
    engine=AugLLMConfig(tools=[calculator]),
    max_iterations=3,
)

# This should work after fixes
result = agent.run("What is 15 * 23?")
# Expected: AIMessage with "345" in response
```
