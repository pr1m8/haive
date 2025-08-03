# Temporarily Bypassed Modules for Documentation

**Date**: August 1, 2025  
**Priority**: HIGH - These need to be fixed and re-enabled  
**Status**: Modules excluded from documentation generation

## Overview

The following modules have been temporarily added to `autoapi_ignore` in `/docs/source/conf.py` to allow documentation to build. Each module has specific issues that need to be resolved before they can be included in the documentation.

## Recently Fixed (2025-08-01)

The following issues have been fixed and modules can be re-enabled:

1. **Pydantic Validators** - FIXED:
   - `haive/agents/common/models/task_analysis/__init__.py` - Removed incorrect import of `validate_decomposition_consistency` method
   - `haive/agents/rag/db_rag/graph_db/models.py` - Fixed field name in `@field_validator` from "cypher_query" to "query"

2. **Import Issues** - FIXED:
   - `haive/agents/agent.py` - Commented out missing `web_nav` module import
   - `haive/agents/rag/db_rag/graph_db/agent.py` - Updated deprecated LangChain import to `langchain_community`

3. **More Relative Import Fixes** - FIXED (2025-08-02):
   - `haive/agents/memory/search/__init__.py` - Fixed relative import from `search.base` to `.base`
   - `haive/agents/document_modifiers/summarizer/iterative_refinement/__init__.py` - Fixed relative imports

4. **Planning Module Import Fixes** - PARTIALLY FIXED (2025-08-02):
   - `haive/agents/planning/plan_and_execute/__init__.py` - Fixed relative imports to use dot notation
   - `haive/agents/planning/llm_compiler/__init__.py` - Fixed relative imports to use dot notation
   - `haive/agents/planning/llm_compiler/agent.py` - Fixed imports to use relative paths
   - `haive/agents/planning/llm_compiler/config.py` - Fixed imports and config class
   - `haive/agents/planning/llm_compiler/state.py` - Fixed relative imports
   - `haive/agents/planning/llm_compiler/utils.py` - Fixed relative imports
   - `haive/agents/planning/llm_compiler/tools/math_tools.py` - Fixed relative imports
   - `haive/agents/planning/plan_and_execute/agent.py` - Updated ReactAgent import to use v4
   - `haive/agents/planning/plan_and_execute/config.py` - Fixed ReactAgentConfig import and undefined variables

5. **Type Hint References Expansion** - FIXED (2025-08-02):
   - Expanded `nitpick_ignore` list from 45 to 113+ entries
   - Added comprehensive LangChain Core type references (25 entries)
   - Added LangGraph type references (8 entries)
   - Added enhanced Pydantic type references (10 entries)
   - Added advanced typing module references (12 entries)
   - Added common external library references (10 entries)
   - This should significantly reduce "reference target not found" warnings

6. **Quick Import Fixes** - FIXED (2025-08-02):
   - `haive/agents/memory/search/base.py` - Added missing `extract_memory_items` function
   - `haive/agents/document_modifiers/summarizer/iterative_refinement/__init__.py` - Removed incorrect `setup_workflow` export (it's a class method)
   - `haive/agents/chain_agent.py` - Fixed `SimpleAgentStateSchema` → `SimpleAgentState` import

7. **Still Need Fixing**:
   - Missing modules that don't exist (compiled_state_graph, agent_types, etc.)
   - Google-search-results dependency
   - Pydantic v2 validator errors in memory_v2 modules
   - Various other structural import issues

## Categories of Issues

### 1. Missing External Dependencies

**Modules affected:**

- `haive/tools/google/google_finance.py`
- `haive/tools/google/google_jobs.py`
- `haive/tools/google/google_scholar.py`
- `haive/tools/google/google_trends.py`

**Issue**: Missing `google-search-results` package
**Fix needed**: Either install the package or properly mock it

### 2. Relative Import Issues ("No module named 'agents'")

**Modules affected:**

- `haive/agents/agent.py`
- `haive/agents/factory.py`
- `haive/agents/chain_agent.py`
- `haive/agents/long_term_memory/**/*.py`

**Issue**: Incorrect relative imports
**Fix needed**: Update imports to use absolute paths (`from haive.agents...`)

### 3. Missing Core Dependencies

**Modules affected:**

- `haive/agents/base/compiled_agent.py` - Missing `haive.core.graph.state_graph.compiled_state_graph`
- `haive/agents/base/universal_agent.py` - Missing `haive.core.engine.base.agent_types`
- `haive/agents/archive/meta/**/*.py` - Cannot import `build_graph`

**Issue**: References to non-existent or moved modules
**Fix needed**: Update imports to correct module paths or implement missing modules

### 4. Pydantic Validation Errors

**Modules affected:**

- `haive/agents/common/models/task_analysis/**/*.py` - `validate_decomposition_consistency` signature issue
- `haive/agents/rag/db_rag/graph_db/**/*.py` - `CypherQueryOutput` validation decorator issue
- `haive/agents/memory_v2/**/*.py` - Same CypherQueryOutput issues

**Issue**: Pydantic v2 incompatible validator signatures
**Fix needed**: Update validators to use Pydantic v2 syntax:

```python
# Old (Pydantic v1)
@validator('field_name')
def validate_field(cls, v):
    return v

# New (Pydantic v2)
@field_validator('field_name')
@classmethod
def validate_field(cls, v):
    return v
```

### 5. Missing Function/Class Imports

**Modules affected:**

- `haive/agents/chain/**/*.py` - Cannot import `complex_rag`
- `haive/agents/conversation/base/example*.py` - Missing conversation functions
- `haive/agents/document_modifiers/kg/**/*.py` - Cannot import `normalize_contents`
- `haive/agents/research/storm/outline_generator/models.py` - Cannot import `as_str`

**Issue**: References to non-existent functions or classes
**Fix needed**: Implement missing functions or update imports

### 6. Module Structure Issues

**Modules affected:**

- `haive/agents/document_loader/examples/**/*.py` - Missing `examples.usage_examples`
- `haive/agents/document_modifiers/summarizer/iterative_refinement/**/*.py` - Module not found
- `haive/agents/experiments/**/*.py` - `langgraph_supervisor` not found
- `haive/agents/memory/models_dir/**/*.py` - Package structure issues
- `haive/agents/memory/search/**/*.py` - Search module not found

**Issue**: Incorrect module structure or missing **init**.py files
**Fix needed**: Verify module structure and add missing **init**.py files

### 7. Circular Import Issues

**Modules affected:**

- `haive/agents/multi/archive/**/*.py`

**Issue**: Circular dependencies between modules
**Fix needed**: Refactor to break circular dependencies

### 8. Schema Generation Errors

**Modules affected:**

- `haive/agents/multi/enhanced_clean_multi_agent.py`

**Issue**: Unable to generate Pydantic schema for certain types
**Fix needed**: Add `arbitrary_types_allowed=True` or implement `__get_pydantic_core_schema__`

## Previously Fixed Issues

These issues were already addressed:

- sphinx_math_dollar crash - Extension disabled
- sphinx_codeautolink Pydantic schema error - Discovery modules excluded
- Type hint references - autodoc_typehints set to "description"
- Non-existent search tool classes - Updated RST to reference actual tools

## Re-enabling Process

To re-enable these modules:

1. Fix the underlying issue in the source code
2. Remove the module pattern from `autoapi_ignore` in `/docs/source/conf.py`
3. Remove any related entries from `autodoc_mock_imports`
4. Run `nox -s docs_phased` to test
5. Update this document when modules are fixed

## Testing Individual Modules

To test if a module is fixed:

```bash
# Test import directly
poetry run python -c "import haive.agents.module_name"

# Test with Sphinx
poetry run sphinx-build -b html -W docs/source docs/test_build
```

## Priority Order for Fixes

1. **HIGH**: Pydantic validation errors (affects core functionality)
2. **HIGH**: Missing core dependencies (breaks imports)
3. **MEDIUM**: Relative import issues (easy to fix)
4. **MEDIUM**: Missing functions/classes (may need implementation)
5. **LOW**: External dependencies (can remain mocked)
6. **LOW**: RST formatting issues (cosmetic)

## Notes

- Total modules bypassed: ~50+
- Impact: Significant portions of agent documentation missing
- Estimated fix time: 2-3 days for all issues
- Most critical: Pydantic validators and core imports

Remember to remove modules from this bypass list as they are fixed!
