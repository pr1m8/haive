#!/bin/bash
# 🚀 Enhanced Master Orchestrator - 2024 Automated Code Fixing
# Usage: ./dev-tools/scripts/enhanced-master-orchestrator.sh <directory> [--auto|--interactive|--preview]
#
# 🎯 ENHANCED APPROACH with 2024 automation tools:
# Step 0: 📊 Comprehensive Error Analysis with Ruff Statistics
# Step 1: 🤖 Missing Imports (autoimport) - Fixes F821 undefined names
# Step 2: 🧹 Remove Unused Code (autoflake) - Fixes F401 unused imports
# Step 3: 🔧 Modernize Syntax (pyupgrade) - Fixes datetime, f-strings, type hints
# Step 4: 📦 Import Organization (isort) - Fixes I001 import sorting
# Step 5: ⚡ Ruff Auto-fixes - Fixes ~1000+ error types automatically
# Step 6: 🎨 Code Formatting (ruff format) - Fixes whitespace, formatting
#
# Expected reduction: 60-80% of all errors automatically fixed!

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
BOLD='\033[1m'
NC='\033[0m'

if [[ ! -d "${DIRECTORY}" ]]; then
	echo -e "${RED}❌ Directory not found${ $DIRECTO}RY${NC}"
	exit 1
fi

echo -e "${BOLD}${CYAN}🚀 ENHANCED MASTER ORCHESTRATOR - 2024 EDITION${NC}"
echo -e "${BLUE}📂 Director${: $DIRECT}ORY${NC}"
echo -e "${BLUE}🔧 Mod${: $M}ODE${NC}"
echo -e "${BLUE}🎯 Goal: 60-80% automated error reduction${NC}"
echo ""

# Enhanced safety checkpoint (ONLY for target directory)
MASTER_TIMESTAMP=$(date +%Y%m%d_%H%M%S)
echo -e "${PURPLE}🛡️ Creating MASTER safety checkpoint${for $DIRE}CTORY...${NC}"
git stash push -m "ENHANCED_MASTER_${MASTER_TIMESTAMP}" -- "${DIRECTORY}" || echo "⚠️ Package stash failed - no changes to stash"

# ===================================================================
# 📊 STEP 0: COMPREHENSIVE ERROR ANALYSIS WITH RUFF
# ===================================================================

echo -e "${BOLD}${PURPLE}📊 STEP 0: COMPREHENSIVE ERROR ANALYSIS${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"

# Get comprehensive ruff statistics
echo -e "${YELLOW}🔍 Running comprehensive ruff analysis...${NC}"
RUFF_STATS=$(poetry run ruff check "${DIRECTORY}" --statistics 2>/dev/null || echo "0	No errors found")

# Parse key error types
F821_ERRORS=$(echo "${RUFF_STATS}" | grep "F821" | head -1 | awk '{print $1}' || echo "0")
F401_ERRORS=$(echo "${RUFF_STATS}" | grep "F401" | head -1 | awk '{print $1}' || echo "0")
I001_ERRORS=$(echo "${RUFF_STATS}" | grep "I001" | head -1 | awk '{print $1}' || echo "0")
W291_ERRORS=$(echo "${RUFF_STATS}" | grep "W291" | head -1 | awk '{print $1}' || echo "0")
W293_ERRORS=$(echo "${RUFF_STATS}" | grep "W293" | head -1 | awk '{print $1}' || echo "0")
UP006_ERRORS=$(echo "${RUFF_STATS}" | grep "UP006" | head -1 | awk '{print $1}' || echo "0")
DTZ005_ERRORS=$(echo "${RUFF_STATS}" | grep "DTZ005" | head -1 | awk '{print $1}' || echo "0")
G004_ERRORS=$(echo "${RUFF_STATS}" | grep "G004" | head -1 | awk '{print $1}' || echo "0")

# Count total errors
TOTAL_ERRORS=$(poetry run ruff check "${DIRECTORY}" 2>/dev/null | wc -l || echo "0")

echo -e "${YELLOW}📊 DETAILED ERROR BREAKDOWN:${NC}"
echo "  🔴 F821 - Undefined names (missing imports${: $F821_ERR}ORS"
echo "  🔴 F401 - Unused import${: $F401_ERR}ORS"
echo "  🔴 I001 - Unsorted import${: $I001_ERR}ORS"
echo "  🔴 W291 - Trailing whitespac${: $W291_ERR}ORS"
echo "  🔴 W293 - Blank line whitespac${: $W293_ERR}ORS"
echo "  🔴 UP006 - Non-PEP585 annotation${: $UP006_ERR}ORS"
echo "  🔴 DTZ005 - Datetime without timezon${: $DTZ005_ERR}ORS"
echo "  🔴 G004 - Logging f-string${: $G004_ERR}ORS"
echo "  📊 Total errors detecte${: $TOTAL_ERR}ORS"
echo ""

# Calculate auto-fixable estimates
AUTO_FIXABLE_F821=$((F821_ERRORS * 90 / 100))          # 90% fixable with autoimport
AUTO_FIXABLE_F401=${F401_ERRORS}                         # 100% fixable with autoflake
AUTO_FIXABLE_I001=${I001_ERRORS}                         # 100% fixable with isort
AUTO_FIXABLE_WHITESPACE=$((W291_ERRORS + W293_ERRORS)) # 100% fixable with ruff format
AUTO_FIXABLE_UP006=${UP006_ERRORS}                       # 100% fixable with pyupgrade
AUTO_FIXABLE_DTZ005=$((DTZ005_ERRORS * 70 / 100))      # 70% fixable with pyupgrade

ESTIMATED_AUTO_FIXABLE=$((AUTO_FIXABLE_F821 + AUTO_FIXABLE_F401 + AUTO_FIXABLE_I001 + AUTO_FIXABLE_WHITESPACE + AUTO_FIXABLE_UP006 + AUTO_FIXABLE_DTZ005))

echo -e "${GREEN}🤖 AUTO-FIXABLE ESTIMATES:${NC}"
echo "  ✅ F821 (90% with autoimport)${ $AUTO_FIXABLE_F8}21"
echo "  ✅ F401 (100% with autoflake)${ $AUTO_FIXABLE_F4}01"
echo "  ✅ I001 (100% with isort)${ $AUTO_FIXABLE_I0}01"
echo "  ✅ Whitespace (100% with ruff)${ $AUTO_FIXABLE_WHITESPA}CE"
echo "  ✅ UP006 (100% with pyupgrade)${ $AUTO_FIXABLE_UP0}06"
echo "  ✅ DTZ005 (70% with pyupgrade)${ $AUTO_FIXABLE_DTZ0}05"
echo "  🎯 Estimated total auto-fixabl${: $ESTIMATED_AUTO_FIXA}BLE"

if [[ "${TOTAL_ERRORS}" -gt 0 ]]; then
	REDUCTION_PERCENT=$((ESTIMATED_AUTO_FIXABLE * 100 / TOTAL_ERRORS))
	echo "  📈 Expected reduction: ${REDUCTION_PERCENT}%"
fi

echo ""

# Manual attention needed
MANUAL_F821=$((F821_ERRORS - AUTO_FIXABLE_F821))
MANUAL_G004=${G004_ERRORS} # No autofix available yet

echo -e "${YELLOW}⚠️  MANUAL ATTENTION NEEDED:${NC}"
echo "  🔴 F821 complex import${: $MANUAL_F}821"
echo "  🔴 G004 logging f-string${: $MANUAL_G}004 (no autofix available)"
echo ""

# User approval for interactive mode
if [[ "${MODE}" = "--interactive" ]]; then
	echo -e "${CYAN}🤔 Proceed with automated fixes?${NC}"
	echo "  Expected to fix ${ESTIMATED_AUTO_FIXABLE} out of ${TOTAL_ERRORS} errors (${REDUCTION_PERCENT}%)"
	echo ""
	read -p "Continue? (y/N): " -n 1 -r
	echo
	if [[ ! ${REPLY} =~ ^[Yy]$ ]]; then
		echo -e "${YELLOW}❌ User cancelled${NC}"
		exit 0
	fi
fi

# ===================================================================
# 🤖 STEP 1: MISSING IMPORTS (autoimport) - Fixes F821
# ===================================================================

if [[ "${MODE}" != "--preview" ]]; then
	echo -e "${BOLD}${GREEN}🤖 STEP 1: FIXING MISSING IMPORTS${NC}"
	echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
	echo -e "${YELLOW}🎯 Target: F${x $F821_ERR}ORS undefined names (F821)${NC}"
	echo ""

	# Install autoimport if needed
	if ! poetry show autoimport >/dev/null 2>&1; then
		echo -e "${BLUE}📥 Installing autoimport...${NC}"
		poetry add --group dev autoimport
	fi

	echo -e "${BLUE}🔧 Running autoimport ${n $DIRECT}ORY...${NC}"
	poetry run autoimport "${DIRECTORY}" || echo -e "${YELLOW}⚠️ autoimport completed with warnings${NC}"

	# Check results
	NEW_F821=$(poetry run ruff check "${DIRECTORY}" --select F821 2>/dev/null | wc -l || echo "0")
	FIXED_F821=$((F821_ERRORS - NEW_F821))

	echo -e "${GREEN}✅ STEP 1 RESULTS:${NC}"
	echo "  🔴 F821 error${: $F821_ERR}ORS${→ $NEW}_F821 (fi${ed: $FIXED}_F821)"
	echo ""

	# Interactive checkpoint
	if [[ "${MODE}" = "--interactive" ]]; then
		echo -e "${CYAN}Review changes before continuing?${NC}"
		read -p "Show git diff? (y/N): " -n 1 -r
		echo
		if [[ ${REPLY} =~ ^[Yy]$ ]]; then
			git diff --stat
			echo ""
			read -p "Continue to next step? (y/N): " -n 1 -r
			echo
			if [[ ! ${REPLY} =~ ^[Yy]$ ]]; then
				echo -e "${YELLOW}❌ User cancelled${NC}"
				exit 0
			fi
		fi
	fi
fi

# ===================================================================
# 🧹 STEP 2: REMOVE UNUSED CODE (autoflake) - Fixes F401
# ===================================================================

if [[ "${MODE}" != "--preview" ]]; then
	echo -e "${BOLD}${BLUE}🧹 STEP 2: REMOVING UNUSED CODE${NC}"
	echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
	echo -e "${YELLOW}🎯 Target: F${x $F401_ERR}ORS unused imports (F401)${NC}"
	echo ""

	# Install autoflake if needed
	if ! poetry show autoflake >/dev/null 2>&1; then
		echo -e "${BLUE}📥 Installing autoflake...${NC}"
		poetry add --group dev autoflake
	fi

	echo -e "${BLUE}🔧 Running autoflake ${n $DIRECT}ORY...${NC}"
	poetry run autoflake --remove-all-unused-imports --remove-unused-variables --in-place --recursive "${DIRECTORY}" || echo -e "${YELLOW}⚠️ autoflake completed with warnings${NC}"

	# Check results
	NEW_F401=$(poetry run ruff check "${DIRECTORY}" --select F401 2>/dev/null | wc -l || echo "0")
	FIXED_F401=$((F401_ERRORS - NEW_F401))

	echo -e "${GREEN}✅ STEP 2 RESULTS:${NC}"
	echo "  🔴 F401 error${: $F401_ERR}ORS${→ $NEW}_F401 (fi${ed: $FIXED}_F401)"
	echo ""
fi

# ===================================================================
# 🔧 STEP 3: MODERNIZE SYNTAX (pyupgrade) - Fixes datetime, type hints
# ===================================================================

if [[ "${MODE}" != "--preview" ]]; then
	echo -e "${BOLD}${PURPLE}🔧 STEP 3: MODERNIZING SYNTAX${NC}"
	echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
	echo -e "${YELLOW}🎯 Target: F${x $UP006_ERR}ORS${+ $DTZ005_ERR}ORS syntax modernization issues${NC}"
	echo ""

	# Install pyupgrade if needed
	if ! poetry show pyupgrade >/dev/null 2>&1; then
		echo -e "${BLUE}📥 Installing pyupgrade...${NC}"
		poetry add --group dev pyupgrade
	fi

	echo -e "${BLUE}🔧 Running pyupgrade ${n $DIRECT}ORY...${NC}"
	find "${DIRECTORY}" -name "*.py" -exec poetry run pyupgrade --py38-plus {} \; || echo -e "${YELLOW}⚠️ pyupgrade completed with warnings${NC}"

	# Check results
	NEW_UP006=$(poetry run ruff check "${DIRECTORY}" --select UP006 2>/dev/null | wc -l || echo "0")
	NEW_DTZ005=$(poetry run ruff check "${DIRECTORY}" --select DTZ005 2>/dev/null | wc -l || echo "0")
	FIXED_UP006=$((UP006_ERRORS - NEW_UP006))
	FIXED_DTZ005=$((DTZ005_ERRORS - NEW_DTZ005))

	echo -e "${GREEN}✅ STEP 3 RESULTS:${NC}"
	echo "  🔴 UP006 error${: $UP006_ERR}ORS${→ $NEW_}UP006 (fi${ed: $FIXED_}UP006)"
	echo "  🔴 DTZ005 error${: $DTZ005_ERR}ORS${→ $NEW_D}TZ005 (fi${ed: $FIXED_D}TZ005)"
	echo ""
fi

# ===================================================================
# 📦 STEP 4: IMPORT ORGANIZATION (isort) - Fixes I001
# ===================================================================

if [[ "${MODE}" != "--preview" ]]; then
	echo -e "${BOLD}${GREEN}📦 STEP 4: ORGANIZING IMPORTS${NC}"
	echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
	echo -e "${YELLOW}🎯 Target: F${x $I001_ERR}ORS unsorted imports (I001)${NC}"
	echo ""

	echo -e "${BLUE}🔧 Running isort ${n $DIRECT}ORY...${NC}"
	poetry run isort "${DIRECTORY}" || echo -e "${YELLOW}⚠️ isort completed with warnings${NC}"

	# Check results
	NEW_I001=$(poetry run ruff check "${DIRECTORY}" --select I001 2>/dev/null | wc -l || echo "0")
	FIXED_I001=$((I001_ERRORS - NEW_I001))

	echo -e "${GREEN}✅ STEP 4 RESULTS:${NC}"
	echo "  🔴 I001 error${: $I001_ERR}ORS${→ $NEW}_I001 (fi${ed: $FIXED}_I001)"
	echo ""
fi

# ===================================================================
# ⚡ STEP 5: RUFF AUTO-FIXES - Mass automated fixes
# ===================================================================

if [[ "${MODE}" != "--preview" ]]; then
	echo -e "${BOLD}${CYAN}⚡ STEP 5: RUFF MASS AUTO-FIXES${NC}"
	echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
	echo -e "${YELLOW}🎯 Target: Fix hundreds of error types automatically${NC}"
	echo ""

	echo -e "${BLUE}🔧 Running ruff auto-fixes ${n $DIRECT}ORY...${NC}"
	poetry run ruff check --fix "${DIRECTORY}" || echo -e "${YELLOW}⚠️ ruff check completed with warnings${NC}"

	echo -e "${GREEN}✅ STEP 5 COMPLETE: Ruff auto-fixes applied${NC}"
	echo ""
fi

# ===================================================================
# 🎨 STEP 6: CODE FORMATTING (ruff format) - Final cleanup
# ===================================================================

if [[ "${MODE}" != "--preview" ]]; then
	echo -e "${BOLD}${YELLOW}🎨 STEP 6: FINAL CODE FORMATTING${NC}"
	echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
	echo -e "${YELLOW}🎯 Target: F${x $W291_ERR}ORS${+ $W293_ERR}ORS whitespace issues${NC}"
	echo ""

	echo -e "${BLUE}🔧 Running ruff format ${n $DIRECT}ORY...${NC}"
	poetry run ruff format "${DIRECTORY}" || echo -e "${YELLOW}⚠️ ruff format completed with warnings${NC}"

	echo -e "${GREEN}✅ STEP 6 COMPLETE: Code formatting applied${NC}"
	echo ""
fi

# ===================================================================
# 📊 FINAL COMPREHENSIVE ASSESSMENT
# ===================================================================

echo -e "${BOLD}${CYAN}📊 FINAL COMPREHENSIVE ASSESSMENT${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"

if [[ "${MODE}" != "--preview" ]]; then
	# Get final statistics
	echo -e "${YELLOW}🔍 Running final ruff analysis...${NC}"
	FINAL_STATS=$(poetry run ruff check "${DIRECTORY}" --statistics 2>/dev/null || echo "0	No errors found")
	FINAL_TOTAL=$(poetry run ruff check "${DIRECTORY}" 2>/dev/null | wc -l || echo "0")

	# Parse final error counts
	FINAL_F821=$(echo "${FINAL_STATS}" | grep "F821" | head -1 | awk '{print $1}' || echo "0")
	FINAL_F401=$(echo "${FINAL_STATS}" | grep "F401" | head -1 | awk '{print $1}' || echo "0")
	FINAL_I001=$(echo "${FINAL_STATS}" | grep "I001" | head -1 | awk '{print $1}' || echo "0")
	FINAL_W291=$(echo "${FINAL_STATS}" | grep "W291" | head -1 | awk '{print $1}' || echo "0")
	FINAL_W293=$(echo "${FINAL_STATS}" | grep "W293" | head -1 | awk '{print $1}' || echo "0")

	# Calculate improvements
	TOTAL_FIXED=$((TOTAL_ERRORS - FINAL_TOTAL))
	if [[ "${TOTAL_ERRORS}" -gt 0 ]]; then
		ACTUAL_REDUCTION=$((TOTAL_FIXED * 100 / TOTAL_ERRORS))
	else
		ACTUAL_REDUCTION=0
	fi

	echo -e "${GREEN}🎉 ENHANCED MASTER ORCHESTRATOR RESULTS:${NC}"
	echo ""
	echo -e "${YELLOW}📊 BEFORE → AFTER COMPARISON:${NC}"
	echo "  🔴 F821 (undefined names${: $F821_ERR}ORS${→ $FINAL}_F821"
	echo "  🔴 F401 (unused imports${: $F401_ERR}ORS${→ $FINAL}_F401"
	echo "  🔴 I001 (unsorted imports${: $I001_ERR}ORS${→ $FINAL}_I001"
	echo "  🔴 W291 (trailing whitespace${: $W291_ERR}ORS${→ $FINAL}_W291"
	echo "  🔴 W293 (blank whitespace${: $W293_ERR}ORS${→ $FINAL}_W293"
	echo "  📊 TOTAL ERROR${: $TOTAL_ERR}ORS${→ $FINAL_}TOTAL"
	echo ""
	echo -e "${BOLD}${GREEN}✅ FIXE${ $TOTAL_FIX}ED ERRORS${($ACTUAL_REDUCTI}ON%) ✅${NC}"
	echo ""

	# Success metrics
	if [[ "${ACTUAL_REDUCTION}" -ge 60 ]]; then
		echo -e "${BOLD}${GREEN}🎯 EXCELLENT! Exceeded 60% error reduction target! 🎉${NC}"
	elif [[ "${ACTUAL_REDUCTION}" -ge 40 ]]; then
		echo -e "${BOLD}${YELLOW}🎯 GOOD! Achieved significant error reduction! 👍${NC}"
	elif [[ "${ACTUAL_REDUCTION}" -ge 20 ]]; then
		echo -e "${BOLD}${BLUE}🎯 PROGRESS! Made solid improvements! 📈${NC}"
	else
		echo -e "${BOLD}${YELLOW}🎯 Some improvements made - may need manual review${NC}"
	fi

	# Show remaining high-impact errors
	if [[ "${FINAL_TOTAL}" -gt 0 ]]; then
		echo ""
		echo -e "${YELLOW}⚠️  REMAINING ERRORS (may need manual attention):${NC}"
		poetry run ruff check "${DIRECTORY}" --statistics 2>/dev/null | head -10
	fi

	# Git changes summary
	if ! git diff --quiet; then
		echo ""
		echo -e "${BLUE}📋 Git Changes Summary:${NC}"
		CHANGED_FILES=$(git diff --name-only | wc -l)
		echo "  📝 Files modifie${: $CHANGED_FI}LES"
		echo "  📊 Lines changed: $(git diff --shortstat | awk '{print $4, $5, $6}')"
		echo ""

		echo -e "${YELLOW}💡 REVIEW AND COMMIT:${NC}"
		echo "  git diff --stat              # Summary of changes"
		echo "  git diff                     # See all changes"
		echo "  git add . && git commit -m 'Enhanced automated code fixes: reduced errors by ${ACTUAL_REDUCTION}%'"
		echo ""
	fi

elif [[ "${MODE}" = "--preview" ]]; then
	echo -e "${YELLOW}👀 PREVIEW MODE - COMPREHENSIVE FIX PLAN:${NC}"
	echo ""
	echo -e "${CYAN}🎯 ENHANCED AUTOMATED FIX STRATEGY:${NC}"
	echo "  1. 🤖 autoimport: Fix ~90% ${f $F821_ERR}ORS undefined names (F821)"
	echo "  2. 🧹 autoflake: Fix 100% ${f $F401_ERR}ORS unused imports (F401)"
	echo "  3. 🔧 pyupgrade: Moderni${e $UP006_ERR}ORS${+ $DTZ005_ERR}ORS syntax issues"
	echo "  4. 📦 isort: Fix 100% ${f $I001_ERR}ORS import sorting (I001)"
	echo "  5. ⚡ ruff --fix: Mass fix hundreds of additional error types"
	echo "  6. 🎨 ruff format: Fix 100% of whitespace issues"
	echo ""
	echo -e "${GREEN}Expected to fix ${ESTIMATED_AUTO_FIXABLE} out of ${TOTAL_ERRORS} errors (${REDUCTION_PERCENT}%)${NC}"
	echo ""
	echo -e "${GREEN}Run with --interactive for guided execution${NC}"
	echo -e "${GREEN}Run with --auto for fully automated execution${NC}"
fi

echo ""
echo -e "${YELLOW}💡 ROLLBACK INSTRUCTIONS:${NC}"
echo "  git stash pop                 # Apply latest stash if needed"
echo "  git reset --hard HEAD~1       # Undo last commit"
echo "  git stash apply stash@{1}     # Restore master checkpoint"
echo ""

echo -e "${BOLD}${CYAN}🚀 Enhanced Master Orchestrator Complete!${NC}"
echo -e "${BLUE}💡 2024 automated tooling for maximum error reduction${NC}"
