# Generic Graph Core

This module provides the foundational abstractions for generic graph structures in the Haive framework.

## Overview

The generic graph system is designed to be:

- **Type-safe**: Full generic parameterization for nodes, edges, and states
- **Extensible**: Clean interfaces for custom implementations
- **Memory-efficient**: Lazy loading and weak references for large graphs
- **Dataflow-ready**: Integration points for haive-dataflow

## Core Components

### `GenericGraph[TNode, TEdge, TState]`

The main graph structure that can be parameterized with any node, edge, and state types.

### `GenericNode[TInput, TOutput]`

Abstract base for nodes with type-safe input/output contracts.

### `GenericEdge[TCondition]`

Edge abstraction supporting conditional routing.

### `ComponentRegistry[T]`

Generic registry system with type safety and dataflow integration points.

## Usage

```python
from haive.core.graph.generic import GenericGraph, GenericNode, GenericEdge

# Create a typed graph
class MyNode(GenericNode[dict, str]):
    def process(self, input_data: dict) -> str:
        return str(input_data)

class MyEdge(GenericEdge[bool]):
    def evaluate_condition(self, state) -> bool:
        return True

graph = GenericGraph[MyNode, MyEdge, dict]()
```

## Integration Points

- **Registry System**: `ComponentRegistry` can link to haive-dataflow registries
- **State Management**: Generic state interfaces work with any state type
- **Validation**: Type-safe validation at compile and runtime
