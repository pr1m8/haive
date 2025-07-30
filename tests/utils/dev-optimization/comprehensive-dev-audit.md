# Comprehensive Dev Dependencies Audit

Generated: $(date)

## 🎯 **Objective**

Before optimizing any package, analyze ALL dev tools for redundancies, gaps, and optimization opportunities.

## 📊 **Current Root Tooling Analysis**

### **Linting & Formatting**

- ✅ **ruff** (^0.11.6) - Modern unified linter
- ❌ **black** (likely in packages) - REDUNDANT with ruff format
- ❌ **isort** (likely in packages) - REDUNDANT with ruff isort
- ✅ **pyright** (^1.1.399) - Type checking

### **Documentation & Docstrings**

- ✅ **interrogate** (^1.5.0) - Missing docstring detection
- ❌ **pydocstyle** (^6.3.0) - REDUNDANT with ruff pydocstyle
- ✅ **darglint** (^1.8.1) - Docstring-code sync validation
- ❓ **docformatter** - MISSING (auto-format docstrings)

### **Sphinx Ecosystem (30+ packages!)**

```toml
sphinx = "^8.0.0"                    # Core
sphinx-autoapi = "^3.6.0"          # API docs
sphinx-autodoc-typehints = "^3.1.0" # Type hints
sphinx-rtd-theme = "^3.0.2"        # Theme
sphinx-autobuild = "^2024.10.3"    # Live rebuild
sphinx-design = "^0.6.1"           # Design components
sphinx-tabs = "^3.4.7"             # Tabs
sphinx-copybutton = "^0.5.2"       # Copy buttons
sphinx-togglebutton = "^0.3.2"     # Toggle buttons
# ... 20+ more packages
```

**Analysis:**

- 🔴 **MASSIVE OVERKILL** for most projects
- 🟡 **Core need**: sphinx + autoapi + theme + napoleon
- 🟡 **Nice to have**: autobuild, copybutton
- 🔴 **Probably unnecessary**: 15+ specialty packages

### **Testing & Coverage**

- ✅ **pytest** (^8.3.5) - Core testing
- ✅ **coverage** (^7.8.0) - Coverage analysis
- ✅ **pytest-html** (^4.1.1) - HTML reports
- ✅ **pytest-sugar** (^1.0.0) - Better output
- ✅ **pytest-clarity** (^1.0.1) - Better diffs

### **Type Annotation Tools**

- ✅ **monkeytype** (in packages) - Runtime type collection
- ❓ **autotyping** - MISSING (static type inference)

### **Performance & Debugging**

- ✅ **py-spy** (^0.4.0) - Profiling
- ✅ **memray** (^1.17.1) - Memory profiling
- ✅ **viztracer** (^1.0.3) - Tracing
- ✅ **ipdb** (^0.13.13) - Enhanced debugger

## 🔍 **Per-Package Analysis**

### **haive-games Current State:**

```toml
[tool.poetry.group.dev.dependencies]
pytest = "^8.3.5"
black = "^25.1.0"      # ❌ REDUNDANT with ruff
isort = "^6.0.1"       # ❌ REDUNDANT with ruff
mypy = "^1.15.0"       # ⚠️  vs pyright?
monkeytype = "^23.3.0" # ✅ Good
```

**Issues:**

- ❌ black/isort redundancy
- ⚠️ mypy vs pyright decision needed
- ❓ Missing ruff
- ❓ Missing docstring tools

## 🎯 **Optimization Strategy**

### **Phase 1: Standardize Core Tools**

1. **Unified linting**: ruff (replace black + isort)
2. **Type checking**: Choose pyright OR mypy (not both)
3. **Docstrings**: ruff pydocstyle (remove pydocstyle package)
4. **Add missing**: docformatter, autotyping

### **Phase 2: Sphinx Optimization**

1. **Core only**: sphinx + autoapi + theme + napoleon
2. **Development**: + autobuild + copybutton
3. **Remove**: 15+ specialty packages

### **Phase 3: Per-Package Application**

1. **Templates**: Create optimized pyproject.toml templates
2. **Safe application**: Use our tracking script
3. **Testing**: Verify each package works

## 🛠️ **Recommended Unified Dev Stack**

### **Essential (Every Package)**

```toml
[tool.poetry.group.dev.dependencies]
# Linting & Formatting
ruff = "^0.11.6"                    # Unified linter + formatter
pyright = "^1.1.399"               # Type checking

# Testing
pytest = "^8.3.5"
coverage = "^7.8.0"

# Type annotation generation
monkeytype = "^23.3.0"
autotyping = "^23.3.0"

# Docstring tools
docformatter = "^1.7.5"           # Auto-format docstrings
darglint = "^1.8.1"               # Docstring validation
interrogate = "^1.5.0"            # Missing docstring detection
```

### **Documentation (Root Only)**

```toml
[tool.poetry.group.docs.dependencies]
# Core Sphinx
sphinx = "^8.0.0"
sphinx-autoapi = "^3.6.0"         # API docs
sphinx-autodoc-typehints = "^3.1.0"
sphinx-rtd-theme = "^3.0.2"       # Theme

# Development convenience
sphinx-autobuild = "^2024.10.3"   # Live rebuild
sphinx-copybutton = "^0.5.2"      # Copy buttons
```

### **Advanced (Root Only)**

```toml
[tool.poetry.group.advanced.dependencies]
# Performance profiling
py-spy = "^0.4.0"
memray = "^1.17.1"
viztracer = "^1.0.3"

# Enhanced debugging
ipdb = "^0.13.13"

# Security
bandit = "^1.8.3"
```

## 📋 **Action Items**

1. **Audit individual packages** for redundancies
2. **Create optimized templates** for different package types
3. **Test unified configuration** on haive-games
4. **Document migration strategy** for each tool
5. **Create rollback procedures** for each change

## ⚠️ **Critical Questions to Answer**

1. **Type checking**: pyright vs mypy strategy?
2. **Sphinx scope**: What docs features are actually needed?
3. **Package inheritance**: Should packages inherit root tools?
4. **Testing strategy**: Package-specific vs monorepo testing?
5. **Performance impact**: Tool startup time comparisons?

---

**Next Step**: Answer critical questions before proceeding with any optimization.
