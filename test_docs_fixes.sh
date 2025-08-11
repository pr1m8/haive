#!/bin/bash

echo "🧪 Testing Sphinx build fixes..."
echo "=================================="

# Set working directory
cd /home/will/Projects/haive/backend/haive

# Test the organized build with fixes
echo "📁 Building with organized structure and fixes..."
poetry run sphinx-build -d docs/builds/doctrees -b html docs/source docs/builds/html -W --keep-going 2>&1 | tee docs/builds/logs/test-fixes-$(date +%Y%m%d-%H%M%S).log

echo ""
echo "🔍 Build completed!"
echo "📄 Log saved to: docs/builds/logs/test-fixes-$(date +%Y%m%d-%H%M%S).log"
echo "🌐 View docs: docs/builds/html/index.html"
echo ""
echo "⚡ For future incremental builds, use:"
echo "poetry run sphinx-build -d docs/builds/doctrees -b html docs/source docs/builds/html"
echo ""
echo "🚀 To serve locally:"
echo "poetry run python -m http.server 8000 --directory docs/builds/html"
