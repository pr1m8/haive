# Nox Session Documentation - Haive Framework

## Overview

The Haive framework uses [Nox](https://nox.thea.codes/) as its task automation tool, providing a comprehensive suite of sessions for documentation, testing, linting, and example management. Our noxfile architecture is **modular and organized**, making it easy to maintain and extend.

## Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Available Sessions](#available-sessions)
  - [Documentation Building](#documentation-building)
  - [Documentation Testing](#documentation-testing)
  - [Memory-Aware Documentation](#memory-aware-documentation)
  - [Examples](#examples)
  - [Code Quality](#code-quality)
  - [Testing](#testing)
- [Common Workflows](#common-workflows)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)

## Quick Start

```bash
# List all available sessions
nox -l

# Build documentation quickly
nox -s docs_fast

# Build and serve documentation
nox -s docs_serve

# Run all tests
nox -s test

# Run linters
nox -s lint

# Use short aliases
nox -s d    # Same as 'docs'
nox -s s    # Same as 'docs_serve'
nox -s dl   # Same as 'docs_autobuild'
```

## Architecture

```
haive/
├── noxfile.py                    # Main entry point - imports all sessions
└── noxfiles/                     # Modular session definitions
    ├── session_docs.py           # Documentation building (15 sessions)
    ├── session_docs_phased.py    # Phased documentation builds (3 sessions)
    ├── session_docs_testing.py   # Documentation testing (8 sessions)
    ├── session_docs_memory.py    # Memory-aware builds (5 sessions)
    ├── session_examples.py       # Example running (7 sessions)
    ├── session_lint.py           # Code quality (4 sessions)
    ├── session_test.py           # Testing (4 sessions)
    ├── memory_manager.py         # Intelligent memory management
    ├── env_utils.py             # Environment utilities
    └── conf_simple.py           # Simplified Sphinx config template
```

## Available Sessions

### Documentation Building

| Session          | Description                              | Usage                   |
| ---------------- | ---------------------------------------- | ----------------------- |
| `docs`           | Standard Sphinx build with logging       | `nox -s docs`           |
| `docs_fast`      | Fast build, continues on errors          | `nox -s docs_fast`      |
| `docs_full`      | Full build with autosummary regeneration | `nox -s docs_full`      |
| `docs_serve`     | Serve pre-built docs on port 8003        | `nox -s docs_serve`     |
| `docs_autobuild` | Auto-rebuild on file changes             | `nox -s docs_autobuild` |
| `docs_clean`     | Clean all build artifacts                | `nox -s docs_clean`     |
| `docs_debug`     | Analyze recent build logs                | `nox -s docs_debug`     |
| `docs_history`   | Show build history and trends            | `nox -s docs_history`   |
| `docs_logs`      | List and manage build logs               | `nox -s docs_logs`      |
| `docs_quality`   | Run doc8 and codespell checks            | `nox -s docs_quality`   |
| `docs_linkcheck` | Check for broken links                   | `nox -s docs_linkcheck` |
| `docs_nitpicky`  | Build with all warnings as errors        | `nox -s docs_nitpicky`  |
| `docs_test`      | Quick validation of conf.py              | `nox -s docs_test`      |
| `docs_coverage`  | Check documentation coverage             | `nox -s docs_coverage`  |
| `docs_pdf`       | Generate PDF documentation               | `nox -s docs_pdf`       |

#### Example Usage

```bash
# Quick iterative development
nox -s docs_fast

# Full clean build for production
nox -s docs_clean docs_full

# Build and immediately serve
nox -s docs docs_serve

# Auto-rebuild during development
nox -s docs_autobuild
```

### Documentation Testing

| Session                | Description                     | Usage                         |
| ---------------------- | ------------------------------- | ----------------------------- |
| `docs_test_all`        | Run ALL documentation tests     | `nox -s docs_test_all`        |
| `docs_test_docstrings` | Test docstring coverage/quality | `nox -s docs_test_docstrings` |
| `docs_test_examples`   | Test code examples              | `nox -s docs_test_examples`   |
| `docs_test_notebooks`  | Test Jupyter notebooks          | `nox -s docs_test_notebooks`  |
| `docs_test_spelling`   | Advanced spell checking         | `nox -s docs_test_spelling`   |
| `docs_test_prose`      | Test prose quality              | `nox -s docs_test_prose`      |
| `docs_test_metadata`   | Check package metadata          | `nox -s docs_test_metadata`   |
| `docs_test_pipeline`   | Full quality pipeline           | `nox -s docs_test_pipeline`   |

#### Example Usage

```bash
# Quick docstring check
nox -s docs_test_docstrings

# Full documentation quality check
nox -s docs_test_pipeline

# Test all code examples
nox -s docs_test_examples
```

### Memory-Aware Documentation

These sessions automatically manage system resources during builds:

| Session                 | Description                                | Usage                          |
| ----------------------- | ------------------------------------------ | ------------------------------ |
| `docs_memory_safe`      | Memory-safe build with resource management | `nox -s docs_memory_safe`      |
| `docs_fast_memory`      | Fast build with memory monitoring          | `nox -s docs_fast_memory`      |
| `docs_monitor`          | Monitor resources and suggest strategy     | `nox -s docs_monitor`          |
| `docs_adaptive`         | Adaptive build adjusting to resources      | `nox -s docs_adaptive`         |
| `docs_autobuild_memory` | Memory-aware auto-build                    | `nox -s docs_autobuild_memory` |

#### Example Usage

```bash
# Check system resources
nox -s docs_monitor

# Build on low-memory system
nox -s docs_memory_safe

# Adaptive build that adjusts automatically
nox -s docs_adaptive
```

### Examples

| Session             | Description                     | Usage                              |
| ------------------- | ------------------------------- | ---------------------------------- |
| `examples`          | Run all examples                | `nox -s examples`                  |
| `validate_examples` | Validate example syntax/imports | `nox -s validate_examples`         |
| `run_example`       | Run specific example            | `nox -s run_example -- example.py` |
| `examples_simple`   | Run SimpleAgent examples        | `nox -s examples_simple`           |
| `examples_react`    | Run ReactAgent examples         | `nox -s examples_react`            |
| `examples_rag`      | Run RAG agent examples          | `nox -s examples_rag`              |
| `examples_docs`     | Generate examples for docs      | `nox -s examples_docs`             |

#### Example Usage

```bash
# Run all examples
nox -s examples

# Run specific example
nox -s run_example -- examples/agents/simple_agent.py

# Run examples for specific agent type
nox -s examples_react
```

### Code Quality

| Session    | Description                 | Usage             |
| ---------- | --------------------------- | ----------------- |
| `lint`     | Run all linters             | `nox -s lint`     |
| `format`   | Format with black and isort | `nox -s format`   |
| `mypy`     | Type check with mypy        | `nox -s mypy`     |
| `security` | Security checks with bandit | `nox -s security` |

#### Example Usage

```bash
# Check code quality
nox -s lint

# Auto-format code
nox -s format

# Type checking
nox -s mypy
```

### Testing

| Session            | Description                  | Usage                                 |
| ------------------ | ---------------------------- | ------------------------------------- |
| `test`             | Run all tests                | `nox -s test`                         |
| `test_quick`       | Quick tests without coverage | `nox -s test_quick`                   |
| `test_package`     | Test specific package        | `nox -s test_package -- haive-agents` |
| `test_integration` | Run integration tests        | `nox -s test_integration`             |

#### Example Usage

```bash
# Run all tests with coverage
nox -s test

# Quick test run
nox -s test_quick

# Test specific package
nox -s test_package -- haive-core
```

## Common Workflows

### 1. Development Workflow

```bash
# Initial setup
poetry install

# During development
nox -s docs_autobuild  # Auto-rebuild docs
nox -s lint           # Check code quality
nox -s test_quick     # Quick tests

# Before committing
nox -s format         # Format code
nox -s test          # Full test suite
nox -s docs_full     # Full docs build
```

### 2. Documentation Development

```bash
# Quick iteration
nox -s docs_fast

# Test documentation quality
nox -s docs_test_pipeline

# Full production build
nox -s docs_clean docs_full docs_linkcheck
```

### 3. CI/CD Pipeline

```bash
# Lint and format check
nox -s lint

# Run tests
nox -s test

# Build documentation
nox -s docs_full

# Check documentation quality
nox -s docs_test_all
```

### 4. Low-Memory Systems

```bash
# Check available resources
nox -s docs_monitor

# Use memory-safe build
nox -s docs_memory_safe

# Or use adaptive build
nox -s docs_adaptive
```

## Advanced Features

### 1. Memory Management

The memory-aware sessions include:

- Automatic resource detection
- Progressive fallback strategies
- Garbage collection between phases
- Memory monitoring and reporting

### 2. Logging System

All documentation builds create detailed logs:

- Stored in `docs/logs/` with timestamps
- Error pattern detection
- Success/warning/error tracking
- Historical analysis with `docs_history`

### 3. Phased Building

The phased build system (`docs_phased`) builds documentation in stages:

1. **Phase 1**: Clean and prepare
2. **Phase 2**: Core documentation
3. **Phase 3**: API documentation
4. **Phase 4**: Examples and extras

### 4. Quality Pipeline

The `docs_test_pipeline` runs comprehensive checks:

- Docstring coverage
- Code example validation
- Spell checking
- Link validation
- Prose quality
- Metadata validation

## Troubleshooting

### Common Issues

#### 1. Out of Memory Errors

```bash
# Use memory-safe build
nox -s docs_memory_safe

# Or monitor and adjust
nox -s docs_monitor
nox -s docs_adaptive
```

#### 2. Build Failures

```bash
# Debug recent failures
nox -s docs_debug

# Check build history
nox -s docs_history

# Clean and retry
nox -s docs_clean docs_full
```

#### 3. Import Errors

```bash
# Ensure dependencies are installed
poetry install --with docs

# Validate environment
nox -s docs_test
```

#### 4. Slow Builds

```bash
# Use fast mode for development
nox -s docs_fast

# Or use autobuild for specific files
nox -s docs_autobuild
```

### Log Analysis

```bash
# List recent logs
nox -s docs_logs

# Analyze specific log
cat docs/logs/sphinx_build_YYYYMMDD_HHMMSS.log

# Debug recent build
nox -s docs_debug
```

## Environment Variables

- `HAIVE_DOCS_MEMORY_LIMIT`: Set memory limit for builds (e.g., "2G")
- `HAIVE_DOCS_PARALLEL`: Enable parallel building (experimental)
- `HAIVE_DOCS_VERBOSE`: Increase verbosity level

## Contributing

When adding new sessions:

1. Create a new module in `noxfiles/` for related sessions
2. Import sessions in main `noxfile.py`
3. Follow naming conventions:
   - `docs_*` for documentation
   - `test_*` for testing
   - `examples_*` for examples
4. Add logging and error handling
5. Update this README

## Additional Resources

- [Nox Documentation](https://nox.thea.codes/)
- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [Poetry Documentation](https://python-poetry.org/)
- [Haive Documentation Guide](../docs/DOCUMENTATION_GUIDE.md)
