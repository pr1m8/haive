# Agent 2 Critical Error TODO List - Current Remaining

**Packages**: haive-core, haive-dataflow, haive-mcp, haive-prebuilt  
**Generated**: 2025-08-05  
**Updated After Agent 2 Previous Fixes**

## Progress Summary

- **Total Errors Fixed by Agent 2**: 240 ✅
- **Major Fixes Applied**: RAGState, TypeConverter, GitHubLoader, import paths, prebuilt modules
- **Agent 2 Critical Errors Remaining**: ~28 errors (estimated from 118 total)
- **Ready for Parallel Work**: Yes

## 🔴 Critical Error Groups for Agent 2

### Group 1: Already Fixed - Verify Resolution ✅

**These should be resolved by Agent 2's previous work**:

- ✅ RAGState imports (6-7 errors) - Agent 2 created the module
- ✅ TypeConverter imports (50+ modules unblocked) - Agent 2 fixed
- ✅ GitHubLoader imports (80+ modules unblocked) - Agent 2 fixed
- ✅ Prebuilt import paths (42 errors) - Agent 2 fixed

**Action**: Verify these are resolved in new analysis

### Group 2: Core Infrastructure Missing Modules (Priority 1)

**Impact**: Cross-package dependencies

**Focus Areas**:

1. **Schema Compatibility Issues** - Ensure TypeConverter fixes are complete
2. **Missing Core Schema Modules** - Any remaining core schema dependencies
3. **Engine Configuration Issues** - AugLLMConfig field mismatches

**Investigation Needed**:

- Run focused analysis on haive-core to find remaining critical imports
- Check for any schema modules still missing
- Verify engine configuration consistency

### Group 3: Dataflow Package Critical Issues (Priority 2)

**Known Patterns from Previous Analysis**:

1. **Import Path Errors** (some may remain)
   - API module path duplications
   - Database connection imports
   - Configuration import issues

2. **Logging and Exception Patterns** (lower priority but high volume)
   - G004: Logging format strings (1219 occurrences)
   - TRY401: Exception handling (391 occurrences)
   - DTZ005: Datetime timezone issues (248 occurrences)

**Fix Strategy**:

1. Focus on remaining critical import errors first
2. Address logging/exception patterns in batch fixes
3. Use automated tools for repetitive pattern fixes

### Group 4: MCP Package Critical Issues (Priority 2)

**Previous Fixes Applied**:

- ✅ GitHubLoader and WebScraper classes created
- ✅ Documentation imports fixed

**Remaining Focus**:

1. **Model Context Protocol specific errors**
2. **Integration import issues**
3. **Optional dependency handling**

### Group 5: Prebuilt Package Critical Issues (Priority 3)

**Previous Fixes Applied**:

- ✅ 42 import errors fixed
- ✅ 2 missing modules created
- ✅ NewsAPI optional dependency fixed

**Remaining Focus**:

1. **Agent configuration mismatches**
2. **Model field name inconsistencies**
3. **Dependencies on other package fixes**

## 📋 Implementation Strategy for Agent 2

### Phase 1: Verification & Analysis (Priority 1)

1. **Run updated error analysis** on Agent 2's packages only
2. **Verify previous fixes** are working correctly
3. **Identify truly remaining critical errors** after fixes applied

### Phase 2: Core Infrastructure Completion (Priority 1)

1. **Complete core schema modules** if any missing
2. **Fix remaining engine compatibility issues**
3. **Ensure cross-package dependencies resolved**

### Phase 3: Package-Specific Critical Fixes (Priority 2)

1. **Dataflow**: Focus on remaining import errors
2. **MCP**: Fix integration and protocol issues
3. **Prebuilt**: Complete agent configuration consistency

### Phase 4: High-Volume Pattern Fixes (Priority 3)

1. **Logging format fixes** (G004 pattern - 1219 in dataflow)
2. **Exception handling standardization** (TRY401 pattern)
3. **Type annotation completion** (mypy patterns)

## 🔧 Agent 2 Specific Commands

```bash
# Run analysis on Agent 2's packages only
poetry run python analyze_errors.py --packages haive-core,haive-dataflow,haive-mcp,haive-prebuilt --critical-only

# Test core infrastructure
poetry run python -c "from haive.core.schema.compatibility import TypeConverter; print('✅ TypeConverter works')"
poetry run python -c "from haive.core.schema.prebuilt.rag_state import RAGState; print('✅ RAGState works')"

# Test cross-package integration
poetry run python -c "from haive.mcp.documentation import GitHubLoader; print('✅ GitHubLoader works')"

# Verify prebuilt agents
poetry run python -c "from haive.prebuilt.misc import agent_utilities_models; print('✅ Prebuilt models work')"
```

## 📊 Expected Agent 2 Workload

**Verification Phase**: ~5-10 critical errors to confirm resolved  
**Core Infrastructure**: ~5-8 remaining critical core issues  
**Package-Specific**: ~10-15 remaining critical errors per package  
**Pattern Fixes**: ~2000+ low-priority style/type errors for batch processing

## 🤝 Coordination with Agent 1

### Clear Separation:

- **Agent 1**: haive-agents, haive-tools, haive-games (all agent implementation errors)
- **Agent 2**: haive-core, haive-dataflow, haive-mcp, haive-prebuilt (infrastructure & integration)

### No Cross-Dependencies Expected:

- Agent 2's RAGState fix unblocked Agent 1's RAG errors
- Agent 2's core fixes enable Agent 1's agent implementations
- Parallel work can proceed independently

### Communication:

- Share completion of major infrastructure fixes
- Coordinate on any unexpected cross-package dependencies
- Update progress in respective TODO files

## 🎯 Success Metrics for Agent 2

1. **Infrastructure Complete**: All core schema modules functional
2. **Integration Working**: MCP and dataflow imports resolved
3. **Prebuilt Agents**: Configuration consistency achieved
4. **Pattern Progress**: Bulk style/type fixes applied efficiently
5. **Cross-Package Support**: Agent 1 can work without waiting for Agent 2

## 🔍 Next Immediate Action

**Run Updated Analysis**: Get current state after Agent 2's 240 fixes to see true remaining critical errors:

```bash
cd /home/will/Projects/haive/backend/haive
poetry run python analyze_all_errors.py --output-dir error_analysis/current_state --packages haive-core,haive-dataflow,haive-mcp,haive-prebuilt --critical-only
```
