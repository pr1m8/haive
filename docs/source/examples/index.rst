Examples and Tutorials
======================

The Haive framework includes extensive examples distributed throughout the codebase. Each module contains its own example files demonstrating usage patterns.

Example Locations
-----------------

Examples are organized by package and module:

Agent Examples
~~~~~~~~~~~~~~

**Core Agent Types**

- **Simple Agents**: ``packages/haive-agents/src/haive/agents/simple/example.py``
- **ReAct Agents**: ``packages/haive-agents/src/haive/agents/react_class/react_agent2/example.py``
- **Multi-Agent Systems**: ``packages/haive-agents/src/haive/agents/multi/example.py``
- **Supervisor Agents**: ``packages/haive-agents/src/haive/agents/supervisor/example_*.py``

**Conversation Agents**

- **Collaborative**: ``packages/haive-agents/src/haive/agents/conversation/collaberative/example.py``
- **Debate**: ``packages/haive-agents/src/haive/agents/conversation/debate/example.py``
- **Directed**: ``packages/haive-agents/src/haive/agents/conversation/directed/example.py``
- **Round Robin**: ``packages/haive-agents/src/haive/agents/conversation/round_robin/example.py``
- **Social Media**: ``packages/haive-agents/src/haive/agents/conversation/social_media/example.py``

**RAG Agents**

- **Graph Database RAG**: ``packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/example.py``
- **SQL RAG**: ``packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/example.py``
- **LLM RAG**: ``packages/haive-agents/src/haive/agents/rag/llm_rag/example.py``

**Reasoning & Critique Agents**

- **LATS**: ``packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/example.py``
- **Logic**: ``packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/example.py``
- **MCTS**: ``packages/haive-agents/src/haive/agents/reasoning_and_critique/mcts/example.py``
- **Reflexion**: ``packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/example.py``
- **Self-Discover**: ``packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/example.py``
- **Tree of Thoughts**: ``packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/example.py``

**Planning Agents**

- **Plan & Execute**: ``packages/haive-agents/src/haive/agents/planning/p_and_e/example.py``

**Research Agents**

- **STORM**: ``packages/haive-agents/src/haive/agents/research/storm/example.py``

Game Examples
~~~~~~~~~~~~~

Each game includes example implementations:

- **Chess**: ``packages/haive-games/src/haive/games/chess/example.py``
- **Connect4**: ``packages/haive-games/src/haive/games/connect4/example.py``
- **Tic Tac Toe**: ``packages/haive-games/src/haive/games/tic_tac_toe/example.py``
- **Poker**: ``packages/haive-games/src/haive/games/holdem/example.py``
- **Among Us**: ``packages/haive-games/src/haive/games/mafia/example.py``
- **Monopoly**: ``packages/haive-games/src/haive/games/monopoly/example.py``

Core Examples
~~~~~~~~~~~~~

- **Logging**: ``packages/haive-core/examples/logging_demo.py``
- **Meta Agent**: ``packages/haive-core/examples/meta_agent_example.py``
- **State Schema**: ``packages/haive-core/examples/state_schema_integration.py``
- **Graph Visualization**: ``packages/haive-core/src/haive/core/graph/state_graph/visualization/examples.py``

MCP Examples
~~~~~~~~~~~~

- **MCP Integration**: ``packages/haive-mcp/examples/mcp_example.py``
- **Dataflow**: ``packages/haive-mcp/examples/dataflow_example.py``

Running Examples
----------------

To run any example:

.. code-block:: bash

    # Navigate to the haive backend directory
    cd /home/will/Projects/haive/backend/haive

    # Run with poetry
    poetry run python packages/haive-agents/src/haive/agents/simple/example.py

    # Or activate the virtual environment
    poetry shell
    python packages/haive-agents/src/haive/agents/simple/example.py

Example Collections
-------------------

The main example directories contain additional demos:

1. **Agent Examples**: ``packages/haive-agents/examples/``
   
   - Supervisor demos
   - Multi-agent systems
   - Token tracking
   - Output adapters
   - Performance benchmarks

2. **Game Examples**: ``packages/haive-games/examples/``
   
   - Chess API demo
   - Connect4 gameplay
   - Configurable agents
   - Tournament systems

3. **Core Examples**: ``packages/haive-core/examples/``
   
   - Logging configurations
   - State management
   - Schema integration

Quick Start Examples
--------------------

Simple Agent
~~~~~~~~~~~~

.. code-block:: python

    from haive.agents.simple import SimpleAgent

    agent = SimpleAgent(name="assistant")
    response = await agent.arun("Hello, how can you help me?")
    print(response)

ReAct Agent with Tools
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from haive.agents.react import ReactAgent
    from haive.tools import WebSearchTool, CalculatorTool

    agent = ReactAgent(
    name="researcher",
    tools=[WebSearchTool(), CalculatorTool()]
    )

    result = await agent.arun("What's the population of Tokyo?")

Multi-Agent Conversation
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from haive.agents.conversation.debate import DebateConversation

    debate = DebateConversation.create_simple_debate(
    topic="Is AI beneficial for humanity?",
    position_a=("Alice", "Pro-AI"),
    position_b=("Bob", "AI-Skeptic")
    )

    result = await debate.arun()

See Also
--------

- :doc:`/agents/gallery` - Agent gallery with interactive examples
- :doc:`/guides/index` - Step-by-step guides
- :doc:`/api/haive/index` - Complete API reference