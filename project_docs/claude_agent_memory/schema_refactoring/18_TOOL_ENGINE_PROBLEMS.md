# Critical Issue: Tool Engines and Other Engine Problems

## Overview

Beyond the schema chaos, we have MAJOR issues with tool engines and other engine implementations that are fundamental to the system working at all.

## Tool Engine Problems

### **1. Tool Engines Not Working Properly**

#### Current Broken Patterns

```python
# Tools treated as engines sometimes
class ToolEngine(Engine):
    tools: List[Any]  # What goes here?

    def invoke(self, input_data):
        # How do tools get executed?
        # How do they relate to structured output?
        # What about tool routing?

# Tools treated as schemas sometimes
if self.structured_output_model not in self.tools:
    self.tools.append(self.structured_output_model)  # Pydantic model as tool?!

# Tools in engine.tools vs engine.schemas vs engine.pydantic_tools
# THREE different places for tools!
```

#### The Confusion

- Are tools engines?
- Are tools schemas?
- Are tools separate things?
- How do tool engines relate to other engines?
- Why are Pydantic models becoming tools?

### **2. Engine Type Proliferation**

```
Current Engine Types (all broken in different ways):
├── Engine (base - confused about identity)
├── InvokableEngine (adds invoke... but Engine already has it?)
├── ToolEngine (broken tool handling)
├── LLMEngine (LLM-specific... or not?)
├── PromptTemplateEngine (is this even an engine?)
├── AugLLMConfig (config that's also an engine?!)
├── RetrievalEngine (how does this relate to tools?)
└── Agent (which IS an engine too!)
```

### **3. Tool Execution Path Chaos**

```python
# Path 1: Through ToolNodeConfig
ToolNodeConfig → finds tools in 3 places → filters by routes → executes somehow

# Path 2: Through ValidationNodeConfig
ValidationNodeConfig → syncs tools/schemas → routes to other nodes → ???

# Path 3: Through Engine directly
Engine.tools → but how are they executed?

# Path 4: Through structured output
StructuredOutputMixin → adds Pydantic models as tools → ???
```

## Other Engine Problems

### **1. Engine Registry Chaos**

```python
# Global registry
EngineRegistry.register(engine)

# But also in agent.engines
agent.engines["main"] = engine

# And in node metadata
node.metadata["engine"] = engine

# And passed directly
EngineNodeConfig(engine=engine)

# WHICH IS THE SOURCE OF TRUTH?!
```

### **2. Engine Creation Confusion**

```python
# Engines create runnables
engine.create_runnable()

# But engines ARE runnables
engine.invoke()

# And engines can be created from configs
config.create_engine()

# But configs ARE engines
config.invoke()

# CIRCULAR MADNESS!
```

### **3. Engine Type System Disasters**

```python
# No type parameters
class Engine:
    def invoke(self, input_data, config=None):  # Any in, Any out

# Should be:
class Engine[TInput, TOutput]:
    def invoke(self, input: TInput) -> TOutput:  # Type safe!

# But then how do tools fit in?
class ToolEngine[TInput, TOutput, TTool]:  # Gets complex fast
```

## State Schema Module Problems (Additional)

### **1. State Schema Engine Integration**

```python
# State schemas have engines somehow
class StateSchema:
    __engine_io_mappings__ = {}  # What engines?

    def get_all_class_engines(self):  # Engines in schemas?
        # How did engines get here?
```

### **2. Schema-Tool Confusion**

```python
# Schemas contain tools
def get_state_tools(self) -> list[Any]:
    # Tools from state schema?

# But tools need schemas
class Tool:
    input_schema: Type[BaseModel]
    output_schema: Type[BaseModel]

# CIRCULAR DEPENDENCY!
```

## The Full Scope of Work

### **Engine System** (Completely Broken)

- [ ] Define what an Engine actually IS
- [ ] Fix Engine vs Config vs Executable
- [ ] Separate tool engines from other engines
- [ ] Create proper engine hierarchy
- [ ] Add type parameters everywhere
- [ ] Fix engine registry/discovery

### **Tool System** (Not Working)

- [ ] Define what a Tool actually IS
- [ ] Fix tool vs schema vs engine confusion
- [ ] Unify tool discovery (not 3 places)
- [ ] Fix tool routing system
- [ ] Standardize tool execution
- [ ] Fix structured output as tools

### **Schema System** (What we already knew)

- [ ] Break apart StateSchema (2,153 lines)
- [ ] Replace SchemaComposer (29k tokens)
- [ ] Fix schema-engine integration
- [ ] Add proper type safety
- [ ] Use Pydantic v2 features

### **Node System** (Also Broken)

- [ ] Fix node config patterns
- [ ] Unify engine access in nodes
- [ ] Type-safe node definitions
- [ ] Standardize execution patterns

### **Graph System** (Affected by Everything)

- [ ] Type-safe graph nodes
- [ ] Clear compilation model
- [ ] Subgraph handling
- [ ] State management

## Complexity Update

### Previous Assessment: 37🔥

### New Assessment: 52🔥 (Added 15🔥 for engine/tool issues)

| Component       | Issues | Complexity | Priority |
| --------------- | ------ | ---------- | -------- |
| Tool Engines    | 8+     | 🔥🔥🔥🔥🔥 | CRITICAL |
| Other Engines   | 6+     | 🔥🔥🔥🔥   | CRITICAL |
| Engine Registry | 4+     | 🔥🔥🔥     | HIGH     |
| Tool Routing    | 5+     | 🔥🔥🔥     | HIGH     |

## Impact

Without fixing the engine/tool system:

- **Tools don't execute reliably**
- **Can't add new tool types**
- **Structured output breaks randomly**
- **Multi-agent tool sharing fails**
- **No type safety for tool calls**

## For Our Session

We need to address:

1. **What IS an Engine?** (fundamental concept)
2. **What IS a Tool?** (fundamental concept)
3. **How do they relate?** (architecture)
4. **How do we fix tool execution?** (implementation)
5. **How do we type everything?** (safety)

This is even bigger than we thought!
