# Haive Error Fix TODO List

Generated: 2025-08-04 20:09:16

## Progress Summary

- **Total Errors**: 51438
- **Fixed**: 0 ✅
- **In Progress**: 0 🔄
- **Won't Fix**: 0 ❌
- **Remaining**: 51438 ⏳
- **Progress**: 0/51438 (0.0%)

Progress: [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 0.0%

## 🔴 Critical Errors (Fix First)

These errors block multiple modules and should be fixed first:

1. ⏳ **[3f0906f5]** `ImportError` in `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/__init__.py`
   - Line: 20
   - Message: cannot import name 'should_continue' from 'haive.agents.planning.plan_and_execute_multi' (/home/will...
   - Impact: Blocks 176 modules
   - Package: haive-agents

2. ⏳ **[8e986bf2]** `ModuleNotFoundError` in `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/__init__.py`
   - Line: 46
   - Message: No module named 'haive.agents.multi.base_multi_agent'...
   - Impact: Blocks 153 modules
   - Package: haive-agents

3. ⏳ **[15f3c5d0]** `ModuleNotFoundError` in `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic/__init__.py`
   - Line: 0
   - Message: No module named 'haive.agents.multi.base_multi_agent'...
   - Impact: Blocks 99 modules
   - Package: haive-agents

4. ⏳ **[2ec57118]** `ImportError` in `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/__init__.py`
   - Line: 0
   - Message: cannot import name 'should_continue' from 'haive.agents.planning.plan_and_execute_multi' (/home/will...
   - Impact: Blocks 98 modules
   - Package: haive-agents

5. ⏳ **[7de92e7e]** `TypeError` in `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/__init__.py`
   - Line: 37
   - Message: unsupported operand type(s) for |: 'type' and 'str'...
   - Impact: Blocks 96 modules
   - Package: haive-agents

6. ⏳ **[5ca9b746]** `ImportError` in `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/__init__.py`
   - Line: 3
   - Message: cannot import name 'get_client' from 'haive.tools.tools.toolkits.alpha_vantage' (/home/will/Projects...
   - Impact: Blocks 94 modules
   - Package: haive-tools

7. ⏳ **[7c6e3ce7]** `ImportError` in `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/__init__.py`
   - Line: 3
   - Message: cannot import name 'MonopolyPlayerAgent' from partially initialized module 'haive.games.monopoly.pla...
   - Impact: Blocks 88 modules
   - Package: haive-games

8. ⏳ **[a607ddc3]** `ModuleNotFoundError` in `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent/__init__.py`
   - Line: 3
   - Message: No module named 'react_agent'...
   - Impact: Blocks 65 modules
   - Package: haive-agents

9. ⏳ **[16a43fd8]** `ImportError` in `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/__init__.py`
   - Line: 3
   - Message: cannot import name 'add_tool' from 'haive.agents.react_class.react_agent2.advanced_agent3' (/home/wi...
   - Impact: Blocks 62 modules
   - Package: haive-agents

10. ⏳ **[04fcccf3]** `ModuleNotFoundError` in `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic_multi_agent.py`

- Line: 16
- Message: No module named 'haive.agents.multi.base_multi_agent'...
- Impact: Blocks 55 modules
- Package: haive-agents

11. ⏳ **[4732a339]** `ModuleNotFoundError` in `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/__init__.py`

- Line: 3
- Message: No module named 'haive.core.schema.prebuilt.rag_state'...
- Impact: Blocks 54 modules
- Package: haive-agents

12. ⏳ **[7ffb923a]** `ImportError` in `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/__init__.py`

- Line: 11
- Message: cannot import name 'TypeConverter' from 'haive.core.schema.compatibility.converters' (/home/will/Pro...
- Impact: Blocks 50 modules
- Package: haive-core

13. ⏳ **[cd460ed2]** `ImportError` in `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/documentation/__init__.py`

- Line: 3
- Message: cannot import name 'GitHubLoader' from 'haive.agents.research.open_perplexity.structured_tools' (/ho...
- Impact: Blocks 48 modules
- Package: haive-mcp

14. ⏳ **[56a67986]** `ImportError` in `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/__init__.py`

- Line: 3
- Message: cannot import name 'format_search_context' from 'haive.agents.memory.search.base' (/home/will/Project...
- Impact: Blocks 46 modules
- Package: haive-agents

15. ⏳ **[752226ae]** `TypeError` in `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/agent.py`

- Line: 30
- Message: unsupported operand type(s) for |: 'type' and 'str'...
- Impact: Blocks 42 modules
- Package: haive-agents

16. ⏳ **[79aa000b]** `ImportError` in `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/__init__.py`

- Line: 22
- Message: cannot import name 'StrategyDecision' from 'haive.agents.chain.examples' (/home/will/Projects/haive/...
- Impact: Blocks 40 modules
- Package: haive-agents

17. ⏳ **[e9453a77]** `ImportError` in `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/base.py`

- Line: 0
- Message: cannot import name 'format_search_context' from 'haive.agents.memory.search.base' (/home/will/Project...
- Impact: Blocks 38 modules
- Package: haive-agents

18. ⏳ **[7d3fa0fd]** `ImportError` in `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/__init__.py`

- Line: 7
- Message: cannot import name 'from_llms' from 'haive.agents.reasoning_and_critique.lats.config' (/home/will/Pr...
- Impact: Blocks 35 modules
- Package: haive-agents

19. ⏳ **[d69699b7]** `AttributeError` in `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/__init__.py`

- Line: 3
- Message: type object 'NodeType' has no attribute 'MESSAGE_TRANSFORMER'...
- Impact: Blocks 34 modules
- Package: haive-agents

20. ⏳ **[75ca534c]** `ImportError` in `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/documentation/doc_loader.py`

- Line: 51
- Message: cannot import name 'GitHubLoader' from 'haive.agents.research.open_perplexity.structured_tools' (/ho...
- Impact: Blocks 34 modules
- Package: haive-mcp

## 🟡 High Priority Errors

Common error patterns that affect many files:

### 1. mypy:error:unknown (8663 occurrences)

1.  ⏳ [120f0503] `packages/haive-core/src/haive/core/errors.py:0`
2.  ⏳ [0f8daecb] `packages/haive-core/src/haive/core/utils/visualize_graph_utils.py:0`
3.  ⏳ [330e7a56] `packages/haive-core/src/haive/core/utils/state_utils.py:0`
4.  ⏳ [d5eb97e8] `packages/haive-core/src/haive/core/utils/getter_mixin.py:0`
5.  ⏳ [d5eb97e8] `packages/haive-core/src/haive/core/utils/getter_mixin.py:0`
    ... and 8658 more

### 2. ruff:Q000:unknown (7782 occurrences)

1.  ⏳ [0648fd8f] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:32`
2.  ⏳ [7d895488] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:89`
3.  ⏳ [80882800] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:90`
4.  ⏳ [80882800] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:90`
5.  ⏳ [bc30b01f] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:91`
    ... and 7777 more

### 3. mypy:import-untyped:unknown (5942 occurrences)

1.  ⏳ [cae60fe7] `packages/haive-core/src/haive/core/utils/visualize_graph_utils.py:3`
2.  ⏳ [3dd2f80f] `packages/haive-core/src/haive/core/utils/pydantic_utils/__init__.py:3`
3.  ⏳ [c304fb99] `packages/haive-core/src/haive/core/utils/haive_discovery/__init__.py:7`
4.  ⏳ [52fd517c] `packages/haive-core/src/haive/core/utils/haive_discovery/__init__.py:8`
5.  ⏳ [07edc4d7] `packages/haive-core/src/haive/core/utils/haive_discovery/__init__.py:9`
    ... and 5937 more

### 4. mypy:no-untyped-def:unknown (4512 occurrences)

1.  ⏳ [24d10d4e] `packages/haive-core/src/haive/core/errors.py:4`
2.  ⏳ [87d1c98f] `packages/haive-core/src/haive/core/utils/visualize_graph_utils.py:9`
3.  ⏳ [b039aa35] `packages/haive-core/src/haive/core/utils/state_utils.py:1`
4.  ⏳ [6c4a0c0c] `packages/haive-core/src/haive/core/utils/getter_mixin.py:61`
5.  ⏳ [a7ad3b95] `packages/haive-core/src/haive/core/utils/getter_mixin.py:137`
    ... and 4507 more

### 5. ruff:G004:unknown (3299 occurrences)

1.  ⏳ [46504325] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:363`
2.  ⏳ [402d83a4] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:401`
3.  ⏳ [cf880e79] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:427`
4.  ⏳ [b5dc024b] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:438`
5.  ⏳ [6897c96c] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:535`
    ... and 3294 more

### 6. ruff:I001:unknown (1352 occurrences)

1.  ⏳ [10b8c358] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/__init__.py:52`
2.  ⏳ [dd55dceb] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/__init__.py:98`
3.  ⏳ [caeadfbd] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:1`
4.  ⏳ [23cbc692] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/archive/meta/__init__.py:3`
5.  ⏳ [8d2368ff] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/archive/meta/agent.py:3`
    ... and 1347 more

### 7. ruff:E501:unknown (1249 occurrences)

1.  ⏳ [1aa54446] `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/config.py:207`
2.  ⏳ [88557700] `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/configurable_config.py:212`
3.  ⏳ [5c2c6972] `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/demo.py:95`
4.  ⏳ [48e1c04a] `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/demo.py:346`
5.  ⏳ [bfaacbaf] `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/demo.py:499`
    ... and 1244 more

### 8. ruff:TRY401:unknown (908 occurrences)

1.  ⏳ [05cc01a2] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:363`
2.  ⏳ [77299915] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:438`
3.  ⏳ [9219124b] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:535`
4.  ⏳ [82cb114f] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:610`
5.  ⏳ [25f8de22] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:613`
    ... and 903 more

### 9. mypy:no-any-return:unknown (760 occurrences)

1.  ⏳ [78ee2d2b] `packages/haive-core/src/haive/core/utils/debugkit/debugging.py:79`
2.  ⏳ [022226b7] `packages/haive-core/src/haive/core/utils/debugkit/fallbacks.py:554`
3.  ⏳ [fb9fc628] `packages/haive-core/src/haive/core/registry/memory.py:42`
4.  ⏳ [3db025c6] `packages/haive-core/src/haive/core/models/metadata_mixin.py:33`
5.  ⏳ [3bb6ed2e] `packages/haive-core/src/haive/core/models/metadata_mixin.py:41`
    ... and 755 more

### 10. ruff:F821:unknown (722 occurrences)

1.  ⏳ [b378ced1] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:768`
2.  ⏳ [02712ce3] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/compiled_agent.py:61`
3.  ⏳ [5214ac04] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/compiled_agent.py:62`
4.  ⏳ [4d375f51] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/compiled_agent.py:64`
5.  ⏳ [3c3c93b2] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/compiled_agent.py:66`
    ... and 717 more

### 11. mypy:name-defined:unknown (707 occurrences)

1.  ⏳ [40ea8720] `packages/haive-core/src/haive/core/graph/state_graph/pattern_registry.py:6`
2.  ⏳ [3ba7eafc] `packages/haive-core/src/haive/core/graph/state_graph/pattern_registry.py:20`
3.  ⏳ [76b375ed] `packages/haive-core/src/haive/core/graph/state_graph/pattern_registry.py:21`
4.  ⏳ [e162d94c] `packages/haive-core/src/haive/core/graph/state_graph/pattern_registry.py:24`
5.  ⏳ [3fb18f2b] `packages/haive-core/src/haive/core/graph/state_graph/pattern_registry.py:36`
    ... and 702 more

### 12. ruff:PLR2004:unknown (697 occurrences)

1.  ⏳ [408530d5] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:559`
2.  ⏳ [38b31dd0] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:624`
3.  ⏳ [cec800fe] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:368`
4.  ⏳ [5500943a] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/debug_utils.py:90`
5.  ⏳ [b7e5eacd] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/debug_utils.py:101`
    ... and 692 more

### 13. ruff:DTZ005:unknown (619 occurrences)

1.  ⏳ [97d269f5] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:707`
2.  ⏳ [60c04a9f] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/state_mixin.py:61`
3.  ⏳ [848a799b] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain_agent.py:89`
4.  ⏳ [fad1cabf] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_processing/agent.py:393`
5.  ⏳ [de26673b] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_processing/agent.py:421`
    ... and 614 more

### 14. mypy:str, Any:unknown (583 occurrences)

1.  ⏳ [4d450693] `packages/haive-core/src/haive/core/graph/node/composer/update_functions.py:102`
2.  ⏳ [32e673bd] `packages/haive-core/src/haive/core/engine/document/loaders/sources/local/pdf.py:94`
3.  ⏳ [898c5aae] `packages/haive-core/src/haive/core/engine/document/loaders/sources/local/pdf.py:156`
4.  ⏳ [0d6d0aac] `packages/haive-core/src/haive/core/schema/compatibility/field_mapping.py:144`
5.  ⏳ [2645e63f] `packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:231`
    ... and 578 more

### 15. ruff:W293:unknown (582 occurrences)

1.  ⏳ [54b1bcff] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent_structured_output_mixin.py:253`
2.  ⏳ [8b9b0e57] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/execution_mixin.py:371`
3.  ⏳ [b2d7f896] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:31`
4.  ⏳ [87df53ce] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:36`
5.  ⏳ [75e00fca] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:42`
    ... and 577 more

## 📦 Errors by Package

### haive-agents (24250 errors)

- ruff:Q000: 5173
- mypy:error: 3127
- mypy:import-untyped: 2945
- ruff:G004: 1853
- mypy:no-untyped-def: 1764

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

### haive-games (6321 errors)

- mypy:error: 1518
- ruff:E501: 1249
- mypy:import-untyped: 1041
- mypy:no-untyped-def: 725
- ruff:I001: 175

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

### haive-tools (704 errors)

- mypy:error: 167
- mypy:import-untyped: 83
- mypy:no-untyped-def: 68
- ImportError: 64
- ruff:N802: 36

## How to Use This Index

1. Start with Critical Errors (🔴) - these block the most modules
2. Fix High Priority patterns (🟡) - these affect many files
3. Use error IDs to look up full details: `python error_search_tool.py id <error_id>`
4. Mark errors as fixed: `python mark_error_fixed.py <error_id>`
5. Add notes: `python add_error_note.py <error_id> "Your note here"`

## Status Legend

- ⏳ = Not started
- 🔄 = In progress
- ✅ = Fixed
- ❌ = Won't fix
