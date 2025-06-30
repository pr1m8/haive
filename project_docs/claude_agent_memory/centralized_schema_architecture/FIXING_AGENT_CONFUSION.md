# Fixing Agent Confusion - Implementation Guide

**Date**: 2025-06-28  
**Focus**: Concrete steps to fix the agent/component confusion in Haive

## The Core Problems

### **1. ChainAgent - No Schema Handling**
```python
# Current: No schema composition at all
class ChainAgent(Agent):
    def build_graph(self) -> BaseGraph:
        # Just adds nodes to graph
        # NO SCHEMA COMPOSITION
        # NO STATE MANAGEMENT
```

### **2. SimpleAgent - Dangerous Schema Modification**
```python
# Current: Modifies engine schemas directly
def _modify_engine_schema(self) -> None:
    # OVERRIDE the engine's output schema
    self.engine.output_schema = enhanced_schema  # DANGEROUS!
```

### **3. Everything Treated as Agent**
```python
# Current: Retriever alone becomes "agent"
SimpleAgent(engine=retriever_engine)  # No reasoning capability!
```

## Quick Fixes (Minimal Breaking Changes)

### **Fix 1: Add Schema Handling to ChainAgent**
```python
class ChainAgent(Agent):
    def setup_agent(self):
        """Add missing schema setup."""
        # Collect actual agents from nodes
        agent_nodes = []
        component_nodes = []
        
        for i, node in enumerate(self.nodes):
            if isinstance(node, Agent):
                agent_nodes.append(node)
                # Add to engines for schema composition
                self.engines[f"agent_{i}"] = node.engine if hasattr(node, 'engine') else None
            else:
                component_nodes.append(node)
        
        # Let base Agent._setup_schemas() handle it
        # It will use AgentSchemaComposer if agent_nodes exist
        super().setup_agent()
    
    def _setup_schemas(self):
        """Override to use sequential composition for chains."""
        if self.nodes:
            # Check if we have actual agents
            agents = [n for n in self.nodes if isinstance(n, Agent)]
            
            if agents:
                # Use AgentSchemaComposer for agent chains
                from haive.core.schema.agent_schema_composer import AgentSchemaComposer, BuildMode
                
                self.state_schema = AgentSchemaComposer.from_agents(
                    agents=agents,
                    name=f"{self.__class__.__name__}State",
                    separation="smart",
                    build_mode=BuildMode.SEQUENCE  # Chains are sequential
                )
            else:
                # Just components - use basic composer
                from haive.core.schema.schema_composer import SchemaComposer
                
                components = [n for n in self.nodes if hasattr(n, 'engine')]
                if components:
                    self.state_schema = SchemaComposer.from_components(
                        components=[n.engine for n in components if n.engine],
                        name=f"{self.__class__.__name__}State"
                    )
```

### **Fix 2: Stop SimpleAgent from Modifying Engine Schemas**
```python
class SimpleAgent(Agent):
    def _modify_engine_schema(self) -> None:
        """FIXED: Create local schema instead of modifying engine."""
        if not self.structured_output_model or not self.engine:
            return
        
        logger.info(f"Creating agent output schema with {self.structured_output_model.__name__}")
        
        # Get the engine's current output schema
        current_output_schema = self.engine.derive_output_schema()
        
        # Create a new schema composer
        composer = SchemaComposer(name=f"{self.name}OutputSchema")
        
        # Add existing fields
        composer.add_fields_from_model(current_output_schema)
        
        # Add structured output field
        field_name = self._get_output_field_name()
        composer.add_field(
            name=field_name,
            field_type=Optional[self.structured_output_model],
            default=None,
            description=f"Structured output of type {self.structured_output_model.__name__}",
        )
        
        # Set AGENT's output schema, not ENGINE's
        self.output_schema = composer.build()  # FIXED: Agent's schema, not engine's!
        
        logger.info(f"Agent output schema created with field '{field_name}'")
```

### **Fix 3: Add Agent Validation**
```python
class Agent(ABC):
    """Add validation that this is actually an agent."""
    
    @model_validator(mode='after')
    def validate_has_reasoning_capability(self):
        """Validate this is actually an agent with reasoning."""
        # Check engines for reasoning capability
        reasoning_engines = [
            e for e in self.engines.values()
            if e and hasattr(e, 'engine_type') and 
            e.engine_type in [EngineType.LLM, EngineType.AGENT]
        ]
        
        # Allow agents without engines if they're containers (Multi, Chain)
        is_container = isinstance(self, (MultiAgent, ChainAgent))
        
        if not reasoning_engines and not is_container:
            logger.warning(
                f"{self.__class__.__name__} has no reasoning engines. "
                f"Consider using a Component instead of Agent."
            )
        
        return self
```

### **Fix 4: Create Component Alternative**
```python
# Add new file: haive/core/graph/node/component_node.py
from haive.core.graph.node.base_config import NodeConfig

class ComponentNode(NodeConfig):
    """Node for simple components without agent complexity."""
    
    component: Any = Field(description="The component (retriever, embeddings, etc)")
    component_type: str = Field(default="generic")
    
    def __call__(self, state, config=None):
        """Execute component with simple logic."""
        # Extract input based on component type
        if hasattr(self.component, 'invoke'):
            # Get appropriate input from state
            input_data = self._extract_component_input(state)
            result = self.component.invoke(input_data, config)
            return self._wrap_component_result(result, state)
        else:
            raise ValueError(f"Component {self.component} is not invokable")
    
    def _extract_component_input(self, state):
        """Extract input based on component type."""
        if self.component_type == "retriever":
            return getattr(state, 'query', '')
        elif self.component_type == "embeddings":
            return getattr(state, 'text', '')
        else:
            return state
```

## Long-Term Fixes (More Comprehensive)

### **1. Separate Agent and Component Hierarchies**
```python
# haive/core/component/base.py
class Component(BaseModel):
    """Base for non-agent components."""
    name: str
    component_type: ComponentType
    
    def invoke(self, input_data, config=None):
        """Simple execution without agent complexity."""

# Clear separation
RetrieverComponent(Component)  # Not an agent
EmbeddingsComponent(Component)  # Not an agent
```

### **2. Factory Functions with Validation**
```python
def create_graph_node(thing: Any, name: str) -> NodeConfig:
    """Smart factory that creates appropriate node type."""
    
    # Check if it's an agent with reasoning
    if isinstance(thing, Agent):
        # Validate it's actually an agent
        reasoning_engines = [
            e for e in thing.engines.values()
            if e and e.engine_type in [EngineType.LLM, EngineType.AGENT]
        ]
        if reasoning_engines:
            return EngineNodeConfig(name=name, engine=thing)
        else:
            logger.warning(f"{thing.name} has no reasoning - treating as component")
            return ComponentNode(name=name, component=thing)
    
    # It's a component
    return ComponentNode(name=name, component=thing)
```

### **3. Update Documentation**
```python
class SimpleAgent(Agent):
    """Simple agent for single-LLM workflows.
    
    WARNING: This is for agents with reasoning capability (LLMs).
    For simple components like retrievers, use ComponentNode instead.
    
    Example:
        # RIGHT - LLM is an agent
        agent = SimpleAgent(engine=llm_engine)
        
        # WRONG - Retriever alone is not an agent
        # agent = SimpleAgent(engine=retriever_engine)  # Use ComponentNode!
    """
```

## Migration Strategy

### **Phase 1: Add Warnings (Non-Breaking)**
```python
# Add to SimpleAgent.__init__
if self.engine and self.engine.engine_type not in [EngineType.LLM, EngineType.AGENT]:
    logger.warning(
        f"SimpleAgent created with {self.engine.engine_type} engine. "
        f"Consider using ComponentNode for non-reasoning components."
    )
```

### **Phase 2: Fix Critical Issues**
1. Fix ChainAgent schema handling
2. Fix SimpleAgent schema modification
3. Add ComponentNode as alternative

### **Phase 3: Update Examples**
```python
# Old pattern (discouraged)
retriever_agent = SimpleAgent(engine=retriever)

# New pattern (recommended)
retriever_node = ComponentNode(component=retriever)
```

### **Phase 4: Gradual Enforcement**
```python
# Future: Make it an error
if self.engine.engine_type not in [EngineType.LLM, EngineType.AGENT]:
    raise ValueError(
        f"SimpleAgent requires reasoning engine, got {self.engine.engine_type}. "
        f"Use ComponentNode for non-reasoning components."
    )
```

## Summary

The fixes focus on:

1. **Adding schema handling** where it's missing (ChainAgent)
2. **Stopping dangerous practices** (SimpleAgent modifying engine schemas)
3. **Providing alternatives** (ComponentNode for non-agents)
4. **Adding validation** without breaking existing code
5. **Clear documentation** about what is/isn't an agent

These changes can be implemented incrementally without breaking existing code, while guiding users toward better patterns.