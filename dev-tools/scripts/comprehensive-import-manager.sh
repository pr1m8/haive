#!/bin/bash
# 📦 Comprehensive Import Manager - 3-Way Import Handling for Namespaced Poly Repo
# Usage: ./dev-tools/scripts/comprehensive-import-manager.sh <directory> [--fix|--preview]
#
# 🎯 This handles the 2-3 way import management:
# 1. DETECT & REMOVE bad imports (relative imports, wrong namespaces)
# 2. ADD missing imports (autoimport with namespace awareness)  
# 3. ORGANIZE & CLEAN (isort + ruff for final cleanup)

set -e

DIRECTORY=${1:-"src/"}
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

echo -e "${CYAN}🚀 COMPREHENSIVE IMPORT MANAGER - NAMESPACED POLY REPO${NC}"
echo -e "${BLUE}📂 Directory: $DIRECTORY${NC}"
echo -e "${BLUE}🔧 Mode: $MODE${NC}"
echo ""

# Safety checkpoint
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
git stash push -m "IMPORT_MANAGER_CHECKPOINT_${TIMESTAMP}" || echo "⚠️ No changes to stash"

# ===================================================================
# 🔍 PHASE 1: ANALYSIS - Detect Import Issues
# ===================================================================

echo -e "${PURPLE}🔍 PHASE 1: ANALYZING IMPORT ISSUES...${NC}"
echo ""

# Count different types of import issues
RELATIVE_IMPORTS=$(find "$DIRECTORY" -name "*.py" -exec grep -l "from \.\|import \." {} \; 2>/dev/null | wc -l || echo "0")
BAD_NAMESPACE_IMPORTS=$(find "$DIRECTORY" -name "*.py" -exec grep -l "from src\.haive\|import src\.haive\|from packages\.haive" {} \; 2>/dev/null | wc -l || echo "0")
UNDEFINED_NAMES=$(poetry run ruff check "$DIRECTORY" --select F821 2>/dev/null | wc -l || echo "0")
UNUSED_IMPORTS=$(poetry run ruff check "$DIRECTORY" --select F401 2>/dev/null | wc -l || echo "0")
IMPORT_ERRORS=$(poetry run ruff check "$DIRECTORY" --select I001,F401,F821 2>/dev/null | wc -l || echo "0")

echo -e "${YELLOW}📊 IMPORT ISSUES DETECTED:${NC}"
echo "  🔴 Relative imports (should be absolute): $RELATIVE_IMPORTS files"
echo "  🔴 Bad namespace imports (src.haive, packages.haive): $BAD_NAMESPACE_IMPORTS files"  
echo "  🔴 Undefined names (missing imports): $UNDEFINED_NAMES issues"
echo "  🔴 Unused imports: $UNUSED_IMPORTS issues"
echo "  📊 Total import-related issues: $IMPORT_ERRORS"
echo ""

# ===================================================================
# 🧹 PHASE 2: BAD IMPORT REMOVAL - Clean up incorrect imports
# ===================================================================

if [ "$MODE" = "--fix" ]; then
    echo -e "${PURPLE}🧹 PHASE 2: REMOVING BAD IMPORTS...${NC}"
    echo ""
    
    # Step 2a: Remove relative imports and replace with absolute
    echo -e "${BLUE}🔧 Step 2a: Converting relative to absolute imports...${NC}"
    find "$DIRECTORY" -name "*.py" -type f -exec sed -i.bak '
        # Convert relative imports to absolute haive imports
        s/from \.\.haive/from haive/g
        s/from \.haive/from haive/g  
        s/import \.\.haive/import haive/g
        s/import \.haive/import haive/g
        
        # Fix bad namespace patterns
        s/from src\.haive/from haive/g
        s/import src\.haive/import haive/g
        s/from packages\.haive/from haive/g
        s/import packages\.haive/import haive/g
    ' {} \;
    
    # Clean up backup files
    find "$DIRECTORY" -name "*.py.bak" -delete
    
    # Step 2b: Use ruff to catch and fix import violations
    echo -e "${BLUE}🔧 Step 2b: Using ruff to enforce absolute imports...${NC}"
    poetry run ruff check "$DIRECTORY" --select TID251,TID252,TID253 --fix || echo "⚠️ Some import violations need manual review"
    
    echo -e "${GREEN}✅ Bad import removal completed${NC}"
    echo ""
fi

# ===================================================================  
# 📦 PHASE 3: MISSING IMPORT ADDITION - Add missing imports
# ===================================================================

if [ "$MODE" = "--fix" ]; then
    echo -e "${PURPLE}📦 PHASE 3: ADDING MISSING IMPORTS...${NC}"
    echo ""
    
    # Step 3a: Install autoimport if needed
    if ! poetry show autoimport >/dev/null 2>&1; then
        echo -e "${BLUE}📥 Installing autoimport...${NC}"
        poetry add --group dev autoimport
    fi
    
    # Step 3b: Run autoimport with namespace awareness
    echo -e "${BLUE}🔧 Step 3a: Adding missing imports (autoimport)...${NC}"
    poetry run autoimport "$DIRECTORY" || echo "⚠️ autoimport completed with warnings"
    
    # Step 3c: Handle common haive namespace imports manually
    echo -e "${BLUE}🔧 Step 3b: Adding common haive namespace imports...${NC}"
    find "$DIRECTORY" -name "*.py" -type f -exec python3 -c "
import re
import sys

def add_missing_haive_imports(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    lines = content.split('\n')
    
    # Check for common patterns that need haive imports
    needs_core = re.search(r'\bhaive\.core\b', content) and not re.search(r'from haive import core|import haive\.core', content)
    needs_agents = re.search(r'\bhaive\.agents\b', content) and not re.search(r'from haive import agents|import haive\.agents', content)
    needs_tools = re.search(r'\bhaive\.tools\b', content) and not re.search(r'from haive import tools|import haive\.tools', content)
    needs_games = re.search(r'\bhaive\.games\b', content) and not re.search(r'from haive import games|import haive\.games', content)
    
    # Find insertion point (after existing imports)
    insert_line = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('import ') or line.strip().startswith('from '):
            insert_line = i + 1
        elif line.strip() == '' and insert_line > 0:
            break
    
    # Add missing imports
    new_imports = []
    if needs_core:
        new_imports.append('from haive import core')
    if needs_agents:
        new_imports.append('from haive import agents')  
    if needs_tools:
        new_imports.append('from haive import tools')
    if needs_games:
        new_imports.append('from haive import games')
    
    if new_imports:
        lines[insert_line:insert_line] = new_imports + ['']
        content = '\n'.join(lines)
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f'Added imports to {filepath}: {new_imports}')

add_missing_haive_imports(sys.argv[1])
" {} \;
    
    echo -e "${GREEN}✅ Missing import addition completed${NC}"
    echo ""
fi

# ===================================================================
# 🎯 PHASE 4: IMPORT ORGANIZATION - Final cleanup and organization  
# ===================================================================

if [ "$MODE" = "--fix" ]; then
    echo -e "${PURPLE}🎯 PHASE 4: ORGANIZING IMPORTS...${NC}"
    echo ""
    
    # Step 4a: Sort and organize with isort
    echo -e "${BLUE}🔧 Step 4a: Organizing imports (isort)...${NC}"
    poetry run isort "$DIRECTORY" || echo "⚠️ isort completed with warnings"
    
    # Step 4b: Final cleanup with ruff
    echo -e "${BLUE}🔧 Step 4b: Final import cleanup (ruff)...${NC}"
    poetry run ruff check "$DIRECTORY" --select I,F401 --fix || echo "⚠️ ruff completed with warnings"
    
    # Step 4c: Format code to ensure consistency
    echo -e "${BLUE}🔧 Step 4c: Code formatting (ruff format)...${NC}"
    poetry run ruff format "$DIRECTORY" || echo "⚠️ ruff format completed with warnings"
    
    echo -e "${GREEN}✅ Import organization completed${NC}"
    echo ""
fi

# ===================================================================
# 📊 FINAL ASSESSMENT  
# ===================================================================

echo -e "${PURPLE}📊 FINAL ASSESSMENT...${NC}"
echo ""

if [ "$MODE" = "--fix" ]; then
    # Recheck issues after fixes
    FINAL_RELATIVE=$(find "$DIRECTORY" -name "*.py" -exec grep -l "from \.\|import \." {} \; 2>/dev/null | wc -l || echo "0")
    FINAL_BAD_NAMESPACE=$(find "$DIRECTORY" -name "*.py" -exec grep -l "from src\.haive\|import src\.haive" {} \; 2>/dev/null | wc -l || echo "0")
    FINAL_ERRORS=$(poetry run ruff check "$DIRECTORY" --select I001,F401,F821 2>/dev/null | wc -l || echo "0")
    
    FIXED_RELATIVE=$((RELATIVE_IMPORTS - FINAL_RELATIVE))
    FIXED_BAD_NAMESPACE=$((BAD_NAMESPACE_IMPORTS - FINAL_BAD_NAMESPACE))
    FIXED_TOTAL=$((IMPORT_ERRORS - FINAL_ERRORS))
    
    echo -e "${GREEN}🎉 COMPREHENSIVE IMPORT MANAGEMENT RESULTS:${NC}"
    echo ""
    echo -e "${BLUE}📊 BEFORE vs AFTER:${NC}"
    echo "  🔴 Relative imports: $RELATIVE_IMPORTS → $FINAL_RELATIVE (fixed: $FIXED_RELATIVE)"
    echo "  🔴 Bad namespace imports: $BAD_NAMESPACE_IMPORTS → $FINAL_BAD_NAMESPACE (fixed: $FIXED_BAD_NAMESPACE)"
    echo "  📊 Total import issues: $IMPORT_ERRORS → $FINAL_ERRORS (fixed: $FIXED_TOTAL)"
    echo ""
    echo -e "${YELLOW}🔧 IMPROVEMENTS APPLIED:${NC}"
    echo "  • ✅ Converted relative imports to absolute haive.* namespace"
    echo "  • ✅ Removed bad namespace patterns (src.haive, packages.haive)"
    echo "  • ✅ Added missing imports automatically"
    echo "  • ✅ Organized imports into proper sections (stdlib, 3rd party, haive)"
    echo "  • ✅ Removed unused import statements"
    echo "  • ✅ Applied consistent import ordering and formatting"
    echo ""
    
    if [ "$FINAL_ERRORS" -gt 0 ]; then
        echo -e "${YELLOW}⚠️  REMAINING ISSUES (may need manual review):${NC}"
        poetry run ruff check "$DIRECTORY" --select I001,F401,F821 || true
    else
        echo -e "${GREEN}🎯 ALL IMPORT ISSUES RESOLVED!${NC}"
    fi
    
elif [ "$MODE" = "--preview" ]; then
    echo -e "${YELLOW}👀 PREVIEW MODE - No changes applied${NC}"
    echo ""
    echo -e "${CYAN}🔧 WOULD APPLY THE FOLLOWING FIXES:${NC}"
    echo "  1. 🧹 Convert $RELATIVE_IMPORTS files with relative imports to absolute"
    echo "  2. 🧹 Fix $BAD_NAMESPACE_IMPORTS files with bad namespace patterns"
    echo "  3. 📦 Add missing imports using autoimport + custom haive namespace logic"
    echo "  4. 🎯 Organize all imports with isort + ruff cleanup"
    echo "  5. 🎨 Apply consistent formatting"
    echo ""
    echo -e "${GREEN}Run with --fix to apply these changes${NC}"
fi

echo ""
echo -e "${CYAN}🚀 Comprehensive Import Manager Complete!${NC}"
echo -e "${BLUE}💡 Use 'git diff' to review changes before committing${NC}" 