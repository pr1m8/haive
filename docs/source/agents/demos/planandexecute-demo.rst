PlanAndExecuteAgent Demo
{{ '=' * (len(agent_name) + 5) }}*

PlanAndExecuteAgent - Multi-step planning and execution agents

.. raw:: html

   <div class="agent-demo-container">
   <!-- Agent Overview Card -->

.. raw:: html

   <div class="agent-overview-card">

.. raw:: html

   <div class="agent-header">

.. raw:: html

   <div class="agent-icon">📋</div>

.. raw:: html

   <div>
   <h2>PlanAndExecuteAgent</h2>
   <p class="agent-type">planning</p>
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

           <div id="planandexecute-graph"
                class="agent-graph-container"
                data-agent-graph='{"nodes": [{"id": "start", "type": "start", "label": "START"}, {"id": "end", "type": "end", "label": "END"}, {"id": "plan", "type": "agent", "label": "Plan", "description": "Create execution plan"}, {"id": "execute", "type": "tool", "label": "Execute", "description": "Run plan steps"}, {"id": "monitor", "type": "validation", "label": "Monitor", "description": "Track progress"}], "edges": [{"source": "start", "target": "plan"}, {"source": "plan", "target": "execute"}, {"source": "execute", "target": "monitor"}, {"source": "monitor", "target": "execute"}, {"source": "monitor", "target": "end"}], "executionTrace": [{"step": 1, "node": "start", "status": "completed", "duration": 0.1, "output": "Initialized"}, {"step": 2, "node": "plan", "status": "completed", "duration": 1.2, "output": "Processing..."}, {"step": 3, "node": "end", "status": "completed", "duration": 0.1, "output": "Finished"}]}'>
.. raw:: html

   </div>

.. raw:: html

   <!-- State History Timeline -->

           <div id="planandexecute-state-history"
                class="state-history-container"
                data-state-history='[{"timestamp": "2025-01-08T10:00:00Z", "step": 1, "state": {"status": "initialized", "input": "User query"}, "diff": {"added": ["status", "input"], "changed": [], "removed": []}}, {"timestamp": "2025-01-08T10:00:01Z", "step": 2, "state": {"status": "processing", "input": "User query", "output": "Generated response"}, "diff": {"added": ["output"], "changed": ["status"], "removed": []}}]'>
.. raw:: html

   </div>

.. raw:: html

   <!-- Execution Trace -->

           <div id="planandexecute-execution-trace"
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
   <textarea id="planandexecute-input" placeholder="Example task for PlanAndExecuteAgent"></textarea>
   </div>

.. raw:: html

   <button onclick="runAgent('planandexecute')" class="run-button">

                Run PlanAndExecuteAgent
.. raw:: html

   </button>

.. raw:: html

   <div id="planandexecute-output" class="example-output"></div>
   </div>

.. raw:: html

   </div>

.. raw:: html

   <script>

    // Initialize visualization on page load
    document.addEventListener('DOMContentLoaded', function() {
        // Initialize graph
        const graphData = JSON.parse(document.getElementById('planandexecute-graph').dataset.agentGraph);
        new AgentGraphVisualizer('planandexecute-graph', graphData);

        // Initialize state history
        const stateData = JSON.parse(document.getElementById('planandexecute-state-history').dataset.stateHistory);
        new StateHistoryVisualizer('planandexecute-state-history', stateData);

        // Initialize execution trace
        const traceData = JSON.parse(document.getElementById('planandexecute-execution-trace').dataset.executionTrace);
        new ExecutionTraceVisualizer('planandexecute-execution-trace', traceData);
    });
.. raw:: html

   </script>

Code Example
------------

.. code-block:: python

    from haive.agents.planning.plan_and_execute import PlanAndExecuteAgent

    # Initialize the agent
    agent = PlanAndExecuteAgent(
    name="planandexecute",
    model="gpt-4",
    temperature=0.7
    )

    # Run the agent
    result = await agent.arun("Example task for PlanAndExecuteAgent")
    print(result)

    Architecture Details
    --------------------

    The PlanAndExecuteAgent implements multi-step planning and execution agents.

    See Also
    --------

    - :doc:`/api/haive/agents/planning/plan_and_execute` - Full API documentation
    - :doc:`/guides/planning-guide` - Usage guide
    - :doc:`/examples/planning-examples` - More examples
