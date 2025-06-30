# Agent vs Component Architecture - Claude Discovery Agent

**Date**: 2025-06-28  
**Focus**: Fundamental distinction between true agents and simple executable components

## The Core Distinction

### **Not Everything is an Agent**

There's a fundamental architectural confusion in the current system: we're treating simple executable components as if they were agents. This leads to unnecessary complexity and incorrect schema composition patterns.

## Component Types

### **1. Simple Executable Components (NOT Agents)**

These are basic execution units that perform specific tasks without reasoning:

```python
# Simple components - just execute, no reasoning
- Retriever: Fetches documents based on query
- Embeddings: Converts text to vectors
- VectorStore: Stores and searches vectors
- Callable: Executes a function
- Parser: Transforms data format
```

**Characteristics:**
- Single-purpose execution
- No decision-making capability
- No reasoning or planning
- Can be nodes in a graph
- Do NOT need AgentSchemaComposer

### **2. True Agents**

Agents have reasoning capability and combine multiple components:

```python
# True agents - reason and make decisions
- RAGAgent: Retriever + LLM + reasoning
- ReactAgent: LLM + tools + decision loop
- PlannerAgent: LLM + planning logic
- SupervisorAgent: LLM + agent coordination
```

**Characteristics:**
- MUST have reasoning capability (usually LLM)
- Combine multiple components
- Make decisions based on context
- Can plan and adapt behavior
- NEED AgentSchemaComposer for schema composition

## The Architecture Problem

### **Current Confusion**
```python
# WRONG - Retriever alone is not an agent!
class RetrieverAgent(Agent):
    engine: RetrieverEngine  # No reasoning capability!
    
# This leads to:
# - Unnecessary schema complexity
# - Incorrect use of AgentSchemaComposer
# - Type safety issues
```

### **Correct Architecture**
```python
# RIGHT - Retriever is just a component
class RetrieverNode(ExecutableNode):
    component: RetrieverEngine
    
# RIGHT - RAG Agent combines retriever + LLM
class RAGAgent(Agent):
    retriever: RetrieverEngine
    llm: LLMEngine  # This makes it an agent!
    
    def get_reasoning_engine(self) -> Engine:
        return self.llm  # Has reasoning capability
```

## Proposed Architecture

### **1. Clear Node Type Hierarchy**
```python
# Base node for any executable
class ExecutableNode(NodeConfig):
    """Base for any executable component in a graph."""
    
# Specific node types
class ComponentNode(ExecutableNode):
    """For simple components without reasoning."""
    component: Union[Retriever, Embeddings, VectorStore, Callable]
    
class AgentNode(ExecutableNode):
    """For true agents with reasoning capability."""
    agent: Agent  # Must have reasoning engine
    
    @model_validator(mode='after')
    def validate_has_reasoning(self):
        if not self.agent.has_reasoning_capability():
            raise ValueError(f"{self.agent.name} is not a true agent - no reasoning capability")
        return self
```

### **2. Agent Definition with Reasoning Requirement**
```python
class Agent(ABC):
    """True agent MUST have reasoning capability."""
    
    @abstractmethod
    def get_reasoning_engine(self) -> Engine:
        """Must return the primary reasoning engine (usually LLM)."""
        raise NotImplementedError
    
    def has_reasoning_capability(self) -> bool:
        """Check if this has reasoning capability."""
        try:
            engine = self.get_reasoning_engine()
            return engine.engine_type in [EngineType.LLM, EngineType.AGENT]
        except:
            return False
    
    def validate_agent_requirements(self) -> bool:
        """Validate this is actually an agent."""
        # Must have at least one reasoning engine
        reasoning_engines = [
            e for e in self.engines.values() 
            if e.engine_type in [EngineType.LLM, EngineType.AGENT]
        ]
        if not reasoning_engines:
            raise ValueError(f"{self.name} has no reasoning engines - not a true agent")
        return True
```

### **3. Different Schema Composition Strategies**
```python
class ComponentGraph(BaseGraph):
    """Graph of simple components - no agent complexity."""
    
    def build_schema(self):
        # Simple components use basic SchemaComposer
        components = [n.component for n in self.nodes if isinstance(n, ComponentNode)]
        self.state_schema = SchemaComposer.from_components(
            components=components,
            name=f"{self.name}State"
        )

class AgentGraph(BaseGraph):
    """Graph of true agents - needs sophisticated composition."""
    
    def build_schema(self):
        # True agents use AgentSchemaComposer
        agents = [n.agent for n in self.nodes if isinstance(n, AgentNode)]
        self.state_schema = AgentSchemaComposer.from_agents(
            agents=agents,
            name=f"{self.name}State",
            separation="smart",
            build_mode=BuildMode.SEQUENCE
        )
```

### **4. Factory Functions for Clarity**
```python
def create_component_node(component: Any, name: str) -> ComponentNode:
    """Create node for simple component."""
    if hasattr(component, 'engine_type'):
        if component.engine_type == EngineType.LLM:
            raise ValueError("LLM should be part of an Agent, not a standalone component")
    
    return ComponentNode(name=name, component=component)

def create_agent_node(agent: Agent, name: str) -> AgentNode:
    """Create node for true agent."""
    if not agent.has_reasoning_capability():
        raise ValueError(f"{agent.name} is not a true agent - use create_component_node instead")
    
    return AgentNode(name=name, agent=agent)
```

## Examples

### **Incorrect Usage (Current)**
```python
# WRONG - Treating retriever as agent
retriever_agent = SimpleAgent(engine=retriever_engine)  # No reasoning!
graph.add_node("retriever", retriever_agent)

# Leads to:
# - Unnecessary AgentSchemaComposer usage
# - Complex schema for simple retrieval
# - Confusion about what's an agent
```

### **Correct Usage (Proposed)**
```python
# RIGHT - Retriever as component
retriever_node = create_component_node(retriever_engine, "retriever")
graph.add_node("retriever", retriever_node)

# RIGHT - RAG as true agent
rag_agent = RAGAgent(
    retriever=retriever_engine,
    llm=llm_engine  # Reasoning capability!
)
rag_node = create_agent_node(rag_agent, "rag")
graph.add_node("rag", rag_node)
```

## Benefits

### **1. Conceptual Clarity**
- Clear distinction between components and agents
- No confusion about what needs reasoning capability
- Proper use of schema composition patterns

### **2. Simplified Architecture**
- Simple components don't need agent complexity
- AgentSchemaComposer only for true multi-agent scenarios
- Appropriate complexity for each use case

### **3. Better Type Safety**
- ComponentNode vs AgentNode distinction
- Validation ensures agents have reasoning
- Type checker can enforce correct usage

### **4. Performance**
- Simple components don't carry agent overhead
- Faster execution for basic operations
- Schema composition matches actual needs

## Migration Path

### **Phase 1: Add Component Types**
```python
# Add new node types without breaking existing
class ComponentNode(ExecutableNode): ...
class AgentNode(ExecutableNode): ...
```

### **Phase 2: Update Factory Functions**
```python
# Enhanced factory with type detection
def create_node(thing: Any, name: str) -> ExecutableNode:
    if isinstance(thing, Agent) and thing.has_reasoning_capability():
        return AgentNode(name=name, agent=thing)
    else:
        return ComponentNode(name=name, component=thing)
```

### **Phase 3: Migrate Existing Code**
```python
# Gradually update existing "agents" that are really components
# Old: SimpleAgent(engine=retriever)
# New: ComponentNode(component=retriever)
```

### **Phase 4: Enforce in New Code**
```python
# Require explicit choice in new code
# Must use either create_component_node or create_agent_node
# No ambiguous SimpleAgent with non-reasoning engines
```

## Conclusion

The key insight is that **an agent must have reasoning capability** - typically through an LLM. Simple executors like retrievers, embeddings, and vector stores are **components, not agents**. This distinction should be reflected in our architecture to avoid unnecessary complexity and ensure proper use of schema composition patterns.

By making this distinction clear, we can:
- Use appropriate complexity for each component type
- Apply AgentSchemaComposer only where truly needed
- Maintain better type safety and clearer architecture
- Improve performance by avoiding unnecessary overhead