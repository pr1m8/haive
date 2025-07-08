# Haive Documentation Navigation Structure

## Overview

The documentation now uses a hierarchical navigation structure with Haive as the root, following the pattern you requested:

```
haive (root)
├── core (package)
│   ├── engine (module)
│   │   ├── base (submodule)
│   │   ├── aug_llm (submodule)
│   │   └── ...
│   ├── schema (module)
│   │   ├── state_schema (submodule)
│   │   └── ...
│   └── ...
├── agents (package)
│   ├── simple (module)
│   │   ├── structured (submodule)
│   │   └── ...
│   └── ...
└── ...
```

## URL Structure

The new URL pattern follows:

- Root: `/api/haive/index.html`
- Package: `/api/haive/core/index.html`
- Module: `/api/haive/core/engine/index.html`
- Submodule: `/api/haive/core/engine/base.html`

## Features Implemented

1. **Hierarchical Navigation**
   - Haive as the root with all packages as subdirectories
   - Consistent module-based pattern throughout
   - Each level has its own index page with overview

2. **Contextual Sidebar**
   - Sidebar changes based on current location
   - Shows relevant modules/submodules for current package
   - Expands current section automatically

3. **Breadcrumb Navigation**
   - Shows path: API Reference > Haive > Package > Module
   - Quick navigation back to any level

4. **Enhanced Styling**
   - Package overview cards with icons
   - Module grids for easy navigation
   - Highlighted current location in sidebar

## Files Created/Modified

1. **Navigation Scripts**
   - `restructure_navigation.py` - Generates new structure
   - `update_sidebar_structure.py` - Updates main index

2. **CSS Enhancements**
   - `haive-navigation.css` - New navigation styles

3. **JavaScript Updates**
   - `contextual-navigation.js` - Updated for new URL pattern

4. **Configuration**
   - `conf.py` - Updated with navigation depth and new CSS

## Viewing the Documentation

The documentation server is running at: http://localhost:8002

Key pages to visit:

- Main API: http://localhost:8002/api/haive/index.html
- Core Package: http://localhost:8002/api/haive/core/index.html
- Engine Module: http://localhost:8002/api/haive/core/engine/index.html
- Base Submodule: http://localhost:8002/api/haive/core/engine/base.html

## Navigation Behavior

1. **Global Navigation**: Available from any page via sidebar
2. **Contextual Focus**: Current package/module expanded
3. **Quick Access**: Grid cards for visual navigation
4. **Module Paths**: Clear display of import paths
