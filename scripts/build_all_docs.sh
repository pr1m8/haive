#!/bin/bash

# Build documentation for all haive packages

PACKAGES=(
	"haive-core"
	"haive-agents"
	"haive-tools"
	"haive-mcp"
	"haive-games"
	"haive-dataflow"
	"haive-prebuilt"
	"haive-hap"
)

echo "🚀 Building documentation for all haive packages..."

for pkg in "${PACKAGES[@]}"; do
	echo "📦 Building docs for $pkg..."

	DOC_DIR="/home/will/Projects/haive/packages/$pkg/docs"

	if [ -d "$DOC_DIR/source" ]; then
		echo "  Found docs directory for $pkg"

		# Clean previous build
		rm -rf "$DOC_DIR/build"

		# Build docs (without -W to allow warnings)
		cd "$DOC_DIR"
		poetry run sphinx-build -b html source build/html --keep-going 2>&1 | tee "/tmp/${pkg}_doc_build.log"

		if [ -f "$DOC_DIR/build/html/index.html" ]; then
			echo "  ✅ Successfully built docs for $pkg"
		else
			echo "  ❌ Failed to build docs for $pkg (see /tmp/${pkg}_doc_build.log)"
		fi
	else
		echo "  ⚠️ No docs directory found for $pkg"
	fi

	echo ""
done

echo "📋 Build Summary:"
for pkg in "${PACKAGES[@]}"; do
	if [ -f "/home/will/Projects/haive/packages/$pkg/docs/build/html/index.html" ]; then
		echo "  ✅ $pkg: Success"
	else
		echo "  ❌ $pkg: Failed or not built"
	fi
done

echo ""
echo "✨ Documentation build process complete!"
