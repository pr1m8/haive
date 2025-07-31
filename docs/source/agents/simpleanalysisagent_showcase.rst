SimpleAnalysisAgent Agent
=========================

A straightforward agent for content analysis and summarization

**Agent Type:** ``custom.ReactAgent``

**Module:** ``haive.mock.reactagent``

**Features:**

* Streaming Support: ✅ Yes
* Graph Visualization: ✅ Yes
* Steps Captured: 5


.. figure:: ../../captures/SimpleAnalysisAgent_graph.png
   :alt: SimpleAnalysisAgent Agent Graph
   :align: center
   :width: 80%
   
   Agent Architecture Graph


Interactive Example
-------------------

Analyzing renewable energy components

**Input:**

.. code-block:: json

    {
    "question": "What are the key components of a sustainable energy system?",
    "context": "renewable energy research"
    }

**Result:** ✅ **Success**

The agent completed successfully.

**Execution Time:** 0.00 seconds

**Steps:** 5 processing steps


Live Execution Capture
----------------------

Below is the complete execution trace captured from a live run of this agent:


.. note::

   Agent execution capture available at: ../../captures/SimpleAnalysisAgent_2dc7adda-3576-49f8-a799-0505a1d9604b_20250626_113523.json

Technical Details
-----------------

**Configuration**

This agent is implemented as a ``ReactAgent`` class.

**Input Schema**

.. code-block:: json

    {
    "question": "What are the key components of a sustainable energy system?",
    "context": "renewable energy research"
    }

**Output Schema**

.. code-block:: json

    {
    "messages": [
    {
    "content": "Processed: {'question': 'What are the key components of a sustainable energy system?', 'context': 'renewable energy research'}",
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

    from haive.mock.reactagent import ReactAgent

    # Initialize the agent
    agent = ReactAgent()

    # Run with example input
    result = agent.run({"question": "What are the key components of a sustainable energy system?", "context": "renewable energy research"})

    # For streaming agents
    for update in agent.stream({"question": "What are the key components of a sustainable energy system?", "context": "renewable energy research"}):
    print(update)

See Also
--------

* :doc:`../index` - Agent Index
* :doc:`../showcase` - Agent Showcase