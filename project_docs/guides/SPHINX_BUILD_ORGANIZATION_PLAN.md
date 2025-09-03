# Sphinx Build Organization Plan

## Current State Analysis

### Problems Identified:
- **Scattered build directories**: `docs/build/`, `docs/source/_build/`, `docs/debug_build/`, etc.
- **Build artifacts in source**: Confuses Sphinx incremental builds
- **No persistent doctree location**: Cache gets lost, causing full rebuilds
- **Hundreds of log files**: Scattered across multiple directories

### Current Build Directories Found:
```
/docs/build
/docs/build/test-build
/docs/debug_build  
/docs/source/_build
/docs/source/build_minimal
/docs/debug_trace_build
```

## Proposed Clean Structure (Option 1)

```
docs/
├── source/                 # ONLY source files (clean)
│   ├── conf.py
│   ├── index.rst
│   ├── _static/
│   └── _templates/
├── builds/                 # ALL build outputs here
│   ├── html/              # Main production HTML
│   ├── doctrees/          # PERSISTENT cache (key for incremental!)
│   ├── logs/              # All build logs organized
│   │   ├── 2025-08-07/
│   │   └── latest.log
│   ├── debug/             # Debug builds
│   ├── test/              # Test builds
│   └── minimal/           # Minimal builds
└── scripts/               # Build helper scripts
    ├── build-clean.sh
    ├── build-watch.sh
    └── build-debug.sh
```

## Key Configuration Changes Needed

### 1. Update conf.py Build Paths
```python
# In conf.py - set consistent build directories
import os
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
docs_root = project_root / "docs"

# Define clean build structure
BUILDS_DIR = docs_root / "builds"
HTML_DIR = BUILDS_DIR / "html"
DOCTREES_DIR = BUILDS_DIR / "doctrees"  # PERSISTENT CACHE
LOGS_DIR = BUILDS_DIR / "logs"

# Ensure directories exist
for dir_path in [BUILDS_DIR, HTML_DIR, DOCTREES_DIR, LOGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)
```

### 2. Standard Build Commands
```bash
# Clean incremental build (preserves doctrees cache)
sphinx-build -d docs/builds/doctrees -b html docs/source docs/builds/html

# Full rebuild when needed
sphinx-build -E -a -d docs/builds/doctrees -b html docs/source docs/builds/html

# Debug build
sphinx-build -d docs/builds/doctrees -b html docs/source docs/builds/debug

# With logging
sphinx-build -d docs/builds/doctrees -b html docs/source docs/builds/html 2>&1 | tee docs/builds/logs/build-$(date +%Y%m%d-%H%M%S).log
```

### 3. Environment Variables for Flexibility
```bash
# Set these in your shell or build scripts
export SPHINX_SOURCE_DIR="docs/source"
export SPHINX_BUILD_DIR="docs/builds/html" 
export SPHINX_DOCTREE_DIR="docs/builds/doctrees"
export SPHINX_LOG_DIR="docs/builds/logs"
```

## Migration Steps (When Current Build Finishes)

### Phase 1: Create New Structure (Non-destructive)
1. Create `docs/builds/` directory structure
2. Update conf.py with new paths
3. Test build with new structure
4. Verify incremental builds work

### Phase 2: Migrate Existing Builds (Optional)
1. Copy current `docs/build/html` → `docs/builds/html`
2. Move logs to `docs/builds/logs/archive/`
3. Clean up old scattered directories

### Phase 3: Update Build Scripts
1. Update nox sessions to use new paths
2. Create convenience scripts
3. Update documentation

## Benefits of This Organization

### ✅ Clean Separation
- Source directory only contains source files
- All build outputs in dedicated `builds/` directory
- Easy to add to `.gitignore`

### ✅ Persistent Incremental Builds  
- Consistent doctree location preserves cache
- Builds resume from where they left off
- No more full rebuilds after errors

### ✅ Better Debugging
- Organized log files by date
- Debug builds separate from production
- Easy to compare different build types

### ✅ CI/CD Friendly
- Clear input/output separation
- Easy to cache `doctrees/` directory
- Predictable build artifacts location

## Current Build Command Detection

To implement this, we need to identify:
1. How you currently run builds (nox? make? direct sphinx-build?)
2. Any CI/CD scripts that need updating
3. IDE configurations that reference build paths

## Notes for Implementation

**IMPORTANT**: Wait for current build to complete before making any changes!

**Configuration References to Add**:
- Update `.gitignore` to exclude `docs/builds/` 
- Update any IDE workspace settings
- Update CI/CD build commands
- Update documentation references to build paths

**Testing Plan**:
1. Test incremental build behavior
2. Test build failure recovery  
3. Test different build types (html, debug, minimal)
4. Verify doctree cache persistence