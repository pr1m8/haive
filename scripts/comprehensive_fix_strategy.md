# Comprehensive Fix Strategy for Haive Documentation Build

## 🔍 Current Situation

From the documentation audit, we have:
- **Total Issues**: 21,139
- **Critical Parse Errors**: 51 
- **Syntax Errors**: 195+ files with various syntax issues

## 🛠️ Available Tools

### 1. **Trunk** (Recommended for automated fixes)
```bash
# Fix all issues automatically in a specific package
cd packages/haive-core
trunk check --fix --all

# Fix specific types of issues
trunk check --fix --filter="ruff,black"

# Show what can be fixed without applying
trunk check --show-existing
```

### 2. **Documentation Scripts**
- `docs/scripts/documentation_audit.py` - Find all issues
- `docs/scripts/fix_parse_errors.py` - Fix parse errors from audit
- `docs/scripts/fix_prebuilt_init_files.py` - Fix init file issues

### 3. **Ruff** (Direct usage)
```bash
# Fix all fixable issues in a package
cd packages/haive-agents
poetry run ruff check --fix src/

# Fix specific error codes
poetry run ruff check --fix --select=E,W,F src/
```

### 4. **Black** (Code formatting)
```bash
# Format all Python files
cd packages/haive-core
poetry run black src/ tests/
```

## 📋 Step-by-Step Fix Process

### Phase 1: Fix Critical Parse Errors
```bash
# 1. Run trunk with auto-fix on each package
for package in haive-core haive-agents haive-tools haive-games haive-dataflow haive-mcp haive-prebuilt; do
    echo "Fixing $package..."
    cd packages/$package
    trunk check --fix --all
    cd ../..
done

# 2. Use ruff for remaining syntax issues
for package in haive-core haive-agents haive-tools haive-games haive-dataflow haive-mcp haive-prebuilt; do
    echo "Ruff fixing $package..."
    cd packages/$package
    poetry run ruff check --fix src/ tests/ --unsafe-fixes
    cd ../..
done
```

### Phase 2: Fix Documentation Issues
```bash
# 1. Run the audit to get current state
python docs/scripts/documentation_audit.py packages/ --format json --output docs/audit_results/current.json

# 2. Use existing fix script
python docs/scripts/fix_parse_errors.py

# 3. Add missing docstrings with custom script (see below)
```

### Phase 3: Package-Specific Fixes

#### For each package:
```bash
cd packages/haive-agents

# 1. Fix syntax and style issues
trunk check --fix --all
poetry run ruff check --fix src/ tests/
poetry run black src/ tests/

# 2. Check imports
poetry run isort src/ tests/

# 3. Type checking (identify issues, manual fix needed)
poetry run mypy src/

# 4. Test that everything still works
poetry run pytest tests/
```

## 🔧 Custom Fix Script for Common Issues

Create a script that combines all fixes:

```python
#!/usr/bin/env python3
"""Comprehensive fix script using all available tools."""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return success status."""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def fix_package(package_name):
    """Apply all fixes to a package."""
    package_path = Path(f"packages/{package_name}")
    
    if not package_path.exists():
        print(f"Package {package_name} not found")
        return False
    
    print(f"\n🔧 Fixing {package_name}...")
    
    # 1. Trunk auto-fix
    print("  Running trunk fix...")
    success, out, err = run_command("trunk check --fix --all", cwd=package_path)
    if success:
        print("  ✅ Trunk fixes applied")
    else:
        print(f"  ⚠️  Trunk had issues: {err}")
    
    # 2. Ruff fixes
    print("  Running ruff fix...")
    success, out, err = run_command("poetry run ruff check --fix src/ tests/ --unsafe-fixes", cwd=package_path)
    if success:
        print("  ✅ Ruff fixes applied")
    
    # 3. Black formatting
    print("  Running black...")
    success, out, err = run_command("poetry run black src/ tests/", cwd=package_path)
    if success:
        print("  ✅ Black formatting applied")
    
    # 4. isort imports
    print("  Running isort...")
    success, out, err = run_command("poetry run isort src/ tests/", cwd=package_path)
    if success:
        print("  ✅ Import sorting applied")
    
    return True

def main():
    packages = [
        "haive-core",
        "haive-agents", 
        "haive-tools",
        "haive-games",
        "haive-dataflow",
        "haive-mcp",
        "haive-prebuilt"
    ]
    
    for package in packages:
        fix_package(package)
    
    print("\n📊 Running final audit...")
    run_command("python docs/scripts/documentation_audit.py packages/ --output docs/audit_results/post_fix_audit.txt")

if __name__ == "__main__":
    main()
```

## 🎯 Specific Issue Fixes

### 1. Escape Sequence Warnings
```bash
# Use ruff to fix escape sequences
poetry run ruff check --fix --select=W605 src/
```

### 2. Unterminated String Literals
```bash
# These often need manual fixing, but trunk can catch many
trunk check --fix --filter="ruff"
```

### 3. Missing Docstrings
```bash
# Use docstring linters
poetry run pydocstyle src/ --add-ignore=D100,D101,D102
```

### 4. Type Hints
```bash
# Use mypy to identify, then fix manually
poetry run mypy src/ --install-types --non-interactive
```

## 🚀 Quick One-Liner for Everything

```bash
# Fix all issues in all packages
for p in packages/*; do cd "$p" && trunk check --fix --all && poetry run ruff check --fix src/ tests/ --unsafe-fixes && poetry run black src/ tests/ && cd ../..; done
```

## 📝 After Fixes

1. **Commit changes per package** (as they're submodules)
2. **Run tests** to ensure nothing broke
3. **Re-run documentation audit** to see remaining issues
4. **Build docs** to test if it works

```bash
# Test documentation build
cd docs
sphinx-build -b html source build
```