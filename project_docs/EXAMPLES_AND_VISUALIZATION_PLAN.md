# Examples and Visualization Implementation Plan

**Date**: January 22, 2025
**Purpose**: Comprehensive plan for implementing documentation examples and visualizations

## 🎯 Overview

This document outlines the strategy for implementing proper examples gallery and visualizations in the Haive documentation.

## 📚 1. Sphinx Gallery Implementation

### What is Sphinx Gallery?

Sphinx Gallery converts Python scripts into:

- Rendered documentation pages with code and output
- Downloadable Python scripts
- Jupyter notebooks
- Thumbnail galleries

### Required Format

```python
"""
Title of Example
================

This is a description of what the example demonstrates.
"""

# Standard imports
import haive
from haive.agents.simple import SimpleAgent

# %%
# Section Header
# --------------
#
# Text explaining this section. Note the space after # for reST rendering.

# Code for this section
agent = SimpleAgent(name="example")
result = agent.run("Hello")
print(result)

# %%
# Another Section
# ---------------
#
# More explanation here.

# More code
# Any plots generated here will be automatically captured
```

### Key Requirements

1. **File naming**: Must match pattern in config (`*tutorial.py`, `*guide.py`, `*example.py`)
2. **Docstring**: Triple-quoted string at top with title and description
3. **Section markers**: `# %%` to separate code blocks
4. **Comments**: Lines starting with `# ` (with space) become reST text
5. **Output capture**: Print statements and plots are automatically captured

## 🎨 2. Visualization Options

### A. Mermaid Diagrams (Already Available)

**Capabilities**:

- Agent workflow diagrams
- State machine visualizations
- Architecture diagrams
- Sequence diagrams

**Implementation**:

```python
from haive.core.graph.utils.mermaid_visualizer import MermaidVisualizer

# Create Mermaid diagram
visualizer = MermaidVisualizer(graph)
mermaid_code = visualizer.generate_mermaid()

# Save as HTML or image
visualizer.save_as_html("workflow.html")
visualizer.save_as_image("workflow.png")  # Requires mermaid-cli
```

### B. D3.js Interactive Visualizations

**Current Status**: Placeholder classes exist in `haive-graph-visualizations.js`

**Needed Implementation**:

1. **AgentGraphVisualizer**: Interactive agent workflow graphs
2. **AgentStateHistory**: Timeline of state changes
3. **AgentMetricsVisualizer**: Performance metrics charts

**Example D3.js Integration**:

```javascript
class AgentGraphVisualizer {
  constructor(containerId, graphData) {
    this.svg = d3
      .select(`#${containerId}`)
      .append("svg")
      .attr("width", 800)
      .attr("height", 600);

    this.simulation = d3
      .forceSimulation()
      .force(
        "link",
        d3.forceLink().id((d) => d.id),
      )
      .force("charge", d3.forceManyBody())
      .force("center", d3.forceCenter(400, 300));
  }

  render() {
    // Implement node and edge rendering
  }
}
```

### C. Matplotlib Visualizations

**For Static Plots**:

- Agent performance metrics
- State transition diagrams
- Comparison charts

**Example**:

```python
import matplotlib.pyplot as plt

def plot_agent_performance(metrics):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(metrics['time'], metrics['accuracy'])
    ax.set_title('Agent Performance Over Time')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Accuracy')
    plt.show()  # Automatically captured by Sphinx Gallery
```

## 📂 3. Example Organization Strategy

### Categorization

```
examples/
├── quickstart/
│   ├── first_agent.py          # Minimal hello world
│   ├── basic_conversation.py   # Simple chat
│   └── first_tool.py           # Adding tools
├── agents/
│   ├── simple_agent/
│   │   ├── basic_usage.py
│   │   ├── structured_output.py
│   │   └── with_memory.py
│   ├── react_agent/
│   │   ├── reasoning_loops.py
│   │   ├── tool_usage.py
│   │   └── complex_tasks.py
│   └── multi_agent/
│       ├── sequential_flow.py
│       ├── parallel_execution.py
│       └── supervisor_pattern.py
├── tools/
│   ├── custom_tools.py
│   ├── tool_validation.py
│   └── async_tools.py
├── games/
│   ├── tic_tac_toe_ai.py
│   ├── chess_engine.py
│   └── custom_game.py
├── advanced/
│   ├── rag_pipeline.py
│   ├── memory_systems.py
│   └── production_deployment.py
└── visualizations/
    ├── agent_graphs.py
    ├── state_diagrams.py
    └── performance_metrics.py
```

### Metadata Format

Each example should have:

```python
"""
Title: Building a Customer Service Agent
Level: Intermediate
Time: 15 minutes
Prerequisites: Basic Python, SimpleAgent basics
Tags: agents, customer-service, structured-output

This example demonstrates how to build a customer service agent
that can handle inquiries, route to departments, and generate
structured responses.
"""
```

## 🚀 4. Implementation Steps

### Phase 1: Convert Existing Examples (Week 1)

1. **Select Best Examples**:
   - Simple agent tutorial ✓ (already in format)
   - React agent tutorial ✓ (already in format)
   - Multi-agent supervisor pattern
   - RAG agent example
   - Tool creation example

2. **Convert to Gallery Format**:
   - Add proper docstrings
   - Add `# %%` section markers
   - Ensure output is captured
   - Test gallery generation

### Phase 2: Create Visualizations (Week 2)

1. **Mermaid Diagrams**:
   - Agent architecture diagram
   - State flow diagrams
   - Tool integration flowchart
   - Multi-agent communication

2. **Interactive D3.js**:
   - Implement AgentGraphVisualizer
   - Create live execution viewer
   - Add state timeline visualization

### Phase 3: New Examples (Week 3)

1. **Quickstart Series**:
   - 5-minute first agent
   - Adding your first tool
   - Basic error handling

2. **Advanced Patterns**:
   - Production RAG pipeline
   - Custom memory systems
   - Performance optimization

### Phase 4: Integration (Week 4)

1. **Gallery Pages**:
   - Update gallery.rst
   - Create category pages
   - Add navigation
   - Link from main docs

2. **Interactive Features**:
   - "Try it live" buttons
   - Colab/Binder links
   - Parameter playgrounds

## 🛠️ 5. Technical Requirements

### Dependencies

```toml
[tool.poetry.group.docs]
sphinx-gallery = "^0.15.0"
matplotlib = "^3.8.0"
pillow = "^10.0.0"           # For image generation
sphinx-copybutton = "^0.5.2" # Copy button for code
nbsphinx = "^0.9.3"          # Notebook support
```

### JavaScript Libraries

```html
<!-- In documentation template -->
<script src="https://d3js.org/d3.v7.min.js"></script>
<script src="https://unpkg.com/mermaid@10/dist/mermaid.min.js"></script>
<script src="_static/haive-graph-visualizations.js"></script>
```

### Build Configuration

```python
# conf.py additions
sphinx_gallery_conf = {
    'examples_dirs': ['../../examples'],
    'gallery_dirs': ['auto_examples'],
    'subsection_order': ExplicitOrder([
        '../../examples/quickstart',
        '../../examples/agents',
        '../../examples/tools',
        '../../examples/advanced',
    ]),
    'within_subsection_order': FileNameSortKey,
    'capture_repr': ('_repr_html_', '__repr__'),
    'matplotlib_animations': True,
    'image_scrapers': ('matplotlib',),
}
```

## 📊 6. Example Template

```python
"""
Building a Research Assistant with RAG
======================================

**Level**: Intermediate
**Time**: 20 minutes
**Prerequisites**: SimpleAgent, Vector stores

This example shows how to build a research assistant that can:
- Search through documents
- Synthesize information
- Provide cited responses
- Handle follow-up questions
"""

# %%
# Setup and Imports
# -----------------
#
# First, we'll import the necessary components and set up our environment.

from haive.agents.rag import BaseRAGAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.retriever import SimpleRetriever
import matplotlib.pyplot as plt

# %%
# Create the RAG Agent
# --------------------
#
# We'll create a RAG agent with a simple retriever for demonstration.

# Configure the agent
config = AugLLMConfig(
    temperature=0.3,  # Lower temperature for factual responses
    system_message="You are a research assistant. Always cite your sources."
)

# Create retriever with sample documents
retriever = SimpleRetriever()
retriever.add_documents([
    "Document 1: Python is a high-level programming language...",
    "Document 2: Machine learning is a subset of AI...",
    "Document 3: RAG combines retrieval with generation..."
])

# Initialize the agent
agent = BaseRAGAgent(
    name="research_assistant",
    engine=config,
    retriever=retriever,
    k=3  # Retrieve top 3 documents
)

# %%
# Example Query
# -------------
#
# Let's ask our research assistant about Python and ML.

query = "How is Python used in machine learning?"
response = agent.run(query)

print(f"Query: {query}")
print(f"Response: {response}")

# %%
# Visualize Retrieval Process
# ----------------------------
#
# We can visualize which documents were retrieved and their relevance scores.

# Get retrieval metrics
metrics = agent.get_last_retrieval_metrics()

# Create visualization
fig, ax = plt.subplots(figsize=(10, 6))
documents = [f"Doc {i+1}" for i in range(len(metrics['scores']))]
scores = metrics['scores']

bars = ax.bar(documents, scores, color=['#0066cc', '#4da6ff', '#b3d9ff'])
ax.set_xlabel('Documents')
ax.set_ylabel('Relevance Score')
ax.set_title('Document Retrieval Scores')
ax.set_ylim(0, 1)

# Add value labels on bars
for bar, score in zip(bars, scores):
    height = bar.get_height()
    ax.annotate(f'{score:.3f}',
                xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')

plt.tight_layout()
plt.show()

# %%
# Advanced Features
# -----------------
#
# The RAG agent supports many advanced features:
#
# - **Streaming responses**: Get tokens as they're generated
# - **Source tracking**: Know exactly which documents were used
# - **Custom retrievers**: Plug in any retrieval system
# - **Hybrid search**: Combine semantic and keyword search

# Example with streaming
print("\nStreaming response:")
for chunk in agent.stream("What are the key features of Python?"):
    print(chunk, end='', flush=True)

# %%
# Performance Visualization
# -------------------------
#
# Let's visualize the agent's performance over multiple queries.

queries = [
    "What is Python?",
    "Explain machine learning",
    "How does RAG work?",
    "Compare Python and Java",
    "What is deep learning?"
]

latencies = []
retrieval_times = []

for q in queries:
    metrics = agent.run_with_metrics(q)
    latencies.append(metrics['total_time'])
    retrieval_times.append(metrics['retrieval_time'])

# Create performance plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Latency plot
ax1.plot(range(len(queries)), latencies, 'o-', color='#0066cc', linewidth=2, markersize=8)
ax1.set_xlabel('Query Number')
ax1.set_ylabel('Total Latency (s)')
ax1.set_title('Query Response Times')
ax1.grid(True, alpha=0.3)

# Retrieval vs Generation time
generation_times = [l - r for l, r in zip(latencies, retrieval_times)]
x = range(len(queries))
width = 0.35

ax2.bar([i - width/2 for i in x], retrieval_times, width, label='Retrieval', color='#4da6ff')
ax2.bar([i + width/2 for i in x], generation_times, width, label='Generation', color='#0066cc')
ax2.set_xlabel('Query Number')
ax2.set_ylabel('Time (s)')
ax2.set_title('Time Breakdown: Retrieval vs Generation')
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

# %%
# Conclusion
# ----------
#
# This example demonstrated how to:
#
# 1. Create a RAG agent with custom retrieval
# 2. Visualize the retrieval process
# 3. Track performance metrics
# 4. Use advanced features like streaming
#
# **Next Steps**:
#
# - Try different retrieval strategies
# - Experiment with reranking models
# - Add document preprocessing
# - Implement caching for better performance
#
# For more examples, check out:
#
# - :doc:`/auto_examples/agents/rag_with_chroma`
# - :doc:`/auto_examples/advanced/production_rag`
# - :doc:`/auto_examples/tools/custom_retriever`
"""
```

## 🎯 7. Success Metrics

1. **Gallery Generation**: All examples render properly
2. **Interactivity**: D3.js visualizations work smoothly
3. **Download Options**: Scripts and notebooks available
4. **Navigation**: Easy to find relevant examples
5. **Performance**: Page load time < 3 seconds
6. **Coverage**: Examples for all major features

## 🚀 Next Steps

1. Start converting existing examples to Sphinx Gallery format
2. Implement D3.js visualization classes
3. Create Mermaid architecture diagrams
4. Set up example categorization
5. Test gallery generation locally
6. Deploy and gather feedback

This plan provides a clear path to creating a professional, interactive documentation experience with rich examples and visualizations.
