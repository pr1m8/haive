# Quick Fixes

**Purpose**: One-off fix scripts for common code issues  
**Usage**: Run when encountering specific syntax, validation, or structural problems

## 📄 Scripts

### `fix_syntax_errors.py`

- **Purpose**: Fix common Python syntax errors across the codebase
- **Usage**: `poetry run python scripts/maintenance/quick-fixes/fix_syntax_errors.py`
- **Safe**: Includes dry-run mode and backup creation

### `fix_pydantic_validators.py`

- **Purpose**: Fix Pydantic validator signature and compatibility issues
- **Usage**: `poetry run python scripts/maintenance/quick-fixes/fix_pydantic_validators.py`
- **Safe**: Validates before applying changes

## 🚀 Usage Pattern

```bash
# Always run with caution and backups
git checkout -b backup-before-fixes
poetry run python scripts/maintenance/quick-fixes/[script_name].py
# Validate results before committing
```

## ⚠️ Safety Notes

- All scripts should be run with backups
- Test imports after running fixes
- Review changes before committing
- Use `--help` flag for script-specific options
