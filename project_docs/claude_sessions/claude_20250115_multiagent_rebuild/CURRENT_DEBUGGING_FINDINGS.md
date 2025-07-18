# Current Debugging Findings - Multi-Agent Rebuild

**Updated**: 2025-01-15 16:55  
**Status**: Active debugging session

## 🔍 What We Found

### Base Agent Schema Setup Issue

From debug output, we discovered:

1. **Agent normalization works**: `Agents dict: ['agent1']` ✅
2. **State schema override fails**: Gets `MessagesState` instead of `MultiAgentState` ❌
3. **No engines found**: `Engines: []` - agents not added to engines dict ❌
4. **Schema setup sequence problem**:
   - Our `setup_agent()` sets `state_schema = MultiAgentState`
   - Base agent's `_setup_schemas()` runs after and overrides it
   - Since no engines found, falls back to default `MessagesState`

### Debug Output Analysis

```
DEBUG    Setting up schemas for debug_multi with 0 engines and 0 sub-agents
DEBUG    No engines or agents found, using default MessagesState
State schema: <class 'haive.core.schema.prebuilt.messages_state.MessagesState'>
Engines: []
```

**Problem**: The agents aren't being added to the engines dict for schema composition.

## 🔧 MultiAgentState Current Structure

From `/haive-core/src/haive/core/schema/prebuilt/multi_agent_state.py`:

```python
class MultiAgentState(ToolState):
    """State schema for multi-agent systems with hierarchical management."""

    # Agents stored as first-class fields
    agents: list["Agent"] | dict[str, "Agent"] = Field(
        default_factory=dict,
        description="Agent instances contained in this state (not flattened)",
    )

    # Hierarchical state management - each agent has isolated state
    agent_states: dict[str, dict[str, Any]] = Field(
        default_factory=dict,
        description="Isolated state for each agent, preserving their schemas",
    )

    # Execution tracking
    active_agent: str | None = Field(default=None)
    agent_outputs: dict[str, Any] = Field(default_factory=dict)
    agent_execution_order: list[str] = Field(default_factory=list)

    # Recompilation support
    agents_needing_recompile: set[str] = Field(default_factory=set)
    recompile_count: int = Field(default=0)
    recompile_history: list[dict[str, Any]] = Field(default_factory=list)
```

**Key Points**:

- Extends `ToolState` (has messages, tools, token tracking)
- Has `agents` field (list or dict)
- Has `agent_states` for isolated states
- Has execution tracking fields
- Has recompilation support

## 🎯 Possible Solutions

### Option 1: Fix Schema Setup Sequence

```python
def setup_agent(self) -> None:
    """Force MultiAgentState and add agents to engines."""
    # Add agents to engines dict for schema composition
    if isinstance(self.agents, dict):
        for agent_name, agent in self.agents.items():
            # Add agent itself as an "engine" for schema composition
            self.engines[f"agent_{agent_name}"] = agent

            # Add agent's engines with namespacing
            if hasattr(agent, 'engines') and agent.engines:
                for engine_name, engine in agent.engines.items():
                    self.engines[f"{agent_name}.{engine_name}"] = engine

    # Force state schema
    self.state_schema = MultiAgentState
    self.use_prebuilt_base = True
```

### Option 2: Use SchemaComposer Directly

```python
def setup_agent(self) -> None:
    """Use SchemaComposer to compose from agents."""
    if isinstance(self.agents, dict):
        # Use SchemaComposer to create schema from agents
        composer = SchemaComposer()

        # Add MultiAgentState as base
        composer.add_schema(MultiAgentState)

        # Add agent schemas
        for agent_name, agent in self.agents.items():
            if hasattr(agent, 'state_schema') and agent.state_schema:
                composer.add_schema(agent.state_schema, namespace=agent_name)

        # Build composed schema
        self.state_schema = composer.build_schema(name=f"{self.name}State")
```

### Option 3: Force State Schema in model_validator

```python
@model_validator(mode="after")
def force_multi_agent_state(self) -> "ProperMultiAgent":
    """Force MultiAgentState after all setup."""
    # Override any schema setup
    self.state_schema = MultiAgentState
    self.use_prebuilt_base = True

    # Reset schema generation flag
    self.set_schema = False

    return self
```

## 🔄 Next Steps

1. **Try Option 1 first**: Add agents to engines dict
2. **Test with SchemaComposer**: See if it can compose properly
3. **Check MultiAgentState validator**: See if it sets up agents properly
4. **Test AgentNodeV3Config**: Fix the circular import issue

## 📊 Current Status

- **Agent normalization**: ✅ Working
- **State schema**: ❌ Falls back to MessagesState
- **Engines integration**: ❌ Not working
- **AgentNodeV3Config**: ❌ Circular import issue
- **Graph building**: ❌ Blocked by above issues

## 🎯 Focus Areas

1. **Fix schema setup sequence** - Primary issue
2. **Add agents to engines properly** - For schema composition
3. **Test with real LLM execution** - End-to-end validation
4. **AgentNodeV3Config circular import** - Technical blocker

---

**Current approach**: Focus on fixing the schema setup sequence to get MultiAgentState working properly.
