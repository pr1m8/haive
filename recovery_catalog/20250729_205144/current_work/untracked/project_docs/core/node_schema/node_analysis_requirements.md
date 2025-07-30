# Node Schema Composition Analysis Requirements

**Document Version**: 1.0
**Purpose**: Central documentation for node schema composition patterns and requirements
**Last Updated**: 2025-01-29
**Status**: Active Reference

## 🎯 Overview

This document outlines the requirements and patterns for node schema composition in the Haive framework, particularly focusing on validation nodes and dynamic schema handling.

## 📋 Core Requirements

### 1. Schema Composition Hierarchy

```
NodeSchemaComposer (needed)
    ↓
AgentSchemaComposer (exists - for agents)
    ↓  
MultiAgentSchemaComposer (needs update - field visibility)
```

### 2. Dynamic Field Mapping

The system needs to support flexible I/O mapping for nodes:

- **Extract Functions**: Pull specific fields from input state
- **Update Functions**: Map outputs back to state fields
- **Field Renaming**: Support "result → potato" type mappings
- **Type Safety**: Maintain type checking through transformations

### 3. Validation Node Patterns

Two primary patterns for validation nodes:

#### Pattern A: Direct Schema Extension
```python
class ValidationState(MessagesState):
    validation_result: Optional[ValidationResult] = Field(default=None)
    validation_history: List[ValidationResult] = Field(default_factory=list)
```

#### Pattern B: Nested Validation State
```python
class NestedValidationState(BaseModel):
    messages: List[BaseMessage]
    validation: ValidationData  # Nested structure
```

### 4. Field Visibility Requirements

For multi-agent systems, we need:

- **Shared Fields**: Visible to all agents (e.g., messages)
- **Private Fields**: Agent-specific state
- **Coordinator Fields**: Routing and orchestration metadata
- **Projection Support**: Type-safe field access

## 🏗️ Architecture Patterns

### 1. Node Input/Output Patterns

```python
# Flexible I/O mapping
node_config = {
    "input_mapping": {
        "messages": "conversation",  # state.conversation → node.messages
        "context": "shared_context"
    },
    "output_mapping": {
        "result": "validation_result",  # node.result → state.validation_result
        "score": "quality_score"
    }
}
```

### 2. Schema Composer Pattern

```python
class NodeSchemaComposer:
    """Compose schemas dynamically for nodes."""
    
    def compose(
        self,
        base_schema: Type[BaseModel],
        extensions: List[Type[BaseModel]],
        field_mappings: Dict[str, str]
    ) -> Type[BaseModel]:
        """Create composed schema with mappings."""
        pass
```

### 3. Validation Integration

```python
# Validation as a node capability
validation_node = create_node(
    ValidationEngine(),
    input_schema=MessagesState,
    output_schema=ValidationState,
    merge_strategy="update"  # or "replace"
)
```

## 📊 Implementation Status

### ✅ Completed

1. **Base Schema Patterns** - MessagesState, StateSchema foundations
2. **Agent Schema Composition** - Working for single agents
3. **Basic Validation Nodes** - Simple validation patterns

### 🔄 In Progress

1. **NodeSchemaComposer** - Flexible schema composition
2. **Field Visibility Rules** - Multi-agent field access
3. **Dynamic Mapping** - Runtime field transformations

### 📅 Planned

1. **Schema Evolution** - Version migration support
2. **Complex Projections** - Advanced field transformations
3. **Performance Optimization** - Schema caching

## 🎯 Success Criteria

1. **Type Safety**: Full type checking through all transformations
2. **Flexibility**: Support arbitrary field mappings
3. **Performance**: <1ms schema composition overhead
4. **Developer Experience**: Clear, intuitive API
5. **Compatibility**: Works with existing patterns

## 🔗 Related Documentation

- [Node I/O Patterns](./node_io_patterns.md)
- [Validation Node Comparison](./validation_node/validation_nodes_comparison.md)
- [Meta State Pattern](../../active/architecture/meta_state_pattern.md)
- [Multi-Agent Architecture](../../active/architecture/multi_agent_meta_agent_memory_hub.md)

## 📝 Example Implementations

### Simple Validation Node

```python
class ValidationNode:
    """Basic validation node with schema composition."""
    
    def __init__(self, validation_model: Type[BaseModel]):
        self.schema = compose_schemas(
            MessagesState,
            ValidationResultSchema,
            field_mappings={"messages": "conversation"}
        )
```

### Multi-Agent Validation

```python
class MultiAgentValidationNode:
    """Validation across multiple agents."""
    
    def __init__(self, agents: List[Agent]):
        self.schema = MultiAgentSchemaComposer.compose(
            base=MessagesState,
            agent_schemas={a.name: a.state_schema for a in agents},
            shared_fields=["messages", "context"],
            private_fields=["internal_state", "memory"]
        )
```

## 🚀 Next Steps

1. **Implement NodeSchemaComposer** - Core composition logic
2. **Update Validation Nodes** - Use new patterns
3. **Test Multi-Agent Scenarios** - Field visibility
4. **Document Patterns** - Developer guide
5. **Performance Testing** - Benchmark overhead

---

**Note**: This document is actively maintained as the node schema system evolves.