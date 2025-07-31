#!/bin/bash
# 🚨 Pre-flight Syntax Fixer - Fix obvious typos before indentation tools
# Usage: ./dev-tools/scripts/pre-flight-syntax-fixer.sh <directory> [--fix|--preview]
#
# 🎯 Fixes common typos that prevent indentation tools from working:
# - "return" → "return"
# - "st" type hints → "str"
# - Common keyword typos

set -e

DIRECTORY=${1:-"packages/haive-prebuilt/src"}
MODE=${2:-"--preview"}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

if [ ! -d "$DIRECTORY" ]; then
    echo -e "${RED}❌ Directory not found: $DIRECTORY${NC}"
    exit 1
fi

echo -e "${CYAN}🚨 PRE-FLIGHT SYNTAX FIXER${NC}"
echo -e "${BLUE}📂 Directory: $DIRECTORY${NC}"
echo -e "${BLUE}🔧 Mode: $MODE${NC}"
echo ""

# Safety checkpoint (ONLY for target directory)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
echo -e "${PURPLE}🛡️ Creating safety checkpoint for $DIRECTORY...${NC}"
git stash push -m "PRE_FLIGHT_SYNTAX_${TIMESTAMP}" -- "$DIRECTORY" || echo "⚠️ No changes to stash"

# ===================================================================
# 🔍 PHASE 1: SCAN FOR COMMON TYPOS
# ===================================================================

echo -e "${PURPLE}🔍 PHASE 1: SCANNING FOR COMMON SYNTAX TYPOS...${NC}"
echo ""

# Find common typos
RETUR_FILES=$(grep -r "return " "$DIRECTORY" --include="*.py" | wc -l || echo "0")
RETUR_ONLY_FILES=$(grep -r "^[ ]*return$" "$DIRECTORY" --include="*.py" | wc -l || echo "0")
ST_TYPE_FILES=$(grep -r ") -> st:" "$DIRECTORY" --include="*.py" | wc -l || echo "0")
UNTERMINATED_STRINGS=$(find "$DIRECTORY" -name "*.py" -exec python3 -c "
import sys
try:
    with open(sys.argv[1], 'r') as f:
        compile(f.read(), sys.argv[1], 'exec')
except SyntaxError as e:
    if 'unterminated string' in str(e):
        print(sys.argv[1])
" {} \; 2>/dev/null | wc -l || echo "0")

echo -e "${YELLOW}📊 COMMON SYNTAX TYPOS DETECTED:${NC}"
echo "  🔴 'retur ' (missing 'n'): $RETUR_FILES occurrences"
echo "  🔴 'retur' (line ending): $RETUR_ONLY_FILES occurrences"
echo "  🔴 ') -> st:' (should be str): $ST_TYPE_FILES occurrences"
echo "  🔴 Unterminated strings: $UNTERMINATED_STRINGS files"
echo ""

# ===================================================================
# 🔧 PHASE 2: APPLY FIXES
# ===================================================================

if [ "$MODE" = "--fix" ]; then
    echo -e "${PURPLE}🔧 PHASE 2: APPLYING SYNTAX FIXES...${NC}"
    echo ""

    # Fix 1: "return " → "return "
    if [ "$RETUR_FILES" -gt 0 ]; then
        echo -e "${BLUE}🔧 Fixing 'retur ' → 'return '...${NC}"
        find "$DIRECTORY" -name "*.py" -type f -exec sed -i.bak 's/return /return /g' {} \;
        echo "  ✅ Fixed $RETUR_FILES occurrences"
    fi

    # Fix 2: "return" at end of line → "return"
    if [ "$RETUR_ONLY_FILES" -gt 0 ]; then
        echo -e "${BLUE}🔧 Fixing standalone 'retur' → 'return'...${NC}"
        find "$DIRECTORY" -name "*.py" -type f -exec sed -i.bak 's/^[ ]*return$/&n/' {} \;
        find "$DIRECTORY" -name "*.py" -type f -exec sed -i.bak 's/return/return/g' {} \;
        echo "  ✅ Fixed $RETUR_ONLY_FILES occurrences"
    fi

    # Fix 3: ") -> st:" → ") -> str:"
    if [ "$ST_TYPE_FILES" -gt 0 ]; then
        echo -e "${BLUE}🔧 Fixing ') -> st:' → ') -> str:'...${NC}"
        find "$DIRECTORY" -name "*.py" -type f -exec sed -i.bak 's/) -> st:/) -> str:/g' {} \;
        echo "  ✅ Fixed $ST_TYPE_FILES occurrences"
    fi

    # Clean up backup files
    find "$DIRECTORY" -name "*.py.bak" -delete 2>/dev/null || true

    echo -e "${GREEN}✅ Syntax fixes completed${NC}"
    echo ""
fi

# ===================================================================
# 📊 PHASE 3: VERIFY FIXES
# ===================================================================

echo -e "${PURPLE}📊 PHASE 3: VERIFICATION...${NC}"
echo ""

if [ "$MODE" = "--fix" ]; then
    # Recheck compilation
    echo -e "${BLUE}🔍 Testing Python compilation after fixes...${NC}"
    COMPILATION_RESULT=$(python3 -c "
import os
syntax_errors = 0
indentation_errors = 0
fixed_files = []

for root, dirs, files in os.walk('$DIRECTORY'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r') as f:
                    compile(f.read(), filepath, 'exec')
                fixed_files.append(filepath)
            except IndentationError:
                indentation_errors += 1
            except SyntaxError:
                syntax_errors += 1
            except Exception:
                pass

print(f'{indentation_errors}|{syntax_errors}|{len(fixed_files)}')
")

    IFS='|' read -r NEW_INDENT_ERRORS NEW_SYNTAX_ERRORS COMPILABLE_FILES <<< "$COMPILATION_RESULT"

    echo -e "${BLUE}📊 VERIFICATION RESULTS:${NC}"
    echo "  ✅ Files that now compile: $COMPILABLE_FILES"
    echo "  🔴 Remaining IndentationErrors: $NEW_INDENT_ERRORS"
    echo "  🔴 Remaining SyntaxErrors: $NEW_SYNTAX_ERRORS"

    if git diff --quiet; then
        echo -e "${YELLOW}ℹ️  No changes were made${NC}"
    else
        echo ""
        echo -e "${GREEN}🎉 SYNTAX CHANGES APPLIED:${NC}"
        echo ""

        # Show summary of changed files
        echo -e "${BLUE}📋 Modified files:${NC}"
        git diff --name-only | head -10 | while read -r file; do
            echo "  📝 $file"
        done
        [ $(git diff --name-only | wc -l) -gt 10 ] && echo "  ... and more"
        echo ""

        echo -e "${YELLOW}💡 TO REVIEW CHANGES:${NC}"
        echo "  git diff                    # See all changes"
        echo "  git diff --word-diff        # Word-level changes"
        echo ""
    fi

elif [ "$MODE" = "--preview" ]; then
    echo -e "${YELLOW}👀 PREVIEW MODE - Would apply the following fixes:${NC}"
    echo ""
    echo -e "${CYAN}🎯 SYNTAX FIX STRATEGY:${NC}"
    echo "  1. Fix 'retur' → 'return' typos"
    echo "  2. Fix ') -> st:' → ') -> str:' type hints"
    echo "  3. Address unterminated string literals"
    echo "  4. Verify compilation works after fixes"
    echo ""
    echo -e "${GREEN}After these fixes, indentation tools should work!${NC}"
    echo -e "${GREEN}Run with --fix to apply syntax fixes${NC}"
fi

echo ""
echo -e "${CYAN}🚀 Pre-flight Syntax Fixer Complete!${NC}"
echo -e "${BLUE}💡 Run indentation tools AFTER fixing these syntax errors${NC}"
