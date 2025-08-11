# Utility Scripts

**Utility scripts for haive-mcp maintenance and development**

## 🛠️ Available Utilities

### Data Management

- **`get_all_registries.py`** - Fetch MCP server registry data
- **`get_all_servers.py`** - Download complete MCP server database
- **`fix_imports.sh`** - Fix import statements in Python files

### Usage

```bash
# Update MCP server registry
python scripts/utilities/get_all_registries.py

# Download latest server database
python scripts/utilities/get_all_servers.py

# Fix import issues
bash scripts/utilities/fix_imports.sh
```

## 🎯 Purpose

These utilities help with:

- **Data Updates**: Keep MCP server database current
- **Maintenance**: Fix common development issues
- **Database Management**: Manage the 1,960+ server database
- **Import Fixes**: Resolve Python import problems

## ⚠️ Usage Notes

- Run data scripts with caution - they download large amounts of data
- `fix_imports.sh` modifies source files - use version control
- These scripts are primarily for maintainers and advanced users
