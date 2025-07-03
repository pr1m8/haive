# Documentation Fix Guide

## Quick Start for Fixed Documentation

I've created two convenient scripts to solve the documentation building and serving issues:

```bash
# Build the documentation
./docs/build_docs.sh

# Serve the documentation
./docs/serve_docs.sh
```

Or with auto-reload (for development):

```bash
./docs/serve_docs.sh --autobuild
```

## What Was Fixed

1. **Missing Logo Files**: Added placeholder SVG logos that were referenced in the theme configuration
2. **Python Path Issues**: Set up proper PYTHONPATH to include all namespaced packages
3. **Build Environment**: Created controlled build environment with proper dependency installation
4. **Simplified Process**: Created easy-to-use scripts for building and serving

## Common Problems

The documentation system was facing several issues:

1. **Import Errors**: The namespaced package structure (`packages/haive-*/src`) required special Python path handling
2. **Missing Assets**: Logo files referenced in `conf.py` were missing
3. **Build Environment**: Poetry and nox weren't configured properly for the namespaced packages
4. **Configuration**: Some Sphinx extensions had incorrect configurations

## Additional Notes

- The documentation is built in `docs/build/html/`
- View at http://localhost:8000 after running the serve script
- For more advanced configuration, check `docs/source/conf.py`
- All warnings should be visible during the build process now

## For Advanced Users

You can still use the nox commands if you prefer, but they may require environment tweaking:

```bash
# With proper environment
export PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/packages/haive-core/src:$(pwd)/packages/haive-agents/src:$(pwd)/packages/haive-tools/src:$(pwd)/packages/haive-games/src:$(pwd)/packages/haive-dataflow/src:$(pwd)/packages/haive-prebuilt/src:$(pwd)/packages/haive-mcp/src
poetry run nox -s docs
```
