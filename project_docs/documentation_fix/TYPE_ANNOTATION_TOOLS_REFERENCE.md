# Type Annotation Tools Reference Guide

**Created**: 2025-07-28
**Purpose**: Complete reference for all type annotation and documentation tools in Haive
**Status**: Comprehensive tool inventory and usage guide

## 📊 Tool Categories & Purpose

### 🔍 **Static Type Checkers**

Check types without running code - analyze source code statically

### 🏃 **Runtime Type Collectors**

Observe actual types during code execution to generate annotations

### ✨ **Annotation Generators**

Automatically add simple type hints based on code patterns

### 📝 **Documentation Tools**

Format, validate, and measure documentation quality

---

## 🛠️ Available Tools Inventory

### ✅ **WORKING TOOLS**

#### **mypy** (1.15.0) - Static Type Checker

- **Purpose**: Primary static type checker for Python
- **What it does**: Analyzes code without running it to find type errors
- **When to use**: Always - as your main type validation tool
- **Usage**:
  ```bash
  poetry run mypy packages/haive-core/src/
  poetry run mypy --config-file pyproject.toml packages/
  ```
- **Configuration**: Already configured in pyproject.toml
- **Pros**: Most mature, widely supported, IDE integration
- **Cons**: Requires existing type annotations to be effective

#### **autotyping** (24.9.0) - Simple Annotation Generator

- **Purpose**: Automatically add basic return type annotations
- **What it does**: Infers simple types (bool, None, Optional) from code context
- **When to use**: Quick wins for functions missing return type annotations
- **Usage**:

  ```bash
  # Add basic return types
  poetry run autotyping --none-return --scalar-return packages/haive-core/src/

  # Add parameter types for common patterns
  poetry run autotyping --bool-param --str-param packages/haive-core/src/
  ```

- **Pros**: Fast, safe, handles common cases automatically
- **Cons**: Limited to simple types, doesn't handle complex generics

#### **monkeytype** (23.3.0) - Runtime Type Collector

- **Purpose**: Generate type annotations from actual runtime usage
- **What it does**: Records function calls and return types during execution
- **When to use**: For complex functions where static analysis isn't enough
- **Usage**:

  ```bash
  # 1. Run code to collect types
  poetry run monkeytype run your_script.py

  # 2. Generate stub file
  poetry run monkeytype stub your.module

  # 3. Apply to source code
  poetry run monkeytype apply your.module
  ```

- **Pros**: Captures actual usage patterns, works with complex types
- **Cons**: Requires running code, only captures observed paths

#### **docformatter** (1.7.7) - Docstring Formatter

- **Purpose**: Format existing docstrings to PEP 257 standards
- **What it does**: Wraps lines, fixes whitespace, standardizes format
- **When to use**: To clean up existing docstring formatting
- **Usage**:

  ```bash
  # Preview changes
  poetry run docformatter --diff packages/haive-core/src/

  # Apply formatting
  poetry run docformatter --in-place --recursive packages/haive-core/src/
  ```

- **Pros**: Safe, predictable, preserves content
- **Cons**: Only formats existing docstrings, doesn't add new ones

#### **pydocstyle** (6.3.0) - Docstring Style Checker

- **Purpose**: Validate docstrings follow Google/NumPy/PEP 257 conventions
- **What it does**: Checks docstring format, missing sections, style compliance
- **When to use**: To validate docstring quality and consistency
- **Usage**:

  ```bash
  # Check Google style compliance
  poetry run pydocstyle packages/ --convention=google

  # Count violations
  poetry run pydocstyle packages/ --count
  ```

- **Configuration**: Supports pyproject.toml with `pydocstyle[toml]`
- **Pros**: Comprehensive style checking, configurable
- **Cons**: Only validates, doesn't fix issues

#### **darglint** (1.8.1) - Semantic Docstring Validator

- **Purpose**: Ensure docstring Args/Returns match actual function signature
- **What it does**: Validates docstring sections match the code semantically
- **When to use**: To catch mismatches between docs and implementation
- **Usage**:
  ```bash
  # Check semantic correctness
  poetry run darglint packages/haive-core/src/ --strictness=short
  ```
- **Configuration**: Uses `.darglint` file (no pyproject.toml support)
- **Pros**: Catches documentation bugs, semantic validation
- **Cons**: No pyproject.toml support, archived project

#### **interrogate** (1.5.0) - Documentation Coverage Measurement

- **Purpose**: Measure percentage of code with docstrings
- **What it does**: Counts missing docstrings, generates coverage reports and badges
- **When to use**: To track documentation progress and set coverage goals
- **Usage**:

  ```bash
  # Measure coverage
  poetry run interrogate packages/ --verbose

  # Generate badge
  poetry run interrogate packages/ --generate-badge docs/coverage.svg
  ```

- **Configuration**: Full pyproject.toml support
- **Pros**: Great reporting, badge generation, configurable
- **Cons**: Only measures quantity, not quality

#### **autoflake** (2.3.1) - Import Cleaner

- **Purpose**: Remove unused imports and variables
- **What it does**: Cleans up code by removing unnecessary imports
- **When to use**: Before applying other tools to clean up the codebase
- **Usage**:

  ```bash
  # Check what would be removed
  poetry run autoflake --check --remove-all-unused-imports packages/

  # Apply cleanup
  poetry run autoflake --in-place --remove-all-unused-imports --recursive packages/
  ```

- **Pros**: Safe cleanup, improves code quality
- **Cons**: Limited scope (only imports/unused variables)

#### **ruff** (0.11.6) - Fast All-in-One Linter

- **Purpose**: Fast linter with integrated docstring checking
- **What it does**: Combines multiple linting rules including docstring validation
- **When to use**: As primary linter for fast, comprehensive checking
- **Usage**:

  ```bash
  # Check docstring rules
  poetry run ruff check packages/ --select=D

  # Auto-fix issues
  poetry run ruff check packages/ --select=D --fix
  ```

- **Configuration**: Already configured for Google style in pyproject.toml
- **Pros**: Very fast, integrated approach, good auto-fixes
- **Cons**: Less specialized than dedicated tools

### ❌ **BROKEN TOOLS**

#### **pyannotate** (1.2.0) - Runtime Type Collector (Dropbox)

- **Purpose**: Generate type annotations from test runs (similar to monkeytype)
- **Status**: ❌ BROKEN - Missing lib2to3 dependency
- **Error**: `ModuleNotFoundError: No module named 'lib2to3'`
- **Solution**: Use monkeytype instead (same purpose, actively maintained)

---

## 🎯 **Tool Selection Matrix**

### **What Tool for What Purpose**

| Goal                           | Primary Tool | Backup/Alternative   | Notes                             |
| ------------------------------ | ------------ | -------------------- | --------------------------------- |
| **Check existing types**       | mypy         | ruff (--select=ANN)  | mypy is more comprehensive        |
| **Add simple return types**    | autotyping   | Manual addition      | Quick wins for bool/None/Optional |
| **Add complex types**          | monkeytype   | Manual analysis      | Requires running code             |
| **Format existing docstrings** | docformatter | ruff format          | docformatter is specialized       |
| **Check docstring style**      | pydocstyle   | ruff (--select=D)    | pydocstyle more detailed          |
| **Validate Args/Returns**      | darglint     | Manual review        | No good alternative               |
| **Measure doc coverage**       | interrogate  | Manual counting      | Only tool for this                |
| **Clean imports**              | autoflake    | ruff (--select=F401) | Both work well                    |
| **General linting**            | ruff         | Multiple tools       | Fastest integrated approach       |

### **Workflow Combinations**

#### **Quick Documentation Cleanup**

```bash
1. autoflake (clean imports)
2. docformatter (format docstrings)
3. pydocstyle (check compliance)
```

#### **Type Annotation Workflow**

```bash
1. autotyping (simple types)
2. mypy (check existing)
3. monkeytype (complex cases)
4. mypy (final validation)
```

#### **Complete Documentation Audit**

```bash
1. interrogate (measure baseline)
2. pydocstyle (style issues)
3. darglint (semantic issues)
4. Document findings and prioritize fixes
```

---

## 🚀 **Execution Order Recommendations**

### **Phase 1: Cleanup**

- autoflake (remove unused imports)
- docformatter (standardize existing docstrings)

### **Phase 2: Basic Type Annotations**

- autotyping (add simple return types)
- mypy (check for obvious type errors)

### **Phase 3: Documentation Validation**

- pydocstyle (check Google style compliance)
- darglint (validate Args/Returns)
- interrogate (measure coverage)

### **Phase 4: Advanced Type Work**

- monkeytype (for complex functions, if runnable)
- mypy (comprehensive type checking)

### **Phase 5: Measurement**

- interrogate (final coverage measurement)
- Generate badges and reports

---

## 📋 **Configuration Status**

### **Configured in pyproject.toml**

✅ mypy, ruff, interrogate (planned)

### **Separate Config Files Needed**

⚠️ darglint (uses .darglint file)

### **No Configuration Required**

✅ autotyping, monkeytype, docformatter, autoflake

### **Broken/Needs Fixing**

❌ pyannotate (lib2to3 dependency issue)

---

## 🎯 **Next Steps**

1. **Fix broken tools** (pyannotate or remove it)
2. **Add missing pyproject.toml configurations** (interrogate, pydocstyle)
3. **Test each tool individually** on sample files
4. **Create automated workflow scripts** for common combinations
5. **Document tool-specific best practices** and gotchas

This reference provides the foundation for systematic documentation and type annotation improvement across the Haive codebase.
