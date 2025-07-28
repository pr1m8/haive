# Git Workflow for Documentation Fix

**Purpose**: Version control strategy for documentation improvements

## 🌿 Branch Strategy

### Current State

```
main (or feature/fix_everything)
└── docs/fix-documentation-20250121 (existing attempt)
```

### Proposed Structure

```
main
├── docs/fix-documentation-20250121 (keep for reference)
├── docs/sphinx-incremental-fix-2025 (new)
├── docs/mkdocs-poc-2025 (new)
├── docs/hybrid-comparison-2025 (new)
└── docs/final-documentation-2025 (after decision)
```

## 📝 Branch Descriptions

### `docs/sphinx-incremental-fix-2025`

- **Purpose**: Fix current Sphinx setup
- **Approach**: Incremental improvements
- **Based on**: Current main + learnings from previous branch

### `docs/mkdocs-poc-2025`

- **Purpose**: MkDocs proof of concept
- **Approach**: Fresh start with MkDocs
- **Scope**: Initially just haive-core

### `docs/hybrid-comparison-2025`

- **Purpose**: Side-by-side comparison
- **Approach**: Cherry-pick from both branches
- **Output**: Comparison reports

### `docs/final-documentation-2025`

- **Purpose**: Final chosen solution
- **Created**: After decision made
- **Content**: Merged from winning approach

## 🔧 Workflow Commands

### Initial Setup

```bash
# Stash any current work
git stash push -m "Current documentation work"

# Create Sphinx fix branch
git checkout -b docs/sphinx-incremental-fix-2025
git push -u origin docs/sphinx-incremental-fix-2025

# Create MkDocs PoC branch
git checkout main
git checkout -b docs/mkdocs-poc-2025
git push -u origin docs/mkdocs-poc-2025

# Create comparison branch
git checkout main
git checkout -b docs/hybrid-comparison-2025
git push -u origin docs/hybrid-comparison-2025
```

### Daily Workflow

```bash
# Start work
git checkout docs/sphinx-incremental-fix-2025
git pull

# Make changes
# ... edit files ...

# Commit with meaningful message
git add -p  # Interactive staging
git commit -m "docs(sphinx): implement phase 1 minimal build

- Remove all complexity
- Basic Furo theme working
- Baseline metrics: X errors, Y warnings

Ref: PHASE_1_MINIMAL.md"

# Push changes
git push
```

### Commit Message Format

```
docs(<approach>): <what changed>

- <detail 1>
- <detail 2>
- Metrics: X errors, Y warnings, Z files

Ref: <relevant doc>
```

Examples:

```
docs(sphinx): reduce errors from 6802 to 3000
docs(mkdocs): create initial configuration
docs(comparison): add build time metrics
```

### Comparison Workflow

```bash
# On comparison branch
git checkout docs/hybrid-comparison-2025

# Cherry-pick successful fixes
git cherry-pick <commit-from-sphinx-branch>
git cherry-pick <commit-from-mkdocs-branch>

# Create comparison report
echo "# Build Comparison $(date)" > comparison-report.md
# Add metrics, screenshots, etc.
```

## 📊 Tracking Progress

### Metrics to Track in Each Commit

```markdown
<!-- In commit message or file -->

## Build Metrics

- Errors: 6802 → 3401 (-50%)
- Warnings: 2407 → 1200 (-50%)
- HTML files: 13 → 156 (+1100%)
- Build time: ??? → 45s
- Memory usage: ??? → 1.2GB
```

### Tag Working Configurations

```bash
# When something works
git tag -a sphinx-phase1-working -m "Phase 1 working: 0 errors on minimal build"
git push --tags

# For comparison points
git tag -a comparison-checkpoint-1 -m "First comparison point"
```

## 🔄 Synchronization

### Keep Branches Updated

```bash
# Regularly sync with main
git checkout docs/sphinx-incremental-fix-2025
git fetch origin
git rebase origin/main

# Share learnings between branches
git checkout docs/mkdocs-poc-2025
git cherry-pick <useful-commit-from-sphinx>
```

### Cross-Branch Learnings

```bash
# Create a learnings file
cat > docs/LEARNINGS.md << EOF
# Documentation Build Learnings

## From Sphinx Branch
- Discovery 1
- Discovery 2

## From MkDocs Branch
- Discovery 1
- Discovery 2
EOF

# Share across branches
git add docs/LEARNINGS.md
git commit -m "docs: share learnings across approaches"
```

## 🚀 Deployment Strategy

### Testing Builds

```bash
# Sphinx branch
git checkout docs/sphinx-incremental-fix-2025
nox -s docs
python -m http.server 8000 --directory docs/build/html

# MkDocs branch
git checkout docs/mkdocs-poc-2025
mkdocs serve --dev-addr 0.0.0.0:8001
```

### Final Merge

```bash
# After decision made
git checkout main
git checkout -b docs/final-documentation-2025

# Merge chosen approach
git merge --no-ff docs/sphinx-incremental-fix-2025
# OR
git merge --no-ff docs/mkdocs-poc-2025

# Tag release
git tag -a docs-v2.0.0 -m "New documentation system"
git push --tags
```

## 📋 Checklist for Each Approach

### Sphinx Branch Checklist

- [ ] Create branch
- [ ] Implement Phase 1
- [ ] Commit with metrics
- [ ] Tag if working
- [ ] Document learnings
- [ ] Update comparison

### MkDocs Branch Checklist

- [ ] Create branch
- [ ] Set up MkDocs
- [ ] Configure for monorepo
- [ ] Test with haive-core
- [ ] Document setup process
- [ ] Update comparison

### Comparison Checklist

- [ ] Screenshot both outputs
- [ ] Measure build times
- [ ] Count files generated
- [ ] Test search functionality
- [ ] Check mobile responsive
- [ ] Create decision matrix

## 🛟 Recovery Procedures

### If Branch Gets Messy

```bash
# Save current work
git stash push -m "Saving work before cleanup"

# Reset to last known good
git reset --hard <last-good-commit>

# Or start fresh
git checkout main
git branch -D docs/sphinx-incremental-fix-2025
git checkout -b docs/sphinx-incremental-fix-2025
```

### If Need Previous Work

```bash
# Check out file from other branch
git checkout docs/fix-documentation-20250121 -- docs/source/conf.py

# Or view without checking out
git show docs/fix-documentation-20250121:docs/source/conf.py
```

## 📝 Documentation Updates

Each branch should maintain:

1. `PROGRESS.md` - Daily progress log
2. `METRICS.md` - Current metrics
3. `ISSUES.md` - Problems encountered
4. `DECISIONS.md` - Decisions made

## 🎯 Success Criteria

Before merging any branch:

- [ ] Metrics documented
- [ ] Comparison updated
- [ ] Team review completed
- [ ] Decision documented
- [ ] Clean commit history

---

**Next Step**: Create branches and start implementation per [MASTER_PLAN.md](./MASTER_PLAN.md)
