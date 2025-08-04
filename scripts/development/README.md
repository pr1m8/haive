# Development Utilities

**Purpose**: Development workflow tools, git utilities, and diagnostics
**Usage**: Daily development workflow support and troubleshooting

## 📄 Scripts

### Git Workflow

- **`stash_recovery_plan.sh`** - Recover lost git stashes and work
- **`analyze_stash_differences.sh`** - Analyze differences between stashes
- **`safe-dev-changes.sh`** - Safe development workflow with backups
- **`universal_pre_commit_capture.sh`** - Pre-commit validation and capture

### Subdirectories

#### `diagnostics/`

- Diagnostic and analysis tools
- Error analysis and troubleshooting utilities
- Code quality assessment tools

#### `typing/`

- Type checking and inference tools
- Automatic type hint generation
- Type system utilities

#### `git/`

- Advanced git utilities and analysis
- Repository management tools
- Git history analysis

## 🚀 Common Usage

```bash
# Safe development workflow
./scripts/development/safe-dev-changes.sh

# Recover lost work
./scripts/development/stash_recovery_plan.sh

# Pre-commit validation
./scripts/development/universal_pre_commit_capture.sh

# Run diagnostics
poetry run python scripts/development/diagnostics/[tool_name].py
```

## 🛡️ Safety Features

- Automatic backup creation
- Validation before changes
- Rollback capabilities
- Comprehensive logging
