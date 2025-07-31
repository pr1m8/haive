# MCP Server Architecture and Patterns

## Overview

The haive-mcp package implements a sophisticated architecture for integrating Model Context Protocol (MCP) servers with Haive agents. This document outlines the key architectural patterns and implementation strategies.

## Core Architecture Components

### 1. MCP Mixin Pattern

The `MCPMixin` class provides MCP capabilities that can be mixed into any Haive agent:

```python
class MCPMixin:
    """Mixin that adds MCP capabilities to any agent class."""

    def setup_mcp(self) -> None:
        """Initialize MCP configuration and state."""

    async def initialize_mcp(self) -> bool:
        """Connect to MCP servers and discover tools."""

    async def _setup_mcp_tools(self) -> None:
        """Register discovered MCP tools with the agent."""
```

**Benefits:**

- Composition over inheritance
- Can be added to any agent type
- Provides consistent MCP interface

### 2. Agent Hierarchy Pattern

```
BaseAgent
├── SimpleAgent
│   └── MCPAgent (with MCPMixin)
├── ReactAgent
│   └── MCPReactAgent (potential)
└── BaseRAGAgent
    └── MCPRAGAgent (potential)
```

**Design Principle**: MCP capabilities are additive, not restrictive.

### 3. Configuration Schema Pattern

```python
class MCPConfig(BaseModel):
    enabled: bool = True
    lazy_init: bool = False
    servers: Dict[str, MCPServerConfig] = Field(default_factory=dict)

class MCPServerConfig(BaseModel):
    name: str
    transport: MCPTransport = "stdio"  # or "sse"
    command: Optional[str] = None
    args: List[str] = Field(default_factory=list)
    env: Dict[str, str] = Field(default_factory=dict)
    capabilities: List[str] = Field(default_factory=list)
    description: Optional[str] = None
```

**Key Features:**

- Pydantic validation
- Environment variable support
- Capability tracking
- Transport flexibility (stdio/sse)

## MCP Server Integration Patterns

### 1. Stdio Transport Pattern

```python
server_config = MCPServerConfig(
    name="filesystem",
    transport="stdio",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem"],
    capabilities=["file_read", "file_write", "directory_list"]
)
```

**Use Cases:**

- NPM packages (`npx` execution)
- Python scripts
- Local executables

### 2. SSE Transport Pattern

```python
server_config = MCPServerConfig(
    name="web_service",
    transport="sse",
    url="http://localhost:8080/mcp",
    capabilities=["web_api"]
)
```

**Use Cases:**

- Web-based MCP servers
- Remote services
- Containerized servers

### 3. Environment Configuration Pattern

```python
server_config = MCPServerConfig(
    name="github",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-github"],
    env={
        "GITHUB_TOKEN": "your_token",
        "GITHUB_API_URL": "https://api.github.com"
    }
)
```

**Security Considerations:**

- Environment variables for secrets
- No hardcoded credentials
- Runtime configuration

## Tool Discovery and Registration

### 1. Automatic Tool Discovery

```python
async def initialize_mcp(self) -> bool:
    """Connect to servers and discover tools automatically."""
    for server_name, config in self.mcp_config.servers.items():
        client = await self._connect_to_server(config)
        tools = await client.list_tools()

        # Register tools with server prefix
        for tool in tools:
            tool_name = f"{server_name}_{tool.name}"
            self._mcp_tools[tool_name] = tool
```

### 2. Tool Naming Convention

**Pattern**: `{server_name}_{tool_name}`

**Examples:**

- `filesystem_read_file`
- `github_create_issue`
- `postgres_execute_query`

**Benefits:**

- Namespace isolation
- Server identification
- Conflict prevention

### 3. Tool Registration with Langchain

```python
async def _setup_mcp_tools(self) -> None:
    """Convert MCP tools to Langchain tools and register."""
    for tool_name, mcp_tool in self._mcp_tools.items():
        langchain_tool = self._convert_mcp_to_langchain_tool(mcp_tool)
        self.tools.append(langchain_tool)
```

## State Management Patterns

### 1. Connection State Tracking

```python
class MCPMixin:
    def __init__(self):
        self._mcp_initialized: bool = False
        self._mcp_servers: Dict[str, MCPServerConfig] = {}
        self._mcp_tools: Dict[str, Any] = {}
        self._failed_servers: Set[str] = set()
```

### 2. Health Monitoring

```python
def get_mcp_status(self) -> Dict[str, Any]:
    """Get comprehensive MCP status."""
    return {
        "enabled": self.mcp_config.enabled if self.mcp_config else False,
        "initialized": self._mcp_initialized,
        "connected_servers": list(self._mcp_servers.keys()),
        "failed_servers": list(self._failed_servers),
        "tool_count": len(self._mcp_tools)
    }
```

### 3. Error Recovery

```python
async def refresh_mcp_servers(self) -> None:
    """Reconnect to failed servers."""
    for server_name in self._failed_servers.copy():
        try:
            await self._reconnect_server(server_name)
            self._failed_servers.remove(server_name)
        except Exception:
            continue  # Keep in failed state
```

## Agent Factory Patterns

### 1. Configuration-Based Factory

```python
@classmethod
def create_with_mcp_servers(
    cls,
    engine: Any,
    server_configs: Dict[str, Dict[str, Any]],
    **kwargs
) -> "MCPAgent":
    """Create agent from configuration dictionaries."""
    # Convert dict configs to MCPServerConfig objects
    servers = {
        name: MCPServerConfig(name=name, **config)
        for name, config in server_configs.items()
    }

    mcp_config = MCPConfig(enabled=True, servers=servers)
    return cls(engine=engine, mcp_config=mcp_config, **kwargs)
```

### 2. Specialized Agent Factories

```python
def create_filesystem_agent(engine: Any) -> MCPAgent:
    """Pre-configured filesystem agent."""
    return MCPAgent.create_with_mcp_servers(
        engine=engine,
        server_configs={
            "filesystem": {
                "transport": "stdio",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem"]
            }
        }
    )
```

### 3. Multi-Server Agent Pattern

```python
def create_multi_mcp_agent(engine: Any, **tokens) -> MCPAgent:
    """Agent with multiple specialized servers."""
    server_configs = {
        "filesystem": {...},
        "github": {...},
        "postgres": {...}
    }

    return MCPAgent.create_with_mcp_servers(
        engine=engine,
        server_configs=server_configs
    )
```

## Documentation-Driven Development

### 1. Documentation Database Pattern

```python
class MCPDocumentationLoader:
    """Load and search MCP server documentation."""

    def load_all_mcp_documents(self) -> List[Dict]:
        """Load all 992 server documents."""

    def find_servers_by_capability(self, capability: str) -> List[Dict]:
        """AI-powered capability search."""

    def generate_implementation_guide(self, servers: List[str]) -> Dict:
        """Auto-generate configuration from docs."""
```

### 2. Research → Production Pattern

```python
# Phase 1: Research suitable servers
doc_agent = MCPDocumentationAgent.create_for_mcp_setup(engine)
servers = await doc_agent.find_servers_by_capability("database")
guide = await doc_agent.generate_implementation_guide(server_names)

# Phase 2: Use generated configuration
prod_agent = MCPAgent(
    engine=engine,
    mcp_config=guide["combined_config"]  # Auto-generated!
)
```

## Tool Transfer Patterns

### 1. Agent-to-Agent Tool Transfer

```python
class TransferableMCPAgent(MCPAgent):
    async def transfer_tools_to_agent(
        self,
        target_agent: MCPAgent,
        tool_names: Optional[List[str]] = None
    ) -> None:
        """Transfer specific tools between agents."""

    async def transfer_all_tools_to_agent(self, target_agent: MCPAgent) -> None:
        """Transfer all tools to another agent."""
```

### 2. Collaborative Agent Workflows

```python
# Setup specialized agents
file_agent = create_filesystem_agent(engine)
db_agent = create_database_agent(engine)

# Share file tools with database agent
await file_agent.transfer_tools_to_agent(
    db_agent,
    tool_names=["filesystem_read_file", "filesystem_write_file"]
)

# Now db_agent has both database and file capabilities
```

## Error Handling Patterns

### 1. Graceful Degradation

```python
async def call_tool_with_retry(
    self,
    tool_name: str,
    arguments: Dict[str, Any],
    max_retries: int = 3
) -> Any:
    """Call tool with automatic retry and fallback."""
    for attempt in range(max_retries):
        try:
            return await self.call_mcp_tool(tool_name, arguments)
        except Exception as e:
            if attempt < max_retries - 1:
                await self.refresh_mcp_servers()
            else:
                raise e
```

### 2. Server Health Monitoring

```python
def _mark_server_failed(self, server_name: str, error: Exception) -> None:
    """Track failed servers for recovery attempts."""
    self._failed_servers.add(server_name)
    self.logger.warning(f"Server {server_name} failed: {error}")
```

## Performance Patterns

### 1. Lazy Initialization

```python
class MCPConfig(BaseModel):
    lazy_init: bool = False  # Connect only when first tool is used
```

### 2. Connection Pooling

```python
class MCPMixin:
    def __init__(self):
        self._server_connections: Dict[str, Any] = {}
        self._connection_pool_size: int = 5
```

### 3. Tool Caching

```python
async def call_mcp_tool(self, tool_name: str, arguments: Dict) -> Any:
    """Call tool with result caching for expensive operations."""
    cache_key = f"{tool_name}:{hash(str(arguments))}"

    if cache_key in self._tool_cache:
        return self._tool_cache[cache_key]

    result = await self._execute_tool(tool_name, arguments)
    self._tool_cache[cache_key] = result
    return result
```

## Integration Patterns with Haive Framework

### 1. Engine Integration

```python
class MCPAgent(MCPMixin, SimpleAgent):
    """MCP capabilities added to SimpleAgent via mixin."""

    def setup_agent(self) -> None:
        super().setup_agent()  # Base agent setup
        if self.mcp_config and self.mcp_config.enabled:
            self.setup_mcp()  # Add MCP setup
```

### 2. Schema Integration

```python
# MCP tools automatically integrate with Haive's tool system
class MCPAgent(SimpleAgent):
    @property
    def tool_count(self) -> int:
        base_tools = len(self.tools)
        mcp_tools = len(self._mcp_tools)
        return base_tools + mcp_tools
```

### 3. State Schema Integration

```python
# MCP agents can extend any Haive state schema
class MCPAgentState(SimpleAgentState):
    mcp_tool_results: List[Dict] = Field(default_factory=list)
    active_servers: List[str] = Field(default_factory=list)
```

## Best Practices

### 1. Configuration Management

- Use environment variables for secrets
- Validate configurations with Pydantic
- Support both development and production configs

### 2. Error Handling

- Implement graceful degradation
- Provide meaningful error messages
- Log failures for debugging

### 3. Performance

- Use lazy initialization when appropriate
- Cache expensive operations
- Monitor server health

### 4. Security

- Never hardcode credentials
- Use secure transport when available
- Validate all inputs

### 5. Testing

- Mock MCP servers for unit tests
- Use real servers for integration tests
- Test error conditions and recovery
