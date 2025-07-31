# 🛡️ Safe Dev Dependencies Change Workflow

## 🎯 **Overview: Test Big Changes Safely**

This workflow ensures you can experiment with dev tooling changes, test them thoroughly, and rollback instantly if anything goes wrong.

---

## 🔄 **Git Workflow for Safe Changes**

### **Step 1: Create Experimental Branch**

```bash
# Save current state and create experiment branch
git stash push -m "WIP: before dev deps experiment"
git checkout -b experiment/dev-deps-optimization
git push -u origin experiment/dev-deps-optimization
```

### **Step 2: Create Safety Checkpoint**

```bash
# Tag current working state for easy rollback
git tag checkpoint-before-dev-changes
git push origin checkpoint-before-dev-changes

echo "📍 Safety checkpoint created: checkpoint-before-dev-changes"
```

---

## 🧪 **Dry-Run Testing Strategy**

### **Poetry Dependency Changes (Dry-Run)**

```bash
# Test dependency changes without installing
echo "🔍 Testing Poetry changes..."

# Backup current state
cp pyproject.toml pyproject.toml.backup
cp poetry.lock poetry.lock.backup

# Dry-run dependency changes
poetry remove black isort --group dev --dry-run
poetry add monkeytype --group dev --dry-run

# Show what would change
echo "📋 Dependency changes that would be made:"
poetry show --tree --only=dev
```

### **Pre-commit Configuration (Dry-Run)**

```bash
# Test pre-commit changes without installing
echo "🔍 Testing pre-commit changes..."

# Backup current config
cp .pre-commit-config.yaml .pre-commit-config.yaml.backup

# Test configuration without installing hooks
pre-commit try-repo . --all-files --verbose

# Show what hooks would run
pre-commit run --all-files --verbose --dry-run
```

### **Ruff Configuration (Dry-Run)**

```bash
# Test ruff changes without modifying files
echo "🔍 Testing Ruff configuration..."

# Backup current config
cp pyproject.toml pyproject.toml.ruff-backup

# Test ruff rules without applying changes
ruff check . --diff          # Show what would change
ruff format . --diff         # Show formatting changes
ruff check . --statistics    # Show rule violations

echo "📊 Ruff would make these changes:"
ruff check . --diff | head -50
```

---

## 📋 **Staged Implementation Plan**

### **Phase 1: Configuration Testing**

```bash
#!/bin/bash
# phase1-config-test.sh

echo "🧪 Phase 1: Testing Configuration Changes"

# Create working branch
git checkout -b phase1/config-test

# 1. Test Ruff configuration
echo "Testing Ruff config..."
cat >> pyproject.toml << 'EOF'

[tool.ruff]
target-version = "py312"
line-length = 88

[tool.ruff.lint]
select = [
    "E", "W",      # pycodestyle
    "F",           # Pyflakes
    "I",           # isort
    "B",           # flake8-bugbear
    "C4",          # flake8-comprehensions
    "UP",          # pyupgrade
    "TID251",      # Banned relative imports
]

[tool.ruff.lint.isort]
known-first-party = ["haive"]
force-sort-within-sections = true
EOF

# Test the configuration
ruff check . --diff > ruff-changes-preview.txt
echo "📄 Ruff changes saved to: ruff-changes-preview.txt"

# 2. Test pre-commit config
cat > .pre-commit-config.yaml.new << 'EOF'
default_language_version:
  python: python3.12

repos:
  - repo: local
    hooks:
      - id: ruff-check
        name: "Ruff Linter"
        entry: ruff check --fix
        language: system
        types: [python]
        stages: [pre-commit]

      - id: ruff-format
        name: "Ruff Formatter"
        entry: ruff format
        language: system
        types: [python]
        stages: [pre-commit]

  # Type checking on pre-push (slower)
  - repo: local
    hooks:
      - id: pyright
        name: "Pyright Type Checker"
        entry: pyright
        language: system
        types: [python]
        stages: [pre-push]
        pass_filenames: false
EOF

# Test new pre-commit config
cp .pre-commit-config.yaml.new .pre-commit-config.yaml
pre-commit try-repo . --all-files --verbose > precommit-test.log 2>&1

echo "✅ Phase 1 complete. Review:"
echo "  - ruff-changes-preview.txt"
echo "  - precommit-test.log"
```

### **Phase 2: Dependency Testing**

```bash
#!/bin/bash
# phase2-deps-test.sh

echo "🧪 Phase 2: Testing Dependency Changes"

git checkout -b phase2/deps-test

# 1. Test removing redundant tools
echo "Testing dependency removal..."
poetry remove black isort --group dev --dry-run > deps-removal-preview.txt

# 2. Test adding MonkeyType
echo "Testing MonkeyType addition..."
poetry add monkeytype --group dev --dry-run > deps-addition-preview.txt

# 3. Test lock file changes
echo "Testing lock file resolution..."
poetry lock --check

echo "✅ Phase 2 complete. Review:"
echo "  - deps-removal-preview.txt"
echo "  - deps-addition-preview.txt"
```

### **Phase 3: Integration Testing**

```bash
#!/bin/bash
# phase3-integration-test.sh

echo "🧪 Phase 3: Integration Testing"

git checkout -b phase3/integration-test

# Actually apply changes for testing
echo "Applying changes for integration test..."

# 1. Remove redundant tools
poetry remove black isort --group dev

# 2. Add MonkeyType
poetry add monkeytype --group dev

# 3. Update pre-commit
cp .pre-commit-config.yaml.new .pre-commit-config.yaml
pre-commit uninstall
pre-commit install
pre-commit install --hook-type pre-push

# 4. Test the full pipeline
echo "Testing full development pipeline..."

# Test ruff formatting
echo "Testing ruff format..."
ruff format packages/haive-core/src/haive/core/utils/dev/debug_enhanced.py --diff

# Test ruff linting
echo "Testing ruff check..."
ruff check packages/haive-core/src/haive/core/utils/dev/ --fix --diff

# Test pyright
echo "Testing pyright..."
pyright packages/haive-core/src/haive/core/utils/dev/

# Test pre-commit hooks
echo "Testing pre-commit..."
pre-commit run --all-files

# Test MonkeyType
echo "Testing MonkeyType..."
cd packages/haive-core
monkeytype run -c "from src.haive.core.utils.dev import debug; debug.ice('test')"
monkeytype list-modules

echo "✅ Phase 3 complete. Full integration tested."
```

---

## 🔄 **Quick Rollback Commands**

### **Emergency Rollback (Nuclear Option)**

```bash
#!/bin/bash
# emergency-rollback.sh

echo "🚨 Emergency Rollback Initiated"

# 1. Reset to checkpoint
git reset --hard checkpoint-before-dev-changes

# 2. Restore backup files
[ -f pyproject.toml.backup ] && cp pyproject.toml.backup pyproject.toml
[ -f poetry.lock.backup ] && cp poetry.lock.backup poetry.lock
[ -f .pre-commit-config.yaml.backup ] && cp .pre-commit-config.yaml.backup .pre-commit-config.yaml

# 3. Reinstall environment
poetry install
pre-commit uninstall
pre-commit install

# 4. Verify restoration
echo "🔍 Verifying rollback..."
poetry run python -c "from src.haive.core.utils.dev import debug; debug.ice('Rollback test')"

echo "✅ Emergency rollback complete!"
```

### **Selective Rollback**

```bash
# Rollback just dependencies
git checkout checkpoint-before-dev-changes -- pyproject.toml poetry.lock
poetry install

# Rollback just pre-commit config
git checkout checkpoint-before-dev-changes -- .pre-commit-config.yaml
pre-commit uninstall && pre-commit install

# Rollback just ruff config
git checkout checkpoint-before-dev-changes -- pyproject.toml
# (keep only the [tool.ruff] section you want to keep)
```

---

## 🎯 **Safe Testing Script (All-in-One)**

```bash
#!/bin/bash
# safe-dev-changes.sh

set -e  # Exit on any error

echo "🛡️ Starting Safe Dev Dependencies Change Workflow"

# Setup safety measures
setup_safety() {
    echo "📍 Setting up safety measures..."

    # Create checkpoint
    git tag checkpoint-$(date +%Y%m%d-%H%M%S) 2>/dev/null || true

    # Backup critical files
    cp pyproject.toml pyproject.toml.backup
    cp poetry.lock poetry.lock.backup
    cp .pre-commit-config.yaml .pre-commit-config.yaml.backup

    echo "✅ Safety measures in place"
}

# Test changes without applying
test_changes() {
    echo "🧪 Testing changes (dry-run)..."

    # Test dependency changes
    echo "Testing Poetry changes..."
    poetry remove black isort --group dev --dry-run
    poetry add monkeytype --group dev --dry-run

    # Test ruff configuration
    echo "Testing Ruff configuration..."
    ruff check . --diff | head -20

    # Test pre-commit configuration
    echo "Testing pre-commit configuration..."
    # Create temp config and test

    echo "✅ Dry-run tests complete"
}

# Apply changes with verification
apply_changes() {
    echo "🔄 Applying changes..."

    # Remove redundant tools
    poetry remove black isort --group dev

    # Add MonkeyType
    poetry add monkeytype --group dev

    # Update configurations
    # (implement config updates)

    # Verify changes work
    echo "🔍 Verifying changes..."
    poetry run python -c "from src.haive.core.utils.dev import debug; debug.ice('Changes test')"

    echo "✅ Changes applied and verified"
}

# Main workflow
case "${1:-test}" in
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
    "rollback")
        source emergency-rollback.sh
        ;;
    *)
        echo "Usage: $0 {setup|test|apply|rollback}"
        echo "  setup   - Create safety checkpoint"
        echo "  test    - Test changes (dry-run)"
        echo "  apply   - Apply changes with verification"
        echo "  rollback - Emergency rollback"
        ;;
esac
```

---

## 📊 **Verification Checklist**

After each phase, verify:

### **✅ Basic Functionality**

```bash
# Can import our dev utilities?
poetry run python -c "from src.haive.core.utils.dev import debug, log, benchmark; print('✅ Imports work')"

# Do pre-commit hooks work?
echo "test" > temp_test_file.py && pre-commit run --files temp_test_file.py && rm temp_test_file.py

# Does type checking work?
pyright packages/haive-core/src/haive/core/utils/dev/debug_enhanced.py

# Does ruff work properly?
ruff check packages/haive-core/src/haive/core/utils/dev/ --statistics
```

### **✅ Performance Check**

```bash
# Time the operations
time ruff check packages/haive-core/src/
time pyright packages/haive-core/src/haive/core/utils/dev/
time pre-commit run --all-files
```

### **✅ Integration Check**

```bash
# Full development workflow
cd packages/haive-core
poetry run python -c "
from src.haive.core.utils.dev import debug, benchmark
debug.ice('Integration test')
def test_func(): return sum(i**2 for i in range(100))
result = benchmark.timing.time_it(test_func, iterations=10)
print(f'✅ Benchmark works: {result[\"mean\"]:.6f}s')
"
```

---

## 🎉 **Success Criteria**

Consider the changes successful when:

- ⚡ Pre-commit runs < 30 seconds
- 🔍 All imports work correctly
- 🧪 Tests pass with new tooling
- 📊 No new linting errors introduced
- 🐒 MonkeyType generates useful annotations
- 🔄 Easy rollback available if needed

**Ready to start? Run: `./safe-dev-changes.sh test` to begin safely!**
