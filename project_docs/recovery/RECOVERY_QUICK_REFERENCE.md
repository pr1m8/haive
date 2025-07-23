# Quick Reference: Haive Import Recovery

## 🚨 Current Status (July 20, 2025 - 6:45 PM)

- ✅ All packages reverted to working state (July 18 commits)
- ✅ Imports working, docs building
- ⚠️ Missing 2,550+ type hints and new features
- 📋 Recovery plan created

## 🔧 Immediate Commands

### Check Current State

```bash
# Verify imports work
poetry run python -c "import haive.core; import haive.agents; print('✅ Imports OK')"

# Check what we're missing
git stash list
git stash show stash@{0} --stat

# See specific file changes
git stash show -p stash@{0} -- path/to/file
```

### Extract Good Files (Example)

```bash
# Extract timestamp_mixin.py
git show stash@{0}:src/haive/core/common/mixins/timestamp_mixin.py > /tmp/timestamp_mixin_broken.py

# View it first
less /tmp/timestamp_mixin_broken.py

# Fix imports manually, then copy
# Change: from mixins.X import Y
# To: from haive.core.common.mixins.X import Y
```

## 📍 Quick Locations

### Stashed Changes

- `stash@{0}`: Current broken state with all changes
- `stash@{1}`: Earlier work in progress

### Key Files to Recover

1. `/src/haive/core/common/mixins/timestamp_mixin.py`
2. `/src/haive/core/persistence/persistence_types.py`
3. Type hints in all packages
4. Automation tools in root directory

### Working Commits (Don't Go Past These!)

- haive-core: `b970f90`
- haive-agents: `c8d0985`
- haive-dataflow: `4ae4337`
- haive-games: `70c6da8`
- haive-mcp: `6b53181`
- haive-prebuilt: `c493c58`
- haive-tools: `1553cce`

## ⚡ Quick Fixes

### Fix Import Pattern

```python
# WRONG (from stash)
from mixins.timestamp_mixin import TimestampMixin
from engine.aug_llm import AugLLMConfig

# CORRECT
from haive.core.common.mixins.timestamp_mixin import TimestampMixin
from haive.core.engine.aug_llm import AugLLMConfig
```

### Test After Each Change

```bash
# Quick test
poetry run python -c "from haive.core.common.mixins.timestamp_mixin import TimestampMixin"

# Full test
poetry run pytest packages/haive-core/tests/ -k "timestamp" -v
```

## 🎯 Priority Order

1. **First**: Get timestamp_mixin.py working (test case)
2. **Second**: Fix critical **init**.py files
3. **Third**: Apply type hints to core modules
4. **Fourth**: Recover automation tools
5. **Last**: Clean up and document

## ⚠️ What NOT to Do

- ❌ Don't run any "fix all" scripts
- ❌ Don't trust regex replacements on imports
- ❌ Don't commit without testing imports
- ❌ Don't apply stashed changes directly
- ❌ Don't modify multiple packages at once

## ✅ Safe Recovery Process

1. Extract one file from stash
2. Fix its imports manually
3. Test that specific import works
4. Run related tests
5. Commit with clear message
6. Move to next file

## 📞 If Something Goes Wrong

```bash
# Check current state
git status
git diff

# Revert if needed
git checkout -- path/to/file

# Return to safe commit
git checkout b970f90  # for haive-core
```

---

**Remember**: Slow and steady. Test every change. Imports first, features second.
