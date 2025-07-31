# Package Documentation

This directory contains organized documentation for each Haive framework package.

## 📦 Package Structure

```
packages/
├── README.md                    # This file
├── haive-agents/               # Agent implementations
│   ├── README.md               # Agent package documentation hub
│   ├── guides/                 # User guides and tutorials
│   ├── implementation/         # Implementation details
│   ├── patterns/              # Design patterns
│   ├── examples/              # Examples and demos
│   ├── architecture/          # Architecture documentation
│   ├── testing/               # Testing guides
│   └── analysis/              # Analysis and evaluation
├── haive-core/                 # Core framework (planned)
├── haive-tools/                # Tool integrations (planned)
├── haive-games/                # Game environments (planned)
├── haive-mcp/                  # MCP integration (planned)
└── haive-dataflow/             # Data processing (planned)
```

## 🎯 Current Status

### ✅ Organized Packages

- **[haive-agents](haive-agents/README.md)** - Comprehensive documentation organized from scattered files throughout the project

### 📋 Planned Organization

- **haive-core** - Core framework documentation
- **haive-tools** - Tool integration guides
- **haive-games** - Game environment documentation
- **haive-mcp** - Model Context Protocol integration
- **haive-dataflow** - Data processing workflows

## 🚀 Navigation

### For Specific Packages

- **[Haive Agents](haive-agents/README.md)** - Agent implementations and usage
- **Haive Core** - Core framework (see [active architecture](../active/architecture/README.md))
- **Haive Tools** - Tool integrations (see [tools documentation](../claude_documentation/TOOL_SYSTEM_ANALYSIS.md))

### For General Framework

- **[Active Documentation](../active/README.md)** - Current standards and architecture
- **[Memory Index](../memory_index/README.md)** - Searchable memory system
- **[Guides](../guides/README.md)** - Cross-package guides

## 🔗 Integration

This package documentation structure integrates with:

- **Main Project**: [Project Documentation](../README.md)
- **Development Hub**: [CLAUDE.md](../../CLAUDE.md)
- **Active Standards**: [Standards](../active/standards/README.md)
- **Memory System**: [Memory Index](../memory_index/README.md)

## 📝 Contributing

When adding package documentation:

1. **Create Package Directory**: `packages/package-name/`
2. **Follow Structure**: Use haive-agents as template
3. **Link Integration**: Add cross-references to related docs
4. **Update This File**: Add package to the structure above

---

**Note**: This organization provides better navigation and maintainability for package-specific documentation while maintaining integration with the overall project documentation system.
