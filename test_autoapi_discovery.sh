#!/bin/bash

# Test AutoAPI file discovery with verbose output
echo "🔍 Testing AutoAPI file discovery (SAFE MODE - LIMITED RUN)..."
echo "============================================================"

cd /home/will/Projects/haive/backend/haive

# Use a completely separate directory to avoid conflicts
TEST_DIR="docs/builds/test-autoapi-safe"

# Clean only our test directory
echo "🧹 Cleaning test directory only..."
rm -rf "$TEST_DIR"

# Run build with maximum verbosity but STOP after AutoAPI phase
echo "🏗️  Running LIMITED Sphinx build (AutoAPI discovery only)..."
echo ""

# Set environment to see what's being processed
export SPHINX_PACKAGES="core"     # Just test with core package to be faster
export SPHINX_DISABLE_EXAMPLES="" # Don't disable anything

# Run with timeout and kill after 30 seconds to ensure it doesn't run forever
timeout 30s poetry run sphinx-build \
	-vvvv \
	-d "$TEST_DIR/doctrees" \
	-b html \
	docs/source \
	"$TEST_DIR/html" \
	--keep-going \
	-T \
	2>&1 | head -500 >"$TEST_DIR-discovery.log"

# The timeout will kill it, that's expected
echo ""
echo "✅ Test run stopped (as intended)"

echo ""
echo "📊 AutoAPI Discovery Summary:"
echo "============================="

# Count different types of files found
echo "📄 Python files discovered:"
grep -c "🔍 AutoAPI processing" docs/builds/autoapi-discovery.log || echo "0"

echo ""
echo "🔍 Modules processed:"
grep "🔍 AutoAPI processing module:" docs/builds/autoapi-discovery.log | head -20

echo ""
echo "⚠️  Files skipped (if any):"
grep -i "skip\|ignore\|exclude" docs/builds/autoapi-discovery.log | grep -v "autoapi_skip_member" | head -10

echo ""
echo "📁 Check generated API docs at: docs/builds/test-autoapi/api/"
echo "📋 Full log saved to: docs/builds/autoapi-discovery.log"
