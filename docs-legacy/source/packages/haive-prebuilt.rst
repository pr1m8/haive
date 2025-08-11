haive-prebuilt
==============

Ready-to-use agent templates and workflows for common tasks.

Overview
--------

The ``haive-prebuilt`` package provides a collection of pre-configured agents for common use cases:

- **Content Creation** - Blog writing, summarization, tagging
- **Research Agents** - Academic research, company analysis, web search
- **Business Tools** - Project management, sales analysis, startup tools
- **Specialized Agents** - Contract analysis, scientific papers, weather monitoring
- **Query Processing** - Query enhancement, SQL generation, intent detection
- **Creative Tools** - Podcast generation, GIF creation, meme generation

Installation
------------

.. code-block:: bash

   pip install haive-prebuilt

Or as part of the full framework:

.. code-block:: bash

   pip install haive

Quick Start
-----------

.. code-block:: python

   from haive.prebuilt.search_and_summarize.agent import SearchAndSummarizeAgent
   from haive.core.engine.aug_llm import AugLLMConfig
   
   # Create pre-built agent
   agent = SearchAndSummarizeAgent(
       name="researcher",
       engine=AugLLMConfig()
   )
   
   # Use the agent
   result = await agent.arun("Latest developments in quantum computing")

Agent Categories
----------------

Content & Research
^^^^^^^^^^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: Search & Summarize
      :link: ../api/prebuilt/search_and_summarize/index
      :link-type: doc

      Web search with summaries
      
      - Multi-source search
      - Content extraction
      - Summarization
      - Citation tracking

   .. grid-item-card:: Scientific Paper Agent
      :link: ../api/prebuilt/scientific_paper_agent/index
      :link-type: doc

      Academic paper analysis
      
      - Paper parsing
      - Method extraction
      - Results analysis
      - Literature review

Business & Analytics
^^^^^^^^^^^^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: Company Researcher
      :link: ../api/prebuilt/company_researcher/index
      :link-type: doc

      Company analysis
      
      - Financial data
      - Market position
      - Competitor analysis
      - News tracking

   .. grid-item-card:: Project Manager
      :link: ../api/prebuilt/project_manager/index
      :link-type: doc

      Project coordination
      
      - Task planning
      - Resource allocation
      - Timeline management
      - Progress tracking

Specialized Tools
^^^^^^^^^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: Contract Analysis
      :link: ../api/prebuilt/contract_analysis/index
      :link-type: doc

      Legal document review
      
      - Clause extraction
      - Risk identification
      - Compliance check
      - Summary generation

   .. grid-item-card:: Weather Disaster Management
      :link: ../api/prebuilt/weather_disaster_management/index
      :link-type: doc

      Disaster response
      
      - Weather monitoring
      - Alert generation
      - Resource planning
      - Emergency response

Creative Agents
^^^^^^^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: Podcast Generator
      :link: ../api/prebuilt/podcast_generator/index
      :link-type: doc

      Podcast creation
      
      - Script writing
      - Interview simulation
      - Audio generation
      - Show notes

   .. grid-item-card:: AI Insight
      :link: ../api/prebuilt/ai_insight/index
      :link-type: doc

      AI trend analysis
      
      - Technology tracking
      - Insight generation
      - Future predictions
      - Impact analysis

Core Pre-built Agents
---------------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.prebuilt.search_and_summarize.agent.SearchAndSummarizeAgent
   haive.prebuilt.scientific_paper_agent.agent.ScientificPaperAgent
   haive.prebuilt.company_researcher.agent.CompanyResearcherAgent
   haive.prebuilt.project_manager.agent.ProjectManagerAgent

Content Creation Agents
-----------------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.prebuilt.content.summarizer.Summarizer
   haive.prebuilt.content.tagger.Tagger
   haive.prebuilt.content.document_extractor.DocumentExtractor
   haive.prebuilt.content.qa_gen.QAGenerator

Research & Analysis Agents
--------------------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.prebuilt.open_researcher.OpenResearcherAgent
   haive.prebuilt.people_researcher.PeopleResearcherAgent
   haive.prebuilt.arxiv_agent.ArxivAgent
   haive.prebuilt.github_agent.GitHubAgent

Business & Productivity Agents
------------------------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.prebuilt.startup.agent.StartupAgent
   haive.prebuilt.sales_call_analyzer.SalesCallAnalyzer
   haive.prebuilt.contract_analysis.agent.ContractAnalysisAgent
   haive.prebuilt.taskifier.agent.TaskifierAgent

Query Processing Tools
----------------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.prebuilt.query.query_enhance.QueryEnhancer
   haive.prebuilt.query.query_decomposer.QueryDecomposer
   haive.prebuilt.query.query_to_sql.QueryToSQL
   haive.prebuilt.query.query_intent.QueryIntentClassifier

Utility Functions
-----------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/function.rst

   haive.prebuilt.reflection.create_reflection_agent
   haive.prebuilt.general.planner.create_planner

Complete API Reference
----------------------

For the complete API documentation with all pre-built agents:

.. toctree::
   :maxdepth: 3

   ../api/prebuilt/index

Examples
--------

Web Search & Summarization
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.prebuilt.search_and_summarize.agent import SearchAndSummarizeAgent
   
   agent = SearchAndSummarizeAgent(
       name="web_researcher",
       engine=AugLLMConfig(temperature=0.3)
   )
   
   # Search and summarize
   result = await agent.arun(
       "What are the latest breakthroughs in renewable energy?"
   )
   
   print(result.summary)
   print(f"Sources: {result.sources}")

Company Research
^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.prebuilt.company_researcher.agent import CompanyResearcherAgent
   
   agent = CompanyResearcherAgent(
       name="company_analyst",
       engine=AugLLMConfig()
   )
   
   # Analyze a company
   analysis = await agent.arun({
       "company": "Tesla",
       "aspects": ["financials", "competition", "innovation"]
   })

Scientific Paper Analysis
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.prebuilt.scientific_paper_agent.agent import ScientificPaperAgent
   
   agent = ScientificPaperAgent(
       name="paper_analyzer",
       engine=AugLLMConfig()
   )
   
   # Analyze paper
   analysis = await agent.arun({
       "paper_url": "https://arxiv.org/abs/2301.00234",
       "focus": ["methodology", "results", "limitations"]
   })

Contract Review
^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.prebuilt.contract_analysis.agent import ContractAnalysisAgent
   
   agent = ContractAnalysisAgent(
       name="legal_reviewer",
       engine=AugLLMConfig(temperature=0.1)
   )
   
   # Review contract
   review = await agent.arun({
       "contract_text": contract_content,
       "check_for": ["liability", "termination", "payment_terms"]
   })

Podcast Generation
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.prebuilt.podcast_generator.agent import PodcastGeneratorAgent
   
   agent = PodcastGeneratorAgent(
       name="podcast_creator",
       engine=AugLLMConfig(temperature=0.8)
   )
   
   # Generate podcast episode
   episode = await agent.arun({
       "topic": "The Future of AI",
       "guest": "AI Researcher",
       "duration": "30 minutes"
   })

Query Enhancement
^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.prebuilt.query.query_enhance import QueryEnhancer
   from haive.prebuilt.query.query_to_sql import QueryToSQL
   
   # Enhance user query
   enhancer = QueryEnhancer()
   enhanced = await enhancer.enhance("show sales last month")
   
   # Convert to SQL
   sql_gen = QueryToSQL(schema=database_schema)
   sql_query = await sql_gen.convert(enhanced)

Best Practices
--------------

1. **Choose the right agent** for your specific use case
2. **Configure appropriately** - adjust temperature and parameters
3. **Provide clear inputs** - structured inputs work best
4. **Handle outputs properly** - each agent has specific output format
5. **Combine agents** for complex workflows
6. **Monitor performance** - some agents make multiple API calls

Agent Configuration
-------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Configuration
     - Description
   * - **Engine Settings**
     - Adjust temperature, max_tokens based on task
   * - **Tool Selection**
     - Enable/disable specific tools per agent
   * - **Output Format**
     - Configure structured output models
   * - **Retry Logic**
     - Set retry attempts for reliability
   * - **Caching**
     - Enable result caching for efficiency

Creating Custom Pre-built Agents
--------------------------------

.. code-block:: python

   from haive.agents.base.agent import Agent
   from haive.prebuilt.base import PrebuiltMixin
   
   class MyPrebuiltAgent(PrebuiltMixin, Agent):
       """Custom pre-built agent."""
       
       # Pre-configured settings
       default_engine_config = {
           "temperature": 0.5,
           "system_message": "You are a specialized assistant."
       }
       
       # Pre-defined tools
       default_tools = ["web_search", "calculator"]
       
       # Custom workflow
       async def run_workflow(self, input_data):
           # Implement specialized workflow
           pass

Related Documentation
---------------------

- :doc:`../guide/prebuilt` - Pre-built agents guide
- :doc:`../api/prebuilt/index` - Complete pre-built API reference
- :doc:`haive-agents` - Base agent framework
- :doc:`../examples/prebuilt` - Pre-built agent examples