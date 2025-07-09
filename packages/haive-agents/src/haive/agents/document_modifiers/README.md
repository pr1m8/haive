# Document Modifiers

Advanced document transformation and information extraction agents for the Haive framework.

## Overview

The Document Modifiers module provides a comprehensive suite of agents designed to transform, analyze, and extract structured information from documents. These agents handle various document processing tasks including summarization, knowledge graph construction, taxonomy generation, and complex data extraction with validation.

This module is ideal for:

- Building knowledge graphs from unstructured text
- Generating hierarchical taxonomies from conversation histories
- Extracting structured data with schema validation
- Summarizing large documents using map-reduce approaches
- Creating semantic representations of document content

## Architecture

```
document_modifiers/
├── base/                    # Shared state and models for document processing
├── tnt/                     # Taxonomy and Topic (TNT) generation
├── complex_extraction/      # Advanced structured data extraction with validation
├── kg/                      # Knowledge Graph construction agents
│   ├── kg_base/            # Base models for knowledge graphs
│   ├── kg_iterative_refinement/  # Iterative graph building
│   └── kg_map_merge/       # Parallel graph construction with merging
└── summarizer/             # Document summarization agents
    ├── iterative_refinement/  # Iterative summary refinement
    └── map_branch/         # Map-reduce summarization
```

## Key Components

### Base Module

The `base` submodule provides shared functionality for all document modifiers:

- **DocumentModifierState**: Common state schema for document processing
- **Document handling**: Utilities for managing document collections
- **Validation**: Document validation and preprocessing

### TNT (Taxonomy and Topic Generation)

The `tnt` submodule generates hierarchical taxonomies from conversation histories:

- **TaxonomyAgent**: Creates taxonomies through iterative refinement
- **Document clustering**: Groups similar documents for taxonomy generation
- **Multi-stage processing**: Summarization → Clustering → Taxonomy → Review

### Complex Extraction

The `complex_extraction` submodule provides robust structured data extraction:

- **Schema-based extraction**: Extract data according to Pydantic models
- **Validation with retries**: Automatic retry with error correction
- **JSONPatch support**: Fine-grained error correction for complex schemas

### Knowledge Graph (KG) Agents

The `kg` submodule offers multiple strategies for building knowledge graphs:

#### KG Iterative Refinement

- **IterativeGraphTransformer**: Builds graphs incrementally from document sequences
- **Progressive enhancement**: Each document refines the existing graph
- **Context preservation**: Maintains relationships across documents

#### KG Map-Merge

- **ParallelKGTransformer**: Parallel graph extraction with merging
- **High throughput**: Processes multiple documents simultaneously
- **Conflict resolution**: Intelligent merging of parallel results

### Summarizer Agents

The `summarizer` submodule provides document summarization capabilities:

#### Map-Branch Summarizer

- **SummarizerAgent**: Map-reduce approach for large documents
- **Token-aware**: Handles token limits intelligently
- **Hierarchical summarization**: Multi-level summary generation

#### Iterative Refinement Summarizer

- **Iterative improvement**: Refines summaries through multiple passes
- **Quality focus**: Emphasizes summary coherence and completeness

## Installation

This module is part of the `haive-agents` package. Install it using:

```bash
pip install haive-agents

# Or install from source with development dependencies
pip install -e ".[agents,dev]"
```

## Quick Start

### Knowledge Graph Generation

```python
from haive.agents.document_modifiers.kg.kg_map_merge import ParallelKGTransformer
from haive.agents.document_modifiers.kg.kg_map_merge.config import ParallelKGTransformerConfig

# Configure the agent
config = ParallelKGTransformerConfig(
    name="research_graph_builder"
)

# Create agent instance
agent = ParallelKGTransformer(config)

# Process documents
documents = [
    "Marie Curie was a physicist who won two Nobel Prizes.",
    "She discovered polonium and radium with her husband Pierre.",
    "Their daughter Irène also won a Nobel Prize in Chemistry."
]

result = agent.run({"contents": documents})
knowledge_graph = result["final_graph"]

# Access extracted entities and relationships
for entity in knowledge_graph.entities:
    print(f"Entity: {entity.name} ({entity.type})")

for relationship in knowledge_graph.relationships:
    print(f"Relationship: {relationship.source} -> {relationship.target} ({relationship.type})")
```

### Document Summarization

```python
from haive.agents.document_modifiers.summarizer.map_branch import SummarizerAgent
from haive.agents.document_modifiers.summarizer.map_branch.config import SummarizerAgentConfig

# Configure with token limits
config = SummarizerAgentConfig(
    token_max=1000,  # Maximum tokens per summary chunk
    name="document_summarizer"
)

agent = SummarizerAgent(config)

# Summarize large documents
long_documents = ["Very long document text...", "Another long document..."]
result = agent.run({"contents": long_documents})
summary = result["final_summary"]
```

### Complex Data Extraction

```python
from haive.agents.document_modifiers.complex_extraction import ComplexExtractionAgent
from haive.agents.document_modifiers.complex_extraction.config import ComplexExtractionAgentConfig
from pydantic import BaseModel

# Define extraction schema
class CompanyInfo(BaseModel):
    name: str
    founded: int
    headquarters: str
    employees: int
    products: list[str]

# Configure with validation
config = ComplexExtractionAgentConfig(
    extraction_model=CompanyInfo,
    max_retries=3,
    use_jsonpatch=True  # Enable error correction
)

agent = ComplexExtractionAgent(config)

# Extract structured data
text = """
Apple Inc. was founded in 1976 and is headquartered in Cupertino, California.
The company employs over 150,000 people and is known for products like the
iPhone, iPad, Mac computers, and Apple Watch.
"""

result = agent.run(text)
company_data = result["extracted_data"]
# CompanyInfo(name='Apple Inc.', founded=1976, headquarters='Cupertino, California',
#            employees=150000, products=['iPhone', 'iPad', 'Mac computers', 'Apple Watch'])
```

### Taxonomy Generation

```python
from haive.agents.document_modifiers.tnt import TaxonomyAgent
from haive.agents.document_modifiers.tnt.config import TaxonomyAgentConfig

# Configure taxonomy generation
config = TaxonomyAgentConfig(
    name="conversation_taxonomy",
    visualize=True  # Generate visual representation
)

agent = TaxonomyAgent(config)

# Generate taxonomy from conversations
conversations = [
    "User asked about Python programming and loops",
    "Discussion about machine learning algorithms",
    "Question regarding database design patterns",
    # ... more conversation documents
]

result = agent.run({"documents": conversations})
taxonomy = result["final_taxonomy"]
```

## Advanced Usage

### Custom Document State

```python
from haive.agents.document_modifiers.base.state import DocumentModifierState
from langchain_core.documents import Document
from pydantic import Field

class CustomDocumentState(DocumentModifierState):
    """Extended document state with metadata."""

    source_urls: list[str] = Field(default_factory=list)
    processing_metadata: dict = Field(default_factory=dict)
    quality_scores: list[float] = Field(default_factory=list)

    def add_quality_score(self, score: float) -> None:
        """Add a quality score for processed documents."""
        self.quality_scores.append(score)
```

### Combining Multiple Agents

```python
# Pipeline: Extract → Build Graph → Summarize
from haive.agents.document_modifiers.complex_extraction import ComplexExtractionAgent
from haive.agents.document_modifiers.kg.kg_iterative_refinement import IterativeGraphTransformer
from haive.agents.document_modifiers.summarizer.map_branch import SummarizerAgent

# Step 1: Extract structured data
extractor = ComplexExtractionAgent(extraction_config)
extracted_data = extractor.run(raw_text)

# Step 2: Build knowledge graph
graph_builder = IterativeGraphTransformer(graph_config)
knowledge_graph = graph_builder.run({"contents": extracted_data["documents"]})

# Step 3: Generate summary
summarizer = SummarizerAgent(summary_config)
summary = summarizer.run({"contents": [str(knowledge_graph["graph_doc"])]})
```

## Configuration Options

### Common Configuration Parameters

All document modifier agents support these base configuration options:

```python
{
    "name": "agent_name",           # Agent identifier
    "state_schema": StateClass,     # State schema to use
    "engines": {                    # LLM engine configurations
        "default": AugLLMConfig(...)
    },
    "visualize": False,             # Enable visualization (where applicable)
    "checkpoint_mode": "async"      # Checkpointing strategy
}
```

### Agent-Specific Configurations

Each agent type has specific configuration options:

- **ComplexExtractionAgent**: `extraction_model`, `max_retries`, `use_jsonpatch`
- **KG Agents**: `graph_schema`, `merge_strategy`, `parallel_workers`
- **SummarizerAgent**: `token_max`, `chunk_size`, `summary_style`
- **TaxonomyAgent**: `max_depth`, `min_cluster_size`, `review_iterations`

## Best Practices

1. **Document Preprocessing**
   - Clean and normalize text before processing
   - Remove irrelevant metadata that might confuse extraction
   - Consider document chunking for very large texts

2. **Schema Design for Extraction**
   - Start with simple schemas and iterate
   - Use Optional fields for uncertain data
   - Provide clear field descriptions for better extraction

3. **Knowledge Graph Construction**
   - Use iterative refinement for related document sets
   - Use parallel processing for independent documents
   - Define clear entity and relationship types

4. **Performance Optimization**
   - Batch similar documents together
   - Use appropriate token limits for your use case
   - Consider caching for repeated processing

## Troubleshooting

### Common Issues

1. **Token Limit Exceeded**

   ```python
   # Solution: Adjust token_max in configuration
   config = SummarizerAgentConfig(token_max=500)
   ```

2. **Extraction Validation Failures**

   ```python
   # Solution: Enable JSONPatch for error correction
   config = ComplexExtractionAgentConfig(use_jsonpatch=True)
   ```

3. **Graph Merge Conflicts**
   ```python
   # Solution: Implement custom merge strategy
   config.merge_strategy = "conservative"  # or "aggressive"
   ```

## API Reference

For detailed API documentation, see the [API Reference](../../../docs/source/api/document_modifiers/index.rst).

## See Also

- [`haive.agents`](../): Parent module for all Haive agents
- [`document_modifiers.tnt`](./tnt/): Taxonomy and topic generation
- [`document_modifiers.base`](./base/): Base classes and utilities
- [`document_modifiers.summarizer`](./summarizer/): Document summarization
- [`document_modifiers.complex_extraction`](./complex_extraction/): Structured extraction
- [`document_modifiers.kg`](./kg/): Knowledge graph construction
