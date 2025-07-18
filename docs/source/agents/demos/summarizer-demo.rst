SummarizerAgent Demo
{{ '=' * (len(agent_name) + 5) }}

SummarizerAgent - Document processing and transformation agents

.. raw:: html

    <div class="agent-demo-container">
        <!-- Agent Overview Card -->
        <div class="agent-overview-card">
            <div class="agent-header">
                <div class="agent-icon">📄</div>
                <div>
                    <h2>SummarizerAgent</h2>
                    <p class="agent-type">document_modifiers</p>
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
        <div id="summarizer-graph" 
             class="agent-graph-container"
             data-agent-graph='{"nodes": [{"id": "start", "type": "start", "label": "START"}, {"id": "end", "type": "end", "label": "END"}, {"id": "process", "type": "agent", "label": "Process", "description": "Main processing"}, {"id": "tools", "type": "tool", "label": "Tools", "description": "External tools"}, {"id": "validate", "type": "validation", "label": "Validate", "description": "Check results"}], "edges": [{"source": "start", "target": "process"}, {"source": "process", "target": "tools"}, {"source": "tools", "target": "validate"}, {"source": "validate", "target": "end"}], "executionTrace": [{"step": 1, "node": "start", "status": "completed", "duration": 0.1, "output": "Initialized"}, {"step": 2, "node": "process", "status": "completed", "duration": 1.2, "output": "Processing..."}, {"step": 3, "node": "end", "status": "completed", "duration": 0.1, "output": "Finished"}]}'>
        </div>

        <!-- State History Timeline -->
        <div id="summarizer-state-history" 
             class="state-history-container"
             data-state-history='[{"timestamp": "2025-01-08T10:00:00Z", "step": 1, "state": {"status": "initialized", "input": "User query"}, "diff": {"added": ["status", "input"], "changed": [], "removed": []}}, {"timestamp": "2025-01-08T10:00:01Z", "step": 2, "state": {"status": "processing", "input": "User query", "output": "Generated response"}, "diff": {"added": ["output"], "changed": ["status"], "removed": []}}]'>
        </div>

        <!-- Execution Trace -->
        <div id="summarizer-execution-trace" 
             class="execution-trace-container"
             data-execution-trace='[{"step": 1, "operation": "Initialize", "duration": 0.1, "status": "success"}, {"step": 2, "operation": "Process", "duration": 1.5, "status": "success"}, {"step": 3, "operation": "Finalize", "duration": 0.2, "status": "success"}]'>
        </div>

        <!-- Interactive Example -->
        <div class="interactive-example">
            <h3>Try it Live</h3>
            <div class="example-input">
                <label>Input:</label>
                <textarea id="summarizer-input" placeholder="Example task for SummarizerAgent"></textarea>
            </div>
            <button onclick="runAgent('summarizer')" class="run-button">
                Run SummarizerAgent
            </button>
            <div id="summarizer-output" class="example-output"></div>
        </div>
    </div>

    <script>
    // Initialize visualization on page load
    document.addEventListener('DOMContentLoaded', function() {
        // Initialize graph
        const graphData = JSON.parse(document.getElementById('summarizer-graph').dataset.agentGraph);
        new AgentGraphVisualizer('summarizer-graph', graphData);
        
        // Initialize state history
        const stateData = JSON.parse(document.getElementById('summarizer-state-history').dataset.stateHistory);
        new StateHistoryVisualizer('summarizer-state-history', stateData);
        
        // Initialize execution trace
        const traceData = JSON.parse(document.getElementById('summarizer-execution-trace').dataset.executionTrace);
        new ExecutionTraceVisualizer('summarizer-execution-trace', traceData);
    });
    </script>

Code Example
------------

.. code-block:: python

    from haive.agents.document_modifiers.summarizer import SummarizerAgent

    # Initialize the agent
    agent = SummarizerAgent(
    name="summarizer",
    model="gpt-4",
    temperature=0.7
    )

    # Run the agent
    result = await agent.arun("Example task for SummarizerAgent")
    print(result)

Architecture Details
--------------------

The SummarizerAgent implements document processing and transformation agents.

See Also
--------

- :doc:`/api/haive/agents/document_modifiers/summarizer` - Full API documentation
- :doc:`/guides/document_modifiers-guide` - Usage guide
- :doc:`/examples/document_modifiers-examples` - More examples