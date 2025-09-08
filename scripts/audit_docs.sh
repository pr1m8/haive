#!/bin/bash

# Audit documentation for all haive packages

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

echo "🔍 Auditing documentation for all haive packages..."
echo ""

for pkg in "${PACKAGES[@]}"; do
	echo "📦 Auditing $pkg..."

	BUILD_DIR="/home/will/Projects/haive/packages/$pkg/docs/build/html"

	if [ -d "$BUILD_DIR" ]; then
		# Check if index.html exists
		if [ -f "$BUILD_DIR/index.html" ]; then
			echo "  ✅ index.html exists"

			# Check for custom.css
			if grep -q "custom.css" "$BUILD_DIR/index.html" 2>/dev/null; then
				echo "  ✅ custom.css is included"
			else
				echo "  ❌ custom.css not included"
			fi

			# Check for announcement bar
			if grep -q "Star us on GitHub" "$BUILD_DIR/index.html" 2>/dev/null; then
				echo "  ✅ Announcement bar present"
			else
				echo "  ❌ Announcement bar missing"
			fi

			# Check GitHub links
			if grep -q "github.com/pr1m8/$pkg" "$BUILD_DIR/index.html" 2>/dev/null; then
				echo "  ✅ GitHub links to pr1m8 organization"
			else
				echo "  ⚠️ GitHub links may not be correct"
			fi

			# Check footer icons
			if grep -q "footer-icons" "$BUILD_DIR/index.html" 2>/dev/null; then
				echo "  ✅ Footer icons present"
			else
				echo "  ❌ Footer icons missing"
			fi

			# Count HTML files
			HTML_COUNT=$(find "$BUILD_DIR" -name "*.html" | wc -l)
			echo "  📄 HTML files: $HTML_COUNT"

		else
			echo "  ❌ No index.html found"
		fi
	else
		echo "  ❌ No build directory found"
	fi

	echo ""
done

echo "✨ Audit complete!"
