# Corrected Architectural Understanding

**Created**: 2025-01-07  
**Purpose**: Corrected understanding of Haive's three-layer architecture  
**Status**: Critical architectural correction

## 🚨 Key Correction: Workflows DO Have Engines

### Previous Misunderstanding

I incorrectly stated:

- ❌ "Workflows have no engines"
- ❌ "Pure orchestration without any engine"

### Correct Understanding

- ✅ **Workflows CAN have engines** - Just not LLM engines (AugLLMConfig)
- ✅ **Workflows use non-LLM engines** for specific tasks
- ✅ **Agents specifically add LLM capability** via AugLLMConfig

## 🏗️ Corrected Three-Layer Architecture

### Layer 1: Workflow (Orchestration + Non-LLM Engines)

**Purpose**: Pure orchestration with optional non-LLM processing engines

**Can Have Engines**:

- `PromptTemplateEngine` - Template formatting
- `DocumentEngine` - Document processing
- `ToolEngine` - Tool execution
- `TransformerEngine` - Data transformation
- `SplitterEngine` - Text splitting
- `LoaderEngine` - Data loading

**Cannot Have**:

- `AugLLMConfig` - LLM engines are Agent-specific

```python
class DataProcessingWorkflow(Workflow):
    # Can have document processing engine
    document_engine: DocumentEngine

    # Can have transformer engine
    transformer_engine: TransformerEngine

    # But NO LLM engine
    # engine: AugLLMConfig  # ❌ Not allowed in Workflow
```

### Layer 2: Agent (Workflow + LLM Engine)

**Purpose**: Adds LLM capability to workflow orchestration

**Key Addition**:

- `engine: AugLLMConfig` - Required LLM engine
- `engines: dict[str, Engine]` - Can have multiple engines

```python
class Agent(Workflow):  # Inherits orchestration capability
    engine: AugLLMConfig  # ✅ Adds LLM capability
    engines: dict[str, Engine]  # Can mix engine types
```

### Layer 3: MultiAgent (Agent + Agent Coordination)

**Purpose**: Coordinates multiple agents

**Key Addition**:

- `agents: dict[str, Agent]` - Multiple agent management

```python
class MultiAgent(Agent):  # Has LLM for coordination
    agents: dict[str, Agent]  # Manages other agents
```

## 📊 Engine Type Hierarchy

### Non-LLM Engines (Workflow-Compatible)

```
InvokableEngine (Base)
├── PromptTemplateEngine  # Template formatting
├── DocumentEngine         # Document processing
│   ├── LoaderEngine      # Loading documents
│   ├── SplitterEngine    # Splitting text
│   └── TransformerEngine # Transforming data
├── ToolEngine            # Tool execution
├── ValidationEngine      # Data validation
└── RoutingEngine        # Routing decisions
```

### LLM Engines (Agent-Only)

```
InvokableEngine (Base)
└── LLMEngine
    └── AugLLMConfig      # Full LLM capability
        ├── OpenAI
        ├── Anthropic
        ├── Azure
        └── Custom
```

## 🎯 Why This Matters

### 1. Separation of Concerns

- **Workflows** handle non-LLM processing (documents, tools, routing)
- **Agents** add intelligence via LLM
- **MultiAgents** coordinate intelligent agents

### 2. Progressive Enhancement

```python
# Start with pure processing
workflow = DocumentWorkflow(
    document_engine=DocumentEngine(),
    transformer_engine=TransformerEngine()
)

# Add intelligence
agent = DocumentAgent(
    document_engine=DocumentEngine(),
    engine=AugLLMConfig()  # Adds LLM
)

# Scale to multiple agents
multi = DocumentMultiAgent(
    engine=AugLLMConfig(),  # Coordinator LLM
    agents={
        "analyzer": AnalyzerAgent(),
        "summarizer": SummarizerAgent()
    }
)
```

### 3. Engine Composition Patterns

**Workflow with Multiple Non-LLM Engines**:

```python
class ETLWorkflow(Workflow):
    loader_engine: LoaderEngine
    transformer_engine: TransformerEngine
    validator_engine: ValidationEngine
    # No LLM needed for ETL
```

**Agent with Mixed Engines**:

```python
class SmartETLAgent(Agent):
    engine: AugLLMConfig  # LLM for decisions
    engines: dict[str, Engine] = {
        "loader": LoaderEngine(),
        "transformer": TransformerEngine(),
        "llm": AugLLMConfig()  # Also in engines dict
    }
```

## 🔄 State and Engine Relationship

### Workflows Store Non-LLM Engines in State

```python
class WorkflowState(StateSchema):
    # Non-LLM engines in state
    document_engines: dict[str, DocumentEngine]
    tool_engines: dict[str, ToolEngine]
    # But no LLM engines here
```

### Agents Add LLM Engines to State

```python
class AgentState(StateSchema):
    # Both LLM and non-LLM engines
    engine: AugLLMConfig  # Main LLM
    engines: dict[str, Engine]  # Mixed types
```

## 💡 Design Implications

### 1. Engine Hot-Swapping

- **Workflows** can hot-swap document/tool engines
- **Agents** can hot-swap LLM engines
- **Both** benefit from state-driven architecture

### 2. Recompilation Triggers

- Changing ANY engine type triggers recompilation
- Soft recompilation works for all engine swaps
- Engine type doesn't affect recompilation strategy

### 3. Testing Strategy

- **Workflows** test with real document/tool engines
- **Agents** test with real LLM engines
- **No mocks** for any engine type

## 🚀 Corrected Design Patterns

### Pattern 1: Workflow-First Development

```python
# Start with non-LLM workflow
class DataProcessor(Workflow):
    document_engine: DocumentEngine

    async def execute(self, docs):
        # Pure processing, no LLM
        return self.document_engine.process(docs)

# Later add LLM if needed
class SmartDataProcessor(Agent):
    engine: AugLLMConfig  # Now has LLM
    document_engine: DocumentEngine

    async def execute(self, docs):
        # Use LLM for intelligent processing
        processed = self.document_engine.process(docs)
        enhanced = await self.engine.enhance(processed)
        return enhanced
```

### Pattern 2: Engine Composition

```python
# Compose different engine types
class HybridWorkflow(Workflow):
    engines: dict[str, Engine] = {
        "prompt": PromptTemplateEngine(),
        "document": DocumentEngine(),
        "tool": ToolEngine(),
        # No "llm" here - that's Agent territory
    }
```

### Pattern 3: Progressive Intelligence

```python
# Level 1: Pure processing
workflow = Workflow(engines={"doc": DocumentEngine()})

# Level 2: Add intelligence
agent = Agent(
    engines={"doc": DocumentEngine()},
    engine=AugLLMConfig()  # Intelligence layer
)

# Level 3: Coordinate multiple intelligent agents
multi = MultiAgent(
    engine=AugLLMConfig(),  # Coordinator
    agents={"a1": agent1, "a2": agent2}
)
```

## 📈 Architectural Benefits

1. **Clear Boundaries**: Non-LLM vs LLM processing
2. **Cost Optimization**: Use LLM only when needed
3. **Performance**: Workflows avoid LLM overhead
4. **Testability**: Test non-LLM logic separately
5. **Composability**: Mix and match engine types

## 🔍 Implementation Examples

### Example 1: Document Processing Pipeline

```python
# Pure document workflow (no LLM)
class DocumentPipeline(Workflow):
    loader: LoaderEngine = LoaderEngine()
    splitter: SplitterEngine = SplitterEngine()
    transformer: TransformerEngine = TransformerEngine()

    async def execute(self, file_path):
        docs = await self.loader.load(file_path)
        chunks = await self.splitter.split(docs)
        transformed = await self.transformer.transform(chunks)
        return transformed
```

### Example 2: Intelligent Document Analysis

```python
# Add LLM for intelligent analysis
class DocumentAnalyzer(Agent):
    engine: AugLLMConfig = AugLLMConfig()  # LLM for analysis
    document_pipeline: DocumentPipeline = DocumentPipeline()

    async def execute(self, file_path):
        # Use workflow for processing
        processed = await self.document_pipeline.execute(file_path)

        # Use LLM for analysis
        analysis = await self.engine.analyze(processed)
        return analysis
```

### Example 3: Multi-Agent Document System

```python
# Coordinate multiple document agents
class DocumentSystem(MultiAgent):
    engine: AugLLMConfig = AugLLMConfig()  # For coordination

    agents: dict[str, Agent] = {
        "extractor": DataExtractor(),  # Has own LLM
        "analyzer": DocumentAnalyzer(),  # Has own LLM
        "summarizer": Summarizer()  # Has own LLM
    }

    async def execute(self, file_path):
        # Coordinate agents intelligently
        extraction = await self.agents["extractor"].execute(file_path)
        analysis = await self.agents["analyzer"].execute(extraction)
        summary = await self.agents["summarizer"].execute(analysis)
        return summary
```

## 🎯 Key Takeaways

1. **Workflows HAVE engines** - Just not LLM engines
2. **Engine diversity is intentional** - Different engines for different tasks
3. **LLM is one engine type** - Special, but not the only one
4. **State holds ALL engine types** - Enables hot-swapping
5. **Architecture is about capability layers** - Not about presence/absence of engines

---

**Bottom Line**: The three-layer architecture is about WHAT KIND of engines, not WHETHER there are engines. Workflows use non-LLM engines, Agents add LLM engines, MultiAgents coordinate LLM-powered agents.
