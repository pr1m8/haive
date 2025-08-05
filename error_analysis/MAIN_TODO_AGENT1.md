# Haive Error Fix TODO List - AGENT 1

## Packages: haive-agents, haive-games, haive-tools

Generated: 2025-08-04 20:09:16
Split for: Agent 1

## Progress Summary

- **Total Errors**: 31275 (Agent 1's packages)
- **Fixed**: 0 ✅
- **In Progress**: 0 🔄
- **Won't Fix**: 0 ❌
- **Remaining**: 31275 ⏳
- **Progress**: 0/31275 (0.0%)

Progress: [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 0.0%

## 📦 Package Assignment for Agent 1

### haive-agents (24250 errors)

- ruff:Q000: 5173
- mypy:error: 3127
- mypy:import-untyped: 2945
- ruff:G004: 1853
- mypy:no-untyped-def: 1764

### haive-games (6321 errors)

- mypy:error: 1518
- ruff:E501: 1249
- mypy:import-untyped: 1041
- mypy:no-untyped-def: 725
- ruff:I001: 175

### haive-tools (704 errors)

- mypy:error: 167
- mypy:import-untyped: 83
- mypy:no-untyped-def: 68
- ImportError: 64
- ruff:N802: 36

## 🔴 Critical Errors (Fix First) - AGENT 1's Packages

These errors block multiple modules and should be fixed first:

### haive-agents Critical Errors

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

6. ⏳ **[a607ddc3]** `ModuleNotFoundError` in `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent/__init__.py`
   - Line: 3
   - Message: No module named 'react_agent'...
   - Impact: Blocks 65 modules
   - Package: haive-agents

7. ⏳ **[16a43fd8]** `ImportError` in `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/__init__.py`
   - Line: 3
   - Message: cannot import name 'add_tool' from 'haive.agents.react_class.react_agent2.advanced_agent3' (/home/wi...
   - Impact: Blocks 62 modules
   - Package: haive-agents

8. ⏳ **[04fcccf3]** `ModuleNotFoundError` in `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic_multi_agent.py`

- Line: 16
- Message: No module named 'haive.agents.multi.base_multi_agent'...
- Impact: Blocks 55 modules
- Package: haive-agents

11. ⏳ **[4732a339]** `ModuleNotFoundError` in `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/__init__.py`

- Line: 3
- Message: No module named 'haive.core.schema.prebuilt.rag_state'...
- Impact: Blocks 54 modules
- Package: haive-agents

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

### haive-tools Critical Errors

6. ⏳ **[5ca9b746]** `ImportError` in `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/__init__.py`
   - Line: 3
   - Message: cannot import name 'get_client' from 'haive.tools.tools.toolkits.alpha_vantage' (/home/will/Projects...
   - Impact: Blocks 94 modules
   - Package: haive-tools

### haive-games Critical Errors

7. ⏳ **[7c6e3ce7]** `ImportError` in `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/__init__.py`
   - Line: 3
   - Message: cannot import name 'MonopolyPlayerAgent' from partially initialized module 'haive.games.monopoly.pla...
   - Impact: Blocks 88 modules
   - Package: haive-games

## 🟡 High Priority Errors - AGENT 1's Packages

Common error patterns affecting Agent 1's packages:

### haive-agents Package Errors

#### ruff:Q000 (5173 occurrences in haive-agents)

1.  ⏳ [0648fd8f] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:32`
2.  ⏳ [7d895488] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:89`
3.  ⏳ [80882800] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:90`
    ... and 5170 more

#### mypy:error (3127 occurrences in haive-agents)

Focus on haive-agents related errors from the main list

#### mypy:import-untyped (2945 occurrences in haive-agents)

Focus on haive-agents related errors from the main list

#### ruff:G004 (1853 occurrences in haive-agents)

1.  ⏳ [46504325] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:363`
2.  ⏳ [402d83a4] `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:401`
    ... and 1851 more

### haive-games Package Errors

#### mypy:error (1518 occurrences in haive-games)

Focus on haive-games related errors from the main list

#### ruff:E501 (1249 occurrences in haive-games)

1.  ⏳ [1aa54446] `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/config.py:207`
2.  ⏳ [88557700] `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/configurable_config.py:212`
3.  ⏳ [5c2c6972] `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/demo.py:95`
    ... and 1246 more

### haive-tools Package Errors

#### mypy:error (167 occurrences in haive-tools)

Focus on haive-tools related errors from the main list

#### ImportError (64 occurrences in haive-tools)

Focus on fixing the critical import errors first as they block many modules

## 📝 Key Focus Areas for Agent 1

1. **Fix Missing Modules First**:
   - `haive.agents.multi.base_multi_agent` (blocks 307+ modules)
   - `haive.core.schema.prebuilt.rag_state` (blocks 54 modules)
   - NodeType.MESSAGE_TRANSFORMER attribute

2. **Common Patterns to Fix**:
   - Python 3.8 style type hints (`|` operator issues)
   - Missing imports and circular dependencies
   - Undefined names and functions

3. **Package Priorities**:
   - haive-agents: Most errors, fix critical imports first
   - haive-games: Focus on monopoly module circular import
   - haive-tools: Fix toolkit imports

## How to Use This Index

1. Start with Critical Errors (🔴) in your assigned packages
2. Fix missing modules that block the most other modules
3. Use error IDs to look up full details: `python error_search_tool.py id <error_id>`
4. Mark errors as fixed: `python mark_error_fixed.py <error_id>`
5. Add notes: `python add_error_note.py <error_id> "Your note here"`

## Status Legend

- ⏳ = Not started
- 🔄 = In progress
- ✅ = Fixed
- ❌ = Won't fix
