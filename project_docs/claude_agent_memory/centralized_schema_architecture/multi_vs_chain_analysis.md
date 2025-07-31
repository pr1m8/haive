# Multi vs Chain Agent Analysis - Claude Discovery Agent

**Date**: 2025-06-28
**Focus**: Comparing MultiAgent vs ChainAgent schema handling

## Critical Differences

### MultiAgent (Complex)

```python
# Uses AgentSchemaComposer with sophisticated handling
self.state_schema = AgentSchemaComposer.from_agents(
    agents=list(self.agents),
    name=f"{self.__class__.__name__}State",
    include_meta=self.include_meta,
    separation=self.schema_separation,  # "smart", "shared", "namespaced"
    build_mode=build_mode,
)
```

**Key Features**:

- Uses AgentSchemaComposer (not basic SchemaComposer)
- Has separation strategies for field management
- Preserves message reducers (tool_call_id preservation)
- Tracks private states per agent
- Maps execution modes to build modes
- Handles I/O schema setup based on execution pattern

### ChainAgent (Too Simple)

```python
# NO SCHEMA HANDLING AT ALL!
def build_graph(self) -> BaseGraph:
    # Just adds nodes to graph
    # No schema composition
    # No state management
    # No field coordination
```

**Major Problems**:

1. **NO SCHEMA SETUP** - Inherits from Agent but doesn't implement schema logic
2. **NO STATE MANAGEMENT** - Just passes nodes through
3. **NO FIELD COORDINATION** - Each node handles its own state
4. **NO MESSAGE PRESERVATION** - Could lose tool_call_id

## The Problem

ChainAgent is **too simple** - it completely ignores schema composition:

- Doesn't call `_setup_schemas()`
- Doesn't use SchemaComposer or AgentSchemaComposer
- No consideration for how data flows between nodes
- No message preservation strategy

MultiAgent is **properly complex** but ChainAgent doesn't even try to handle schemas.

## Other Agent Schema Problems

### SimpleAgent

- **MODIFIES ENGINE SCHEMAS DIRECTLY** (BAD!)
- Uses basic SchemaComposer
- No concept of shared fields or reducers

### RAG Agents

- No consistent schema extension pattern
- Each variant does its own thing
- No use of SchemaComposer

### ReAct Agents

- Multiple versions (v2, v3, etc.)
- Inconsistent schema handling between versions

### Generic Agent

- Over-engineered type system
- Doesn't integrate well with dynamic schema composition

## What Needs Fixing

1. **ChainAgent needs schema handling** - At minimum basic SchemaComposer
2. **SimpleAgent must stop modifying engine schemas**
3. **All agents need consistent schema extension pattern**
4. **Message preservation must be standard** (preserve_messages_reducer)
5. **Clear guidance on when to use which composer**
