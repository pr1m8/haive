# Import Fixes Needed - 2025-07-29 14:37

## 🔧 Immediate Fixes Required

### 1. Fix haive.agents.chain Import
**Problem**: `__init__.py` imports functions that don't exist in `chain_agent_simple.py`

**Missing functions**:
- `add` (imported but not defined)
- `branch` (imported but not defined)  
- `build` (exists as method, not standalone function)
- `flow` (imported but not defined)

**Fix**:
```python
# Edit packages/haive-agents/src/haive/agents/chain/__init__.py
# Remove missing imports:
from haive.agents.chain.chain_agent_simple import (
    ChainAgent,
    FlowBuilder,
    # add,        # <- REMOVE (doesn't exist)
    # branch,     # <- REMOVE (doesn't exist)
    # build,      # <- REMOVE (method only)
    # build_graph,# <- REMOVE (method only)  
    # flow,       # <- REMOVE (doesn't exist)
)
```

### 2. Fix haive.dataflow.registry Import  
**Problem**: Import tries `haive.dataflow.registry.registry` but structure is different

**Current structure**:
- `packages/haive-dataflow/src/haive/dataflow/registry.py` (file)
- `packages/haive-dataflow/src/haive/dataflow/registry/` (directory)

**Fix**: Check which one should be imported and fix the import path

### 3. Fix haive.mcp Import
**Problem**: `generate_setup_script` doesn't exist in current MCP library

**Fix**: Check current MCP CLI API and update imports

## 🎯 Action Plan
1. **Fix chain imports first** (most frequent error)
2. **Check registry structure** 
3. **Update MCP compatibility**
4. **Re-run build**

## 📝 Commands to Run
```bash
# 1. Fix chain imports
vim packages/haive-agents/src/haive/agents/chain/__init__.py

# 2. Check registry structure  
ls -la packages/haive-dataflow/src/haive/dataflow/registry*

# 3. Check MCP API
python -c "from mcp import cli; print(dir(cli))"

# 4. Re-run build
./docs/scripts/build_docs_fast.sh --background
```