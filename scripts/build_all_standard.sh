#!/bin/bash
# Build all packages with standard profile - "the real deal"

echo "🚀 Building ALL packages with STANDARD profile"
echo "   This creates production-ready documentation for each package"
echo

packages=("core" "agents" "tools" "mcp" "games" "dataflow" "prebuilt")

for package in "${packages[@]}"; do
	echo "📦 Building haive-$package (standard profile)..."
	poetry run nox -s "docs-package-3.12(profile='standard', package='$package')"

	if [ $? -eq 0 ]; then
		echo "✅ $package completed successfully"
		echo "   📄 View: file://$(pwd)/docs/build/${package}_standard/index.html"
	else
		echo "❌ $package build failed"
	fi
	echo
done

echo "🎉 All standard builds completed!"
echo
echo "📁 Documentation sites available at:"
for package in "${packages[@]}"; do
	echo "   📄 haive-$package: docs/build/${package}_standard/index.html"
done
