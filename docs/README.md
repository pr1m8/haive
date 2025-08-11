# PyAutoDoc Documentation

This directory contains all documentation for the PyAutoDoc project.

## Structure

### User Documentation

- `user-guide.md` - Getting started and basic usage
- `quick-reference.md` - Command reference and common patterns
- `api-endpoints-guide.md` - Guide for using the API endpoints

### Developer Documentation

- `developer-guide.md` - Architecture and extending PyAutoDoc
- `seed-intersphinx-guide.md` - How automatic dependency linking works

### Migration & Cleanup

- `cleanup-migration-guide.md` - Migrating to unified configuration
- `cleanup-status.md` - Status of the cleanup process

### Technical Documentation

- `DOCUMENTATION_DEPENDENCIES.md` - List of all Sphinx extensions

### Build Files

- `conf.py` - Sphinx configuration for building these docs
- `index.rst` - Main documentation index
- `Makefile` - Build commands for Unix/Linux
- `make.bat` - Build commands for Windows
- `build-docs.sh` - Shell script for building

## Building Documentation

To build this documentation:

```bash
cd docs
make html
```

Or:

```bash
sphinx-build -b html . _build/html
```

## Note

The actual PyAutoDoc tool files are in the parent directory:

- `../pyautodoc_simple.py` - The main portable tool
- `../pyautodoc.py` - Full-featured version
- `../standalone/` - Standalone versions
