# Debug Schema Composer Wrong Fields Issue

**Issue**: Schema composer is creating wrong output fields ['context', 'engine_name'] instead of ['retrieved_documents']
**Date**: 2025-01-09
**Status**: In Progress

## Problem Description

When running BaseRAGAgent, the schema composer is creating wrong output fields:

- Expected: `retrieved_documents` (from RetrieverOutput schema)
- Actual: `['context', 'engine_name']`

Error message:

```
INFO     Using schema-based output creation: ['context', 'engine_name']
```

This is causing the RAG agent to fail because it's not getting the correct fields from the retriever.

## Areas to Investigate

### 1. SchemaComposer.add_fields_from_engine()

- How does it extract fields from engine?
- Is it using the engine's output schema correctly?
- Is it adding management fields that override engine fields?

### 2. EngineNodeV2

- What modifications does it make to output?
- Is it overriding the engine's output schema?
- Is it adding its own fields?

### 3. BaseNodeConfig

- Is it adding extra fields during node creation?
- Are there default fields being injected?

### 4. BaseRAGAgent

- It's using EngineNodeConfig (not V2)
- But still getting wrong fields

## Debug Plan

1. **Check SchemaComposer.add_fields_from_engine()**
   - Look for where it gets output fields from engine
   - Check if it's modifying or overriding fields

2. **Check EngineNode output handling**
   - See how it processes engine output schema
   - Look for field additions or modifications

3. **Trace field creation**
   - Add debug logging to see where 'context' and 'engine_name' come from
   - These don't exist in RetrieverOutput schema

4. **Check engine registration**
   - Ensure retriever engine is properly registered
   - Check if schema is being cached incorrectly

## Hypothesis

The issue might be:

1. SchemaComposer is adding management fields that override engine output
2. EngineNode is not respecting the engine's output schema
3. There's a mismatch between what the engine declares and what gets composed

## Next Steps

1. Read SchemaComposer.add_fields_from_engine()
2. Read EngineNode/EngineNodeV2 output handling
3. Add debug logging to trace field creation
4. Fix the field generation logic
