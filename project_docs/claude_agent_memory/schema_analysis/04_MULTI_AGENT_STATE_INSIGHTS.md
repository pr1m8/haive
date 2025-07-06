# Multi-Agent State Schema Insights

**Memory Tag**: [MEM-101-D]  
**Parent**: [MEM-101] Schema Analysis  
**Related**: [MEM-101-A] State Schema, [MEM-101-B] Schema Composer, [MEM-102-C] Multi-Agent Patterns  
**Date**: 2025-01-06

## 🎯 Purpose

Deep understanding of MultiAgentStateSchema - the specialized schema that solves engine visibility and access issues in multi-agent architectures.

## 📊 Problem It Solves

### The Engine Access Issue

In multi-agent systems, engine nodes need to find engines by name:

```python
# EngineNodeConfig looks for engines in:
1. state.engines dictionary (if exists)
2. EngineRegistry (global registry)

# Problem: Regular StateSchema doesn't populate state.engines
# Result: Engine nodes can't find engines from sub-agents
```

### The Solution

MultiAgentStateSchema automatically:

1. Creates an explicit `engines` field
2. Populates it with all available engines
3. Consolidates engines from sub-agents
4. Makes engines visible to all nodes

## 🔍 Key Implementation

### Core Structure

```python
class MultiAgentStateSchema(StateSchema):
    # Explicit engines field that nodes expect
    engines: Dict[str, Any] = Field(
        default_factory=dict,
        description="Dictionary of engines accessible to nodes"
    )

    @model_validator(mode="after")
    def populate_engines_dict(self):
        """Auto-populate engines from all sources"""
        # 1. Instance field engines
        # 2. Class-level engines
        # 3. Sub-agent engines
        # 4. Qualified names for collision avoidance
```

### Engine Collection Process

```python
# 1. Collect from instance fields
field_engines = self.get_engines()  # From StateSchema

# 2. Collect from class-level
class_engines = self.__class__.get_all_class_engines()

# 3. Collect from sub-agents
if hasattr(self, "agents"):
    for agent_name, agent in self.agents.items():
        # Add agent itself
        self.engines[agent.name] = agent

        # Add agent's engines with qualified names
        for eng_name, engine in agent.engines.items():
            # Both qualified and unqualified names
            self.engines[f"{agent_name}.{eng_name}"] = engine
            self.engines[eng_name] = engine  # If not taken
```

## 💡 Usage Patterns

### 1. Multi-Agent Coordinator

```python
class CoordinatorState(MultiAgentStateSchema):
    # Sub-agents field
    agents: Dict[str, Agent] = Field(default_factory=dict)

    # Shared conversation state
    messages: List[BaseMessage] = Field(default_factory=list)

    # Coordinator metadata
    current_agent: Optional[str] = None
    agent_history: List[str] = Field(default_factory=list)

# Engines automatically collected from all agents
# Accessible via state.engines["agent_name.engine_name"]
```

### 2. Converting Existing Schema

```python
# Convert any StateSchema to MultiAgent version
from haive.core.schema import MessagesState

MultiMessagesState = MultiAgentStateSchema.from_state_schema(
    MessagesState,
    name="MultiMessagesState"
)

# Now has automatic engine population
```

### 3. Building from Components

```python
# Use MultiAgentSchemaComposer
schema = MultiAgentSchemaComposer.from_components(
    components=[agent1, agent2, shared_engine],
    name="TeamState"
)

# Engines from all components available
```

## 🏗️ Real-World Example

### Agent Team Setup

```python
class ResearchTeamState(MultiAgentStateSchema):
    # Sub-agents
    agents: Dict[str, Agent] = Field(
        default_factory=lambda: {
            "researcher": ResearchAgent(),
            "analyzer": AnalysisAgent(),
            "writer": WriterAgent()
        }
    )

    # Shared state
    messages: List[BaseMessage] = []
    research_data: List[Dict] = []
    analysis_results: Dict[str, Any] = {}
    final_report: Optional[str] = None

# When instantiated:
state = ResearchTeamState()

# state.engines now contains:
# - "researcher": ResearchAgent instance
# - "researcher.llm": Research LLM engine
# - "researcher.retriever": Research retriever
# - "analyzer": AnalysisAgent instance
# - "analyzer.llm": Analysis LLM engine
# - etc...
```

### Engine Node Access

```python
# In a graph node
class AnalysisNode(EngineNodeConfig):
    engine_name = "analyzer.llm"  # Can find via state.engines

    def process(self, state):
        # Engine found automatically through state.engines
        engine = self._get_engine(state)
        result = engine.invoke(state.research_data)
        return {"analysis_results": result}
```

## 🐛 Common Issues & Solutions

### 1. Engine Name Collisions

**Problem**: Multiple agents have engine named "llm"  
**Solution**: Qualified names

```python
# Access via qualified name
state.engines["researcher.llm"]  # Specific
state.engines["llm"]  # Last one wins
```

### 2. Missing Engines

**Problem**: Engine not in state.engines  
**Solution**: Check collection order

```python
# Engines must be present when state created
# Not dynamically added later
```

### 3. Circular References

**Problem**: Agents reference each other  
**Solution**: Use lazy initialization

```python
agents: Dict[str, Agent] = Field(
    default_factory=dict  # Initialize empty
)

# Add agents after creation
state.agents["coordinator"] = coordinator
```

## 🎯 Best Practices

1. **Use for multi-agent systems**: Not needed for single agents
2. **Name engines uniquely**: Avoid collisions
3. **Use qualified names**: For specific engine access
4. **Initialize agents early**: Before state creation
5. **Document engine names**: For node configuration

## 🔄 Integration with Graphs

### Node Configuration

```python
# Nodes can reference engines by name
tool_node = ToolNodeConfig(
    engine_name="researcher.llm",  # Found in state.engines
    # Not needed: engine=engine_instance
)

validation_node = ValidationNodeConfig(
    engine_name="analyzer.llm"
)
```

### Dynamic Engine Selection

```python
def select_engine(state):
    """Choose engine based on task"""
    if state.task_type == "research":
        return state.engines["researcher.llm"]
    elif state.task_type == "analysis":
        return state.engines["analyzer.llm"]
    return state.engines["writer.llm"]
```

## 📊 Comparison with Regular StateSchema

| Feature            | StateSchema     | MultiAgentStateSchema |
| ------------------ | --------------- | --------------------- |
| engines field      | Optional/Manual | Automatic             |
| Engine population  | Manual          | Automatic             |
| Sub-agent support  | Manual          | Built-in              |
| Node compatibility | Requires setup  | Works out-of-box      |
| Use case           | Single agents   | Multi-agent teams     |

## 🚀 Advanced Patterns

### 1. Hierarchical Teams

```python
class DepartmentState(MultiAgentStateSchema):
    teams: Dict[str, MultiAgentStateSchema] = Field(
        default_factory=dict
    )

    # Engines collected from all levels
```

### 2. Dynamic Agent Addition

```python
def add_specialist(state, specialist_type):
    """Add specialist agent dynamically"""
    specialist = create_specialist(specialist_type)
    state.agents[specialist_type] = specialist
    # Note: engines dict not auto-updated after creation
```

### 3. Engine Routing

```python
def route_to_engine(state) -> str:
    """Route based on available engines"""
    if "researcher.llm" in state.engines:
        return "research_node"
    return "default_node"
```

## 🔗 Cross-References

- Base StateSchema: [MEM-101-A]
- Schema Composer: [MEM-101-B]
- Multi-agent patterns: [MEM-102-C]
- Engine registration: [MEM-104-A]

---

**Status**: Core insights documented
**Last Updated**: 2025-01-06
