# Tools Directory

**Utility tools for haive-mcp development and maintenance**

## 🔧 Available Tools

### Health & Validation

- **`check_health.py`** - Health check for MCP servers and connections
- **`check_syntax_errors.py`** - Syntax validation for Python files
- **`validate_setup.py`** - Validate haive-mcp installation and configuration

### Usage

```bash
# Check system health
python tools/check_health.py

# Validate syntax
python tools/check_syntax_errors.py

# Validate setup
python tools/validate_setup.py
```

## 🎯 Purpose

These tools help with:

- **Development**: Quick validation during development
- **CI/CD**: Automated health checks in pipelines
- **Troubleshooting**: Diagnose issues with MCP setup
- **Quality Assurance**: Ensure code quality and proper configuration
