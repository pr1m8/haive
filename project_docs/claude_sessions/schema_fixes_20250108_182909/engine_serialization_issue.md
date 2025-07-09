# Engine Serialization Issue

## Problem
When EngineType enum is serialized, it's showing as 'EngineType.LLM' instead of 'llm'.

## Root Cause Analysis

1. **EngineType Definition**: Correctly defined as `class EngineType(str, Enum)`
2. **Engine Base Class**: Has `engine_type: EngineType` field
3. **Serialization Issue**: When engine objects are serialized (likely to dict), the enum is being converted to its string representation

## Likely Causes

1. **Custom Serialization**: Some code might be using `str()` on the enum instead of `.value`
2. **Pydantic Serialization**: When converting to dict, Pydantic might not be using the enum value
3. **State Composition**: When engines are added to state, they might be improperly serialized

## Solution Approaches

1. **Add Field Serializer**: Use Pydantic's field_serializer to ensure proper enum serialization
2. **Custom dict() method**: Override dict() to handle enum serialization
3. **Fix at State Level**: Ensure state composition properly handles engine serialization

## Recommended Fix

Add a field serializer to the Engine base class:

```python
from pydantic import field_serializer

class Engine(ABC, BaseModel, Generic[TIn, TOut]):
    # ... existing fields ...
    engine_type: EngineType = Field(description="Type of engine")
    
    @field_serializer('engine_type')
    def serialize_engine_type(self, engine_type: EngineType) -> str:
        """Ensure engine_type is serialized as its value, not string representation."""
        return engine_type.value
```