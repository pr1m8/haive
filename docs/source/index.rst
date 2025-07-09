Haive Documentation
===================

Beautiful AI agent framework with intelligent collaboration.

.. raw:: html

    <div class="homepage-showcase">
        
        <div class="hero-section">
            <div class="hero-content">
                <h1 class="hero-title">🤖 Haive Agent Framework</h1>
                <p class="hero-subtitle">Build intelligent, collaborative agents with beautiful documentation</p>
            </div>
        </div>
        
        <div class="navigation-grid">
            
            <div class="nav-card primary" onclick="window.location.href='introduction/index.html'">
                <div class="card-icon">🚀</div>
                <h3>Getting Started</h3>
                <p>Installation, quickstart guide, and basic concepts</p>
                <div class="card-arrow">→</div>
            </div>
            
            <div class="nav-card secondary" onclick="window.location.href='agents/gallery.html'">
                <div class="card-icon">🤖</div>
                <h3>Agent Gallery</h3>
                <p>Explore pre-built agents and their capabilities</p>
                <div class="card-arrow">→</div>
            </div>
            
            <div class="nav-card accent" onclick="window.location.href='games/index.html'">
                <div class="card-icon">🎮</div>
                <h3>Interactive Games</h3>
                <p>AI opponents and interactive demonstrations</p>
                <div class="card-arrow">→</div>
            </div>
            
            <div class="nav-card warm" onclick="window.location.href='tools/index.html'">
                <div class="card-icon">🛠️</div>
                <h3>Tools Library</h3>
                <p>Browse available tools and integrations</p>
                <div class="card-arrow">→</div>
            </div>
            
            <div class="nav-card cool" onclick="window.location.href='guides/index.html'">
                <div class="card-icon">📝</div>
                <h3>Development Guides</h3>
                <p>Step-by-step tutorials and best practices</p>
                <div class="card-arrow">→</div>
            </div>
            
            <div class="nav-card info" onclick="window.location.href='api/haive/index.html'">
                <div class="card-icon">📚</div>
                <h3>API Reference</h3>
                <p>Complete API documentation by package</p>
                <div class="card-arrow">→</div>
            </div>
            
        </div>
        
    </div>

    <style>
    .homepage-showcase {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem 1rem;
        min-height: 100vh;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 50%, #e2e8f0 100%);
        position: relative;
    }
    
    .homepage-showcase::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 20%, rgba(138, 63, 252, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(106, 90, 205, 0.1) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }
    
    .hero-section {
        text-align: center;
        margin-bottom: 4rem;
        padding: 4rem 0;
        position: relative;
        z-index: 1;
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #64748b;
        margin: 0;
    }
    
    .navigation-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }
    
    .nav-card {
        border-radius: 24px;
        padding: 2.5rem;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1);
        border: none;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
    }
    
    /* Beautiful purple/dark gradient backgrounds for each card */
    .nav-card.primary {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
    }
    
    .nav-card.secondary {
        background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%);
        color: white;
    }
    
    .nav-card.accent {
        background: linear-gradient(135deg, #a855f7 0%, #d946ef 100%);
        color: white;
    }
    
    .nav-card.warm {
        background: linear-gradient(135deg, #d946ef 0%, #ec4899 100%);
        color: white;
    }
    
    .nav-card.cool {
        background: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%);
        color: white;
    }
    
    .nav-card.info {
        background: linear-gradient(135deg, #06b6d4 0%, #10b981 100%);
        color: white;
    }
    
    .nav-card:hover {
        transform: translateY(-12px) scale(1.02);
        box-shadow: 0 24px 64px rgba(0, 0, 0, 0.25);
    }
    
    .card-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .nav-card h3 {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0 0 0.75rem 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .nav-card p {
        margin: 0 0 1.5rem 0;
        line-height: 1.6;
        font-size: 1rem;
        opacity: 0.95;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    }
    
    /* All cards have consistent white text */
    
    .card-arrow {
        position: absolute;
        bottom: 1.5rem;
        right: 2rem;
        font-size: 1.5rem;
        opacity: 0;
        transform: translateX(-10px);
        transition: all 0.3s ease;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .nav-card:hover .card-arrow {
        opacity: 1;
        transform: translateX(0);
    }
    
    /* All arrows have consistent white color */
    
    @media (max-width: 768px) {
        .navigation-grid {
            grid-template-columns: 1fr;
        }
        
        .hero-title {
            font-size: 2rem;
        }
        
        .nav-card {
            padding: 1.5rem;
        }
    }
    </style>

.. toctree::
   :maxdepth: 2
   :caption: Contents
   :hidden:

   introduction/index
   guides/index
   examples/index
   api/haive/index
   agents/gallery
   tools/index
   games/index
   reference/index

Quick Links
-----------

- :doc:`api/haive/core/index` - Core infrastructure
- :doc:`api/haive/agents/index` - Agent implementations
- :doc:`api/haive/tools/index` - Tool integrations
- :ref:`genindex` - Complete index
- :ref:`modindex` - Module index
- :ref:`search` - Search documentation

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
