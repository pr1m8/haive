#!/bin/bash
# Sphinx autobuild script with optimizations

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting Sphinx autobuild with optimizations...${NC}"

# Run sphinx-autobuild with optimizations
poetry run sphinx-autobuild \
    source \
    _build/html \
    --port 8003 \
    --host 0.0.0.0 \
    --ignore "*.pyc" \
    --ignore "*.pyo" \
    --ignore "*.tmp" \
    --ignore "*~" \
    --ignore ".git/*" \
    --ignore "_build/*" \
    --ignore "**/__pycache__/*" \
    --ignore "**/node_modules/*" \
    --ignore "**/.pytest_cache/*" \
    --ignore "**/.tox/*" \
    --ignore "**/htmlcov/*" \
    --ignore "**/*.egg-info/*" \
    --re-ignore ".*\\.#.*" \
    --re-ignore ".*~$$" \
    --watch ../packages \
    --open-browser \
    -j auto \
    -E \
    $@

# -j auto: Use all CPU cores for parallel building
# -E: Don't use cached environment (forces fresh build)
# --watch ../packages: Also watch package source files
# --open-browser: Open browser automatically