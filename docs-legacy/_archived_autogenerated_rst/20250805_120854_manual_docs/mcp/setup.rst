.. title:: MCP Setup and Configuration
.. _mcp-setup:

⚙️ MCP Setup and Configuration



   <div class="agent-hero-section">

   <div class="hero-content">
   <h2>🛠️ Complete MCP Setup Guide</h2>
   <p class="hero-description">
   Step-by-step guide to configure MCP servers for development and production environments.
   From basic setup to advanced enterprise configurations.

   </p>
   </div>

   </div>

Comprehensive guide for setting up Model Context Protocol integration with detailed
configuration examples and best practices.

Prerequisites



   <div class="custom-section">
   <h3>📋 System Requirements</h3>
   <p>Ensure your system meets the requirements for MCP integration.</p>

   **Required Software:**

.. code-block:: bash

   # Python 3.12+ (recommended)
   python --version  # Should be 3.12+

   # Node.js (for MCP servers)
   node --version     # Should be 18+
   npm --version      # Should be 9+

   # Claude Code (for direct MCP usage)
   claude --version   # Latest version

   **Installation:**

.. code-block:: bash

   # Install Node.js (if not installed)
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash
------------------------------------------------------------------
   sudo apt-get install -y nodejs

   # Install Claude Code (if not installed)
   curl -fsSL https://claude.ai/install.sh | sh

   # Install haive-mcp
   poetry add haive-mcp

   </div>

   Quick Setup Methods



   <div class="showcase-tabs">
   <button class="showcase-tab active">Dynamic Discovery</button>
   <button class="showcase-tab">Direct MCP Commands</button>
   <button class="showcase-tab">Static Configuration</button>
   <button class="showcase-tab">Hybrid Approach</button>
   </div>

   <div class="showcase-content active">
   <h3>🤖 Dynamic Discovery Setup</h3>
   <p>Let AI automatically find and install servers based on your needs.</p>

.. code-block:: python

    # Code example here

      from haive.mcp.agents import IntelligentMCPAgent
      from haive.core.engine.aug_llm import AugLLMConfig



      # Create agent with auto-discovery
      agent = IntelligentMCPAgent(
          engine=AugLLMConfig(),
          auto_discover=True,      # Enable AI discovery
          require_approval=True    # Require approval for installs
      )



      await agent.setup()



      # Agent automatically discovers and installs servers!
      result = await agent.arun({
          "messages": [{
              "role": "user",
              "content": "Connect to PostgreSQL and analyze user data"
          }]
      })
      # Auto-installs postgres server if approved!



  **Benefits:**
      - Zero manual configuration
      - AI selects appropriate servers
      - Handles complex requirements automatically
      - Great for exploration and prototyping

      </div>

      <div class="showcase-content">
      <h3>📡 Direct MCP Commands</h3>
      <p>Use Claude Code MCP commands for direct server management.</p>

.. code-block:: bash



      # PostgreSQL - Database operations
      claude mcp add haive-db -s user -- npx -y @modelcontextprotocol/server-postgres "postgresql://localhost/haive"



      # Filesystem - Enhanced file operations
      claude mcp add haive-files -s user -- npx -y @modelcontextprotocol/server-filesystem /home/user/project



      # GitHub - Repository management
      claude mcp add haive-github -s user -e GITHUB_TOKEN=$GITHUB_TOKEN -- npx -y @modelcontextprotocol/server-github



      # Web search - Information retrieval
      claude mcp add brave-search -s user -e BRAVE_API_KEY=$BRAVE_API_KEY -- npx -y @modelcontextprotocol/server-brave-search



      # Browser automation - Web testing
      claude mcp add haive-browser -s user -- npx -y @modelcontextprotocol/server-puppeteer



      # List all configured servers
      claude mcp list


      **Benefits:**
      - Direct control over installations
      - Immediate availability
      - Easy to script and automate
      - Works with any MCP-compatible tool

      </div>

      <div class="showcase-content">
      <h3>⚙️ Static Configuration</h3>
      <p>Define servers in configuration files for production environments.</p>

.. code-block:: python

    # Code example here

      from haive.mcp.config import MCPConfig, MCPServerConfig
      from haive.mcp.agents import MCPAgent



      # Production configuration
      production_config = MCPConfig(
          enabled=True,
          auto_discover=False,  # Disable auto-discovery
          servers={
              "postgres": MCPServerConfig(
                  name="postgres",
                  transport="stdio",
                  command="npx",
                  args=["-y", "@modelcontextprotocol/server-postgres"],
                  env={"DATABASE_URL": "postgresql://user:pass@localhost/db"}
              ),
              "github": MCPServerConfig(
                  name="github",
                  transport="stdio",
                  command="npx",
                  args=["-y", "@modelcontextprotocol/server-github"],
                  env={"GITHUB_TOKEN": "your_token"}
              ),
              "filesystem": MCPServerConfig(
                  name="filesystem",
                  transport="stdio",
                  command="npx",
                  args=["-y", "@modelcontextprotocol/server-filesystem"],
                  env={"ALLOWED_DIRS": "/app/data,/app/output"}
              )
          },
          retry_attempts=3,
          timeout=30
      )



      # Agent with static configuration
      agent = MCPAgent(
          engine=AugLLMConfig(),
          mcp_config=production_config
      )



      await agent.setup()



  **Benefits:**
      - Predictable behavior
      - Version control friendly
      - Production ready
      - Security auditable

      </div>

      <div class="showcase-content">
      <h3>🔀 Hybrid Approach</h3>
      <p>Combine static base configuration with dynamic discovery.</p>

.. code-block:: python

    # Code example here

      # Base configuration with essential servers
      base_config = MCPConfig(
          servers={
              "postgres": MCPServerConfig(
                  name="postgres",
                  transport="stdio",
                  command="npx",
                  args=["-y", "@modelcontextprotocol/server-postgres"],
                  env={"DATABASE_URL": os.getenv("DATABASE_URL")}
              ),
              "filesystem": MCPServerConfig(
                  name="filesystem",
                  transport="stdio",
                  command="npx",
                  args=["-y", "@modelcontextprotocol/server-filesystem"],
                  env={"ALLOWED_DIRS": "/app/data"}
              )
          }
      )



      # Agent with base config + dynamic discovery
      agent = IntelligentMCPAgent(
          engine=AugLLMConfig(),
          mcp_config=base_config,    # Static base
          auto_discover=True,        # Dynamic additions
          require_approval=True      # Controlled expansion
      )



      await agent.setup()



  **Benefits:**
      - Reliable core functionality
      - Flexible expansion
      - Controlled growth
      - Best of both worlds

      </div>

      Environment Configuration



      <div class="custom-section">
      <h3>🌍 Environment-Specific Settings</h3>
      <p>Configure MCP for different environments and use cases.</p>

      Development Environment



.. code-block:: python

    # Code example here

   # Development configuration
   dev_config = MCPConfig(
   enabled=True,
   auto_discover=True,        # Enable discovery for exploration
   lazy_init=True,           # Delay initialization
   servers={
   "postgres": MCPServerConfig(
   name="postgres",
   transport="stdio",
   command="npx",
   args=["-y", "@modelcontextprotocol/server-postgres"],
   env={"DATABASE_URL": "postgresql://localhost/haive_dev"}
   ),
   "filesystem": MCPServerConfig(
   name="filesystem",
   transport="stdio",
   command="npx",
   args=["-y", "@modelcontextprotocol/server-filesystem"],
   env={"ALLOWED_DIRS": "/home/user/dev/haive"}
   )
   },
   retry_attempts=2,
   timeout=10
   )

   # Development agent
   dev_agent = IntelligentMCPAgent(
   engine=AugLLMConfig(temperature=0.7),
   mcp_config=dev_config,
   auto_discover=True,
   require_approval=False  # Auto-approve for dev
   )

   Staging Environment



.. code-block:: python

    # Code example here

   # Staging configuration
   staging_config = MCPConfig(
   enabled=True,
   auto_discover=False,      # Disable discovery for stability
   servers={
   "postgres": MCPServerConfig(
   name="postgres",
   transport="stdio",
   command="npx",
   args=["-y", "@modelcontextprotocol/server-postgres"],
   env={
   "DATABASE_URL": os.getenv("STAGING_DATABASE_URL"),
   "SSL_MODE": "require"
   }
   ),
   "github": MCPServerConfig(
   name="github",
   transport="stdio",
   command="npx",
   args=["-y", "@modelcontextprotocol/server-github"],
   env={
   "GITHUB_TOKEN": os.getenv("STAGING_GITHUB_TOKEN"),
   "GITHUB_OWNER": "staging-org"
   }
   )
   },
   retry_attempts=3,
   timeout=30
   )

   Production Environment



.. code-block:: python

    # Code example here

   # Production configuration
   production_config = MCPConfig(
   enabled=True,
   auto_discover=False,      # Never auto-discover in production
   servers={
   "postgres": MCPServerConfig(
   name="postgres",
   transport="stdio",
   command="npx",
   args=["-y", "@modelcontextprotocol/server-postgres"],
   env={
   "DATABASE_URL": os.getenv("DATABASE_URL"),
   "SSL_MODE": "require",
   "POOL_SIZE": "20"
   }
   ),
   "redis": MCPServerConfig(
   name="redis",
   transport="stdio",
   command="npx",
   args=["-y", "@modelcontextprotocol/server-redis"],
   env={
   "REDIS_URL": os.getenv("REDIS_URL"),
   "REDIS_TLS": "true"
   }
   )
   },
   retry_attempts=5,
   timeout=60
   )

   # Production agent with strict approval
   production_agent = MCPAgent(
   engine=AugLLMConfig(temperature=0.1),
   mcp_config=production_config
   )

   </div>

   Server-Specific Setup



   <div class="server-setup-grid">

   .. _postgresql-setup:

   PostgreSQL Server Setup



   <div class="server-setup-card">
   <h4>🗄️ PostgreSQL Configuration</h4>

   <div class="server-badges">
   <span class="status-badge stable">Stable</span>
   <span class="status-badge official">Official</span>
   </div>

   **Basic Setup:**

.. code-block:: bash

   # Local database
   claude mcp add haive-db -s user -- npx -y @modelcontextprotocol/server-postgres "postgresql://localhost/haive"

   # With authentication
   claude mcp add haive-db -s user -- npx -y @modelcontextprotocol/server-postgres "postgresql://user:pass@localhost:5432/haive"

   # With SSL
   claude mcp add haive-db -s user -- npx -y @modelcontextprotocol/server-postgres "postgresql://user:pass@localhost:5432/haive?sslmode=require"

   **Configuration Options:**

.. code-block:: python

    # Code example here

   postgres_config = MCPServerConfig(

       name="postgres",
       transport="stdio",
       command="npx",
       args=["-y", "@modelcontextprotocol/server-postgres"],
       env={
           "DATABASE_URL": "postgresql://user:pass@localhost/haive",
           "SSL_MODE": "require",
           "POOL_SIZE": "10",
           "TIMEOUT": "30"
       }

   )

   **Connection String Formats:**

.. code-block:: bash

   # Local
   postgresql://localhost/database

   # With auth
   postgresql://user:password@localhost:5432/database

   # With SSL
   postgresql://user:password@localhost:5432/database?sslmode=require

   # Production
   postgresql://user:password@prod-server:5432/database?sslmode=require&pool_size=20

   **Testing:**

.. code-block:: bash

   # Test connection
   claude mcp test haive-db

   # Manual query
   @haive-db show tables
   @haive-db describe users
   @haive-db run SELECT version()

   </div>

   .. _filesystem-setup:

   Filesystem Server Setup



   <div class="server-setup-card">
   <h4>📁 Filesystem Configuration</h4>

   <div class="server-badges">
   <span class="status-badge stable">Stable</span>
   <span class="status-badge official">Official</span>
   </div>

   **Basic Setup:**

.. code-block:: bash

   # Single directory
   claude mcp add haive-files -s user -- npx -y @modelcontextprotocol/server-filesystem /path/to/project

   # Multiple directories
   claude mcp add haive-files -s user -- npx -y @modelcontextprotocol/server-filesystem \

     /home/user/project \
     /home/user/documents \
     /home/user/data

   **Security Configuration:**

.. code-block:: python

    # Code example here

   filesystem_config = MCPServerConfig(

       name="filesystem",
       transport="stdio",
       command="npx",
       args=["-y", "@modelcontextprotocol/server-filesystem"],
       env={
           "ALLOWED_DIRS": "/app/data,/app/output",
           "READ_ONLY": "false",
           "MAX_FILE_SIZE": "10MB",
           "BLOCKED_EXTENSIONS": ".exe,.bat,.sh"
       }

   )

   **Usage Examples:**

.. code-block:: bash

   # File operations
   @haive-files find all Python files containing "ReactAgent"
   @haive-files analyze directory structure of packages/
   @haive-files search for "TODO" in all files
   @haive-files create directory output/reports

   </div>

   .. _github-setup:

   GitHub Server Setup



   <div class="server-setup-card">
   <h4>🐙 GitHub Configuration</h4>

   <div class="server-badges">
   <span class="status-badge stable">Stable</span>
   <span class="status-badge official">Official</span>
   </div>

   **Prerequisites:**

.. code-block:: bash

   # Install globally first
   npm install -g @modelcontextprotocol/server-github

   # Get GitHub token from: https://github.com/settings/tokens
   # Required scopes: repo, read:org, read:user

   **Basic Setup:**

.. code-block:: bash

   # Single repository
   claude mcp add haive-github -s user -e GITHUB_TOKEN=$GITHUB_TOKEN -- \

     npx -y @modelcontextprotocol/server-github --owner=yourusername --repo=yourrepo

   # Organization access
   claude mcp add haive-github -s user -e GITHUB_TOKEN=$GITHUB_TOKEN -- \

     npx -y @modelcontextprotocol/server-github --owner=yourorg

   **Configuration Options:**

.. code-block:: python

    # Code example here

   github_config = MCPServerConfig(

       name="github",
       transport="stdio",
       command="npx",
       args=["-y", "@modelcontextprotocol/server-github"],
       env={
           "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
           "GITHUB_OWNER": "your-org",
           "GITHUB_REPO": "your-repo",
           "GITHUB_API_URL": "https://api.github.com"  # Or enterprise
       }

   )

   **Usage Examples:**

.. code-block:: bash

   # Issue management
   @haive-github list open issues with label "bug"
   @haive-github create issue "Bug in authentication" --label bug

   # Pull requests
   @haive-github create PR from feature/new-auth to main
   @haive-github list PR reviews

   # Repository info
   @haive-github show workflow runs
   @haive-github get repository statistics

   </div>

   .. _brave-search-setup:

   Brave Search Server Setup



   <div class="server-setup-card">
   <h4>🔍 Brave Search Configuration</h4>

   <div class="server-badges">
   <span class="status-badge stable">Stable</span>
   <span class="status-badge official">Official</span>
   </div>

   **Prerequisites:**

.. code-block:: bash

   # Get API key from: https://api.search.brave.com/
   # Sign up for free tier or paid plan

   **Basic Setup:**

.. code-block:: bash

   # Standard search
   claude mcp add brave-search -s user -e BRAVE_API_KEY=$BRAVE_API_KEY -- \

     npx -y @modelcontextprotocol/server-brave-search

   # With custom options
   claude mcp add brave-search -s user -e BRAVE_API_KEY=$BRAVE_API_KEY -- \

     npx -y @modelcontextprotocol/server-brave-search --max-results 20 --safe-search moderate

   **Configuration Options:**

.. code-block:: python

    # Code example here

   brave_config = MCPServerConfig(

       name="brave_search",
       transport="stdio",
       command="npx",
       args=["-y", "@modelcontextprotocol/server-brave-search"],
       env={
           "BRAVE_API_KEY": os.getenv("BRAVE_API_KEY"),
           "MAX_RESULTS": "10",
           "SAFE_SEARCH": "moderate",
           "COUNTRY": "US",
           "LANGUAGE": "en"
       }

   )

   **Usage Examples:**

.. code-block:: bash

   # Web search
   @brave-search latest Python 3.12 features
   @brave-search "machine learning tutorials" site:python.org

   # News search
   @brave-search AI developments 2024 --type news

   # Academic search
   @brave-search quantum computing research --type academic

   </div>

   </div>

   Advanced Configuration



   <div class="custom-section">
   <h3>🔧 Advanced Setup Options</h3>
   <p>Enterprise-grade configuration and security settings.</p>

   Configuration Scopes



.. code-block:: bash

   # Local scope (default) - current project only
   claude mcp add server-name -s local -- server-command

   # Project scope - shared with team via .mcp.json
   claude mcp add server-name -s project -- server-command

   # User scope - available across all projects
   claude mcp add server-name -s user -- server-command

   Security Configuration



.. code-block:: python

    # Code example here

   # Security-focused configuration
   secure_config = MCPConfig(
   enabled=True,
   auto_discover=False,      # Never auto-discover
   servers={
   "postgres": MCPServerConfig(
   name="postgres",
   transport="stdio",
   command="npx",
   args=["-y", "@modelcontextprotocol/server-postgres"],
   env={
   "DATABASE_URL": os.getenv("DATABASE_URL"),
   "SSL_MODE": "require",
   "SSL_CERT": "/path/to/cert.pem",
   "SSL_KEY": "/path/to/key.pem",
   "SSL_CA": "/path/to/ca.pem"
   }
   )
   },
   retry_attempts=3,
   timeout=30,
   # Security settings
   allowed_commands=["npx"],
   blocked_packages=["suspicious-package"],
   sandbox_mode=True
   )

   Connection Pooling



.. code-block:: python

    # Code example here

   # Connection pooling configuration
   pooled_config = MCPConfig(
   servers={
   "postgres": MCPServerConfig(
   name="postgres",
   transport="stdio",
   command="npx",
   args=["-y", "@modelcontextprotocol/server-postgres"],
   env={
   "DATABASE_URL": os.getenv("DATABASE_URL"),
   "POOL_SIZE": "20",
   "POOL_TIMEOUT": "30",
   "POOL_MAX_CONNECTIONS": "100"
   }
   )
   },
   # Manager settings
   max_connections_per_server=10,
   connection_timeout=30,
   health_check_interval=60
   )

   Load Balancing



.. code-block:: python

    # Code example here

   # Multiple server instances for load balancing
   load_balanced_config = MCPConfig(
   servers={
   "postgres_primary": MCPServerConfig(
   name="postgres_primary",
   transport="stdio",
   command="npx",
   args=["-y", "@modelcontextprotocol/server-postgres"],
   env={"DATABASE_URL": os.getenv("PRIMARY_DATABASE_URL")}
   ),
   "postgres_secondary": MCPServerConfig(
   name="postgres_secondary",
   transport="stdio",
   command="npx",
   args=["-y", "@modelcontextprotocol/server-postgres"],
   env={"DATABASE_URL": os.getenv("SECONDARY_DATABASE_URL")}
   )
   },
   # Load balancing settings
   load_balancing_strategy="round_robin",
   health_check_enabled=True,
   failover_enabled=True
   )

   </div>

   Configuration File Management



   <div class="custom-section">
   <h3>📄 Configuration Files</h3>
   <p>Manage configurations using files for different environments.</p>

   Configuration File Locations



.. code-block:: bash

   # macOS
   ~/Library/Application\ Support/Claude/claude_desktop_config.json

   # Windows
   %AppData%\Claude\claude_desktop_config.json

   # Linux
   ~/.config/claude/claude_desktop_config.json

   Example Configuration File



.. code-block:: json

   {
   "mcpServers": {
   "haive-db": {
   "command": "npx",
   "args": [
   "-y",
   "@modelcontextprotocol/server-postgres",
   "postgresql://localhost/haive"
   ]
   },
   "haive-files": {
   "command": "npx",
   "args": [
   "-y",
   "@modelcontextprotocol/server-filesystem",
   "/home/user/projects/haive"
   ]
   },
   "haive-github": {
   "command": "npx",
   "args": [
   "-y",
   "@modelcontextprotocol/server-github",
   "--owner=myorg",
   "--repo=myrepo"
   ],
   "env": {
   "GITHUB_TOKEN": "your_token_here"
   }
   }
   }
   }

   Environment-Specific Files



.. code-block:: bash

   # Development
   cp claude_desktop_config.json claude_desktop_config.dev.json

   # Staging
   cp claude_desktop_config.json claude_desktop_config.staging.json

   # Production
   cp claude_desktop_config.json claude_desktop_config.prod.json

   # Use environment-specific config
   export CLAUDE_CONFIG_FILE=claude_desktop_config.prod.json

   </div>

   Health Monitoring and Diagnostics



   <div class="custom-section">
   <h3>🏥 Health Monitoring</h3>
   <p>Monitor server health and diagnose connection issues.</p>

   Health Check Commands



.. code-block:: bash

   # Check all servers
   claude mcp list

   # Test specific server
   claude mcp test haive-db

   # View server logs
   claude mcp logs haive-db

   # Get detailed status
   claude mcp status haive-db

   Programmatic Health Monitoring



.. code-block:: python

    # Code example here

   from haive.mcp.manager import MCPManager

   # Create manager with health monitoring
   manager = MCPManager(
   auto_health_check=True,
   health_check_interval=30.0,
   max_retry_attempts=3
   )

   # Get health status
   status = manager.get_all_server_status()
   print(f"Connected servers: {status['summary']['connected_servers']}")
   print(f"Failed servers: {status['summary']['failed_servers']}")

   # Check specific server
   postgres_health = manager.get_server_health("postgres")
   if postgres_health:
   print(f"Status: {postgres_health.status}")
   print(f"Response time: {postgres_health.response_time}ms")
   print(f"Last check: {postgres_health.last_check}")

   # Retry failed servers
   retry_results = await manager.retry_failed_servers()
   for result in retry_results:
   if result.success:
   print(f"✅ Recovered: {result.server_name}")
   else:
   print(f"❌ Still failed: {result.server_name}")

   Automated Health Monitoring



.. code-block:: python

    # Code example here

   import asyncio
   import logging

   async def monitor_mcp_health(manager: MCPManager):
   """Continuous health monitoring with alerts."""
   while True:
   try:
   status = manager.get_all_server_status()

   # Log health summary
   logging.info(
   f"MCP Health: Connected={status['summary']['connected_servers']}, "
   f"Failed={status['summary']['failed_servers']}, "
   f"Tools={status['summary']['total_tools']}"
   )

   # Alert on failures
   if status['summary']['failed_servers'] > 0:
   await alert_failed_servers(status)

   # Check response times
   for server_name, server_info in status['servers'].items():
   if server_info.get('response_time', 0) > 5000:  # 5 second threshold
   logging.warning(f"Slow response from {server_name}: {server_info['response_time']}ms")

   await asyncio.sleep(60)  # Check every minute

   except Exception as e:
   logging.error(f"Health monitoring error: {e}")
   await asyncio.sleep(60)

   </div>

   Troubleshooting



   <div class="troubleshooting-section">
   <h3>🔧 Common Issues and Solutions</h3>

   **Server Not Starting:**

.. code-block:: bash

   # Check if npm/npx is available
   which npx

   # Check if server package is installed
   npm list -g @modelcontextprotocol/server-postgres

   # Reinstall if needed
   npm install -g @modelcontextprotocol/server-postgres

   **Connection Errors:**

.. code-block:: bash

   # Test basic connectivity
   claude mcp test haive-db

   # Check logs for details
   claude mcp logs haive-db

   # Verify connection string
   echo $DATABASE_URL

   **Permission Issues:**

.. code-block:: bash

   # Check file permissions
   ls -la /path/to/allowed/directory

   # Fix permissions if needed
   chmod 755 /path/to/allowed/directory

   **Environment Variables:**

.. code-block:: bash

   # Check environment variables
   echo $GITHUB_TOKEN
   echo $BRAVE_API_KEY
   echo $DATABASE_URL

   # Set if missing
   export GITHUB_TOKEN=your_token_here

   **Performance Issues:**

.. code-block:: python

    # Code example here

   # Enable debug logging
   import logging
   logging.getLogger("haive.mcp").setLevel(logging.DEBUG)

   # Check connection pool settings
   manager = MCPManager(
   connection_timeout=30.0,
   max_retry_attempts=3,
   health_check_interval=60.0
   )

   </div>

   Best Practices



   <div class="best-practices">
   <h3>✅ Setup Best Practices</h3>
   <ul>
   <li><strong>Use environment variables</strong> for sensitive data</li>
   <li><strong>Test connections</strong> before deploying</li>
   <li><strong>Monitor server health</strong> continuously</li>
   <li><strong>Use static configs</strong> for production</li>
   <li><strong>Implement proper error handling</strong></li>
   <li><strong>Document your configurations</strong></li>
   <li><strong>Use version control</strong> for config files</li>
   </ul>
   </div>

   <div class="warning-section">
   <h3>⚠️ Security Considerations</h3>
   <ul>
   <li>Never commit secrets to version control</li>
   <li>Use SSL/TLS for database connections</li>
   <li>Limit filesystem access to necessary directories</li>
   <li>Regularly rotate API keys and tokens</li>
   <li>Use least privilege access principles</li>
   <li>Audit server installations regularly</li>
   </ul>
   </div>

   Next Steps



   - **Test**: Verify your setup with simple commands
   - **Monitor**: Set up health monitoring
   - **Scale**: Add more servers as needed
   - **Secure**: Review and harden security settings
   - **Optimize**: Tune performance settings

   .. toctree::


   :maxdepth: 2
   :hidden:

   environment-config
   security-config
   performance-tuning
