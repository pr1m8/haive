#!/bin/bash
# 🖨️ Enhanced Print Statement Eliminator - T201 Handler
# Usage: ./dev-tools/scripts/print-statement-eliminator.sh <directory> [--fix|--safe]

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

if [ ! -d "$DIRECTORY" ]; then
    echo -e "${RED}❌ Directory not found: $DIRECTORY${NC}"
    exit 1
fi

echo -e "${CYAN}🖨️ PRINT STATEMENT ELIMINATOR (T201 Handler)${NC}"
echo -e "${BLUE}Directory: $DIRECTORY${NC}"

# Safety checkpoint
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
git stash push -m "PRINT_ELIMINATION_CHECKPOINT_${TIMESTAMP}" || echo "⚠️ No changes to stash"

# Count T201 violations (print statements)
echo -e "${BLUE}🔍 Scanning for T201 violations (print statements)...${NC}"
T201_COUNT=$(poetry run ruff check "$DIRECTORY" --select T201 2>/dev/null | wc -l || echo "0")
echo -e "${YELLOW}🚨 Found $T201_COUNT print statements${NC}"

if [ "$T201_COUNT" -eq 0 ]; then
    echo -e "${GREEN}✅ No print statements found! Code is clean.${NC}"
    exit 0
fi

case $MODE in
    "--fix")
        echo -e "${GREEN}🔧 APPLYING RUFF AUTO-FIX (UNSAFE)...${NC}"
        echo -e "${YELLOW}⚠️  Warning: This uses unsafe fixes that might change semantics${NC}"
        
        # Use ruff to remove print statements
        poetry run ruff check "$DIRECTORY" --select T201 --fix --unsafe-fixes
        
        # Verify results
        FINAL_COUNT=$(poetry run ruff check "$DIRECTORY" --select T201 2>/dev/null | wc -l || echo "0")
        ELIMINATED=$((T201_COUNT - FINAL_COUNT))
        
        echo ""
        echo -e "${GREEN}🎉 RUFF T201 FIX RESULTS:${NC}"
        echo -e "${BLUE}📊 BEFORE: $T201_COUNT print statements${NC}"
        echo -e "${GREEN}✅ AFTER:  $FINAL_COUNT print statements${NC}"
        echo -e "${CYAN}🎯 ELIMINATED: $ELIMINATED print statements${NC}"
        ;;
        
    "--safe")
        echo -e "${GREEN}🛡️ APPLYING SAFE REMOVAL (remove-print-statements)...${NC}"
        
        # Install remove-print-statements if not available
        if ! command -v remove-print-statements >/dev/null 2>&1; then
            echo -e "${YELLOW}📦 Installing remove-print-statements...${NC}"
            pipx install remove-print-statements || pip install remove-print-statements
        fi
        
        # Apply safe removal
        remove-print-statements $(find "$DIRECTORY" -name "*.py")
        
        # Verify results
        FINAL_COUNT=$(poetry run ruff check "$DIRECTORY" --select T201 2>/dev/null | wc -l || echo "0")
        ELIMINATED=$((T201_COUNT - FINAL_COUNT))
        
        echo ""
        echo -e "${GREEN}🎉 SAFE REMOVAL RESULTS:${NC}"
        echo -e "${BLUE}📊 BEFORE: $T201_COUNT print statements${NC}"
        echo -e "${GREEN}✅ AFTER:  $FINAL_COUNT print statements${NC}"
        echo -e "${CYAN}🎯 ELIMINATED: $ELIMINATED print statements${NC}"
        ;;
        
    "--preview"|*)
        echo -e "${BLUE}🔍 PREVIEW MODE - Showing T201 violations...${NC}"
        poetry run ruff check "$DIRECTORY" --select T201
        
        echo ""
        echo -e "${GREEN}💡 REMOVAL OPTIONS:${NC}"
        echo -e "${YELLOW}🔧 Quick (unsafe): ${NC}./dev-tools/scripts/print-statement-eliminator.sh $DIRECTORY --fix"
        echo -e "${GREEN}🛡️ Safe:          ${NC}./dev-tools/scripts/print-statement-eliminator.sh $DIRECTORY --safe"
        echo ""
        echo -e "${BLUE}📋 TOOL COMPARISON:${NC}"
        echo "  🔧 --fix (ruff):  Fast, might change semantics (unsafe fixes)"
        echo "  🛡️ --safe:        Guaranteed safe removal, semantic preserving"
        ;;
esac

echo ""
echo -e "${GREEN}🎉 Print statement analysis complete!${NC}"
echo -e "${YELLOW}🔄 Rollback: git stash apply stash@{0} (if needed)${NC}"

# Add to pre-commit recommendation
if [ "$MODE" = "--safe" ] || [ "$MODE" = "--fix" ]; then
    echo ""
    echo -e "${CYAN}💡 PREVENT FUTURE T201 VIOLATIONS:${NC}"
    echo "Add to .pre-commit-config.yaml:"
    echo ""
    echo "  - repo: https://github.com/pre-commit/pre-commit-hooks"
    echo "    rev: v5.0.0"
    echo "    hooks:"
    echo "      - id: debug-statements"
    echo "        name: 'Block print() statements'"
    echo ""
    echo "  - repo: https://github.com/astral-sh/ruff-pre-commit"
    echo "    rev: v0.11.6"
    echo "    hooks:"
    echo "      - id: ruff"
    echo "        args: [--select, T201, --fix]"
fi 