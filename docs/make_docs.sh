#!/bin/bash
# Script to build documentation

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Clean previous build
echo -e "${YELLOW}Cleaning previous build...${NC}"
rm -rf _build

# Create mockup modules
echo -e "${YELLOW}Creating mockup modules...${NC}"
poetry run python scripts/create_module_mockups.py

# Build HTML documentation
echo -e "${YELLOW}Building HTML documentation...${NC}"
poetry run sphinx-build -b html . _build/html

echo -e "${GREEN}Documentation built successfully! Open _build/html/index.html to view.${NC}"
