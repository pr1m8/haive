# Haive-Core Pyright Issues

**Package**: haive-core
**Total Errors**: 2804
**Total Warnings**: 513

## Critical Issues to Fix

### 1. **all** Module Issues (haive/core/**init**.py)

- **Warning**: "engine" is specified in **all** but is not present in module (line 159)
- **Warning**: "graph" is specified in **all** but is not present in module (line 160)
- **Warning**: "schema" is specified in **all** but is not present in module (line 161)
- **Warning**: "tools" is specified in **all** but is not present in module (line 162)
- **Warning**: "types" is specified in **all** but is not present in module (line 163)
- **Warning**: "utils" is specified in **all** but is not present in module (line 164)
- **Warning**: "models" is specified in **all** but is not present in module (line 165)
- **Warning**: "registry" is specified in **all** but is not present in module (line 166)
- **Warning**: "runtime" is specified in **all** but is not present in module (line 167)

**Fix**: Remove these from **all** or add proper imports for the modules.

### 2. Tool Schema Generator Issues (haive/core/utils/tools/tool_schema_generator.py)

- **Error**: Cannot assign to attribute "**signature_info**" for class "type[BaseModel]" (line 258)
- **Error**: Cannot access attribute "**signature_info**" for class "type[BaseModel]" (line 443)
- **Error**: "from_function" is not a known attribute of "None" (lines 618, 687)
- **Error**: Argument type issues with None values in isinstance checks

**Fix**: Add proper type guards and null checks for optional attributes.

## Status

- [ ] Fix **all** issues in core/**init**.py
- [ ] Fix tool schema generator type issues
- [ ] Address remaining 2800+ type errors
