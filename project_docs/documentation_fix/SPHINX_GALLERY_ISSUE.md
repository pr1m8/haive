# Sphinx-Gallery Extension Issue Analysis

**Issue**: `WARNING: while setting up extension sphinx_gallery: extension 'sphinx_gallery' has no setup() function; is it really a Sphinx extension module?`
**Status**: Non-critical warning, but needs proper configuration
**Date**: 2025-07-27

## 🚨 Current Problem

In our `conf.py`, we have:
```python
extensions = [
    # Documentation enhancement
    "sphinx_gallery",  # ❌ WRONG - should be sphinx_gallery.gen_gallery
    "sphinx_exec_directive",
]
```

This causes the warning because `sphinx_gallery` is the package name, but the actual extension module is `sphinx_gallery.gen_gallery`.

## ✅ Proper Configuration

### 1. Fix Extension Import
```python
extensions = [
    # Documentation enhancement
    "sphinx_gallery.gen_gallery",  # ✅ CORRECT
    "sphinx_exec_directive",
]
```

### 2. Add Configuration Dictionary
```python
# Sphinx Gallery configuration
sphinx_gallery_conf = {
    # Required: path to example scripts
    'examples_dirs': 'examples',   # path to example scripts
    'gallery_dirs': 'auto_examples',  # path to gallery generated output
    
    # Optional configurations
    'filename_pattern': '/plot_',  # Only files matching this pattern
    'ignore_pattern': r'__init__\.py',
    'download_all_examples': True,
    'plot_gallery': True,
    'remove_config_comments': True,
    'expected_failing_examples': [],
    
    # Execution configuration
    'abort_on_example_error': False,  # Don't stop build on example errors
    'run_stale_examples': True,
    
    # Output configuration
    'compress_images': ['images', 'thumbnails'],
    'image_scrapers': ('matplotlib',),
    
    # Reference links
    'reference_url': {
        'sphinx_gallery': None,  # Keep as None for now
    }
}
```

## 🔍 Understanding Sphinx-Gallery

### Purpose
Sphinx-Gallery automatically:
1. **Executes Python scripts** in your examples directory
2. **Captures output** (text, plots, images)
3. **Generates documentation** with code + output
4. **Creates downloadable** Jupyter notebooks
5. **Builds thumbnail galleries** of examples

### Directory Structure
```
docs/
├── source/
│   ├── conf.py
│   └── examples/          # Source example scripts
│       ├── plot_basic_usage.py
│       ├── plot_advanced_features.py
│       └── ...
└── build/
    └── html/
        └── auto_examples/  # Generated gallery output
            ├── index.html
            ├── plot_basic_usage.html
            └── ...
```

## 🎯 For Haive Project

### Current Status
- **Examples exist**: We have examples in various packages
- **Gallery not configured**: No examples directory set up for gallery
- **Extension misconfigured**: Wrong import causing warning

### Recommended Setup

#### Option 1: Minimal Fix (Remove Warning)
```python
# In conf.py - remove sphinx_gallery entirely for now
extensions = [
    "autoapi.extension",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_design",
    "myst_parser",
    "sphinxcontrib.mermaid",
    # "sphinx_gallery.gen_gallery",  # Remove until properly configured
    "sphinx_exec_directive",
]
```

#### Option 2: Proper Configuration (Recommended)
```python
# In conf.py - fix the import and add configuration
extensions = [
    "autoapi.extension",
    "sphinx.ext.napoleon", 
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_design",
    "myst_parser",
    "sphinxcontrib.mermaid",
    "sphinx_gallery.gen_gallery",  # ✅ FIXED
    "sphinx_exec_directive",
]

# Add gallery configuration
sphinx_gallery_conf = {
    'examples_dirs': ['../examples', '../packages/*/examples'],
    'gallery_dirs': 'auto_examples',
    'filename_pattern': '/example_',
    'ignore_pattern': r'__init__\.py',
    'download_all_examples': False,  # Disable for now
    'plot_gallery': True,
    'abort_on_example_error': False,  # Don't break build
    'run_stale_examples': False,  # Don't re-run if not changed
}
```

## 📋 Implementation Plan

### Phase 1: Quick Fix ✅
- Fix the extension import from `sphinx_gallery` to `sphinx_gallery.gen_gallery`
- This eliminates the warning immediately

### Phase 2: Proper Configuration (Future)
1. **Identify example files** across packages
2. **Create unified examples directory** or configure multiple dirs
3. **Add sphinx_gallery_conf** with proper settings
4. **Test gallery generation** with a few examples

### Phase 3: Full Gallery Implementation (Future)
1. **Standardize example format** for gallery
2. **Add plot examples** for visual components
3. **Create downloadable notebooks**
4. **Integrate with main documentation**

## 🔧 Quick Fix Implementation

Let's update the conf.py to fix the immediate warning:

```python
# Current problematic line:
"sphinx_gallery",

# Should be:
"sphinx_gallery.gen_gallery",

# OR remove entirely if not using:
# Comment out until properly configured
```

## 📊 Benefits of Proper Sphinx-Gallery

### For Users
- **Executable examples** with guaranteed working code
- **Visual output** showing plots, results
- **Downloadable notebooks** for experimentation
- **Thumbnail gallery** for quick browsing

### For Developers  
- **Automatic testing** of example code
- **Documentation that can't go stale** (code is executed)
- **Professional presentation** of capabilities
- **Integration with CI/CD** for example validation

## 🎯 Recommendation

**Immediate**: Fix the extension import to eliminate warning
**Future**: Implement proper gallery configuration once core documentation is stable

The warning is non-critical and doesn't affect our AutoAPI success, but fixing it improves the build output quality.