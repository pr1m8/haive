#!/bin/bash
# Place in docs/scripts/build.sh
cd docs
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}Setting up documentation environment...${NC}"

# Ensure we're in the docs directory
cd "$(dirname "$0")/.."

# Create mock modules
echo -e "${YELLOW}Creating mock modules...${NC}"
python scripts/mock_modules.py

# Clean previous build
echo -e "${YELLOW}Cleaning previous build...${NC}"
rm -rf _build
rm -rf api/_autosummary

# Create necessary directories
mkdir -p _static
mkdir -p _build
mkdir -p _templates
mkdir -p api/_autosummary

# Build documentation
echo -e "${YELLOW}Building documentation...${NC}"
PYTHONPATH="../src:${PYTHONPATH}" sphinx-build -b html . _build/html

# Start server if requested
if [ "$1" == "serve" ]; then
    echo -e "${GREEN}Starting documentation server...${NC}"
    cd _build/html
    python -m http.server 8000
fi