# Component-Agent Hierarchy Design Notes

## Current Understanding

### Desired Hierarchy
```
Component (high-level, abstract base)
└── Agent (extends Component, adds LLM reasoning)
    ├── SimpleAgent (single LLM)
    ├── ReactAgent (LLM + tools + reasoning loop)
    ├── MultiAgent (coordinated LLMs)
    └── ChainAgent (sequential agents)
```

### Component as Foundation
- **Component** should be the broader, more abstract concept
- All executable units are "Components" 
- **Agent** is a specialized Component that adds LLM reasoning
- This allows for non-LLM components that still follow the same patterns

## Key Design Principles

### 1. Component = Universal Executable Unit
```python
class Component(GraphNode):
    """Abstract base for all executable units"""
    
    # Common functionality:
    - Engine management (engine, engines dict)
    - Schema composition and generation
    - Graph building and compilation  
    - Execution lifecycle (setup hooks, etc.)
    - Performance settings (timeout, batching)
    
    @abstractmethod
    def execute(self, input_data, context=None):
        """Universal execution interface"""
        pass
```

### 2. Agent = Component + LLM Reasoning
```python
class Agent(Component):
    """Component specialized for LLM reasoning"""
    
    # Inherits all Component functionality, adds:
    - LLM engine requirement/validation
    - Tool usage capabilities
    - Reasoning methods (reason, areason)
    - Conversation memory
    - Agent-specific schema composition (AgentSchemaComposer)
    
    def execute(self, input_data, context=None):
        """Delegates to reason() for agents"""
        return self.reason(input_data, context)
    
    @abstractmethod  
    def reason(self, problem, context=None):
        """Agent-specific reasoning interface"""
        pass
```

### 3. Specialized Components (Non-LLM)
```python
class ProcessorComponent(Component):
    """Component for deterministic processing"""
    component_type = EngineType.PROCESSOR
    
    def execute(self, input_data, context=None):
        return self.process(input_data)
    
    @abstractmethod
    def process(self, data):
        """Processing-specific interface"""
        pass

class RetrieverComponent(Component):
    """Component for information retrieval"""
    component_type = EngineType.RETRIEVER
    
    def execute(self, input_data, context=None):
        return self.retrieve(input_data.get("query"))
    
    @abstractmethod
    def retrieve(self, query):
        """Retrieval-specific interface"""
        pass
```

## Benefits of This Approach

### 1. **Clear Conceptual Model**
- Component = "Anything that can be executed"
- Agent = "Component that reasons with LLM"
- RetrieverComponent = "Component that retrieves data"
- ProcessorComponent = "Component that processes data"

### 2. **Shared Infrastructure**
All components get:
- Engine management
- Schema composition
- Graph compilation
- Execution lifecycle
- Performance optimization

### 3. **Type-Specific Specialization**
- Agents get reasoning capabilities
- Processors get batch processing optimization
- Retrievers get search/filter capabilities
- All while sharing the same foundation

### 4. **Composition Flexibility**
```python
# Can compose any components together:
workflow = WorkflowComponent([
    RetrieverComponent(...),  # Get data
    Agent(...),              # Reason about it
    ProcessorComponent(...)   # Transform result
])
```

## Implementation Strategy

### Phase 1: Create Component Base
1. Component class with universal execution interface
2. Engine management and schema composition
3. Common lifecycle hooks and performance settings

### Phase 2: Migrate Agent to Extend Component
1. Agent inherits from Component
2. Adds LLM requirements and reasoning capabilities
3. Maintains backward compatibility with existing agents

### Phase 3: Create Specialized Component Types
1. ProcessorComponent for deterministic processing
2. RetrieverComponent for data retrieval
3. LoaderComponent for data loading

### Phase 4: Migrate Misclassified "Agents"
1. BaseRAGAgent → RetrieverComponent
2. DocumentAgent → ProcessorComponent
3. LoaderAgent → LoaderComponent

## Schema Composition Strategy

### Component-Level Schema Composition
```python
class Component:
    def _setup_schemas(self):
        # Basic schema composition for all components
        if self.engines:
            self.state_schema = SchemaComposer.from_components(
                self.engines, name=f"{self.__class__.__name__}State"
            )
```

### Agent-Level Schema Enhancement
```python
class Agent(Component):
    def _setup_schemas(self):
        # Use AgentSchemaComposer for agents
        if self.has_sub_agents():
            self.state_schema = AgentSchemaComposer.from_agents(
                self.sub_agents, separation="smart"
            )
        else:
            super()._setup_schemas()  # Use Component's method
```

## Backward Compatibility

### Existing Code Continues to Work
```python
# This still works:
agent = SimpleAgent(name="my_agent", engine=llm_config)
result = agent.invoke(input_data)

# But now also works:
result = agent.execute(input_data)  # Universal interface
```

### Gradual Migration Path
1. Component base provides all current Agent functionality
2. Agent extends Component with reasoning-specific features
3. Existing agents inherit enhanced capabilities automatically
4. New component types can be added without breaking existing code

## Questions to Resolve

1. **Method naming**: Should Agent have both `execute()` and `reason()`, or just `reason()`?
2. **Schema composition**: How to handle mixed component types in workflows?
3. **Type checking**: Should we validate component types at composition time?
4. **Performance**: Any performance implications of the deeper inheritance?

## Next Steps

1. Design the Component base class interface
2. Plan the Agent migration strategy
3. Identify which current "agents" should become other component types
4. Create migration plan that maintains backward compatibility