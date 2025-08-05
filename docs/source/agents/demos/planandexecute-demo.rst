PlanAndExecuteAgent Demo
{{ '=' * (len(agent_name) + 5) }}*

PlanAndExecuteAgent - Multi-step planning and execution agents

   <div class="agent-demo-container">
   <!-- Agent Overview Card -->

   <div class="agent-overview-card">

   <div class="agent-header">

   <div class="agent-icon">📋</div>

   <div>
   <h2>PlanAndExecuteAgent</h2>
   <p class="agent-type">planning</p>
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

           <div id="planandexecute-graph"
                class="agent-graph-container"
                data-agent-graph='{"nodes": [{"id": "start", "type": "start", "label": "START"}, {"id": "end", "type": "end", "label": "END"}, {"id": "plan", "type": "agent", "label": "Plan", "description": "Create execution plan"}, {"id": "execute", "type": "tool", "label": "Execute", "description": "Run plan steps"}, {"id": "monitor", "type": "validation", "label": "Monitor", "description": "Track progress"}], "edges": [{"source": "start", "target": "plan"}, {"source": "plan", "target": "execute"}, {"source": "execute", "target": "monitor"}, {"source": "monitor", "target": "execute"}, {"source": "monitor", "target": "end"}], "executionTrace": [{"step": 1, "node": "start", "status": "completed", "duration": 0.1, "output": "Initialized"}, {"step": 2, "node": "plan", "status": "completed", "duration": 1.2, "output": "Processing..."}, {"step": 3, "node": "end", "status": "completed", "duration": 0.1, "output": "Finished"}]}'>
   </div>

   <!-- State History Timeline -->

           <div id="planandexecute-state-history"
                class="state-history-container"
                data-state-history='[{"timestamp": "2025-01-08T10:00:00Z", "step": 1, "state": {"status": "initialized", "input": "User query"}, "diff": {"added": ["status", "input"], "changed": [], "removed": []}}, {"timestamp": "2025-01-08T10:00:01Z", "step": 2, "state": {"status": "processing", "input": "User query", "output": "Generated response"}, "diff": {"added": ["output"], "changed": ["status"], "removed": []}}]'>
   </div>

   <!-- Execution Trace -->

           <div id="planandexecute-execution-trace"
                class="execution-trace-container"
                data-execution-trace='[{"step": 1, "operation": "Initialize", "duration": 0.1, "status": "success"}, {"step": 2, "operation": "Process", "duration": 1.5, "status": "success"}, {"step": 3, "operation": "Finalize", "duration": 0.2, "status": "success"}]'>
   </div>

   <!-- Interactive Example -->

   <div class="interactive-example">
   <h3>Try it Live</h3>

   <div class="example-input">
   <label>Input:</label>
   <textarea id="planandexecute-input" placeholder="Example task for PlanAndExecuteAgent"></textarea>
   </div>

   <button onclick="runAgent('planandexecute')" class="run-button">

                Run PlanAndExecuteAgent
   </button>

   <div id="planandexecute-output" class="example-output"></div>
   </div>

   </div>

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
   </script>

Code Example
------------

.. code-block:: python

    # Code example here

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

    - :doc:`/api/haive/agents/planning/plan_and_execute - Full API documentation`
    - :doc:`/guides/planning-guide - Usage guide`
    - :doc:`/examples/planning-examples - More examples`
