# Current Context - MCP Development

## Working On

- Understanding haive-mcp package for MCP server development
- Analyzing existing MCP setup instructions for screenshot server
- Building comprehensive development guide

## Key Insights from MCP Setup Instructions

- Focus on screenshot server setup for Claude Desktop integration
- Uses NPM packages: `@sethbang/mcp-screenshot-server` and `browser-use-mcp-server`
- Configuration via `claude_desktop_config.json`
- Target: localhost:8003 documentation server
- Integration with Sphinx documentation build system

## Understanding from Setup Instructions

1. **MCP Protocol Purpose**: Screenshots of localhost documentation for visual analysis
2. **Configuration Pattern**: JSON config with command/args/env structure
3. **Testing Approach**: Manual server testing, configuration validation
4. **Integration Points**: Claude Desktop app, NPM ecosystem, local documentation

## Next Steps

1. Examine haive-mcp package structure and implementation
2. Understand how Haive implements MCP servers vs external packages
3. Document patterns for creating custom MCP servers within Haive
4. Identify integration points with Haive agents and engines

## Questions to Explore

- How does haive-mcp relate to external MCP servers?
- What utilities does Haive provide for MCP development?
- How do MCP servers integrate with Haive agents?
- What are the patterns for custom tool/resource registration?