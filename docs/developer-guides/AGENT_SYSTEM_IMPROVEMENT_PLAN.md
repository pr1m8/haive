# Agent System Improvement Plan

## 🎯 Core Vision
Make building agents as simple as writing a function, while preserving the power of the current system.

## 🔍 Current State Summary

### What We Have
1. **Engines**: Configuration factories (not directly callable)
2. **Nodes**: Graph building blocks with I/O mapping
3. **Agents**: Complex orchestrators that build graphs
4. **Schemas**: Dynamic Pydantic models with reducers
5. **Graphs**: BaseGraph → LangGraph conversion

### The Problems
1. **Too Many Concepts**: Users must understand 5+ abstractions
2. **Hidden Complexity**: Schema generation, tool routing, state management
3. **Poor Defaults**: Requires too much configuration
4. **Type Unsafety**: Dynamic schemas lose type information
5. **Hard Debugging**: Errors are cryptic and hard to trace

## 💡 Proposed Solutions

### Solution 1: Agent-as-Node Simplification

```python
# Current (complex)
class MyAgent(Agent):
    def build_graph(self):
        graph = BaseGraph(state_schema=self.state_schema)
        graph.add_node("process", EngineNode(name="process"))
        graph.add_edge(START, "process")
        graph.add_edge("process", END)
        return graph

# Proposed (simple)
@agent_node
def my_agent(query: str) -> str:
    engine = get_engine("gpt-4")
    return engine.invoke({"query": query})

# Or class-based but simpler
class MyAgent(SimpleNode):
    engine: Engine = GPT4Engine()
    
    def process(self, query: str) -> str:
        return self.engine.invoke({"query": query})
```

### Solution 2: Prebuilt Agent Types

```python
# Common patterns as ready-to-use classes
class ChatAgent(PrebuiltAgent):
    """Ready-to-use chat agent with messages and tools"""
    pass

class RAGAgent(PrebuiltAgent):
    """Ready-to-use RAG agent with retriever and LLM"""
    retriever: Retriever
    
class PlanExecuteAgent(PrebuiltAgent):
    """Ready-to-use planner/executor pattern"""
    planner: Engine
    executor: Engine
    
class RouterAgent(PrebuiltAgent):
    """Ready-to-use routing agent"""
    routes: Dict[str, Agent]
```

### Solution 3: Schema Templates

```python
# Prebuilt schemas for common patterns
from haive.schemas import (
    ChatSchema,      # messages + query/response
    RAGSchema,       # query + context + response  
    PlannerSchema,   # objective + steps + status
    RouterSchema,    # input + route + output
)

# Use directly
agent = SimpleAgent(engine=my_engine, schema=ChatSchema)

# Or extend
class MySchema(ChatSchema):
    custom_field: str = "default"
```

### Solution 4: Unified Node Interface

```python
# Everything is just a node
def create_workflow(*components):
    """Create workflow from any components"""
    nodes = [standardize(c) for c in components]
    return Graph(nodes)

# All these work the same way
workflow = create_workflow(
    my_agent,           # Agent
    my_engine,          # Engine  
    my_function,        # Callable
    lambda x: x * 2,    # Lambda
)
```

### Solution 5: Type-Safe Builders

```python
# Type-safe agent builder
agent = (
    AgentBuilder[InputType, OutputType]()
    .with_engine(my_engine)
    .with_tools(tool1, tool2)
    .with_reducer("messages", add_messages)
    .build()
)

# Catches errors at compile time
agent.invoke(InputType(...))  # ✓ Type checked
```

## 📋 Implementation Plan

### Phase 1: Core Simplification (Week 1-2)
1. **Standardized Node Interface**
   - Create universal `process()` method
   - Auto-detect component types
   - Unified execution model

2. **Agent-as-Node**
   - Agents are just nodes with internal graphs
   - No special treatment in multi-agent
   - Simple composition

3. **Simplified Schema System**
   - Prebuilt schemas for common cases
   - Explicit over implicit behavior
   - Better error messages

### Phase 2: Developer Experience (Week 3-4)
1. **Prebuilt Agents**
   - ChatAgent, RAGAgent, PlannerAgent, etc.
   - Ready-to-use with sensible defaults
   - Easy to extend

2. **Type-Safe APIs**
   - Generic types for input/output
   - Compile-time checking
   - IDE autocomplete

3. **Better Debugging**
   - Visual graph representation
   - Step-by-step execution tracing
   - Clear error messages

### Phase 3: Advanced Features (Week 5-6)
1. **Schema Compatibility**
   - Automatic adaptation between schemas
   - Compatibility checking
   - Migration tools

2. **Performance**
   - Lazy evaluation
   - Parallel execution
   - Caching

3. **Extensibility**
   - Plugin system
   - Custom node types
   - Hook points

## 🎨 Design Principles

1. **Simple by Default**: Common cases require minimal code
2. **Progressive Complexity**: Advanced features are optional
3. **Type Safety**: Catch errors early with strong typing
4. **Explicit Behavior**: No hidden magic
5. **Composable**: Everything works together naturally
6. **Backward Compatible**: Don't break existing code

## 📚 Example: Before and After

### Before (Current System)
```python
class MyRAGAgent(Agent):
    def __init__(self):
        retriever_engine = RetrieverEngine(...)
        llm_engine = AugLLMConfig(...)
        super().__init__(
            name="rag_agent",
            engines={"retriever": retriever_engine, "llm": llm_engine}
        )
    
    def build_graph(self):
        graph = BaseGraph(state_schema=self.state_schema)
        graph.add_node("retrieve", EngineNode(name="retrieve"))
        graph.add_node("generate", EngineNode(name="generate"))
        graph.add_edge(START, "retrieve")
        graph.add_edge("retrieve", "generate")
        graph.add_edge("generate", END)
        return graph
```

### After (Improved System)
```python
# Option 1: Prebuilt
agent = RAGAgent(
    retriever=my_retriever,
    llm=my_llm
)

# Option 2: Functional
@rag_agent
def my_rag(query: str) -> str:
    context = retrieve(query)
    return generate(query, context)

# Option 3: Simple class
class MyRAGAgent(SimpleNode):
    def process(self, query: str) -> str:
        context = self.retriever.search(query)
        return self.llm.invoke({
            "query": query,
            "context": context
        })
```

## 🚀 Success Metrics

1. **Lines of Code**: 50% reduction for common agents
2. **Time to First Agent**: Under 5 minutes
3. **Type Safety**: 90% of errors caught at compile time
4. **Documentation**: Every pattern has an example
5. **Performance**: No regression from current system

## 📅 Timeline

- **Week 1-2**: Core simplification
- **Week 3-4**: Developer experience
- **Week 5-6**: Advanced features
- **Week 7**: Documentation and examples
- **Week 8**: Migration guide and tools

## 🎯 End Goal

Building agents should feel like writing normal Python code, with the power of the graph system available when needed. The complexity should be progressive - simple things simple, complex things possible.