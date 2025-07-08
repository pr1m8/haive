#!/bin/bash

echo "=== Haive Documentation Navigation Status ==="
echo "Time: $(date)"
echo ""

# Check build status
if pgrep -f "sphinx-build" >/dev/null; then
	echo "📦 Build Status: IN PROGRESS"
	PROGRESS=$(tail -1 /tmp/haive_docs_build.log | grep -oE '[0-9]+%' || echo "Starting...")
	echo "   Progress: ${PROGRESS}"
else
	echo "✅ Build Status: COMPLETE (or not running)"
fi

echo ""
echo "📂 New Structure Files Created:"
find docs/source/api/haive -type f -name "*.rst" | wc -l | xargs -I {} echo "   {} RST files"

echo ""
echo "🌐 Server Status:"
if lsof -ti :8002 >/dev/null; then
	echo "   ✅ Running on http://localhost:8002"

	# Check if new structure is accessible
	if [[ -f "docs/build/html/api/haive/index.html" ]]; then
		echo "   ✅ New structure available!"
		echo ""
		echo "🔗 Key URLs to test:"
		echo "   - Main: http://localhost:8002/api/haive/index.html"
		echo "   - Core: http://localhost:8002/api/haive/core/index.html"
		echo "   - Engine: http://localhost:8002/api/haive/core/engine/index.html"
	else
		echo "   ⏳ New structure not yet built"
		echo "   Using old structure at: http://localhost:8002/api/haive-core.html"
	fi
else
	echo "   ❌ Not running"
fi

echo ""
echo "📄 Latest build activity:"
tail -3 /tmp/haive_docs_build.log 2>/dev/null || echo "   No build log found"

echo ""
echo "💡 Quick Commands:"
echo "   - Watch build: tail -f /tmp/haive_docs_build.log"
echo "   - Start server: cd docs/build/html && python -m http.server 8002"
echo "   - Rebuild: ./docs/auto_build.sh"
