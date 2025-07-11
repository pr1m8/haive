# Documentation Build Strategy for Haive

**Date**: 2025-01-08
**Purpose**: Define comprehensive documentation build approach for complex monorepo

## Overview

The Haive codebase has unique challenges:

- Monorepo with multiple packages
- Tools organized in non-standard ways (`toolkits/` vs direct imports)
- Distributed examples throughout modules
- Complex type hints and inheritance
- Need for both API docs and interactive demos

## Documentation Strategy

### 1. **Sphinx Configuration Improvements**

```python
# conf.py improvements needed

# Better autodoc configuration
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__',
    'show-inheritance': True,
    'inherited-members': True,
}

# Type hint configuration
autodoc_typehints = 'both'  # Show in signature AND description
autodoc_typehints_format = 'short'
autodoc_type_aliases = {
    'HaiveAgent': 'haive.agents.base.Agent',
    'ToolType': 'Union[Tool, Callable]',
}

# Mock imports for missing/optional dependencies
autodoc_mock_imports = [
    # These don't exist but are referenced
    'haive.tools.api',
    'haive.tools.utility',
    'haive.tools.code',
    'haive.agents.rag.self_rag',
    'haive.core.schema.compatibility',
    'haive.agents.planning.llm_compiler',

    # External dependencies that might not be installed
    'langchain_community',
    'langgraph',
    'libcst',
    'networkx',
]

# Napoleon settings for Google-style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = autodoc_type_aliases
```

### 2. **Custom Documentation Generator**

Create a custom extension to handle Haive's structure:

```python
# _extensions/haive_autodoc.py

from sphinx.ext.autodoc import ModuleDocumenter, ClassDocumenter
from sphinx.util import logging
import inspect
import ast

logger = logging.getLogger(__name__)

class HaiveModuleDocumenter(ModuleDocumenter):
    """Custom documenter that understands Haive's structure."""

    def import_object(self):
        """Import with fallback for reorganized modules."""
        try:
            return super().import_object()
        except ImportError as e:
            # Handle known reorganizations
            if 'tools.code' in str(e):
                # Redirect to actual location
                self.modname = self.modname.replace('tools.code', 'tools.toolkits.dev.tools')
                return super().import_object()
            raise

class HaiveToolDocumenter(ClassDocumenter):
    """Special handling for tool classes."""

    def add_content(self, more_content, no_docstring=False):
        """Add tool-specific information."""
        super().add_content(more_content, no_docstring)

        # Add tool metadata if available
        if hasattr(self.object, '_tool_metadata'):
            self.add_line('', '<autodoc>')
            self.add_line('**Tool Metadata:**', '<autodoc>')
            self.add_line('', '<autodoc>')
            for key, value in self.object._tool_metadata.items():
                self.add_line(f'- **{key}**: {value}', '<autodoc>')

def setup(app):
    app.add_autodocumenter(HaiveModuleDocumenter, override=True)
    app.add_autodocumenter(HaiveToolDocumenter)
    return {'version': '1.0'}
```

### 3. **Documentation Templates**

#### Module Documentation Template

```rst
{{ fullname }}
{{ '=' * len(fullname) }}

.. automodule:: {{ fullname }}
   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:
   :special-members: __init__

   .. rubric:: Overview

   {{ module_overview }}

   .. rubric:: Type Definitions

   .. autosummary::
      :nosignatures:
      :toctree: _autosummary

      {% for type in type_definitions %}
      {{ type }}
      {% endfor %}

   .. rubric:: Classes

   .. autosummary::
      :nosignatures:
      :toctree: _autosummary
      :template: custom-class-template.rst

      {% for class in classes %}
      {{ class }}
      {% endfor %}

   .. rubric:: Functions

   .. autosummary::
      :nosignatures:
      :toctree: _autosummary

      {% for func in functions %}
      {{ func }}
      {% endfor %}

   .. rubric:: Examples

   .. include:: {{ example_file }}
      :start-after: [example-start]
      :end-before: [example-end]

   .. rubric:: See Also

   - :doc:`/guides/{{ guide_name }}` - Usage guide
   - :doc:`/api/{{ parent_module }}` - Parent module
```

#### Class Documentation Template

```rst
{{ fullname }}
{{ '=' * len(fullname) }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:
   :special-members: __init__, __call__

   .. rubric:: Type Parameters

   {% if type_params %}
   .. list-table::
      :header-rows: 1
      :widths: 20 80

      * - Parameter
        - Description
      {% for param in type_params %}
      * - ``{{ param.name }}``
        - {{ param.description }}
      {% endfor %}
   {% endif %}

   .. rubric:: Configuration

   {% if config_class %}
   .. autoclass:: {{ config_class }}
      :members:
      :show-inheritance:
   {% endif %}

   .. rubric:: State Schema

   {% if state_schema %}
   .. autoclass:: {{ state_schema }}
      :members:
      :show-inheritance:
   {% endif %}

   .. rubric:: Example Usage

   .. code-block:: python

      {{ example_code }}

   .. rubric:: Visualization

   {% if has_graph %}
   .. raw:: html

      <div id="{{ objname }}-graph" class="agent-graph-container">
        <!-- Graph visualization will be rendered here -->
      </div>
   {% endif %}
```

### 4. **Google-Style Docstring Standards**

```python
# Example of proper Google-style docstring for Haive

from typing import TypeVar, Generic, Optional, Dict, Any, List
from haive.core.schema import StateSchema

TState = TypeVar('TState', bound=StateSchema)

class Agent(Generic[TState]):
    """Base class for all Haive agents.

    This class provides the foundation for building conversational and task-oriented
    agents. It handles state management, graph compilation, and execution flow.

    Args:
        name: Unique identifier for the agent instance.
        engine: Language model engine configuration or instance.
        state_schema: State schema class defining the agent's memory structure.
            If not provided, will be composed from engine schemas.
        tools: List of tools available to the agent. Tools can be functions,
            Tool instances, or toolkit names.
        checkpointer: Persistence backend for state management. Defaults to
            in-memory storage.
        interrupt_before: List of node names to pause execution before.
        interrupt_after: List of node names to pause execution after.
        debug: Enable debug logging and execution tracing.

    Attributes:
        name: Agent's unique identifier.
        graph: Compiled state graph representing the agent's workflow.
        state_schema: Pydantic model defining state structure.
        tools: Dictionary of available tools mapped by name.

    Type Parameters:
        TState: State schema type, must inherit from StateSchema.

    Raises:
        ConfigurationError: If engine or state schema configuration is invalid.
        ToolError: If tool initialization fails.

    Examples:
        Basic usage with default state:

        >>> agent = Agent(name="assistant")
        >>> response = await agent.arun("Hello!")
        >>> print(response)
        'Hello! How can I help you today?'

        Custom state schema:

        >>> class MyState(StateSchema):
        ...     context: str = ""
        ...     history: List[str] = Field(default_factory=list)
        ...
        >>> agent = Agent(
        ...     name="contextual",
        ...     state_schema=MyState
        ... )

        With tools:

        >>> agent = Agent(
        ...     name="researcher",
        ...     tools=["web_search", "calculator"]
        ... )

    Note:
        Agents are stateful and maintain conversation context. Use the
        `config` parameter with a `thread_id` to maintain state across
        multiple interactions.

    See Also:
        - :class:`SimpleAgent`: Basic conversational agent
        - :class:`ReactAgent`: Agent with reasoning and tool use
        - :class:`MultiAgent`: Orchestrator for multiple agents
    """

    def __init__(
        self,
        name: str,
        engine: Optional[Union[Engine, EngineConfig]] = None,
        state_schema: Optional[Type[TState]] = None,
        tools: Optional[List[Union[Tool, Callable, str]]] = None,
        checkpointer: Optional[BaseCheckpointSaver] = None,
        interrupt_before: Optional[List[str]] = None,
        interrupt_after: Optional[List[str]] = None,
        debug: bool = False
    ) -> None:
        """Initialize the agent.

        See class docstring for detailed parameter descriptions.
        """
        pass

    async def arun(
        self,
        input: Union[str, Dict[str, Any]],
        *,
        config: Optional[RunnableConfig] = None,
        **kwargs: Any
    ) -> Any:
        """Execute the agent asynchronously.

        Args:
            input: User input as string or structured dictionary.
            config: Runtime configuration including thread_id for state.
            **kwargs: Additional arguments passed to the graph execution.

        Returns:
            Agent's response. Type depends on output schema configuration.

        Raises:
            ExecutionError: If graph execution fails.
            TimeoutError: If execution exceeds configured timeout.

        Examples:
            Simple execution:

            >>> response = await agent.arun("What's the weather?")

            With conversation state:

            >>> config = {"configurable": {"thread_id": "user123"}}
            >>> await agent.arun("My name is Alice", config=config)
            >>> response = await agent.arun("What's my name?", config=config)
            >>> assert "Alice" in response
        """
        pass
```

### 5. **Build Process Improvements**

```makefile
# Enhanced Makefile

.PHONY: docs docs-clean docs-build docs-serve docs-test

# Build with proper settings
docs-build:
	poetry run sphinx-build -b html \
		-d _build/doctrees \
		-j auto \
		-E \
		-T \
		source _build/html

# Build only changed files (faster)
docs-incremental:
	poetry run sphinx-build -b html \
		-d _build/doctrees \
		-j auto \
		source _build/html

# Test documentation
docs-test:
	poetry run sphinx-build -b doctest source _build/doctest
	poetry run sphinx-build -b linkcheck source _build/linkcheck

# Generate API docs automatically
docs-apidoc:
	poetry run sphinx-apidoc -f -e -M -T \
		--implicit-namespaces \
		-t _templates \
		-o source/api \
		../packages/*/src/haive

# Full rebuild
docs: docs-clean docs-apidoc docs-build
```

### 6. **Type Hint Documentation**

Use `sphinx-autodoc-typehints` with custom rendering:

```python
# In conf.py
from sphinx_autodoc_typehints import format_annotation

def custom_format_annotation(annotation, config):
    """Custom type hint formatter."""
    # Simplify complex types
    if hasattr(annotation, '__module__'):
        if annotation.__module__.startswith('haive.'):
            # Use short names for Haive types
            return annotation.__name__
    return format_annotation(annotation, config)

# Configure
typehints_formatter = custom_format_annotation
```

### 7. **Documentation Coverage Report**

```python
# scripts/check_doc_coverage.py

import ast
import os
from pathlib import Path

def check_docstring_coverage(package_path):
    """Generate documentation coverage report."""
    stats = {
        'modules': {'total': 0, 'documented': 0},
        'classes': {'total': 0, 'documented': 0},
        'functions': {'total': 0, 'documented': 0},
        'methods': {'total': 0, 'documented': 0},
    }

    for py_file in Path(package_path).rglob('*.py'):
        if '__pycache__' in str(py_file):
            continue

        with open(py_file) as f:
            try:
                tree = ast.parse(f.read())
            except:
                continue

        # Check module docstring
        stats['modules']['total'] += 1
        if ast.get_docstring(tree):
            stats['modules']['documented'] += 1

        # Walk the AST
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                stats['classes']['total'] += 1
                if ast.get_docstring(node):
                    stats['classes']['documented'] += 1

            elif isinstance(node, ast.FunctionDef):
                if node.name.startswith('_') and not node.name.startswith('__'):
                    continue  # Skip private methods

                category = 'methods' if isinstance(node, ast.AsyncFunctionDef) else 'functions'
                stats[category]['total'] += 1
                if ast.get_docstring(node):
                    stats[category]['documented'] += 1

    return stats
```

## Implementation Steps

1. **Update conf.py** with enhanced autodoc settings
2. **Create custom documenters** for Haive-specific patterns
3. **Generate proper API structure** respecting actual module layout
4. **Add type hint processing** for better readability
5. **Create documentation templates** for consistent output
6. **Set up coverage reporting** to track progress
7. **Optimize build process** for faster iteration

## Benefits

- Handles complex monorepo structure
- Respects actual module organization (toolkits vs direct imports)
- Provides rich type information
- Generates interactive examples
- Maintains consistency across all modules
- Tracks documentation completeness
