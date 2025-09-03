haive-agents
============

Pre-built agent implementations for the Haive framework.

Overview
--------

The ``haive-agents`` package provides a comprehensive collection of ready-to-use AI agents:

- **Simple Agents** - Basic conversational agents with templates
- **ReAct Agents** - Reasoning and action agents with tool use
- **RAG Agents** - Retrieval-augmented generation for knowledge tasks
- **Multi-Agent Systems** - Orchestration of multiple agents
- **Specialized Agents** - Planning, research, memory, and more

Installation
------------

.. code-block:: bash

   pip install haive-agents

Or as part of the full framework:

.. code-block:: bash

   pip install haive

Quick Start
-----------

.. code-block:: python

   from haive.agents.simple.agent import SimpleAgent
   from haive.agents.react.agent import ReactAgent
   from haive.core.engine.aug_llm import AugLLMConfig
   
   # Simple conversational agent
   simple = SimpleAgent(
       name="assistant",
       engine=AugLLMConfig()
   )
   
   # ReAct agent with tools
   react = ReactAgent(
       name="researcher", 
       engine=AugLLMConfig(),
       tools=["web_search", "calculator"]
   )

Agent Categories
----------------

Core Agents
^^^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: SimpleAgent
      :link: ../api/agents/simple/agent/index
      :link-type: doc

      Basic conversational agent
      
      - Prompt templates
      - Stateful conversations
      - Memory support
      - Async operations

   .. grid-item-card:: ReactAgent
      :link: ../api/agents/react/agent/index
      :link-type: doc

      Reasoning and action agent
      
      - Tool integration
      - Chain of thought
      - Error recovery
      - Multi-step planning

RAG Agents
^^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: BaseRAGAgent
      :link: ../api/agents/rag/base/agent/index
      :link-type: doc

      RAG foundation
      
      - Vector stores
      - Retrieval strategies
      - Context injection
      - Reranking

   .. grid-item-card:: SimpleRAGAgent
      :link: ../api/agents/rag/simple/agent/index
      :link-type: doc

      Easy RAG setup
      
      - Quick configuration
      - Default embeddings
      - Answer generation
      - Source citations

Multi-Agent Systems
^^^^^^^^^^^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: MultiAgent
      :link: ../api/agents/multi/agent/index
      :link-type: doc

      Agent orchestration
      
      - Sequential execution
      - Parallel coordination
      - State sharing
      - Result aggregation

   .. grid-item-card:: SupervisorAgent
      :link: ../api/agents/supervisor/agent/index
      :link-type: doc

      Hierarchical control
      
      - Task delegation
      - Team management
      - Progress monitoring
      - Dynamic routing

Specialized Agents
^^^^^^^^^^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: PlannerAgent
      :link: ../api/agents/planning/planner/agent/index
      :link-type: doc

      Strategic planning
      
      - Goal decomposition
      - Step generation
      - Plan validation
      - Adaptive replanning

   .. grid-item-card:: ResearchAgent
      :link: ../api/agents/research/agent/index
      :link-type: doc

      Research automation
      
      - Web research
      - Source evaluation
      - Report generation
      - Citation management

Core Agent Classes
------------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.agents.simple.agent.SimpleAgent
   haive.agents.simple.agent_v3.SimpleAgentV3
   haive.agents.react.agent.ReactAgent
   haive.agents.base.agent.Agent
   haive.agents.base.enhanced_agent.Agent

RAG Agents
----------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.agents.rag.base.agent.BaseRAGAgent
   haive.agents.rag.simple.agent.SimpleRAGAgent
   haive.agents.rag.simple.answer_agent.AnswerAgent
   haive.agents.rag.collective_rag_agent_v4.CollectiveRAGAgentV4

Multi-Agent Systems
-------------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.agents.multi.agent.MultiAgent
   haive.agents.multi.enhanced_multi_agent_v4.EnhancedMultiAgentV4
   haive.agents.supervisor.agent.SupervisorAgent
   haive.agents.supervisor.agent_v2.SupervisorAgentV2

Planning & Research Agents
--------------------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.agents.planning.planner.agent.PlannerAgent
   haive.agents.planning.adaptive.agent.AdaptivePlanningAgent
   haive.agents.research.agent.ResearchAgent
   haive.agents.research.open_perplexity.agent.OpenPerplexityAgent

Memory Agents
-------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.agents.memory.agent.MemoryAgent
   haive.agents.memory_v2.agent.MemoryAgentV2
   haive.agents.memory_v2.react_memory_coordinator.ReactMemoryCoordinator
   haive.agents.memory_v2.graph_memory_agent.GraphMemoryAgent

Reasoning & Critique Agents
---------------------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.agents.reasoning_and_critique.self_discover.agent.SelfDiscoverAgent
   haive.agents.reasoning_and_critique.cot_agent.ChainOfThoughtAgent
   haive.agents.reasoning_and_critique.cot_agent_fixed.ChainOfThoughtAgent

Agent Patterns
--------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Pattern
     - Description
   * - **Simple → Structured**
     - Basic agent with structured output using Pydantic
   * - **React → Multi-Tool**
     - ReAct agent with multiple tools working together
   * - **RAG → QA System**
     - RAG agent for question answering over documents
   * - **Multi → Workflow**
     - Multiple agents in sequential/parallel workflows
   * - **Supervisor → Team**
     - Supervisor coordinating specialized agents

Complete API Reference
----------------------

For the complete API documentation with all agent implementations:

.. toctree::
   :maxdepth: 3

   ../api/agents/index

Examples
--------

Simple Agent with Memory
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.agents.simple.agent_v3 import SimpleAgentV3
   from haive.core.engine.aug_llm import AugLLMConfig
   
   agent = SimpleAgentV3(
       name="chatbot",
       engine=AugLLMConfig(
           temperature=0.7,
           system_message="You are a helpful assistant"
       )
   )
   
   # Conversation with memory
   response1 = await agent.arun("My name is Alice")
   response2 = await agent.arun("What's my name?")  # Remembers context

ReAct Agent with Tools
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.agents.react.agent import ReactAgent
   from langchain_core.tools import tool
   
   @tool
   def calculator(expression: str) -> str:
       """Calculate mathematical expressions."""
       return str(eval(expression))
   
   agent = ReactAgent(
       name="math_assistant",
       engine=AugLLMConfig(),
       tools=[calculator]
   )
   
   result = await agent.arun("What is 25 * 17 + 93?")

Multi-Agent Workflow
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4
   
   # Create workflow: Planner → Researcher → Writer
   workflow = EnhancedMultiAgentV4(
       agents=[
           PlannerAgent(name="planner"),
           ResearchAgent(name="researcher"),
           WriterAgent(name="writer")
       ],
       execution_mode="sequential"
   )
   
   result = await workflow.arun("Create a report on AI trends")

RAG Question Answering
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.agents.rag.simple.agent import SimpleRAGAgent
   
   # Create RAG agent with default vector store
   rag_agent = SimpleRAGAgent(
       name="qa_bot",
       engine=AugLLMConfig()
   )
   
   # Add documents
   await rag_agent.add_documents([
       "Python is a programming language.",
       "It was created by Guido van Rossum."
   ])
   
   # Query
   answer = await rag_agent.arun("Who created Python?")

Best Practices
--------------

1. **Choose the right agent** for your use case
2. **Start simple** with SimpleAgent, add complexity as needed
3. **Use async methods** (arun) for better performance
4. **Configure engines** appropriately for your task
5. **Test with real LLMs**, avoid mocks
6. **Compose agents** for complex workflows

Agent Selection Guide
---------------------

.. list-table::
   :widths: 40 60
   :header-rows: 1

   * - Use Case
     - Recommended Agent
   * - Basic chat/conversation
     - SimpleAgent or SimpleAgentV3
   * - Tool use and reasoning
     - ReactAgent
   * - Document Q&A
     - SimpleRAGAgent or BaseRAGAgent
   * - Complex workflows
     - EnhancedMultiAgentV4
   * - Task delegation
     - SupervisorAgent
   * - Research tasks
     - ResearchAgent
   * - Planning and strategy
     - PlannerAgent

Related Documentation
---------------------

- :doc:`../showcase` - Interactive agent showcase
- :doc:`../guide/agents` - Agent development guide
- :doc:`../api/agents/index` - Complete agents API reference
- :doc:`haive-tools` - Tools for agent capabilities