# MCP Servers Module

MCP server implementations using FastMCP for the Haive framework.

## Overview

This module provides ready-to-use MCP server implementations:

- Example servers demonstrating MCP capabilities
- HTTP-based servers for production deployment
- Integration servers for haive-dataflow
- Custom server templates

## Server Implementations

### Example Server (FastMCP)

Basic file system server demonstrating core MCP features.

```python
from mcp.server import FastMCP

mcp = FastMCP("example-server")

@mcp.tool()
async def read_file(path: str) -> str:
    """Read file contents."""
    with open(path, 'r') as f:
        return f.read()

@mcp.resource("file://{path}")
async def file_resource(path: str) -> str:
    """File resource handler."""
    return await read_file(path)

# Run with stdio transport
mcp.run(transport="stdio")
```

### HTTP Server

Production-ready HTTP server using aiohttp.

```python
from haive.mcp.servers import create_http_server

# Create HTTP server
server = create_http_server(
    name="my-http-server",
    port=8001
)

# Add custom tools
@server.tool()
async def custom_tool(param: str) -> str:
    return f"Processed: {param}"

# Run server
server.run()
```

### Dataflow Integration Server

Server that integrates with haive-dataflow registry.

```python
from haive.mcp.servers import DataflowMCPServer

server = DataflowMCPServer()

# Provides tools for:
# - list_components
# - register_component
# - discover_components
# - create_agent_config

server.run()
```

## Creating Custom Servers

### Basic Template

```python
from mcp.server import FastMCP

# Create server
mcp = FastMCP("my-server")

# Add tools
@mcp.tool()
async def my_tool(param: str) -> str:
    """Tool description."""
    return process(param)

# Add resources
@mcp.resource("custom://{id}")
async def my_resource(id: str) -> str:
    """Resource description."""
    return fetch_resource(id)

# Add prompts
@mcp.prompt()
async def my_prompt(context: str) -> List[Dict[str, str]]:
    """Generate prompt."""
    return [{"role": "user", "content": f"Process: {context}"}]

if __name__ == "__main__":
    mcp.run()
```

### HTTP Server Template

```python
from aiohttp import web
from haive.mcp.servers import HTTPMCPServer

class MyHTTPServer(HTTPMCPServer):
    def setup_routes(self):
        self.router.add_post("/execute", self.execute_tool)
        self.router.add_get("/tools", self.list_tools)

    async def execute_tool(self, request):
        data = await request.json()
        result = await self.mcp.execute(
            data["tool"],
            data["params"]
        )
        return web.json_response({"result": result})

server = MyHTTPServer(port=8000)
server.run()
```

## Deployment

### Stdio Transport

```bash
# Run directly
python my_server.py

# With FastMCP CLI
fastmcp run my_server.py
```

### HTTP Transport

```bash
# Run with Python
python http_server.py

# With uvicorn (if using FastAPI)
uvicorn server:app --port 8000

# With gunicorn
gunicorn server:app --worker-class aiohttp.GunicornWebWorker
```

### Docker Deployment

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install mcp aiohttp

EXPOSE 8000
CMD ["python", "server.py"]
```

## Testing Servers

### Direct Testing

```python
# Test tools directly
async def test_server():
    from my_server import mcp

    result = await mcp._tools["my_tool"]("test")
    assert result == expected
```

### HTTP Testing

```python
import aiohttp

async def test_http_server():
    async with aiohttp.ClientSession() as session:
        resp = await session.post(
            "http://localhost:8000/execute",
            json={"tool": "my_tool", "params": {"param": "test"}}
        )
        result = await resp.json()
        assert result["result"] == expected
```

## See Also

- [MCP Manager](../manager.py) - Client-side server management
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [MCP Specification](https://modelcontextprotocol.io/)
