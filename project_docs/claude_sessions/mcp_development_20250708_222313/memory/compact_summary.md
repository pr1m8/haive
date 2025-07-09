# MCP Development - Compact Memory

## Quick Reference

### What We Built
Located in `/packages/haive-mcp/src/haive/mcp/`:

1. **fastapi_mcp_server.py** - Complete web server with:
   - Web UI for search/install/test
   - HITL approval system
   - WebSocket real-time updates
   - Live MCP server testing

2. **working_enhanced_retriever.py** - Key pattern:
   - Parent-child docs + self-query
   - Metadata on BOTH parents AND chunks
   - Natural language queries with filtering

3. **production_mcp_tool.py** - Production tool:
   - 1,960 server database
   - RAG search + HITL
   - FastMCP auto-generation

### Running the Server

```bash
cd /home/will/Projects/haive/backend/haive
poetry run python packages/haive-mcp/src/haive/mcp/fastapi_mcp_server.py
```

Then open http://localhost:8000

### Key Insights

1. **MCP = Tools + Resources + Prompts** (not agents)
2. **Parent-child + self-query** = metadata on both levels
3. **FastMCP** for Python, standard MCP for npm
4. **HITL** via web UI with WebSocket updates

### Architecture
- Database: 1,960 MCP servers
- Retriever: Enhanced parent-child + self-query  
- Integration: langchain_mcp_adapters.MultiServerMCPClient
- Testing: Live server connections with all capabilities

Ready to continue development!