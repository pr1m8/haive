# Haive AI Agent Framework

A comprehensive Python framework for building intelligent AI agents with advanced capabilities including tools, memory, and multi-agent coordination.

## Overview

Haive provides a modular architecture for creating sophisticated AI agents that can:

- Execute complex workflows with planning and reasoning
- Use external tools and APIs
- Maintain conversation memory and context
- Collaborate in multi-agent systems
- Play games and interact with environments
- Process documents and data with RAG capabilities

## Quick Start

```bash
# Install with poetry
poetry install

# Run tests
poetry run pytest

# Build documentation
poetry run nox -s docs_fast

# See all available commands
poetry run nox -s list
```

## Documentation

- **Full Documentation**: Run `poetry run nox -s docs_serve` and visit http://localhost:8000
- **Quick Reference**: See [CLAUDE.md](./CLAUDE.md) for developer information
- **API Reference**: Built with Sphinx from source code docstrings

## Architecture

The framework is organized into focused packages:

- **haive-core**: Core agent engine and infrastructure
- **haive-agents**: Pre-built agent implementations
- **haive-tools**: Tool integrations and toolkits
- **haive-games**: Game environments and agents
- **haive-dataflow**: Streaming and data processing
- **haive-mcp**: Model Context Protocol integration
- **haive-prebuilt**: Ready-to-use agent configurations

## Development

See [CLAUDE.md](./CLAUDE.md) for detailed development information and project structure.

## License

MIT License - see LICENSE file for details.
