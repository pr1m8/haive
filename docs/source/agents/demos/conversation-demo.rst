Conversation Agent Demo
=======================

Manages multi-turn conversations with context

.. raw:: html

    <div class="agent-demo-container">
        <!-- Agent Overview -->
        <div class="agent-overview-card">
            <div class="agent-header">
                <div class="agent-icon">💭</div>
                <div>
                    <h2>Conversation Agent</h2>
                    <p class="agent-category">Category: Dialogue</p>
                </div>
            </div>

            <div class="agent-features">
                <span class="feature-tag">Context tracking</span>
                <span class="feature-tag">Turn management</span>
                <span class="feature-tag">Memory integration</span>
                <span class="feature-tag">Personality</span>
            </div>
        </div>

        <!-- Interactive Demo -->
        <div class="agent-interface">
            <div class="demo-controls">
                <h3>Try Conversation Agent</h3>
                <div class="input-area">
                    <textarea id="conversation-input" placeholder="Enter your input here..." rows="4"></textarea>
                </div>
                <button onclick="runAgent('conversation')" class="run-agent-btn">
                    Run Agent
                </button>
            </div>

            <div id="conversation-output" class="agent-output">
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
                <pre id="conversation-execution">
User: Tell me about AI safety
Assistant: AI safety is a critical field focusing on ensuring AI systems are beneficial and aligned with human values...

User: What are the main risks?
Assistant: The main risks include:
1. Misalignment with human goals
2. Unintended consequences
3. Adversarial uses...
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

The Conversation Agent operates by:

1. Receiving input from the user or system
2. Processing through its specialized pipeline
3. Generating structured outputs
4. Maintaining state for future interactions

Use Cases
---------

- Ideal for dialogue tasks
- Can be integrated into larger workflows
- Supports both synchronous and asynchronous execution

Code Example
------------

.. code-block:: python

    from haive.agents.conversation.agent import ConversationAgent
    from haive.core.engine import AugLLMConfig

    # Create agent
    agent = ConversationAgent(
        name="my_conversation",
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

- :doc:`/api/haive/agents/conversation/index` - API documentation
- :doc:`/guides/building_agents` - Agent development guide
- :doc:`/examples/agent_patterns` - Common patterns
