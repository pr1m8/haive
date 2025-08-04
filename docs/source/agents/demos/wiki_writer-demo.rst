Wiki Writer Agent Demo
======================

Creates wiki-style documentation

.. raw:: html

   <div class="agent-demo-container">
   <!-- Agent Overview -->

.. raw:: html

   <div class="agent-overview-card">

.. raw:: html

   <div class="agent-header">

.. raw:: html

   <div class="agent-icon">✍️</div>

.. raw:: html

   <div>
   <h2>Wiki Writer Agent</h2>
   <p class="agent-category">Category: Content</p>
   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="agent-features">
   <span class="feature-tag">Structured writing</span>
   <span class="feature-tag">Cross-referencing</span>
   <span class="feature-tag">Formatting</span>
   <span class="feature-tag">Version control</span>
   </div>

.. raw:: html

   </div>

.. raw:: html

   <!-- Interactive Demo -->

.. raw:: html

   <div class="agent-interface">

.. raw:: html

   <div class="demo-controls">
   <h3>Try Wiki Writer Agent</h3>

.. raw:: html

   <div class="input-area">
   <textarea id="wiki_writer-input" placeholder="Enter your input here..." rows="4"></textarea>
   </div>

.. raw:: html

   <button onclick="runAgent('wiki_writer')" class="run-agent-btn">

                    Run Agent
.. raw:: html

   </button>
   </div>

.. raw:: html

   <div id="wiki_writer-output" class="agent-output">
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

   <pre id="wiki_writer-execution">

       = Quantum Computing =


   Quantum computing is a type of computation that harnesses quantum phenomena.

   == Overview ==
   Unlike classical computers that use bits...

   == Key Concepts ==
   * Superposition*
   * Entanglement*
   * Quantum gates*

   [[See also]]: Quantum mechanics, Qubits

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

The Wiki Writer Agent operates by:

1. Receiving input from the user or system
2. Processing through its specialized pipeline
3. Generating structured outputs
4. Maintaining state for future interactions

Use Cases
---------

- Ideal for content tasks
- Can be integrated into larger workflows
- Supports both synchronous and asynchronous execution

Code Example
------------

.. code-block:: python

    from haive.agents.wiki_writer.agent import WikiWriterAgent
    from haive.core.engine import AugLLMConfig

    # Create agent
    agent = WikiWriterAgent(
        name="my_wiki_writer",
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

    - :doc:`/api/haive/agents/wiki_writer/index` - API documentation
    - :doc:`/guides/building_agents` - Agent development guide
    - :doc:`/examples/agent_patterns` - Common patterns
