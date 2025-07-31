# Noxfiles - Modular Task Automation

This directory contains the modular noxfile structure for the Haive project. Instead of one monolithic 1700+ line noxfile, we've organized sessions into focused modules.

## Structure

```
noxfiles/
├── README.md              # This file
├── __init__.py            # Package marker
├── session_docs.py        # Documentation building sessions
├── session_docs_testing.py # Documentation testing sessions
├── session_docs_memory.py # Memory-aware documentation sessions
├── session_examples.py    # Example running sessions
├── session_lint.py        # Code quality sessions
├── session_test.py        # Testing sessions
├── memory_manager.py      # Memory management utilities
└── conf_simple.py         # Simplified Sphinx configuration template
```

## Usage

The main `noxfile.py` in the project root imports all sessions from these modules:

```bash
# List all available sessions
nox -l

# Run documentation build
nox -s docs

# Run memory-safe documentation build
nox -s docs_memory_safe

# Check system resources
nox -s docs_monitor
```

## Memory Management

The `memory_manager.py` module provides intelligent memory management for resource-intensive builds:

- **Automatic resource detection**: Detects available memory and adjusts build parallelism
- **Progressive fallback**: Reduces parallelism under memory pressure
- **Memory monitoring**: Tracks memory usage during builds
- **Resource cleanup**: Performs garbage collection when memory is low

Memory-aware sessions include:

- `docs_monitor` - Check system resources and get recommendations
- `docs_memory_safe` - Build with automatic memory management
- `docs_adaptive` - Automatically adjust to available resources
- `docs_fast_memory` - Fast build with memory monitoring
- `docs_autobuild_memory` - Auto-rebuild with memory awareness

## Adding New Sessions

To add a new session type:

1. Create a new `session_<type>.py` file
2. Define your sessions using `@nox.session` decorator
3. Import the sessions in the main `noxfile.py`

Example:

```python
# session_deploy.py
import nox

@nox.session(python="3.12")
def deploy_staging(session):
    """Deploy to staging environment."""
    session.log("🚀 Deploying to staging...")
    # deployment logic here
```

## Configuration

- Python version: 3.12 (configured in PYTHON_VERSIONS)
- Virtual environments are reused for speed
- Logs are stored in `docs/logs/`
- Quality reports in `docs/quality-reports/`

## Simplified Sphinx Configuration

The `conf_simple.py` provides a clean, minimal Sphinx configuration template. To use it:

```bash
# Copy to your docs source directory
cp noxfiles/conf_simple.py docs/source/conf.py
```

This simplified configuration:

- Uses Furo theme for modern documentation
- Supports Google-style docstrings
- Includes essential extensions only
- Has clean, organized structure

## Benefits

1. **Modularity**: Each session type is in its own file
2. **Maintainability**: Easier to find and modify specific sessions
3. **Reusability**: Sessions can import utilities from each other
4. **Extensibility**: Easy to add new session types
5. **Memory Safety**: Optional memory management for large projects
6. **Organization**: Clear separation of concerns
