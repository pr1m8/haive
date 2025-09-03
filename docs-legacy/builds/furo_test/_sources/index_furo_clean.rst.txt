Haive AI Agent Framework
========================

A production-ready AI agent framework for building sophisticated LLM-powered applications.

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: 🚀 Getting Started
      :link: quickstart
      :link-type: doc

      Quick installation and your first agent in 5 minutes

   .. grid-item-card:: 📖 User Guide
      :link: guide/index
      :link-type: doc

      Learn how to build agents and workflows

   .. grid-item-card:: 🎯 Examples
      :link: examples/index
      :link-type: doc

      Code examples and tutorials

   .. grid-item-card:: 📚 API Reference
      :link: api/haive/index
      :link-type: doc

      Complete API documentation

Overview
--------

Haive provides a modular, type-safe framework for creating AI agents that can:

- **🤖 Execute Complex Workflows** - Chain agents together for sophisticated tasks
- **🔧 Use Tools** - Integrate with APIs, databases, and external services
- **🧠 Maintain Memory** - Remember context across conversations
- **🔄 Handle State** - Manage complex state transitions
- **📊 Process Data** - Stream and transform data efficiently
- **🎮 Play Games** - Learn and interact through game environments

Key Features
------------

.. grid:: 3
   :gutter: 2

   .. grid-item::
      
      **Type Safety**
      
      Pydantic models throughout for reliable data handling

   .. grid-item::
      
      **Async First**
      
      Built for high-performance async operations

   .. grid-item::
      
      **Modular Design**
      
      Mix and match components as needed

   .. grid-item::
      
      **LLM Agnostic**
      
      Works with OpenAI, Anthropic, Google, and more

   .. grid-item::
      
      **Production Ready**
      
      Battle-tested in real applications

   .. grid-item::
      
      **Extensible**
      
      Easy to add custom agents and tools

Quick Example
-------------

.. code-block:: python

   from haive.agents.react import ReactAgent
   from haive.core.engine import AugLLMConfig
   from langchain_core.tools import tool

   @tool
   def calculator(expression: str) -> str:
       """Calculate mathematical expressions."""
       return str(eval(expression))

   # Create an agent with tools
   agent = ReactAgent(
       name="math_assistant",
       engine=AugLLMConfig(),
       tools=[calculator]
   )

   # Run the agent
   result = await agent.arun("What is 25 * 17 + 93?")
   print(result)  # "25 * 17 = 425, plus 93 equals 518"

API Documentation
-----------------

The Haive framework is organized into focused packages. Below is the API documentation for each package with proper ``haive.*`` namespacing:

.. toctree::
   :maxdepth: 3
   :caption: Package APIs
   :titlesonly:

   api/haive/index

Documentation Structure
-----------------------

.. toctree::
   :maxdepth: 2
   :caption: Learn
   :hidden:

   quickstart
   guide/index
   examples/index

.. toctree::
   :maxdepth: 2
   :caption: Reference
   :hidden:

   api/haive/index
   architecture/index
   changelog

.. toctree::
   :maxdepth: 2
   :caption: Development
   :hidden:

   contributing
   development/index
   testing

Indices and Search
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`