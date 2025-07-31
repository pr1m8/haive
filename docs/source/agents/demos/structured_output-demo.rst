Structured Output Agent Demo
============================

Generates structured, schema-compliant outputs

.. raw:: html

    <div class="agent-demo-container">
        <!-- Agent Overview -->
        <div class="agent-overview-card">
            <div class="agent-header">
                <div class="agent-icon">📊</div>
                <div>
                    <h2>Structured Output Agent</h2>
                    <p class="agent-category">Category: Data</p>
                </div>
            </div>

            <div class="agent-features">
                <span class="feature-tag">Schema validation</span>
                <span class="feature-tag">Type safety</span>
                <span class="feature-tag">Format conversion</span>
                <span class="feature-tag">Consistency</span>
            </div>
        </div>

        <!-- Interactive Demo -->
        <div class="agent-interface">
            <div class="demo-controls">
                <h3>Try Structured Output Agent</h3>
                <div class="input-area">
                    <textarea id="structured_output-input" placeholder="Enter your input here..." rows="4"></textarea>
                </div>
                <button onclick="runAgent('structured_output')" class="run-agent-btn">
                    Run Agent
                </button>
            </div>

            <div id="structured_output-output" class="agent-output">
                <!-- Agent output will appear here -->
                <div class="output-placeholder">
                    <p>Enter input and click "Run Agent" to see results</p>
                </div>
            </div>
        </div>

        <!-- Live Execution Stream -->
        <div class="agent-streaming">
            <h3>Live Execution</h3>
            <div class="streaming-indicator">
                Live Stream
            </div>
            <div class="execution-display">
                <pre id="structured_output-execution">
{
  "analysis": {
    "sentiment": "positive",
    "confidence": 0.89,
    "topics": ["AI", "innovation", "future"],
    "entities": [
      {"name": "OpenAI", "type": "ORG"},
      {"name": "GPT-4", "type": "PRODUCT"}
    ]
  }
}
                </pre>
            </div>
            <div class="execution-stats">
                <div class="stat">
                    <label>Status:</label>
                    <span class="status-active">Active</span>
                </div>
                <div class="stat">
                    <label>Runtime:</label>
                    <span>1.2s</span>
                </div>
                <div class="stat">
                    <label>Tokens:</label>
                    <span>847</span>
                </div>
            </div>
        </div>
    </div>

How It Works
------------

The Structured Output Agent operates by:

1. Receiving input from the user or system
2. Processing through its specialized pipeline
3. Generating structured outputs
4. Maintaining state for future interactions

Use Cases
---------

- Ideal for data tasks
- Can be integrated into larger workflows
- Supports both synchronous and asynchronous execution

Code Example
------------

.. code-block:: python

    from haive.agents.structured_output.agent import StructuredOutputAgent
    from haive.core.engine import AugLLMConfig

    # Create agent
    agent = StructuredOutputAgent(
        name="my_structured_output",
        engine=AugLLMConfig(temperature=0.7)
    )

    # Run agent
    result = agent.run("Your input here")
    print(result)

Configuration Options
--------------------

.. code-block:: python

    config = {
        "temperature": 0.7,
        "max_tokens": 1000,
        "timeout": 30,
        "retry_attempts": 3
    }

See Also
--------

- :doc:`/api/haive/agents/structured_output/index` - API documentation
- :doc:`/guides/building_agents` - Agent development guide
- :doc:`/examples/agent_patterns` - Common patterns
