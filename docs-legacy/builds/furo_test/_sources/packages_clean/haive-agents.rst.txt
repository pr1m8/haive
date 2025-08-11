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
      :link: ../api/haive/agents/simple/agent/index
      :link-type: doc

      Basic conversational agent
      
      - Prompt templates
      - Stateful conversations
      - Memory support
      - Async operations

   .. grid-item-card:: ReactAgent
      :link: ../api/haive/agents/react/agent/index
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
      :link: ../api/haive/agents/rag/base/agent/index
      :link-type: doc

      RAG foundation
      
      - Vector stores
      - Retrieval strategies
      - Context injection
      - Reranking

   .. grid-item-card:: SimpleRAGAgent
      :link: ../api/haive/agents/rag/simple/agent/index
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
      :link: ../api/haive/agents/multi/agent/index
      :link-type: doc

      Agent orchestration
      
      - Sequential execution
      - Parallel coordination
      - State sharing
      - Result aggregation

   .. grid-item-card:: SupervisorAgent
      :link: ../api/haive/agents/supervisor/agent/index
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
      :link: ../api/haive/agents/planning/planner/agent/index
      :link-type: doc

      Strategic planning
      
      - Goal decomposition
      - Step generation
      - Plan validation
      - Adaptive replanning

   .. grid-item-card:: ResearchAgent
      :link: ../api/haive/agents/research/agent/index
      :link-type: doc

      Research automation
      
      - Web research
      - Source evaluation
      - Report generation
      - Citation management

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

   ../api/haive/agents/index

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
- :doc:`../api/haive/agents/index` - Complete agents API reference
- :doc:`haive-tools` - Tools for agent capabilities