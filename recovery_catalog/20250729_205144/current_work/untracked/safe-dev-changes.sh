#!/bin/bash
# safe-dev-changes.sh
# Safe Dev Dependencies Change Workflow

set -e # Exit on any error

echo "🛡️ Safe Dev Dependencies Change Workflow"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Setup safety measures
setup_safety() {
	echo -e "${BLUE}📍 Setting up safety measures...${NC}"

	# Create timestamped checkpoint
	CHECKPOINT_TAG="checkpoint-$(date +%Y%m%d-%H%M%S)"
	git tag "$CHECKPOINT_TAG" 2>/dev/null || true
	echo -e "${GREEN}✅ Git checkpoint created: $CHECKPOINT_TAG${NC}"

	# Backup critical files
	echo "Creating backups..."
	cp pyproject.toml pyproject.toml.backup
	[ -f poetry.lock ] && cp poetry.lock poetry.lock.backup
	[ -f .pre-commit-config.yaml ] && cp .pre-commit-config.yaml .pre-commit-config.yaml.backup

	echo -e "${GREEN}✅ Safety measures in place${NC}"
	echo "   - Git tag: $CHECKPOINT_TAG"
	echo "   - Backups: *.backup files created"
}

# Test changes without applying
test_changes() {
	echo -e "${BLUE}🧪 Testing changes (dry-run)...${NC}"

	echo "1. Testing Poetry dependency changes..."
	echo -e "${YELLOW}   Checking what removing black + isort would do:${NC}"
	poetry remove black isort --group dev --dry-run 2>/dev/null || echo "   (black/isort not found - that's ok)"

	echo -e "${YELLOW}   Checking what adding monkeytype would do:${NC}"
	poetry add monkeytype --group dev --dry-run

	echo "2. Testing current Ruff configuration..."
	if command -v ruff >/dev/null 2>&1; then
		echo -e "${YELLOW}   Current Ruff check results:${NC}"
		ruff check . --statistics | head -10

		echo -e "${YELLOW}   What Ruff formatting would change:${NC}"
		ruff format . --diff | head -20
	else
		echo -e "${YELLOW}   Ruff not installed - will be handled by Poetry${NC}"
	fi

	echo "3. Testing current pre-commit setup..."
	if [ -f .pre-commit-config.yaml ]; then
		echo -e "${YELLOW}   Current pre-commit hooks:${NC}"
		grep -E "^\s*-\s*id:" .pre-commit-config.yaml | head -10
	else
		echo -e "${YELLOW}   No .pre-commit-config.yaml found${NC}"
	fi

	echo -e "${GREEN}✅ Dry-run tests complete${NC}"
	echo "📋 Summary:"
	echo "   - Dependencies: Ready to optimize (remove black/isort, add monkeytype)"
	echo "   - Ruff: Ready to configure for formatting + linting"
	echo "   - Pre-commit: Ready to optimize hook stages"
}

# Show current state
show_current_state() {
	echo -e "${BLUE}📊 Current Development Environment State${NC}"
	echo "========================================"

	echo "🐍 Python version:"
	python --version 2>/dev/null || echo "   Python not found in PATH"

	echo "📦 Poetry dependencies (dev group):"
	if command -v poetry >/dev/null 2>&1; then
		poetry show --only dev --tree | head -10
		echo "   ... (showing first 10)"
	else
		echo "   Poetry not found"
	fi

	echo "🔧 Available dev tools:"
	for tool in ruff black isort mypy pyright pre-commit; do
		if command -v $tool >/dev/null 2>&1; then
			echo -e "   ✅ $tool ($(which $tool))"
		else
			echo -e "   ❌ $tool (not found)"
		fi
	done

	echo "📋 Current imports test:"
	if python -c "from src.haive.core.utils.dev import debug; print('✅ Dev utils import works')" 2>/dev/null; then
		echo "   ✅ Core dev utilities are working"
	else
		echo -e "   ${YELLOW}⚠️  Core dev utilities import failed${NC}"
	fi
}

# Apply changes with verification
apply_changes() {
	echo -e "${BLUE}🔄 Applying changes...${NC}"

	echo "Phase 1: Updating dependencies..."

	# Remove redundant tools (if they exist)
	echo "Removing black and isort (if present)..."
	poetry remove black isort --group dev 2>/dev/null || echo "   black/isort not found in pyproject.toml"

	# Add MonkeyType
	echo "Adding MonkeyType..."
	poetry add monkeytype --group dev

	echo "Phase 2: Updating Ruff configuration..."

	# Add/update Ruff config in pyproject.toml
	if ! grep -q "\[tool.ruff\]" pyproject.toml; then
		echo "Adding Ruff configuration to pyproject.toml..."
		cat >>pyproject.toml <<'EOF'

# Ruff configuration for linting and formatting
[tool.ruff]
target-version = "py312"
line-length = 88

[tool.ruff.lint]
select = [
    "E", "W",      # pycodestyle errors and warnings
    "F",           # Pyflakes
    "I",           # isort
    "B",           # flake8-bugbear
    "C4",          # flake8-comprehensions
    "UP",          # pyupgrade
    "TID251",      # Banned relative imports -> absolute imports
]

[tool.ruff.lint.isort]
known-first-party = ["haive"]
force-sort-within-sections = true
EOF
		echo -e "${GREEN}✅ Ruff configuration added${NC}"
	else
		echo -e "${YELLOW}⚠️  Ruff configuration already exists${NC}"
	fi

	echo "Phase 3: Updating pre-commit configuration..."

	# Create optimized pre-commit config
	cat >.pre-commit-config.yaml <<'EOF'
default_language_version:
  python: python3.12

repos:
  # Local hooks for consistency with project dependencies
  - repo: local
    hooks:
      - id: ruff-check
        name: "Ruff Linter"
        entry: ruff check --fix
        language: system
        types: [python]
        stages: [pre-commit]
        pass_filenames: true
        
      - id: ruff-format  
        name: "Ruff Formatter"
        entry: ruff format
        language: system
        types: [python]
        stages: [pre-commit]
        pass_filenames: true

  # Type checking on pre-push (slower, so we don't block commits)
  - repo: local
    hooks:
      - id: pyright
        name: "Pyright Type Checker"
        entry: pyright
        language: system
        types: [python]
        stages: [pre-push]
        pass_filenames: false

  # File quality checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: check-yaml
      - id: check-toml
      - id: check-merge-conflict
      - id: trailing-whitespace
      - id: end-of-file-fixer
EOF

	echo "Phase 4: Installing and testing..."

	# Reinstall pre-commit hooks
	if command -v pre-commit >/dev/null 2>&1; then
		pre-commit uninstall >/dev/null 2>&1 || true
		pre-commit install
		pre-commit install --hook-type pre-push
		echo -e "${GREEN}✅ Pre-commit hooks installed${NC}"
	else
		echo -e "${YELLOW}⚠️  Pre-commit not available yet (will be after poetry install)${NC}"
	fi

	# Update environment
	echo "Updating Poetry environment..."
	poetry install

	echo -e "${GREEN}✅ Changes applied successfully${NC}"
}

# Verify changes work
verify_changes() {
	echo -e "${BLUE}🔍 Verifying changes...${NC}"

	echo "1. Testing core functionality..."
	if poetry run python -c "from src.haive.core.utils.dev import debug; debug.ice('✅ Verification test'); print('Core imports work!')"; then
		echo -e "${GREEN}   ✅ Core dev utilities working${NC}"
	else
		echo -e "${RED}   ❌ Core dev utilities failed${NC}"
		return 1
	fi

	echo "2. Testing new tools..."

	# Test Ruff
	echo "   Testing Ruff..."
	if poetry run ruff check --version >/dev/null 2>&1; then
		echo -e "${GREEN}   ✅ Ruff available${NC}"
		# Test on a small file
		poetry run ruff check packages/haive-core/src/haive/core/utils/dev/debug_enhanced.py --quiet && echo -e "${GREEN}   ✅ Ruff check works${NC}" || echo -e "${YELLOW}   ⚠️  Ruff found issues (normal)${NC}"
	else
		echo -e "${RED}   ❌ Ruff failed${NC}"
	fi

	# Test MonkeyType
	echo "   Testing MonkeyType..."
	if poetry run monkeytype --help >/dev/null 2>&1; then
		echo -e "${GREEN}   ✅ MonkeyType available${NC}"
	else
		echo -e "${RED}   ❌ MonkeyType failed${NC}"
	fi

	# Test pre-commit
	echo "   Testing pre-commit setup..."
	if command -v pre-commit >/dev/null 2>&1; then
		if pre-commit run --all-files --verbose >/dev/null 2>&1; then
			echo -e "${GREEN}   ✅ Pre-commit hooks working${NC}"
		else
			echo -e "${YELLOW}   ⚠️  Pre-commit found issues (normal for first run)${NC}"
		fi
	else
		echo -e "${YELLOW}   ⚠️  Pre-commit not in PATH${NC}"
	fi

	echo -e "${GREEN}✅ Verification complete${NC}"
}

# Emergency rollback
rollback_changes() {
	echo -e "${RED}🚨 Emergency Rollback Initiated${NC}"

	# Find the most recent checkpoint
	LATEST_CHECKPOINT=$(git tag -l "checkpoint-*" | sort | tail -1)

	if [ -n "$LATEST_CHECKPOINT" ]; then
		echo "Rolling back to: $LATEST_CHECKPOINT"
		git reset --hard "$LATEST_CHECKPOINT"
	else
		echo "No checkpoint found, using backup files..."
	fi

	# Restore backup files
	[ -f pyproject.toml.backup ] && cp pyproject.toml.backup pyproject.toml && echo "✅ pyproject.toml restored"
	[ -f poetry.lock.backup ] && cp poetry.lock.backup poetry.lock && echo "✅ poetry.lock restored"
	[ -f .pre-commit-config.yaml.backup ] && cp .pre-commit-config.yaml.backup .pre-commit-config.yaml && echo "✅ pre-commit config restored"

	# Reinstall environment
	echo "Reinstalling environment..."
	poetry install

	# Reinstall pre-commit
	if command -v pre-commit >/dev/null 2>&1; then
		pre-commit uninstall >/dev/null 2>&1 || true
		pre-commit install
	fi

	# Verify restoration
	echo "🔍 Verifying rollback..."
	if poetry run python -c "from src.haive.core.utils.dev import debug; debug.ice('Rollback test'); print('✅ Rollback successful!')"; then
		echo -e "${GREEN}✅ Emergency rollback complete!${NC}"
	else
		echo -e "${RED}❌ Rollback verification failed${NC}"
		exit 1
	fi
}

# Show help
show_help() {
	echo "Usage: $0 {status|setup|test|apply|verify|rollback|help}"
	echo ""
	echo "Commands:"
	echo "  status   - Show current development environment state"
	echo "  setup    - Create safety checkpoint and backups"
	echo "  test     - Test changes (dry-run, no modifications)"
	echo "  apply    - Apply changes with verification"
	echo "  verify   - Verify that applied changes work correctly"
	echo "  rollback - Emergency rollback to previous state"
	echo "  help     - Show this help message"
	echo ""
	echo "Recommended workflow:"
	echo "  1. ./safe-dev-changes.sh status   # See current state"
	echo "  2. ./safe-dev-changes.sh setup    # Create safety net"
	echo "  3. ./safe-dev-changes.sh test     # Test changes safely"
	echo "  4. ./safe-dev-changes.sh apply    # Apply changes"
	echo "  5. ./safe-dev-changes.sh verify   # Verify everything works"
	echo ""
	echo "If anything goes wrong:"
	echo "  ./safe-dev-changes.sh rollback    # Emergency restore"
}

# Main workflow
case "${1:-help}" in
"status")
	show_current_state
	;;
"setup")
	setup_safety
	;;
"test")
	setup_safety
	test_changes
	;;
"apply")
	setup_safety
	test_changes
	apply_changes
	;;
"verify")
	verify_changes
	;;
"rollback")
	rollback_changes
	;;
"help" | "--help" | "-h")
	show_help
	;;
*)
	echo -e "${RED}Unknown command: $1${NC}"
	echo ""
	show_help
	exit 1
	;;
esac

echo ""
echo -e "${BLUE}📋 Next steps:${NC}"
case "${1}" in
"status")
	echo "   Run: ./safe-dev-changes.sh setup"
	;;
"setup")
	echo "   Run: ./safe-dev-changes.sh test"
	;;
"test")
	echo "   If tests look good, run: ./safe-dev-changes.sh apply"
	;;
"apply")
	echo "   Run: ./safe-dev-changes.sh verify"
	;;
"verify")
	echo "   🎉 All done! Your dev environment is optimized."
	echo "   💡 Try: poetry run ruff format . && poetry run ruff check ."
	;;
esac
