# Import Error Dependency Analysis

Total Errors: 1069

## Error Summary by Type

- **AttributeError**: 19 errors
- **ImportError**: 390 errors
- **KeyError**: 3 errors
- **ModuleNotFoundError**: 537 errors
- **NameError**: 37 errors
- **PydanticSchemaGenerationError**: 2 errors
- **PydanticUndefinedAnnotation**: 1 errors
- **PydanticUserError**: 3 errors
- **TypeError**: 73 errors
- **ValidationError**: 4 errors

## Error Summary by Package

- **haive-agents**: 580 errors
- **haive-core**: 134 errors
- **haive-dataflow**: 61 errors
- **haive-games**: 120 errors
- **haive-mcp**: 47 errors
- **haive-prebuilt**: 56 errors
- **haive-tools**: 71 errors

## Error Dependency Chains

These are groups of modules that fail due to the same root cause:


### Chain 1: haive.agents.planning.plan_and_execute_multi import (
- **Affected Modules**: 72
- **Packages**: haive-agents
- **Modules**:
  - `haive.agents.planning` (haive-agents)
  - `haive.agents.planning.base` (haive-agents)
  - `haive.agents.planning.base.agents` (haive-agents)
  - `haive.agents.planning.base.agents.executor` (haive-agents)
  - `haive.agents.planning.base.agents.planner` (haive-agents)
  - `haive.agents.planning.base.models` (haive-agents)
  - `haive.agents.planning.base.prompts` (haive-agents)
  - `haive.agents.planning.enhanced_plan_execute_v5` (haive-agents)
  - `haive.agents.planning.enhanced_plan_execute_v5.planner` (haive-agents)
  - `haive.agents.planning.enhanced_plan_execute_v5.planner.models` (haive-agents)
  - ... and 62 more

### Chain 2: haive.tools.tools.toolkits.alpha_vantage import (
- **Affected Modules**: 64
- **Packages**: haive-tools
- **Modules**:
  - `haive.tools.tools.toolkits` (haive-tools)
  - `haive.tools.tools.toolkits.amadues_toolkit` (haive-tools)
  - `haive.tools.tools.toolkits.azure_ai_services_toolkit` (haive-tools)
  - `haive.tools.tools.toolkits.base` (haive-tools)
  - `haive.tools.tools.toolkits.chuck_norris_jokes_toolkit` (haive-tools)
  - `haive.tools.tools.toolkits.citydsk_toolkit` (haive-tools)
  - `haive.tools.tools.toolkits.clickup_toolkit` (haive-tools)
  - `haive.tools.tools.toolkits.dataforseo_toolkit` (haive-tools)
  - `haive.tools.tools.toolkits.dev` (haive-tools)
  - `haive.tools.tools.toolkits.dev.project_creation` (haive-tools)
  - ... and 54 more

### Chain 3: haive.core.engine.loaders
- **Affected Modules**: 53
- **Packages**: haive-core
- **Modules**:
  - `haive.core.engine.document.loaders.adapters` (haive-core)
  - `haive.core.engine.document.loaders.adapters.base` (haive-core)
  - `haive.core.engine.document.loaders.adapters.local` (haive-core)
  - `haive.core.engine.document.loaders.sources.base.base` (haive-core)
  - `haive.core.engine.document.loaders.sources.factory` (haive-core)
  - `haive.core.engine.document.loaders.sources.groups` (haive-core)
  - `haive.core.engine.document.loaders.sources.local.base` (haive-core)
  - `haive.core.engine.document.loaders.sources.local.bibtex_source` (haive-core)
  - `haive.core.engine.document.loaders.sources.local.chm_source` (haive-core)
  - `haive.core.engine.document.loaders.sources.local.csv_source` (haive-core)
  - ... and 43 more

### Chain 4: haive.agents.multi.base_multi_agent
- **Affected Modules**: 49
- **Packages**: haive-agents
- **Modules**:
  - `haive.agents.supervisor` (haive-agents)
  - `haive.agents.supervisor.archive.agent_v2` (haive-agents)
  - `haive.agents.supervisor.archive.choice_model_supervisor` (haive-agents)
  - `haive.agents.supervisor.archive.dynamic_activation_supervisor` (haive-agents)
  - `haive.agents.supervisor.archive.dynamic_agent_discovery_supervisor` (haive-agents)
  - `haive.agents.supervisor.archive.dynamic_executor_node` (haive-agents)
  - `haive.agents.supervisor.archive.dynamic_supervisor` (haive-agents)
  - `haive.agents.supervisor.archive.dynamic_supervisor_fixed` (haive-agents)
  - `haive.agents.supervisor.archive.dynamic_tool_discovery_supervisor` (haive-agents)
  - `haive.agents.supervisor.archive.example_delegation` (haive-agents)
  - ... and 39 more

### Chain 5: task_analysis
- **Affected Modules**: 30
- **Packages**: haive-agents
- **Modules**:
  - `haive.agents.task_analysis` (haive-agents)
  - `haive.agents.task_analysis.agent` (haive-agents)
  - `haive.agents.task_analysis.analysis` (haive-agents)
  - `haive.agents.task_analysis.analysis.engines` (haive-agents)
  - `haive.agents.task_analysis.analysis.models` (haive-agents)
  - `haive.agents.task_analysis.analysis.prompts` (haive-agents)
  - `haive.agents.task_analysis.base` (haive-agents)
  - `haive.agents.task_analysis.base.models` (haive-agents)
  - `haive.agents.task_analysis.complexity` (haive-agents)
  - `haive.agents.task_analysis.complexity.engines` (haive-agents)
  - ... and 20 more

### Chain 6: haive.agents.react_class.react_agent2.advanced_agent3 import (
- **Affected Modules**: 20
- **Packages**: haive-agents
- **Modules**:
  - `haive.agents.react_class.react_agent2` (haive-agents)
  - `haive.agents.react_class.react_agent2.agent` (haive-agents)
  - `haive.agents.react_class.react_agent2.agent2` (haive-agents)
  - `haive.agents.react_class.react_agent2.agent3` (haive-agents)
  - `haive.agents.react_class.react_agent2.aug_llms` (haive-agents)
  - `haive.agents.react_class.react_agent2.config` (haive-agents)
  - `haive.agents.react_class.react_agent2.debug` (haive-agents)
  - `haive.agents.react_class.react_agent2.dynamic_agent` (haive-agents)
  - `haive.agents.react_class.react_agent2.example` (haive-agents)
  - `haive.agents.react_class.react_agent2.example2` (haive-agents)
  - ... and 10 more

### Chain 7: haive.games.monopoly.agent import MonopolyAgent, MonopolyAgentConfig
- **Affected Modules**: 20
- **Packages**: haive-games
- **Modules**:
  - `haive.games.monopoly` (haive-games)
  - `haive.games.monopoly.agent` (haive-games)
  - `haive.games.monopoly.config` (haive-games)
  - `haive.games.monopoly.configurable_config` (haive-games)
  - `haive.games.monopoly.example` (haive-games)
  - `haive.games.monopoly.game` (haive-games)
  - `haive.games.monopoly.game.card` (haive-games)
  - `haive.games.monopoly.game.game` (haive-games)
  - `haive.games.monopoly.game.player` (haive-games)
  - `haive.games.monopoly.game.property` (haive-games)
  - ... and 10 more

### Chain 8: haive.core.schema.prebuilt.rag_state
- **Affected Modules**: 17
- **Packages**: haive-agents
- **Modules**:
  - `haive.agents.rag.multi_agent_rag` (haive-agents)
  - `haive.agents.rag.multi_agent_rag.additional_workflows` (haive-agents)
  - `haive.agents.rag.multi_agent_rag.advanced_workflows` (haive-agents)
  - `haive.agents.rag.multi_agent_rag.agents` (haive-agents)
  - `haive.agents.rag.multi_agent_rag.compatibility` (haive-agents)
  - `haive.agents.rag.multi_agent_rag.complete_rag_workflows` (haive-agents)
  - `haive.agents.rag.multi_agent_rag.enhanced_multi_rag` (haive-agents)
  - `haive.agents.rag.multi_agent_rag.enhanced_state_schemas` (haive-agents)
  - `haive.agents.rag.multi_agent_rag.enhanced_workflows` (haive-agents)
  - `haive.agents.rag.multi_agent_rag.graded_rag_workflows` (haive-agents)
  - ... and 7 more

### Chain 9: AttributeError:MESSAGE_TRANSFORMER
- **Affected Modules**: 16
- **Packages**: haive-agents, haive-core
- **Modules**:
  - `haive.agents.reasoning_and_critique.reflection` (haive-agents)
  - `haive.agents.reasoning_and_critique.reflection.agent` (haive-agents)
  - `haive.agents.reasoning_and_critique.reflection.config` (haive-agents)
  - `haive.agents.reasoning_and_critique.reflection.models` (haive-agents)
  - `haive.agents.reasoning_and_critique.reflection.state` (haive-agents)
  - `haive.agents.reflection` (haive-agents)
  - `haive.agents.reflection.agent` (haive-agents)
  - `haive.agents.reflection.message_transformer` (haive-agents)
  - `haive.agents.reflection.message_transformer_posthook` (haive-agents)
  - `haive.agents.reflection.models` (haive-agents)
  - ... and 6 more

### Chain 10: wiki_writer
- **Affected Modules**: 16
- **Packages**: haive-agents
- **Modules**:
  - `haive.agents.wiki_writer` (haive-agents)
  - `haive.agents.wiki_writer.agent` (haive-agents)
  - `haive.agents.wiki_writer.aug_llms` (haive-agents)
  - `haive.agents.wiki_writer.base` (haive-agents)
  - `haive.agents.wiki_writer.interview` (haive-agents)
  - `haive.agents.wiki_writer.interview.agent` (haive-agents)
  - `haive.agents.wiki_writer.interview.aug_llms` (haive-agents)
  - `haive.agents.wiki_writer.interview.models` (haive-agents)
  - `haive.agents.wiki_writer.interview.nodes` (haive-agents)
  - `haive.agents.wiki_writer.interview.state` (haive-agents)
  - ... and 6 more

### Chain 11: .base import (
- **Affected Modules**: 14
- **Packages**: haive-agents
- **Modules**:
  - `haive.agents.memory.search` (haive-agents)
  - `haive.agents.memory.search.base` (haive-agents)
  - `haive.agents.memory.search.deep_research` (haive-agents)
  - `haive.agents.memory.search.deep_research.agent` (haive-agents)
  - `haive.agents.memory.search.deep_research.models` (haive-agents)
  - `haive.agents.memory.search.labs` (haive-agents)
  - `haive.agents.memory.search.labs.agent` (haive-agents)
  - `haive.agents.memory.search.labs.models` (haive-agents)
  - `haive.agents.memory.search.pro_search` (haive-agents)
  - `haive.agents.memory.search.pro_search.agent` (haive-agents)
  - ... and 4 more

### Chain 12: haive.agents.memory_reorganized.search.base import (
- **Affected Modules**: 13
- **Packages**: haive-agents
- **Modules**:
  - `haive.agents.memory_reorganized.search` (haive-agents)
  - `haive.agents.memory_reorganized.search.deep_research` (haive-agents)
  - `haive.agents.memory_reorganized.search.deep_research.agent` (haive-agents)
  - `haive.agents.memory_reorganized.search.deep_research.models` (haive-agents)
  - `haive.agents.memory_reorganized.search.labs` (haive-agents)
  - `haive.agents.memory_reorganized.search.labs.agent` (haive-agents)
  - `haive.agents.memory_reorganized.search.labs.models` (haive-agents)
  - `haive.agents.memory_reorganized.search.pro_search` (haive-agents)
  - `haive.agents.memory_reorganized.search.pro_search.agent` (haive-agents)
  - `haive.agents.memory_reorganized.search.pro_search.models` (haive-agents)
  - ... and 3 more

### Chain 13: self_rag2
- **Affected Modules**: 12
- **Packages**: haive-agents
- **Modules**:
  - `haive.agents.rag.self_rag2` (haive-agents)
  - `haive.agents.rag.self_rag2.configuration` (haive-agents)
  - `haive.agents.rag.self_rag2.graph` (haive-agents)
  - `haive.agents.rag.self_rag2.nodes` (haive-agents)
  - `haive.agents.rag.self_rag2.nodes.decide_to_generate` (haive-agents)
  - `haive.agents.rag.self_rag2.nodes.generate` (haive-agents)
  - `haive.agents.rag.self_rag2.nodes.grade_documents` (haive-agents)
  - `haive.agents.rag.self_rag2.nodes.grade_generation_v_documents_and_question` (haive-agents)
  - `haive.agents.rag.self_rag2.nodes.retrieve` (haive-agents)
  - `haive.agents.rag.self_rag2.nodes.transform_query` (haive-agents)
  - ... and 2 more

### Chain 14: haive.agents.reflexion
- **Affected Modules**: 11
- **Packages**: haive-agents
- **Modules**:
  - `haive.agents.reasoning_and_critique.reflexion` (haive-agents)
  - `haive.agents.reasoning_and_critique.reflexion.agent` (haive-agents)
  - `haive.agents.reasoning_and_critique.reflexion.aug_llms` (haive-agents)
  - `haive.agents.reasoning_and_critique.reflexion.config` (haive-agents)
  - `haive.agents.reasoning_and_critique.reflexion.example` (haive-agents)
  - `haive.agents.reasoning_and_critique.reflexion.models` (haive-agents)
  - `haive.agents.reasoning_and_critique.reflexion.prompts` (haive-agents)
  - `haive.agents.reasoning_and_critique.reflexion.responder_with_retries` (haive-agents)
  - `haive.agents.reasoning_and_critique.reflexion.state` (haive-agents)
  - `haive.agents.reasoning_and_critique.reflexion.tools` (haive-agents)
  - ... and 1 more

### Chain 15: haive.dataflow.api.api
- **Affected Modules**: 11
- **Packages**: haive-dataflow, haive-games
- **Modules**:
  - `haive.dataflow.api.app` (haive-dataflow)
  - `haive.dataflow.api.app_dep` (haive-dataflow)
  - `haive.dataflow.api.game_api` (haive-dataflow)
  - `haive.dataflow.api.general_games_api` (haive-dataflow)
  - `haive.dataflow.api.main` (haive-dataflow)
  - `haive.dataflow.api.router` (haive-dataflow)
  - `haive.dataflow.api.run_game_api` (haive-dataflow)
  - `haive.dataflow.api.run_integrated_api` (haive-dataflow)
  - `haive.dataflow.main` (haive-dataflow)
  - `haive.games.api.general_api` (haive-games)
  - ... and 1 more

### Chain 16: game
- **Affected Modules**: 11
- **Packages**: haive-games
- **Modules**:
  - `haive.games.core.game` (haive-games)
  - `haive.games.core.game.containers` (haive-games)
  - `haive.games.core.game.containers.base` (haive-games)
  - `haive.games.core.game.containers.container` (haive-games)
  - `haive.games.core.game.containers.deck` (haive-games)
  - `haive.games.core.game.core_board` (haive-games)
  - `haive.games.core.game.core_game` (haive-games)
  - `haive.games.core.game.core_position` (haive-games)
  - `haive.games.core.game.core_space` (haive-games)
  - `haive.games.core.game.piece` (haive-games)
  - ... and 1 more

### Chain 17: haive.core.aug_llm
- **Affected Modules**: 11
- **Packages**: haive-dataflow, haive-prebuilt
- **Modules**:
  - `haive.dataflow.base` (haive-dataflow)
  - `haive.prebuilt.content.document_extractor` (haive-prebuilt)
  - `haive.prebuilt.content.summarizer` (haive-prebuilt)
  - `haive.prebuilt.content.tagger` (haive-prebuilt)
  - `haive.prebuilt.contract_analysis.aug_llms` (haive-prebuilt)
  - `haive.prebuilt.query.query_decomposer` (haive-prebuilt)
  - `haive.prebuilt.query.query_enhance` (haive-prebuilt)
  - `haive.prebuilt.query.query_intent` (haive-prebuilt)
  - `haive.prebuilt.query.query_rewriter` (haive-prebuilt)
  - `haive.prebuilt.query.query_to_sql` (haive-prebuilt)
  - ... and 1 more

### Chain 18: haive.core.schema.compatibility.compatibility import (
- **Affected Modules**: 10
- **Packages**: haive-core
- **Modules**:
  - `haive.core.schema.compatibility` (haive-core)
  - `haive.core.schema.compatibility.compatibility` (haive-core)
  - `haive.core.schema.compatibility.examples` (haive-core)
  - `haive.core.schema.compatibility.field_mapping` (haive-core)
  - `haive.core.schema.compatibility.langchain_converters` (haive-core)
  - `haive.core.schema.compatibility.mergers` (haive-core)
  - `haive.core.schema.compatibility.protocols` (haive-core)
  - `haive.core.schema.compatibility.reports` (haive-core)
  - `haive.core.schema.compatibility.utils` (haive-core)
  - `haive.core.schema.compatibility.validators` (haive-core)

### Chain 19: _llms
- **Affected Modules**: 10
- **Packages**: haive-agents
- **Modules**:
  - `haive.agents.reasoning_and_critique.lats` (haive-agents)
  - `haive.agents.reasoning_and_critique.lats.aug_llms` (haive-agents)
  - `haive.agents.reasoning_and_critique.lats.example` (haive-agents)
  - `haive.agents.reasoning_and_critique.lats.state` (haive-agents)
  - `haive.agents.reasoning_and_critique.lats.utils` (haive-agents)
  - `haive.agents.reasoning_and_critique.lats.v2` (haive-agents)
  - `haive.agents.reasoning_and_critique.lats.v2.agents` (haive-agents)
  - `haive.agents.reasoning_and_critique.lats.v2.models` (haive-agents)
  - `haive.agents.reasoning_and_critique.lats.v2.prompts` (haive-agents)
  - `haive.agents.reasoning_and_critique.lats.v2.state` (haive-agents)

### Chain 20: haive.agents.reasoning_and_critique.logic.models import (
- **Affected Modules**: 10
- **Packages**: haive-agents
- **Modules**:
  - `haive.agents.reasoning_and_critique.logic` (haive-agents)
  - `haive.agents.reasoning_and_critique.logic.agent` (haive-agents)
  - `haive.agents.reasoning_and_critique.logic.engines` (haive-agents)
  - `haive.agents.reasoning_and_critique.logic.engines.bias_detector` (haive-agents)
  - `haive.agents.reasoning_and_critique.logic.engines.logical_reasoner` (haive-agents)
  - `haive.agents.reasoning_and_critique.logic.engines.premise_extractor` (haive-agents)
  - `haive.agents.reasoning_and_critique.logic.engines.synthesis_agent` (haive-agents)
  - `haive.agents.reasoning_and_critique.logic.engines.uncertainty_analyzer` (haive-agents)
  - `haive.agents.reasoning_and_critique.logic.example` (haive-agents)
  - `haive.agents.reasoning_and_critique.logic.models` (haive-agents)

## Detailed Errors by Type


### ImportError (390 errors)


#### `haive.core.persistence.supabase_config`
- **Package**: haive-core
- **Error**: cannot import name 'SupabaseCheckpointerConfig' from 'haive.core.persistence' (/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/__init__.py)
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **Failed Import**: `SupabaseCheckpointerConfig`
- **This module imports**: 28 modules
  - `datetime` ✓
  - `datetime.datetime` ✓
  - `haive.core.persistence` ✓
  - `haive.core.persistence.SupabaseCheckpointerConfig` ✓
  - `haive.core.persistence.base` ✓

#### `haive.core.schema.example`
- **Package**: haive-core
- **Error**: cannot import name 'create_age' from 'haive.core.schema' (/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/__init__.py)
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **Failed Import**: `create_age`
- **This module imports**: 23 modules
  - `contextlib` ✓
  - `datetime` ✓
  - `haive.core.schema` ✓
  - `haive.core.schema.SchemaComposer` ✓
  - `haive.core.schema.StateSchema` ✓

#### `haive.core.graph.graph_builder2`
- **Package**: haive-core
- **Error**: cannot import name 'register_node' from 'haive.core.graph.node.registry' (/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/registry.py)
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **Failed Import**: `register_node`
- **This module imports**: 28 modules
  - `asyncio` ✓
  - `collections.abc` ✓
  - `collections.abc.Callable` ✓
  - `concurrent.futures` ✓
  - `enum` ✓
- **Imported by**: 1 modules
  - `haive.core.graph.routing` ❌

#### `haive.core.graph.NodeFactory`
- **Package**: haive-core
- **Error**: cannot import name 'Dict' from 'haive.core.engine.base' (/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/base/__init__.py)
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **Failed Import**: `Dict`
- **This module imports**: 45 modules
  - `collections.abc` ✓
  - `collections.abc.Callable` ✓
  - `functools` ✓
  - `functools.wraps` ✓
  - `haive.core.config.runnable` ✓
- **Imported by**: 1 modules
  - `haive.core.graph.StateGraphEditor` ❌

#### `haive.core.graph.StateGraphEditor`
- **Package**: haive-core
- **Error**: cannot import name 'register_graph_component' from 'haive.core.graph.graph_pattern_registry' (/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/graph_pattern_registry.py)
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **Failed Import**: `register_graph_component`
- **This module imports**: 31 modules
  - `collections.abc` ✓
  - `collections.abc.Callable` ✓
  - `haive.core.engine.base` ✓
  - `haive.core.engine.base.Engine` ✓
  - `haive.core.engine.base.registry` ✓

### ModuleNotFoundError (537 errors)


#### `haive.core.utils.parser_utils`
- **Package**: haive-core
- **Error**: No module named 'haive_agents_dep'
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 4 modules
  - `haive_agents_dep.self_discover.models` ✓
  - `haive_agents_dep.self_discover.models.ReasoningModule` ✓
  - `langchain_core.tools` ✓
  - `langchain_core.tools.BaseTool` ✓
- **Imported by**: 1 modules
  - `haive.agents.reasoning_and_critique.self_discover.aug_llms` ❌

#### `haive.core.utils.tool_list`
- **Package**: haive-core
- **Error**: No module named 'haive.core.utils.collections'
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 16 modules
  - `collections.abc` ✓
  - `collections.abc.Callable` ✓
  - `collections.abc.Sequence` ✓
  - `haive.core.utils.collections` ✓
  - `haive.core.utils.collections.NamedDict` ✓

#### `haive.core.persistence.store.postgres`
- **Package**: haive-core
- **Error**: No module named 'core'
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 25 modules
  - `base` ✓
  - `base.SerializableStoreWrapper` ✓
  - `core.persistence.postgres_config` ✓
  - `core.persistence.postgres_config.PostgresCheckpointerConfig` ✓
  - `langchain_community.embeddings` ✓

#### `haive.core.models.llm.export_llm_models_to_csv`
- **Package**: haive-core
- **Error**: No module named 'base'
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 6 modules
  - `base` ✓
  - `base.AnthropicLLMConfig` ✓
  - `base.DeepSeekLLMConfig` ✓
  - `base.MistralLLMConfig` ✓
  - `base.OpenAILLMConfig` ✓

#### `haive.core.utils.debugkit.debugging`
- **Package**: haive-core
- **Error**: No module named 'haive.core.utils.dev'
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 8 modules
  - `haive.core.utils.dev.debug_decorators` ✓
  - `haive.core.utils.dev.debug_decorators.debug_decorators` ✓
  - `haive.core.utils.dev.debug_enhanced` ✓
  - `haive.core.utils.dev.debug_enhanced.enhanced_debugger` ✓
  - `haive.core.utils.dev.debug_inspection` ✓

### TypeError (73 errors)


#### `haive.core.types.tree_leaf`
- **Package**: haive-core
- **Error**: Cannot create a consistent method resolution
order (MRO) for bases BaseModel, Generic, NodeMixin
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 10 modules
  - `__future__` ✓
  - `__future__.annotations` ✓
  - `pydantic` ✓
  - `pydantic.BaseModel` ✓
  - `pydantic.Field` ✓

#### `haive.core.schema.typed_state_schema`
- **Package**: haive-core
- **Error**: All parameters must be present on typing.Generic; you should inherit from typing.Generic[~TEngine, ~TEngines, ~TEngine].
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 21 modules
  - `__future__` ✓
  - `__future__.annotations` ✓
  - `haive.core.engine.base` ✓
  - `haive.core.engine.base.Engine` ✓
  - `haive.core.engine.base.types` ✓

#### `haive.core.graph.state_graph_manager`
- **Package**: haive-core
- **Error**: unsupported operand type(s) for |: 'builtin_function_or_method' and 'NoneType'
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 6 modules
  - `collections` ✓
  - `collections.defaultdict` ✓
  - `matplotlib.pyplot` ✓
  - `networkx` ✓
  - `typing` ✓

#### `haive.core.engine.document.loaders.sources.essential_sources`
- **Package**: haive-core
- **Error**: haive.core.engine.document.loaders.sources.enhanced_registry.register_source() got multiple values for keyword argument 'credential_type'
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 15 modules
  - `enhanced_registry` ✓
  - `enhanced_registry.enhanced_registry` ✓
  - `enhanced_registry.register_bulk_source` ✓
  - `enhanced_registry.register_database_source` ✓
  - `enhanced_registry.register_file_source` ✓

#### `haive.core.engine.document.loaders.sources.database.types`
- **Package**: haive-core
- **Error**: new enumerations should be created as `EnumName([mixin_type, ...] [data_type,] enum_type)`
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 2 modules
  - `enum` ✓
  - `enum.Enum` ✓

### NameError (37 errors)


#### `haive.core.engine.document.loaders.sources.specialized_sources`
- **Package**: haive-core
- **Error**: name 'field_validator' is not defined
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 19 modules
  - `enhanced_registry` ✓
  - `enhanced_registry.enhanced_registry` ✓
  - `enhanced_registry.register_file_source` ✓
  - `enhanced_registry.register_source` ✓
  - `enum` ✓

#### `haive.core.engine.document.loaders.sources.database_sources`
- **Package**: haive-core
- **Error**: name 'field_validator' is not defined
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 15 modules
  - `enhanced_registry` ✓
  - `enhanced_registry.enhanced_registry` ✓
  - `enhanced_registry.register_database_source` ✓
  - `enum` ✓
  - `enum.Enum` ✓

#### `haive.core.engine.document.loaders.sources.chat.base`
- **Package**: haive-core
- **Error**: name 'BaseSource' is not defined
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64

#### `haive.core.engine.embedding.providers.OllamaEmbeddingConfig`
- **Package**: haive-core
- **Error**: name 'field_validator' is not defined
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 13 modules
  - `haive.core.engine.embedding.base` ✓
  - `haive.core.engine.embedding.base.BaseEmbeddingConfig` ✓
  - `haive.core.engine.embedding.types` ✓
  - `haive.core.engine.embedding.types.EmbeddingType` ✓
  - `langchain_ollama` ✓

#### `haive.core.engine.embedding.providers.AzureOpenAIEmbeddingConfig`
- **Package**: haive-core
- **Error**: name 'field_validator' is not defined
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 13 modules
  - `haive.core.engine.embedding.base` ✓
  - `haive.core.engine.embedding.base.BaseEmbeddingConfig` ✓
  - `haive.core.engine.embedding.types` ✓
  - `haive.core.engine.embedding.types.EmbeddingType` ✓
  - `langchain_openai` ✓

### AttributeError (19 errors)


#### `haive.core.graph.node.agent_node_v2`
- **Package**: haive-core
- **Error**: type object 'NodeType' has no attribute 'COORDINATOR'
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **Missing Attribute**: `COORDINATOR`
- **This module imports**: 29 modules
  - `haive.agents.base.agent` ✓
  - `haive.agents.base.agent.Agent` ✓
  - `haive.core.graph.common.types` ✓
  - `haive.core.graph.common.types.ConfigLike` ✓
  - `haive.core.graph.common.types.NodeType` ✓

#### `haive.core.graph.node.message_transformation_v2`
- **Package**: haive-core
- **Error**: type object 'NodeType' has no attribute 'MESSAGE_TRANSFORMER'
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **Missing Attribute**: `MESSAGE_TRANSFORMER`
- **This module imports**: 34 modules
  - `collections.abc` ✓
  - `collections.abc.Callable` ✓
  - `enum` ✓
  - `enum.Enum` ✓
  - `haive.core.graph.common.types` ✓
- **Imported by**: 3 modules
  - `haive.agents.reflection.agent` ❌
  - `haive.agents.reflection.message_transformer` ❌
  - `haive.agents.reflection.message_transformer_posthook` ❌

#### `haive.core.graph.node.multi_agent_node`
- **Package**: haive-core
- **Error**: type object 'NodeType' has no attribute 'TRANSFORM'
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **Missing Attribute**: `TRANSFORM`
- **This module imports**: 21 modules
  - `haive.agents.base.agent` ✓
  - `haive.agents.base.agent.Agent` ✓
  - `haive.core.graph.common.types` ✓
  - `haive.core.graph.common.types.ConfigLike` ✓
  - `haive.core.graph.common.types.NodeType` ✓
- **Imported by**: 1 modules

#### `haive.agents.reflection.state`
- **Package**: haive-agents
- **Error**: type object 'NodeType' has no attribute 'MESSAGE_TRANSFORMER'
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **Missing Attribute**: `MESSAGE_TRANSFORMER`
- **This module imports**: 7 modules
  - `haive.agents.reflection.models` ❌ (AttributeError)
  - `haive.agents.reflection.models.Critique` ✓
  - `haive.agents.reflection.models.Improvement` ✓
  - `haive.core.schema.prebuilt.multi_agent_state` ✓
  - `haive.core.schema.prebuilt.multi_agent_state.MultiAgentState` ✓
- **Imported by**: 3 modules
  - `haive.agents.reasoning_and_critique.reflection.agent` ❌
  - `haive.agents.reasoning_and_critique.reflection.config` ❌
  - `haive.agents.reflection` ❌

#### `haive.agents.reflection.models`
- **Package**: haive-agents
- **Error**: type object 'NodeType' has no attribute 'MESSAGE_TRANSFORMER'
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **Missing Attribute**: `MESSAGE_TRANSFORMER`
- **This module imports**: 7 modules
  - `pydantic` ✓
  - `pydantic.BaseModel` ✓
  - `pydantic.Field` ✓
  - `pydantic.validator` ✓
  - `typing` ✓
- **Imported by**: 4 modules
  - `haive.agents.reasoning_and_critique.reflection.config` ❌
  - `haive.agents.reasoning_and_critique.reflection.state` ❌
  - `haive.agents.reflection.simple_agent` ❌
  - `haive.agents.reflection.state` ❌

### ValidationError (4 errors)


#### `haive.core.graph.node.test`
- **Package**: haive-core
- **Error**: 1 validation error for AugLLMConfig
system_prompt
  Extra inputs are not permitted [type=extra_forbidden, input_value='You are a helpful assist...an help me plan my day.', input_type=str]
    For further information visit https://errors.pydantic.dev/2.11/v/extra_forbidden
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 16 modules
  - `haive.core.engine.aug_llm` ✓
  - `haive.core.engine.aug_llm.AugLLMConfig` ✓
  - `haive.core.graph.node.config` ✓
  - `haive.core.graph.node.config.NodeConfig` ✓
  - `haive.core.graph.node.factory` ✓

#### `haive.core.graph.routers.test`
- **Package**: haive-core
- **Error**: 2 validation errors for StateValueCondition
key
  Field required [type=missing, input_value={'state_key': 'should_con... 'end', 'False': 'end'}}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.11/v/missing
value
  Field required [type=missing, input_value={'state_key': 'should_con... 'end', 'False': 'end'}}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.11/v/missing
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 2 modules
  - `haive.core.graph.routers.conditions` ✓
  - `haive.core.graph.routers.conditions.*` ✓

#### `haive.agents.simple.debug.v2`
- **Package**: haive-agents
- **Error**: 1 validation error for AugLLMConfig
system_prompt
  Extra inputs are not permitted [type=extra_forbidden, input_value='You are a helpful assistant.', input_type=str]
    For further information visit https://errors.pydantic.dev/2.11/v/extra_forbidden
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 7 modules
  - `haive.core.engine.aug_llm` ✓
  - `haive.core.engine.aug_llm.AugLLMConfig` ✓
  - `haive.core.models.llm.base` ✓
  - `haive.core.models.llm.base.AzureLLMConfig` ✓
  - `langchain_core.prompts` ✓

#### `haive.agents.simple.debug`
- **Package**: haive-agents
- **Error**: 1 validation error for AugLLMConfig
system_prompt
  Extra inputs are not permitted [type=extra_forbidden, input_value='You are a helpful assistant.', input_type=str]
    For further information visit https://errors.pydantic.dev/2.11/v/extra_forbidden
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 7 modules
  - `haive.core.engine.aug_llm` ✓
  - `haive.core.engine.aug_llm.AugLLMConfig` ✓
  - `haive.core.models.llm.base` ✓
  - `haive.core.models.llm.base.AzureLLMConfig` ✓
  - `langchain_core.prompts` ✓

### PydanticUndefinedAnnotation (1 errors)


#### `haive.agents.react.agent_v4`
- **Package**: haive-agents
- **Error**: name 'Agent' is not defined

For further information visit https://errors.pydantic.dev/2.11/u/undefined-annotation
- **Location**: /home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/pydantic/main.py:645
- **This module imports**: 10 modules
  - `contextlib` ✓
  - `haive.agents.simple.agent_v3` ✓
  - `haive.agents.simple.agent_v3.SimpleAgentV3` ✓
  - `haive.core.graph.state_graph.base_graph2` ✓
  - `haive.core.graph.state_graph.base_graph2.BaseGraph` ✓
- **Imported by**: 1 modules
  - `haive.agents.planning.plan_and_execute.agent` ❌

### PydanticSchemaGenerationError (2 errors)


#### `haive.agents.multi.enhanced_clean_multi_agent`
- **Package**: haive-agents
- **Error**: Unable to generate pydantic-core schema for <class 'haive.agents.simple.enhanced_simple_real.EnhancedAgentBase'>. Set `arbitrary_types_allowed=True` in the model_config to ignore this error or implement `__get_pydantic_core_schema__` on your type to fully support it.

If you got this error by calling handler(<some type>) within `__get_pydantic_core_schema__` then you likely need to call `handler.generate_schema(<some type>)` since we do not call `__get_pydantic_core_schema__` on `<some type>` otherwise to avoid infinite recursion.

For further information visit https://errors.pydantic.dev/2.11/u/schema-for-unknown-type
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 36 modules
  - `haive.agents.react.enhanced_react_agent` ✓
  - `haive.agents.react.enhanced_react_agent.ReactAgent` ✓
  - `haive.agents.simple.enhanced_simple_real` ✓
  - `haive.agents.simple.enhanced_simple_real.EnhancedAgentBase` ✓
  - `haive.agents.simple.enhanced_simple_real.SimpleAgent` ✓

#### `haive.agents.multi.archive.enhanced_clean_multi_agent`
- **Package**: haive-agents
- **Error**: Unable to generate pydantic-core schema for <class 'haive.agents.simple.enhanced_simple_real.EnhancedAgentBase'>. Set `arbitrary_types_allowed=True` in the model_config to ignore this error or implement `__get_pydantic_core_schema__` on your type to fully support it.

If you got this error by calling handler(<some type>) within `__get_pydantic_core_schema__` then you likely need to call `handler.generate_schema(<some type>)` since we do not call `__get_pydantic_core_schema__` on `<some type>` otherwise to avoid infinite recursion.

For further information visit https://errors.pydantic.dev/2.11/u/schema-for-unknown-type
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 30 modules
  - `haive.agents.react.enhanced_react_agent` ✓
  - `haive.agents.react.enhanced_react_agent.ReactAgent` ✓
  - `haive.agents.simple.enhanced_simple_real` ✓
  - `haive.agents.simple.enhanced_simple_real.EnhancedAgentBase` ✓
  - `haive.agents.simple.enhanced_simple_real.SimpleAgent` ✓

### PydanticUserError (3 errors)


#### `haive.agents.multi.archive.experiments.implementations.clean_multi_agent`
- **Package**: haive-agents
- **Error**: `const` is removed, use `Literal` instead

For further information visit https://errors.pydantic.dev/2.11/u/removed-kwargs
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 21 modules
  - `haive.agents.base.agent` ✓
  - `haive.agents.base.agent.Agent` ✓
  - `haive.core.graph.node.agent_node_v3` ✓
  - `haive.core.graph.node.agent_node_v3.AgentNodeV3Config` ✓
  - `haive.core.graph.state_graph.base_graph2` ✓

#### `haive.agents.multi.experiments.implementations.clean_multi_agent`
- **Package**: haive-agents
- **Error**: `const` is removed, use `Literal` instead

For further information visit https://errors.pydantic.dev/2.11/u/removed-kwargs
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 21 modules
  - `haive.agents.base.agent` ✓
  - `haive.agents.base.agent.Agent` ✓
  - `haive.core.graph.node.agent_node_v3` ✓
  - `haive.core.graph.node.agent_node_v3.AgentNodeV3Config` ✓
  - `haive.core.graph.state_graph.base_graph2` ✓

#### `haive.tools.tools.discord_tools`
- **Package**: haive-tools
- **Error**: Field 'name' defined on a base class was overridden by a non-annotated attribute. All field definitions, including overrides, require a type annotation.

For further information visit https://errors.pydantic.dev/2.11/u/model-field-overridden
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 4 modules
  - `dotenv` ✓
  - `dotenv.load_dotenv` ✓
  - `langchain_discord_shikenso.toolkits` ✓
  - `langchain_discord_shikenso.toolkits.DiscordToolkit` ✓

### KeyError (3 errors)


#### `haive.prebuilt.scientific_paper_agent.models`
- **Package**: haive-prebuilt
- **Error**: 'CORE_API_KEY'
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 9 modules
  - `os` ✓
  - `pydantic` ✓
  - `pydantic.BaseModel` ✓
  - `pydantic.Field` ✓
  - `time` ✓
- **Imported by**: 1 modules
  - `haive.prebuilt.scientific_paper_agent.nodes` ❌

#### `haive.prebuilt.scientific_paper_agent.nodes`
- **Package**: haive-prebuilt
- **Error**: 'CORE_API_KEY'
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 21 modules
  - `haive.prebuilt.scientific_paper_agent.models` ❌ (KeyError)
  - `haive.prebuilt.scientific_paper_agent.models.DecisionMakingOutput` ✓
  - `haive.prebuilt.scientific_paper_agent.models.JudgeOutput` ✓
  - `haive.prebuilt.scientific_paper_agent.prompts` ✓
  - `haive.prebuilt.scientific_paper_agent.prompts.agent_prompt` ✓
- **Imported by**: 1 modules
  - `haive.prebuilt.scientific_paper_agent.agent` ❌

#### `haive.prebuilt.scientific_paper_agent.agent`
- **Package**: haive-prebuilt
- **Error**: 'CORE_API_KEY'
- **Location**: /home/will/Projects/haive/backend/haive/analyze_import_dependencies.py:64
- **This module imports**: 8 modules
  - `haive.prebuilt.scientific_paper_agent.nodes` ❌ (KeyError)
  - `haive.prebuilt.scientific_paper_agent.nodes.agent_node` ✓
  - `haive.prebuilt.scientific_paper_agent.nodes.decision_making_node` ✓
  - `haive.prebuilt.scientific_paper_agent.nodes.judge_node` ✓
  - `haive.prebuilt.scientific_paper_agent.nodes.planning_node` ✓
