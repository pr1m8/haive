# RAG Agents Module

This module provides a comprehensive collection of Retrieval-Augmented Generation (RAG) agents for the Haive framework. It includes 12+ different RAG patterns and strategies, each optimized for specific use cases and query types.

## Overview

RAG (Retrieval-Augmented Generation) combines information retrieval with language generation to provide accurate, contextual responses based on specific document collections. This module implements various RAG patterns using the ChainAgent framework for consistency and composability.

## Available RAG Strategies

### Core RAG Patterns

- **Simple RAG** (`simple/`) - Basic retrieve-and-generate pattern
- **Multi-Query RAG** (`multi_query/`) - Multiple query perspectives for comprehensive retrieval
- **HyDE RAG** (`hyde/`) - Hypothetical document generation for enhanced retrieval
- **Fusion RAG** (`fusion/`) - Multi-query retrieval with reciprocal rank fusion

### Advanced RAG Patterns

- **FLARE RAG** (`flare/`) - Forward-looking active retrieval with iterative refinement
- **Speculative RAG** (`speculative/`) - Hypothesis generation and verification
- **Step-Back RAG** (`step_back/`) - Abstract reasoning before specific answers
- **Memory-Aware RAG** (`memory_aware/`) - Conversation context integration

### Agentic RAG Systems

- **Self-Route RAG** (`self_route/`) - Dynamic routing based on query analysis
- **Adaptive RAG** (`adaptive_tools/`) - Tool integration for enhanced capabilities
- **Agentic Router** (`agentic_router/`) - Intelligent strategy selection
- **Query Planning** (`query_planning/`) - Complex query decomposition

### Extended RAG Systems

- **Modular RAG** (`modular_chain.py`) - Configurable pipeline components
- **Branched RAG** (`branched_chain.py`) - Multi-path retrieval strategies
- **Enhanced Memory ReAct** (`enhanced_memory_react.py`) - Full ReAct pattern with memory

## Architecture

### Implementation Styles

Each RAG type can be created in three different styles:

1. **Traditional Style** - Direct agent instantiation with full control
2. **Chain Style** - Simplified sequential workflows using ChainAgent
3. **Multi Style** - Parallel and conditional execution using MultiAgent

### Key Components

- **Chain Collection** (`chain_collection.py`) - ChainAgent implementations
- **Unified Factory** (`unified_factory.py`) - Single interface for all RAG types
- **State Schemas** - Pydantic models for type safety and validation

## Quick Start

### Using the Collection

```python
from haive.agents.rag.chain_collection import RAGChainCollection
from langchain_core.documents import Document
from haive.core.models.llm.base import AzureLLMConfig

# Prepare documents
docs = [
    Document(page_content="Machine learning uses algorithms to learn from data..."),
    Document(page_content="Neural networks are inspired by biological neurons...")
]

# Configure LLM
llm_config = AzureLLMConfig(deployment_name="gpt-4")

# Create RAG agent
collection = RAGChainCollection()
agent = collection.create_fusion_rag(docs, llm_config)

# Use the agent
response = agent.invoke({"query": "What is machine learning?"})
```

### Using the Factory

```python
from haive.agents.rag.unified_factory import create_rag

# Create any RAG type with unified interface
simple_rag = create_rag("simple", docs, style="chain")
fusion_rag = create_rag("fusion", docs, style="chain")
hyde_rag = create_rag("hyde", docs, style="traditional")

# Create multi-agent version
multi_rag = create_rag("speculative", docs, style="multi")
```

### Building Pipelines

```python
from haive.agents.rag.unified_factory import create_rag_pipeline

# Combine multiple RAG strategies
pipeline = create_rag_pipeline(
    ["simple", "fusion", "flare"],
    docs,
    style="chain"
)
```

## Module Structure

```
rag/
├── README.md                    # This file
├── __init__.py                  # Package initialization
├── chain_collection.py          # ChainAgent RAG implementations
├── unified_factory.py           # Unified factory interface
├── modular_chain.py            # Modular RAG components
├── branched_chain.py           # Branched retrieval strategies
├── enhanced_memory_react.py    # Memory + ReAct integration
├── simple/                     # Simple RAG implementation
├── multi_query/               # Multi-query RAG
├── hyde/                      # HyDE RAG
├── fusion/                    # Fusion RAG
├── flare/                     # FLARE RAG
├── speculative/               # Speculative RAG
├── step_back/                 # Step-Back RAG
├── memory_aware/              # Memory-Aware RAG
├── self_route/                # Self-Route RAG
├── adaptive_tools/            # Adaptive RAG with tools
├── agentic_router/            # Agentic routing
├── query_planning/            # Query planning
├── self_reflective/           # Self-reflective RAG
└── corrective/                # Corrective RAG
```

## Best Practices

### Choosing the Right RAG Strategy

- **Simple RAG**: Use for straightforward Q&A over documents
- **Fusion RAG**: Use when you need high-quality, comprehensive answers
- **HyDE RAG**: Use for abstract or conceptual queries
- **FLARE RAG**: Use when iterative refinement is beneficial
- **Agentic Router**: Use when query types vary significantly

### Performance Considerations

- **Document Size**: Larger document sets benefit from advanced retrieval strategies
- **Query Complexity**: Complex queries benefit from planning and decomposition
- **Response Quality**: Fusion and speculative approaches provide higher quality
- **Speed Requirements**: Simple RAG is fastest, agentic approaches are more thorough

### Integration Tips

- Use the unified factory for consistent interfaces
- Combine RAG agents with other Haive agents using ChainAgent
- Leverage state schemas for type safety
- Monitor performance with built-in logging

## Testing

Run the comprehensive test suite:

```bash
poetry run python -m pytest tests/test_rag_comprehensive.py -v
```

Test specific RAG types:

```bash
poetry run python -c "
from haive.agents.rag.unified_factory import create_rag
agent = create_rag('fusion', docs)
print(f'Created {agent.name} with {len(agent.nodes)} nodes')
"
```

## Examples

See the `examples/` directory for detailed usage examples:

- Basic RAG usage patterns
- Advanced configuration options
- Integration with other agents
- Custom RAG pattern development

## Contributing

When adding new RAG patterns:

1. Create a new subdirectory with descriptive name
2. Implement both traditional and chain versions
3. Add comprehensive docstrings following Google style
4. Include proper type hints and Pydantic models
5. Add tests and usage examples
6. Update this README with the new pattern

## Related Modules

- `haive.agents.chain` - ChainAgent framework
- `haive.agents.multi` - Multi-agent orchestration
- `haive.core.engine` - Engine system for LLM integration
- `haive.tools` - Tool integration for adaptive RAG
