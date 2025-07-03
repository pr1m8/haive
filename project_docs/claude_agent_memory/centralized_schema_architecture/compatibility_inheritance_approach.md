# Compatibility & Inheritance Approach - Claude Discovery Agent

**Date**: 2025-06-28  
**Focus**: Using compatibility patterns and better inheritance to fix the layered architecture

## Current Inheritance Problems

### **Broken Inheritance Chain**

```python
# Current: Each layer starts over, loses previous info
Engine (typed) → Node (Any) → Schema (recover) → Graph (Any) → Agent (mixed)

# Better: Each layer inherits and extends previous contracts
Engine → EngineAwareNode → SchemaAwareNode → TypedGraph → TypedAgent
```

### **No Compatibility Contracts**

```python
# Current: Everything accepts Any
def add_node(self, name: str, node: Any): ...

# Better: Compatibility interfaces
def add_node(self, name: str, node: EngineCompatible): ...
```

## Proposed Compatibility Pattern

### **1. Engine Compatibility Interface**

```python
from typing import Protocol

class EngineCompatible(Protocol):
    """Things that can work with engines."""

    def accepts_engine(self, engine: Engine) -> bool:
        """Check if this component can work with the engine."""

    def get_required_fields(self) -> Set[str]:
        """What fields this component needs from state."""

    def get_provided_fields(self) -> Set[str]:
        """What fields this component adds to state."""

    def validate_compatibility(self, other: 'EngineCompatible') -> bool:
        """Check if compatible with another component."""
```

### **2. Schema Compatibility Interface**

```python
class SchemaCompatible(EngineCompatible, Protocol):
    """Things that can work with typed schemas."""

    input_schema: Type[BaseModel] | None
    output_schema: Type[BaseModel] | None

    def derive_schema_fields(self) -> Dict[str, FieldInfo]:
        """Derive fields for schema composition."""

    def validate_schema_flow(self, input_schema: Type[BaseModel]) -> bool:
        """Check if can accept this input schema."""
```

### **3. Graph Compatibility Interface**

```python
class GraphCompatible(SchemaCompatible, Protocol):
    """Things that can be composed in graphs."""

    def get_dependencies(self) -> Set[str]:
        """What other nodes this depends on."""

    def get_routing_info(self) -> RoutingInfo:
        """How this node routes to others."""

    def compose_with(self, others: List['GraphCompatible']) -> CompositionResult:
        """Check how well this composes with others."""
```

## Better Inheritance Hierarchy

### **1. Typed Engine Base**

```python
class TypedEngine(Engine):
    """Engine with guaranteed type contracts."""

    # Override to ensure these are always provided
    input_schema: Type[BaseModel]  # Required, not optional
    output_schema: Type[BaseModel]  # Required, not optional

    def __init_subclass__(cls, **kwargs):
        """Ensure subclasses provide schemas."""
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, 'input_schema') or cls.input_schema is None:
            raise TypeError(f"{cls.__name__} must define input_schema")
        if not hasattr(cls, 'output_schema') or cls.output_schema is None:
            raise TypeError(f"{cls.__name__} must define output_schema")
```

### **2. Engine-Aware Node**

```python
class EngineAwareNode(NodeConfig):
    """Node that maintains engine type contracts."""

    engine: TypedEngine  # Not Optional!

    @property
    def input_schema(self) -> Type[BaseModel]:
        """Inherit input schema from engine."""
        return self.engine.input_schema

    @property
    def output_schema(self) -> Type[BaseModel]:
        """Inherit output schema from engine."""
        return self.engine.output_schema

    def accepts_engine(self, engine: Engine) -> bool:
        """Check engine compatibility."""
        return isinstance(engine, TypedEngine)

    def validate_state_compatibility(self, state_schema: Type[BaseModel]) -> bool:
        """Validate that state schema has required fields."""
        required = set(self.engine.get_input_fields().keys())
        available = set(state_schema.model_fields.keys())
        return required.issubset(available)
```

### **3. Schema-Aware Node**

```python
class SchemaAwareNode(EngineAwareNode):
    """Node that participates in schema composition."""

    field_mapping: Dict[str, str] = Field(default_factory=dict)

    def derive_schema_fields(self) -> Dict[str, FieldInfo]:
        """Contribute fields to schema composition."""
        fields = {}

        # Add input field requirements
        for field_name, (field_type, default) in self.engine.get_input_fields().items():
            mapped_name = self.field_mapping.get(field_name, field_name)
            fields[mapped_name] = FieldInfo(
                annotation=field_type,
                default=default,
                description=f"Input for {self.name}"
            )

        # Add output field contributions
        for field_name, (field_type, default) in self.engine.get_output_fields().items():
            mapped_name = self.field_mapping.get(field_name, field_name)
            fields[mapped_name] = FieldInfo(
                annotation=field_type,
                default=default,
                description=f"Output from {self.name}"
            )

        return fields
```

### **4. Typed Graph**

```python
class TypedGraph(BaseGraph):
    """Graph with type-safe node management."""

    nodes: Dict[str, SchemaAwareNode]  # Not Any!
    state_schema: Type[BaseModel]  # Required!

    def add_node(self, name: str, node: SchemaAwareNode) -> None:
        """Add node with compatibility validation."""
        # Validate node is compatible with current state schema
        if self.state_schema and not node.validate_state_compatibility(self.state_schema):
            raise ValueError(f"Node {name} not compatible with current state schema")

        # Validate node is compatible with existing nodes
        for existing_name, existing_node in self.nodes.items():
            if not node.validate_compatibility(existing_node):
                raise ValueError(f"Node {name} not compatible with existing node {existing_name}")

        self.nodes[name] = node

        # Update state schema to include this node's fields
        self._update_state_schema()

    def _update_state_schema(self) -> None:
        """Recompose state schema from all nodes."""
        composer = SchemaComposer(name=f"{self.name}State")

        for node in self.nodes.values():
            node_fields = node.derive_schema_fields()
            for field_name, field_info in node_fields.items():
                composer.add_field(field_name, field_info)

        self.state_schema = composer.build()
```

### **5. Typed Agent**

```python
class TypedAgent(Agent):
    """Agent with type-safe composition."""

    engines: Dict[str, TypedEngine]  # Not Optional!
    graph: TypedGraph  # Not Optional!

    def add_engine(self, name: str, engine: TypedEngine) -> None:
        """Add engine with automatic node creation."""
        # Create schema-aware node for this engine
        node = SchemaAwareNode(
            name=f"{name}_node",
            engine=engine,
            node_type=NodeType.ENGINE
        )

        # Add to engines and graph
        self.engines[name] = engine
        self.graph.add_node(f"{name}_node", node)

    def build_graph(self) -> TypedGraph:
        """Graph is maintained automatically."""
        return self.graph
```

## Compatibility Checking System

### **Automatic Validation**

```python
class CompatibilityChecker:
    """System for checking component compatibility."""

    @staticmethod
    def check_engine_node_compatibility(engine: Engine, node: NodeConfig) -> CompatibilityResult:
        """Check if node can work with engine."""
        issues = []

        # Check if node can accept engine type
        if not isinstance(node, EngineAwareNode):
            issues.append("Node doesn't support engines")

        # Check field compatibility
        required_inputs = set(engine.get_input_fields().keys())
        if hasattr(node, 'extract_fields') and node.extract_fields:
            available_extractions = set(node.extract_fields)
            missing = required_inputs - available_extractions
            if missing:
                issues.append(f"Node can't extract required fields: {missing}")

        return CompatibilityResult(compatible=len(issues) == 0, issues=issues)

    @staticmethod
    def check_node_schema_compatibility(node: NodeConfig, schema: Type[BaseModel]) -> CompatibilityResult:
        """Check if node works with schema."""
        # Implementation...

    @staticmethod
    def check_graph_composition(nodes: List[NodeConfig]) -> CompatibilityResult:
        """Check if nodes compose well together."""
        # Implementation...
```

## Key Benefits

### **1. Type Safety Preservation**

- Each layer inherits and extends type contracts
- No more `Any` types losing information
- Compile-time error catching

### **2. Compatibility Contracts**

- Clear interfaces for what works with what
- Automatic validation of component compatibility
- Better error messages when things don't fit

### **3. Progressive Enhancement**

- Start with simple Engine → upgrade to TypedEngine
- Start with NodeConfig → upgrade to EngineAwareNode
- Gradual migration path

### **4. Better Separation of Concerns**

- Each layer has clear responsibilities
- Inheritance follows logical progression
- No feature mixing

## Migration Strategy

### **Phase 1: Add Compatibility Interfaces**

```python
# Add protocols without breaking existing code
class EngineCompatible(Protocol): ...
class SchemaCompatible(Protocol): ...
```

### **Phase 2: Create Typed Subclasses**

```python
# New typed versions alongside existing
class TypedEngine(Engine): ...
class EngineAwareNode(NodeConfig): ...
```

### **Phase 3: Migrate Components**

```python
# Convert existing engines to typed versions
# Update nodes to be engine-aware
# Update graphs to be type-safe
```

### **Phase 4: Deprecate Old Patterns**

```python
# Mark Any-typed versions as deprecated
# Provide migration guides
# Eventually remove loose typing
```

This approach gives us **type safety + compatibility checking + better inheritance** while maintaining a migration path from the current system.
