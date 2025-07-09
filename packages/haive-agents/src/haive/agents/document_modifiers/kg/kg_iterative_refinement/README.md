# KG Iterative Refinement

Iterative knowledge graph construction that builds and refines graphs incrementally from document sequences.

## Overview

The KG Iterative Refinement module provides an agent that constructs knowledge graphs by processing documents one at a time, continuously refining and expanding the graph with each new document. This approach is particularly effective for building comprehensive knowledge graphs from related documents where later documents may provide additional context or details about entities discovered earlier.

Key features:

- **Incremental graph building**: Process documents sequentially
- **Context preservation**: Maintain relationships across documents
- **Progressive refinement**: Enhance existing entities with new information
- **Conflict resolution**: Handle contradictions and updates intelligently
- **Memory efficient**: Process large document sets without loading all at once

This module is ideal for:

- Building knowledge graphs from document series (e.g., news articles over time)
- Processing related documents that reference common entities
- Creating graphs where context builds progressively
- Handling document streams or feeds
- Maintaining coherent graphs from multiple sources

## Architecture

The iterative refinement process follows these steps:

1. **Initial Graph**: Start with empty graph or seed knowledge
2. **Document Processing**: Process each document individually
3. **Entity Recognition**: Identify entities in context of existing graph
4. **Relationship Extraction**: Find relationships considering known entities
5. **Graph Integration**: Merge new information with existing graph
6. **Conflict Resolution**: Handle updates and contradictions
7. **Graph Refinement**: Enhance and consolidate the graph

## Key Components

### IterativeGraphTransformer

The main agent class that manages the iterative graph construction process.

```python
class IterativeGraphTransformer(Agent):
    """Builds knowledge graphs iteratively from document sequences."""
```

### State Management

- **IterativeGraphTransformerState**: Tracks graph evolution and document processing
- **GraphDocument**: Current state of the knowledge graph
- **Processing history**: Track which documents have been processed

### Configuration

- **IterativeGraphTransformerConfig**: Agent configuration
- **Refinement strategies**: How to handle conflicts and updates
- **Graph constraints**: Rules for graph construction

## Installation

This module is part of the `haive-agents` package. Install it using:

```bash
pip install haive-agents
```

## Usage Examples

### Basic Iterative Graph Building

```python
from haive.agents.document_modifiers.kg.kg_iterative_refinement import IterativeGraphTransformer
from haive.agents.document_modifiers.kg.kg_iterative_refinement.config import IterativeGraphTransformerConfig
from langchain_core.documents import Document

# Configure the agent
config = IterativeGraphTransformerConfig(
    name="iterative_kg_builder",
    allowed_nodes=["Person", "Organization", "Event", "Location"],
    allowed_relationships=[
        ("Person", "WORKS_FOR", "Organization"),
        ("Person", "PARTICIPATED_IN", "Event"),
        ("Event", "LOCATED_IN", "Location"),
        ("Organization", "HEADQUARTERED_IN", "Location")
    ]
)

# Create agent
agent = IterativeGraphTransformer(config)

# Process documents iteratively
documents = [
    "Marie Curie was a Polish physicist who conducted pioneering research.",
    "Curie became the first woman to win a Nobel Prize in 1903.",
    "She shared the 1903 Nobel Prize in Physics with her husband Pierre Curie.",
    "Marie Curie won a second Nobel Prize in Chemistry in 1911.",
    "She founded the Radium Institute in Paris for cancer research.",
    "The Radium Institute later became the Curie Institute."
]

# Build graph iteratively
result = agent.run({"contents": documents})
final_graph = result["graph_doc"]

# The graph now contains:
# - Marie Curie entity enhanced with each document
# - Nobel Prize events with dates and fields
# - Relationships showing her achievements
# - Institute evolution over time
```

### Processing News Articles Over Time

```python
from datetime import datetime

# Configure for news processing
config = IterativeGraphTransformerConfig(
    name="news_kg_builder",
    allowed_nodes=["Person", "Company", "Product", "Event", "Location"],
    allowed_relationships=[
        ("Person", "CEO_OF", "Company"),
        ("Person", "FOUNDED", "Company"),
        ("Company", "LAUNCHED", "Product"),
        ("Company", "ACQUIRED", "Company"),
        ("Event", "OCCURRED_IN", "Location")
    ],
    merge_strategy="temporal",  # Consider time in updates
    conflict_resolution="latest"  # Latest info takes precedence
)

agent = IterativeGraphTransformer(config)

# Process news articles chronologically
news_articles = [
    {
        "date": "2023-01-15",
        "content": "Tech startup Innovate AI was founded by Jane Smith in Silicon Valley."
    },
    {
        "date": "2023-06-20",
        "content": "Innovate AI launches revolutionary product AIAssist with Jane Smith as CEO."
    },
    {
        "date": "2023-11-10",
        "content": "Major Corp acquires Innovate AI for $500M. Jane Smith to lead AI division."
    }
]

# Sort by date and process
sorted_articles = sorted(news_articles, key=lambda x: x["date"])
documents = [article["content"] for article in sorted_articles]

result = agent.run({"contents": documents})

# Graph evolution:
# 1. Initial: Jane Smith -> FOUNDED -> Innovate AI
# 2. Update: Jane Smith -> CEO_OF -> Innovate AI, Innovate AI -> LAUNCHED -> AIAssist
# 3. Final: Major Corp -> ACQUIRED -> Innovate AI, Jane Smith -> LEADS -> AI Division
```

### Research Paper Analysis

```python
# Configure for academic knowledge graph
config = IterativeGraphTransformerConfig(
    name="research_kg_builder",
    allowed_nodes=["Researcher", "Paper", "Institution", "Concept", "Method"],
    allowed_relationships=[
        ("Researcher", "AUTHORED", "Paper"),
        ("Researcher", "AFFILIATED_WITH", "Institution"),
        ("Paper", "INTRODUCES", "Concept"),
        ("Paper", "USES", "Method"),
        ("Paper", "CITES", "Paper"),
        ("Concept", "RELATED_TO", "Concept")
    ],
    enable_coreference=True,  # Resolve "the authors", "they", etc.
    extract_properties=True   # Extract publication years, etc.
)

agent = IterativeGraphTransformer(config)

# Process paper abstracts
abstracts = [
    "Smith et al. (2023) from MIT introduce the TransformerX architecture for NLP.",
    "Building on TransformerX, the authors propose a novel attention mechanism.",
    "Johnson (2023) from Stanford applies TransformerX to computer vision tasks.",
    "The Stanford team's results show 95% accuracy using the modified architecture."
]

result = agent.run({"contents": abstracts})

# Graph includes:
# - Researcher entities with affiliations
# - Paper relationships and citations
# - Concept evolution (TransformerX -> modified architecture)
# - Cross-domain applications
```

### Handling Conflicting Information

```python
# Configure with conflict resolution
config = IterativeGraphTransformerConfig(
    name="conflict_aware_builder",
    allowed_nodes=["Person", "Company", "Position"],
    allowed_relationships=[
        ("Person", "HOLDS_POSITION", "Position"),
        ("Position", "AT_COMPANY", "Company")
    ],
    conflict_resolution="confidence_weighted",  # Use confidence scores
    track_provenance=True,  # Remember source of each fact
    versioning=True  # Keep history of changes
)

agent = IterativeGraphTransformer(config)

# Documents with potential conflicts
documents = [
    "As of Jan 2023, John Doe is the CTO of TechCorp.",
    "TechCorp announced John Doe as their new CEO in March 2023.",
    "Correction: John Doe serves as CTO, not CEO, of TechCorp as of April 2023."
]

result = agent.run({"contents": documents})

# The agent:
# 1. Creates initial relationship: John Doe -> CTO -> TechCorp
# 2. Updates with conflict: John Doe -> CEO -> TechCorp (marks conflict)
# 3. Resolves with correction: John Doe -> CTO -> TechCorp (final state)
# 4. Maintains history of all states with timestamps
```

### Streaming Document Processing

```python
import asyncio
from typing import AsyncIterator

async def process_document_stream(
    agent: IterativeGraphTransformer,
    document_stream: AsyncIterator[str]
) -> None:
    """Process documents as they arrive."""

    current_graph = None

    async for document in document_stream:
        # Process single document
        result = await agent.arun({
            "contents": [document],
            "existing_graph": current_graph
        })

        current_graph = result["graph_doc"]

        # Optionally save intermediate state
        if len(current_graph.nodes) % 100 == 0:
            await save_graph_checkpoint(current_graph)

        # Yield progress
        yield {
            "processed": document[:50] + "...",
            "total_entities": len(current_graph.nodes),
            "total_relationships": len(current_graph.relationships)
        }

# Usage with async stream
async def main():
    config = IterativeGraphTransformerConfig(streaming_mode=True)
    agent = IterativeGraphTransformer(config)

    document_stream = fetch_documents_async()  # Your async source

    async for progress in process_document_stream(agent, document_stream):
        print(f"Processed: {progress['processed']}")
        print(f"Graph size: {progress['total_entities']} entities")
```

## Configuration Options

### IterativeGraphTransformerConfig

- `allowed_nodes`: List of permitted entity types
- `allowed_relationships`: Valid relationship types
- `merge_strategy`: How to merge new information ("temporal", "confidence", "source")
- `conflict_resolution`: How to handle conflicts ("latest", "confidence_weighted", "manual")
- `enable_coreference`: Resolve pronouns and references
- `extract_properties`: Extract entity/relationship properties
- `track_provenance`: Remember source documents
- `versioning`: Keep history of changes
- `streaming_mode`: Enable for continuous processing
- `checkpoint_interval`: Save progress periodically

### Merge Strategies

1. **Temporal**: Later documents override earlier ones
2. **Confidence**: Higher confidence information takes precedence
3. **Source**: Prioritize based on source reliability
4. **Additive**: Only add new information, never remove

### Conflict Resolution

1. **Latest**: Most recent information wins
2. **Confidence Weighted**: Use confidence scores
3. **Manual**: Flag conflicts for human review
4. **Consensus**: Require multiple sources

## Best Practices

1. **Document Ordering**
   - Process documents in logical order (chronological, topical)
   - Consider dependencies between documents
   - Group related documents together

2. **Schema Design**
   - Start with core entities and relationships
   - Allow for entity evolution over iterations
   - Consider temporal aspects in relationships

3. **Performance Optimization**
   - Use checkpointing for large document sets
   - Process in batches when possible
   - Monitor graph size and complexity

4. **Quality Assurance**
   - Validate graph consistency periodically
   - Check for orphaned nodes or relationships
   - Review conflict resolutions

## Advanced Features

### Custom Refinement Logic

```python
from haive.agents.document_modifiers.kg.kg_iterative_refinement.utils import RefinementStrategy

class CustomRefinementStrategy(RefinementStrategy):
    """Custom logic for graph refinement."""

    def should_merge_entities(self, entity1, entity2, context):
        """Determine if two entities should be merged."""
        # Custom logic based on similarity, context, etc.
        similarity = calculate_similarity(entity1, entity2)
        return similarity > 0.85

    def resolve_conflict(self, old_value, new_value, context):
        """Resolve conflicting information."""
        # Custom conflict resolution
        if context.get("source_reliability", 0) > 0.9:
            return new_value
        return old_value

config.refinement_strategy = CustomRefinementStrategy()
```

### Graph Metrics and Analysis

```python
# Enable metrics collection
config = IterativeGraphTransformerConfig(
    collect_metrics=True,
    metrics_interval=10  # Every 10 documents
)

agent = IterativeGraphTransformer(config)
result = agent.run({"contents": documents})

# Access metrics
metrics = result["metrics"]
print(f"Entity growth rate: {metrics['entity_growth_rate']}")
print(f"Relationship density: {metrics['relationship_density']}")
print(f"Average refinements per entity: {metrics['avg_refinements']}")
print(f"Conflict rate: {metrics['conflict_rate']}")
```

## Troubleshooting

### Common Issues

1. **Graph Explosion**

   ```python
   # Solution: Add constraints
   config.max_entities_per_document = 20
   config.relationship_threshold = 0.7  # Confidence threshold
   ```

2. **Lost Context Between Documents**

   ```python
   # Solution: Enable coreference resolution
   config.enable_coreference = True
   config.context_window = 3  # Look back 3 documents
   ```

3. **Inconsistent Entity Names**
   ```python
   # Solution: Add normalization
   config.entity_normalization = True
   config.normalization_rules = {
       "company_names": "official",
       "person_names": "full_name"
   }
   ```

## API Reference

For detailed API documentation, see the [API Reference](../../../../../docs/source/api/document_modifiers/kg/kg_iterative_refinement/index.rst).

## See Also

- [`kg_base`](../kg_base/): Base knowledge graph components
- [`kg_map_merge`](../kg_map_merge/): Parallel graph construction
- [`haive.agents.document_modifiers`](../../): Parent module
- [Neo4j Best Practices](https://neo4j.com/docs/): Graph database patterns
