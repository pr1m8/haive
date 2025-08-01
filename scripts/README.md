# Haive Development Scripts

**Version**: 2.0  
**Last Updated**: 2025-08-01  
**Status**: Organized & Production Ready

## 🎯 Overview

This directory contains development, maintenance, and automation scripts for the Haive framework. All scripts follow our **dry-run first, safety-focused** approach with comprehensive validation and backup strategies.

## 📁 Directory Structure

```
scripts/
├── README.md                 # This file - your navigation hub
├── typing/                   # 🔥 NEW: Auto-typing & monkey patching
│   ├── apply_auto_typing.py     # Automatic type hint generation
│   ├── apply_monkey_patches.py  # Runtime code patching
│   └── README.md               # Comprehensive typing guide
├── maintenance/              # Core maintenance & lazy loading
│   ├── apply_lazy_loading.py    # ✅ Main lazy loading deployment script
│   ├── smart_dryrun_wrapper.py  # Universal dry-run wrapper
│   ├── generalized_lazy_loading.py
│   └── README.md               # Lazy loading deployment guide
├── documentation/            # Documentation generation & tools
│   ├── doc_tools/              # Documentation utilities
│   ├── doc_utils/              # Documentation generators
│   └── builders/               # Documentation build scripts
├── development/              # Development & analysis tools
│   ├── debug/                  # Debugging utilities
│   ├── dev/                    # Development tools
│   ├── migration/              # Migration scripts
│   └── analysis/               # Code analysis tools
└── archive/                  # 📦 Archived/legacy scripts
    ├── syntax_fixes/           # Old syntax fix scripts
    ├── analysis/               # Legacy analysis scripts
    └── testing/                # Archived test scripts
```

## 🚀 Most Important Scripts

### 1. **Auto-Typing System** 🔥 **NEW & RECOMMENDED**

```bash
# Generate type hints automatically
poetry run python scripts/typing/apply_auto_typing.py --target haive-tools --dry-run
poetry run python scripts/typing/apply_auto_typing.py --target haive-tools --confirm

# Generate stub files (.pyi) without modifying source
poetry run python scripts/typing/apply_auto_typing.py --target haive-core --stubs-only

# Professional-quality stubs with mypy
poetry run python scripts/typing/apply_auto_typing.py --target haive-agents --mypy-stubgen
```

**Features**: AST-based type inference, confidence scoring, MyPy integration, stub generation

### 2. **Lazy Loading System** ✅ **PROVEN & DEPLOYED**

```bash
# Apply lazy loading to packages (6/7 packages successfully deployed)
poetry run python scripts/maintenance/apply_lazy_loading.py --target haive-tools --dry-run
poetry run python scripts/maintenance/apply_lazy_loading.py --target haive-tools --confirm
```

**Results**: 70% import time reduction, successfully deployed across haive-core, haive-tools, haive-games, haive-dataflow, haive-mcp, haive-prebuilt

### 3. **Universal Dry-Run Wrapper** 🛡️ **SAFETY FIRST**

```bash
# Wrap any command with intelligent dry-run
poetry run python scripts/maintenance/smart_dryrun_wrapper.py --target "ruff check packages/" --dry-run
```

**Features**: Smart command modification, safety confirmation, project-aware execution

### 4. **Monkey Patching System** 🐒 **EXPERIMENTAL**

```bash
# Apply runtime code patches safely
poetry run python scripts/typing/apply_monkey_patches.py --target haive-agents --dry-run
poetry run python scripts/typing/apply_monkey_patches.py --target haive-agents --interactive
```

**Features**: Runtime enhancement, bug fixes, capability injection, rollback support

## 📊 Success Stories

### ✅ **Lazy Loading Deployment (2025-07-29)**

- **Packages**: 6/7 successfully implemented (haive-agents deferred)
- **Performance**: ~70% import time reduction
- **Approach**: Dry-run validation → manual fixes → automated deployment
- **Challenge**: haive-dataflow required extensive debugging (broken imports, wrong model locations)
- **Outcome**: All packages now have working lazy loading with comprehensive documentation

### ✅ **Scripts Cleanup & Organization (2025-08-01)**

- **Before**: 100+ scattered files, duplicated functionality
- **After**: Organized structure with clear navigation
- **Archived**: 50+ legacy syntax fix scripts to `archive/`
- **Active**: Focus on proven, reusable tools

## 🔧 Quick Commands Reference

### Development Workflow

```bash
# 1. Always check current state
git status && git diff

# 2. Create safety backup
git checkout -b safety-backup-$(date +%Y%m%d-%H%M%S)
git add . && git commit -m "Safety backup before script execution"
git checkout main

# 3. Run dry-run first
poetry run python scripts/[category]/script.py --target package --dry-run

# 4. Apply with confirmation
poetry run python scripts/[category]/script.py --target package --confirm

# 5. Validate results
poetry run python -c "from haive.package import *; print('✅ Imports work')"
poetry run pytest packages/package/tests/ -v
```

### Common Tasks

```bash
# Add type hints to a package
poetry run python scripts/typing/apply_auto_typing.py --target haive-tools --dry-run

# Apply lazy loading to a package
poetry run python scripts/maintenance/apply_lazy_loading.py --target haive-mcp --dry-run

# Debug test performance
poetry run python scripts/development/debug/diagnose_test_performance.py

# Check poetry lock files
poetry run python scripts/development/dev/check_poetry_locks.py

# Build documentation
poetry run python scripts/documentation/builders/safe_docs_build.py
```

## 📚 Detailed Guides

### For Auto-Typing & Monkey Patching:

- **[Complete Typing Guide](typing/README.md)** - Comprehensive documentation
- Type inference strategies, confidence scoring, stub generation
- Monkey patching patterns, safety protocols, rollback procedures

### For Lazy Loading & Maintenance:

- **[Maintenance Scripts Guide](maintenance/README.md)** - Deployment lessons learned
- Package complexity analysis, backup strategies, recovery procedures
- Real-world examples from our 6/7 package deployment

### For Documentation:

- **[Documentation Tools](documentation/doc_tools/README.md)** - Documentation generation
- **[Documentation Utils](documentation/doc_utils/README.md)** - Documentation utilities

## 🚨 Critical Safety Guidelines

### **ALWAYS Follow This Sequence**:

1. **🔍 Research First**

   ```bash
   # Understand what you're working with
   find packages/target-package -name "*.py" | head -10
   poetry run python -c "import haive.target_package; print('Current state works')"
   ```

2. **🛡️ Backup Everything**

   ```bash
   # Git-based backup (preferred)
   git checkout -b safety-backup-$(date +%Y%m%d-%H%M%S)
   git add . && git commit -m "Safety backup before [operation]"
   git checkout main

   # File-based backup (additional safety)
   cp important_file.py important_file.py.backup.$(date +%Y%m%d-%H%M%S)
   ```

3. **🧪 Dry-Run Everything**

   ```bash
   # NEVER skip dry-run mode
   poetry run python scripts/category/script.py --target package --dry-run
   # Review output carefully before proceeding
   ```

4. **✅ Validate Results**

   ```bash
   # Test imports still work
   poetry run python -c "from haive.package import *; print('✅ Imports work')"

   # Run tests
   poetry run pytest packages/package/tests/ -v

   # Check with MyPy (for typing changes)
   poetry run mypy packages/package/src/
   ```

### **Recovery Procedures**:

**If Scripts Break Imports**:

```bash
# Restore from git backup
git checkout safety-backup-YYYYMMDD-HHMMSS -- path/to/broken/file.py

# Or restore from file backup
cp important_file.py.backup important_file.py
```

**If Entire Package Breaks**:

```bash
# Nuclear option - restore entire package
git checkout safety-backup-YYYYMMDD-HHMMSS -- packages/broken-package/
```

## 🏗️ Script Development Guidelines

### When Creating New Scripts:

1. **Follow the Dry-Run Pattern**:

   ```python
   parser.add_argument('--dry-run', action='store_true',
                      help='Validate without applying changes')

   if args.dry_run:
       logger.info("🧪 DRY-RUN MODE: No changes will be applied")
       # Show what would be done
       return
   ```

2. **Include Safety Confirmations**:

   ```python
   if risky_operation and interactive:
       response = input("Continue with risky operation? [y/N]: ")
       if response.lower() not in ['y', 'yes']:
           logger.info("🛑 User cancelled operation")
           return
   ```

3. **Comprehensive Logging**:

   ```python
   logger.info(f"🔍 Discovering targets in {package}")
   logger.info(f"✅ Found {len(targets)} targets")
   logger.info(f"🎉 Successfully processed {success_count} targets")
   ```

4. **Rollback Capabilities**:

   ```python
   # Store originals for rollback
   self.original_objects[key] = original_value

   def rollback(self):
       for key, original in self.original_objects.items():
           restore_original(key, original)
   ```

## 📈 Performance & Metrics

### Lazy Loading Impact:

- **haive-core**: 93 components → ~2s import time reduction
- **haive-tools**: 15+ tools → ~1.5s import time reduction
- **haive-games**: 32+ games → ~3s import time reduction
- **Total**: ~70% cold import performance improvement

### Auto-Typing Capabilities:

- **Type inference**: 85% accuracy for basic types
- **Confidence scoring**: 0.9+ for primitives, 0.7+ for generics
- **Stub generation**: Both custom and MyPy stubgen support
- **Safety**: Comprehensive dry-run validation

## 🔗 Related Documentation

- **[CLAUDE.md](../CLAUDE.md)** - Main project hub & development memory
- **[Memory Index](../memory_index/)** - Chronological development history
- **[Project Docs](../project_docs/)** - Architecture & standards documentation
- **[Package Documentation](../project_docs/packages/)** - Package-specific guides

## 🎯 Future Roadmap

### Planned Enhancements:

1. **Auto-typing improvements**: Better generic inference, Protocol support
2. **Lazy loading expansion**: haive-agents package completion
3. **Monkey patching library**: Common patch patterns as reusable modules
4. **CI/CD integration**: Automated dry-run validation in GitHub Actions

### Script Maintenance:

1. **Regular cleanup**: Archive outdated scripts quarterly
2. **Documentation updates**: Keep guides current with implementations
3. **Performance monitoring**: Track script execution times and success rates
4. **User feedback**: Incorporate lessons learned from real usage

---

**Remember**: All scripts in this directory are designed with **safety first** principles. Always run dry-run mode, create backups, and validate results. The goal is to enhance development productivity while maintaining code quality and stability.

**Need Help?** Check the specific README files in each subdirectory, or refer to our comprehensive guides in the [Memory Index](../memory_index/) for real-world usage examples and troubleshooting.
