Agent Visualization Guide
=========================

This guide explains how to standardize agent output visualization for documentation using the

``haive.core.utils.doc_util``s`` module.

Overview

--------

The agent visualization utilities help you:

1. Convert agent state history to markdown or RST for documentation

2. Visualize agent graphs consistently

3. Generate standardized documentation pages for agent examples
4. Create galleries of agent examples

These tools work with both`` ``haive.core.engine.agen``t`` and`` ``haive.agents.base.agen``t`` patterns.

Basic Usage

-----------

From a Python Script

~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from haive.core.utils.doc_utils import visualize_agent_run

    # After running your agent
    agent = SimpleAgent()
    result = agent.invoke("Hello, world!")

    # Visualize the run
    paths = visualize_agent_run(
    agent_name="SimpleAgent",
    state_history=agent.state_history,
    graph=agent.graph,
    description="Simple agent demonstration"
    )

    # Print paths to generated files
    print(f"State history: {paths['state_history']}")
    print(f"Graph visualization: {paths['graph']}")
    print(f"Documentation page: {paths['documentation']}")

From the Command Line

~~~~~~~~~~~~~~~~~~~~~

Use the provided script to process existing state history files or run agents:

.. code-block:: bash

    # Process existing state history files
    python scripts/generate_agent_docs.py --state-dir outputs/State_History

    # Run an agent and generate documentation
    python scripts/generate_agent_docs.py --agent SimpleAgent --prompt "Hello, world!"

    # Run all available agents with a standard prompt
    python scripts/generate_agent_docs.py --all

    # Run all agents with a custom prompt
    python scripts/generate_agent_docs.py --all --prompt "Explain how you work"

Advanced Usage

--------------

Customizing Visualization

~~~~~~~~~~~~~~~~~~~~~~~~~

You can create a custom`` ``AgentVisualize``r`` instance with specific output directories:

.. code-block:: python

    from haive.core.utils.doc_utils import AgentVisualizer

    # Create visualizer with custom directories
    visualizer = AgentVisualizer(
    output_dir="/path/to/output",
    state_history_dir="/path/to/state_history",
    graph_dir="/path/to/graphs"
    )

    # Use the visualizer methods directly
    state_path = visualizer.save_agent_state_history(
    agent_name="MyAgent",
    state_history=state_history,
    metadata={"custom_key": "custom_value"}
    )

    # Convert state history to markdown
    markdown = visualizer.state_history_to_markdown(
    state_history_path=state_path,
    include_metadata=True,
    max_states=5  # Limit to 5 states
    )

Creating Documentation Pages

~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generate complete documentation pages for agent examples:

.. code-block:: python

    # Generate a documentation page
    doc_path = visualizer.generate_agent_visualization_page(
    agent_name="ReActAgent",
    agent_description="ReAct agent that combines reasoning with actions",
    state_history_path=state_path,
    graph_path=graph_path,
    additional_content="## Custom Content\n\nAdd additional markdown content here."
    )

    # Create an index page for all examples
    index_path = create_agent_example_index()

Implementation Details

----------------------

State History Format

~~~~~~~~~~~~~~~~~~~~

The standard state history format is a JSON file with this structure:

.. code-block:: json

    {
    "metadata": {
    "agent_name": "SimpleAgent",
    "timestamp": "20250619_123456",
    "run_id": "abcd1234",
    "custom_field": "custom_value"
    },
    "state_history": [
    {
    "input": "Hello, world!",
    "thought": "I should respond to this greeting",
    "action": "respond",
    "observation": null,
    "output": "Hello! How can I help you today?"
    },
    // More states...
    ]
    }

Graph Visualization

~~~~~~~~~~~~~~~~~~~

The utility supports multiple graph formats:

1. LangGraph Graph objects (using`` ``get_graph(``)``)

2. Graphviz Digraph objects

3. Dictionary representations of graphs

Integration with Sphinx

-----------------------

To integrate agent examples into Sphinx documentation:

1. Create an examples directory in your docs:

   .. code-block:: bash

    mkdir -p docs/source/agents/examples

2. Generate agent examples using the utilities

3. Include the examples index in your toctree:

   .. code-block:: rst

    .. toctree::
    :maxdepth: 2
    :caption: Agent Documentation

    agents/index
    agents/examples/index

Best Practices

--------------

1. **Consistent Agent Name***s**: Use descriptive, consistent names for agents

2.*** **Add Metadat***a**: Include relevant metadata with each agent run

3.*** **Limit State Histor***y**: For documentation, limit to 5-10 states to keep pages concise
4.*** **Use SVG Graph***s**: SVG format provides the best quality for documentation
5.*** **Add Description***s**: Provide clear descriptions of what each agent example demonstrates

Example Gallery

---------------

Below is a gallery of example agent visualizations:


   .. card::
      :link: ../agents/examples/simple_agent_example
      :link-type: doc
      :class-card: agent-card

      Basic conversational agent example
   
   .. card::
      :link: ../agents/examples/react_agent_example
      :link-type: doc
      :class-card: agent-card

      Reasoning and acting agent example
   
   .. card::
      :link: ../agents/examples/rag_agent_example
      :link-type: doc
      :class-card: agent-card

      Retrieval-augmented generation example
   
   .. card::
      :link: ../agents/examples/task_analysis_example
      :link-type: doc
      :class-card: agent-card

      Task decomposition agent example``***