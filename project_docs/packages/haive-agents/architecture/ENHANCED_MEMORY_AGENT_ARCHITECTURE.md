# Enhanced Long-Term Memory Agent Architecture

**Version**: 1.0
**Purpose**: Complete architecture guide for building enhanced memory agents with agentic RAG, handoffs, and multi-modal memory types
**Last Updated**: 2025-01-14

## 🧠 Overview

This document outlines the architecture for building sophisticated long-term memory agents that combine:

- **Agentic RAG**: Intelligent retrieval strategy selection
- **Agent Handoffs**: Tool-based agent delegation with Command patterns
- **Multi-Modal Memory**: Semantic, episodic, procedural + hidden memory types
- **Smart Routing**: Context-aware tool selection and delegation

## 🏗️ Core Architecture

### **Foundation: Agent-as-Tool Pattern**

```python
from typing import TypeVar, Generic, Union
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langgraph.types import Command
from haive.agents.base.agent import Agent

T = TypeVar('T', bound=Agent)

class GenericAgentTool(BaseModel, Generic[T]):
    """Generic agent-as-tool with proper input/output schemas."""

    agent_class: Type[T] = Field(..., description="Agent class to wrap")
    input_schema: Type[BaseModel] = Field(..., description="Input schema")
    output_schema: Type[BaseModel] = Field(..., description="Output schema")
    tool_name: str = Field(..., description="Tool identifier")
    handoff_mode: str = Field(default="return", description="return|command|handoff")

    def create_tool(self):
        """Create tool with proper schemas and handoff pattern."""

        if self.handoff_mode == "return":
            return self._create_return_tool()
        elif self.handoff_mode == "command":
            return self._create_command_tool()
        elif self.handoff_mode == "handoff":
            return self._create_handoff_tool()

    def _create_return_tool(self):
        """Agent-as-tool that returns response directly."""

        @tool(self.tool_name, args_schema=self.input_schema)
        def agent_tool(query: str) -> str:
            f"""Execute {self.agent_class.__name__} for query processing."""

            # Create agent instance
            agent = self.agent_class()

            # Execute with input schema validation
            validated_input = self.input_schema(query=query)
            result = agent.run(validated_input.model_dump())

            # Return response with output schema
            if isinstance(result, dict):
                output = self.output_schema(**result)
                return output.model_dump_json()

            return str(result)

        return agent_tool

    def _create_command_tool(self):
        """Agent-as-tool using Command handoff pattern."""

        @tool(self.tool_name, args_schema=self.input_schema)
        def command_tool(query: str) -> Command:
            f"""Delegate to {self.agent_class.__name__} using Command handoff."""

            return Command(
                goto=f"agent_{self.tool_name}",
                update={"query": query, "agent_context": self.tool_name}
            )

        return command_tool
```

### **Enhanced Memory Types Architecture**

```python
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class MemoryType(str, Enum):
    """Enhanced memory type classifications."""

    # Core memory types
    SEMANTIC = "semantic"           # Facts, concepts, knowledge triples
    EPISODIC = "episodic"          # Specific events, conversations, temporal context
    PROCEDURAL = "procedural"       # How-to knowledge, workflows, patterns

    # Hidden/Advanced memory types
    CONTEXTUAL = "contextual"       # Relationship mappings, social graphs
    PREFERENCE = "preference"       # User patterns, choices, behavioral tendencies
    META = "meta"                  # Memory about memory (self-awareness)
    EMOTIONAL = "emotional"         # Sentiment patterns, emotional context
    TEMPORAL = "temporal"          # Time-based patterns, recency weights

class MemoryEntry(BaseModel):
    """Enhanced memory entry with multi-modal classification."""

    content: str = Field(..., description="Memory content")
    memory_types: List[MemoryType] = Field(..., description="Memory type classifications")

    # Temporal metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_accessed: datetime = Field(default_factory=datetime.utcnow)
    access_count: int = Field(default=0)

    # Importance and decay
    importance: float = Field(default=0.5, ge=0.0, le=1.0)
    decay_rate: float = Field(default=0.1, ge=0.0, le=1.0)
    current_weight: float = Field(default=1.0, ge=0.0, le=1.0)

    # Relationships
    entity_relations: List[Dict[str, str]] = Field(default_factory=list)
    conversation_id: Optional[str] = Field(default=None)
    user_context: Dict[str, Any] = Field(default_factory=dict)

    # Quality metadata
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    source_quality: float = Field(default=1.0, ge=0.0, le=1.0)
    validation_status: str = Field(default="unverified")

class EnhancedMemoryStore(BaseModel):
    """Multi-modal memory store with intelligent organization."""

    memory_stores: Dict[MemoryType, Any] = Field(default_factory=dict)
    cross_references: Dict[str, List[str]] = Field(default_factory=dict)

    def setup_stores(self):
        """Initialize specialized stores for each memory type."""

        self.memory_stores = {
            MemoryType.SEMANTIC: KnowledgeGraphStore(),      # From document_modifiers/kg
            MemoryType.EPISODIC: TemporalVectorStore(),      # Time-weighted retrieval
            MemoryType.PROCEDURAL: StructuredProcedureStore(), # Workflow patterns
            MemoryType.CONTEXTUAL: RelationshipGraphStore(),   # Social/entity relationships
            MemoryType.PREFERENCE: PreferenceVectorStore(),    # User behavior patterns
            MemoryType.META: MetaMemoryStore(),              # Self-awareness
            MemoryType.EMOTIONAL: SentimentVectorStore(),    # Emotional context
            MemoryType.TEMPORAL: TimeSeriesStore()           # Temporal patterns
        }
```

### **Agentic RAG Integration**

```python
class AgenticRAGMemoryTool(BaseModel):
    """Agentic RAG agent as memory search tool."""

    rag_strategies: Dict[str, Any] = Field(default_factory=dict)
    memory_store: EnhancedMemoryStore = Field(...)

    def setup_rag_strategies(self):
        """Setup different RAG strategies for different memory types."""

        self.rag_strategies = {
            "semantic_search": SimpleRAGAgent(retriever=self.memory_store.memory_stores[MemoryType.SEMANTIC]),
            "episodic_recall": HyDERAGAgent(retriever=self.memory_store.memory_stores[MemoryType.EPISODIC]),
            "procedural_lookup": MultiQueryRAGAgent(retriever=self.memory_store.memory_stores[MemoryType.PROCEDURAL]),
            "contextual_mapping": FusionRAGAgent(retriever=self.memory_store.memory_stores[MemoryType.CONTEXTUAL]),
            "preference_analysis": AdaptiveRAGAgent(retriever=self.memory_store.memory_stores[MemoryType.PREFERENCE]),
            "meta_reflection": FLARERAGAgent(retriever=self.memory_store.memory_stores[MemoryType.META])
        }

    def create_agentic_memory_tool(self):
        """Create agentic RAG tool with intelligent strategy selection."""

        @tool("agentic_memory_search")
        def agentic_memory_search(query: str) -> str:
            """Intelligent memory search using agentic RAG routing.

            Analyzes query intent and selects optimal retrieval strategy:
            - Factual questions → semantic search
            - Personal history → episodic recall
            - How-to queries → procedural lookup
            - Relationship questions → contextual mapping
            - Preference queries → preference analysis
            - Self-reflection → meta memory
            """

            # Analyze query to determine memory types and strategy
            query_analysis = self._analyze_query_intent(query)

            # Select optimal RAG strategy based on analysis
            strategy_name = self._select_rag_strategy(query_analysis)
            rag_agent = self.rag_strategies[strategy_name]

            # Execute RAG with selected strategy
            result = rag_agent.run(query)

            # Cross-reference with related memory types
            enriched_result = self._enrich_with_cross_references(result, query_analysis)

            return f"Memory search ({strategy_name}): {enriched_result}"

        return agentic_memory_search

    def _analyze_query_intent(self, query: str) -> Dict[str, Any]:
        """Analyze query to determine memory types and complexity."""

        # Simple keyword-based analysis (can be enhanced with LLM)
        intent = {
            "memory_types": [],
            "complexity": "simple",
            "temporal_scope": "recent",
            "requires_reasoning": False
        }

        query_lower = query.lower()

        # Classify memory types needed
        if any(kw in query_lower for kw in ["fact", "definition", "what is", "who is"]):
            intent["memory_types"].append(MemoryType.SEMANTIC)

        if any(kw in query_lower for kw in ["remember", "discussion", "conversation", "when did"]):
            intent["memory_types"].append(MemoryType.EPISODIC)

        if any(kw in query_lower for kw in ["how to", "process", "steps", "procedure"]):
            intent["memory_types"].append(MemoryType.PROCEDURAL)

        if any(kw in query_lower for kw in ["relationship", "connected", "related to"]):
            intent["memory_types"].append(MemoryType.CONTEXTUAL)

        if any(kw in query_lower for kw in ["prefer", "like", "favorite", "usually"]):
            intent["memory_types"].append(MemoryType.PREFERENCE)

        if any(kw in query_lower for kw in ["think about", "understand", "know about"]):
            intent["memory_types"].append(MemoryType.META)

        return intent

    def _select_rag_strategy(self, query_analysis: Dict[str, Any]) -> str:
        """Select optimal RAG strategy based on query analysis."""

        memory_types = query_analysis["memory_types"]

        # Simple strategy selection logic
        if MemoryType.SEMANTIC in memory_types:
            return "semantic_search"
        elif MemoryType.EPISODIC in memory_types:
            return "episodic_recall"
        elif MemoryType.PROCEDURAL in memory_types:
            return "procedural_lookup"
        elif MemoryType.CONTEXTUAL in memory_types:
            return "contextual_mapping"
        elif MemoryType.PREFERENCE in memory_types:
            return "preference_analysis"
        elif MemoryType.META in memory_types:
            return "meta_reflection"
        else:
            return "semantic_search"  # Default fallback
```

### **Smart Tool Routing with Memory Context**

```python
class MemoryEnhancedReactAgent(BaseModel):
    """React agent with intelligent memory-aware tool routing."""

    base_agent: Agent = Field(...)
    memory_tool: AgenticRAGMemoryTool = Field(...)
    web_search_tool: Any = Field(...)
    research_tools: List[Any] = Field(default_factory=list)

    def create_smart_routing_agent(self):
        """Create agent with memory-aware tool routing."""

        # Setup all tools
        tools = [
            self.memory_tool.create_agentic_memory_tool(),
            self.web_search_tool,
            *self.research_tools
        ]

        # Enhanced system message for smart routing
        system_message = self._create_memory_aware_system_message()

        # Create ReactAgent with memory context
        if hasattr(self.base_agent, 'tools'):
            self.base_agent.tools = tools
        if hasattr(self.base_agent, 'system_message'):
            self.base_agent.system_message = system_message

        return self.base_agent

    def _create_memory_aware_system_message(self) -> str:
        """Create system message with memory-aware routing logic."""

        return """You are an intelligent assistant with enhanced memory capabilities.

**MEMORY-FIRST APPROACH:**
1. **Always check memory first** before searching externally
2. **Cross-reference memory types** for comprehensive understanding
3. **Use web search only** when memory is insufficient
4. **Update memory** with new information learned

**TOOL ROUTING LOGIC:**

**agentic_memory_search** - Use for:
- Questions about previous conversations
- Personal information and preferences
- Learned facts and procedures
- Relationship and contextual information
- Self-reflection and meta-knowledge

**web_search** - Use when:
- Memory search returns insufficient results
- Need current/recent information not in memory
- Factual verification of memory contents
- Exploring new topics not previously encountered

**MEMORY TYPES AWARENESS:**
- **Semantic**: Facts, definitions, knowledge
- **Episodic**: Personal conversations, events
- **Procedural**: How-to knowledge, workflows
- **Contextual**: Relationships, connections
- **Preference**: User patterns, likes/dislikes
- **Meta**: Self-awareness, learning patterns

**WORKFLOW:**
1. Analyze query for memory type requirements
2. Search relevant memory with agentic_memory_search
3. Evaluate completeness of memory results
4. If insufficient, supplement with web_search
5. Synthesize memory + external information
6. Provide comprehensive, memory-informed response

Always prioritize memory-informed responses and mention the source of information."""
```

### **Command Handoff Integration**

```python
class HandoffCapableMemoryAgent(BaseModel):
    """Memory agent with Command-based handoff capabilities."""

    memory_agent: Any = Field(...)
    research_agent: Any = Field(...)
    analysis_agent: Any = Field(...)

    def create_handoff_tools(self):
        """Create tools that use Command handoff pattern."""

        @tool("delegate_to_research")
        def delegate_to_research(query: str) -> Command:
            """Delegate complex research tasks to specialized research agent."""
            return Command(
                goto="research_agent",
                update={
                    "query": query,
                    "context": "delegated_from_memory_agent",
                    "memory_context": self._get_memory_context(query)
                }
            )

        @tool("delegate_to_analysis")
        def delegate_to_analysis(data: str) -> Command:
            """Delegate analysis tasks to specialized analysis agent."""
            return Command(
                goto="analysis_agent",
                update={
                    "data": data,
                    "analysis_type": "memory_informed",
                    "memory_context": self._get_memory_context(data)
                }
            )

        return [delegate_to_research, delegate_to_analysis]

    def _get_memory_context(self, query: str) -> Dict[str, Any]:
        """Get relevant memory context for handoff."""

        # Quick memory lookup to provide context
        memory_results = self.memory_agent.memory_tool.create_agentic_memory_tool().invoke(query)

        return {
            "relevant_memories": memory_results,
            "user_preferences": self._get_user_preferences(),
            "conversation_context": self._get_conversation_context()
        }
```

## 🚀 Implementation Roadmap

### **Phase 1: Foundation**

1. ✅ **Basic Store Tools** - Working memory storage (COMPLETED)
2. **Generic Agent-as-Tool Factory** - Reusable pattern
3. **Enhanced Memory Types** - Multi-modal classification
4. **Basic Agentic RAG** - Simple strategy selection

### **Phase 2: Intelligence**

1. **Smart Tool Routing** - Context-aware delegation
2. **Cross-Reference System** - Memory type interconnections
3. **Command Handoff Integration** - Agent delegation patterns
4. **Quality Metrics** - Memory reliability and relevance

### **Phase 3: Advanced Features**

1. **Time-Weighted Retrieval** - Importance decay and recency
2. **Knowledge Graph Integration** - Entity-relationship memory
3. **Self-Organizing Taxonomy** - TNT-based categorization
4. **Meta-Memory Capabilities** - Self-awareness and learning

### **Phase 4: Production**

1. **Performance Optimization** - Caching and indexing
2. **Scalability Patterns** - Multi-user and high-volume
3. **Security and Privacy** - Memory isolation and protection
4. **Monitoring and Analytics** - Memory usage insights

## 🎯 Key Design Principles

1. **Memory-First Architecture**: Always check memory before external sources
2. **Agentic Intelligence**: Let agents decide optimal retrieval strategies
3. **Handoff Clarity**: Use Command patterns for clean agent delegation
4. **Type Safety**: Proper Pydantic schemas throughout
5. **Composability**: Reusable patterns and generic implementations
6. **Real Components**: No mocks, test with actual LLMs and tools

## 📊 Success Metrics

- **Response Quality**: >90% relevance for memory-based queries
- **Retrieval Speed**: <2s for memory searches, <10s for complex queries
- **Memory Accuracy**: >95% factual accuracy in stored information
- **Strategy Selection**: >80% optimal strategy selection by agentic router
- **Handoff Efficiency**: <500ms overhead for agent delegation

---

**Next Steps**: Begin with Phase 1 implementation, focusing on the generic agent-as-tool factory and enhanced memory type classification.
