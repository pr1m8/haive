# MCP Integration Guide

**How to integrate dynamic MCP capabilities into your Haive agents**

## 🎯 Overview

This guide explains how to add Model Context Protocol (MCP) capabilities to your Haive agents, enabling them to dynamically discover, install, and use external tools and resources.

## 🚀 Quick Start Integration

### 1. Basic MCP Agent

The simplest way to add MCP capabilities:

```python
from haive.mcp.agents import MCPAgent
from haive.mcp.config import MCPConfig, MCPServerConfig
from haive.core.engine.aug_llm import AugLLMConfig

# Static configuration approach
config = MCPConfig(
    servers={
        "filesystem": MCPServerConfig(
            name="filesystem",
            transport="stdio",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", "/path/to/directory"]
        ),
        "github": MCPServerConfig(
            name="github",
            transport="stdio",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-github"],
            env={"GITHUB_TOKEN": "your-token"}
        )
    }
)

# Create agent with MCP capabilities
agent = MCPAgent(
    engine=AugLLMConfig(),
    mcp_config=config
)

await agent.setup()
result = await agent.arun({"messages": [{"role": "user", "content": "List files and create an issue"}]})
```

### 2. Intelligent Dynamic Agent

For automatic server discovery and installation:

```python
from haive.mcp.agents import IntelligentMCPAgent

# Dynamic discovery approach
agent = IntelligentMCPAgent(
    engine=AugLLMConfig(),
    auto_discover=True,      # Automatically find needed servers
    require_approval=True    # Ask before installing
)

await agent.setup()

# Agent analyzes request and installs appropriate servers
result = await agent.arun({
    "messages": [{
        "role": "user",
        "content": "Search for React tutorials and save to a database"
    }]
})
# Automatically installs: web-search + database servers
```

## 🔧 Integration Patterns

### Pattern 1: Extending Existing Agents

Add MCP capabilities to your existing agents:

```python
from haive.agents.simple import SimpleAgent
from haive.mcp.mixins import MCPMixin

class MyEnhancedAgent(SimpleAgent, MCPMixin):
    """Existing agent enhanced with MCP capabilities."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mcp_config = MCPConfig(servers={...})

    async def setup(self):
        await super().setup()
        await self.setup_mcp()  # From MCPMixin

    async def arun(self, input_data):
        # Access MCP tools via self.mcp_tools
        tools = await self.get_mcp_tools()
        # Use tools in your agent logic
        return await super().arun(input_data)
```

### Pattern 2: Composable MCP Agents

Build agents with specific MCP server combinations:

```python
def create_research_agent():
    """Research agent with web search and document tools."""
    config = MCPConfig(
        servers={
            "brave_search": MCPServerConfig(
                name="brave_search",
                transport="stdio",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-brave-search"],
                env={"BRAVE_API_KEY": "your-key"}
            ),
            "filesystem": MCPServerConfig(
                name="filesystem",
                transport="stdio",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-filesystem", "./research"]
            )
        }
    )

    return MCPAgent(
        engine=AugLLMConfig(temperature=0.3),
        mcp_config=config
    )

def create_database_agent():
    """Database agent with PostgreSQL and spreadsheet tools."""
    config = MCPConfig(
        servers={
            "postgres": MCPServerConfig(
                name="postgres",
                transport="stdio",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-postgres"],
                env={"DATABASE_URL": "postgresql://..."}
            ),
            "sheets": MCPServerConfig(
                name="sheets",
                transport="stdio",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-google-sheets"],
                env={"GOOGLE_SHEETS_API_KEY": "your-key"}
            )
        }
    )

    return MCPAgent(
        engine=AugLLMConfig(),
        mcp_config=config
    )
```

### Pattern 3: Hot-Reload Management

Dynamic server management during runtime:

```python
from haive.mcp.manager import MCPManager

async def dynamic_tool_management():
    """Example of runtime server management."""
    manager = MCPManager()

    # Start with basic tools
    await manager.add_server("filesystem", filesystem_config)

    # Add new capabilities based on user needs
    if user_needs_web_search:
        await manager.add_server("search", search_config)

    # Reload tools without restart
    tools = await manager.get_all_tools(refresh=True)

    # Remove unused servers
    await manager.remove_server("unused_server")

    return tools
```

## 🔍 Discovery Integration

### Automatic Server Discovery

```python
from haive.mcp.discovery import MCPServerDiscovery

async def intelligent_discovery_example():
    """Example of AI-powered server discovery."""
    discovery = MCPServerDiscovery()

    # Analyze user request for needed capabilities
    user_request = "I need to analyze data from multiple APIs and create visualizations"

    # AI-powered capability analysis
    needed_capabilities = await discovery.analyze_capability_needs(user_request)
    # Returns: ["api", "data_analysis", "visualization"]

    # Find matching servers
    recommendations = await discovery.find_servers_by_capabilities(needed_capabilities)

    # Get top recommendations
    for rec in recommendations[:3]:
        print(f"Server: {rec.server_name}")
        print(f"Capabilities: {rec.capabilities}")
        print(f"Confidence: {rec.confidence}")
        print(f"Setup: {rec.setup_instructions}")
```

### Custom Discovery Logic

```python
class CustomDiscoveryAgent(IntelligentMCPAgent):
    """Agent with custom discovery logic."""

    async def _analyze_capability_needs(self, user_message: str) -> list[str]:
        """Custom capability analysis."""
        capabilities = []

        # Domain-specific analysis
        if "spreadsheet" in user_message.lower():
            capabilities.extend(["excel", "sheets", "csv"])
        if "database" in user_message.lower():
            capabilities.extend(["sql", "postgres", "mysql"])
        if "api" in user_message.lower():
            capabilities.extend(["http", "rest", "graphql"])

        # Fallback to AI analysis
        if not capabilities:
            capabilities = await super()._analyze_capability_needs(user_message)

        return capabilities
```

## 🤝 Human-in-the-Loop Integration

### Custom Approval Workflows

```python
async def custom_approval_handler(request: HITLApprovalRequest) -> bool:
    """Custom approval logic for server installations."""

    # Log the request
    logger.info(f"Approval requested for: {request.recommendation.server_name}")

    # Auto-approve trusted servers
    trusted_servers = ["filesystem", "calculator", "weather"]
    if request.recommendation.server_name in trusted_servers:
        return True

    # Require explicit approval for others
    print(f"\n🔔 Server Installation Request:")
    print(f"Server: {request.recommendation.server_name}")
    print(f"Reason: {request.recommendation.reason}")
    print(f"Capabilities: {', '.join(request.recommendation.capabilities)}")
    print(f"Setup: {request.recommendation.setup_instructions}")

    # Your approval logic here
    response = input("\nApprove installation? (y/n/details): ").lower()

    if response == "details":
        print(f"Documentation: {request.recommendation.documentation_url}")
        response = input("Approve after review? (y/n): ").lower()

    return response == "y"

# Use custom approval handler
agent = IntelligentMCPAgent(
    engine=AugLLMConfig(),
    require_approval=True,
    approval_callback=custom_approval_handler
)
```

## 🔧 Advanced Integration

### Multi-Agent MCP Coordination

```python
from haive.agents.multi import MultiAgent

async def create_mcp_workflow():
    """Multi-agent workflow with shared MCP capabilities."""

    # Create specialized agents
    research_agent = IntelligentMCPAgent(
        name="researcher",
        engine=AugLLMConfig(),
        auto_discover=True
    )

    analysis_agent = IntelligentMCPAgent(
        name="analyst",
        engine=AugLLMConfig(),
        auto_discover=True
    )

    # Setup agents
    await research_agent.setup()
    await analysis_agent.setup()

    # Create coordinating multi-agent
    coordinator = MultiAgent(
        agents={
            "research": research_agent,
            "analysis": analysis_agent
        },
        execution_mode="sequential"
    )

    return coordinator
```

### Tool Transfer Between Agents

```python
from haive.mcp.agents import TransferableMCPAgent

async def tool_sharing_example():
    """Example of sharing tools between agents."""

    # Create agents with different capabilities
    agent1 = TransferableMCPAgent(
        engine=AugLLMConfig(),
        mcp_config=web_tools_config
    )

    agent2 = TransferableMCPAgent(
        engine=AugLLMConfig(),
        mcp_config=database_tools_config
    )

    await agent1.setup()
    await agent2.setup()

    # Share specific tools
    await agent1.transfer_tools_to_agent(
        agent2,
        tool_names=["web_search", "url_fetch"]
    )

    # Now agent2 has web tools + database tools
    return agent2
```

## 📊 Monitoring & Management

### Server Health Monitoring

```python
async def monitor_mcp_servers():
    """Monitor MCP server health."""
    manager = MCPManager()

    # Get comprehensive status
    status = manager.get_all_server_status()

    print(f"Connected servers: {status['summary']['connected_servers']}")
    print(f"Failed servers: {status['summary']['failed_servers']}")
    print(f"Total tools: {status['summary']['total_tools']}")

    # Check individual server health
    for server_name in status['servers']:
        health = await manager.check_server_health(server_name)
        print(f"{server_name}: {health.status} ({health.response_time:.2f}s)")
```

## 🚨 Error Handling

### Robust MCP Integration

```python
async def robust_mcp_agent():
    """Agent with comprehensive error handling."""

    try:
        agent = IntelligentMCPAgent(
            engine=AugLLMConfig(),
            auto_discover=True,
            require_approval=True
        )

        await agent.setup()

    except MCPServerConnectionError as e:
        logger.error(f"Failed to connect to MCP server: {e}")
        # Fallback to basic agent without MCP
        agent = SimpleAgent(engine=AugLLMConfig())

    except MCPDiscoveryError as e:
        logger.error(f"Server discovery failed: {e}")
        # Use static configuration
        agent = MCPAgent(
            engine=AugLLMConfig(),
            mcp_config=fallback_config
        )

    return agent
```

## 🔗 Next Steps

- **[Usage Patterns](../guides/usage-patterns.md)** - Common usage scenarios
- **[Architecture](../architecture/README.md)** - Understanding the system design
- **[Examples](../examples/README.md)** - Working code examples
- **[Implementation](../implementation/README.md)** - Production patterns

---

**Need Help?** Check the [Examples](../examples/README.md) directory for working code samples.
