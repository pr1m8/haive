Discovery Agent Demo
====================

Discovers patterns and insights in data

.. raw:: html

    <div class="agent-demo-container">
        <!-- Agent Overview -->
        <div class="agent-overview-card">
            <div class="agent-header">
                <div class="agent-icon">🔍</div>
                <div>
                    <h2>Discovery Agent</h2>
                    <p class="agent-category">Category: Analysis</p>
                </div>
            </div>

            <div class="agent-features">
                <span class="feature-tag">Pattern recognition</span>
                <span class="feature-tag">Anomaly detection</span>
                <span class="feature-tag">Insight generation</span>
                <span class="feature-tag">Visualization</span>
            </div>
        </div>

        <!-- Interactive Demo -->
        <div class="agent-interface">
            <div class="demo-controls">
                <h3>Try Discovery Agent</h3>
                <div class="input-area">
                    <textarea id="discovery-input" placeholder="Enter your input here..." rows="4"></textarea>
                </div>
                <button onclick="runAgent('discovery')" class="run-agent-btn">
                    Run Agent
                </button>
            </div>

            <div id="discovery-output" class="agent-output">
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
                <pre id="discovery-execution">
Discovery Report:
✓ Found 3 significant patterns
✓ Identified 2 anomalies
✓ Generated 5 insights

Key Finding: Customer behavior shifts on weekends
Confidence: 87%
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

The Discovery Agent operates by:

1. Receiving input from the user or system
2. Processing through its specialized pipeline
3. Generating structured outputs
4. Maintaining state for future interactions

Use Cases
---------

- Ideal for analysis tasks
- Can be integrated into larger workflows
- Supports both synchronous and asynchronous execution

Code Example
------------

.. code-block:: python

    from haive.agents.discovery.agent import DiscoveryAgent
    from haive.core.engine import AugLLMConfig

    # Create agent
    agent = DiscoveryAgent(
        name="my_discovery",
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

- :doc:`/api/haive/agents/discovery/index` - API documentation
- :doc:`/guides/building_agents` - Agent development guide
- :doc:`/examples/agent_patterns` - Common patterns
