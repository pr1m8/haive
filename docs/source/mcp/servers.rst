.. title:: MCP Server Directory
.. _mcp-servers:

🗄️ MCP Server Directory
=======================

   <div class="agent-hero-section">

   <div class="hero-content">
   <h2>🌟 1,960+ MCP Servers at Your Fingertips</h2>
   <p class="hero-description">
   Comprehensive directory of pre-indexed MCP servers with setup guides,
   capabilities, and integration examples. From databases to AI services.
   </p>
   </div>

   </div>

Comprehensive catalog of MCP servers categorized by functionality and use case.

Server Categories
-----------------

   <div class="agent-showcase">

   <div class="agent-card">

   <div class="agent-header">

   <div class="agent-emoji">🗄️</div>

   <div>
   <h3 class="agent-title">Database Servers</h3>
   <p class="agent-subtitle">Data storage and querying</p>
   </div>

   </div>
   <p class="agent-description">

            Connect to PostgreSQL, MySQL, SQLite, MongoDB, and other databases for data operations.
   </p>

   <div class="agent-features">
   <span class="feature-tag">PostgreSQL</span>
   <span class="feature-tag">MySQL</span>
   <span class="feature-tag">SQLite</span>
   <span class="feature-tag">MongoDB</span>
   </div>

   <a href="#database-servers" class="agent-link">View Database Servers</a>
   </div>

   <div class="agent-card">

   <div class="agent-header">

   <div class="agent-emoji">📁</div>

   <div>
   <h3 class="agent-title">Filesystem Servers</h3>
   <p class="agent-subtitle">File and directory operations</p>
   </div>

   </div>
   <p class="agent-description">

            Advanced file operations, directory analysis, and filesystem management capabilities.
   </p>

   <div class="agent-features">
   <span class="feature-tag">File Operations</span>
   <span class="feature-tag">Directory Search</span>
   <span class="feature-tag">Batch Processing</span>
   </div>

   <a href="#filesystem-servers" class="agent-link">View Filesystem Servers</a>
   </div>

   <div class="agent-card">

   <div class="agent-header">

   <div class="agent-emoji">🔍</div>

   <div>
   <h3 class="agent-title">Search Servers</h3>
   <p class="agent-subtitle">Web and data search</p>
   </div>

   </div>
   <p class="agent-description">

            Web search, academic search, and specialized search engines for information retrieval.
   </p>

   <div class="agent-features">
   <span class="feature-tag">Web Search</span>
   <span class="feature-tag">Academic Search</span>
   <span class="feature-tag">News Search</span>
   </div>

   <a href="#search-servers" class="agent-link">View Search Servers</a>
   </div>

   <div class="agent-card">

   <div class="agent-header">

   <div class="agent-emoji">🐙</div>

   <div>
   <h3 class="agent-title">Development Servers</h3>
   <p class="agent-subtitle">Software development tools</p>
   </div>

   </div>
   <p class="agent-description">

            GitHub, GitLab, Docker, and other development tools for software engineering workflows.
   </p>

   <div class="agent-features">
   <span class="feature-tag">GitHub</span>
   <span class="feature-tag">Docker</span>
   <span class="feature-tag">Git</span>
   </div>

   <a href="#development-servers" class="agent-link">View Development Servers</a>
   </div>

   <div class="agent-card">

   <div class="agent-header">

   <div class="agent-emoji">🌐</div>

   <div>
   <h3 class="agent-title">Web Servers</h3>
   <p class="agent-subtitle">Web automation and scraping</p>
   </div>

   </div>
   <p class="agent-description">

            Browser automation, web scraping, and web testing with Puppeteer and Playwright.
   </p>

   <div class="agent-features">
   <span class="feature-tag">Puppeteer</span>
   <span class="feature-tag">Playwright</span>
   <span class="feature-tag">Scraping</span>
   </div>

   <a href="#web-servers" class="agent-link">View Web Servers</a>
   </div>

   <div class="agent-card">

   <div class="agent-header">

   <div class="agent-emoji">📊</div>

   <div>
   <h3 class="agent-title">Analytics Servers</h3>
   <p class="agent-subtitle">Data analysis and visualization</p>
   </div>

   </div>
   <p class="agent-description">

            Data analysis, visualization, and reporting tools for business intelligence.
   </p>

   <div class="agent-features">
   <span class="feature-tag">Analytics</span>
   <span class="feature-tag">Visualization</span>
   <span class="feature-tag">Reporting</span>
   </div>

   <a href="#analytics-servers" class="agent-link">View Analytics Servers</a>
   </div>
   </div>

.. _database-servers:

Database Servers
----------------

   <div class="server-category">
   <h3>🗄️ Database Connectivity</h3>
   <p>Connect to popular databases for data operations.</p>

   PostgreSQL Server
   ~~~~~~~~~~~~~~~~~

   <div class="server-card">

   <div class="server-header">
   <h4>📊 PostgreSQL MCP Server</h4>

   <div class="server-badges">
   <span class="status-badge stable">Stable</span>
   <span class="status-badge official">Official</span>
   </div>

   </div>
   <p class="server-description">

         Direct PostgreSQL database access with schema exploration, query execution, and transaction management.
   </p>

   <div class="server-details">

   <div class="detail-item">
   <strong>Package:</strong> <code>@modelcontextprotocol/server-postgres</code>
   </div>

   <div class="detail-item">
   <strong>Capabilities:</strong> Schema exploration, SQL execution, performance analysis
   </div>

   <div class="detail-item">
   <strong>Transport:</strong> stdio
   </div>

   </div>

**Setup:*

.. code-block:: bash

   # Basic setup
   claude mcp add haive-db -s user -- npx -y @modelcontextprotocol/server-postgres "postgresql://localhost/haive"

   # With authentication
   claude mcp add haive-db -s user -- npx -y @modelcontextprotocol/server-postgres "postgresql://user:pass@localhost:5432/haive"

   # With SSL
   claude mcp add haive-db -s user -- npx -y @modelcontextprotocol/server-postgres "postgresql://user:pass@localhost:5432/haive?sslmode=require"

   **Usage Examples:*

.. code-block:: python

    # Code example here

   # In haive-mcp dynamic agent
   await agent.arun({

       "messages": [{
           "role": "user",
           "content": "Connect to PostgreSQL and show all tables"
       }]

   })

   # Or use discover_mcp_servers tool
   await agent.arun({

       "messages": [{
           "role": "user",
           "content": "Find database servers and install PostgreSQL"
       }]

   })

   **Manual Usage:*

.. code-block:: bash

   # Direct MCP usage
   @haive-db show tables
   @haive-db describe users table
   @haive-db run SELECT * FROM users WHERE active = true LIMIT 10*

   </div>

   MySQL Server
   ~~~~~~~~~~~~

   <div class="server-card">

   <div class="server-header">
   <h4>🐬 MySQL MCP Server</h4>

   <div class="server-badges">
   <span class="status-badge stable">Stable</span>
   <span class="status-badge community">Community</span>
   </div>

   </div>
   <p class="server-description">

         Connect to MySQL databases with full query support and schema management.
   </p>

   **Setup:*

.. code-block:: bash

   # MySQL server setup
   claude mcp add mysql-db -s user -- npx -y @modelcontextprotocol/server-mysql "mysql://user:pass@localhost:3306/mydb"

   **Usage:*

.. code-block:: bash

   @mysql-db show databases
   @mysql-db use mydb
   @mysql-db show tables

   </div>

   SQLite Server
   ~~~~~~~~~~~~~

   <div class="server-card">

   <div class="server-header">
   <h4>📋 SQLite MCP Server</h4>

   <div class="server-badges">
   <span class="status-badge stable">Stable</span>
   <span class="status-badge official">Official</span>
   </div>

   </div>
   <p class="server-description">

         Lightweight SQLite database access for local data storage and analysis.
   </p>

   **Setup:*

.. code-block:: bash

   # SQLite server with local database
   claude mcp add sqlite-db -s user -- npx -y @modelcontextprotocol/server-sqlite "/path/to/database.db"

   **Usage:*

.. code-block:: bash

   @sqlite-db .tables
   @sqlite-db .schema users
   @sqlite-db SELECT * FROM users LIMIT 5*

   </div>

   </div>

   .. _filesystem-servers:

   Filesystem Servers
   ------------------

   <div class="server-category">
   <h3>📁 File System Operations</h3>
   <p>Advanced file and directory management capabilities.</p>

   Filesystem Server
   ~~~~~~~~~~~~~~~~~

   <div class="server-card">

   <div class="server-header">
   <h4>📁 Filesystem MCP Server</h4>

   <div class="server-badges">
   <span class="status-badge stable">Stable</span>
   <span class="status-badge official">Official</span>
   </div>

   </div>
   <p class="server-description">

         Enhanced file operations with recursive search, batch processing, and directory analysis.
   </p>

   <div class="server-details">

   <div class="detail-item">
   <strong>Package:</strong> <code>@modelcontextprotocol/server-filesystem</code>
   </div>

   <div class="detail-item">
   <strong>Capabilities:</strong> File operations, directory search, batch processing
   </div>

   <div class="detail-item">
   <strong>Transport:</strong> stdio
   </div>

   </div>

   **Setup:*

.. code-block:: bash

   # Single directory
   claude mcp add haive-files -s user -- npx -y @modelcontextprotocol/server-filesystem /home/user/project

   # Multiple directories
   claude mcp add haive-files -s user -- npx -y @modelcontextprotocol/server-filesystem \

     /home/user/project \
     /home/user/documents \
     /home/user/data

   **Usage Examples:*

.. code-block:: python

    # Code example here

   # Dynamic discovery
   await agent.arun({

       "messages": [{
           "role": "user",
           "content": "Find all Python files containing 'ReactAgent' and analyze their imports"
       }]

   })

   **Manual Usage:*

.. code-block:: bash

   # File operations
   @haive-files find all Python files containing "ReactAgent"
   @haive-files analyze directory structure of packages/
   @haive-files search for "TODO" in all files

   </div>

   </div>

   .. _search-servers:

   Search Servers
   --------------

   <div class="server-category">
   <h3>🔍 Search and Information Retrieval</h3>
   <p>Web search, academic search, and specialized search engines.</p>

   Brave Search Server
   ~~~~~~~~~~~~~~~~~~~

   <div class="server-card">

   <div class="server-header">
   <h4>🔍 Brave Search MCP Server</h4>

   <div class="server-badges">
   <span class="status-badge stable">Stable</span>
   <span class="status-badge official">Official</span>
   </div>

   </div>
   <p class="server-description">

         Real-time web search with privacy-focused results and news aggregation.
   </p>

   <div class="server-details">

   <div class="detail-item">
   <strong>Package:</strong> <code>@modelcontextprotocol/server-brave-search</code>
   </div>

   <div class="detail-item">
   <strong>Capabilities:</strong> Web search, news search, result filtering
   </div>

   <div class="detail-item">
   <strong>Requirements:</strong> Brave API Key
   </div>

   </div>

   **Setup:*

.. code-block:: bash

   # Get API key from https://api.search.brave.com/
   claude mcp add brave-search -s user -e BRAVE_API_KEY=your_api_key -- \

     npx -y @modelcontextprotocol/server-brave-search

   **Usage:*

.. code-block:: python

    # Code example here

   # Auto-discovery
   await agent.arun({

       "messages": [{
           "role": "user",
           "content": "Search for latest Python 3.12 features and summarize"
       }]

   })

   **Manual Usage:*

.. code-block:: bash

   @brave-search latest Python 3.12 features
   @brave-search Python async programming tutorial

   </div>

   Google Search Server
   ~~~~~~~~~~~~~~~~~~~~

   <div class="server-card">

   <div class="server-header">
   <h4>🔍 Google Search MCP Server</h4>

   <div class="server-badges">
   <span class="status-badge community">Community</span>
   </div>

   </div>
   <p class="server-description">

         Google Custom Search integration for web search capabilities.
   </p>

   **Setup:*

.. code-block:: bash

   # Google Custom Search
   claude mcp add google-search -s user -e GOOGLE_API_KEY=your_key -e GOOGLE_CSE_ID=your_cse_id -- \

     npx -y mcp-server-google-search

   </div>

   </div>

   .. _development-servers:

   Development Servers
   -------------------

   <div class="server-category">
   <h3>🐙 Software Development Tools</h3>
   <p>Integration with development platforms and tools.</p>

   GitHub Server
   ~~~~~~~~~~~~~

   <div class="server-card">

   <div class="server-header">
   <h4>🐙 GitHub MCP Server</h4>

   <div class="server-badges">
   <span class="status-badge stable">Stable</span>
   <span class="status-badge official">Official</span>
   </div>

   </div>
   <p class="server-description">

         Complete GitHub integration for repository management, issues, pull requests, and CI/CD.
   </p>

   <div class="server-details">

   <div class="detail-item">
   <strong>Package:</strong> <code>@modelcontextprotocol/server-github</code>
   </div>

   <div class="detail-item">
   <strong>Capabilities:</strong> Issue management, PR operations, commit history
   </div>

   <div class="detail-item">
   <strong>Requirements:</strong> GitHub Token
   </div>

   </div>

   **Setup:*

.. code-block:: bash

   # Install globally first
   npm install -g @modelcontextprotocol/server-github

   # Configure with repository
   claude mcp add haive-github -s user -e GITHUB_TOKEN=$GITHUB_TOKEN -- \

     npx -y @modelcontextprotocol/server-github --owner=yourusername --repo=yourrepo

   **Usage:*

.. code-block:: python

    # Code example here

   # Auto-discovery
   await agent.arun({

       "messages": [{
           "role": "user",
           "content": "Check my GitHub repos for open issues labeled 'bug'"
       }]

   })

   **Manual Usage:*

.. code-block:: bash

   @haive-github list open issues with label "bug"
   @haive-github create PR from feature/new-feature to main
   @haive-github show workflow runs

   </div>

   Docker Server
   ~~~~~~~~~~~~~

   <div class="server-card">

   <div class="server-header">
   <h4>🐳 Docker MCP Server</h4>

   <div class="server-badges">
   <span class="status-badge stable">Stable</span>
   <span class="status-badge official">Official</span>
   </div>

   </div>
   <p class="server-description">

         Docker container management for isolated code execution and service orchestration.
   </p>

   **Setup:*

.. code-block:: bash

   # Docker server
   claude mcp add haive-docker -s user -- npx -y @modelcontextprotocol/server-docker

   **Usage:*

.. code-block:: python

    # Code example here

   # Auto-discovery
   await agent.arun({

       "messages": [{
           "role": "user",
           "content": "Run Python tests in a Docker container"
       }]

   })

   **Manual Usage:*

.. code-block:: bash

   @haive-docker list containers
   @haive-docker run python:3.12 python -c "print('Hello from Docker')"

   </div>

   </div>

   .. _web-servers:

   Web Servers
   -----------

   <div class="server-category">
   <h3>🌐 Web Automation and Scraping</h3>
   <p>Browser automation, web scraping, and testing tools.</p>

   Puppeteer Server
   ~~~~~~~~~~~~~~~~

   <div class="server-card">

   <div class="server-header">
   <h4>🌐 Puppeteer MCP Server</h4>

   <div class="server-badges">
   <span class="status-badge stable">Stable</span>
   <span class="status-badge official">Official</span>
   </div>

   </div>
   <p class="server-description">

         Browser automation and web scraping with screenshot capabilities and UI testing.
   </p>

   <div class="server-details">

   <div class="detail-item">
   <strong>Package:</strong> <code>@modelcontextprotocol/server-puppeteer</code>
   </div>

   <div class="detail-item">
   <strong>Capabilities:</strong> Web scraping, screenshots, UI testing
   </div>

   <div class="detail-item">
   <strong>Transport:</strong> stdio
   </div>

   </div>

   **Setup:*

.. code-block:: bash

   # Puppeteer server
   claude mcp add haive-browser -s user -- npx -y @modelcontextprotocol/server-puppeteer

   **Usage:*

.. code-block:: python

    # Code example here

   # Auto-discovery
   await agent.arun({

       "messages": [{
           "role": "user",
           "content": "Take a screenshot of https://example.com and analyze the page"
       }]

   })

   **Manual Usage:*

.. code-block:: bash

   @haive-browser navigate to https://example.com
   @haive-browser take screenshot
   @haive-browser extract text from page

   </div>

   </div>

   .. _analytics-servers:

   Analytics Servers
   -----------------

   <div class="server-category">
   <h3>📊 Data Analysis and Visualization</h3>
   <p>Business intelligence and data analysis tools.</p>

   Memory Bank Server
   ~~~~~~~~~~~~~~~~~~

   <div class="server-card">

   <div class="server-header">
   <h4>🧠 Memory Bank MCP Server</h4>

   <div class="server-badges">
   <span class="status-badge stable">Stable</span>
   <span class="status-badge official">Official</span>
   </div>

   </div>
   <p class="server-description">

         Persistent context management with intelligent memory organization and recall.
   </p>

   **Setup:*

.. code-block:: bash

   # Memory bank server
   claude mcp add haive-memory -s user -- npx -y @modelcontextprotocol/server-memory

   **Usage:*

.. code-block:: python

    # Code example here

   # Auto-discovery
   await agent.arun({

       "messages": [{
           "role": "user",
           "content": "Remember that I prefer Python 3.12 for new projects"
       }]

   })

   </div>

   Sequential Thinking Server
   ~~~~~~~~~~~~~~~~~~~~~~~~~~

   <div class="server-card">

   <div class="server-header">
   <h4>💭 Sequential Thinking MCP Server</h4>

   <div class="server-badges">
   <span class="status-badge stable">Stable</span>
   <span class="status-badge official">Official</span>
   </div>

   </div>
   <p class="server-description">

         Complex problem solving with structured thinking and step-by-step planning.
   </p>

   **Setup:*

.. code-block:: bash

   # Sequential thinking server
   claude mcp add haive-thinking -s user -- npx -y @modelcontextprotocol/server-sequential-thinking

   **Usage:*

.. code-block:: python

    # Code example here

   # Auto-discovery
   await agent.arun({

       "messages": [{
           "role": "user",
           "content": "Break down the task of migrating from Python 3.9 to 3.12"
       }]

   })

   </div>

   </div>

   Server Discovery
   ----------------

   <div class="custom-section">
   <h3>🔍 Finding the Right Server</h3>
   <p>Use AI-powered discovery to find servers for your specific needs.</p>

.. code-block:: python

    # Code example here

   from haive.mcp.agents import IntelligentMCPAgent

   # Agent with discovery capabilities
   agent = IntelligentMCPAgent(
   engine=AugLLMConfig(),
   auto_discover=True
   )

   # Find servers by capability
   await agent.arun({
   "messages": [{
   "role": "user",
   "content": "Use discover_mcp_servers to find all database servers"
   }]
   })

   # Find servers by use case
   await agent.arun({
   "messages": [{
   "role": "user",
   "content": "Find servers for web scraping and data analysis"
   }]
   })

   # Get server recommendations
   await agent.arun({
   "messages": [{
   "role": "user",
   "content": "What servers do I need for a research assistant that can search and save files?"
   }]
   })

   Manual Server Database Access
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Code example here

   from haive.mcp.documentation import MCPDocumentationLoader

   # Load server database
   loader = MCPDocumentationLoader()
   all_servers = loader.load_all_mcp_documents()

   print(f"Found {len(all_servers)} MCP servers")  # 1,960+ servers available

   # Search by capability
   database_servers = [
   server for server in all_servers
   if "database" in server.capabilities
   ]

   # Search by category
   search_servers = [
   server for server in all_servers
   if server.category == "search"
   ]

   # Get specific server
   postgres_doc = loader.get_server_documentation(
   "modelcontextprotocol/server-postgres"
   )

   </div>

   Common Server Combinations
   --------------------------

   <div class="showcase-tabs">
   <button class="showcase-tab active">Research Stack</button>
   <button class="showcase-tab">Data Analysis</button>
   <button class="showcase-tab">DevOps Suite</button>
   <button class="showcase-tab">Web Development</button>
   </div>

   <div class="showcase-content active">
   <h3>🔍 Research Assistant Stack</h3>
   <p>Complete research workflow with search, analysis, and documentation.</p>

.. code-block:: python

    # Code example here

      # Research assistant configuration
      research_servers = {
          "brave_search": {
              "package": "@modelcontextprotocol/server-brave-search",
              "purpose": "Web search and current information"
          },
          "filesystem": {
              "package": "@modelcontextprotocol/server-filesystem",
              "purpose": "Save research documents"
          },
          "memory_bank": {
              "package": "@modelcontextprotocol/server-memory",
              "purpose": "Remember research context"
          },
          "sequential_thinking": {
              "package": "@modelcontextprotocol/server-sequential-thinking",
              "purpose": "Structured research planning"
          }
      }



      # Auto-discovery will find these automatically
      await agent.arun({
          "messages": [{
              "role": "user",
              "content": "Research AI trends in 2024 and create a comprehensive report"
          }]
      })


      </div>

      <div class="showcase-content">
      <h3>📊 Data Analysis Stack</h3>
      <p>End-to-end data analysis with databases, visualization, and reporting.</p>

.. code-block:: python

    # Code example here

      # Data analysis configuration
      analysis_servers = {
          "postgres": {
              "package": "@modelcontextprotocol/server-postgres",
              "purpose": "Database queries and analysis"
          },
          "excel": {
              "package": "@modelcontextprotocol/server-excel",
              "purpose": "Spreadsheet operations"
          },
          "matplotlib": {
              "package": "@modelcontextprotocol/server-matplotlib",
              "purpose": "Data visualization"
          },
          "filesystem": {
              "package": "@modelcontextprotocol/server-filesystem",
              "purpose": "Export reports and charts"
          }
      }


      </div>

      <div class="showcase-content">
      <h3>🛠️ DevOps Automation Suite</h3>
      <p>Complete DevOps workflow with CI/CD, containers, and monitoring.</p>

.. code-block:: python

    # Code example here

      # DevOps automation configuration
      devops_servers = {
          "github": {
              "package": "@modelcontextprotocol/server-github",
              "purpose": "Repository and CI/CD management"
          },
          "docker": {
              "package": "@modelcontextprotocol/server-docker",
              "purpose": "Container operations"
          },
          "kubernetes": {
              "package": "@modelcontextprotocol/server-kubernetes",
              "purpose": "Service orchestration"
          },
          "slack": {
              "package": "@modelcontextprotocol/server-slack",
              "purpose": "Notifications and alerts"
          }
      }


      </div>

      <div class="showcase-content">
      <h3>🌐 Web Development Stack</h3>
      <p>Full web development workflow with testing, deployment, and monitoring.</p>

.. code-block:: python

    # Code example here

      # Web development configuration
      web_servers = {
          "puppeteer": {
              "package": "@modelcontextprotocol/server-puppeteer",
              "purpose": "Browser testing and automation"
          },
          "github": {
              "package": "@modelcontextprotocol/server-github",
              "purpose": "Code repository management"
          },
          "docker": {
              "package": "@modelcontextprotocol/server-docker",
              "purpose": "Development environments"
          },
          "filesystem": {
              "package": "@modelcontextprotocol/server-filesystem",
              "purpose": "Project file management"
          }
      }


      </div>

      Installation Quick Reference

  ----------------------------

      <div class="quick-reference">
      <h3>🚀 Quick Installation Commands</h3>

      <div class="command-grid">

      **Essential Servers:*


.. code-block:: bash



      # Database access
      claude mcp add haive-db -s user -- npx -y @modelcontextprotocol/server-postgres "postgresql://localhost/haive"

      # File operations
      claude mcp add haive-files -s user -- npx -y @modelcontextprotocol/server-filesystem /path/to/project

      # Web search
      claude mcp add brave-search -s user -e BRAVE_API_KEY=$BRAVE_API_KEY -- npx -y @modelcontextprotocol/server-brave-search

      # GitHub integration
      claude mcp add haive-github -s user -e GITHUB_TOKEN=$GITHUB_TOKEN -- npx -y @modelcontextprotocol/server-github


      **Development Tools:*


.. code-block:: bash



      # Browser automation
      claude mcp add haive-browser -s user -- npx -y @modelcontextprotocol/server-puppeteer

      # Container management
      claude mcp add haive-docker -s user -- npx -y @modelcontextprotocol/server-docker

      # Memory management
      claude mcp add haive-memory -s user -- npx -y @modelcontextprotocol/server-memory


      **Management Commands:*


.. code-block:: bash



      # List all servers
      claude mcp list

      # Test server connection
      claude mcp test haive-db

      # Remove server
      claude mcp remove haive-db

      # View server logs
      claude mcp logs haive-db


      </div>

      </div>

      Contributing New Servers
      -------------------------

      <div class="custom-section">
      <h3>🤝 Contributing to the Server Database</h3>
      <p>Help expand the MCP server ecosystem by contributing new servers.</p>

.. code-block:: python

    # Code example here

   # Example: Adding a new server to the database
   from haive.mcp.documentation import MCPDocumentationLoader

   # Document new server
   new_server = {
   "name": "my-custom-server",
   "package": "@myorg/mcp-server-custom",
   "category": "analytics",
   "capabilities": ["data_analysis", "visualization"],
   "description": "Custom analytics server for specialized data processing",
   "setup_instructions": "npm install -g @myorg/mcp-server-custom",
   "config_example": {
   "transport": "stdio",
   "command": "npx",
   "args": ["-y", "@myorg/mcp-server-custom"]
   }
   }

   # Contribute to database
   loader = MCPDocumentationLoader()
   loader.add_server_documentation(new_server)

   Server Requirements
   ~~~~~~~~~~~~~~~~~~~

   To be included in the official server database, servers should:

   - Follow MCP specification
   - Include comprehensive documentation
   - Provide setup instructions
   - Have working examples
   - Include error handling
   - Support standard transports (stdio/sse)

   </div>

   Next Steps
   ----------

   - **Browse*: Explore servers by category
   - **Try*: Use auto-discovery to find servers
   - **Integrate*: Add servers to your workflows
   - **Contribute*: Submit new servers to the database
   - **Monitor*: Keep track of server performance

   .. toctree::

   :maxdepth: 2
   :hidden:

   postgres/index
   filesystem/index
   github/index
   puppeteer/index
