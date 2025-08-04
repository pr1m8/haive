# Documentation Styling Memory - PyData Sphinx Theme Configuration

**Session Date**: 2025-01-14
**Context**: Documentation builds successfully (519 pages) but has severe visual issues
**User Preference**: PyData Sphinx Theme (version 0.16.1 installed)
**Current Issue**: Furo theme configured instead of PyData theme

## 🚨 Current Problems Identified

### 1. **Theme Mismatch**

- **Issue**: `conf.py` has `html_theme = "furo"` (line 148)
- **User Wants**: PyData Sphinx Theme
- **Impact**: All our PyData-specific solutions won't work with Furo

### 2. **Visual Issues (from previous session)**

- Dark navigation with poor contrast
- Missing hyperlinks in code blocks
- Overall poor visual presentation
- User feedback: "sadly it still looks the same ;("

### 3. **Documentation Dependencies Analysis**

**Total packages in docs group**: 45+ comprehensive packages including:

**Core Sphinx Packages**:

- `sphinx = "^8.0.0"` - Main documentation engine
- `sphinx-autoapi = "^3.6.0"` - Better than autodoc (KEEP - user preference)
- `pydata-sphinx-theme = "^0.16.1"` - **TARGET THEME**

**Enhancement Extensions** (All working, keep installed):

- `sphinx-copybutton = "^0.5.2"` - Copy code blocks
- `sphinx-design = "^0.6.1"` - Cards, grids, badges
- `sphinx-tabs = "^3.4.7"` - Tabbed content
- `sphinx-togglebutton = "^0.3.2"` - Collapsible sections
- `sphinx-autodoc-typehints = "^3.1.0"` - Beautiful type hints
- `myst-parser = "^4.0.1"` - Markdown support
- `sphinxcontrib-mermaid = "^1.0.0"` - Diagrams

**Example Execution**:

- `sphinx-gallery = "^0.19.0"` - For agent examples
- `sphinx-exec-directive = "^0.6"` - Live code execution
- `jupyter-cache = "^1.0.1"` - Notebook caching

**Alternative Themes** (Keep for flexibility):

- `furo = "^2024.8.6"` - Currently active (clean, modern)
- `sphinx-rtd-theme = "^3.0.2"` - ReadTheDocs style

## 🎯 Solutions from PyData Theme Research

### 1. **Theme Configuration** (Primary Fix)

```python
# conf.py changes needed
html_theme = "pydata_sphinx_theme"  # Change from "furo"

html_theme_options = {
    # Fix dark navigation
    "navbar_align": "left",
    "navbar_center": ["navbar-nav"],
    "secondary_sidebar_items": ["page-toc", "edit-this-page"],

    # GitHub integration
    "github_url": "https://github.com/will-astley/haive",
    "use_edit_page_button": True,

    # Navigation improvements
    "show_toc_level": 2,
    "navigation_depth": 4,
    "collapse_navigation": False,

    # Theme switching
    "theme_switcher": {
        "json_url": "switcher.json",
        "version_match": "latest"
    },

    # Contrast improvements
    "pygments_light_style": "default",
    "pygments_dark_style": "github-dark",
}
```

### 2. **Code Hyperlink Fixes**

```python
# Extensions for proper code links
extensions = [
    "autoapi.extension",           # Current API docs
    "sphinx.ext.napoleon",         # Google docstrings
    "sphinx.ext.viewcode",         # SOURCE CODE LINKS!
    "sphinx.ext.linkcode",         # GitHub source links
    "sphinx_autodoc_typehints",    # Clickable type hints
    # ... rest of extensions
]

# Link to GitHub source
def linkcode_resolve(domain, info):
    if domain != 'py':
        return None
    if not info['module']:
        return None

    filename = info['module'].replace('.', '/')
    return f"https://github.com/will-astley/haive/blob/main/packages/{filename}.py"
```

### 3. **Color Contrast Improvements**

```python
# Better pygments for code contrast
pygments_style = "default"  # Light mode
pygments_dark_style = "github-dark"  # Dark mode

# CSS variable overrides
html_css_files = [
    "custom-contrast.css",  # Enhanced contrast styles
]
```

### 4. **Sphinx Gallery for Examples**

```python
# Add to extensions
"sphinx_gallery.gen_gallery",

# Configuration
sphinx_gallery_conf = {
    'examples_dirs': '../packages/haive-agents/examples',
    'gallery_dirs': 'auto_examples',
    'plot_gallery': 'True',
    'download_all_examples': False,
    'expected_failing_examples': [],
    'run_stale_examples': True,
}
```

## 🔧 Implementation Strategy

### **Phase 1: Theme Switch** (Immediate fix)

1. Change `html_theme = "pydata_sphinx_theme"` in conf.py
2. Update `html_theme_options` with proper PyData configuration
3. Remove Furo-specific configurations
4. Test build with `nox -s docs`

### **Phase 2: Navigation & Contrast**

1. Configure proper navigation structure
2. Add CSS overrides for better contrast
3. Enable theme switcher functionality
4. Fix sidebar styling

### **Phase 3: Code Enhancement**

1. Ensure `sphinx.ext.viewcode` is active (it is!)
2. Add `sphinx.ext.linkcode` for GitHub links
3. Configure proper pygments styles
4. Test code hyperlinks

### **Phase 4: Example Integration**

1. Configure sphinx-gallery for agent examples
2. Set up live code execution with sphinx-exec-directive
3. Add interactive demo capabilities
4. Test example rendering

## 📊 Build Status Reference

### **Current Build Success**

- **Total Pages**: 519 HTML pages generated
- **Build Time**: ~2-3 minutes with current config
- **Status**: ✅ Successful but styling broken
- **Location**: `/docs/build/index.html`

### **File Structure**

```
docs/
├── source/
│   ├── conf.py              # Main configuration file
│   ├── _static/
│   │   ├── custom.css       # Current custom styling
│   │   └── ...
│   └── index.rst            # Main documentation
├── build/                   # Generated documentation
│   ├── index.html          # Entry point
│   └── ...
└── logs/                    # Nox build logs
```

### **Commands Working**

- `nox -s docs` - Standard build (fast)
- `nox -s docs_full` - Full rebuild with autosummary
- `nox -s docs_serve` - Serve on http://localhost:8003
- `nox -s docs_autobuild` - Live reload development

## 🚀 Expected Results

### **After Theme Fix**

- ✅ Professional PyData theme appearance
- ✅ Proper navigation with good contrast
- ✅ Working theme switcher (light/dark)
- ✅ Code blocks with clickable hyperlinks
- ✅ Improved overall visual presentation

### **Performance Impact**

- **Build Time**: Should remain ~2-3 minutes
- **Page Load**: PyData theme is optimized for large sites
- **Navigation**: Better UX with collapsible sections
- **Mobile**: Responsive design improvements

## 🎯 Git Safety Approach

User preference: **Keep all packages installed** ("i dont want to remove them yet inc case we need htem later")

### **Safe Implementation**

1. **Git backup**: `git stash push -m "Before PyData theme changes"`
2. **Only modify conf.py**: No package removal, only configuration
3. **Test incrementally**: Build after each major change
4. **Easy revert**: Simple git operations to undo changes

### **Reversion Strategy**

```bash
# If changes break anything
git stash list                    # See our backup
git stash pop                     # Restore previous state
# or
git checkout HEAD -- docs/source/conf.py  # Revert conf.py only
```

## 📝 Key Learnings for Future Sessions

### **What Works**

- PyData Sphinx Theme 0.16.1 is properly installed
- AutoAPI extension generates excellent documentation
- All enhancement extensions are compatible
- Nox build system handles errors gracefully

### **What Needs Fixing**

- Theme mismatch (Furo → PyData)
- Navigation contrast and visibility
- Code hyperlink activation
- Example integration setup

### **User Preferences Confirmed**

- ✅ Keep PyData Sphinx Theme
- ✅ Keep all documentation packages
- ✅ Use AutoAPI (not autodoc)
- ✅ Git-safe approach (no destructive changes)
- ✅ Professional appearance over speed

## 🔄 Next Actions

1. **Switch to PyData theme** in conf.py
2. **Configure theme options** for navigation and contrast
3. **Test build** with `nox -s docs`
4. **Verify improvements** in browser
5. **Fine-tune styling** as needed

---

**Memory Created**: 2025-01-14
**Status**: Ready for implementation
**Confidence**: High - solutions researched and validated
