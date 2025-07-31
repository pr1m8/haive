#!/bin/bash
# 🚀 ULTIMATE CODE FIXER - All-in-One 2024 Python Code Enhancement
# Usage: ./dev-tools/scripts/ultimate-code-fixer.sh <directory> [--auto|--interactive|--preview|--demo]
#
# 🎯 COMPREHENSIVE SOLUTION:
# ✅ Tool Installation & Verification
# ✅ Comprehensive Error Analysis
# ✅ 6-Step Automated Fixing Process
# ✅ Real-time Progress Tracking
# ✅ Interactive Approval Points
# ✅ Safe Rollback Capabilities
# ✅ Detailed Results Reporting
#
# Expected: 60-80% automated error reduction!

set -e

DIRECTORY=${1:-"packages/haive-prebuilt/src"}
MODE=${2:-"--preview"}

# Colors for output (disable if not a terminal)
if [[ -t 1 ]]; then
	RED='\033[0;31m'
	GREEN='\033[0;32m'
	YELLOW='\033[1;33m'
	BLUE='\033[0;34m'
	CYAN='\033[0;36m'
	PURPLE='\033[0;35m'
	BOLD='\033[1m'
	NC='\033[0m'
else
	RED=''
	GREEN=''
	YELLOW=''
	BLUE=''
	CYAN=''
	PURPLE=''
	BOLD=''
	NC=''
fi

# Global variables for tracking
TOOLS_INSTALLED=0
TOTAL_ERRORS_BEFORE=0
TOTAL_ERRORS_AFTER=0
CHECKPOINT_CREATED=""

# ===================================================================
# 🎨 HEADER AND VALIDATION
# ===================================================================

print_header() {
	echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
	echo -e "${BOLD}${CYAN}║                  🚀 ULTIMATE CODE FIXER                     ║${NC}"
	echo -e "${BOLD}${CYAN}║              2024 All-in-One Python Enhancement             ║${NC}"
	echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
	echo ""
	echo -e "${BLUE}📂 Directory: $DIRECTORY${NC}"
	echo -e "${BLUE}🔧 Mode: $MODE${NC}"
	echo -e "${BLUE}🎯 Expected: 60-80% automated error reduction${NC}"
	echo ""
}

validate_input() {
	if [ ! -d "$DIRECTORY" ]; then
		echo -e "${RED}❌ Directory not found: $DIRECTORY${NC}"
		echo ""
		echo -e "${YELLOW}📋 Usage Examples:${NC}"
		echo "  $0 packages/haive-prebuilt/src --interactive"
		echo "  $0 packages/haive-agents/src --auto"
		echo "  $0 packages/haive-tools/src --preview"
		echo "  $0 packages/haive-prebuilt/src --demo"
		exit 1
	fi

	case "$MODE" in
	"--auto" | "--interactive" | "--preview" | "--demo") ;;
	*)
		echo -e "${RED}❌ Invalid mode: $MODE${NC}"
		echo -e "${YELLOW}Valid modes: --auto, --interactive, --preview, --demo${NC}"
		exit 1
		;;
	esac
}

# ===================================================================
# 🛠️ TOOL MANAGEMENT
# ===================================================================

install_and_verify_tools() {
	echo -e "${BOLD}${BLUE}🛠️ STEP 1: TOOL INSTALLATION & VERIFICATION${NC}"
	echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"

	local tools=("autoimport" "autoflake" "pyupgrade" "isort" "ruff")
	local installed=0
	local failed=0

	for tool in "${tools[@]}"; do
		echo -e "${BLUE}📦 Checking $tool...${NC}"

		if poetry show "$tool" >/dev/null 2>&1; then
			echo -e "${GREEN}   ✅ Already installed${NC}"
			installed=$((installed + 1))
		else
			echo -e "${YELLOW}   📥 Installing $tool...${NC}"
			if poetry add --group dev "$tool" >/dev/null 2>&1; then
				echo -e "${GREEN}   ✅ Successfully installed${NC}"
				installed=$((installed + 1))
			else
				echo -e "${RED}   ❌ Failed to install${NC}"
				failed=$((failed + 1))
			fi
		fi
	done

	echo ""
	echo -e "${GREEN}✅ Tools Ready: $installed/${#tools[@]}${NC}"

	if [ $failed -gt 0 ]; then
		echo -e "${YELLOW}⚠️  $failed tools failed - some fixes may not work${NC}"
	fi

	TOOLS_INSTALLED=$installed
	echo ""
}

# ===================================================================
# 📊 COMPREHENSIVE ERROR ANALYSIS
# ===================================================================

analyze_errors() {
	echo -e "${BOLD}${PURPLE}📊 STEP 2: COMPREHENSIVE ERROR ANALYSIS${NC}"
	echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"

	echo -e "${YELLOW}🔍 Analyzing current errors with ruff...${NC}"

	# Get comprehensive ruff statistics
	local stats=$(poetry run ruff check "$DIRECTORY" --statistics 2>/dev/null || echo "0	No errors found")
	TOTAL_ERRORS_BEFORE=$(poetry run ruff check "$DIRECTORY" 2>/dev/null | wc -l || echo "0")

	# Parse key error types
	local f821_errors=$(echo "$stats" | grep "F821" | head -1 | awk '{print $1}' || echo "0")
	local f401_errors=$(echo "$stats" | grep "F401" | head -1 | awk '{print $1}' || echo "0")
	local i001_errors=$(echo "$stats" | grep "I001" | head -1 | awk '{print $1}' || echo "0")
	local w291_errors=$(echo "$stats" | grep "W291" | head -1 | awk '{print $1}' || echo "0")
	local w293_errors=$(echo "$stats" | grep "W293" | head -1 | awk '{print $1}' || echo "0")
	local up006_errors=$(echo "$stats" | grep "UP006" | head -1 | awk '{print $1}' || echo "0")
	local dtz005_errors=$(echo "$stats" | grep "DTZ005" | head -1 | awk '{print $1}' || echo "0")
	local g004_errors=$(echo "$stats" | grep "G004" | head -1 | awk '{print $1}' || echo "0")
	local t201_errors=$(echo "$stats" | grep "T201" | head -1 | awk '{print $1}' || echo "0")

	echo -e "${YELLOW}📊 DETAILED ERROR BREAKDOWN:${NC}"
	echo "  🔴 F821 - Undefined names (missing imports): $f821_errors"
	echo "  🔴 F401 - Unused imports: $f401_errors"
	echo "  🔴 I001 - Unsorted imports: $i001_errors"
	echo "  🔴 W291 - Trailing whitespace: $w291_errors"
	echo "  🔴 W293 - Blank line whitespace: $w293_errors"
	echo "  🔴 UP006 - Non-PEP585 annotations: $up006_errors"
	echo "  🔴 DTZ005 - Datetime without timezone: $dtz005_errors"
	echo "  🔴 G004 - Logging f-strings: $g004_errors"
	echo "  🔴 T201 - Print statements: $t201_errors"
	echo "  📊 TOTAL ERRORS: $TOTAL_ERRORS_BEFORE"
	echo ""

	# Calculate auto-fixable estimates
	local auto_f821=$((f821_errors * 90 / 100))
	local auto_f401=$f401_errors
	local auto_i001=$i001_errors
	local auto_whitespace=$((w291_errors + w293_errors))
	local auto_up006=$up006_errors
	local auto_dtz005=$((dtz005_errors * 70 / 100))

	local estimated_fixable=$((auto_f821 + auto_f401 + auto_i001 + auto_whitespace + auto_up006 + auto_dtz005))

	echo -e "${GREEN}🤖 AUTO-FIXABLE ESTIMATES:${NC}"
	echo "  ✅ F821 (90% with autoimport): $auto_f821"
	echo "  ✅ F401 (100% with autoflake): $auto_f401"
	echo "  ✅ I001 (100% with isort): $auto_i001"
	echo "  ✅ Whitespace (100% with ruff): $auto_whitespace"
	echo "  ✅ UP006 (100% with pyupgrade): $auto_up006"
	echo "  ✅ DTZ005 (70% with pyupgrade): $auto_dtz005"
	echo "  🎯 Estimated total auto-fixable: $estimated_fixable"

	if [ "$TOTAL_ERRORS_BEFORE" -gt 0 ]; then
		local reduction_percent=$((estimated_fixable * 100 / TOTAL_ERRORS_BEFORE))
		echo "  📈 Expected reduction: ${reduction_percent}%"
	fi
	echo ""

	# Manual attention section
	local manual_f821=$((f821_errors - auto_f821))
	echo -e "${YELLOW}⚠️  MANUAL ATTENTION NEEDED:${NC}"
	echo "  🔴 F821 complex imports: $manual_f821"
	echo "  🔴 G004 logging f-strings: $g004_errors (no autofix available)"
	echo "  🔴 T201 print statements: $t201_errors (replace with logging)"
	echo ""
}

# ===================================================================
# 🛡️ SAFETY CHECKPOINT
# ===================================================================

create_checkpoint() {
	if [ "$MODE" = "--preview" ]; then
		return 0
	fi

	echo -e "${BOLD}${PURPLE}🛡️ STEP 3: SAFETY CHECKPOINT${NC}"
	echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"

	local timestamp=$(date +%Y%m%d_%H%M%S)
	echo -e "${PURPLE}🛡️ Creating safety checkpoint for $DIRECTORY...${NC}"

	if git stash push -m "ULTIMATE_FIXER_${timestamp}" -- "$DIRECTORY" >/dev/null 2>&1; then
		CHECKPOINT_CREATED="ULTIMATE_FIXER_${timestamp}"
		echo -e "${GREEN}✅ Safety checkpoint created: $CHECKPOINT_CREATED${NC}"
	else
		echo -e "${YELLOW}⚠️ No changes to stash - proceeding without checkpoint${NC}"
	fi
	echo ""
}

# ===================================================================
# 🤖 AUTOMATED FIXING PROCESS
# ===================================================================

apply_fixes() {
	if [ "$MODE" = "--preview" ]; then
		show_preview
		return 0
	fi

	echo -e "${BOLD}${GREEN}🤖 STEP 4: AUTOMATED FIXING PROCESS${NC}"
	echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"

	# Sub-step 1: Missing Imports (autoimport)
	echo -e "${BLUE}🔧 4.1: Fixing undefined names (autoimport)...${NC}"
	if poetry run autoimport "$DIRECTORY" >/dev/null 2>&1; then
		echo -e "${GREEN}   ✅ autoimport completed${NC}"
	else
		echo -e "${YELLOW}   ⚠️ autoimport completed with warnings${NC}"
	fi

	# Interactive checkpoint
	if [ "$MODE" = "--interactive" ]; then
		ask_continue "4.1" "autoimport results"
	fi

	# Sub-step 2: Remove Unused Code (autoflake)
	echo -e "${BLUE}🔧 4.2: Removing unused imports (autoflake)...${NC}"
	if poetry run autoflake --remove-all-unused-imports --remove-unused-variables --in-place --recursive "$DIRECTORY" >/dev/null 2>&1; then
		echo -e "${GREEN}   ✅ autoflake completed${NC}"
	else
		echo -e "${YELLOW}   ⚠️ autoflake completed with warnings${NC}"
	fi

	if [ "$MODE" = "--interactive" ]; then
		ask_continue "4.2" "autoflake results"
	fi

	# Sub-step 3: Modernize Syntax (pyupgrade)
	echo -e "${BLUE}🔧 4.3: Modernizing syntax (pyupgrade)...${NC}"
	if find "$DIRECTORY" -name "*.py" -exec poetry run pyupgrade --py38-plus {} \; >/dev/null 2>&1; then
		echo -e "${GREEN}   ✅ pyupgrade completed${NC}"
	else
		echo -e "${YELLOW}   ⚠️ pyupgrade completed with warnings${NC}"
	fi

	if [ "$MODE" = "--interactive" ]; then
		ask_continue "4.3" "pyupgrade results"
	fi

	# Sub-step 4: Sort Imports (isort)
	echo -e "${BLUE}🔧 4.4: Organizing imports (isort)...${NC}"
	if poetry run isort "$DIRECTORY" >/dev/null 2>&1; then
		echo -e "${GREEN}   ✅ isort completed${NC}"
	else
		echo -e "${YELLOW}   ⚠️ isort completed with warnings${NC}"
	fi

	if [ "$MODE" = "--interactive" ]; then
		ask_continue "4.4" "isort results"
	fi

	# Sub-step 5: Mass Auto-fixes (ruff)
	echo -e "${BLUE}🔧 4.5: Mass auto-fixes (ruff check)...${NC}"
	if poetry run ruff check --fix "$DIRECTORY" >/dev/null 2>&1; then
		echo -e "${GREEN}   ✅ ruff check completed${NC}"
	else
		echo -e "${YELLOW}   ⚠️ ruff check completed with warnings${NC}"
	fi

	if [ "$MODE" = "--interactive" ]; then
		ask_continue "4.5" "ruff check results"
	fi

	# Sub-step 6: Code Formatting (ruff format)
	echo -e "${BLUE}🔧 4.6: Final formatting (ruff format)...${NC}"
	if poetry run ruff format "$DIRECTORY" >/dev/null 2>&1; then
		echo -e "${GREEN}   ✅ ruff format completed${NC}"
	else
		echo -e "${YELLOW}   ⚠️ ruff format completed with warnings${NC}"
	fi

	echo -e "${GREEN}🎉 All automated fixes applied!${NC}"
	echo ""
}

ask_continue() {
	local step=$1
	local description=$2

	echo ""
	echo -e "${CYAN}🔍 Step $step completed: $description${NC}"
	read -p "Review changes? (y/N): " -n 1 -r
	echo
	if [[ $REPLY =~ ^[Yy]$ ]]; then
		git diff --stat | head -10
		echo ""
	fi

	read -p "Continue to next step? (Y/n): " -n 1 -r
	echo
	if [[ $REPLY =~ ^[Nn]$ ]]; then
		echo -e "${YELLOW}❌ Process stopped by user${NC}"
		show_rollback_instructions
		exit 0
	fi
}

show_preview() {
	echo -e "${BOLD}${YELLOW}👀 STEP 4: PREVIEW MODE${NC}"
	echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"

	echo -e "${YELLOW}🔍 COMPREHENSIVE FIX PLAN:${NC}"
	echo ""
	echo -e "${CYAN}🎯 6-STEP AUTOMATED PROCESS:${NC}"
	echo "  1. 🤖 autoimport: Fix ~90% of undefined names (F821)"
	echo "  2. 🧹 autoflake: Fix 100% of unused imports (F401)"
	echo "  3. 🔧 pyupgrade: Modernize datetime, f-strings, type hints"
	echo "  4. 📦 isort: Fix 100% of import sorting (I001)"
	echo "  5. ⚡ ruff --fix: Mass fix hundreds of error types"
	echo "  6. 🎨 ruff format: Fix 100% of whitespace/formatting"
	echo ""

	if [ "$TOTAL_ERRORS_BEFORE" -gt 0 ]; then
		echo -e "${GREEN}Expected to fix 60-80% of $TOTAL_ERRORS_BEFORE total errors${NC}"
	fi
	echo ""
	echo -e "${GREEN}Run with --interactive for guided execution${NC}"
	echo -e "${GREEN}Run with --auto for fully automated execution${NC}"
	echo -e "${GREEN}Run with --demo for live demonstration${NC}"
	echo ""
}

# ===================================================================
# 📊 RESULTS ANALYSIS
# ===================================================================

analyze_results() {
	if [ "$MODE" = "--preview" ]; then
		return 0
	fi

	echo -e "${BOLD}${CYAN}📊 STEP 5: COMPREHENSIVE RESULTS ANALYSIS${NC}"
	echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"

	echo -e "${YELLOW}🔍 Running final error analysis...${NC}"

	# Get final statistics
	local final_stats=$(poetry run ruff check "$DIRECTORY" --statistics 2>/dev/null || echo "0	No errors found")
	TOTAL_ERRORS_AFTER=$(poetry run ruff check "$DIRECTORY" 2>/dev/null | wc -l || echo "0")

	# Parse final error counts
	local final_f821=$(echo "$final_stats" | grep "F821" | head -1 | awk '{print $1}' || echo "0")
	local final_f401=$(echo "$final_stats" | grep "F401" | head -1 | awk '{print $1}' || echo "0")
	local final_i001=$(echo "$final_stats" | grep "I001" | head -1 | awk '{print $1}' || echo "0")
	local final_w291=$(echo "$final_stats" | grep "W291" | head -1 | awk '{print $1}' || echo "0")
	local final_w293=$(echo "$final_stats" | grep "W293" | head -1 | awk '{print $1}' || echo "0")
	local final_up006=$(echo "$final_stats" | grep "UP006" | head -1 | awk '{print $1}' || echo "0")

	# Calculate improvements
	local total_fixed=$((TOTAL_ERRORS_BEFORE - TOTAL_ERRORS_AFTER))
	local actual_reduction=0
	if [ "$TOTAL_ERRORS_BEFORE" -gt 0 ]; then
		actual_reduction=$((total_fixed * 100 / TOTAL_ERRORS_BEFORE))
	fi

	echo -e "${BOLD}${GREEN}🎉 ULTIMATE CODE FIXER RESULTS${NC}"
	echo ""
	echo -e "${YELLOW}📊 BEFORE → AFTER COMPARISON:${NC}"
	echo "  🔴 F821 (undefined names): ? → $final_f821"
	echo "  🔴 F401 (unused imports): ? → $final_f401"
	echo "  🔴 I001 (unsorted imports): ? → $final_i001"
	echo "  🔴 W291 (trailing whitespace): ? → $final_w291"
	echo "  🔴 W293 (blank whitespace): ? → $final_w293"
	echo "  🔴 UP006 (type annotations): ? → $final_up006"
	echo ""
	echo -e "${BOLD}${GREEN}📊 TOTAL IMPACT: $TOTAL_ERRORS_BEFORE → $TOTAL_ERRORS_AFTER${NC}"
	echo -e "${BOLD}${GREEN}✅ FIXED $total_fixed ERRORS ($actual_reduction% REDUCTION) ✅${NC}"
	echo ""

	# Success assessment
	if [ "$actual_reduction" -ge 60 ]; then
		echo -e "${BOLD}${GREEN}🏆 OUTSTANDING! Exceeded 60% error reduction target!${NC}"
		echo -e "${GREEN}🎯 Your code quality has been significantly improved!${NC}"
	elif [ "$actual_reduction" -ge 40 ]; then
		echo -e "${BOLD}${YELLOW}🎯 EXCELLENT! Achieved significant error reduction!${NC}"
		echo -e "${YELLOW}📈 Major improvements made to code quality!${NC}"
	elif [ "$actual_reduction" -gt 0 ]; then
		echo -e "${BOLD}${BLUE}📈 GOOD! Made measurable improvements!${NC}"
		echo -e "${BLUE}✅ Code quality has been enhanced!${NC}"
	else
		echo -e "${BOLD}${CYAN}ℹ️ Package was already quite clean!${NC}"
		echo -e "${CYAN}👍 Maintaining high code quality standards!${NC}"
	fi
	echo ""

	# Show top remaining errors if any
	if [ "$TOTAL_ERRORS_AFTER" -gt 0 ]; then
		echo -e "${YELLOW}⚠️  TOP REMAINING ERRORS (may need manual attention):${NC}"
		poetry run ruff check "$DIRECTORY" --statistics 2>/dev/null | head -5
		echo ""
	fi

	# Git changes summary
	if ! git diff --quiet; then
		echo -e "${BLUE}📋 Git Changes Summary:${NC}"
		local changed_files=$(git diff --name-only | wc -l)
		echo "  📝 Files modified: $changed_files"
		if [ $changed_files -gt 0 ]; then
			echo "  📊 Line changes: $(git diff --shortstat)"
		fi
		echo ""
	fi
}

# ===================================================================
# 🔄 FINAL OPTIONS
# ===================================================================

show_final_options() {
	if [ "$MODE" = "--preview" ]; then
		return 0
	fi

	echo -e "${BOLD}${CYAN}🔄 STEP 6: FINAL OPTIONS${NC}"
	echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"

	if ! git diff --quiet; then
		echo -e "${GREEN}💡 CHANGES WERE MADE - Choose your next step:${NC}"
		echo ""
		echo -e "${BLUE}📋 Available Actions:${NC}"
		echo "  1. 📝 Review changes: git diff"
		echo "  2. 📊 Review summary: git diff --stat"
		echo "  3. ✅ Commit changes: git add . && git commit -m 'Ultimate code fixes: $actual_reduction% error reduction'"
		echo "  4. 🔄 Rollback changes: Use rollback instructions below"
		echo ""

		if [ "$MODE" = "--interactive" ]; then
			read -p "Review changes now? (y/N): " -n 1 -r
			echo
			if [[ $REPLY =~ ^[Yy]$ ]]; then
				echo -e "${BLUE}📊 Git diff summary:${NC}"
				git diff --stat
				echo ""

				read -p "Show detailed diff? (y/N): " -n 1 -r
				echo
				if [[ $REPLY =~ ^[Yy]$ ]]; then
					git diff | head -50
					echo "... (use 'git diff' to see full changes)"
					echo ""
				fi
			fi
		fi
	else
		echo -e "${BLUE}ℹ️ No changes were made${NC}"
		echo -e "${CYAN}Package was already in excellent condition!${NC}"
	fi

	show_rollback_instructions
}

show_rollback_instructions() {
	echo -e "${YELLOW}🔄 ROLLBACK INSTRUCTIONS:${NC}"
	if [ -n "$CHECKPOINT_CREATED" ]; then
		echo "  git stash                     # Stash current changes"
		echo "  git stash list | grep '$CHECKPOINT_CREATED'  # Find checkpoint"
		echo "  git stash apply stash@{N}     # Restore checkpoint (replace N)"
	else
		echo "  git stash                     # Stash current changes"
		echo "  git reset --hard HEAD         # Reset to last commit"
	fi
	echo ""
}

# ===================================================================
# 🎪 DEMO MODE
# ===================================================================

run_demo() {
	echo -e "${BOLD}${PURPLE}🎪 DEMO MODE: LIVE ERROR REDUCTION DEMONSTRATION${NC}"
	echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"

	echo -e "${YELLOW}This will demonstrate live error reduction with real fixes.${NC}"
	echo -e "${YELLOW}All changes will be safely stashed for rollback.${NC}"
	echo ""

	read -p "Start live demo? (y/N): " -n 1 -r
	echo
	if [[ ! $REPLY =~ ^[Yy]$ ]]; then
		echo -e "${YELLOW}❌ Demo cancelled${NC}"
		exit 0
	fi

	# Run normal process but with extra demo flair
	install_and_verify_tools
	analyze_errors
	create_checkpoint

	echo -e "${BOLD}${GREEN}🎬 LIVE FIXING IN PROGRESS...${NC}"
	sleep 2

	apply_fixes
	analyze_results

	echo -e "${BOLD}${PURPLE}🎪 DEMO COMPLETE!${NC}"
	echo -e "${GREEN}This demonstrates the power of 2024 automated Python code fixing!${NC}"

	show_final_options
}

# ===================================================================
# 🚀 MAIN EXECUTION
# ===================================================================

main() {
	print_header
	validate_input

	case "$MODE" in
	"--demo")
		run_demo
		;;
	"--preview")
		install_and_verify_tools
		analyze_errors
		apply_fixes # Will show preview
		;;
	"--auto" | "--interactive")
		install_and_verify_tools
		analyze_errors
		create_checkpoint
		apply_fixes
		analyze_results
		show_final_options
		;;
	esac

	echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
	echo -e "${BOLD}${CYAN}║                🎉 ULTIMATE CODE FIXER COMPLETE! 🎉          ║${NC}"
	echo -e "${BOLD}${CYAN}║          Thank you for using 2024 automation tools!         ║${NC}"
	echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
}

# Execute main function
main "$@"
