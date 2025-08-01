# Quick Import Fix with Ruff

Since you already have Ruff configured with TID252 in your pyproject.toml, here's the simplest approach:

## 1. Fix Relative Imports with Ruff

```bash
# Dry run - see what would be changed
poetry run ruff check packages/haive-core/src --select TID252 --show-fixes

# Actually fix them
poetry run ruff check packages/haive-core/src --select TID252 --fix
```

## 2. Fix Missing Imports with autoimport

Since autoimport is also configured in pyproject.toml with `force_absolute_imports = true`:

```bash
# Check what needs fixing
poetry run autoimport --check packages/haive-core/src/haive/core

# Fix all import issues
poetry run autoimport packages/haive-core/src/haive/core
```

## 3. Fix All Packages at Once

```bash
# Fix relative imports in all packages
poetry run ruff check packages/ --select TID252 --fix

# Fix missing imports in all packages
for pkg in packages/haive-*/src; do
    echo "Fixing imports in $pkg"
    poetry run autoimport $pkg
done
```

## What's Already Configured

In your `pyproject.toml`:

### Ruff Configuration:
```toml
[tool.ruff.lint]
select = [
    "TID251",
    "TID252",  # enforce absolute imports
]
```

### Autoimport Configuration:
```toml
[tool.autoimport]
disable_move_to_top = false
force_absolute_imports = true  # This is key!

[tool.autoimport.import_rules]
prefer_absolute = ["haive.*"]
flag_relative_imports = true
auto_fix_imports = true
```

## Quick One-Liner

Fix everything in haive-core:

```bash
# Fix relative imports then missing imports
poetry run ruff check packages/haive-core/src --select TID252 --fix && \
poetry run autoimport packages/haive-core/src
```

## Verify Results

After running:

```bash
# Check for any remaining issues
poetry run ruff check packages/haive-core/src --select TID252
poetry run autoimport --check packages/haive-core/src

# Run Sphinx to see if errors are fixed
poetry run sphinx-build -b html docs/source docs/build/html
```