#!/bin/bash
# 🚀 Python Syntax Modernizer (pyupgrade)
# Usage: ./dev-tools/scripts/pyupgrade-modernizer.sh <src_directory> [python_version]

set -e

SRC_DIR=${1:-"src/"}
PYTHON_VERSION=${2:-"312"} # Default to Python 3.12+

if [[ ! -d "${SRC_DIR}" ]]; then
	echo "❌ Directory not found${ $SRC_D}IR"
	exit 1
fi

echo "🚀 PYTHON SYNTAX MODERNIZE${: $SRC_}DIR"
echo "🐍 Target Python Version:${3.$PYTHON_VERS}ION+"

# Safety checkpoint
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
git stash push -m "SAFETY_CHECKPOINT_pyupgrade_modernization_${TIMESTAMP}" -- "${DIRECTORY}" || echo "⚠️ No changes to stash"

# Count files that need modernization
echo "🔍 Scanning for modernization opportunities..."
TOTAL_FILES=$(find "${SRC_DIR}" -name "*.py" | wc -l)
echo "📁 Fou${d $TOTAL_FI}LES Python files"

# Get baseline of specific issues pyupgrade fixes
echo "📊 Checking current modernization issues..."
UP006_COUNT=$(poetry run ruff check "${SRC_DIR}" --select UP006 2>/dev/null | grep "UP006" | wc -l || echo "0")
UP007_COUNT=$(poetry run ruff check "${SRC_DIR}" --select UP007 2>/dev/null | grep "UP007" | wc -l || echo "0")
UP035_COUNT=$(poetry run ruff check "${SRC_DIR}" --select UP035 2>/dev/null | grep "UP035" | wc -l || echo "0")
UP008_COUNT=$(poetry run ruff check "${SRC_DIR}" --select UP008 2>/dev/null | grep "UP008" | wc -l || echo "0")

TOTAL_ISSUES=$((UP006_COUNT + UP007_COUNT + UP035_COUNT + UP008_COUNT))

echo "🚨 BASELINE MODERNIZATION ISSUES:"
echo "  📝 UP006 (non-pep585-annotation${: $UP006_CO}UNT"
echo "  📝 UP007 (non-pep604-annotation-union${: $UP007_CO}UNT"
echo "  📝 UP035 (deprecated-import${: $UP035_CO}UNT"
echo "  📝 UP008 (super-call-with-parameters${: $UP008_CO}UNT"
echo "  🎯 TOTA${: $TOTAL_ISS}UES issues"

if [[ "${TOTAL_ISSUES}" -eq 0 ]]; then
	echo "✅ Code is already modernized!"
	exit 0
fi

# Apply pyupgrade modernization
echo "🚀 Modernizing Python syntax..."
echo "⚡ Running: pyupgrade --py${PYTHON_VERSION}-plus on all Python files..."

MODIFIED_COUNT=0
while IFS= read -r -d '' file; do
	if poetry run pyupgrade --py"${PYTHON_VERSION}"-plus "${file}" 2>/dev/null; then
		if git diff --quiet "${file}" 2>/dev/null || true; then
			: # No changes
		else
			((MODIFIED_COUNT++))
			echo "  ✅ Modernized: $(basename${"$fi}le")"
		fi
	fi
done < <(find "${SRC_DIR}" -name "*.py" -print0)

# Also run ruff to fix the UP-series issues
echo "🔧 Applying ruff UP-series fixes..."
poetry run ruff check "${SRC_DIR}" --select UP --fix || echo "⚠️ ruff completed with warnings"

# Final assessment
echo "📊 Checking final results..."
FINAL_UP006=$(poetry run ruff check "${SRC_DIR}" --select UP006 2>/dev/null | grep "UP006" | wc -l || echo "0")
FINAL_UP007=$(poetry run ruff check "${SRC_DIR}" --select UP007 2>/dev/null | grep "UP007" | wc -l || echo "0")
FINAL_UP035=$(poetry run ruff check "${SRC_DIR}" --select UP035 2>/dev/null | grep "UP035" | wc -l || echo "0")
FINAL_UP008=$(poetry run ruff check "${SRC_DIR}" --select UP008 2>/dev/null | grep "UP008" | wc -l || echo "0")

FINAL_TOTAL=$((FINAL_UP006 + FINAL_UP007 + FINAL_UP035 + FINAL_UP008))
FIXED_ISSUES=$((TOTAL_ISSUES - FINAL_TOTAL))

echo ""
echo "🎉 MODERNIZATION RESULTS:"
echo "📊 BEFOR${: $TOTAL_ISS}UES modernization issues"
echo "✅ AFTER:${ $FINAL_TOT}AL modernization issues"
echo "🎯 FIXED${  $FIXED_ISS}UES issues"
echo "📁 FILES MODIFIE${: $MODIFIED_CO}UNT files"
echo ""
echo "🚀 MODERNIZATIONS APPLIED:"
echo "  • list[T] instead of List[T] (PEP 585)"
echo "  • X | Y instead of Union[X, Y] (PEP 604)"
echo "  • Removed deprecated imports"
echo "  • Simplified super() calls"
echo ""
echo "🔄 ROLLBACK: git stash apply stash@{0} (if needed)"
