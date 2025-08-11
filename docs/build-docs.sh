#!/bin/bash
# Simple script to build documentation using Poetry

set -e

echo "Building pyautodoc documentation..."

# Ensure we're in the project root
cd "$(dirname "$0")/.."

# Install dependencies if needed
echo "Installing documentation dependencies..."
poetry install --with docs --no-root

# Build the documentation
echo "Building HTML documentation..."
poetry run sphinx-build -b html docs/source docs/build/html

echo "Documentation built successfully!"
echo "Open docs/build/html/index.html in your browser to view the documentation."
echo "Or run 'cd docs/build/html && python -m http.server 8000' to serve it locally."
