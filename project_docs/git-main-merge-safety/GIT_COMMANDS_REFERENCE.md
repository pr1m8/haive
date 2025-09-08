# Git Commands Reference - Recovery & Merge

## Current State References

### Branches

- **Current**: main
- **Backup**: backup-before-merge-20250130-014510
- **Remote**: origin/main (284 commits ahead)
- **Docs Branch**: docs/ai21-pilot (already merged to remote)

### Important Commits

- `e9380f7f` - Our latest: feat(docs): update submodules and add documentation infrastructure
- `d9ea365c` - Our second: docs: standardize purple theme using CSS variables
- `9df785a4` - Common ancestor: Merge pull request #2
- `5ca72de7` - Remote latest: Merge pull request #4 from pr1m8/docs/ai21-pilot

### Stash

- `stash@{0}` - "Save uncommitted changes: trunk config and haive-mcp"

## Recovery Commands

### Get Back to Current State

```bash
# Method 1: Using backup branch
git checkout backup-before-merge-20250130-014510
git stash pop  # Restore uncommitted changes

# Method 2: Reset to specific commit
git reset --hard e9380f7f
git stash pop

# Method 3: From patches
git checkout 9df785a4  # Go to common ancestor
git am project_docs/git-main-merge-safety/0001-*.patch
git am project_docs/git-main-merge-safety/0002-*.patch
```

### View What's in Stash

```bash
git stash list
git stash show -p stash@{0}
```

## Merge Options

### Option 1: Safe Merge (Recommended)

```bash
# Create feature branch first
git checkout -b feature/simplified-docs
git merge origin/main

# Resolve conflicts:
# - Keep our docs/source/conf.py
# - Accept their tools/ structure
# - Keep our submodule refs

# Test everything
poetry run sphinx-build -b html docs/source docs/build/html

# If good, update main
git checkout main
git merge feature/simplified-docs
```

### Option 2: Cherry-pick Approach

```bash
# Start from updated remote
git checkout -b feature/docs-simplification origin/main

# Apply our changes
git cherry-pick d9ea365c  # Purple theme standardization
git cherry-pick e9380f7f  # Submodule updates

# Create PR
gh pr create --title "Simplify documentation setup" --body "..."
```

### Option 3: Direct Merge (Risky)

```bash
git merge origin/main
# Resolve all conflicts
# Test thoroughly
```

## Conflict Resolution

### For docs/source/conf.py

```bash
# During merge conflict
git checkout --ours docs/source/conf.py  # Keep our version
# OR
git checkout --theirs docs/source/conf.py  # Take their version
# OR
# Edit manually and then:
git add docs/source/conf.py
```

### For submodules

```bash
# After merge, update submodules
git submodule update --init --recursive

# To keep our submodule versions:
cd packages/haive-agents
git checkout <our-commit>
cd ../..
git add packages/haive-agents
```

## Verification Commands

### Check Current Status

```bash
git status
git branch -vv
git log --oneline -5
git diff origin/main
```

### Check Submodules

```bash
git submodule status
git submodule foreach 'echo $path: && git status'
```

### Check Documentation

```bash
# Build docs
poetry run sphinx-build -b html docs/source docs/build/html

# Test with playwright
poetry run playwright test

# Check for broken links
python -m http.server 8000 --directory docs/build/html
```

## Emergency Rollback

### If Everything Goes Wrong

```bash
# Save current state first
git branch emergency-save-$(date +%s)

# Go back to backup
git reset --hard backup-before-merge-20250130-014510

# Restore stash
git stash pop

# Verify we're back
git log --oneline -5
git status
```

### Nuclear Option

```bash
# Complete reset to our last known good state
git reset --hard e9380f7f
git clean -fd
git submodule update --init --recursive
git stash pop
```

## Important Files to Preserve

1. `docs/source/conf.py` - Our simplified version
2. `docs/source/_templates/` - Our templates
3. `.env.example` - With R2 variables
4. All submodule current commits

## Testing Checklist After Merge

- [ ] Documentation builds without errors
- [ ] All package links work
- [ ] Purple theme displays correctly (if applicable)
- [ ] No redundant CSS files
- [ ] Submodules at correct commits
- [ ] R2 upload still works
- [ ] Playwright tests pass

## Notes

- Our commits are saved as patches in `project_docs/git-main-merge-safety/`
- Backup branch: `backup-before-merge-20250130-014510`
- Stash contains trunk config and haive-mcp changes
- All submodule work is already pushed to their repos

## DO NOT FORGET

1. We removed CSS files - this is correct
2. Our simple conf.py is what we want
3. Submodules are all updated and pushed
4. haive-mcp PR #2 is already merged
5. Test everything before finalizing
