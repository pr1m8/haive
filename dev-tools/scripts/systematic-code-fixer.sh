#!/bin/bash
# 🔄 Systematic Code Fixer - Safe, Step-by-Step Code Quality Improvement
# Usage: ./dev-tools/scripts/systematic-code-fixer.sh <directory> [--fix|--preview] [--step=all|1|2|3|4]
#
# 🎯 SYSTEMATIC APPROACH:
# Step 1: 🚨 Pre-flight syntax fixes (typos, obvious errors)
# Step 2: 🔧 Indentation and formatting fixes
# Step 3: 📦 Import management (missing, unused, sorting)
# Step 4: 🐍 Python modernization (f-strings, typing, etc.)

set -e

DIRECTORY=${1:-"packages/haive-prebuilt/src"}
MODE=${2:-"--preview"}
STEP=${3:-"--step=all"}

# Extract step number
STEP_NUM=$(echo "$STEP" | sed 's/--step=//')

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

if [ ! -d "$DIRECTORY" ]; then
	echo -e "${RED}❌ Directory not found: $DIRECTORY${NC}"
	exit 1
fi

echo -e "${BOLD}${CYAN}🔄 SYSTEMATIC CODE FIXER${NC}"
echo -e "${BLUE}📂 Directory: $DIRECTORY${NC}"
echo -e "${BLUE}🔧 Mode: $MODE${NC}"
echo -e "${BLUE}📋 Steps: $STEP_NUM${NC}"
echo ""

# Master safety checkpoint
MASTER_TIMESTAMP=$(date +%Y%m%d_%H%M%S)
echo -e "${PURPLE}🛡️ Creating MASTER safety checkpoint...${NC}"
git stash push -m "SYSTEMATIC_FIXER_MASTER_${MASTER_TIMESTAMP}" -- "$DIRECTORY" || echo "⚠️ Package stash failed - no changes to stash"

# ===================================================================
# 📊 INITIAL ASSESSMENT
# ===================================================================

echo -e "${BOLD}${PURPLE}📊 INITIAL ASSESSMENT${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"

# Get baseline metrics
INITIAL_ASSESSMENT=$(python3 -c "
import os
syntax_errors = 0
indentation_errors = 0
total_files = 0

for root, dirs, files in os.walk('$DIRECTORY'):
    for file in files:
        if file.endswith('.py'):
            total_files += 1
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r') as f:
                    compile(f.read(), filepath, 'exec')
            except IndentationError:
                indentation_errors += 1
            except SyntaxError:
                syntax_errors += 1
            except Exception:
                pass

print(f'{total_files}|{syntax_errors}|{indentation_errors}')
")

IFS='|' read -r TOTAL_FILES INITIAL_SYNTAX_ERRORS INITIAL_INDENT_ERRORS <<<"$INITIAL_ASSESSMENT"

echo -e "${YELLOW}📊 BASELINE METRICS:${NC}"
echo "  📁 Total Python files: $TOTAL_FILES"
echo "  🚨 Files with SyntaxErrors: $INITIAL_SYNTAX_ERRORS"
echo "  🔧 Files with IndentationErrors: $INITIAL_INDENT_ERRORS"
echo "  ✅ Healthy files: $((TOTAL_FILES - INITIAL_SYNTAX_ERRORS - INITIAL_INDENT_ERRORS))"
echo ""

# ===================================================================
# 🤖 STEP 0: AUTO-IMPORT MISSING IMPORTS
# ===================================================================

if [ "$STEP_NUM" = "all" ] || [ "$STEP_NUM" = "0" ]; then
	echo -e "${BOLD}${GREEN}🤖 STEP 0: AUTO-IMPORT MISSING IMPORTS${NC}"
	echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
	echo -e "${YELLOW}🎯 Goal: Automatically add missing imports for undefined names (F821)${NC}"
	echo ""

	if [ "$MODE" = "--fix" ]; then
		# Install autoimport if needed
		if ! poetry show autoimport >/dev/null 2>&1; then
			echo -e "${BLUE}📥 Installing autoimport...${NC}"
			poetry add --group dev autoimport
		fi

		echo -e "${BLUE}🔧 Running autoimport to fix undefined names...${NC}"
		poetry run autoimport "$DIRECTORY" || echo -e "${YELLOW}⚠️ Autoimport completed with warnings${NC}"

		# Check results
		F821_BEFORE=$(poetry run ruff check "$DIRECTORY" --select F821 2>/dev/null | wc -l || echo "0")
		echo -e "${GREEN}✅ STEP 0 COMPLETE: Missing imports added${NC}"
		echo -e "${YELLOW}   F821 undefined names remaining: $F821_BEFORE${NC}"
		echo ""
	else
		F821_COUNT=$(poetry run ruff check "$DIRECTORY" --select F821 2>/dev/null | wc -l || echo "0")
		echo -e "${BLUE}👀 Preview: Would run autoimport to fix $F821_COUNT undefined names (F821)${NC}"
		echo ""
	fi
fi

# ===================================================================
# 🚨 STEP 1: PRE-FLIGHT SYNTAX FIXES
# ===================================================================

if [ "$STEP_NUM" = "all" ] || [ "$STEP_NUM" = "1" ]; then
	echo -e "${BOLD}${RED}🚨 STEP 1: PRE-FLIGHT SYNTAX FIXES${NC}"
	echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
	echo -e "${YELLOW}🎯 Goal: Fix obvious typos that prevent tools from working${NC}"
	echo ""

	if [ "$MODE" = "--fix" ]; then
		echo -e "${BLUE}🔧 Running pre-flight syntax fixer...${NC}"
		./dev-tools/scripts/pre-flight-syntax-fixer.sh "$DIRECTORY" --fix

		# Verify step 1 results
		STEP1_RESULT=$(python3 -c "
import os
syntax_errors = 0
indentation_errors = 0

for root, dirs, files in os.walk('$DIRECTORY'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r') as f:
                    compile(f.read(), filepath, 'exec')
            except IndentationError:
                indentation_errors += 1
            except SyntaxError:
                syntax_errors += 1
            except Exception:
                pass

print(f'{syntax_errors}|{indentation_errors}')
")

		IFS='|' read -r STEP1_SYNTAX STEP1_INDENT <<<"$STEP1_RESULT"

		echo -e "${GREEN}✅ STEP 1 COMPLETE:${NC}"
		echo "  🚨 SyntaxErrors: $INITIAL_SYNTAX_ERRORS → $STEP1_SYNTAX (fixed: $((INITIAL_SYNTAX_ERRORS - STEP1_SYNTAX)))"
		echo "  🔧 IndentationErrors: $INITIAL_INDENT_ERRORS → $STEP1_INDENT"
		echo ""

		if [ "$STEP1_SYNTAX" -gt 0 ]; then
			echo -e "${YELLOW}⚠️  Still have $STEP1_SYNTAX syntax errors - may need manual fixes${NC}"
			echo ""
		fi
	else
		echo -e "${BLUE}👀 Preview: Would run pre-flight syntax fixer${NC}"
		./dev-tools/scripts/pre-flight-syntax-fixer.sh "$DIRECTORY" --preview
		echo ""
	fi
fi

# ===================================================================
# 🔧 STEP 2: INDENTATION AND FORMATTING
# ===================================================================

if [ "$STEP_NUM" = "all" ] || [ "$STEP_NUM" = "2" ]; then
	echo -e "${BOLD}${CYAN}🔧 STEP 2: INDENTATION AND FORMATTING${NC}"
	echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
	echo -e "${YELLOW}🎯 Goal: Fix indentation and apply consistent formatting${NC}"
	echo ""

	if [ "$MODE" = "--fix" ]; then
		# Check if we have too many syntax errors to proceed
		CURRENT_SYNTAX=$(python3 -c "
import os
syntax_errors = 0
for root, dirs, files in os.walk('$DIRECTORY'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r') as f:
                    compile(f.read(), filepath, 'exec')
            except SyntaxError:
                syntax_errors += 1
            except Exception:
                pass
print(syntax_errors)
")

		if [ "$CURRENT_SYNTAX" -gt 10 ]; then
			echo -e "${YELLOW}⚠️  Too many syntax errors ($CURRENT_SYNTAX) - skipping indentation step${NC}"
			echo -e "${YELLOW}   Run Step 1 manually or fix remaining syntax errors first${NC}"
			echo ""
		else
			echo -e "${BLUE}🔧 Running modern indentation fixer (autopep8)...${NC}"
			./dev-tools/scripts/modern-indentation-fixer.sh "$DIRECTORY" --fix --tool=autopep8

			echo -e "${GREEN}✅ STEP 2 COMPLETE: Indentation fixes applied${NC}"
			echo ""
		fi
	else
		echo -e "${BLUE}👀 Preview: Would run modern indentation fixer${NC}"
		./dev-tools/scripts/modern-indentation-fixer.sh "$DIRECTORY" --preview --tool=autopep8
		echo ""
	fi
fi

# ===================================================================
# 📦 STEP 3: IMPORT MANAGEMENT
# ===================================================================

if [ "$STEP_NUM" = "all" ] || [ "$STEP_NUM" = "3" ]; then
	echo -e "${BOLD}${GREEN}📦 STEP 3: IMPORT MANAGEMENT${NC}"
	echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
	echo -e "${YELLOW}🎯 Goal: Fix imports (missing, unused, sorting, absolute)${NC}"
	echo ""

	if [ "$MODE" = "--fix" ]; then
		# Install autoflake if needed
		if ! poetry show autoflake >/dev/null 2>&1; then
			echo -e "${BLUE}📥 Installing autoflake...${NC}"
			poetry add --group dev autoflake
		fi

		# Step 3a: Remove unused imports and variables
		echo -e "${BLUE}🔧 Step 3a: Removing unused imports (autoflake)...${NC}"
		poetry run autoflake --remove-all-unused-imports --remove-unused-variables --in-place --recursive "$DIRECTORY" || echo -e "${YELLOW}⚠️ autoflake completed with warnings${NC}"

		# Step 3b: Sort imports
		echo -e "${BLUE}🔧 Step 3b: Sorting imports (isort)...${NC}"
		poetry run isort "$DIRECTORY" || echo -e "${YELLOW}⚠️ isort completed with warnings${NC}"

		# Step 3c: Final import cleanup with ruff
		echo -e "${BLUE}🔧 Step 3c: Import cleanup (ruff)...${NC}"
		poetry run ruff check "$DIRECTORY" --select I,F401 --fix || echo -e "${YELLOW}⚠️ ruff completed with warnings${NC}"

		# Check results
		F401_COUNT=$(poetry run ruff check "$DIRECTORY" --select F401 2>/dev/null | wc -l || echo "0")
		I001_COUNT=$(poetry run ruff check "$DIRECTORY" --select I001 2>/dev/null | wc -l || echo "0")

		echo -e "${GREEN}✅ STEP 3 COMPLETE: Import management applied${NC}"
		echo -e "${YELLOW}   F401 unused imports remaining: $F401_COUNT${NC}"
		echo -e "${YELLOW}   I001 unsorted imports remaining: $I001_COUNT${NC}"
		echo ""
	else
		F401_COUNT=$(poetry run ruff check "$DIRECTORY" --select F401 2>/dev/null | wc -l || echo "0")
		I001_COUNT=$(poetry run ruff check "$DIRECTORY" --select I001 2>/dev/null | wc -l || echo "0")
		echo -e "${BLUE}👀 Preview: Would fix $F401_COUNT unused imports and $I001_COUNT unsorted imports${NC}"
		echo ""
	fi
fi

# ===================================================================
# 🐍 STEP 4: PYTHON MODERNIZATION
# ===================================================================

if [ "$STEP_NUM" = "all" ] || [ "$STEP_NUM" = "4" ]; then
	echo -e "${BOLD}${PURPLE}🐍 STEP 4: PYTHON MODERNIZATION${NC}"
	echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
	echo -e "${YELLOW}🎯 Goal: Modernize Python syntax (f-strings, typing, etc.)${NC}"
	echo ""

	if [ "$MODE" = "--fix" ]; then
		# Install pyupgrade if needed
		if ! poetry show pyupgrade >/dev/null 2>&1; then
			echo -e "${BLUE}📥 Installing pyupgrade...${NC}"
			poetry add --group dev pyupgrade
		fi

		# Step 4a: Modernize syntax with pyupgrade
		echo -e "${BLUE}🔧 Step 4a: Modernizing syntax (pyupgrade)...${NC}"
		find "$DIRECTORY" -name "*.py" -exec poetry run pyupgrade --py38-plus {} \; || echo -e "${YELLOW}⚠️ pyupgrade completed with warnings${NC}"

		# Step 4b: Apply ruff fixes for modernization
		echo -e "${BLUE}🔧 Step 4b: Additional modernization (ruff)...${NC}"
		poetry run ruff check "$DIRECTORY" --select UP,DTZ --fix || echo -e "${YELLOW}⚠️ ruff completed with warnings${NC}"

		# Step 4c: Final formatting with ruff
		echo -e "${BLUE}🔧 Step 4c: Code formatting (ruff format)...${NC}"
		poetry run ruff format "$DIRECTORY" || echo -e "${YELLOW}⚠️ ruff format completed with warnings${NC}"

		# Check results
		UP_COUNT=$(poetry run ruff check "$DIRECTORY" --select UP 2>/dev/null | wc -l || echo "0")
		DTZ_COUNT=$(poetry run ruff check "$DIRECTORY" --select DTZ 2>/dev/null | wc -l || echo "0")

		echo -e "${GREEN}✅ STEP 4 COMPLETE: Python modernization applied${NC}"
		echo -e "${YELLOW}   UP upgrade issues remaining: $UP_COUNT${NC}"
		echo -e "${YELLOW}   DTZ datetime issues remaining: $DTZ_COUNT${NC}"
		echo ""
	else
		UP_COUNT=$(poetry run ruff check "$DIRECTORY" --select UP 2>/dev/null | wc -l || echo "0")
		DTZ_COUNT=$(poetry run ruff check "$DIRECTORY" --select DTZ 2>/dev/null | wc -l || echo "0")
		echo -e "${BLUE}👀 Preview: Would modernize $UP_COUNT syntax upgrades and $DTZ_COUNT datetime issues${NC}"
		echo ""
	fi
fi

# ===================================================================
# 📊 FINAL ASSESSMENT
# ===================================================================

echo -e "${BOLD}${CYAN}📊 FINAL ASSESSMENT${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"

if [ "$MODE" = "--fix" ]; then
	# Get comprehensive final metrics
	FINAL_ASSESSMENT=$(python3 -c "
import os
syntax_errors = 0
indentation_errors = 0
clean_files = 0

for root, dirs, files in os.walk('$DIRECTORY'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r') as f:
                    compile(f.read(), filepath, 'exec')
                clean_files += 1
            except IndentationError:
                indentation_errors += 1
            except SyntaxError:
                syntax_errors += 1
            except Exception:
                pass

print(f'{syntax_errors}|{indentation_errors}|{clean_files}')
")

	IFS='|' read -r FINAL_SYNTAX FINAL_INDENT CLEAN_FILES <<<"$FINAL_ASSESSMENT"

	# Get comprehensive ruff error counts
	FINAL_TOTAL_ERRORS=$(poetry run ruff check "$DIRECTORY" 2>/dev/null | wc -l || echo "0")
	FINAL_F821=$(poetry run ruff check "$DIRECTORY" --select F821 2>/dev/null | wc -l || echo "0")
	FINAL_F401=$(poetry run ruff check "$DIRECTORY" --select F401 2>/dev/null | wc -l || echo "0")
	FINAL_I001=$(poetry run ruff check "$DIRECTORY" --select I001 2>/dev/null | wc -l || echo "0")

	echo -e "${GREEN}🎉 ENHANCED SYSTEMATIC FIXES COMPLETE!${NC}"
	echo ""
	echo -e "${YELLOW}📊 COMPILATION BEFORE → AFTER:${NC}"
	echo "  🚨 SyntaxErrors: $INITIAL_SYNTAX_ERRORS → $FINAL_SYNTAX"
	echo "  🔧 IndentationErrors: $INITIAL_INDENT_ERRORS → $FINAL_INDENT"
	echo "  ✅ Clean files: $((TOTAL_FILES - INITIAL_SYNTAX_ERRORS - INITIAL_INDENT_ERRORS)) → $CLEAN_FILES"
	echo ""
	echo -e "${YELLOW}📊 RUFF ERRORS BEFORE → AFTER:${NC}"
	echo "  🔴 F821 (undefined names): (baseline) → $FINAL_F821"
	echo "  🔴 F401 (unused imports): (baseline) → $FINAL_F401"
	echo "  🔴 I001 (unsorted imports): (baseline) → $FINAL_I001"
	echo "  📊 Total ruff errors: (baseline) → $FINAL_TOTAL_ERRORS"
	echo ""

	SYNTAX_FIXED=$((INITIAL_SYNTAX_ERRORS - FINAL_SYNTAX))
	INDENT_FIXED=$((INITIAL_INDENT_ERRORS - FINAL_INDENT))

	if [ "$SYNTAX_FIXED" -gt 0 ]; then
		echo -e "${GREEN}✅ Fixed $SYNTAX_FIXED syntax errors${NC}"
	fi
	if [ "$INDENT_FIXED" -gt 0 ]; then
		echo -e "${GREEN}✅ Fixed $INDENT_FIXED indentation errors${NC}"
	fi

	if [ "$FINAL_SYNTAX" -eq 0 ] && [ "$FINAL_INDENT" -eq 0 ]; then
		echo ""
		echo -e "${BOLD}${GREEN}🎯 ALL FILES NOW COMPILE SUCCESSFULLY! 🎉${NC}"
	elif [ "$FINAL_SYNTAX" -gt 0 ] || [ "$FINAL_INDENT" -gt 0 ]; then
		echo ""
		echo -e "${YELLOW}⚠️  Some files still need manual attention:${NC}"
		[ "$FINAL_SYNTAX" -gt 0 ] && echo "   🚨 $FINAL_SYNTAX files with syntax errors"
		[ "$FINAL_INDENT" -gt 0 ] && echo "   🔧 $FINAL_INDENT files with indentation errors"
	fi

	# Show git changes summary
	if ! git diff --quiet; then
		echo ""
		echo -e "${BLUE}📋 Files modified:${NC}"
		git diff --name-only | wc -l | xargs echo "  📝 Total changed files:"
		echo ""

		echo -e "${YELLOW}💡 TO REVIEW ALL CHANGES:${NC}"
		echo "  git diff --stat              # Summary of changes"
		echo "  git diff                     # See all changes"
		echo "  git stash                    # Stash current changes"
		echo ""
		echo -e "${YELLOW}💡 TO COMMIT CHANGES:${NC}"
		echo "  git add ."
		echo "  git commit -m 'Systematic code quality fixes'"
		echo ""
	fi

elif [ "$MODE" = "--preview" ]; then
	echo -e "${YELLOW}👀 PREVIEW MODE COMPLETE${NC}"
	echo ""
	echo -e "${CYAN}🎯 SYSTEMATIC FIX PLAN:${NC}"
	echo "  1. 🚨 Fix obvious syntax typos (return→return, st→str)"
	echo "  2. 🔧 Apply indentation and formatting fixes"
	echo "  3. 📦 Manage imports (add missing, remove unused, sort)"
	echo "  4. 🐍 Modernize Python syntax (f-strings, typing)"
	echo ""
	echo -e "${GREEN}Run with --fix to execute this plan safely${NC}"
	echo -e "${GREEN}Or run individual steps: --step=1, --step=2, etc.${NC}"
fi

echo ""
echo -e "${YELLOW}💡 ROLLBACK INSTRUCTIONS:${NC}"
echo "  git stash                    # Stash current state"
echo "  git stash apply stash@{1}    # Restore master checkpoint"
echo ""

echo -e "${BOLD}${CYAN}🚀 Systematic Code Fixer Complete!${NC}"
echo -e "${BLUE}💡 Safe, step-by-step code quality improvement${NC}"
