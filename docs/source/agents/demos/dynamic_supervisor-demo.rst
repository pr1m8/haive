Dynamic Supervisor Demo
=======================

Dynamically manages and coordinates multiple agents

.. raw:: html

   <div class="agent-demo-container">
   <!-- Agent Overview -->

.. raw:: html

   <div class="agent-overview-card">

.. raw:: html

   <div class="agent-header">

.. raw:: html

   <div class="agent-icon">👔</div>

.. raw:: html

   <div>
   <h2>Dynamic Supervisor</h2>
   <p class="agent-category">Category: Orchestration</p>
   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="agent-features">
   <span class="feature-tag">Dynamic routing</span>
   <span class="feature-tag">Load balancing</span>
   <span class="feature-tag">Task delegation</span>
   <span class="feature-tag">Performance monitoring</span>
   </div>

.. raw:: html

   </div>

.. raw:: html

   <!-- Interactive Demo -->

.. raw:: html

   <div class="agent-interface">

.. raw:: html

   <div class="demo-controls">
   <h3>Try Dynamic Supervisor</h3>

.. raw:: html

   <div class="input-area">
   <textarea id="dynamic_supervisor-input" placeholder="Enter your input here..." rows="4"></textarea>
   </div>

.. raw:: html

   <button onclick="runAgent('dynamic_supervisor')" class="run-agent-btn">

                    Run Agent
.. raw:: html

   </button>
   </div>

.. raw:: html

   <div id="dynamic_supervisor-output" class="agent-output">
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

   <pre id="dynamic_supervisor-execution">

       Supervision Status:
       Active Agents: 4
       Tasks Completed: 12/15
       Average Response: 1.2s


   Current Assignments:
   - Research Agent → Market analysis
   - Writer Agent → Report draft
   - Review Agent → Quality check

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

The Dynamic Supervisor operates by:

1. Receiving input from the user or system
2. Processing through its specialized pipeline
3. Generating structured outputs
4. Maintaining state for future interactions

Use Cases
---------

- Ideal for orchestration tasks
- Can be integrated into larger workflows
- Supports both synchronous and asynchronous execution

Code Example
------------

.. code-block:: python

    from haive.agents.dynamic_supervisor.agent import DynamicSupervisor
    from haive.core.engine import AugLLMConfig

    # Create agent
    agent = DynamicSupervisor(
        name="my_dynamic_supervisor",
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

    - :doc:`/api/haive/agents/dynamic_supervisor/index` - API documentation
    - :doc:`/guides/building_agents` - Agent development guide
    - :doc:`/examples/agent_patterns` - Common patterns
