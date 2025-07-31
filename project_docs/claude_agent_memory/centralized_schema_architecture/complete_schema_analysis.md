# Complete Agent Schema Composition Analysis - Claude Discovery Agent

**Date**: 2025-06-28
**Focus**: Understanding schema handling patterns across all agent types

## Summary of Agent Schema Issues

### 1. SimpleAgent (Engine Schema Modification - DANGEROUS)

```python
# Lines 232-281 in simple/agent.py
def _modify_engine_schema(self) -> None:
    """MODIFY the engine's output schema to include structured output fields."""

    # Get the engine's current output schema
    current_output_schema = self.engine.derive_output_schema()

    # Create a new schema composer to build enhanced schema
    composer = SchemaComposer(name=f"Enhanced{current_output_schema.__name__}")

    # Add existing fields from current schema
    composer.add_fields_from_model(current_output_schema)

    # Add the structured output field
    composer.add_field(
        name=field_name,
        field_type=Optional[self.structured_output_model],
        default=None,
        description=f"Structured output of type {self.structured_output_model.__name__}",
    )

    # Build the enhanced schema
    enhanced_schema = composer.build()

    # OVERRIDE the engine's output schema
    self.engine.output_schema = enhanced_schema  # <-- DANGEROUS!
```

**Problems**:

- Directly modifies engine schemas (dangerous side effects)
- Uses basic SchemaComposer (not AgentSchemaComposer)
- No message preservation logic
- Could affect other agents using same engine

### 2. ChainAgent (NO SCHEMA HANDLING)

```python
# Line 55-103 in chain/chain_agent_simple.py
def build_graph(self) -> BaseGraph:
    """Build the graph from nodes and edges."""
    graph = BaseGraph(name=self.name.replace(" ", ""))

    # Add nodes
    for i, node in enumerate(self.nodes):
        node_name = f"node_{i}"
        # Just adds nodes to graph
        # NO SCHEMA COMPOSITION
        # NO STATE MANAGEMENT
        # NO MESSAGE PRESERVATION
```

**Problems**:

- NO schema handling at all
- Just passes nodes through without coordination
- No state management between nodes
- No message preservation (tool_call_id loss risk)

### 3. MultiAgent (SOPHISTICATED SCHEMA HANDLING)

```python
# From multi/base.py (line analysis based on previous reading)
self.state_schema = AgentSchemaComposer.from_agents(
    agents=list(self.agents),
    name=f"{self.__class__.__name__}State",
    include_meta=self.include_meta,
    separation=self.schema_separation,  # "smart", "shared", "namespaced"
    build_mode=build_mode,
)
```

**Features**:

- Uses AgentSchemaComposer (sophisticated)
- Has separation strategies for field management
- Preserves message reducers (tool_call_id preservation)
- Tracks private states per agent
- Maps execution modes to build modes

### 4. BaseAgent (FLEXIBLE SCHEMA SYSTEM)

```python
# Lines 578-640 in base/agent.py
def _setup_schemas(self) -> None:
    """Generate schemas from available engines with intelligent defaults."""

    if agent_list:
        # Use AgentSchemaComposer for agents
        self.state_schema = AgentSchemaComposer.from_agents(
            agents=agent_list,
            name=f"{self.__class__.__name__}State",
            include_meta=True,
            separation="smart",
        )
    elif engine_list:
        # Use enhanced SchemaComposer for engines with tool routing
        if self.schema_config:
            # Use FlexibleSchemaComposer with config
            self.state_schema = FlexibleSchemaComposer.from_components_with_config(
                components=engine_list,
                name=f"{self.__class__.__name__}State",
                schema_config=schema_config
            )
        else:
            # Use basic SchemaComposer
            self.state_schema = SchemaComposer.from_components(
                components=engine_list,
                name=f"{self.__class__.__name__}State"
            )
```

**Features**:

- Uses AgentSchemaComposer for sub-agents
- Can use FlexibleSchemaComposer with configuration
- Falls back to basic SchemaComposer for engines
- Has automatic I/O schema derivation
- Intelligent tool routing support

### 5. RAG Agents (MIXED PATTERNS)

From rag/**init**.py - Multiple RAG agent variants:

- SimpleRAGAgent
- CorrectiveRAGAgentV2
- HyDERAGAgentV2
- MultiQueryRAGAgent
- AdaptiveRAGAgent
- And many more specialized ones

**BaseRAGAgent** (from rag/base/agent.py):

```python
class BaseRAGAgent(RetrieverMixin, Agent):
    """Base RAG agent that performs retrieval."""

    name: str = "Base RAG Agent"
    engine: BaseRetrieverConfig | VectorStoreConfig = Field(...)

    def build_graph(self) -> BaseGraph:
        # Simple linear graph: START -> retrieval_node -> END
        # No complex schema handling
```

**Problems with RAG Agents**:

- Each variant does its own schema handling
- No consistent pattern across RAG types
- Mix of different inheritance patterns
- No unified message preservation strategy

## Core Problems Identified

### 1. **Inconsistent Schema Composition Patterns**

- **SimpleAgent**: Modifies engine schemas directly (dangerous)
- **ChainAgent**: No schema handling at all
- **MultiAgent**: Sophisticated AgentSchemaComposer
- **BaseAgent**: Flexible system with multiple composers
- **RAG Agents**: Each does its own thing

### 2. **Message Preservation Issues**

- **MultiAgent**: Has preserve_messages_reducer
- **ChainAgent**: NO message preservation
- **SimpleAgent**: No message preservation logic
- **Others**: Unclear/inconsistent

### 3. **Tool Coordination Problems**

- **SimpleAgent**: Tool routing in engine
- **ChainAgent**: No tool coordination
- **MultiAgent**: Engine isolation prevents tool contamination
- **BaseAgent**: Tool synchronization support

### 4. **Field Separation Strategies**

- **MultiAgent**: "smart", "shared", "namespaced" separation
- **Others**: No separation strategy

## What Needs Fixing

### Priority 1: Critical Issues

1. **ChainAgent needs basic schema handling** - Currently broken
2. **SimpleAgent must stop modifying engine schemas** - Dangerous pattern
3. **Standardize message preservation** - Use preserve_messages_reducer everywhere

### Priority 2: Consistency Issues

4. **Unified schema composition pattern** across all agent types
5. **Clear guidelines** on when to use which composer
6. **Tool coordination standards** for all agents

### Priority 3: Advanced Features

7. **Field separation strategies** for all multi-component agents
8. **Schema compatibility checking** between agents
9. **Runtime schema modification** support

## Recommended Architecture

### Standard Schema Composition Pattern

```python
# For agents with sub-agents
if has_sub_agents:
    self.state_schema = AgentSchemaComposer.from_agents(
        agents=sub_agents,
        name=f"{self.__class__.__name__}State",
        include_meta=True,
        separation="smart"  # Default to smart separation
    )

# For agents with engines only
elif has_engines:
    if self.schema_config:
        # Use flexible composer with config
        self.state_schema = FlexibleSchemaComposer.from_components_with_config(
            components=engines,
            name=f"{self.__class__.__name__}State",
            schema_config=self.schema_config
        )
    else:
        # Use basic composer
        self.state_schema = SchemaComposer.from_components(
            components=engines,
            name=f"{self.__class__.__name__}State"
        )

# Always add message preservation
if not has_preserve_messages_reducer:
    add_preserve_messages_reducer_to_schema()
```

### Message Preservation Standard

All agents should include preserve_messages_reducer to maintain tool_call_id and other critical fields.

### Engine Schema Safety

- NO agent should modify engine schemas directly
- Use schema composition instead of schema modification
- Engine schemas are immutable from agent perspective

## Key Files Analyzed

1. **SimpleAgent**: `packages/haive-agents/src/haive/agents/simple/agent.py`
   - Lines 232-281: Dangerous engine schema modification
   - Lines 155-179: Setup logic that calls the modification

2. **ChainAgent**: `packages/haive-agents/src/haive/agents/chain/chain_agent_simple.py`
   - Lines 55-103: build_graph with no schema handling
   - Line 26: Inherits from Agent but doesn't implement schema logic

3. **MultiAgent**: `packages/haive-agents/src/haive/agents/multi/base.py`
   - Uses sophisticated AgentSchemaComposer
   - Has proper message preservation and field separation

4. **BaseAgent**: `packages/haive-agents/src/haive/agents/base/agent.py`
   - Lines 578-640: Flexible schema setup system
   - Lines 670-875: Automatic I/O schema derivation

5. **RAG Agents**: Multiple files in `packages/haive-agents/src/haive/agents/rag/`
   - BaseRAGAgent: Simple retrieval-only graph
   - Multiple specialized variants with inconsistent patterns

## No Generic Agent Found

- Searched for generic agent but no files found
- May have been removed or renamed
- Generic patterns seem to be handled by BaseAgent's flexibility

## Conclusion

The agent system has a fundamental schema composition inconsistency that needs to be resolved:

1. **ChainAgent is broken** - needs immediate schema handling
2. **SimpleAgent is dangerous** - needs to stop modifying engine schemas
3. **MultiAgent is the gold standard** - should be the pattern to follow
4. **BaseAgent provides the flexibility** - but needs consistent application
5. **RAG agents need unification** - too many inconsistent patterns

The recommendation is to standardize on the MultiAgent approach with AgentSchemaComposer and preserve_messages_reducer for all multi-component agents.
