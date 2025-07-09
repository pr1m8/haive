# State Schema and Field Syncing Analysis

## Current Confusion Points

### 1. Engine vs Engines in Base Agent
```python
class Agent:
    engine: Optional[Engine] = None  # Single engine?
    engines: Dict[str, Engine] = {}  # Multiple engines?
    
    # Which one to use when?
    # How do they sync to state?
    # Why both patterns?
```

### 2. Field Synchronization Confusion
- `_sync_fields_from_engine()` - What exactly does this sync?
- When do fields get added to state?
- How do engine fields map to state fields?
- What happens with multiple engines?

### 3. State Schema Composition
- When is the state schema created?
- How does SchemaComposer know what fields to include?
- What's the difference between:
  - Fields from engine.get_input_fields()
  - Fields from engine.get_output_fields()  
  - Fields defined on the state class itself
  - Fields added dynamically

### 4. Multi-Agent Makes it Worse
- Each agent has its own state schema
- But they need to share some fields
- How does field ownership work?
- When do fields sync between agents?

## The Real Problems

### Problem 1: No Clear Field Lifecycle
```
Where do fields come from?
1. Defined on StateSchema class? 
2. Added by engine.get_input_fields()?
3. Added by engine.get_output_fields()?
4. Synced from engine attributes?
5. Added by SchemaComposer?
6. Created at runtime?

When do they get added?
- At class definition?
- At agent initialization?
- When engine is set?
- When graph is built?
- At runtime?
```

### Problem 2: Unclear Sync Direction
```
Engine → State:
- engine.tools → state.tools?
- engine.temperature → state.temperature?
- Which fields sync and which don't?

State → Engine:
- Does state ever update engine?
- What about runnable_config?
```

### Problem 3: Multi-Engine Ambiguity
```python
# If agent has multiple engines:
engines = {
    "llm": llm_engine,
    "retriever": retriever_engine
}

# Which engine's fields take precedence?
# How do field names avoid conflicts?
# Who owns the "messages" field?
```

## Current Code Patterns

### Pattern 1: Simple Agent
```python
class SimpleAgent(Agent):
    def __init__(self, engine: Engine):
        self.engine = engine
        # Magic happens - fields appear on state somehow
```

### Pattern 2: Multi-Engine Agent (RAG)
```python
class RAGAgent(Agent):
    def __init__(self):
        self.engines = {
            "llm": llm_engine,
            "retriever": retriever_engine
        }
        # Even more magic - how do these compose?
```

### Pattern 3: Multi-Agent
```python
class SequentialAgent(MultiAgent):
    def __init__(self, agents: List[Agent]):
        self.agents = agents
        # State explosion - all agent fields merged?
```

## What We Really Need

### 1. Clear Field Ownership Model
```python
@dataclass
class FieldSource:
    source_type: Literal["state_class", "engine", "dynamic", "shared"]
    source_name: str  # e.g., "llm_engine", "StateSchema", "parent"
    field_name: str
    field_def: FieldDefinition
    access: Literal["read", "write", "read_write"]
```

### 2. Explicit Sync Rules
```python
class SyncRule:
    """Defines how a field syncs between engine and state."""
    engine_attr: str  # Attribute on engine
    state_field: str  # Field in state
    direction: Literal["engine_to_state", "state_to_engine", "bidirectional"]
    when: Literal["on_init", "on_engine_set", "on_access", "never"]
```

### 3. Clear State Composition
```python
class StateComposition:
    """Tracks how state is composed."""
    base_schema: Type[BaseModel]  # Starting schema
    engine_fields: Dict[str, List[FieldDefinition]]  # Per engine
    dynamic_fields: List[FieldDefinition]  # Added at runtime
    shared_fields: List[str]  # From parent/shared context
    
    def build_schema(self) -> Type[BaseModel]:
        """Build final schema with clear precedence rules."""
        pass
```

## Proposed Simplification

### Option 1: Explicit Field Declaration
```python
class SimpleAgent(Agent):
    # Declare what fields this agent needs
    required_fields = ["messages", "context"]
    
    # Declare what fields this agent provides  
    provided_fields = ["response", "reasoning"]
    
    # Declare engine field mappings
    engine_mappings = {
        "tools": "engine.tools",  # state.tools = engine.tools
        "temperature": "engine.temperature"
    }
```

### Option 2: Schema-First Approach
```python
class SimpleAgentState(StateSchema):
    """Define state schema explicitly."""
    messages: List[BaseMessage]
    context: str
    tools: List[Any] = Field(sync_from="engine.tools")
    temperature: float = Field(sync_from="engine.temperature")

class SimpleAgent(Agent[SimpleAgentState]):
    """Agent knows its state type."""
    state_schema = SimpleAgentState
```

### Option 3: Builder Pattern
```python
agent = (AgentBuilder()
    .with_engine(llm_engine)
    .require_fields(["messages", "context"])
    .provide_fields(["response"])
    .sync_field("tools", from_engine="tools")
    .build())
```

## Next Steps

1. **Pick a Pattern**: Which approach is clearest?
2. **Define Sync Rules**: When and how do fields sync?
3. **Clarify Multi-Engine**: How do multiple engines compose?
4. **Document Lifecycle**: When does each step happen?
5. **Simplify Multi-Agent**: How to avoid field explosion?