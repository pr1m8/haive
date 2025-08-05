Agent Showcase
==============

Explore our comprehensive collection of AI agents, each designed for specific use cases and capabilities.

   <div class="modern-agent-showcase">

   <!-- Hero Section -->

   <div class="showcase-hero">
   <h1 class="hero-title">🚀 Haive Agent Collection</h1>
   <p class="hero-subtitle">Powerful, composable AI agents for every use case</p>

   <div class="hero-stats">

   <div class="stat">
   <span class="stat-number">25+</span>
   <span class="stat-label">Agent Types</span>
   </div>

   <div class="stat">
   <span class="stat-number">100+</span>
   <span class="stat-label">Built-in Tools</span>
   </div>

   <div class="stat">
   <span class="stat-number">∞</span>
   <span class="stat-label">Possibilities</span>
   </div>

   </div>
   </div>

   <!-- Filter Tabs -->

   <div class="filter-tabs">
   <button class="filter-tab active" onclick="filterAgents('all')">All Agents</button>
   <button class="filter-tab" onclick="filterAgents('simple')">Simple</button>
   <button class="filter-tab" onclick="filterAgents('react')">ReAct</button>
   <button class="filter-tab" onclick="filterAgents('rag')">RAG</button>
   <button class="filter-tab" onclick="filterAgents('multi')">Multi-Agent</button>
   <button class="filter-tab" onclick="filterAgents('research')">Research</button>
   <button class="filter-tab" onclick="filterAgents('planning')">Planning</button>
   </div>

   <!-- Core Agents Section -->

   <div class="agent-section" data-category="simple">

   <div class="section-header">
   <h2 class="section-title">
   <span class="section-icon">⭐</span>
   Core Agents
   </h2>
   <p class="section-description">Foundation agents for common tasks</p>
   </div>

   <div class="agent-grid">
   <!-- Simple Agent -->

   <div class="agent-card featured" data-tags="simple conversation">

   <div class="card-header">

   <div class="agent-icon">💬</div>

   <div class="agent-badge">Popular</div>
   </div>

   <h3 class="agent-name">SimpleAgent</h3>
   <p class="agent-description">

                        The foundation agent for straightforward conversational AI tasks.
                        Perfect for chatbots, Q&A systems, and basic interactions.
   </p>

   <div class="agent-features">
   <span class="feature-tag">Stateful Conversations</span>
   <span class="feature-tag">Memory Support</span>
   <span class="feature-tag">Async Ready</span>
   </div>

   <div class="agent-actions">
   <a href="/api/haive/agents/simple" class="action-primary">View Docs</a>
   <a href="#simple-example" class="action-secondary">See Example</a>
   </div>

   </div>

   <!-- Structured Output Agent -->

   <div class="agent-card" data-tags="simple structured">

   <div class="card-header">

   <div class="agent-icon">📊</div>

   <div class="agent-badge new">New</div>
   </div>

   <h3 class="agent-name">StructuredSimpleAgent</h3>
   <p class="agent-description">

                        Get perfectly structured, validated responses using Pydantic models.
                        Ideal for APIs, data extraction, and form processing.
   </p>

   <div class="agent-features">
   <span class="feature-tag">Type Safety</span>
   <span class="feature-tag">Pydantic Models</span>
   <span class="feature-tag">Validation</span>
   </div>

   <div class="agent-actions">
   <a href="/api/haive/agents/simple/structured" class="action-primary">View Docs</a>
   <a href="#structured-example" class="action-secondary">See Example</a>
   </div>

   </div>

   <!-- SimpleAgentV2 -->

   <div class="agent-card" data-tags="simple advanced">

   <div class="card-header">

   <div class="agent-icon">🚀</div>

   <div class="agent-badge enhanced">Enhanced</div>
   </div>

   <h3 class="agent-name">SimpleAgentV2</h3>
   <p class="agent-description">

                        Next-generation simple agent with advanced state management,
                        tool integration, and enhanced performance.
   </p>

   <div class="agent-features">
   <span class="feature-tag">Tool Support</span>
   <span class="feature-tag">Advanced State</span>
   <span class="feature-tag">Streaming</span>
   </div>

   <div class="agent-actions">
   <a href="/api/haive/agents/simple/v2" class="action-primary">View Docs</a>
   <a href="#v2-example" class="action-secondary">See Example</a>
   </div>

   </div>
   </div>
   </div>

   <!-- ReAct Agents Section -->

   <div class="agent-section" data-category="react">

   <div class="section-header">
   <h2 class="section-title">
   <span class="section-icon">🧠</span>
   ReAct Agents
   </h2>
   <p class="section-description">Reasoning and acting agents with tool integration</p>
   </div>

   <div class="agent-grid">
   <!-- ReactAgent -->

   <div class="agent-card featured" data-tags="react tools">

   <div class="card-header">

   <div class="agent-icon">🔧</div>

   <div class="agent-badge">Core</div>
   </div>

   <h3 class="agent-name">ReactAgent</h3>
   <p class="agent-description">

                        Powerful reasoning agent that can use tools to solve complex problems.
                        Combines thought, action, and observation cycles.
   </p>

   <div class="agent-features">
   <span class="feature-tag">Tool Integration</span>
   <span class="feature-tag">Chain of Thought</span>
   <span class="feature-tag">Error Recovery</span>
   </div>

   <div class="agent-actions">
   <a href="/api/haive/agents/react" class="action-primary">View Docs</a>
   <a href="#react-example" class="action-secondary">See Example</a>
   </div>

   </div>

   <!-- ReactAgent with Memory -->

   <div class="agent-card" data-tags="react memory">

   <div class="card-header">

   <div class="agent-icon">🧠</div>

   <div class="agent-badge">Advanced</div>
   </div>

   <h3 class="agent-name">ReactAgent + Memory</h3>
   <p class="agent-description">

                        Enhanced ReAct agent with persistent memory for long-term reasoning
                        and complex multi-step problem solving.
   </p>

   <div class="agent-features">
   <span class="feature-tag">Long-term Memory</span>
   <span class="feature-tag">Context Retention</span>
   <span class="feature-tag">Multi-step Tasks</span>
   </div>

   <div class="agent-actions">
   <a href="/api/haive/agents/react/memory" class="action-primary">View Docs</a>
   <a href="#react-memory-example" class="action-secondary">See Example</a>
   </div>

   </div>
   </div>
   </div>

   <!-- RAG Agents Section -->

   <div class="agent-section" data-category="rag">

   <div class="section-header">
   <h2 class="section-title">
   <span class="section-icon">📚</span>
   RAG Agents
   </h2>
   <p class="section-description">Retrieval-augmented generation for knowledge-intensive tasks</p>
   </div>

   <div class="agent-grid">
   <!-- Base RAG Agent -->

   <div class="agent-card" data-tags="rag knowledge">

   <div class="card-header">

   <div class="agent-icon">📖</div>

   <div class="agent-badge">Foundation</div>
   </div>

   <h3 class="agent-name">BaseRAGAgent</h3>
   <p class="agent-description">

                        Foundation RAG agent for building knowledge-aware applications.
                        Integrates with various vector stores and retrieval strategies.
   </p>

   <div class="agent-features">
   <span class="feature-tag">Vector Search</span>
   <span class="feature-tag">Knowledge Base</span>
   <span class="feature-tag">Flexible Retrieval</span>
   </div>

   <div class="agent-actions">
   <a href="/api/haive/agents/rag/base" class="action-primary">View Docs</a>
   <a href="#rag-example" class="action-secondary">See Example</a>
   </div>

   </div>

   <!-- Agentic RAG -->

   <div class="agent-card featured" data-tags="rag advanced">

   <div class="card-header">

   <div class="agent-icon">🎯</div>

   <div class="agent-badge hot">Hot</div>
   </div>

   <h3 class="agent-name">AgenticRAG</h3>
   <p class="agent-description">

                        State-of-the-art RAG with document grading, query rewriting,
                        and web search fallback. Production-ready for complex Q&A.
   </p>

   <div class="agent-features">
   <span class="feature-tag">Document Grading</span>
   <span class="feature-tag">Query Rewriting</span>
   <span class="feature-tag">Web Fallback</span>
   </div>

   <div class="agent-actions">
   <a href="/api/haive/agents/rag/agentic" class="action-primary">View Docs</a>
   <a href="#agentic-rag-example" class="action-secondary">See Example</a>
   </div>

   </div>

   <!-- Adaptive RAG -->

   <div class="agent-card" data-tags="rag adaptive">

   <div class="card-header">

   <div class="agent-icon">🔄</div>

   <div class="agent-badge">Smart</div>
   </div>

   <h3 class="agent-name">AdaptiveRAG</h3>
   <p class="agent-description">

                        Intelligent RAG that dynamically adjusts retrieval strategy based
                        on query complexity and available resources.
   </p>

   <div class="agent-features">
   <span class="feature-tag">Dynamic Strategy</span>
   <span class="feature-tag">Auto-optimization</span>
   <span class="feature-tag">Multi-source</span>
   </div>

   <div class="agent-actions">
   <a href="/api/haive/agents/rag/adaptive" class="action-primary">View Docs</a>
   <a href="#adaptive-rag-example" class="action-secondary">See Example</a>
   </div>

   </div>
   </div>
   </div>

   <!-- Multi-Agent Systems Section -->

   <div class="agent-section" data-category="multi">

   <div class="section-header">
   <h2 class="section-title">
   <span class="section-icon">👥</span>
   Multi-Agent Systems
   </h2>
   <p class="section-description">Coordinate multiple agents for complex workflows</p>
   </div>

   <div class="agent-grid">
   <!-- MultiAgent -->

   <div class="agent-card featured" data-tags="multi coordination">

   <div class="card-header">

   <div class="agent-icon">🎭</div>

   <div class="agent-badge">Powerful</div>
   </div>

   <h3 class="agent-name">MultiAgent</h3>
   <p class="agent-description">

                        Orchestrate multiple specialized agents working together.
                        Supports sequential, parallel, and conditional execution patterns.
   </p>

   <div class="agent-features">
   <span class="feature-tag">Agent Orchestration</span>
   <span class="feature-tag">State Sharing</span>
   <span class="feature-tag">Dynamic Routing</span>
   </div>

   <div class="agent-actions">
   <a href="/api/haive/agents/multi" class="action-primary">View Docs</a>
   <a href="#multi-agent-example" class="action-secondary">See Example</a>
   </div>

   </div>

   <!-- Supervisor Agent -->

   <div class="agent-card" data-tags="multi supervisor">

   <div class="card-header">

   <div class="agent-icon">👔</div>

   <div class="agent-badge">Leadership</div>
   </div>

   <h3 class="agent-name">SupervisorAgent</h3>
   <p class="agent-description">

                        Intelligent task delegation to specialized worker agents.
                        Monitors progress and ensures quality outcomes.
   </p>

   <div class="agent-features">
   <span class="feature-tag">Task Delegation</span>
   <span class="feature-tag">Quality Control</span>
   <span class="feature-tag">Worker Management</span>
   </div>

   <div class="agent-actions">
   <a href="/api/haive/agents/supervisor" class="action-primary">View Docs</a>
   <a href="#supervisor-example" class="action-secondary">See Example</a>
   </div>

   </div>

   <!-- Debate Agent -->

   <div class="agent-card" data-tags="multi conversation">

   <div class="card-header">

   <div class="agent-icon">⚖️</div>

   <div class="agent-badge">Discussion</div>
   </div>

   <h3 class="agent-name">DebateAgent</h3>
   <p class="agent-description">

                        Facilitate structured debates between multiple agents to explore
                        different perspectives and reach consensus.
   </p>

   <div class="agent-features">
   <span class="feature-tag">Multi-perspective</span>
   <span class="feature-tag">Consensus Building</span>
   <span class="feature-tag">Structured Format</span>
   </div>

   <div class="agent-actions">
   <a href="/api/haive/agents/conversation/debate" class="action-primary">View Docs</a>
   <a href="#debate-example" class="action-secondary">See Example</a>
   </div>

   </div>
   </div>
   </div>

   <!-- Research & Analysis Section -->

   <div class="agent-section" data-category="research">

   <div class="section-header">
   <h2 class="section-title">
   <span class="section-icon">🔬</span>
   Research & Analysis
   </h2>
   <p class="section-description">Deep research and analytical capabilities</p>
   </div>

   <div class="agent-grid">
   <!-- Person Research Agent -->

   <div class="agent-card" data-tags="research person">

   <div class="card-header">

   <div class="agent-icon">👤</div>

   <div class="agent-badge">Research</div>
   </div>

   <h3 class="agent-name">PersonResearchAgent</h3>
   <p class="agent-description">

                        Comprehensive research agent for gathering and analyzing information
                        about individuals from various sources.
   </p>

   <div class="agent-features">
   <span class="feature-tag">Multi-source</span>
   <span class="feature-tag">Fact Verification</span>
   <span class="feature-tag">Report Generation</span>
   </div>

   <div class="agent-actions">
   <a href="/api/haive/agents/research/person" class="action-primary">View Docs</a>
   <a href="#person-research-example" class="action-secondary">See Example</a>
   </div>

   </div>

   <!-- Deep Research Agent -->

   <div class="agent-card featured" data-tags="research deep">

   <div class="card-header">

   <div class="agent-icon">🔍</div>

   <div class="agent-badge">Advanced</div>
   </div>

   <h3 class="agent-name">DeepResearchAgent</h3>
   <p class="agent-description">

                        Advanced research agent that performs iterative, deep-dive research
                        with source verification and synthesis.
   </p>

   <div class="agent-features">
   <span class="feature-tag">Iterative Research</span>
   <span class="feature-tag">Source Validation</span>
   <span class="feature-tag">Synthesis</span>
   </div>

   <div class="agent-actions">
   <a href="/api/haive/agents/research/deep" class="action-primary">View Docs</a>
   <a href="#deep-research-example" class="action-secondary">See Example</a>
   </div>

   </div>

   <!-- STORM Research -->

   <div class="agent-card" data-tags="research storm">

   <div class="card-header">

   <div class="agent-icon">⚡</div>

   <div class="agent-badge">Comprehensive</div>
   </div>

   <h3 class="agent-name">STORMAgent</h3>
   <p class="agent-description">

                        Stanford's STORM methodology for creating comprehensive,
                        Wikipedia-style articles from research.
   </p>

   <div class="agent-features">
   <span class="feature-tag">Article Generation</span>
   <span class="feature-tag">Structured Output</span>
   <span class="feature-tag">Citations</span>
   </div>

   <div class="agent-actions">
   <a href="/api/haive/agents/research/storm" class="action-primary">View Docs</a>
   <a href="#storm-example" class="action-secondary">See Example</a>
   </div>

   </div>
   </div>
   </div>

   <!-- Planning & Reasoning Section -->

   <div class="agent-section" data-category="planning">

   <div class="section-header">
   <h2 class="section-title">
   <span class="section-icon">🎯</span>
   Planning & Reasoning
   </h2>
   <p class="section-description">Advanced planning and logical reasoning agents</p>
   </div>

   <div class="agent-grid">
   <!-- Plan and Execute -->

   <div class="agent-card featured" data-tags="planning execution">

   <div class="card-header">

   <div class="agent-icon">📋</div>

   <div class="agent-badge">Strategic</div>
   </div>

   <h3 class="agent-name">PlanAndExecuteAgent</h3>
   <p class="agent-description">

                        Creates comprehensive plans and executes them step-by-step with
                        adaptive replanning based on outcomes.
   </p>

   <div class="agent-features">
   <span class="feature-tag">Strategic Planning</span>
   <span class="feature-tag">Step Execution</span>
   <span class="feature-tag">Adaptive</span>
   </div>

   <div class="agent-actions">
   <a href="/api/haive/agents/planning/plan_and_execute" class="action-primary">View Docs</a>
   <a href="#plan-execute-example" class="action-secondary">See Example</a>
   </div>

   </div>

   <!-- ReWOO Agent -->

   <div class="agent-card" data-tags="planning rewoo">

   <div class="card-header">

   <div class="agent-icon">🌳</div>

   <div class="agent-badge">Efficient</div>
   </div>

   <h3 class="agent-name">ReWOOAgent</h3>
   <p class="agent-description">

                        Reasoning without observation - plans entire tool use sequence
                        upfront for maximum efficiency.
   </p>

   <div class="agent-features">
   <span class="feature-tag">Upfront Planning</span>
   <span class="feature-tag">Parallel Execution</span>
   <span class="feature-tag">Efficient</span>
   </div>

   <div class="agent-actions">
   <a href="/api/haive/agents/planning/rewoo" class="action-primary">View Docs</a>
   <a href="#rewoo-example" class="action-secondary">See Example</a>
   </div>

   </div>

   <!-- Self-Discover Agent -->

   <div class="agent-card" data-tags="planning reasoning">

   <div class="card-header">

   <div class="agent-icon">💡</div>

   <div class="agent-badge">Meta</div>
   </div>

   <h3 class="agent-name">SelfDiscoverAgent</h3>
   <p class="agent-description">

                        Meta-reasoning agent that discovers and applies the best reasoning
                        structure for each unique problem.
   </p>

   <div class="agent-features">
   <span class="feature-tag">Meta-reasoning</span>
   <span class="feature-tag">Self-improvement</span>
   <span class="feature-tag">Adaptive Logic</span>
   </div>

   <div class="agent-actions">
   <a href="/api/haive/agents/reasoning/self_discover" class="action-primary">View Docs</a>
   <a href="#self-discover-example" class="action-secondary">See Example</a>
   </div>

   </div>
   </div>
   </div>

   <!-- Specialized Agents Section -->

   <div class="agent-section" data-category="specialized">

   <div class="section-header">
   <h2 class="section-title">
   <span class="section-icon">🛠️</span>
   Specialized Agents
   </h2>
   <p class="section-description">Purpose-built agents for specific domains</p>
   </div>

   <div class="agent-grid">
   <!-- Document Processing -->

   <div class="agent-card" data-tags="specialized documents">

   <div class="card-header">

   <div class="agent-icon">📄</div>

   <div class="agent-badge">Documents</div>
   </div>

   <h3 class="agent-name">DocumentProcessingAgent</h3>
   <p class="agent-description">

                        Intelligent document processing with extraction, summarization,
                        and structured data output capabilities.
   </p>

   <div class="agent-features">
   <span class="feature-tag">OCR Support</span>
   <span class="feature-tag">Data Extraction</span>
   <span class="feature-tag">Multi-format</span>
   </div>

   <div class="agent-actions">
   <a href="/api/haive/agents/document" class="action-primary">View Docs</a>
   <a href="#document-example" class="action-secondary">See Example</a>
   </div>

   </div>

   <!-- Knowledge Graph Agent -->

   <div class="agent-card" data-tags="specialized knowledge">

   <div class="card-header">

   <div class="agent-icon">🕸️</div>

   <div class="agent-badge">Knowledge</div>
   </div>

   <h3 class="agent-name">KnowledgeGraphAgent</h3>
   <p class="agent-description">

                        Build and query knowledge graphs from unstructured data.
                        Perfect for relationship mapping and insights.
   </p>

   <div class="agent-features">
   <span class="feature-tag">Graph Building</span>
   <span class="feature-tag">Relationship Extraction</span>
   <span class="feature-tag">Query Interface</span>
   </div>

   <div class="agent-actions">
   <a href="/api/haive/agents/knowledge_graph" class="action-primary">View Docs</a>
   <a href="#kg-example" class="action-secondary">See Example</a>
   </div>

   </div>

   <!-- Summarization Agent -->

   <div class="agent-card" data-tags="specialized summarization">

   <div class="card-header">

   <div class="agent-icon">📝</div>

   <div class="agent-badge">Summary</div>
   </div>

   <h3 class="agent-name">SummarizationAgent</h3>
   <p class="agent-description">

                        Advanced summarization with multiple strategies: extractive,
                        abstractive, and hierarchical summarization.
   </p>

   <div class="agent-features">
   <span class="feature-tag">Multi-strategy</span>
   <span class="feature-tag">Length Control</span>
   <span class="feature-tag">Key Points</span>
   </div>

   <div class="agent-actions">
   <a href="/api/haive/agents/summarization" class="action-primary">View Docs</a>
   <a href="#summary-example" class="action-secondary">See Example</a>
   </div>

   </div>
   </div>
   </div>

   </div>

   <!-- Modern CSS Styling -->
   <style>

    /* Reset and Base Styles */
    .modern-agent-showcase {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        color: #1a1a1a;
        line-height: 1.6;
        max-width: 1400px;
        margin: 0 auto;
        padding: 2rem;
    }

    /* Hero Section */
    .showcase-hero {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 24px;
        color: white;
        margin-bottom: 3rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0 0 1rem 0;
        background: linear-gradient(to right, #fff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-subtitle {
        font-size: 1.5rem;
        opacity: 0.95;
        margin-bottom: 3rem;
        font-weight: 300;
    }

    .hero-stats {
        display: flex;
        justify-content: center;
        gap: 4rem;
        flex-wrap: wrap;
    }

    .stat {
        text-align: center;
    }

    .stat-number {
        display: block;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }

    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Filter Tabs */
    .filter-tabs {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 3rem;
        flex-wrap: wrap;
        padding: 0 1rem;
    }

    .filter-tab {
        padding: 0.75rem 1.5rem;
        border: 2px solid #e5e7eb;
        background: white;
        border-radius: 12px;
        font-weight: 600;
        color: #4b5563;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 0.95rem;
    }

    .filter-tab:hover {
        border-color: #667eea;
        color: #667eea;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
    }

    .filter-tab.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: transparent;
    }

    /* Agent Sections */
    .agent-section {
        margin-bottom: 4rem;
    }

    .section-header {
        margin-bottom: 2rem;
    }

    .section-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        color: #1f2937;
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .section-icon {
        font-size: 2.5rem;
    }

    .section-description {
        font-size: 1.1rem;
        color: #6b7280;
        margin: 0;
    }

    /* Agent Grid */
    .agent-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
        gap: 2rem;
    }

    /* Agent Cards */
    .agent-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 2px solid transparent;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .agent-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        border-color: #667eea;
    }

    .agent-card.featured {
        border-color: #667eea;
        background: linear-gradient(to bottom right, #ffffff, #f9fafb);
    }

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }

    .agent-icon {
        font-size: 3rem;
        line-height: 1;
    }

    .agent-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .agent-badge {
        background: #e5e7eb;
        color: #4b5563;
    }

    .agent-badge.new {
        background: #10b981;
        color: white;
    }

    .agent-badge.hot {
        background: #ef4444;
        color: white;
    }

    .agent-badge.enhanced {
        background: #8b5cf6;
        color: white;
    }

    .agent-name {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0 0 0.75rem 0;
        color: #1f2937;
    }

    .agent-description {
        color: #4b5563;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }

    .agent-features {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
    }

    .feature-tag {
        padding: 0.375rem 0.875rem;
        background: #f3f4f6;
        color: #374151;
        border-radius: 8px;
        font-size: 0.875rem;
        font-weight: 500;
    }

    .agent-actions {
        display: flex;
        gap: 1rem;
        margin-top: auto;
    }

    .action-primary,
    .action-secondary {
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        text-decoration: none;
        transition: all 0.3s ease;
        text-align: center;
        flex: 1;
    }

    .action-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    .action-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
    }

    .action-secondary {
        background: white;
        color: #667eea;
        border: 2px solid #667eea;
    }

    .action-secondary:hover {
        background: #667eea;
        color: white;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }

        .hero-subtitle {
            font-size: 1.25rem;
        }

        .agent-grid {
            grid-template-columns: 1fr;
        }

        .filter-tabs {
            justify-content: flex-start;
            overflow-x: auto;
            padding-bottom: 1rem;
        }

        .filter-tab {
            white-space: nowrap;
        }
    }

    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .modern-agent-showcase {
            color: #e5e7eb;
        }

        .agent-card {
            background: #1f2937;
            border-color: #374151;
        }

        .agent-name,
        .section-title {
            color: #f3f4f6;
        }

        .agent-description {
            color: #9ca3af;
        }

        .feature-tag {
            background: #374151;
            color: #e5e7eb;
        }

        .filter-tab {
            background: #1f2937;
            border-color: #374151;
            color: #e5e7eb;
        }

        .action-secondary {
            background: #1f2937;
            border-color: #667eea;
        }
    }
   </style>

   <!-- JavaScript for filtering -->
   <script>

    function filterAgents(category) {
        // Update active tab
        document.querySelectorAll('.filter-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        event.target.classList.add('active');

        // Show/hide sections
        document.querySelectorAll('.agent-section').forEach(section => {
            if (category === 'all' || section.dataset.category === category) {
                section.style.display = 'block';
            } else {
                section.style.display = 'none';
            }
        });
    }

    // Initialize
    document.addEventListener('DOMContentLoaded', function() {
        // Show all sections by default
        filterAgents('all');
    });
   </script>
