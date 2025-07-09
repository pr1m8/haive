# Compact Summary - Multi-Agent State Rebuild

## The Problem
Current multi-agent implementation flattens agent schemas into one big schema, breaking type safety. Agents expect their specific state types but get a merged state.

## The Solution Direction
1. **MetaAgentState** - A state that CONTAINS agents (not just references)
2. **State Projection** - Each agent gets its expected state type
3. **Recompilation** - Track when agents/tools change
4. **No Schema Flattening** - Keep agent schemas separate

## What's Wrong with Current Prebuilts
- `MetaStateSchema` - Single agent only
- `MultiAgentStateSchema` - Still flattens schemas
- `MetaAgentState` - Just coordination, no agents

## What We Need
```python
class ProperMetaAgentState(StateSchema):
    agents: Dict[str, Agent]  # Actual agents IN state
    agent_states: Dict[str, Any]  # Isolated states per agent
    agents_needing_recompile: Set[str]  # Recompilation tracking
    
    # NO schema flattening!
    # Each agent keeps its own schema
```

## Test Case
Plan-and-Execute pattern with Planner, Executor, Replanner agents - each with different state schemas.

## Key Principle
Agents are IN the state, not just referenced. The state IS the container.