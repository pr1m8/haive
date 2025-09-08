# Deep Dive Findings - Tool Schemas and Engine Ecosystem

**Created**: 2025-01-06
**Purpose**: Document findings from deep dive into tool schemas and various engine types
**Status**: Analysis Complete

## 🔍 Tool System Architecture

### Tool Type System (`engine/tool/types.py`)

The framework has a sophisticated tool type system with:

```python
# Universal tool type definition
ToolLike: TypeAlias = (
    BaseTool | StructuredTool | type[BaseTool] |
    BaseModel | type[BaseModel] | Callable[..., Any] | BaseToolkit
)
```

### Tool Classification

1. **ToolType Enum**: Implementation types
   - LANGCHAIN_TOOL
   - PYDANTIC_MODEL
   - FUNCTION
   - STRUCTURED_TOOL
   - TOOLKIT
   - RETRIEVER_TOOL
   - VALIDATION_TOOL
   - STORE_TOOL

2. **ToolCategory Enum**: High-level categories
   - RETRIEVAL
   - COMPUTATION
   - COMMUNICATION
   - TRANSFORMATION
   - VALIDATION
   - COORDINATION
   - MEMORY
   - SEARCH
   - GENERATION

3. **ToolCapability Enum**: Fine-grained capabilities
   - Execution: INTERRUPTIBLE, ASYNC_CAPABLE, STREAMING, BATCH_CAPABLE
   - State: READS_STATE, WRITES_STATE, STATE_AWARE, TO_STATE, FROM_STATE
   - Output: STRUCTURED_OUTPUT, VALIDATED_OUTPUT
   - Special: RETRIEVER, VALIDATOR, TRANSFORMER, ROUTED, STORE

### ToolProperties Model

Comprehensive tool metadata with 20+ fields:

- Core identification (name, type, category)
- Capability set
- State interaction properties
- Execution properties
- Schema information
- Performance hints

**Key Insight**: Tools are treated as first-class citizens with rich metadata for routing and execution decisions.

## 🏗️ Engine Type Hierarchy

### Core Engine Types (from `EngineType` enum)

1. **LLM** - Language model engines
2. **VECTOR_STORE** - Vector database engines
3. **RETRIEVER** - Information retrieval engines
4. **TOOL** - Tool execution engines
5. **EMBEDDINGS** - Text embedding engines
6. **AGENT** - Agent orchestration engines
7. **DOCUMENT_LOADER** - Document loading engines
8. **DOCUMENT_TRANSFORMER** - Document transformation engines
9. **DOCUMENT_SPLITTER** - Document splitting engines
10. **OUTPUT_PARSER** - Output parsing engines
11. **PROMPT** - Prompt template engines

### Engine Class Hierarchy

```
Engine (Abstract Base)
├── InvokableEngine (Can be called)
│   ├── AugLLMConfig (2600+ lines monolith)
│   ├── ToolEngine
│   ├── PromptTemplateEngine
│   ├── OutputParserEngine
│   ├── DocumentTransformerEngine
│   ├── DocumentSplitterEngine
│   └── BaseRetrieverConfig
└── NonInvokableEngine (Cannot be called directly)
    └── (Used for embeddings, vector stores)
```

## 📊 Specific Engine Implementations

### 1. ToolEngine (`engine/tool/engine.py`)

**Features**:

- Universal typing with `ToolLike`
- Automatic tool analysis
- Capability-based routing
- State interaction tracking
- Parallel execution support

**I/O Schema**:

```python
# Input fields
- messages: List[BaseMessage]
- state: Dict[str, Any]
- tool_choice: Optional[str | List[str]]
- required_capabilities: Optional[List[ToolCapability]]

# Output fields
- messages: List[BaseMessage]  # With tool results
- tool_results: List[Dict[str, Any]]
- state: Dict[str, Any]  # Updated state
- execution_metadata: Dict[str, Any]
```

### 2. RetrieverEngine (`engine/retriever/retriever.py`)

**Massive Provider Support**: 40+ retriever configurations!

- ArxivRetriever, AzureAISearchRetriever, BM25Retriever
- ElasticsearchRetriever, KendraRetriever, MilvusRetriever
- PineconeHybridSearchRetriever, QdrantSparseVectorRetriever
- WikipediaRetriever, YouRetriever, ZepRetriever
- And many more...

**I/O Schema**:

```python
# Input (RetrieverInput)
- query: str
- k: Optional[int]  # Number of docs
- filter: Optional[Dict[str, Any]]
- search_type: Optional[str]
- score_threshold: Optional[float]

# Output (RetrieverOutput)
- retrieved_documents: Sequence[Document]
```

### 3. PromptTemplateEngine

**Responsibility**: Format prompts with variables
**I/O**: Dict[str, Any] → Formatted prompt (str or messages)

### 4. OutputParserEngine

**Responsibility**: Parse LLM outputs into structured data
**Types**: Pydantic, JSON, custom parsers

## 🔄 Engine-Schema-Tool Integration

### Current Integration Points

1. **StateSchema ↔ Engine**
   - `__engine_io_mappings__` maps schema fields to engine I/O
   - Engines stored in `engines` dict field
   - Primary `engine` field for main engine

2. **Engine ↔ Tools**
   - AugLLMConfig manages tool binding
   - Tool routes stored in config
   - Tool metadata tracked for routing

3. **Schema ↔ Tools**
   - Tools not directly in schema
   - Tools passed through engine configuration
   - State interaction through capabilities

## 🚨 Key Observations

### 1. Over-Engineering Patterns

- **70+ schema files** for state management
- **40+ retriever configurations** (do we need all?)
- **2600+ lines in AugLLMConfig** (massive bloat)
- **Multiple inheritance chains** everywhere

### 2. Good Design Elements

- **Tool capability system** is well thought out
- **Engine type hierarchy** makes sense
- **I/O schemas** provide type safety
- **Retriever abstraction** is clean

### 3. Inconsistencies

- **Engine sizes vary wildly**: Base Engine (~200 lines) vs AugLLMConfig (2600+ lines)
- **Some engines are simple**, others are monoliths
- **Tool management** split between multiple places
- **State interaction** not standardized

## 💡 Architecture Insights

### 1. Separation of Concerns Needed

**Current**: Everything mixed together
**Better**: Clear boundaries between:

- Configuration (settings)
- Runtime (execution)
- Schema (data structure)
- Tools (capabilities)

### 2. Tool System is Actually Good

The tool type system with capabilities is well-designed:

- Clear categorization
- Rich metadata
- Routing support
- State awareness

**This should be preserved in refactoring!**

### 3. Provider Explosion

40+ retriever configs suggests:

- Need for plugin architecture
- Dynamic provider loading
- Common base patterns

### 4. Schema-Engine Coupling

The tight coupling between schemas and engines causes:

- Recompilation triggers
- Complex validation
- Circular dependencies

## 🎯 Refactoring Recommendations

### 1. Preserve Good Parts

- **Keep**: Tool capability system
- **Keep**: Engine type hierarchy
- **Keep**: I/O schema pattern
- **Enhance**: Make consistent across all engines

### 2. Break Apart Monoliths

- **AugLLMConfig** → LLMSettings + PromptManager + ToolManager + OutputHandler
- **StateSchema** → StateData + FieldManager + DirtyTracker

### 3. Standardize Engine Sizes

- **Target**: 200-500 lines per engine
- **Pattern**: Composition over inheritance
- **Focus**: Single responsibility

### 4. Plugin Architecture for Providers

Instead of 40+ retriever configs in core:

```python
class RetrieverRegistry:
    def register_provider(name: str, config_class: Type[BaseRetrieverConfig]):
        # Dynamic registration

    def load_provider(name: str) -> BaseRetrieverConfig:
        # Lazy loading
```

### 5. Decouple Schema from Engine

Schemas should not know about engines:

```python
# Bad (current)
class StateSchema:
    engine: Engine
    engines: Dict[str, Engine]
    __engine_io_mappings__: Dict

# Good (proposed)
class StateData:
    # Just data, no engine knowledge

class EngineManager:
    # Manages engines separately
```

## 📈 Metrics Summary

- **Engine Types**: 11 distinct types
- **Tool Capabilities**: 15+ defined
- **Retriever Providers**: 40+ configurations
- **Tool Categories**: 10 categories
- **ToolProperties Fields**: 20+ metadata fields

## 🔗 Related Patterns

### Tool as First-Class Citizen

Tools are not just functions but rich objects with:

- Type classification
- Capability declaration
- State interaction patterns
- Performance characteristics

### Engine as Factory

Engines follow factory pattern:

- Configuration phase (Engine class)
- Creation phase (create_runnable)
- Execution phase (invoke/ainvoke)

### Schema as Contract

Schemas define contracts between components:

- Input requirements
- Output guarantees
- State transitions

## 🚀 Next Steps

1. **Preserve tool system** - It's actually well-designed
2. **Refactor engines** - Apply consistent patterns
3. **Simplify schemas** - Remove engine coupling
4. **Create plugin system** - For provider explosion
5. **Document patterns** - Clear usage guidelines

---

**Key Takeaway**: The framework has both excellent design elements (tool system) and problematic ones (monolithic configs). Refactoring should preserve the good while fixing the bad.
