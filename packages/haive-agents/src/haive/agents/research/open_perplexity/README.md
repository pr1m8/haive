# Open Perplexity Research Agent

A deep research agent with dynamic document loader selection, built to perform comprehensive research on any topic and produce detailed reports with confidence assessments.

## Features

- Dynamic document loader selection based on research topics
- Multi-stage research pipeline with source evaluation
- Comprehensive report generation with confidence assessment
- State visualization and history tracking
- Command-line interface for running research and visualizing results

## Installation

The Open Perplexity agent is part of the Haive framework. To use it:

```bash
# Clone the repository
git clone <repository-url>
cd <repository-directory>

# Install dependencies
pip install -e .
```

## Usage

### Command Line Interface

Run research from a text file:

```bash
python -m haive.agents.open_perplexity.cli research path/to/question.txt --output report.md --save-state history.json
```

Visualize a saved state:

```bash
python -m haive.agents.open_perplexity.cli visualize history.json --markdown report.md
```

### Python API

```python
from haive.agents.open_perplexity import ResearchAgent, ResearchAgentConfig
from haive.core.models.vectorstore.base import VectorStoreConfig
from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig

# Configure embedding and vector store
embedding_config = HuggingFaceEmbeddingConfig(
    model="sentence-transformers/all-mpnet-base-v2"
)
vectorstore_config = VectorStoreConfig(
    embedding_model=embedding_config,
    vector_store_path="research_vector_store"
)

# Create agent configuration
config = ResearchAgentConfig.from_scratch(
    vectorstore_config=vectorstore_config,
    research_depth=3,
    concurrent_searches=3,
    max_sources_per_query=5
)

# Initialize and run the agent
agent = ResearchAgent(config=config)
research_question = "What is the current state of quantum computing?"
final_state = agent.run({"input_text": research_question})

# Generate a report
report = agent.generate_markdown_report(final_state)
print(report)

# Save state history for later analysis
agent.save_state_history("research_state_history.json")
```

## Examples

Check the `examples` directory for sample scripts:

- `run_with_visualization.py`: Demonstrates a complete research workflow with visualization

## Architecture

The research agent follows a multi-stage workflow:

1. **Process Input**: Extract the research topic and question
2. **Generate Report Plan**: Create a structured outline for the research
3. **Generate Search Queries**: Produce targeted search queries for each section
4. **Recommend Document Loaders**: Select appropriate document loaders based on research needs
5. **Execute Searches**: Retrieve information from various sources
6. **Evaluate Sources**: Assess the reliability and relevance of retrieved information
7. **Write Sections**: Generate content for each report section
8. **Consolidate Findings**: Extract key insights from all sections
9. **Assess Confidence**: Evaluate the overall confidence in the research findings
10. **Compile Final Report**: Generate a comprehensive research report

## Extension

To add new document loaders, implement them using the Langchain document loader interface. 