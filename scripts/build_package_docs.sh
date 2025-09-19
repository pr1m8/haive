#!/bin/bash
# Build individual package documentation
# Usage: ./scripts/build_package_docs.sh <package_name>

set -e

if [ -z "$1" ]; then
	echo "❌ Usage: $0 <package_name>"
	echo "📦 Available packages: core, agents, mcp, games, hap, prebuilt, dataflow, tools"
	exit 1
fi

PACKAGE=$1
PACKAGE_DIR="packages/haive-$PACKAGE"

if [ ! -d "$PACKAGE_DIR" ]; then
	echo "❌ Package directory not found: $PACKAGE_DIR"
	exit 1
fi

echo "🔨 Building haive-$PACKAGE documentation..."
echo "📁 Package: $PACKAGE_DIR"
echo "⏰ Started: $(date)"
echo

cd "$PACKAGE_DIR"

# Check if docs directory exists
if [ ! -d "docs" ]; then
	echo "❌ No docs directory found in $PACKAGE_DIR"
	exit 1
fi

cd docs

# Clean previous build
if [ -d "build" ]; then
	echo "🧹 Cleaning previous build..."
	rm -rf build/*
fi

# Build documentation
echo "📖 Building Sphinx documentation..."
echo "🏃 Running: poetry run sphinx-build -b html source build/html"
echo

# Build with timeout and memory considerations
timeout 600 poetry run sphinx-build -b html source build/html

if [ $? -eq 0 ]; then
	echo
	echo "✅ haive-$PACKAGE documentation built successfully!"
	echo "📍 Location: $PACKAGE_DIR/docs/build/html/"
	echo "🌐 View: file://$(pwd)/build/html/index.html"
	echo "⏰ Completed: $(date)"

	# Check build size
	BUILD_SIZE=$(du -sh build/html/ | cut -f1)
	echo "📏 Build size: $BUILD_SIZE"

	# Count HTML files
	HTML_COUNT=$(find build/html/ -name "*.html" | wc -l)
	echo "📄 HTML files: $HTML_COUNT"

else
	echo
	echo "❌ haive-$PACKAGE build failed!"
	echo "💡 Check the error output above"
	exit 1
fi
