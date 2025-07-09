# LTM Implementation Guide

## Implementation Roadmap

### Phase 1: Core Foundation (Week 1)

#### Day 1-2: Basic Structure Setup

```bash
# Create core module structure
mkdir -p haive-agents/src/haive/agents/ltm/{engines,tools,nodes,integration}

# Core files to implement:
# - config.py (LTMAgentConfig and related configs)
# - state.py (LTMState and memory schemas)
# - agent.py (basic LTMAgent structure)
```

#### Day 3-4: Memory Extraction Engine

```python
# File: engines/memory_extraction.py
# Implement MemoryExtractionEngine using LangMem patterns
# - Integrate with trustcall extractor
# - Support custom memory schemas
# - Handle multi-step extraction
```

#### Day 5-7: Basic LTM Agent

```python
# File: agent.py
# Implement core LTMAgent with:
# - Proper @register_agent decoration
# - Agent[LTMAgentConfig] inheritance
# - Basic build_graph() with memory extraction
# - Simple storage integration
```

### Phase 2: Enhanced Processing (Week 2)

#### Day 8-10: Knowledge Graph Integration

```python
# File: engines/knowledge_graph.py
# Integrate existing Haive KG components:
# - Wrap IterativeGraphTransformer
# - Handle entity/relationship extraction
# - Support confidence scoring
```

#### Day 11-12: TNT Categorization

```python
# File: engines/categorization.py
# Integrate TaxonomyAgent:
# - Wrap existing TNT functionality
# - Support hierarchical categorization
# - Handle batch processing
```

#### Day 13-14: Memory Consolidation

```python
# File: engines/consolidation.py
# Integrate IterativeSummarizer:
# - Memory summarization and merging
# - Progressive consolidation
# - Threshold-based triggers
```

### Phase 3: Advanced Features (Week 3)

#### Day 15-17: LangMem Tools Integration

```python
# File: tools/memory_tools.py
# Implement LangMem-compatible tools:
# - create_manage_memory_tool adaptation
# - create_search_memory_tool adaptation
# - Haive ToolNodeConfig integration
```

#### Day 18-19: Multi-Modal Retrieval

```python
# File: tools/search_tools.py
# Advanced search capabilities:
# - Semantic search via embeddings
# - Graph traversal search
# - Categorical search via TNT
# - Result fusion and ranking
```

#### Day 20-21: Enhanced Workflow Nodes

```python
# File: nodes/
# Implement specialized workflow nodes:
# - extraction_nodes.py (memory extraction)
# - processing_nodes.py (KG/TNT processing)
# - storage_nodes.py (multi-backend storage)
```

### Phase 4: Integration & Testing (Week 4)

#### Day 22-24: Multi-Agent Integration

```python
# File: integration/multi_agent.py
# Memory-shared multi-agent systems:
# - MemorySharedMultiAgent implementation
# - Cross-agent memory sharing
# - Supervisor coordination patterns
```

#### Day 25-26: Reflection Enhancement

```python
# File: integration/reflection.py
# Enhanced reflection patterns:
# - Message transformation integration
# - Self-assessment capabilities
# - Memory quality improvement
```

#### Day 27-28: Testing & Validation

```python
# Comprehensive testing:
# - Unit tests for all components
# - Integration tests with existing agents
# - Performance benchmarking
# - Documentation completion
```

## Detailed Implementation Steps

### Step 1: Configuration System

```python
# File: config.py
from pydantic import BaseModel, Field
from haive.core.engine.agent.agent import AgentConfig
from haive.core.models.llm.base import LLMConfig
from haive.core.engine.aug_llm import AugLLMConfig

class LTMAgentConfig(AgentConfig):
    """Main configuration for LTM Agent."""

    # Feature toggles
    enable_memory_extraction: bool = Field(default=True)
    enable_kg_processing: bool = Field(default=True)
    enable_categorization: bool = Field(default=True)
    enable_consolidation: bool = Field(default=True)
    create_memory_tools: bool = Field(default=True)

    # Sub-configurations
    memory_config: "MemoryExtractionConfig" = Field(default_factory=lambda: MemoryExtractionConfig())
    kg_config: "KGExtractionConfig" = Field(default_factory=lambda: KGExtractionConfig())
    tnt_config: "TNTConfig" = Field(default_factory=lambda: TNTConfig())
    summary_config: "SummarizationConfig" = Field(default_factory=lambda: SummarizationConfig())

    # Storage settings
    storage_namespace: tuple[str, ...] = Field(default=("ltm", "memories"))
    namespace_template: str = Field(default="ltm_user_{user_id}")

class MemoryExtractionConfig(BaseModel):
    llm_config: LLMConfig = Field(default_factory=AugLLMConfig)
    memory_schemas: list[type[BaseModel]] = Field(default_factory=list)
    max_extraction_steps: int = Field(default=3)
    enable_inserts: bool = Field(default=True)
    enable_updates: bool = Field(default=True)
    enable_deletes: bool = Field(default=False)

# Similar for KGExtractionConfig, TNTConfig, SummarizationConfig...
```

### Step 2: State Schema Design

```python
# File: state.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal
from langchain_core.messages import BaseMessage

class LTMState(BaseModel):
    """Main state for LTM processing workflow."""

    # Input
    messages: list[BaseMessage] = Field(description="Input conversation messages")
    user_id: str | None = Field(default=None)
    session_id: str | None = Field(default=None)

    # Processing outputs
    extracted_memories: list[dict] = Field(default_factory=list)
    knowledge_graph: dict = Field(default_factory=dict)
    categories: list[str] = Field(default_factory=list)
    consolidated_summary: str = Field(default="")

    # Storage
    stored_memory_ids: list[str] = Field(default_factory=list)
    storage_namespace: tuple[str, ...] = Field(default=("ltm", "memories"))

    # Control
    processing_stage: Literal["extract", "kg", "categorize", "consolidate", "store", "complete"] = Field(default="extract")
    processing_errors: list[str] = Field(default_factory=list)

class EnhancedMemorySchema(BaseModel):
    """Enhanced memory schema with KG and TNT features."""

    # Core LangMem fields
    content: str = Field(description="Memory content")
    memory_id: str = Field(description="Unique identifier")
    timestamp: datetime = Field(default_factory=datetime.now)

    # KG enhancement
    entities: list[dict] = Field(default_factory=list)
    relationships: list[dict] = Field(default_factory=list)

    # TNT categorization
    categories: list[str] = Field(default_factory=list)
    category_confidence: dict[str, float] = Field(default_factory=dict)

    # Consolidation
    summary: str | None = Field(default=None)
    consolidated_from: list[str] = Field(default_factory=list)

    # Retrieval optimization
    embeddings: list[float] = Field(default_factory=list)
    importance_score: float = Field(default=0.5)
    access_count: int = Field(default=0)
```

### Step 3: Core Agent Implementation

```python
# File: agent.py
import logging
from haive.core.engine.agent.agent import Agent, register_agent
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langgraph.graph import START, END
from langgraph.types import Command
from langchain_core.runnables import RunnableConfig

from .config import LTMAgentConfig
from .state import LTMState
from .engines.memory_extraction import MemoryExtractionEngine
from .engines.knowledge_graph import KGExtractionEngine
from .engines.categorization import CategorizationEngine
from .engines.consolidation import ConsolidationEngine

logger = logging.getLogger(__name__)

@register_agent(LTMAgentConfig)
class LTMAgent(Agent[LTMAgentConfig]):
    """Long-Term Memory Agent integrating LangMem patterns with Haive components."""

    def __init__(self, config: LTMAgentConfig = LTMAgentConfig()):
        # Initialize engines based on configuration
        self.engines = {}

        if config.enable_memory_extraction:
            self.engines["memory_extraction"] = MemoryExtractionEngine(config.memory_config)

        if config.enable_kg_processing:
            self.engines["kg_extraction"] = KGExtractionEngine(config.kg_config)

        if config.enable_categorization:
            self.engines["categorization"] = CategorizationEngine(config.tnt_config)

        if config.enable_consolidation:
            self.engines["consolidation"] = ConsolidationEngine(config.summary_config)

        super().__init__(config)

    def setup_agent(self):
        """Setup agent after initialization."""
        # Configure persistence namespace
        if hasattr(self, 'store') and self.config.storage_namespace:
            self.namespace = self.config.storage_namespace

        # Setup tool nodes if enabled
        if self.config.create_memory_tools:
            self._setup_memory_tools()

    def build_graph(self) -> BaseGraph:
        """Build LTM processing workflow."""
        graph = BaseGraph()

        # Add core processing nodes
        graph.add_node("extract_memories", self.extract_memories_node)

        if "kg_extraction" in self.engines:
            graph.add_node("process_kg", self.process_kg_node)

        if "categorization" in self.engines:
            graph.add_node("categorize", self.categorize_node)

        if "consolidation" in self.engines:
            graph.add_node("consolidate", self.consolidate_node)

        graph.add_node("store_memories", self.store_memories_node)

        # Define workflow
        self._define_workflow_edges(graph)

        return graph

    def _define_workflow_edges(self, graph: BaseGraph):
        """Define workflow routing."""
        graph.add_edge(START, "extract_memories")

        # Conditional routing based on enabled features
        next_node = self._determine_next_node_after_extraction()
        graph.add_edge("extract_memories", next_node)

        # Chain remaining nodes
        if "kg_extraction" in self.engines:
            next_after_kg = self._determine_next_node_after_kg()
            graph.add_edge("process_kg", next_after_kg)

        if "categorization" in self.engines:
            next_after_cat = self._determine_next_node_after_categorization()
            graph.add_edge("categorize", next_after_cat)

        if "consolidation" in self.engines:
            graph.add_edge("consolidate", "store_memories")

        graph.add_edge("store_memories", END)

    # Node implementations
    async def extract_memories_node(self, state: LTMState, config: RunnableConfig) -> Command:
        """Extract memories from conversation messages."""
        try:
            if "memory_extraction" not in self.engines:
                return Command(update={"processing_errors": ["Memory extraction disabled"]})

            result = await self.engines["memory_extraction"].ainvoke({
                "messages": state.messages,
                "existing_memories": []  # Could load from store
            }, config)

            return Command(update={
                "extracted_memories": result["extracted_memories"],
                "processing_stage": "kg"
            })

        except Exception as e:
            logger.error(f"Memory extraction failed: {e}")
            return Command(update={
                "processing_errors": [str(e)],
                "processing_stage": "error"
            })

    async def process_kg_node(self, state: LTMState, config: RunnableConfig) -> Command:
        """Process knowledge graph extraction."""
        try:
            if "kg_extraction" not in self.engines:
                return Command(update={"processing_stage": "categorize"})

            result = await self.engines["kg_extraction"].ainvoke({
                "extracted_memories": state.extracted_memories
            }, config)

            return Command(update={
                "knowledge_graph": result["knowledge_graph"],
                "processing_stage": "categorize"
            })

        except Exception as e:
            logger.error(f"KG extraction failed: {e}")
            return Command(update={
                "processing_errors": state.processing_errors + [str(e)],
                "processing_stage": "categorize"  # Continue despite error
            })

    async def categorize_node(self, state: LTMState, config: RunnableConfig) -> Command:
        """Categorize memories using TNT."""
        try:
            if "categorization" not in self.engines:
                return Command(update={"processing_stage": "consolidate"})

            result = await self.engines["categorization"].ainvoke({
                "extracted_memories": state.extracted_memories,
                "knowledge_graph": state.knowledge_graph
            }, config)

            return Command(update={
                "categories": result["categories"],
                "processing_stage": "consolidate"
            })

        except Exception as e:
            logger.error(f"Categorization failed: {e}")
            return Command(update={
                "processing_errors": state.processing_errors + [str(e)],
                "processing_stage": "consolidate"
            })

    async def consolidate_node(self, state: LTMState, config: RunnableConfig) -> Command:
        """Consolidate memories using iterative summarization."""
        try:
            if "consolidation" not in self.engines:
                return Command(update={"processing_stage": "store"})

            result = await self.engines["consolidation"].ainvoke({
                "extracted_memories": state.extracted_memories,
                "categories": state.categories,
                "knowledge_graph": state.knowledge_graph
            }, config)

            return Command(update={
                "consolidated_summary": result["summary"],
                "processing_stage": "store"
            })

        except Exception as e:
            logger.error(f"Consolidation failed: {e}")
            return Command(update={
                "processing_errors": state.processing_errors + [str(e)],
                "processing_stage": "store"
            })

    async def store_memories_node(self, state: LTMState, config: RunnableConfig) -> Command:
        """Store processed memories."""
        try:
            # Store memories using Haive persistence
            stored_ids = []

            for memory in state.extracted_memories:
                # Enhance memory with processing results
                enhanced_memory = self._enhance_memory_for_storage(
                    memory, state.knowledge_graph, state.categories, state.consolidated_summary
                )

                # Store in namespace
                memory_id = await self._store_memory(enhanced_memory, state.storage_namespace)
                stored_ids.append(memory_id)

            return Command(update={
                "stored_memory_ids": stored_ids,
                "processing_stage": "complete"
            })

        except Exception as e:
            logger.error(f"Memory storage failed: {e}")
            return Command(update={
                "processing_errors": state.processing_errors + [str(e)],
                "processing_stage": "error"
            })

    def _enhance_memory_for_storage(self, memory: dict, kg: dict, categories: list[str], summary: str) -> dict:
        """Enhance memory with processing results before storage."""
        enhanced = memory.copy()

        # Add KG data
        if kg:
            enhanced["entities"] = kg.get("entities", [])
            enhanced["relationships"] = kg.get("relationships", [])

        # Add categories
        enhanced["categories"] = categories

        # Add summary if available
        if summary:
            enhanced["summary"] = summary

        # Add timestamps and metadata
        enhanced["timestamp"] = datetime.now().isoformat()
        enhanced["processing_version"] = "1.0"

        return enhanced

    async def _store_memory(self, memory: dict, namespace: tuple[str, ...]) -> str:
        """Store individual memory in persistence layer."""
        if not hasattr(self, 'store'):
            raise RuntimeError("No store configured for memory storage")

        memory_id = memory.get("memory_id") or str(uuid.uuid4())

        await self.store.aput(
            namespace=namespace,
            key=memory_id,
            value=memory
        )

        return memory_id

    def _setup_memory_tools(self):
        """Setup LangMem-compatible memory tools."""
        # This would integrate with ToolNodeConfig
        # Implementation depends on tool integration pattern
        pass

    def _determine_next_node_after_extraction(self) -> str:
        """Determine next node after memory extraction."""
        if "kg_extraction" in self.engines:
            return "process_kg"
        elif "categorization" in self.engines:
            return "categorize"
        elif "consolidation" in self.engines:
            return "consolidate"
        else:
            return "store_memories"

    def _determine_next_node_after_kg(self) -> str:
        """Determine next node after KG processing."""
        if "categorization" in self.engines:
            return "categorize"
        elif "consolidation" in self.engines:
            return "consolidate"
        else:
            return "store_memories"

    def _determine_next_node_after_categorization(self) -> str:
        """Determine next node after categorization."""
        if "consolidation" in self.engines:
            return "consolidate"
        else:
            return "store_memories"
```

### Step 4: Engine Implementations

```python
# File: engines/memory_extraction.py
from haive.core.engine.base import Engine
from langchain_core.runnables import RunnableConfig
from trustcall import create_extractor
from ..config import MemoryExtractionConfig
from ..state import EnhancedMemorySchema

class MemoryExtractionEngine(Engine):
    """Memory extraction using LangMem patterns."""

    def __init__(self, config: MemoryExtractionConfig):
        self.config = config
        self.llm = self._create_llm(config.llm_config)

        # Setup memory schemas
        schemas = config.memory_schemas or [EnhancedMemorySchema]
        self.extractor = create_extractor(
            self.llm,
            tools=schemas,
            instructions=config.extraction_instructions
        )

        super().__init__(config)

    async def ainvoke(self, input_data: dict, config: RunnableConfig = None) -> dict:
        """Extract memories from messages."""
        messages = input_data["messages"]
        existing = input_data.get("existing_memories", [])

        # Use LangMem memory manager pattern
        extraction_input = {
            "messages": messages,
            "existing": existing,
            "max_steps": self.config.max_extraction_steps
        }

        extracted = await self.extractor.ainvoke(extraction_input, config)

        return {
            "extracted_memories": extracted,
            "extraction_metadata": {
                "num_extracted": len(extracted),
                "schemas_used": [s.__name__ for s in self.config.memory_schemas or [EnhancedMemorySchema]]
            }
        }

    def _create_llm(self, llm_config):
        """Create LLM from config."""
        # Implementation depends on Haive's LLM creation patterns
        # This should use the same pattern as other Haive agents
        pass
```

## Testing Strategy

### Unit Tests

```python
# File: tests/test_ltm_agent.py
import pytest
from haive.agents.ltm import LTMAgent, LTMAgentConfig
from haive.agents.ltm.state import LTMState
from langchain_core.messages import HumanMessage

@pytest.fixture
def ltm_config():
    return LTMAgentConfig(
        enable_memory_extraction=True,
        enable_kg_processing=False,  # Simplify for testing
        enable_categorization=False,
        enable_consolidation=False
    )

@pytest.fixture
def ltm_agent(ltm_config):
    return LTMAgent(ltm_config)

@pytest.mark.asyncio
async def test_memory_extraction(ltm_agent):
    """Test basic memory extraction functionality."""
    state = LTMState(
        messages=[HumanMessage(content="I love pizza and hiking")]
    )

    result = await ltm_agent.extract_memories_node(state, {})

    assert "extracted_memories" in result.update
    assert len(result.update["extracted_memories"]) > 0
    assert result.update["processing_stage"] == "store"  # Next stage

@pytest.mark.asyncio
async def test_full_workflow(ltm_agent):
    """Test complete LTM workflow."""
    input_data = {
        "messages": [
            HumanMessage(content="I prefer coffee over tea"),
            HumanMessage(content="My favorite color is blue")
        ]
    }

    result = await ltm_agent.ainvoke(input_data)

    assert result["processing_stage"] == "complete"
    assert len(result["stored_memory_ids"]) > 0
    assert len(result["processing_errors"]) == 0
```

### Integration Tests

```python
# File: tests/test_integration.py
import pytest
from haive.agents.simple import SimpleAgent
from haive.agents.ltm import LTMAgent, create_ltm_tools

@pytest.mark.asyncio
async def test_simple_agent_with_ltm_tools():
    """Test SimpleAgent enhanced with LTM tools."""
    # Create LTM tools
    ltm_tools = create_ltm_tools(
        namespace=("test", "memories"),
        config={"enable_search": True, "enable_management": True}
    )

    # Create SimpleAgent with LTM tools
    simple_config = SimpleAgentConfig(
        tools=ltm_tools,
        # ... other config
    )
    agent = SimpleAgent(simple_config)

    # Test memory storage
    result = await agent.ainvoke({
        "messages": [HumanMessage(content="Store this important fact")]
    })

    # Verify memory was stored
    assert "memory_stored" in result
```

## Deployment Considerations

### Performance Optimization

- **Async Processing**: All memory operations should be async
- **Batch Processing**: Handle multiple memories efficiently
- **Caching**: Cache frequently accessed memories
- **Connection Pooling**: Efficient database connections

### Monitoring & Observability

```python
# Add logging and metrics to all components
import logging
from haive.core.monitoring import track_performance

logger = logging.getLogger(__name__)

@track_performance("ltm.memory_extraction")
async def extract_memories_node(self, state: LTMState, config: RunnableConfig) -> Command:
    logger.info(f"Extracting memories from {len(state.messages)} messages")
    # ... implementation
    logger.info(f"Extracted {len(extracted)} memories")
```

### Error Handling & Recovery

- **Graceful Degradation**: Continue processing even if some components fail
- **Partial Success**: Store what was successfully processed
- **Retry Logic**: Retry failed operations with exponential backoff
- **Error Aggregation**: Collect and report all errors

This implementation guide provides a clear path to building the LTM system while properly following Haive's architectural patterns and integrating LangMem's proven memory management capabilities.
