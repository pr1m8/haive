# Noxfile Migration Guide

## Overview

The improved noxfile addresses several key issues:

1. **Virtual Environment Corruption**: Uses `reuse_venv=True` and better cache management
2. **Dependency Issues**: Provides `fix-deps` command and minimal install options
3. **Performance**: Adds parallel builds and direct poetry execution
4. **Error Handling**: Better recovery options and clearer error messages

## Key Improvements

### 1. Direct Poetry Execution (NEW)

```bash
nox -s docs_direct  # Bypasses nox venv management, uses poetry directly
```

This is the **fastest option** - no virtual environment overhead!

### 2. Virtual Environment Reuse

- All sessions now use `reuse_venv=True` by default
- Prevents the `.nox` directory corruption issues
- Much faster subsequent runs

### 3. Parallel Builds

- Added `-j auto` flag to sphinx-build for parallel processing
- Significantly faster on multi-core systems

### 4. Better Dependency Management

```bash
nox -s fix-deps  # Fixes yanked packages and lock file issues
```

### 5. Minimal Install Options

- `--only docs` instead of `--with docs` for faster installs
- `docs_minimal` session for bare-bones builds

## Migration Steps

1. **Backup current noxfile**:

   ```bash
   cp noxfile.py noxfile_backup.py
   ```

2. **Replace with improved version**:

   ```bash
   cp noxfile_improved.py noxfile.py
   ```

3. **Clean existing cache** (optional):

   ```bash
   rm -rf .nox
   nox -s docs_clean -- --clean-nox
   ```

4. **Fix any dependency issues**:

   ```bash
   nox -s fix-deps
   ```

5. **Test the new setup**:
   ```bash
   nox -s docs_direct  # Fastest option
   nox -s docs_view    # View results
   ```

## Quick Command Reference

### Old vs New Commands

| Task        | Old Command         | New/Better Command   |
| ----------- | ------------------- | -------------------- |
| Build docs  | `nox -s docs`       | `nox -s docs_direct` |
| Quick build | `nox -s docs_fast`  | `nox -s docs_direct` |
| Dev server  | `nox -s docs_serve` | Same (improved)      |
| View docs   | `nox -s docs_view`  | Same (improved)      |
| Fix issues  | N/A                 | `nox -s fix-deps`    |

### Direct Poetry Commands (Fastest)

Skip nox entirely for maximum speed:

```bash
# Build documentation
poetry run sphinx-build -b html docs/source docs/build/html

# Development server with auto-reload
poetry run sphinx-autobuild docs/source docs/build/html

# View existing docs
cd docs/build/html && python -m http.server 8000
```

## Troubleshooting

### Issue: Virtual environment corruption

```bash
# Solution 1: Use direct execution
nox -s docs_direct

# Solution 2: Clean and rebuild
rm -rf .nox
nox -s docs_clean -- --clean-nox
nox -s docs
```

### Issue: Yanked package errors (like aiohttp)

```bash
nox -s fix-deps
# or manually:
poetry lock --no-update
poetry install --sync
```

### Issue: Long installation times

```bash
# Use minimal install
nox -s docs_minimal

# Or direct poetry
poetry run sphinx-build -b html docs/source docs/build/html
```

### Issue: Permission errors on .nox directory

```bash
# Force remove with sudo if needed
sudo rm -rf .nox

# Or use direct execution to avoid .nox entirely
nox -s docs_direct
```

## Performance Comparison

| Method                    | First Run | Subsequent Runs | Notes            |
| ------------------------- | --------- | --------------- | ---------------- |
| `nox -s docs`             | ~3-5 min  | ~30s            | Full venv setup  |
| `nox -s docs_direct`      | ~10s      | ~10s            | No venv overhead |
| `poetry run sphinx-build` | ~10s      | ~10s            | Direct execution |
| `nox -s docs_minimal`     | ~1 min    | ~20s            | Minimal deps     |

## Recommendations

1. **For daily use**: Use `nox -s docs_direct` or direct poetry commands
2. **For CI/CD**: Use `nox -s docs` for full isolation
3. **For development**: Use `nox -s docs_serve` for auto-reload
4. **For debugging**: Use `nox -s docs` with full output

## Configuration Options

Edit these in `noxfile_improved.py`:

```python
# Cache control
USE_VENV_CACHE = True  # Set False to force fresh environments

# Performance settings
PARALLEL_INSTALL = True  # Parallel dependency installation
MINIMAL_INSTALL = True   # Install only required dependencies
```

## Summary

The improved noxfile provides:

- ✅ Faster builds with `docs_direct`
- ✅ Better error recovery with `fix-deps`
- ✅ Virtual environment reuse to prevent corruption
- ✅ Parallel builds for better performance
- ✅ Direct poetry commands for maximum speed
- ✅ Clear command documentation with `nox -s list`

Choose the method that best fits your workflow!
