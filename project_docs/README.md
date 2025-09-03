# Haive Project Documentation

**Version**: 4.0
**Last Updated**: 2025-01-23
**Status**: Reorganized and Decluttered

Welcome to the Haive AI Agent Framework documentation. This README serves as your navigation hub for all project documentation.

## 📋 Recent Organization (January 2025)

This documentation system has been comprehensively reorganized with:

- **✅ Root Directory Declutter**: ~150 files moved from root to organized locations
- **✅ Test Organization**: 18 test files moved to appropriate package test directories
- **✅ Documentation Structure**: 45 MD files organized into project_docs/ subdirectories
- **✅ Script Organization**: Python scripts organized into scripts/ with categories
- **✅ Gitignore Updates**: Enhanced patterns to prevent future accumulation
- **✅ Logging Fixes**: Replaced all custom `get_logger` usage with standard `logging.getLogger`

### File Movement Summary

**Test Files** → `packages/haive-*/tests/`

- Multi-agent tests → `packages/haive-agents/tests/multi/`
- Core tests → `packages/haive-core/tests/`
- Debug tests → `packages/haive-core/tests/debug/`

**Documentation** → `project_docs/`

- Implementation guides → `project_docs/guides/`
- Status reports → `project_docs/build-reports/`
- Analysis documents → `project_docs/analysis/`
- Architecture docs → `project_docs/active/architecture/`

**Scripts** → `scripts/`

- Debug utilities → `scripts/debug/`
- Maintenance tools → `scripts/maintenance/`
- Documentation scripts → `scripts/maintenance/docs/`

**Package Documentation** → `project_docs/packages/`

- haive-agents documentation → `project_docs/packages/haive-agents/`
  - Guides, implementation, patterns, examples organized by category
  - ~20 agent-related files consolidated from scattered locations

## 🏗️ Framework Overview

Haive provides a modular architecture for creating sophisticated AI agents that can:

- Execute complex workflows with planning and reasoning
- Use external tools and APIs
- Maintain conversation memory and context
- Collaborate in multi-agent systems
- Play games and interact with environments
- Process documents and data with RAG capabilities

## 🚀 Quick Start

**New to Haive?** Start here:

- [Getting Started](quick_start/README.md) - First-time setup and overview
- [Development Setup](quick_start/development_setup.md) - Environment configuration
- [Create Your First Agent](quick_start/first_agent.md) - Step-by-step tutorial

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

## 🧠 Memory Index System

**UPDATED!** Centralized memory indexing for all discoveries and knowledge:

- **[Memory Index](memory_index/README.md)** - Central index for all memories
  - [Quick Reference](memory_index/quick_reference.md) - Most-used patterns and fixes
  - [By Date](memory_index/by_date/) - Chronological memories
  - [By Error](memory_index/by_error/) - Error solutions and fixes
  - [By Task](memory_index/by_task/) - Task-specific knowledge
  - [By Agent](memory_index/by_agent/) - Agent patterns and implementations
  - [By Package](memory_index/by_package/) - Package discoveries and patterns

Use `@memory_index/` to reference specific memories throughout the project.

## 📦 Package Documentation

Organized documentation for each Haive framework package:

- **[Packages Overview](packages/README.md)** - Package documentation hub
- **[haive-core](../packages/haive-core/docs/build/html/index.html)** - 🚀 **Enhanced Documentation Available!**
  - Beautiful Furo theme with purple/violet color scheme
  - Interactive navigation with sphinx-design cards
  - Comprehensive API reference with emojis and tooltips
  - Enhanced AutoAPI with better organization
  - Full integration of 36+ Sphinx extensions
- **[haive-agents](packages/haive-agents/README.md)** - Agent implementations, patterns, and guides
  - [User Guides](packages/haive-agents/guides/) - Tutorials and usage examples
  - [Implementation Details](packages/haive-agents/implementation/) - Technical implementation
  - [Design Patterns](packages/haive-agents/patterns/) - Common patterns and fixes
  - [Architecture](packages/haive-agents/architecture/) - Agent architecture documentation
- **haive-tools** - Tool integration guides (planned)
- **haive-games** - Game environment documentation (planned)

## 📚 Documentation Navigation

- **Full Documentation**: Run `poetry run nox -s docs_serve` and visit http://localhost:8000
- **Developer Hub**: See [CLAUDE.md](../CLAUDE.md) for central development information
- **API Reference**: Built with Sphinx from source code docstrings
- **Active Development**: See [Active Documentation](active/README.md) for current standards and architecture

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
