Document Agent Demo
===================

Processes and analyzes documents

.. raw:: html

   <div class="agent-demo-container">
   <!-- Agent Overview -->

.. raw:: html

   <div class="agent-overview-card">

.. raw:: html

   <div class="agent-header">

.. raw:: html

   <div class="agent-icon">📄</div>

.. raw:: html

   <div>
   <h2>Document Agent</h2>
   <p class="agent-category">Category: Document Processing</p>
   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="agent-features">
   <span class="feature-tag">Text extraction</span>
   <span class="feature-tag">Summarization</span>
   <span class="feature-tag">Entity recognition</span>
   <span class="feature-tag">Classification</span>
   </div>

.. raw:: html

   </div>

.. raw:: html

   <!-- Interactive Demo -->

.. raw:: html

   <div class="agent-interface">

.. raw:: html

   <div class="demo-controls">
   <h3>Try Document Agent</h3>

.. raw:: html

   <div class="input-area">
   <textarea id="document-input" placeholder="Enter your input here..." rows="4"></textarea>
   </div>

.. raw:: html

   <button onclick="runAgent('document')" class="run-agent-btn">

                    Run Agent
.. raw:: html

   </button>
   </div>

.. raw:: html

   <div id="document-output" class="agent-output">
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

   <pre id="document-execution">

       Document Analysis:
       Type: Research Paper
       Pages: 12
       Topics: Machine Learning, NLP
       Key Entities: 8 identified


   Summary: This paper presents a novel approach to...

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

The Document Agent operates by:

1. Receiving input from the user or system
2. Processing through its specialized pipeline
3. Generating structured outputs
4. Maintaining state for future interactions

Use Cases
---------

- Ideal for document processing tasks
- Can be integrated into larger workflows
- Supports both synchronous and asynchronous execution

Code Example
------------

.. code-block:: python

    from haive.agents.document.agent import DocumentAgent
    from haive.core.engine import AugLLMConfig

    # Create agent
    agent = DocumentAgent(
        name="my_document",
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

    - :doc:`/api/haive/agents/document/index` - API documentation
    - :doc:`/guides/building_agents` - Agent development guide
    - :doc:`/examples/agent_patterns` - Common patterns
