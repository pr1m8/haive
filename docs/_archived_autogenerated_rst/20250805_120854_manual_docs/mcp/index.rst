.. title:: MCP (Model Context Protocol) Integration
.. _mcp:

🔌 MCP Integration



   <div class="agent-hero-section">

   <div class="hero-content">
   <h2>🚀 Connect Claude to Your World</h2>
   <p class="hero-description">
   Model Context Protocol (MCP) enables Claude to connect to external tools and data sources, extending its capabilities beyond file editing.

   </p>
   </div>

   </div>

MCP Server Showcase



   <div class="agent-showcase">

   <div class="agent-card">

   <div class="agent-header">

   <div class="agent-emoji">🗄️</div>

   <div>
   <h3 class="agent-title">PostgreSQL Server</h3>
   <p class="agent-subtitle">Database Operations</p>
   </div>

   </div>
   <p class="agent-description">

            Direct database access for querying schemas, running SQL, analyzing performance, and managing data.

   </p>
   <ul class="agent-features">
   <li>Schema exploration</li>
   <li>SQL query execution</li>
   <li>Performance analysis</li>
   <li>Transaction management</li>
   </ul>
   <a href="#postgresql-setup" class="agent-link">Setup Guide</a>
   </div>

   <div class="agent-card">

   <div class="agent-header">

   <div class="agent-emoji">📁</div>

   <div>
   <h3 class="agent-title">Filesystem Server</h3>
   <p class="agent-subtitle">Enhanced File Operations</p>
   </div>

   </div>
   <p class="agent-description">

            Advanced file operations beyond basic editing with search, batch processing, and filesystem analysis.

   </p>
   <ul class="agent-features">
   <li>Recursive file search</li>
   <li>Batch operations</li>
   <li>Directory analysis</li>
   <li>Permission management</li>
   </ul>
   <a href="#filesystem-setup" class="agent-link">Setup Guide</a>
   </div>

   <div class="agent-card">

   <div class="agent-header">

   <div class="agent-emoji">🐙</div>

   <div>
   <h3 class="agent-title">GitHub Server</h3>
   <p class="agent-subtitle">Repository Management</p>
   </div>

   </div>
   <p class="agent-description">

            Complete GitHub integration for managing issues, pull requests, commits, and CI/CD workflows.

   </p>
   <ul class="agent-features">
   <li>Issue management</li>
   <li>PR creation & review</li>
   <li>Commit operations</li>
   <li>Actions monitoring</li>
   </ul>
   <a href="#github-setup" class="agent-link">Setup Guide</a>
   </div>

   <div class="agent-card">

   <div class="agent-header">

   <div class="agent-emoji">🌐</div>

   <div>
   <h3 class="agent-title">Puppeteer Server</h3>
   <p class="agent-subtitle">Browser Automation</p>
   </div>

   </div>
   <p class="agent-description">

            Browser automation and web scraping with screenshot capabilities and UI testing support.

   </p>
   <ul class="agent-features">
   <li>Web scraping</li>
   <li>Screenshot capture</li>
   <li>UI testing</li>
   <li>Form automation</li>
   </ul>
   <a href="#puppeteer-setup" class="agent-link">Setup Guide</a>
   </div>

   <div class="agent-card">

   <div class="agent-header">

   <div class="agent-emoji">🔍</div>

   <div>
   <h3 class="agent-title">Brave Search Server</h3>
   <p class="agent-subtitle">Web Research</p>
   </div>

   </div>
   <p class="agent-description">

            Real-time web search integration for current information, documentation lookup, and research.

   </p>
   <ul class="agent-features">
   <li>Real-time search</li>
   <li>News aggregation</li>
   <li>Documentation lookup</li>
   <li>Result filtering</li>
   </ul>
   <a href="#brave-search-setup" class="agent-link">Setup Guide</a>
   </div>

   <div class="agent-card">

   <div class="agent-header">

   <div class="agent-emoji">🐳</div>

   <div>
   <h3 class="agent-title">Docker Server</h3>
   <p class="agent-subtitle">Container Management</p>
   </div>

   </div>
   <p class="agent-description">

            Docker container management for running code in isolated environments and managing services.

   </p>
   <ul class="agent-features">
   <li>Container creation</li>
   <li>Image management</li>
   <li>Service orchestration</li>
   <li>Resource monitoring</li>
   </ul>
   <a href="#docker-setup" class="agent-link">Setup Guide</a>
   </div>

   <div class="agent-card">

   <div class="agent-header">

   <div class="agent-emoji">🧠</div>

   <div>
   <h3 class="agent-title">Memory Bank Server</h3>
   <p class="agent-subtitle">Persistent Context</p>
   </div>

   </div>
   <p class="agent-description">

            Maintain persistent context across sessions with intelligent memory management and recall.

   </p>
   <ul class="agent-features">
   <li>Context persistence</li>
   <li>Memory organization</li>
   <li>Intelligent recall</li>
   <li>Session continuity</li>
   </ul>
   <a href="#memory-bank-setup" class="agent-link">Setup Guide</a>
   </div>

   <div class="agent-card">

   <div class="agent-header">

   <div class="agent-emoji">💭</div>

   <div>
   <h3 class="agent-title">Sequential Thinking</h3>
   <p class="agent-subtitle">Complex Problem Solving</p>
   </div>

   </div>
   <p class="agent-description">

            Break down complex tasks into manageable steps with structured thinking and planning.

   </p>
   <ul class="agent-features">
   <li>Task decomposition</li>
   <li>Step-by-step planning</li>
   <li>Progress tracking</li>
   <li>Decision trees</li>
   </ul>
   <a href="#sequential-thinking-setup" class="agent-link">Setup Guide</a>
   </div>
   </div>

Quick Setup



.. code-block:: bash

   # PostgreSQL - Database operations
   claude mcp add haive-db -s user -- npx -y @modelcontextprotocol/server-postgres "postgresql://localhost/haive"

   # Filesystem - Enhanced file operations
   claude mcp add haive-files -s user -- npx -y @modelcontextprotocol/server-filesystem /home/will/Projects/haive

   # GitHub - Repository management
   claude mcp add haive-github -s user -e GITHUB_TOKEN=$GITHUB_TOKEN -- npx -y @modelcontextprotocol/server-github

   # List configured servers
   claude mcp list

   Runnable Agent Examples



   <div class="code-example-section">
   <h4>🚀 MCP with Haive Agents in 30 Seconds</h4>

.. code-block:: python

    # Code example here

   from haive.agents.react import ReactAgent
   from haive.core.engine.aug_llm import AugLLMConfig
   from langchain_mcp import MCPToolkit
   from langchain_core.tools import tool

   # 1. Database Research Agent with PostgreSQL MCP
   @tool
   def analyze_database_performance():
   """Use @haive-db to analyze database performance metrics."""
   # MCP call: @haive-db run SELECT table_name, pg_size_pretty(pg_total_relation_size(table_name)) FROM information_schema.tables
   return "Database analysis complete"

   db_agent = ReactAgent(
   name="database_analyst",
   engine=AugLLMConfig(temperature=0.1),
   tools=[analyze_database_performance]
   )

   # Usage: Agent can query database through MCP
   result = await db_agent.arun(
   "Analyze our database performance and suggest optimizations"
   )

   # 2. File Management Agent with Filesystem MCP
   @tool
   def find_code_patterns():
   """Use @haive-files to search for code patterns across the project."""
   # MCP call: @haive-files find all Python files containing "ReactAgent"
   return "Code pattern analysis complete"

   file_agent = ReactAgent(
   name="file_manager",
   engine=AugLLMConfig(),
   tools=[find_code_patterns]
   )

   # Usage: Agent can search and analyze files
   result = await file_agent.arun(
   "Find all React agents in the codebase and analyze their patterns"
   )

   # 3. DevOps Agent with GitHub MCP
   @tool
   def manage_github_workflow():
   """Use @haive-github to manage GitHub issues and PRs."""
   # MCP call: @haive-github list open issues with label "bug"
   return "GitHub workflow management complete"

   devops_agent = ReactAgent(
   name="devops_manager",
   engine=AugLLMConfig(),
   tools=[manage_github_workflow]
   )

   # Usage: Agent can manage GitHub workflows
   result = await devops_agent.arun(
   "Check for critical bugs and create a summary report"
   )

   </div>

   Advanced MCP Integration



   <div class="custom-section">
   <h3>🔗 Multi-Server Agent Workflows</h3>
   <p>Combine multiple MCP servers for powerful automation workflows.</p>

.. code-block:: python

    # Code example here

   from haive.agents.react import ReactAgent
   from haive.agents.simple import SimpleAgent
   from haive.core.engine.aug_llm import AugLLMConfig
   from langchain_core.tools import tool

   class DevOpsWorkflowAgent:
   """Complete DevOps workflow using multiple MCP servers."""

   def __init__(self):
   self.config = AugLLMConfig(temperature=0.2)

   @tool
   def check_database_health(self):
   """Check database health using PostgreSQL MCP."""
   # @haive-db run SELECT datname, state, query FROM pg_stat_activity WHERE state = 'active'
   return "Database health check complete"

   @tool
   def analyze_project_files(self):
   """Analyze project structure using Filesystem MCP."""
   # @haive-files analyze directory structure of packages/
   return "Project analysis complete"

   @tool
   def check_github_status(self):
   """Check GitHub repository status."""
   # @haive-github show workflow runs
   # @haive-github list open issues with label "critical"
   return "GitHub status check complete"

   @tool
   def run_container_tests(self):
   """Run tests in Docker containers."""
   # @haive-docker create container with test environment
   # @haive-docker run tests in isolated environment
   return "Container tests complete"

   async def run_full_workflow(self):
   """Execute complete DevOps workflow."""
   tools = [
   self.check_database_health,
   self.analyze_project_files,
   self.check_github_status,
   self.run_container_tests
   ]

   workflow_agent = ReactAgent(
   name="devops_workflow",
   engine=self.config,
   tools=tools
   )

   result = await workflow_agent.arun(
   "Run a complete system health check including database, "
   "codebase analysis, GitHub status, and container tests. "
   "Provide a comprehensive report with recommendations."
   )

   return result

   # Usage
   workflow = DevOpsWorkflowAgent()
   report = await workflow.run_full_workflow()

   </div>

   Why Use MCP?



   <div class="showcase-tabs">
   <button class="showcase-tab active">Enhanced Capabilities</button>
   <button class="showcase-tab">Real-Time Data</button>
   <button class="showcase-tab">Tool Integration</button>
   <button class="showcase-tab">Workflow Automation</button>
   </div>

   <div class="showcase-content active">
   <h3>🚀 Enhanced Capabilities</h3>
   <p>MCP extends Claude's abilities beyond text processing:</p>
   <ul>
   <li><strong>Database Access</strong>: Query and modify databases directly</li>
   <li><strong>Web Interaction</strong>: Browse, scrape, and automate web tasks</li>
   <li><strong>System Integration</strong>: Interact with Docker, Git, and more</li>
   <li><strong>Persistent Memory</strong>: Maintain context across sessions</li>
   </ul>
   </div>

   <div class="showcase-content">
   <h3>📊 Real-Time Data</h3>
   <p>Access current information and live data sources:</p>
   <ul>
   <li><strong>Web Search</strong>: Get up-to-date information from the internet</li>
   <li><strong>API Integration</strong>: Connect to external services and APIs</li>
   <li><strong>Live Monitoring</strong>: Track system metrics and performance</li>
   <li><strong>Dynamic Updates</strong>: React to changes in real-time</li>
   </ul>
   </div>

   <div class="showcase-content">
   <h3>🛠️ Tool Integration</h3>
   <p>Seamlessly integrate with your development tools:</p>
   <ul>
   <li><strong>Version Control</strong>: Full Git and GitHub integration</li>
   <li><strong>Containerization</strong>: Docker management and orchestration</li>
   <li><strong>Testing</strong>: Automated browser testing with Puppeteer</li>
   <li><strong>Deployment</strong>: CI/CD pipeline integration</li>
   </ul>
   </div>

   <div class="showcase-content">
   <h3>⚡ Workflow Automation</h3>
   <p>Automate complex workflows and repetitive tasks:</p>
   <ul>
   <li><strong>Data Processing</strong>: Batch operations on files and databases</li>
   <li><strong>Report Generation</strong>: Automated analysis and reporting</li>
   <li><strong>System Administration</strong>: Manage services and configurations</li>
   <li><strong>Integration Workflows</strong>: Connect multiple systems seamlessly</li>
   </ul>
   </div>

   Setup Guides



   .. _postgresql-setup:

   PostgreSQL Server



.. code-block:: bash

   # Basic setup
   claude mcp add haive-db -s user -- npx -y @modelcontextprotocol/server-postgres "postgresql://localhost/haive"

   # With authentication
   claude mcp add haive-db -s user -- npx -y @modelcontextprotocol/server-postgres "postgresql://username:password@localhost:5432/haive"

   # Usage examples
   @haive-db show tables
   @haive-db describe agents table
   @haive-db run SELECT * FROM agent_configurations LIMIT 10*

   .. _filesystem-setup:

   Filesystem Server



.. code-block:: bash

   # Setup with multiple directories
   claude mcp add haive-files -s user -- npx -y @modelcontextprotocol/server-filesystem \

     /home/will/Projects/haive \
     /home/will/Projects/haive/packages \
     /home/will/Projects/haive/project_docs

   # Usage examples
   @haive-files find all Python files containing "ReactAgent"
   @haive-files analyze directory structure of packages/

   .. _github-setup:

   GitHub Server



.. code-block:: bash

   # Install and configure
   npm install -g @modelcontextprotocol/server-github
   claude mcp add haive-github -s user -e GITHUB_TOKEN=$GITHUB_TOKEN -- \

     npx -y @modelcontextprotocol/server-github --owner=yourusername --repo=haive

   # Usage examples
   @haive-github list open issues with label "bug"
   @haive-github create PR from feature/new-agent to main
   @haive-github show workflow runs

   Best Practices



   <div class="best-practices">
   <h3>Security Considerations</h3>
   <ul>
   <li>Only add trusted MCP servers</li>
   <li>Use environment variables for sensitive data</li>
   <li>Limit permissions to necessary scopes</li>
   <li>Review server configurations regularly</li>
   </ul>
   </div>

   <div class="warning-section">
   <h3>Common Pitfalls</h3>
   <ul>
   <li>Not checking server connectivity before use</li>
   <li>Forgetting to set required environment variables</li>
   <li>Using incorrect connection strings</li>
   <li>Not handling server timeouts properly</li>
   </ul>
   </div>

   Troubleshooting



.. code-block:: bash

   # Check server status
   claude mcp list

   # Test connectivity
   claude mcp test haive-db

   # View logs
   claude mcp logs haive-db

   # Remove problematic server
   claude mcp remove haive-db

   # Reinstall if needed
   npm install -g @modelcontextprotocol/server-postgres

   Resources



   * ``MCP Documentation <https://modelcontextprotocol.io>_*`

``
   *` ``Available MCP Servers <https://github.com/modelcontextprotocol>_*`
``
   *` ``Claude Code MCP Guide <https://docs.anthropic.com/en/docs/claude-code/mcp>_*`
``
   *` ``Community MCP Servers <https://github.com/topics/mcp-server>_*`
``

   Navigation



   .. toctree::


   :maxdepth: 2
   :hidden:

   dynamic-mcp
   setup
   servers
   development
   troubleshooting
`
