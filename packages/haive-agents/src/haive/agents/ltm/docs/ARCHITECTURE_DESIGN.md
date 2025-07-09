# LTM Architecture Design (Corrected for Haive Patterns)

## Overview

This document outlines the Long-Term Memory (LTM) system architecture that properly follows Haive's agent patterns while incorporating LangMem's proven memory management capabilities.

## Core Architecture Principles

### 1. Agent-Centric Design

- **LTMAgent**: Main agent following `Agent[LTMAgentConfig]` pattern
- **Engine Composition**: Memory processing via dedicated engines
- **Graph Workflows**: BaseGraph-based processing pipelines
- **Mixin Integration**: Leverage existing ExecutionMixin, StateMixin, etc.

### 2. LangMem Compatibility

- **Tool Patterns**: Adapt `create_manage_memory_tool` and `create_search_memory_tool`
- **Storage Patterns**: Use LangMem's namespace and store integration
- **Processing Patterns**: Memory extraction, consolidation, optimization

### 3. Haive Component Reuse

- **KG Extraction**: Leverage existing IterativeGraphTransformer
- **TNT Categorization**: Use TaxonomyAgent for memory organization
- **Iterative Summarization**: Memory consolidation via IterativeSummarizer
- **Message Transformation**: Enhanced reflection and agent communication

## Component Architecture

### Core Components Structure

```
haive-agents/src/haive/agents/ltm/
├── __init__.py                    # Public API
├── agent.py                      # LTMAgent main implementation
├── config.py                     # LTMAgentConfig and related configs
├── state.py                      # LTM state schemas
├── engines/                      # Processing engines
│   ├── __init__.py
│   ├── memory_extraction.py     # Memory extraction engine
│   ├── knowledge_graph.py       # KG processing engine
│   ├── categorization.py        # TNT-based categorization engine
│   └── consolidation.py         # Memory consolidation engine
├── tools/                        # LangMem-compatible tools
│   ├── __init__.py
│   ├── memory_tools.py          # Memory management tools
│   └── search_tools.py          # Memory search tools
├── nodes/                        # Graph workflow nodes
│   ├── __init__.py
│   ├── extraction_nodes.py      # Memory extraction nodes
│   ├── processing_nodes.py      # KG/TNT processing nodes
│   └── storage_nodes.py         # Memory storage nodes
├── integration/                  # Framework integration
│   ├── __init__.py
│   ├── multi_agent.py           # Multi-agent memory sharing
│   ├── persistence.py           # Haive persistence integration
│   └── reflection.py            # Enhanced reflection patterns
└── docs/                         # Documentation
    ├── ANALYSIS_NOTES.md
    ├── ARCHITECTURE_DESIGN.md
    └── IMPLEMENTATION_GUIDE.md
```

## Detailed Component Design

### 1. LTMAgent Implementation

```python
@register_agent(LTMAgentConfig)
class LTMAgent(Agent[LTMAgentConfig]):
    """Long-Term Memory Agent for conversation memory management.

    Integrates LangMem patterns with Haive's existing KG, TNT, and
    summarization capabilities for comprehensive memory processing.
    """

    def __init__(self, config: LTMAgentConfig = LTMAgentConfig()):
        # Initialize processing engines based on config
        if config.enable_memory_extraction:
            self.memory_engine = MemoryExtractionEngine(config.memory_config)

        if config.enable_kg_processing:
            self.kg_engine = KGExtractionEngine(config.kg_config)

        if config.enable_categorization:
            self.categorization_engine = CategorizationEngine(config.tnt_config)

        if config.enable_consolidation:
            self.consolidation_engine = ConsolidationEngine(config.summary_config)

        super().__init__(config)

    def setup_agent(self):
        """Setup agent-specific configuration after initialization."""
        # Configure tool nodes if enabled
        if self.config.create_memory_tools:
            self.tool_node = self._create_ltm_tool_node()

    def build_graph(self) -> BaseGraph:
        """Build LTM processing workflow graph."""
        graph = BaseGraph()

        # Add processing nodes
        graph.add_node("extract_memories", self.extract_memories_node)

        if self.config.enable_kg_processing:
            graph.add_node("process_kg", self.process_kg_node)

        if self.config.enable_categorization:
            graph.add_node("categorize", self.categorize_node)

        if self.config.enable_consolidation:
            graph.add_node("consolidate", self.consolidate_node)

        graph.add_node("store_memories", self.store_memories_node)

        # Add tool node if configured
        if hasattr(self, 'tool_node'):
            graph.add_node("tools", self.tool_node)

        # Define workflow edges
        self._define_workflow_edges(graph)

        return graph

    def _define_workflow_edges(self, graph: BaseGraph):
        """Define the workflow edges based on configuration."""
        graph.add_edge(START, "extract_memories")

        # Conditional routing based on enabled features
        if self.config.enable_kg_processing:
            graph.add_conditional_edges(
                "extract_memories",
                self._should_process_kg,
                {"kg": "process_kg", "categorize": "categorize", "store": "store_memories"}
            )
            graph.add_edge("process_kg", "categorize" if self.config.enable_categorization else "store_memories")
        else:
            graph.add_edge("extract_memories", "categorize" if self.config.enable_categorization else "store_memories")

        if self.config.enable_categorization:
            graph.add_edge("categorize", "consolidate" if self.config.enable_consolidation else "store_memories")

        if self.config.enable_consolidation:
            graph.add_edge("consolidate", "store_memories")

        # Tool routing
        if hasattr(self, 'tool_node'):
            graph.add_conditional_edges(
                "store_memories",
                self._needs_tools,
                {"tools": "tools", "end": END}
            )
            graph.add_edge("tools", END)
        else:
            graph.add_edge("store_memories", END)
```

### 2. Configuration System

```python
class LTMAgentConfig(AgentConfig):
    """Configuration for Long-Term Memory Agent."""

    # Feature toggles
    enable_memory_extraction: bool = Field(default=True, description="Enable memory extraction from conversations")
    enable_kg_processing: bool = Field(default=True, description="Enable knowledge graph processing")
    enable_categorization: bool = Field(default=True, description="Enable TNT-based categorization")
    enable_consolidation: bool = Field(default=True, description="Enable iterative memory consolidation")
    create_memory_tools: bool = Field(default=True, description="Create LangMem-compatible tools")

    # Processing configurations
    memory_config: MemoryExtractionConfig = Field(default_factory=MemoryExtractionConfig)
    kg_config: KGExtractionConfig = Field(default_factory=KGExtractionConfig)
    tnt_config: TNTConfig = Field(default_factory=TNTConfig)
    summary_config: SummarizationConfig = Field(default_factory=SummarizationConfig)

    # Storage configuration
    storage_namespace: tuple[str, ...] = Field(default=("ltm", "memories"), description="Memory storage namespace")
    namespace_template: str = Field(default="ltm_user_{user_id}", description="Dynamic namespace template")

    # Tool configuration
    tool_permissions: list[str] = Field(default=["create", "update", "delete", "search"], description="Allowed tool operations")
    search_limit: int = Field(default=10, description="Default search result limit")

    # Processing limits
    max_extraction_steps: int = Field(default=3, description="Maximum memory extraction iterations")
    batch_size: int = Field(default=100, description="Batch size for memory processing")
    consolidation_threshold: int = Field(default=50, description="Number of memories before consolidation")


class MemoryExtractionConfig(BaseModel):
    """Configuration for memory extraction engine."""
    llm_config: LLMConfig = Field(default_factory=lambda: AugLLMConfig())
    memory_schemas: list[type[BaseModel]] = Field(default_factory=list, description="Custom memory schemas")
    extraction_instructions: str = Field(default="Extract important information for long-term memory", description="Custom extraction prompt")
    enable_inserts: bool = Field(default=True)
    enable_updates: bool = Field(default=True)
    enable_deletes: bool = Field(default=False)


class KGExtractionConfig(BaseModel):
    """Configuration for knowledge graph extraction."""
    use_iterative_refinement: bool = Field(default=True, description="Use iterative KG refinement")
    allowed_nodes: list[str] = Field(default_factory=list, description="Allowed entity types")
    allowed_relationships: list[str] = Field(default_factory=list, description="Allowed relationship types")
    confidence_threshold: float = Field(default=0.7, description="Minimum confidence for relationships")


class TNTConfig(BaseModel):
    """Configuration for TNT categorization."""
    max_categories: int = Field(default=20, description="Maximum number of categories")
    category_depth: int = Field(default=3, description="Maximum category hierarchy depth")
    min_docs_per_category: int = Field(default=5, description="Minimum documents per category")


class SummarizationConfig(BaseModel):
    """Configuration for memory consolidation."""
    summarization_strategy: Literal["iterative", "batch", "hierarchical"] = Field(default="iterative")
    max_summary_length: int = Field(default=500, description="Maximum summary length in tokens")
    consolidation_frequency: Literal["daily", "weekly", "threshold"] = Field(default="threshold")
```

### 3. State Schema Design

```python
class LTMState(BaseModel):
    """State schema for LTM processing workflow."""

    # Input data
    messages: list[BaseMessage] = Field(description="Input conversation messages")
    user_id: str | None = Field(default=None, description="User identifier for namespace")
    session_id: str | None = Field(default=None, description="Session identifier")

    # Processing outputs
    extracted_memories: list[dict] = Field(default_factory=list, description="Extracted memory objects")
    knowledge_graph: dict = Field(default_factory=dict, description="Extracted entities and relationships")
    categories: list[str] = Field(default_factory=list, description="Memory categories")
    consolidated_summary: str = Field(default="", description="Consolidated memory summary")

    # Storage results
    stored_memory_ids: list[str] = Field(default_factory=list, description="IDs of stored memories")
    storage_namespace: tuple[str, ...] = Field(default=("ltm", "memories"), description="Storage namespace used")

    # Processing control
    processing_stage: Literal["extract", "kg", "categorize", "consolidate", "store", "complete"] = Field(default="extract")
    kg_enabled: bool = Field(default=True)
    categorization_enabled: bool = Field(default=True)
    consolidation_enabled: bool = Field(default=True)

    # Error handling
    processing_errors: list[str] = Field(default_factory=list, description="Processing errors")
    partial_success: bool = Field(default=False, description="Whether processing partially succeeded")

    # Tool interaction
    tool_calls_needed: bool = Field(default=False, description="Whether tool calls are needed")
    tool_results: list[dict] = Field(default_factory=list, description="Results from tool calls")


class EnhancedMemorySchema(BaseModel):
    """Enhanced memory schema combining LangMem + Haive capabilities."""

    # Core LangMem fields
    content: str = Field(description="Memory content")
    memory_id: str = Field(description="Unique memory identifier")
    timestamp: datetime = Field(default_factory=datetime.now, description="Memory creation time")

    # KG enhancement
    entities: list[dict] = Field(default_factory=list, description="Extracted entities")
    relationships: list[dict] = Field(default_factory=list, description="Entity relationships")
    entity_confidence: dict[str, float] = Field(default_factory=dict, description="Entity confidence scores")

    # TNT categorization
    categories: list[str] = Field(default_factory=list, description="Memory categories")
    category_confidence: dict[str, float] = Field(default_factory=dict, description="Category confidence scores")
    taxonomy_path: list[str] = Field(default_factory=list, description="Hierarchical category path")

    # Summarization support
    summary: str | None = Field(default=None, description="Memory summary")
    consolidated_from: list[str] = Field(default_factory=list, description="Source memory IDs if consolidated")
    consolidation_level: int = Field(default=0, description="Number of consolidation steps")

    # Retrieval optimization
    embeddings: list[float] = Field(default_factory=list, description="Vector embeddings")
    keywords: list[str] = Field(default_factory=list, description="Extracted keywords")
    importance_score: float = Field(default=0.5, description="Memory importance score")

    # Access patterns
    access_count: int = Field(default=0, description="Number of times accessed")
    last_accessed: datetime | None = Field(default=None, description="Last access time")
    access_context: list[str] = Field(default_factory=list, description="Access contexts")

    # Metadata
    source: str = Field(default="conversation", description="Memory source")
    user_id: str | None = Field(default=None, description="Associated user")
    session_id: str | None = Field(default=None, description="Associated session")
    tags: list[str] = Field(default_factory=list, description="User-defined tags")
```

### 4. Engine Implementation Patterns

```python
class MemoryExtractionEngine(Engine):
    """Engine for extracting memories using LangMem patterns."""

    def __init__(self, config: MemoryExtractionConfig):
        self.config = config
        self.llm = create_llm(config.llm_config)

        # Create memory schemas (LangMem pattern)
        schemas = config.memory_schemas or [EnhancedMemorySchema]
        self.extractor = create_extractor(
            self.llm,
            tools=schemas,
            instructions=config.extraction_instructions
        )

        super().__init__(config)

    async def ainvoke(self, input_data: dict, config: RunnableConfig = None) -> dict:
        """Extract memories from conversation messages."""
        messages = input_data["messages"]
        existing_memories = input_data.get("existing_memories", [])

        # Use LangMem memory manager pattern
        memory_state = {
            "messages": messages,
            "existing": existing_memories,
            "max_steps": self.config.max_extraction_steps
        }

        extracted = await self.extractor.ainvoke(memory_state, config)

        return {
            "extracted_memories": extracted,
            "extraction_metadata": {
                "num_extracted": len(extracted),
                "processing_time": time.time(),
                "schemas_used": [s.__name__ for s in self.config.memory_schemas]
            }
        }


class KGExtractionEngine(Engine):
    """Engine for knowledge graph extraction using Haive KG components."""

    def __init__(self, config: KGExtractionConfig):
        self.config = config

        # Use existing Haive KG transformer
        if config.use_iterative_refinement:
            kg_config = IterativeGraphTransformerConfig(
                allowed_nodes=config.allowed_nodes,
                allowed_relationships=config.allowed_relationships
            )
            self.kg_transformer = IterativeGraphTransformer(kg_config)
        else:
            # Use base graph transformer
            self.kg_transformer = GraphTransformer()

        super().__init__(config)

    async def ainvoke(self, input_data: dict, config: RunnableConfig = None) -> dict:
        """Extract knowledge graph from memories."""
        memories = input_data["extracted_memories"]

        # Convert memories to documents
        documents = [
            Document(page_content=memory.get("content", ""))
            for memory in memories
        ]

        # Extract knowledge graph
        if hasattr(self.kg_transformer, 'ainvoke'):
            # Use agent-based transformer
            kg_result = await self.kg_transformer.ainvoke({
                "contents": documents
            }, config)
        else:
            # Use direct transformer
            graph_docs = self.kg_transformer.transform_documents(documents)
            kg_result = {"graph_doc": graph_docs[0] if graph_docs else None}

        return {
            "knowledge_graph": kg_result,
            "kg_metadata": {
                "num_entities": len(kg_result.get("entities", [])),
                "num_relationships": len(kg_result.get("relationships", [])),
                "confidence_threshold": self.config.confidence_threshold
            }
        }
```

## Integration Patterns

### 1. Multi-Agent Memory Sharing

```python
class MemorySharedMultiAgent(MultiAgent):
    """Multi-agent system with shared LTM capabilities."""

    def __init__(self, agents: list[Agent], ltm_config: LTMAgentConfig):
        # Create shared LTM agent
        self.ltm_agent = LTMAgent(ltm_config)

        # Enhance agents with memory tools
        enhanced_agents = []
        for agent in agents:
            enhanced_agent = self._add_memory_capabilities(agent, ltm_config)
            enhanced_agents.append(enhanced_agent)

        # Include LTM agent in coordination
        all_agents = [self.ltm_agent] + enhanced_agents

        super().__init__(
            agents=all_agents,
            coordination_mode="supervisor",
            supervisor_agent=self.ltm_agent  # LTM agent coordinates memory
        )

    def _add_memory_capabilities(self, agent: Agent, ltm_config: LTMAgentConfig):
        """Add memory tools to existing agent."""
        # Create memory tools for this agent
        memory_tools = create_ltm_tools(
            namespace=(ltm_config.storage_namespace[0], agent.name),
            config=ltm_config
        )

        # Add tools to agent's graph (this would need proper implementation)
        # This is a conceptual example - actual implementation would depend on agent type
        if hasattr(agent, 'tools'):
            agent.tools.extend(memory_tools)

        return agent
```

### 2. Enhanced Reflection Patterns

```python
class ReflectionEnhancedLTMAgent(LTMAgent):
    """LTM Agent with enhanced reflection capabilities."""

    def __init__(self, config: LTMAgentConfig):
        super().__init__(config)

        # Add message transformation capabilities
        self.reflection_transformer = MessageTransformationNodeConfig(
            transformation_type=TransformationType.REFLECTION,
            preserve_first_message=True
        )

    def build_graph(self) -> BaseGraph:
        """Build graph with reflection capabilities."""
        graph = super().build_graph()

        # Add reflection processing
        graph.add_node("reflect_on_memories", self.reflect_on_memories_node)
        graph.add_node("update_from_reflection", self.update_from_reflection_node)

        # Add reflection edges
        graph.add_edge("store_memories", "reflect_on_memories")
        graph.add_conditional_edges(
            "reflect_on_memories",
            self._should_update_from_reflection,
            {"update": "update_from_reflection", "end": END}
        )
        graph.add_edge("update_from_reflection", END)

        return graph

    async def reflect_on_memories_node(self, state: LTMState, config: RunnableConfig) -> Command:
        """Reflect on stored memories to identify improvements."""
        # Transform messages for reflection
        reflected_messages = self.reflection_transformer(state.messages)

        # Use reflection to assess memory quality and suggest improvements
        reflection_prompt = "Reflect on the quality and completeness of these memories..."
        reflection_result = await self.engines["reflection"].ainvoke({
            "messages": reflected_messages,
            "memories": state.extracted_memories,
            "prompt": reflection_prompt
        })

        return Command(update={
            "reflection_result": reflection_result,
            "needs_memory_update": reflection_result.get("needs_update", False)
        })
```

## Summary

This architecture design properly follows Haive's patterns while incorporating LangMem's proven capabilities:

1. **Proper Agent Implementation**: Uses `@register_agent`, `Agent[ConfigType]`, and `build_graph()` patterns
2. **Engine Composition**: Memory processing via dedicated engines rather than direct function calls
3. **Configuration-Driven**: Proper `AgentConfig` subclasses with `Field` definitions
4. **Component Reuse**: Leverages existing Haive KG, TNT, and summarization components
5. **LangMem Integration**: Adapts proven memory management patterns to Haive's architecture
6. **Multi-Agent Support**: Enables memory sharing across agent systems
7. **Enhanced Capabilities**: Adds reflection, categorization, and knowledge graph features

The design maintains compatibility with both LangMem's memory management approach and Haive's agent architecture patterns.
