# Documentation Organization Guide

This folder contains comprehensive guidelines for writing and organizing documentation for the Haive project. Follow these guides to maintain consistency and quality across all documentation.

## 📁 Documentation Structure

```
project_docs/docs/
├── README.md                    # This file - main navigation
├── writing-guidelines/          # How to write documentation
├── organization-standards/      # How to organize documentation
├── content-types/              # Different types of documentation
├── tools-and-automation/       # Documentation tools and automation
├── quality-assurance/          # Review and quality processes
└── examples/                   # Real examples and templates
```

## 🎯 Quick Start Guides

### For New Contributors
1. **[Writing Guidelines](writing-guidelines/)** - Learn the Haive documentation style
2. **[Content Types](content-types/)** - Understand what type of documentation to write
3. **[Examples](examples/)** - See real examples and use templates

### For Maintainers
1. **[Organization Standards](organization-standards/)** - Structure and hierarchy rules
2. **[Tools and Automation](tools-and-automation/)** - Sphinx, extensions, and automation
3. **[Quality Assurance](quality-assurance/)** - Review processes and standards

## 📚 Documentation Hierarchy

### 1. **User-Facing Documentation** (`/docs/source/`)
- **API References** - Auto-generated from docstrings
- **User Guides** - How to use the framework
- **Agent Showcase** - Live examples and demonstrations
- **Getting Started** - Quick start and tutorials

### 2. **Developer Documentation** (`/project_docs/`)
- **Technical Notes** - Implementation details
- **Architecture Decisions** - Design rationale
- **Development Guides** - How to contribute and develop

### 3. **Package Documentation** (`/packages/{name}/README.md`)
- **Package-specific** - Individual package documentation
- **API Examples** - Usage examples for each package
- **Configuration** - Package-specific configuration

## 🛠️ Documentation Tools

- **Sphinx** - Main documentation generator
- **Google-style Docstrings** - Code documentation standard
- **Myst-Parser** - Markdown support in Sphinx
- **Custom Extensions** - Agent discovery and showcase generation
- **Automatic Generation** - Agent documentation and API references

## 📋 Quick Reference

### Writing Documentation
- Use Google-style docstrings for all Python code
- Write in clear, concise language
- Include examples for all public APIs
- Follow the established tone and style

### Organizing Content
- Group related content together
- Use consistent naming conventions
- Maintain clear hierarchy and navigation
- Cross-reference related sections

### Quality Standards
- All documentation must be reviewed
- Examples must be tested and working
- Links must be verified
- Consistency with project standards

## 🔗 Related Resources

- [CLAUDE.md](../CLAUDE.md) - Main project navigation
- [Documentation Standards](../claude_documentation/DOCUMENTATION_STANDARDS.md) - Detailed standards
- [Agent Documentation Hub](../claude_documentation/CLAUDE_AGENTS.md) - Agent-specific docs

---

**Note**: This documentation system follows the principles established in the main project documentation and integrates with the automated agent discovery and showcase generation systems.