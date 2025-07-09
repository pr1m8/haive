# Haive Core: AugLLM Module

## Overview

The AugLLM module provides a comprehensive system for creating enhanced LLM chains with advanced configuration, structured output, tool integration, and debugging capabilities. It streamlines the creation of complex LLM interactions while ensuring type safety, validation, and customization options. This module bridges the gap between LangChain runnables and Haive's engine architecture.

## Key Features

- **Declarative Configuration**: Build complex LLM chains with a simple, declarative configuration API
- **Structured Output**: Generate structured, validated outputs using Pydantic models
- **Tool Integration**: Seamlessly integrate tools with automatic configuration and validation
- **Prompt Management**: Flexible prompt template creation with support for few-shot learning
- **Debugging Support**: Rich debugging capabilities for tracing and troubleshooting
- **Composability**: Chain and compose multiple LLM configurations together
- **Type Safety**: End-to-end type validation for inputs and outputs

## Installation

This module is part of the `haive-core` package. Install the full package with:

```bash
pip install haive-core
```

Or install via Poetry:

```bash
poetry add haive-core
```

## Quick Start

```python
from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable
from pydantic import BaseModel, Field

# Define a structured output model
class Analysis(BaseModel):
    main_points: list[str] = Field(description="The main points from the text")
    sentiment: str = Field(description="The overall sentiment (positive/negative/neutral)")

# Create a configuration
config = AugLLMConfig(
    name="text_analyzer",
    system_message="You are an expert text analyzer. Extract key information from the input text.",
    structured_output_model=Analysis,
    temperature=0.1
)

# Create a runnable
analyzer = compose_runnable(config)

# Use the runnable
result = analyzer.invoke("The new product launch exceeded expectations, with sales reaching 150% of targets.")
print(f"Main Points: {result.main_points}")
print(f"Sentiment: {result.sentiment}")
```

## Components

### AugLLMConfig

The central configuration class for defining LLM chain behavior.

```python
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool

# Create a basic configuration
config = AugLLMConfig(
    name="assistant",
    system_message="You are a helpful AI assistant.",
    llm=ChatOpenAI(temperature=0.7)
)

# Configuration with tools
config_with_tools = AugLLMConfig(
    name="research_assistant",
    system_message="You are a research assistant with access to various tools.",
    tools=[
        Tool.from_function(
            func=search_web,
            name="search_web",
            description="Search the web for information"
        )
    ],
    structured_tools_format=True  # Use OpenAI function-calling format
)

# Configuration with structured output
from pydantic import BaseModel, Field

class MovieReview(BaseModel):
    title: str = Field(description="The title of the movie")
    rating: float = Field(description="Rating from 0.0 to 10.0")
    pros: list[str] = Field(description="List of positive aspects")
    cons: list[str] = Field(description="List of negative aspects")

structured_config = AugLLMConfig(
    name="movie_reviewer",
    system_message="You are a film critic who provides detailed movie reviews.",
    structured_output_model=MovieReview,
    temperature=0.3
)
```

### AugLLMFactory

Factory for transforming configurations into executable runnables.

```python
from haive.core.engine.aug_llm import AugLLMFactory, AugLLMConfig

# Create a configuration
config = AugLLMConfig(
    name="code_assistant",
    system_message="You are a Python programming assistant.",
    temperature=0.2
)

# Use the factory to create a runnable
factory = AugLLMFactory()
code_assistant = factory.create_runnable(config)

# Invoke the runnable
response = code_assistant.invoke("Write a Python function to calculate Fibonacci numbers")
```

### Utility Functions

Tools for composing, chaining, and managing runnables.

```python
from haive.core.engine.aug_llm import (
    AugLLMConfig,
    compose_runnable,
    chain_runnables,
    create_runnables_dict
)

# Create multiple configurations
summarizer_config = AugLLMConfig(
    name="summarizer",
    system_message="Summarize the input text concisely."
)

translator_config = AugLLMConfig(
    name="translator",
    system_message="Translate the text to French."
)

# Create individual runnables
summarizer = compose_runnable(summarizer_config)
translator = compose_runnable(translator_config)

# Chain runnables together
summary_then_translate = chain_runnables([summarizer, translator])

# Create a dictionary of runnables
runnables_dict = create_runnables_dict({
    "summarizer": summarizer_config,
    "translator": translator_config
})
```

## Usage Patterns

### Structured Output Generation

```python
from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable
from pydantic import BaseModel, Field
from typing import List

# Define a structured output model
class TextAnalysis(BaseModel):
    topics: List[str] = Field(description="Main topics discussed in the text")
    summary: str = Field(description="Brief summary of the content")
    sentiment: str = Field(description="Overall sentiment (positive/negative/neutral)")
    key_entities: List[str] = Field(description="Important entities mentioned")

# Create a configuration with structured output
config = AugLLMConfig(
    name="text_analyzer",
    system_message="""
    You are an expert text analyzer. Extract key information from the input text,
    including main topics, a brief summary, sentiment, and key entities mentioned.
    """,
    structured_output_model=TextAnalysis,
    temperature=0.1
)

# Create and use the runnable
analyzer = compose_runnable(config)
result = analyzer.invoke("The new AI breakthrough from OpenAI has excited researchers worldwide, though some critics express concerns about potential misuse.")

print(f"Topics: {result.topics}")
print(f"Summary: {result.summary}")
print(f"Sentiment: {result.sentiment}")
print(f"Key Entities: {result.key_entities}")
```

### Tool Integration

```python
from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable
from langchain_core.tools import Tool
import requests

# Define a weather lookup tool
def get_weather(location: str) -> str:
    """Get the current weather for a location."""
    # In a real implementation, this would call a weather API
    return f"The weather in {location} is currently sunny with a temperature of 22°C."

# Create a tool
weather_tool = Tool.from_function(
    func=get_weather,
    name="get_weather",
    description="Get the current weather for a specific location."
)

# Create a configuration with the tool
config = AugLLMConfig(
    name="weather_assistant",
    system_message="You are a helpful weather assistant. Use the provided tools to answer questions about weather.",
    tools=[weather_tool],
    structured_tools_format=True  # Use OpenAI function-calling format
)

# Create and use the runnable
assistant = compose_runnable(config)
result = assistant.invoke("What's the weather like in Paris today?")
print(result)
```

### Few-Shot Learning

```python
from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable
from langchain_core.messages import HumanMessage, AIMessage

# Define example conversations
examples = [
    {
        "input": "My computer won't turn on",
        "output": "Let's troubleshoot this step by step. First, check if the power cable is properly connected. Then, try a different power outlet. If that doesn't work, check if the battery is charged or if the power button is functioning properly."
    },
    {
        "input": "I'm getting a blue screen error",
        "output": "Blue screen errors (BSoD) often indicate hardware or driver issues. Try restarting in safe mode by pressing F8 during startup. Note the error code displayed, which will help identify the specific issue. Common fixes include updating drivers, running memory diagnostics, or checking for recent hardware changes."
    }
]

# Convert to message pairs
few_shot_examples = []
for example in examples:
    few_shot_examples.append([
        HumanMessage(content=example["input"]),
        AIMessage(content=example["output"])
    ])

# Create a configuration with few-shot examples
config = AugLLMConfig(
    name="tech_support",
    system_message="You are a helpful IT support specialist who provides step-by-step troubleshooting advice.",
    few_shot_examples=few_shot_examples,
    temperature=0.3
)

# Create and use the runnable
support_agent = compose_runnable(config)
result = support_agent.invoke("My laptop is running very slowly")
print(result)
```

## Configuration

The AugLLMConfig class provides extensive configuration options:

```python
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_openai import ChatOpenAI
from typing import Dict, Any

# Create a configuration with advanced options
config = AugLLMConfig(
    # Basic configuration
    name="advanced_assistant",
    system_message="You are an advanced AI assistant with specialized capabilities.",

    # LLM configuration
    llm=ChatOpenAI(model="gpt-4"),
    temperature=0.2,
    max_tokens=2000,

    # Tool configuration
    tools=[search_tool, calculator_tool],
    structured_tools_format=True,

    # Output configuration
    structured_output_model=ResponseModel,
    output_parser=custom_parser,  # Optional custom parser

    # Prompt configuration
    human_message_template="User query: {input}",
    few_shot_examples=examples,

    # Processing hooks
    pre_process_function=lambda x: preprocess_input(x),
    post_process_function=lambda x: postprocess_output(x),

    # Debugging
    debug=True,
    verbose=True,

    # Execution configuration
    streaming=True,
    asynchronous=False,

    # Metadata
    metadata={"version": "1.0", "author": "AI Team"}
)
```

## Integration with Other Modules

### Integration with Engine Module

```python
from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable
from haive.core.engine.base import EngineInput, EngineOutput
from pydantic import BaseModel, Field

# Define input and output schemas
class QuestionInput(EngineInput):
    question: str = Field(description="The question to answer")
    context: str = Field(description="Additional context", default="")

class AnswerOutput(EngineOutput):
    answer: str = Field(description="The answer to the question")
    confidence: float = Field(description="Confidence score from 0.0 to 1.0")

# Create AugLLM configuration
config = AugLLMConfig(
    name="qa_engine",
    system_message="Answer questions accurately based on the provided context.",
    structured_output_model=AnswerOutput,
    temperature=0.1
)

# Create a runnable
qa_runnable = compose_runnable(config)

# Create an engine from the runnable
from haive.core.engine.base import create_engine_from_runnable

QAEngine = create_engine_from_runnable(
    name="QAEngine",
    runnable=qa_runnable,
    input_schema=QuestionInput,
    output_schema=AnswerOutput
)

# Instantiate and use the engine
engine = QAEngine()
result = engine.run(QuestionInput(
    question="What is the capital of France?",
    context="France is a country in Western Europe."
))
```

### Integration with Graph Module

```python
from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable
from haive.core.graph.node import create_node
from haive.core.graph.state_graph import BaseGraph
from langgraph.graph import START, END

# Create AugLLM configurations
retriever_config = AugLLMConfig(
    name="retriever",
    system_message="Extract key search terms from the user's question.",
    structured_output_model=SearchTerms
)

generator_config = AugLLMConfig(
    name="generator",
    system_message="Generate a comprehensive answer based on the retrieved information.",
    tools=[search_tool]
)

# Create runnables
retriever = compose_runnable(retriever_config)
generator = compose_runnable(generator_config)

# Create nodes
retriever_node = create_node(
    retriever,
    name="retrieve",
    input_mapping={"input": "question"},
    output_mapping={"search_terms": "search_terms"}
)

generator_node = create_node(
    generator,
    name="generate",
    input_mapping={"input": "question", "context": "search_results"},
    output_mapping={"response": "answer"}
)

# Create a graph
graph = BaseGraph(name="qa_workflow")
graph.add_node("retrieve", retriever_node)
graph.add_node("generate", generator_node)

# Add edges
graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)

# Compile and run
runnable_graph = graph.compile()
result = runnable_graph.invoke({"question": "What are the main features of quantum computing?"})
```

## Best Practices

- **Use Structured Output**: Leverage Pydantic models for type-safe structured output
- **Enable Debugging**: Use `debug=True` during development to inspect LLM inputs and outputs
- **Leverage Pre/Post Processing**: Implement custom processing for input preparation and output refinement
- **Chain Runnables**: Break complex tasks into smaller, focused LLM configurations and chain them
- **Reuse Configurations**: Create base configurations and extend them for specific use cases
- **Set Appropriate Temperature**: Use lower temperatures (0.0-0.3) for factual/structured tasks and higher values for creative tasks
- **Manage Context Length**: Be mindful of token limits, especially with tools and few-shot examples

## Advanced Usage

### Custom Output Parsers

````python
from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable
from langchain_core.output_parsers import BaseOutputParser
from typing import Dict, Any

# Create a custom output parser
class JSONListParser(BaseOutputParser):
    """Parse the output as a JSON list."""

    def parse(self, text: str) -> list:
        # Extract JSON content if enclosed in ```json and ```
        if "```json" in text and "```" in text.split("```json", 1)[1]:
            json_str = text.split("```json", 1)[1].split("```", 1)[0].strip()
        else:
            # Try to find any JSON-like array in the text
            import re
            match = re.search(r'\[(.*)\]', text, re.DOTALL)
            json_str = match.group(0) if match else text

        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # Fallback for non-JSON output
            return [{"item": text.strip()}]

    def get_format_instructions(self) -> str:
        return "Provide your response as a JSON list enclosed in ```json and ``` tags."

# Use the custom parser in a configuration
config = AugLLMConfig(
    name="list_generator",
    system_message="Generate a list of items based on the input prompt.",
    output_parser=JSONListParser(),
    temperature=0.5
)

# Create and use the runnable
list_generator = compose_runnable(config)
result = list_generator.invoke("List 5 best practices for Python programming")
for item in result:
    print(f"- {item}")
````

### Configuration Merging

```python
from haive.core.engine.aug_llm import AugLLMConfig, merge_configs

# Create a base configuration
base_config = AugLLMConfig(
    name="base_assistant",
    system_message="You are a helpful assistant.",
    temperature=0.7,
    max_tokens=1000
)

# Create a specialized configuration
code_config = AugLLMConfig(
    name="code_assistant",
    system_message="You are a programming assistant specializing in Python code.",
    temperature=0.2
)

# Merge configurations (code_config overrides base_config)
merged_config = merge_configs(base_config, code_config)

print(merged_config.name)  # "code_assistant"
print(merged_config.system_message)  # "You are a programming assistant specializing in Python code."
print(merged_config.temperature)  # 0.2
print(merged_config.max_tokens)  # 1000 (inherited from base_config)
```

## API Reference

For full API details, see the [documentation](https://docs.haive.ai/core/engine/aug_llm).

## Related Modules

- **haive.core.engine**: Parent module providing the engine abstraction
- **haive.core.models.llm**: LLM model configurations and implementations
- **haive.core.graph**: Graph system that can incorporate AugLLM components
- **haive.core.schema**: Schema definitions that can be used with structured outputs
