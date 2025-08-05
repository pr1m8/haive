# Furo Sphinx Theme: Complete Professional Guide

**Created**: 2025-08-05  
**Purpose**: Comprehensive guide to using and customizing the Furo Sphinx theme  
**Version Coverage**: Furo 2024.08.06 + Sphinx 8.2.3

## Table of Contents

1. [Introduction & Philosophy](#introduction--philosophy)
2. [Installation & Basic Setup](#installation--basic-setup)
3. [Complete Configuration Reference](#complete-configuration-reference)
4. [CSS Variables Mastery](#css-variables-mastery)
5. [Dark/Light Mode Implementation](#darklight-mode-implementation)
6. [Navigation & Sidebar Customization](#navigation--sidebar-customization)
7. [Advanced Features](#advanced-features)
8. [Professional Customization Patterns](#professional-customization-patterns)
9. [Integration with Extensions](#integration-with-extensions)
10. [Performance & Accessibility](#performance--accessibility)
11. [Troubleshooting](#troubleshooting)
12. [Real-World Examples](#real-world-examples)

## Introduction & Philosophy

### What Makes Furo Special

Furo is built on the principle that **content is king**. Unlike other themes that add visual flourishes, Furo focuses on:

- **Readability**: Typography and spacing optimized for reading
- **Simplicity**: Minimal UI that doesn't distract from content
- **Customizability**: Extensive CSS variables for professional branding
- **Accessibility**: WCAG 2.1 compliant by default
- **Performance**: Fast, efficient rendering with minimal JavaScript

### Core Design Principles

1. **Content-First**: The most important thing is your content
2. **Responsive**: Works perfectly on all screen sizes
3. **Accessible**: Screen reader friendly, keyboard navigable
4. **Customizable**: Brand it to match your organization
5. **Modern**: Built with 2024+ web standards

## Installation & Basic Setup

### Installation

```bash
# Install Furo
pip install furo

# Or with Poetry
poetry add furo
```

### Minimal Configuration

```python
# conf.py - Minimal setup
html_theme = "furo"

html_theme_options = {
    # Minimal required options
}
```

### Standard Configuration

```python
# conf.py - Recommended setup
html_theme = "furo"
html_title = f"{project} Documentation"

html_theme_options = {
    "sidebar_hide_name": True,  # Hide project name in sidebar
    "navigation_with_keys": True,  # Arrow key navigation
    "top_of_page_buttons": ["edit", "view"],  # Show edit/view buttons
}

# Static files
html_static_path = ["_static"]
html_css_files = ["custom.css"]
```

## Complete Configuration Reference

### Core Theme Options (`html_theme_options`)

| Option | Type | Description | Example |
|--------|------|-------------|---------|
| `sidebar_hide_name` | bool | Hide project name in sidebar | `True` |
| `navigation_with_keys` | bool | Enable arrow key navigation | `True` |
| `top_of_page_buttons` | list | Show edit/view buttons | `["edit", "view"]` |
| `footer_icons` | list | Social links in footer | See [Footer Icons](#footer-icons) |
| `source_repository` | str | Repository URL for edit links | `"https://github.com/user/repo"` |
| `source_branch` | str | Default branch | `"main"` |
| `source_directory` | str | Docs directory in repo | `"docs/"` |
| `announcement` | str | Site-wide banner message | `"🚀 New release available!"` |
| `light_logo` | str | Logo for light mode | `"logo-light.png"` |
| `dark_logo` | str | Logo for dark mode | `"logo-dark.png"` |

### Logo Configuration Patterns

#### Single Logo (Works in Both Modes)
```python
html_logo = "_static/logo.png"
```

#### Dual Mode Logos
```python
html_theme_options = {
    "light_logo": "_static/logo-light.png",
    "dark_logo": "_static/logo-dark.png",
}
```

#### Logo with Text Fallback
```python
html_theme_options = {
    "sidebar_hide_name": False,  # Show text if logo fails
}
html_logo = "_static/logo.png"
```

### Footer Icons

```python
html_theme_options = {
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/yourusername/project",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 496 512">
                    <path d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"/>
                </svg>
            """,
            "class": "",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/yourproject/",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 24 24">
                    <path d="M12 2L13.09 8.26L22 9L13.09 9.74L12 22L10.91 9.74L2 9L10.91 8.26L12 2Z"/>
                </svg>
            """,
        }
    ],
}
```

### Announcement Banner

```python
html_theme_options = {
    "announcement": """
        🚀 <strong>New Release:</strong> Haive v2.0 is now available! 
        <a href="/changelog">See what's new</a>
    """,
}
```

## CSS Variables Mastery

### Understanding CSS Variables System

Furo uses CSS custom properties (variables) for all styling. This allows:
- **Consistent theming**: Change one variable, update everywhere
- **Dark/light modes**: Different variable sets for each mode
- **Brand customization**: Match your organization's colors
- **Maintainable code**: Changes cascade automatically

### Complete CSS Variables Reference

#### Brand & Identity Colors

```python
html_theme_options = {
    "light_css_variables": {
        # Primary brand color (links, buttons, accents)
        "color-brand-primary": "#2563eb",      # Blue-600
        "color-brand-content": "#1e40af",      # Blue-700 (slightly darker)
        
        # Brand colors for different contexts
        "color-brand-visited": "#7c3aed",      # Purple for visited links
    },
    "dark_css_variables": {
        "color-brand-primary": "#3b82f6",      # Lighter blue for dark mode
        "color-brand-content": "#60a5fa",      # Even lighter for content
        "color-brand-visited": "#a78bfa",      # Lighter purple
    }
}
```

#### Typography System

```python
"light_css_variables": {
    # Font stacks
    "font-stack": "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    "font-stack--monospace": "'JetBrains Mono', 'SF Mono', Consolas, monospace",
    
    # Font sizes (using fluid typography)
    "font-size--small": "0.875rem",           # 14px
    "font-size--normal": "1rem",              # 16px  
    "font-size--large": "1.125rem",           # 18px
    
    # Line heights for readability
    "line-height": "1.6",                     # Body text
    "line-height--normal": "1.5",             # Headings
    "line-height--tight": "1.3",              # Large headings
}
```

#### Layout & Spacing

```python
"light_css_variables": {
    # Content area dimensions
    "content-padding-x": "2rem",              # Horizontal padding
    "content-padding-y": "1rem",              # Vertical padding
    "content-width": "46rem",                 # Max content width (736px)
    
    # Sidebar configuration
    "sidebar-width": "16rem",                 # 256px sidebar
    "sidebar-item-spacing": "0.5rem",         # Space between items
    
    # Header configuration  
    "header-height": "3.5rem",               # 56px header
    "header-padding": "1rem",                # Header internal padding
    
    # Responsive breakpoints
    "sidebar-hide-threshold": "62rem",       # When to hide sidebar
}
```

#### Color Palette System

```python
"light_css_variables": {
    # Foreground colors (text)
    "color-foreground-primary": "#1a202c",    # Main text (gray-900)
    "color-foreground-secondary": "#4a5568",  # Secondary text (gray-600)  
    "color-foreground-muted": "#718096",      # Muted text (gray-500)
    "color-foreground-border": "#e2e8f0",     # Borders (gray-200)
    
    # Background colors
    "color-background-primary": "#ffffff",     # Main background
    "color-background-secondary": "#f7fafc",  # Sidebar background
    "color-background-hover": "#edf2f7",      # Hover states
    "color-background-border": "#e2e8f0",     # Border accents
    
    # Semantic colors
    "color-admonition-title--note": "#2563eb",      # Blue
    "color-admonition-title--tip": "#059669",       # Green  
    "color-admonition-title--warning": "#d97706",   # Orange
    "color-admonition-title--caution": "#dc2626",   # Red
}
```

#### Code & API Documentation

```python
"light_css_variables": {
    # Code blocks
    "color-code-background": "#f8f9fa",       # Light gray background
    "color-code-foreground": "#24292e",       # Dark text
    "color-inline-code-background": "#f1f3f5", # Inline code background
    
    # API documentation  
    "color-api-background": "#f8f9fa",        # API section background
    "color-api-background-hover": "#e9ecef",  # API hover state
    "color-api-overall": "#495057",           # API text color
    
    # Tables
    "color-table-border": "#dee2e6",          # Table borders
    "color-table-background-hover": "#f8f9fa", # Row hover
}
```

### Professional Color Schemes

#### Corporate Blue Theme
```python
"light_css_variables": {
    "color-brand-primary": "#0066cc",         # Corporate blue
    "color-brand-content": "#004499",         # Darker blue for content
    "color-foreground-primary": "#1a1a1a",    # Near-black text
    "color-background-primary": "#ffffff",     # Pure white
    "color-background-secondary": "#f8f9ff",   # Very light blue tint
},
"dark_css_variables": {
    "color-brand-primary": "#3399ff",         # Brighter blue for dark
    "color-brand-content": "#66b3ff",         # Even brighter for content
    "color-foreground-primary": "#e6e6e6",    # Light gray text
    "color-background-primary": "#1a1d23",    # Dark blue-gray
    "color-background-secondary": "#252830",   # Lighter dark
}
```

#### Green Tech Theme
```python
"light_css_variables": {
    "color-brand-primary": "#059669",         # Emerald green
    "color-brand-content": "#047857",         # Darker green
    "color-foreground-primary": "#111827",    # Dark gray
    "color-background-primary": "#ffffff",     
    "color-background-secondary": "#f0fdf4",   # Very light green tint
},
"dark_css_variables": {
    "color-brand-primary": "#10b981",         # Brighter green
    "color-brand-content": "#34d399",         
    "color-foreground-primary": "#f3f4f6",    
    "color-background-primary": "#111827",     # Dark gray
    "color-background-secondary": "#1f2937",   
}
```

## Dark/Light Mode Implementation

### Automatic Mode Detection

Furo automatically detects system preference and provides a toggle. No configuration needed:

```python
# Default behavior - automatically works
html_theme = "furo"
```

### Custom Mode Configuration

```python
html_theme_options = {
    # Separate variables for each mode
    "light_css_variables": {
        "color-brand-primary": "#2563eb",
        "color-background-primary": "#ffffff",
        # ... all light mode variables
    },
    "dark_css_variables": {
        "color-brand-primary": "#3b82f6", 
        "color-background-primary": "#1a202c",
        # ... all dark mode variables
    }
}
```

### Mode-Specific Assets

```python
html_theme_options = {
    "light_logo": "_static/logo-light.png",   # Dark logo on light background
    "dark_logo": "_static/logo-dark.png",     # Light logo on dark background
}

# Also configure Pygments for code highlighting
pygments_style = "default"           # Light mode code theme
pygments_dark_style = "monokai"      # Dark mode code theme
```

### CSS Custom Properties for Modes

Create mode-aware custom CSS:

```css
/* _static/custom.css */

/* Variables that work in both modes */
:root {
    --custom-accent: var(--color-brand-primary);
    --custom-spacing: 1.5rem;
}

/* Mode-specific overrides */
[data-theme="light"] {
    --custom-shadow: rgba(0, 0, 0, 0.1);
}

[data-theme="dark"] {
    --custom-shadow: rgba(255, 255, 255, 0.1);
}

/* Use the variables */
.custom-card {
    border: 1px solid var(--color-background-border);
    box-shadow: 0 2px 4px var(--custom-shadow);
    padding: var(--custom-spacing);
}
```

## Navigation & Sidebar Customization

### Sidebar Configuration

```python
html_theme_options = {
    # Hide project name in sidebar (cleaner look)
    "sidebar_hide_name": True,
    
    # Show edit/view buttons at top of pages
    "top_of_page_buttons": ["edit", "view"],
    
    # Enable keyboard navigation (left/right arrows)
    "navigation_with_keys": True,
}
```

### Toctree Customization

Control navigation depth and structure:

```rst
.. toctree::
   :maxdepth: 2
   :caption: User Guide
   :hidden:

   quickstart
   user-guide/index
   api/index

.. toctree::  
   :maxdepth: 1
   :caption: Development
   :hidden:

   contributing
   development/index
```

### Custom Navigation CSS

```css
/* Customize sidebar appearance */
.sidebar-tree {
    font-size: 0.9rem;
}

.sidebar-tree .caption {
    color: var(--color-brand-primary);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 1.5rem;
}

.sidebar-tree .toctree-l1 > a {
    font-weight: 500;
    padding: 0.25rem 0;
}

.sidebar-tree .current > a {
    color: var(--color-brand-primary);
    border-left: 3px solid var(--color-brand-primary);
    padding-left: 0.75rem;
}
```

### Mobile Navigation

Furo automatically handles mobile navigation, but you can customize:

```css
/* Mobile-specific customizations */
@media (max-width: 62rem) {
    .mobile-header {
        background: var(--color-background-secondary);
        border-bottom: 1px solid var(--color-background-border);
    }
    
    .sidebar-drawer {
        background: var(--color-background-primary);
        box-shadow: 0 0 2rem rgba(0, 0, 0, 0.1);
    }
}
```

## Advanced Features

### Source Repository Integration

Automatic edit/view buttons based on repository URL:

```python
html_theme_options = {
    "source_repository": "https://github.com/yourusername/project",
    "source_branch": "main",
    "source_directory": "docs/source/",
    "top_of_page_buttons": ["edit", "view"],
}
```

### Custom Edit URLs

For non-standard setups:

```python
html_context = {
    "edit_page_url_template": "https://github.com/user/repo/edit/main/docs/{{ pagename }}.rst",
    "view_page_source_url": "https://github.com/user/repo/blob/main/docs/{{ pagename }}.rst",
}
```

### Announcement System

Site-wide announcements with HTML support:

```python
html_theme_options = {
    "announcement": """
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span>🚀</span>
            <strong>New Release:</strong> 
            <span>Haive v2.0 is now available!</span>  
            <a href="/changelog" style="margin-left: auto;">See what's new →</a>
        </div>
    """,
}
```

### Metadata System

Per-page customization using metadata:

```rst
:og:description: Custom social media description for this page
:og:image: /images/custom-social-image.png

# Page Title

Page content here...
```

Access in templates:

```html
<!-- custom template -->
<meta property="og:description" content="{{ meta.get('og:description', '') }}">
```

## Professional Customization Patterns

### Corporate Branding Template

```python
# Corporate theme configuration
html_theme_options = {
    "sidebar_hide_name": True,
    "light_logo": "_static/corporate-logo.png",
    "dark_logo": "_static/corporate-logo-white.png",
    
    "light_css_variables": {
        # Corporate blue palette
        "color-brand-primary": "#003d7a",      # Corporate blue
        "color-brand-content": "#002c5f", 
        
        # Professional typography
        "font-stack": "'Source Sans Pro', sans-serif",
        "font-stack--monospace": "'Source Code Pro', monospace",
        
        # Conservative color scheme
        "color-foreground-primary": "#1a1a1a",
        "color-background-primary": "#ffffff",
        "color-background-secondary": "#f8f9fa",
        
        # Subtle borders and spacing
        "color-background-border": "#e1e5e9",
        "content-padding-x": "2.5rem",
    },
    
    "dark_css_variables": {
        "color-brand-primary": "#4d94ff",
        "color-brand-content": "#80b3ff",
        "color-foreground-primary": "#e6e6e6", 
        "color-background-primary": "#1a1d23",
        "color-background-secondary": "#252830",
    },
    
    "footer_icons": [
        {
            "name": "Corporate Website",
            "url": "https://company.com",
            "html": "<span>🏢</span>",
        }
    ],
}
```

### Developer Documentation Template

```python
# Developer-focused theme
html_theme_options = {
    "navigation_with_keys": True,  # Keyboard shortcuts
    "top_of_page_buttons": ["edit", "view"],
    
    "light_css_variables": {
        # Developer-friendly colors
        "color-brand-primary": "#0969da",      # GitHub blue
        "color-brand-content": "#0550ae",
        
        # Code-focused typography
        "font-stack": "'Inter', system-ui, sans-serif", 
        "font-stack--monospace": "'JetBrains Mono', 'Fira Code', monospace",
        
        # Higher contrast for readability
        "color-foreground-primary": "#24292f",
        "color-foreground-secondary": "#656d76",
        
        # Code block styling
        "color-code-background": "#f6f8fa",
        "color-code-foreground": "#24292f",
        "color-inline-code-background": "#afb8c133",
        
        # API documentation colors
        "color-api-background": "#f6f8fa",
        "color-api-background-hover": "#eef1f5",
    },
    
    "dark_css_variables": {
        "color-brand-primary": "#58a6ff",
        "color-brand-content": "#79c0ff", 
        "color-foreground-primary": "#e6edf3",
        "color-foreground-secondary": "#9198a1",
        "color-background-primary": "#0d1117",
        "color-background-secondary": "#161b22",
        "color-code-background": "#161b22",
        "color-code-foreground": "#e6edf3",
    }
}
```

### Academic/Research Template

```python
# Academic documentation theme
html_theme_options = {
    "sidebar_hide_name": False,  # Show full project name
    
    "light_css_variables": {
        # Academic color scheme (conservative)
        "color-brand-primary": "#8b5a2b",      # Brown
        "color-brand-content": "#704621",
        
        # Academic typography (serif for readability)
        "font-stack": "'Crimson Text', 'Times New Roman', serif",
        "font-stack--monospace": "'Inconsolata', monospace",
        "line-height": "1.7",  # More spacing for reading
        
        # Warm, paper-like colors
        "color-background-primary": "#fffef7",  # Warm white
        "color-background-secondary": "#faf9f2", # Warm gray
        "color-foreground-primary": "#2d2d2d",
        
        # Subtle, academic styling
        "color-background-border": "#d4c5b9",
        "content-padding-x": "3rem",  # More padding for reading
    },
    
    "announcement": """
        📚 <strong>Research Publication:</strong> 
        New findings published in <em>Journal of AI Research</em>
    """,
}
```

## Integration with Extensions

### Essential Extensions for Furo

```python
extensions = [
    # Core documentation
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    
    # Enhanced API docs (better than autodoc)
    'autoapi.extension',
    
    # Markdown support
    'myst_parser',
    
    # Interactive elements
    'sphinx_copybutton',
    'sphinx_togglebutton', 
    'sphinx_tabs.tabs',
    
    # Design elements (if compatible)
    'sphinx_design',  # Cards, grids, badges
]
```

### Copy Button Integration

```python
# Seamless integration with Furo
extensions = ['sphinx_copybutton']

copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

# Custom CSS for copy button styling
html_css_files = ["copybutton-custom.css"]
```

```css
/* _static/copybutton-custom.css */
.copybtn {
    background: var(--color-background-secondary);
    border: 1px solid var(--color-background-border);
    color: var(--color-foreground-secondary);
    border-radius: 0.25rem;
    transition: all 0.2s ease;
}

.copybtn:hover {
    background: var(--color-brand-primary);
    color: white;
    border-color: var(--color-brand-primary);
}
```

### MyST Parser Configuration

```python
# Enhanced Markdown support
extensions = ['myst_parser']

myst_enable_extensions = [
    "colon_fence",      # ::: fences
    "deflist",          # Definition lists
    "tasklist",         # Task lists  
    "attrs_inline",     # {.class} syntax
    "attrs_block",      # {.class} for blocks
]

# Works perfectly with Furo's styling
```

### Tabs Integration

```python
extensions = ['sphinx_tabs.tabs']

# Furo automatically styles tabs beautifully
# No additional configuration needed
```

Usage in documents:

```rst
.. tabs::

   .. tab:: Python
   
      .. code-block:: python
      
         from haive import Agent
         agent = Agent(name="example")

   .. tab:: JavaScript
   
      .. code-block:: javascript
      
         const agent = new Agent({name: "example"});
```

## Performance & Accessibility

### Performance Optimization

#### CSS Optimization
```python
# Minimize CSS file count
html_css_files = [
    "custom.css",  # Single consolidated file
]

# Use CSS variables instead of multiple theme files
html_theme_options = {
    "light_css_variables": {
        # All customizations in variables
    }
}
```

#### JavaScript Optimization
```python
# Minimal JavaScript usage
html_js_files = [
    "analytics.js",  # Only essential scripts
]

# Furo uses minimal JS by design - don't add unnecessary scripts
```

#### Image Optimization
```python
# Optimized logo sizes
html_theme_options = {
    "light_logo": "_static/logo-optimized.svg",  # SVG preferred
    "dark_logo": "_static/logo-dark-optimized.svg",
}

# Or WebP format for raster images
html_logo = "_static/logo.webp"
```

### Accessibility Features

#### Built-in Accessibility
Furo provides out-of-the-box:
- **ARIA labels**: Proper semantic markup
- **Keyboard navigation**: Tab order and shortcuts
- **Screen reader support**: Descriptive elements
- **High contrast**: Respects system preferences
- **Focus indicators**: Clear focus states

#### Enhanced Accessibility Configuration
```python
html_theme_options = {
    "navigation_with_keys": True,  # Arrow key navigation
    
    "light_css_variables": {
        # High contrast ratios (WCAG AA compliant)
        "color-foreground-primary": "#1a1a1a",  # Contrast ratio: 16.94:1
        "color-brand-primary": "#0066cc",        # Contrast ratio: 7.16:1
        
        # Focus indicators
        "color-focus-outline": "#005fcc",
        "focus-outline-width": "2px",
    }
}
```

#### Custom Accessibility CSS
```css
/* Enhanced focus indicators */
:focus {
    outline: 2px solid var(--color-brand-primary);
    outline-offset: 2px;
}

/* Skip navigation link */
.skip-link {
    position: absolute;
    top: -40px;
    left: 6px;
    background: var(--color-brand-primary);
    color: white;
    padding: 8px;
    text-decoration: none;
    z-index: 1000;
}

.skip-link:focus {
    top: 6px;
}

/* Screen reader only content */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}
```

## Troubleshooting

### Common Issues & Solutions

#### Issue: CSS Variables Not Working
```python
# ❌ Common typo - silent failure
"colour-brand-primary": "#ff0000",  # Wrong: "colour"

# ✅ Correct spelling
"color-brand-primary": "#ff0000",   # Correct: "color"
```

#### Issue: Logo Not Showing
```python
# ❌ Wrong path
html_logo = "logo.png"  # File not found

# ✅ Correct path  
html_logo = "_static/logo.png"  # Must be in static path
html_static_path = ["_static"]
```

#### Issue: Dark Mode Not Working
```python
# ❌ Missing dark variables
html_theme_options = {
    "light_css_variables": {"color-brand-primary": "#blue"},
    # Missing dark_css_variables - theme won't switch properly
}

# ✅ Both modes defined
html_theme_options = {
    "light_css_variables": {"color-brand-primary": "#2563eb"},
    "dark_css_variables": {"color-brand-primary": "#3b82f6"},
}
```

#### Issue: Edit Button Not Appearing
```python
# ❌ Missing repository info
html_theme_options = {
    "top_of_page_buttons": ["edit"],  # Button enabled but no URL
}

# ✅ Complete configuration
html_theme_options = {
    "top_of_page_buttons": ["edit"],
    "source_repository": "https://github.com/user/repo",
    "source_branch": "main",
    "source_directory": "docs/source/",
}
```

### Debugging CSS Variables

Create a debug page to test variables:

```rst
CSS Variables Debug
===================

.. raw:: html

   <div style="padding: 1rem; margin: 1rem 0;">
       <h3>Color Variables Test</h3>
       <div style="background: var(--color-brand-primary); color: white; padding: 1rem; margin: 0.5rem 0;">
           Brand Primary: var(--color-brand-primary)
       </div>
       <div style="background: var(--color-background-secondary); padding: 1rem; margin: 0.5rem 0;">
           Background Secondary: var(--color-background-secondary)
       </div>
       <div style="color: var(--color-foreground-secondary); padding: 1rem; margin: 0.5rem 0;">
           Foreground Secondary: var(--color-foreground-secondary)
       </div>
   </div>
```

### Performance Debugging

```python
# Add build timing
import time
start_time = time.time()

# At end of conf.py
print(f"Config loaded in {time.time() - start_time:.2f}s")

# Enable Sphinx timing
extensions.append('sphinx.ext.duration')
```

## Real-World Examples

### Example 1: Tech Startup Documentation

```python
# Modern, clean tech company theme
html_theme = "furo"
html_title = "TechCorp API Documentation"

html_theme_options = {
    "sidebar_hide_name": True,
    "navigation_with_keys": True,
    "top_of_page_buttons": ["edit", "view"],
    
    "light_css_variables": {
        # Tech company brand colors
        "color-brand-primary": "#6366f1",      # Indigo
        "color-brand-content": "#4f46e5",      # Darker indigo
        
        # Modern typography
        "font-stack": "'Inter', system-ui, sans-serif",
        "font-stack--monospace": "'JetBrains Mono', monospace",
        
        # Clean, minimal colors
        "color-foreground-primary": "#111827",  
        "color-background-primary": "#ffffff",
        "color-background-secondary": "#f9fafb",
        
        # API-focused styling
        "color-api-background": "#f8fafc",
        "color-code-background": "#f1f5f9",
    },
    
    "dark_css_variables": {
        "color-brand-primary": "#818cf8",
        "color-brand-content": "#a5b4fc", 
        "color-foreground-primary": "#f3f4f6",
        "color-background-primary": "#111827",
        "color-background-secondary": "#1f2937",
        "color-api-background": "#1f2937", 
        "color-code-background": "#374151",
    },
    
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/techcorp/api",
            "html": """<svg>...</svg>""",
        },
        {
            "name": "API Status",
            "url": "https://status.techcorp.com",
            "html": "🟢",
        }
    ],
    
    "announcement": """
        🚀 <strong>API v2.0</strong> now available with GraphQL support!
        <a href="/v2/migration">Migration guide →</a>
    """,
}

html_css_files = [
    "techcorp-custom.css",
    "api-styling.css",
]
```

### Example 2: Open Source Project

```python
# Community-focused open source theme
html_theme = "furo"
html_title = f"{project} Documentation"

html_theme_options = {
    "sidebar_hide_name": False,  # Show project name proudly
    "navigation_with_keys": True,
    "top_of_page_buttons": ["edit", "view"],
    
    "source_repository": "https://github.com/opensource/project",
    "source_branch": "main",
    "source_directory": "docs/",
    
    "light_css_variables": {
        # Friendly, approachable colors
        "color-brand-primary": "#059669",      # Green (growth, community)
        "color-brand-content": "#047857",
        
        # Readable typography
        "font-stack": "'Source Sans Pro', sans-serif",
        "line-height": "1.6",
        
        # Warm, welcoming colors
        "color-foreground-primary": "#1f2937",
        "color-background-primary": "#ffffff", 
        "color-background-secondary": "#f0fdf4",  # Very light green
    },
    
    "dark_css_variables": {
        "color-brand-primary": "#10b981",
        "color-brand-content": "#34d399",
        "color-foreground-primary": "#f3f4f6",
        "color-background-primary": "#111827",
        "color-background-secondary": "#1f2937",
    },
    
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/opensource/project",
            "html": """<svg>...</svg>""", 
        },
        {
            "name": "Discord",
            "url": "https://discord.gg/project",
            "html": """<svg>...</svg>""",
        },
        {
            "name": "Sponsor",
            "url": "https://github.com/sponsors/project",
            "html": "❤️",
        }
    ],
    
    "announcement": """
        💚 <strong>Community:</strong> Join our Discord for support and discussions!
        <a href="https://discord.gg/project">Join now →</a>
    """,
}
```

### Example 3: Enterprise Documentation

```python
# Enterprise-grade documentation theme
html_theme = "furo"
html_title = "Enterprise Platform Documentation"

html_theme_options = {
    "sidebar_hide_name": True,
    "light_logo": "_static/enterprise-logo.svg",
    "dark_logo": "_static/enterprise-logo-white.svg",
    
    "light_css_variables": {
        # Professional enterprise colors
        "color-brand-primary": "#1e40af",      # Professional blue
        "color-brand-content": "#1e3a8a",
        
        # Enterprise typography (conservative)
        "font-stack": "'Source Sans Pro', Arial, sans-serif",
        "font-stack--monospace": "'Source Code Pro', Consolas, monospace",
        
        # High-contrast, accessible colors
        "color-foreground-primary": "#111827",
        "color-foreground-secondary": "#374151",
        "color-background-primary": "#ffffff",
        "color-background-secondary": "#f9fafb",
        
        # Professional spacing and layout
        "content-padding-x": "3rem",
        "sidebar-width": "18rem",
        
        # Subtle, professional styling
        "color-background-border": "#d1d5db",
        "color-admonition-title--note": "#1e40af",
        "color-admonition-title--warning": "#d97706",
        "color-admonition-title--caution": "#dc2626",
    },
    
    "dark_css_variables": {
        "color-brand-primary": "#3b82f6",
        "color-brand-content": "#60a5fa",
        "color-foreground-primary": "#f3f4f6",
        "color-foreground-secondary": "#d1d5db",
        "color-background-primary": "#1f2937",
        "color-background-secondary": "#111827",
        "color-background-border": "#374151",
    },
    
    "footer_icons": [
        {
            "name": "Support",
            "url": "https://enterprise.com/support",
            "html": "🎧",
        },
        {
            "name": "Training",
            "url": "https://enterprise.com/training",
            "html": "🎓",
        }
    ],
}

# Enterprise-specific CSS for additional branding
html_css_files = [
    "enterprise-branding.css",
    "compliance-styling.css",  # Accessibility compliance styles
]

# Additional enterprise features
html_context = {
    "display_version": True,
    "display_edit_on_github": False,  # Internal docs
    "conf_py_path": "/docs/source/",
}
```

## Summary & Best Practices

### Quick Start Checklist

1. **✅ Install Furo**: `pip install furo`
2. **✅ Basic config**: Set `html_theme = "furo"`
3. **✅ Brand colors**: Define light/dark CSS variables
4. **✅ Logo setup**: Add light/dark mode logos
5. **✅ Repository links**: Configure edit/view buttons
6. **✅ Custom CSS**: Add brand-specific styling
7. **✅ Test both modes**: Verify light/dark appearance
8. **✅ Accessibility check**: Ensure contrast ratios
9. **✅ Mobile test**: Check responsive behavior
10. **✅ Performance test**: Monitor build times

### Professional Tips

1. **Start Simple**: Begin with minimal config, add features gradually
2. **Brand Consistency**: Use your organization's exact colors
3. **Typography Matters**: Choose readable font stacks
4. **Dark Mode is Essential**: Always provide dark mode variables
5. **Test Everything**: Check all screen sizes and themes
6. **Accessibility First**: Use WCAG-compliant contrast ratios
7. **Performance Conscious**: Minimize custom CSS/JS
8. **Documentation**: Comment your customizations
9. **Version Control**: Track theme changes with git
10. **User Feedback**: Gather feedback on readability and usability

### Advanced Customization

For complex customizations beyond CSS variables:
- **Template overrides**: Copy templates to `_templates/`
- **Custom extensions**: Create Sphinx extensions for special features
- **Build scripts**: Automate theme asset generation
- **CI/CD integration**: Test documentation builds automatically

Remember: Furo's strength is in its simplicity and customizability through CSS variables. Start with the variables system before attempting more complex customizations.