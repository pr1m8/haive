# Haive Documentation Scripts

This directory contains all scripts and utilities for building, maintaining, and generating documentation for the Haive project.

## Directory Structure

### 🎬 Agent Demos (`agent_demos/`)

Scripts for generating agent demonstration content:

- `generate_agent_demos.py` - Generate agent showcase content
- `generate_game_demos.py` - Generate game agent demonstrations
- `agent_cache_loader.py` - Load and format cached agent execution data
- `agent_demo_data.py` - Agent demo configuration data

### 🔧 Build Tools (`build_tools/`)

Core documentation build and maintenance scripts:

- `fix_doc_warnings.py` - Fix documentation warnings and issues
- `generate_package_docs.py` - Generate package-level documentation
- `restructure_navigation.py` - Restructure documentation navigation
- `update_sidebar_structure.py` - Update sidebar organization

### 💾 Cache Generation (`cache_generation/`)

Scripts for generating cached agent execution data:

- `generate_agent_cache.py` - Generate cached agent execution data with real LLM calls
- Cache files: `agent_cache_simple.json`, `agent_cache_react.json`

### 🛠️ Utilities (`utilities/`)

General utility scripts:

- Various helper scripts for documentation tasks

### 🔌 Extensions Dev (`extensions_dev/`)

Sphinx extension development and testing:

- Custom Sphinx extensions for Haive documentation
- Testing utilities for extensions

## Key Scripts

### Agent Cache Generation System

The agent cache generation system creates real cached agent execution data to avoid expensive LLM calls during documentation builds:

```bash
# Generate SimpleAgent cache
poetry run python scripts/generate_agent_cache.py simple

# Generate ReactAgent cache
poetry run python scripts/generate_agent_cache.py react
```

### Jinja2 Template Processing

The documentation uses Jinja2 templates for dynamic content generation:

- **Template files**: `*.rst` files with Jinja2 syntax
- **Data loader**: `agent_cache_loader.py` loads cached execution data
- **Configuration**: `agent_demo_data.py` contains demo configurations

### Sphinx Extensions

Custom Sphinx extensions in `docs/source/_extensions/`:

- `haive_sphinx_ext.py` - Core Haive documentation features
- `agent_docs.py` - Agent documentation utilities
- `games_autodoc.py` - Game documentation generation
- `safe_autosummary.py` - Safe autosummary generation

## Usage Examples

### Building Documentation

```bash
# Quick build (from docs directory)
nox -s docs_fast

# Full build with all features
nox -s docs

# Auto-rebuild on changes
nox -s docs_serve
```

### Generating Agent Demos

```bash
# Generate all agent demos
python docs/scripts/agent_demos/generate_agent_demos.py

# Generate specific agent cache
python scripts/generate_agent_cache.py simple
```

### Fixing Documentation Issues

```bash
# Fix common documentation warnings
python docs/scripts/build_tools/fix_doc_warnings.py

# Update package documentation
python docs/scripts/build_tools/generate_package_docs.py
```

## Integration with Main Scripts

This documentation scripts system integrates with the main `scripts/` directory:

- **Main script**: `scripts/generate_agent_cache.py` - Shared cache generation
- **Build scripts**: `scripts/maintenance/docs/` - Advanced build utilities
- **Doc tools**: `scripts/doc_tools/` - Documentation tooling

## Development Guidelines

### Adding New Scripts

1. Place scripts in the appropriate subdirectory
2. Update this README with script descriptions
3. Add proper docstrings and type hints
4. Test scripts thoroughly before committing

### Script Standards

- Use `poetry run` for all Python execution
- Include comprehensive docstrings
- Handle errors gracefully
- Log progress and results
- Follow the existing code style

## Recent Improvements

- ✅ **Jinja2 Template System**: Implemented sphinx-jinja2 for dynamic content
- ✅ **Agent Cache Generation**: Real LLM execution data cached for documentation
- ✅ **Visualization System**: JavaScript utilities for interactive demos
- ✅ **Organized Structure**: Better organization of documentation scripts

## Next Steps

- [ ] Migrate remaining documentation scripts to this organized structure
- [ ] Add automated testing for documentation scripts
- [ ] Create documentation script CI/CD pipeline
- [ ] Expand visualization capabilities
