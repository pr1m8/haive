PersonResearchAgent Demo
{{ '=' * (len(agent_name) + 5) }}*

PersonResearchAgent - Deep research and analysis agents

   <div class="agent-demo-container">
   <!-- Agent Overview Card -->

   <div class="agent-overview-card">

   <div class="agent-header">

   <div class="agent-icon">🔬</div>

   <div>
   <h2>PersonResearchAgent</h2>
   <p class="agent-type">research</p>
   </div>

   </div>



   <div class="agent-features">
   <span class="feature-tag">Interactive</span>
   <span class="feature-tag">Visualized</span>
   <span class="feature-tag">Stateful</span>
   <span class="feature-tag">Async</span>
   </div>

   </div>

   <!-- Graph Visualization -->

           <div id="personresearch-graph"
                class="agent-graph-container"
                data-agent-graph='{"nodes": [{"id": "start", "type": "start", "label": "START"}, {"id": "end", "type": "end", "label": "END"}, {"id": "process", "type": "agent", "label": "Process", "description": "Main processing"}, {"id": "tools", "type": "tool", "label": "Tools", "description": "External tools"}, {"id": "validate", "type": "validation", "label": "Validate", "description": "Check results"}], "edges": [{"source": "start", "target": "process"}, {"source": "process", "target": "tools"}, {"source": "tools", "target": "validate"}, {"source": "validate", "target": "end"}], "executionTrace": [{"step": 1, "node": "start", "status": "completed", "duration": 0.1, "output": "Initialized"}, {"step": 2, "node": "process", "status": "completed", "duration": 1.2, "output": "Processing..."}, {"step": 3, "node": "end", "status": "completed", "duration": 0.1, "output": "Finished"}]}'>
   </div>

   <!-- State History Timeline -->

           <div id="personresearch-state-history"
                class="state-history-container"
                data-state-history='[{"timestamp": "2025-01-08T10:00:00Z", "step": 1, "state": {"status": "initialized", "input": "User query"}, "diff": {"added": ["status", "input"], "changed": [], "removed": []}}, {"timestamp": "2025-01-08T10:00:01Z", "step": 2, "state": {"status": "processing", "input": "User query", "output": "Generated response"}, "diff": {"added": ["output"], "changed": ["status"], "removed": []}}]'>
   </div>

   <!-- Execution Trace -->

           <div id="personresearch-execution-trace"
                class="execution-trace-container"
                data-execution-trace='[{"step": 1, "operation": "Initialize", "duration": 0.1, "status": "success"}, {"step": 2, "operation": "Process", "duration": 1.5, "status": "success"}, {"step": 3, "operation": "Finalize", "duration": 0.2, "status": "success"}]'>
   </div>

   <!-- Interactive Example -->

   <div class="interactive-example">
   <h3>Try it Live</h3>

   <div class="example-input">
   <label>Input:</label>
   <textarea id="personresearch-input" placeholder="Example task for PersonResearchAgent"></textarea>
   </div>

   <button onclick="runAgent('personresearch')" class="run-button">

                Run PersonResearchAgent
   </button>

   <div id="personresearch-output" class="example-output"></div>
   </div>

   </div>

   <script>

    // Initialize visualization on page load
    document.addEventListener('DOMContentLoaded', function() {
        // Initialize graph
        const graphData = JSON.parse(document.getElementById('personresearch-graph').dataset.agentGraph);
        new AgentGraphVisualizer('personresearch-graph', graphData);

        // Initialize state history
        const stateData = JSON.parse(document.getElementById('personresearch-state-history').dataset.stateHistory);
        new StateHistoryVisualizer('personresearch-state-history', stateData);

        // Initialize execution trace
        const traceData = JSON.parse(document.getElementById('personresearch-execution-trace').dataset.executionTrace);
        new ExecutionTraceVisualizer('personresearch-execution-trace', traceData);
    });
   </script>

Code Example
------------

.. code-block:: python

    # Code example here

    from haive.agents.research.person import PersonResearchAgent

    # Initialize the agent
    agent = PersonResearchAgent(
    name="personresearch",
    model="gpt-4",
    temperature=0.7
    )

    # Run the agent
    result = await agent.arun("Example task for PersonResearchAgent")
    print(result)

    Architecture Details

--------------------

    The PersonResearchAgent implements deep research and analysis agents.

    See Also
    --------

    - :doc:`/api/haive/agents/research/person - Full API documentation`
    - :doc:`/guides/research-guide - Usage guide`
    - :doc:`/examples/research-examples - More examples`
