#!/bin/bash
# 🖨️ Print Statement Eliminator
# Usage: ./dev-tools/scripts/print-eliminator.sh <src_directory>

set -e

SRC_DIR=${1:-"src/"}
if [ ! -d "$SRC_DIR" ]; then
    echo "❌ Directory not found: $SRC_DIR"
    exit 1
fi

echo "🖨️ PRINT ELIMINATOR: $SRC_DIR"

# Safety checkpoint
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
git stash push -m "SAFETY_CHECKPOINT_print_elimination_${TIMESTAMP}" || echo "⚠️ No changes to stash"

# Count current print statements
PRINT_COUNT=$(grep -r "print(" "$SRC_DIR" --include="*.py" | wc -l || echo "0")
echo "🚨 Found $PRINT_COUNT print statements"

if [ "$PRINT_COUNT" -eq 0 ]; then
    echo "✅ No print statements found!"
    exit 0
fi

# Method 1: Use ruff to remove print statements
echo "🚀 Removing print statements with ruff..."
poetry run ruff check "$SRC_DIR" --select T201 --fix || echo "⚠️ ruff completed with warnings"

# Method 2: Backup approach - sed replacement for remaining prints
echo "🔧 Converting remaining prints to logger..."
find "$SRC_DIR" -name "*.py" -exec sed -i 's/print(/logger.info(/g' {} \;

# Add logger import where needed
echo "📝 Adding logger imports where needed..."
for file in $(grep -l "logger\." "$SRC_DIR"/*.py 2>/dev/null || true); do
    if ! grep -q "from haive.core.utils.dev import logger" "$file" && ! grep -q "import logging" "$file"; then
        sed -i '1i from haive.core.utils.dev import logger' "$file"
    fi
done

# Final count
FINAL_COUNT=$(grep -r "print(" "$SRC_DIR" --include="*.py" | wc -l || echo "0")
ELIMINATED=$((PRINT_COUNT - FINAL_COUNT))

echo ""
echo "🎉 RESULTS:"
echo "📊 BEFORE: $PRINT_COUNT print statements"
echo "✅ AFTER:  $FINAL_COUNT print statements"
echo "🎯 ELIMINATED: $ELIMINATED print statements"
echo ""
echo "🔄 ROLLBACK: git stash apply stash@{0} (if needed)" 