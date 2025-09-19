#!/bin/bash
# Build all package documentation sequentially in memory-optimized order
# Order: hap, tools, mcp, dataflow, games, agents (core already building)

set -e

echo "🚀 Building ALL package documentation sequentially"
echo "💾 Memory-optimized order: hap → tools → mcp → dataflow → games → agents"
echo "⏰ Started: $(date)"
echo "📝 Note: haive-core should already be building in background"
echo

# Packages in memory-optimized order
PACKAGES=("hap" "tools" "mcp" "dataflow" "games" "agents")
TOTAL=${#PACKAGES[@]}
CURRENT=1

for PACKAGE in "${PACKAGES[@]}"; do
	echo "=================================================================================="
	echo "📦 Building haive-$PACKAGE ($CURRENT/$TOTAL)"
	echo "=================================================================================="

	# Run the individual build script
	./scripts/build_package_docs.sh "$PACKAGE"

	if [ $? -eq 0 ]; then
		echo "✅ haive-$PACKAGE completed successfully!"
	else
		echo "❌ haive-$PACKAGE failed - continuing with next package"
	fi

	echo
	echo "⏸️  Waiting 5 seconds before next build..."
	sleep 5

	CURRENT=$((CURRENT + 1))
done

echo "=================================================================================="
echo "🎉 All package builds completed!"
echo "⏰ Finished: $(date)"
echo "=================================================================================="

echo
echo "📁 Documentation available at:"
for PACKAGE in "${PACKAGES[@]}"; do
	BUILD_PATH="packages/haive-$PACKAGE/docs/build/html/"
	if [ -d "$BUILD_PATH" ]; then
		echo "   ✅ haive-$PACKAGE: $BUILD_PATH"
	else
		echo "   ❌ haive-$PACKAGE: Build not found"
	fi
done

echo
echo "🌐 To view documentation:"
echo "   cd packages/haive-<package>/docs/build/html && python -m http.server 8001"
