# Haive Core: Engine Module

## Overview

The Engine module provides foundational abstractions for creating and managing different types of AI engines within the Haive framework. Engines are composable components that encapsulate specific AI capabilities, such as language models, retrieval systems, vector stores, and document processors.

## Key Features

- **Standardized Interface**: Common interface for all engine types
- **Type Safety**: Input and output validation through Pydantic models
- **Composability**: Easy composition of engines for complex workflows
- **Extensibility**: Straightforward API for creating custom engines
- **LLM Integration**: Enhanced LLM configuration and interaction
- **Specialized Engines**: Purpose-built engines for common AI tasks

## Installation

This module is part of the `haive-core` package. Install the full package with:

```bash
pip install haive-core
```

Or install via Poetry:

```bash
poetry add haive-core
```

## Components

### Base Engine

The core engine abstraction that defines the standard interface for all engines:

```python
from haive.core.engine.base import BaseEngine, EngineInput, EngineOutput
from pydantic import Field

class CustomInput(EngineInput):
    query: str = Field(description="The input query")

class CustomOutput(EngineOutput):
    result: str = Field(description="The generated result")

class CustomEngine(BaseEngine):
    input_schema = CustomInput
    output_schema = CustomOutput

    def _run(self, input_data: CustomInput) -> CustomOutput:
        # Implementation
        return CustomOutput(result=f"Processed: {input_data.query}")
```

### Aug LLM

The enhanced LLM configuration and integration system:

```python
from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable
from pydantic import BaseModel, Field

# Define a structured output model
class Analysis(BaseModel):
    summary: str = Field(description="Brief summary of the content")
    sentiment: str = Field(description="Sentiment analysis result")

# Create a configuration
config = AugLLMConfig(
    name="content_analyzer",
    system_message="Analyze the provided content and extract key information.",
    structured_output_model=Analysis,
    temperature=0.1
)

# Create a runnable
analyzer = compose_runnable(config)
```

### Agent Engine

Agent engines provide high-level abstractions for creating AI agents with various capabilities:

```python
from haive.core.engine.agent import AgentEngine
from haive.core.schema import SchemaComposer

# Create an agent engine
schema = SchemaComposer.create({
    "messages": MessagesField(),
    "context": DictField()
})

agent = AgentEngine(
    state_schema=schema,
    tools=[search_tool, calculator_tool]
)

# Run the agent
result = agent.run({"messages": [{"role": "user", "content": "What is 25 * 16?"}]})
```

### Other Specialized Engines

The engine module includes several specialized engines for common AI tasks:

- **Document Engines**: Process and transform various document types
- **Retrieval Engines**: Retrieve relevant information from data sources
- **Vector Store Engines**: Store and query vector embeddings
- **Tool Engines**: Execute external tools and APIs

## Best Practices

- **Type Safety**: Define clear input and output schemas for all engines
- **Composability**: Build complex workflows by combining simple engines
- **Configuration**: Use appropriate configuration for different engine types
- **Error Handling**: Implement robust error handling in engine implementations
- **Testing**: Create tests for engine behavior with various inputs

## Related Modules

- **haive.core.graph**: Graph system that uses engines as node components
- **haive.core.models**: Model configurations used by engines
- **haive.core.schema**: Schema definitions for engine input and output validation
