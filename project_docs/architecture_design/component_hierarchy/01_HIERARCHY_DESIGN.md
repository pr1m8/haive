# Component-Agent Hierarchy Design

## Overview

Design for a Component-Agent hierarchy that provides clear separation between LLM reasoning agents and deterministic processing components, while maintaining backward compatibility.

## Design Goals

1. **Component as high-level abstraction** - Universal base for all executable units
2. **Agent as LLM specialization** - Component + reasoning capabilities
3. **Backward compatibility** - Existing Agent code continues to work
4. **Clear type distinction** - Easy to understand what each component does
5. **Gradual migration** - Optional upgrade path, not forced changes

## Proposed Hierarchy

```
GraphNode (base interface)
└── Component (high-level executable base)
    ├── Agent (LLM reasoning specialization)
    │   ├── SimpleAgent
    │   ├── ReactAgent
    │   ├── MultiAgent
    │   └── ChainAgent (fixed)
    ├── ProcessorComponent (deterministic processing)
    ├── RetrieverComponent (data retrieval)
    ├── LoaderComponent (data loading)
    └── WorkflowComponent (orchestration)
```

## Component Design

### Core Component Class

```python
class Component(GraphNode):
    """High-level base for all executable workflow units"""

    # Engine management
    engine: Engine | None = None
    engines: dict[str, Engine] = Field(default_factory=dict)
    component_type: EngineType = EngineType.COMPONENT

    # Schema and execution
    set_schema: bool = True
    timeout: float | None = None

    # Lifecycle hooks
    def setup_component_hook(self): pass
    def _setup_schemas(self): pass

    # Universal execution interface
    @abstractmethod
    def execute(self, input_data, context=None):
        pass
```

### Key Features

- **Engine management** - Handles single engine or multiple engines
- **Schema composition** - Automatic schema generation from engines
- **Lifecycle hooks** - Setup and teardown capabilities
- **Universal interface** - `execute()` method for all components
- **Type classification** - `component_type` for capability determination

## Agent Design

### Agent as Component Specialization

```python
class Agent(Component):
    """Component specialized for LLM reasoning"""

    # Override component type
    component_type: Literal[EngineType.AGENT] = EngineType.AGENT

    # Agent-specific features
    tools: list[BaseTool] = Field(default_factory=list)
    conversation_memory: bool = True
    max_iterations: int = 10

    # LLM validation
    @model_validator(mode="after")
    def validate_llm_requirement(self):
        if not self.has_llm_engine():
            raise ValueError("Agents require LLM engine for reasoning")

    # Agent-specific interface
    @abstractmethod
    def reason(self, problem, context=None):
        pass

    # Bridge to universal interface
    def execute(self, input_data, context=None):
        return self.reason(input_data, context)
```

### Key Agent Features

- **LLM requirement** - Validates presence of LLM engine
- **Tool capabilities** - Tool management and usage
- **Reasoning interface** - `reason()` method for LLM operations
- **Interface bridge** - `execute()` delegates to `reason()`
- **Enhanced schema** - Uses AgentSchemaComposer when appropriate

## Specialized Components

### ProcessorComponent

```python
class ProcessorComponent(Component):
    """Deterministic data processing"""
    component_type = EngineType.PROCESSOR

    batch_size: int | None = None
    preserve_metadata: bool = True

    @abstractmethod
    def process(self, data):
        pass

    def execute(self, input_data, context=None):
        return self.process(input_data)

    def batch_process(self, data_list):
        return [self.process(item) for item in data_list]
```

### RetrieverComponent

```python
class RetrieverComponent(Component):
    """Information retrieval operations"""
    component_type = EngineType.RETRIEVER

    top_k: int = 10
    similarity_threshold: float | None = None

    @abstractmethod
    def retrieve(self, query):
        pass

    def execute(self, input_data, context=None):
        query = input_data.get("query") if isinstance(input_data, dict) else input_data
        return self.retrieve(query)
```

## Migration Strategy

### Phase 1: Add Component Base (Additive)

- Create Component class alongside existing Agent
- No changes to existing Agent class
- Component provides new capabilities for those who want them

### Phase 2: Create Specialized Components (New Options)

- ProcessorComponent, RetrieverComponent, etc.
- These are additions, not replacements
- Existing "agents" can migrate gradually

### Phase 3: Optional Agent Migration

- Agent can optionally extend Component
- Maintains all existing functionality
- Adds Component capabilities
- Backward compatibility preserved

### Phase 4: Gradual Ecosystem Migration

- New components use Component base
- Existing agents continue working
- Mixed workflows supported
- Migration helpers provided

## Backward Compatibility Strategy

### Existing Code Unchanged

```python
# This continues to work exactly as before:
agent = SimpleAgent(name="test", engine=llm_config)
result = agent.invoke(input_data)

# Existing imports unchanged:
from haive.agents import SimpleAgent, ReactAgent
```

### New Capabilities Added

```python
# New universal interface (optional):
result = agent.execute(input_data)

# New component types (additions):
from haive.components import ProcessorComponent, RetrieverComponent

# Mixed workflows (new capability):
workflow = WorkflowComponent([
    RetrieverComponent(...),
    Agent(...),
    ProcessorComponent(...)
])
```

### Migration Helpers

```python
# Optional migration utilities
def migrate_agent_to_component(agent_class):
    """Convert agent class to use Component base"""
    # Helper for gradual migration

def create_component_from_agent(agent_instance):
    """Wrap existing agent as component"""
    # Compatibility wrapper
```

## Schema Composition Strategy

### Component-Level Schema (Basic)

```python
class Component:
    def _setup_schemas(self):
        if self.engines:
            self.state_schema = SchemaComposer.from_components(
                self.engines, name=f"{self.__class__.__name__}State"
            )
```

### Agent-Level Schema (Enhanced)

```python
class Agent(Component):
    def _setup_schemas(self):
        # Use AgentSchemaComposer for agent-specific features
        if self.has_sub_agents():
            self.state_schema = AgentSchemaComposer.from_agents(
                self.sub_agents, separation="smart"
            )
        else:
            super()._setup_schemas()
```

### Mixed Workflow Schema (Unified)

```python
def compose_mixed_schema(components):
    """Handle mixed component types in workflows"""
    agents = [c for c in components if isinstance(c, Agent)]
    processors = [c for c in components if isinstance(c, ProcessorComponent)]

    # Use appropriate composer for each type
    # Combine results intelligently
```

## Benefits

### 1. Clear Conceptual Model

- **Component** = "Can be executed in workflow"
- **Agent** = "Component that reasons with LLM"
- **ProcessorComponent** = "Component that processes data"
- **RetrieverComponent** = "Component that retrieves information"

### 2. Shared Infrastructure

All components get:

- Engine management
- Schema composition
- Graph compilation
- Execution lifecycle
- Performance optimization

### 3. Type-Specific Optimization

- Agents optimized for reasoning and tool usage
- Processors optimized for batch operations and throughput
- Retrievers optimized for search and filtering
- All while sharing common foundation

### 4. Flexible Composition

```python
# Can compose any component types:
workflow = SequentialWorkflow([
    LoaderComponent(source="docs/"),
    ProcessorComponent(transform="split"),
    RetrieverComponent(index="vector_db"),
    Agent(engine=llm, tools=[...]),
    ProcessorComponent(transform="format")
])
```

### 5. Gradual Evolution

- Existing code continues working
- New code can use better patterns
- Migration is optional and gradual
- No forced breaking changes

This design provides a clear upgrade path while maintaining full backward compatibility and enabling better architectural patterns for future development.
