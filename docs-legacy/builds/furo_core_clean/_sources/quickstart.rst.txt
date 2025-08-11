Quick Start
===========

Get started with Haive in just a few minutes! This guide will walk you through installation, creating your first agent, and understanding the core concepts.

Installation
------------

Install Haive using pip:

.. code-block:: bash

   pip install haive

Or install with all optional dependencies:

.. code-block:: bash

   pip install "haive[all]"

For development installation:

.. code-block:: bash

   git clone https://github.com/haive-ai/haive.git
   cd haive
   poetry install

Your First Agent
----------------

Let's create a simple conversational agent:

.. code-block:: python

   from haive.agents.simple import SimpleAgent
   from haive.core.engine.aug_llm import AugLLMConfig

   # Create an LLM configuration
   config = AugLLMConfig(
       temperature=0.7,
       system_message="You are a helpful AI assistant."
   )

   # Create a simple agent
   agent = SimpleAgent(
       name="my_assistant",
       engine=config
   )

   # Run the agent
   response = agent.run("Hello! What can you help me with?")
   print(response)

Using Async Operations
~~~~~~~~~~~~~~~~~~~~~~

For better performance, use async operations:

.. code-block:: python

   import asyncio
   
   async def chat_with_agent():
       response = await agent.arun("Tell me about AI agents")
       print(response)
   
   # Run the async function
   asyncio.run(chat_with_agent())

Agent with Tools
----------------

Create an agent that can use tools:

.. code-block:: python

   from haive.agents.react import ReactAgent
   from langchain_core.tools import tool

   # Define a simple tool
   @tool
   def calculator(expression: str) -> str:
       """Calculate mathematical expressions."""
       try:
           result = eval(expression)
           return f"The result is: {result}"
       except Exception as e:
           return f"Error: {str(e)}"

   # Create a ReAct agent with tools
   agent = ReactAgent(
       name="math_assistant",
       engine=AugLLMConfig(),
       tools=[calculator]
   )

   # Use the agent
   response = agent.run("What is 15 * 23 + 42?")
   print(response)

Structured Output
-----------------

Use Pydantic models for structured output:

.. code-block:: python

   from pydantic import BaseModel, Field
   from typing import List

   class TaskPlan(BaseModel):
       """Structured task plan."""
       goal: str = Field(description="Main goal")
       steps: List[str] = Field(description="Steps to achieve goal")
       priority: int = Field(ge=1, le=5, description="Priority level")

   # Create agent with structured output
   agent = SimpleAgent(
       name="planner",
       engine=AugLLMConfig(
           structured_output_model=TaskPlan
       )
   )

   # Get structured response
   plan = agent.run("Plan how to learn Python programming")
   print(f"Goal: {plan.goal}")
   print(f"Steps: {plan.steps}")

Multi-Agent Systems
-------------------

Coordinate multiple agents:

.. code-block:: python

   from haive.agents.multi import MultiAgent

   # Create specialized agents
   researcher = ReactAgent(
       name="researcher",
       engine=AugLLMConfig(),
       tools=[web_search_tool]
   )

   writer = SimpleAgent(
       name="writer",
       engine=AugLLMConfig(
           system_message="You are a professional writer."
       )
   )

   # Create multi-agent system
   team = MultiAgent(
       agents=[researcher, writer],
       execution_mode="sequential"
   )

   # Execute multi-agent workflow
   result = team.run("Research quantum computing and write a summary")

Memory and State
----------------

Add memory to your agents:

.. code-block:: python

   from haive.core.memory import ConversationBufferMemory

   # Create agent with memory
   agent = SimpleAgent(
       name="memory_agent",
       engine=AugLLMConfig(),
       memory=ConversationBufferMemory(
           memory_key="chat_history",
           return_messages=True
       )
   )

   # Conversations are remembered
   agent.run("My name is Alice")
   response = agent.run("What's my name?")  # Will remember "Alice"

Common Patterns
---------------

Error Handling
~~~~~~~~~~~~~~

.. code-block:: python

   try:
       response = agent.run(user_input)
   except Exception as e:
       print(f"Error: {e}")

Streaming Responses
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   async for chunk in agent.astream(user_input):
       print(chunk, end="", flush=True)

State Management
~~~~~~~~~~~~~~~~

.. code-block:: python

   # Access agent state
   state = agent.get_state()
   
   # Update state
   agent.update_state({"custom_field": "value"})

Agent Configuration
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Detailed configuration
   agent = SimpleAgent(
       name="configured_agent",
       engine=AugLLMConfig(
           model="gpt-4",
           temperature=0.3,
           max_tokens=1000,
           timeout=30.0,
           retry_count=3
       )
   )

Next Steps
----------

Now that you have the basics:

1. **Explore Agent Types**: Check out :doc:`agents/index` for different agent patterns
2. **Learn About Tools**: Read :doc:`tools/index` to add capabilities
3. **Understand Architecture**: See :doc:`concepts` for design principles
4. **Build Complex Workflows**: Study :doc:`workflows/index` for advanced patterns

Example Projects
----------------

Check out these example projects:

- **Chatbot**: Simple conversational assistant
- **Research Assistant**: Multi-agent research system
- **Code Analyzer**: Development helper with tools
- **Game Player**: AI agents for games

Resources
---------

- :doc:`api/index` - Complete API reference
- :doc:`examples/index` - More code examples
- `GitHub Repository <https://github.com/haive-ai/haive>`_ - Source code
- `Discord Community <https://discord.gg/haive>`_ - Get help and share