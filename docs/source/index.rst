Haive Documentation
===================

Professional AI agent framework for Python developers.

.. raw:: html

    <div class="homepage-showcase">
        
        <div class="hero-section">
            <div class="hero-content">
                <div class="hero-badge">
                    <span class="badge-text">AI Agent Framework</span>
                </div>
                <h1 class="hero-title">Haive</h1>
                <p class="hero-subtitle">Professional-grade AI agents for conversational AI, game playing, and tool orchestration</p>
                <div class="hero-code">
                    <div class="code-header">
                        <span class="code-language">Python</span>
                        <span class="code-copy">📋</span>
                    </div>
                    <pre><code>pip install haive-agents
from haive.agents import SimpleAgent

agent = SimpleAgent(name="assistant")
response = await agent.arun("Hello, world!")
print(response)</code></pre>
                </div>
            </div>
        </div>
        
        <div class="navigation-grid">
            
            <div class="nav-card" onclick="window.location.href='introduction/index.html'">
                <div class="card-icon-wrapper">
                    <div class="card-icon">⚡</div>
                </div>
                <div class="card-content">
                    <h3>Quick Start</h3>
                    <p>Install Haive and create your first agent in minutes</p>
                    <span class="card-link">Get Started →</span>
                </div>
            </div>
            
            <div class="nav-card" onclick="window.location.href='agents/gallery.html'">
                <div class="card-icon-wrapper">
                    <div class="card-icon">🧠</div>
                </div>
                <div class="card-content">
                    <h3>Agent Gallery</h3>
                    <p>Explore conversational agents, game players, and RAG systems</p>
                    <span class="card-link">Browse Agents →</span>
                </div>
            </div>
            
            <div class="nav-card" onclick="window.location.href='api/haive/index.html'">
                <div class="card-icon-wrapper">
                    <div class="card-icon">📖</div>
                </div>
                <div class="card-content">
                    <h3>API Reference</h3>
                    <p>Complete documentation for all classes and methods</p>
                    <span class="card-link">View API Docs →</span>
                </div>
            </div>
            
        </div>
        
        <div class="features-section">
            <div class="section-header">
                <h2>Core Capabilities</h2>
                <p>Build sophisticated AI agents with these powerful features</p>
            </div>
            
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">🎮</div>
                    <h3>Game Intelligence</h3>
                    <p>Create AI opponents for Chess, Go, Poker, and strategic games</p>
                    <a href="games/index.html" class="feature-link">View Demos</a>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🔧</div>
                    <h3>Tool Orchestration</h3>
                    <p>Connect agents to APIs, databases, and external services</p>
                    <a href="tools/index.html" class="feature-link">Browse Tools</a>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">📚</div>
                    <h3>Knowledge Systems</h3>
                    <p>Build RAG systems with document retrieval and grounding</p>
                    <a href="guides/index.html" class="feature-link">Learn More</a>
                </div>
                
            </div>
        </div>
        
        <div class="use-cases-section">
            <div class="section-header">
                <h2>Implementation Examples</h2>
                <p>Common patterns and use cases for building AI agents</p>
            </div>
            
            <div class="use-cases-grid">
                <div class="use-case">
                    <div class="use-case-header">
                        <h3>Conversational AI</h3>
                        <span class="use-case-type">Chat Assistant</span>
                    </div>
                    <p>Build intelligent chatbots with memory and personality</p>
                    <div class="code-snippet">
                        <code>SimpleAgent(name="assistant", system_message="You are helpful")</code>
                    </div>
                </div>
                
                <div class="use-case">
                    <div class="use-case-header">
                        <h3>Knowledge Retrieval</h3>
                        <span class="use-case-type">RAG System</span>
                    </div>
                    <p>Create knowledge-grounded agents with document retrieval</p>
                    <div class="code-snippet">
                        <code>BaseRAGAgent.from_documents(documents, name="expert")</code>
                    </div>
                </div>
                
                <div class="use-case">
                    <div class="use-case-header">
                        <h3>Tool Integration</h3>
                        <span class="use-case-type">React Agent</span>
                    </div>
                    <p>Build agents that can use external tools and APIs</p>
                    <div class="code-snippet">
                        <code>ReactAgent(name="helper", tools=[calculator, search])</code>
                    </div>
                </div>
            </div>
        </div>
        
    </div>

    <style>
    /* Modern Professional Design */
    .homepage-showcase {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        position: relative;
        overflow: hidden;
    }
    
    .hero-section {
        text-align: center;
        padding: 6rem 2rem 4rem;
        position: relative;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .hero-badge {
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    .badge-text {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 300;
        margin-bottom: 1rem;
        color: white;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.9);
        margin: 0 0 3rem 0;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.5;
    }
    
    .hero-code {
        max-width: 650px;
        margin: 0 auto;
        text-align: left;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .code-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 1.5rem;
        background: rgba(0, 0, 0, 0.05);
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    .code-language {
        font-size: 0.8rem;
        color: #6b7280;
        font-weight: 500;
    }
    
    .code-copy {
        cursor: pointer;
        font-size: 0.9rem;
        opacity: 0.7;
        transition: opacity 0.2s ease;
    }
    
    .code-copy:hover {
        opacity: 1;
    }
    
    .hero-code pre {
        margin: 0;
        padding: 1.5rem;
        font-family: 'SF Mono', 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        font-size: 0.9rem;
        line-height: 1.6;
        color: #374151;
        background: none;
    }
    
    .hero-code code {
        background: none;
        padding: 0;
        font-size: inherit;
        color: inherit;
    }
    
    .navigation-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2rem;
        padding: 4rem 2rem;
        background: #ffffff;
    }
    
    .nav-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 2.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        display: flex;
        align-items: flex-start;
        gap: 1.5rem;
    }
    
    .nav-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
        border-color: #667eea;
    }
    
    .card-icon-wrapper {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        min-width: 60px;
        height: 60px;
    }
    
    .card-icon {
        font-size: 1.5rem;
        filter: grayscale(1) brightness(0) invert(1);
    }
    
    .card-content {
        flex: 1;
    }
    
    .nav-card h3 {
        font-size: 1.4rem;
        font-weight: 600;
        color: #1f2937;
        margin: 0 0 0.5rem 0;
    }
    
    .nav-card p {
        margin: 0 0 1rem 0;
        line-height: 1.6;
        font-size: 1rem;
        color: #6b7280;
    }
    
    .card-link {
        color: #667eea;
        font-weight: 500;
        font-size: 0.9rem;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        transition: color 0.2s ease;
    }
    
    .nav-card:hover .card-link {
        color: #4f46e5;
    }
    
    .features-section {
        padding: 4rem 2rem;
        background: #f8fafc;
    }
    
    .section-header {
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .section-header h2 {
        font-size: 2.5rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 1rem;
    }
    
    .section-header p {
        font-size: 1.1rem;
        color: #6b7280;
        margin: 0;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        max-width: 1000px;
        margin: 0 auto;
    }
    
    .feature-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 2rem;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .feature-card h3 {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1f2937;
        margin: 0 0 1rem 0;
    }
    
    .feature-card p {
        margin: 0 0 1.5rem 0;
        font-size: 1rem;
        color: #6b7280;
        line-height: 1.6;
    }
    
    .feature-link {
        color: #667eea;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.9rem;
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        transition: color 0.2s ease;
    }
    
    .feature-link:hover {
        color: #4f46e5;
    }
    
    .use-cases-section {
        padding: 4rem 2rem;
        background: #ffffff;
    }
    
    .use-cases-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2rem;
        max-width: 1100px;
        margin: 0 auto;
    }
    
    .use-case {
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .use-case:hover {
        background: #ffffff;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        transform: translateY(-1px);
    }
    
    .use-case-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .use-case h3 {
        margin: 0;
        color: #1f2937;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .use-case-type {
        background: #667eea;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .use-case p {
        margin: 0 0 1.5rem 0;
        color: #6b7280;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .code-snippet {
        background: #1f2937;
        border-radius: 8px;
        padding: 1rem;
        overflow-x: auto;
    }
    
    .code-snippet code {
        font-family: 'SF Mono', 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        font-size: 0.85rem;
        color: #e5e7eb;
        background: none;
        padding: 0;
        white-space: pre;
        line-height: 1.5;
    }

    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-subtitle {
            font-size: 1.1rem;
        }
        
        .navigation-grid {
            grid-template-columns: 1fr;
            padding: 2rem 1rem;
        }
        
        .nav-card {
            padding: 2rem;
        }
        
        .features-grid {
            grid-template-columns: 1fr;
        }
        
        .use-cases-grid {
            grid-template-columns: 1fr;
        }
        
        .hero-code {
            margin: 0 -1rem;
        }
        
        .section-header h2 {
            font-size: 2rem;
        }
        
        .features-section,
        .use-cases-section {
            padding: 2rem 1rem;
        }
    }
    </style>

.. toctree::
   :maxdepth: 2
   :caption: 📚 Introduction
   :hidden:

   introduction/index

.. toctree::
   :maxdepth: 2
   :caption: 🎮 Showcases & Gallery
   :hidden:

   agents/gallery
   games/index
   tools/index

.. toctree::
   :maxdepth: 2
   :caption: 📖 API Reference
   :hidden:

   api/haive/index

.. toctree::
   :maxdepth: 2
   :caption: 🧑‍💻 Guides & Examples
   :hidden:

   guides/index
   examples/index
   reference/index

Quick Links
-----------

- :doc:`api/haive/core/index` - Core infrastructure
- :doc:`api/haive/agents/index` - Agent implementations
- :doc:`api/haive/tools/index` - Tool integrations
- :ref:`genindex` - Complete index
- :ref:`modindex` - Module index
- :ref:`search` - Search documentation

Package Status
^^^^^^^^^^^^^^

.. raw:: html

   <div class="package-status">
       <div class="status-item">
           <span class="status-icon">🚀</span>
           <strong>haive-core</strong>
           <span class="status-badge stable">Stable</span>
       </div>
       <div class="status-item">
           <span class="status-icon">🤖</span>
           <strong>haive-agents</strong>
           <span class="status-badge stable">Stable</span>
       </div>
       <div class="status-item">
           <span class="status-icon">🛠️</span>
           <strong>haive-tools</strong>
           <span class="status-badge stable">Stable</span>
       </div>
       <div class="status-item">
           <span class="status-icon">🎮</span>
           <strong>haive-games</strong>
           <span class="status-badge beta">Beta</span>
       </div>
       <div class="status-item">
           <span class="status-icon">📡</span>
           <strong>haive-mcp</strong>
           <span class="status-badge beta">Beta</span>
       </div>
   </div>

   <style>
   .package-status {
       display: flex;
       flex-wrap: wrap;
       gap: 1rem;
       margin: 1rem 0;
       padding: 1rem;
       background: #f8fafc;
       border-radius: 8px;
       border: 1px solid #e2e8f0;
   }
   
   .status-item {
       display: flex;
       align-items: center;
       gap: 0.5rem;
       padding: 0.5rem 1rem;
       background: white;
       border-radius: 6px;
       border: 1px solid #e2e8f0;
       font-size: 0.9rem;
   }
   
   .status-icon {
       font-size: 1.2rem;
   }
   
   .status-badge {
       padding: 0.25rem 0.5rem;
       border-radius: 4px;
       font-size: 0.75rem;
       font-weight: 600;
       text-transform: uppercase;
   }
   
   .status-badge.stable {
       background: #dcfce7;
       color: #166534;
   }
   
   .status-badge.beta {
       background: #fef3c7;
       color: #92400e;
   }
   </style>

What's New
----------

.. note::
   
   **New Navigation Structure!** 
   
   The API documentation now uses a hierarchical structure with Haive as the root.
   Navigate through packages → modules → submodules for better organization.

Latest Updates
^^^^^^^^^^^^^^

- Restructured API documentation for better navigation
- Added contextual navigation that changes based on your location
- Improved module discovery and documentation generation
