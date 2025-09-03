haive-mcp
=========

Model Context Protocol integration for Haive framework.

Overview
--------

The ``haive-mcp`` package provides seamless integration with Model Context Protocol (MCP) servers:

- **MCP Server Discovery** - Automatic discovery and connection to MCP servers
- **Tool Integration** - Convert MCP tools to Haive-compatible tools
- **Agent Mixins** - Add MCP capabilities to any agent
- **Server Management** - Launch and manage MCP servers
- **Documentation Agent** - Query MCP server documentation

Installation
------------

.. code-block:: bash

   pip install haive-mcp

Or as part of the full framework:

.. code-block:: bash

   pip install haive

Quick Start
-----------

.. code-block:: python

   from haive.mcp.agents.mcp_agent import MCPAgent
   from haive.core.engine.aug_llm import AugLLMConfig
   
   # Create MCP-enabled agent
   agent = MCPAgent(
       name="mcp_assistant",
       engine=AugLLMConfig(),
       mcp_servers=["filesystem", "postgres"]
   )
   
   # Use MCP tools
   result = await agent.arun("List files in /home/user/documents")

MCP Components
--------------

Core Classes
^^^^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: MCPAgent
      :link: ../api/mcp/agents/mcp_agent/index
      :link-type: doc

      Main MCP-enabled agent
      
      - Auto tool discovery
      - Server management
      - Dynamic tool loading
      - Error handling

   .. grid-item-card:: MCPMixin
      :link: ../api/mcp/mixins/mcp_mixin/index
      :link-type: doc

      Add MCP to any agent
      
      - Mixin pattern
      - Tool injection
      - Server lifecycle
      - State management

Specialized Agents
^^^^^^^^^^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: DocumentationAgent
      :link: ../api/mcp/agents/documentation_agent/index
      :link-type: doc

      Query MCP docs
      
      - Server documentation
      - Tool descriptions
      - Usage examples
      - API reference

   .. grid-item-card:: IntelligentMCPAgent
      :link: ../api/mcp/agents/intelligent_mcp_agent/index
      :link-type: doc

      Smart MCP routing
      
      - Server selection
      - Tool optimization
      - Context awareness
      - Performance tuning

Server Management
^^^^^^^^^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: ServerDiscovery
      :link: ../api/mcp/discovery/server_discovery/index
      :link-type: doc

      Find MCP servers
      
      - Auto-discovery
      - Registry lookup
      - Local scanning
      - Cloud integration

   .. grid-item-card:: MCPManager
      :link: ../api/mcp/manager/index
      :link-type: doc

      Server lifecycle
      
      - Start/stop servers
      - Health monitoring
      - Resource management
      - Error recovery

Core MCP Classes
----------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.mcp.agents.mcp_agent.MCPAgent
   haive.mcp.mixins.mcp_mixin.MCPMixin
   haive.mcp.manager.MCPManager
   haive.mcp.config.MCPConfig

MCP Agents
----------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.mcp.agents.documentation_agent.DocumentationAgent
   haive.mcp.agents.intelligent_mcp_agent.IntelligentMCPAgent
   haive.mcp.agents.transferable_mcp_agent.TransferableMCPAgent
   haive.mcp.self_query_mcp_agent.SelfQueryMCPAgent
   haive.mcp.self_query_mcp_agent_v2.SelfQueryMCPAgentV2

Discovery & Management
----------------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.mcp.discovery.server_discovery.ServerDiscovery
   haive.mcp.discovery.analyzer.MCPAnalyzer
   haive.mcp.cli.mcp_manager.MCPCLIManager
   haive.mcp.launcher.MCPLauncher

MCP Tools
---------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.mcp.dynamic_mcp_tool.DynamicMCPTool
   haive.mcp.production_mcp_tool.ProductionMCPTool
   haive.mcp.tools.server_selector.ServerSelector
   haive.mcp.tools.server_tester.ServerTester

MCP Servers
-----------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.mcp.servers.dataflow_mcp_server.DataflowMCPServer
   haive.mcp.servers.http_server.HTTPMCPServer
   haive.mcp.servers.simple_http_server.SimpleHTTPServer

Complete API Reference
----------------------

For the complete API documentation with all MCP components:

.. toctree::
   :maxdepth: 3

   ../api/mcp/index

Examples
--------

Basic MCP Agent
^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.mcp.agents.mcp_agent import MCPAgent
   from haive.core.engine.aug_llm import AugLLMConfig
   
   # Create agent with MCP servers
   agent = MCPAgent(
       name="mcp_helper",
       engine=AugLLMConfig(),
       mcp_servers=["filesystem", "github", "postgres"]
   )
   
   # Use filesystem server
   result = await agent.arun("Show contents of current directory")
   
   # Use GitHub server
   result = await agent.arun("List open issues in repo myorg/myrepo")
   
   # Use PostgreSQL server
   result = await agent.arun("Show all tables in database")

Adding MCP to Existing Agent
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.agents.simple.agent import SimpleAgent
   from haive.mcp.mixins.mcp_mixin import MCPMixin
   
   # Create hybrid agent class
   class MCPSimpleAgent(MCPMixin, SimpleAgent):
       """Simple agent with MCP capabilities."""
       pass
   
   # Use the enhanced agent
   agent = MCPSimpleAgent(
       name="enhanced",
       engine=AugLLMConfig(),
       mcp_servers=["brave-search", "filesystem"]
   )
   
   result = await agent.arun("Search for Python MCP tutorials")

Server Discovery
^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.mcp.discovery.server_discovery import ServerDiscovery
   
   # Discover available servers
   discovery = ServerDiscovery()
   servers = await discovery.discover_servers()
   
   print("Available MCP servers:")
   for server in servers:
       print(f"- {server.name}: {server.description}")
       print(f"  Tools: {', '.join(server.tools)}")

Dynamic Tool Loading
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.mcp.agents.intelligent_mcp_agent import IntelligentMCPAgent
   
   # Agent that dynamically loads tools
   agent = IntelligentMCPAgent(
       name="dynamic",
       engine=AugLLMConfig()
   )
   
   # Agent discovers and uses appropriate MCP server
   result = await agent.arun("I need to analyze this CSV file: data.csv")
   # Automatically loads CSV viewer MCP server

Documentation Query
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.mcp.agents.documentation_agent import DocumentationAgent
   
   # Create documentation agent
   doc_agent = DocumentationAgent(
       name="mcp_docs",
       engine=AugLLMConfig()
   )
   
   # Query MCP documentation
   result = await doc_agent.arun(
       "How do I use the postgres MCP server to query data?"
   )

Custom MCP Server
^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.mcp.servers.http_server import HTTPMCPServer
   from fastapi import FastAPI
   
   # Create custom MCP server
   app = FastAPI()
   
   @app.post("/tools/custom_tool")
   async def custom_tool(data: dict):
       """Custom MCP tool implementation."""
       return {"result": f"Processed: {data}"}
   
   # Run as MCP server
   server = HTTPMCPServer(app=app, port=8000)
   await server.start()

Best Practices
--------------

1. **Select appropriate servers** for your use case
2. **Handle server failures** gracefully
3. **Monitor server health** in production
4. **Use discovery** for dynamic environments
5. **Cache server connections** for performance
6. **Implement proper cleanup** on shutdown

MCP Integration Guidelines
--------------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Guideline
     - Description
   * - **Server Selection**
     - Choose minimal set of required servers
   * - **Error Handling**
     - Gracefully handle server unavailability
   * - **Resource Management**
     - Properly cleanup server connections
   * - **Security**
     - Validate server sources and permissions
   * - **Performance**
     - Use connection pooling for efficiency

Available MCP Servers
---------------------

Common MCP servers that work with haive-mcp:

- **filesystem** - File system operations
- **postgres** - PostgreSQL database access
- **github** - GitHub API integration
- **brave-search** - Web search capabilities
- **sequential-thinking** - Step-by-step reasoning
- **memory** - Persistent memory storage
- **puppeteer** - Browser automation
- **slack** - Slack messaging

Related Documentation
---------------------

- :doc:`../guide/mcp` - MCP integration guide
- :doc:`../api/mcp/index` - Complete MCP API reference
- :doc:`haive-agents` - Base agent framework
- `MCP Specification <https://modelcontextprotocol.io>`_ - Official MCP docs