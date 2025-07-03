# Agent Architecture Overview

## Overview

The haive-agents package implements a sophisticated agent architecture built on top of LangGraph, providing multiple abstraction levels and composition patterns for building AI agents.

## Core Architecture Components

### Base Agent Class (`/src/haive/agents/base/agent.py`)

The foundation for all agents in the system:

```python
class Agent:
    """Base agent class providing core functionality"""
    - State management through Pydantic models
    - Workflow setup and execution
    - Integration with LangGraph
    - Extensible architecture
```

### Agent Registration System

Agents are registered using decorators:
```python
@register_agent(ConfigClass)
class MyAgent(Agent[ConfigClass]):
    """Custom agent implementation"""
```

## Agent Hierarchy

### 1. Base Level Agents

**Agent** (Abstract Base)
- Core agent functionality
- State management
- Workflow orchestration

**SimpleAgent**
- Single-task execution
- Direct LLM integration
- Minimal state management

### 2. Composition Patterns

**SequentialAgent**
- Execute agents in sequence
- Pass state between agents
- Pipeline workflows

**ParallelAgent**
- Execute agents concurrently
- Merge results
- Performance optimization

**ConditionalAgent**
- Conditional execution paths
- Dynamic routing
- Decision trees

**MultiAgent**
- Combines sequential, parallel, and conditional
- Complex workflows
- Advanced orchestration

### 3. Specialized Agents

**ChainAgent**
- Simplified sequential workflows
- Reduced boilerplate
- Quick prototyping

**RAG Agents**
- Retrieval-augmented generation
- Multiple strategies
- Document processing

**Document Agents**
- Document pipeline processing
- Format handling
- Metadata extraction

## State Management

### State Schema Pattern

All agents use Pydantic models for state:

```python
class RAGState(BaseModel):
    query: str
    retrieved_documents: List[Document] = []
    answer: str = ""
    metadata: Dict[str, Any] = {}
```

### State Flow
1. Initial state creation
2. State updates through nodes
3. State persistence
4. State merging (for parallel execution)

## Workflow Patterns

### 1. Graph-Based Workflows

Using LangGraph's StateGraph:
```python
def setup_workflow(self):
    gb = DynamicGraph(state_schema=self.state_schema)
    gb.add_node("retrieve", self.retrieve)
    gb.add_node("generate", self.generate)
    gb.add_edge(START, "retrieve")
    gb.add_edge("retrieve", "generate")
    gb.add_edge("generate", END)
    self.graph = gb.build()
```

### 2. Node Types

**Engine Nodes**
- Integrate with haive engines
- Document processing
- LLM operations

**Function Nodes**
- Custom logic
- State transformations
- External integrations

**Conditional Nodes**
- Routing decisions
- Branch selection
- Dynamic paths

### 3. Edge Types

**Direct Edges**
- Simple transitions
- Linear flow

**Conditional Edges**
- Based on state
- Dynamic routing

**Parallel Edges**
- Fan-out patterns
- Concurrent execution

## Configuration System

### Config Classes

Each agent type has a configuration class:

```python
class BaseRAGConfig(BaseModel):
    retriever_engine: RetrieverEngineConfig
    engine: AugLLMConfig
    max_documents: int = 10
```

### Engine Integration

Agents integrate with haive engines:
- **LLM Engine**: Language model operations
- **Document Engine**: Document processing
- **Retriever Engine**: Vector search
- **Embedding Engine**: Generate embeddings

## Multi-Agent Patterns

### Sequential Execution
```
Agent1 → Agent2 → Agent3
```

### Parallel Execution
```
     → Agent1 →
    ↗          ↘
Start            → Merge → End
    ↘          ↗
     → Agent2 →
```

### Conditional Routing
```
         → Agent1 (if condition A)
        ↗
Start → Router
        ↘
         → Agent2 (if condition B)
```

### Complex Workflows
Combination of all patterns with nested structures

## Factory Patterns

### Unified Factory
Single interface for creating agents:
```python
agent = create_agent(
    agent_type="rag",
    strategy="hyde",
    documents=docs,
    config=config
)
```

### Collection Pattern
Grouped agent creation:
```python
collection = RAGChainCollection()
agent = collection.create_fusion_rag(docs, llm_config)
```

## Extension Points

### 1. Custom Agents
- Inherit from base Agent
- Implement required methods
- Register with decorator

### 2. Custom Nodes
- Define node functions
- Add to workflow
- Handle state updates

### 3. Custom State
- Extend base state models
- Add domain-specific fields
- Maintain compatibility

### 4. Custom Engines
- Implement engine interface
- Integrate with agents
- Extend capabilities

## Best Practices

### 1. State Design
- Keep state minimal
- Use structured types
- Document fields
- Version state schemas

### 2. Error Handling
- Implement retry logic
- Graceful degradation
- Comprehensive logging
- State recovery

### 3. Performance
- Use parallel execution
- Optimize state updates
- Cache when possible
- Profile workflows

### 4. Testing
- Unit test nodes
- Integration test workflows
- Mock external services
- Test error paths

## Common Patterns

### 1. Retrieval Pattern
```
Query → Retrieve → Filter → Rank → Return
```

### 2. Generation Pattern
```
Context → Prompt → Generate → Validate → Return
```

### 3. Processing Pattern
```
Load → Transform → Chunk → Embed → Store
```

### 4. Routing Pattern
```
Analyze → Classify → Route → Execute → Merge
```

## Integration with LangGraph

### StateGraph Usage
- Define state schema
- Add nodes and edges
- Compile to runnable
- Execute with invoke/stream

### Command Pattern
Updates state through Command objects:
```python
return Command(update={"field": value})
```

### Checkpoint Support
- State persistence
- Resume capabilities
- History tracking

## Debugging and Monitoring

### 1. State Inspection
- Print state at nodes
- Log transitions
- Track updates

### 2. Graph Visualization
- Export graph structure
- Visualize flow
- Identify bottlenecks

### 3. Performance Metrics
- Node execution time
- State update cost
- Memory usage

### 4. Error Tracking
- Exception handling
- Error state capture
- Recovery mechanisms