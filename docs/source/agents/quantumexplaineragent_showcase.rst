QuantumExplainerAgent Agent
===========================

Agent specializing in quantum computing education

**Agent Type:** ``custom.SimpleAgent``

**Module:** ``haive.mock.simpleagent``

**Features:**

* Streaming Support: ✅ Yes*
* Graph Visualization: ✅ Yes*
* Steps Captured: 5*

.. figure:: ../../captures/QuantumExplainerAgent_graph.png

   :alt: QuantumExplainerAgent Agent Graph
   :align: center
   :width: 80%

   Agent Architecture Graph

Interactive Example
-------------------

Example usage

**Input:**

.. code-block:: json

    {
    "query": "Explain quantum computing principles",
    "format": "beginner"
    }

    **Result:** ✅ **Success**

    The agent completed successfully.

    **Execution Time:** 0.00 seconds

    **Steps:** 5 processing steps

    Live Execution Capture
    ----------------------

    Below is the complete execution trace captured from a live run of this agent:

    .. note::

    Agent execution capture available at: ../../captures/QuantumExplainerAgent_dfca177b-5cba-4e06-99cc-c42174670413_202506.json

    Technical Details
    -----------------

    **Configuration**

    This agent is implemented as a ``SimpleAgent`` class.

    **Input Schema**

.. code-block:: json

    {
    "query": "Explain quantum computing principles",
    "format": "beginner"
    }

    **Output Schema**

.. code-block:: json

    {
    "messages": [
    {
    "content": "Processed: {'query': 'Explain quantum computing principles', 'format': 'beginner'}",
    "type": "result"
    }
    ]
    }

    **Performance**

    * Execution Time: 0.00s*
    * Status: ✅ Success*
    * Steps: 5*

    Usage Example
    -------------

.. code-block:: python

    from haive.mock.simpleagent import SimpleAgent

    # Initialize the agent
    agent = SimpleAgent()

    # Run with example input
    result = agent.run({"query": "Explain quantum computing principles", "format": "beginner"})

    # For streaming agents
    for update in agent.stream({"query": "Explain quantum computing principles", "format": "beginner"}):
    print(update)

    See Also
    --------

    * :doc:`../index` - Agent Index*
    * :doc:`../showcase` - Agent Showcase*
