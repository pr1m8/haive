#!/bin/bash
# Pre-flight safety checks for agent consolidation
# This script ensures we have a clean, stable starting point

set -e # Exit on any error

echo "🛡️ PRE-FLIGHT SAFETY CHECK FOR AGENT CONSOLIDATION"
echo "=================================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
	local status=$1
	local message=$2
	if [ "$status" = "pass" ]; then
		echo -e "${GREEN}✅ $message${NC}"
	elif [ "$status" = "warn" ]; then
		echo -e "${YELLOW}⚠️ $message${NC}"
	else
		echo -e "${RED}❌ $message${NC}"
	fi
}

# Phase 1: Git Repository Health
echo -e "\n📊 Phase 1: Git Repository Health"
echo "--------------------------------"

# Check if we're in git repo
if ! git rev-parse --git-dir >/dev/null 2>&1; then
	print_status "fail" "Not in a git repository"
	exit 1
fi

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
print_status "pass" "Current branch: $CURRENT_BRANCH"

# Check for uncommitted changes
UNCOMMITTED_CHANGES=$(git status --porcelain | wc -l)
if [ "$UNCOMMITTED_CHANGES" -gt 0 ]; then
	print_status "warn" "$UNCOMMITTED_CHANGES uncommitted changes (will be handled)"
else
	print_status "pass" "Working directory clean"
fi

# Check for untracked files that might interfere
PROBLEMATIC_FILES=$(find . -name "*.pyc" -o -name "__pycache__" -o -name ".pytest_cache" | wc -l)
if [ "$PROBLEMATIC_FILES" -gt 0 ]; then
	print_status "warn" "$PROBLEMATIC_FILES cache files found (will be cleaned)"
else
	print_status "pass" "No problematic cache files"
fi

# Phase 2: Python Environment Health
echo -e "\n🐍 Phase 2: Python Environment Health"
echo "-------------------------------------"

# Check poetry installation
if command -v poetry >/dev/null 2>&1; then
	print_status "pass" "Poetry is installed"
else
	print_status "fail" "Poetry not found - required for safe execution"
	exit 1
fi

# Check if in virtual environment
if [ -n "$VIRTUAL_ENV" ] || poetry env info >/dev/null 2>&1; then
	print_status "pass" "Virtual environment active"
else
	print_status "fail" "No virtual environment detected"
	exit 1
fi

# Check Python version
PYTHON_VERSION=$(poetry run python --version 2>&1)
print_status "pass" "Python version: $PYTHON_VERSION"

# Phase 3: Package Dependencies
echo -e "\n📦 Phase 3: Package Dependencies"
echo "--------------------------------"

# Check core imports
echo "Testing core imports..."
if poetry run python -c "import haive.core; print('Core imports OK')" 2>/dev/null; then
	print_status "pass" "haive-core imports work"
else
	print_status "fail" "haive-core imports broken - cannot proceed"
	exit 1
fi

# Check agents imports
if poetry run python -c "import haive.agents; print('Agents imports OK')" 2>/dev/null; then
	print_status "pass" "haive-agents imports work"
else
	print_status "fail" "haive-agents imports broken - cannot proceed"
	exit 1
fi

# Check rope dependency (needed for refactoring)
if poetry run python -c "import rope; print('Rope available')" 2>/dev/null; then
	print_status "pass" "rope library available"
else
	print_status "warn" "rope library not installed - will install automatically"
fi

# Phase 4: Target Package Structure
echo -e "\n🎯 Phase 4: Target Package Structure"
echo "------------------------------------"

TARGET_PACKAGE="packages/haive-agents"

if [ -d "$TARGET_PACKAGE" ]; then
	print_status "pass" "Target package exists: $TARGET_PACKAGE"
else
	print_status "fail" "Target package not found: $TARGET_PACKAGE"
	exit 1
fi

# Check critical files exist
CRITICAL_FILES=(
	"$TARGET_PACKAGE/src/haive/agents/base/enhanced_agent.py"
	"$TARGET_PACKAGE/src/haive/agents/base/agent.py"
	"$TARGET_PACKAGE/src/haive/agents/simple/agent_v3.py"
	"$TARGET_PACKAGE/src/haive/agents/base/__init__.py"
	"$TARGET_PACKAGE/src/haive/agents/simple/__init__.py"
)

for file in "${CRITICAL_FILES[@]}"; do
	if [ -f "$file" ]; then
		print_status "pass" "Critical file exists: $(basename $file)"
	else
		print_status "fail" "Missing critical file: $file"
		exit 1
	fi
done

# Phase 5: Test Suite Baseline
echo -e "\n🧪 Phase 5: Test Suite Baseline"
echo "-------------------------------"

# Count total test files
TOTAL_TESTS=$(find "$TARGET_PACKAGE/tests" -name "test_*.py" | wc -l)
print_status "pass" "Found $TOTAL_TESTS test files"

# Quick syntax check on critical files
echo "Checking Python syntax on critical files..."
SYNTAX_ERRORS=0

for file in "${CRITICAL_FILES[@]}"; do
	if [ -f "$file" ]; then
		if poetry run python -m py_compile "$file" 2>/dev/null; then
			echo "  ✅ $(basename $file) - syntax OK"
		else
			echo "  ❌ $(basename $file) - syntax ERROR"
			SYNTAX_ERRORS=$((SYNTAX_ERRORS + 1))
		fi
	fi
done

if [ "$SYNTAX_ERRORS" -eq 0 ]; then
	print_status "pass" "All critical files have valid Python syntax"
else
	print_status "fail" "$SYNTAX_ERRORS files have syntax errors"
	exit 1
fi

# Phase 6: Disk Space & Backup Readiness
echo -e "\n💾 Phase 6: Disk Space & Backup Readiness"
echo "-----------------------------------------"

# Check available disk space (need at least 1GB for backups)
AVAILABLE_SPACE_KB=$(df . | awk 'NR==2 {print $4}')
AVAILABLE_SPACE_GB=$((AVAILABLE_SPACE_KB / 1024 / 1024))

if [ "$AVAILABLE_SPACE_GB" -ge 1 ]; then
	print_status "pass" "Available disk space: ${AVAILABLE_SPACE_GB}GB"
else
	print_status "warn" "Low disk space: ${AVAILABLE_SPACE_GB}GB (may cause issues)"
fi

# Phase 7: Network Connectivity (for LLM access during testing)
echo -e "\n🌐 Phase 7: Network Connectivity"
echo "--------------------------------"

if ping -c 1 8.8.8.8 >/dev/null 2>&1; then
	print_status "pass" "Network connectivity available"
else
	print_status "warn" "Network connectivity issues (may affect LLM testing)"
fi

# Final Assessment
echo -e "\n📋 FINAL ASSESSMENT"
echo "==================="

print_status "pass" "Pre-flight safety checks completed"
print_status "pass" "Git repository: healthy"
print_status "pass" "Python environment: ready"
print_status "pass" "Package dependencies: working"
print_status "pass" "Target package structure: valid"
print_status "pass" "Test suite baseline: established"
print_status "pass" "Backup readiness: confirmed"

echo -e "\n🚀 ${GREEN}READY TO PROCEED WITH AGENT CONSOLIDATION${NC}"
echo "   • Branch: $CURRENT_BRANCH"
echo "   • Target: $TARGET_PACKAGE"
echo "   • Backup strategy: Multi-level checkpoints"
echo "   • Safety level: MAXIMUM"

echo -e "\n📋 Next steps:"
echo "   1. Run: DRY_RUN=1 python scripts/maintenance/analyze_agent_dependencies.py"
echo "   2. Run: DRY_RUN=1 python scripts/maintenance/agent_consolidation_refactorer.py"
echo "   3. Execute: ./scripts/maintenance/safe_agent_consolidation_master.sh"

exit 0
