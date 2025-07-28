# Example Output Handling in Sphinx Documentation

**Created**: 2025-01-27
**Purpose**: Guide for handling code examples and their outputs in Haive documentation
**Status**: Best practices for sphinx-gallery, sphinx-exec-directive, and jupyter-cache

## 🎯 Overview

Haive has three powerful tools installed for handling example outputs:

1. **sphinx-gallery** (^0.19.0) - Create galleries of examples with outputs
2. **sphinx-exec-directive** (^0.6) - Execute code blocks and show outputs inline
3. **jupyter-cache** (^1.0.1) - Cache executed notebooks to speed up builds

## 📦 Available Tools

### 1. Sphinx Gallery

**Purpose**: Create beautiful galleries of Python examples with outputs, plots, and downloadable scripts.

**Configuration in conf.py**:

```python
# Add to extensions
extensions = [
    'sphinx_gallery.gen_gallery',
    # ... other extensions
]

# Configure sphinx-gallery
sphinx_gallery_conf = {
    'examples_dirs': [
        '../../examples',  # Source of examples
        '../../packages/haive-agents/examples',
        '../../packages/haive-core/examples',
    ],
    'gallery_dirs': [
        'auto_examples',  # Where to save generated galleries
        'auto_examples/agents',
        'auto_examples/core',
    ],
    'filename_pattern': r'\.py$',  # Which files to process
    'ignore_pattern': r'__init__\.py|test_.*\.py',  # Files to ignore
    'plot_gallery': True,  # Generate plots
    'download_all_examples': True,  # Add download buttons
    'remove_config_comments': True,  # Clean up special comments
    'expected_failing_examples': [],  # List examples that should fail
    'run_stale_examples': True,  # Re-run modified examples
    'matplotlib_animations': True,  # Support animations
    'image_scrapers': ('matplotlib',),  # What generates images
    'reset_argv': True,  # Reset sys.argv for each example
    'capture_repr': ('_repr_html_', '__repr__'),  # Capture these outputs
    'nested_sections': True,  # Allow nested sections in examples
    'backreferences_dir': 'gen_modules/backreferences',  # Cross-references
    'doc_module': ('haive',),  # Modules to document
    'reference_url': {
        'haive': None,  # Use local references
    },
    'show_memory': True,  # Show memory usage
    'show_signature': True,  # Show function signatures
    'copyfile_regex': r'.*\.(py|rst|md)$',  # Files to copy
    'parallel': True,  # Parallel execution
    'n_jobs': -1,  # Use all cores
}
```

**Example File Structure**:

```python
"""
Simple Agent Example
===================

This example demonstrates how to create and use a SimpleAgent.

This initial block is the example description. It will be rendered
as the introduction to the example page.
"""

# %%
# Import necessary modules
# ------------------------
# First, we import the required modules

from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

# %%
# Create the agent
# ----------------
# Now we create a simple agent with basic configuration

config = AugLLMConfig(
    temperature=0.7,
    max_tokens=100
)

agent = SimpleAgent(
    name="example_agent",
    engine=config
)

print(f"Created agent: {agent.name}")
print(f"Temperature: {config.temperature}")

# %%
# Run the agent
# -------------
# Let's run the agent with a simple query

result = agent.run("What is the capital of France?")
print(f"Agent response: {result}")

# %%
# Plot agent metrics (if applicable)
# ----------------------------------

import matplotlib.pyplot as plt
import numpy as np

# Example metrics visualization
x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(8, 4))
plt.plot(x, y)
plt.title('Agent Performance Over Time')
plt.xlabel('Time')
plt.ylabel('Performance')
plt.grid(True)
plt.show()

# %%
# .. note::
#    This example demonstrates basic agent usage. For more advanced
#    examples, see the multi-agent examples.
```

### 2. Sphinx Exec Directive

**Purpose**: Execute code blocks inline and show their output directly in the documentation.

**Configuration**:

```python
# Add to extensions
extensions = [
    'sphinx_exec_directive',
    # ... other extensions
]

# Optional configuration
exec_directive_config = {
    'exec_debug': False,  # Debug mode
    'exec_timeout': 30,   # Timeout in seconds
}
```

**Usage in RST**:

```rst
.. exec::
   :linenos:
   :hide-code:

   from haive.agents.simple import SimpleAgent
   from haive.core.engine.aug_llm import AugLLMConfig

   agent = SimpleAgent(
       name="demo",
       engine=AugLLMConfig()
   )

   print(f"Agent created: {agent.name}")
   print(f"Agent type: {type(agent).__name__}")
```

**Usage in Markdown (MyST)**:

````markdown
```{exec} python
:linenos:
:show-output:

from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Create and run agent
agent = SimpleAgent(name="example", engine=AugLLMConfig())
result = agent.run("Hello, world!")
print(f"Response: {result}")
```
````

**Options**:

- `:linenos:` - Show line numbers
- `:hide-code:` - Hide the code, show only output
- `:hide-output:` - Hide output, show only code
- `:show-output:` - Explicitly show output (default)
- `:caption: Title` - Add a caption

### 3. Jupyter Cache

**Purpose**: Cache executed Jupyter notebooks to speed up documentation builds.

**Configuration**:

```python
# Add to extensions
extensions = [
    'jupyter_sphinx',
    'myst_nb',  # If using notebooks with MyST
    # ... other extensions
]

# Configure jupyter execution
jupyter_execute_notebooks = "cache"  # Use cache

# Configure cache
jupyter_cache_config = {
    'cache_dir': '_jupyter_cache',
    'timeout': 600,  # 10 minutes
    'allow_errors': False,
    'kernel_name': 'python3',
}

# For MyST-NB
nb_execution_mode = "cache"
nb_execution_cache_path = "_jupyter_cache"
nb_execution_timeout = 600
nb_execution_allow_errors = False
```

**Usage with Notebooks**:

````markdown
```{nb-code} python
:linenos:
:number-lines: 1

# This will be executed and cached
from haive.agents.react import ReactAgent
agent = ReactAgent(name="cached_example")
print(agent.name)
```

```{nb-output}
:class: output
:name: my-output

cached_example
```
````

## 🎨 Best Practices

### 1. Organizing Examples

```
examples/
├── README.rst
├── agents/
│   ├── simple_agent_example.py
│   ├── react_agent_example.py
│   └── multi_agent_example.py
├── tools/
│   ├── calculator_tool.py
│   └── web_search_tool.py
└── advanced/
    ├── memory_management.py
    └── state_persistence.py
```

### 2. Example Template

```python
"""
Title of Example
================

Brief description of what this example demonstrates.

.. note::
   Important information about prerequisites or setup.
"""

# %%
# Section Title
# -------------
# Description of this section

# Code here
print("Output will be captured")

# %%
# Another Section
# ---------------
# More explanation

# More code
result = some_function()
print(f"Result: {result}")

# %%
# Visualization (if applicable)
# -----------------------------

import matplotlib.pyplot as plt
# Plotting code
plt.show()

# %%
# .. seealso::
#    :ref:`related_example` : Description
#    :doc:`/user_guide/topic` : Related documentation
```

### 3. Controlling Execution

**Skip execution for specific blocks**:

```python
# %%
# .. skip-execution::
#
# This code won't be executed (e.g., requires external services)

result = expensive_api_call()  # This won't run
print("This is just for display")
```

**Expected failures**:

```python
# %%
# .. raises:: ValueError
#
# This demonstrates error handling

raise ValueError("This error is expected!")
```

**Conditional execution**:

```python
# %%
# .. only:: not skip_gpu
#
# GPU-specific code

import torch
model = torch.nn.Linear(10, 10).cuda()
```

### 4. Output Formatting

**Capture specific outputs**:

```python
# For sphinx-gallery
class MyClass:
    def _repr_html_(self):
        """Rich HTML representation."""
        return "<b>MyClass instance</b>"

    def __repr__(self):
        """Fallback text representation."""
        return "MyClass()"

# This will use _repr_html_ in the gallery
obj = MyClass()
obj  # Display the object
```

**Format console output**:

```python
# %%
# Formatted output example
# ------------------------

from rich.console import Console
from rich.table import Table

console = Console(record=True)

table = Table(title="Agent Comparison")
table.add_column("Agent Type", style="cyan")
table.add_column("Use Case", style="magenta")
table.add_column("Complexity", style="green")

table.add_row("SimpleAgent", "Basic Q&A", "Low")
table.add_row("ReactAgent", "Tool usage", "Medium")
table.add_row("MultiAgent", "Complex workflows", "High")

console.print(table)
print(console.export_text())  # This will be captured
```

## 🚀 Advanced Techniques

### 1. Interactive Examples

```python
# %%
# Interactive widget (works in Jupyter)
# -------------------------------------

try:
    import ipywidgets as widgets
    from IPython.display import display

    temperature = widgets.FloatSlider(
        value=0.7,
        min=0.0,
        max=2.0,
        step=0.1,
        description='Temperature:'
    )

    def update_agent(change):
        config = AugLLMConfig(temperature=change['new'])
        print(f"Temperature updated to: {change['new']}")

    temperature.observe(update_agent, names='value')
    display(temperature)
except ImportError:
    print("Interactive widgets require Jupyter environment")
```

### 2. Timing and Performance

```python
# %%
# Performance measurement
# -----------------------

import time

# Measure execution time
start = time.time()

agent = SimpleAgent(name="perf_test", engine=AugLLMConfig())
result = agent.run("Test query")

elapsed = time.time() - start
print(f"Execution time: {elapsed:.3f} seconds")

# sphinx-gallery will also show memory usage automatically
```

### 3. Async Examples

```python
# %%
# Async execution example
# -----------------------

import asyncio

async def run_agent_async():
    """Demonstrate async agent execution."""
    agent = SimpleAgent(name="async_test", engine=AugLLMConfig())

    # Run multiple queries concurrently
    tasks = [
        agent.arun("Query 1"),
        agent.arun("Query 2"),
        agent.arun("Query 3")
    ]

    results = await asyncio.gather(*tasks)

    for i, result in enumerate(results, 1):
        print(f"Query {i} result: {result[:50]}...")

    return results

# Execute async code in sync context
results = asyncio.run(run_agent_async())
print(f"Processed {len(results)} queries")
```

## 📋 Configuration Checklist

### For sphinx-gallery:

- [ ] Add example directories to `sphinx_gallery_conf['examples_dirs']`
- [ ] Set output directories in `sphinx_gallery_conf['gallery_dirs']`
- [ ] Configure ignore patterns for test files
- [ ] Enable `plot_gallery` for visualizations
- [ ] Set `parallel: True` for faster builds
- [ ] Add expected failing examples if any

### For sphinx-exec-directive:

- [ ] Add to extensions list
- [ ] Set appropriate timeout
- [ ] Configure debug mode if needed
- [ ] Use proper directives in documentation

### For jupyter-cache:

- [ ] Configure cache directory
- [ ] Set execution timeout
- [ ] Decide on error handling
- [ ] Clean cache periodically

## 🔍 Debugging Tips

### Debug sphinx-gallery:

```python
sphinx_gallery_conf = {
    'log_level': 'debug',  # Enable debug logging
    'show_memory': True,   # Show memory usage
    'junit': 'gallery-junit.xml',  # Generate test report
    'binder': {
        'org': 'haive',
        'repo': 'haive',
        'branch': 'main',
        'binderhub_url': 'https://mybinder.org',
        'dependencies': ['requirements.txt'],
    }
}
```

### Debug exec-directive:

```rst
.. exec::
   :debug:

   # This will show debug information
   import sys
   print(sys.version)
```

### Clear jupyter cache:

```bash
# Clear cache when debugging
rm -rf _jupyter_cache/
rm -rf docs/build/jupyter_execute/
```

## 🎯 Recommendations

1. **Use sphinx-gallery for**:
   - Complete example scripts
   - Examples with visualizations
   - Downloadable examples
   - Gallery-style documentation

2. **Use sphinx-exec-directive for**:
   - Small inline code snippets
   - Quick demonstrations
   - Dynamic content generation
   - API usage examples

3. **Use jupyter-cache for**:
   - Notebook-based tutorials
   - Long-running examples
   - Examples with complex outputs
   - Interactive documentation

## 📝 Example Integration

Here's how to integrate all three in your documentation:

```rst
Agent Examples
==============

Quick Demo
----------

Here's a quick example using exec-directive:

.. exec::
   :linenos:

   from haive.agents.simple import SimpleAgent
   agent = SimpleAgent(name="demo")
   print(f"Agent ready: {agent.name}")

Complete Examples
-----------------

For complete examples, see our gallery:

.. gallery-grid::
   :grid-columns: 1 2 2 3

   ../auto_examples/agents/simple_agent_example.py
   ../auto_examples/agents/react_agent_example.py
   ../auto_examples/agents/multi_agent_example.py

Jupyter Notebook Tutorial
-------------------------

For an interactive tutorial:

.. toctree::
   :maxdepth: 1

   notebooks/getting_started.ipynb
   notebooks/advanced_agents.ipynb
```

---

**Next Steps**:

1. Configure sphinx-gallery in conf.py
2. Create example scripts following the template
3. Add exec directives to existing documentation
4. Set up jupyter cache for notebooks
