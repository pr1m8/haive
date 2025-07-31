#!/bin/bash

# 🧠 Intelligent Error Analyzer & Categorizer
# Analyzes Python code errors by severity and safety level
# Automatically selects the safest fixing approach for different error types

set -euo pipefail

# Configuration
SCRIPT_NAME="$(basename "$0")"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="dev-tools/logs/error-analysis-${TIMESTAMP}.log"

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Error severity levels
declare -A ERROR_SEVERITY=(
    ["CRITICAL"]="1"    # Prevents parsing entirely
    ["HIGH"]="2"        # Major syntax issues
    ["MEDIUM"]="3"      # Style/import issues
    ["LOW"]="4"         # Minor formatting
    ["SAFE"]="5"        # Cosmetic only
)

# Safety levels for fixes
declare -A FIX_SAFETY=(
    ["EMERGENCY"]="1"   # sed replacements for critical typos
    ["SURGICAL"]="2"    # autopep8 aggressive for indentation
    ["MODERATE"]="3"    # pyupgrade, ruff fixes
    ["CONSERVATIVE"]="4" # isort, ruff format
    ["COSMETIC"]="5"    # black, yapf
)

# Error patterns and their classifications
declare -A ERROR_PATTERNS=(
    # CRITICAL - Prevents parsing
    ["SyntaxError.*unexpected indent"]="CRITICAL|SURGICAL"
    ["SyntaxError.*invalid syntax"]="CRITICAL|EMERGENCY"
    ["SyntaxError.*unterminated string"]="CRITICAL|EMERGENCY"
    ["IndentationError"]="CRITICAL|SURGICAL"
    ["SyntaxError.*unmatched"]="CRITICAL|EMERGENCY"
    ["SyntaxError.*invalid decimal literal"]="CRITICAL|EMERGENCY"
    ["SyntaxError.*expected.*expression"]="CRITICAL|EMERGENCY"

    # HIGH - Major syntax issues
    ["E999.*SyntaxError"]="HIGH|SURGICAL"
    ["F821.*undefined name"]="HIGH|MODERATE"
    ["E101.*indentation contains mixed"]="HIGH|SURGICAL"
    ["E111.*indentation is not a multiple"]="HIGH|SURGICAL"
    ["E114.*indentation is not a multiple.*comment"]="HIGH|SURGICAL"

    # MEDIUM - Import and style issues
    ["TID251.*Banned relative import"]="MEDIUM|MODERATE"
    ["TID252.*Relative imports from parent"]="MEDIUM|MODERATE"
    ["F401.*imported but unused"]="MEDIUM|CONSERVATIVE"
    ["I001.*Import block is un-sorted"]="MEDIUM|CONSERVATIVE"
    ["UP032.*Use f-string"]="MEDIUM|MODERATE"

    # LOW - Minor formatting
    ["E501.*line too long"]="LOW|CONSERVATIVE"
    ["W291.*trailing whitespace"]="LOW|CONSERVATIVE"
    ["E302.*expected 2 blank lines"]="LOW|CONSERVATIVE"

    # SAFE - Cosmetic
    ["E203.*whitespace before"]="SAFE|COSMETIC"
    ["E231.*missing whitespace after"]="SAFE|COSMETIC"
)

# Tool configurations by safety level
declare -A TOOL_CONFIG=(
    ["EMERGENCY"]="sed|Custom regex patterns for critical typos"
    ["SURGICAL"]="autopep8|autopep8 --aggressive --aggressive --in-place"
    ["MODERATE"]="pyupgrade+ruff|pyupgrade --py38-plus && ruff check --fix"
    ["CONSERVATIVE"]="isort+ruff|isort . && ruff check --fix --select I,F401"
    ["COSMETIC"]="black|black ."
)

usage() {
    cat << EOF
🧠 ${SCRIPT_NAME} - Intelligent Error Analyzer & Categorizer

USAGE:
    $0 <directory> [options]

OPTIONS:
    --analyze-only       Only analyze errors, don't suggest fixes
    --fix                Apply fixes automatically based on safety analysis
    --preview            Show what would be fixed without applying
    --safety-level <N>   Only apply fixes up to safety level N (1-5)
    --report <format>    Generate report (json|markdown|text)
    --verbose            Show detailed analysis

SAFETY LEVELS:
    1 = EMERGENCY    (sed replacements for critical typos)
    2 = SURGICAL     (autopep8 aggressive for indentation)
    3 = MODERATE     (pyupgrade, ruff fixes)
    4 = CONSERVATIVE (isort, ruff format)
    5 = COSMETIC     (black, yapf)

EXAMPLES:
    # Analyze errors in haive-prebuilt
    $0 packages/haive-prebuilt/src --analyze-only

    # Apply only emergency and surgical fixes
    $0 packages/haive-prebuilt/src --fix --safety-level 2

    # Full analysis with markdown report
    $0 packages/haive-prebuilt/src --report markdown --verbose

EOF
}

log() {
    local level="$1"
    shift
    echo -e "[$level] $(date '+%H:%M:%S') $*" | tee -a "$LOG_FILE"
}

create_safety_checkpoint() {
    local dir="$1"
    local stash_name="error-analyzer-checkpoint-${TIMESTAMP}"

    log "INFO" "🛡️  Creating safety checkpoint for $DIRECTORY..."
    if git stash push -m "$stash_name" -- "$DIRECTORY" 2>/dev/null; then
        log "INFO" "✅ Safety checkpoint created for $DIRECTORY: $stash_name"
        echo "$stash_name"
    else
        log "WARN" "⚠️  No changes to stash in $DIRECTORY, proceeding without checkpoint"
        echo ""
    fi
}

analyze_python_file() {
    local file="$1"
    local errors=()

    # Check for compilation errors
    local compile_output
    if ! compile_output=$(python3 -c "
import sys
try:
    with open('$file', 'r') as f:
        compile(f.read(), '$file', 'exec')
except SyntaxError as e:
    print(f'SyntaxError:{e.lineno}:{e.msg}')
    sys.exit(1)
except IndentationError as e:
    print(f'IndentationError:{e.lineno}:{e.msg}')
    sys.exit(1)
" 2>&1); then
        errors+=("$compile_output")
    fi

    # Check with ruff
    local ruff_output
    if command -v ruff >/dev/null 2>&1; then
        if ruff_output=$(ruff check "$file" --output-format=text 2>/dev/null); then
            while IFS= read -r line; do
                [[ -n "$line" ]] && errors+=("$line")
            done <<< "$ruff_output"
        fi
    fi

    printf '%s\n' "${errors[@]}"
}

categorize_error() {
    local error="$1"
    local severity="UNKNOWN"
    local safety="UNKNOWN"

    for pattern in "${!ERROR_PATTERNS[@]}"; do
        if [[ $error =~ $pattern ]]; then
            IFS='|' read -r severity safety <<< "${ERROR_PATTERNS[$pattern]}"
            break
        fi
    done

    echo "${severity}|${safety}"
}

analyze_directory() {
    local directory="$1"
    local verbose="$2"

    log "INFO" "🔍 Analyzing directory: $directory"

    # Initialize counters
    declare -A severity_counts=()
    declare -A safety_counts=()
    declare -A file_errors=()

    # Find all Python files
    local python_files=()
    while IFS= read -r -d '' file; do
        python_files+=("$file")
    done < <(find "$directory" -name "*.py" -type f -print0)

    log "INFO" "📊 Found ${#python_files[@]} Python files"

    # Analyze each file
    local total_errors=0
    for file in "${python_files[@]}"; do
        local file_error_count=0
        local file_errors_list=()

        while IFS= read -r error; do
            [[ -z "$error" ]] && continue

            local classification
            classification=$(categorize_error "$error")
            IFS='|' read -r severity safety <<< "$classification"

            # Count by severity and safety
            ((severity_counts["$severity"]++)) || severity_counts["$severity"]=1
            ((safety_counts["$safety"]++)) || safety_counts["$safety"]=1
            ((total_errors++))
            ((file_error_count++))

            file_errors_list+=("$error|$severity|$safety")

            if [[ "$verbose" == "true" ]]; then
                echo -e "${CYAN}📁 $file${NC}"
                echo -e "   ${RED}❌ $error${NC}"
                echo -e "   ${YELLOW}🏷️  Severity: $severity, Safety: $safety${NC}"
                echo
            fi
        done < <(analyze_python_file "$file")

        if [[ $file_error_count -gt 0 ]]; then
            file_errors["$file"]="$file_error_count"
        fi
    done

    # Generate summary
    echo
    echo -e "${BLUE}📊 ERROR ANALYSIS SUMMARY${NC}"
    echo "=================================="
    echo -e "${CYAN}📁 Directory: $directory${NC}"
    echo -e "${CYAN}🔍 Files analyzed: ${#python_files[@]}${NC}"
    echo -e "${CYAN}❌ Total errors: $total_errors${NC}"
    echo -e "${CYAN}📝 Files with errors: ${#file_errors[@]}${NC}"
    echo

    # Severity breakdown
    echo -e "${RED}🚨 BY SEVERITY:${NC}"
    for severity in CRITICAL HIGH MEDIUM LOW SAFE UNKNOWN; do
        local count="${severity_counts[$severity]:-0}"
        if [[ $count -gt 0 ]]; then
            case $severity in
                CRITICAL) echo -e "   ${RED}🔴 $severity: $count${NC}" ;;
                HIGH)     echo -e "   ${YELLOW}🟡 $severity: $count${NC}" ;;
                MEDIUM)   echo -e "   ${BLUE}🔵 $severity: $count${NC}" ;;
                LOW)      echo -e "   ${GREEN}🟢 $severity: $count${NC}" ;;
                SAFE)     echo -e "   ${CYAN}⚪ $severity: $count${NC}" ;;
                *)        echo -e "   ${PURPLE}❓ $severity: $count${NC}" ;;
            esac
        fi
    done
    echo

    # Safety recommendations
    echo -e "${GREEN}🛡️  RECOMMENDED FIX APPROACH:${NC}"
    for safety in EMERGENCY SURGICAL MODERATE CONSERVATIVE COSMETIC UNKNOWN; do
        local count="${safety_counts[$safety]:-0}"
        if [[ $count -gt 0 ]]; then
            local tools="${TOOL_CONFIG[$safety]:-Unknown}"
            IFS='|' read -r tool_name tool_cmd <<< "$tools"
            case $safety in
                EMERGENCY)    echo -e "   ${RED}🚨 $safety ($count errors): $tool_name${NC}" ;;
                SURGICAL)     echo -e "   ${YELLOW}⚡ $safety ($count errors): $tool_name${NC}" ;;
                MODERATE)     echo -e "   ${BLUE}🔧 $safety ($count errors): $tool_name${NC}" ;;
                CONSERVATIVE) echo -e "   ${GREEN}✅ $safety ($count errors): $tool_name${NC}" ;;
                COSMETIC)     echo -e "   ${CYAN}💄 $safety ($count errors): $tool_name${NC}" ;;
                *)            echo -e "   ${PURPLE}❓ $safety ($count errors): Unknown${NC}" ;;
            esac
        fi
    done

    # Store analysis results for potential fixing
    echo "$total_errors" > "/tmp/error_analysis_${TIMESTAMP}.total"
    printf '%s\n' "${!file_errors[@]}" > "/tmp/error_analysis_${TIMESTAMP}.files"

    # Return severity counts for decision making
    local critical_count="${severity_counts[CRITICAL]:-0}"
    local high_count="${severity_counts[HIGH]:-0}"

    echo
    if [[ $critical_count -gt 0 ]]; then
        echo -e "${RED}⚠️  CRITICAL: $critical_count critical errors must be fixed first${NC}"
        return 1
    elif [[ $high_count -gt 0 ]]; then
        echo -e "${YELLOW}⚠️  HIGH: $high_count high-severity errors should be prioritized${NC}"
        return 2
    else
        echo -e "${GREEN}✅ No critical or high-severity errors detected${NC}"
        return 0
    fi
}

apply_emergency_fixes() {
    local directory="$1"
    local preview="$2"

    log "INFO" "🚨 Applying emergency fixes (critical typos)..."

    local fixes_applied=0
    local emergency_patterns=(
        "s/return /return /g"
        "s/^[ ]*return$/&n/"
        "s/return/return/g"
        "s/) -> st:/) -> str:/g"
        "s/from haive-prebuilt\.src\.haive\.prebuilt/from haive.prebuilt/g"
        "s/from haive-games\.src\.haive\.games/from haive.games/g"
        "s/from haive-dataflow\.src\.haive\.dataflow/from haive.dataflow/g"
        "s/from haive-mcp\.src\.haive\.mcp/from haive.mcp/g"
    )

    for pattern in "${emergency_patterns[@]}"; do
        echo -e "${RED}🔧 Applying pattern: $pattern${NC}"

        if [[ "$preview" == "true" ]]; then
            # Show what would be changed
            find "$directory" -name "*.py" -exec grep -l "${pattern//s\///}" {} \; 2>/dev/null || true
        else
            # Apply the fix
            local changed_files
            changed_files=$(find "$directory" -name "*.py" -exec sed -i "$pattern" {} \; -exec echo {} \; 2>/dev/null || true)
            if [[ -n "$changed_files" ]]; then
                ((fixes_applied++))
                log "INFO" "✅ Pattern applied to files: $changed_files"
            fi
        fi
    done

    echo -e "${GREEN}🚨 Emergency fixes: $fixes_applied patterns applied${NC}"
}

apply_surgical_fixes() {
    local directory="$1"
    local preview="$2"

    log "INFO" "⚡ Applying surgical fixes (indentation)..."

    if ! command -v autopep8 >/dev/null 2>&1; then
        log "WARN" "autopep8 not found, skipping surgical fixes"
        return 1
    fi

    if [[ "$preview" == "true" ]]; then
        echo -e "${YELLOW}⚡ Would apply: autopep8 --aggressive --aggressive --diff${NC}"
        autopep8 --aggressive --aggressive --diff "$directory"/*.py 2>/dev/null | head -20
    else
        echo -e "${YELLOW}⚡ Applying: autopep8 --aggressive --aggressive --in-place${NC}"
        find "$directory" -name "*.py" -exec autopep8 --aggressive --aggressive --in-place {} \;
        log "INFO" "✅ Surgical indentation fixes applied"
    fi
}

apply_moderate_fixes() {
    local directory="$1"
    local preview="$2"

    log "INFO" "🔧 Applying moderate fixes (pyupgrade + ruff)..."

    if [[ "$preview" == "true" ]]; then
        echo -e "${BLUE}🔧 Would apply: pyupgrade + ruff fixes${NC}"
        if command -v ruff >/dev/null 2>&1; then
            ruff check "$directory" --select UP032,F821,TID251,TID252 --diff 2>/dev/null | head -20
        fi
    else
        # Apply pyupgrade
        if command -v pyupgrade >/dev/null 2>&1; then
            find "$directory" -name "*.py" -exec pyupgrade --py38-plus {} \;
        fi

        # Apply ruff fixes
        if command -v ruff >/dev/null 2>&1; then
            ruff check "$directory" --fix --select UP032,F821,TID251,TID252 2>/dev/null || true
        fi

        log "INFO" "✅ Moderate fixes applied"
    fi
}

apply_conservative_fixes() {
    local directory="$1"
    local preview="$2"

    log "INFO" "✅ Applying conservative fixes (imports + formatting)..."

    if [[ "$preview" == "true" ]]; then
        echo -e "${GREEN}✅ Would apply: isort + ruff format${NC}"
        if command -v isort >/dev/null 2>&1; then
            isort --diff "$directory" 2>/dev/null | head -10
        fi
    else
        # Apply isort
        if command -v isort >/dev/null 2>&1; then
            isort "$directory" 2>/dev/null || true
        fi

        # Apply ruff formatting
        if command -v ruff >/dev/null 2>&1; then
            ruff format "$directory" 2>/dev/null || true
        fi

        log "INFO" "✅ Conservative fixes applied"
    fi
}

apply_cosmetic_fixes() {
    local directory="$1"
    local preview="$2"

    log "INFO" "💄 Applying cosmetic fixes (black)..."

    if [[ "$preview" == "true" ]]; then
        echo -e "${CYAN}💄 Would apply: black formatting${NC}"
        if command -v black >/dev/null 2>&1; then
            black --diff "$directory" 2>/dev/null | head -10
        fi
    else
        if command -v black >/dev/null 2>&1; then
            black "$directory" 2>/dev/null || true
            log "INFO" "✅ Cosmetic fixes applied"
        fi
    fi
}

generate_report() {
    local format="$1"
    local directory="$2"

    local report_file="dev-tools/reports/error-analysis-${TIMESTAMP}.${format}"
    mkdir -p "$(dirname "$report_file")"

    case "$format" in
        "json")
            cat > "$report_file" << EOF
{
    "timestamp": "$TIMESTAMP",
    "directory": "$directory",
    "analysis": {
        "total_errors": $(cat "/tmp/error_analysis_${TIMESTAMP}.total" 2>/dev/null || echo 0),
        "files_with_errors": $(wc -l < "/tmp/error_analysis_${TIMESTAMP}.files" 2>/dev/null || echo 0)
    },
    "recommendations": {
        "emergency": "Apply sed patterns for critical typos",
        "surgical": "Use autopep8 --aggressive for indentation",
        "moderate": "Apply pyupgrade and ruff fixes",
        "conservative": "Use isort and ruff format",
        "cosmetic": "Apply black formatting"
    }
}
EOF
            ;;
        "markdown")
            cat > "$report_file" << EOF
# 🧠 Error Analysis Report

**Timestamp:** $TIMESTAMP
**Directory:** $directory

## 📊 Summary

- **Total Errors:** $(cat "/tmp/error_analysis_${TIMESTAMP}.total" 2>/dev/null || echo 0)
- **Files with Errors:** $(wc -l < "/tmp/error_analysis_${TIMESTAMP}.files" 2>/dev/null || echo 0)

## 🛡️ Recommended Fix Strategy

| Safety Level | Tool | Description |
|--------------|------|-------------|
| 🚨 Emergency | sed | Critical typo fixes |
| ⚡ Surgical | autopep8 | Aggressive indentation fixes |
| 🔧 Moderate | pyupgrade+ruff | Syntax modernization |
| ✅ Conservative | isort+ruff | Import organization |
| 💄 Cosmetic | black | Final formatting |

## 🚀 Usage

\`\`\`bash
# Apply fixes up to surgical level
$0 $directory --fix --safety-level 2

# Preview all potential fixes
$0 $directory --preview --safety-level 5
\`\`\`
EOF
            ;;
    esac

    echo -e "${GREEN}📄 Report generated: $report_file${NC}"
}

main() {
    local directory=""
    local analyze_only=false
    local fix=false
    local preview=false
    local safety_level=5
    local report_format=""
    local verbose=false

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --analyze-only) analyze_only=true; shift ;;
            --fix) fix=true; shift ;;
            --preview) preview=true; shift ;;
            --safety-level) safety_level="$2"; shift 2 ;;
            --report) report_format="$2"; shift 2 ;;
            --verbose) verbose=true; shift ;;
            --help|-h) usage; exit 0 ;;
            -*) echo "Unknown option: $1"; usage; exit 1 ;;
            *) directory="$1"; shift ;;
        esac
    done

    # Validate inputs
    if [[ -z "$directory" ]]; then
        echo "Error: Directory is required"
        usage
        exit 1
    fi

    if [[ ! -d "$directory" ]]; then
        echo "Error: Directory '$directory' does not exist"
        exit 1
    fi

    # Ensure log directory exists
    mkdir -p "$(dirname "$LOG_FILE")"

    # Start analysis
    log "INFO" "🧠 Starting intelligent error analysis..."
    log "INFO" "📁 Target: $directory"
    log "INFO" "🛡️  Safety level: $safety_level"

    # Analyze directory
    local analysis_result
    if ! analysis_result=$(analyze_directory "$directory" "$verbose"); then
        local exit_code=$?

        if [[ $exit_code -eq 1 ]]; then
            log "WARN" "Critical errors detected - emergency fixes recommended"
        elif [[ $exit_code -eq 2 ]]; then
            log "WARN" "High-severity errors detected - surgical fixes recommended"
        fi
    fi

    # Generate report if requested
    if [[ -n "$report_format" ]]; then
        generate_report "$report_format" "$directory"
    fi

    # Apply fixes if requested
    if [[ "$fix" == "true" || "$preview" == "true" ]]; then
        local checkpoint=""
        if [[ "$fix" == "true" ]]; then
            checkpoint=$(create_safety_checkpoint "$directory")
        fi

        echo
        echo -e "${BLUE}🔧 APPLYING FIXES (Safety Level: $safety_level)${NC}"
        echo "=================================================="

        # Apply fixes in order of safety level
        if [[ $safety_level -ge 1 ]]; then
            apply_emergency_fixes "$directory" "$preview"
        fi

        if [[ $safety_level -ge 2 ]]; then
            apply_surgical_fixes "$directory" "$preview"
        fi

        if [[ $safety_level -ge 3 ]]; then
            apply_moderate_fixes "$directory" "$preview"
        fi

        if [[ $safety_level -ge 4 ]]; then
            apply_conservative_fixes "$directory" "$preview"
        fi

        if [[ $safety_level -ge 5 ]]; then
            apply_cosmetic_fixes "$directory" "$preview"
        fi

        # Show rollback information
        if [[ -n "$checkpoint" ]]; then
            echo
            echo -e "${CYAN}🛡️  Safety checkpoint created: $checkpoint${NC}"
            echo -e "${CYAN}📝 To rollback: git stash pop ${checkpoint}${NC}"
        fi
    fi

    # Cleanup temp files
    rm -f "/tmp/error_analysis_${TIMESTAMP}."*

    log "INFO" "✅ Analysis complete"
}

# Execute main function
main "$@"
