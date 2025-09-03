# Sphinx Configuration & Debugging Guide

## Overview

This document explains how we set up and debugged the complete Sphinx documentation system for the Haive AI Agent Framework, including the resolution of major issues like namespace configuration problems and extension conflicts.

## 🏗️ Project Structure

Haive is a **namespaced polyrepo** with 7 packages managed as Git submodules:

```
haive/
├── packages/                    # Each package is its own Git repo
│   ├── haive-core/             # Foundation framework
│   ├── haive-agents/           # Agent implementations  
│   ├── haive-tools/            # Tool integrations
│   ├── haive-games/            # Game environments
│   ├── haive-dataflow/         # Data processing
│   ├── haive-mcp/              # MCP integration
│   └── haive-prebuilt/         # Pre-configured agents
└── docs/
    └── source/
        └── conf.py             # THIS FILE - Master Sphinx config
```

## 🎯 Key Configuration Achievements

### 1. **All 7 Packages Documented**
**Problem**: Initially only `haive-core` was being documented  
**Root Cause**: Incorrect namespace paths pointing to `src/` instead of `src/haive/packagename`  
**Solution**: Fixed `ALL_PACKAGES` configuration

```python
# ❌ WRONG - Only points to src level
ALL_PACKAGES = {
    "core": str(packages_dir / "haive-core/src"),
    # ... other packages
}

# ✅ CORRECT - Points to actual package directories
ALL_PACKAGES = {
    "core": str(packages_dir / "haive-core/src/haive/core"),
    "agents": str(packages_dir / "haive-agents/src/haive/agents"),
    "tools": str(packages_dir / "haive-tools/src/haive/tools"),
    "games": str(packages_dir / "haive-games/src/haive/games"),
    "dataflow": str(packages_dir / "haive-dataflow/src/haive/dataflow"),
    "mcp": str(packages_dir / "haive-mcp/src/haive/mcp"),
    "prebuilt": str(packages_dir / "haive-prebuilt/src/haive/prebuilt"),
}
```

### 2. **Extension Compatibility Issues Resolved**
**Problem**: Multiple extension conflicts causing build failures  
**Solutions Applied**:

```python
# Extensions that were problematic and disabled:
# "sphinx_math_dollar",           # Error: pending_xref_condition node type
# "sphinx_codeautolink",          # Error: 'module' object is not callable  
# "sphinx_gallery.gen_gallery",  # Missing GALLERY_HEADER issues
# "sphinxcontrib.actdiag",        # Package not installed

# Extensions that needed configuration:
"sphinx_tippy",                   # Added proper tippy config to prevent KeyError
```

### 3. **Duplicate API Paths Eliminated** 
**Problem**: Documentation generated both `api/core/` AND `api/src/haive/core/`  
**Root Cause**: `autoapi_python_use_implicit_namespaces = True`  
**Solution**: Changed to `False` since we don't use PEP 420 namespace packages

### 4. **Comprehensive File Filtering**
**Added**: Extensive `autoapi_ignore` patterns to exclude tests, examples, and artifacts

## 🔧 Build System Configuration

### Core Settings
```python
# Project detection - ALL 7 packages
SPHINX_PACKAGES = os.environ.get("SPHINX_PACKAGES", "all")

# AutoAPI - Document all Python packages automatically
extensions = [
    "autoapi.extension",  # CRITICAL: Must be first
    # ... 83+ other extensions
]

# Theme - Professional documentation theme
html_theme = "pydata_sphinx_theme"  # Chosen after testing multiple themes
```

### Extension Management (83+ Extensions)
The configuration includes comprehensive extension support:
- **Core Sphinx**: autodoc, autosummary, napoleon, viewcode, intersphinx
- **API Generation**: autoapi (primary), sphinx_automodapi
- **Enhanced Features**: sphinx_design, sphinx_copybutton, sphinx_togglebutton
- **Diagrams**: mermaid, plantuml, graphviz, inheritance diagrams
- **Content**: MyST parser for Markdown, sphinx_tabs, sphinx_needs
- **Quality**: spelling checker, link checking, automated testing

### Environment Variables
```bash
# Build specific packages only
SPHINX_PACKAGES="core,agents" 

# Skip computational examples  
SPHINX_DISABLE_EXAMPLES=1

# Use minimal profile for faster builds
SPHINX_PROFILE=minimal

# Control import diagnostics
SPHINX_FAST_IMPORTS=1
```

## 🐛 Major Issues Resolved

### Issue 1: Missing Namespace Configuration
**Symptom**: Only haive-core package documented, others missing  
**Diagnosis**: `autoapi_dirs` pointing to wrong directory level  
**Resolution**: Updated paths to include full namespace hierarchy  
**Verification**: All 7 packages now generate documentation

### Issue 2: Extension Conflicts  
**Symptom**: Build failures with various extension errors  
**Diagnosis**: Incompatible or missing extensions  
**Resolution**: 
- Disabled problematic extensions with detailed comments
- Added proper configuration for remaining extensions
- 83 of 89 extensions now working

### Issue 3: Duplicate API Structure
**Symptom**: Both `api/core/` and `api/src/haive/core/` generated  
**Diagnosis**: `autoapi_python_use_implicit_namespaces = True`  
**Resolution**: Set to `False` + proper path configuration  
**Verification**: Clean single API structure

### Issue 4: Memory and Performance Issues  
**Symptom**: Build taking 30+ minutes, 5GB+ memory usage  
**Optimization**: 
- Added comprehensive ignore patterns for tests/examples
- Configured extension-specific optimizations
- Provided environment variable controls

## 🚀 Build Commands & Debugging

### Standard Build Process
```bash
# Basic build
poetry run python -m sphinx -b html docs/source docs/build/html

# Verbose build (recommended)
poetry run python -m sphinx -b html docs/source docs/build/html -v

# Background build with monitoring
nohup poetry run python -m sphinx -b html docs/source docs/build/html -v > /tmp/sphinx_build.log 2>&1 &
tail -f /tmp/sphinx_build.log
```

### Configuration Testing
```bash
# Test configuration loads correctly
poetry run python -c "
import sys
sys.path.insert(0, 'docs/source')
from conf import ALL_PACKAGES, extensions
print(f'✅ {len(ALL_PACKAGES)} packages, {len(extensions)} extensions')
"

# Test specific extension availability
poetry run python -c "import sphinx_tippy; print('✅ tippy available')"
```

### Build Monitoring
```bash
# Check process status
ps aux | grep sphinx

# Monitor progress
watch -n 30 'wc -l /tmp/sphinx_build.log'

# Check generated files
find docs/build/html -name "*.html" | wc -l
```

## 📊 Build Performance

### Expected Build Times
- **5 minutes**: 10-30% (AutoAPI reading source files)
- **10 minutes**: 40-70% (Processing documentation)  
- **15-20 minutes**: 80-100% (HTML generation)

### Success Metrics  
- **HTML Files**: 5,000+ files generated
- **Packages**: All 7 packages documented
- **API Coverage**: Complete module/class/function documentation
- **Memory Usage**: ~5-6GB peak during build

## 🔍 Troubleshooting Guide

### Common Issues
1. **Extension Errors**: Check extension installation and configuration
2. **Import Errors**: Verify package imports work with poetry run
3. **Memory Issues**: Use SPHINX_PROFILE=minimal for limited resources  
4. **Path Issues**: Ensure autoapi_dirs points to package directories, not parent dirs

### Debug Commands  
```bash
# Check imports work
poetry run python -c "
import sys
sys.path.insert(0, 'packages/haive-core/src')
import haive.core; print('✅ Core imports OK')
"

# Find errors in build log
grep -i error /tmp/sphinx_build.log | tail -10

# Check extension conflicts
poetry run python -c "
try:
    import problematic_extension
    print('✅ Available')
except ImportError as e:
    print(f'❌ Missing: {e}')
"
```

## 📁 File Structure After Build

```
docs/build/html/
├── index.html                  # Main documentation page
├── api/                        # Auto-generated API docs
│   ├── core/                   # haive-core package docs
│   ├── agents/                 # haive-agents package docs  
│   ├── tools/                  # haive-tools package docs
│   ├── games/                  # haive-games package docs
│   ├── dataflow/               # haive-dataflow package docs
│   ├── mcp/                    # haive-mcp package docs
│   └── prebuilt/               # haive-prebuilt package docs
├── _static/                    # CSS, JS, images
├── _sources/                   # RST source files
└── genindex.html               # Generated index
```

## 🎯 Configuration Philosophy

1. **Comprehensive Documentation**: Document everything automatically
2. **Professional Appearance**: Clean, modern theme with good navigation
3. **Developer Friendly**: Include source links, search, and cross-references  
4. **Performance Balanced**: Full features but with reasonable build times
5. **Maintainable**: Clear configuration with extensive commenting

## 📚 Extension Categories

### Essential (Always Enabled)
- `autoapi.extension` - Primary API documentation  
- `sphinx.ext.autodoc` - Docstring processing
- `sphinx.ext.napoleon` - Google/NumPy docstring support
- `sphinx.ext.viewcode` - Source code links

### Enhanced Features  
- `sphinx_design` - Modern UI components
- `sphinx_copybutton` - Copy code button
- `myst_parser` - Markdown support
- `sphinx_tabs.tabs` - Tabbed content

### Specialized
- `sphinxcontrib.mermaid` - Diagram generation
- `sphinx.ext.intersphinx` - Cross-project linking  
- `sphinx_tippy` - Enhanced tooltips
- `sphinx.ext.inheritance_diagram` - Class hierarchy visualization

## 🔄 Continuous Maintenance

### Regular Tasks
1. **Extension Updates**: Keep extensions compatible with latest Sphinx
2. **Performance Monitoring**: Track build times and memory usage
3. **Content Quality**: Review auto-generated documentation quality
4. **Link Checking**: Verify external links remain valid

### Configuration Evolution
- The configuration is designed to be modular and maintainable
- Extensions can be easily disabled/enabled via environment variables
- Profile system allows different build configurations for different use cases

---

**Last Updated**: 2025-08-06  
**Sphinx Version**: 8.2.3  
**Python Version**: 3.12.3  
**Build Status**: ✅ All 7 packages successfully documented