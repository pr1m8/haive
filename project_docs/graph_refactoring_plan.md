# Haive Graph System Refactoring Plan

## Executive Summary

This document outlines a comprehensive refactoring plan for the Haive graph system to address core architectural issues and improve generalization. The plan is organized into disjoint implementation sets based on priority, process isolation, and memory requirements.

## Current Issues Analysis

### Core Problems Identified

1. **Dynamic Routing Disconnection**: `base_config.py` has dynamic routing capabilities but `base_graph2.py` doesn't properly integrate with them
2. **Graph Structure Specificity**: Current graph is too specific to Haive use cases, lacks generic abstractions
3. **Visualization Coupling**: Visualization logic is embedded rather than being a mixin
4. **Subgraph Handling**: Poor handling of nested subgraphs and composition
5. **Registry Limitations**: Missing generic registry system for components
6. **Conditional Edge Complexity**: Confusing branch vs conditional edge concepts
7. **Send Operation Integration**: Lacks proper support for parallel execution patterns

## Implementation Plan: Disjoint Sets

### SET A: Core Foundations (Priority: CRITICAL, Memory: High)

**Process**: Core abstractions and base classes
**Dependencies**: None (foundation layer)
**Timeline**: Phase 1 (Weeks 1-2)

#### A1. Generic Graph Core

```
packages/haive-core/src/haive/core/graph/generic/
├── README.md
├── __init__.py
├── core_graph.py          # Generic graph structure
├── core_node.py           # Generic node interface
├── core_edge.py           # Generic edge types
├── core_registry.py       # Generic component registry
└── types.py               # Core type definitions
```

**Key Components:**

- `GenericGraph[TNode, TEdge, TState]` - Parameterized graph base
- `GenericNode[TInput, TOutput]` - Generic node interface
- `GenericEdge[TCondition]` - Generic edge with condition support
- `ComponentRegistry[T]` - Generic registry mixin with type safety

#### A2. State Management Abstractions

```
packages/haive-core/src/haive/core/graph/state/
├── README.md
├── __init__.py
├── state_interface.py     # Generic state protocol
├── state_transformer.py  # State transformation utilities
└── state_validation.py   # State validation mixins
```

### SET B: Execution Engine (Priority: CRITICAL, Memory: Medium)

**Process**: Execution and routing logic
**Dependencies**: SET A
**Timeline**: Phase 1 (Weeks 2-3)

#### B1. Enhanced Routing System

```
packages/haive-core/src/haive/core/graph/routing/
├── README.md
├── __init__.py
├── routing_engine.py      # Central routing coordination
├── strategies/
│   ├── __init__.py
│   ├── base_strategy.py   # Strategy interface
│   ├── dynamic_strategy.py # Dynamic type-hint based routing
│   ├── conditional_strategy.py # Conditional routing
│   └── parallel_strategy.py # Send/parallel routing
└── validators/
    ├── __init__.py
    ├── route_validator.py # Validates routes exist
    └── type_validator.py  # Type hint validation
```

#### B2. Command & Send Integration

```
packages/haive-core/src/haive/core/graph/execution/
├── README.md
├── __init__.py
├── command_wrapper.py     # Auto-wrapping of results
├── send_coordinator.py    # Parallel execution coordination
├── execution_context.py   # Execution state management
└── result_processor.py    # Result handling and state updates
```

### SET C: Node System Refactoring (Priority: HIGH, Memory: Medium)

**Process**: Node implementation and configuration
**Dependencies**: SET A, SET B
**Timeline**: Phase 2 (Weeks 3-4)

#### C1. Enhanced Node Base Classes

```
packages/haive-core/src/haive/core/graph/node/enhanced/
├── README.md
├── __init__.py
├── enhanced_base_config.py # Improved NodeConfig with routing
├── dynamic_node_mixin.py   # Dynamic routing capabilities
├── validation_mixin.py     # Input/output validation
├── processing_hooks.py     # Pre/post processing
└── schema_integration.py   # Pydantic schema support
```

#### C2. Node Type Validation & Registry

```
packages/haive-core/src/haive/core/graph/node/registry/
├── README.md
├── __init__.py
├── node_registry.py       # Node type registry
├── type_resolver.py       # Type hint to node route resolution
├── validation_registry.py # Route validation rules
└── factory.py             # Enhanced node factory
```

### SET D: Visualization & Tooling (Priority: MEDIUM, Memory: Low)

**Process**: Developer tools and visualization
**Dependencies**: SET A, SET C
**Timeline**: Phase 3 (Weeks 4-5)

#### D1. Visualization Mixin System

```
packages/haive-core/src/haive/core/graph/visualization/
├── README.md
├── __init__.py
├── visualization_mixin.py # Mixin for graph visualization
├── renderers/
│   ├── __init__.py
│   ├── mermaid_renderer.py
│   ├── graphviz_renderer.py
│   └── ascii_renderer.py
└── export/
    ├── __init__.py
    ├── image_export.py
    └── interactive_export.py
```

#### D2. Development Tools

```
packages/haive-core/src/haive/core/graph/dev_tools/
├── README.md
├── __init__.py
├── graph_inspector.py     # Graph structure analysis
├── route_analyzer.py      # Route validation and analysis
├── performance_profiler.py # Execution profiling
└── debug_renderer.py      # Debug visualization
```

### SET E: Subgraph & Composition (Priority: MEDIUM, Memory: High)

**Process**: Advanced graph composition
**Dependencies**: SET A, SET B, SET C
**Timeline**: Phase 3 (Weeks 5-6)

#### E1. Subgraph Management

```
packages/haive-core/src/haive/core/graph/composition/
├── README.md
├── __init__.py
├── subgraph_manager.py    # Subgraph lifecycle management
├── graph_composer.py      # Graph composition utilities
├── boundary_manager.py    # Subgraph boundaries and interfaces
└── nesting_validator.py   # Nested graph validation
```

#### E2. Graph Patterns & Templates

```
packages/haive-core/src/haive/core/graph/patterns/enhanced/
├── README.md
├── __init__.py
├── pattern_registry.py    # Enhanced pattern system
├── template_engine.py     # Graph template system
├── composition_patterns.py # Common composition patterns
└── migration_patterns.py  # Migration utilities
```

### SET F: Haive-Specific Implementation (Priority: MEDIUM, Memory: Medium)

**Process**: Haive-specific graph implementation
**Dependencies**: SET A, SET B, SET C
**Timeline**: Phase 4 (Weeks 6-7)

#### F1. Haive Graph Implementation

```
packages/haive-core/src/haive/core/graph/haive/
├── README.md
├── __init__.py
├── haive_graph.py         # Haive-specific graph extending generic
├── haive_node_types.py    # Haive node type definitions
├── haive_routing.py       # Haive-specific routing strategies
└── haive_patterns.py      # Haive-specific graph patterns
```

#### F2. Migration & Compatibility

```
packages/haive-core/src/haive/core/graph/migration/
├── README.md
├── __init__.py
├── legacy_adapter.py      # Backward compatibility layer
├── migration_tools.py     # Migration utilities
├── compatibility_tests.py # Compatibility validation
└── upgrade_guide.md       # Migration documentation
```

### SET G: Testing & Documentation (Priority: MEDIUM, Memory: Low)

**Process**: Quality assurance and documentation
**Dependencies**: All previous sets
**Timeline**: Continuous (Weeks 1-7)

#### G1. Comprehensive Testing

```
packages/haive-core/tests/graph/
├── test_generic/          # Generic graph tests
├── test_routing/          # Routing system tests
├── test_nodes/            # Node system tests
├── test_composition/      # Subgraph tests
├── test_haive/            # Haive-specific tests
├── test_migration/        # Migration tests
├── integration/           # Integration tests
└── performance/           # Performance tests
```

#### G2. Documentation System

```
packages/haive-core/docs/graph/
├── README.md
├── architecture/          # Architecture documentation
├── api/                   # API documentation
├── tutorials/             # Tutorial guides
├── migration/             # Migration guides
└── examples/              # Example implementations
```

## Memory Requirements Analysis

### High Memory Components (>100MB peak)

- **SET A**: Core graph structures with type parameterization
- **SET E**: Subgraph composition with deep nesting support
- Requires careful memory management and lazy loading

### Medium Memory Components (10-100MB peak)

- **SET B**: Execution engine with routing caches
- **SET C**: Node registry with type reflection
- **SET F**: Haive implementation with legacy support

### Low Memory Components (<10MB peak)

- **SET D**: Visualization tools (generate on demand)
- **SET G**: Testing and documentation

## Implementation Phases

### Phase 1: Foundation (Weeks 1-3)

- **Primary**: SET A + SET B
- **Secondary**: Begin SET G testing framework
- **Deliverable**: Generic graph core with routing engine

### Phase 2: Node Enhancement (Weeks 3-4)

- **Primary**: SET C
- **Secondary**: Continue SET G, begin SET D
- **Deliverable**: Enhanced node system with dynamic routing

### Phase 3: Advanced Features (Weeks 4-6)

- **Primary**: SET D + SET E
- **Secondary**: Begin SET F
- **Deliverable**: Visualization + subgraph composition

### Phase 4: Haive Integration (Weeks 6-7)

- **Primary**: SET F
- **Secondary**: Complete SET G
- **Deliverable**: Full Haive implementation with migration path

## Risk Mitigation

### High-Risk Components

1. **Dynamic Type Resolution** (SET B): Complex type hint parsing
   - _Mitigation_: Extensive unit testing, fallback mechanisms
2. **Subgraph Composition** (SET E): Complex nesting scenarios
   - _Mitigation_: Incremental implementation, boundary validation
3. **Memory Management** (SET A, E): Large graph structures
   - _Mitigation_: Lazy loading, weak references, memory profiling

### Medium-Risk Components

1. **Legacy Compatibility** (SET F): Breaking changes
   - _Mitigation_: Adapter pattern, deprecation warnings
2. **Performance** (SET B): Routing overhead
   - _Mitigation_: Caching, profiling, optimization

## Success Metrics

### Technical Metrics

- [ ] Generic graph supports any node/edge types
- [ ] Dynamic routing resolves type hints to valid routes
- [ ] Subgraphs compose without memory leaks
- [ ] Visualization works as optional mixin
- [ ] 100% backward compatibility maintained
- [ ] <10% performance overhead vs current implementation

### Development Metrics

- [ ] Clear separation of concerns (disjoint sets)
- [ ] Comprehensive test coverage (>90%)
- [ ] Complete API documentation
- [ ] Migration guide with examples
- [ ] Performance benchmarks established

## Integration with Haive DataFlow

### Registry Integration Points

- `ComponentRegistry` (SET A) designed to link with haive-dataflow
- Generic type system supports dataflow node registration
- Routing strategies can integrate with dataflow pipelines
- Visualization system exports to dataflow-compatible formats

### Future Extension Points

- Plugin architecture for custom routing strategies
- Extensible visualization renderer system
- Generic registry supports arbitrary component types
- Composition patterns support dataflow integration

## Implementation Notes

### Code Standards

- **Documentation**: Google-style docstrings with top-file comments
- **Testing**: `poetry run pytest` in package-specific test directories
- **Module READMEs**: Every module gets explanatory README
- **Type Safety**: Full type hints with generic parameterization

### File Organization

- Packages in `/home/will/Projects/haive/backend/haive/packages/`
- Tests in `{package}/tests/` with appropriate routing
- Each SET is independently testable
- Clear dependency chains between sets

This plan provides a comprehensive roadmap for refactoring the Haive graph system into a robust, generic, and extensible architecture while maintaining backward compatibility and addressing all identified issues.
