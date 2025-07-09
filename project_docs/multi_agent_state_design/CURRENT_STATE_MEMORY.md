# Multi-Agent State Design - Current State Memory

## What We've Discovered

### 1. Core Issues
- **AgentSchemaComposer** flattens schemas incorrectly - loses type safety
- **MultiAgent** in agents/multi/base.py uses this flawed approach
- **AgentNodeV2** tries to handle projection but it's incomplete
- **Plan-and-Execute** pattern is our test case from LangGraph

### 2. Key Insights

#### Graph Recompilation
- BaseGraph2 has `needs_recompile()` and recompilation tracking
- Dynamic tool routing requires recompilation checks
- Agents can change at runtime and graph needs to recompile

#### Meta Agent Concept
- **MetaAgentState** should contain agents IN the state
- Not just references, but actual agent instances
- Enables dynamic agent management with recompilation

#### Prebuilt Schemas Found
1. **MetaStateSchema** (in prebuilt/meta_state.py)
   - Contains single agent
   - Has execute_agent() method
   - Syncs engines from contained agent

2. **MultiAgentStateSchema** (in core/schema/)
   - Populates engines dict from agents
   - Handles engine visibility for nodes
   - Has recompilation tracking

3. **MetaAgentState** (in core/schema/)
   - Coordination focused
   - Tracks active agent, outputs, history
   - No actual agents stored

### 3. Problems with Current Prebuilt Schemas

- **MetaStateSchema** - Only handles single agent, not multi
- **MultiAgentStateSchema** - Still uses flattened approach
- **MetaAgentState** - Doesn't contain agents, just coordination

### 4. What Needs to Be Rebuilt

1. **New MetaAgentState** that:
   - Contains agents as first-class fields
   - Tracks recompilation needs
   - Handles state projection per agent
   - Maintains type safety

2. **New MultiAgent** that:
   - Uses the new MetaAgentState
   - Doesn't flatten schemas
   - Supports recompilation
   - Uses compilation kwargs from base

3. **Enhanced AgentNode** that:
   - Projects state correctly
   - Maintains type safety
   - Updates meta state properly

### 5. Key Requirements

- Must work with BaseGraph2 and conditional edges
- Must support recompilation when agents/tools change
- Must maintain type safety (no schema flattening)
- Must use existing Agent base features
- Must support Plan-and-Execute pattern

### 6. Next Steps

1. Design proper MetaAgentState schema
2. Rebuild MultiAgent to use it correctly
3. Ensure compilation kwargs pass through
4. Test with Plan-and-Execute pattern
5. Make it general, not specific

## Memory Checkpoint

This is where we are - the prebuilt schemas are incorrect for true multi-agent systems. They either:
- Only handle single agents (MetaStateSchema)
- Use flawed schema composition (MultiAgentStateSchema)  
- Don't contain agents (MetaAgentState)

We need to rebuild these properly.