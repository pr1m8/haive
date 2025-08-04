# Documentation Import Issues Analysis

**Date**: 2025-01-04
**Purpose**: Comprehensive analysis of all import errors preventing documentation build
**Status**: Analysis Phase - No fixes applied yet

## Overview

The documentation build is failing due to multiple import errors across the haive packages. This document catalogs all identified issues and provides a plan for systematic fixes.

## Import Error Categories

### 1. Chain Module Issues (BranchSpec)

**Error Pattern**: `ImportError - cannot import name 'BranchSpec' from 'haive.agents.chain.declarative_chain'`

**Affected Files**:
- `haive.agents.chain`
- `haive.agents.chain.chain_agent_simple`
- `haive.agents.chain.examples`
- `haive.agents.chain.examples_simple`
- `haive.agents.chain.extended_examples`
- `haive.agents.chain.multi_integration`

**Root Cause**: Missing `BranchSpec` class or import in `declarative_chain.py`

**Fix Strategy**: 
- Check if `BranchSpec` exists in the module
- Add to mock imports if it's a complex dependency
- Consider excluding chain modules from documentation if they're experimental

### 2. Archive Meta Module Issues

**Error Pattern**: `ImportError - cannot import name 'get_summary' from 'haive.agents.archive.meta.agent'`

**Affected Files**:
- `haive.agents.archive.meta`

**Root Cause**: Missing `get_summary` function in the meta agent module

**Fix Strategy**:
- Check if function exists and is properly exported
- Add to mock imports or exclude archive modules

### 3. Document Modifiers Issues

**Error Pattern**: `ImportError - cannot import name 'normalize_contents'`

**Affected Files**:
- `haive.agents.document_modifiers.kg.kg_iterative_refinement`
- `haive.agents.document_modifiers.kg.kg_iterative_refinement.engines`
- `haive.agents.document_modifiers.summarizer.iterative_refinement`
- `haive.agents.document_modifiers.summarizer.iterative_refinement.example`

**Root Cause**: Missing `normalize_contents` function in state modules

**Additional Issues**:
- `ImportError - cannot import name 'ParallelKGAgentConfig'` in kg_map_merge modules

**Fix Strategy**:
- Check if functions exist in their expected locations
- Add missing functions or mock them
- Consider excluding document_modifiers if they're incomplete

### 4. Long Term Memory Issues

**Error Pattern**: `ImportError - cannot import name 'AgentState' from 'haive.agents.react.state'`

**Affected Files**:
- `haive.agents.long_term_memory`
- `haive.agents.long_term_memory.agent`
- `haive.agents.long_term_memory.engines`

**Root Cause**: Missing `AgentState` class in react.state module

**Fix Strategy**:
- Check if AgentState exists in react package
- Create the missing class or mock it
- Verify if long_term_memory is using the correct import path

### 5. Generic Class Type Issues

**Error Pattern**: `TypeError - <class 'haive.agents.react.agent.ReactAgent'> is not a generic class`

**Affected Files**:
- `haive.agents.conversation.base.example`
- `haive.agents.experiments.*`

**Root Cause**: Attempting to use ReactAgent and BaseConversationAgent as generic types with type parameters

**Fix Strategy**:
- Remove generic type usage where inappropriate
- Fix type annotations to use proper generic syntax
- Add proper TypeVar definitions if needed

### 6. Missing Module Dependencies

**Error Pattern**: `ModuleNotFoundError - No module named 'examples.usage_examples'`

**Affected Files**:
- `haive.agents.document_loader.examples`
- `haive.agents.document_loader.examples.usage_examples`

**Root Cause**: Missing or incorrectly referenced modules

**Fix Strategy**:
- Create missing modules or fix import paths
- Add to autoapi_ignore if they're not essential

### 7. Missing Dependencies (External)

**Warning Pattern**: `Failed to initialize Google **** tool: google-search-results is not installed`

**Affected Tools**:
- Google Finance
- Google Jobs  
- Google Scholar
- Google Trends

**Root Cause**: Optional dependencies not installed

**Fix Strategy**:
- Add to mock imports (already partially done)
- Document as optional dependencies

### 8. Multi-Agent Module Issues

**Error Pattern**: Various import errors in multi-agent modules

**Affected Files**:
- Multiple files in `haive.agents.multi.*`
- Missing modules referenced from multi-agent configs

**Root Cause**: Refactoring or incomplete module implementations

**Fix Strategy**:
- Review multi-agent architecture
- Fix missing imports or mock them
- Update import paths after refactoring

### 9. Memory and State Issues

**Error Patterns**:
- Missing unified_memory_api imports
- State schema conflicts
- Memory reorganization import issues

**Affected Areas**:
- Memory management modules
- State handling
- Recently reorganized memory modules

**Fix Strategy**:
- Review memory reorganization impacts
- Fix import paths
- Update module exports

## Current Mitigation in conf.py

### Already Excluded via autoapi_ignore:
- All examples and test files
- Archive directories
- Research and planning agents (incomplete)
- Multi-agent experimental modules
- Tools with missing dependencies
- Memory v2 modules (Pydantic issues)

### Already Mocked via autodoc_mock_imports:
- External tool dependencies (alpha_vantage, amadeus, etc.)
- LangChain community modules
- Games framework modules
- MCP modules
- Basic chain and state imports

## Recommended Fix Priority

### High Priority (Blocking Documentation)
1. **Chain Module BranchSpec** - Most frequent error
2. **Generic Type Issues** - Affects multiple modules
3. **Long Term Memory AgentState** - Core functionality

### Medium Priority (Reduce Noise)
1. **Document Modifiers** - Exclude if incomplete
2. **Archive Meta Modules** - Exclude if deprecated
3. **Missing Usage Examples** - Fix or exclude

### Low Priority (Warnings Only)
1. **External Dependencies** - Already partially handled
2. **Experimental Modules** - Can remain excluded

## Systematic Fix Plan

### Phase 1: Quick Wins (Mock/Exclude)
- Add all missing imports to autodoc_mock_imports
- Expand autoapi_ignore patterns for problematic modules
- Test build to verify error reduction

### Phase 2: Code Fixes
- Fix actual missing functions/classes where feasible
- Update import paths after module reorganization
- Fix generic type usage

### Phase 3: Architecture Review
- Review chain module completeness
- Assess long_term_memory module status
- Clean up experimental/deprecated modules

## Files to Examine for Fixes

### Chain Module:
- `packages/haive-agents/src/haive/agents/chain/declarative_chain.py`

### React State:
- `packages/haive-agents/src/haive/agents/react/state.py`

### Archive Meta:
- `packages/haive-agents/src/haive/agents/archive/meta/agent.py`

### Document Modifiers:
- `packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_iterative_refinement/state.py`
- `packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/config.py`

### Generic Type Issues:
- `packages/haive-agents/src/haive/agents/conversation/base/example.py`
- `packages/haive-agents/src/haive/agents/experiments/*.py`

## Next Steps

1. **Review this analysis** with the development team
2. **Choose fix strategy** for each category (mock vs. fix vs. exclude)
3. **Implement fixes systematically** starting with high priority
4. **Test documentation build** after each fix category
5. **Update this document** as fixes are applied

## Notes

- Some modules may be experimental or deprecated - confirm before fixing
- Generic type issues may indicate broader architectural concerns
- Consider creating a "documentation-ready" build profile that excludes experimental modules
- Monitor for new import errors introduced by ongoing development