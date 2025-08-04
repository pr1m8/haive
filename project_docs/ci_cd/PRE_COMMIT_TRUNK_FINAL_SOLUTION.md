# Pre-commit & Trunk Final Solution

**Document Version**: 5.0
**Date**: 2025-01-31
**Status**: ✅ FINAL SOLUTION - Separate Tools Approach
**Issue Resolution**: Resolved core.hooksPath conflict without integration problems

## 🎯 Executive Summary

**Problem**: Using trunk.io and pre-commit together causes `core.hooksPath` conflicts.
**Solution**: Use both tools separately - trunk for automatic git hooks, pre-commit for manual comprehensive checks.
**Result**: No conflicts, fast daily workflow, comprehensive checks available on demand.

## ⚠️ What We Learned (The Hard Way)

**Attempted Solution**: Custom trunk linter to run pre-commit through trunk
**Result**: DISASTER - Cache pollution, endless file changes, performance issues
**Lesson**: Don't try to force integration between incompatible hook managers

## ✅ FINAL WORKING SOLUTION

### 1. Trunk (Primary - Automatic Git Hooks)

**Configuration**: `.trunk/trunk.yaml`

```yaml
lint:
  enabled:
    - actionlint@1.7.7 # GitHub Actions linting
    - bandit@1.8.6 # Security scanning
    - black@25.1.0 # Code formatting
    - checkov@3.2.451 # Infrastructure security
    - git-diff-check # Git whitespace check
    - isort@6.0.1 # Import sorting
    - markdownlint@0.45.0 # Markdown linting
    - mypy@1.17.0 # Type checking
    - prettier@3.6.2 # JSON/YAML formatting
    - ruff@0.12.3 # Python linting
    - shellcheck@0.10.0 # Shell script linting
    - trufflehog@3.90.0 # Secret scanning
    - yamllint@1.37.1 # YAML linting

actions:
  enabled:
    - trunk-check-pre-push # Run checks before push
    - trunk-fmt-pre-commit # Format files on commit
    - trunk-check-pre-commit # Essential checks on commit
    - haive-import-validation # Custom Haive import checks
    - haive-memory-integrity # Custom Haive memory checks
```

**Git Configuration**:

```bash
# Trunk manages git hooks automatically
git config core.hooksPath /home/will/.cache/trunk/repos/.../git-hooks
```

**Daily Usage**:

```bash
git add file.py
git commit -m "feat: new feature"
# Trunk runs automatically: ✓ format ✓ lint ✓ type-check ✓ security
```

### 2. Pre-commit (Secondary - Manual Comprehensive Checks)

**Configuration**: `.pre-commit-config.yaml` (40+ hooks available)

- Comprehensive formatting (ruff, docformatter, add-trailing-comma)
- Security scanning (bandit, advanced checks)
- Documentation quality (interrogate, darglint, sphinx-lint)
- Code quality (multiple linters, dead code detection)
- Advanced type checking and import management

**Manual Usage**:

```bash
# Full comprehensive check when needed
poetry run pre-commit run --all-files

# Specific hook categories
poetry run pre-commit run docstring-coverage
poetry run pre-commit run security-check
poetry run pre-commit run import-quality

# DON'T install hooks (avoids core.hooksPath conflict)
# poetry run pre-commit install  # ❌ DON'T DO THIS
```

## 🚀 Benefits Achieved

### Technical Benefits

1. **✅ No core.hooksPath conflicts** - Each tool manages its own hooks
2. **✅ Fast daily workflow** - Trunk's essential checks run in ~5-10 seconds
3. **✅ Comprehensive on-demand** - Full 40+ hook suite available manually
4. **✅ No cache pollution** - Pre-commit runs in isolation, no workspace contamination
5. **✅ No endless file changes** - Controlled execution prevents modification loops

### Workflow Benefits

1. **✅ Best of both worlds** - Speed for daily work, thoroughness when needed
2. **✅ Zero installation friction** - Trunk works immediately, pre-commit available
3. **✅ Team consistency** - Trunk ensures automatic baseline quality
4. **✅ Flexibility** - Developers can run comprehensive checks before releases

## 📊 Performance Comparison

| Tool           | Speed     | Scope             | When Used    | File Changes     |
| -------------- | --------- | ----------------- | ------------ | ---------------- |
| **Trunk**      | ⚡ 5-10s  | Essential checks  | Every commit | Targeted         |
| **Pre-commit** | 🐌 30-60s | 40+ comprehensive | On demand    | Can be extensive |

## 🚨 What NOT to Do

**❌ Never attempt Option 3 (Custom Trunk Linter)**:

```bash
# This causes disasters:
trunk check --filter=pre-commit-custom --all-files
```

**Problems it causes**:

- Pre-commit cache downloads external repos into your workspace
- Endless file modification loops
- Severe performance degradation
- Repository contamination

## 🎯 Usage Guidelines

### Daily Development

```bash
# Normal workflow - trunk handles everything automatically
git add .
git commit -m "feat: implement feature"
git push
```

### Before Important Releases

```bash
# Run comprehensive checks manually
poetry run pre-commit run --all-files

# Fix any issues found
git add .
git commit -m "chore: comprehensive quality fixes"
```

### Debugging Hook Issues

```bash
# Check trunk status
trunk --version
trunk check --help

# Test pre-commit manually
poetry run pre-commit run specific-hook --files file.py

# Check git hook configuration
git config core.hooksPath
```

## 🎉 Conclusion

This **separate tools approach** successfully resolves the core.hooksPath conflict while providing:

1. **Daily productivity** - Fast, automatic essential checks via trunk
2. **Comprehensive quality** - Full validation suite available via pre-commit
3. **Zero conflicts** - Each tool operates independently
4. **Clean workspace** - No cache pollution or file contamination
5. **Team scalability** - Works for all team members without installation issues

The key insight: **Don't force integration between incompatible systems**. Instead, use each tool for its strengths and let them coexist peacefully.

---

**Status**: ✅ **Production Ready and Battle Tested**
**Last Updated**: 2025-01-31
**Disaster Lessons**: Learned from failed Option 3 implementation
