# Submodule Management - August 11, 2025

## Overview

This document describes the submodule management actions taken on August 11, 2025, for the haive-mcp and haive-games submodules.

## Submodules Managed

### 1. haive-mcp (`packages/haive-mcp`)

**Repository**: Independent Git repository at `packages/haive-mcp`

**Actions Taken**:

- Created backup tag: `backup-20250811-125715`
- Stashed 1616 modified documentation files (auto-generated RST files)
- Cleaned ~1165 untracked directories (new documentation folders)
- Repository status: Clean

**Restoration Commands**:

```bash
# To view stashed changes
cd packages/haive-mcp
git stash list

# To restore stashed documentation changes
git stash pop

# To go back to backup state
git checkout backup-20250811-125715
```

### 2. haive-games (`packages/haive-games`)

**Repository**: Independent Git repository at `packages/haive-games`

**Actions Taken**:

- Created backup tag: `backup-20250811-125733`
- Stashed 2 modified game files:
  - `src/haive/games/battleship/state_manager.py`
  - `src/haive/games/single_player/wordle/models.py`
- Added to `.gitignore`:
  - `game_test_data/`
  - `real_example_test_data/`
  - `runs/`
  - `**/example.py`
- Committed 3 project documentation files:
  - `project_docs/HAIVE_GAMES_DEVELOPER_GUIDE.md`
  - `project_docs/PENDING_FIXES.md`
  - `project_docs/README.md`

**Restoration Commands**:

```bash
# To view stashed game changes
cd packages/haive-games
git stash list

# To restore stashed game modifications
git stash pop

# To go back to backup state
git checkout backup-20250811-125733
```

## Main Repository Updates

**Actions Taken**:

- Updated submodule reference for haive-games to include new documentation commit
- Commit: "chore: update haive-games submodule with documentation and gitignore updates"

## Important Notes

1. **Submodules are separate Git repositories** - each has its own history, branches, and remote
2. **Backup tags created** - Use these to restore to the exact state before our changes
3. **Stashed changes preserved** - Original modifications are safely stored in git stash
4. **Documentation cleaned** - Auto-generated docs were removed from haive-mcp

## Working with Submodules

### Check submodule status

```bash
git submodule status
```

### Update submodules

```bash
git submodule update --init --recursive
```

### Push changes in submodules

```bash
cd packages/haive-mcp  # or haive-games
git push origin main
```

### Update main repo after submodule changes

```bash
git add packages/haive-mcp  # or haive-games
git commit -m "Update submodule reference"
```

## Git LFS Notes

haive-mcp uses Git LFS for large files. The `.gitattributes` file tracks:

- JSON files
- Data files (pkl, h5, parquet, etc.)
- Model files

When you saw LFS status output, it was showing modified tracked files, not necessarily LFS-specific issues.
