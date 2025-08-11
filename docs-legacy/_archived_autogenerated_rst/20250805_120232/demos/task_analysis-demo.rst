Task Analysis Agent Demo



Analyzes and decomposes complex tasks

   <div class="agent-demo-container">
   <!-- Agent Overview -->

   <div class="agent-overview-card">

   <div class="agent-header">

   <div class="agent-icon">📈</div>

   <div>
   <h2>Task Analysis Agent</h2>
   <p class="agent-category">Category: Planning</p>
   </div>

   </div>

   <div class="agent-features">
   <span class="feature-tag">Task breakdown</span>
   <span class="feature-tag">Complexity analysis</span>
   <span class="feature-tag">Resource estimation</span>
   <span class="feature-tag">Risk assessment</span>
   </div>

   </div>

   <!-- Interactive Demo -->

   <div class="agent-interface">

   <div class="demo-controls">
   <h3>Try Task Analysis Agent</h3>

   <div class="input-area">
   <textarea id="task_analysis-input" placeholder="Enter your input here..." rows="4"></textarea>
   </div>

   <button onclick="runAgent('task_analysis')" class="run-agent-btn">

                    Run Agent

   </button>
   </div>

   <div id="task_analysis-output" class="agent-output">
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

   <pre id="task_analysis-execution">

       Task Analysis: Build E-commerce Site


   Complexity: High
   Estimated Time: 3 months
   Required Skills: 5

   Subtasks:
   1. Frontend (40h)
   2. Backend API (60h)
   3. Database (20h)
   4. Payment Integration (30h)
   5. Testing (25h)

   Risk Factors: 3 identified

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



The Task Analysis Agent operates by:

1. Receiving input from the user or system
2. Processing through its specialized pipeline
3. Generating structured outputs
4. Maintaining state for future interactions

Use Cases



- Ideal for planning tasks
- Can be integrated into larger workflows
- Supports both synchronous and asynchronous execution

Code Example



.. code-block:: python

    # Code example here

    from haive.agents.task_analysis.agent import TaskAnalysisAgent
    from haive.core.engine import AugLLMConfig

    # Create agent
    agent = TaskAnalysisAgent(
        name="my_task_analysis",
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

    - :doc:`/api/haive/agents/task_analysis/index - API documentation`

`
    - :doc`:`/guides/building_agents - Agent development guide`

`
    - :doc`:`/examples/agent_patterns - Common patterns`

`
`
