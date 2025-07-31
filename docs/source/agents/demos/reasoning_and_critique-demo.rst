Reasoning & Critique Agent Demo
===============================

Provides logical reasoning and critical analysis

.. raw:: html

    <div class="agent-demo-container">
        <!-- Agent Overview -->
        <div class="agent-overview-card">
            <div class="agent-header">
                <div class="agent-icon">🤔</div>
                <div>
                    <h2>Reasoning & Critique Agent</h2>
                    <p class="agent-category">Category: Analysis</p>
                </div>
            </div>

            <div class="agent-features">
                <span class="feature-tag">Logic chains</span>
                <span class="feature-tag">Argument analysis</span>
                <span class="feature-tag">Critique generation</span>
                <span class="feature-tag">Bias detection</span>
            </div>
        </div>

        <!-- Interactive Demo -->
        <div class="agent-interface">
            <div class="demo-controls">
                <h3>Try Reasoning & Critique Agent</h3>
                <div class="input-area">
                    <textarea id="reasoning_and_critique-input" placeholder="Enter your input here..." rows="4"></textarea>
                </div>
                <button onclick="runAgent('reasoning_and_critique')" class="run-agent-btn">
                    Run Agent
                </button>
            </div>

            <div id="reasoning_and_critique-output" class="agent-output">
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
                <pre id="reasoning_and_critique-execution">
Analysis of Argument:

Premise 1: Valid ✓
Premise 2: Questionable ⚠️
Conclusion: Does not follow

Logical Fallacies Detected:
- Hasty generalization
- Appeal to authority

Recommendation: Strengthen premise 2 with data
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

The Reasoning & Critique Agent operates by:

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

    from haive.agents.reasoning_and_critique.agent import Reasoning&CritiqueAgent
    from haive.core.engine import AugLLMConfig

    # Create agent
    agent = Reasoning&CritiqueAgent(
        name="my_reasoning_and_critique",
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

- :doc:`/api/haive/agents/reasoning_and_critique/index` - API documentation
- :doc:`/guides/building_agents` - Agent development guide
- :doc:`/examples/agent_patterns` - Common patterns
