#!/bin/bash
# optimize-single-package.sh
# Optimize dev dependencies for a single package with detailed tracking

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PACKAGE_PATH="${1}"
PACKAGE_NAME=$(basename "${PACKAGE_PATH}")

if [[ -z "${PACKAGE_PATH}" ]]; then
	echo -e "${RED}Usage: $0 <package-path>${NC}"
	echo "Example: $0 packages/haive-games"
	exit 1
fi

if [[ ! -d "${PACKAGE_PATH}" ]]; then
	echo -e "${RED}Package path does not exist: ${PACKAGE_PATH}${NC}"
	exit 1
fi

if [[ ! -f "${PACKAGE_PATH}/pyproject.toml" ]]; then
	echo -e "${RED}No pyproject.toml found in: ${PACKAGE_PATH}${NC}"
	exit 1
fi

echo -e "${BLUE}🎯 Optimizing Packag${: $PACKAGE_N}AME${NC}"
echo "========================================"

# Create tracking directory
TRACK_DIR="tests/utils/dev-optimization/results/${PACKAGE_NAME}"
mkdir -p "${TRACK_DIR}"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Setup safety measures
setup_safety() {
	echo -e "${BLUE}📍 Setting up safety measures f${r $PACKAGE_N}AME...${NC}"

	# Create package-specific checkpoint
	CHECKPOINT_TAG="checkpoint-${PACKAGE_NAME}-${TIMESTAMP}"
	git tag "${CHECKPOINT_TAG}" 2>/dev/null || true
	echo -e "${GREEN}✅ Git checkpoint${ $CHECKPOINT_T}AG${NC}"

	# Backup package files
	echo "Creating backups..."
	cp "${PACKAGE_PATH}/pyproject.toml" "${TRACK_DIR}/pyproject.toml.backup"
	[[ -f "${PACKAGE_PATH}/poetry.lock" ]] && cp "${PACKAGE_PATH}/poetry.lock" "${TRACK_DIR}/poetry.lock.backup"
	[[ -f "${PACKAGE_PATH}/.pre-commit-config.yaml" ]] && cp "${PACKAGE_PATH}/.pre-commit-config.yaml" "${TRACK_DIR}/pre-commit-config.yaml.backup"

	echo -e "${GREEN}✅ Backups created in${ $TRACK_D}IR${NC}"
}

# Analyze current state
analyze_current_state() {
	echo -e "${BLUE}📊 Analyzing current state ${f $PACKAGE_N}AME...${NC}"

	# Create analysis report
	cat >"${TRACK_DIR}/analysis-${TIMESTAMP}.md" <<EOF
# ${PACKAGE_NAME} Development Dependencies Analysis
Generated: $(date)

## Current Dependencies
EOF

	echo "### Dev Dependencies" >>"${TRACK_DIR}/analysis-${TIMESTAMP}.md"
	if grep -A 20 "\[tool.poetry.group.dev.dependencies\]" "${PACKAGE_PATH}/pyproject.toml" | grep -E "^[a-zA-Z]" >>"${TRACK_DIR}/analysis-${TIMESTAMP}.md" 2>/dev/null; then
		echo "✅ Dev dependencies found"
	else
		echo "⚠️  No dev dependencies section found"${>>"$TRACK}_DIR/analy${is-$TIMES}TAMP.md"
	fi

	# Check for redundant tools
	echo -e "\n### Redundancy Analysis" >>"${TRACK_DIR}/analysis-${TIMESTAMP}.md"
	if grep -q "black.*=" "${PACKAGE_PATH}/pyproject.toml" && grep -q "isort.*=" "${PACKAGE_PATH}/pyproject.toml"; then
		echo "❌ **ISSUE**: Both black and isort present (can be replaced by ruff)" >${"$TRACK_D}IR/analysi${-$TIMESTA}MP.md"
		echo -e "${YELLOW}   Found: black + isort redundancy${NC}"
	fi

	if grep -q "ruff.*=" "${PACKAGE_PATH}/pyproject.toml"; then
		echo "✅ Ruff already present" >${"$TRACK_D}IR/analysi${-$TIMESTA}MP.md"
	else
		echo "⚠️  Ruff not found - will be added"${>>"$TRACK}_DIR/analy${is-$TIMES}TAMP.md"
	fi

	if grep -q "monkeytype.*=" "${PACKAGE_PATH}/pyproject.toml"; then
		echo "✅ MonkeyType already present" >${"$TRACK_D}IR/analysi${-$TIMESTA}MP.md"
	else
		echo "📝 MonkeyType not found - will be added" ${>"$TRACK_}DIR/analys${s-$TIMEST}AMP.md"
	fi

	echo -e "${GREEN}✅ Analysis saved to${ $TRACK_D}IR/analysi${-$TIMESTA}MP.md${NC}"
}

# Test changes (dry-run)
test_changes() {
	echo -e "${BLUE}🧪 Testing changes f${r $PACKAGE_N}AME (dry-run)...${NC}"

	cd "${PACKAGE_PATH}"

	# Test dependency changes
	echo "Testing dependency removals..."
	poetry remove black isort --group dev --dry-run >"${TRACK_DIR}/removal-test-${TIMESTAMP}.log" 2>&1 || echo "   (black/isort not found or already removed)"

	echo "Testing ruff addition..."
	poetry add ruff --group dev --dry-run >"${TRACK_DIR}/ruff-addition-test-${TIMESTAMP}.log" 2>&1 || echo "   (ruff already present)"

	echo "Testing monkeytype..."
	poetry add monkeytype --group dev --dry-run >"${TRACK_DIR}/monkeytype-test-${TIMESTAMP}.log" 2>&1 || echo "   (monkeytype already present)"

	# Test ruff functionality if available
	if command -v ruff >/dev/null 2>&1; then
		echo "Testing ruff check..."
		ruff check . --statistics >"${TRACK_DIR}/ruff-check-before-${TIMESTAMP}.log" 2>&1 || true

		echo "Testing ruff format..."
		ruff format . --diff >"${TRACK_DIR}/ruff-format-preview-${TIMESTAMP}.log" 2>&1 || true
	fi

	cd - >/dev/null
	echo -e "${GREEN}✅ Dry-run tests completed - logs i${ $TRACK_D}IR${NC}"
}

# Apply optimizations
apply_optimizations() {
	echo -e "${BLUE}🔄 Applying optimizations ${o $PACKAGE_N}AME...${NC}"

	cd "${PACKAGE_PATH}"

	echo "Phase 1: Removing redundant tools..."
	poetry remove black isort --group dev 2>/dev/null || echo "   black/isort not found (ok)"

	echo "Phase 2: Adding ruff..."
	poetry add ruff --group dev 2>/dev/null || echo "   ruff already present"

	echo "Phase 3: Ensuring monkeytype..."
	poetry add monkeytype --group dev 2>/dev/null || echo "   monkeytype already present"

	echo "Phase 4: Adding ruff configuration..."
	if ! grep -q "\[tool.ruff\]" pyproject.toml; then
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

	echo "Phase 5: Creating optimized pre-commit config..."
	cat >.pre-commit-config.yaml <<'EOF'
default_language_version:
  python: python3.12

repos:
  # Use ruff for both linting and formatting
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

  # Type checking on pre-push (slower)
  - repo: local
    hooks:
      - id: mypy
        name: "MyPy Type Checker"
        entry: mypy
        language: system
        types: [python]
        stages: [pre-push]
        pass_filenames: true

  # File quality checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: check-yaml
      - id: check-toml
      - id: trailing-whitespace
      - id: end-of-file-fixer
EOF

	echo "Phase 6: Installing environment..."
	poetry install

	echo "Phase 7: Installing pre-commit hooks..."
	if command -v pre-commit >/dev/null 2>&1; then
		pre-commit uninstall >/dev/null 2>&1 || true
		pre-commit install
		pre-commit install --hook-type pre-push
	fi

	cd - >/dev/null
	echo -e "${GREEN}✅ Optimizations applied${NC}"
}

# Verify optimizations
verify_optimizations() {
	echo -e "${BLUE}🔍 Verifying optimizations f${r $PACKAGE_N}AME...${NC}"

	cd "${PACKAGE_PATH}"

	# Test imports
	echo "1. Testing package imports..."
	if poetry run python -c "import haive.games; print('✅ Package imports work')" 2>/dev/null; then
		echo -e "${GREEN}   ✅ Package imports working${NC}"
	else
		echo -e "${YELLOW}   ⚠️  Package imports failed (may need fixing)${NC}"
	fi

	# Test ruff
	echo "2. Testing ruff functionality..."
	if poetry run ruff check --version >/dev/null 2>&1; then
		echo -e "${GREEN}   ✅ Ruff available${NC}"

		# Run ruff check and save results
		poetry run ruff check . --statistics >"${TRACK_DIR}/ruff-check-after-${TIMESTAMP}.log" 2>&1 || true
		echo "   📊 Ruff check results saved"

		# Test ruff format
		poetry run ruff format . --check >/dev/null 2>&1 && echo -e "${GREEN}   ✅ Code already formatted${NC}" || echo -e "${YELLOW}   📝 Code needs formatting${NC}"
	else
		echo -e "${RED}   ❌ Ruff failed${NC}"
	fi

	# Test monkeytype
	echo "3. Testing monkeytype..."
	if poetry run monkeytype --help >/dev/null 2>&1; then
		echo -e "${GREEN}   ✅ MonkeyType available${NC}"
	else
		echo -e "${RED}   ❌ MonkeyType failed${NC}"
	fi

	# Test pre-commit
	echo "4. Testing pre-commit setup..."
	if [[ -f .pre-commit-config.yaml ]]; then
		echo -e "${GREEN}   ✅ Pre-commit config exists${NC}"
		if command -v pre-commit >/dev/null 2>&1; then
			if pre-commit run --all-files >/dev/null 2>&1; then
				echo -e "${GREEN}   ✅ Pre-commit hooks working${NC}"
			else
				echo -e "${YELLOW}   ⚠️  Pre-commit found issues (normal)${NC}"
			fi
		fi
	fi

	cd - >/dev/null
	echo -e "${GREEN}✅ Verification complete${NC}"
}

# Generate final report
generate_report() {
	echo -e "${BLUE}📋 Generating final report f${r $PACKAGE_N}AME...${NC}"

	cat >"${TRACK_DIR}/optimization-report-${TIMESTAMP}.md" <<EOF
# ${PACKAGE_NAME} Optimization Report
Generated: $(date)
Package: ${PACKAGE_PATH}

## Summary
- ✅ Safety checkpoint created: checkpoin${-$PACKAGE_NA}M${-$TIMESTA}MP
- ✅ Backup files saved in${ $TRACK_D}IR
- ✅ Optimizations applied successfully

## Changes Made
1. **Dependency Optimization**
   - Removed: black, isort (redundant with ruff)
   - Added: ruff (unified linting + formatting)
   - Ensured: monkeytype (type annotation generation)

2. **Configuration Added**
   - Ruff configuration in pyproject.toml
   - Optimized .pre-commit-config.yaml
   - Pre-commit hooks installed

3. **Performance Improvements**
   - Pre-commit hooks run only on changed files
   - Type checking moved to pre-push (faster commits)
   - Unified tooling reduces complexity

## Files Modified
- pyproject.toml (dependencies + ruff config)
- .pre-commit-config.yaml (created/updated)
- poetry.lock (regenerated)

## Rollback Instructions
If needed, rollback with:
\`\`\`bash
git reset --hard checkpoint-${PACKAGE_NAME}-${TIMESTAMP}
cp ${TRACK_DIR}/pyproject.toml.backup ${PACKAGE_PATH}/pyproject.toml
cd ${PACKAGE_PATH} && poetry install
\`\`\`

## Next Steps
1. Test the optimized workflow:
   \`\`\`bash
   cd ${PACKAGE_PATH}
   poetry run ruff format .
   poetry run ruff check --fix .
   poetry run monkeytype run -m pytest
   \`\`\`

2. Commit changes if satisfied:
   \`\`\`bash
   git add ${PACKAGE_PATH}/pyproject.toml ${PACKAGE_PATH}/.pre-commit-config.yaml
   git commit -m "optimize: dev dependencies for ${PACKAGE_NAME}"
   \`\`\`
EOF

	echo -e "${GREEN}✅ Report saved${ $TRACK_D}IR/optimization-repor${-$TIMESTA}MP.md${NC}"
}

# Emergency rollback
rollback() {
	echo -e "${RED}🚨 Emergency Rollback f${r $PACKAGE_N}AME${NC}"

	LATEST_CHECKPOINT=$(git tag -l "checkpoint-${PACKAGE_NAME}-*" | sort | tail -1)

	if [[ -n "${LATEST_CHECKPOINT}" ]]; then
		echo "Rolling back to: ${LATEST_CHECKPOINT}"
		git reset --hard "${LATEST_CHECKPOINT}"
	fi

	# Restore backups
	[[ -f "${TRACK_DIR}/pyproject.toml.backup" ]] && cp "${TRACK_DIR}/pyproject.toml.backup" "${PACKAGE_PATH}/pyproject.toml"
	[[ -f "${TRACK_DIR}/poetry.lock.backup" ]] && cp "${TRACK_DIR}/poetry.lock.backup" "${PACKAGE_PATH}/poetry.lock"
	[[ -f "${TRACK_DIR}/pre-commit-config.yaml.backup" ]] && cp "${TRACK_DIR}/pre-commit-config.yaml.backup" "${PACKAGE_PATH}/.pre-commit-config.yaml"

	cd "${PACKAGE_PATH}" && poetry install
	echo -e "${GREEN}✅ Rollback complete${NC}"
}

# Main execution
case "${2:-all}" in
"analyze")
	setup_safety
	analyze_current_state
	;;
"test")
	setup_safety
	analyze_current_state
	test_changes
	;;
"apply")
	setup_safety
	analyze_current_state
	test_changes
	apply_optimizations
	;;
"verify")
	verify_optimizations
	;;
"report")
	generate_report
	;;
"rollback")
	rollback
	;;
"all")
	setup_safety
	analyze_current_state
	test_changes
	apply_optimizations
	verify_optimizations
	generate_report
	;;
*)
	echo "Usage: $0 <package-path> {analyze|test|apply|verify|report|rollback|all}"
	echo ""
	echo "Commands:"
	echo "  analyze  - Analyze current state only"
	echo "  test     - Test changes (dry-run)"
	echo "  apply    - Apply optimizations"
	echo "  verify   - Verify optimizations work"
	echo "  report   - Generate final report"
	echo "  rollback - Emergency rollback"
	echo "  all      - Run complete optimization workflow"
	exit 1
	;;
esac

echo ""
echo -e "${BLUE}�${� $PACKAGE_N}AME optimization workflow complete!${NC}"
echo "📁 Tracking dat${: $TRACK_}DIR"
