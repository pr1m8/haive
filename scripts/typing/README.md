# Haive Typing Scripts - Auto-Typing & Monkey Patching

**Version**: 1.0  
**Last Updated**: 2025-08-01  
**Status**: Experimental

## 🎯 Overview

This directory contains advanced scripts for automatic type hinting and runtime code modification (monkey patching) with comprehensive dry-run validation and safety features.

## ⚡ Quick Start

```bash
# 🔥 Most Common: Auto-add type hints
poetry run python scripts/typing/apply_auto_typing.py --target haive-tools --dry-run
poetry run python scripts/typing/apply_auto_typing.py --target haive-tools --confirm

# 📝 Generate stub files (.pyi) without modifying source
poetry run python scripts/typing/apply_auto_typing.py --target haive-core --stubs-only

# 🐒 Apply runtime patches (experimental)
poetry run python scripts/typing/apply_monkey_patches.py --target haive-agents --dry-run
```

**⚠️ Always run `--dry-run` first!** These scripts modify code and runtime behavior.

## 🔧 Scripts

### 1. `apply_auto_typing.py` - Automatic Type Hints

**Purpose**: Automatically add type hints to Python code using AST analysis and static inference.

**Usage**:

```bash
# Discover functions needing type hints
poetry run python scripts/typing/apply_auto_typing.py --discover --target haive-agents

# Dry-run validation (ALWAYS run first)
poetry run python scripts/typing/apply_auto_typing.py --target haive-core --dry-run

# Apply type hints with confirmation
poetry run python scripts/typing/apply_auto_typing.py --target haive-tools --confirm

# Interactive mode with manual review
poetry run python scripts/typing/apply_auto_typing.py --interactive --target haive-agents

# Generate stub files only (don't modify source code)
poetry run python scripts/typing/apply_auto_typing.py --stubs-only --target haive-tools

# Use mypy stubgen for professional-quality stubs
poetry run python scripts/typing/apply_auto_typing.py --mypy-stubgen --target haive-core
```

**Features**:

- 🔍 **AST-based analysis** - parses Python code to understand structure
- 🧠 **Type inference** - infers types from usage patterns, return statements, method calls
- 🎯 **Confidence scoring** - rates confidence in inferred types (0.0-1.0)
- 📊 **MyPy integration** - validates generated type hints
- 🛡️ **Safe application** - dry-run validation before changes
- 📦 **Import management** - automatically adds required typing imports
- 📝 **Stub file generation** - create `.pyi` files instead of modifying source
- 🔧 **MyPy stubgen integration** - professional-quality stub generation

**Type Inference Strategies**:

```python
# Infers from return statements
def get_name():
    return "Alice"  # → def get_name() -> str:

# Infers from method calls
def process_items(items):
    items.append("new")  # → def process_items(items: List[Any]):

# Infers from comparisons
def check_value(val):
    if val > 0:  # → def check_value(val: int):
        return True
```

**Stub File Generation**:

The script can generate `.pyi` stub files instead of modifying source code:

```python
# Original source file: my_module.py
def process_data(items):
    items.append("processed")
    return len(items)

# Generated stub file: my_module.pyi
"""Stub file for my_module.py"""

from typing import List

def process_data(items: List[Any]) -> int: ...
```

**Two stub generation modes**:

1. **Custom stub generation** (`--stubs-only`) - uses our type inference
2. **MyPy stubgen** (`--mypy-stubgen`) - uses mypy's professional stub generator

```bash
# Custom stubs with inferred types
poetry run python scripts/typing/apply_auto_typing.py --stubs-only --target haive-tools
# Creates: tool_file.pyi with inferred types

# Professional stubs with mypy
poetry run python scripts/typing/apply_auto_typing.py --mypy-stubgen --target haive-core
# Creates: stubs/haive/core/ directory with comprehensive .pyi files
```

### 2. `apply_monkey_patches.py` - Runtime Code Patching

**Purpose**: Apply runtime modifications to classes and functions with validation and rollback capabilities.

**Usage**:

```bash
# Discover patch targets
poetry run python scripts/typing/apply_monkey_patches.py --discover --target haive-agents

# Validate patches (dry-run)
poetry run python scripts/typing/apply_monkey_patches.py --target haive-agents --dry-run

# Apply patches with confirmation
poetry run python scripts/typing/apply_monkey_patches.py --target haive-agents --confirm

# Rollback applied patches
poetry run python scripts/typing/apply_monkey_patches.py --rollback
```

**Features**:

- 🔍 **Automatic target discovery** - finds classes/functions suitable for patching
- 🧪 **Patch validation** - tests patches before applying
- 🛡️ **Risk assessment** - categorizes patches by risk level
- 🔄 **Rollback support** - undo patches if needed
- 📊 **Impact analysis** - reports what will be changed

**Patch Types**:

**Enhancement Patches**:

```python
# Add logging to all agent run() methods
@patch_all_agents
def add_execution_logging(original_run):
    def patched_run(self, *args, **kwargs):
        logger.info(f"🚀 {self.name} starting execution")
        result = original_run(self, *args, **kwargs)
        logger.info(f"✅ {self.name} completed execution")
        return result
    return patched_run
```

**Bug Fix Patches**:

```python
# Fix validation issues in third-party libraries
@patch_library("langchain_core.tools")
def fix_tool_validation_bug(original_method):
    def patched_method(*args, **kwargs):
        try:
            return original_method(*args, **kwargs)
        except ValidationError as e:
            logger.warning(f"Patch caught validation error: {e}")
            return safe_default_response()
    return patched_method
```

**Capability Injection**:

```python
# Add memory capabilities to any agent class
@patch_class("haive.agents.SimpleAgent")
def add_memory_capability(cls):
    def remember(self, key: str, value: Any):
        if not hasattr(self, '_memory'):
            self._memory = {}
        self._memory[key] = value

    cls.remember = remember
    cls.recall = lambda self, key: self._memory.get(key)
    return cls
```

## 🚨 Critical Safety Guidelines

### **ALWAYS Create Backups First**

```bash
# Create safety branch before ANY typing/patching work
git checkout -b typing-safety-$(date +%Y%m%d-%H%M%S)
git add . && git commit -m "Safety backup before typing changes"
git checkout main
```

### **ALWAYS Run Dry-Run First**

```bash
# Auto-typing dry-run
poetry run python scripts/typing/apply_auto_typing.py --target package-name --dry-run

# Monkey patching dry-run
poetry run python scripts/typing/apply_monkey_patches.py --target package-name --dry-run
```

### **ALWAYS Validate After Changes**

```bash
# Check imports still work
poetry run python -c "from haive.package import *; print('✅ Imports work')"

# Run MyPy validation
poetry run mypy packages/package-name/src/

# Run tests
poetry run pytest packages/package-name/tests/ -v
```

## 📊 Type Hint Quality Metrics

### Confidence Levels:

- **0.9-1.0**: High confidence (basic types: `str`, `int`, `float`, `bool`)
- **0.7-0.8**: Medium confidence (specific generic types: `List[str]`)
- **0.5-0.6**: Low confidence (generic types: `List[Any]`, `Dict[str, Any]`)
- **0.0-0.4**: Very low confidence (fallback to `Any`)

### Risk Assessment:

- **Low Risk**: High confidence types, non-critical functions
- **Medium Risk**: Medium confidence types, utility functions
- **High Risk**: Low confidence types, critical methods, core functionality

## 🔄 Rollback Procedures

### Auto-Typing Rollback:

```bash
# Restore from backup
git checkout typing-safety-YYYYMMDD-HHMMSS -- path/to/file.py

# Remove typing imports if they cause issues
# Edit __init__.py and remove: from typing import ...
```

### Monkey Patching Rollback:

```bash
# Use built-in rollback
poetry run python scripts/typing/apply_monkey_patches.py --rollback

# Or restore from backup branch
git checkout typing-safety-YYYYMMDD-HHMMSS -- packages/affected-package/
```

## 📈 Expected Outcomes

### Auto-Typing Benefits:

- ✅ **Better IDE support** - improved autocomplete and error detection
- ✅ **MyPy validation** - catch type errors before runtime
- ✅ **Code documentation** - types serve as inline documentation
- ✅ **Refactoring safety** - type hints help prevent breaking changes

### Monkey Patching Benefits:

- ✅ **Runtime enhancement** - add features without modifying source
- ✅ **Bug fixes** - temporary fixes while waiting for upstream patches
- ✅ **Instrumentation** - add logging/monitoring to any code
- ✅ **Capability injection** - extend existing classes dynamically

## ⚠️ Limitations & Considerations

### Auto-Typing Limitations:

- **Type inference is heuristic** - may not always be correct
- **Complex types are difficult** - falls back to `Any` for complex cases
- **Context-dependent types** - may miss context-specific type requirements
- **Generic constraints** - doesn't infer complex generic constraints

### Monkey Patching Limitations:

- **Runtime only** - patches don't persist across process restarts
- **Testing complexity** - patched code may behave differently in tests
- **Debugging difficulty** - stack traces may be confusing
- **Version sensitivity** - patches may break with library updates

## 🎯 Best Practices

### For Auto-Typing:

1. **Start with high-confidence functions** - build confidence gradually
2. **Review generated types** - don't blindly accept all suggestions
3. **Run MyPy frequently** - catch issues early
4. **Focus on public APIs first** - most important for external users

### For Monkey Patching:

1. **Use sparingly** - prefer proper fixes when possible
2. **Document thoroughly** - explain why patches are needed
3. **Monitor patch effectiveness** - ensure patches are working as expected
4. **Plan for removal** - patches should be temporary

## 📚 Examples

### Typical Auto-Typing Session:

```bash
# 1. Discover opportunities
poetry run python scripts/typing/apply_auto_typing.py --discover --target haive-tools
# Output: Found 23 functions needing type hints

# 2. Validate in dry-run
poetry run python scripts/typing/apply_auto_typing.py --target haive-tools --dry-run
# Output: 18 safe changes, 3 risky changes, 2 syntax errors

# 3. Apply safe changes first
poetry run python scripts/typing/apply_auto_typing.py --target haive-tools --confirm
# Output: Applied type hints to 18 functions

# 4. Validate results
poetry run mypy packages/haive-tools/src/
# Output: Success: no issues found in 45 source files
```

### Typical Monkey Patching Session:

```bash
# 1. Discover patch opportunities
poetry run python scripts/typing/apply_monkey_patches.py --discover --target haive-agents
# Output: Found 12 agent classes suitable for logging enhancement

# 2. Validate patches
poetry run python scripts/typing/apply_monkey_patches.py --target haive-agents --dry-run
# Output: 10 safe patches, 2 high-risk patches

# 3. Apply with caution
poetry run python scripts/typing/apply_monkey_patches.py --target haive-agents --interactive
# Output: Interactive confirmation for each patch

# 4. Test runtime behavior
poetry run python -c "
from haive.agents import SimpleAgent
agent = SimpleAgent(name='test')
result = agent.run('Hello')  # Should show enhanced logging
"
```

---

**Remember**: These are powerful tools that modify code at both static (typing) and runtime (patching) levels. Always use dry-run mode, create backups, and validate thoroughly. The goal is to enhance code quality and capabilities while maintaining stability and correctness.
