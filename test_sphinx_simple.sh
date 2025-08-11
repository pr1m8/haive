#!/bin/bash
# Simple Sphinx test build

echo "======================================================================="
echo "SIMPLE SPHINX TEST BUILD"
echo "======================================================================="

# Backup current conf.py
cp docs/source/conf.py docs/source/conf.py.current_backup

# Use test configuration
cp docs/source/conf_test_autodoc_pydantic.py docs/source/conf.py

# Clean and build
rm -rf docs/build/html_test
echo "🔨 Building with test configuration..."
poetry run sphinx-build -b html docs/source docs/build/html_test -v -W --keep-going 2>&1 | tee sphinx_simple_test.log

# Restore original conf.py
cp docs/source/conf.py.current_backup docs/source/conf.py

# Analysis
echo ""
echo "📊 Results:"
echo "  - Warnings: $(grep -c "WARNING:" sphinx_simple_test.log || echo 0)"
echo "  - HTML files: $(find docs/build/html_test -name "*.html" 2>/dev/null | wc -l || echo 0)"
echo ""
echo "Log: sphinx_simple_test.log"
echo "Output: docs/build/html_test/"
