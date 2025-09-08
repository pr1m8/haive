# Recovery Plan - Step by Step

## 🎯 The Goal

Get our good changes (CSS simplification, submodule updates) onto the CURRENT main that has all the docs/ai21-pilot work.

## 📋 Current Status

- **We have**: 2 commits on old main + stashed changes
- **We need**: Those changes on top of current remote main
- **Backup branch**: `backup-before-merge-20250130-014510`
- **Patch files**: Already saved in `project_docs/git-main-merge-safety/`
- **Stash**: Contains trunk config and haive-mcp changes

## 🚀 THE PLAN

### Step 1: Create New Feature Branch from Current Remote

```bash
# Start from the CURRENT remote main (has docs/ai21-pilot merged)
git checkout -b feature/doc-simplification origin/main

# This gives us all 284 commits including docs/ai21-pilot work
```

### Step 2: Apply Our Good Changes

```bash
# Option A: Use the patch files (SAFEST)
git am project_docs/git-main-merge-safety/0001-docs-standardize-purple-theme-using-CSS-variables.patch
git am project_docs/git-main-merge-safety/0002-feat-docs-update-submodules-and-add-documentation-in.patch

# OR Option B: Cherry-pick from our backup
git cherry-pick d9ea365c  # CSS standardization
git cherry-pick e9380f7f  # Submodule updates
```

### Step 3: Handle Conflicts (if any)

During the apply, we'll likely get conflicts on:

- `docs/source/conf.py` - Keep OUR simple version
- Submodule references - Keep OUR updated ones

```bash
# If conflicts occur:
git status  # See what's conflicting

# For conf.py - keep our simplified version:
git checkout backup-before-merge-20250130-014510 -- docs/source/conf.py
git add docs/source/conf.py

# Continue applying:
git am --continue  # or git cherry-pick --continue
```

### Step 4: Apply Stashed Changes

```bash
# Apply the trunk config and haive-mcp changes
git stash pop  # or git stash apply stash@{0}
```

### Step 5: Verify Everything Works

```bash
# Build docs to test
poetry run sphinx-build -b html docs/source docs/build/html

# Check submodule status
git submodule status

# Run any tests
poetry run pytest
```

### Step 6: Commit Final Changes

```bash
# If there are any remaining changes
git add .
git commit -m "feat(docs): apply documentation simplifications

- Remove redundant CSS files
- Simplify conf.py configuration
- Update submodule references
- Enable trunk submodule hooks"
```

## 🔄 Alternative Approach (if cherry-pick fails)

### Manual Recreation

```bash
# 1. Start fresh from remote main
git checkout -b feature/doc-cleanup origin/main

# 2. Manually remove CSS files
find packages -name "purple-theme*.css" -delete
find packages -name "code-purple-theme.css" -delete
find packages -name "tippy-enhancements.css" -delete

# 3. Copy our simplified conf.py
cp project_docs/git-main-merge-safety/conf.py.backup docs/source/conf.py

# 4. Update submodule references
cd packages/haive-agents && git checkout <our-commit> && cd ../..
cd packages/haive-core && git checkout <our-commit> && cd ../..
# ... repeat for all submodules

# 5. Add and commit
git add -A
git commit -m "feat(docs): simplify documentation setup"
```

## ⚠️ What We're Preserving

1. **Our simplified conf.py** (no haive_docs_config complexity)
2. **Removed CSS files** (clean approach)
3. **Updated submodule references** (our latest updates)
4. **Trunk config changes** (submodule-init-update enabled)

## ✅ Success Criteria

After recovery, we should have:

- All 284 commits from remote main ✓
- Our CSS simplifications on top ✓
- Updated submodule references ✓
- Documentation builds successfully ✓
- No redundant CSS files ✓

## 🔐 Safety Checks

Before starting:

```bash
# Verify backup branch exists
git branch | grep backup-before-merge

# Verify patches exist
ls project_docs/git-main-merge-safety/*.patch

# Verify stash exists
git stash list | grep "trunk config"
```

## 🚨 If Something Goes Wrong

```bash
# Reset to our backup
git reset --hard backup-before-merge-20250130-014510

# Or reset to original state
git checkout main
git reset --hard e9380f7f
git stash pop
```

## 📝 Final Notes

The key insight: We're NOT trying to merge our old main. We're:

1. Starting fresh from current remote main
2. Applying just our valuable changes on top
3. This avoids complex merge conflicts
4. Gets us the best of both worlds

Ready to proceed?
