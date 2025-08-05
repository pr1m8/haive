# Haive Error Fix TODO List - AGENT 2

## Packages: haive-core, haive-dataflow, haive-mcp, haive-prebuilt

Generated: 2025-08-04 20:09:16
Split for: Agent 2

## Progress Summary

- **Total Errors**: 20163 (Agent 2's packages)
- **Fixed**: 240 ✅ (50 TypeConverter + 19 NodeType + 54 RAGState + 48 GitHubLoader + 34 doc_loader + 42 prebuilt imports + 5 dataflow API imports + 2 prebuilt modules)
- **In Progress**: 0 🔄
- **Won't Fix**: 0 ❌
- **Remaining**: 19923 ⏳
- **Progress**: 240/20163 (1.19%)

Progress: [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 0.0%

## 📦 Package Assignment for Agent 2

### haive-core (13161 errors)

- mypy:error: 2628
- ruff:Q000: 2518
- mypy:import-untyped: 1367
- mypy:no-untyped-def: 1259
- mypy:no-any-return: 219

### haive-dataflow (4452 errors)

- ruff:G004: 1219
- mypy:error: 612
- mypy:no-untyped-def: 405
- ruff:TRY401: 391
- ruff:DTZ005: 248

### haive-mcp (1625 errors)

- mypy:error: 361
- ruff:G004: 216
- mypy:no-untyped-def: 171
- mypy:import-untyped: 121
- ruff:Q000: 91

### haive-prebuilt (925 errors)

- mypy:error: 250
- mypy:import-untyped: 163
- mypy:no-untyped-def: 120
- ModuleNotFoundError: 42
- ruff:I001: 41

## 🔴 Critical Errors (Fix First) - AGENT 2's Packages

These errors block multiple modules and should be fixed first:

### haive-core Critical Errors

12. ✅ **[7ffb923a]** `ImportError` in `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/__init__.py`

- Line: 11
- Message: cannot import name 'TypeConverter' from 'haive.core.schema.compatibility.converters' (/home/will/Pro...
- Impact: Blocks 50 modules
- Package: haive-core
- **FIXED**: Created converters.py and added SchemaCompatibility class

### haive-mcp Critical Errors

13. ✅ **[cd460ed2]** `ImportError` in `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/documentation/__init__.py`

- Line: 3
- Message: cannot import name 'GitHubLoader' from 'haive.agents.research.open_perplexity.structured_tools' (/ho...
- Impact: Blocks 48 modules
- Package: haive-mcp
- **FIXED**: Added GitHubLoader and WebScraper classes to structured_tools.py + fixed **init**.py imports

20. ✅ **[75ca534c]** `ImportError` in `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/documentation/doc_loader.py`

- Line: 51
- Message: cannot import name 'GitHubLoader' from 'haive.agents.research.open_perplexity.structured_tools' (/ho...
- Impact: Blocks 34 modules
- Package: haive-mcp
- **FIXED**: Added GitHubLoader and WebScraper classes to structured_tools.py

### Cross-Package Dependencies (Affecting Agent 2)

Note: These errors reference missing modules that may need coordination with Agent 1:

- ✅ `haive.core.schema.prebuilt.rag_state` - **FIXED**: Created RAGState schema extending MessagesState with RAG-specific fields
- ✅ NodeType enum missing attributes - **FIXED**: Added MESSAGE_TRANSFORMER, COORDINATOR, TRANSFORM, OUTPUT_PARSER

## 🟡 High Priority Errors - AGENT 2's Packages

Common error patterns affecting Agent 2's packages:

### haive-core Package Errors

#### mypy:error (2628 occurrences in haive-core)

1.  ⏳ [120f0503] `packages/haive-core/src/haive/core/errors.py:0`
2.  ⏳ [0f8daecb] `packages/haive-core/src/haive/core/utils/visualize_graph_utils.py:0`
3.  ⏳ [330e7a56] `packages/haive-core/src/haive/core/utils/state_utils.py:0`
4.  ⏳ [d5eb97e8] `packages/haive-core/src/haive/core/utils/getter_mixin.py:0`
    ... and 2624 more

#### ruff:Q000 (2518 occurrences in haive-core)

Focus on haive-core specific files

#### mypy:import-untyped (1367 occurrences in haive-core)

1.  ⏳ [cae60fe7] `packages/haive-core/src/haive/core/utils/visualize_graph_utils.py:3`
2.  ⏳ [3dd2f80f] `packages/haive-core/src/haive/core/utils/pydantic_utils/__init__.py:3`
3.  ⏳ [c304fb99] `packages/haive-core/src/haive/core/utils/haive_discovery/__init__.py:7`
    ... and 1364 more

### haive-dataflow Package Errors

#### ruff:G004 (1219 occurrences in haive-dataflow)

Focus on haive-dataflow logging patterns

#### mypy:error (612 occurrences in haive-dataflow)

Focus on haive-dataflow type errors

#### ruff:TRY401 (391 occurrences in haive-dataflow)

Exception handling patterns need fixing

#### ruff:DTZ005 (248 occurrences in haive-dataflow)

Datetime timezone issues

### haive-mcp Package Errors

#### mypy:error (361 occurrences in haive-mcp)

Focus on haive-mcp type errors

#### ruff:G004 (216 occurrences in haive-mcp)

Logging format issues

### haive-dataflow Package Errors

#### ✅ Major Import Path Fixes Applied (5 errors fixed)

- Fixed app.py: haive.dataflow.api.api._ → haive.dataflow.api._ imports
- Fixed game_api.py: haive.dataflow.api.api.game_socket → haive.dataflow.api.game_socket
- Fixed registry.py: haive.api.api.db → haive.dataflow.api.db imports
- Fixed supabase_adapter.py: haive.dataflow.persistence.persistence.factory → haive.core.persistence.factory
- Fixed model_registry.py: haive.dataflow.registries.db.supabase → haive.dataflow.db.supabase

### haive-prebuilt Package Errors

#### ✅ Major Import Fixes Applied (42 errors fixed)

- Fixed haive_agents → haive.agents imports (15 files)
- Fixed haive.core.aug_llm → haive.core.engine.aug_llm imports
- Fixed Agent import from langchain_core.agents → haive.agents.base.agent
- Fixed contract_analysis imports to use local models
- Fixed AugLLMConfig field names (promptTemplate → prompt_template, structured_output → structured_output_model)

#### ✅ Missing Module Creation (2 errors fixed)

- Created agent_utilities_models.py with comprehensive Pydantic models for business processes
- Created agent_utilities_prompts.py with expert system prompts and agent factory functions
- Fixed optional NewsAPI dependency in tldr2/tools.py with graceful fallback

#### mypy:error (208 remaining occurrences in haive-prebuilt)

Focus on remaining haive-prebuilt type errors

#### ModuleNotFoundError (remaining occurrences in haive-prebuilt)

Additional missing dependencies specific to prebuilt agents

## 📝 Key Focus Areas for Agent 2

1. **Fix Core Infrastructure First**:
   - TypeConverter import in schema/compatibility
   - Missing NodeType enum values (MESSAGE_TRANSFORMER, COORDINATOR, TRANSFORM)
   - Create `haive.core.schema.prebuilt.rag_state` module

2. **Common Patterns to Fix**:
   - Type annotations and mypy errors
   - Logging format strings (G004)
   - Exception handling patterns (TRY401)
   - Datetime timezone awareness (DTZ005)

3. **Package Priorities**:
   - haive-core: Foundation package, fix critical infrastructure
   - haive-dataflow: API and streaming functionality
   - haive-mcp: Model Context Protocol integration
   - haive-prebuilt: Pre-configured agents (depends on other fixes)

4. **Cross-Package Coordination**:
   - Coordinate with Agent 1 on shared dependencies
   - Fix NodeType enum in haive-core (affects Agent 1's packages)
   - Create missing schema modules referenced by other packages

## 🔧 Special Considerations for Agent 2

1. **NodeType Enum Fix** (High Priority):
   - Add MESSAGE_TRANSFORMER attribute
   - Add COORDINATOR attribute
   - Add TRANSFORM attribute
   - This will unblock 19 modules in Agent 1's packages

2. **Schema Modules**:
   - Create `haive.core.schema.prebuilt.rag_state`
   - Fix compatibility module imports

3. **Dataflow Package**:
   - Many logging and exception handling issues
   - Focus on consistent patterns across the package

## How to Use This Index

1. Start with Critical Errors (🔴) in your assigned packages
2. Fix core infrastructure that other packages depend on
3. Use error IDs to look up full details: `python error_search_tool.py id <error_id>`
4. Mark errors as fixed: `python mark_error_fixed.py <error_id>`
5. Add notes: `python add_error_note.py <error_id> "Your note here"`

## Status Legend

- ⏳ = Not started
- 🔄 = In progress
- ✅ = Fixed
- ❌ = Won't fix
