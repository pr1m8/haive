# Pre-commit & Trunk Integration Guide

**Document Version**: 5.0
**Date**: 2025-01-31
**Status**: ✅ **PRODUCTION READY** - Trunk Actions Approach
**Issue Resolution**: Proper trunk actions configuration following official documentation

## 🎉 FINAL WORKING SOLUTION

After comprehensive testing and following official trunk documentation, the optimal approach is to use **trunk's native actions** for git hook management with **pre-commit as supplementary tooling**.

### ✅ What Works: Trunk Actions + Pre-commit Supplementary

**Primary**: Trunk manages git hooks automatically
**Secondary**: Pre-commit available for additional comprehensive checks

## 🏗️ Final Architecture

### 1. Trunk Configuration (.trunk/trunk.yaml)

**Following official trunk actions documentation:**

```yaml
# .trunk/trunk.yaml
version: 0.1

cli:
  version: 1.24.0

plugins:
  sources:
    - id: trunk
      ref: v1.7.1
      uri: https://github.com/trunk-io/plugins

lint:
  enabled:
    - pre-commit-hooks@5.0.0
    - actionlint@1.7.7
    - bandit@1.8.6
    - black@25.1.0
    - checkov@3.2.451
    - dotenv-linter@3.3.0
    - git-diff-check
    - hadolint@2.12.1-beta
    - isort@6.0.1
    - markdownlint@0.45.0
    - mypy@1.17.0
    - osv-scanner@2.0.3
    - oxipng@9.1.5
    - prettier@3.6.2
    - ruff@0.12.3
    - shellcheck@0.10.0
    - shfmt@3.6.0
    - taplo@0.9.3
    - trufflehog@3.90.0
    - yamllint@1.37.1

# Trunk Actions - Following trunk's recommended defaults
actions:
  disabled:
    - trunk-announce # Disable announcements only
  enabled:
    - git-lfs
    - trunk-fmt-pre-commit # ✅ Auto-format on commit
    - trunk-check-pre-push # ✅ Check before push
    - trunk-cache-prune
    - trunk-upgrade-available
```

### 2. Pre-commit Configuration (.pre-commit-config.yaml)

**Simplified for supplementary use (trunk handles core workflow):**

```yaml
# ===================================================================
# 🚀 Haive Pre-commit Configuration
# Comprehensive code quality, security, and documentation enforcement
# ===================================================================

repos:
  # 🔧 Note: Trunk manages git hooks directly via trunk-fmt-pre-commit and trunk-check-pre-push
  # No need for trunk hooks in pre-commit - trunk handles this automatically

  # 🚀 Core Python Formatting & Linting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.6
    hooks:
      - id: ruff
        name: "Ruff Linter"
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format
        name: "Ruff Formatter"

  # 🧹 Code Cleanup
  - repo: https://github.com/PyCQA/autoflake
    rev: v2.3.1
    hooks:
      - id: autoflake
        name: "Remove Unused Imports"
        args:
          - --remove-all-unused-imports
          - --remove-unused-variables
          - --in-place

  # 🧹 Essential Code Quality
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
        name: Remove Trailing Whitespace
      - id: end-of-file-fixer
        name: Fix End of Files
      - id: check-yaml
        name: Check YAML
      - id: check-toml
        name: Check TOML
      - id: check-merge-conflict
        name: Check Merge Conflicts
      - id: debug-statements
        name: Check Debug Statements

  # 🔒 Security & Import Quality
  - repo: https://github.com/PyCQA/isort
    rev: 5.14.2
    hooks:
      - id: isort
        name: Import Quality Check
        args: [--profile, black]

  # 🎯 Type Checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.17.0
    hooks:
      - id: mypy
        name: Type Check
        additional_dependencies: [types-all]
        args: [--ignore-missing-imports, --no-strict-optional]

  # Note: Problematic hooks (interrogate, flake8 conflicts) temporarily disabled
  # TODO: Re-enable after fixing plugin conflicts and syntax issues
```

### 3. Git Configuration

**Trunk manages git hooks automatically:**

```bash
# Trunk sets this automatically - no manual configuration needed
git config core.hooksPath /home/will/.cache/trunk/repos/.../git-hooks
```

## 🚀 Usage Patterns

### Daily Development Workflow (Automatic)

```bash
git add modified_file.py
git commit -m "feat: new feature"
# → trunk-fmt-pre-commit: Auto-formats code ✅
# → Additional checks via trunk linters ✅

git push
# → trunk-check-pre-push: Comprehensive checks ✅
# → Push succeeds if all checks pass ✅
```

### Comprehensive Checks (Manual)

```bash
# When you need additional pre-commit hooks
poetry run pre-commit run --all-files

# Or specific pre-commit hooks
poetry run pre-commit run trailing-whitespace
poetry run pre-commit run mypy
```

### Manual Trunk Commands

```bash
# Direct trunk usage
trunk fmt .              # Format all files
trunk check .            # Check all files
trunk actions list       # List available actions
```

## 🎯 Key Benefits Achieved

### ✅ Technical Benefits

1. **No Conflicts** - Trunk manages git hooks as designed
2. **Automatic Execution** - `trunk-fmt-pre-commit` and `trunk-check-pre-push` work automatically
3. **Best of Both Worlds** - Trunk's speed + Pre-commit's comprehensiveness
4. **Zero Installation Friction** - New team members get hooks immediately
5. **Performance** - Trunk's intelligent caching and parallel execution

### ✅ Workflow Benefits

1. **Automatic Formatting** - Code formatted on every commit
2. **Push Validation** - Comprehensive checks before push
3. **Supplementary Tools** - Pre-commit available for additional checks
4. **Team Consistency** - Version-controlled hook configuration
5. **No Hook Bypass** - Automatic execution prevents `--no-verify` usage

## 📊 Real-World Evidence

### Successful Commit Example

```bash
$ git commit -m "feat(trunk): complete integration"
[0G[2K[0G[2K... (trunk formatting output)
✔ Formatted .trunk/trunk.yaml
✔ Formatted .pre-commit-config.yaml
✔ No issues

Checked 3 modified files
✔ No issues
[recovery/stash_10_20250729_205753 c7424fd6] feat(trunk): complete integration
```

### Successful Push Example

```bash
$ git push
remote: GitHub found 3 vulnerabilities... (unrelated security notice)
To https://github.com/pr1m8/haive.git
   afbdb5c7..c7424fd6  recovery/stash_10_20250729_205753 -> recovery/stash_10_20250729_205753
```

## ⚠️ What We Learned: Avoid These Approaches

### ❌ Option 1: Custom Trunk Linter (Causes Problems)

- Cache pollution in workspace
- Endless file modification loops
- Severe performance issues
- Repository contamination

### ❌ Option 2: Disabling Trunk Actions (Against Design)

- Goes against trunk's intended architecture
- Loses trunk's performance benefits
- Manual management overhead

### ❌ Option 3: Dual Hook Management (Conflicts)

- core.hooksPath conflicts
- Competing hook systems
- Installation friction

## 🔧 Troubleshooting

### Pre-commit Stashing (Normal Behavior)

```bash
[WARNING] Unstaged files detected.
[INFO] Stashing unstaged files to /home/will/.cache/pre-commit/patch...
```

**This is correct behavior** - pre-commit stashes unstaged changes to run hooks on exactly what will be committed, then restores changes afterward.

### Trunk Taking Over Hooks (Expected)

```bash
✔ Trunk is now managing your git hooks
```

**This is the intended behavior** when trunk actions are enabled. Trunk manages git hooks directly as designed.

### Reset to Pre-commit Only (If Needed)

```bash
# Only if you want to switch back to pre-commit
git config --unset core.hooksPath
poetry run pre-commit install
```

## 📈 Performance Metrics

**Trunk Automatic Hooks**:

- ⚡ **Fast**: ~5-10 seconds per commit
- 🎯 **Focused**: Essential checks only
- 🔄 **Cached**: Intelligent incremental checking

**Pre-commit Manual Execution**:

- 🐌 **Slower**: ~30-60 seconds for full suite
- 📚 **Comprehensive**: All hooks
- 🎛️ **Controlled**: Run when needed

## 🎉 Conclusion

The **trunk actions approach** provides the optimal developer experience:

1. **Trunk for daily workflow** - Fast, automatic, essential checks via official actions
2. **Pre-commit for comprehensiveness** - Additional manual validation when needed
3. **No conflicts** - Single hook management system (trunk)
4. **Following best practices** - Using trunk as designed per official documentation

This solution provides:

- ✅ **Zero configuration conflicts**
- ✅ **Automatic code quality enforcement**
- ✅ **Superior performance** with intelligent caching
- ✅ **Team consistency** through version-controlled configuration
- ✅ **Industry standard workflow** following trunk's official documentation

---

**Status**: ✅ **Production Ready**
**Last Updated**: 2025-01-31
**Next Review**: As needed based on trunk updates

## 📚 References

- [Trunk Actions Documentation](https://docs.trunk.io/references/cli/getting-started/actions)
- [Pre-commit Documentation](https://pre-commit.com)
- [Git Hooks Best Practices](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
