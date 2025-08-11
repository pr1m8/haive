#!/bin/bash

# Test script for AutoAPI namespace fix
# This builds documentation using the namespace-fixed configuration

echo "🧪 Testing AutoAPI Namespace Fix Configuration"
echo "=============================================="

# Set up directories
SOURCE_DIR="/home/will/Projects/haive/backend/haive/docs/source"
BUILD_DIR="/home/will/Projects/haive/backend/haive/docs/builds/autoapi_namespace_test"
CONF_FILE="$SOURCE_DIR/conf_templates/conf_autoapi_namespace_fixed.py"

echo "📁 Source: $SOURCE_DIR"
echo "📁 Build: $BUILD_DIR"
echo "⚙️  Config: $CONF_FILE"
echo ""

# Clean build directory
echo "🧹 Cleaning build directory..."
rm -rf "$BUILD_DIR"/*

# Build with the namespace-fixed configuration
echo "🔨 Building documentation with namespace fix..."
echo "Environment: SPHINX_PACKAGES=core (haive-core only)"

cd /home/will/Projects/haive/backend/haive/docs

# Create a temporary source directory with the fixed config
TEMP_SOURCE="$BUILD_DIR/temp_source"
mkdir -p "$TEMP_SOURCE"

echo "📋 Setting up test environment..."
# Copy essential source files
cp "$SOURCE_DIR/index_furo.rst" "$TEMP_SOURCE/" 2>/dev/null || echo "index_furo.rst not found, using basic index"
cp -r "$SOURCE_DIR/_templates" "$TEMP_SOURCE/" 2>/dev/null || echo "_templates not found"
cp -r "$SOURCE_DIR/_static" "$TEMP_SOURCE/" 2>/dev/null || echo "_static not found"

# Use the fixed configuration as conf.py
cp "$CONF_FILE" "$TEMP_SOURCE/conf.py"

# Create basic index if index_furo.rst doesn't exist
if [ ! -f "$TEMP_SOURCE/index_furo.rst" ]; then
	cat >"$TEMP_SOURCE/index_furo.rst" <<'EOF'
AutoAPI Namespace Test
======================

This is a test build to verify AutoAPI namespace discovery.

API Documentation
-----------------

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/haive/index
EOF
fi

# Build using the temporary source with fixed config
echo "🔨 Building documentation..."
SPHINX_PACKAGES=core poetry run sphinx-build \
	-b html \
	-W --keep-going \
	"$TEMP_SOURCE" \
	"$BUILD_DIR/html" 2>&1 | tee "$BUILD_DIR/build.log"

# Update BUILD_DIR to point to the html output
BUILD_DIR="$BUILD_DIR/html"

echo ""
echo "🔍 Build Results:"

if [ -d "$BUILD_DIR/api" ]; then
	echo "✅ API documentation generated"
	echo "📄 Generated API files:"
	find "$BUILD_DIR/api" -name "*.html" | head -10 | sed 's|.*/||'

	echo ""
	echo "🎯 Namespace Check:"
	if [ -f "$BUILD_DIR/api/haive/index.html" ]; then
		echo "✅ Found haive/ namespace directory"
	else
		echo "❌ Missing haive/ namespace directory"
	fi

	if [ -f "$BUILD_DIR/api/haive/core/index.html" ]; then
		echo "✅ Found haive.core/ documentation"
	else
		echo "❌ Missing haive.core/ documentation"
	fi

	if [ -f "$BUILD_DIR/api/core/index.html" ]; then
		echo "❌ Found incorrect core/ namespace (should be haive.core/)"
	else
		echo "✅ No incorrect core/ namespace found"
	fi

else
	echo "❌ No API documentation generated"
fi

echo ""
echo "🌐 View results: file://$BUILD_DIR/index.html"
echo "📋 Full build log: file://$BUILD_DIR/build.log"
