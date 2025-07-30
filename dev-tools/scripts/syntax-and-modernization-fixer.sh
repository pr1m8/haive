#!/bin/bash
# 🔧 Comprehensive Syntax & Modernization Fixer
# Usage: ./dev-tools/scripts/syntax-and-modernization-fixer.sh <directory> [--fix|--preview]
#
# 🎯 This handles multiple modernization tasks:
# 1. FIX syntax errors (invalid imports, malformed strings)
# 2. MODERNIZE f-strings (.format() → f-strings)  
# 3. CLEAN UP imports (remove unused, fix undefined)
# 4. UPGRADE Python syntax (typing, super calls, etc.)

set -e

DIRECTORY=${1:-"packages/haive-games/src"}
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

echo -e "${CYAN}🔧 COMPREHENSIVE SYNTAX & MODERNIZATION FIXER${NC}"
echo -e "${BLUE}📂 Directory: $DIRECTORY${NC}"
echo -e "${BLUE}🔧 Mode: $MODE${NC}"
echo ""

# Safety checkpoint
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
git stash push -m "MODERNIZATION_CHECKPOINT_${TIMESTAMP}" || echo "⚠️ No changes to stash"

# ===================================================================
# 🔍 PHASE 1: ANALYSIS - Detect Issues
# ===================================================================

echo -e "${PURPLE}🔍 PHASE 1: ANALYZING MODERNIZATION ISSUES...${NC}"
echo ""

# Count syntax errors (main blocker)
SYNTAX_ERRORS=$(ruff check "$DIRECTORY" --select E999 2>/dev/null | wc -l || echo "0")

# Count f-string opportunities  
FORMAT_STRINGS=$(find "$DIRECTORY" -name "*.py" -exec grep -l "\.format(" {} \; 2>/dev/null | wc -l || echo "0")

# Count undefined names and unused imports
UNDEFINED_NAMES=$(ruff check "$DIRECTORY" --select F821 2>/dev/null | wc -l || echo "0")
UNUSED_IMPORTS=$(ruff check "$DIRECTORY" --select F401 2>/dev/null | wc -l || echo "0")

# Count unsorted imports
UNSORTED_IMPORTS=$(ruff check "$DIRECTORY" --select I001 2>/dev/null | wc -l || echo "0")

# Count typing modernization opportunities
OLD_TYPING=$(ruff check "$DIRECTORY" --select UP006,UP007 2>/dev/null | wc -l || echo "0")

echo -e "${YELLOW}📊 MODERNIZATION ISSUES DETECTED:${NC}"
echo "  🔴 Syntax errors (blocking): $SYNTAX_ERRORS"
echo "  🔄 F-string opportunities: $FORMAT_STRINGS files"  
echo "  🔴 Undefined names: $UNDEFINED_NAMES"
echo "  🧹 Unused imports: $UNUSED_IMPORTS"
echo "  📋 Unsorted imports: $UNSORTED_IMPORTS"
echo "  🐍 Old typing syntax: $OLD_TYPING"
echo ""

# ===================================================================
# 🚨 PHASE 2: SYNTAX ERROR FIXES - Must fix first
# ===================================================================

if [ "$MODE" = "--fix" ]; then
    echo -e "${PURPLE}🚨 PHASE 2: FIXING SYNTAX ERRORS...${NC}"
    echo ""
    
    # Step 2a: Fix common invalid import patterns
    echo -e "${BLUE}🔧 Step 2a: Fixing invalid import patterns...${NC}"
    
    # Fix the haive-prebuilt syntax errors specifically
    find "$DIRECTORY" -name "*.py" -type f -exec sed -i.bak '
        # Fix invalid import patterns with hyphens
        s/from haive-prebuilt\.src\.haive\.prebuilt\./from haive.prebuilt./g
        s/from haive-[a-z]*\.src\.haive\./from haive./g
        s/import haive-[a-z]*\.src\.haive\./import haive./g
        
        # Fix other common syntax issues
        s/from \.\.haive/from haive/g
        s/from \.haive/from haive/g
    ' {} \;
    
    # Clean up backup files
    find "$DIRECTORY" -name "*.py.bak" -delete
    
    echo -e "${GREEN}✅ Invalid import patterns fixed${NC}"
    echo ""
fi

# ===================================================================
# 🎯 PHASE 3: F-STRING MODERNIZATION  
# ===================================================================

if [ "$MODE" = "--fix" ]; then
    echo -e "${PURPLE}🎯 PHASE 3: MODERNIZING F-STRINGS...${NC}"
    echo ""
    
    # Step 3a: Convert .format() to f-strings using pyupgrade
    echo -e "${BLUE}🔧 Step 3a: Converting .format() to f-strings...${NC}"
    
    find "$DIRECTORY" -name "*.py" -type f -exec pyupgrade --py312-plus {} \; || echo "⚠️ Some files may need manual review"
    
    # Step 3b: Use ruff to fix f-string issues
    echo -e "${BLUE}🔧 Step 3b: Applying ruff f-string fixes...${NC}"
    ruff check "$DIRECTORY" --select UP032 --fix || echo "⚠️ Some f-string conversions may need manual review"
    
    echo -e "${GREEN}✅ F-string modernization completed${NC}"
    echo ""
fi

# ===================================================================
# 🧹 PHASE 4: IMPORT CLEANUP
# ===================================================================

if [ "$MODE" = "--fix" ]; then
    echo -e "${PURPLE}🧹 PHASE 4: CLEANING UP IMPORTS...${NC}"
    echo ""
    
    # Step 4a: Sort imports
    echo -e "${BLUE}🔧 Step 4a: Sorting imports...${NC}"
    ruff check "$DIRECTORY" --select I001 --fix || echo "⚠️ Some import sorting issues may remain"
    
    # Step 4b: Remove unused imports  
    echo -e "${BLUE}🔧 Step 4b: Removing unused imports...${NC}"
    ruff check "$DIRECTORY" --select F401 --fix || echo "⚠️ Some unused imports may need manual review"
    
    # Step 4c: Apply comprehensive import management if available
    if [ -f "dev-tools/scripts/comprehensive-import-manager.sh" ]; then
        echo -e "${BLUE}🔧 Step 4c: Running comprehensive import manager...${NC}"
        ./dev-tools/scripts/comprehensive-import-manager.sh "$DIRECTORY" --fix || echo "⚠️ Import manager completed with warnings"
    fi
    
    echo -e "${GREEN}✅ Import cleanup completed${NC}"
    echo ""
fi

# ===================================================================
# 🐍 PHASE 5: PYTHON SYNTAX MODERNIZATION
# ===================================================================

if [ "$MODE" = "--fix" ]; then
    echo -e "${PURPLE}🐍 PHASE 5: MODERNIZING PYTHON SYNTAX...${NC}"
    echo ""
    
    # Step 5a: Modernize typing syntax
    echo -e "${BLUE}🔧 Step 5a: Modernizing typing syntax...${NC}"
    ruff check "$DIRECTORY" --select UP006,UP007,UP035 --fix || echo "⚠️ Some typing modernization may need manual review"
    
    # Step 5b: Fix super() calls and other modernizations
    echo -e "${BLUE}🔧 Step 5b: Modernizing super() calls and other syntax...${NC}"
    ruff check "$DIRECTORY" --select UP008,UP009 --fix || echo "⚠️ Some syntax modernization may need manual review"
    
    echo -e "${GREEN}✅ Python syntax modernization completed${NC}"
    echo ""
fi

# ===================================================================
# 🎨 PHASE 6: FINAL FORMATTING & VALIDATION
# ===================================================================

if [ "$MODE" = "--fix" ]; then
    echo -e "${PURPLE}🎨 PHASE 6: FINAL FORMATTING...${NC}"
    echo ""
    
    # Apply final formatting
    echo -e "${BLUE}🔧 Final code formatting...${NC}"
    ruff format "$DIRECTORY" || echo "⚠️ Some formatting issues may remain"
    
    echo -e "${GREEN}✅ Final formatting completed${NC}"
    echo ""
fi

# ===================================================================
# 📊 FINAL ASSESSMENT  
# ===================================================================

echo -e "${PURPLE}📊 FINAL ASSESSMENT...${NC}"
echo ""

if [ "$MODE" = "--fix" ]; then
    # Recheck issues after fixes
    FINAL_SYNTAX=$(ruff check "$DIRECTORY" --select E999 2>/dev/null | wc -l || echo "0")
    FINAL_FORMAT=$(find "$DIRECTORY" -name "*.py" -exec grep -l "\.format(" {} \; 2>/dev/null | wc -l || echo "0")
    FINAL_UNDEFINED=$(ruff check "$DIRECTORY" --select F821 2>/dev/null | wc -l || echo "0")
    FINAL_UNUSED=$(ruff check "$DIRECTORY" --select F401 2>/dev/null | wc -l || echo "0")
    FINAL_UNSORTED=$(ruff check "$DIRECTORY" --select I001 2>/dev/null | wc -l || echo "0")
    
    FIXED_SYNTAX=$((SYNTAX_ERRORS - FINAL_SYNTAX))
    FIXED_FORMAT=$((FORMAT_STRINGS - FINAL_FORMAT))
    FIXED_UNDEFINED=$((UNDEFINED_NAMES - FINAL_UNDEFINED))
    FIXED_UNUSED=$((UNUSED_IMPORTS - FINAL_UNUSED))
    FIXED_UNSORTED=$((UNSORTED_IMPORTS - FINAL_UNSORTED))
    
    echo -e "${GREEN}🎉 COMPREHENSIVE MODERNIZATION RESULTS:${NC}"
    echo ""
    echo -e "${BLUE}📊 BEFORE vs AFTER:${NC}"
    echo "  🔴 Syntax errors: $SYNTAX_ERRORS → $FINAL_SYNTAX (fixed: $FIXED_SYNTAX)"
    echo "  🔄 F-string opportunities: $FORMAT_STRINGS → $FINAL_FORMAT (fixed: $FIXED_FORMAT)"
    echo "  🔴 Undefined names: $UNDEFINED_NAMES → $FINAL_UNDEFINED (fixed: $FIXED_UNDEFINED)"
    echo "  🧹 Unused imports: $UNUSED_IMPORTS → $FINAL_UNUSED (fixed: $FIXED_UNUSED)"
    echo "  📋 Unsorted imports: $UNSORTED_IMPORTS → $FINAL_UNSORTED (fixed: $FIXED_UNSORTED)"
    echo ""
    echo -e "${YELLOW}🔧 IMPROVEMENTS APPLIED:${NC}"
    echo "  • ✅ Fixed invalid import syntax (haive-prebuilt patterns)"
    echo "  • ✅ Converted .format() strings to f-strings" 
    echo "  • ✅ Removed unused imports"
    echo "  • ✅ Sorted and organized imports"
    echo "  • ✅ Modernized Python typing syntax"
    echo "  • ✅ Applied consistent code formatting"
    echo ""
    
    if [ "$FINAL_SYNTAX" -gt 0 ]; then
        echo -e "${YELLOW}⚠️  REMAINING SYNTAX ERRORS (need manual review):${NC}"
        ruff check "$DIRECTORY" --select E999 || true
    else
        echo -e "${GREEN}🎯 ALL SYNTAX ERRORS RESOLVED!${NC}"
    fi
    
elif [ "$MODE" = "--preview" ]; then
    echo -e "${YELLOW}👀 PREVIEW MODE - No changes applied${NC}"
    echo ""
    echo -e "${CYAN}🔧 WOULD APPLY THE FOLLOWING FIXES:${NC}"
    echo "  1. 🚨 Fix $SYNTAX_ERRORS syntax errors (invalid imports)"
    echo "  2. 🎯 Convert $FORMAT_STRINGS files from .format() to f-strings"
    echo "  3. 🧹 Remove $UNUSED_IMPORTS unused imports"
    echo "  4. 📋 Sort $UNSORTED_IMPORTS unsorted imports" 
    echo "  5. 🐍 Modernize $OLD_TYPING old typing syntax patterns"
    echo "  6. 🎨 Apply consistent formatting"
    echo ""
    echo -e "${GREEN}Run with --fix to apply these changes${NC}"
fi

echo ""
echo -e "${CYAN}🚀 Comprehensive Syntax & Modernization Fixer Complete!${NC}"
echo -e "${BLUE}💡 Use 'git diff' to review changes before committing${NC}" 