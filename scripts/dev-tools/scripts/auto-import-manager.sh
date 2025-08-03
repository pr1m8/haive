#!/bin/bash
# 📦 Auto-Import Manager - Comprehensive Import Organization
# Usage: ./dev-tools/scripts/auto-import-manager.sh <directory> [--fix|--preview]

set -e

DIRECTORY=${1:-"src/"}
MODE=${2:-"--preview"}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

if [[ ! -d "${DIRECTORY}" ]]; then
	echo -e "${RED}❌ Directory not found${ $DIRECTO}RY${NC}"
	exit 1
fi

echo -e "${CYAN}📦 AUTO-IMPORT MANAGER${NC}"
echo -e "${BLUE}Directory: ${DIRECTORY}${NC}"
echo ""

# Safety checkpoint (ONLY for target directory)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
git stash push -m "AUTO_IMPORT_CHECKPOINT_${TIMESTAMP}" -- "${DIRECTORY}" || echo "⚠️ No changes to stash"

# Check and install required tools
echo -e "${BLUE}🔍 Checking import management tools...${NC}"

TOOLS_TO_INSTALL=()

# Check for autoimport (missing imports)
if ! poetry show autoimport >/dev/null 2>&1; then
	TOOLS_TO_INSTALL+=("autoimport")
fi

# Check for reorder-python-imports (import ordering)
if ! poetry show reorder-python-imports >/dev/null 2>&1; then
	TOOLS_TO_INSTALL+=("reorder-python-imports")
fi

# Check for isort (already have this, but verify)
if ! poetry show isort >/dev/null 2>&1; then
	TOOLS_TO_INSTALL+=("isort")
fi

# Install missing tools
if [[ ${#TOOLS_TO_INSTALL[@]} -gt 0 ]]; then
	echo -e "${YELLOW}📦 Installing missing tools: ${TOOLS_TO_INSTALL[*]}${NC}"
	for tool in "${TOOLS_TO_INSTALL[@]}"; do
		poetry add --group dev "${tool}"
	done
fi

echo -e "${GREEN}✅ All import tools ready${NC}"
echo ""

# Analyze current import issues
echo -e "${BLUE}📊 ANALYZING IMPORT ISSUES...${NC}"

# Count various import issues
MISSING_IMPORTS=$(poetry run python -c "
import ast
import os
import sys

missing_count = 0
for root, dirs, files in os.walk('${DIRECTORY}'):
    for file in files:
        if file.endswith('.py'):
            try:
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    # Simple heuristic: look for common undefined names
                    if 'pandas' in content and 'import pandas' not in content:
                        missing_count += 1
                    elif 'np.' in content and 'import numpy' not in content:
                        missing_count += 1
                    elif 'os.path' in content and 'import os' not in content:
                        missing_count += 1
            except:
                pass
print(missing_count)
" 2>/dev/null || echo "0")

UNORGANIZED_IMPORTS=$(find "${DIRECTORY}" -name "*.py" | wc -l)
IMPORT_ERRORS=$(poetry run ruff check "${DIRECTORY}" --select I001,F401 2>/dev/null | wc -l || echo "0")

echo -e "${YELLOW}📋 IMPORT ANALYSIS RESULTS:${NC}"
echo "  🔍 Files to chec${: $UNORGANIZED_IMPO}RTS Python files"
echo "  📦 Import errors (I001, F401${: $IMPORT_ERR}ORS"
echo "  ❓ Potential missing imports${ $MISSING_IMPOR}TS"
echo ""

if [[ "${MODE}" = "--fix" ]]; then
	echo -e "${GREEN}🔧 APPLYING COMPREHENSIVE IMPORT FIXES...${NC}"
	echo ""

	# Step 1: Add missing imports with autoimport
	echo -e "${BLUE}📦 STEP 1: Adding missing imports (autoimport)...${NC}"
	poetry run autoimport "${DIRECTORY}" || echo "⚠️ autoimport completed with warnings"

	# Step 2: Reorder imports with reorder-python-imports
	echo -e "${BLUE}🔄 STEP 2: Reordering imports (reorder-python-imports)...${NC}"
	find "${DIRECTORY}" -name "*.py" -exec poetry run reorder-python-imports {} \; || echo "⚠️ reorder-python-imports completed with warnings"

	# Step 3: Final organization with isort (your existing tool)
	echo -e "${BLUE}📋 STEP 3: Final organization (isort)...${NC}"
	poetry run isort "${DIRECTORY}" || echo "⚠️ isort completed with warnings"

	# Step 4: Remove unused imports with ruff
	echo -e "${BLUE}🧹 STEP 4: Removing unused imports (ruff)...${NC}"
	poetry run ruff check "${DIRECTORY}" --select F401 --fix || echo "⚠️ ruff completed with warnings"

	# Final assessment
	FINAL_ERRORS=$(poetry run ruff check "${DIRECTORY}" --select I001,F401 2>/dev/null | wc -l || echo "0")
	FIXED_ISSUES=$((IMPORT_ERRORS - FINAL_ERRORS))

	echo ""
	echo -e "${GREEN}🎉 IMPORT MANAGEMENT RESULTS:${NC}"
	echo -e "${BLUE}📊 BEFOR${: $IMPORT_ERR}ORS import issues${NC}"
	echo -e "${GREEN}✅ AFTER:${ $FINAL_ERRO}RS import issues${NC}"
	echo -e "${CYAN}🎯 FIXED${  $FIXED_ISS}UES import issues${NC}"
	echo ""
	echo -e "${YELLOW}🔍 IMPROVEMENTS APPLIED:${NC}"
	echo "  • Added missing imports automatically"
	echo "  • Organized imports into proper sections (stdlib, 3rd party, local)"
	echo "  • Removed unused import statements"
	echo "  • Split multi-imports into single lines"
	echo "  • Applied consistent import ordering"

elif [[ "${MODE}" = "--preview" ]]; then
	echo -e "${BLUE}🔍 PREVIEW MODE - Showing what would be fixed...${NC}"
	echo ""

	echo -e "${YELLOW}📦 Missing imports that would be added:${NC}"
	poetry run autoimport "${DIRECTORY}" 2>/dev/null | head -10 || echo "  No obvious missing imports detected"

	echo ""
	echo -e "${YELLOW}🔄 Import organization preview:${NC}"
	find "${DIRECTORY}" -name "*.py" | head -3 | while read -r file; do
		echo "  �${� $f}ile:"
		poetry run reorder-python-imports --diff "${file}" 2>/dev/null | head -5 || echo "    No changes needed"
	done

	echo ""
	echo -e "${YELLOW}🧹 Unused imports that would be removed:${NC}"
	poetry run ruff check "${DIRECTORY}" --select F401 | head -5 || echo "  No unused imports found"

	echo ""
	echo -e "${GREEN}💡 TO APPLY ALL FIXES:${NC}"
	echo "  ./dev-tools/scripts/auto-import-manager.sh ${DIRECTORY} --fix"
fi

echo ""
echo -e "${GREEN}🎉 Auto-import analysis complete!${NC}"
echo -e "${YELLOW}🔄 Rollback: git stash apply stash@{0} (if needed)${NC}"

# Provide setup recommendations
if [[ "${MODE}" = "--fix" ]]; then
	echo ""
	echo -e "${CYAN}💡 EDITOR INTEGRATION RECOMMENDATIONS:${NC}"
	echo ""
	echo -e "${BLUE}🔥 For VS Code (settings.json):${NC}"
	echo '{'
	echo '  "python.linting.enabled": true,'
	echo '  "python.linting.ruffEnabled": true,'
	echo '  "editor.formatOnSave": true,'
	echo '  "editor.codeActionsOnSave": {'
	echo '    "source.organizeImports": true'
	echo '  }'
	echo '}'
	echo ""
	echo -e "${BLUE}🔥 For Neovim (pyflyby integration):${NC}"
	echo "# Add to ~/.pyflyby for automatic imports:"
	echo "import pandas as pd"
	echo "import numpy as np"
	echo "from pathlib import Path"
	echo "from typing import List, Dict, Optional, Union"
	echo ""
	echo -e "${BLUE}📚 Learn more:${NC}"
	echo "  • autoimport: https://lyz-code.github.io/autoimport/"
	echo "  • reorder-python-imports: https://github.com/asottile/reorder-python-imports"
	echo "  • pyflyby: https://pyflyby.readthedocs.io/"
fi
