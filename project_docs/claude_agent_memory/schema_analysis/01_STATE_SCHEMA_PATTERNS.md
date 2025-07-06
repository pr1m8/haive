# State Schema Patterns Analysis

**Memory Tag**: [MEM-101-A]  
**Parent**: [MEM-101] Schema Analysis  
**Related**: [MEM-102-A] Base Agent Architecture  
**Date**: 2025-01-06

## 🎯 Purpose

Document patterns and insights about StateSchema, the foundation of agent state management in Haive.

## 📊 Core StateSchema Patterns

### 1. Base StateSchema Class

- Location: `/packages/haive-core/src/haive/core/schema/state_schema.py`
- Purpose: Abstract base for all agent states
- Key features:
  - Engine management at class and instance level
  - Tool routing and distribution
  - Schema derivation capabilities
  - Automatic field generation

### 2. Schema Inheritance Hierarchy

```
StateSchema (abstract base)
├── MessagesState (basic messaging)
├── ToolState (tool management)
├── ValidationState (with validation routing)
└── Custom schemas (agent-specific)
```

### 3. Engine Management Pattern

```python
class MyAgentState(StateSchema):
    # Class-level engines (shared across instances)
    llm: AugLLMEngine = AugLLMEngine(name="main_llm")
    retriever: RetrieverEngine = RetrieverEngine(name="retriever")

    # Instance fields
    messages: list[BaseMessage] = []
    context: str = ""
```

### 4. Tool Routing Pattern

```python
# Tools are routed to engines based on type
tool_routes = {
    "pydantic_model": ["llm"],      # Pydantic tools → LLM
    "langchain_tool": ["tool_node"], # LangChain tools → tool node
    "function": ["llm", "parser"]    # Functions → multiple engines
}
```

## 🔍 Key Insights

### Schema Composition Process

1. **Engine Discovery**: Find all engines (class + instance level)
2. **Field Extraction**: Get fields from each engine
3. **Field Merging**: Combine fields, handling conflicts
4. **Schema Building**: Create final Pydantic model

### Tool Distribution Logic

1. **Route Detection**: Analyze tool type/interface
2. **Engine Matching**: Find engines accepting route
3. **Tool Assignment**: Add tools to matched engines
4. **Sync on Access**: Tools synced when engine accessed

### Schema Derivation

- **Input Schema**: Extract only input-relevant fields
- **Output Schema**: Extract only output-relevant fields
- **Focused schemas**: Prevent exposing internal state

## 🐛 Common Issues

### 1. Missing Engine Registration

**Problem**: Engines not found by nodes  
**Solution**: Register in EngineRegistry

```python
EngineRegistry.get_instance().register(engine)
```

### 2. Tool Routing Failures

**Problem**: Tools not reaching correct engine  
**Solution**: Configure tool routes properly

```python
state.configure_engine_routes("llm", ["pydantic_model"])
```

### 3. Schema Generation Errors

**Problem**: Fields missing or duplicated  
**Solution**: Check engine output schema configuration

## 💡 Best Practices

1. **Define engines at class level** for sharing
2. **Use descriptive engine names** for routing
3. **Configure tool routes explicitly** when needed
4. **Derive focused schemas** for input/output
5. **Test schema generation** with real engines

## 🔗 Cross-References

- Engine patterns: [MEM-104-A]
- Tool routing details: [MEM-101-C]
- Schema composer: [MEM-101-B]
- Common errors: [MEM-105-A]

---

**Status**: Living document
**Last Updated**: 2025-01-06
