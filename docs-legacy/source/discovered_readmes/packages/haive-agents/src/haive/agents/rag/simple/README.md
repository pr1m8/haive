# Simple RAG Agent

Simple Retrieval-Augmented Generation (RAG) agent that combines document retrieval with answer generation in a clean, sequential workflow.

## Overview

The `SimpleRAGAgent` is a Pydantic class that extends `EnhancedMultiAgentV4` to provide a straightforward RAG implementation:

1. **BaseRAGAgent** retrieves relevant documents
2. **AnswerAgent** generates answers based on retrieved documents
3. **Sequential execution** ensures proper data flow

## Architecture

```python
SimpleRAGAgent = BaseRAGAgent → AnswerAgent (sequential)
```

## Usage

### Basic Usage

```python
from haive.agents.rag.simple.agent import SimpleRAGAgent

# Create instance with defaults
rag_agent = SimpleRAGAgent(name="my_rag")

# Execute RAG workflow
result = rag_agent.run("What is machine learning?")
print(result)
```

### Custom Configuration

```python
from haive.agents.rag.simple.agent import SimpleRAGAgent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.rag.simple.answer_agent import AnswerAgent

# Create with custom agents
rag_agent = SimpleRAGAgent(
    name="custom_rag",
    agents=[
        BaseRAGAgent(name="my_retriever"),
        AnswerAgent(name="my_answerer")
    ],
    execution_mode="sequential"
)
```

## Components

### BaseRAGAgent

- **Purpose**: Document retrieval using vector similarity
- **Default Engine**: HuggingFace embeddings with in-memory vector store
- **Output**: Retrieved documents with context

### AnswerAgent

- **Purpose**: Generate structured answers from retrieved documents
- **Engine**: SimpleAgentV3 with AugLLMConfig
- **Features**:
  - System message for RAG context
  - Human prompt template with `{retrieved_documents}` and `{query}`
  - Detailed answering instructions

## Configuration

### Default Settings

```python
class SimpleRAGAgent(EnhancedMultiAgentV4):
    agents: List = Field(
        default_factory=lambda: [
            BaseRAGAgent(name="retriever"),     # HuggingFace + InMemory
            AnswerAgent(name="answerer")        # SimpleAgentV3 + AugLLMConfig
        ]
    )
    execution_mode: str = Field(default="sequential")
```

### Customization Options

1. **Custom Vector Store**: Provide custom `BaseRAGAgent` with different engine
2. **Custom LLM**: Provide custom `AnswerAgent` with different AugLLMConfig
3. **Custom Prompts**: Override prompt templates in AnswerAgent

## Examples

### With Custom Vector Store

```python
from haive.core.engine.vectorstore.vectorstore import VectorStoreConfig
from haive.core.engine.embedding.providers.HuggingFaceEmbeddingConfig import HuggingFaceEmbeddingConfig

# Custom vector store config
vector_config = VectorStoreConfig(
    name="custom_store",
    provider="FAISS",
    embedding_config=HuggingFaceEmbeddingConfig(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
)

# Create RAG with custom store
rag_agent = SimpleRAGAgent(
    name="custom_rag",
    agents=[
        BaseRAGAgent(name="retriever", engine=vector_config),
        AnswerAgent(name="answerer")
    ]
)
```

### With Custom Answer Agent

```python
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate

# Custom answer agent
custom_answer_agent = AnswerAgent(
    name="custom_answerer",
    engine=AugLLMConfig(
        temperature=0.3,
        system_message="You are a precise technical assistant."
    ),
    prompt_template=ChatPromptTemplate.from_messages([
        ("system", "Answer based on technical documents."),
        ("human", "Documents: {retrieved_documents}\n\nQuestion: {query}")
    ])
)

rag_agent = SimpleRAGAgent(
    name="technical_rag",
    agents=[
        BaseRAGAgent(name="retriever"),
        custom_answer_agent
    ]
)
```

### Testing

```python
def test_simple_rag_agent():
    """Test SimpleRAGAgent with real components - NO MOCKS."""
    rag_agent = SimpleRAGAgent(name="test_rag")

    # Real execution
    result = rag_agent.run("What is Python?")

    # Verify structure
    assert isinstance(result, str)
    assert len(result) > 0

    # Verify agents
    assert len(rag_agent.agents) == 2
    assert rag_agent.execution_mode == "sequential"
```

## Data Flow

1. **Input**: User query as string
2. **BaseRAGAgent**:
   - Retrieves relevant documents
   - Outputs: `{retrieved_documents: [...], context: "...", query: "..."}`
3. **AnswerAgent**:
   - Receives retrieved documents and query
   - Generates structured answer
   - Outputs: Answer string

## State Management

The agents share state through the multi-agent framework:

- **Query**: Passed from input through both agents
- **Retrieved Documents**: BaseRAGAgent → AnswerAgent
- **Context**: Additional retrieval metadata
- **Final Answer**: AnswerAgent output

## Best Practices

1. **Real Components**: Always test with real LLMs and vector stores
2. **Custom Engines**: Override engines for specific use cases
3. **Prompt Engineering**: Customize AnswerAgent prompts for domain-specific tasks
4. **State Validation**: Ensure proper data flow between agents

## See Also

- [BaseRAGAgent Documentation](../base/README.md)
- [AnswerAgent Documentation](answer_agent.py)
- [CollectiveRAGAgent](../collective_rag_agent_v4.py) - Multiple RAG sources
- [Multi-Agent Documentation](../../multi/README.md)
