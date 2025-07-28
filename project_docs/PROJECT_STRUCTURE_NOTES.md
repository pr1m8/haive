# Project Structure Notes - Haive Namespaced Polyrepo

**Date**: 2025-01-28
**Purpose**: Document the actual structure and issues with current setup

## What This Is

**Namespaced Polyrepo**: Each package is a completely separate Git repository
- `github.com/pr1m8/haive-core` → publishes `haive-core` to PyPI
- `github.com/pr1m8/haive-agents` → publishes `haive-agents` to PyPI  
- `github.com/pr1m8/haive-tools` → publishes `haive-tools` to PyPI
- etc.

All packages share the `haive.*` Python namespace.

## Current Structure (Problematic)

```
/home/will/Projects/haive/backend/haive/  (parent repo - unnecessary!)
├── packages/
│   ├── haive-core/     (git submodule → github.com/pr1m8/haive-core)
│   ├── haive-agents/   (git submodule → github.com/pr1m8/haive-agents)
│   ├── haive-tools/    (git submodule → github.com/pr1m8/haive-tools)
│   ├── haive-games/    (git submodule → github.com/pr1m8/haive-games)
│   ├── haive-mcp/      (git submodule → github.com/pr1m8/haive-mcp)
│   ├── haive-prebuilt/ (git submodule → github.com/pr1m8/haive-prebuilt)
│   └── haive-dataflow/ (git submodule → github.com/pr1m8/haive-dataflow)
├── project_docs/       (only in parent repo)
├── CLAUDE.md          (only in parent repo)
└── pyproject.toml     (parent repo config)
```

## Why This Is Wrong

1. **Submodules are unnecessary**: In a namespaced polyrepo, packages are independent
2. **Causes detached HEAD issues**: Submodules constantly get into bad states
3. **Complex git workflows**: Can't easily work across packages
4. **No real benefit**: Parent repo doesn't add value

## How It Should Work

**Option 1: True Polyrepo** (each package completely independent)
```
~/Projects/haive-core/      (standalone repo)
~/Projects/haive-agents/    (standalone repo)
~/Projects/haive-tools/     (standalone repo)
```

**Option 2: Monorepo** (everything in one repo)
```
~/Projects/haive/
├── packages/
│   ├── haive-core/     (just a folder)
│   ├── haive-agents/   (just a folder)
│   └── haive-tools/    (just a folder)
└── pyproject.toml      (manages all packages)
```

## Current Problems

1. **Git Submodule Hell**
   - Detached HEAD states
   - `git submodule update` destroys branches
   - Can't commit across packages easily
   - Confusing which repo you're in

2. **Development Friction**
   - Have to manage 8 different git repos
   - Parent repo tracks specific commits (not branches)
   - Easy to break (as demonstrated)

3. **No Clear Benefits**
   - Packages already namespaced (haive.*)
   - Already separate repos on GitHub
   - Parent repo just adds complexity

## What Needs Fixing

### Immediate (haive-core first):
1. Fix import errors in haive-core
2. Get all packages on correct branches
3. Make sure tests pass

### Long-term Options:
1. **Remove parent repo**: Work directly in individual package repos
2. **Convert to monorepo**: Merge all packages into one repo
3. **Keep but simplify**: Remove submodules, just have docs in parent

## Current State of Packages

From `.gitmodules`:
- haive-core: `feature/fix_everything`
- haive-agents: `feature/fix_everything_v2` 
- haive-tools: `feature/fix_everything`
- haive-games: `feature/fix_everything`
- haive-mcp: `feature/fix_everything`
- haive-prebuilt: `feature/fix_everything`
- haive-dataflow: `feature/fix_everything`

But actual state is different due to submodule issues.