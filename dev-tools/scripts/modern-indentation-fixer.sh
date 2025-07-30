#!/bin/bash
# 🔧 Modern Indentation Fixer - Better than reindent
# Usage: ./dev-tools/scripts/modern-indentation-fixer.sh <directory> [--fix|--preview] [--tool=autopep8|black|yapf]
#
# 🎯 Uses modern tools instead of old reindent:
# - autopep8: Targets specific indentation errors (E101, E111, E114, E121, E122, E124, E125, E127, E128)
# - black: Opinionated 4-space formatting  
# - yapf: Configurable Google-style formatting
# - Custom libcst-based fixer for complex cases

set -e

DIRECTORY=${1:-"packages/haive-prebuilt/src"}
MODE=${2:-"--preview"}
TOOL=${3:-"--tool=autopep8"}

# Extract tool name
TOOL_NAME=$(echo "$TOOL" | sed 's/--tool=//')

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

echo -e "${CYAN}🔧 MODERN INDENTATION FIXER${NC}"
echo -e "${BLUE}📂 Directory: $DIRECTORY${NC}"
echo -e "${BLUE}🔧 Mode: $MODE${NC}"
echo -e "${BLUE}🛠️  Tool: $TOOL_NAME${NC}"
echo ""

# Safety checkpoint
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
echo -e "${PURPLE}🛡️ Creating safety checkpoint...${NC}"
git stash push -m "INDENTATION_FIX_${TOOL_NAME}_${TIMESTAMP}" || echo "⚠️ No changes to stash"

# ===================================================================
# 🔍 PHASE 1: ANALYZE INDENTATION ISSUES
# ===================================================================

echo -e "${PURPLE}🔍 PHASE 1: ANALYZING INDENTATION ISSUES...${NC}"
echo ""

# Count actual indentation errors using Python compilation
echo "🔍 Scanning for real indentation and syntax issues..."
ANALYSIS_RESULT=$(python3 -c "
import os
syntax_errors = 0
indentation_errors = 0
e101_issues = 0
problematic_files = []

for root, dirs, files in os.walk('$DIRECTORY'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r') as f:
                    content = f.read()
                    # Check for mixed tabs/spaces (basic check)
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if line.strip() and '\t' in line and '    ' in line:
                            e101_issues += 1
                            break
                    compile(content, filepath, 'exec')
            except IndentationError:
                indentation_errors += 1
                problematic_files.append(f'INDENT: {filepath}')
            except SyntaxError:
                syntax_errors += 1
                problematic_files.append(f'SYNTAX: {filepath}')
            except Exception:
                pass

print(f'{indentation_errors}|{syntax_errors}|{e101_issues}')
")

IFS='|' read -r INDENTATION_ERRORS SYNTAX_ERRORS E101_APPROX <<< "$ANALYSIS_RESULT"

# Get actual ruff counts for supported codes
E101_FILES=$(ruff check "$DIRECTORY" --select E101 --output-format=concise 2>/dev/null | wc -l || echo "0")

TOTAL_INDENT_ISSUES=$((INDENTATION_ERRORS + E101_FILES))

# Get additional ruff indentation codes  
E111_FILES=$(ruff check "$DIRECTORY" --select E111 --preview --output-format=concise 2>/dev/null | wc -l || echo "0")
E112_FILES=$(ruff check "$DIRECTORY" --select E112 --preview --output-format=concise 2>/dev/null | wc -l || echo "0")
E113_FILES=$(ruff check "$DIRECTORY" --select E113 --preview --output-format=concise 2>/dev/null | wc -l || echo "0")
E116_FILES=$(ruff check "$DIRECTORY" --select E116 --preview --output-format=concise 2>/dev/null | wc -l || echo "0")
E117_FILES=$(ruff check "$DIRECTORY" --select E117 --preview --output-format=concise 2>/dev/null | wc -l || echo "0")

echo -e "${YELLOW}📊 ACTUAL INDENTATION ISSUES DETECTED:${NC}"
echo "  🔴 Files with IndentationError: $INDENTATION_ERRORS"
echo "  🔴 Files with SyntaxError: $SYNTAX_ERRORS"
echo "  🔴 E101 (mixed tabs/spaces): $E101_FILES line-level issues"
echo "  🔴 E111 (indentation-with-invalid-multiple): $E111_FILES"  
echo "  🔴 E112 (no-indented-block): $E112_FILES"
echo "  🔴 E113 (unexpected-indentation): $E113_FILES"
echo "  🔴 E116 (unexpected-indentation-comment): $E116_FILES"
echo "  🔴 E117 (over-indented): $E117_FILES"
echo "  📊 Critical files needing fix: $((INDENTATION_ERRORS + SYNTAX_ERRORS))"
echo "  📊 Line-level style issues: $((E101_FILES + E111_FILES + E112_FILES + E113_FILES + E116_FILES + E117_FILES))"
echo ""

# ===================================================================
# 🔧 PHASE 2: APPLY TOOL-SPECIFIC FIXES
# ===================================================================

if [ "$MODE" = "--fix" ]; then
    echo -e "${PURPLE}🔧 PHASE 2: APPLYING $TOOL_NAME INDENTATION FIXES...${NC}"
    echo ""
    
    case $TOOL_NAME in
        "autopep8")
            echo -e "${BLUE}🎯 Using autopep8 for targeted indentation fixes...${NC}"
            echo "  • Targeting specific indentation errors only"
            echo "  • Using 4-space indentation"
            echo "  • Aggressive mode for stubborn issues"
            echo ""
            
            # Target only indentation-related errors
            AUTOPEP8_SELECT="E101,E111,E114,E121,E122,E124,E125,E127,E128"
            
            find "$DIRECTORY" -name "*.py" -type f | while read -r file; do
                echo -e "${BLUE}🔧 Fixing indentation: $(basename "$file")${NC}"
                
                # Try gentle fix first
                if poetry run autopep8 --in-place --select="$AUTOPEP8_SELECT" --indent-size=4 "$file" 2>/dev/null; then
                    echo "  ✅ Gentle fix applied"
                else
                    # Try aggressive mode for stubborn files
                    if poetry run autopep8 --in-place --aggressive --aggressive --select="$AUTOPEP8_SELECT" --indent-size=4 "$file" 2>/dev/null; then
                        echo "  ⚡ Aggressive fix applied"
                    else
                        echo "  ⚠️ Could not fix (syntax errors?)"
                    fi
                fi
            done
            ;;
            
        "black")
            echo -e "${BLUE}🎯 Using Black for opinionated 4-space formatting...${NC}"
            echo "  • Zero configuration required"
            echo "  • Enforces 4-space indentation"
            echo "  • Handles modern Python syntax"
            echo ""
            
            if poetry run black "$DIRECTORY" 2>/dev/null; then
                echo "  ✅ Black formatting applied"
            else
                echo "  ⚠️ Black could not format some files (syntax errors?)"
            fi
            ;;
            
        "yapf")
            echo -e "${BLUE}🎯 Using YAPF for configurable Google-style formatting...${NC}"
            echo "  • Using Google style configuration"  
            echo "  • 4-space indentation with hanging indents"
            echo "  • Configurable via .style.yapf"
            echo ""
            
            # Create temporary style config for indentation focus
            cat > /tmp/yapf_indent_style.yapf << 'EOF'
[style]
based_on_style = google
indent_width = 4
continuation_indent_width = 4
allow_multiline_lambdas = false
indent_closing_brackets = false
EOF
            
            if poetry run yapf --in-place --style=/tmp/yapf_indent_style.yapf --recursive "$DIRECTORY" 2>/dev/null; then
                echo "  ✅ YAPF formatting applied"
            else
                echo "  ⚠️ YAPF could not format some files (syntax errors?)"
            fi
            
            rm -f /tmp/yapf_indent_style.yapf
            ;;
            
        "ruff")
            echo -e "${BLUE}🎯 Using Ruff for fast indentation fixes...${NC}"
            echo "  • Rust-based high performance"
            echo "  • Fixes safe indentation issues only"
            echo "  • Integrates linting + formatting"
            echo ""
            
            # Use ruff to fix indentation issues
            if ruff check "$DIRECTORY" --select E101,E111,E114,E121,E122,E124,E125,E127,E128 --fix 2>/dev/null; then
                echo "  ✅ Ruff indentation fixes applied"
                
                # Follow up with ruff format for consistency
                if ruff format "$DIRECTORY" 2>/dev/null; then
                    echo "  ✅ Ruff formatting applied"
                fi
            else
                echo "  ⚠️ Ruff could not fix some files (syntax errors?)"
            fi
            ;;
            
        *)
            echo -e "${RED}❌ Unknown tool: $TOOL_NAME${NC}"
            echo "Available tools: autopep8, black, yapf, ruff"
            exit 1
            ;;
    esac
    
    echo -e "${GREEN}✅ $TOOL_NAME indentation fixes completed${NC}"
    echo ""
fi

# ===================================================================
# 📊 PHASE 3: SHOW RESULTS
# ===================================================================

echo -e "${PURPLE}📊 SHOWING RESULTS...${NC}"
echo ""

if [ "$MODE" = "--fix" ]; then
    # Recheck indentation issues
    FINAL_E101=$(ruff check "$DIRECTORY" --select E101 2>/dev/null | wc -l || echo "0")
    FINAL_E111=$(ruff check "$DIRECTORY" --select E111 2>/dev/null | wc -l || echo "0")
    FINAL_E114=$(ruff check "$DIRECTORY" --select E114 2>/dev/null | wc -l || echo "0")
    FINAL_TOTAL=$((FINAL_E101 + FINAL_E111 + FINAL_E114))
    
    FIXED_ISSUES=$((TOTAL_INDENT_ISSUES - FINAL_TOTAL))
    
    # Show git changes
    if git diff --quiet; then
        echo -e "${YELLOW}ℹ️  No changes were made${NC}"
    else
        echo -e "${GREEN}🎉 INDENTATION CHANGES APPLIED:${NC}"
        echo ""
        
        # Show summary of changed files
        echo -e "${BLUE}📋 Modified files:${NC}"
        git diff --name-only | head -10 | while read -r file; do
            echo "  📝 $file"
        done
        [ $(git diff --name-only | wc -l) -gt 10 ] && echo "  ... and more"
        echo ""
        
        # Show sample diff
        echo -e "${BLUE}🔍 Sample changes:${NC}"
        git diff | head -30
        echo ""
        
        echo -e "${YELLOW}💡 TO REVIEW ALL CHANGES:${NC}"
        echo "  git diff                    # See all changes"
        echo "  git diff --stat             # Summary of changes"
        echo ""
    fi
    
    echo -e "${BLUE}📊 INDENTATION FIX RESULTS:${NC}"
    echo "  🔴 Original issues: $TOTAL_INDENT_ISSUES"
    echo "  🔴 Remaining issues: $FINAL_TOTAL"
    echo "  ✅ Fixed issues: $FIXED_ISSUES"
    
    if [ "$FINAL_TOTAL" -eq 0 ]; then
        echo ""
        echo -e "${GREEN}🎯 ALL INDENTATION ISSUES RESOLVED!${NC}"
    elif [ "$FIXED_ISSUES" -gt 0 ]; then
        echo ""
        echo -e "${YELLOW}📈 PROGRESS MADE! Fixed $FIXED_ISSUES indentation issues${NC}"
    fi
    
elif [ "$MODE" = "--preview" ]; then
    echo -e "${YELLOW}👀 PREVIEW MODE - Would apply the following fixes with $TOOL_NAME:${NC}"
    echo ""
    
    case $TOOL_NAME in
        "autopep8")
            echo -e "${CYAN}🎯 AUTOPEP8 STRATEGY:${NC}"
            echo "  1. Target specific indentation errors (E101, E111, E114, etc.)"
            echo "  2. Use 4-space indentation consistently"
            echo "  3. Apply gentle fixes first, then aggressive mode if needed"
            echo "  4. Preserve other formatting choices"
            ;;
        "black")
            echo -e "${CYAN}🎯 BLACK STRATEGY:${NC}" 
            echo "  1. Apply opinionated 4-space indentation"
            echo "  2. Reformat entire files for consistency"
            echo "  3. Zero configuration needed"
            echo "  4. May change line breaks and other formatting"
            ;;
        "yapf")
            echo -e "${CYAN}🎯 YAPF STRATEGY:${NC}"
            echo "  1. Use Google style configuration"
            echo "  2. Configurable indentation rules"
            echo "  3. Preserve some formatting preferences"
            echo "  4. Handle complex indentation scenarios"
            ;;
        "ruff")
            echo -e "${CYAN}🎯 RUFF STRATEGY:${NC}"
            echo "  1. Fast Rust-based indentation fixes"
            echo "  2. Safe fixes only (no unsafe changes)"
            echo "  3. Combine with ruff format for consistency"
            echo "  4. Excellent performance on large codebases"
            ;;
    esac
    
    echo ""
    echo -e "${GREEN}Run with --fix to apply $TOOL_NAME indentation fixes${NC}"
fi

echo ""
echo -e "${CYAN}🚀 Modern Indentation Fixer Complete!${NC}"
echo -e "${BLUE}💡 Consider trying different tools if one doesn't work${NC}"
echo -e "${BLUE}💡 autopep8 is best for surgical indentation fixes${NC}"
echo -e "${BLUE}💡 black is best for full reformatting with indentation${NC}" 