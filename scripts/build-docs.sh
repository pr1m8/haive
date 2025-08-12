#!/bin/bash
# Build documentation

set -e

echo "Building documentation..."

# Clean previous builds
rm -rf docs/build/*

# Build HTML documentation
cd docs && make html

echo "Documentation built successfully!"
echo "Open docs/build/html/index.html to view."
