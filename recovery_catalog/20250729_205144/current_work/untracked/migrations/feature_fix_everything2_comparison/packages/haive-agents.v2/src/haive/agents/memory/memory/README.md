# Haive Memory Agents System

A comprehensive multi-agent memory system for intelligent storage, retrieval, and analysis of information with knowledge graph capabilities.

## Overview

The Haive Memory Agents System provides a sophisticated framework for managing different types of memory through specialized agents. Each agent is designed to handle specific aspects of memory management, from classification and storage to advanced retrieval and knowledge graph generation.

## Architecture

### Core Components

```
Memory System Architecture
├── Core Components
│   ├── MemoryStoreManager      # Centralized memory storage
│   ├── MemoryClassifier        # Memory type classification
│   └── MemoryTypes            # Type definitions and enums
├── Specialized Agents
│   ├── KGGeneratorAgent       # Knowledge graph extraction
│   ├── GraphRAGRetriever      # Graph-enhanced retrieval
│   ├── AgenticRAGCoordinator  # Multi-strategy coordination
│   └── MultiAgentCoordinator  # System orchestration
└── Unified Interface
    └── UnifiedMemorySystem    # Single API for all features
```

### Memory Types

The system supports multiple memory types:

- **Semantic**: Factual information and concepts
- **Episodic**: Personal experiences and events
- **Procedural**: How-to knowledge and processes
- **Temporal**: Time-based information
- **Contextual**: Situational and environmental data
- **Preference**: User preferences and choices
- **Feedback**: Error reports and corrections
- **System**: Internal system information
- **Skill**: Learned abilities and competencies
- **Social**: Interpersonal relationships and interactions
- **Spatial**: Location and spatial information

## Quick Start

### Basic Usage

```python
from haive.agents.memory.unified_memory_api import create_memory_system

# Create a complete memory system
memory_system = await create_memory_system(
    store_type="memory",
    collection_name="my_memories",
    enable_graph_rag=True,
    enable_multi_agent_coordination=True
)

# Store a memory
result = await memory_system.store_memory(
    content="I learned Python programming at Stanford University",
    metadata={"source": "learning", "importance": 0.8}
)

# Retrieve memories with intelligent routing
result = await memory_system.retrieve_memories(
    query="What programming languages do I know?",
    use_graph_rag=True,
    use_multi_agent=True
)

# Generate knowledge graph
result = await memory_system.generate_knowledge_graph()
```

### Advanced Usage

```python
from haive.agents.memory.multi_agent_coordinator import MultiAgentMemoryCoordinator
from haive.agents.memory.core.stores import MemoryStoreManager
from haive.agents.memory.core.classifier import MemoryClassifier

# Create individual components
store_manager = MemoryStoreManager(config)
classifier = MemoryClassifier(config)

# Create multi-agent coordinator
coordinator = MultiAgentMemoryCoordinator(
    MultiAgentCoordinatorConfig(
        memory_store_manager=store_manager,
        memory_classifier=classifier,
        enable_graph_rag=True,
        enable_multi_agent_coordination=True
    )
)

# Execute complex memory tasks
task = MemoryTask(
    id="analyze_learning",
    type="analyze_and_graph",
    query="Analyze my learning patterns and build a knowledge graph",
    priority=1
)

result = await coordinator.execute_task(task)
```

## Individual Agent Documentation

### 1. KGGeneratorAgent

**Purpose**: Extracts entities and relationships from memories to build knowledge graphs.

**Key Features**:

- Entity extraction with confidence scoring
- Relationship discovery between entities
- Incremental graph building
- Entity neighborhood exploration

**Example**:

```python
from haive.agents.memory.kg_generator_agent import KGGeneratorAgent

kg_agent = KGGeneratorAgent(config)

# Extract knowledge graph
graph = await kg_agent.extract_knowledge_graph_from_memories()
print(f"Found {len(graph.nodes)} entities and {len(graph.relationships)} relationships")

# Get entity context
context = await kg_agent.get_entity_context("Python")
```

### 2. GraphRAGRetriever

**Purpose**: Enhanced retrieval using graph traversal combined with vector similarity.

**Key Features**:

- Multi-hop graph traversal
- Hybrid vector + graph search
- Path-based result ranking
- Graph-aware relevance scoring

**Example**:

```python
from haive.agents.memory.graph_rag_retriever import GraphRAGRetriever

retriever = GraphRAGRetriever(config)

# Retrieve with graph traversal
result = await retriever.retrieve_memories(
    query="machine learning algorithms",
    enable_graph_traversal=True,
    max_graph_depth=3
)

print(f"Found {len(result.memories)} memories via {result.graph_nodes_explored} graph nodes")
```

### 3. AgenticRAGCoordinator

**Purpose**: Intelligent coordination of multiple retrieval strategies.

**Key Features**:

- Strategy selection based on query analysis
- Multi-strategy result fusion
- Confidence-based ranking
- Adaptive strategy weighting

**Example**:

```python
from haive.agents.memory.agentic_rag_coordinator import AgenticRAGCoordinator

coordinator = AgenticRAGCoordinator(config)

# Intelligent retrieval with strategy selection
result = await coordinator.retrieve_memories(
    query="How do I deploy web applications?",
    enable_strategy_fusion=True
)

print(f"Used strategies: {result.selected_strategies}")
print(f"Confidence: {result.confidence_score}")
```

### 4. MultiAgentCoordinator

**Purpose**: Orchestrates multiple memory agents for complex tasks.

**Key Features**:

- Intelligent task routing
- Agent capability matching
- Parallel and sequential execution
- Performance monitoring

**Example**:

```python
from haive.agents.memory.multi_agent_coordinator import MultiAgentMemoryCoordinator

coordinator = MultiAgentMemoryCoordinator(config)

# Store memory through coordination
await coordinator.store_memory("New learning: Docker containerization")

# Retrieve with agent coordination
memories = await coordinator.retrieve_memories("Docker containers")

# System health check
status = coordinator.get_system_status()
diagnostic = await coordinator.run_diagnostic()
```

### 5. UnifiedMemorySystem

**Purpose**: Single API interface for all memory system functionality.

**Key Features**:

- Unified API for all operations
- Automatic agent selection
- Performance optimization
- System health monitoring

**Example**:

```python
from haive.agents.memory.unified_memory_api import UnifiedMemorySystem

system = UnifiedMemorySystem(config)

# All operations through single interface
await system.store_memory("Content")
memories = await system.retrieve_memories("Query")
analysis = await system.analyze_memory("Content")
graph = await system.generate_knowledge_graph()
stats = await system.get_memory_statistics()
```

## Configuration

### Basic Configuration

```python
from haive.agents.memory.unified_memory_api import MemorySystemConfig
from haive.core.engine.aug_llm import AugLLMConfig

config = MemorySystemConfig(
    store_type="memory",  # or "postgres", "redis", etc.
    collection_name="my_memories",
    default_namespace=("user", "personal"),

    # Feature flags
    enable_auto_classification=True,
    enable_enhanced_retrieval=True,
    enable_graph_rag=True,
    enable_multi_agent_coordination=True,

    # LLM configuration
    llm_config=AugLLMConfig(
        model="gpt-4",
        temperature=0.7
    )
)
```

### Advanced Configuration

```python
from haive.agents.memory.multi_agent_coordinator import MultiAgentCoordinatorConfig
from haive.agents.memory.kg_generator_agent import KGGeneratorAgentConfig
from haive.agents.memory.agentic_rag_coordinator import AgenticRAGCoordinatorConfig

# Fine-tune individual agents
kg_config = KGGeneratorAgentConfig(
    memory_store_manager=store_manager,
    memory_classifier=classifier,
    extract_batch_size=20,
    min_confidence_threshold=0.7,
    entity_types=["person", "organization", "concept", "technology"],
    relationship_types=["works_at", "knows", "uses", "creates"]
)

rag_config = AgenticRAGCoordinatorConfig(
    memory_store_manager=store_manager,
    memory_classifier=classifier,
    kg_generator=kg_generator,
    enable_strategy_fusion=True,
    confidence_threshold=0.6,
    max_strategies=3
)

coordinator_config = MultiAgentCoordinatorConfig(
    memory_store_manager=store_manager,
    memory_classifier=classifier,
    kg_generator_config=kg_config,
    agentic_rag_config=rag_config,
    max_concurrent_tasks=5,
    enable_agent_communication=True
)
```

## Performance Optimization

### Caching Strategies

```python
# Enable caching for better performance
config = MemorySystemConfig(
    enable_caching=True,
    cache_ttl_seconds=3600,  # 1 hour
    cache_size_mb=100
)
```

### Batch Processing

```python
# Process memories in batches
kg_agent = KGGeneratorAgent(config)
await kg_agent.extract_knowledge_graph_from_memories(
    batch_size=50,  # Process 50 memories at once
    parallel_processing=True
)
```

### Concurrent Operations

```python
# Execute multiple operations concurrently
coordinator = MultiAgentMemoryCoordinator(config)

# Concurrent task execution
tasks = [
    coordinator.store_memory("Memory 1"),
    coordinator.store_memory("Memory 2"),
    coordinator.analyze_memory("Content to analyze")
]

results = await asyncio.gather(*tasks)
```

## Error Handling

### Graceful Degradation

```python
try:
    # Attempt advanced retrieval
    result = await system.retrieve_memories(
        query="complex query",
        use_graph_rag=True,
        use_multi_agent=True
    )
except GraphRAGError:
    # Fall back to simple retrieval
    result = await system.retrieve_memories(
        query="complex query",
        use_graph_rag=False
    )
```

### Health Monitoring

```python
# System health check
diagnostic = await coordinator.run_diagnostic()

if diagnostic["system_status"] == "degraded":
    # Handle degraded performance
    logger.warning("Memory system performance degraded")

    # Check individual agent status
    for agent, status in diagnostic["agent_diagnostics"].items():
        if status["status"] == "error":
            logger.error(f"Agent {agent} error: {status['error']}")
```

## Testing

### Unit Tests

```python
import pytest
from haive.agents.memory.kg_generator_agent import KGGeneratorAgent

@pytest.mark.asyncio
async def test_kg_extraction():
    """Test knowledge graph extraction with real LLM."""
    agent = KGGeneratorAgent(test_config)

    # Test entity extraction
    entities = await agent.extract_entities_from_memories(limit=5)
    assert len(entities) > 0
    assert all(entity.confidence > 0.5 for entity in entities)

    # Test relationship extraction
    relationships = await agent.extract_relationships_from_memories(limit=5)
    assert len(relationships) > 0
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_full_memory_system():
    """Test complete memory system integration."""
    system = await create_memory_system("memory", "test_collection")

    # Store memory
    store_result = await system.store_memory("Test content")
    assert store_result.success

    # Retrieve memory
    retrieve_result = await system.retrieve_memories("Test")
    assert retrieve_result.success
    assert len(retrieve_result.result["memories"]) > 0
```

## Performance Benchmarks

### Typical Performance Metrics

- **Memory Storage**: 50-200ms per memory
- **Simple Retrieval**: 100-500ms
- **Graph RAG Retrieval**: 500-2000ms
- **Knowledge Graph Generation**: 2-10 seconds (batch)
- **Multi-Agent Coordination**: 200-1000ms overhead

### Optimization Tips

1. **Batch Operations**: Process multiple memories together
2. **Caching**: Enable caching for frequently accessed data
3. **Async Operations**: Use async/await for I/O operations
4. **Connection Pooling**: Use connection pools for database operations
5. **Selective Features**: Disable unused features to reduce overhead

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Memory Store Connection**: Check database/store connectivity
3. **LLM API Limits**: Monitor API usage and implement retry logic
4. **Performance Issues**: Enable profiling and optimize batch sizes
5. **Graph Extraction**: Ensure sufficient memory content for graph building

### Debug Mode

```python
# Enable debug mode for detailed logging
config = MemorySystemConfig(
    debug=True,
    log_level="DEBUG"
)

# Run with debug information
result = await system.retrieve_memories("query", debug=True)
```

## Contributing

### Development Setup

```bash
# Install development dependencies
poetry install --with dev

# Run tests
poetry run pytest packages/haive-agents/tests/memory/

# Run linting
poetry run ruff check packages/haive-agents/src/haive/agents/memory/
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Add comprehensive docstrings
- Include examples in docstrings
- Write tests for new features

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For issues and questions:

- GitHub Issues: [Project Issues](https://github.com/your-org/haive/issues)
- Documentation: [Full Documentation](https://haive.readthedocs.io/)
- Community: [Discord Server](https://discord.gg/haive)
