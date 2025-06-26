# Haive Documentation Structure and Improvement Plan

## Current State Analysis

Based on my examination of the Haive documentation system, I've identified the following areas:

### Documentation Infrastructure

- **Build System**: Nox is used for documentation building and serving with the following commands:
  - `nox -s docs`: Build documentation incrementally
  - `nox -s docs-live`: Start a live server with auto-rebuild
  - `nox -s serve`: Serve built documentation
  - `nox -s docs-clean`: Clean documentation build
  - `nox -s docs-check`: Check documentation for errors

- **Framework**: Sphinx with extensions:
  - Core extensions: autodoc, autosummary, viewcode, napoleon
  - Additional: sphinx_copybutton, sphinx_tabs, sphinx_design, myst_parser, mermaid

- **Theme**: Furo (a clean, modern Sphinx theme)

### Content Structure

- **Top-Level Organization**:
  - Getting Started
  - Packages
  - User Guide
  - Examples
  - Agents Gallery
  - Games Showcase

- **Package Documentation**:
  - Core
  - Agents
  - Tools
  - Games
  - Dataflow
  - MCP
  - Prebuilt

### Issues Identified

1. **Missing Content**: Many of the linked pages appear to be missing or incomplete
2. **Inconsistent Structure**: Documentation structure doesn't match package organization
3. **Broken Cross-References**: Links to non-existent pages
4. **Incomplete API Documentation**: Auto-generated API docs are incomplete
5. **Lack of Examples**: Not enough practical examples
6. **Missing Package-Level Documentation**: No clear documentation for each package
7. **No Conceptual Documentation**: Missing explanations of core concepts
8. **Navigation Issues**: Disjointed navigation between sections

## Improvement Plan

### 1. Core Structure Reorganization

Create a consistent and comprehensive documentation structure:

```
docs/
├── source/
│   ├── index.rst                   # Main landing page
│   ├── getting_started.rst         # Installation and quick start
│   ├── concepts/                   # Core concepts
│   │   ├── index.rst
│   │   ├── agents.rst              # What are agents?
│   │   ├── langgraph.rst           # LangGraph integration
│   │   ├── tools.rst               # Tool usage
│   │   ├── engines.rst             # Engines explained
│   │   ├── registries.rst          # Registry system
│   │   └── extensions.rst          # Extending Haive
│   ├── packages/                   # Package-specific docs
│   │   ├── index.rst
│   │   ├── core/                   # haive-core package
│   │   ├── agents/                 # haive-agents package
│   │   ├── tools/                  # haive-tools package
│   │   ├── games/                  # haive-games package
│   │   ├── dataflow/               # haive-dataflow package
│   │   ├── mcp/                    # haive-mcp package
│   │   └── prebuilt/               # haive-prebuilt package
│   ├── guides/                     # User guides
│   │   ├── index.rst
│   │   ├── building_agents.rst
│   │   ├── using_tools.rst
│   │   ├── custom_engines.rst
│   │   ├── persistence.rst
│   │   └── deployment.rst
│   ├── examples/                   # Code examples
│   │   ├── index.rst
│   │   ├── simple_agent.rst
│   │   ├── rag_agent.rst
│   │   ├── tool_integration.rst
│   │   └── game_agent.rst
│   ├── api/                        # API reference
│   │   ├── index.rst               # Landing page for API docs
│   │   ├── core/                   # Auto-generated API docs
│   │   ├── agents/
│   │   ├── tools/
│   │   └── ...
│   └── _templates/                 # Templates for customization
```

### 2. Content Creation Priorities

1. **Core Documentation**:
   - Comprehensive getting started guide
   - Package overview pages
   - Core concepts documentation

2. **Package Documentation**:
   - README.md in each package
   - Module docstrings for public APIs
   - Examples for each package

3. **API Reference**:
   - Fix autodoc configuration
   - Ensure all public APIs are documented
   - Add cross-references

4. **Tutorials and Guides**:
   - Step-by-step tutorials for common tasks
   - Integration guides
   - Deployment guides

### 3. Implementation Strategy

#### Phase 1: Foundation (1-2 weeks)

- [x] Analyze current documentation
- [ ] Create missing directory structure
- [ ] Update root index.rst
- [ ] Write basic getting started guide
- [ ] Create package overview pages
- [ ] Fix configuration issues

#### Phase 2: Core Content (2-3 weeks)

- [ ] Write core concepts documentation
- [ ] Create package-specific READMEs
- [ ] Add Google-style docstrings to key modules
- [ ] Implement consistent API documentation
- [ ] Add cross-references between sections

#### Phase 3: Examples and Guides (2-3 weeks)

- [ ] Develop step-by-step tutorials
- [ ] Create code examples for each package
- [ ] Write integration guides
- [ ] Add troubleshooting sections
- [ ] Implement search functionality

#### Phase 4: Polish and Review (1-2 weeks)

- [ ] Review all documentation
- [ ] Fix broken links
- [ ] Ensure consistent styling
- [ ] Add missing cross-references
- [ ] Optimize for readability

## Technical Implementation Notes

### Poetry Integration

To build documentation with Poetry:

```bash
# Install dependencies
poetry install --with docs

# Build docs
poetry run sphinx-build -b html docs/source docs/build/html

# Start live server
poetry run sphinx-autobuild docs/source docs/build/html
```

### Automating Documentation Generation

1. **Module Docstrings**: Use Google-style docstrings for better rendering with Napoleon

```python
"""Module for agent functionality.

This module provides the core functionality for creating and managing agents
in the Haive framework.

Typical usage example:

    from haive.agents import SimpleAgent

    agent = SimpleAgent(name="My Agent")
    result = agent.invoke("Hello, world!")
"""
```

2. **Class Docstrings**: Include attributes, methods, and examples

```python
class SimpleAgent:
    """A simple agent implementation.

    This class provides a basic agent implementation that can process
    user inputs and generate responses using an LLM.

    Attributes:
        name: The name of the agent
        engine: The LLM engine configuration

    Example:
        >>> from haive.agents import SimpleAgent
        >>> agent = SimpleAgent(name="Assistant")
        >>> response = agent.invoke("Tell me about AI")
        >>> print(response)
    """
```

3. **Function Docstrings**: Document parameters, return values, and exceptions

```python
def invoke(self, input_text: str) -> str:
    """Process user input and generate a response.

    Args:
        input_text: The user input text to process

    Returns:
        A string containing the agent's response

    Raises:
        ValueError: If the input text is empty

    Example:
        >>> response = agent.invoke("Hello")
        >>> print(response)
        "Hello! How can I help you today?"
    """
```

### Continuous Integration

Add documentation building to CI workflow:

```yaml
docs:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.12"
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install poetry
        poetry install --with docs
    - name: Build documentation
      run: |
        poetry run sphinx-build -b html docs/source docs/build/html
    - name: Upload documentation
      uses: actions/upload-artifact@v3
      with:
        name: documentation
        path: docs/build/html
```

## Progress Tracking

| Section           | Status      | Assignee | Target Date |
| ----------------- | ----------- | -------- | ----------- |
| Getting Started   | Not Started |          |             |
| Core Concepts     | Not Started |          |             |
| Package: Core     | Not Started |          |             |
| Package: Agents   | Not Started |          |             |
| Package: Tools    | Not Started |          |             |
| Package: Games    | Not Started |          |             |
| Package: Dataflow | In Progress |          |             |
| Package: MCP      | Not Started |          |             |
| Package: Prebuilt | Not Started |          |             |
| API Reference     | Not Started |          |             |
| Examples          | Not Started |          |             |
| Guides            | Not Started |          |             |

## Next Steps

1. Create the basic directory structure for all documentation sections
2. Write skeleton files for each section to establish navigation
3. Focus on the getting started guide and package overviews
4. Add Google-style docstrings to key modules in each package
5. Set up automated documentation building and testing
