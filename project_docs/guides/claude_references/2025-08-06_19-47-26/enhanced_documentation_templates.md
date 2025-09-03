# Enhanced Documentation Templates for Haive

**Created**: 2025-08-06
**Purpose**: Ready-to-use RST templates leveraging all available Sphinx extensions

## 📚 Template Collection

### 1. Enhanced Main Landing Page (index.rst)

```rst
:sd-hide-title:

.. title:: Haive AI Agent Framework - Build Intelligent AI Agents

=========================
Haive AI Agent Framework
=========================

.. div:: sd-text-center sd-text-primary sd-fs-1 sd-font-weight-bold

   Build Production-Ready AI Agents 🤖

.. div:: sd-text-center sd-text-muted sd-fs-3 sd-mb-4

   Professional framework for creating sophisticated AI agents with conversational intelligence,
   tool orchestration, game strategies, and multi-agent coordination.

.. grid:: 1 2 2 3
   :gutter: 3
   :margin: 4 4 0 0
   :class-container: sd-text-center

   .. grid-item-card::
      :text-align: center
      :class-header: sd-bg-primary sd-text-white
      :class-card: sd-rounded-3

      **🚀 Quick Start**
      ^^^
      Get up and running in 5 minutes
      +++
      .. button-ref:: quickstart
         :color: primary
         :click-parent:
         :expand:

         Get Started

   .. grid-item-card::
      :text-align: center
      :class-header: sd-bg-info sd-text-white
      :class-card: sd-rounded-3

      **📖 User Guide**
      ^^^
      Learn concepts and best practices
      +++
      .. button-ref:: guides/index
         :color: info
         :click-parent:
         :expand:

         Learn More

   .. grid-item-card::
      :text-align: center
      :class-header: sd-bg-success sd-text-white
      :class-card: sd-rounded-3

      **📚 API Reference**
      ^^^
      Complete API documentation
      +++
      .. button-ref:: api/index
         :color: success
         :click-parent:
         :expand:

         Browse API

.. div:: sd-mt-4

   .. tab-set::

      .. tab-item:: Installation
         :sync: install

         .. code-block:: bash
            :caption: Install via pip
            :linenos:

            # Basic installation
            pip install haive

            # With all extras
            pip install haive[all]

            # Development installation
            git clone https://github.com/will-astley/haive
            cd haive
            poetry install

      .. tab-item:: Your First Agent
         :sync: first-agent

         .. code-block:: python
            :caption: simple_agent.py
            :linenos:
            :emphasize-lines: 7-9

            from haive.agents import SimpleAgent
            from haive.core.engine import AugLLMConfig

            # Configure the LLM
            config = AugLLMConfig(model="gpt-4", temperature=0.7)

            # Create your agent
            agent = SimpleAgent(
                name="assistant",
                engine=config
            )

            # Run the agent
            async def main():
                response = await agent.arun("Explain quantum computing")
                print(response)

            # Execute
            import asyncio
            asyncio.run(main())

      .. tab-item:: Agent with Tools
         :sync: tools

         .. code-block:: python
            :caption: react_agent.py
            :linenos:
            :emphasize-lines: 12-15

            from haive.agents import ReactAgent
            from haive.tools import WebSearchTool, CalculatorTool
            from haive.core.engine import AugLLMConfig

            # Create tools
            search = WebSearchTool()
            calculator = CalculatorTool()

            # Configure agent with tools
            config = AugLLMConfig(model="gpt-4")

            agent = ReactAgent(
                name="researcher",
                engine=config,
                tools=[search, calculator]
            )

            # Agent can now search and calculate
            result = await agent.arun(
                "What's the population of Tokyo and calculate 20% of it"
            )

.. dropdown:: 🎯 Why Choose Haive?
   :color: primary
   :icon: star
   :animate: fade-in-slide-down
   :class-container: sd-mt-4

   .. grid:: 2 2 3 4
      :gutter: 2
      :margin: 0

      .. grid-item::
         :columns: 12 6 6 3

         .. card::
            :text-align: center
            :class-card: sd-rounded-2

            **⚡ Fast**
            ^^^
            < 100ms response time with caching

      .. grid-item::
         :columns: 12 6 6 3

         .. card::
            :text-align: center
            :class-card: sd-rounded-2

            **🔒 Type Safe**
            ^^^
            Full Pydantic models & type hints

      .. grid-item::
         :columns: 12 6 6 3

         .. card::
            :text-align: center
            :class-card: sd-rounded-2

            **🚀 Scalable**
            ^^^
            Handle 10K+ agents per hour

      .. grid-item::
         :columns: 12 6 6 3

         .. card::
            :text-align: center
            :class-card: sd-rounded-2

            **🎯 Extensible**
            ^^^
            Plugin architecture for custom needs

.. div:: sd-mt-5

   .. mermaid::
      :align: center
      :caption: Haive Architecture Overview

      graph TB
          subgraph "Your Application"
              A[User Request]
          end

          subgraph "Haive Framework"
              B[Agent Router]
              C[SimpleAgent]
              D[ReactAgent]
              E[RAG Agent]
              F[Multi-Agent]
          end

          subgraph "Integrations"
              G[LLM APIs]
              H[Tools & APIs]
              I[Vector DBs]
              J[MCP Servers]
          end

          A --> B
          B --> C
          B --> D
          B --> E
          B --> F
          C --> G
          D --> G
          D --> H
          E --> G
          E --> I
          F --> J

          style A fill:#e1f5fe
          style B fill:#4fc3f7
          style G fill:#81c784
          style H fill:#81c784
          style I fill:#81c784
          style J fill:#81c784

.. rubric:: 📖 Documentation Sections

.. grid:: 1 2 2 3
   :gutter: 3
   :margin: 4 4 0 0

   .. grid-item-card:: 🏁 Getting Started
      :link: getting-started/index
      :link-type: doc

      - Installation guide
      - Quick start tutorial
      - Core concepts
      - First agent

   .. grid-item-card:: 🤖 Agent Types
      :link: agents/index
      :link-type: doc

      - SimpleAgent
      - ReactAgent
      - RAG agents
      - Multi-agent systems

   .. grid-item-card:: 🔧 Tools & Integration
      :link: tools/index
      :link-type: doc

      - Built-in tools
      - Custom tools
      - API integration
      - MCP servers

   .. grid-item-card:: 🎮 Game Intelligence
      :link: games/index
      :link-type: doc

      - Game frameworks
      - Strategy agents
      - Multi-player
      - Tournaments

   .. grid-item-card:: 💻 Examples
      :link: examples/index
      :link-type: doc

      - Code examples
      - Jupyter notebooks
      - Full applications
      - Best practices

   .. grid-item-card:: 📚 API Reference
      :link: api/index
      :link-type: doc

      - Complete API docs
      - Class references
      - Type definitions
      - Configuration

.. toctree::
   :hidden:
   :maxdepth: 2

   getting-started/index
   agents/index
   tools/index
   games/index
   examples/index
   api/index
```

### 2. Agent Documentation Template (agent_template.rst)

```rst
{{ fullname | escape | underline(line='=') }}

.. currentmodule:: {{ module }}

.. autopydantic_model:: {{ fullname }}
   :model-show-json: False
   :model-show-config-summary: True
   :model-show-field-summary: True
   :model-show-validator-members: True
   :field-list-validators: True
   :field-show-constraints: True
   :members:
   :inherited-members:
   :member-order: bysource

.. rubric:: Overview

{{ obj.docstring or "No description available." }}

.. dropdown:: Quick Example
   :color: primary
   :icon: code-square
   :animate: fade-in-slide-down
   :open:

   .. tab-set::

      .. tab-item:: Basic Usage

         .. code-block:: python
            :linenos:
            :caption: Basic {{ name }} usage

            from {{ module }} import {{ name }}
            from haive.core.engine import AugLLMConfig

            # Create agent
            agent = {{ name }}(
                name="my_agent",
                engine=AugLLMConfig()
            )

            # Execute
            result = await agent.arun("Your query here")
            print(result)

      .. tab-item:: With Configuration

         .. code-block:: python
            :linenos:
            :caption: Configured {{ name }}

            config = AugLLMConfig(
                model="gpt-4",
                temperature=0.7,
                max_tokens=2000,
                system_message="You are a helpful assistant"
            )

            agent = {{ name }}(
                name="configured_agent",
                engine=config,
                # Add other parameters
            )

      .. tab-item:: Advanced

         .. code-block:: python
            :linenos:
            :caption: Advanced {{ name }} usage

            # With tools (if applicable)
            agent = {{ name }}(
                name="advanced_agent",
                engine=config,
                tools=[tool1, tool2],
                # Other advanced options
            )

            # Stream responses
            async for chunk in agent.astream("Query"):
                print(chunk, end="")

.. rubric:: Architecture

.. mermaid::
   :align: center

   classDiagram
       class {{ name }} {
           +name: str
           +engine: AugLLMConfig
           +state: AgentState
           +run(input: str) str
           +arun(input: str) str
           +stream(input: str) Iterator
           +astream(input: str) AsyncIterator
       }

       class Agent {
           <<abstract>>
           +name: str
           +run(input: str)
           +arun(input: str)
       }

       Agent <|-- {{ name }}

.. rubric:: Configuration Options

.. list-table::
   :header-rows: 1
   :widths: 25 20 55
   :class: sd-table-hover

   * - Parameter
     - Type
     - Description
   * - ``name``
     - ``str``
     - Unique identifier for the agent
   * - ``engine``
     - ``AugLLMConfig``
     - LLM configuration
   * - ``state``
     - ``AgentState``
     - Initial agent state (optional)

.. rubric:: Methods

.. autosummary::
   :toctree: _autosummary
   :recursive:

   {% for item in methods %}
   ~{{ fullname }}.{{ item }}
   {%- endfor %}

.. dropdown:: Inherited Methods
   :color: secondary
   :icon: arrow-down-circle

   .. autosummary::
      :toctree: _autosummary

      {% for item in inherited_methods %}
      ~{{ fullname }}.{{ item }}
      {%- endfor %}

.. rubric:: Attributes

.. autosummary::
   :toctree: _autosummary

   {% for item in attributes %}
   ~{{ fullname }}.{{ item }}
   {%- endfor %}

.. rubric:: Examples

.. tab-set::

   .. tab-item:: Simple Example

      .. literalinclude:: ../../examples/{{ name.lower() }}_simple.py
         :language: python
         :caption: Simple {{ name }} example
         :linenos:

   .. tab-item:: Advanced Example

      .. literalinclude:: ../../examples/{{ name.lower() }}_advanced.py
         :language: python
         :caption: Advanced {{ name }} example
         :linenos:

   .. tab-item:: Real World

      .. literalinclude:: ../../examples/{{ name.lower() }}_real_world.py
         :language: python
         :caption: Real-world {{ name }} usage
         :linenos:

.. rubric:: See Also

- :class:`~haive.agents.base.Agent` - Base agent class
- :class:`~haive.core.engine.AugLLMConfig` - LLM configuration
- :doc:`/guides/agents` - Agent development guide
```

### 3. Tool Documentation Template (tool_template.rst)

```rst
{{ fullname | escape | underline(line='=') }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ fullname }}
   :members:
   :show-inheritance:

.. rubric:: Overview

{{ obj.docstring or "Tool for " + name }}

.. card:: Quick Info
   :class-card: sd-rounded-2

   .. grid:: 2
      :gutter: 2

      .. grid-item::
         :columns: 6

         **Category**: {{ category|default("General") }}

         **Requires**: {{ requirements|default("None") }}

      .. grid-item::
         :columns: 6

         **Async**: {{ "Yes" if async_tool else "No" }}

         **Rate Limited**: {{ "Yes" if rate_limited else "No" }}

.. rubric:: Usage

.. tab-set::

   .. tab-item:: Basic Usage

      .. code-block:: python
         :linenos:

         from {{ module }} import {{ name }}

         # Create tool
         tool = {{ name }}()

         # Use directly
         result = tool.invoke({"query": "Your input"})

         # Use with agent
         agent = ReactAgent(
             name="agent_with_tool",
             tools=[tool]
         )

   .. tab-item:: Configuration

      .. code-block:: python
         :linenos:

         # Configure the tool
         tool = {{ name }}(
             api_key="your-api-key",
             timeout=30,
             max_retries=3
         )

   .. tab-item:: Error Handling

      .. code-block:: python
         :linenos:

         try:
             result = tool.invoke({"query": "test"})
         except ToolException as e:
             print(f"Tool error: {e}")
         except Exception as e:
             print(f"Unexpected error: {e}")

.. rubric:: Input/Output Schema

.. tab-set::

   .. tab-item:: Input Schema

      .. autopydantic_model:: {{ fullname }}.InputSchema
         :model-show-json: True
         :model-show-config-summary: False
         :model-show-field-summary: True

   .. tab-item:: Output Schema

      .. autopydantic_model:: {{ fullname }}.OutputSchema
         :model-show-json: True
         :model-show-config-summary: False
         :model-show-field-summary: True

.. mermaid::
   :align: center
   :caption: Tool Flow

   sequenceDiagram
       participant Agent
       participant Tool
       participant API

       Agent->>Tool: invoke(input)
       Tool->>Tool: validate input
       Tool->>API: make request
       API-->>Tool: response
       Tool->>Tool: parse response
       Tool-->>Agent: return output

.. rubric:: Integration Examples

.. dropdown:: With SimpleAgent
   :color: info

   .. literalinclude:: ../../examples/tools/{{ name.lower() }}_simple.py
      :language: python
      :linenos:

.. dropdown:: With ReactAgent
   :color: info

   .. literalinclude:: ../../examples/tools/{{ name.lower() }}_react.py
      :language: python
      :linenos:

.. rubric:: API Reference

.. automethod:: {{ fullname }}.invoke
.. automethod:: {{ fullname }}.ainvoke
```

### 4. Guide/Tutorial Template (guide_template.rst)

```rst
{{ title }}
{{ "=" * len(title) }}

.. contents:: Table of Contents
   :local:
   :depth: 2
   :backlinks: top

.. rubric:: What You'll Learn

.. checklist::

   - [ ] Core concepts of {{ topic }}
   - [ ] How to implement {{ feature }}
   - [ ] Best practices and patterns
   - [ ] Common pitfalls to avoid
   - [ ] Real-world examples

.. admonition:: Prerequisites
   :class: note

   Before starting this guide, you should:

   - Have Haive installed (``pip install haive``)
   - Understand basic Python async/await
   - Be familiar with :doc:`/guides/quickstart`

Introduction
------------

.. lead::

   {{ introduction_text }}

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: Time to Complete
      :text-align: center

      **~30 minutes**

   .. grid-item-card:: Difficulty
      :text-align: center

      **{{ difficulty|default("Intermediate") }}**

Core Concepts
-------------

.. dropdown:: Concept 1: {{ concept_1_title }}
   :color: primary
   :icon: book
   :animate: fade-in

   {{ concept_1_description }}

   .. mermaid::

      graph LR
          A[Input] --> B[Process]
          B --> C[Output]

.. dropdown:: Concept 2: {{ concept_2_title }}
   :color: primary
   :icon: book
   :animate: fade-in

   {{ concept_2_description }}

Step-by-Step Tutorial
---------------------

.. tab-set::

   .. tab-item:: Step 1
      :sync: step1

      **{{ step_1_title }}**

      {{ step_1_description }}

      .. code-block:: python
         :linenos:
         :emphasize-lines: 3-5

         # Step 1 code
         {{ step_1_code }}

   .. tab-item:: Step 2
      :sync: step2

      **{{ step_2_title }}**

      {{ step_2_description }}

      .. code-block:: python
         :linenos:
         :emphasize-lines: 7-10

         # Step 2 code
         {{ step_2_code }}

   .. tab-item:: Step 3
      :sync: step3

      **{{ step_3_title }}**

      {{ step_3_description }}

      .. code-block:: python
         :linenos:

         # Step 3 code
         {{ step_3_code }}

.. rubric:: Complete Example

.. literalinclude:: ../../examples/guides/{{ guide_name }}_complete.py
   :language: python
   :caption: Complete working example
   :linenos:
   :emphasize-lines: 15-20

Best Practices
--------------

.. card-carousel:: 2

   .. card:: Do ✅
      :class-card: sd-bg-success sd-text-white

      - {{ best_practice_1 }}
      - {{ best_practice_2 }}
      - {{ best_practice_3 }}

   .. card:: Don't ❌
      :class-card: sd-bg-danger sd-text-white

      - {{ anti_pattern_1 }}
      - {{ anti_pattern_2 }}
      - {{ anti_pattern_3 }}

Common Issues
-------------

.. accordion::

   .. accordion-item:: Issue: {{ issue_1_title }}
      :class-title: sd-bg-warning

      **Problem**: {{ issue_1_problem }}

      **Solution**:

      .. code-block:: python

         {{ issue_1_solution }}

   .. accordion-item:: Issue: {{ issue_2_title }}
      :class-title: sd-bg-warning

      **Problem**: {{ issue_2_problem }}

      **Solution**:

      .. code-block:: python

         {{ issue_2_solution }}

Advanced Topics
---------------

.. only:: advanced

   .. dropdown:: Performance Optimization
      :color: secondary
      :icon: speedometer

      Tips for optimizing {{ topic }}...

   .. dropdown:: Scaling Considerations
      :color: secondary
      :icon: arrows-expand

      When scaling {{ topic }}...

Next Steps
----------

.. card:: 🎉 Congratulations!

   You've learned how to {{ achievement }}.

   **What's next?**

   .. button-ref:: {{ next_guide }}
      :color: primary
      :outline:

      Continue to {{ next_topic }}

   .. button-link:: https://github.com/will-astley/haive/discussions
      :color: secondary
      :outline:

      Join the Discussion

Related Resources
-----------------

.. seealso::

   - :doc:`/api/{{ related_api }}` - API documentation
   - :doc:`/examples/{{ related_example }}` - More examples
   - :doc:`/guides/{{ related_guide }}` - Related guide
```

### 5. Example Gallery Template (example_gallery.rst)

```rst
{{ title }}
{{ "=" * len(title) }}

.. gallery-grid::
   :grid-columns: 1 2 3

   .. gallery-grid-item::
      :tooltip: Basic agent example

      .. image:: /_static/images/examples/basic_agent_thumb.png
         :alt: Basic Agent

      .. div:: sd-text-center

         :doc:`/examples/basic_agent`

   .. gallery-grid-item::
      :tooltip: Agent with tools

      .. image:: /_static/images/examples/tools_agent_thumb.png
         :alt: Tools Agent

      .. div:: sd-text-center

         :doc:`/examples/agent_with_tools`

   .. gallery-grid-item::
      :tooltip: Multi-agent system

      .. image:: /_static/images/examples/multi_agent_thumb.png
         :alt: Multi-Agent

      .. div:: sd-text-center

         :doc:`/examples/multi_agent_system`

.. rubric:: Interactive Examples

.. jupyter-execute::
   :hide-code:

   # This will be executed and output shown
   from haive.agents import SimpleAgent
   agent = SimpleAgent(name="demo")
   print("Agent created successfully!")

.. thebe-button:: Launch Interactive Environment

Browse Examples by Category
---------------------------

.. tab-set::

   .. tab-item:: By Agent Type

      .. toctree::
         :maxdepth: 1

         examples/simple/*
         examples/react/*
         examples/rag/*
         examples/multi/*

   .. tab-item:: By Use Case

      .. toctree::
         :maxdepth: 1

         examples/chatbot/*
         examples/research/*
         examples/automation/*
         examples/games/*

   .. tab-item:: By Difficulty

      .. toctree::
         :maxdepth: 1

         examples/beginner/*
         examples/intermediate/*
         examples/advanced/*
```

## 🎨 CSS Customizations for Extensions

Create `_static/custom.css`:

```css
/* Enhanced Sphinx Design Components */
.sd-card {
  border: 1px solid var(--color-background-border);
  transition: all 0.3s ease;
}

.sd-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  border-color: var(--color-brand-primary);
}

/* Animated dropdowns */
.sd-dropdown {
  margin: 1.5rem 0;
}

.sd-dropdown summary {
  cursor: pointer;
  padding: 0.75rem 1rem;
  background: var(--color-background-secondary);
  border-radius: 8px;
  transition: all 0.2s;
}

.sd-dropdown summary:hover {
  background: var(--color-background-hover);
}

/* Tab styling */
.sphinx-tabs {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.sphinx-tabs .sphinx-tabs-nav {
  background: var(--color-background-secondary);
  padding: 0;
}

.sphinx-tabs .sphinx-tabs-tab {
  padding: 0.75rem 1.5rem;
  transition: all 0.2s;
}

.sphinx-tabs .sphinx-tabs-tab[aria-selected="true"] {
  background: var(--color-brand-primary);
  color: white;
}

/* Mermaid diagrams */
.mermaid {
  background: var(--color-background-secondary);
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

/* Copy button improvements */
.highlight {
  position: relative;
}

.highlight .copybtn {
  opacity: 0;
  transition: opacity 0.2s;
}

.highlight:hover .copybtn {
  opacity: 1;
}

/* Autodoc enhancements */
.py.class,
.py.function,
.py.method {
  border-left: 4px solid var(--color-brand-primary);
  padding-left: 1rem;
  margin: 2rem 0;
  transition: all 0.2s;
}

.py.class:hover,
.py.function:hover,
.py.method:hover {
  background: var(--color-background-hover);
  border-left-width: 6px;
}

/* Grid improvements */
.sd-container-fluid {
  padding: 0;
}

.sd-row > * {
  padding: 0.5rem;
}

/* Checklist styling */
.checklist {
  list-style: none;
  padding-left: 0;
}

.checklist li::before {
  content: "☐ ";
  color: var(--color-brand-primary);
  font-weight: bold;
}

.checklist li.checked::before {
  content: "✓ ";
  color: var(--color-success);
}

/* Admonition improvements */
.admonition {
  border-radius: 8px;
  border-left-width: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

/* Gallery grid */
.gallery-grid {
  display: grid;
  gap: 1.5rem;
  margin: 2rem 0;
}

.gallery-grid-item {
  border: 1px solid var(--color-background-border);
  border-radius: 8px;
  padding: 1rem;
  transition: all 0.2s;
}

.gallery-grid-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
```

## 📝 Implementation Checklist

- [ ] Fix malformed RST in existing templates
- [ ] Replace minimal index.rst with enhanced version
- [ ] Update agent_class.rst template
- [ ] Create tool documentation templates
- [ ] Add guide/tutorial templates
- [ ] Configure CSS customizations
- [ ] Test all major extensions
- [ ] Create example content for each template
- [ ] Document template usage for team

---

**Next Steps**: Start with fixing the existing templates, then progressively add enhanced versions using the available extensions!
