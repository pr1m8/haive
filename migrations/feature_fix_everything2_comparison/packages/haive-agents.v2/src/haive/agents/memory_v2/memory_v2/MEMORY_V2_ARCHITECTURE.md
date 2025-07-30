# Memory V2 Architecture - Complete Implementation Plan

**Version**: 2.0  
**Status**: In Development  
**Last Updated**: 2025-01-21  
**Purpose**: Complete memory system rebuild following proper Haive patterns with token tracking and summarization

## 🎯 Overview

Memory V2 is a complete rebuild of Haive's memory system addressing critical architectural issues in the current implementation. This version follows proper Haive patterns with V3 Enhanced Agents, real component testing, and token-aware memory management.

## 🔍 Research & Analysis Summary

### Current Problems Identified

1. **Architectural Violations**
   - `unified_memory_api.py` - 1,357 lines violating single responsibility
   - Wrong inheritance patterns (SimpleRAG inherits from MultiAgent)
   - Overriding `__init__` in Pydantic models
   - Mixed concerns in single agents

2. **Memory Implementation Issues**
   - No clear memory model or type system
   - Storage abstraction mixed with processing logic
   - Multiple overlapping implementations
   - No token tracking or context management

3. **Pattern Violations**
   - Using mocks in tests
   - Agent-as-function anti-pattern
   - Complex state tracking instead of StateSchema
   - Tools mixed with agent logic

### Working Components to Leverage

1. **✅ BaseRAGAgent** - Correctly implemented with RetrieverMixin
2. **✅ Neo4j Graph DB RAG** - Production-ready Cypher generation
3. **✅ KG Transformers** - Document-to-knowledge-graph conversion
4. **✅ Reflection System** - Multi-agent reflection patterns
5. **✅ LangMem Integration** - Tests show working implementation

### Research References

- **LangMem/MemGPT Patterns** (2025)
  - Three memory types: Semantic, Episodic, Procedural
  - Hot path vs background processing
  - Memory scoping with namespaces
  - LangMem SDK with native LangGraph integration

- **LangGraph Memory Concepts**
  - Short-term memory via thread-scoped checkpoints
  - Long-term memory via stores
  - Memory persistence across conversations
  - Token usage tracking for context management

## 🏗️ Architecture Design

### Core Design Principles

1. **Token-Aware Memory Management**
   - Track token usage for all memory operations
   - Automatic summarization when approaching context limits
   - Memory rewriting for efficient storage
   - Context window optimization

2. **V3 Enhanced Agent Pattern**
   - All agents inherit from EnhancedSimpleAgent
   - Proper Pydantic configuration
   - Real component testing (no mocks)
   - Tool-first approach

3. **Prebuilt State with Token Tracking**
   - Use MessagesState with token tracking
   - Automatic threshold monitoring
   - Trigger summarization/rewriting when needed
   - Maintain conversation continuity

### Memory Types Implementation

```python
# Based on LangMem/MemGPT patterns
class MemoryType(str, Enum):
    SEMANTIC = "semantic"        # Facts, knowledge, preferences
    EPISODIC = "episodic"        # Past events, experiences
    PROCEDURAL = "procedural"    # How-to, learned behaviors
    CONTEXTUAL = "contextual"    # Current context information
    PREFERENCE = "preference"    # User preferences
    META = "meta"               # Memory about memories
```

### Token Management Strategy

```python
class TokenAwareMemoryConfig(BaseModel):
    """Configuration for token-aware memory management."""

    max_context_tokens: int = Field(default=8000)
    summarization_threshold: float = Field(default=0.8)  # 80% of max
    rewrite_threshold: float = Field(default=0.9)       # 90% of max

    summarization_strategy: str = Field(
        default="progressive",
        pattern="^(progressive|aggressive|selective)$"
    )

    memory_compression_ratio: float = Field(
        default=0.3,  # Target 30% of original size
        ge=0.1,
        le=0.8
    )
```

## 📦 Implementation Components

### 1. SimpleMemoryAgent (Core Foundation)

```python
from haive.agents.simple.enhanced_agent_v3 import EnhancedSimpleAgent
from haive.core.schema.prebuilt.messages_state import MessagesState

class SimpleMemoryAgent(EnhancedSimpleAgent):
    """Memory agent with token tracking and automatic summarization.

    Features:
    - Token-aware memory storage
    - Automatic summarization on threshold
    - Memory type classification
    - Efficient retrieval with caching
    """

    memory_config: TokenAwareMemoryConfig = Field(default_factory=TokenAwareMemoryConfig)
    token_tracker: TokenTracker = Field(default_factory=TokenTracker)

    def setup_agent(self) -> None:
        """Setup with token tracking and summarization tools."""
        super().setup_agent()

        # Add memory tools
        self.engine.tools.extend([
            store_memory,
            retrieve_memory,
            search_memory,
            classify_memory,
            summarize_memories,
            rewrite_memory
        ])

        # Enable token tracking
        self.engine.track_tokens = True
        self.engine.token_callback = self.token_tracker.track
```

### 2. Memory Tools with Token Awareness

```python
@tool
def summarize_memories(
    memories: List[MemoryEntry],
    target_tokens: int,
    preserve_important: bool = True
) -> str:
    """Summarize memories to fit within token limit.

    Uses progressive summarization to maintain key information
    while reducing token usage.
    """

@tool
def rewrite_memory(
    memory: MemoryEntry,
    compression_ratio: float = 0.3
) -> MemoryEntry:
    """Rewrite memory for efficient storage.

    Maintains semantic meaning while reducing tokens.
    """
```

### 3. TokenTracker Component

```python
class TokenTracker(BaseModel):
    """Track token usage across memory operations."""

    total_tokens: int = 0
    tokens_by_operation: Dict[str, int] = Field(default_factory=dict)

    # Thresholds and alerts
    warning_threshold: float = 0.7
    critical_threshold: float = 0.85

    def track(self, operation: str, tokens: int) -> None:
        """Track tokens for an operation."""
        self.total_tokens += tokens
        self.tokens_by_operation[operation] = (
            self.tokens_by_operation.get(operation, 0) + tokens
        )

    def check_thresholds(self, max_tokens: int) -> str:
        """Check if approaching token limits."""
        ratio = self.total_tokens / max_tokens

        if ratio >= self.critical_threshold:
            return "CRITICAL"
        elif ratio >= self.warning_threshold:
            return "WARNING"
        return "OK"
```

### 4. Memory State with Token Tracking

```python
from haive.core.schema.prebuilt.messages_state_with_token_tracking import MessagesStateWithTokenTracking

class TokenAwareMemoryState(MessagesStateWithTokenTracking):
    """Memory state with automatic token management."""

    # Memory-specific fields
    current_memories: List[MemoryEntry] = Field(default_factory=list)
    memory_summary: Optional[str] = None
    summarization_history: List[Dict[str, Any]] = Field(default_factory=list)

    # Token tracking
    memory_token_usage: Dict[str, int] = Field(default_factory=dict)
    last_summarization_tokens: int = 0

    def should_summarize(self) -> bool:
        """Check if summarization needed based on token usage."""
        if self.total_tokens > self.token_limit * 0.8:
            return True
        return False

    def should_rewrite(self) -> bool:
        """Check if memory rewriting needed."""
        if self.total_tokens > self.token_limit * 0.9:
            return True
        return False
```

### 5. Graph Structure with Summarization

```python
def build_graph(self) -> BaseGraph:
    """Build graph with token-aware memory management."""
    graph = BaseGraph(name=f"{self.name}_graph")

    # Main memory node
    graph.add_node("memory_node", self.process_memory)

    # Token check node
    graph.add_node("token_check", self.check_token_usage)

    # Summarization node
    graph.add_node("summarize", self.summarize_memories_node)

    # Rewrite node
    graph.add_node("rewrite", self.rewrite_memories_node)

    # Conditional routing based on token usage
    graph.add_conditional_edges(
        "memory_node",
        self.route_by_token_usage,
        {
            "ok": "token_check",
            "summarize": "summarize",
            "rewrite": "rewrite"
        }
    )

    return graph
```

## 🧪 Testing Strategy

### Incremental Testing with Real Components

```python
def test_memory_with_token_tracking():
    """Test memory storage with token awareness."""
    agent = SimpleMemoryAgent(
        name="test_memory",
        memory_config=TokenAwareMemoryConfig(
            max_context_tokens=1000,
            summarization_threshold=0.8
        )
    )

    # Store memories until approaching limit
    for i in range(10):
        result = agent.run(f"Remember fact {i}: This is a test memory")

    # Check token tracking
    assert agent.token_tracker.total_tokens > 0
    assert agent.state.should_summarize()

    # Trigger summarization
    result = agent.run("What do you remember?")
    assert "summarized" in result.lower()

def test_memory_rewriting():
    """Test automatic memory rewriting."""
    # Test compression while maintaining meaning
    memory = MemoryEntry(
        content="Alice works at OpenAI as a senior researcher...",
        metadata=MemoryMetadata(importance="high")
    )

    rewritten = rewrite_memory(memory, compression_ratio=0.3)
    assert len(rewritten.content) < len(memory.content) * 0.4
```

## 🚀 Implementation Plan

### Phase 1: Core Foundation ✅ (In Progress)

- [x] Memory state schema with token tracking
- [x] Basic memory tools (store, retrieve, search, classify)
- [ ] SimpleMemoryAgent with V3 pattern
- [ ] Token tracker component
- [ ] Basic tests with real LLMs

### Phase 2: Token Management

- [ ] Summarization tools and strategies
- [ ] Memory rewriting for compression
- [ ] Token-aware graph routing
- [ ] Threshold monitoring and alerts
- [ ] Progressive summarization tests

### Phase 3: Advanced Memory Agents

- [ ] GraphMemoryAgent with Neo4j
- [ ] RAGMemoryAgent with LangMem
- [ ] ReflectiveMemoryAgent
- [ ] Memory type-specific strategies
- [ ] Integration tests

### Phase 4: Multi-Strategy Coordination

- [ ] MultiMemoryAgent coordinator
- [ ] Intelligent routing by memory type
- [ ] Performance optimization
- [ ] End-to-end workflows
- [ ] Production deployment guide

## 📊 Success Metrics

1. **Token Efficiency**
   - Maintain <8K tokens for active context
   - Achieve 30% compression without semantic loss
   - <100ms for summarization operations

2. **Memory Quality**
   - > 90% accuracy in memory classification
   - > 85% relevance in retrieval
   - Maintain important memories through summarization

3. **Performance**
   - <50ms memory storage operations
   - <100ms retrieval with caching
   - Support 100K+ memories per namespace

4. **Developer Experience**
   - Simple API following Haive patterns
   - Comprehensive testing suite
   - Clear documentation and examples

## 🔗 References

### Internal Haive Components

- `/packages/haive-agents/src/haive/agents/simple/enhanced_agent_v3.py` - Base V3 pattern
- `/packages/haive-agents/src/haive/agents/rag/base/agent.py` - Correct RAG pattern
- `/packages/haive-agents/src/haive/agents/reflection/multi_agent_reflection.py` - Reflection patterns
- `/packages/haive-core/src/haive/core/schema/prebuilt/messages_state.py` - Base state

### External Resources

- [LangMem SDK Documentation](https://langchain-ai.github.io/langmem/)
- [LangGraph Memory Concepts](https://langchain-ai.github.io/langgraph/concepts/memory/)
- [DeepLearning.AI Long-Term Memory Course](https://www.deeplearning.ai/short-courses/long-term-agentic-memory-with-langgraph/)

### Research Papers

- MemGPT: Towards LLMs as Operating Systems
- CoALA: Cognitive Architectures for Language Agents
- Long-Term Memory for AI Agents (LangChain 2025)

## 🎯 Next Steps

1. **Complete SimpleMemoryAgent** with token tracking
2. **Implement summarization tools** with different strategies
3. **Add token-aware routing** to the graph
4. **Test with real scenarios** approaching token limits
5. **Build specialized memory agents** for different use cases

The key innovation is **automatic token management** - the system monitors token usage and proactively summarizes or rewrites memories to stay within context limits while preserving important information.
