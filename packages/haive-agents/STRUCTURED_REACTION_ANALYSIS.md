# Structured Reaction Analysis: Proper Agent Architecture

## 🔍 Current Problems Identified

### 1. Inconsistent Type Usage

```python
# ❌ Current inconsistent patterns:
class SimpleAgent(Agent):  # Not using GenericAgent
    engine: AugLLMConfig = Field(...)  # Should be generic

class SimpleRAGAgent(SequentialAgent):  # Should use generics
    # Manual composition without type bounds

# ❌ Mixed concerns - LLM config instead of engine types:
def create_hyde_enhancer() -> StructuredOutputEnhancer:
    # Takes LLMConfig instead of proper engine types
```

### 2. Missing Generalizability

```python
# ❌ Not leveraging GenericAgent infrastructure:
class GenericAgent[TInput, TOutput, TState](Agent, Generic[...], ABC):
    # Sophisticated auto-configuration EXISTS but not used!

# ❌ Manual schema modification instead of using type system:
def _modify_engine_schema(self) -> None:
    # Manual schema composer usage instead of generics
```

### 3. Should Be Multi-Agent, Not Single Engine

```python
# ❌ Current: Single engine approach
engine: AugLLMConfig = Field(...)

# ✅ Should be: Multi-engine approach
engines: Dict[str, Engine] = Field(...)
retriever_engine: BaseRetrieverConfig = Field(...)
llm_engine: AugLLMConfig = Field(...)
```

## 🎯 Proper Architecture Using Base Agent

### 1. Type-Safe Engine Specialization

```python
from typing import TypeVar, Generic, Protocol
from haive.agents.base.generic_agent import GenericAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.retriever import BaseRetrieverConfig

# Define engine type bounds
TLLMEngine = TypeVar("TLLMEngine", bound=AugLLMConfig)
TRetrieverEngine = TypeVar("TRetrieverEngine", bound=BaseRetrieverConfig)
TInput = TypeVar("TInput", bound=BaseModel)
TOutput = TypeVar("TOutput", bound=BaseModel)
TState = TypeVar("TState", bound=BaseModel)

class LLMAgent[TLLMEngine, TInput, TOutput, TState](
    GenericAgent[TInput, TOutput, TState]
):
    """Type-safe LLM agent with proper generics."""

    # Use engines dict, not single engine
    def setup_agent(self):
        """Setup with type constraints."""
        if not any(isinstance(eng, AugLLMConfig) for eng in self.engines.values()):
            raise TypeError("LLMAgent requires at least one AugLLMConfig engine")

    @property
    def llm_engine(self) -> TLLMEngine:
        """Get the primary LLM engine with type safety."""
        for engine in self.engines.values():
            if isinstance(engine, AugLLMConfig):
                return engine
        raise ValueError("No LLM engine found")

class RetrieverAgent[TRetrieverEngine, TInput, TOutput, TState](
    GenericAgent[TInput, TOutput, TState]
):
    """Type-safe retriever agent."""

    def setup_agent(self):
        if not any(isinstance(eng, BaseRetrieverConfig) for eng in self.engines.values()):
            raise TypeError("RetrieverAgent requires at least one BaseRetrieverConfig engine")

    @property
    def retriever_engine(self) -> TRetrieverEngine:
        for engine in self.engines.values():
            if isinstance(engine, BaseRetrieverConfig):
                return engine
        raise ValueError("No retriever engine found")
```

### 2. Multi-Agent RAG with Type Safety

```python
from haive.agents.multi.base import SequentialAgent

class RAGAgent[TLLMEngine: AugLLMConfig, TRetrieverEngine: BaseRetrieverConfig, TInput, TOutput](
    SequentialAgent[TInput, TOutput, RAGState]
):
    """Type-safe RAG composition using multi-agent pattern."""

    def __init__(
        self,
        llm_engine: TLLMEngine,
        retriever_engine: TRetrieverEngine,
        **kwargs
    ):
        # Create typed sub-agents
        retriever = RetrieverAgent[TRetrieverEngine, TInput, RetrievalOutput, RAGState](
            engines={"retriever": retriever_engine},
            name="RAG Retriever"
        )

        generator = LLMAgent[TLLMEngine, RetrievalOutput, TOutput, RAGState](
            engines={"llm": llm_engine},
            name="RAG Generator"
        )

        # Multi-agent composition with type safety
        super().__init__(
            agents=[retriever, generator],
            **kwargs
        )

    @classmethod
    def from_documents(
        cls,
        documents: List[Document],
        llm_config: LLMConfig,
        embedding_config: Optional[EmbeddingConfig] = None,
        **kwargs
    ) -> "RAGAgent":
        """Factory method with proper engine separation."""

        # Create retriever engine from documents + embeddings
        retriever_engine = BaseRetrieverConfig.from_documents(
            documents=documents,
            embedding_config=embedding_config or DEFAULT_EMBEDDING_CONFIG
        )

        # Create LLM engine
        llm_engine = AugLLMConfig(
            llm_config=llm_config,
            prompt_template=RAG_ANSWER_STANDARD
        )

        return cls(
            llm_engine=llm_engine,
            retriever_engine=retriever_engine,
            **kwargs
        )
```

### 3. Generic Structured Output Enhancement

```python
from haive.agents.base.generic_agent import GenericAgent

class StructuredOutputAgent[TEngine: Engine, TStructuredModel: BaseModel, TInput, TOutput](
    GenericAgent[TInput, TOutput, MessagesState]
):
    """Generic structured output agent using base agent properly."""

    structured_model: Type[TStructuredModel] = Field(...)

    def setup_agent(self):
        """Leverage base agent's schema auto-derivation."""
        # Get primary engine
        primary_engine = self.main_engine
        if not primary_engine:
            raise ValueError("StructuredOutputAgent requires a primary engine")

        # Configure structured output on engine
        if hasattr(primary_engine, 'structured_output_model'):
            primary_engine.structured_output_model = self.structured_model
            primary_engine.structured_output_version = "v1"

        # Let base agent handle schema derivation automatically
        # This leverages the sophisticated schema system already built!

# Usage with proper generics:
class HyDEAnalysisAgent(StructuredOutputAgent[AugLLMConfig, HyDEResult, QueryInput, HyDEOutput]):
    """HyDE analysis with proper type bounds."""

    def build_graph(self) -> BaseGraph:
        # Build graph using typed engines
        return self._build_structured_output_graph()

# Multi-agent composition:
class EnhancedRAGWorkflow[TAnalysisModel: BaseModel](
    SequentialAgent[QueryInput, AnalysisOutput, RAGState]
):
    """Generic enhanced RAG with analysis."""

    @classmethod
    def create_workflow(
        cls,
        documents: List[Document],
        llm_config: LLMConfig,
        analysis_model: Type[TAnalysisModel],
        **kwargs
    ):
        # Create base RAG
        base_rag = RAGAgent.from_documents(documents, llm_config)

        # Create analysis enhancement
        analyzer = StructuredOutputAgent[AugLLMConfig, TAnalysisModel, RAGOutput, AnalysisOutput](
            engines={"analyzer": AugLLMConfig(llm_config=llm_config, ...)},
            structured_model=analysis_model
        )

        return cls(agents=[base_rag, analyzer], **kwargs)
```

### 4. Proper State Schema Usage

```python
# ✅ Using base agent's schema composition properly:
from haive.core.schema.agent_schema_composer import AgentSchemaComposer

class MessagesState(BaseModel):
    messages: List[BaseMessage] = Field(default_factory=list)

class RetrievalState(MessagesState):
    query: str = Field(...)
    retrieved_documents: List[Document] = Field(default_factory=list)

class AnalysisState(RetrievalState):
    analysis_result: Optional[BaseModel] = Field(default=None)

# Agents automatically get proper schema composition via GenericAgent
```

## 🏗️ Benefits of Proper Architecture

### 1. Type Safety

- Compile-time checking of engine compatibility
- Generic constraints prevent mixing incompatible types
- Proper separation of LLM vs Retriever vs Multi concerns

### 2. Leverages Existing Infrastructure

- Uses `GenericAgent` auto-configuration
- Uses `AgentSchemaComposer` for compatibility
- Uses base agent's sophisticated schema derivation

### 3. Consistency

- All agents follow same pattern: `GenericAgent[TInput, TOutput, TState]`
- Engine management through `engines` dict, not single `engine`
- Multi-agent composition for complex workflows

### 4. Generalizability

- `StructuredOutputAgent` works with any engine + model combination
- `RAGAgent` can be specialized for different engine types
- Enhancement patterns are reusable across agent types

## 🎯 Reaction: We Need Consistency

**The real issue**: We built sophisticated infrastructure (`GenericAgent`, compatibility systems, schema composition) but we're not using it consistently!

**The solution**:

1. Refactor existing agents to use `GenericAgent` properly
2. Use engine type bounds and generics throughout
3. Multi-agent composition instead of single-engine approaches
4. Leverage the schema auto-derivation instead of manual modification

This gives us the type safety, generalizability, and consistency we need while using the sophisticated infrastructure that already exists.
