# Unified Schema Composition Strategy

## Problem Statement

Currently, different agent types use different schema composition approaches, leading to:
- Inconsistent field handling across agent types
- No standard message preservation strategy  
- Different composers used without clear guidelines
- NodeConfig-Schema disconnection causing type safety loss

## Current Schema Composition Landscape

### MultiAgent (Gold Standard)
```python
# Uses AgentSchemaComposer with sophisticated features:
self.state_schema = AgentSchemaComposer.from_agents(
    agents=agent_list,
    separation="smart",  # Intelligent field conflict resolution
    build_mode=BuildMode.PARALLEL,
    include_meta=True,
    preserve_messages=True  # Critical for tool_call_id
)
```

### SimpleAgent (Problematic)
```python
# Directly modifies engine schemas - DANGEROUS:
def _modify_engine_schema(self):
    # Get engine's current schema
    current_schema = self.engine.derive_output_schema()
    
    # Modify it directly
    self.engine.output_schema = enhanced_schema  # BAD!
```

### ChainAgent (Broken)
```python
# No schema composition at all:
def build_graph(self):
    # Just adds nodes without any schema coordination
    # Manual data passing
    # No field mapping
```

### BaseAgent (Inconsistent)
```python
# Sometimes uses SchemaComposer, sometimes AgentSchemaComposer:
if agent_list:
    self.state_schema = AgentSchemaComposer.from_agents(agents)
elif engine_list:
    self.state_schema = SchemaComposer.from_components(engines)
```

## Unified Strategy Design

### 1. Clear Composer Selection Rules

#### Rule 1: Agent Composition
```python
# Use AgentSchemaComposer when:
# - Composing multiple agents
# - Need reasoning capability coordination
# - Require tool_call_id preservation
# - Want intelligent field separation

if any(isinstance(item, Agent) for item in items):
    return AgentSchemaComposer.from_agents(
        agents=[item for item in items if isinstance(item, Agent)],
        separation="smart",
        preserve_messages=True
    )
```

#### Rule 2: Component Composition  
```python
# Use ComponentSchemaComposer when:
# - Composing deterministic components
# - Need efficient data flow patterns
# - Want batch processing optimization

if all(isinstance(item, Component) and not isinstance(item, Agent) for item in items):
    return ComponentSchemaComposer.from_components(
        components=items,
        flow_pattern="pipeline"
    )
```

#### Rule 3: Mixed Composition
```python
# Use MixedSchemaComposer when:
# - Combining agents and components
# - Need different optimization strategies per type
# - Want unified state management

if has_mixed_types(items):
    return MixedSchemaComposer.from_mixed(
        items=items,
        agent_strategy="reasoning",
        component_strategy="pipeline"
    )
```

#### Rule 4: Engine Composition (Legacy)
```python
# Use SchemaComposer only when:
# - Dealing with raw engines (no agent wrapper)
# - Legacy compatibility required
# - Simple field merging sufficient

return SchemaComposer.from_components(
    components=engines,
    name=f"{class_name}State"
)
```

### 2. Standardized Message Preservation

#### Universal Message Preservation
```python
# ALL schema composers should include message preservation:
class UnifiedSchemaComposer:
    @classmethod
    def compose_with_preservation(cls, items, **kwargs):
        # Always include preserve_messages_reducer
        schema = cls._compose_schema(items, **kwargs)
        
        # Add message preservation if not already present
        if not has_preserve_messages_reducer(schema):
            add_preserve_messages_reducer(schema)
        
        return schema
```

#### Message Preservation Implementation
```python
def ensure_message_preservation(schema: StateSchema):
    """Ensure schema preserves tool_call_id and message integrity"""
    
    # Add preserve_messages_reducer if messages field exists
    if hasattr(schema, "messages"):
        if "__reducer_fields__" not in schema.__dict__:
            schema.__reducer_fields__ = {}
        
        schema.__reducer_fields__["messages"] = preserve_messages_reducer
    
    return schema
```

### 3. NodeConfig-Schema Integration

#### Schema-Aware NodeConfig
```python
class SchemaAwareNodeConfig:
    """NodeConfig that understands schema field mappings"""
    
    def __init__(self, node_name: str, state_schema: StateSchema):
        self.node_name = node_name
        self.state_schema = state_schema
        
        # Extract field mappings from schema
        self.input_fields = self._extract_input_fields()
        self.output_fields = self._extract_output_fields()
    
    def _extract_input_fields(self) -> list[str]:
        """Extract required input fields from schema mappings"""
        mappings = getattr(self.state_schema, "__engine_io_mappings__", {})
        node_mapping = mappings.get(self.node_name, {})
        return node_mapping.get("input_fields", [])
    
    def _extract_output_fields(self) -> list[str]:
        """Extract produced output fields from schema mappings"""
        mappings = getattr(self.state_schema, "__engine_io_mappings__", {})
        node_mapping = mappings.get(self.node_name, {})
        return node_mapping.get("output_fields", [])
```

#### Type-Safe Node Functions
```python
def create_type_safe_node(config: SchemaAwareNodeConfig, component):
    """Create node function with type safety from schema"""
    
    def type_safe_node(state: config.state_schema) -> dict:
        # Extract only required input fields
        input_data = {}
        for field in config.input_fields:
            if hasattr(state, field):
                input_data[field] = getattr(state, field)
        
        # Execute component
        result = component.execute(input_data)
        
        # Return only mapped output fields
        output_data = {}
        for field in config.output_fields:
            if field in result:
                output_data[field] = result[field]
        
        return output_data
    
    return type_safe_node
```

## Implementation Strategy

### Phase 1: Create Unified Composer Interface
```python
class UnifiedSchemaComposer:
    """Single interface for all schema composition needs"""
    
    @classmethod
    def compose(cls, items: list, **kwargs) -> StateSchema:
        """Automatically select and apply appropriate composition strategy"""
        
        # Analyze item types
        agents = [item for item in items if isinstance(item, Agent)]
        components = [item for item in items if isinstance(item, Component) and not isinstance(item, Agent)]
        engines = [item for item in items if isinstance(item, Engine)]
        
        # Select appropriate composer
        if agents and components:
            return cls._compose_mixed(agents, components, **kwargs)
        elif agents:
            return cls._compose_agents(agents, **kwargs)
        elif components:
            return cls._compose_components(components, **kwargs)
        elif engines:
            return cls._compose_engines(engines, **kwargs)
        else:
            raise ValueError("No composable items provided")
    
    @classmethod
    def _compose_agents(cls, agents: list[Agent], **kwargs) -> StateSchema:
        """Compose agent schemas with AgentSchemaComposer"""
        return AgentSchemaComposer.from_agents(
            agents=agents,
            separation=kwargs.get("separation", "smart"),
            preserve_messages=True,
            **kwargs
        )
    
    @classmethod
    def _compose_components(cls, components: list[Component], **kwargs) -> StateSchema:
        """Compose component schemas with ComponentSchemaComposer"""
        return ComponentSchemaComposer.from_components(
            components=components,
            flow_pattern=kwargs.get("flow_pattern", "pipeline"),
            **kwargs
        )
    
    @classmethod
    def _compose_mixed(cls, agents: list[Agent], components: list[Component], **kwargs) -> StateSchema:
        """Compose mixed agent/component schemas"""
        return MixedSchemaComposer.from_mixed(
            agents=agents,
            components=components,
            **kwargs
        )
```

### Phase 2: Update All Agent Types
```python
# Standardize schema setup across all agent types:
class Agent:
    def _setup_schemas(self):
        """Unified schema setup for all agent types"""
        if not self.state_schema:
            all_items = self._collect_composable_items()
            
            if all_items:
                self.state_schema = UnifiedSchemaComposer.compose(
                    items=all_items,
                    name=f"{self.__class__.__name__}State",
                    agent_type=self.__class__.__name__
                )
```

### Phase 3: Fix Specific Issues
```python
# Fix SimpleAgent engine modification:
class SimpleAgent(Agent):
    def _setup_schemas(self):
        # Don't modify engine schemas directly
        # Use proper schema composition instead
        super()._setup_schemas()
        
        # Add structured output to agent schema, not engine schema
        if self.structured_output_model:
            self._add_structured_output_to_schema()

# Fix ChainAgent missing schema:
class SequentialAgent(Agent):
    def _setup_schemas(self):
        # Use AgentSchemaComposer for sequential agent coordination
        self.state_schema = AgentSchemaComposer.from_agents(
            agents=self.agents,
            separation="sequence",
            build_mode=BuildMode.SEQUENCE,
            preserve_messages=True
        )
```

## Benefits of Unified Strategy

### 1. **Consistency Across All Agent Types**
- All agents use same composition logic
- Consistent message preservation everywhere
- Standard field mapping patterns

### 2. **Type Safety Throughout**
- Schema drives node execution
- Type checking at composition time
- Runtime validation of field mappings

### 3. **Tool Coordination Reliability**
- tool_call_id preserved in all workflows
- Complete tool interaction context maintained
- No message field loss between components

### 4. **Developer Experience**
- Clear rules for when to use which composer
- Automatic selection of appropriate strategy
- Consistent API across all composition scenarios

### 5. **Performance Optimization**
- Schema-aware field extraction (only what's needed)
- Type-safe execution with validation
- Optimized field mapping based on component types

## Migration Guidelines

### For Agent Developers
```python
# OLD: Manual composer selection
if agents:
    schema = AgentSchemaComposer.from_agents(agents)
elif engines:
    schema = SchemaComposer.from_components(engines)

# NEW: Automatic composer selection
schema = UnifiedSchemaComposer.compose(items)
```

### For Framework Maintainers
1. **Add message preservation** to all existing schema composers
2. **Update agent base classes** to use unified composition
3. **Create migration helpers** for complex schemas
4. **Add validation** for schema composition correctness

This unified strategy ensures consistent, reliable schema composition across the entire framework while maintaining backward compatibility and providing clear upgrade paths.