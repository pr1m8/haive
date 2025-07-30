#!/bin/bash
# 🔧 Debug and Fix Syntax Issues - Safe Edition
# Usage: ./dev-tools/scripts/debug-and-fix-syntax.sh <directory> [--fix|--preview]
#
# 🎯 This safely handles syntax issues in order:
# 1. ANALYZE and DEBUG what's actually broken
# 2. FIX invalid imports (haive-package patterns)
# 3. FIX indentation errors using reindent 
# 4. SHOW git diffs for review
# 5. SAFE rollback if needed

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

echo -e "${CYAN}🔧 DEBUG AND FIX SYNTAX ISSUES - SAFE EDITION${NC}"
echo -e "${BLUE}📂 Directory: $DIRECTORY${NC}"
echo -e "${BLUE}🔧 Mode: $MODE${NC}"
echo ""

# ===================================================================
# 🛡️ SAFETY CHECKPOINT - Always create before any changes
# ===================================================================

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
echo -e "${PURPLE}🛡️ Creating safety checkpoint...${NC}"
git stash push -m "DEBUG_SYNTAX_CHECKPOINT_${TIMESTAMP}" || echo "⚠️ No changes to stash"

# ===================================================================
# 🔍 PHASE 1: DEBUG - Find the actual problems
# ===================================================================

echo -e "${PURPLE}🔍 PHASE 1: DEBUGGING SYNTAX ISSUES...${NC}"
echo ""

# Find files with obvious syntax errors
echo -e "${BLUE}🔍 Scanning for Python syntax errors...${NC}"

SYNTAX_ERROR_FILES=()
INVALID_IMPORT_FILES=()
INDENTATION_ERROR_FILES=()

# Check each Python file individually
while IFS= read -r -d '' file; do
    # Check for invalid import patterns
    if grep -q "from haive-[^.]*\.src\.haive\." "$file" 2>/dev/null; then
        INVALID_IMPORT_FILES+=("$file")
    fi
    
    # Try to parse with Python to catch syntax errors
    if ! python3 -m py_compile "$file" 2>/dev/null; then
        SYNTAX_ERROR_FILES+=("$file")
        
        # Check if it's an indentation error specifically
        if python3 -m py_compile "$file" 2>&1 | grep -q "IndentationError\|unindent"; then
            INDENTATION_ERROR_FILES+=("$file")
        fi
    fi
done < <(find "$DIRECTORY" -name "*.py" -print0)

echo -e "${YELLOW}📊 SYNTAX ISSUES DETECTED:${NC}"
echo "  🔴 Files with invalid imports: ${#INVALID_IMPORT_FILES[@]}"
echo "  🔴 Files with syntax errors: ${#SYNTAX_ERROR_FILES[@]}"
echo "  🔴 Files with indentation errors: ${#INDENTATION_ERROR_FILES[@]}"
echo ""

# Show specific problematic files
if [ ${#INVALID_IMPORT_FILES[@]} -gt 0 ]; then
    echo -e "${BLUE}🔍 Files with invalid import patterns:${NC}"
    printf '  %s\n' "${INVALID_IMPORT_FILES[@]}" | head -5
    [ ${#INVALID_IMPORT_FILES[@]} -gt 5 ] && echo "  ... and $((${#INVALID_IMPORT_FILES[@]} - 5)) more"
    echo ""
fi

if [ ${#INDENTATION_ERROR_FILES[@]} -gt 0 ]; then
    echo -e "${BLUE}🔍 Files with indentation errors:${NC}"
    printf '  %s\n' "${INDENTATION_ERROR_FILES[@]}" | head -5
    [ ${#INDENTATION_ERROR_FILES[@]} -gt 5 ] && echo "  ... and $((${#INDENTATION_ERROR_FILES[@]} - 5)) more"
    echo ""
fi

# ===================================================================
# 🚨 PHASE 2: FIX INVALID IMPORTS - Must fix first
# ===================================================================

if [ "$MODE" = "--fix" ] && [ ${#INVALID_IMPORT_FILES[@]} -gt 0 ]; then
    echo -e "${PURPLE}🚨 PHASE 2: FIXING INVALID IMPORT PATTERNS...${NC}"
    echo ""
    
    for file in "${INVALID_IMPORT_FILES[@]}"; do
        echo -e "${BLUE}🔧 Fixing imports in: $(basename "$file")${NC}"
        
        # Create backup
        cp "$file" "$file.backup"
        
        # Fix invalid import patterns
        sed -i '
            # Fix the main problematic patterns
            s/from haive-prebuilt\.src\.haive\.prebuilt\./from haive.prebuilt./g
            s/from haive-[a-z]*\.src\.haive\./from haive./g
            s/import haive-[a-z]*\.src\.haive\./import haive./g
            s/from haive-[a-z]*\.tests\./from haive./g
        ' "$file"
        
        # Check if fix worked
        if python3 -m py_compile "$file" 2>/dev/null; then
            echo "  ✅ Import fixes successful"
            rm "$file.backup"
        else
            echo "  ⚠️ Still has syntax errors, but imports fixed"
            rm "$file.backup"
        fi
    done
    
    echo -e "${GREEN}✅ Invalid import patterns fixed${NC}"
    echo ""
fi

# ===================================================================
# 🔧 PHASE 3: FIX INDENTATION ERRORS
# ===================================================================

if [ "$MODE" = "--fix" ] && [ ${#INDENTATION_ERROR_FILES[@]} -gt 0 ]; then
    echo -e "${PURPLE}🔧 PHASE 3: FIXING INDENTATION ERRORS...${NC}"
    echo ""
    
    # Try to fix indentation for files that still have errors
    FIXED_FILES=()
    
    for file in "${INDENTATION_ERROR_FILES[@]}"; do
        echo -e "${BLUE}🔧 Fixing indentation in: $(basename "$file")${NC}"
        
        # Create backup
        cp "$file" "$file.backup"
        
        # Try using reindent (Tim Peters' tool)
        if poetry run python -m reindent -n "$file" 2>/dev/null; then
            # Check if it's now syntactically valid
            if python3 -m py_compile "$file" 2>/dev/null; then
                echo "  ✅ Indentation fixed with reindent"
                FIXED_FILES+=("$file")
                rm "$file.backup"
            else
                # Try autopep8 aggressive mode
                if poetry run autopep8 --aggressive --aggressive --in-place "$file" 2>/dev/null; then
                    if python3 -m py_compile "$file" 2>/dev/null; then
                        echo "  ✅ Indentation fixed with autopep8"
                        FIXED_FILES+=("$file")
                        rm "$file.backup"
                    else
                        echo "  ⚠️ Still has errors after autopep8"
                        mv "$file.backup" "$file"  # Restore backup
                    fi
                else
                    echo "  ⚠️ Could not fix with autopep8"
                    mv "$file.backup" "$file"  # Restore backup
                fi
            fi
        else
            echo "  ⚠️ Reindent could not process file"
            mv "$file.backup" "$file"  # Restore backup
        fi
    done
    
    echo -e "${GREEN}✅ Fixed indentation in ${#FIXED_FILES[@]} files${NC}"
    echo ""
fi

# ===================================================================
# 📊 PHASE 4: SHOW RESULTS AND DIFFS
# ===================================================================

echo -e "${PURPLE}📊 SHOWING RESULTS...${NC}"
echo ""

if [ "$MODE" = "--fix" ]; then
    # Show what was changed
    if git diff --quiet; then
        echo -e "${YELLOW}ℹ️  No changes were made${NC}"
    else
        echo -e "${GREEN}🎉 CHANGES APPLIED:${NC}"
        echo ""
        
        # Show summary of changed files
        echo -e "${BLUE}📋 Modified files:${NC}"
        git diff --name-only | while read -r file; do
            echo "  📝 $file"
        done
        echo ""
        
        # Show sample diff for first few files
        echo -e "${BLUE}🔍 Sample changes (first 3 files):${NC}"
        git diff --name-only | head -3 | while read -r file; do
            echo ""
            echo -e "${CYAN}📄 Changes in $file:${NC}"
            git diff "$file" | head -20
            if [ $(git diff "$file" | wc -l) -gt 20 ]; then
                echo "  ... (truncated, use 'git diff $file' to see all)"
            fi
        done
        
        echo ""
        echo -e "${YELLOW}💡 TO REVIEW ALL CHANGES:${NC}"
        echo "  git diff                    # See all changes"
        echo "  git diff --stat             # Summary of changes" 
        echo "  git stash                   # Stash changes to review later"
        echo ""
        echo -e "${YELLOW}💡 TO COMMIT CHANGES:${NC}"
        echo "  git add ."
        echo "  git commit -m 'Fix syntax and indentation errors'"
        echo ""
        echo -e "${YELLOW}💡 TO ROLLBACK:${NC}"
        echo "  git stash"
        echo "  git stash apply stash@{1}   # Restore checkpoint"
    fi
    
    # Recheck syntax errors
    REMAINING_SYNTAX_FILES=()
    while IFS= read -r -d '' file; do
        if ! python3 -m py_compile "$file" 2>/dev/null; then
            REMAINING_SYNTAX_FILES+=("$file")
        fi
    done < <(find "$DIRECTORY" -name "*.py" -print0)
    
    echo -e "${BLUE}📊 FINAL STATUS:${NC}"
    echo "  🔴 Original syntax error files: ${#SYNTAX_ERROR_FILES[@]}"
    echo "  🔴 Remaining syntax error files: ${#REMAINING_SYNTAX_FILES[@]}"
    echo "  ✅ Fixed files: $((${#SYNTAX_ERROR_FILES[@]} - ${#REMAINING_SYNTAX_FILES[@]}))"
    
    if [ ${#REMAINING_SYNTAX_FILES[@]} -eq 0 ]; then
        echo ""
        echo -e "${GREEN}🎯 ALL SYNTAX ERRORS RESOLVED!${NC}"
    elif [ ${#REMAINING_SYNTAX_FILES[@]} -lt ${#SYNTAX_ERROR_FILES[@]} ]; then
        echo ""
        echo -e "${YELLOW}📈 PROGRESS MADE! Fixed $((${#SYNTAX_ERROR_FILES[@]} - ${#REMAINING_SYNTAX_FILES[@]})) files${NC}"
        echo -e "${BLUE}🔍 Remaining problem files:${NC}"
        printf '  %s\n' "${REMAINING_SYNTAX_FILES[@]}" | head -5
    fi
    
elif [ "$MODE" = "--preview" ]; then
    echo -e "${YELLOW}👀 PREVIEW MODE - Would apply the following fixes:${NC}"
    echo ""
    echo -e "${CYAN}🔧 WOULD FIX:${NC}"
    echo "  1. 🚨 Fix ${#INVALID_IMPORT_FILES[@]} files with invalid import patterns"
    echo "  2. 🔧 Fix ${#INDENTATION_ERROR_FILES[@]} files with indentation errors"
    echo "  3. 📊 Show git diffs for review"
    echo ""
    echo -e "${GREEN}Run with --fix to apply these changes${NC}"
fi

echo ""
echo -e "${CYAN}🚀 Debug and Fix Syntax Complete!${NC}"
echo -e "${BLUE}💡 Safe rollback available via git stash if needed${NC}" 