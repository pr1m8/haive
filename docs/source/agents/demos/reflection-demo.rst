Reflection Agent Demo
=====================

Self-reflects on outputs and improves them

.. raw:: html

   <div class="agent-demo-container">
   <!-- Agent Overview -->

.. raw:: html

   <div class="agent-overview-card">

.. raw:: html

   <div class="agent-header">

.. raw:: html

   <div class="agent-icon">🪞</div>

.. raw:: html

   <div>
   <h2>Reflection Agent</h2>
   <p class="agent-category">Category: Quality</p>
   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="agent-features">
   <span class="feature-tag">Self-evaluation</span>
   <span class="feature-tag">Improvement suggestions</span>
   <span class="feature-tag">Quality metrics</span>
   <span class="feature-tag">Iterative refinement</span>
   </div>

.. raw:: html

   </div>

.. raw:: html

   <!-- Interactive Demo -->

.. raw:: html

   <div class="agent-interface">

.. raw:: html

   <div class="demo-controls">
   <h3>Try Reflection Agent</h3>

.. raw:: html

   <div class="input-area">
   <textarea id="reflection-input" placeholder="Enter your input here..." rows="4"></textarea>
   </div>

.. raw:: html

   <button onclick="runAgent('reflection')" class="run-agent-btn">

                    Run Agent
.. raw:: html

   </button>
   </div>

.. raw:: html

   <div id="reflection-output" class="agent-output">
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

   <pre id="reflection-execution">

       Initial Output: "The data shows improvement"


   Reflection:
   - Too vague ⚠️
   - Lacks specifics ⚠️
   - No metrics ⚠️

   Improved Output: "Sales data shows 23% improvement in Q3 2024 compared to Q2, driven by new marketing campaign

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

The Reflection Agent operates by:

1. Receiving input from the user or system
2. Processing through its specialized pipeline
3. Generating structured outputs
4. Maintaining state for future interactions

Use Cases
---------

- Ideal for quality tasks
- Can be integrated into larger workflows
- Supports both synchronous and asynchronous execution

Code Example
------------

.. code-block:: python

    from haive.agents.reflection.agent import ReflectionAgent
    from haive.core.engine import AugLLMConfig

    # Create agent
    agent = ReflectionAgent(
        name="my_reflection",
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

    - :doc:`/api/haive/agents/reflection/index` - API documentation
    - :doc:`/guides/building_agents` - Agent development guide
    - :doc:`/examples/agent_patterns` - Common patterns
