Enhanced Documentation Features Demo
====================================

This page demonstrates the enhanced documentation features available with our 86+ Sphinx extensions.

.. container:: hero-banner

   :name: feature-demo-hero

   🎨 Enhanced Documentation Showcase
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   Demonstrating advanced features using 86+ Sphinx extensions including Pydantic models, 
   interactive components, diagrams, and enhanced UI elements.

🚀 Interactive Components
=========================

Enhanced Tabs with Sphinx-Design
---------------------------------

.. tab-set::

   .. tab-item:: 🤖 Agent Examples

      :sync: agents

.. code-block:: python

         :caption: Enhanced SimpleAgent with Pydantic Configuration
         :linenos:
         :emphasize-lines: 4-10
         :class:`copy`-button

         from haive.agents import SimpleAgent
         from haive.core.engine import AugLLMConfig
         from pydantic import BaseModel, Field

         class AgentConfig(BaseModel):
             """Enhanced agent configuration with Pydantic validation."""
             temperature: float = Field(ge=0.0, le=2.0, description="Sampling temperature")
             max_tokens: int = Field(ge=1, le=4000, description="Maximum response tokens")
             system_message: str = Field(min_length=1, description="System prompt")

         config = AugLLMConfig(
             model="gpt-4",
             temperature=0.7,
             system_message="You are a helpful AI assistant."
         )

         agent = SimpleAgent(name="demo_agent", engine=config)
         result = await agent.arun("Hello!")

         .. tab-item:: 🔧 Pydantic Models

         :sync: pydantic

         .. autopydantic_model:: haive.core.engine.aug_llm.AugLLMConfig
         :model-show-config-member: true
         :model-show-field-summary: true
         :field-show-constraints: true
         :field-show-default: true

         .. tab-item:: 📊 Diagrams

         :sync: diagrams

         .. mermaid::
         :caption: Agent Architecture Flow

         graph TD
             A[User Input] --> B[SimpleAgent]
             B --> C[AugLLMConfig]
             C --> D[LLM Provider]
             D --> E[Response Processing]
             E --> F[State Management]
             F --> G[User Output]

         Enhanced Grid Layout
         --------------------

         .. grid:: 1 2 3 3

         :gutter: 3
         :class-container: feature-demo-grid

         .. grid-item-card:: 🧠 AI Agents

         :class-header: demo-card-header
         :shadow: lg
      
         Advanced agent types with Pydantic validation and enhanced documentation.
      
         * SimpleAgent with config validation*
         * ReactAgent with tool integration  *
         * Multi-agent coordination*
         * State management and persistence*

         .. grid-item-card:: 📋 Enhanced Models

         :class-header: demo-card-header
         :shadow: lg
      
         Pydantic models with comprehensive documentation and validation.
      
         * Field constraints and validation*
         * Type hints and descriptions*
         * Configuration summaries*
         * Validator documentation*

         .. grid-item-card:: 🎨 UI Components

         :class-header: demo-card-header
         :shadow: lg
      
         Rich UI components using sphinx-design and other extensions.
      
         * Interactive tabs and dropdowns*
         * Enhanced code blocks with copy*
         * Responsive grid layouts*
         * Beautiful admonitions*

         🔍 Enhanced Admonitions
         =======================

         .. admonition:: 💡 Pro Tip

         :class:`tip`

         The enhanced documentation system automatically detects Pydantic models and applies 
         specialized formatting for better readability and developer experience.

         .. admonition:: ⚠️ Important

         :class:`warning`

         When using the enhanced templates, make sure your Pydantic models have comprehensive 
         docstrings for the best documentation experience.

         .. admonition:: 📚 More Information

         :class:`note`

         All 86 Sphinx extensions work together to provide a comprehensive documentation 
         experience with automatic cross-references, enhanced search, and beautiful styling.

         🎯 Dropdown Components
         ======================

         .. dropdown:: 🔍 Advanced Configuration Options

         :color: primary
         :icon: gear

.. code-block:: python

      :caption: Advanced AugLLMConfig with all options
      :class:`copy`-button

      from haive.core.engine import AugLLMConfig
      from pydantic import Field

      config = AugLLMConfig(
          # Model selection
          model="gpt-4-turbo",
          provider="openai",
          
          # Generation parameters
          temperature=0.7,
          max_tokens=2000,
          top_p=0.9,
          frequency_penalty=0.1,
          presence_penalty=0.1,
          
          # System configuration
          system_message="You are an expert AI assistant.",
          max_retries=3,
          timeout=30.0,
          
          # Structured output
          structured_output_model=MyResponseModel,
          
          # Advanced features
          tools=["web_search", "calculator"],
          memory_enabled=True,
          state_persistence=True
      )

      .. dropdown:: 📊 Extension Statistics

      :color: info
      :icon: chart-bar

      Our enhanced documentation system includes:

      .. list-table:: Extension Categories

      :header-rows: 1
      :widths: 30 20 50

      * - Category*
        - Count
        - Key Features
      * - Core Sphinx*
        - 14
        - autodoc, autosummary, intersphinx, napoleon
      * - UI/UX Extensions*
        - 29
        - sphinx-design, copybutton, tabs, toggles
      * - API Documentation*
        - 11
        - autodoc-pydantic, autodocsumm, openapi
      * - Diagrams & Charts*
        - 8
        - mermaid, plantuml, inheritance diagrams
      * - Enhanced Features*
        - 24
        - search improvements, SEO, versioning

      📈 Interactive Examples
      =======================

      Inheritance Diagram Example
      ----------------------------

      .. inheritance-diagram:: haive.agents.simple.agent.SimpleAgent haive.agents.react.agent.ReactAgent

      :parts: 2
      :caption: Agent Class Hierarchy

      Code Block with Enhanced Copy Button
      -------------------------------------

.. code-block:: python

   :caption: Multi-Agent Coordination Example
   :linenos:
   :emphasize-lines: 8-12
   :class:`copy`-button

   from haive.agents import MultiAgent, SimpleAgent, ReactAgent
   from haive.tools import WebSearchTool

   # Create specialized agents
   researcher = ReactAgent(

       name="researcher", 
       tools=[WebSearchTool()]

   )
   writer = SimpleAgent(name="writer")

   # Coordinate with MultiAgent
   team = MultiAgent(

       name="content_team",
       agents=[researcher, writer],
       execution_mode="sequential"

   )

   # Execute workflow
   result = await team.arun("Research AI trends and write a summary")
   print(result)

   🎨 Styling Features
   ===================

   Custom Styling Elements
   -----------------------

   .. container:: highlight-box

   **Enhanced Styling**: This documentation uses custom CSS that integrates with 
   all 86+ Sphinx extensions to provide a cohesive and beautiful experience.

   .. container:: metrics-showcase

   .. grid:: 1 2 4 4

      :gutter: 2

      .. grid-item::
         :class:`metric`-display
         
         **86**
         
         *Total Extensions*

      .. grid-item::
         :class:`metric`-display
         
         **100%**
         
         *Compatibility*

      .. grid-item::
         :class:`metric`-display
         
         **0**
         
         *Failed Extensions*

      .. grid-item::
         :class:`metric`-display
         
         **6**
         
         *New Templates*

   🔗 Cross-References and Links
   =============================

   Enhanced Intersphinx Integration
   ---------------------------------

   With our comprehensive intersphinx configuration, you can easily reference:

   * :class:`pydantic.BaseModel` - Pydantic base model documentation*
   * :func:`langchain.tools.tool` - LangChain tool decorator*
   * :class:`haive.agents.simple.agent.SimpleAgent` - Our SimpleAgent class*
   * :doc:`/api/index` - Complete API reference*

   Search and Navigation
   ---------------------

   The enhanced search functionality includes:

   - Full-text search across all documentation
   - API-specific search with type information  
   - Cross-package search with namespace handling
   - Enhanced result ranking and context

   📱 Responsive Design
   ====================

   The documentation is fully responsive and works beautifully on:

   * 📱 Mobile devices (phones and tablets)*
   * 💻 Desktop computers and laptops  *
   * 🖥️ Large screens and ultra-wide displays*
   * 🌙 Dark mode and light mode themes*

   All interactive components adapt seamlessly to different screen sizes while 
   maintaining full functionality and beautiful styling.
