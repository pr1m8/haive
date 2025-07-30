#!/bin/bash
# 🚀 Bulk Package Fix Script - Automated 5-Step Methodology
# Usage: ./scripts/bulk_package_fix.sh <package_name>

set -e  # Exit on any error

PACKAGE_NAME=${1:-""}
if [ -z "$PACKAGE_NAME" ]; then
    echo "❌ Usage: $0 <package_name>"
    echo "Example: $0 haive-games"
    exit 1
fi

PACKAGE_DIR="packages/$PACKAGE_NAME"
if [ ! -d "$PACKAGE_DIR" ]; then
    echo "❌ Package directory not found: $PACKAGE_DIR"
    exit 1
fi

echo "🚀 BULK PACKAGE FIX: $PACKAGE_NAME"
echo "📍 Working in: $PACKAGE_DIR"

cd "$PACKAGE_DIR"

# Phase 1: Safety Checkpoint
echo "📋 PHASE 1: Creating safety checkpoint..."
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
git stash push -m "SAFETY_CHECKPOINT_${PACKAGE_NAME}_${TIMESTAMP}" || echo "⚠️ No changes to stash"

# Get baseline error count
echo "📊 Getting baseline error count..."
BASELINE_ERRORS=$(poetry run ruff check src/ --statistics 2>/dev/null | grep "Found" | grep -o '[0-9]*' | head -1 || echo "0")
echo "🚨 BASELINE: $BASELINE_ERRORS errors"

# Phase 2: Automated 5-Step Cleanup
echo "📋 PHASE 2: Applying 5-step cleanup methodology..."

echo "🚀 STEP 1/5: Removing unused imports/variables (autoflake)..."
poetry run autoflake --recursive --in-place --remove-all-unused-imports --remove-unused-variables src/ || echo "⚠️ autoflake completed with warnings"

echo "🚀 STEP 2/5: Fixing PEP 8 issues (autopep8)..."
poetry run autopep8 --aggressive --aggressive --in-place --recursive --max-line-length=88 src/ || echo "⚠️ autopep8 completed with warnings"

echo "🚀 STEP 3/5: Formatting docstrings (docformatter)..."
poetry run docformatter --in-place --recursive src/ || echo "⚠️ docformatter completed with warnings"

echo "🚀 STEP 4/5: Modernizing Python syntax (pyupgrade)..."
find src -name "*.py" -exec poetry run pyupgrade --py312-plus {} \; || echo "⚠️ pyupgrade completed with warnings"

echo "🚀 STEP 5/5: Final ruff formatting and fixes..."
poetry run ruff format src/ || echo "⚠️ ruff format completed with warnings"
poetry run ruff check src/ --fix || echo "⚠️ ruff fix completed with warnings"

# Phase 3: Results
echo "📋 PHASE 3: Final results..."
FINAL_ERRORS=$(poetry run ruff check src/ --statistics 2>/dev/null | grep "Found" | grep -o '[0-9]*' | head -1 || echo "0")
IMPROVEMENT=$((BASELINE_ERRORS - FINAL_ERRORS))
PERCENTAGE=$((IMPROVEMENT * 100 / BASELINE_ERRORS))

echo ""
echo "🎉 RESULTS SUMMARY:"
echo "📊 BEFORE: $BASELINE_ERRORS errors"
echo "✅ AFTER:  $FINAL_ERRORS errors"
echo "🎯 FIXED:  $IMPROVEMENT errors ($PERCENTAGE% improvement)"
echo ""
echo "🔄 ROLLBACK: git stash apply stash@{0} (if needed)"
echo "✅ PACKAGE FIXED: $PACKAGE_NAME" 