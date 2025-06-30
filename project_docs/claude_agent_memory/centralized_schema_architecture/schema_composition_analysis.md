# Schema Composition Analysis - Claude Agent Memory

**Agent Name**: Claude Discovery Agent
**Date**: 2025-06-28
**Focus**: Schema composition patterns and issues in Haive agents

## Critical Points to Remember

### 1. NO DIRECT ENGINE MODIFICATION
- SimpleAgent directly modifies engine schemas - **THIS IS BAD**
- Breaks engine assumptions
- Can contaminate shared engines
- Must be fixed

### 2. Compatibility Component
- AgentSchemaComposer includes compatibility analysis
- Tracks which fields work with which components
- Important for multi-agent coordination
- Not discussed enough in initial analysis

### 3. Multi vs Chain Comparison (MISSING FROM ANALYSIS)
- Need to analyze how Chain agents handle schemas
- Compare with Multi-agent approach
- Identify conflicts and patterns

### 4. Other Agent Problems (NOT FULLY DISCUSSED)
- RAG agents: Inconsistent schema patterns
- ReAct agents: Multiple versions with different approaches
- Generic agents: Over-engineered type system doesn't play well with dynamic schemas

## Key Schema Composition Findings

### FieldDefinition Complexity
```python
FieldDefinition(
    name="messages",
    field_type=List[BaseMessage],
    default_factory=list,
    shared=True,  # Parent/child communication
    reducer=preserve_messages_reducer,  # CRITICAL for tool_call_id
    input_for=["llm_engine"],
    output_from=["message_processor"],
    source="conversation_agent"
)
```

### AgentSchemaComposer Features
1. **Separation Strategies**:
   - "shared": All agents see all fields
   - "smart": Automatic sharing based on usage
   - "namespaced": Prefixed fields per agent

2. **Automatic Reducer Assignment**:
   - Messages always get preserve_messages_reducer
   - Prevents tool_call_id loss

3. **Engine I/O Mapping**:
   - Preserves which engines produce/consume fields
   - Critical for routing

### Current Issues Summary
1. SimpleAgent modifies engine schemas directly
2. No consistent base pattern for schema extension
3. Each agent type has different approach
4. Complex metadata not used consistently
5. RAG agents lack consistent patterns
6. Chain vs Multi comparison needed

## Next Focus Areas
1. Analyze Chain agent schema handling
2. Compare Multi vs Chain approaches
3. Document all agent type problems
4. Design unified schema extension pattern
5. Fix direct engine modification issue