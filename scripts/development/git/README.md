# Git Development Tools

**Purpose**: Git workflow automation, repository management, and development utilities
**Usage**: Streamlining git operations, automated workflows, and repository maintenance

## 📄 Current Scripts

### Git Automation

- **`git_workflow_helper.py`** - Automated git workflow operations
- **`branch_management.py`** - Branch creation and management utilities
- **`commit_helper.py`** - Standardized commit message generation

### Repository Maintenance

- **`cleanup_branches.py`** - Clean up merged and stale branches
- **`validate_commits.py`** - Validate commit message standards
- **`sync_submodules.py`** - Submodule synchronization utilities

## 🚀 Common Usage

### Workflow Automation

```bash
# Automated workflow operations
poetry run python scripts/development/git/git_workflow_helper.py

# Branch management
poetry run python scripts/development/git/branch_management.py --create feature/new-feature

# Standardized commits
poetry run python scripts/development/git/commit_helper.py --type feat --scope agents
```

### Repository Maintenance

```bash
# Clean up branches
poetry run python scripts/development/git/cleanup_branches.py

# Validate commit standards
poetry run python scripts/development/git/validate_commits.py

# Sync submodules
poetry run python scripts/development/git/sync_submodules.py
```

## 🔧 Git Standards

### Commit Message Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Branch Naming

- **feature/**: New features
- **fix/**: Bug fixes
- **docs/**: Documentation updates
- **refactor/**: Code refactoring
- **test/**: Test additions

### Workflow Standards

- **Safety checks**: Always check status before operations
- **Incremental commits**: Small, focused changes
- **Quality gates**: Tests must pass before commit
- **Review process**: Code review before merge

## 📊 Git Categories

### Development Workflows

- Feature branch creation and management
- Automated testing integration
- Code review preparation
- Merge conflict resolution

### Repository Health

- Branch cleanup and maintenance
- Commit history validation
- Submodule synchronization
- Repository optimization

### Automation Integration

- CI/CD pipeline integration
- Automated quality checks
- Release preparation
- Deployment workflows

## 🔍 Submodule Management

### Haive Submodules

```
packages/haive-core/     # Core framework
packages/haive-agents/   # Agent implementations
packages/haive-tools/    # Tool integrations
packages/haive-games/    # Game environments
packages/haive-mcp/      # MCP integration
```

### Submodule Operations

```bash
# Initialize all submodules
git submodule update --init --recursive

# Update specific submodule
cd packages/haive-agents && git pull origin main

# Sync all submodules
poetry run python scripts/development/git/sync_submodules.py
```

## 🚀 Development Benefits

### Workflow Efficiency

- Automated repetitive tasks
- Consistent naming conventions
- Standardized processes
- Reduced manual errors

### Quality Assurance

- Commit message validation
- Pre-commit quality checks
- Automated testing integration
- Code review automation

### Repository Management

- Clean branch structure
- Healthy commit history
- Synchronized submodules
- Optimized performance

## 🔗 Related

- **[Git Workflow Guide](../../../project_docs/active/standards/git/workflow.md)** - Complete git standards
- **[CI/CD Scripts](../../ci/README.md)** - Continuous integration
- **[Testing Suite](../../testing/README.md)** - Quality validation
