.. title:: Dynamic MCP Server Management
.. _dynamic-mcp:

🔄 Dynamic MCP Server Management
=================================

.. raw:: html

   .. raw:: html

   <div class="agent-hero-section">

.. raw:: html

   <div class="hero-content">
   <h2>🚀 Dynamic MCP with haive-mcp</h2>
   <p class="hero-description">
   Intelligent MCP server discovery, hot-reload capabilities, and HITL approval workflows. 
   Access 992+ pre-indexed MCP servers with AI-powered discovery and real-time installation.
   </p>
   </div>

.. raw:: html

   </div>

The haive-mcp package brings advanced dynamic capabilities to Model Context Protocol integration, 
enabling agents to automatically discover, install, and manage MCP servers based on their needs.

Key Features
------------

.. raw:: html

   .. raw:: html

   <div class="agent-showcase">

.. raw:: html

   <div class="agent-card">

.. raw:: html

   <div class="agent-header">

.. raw:: html

   <div class="agent-emoji">🔄</div>

.. raw:: html

   <div>
   <h3 class="agent-title">Hot-Reload</h3>
   <p class="agent-subtitle">Zero-downtime updates</p>
   </div>

.. raw:: html

   </div>
   <p class="agent-description">

            Add servers and refresh tools without restarting your agents. 
            Dynamic tool discovery and immediate availability.
.. raw:: html

   </p>
   <ul class="agent-features">
   <li>Add servers dynamically</li>
   <li>Refresh tools instantly</li>
   <li>No restart required</li>
   <li>Real-time updates</li>
   </ul>
   </div>

.. raw:: html

   <div class="agent-card">

.. raw:: html

   <div class="agent-header">

.. raw:: html

   <div class="agent-emoji">🤖</div>

.. raw:: html

   <div>
   <h3 class="agent-title">AI Discovery</h3>
   <p class="agent-subtitle">Intelligent server selection</p>
   </div>

.. raw:: html

   </div>
   <p class="agent-description">

            AI analyzes user requests and automatically finds the right MCP servers 
            from our database of 1,960+ pre-indexed servers.
.. raw:: html

   </p>
   <ul class="agent-features">
   <li>Capability analysis</li>
   <li>Smart recommendations</li>
   <li>1,960+ server database</li>
   <li>Context-aware selection</li>
   </ul>
   </div>

.. raw:: html

   <div class="agent-card">

.. raw:: html

   <div class="agent-header">

.. raw:: html

   <div class="agent-emoji">👤</div>

.. raw:: html

   <div>
   <h3 class="agent-title">HITL Approval</h3>
   <p class="agent-subtitle">Human-in-the-loop control</p>
   </div>

.. raw:: html

   </div>
   <p class="agent-description">

            Maintain control over server installations with flexible approval workflows. 
            Custom approval logic and enterprise-grade security.
.. raw:: html

   </p>
   <ul class="agent-features">
   <li>Custom approval callbacks</li>
   <li>Security policies</li>
   <li>Audit trails</li>
   <li>Allowlist management</li>
   </ul>
   </div>
   </div>

Quick Start
-----------

.. raw:: html

   .. raw:: html

   <div class="code-example-section">
   <h4>🚀 Auto-Discovery in 30 Seconds</h4>

.. code-block:: python

   from haive.mcp.agents import IntelligentMCPAgent
   from haive.core.engine.aug_llm import AugLLMConfig

   # Create intelligent agent with auto-discovery
   agent = IntelligentMCPAgent(
   engine=AugLLMConfig(),
   auto_discover=True,      # AI finds needed servers
   require_approval=True    # Ask before installing
   )

   await agent.setup()

   # Agent automatically discovers and installs servers!
   result = await agent.arun({
   "messages": [{
   "role": "user", 
   "content": "Search for Python tutorials and save to a file"
   }]
   })

   # Behind the scenes:
   # 1. AI detects need for web search + file operations
   # 2. Finds brave-search and filesystem servers
   # 3. Requests approval for installation
   # 4. Installs servers and gets tools
   # 5. Completes the task!

   .. raw:: html

   </div>

   Dynamic Server Management
   -------------------------

   .. raw:: html

   .. raw:: html

   <div class="custom-section">
   <h3>🔧 Hot-Reload Capabilities</h3>
   <p>Add and manage servers dynamically without restart.</p>

.. code-block:: python

   from haive.mcp.manager import MCPManager
   from haive.mcp.config import MCPServerConfig

   # Create dynamic manager
   manager = MCPManager(
   auto_health_check=True,
   health_check_interval=30.0
   )

   # Add server dynamically
   await manager.add_server("github", MCPServerConfig(
   name="github",
   transport="stdio",
   command="npx",
   args=["-y", "@modelcontextprotocol/server-github"],
   env={"GITHUB_TOKEN": token}
   ))

   # Hot-reload tools - no restart needed!
   tools = await manager.get_all_tools(refresh=True)
   print(f"Now have {len(tools)} tools available")

   # Get resources and prompts
   resources = await manager.get_resources()
   prompts = await manager.get_prompts()

   # Reload specific server
   await manager.reload_server("github")

   .. raw:: html

   </div>

   Intelligent Discovery System
   ----------------------------

   .. raw:: html

   .. raw:: html

   <div class="custom-section">
   <h3>🧠 AI-Powered Server Discovery</h3>
   <p>Let AI find the right servers for your needs.</p>

.. code-block:: python

   # Agent with built-in discovery tools
   agent = IntelligentMCPAgent(
   engine=AugLLMConfig(),
   auto_discover=True  # Enable AI discovery
   )

   # Manual discovery using built-in tools
   await agent.arun({
   "messages": [{
   "role": "user",
   "content": "Use discover_mcp_servers to find database servers"
   }]
   })

   # Install specific server
   await agent.arun({
   "messages": [{
   "role": "user", 
   "content": "Install modelcontextprotocol/server-postgres"
   }]
   })

   # Check status
   await agent.arun({
   "messages": [{
   "role": "user",
   "content": "List MCP server status and available tools"
   }]
   })

   Built-in Discovery Tools
   ~~~~~~~~~~~~~~~~~~~~~~~~

   The IntelligentMCPAgent includes these tools:

   - **discover_mcp_servers(capability)** - Find servers by capability
   - **install_mcp_server(server_name)** - Install with optional approval
   - **list_mcp_status()** - Get current server and tool status  
   - **reload_mcp_server(server_name)** - Hot-reload specific server

   .. raw:: html

   </div>

   HITL Approval Workflows
   -----------------------

   .. raw:: html

   .. raw:: html

   <div class="custom-section">
   <h3>🔒 Human-in-the-Loop Control</h3>
   <p>Maintain security and control over server installations.</p>

.. code-block:: python

   # Custom approval logic
   async def security_approval(request):
   """Custom approval with security checks."""
   server_name = request.recommendation.server_name
   capabilities = request.recommendation.capabilities

   print(f"🔔 Server Installation Request")
   print(f"Server: {server_name}")
   print(f"Reason: {request.recommendation.reason}")
   print(f"Capabilities: {', '.join(capabilities)}")

   # Security checks
   if "postgres" in server_name.lower():
   print("⚠️  Database access requested!")
   # Check against company policy
   return await check_database_policy(request)

   if "github" in server_name.lower():
   print("🐙 GitHub access requested")
   # Verify GitHub token permissions
   return await verify_github_permissions(request)

   # Auto-approve safe servers
   safe_servers = ["filesystem", "calculator", "brave-search"]
   if any(safe in server_name for safe in safe_servers):
   print("✅ Auto-approved safe server")
   return True

   # Manual approval for others
   user_input = input("Approve installation? (y/n): ")
   return user_input.lower() == 'y'

   # Agent with custom approval
   agent = IntelligentMCPAgent(
   engine=AugLLMConfig(),
   auto_discover=True,
   require_approval=True,
   approval_callback=security_approval
   )

   Enterprise Approval System
   ~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Production approval with Slack integration
   async def enterprise_approval(request):
   """Enterprise approval system with Slack notifications."""

   # Auto-approve allowlisted servers
   allowlist = ["filesystem", "calculator", "brave-search"]
   if any(server in request.recommendation.server_name for server in allowlist):
   logger.info(f"Auto-approved: {request.recommendation.server_name}")
   return True

   # Send to Slack for review
   await send_slack_approval_request(request)

   # Wait for human response
   return await wait_for_slack_approval(request.request_id)

   async def send_slack_approval_request(request):
   """Send approval request to Slack channel."""
   message = {
   "text": f"MCP Server Approval: {request.recommendation.server_name}",
   "attachments": [{
   "color": "warning",
   "fields": [
   {"title": "Server", "value": request.recommendation.server_name},
   {"title": "Reason", "value": request.recommendation.reason},
   {"title": "Capabilities", "value": ", ".join(request.recommendation.capabilities)}
   ]
   }]
   }
   # Send to Slack webhook...

   .. raw:: html

   </div>

   Multi-Agent Tool Sharing
   -------------------------

   .. raw:: html

   .. raw:: html

   <div class="custom-section">
   <h3>🤝 Agent Collaboration</h3>
   <p>Share tools and capabilities between agents.</p>

.. code-block:: python

   from haive.mcp.agents import TransferableMCPAgent

   # Create agents with different specializations
   researcher = TransferableMCPAgent(
   engine=AugLLMConfig(),
   name="researcher",
   mcp_config=research_config
   )

   writer = TransferableMCPAgent(
   engine=AugLLMConfig(), 
   name="writer",
   mcp_config=writer_config
   )

   await researcher.setup()
   await writer.setup()

   # Researcher finds information
   research_result = await researcher.arun({
   "messages": [{
   "role": "user",
   "content": "Research latest AI developments using web search"
   }]
   })

   # Transfer search tools to writer
   await researcher.transfer_tools_to_agent(
   writer, 
   tool_names=["web_search", "arxiv_search"]
   )

   # Writer can now use research tools
   article = await writer.arun({
   "messages": [{
   "role": "user",
   "content": "Write article about AI trends using web search for current info"
   }]
   })

   Workflow Orchestration
   ~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   class ResearchWorkflow:
   """Multi-agent research workflow with tool sharing."""

   async def run_research_pipeline(self, topic: str):
   # Stage 1: Research agent gathers information
   research_agent = TransferableMCPAgent(
   engine=AugLLMConfig(),
   name="researcher"
   )

   # Stage 2: Analysis agent processes data
   analysis_agent = TransferableMCPAgent(
   engine=AugLLMConfig(),
   name="analyst"
   )

   # Stage 3: Writer creates final report
   writer_agent = TransferableMCPAgent(
   engine=AugLLMConfig(),
   name="writer"
   )

   # Setup all agents
   await research_agent.setup()
   await analysis_agent.setup()
   await writer_agent.setup()

   # Research phase
   research_data = await research_agent.arun({
   "messages": [{
   "role": "user",
   "content": f"Research comprehensive information about {topic}"
   }]
   })

   # Transfer research tools to analyst
   await research_agent.transfer_tools_to_agent(
   analysis_agent,
   tool_names=["web_search", "database_query"]
   )

   # Analysis phase
   analysis_result = await analysis_agent.arun({
   "messages": [{
   "role": "user", 
   "content": f"Analyze this research data: {research_data}"
   }]
   })

   # Transfer all tools to writer
   await analysis_agent.transfer_all_tools_to_agent(writer_agent)

   # Writing phase
   final_report = await writer_agent.arun({
   "messages": [{
   "role": "user",
   "content": f"Create final report: {analysis_result}"
   }]
   })

   return final_report

   .. raw:: html

   </div>

   Common Use Cases
   ----------------

   .. raw:: html

   .. raw:: html

   <div class="showcase-tabs">
   <button class="showcase-tab active">Research Assistant</button>
   <button class="showcase-tab">Data Analyst</button>
   <button class="showcase-tab">DevOps Automation</button>
   <button class="showcase-tab">Content Creation</button>
   </div>

   .. raw:: html

   <div class="showcase-content active">
   <h3>🔍 Research Assistant</h3>
   <p>Automatically install search and file tools for research tasks.</p>

.. code-block:: python

   

      # Research agent with auto-discovery
      research_agent = IntelligentMCPAgent(
          engine=AugLLMConfig(),
          auto_discover=True,
          require_approval=True
      )

   

      # Agent automatically installs needed servers
      result = await research_agent.arun({
          "messages": [{
              "role": "user",
              "content": """
              Research quantum computing developments in 2024.
              Search multiple sources and create a comprehensive report.
              Save the report as quantum_computing_2024.md
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
          }]
      })

   

      # Auto-installs: brave-search, filesystem, possibly arxiv

   
      .. raw:: html

      </div>

      .. raw:: html

      <div class="showcase-content">
      <h3>📊 Data Analyst</h3>
      <p>Connect to databases and analysis tools dynamically.</p>

.. code-block:: python

   

      # Data analysis agent
      analyst_agent = IntelligentMCPAgent(
          engine=AugLLMConfig(),
          auto_discover=True
      )

   

      result = await analyst_agent.arun({
          "messages": [{
              "role": "user",
              "content": """
              Connect to PostgreSQL and analyze sales data.
              Create visualizations and export to Excel.
              Send summary report via email.
""""""""""""""""""""""""""""""""""""""""""""
          }]
      })

   

      # Auto-installs: postgres, excel, matplotlib, email servers

   
      .. raw:: html

      </div>

      .. raw:: html

      <div class="showcase-content">
      <h3>🛠️ DevOps Automation</h3>
      <p>Manage infrastructure and deployment pipelines.</p>

.. code-block:: python

   

      # DevOps agent
      devops_agent = IntelligentMCPAgent(
          engine=AugLLMConfig(),
          auto_discover=True
      )

   

      result = await devops_agent.arun({
          "messages": [{
              "role": "user",
              "content": """
              Check GitHub repository status.
              Run tests in Docker containers.
              Deploy to Kubernetes if tests pass.
              Update deployment status in Slack.
""""""""""""""""""""""""""""""""""""""""""""""""
          }]
      })

   

      # Auto-installs: github, docker, kubernetes, slack servers

   
      .. raw:: html

      </div>

      .. raw:: html

      <div class="showcase-content">
      <h3>📝 Content Creation</h3>
      <p>Research, write, and publish content automatically.</p>

.. code-block:: python

   

      # Content creation agent
      content_agent = IntelligentMCPAgent(
          engine=AugLLMConfig(),
          auto_discover=True
      )

   

      result = await content_agent.arun({
          "messages": [{
              "role": "user",
              "content": """
              Research latest Python features.
              Write a blog post with code examples.
              Create social media posts.
              Schedule publication on WordPress.
""""""""""""""""""""""""""""""""""""""""""""""""
          }]
      })

   

      # Auto-installs: brave-search, github, wordpress, social-media servers

   
      .. raw:: html

      </div>

      Performance and Monitoring
      --------------------------

      .. raw:: html

      .. raw:: html

      <div class="custom-section">
      <h3>📊 Health Monitoring</h3>
      <p>Monitor server health and performance metrics.</p>

.. code-block:: python

   # Get comprehensive status
   manager = MCPManager(auto_health_check=True)

   # Check all servers
   status = manager.get_all_server_status()
   print(f"Connected servers: {status['summary']['connected_servers']}")
   print(f"Failed servers: {status['summary']['failed_servers']}")
   print(f"Total tools: {status['summary']['total_tools']}")

   # Check specific server
   postgres_status = manager.get_server_status("postgres")
   if postgres_status:
   print(f"Status: {postgres_status.name}")
   print(f"Response time: {postgres_status.response_time}ms")

   # Retry failed servers
   retry_results = await manager.retry_failed_servers()
   for result in retry_results:
   if result.success:
   print(f"✅ Recovered: {result.server_name}")
   else:
   print(f"❌ Still failed: {result.server_name} - {result.error_message}")

   Metrics and Logging
   ~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   from haive.mcp.manager import MCPManager

   # Enable debug logging
   logging.getLogger("haive.mcp").setLevel(logging.DEBUG)

   # Create manager with detailed monitoring
   manager = MCPManager(
   auto_health_check=True,
   health_check_interval=30.0,
   max_retry_attempts=3,
   connection_timeout=10.0
   )

   # Monitor health continuously
   async def monitor_health():
   while True:
   status = manager.get_all_server_status()

   # Log health metrics
   logger.info(
   f"MCP Health: Connected={status['summary']['connected_servers']}, "
   f"Failed={status['summary']['failed_servers']}, "
   f"Tools={status['summary']['total_tools']}"
   )

   # Alert on failures
   if status['summary']['failed_servers'] > 0:
   await alert_on_failure(status)

   await asyncio.sleep(60)

   .. raw:: html

   </div>

   Best Practices
   --------------

   .. raw:: html

   .. raw:: html

   <div class="best-practices">
   <h3>🚀 Development Best Practices</h3>
   <ul>
   <li><strong>Start with auto-discovery</strong> for exploration and prototyping</li>
   <li><strong>Use static configs</strong> for production environments</li>
   <li><strong>Implement proper approval logic</strong> for security</li>
   <li><strong>Monitor server health</strong> continuously</li>
   <li><strong>Use environment variables</strong> for sensitive data</li>
   <li><strong>Handle errors gracefully</strong> with retry logic</li>
   </ul>
   </div>

   .. raw:: html

   <div class="warning-section">
   <h3>⚠️ Security Considerations</h3>
   <ul>
   <li>Only install trusted MCP servers</li>
   <li>Review server permissions carefully</li>
   <li>Use allowlists for production environments</li>
   <li>Implement audit logging for installations</li>
   <li>Regularly review installed servers</li>
   </ul>
   </div>

   Production Deployment
   ~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Production configuration
   from haive.mcp.config import MCPConfig, MCPServerConfig

   production_config = MCPConfig(

       enabled=True,
       auto_discover=False,  # Disable auto-discovery in production
       servers={
           "postgres": MCPServerConfig(
               name="postgres",
               transport="stdio", 
               command="npx",
               args=["-y", "@modelcontextprotocol/server-postgres"],
               env={"DATABASE_URL": os.getenv("DATABASE_URL")}
           ),
           "github": MCPServerConfig(
               name="github",
               transport="stdio",
               command="npx", 
               args=["-y", "@modelcontextprotocol/server-github"],
               env={"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")}
           )
       },
       retry_attempts=5,
       timeout=60

   )

   # Production agent
   production_agent = MCPAgent(

       engine=AugLLMConfig(),
       mcp_config=production_config

   )

   Integration with Static MCP
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Hybrid approach: Static base + dynamic additions
   base_config = MCPConfig(

       servers={
           "postgres": postgres_config,
           "github": github_config
       }

   )

   # Start with static configuration
   agent = IntelligentMCPAgent(

       engine=AugLLMConfig(),
       mcp_config=base_config,    # Static base
       auto_discover=True,        # Dynamic additions
       require_approval=True      # Controlled expansion

   )

   # Agent has static servers + can add more dynamically

   Next Steps
   ----------

   - **Explore**: Try the auto-discovery features
   - **Experiment**: Create custom approval workflows  
   - **Scale**: Move to production with static configs
   - **Monitor**: Implement health monitoring
   - **Contribute**: Add more servers to the database

   .. toctree::

   :maxdepth: 2
   :hidden:

   setup
   servers
   development
   troubleshooting
