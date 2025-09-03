# Import Error Breakdown by Module - August 5, 2025

## Summary
Total import errors: 1,555 (293 critical)

## Package Breakdown

### 🔴 haive-agents (1,108 import errors)
**Priority: HIGH - Most errors concentrated here**

#### 1. Simple Models Issue (235+ files affected)
- Missing: `haive.agents.simple.models` module
- Impact: Cascading failures across base, enhanced_agent, pre_post_agent_mixin
- Root cause: Module doesn't exist or wrong import path

#### 2. Planning Module (~30 errors)
- `plan_and_execute`: Wrong import paths (haive.agents.plan_and_execute)
- `rewoo`: Relative import issues (from models.join_step)
- `llm_compiler`: Missing haive.core.tools.dev_tools

#### 3. RAG Module (~15 errors)
- `corrective`: Relative imports (from corrective.agent)
- `collective`: Import path issues

#### 4. Other Issues (~20 errors)
- `routing_agent`: SimpleAgentSchema missing
- `supervisor`: build_graph missing from simple_supervisor
- `validation`: END missing from langgraph.types

### 🟡 haive-games (101 import errors)
**Priority: MEDIUM**

#### 1. Monopoly (~5 errors)
- Missing: MonopolyGame from haive.games.monopoly.game
- Missing: GameAgent from haive.games.framework

#### 2. Mafia (~10 errors)
- Missing: MafiaConfig from haive.games.mafia.config
- Missing: MafiaAnalysis from haive.games.mafia.models

#### 3. Clue (~5 errors)
- Wrong import: AugLLMEngine (should be AugLLMConfig)

### 🟡 haive-core (122 import errors)
**Priority: MEDIUM**

#### 1. Persistence (~30 errors)
- SupabaseCheckpointerConfig circular import
- PostgreSQL connection issues

#### 2. Document Loaders (~20 errors)
- ODPSource missing from files_office
- LoaderPreference from enhanced_registry
- Document from wrong langchain module

#### 3. Graph/Schema (~15 errors)
- register_node missing from node.registry
- Dict import from wrong module

### 🟢 haive-tools (69 import errors)
**Priority: LOW**
- Mostly ImportError (62) vs ModuleNotFoundError
- amadeus_toolkit function exports

### 🟢 haive-dataflow (55 import errors)
**Priority: LOW**
- SupabaseServerConfig imports
- AgentRegistry from wrong location
- GameInfo from haive.games.api

### 🟢 haive-mcp (48 import errors)  
**Priority: LOW**
- Mostly langchain deprecation warnings
- Need to update to langchain_community imports

### 🟢 haive-prebuilt (52 import errors)
**Priority: LOW**
- Essay grading NoneType errors
- Missing structured_output attributes

## Recommended Fix Order

1. **haive-agents simple.models** - Will fix 235+ errors
2. **haive-agents planning modules** - Quick path fixes
3. **haive-games** - Simple import corrections
4. **haive-core persistence** - May need architecture review
5. **Other packages** - Lower impact, can be done incrementally