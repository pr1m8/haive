Chain Agent Demo
================

Executes chains of operations in sequence

.. raw:: html

    <div class="agent-demo-container">
        <!-- Agent Overview -->
        <div class="agent-overview-card">
            <div class="agent-header">
                <div class="agent-icon">🔗</div>
                <div>
                    <h2>Chain Agent</h2>
                    <p class="agent-category">Category: Workflow</p>
                </div>
            </div>

            <div class="agent-features">
                <span class="feature-tag">Sequential execution</span>
                <span class="feature-tag">State passing</span>
                <span class="feature-tag">Error handling</span>
                <span class="feature-tag">Retry logic</span>
            </div>
        </div>

        <!-- Interactive Demo -->
        <div class="agent-interface">
            <div class="demo-controls">
                <h3>Try Chain Agent</h3>
                <div class="input-area">
                    <textarea id="chain-input" placeholder="Enter your input here..." rows="4"></textarea>
                </div>
                <button onclick="runAgent('chain')" class="run-agent-btn">
                    Run Agent
                </button>
            </div>

            <div id="chain-output" class="agent-output">
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
                <pre id="chain-execution">
Chain Execution:
Step 1: Data retrieval ✓
Step 2: Processing ✓
Step 3: Validation ✓
Step 4: Output generation ✓

Total time: 2.3s
Status: Complete
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

The Chain Agent operates by:

1. Receiving input from the user or system
2. Processing through its specialized pipeline
3. Generating structured outputs
4. Maintaining state for future interactions

Use Cases
---------

- Ideal for workflow tasks
- Can be integrated into larger workflows
- Supports both synchronous and asynchronous execution

Code Example
------------

.. code-block:: python

    from haive.agents.chain.agent import ChainAgent
    from haive.core.engine import AugLLMConfig

    # Create agent
    agent = ChainAgent(
        name="my_chain",
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

- :doc:`/api/haive/agents/chain/index` - API documentation
- :doc:`/guides/building_agents` - Agent development guide
- :doc:`/examples/agent_patterns` - Common patterns
