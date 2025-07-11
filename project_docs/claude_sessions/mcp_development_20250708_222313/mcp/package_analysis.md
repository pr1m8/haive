# Haive-MCP Package Analysis

## Overview

The haive-mcp package is a comprehensive MCP (Model Context Protocol) integration system that provides:

1. **Documentation Database**: 992 MCP servers scraped from GitHub with processed documentation
2. **Intelligent Discovery**: LLM-powered server discovery and capability matching
3. **Production Agents**: Ready-to-use agents with MCP tool integration
4. **Mass Installation**: Automated setup of MCP servers

## Package Structure

```
haive-mcp/
├── src/haive/mcp/
│   ├── agents/                    # MCP-enabled agents
│   │   ├── documentation_agent.py # Researches MCP servers from database
│   │   ├── mcp_agent.py           # Production agent with MCP tools
│   │   └── transferable_mcp_agent.py # Tool sharing between agents
│   ├── cli/                       # Command-line interface
│   ├── config.py                  # Configuration models
│   ├── discovery/                 # Server discovery and analysis
│   ├── documentation/             # Documentation processing
│   ├── downloader/               # Server installation system
│   ├── integration/              # Haive framework integration
│   ├── mixins/                   # MCP mixins for agents
│   ├── servers/                  # Custom MCP server implementations
│   ├── tools/                    # Utility tools
│   └── utils/                    # Helper utilities
├── data/mcp_servers/             # 992 server documentation database
├── configs/                      # Configuration files
├── examples/                     # Usage examples
└── tests/                        # Test suite
```

## Key Components

### 1. Documentation Agent (`documentation_agent.py`)

- **Purpose**: Research and analyze the 992-server database
- **Key Methods**:
  - `find_servers_by_capability(capability, limit)` - AI-powered server discovery
  - `generate_implementation_guide(server_names, target_agent_type)` - Complete setup guides
  - `process_mcp_server(server_name)` - Analyze specific server documentation

### 2. MCP Agent (`mcp_agent.py`)

- **Purpose**: Production agent that uses MCP servers
- **Features**:
  - Connects to multiple MCP servers simultaneously
  - Auto-discovers tools and resources from connected servers
  - Integrates with Haive agent framework

### 3. Transferable MCP Agent (`transferable_mcp_agent.py`)

- **Purpose**: Tool sharing between agents
- **Features**:
  - Transfer specific tools between agents
  - Share all tools from one agent to another
  - Enable collaborative agent workflows

### 4. Documentation Loader (`documentation/doc_loader.py`)

- **Purpose**: Direct access to the documentation database
- **Features**:
  - Load all 992 server documents
  - Get specific server documentation
  - Search and filter servers

### 5. Downloader System (`downloader/`)

- **Purpose**: Automated MCP server installation
- **Components**:
  - `core.py` - Core download logic
  - `installers.py` - Different installer types (npm, python, etc.)
  - `github_mass_downloader.py` - Mass download from GitHub

## Configuration System

### MCPConfig Model

```python
class MCPConfig(BaseModel):
    enabled: bool = True
    servers: Dict[str, MCPServerConfig] = Field(default_factory=dict)

class MCPServerConfig(BaseModel):
    name: str
    transport: str = "stdio"  # or "sse"
    command: str
    args: List[str] = Field(default_factory=list)
    env: Dict[str, str] = Field(default_factory=dict)
```

## Data Sources

### MCP Server Database

- **Location**: `data/mcp_servers/`
- **Size**: 992 GitHub repositories
- **Content**:
  - README parsing for setup instructions
  - LLM-powered capability extraction
  - Installation command detection
  - Pre-processed and cached documentation

### Key Data Files

- `ALL_MCP_SERVERS_COMPLETE.json` - Complete server database
- `production_mcp_database.json` - Production-ready servers
- `discovery_results.json` - Discovery analysis results
- `documents/` - Individual server documentation files

## Integration with Haive Framework

### Agent Integration

- Extends base Haive agents with MCP capabilities
- Uses Haive's engine system for LLM operations
- Integrates with Haive's schema system for state management

### Tool System

- MCP tools are exposed as Langchain tools
- Tools are automatically discovered from MCP servers
- Tools can be transferred between agents

### Configuration Integration

- Uses Haive's configuration patterns
- Validates configurations with Pydantic models
- Supports environment-specific configurations

## Workflow Patterns

### 1. Research → Production Pattern

```python
# Research phase: Find suitable servers
doc_agent = MCPDocumentationAgent.create_for_mcp_setup(engine)
servers = await doc_agent.find_servers_by_capability("database")
guide = await doc_agent.generate_implementation_guide(server_names)

# Production phase: Use discovered configuration
prod_agent = MCPAgent(engine=engine, mcp_config=guide["combined_config"])
```

### 2. Mass Installation Pattern

```python
# Install all documented servers
downloader = GeneralMCPDownloader()
await downloader.download_all_servers()
```

### 3. Tool Transfer Pattern

```python
# Share tools between agents
await agent1.transfer_tools_to_agent(agent2, tool_names=["read_file"])
```

## Dependencies

### Core MCP

- `mcp ^1.9.4` - Core MCP protocol
- `fastmcp ^2.8.0` - FastMCP implementation
- `langchain-mcp-adapters ^0.1.7` - Langchain integration
- `langchain-mcp-tools ^0.2.9` - Tool adapters

### Haive Framework

- `langchain ^0.3.20` - LLM framework
- `langgraph ^0.3.5` - Graph workflows
- `pydantic ^2.10.6` - Configuration validation

### Utilities

- `aiohttp ^3.9.5` - HTTP client
- `fastapi ^0.115.0` - Web framework
- `click ^8.2.1` - CLI framework
- `pyyaml ^6.0.2` - YAML processing

## Architecture Insights

### Design Patterns

1. **Repository Pattern**: MCP server documentation as data repository
2. **Agent Pattern**: Specialized agents for different MCP workflows
3. **Factory Pattern**: Agent creation with auto-configuration
4. **Adapter Pattern**: Integration between MCP and Haive frameworks

### Key Architectural Decisions

1. **Documentation-First**: Build database of server docs, then use AI to process
2. **Two-Phase Workflow**: Research phase (documentation) → Production phase (usage)
3. **Auto-Configuration**: Generate configs from documentation automatically
4. **Tool Transfer**: Enable collaborative agent workflows

### Performance Considerations

- Pre-processed documentation for fast access
- Cached discovery results
- Async operations throughout
- Batch installation capabilities
