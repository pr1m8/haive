# Design Decisions - MCP Development

## Key Architectural Decisions

### 1. Tool vs Agent Terminology
**Decision**: Create a **tool** for MCP discovery/installation, not an "agent"
**Rationale**: 
- MCP servers provide capabilities (tools/resources/prompts), they are not agents
- The "MCPAgent" in haive-mcp is actually a configuration pattern
- Tools integrate better with the AugLLMConfig pattern

### 2. Self-Query Retriever Architecture
**Decision**: Use haive-core's SelfQueryRetrieverConfig with ChromaVectorStore
**Rationale**:
- Enables natural language queries with metadata filtering
- Can query like "database servers with more than 100 stars"
- Integrates seamlessly with existing Haive retriever system
- Metadata fields: category, stars, has_install_command, capability_count

### 3. Hierarchical Categorization with AutoTree
**Decision**: Use haive-core's AutoTree for server categorization
**Rationale**:
- Provides automatic tree visualization
- Supports Union types for mixed hierarchies
- Built-in search and traversal capabilities
- Natural representation of category → subcategory → server hierarchy

### 4. HITL Implementation
**Decision**: Simple approval system with risk levels
**Rationale**:
- Low risk: Auto-approve (read operations)
- Medium risk: Human approval (installations)
- High risk: Always require approval (system modifications)
- Maintains audit trail of all approvals

### 5. FastMCP vs Standard MCP
**Decision**: Prefer FastMCP for Python servers, fallback to standard
**Rationale**:
- FastMCP: More Pythonic, easier to generate dynamically
- Standard MCP: Broader ecosystem support (npm packages)
- Auto-detection based on repository indicators

### 6. Live Server Testing
**Decision**: Test tools, resources, AND prompts (not just tools)
**Rationale**:
- MCP defines 3 capability types, we should test all
- Tools: Functions for actions
- Resources: Data sources for retrieval
- Prompts: Templates for consistent interactions

## Implementation Patterns

### 1. Document Preparation for Retriever
```python
# Convert server data to LangChain documents with rich metadata
metadata = {
    "name": server_name,
    "category": category,
    "stars": stars,
    "has_install_command": bool(install_cmd),
    "capability_count": len(capabilities)
}
```

### 2. Client Configuration Pattern
```python
client_config = {
    "server_name": {
        "command": "python",  # or "npx"
        "args": [server_path],
        "transport": "stdio"  # or "sse"
    }
}
```

### 3. Testing Pattern
- Connect via MultiServerMCPClient
- List capabilities (tools/resources/prompts)
- Test at least one of each type
- Handle errors gracefully

## Future Enhancements

1. **Watchdog Monitoring**: Add server health checks
2. **Update Detection**: Monitor GitHub for server updates
3. **Caching**: Cache vector store for faster queries
4. **UI Integration**: Web interface for approvals
5. **Batch Operations**: Install multiple servers at once