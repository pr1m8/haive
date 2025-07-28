# CSS and Layout Issues Analysis

**Purpose**: Document CSS problems and solutions for Furo theme

## Current Issues

### 1. "Everything Pushed to the Right"

**Symptoms**:

- Content appears far from left edge
- Excessive whitespace
- Poor use of screen space

**Root Causes**:

1. Sidebar width set to 30.5rem (488px)
2. Content margin-left: 320px hardcoded
3. Multiple CSS files conflicting

**Evidence**:

```css
/* In conf.py - DUPLICATE DEFINITIONS */
"sidebar-width": "30.5rem",  # Line 220
"sidebar-width": "30.5rem",  # Line 277 (duplicate!)
```

### 2. Code Blocks Too Narrow

**Symptoms**:

- Code blocks don't use full width
- Horizontal scrolling on short lines
- Poor readability

**Root Causes**:

1. Content area constrained
2. Pre/code max-width settings
3. Nested container issues

### 3. Sidebar Too Wide

**Current**: 494px (30.5rem)
**Should be**: ~300px (18-19rem)
**Impact**: Squeezes content area

## CSS File Analysis

### Current Files (3 files, 44KB total)

1. `haive-minimal.css` - 33KB (huge!)
2. `haive-enhanced.css` - 6KB
3. `haive-css-fixes.css` - 4KB

### Problems with Current Approach

- Fighting Furo with `!important`
- Hardcoded pixel values
- Not using CSS variables
- Multiple files = conflicts

## The Right Way: Work WITH Furo

### 1. Use Furo's CSS Variables

```python
# In conf.py
html_theme_options = {
    "light_css_variables": {
        # These are EXAMPLES - Furo doesn't document layout vars
        "color-sidebar-background": "#f8f9fb",
        "color-sidebar-link-text": "#333333",
        # We'll need custom CSS for layout
    }
}
```

### 2. Minimal Custom CSS

```css
/* furo-custom.css - Work WITH the theme */
:root {
  /* Layout adjustments */
  --sidebar-width: 19rem; /* ~304px */
  --content-width: 50rem;
  --content-padding-x: 2rem;
}

/* NO !important declarations */
.sidebar-drawer {
  width: var(--sidebar-width);
  max-width: var(--sidebar-width);
}

/* Code blocks */
.highlight pre {
  overflow-x: auto;
  /* Let it use available width */
}
```

### 3. Remove Problem CSS

**Delete or disable**:

- Hardcoded widths
- !important rules
- Pixel-based margins
- Fighting selectors

## Responsive Design Considerations

### Furo's Breakpoints

- Mobile: < 48em (768px)
- Tablet: < 67em (1072px)
- Desktop: > 67em

### Our Adjustments

```css
/* Tablet and below */
@media (max-width: 67em) {
  :root {
    --sidebar-width: 100%;
  }

  /* Sidebar becomes overlay */
  .sidebar-drawer {
    position: fixed;
    transform: translateX(-100%);
  }
}
```

## Implementation Strategy

### Phase 1: Clean Slate

1. Backup existing CSS
2. Remove all custom CSS
3. Use only Furo defaults
4. Document what's broken

### Phase 2: Minimal Fixes

1. Create single CSS file
2. Use CSS variables only
3. Fix critical issues only:
   - Sidebar width
   - Code block width
   - Basic spacing

### Phase 3: Progressive Enhancement

1. Test responsive behavior
2. Add typography improvements
3. Enhance API documentation
4. Polish interactions

## CSS Best Practices for Furo

### DO ✅

- Use CSS custom properties
- Work with Furo's structure
- Test responsive behavior
- Keep it minimal
- Use semantic units (rem, em)

### DON'T ❌

- Use !important
- Hardcode pixel values
- Fight the theme
- Create multiple CSS files
- Override core structure

## Testing CSS Changes

### 1. Visual Testing

```bash
# Build and serve
sphinx-build -b html docs/source docs/build/html
python -m http.server 8000 --directory docs/build/html

# Test at different widths:
# - Mobile: 375px
# - Tablet: 768px
# - Desktop: 1200px
# - Wide: 1920px
```

### 2. Debug Mode

```css
/* Temporary debug CSS */
* {
  outline: 1px solid rgba(255, 0, 0, 0.1);
}

.sidebar-drawer {
  background: rgba(0, 255, 0, 0.1);
}

.content {
  background: rgba(0, 0, 255, 0.1);
}
```

### 3. Browser DevTools

- Check computed styles
- Look for conflicts
- Test responsive modes
- Measure actual widths

## Common CSS Fixes

### Fix 1: Sidebar Width

```css
:root {
  --sidebar-width: 19rem;
}

.sidebar-drawer {
  width: var(--sidebar-width);
}
```

### Fix 2: Content Width

```css
.content {
  max-width: var(--content-width, 50rem);
  margin: 0 auto;
  padding: var(--content-padding-y, 2rem) var(--content-padding-x, 2rem);
}
```

### Fix 3: Code Blocks

```css
.highlight {
  margin: 1rem 0;
}

.highlight pre {
  overflow-x: auto;
  max-width: 100%;
}
```

### Fix 4: API Documentation

```css
/* Better spacing for API docs */
dl.py {
  margin: 2rem 0;
}

dl.py > dt {
  background: var(--color-api-background, #f8f9fa);
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
}
```

## Success Criteria

- [ ] Sidebar ~300px wide
- [ ] Content uses available space
- [ ] Code blocks full width
- [ ] No horizontal scrolling
- [ ] Responsive on mobile
- [ ] Single CSS file < 5KB
- [ ] No !important rules
- [ ] Fast page loads
