#!/bin/bash
# Simple docs build using poetry directly

echo "🚀 Building documentation with poetry..."

# Ensure we're in the right directory
cd /home/will/Projects/haive/backend/haive

# Install docs dependencies with poetry
echo "📦 Installing documentation dependencies..."
poetry install --with docs

# Build the docs with single thread to avoid NoneType error
echo "📚 Building HTML documentation..."
poetry run sphinx-build -b html -j 1 docs/source docs/build/html

# Count generated files
HTML_COUNT=$(find docs/build/html -name "*.html" | wc -l)
echo "✅ Generated $HTML_COUNT HTML files"

# Show the index file location
echo "🌐 View docs at: file:///home/will/Projects/haive/backend/haive/docs/build/html/index.html"
