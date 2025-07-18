# Dynamic Schema Architecture Analysis - Claude Discovery Agent

**Date**: 2025-06-28
**Focus**: Understanding the dynamic typing system that gives generalizability but poor separation

## The Dynamic Architecture Problem

### Current System Overview

The Haive framework has a **highly dynamic, flexible architecture** but this flexibility comes at the cost of **poor separation of concerns** and **unclear boundaries**.

## Key Components Analysis

### 1. BaseGraph2 - Too Generic

```python
# Line 124-173 in base_graph2.py
class BaseGraph(BaseModel, ValidationMixin):
    # Core graph components - branches now handle conditional routing
    nodes: dict[str, Node | NodeConfig | Any | None] = Field(default_factory=dict)  # <-- ANY!
    edges: list[Edge] = Field(default_factory=list)
    branches: dict[str, Branch] = Field(default_factory=dict)
```

**Problems**:

- `nodes: dict[str, Node | NodeConfig | Any | None]` - **ANY type allowed!**
- No clear separation between different node types
- Everything is optional and loosely typed
- No enforcement of node contracts

### 2. NodeConfig - Massive Feature Creep

```python
# Lines 17-100 in base_config.py
class NodeConfig(ABC, BaseModel):
    # Core identification
    id: str
    name: str
    node_type: NodeType

    # ===== DYNAMIC ROUTING CAPABILITIES (OPTIONAL) =====
    routing_enabled: bool = Field(default=False)
    routing_strategy: Optional[Any] = Field(default=None)  # <-- ANY again!
    auto_wrap_commands: bool = Field(default=True)

    # I/O Schema Configuration
    input_schema: Optional[Type[BaseModel]] = Field(default=None)
    output_schema: Optional[Type[BaseModel]] = Field(default=None)

    # State field extraction
    extract_fields: Optional[Union[List[str], Dict[str, str]]] = Field(default=None)

    # Result field mapping
    result_fields: Optional[Union[str, List[str], Dict[str, str]]] = Field(default=None)

    # State transformation
    state_transformer: Optional[Callable[[Any], Any]] = Field(default=None)

    # Pre/post processing
    pre_process: Optional[Callable] = Field(default=None)
    post_process: Optional[Callable] = Field(default=None)
```

**Problems**:

- **Everything is optional** - no clear required contracts
- **Routing, I/O, processing, transformation** all mixed together
- **Generic "Any" types** everywhere
- **No clear separation** between different concerns

### 3. EngineNodeConfig - Smart But Complex

```python
# Lines 19-35 in engine_node.py
class EngineNodeConfig(NodeConfig):
    node_type: NodeType = Field(default=NodeType.ENGINE)
    engine: Engine | None = Field(default=None)
    engine_name: str | None = Field(default=None)

    # Field mappings (auto-normalized)
    input_fields: list[str] | dict[str, str] | None = Field(default=None)
    output_fields: list[str] | dict[str, str] | None = Field(default=None)
```

**Features**:

- Smart input/output mapping with engine-specific extraction
- Dynamic routing capabilities when enabled
- Type-aware processing (lines 358-490)
- Intelligent field mapping strategies

**Problems**:

- **Inherits all the complexity** from NodeConfig
- **Two different routing systems** (original + dynamic)
- **Unclear when to use which features**

## The Core Issues

### 1. **Everything is Optional/Any**

```python
# From BaseGraph
nodes: dict[str, Node | NodeConfig | Any | None]  # Any type allowed!

# From NodeConfig
routing_strategy: Optional[Any]  # Any strategy!
state_transformer: Optional[Callable[[Any], Any]]  # Any -> Any!
```

### 2. **Feature Creep in Base Classes**

- NodeConfig has **routing + I/O + processing + transformation**
- No clear separation between **simple nodes vs complex nodes**
- Every node gets **all capabilities** whether needed or not

### 3. **Multiple Overlapping Systems**

- **Original node execution** vs **dynamic routing**
- **Direct engine reference** vs **engine_name lookup**
- **Explicit mapping** vs **smart extraction**

### 4. **Unclear Boundaries**

- When to use `routing_enabled=True`?
- When to use `extract_fields` vs smart extraction?
- When to use `input_schema` vs engine input fields?

## The Schema Composition Problem

This architecture makes **schema composition challenging** because:

1. **No clear node contracts** - everything is optional
2. **Type safety lost** - `Any` types everywhere
3. **Feature mixing** - routing + I/O + processing all together
4. **Unclear interfaces** - what does each node actually do?

## Proposed Solutions

### 1. **Separate Node Types by Responsibility**

```python
# Base interface
class NodeContract(Protocol):
    def execute(self, state: StateType) -> ResultType: ...

# Specific implementations
class SimpleNode(NodeContract): pass
class RoutingNode(NodeContract): pass
class ProcessingNode(NodeContract): pass
class EngineNode(NodeContract): pass
```

### 2. **Clear Schema Interfaces**

```python
class SchemaAwareNode(Protocol):
    input_schema: Type[BaseModel]
    output_schema: Type[BaseModel]

class DynamicNode(Protocol):
    supports_routing: bool
    routing_strategy: RoutingStrategy
```

### 3. **Composition over Inheritance**

```python
class NodeCapabilities:
    routing: Optional[RoutingCapability] = None
    processing: Optional[ProcessingCapability] = None
    io_mapping: Optional[IOMappingCapability] = None

class TypedNode:
    capabilities: NodeCapabilities
    contract: NodeContract
```

### 4. **Typed State Flow**

```python
class TypedGraph:
    nodes: Dict[str, TypedNode]
    state_flow: StateFlowDefinition
    schema_composition: SchemaComposer
```

## Key Insights

1. **Dynamic typing gives flexibility** but loses **type safety** and **clear contracts**
2. **Feature mixing** makes it hard to understand what each component does
3. **Optional everything** means no guarantees about node behavior
4. **Multiple overlapping systems** create confusion about which to use

## Recommendation

**Split the architecture into layers**:

- **Contract Layer**: Clear interfaces and protocols
- **Implementation Layer**: Specific node types with clear responsibilities
- **Composition Layer**: Combine capabilities as needed
- **Schema Layer**: Type-safe state flow and schema composition

This would give the **flexibility of dynamic typing** while maintaining **clear boundaries** and **type safety**.
