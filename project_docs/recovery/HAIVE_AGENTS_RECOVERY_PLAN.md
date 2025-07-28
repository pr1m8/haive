# Haive-Agents Recovery and Merge Plan

**Created**: 2025-07-20
**Purpose**: Calculated merge to recover good features while fixing **init** import issues

## Current Situation

1. **Current State**: haive-agents at commit c8d0985 (July 18) - last good state before parse errors
2. **Parse Error Fix**: commit d0507af (July 20) - broke imports across 400+ files
3. **Enhanced Features**: commit c4e7f99 (July 20) - added enhanced agents on broken base
4. **Stashed Changes**: Contains all the broken state including type hints

## What We Need to Recover

### From Commit c4e7f99 (Enhanced Agents)

- ✅ `enhanced_supervisor_agent.py` - Already added back with correct imports
- ✅ `enhanced_react_agent.py` - Already added back with correct imports

### From Commit 3041de7 (Invalid Keyword Imports)

- Fixed invalid keyword imports in models
- Need to check if this affected actual code or just imports

### From Stash (Type Hints & More)

- Type hints for 835+ functions
- Any other enhancements that don't break imports

## **init**.py Files to Fix

### Critical **init** Files (Main Exports)

1. `/src/haive/agents/__init__.py` - Main package exports
2. `/src/haive/agents/base/__init__.py` - Base agent exports
3. `/src/haive/agents/multi/__init__.py` - Multi-agent exports
4. `/src/haive/agents/react/__init__.py` - React agent exports
5. `/src/haive/agents/simple/__init__.py` - Simple agent exports
6. `/src/haive/agents/rag/__init__.py` - RAG agent exports

### Import Pattern to Fix

```python
# ❌ WRONG (from parse error fix)
from agents.base import Agent
from multi.clean import MultiAgent
from react.agent import ReactAgent

# ✅ CORRECT
from haive.agents.base import Agent
from haive.agents.multi.clean import MultiAgent
from haive.agents.react.agent import ReactAgent
```

## Recovery Strategy

### Phase 1: Fix Critical **init** Files

1. [ ] Fix main agents **init**.py with correct imports
2. [ ] Fix base/**init**.py
3. [ ] Fix multi/**init**.py
4. [ ] Fix react/**init**.py
5. [ ] Fix simple/**init**.py
6. [ ] Fix rag/**init**.py

### Phase 2: Cherry-Pick Good Changes

1. [ ] Extract type hints from stash (without import changes)
2. [ ] Check commit 3041de7 for any useful fixes
3. [ ] Apply type hints using AST parsing

### Phase 3: Validate Everything

1. [ ] Test all imports work
2. [ ] Run pytest on affected modules
3. [ ] Build documentation

## Safe Recovery Commands

```bash
# Check specific file from stash
git show stash@{0}:src/haive/agents/some_file.py > /tmp/check_file.py

# Cherry-pick specific files from commit
git checkout c4e7f99 -- src/haive/agents/specific_file.py
# Then fix imports manually

# Extract type hints only
# Use AST parsing script to extract only type annotations
```

## Import Patterns to Maintain

### For haive-agents **init** files:

- Always use full `haive.agents.module.submodule` imports
- Never use relative imports in **init** files
- Always specify `__all__` exports

### Example Fixed **init**.py:

```python
"""Package description."""

# Full imports
from haive.agents.base.agent import Agent
from haive.agents.multi.clean import MultiAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent

__all__ = [
    "Agent",
    "MultiAgent",
    "ReactAgent",
    "SimpleAgent",
]
```

## Validation Checklist

After each fix:

- [ ] Run: `poetry run python -c "from haive.agents import Agent"`
- [ ] Run: `poetry run python -c "from haive.agents.multi import MultiAgent"`
- [ ] Run: `poetry run python -c "from haive.agents.react import ReactAgent"`
- [ ] Check no circular imports
- [ ] Verify **all** exports work

## Dependencies Between Packages

- haive-agents depends on haive-core
- haive-agents should NOT import from:
  - haive-tools
  - haive-games
  - haive-dataflow
  - haive-mcp
  - haive-prebuilt

## Next Steps

1. Start with fixing the main **init**.py files
2. Test each fix immediately
3. Only proceed if imports work
4. Document any issues found
