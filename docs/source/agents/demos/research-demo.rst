Research Agent Demo
===================

Conducts comprehensive research on topics

   <div class="agent-demo-container">
   <!-- Agent Overview -->

   <div class="agent-overview-card">

   <div class="agent-header">

   <div class="agent-icon">🔬</div>

   <div>
   <h2>Research Agent</h2>
   <p class="agent-category">Category: Investigation</p>
   </div>

   </div>

   <div class="agent-features">
   <span class="feature-tag">Multi-source search</span>
   <span class="feature-tag">Fact verification</span>
   <span class="feature-tag">Bibliography</span>
   <span class="feature-tag">Synthesis</span>
   </div>

   </div>

   <!-- Interactive Demo -->

   <div class="agent-interface">

   <div class="demo-controls">
   <h3>Try Research Agent</h3>

   <div class="input-area">
   <textarea id="research-input" placeholder="Enter your input here..." rows="4"></textarea>
   </div>

   <button onclick="runAgent('research')" class="run-agent-btn">

                    Run Agent
   </button>
   </div>

   <div id="research-output" class="agent-output">
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

   <pre id="research-execution">

       Research Report: AI in Healthcare


   Sources Analyzed: 47
   Key Findings: 12
   Confidence Level: High

   Executive Summary:
   AI adoption in healthcare has increased 40% in 2024...

   Full report: 2,500 words
   Citations: 23

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

The Research Agent operates by:

1. Receiving input from the user or system
2. Processing through its specialized pipeline
3. Generating structured outputs
4. Maintaining state for future interactions

Use Cases
---------

- Ideal for investigation tasks
- Can be integrated into larger workflows
- Supports both synchronous and asynchronous execution

Code Example
------------

.. code-block:: python

    # Code example here

    from haive.agents.research.agent import ResearchAgent
    from haive.core.engine import AugLLMConfig

    # Create agent
    agent = ResearchAgent(
        name="my_research",
        engine=AugLLMConfig(temperature=0.7)
    )

    # Run agent
    result = agent.run("Your input here")
    print(result)

    Configuration Options

---------------------

.. code-block:: python

    # Code example here

    config = {
        "temperature": 0.7,
        "max_tokens": 1000,
        "timeout": 30,
        "retry_attempts": 3
    }

    See Also

--------

    - :doc:`/api/haive/agents/research/index - API documentation`
    - :doc:`/guides/building_agents - Agent development guide`
    - :doc:`/examples/agent_patterns - Common patterns`
