# Haive AI Agent Framework
docs: 
Advanced AI Agent Framework with auto-persistence, multi-agent coordination, and rich tool ecosystem.
https://tinyurl.com/haive-central
## Quick Start

```bash
# Install with Poetry
poetry install

# Install with development tools
poetry install --with dev

# Run tests
poetry run pytest

# Build documentation
poetry run pydevelop-docs build
```

## Structure

- `packages/` - Core framework packages
- `tools/` - Development and CLI tools
- `docs/` - Documentation
- `examples/` - Usage examples

## Tools

- `haive-cli` - Command-line interface
- `haive-dev` - Development utilities
- `haive-testing` - Testing infrastructure
- `pydevelop-docs` - Documentation generator

## Documentation

### 🚀 Enhanced Package Documentation

- **haive-core**: Enhanced documentation with Furo theme, sphinx-design cards, and interactive navigation
  - Build: `cd packages/haive-core && poetry run sphinx-build -b html docs/source docs/build`
  - View: Open `packages/haive-core/docs/build/html/index.html` in your browser
  - Features: Purple/violet color scheme, emojis, tooltips, and 36+ Sphinx extensions

### Full Framework Documentation

Build all documentation:
```bash
poetry run pydevelop-docs build
```

View at `/docs/build/html/index.html` after building.

## License

MIT License - see LICENSE file for details.
