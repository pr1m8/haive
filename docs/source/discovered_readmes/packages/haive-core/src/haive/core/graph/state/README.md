# State Management System

This module provides generic state management abstractions for graph execution,
including state interfaces, transformation utilities, and validation mixins.

## Overview

The state management system is designed to:

- **Support any state type**: Works with dicts, Pydantic models, custom classes
- **Provide validation**: Type-safe state validation with clear error messages
- **Enable transformation**: Flexible state transformation pipelines
- **Maintain immutability**: Optional immutable state handling

## Core Components

### `StateProtocol[T]`

Generic protocol for state objects with type safety.

### `StateTransformer[TInput, TOutput]`

Abstract base for state transformation logic.

### `StateValidator[T]`

Validation system for state objects with comprehensive error reporting.

### `StateValidationMixin`

Mixin for adding state validation to any class.

## Usage

```python
from haive.core.graph.state import StateProtocol, StateValidator, StateTransformer

# Define state type
class MyState(StateProtocol):
    data: dict
    step: int

# Create validator
validator = StateValidator(MyState)

# Create transformer
class MyTransformer(StateTransformer[dict, MyState]):
    def transform(self, input_state: dict) -> MyState:
        return MyState(data=input_state, step=0)

# Use in graph
transformer = MyTransformer()
validated_state = transformer.transform({"key": "value"})
```

## Integration

- Works with any graph execution engine
- Supports Pydantic models out of the box
- Integrates with validation mixin system
- Compatible with immutable state patterns
