TextSummarizerAgent Agent
=========================

Fast text summarization agent

**Agent Type:** ``custom.SimpleAgent``

**Module:** ``haive.mock.simpleagent``

**Features:**

* Streaming Support: ✅ Yes
* Graph Visualization: ✅ Yes
* Steps Captured: 5


.. figure:: ../../captures/TextSummarizerAgent_graph.png
   :alt: TextSummarizerAgent Agent Graph
   :align: center
   :width: 80%
   
   Agent Architecture Graph


Interactive Example
-------------------

Example usage

**Input:**

.. code-block:: json

    {
    "text": "Lorem ipsum dolor sit amet...",
    "task": "summarize"
    }

**Result:** ✅ **Success**

The agent completed successfully.

**Execution Time:** 0.00 seconds

**Steps:** 5 processing steps


Live Execution Capture
----------------------

Below is the complete execution trace captured from a live run of this agent:


.. note::

   Agent execution capture available at: ../../captures/TextSummarizerAgent_c9e09adb-29f0-4662-b877-f45abcdd97c9_202506.json

Technical Details
-----------------

**Configuration**

This agent is implemented as a ``SimpleAgent`` class.

**Input Schema**

.. code-block:: json

    {
    "text": "Lorem ipsum dolor sit amet...",
    "task": "summarize"
    }

**Output Schema**

.. code-block:: json

    {
    "messages": [
    {
    "content": "Processed: {'text': 'Lorem ipsum dolor sit amet...', 'task': 'summarize'}",
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
    result = agent.run({"text": "Lorem ipsum dolor sit amet...", "task": "summarize"})

    # For streaming agents
    for update in agent.stream({"text": "Lorem ipsum dolor sit amet...", "task": "summarize"}):
    print(update)

See Also
--------

* :doc:`../index` - Agent Index
* :doc:`../showcase` - Agent Showcase