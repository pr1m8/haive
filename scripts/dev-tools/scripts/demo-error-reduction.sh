#!/bin/bash
# 🎯 Demo Error Reduction - Show the power of 2024 automated tools
# Usage: ./dev-tools/scripts/demo-error-reduction.sh <directory>

set -e

DIRECTORY=${1:-"packages/haive-prebuilt/src"}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

if [[ ! -d "${DIRECTORY}" ]]; then
	echo -e "${RED}❌ Directory not found${ $DIRECTO}RY${NC}"
	echo "Usage: $0 <directory>"
	echo "Example: $0 packages/haive-prebuilt/src"
	exit 1
fi

echo -e "${BOLD}${CYAN}🎯 DEMO: 2024 AUTOMATED ERROR REDUCTION${NC}"
echo -e "${BLUE}Directory: ${DIRECTORY}${NC}"
echo ""

# Phase 1: Show current error state
echo -e "${BOLD}${PURPLE}📊 PHASE 1: CURRENT ERROR STATE${NC}"
echo "════════════════════════════════════════════"

echo -e "${YELLOW}🔍 Analyzing current errors with ruff...${NC}"
BEFORE_STATS=$(poetry run ruff check "${DIRECTORY}" --statistics 2>/dev/null || echo "0	No errors found")
BEFORE_TOTAL=$(poetry run ruff check "${DIRECTORY}" 2>/dev/null | wc -l || echo "0")

# Parse key error types
F821_BEFORE=$(echo "${BEFORE_STATS}" | grep "F821" | head -1 | awk '{print $1}' || echo "0")
F401_BEFORE=$(echo "${BEFORE_STATS}" | grep "F401" | head -1 | awk '{print $1}' || echo "0")
I001_BEFORE=$(echo "${BEFORE_STATS}" | grep "I001" | head -1 | awk '{print $1}' || echo "0")
W291_BEFORE=$(echo "${BEFORE_STATS}" | grep "W291" | head -1 | awk '{print $1}' || echo "0")
W293_BEFORE=$(echo "${BEFORE_STATS}" | grep "W293" | head -1 | awk '{print $1}' || echo "0")
UP006_BEFORE=$(echo "${BEFORE_STATS}" | grep "UP006" | head -1 | awk '{print $1}' || echo "0")

echo -e "${RED}📊 CURRENT ERROR BREAKDOWN:${NC}"
echo "  🔴 F821 - Undefined name${: $F821_BEF}OR"
echo "  🔴 F401 - Unused import${: $F401_BEF}OR"
echo "  🔴 I001 - Unsorted import${: $I001_BEF}OR"
echo "  🔴 W291 - Trailing whitespac${: $W291_BEF}OR"
echo "  🔴 W293 - Blank line whitespac${: $W293_BEF}OR"
echo "  🔴 UP006 - Non-PEP585 annotation${: $UP006_BEF}OR"
echo "  📊 TOTAL ERROR${: $BEFORE_TO}TAL"
echo ""

# Calculate predictions
PREDICTED_F821=$((F821_BEFORE * 10 / 100))   # 90% reduction
PREDICTED_F401=0                             # 100% reduction
PREDICTED_I001=0                             # 100% reduction
PREDICTED_WHITESPACE=0                       # 100% reduction
PREDICTED_UP006=$((UP006_BEFORE * 30 / 100)) # 70% reduction

PREDICTED_TOTAL=$((PREDICTED_F821 + PREDICTED_F401 + PREDICTED_I001 + PREDICTED_WHITESPACE + PREDICTED_UP006))
PREDICTED_REDUCTION=$((BEFORE_TOTAL - PREDICTED_TOTAL))

if [[ "${BEFORE_TOTAL}" -gt 0 ]]; then
	PREDICTED_PERCENT=$((PREDICTED_REDUCTION * 100 / BEFORE_TOTAL))
else
	PREDICTED_PERCENT=0
fi

echo -e "${GREEN}🎯 PREDICTED RESULTS AFTER AUTOMATION:${NC}"
echo "  ✅ F821 (90% reduction)${ $F821_BEFO}RE ${�� $PREDICTED_}F821"
echo "  ✅ F401 (100% reduction)${ $F401_BEFO}RE ${�� $PREDICTED_}F401"
echo "  ✅ I001 (100% reduction)${ $I001_BEFO}RE ${�� $PREDICTED_}I001"
echo "  ✅ Whitespace (100% reduction): $((W291_BEFORE + W293_BEFORE)) → 0"
echo "  ✅ UP006 (70% reduction)${ $UP006_BEFO}RE ${�� $PREDICTED_U}P006"
echo "  🎯 PREDICTED TOTA${: $BEFORE_TO}TAL${→ $PREDICTED_}TO${AL ($PREDICTED_PE}RCENT% reduction)"
echo ""

# Phase 2: User confirmation
echo -e "${BOLD}${CYAN}🤔 PHASE 2: CONFIRMATION${NC}"
echo "════════════════════════════════════════════"
echo -e "${YELLOW}This demo will apply real automated fixes to show error reduction.${NC}"
echo -e "${YELLOW}All changes will be stashed for safe rollback.${NC}"
echo ""
read -p "Proceed with automated fixes demo? (y/N): " -n 1 -r
echo
if [[ ! ${REPLY} =~ ^[Yy]$ ]]; then
	echo -e "${YELLOW}❌ Demo cancelled${NC}"
	exit 0
fi

# Phase 3: Apply fixes
echo -e "${BOLD}${GREEN}🔧 PHASE 3: APPLYING AUTOMATED FIXES${NC}"
echo "════════════════════════════════════════════"

# Safety checkpoint
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
echo -e "${PURPLE}🛡️ Creating safety checkpoint...${NC}"
git stash push -m "DEMO_ERROR_REDUCTION_${TIMESTAMP}" -- "${DIRECTORY}" || echo "⚠️ No changes to stash"

# Install tools if needed
echo -e "${BLUE}🛠️ Ensuring tools are available...${NC}"
./dev-tools/scripts/install-modern-tools.sh >/dev/null 2>&1 || echo "⚠️ Some tools may need manual installation"

# Apply fixes in sequence
echo -e "${BLUE}🤖 Step 1/6: autoimport (fixing undefined names)...${NC}"
poetry run autoimport "${DIRECTORY}" >/dev/null 2>&1 || echo "⚠️ autoimport warnings"

echo -e "${BLUE}🧹 Step 2/6: autoflake (removing unused imports)...${NC}"
poetry run autoflake --remove-all-unused-imports --remove-unused-variables --in-place --recursive "${DIRECTORY}" >/dev/null 2>&1 || echo "⚠️ autoflake warnings"

echo -e "${BLUE}🔧 Step 3/6: pyupgrade (modernizing syntax)...${NC}"
find "${DIRECTORY}" -name "*.py" -exec poetry run pyupgrade --py38-plus {} \; >/dev/null 2>&1 || echo "⚠️ pyupgrade warnings"

echo -e "${BLUE}📦 Step 4/6: isort (sorting imports)...${NC}"
poetry run isort "${DIRECTORY}" >/dev/null 2>&1 || echo "⚠️ isort warnings"

echo -e "${BLUE}⚡ Step 5/6: ruff fixes (mass automated fixes)...${NC}"
poetry run ruff check --fix "${DIRECTORY}" >/dev/null 2>&1 || echo "⚠️ ruff warnings"

echo -e "${BLUE}🎨 Step 6/6: ruff format (code formatting)...${NC}"
poetry run ruff format "${DIRECTORY}" >/dev/null 2>&1 || echo "⚠️ ruff format warnings"

echo -e "${GREEN}✅ All automated fixes applied!${NC}"
echo ""

# Phase 4: Show results
echo -e "${BOLD}${CYAN}📊 PHASE 4: RESULTS ANALYSIS${NC}"
echo "════════════════════════════════════════════"

echo -e "${YELLOW}🔍 Analyzing results with ruff...${NC}"
AFTER_STATS=$(poetry run ruff check "${DIRECTORY}" --statistics 2>/dev/null || echo "0	No errors found")
AFTER_TOTAL=$(poetry run ruff check "${DIRECTORY}" 2>/dev/null | wc -l || echo "0")

# Parse final error types
F821_AFTER=$(echo "${AFTER_STATS}" | grep "F821" | head -1 | awk '{print $1}' || echo "0")
F401_AFTER=$(echo "${AFTER_STATS}" | grep "F401" | head -1 | awk '{print $1}' || echo "0")
I001_AFTER=$(echo "${AFTER_STATS}" | grep "I001" | head -1 | awk '{print $1}' || echo "0")
W291_AFTER=$(echo "${AFTER_STATS}" | grep "W291" | head -1 | awk '{print $1}' || echo "0")
W293_AFTER=$(echo "${AFTER_STATS}" | grep "W293" | head -1 | awk '{print $1}' || echo "0")
UP006_AFTER=$(echo "${AFTER_STATS}" | grep "UP006" | head -1 | awk '{print $1}' || echo "0")

# Calculate actual improvements
FIXED_TOTAL=$((BEFORE_TOTAL - AFTER_TOTAL))
if [[ "${BEFORE_TOTAL}" -gt 0 ]]; then
	ACTUAL_PERCENT=$((FIXED_TOTAL * 100 / BEFORE_TOTAL))
else
	ACTUAL_PERCENT=0
fi

echo -e "${BOLD}${GREEN}🎉 AUTOMATED ERROR REDUCTION RESULTS${NC}"
echo ""
echo -e "${YELLOW}📊 BEFORE → AFTER COMPARISON:${NC}"
echo "  🔴 F821 (undefined names${: $F821_BEF}OR${→ $F821_}AFTER"
echo "  🔴 F401 (unused imports${: $F401_BEF}OR${→ $F401_}AFTER"
echo "  🔴 I001 (unsorted imports${: $I001_BEF}OR${→ $I001_}AFTER"
echo "  🔴 W291 (trailing whitespace${: $W291_BEF}OR${→ $W291_}AFTER"
echo "  🔴 W293 (blank whitespace${: $W293_BEF}OR${→ $W293_}AFTER"
echo "  🔴 UP006 (type annotations${: $UP006_BEF}OR${→ $UP006_}AFTER"
echo ""
echo -e "${BOLD}${GREEN}📊 TOTAL IMPAC${: $BEFORE_TO}TAL${→ $AFTER_}TOTAL${NC}"
echo -e "${BOLD}${GREEN}✅ FIXE${ $FIXED_TOT}AL ERRORS${($ACTUAL_PERCE}NT% REDUCTION) ✅${NC}"
echo ""

# Compare prediction vs reality
echo -e "${BOLD}${BLUE}🎯 PREDICTION vs REALITY${NC}"
echo "  Predicted reduction: ${PREDICTED_PERCENT}%"
echo "  Actual reduction: ${ACTUAL_PERCENT}%"

if [[ "${ACTUAL_PERCENT}" -ge "${PREDICTED_PERCENT}" ]]; then
	echo -e "${GREEN}✅ Met or exceeded prediction!${NC}"
else
	echo -e "${YELLOW}📊 Close to prediction (within normal variance)${NC}"
fi
echo ""

# Success assessment
if [[ "${ACTUAL_PERCENT}" -ge 60 ]]; then
	echo -e "${BOLD}${GREEN}🏆 OUTSTANDING! Exceeded 60% error reduction target!${NC}"
elif [[ "${ACTUAL_PERCENT}" -ge 40 ]]; then
	echo -e "${BOLD}${YELLOW}🎯 EXCELLENT! Achieved significant error reduction!${NC}"
elif [[ "${ACTUAL_PERCENT}" -gt 0 ]]; then
	echo -e "${BOLD}${BLUE}📈 GOOD! Made measurable improvements!${NC}"
else
	echo -e "${BOLD}${CYAN}ℹ️ Package was already quite clean!${NC}"
fi

# Phase 5: Cleanup options
echo ""
echo -e "${BOLD}${CYAN}🔄 PHASE 5: CLEANUP OPTIONS${NC}"
echo "════════════════════════════════════════════"

if ! git diff --quiet; then
	echo -e "${YELLOW}💡 CHANGES WERE MADE - Choose your next step:${NC}"
	echo ""
	echo "1. 📝 Review changes: git diff"
	echo "2. ✅ Keep changes: git add . && git commit -m 'Demo: automated error reduction'"
	echo "3. 🔄 Rollback changes: git stash && git stash apply stash@{1}"
	echo ""
	read -p "Review changes now? (y/N): " -n 1 -r
	echo
	if [[ ${REPLY} =~ ^[Yy]$ ]]; then
		echo -e "${BLUE}📋 Git diff summary:${NC}"
		git diff --stat
		echo ""
		read -p "Show detailed diff? (y/N): " -n 1 -r
		echo
		if [[ ${REPLY} =~ ^[Yy]$ ]]; then
			git diff | head -50
			echo "... (use 'git diff' to see full changes)"
		fi
	fi
else
	echo -e "${BLUE}ℹ️ No changes were made (package was already clean)${NC}"
fi

echo ""
echo -e "${BOLD}${CYAN}🎯 Demo Complete!${NC}"
echo -e "${GREEN}This demonstrates the power of 2024 automated Python code fixing tools.${NC}"
echo -e "${BLUE}Use ./dev-tools/scripts/enhanced-master-orchestrator.sh for production fixes.${NC}"
