# Auto-Build Implementation with Smart Caching

## Overview
Implemented comprehensive auto-build system for Haive documentation that:
1. **Generates manual module pages** automatically from package structure
2. **Smart caching** - only regenerates when source files change
3. **Separate example runs** - don't rebuild docs when only running examples
4. **Gallery + Automodule** - maintains visual galleries while ensuring automodule works

## New Nox Sessions

### 1. `nox -s docs_auto` (Primary Command)
**Smart auto-build with caching:**
- ✅ **Detects changes**: Compares source file timestamps to last generation
- ✅ **Generates modules**: Creates manual `.rst` files for all packages
- ✅ **Builds docs**: Full Sphinx build with both galleries and automodule
- ✅ **Caching**: Only regenerates when needed
- ✅ **Performance**: Skips generation if modules are up-to-date

### 2. `nox -s docs_regenerate`
**Force fresh module generation:**
- 🗑️ Removes existing module files
- 🏗️ Generates fresh documentation for all packages
- ✨ Creates marker file for timestamp tracking

### 3. `nox -s docs_examples`
**Run examples separately:**
- 🏃 Executes documentation example scripts
- 📁 Scans `examples/` directory for Python files
- ⚠️ Reports failures but continues
- 🔄 No documentation rebuild

## Module Generation Script

**Location**: `/scripts/generate_modules.py`

### Features:
- **Package scanning**: Automatically discovers all Python modules
- **Smart filtering**: Skips test files, cache, build artifacts
- **Import validation**: Checks if modules can be imported
- **Comprehensive RST**: Full automodule directives with all options
- **Error handling**: Continues on failures, reports issues

### Template Format:
```rst
haive.core.engine
=================

.. py:module:: haive.core.engine

.. currentmodule:: haive.core.engine

.. raw:: html

   <div class="module-path">
      <code>haive.core.engine</code>
   </div>

.. automodule:: haive.core.engine
   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:
   :special-members: __init__, __call__, __new__
   :imported-members:
   :exclude-members: logger
```

## Smart Caching System

### Timestamp-Based Detection:
1. **Marker file**: `.generated` in modules directory
2. **Source scanning**: Checks all `.py` files in packages
3. **Comparison**: Only regenerates if source files newer than marker
4. **Performance**: Avoids unnecessary regeneration

### Cache Invalidation:
- ✅ New Python files added to packages
- ✅ Existing Python files modified
- ✅ Package structure changes
- ✅ Manual regeneration requested

## Gallery + Automodule Integration

### Maintains Both Approaches:
1. **Visual galleries**: Beautiful card-based browsing (existing)
2. **Full automodule**: Complete API documentation (new)
3. **Consistent linking**: Gallery cards link to automodule pages
4. **No conflicts**: Manual modules replace broken autosummary

### Result:
- 🎨 **Users browse visually** via gallery cards
- 📚 **Developers get full API** via automodule pages
- 🔗 **Seamless navigation** between both views
- ✅ **Everything works** - no more broken links

## Commands Summary

### Daily Development:
```bash
# Smart build (recommended)
nox -s docs_auto

# Live development server
nox -s docs_serve

# View without rebuild
nox -s docs_view
```

### Maintenance:
```bash
# Force fresh generation
nox -s docs_regenerate

# Run examples separately
nox -s docs_examples

# Clean everything
nox -s docs_clean
```

### Direct Poetry (Fastest):
```bash
# If you just want to build quickly
poetry run sphinx-build -b html docs/source docs/build/html
```

## Benefits

### For Developers:
- **Automatic**: No manual module page creation
- **Fast**: Smart caching prevents unnecessary work
- **Reliable**: Always generates working automodule pages
- **Complete**: Full API documentation with all classes/functions

### For Users:
- **Visual**: Beautiful gallery browsing experience
- **Functional**: All links work and show content
- **Comprehensive**: Both overview and detailed documentation
- **Responsive**: Modern navigation improvements

### For Maintenance:
- **Self-updating**: Detects package changes automatically
- **Separate concerns**: Examples don't trigger doc rebuilds
- **Error resilient**: Continues on import failures
- **Debuggable**: Clear logging and error reporting

## Status: ✅ COMPLETE
Auto-build system implemented with:
- ✅ Smart module generation
- ✅ Timestamp-based caching
- ✅ Separate example runs
- ✅ Gallery + automodule integration
- ✅ Comprehensive error handling
- ✅ Performance optimizations

Run `nox -s docs_auto` to test the new system!