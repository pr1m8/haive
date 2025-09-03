# Haive-MCP Project Documentation

**Dynamic Model Context Protocol Integration for Haive Agents**

## 📋 Documentation Overview

This directory contains comprehensive documentation for the Haive-MCP package, which provides dynamic MCP (Model Context Protocol) integration capabilities for Haive agents.

## 🎯 Purpose

Haive-MCP enables agents to:

- **Dynamically discover** and install MCP servers from a database of 1,960+ servers
- **Hot-reload** tools and capabilities without restarting
- **Intelligent analysis** of user needs to automatically suggest appropriate servers
- **Human-in-the-loop approval** workflows for server installations
- **Seamless integration** with existing Haive agent framework

## 📚 Documentation Structure

### 🚀 Getting Started

- **[Integration Guide](integration/README.md)** - How to integrate MCP capabilities into your agents
- **[Quick Start](guides/quick-start.md)** - Get up and running in 5 minutes
- **[Installation](guides/installation.md)** - Detailed installation instructions

### 🏗️ Architecture & Implementation

- **[Architecture Overview](architecture/README.md)** - System design and components
- **[Dynamic Discovery](architecture/dynamic-discovery.md)** - How intelligent server discovery works
- **[Hot-Reload System](architecture/hot-reload.md)** - Runtime tool management
- **[Implementation Patterns](implementation/README.md)** - Common implementation patterns

### 📖 Guides & Tutorials

- **[Usage Patterns](guides/usage-patterns.md)** - Common usage scenarios
- **[Agent Integration](guides/agent-integration.md)** - Integrating MCP with existing agents
- **[Server Management](guides/server-management.md)** - Managing MCP servers
- **[HITL Workflows](guides/hitl-workflows.md)** - Human-in-the-loop approval patterns

### 🔧 Examples & Templates

- **[Code Examples](examples/README.md)** - Working code examples
- **[Templates](examples/templates/)** - Starter templates for common scenarios
- **[Best Practices](examples/best-practices.md)** - Production-ready patterns

## 🎯 Key Concepts

### Dynamic MCP Integration

Unlike static MCP configurations, Haive-MCP provides:

1. **Runtime Discovery**: Agents can discover and install servers based on task requirements
2. **Intelligent Matching**: AI-powered analysis matches user needs to appropriate servers
3. **Hot-Reload**: Add new capabilities without restarting agents
4. **Approval Workflows**: Human oversight for server installations

### Core Components

- **`IntelligentMCPAgent`**: AI-powered agent with dynamic discovery
- **`MCPManager`**: Server lifecycle management with hot-reload
- **`MCPServerDiscovery`**: Intelligent server discovery and matching
- **`MCPDocumentationLoader`**: Access to 1,960+ server database

## 🚀 Quick Example

```python
from haive.mcp.agents import IntelligentMCPAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Create agent with dynamic discovery
agent = IntelligentMCPAgent(
    engine=AugLLMConfig(),
    auto_discover=True,      # Enable automatic server discovery
    require_approval=True    # Human approval for installations
)

await agent.setup()

# Agent automatically discovers and installs needed servers!
result = await agent.arun({
    "messages": [{
        "role": "user",
        "content": "Search for Python tutorials and save to a spreadsheet"
    }]
})
# Agent detects needs:
# - Web search → installs brave-search server
# - Spreadsheet → installs google-sheets server
# Then completes the task!
```

## 📊 Package Statistics

- **1,960+ MCP Servers** in discovery database
- **Dynamic Hot-Reload** capabilities
- **AI-Powered Discovery** matching
- **Production-Ready** HITL workflows
- **Seamless Integration** with Haive framework

## 🔗 Quick Navigation

- **New to MCP?** → Start with [Integration Guide](integration/README.md)
- **Need examples?** → Check [Examples](examples/README.md)
- **Building production?** → See [Implementation Patterns](implementation/README.md)
- **Understanding architecture?** → Read [Architecture Overview](architecture/README.md)

---

**Last Updated**: January 2025  
**Version**: 0.1.0  
**Status**: Active Development
