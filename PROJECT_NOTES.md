# Haive Monorepo Documentation Architecture - Project Notes

**Created:** 2025-01-12  
**Last Updated:** 2025-01-12  
**Status:** Active Development - Documentation System Migration

---

## 📋 Executive Summary

This document captures the journey of migrating PyAutoDoc's sophisticated 43-extension documentation system to Haive's hybrid mono-polyrepo structure. We've successfully created a shared documentation configuration but face challenges with Python import paths across different build contexts.

---

## 🏗️ Repository Architecture

### Current Structure
```
haive/
├── packages/              # User-facing packages (polyrepo style)
│   ├── haive-core/       # Core framework (git submodule)
│   ├── haive-agents/     # Agent implementations
│   ├── haive-tools/      # User tools/utilities
│   ├── haive-games/      # Game environments
│   ├── haive-dataflow/   # Data processing
│   ├── haive-mcp/        # MCP server integration
│   └── haive-prebuilt/   # Pre-built agents
├── tools/                 # Development tools
│   └── haive-docs/       # Shared documentation config
├── src/                   # Root source (empty - packages use PEP 420)
├── docs/                  # Central documentation hub
└── pyproject.toml        # Root poetry configuration
```

### Key Architectural Insights
- **Hybrid Mono-Polyrepo**: Monorepo structure with polyrepo practices
- **PEP 420 Namespace**: Implicit namespace packages (no __init__.py in haive/)
- **Git Submodules**: haive-core is a submodule with its own repository
- **Development vs User Tools**: Clear separation (tools/ vs packages/)

---

## 🎯 Current Challenge: Import Path Resolution

### The Problem
`haive-docs` provides shared Sphinx configuration but needs to be importable from multiple contexts:

1. **Root Level Build**: `/home/will/Projects/haive/backend/haive/`
2. **Package Level Build**: `/home/will/Projects/haive/backend/haive/packages/haive-core/`
3. **Docs Directory Build**: `/home/will/Projects/haive/backend/haive/packages/haive-core/docs/`

Each location has different relative paths to `tools/haive-docs/`.

### Import Statement
```python
from haive_docs.config import get_haive_config
```

### Current Status
- ✅ haive-docs created with 600+ line configuration
- ✅ Added to root pyproject.toml as dev dependency
- ❌ Import fails when building from package directories
- ❓ Need solution for consistent imports across contexts

---

## 🔍 Issues and Concerns

### 1. **Import Path Inconsistency**
- **Issue**: Relative path from root differs from package paths
- **Impact**: Can't build docs from package directories
- **Severity**: 🔴 High - Blocks distributed documentation

### 2. **Namespace Conflicts**
- **Issue**: Attempted `haive_development` namespace caused Poetry conflicts
- **Impact**: Can't have package name matching root project name
- **Severity**: 🟡 Medium - Found workaround with separate tools

### 3. **Dependency Duplication**
- **Issue**: Each package might need its own haive-docs dependency
- **Impact**: Maintenance overhead, version sync challenges
- **Severity**: 🟡 Medium - Manageable with automation

### 4. **Submodule Complications**
- **Issue**: haive-core as git submodule adds complexity
- **Impact**: Different git context, potential CI/CD issues
- **Severity**: 🟡 Medium - Requires special handling

### 5. **Build Context Variations**
- **Issue**: Sphinx can be run from multiple directories
- **Impact**: Configuration must work in all contexts
- **Severity**: 🔴 High - Core functionality requirement

---

## 💡 Approaches Considered

### Approach 1: Separate Tools Directory (Current)
**Structure**: Keep development tools in `tools/` directory
```
tools/
├── haive-docs/
├── haive-cli/
└── haive-dev/
```
**Pros**: Clean separation, no naming conflicts  
**Cons**: Import path challenges  
**Status**: ✅ Implemented for haive-docs

### Approach 2: Development Namespace Package (Failed)
**Structure**: Create `haive_development` namespace in src/
```
src/haive_development/
├── docs/
├── cli/
└── dev/
```
**Pros**: Clean imports  
**Cons**: Poetry naming conflict with root project  
**Status**: ❌ Abandoned due to conflicts

### Approach 3: Integration with haive-tools Package
**Structure**: Add dev tools to existing `packages/haive-tools/`
**Pros**: Uses existing package structure  
**Cons**: Mixes user and dev tools  
**Status**: ❌ Rejected - wrong separation of concerns

### Approach 4: Distributed Dependencies
**Structure**: Add haive-docs to each package's pyproject.toml
**Pros**: Each package self-contained  
**Cons**: Duplication, maintenance overhead  
**Status**: 🤔 Under consideration

---

## 🛠️ Implementation Details

### What We've Built
1. **haive-docs Package** (`tools/haive-docs/`)
   - 600+ line Sphinx configuration from PyAutoDoc
   - Supports all 43 extensions
   - Provides `get_haive_config()` and `get_central_hub_config()`
   - Installable Python package with entry points

2. **Package Documentation Structure**
   ```
   packages/haive-core/
   └── docs/
       └── source/
           ├── conf.py       # Imports from haive_docs
           ├── index.rst
           └── _static/
   ```

3. **Central Hub Configuration**
   - Uses sphinx-collections for aggregation
   - Can pull from all 7 packages
   - Provides unified documentation site

### Configuration Architecture
```python
# In haive_docs/config.py
def get_haive_config(
    package_name: str,
    package_path: str, 
    is_central_hub: bool = False,
    extra_extensions: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Generate Sphinx configuration for any Haive package."""
```

---

## 🤔 Considerations

### Technical Considerations
1. **Python Path Management**
   - Need consistent PYTHONPATH across environments
   - Consider using .env files or shell scripts
   - May need different approaches for dev vs CI/CD

2. **Poetry Workspace Feature**
   - Poetry doesn't have true workspace support like npm/yarn
   - Each package has independent dependencies
   - Root pyproject.toml uses path dependencies

3. **Documentation Build Performance**
   - 7 packages × 43 extensions = potential for slow builds
   - Consider parallel builds or caching
   - May need selective extension loading

4. **Version Synchronization**
   - How to ensure haive-docs version consistency?
   - Automated updates vs manual coordination
   - Consider using poetry groups

### Organizational Considerations
1. **Developer Experience**
   - Should work with minimal setup
   - Clear error messages when haive-docs missing
   - Good defaults for common cases

2. **CI/CD Integration**
   - GitHub Actions needs proper Python path
   - Consider containerized builds
   - Cache dependencies for speed

3. **Documentation Standards**
   - Enforce consistent structure across packages
   - Shared templates and assets
   - Unified styling and branding

---

## 📊 Decision Matrix

| Solution | Import Simplicity | Maintenance | Flexibility | CI/CD Friendly |
|----------|------------------|-------------|-------------|----------------|
| Root Install Only | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Package Install Each | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| PYTHONPATH Export | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| PyPI Package | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🚀 Recommended Path Forward

### Short Term (Immediate)
1. **Dual Installation Approach**
   - Keep haive-docs in root dev dependencies
   - Add to each package's docs dependencies with relative paths
   - Document the setup process clearly

2. **Build Scripts**
   - Create `scripts/build-docs.sh` with proper PYTHONPATH
   - Package-specific build helpers
   - Unified build command for all packages

### Medium Term (This Week)
1. **Test Coverage**
   - Verify builds work from all contexts
   - Set up CI/CD documentation builds
   - Create integration tests

2. **Documentation**
   - Complete setup guide
   - Package author guidelines
   - Troubleshooting guide

### Long Term (Future)
1. **Consider PyPI Publication**
   - Private PyPI or GitHub packages
   - Version management strategy
   - Automated releases

2. **Enhanced Tooling**
   - VSCode tasks for doc building
   - Pre-commit hooks for doc validation
   - Documentation coverage reports

---

## 📝 Open Questions

1. **Should haive-docs be versioned independently or with Haive?**
2. **How to handle breaking changes in documentation config?**
3. **Should each package maintain its own changelog?**
4. **What's the strategy for documentation deployment?**
5. **How to handle private vs public documentation?**

---

## 🔗 Related Documents

- `/home/will/Projects/pyautodoc/PROJECT_STATUS.md` - PyAutoDoc implementation details
- `/home/will/Projects/pyautodoc/COMMON_ISSUES.md` - Known issues and solutions
- `/home/will/Projects/haive/backend/haive/tools/haive-docs/README.md` - haive-docs documentation

---

## 📌 Current Action Items

1. [ ] Implement dual installation approach
2. [ ] Create build scripts with proper Python paths
3. [ ] Test documentation builds from all contexts
4. [ ] Document the setup process
5. [ ] Set up CI/CD for documentation

---

**Next Review Date**: 2025-01-15  
**Owner**: Haive Development Team  
**Status**: 🟡 Active Development - Path forward identified, implementation pending