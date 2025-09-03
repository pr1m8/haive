# Haive-MCP Architecture Overview

**System design and components for dynamic MCP integration**

## 🏗️ Architecture Overview

Haive-MCP is designed as a layered architecture that provides dynamic Model Context Protocol integration for Haive agents.

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Layer                              │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐│
│  │IntelligentMCP   │ │   MCPAgent      │ │TransferableMCP  ││
│  │    Agent        │ │                 │ │    Agent        ││
│  └─────────────────┘ └─────────────────┘ └─────────────────┘│
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                  Management Layer                           │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐│
│  │   MCPManager    │ │ ServerDiscovery │ │   DocLoader     ││
│  │  (Hot-Reload)   │ │  (AI-Powered)   │ │ (1960+ Servers) ││
│  └─────────────────┘ └─────────────────┘ └─────────────────┘│
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                    MCP Layer                                │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐│
│  │  MCP Servers    │ │     Tools       │ │   Resources     ││
│  │  (External)     │ │   (Dynamic)     │ │  (Documents)    ││
│  └─────────────────┘ └─────────────────┘ └─────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## 🧩 Core Components

### 1. Agent Layer

#### IntelligentMCPAgent

**Purpose**: AI-powered agent with automatic server discovery and HITL approval.

**Key Features**:

- Automatic capability analysis from user requests
- Server discovery and installation
- Human-in-the-loop approval workflows
- Hot-reload of tools and capabilities

**Usage**:

```python
agent = IntelligentMCPAgent(
    engine=AugLLMConfig(),
    auto_discover=True,      # Enable AI discovery
    require_approval=True    # HITL approval
)
```

#### MCPAgent

**Purpose**: Production agent with static MCP server configuration.

**Key Features**:

- Pre-configured MCP servers
- Reliable tool access
- Production-ready patterns
- Integrates with existing Haive agents

**Usage**:

```python
agent = MCPAgent(
    engine=AugLLMConfig(),
    mcp_config=static_config
)
```

#### TransferableMCPAgent

**Purpose**: Agent that can share tools with other agents.

**Key Features**:

- Tool sharing between agents
- Multi-agent collaboration
- Selective capability transfer
- Dynamic tool sets

### 2. Management Layer

#### MCPManager

**Purpose**: Central server lifecycle management with hot-reload capabilities.

**Key Features**:

- Dynamic server addition/removal
- Health monitoring
- Tool refreshing
- Connection management

**Core Methods**:

```python
manager = MCPManager()

# Server management
await manager.add_server(name, config)
await manager.remove_server(name)
await manager.reload_server(name)

# Tool management
tools = await manager.get_all_tools(refresh=True)
resources = await manager.get_resources()
prompts = await manager.get_prompts()

# Health monitoring
status = manager.get_all_server_status()
health = await manager.check_server_health(name)
```

#### MCPServerDiscovery

**Purpose**: AI-powered intelligent server discovery and matching.

**Key Features**:

- Capability analysis using LLM
- Server matching algorithms
- Confidence scoring
- Setup instruction extraction

**Discovery Process**:

```python
discovery = MCPServerDiscovery()

# 1. Analyze user request
capabilities = await discovery.analyze_capability_needs(user_request)

# 2. Find matching servers
recommendations = await discovery.find_servers_by_capabilities(capabilities)

# 3. Rank by confidence
top_servers = sorted(recommendations, key=lambda x: x.confidence, reverse=True)
```

#### MCPDocumentationLoader

**Purpose**: Access to pre-processed database of 1,960+ MCP servers.

**Key Features**:

- Server metadata and documentation
- Setup instructions
- Capability categorization
- Quality scoring

**Data Structure**:

```python
loader = MCPDocumentationLoader()

# Load all servers
all_servers = loader.load_all_mcp_documents()

# Find specific server
server_doc = loader.get_server_documentation("server-name")

# Search by capability
database_servers = loader.find_servers_by_capability("database")
```

### 3. Configuration Layer

#### MCPConfig & MCPServerConfig

**Purpose**: Type-safe configuration for MCP servers and connections.

```python
from haive.mcp.config import MCPConfig, MCPServerConfig

# Individual server configuration
server_config = MCPServerConfig(
    name="postgres",
    transport="stdio",           # stdio, sse, or http
    command="npx",
    args=["-y", "@modelcontextprotocol/server-postgres"],
    env={"DATABASE_URL": "postgresql://..."},
    timeout=30.0,
    retry_attempts=3
)

# Full MCP configuration
mcp_config = MCPConfig(
    servers={"postgres": server_config},
    auto_health_check=True,
    health_check_interval=30.0,
    max_concurrent_connections=10
)
```

## 🔄 Dynamic Discovery Process

### 1. Capability Analysis

```
User Request → LLM Analysis → Capability List
"Search for Python tutorials and save to spreadsheet"
↓
["web_search", "document_storage", "spreadsheet"]
```

### 2. Server Matching

```
Capability List → Database Query → Server Recommendations
["web_search", "spreadsheet"]
↓
[{server: "brave-search", confidence: 0.95},
 {server: "google-sheets", confidence: 0.89}]
```

### 3. Installation & Integration

```
User Approval → Server Installation → Tool Integration
User approves "brave-search" and "google-sheets"
↓
Tools available in agent.mcp_tools
```

## 🔥 Hot-Reload Architecture

### Server Lifecycle Management

```
Server Addition:  Config → Connection → Tool Loading → Integration
Server Removal:   Cleanup → Connection Close → Tool Removal
Server Reload:    Disconnect → Reconnect → Tool Refresh → Update
```

### Tool Synchronization

```python
# Before tool refresh
agent.mcp_tools = {"file_read": tool1, "file_write": tool2}

# Add new server with web tools
await manager.add_server("web", web_config)

# After refresh
agent.mcp_tools = {
    "file_read": tool1,
    "file_write": tool2,
    "web_search": tool3,    # New!
    "url_fetch": tool4      # New!
}
```

## 🤖 AI-Powered Discovery

### Capability Analysis Pipeline

```python
class CapabilityAnalyzer:
    async def analyze_request(self, user_request: str) -> list[str]:
        """Extract needed capabilities from user request."""

        # 1. LLM-based analysis
        llm_capabilities = await self._llm_analyze(user_request)

        # 2. Keyword matching
        keyword_capabilities = self._keyword_analyze(user_request)

        # 3. Context-aware enhancement
        context_capabilities = await self._context_analyze(user_request)

        # 4. Merge and deduplicate
        return self._merge_capabilities(
            llm_capabilities,
            keyword_capabilities,
            context_capabilities
        )
```

### Server Matching Algorithm

```python
class ServerMatcher:
    def match_servers(self, capabilities: list[str]) -> list[ServerRecommendation]:
        """Find best matching servers for capabilities."""

        matches = []
        for server in self.server_database:
            # Calculate capability overlap
            overlap = set(capabilities) & set(server.capabilities)
            coverage = len(overlap) / len(capabilities)

            # Factor in server quality
            quality_score = server.quality_rating / 10.0

            # Calculate confidence
            confidence = (coverage * 0.7) + (quality_score * 0.3)

            if confidence > 0.5:  # Threshold
                matches.append(ServerRecommendation(
                    server_name=server.name,
                    confidence=confidence,
                    matched_capabilities=list(overlap),
                    setup_instructions=server.setup_instructions
                ))

        return sorted(matches, key=lambda x: x.confidence, reverse=True)
```

## 🔒 Security & Safety

### Approval Workflows

```python
class HITLApprovalSystem:
    async def request_approval(self, recommendation: ServerRecommendation) -> bool:
        """Human-in-the-loop approval for server installation."""

        request = HITLApprovalRequest(
            recommendation=recommendation,
            timestamp=datetime.now(),
            risk_assessment=self._assess_risk(recommendation)
        )

        # Custom approval callback
        if self.approval_callback:
            return await self.approval_callback(request)

        # Default approval logic
        return self._default_approval(request)

    def _assess_risk(self, recommendation: ServerRecommendation) -> RiskLevel:
        """Assess security risk of server installation."""
        # Check against allowlist/denylist
        # Analyze server permissions
        # Consider data access patterns
        pass
```

### Server Sandboxing

```python
class SecureMCPConnection:
    """Secure wrapper for MCP server connections."""

    def __init__(self, config: MCPServerConfig):
        self.config = config
        self.resource_limits = ResourceLimits(
            max_memory="512MB",
            max_cpu_time="30s",
            network_access="restricted"
        )

    async def execute_tool(self, tool_name: str, args: dict) -> any:
        """Execute tool with security constraints."""
        # Validate arguments
        # Apply resource limits
        # Monitor execution
        # Log activity
        pass
```

## 📊 Performance Considerations

### Connection Pooling

```python
class MCPConnectionPool:
    """Efficient connection management for MCP servers."""

    def __init__(self, max_connections: int = 10):
        self.pool = asyncio.Queue(maxsize=max_connections)
        self.active_connections = {}

    async def get_connection(self, server_name: str) -> MCPConnection:
        """Get pooled connection to server."""
        if server_name in self.active_connections:
            return self.active_connections[server_name]

        connection = await self._create_connection(server_name)
        self.active_connections[server_name] = connection
        return connection
```

### Tool Caching

```python
class ToolCache:
    """Cache for MCP tools to improve performance."""

    def __init__(self, ttl: int = 300):  # 5 minutes
        self.cache = {}
        self.ttl = ttl

    async def get_tools(self, server_name: str) -> list[Tool]:
        """Get cached tools or fetch from server."""
        cache_key = f"tools_{server_name}"

        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.ttl:
                return cached_data

        # Fetch fresh tools
        tools = await self._fetch_tools(server_name)
        self.cache[cache_key] = (tools, time.time())
        return tools
```

## 🔗 Integration Points

### Haive Agent Framework

```python
# MCP capabilities integrate seamlessly with existing Haive patterns
class EnhancedReactAgent(ReactAgent, MCPMixin):
    """ReactAgent enhanced with MCP capabilities."""

    async def setup(self):
        await super().setup()
        await self.setup_mcp()

    async def get_tools(self):
        # Combine built-in tools with MCP tools
        built_in_tools = await super().get_tools()
        mcp_tools = await self.get_mcp_tools()
        return built_in_tools + mcp_tools
```

### LangGraph Integration

```python
def create_mcp_enhanced_graph():
    """Create LangGraph workflow with MCP tools."""

    graph = StateGraph(AgentState)

    # MCP-enhanced agent node
    graph.add_node("mcp_agent", mcp_agent_node)
    graph.add_node("tool_node", create_tool_node(mcp_tools))

    # Dynamic tool routing
    graph.add_conditional_edges(
        "mcp_agent",
        should_continue,
        {"continue": "tool_node", "end": END}
    )

    return graph
```

## 🚀 Scalability

### Distributed MCP Servers

```python
class DistributedMCPManager:
    """Manage MCP servers across multiple processes/machines."""

    def __init__(self):
        self.local_servers = {}
        self.remote_servers = {}
        self.load_balancer = MCPLoadBalancer()

    async def route_tool_call(self, tool_name: str, args: dict):
        """Route tool call to appropriate server instance."""
        server_instance = await self.load_balancer.select_server(tool_name)
        return await server_instance.execute_tool(tool_name, args)
```

---

**Next**: [Dynamic Discovery Deep Dive](dynamic-discovery.md) | [Hot-Reload System](hot-reload.md)
