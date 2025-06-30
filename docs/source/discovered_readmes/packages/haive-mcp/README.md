# haive-mcp

Model Context Protocol (MCP) integration for the Haive framework, providing type-safe access to MCP servers and their tools, resources, and prompts.

## Overview

The haive-mcp package enables Haive agents to connect to and use MCP servers, which provide:

- **Tools**: Functions the model can call
- **Resources**: Data sources the application controls
- **Prompts**: User-defined templates for optimal tool usage

This integration supports the full MCP ecosystem with type checking, automatic discovery, and seamless agent integration.

## Features

- 🔧 **Type-Safe Configuration**: Full Pydantic model validation
- 🔄 **Tool Transfer**: Share tools between agents dynamically
- 📚 **Documentation Processing**: Extract setup from 992+ MCP server docs
- 🔍 **Discovery System**: Find servers by capability or category
- 🤝 **Agent Integration**: Extends any Haive agent with MCP capabilities
- ⚡ **Lazy Loading**: Initialize MCP servers on-demand
- 🛡️ **Graceful Degradation**: Handles missing dependencies and failures

## Installation

```bash
# Install the package
cd packages/haive-mcp
poetry install

# Install MCP adapter dependencies
poetry add langchain-mcp-adapters
```

## Quick Start

### Basic Usage

```python
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import LLMConfig
from haive.mcp.agents import MCPAgent
from haive.mcp.config import MCPConfig, MCPServerConfig

# Create engine
engine = AugLLMConfig(
    llm_config=LLMConfig(
        provider="openai",
        model="gpt-4o-mini"
    ),
    name="my_engine"
)

# Configure MCP
mcp_config = MCPConfig(
    enabled=True,
    servers={
        "filesystem": MCPServerConfig(
            name="filesystem",
            transport="stdio",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem"],
            capabilities=["file_read", "file_write"]
        )
    }
)

# Create agent
agent = MCPAgent(
    engine=engine,
    mcp_config=mcp_config,
    name="mcp_assistant"
)

# Initialize and use
await agent.setup()
result = await agent.arun({
    "messages": [{"role": "user", "content": "List files in current directory"}]
})
```

### Using Convenience Methods

```python
# Create agent with multiple MCP servers
agent = MCPAgent.create_with_mcp_servers(
    engine=engine,
    server_configs={
        "filesystem": {
            "transport": "stdio",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem"]
        },
        "github": {
            "transport": "stdio",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_TOKEN": github_token}
        }
    }
)
```

## Advanced Features

### Tool Transfer Between Agents

```python
from haive.mcp.agents import TransferableMCPAgent

# Create collaborative agents
agents = TransferableMCPAgent.create_collaborative_agents(
    engine=engine,
    mcp_config=mcp_config,
    num_agents=3,
    shared_client=True  # Share MCP client
)

# Transfer tools between agents
agent1, agent2 = agents[:2]
await agent1.transfer_all_tools_to_agent(agent2)

# Share resources
resources = await agent1.delegate_resource_access(
    agent2,
    server_name="github",
    resource_uris=["repo:owner/name"]
)
```

### Documentation-Based Setup

```python
from haive.mcp.agents import MCPDocumentationAgent

# Create documentation agent
doc_agent = MCPDocumentationAgent.create_for_mcp_setup()

# Process MCP server documentation
result = await doc_agent.process_mcp_server(
    "modelcontextprotocol/server-filesystem"
)

# Get setup instructions
setup_instructions = result["setup_instructions"]
mcp_config = result["mcp_config"]

# Find servers by capability
servers = await doc_agent.find_servers_by_capability("search", limit=5)

# Generate implementation guide
guide = await doc_agent.generate_implementation_guide(
    server_names=["server1", "server2"],
    target_agent_type="research"
)
```

### Dynamic Server Discovery

```python
from haive.mcp.discovery import MCPServerDiscovery

# Discover available servers
discovery = MCPServerDiscovery()
servers = await discovery.discover_all()

# Filter by capability
file_servers = discovery.get_servers_by_capability("file_operations")

# Create configuration from discovered servers
mcp_config = discovery.create_mcp_config()
```

## Configuration

### MCPConfig Structure

```python
MCPConfig(
    enabled=True,                    # Enable/disable MCP
    auto_discover=True,             # Auto-discover servers
    lazy_init=True,                 # Initialize on-demand
    servers={...},                  # Server configurations
    discovery_paths=[               # Paths to search
        "~/.mcp/servers",
        ".mcp/servers"
    ],
    categories=["dev", "util"],     # Filter by category
    required_capabilities=["file"]   # Required capabilities
)
```

### MCPServerConfig Options

```python
MCPServerConfig(
    name="server_name",
    transport="stdio",              # stdio, sse, streamable_http
    command="npx",                  # Command to run
    args=["-y", "package"],        # Command arguments
    url="http://...",              # For HTTP transports
    env={"KEY": "value"},          # Environment variables
    capabilities=["file_ops"],      # Server capabilities
    category="filesystem",          # Server category
    timeout=30,                     # Connection timeout
    retry_attempts=3,              # Retry on failure
    health_check_interval=60       # Health check interval
)
```

## Agent Types

### MCPAgent

Basic agent with MCP capabilities.

### TransferableMCPAgent

Agent with enhanced transfer capabilities for sharing tools, resources, and prompts.

### MCPDocumentationAgent

Specialized agent for processing MCP documentation and generating setups.

## Examples

See the `examples/` directory for complete examples:

- `basic_mcp_agent.py` - Basic MCP usage
- `mcp_documentation_example.py` - Documentation processing
- `complete_mcp_integration.py` - Full integration demo

## Architecture

```
haive-mcp/
├── src/haive/mcp/
│   ├── agents/              # MCP-enabled agents
│   │   ├── mcp_agent.py
│   │   ├── transferable_mcp_agent.py
│   │   └── documentation_agent.py
│   ├── mixins/              # MCP mixin for agents
│   │   └── mcp_mixin.py
│   ├── discovery/           # Server discovery
│   │   ├── analyzer.py
│   │   └── server_discovery.py
│   ├── documentation/       # Documentation processing
│   │   └── doc_loader.py
│   └── config.py           # Configuration models
├── agent_resources/         # MCP server documentation
│   └── mcp_servers/
│       ├── all_mcp_documents.json
│       └── documents/      # Individual server docs
├── tests/                  # Test suite
├── examples/              # Usage examples
└── README.md
```

## Testing

```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest tests/test_mcp_real.py -v

# Run with coverage
poetry run pytest --cov=haive.mcp
```

## Dependencies

- `pydantic>=2.0` - Configuration validation
- `langchain-mcp-adapters` - MCP client implementation
- `mcp` or `fastmcp` - Core MCP protocol
- `langchain-core` - Tool interfaces
- `langgraph` - Graph workflows

## Contributing

1. Follow Google-style docstrings
2. Add type hints to all functions
3. Write tests for new features
4. Update documentation

## License

MIT License - see LICENSE file for details.

## References

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Specification](https://github.com/modelcontextprotocol/specification)
- [Haive Framework](https://github.com/yourusername/haive)
