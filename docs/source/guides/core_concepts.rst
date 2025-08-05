.. title:: Core Concepts
.. _core_concepts:

Core Concepts
=============

This guide introduces the core concepts behind Haive's architecture and functionality.

Agents
------

Agents are autonomous entities that can process information, make decisions, and take actions. In Haive, agents are:

- **Modular*: Composed of interchangeable components
- **Stateful*: Maintain information across interactions
- **Tool-enabled*: Can use tools to interact with external systems
- **Configurable*: Highly customizable for different use cases

Engines
-------

Engines power the cognitive abilities of agents:

- **LLM Engines*: Connect to language models from providers like OpenAI, Anthropic, etc.
- **Vector Engines*: Enable semantic search and retrieval
- **Custom Engines*: Create specialized cognitive components

Tools
-----

Tools extend agent capabilities, allowing them to:

- Search the web
- Access databases
- Perform calculations
- Generate images
- And much more

State Management
----------------

Haive's state management system:

- Tracks agent knowledge and memory
- Enables persistence across sessions
- Allows for structured state schemas
- Supports dynamic state updates

Nodes
-----

The node system enables:

- Composable agent architectures
- Flexible execution flows
- Custom node implementation
- Dynamic routing between components

Next Steps
----------

Continue with these guides:

- :doc:`architecture - Detailed system architecture`
- :doc:`building_agents - How to create custom agents`
- :doc:`using_tools - Working with tools effectively`
