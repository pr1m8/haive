# Structured Output Consolidation Guide

**Reference**: @STRUCTURED_OUTPUT_CONSOLIDATION_GUIDE.md  
**Topic**: Multi-layer field syncing in structured output systems  
**Research Date**: 2025-08-08

## Key Insights from Research

### The Core Problem

Multi-layer syncing issue where `AugLLMConfig` defines `structured_output_model` but it doesn't properly sync through the engine to the agent, causing structured output parsing failures.

### Architecture Flow

```
AugLLMConfig.structured_output_model → Engine.structured_output_model → Agent.structured_output_model
```

### Primary Issues Identified

1. **Field Syncing Gap**: `setup_agent()` doesn't sync `structured_output_model` from AugLLMConfig/engine
2. **Fallback Chain Missing**: `_process_output()` only checks agent field, ignores engine sources
3. **Inconsistent Usage**: Tests use `Plan[Task]` generics vs `TaskPlan` concrete classes
4. **Multi-source Confusion**: Agent → Engine → AugLLMConfig → Engines dict hierarchy unclear

### Critical Fix Points

1. **Agent.setup_agent()** - Add multi-source field syncing with priority chain
2. **ExecutionMixin.\_process_output()** - Add fallback lookup chain
3. **Test Patterns** - Standardize AugLLMConfig usage to concrete classes
4. **Validation** - Add AugLLMConfig validation for generic vs concrete classes

### Implementation Strategy

**Phase 1**: Fix multi-layer field syncing in `setup_agent()`  
**Phase 2**: Add fallback chain in `_process_output()`  
**Phase 3**: Standardize AugLLMConfig usage patterns  
**Phase 4**: Add AugLLMConfig-specific validation

### Risk Assessment

- Low risk: AugLLMConfig validation, field syncing in setup_agent()
- Medium risk: Fallback logic in \_process_output() (affects all agents)

### Success Criteria

- Tests pass with Plan objects (not dicts)
- `agent.structured_output_model` equals `aug_llm_config.structured_output_model`
- Fallback chain works at all levels
- Consistent AugLLMConfig patterns across codebase

## Tags

`#structured-output` `#field-syncing` `#aug-llm-config` `#agent-architecture` `#pydantic-models`
