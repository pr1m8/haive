.. title:: State Management
.. _state_management:

State Management
================

Effective state management is crucial for building capable and persistent agents in Haive.

State Basics

------------

In Haive, state:

- Represents an agent's knowledge and memory

- Persists across interactions
- Contains structured data
- Evolves throughout agent lifecycle

State Schema

------------

Haive uses Pydantic for state schemas:

.. code-block:: python

    from haive.core.schema import AgentState
    from pydantic import Field
    from typing import List, Dict, Optional

    class CustomerServiceAgentState(AgentState):
    customer_name: Optional[str] = None
    issue_description: Optional[str] = None
    past_interactions: List[Dict] = Field(default_factory=list)
    resolution_steps: List[str] = Field(default_factory=list)
    resolved: bool = False

    State Lifecycle

    ---------------

    Agent state goes through a typical lifecycle:

    1. **Initialization**: Created with default values

    2. **Population**: Updated with new information

    3. **Persistence**: Saved to storage

    4. **Retrieval**: Loaded from storage

    5. **Transformation**: Modified during execution

    Working with State

    ------------------

    Basic State Access

    ^^^^^^^^^^^^^^^^^^

.. code-block:: python

    # Creating an agent with custom state
    from haive.agents import SimpleAgent

    agent = SimpleAgent(state_class=CustomerServiceAgentState)

    # Accessing state properties
    agent.state.customer_name = "John Doe"
    print(agent.state.customer_name)  # John Doe

    # Checking state values
    if agent.state.resolved:
    print("Issue resolved!")
    else:
    print("Issue still pending")

    State Updates

    ^^^^^^^^^^^^^

.. code-block:: python

    # Adding to a list in state
    agent.state.resolution_steps.append("Verified account information")

    # Adding a past interaction
    agent.state.past_interactions.append({
    "timestamp": "2025-06-19T10:30:00",
    "message": "Customer reported login issues",
    "sentiment": "frustrated"
    })

    # Complete state update
    agent.state = CustomerServiceAgentState(
    customer_name="Jane Smith",
    issue_description="Billing dispute",
    resolution_steps=["Reviewed account history"]
    )

    State Persistence

    -----------------

    Haive supports multiple state persistence options:

    In-memory

    ^^^^^^^^^

    Default for short-lived agents:

.. code-block:: python

    agent = SimpleAgent(
    persistence_manager="memory"
    )

    File-based

    ^^^^^^^^^^

    For local development and testing:

.. code-block:: python

    agent = SimpleAgent(
    persistence_manager=FilePersistenceManager(
    directory="./agent_states"
    )
    )

    Database

    ^^^^^^^^

    For production deployments:

.. code-block:: python

    agent = SimpleAgent(
    persistence_manager=DatabasePersistenceManager(
    connection_string="postgresql://user:pass@localhost/agents"
    )
    )

    State Sharing

    -------------

    Agents can share state:

.. code-block:: python

    # Create a shared state
    shared_state = CustomerServiceAgentState(
    customer_name="Alex Johnson"
    )

    # Create agents with shared state
    agent1 = SimpleAgent(state=shared_state)
    agent2 = SimpleAgent(state=shared_state)

    # Update shared state through either agent
    agent1.state.issue_description = "Password reset"
    print(agent2.state.issue_description)  # Password reset

    Best Practices

    --------------

    - Define clear state schemas with appropriate types

    - Initialize state with sensible defaults
    - Document state fields with descriptive comments
    - Use state validation with Pydantic
    - Implement state persistence for important agents
    - Monitor state size to prevent excessive growth

    Next Steps

    ----------

    Continue with:

    - :doc:`engine_system` - Understanding the engine system

    - :doc:`agent_patterns` - Common agent design patterns
    - :doc:`custom_agents` - Building agents with custom state
