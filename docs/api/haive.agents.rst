haive.agents
============

.. module:: haive.agents

.. image:: /_static/module_icons/agents.svg
   :align: right
   :width: 100px

Module Overview
--------------

The ``haive.agents`` package provides advanced agent capabilities for creating, managing, and deploying 
intelligent agents across various domains including games, database interactions, and computational tasks.

Subpackages
----------

.. grid:: 1 2 2 3
    :gutter: 3
    
    .. grid-item-card:: Agent Games
        :link: haive.agents.agent_games
        :link-type: doc
        :img-top: /_static/module_icons/agent_games.svg
        
        Game-playing agents for Chess, Go, Checkers and more.

    .. grid-item-card:: Graph Database
        :link: haive.agents.graph_db
        :link-type: doc
        :img-top: /_static/module_icons/graph_db.svg
        
        Database interaction agents with Cypher query generation.

    .. grid-item-card:: LATS
        :link: haive.agents.lats
        :link-type: doc
        :img-top: /_static/module_icons/lats.svg
        
        Language Agent Task System implementation.

    .. grid-item-card:: LLM Compiler
        :link: haive.agents.llm_compiler
        :link-type: doc
        :img-top: /_static/module_icons/llm_compiler.svg
        
        Advanced LLM compilation and task scheduling.

Key Features
-----------

* **Multi-domain Agent Support**: Agents specialized for games, databases, and computational tasks
* **Modular Architecture**: Consistent interfaces across different agent types
* **State Management**: Sophisticated state tracking and management
* **LLM Augmentation**: Enhanced language model capabilities through specialized interfaces

Getting Started
-------------

.. code-block:: python
   :linenos:
   
   from haive.agents import create_agent
   
   # Create an agent for a specific purpose
   chess_agent = create_agent("chess")
   
   # Configure the agent
   chess_agent.configure(skill_level="advanced")
   
   # Run the agent with a specific task
   result = chess_agent.run(initial_state="e4")

API Reference
-----------

.. toctree::
   :maxdepth: 1
   
   agents/agent_games
   agents/graph_db
   agents/lats
   agents/llm_compiler