# Haive Scripts Organization

**Updated**: 2025-01-14  
**Purpose**: Comprehensive organization of all scripts and utilities  
**Structure**: Organized by function and frequency of use with complete README coverage

## 📁 Directory Structure

```
scripts/
├── automation/           # Automated workflows and CI/CD
├── build/               # Build and compilation utilities
├── development/         # Development utilities and helpers
│   ├── diagnostics/     # Diagnostic and analysis tools
│   ├── typing/          # Type checking and inference
│   └── git/            # Git utilities and analysis
├── maintenance/         # Code maintenance and fixes
│   ├── quick-fixes/     # One-off fix scripts
│   ├── docs/           # Documentation maintenance
│   └── imports/        # Import fixing utilities
├── testing/            # Testing utilities and validation
│   ├── docs/           # 🔥 Documentation testing suite
│   └── validators/     # Code validation tools
├── tools/              # General utilities and tools
└── archive/            # Deprecated/historical scripts
```

## 🔥 Key Script Categories

### 1. **Documentation Testing Suite** 🧪 **NEW & COMPREHENSIVE**

```bash
# Run complete documentation test suite
poetry run python scripts/testing/docs/run_docs_tests.py

# Individual test components
poetry run python scripts/testing/docs/docs_validation.py    # Structure validation
poetry run python scripts/testing/docs/css_audit.py         # CSS optimization
poetry run python scripts/testing/docs/path_resolution_test.py  # Link validation
poetry run python scripts/testing/docs/build_performance_test.py  # Performance analysis
```

**Features**: Real-time validation, CSS optimization, broken link detection, build performance analysis, health scoring

### 2. **Maintenance & Quick Fixes** 🔧 **RELIABLE & PROVEN**

```bash
# Quick syntax and validation fixes
poetry run python scripts/maintenance/quick-fixes/fix_syntax_errors.py
poetry run python scripts/maintenance/quick-fixes/fix_pydantic_validators.py

# Documentation maintenance
poetry run python scripts/maintenance/docs/cleanup_docs_directory.py
poetry run python scripts/maintenance/docs/enhanced_docs_build.py
```

**Results**: Proven track record with syntax fixes, Pydantic validation, and documentation cleanup

### 3. **Development Tools** 🚀 **WORKFLOW ENHANCERS**

```bash
# Git utilities and recovery
./scripts/development/stash_recovery_plan.sh
./scripts/development/analyze_stash_differences.sh

# Development safety tools
./scripts/development/safe-dev-changes.sh
./scripts/development/universal_pre_commit_capture.sh

# Diagnostics and analysis
poetry run python scripts/development/diagnostics/recommended_full_nitpick_ignore.py
```

**Features**: Git workflow support, safety protocols, diagnostics and analysis

### 4. **Typing & Code Quality** 📝 **TYPE SAFETY**

```bash
# Type hint generation and analysis
poetry run python scripts/development/typing/apply_auto_typing.py
poetry run python scripts/development/typing/apply_monkey_patches.py

# Code validation and testing
poetry run python scripts/testing/test_simpleagentv3_validation.py
poetry run python scripts/testing/test_autoapi_paths.py
```

**Features**: Automatic type hints, code patching, validation testing

## 📊 Recent Achievements

### ✅ **Documentation Testing Suite Implementation (2025-01-03)**

- **Created**: Comprehensive testing methodology for documentation issues
- **Components**: 5 specialized test scripts addressing structure, CSS, paths, and performance
- **Results**: Identified 700+ documentation issues with actionable recommendations
- **Impact**: Data-driven approach to documentation cleanup and optimization
- **Features**: Health scoring, comprehensive reporting, continuous validation capabilities

### ✅ **Scripts Organization & Cleanup (2025-01-14)**

- **Before**: 200+ scattered scripts across root and subdirectories
- **After**: Organized into 7 logical categories with clear purpose
- **Moved**: Root-level scripts to appropriate organized locations
- **Archived**: Historical/deprecated scripts with clear migration paths
- **Documentation**: Complete README coverage for all script categories
- **Active**: Focus on frequently-used, production-ready tools

### ✅ **Complete README Documentation Coverage (2025-01-14)**

- **Created**: 15+ comprehensive README files across all script directories
- **Coverage**: Every major script category now has detailed documentation
- **Standards**: Consistent format with purpose, usage, examples, and related links
- **Navigation**: Clear cross-references between related tools and categories
- **Benefits**: Improved discoverability and understanding of available tools

## 🔧 Most Common Usage Patterns

### Documentation Testing & Validation

```bash
# Complete documentation health check
poetry run python scripts/testing/docs/run_docs_tests.py

# Quick validation of documentation structure
poetry run python scripts/testing/docs/docs_validation.py

# CSS optimization analysis
poetry run python scripts/testing/docs/css_audit.py

# Build performance benchmarking
poetry run python scripts/testing/docs/build_performance_test.py
```

### Quick Fixes & Maintenance

```bash
# Fix syntax errors in codebase
poetry run python scripts/maintenance/quick-fixes/fix_syntax_errors.py

# Fix Pydantic validator issues
poetry run python scripts/maintenance/quick-fixes/fix_pydantic_validators.py

# Clean up documentation directory
poetry run python scripts/maintenance/docs/cleanup_docs_directory.py
```

### Development Workflow

```bash
# Git workflow and recovery
./scripts/development/stash_recovery_plan.sh
./scripts/development/safe-dev-changes.sh

# Type checking and validation
poetry run python scripts/testing/test_simpleagentv3_validation.py
poetry run python scripts/development/diagnostics/recommended_full_nitpick_ignore.py

# Pre-commit safety checks
./scripts/development/universal_pre_commit_capture.sh
```

### Build & Automation

```bash
# Documentation building
./scripts/build/build_docs.sh
./scripts/build/build_docs_realtime.sh

# Development server
./scripts/build/docs-server.sh
```

## 📚 Detailed Documentation

### Testing & Validation

- **[Documentation Testing Summary](testing/docs/TESTING_SUMMARY.md)** - Complete testing methodology guide
- **[Documentation Structure Analysis](../docs/source/conf_modules/README.md)** - Configuration and structure issues
- **[Testing Results](testing/docs/test_results/)** - Historical test results and reports

### Maintenance & Tools

- **[Maintenance Guide](maintenance/README.md)** - Deployment lessons learned and procedures
- **[Documentation Tools](doc_tools/README.md)** - Documentation generation utilities
- **[Development Tools](dev-tools/README.md)** - Development workflow enhancements

### Architecture & Standards

- **[CLAUDE.md](../CLAUDE.md)** - Main project hub & development memory
- **[Project Documentation](../project_docs/)** - Architecture & standards documentation
- **[Memory Index](../memory_index/)** - Chronological development history

## 🎯 Finding Scripts by Purpose

### By Function

- **Documentation**: `testing/docs/`, `maintenance/docs/`, `build/`
- **Code Quality**: `testing/`, `maintenance/quick-fixes/`, `development/diagnostics/`
- **Development**: `development/`, `tools/`, `automation/`
- **Build & CI**: `build/`, `automation/`

### By Frequency

- **Daily Use**: `testing/docs/`, `development/`, `maintenance/quick-fixes/`
- **Weekly Use**: `maintenance/docs/`, `build/`, `tools/`
- **Occasional**: `automation/`, `development/typing/`
- **Historical**: `archive/`

## 🔍 Quick Script Discovery

### Find Scripts by Keyword

```bash
# Find documentation-related scripts
find scripts/ -name "*doc*" -type f

# Find testing utilities
find scripts/ -name "*test*" -type f

# Find fix and maintenance scripts
find scripts/ -name "*fix*" -o -name "*maintenance*"

# Find validation tools
find scripts/ -name "*valid*" -o -name "*audit*"
```

### Most Useful Commands

```bash
# Documentation health check (most common)
poetry run python scripts/testing/docs/run_docs_tests.py

# Quick syntax fixes (frequent)
poetry run python scripts/maintenance/quick-fixes/fix_syntax_errors.py

# Development workflow (daily)
./scripts/development/safe-dev-changes.sh

# Build documentation (regular)
./scripts/build/build_docs.sh
```

## 📋 Script Standards

### Naming Convention

- **Action_Subject**: `fix_syntax_errors.py`
- **Category_Action**: `docs_validation.py`
- **Tool_Purpose**: `agent_run_capture.py`

### Documentation Requirements

Each script should have:

- Docstring with purpose and usage
- Command-line help (`--help`)
- Error handling and logging
- Example usage in comments

### Dependencies

- Use `poetry run` for all Python scripts
- Document any external tool dependencies
- Include error messages for missing dependencies

## 🚀 Next Steps

1. **Test the documentation suite** - Run comprehensive validation
2. **Explore organized structure** - Navigate by function and frequency
3. **Use appropriate tools** - Match scripts to your specific needs
4. **Check documentation** - Reference detailed guides for complex operations
5. **Follow safety practices** - Always validate before applying changes

---

**Quick Start**: Use `poetry run python scripts/testing/docs/run_docs_tests.py` to get a comprehensive overview of your documentation health, then explore other categories based on your needs.

**Navigation**: Scripts are organized by function (testing, maintenance, development, build, automation) and frequency of use (daily, weekly, occasional). Check the directory structure above or use the find commands to locate specific utilities.
