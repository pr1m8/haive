# TNT - Taxonomy and Topic Generation

Advanced taxonomy generation agent for creating hierarchical categorizations from document collections.

## Overview

The TNT (Taxonomy and Topic) module provides an intelligent agent that generates hierarchical taxonomies from collections of documents, particularly conversation histories. It uses an iterative refinement process to create meaningful categorizations that capture the essence of document collections.

The agent follows a sophisticated multi-stage process:

1. **Document Summarization**: Each document is summarized to extract key concepts
2. **Minibatch Creation**: Documents are grouped into processable batches
3. **Initial Taxonomy Generation**: Create initial category clusters
4. **Iterative Refinement**: Refine and improve the taxonomy through multiple passes
5. **Final Review**: Ensure taxonomy quality and coherence

This module is ideal for:

- Organizing large conversation histories into topics
- Creating hierarchical categorizations of documents
- Discovering themes in unstructured text collections
- Building navigable taxonomies for content management

## Key Components

### TaxonomyAgent

The main agent class that orchestrates the entire taxonomy generation process. It uses LLMs at each stage to ensure high-quality outputs.

### State Management

- **TaxonomyGenerationState**: Tracks documents, minibatches, and taxonomy evolution
- **Doc Model**: Represents documents with id, content, summary, and category

### Processing Stages

- **Summary Engine**: Generates concise summaries of documents
- **Taxonomy Generator**: Creates initial taxonomy from document summaries
- **Taxonomy Updater**: Refines taxonomy based on additional documents
- **Taxonomy Reviewer**: Ensures final taxonomy quality

### Utilities

- **format_taxonomy**: Formats taxonomy for display
- **format_docs**: Prepares documents for processing
- **should_review**: Determines if taxonomy needs review

## Installation

This module is part of the `haive-agents` package. Install it using:

```bash
pip install haive-agents
```

## Usage Examples

### Basic Taxonomy Generation

```python
from haive.agents.document_modifiers.tnt import TaxonomyAgent
from haive.agents.document_modifiers.tnt.config import TaxonomyAgentConfig

# Configure the agent
config = TaxonomyAgentConfig(
    name="conversation_taxonomy",
    visualize=True  # Enable graph visualization
)

# Create agent instance
agent = TaxonomyAgent(config)

# Prepare conversation documents
conversations = [
    "User asked about Python list comprehensions and their performance",
    "Discussion about database indexing strategies in PostgreSQL",
    "Questions regarding React hooks and state management",
    "Conversation about machine learning model deployment",
    "User needs help with Docker containerization",
    "Discussion about microservices architecture patterns"
]

# Generate taxonomy
result = agent.run({"documents": conversations})
taxonomy = result["final_taxonomy"]

# Access the generated categories
for cluster in taxonomy:
    print(f"Category: {cluster['name']}")
    print(f"Description: {cluster['description']}")
    print()
```

### Advanced Configuration

```python
from haive.agents.document_modifiers.tnt import TaxonomyAgent
from haive.agents.document_modifiers.tnt.config import TaxonomyAgentConfig
from haive.agents.document_modifiers.tnt.engines import (
    summary_aug_llm_config,
    taxonomy_generation_aug_llm_config
)

# Custom engine configurations
custom_engines = {
    "summary_engine": summary_aug_llm_config(temperature=0.3),
    "taxonomy_engine": taxonomy_generation_aug_llm_config(max_tokens=2000),
}

config = TaxonomyAgentConfig(
    name="detailed_taxonomy",
    engines=custom_engines,
    max_iterations=5,  # More refinement iterations
    minibatch_size=10  # Larger batches
)

agent = TaxonomyAgent(config)
```

### Processing Large Document Sets

```python
from haive.agents.document_modifiers.tnt import TaxonomyAgent
from haive.agents.document_modifiers.tnt.models import Doc

# Prepare documents with metadata
documents = []
for i, content in enumerate(large_document_collection):
    doc = Doc(
        id=f"doc_{i}",
        content=content,
        # Additional metadata can be added
    )
    documents.append(doc)

# Process in batches
config = TaxonomyAgentConfig(
    name="large_corpus_taxonomy",
    minibatch_size=20,  # Process 20 docs at a time
    checkpoint_mode="async"  # Enable checkpointing
)

agent = TaxonomyAgent(config)
result = agent.run({"documents": documents})

# Save taxonomy for later use
import json
with open("taxonomy.json", "w") as f:
    json.dump(result["final_taxonomy"], f, indent=2)
```

### Visualizing Taxonomy Evolution

```python
# Enable visualization to see how taxonomy evolves
config = TaxonomyAgentConfig(
    name="visual_taxonomy",
    visualize=True,
    checkpoint_dir="./taxonomy_checkpoints"
)

agent = TaxonomyAgent(config)
result = agent.run({"documents": documents})

# Access iteration history
for i, taxonomy_version in enumerate(result["clusters"]):
    print(f"Iteration {i}: {len(taxonomy_version)} categories")
```

## How It Works

### 1. Document Summarization

Each document is processed to extract key themes:

```python
"User asked about Python decorators and their use cases"
→ Summary: "Python decorator patterns and applications"
→ Explanation: "Discussion of function modification techniques"
```

### 2. Minibatch Processing

Documents are grouped for efficient processing:

```python
minibatches = [
    [0, 1, 2],  # Programming topics
    [3, 4],     # DevOps topics
    [5]         # Architecture
]
```

### 3. Taxonomy Generation

Initial clusters are created from document summaries:

```python
clusters = [
    {
        "id": 1,
        "name": "Programming Languages",
        "description": "Discussions about coding and language features"
    },
    {
        "id": 2,
        "name": "Infrastructure",
        "description": "DevOps and deployment topics"
    }
]
```

### 4. Iterative Refinement

The taxonomy is refined through multiple passes, merging similar categories and creating hierarchies.

### 5. Final Review

The agent reviews the taxonomy for quality, consistency, and completeness.

## Configuration Options

### TaxonomyAgentConfig Parameters

- `name`: Agent identifier
- `visualize`: Enable/disable graph visualization
- `max_iterations`: Maximum refinement iterations (default: 3)
- `minibatch_size`: Documents per batch (default: 5)
- `review_threshold`: When to trigger review (default: 0.8)
- `engines`: Custom LLM configurations for each stage

### Engine Configuration

Different engines can be configured for each stage:

```python
engines = {
    "summary_engine": AugLLMConfig(...),
    "taxonomy_generation_engine": AugLLMConfig(...),
    "taxonomy_update_engine": AugLLMConfig(...),
    "taxonomy_review_engine": AugLLMConfig(...)
}
```

## Best Practices

1. **Document Preparation**
   - Ensure documents have meaningful content
   - Remove boilerplate or repetitive text
   - Consider document length (very short documents may not summarize well)

2. **Batch Size Selection**
   - Smaller batches (3-5) for diverse topics
   - Larger batches (10-20) for similar content
   - Balance between processing time and quality

3. **Iteration Count**
   - More iterations for complex document sets
   - Fewer iterations for well-structured content
   - Monitor convergence of taxonomy

4. **Review Process**
   - Always review final taxonomy
   - Check for overlapping categories
   - Ensure hierarchical consistency

## Troubleshooting

### Common Issues

1. **Poor Category Quality**

   ```python
   # Solution: Adjust temperature for more focused generation
   config.engines["taxonomy_generation_engine"].temperature = 0.3
   ```

2. **Too Many/Few Categories**

   ```python
   # Solution: Adjust prompts or minibatch size
   config.minibatch_size = 8  # Larger batches = fewer categories
   ```

3. **Slow Processing**
   ```python
   # Solution: Reduce iterations or use smaller batches
   config.max_iterations = 2
   config.minibatch_size = 3
   ```

## API Reference

For detailed API documentation, see the [API Reference](../../../../docs/source/api/document_modifiers/tnt/index.rst).

## See Also

- [`haive.agents.document_modifiers`](../): Parent module
- [`haive.agents.document_modifiers.base`](../base/): Base document processing
- [LangGraph TNT Tutorial](https://langchain-ai.github.io/langgraph/tutorials/tnt-llm/tnt-llm/): Original implementation reference
