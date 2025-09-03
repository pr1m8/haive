# Import Maintenance

**Purpose**: Import statement management, dependency cleanup, and module organization
**Usage**: Maintaining clean import structures, resolving circular dependencies, and optimizing imports

## 📄 Current Scripts

### Import Optimization

- **`fix_circular_imports.py`** - Resolve circular dependency issues
- **`optimize_imports.py`** - Clean up and organize import statements
- **`validate_import_structure.py`** - Validate package import hierarchy

### Dependency Management

- **`update_dependencies.py`** - Update and validate package dependencies
- **`check_unused_imports.py`** - Identify and remove unused imports
- **`standardize_imports.py`** - Enforce consistent import patterns

## 🚀 Common Tasks

### Import Cleanup

```bash
# Resolve circular import issues
poetry run python scripts/maintenance/imports/fix_circular_imports.py

# Optimize import statements
poetry run python scripts/maintenance/imports/optimize_imports.py

# Check for unused imports
poetry run python scripts/maintenance/imports/check_unused_imports.py
```

### Structure Validation

```bash
# Validate import hierarchy
poetry run python scripts/maintenance/imports/validate_import_structure.py

# Standardize import patterns
poetry run python scripts/maintenance/imports/standardize_imports.py
```

## 🔧 Import Standards

### Best Practices

- **Explicit imports**: Use full module paths
- **Consistent ordering**: Standard library, third-party, local imports
- **No circular dependencies**: Maintain clean dependency graph
- **Minimal imports**: Import only what's needed

### Common Issues

- **Circular imports**: Between agent and engine modules
- **Unused imports**: Leftover from refactoring
- **Inconsistent patterns**: Mixed import styles
- **Deep nesting**: Overly complex import paths

## 📊 Import Categories

### Core Framework

```python
# Correct patterns
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.prebuilt.messages_state import MessagesState
```

### Agent Imports

```python
# Consistent agent imports
from haive.agents.simple.agent_v3 import SimpleAgentV3
from haive.agents.react.agent import ReactAgent
```

### Tool Imports

```python
# Tool integration patterns
from langchain_core.tools import Tool, tool
from haive.tools.search import WebSearchTool
```

## 🔍 Dependency Analysis

### Package Hierarchy

```
haive-core: Foundation (no dependencies on other haive packages)
├── haive-agents: Depends on haive-core
├── haive-tools: Depends on haive-core
├── haive-games: Depends on haive-core, haive-agents
└── haive-mcp: Depends on haive-core
```

### Forbidden Dependencies

- **Core → Agents**: Core should not import from agents
- **Agents → Games**: Agents should not depend on games
- **Circular references**: Any package importing from itself through others

## 🚀 Maintenance Benefits

### Code Quality

- Clean, readable import statements
- Eliminated circular dependencies
- Consistent import patterns
- Reduced complexity

### Development Experience

- Faster import resolution
- Clear dependency relationships
- Easier refactoring
- Better IDE support

## 🔗 Related

- **[Quick Fixes](../quick-fixes/README.md)** - Immediate import fixes
- **[Development Tools](../../development/README.md)** - Development workflow
- **[Testing Suite](../../testing/docs/README.md)** - Import validation
