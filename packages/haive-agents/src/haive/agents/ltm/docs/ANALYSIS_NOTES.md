# Long-Term Memory (LTM) Analysis & Implementation Notes

## LangMem Analysis Summary

### Core Architecture Components

#### 1. Memory Models & Data Structures

- **Memory**: Basic content + metadata structure
- **ExtractedMemory**: ID + BaseModel content tuple
- **MemoryItem**: Store format with namespace, key, value, timestamps, score
- **Prompt**: Name + prompt + optimization metadata
- **AnnotatedTrajectory**: Messages + feedback for optimization

#### 2. Factory Function Patterns

- `create_memory_manager()` - Memory extraction from conversations
- `create_memory_store_manager()` - Storage-integrated memory management
- `create_manage_memory_tool()` - CRUD operations tool
- `create_search_memory_tool()` - Memory search tool
- `create_prompt_optimizer()` - Single/multi-prompt optimization

#### 3. Processing Pipelines

- **Memory Extraction**: Messages → ExtractedMemory via trustcall extractors
- **Store Integration**: Extract → Store in BaseStore with namespace isolation
- **Search & Retrieval**: Query → semantic search → ranked results
- **Prompt Optimization**: Trajectories + feedback → improved prompts

#### 4. LangGraph Integrations

- **optimize_prompts**: StateGraph for prompt optimization workflows
- **general_reflection_graph**: StateGraph for prompt updates with store integration
- Async/sync duality throughout all components

## Haive Framework Analysis

### Agent Architecture Patterns (CORRECT UNDERSTANDING)

#### Base Agent Class

```python
class Agent(InvokableEngine[BaseModel, BaseModel], ExecutionMixin, StateMixin, PersistenceMixin, SerializationMixin, ABC):
    """Base agent with mixins for execution, state, persistence, serialization"""

    # Key attributes:
    engines: dict[str, Engine]  # Named engines
    engine: Engine             # Primary engine
    state_schema: type[BaseModel]
    graph: BaseGraph          # Workflow graph
    checkpointer: Any         # Persistence
```

#### Agent Hierarchy

- **Agent (base)** → **SimpleAgent** → **ReactAgent**
- **Agent (base)** → **MultiAgent** (coordinates multiple agents)
- Each agent builds a `BaseGraph` via `build_graph()` method
- Engines are core processing units (AugLLM, etc.)
- State schemas define data flow

#### Key Differences from My Initial Understanding:

1. **Agents are NOT Pydantic models** - they're Engine subclasses with mixins
2. **No direct tool creation** - tools are handled via EngineNodeConfig/ToolNodeConfig
3. **Graph-based workflow** - agents build BaseGraph workflows, not simple functions
4. **Schema composition** - uses SchemaComposer for automatic schema generation
5. **Mixin architecture** - functionality via ExecutionMixin, StateMixin, etc.

### Haive Component Analysis for LTM

#### 1. Knowledge Graph Extraction (KG)

**Location**: `document_modifiers/kg/`

**Correct Architecture**:

```python
@register_agent(IterativeGraphTransformerConfig)
class IterativeGraphTransformer(Agent[IterativeGraphTransformerConfig]):
    def __init__(self, config: IterativeGraphTransformerConfig):
        self.llm_graph_transformer = GraphTransformer()
        super().__init__(config)

    def setup_workflow(self):
        self.graph.add_node("generate_initial_summary", self.generate_initial_summary)
        self.graph.add_node("refine_summary", self.refine_summary)
        # ... workflow setup
```

**Key Insights**:

- Agents are registered with configs using `@register_agent`
- Inherit from `Agent[ConfigType]` with proper typing
- Use `setup_workflow()` to define graph nodes
- Return `Command(update={...})` for state updates

#### 2. TNT (Structured Memories)

**Location**: `document_modifiers/tnt/`

**Architecture Pattern**:

```python
@register_agent(TaxonomyAgentConfig)
class TaxonomyAgent(Agent[TaxonomyAgentConfig]):
    """Generates taxonomies through iterative document processing"""

    # Uses engines configured in config:
    # - summary_aug_llm_config
    # - taxonomy_generation_aug_llm_config
    # - taxonomy_review_aug_llm_config
```

**Processing Pipeline**:

1. Document summarization
2. Minibatch creation
3. Initial taxonomy generation
4. Iterative refinement
5. Final review

#### 3. Iterative Summarizer

**Location**: `document_modifiers/summarizer/iterative_refinement/`

**State-Driven Pattern**:

```python
class IterativeSummarizerState(BaseModel):
    contents: list[str | Document | AnyMessage | dict]
    summary: str = ""
    index: int = 0

    def should_refine(self) -> Literal["refine_summary", "__end__"]:
        return "refine_summary" if self.index < len(self.contents) else "__end__"
```

#### 4. Message Transformation

**Location**: `haive-core/src/haive/core/graph/node/message_transformation.py`

**Node-Based Architecture**:

```python
class MessageTransformationNodeConfig(NodeConfig):
    transformation_type: TransformationType
    # Configuration for various transformations:
    # - AI_TO_HUMAN, HUMAN_TO_AI
    # - REFLECTION (role swapping)
    # - AGENT_TO_AGENT (inter-agent communication)
```

## LTM Implementation Strategy (CORRECTED)

### 1. Agent-Based Architecture

#### Core LTM Agent

```python
@register_agent(LTMAgentConfig)
class LTMAgent(Agent[LTMAgentConfig]):
    """Long-term memory agent for conversation memory management"""

    def __init__(self, config: LTMAgentConfig):
        # Initialize memory processors as engines
        self.memory_extractor = MemoryExtractionEngine(config.memory_config)
        self.kg_processor = KGExtractionEngine(config.kg_config)
        self.categorizer = CategorizationEngine(config.tnt_config)
        self.summarizer = SummarizationEngine(config.summary_config)

        super().__init__(config)

    def build_graph(self) -> BaseGraph:
        """Build LTM processing workflow"""
        graph = BaseGraph()

        # Memory processing pipeline
        graph.add_node("extract_memories", self.extract_memories)
        graph.add_node("process_kg", self.process_knowledge_graph)
        graph.add_node("categorize", self.categorize_memories)
        graph.add_node("consolidate", self.consolidate_memories)
        graph.add_node("store", self.store_memories)

        # Define workflow
        graph.add_edge(START, "extract_memories")
        graph.add_conditional_edges(
            "extract_memories",
            self.should_process_kg,
            {"process_kg": "process_kg", "categorize": "categorize"}
        )
        # ... more edges

        return graph
```

#### LTM State Schema

```python
class LTMState(BaseModel):
    """State for LTM processing workflow"""
    messages: list[BaseMessage]
    extracted_memories: list[dict] = []
    knowledge_graph: dict = {}
    categories: list[str] = []
    consolidated_summary: str = ""
    stored_memory_ids: list[str] = []

    # Processing control
    processing_stage: Literal["extract", "kg", "categorize", "consolidate", "store"] = "extract"
    kg_enabled: bool = True
    categorization_enabled: bool = True
```

### 2. Configuration Pattern

#### LTM Agent Config

```python
class LTMAgentConfig(AgentConfig):
    """Configuration for Long-Term Memory Agent"""

    # Memory processing configs
    memory_config: MemoryExtractionConfig = Field(default_factory=MemoryExtractionConfig)
    kg_config: KGExtractionConfig = Field(default_factory=KGExtractionConfig)
    tnt_config: TNTConfig = Field(default_factory=TNTConfig)
    summary_config: SummarizationConfig = Field(default_factory=SummarizationConfig)

    # Storage configuration
    storage_namespace: tuple[str, ...] = ("ltm", "memories")
    enable_kg_processing: bool = True
    enable_categorization: bool = True
    enable_consolidation: bool = True

    # Tool configuration
    create_memory_tools: bool = True
    tool_namespace_template: str = "ltm_user_{user_id}"
```

### 3. Engine-Based Processing

#### Memory Extraction Engine

```python
class MemoryExtractionEngine(Engine):
    """Engine for extracting memories from conversations using LangMem patterns"""

    def __init__(self, config: MemoryExtractionConfig):
        self.llm = create_llm(config.llm_config)
        self.schemas = config.memory_schemas
        self.extractor = create_extractor(self.llm, tools=self.schemas)
        super().__init__(config)

    async def ainvoke(self, input_data: dict, config: RunnableConfig = None) -> dict:
        messages = input_data["messages"]
        existing = input_data.get("existing_memories", [])

        # Use LangMem memory manager pattern
        extracted = await self.extractor.ainvoke({
            "messages": messages,
            "existing": existing,
            "max_steps": self.config.max_extraction_steps
        })

        return {"extracted_memories": extracted}
```

### 4. Tool Integration (Corrected Approach)

#### LTM Tools via ToolNodeConfig

```python
def create_ltm_tool_node(config: LTMAgentConfig) -> ToolNodeConfig:
    """Create tool node with LTM capabilities"""

    # Create tools using LangMem patterns but with Haive integration
    memory_tools = [
        create_manage_memory_tool(
            namespace=config.storage_namespace,
            store=config.persistence.store_factory.create_store()
        ),
        create_search_memory_tool(
            namespace=config.storage_namespace,
            store=config.persistence.store_factory.create_store()
        )
    ]

    return ToolNodeConfig(
        name="ltm_tools",
        tools=memory_tools,
        tools_condition="always"  # Or conditional logic
    )
```

### 5. Multi-Agent Integration

#### Memory-Enhanced Multi-Agent

```python
class MemoryEnhancedMultiAgent(MultiAgent):
    """Multi-agent system with shared long-term memory"""

    def __init__(self, agents: list[Agent], ltm_config: LTMAgentConfig):
        # Create LTM agent
        self.ltm_agent = LTMAgent(ltm_config)

        # Add LTM agent to the multi-agent system
        enhanced_agents = [self.ltm_agent] + agents

        super().__init__(
            agents=enhanced_agents,
            coordination_mode="supervisor",  # LTM agent supervises memory
            supervisor_agent=self.ltm_agent
        )
```

## Key Corrections & Insights

### What I Got Wrong Initially:

1. **Agent Architecture**: Agents are NOT simple Pydantic models, they're Engine subclasses
2. **Tool Creation**: Tools are integrated via ToolNodeConfig, not direct creation
3. **Workflow Definition**: Uses BaseGraph with nodes/edges, not simple function calls
4. **State Management**: Via BaseModel state schemas with Command updates
5. **Configuration**: Proper AgentConfig subclasses with Field definitions

### Correct Haive Patterns:

1. **@register_agent decorator** with typed configs
2. **Agent[ConfigType] inheritance** with proper generics
3. **build_graph() method** returning BaseGraph workflows
4. **Engine composition** for processing capabilities
5. **Mixin architecture** for cross-cutting concerns
6. **SchemaComposer** for automatic schema generation

### LTM Integration Strategy:

1. Create **LTMAgent** following Haive agent patterns
2. Use **existing Haive components** (KG, TNT, Summarizer) as engines
3. Implement **LangMem tool patterns** via ToolNodeConfig
4. Leverage **Haive persistence** for storage backend
5. Support **multi-agent scenarios** via supervisor patterns

This corrected understanding respects Haive's actual architecture while incorporating LangMem's proven memory management patterns.
