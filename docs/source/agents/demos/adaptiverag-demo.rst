AdaptiveRAGAgent Demo
{{ '=' * (len(agent_name) + 5) }}*

AdaptiveRAGAgent - Retrieval-Augmented Generation agents with knowledge

.. raw:: html

   <div class="agent-demo-container">
   <!-- Agent Overview Card -->

.. raw:: html

   <div class="agent-overview-card">

.. raw:: html

   <div class="agent-header">

.. raw:: html

   <div class="agent-icon">📚</div>

.. raw:: html

   <div>
   <h2>AdaptiveRAGAgent</h2>
   <p class="agent-type">rag</p>
   </div>

.. raw:: html

   </div>

            

.. raw:: html

   <div class="agent-features">
   <span class="feature-tag">Interactive</span>
   <span class="feature-tag">Visualized</span>
   <span class="feature-tag">Stateful</span>
   <span class="feature-tag">Async</span>
   </div>

.. raw:: html

   </div>

.. raw:: html

   <!-- Graph Visualization -->

           <div id="adaptiverag-graph" 
                class="agent-graph-container"
                data-agent-graph='{"nodes": [{"id": "start", "type": "start", "label": "START"}, {"id": "end", "type": "end", "label": "END"}, {"id": "query", "type": "agent", "label": "Query Analysis", "description": "Understand the question"}, {"id": "retrieve", "type": "tool", "label": "Retrieve", "description": "Search knowledge base"}, {"id": "generate", "type": "agent", "label": "Generate", "description": "Create response"}], "edges": [{"source": "start", "target": "query"}, {"source": "query", "target": "retrieve"}, {"source": "retrieve", "target": "generate"}, {"source": "generate", "target": "end"}], "executionTrace": [{"step": 1, "node": "start", "status": "completed", "duration": 0.1, "output": "Initialized"}, {"step": 2, "node": "query", "status": "completed", "duration": 1.2, "output": "Processing..."}, {"step": 3, "node": "end", "status": "completed", "duration": 0.1, "output": "Finished"}]}'>
.. raw:: html

   </div>

.. raw:: html

   <!-- State History Timeline -->

           <div id="adaptiverag-state-history" 
                class="state-history-container"
                data-state-history='[{"timestamp": "2025-01-08T10:00:00Z", "step": 1, "state": {"status": "initialized", "input": "User query"}, "diff": {"added": ["status", "input"], "changed": [], "removed": []}}, {"timestamp": "2025-01-08T10:00:01Z", "step": 2, "state": {"status": "processing", "input": "User query", "output": "Generated response"}, "diff": {"added": ["output"], "changed": ["status"], "removed": []}}]'>
.. raw:: html

   </div>

.. raw:: html

   <!-- Execution Trace -->

           <div id="adaptiverag-execution-trace" 
                class="execution-trace-container"
                data-execution-trace='[{"step": 1, "operation": "Initialize", "duration": 0.1, "status": "success"}, {"step": 2, "operation": "Process", "duration": 1.5, "status": "success"}, {"step": 3, "operation": "Finalize", "duration": 0.2, "status": "success"}]'>
.. raw:: html

   </div>

.. raw:: html

   <!-- Interactive Example -->

.. raw:: html

   <div class="interactive-example">
   <h3>Try it Live</h3>

.. raw:: html

   <div class="example-input">
   <label>Input:</label>
   <textarea id="adaptiverag-input" placeholder="Example task for AdaptiveRAGAgent"></textarea>
   </div>

.. raw:: html

   <button onclick="runAgent('adaptiverag')" class="run-button">

                Run AdaptiveRAGAgent
.. raw:: html

   </button>

.. raw:: html

   <div id="adaptiverag-output" class="example-output"></div>
   </div>

.. raw:: html

   </div>

.. raw:: html

   <script>

    // Initialize visualization on page load
    document.addEventListener('DOMContentLoaded', function() {
        // Initialize graph
        const graphData = JSON.parse(document.getElementById('adaptiverag-graph').dataset.agentGraph);
        new AgentGraphVisualizer('adaptiverag-graph', graphData);
        
        // Initialize state history
        const stateData = JSON.parse(document.getElementById('adaptiverag-state-history').dataset.stateHistory);
        new StateHistoryVisualizer('adaptiverag-state-history', stateData);
        
        // Initialize execution trace
        const traceData = JSON.parse(document.getElementById('adaptiverag-execution-trace').dataset.executionTrace);
        new ExecutionTraceVisualizer('adaptiverag-execution-trace', traceData);
    });
.. raw:: html

   </script>

Code Example
------------

.. code-block:: python

    from haive.agents.rag.adaptive_rag import AdaptiveRAGAgent

    # Initialize the agent
    agent = AdaptiveRAGAgent(
    name="adaptiverag",
    model="gpt-4",
    temperature=0.7
    )

    # Run the agent
    result = await agent.arun("Example task for AdaptiveRAGAgent")
    print(result)

    Architecture Details
    --------------------

    The AdaptiveRAGAgent implements retrieval-augmented generation agents with knowledge.

    See Also
    --------

    - :doc:`/api/haive/agents/rag/adaptive_rag` - Full API documentation
    - :doc:`/guides/rag-guide` - Usage guide
    - :doc:`/examples/rag-examples` - More examples
