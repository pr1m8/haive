haive.agents
===============

.. module:: haive.agents

.. image:: /_static/module_icons/agents.svg
   :align: right
   :width: 100px

Module Description
----------------

This module provides agent functionality for [brief description of what the agents module does].

Key Components
------------

* :class:`Agent` - Primary class for agent behavior
* :class:`AgentManager` - Manages multiple agents
* :func:`create_agent` - Factory function to create new agents

Examples
-------

Basic Usage
~~~~~~~~~~

.. code-block:: python
   :linenos:
   
   from haive.agents import Agent
   
   # Create an agent
   agent = Agent(name='my_agent')
   
   # Run the agent
   result = agent.run(task='process data')
   
Advanced Usage
~~~~~~~~~~~~~

.. code-block:: python
   :linenos:
   
   from haive.agents import Agent, AgentManager
   
   # Create multiple agents
   agent1 = Agent(name='agent1')
   agent2 = Agent(name='agent2')
   
   # Create a manager and register agents
   manager = AgentManager()
   manager.register(agent1)
   manager.register(agent2)
   
   # Run all agents in parallel
   results = manager.run_all(task='distributed task')

API Reference
-----------

Core Classes
~~~~~~~~~~~

.. autoclass:: Agent
   :members:
   :inherited-members:
   
.. autoclass:: AgentManager
   :members:

Utility Functions
~~~~~~~~~~~~~~~

.. autofunction:: create_agent

.. autofunction:: configure_agent