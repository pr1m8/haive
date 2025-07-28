# Type Annotation & Formatting Tools Inventory - Haive Project

**Date**: 2025-07-28
**Purpose**: Complete inventory of type hint and code formatting tools available
**Status**: Comprehensive analysis of installed vs missing tools

## 🔍 **INSTALLED Type Annotation Tools**

### ✅ **Primary Type Tools (Active)**

| Tool           | Version | Purpose                   | Status           | Usage                                            |
| -------------- | ------- | ------------------------- | ---------------- | ------------------------------------------------ |
| **mypy**       | 1.15.0  | Static type checker       | ✅ **Active**    | `poetry run mypy packages/`                      |
| **monkeytype** | 23.3.0  | Runtime type collection   | 🔄 **Available** | Generate types from runtime                      |
| **pyannotate** | 1.2.0   | Type annotation generator | ❌ **BROKEN**    | `ModuleNotFoundError: No module named 'lib2to3'` |

### ✅ **Type Support Libraries**

| Tool                   | Version | Purpose                     |
| ---------------------- | ------- | --------------------------- |
| **annotated-types**    | 0.7.0   | Enhanced type annotations   |
| **mypy-extensions**    | 1.0.0   | Extended mypy functionality |
| **eval-type-backport** | 0.2.2   | Backport of eval support    |

### ✅ **Type Stub Files (Active)**

| Package                   | Version         | Coverage           |
| ------------------------- | --------------- | ------------------ |
| **types-python-dateutil** | 2.9.0.20250708  | datetime utilities |
| **types-pyyaml**          | 6.0.12.20250516 | YAML processing    |
| **types-requests**        | 2.32.0.20250328 | HTTP requests      |
| **types-setuptools**      | 80.9.0.20250529 | Package setup      |
| **types-toml**            | 0.10.8.20240310 | TOML configuration |
| **types-urllib3**         | 1.26.25.14      | URL utilities      |

## 🎨 **INSTALLED Code Formatting Tools**

### ✅ **Primary Formatters**

| Tool         | Version | Purpose               | Configuration              | Usage                |
| ------------ | ------- | --------------------- | -------------------------- | -------------------- |
| **autopep8** | 2.3.2   | PEP 8 auto-formatter  | ⚠️ **No config**           | Fix PEP 8 violations |
| **black**    | 25.1.0  | Opinionated formatter | ⚠️ **Conflicts with ruff** | NOT recommended      |
| **ruff**     | ^0.11.6 | Fast all-in-one       | ✅ **Configured**          | Primary formatter    |

### ✅ **Documentation Formatters**

| Tool             | Version | Purpose             | Status           |
| ---------------- | ------- | ------------------- | ---------------- | ----------------------------- |
| **blacken-docs** | 1.19.1  | Format code in docs | 🔄 **Available** | Format examples in docstrings |

## 📊 **Type Annotation Capabilities Matrix**

### **What We CAN Do (Installed Tools)**

| Task                        | Tool         | Command                                  | Effectiveness      |
| --------------------------- | ------------ | ---------------------------------------- | ------------------ |
| **Static type checking**    | mypy         | `poetry run mypy packages/`              | ✅ **Excellent**   |
| **Runtime type collection** | monkeytype   | `poetry run monkeytype run script.py`    | ✅ **Good**        |
| **Type stub generation**    | monkeytype   | `poetry run monkeytype stub module`      | ✅ **Good**        |
| **Type application**        | monkeytype   | `poetry run monkeytype apply module`     | ✅ **Good**        |
| **PEP 8 formatting**        | autopep8     | `poetry run autopep8 --in-place file.py` | ✅ **Good**        |
| **Code in docs formatting** | blacken-docs | `poetry run blacken-docs docs/*.md`      | ✅ **Specialized** |

### **What We CANNOT Do (Missing/Broken)**

| Task                          | Missing Tool | Why We Need It          | Alternative          |
| ----------------------------- | ------------ | ----------------------- | -------------------- |
| **Generate from source**      | pyannotate   | ❌ **BROKEN** (lib2to3) | Use monkeytype       |
| **Automatic type inference**  | pytype       | Not installed           | Manual with mypy     |
| **Type coverage measurement** | typecov      | Not installed           | Manual mypy analysis |
| **Type hint removal**         | strip-hints  | Not installed           | Manual editing       |

## 🚀 **Recommended Type Annotation Workflow**

### **Phase 1: Assessment**

```bash
# Check current type coverage
poetry run mypy packages/haive-games/src/ --strict

# Count type annotations
find packages/haive-games/src/ -name "*.py" -exec grep -l "-> " {} \; | wc -l
```

### **Phase 2: Runtime Collection (monkeytype)**

```bash
# Collect runtime types
poetry run monkeytype run packages/haive-games/src/haive/games/example.py

# Generate stubs
poetry run monkeytype stub haive.games.clue.controller

# Apply to source
poetry run monkeytype apply haive.games.clue.controller
```

### **Phase 3: Manual Addition**

```bash
# Add types to functions missing them
# Focus on public APIs first
```

### **Phase 4: Validation**

```bash
# Verify with mypy
poetry run mypy packages/haive-games/src/ --strict
```

## 📋 **autopep8 Configuration & Usage**

### **Current Status: NO Configuration**

- ⚠️ **No `[tool.autopep8]` in pyproject.toml**
- ⚠️ **No `.autopep8` file**
- ⚠️ **Using default settings**

### **Recommended Configuration**

```toml
[tool.autopep8]
max_line_length = 100
ignore = ["E501", "W503"]  # Long lines handled by ruff, line breaks
aggressive = 1
experimental = false
```

### **Safe Usage Patterns**

```bash
# Preview changes first
poetry run autopep8 --diff packages/haive-games/src/haive/games/clue/

# Apply to single file
poetry run autopep8 --in-place packages/haive-games/src/haive/games/clue/controller.py

# Apply to directory (after preview)
poetry run autopep8 --in-place --recursive packages/haive-games/src/
```

### **Integration with Documentation Pipeline**

```bash
# Enhanced pipeline with autopep8:
# 1. autoflake (remove unused imports)
# 2. autopep8 (PEP 8 compliance)
# 3. pydocstringformatter (docstring formatting)
# 4. ruff format (final formatting)
# 5. mypy (type checking)
```

## 🔄 **monkeytype Workflow for Missing Type Hints**

### **Setup**

```bash
# Verify installation
poetry run monkeytype --version

# Create collection script
cat > collect_types.py << 'EOF'
#!/usr/bin/env python3
"""Script to collect runtime types from haive-games."""

import sys
sys.path.insert(0, 'packages/haive-games/src')

# Import and run modules to collect types
from haive.games.clue.controller import ClueGameController
from haive.games.clue.state_manager import ClueStateManager

# Example usage to collect types
controller = ClueGameController(["Alice", "Bob"])
game_state = controller.get_game_state()
EOF
```

### **Collection Process**

```bash
# Run with monkeytype to collect types
poetry run monkeytype run collect_types.py

# Check collected data
poetry run monkeytype list-modules

# Generate stub for specific module
poetry run monkeytype stub haive.games.clue.controller

# Review stub file
cat out/haive/games/clue/controller.pyi

# Apply if looks good
poetry run monkeytype apply haive.games.clue.controller
```

## 🎯 **blacken-docs for Documentation Code**

### **Purpose**

Format Python code blocks within docstrings and markdown files.

### **Usage Examples**

```bash
# Format code in docstrings
poetry run blacken-docs packages/haive-games/src/**/*.py

# Format code in markdown docs
poetry run blacken-docs project_docs/**/*.md

# Preview changes
poetry run blacken-docs --diff packages/haive-games/src/**/*.py
```

### **Integration Point**

```bash
# Add to documentation pipeline after docstring formatting:
# 1. pydocstringformatter (docstring structure)
# 2. blacken-docs (code examples in docstrings)
# 3. ruff format (final pass)
```

## 📊 **Tool Effectiveness Analysis**

### **Type Coverage Current State**

```bash
# Run this to get baseline
poetry run mypy packages/haive-games/src/ --strict 2>&1 | grep -c "error:"
```

### **Expected Improvements with Full Workflow**

| Phase               | Tool          | Expected Impact                     |
| ------------------- | ------------- | ----------------------------------- |
| **Assessment**      | mypy --strict | Identify 200-500 missing type hints |
| **Auto-collection** | monkeytype    | Add 50-100 function signatures      |
| **Manual addition** | Hand coding   | Add 100-200 critical type hints     |
| **Code formatting** | autopep8      | Fix 50-100 PEP 8 violations         |
| **Doc code format** | blacken-docs  | Clean up 20-50 code examples        |

## 🚨 **Tool Conflicts & Solutions**

### **Potential Conflicts**

1. **black vs ruff**: Both format code differently
2. **autopep8 vs ruff**: May make conflicting changes
3. **Multiple type tools**: Different inference approaches

### **Resolution Strategy**

```bash
# Recommended order to avoid conflicts:
# 1. autopep8 (PEP 8 compliance)
# 2. ruff format (primary formatter)
# 3. mypy (type checking)
# 4. blacken-docs (documentation code)

# DO NOT USE black (conflicts with ruff)
```

## 📋 **Missing Tools Worth Adding**

### **High Value Additions**

```bash
# Type coverage measurement
poetry add --group dev typecov

# Type hint removal (for testing)
poetry add --group dev strip-hints

# Advanced type inference
poetry add --group dev pytype  # Google's type inference
```

### **Lower Priority**

```bash
# Type annotation helpers
poetry add --group dev typing-extensions  # May already be installed via dependencies
poetry add --group dev typing-inspect     # Runtime type inspection
```

## 🎯 **IMMEDIATE ACTIONABLE RECOMMENDATIONS**

### **1. Test autopep8 on haive-games (15 minutes)**

```bash
# Preview what autopep8 would fix
poetry run autopep8 --diff --aggressive packages/haive-games/src/ | head -50

# Count potential fixes
poetry run autopep8 --diff packages/haive-games/src/ 2>/dev/null | grep -c "^-.*\|^+.*"
```

### **2. Run monkeytype collection (30 minutes)**

```bash
# Create type collection script for clue game
# Run collection
# Generate and review stubs
# Apply selective type improvements
```

### **3. Configure autopep8 properly (10 minutes)**

```bash
# Add autopep8 configuration to pyproject.toml
# Test configuration works correctly
```

### **4. Integrate into documentation pipeline (20 minutes)**

```bash
# Create enhanced 7-tool pipeline:
# autoflake → autopep8 → pydocstringformatter → blacken-docs → ruff format → mypy → interrogate
```

---

## 🏆 **SUMMARY**

**We have a RICH type annotation and formatting toolset:**

- ✅ **mypy** for static checking
- ✅ **monkeytype** for runtime collection
- ✅ **autopep8** for PEP 8 formatting (unconfigured)
- ✅ **blacken-docs** for documentation code
- ❌ **pyannotate** is broken (use monkeytype instead)

**The tools exist to significantly improve type annotation coverage and code formatting quality!**
