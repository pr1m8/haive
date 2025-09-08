# Branching and Submodule Strategy for Architecture v3.0

**Created**: 2025-01-30  
**Purpose**: Define branching strategy and submodule management for clean architecture transformation  
**Status**: Implementation Guidelines

## 🎯 Overview

Haive is a **monorepo with Git submodules** - each package is its own repository. This requires careful coordination during the architecture transformation to maintain consistency across all packages.

## 📦 Submodule Structure

```
haive/                           # Main repository
├── packages/                    # Each package is a separate Git repository
│   ├── haive-core/             # github.com/pr1m8/haive-core
│   ├── haive-agents/           # github.com/pr1m8/haive-agents
│   ├── haive-tools/            # github.com/pr1m8/haive-tools
│   ├── haive-games/            # github.com/pr1m8/haive-games
│   ├── haive-mcp/              # github.com/pr1m8/haive-mcp
│   ├── haive-prebuilt/         # github.com/pr1m8/haive-prebuilt
│   ├── haive-dataflow/         # github.com/pr1m8/haive-dataflow
│   └── haive-hap/              # github.com/pr1m8/haive-hap
├── project_docs/               # Documentation (main repo only)
├── scripts/                    # Utility scripts (main repo only)
└── examples/                   # Example code (main repo only)
```

### Key Implications

1. **Each package has its own**:
   - Git history and branches
   - Issues and PRs
   - Version tags
   - CI/CD pipelines
   - Release cycle

2. **Changes must be coordinated**:
   - Breaking changes affect multiple repos
   - Dependencies between packages
   - Version compatibility requirements

## 🌿 Branching Strategy

### Main Repository Branches

```
main                            # Stable production code
├── feature/arch-v3-transformation  # Architecture v3.0 umbrella branch
│   ├── feature/arch-v3-contracts   # Contracts domain work
│   ├── feature/arch-v3-engine      # Engine decomposition work
│   ├── feature/arch-v3-node        # Node consolidation work
│   ├── feature/arch-v3-schema      # Schema modularization work
│   ├── feature/arch-v3-workflow    # Workflow creation work
│   ├── feature/arch-v3-agent       # Agent cleanup work
│   └── feature/arch-v3-testing     # Testing infrastructure
└── develop                     # Integration branch for v3.0
```

### Submodule Branch Coordination

Each submodule should have matching branches:

```
haive-core/
├── main                        # Current stable
├── feature/arch-v3             # Architecture v3.0 changes
└── feature/arch-v3-contracts   # Specific domain work

haive-agents/
├── main                        # Current stable
├── feature/arch-v3             # Architecture v3.0 changes
└── feature/arch-v3-agent       # Agent cleanup work
```

## 📋 Implementation Workflow

### Phase 1: Setup (Day 1)

```bash
# 1. Create umbrella branch in main repo
git checkout -b feature/arch-v3-transformation

# 2. Create matching branches in each submodule
cd packages/haive-core
git checkout -b feature/arch-v3
cd ../..

cd packages/haive-agents
git checkout -b feature/arch-v3
cd ../..

# 3. Update submodule references
git add packages/
git commit -m "chore: create arch-v3 branches in all submodules"
```

### Phase 2: Domain Implementation

For each domain (contracts, engine, node, etc.):

```bash
# 1. Create domain branch in main repo
git checkout feature/arch-v3-transformation
git checkout -b feature/arch-v3-contracts

# 2. Create domain branches in affected submodules
cd packages/haive-core
git checkout feature/arch-v3
git checkout -b feature/arch-v3-contracts

# 3. Implement changes
# ... make changes ...

# 4. Commit in submodule
git add .
git commit -m "feat(contracts): implement ExecutionContract protocol"
git push origin feature/arch-v3-contracts

# 5. Update main repo reference
cd ../..
git add packages/haive-core
git commit -m "feat(contracts): update haive-core with ExecutionContract"
```

### Phase 3: Integration

```bash
# 1. Merge domain branches into arch-v3 in each submodule
cd packages/haive-core
git checkout feature/arch-v3
git merge feature/arch-v3-contracts
git merge feature/arch-v3-engine
# ... merge all domain branches

# 2. Test integration
poetry run pytest

# 3. Push integrated branch
git push origin feature/arch-v3
```

### Phase 4: Release

```bash
# 1. Create PRs in each submodule
# haive-core: feature/arch-v3 → main
# haive-agents: feature/arch-v3 → main
# ... for each package

# 2. Coordinate merged PRs

# 3. Update main repo to point to new commits
git checkout feature/arch-v3-transformation
git submodule update --remote
git add packages/
git commit -m "feat: complete architecture v3.0 transformation"

# 4. Create main repo PR
# feature/arch-v3-transformation → main
```

## 🔄 Dependency Management

### Package Dependencies

```python
# haive-core/pyproject.toml
[tool.poetry.dependencies]
# No dependencies on other haive packages (foundation)

# haive-agents/pyproject.toml
[tool.poetry.dependencies]
haive-core = "^3.0.0"  # Depends on core v3

# haive-tools/pyproject.toml
[tool.poetry.dependencies]
haive-core = "^3.0.0"  # Depends on core v3

# haive-prebuilt/pyproject.toml
[tool.poetry.dependencies]
haive-core = "^3.0.0"
haive-agents = "^3.0.0"
haive-tools = "^3.0.0"
```

### Version Coordination

During transformation, use path dependencies:

```toml
# Temporary during development
haive-core = { path = "../haive-core", develop = true }
```

After release, switch to version dependencies:

```toml
# Production dependencies
haive-core = "^3.0.0"
```

## 🧹 Keeping It Clean

### 1. Commit Hygiene

```bash
# ✅ GOOD - Clear, atomic commits
git commit -m "refactor(engine): extract LLMConfig from AugLLMConfig"
git commit -m "feat(node): implement ContractNode with ExecutionContract"
git commit -m "test(schema): add property-based tests for StateSchema"

# ❌ BAD - Vague, mixed commits
git commit -m "updates"
git commit -m "WIP"
git commit -m "fix stuff and add features"
```

### 2. Branch Cleanup

```bash
# After merging, delete feature branches
git branch -d feature/arch-v3-contracts
git push origin --delete feature/arch-v3-contracts

# Clean up in submodules too
cd packages/haive-core
git branch -d feature/arch-v3-contracts
git push origin --delete feature/arch-v3-contracts
```

### 3. Submodule Sync

```bash
# Keep submodules in sync
git submodule update --init --recursive
git submodule foreach git fetch
git submodule foreach git checkout feature/arch-v3

# Update to latest commits
git submodule update --remote
```

## 📊 Progress Tracking

### Branch Status Dashboard

```bash
#!/bin/bash
# Check transformation progress across all packages

echo "🎯 Architecture v3.0 Branch Status"
echo "=================================="

for pkg in haive-core haive-agents haive-tools haive-games haive-mcp haive-prebuilt haive-dataflow haive-hap; do
    echo -n "📦 $pkg: "
    cd packages/$pkg

    if git branch -r | grep -q "origin/feature/arch-v3"; then
        echo "✅ arch-v3 branch exists"

        # Check progress
        COMMITS=$(git rev-list --count main..origin/feature/arch-v3 2>/dev/null || echo "0")
        echo "   📈 Progress: $COMMITS commits ahead of main"
    else
        echo "❌ No arch-v3 branch yet"
    fi

    cd ../..
done
```

### Domain Implementation Tracking

| Domain    | Branch                    | haive-core | haive-agents | haive-tools | Status   |
| --------- | ------------------------- | ---------- | ------------ | ----------- | -------- |
| Contracts | feature/arch-v3-contracts | Required   | -            | -           | 🔄 Ready |
| Engine    | feature/arch-v3-engine    | Required   | Impact       | -           | 🔄 Ready |
| Node      | feature/arch-v3-node      | Required   | Impact       | -           | 🔄 Ready |
| Schema    | feature/arch-v3-schema    | Required   | Impact       | Impact      | 🔄 Ready |
| Workflow  | feature/arch-v3-workflow  | -          | Required     | -           | 🔄 Ready |
| Agent     | feature/arch-v3-agent     | -          | Required     | -           | 🔄 Ready |
| Testing   | feature/arch-v3-testing   | Required   | Required     | Required    | 🔄 Ready |

## 🚨 Critical Rules

### 1. Never Force Push Submodules

```bash
# ❌ NEVER DO THIS
git push --force origin feature/arch-v3

# ✅ Safe push
git push origin feature/arch-v3
```

### 2. Always Test Before Pushing

```bash
# Required checks before push
poetry run pytest
poetry run mypy .
poetry run ruff check
```

### 3. Coordinate Breaking Changes

When making breaking changes:

1. **Document** in BREAKING_CHANGES.md
2. **Communicate** via PRs in all affected repos
3. **Version** appropriately (major version bump)
4. **Migrate** with compatibility layer if possible

### 4. Maintain CI/CD

Each submodule PR must:

- Pass all tests
- Pass linting and type checking
- Update documentation
- Include migration guide if breaking

## 🎯 Success Criteria

### Clean Transformation Checklist

- [ ] All packages have feature/arch-v3 branches
- [ ] No commits on main during transformation
- [ ] All tests pass on every commit
- [ ] Documentation updated for all changes
- [ ] Migration guides for breaking changes
- [ ] Version bumps planned and coordinated
- [ ] CI/CD pipelines remain green
- [ ] Old branches deleted after merge
- [ ] Submodule references updated in main repo
- [ ] Final PR includes all transformation documentation

## 📝 Git Commands Reference

### Common Submodule Operations

```bash
# Update all submodules to latest
git submodule update --remote --merge

# Check status of all submodules
git submodule foreach git status

# Fetch updates in all submodules
git submodule foreach git fetch

# Check out specific branch in all submodules
git submodule foreach git checkout feature/arch-v3

# See what changed in submodules
git diff --submodule

# Reset submodule to recorded commit
git submodule update --force packages/haive-core
```

### Coordination Commands

```bash
# Create branch in all packages
for pkg in packages/*; do
    cd $pkg
    git checkout -b feature/arch-v3
    cd ../..
done

# Check branch status across packages
for pkg in packages/*; do
    echo "$(basename $pkg):"
    cd $pkg
    git branch -v | grep arch-v3
    cd ../..
done
```

## 🔄 Rollback Strategy

If transformation needs rollback:

```bash
# 1. In each submodule
cd packages/haive-core
git checkout main
git branch -D feature/arch-v3

# 2. In main repo
git checkout main
git branch -D feature/arch-v3-transformation
git submodule update --init --recursive
```

---

**Remember**: The architecture transformation spans multiple repositories. Careful coordination and clean branching practices are essential for success. Each domain implementation should be atomic and testable independently.
