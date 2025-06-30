# Serving Documentation - Quick Guide

## Quick Start

The documentation has been successfully built! Here's how to serve it:

### Option 1: Using Python's built-in server (Simplest)

```bash
cd docs/build/html
python -m http.server 8000
```

Then open http://localhost:8000 in your browser.

### Option 2: Using sphinx-autobuild (Auto-reload)

```bash
cd /home/will/Projects/haive/backend/haive
poetry run sphinx-autobuild docs/source docs/build/html --port 8000
```

This will:
- Watch for changes in source files
- Automatically rebuild when changes are detected
- Auto-refresh your browser

### Option 3: Using nox (Recommended)

```bash
cd /home/will/Projects/haive/backend/haive
nox -s docs_serve
```

This uses the nox session we created that handles everything automatically.

## Current Status

✅ **Documentation built successfully** with 1765 warnings (mostly formatting issues)
✅ **HTML files generated** in `docs/build/html/`
✅ **Ready to serve**

## Addressing Warnings

The warnings are primarily:
1. **Title underline length** issues in RST files
2. **Docstring formatting** issues (inline literals, indentation)
3. **Grid structure** issues in showcase pages

These don't prevent the docs from being usable but should be fixed over time.

## Next Steps

1. **Serve the docs** using one of the methods above
2. **Browse** to verify everything looks correct
3. **Fix warnings** gradually by:
   - Running the fix script periodically
   - Updating docstrings to follow Google style
   - Fixing RST formatting issues

---

The documentation is ready to use!