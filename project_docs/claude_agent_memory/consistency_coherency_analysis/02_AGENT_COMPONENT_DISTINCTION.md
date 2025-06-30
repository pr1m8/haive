# Agent vs Component Distinction Crisis

## Current Problem: Everything is an "Agent"

### Misclassified Components
**Problem**: Components that don't need LLM reasoning inherit from Agent base class

```python
# WRONG: Retriever doesn't need Agent complexity
class BaseRAGAgent(RetrieverMixin, Agent):
    """This is actually a RETRIEVER COMPONENT, not an Agent"""
    
# WRONG: Document loader isn't an agent
class DocumentLoaderAgent(Agent):
    """This is a LOADER COMPONENT, not an Agent"""

# WRONG: Callable wrapper doesn't need agent features  
class CallableAgent(Agent):
    """This is a CALLABLE COMPONENT, not an Agent"""
```

### Engine Type Confusion
**Current**: Everything uses `engine_type: EngineType.AGENT`
```python
# ALL of these use the same engine type:
- LLM-based reasoning agent (CORRECT)
- Document retriever (WRONG - should be RETRIEVER)
- File loader (WRONG - should be LOADER) 
- Callable wrapper (WRONG - should be CALLABLE)
```

## Proposed Taxonomy

### True Agents (LLM-based reasoning)
```python
class Agent(BaseComponent):
    """Agents have LLM engines and reasoning capability"""
    engine_type: Literal[EngineType.AGENT] = EngineType.AGENT
    engine: LLMEngine | AugLLMConfig = Field(...)  # Must be LLM
    
    @abstractmethod
    def reason(self, input_data: Any) -> Any:
        """Agents must implement reasoning"""
```

**Examples**:
- SimpleAgent (single LLM reasoning)
- ReactAgent (reasoning + tool use)
- MultiAgent (coordinated reasoning)

### Deterministic Components
```python
class Component(BaseComponent):
    """Components are deterministic, no LLM needed"""
    engine_type: Literal[EngineType.COMPONENT] = EngineType.COMPONENT
    
    @abstractmethod  
    def process(self, input_data: Any) -> Any:
        """Components process data deterministically"""
```

**Component Types**:
```python
class RetrieverComponent(Component):
    engine_type: Literal[EngineType.RETRIEVER] = EngineType.RETRIEVER
    engine: BaseRetrieverConfig | VectorStoreConfig
    
class LoaderComponent(Component):
    engine_type: Literal[EngineType.LOADER] = EngineType.LOADER  
    engine: DocumentLoaderConfig
    
class CallableComponent(Component):
    engine_type: Literal[EngineType.CALLABLE] = EngineType.CALLABLE
    engine: CallableConfig
    
class ProcessorComponent(Component):
    engine_type: Literal[EngineType.PROCESSOR] = EngineType.PROCESSOR
    engine: ProcessorConfig
```

### Workflow Orchestrators
```python
class Workflow(BaseComponent):
    """Workflows orchestrate agents and components"""
    engine_type: Literal[EngineType.WORKFLOW] = EngineType.WORKFLOW
    
    components: list[Agent | Component] = Field(...)
    
    @abstractmethod
    def build_graph(self) -> BaseGraph:
        """Workflows define execution patterns"""
```

**Workflow Types**:
```python
class SequentialWorkflow(Workflow):
    """Execute components in sequence"""
    
class ParallelWorkflow(Workflow):  
    """Execute components in parallel with aggregation"""
    
class ConditionalWorkflow(Workflow):
    """Conditional branching between components"""
```

## Schema Composition by Type

### Agent Schema Composition
```python
# For true agents only
class AgentSchemaComposer:
    @classmethod
    def from_agents(cls, agents: list[Agent], **kwargs):
        """Compose schemas from LLM-based agents"""
        for agent in agents:
            if not isinstance(agent, Agent):
                raise TypeError(f"{agent} is not an Agent")
            if agent.engine_type != EngineType.AGENT:
                raise TypeError(f"{agent} doesn't have LLM capability")
```

### Component Schema Composition  
```python
# For deterministic components
class ComponentSchemaComposer:
    @classmethod
    def from_components(cls, components: list[Component], **kwargs):
        """Compose schemas from deterministic components"""
        for component in components:
            if isinstance(component, Agent):
                raise TypeError(f"Use AgentSchemaComposer for {component}")
```

### Unified Workflow Composition
```python
# For mixed agent/component workflows
class WorkflowSchemaComposer:
    @classmethod
    def from_mixed_components(cls, components: list[Agent | Component], **kwargs):
        """Handle mixed agent/component workflows"""
        agents = [c for c in components if isinstance(c, Agent)]
        comps = [c for c in components if isinstance(c, Component)]
        
        # Use appropriate composer for each type
        agent_schema = AgentSchemaComposer.from_agents(agents) if agents else None
        comp_schema = ComponentSchemaComposer.from_components(comps) if comps else None
        
        # Merge with workflow-specific logic
        return cls._merge_schemas(agent_schema, comp_schema, **kwargs)
```

## Migration Strategy

### Phase 1: Identify Misclassified Components
```python
# Audit current "agents" that should be components:
- BaseRAGAgent → RetrieverComponent
- DocumentLoaderAgent → LoaderComponent  
- CallableAgent → CallableComponent
- EmbeddingAgent → ProcessorComponent
```

### Phase 2: Create Component Base Classes
```python
# New hierarchy:
BaseComponent
├── Agent (LLM-based reasoning)
│   ├── SimpleAgent
│   ├── ReactAgent  
│   └── MultiAgent
├── Component (deterministic processing)
│   ├── RetrieverComponent
│   ├── LoaderComponent
│   ├── CallableComponent
│   └── ProcessorComponent
└── Workflow (orchestration)
    ├── SequentialWorkflow
    ├── ParallelWorkflow
    └── ConditionalWorkflow
```

### Phase 3: Update Engine Types
```python
class EngineType(Enum):
    AGENT = "agent"        # LLM-based reasoning
    RETRIEVER = "retriever" # Data retrieval  
    LOADER = "loader"      # Data loading
    CALLABLE = "callable"  # Function wrapping
    PROCESSOR = "processor" # Data transformation
    WORKFLOW = "workflow"  # Orchestration
```

### Phase 4: Migrate Existing Code
```python
# Before (WRONG):
class SimpleRAGAgent(SequentialAgent):
    retrieval_agent = BaseRAGAgent(...)  # Not an agent!
    answer_agent = SimpleAgent(...)      # This is an agent

# After (CORRECT):  
class SimpleRAGWorkflow(SequentialWorkflow):
    retrieval_component = RetrieverComponent(...)  # Component
    answer_agent = SimpleAgent(...)               # Agent
```

## Benefits of Clear Distinction

### 1. **Conceptual Clarity**
- Developers understand when to use agents vs components
- Clear functional boundaries reduce confusion
- Better alignment with actual capabilities

### 2. **Performance Optimization**
- Components can be optimized for deterministic processing
- Agents can focus on LLM reasoning efficiency
- Resource allocation matches component type

### 3. **Schema Composition Accuracy**
- AgentSchemaComposer only handles LLM-based reasoning
- ComponentSchemaComposer optimized for deterministic data flow
- No unnecessary agent complexity for simple components

### 4. **Tool Coordination**
- Only true agents need tool_call_id preservation
- Components have simpler input/output patterns
- Cleaner separation of concerns

This taxonomy resolves the current confusion and provides a clear framework for when to use each abstraction level.