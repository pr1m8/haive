ReflectionAgent Demo
{{ '=' * (len(agent_name) + 5) }}

ReflectionAgent - Advanced reasoning and self-critique agents

.. raw:: html

    <div class="agent-demo-container">
        <!-- Agent Overview Card -->
        <div class="agent-overview-card">
            <div class="agent-header">
                <div class="agent-icon">🎯</div>
                <div>
                    <h2>ReflectionAgent</h2>
                    <p class="agent-type">reasoning_and_critique</p>
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
        <div id="reflection-graph" 
             class="agent-graph-container"
             data-agent-graph='{"nodes": [{"id": "start", "type": "start", "label": "START"}, {"id": "end", "type": "end", "label": "END"}, {"id": "process", "type": "agent", "label": "Process", "description": "Main processing"}, {"id": "tools", "type": "tool", "label": "Tools", "description": "External tools"}, {"id": "validate", "type": "validation", "label": "Validate", "description": "Check results"}], "edges": [{"source": "start", "target": "process"}, {"source": "process", "target": "tools"}, {"source": "tools", "target": "validate"}, {"source": "validate", "target": "end"}], "executionTrace": [{"step": 1, "node": "start", "status": "completed", "duration": 0.1, "output": "Initialized"}, {"step": 2, "node": "process", "status": "completed", "duration": 1.2, "output": "Processing..."}, {"step": 3, "node": "end", "status": "completed", "duration": 0.1, "output": "Finished"}]}'>
        </div>

        <!-- State History Timeline -->
        <div id="reflection-state-history" 
             class="state-history-container"
             data-state-history='[{"timestamp": "2025-01-08T10:00:00Z", "step": 1, "state": {"status": "initialized", "input": "User query"}, "diff": {"added": ["status", "input"], "changed": [], "removed": []}}, {"timestamp": "2025-01-08T10:00:01Z", "step": 2, "state": {"status": "processing", "input": "User query", "output": "Generated response"}, "diff": {"added": ["output"], "changed": ["status"], "removed": []}}]'>
        </div>

        <!-- Execution Trace -->
        <div id="reflection-execution-trace" 
             class="execution-trace-container"
             data-execution-trace='[{"step": 1, "operation": "Initialize", "duration": 0.1, "status": "success"}, {"step": 2, "operation": "Process", "duration": 1.5, "status": "success"}, {"step": 3, "operation": "Finalize", "duration": 0.2, "status": "success"}]'>
        </div>

        <!-- Interactive Example -->
        <div class="interactive-example">
            <h3>Try it Live</h3>
            <div class="example-input">
                <label>Input:</label>
                <textarea id="reflection-input" placeholder="Example task for ReflectionAgent"></textarea>
            </div>
            <button onclick="runAgent('reflection')" class="run-button">
                Run ReflectionAgent
            </button>
            <div id="reflection-output" class="example-output"></div>
        </div>
    </div>

    <script>
    // Initialize visualization on page load
    document.addEventListener('DOMContentLoaded', function() {
        // Initialize graph
        const graphData = JSON.parse(document.getElementById('reflection-graph').dataset.agentGraph);
        new AgentGraphVisualizer('reflection-graph', graphData);
        
        // Initialize state history
        const stateData = JSON.parse(document.getElementById('reflection-state-history').dataset.stateHistory);
        new StateHistoryVisualizer('reflection-state-history', stateData);
        
        // Initialize execution trace
        const traceData = JSON.parse(document.getElementById('reflection-execution-trace').dataset.executionTrace);
        new ExecutionTraceVisualizer('reflection-execution-trace', traceData);
    });
    </script>

Code Example
------------

.. code-block:: python

    from haive.agents.reasoning_and_critique.reflection import ReflectionAgent

    # Initialize the agent
    agent = ReflectionAgent(
    name="reflection",
    model="gpt-4",
    temperature=0.7
    )

    # Run the agent
    result = await agent.arun("Example task for ReflectionAgent")
    print(result)

Architecture Details
--------------------

The ReflectionAgent implements advanced reasoning and self-critique agents.

See Also
--------

- :doc:`/api/haive/agents/reasoning_and_critique/reflection` - Full API documentation
- :doc:`/guides/reasoning_and_critique-guide` - Usage guide
- :doc:`/examples/reasoning_and_critique-examples` - More examples