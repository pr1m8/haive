# MCP Agents Module

MCP-enabled AI agents for the Haive framework.

## Overview

This module provides agent implementations that integrate MCP servers:

- **MCPAgent**: Basic agent with MCP capabilities
- **TransferableMCPAgent**: Agent with tool transfer abilities
- **MCPDocumentationAgent**: Specialized agent for MCP documentation

## Components

### MCPAgent

Basic agent that can connect to and use MCP servers.

```python
from haive.mcp.agents import MCPAgent
from haive.mcp.config import MCPConfig, MCPServerConfig
from haive.core.engine import AugLLMConfig

# Create agent with MCP
agent = MCPAgent(
    engine=AugLLMConfig(),
    mcp_config=MCPConfig(
        servers={
            "filesystem": MCPServerConfig(
                transport="stdio",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-filesystem"]
            )
        }
    )
)

# Initialize and use
await agent.setup()
result = await agent.arun("List files in current directory")
```

### TransferableMCPAgent

Agent with enhanced capabilities for sharing tools between agents.

```python
from haive.mcp.agents import TransferableMCPAgent

# Create collaborative agents
agent1 = TransferableMCPAgent(engine=engine, mcp_config=config)
agent2 = TransferableMCPAgent(engine=engine, mcp_config=config)

# Transfer tools
await agent1.transfer_all_tools_to_agent(agent2)

# Share specific tools
await agent1.transfer_tools_to_agent(
    agent2,
    server_name="github",
    tool_names=["create_issue", "list_repos"]
)
```

### MCPDocumentationAgent

Specialized agent for processing MCP server documentation.

```python
from haive.mcp.agents import MCPDocumentationAgent

doc_agent = MCPDocumentationAgent.create_for_mcp_setup()

# Process server documentation
result = await doc_agent.process_mcp_server("filesystem-server")
setup_instructions = result["setup_instructions"]
config = result["mcp_config"]

# Find servers by capability
servers = await doc_agent.find_servers_by_capability("file_operations")
```

## Features

- **Automatic Tool Discovery**: Agents automatically discover and register MCP tools
- **Dynamic Server Management**: Add/remove servers at runtime
- **Tool Transfer**: Share tools between agents for collaboration
- **Error Handling**: Graceful degradation when servers are unavailable
- **Type Safety**: Full type checking with Pydantic models

## Usage Patterns

### Single Agent Pattern

```python
agent = MCPAgent.create_with_mcp_servers(
    engine=engine,
    server_configs={
        "server1": {...},
        "server2": {...}
    }
)
```

### Multi-Agent Collaboration

```python
agents = TransferableMCPAgent.create_collaborative_agents(
    engine=engine,
    mcp_config=config,
    num_agents=3,
    shared_client=True
)
```

### Documentation Processing

```python
# Get setup instructions for any MCP server
instructions = await doc_agent.generate_setup_instructions(
    server_name="@modelcontextprotocol/server-github"
)
```

## See Also

- [MCP Config](../config.py) - Configuration models
- [MCP Manager](../manager.py) - Server management
- [MCP Mixins](../mixins/) - Add MCP to existing agents
