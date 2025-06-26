# Engine Usage in Haive

## Core Engine Concepts

Engines in Haive are configurable, serializable factory objects that produce runtime components. They provide a consistent interface for creating and using AI components like LLMs, retrievers, and vector stores.

## Engine Base Class

All engines inherit from the `Engine` base class:

```python
from haive.core.engine.base import Engine, EngineType, InvokableEngine
from pydantic import Field
from typing import Dict, Any, Tuple, Type

class MyEngine(InvokableEngine):
    engine_type = EngineType.LLM

    # Engine-specific parameters
    model: str = Field(default="gpt-4o", description="Model identifier")
    temperature: float = Field(default=0.7, description="Sampling temperature")

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Define required input fields."""
        return {
            "prompt": (str, None),
            "context": (Dict[str, Any], {})
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Define produced output fields."""
        return {
            "completion": (str, None),
            "metadata": (Dict[str, Any], {})
        }

    def create_runnable(self, runnable_config=None) -> Any:
        """Create the actual runtime object."""
        # Extract configuration
        params = self.apply_runnable_config(runnable_config)

        # Apply configuration over defaults
        model = params.get("model", self.model)
        temperature = params.get("temperature", self.temperature)

        # Create and return actual LLM instance
        return create_llm_instance(model, temperature)
```

## AugLLM Engine

The AugLLM engine provides enhanced LLM capabilities with integrated tools, prompts, and structured outputs:

```python
from haive.core.engine.aug_llm import AugLLMConfig
from pydantic import BaseModel

# Define structured output
class AnalysisOutput(BaseModel):
    summary: str
    key_points: List[str]
    sentiment: str

# Create AugLLM configuration
llm_config = AugLLMConfig(
    name="analysis_llm",
    llm_config=AzureLLMConfig(model="gpt-4o"),
    system_message="You are a text analysis assistant.",
    tools=[search_tool, calculator_tool],
    structured_output_model=AnalysisOutput
)

# Create runnable
llm = llm_config.create_runnable()

# Execute with input
result = llm.invoke("Analyze this quarterly financial report...")

# Access structured output
summary = result.summary
key_points = result.key_points
```

## Retriever Engine

Retriever engines provide a consistent interface for document retrieval:

```python
from haive.core.engine.retriever import VectorStoreRetrieverConfig
from haive.core.engine.vectorstore import VectorStoreConfig

# Create vector store config
vs_config = VectorStoreConfig(
    name="knowledge_base",
    provider="chroma",
    connection_string="...",
    embedding_model="text-embedding-3-large"
)

# Create retriever config
retriever_config = VectorStoreRetrieverConfig(
    name="semantic_retriever",
    vector_store_config=vs_config,
    search_type="similarity",
    k=5,
    search_kwargs={"score_threshold": 0.7}
)

# Create runnable
retriever = retriever_config.create_runnable()

# Retrieve documents
docs = retriever.get_relevant_documents("How does photosynthesis work?")
```

## VectorStore Engine

VectorStore engines provide access to vector databases for similarity search:

```python
from haive.core.engine.vectorstore import VectorStoreConfig

# Create vector store config
vs_config = VectorStoreConfig(
    name="document_store",
    provider="pinecone",
    connection_string="pinecone://...",
    embedding_model="text-embedding-3-large"
)

# Create vector store
vs = vs_config.create_runnable()

# Add documents
vs.add_documents(documents)

# Search directly
results = vs.similarity_search("quantum computing applications", k=5)
```

## Agent Engine

Agent engines manage the creation and execution of agent workflows:

```python
from haive.core.engine.agent.config import AgentConfig
from haive.agents.react.config import ReactAgentConfig

# Create agent config
agent_config = ReactAgentConfig(
    name="research_agent",
    llm_config=llm_config,
    tools=[search_tool, calculator_tool, retriever_tool],
    persistence_config=MemoryCheckpointerConfig()
)

# Create agent
agent = agent_config.create_runnable()

# Invoke agent
response = agent.invoke("Research the impact of climate change on crop yields")
```

## Engine Registration and Discovery

Engines can be registered for easy discovery:

```python
from haive.core.engine.base.registry import EngineRegistry

# Register an engine instance
registry = EngineRegistry.get_instance()
registry.register(my_engine)

# Retrieve by ID
retrieved_engine = registry.get_by_id(my_engine.id)

# Find by type and criteria
llm_engines = registry.find_by_type(EngineType.LLM)
```

## Runtime Configuration

Engines support runtime configuration through `RunnableConfig`:

```python
from langchain_core.runnables import RunnableConfig

# Create runtime configuration
config = RunnableConfig(
    configurable={
        "engine_configs": {
            "my_llm": {
                "temperature": 0.9,
                "max_tokens": 500
            }
        }
    }
)

# Apply at runtime
result = llm_engine.invoke(input_data, runnable_config=config)
```

## Serialization and Persistence

Engines are fully serializable for persistence:

```python
# Convert to dictionary
engine_dict = engine.to_dict()

# Convert to JSON
engine_json = engine.to_json()

# Recreate from dictionary
new_engine = Engine.from_dict(engine_dict)

# Recreate from JSON
new_engine = Engine.from_json(engine_json)
```

## Engine Composition

Engines can be composed and used together:

```python
# Create a RAG pipeline
retriever = retriever_config.create_runnable()
llm = llm_config.create_runnable()

def rag_pipeline(query):
    # Retrieve documents
    docs = retriever.get_relevant_documents(query)

    # Format context
    context = "\n\n".join([doc.page_content for doc in docs])

    # Generate response with context
    response = llm.invoke({
        "question": query,
        "context": context
    })

    return response
```
