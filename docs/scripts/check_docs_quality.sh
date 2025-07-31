#!/bin/bash
# Quick documentation quality check

echo "📊 DOCUMENTATION BUILD STATUS"
echo "=============================="

# Check latest build
LOG_FILE=$(ls -t docs/logs/fast_build_*.log 2>/dev/null | head -1)
if [ -n "$LOG_FILE" ]; then
	echo "📝 Latest build log: $LOG_FILE"

	# Check progress
	last_progress=$(grep -oE '\[ *[0-9]+%' "$LOG_FILE" | tail -1 | grep -oE '[0-9]+')
	if [ -n "$last_progress" ]; then
		echo "📈 Last progress: $last_progress%"
	fi

	# Count pages and issues
	pages=$(grep -c "reading sources\|writing output" "$LOG_FILE" 2>/dev/null || echo 0)
	errors=$(grep -c "ERROR\|ImportError" "$LOG_FILE" 2>/dev/null || echo 0)
	warnings=$(grep -c "WARNING" "$LOG_FILE" 2>/dev/null || echo 0)

	echo "📄 Pages processed: $pages"
	echo "❌ Errors: $errors"
	echo "⚠️  Warnings: $warnings"
fi

# Check output
echo -e "\n🌐 HTML OUTPUT:"
echo "==============="
if [ -d docs/build/html ]; then
	html_count=$(find docs/build/html -name "*.html" | wc -l)
	echo "HTML files generated: $html_count"

	if [ -f docs/build/html/index.html ]; then
		echo "✅ Index page exists"
		echo "🌐 View: file://$(pwd)/docs/build/html/index.html"
	else
		echo "❌ No index.html found"
	fi
else
	echo "❌ No build output directory"
fi

# Quick recommendations
echo -e "\n💡 RECOMMENDATIONS:"
echo "==================="
echo "1. Build stopped at ~87% - likely import errors"
echo "2. Many viewcode import failures in MCP package"
echo "3. Consider excluding problematic modules"
echo "4. Use 'nox -s docs_fast' for cleaner build"

echo -e "\n🔧 QUICK FIXES:"
echo "==============="
echo "• Run: ./scripts/build_docs_fast.sh --background"
echo "• Monitor: ./scripts/monitor_docs_build.sh --watch"
echo "• Check errors: grep -A3 -B3 'ImportError' $LOG_FILE"
