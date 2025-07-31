# GenericAgent Confusion & CompiledStateGraph Alternative

## Current GenericAgent Issues

### 1. **Overcomplicated Generic System**

**Location**: `packages/haive-agents/src/haive/agents/base/generic_agent.py`

```python
# GenericAgent[TInput, TOutput, TState] - TOO COMPLEX
class GenericAgent(Agent[TInput, TOutput, TState]):
    """Generic typing that nobody uses"""
    # Auto-configuration with __init_subclass__
    # Universal adapter compatibility
    # Agent chaining compatibility checks
    # Factory functions for dynamic creation
```

**Problems**:

- ✅ Fully implemented but **zero usage** in codebase
- ❌ Adds generic complexity without clear benefits
- ❌ Another "Agent" when we need **fewer** agent types
- ❌ Competes with SimpleAgent for basic use cases

### 2. **What GenericAgent Actually Is**

Looking at the implementation, GenericAgent is essentially:

- A **type-safe wrapper** around Agent
- An **adapter system** for input/output conversion
- A **factory** for creating agent classes dynamically

**But this is NOT what we need more of!**

## The Real Need: CompiledStateGraph Pattern

### What You're Describing

```python
# Instead of "Agent" for everything, we need:
CompiledStateGraph  # LangGraph execution unit
├── Agent           # LLM-based reasoning only
├── Component       # Deterministic processing
├── Workflow        # Multi-step orchestration
└── Pipeline        # Linear data processing
```

### Current Misclassification Problem

```python
# These are NOT agents, they're CompiledStateGraphs:
class DocumentAgent(Agent):        # Should be: DocumentPipeline
class BaseRAGAgent(Agent):         # Should be: RAGComponent
class DocumentLoaderAgent(Agent):  # Should be: LoaderComponent
class EmbeddingAgent(Agent):       # Should be: EmbeddingComponent
class RetrieverAgent(Agent):       # Should be: RetrieverComponent
```

## Proposed Clear Hierarchy

### 1. **CompiledStateGraph Base**

```python
class CompiledStateGraph(BaseModel):
    """Base for anything that can be compiled to a LangGraph"""
    name: str
    state_schema: type[StateSchema]

    @abstractmethod
    def build_graph(self) -> BaseGraph:
        """All graph-able things implement this"""
        pass

    def compile(self) -> CompiledGraph:
        """Common compilation logic"""
        return self.build_graph().compile()
```

### 2. **True Agent (LLM-based reasoning only)**

```python
class Agent(CompiledStateGraph):
    """Agents have LLM engines and can reason/use tools"""
    engine: LLMEngine | AugLLMConfig = Field(...)  # Must be LLM!
    tools: list[Tool] = Field(default_factory=list)

    def reason(self, input_data: Any) -> Any:
        """Agents can reason about problems"""
        pass
```

**Examples**:

- `SimpleAgent` - Single LLM reasoning
- `ReactAgent` - LLM + tool use + reasoning loop
- `ConversationalAgent` - LLM + conversation memory

### 3. **Component (Deterministic processing)**

```python
class Component(CompiledStateGraph):
    """Components do deterministic processing"""

    def process(self, input_data: Any) -> Any:
        """Components transform data predictably"""
        pass
```

**Examples**:

- `RetrieverComponent` - Document retrieval
- `EmbeddingComponent` - Text embeddings
- `LoaderComponent` - Data loading
- `TransformerComponent` - Data transformation

### 4. **Pipeline (Linear processing)**

```python
class Pipeline(CompiledStateGraph):
    """Pipelines chain components linearly"""
    components: list[Component] = Field(...)

    def build_graph(self) -> BaseGraph:
        """Create linear component chain"""
        pass
```

**Examples**:

- `DocumentPipeline` - FETCH → LOAD → TRANSFORM → SPLIT → EMBED → STORE
- `RAGPipeline` - RETRIEVE → RANK → FILTER → GENERATE
- `ProcessingPipeline` - Custom component chains

### 5. **Workflow (Complex orchestration)**

```python
class Workflow(CompiledStateGraph):
    """Workflows orchestrate agents, components, and pipelines"""
    participants: list[Agent | Component | Pipeline] = Field(...)
    execution_pattern: ExecutionPattern = Field(...)

    def build_graph(self) -> BaseGraph:
        """Create complex orchestration graph"""
        pass
```

**Examples**:

- `MultiAgentWorkflow` - Coordinate multiple reasoning agents
- `RAGWorkflow` - Retrieval + reasoning + validation
- `DocumentWorkflow` - Document processing + analysis + storage

## Migration Strategy

### Phase 1: Rename Misclassified "Agents"

```python
# Before (CONFUSING):
from haive.agents import DocumentAgent, BaseRAGAgent

# After (CLEAR):
from haive.pipelines import DocumentPipeline
from haive.components import RetrieverComponent
```

### Phase 2: Remove GenericAgent

```python
# GenericAgent adds no value - remove it
# Existing functionality moves to:
# - Type safety → Pydantic models
# - Adapters → Conversion utilities
# - Factories → Component/Pipeline/Workflow factories
```

### Phase 3: Clear Import Structure

```python
# Clear module organization:
from haive.agents import SimpleAgent, ReactAgent, ConversationalAgent
from haive.components import RetrieverComponent, EmbeddingComponent
from haive.pipelines import DocumentPipeline, RAGPipeline
from haive.workflows import MultiAgentWorkflow, DocumentWorkflow
```

## Benefits of Clear Hierarchy

### 1. **Conceptual Clarity**

```python
# CLEAR: What does this do?
document_pipeline = DocumentPipeline.from_directory("/docs")  # Processes documents
retriever = RetrieverComponent.from_vectorstore(store)       # Retrieves data
reasoning_agent = SimpleAgent(engine=llm_config)             # Reasons with LLM

# vs CONFUSING: What does this do?
document_agent = DocumentAgent(...)    # Processes? Reasons? Both?
rag_agent = BaseRAGAgent(...)         # Retrieves? Reasons? Both?
generic_agent = GenericAgent[T,U,V]() # ??? Too abstract
```

### 2. **Appropriate Capabilities**

```python
# Agents get agent capabilities:
agent.reason(problem)           # ✅ Makes sense
agent.use_tools(tool_calls)     # ✅ Makes sense
agent.conversation_memory       # ✅ Makes sense

# Components get component capabilities:
component.process(data)         # ✅ Makes sense
component.batch_process(items)  # ✅ Makes sense
component.validate_input(data)  # ✅ Makes sense

# NOT:
component.reason(problem)       # ❌ Components don't reason
agent.batch_process(items)      # ❌ Agents aren't optimized for bulk processing
```

### 3. **Performance Optimization**

```python
# Components can be optimized for throughput:
class RetrieverComponent:
    async def batch_retrieve(self, queries: list[str]):
        # Optimized for bulk operations

# Agents optimized for reasoning:
class SimpleAgent:
    async def reason_about(self, problem: Problem):
        # Optimized for LLM reasoning chains
```

### 4. **Correct Schema Composition**

```python
# Use appropriate composer for each type:
AgentSchemaComposer.from_agents(agents)           # LLM coordination
ComponentSchemaComposer.from_components(components) # Data flow
PipelineSchemaComposer.from_steps(steps)          # Linear processing
WorkflowSchemaComposer.from_mixed(participants)   # Complex orchestration
```

## Summary

**Remove GenericAgent entirely** - it adds complexity without clear benefits.

**Create clear hierarchy**:

- **Agent** = LLM reasoning capability
- **Component** = Deterministic processing
- **Pipeline** = Linear component chains
- **Workflow** = Complex orchestration

**All inherit from CompiledStateGraph** - the real common interface.

This resolves the "everything is an agent" problem and provides clear guidance on what to use when.
