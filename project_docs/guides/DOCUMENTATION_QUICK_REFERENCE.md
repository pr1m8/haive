# 📚 Documentation Improvements Quick Reference

**Last Updated**: 2025-08-22
**Purpose**: Quick reference for applying haive-mcp documentation patterns

## 🚀 Quick Start

### Apply to a Package

```bash
# Dry run first
python scripts/apply_doc_improvements.py haive-agents --dry-run

# Apply improvements
python scripts/apply_doc_improvements.py haive-agents

# Build and serve
cd packages/haive-agents
sphinx-build -b html docs/source docs/build/html
python -m http.server 8005 --directory docs/build/html
```

## 🔧 Key Configuration Changes

### 1. conf.py Essential Updates

```python
# Hierarchical API organization (CRITICAL!)
autoapi_own_page_level = "module"  # Not "class"
autoapi_member_order = "groupwise"
autoapi_toctree_caption = "🔍 Complete API Reference"
autoapi_toctree_first = True

# All 13 extensions
extensions = [
    "autoapi.extension",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.ifconfig",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_tabs.tabs",
    "sphinx_togglebutton",
    "sphinxcontrib.mermaid",
    "sphinx.ext.graphviz",
]

# Enhanced navigation
html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": False,
    "sticky_navigation": True,
}
```

### 2. Black/Blue Theme CSS

```css
/* Add to _static/black-blue-theme.css */
body[data-theme="dark"] {
  background-color: #000612 !important;
}

body[data-theme="dark"] .sidebar-container {
  background-color: #0a1428 !important;
  border-right: 1px solid #1e3a8a !important;
}

body[data-theme="dark"] pre {
  background-color: #0f172a !important;
}
```

### 3. index.rst Structure

```rst
.. toctree::
   :maxdepth: 4
   :caption: 📖 Documentation
   :hidden:

   API Overview <api_reference>
   Class Inheritance <inheritance_diagram>

.. toctree::
   :maxdepth: 3
   :caption: 🚀 Quick Start
   :hidden:

   getting_started
   installation
   quickstart

.. Use sphinx-design grids for features
.. grid:: 2
   :gutter: 3

   .. grid-item-card:: 🔍 **Feature 1**
   .. grid-item-card:: 🚀 **Feature 2**
```

## 📋 Checklist for Each Package

### Pre-Implementation

- [ ] Check if docs directory exists
- [ ] Verify current Sphinx version
- [ ] Backup existing configuration
- [ ] Review package-specific needs

### Core Updates

- [ ] Update conf.py with all settings
- [ ] Add black/blue theme CSS
- [ ] Fix RST docstrings in **init**.py files
- [ ] Restructure index.rst with proper hierarchy
- [ ] Create inheritance_diagram.rst

### Validation

- [ ] Build docs locally
- [ ] Check AutoAPI hierarchy (not flat)
- [ ] Verify dark mode colors
- [ ] Test all navigation links
- [ ] Screenshot for comparison

### Post-Implementation

- [ ] Commit changes
- [ ] Update package README
- [ ] Add to CI/CD if needed
- [ ] Document any issues

## 🎯 Package-Specific Notes

### haive-agents

- Large number of agent classes
- Complex inheritance hierarchy
- Need comprehensive examples
- Group by agent type (simple, react, multi, rag)

### haive-games

- Visual elements important
- Game screenshots helpful
- State/action space documentation
- Interactive examples if possible

### haive-dataflow

- Flow diagrams essential
- Performance metrics
- Streaming concepts
- Integration examples

### haive-prebuilt

- Quick start focus
- Configuration tables
- Ready-to-use examples
- Minimal setup required

## 🛠️ Common Issues & Fixes

### Issue: Flat API Structure

**Fix**: Set `autoapi_own_page_level = "module"`

### Issue: Poor Dark Mode Contrast

**Fix**: Apply black/blue theme CSS

### Issue: Missing Extensions

**Fix**: Add all 13 extensions to conf.py

### Issue: RST Formatting Errors

**Fix**: Run docstring fixer script

### Issue: Confusing Navigation

**Fix**: Restructure index.rst with proper TOC hierarchy

## 📊 Success Metrics

### Visual

- ✅ Hierarchical API navigation (not alphabetical list)
- ✅ Black/blue dark mode (not purple)
- ✅ Clean code blocks without duplication
- ✅ Professional grid layout for features

### Technical

- ✅ All 13 extensions working
- ✅ Cross-references functional
- ✅ Fast build times
- ✅ No broken links

### User Experience

- ✅ API Reference easily accessible
- ✅ Clear navigation hierarchy
- ✅ Examples for major classes
- ✅ Mobile-responsive design

## 🚀 Automation Commands

### Apply All Improvements

```bash
# Single package
python scripts/apply_doc_improvements.py haive-agents

# All packages (future script)
for pkg in haive-agents haive-games haive-dataflow haive-prebuilt; do
    python scripts/apply_doc_improvements.py $pkg
done
```

### Build All Documentation

```bash
# Build all packages
for pkg in haive-core haive-agents haive-tools haive-games haive-mcp haive-dataflow haive-prebuilt; do
    echo "Building $pkg..."
    sphinx-build -b html packages/$pkg/docs/source packages/$pkg/docs/build/html
done
```

### Validate Documentation

```bash
# Check for broken links
sphinx-build -b linkcheck docs/source docs/build/linkcheck

# Check RST syntax
rst-lint packages/*/docs/source/**/*.rst
```

## 📝 Final Notes

1. **Always test locally first** - Use --dry-run option
2. **Fix RST issues** - Many **init**.py files need formatting
3. **Create missing files** - Some packages lack proper structure
4. **Use descriptive commits** - Track documentation changes
5. **Take screenshots** - Before/after comparison helpful

---

**Remember**: The goal is consistent, professional documentation across all Haive packages! 🎯
