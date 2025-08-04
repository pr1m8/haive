Planning Agent Demo
===================

Creates and executes strategic plans

.. raw:: html

   <div class="agent-demo-container">
   <!-- Agent Overview -->

.. raw:: html

   <div class="agent-overview-card">

.. raw:: html

   <div class="agent-header">

.. raw:: html

   <div class="agent-icon">📋</div>

.. raw:: html

   <div>
   <h2>Planning Agent</h2>
   <p class="agent-category">Category: Strategy</p>
   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="agent-features">
   <span class="feature-tag">Goal decomposition</span>
   <span class="feature-tag">Step generation</span>
   <span class="feature-tag">Resource allocation</span>
   <span class="feature-tag">Timeline creation</span>
   </div>

.. raw:: html

   </div>

.. raw:: html

   <!-- Interactive Demo -->

.. raw:: html

   <div class="agent-interface">

.. raw:: html

   <div class="demo-controls">
   <h3>Try Planning Agent</h3>

.. raw:: html

   <div class="input-area">
   <textarea id="planning-input" placeholder="Enter your input here..." rows="4"></textarea>
   </div>

.. raw:: html

   <button onclick="runAgent('planning')" class="run-agent-btn">

                    Run Agent
.. raw:: html

   </button>
   </div>

.. raw:: html

   <div id="planning-output" class="agent-output">
   <!-- Agent output will appear here -->

.. raw:: html

   <div class="output-placeholder">
   <p>Enter input and click "Run Agent" to see results</p>
   </div>

.. raw:: html

   </div>
   </div>

.. raw:: html

   <!-- Live Execution Stream -->

.. raw:: html

   <div class="agent-streaming">
   <h3>Live Execution</h3>

.. raw:: html

   <div class="streaming-indicator">

                   Live Stream
.. raw:: html

   </div>

.. raw:: html

   <div class="execution-display">

.. raw:: html

   <pre id="planning-execution">

       Generated Plan:
       Goal: Launch new product


   Steps:
   1. Market research (2 weeks)
   2. Design phase (3 weeks)
   3. Development (6 weeks)
   4. Testing (2 weeks)
   5. Launch prep (1 week)

   Total Duration: 14 weeks
   Resources: 5 team members

.. raw:: html

   </pre>
   </div>

.. raw:: html

   <div class="execution-stats">

.. raw:: html

   <div class="stat">
   <label>Status:</label>
   <span class="status-active">Active</span>
   </div>

.. raw:: html

   <div class="stat">
   <label>Runtime:</label>
   <span>1.2s</span>
   </div>

.. raw:: html

   <div class="stat">
   <label>Tokens:</label>
   <span>847</span>
   </div>

.. raw:: html

   </div>
   </div>
   </div>

How It Works
------------

The Planning Agent operates by:

1. Receiving input from the user or system
2. Processing through its specialized pipeline
3. Generating structured outputs
4. Maintaining state for future interactions

Use Cases
---------

- Ideal for strategy tasks
- Can be integrated into larger workflows
- Supports both synchronous and asynchronous execution

Code Example
------------

.. code-block:: python

    from haive.agents.planning.agent import PlanningAgent
    from haive.core.engine import AugLLMConfig

    # Create agent
    agent = PlanningAgent(
        name="my_planning",
        engine=AugLLMConfig(temperature=0.7)
    )

    # Run agent
    result = agent.run("Your input here")
    print(result)

    Configuration Options
    ---------------------

.. code-block:: python

    config = {
        "temperature": 0.7,
        "max_tokens": 1000,
        "timeout": 30,
        "retry_attempts": 3
    }

    See Also
    --------

    - :doc:`/api/haive/agents/planning/index` - API documentation
    - :doc:`/guides/building_agents` - Agent development guide
    - :doc:`/examples/agent_patterns` - Common patterns
