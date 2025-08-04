ReactResearchAgent Agent
========================

A research agent using ReAct pattern with tool integration

**Agent Type:** ``custom.ReactAgent``

**Module:** ``haive.mock.reactagent``

**Features:**

* Streaming Support: ✅ Yes*
* Graph Visualization: ✅ Yes*
* Steps Captured: 5*

.. figure:: ../../captures/ReactResearchAgent_graph.png

   :alt: ReactResearchAgent Agent Graph
   :align: center
   :width: 80%
   
   Agent Architecture Graph

Interactive Example
-------------------

Researching solar panel technology developments

**Input:**

.. code-block:: json

    {
    "task": "Research the latest developments in solar panel technology",
    "tools_required": [
    "web_search",
    "pdf_analysis"
    ],
    "max_iterations": 5
    }

    **Result:** ✅ **Success**

    The agent completed successfully.

    **Execution Time:** 0.00 seconds

    **Steps:** 5 processing steps

    Live Execution Capture
    ----------------------

    Below is the complete execution trace captured from a live run of this agent:

    .. note::

    Agent execution capture available at: ../../captures/ReactResearchAgent_36df075d-3abb-4e13-a950-807bdb120004_202506.json

    Technical Details
    -----------------

    **Configuration**

    This agent is implemented as a ``ReactAgent`` class.

    **Input Schema**

.. code-block:: json

    {
    "task": "Research the latest developments in solar panel technology",
    "tools_required": [
    "web_search",
    "pdf_analysis"
    ],
    "max_iterations": 5
    }

    **Output Schema**

.. code-block:: json

    {
    "messages": [
    {
    "content": "Processed: {'task': 'Research the latest developments in solar panel technology', 'tools_required': ['web_search', 'pdf_analysis'], 'max_iterations': 5}",
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

    from haive.mock.reactagent import ReactAgent

    # Initialize the agent
    agent = ReactAgent()

    # Run with example input
    result = agent.run({"task": "Research the latest developments in solar panel technology", "tools_required": ["web_search", "pdf_analysis"], "max_iterations": 5})

    # For streaming agents
    for update in agent.stream({"task": "Research the latest developments in solar panel technology", "tools_required": ["web_search", "pdf_analysis"], "max_iterations": 5}):
    print(update)

    See Also
    --------

    * :doc:`../index` - Agent Index*
    * :doc:`../showcase` - Agent Showcase*
