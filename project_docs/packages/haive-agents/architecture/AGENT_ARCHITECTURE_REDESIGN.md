# Agent Architecture Analysis & Redesign Proposal

## Current State Analysis

### What We Have Now

#### BaseGraph (haive-core)

- **Purpose**: Workflow template/definition
- **Structure**: Pydantic model with nodes, edges, branches
- **Key Feature**: `to_langgraph()` method converts to executable LangGraph
- **Status**: ✅ Already well-designed and Pydantic-first

#### Agent (haive-agents)

- **Purpose**: Everything! (This is the problem)
- **Structure**: Massive Pydantic model inheriting from 5+ mixins
- **Responsibilities**:
  - Workflow execution
  - Engine management
  - Schema generation/inference
  - Persistence management
  - State management
  - Tool management
  - Serialization
  - Debugging/visualization

#### NodeConfig (haive-core)

- **Purpose**: Node specification with multiple resolution strategies
- **Complexity**: Can reference engines by direct object, name, or callable
- **Schema Integration**: Has own input/output schemas + field mappings
- **Status**: ⚠️ Complex but functional

### The Core Problems

1. **Agent is a God Class**: Trying to be workflow + engine + persistence + everything
2. **Schema Ownership Confusion**: Agent, NodeConfig, and engines all have schemas
3. **Engine Resolution Ambiguity**: Multiple ways to specify what runs in a node
4. **Mixed Abstractions**: Workflow concepts bleeding into execution concepts

## Research Findings

### Key Distinctions We Need

#### Workflow vs Agent vs Engine

- **Workflow (BaseGraph)**: "WHAT to do" - pure orchestration template
- **Engine**: "HOW to do it" - execution units (LLM, processor, retriever, etc.)
- **Agent**: "Workflow + Engines + Context" - executable instance

#### Template vs Runtime

- **Template**: Serializable, engine-agnostic workflow definition
- **Runtime**: Bound workflow with actual engine instances

#### Multi-Agent Clarification

- **Multi-Agent ≠ Special inheritance**
- **Multi-Agent = Agents as engines in a coordination workflow**

## Proposed Architecture

### Core Principles

1. **Pydantic-First**: No `__init__` methods, use Field definitions and validators
2. **Composition over Inheritance**: Build complex behavior from focused components
3. **Clear Separation**: Each class has one primary responsibility
4. **Engine Typing**: Strong typing for different engine categories

### Proposed Structure

#### 1. Workflow Layer (BaseGraph - Keep as-is)

```python
class BaseGraph(BaseModel):
    """Pure workflow template - already good!"""
    nodes: Dict[str, NodeConfig]
    edges: List[Edge]
    branches: Dict[str, Branch]

    def to_langgraph(self, **schemas) -> StateGraph
```

#### 2. Engine Layer (Improve typing)

```python
class Engine(BaseModel):
    name: str
    engine_type: EngineType

class LLMEngine(Engine):
    engine_type: Literal[EngineType.LLM] = EngineType.LLM
    model: str
    tools: List[Tool] = Field(default_factory=list)

class ProcessorEngine(Engine):
    engine_type: Literal[EngineType.PROCESSOR] = EngineType.PROCESSOR

class AgentEngine(Engine):
    engine_type: Literal[EngineType.AGENT] = EngineType.AGENT
    agent: "Agent"  # Reference for multi-agent
```

#### 3. Agent Layer (Minimal core)

```python
class Agent(BaseModel):
    """Minimal agent = workflow + engines + context"""
    workflow: BaseGraph
    engines: Dict[str, Engine]
    context: AgentContext = Field(default_factory=AgentContext)

    @computed_field
    @property
    def agent_type(self) -> AgentType:
        """Auto-detect from engines"""
        # LLM, RAG, PROCESSOR, MULTI_AGENT based on engine types

    def invoke(self, input_data: Any) -> Any:
        """Clean execution path"""
```

#### 4. Context Layer (Extract current bloat)

```python
class AgentContext(BaseModel):
    """All the complex setup stuff currently in Agent"""
    # Schema management
    state_schema: Optional[Type[BaseModel]] = None
    input_schema: Optional[Type[BaseModel]] = None
    output_schema: Optional[Type[BaseModel]] = None

    # Persistence
    persistence_config: Optional[PersistenceConfig] = None
    checkpointer: Any = Field(exclude=True)

    # Runtime
    verbose: bool = False
    debug: bool = False
    runnable_config: Optional[RunnableConfig] = None
```

### Node-Engine Relationship Options

#### Option A: Simple Reference (Recommended)

```python
class TemplateNodeConfig(BaseModel):
    """For workflow templates"""
    name: str
    engine_name: str  # Always reference by name
    input_mapping: Dict[str, str] = {}
    output_mapping: Dict[str, str] = {}

# At runtime, Agent resolves engine_name -> actual Engine
```

#### Option B: Keep Current Complexity

```python
class NodeConfig(BaseModel):
    """Current rich config with multiple resolution strategies"""
    engine: Engine | None = None
    engine_name: str | None = None
    callable_func: Callable | None = None
    # ... all current features
```

#### Option C: Template/Runtime Split

```python
class WorkflowTemplate(BaseModel):
    """Pure template"""
    nodes: Dict[str, TemplateNodeConfig]

class RuntimeWorkflow(BaseModel):
    """Bound with engines"""
    nodes: Dict[str, NodeConfig]
```

## Migration Strategy

### Phase 1: Foundation

1. **Improve Engine typing** with `LLMEngine`, `ProcessorEngine`, etc.
2. **Create AgentContext** to extract current Agent bloat
3. **Keep current Agent as LegacyAgent** for compatibility

### Phase 2: New Agent

1. **Create minimal Agent** = workflow + engines + context
2. **Create agent factories** for LLM, RAG, processor patterns
3. **Test with existing workflows**

### Phase 3: Gradual Migration

1. **Migrate SimpleAgent** to new architecture
2. **Migrate ReactAgent** to new architecture
3. **Migrate specialized agents** (RAG, document, etc.)

### Phase 4: Cleanup

1. **Deprecate LegacyAgent**
2. **Remove complex schema inference** (move to factories)
3. **Simplify inheritance hierarchy**

## Open Questions

### Critical Decisions Needed

1. **NodeConfig Complexity**: Keep rich current system or simplify to engine_name references?

2. **Schema Ownership**: Who owns state_schema - Agent, NodeConfig, or derived from engines?

3. **Engine Resolution Timing**: When does engine_name become actual Engine reference?

4. **Multi-Agent Pattern**: How should agent-as-engine work in practice?

5. **Backward Compatibility**: How much existing code can we break?

### Research Questions

1. **Performance Impact**: Does engine resolution at runtime vs creation-time matter?

2. **Serialization**: Do we need to serialize bound agents or just templates?

3. **Testing Strategy**: How to test new architecture without breaking existing tests?

4. **Documentation**: What examples do we need to show the new patterns?

## Next Steps

1. **Choose NodeConfig approach** (A, B, or C above)
2. **Prototype minimal Agent** with chosen approach
3. **Test with SimpleAgent conversion**
4. **Validate multi-agent scenarios**
5. **Create migration plan** for existing agents

## Benefits of This Approach

### Clarity

- **BaseGraph**: "I define workflow steps"
- **Engine**: "I execute specific tasks"
- **Agent**: "I combine workflow + engines"
- **AgentContext**: "I handle complex setup"

### Reusability

- Same workflow, different engines
- Same engine, different workflows
- Clear composition patterns

### Maintainability

- Focused responsibilities
- Easier testing
- Clear upgrade paths

### Performance

- No unnecessary overhead for simple agents
- Clear optimization boundaries
- Reduced complexity

---

**What aspects should we dive deeper into first?**
