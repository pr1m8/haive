# Haive Codebase Recovery Plan

**Created**: July 20, 2025  
**Purpose**: Track and fix import issues while preserving good changes from July 18-20

## 🚨 Current Situation Summary

### Timeline of Events

1. **April 17, 2025**: Project inception
   - haive-core initial commit
   - Basic structure established

2. **June 26, 2025**: General mixins added (commit 9fe7c2d)
   - IdMixin, MetadataMixin, SerializationMixin
   - StateMixin, TimestampMixin, VersionMixin
   - These are in `src/haive/core/common/mixins/general/`

3. **July 11-14**: Major PostgreSQL/Persistence improvements
   - **July 11**: Implemented secure SecretStr serialization (commit 915ec70) ✅ HAVE THIS
   - **July 14**: Multiple important features:
     - Enhanced PostgresSaver with secure serialization (commit 4615f1d) ❌ MISSING
     - PostgreSQL store wrappers (commit 79c4800)
     - Human-in-the-loop tool wrapper (commit 6cd1ec5)
     - Haive Core Tools for memory management (commit 87641da)

4. **Friday July 18**: Peak productivity day
   - **haive-core** (b970f90): Last good commit before issues
   - **haive-agents** (d79a5dc): Enhanced MultiAgent with structured output and routing
   - Added 2,550+ type hints across all packages (8:30 PM)
   - Added NodeSchemaComposer documentation
   - Implemented RegistryCacheManager

5. **Saturday/Sunday July 20**: The breaking point
   - **4:15 PM**: haive-agents "fix: eliminate all parse errors" (commit d0507af)
   - **4:17 PM**: haive-core "fix: eliminate parse errors" (commit 97af89f)
   - **4:19 PM**: Enhanced agents added on top of broken code (commit c4e7f99)
   - These "fixes" removed module paths from imports, breaking 400+ files

### Current State

- **haive-core**: At b970f90 (July 18) - has SecretStr fix but missing enhanced PostgresSaver
- **haive-agents**: At c8d0985 (July 18) - has MultiAgent enhancements
- Missing: Type hints, enhanced agents, timestamp_mixin, persistence improvements
- Imports work but we lost many improvements from July 18-20

## 📋 Recovery Strategy

### Phase 1: Inventory Missing Features

Track what we need to recover from the stashed changes:

#### haive-core Missing Features

- [ ] `timestamp_mixin.py` - Timestamp tracking functionality
- [ ] `persistence_types.py` - Renamed from types.py to avoid conflicts
- [ ] Type hints for 858 functions
- [ ] Enhanced mixins in `common/mixins/`
- [ ] RegistryCacheManager improvements
- [ ] NodeSchemaComposer examples

#### haive-agents Missing Features

- [ ] Type hints for 835 functions
- [ ] Enhanced agent patterns
- [ ] Possible new agents added
- [ ] Improved tool management
- [ ] Documentation updates

#### Other Packages

- [ ] haive-tools: 67 functions with type hints
- [ ] haive-dataflow: 208 functions with type hints
- [ ] haive-games: 408 functions with type hints
- [ ] haive-mcp: 106 functions with type hints
- [ ] haive-prebuilt: 68 functions with type hints

### Key Improvements to Recover

#### PostgreSQL/Persistence Enhancements (haive-core)

Based on commit history, these improvements were made:

1. **Secure SecretStr Serialization** - PostgreSQL persistence now properly handles SecretStr
2. **Enhanced PostgresSaver** - Improved async counterparts with secure serialization
3. **New Persistence Manager** - `engine/agent/persistence/manager.py` for better state management
4. **PostgreSQL Store Wrappers** - New wrappers for store functionality
5. **Supabase Support** - Enhanced Supabase configuration
6. **Connection Pooling** - Better PostgreSQL connection management

#### Agent Enhancements (haive-agents)

From commit c4e7f99 (July 20, 4:19 PM):

1. **Enhanced Supervisor Agent** - `multi/enhanced_supervisor_agent.py`
2. **Enhanced React Agent** - `react/enhanced_react_agent.py`
3. **MultiAgent Improvements** - Structured output formatting and routing capabilities
4. **Debug Scripts** - Focused debugging for msgpack serialization

### Phase 2: Recovery Actions

#### Step 1: Extract Good Files from Stash

```bash
# Create a recovery directory
mkdir -p /tmp/haive_recovery

# Extract specific good files from stash
git stash show -p stash@{0} -- src/haive/core/common/mixins/timestamp_mixin.py > /tmp/haive_recovery/timestamp_mixin.patch
```

#### Step 2: Fix Import Patterns

Create a script to fix the broken import patterns:

- Change: `from engine.X import Y`
- To: `from haive.core.engine.X import Y`

#### Step 3: Apply Type Hints Selectively

- Extract type hint changes without import modifications
- Apply using AST parsing to preserve correct imports

## 🎯 Action Items Tracker

### Immediate Priority

1. [ ] Create backup of current working state
2. [ ] Extract timestamp_mixin.py with correct imports
3. [ ] Create import fixing script
4. [ ] Test import fixes on one file first

### File-by-File Recovery

#### haive-core Recovery List

| File                                     | Status      | Issue                                    | Action                          |
| ---------------------------------------- | ----------- | ---------------------------------------- | ------------------------------- |
| `persistence/types.py`                   | ❌ Missing  | Need to rename from persistence_types.py | Extract and fix imports         |
| `persistence/postgres_config.py`         | ⚠️ Enhanced | PostgreSQL security improvements         | Extract enhancements            |
| `persistence/postgres_saver_override.py` | ⚠️ Enhanced | Secure serialization for SecretStr       | Extract and fix                 |
| `common/mixins/timestamp_mixin.py`       | ❌ Missing  | Not in current commit                    | Extract from stash, fix imports |
| `common/mixins/__init__.py`              | ⚠️ Broken   | Bad imports in stash                     | Manually fix imports            |
| `engine/__init__.py`                     | ✅ Working  | Has correct imports                      | Keep current version            |
| `engine/agent/persistence/`              | ❌ Missing  | New persistence manager                  | Extract entire directory        |

#### haive-agents Recovery List

| File                                 | Status                | Issue                           | Action                      |
| ------------------------------------ | --------------------- | ------------------------------- | --------------------------- |
| Multiple agent files                 | ⚠️ Missing type hints | 835 functions need hints        | Apply type hints carefully  |
| `multi/enhanced_supervisor_agent.py` | ❌ Missing            | New enhanced supervisor         | Extract from commit c4e7f99 |
| `react/enhanced_react_agent.py`      | ❌ Missing            | New enhanced React agent        | Extract from commit c4e7f99 |
| Enhanced patterns commit             | ❌ Lost               | Commit c4e7f99 had improvements | Cherry-pick specific files  |

## 🛠️ Recovery Scripts Needed

### 1. Import Fixer Script

```python
# fix_imports.py
import re
import os

def fix_imports_in_file(filepath):
    """Fix broken imports in a Python file."""
    # Pattern to fix imports missing module path
    patterns = [
        (r'from (engine|persistence|schema|graph|common)\.', r'from haive.core.\1.'),
        (r'from (agents|tools|dataflow|games|mcp|prebuilt)\.', r'from haive.\1.'),
    ]
    # Implementation here...
```

### 2. Type Hint Extractor

```python
# extract_type_hints.py
import ast
import os

def extract_type_hints_only(old_file, new_file):
    """Extract only type hint changes, preserve imports."""
    # Parse both files with AST
    # Compare function signatures
    # Apply only type hint differences
```

## 📊 Progress Tracking

### Package Recovery Status

- [ ] haive-core (0/858 type hints recovered)
- [ ] haive-agents (0/835 type hints recovered)
- [ ] haive-tools (0/67 type hints recovered)
- [ ] haive-dataflow (0/208 type hints recovered)
- [ ] haive-games (0/408 type hints recovered)
- [ ] haive-mcp (0/106 type hints recovered)
- [ ] haive-prebuilt (0/68 type hints recovered)

### Critical Files Recovery

- [ ] timestamp_mixin.py
- [ ] persistence_types.py
- [ ] All **init**.py files with correct imports
- [ ] Type hint automation tools
- [ ] Documentation improvements

## 🔍 Validation Checklist

After each recovery step:

1. [ ] Run `poetry run python -c "import haive.core; import haive.agents"`
2. [ ] Run `poetry run pytest` on affected package
3. [ ] Run `poetry run mypy` to check type hints
4. [ ] Build docs with `nox -s docs`

### PostgreSQL/Persistence Specific Tests

5. [ ] Test PostgreSQL connection: `poetry run pytest packages/haive-core/tests/persistence/test_postgres_config.py -v`
6. [ ] Test SecretStr serialization: `poetry run python -c "from haive.core.persistence import PostgresCheckpointerConfig"`
7. [ ] Test async persistence: `poetry run pytest packages/haive-core/tests/persistence/test_db_connection_postgres_async.py -v`
8. [ ] Verify persistence manager: `poetry run python -c "from haive.core.engine.agent.persistence.manager import PersistenceManager"`

## 📝 Lessons Learned

1. **Never trust automated "fix all" scripts** without reviewing changes
2. **Always check import statements** when fixing syntax errors
3. **Commit frequently** with small, focused changes
4. **Test imports after each change**
5. **Use AST parsing** instead of regex for Python code modifications

## 🚀 Next Steps

1. Start with recovering `timestamp_mixin.py` as a test case
2. Create and test the import fixer script
3. Systematically recover features package by package
4. Document each successful recovery

## 🔑 Key Commits to Cherry-Pick

### haive-core

1. **4615f1d** (July 14) - Enhanced PostgresSaver with secure serialization
2. **Stash changes** - timestamp_mixin.py and other mixins
3. **Type hints** - 858 functions from automated improvements

### haive-agents

1. **c4e7f99** (July 20) - Enhanced supervisor and React agents
   - `multi/enhanced_supervisor_agent.py`
   - `react/enhanced_react_agent.py`
2. **Type hints** - 835 functions from automated improvements

## 📊 Priority Recovery Order

### High Priority (Core Functionality)

1. **PostgreSQL/Persistence Improvements**
   - SecretStr serialization fix (critical for production)
   - Persistence manager for better state management
   - Async PostgreSQL improvements

2. **Core Mixins**
   - timestamp_mixin.py (widely used)
   - Other general mixins (id, metadata, serialization, state, version)

3. **Enhanced Agents**
   - enhanced_supervisor_agent.py (better multi-agent coordination)
   - enhanced_react_agent.py (improved reasoning loop)

### Medium Priority (Developer Experience)

4. **Type Hints** (2,550+ across all packages)
   - Start with haive-core (858 functions)
   - Then haive-agents (835 functions)

5. **Automation Tools**
   - type_hint_analyzer.py
   - type_hint_fixer.py
   - Other development tools

### Low Priority (Nice to Have)

6. **Documentation Improvements**
7. **Test Enhancements**
8. **Example Scripts**

## 🎯 Recovery Success Criteria

- [ ] All imports working without errors
- [ ] PostgreSQL persistence functioning with SecretStr
- [ ] Timestamp mixin available and working
- [ ] Enhanced agents recoverable
- [ ] At least 50% of type hints recovered
- [ ] Core functionality fully restored
- [ ] Tests passing for recovered components

---

**Remember**: Take it slow, test each change, and preserve the working imports above all else.
