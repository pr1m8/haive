ClimateResearchAgent Agent
==========================

Comprehensive climate change research agent

**Agent Type:** ``custom.SimpleAgent``

**Module:** ``haive.mock.simpleagent``

**Features:**

* Streaming Support: ✅ Yes
* Graph Visualization: ✅ Yes
* Steps Captured: 5


.. figure:: ../../captures/ClimateResearchAgent_graph.png
   :alt: ClimateResearchAgent Agent Graph
   :align: center
   :width: 80%
   
   Agent Architecture Graph


Interactive Example
-------------------

Example usage

**Input:**

.. code-block:: json

    {
    "research_topic": "climate change solutions",
    "depth": "comprehensive"
    }

**Result:** ✅ **Success**

The agent completed successfully.

**Execution Time:** 0.00 seconds

**Steps:** 5 processing steps


Live Execution Capture
----------------------

Below is the complete execution trace captured from a live run of this agent:


.. note::

   Agent execution capture available at: ../../captures/ClimateResearchAgent_4101dd3c-ef9f-41df-a46f-3fc0eef7b22b_202506.json

Technical Details
-----------------

**Configuration**

This agent is implemented as a ``SimpleAgent`` class.

**Input Schema**

.. code-block:: json

    {
    "research_topic": "climate change solutions",
    "depth": "comprehensive"
    }

**Output Schema**

.. code-block:: json

    {
    "messages": [
    {
    "content": "Processed: {'research_topic': 'climate change solutions', 'depth': 'comprehensive'}",
    "type": "result"
    }
    ]
    }

**Performance**

* Execution Time: 0.00s
* Status: ✅ Success
* Steps: 5

Usage Example
-------------

.. code-block:: python

    from haive.mock.simpleagent import SimpleAgent

    # Initialize the agent
    agent = SimpleAgent()

    # Run with example input
    result = agent.run({"research_topic": "climate change solutions", "depth": "comprehensive"})

    # For streaming agents
    for update in agent.stream({"research_topic": "climate change solutions", "depth": "comprehensive"}):
    print(update)

See Also
--------

* :doc:`../index` - Agent Index
* :doc:`../showcase` - Agent Showcase