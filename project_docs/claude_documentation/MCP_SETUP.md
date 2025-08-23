# MCP (Model Context Protocol) Setup for Haive

## What is MCP?

Model Context Protocol enables Claude Code to connect to external tools and data sources, extending its capabilities beyond file editing. Think of it as "USB-C for AI" - a standardized way to connect Claude to various services.

## ✅ Verified MCP Servers for Haive Development

**All servers listed below have been verified to exist on npm and install successfully.**

### 1. PostgreSQL Server (Database Operations) ✅

```bash
# Standard installation
claude mcp add haive-db -s user -- npx -y @modelcontextprotocol/server-postgres "postgresql://localhost/haive_dev"

# With authentication
claude mcp add haive-db -s user -- npx -y @modelcontextprotocol/server-postgres "postgresql://username:password@localhost:5432/haive"

# Usage: @haive-db to query schemas, run SQL, analyze performance
```

### 2. Filesystem Server (Enhanced File Operations) ✅

```bash
# Configure with project directories
claude mcp add haive-files -s user -- npx -y @modelcontextprotocol/server-filesystem \
  /home/will/Projects/haive \
  /home/will/Projects/haive/packages \
  /home/will/Projects/haive/project_docs

# Usage: @haive-files for advanced file operations beyond basic editing
```

### 3. GitHub Server (Repository Management) ✅

```bash
# Configure with your repo
claude mcp add haive-github -s user -e GITHUB_TOKEN=$GITHUB_TOKEN -- \
  npx -y @modelcontextprotocol/server-github --owner=yourusername --repo=haive

# Usage: @haive-github for issues, PRs, commits, CI/CD
```

### 4. Puppeteer Server (Browser Automation & Testing) ✅

```bash
# For UI testing and browser automation
claude mcp add haive-browser -s user -- npx -y @modelcontextprotocol/server-puppeteer

# Usage: @haive-browser to take screenshots, test UI, automate browser tasks
```

### 5. Sequential Thinking Server (Complex Problem Solving) ✅

```bash
# For breaking down complex tasks
claude mcp add haive-thinking -s user -- npx -y @modelcontextprotocol/server-sequential-thinking

# Usage: @haive-thinking for step-by-step problem solving
```

### 6. Brave Search Server (Web Research) ✅

```bash
# Get API key from https://api.search.brave.com/
claude mcp add haive-search -s user -e BRAVE_API_KEY=YOUR_KEY -- \
  npx -y @modelcontextprotocol/server-brave-search

# Usage: @haive-search for current docs, examples, and research
```

### 7. Memory Bank Server (Persistent Context) ✅

```bash
# For maintaining context across sessions
claude mcp add haive-memory -s user -- npx -y @modelcontextprotocol/server-memory

# Usage: @haive-memory to store and recall important context
```

### 8. Time Utilities (Community) ✅

```bash
# Time awareness for LLMs
claude mcp add haive-time -s user -- npx -y time-mcp

# Usage: @haive-time for current time, scheduling, date operations
```

### 9. Enhanced File Operations ✅

```bash
# FileNexus for advanced file operations
claude mcp add haive-filenexus -s user -- npx -y filenexus

# Usage: @haive-filenexus for enhanced file management
```

## Configuration Scopes

- **local** (default): Available only in current project
- **project**: Shared with team via `.mcp.json` file
- **user**: Available across all your projects

## Direct Configuration (Alternative Method)

Edit the config file directly:

### macOS

```bash
~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Windows

```bash
%AppData%\Claude\claude_desktop_config.json
```

### Example Configuration

```json
{
  "mcpServers": {
    "haive-db": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "postgresql://localhost/haive"
      ]
    },
    "haive-files": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/will/Projects/haive"
      ]
    }
  }
}
```

## Management Commands

```bash
# List all configured servers
claude mcp list

# Get details for a specific server
claude mcp get haive-db

# Remove a server
claude mcp remove haive-db

# Test server connection
# In Claude Code, type: @haive-db
```

## Best Practices

1. **Security**: Only add trusted MCP servers
2. **Naming**: Use descriptive prefixes (e.g., `haive-db` not just `db`)
3. **Documentation**: Document each server's purpose
4. **Testing**: Test servers in isolation first
5. **Scoping**: Use `user` scope for personal tools, `project` for team tools

## Common Use Cases for Haive

### Database Development

```bash
# Connect to your development database
@haive-db show tables
@haive-db describe agents table
@haive-db run SELECT * FROM agent_configurations LIMIT 10
```

### File Management

```bash
# Search across project files
@haive-files find all Python files containing "ReactAgent"
@haive-files analyze directory structure of packages/
```

### GitHub Integration

```bash
# Manage issues and PRs
@haive-github list open issues with label "bug"
@haive-github create PR from feature/new-agent to main
```

### Web Research

```bash
# Research current best practices
@haive-search latest Pydantic v2 migration guide
@haive-search LangChain tool integration examples 2025
```

## Troubleshooting

### Server Not Responding

1. Check logs: `claude mcp logs haive-db`
2. Verify connection strings and credentials
3. Ensure npm/npx is available: `which npx`
4. Restart Claude Code after config changes

### Permission Issues

- Database: Check user has required permissions
- Filesystem: Ensure Claude Code can access directories
- GitHub: Verify token has necessary scopes

### Connection Errors

```bash
# Test basic connectivity
claude mcp test haive-db

# Check if server is installed
npm list -g @modelcontextprotocol/server-postgres

# Reinstall if needed
npm install -g @modelcontextprotocol/server-postgres
```

## Advanced Configuration

### Environment Variables

```bash
# Use environment variables in configurations
claude mcp add prod-db -s user -e DATABASE_URL=$DATABASE_URL -- \
  npx -y @modelcontextprotocol/server-postgres "${DATABASE_URL}"
```

### Custom Arguments

```bash
# Add custom arguments to servers
claude mcp add haive-search -s user -- \
  npx -y @modelcontextprotocol/server-brave-search \
  --max-results 20 \
  --safe-search moderate
```

### Transport Options

```bash
# Use SSE transport for real-time updates
claude mcp add --transport sse haive-events https://api.haive.com/sse

# Use HTTP transport for REST APIs
claude mcp add --transport http haive-api https://api.haive.com/mcp
```

## Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [Available MCP Servers](https://github.com/modelcontextprotocol)
- [Claude Code MCP Guide](https://docs.anthropic.com/en/docs/claude-code/mcp)
- [Community MCP Servers](https://github.com/topics/mcp-server)
