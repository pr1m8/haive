# Git Workflow - Haive Framework

**Version**: 1.0  
**Purpose**: Git best practices and workflow standards  
**Last Updated**: 2025-01-09

## 🚨 Mandatory Git Safety Protocol

### Before ANY Work

```bash
# ALWAYS run these FIRST before any work
git status                              # See current state
git diff                               # See unstaged changes
git diff --cached                      # See staged changes
git log --oneline -5                   # Recent commit history
git branch -v                          # Current branch info

# SAFETY BACKUP before major changes
git stash push -m "Safety backup before work"

# NEVER work without knowing current state
# NEVER commit without reviewing changes first
# NEVER push without testing locally
```

## 🔄 Standard Git Workflow

### 1. Start New Work

```bash
# Update from remote (if collaborative)
git fetch origin
git status                             # Check for conflicts

# Create proper branch
git checkout -b feature/description
# or
git checkout -b fix/issue-description
```

### 2. Work Incrementally

```bash
# Stage specific files (never use git add .)
git add specific_files.py
git status                             # Always check what's staged

# Commit with meaningful messages
git commit -m "feat(component): specific change with context"
```

### 3. Pre-commit Checks

```bash
# MANDATORY before committing
poetry run pytest                      # All tests pass
poetry run ruff check                  # Code style
poetry run mypy                        # Type checking

# Verify imports work
poetry run python -c "from haive.core import *; print('Imports OK')"
```

### 4. Final Verification

```bash
# Review changes before push
git log --oneline -3                   # Review recent commits
git diff origin/main...HEAD            # See all changes since main

# Push with upstream tracking
git push -u origin feature/description
```

## 📝 Commit Message Standards

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```bash
# ✅ CORRECT - Detailed commit with context
git commit -m "feat(haive-core): add enhanced tool management with validation

- Added tool validation in ReactAgent
- Implemented state history saving
- Updated imports to use BaseGraph
- All tests pass with real components

Ref: [MEM-004-CORE-G-001] ReactAgent Enhancement
Fixes: Import errors from missing DynamicGraph"

# ✅ CORRECT - Bug fix with clear description
git commit -m "fix(haive-mcp): resolve uvicorn dependency conflict

- Updated uvicorn version to ^0.34.0 in pyproject.toml
- Regenerated poetry.lock
- All packages now install cleanly

Ref: [MEM-006-A] Git Workflow Standards"

# ✅ CORRECT - Documentation update
git commit -m "docs(memory): update methodology with git standards

- Added numbered memory tagging system
- Enhanced no-mocks testing enforcement
- Added git safety protocols
- Updated cross-reference format

Ref: [MEM-002-B] Memory Methodology v2.0"
```

### Anti-patterns

```bash
# ❌ WRONG - Vague, unclear commits
git commit -m "fix stuff"              # No context
git commit -m "update"                 # What was updated?
git commit -m "wip"                    # Work in progress is not ready
git commit -m "temp"                   # Temporary commits pollute history
```

## 🌿 Branch Naming Standards

### Naming Convention

```bash
# ✅ CORRECT - Descriptive with memory references
feature/mem-008-enhanced-testing       # Feature with memory reference
fix/mem-004-core-import-errors         # Fix with memory reference
docs/mem-002-methodology-update        # Documentation with memory reference
refactor/mem-007-file-organization     # Refactor with memory reference

# Traditional format also acceptable
feature/enhanced-tool-management
fix/resolve-import-issues
docs/update-memory-methodology
```

### Branch Types

- **feature/**: New functionality
- **fix/**: Bug fixes
- **docs/**: Documentation updates
- **refactor/**: Code restructuring
- **test/**: Test additions/improvements
- **chore/**: Maintenance tasks

## 🚨 Git Disaster Recovery

### When User Makes a Mess

```bash
# Check what disaster occurred
git status --porcelain
git diff --name-only | head -20
find . -name "*.py" -newer .git/HEAD | head -10

# Check for common disasters
grep -r "print(" . --include="*.py" | head -5
find . -name "*.py" -exec python -m py_compile {} \; 2>&1 | head -10

# Recovery options
git stash push -m "User mess cleanup"
git reset --hard HEAD  # Only if absolutely necessary
git clean -fd  # Remove untracked files
```

### Backup Strategy

```bash
# Before major changes
git stash push -m "Work in progress backup"

# Create safety branch
git checkout -b safety-backup-$(date +%Y%m%d)
git checkout -

# Emergency recovery
git reflog  # Find lost commits
git reset --hard HEAD@{n}  # Restore to specific state
```

## 🔍 Code Review Process

### Before Creating PR

```bash
# Self-review checklist
git diff --name-only origin/main...HEAD  # Files changed
git diff --stat origin/main...HEAD       # Change summary
git log --oneline origin/main...HEAD     # Commit history

# Quality checks
poetry run pytest --cov=haive --cov-fail-under=90
poetry run ruff check .
poetry run mypy .
```

### PR Creation

```bash
# Create PR with gh CLI
gh pr create --title "feat(scope): clear description" --body "$(cat <<'EOF'
## Summary
- Clear description of changes
- Why this change is needed
- How it solves the problem

## Test Plan
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] No regressions

## Breaking Changes
- None / List any breaking changes

🤖 Generated with [Claude Code](https://claude.ai/code)
EOF
)"
```

## 📊 Git Quality Metrics

### Commit Quality

- **Descriptive messages**: Clear intent and context
- **Atomic commits**: One logical change per commit
- **Test coverage**: All commits include tests
- **No broken commits**: Each commit builds successfully

### Branch Management

- **Clean history**: No merge commits in feature branches
- **Rebased features**: Keep linear history
- **Deleted branches**: Remove after merge
- **Protected main**: No direct commits to main

## 🛡️ Protection Protocols

### Pre-work Safety

```bash
# MANDATORY safety checks
git status    # Current state
git diff      # Unstaged changes
git stash push -m "Safety backup"
git branch -v # Current branch
```

### During Work

```bash
# Incremental commits
git add specific_file.py
git commit -m "feat(component): specific change"

# Regular status checks
git status
git diff
```

### Post-work Cleanup

```bash
# Final verification
git log --oneline -5
git diff origin/main...HEAD
poetry run pytest

# Clean push
git push -u origin feature/branch-name
```

## 🎯 Advanced Git Patterns

### Interactive Rebase

```bash
# Clean up commit history before PR
git rebase -i HEAD~3

# Common rebase operations:
# pick = keep commit
# reword = change commit message
# squash = combine with previous commit
# drop = remove commit
```

### Conflict Resolution

```bash
# When merge conflicts occur
git status  # See conflicted files
# Edit files to resolve conflicts
git add resolved_files.py
git commit  # Complete merge

# Abort if needed
git rebase --abort
git merge --abort
```

### Stash Management

```bash
# Named stashes
git stash push -m "work in progress on feature X"

# List stashes
git stash list

# Apply specific stash
git stash apply stash@{1}

# Drop stash
git stash drop stash@{1}
```

## 🔄 Release Workflow

### Version Tagging

```bash
# Create release tag
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin v1.2.0

# List tags
git tag -l

# Checkout specific version
git checkout v1.2.0
```

### Hotfix Process

```bash
# Create hotfix branch from main
git checkout main
git checkout -b hotfix/critical-bug-fix

# Make minimal fix
git add fixed_file.py
git commit -m "fix: resolve critical bug in production"

# Fast-forward merge to main
git checkout main
git merge --ff-only hotfix/critical-bug-fix
git tag -a v1.2.1 -m "Hotfix release 1.2.1"
```

---

**Remember**: Git is our safety net. Proper workflow prevents lost work and enables collaboration. Always prioritize safety over speed.
