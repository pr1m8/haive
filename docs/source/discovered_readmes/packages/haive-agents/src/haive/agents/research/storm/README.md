# STORM Agent - Strategic Topic Organization and Research Method

STORM is a research assistant that generates comprehensive Wikipedia-style articles on user-provided topics. It implements a sophisticated multi-stage approach based on the work by Shao, et al. that extends the idea of "outline-driven RAG" for richer article generation.

## Overview

The STORM agent applies two main insights to produce comprehensive, well-researched articles:

1. **Creating an outline by querying similar topics helps improve coverage**
2. **Multi-perspective, grounded conversation simulation increases reference count and information density**

## Architecture

STORM consists of three main sub-agents that work together sequentially:

### 1. Research Agent

The Research Agent handles the initial stage of article creation:

- **Outline Generator**: Creates an initial outline for the Wikipedia article
- **Related Subjects Finder**: Identifies related topics to inform research
- **Perspective Identifier**: Creates diverse editor personas with different backgrounds and expertise

### 2. Interview Agent

The Interview Agent simulates conversations between editors and domain experts:

- **Editor Questioner**: Generates questions from the editor's perspective
- **Expert Responder**: Searches for information and provides expert answers with citations
- **Reference Collector**: Extracts and organizes references from the interviews

### 3. Writing Agent

The Writing Agent handles the final article creation process:

- **Outline Refiner**: Updates the outline based on interview insights
- **Section Writer**: Writes individual sections with citations to references
- **Article Assembler**: Creates the final cohesive article

## Key Features

- **Modular Design**: Each component is a separate agent that can be used independently
- **Shared State**: All agents share a common state schema for seamless information flow
- **Dynamic RAG**: Uses vector store and retriever for knowledge management
- **Multi-perspective Research**: Incorporates diverse viewpoints for comprehensive coverage
- **Expert Simulation**: Simulates conversations to extract detailed information
- **Reference Management**: Collects and indexes references for citation in the final article

## Requirements

- Python 3.8+
- LangChain >= 0.1.0
- LangGraph >= 0.0.20
- Azure OpenAI API access
- OpenAI API access (for embeddings)

## Installation

```bash
# Install required packages
pip install langchain langchain_openai langchain_community langgraph pydantic
```

## Usage

### Basic Usage

```python
from haive.agents.sequence.storm import STORMAgentConfig, STORMAgent

# Create the STORM agent config
storm_config = STORMAgentConfig(
    name="research_assistant",
    topic="Quantum Computing Applications"
)

# Build the agent
storm_agent = storm_config.build_agent()

# Run the agent
result = await storm_agent.arun("Quantum Computing Applications")

# Get the generated article
article = result.get("article")
print(article)
```

### Command Line Usage

Use the provided example script:

```bash
python examples/storm_agent_example.py "Artificial Intelligence Ethics" \
    --output ai_ethics.md \
    --perspectives 4 \
    --turns 6 \
    --verbose
```

### Customization

The STORM agent is highly configurable:

#### LLM Models

```python
from haive.core.models.llm.base import AzureLLMConfig

# Configure different models for different stages
fast_llm = AzureLLMConfig(model="gpt-4o-mini")
long_context_llm = AzureLLMConfig(model="gpt-4o")

storm_config = STORMAgentConfig(
    fast_llm_config=fast_llm,
    long_context_llm_config=long_context_llm
)
```

#### Vector Store and Retriever

```python
from haive.core.engine.vectorstore import VectorStoreConfig
from haive.core.engine.retriever import VectorStoreRetrieverConfig
from haive.core.models.embeddings.base import OpenAIEmbeddingConfig

# Configure embeddings
embedding_model = OpenAIEmbeddingConfig(model="text-embedding-3-small")

# Configure vector store
vector_store_config = VectorStoreConfig(
    vector_store_provider="Chroma",
    embedding_model=embedding_model,
    persist_directory="/path/to/vectorstore"
)

# Configure retriever
retriever_config = VectorStoreRetrieverConfig(
    vector_store_config=vector_store_config,
    k=4,
    search_type="mmr",  # Maximum Marginal Relevance
    search_kwargs={"lambda_mult": 0.5}
)

storm_config = STORMAgentConfig(
    vector_store_config=vector_store_config,
    retriever_config=retriever_config
)
```

#### Interview Parameters

```python
# Configure the number of perspectives and turns
storm_config = STORMAgentConfig(
    num_perspectives=5,  # More diverse viewpoints
    max_interview_turns=8  # Deeper conversations
)
```

### Advanced: Using Independent Sub-agents

You can use the sub-agents independently:

```python
from haive.agents.sequence.storm.research import ResearchAgentConfig, ResearchAgent

# Configure just the research agent
research_config = ResearchAgentConfig(
    name="outline_generator",
    topic="Neural Networks",
    llm_config=AzureLLMConfig(model="gpt-4o-mini")
)

# Build and run just the research stage
research_agent = research_config.build_agent()
research_result = await research_agent.arun("Neural Networks")

# Get the outline and perspectives
outline = research_result.get("initial_outline")
perspectives = research_result.get("perspectives")
```

## Workflow

1. The STORM agent starts with a topic provided by the user
2. The Research Agent generates an initial outline and identifies diverse perspectives
3. The Interview Agent conducts simulated interviews with each perspective
4. The Writing Agent refines the outline, writes sections, and assembles the final article
5. The completed article is returned to the user

## Implementation Details

- **Asynchronous Execution**: All components support async execution for better performance
- **Error Handling**: Robust error handling ensures the process continues even if individual components fail
- **Progress Tracking**: Detailed logging provides visibility into the generation process
- **State Management**: Shared state ensures seamless information flow between components

## Limitations

- The quality of the generated article depends on the quality of the search results
- The process is computationally intensive and may require significant time to complete
- API costs can accumulate for longer, more complex topics

## Future Improvements

- **Fact-checking**: Enhanced verification of cited information
- **Multimedia Support**: Inclusion of images, diagrams, and other media
- **Collaborative Writing**: Multiple agents working on different sections simultaneously
- **Human-in-the-loop**: Interactive refinement with human feedback
- **Incremental Updates**: Ability to update existing articles with new information

## References

This implementation is based on the work described in:
"STORM: A Multi-perspective Research Assistant for Generating Rich Articles" by Shao, et al.
