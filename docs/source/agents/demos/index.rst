Agent Demos
===========

Interactive demonstrations of all Haive agents with graph visualization, state tracking, and live examples.

.. toctree::
   :maxdepth: 1
   :caption: Agent Demonstrations


🤖 Simple Agents
~~~~~~~~~~~~~~~~~~~~~

   simple-demo
   structuredoutput-demo

🧠 React Agents
~~~~~~~~~~~~~~~~~~~~

   react-demo
   reactwithmemory-demo

📚 Rag Agents
~~~~~~~~~~~~~~~~~~

   baserag-demo
   adaptiverag-demo

📋 Planning Agents
~~~~~~~~~~~~~~~~~~~~~~~

   planandexecute-demo

💬 Conversation Agents
~~~~~~~~~~~~~~~~~~~~~~~~~~~

   debate-demo

🔬 Research Agents
~~~~~~~~~~~~~~~~~~~~~~~

   personresearch-demo

📄 Document_Modifiers Agents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   summarizer-demo

🎯 Reasoning_And_Critique Agents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   reflection-demo


.. raw:: html

    <style>
    .agent-demo-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }

    .demo-card {
        background: var(--color-background-secondary);
        border: 1px solid var(--color-background-border);
        border-radius: 12px;
        padding: 1.5rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .demo-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }

    .demo-card h3 {
        margin-top: 0;
        color: var(--color-brand-primary);
    }

    .demo-features {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 1rem 0;
    }

    .feature-tag {
        background: var(--color-brand-primary);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.75rem;
        font-weight: 500;
    }
    </style>

    <div class="agent-demo-grid">

        <div class="demo-card">
            <h3>🤖 SimpleAgent</h3>
            <p>SimpleAgent - Basic conversational agents for straightforward tasks</p>
            <div class="demo-features">
                <span class="feature-tag">Interactive</span>
                <span class="feature-tag">Visualized</span>
                <span class="feature-tag">Stateful</span>
                <span class="feature-tag">Async</span>
            </div>
            <a href="simple-demo.html" class="demo-link">View Demo →</a>
        </div>

        <div class="demo-card">
            <h3>🤖 StructuredOutputAgent</h3>
            <p>StructuredOutputAgent - Basic conversational agents for straightforward tasks</p>
            <div class="demo-features">
                <span class="feature-tag">Interactive</span>
                <span class="feature-tag">Visualized</span>
                <span class="feature-tag">Stateful</span>
                <span class="feature-tag">Async</span>
            </div>
            <a href="structuredoutput-demo.html" class="demo-link">View Demo →</a>
        </div>

        <div class="demo-card">
            <h3>🧠 ReactAgent</h3>
            <p>ReactAgent - Reasoning and Acting agents that think before they act</p>
            <div class="demo-features">
                <span class="feature-tag">Interactive</span>
                <span class="feature-tag">Visualized</span>
                <span class="feature-tag">Stateful</span>
                <span class="feature-tag">Async</span>
            </div>
            <a href="react-demo.html" class="demo-link">View Demo →</a>
        </div>

        <div class="demo-card">
            <h3>🧠 ReactWithMemoryAgent</h3>
            <p>ReactWithMemoryAgent - Reasoning and Acting agents that think before they act</p>
            <div class="demo-features">
                <span class="feature-tag">Interactive</span>
                <span class="feature-tag">Visualized</span>
                <span class="feature-tag">Stateful</span>
                <span class="feature-tag">Async</span>
            </div>
            <a href="reactwithmemory-demo.html" class="demo-link">View Demo →</a>
        </div>

        <div class="demo-card">
            <h3>📚 BaseRAGAgent</h3>
            <p>BaseRAGAgent - Retrieval-Augmented Generation agents with knowledge</p>
            <div class="demo-features">
                <span class="feature-tag">Interactive</span>
                <span class="feature-tag">Visualized</span>
                <span class="feature-tag">Stateful</span>
                <span class="feature-tag">Async</span>
            </div>
            <a href="baserag-demo.html" class="demo-link">View Demo →</a>
        </div>

        <div class="demo-card">
            <h3>📚 AdaptiveRAGAgent</h3>
            <p>AdaptiveRAGAgent - Retrieval-Augmented Generation agents with knowledge</p>
            <div class="demo-features">
                <span class="feature-tag">Interactive</span>
                <span class="feature-tag">Visualized</span>
                <span class="feature-tag">Stateful</span>
                <span class="feature-tag">Async</span>
            </div>
            <a href="adaptiverag-demo.html" class="demo-link">View Demo →</a>
        </div>

        <div class="demo-card">
            <h3>📋 PlanAndExecuteAgent</h3>
            <p>PlanAndExecuteAgent - Multi-step planning and execution agents</p>
            <div class="demo-features">
                <span class="feature-tag">Interactive</span>
                <span class="feature-tag">Visualized</span>
                <span class="feature-tag">Stateful</span>
                <span class="feature-tag">Async</span>
            </div>
            <a href="planandexecute-demo.html" class="demo-link">View Demo →</a>
        </div>

        <div class="demo-card">
            <h3>💬 DebateAgent</h3>
            <p>DebateAgent - Multi-agent conversation and collaboration</p>
            <div class="demo-features">
                <span class="feature-tag">Interactive</span>
                <span class="feature-tag">Visualized</span>
                <span class="feature-tag">Stateful</span>
                <span class="feature-tag">Async</span>
            </div>
            <a href="debate-demo.html" class="demo-link">View Demo →</a>
        </div>

        <div class="demo-card">
            <h3>🔬 PersonResearchAgent</h3>
            <p>PersonResearchAgent - Deep research and analysis agents</p>
            <div class="demo-features">
                <span class="feature-tag">Interactive</span>
                <span class="feature-tag">Visualized</span>
                <span class="feature-tag">Stateful</span>
                <span class="feature-tag">Async</span>
            </div>
            <a href="personresearch-demo.html" class="demo-link">View Demo →</a>
        </div>

        <div class="demo-card">
            <h3>📄 SummarizerAgent</h3>
            <p>SummarizerAgent - Document processing and transformation agents</p>
            <div class="demo-features">
                <span class="feature-tag">Interactive</span>
                <span class="feature-tag">Visualized</span>
                <span class="feature-tag">Stateful</span>
                <span class="feature-tag">Async</span>
            </div>
            <a href="summarizer-demo.html" class="demo-link">View Demo →</a>
        </div>

        <div class="demo-card">
            <h3>🎯 ReflectionAgent</h3>
            <p>ReflectionAgent - Advanced reasoning and self-critique agents</p>
            <div class="demo-features">
                <span class="feature-tag">Interactive</span>
                <span class="feature-tag">Visualized</span>
                <span class="feature-tag">Stateful</span>
                <span class="feature-tag">Async</span>
            </div>
            <a href="reflection-demo.html" class="demo-link">View Demo →</a>
        </div>
    </div>