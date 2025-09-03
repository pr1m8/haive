Agent Showcase
==============

.. raw:: html

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
               <a href="api/agents/simple/agent/index.html" class="action-primary">View Docs</a>
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
               <a href="api/agents/simple/structured_agent/index.html" class="action-primary">View Docs</a>
               <a href="#structured-example" class="action-secondary">See Example</a>
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
         <p class="section-description">Reasoning and action agents with tool use</p>
      </div>

      <div class="agent-grid">
         <!-- ReactAgent -->
         <div class="agent-card featured" data-tags="react tools">
            <div class="card-header">
               <div class="agent-icon">🔧</div>
               <div class="agent-badge">Essential</div>
            </div>
            <h3 class="agent-name">ReactAgent</h3>
            <p class="agent-description">
               Think-act-observe pattern for complex reasoning tasks.
               Integrates seamlessly with any LangChain tool.
            </p>
            <div class="agent-features">
               <span class="feature-tag">Tool Integration</span>
               <span class="feature-tag">Chain of Thought</span>
               <span class="feature-tag">Error Recovery</span>
            </div>
            <div class="agent-actions">
               <a href="api/agents/react/agent/index.html" class="action-primary">View Docs</a>
               <a href="#react-example" class="action-secondary">See Example</a>
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
         <p class="section-description">Retrieval-augmented generation for knowledge tasks</p>
      </div>

      <div class="agent-grid">
         <!-- Base RAG Agent -->
         <div class="agent-card" data-tags="rag retrieval">
            <div class="card-header">
               <div class="agent-icon">🔍</div>
               <div class="agent-badge">Foundation</div>
            </div>
            <h3 class="agent-name">BaseRAGAgent</h3>
            <p class="agent-description">
               Foundation for retrieval-augmented generation.
               Supports multiple vector stores and retrieval strategies.
            </p>
            <div class="agent-features">
               <span class="feature-tag">Vector Stores</span>
               <span class="feature-tag">Semantic Search</span>
               <span class="feature-tag">Context Injection</span>
            </div>
            <div class="agent-actions">
               <a href="api/agents/rag/base/agent/index.html" class="action-primary">View Docs</a>
               <a href="#rag-example" class="action-secondary">See Example</a>
            </div>
         </div>
      </div>
   </div>

   </div>

   <style>
   .modern-agent-showcase {
      margin: 2rem 0;
   }

   .showcase-hero {
      text-align: center;
      padding: 3rem 0;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border-radius: 1rem;
      margin-bottom: 2rem;
   }

   .hero-title {
      font-size: 3rem;
      margin-bottom: 1rem;
   }

   .hero-stats {
      display: flex;
      justify-content: center;
      gap: 3rem;
      margin-top: 2rem;
   }

   .stat {
      text-align: center;
   }

   .stat-number {
      display: block;
      font-size: 2.5rem;
      font-weight: bold;
   }

   .filter-tabs {
      display: flex;
      gap: 0.5rem;
      margin-bottom: 2rem;
      flex-wrap: wrap;
   }

   .filter-tab {
      padding: 0.5rem 1rem;
      border: 2px solid #e5e7eb;
      background: white;
      border-radius: 2rem;
      cursor: pointer;
      transition: all 0.2s;
   }

   .filter-tab.active {
      background: #667eea;
      color: white;
      border-color: #667eea;
   }

   .agent-section {
      margin-bottom: 3rem;
   }

   .section-header {
      margin-bottom: 2rem;
   }

   .section-title {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 2rem;
   }

   .agent-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
      gap: 1.5rem;
   }

   .agent-card {
      background: white;
      border: 1px solid #e5e7eb;
      border-radius: 0.75rem;
      padding: 1.5rem;
      transition: all 0.3s;
   }

   .agent-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 10px 30px rgba(0,0,0,0.1);
   }

   .agent-card.featured {
      border-color: #667eea;
   }

   .card-header {
      display: flex;
      justify-content: space-between;
      align-items: start;
      margin-bottom: 1rem;
   }

   .agent-icon {
      font-size: 2.5rem;
   }

   .agent-badge {
      background: #f3f4f6;
      padding: 0.25rem 0.75rem;
      border-radius: 1rem;
      font-size: 0.875rem;
      font-weight: 600;
   }

   .agent-badge.new {
      background: #10b981;
      color: white;
   }

   .agent-name {
      font-size: 1.5rem;
      margin-bottom: 0.5rem;
   }

   .agent-features {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
      margin: 1rem 0;
   }

   .feature-tag {
      background: #eff6ff;
      color: #3b82f6;
      padding: 0.25rem 0.75rem;
      border-radius: 1rem;
      font-size: 0.875rem;
   }

   .agent-actions {
      display: flex;
      gap: 1rem;
      margin-top: 1.5rem;
   }

   .action-primary {
      background: #667eea;
      color: white;
      padding: 0.5rem 1.5rem;
      border-radius: 0.5rem;
      text-decoration: none;
      transition: all 0.2s;
   }

   .action-primary:hover {
      background: #5a67d8;
   }

   .action-secondary {
      background: transparent;
      color: #667eea;
      padding: 0.5rem 1.5rem;
      border: 2px solid #667eea;
      border-radius: 0.5rem;
      text-decoration: none;
      transition: all 0.2s;
   }

   .action-secondary:hover {
      background: #667eea;
      color: white;
   }

   /* Dark mode support */
   @media (prefers-color-scheme: dark) {
      body[data-theme="dark"] .agent-card {
         background: #1e293b;
         border-color: #334155;
      }

      body[data-theme="dark"] .filter-tab {
         background: #1e293b;
         border-color: #334155;
         color: #e5e7eb;
      }

      body[data-theme="dark"] .filter-tab.active {
         background: #667eea;
         color: white;
      }
   }
   </style>

   <script>
   function filterAgents(category) {
      // Update active tab
      document.querySelectorAll('.filter-tab').forEach(tab => {
         tab.classList.remove('active');
      });
      event.target.classList.add('active');

      // Show/hide agent sections
      document.querySelectorAll('.agent-section').forEach(section => {
         if (category === 'all' || section.dataset.category === category) {
            section.style.display = 'block';
         } else {
            section.style.display = 'none';
         }
      });
   }
   </script>