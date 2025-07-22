📚 Examples and Tutorials
=========================

Comprehensive examples showcasing Haive's capabilities across all packages.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: 🤖 Agent Examples
      :shadow: lg
      
      **Simple & ReactAgent tutorials**
      
      Learn to create conversational agents, structured output, and tool integration.
      
      +++
      
      ✓ Simple Agent Tutorial • ✓ ReactAgent with Tools • ✓ Structured Output

   .. grid-item-card:: 🎮 Game Examples
      :shadow: lg
      
      **AI Game Playing**
      
      Build AI agents that play games like Chess, Tic-Tac-Toe, and strategy games.
      
      +++
      
      ✓ Chess AI Agent • ✓ Tic-Tac-Toe Battle • ✓ Game Strategy

   .. grid-item-card:: 🔧 Tool Examples
      :shadow: lg
      
      **Tool Integration**
      
      Connect agents to APIs, databases, search engines, and external services.
      
      +++
      
      ✓ Web Search Tools • ✓ Database Tools • ✓ Custom Tools

   .. grid-item-card:: 🔌 MCP Examples
      :shadow: lg
      
      **Model Context Protocol**
      
      Integrate with external tools and services via MCP protocol.
      
      +++
      
      ✓ MCP Basic • ✓ MCP Advanced • ✓ MCP Custom

Getting Started
---------------

**Prerequisites**

.. code-block:: bash

   # Install Haive with examples
   poetry install --extras "agents tools games mcp"
   
   # Set up environment variables  
   export OPENAI_API_KEY="your-api-key"

**Run an Example**

.. code-block:: bash

   # Navigate to any example and run it
   cd packages/haive-agents/examples/
   poetry run python simple_agent_tutorial.py

Quick Start Code
----------------

**Basic Agent Example**

.. code-block:: python
   
   from haive.agents.simple import SimpleAgent
   from haive.core.engine.aug_llm import AugLLMConfig
   
   # Create agent
   config = AugLLMConfig(temperature=0.7)
   agent = SimpleAgent(name="assistant", engine=config)
   
   # Use agent
   result = await agent.arun("Hello, how can you help?")
   print(result)

**ReactAgent with Tools**

.. code-block:: python
   
   from haive.agents.react import ReactAgent
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
   
   result = await agent.arun("What is 15 * 23?")

Available Examples
------------------

**Agent Examples** (``packages/haive-agents/examples/``)

* ``simple_agent_tutorial.py`` - Basic agent with structured output
* ``react_agent_tutorial.py`` - Tool-enabled reasoning agent
* ``agent_with_structured_output.py`` - Advanced Pydantic integration
* ``memory_v2_example.py`` - Long-term memory patterns
* ``dynamic_supervisor_demo.py`` - Multi-agent coordination

**Game Examples** (``packages/haive-games/examples/``)

* ``tic_tac_toe_demo.py`` - AI vs AI Tic-Tac-Toe battle
* ``chess_agent_demo.py`` - Chess-playing agent  
* ``multi_game_tournament.py`` - Tournament between game AIs

**Tool & MCP Examples** (``packages/haive-tools/examples/``, ``packages/haive-mcp/examples/``)

* ``web_search_integration.py`` - Connect agent to web search
* ``database_agent.py`` - SQL database integration
* ``mcp_server_demo.py`` - Custom MCP server creation