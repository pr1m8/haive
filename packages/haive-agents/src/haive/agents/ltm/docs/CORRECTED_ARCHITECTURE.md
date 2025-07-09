# Corrected LTM Architecture (Using Proper Haive Agent Patterns)

## Understanding the Correct Agent Pattern

After examining `haive.agents.base.agent.Agent`, the correct pattern is:

### Proper Agent Structure

```python
from haive.agents.base.agent import Agent
from haive.core.graph.state_graph.base_graph2 import BaseGraph

class LTMAgent(Agent):
    """Long-Term Memory Agent following proper Haive patterns."""

    def setup_agent(self) -> None:
        """Hook called during initialization for custom setup."""
        # This is where we set up engines, sync fields, etc.
        pass

    def build_graph(self) -> BaseGraph:
        """Abstract method - must return a BaseGraph."""
        # This is where we define the workflow
        pass
```

### Key Insights from Base Agent:

1. **No Generic Types**: `Agent` is not `Agent[ConfigType]` - it's just `Agent`
2. **No @register_agent**: The registration pattern is different
3. **Engine-centric**: Uses `engines` dict and optional `engine` field
4. **Auto Schema Generation**: Can auto-generate schemas from engines with `set_schema=True`
5. **Lifecycle Hooks**: `setup_agent()` called before schema/graph building
6. **Mixin-based**: Inherits ExecutionMixin, StateMixin, PersistenceMixin, SerializationMixin

## Corrected LTM Implementation

### 1. LTM Agent (Proper Pattern)

```python
# File: agent.py
from haive.agents.base.agent import Agent
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.engine.aug_llm import AugLLMConfig
from langgraph.graph import START, END
from langchain_core.runnables import RunnableConfig
from typing import Any

class LTMAgent(Agent):
    """Long-Term Memory Agent using proper Haive patterns."""

    # Agent-specific fields (these get auto-handled by base class)
    enable_kg_processing: bool = True
    enable_categorization: bool = True
    enable_consolidation: bool = True
    storage_namespace: tuple[str, ...] = ("ltm", "memories")

    def setup_agent(self) -> None:
        """Setup LTM-specific engines and configuration."""
        # Setup memory extraction engine
        if not self.engines.get("memory_extraction"):
            self.engines["memory_extraction"] = self._create_memory_extraction_engine()

        # Setup KG processing engine if enabled
        if self.enable_kg_processing and not self.engines.get("kg_processing"):
            self.engines["kg_processing"] = self._create_kg_engine()

        # Setup categorization engine if enabled
        if self.enable_categorization and not self.engines.get("categorization"):
            self.engines["categorization"] = self._create_categorization_engine()

        # Setup consolidation engine if enabled
        if self.enable_consolidation and not self.engines.get("consolidation"):
            self.engines["consolidation"] = self._create_consolidation_engine()

    def build_graph(self) -> BaseGraph:
        """Build the LTM processing workflow graph."""
        from haive.core.graph.node.engine_node import EngineNodeConfig
        from haive.core.graph.node.tool_node_config import ToolNodeConfig

        graph = BaseGraph()

        # Add memory extraction node
        graph.add_node(
            "extract_memories",
            EngineNodeConfig(
                name="extract_memories",
                engine_name="memory_extraction",
                input_key="messages",
                output_key="extracted_memories"
            )
        )

        # Add KG processing node if enabled
        if self.enable_kg_processing:
            graph.add_node(
                "process_kg",
                EngineNodeConfig(
                    name="process_kg",
                    engine_name="kg_processing",
                    input_key="extracted_memories",
                    output_key="knowledge_graph"
                )
            )

        # Add categorization node if enabled
        if self.enable_categorization:
            graph.add_node(
                "categorize",
                EngineNodeConfig(
                    name="categorize",
                    engine_name="categorization",
                    input_key="extracted_memories",
                    output_key="categories"
                )
            )

        # Add consolidation node if enabled
        if self.enable_consolidation:
            graph.add_node(
                "consolidate",
                EngineNodeConfig(
                    name="consolidate",
                    engine_name="consolidation",
                    input_key="extracted_memories",
                    output_key="consolidated_summary"
                )
            )

        # Add storage node
        graph.add_node("store_memories", self._create_storage_node())

        # Add memory tools if requested
        if getattr(self, 'create_memory_tools', True):
            graph.add_node("memory_tools", self._create_memory_tools_node())

        # Define workflow edges
        self._add_workflow_edges(graph)

        return graph

    def _create_memory_extraction_engine(self):
        """Create memory extraction engine using LangMem patterns."""
        from .engines.memory_extraction import MemoryExtractionEngine
        return MemoryExtractionEngine(
            llm_config=AugLLMConfig(),
            memory_schemas=[],  # Will use default EnhancedMemorySchema
            max_extraction_steps=3
        )

    def _create_kg_engine(self):
        """Create KG extraction engine using existing Haive components."""
        from .engines.knowledge_graph import KGExtractionEngine
        return KGExtractionEngine()

    def _create_categorization_engine(self):
        """Create categorization engine using TNT."""
        from .engines.categorization import CategorizationEngine
        return CategorizationEngine()

    def _create_consolidation_engine(self):
        """Create consolidation engine using iterative summarizer."""
        from .engines.consolidation import ConsolidationEngine
        return ConsolidationEngine()

    def _create_storage_node(self):
        """Create storage node for persisting memories."""
        from .nodes.storage_node import StorageNodeConfig
        return StorageNodeConfig(
            name="store_memories",
            storage_namespace=self.storage_namespace
        )

    def _create_memory_tools_node(self):
        """Create memory tools node with LangMem-compatible tools."""
        from .tools.memory_tools import create_ltm_tools

        tools = create_ltm_tools(
            namespace=self.storage_namespace,
            store=self.store  # Available from PersistenceMixin
        )

        from haive.core.graph.node.tool_node_config import ToolNodeConfig
        return ToolNodeConfig(
            name="memory_tools",
            tools=tools
        )

    def _add_workflow_edges(self, graph: BaseGraph):
        """Add edges to define workflow routing."""
        graph.add_edge(START, "extract_memories")

        current_node = "extract_memories"

        # Route through enabled processing steps
        if self.enable_kg_processing:
            graph.add_edge(current_node, "process_kg")
            current_node = "process_kg"

        if self.enable_categorization:
            graph.add_edge(current_node, "categorize")
            current_node = "categorize"

        if self.enable_consolidation:
            graph.add_edge(current_node, "consolidate")
            current_node = "consolidate"

        graph.add_edge(current_node, "store_memories")

        # Route to tools if available
        if hasattr(self, 'create_memory_tools') and self.create_memory_tools:
            graph.add_conditional_edges(
                "store_memories",
                self._should_use_tools,
                {"tools": "memory_tools", "end": END}
            )
            graph.add_edge("memory_tools", END)
        else:
            graph.add_edge("store_memories", END)

    def _should_use_tools(self, state) -> str:
        """Determine if tools should be used."""
        # Logic to determine tool usage
        # For now, simple: use tools if last message requests memory operations
        if hasattr(state, 'messages') and state.messages:
            last_message = state.messages[-1]
            if any(keyword in last_message.content.lower()
                   for keyword in ['remember', 'recall', 'search memory', 'forget']):
                return "tools"
        return "end"
```

### 2. Engine Implementations (Following Haive Patterns)

```python
# File: engines/memory_extraction.py
from haive.core.engine.base import Engine
from langchain_core.runnables import RunnableConfig
from trustcall import create_extractor
from typing import Any, Dict

class MemoryExtractionEngine(Engine):
    """Memory extraction engine using LangMem patterns."""

    def __init__(self, llm_config, memory_schemas=None, max_extraction_steps=3):
        self.llm_config = llm_config
        self.memory_schemas = memory_schemas or []
        self.max_extraction_steps = max_extraction_steps

        # Create LLM and extractor
        self.llm = self._create_llm(llm_config)
        self.extractor = self._create_extractor()

        super().__init__(name="memory_extraction")

    def _create_llm(self, config):
        """Create LLM from config using Haive patterns."""
        # This should follow Haive's LLM creation patterns
        # Implementation depends on how Haive creates LLMs
        from haive.core.models.llm.factory import create_llm
        return create_llm(config)

    def _create_extractor(self):
        """Create trustcall extractor with memory schemas."""
        schemas = self.memory_schemas
        if not schemas:
            from ..models.memory import EnhancedMemorySchema
            schemas = [EnhancedMemorySchema]

        return create_extractor(
            self.llm,
            tools=schemas,
            instructions="Extract important information for long-term memory storage"
        )

    async def ainvoke(self, input_data: Dict[str, Any], config: RunnableConfig = None) -> Dict[str, Any]:
        """Extract memories from conversation messages."""
        messages = input_data.get("messages", [])
        existing_memories = input_data.get("existing_memories", [])

        # Use LangMem memory manager pattern
        extraction_input = {
            "messages": messages,
            "existing": existing_memories,
            "max_steps": self.max_extraction_steps
        }

        try:
            extracted = await self.extractor.ainvoke(extraction_input, config)

            return {
                "extracted_memories": extracted,
                "extraction_metadata": {
                    "num_extracted": len(extracted),
                    "schemas_used": [s.__name__ for s in self.memory_schemas or []]
                }
            }
        except Exception as e:
            return {
                "extracted_memories": [],
                "extraction_error": str(e)
            }

    def invoke(self, input_data: Dict[str, Any], config: RunnableConfig = None) -> Dict[str, Any]:
        """Sync version of memory extraction."""
        # Implement sync version or delegate to async
        import asyncio
        return asyncio.run(self.ainvoke(input_data, config))
```

### 3. State Schema (Proper Pydantic)

```python
# File: models/state.py
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
from datetime import datetime
from typing import Literal

class LTMState(BaseModel):
    """State schema for LTM processing workflow."""

    # Input
    messages: list[BaseMessage] = Field(default_factory=list, description="Conversation messages")
    user_id: str | None = Field(default=None, description="User identifier")
    session_id: str | None = Field(default=None, description="Session identifier")

    # Processing outputs
    extracted_memories: list[dict] = Field(default_factory=list, description="Extracted memories")
    knowledge_graph: dict = Field(default_factory=dict, description="KG entities/relationships")
    categories: list[str] = Field(default_factory=list, description="Memory categories")
    consolidated_summary: str = Field(default="", description="Consolidated summary")

    # Storage
    stored_memory_ids: list[str] = Field(default_factory=list, description="Stored memory IDs")
    storage_namespace: tuple[str, ...] = Field(default=("ltm", "memories"), description="Storage namespace")

    # Processing control
    processing_stage: Literal["extract", "kg", "categorize", "consolidate", "store", "complete"] = Field(
        default="extract", description="Current processing stage"
    )
    processing_errors: list[str] = Field(default_factory=list, description="Processing errors")
    partial_success: bool = Field(default=False, description="Partial processing success")

    # Tool interaction
    tool_calls_needed: bool = Field(default=False, description="Tools needed")
    tool_results: list[dict] = Field(default_factory=list, description="Tool results")

class EnhancedMemorySchema(BaseModel):
    """Enhanced memory schema with KG and TNT features."""

    # Core fields
    content: str = Field(description="Memory content")
    memory_id: str = Field(description="Unique identifier")
    timestamp: datetime = Field(default_factory=datetime.now, description="Creation time")

    # KG enhancement
    entities: list[dict] = Field(default_factory=list, description="Extracted entities")
    relationships: list[dict] = Field(default_factory=list, description="Entity relationships")
    entity_confidence: dict[str, float] = Field(default_factory=dict, description="Entity confidence")

    # TNT categorization
    categories: list[str] = Field(default_factory=list, description="Memory categories")
    category_confidence: dict[str, float] = Field(default_factory=dict, description="Category confidence")
    taxonomy_path: list[str] = Field(default_factory=list, description="Hierarchical path")

    # Consolidation
    summary: str | None = Field(default=None, description="Memory summary")
    consolidated_from: list[str] = Field(default_factory=list, description="Source memory IDs")
    consolidation_level: int = Field(default=0, description="Consolidation steps")

    # Retrieval optimization
    embeddings: list[float] = Field(default_factory=list, description="Vector embeddings")
    keywords: list[str] = Field(default_factory=list, description="Keywords")
    importance_score: float = Field(default=0.5, description="Importance score")

    # Access patterns
    access_count: int = Field(default=0, description="Access count")
    last_accessed: datetime | None = Field(default=None, description="Last access time")
    access_context: list[str] = Field(default_factory=list, description="Access contexts")

    # Metadata
    source: str = Field(default="conversation", description="Memory source")
    user_id: str | None = Field(default=None, description="User ID")
    session_id: str | None = Field(default=None, description="Session ID")
    tags: list[str] = Field(default_factory=list, description="User tags")
```

### 4. Usage Pattern

```python
# Creating and using LTM Agent
from haive.agents.ltm import LTMAgent
from langchain_core.messages import HumanMessage

# Create LTM agent with proper Haive patterns
ltm_agent = LTMAgent(
    name="Long Term Memory Agent",
    enable_kg_processing=True,
    enable_categorization=True,
    enable_consolidation=True,
    storage_namespace=("ltm", "user_123"),
    set_schema=True,  # Auto-generate schemas from engines
    persistence={"type": "postgres", "connection": "..."},  # Haive persistence
    add_store=True,  # Add state store
    verbose=True
)

# Use the agent
result = ltm_agent.invoke({
    "messages": [
        HumanMessage(content="I love hiking and prefer morning workouts")
    ]
})

print(f"Stored memories: {result['stored_memory_ids']}")
print(f"Categories: {result['categories']}")
```

## Key Corrections Made:

1. **Proper Base Class**: Use `haive.agents.base.agent.Agent` (not core engine agent)
2. **No Generic Types**: Just `Agent`, not `Agent[ConfigType]`
3. **Lifecycle Hooks**: Use `setup_agent()` for initialization, `build_graph()` for workflow
4. **Engine Management**: Engines go in `engines` dict, auto-handled by base class
5. **Node Configurations**: Use `EngineNodeConfig`, `ToolNodeConfig` for graph nodes
6. **Schema Generation**: Let base class handle with `set_schema=True`
7. **Persistence Integration**: Use inherited mixins for persistence and state management

This approach properly follows Haive's agent patterns while integrating LangMem's memory management capabilities.
