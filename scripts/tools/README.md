# General Tools

**Purpose**: General utilities and standalone tools for development support
**Usage**: Miscellaneous utilities that don't fit into specific categories

## 📄 Current Scripts

### Registry Tools

- **`check_registry_data.py`** - Validate registry data integrity
- **`store_registry_data.py`** - Store and manage registry information

## 🔧 Tool Categories

### Data Management

- Registry validation and management
- Data consistency checking
- Storage utilities

### Utility Functions

- General purpose development tools
- Helper scripts for common tasks
- Standalone utility programs

## 🚀 Usage Examples

### Registry Management

```bash
# Check registry data
poetry run python scripts/tools/check_registry_data.py

# Store registry information
poetry run python scripts/tools/store_registry_data.py
```

### General Utilities

```bash
# Run specific utility tools
poetry run python scripts/tools/[tool_name].py --help
```

## 📊 Tool Standards

### Consistency

- Follow naming conventions: `action_subject.py`
- Include comprehensive help text
- Provide example usage

### Safety

- Include validation before operations
- Provide dry-run modes where appropriate
- Generate logs for tracking

### Integration

- Compatible with automation workflows
- Support for batch operations
- JSON output for programmatic use

## 🔗 Related

- **[Testing Suite](../testing/docs/README.md)** - Validation tools
- **[Development Tools](../development/README.md)** - Development utilities
- **[Automation Scripts](../automation/README.md)** - Workflow integration
