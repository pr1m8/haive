# Haive Core: Utils Module

## Overview

The Utils module provides a comprehensive collection of utility functions and helper classes used throughout the Haive framework. It serves as a toolbox of reusable components that simplify common tasks, enhance functionality, and promote consistent implementation patterns across the framework.

## Key Features

- **Document Processing**: Utilities for handling document manipulation and transformation
- **File Operations**: Tools for reading, writing, and processing various file formats
- **Visualization**: Graph and state visualization capabilities
- **State Management**: Helpers for state inspection, debugging, and transformation
- **Serialization**: Tools for serializing and deserializing complex objects
- **Component Discovery**: System for discovering and analyzing Haive components
- **Pydantic Integration**: Utilities that enhance Pydantic model functionality
- **Configuration Management**: Helpers for loading and managing configurations

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
from haive.core.utils.file_utils import read_file_content
from haive.core.utils.doc_utils import format_docs, clean_page_content
from haive.core.utils.visualize_graph_utils import render_and_display_graph

# Read configuration or prompt files
prompt_content = read_file_content("path/to/prompt.md")

# Process documents
formatted_content = format_docs(documents)
cleaned_content = clean_page_content(document)

# Visualize a graph
render_and_display_graph(compiled_graph, output_name="my_workflow.png")
```

## Components

### Document Utilities

Utilities for processing and transforming document objects.

```python
from haive.core.utils.doc_utils import format_docs, combine_docs, clean_page_content
from langchain_core.documents import Document

# Create sample documents
doc1 = Document(page_content="First document content")
doc2 = Document(page_content="Second document content")
documents = [doc1, doc2]

# Format documents into a single string
formatted_text = format_docs(documents)
print(formatted_text)  # "First document content\n\nSecond document content"

# Combine documents into a single document
combined_doc = combine_docs(documents)
print(combined_doc.page_content)  # "First document content\n\nSecond document content"

# Clean document content
cleaned_doc = clean_page_content(Document(page_content="Content\nwith\nnewlines"))
print(cleaned_doc)  # "Content with newlines"
```

### File Utilities

Utilities for file operations and content handling.

```python
from haive.core.utils.file_utils import read_file_content, read_yaml_file

# Read a markdown file
markdown_content = read_file_content("path/to/instructions.md")

# Read a YAML configuration file
config = read_yaml_file("path/to/config.yaml")
print(config["parameters"])  # Access YAML structure
```

### Visualization Utilities

Tools for visualizing graphs and complex data structures.

```python
from haive.core.utils.visualize_graph_utils import render_and_display_graph
from haive.core.utils.mermaid_utils import generate_mermaid_diagram

# Render a LangGraph graph to PNG
render_and_display_graph(
    compiled_graph,
    output_dir="./visualizations/",
    output_name="agent_workflow.png"
)

# Generate a Mermaid diagram string
mermaid_code = generate_mermaid_diagram(graph_data)
```

### State Utilities

Tools for managing and debugging state in graph workflows.

```python
from haive.core.utils.state_utils import _debug_state_object

# Debug a complex state object
_debug_state_object(state, label="Agent State")

# Output shows state structure, types, and key attributes
# --- Agent State Debug ---
# Type: <class 'langgraph.state.State'>
# Has values: <class 'dict'>
# Messages in values: 5
# State attributes: ['__class__', '__delattr__', '__dict__', ...]
# ------------------------
```

### Component Discovery

System for discovering and analyzing Haive components.

```python
from haive.core.utils.haive_discovery import (
    discover_tools,
    discover_retrievers,
    generate_markdown_report
)

# Discover available tools
tools = discover_tools()
print(f"Found {len(tools)} tools")

# Discover retriever components
retrievers = discover_retrievers()

# Generate documentation report
report = generate_markdown_report(
    tools=tools,
    retrievers=retrievers,
    output_path="components_report.md"
)
```

### Pydantic Utilities

Enhanced functionality for Pydantic models.

```python
from haive.core.utils.pydantic_utils import model_to_dict, dict_to_model, sync_properties
from pydantic import BaseModel, Field
from typing import List, Optional

# Convert Pydantic model to dict with customization
class User(BaseModel):
    name: str
    email: str
    settings: dict = Field(default_factory=dict)

user = User(name="Test User", email="test@example.com")
user_dict = model_to_dict(user, exclude=["email"])

# Synchronize properties between models
class UserSettings(BaseModel):
    theme: str = "light"
    notifications: bool = True

settings = UserSettings()
sync_properties(user.settings, settings)
```

## Usage Patterns

### Document Processing Pipeline

```python
from haive.core.utils.doc_utils import format_docs, clean_page_content, save_docs_to_jsonl
from langchain_core.documents import Document

# Document processing pipeline
def process_documents(documents):
    # Clean each document
    cleaned_docs = [
        Document(page_content=clean_page_content(doc), metadata=doc.metadata)
        for doc in documents
    ]

    # Save processed documents
    save_docs_to_jsonl(cleaned_docs, "processed_docs.jsonl")

    # Return formatted content for LLM input
    return format_docs(cleaned_docs)
```

### Configuration Management

```python
from haive.core.utils.config_utils import load_config, merge_configs
from haive.core.utils.env_utils import get_env_var, load_env_vars

# Load configuration with environment variable interpolation
config = load_config("config.yaml")

# Override with environment-specific settings
env_config = load_config(f"config.{get_env_var('ENVIRONMENT', 'dev')}.yaml")
merged_config = merge_configs(config, env_config)

# Ensure required environment variables
required_vars = ["API_KEY", "MODEL_NAME"]
load_env_vars(required_vars)
```

## Integration with Other Modules

### Integration with Graph Module

````python
from haive.core.graph.state_graph import BaseGraph
from haive.core.utils.visualize_graph_utils import render_and_display_graph
from haive.core.utils.mermaid_utils import generate_mermaid_diagram

# Create a graph
graph = BaseGraph(name="workflow")
# ... add nodes and edges ...

# Compile graph
compiled = graph.compile()

# Visualize the graph
render_and_display_graph(compiled, output_name="workflow.png")

# Generate Mermaid diagram for documentation
mermaid_code = generate_mermaid_diagram(graph)
with open("workflow.md", "w") as f:
    f.write("```mermaid\n")
    f.write(mermaid_code)
    f.write("\n```")
````

### Integration with Document Loaders

```python
from haive.core.utils.doc_utils import format_docs, clean_page_content
from langchain_core.documents import Document

# Process loaded documents
def process_loaded_documents(docs):
    # Clean each document
    cleaned_docs = []
    for doc in docs:
        # Clean content
        content = clean_page_content(doc)
        # Create new document with cleaned content
        cleaned_doc = Document(
            page_content=content,
            metadata=doc.metadata
        )
        cleaned_docs.append(cleaned_doc)

    # Format for LLM consumption
    return format_docs(cleaned_docs)
```

## Best Practices

- **Use Standard Utilities**: Leverage the built-in utilities instead of reinventing common functionality
- **Consistent Document Handling**: Use document utilities for consistent document processing
- **Visualization for Debugging**: Incorporate graph visualization during development for easier debugging
- **Centralize Configuration**: Use configuration utilities for loading and managing settings
- **Component Discovery**: Use the discovery system to identify available components and generate documentation

## Advanced Usage

### Custom Component Discovery

```python
from haive.core.utils.haive_discovery import (
    ComponentAnalyzer,
    EnhancedComponentDiscovery,
    create_custom_analyzer
)

# Create custom component analyzer
class CustomComponentAnalyzer(ComponentAnalyzer):
    component_type = "custom_component"

    def analyze_component(self, component_class):
        # Custom analysis logic
        info = super().analyze_component(component_class)
        info.metadata["custom_field"] = extract_custom_field(component_class)
        return info

# Register and use custom analyzer
discovery = EnhancedComponentDiscovery()
discovery.register_analyzer(CustomComponentAnalyzer())

# Discover components
components = discovery.discover_components()

# Generate custom documentation
discovery.generate_documentation(
    output_dir="./docs/",
    template_path="./templates/custom_template.md"
)
```

### Enhanced Visualization

```python
from haive.core.utils.visualize_graph_utils import render_and_display_graph
from haive.core.graph.state_graph import BaseGraph
import os

# Create a graph visualization with execution history
def visualize_execution(graph, execution_history, output_dir="./visualizations"):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Render base graph
    render_and_display_graph(
        graph.compile(),
        output_dir=output_dir,
        output_name="graph_structure.png"
    )

    # Generate execution visualization with highlighted paths
    for i, step in enumerate(execution_history):
        # Create visualization for each execution step
        node_highlights = {step["current_node"]: "active"}
        edge_highlights = {
            (step["previous_node"], step["current_node"]): "traversed"
        }

        # Generate step visualization
        render_and_display_graph(
            graph.compile(),
            output_dir=output_dir,
            output_name=f"execution_step_{i}.png",
            node_highlights=node_highlights,
            edge_highlights=edge_highlights
        )
```

## API Reference

For full API details, see the [documentation](https://docs.haive.ai/core/utils).

## Related Modules

- **haive.core.common**: Provides common functionality that complements these utilities
- **haive.core.graph**: Uses visualization and state utilities for graph operations
- **haive.core.engine**: Leverages discovery utilities for engine management
- **haive.core.schema**: Integrates with Pydantic utilities for schema handling
