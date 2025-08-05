ReactAgent Demo
{{ '=' * (len(agent_name) + 5) }}*

ReactAgent - Reasoning and Acting agents that think before they act

   <div class="agent-demo-container">
   <!-- Agent Overview Card -->

   <div class="agent-overview-card">

   <div class="agent-header">

   <div class="agent-icon">🧠</div>

   <div>
   <h2>ReactAgent</h2>
   <p class="agent-type">react</p>
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

           <div id="react-graph"
                class="agent-graph-container"
                data-agent-graph='{"nodes": [{"id": "start", "type": "start", "label": "START"}, {"id": "end", "type": "end", "label": "END"}, {"id": "reason", "type": "agent", "label": "Reasoning", "description": "Analyze the problem"}, {"id": "act", "type": "tool", "label": "Action", "description": "Execute tools"}, {"id": "observe", "type": "validation", "label": "Observe", "description": "Process results"}], "edges": [{"source": "start", "target": "reason"}, {"source": "reason", "target": "act", "type": "conditional"}, {"source": "act", "target": "observe"}, {"source": "observe", "target": "reason"}, {"source": "reason", "target": "end"}], "executionTrace": [{"step": 1, "node": "start", "status": "completed", "duration": 0.1, "output": "Initialized"}, {"step": 2, "node": "reason", "status": "completed", "duration": 1.2, "output": "Processing..."}, {"step": 3, "node": "end", "status": "completed", "duration": 0.1, "output": "Finished"}]}'>
   </div>

   <!-- State History Timeline -->

           <div id="react-state-history"
                class="state-history-container"
                data-state-history='[{"timestamp": "2025-01-08T10:00:00Z", "step": 1, "state": {"current_task": "Analyze problem", "thoughts": ["Need to understand the user's request"], "action_needed": true}, "diff": {"added": ["current_task"], "changed": [], "removed": []}}, {"timestamp": "2025-01-08T10:00:01Z", "step": 2, "state": {"current_task": "Execute tool", "thoughts": ["Need to search for information", "Using web search tool"], "action_needed": false, "tool_results": "Found relevant information"}, "diff": {"added": ["tool_results"], "changed": ["current_task", "action_needed"], "removed": []}}]'>
   </div>

   <!-- Execution Trace -->

           <div id="react-execution-trace"
                class="execution-trace-container"
                data-execution-trace='[{"step": 1, "operation": "Initialize", "duration": 0.1, "status": "success"}, {"step": 2, "operation": "Process", "duration": 1.5, "status": "success"}, {"step": 3, "operation": "Finalize", "duration": 0.2, "status": "success"}]'>
   </div>

   <!-- Interactive Example -->

   <div class="interactive-example">
   <h3>Try it Live</h3>

   <div class="example-input">
   <label>Input:</label>
   <textarea id="react-input" placeholder="Example task for ReactAgent"></textarea>
   </div>

   <button onclick="runAgent('react')" class="run-button">

                Run ReactAgent
   </button>

   <div id="react-output" class="example-output"></div>
   </div>

   </div>

   <script>

    // Initialize visualization on page load
    document.addEventListener('DOMContentLoaded', function() {
        // Initialize graph
        const graphData = JSON.parse(document.getElementById('react-graph').dataset.agentGraph);
        new AgentGraphVisualizer('react-graph', graphData);

        // Initialize state history
        const stateData = JSON.parse(document.getElementById('react-state-history').dataset.stateHistory);
        new StateHistoryVisualizer('react-state-history', stateData);

        // Initialize execution trace
        const traceData = JSON.parse(document.getElementById('react-execution-trace').dataset.executionTrace);
        new ExecutionTraceVisualizer('react-execution-trace', traceData);
    });
   </script>

Code Example
------------

.. code-block:: python

    # Code example here

    from haive.agents.react import ReactAgent

    # Initialize the agent
    agent = ReactAgent(
    name="react",
    model="gpt-4",
    temperature=0.7
    )

    # Run the agent
    result = await agent.arun("Example task for ReactAgent")
    print(result)

    Architecture Details

--------------------

    The ReactAgent implements reasoning and acting agents that think before they act.

    See Also
    --------

    - :doc:`/api/haive/agents/react - Full API documentation`
    - :doc:`/guides/react-guide - Usage guide`
    - :doc:`/examples/react-examples - More examples`
