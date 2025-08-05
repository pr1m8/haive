RAG Agent Demo



Retrieval-Augmented Generation for accurate responses

   <div class="agent-demo-container">
   <!-- Agent Overview -->

   <div class="agent-overview-card">

   <div class="agent-header">

   <div class="agent-icon">📚</div>

   <div>
   <h2>RAG Agent</h2>
   <p class="agent-category">Category: Knowledge</p>
   </div>

   </div>

   <div class="agent-features">
   <span class="feature-tag">Document retrieval</span>
   <span class="feature-tag">Context injection</span>
   <span class="feature-tag">Source citation</span>
   <span class="feature-tag">Fact checking</span>
   </div>

   </div>

   <!-- Interactive Demo -->

   <div class="agent-interface">

   <div class="demo-controls">
   <h3>Try RAG Agent</h3>

   <div class="input-area">
   <textarea id="rag-input" placeholder="Enter your input here..." rows="4"></textarea>
   </div>

   <button onclick="runAgent('rag')" class="run-agent-btn">

                    Run Agent

   </button>
   </div>

   <div id="rag-output" class="agent-output">
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

   <pre id="rag-execution">

       Query: What is quantum computing?


   Retrieved Sources: 3
   Confidence: 95%

   Answer: Quantum computing uses quantum mechanics principles...

   Sources:
   [1] Introduction to Quantum Computing, MIT Press
   [2] Nature Physics, Vol 15, 2023
   [3] IBM Quantum Documentation

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



The RAG Agent operates by:

1. Receiving input from the user or system
2. Processing through its specialized pipeline
3. Generating structured outputs
4. Maintaining state for future interactions

Use Cases



- Ideal for knowledge tasks
- Can be integrated into larger workflows
- Supports both synchronous and asynchronous execution

Code Example



.. code-block:: python

    # Code example here

    from haive.agents.rag.agent import RAGAgent
    from haive.core.engine import AugLLMConfig

    # Create agent
    agent = RAGAgent(
        name="my_rag",
        engine=AugLLMConfig(temperature=0.7)
    )

    # Run agent
    result = agent.run("Your input here")
    print(result)

    Configuration Options


--------------------

.. code-block:: python

    # Code example here

    config = {
        "temperature": 0.7,
        "max_tokens": 1000,
        "timeout": 30,
        "retry_attempts": 3
    }

    See Also


-------

    - :doc:`/api/haive/agents/rag/index - API documentation`

`
    - :doc`:`/guides/building_agents - Agent development guide`

`
    - :doc`:`/examples/agent_patterns - Common patterns`

`
`
