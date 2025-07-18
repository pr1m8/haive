# MCP Integration Memory - Haive Framework

**Memory Tag**: [MEM-004-MCP-INT]
**Parent**: [MEM-004-MCP] Haive MCP Package Documentation
**Related**: [MEM-004-CORE] Haive Core Engine, [MEM-004-DATAFLOW] Haive Dataflow
**Date**: 2025-01-05

## 🎯 Purpose

This memory documents the integration of Model Context Protocol (MCP) servers with Haive's core engine and dataflow systems, focusing on how MCP's tools, resources, and prompts integrate with AugLLMConfig and how to create dataflow-based MCP servers.

## 📚 MCP Core Concepts

### 1. MCP Components Overview

```
MCP Server
├── Tools         # Functions the model can call
├── Resources     # Data sources the application controls
└── Prompts       # User-defined templates for optimal tool usage
```

### 2. MCP Transport Types

- **stdio**: Process-based communication (npx, python)
- **SSE**: Server-sent events over HTTP
- **WebSocket**: Bidirectional communication (future)

## 🔗 Integration Points with Haive

### 1. AugLLMConfig Integration [MEM-004-MCP-INT-A]

The AugLLMConfig in haive-core needs to support MCP tools, resources, and prompts:

```python
from haive.core.engine.aug_llm import AugLLMConfig
from haive.mcp.config import MCPConfig

# Current AugLLMConfig structure (to be enhanced)
class AugLLMConfig:
    """Enhanced LLM configuration with MCP support."""

    # Existing fields
    llm_config: LLMConfig
    name: str
    tools: List[str] = []  # Tool names

    # MCP Integration fields (proposed)
    mcp_config: Optional[MCPConfig] = None
    mcp_prompts: Optional[Dict[str, str]] = None
    mcp_resources: Optional[List[MCPResource]] = None
```

### 2. MCP Tool Integration Pattern [MEM-004-MCP-INT-B]

MCP tools need to be converted to Haive-compatible tools:

```python
# MCP Tool Structure
{
    "name": "read_file",
    "description": "Read contents of a file",
    "inputSchema": {
        "type": "object",
        "properties": {
            "path": {"type": "string"}
        },
        "required": ["path"]
    }
}

# Haive Tool Wrapper
class MCPToolWrapper(BaseTool):
    """Wraps MCP tools for Haive compatibility."""

    def __init__(self, mcp_tool: Dict[str, Any], mcp_client: MCPClient):
        self.mcp_tool = mcp_tool
        self.mcp_client = mcp_client
        self.name = mcp_tool["name"]
        self.description = mcp_tool["description"]

    async def _arun(self, **kwargs) -> Any:
        """Execute MCP tool through client."""
        return await self.mcp_client.call_tool(
            self.name,
            arguments=kwargs
        )
```

### 3. MCP Resource Integration [MEM-004-MCP-INT-C]

Resources provide data that the application controls:

```python
# MCP Resource Structure
{
    "uri": "file:///workspace/data.json",
    "name": "Project Data",
    "description": "Current project data",
    "mimeType": "application/json"
}

# Integration with Haive
class MCPResourceProvider:
    """Provides MCP resources to agents."""

    async def get_resource_content(self, uri: str) -> Any:
        """Fetch resource content from MCP server."""
        return await self.mcp_client.read_resource(uri)

    def inject_into_context(self, agent_state: Dict[str, Any]):
        """Inject resources into agent context."""
        agent_state["mcp_resources"] = self.available_resources
```

### 4. MCP Prompts Integration [MEM-004-MCP-INT-D]

Prompts guide optimal tool usage:

```python
# MCP Prompt Structure
{
    "name": "analyze_code",
    "description": "Analyze code for issues",
    "arguments": [
        {
            "name": "language",
            "description": "Programming language",
            "required": true
        }
    ]
}

# Integration with agent system prompts
class MCPPromptManager:
    """Manages MCP prompts for agents."""

    def enhance_system_prompt(self, base_prompt: str, mcp_prompts: List[Dict]) -> str:
        """Add MCP prompt guidance to system prompt."""
        prompt_section = "\n\n## Available MCP Operations:\n"
        for prompt in mcp_prompts:
            prompt_section += f"- {prompt['name']}: {prompt['description']}\n"
        return base_prompt + prompt_section
```

## 🌊 Haive-Dataflow MCP Server Design

### 1. Dataflow-Based MCP Server Architecture [MEM-004-MCP-INT-E]

```python
from haive.dataflow import DataflowGraph, Node, StreamProcessor
from fastmcp import FastMCP

class DataflowMCPServer:
    """MCP server powered by Haive dataflow graphs."""

    def __init__(self, name: str):
        self.mcp = FastMCP(name)
        self.dataflow_graphs = {}

    def register_dataflow_tool(
        self,
        name: str,
        graph: DataflowGraph,
        description: str
    ):
        """Register a dataflow graph as an MCP tool."""

        @self.mcp.tool()
        async def dataflow_tool(**kwargs):
            """Execute dataflow graph with inputs."""
            # Create stream processor
            processor = StreamProcessor(graph)

            # Execute graph with inputs
            result = await processor.process(kwargs)

            return result

        # Store for management
        self.dataflow_graphs[name] = graph
```

### 2. Example: Document Processing MCP Server [MEM-004-MCP-INT-F]

```python
from haive.dataflow.nodes import (
    DocumentLoaderNode,
    ChunkerNode,
    EmbeddingNode,
    VectorStoreNode
)

class DocumentProcessingMCPServer(DataflowMCPServer):
    """MCP server for document processing pipelines."""

    def __init__(self):
        super().__init__("document-processor")
        self._setup_tools()

    def _setup_tools(self):
        # Create document indexing graph
        index_graph = DataflowGraph()

        # Add nodes
        loader = DocumentLoaderNode()
        chunker = ChunkerNode(chunk_size=1000)
        embedder = EmbeddingNode(model="text-embedding-3-small")
        store = VectorStoreNode(collection="documents")

        # Connect nodes
        index_graph.add_edge(loader, chunker)
        index_graph.add_edge(chunker, embedder)
        index_graph.add_edge(embedder, store)

        # Register as MCP tool
        self.register_dataflow_tool(
            name="index_document",
            graph=index_graph,
            description="Index a document for semantic search"
        )

        # Add search tool
        @self.mcp.tool()
        async def search_documents(query: str, limit: int = 5):
            """Search indexed documents."""
            # Use vector store directly
            results = await store.search(query, limit=limit)
            return results
```

### 3. Stream Processing MCP Server [MEM-004-MCP-INT-G]

```python
class StreamProcessingMCPServer(DataflowMCPServer):
    """MCP server for real-time stream processing."""

    def __init__(self):
        super().__init__("stream-processor")
        self.active_streams = {}

    @self.mcp.tool()
    async def create_stream(
        self,
        stream_id: str,
        pipeline_config: Dict[str, Any]
    ):
        """Create a new processing stream."""
        # Build dataflow graph from config
        graph = self._build_pipeline(pipeline_config)

        # Create stream processor
        processor = StreamProcessor(
            graph,
            mode="streaming",
            buffer_size=100
        )

        self.active_streams[stream_id] = processor
        await processor.start()

        return {"stream_id": stream_id, "status": "active"}

    @self.mcp.resource(
        uri="stream://active-streams",
        name="Active Streams",
        mime_type="application/json"
    )
    async def get_active_streams(self):
        """Resource showing all active streams."""
        return {
            stream_id: {
                "status": proc.status,
                "processed": proc.items_processed,
                "errors": proc.error_count
            }
            for stream_id, proc in self.active_streams.items()
        }
```

## 🔧 Implementation Plan

### Phase 1: Core Integration [MEM-004-MCP-INT-H]

1. Extend AugLLMConfig to support MCP configuration
2. Create MCPToolWrapper for tool conversion
3. Implement MCPResourceProvider for resource management
4. Build MCPPromptManager for prompt integration

### Phase 2: Dataflow Server [MEM-004-MCP-INT-I]

1. Create base DataflowMCPServer class
2. Implement tool registration from dataflow graphs
3. Add resource exposure for graph state
4. Build example servers (document, stream, analytics)

### Phase 3: Advanced Features [MEM-004-MCP-INT-J]

1. Multi-server orchestration
2. Dynamic tool generation from graphs
3. State persistence and recovery
4. Performance monitoring and optimization

## 📊 Integration Examples

### 1. Agent with MCP Tools

```python
# Create agent with MCP integration
agent = ReactAgent(
    engine=AugLLMConfig(
        llm_config=LLMConfig(provider="openai"),
        mcp_config=MCPConfig(
            servers={
                "docs": MCPServerConfig(
                    transport="stdio",
                    command="python",
                    args=["document_mcp_server.py"]
                )
            }
        )
    )
)

# Tools automatically available from MCP
result = await agent.arun({
    "messages": [{
        "role": "user",
        "content": "Index all markdown files in /docs"
    }]
})
```

### 2. Dataflow MCP Server Usage

```python
# Start the server
server = DocumentProcessingMCPServer()
await server.start()

# Client can now use the tools
client = MCPClient("stdio://document-processor")
result = await client.call_tool(
    "index_document",
    path="/docs/guide.md"
)
```

## 🚀 Next Steps

1. **Implement AugLLMConfig extensions** for MCP support
2. **Create base DataflowMCPServer** class
3. **Build example servers** demonstrating patterns
4. **Write comprehensive tests** with real MCP servers
5. **Document integration patterns** in main docs

## 📚 References

- **MCP Specification**: https://modelcontextprotocol.io/
- **FastMCP Documentation**: Server implementation framework
- **Haive Core Engine**: [MEM-004-CORE] Engine architecture
- **Haive Dataflow**: [MEM-004-DATAFLOW] Stream processing
- **Memory Methodology**: [MEM-002-B] Development standards

---

**Status**: Initial documentation complete. Ready for implementation phase.
