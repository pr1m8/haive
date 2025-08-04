.. title:: Haive Architecture
.. _architecture:

Architecture
============

Haive is built on a modular architecture that enables flexible, composable AI systems.

System Overview
---------------

At a high level, Haive consists of:

.. code-block:: text

    ┌───────────────────────┐
    │       Agents          │
    │  ┌─────────────────┐  │
    │  │     State       │  │
    │  └─────────────────┘  │
    │  ┌─────────────────┐  │
    │  │     Engine      │  │
    │  └─────────────────┘  │
    │  ┌─────────────────┐  │
    │  │     Tools       │  │
    │  └─────────────────┘  │
    └───────────────────────┘

    Core Components
    ---------------

    Agents
    ^^^^^^

    Agents are the primary abstraction in Haive. Each agent:

    - Maintains internal state
    - Uses an engine for cognition
    - Accesses tools for capabilities
    - Follows defined patterns for processing

    Engines
    ^^^^^^^

    Engines power agent cognition:

    - **LLM Engines**: Connect to language models
    - **Vector Engines**: Manage embeddings and retrieval
    - **Specialized Engines**: Handle specific AI tasks

    Tools
    ^^^^^

    Tools extend agent capabilities:

    - Perform specific functions
    - Access external systems
    - Execute specialized operations
    - Return structured results

    State Management
    ^^^^^^^^^^^^^^^^

    The state system:

    - Tracks agent knowledge
    - Ensures persistence
    - Enables structured data schemas
    - Manages memory and context

    Node System
    -----------

    The node system is a key architectural innovation, enabling:

    - Composable processing units
    - Flexible execution flows
    - Dynamic routing between components
    - Reusable patterns

.. code-block:: text

    ┌───────────┐      ┌───────────┐      ┌───────────┐
    │   Input   │ ──▶ │  Process  │ ──▶ │   Output  │
    │   Node    │      │   Node    │      │   Node    │
    └───────────┘      └───────────┘      └───────────┘
    │
    ▼
    ┌───────────┐
    │   Tool    │
    │   Node    │
    └───────────┘

    Graph System
    ------------

    For complex agent behaviors, Haive uses a graph-based execution model:

    - Nodes connected in directed graphs
    - Conditional routing between nodes
    - State transformation across nodes
    - Parallelism and asynchronous execution

    Extension Points
    ----------------

    Haive is designed for extensibility:

    - **Custom Agents**: Specialized agent types
    - **Custom Tools**: New capabilities
    - **Custom Engines**: Alternative cognition engines
    - **Custom Nodes**: Specialized processing components
    - **Custom Patterns**: Reusable behavioral templates

    Next Steps
    ----------

    Continue with:

    - :doc:`state_management` - Understanding agent state
    - :doc:`engine_system` - Working with cognitive engines
    - :doc:`agent_patterns` - Common agent design patterns
