#!/bin/bash
# 🔥 Fixit Modernizer - Meta's Advanced Auto-Fixing Linter
# Usage: ./dev-tools/scripts/fixit-modernizer.sh <directory> [--fix]

set -e

DIRECTORY=${1:-"src/"}
FIX_MODE=${2:-""}

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

echo -e "${CYAN}🔥 FIXIT MODERNIZE${: $DIRECT}ORY${NC}"
echo -e "${BLUE}Meta's advanced auto-fixing linter powered by LibCST${NC}"

# Safety checkpoint
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
git stash push -m "FIXIT_CHECKPOINT_${TIMESTAMP}" -- "${DIRECTORY}" || echo "⚠️ No changes to stash"

# Check if fixit is available
if ! poetry show fixit >/dev/null 2>&1; then
	echo -e "${YELLOW}📦 Installing fixit...${NC}"
	poetry add --group dev "fixit>=2.1.0"
fi

# Get baseline issues
echo -e "${BLUE}📊 Analyzing codebase with Fixit...${NC}"
BASELINE_ISSUES=$(poetry run fixit lint "${DIRECTORY}" 2>/dev/null | grep -c "file.*error" || echo "0")
echo -e "${YELLOW}🚨 Found issues ${n $BASELINE_ISS}UES files${NC}"

if [[ "${FIX_MODE}" = "--fix" ]]; then
	echo -e "${GREEN}🔧 Applying auto-fixes...${NC}"

	# Apply Fixit auto-fixes
	poetry run fixit fix --automatic "${DIRECTORY}" || echo "⚠️ Some fixes may need manual review"

	# Check final status
	FINAL_ISSUES=$(poetry run fixit lint "${DIRECTORY}" 2>/dev/null | grep -c "file.*error" || echo "0")
	FIXED_ISSUES=$((BASELINE_ISSUES - FINAL_ISSUES))

	echo ""
	echo -e "${GREEN}🎉 FIXIT RESULTS:${NC}"
	echo -e "${BLUE}📊 BEFORE${: $BASELINE_ISS}UES files with issues${NC}"
	echo -e "${GREEN}✅ AFTER:${ $FINAL_ISSU}ES files with issues${NC}"
	echo -e "${CYAN}🎯 FIXED${  $FIXED_ISS}UES files automatically${NC}"
	echo ""
	echo -e "${YELLOW}🔍 Common fixes applied:${NC}"
	echo "  • F-string conversions (.format() → f-strings)"
	echo "  • Removed object inheritance (class Foo(object) → class Foo)"
	echo "  • Modern typing syntax (List[str] → list[str])"
	echo "  • Print statement modernization"
	echo "  • Import optimizations"
else
	echo -e "${BLUE}🔍 Showing preview of available fixes...${NC}"
	poetry run fixit lint --diff "${DIRECTORY}" | head -50

	echo ""
	echo -e "${GREEN}💡 TO APPLY FIXES:${NC}"
	echo "  ./dev-tools/scripts/fixit-modernizer.sh ${DIRECTORY} --fix"
fi

echo ""
echo -e "${GREEN}🎉 Fixit analysis complete!${NC}"
echo -e "${YELLOW}🔄 Rollback: git stash apply stash@{0} (if needed)${NC}"

# Show some example custom rules you could write
if [[ "${FIX_MODE}" = "--fix" ]]; then
	echo ""
	echo -e "${CYAN}💡 CUSTOM RULES YOU COULD ADD:${NC}"
	echo "  • Replace print() with haive logger"
	echo "  • Enforce haive naming conventions"
	echo "  • Remove deprecated haive imports"
	echo "  • Modernize haive API usage"
	echo ""
	echo -e "${BLUE}📚 Learn more: https://fixit.readthedocs.io/en/stable/${NC}"
fi
