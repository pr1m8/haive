# Agent 1 Critical Error TODO List - Current Remaining

**Packages**: haive-agents, haive-tools, haive-games  
**Generated**: 2025-08-05  
**Updated After Agent 2 Fixes**

## Progress Summary

- **Agent 1 Packages Critical Errors**: ~90 errors (estimated from 118 total)
- **Agent 2 Already Fixed**: RAGState imports (~6 errors resolved)
- **Ready for Parallel Work**: Yes

## 🔴 Critical Error Groups for Agent 1

### Group 1: Planning Module `should_continue` Function (Priority 1)

**Impact**: ~15 modules blocked

**Missing Function**: `should_continue` in `haive.agents.planning.plan_and_execute_multi`

**Affected Files**:

- planning/**init**.py (ID: 3f0906f5)
- planning/base/**init**.py (ID: 75f8f2c4)
- planning/base/agents/**init**.py (ID: 191d36d5)
- planning/base/models.py (ID: 56d22de5)
- planning/llm_compiler/**init**.py (ID: 96092425)
- planning/llm_compiler_v3/**init**.py (ID: 956a5284)
- planning/llm_compiler_v3/models.py (ID: 7210caf2)
- planning/plan_and_execute/**init**.py (ID: 2ec57118)
- planning/plan_and_execute/models.py (ID: 72ef7ef2)
- planning/plan_and_execute/v2/**init**.py (ID: b5216115)
- planning/plan_and_execute/v2/models.py (ID: 59e43f3c)
- planning/rewoo/**init**.py (ID: 9e6fc4ed)
- planning/rewoo/models/**init**.py (ID: ad83df47)

**Fix Strategy**:

1. Examine `haive.agents.planning.plan_and_execute_multi.py`
2. Add missing `should_continue` function
3. Test imports work across all planning modules

### Group 2: LangChain Tokenizer Import Errors (Priority 1)

**Impact**: 3 modules blocked

**Issue**: `tokenizer` no longer available in `langchain_core.messages`

**Affected Files**:

- long_term_memory/**init**.py (ID: 2a050eee)
- long_term_memory/agent.py (ID: 9b054315)
- long_term_memory/state.py (ID: b8767f4e)

**Fix Strategy**:

1. Check LangChain changelog for tokenizer replacement
2. Update imports to use correct tokenizer location
3. Test long_term_memory module imports

### Group 3: Chain Module Missing Classes (Priority 2)

**Impact**: 2 modules blocked

**Missing Items**:

- `StrategyDecision` from `haive.agents.chain.examples` (ID: 79aa000b)
- `build_graph` from `haive.agents.rag.hyde.agent_v2` (ID: 28ce1335, b5824698)

**Fix Strategy**:

1. Check if these classes exist but aren't exported
2. Create missing classes if needed
3. Fix chain module imports

### Group 4: Memory Search Functions Missing (Priority 2)

**Impact**: 2 modules blocked

**Missing Functions**:

- `format_search_context` from `haive.agents.memory.search.base` (ID: 56a67986, e9453a77)
- `extract_memory_items` from `haive.agents.memory_reorganized.search.base` (ID: e563e0b0)

**Fix Strategy**:

1. Add missing functions to search base modules
2. Implement basic functionality for memory search
3. Test memory module imports

### Group 5: Supervisor Module Missing (Priority 2)

**Impact**: 2 modules blocked

**Missing Module**: `haive.agents.experiments.supervisor.base_supervisor`

**Affected Files**:

- experiments/supervisor.py (ID: 73105d6c)
- experiments/supervisor/**init**.py (ID: fde7c888)

**Fix Strategy**:

1. Create missing base_supervisor.py module
2. Add basic supervisor class structure
3. Fix supervisor module imports

### Group 6: RAG Module Missing External Imports (Priority 3)

**Impact**: Multiple modules blocked

**Problematic Patterns** (importing non-existent external packages):

- `from agentic.agent import` (ID: 929072df)
- `from document_graders.comprehensive_grader import` (ID: 98e163ab, e7cb628f)
- `from corrective.agent import` (ID: 2caed35f, d101344e)
- `from sql_rag.agent import` (ID: 94d5942c, 2f7fc6ae, 965460a4)
- `from flare.agent import` (ID: 73a6fad8, 413d3495)
- `from fusion.agent import` (ID: d9e89b87, 597b94bd)
- `from llm_rag.agent import` (ID: 79feaf76)
- `from multi_strategy.agent import` (ID: c8fa9d59)
- `from self_corr.agent import` (ID: 6c0e51a0)
- `from react_agent.agent import` (ID: a607ddc3)
- `from react_v3.agent import` (ID: c9e384e6)

**Fix Strategy**:

1. Change imports to use relative haive.agents imports
2. Create missing local modules as needed
3. Remove dependencies on external packages

### Group 7: React Agent Missing Functions (Priority 3)

**Impact**: Multiple modules blocked

**Missing Functions**:

- `add_tool` from `advanced_agent3` (ID: 16a43fd8, 3d61c21c, 7cd60057, 302febd6, 6e50e673)
- `run` from `react_v2.agent` (ID: 15d2b565)
- `from_llms` from `lats.config` (ID: 7d3fa0fd, 8a03adce)

**Fix Strategy**:

1. Add missing functions to respective modules
2. Implement basic functionality
3. Test react agent imports

### Group 8: Graph DB Missing Function (Priority 3)

**Impact**: 1 module blocked

**Missing Function**: `check_domain_relevance` from `haive.agents.rag.db_rag.graph_db.agent`

**Affected File**: rag/db_rag/graph_db/**init**.py (ID: 8cfd02cb)

**Fix Strategy**:

1. Add `check_domain_relevance` function to graph_db agent
2. Implement basic domain checking logic
3. Test graph_db imports

## 📋 Implementation Strategy for Agent 1

### Phase 1: High-Impact Quick Fixes (Priority 1)

1. **Fix `should_continue` function** - Unblocks 15 modules
2. **Fix tokenizer imports** - Unblocks 3 modules
3. **Fix chain module classes** - Unblocks 2 modules

### Phase 2: Medium-Impact Fixes (Priority 2)

4. **Fix memory search functions** - Unblocks 2 modules
5. **Create supervisor module** - Unblocks 2 modules

### Phase 3: External Import Cleanup (Priority 3)

6. **Fix external package imports** - Convert to local imports
7. **Add missing react agent functions**
8. **Fix remaining graph db functions**

## 🔧 Tools and Commands

```bash
# Test specific error fix
poetry run python -c "from haive.agents.planning.plan_and_execute_multi import should_continue"

# Test module imports after fix
poetry run python -c "from haive.agents.planning import *"

# Run error analysis on specific package
poetry run python analyze_errors.py --package haive-agents --critical-only
```

## 📊 Expected Impact

**Phase 1 Completion**: ~20 modules unblocked (~22% of critical errors)  
**Phase 2 Completion**: ~24 modules unblocked (~27% of critical errors)  
**Phase 3 Completion**: ~40+ modules unblocked (~45%+ of critical errors)

## 🤝 Coordination with Agent 2

- **Agent 2 has fixed**: RAGState imports (no longer critical)
- **Agent 2 should focus on**: Their assigned packages (core, dataflow, mcp, prebuilt)
- **Parallel work ready**: Yes, minimal cross-dependencies remaining
