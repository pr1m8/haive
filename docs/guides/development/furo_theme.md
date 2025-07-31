# Furo Theme Configuration Guide for Haive

## Overview

This guide explains how to properly configure the Furo theme for the Haive namespaced monorepo documentation, addressing CSS layout issues and AutoAPI configuration.

## Understanding Furo's Design Philosophy

Furo is designed to be:

- **Intentionally minimal** - Clean, uncluttered design
- **Responsive** - Adapts to all screen sizes
- **CSS Variable-driven** - Customization through variables, not overrides
- **Pure CSS sidebar** - No JavaScript required for navigation

## CSS Variables Configuration

### The Right Way: Use Theme Options

Instead of fighting Furo with `!important` CSS overrides, configure it properly in `conf.py`:

```python
html_theme_options = {
    "light_css_variables": {
        # Layout variables (these are custom, Furo doesn't document layout vars)
        "--sidebar-width": "18rem",  # Default is ~15rem
        "--content-width": "50rem",  # Main content max width
        "--toc-width": "15rem",      # Right sidebar TOC width

        # Spacing
        "--sidebar-item-spacing-vertical": "0.4rem",
        "--sidebar-item-spacing-horizontal": "1rem",
        "--content-padding": "2rem 3rem",

        # Typography
        "--font-stack": "-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif",
        "--font-stack--monospace": "SFMono-Regular, Menlo, Consolas, Monaco, Liberation Mono, Lucida Console, monospace",

        # Colors (documented variables)
        "color-brand-primary": "#007acc",
        "color-brand-content": "#0066cc",
        "color-sidebar-background": "#f8f9fb",
        "color-sidebar-background-border": "#eeebee",
        "color-sidebar-brand-text": "#333333",
        "color-sidebar-search-background": "#ffffff",
        "color-sidebar-search-border": "#cccccc",
        "color-sidebar-link-text": "#333333",
        "color-sidebar-link-text--top-level": "#333333",

        # Code blocks
        "color-code-background": "#f8f8f8",
        "color-code-foreground": "#333333",
    },

    # Dark mode variables
    "dark_css_variables": {
        "color-brand-primary": "#4db8ff",
        "color-brand-content": "#66ccff",
        "color-sidebar-background": "#131416",
        "color-code-background": "#1e1e1e",
    },

    # Other Furo options
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "top_of_page_buttons": ["edit"],
}
```

### Custom CSS (Minimal Approach)

If you need additional customization, create a minimal CSS file:

```css
/* _static/custom-furo.css */

/* Layout adjustments using CSS custom properties */
:root {
  /* These override any theme defaults */
  --sidebar-width: 18rem;
  --content-width: 50rem;
  --content-padding-x: 3rem;
  --content-padding-y: 2rem;
}

/* Fix code blocks to use full width */
.highlight {
  margin: 1rem 0;
}

.highlight pre {
  overflow-x: auto;
  max-width: 100%;
}

/* Responsive breakpoints */
@media (max-width: 67em) {
  :root {
    --sidebar-width: 100%;
  }
}

/* API documentation spacing */
dl.py {
  margin: 1.5rem 0;
}

dl.field-list > dt {
  font-weight: 600;
  margin-top: 1rem;
}
```

Then in `conf.py`:

```python
html_static_path = ["_static"]
html_css_files = ["custom-furo.css"]
```

## AutoAPI Configuration for Namespaced Packages

### The Problem

In a namespaced monorepo with src layout:

```
packages/
├── haive-core/
│   └── src/
│       └── haive/
│           └── core/
├── haive-agents/
│   └── src/
│       └── haive/
│           └── agents/
```

AutoAPI needs to:

1. Find the correct modules
2. Generate docs with correct import paths (`haive.core`, not `src.haive.core`)
3. Not process thousands of test/example files

### The Solution

```python
# conf.py

# 1. Add src directories to Python path
packages_dir = Path(__file__).parent.parent.parent / "packages"
for package in ["haive-core", "haive-agents", "haive-tools", "haive-games"]:
    src_path = packages_dir / package / "src"
    if src_path.exists():
        sys.path.insert(0, str(src_path))

# 2. Configure AutoAPI correctly
extensions = [
    "autoapi.extension",
    # ... other extensions
]

# Point to the haive directories inside src
autoapi_type = "python"
autoapi_dirs = [
    str(packages_dir / "haive-core" / "src" / "haive"),
    str(packages_dir / "haive-agents" / "src" / "haive"),
    str(packages_dir / "haive-tools" / "src" / "haive"),
    str(packages_dir / "haive-games" / "src" / "haive"),
]

# Enable namespace package support
autoapi_python_use_implicit_namespaces = True

# Aggressive ignore patterns to reduce file count
autoapi_ignore = [
    "**/test_*",
    "**/tests/**",
    "**/*_test.py",
    "**/examples/**",
    "**/example_*.py",
    "**/scripts/**",
    "**/.ipynb_checkpoints/**",
    "**/archive/**",
    "**/old/**",
    "**/deprecated/**",
    "**/debug*.py",
    "**/demo*.py",
    "**/cli.py",
    "**/supervisor/**",  # If too many variants
    "**/*_demo.py",
    "**/*_example.py",
]

# Output configuration
autoapi_root = "api"
autoapi_add_toctree_entry = True
autoapi_keep_files = True  # For debugging

# Options
autoapi_options = [
    "members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",  # Show imported members
]
```

## Common Issues and Solutions

### Issue 1: "Everything is pushed to the right"

**Cause**: Sidebar CSS variables are too large or conflicting CSS.

**Solution**: Use Furo's CSS variables properly:

```python
"light_css_variables": {
    "--sidebar-width": "15rem",  # Reasonable width
    "--content-width": "50rem",
}
```

### Issue 2: Code blocks are too narrow

**Cause**: Content area constraints or pre/code styling.

**Solution**: Minimal CSS override:

```css
.highlight pre {
  overflow-x: auto;
  white-space: pre;
}
```

### Issue 3: AutoAPI processes too many files

**Cause**: Pointing to directories with many non-documentation files.

**Solution**: Use aggressive `autoapi_ignore` patterns and point to specific namespace directories.

### Issue 4: Import paths include 'src'

**Cause**: AutoAPI includes the directory structure in module names.

**Solution**:

1. Add src to `sys.path`
2. Point AutoAPI to namespace directories
3. Use `autoapi_python_use_implicit_namespaces = True`

## Testing Your Configuration

1. **Start with minimal configuration**:

   ```python
   # Minimal conf.py
   project = "Haive"
   extensions = ["myst_parser"]
   html_theme = "furo"
   ```

2. **Add one feature at a time**:
   - First, get basic Furo working
   - Then add AutoAPI for one package
   - Then add CSS customization
   - Finally, add all packages

3. **Check the build output**:

   ```bash
   # Clean build
   rm -rf docs/build

   # Build with warnings
   sphinx-build -W -b html docs/source docs/build/html

   # Check for issues
   grep -i "warning\|error" docs/build/*.log
   ```

## Best Practices

1. **Work WITH Furo, not against it** - Use CSS variables, not !important overrides
2. **Keep CSS minimal** - Furo is designed to work out of the box
3. **Use semantic HTML** - Furo styles semantic elements correctly
4. **Test responsive behavior** - Check mobile and desktop views
5. **Configure AutoAPI carefully** - Better to exclude too much than process everything

## References

- [Furo Documentation](https://pradyunsg.me/furo/)
- [Furo GitHub Repository](https://github.com/pradyunsg/furo)
- [AutoAPI Documentation](https://sphinx-autoapi.readthedocs.io/)
- [Sphinx Configuration](https://www.sphinx-doc.org/en/master/usage/configuration.html)
