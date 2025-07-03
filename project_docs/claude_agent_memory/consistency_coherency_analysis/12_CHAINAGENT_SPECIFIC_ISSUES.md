# ChainAgent Specific Issues - Detailed Analysis

## Current ChainAgent Problems

### 1. **No Schema Composition at All**

**Location**: `packages/haive-agents/src/haive/agents/chain/chain_agent_simple.py`

**Current Implementation**:

```python
def build_graph(self) -> BaseGraph:
    """Build the graph from nodes and edges."""
    graph = BaseGraph(name=self.name.replace(" ", ""))

    # Just adds nodes to graph - NO SCHEMA COMPOSITION
    for i, node in enumerate(self.nodes):
        node_name = f"node_{i}"
        # ... add node logic

    # NO schema coordination between nodes
    # NO field mapping
    # NO state management
```

**What's Missing**:

- No use of SchemaComposer or AgentSchemaComposer
- No state schema generation from nodes
- No field mapping between chain steps
- No tool_call_id preservation

### 2. **Wrong Abstraction Level - Uses Engines Not Agents**

```python
# ChainAgent operates at ENGINE level:
nodes: List[NodeLike] = Field(default_factory=list)
# NodeLike = Union[Agent, Engine, Callable, NodeConfig]

# Example usage:
ChainAgent(
    AugLLMConfig(...),  # Engine config
    AugLLMConfig(...),  # Engine config
    edges=["0->1"]
)
```

**Problems**:

- Should chain Agents, not Engines
- Engines don't have state management
- Can't use AgentSchemaComposer with engines
- Loses all agent-level capabilities

### 3. **Manual Data Passing Instead of Schema-Based**

```python
# Current approach - manual state passing:
def _add_edge_to_graph(self, graph, edge, node_names):
    # Manual edge creation
    # No schema awareness
    # No field mapping
    # No validation
```

**Should be**:

```python
# Schema-aware approach:
def build_graph(self) -> BaseGraph:
    # Use AgentSchemaComposer to coordinate agent schemas
    self.state_schema = AgentSchemaComposer.from_agents(
        agents=self.agents,  # NOT engines!
        separation="sequence",
        build_mode=BuildMode.SEQUENCE
    )
```

### 4. **No Message Preservation**

**Critical Issue**: ChainAgent loses tool_call_id between chain steps

**Current**: No preserve_messages_reducer
**Needed**: Message preservation like MultiAgent has

### 5. **No Compatibility with Agent Ecosystem**

```python
# Can't do this with current ChainAgent:
chain = ChainAgent([
    SimpleAgent(engine=llm1),
    ReactAgent(engine=llm2, tools=[...]),
    SimpleAgent(engine=llm3)
])

# Because it expects engines, not agents
```

## What ChainAgent Should Look Like

### Fixed ChainAgent Design

```python
class ChainAgent(Agent):  # or extends MultiAgentBase
    """Sequential agent execution with proper schema composition"""

    agents: list[Agent] = Field(...)  # Agents, not engines!

    def __init__(self, agents: list[Agent], **kwargs):
        # Use AgentSchemaComposer for proper schema handling
        self.state_schema = AgentSchemaComposer.from_agents(
            agents=agents,
            separation="sequence",  # Sequential field handling
            build_mode=BuildMode.SEQUENCE,
            include_meta=True  # For chain coordination
        )

        super().__init__(agents=agents, **kwargs)

    def build_graph(self) -> BaseGraph:
        graph = BaseGraph(name=self.name)

        # Add agents with schema-aware nodes
        prev_node = None
        for i, agent in enumerate(self.agents):
            node_name = f"agent_{i}"

            # Create schema-aware node function
            def create_agent_node(agent_instance):
                def agent_node(state):
                    # Extract fields for this agent using schema mappings
                    agent_input = self._extract_agent_input(state, agent_instance)
                    # Execute agent
                    result = agent_instance.invoke(agent_input)
                    # Update state with result using schema mappings
                    return self._update_state_with_result(state, result, agent_instance)
                return agent_node

            graph.add_node(node_name, create_agent_node(agent))

            # Connect in sequence
            if prev_node:
                graph.add_edge(prev_node, node_name)
            else:
                graph.add_edge(START, node_name)

            prev_node = node_name

        # Connect to end
        if prev_node:
            graph.add_edge(prev_node, END)

        return graph
```

## Migration Strategy for ChainAgent

### Phase 1: Create Fixed ChainAgent Class

```python
# New implementation alongside old one
class SequentialAgent(MultiAgentBase):  # Temporary name
    """Proper sequential agent execution"""
    execution_pattern = "sequential"

    def __init__(self, agents: list[Agent], **kwargs):
        # Use AgentSchemaComposer properly
        super().__init__(agents=agents, **kwargs)
```

### Phase 2: Deprecate Old ChainAgent

```python
# Add deprecation warning to old ChainAgent
class ChainAgent(Agent):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "ChainAgent is deprecated. Use SequentialAgent instead.",
            DeprecationWarning
        )
        # ... old implementation
```

### Phase 3: Migrate Usage

```python
# Old usage (broken):
chain = ChainAgent(
    engine1, engine2, engine3,
    edges=["0->1", "1->2"]
)

# New usage (working):
chain = SequentialAgent([
    SimpleAgent(engine=engine1),
    SimpleAgent(engine=engine2),
    SimpleAgent(engine=engine3)
])
```

## Immediate Fix Options

### Option 1: Quick Fix - Add Schema Composition to Current ChainAgent

```python
# Minimal changes to existing ChainAgent
class ChainAgent(Agent):
    def __init__(self, *nodes, **kwargs):
        # Convert engines to agents
        self.agents = []
        for node in nodes:
            if isinstance(node, Engine):
                # Wrap engine in SimpleAgent
                agent = SimpleAgent(engine=node)
                self.agents.append(agent)
            elif isinstance(node, Agent):
                self.agents.append(node)

        # Add schema composition
        if self.agents:
            self.state_schema = AgentSchemaComposer.from_agents(
                agents=self.agents,
                separation="sequence"
            )

        super().__init__(**kwargs)
```

### Option 2: Create New SequentialAgent

```python
# Clean implementation from scratch
class SequentialAgent(MultiAgentBase):
    """Sequential agent execution with proper schema composition"""
    # Use all MultiAgent infrastructure
    # Add sequential execution pattern
```

### Option 3: Fix Current ChainAgent in Place

```python
# Rewrite current ChainAgent to use proper patterns
# Risk: might break existing usage
# Benefit: fixes the problem immediately
```

## Recommendation

**Start with Option 2 (New SequentialAgent)**:

1. Create SequentialAgent with proper schema composition
2. Use MultiAgent infrastructure
3. Test thoroughly with real use cases
4. Once proven, deprecate old ChainAgent
5. Provide migration guide

This approach:

- Fixes the schema composition problem immediately
- Doesn't break existing code
- Provides upgrade path
- Uses proven MultiAgent patterns
- Maintains backward compatibility

## Testing Requirements

### Must Test

1. **Schema composition** - fields flow correctly between agents
2. **Tool_call_id preservation** - tools work across chain steps
3. **Message handling** - conversation state maintained
4. **Error handling** - failures don't break the chain
5. **Performance** - reasonable overhead for schema composition

### Test Cases

```python
# Basic sequential execution
chain = SequentialAgent([
    SimpleAgent(engine=llm1),
    SimpleAgent(engine=llm2)
])

# Mixed agent types
chain = SequentialAgent([
    RetrieverAgent(engine=retriever),
    SimpleAgent(engine=llm),
    ProcessorAgent(engine=processor)
])

# Tool usage across chain
chain = SequentialAgent([
    ReactAgent(engine=llm, tools=[search_tool]),
    SimpleAgent(engine=llm)  # Should see tool results
])
```

This detailed analysis shows that ChainAgent's issues are fundamental architectural problems that require proper schema composition to fix.
