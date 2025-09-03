# Error Index by Type

## AttributeError (4 errors)

### haive-prebuilt

- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/essay_grading/state.py:0` - 'NoneType' object has no attribute 'with_structured_output'
  - ID: e6a75542
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/essay_grading/nodes.py:0` - 'NoneType' object has no attribute 'with_structured_output'
  - ID: c6bad80b
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:102` - 'NoneType' object has no attribute 'with_structured_output'
  - ID: 11b1cdf0
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/essay_grading/agent.py:0` - 'NoneType' object has no attribute 'with_structured_output'
  - ID: 4f8fafb0

## ImportError (120 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/supabase_config.py:33` - cannot import name 'SupabaseCheckpointerConfig' from 'haive.core.persistence' (/home/will/Projects/h
  - ID: b5b8bdb2
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/example.py:16` - cannot import name 'create_age' from 'haive.core.schema' (/home/will/Projects/haive/backend/haive/pa
  - ID: 6d1a2718
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/graph_builder2.py:16` - cannot import name 'register_node' from 'haive.core.graph.node.registry' (/home/will/Projects/haive/
  - ID: d9824c43
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/NodeFactory.py:16` - cannot import name 'Dict' from 'haive.core.engine.base' (/home/will/Projects/haive/backend/haive/pac
  - ID: 5be39b39
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/StateGraphEditor.py:12` - cannot import name 'register_graph_component' from 'haive.core.graph.graph_pattern_registry' (/home/
  - ID: e350bd40
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/routing.py:14` - cannot import name 'register_node' from 'haive.core.graph.node.registry' (/home/will/Projects/haive/
  - ID: 9e976dfe
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/universal_loader.py:54` - cannot import name 'ODPSource' from 'haive.core.engine.document.loaders.specific.files_office' (/hom
  - ID: c98a5a37
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/examples.py:27` - cannot import name 'LoaderPreference' from 'haive.core.engine.document.loaders.sources.enhanced_regi
  - ID: dde289c5
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/base.py:1` - cannot import name 'Document' from 'langchain.document_loaders.base' (/home/will/Projects/haive/back
  - ID: 54bc32bf
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/config.py:0` - cannot import name 'Document' from 'langchain.document_loaders.base' (/home/will/Projects/haive/back
  - ID: 76ca5cdb
- ... and 14 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/conversations/manager.py:11` - cannot import name 'SupabaseServerConfig' from 'haive.dataflow.config' (/home/will/Projects/haive/ba
  - ID: 2f26fc29
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/bin/litellm_cli.py:21` - cannot import name 'update_availability_status' from 'haive.dataflow.registry.importers.litellm_impo
  - ID: 3c41b04d
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/conversation_routes.py:55` - cannot import name 'AgentRegistry' from 'haive.core.registry' (/home/will/Projects/haive/backend/hai
  - ID: 37af55c3
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routers/games.py:11` - cannot import name 'GameInfo' from 'haive.games.api' (/home/will/Projects/haive/backend/haive/packag
  - ID: 308b6a4e
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/bin/litellm_cli.py:21` - cannot import name 'update_availability_status' from 'haive.dataflow.importers.litellm_importer' (/h
  - ID: b3780685

### haive-games

- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/example.py:19` - cannot import name 'GameAgent' from 'haive.games.framework' (/home/will/Projects/haive/backend/haive
  - ID: 4ba84a90
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/controller.py:11` - cannot import name 'AugLLMEngine' from 'haive.core.engine.aug_llm' (/home/will/Projects/haive/backen
  - ID: 06f99e5c
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/runner.py:12` - cannot import name 'AugLLMEngine' from 'haive.core.engine.aug_llm' (/home/will/Projects/haive/backen
  - ID: e6795209
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/configurable_config.py:13` - cannot import name 'MafiaConfig' from 'haive.games.mafia.config' (/home/will/Projects/haive/backend/
  - ID: 1e034ebc
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/aug_llms.py:25` - cannot import name 'MafiaAnalysis' from 'haive.games.mafia.models' (/home/will/Projects/haive/backen
  - ID: 26e2deb4
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/configurable_config.py:12` - cannot import name 'AmongUsConfig' from 'haive.games.among_us.config' (/home/will/Projects/haive/bac
  - ID: 5b8b6ccc
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/ui.py:18` - cannot import name 'ChessAgentConfig' from 'haive.games.chess.config' (/home/will/Projects/haive/bac
  - ID: 872f9022
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/state_manager.py:5` - cannot import name 'WordConnectionsState' from 'haive.games.base.state' (/home/will/Projects/haive/b
  - ID: f1959abd
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/bs/config.py:7` - cannot import name 'Any' from 'haive.games.cards.standard.bs.models' (/home/will/Projects/haive/back
  - ID: 3bff8759
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/base/config.py:6` - cannot import name 'GameState' from 'haive.games.core.base.state' (/home/will/Projects/haive/backend
  - ID: 1eeb208b
- ... and 4 more

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/manager.py:74` - cannot import name 'stdio_client' from 'langchain_mcp_adapters.client' (/home/will/Projects/haive/ba
  - ID: 5da62c3f
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/integration/aug_llm_mcp_extension.py:16` - cannot import name 'stdio_client' from 'langchain_mcp_adapters.client' (/home/will/Projects/haive/ba
  - ID: da96ee58
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/servers/http_server.py:15` - cannot import name 'SSEServerTransport' from 'mcp.server.sse' (/home/will/Projects/haive/backend/hai
  - ID: dc3aca05
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/servers/__init__.py:4` - cannot import name 'SSEServerTransport' from 'mcp.server.sse' (/home/will/Projects/haive/backend/hai
  - ID: 1cc44e2c
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/servers/simple_http_server.py:0` - cannot import name 'SSEServerTransport' from 'mcp.server.sse' (/home/will/Projects/haive/backend/hai
  - ID: 8814b454
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/servers/dataflow_server.py:0` - cannot import name 'SSEServerTransport' from 'mcp.server.sse' (/home/will/Projects/haive/backend/hai
  - ID: 6bbfec1b
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/servers/example_server_fastmcp.py:0` - cannot import name 'SSEServerTransport' from 'mcp.server.sse' (/home/will/Projects/haive/backend/hai
  - ID: 2b80ef85
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/utils/extract_mcp_github_repos.py:0` - cannot import name 'compute_content_hash' from 'haive.mcp.utils.extract_mcp_github_repos' (/home/wil
  - ID: 30ece397
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/utils/__init__.py:3` - cannot import name 'compute_content_hash' from 'haive.mcp.utils.extract_mcp_github_repos' (/home/wil
  - ID: 0f4504fd

### haive-prebuilt

- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/podcast_generator/nodes.py:3` - cannot import name 'Send' from 'langgraph.graph' (/home/will/Projects/haive/backend/haive/.venv/lib/
  - ID: 14c5478a
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/podcast_generator/agent.py:4` - cannot import name 'Send' from 'langgraph.graph' (/home/will/Projects/haive/backend/haive/.venv/lib/
  - ID: 2f38fc6d
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/startup/prompts.py:22` - cannot import name 'BusinessModelCanvas' from 'haive.prebuilt.startup.models' (/home/will/Projects/h
  - ID: d239bacf
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/utils.py:5` - cannot import name 'CompiledStateGraph' from 'langgraph.graph' (/home/will/Projects/haive/backend/ha
  - ID: e190a09a
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/tools.py:4` - cannot import name 'PDFStackT' from 'pdfminer.pdfinterp' (/home/will/Projects/haive/backend/haive/.v
  - ID: d2b8723f
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/agent.py:24` - cannot import name 'slide_content_aug_llm' from 'haive.prebuilt.startup.pitchdeck.prompts' (/home/wi
  - ID: 7079d1c9

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/google_calendar.py:0` - cannot import name 'from_config' from 'haive.tools.tools.toolkits.base' (/home/will/Projects/haive/b
  - ID: 256f79bd
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/nasa_toolkit.py:0` - cannot import name 'from_config' from 'haive.tools.tools.toolkits.base' (/home/will/Projects/haive/b
  - ID: e04deb1f
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/jira_toolkit.py:0` - cannot import name 'from_config' from 'haive.tools.tools.toolkits.base' (/home/will/Projects/haive/b
  - ID: 7a368698
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/nla_toolkit.py:0` - cannot import name 'from_config' from 'haive.tools.tools.toolkits.base' (/home/will/Projects/haive/b
  - ID: ef75fb34
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/gmail_toolkit.py:0` - cannot import name 'from_config' from 'haive.tools.tools.toolkits.base' (/home/will/Projects/haive/b
  - ID: 3b5ab859
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/twilio_toolkit.py:0` - cannot import name 'from_config' from 'haive.tools.tools.toolkits.base' (/home/will/Projects/haive/b
  - ID: f6d6d42e
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/free_to_game_toolkit.py:0` - cannot import name 'from_config' from 'haive.tools.tools.toolkits.base' (/home/will/Projects/haive/b
  - ID: 7a3152a5
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/rick_and_morty_toolkit.py:0` - cannot import name 'from_config' from 'haive.tools.tools.toolkits.base' (/home/will/Projects/haive/b
  - ID: 162a0d3c
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/yugiioh_toolkit.py:0` - cannot import name 'from_config' from 'haive.tools.tools.toolkits.base' (/home/will/Projects/haive/b
  - ID: 8800e74a
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/citydsk_toolkit.py:0` - cannot import name 'from_config' from 'haive.tools.tools.toolkits.base' (/home/will/Projects/haive/b
  - ID: 71199624
- ... and 52 more

## KeyError (3 errors)

### haive-prebuilt

- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/models.py:9` - 'CORE_API_KEY'
  - ID: d6ce0610
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/nodes.py:8` - 'CORE_API_KEY'
  - ID: 5df03b64
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/agent.py:3` - 'CORE_API_KEY'
  - ID: 1ac72618

## ModuleNotFoundError (1367 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/state.py:0` - No module named 'haive.agents.simple.models'
  - ID: 6aecc315
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base.py:0` - No module named 'haive.agents.simple.models'
  - ID: 14667ec9
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/config.py:0` - No module named 'haive.agents.simple.models'
  - ID: 6a49f067
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/models.py:0` - No module named 'haive.agents.simple.models'
  - ID: 3306a833
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/factory.py:0` - No module named 'haive.agents.simple.models'
  - ID: 238ac816
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/tool_utils.py:0` - No module named 'haive.agents.simple.models'
  - ID: ac0f744b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/__init__.py:98` - No module named 'haive.agents.simple.models'
  - ID: 6d37f5aa
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/state_wrapper.py:0` - No module named 'haive.agents.simple.models'
  - ID: 165b554f
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/qa_agent.py:0` - No module named 'haive.agents.simple.models'
  - ID: 910e2871
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:0` - No module named 'haive.agents.simple.models'
  - ID: ce782d42
- ... and 1098 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/parser_utils.py:1` - No module named 'haive_agents_dep'
  - ID: 16f2e474
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/tool_list.py:13` - No module named 'haive.core.utils.collections'
  - ID: 038a9cc8
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/postgres.py:13` - No module named 'core'
  - ID: a3845c66
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/export_llm_models_to_csv.py:21` - No module named 'base'
  - ID: 1838f735
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/debugging.py:34` - No module named 'haive.core.utils.dev'
  - ID: 5cfb88fc
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/benchmarking/core.py:38` - No module named 'haive.core.utils.dev'
  - ID: e1775c27
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/transformers/base.py:0` - No module named 'haive.core.common.config'
  - ID: f9d93b07
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/transformers/__init__.py:78` - No module named 'haive.core.common.config'
  - ID: 12ab49ff
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/transformers/engine.py:14` - No module named 'haive.core.common.config'
  - ID: ca4261e4
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/transformers/types.py:0` - No module named 'haive.core.common.config'
  - ID: 9368ac49
- ... and 62 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/base.py:9` - No module named 'haive.core.aug_llm'
  - ID: baf7c244
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/app_dep.py:10` - No module named 'haive.dataflow.api.api'
  - ID: 09314930
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/main.py:13` - No module named 'haive.dataflow.api.routes.auth'
  - ID: f7e0374d
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/tic_tac_toe_api.py:10` - No module named 'haive_games'
  - ID: a866908b
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/game_agent.py:14` - No module named 'haive.dataflow.engine'
  - ID: 5b25a3cb
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/connect4_api.py:12` - No module named 'haive.api'
  - ID: 9702ea92
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/__init___lazy.py:55` - No module named 'haive.dataflow.registry.registry'
  - ID: f13779d4
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/llms/api.py:17` - No module named 'haive.dataflow.llms.api.llms'; 'haive.dataflow.llms.api' is not a package
  - ID: 8d15e115
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/persistence/conversations.py:51` - No module named 'haive.dataflow.persistence.config'
  - ID: c5677fb3
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/internal_websockets/handlers.py:12` - No module named 'haive.dataflow.internal_websockets.auth'
  - ID: af36fa4d
- ... and 40 more

### haive-games

- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/benchmark.py:16` - No module named 'haive.games.monopoly.test'
  - ID: c7f5847d
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/llm_config_factory.py:12` - No module named 'haive.games.models'
  - ID: 9392ca51
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/common/voting_system.py:18` - No module named 'haive.games.simple'
  - ID: ea4c8c93
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/configurable_config.py:13` - No module named 'haive.games.models'
  - ID: 111fa9f4
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/generic_engines.py:20` - No module named 'haive.games.models'
  - ID: 5a160ea0
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/verify_imports.py:8` - No module named 'models'
  - ID: 1aec43dc
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/api/setup.py:14` - No module named 'haive.dataflow.api.engine'
  - ID: 787f491b
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/api/general_api.py:20` - No module named 'haive.dataflow.api.engine'
  - ID: c3ffbd96
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/example_with_judges.py:0` - No module named 'haive.agents.simple.models'
  - ID: 40fe29bd
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/__init__.py:3` - No module named 'haive.agents.simple.models'
  - ID: b060b7fc
- ... and 46 more

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/comprehensive_mcp_web.py:18` - No module named 'csv_viewer'
  - ID: 0069842a
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/haive_agent_mcp_integration.py:16` - No module named 'fastmcp_runner'
  - ID: c051b9c1
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mcp_simple_tool_agent.py:12` - No module named 'haive.agents.simple.models'
  - ID: d986af01
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/enhanced_parent_self_query_retriever.py:26` - No module named 'haive.agents.simple.models'
  - ID: 5b6b8fa5
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/simple_faiss_retriever.py:17` - No module named 'haive.agents.simple.models'
  - ID: df9c82e5
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/dynamic_mcp_tool.py:22` - No module named 'haive.agents.simple.models'
  - ID: 2ff7311e
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mcp_rag_agent.py:13` - No module named 'haive.agents.simple.models'
  - ID: 885e92a4
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/working_enhanced_retriever.py:21` - No module named 'haive.agents.simple.models'
  - ID: aae31a40
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/fastapi_mcp_server.py:24` - No module named 'haive.agents.simple.models'
  - ID: 32545dcb
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/integrated_mcp_system.py:26` - No module named 'csv_viewer'
  - ID: 8370dfaa
- ... and 29 more

### haive-prebuilt

- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/project_manager/agent.py:1` - No module named 'haive.agents.simple.models'
  - ID: 3b31adce
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/contract_analysis/agent.py:1` - No module named 'haive.agents.simple.models'
  - ID: dadd86cd
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/state.py:7` - No module named 'haive.haive'
  - ID: 2b2afb1a
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:31` - No module named 'haive.haive'
  - ID: a53b565f
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/agent.py:4` - No module named 'haive.agents.simple.models'
  - ID: 2adb8669
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/startup/agent.py:16` - No module named 'haive.prebuilt.startup.business_model_subgraph'
  - ID: e3f8721d
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/state.py:7` - No module named 'haive.haive'
  - ID: 36060875
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/misc/agent_utilities_prompts.py:9` - No module named 'haive.agents.simple.models'
  - ID: bb36395b
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/misc/__init__.py:50` - No module named 'haive.agents.simple.models'
  - ID: 2f42334f
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/company_researcher/config.py:15` - No module named 'haive.prebuilt.prompts'
  - ID: 3f432f2f
- ... and 27 more

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/dataforseo_tool.py:23` - No module named 'haive.config'
  - ID: 3f977239
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/hinge_tools.py:22` - No module named 'squeaky_hinge'
  - ID: ccc7cfa7
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/wolfram_alpha_tool.py:39` - No module named 'haive.config'
  - ID: 037d5972
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/bing_search_tool_INC.py:11` - No module named 'haive.config'
  - ID: 77533efa
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/ionic_tool.py:19` - No module named 'ionic_langchain'
  - ID: e627bd4f

## NameError (22 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/specialized_sources.py:310` - name 'field_validator' is not defined
  - ID: 8c329408
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/database_sources.py:149` - name 'field_validator' is not defined
  - ID: d795b853
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/chat/base.py:1` - name 'BaseSource' is not defined
  - ID: 3699834d
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/OllamaEmbeddingConfig.py:12` - name 'field_validator' is not defined
  - ID: 2424fa4f
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/AzureOpenAIEmbeddingConfig.py:13` - name 'field_validator' is not defined
  - ID: 57cddeef
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/FakeEmbeddingConfig.py:12` - name 'field_validator' is not defined
  - ID: eb2ea8a1
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/OpenAIEmbeddingConfig.py:12` - name 'field_validator' is not defined
  - ID: 2016423c
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/GoogleVertexAIEmbeddingConfig.py:12` - name 'field_validator' is not defined
  - ID: 4682f53e
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/CohereEmbeddingConfig.py:12` - name 'field_validator' is not defined
  - ID: 6f98feb9
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/messages/examples.py:14` - name 'Any' is not defined
  - ID: 876ba10a
- ... and 6 more

### haive-games

- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/example.py:1` - name 'SinglePlayerGameAgent' is not defined
  - ID: d3826684
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/piece/tile.py:1` - name 'GamePiece' is not defined
  - ID: 9753aebb
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/towers_of_hanoi/position.py:6` - name 'PegNumber' is not defined
  - ID: c3792854
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py:5` - name 'GridBoard' is not defined
  - ID: 3871869d
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:5` - name 'GridBoard' is not defined
  - ID: 74d1cdd8

### haive-prebuilt

- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/simple/questiona_and_answer_generator/models.py:6` - Unexpected field with name 'question'; only 'root' is allowed as a field of a `RootModel`
  - ID: 3eed350e

## PydanticUserError (1 errors)

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/discord_tools.py:28` - Field 'name' defined on a base class was overridden by a non-annotated attribute. All field definiti
  - ID: fe3e7e69

## TypeError (36 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/types/tree_leaf.py:52` - Cannot create a consistent method resolution
  order (MRO) for bases BaseModel, Generic, NodeMixin
  - ID: 7abdfdaa
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/typed_state_schema.py:24` - All parameters must be present on typing.Generic; you should inherit from typing.Generic[~TEngine, ~
  - ID: f9ad2399
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph_manager.py:8` - unsupported operand type(s) for |: 'builtin_function_or_method' and 'NoneType'
  - ID: 1ffb38b8
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/essential_sources.py:348` - haive.core.engine.document.loaders.sources.enhanced_registry.register_source() got multiple values f
  - ID: f7284e51
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/database/types.py:4` - new enumerations should be created as `EnumName([mixin_type, ...] [data_type,] enum_type)`
  - ID: 19a1fee7
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/stateful_node_config.py:31` - unsupported operand type(s) for |: 'builtin_function_or_method' and 'NoneType'
  - ID: 895d2211
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/gb/__init__.py:21` - Callable must be used as Callable[[arg, ...], result].
  - ID: 4afdcdee
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/gb/types.py:0` - Callable must be used as Callable[[arg, ...], result].
  - ID: 15341a6b

### haive-games

- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/configurable_config.py:13` - Can't instantiate abstract class CluePromptGenerator without an implementation for abstract methods
  - ID: dc4c604b
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/generic_engines.py:112` - Can't instantiate abstract class CluePromptGenerator without an implementation for abstract methods
  - ID: 76e37ceb
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/configurable_config.py:14` - Can't instantiate abstract class MastermindPromptGenerator without an implementation for abstract me
  - ID: 65a92507
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/generic_engines.py:112` - Can't instantiate abstract class MastermindPromptGenerator without an implementation for abstract me
  - ID: d9279ae3
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/generic_engines.py:112` - Can't instantiate abstract class MafiaPromptGenerator without an implementation for abstract methods
  - ID: 5bdbacce
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/configurable_config.py:14` - Can't instantiate abstract class DominoesPromptGenerator without an implementation for abstract meth
  - ID: 29046c19
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/generic_engines.py:112` - Can't instantiate abstract class DominoesPromptGenerator without an implementation for abstract meth
  - ID: 232e8067
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/configurable_config.py:15` - Can't instantiate abstract class HoldemPromptGenerator without an implementation for abstract method
  - ID: 44cd723f
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/generic_engines.py:134` - Can't instantiate abstract class HoldemPromptGenerator without an implementation for abstract method
  - ID: d8a411eb
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/configurable_config.py:14` - Can't instantiate abstract class NimPromptGenerator without an implementation for abstract methods '
  - ID: 16f7adf7
- ... and 16 more

### haive-prebuilt

- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/taskifier/agent.py:12` - NoneType takes no arguments
  - ID: 74a6653c

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/brave_search.py:24` - 'module' object is not callable
  - ID: 71409bee

## ValidationError (2 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/test.py:21` - 1 validation error for AugLLMConfig
  system_prompt
  Extra inputs are not permitted [type=extra_forbi
  - ID: 33ed920b
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/routers/test.py:3` - 2 validation errors for StateValueCondition
  key
  Field required [type=missing, input*value={'state*
  - ID: 9b46a8f0

## mypy:'=', '!=', '>', '<', '>=', '<=' (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/models.py:91` - error: Returning Any from function declared to return "Literal['=', '!=', '>', '<', '>=', '<='] | No
  - ID: aff0287a

## mypy:'**end**' (4 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/agent.py:520` - error: Returning Any from function declared to return "str | Literal['__end__']" [no-any-return]
  - ID: 2b51f900
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/agent.py:534` - error: Incompatible return value type (got "str", expected "Literal['__end__'] | list[Send]") [retu
  - ID: adb56495
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/agent.py:543` - error: Incompatible return value type (got "str", expected "Literal['__end__'] | list[Send]") [retu
  - ID: febab021
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/agent.py:590` - error: Returning Any from function declared to return "str | Literal['__end__']" [no-any-return]
  - ID: 30ec5330

## mypy:'after' (4 errors)

### haive-games

- `packages/haive-games/src/haive/games/core/components/cards/standard.py:67` - note: def field_validator(str, /, \*fields: str, mode: Literal['after'] = ..., check_fields: bool
  - ID: cda3136a
- `packages/haive-games/src/haive/games/core/components/cards/standard.py:80` - note: def field_validator(str, /, \*fields: str, mode: Literal['after'] = ..., check_fields: bool
  - ID: f6d8ee01
- `packages/haive-games/src/haive/games/core/components/cards/standard.py:90` - note: def field_validator(str, /, \*fields: str, mode: Literal['after'] = ..., check_fields: bool
  - ID: dee944cc
- `packages/haive-games/src/haive/games/core/components/cards/standard.py:105` - note: def field_validator(str, /, \*fields: str, mode: Literal['after'] = ..., check_fields: bool
  - ID: 1fd6a195

## mypy:'before', 'plain' (4 errors)

### haive-games

- `packages/haive-games/src/haive/games/core/components/cards/standard.py:67` - note: def field_validator(str, /, \*fields: str, mode: Literal['before', 'plain'], check_fields:
  - ID: a18a88c1
- `packages/haive-games/src/haive/games/core/components/cards/standard.py:80` - note: def field_validator(str, /, \*fields: str, mode: Literal['before', 'plain'], check_fields:
  - ID: d8eae43c
- `packages/haive-games/src/haive/games/core/components/cards/standard.py:90` - note: def field_validator(str, /, \*fields: str, mode: Literal['before', 'plain'], check_fields:
  - ID: 29b28819
- `packages/haive-games/src/haive/games/core/components/cards/standard.py:105` - note: def field_validator(str, /, \*fields: str, mode: Literal['before', 'plain'], check_fields:
  - ID: 203e5d0e

## mypy:'beginner', 'intermediate', 'expert', 'world-class' (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/reflection/agent.py:328` - error: Argument "expertise_level" to "ExpertiseConfig" has incompatible type "str"; expected "Litera
  - ID: 7c91daea

## mypy:'critical', 'high', 'medium', 'low' (1 errors)

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:450` - error: Argument "severity" to "ProblemStatement" has incompatible type "str"; expected "Literal['cri
  - ID: 27a3e0ed

## mypy:'off', 'moderate', 'strict' (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/retriever/providers/YouRetrieverConfig.py:164` - error: Argument "safesearch" to "YouRetriever" has incompatible type "str"; expected "Literal['off',
  - ID: 3f6bf9bb

## mypy:'open', 'closed', 'all' (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/research/open_perplexity/structured_tools.py:470` - error: Argument "state" to "EnhancedGitHubIssuesLoader" has incompatible type "str"; expected "Liter
  - ID: 26fd56b3

## mypy:'pass' (7 errors)

### haive-games

- `packages/haive-games/src/haive/games/dominoes/state_manager.py:109` - error: Item "str" of "Any | Literal['pass']" has no attribute "tile" [union-attr]
  - ID: 837fb2d5
- `packages/haive-games/src/haive/games/dominoes/state_manager.py:110` - error: Item "str" of "Any | Literal['pass']" has no attribute "location" [union-attr]
  - ID: 87b741fa
- `packages/haive-games/src/haive/games/dominoes/agent.py:210` - error: Item "str" of "Any | Literal['pass']" has no attribute "tile" [union-attr]
  - ID: 27dc5972
- `packages/haive-games/src/haive/games/dominoes/agent.py:211` - error: Item "str" of "Any | Literal['pass']" has no attribute "tile" [union-attr]
  - ID: 4bd5619b
- `packages/haive-games/src/haive/games/dominoes/agent.py:214` - error: Item "str" of "Any | Literal['pass']" has no attribute "tile" [union-attr]
  - ID: 5b5a37d8
- `packages/haive-games/src/haive/games/dominoes/agent.py:215` - error: Item "str" of "Any | Literal['pass']" has no attribute "tile" [union-attr]
  - ID: 7d7151b9
- `packages/haive-games/src/haive/games/dominoes/agent.py:217` - error: Item "str" of "Any | Literal['pass']" has no attribute "location" [union-attr]
  - ID: 98902c71

## mypy:'v1', 'v2' (2 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/simple/agent_v2.v2.py:504` - error: Incompatible types in assignment (expression has type "str", variable has type "Literal['v1',
  - ID: 1d1a9a7c
- `packages/haive-agents/src/haive/agents/simple/agent_v2.py:514` - error: Incompatible types in assignment (expression has type "str", variable has type "Literal['v1',
  - ID: 461fc7c1

## mypy:'wrap' (4 errors)

### haive-games

- `packages/haive-games/src/haive/games/core/components/cards/standard.py:67` - note: def field_validator(str, /, \*fields: str, mode: Literal['wrap'], check_fields: bool | None
  - ID: bba760fe
- `packages/haive-games/src/haive/games/core/components/cards/standard.py:80` - note: def field_validator(str, /, \*fields: str, mode: Literal['wrap'], check_fields: bool | None
  - ID: 65ab254e
- `packages/haive-games/src/haive/games/core/components/cards/standard.py:90` - note: def field_validator(str, /, \*fields: str, mode: Literal['wrap'], check_fields: bool | None
  - ID: 39f2bbb0
- `packages/haive-games/src/haive/games/core/components/cards/standard.py:105` - note: def field_validator(str, /, \*fields: str, mode: Literal['wrap'], check_fields: bool | None
  - ID: b4399d7e

## mypy:() (2 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/planning/llm_compiler/output_parser.py:33` - error: Incompatible return value type (got "tuple[()]", expected "list[Any]") [return-value]
  - ID: b215eba1
- `packages/haive-agents/src/haive/agents/planning/llm_compiler/output_parser.py:35` - error: Incompatible return value type (got "tuple[()]", expected "list[Any]") [return-value]
  - ID: a50be9e3

## mypy:... (42 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/base/mixins/hooks_mixin.py:24` - error: Free type variable expected in Generic[...] [misc]
  - ID: 840700ad
- `packages/haive-agents/src/haive/agents/base/compiled_agent.py:46` - error: Parameter 1 of Literal[...] cannot be of type "Any" [valid-type]
  - ID: 6bc26879
- `packages/haive-agents/src/haive/agents/discovery/semantic_discovery.py:33` - error: Cannot assign multiple types to name "UnifiedHaiveDiscovery" without an explicit "type[...]"
  - ID: 42791746
- `packages/haive-agents/src/haive/agents/base/enhanced_agent.py:111` - error: Parameter 1 of Literal[...] cannot be of type "Any" [valid-type]
  - ID: ec237f22
- `packages/haive-agents/src/haive/agents/base/agent.py:89` - error: Parameter 1 of Literal[...] cannot be of type "Any" [valid-type]
  - ID: e87beb84
- `packages/haive-agents/src/haive/agents/research/person/agent.py:477` - error: Parameter 1 of Literal[...] is invalid [valid-type]
  - ID: 10f18b4f

### haive-core

- `packages/haive-core/src/haive/core/graph/state_graph/mixin.py:10` - error: Free type variable expected in Generic[...] [misc]
  - ID: 87f4ac45
- `packages/haive-core/src/haive/core/engine/prompt_template/prompt_engine.py:314` - error: Cannot assign multiple types to name "base_type" without an explicit "type[...]" annotation
  - ID: 143b890a
- `packages/haive-core/src/haive/core/engine/prompt_template/prompt_engine.py:319` - error: Cannot assign multiple types to name "base_type" without an explicit "type[...]" annotation
  - ID: 1151be5e
- `packages/haive-core/src/haive/core/engine/prompt_template/prompt_engine.py:323` - error: Cannot assign multiple types to name "base_type" without an explicit "type[...]" annotation
  - ID: 773bfb82
- `packages/haive-core/src/haive/core/engine/prompt_template/prompt_engine.py:328` - error: Cannot assign multiple types to name "base_type" without an explicit "type[...]" annotation
  - ID: e9c6ea3c
- `packages/haive-core/src/haive/core/engine/prompt_template/prompt_engine.py:346` - error: Cannot assign multiple types to name "output_type" without an explicit "type[...]" annotation
  - ID: 9f88ae6e
- `packages/haive-core/src/haive/core/graph/branches/types.py:45` - error: Free type variable expected in Generic[...] [misc]
  - ID: 9c1707be
- `packages/haive-core/src/haive/core/engine/agent/persistence/memory_config.py:17` - error: Parameter 1 of Literal[...] cannot be of type "Any" [valid-type]
  - ID: 976105e9
- `packages/haive-core/src/haive/core/engine/agent/persistence/mongodb_config.py:28` - error: Parameter 1 of Literal[...] cannot be of type "Any" [valid-type]
  - ID: 68a786db
- `packages/haive-core/src/haive/core/schema/field_utils.py:520` - note: Perhaps you need "Callable[...]" or a callback protocol?
  - ID: b2ea1e80
- ... and 3 more

### haive-games

- `packages/haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:14` - error: Free type variable expected in Generic[...] [misc]
  - ID: 6f2eebb3
- `packages/haive-games/src/haive/games/core/game/piece.py:12` - error: Free type variable expected in Generic[...] [misc]
  - ID: 869cf247
- `packages/haive-games/src/haive/games/core/components/cards/turns.py:21` - error: Free type variable expected in Generic[...] [misc]
  - ID: c1918dd5
- `packages/haive-games/src/haive/games/core/components/cards/turns.py:54` - error: Free type variable expected in Generic[...] [misc]
  - ID: a39d5ee3
- `packages/haive-games/src/haive/games/core/components/cards/scoring.py:10` - error: Free type variable expected in Generic[...] [misc]
  - ID: df48487e
- `packages/haive-games/src/haive/games/core/components/cards/scoring.py:29` - error: Free type variable expected in Generic[...] [misc]
  - ID: 9083e42f
- `packages/haive-games/src/haive/games/core/components/cards/actions.py:12` - error: Free type variable expected in Generic[...] [misc]
  - ID: 529bd839
- `packages/haive-games/src/haive/games/hold_em/player_agent.py:635` - error: Parameter 1 of Literal[...] is invalid [valid-type]
  - ID: b64ea57a

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:53` - note: Suggestion: use conint[...] instead of conint(...)
  - ID: 9c510836
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:119` - note: Suggestion: use confloat[...] instead of confloat(...)
  - ID: b760533b
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:144` - note: Suggestion: use confloat[...] instead of confloat(...)
  - ID: bdfb5690
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:160` - note: Suggestion: use confloat[...] instead of confloat(...)
  - ID: 97ad0dc8
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:179` - note: Suggestion: use confloat[...] instead of confloat(...)
  - ID: 36ce105f
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:203` - note: Suggestion: use confloat[...] instead of confloat(...)
  - ID: 863756af
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/models.py:42` - note: Suggestion: use confloat[...] instead of confloat(...)
  - ID: e2914b0e
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/models.py:72` - note: Suggestion: use confloat[...] instead of confloat(...)
  - ID: 57656952
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/models.py:121` - note: Suggestion: use confloat[...] instead of confloat(...)
  - ID: 069173ee
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/models.py:124` - note: Suggestion: use confloat[...] instead of confloat(...)
  - ID: 7019514c
- ... and 5 more

## mypy:..., Any (33 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/base/mixins/hooks_mixin.py:238` - error: "Callable[..., Any]" has no attribute "\_hook_metadata" [attr-defined]
  - ID: e20617e5
- `packages/haive-agents/src/haive/agents/memory_v2/standalone_rag_memory.py:670` - note: def tool(name_or_callable: Callable[..., Any], \*, description: str | None = ..., return_di
  - ID: b69f1c78
- `packages/haive-agents/src/haive/agents/memory_v2/long_term_memory_agent.py:475` - note: def tool(name_or_callable: Callable[..., Any], \*, description: str | None = ..., return_di
  - ID: 838654c0
- `packages/haive-agents/src/haive/agents/memory_reorganized/agents/ltm.py:464` - note: def tool(name_or_callable: Callable[..., Any], \*, description: str | None = ..., return_di
  - ID: acb5692b
- `packages/haive-agents/src/haive/agents/memory_v2/rag_memory_agent.py:633` - note: def tool(name_or_callable: Callable[..., Any], \*, description: str | None = ..., return_di
  - ID: 24771bb4
- `packages/haive-agents/src/haive/agents/simple/agent_v3.py:1207` - note: def tool(name_or_callable: Callable[..., Any], \*, description: str | None = ..., return_di
  - ID: 738b9fc3
- `packages/haive-agents/src/haive/agents/simple/agent_v3.py:1258` - note: def tool(name_or_callable: Callable[..., Any], \*, description: str | None = ..., return_di
  - ID: a31dde19
- `packages/haive-agents/src/haive/agents/react_class/react_v2/agent.py:115` - note: def tool(name_or_callable: Callable[..., Any], \*, description: str | None = ..., return_di
  - ID: a775cab3
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/v2/agents.py:64` - error: List item 0 has incompatible type "str"; expected "BaseTool | Callable[..., Any]" [list-item
  - ID: 5f79040b

### haive-core

- `packages/haive-core/src/haive/core/utils/debugkit/debug/decorators.py:47` - error: Returning Any from function declared to return "Callable[..., Any]" [no-any-return]
  - ID: 0c8277ff
- `packages/haive-core/src/haive/core/utils/debugkit/tracing/execution.py:293` - error: Returning Any from function declared to return "Callable[..., Any]" [no-any-return]
  - ID: e38a634d
- `packages/haive-core/src/haive/core/utils/debugkit/tracing/execution.py:295` - error: Returning Any from function declared to return "Callable[..., Any]" [no-any-return]
  - ID: 1c00124f
- `packages/haive-core/src/haive/core/utils/debugkit/profiling/performance.py:191` - error: Returning Any from function declared to return "Callable[..., Any]" [no-any-return]
  - ID: 1e8d3f61
- `packages/haive-core/src/haive/core/graph/common/references.py:78` - error: "Callable[..., Any]" has no attribute "func" [attr-defined]
  - ID: ca68fdf1
- `packages/haive-core/src/haive/core/graph/common/references.py:82` - error: "Callable[..., Any]" has no attribute "args" [attr-defined]
  - ID: 81eed49c
- `packages/haive-core/src/haive/core/graph/common/references.py:83` - error: "Callable[..., Any]" has no attribute "keywords" [attr-defined]
  - ID: 35eb5833
- `packages/haive-core/src/haive/core/graph/common/references.py:114` - error: Returning Any from function declared to return "Callable[..., Any] | None" [no-any-return]
  - ID: 4f2d0677
- `packages/haive-core/src/haive/core/graph/common/references.py:132` - error: Returning Any from function declared to return "Callable[..., Any] | None" [no-any-return]
  - ID: 253df5c2
- `packages/haive-core/src/haive/core/graph/common/references.py:145` - error: Returning Any from function declared to return "Callable[..., Any] | None" [no-any-return]
  - ID: 9c071e8b
- ... and 14 more

## mypy:..., Awaitable[Any (2 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/tool_utils.py:46` - error: Argument "coroutine" to "from_function" of "StructuredTool" has incompatible type "bool"; exp
  - ID: ae35f39c
- `packages/haive-agents/src/haive/agents/react_class/react/tool_utils.py:44` - error: Argument "coroutine" to "from_function" of "StructuredTool" has incompatible type "bool"; exp
  - ID: 6680d834

## mypy:<type> (195 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/task_analysis/tree/models.py:186` - error: Need type annotation for "processed" (hint: "processed: set[<type>] = ...") [var-annotated]
  - ID: 63638301
- `packages/haive-agents/src/haive/agents/task_analysis/decomposer/__init__.py:17` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: 566e33ed
- `packages/haive-agents/src/haive/agents/task_analysis/analysis/__init__.py:17` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: 31ae2e86
- `packages/haive-agents/src/haive/agents/research/storm/wiki_writer/__init__.py:1` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: 9dd8affd
- `packages/haive-agents/src/haive/agents/research/storm/outline_refiner/__init__.py:1` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: f226d7cb
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/engines/__init__.py:17` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: dd20f950
- `packages/haive-agents/src/haive/agents/react_class/__init__.py:22` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: 5bf1b15f
- `packages/haive-agents/src/haive/agents/rag/simple/__init__.py:6` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: 6c19e14e
- `packages/haive-agents/src/haive/agents/rag/db_rag/__init__.py:10` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: 539fb257
- `packages/haive-agents/src/haive/agents/rag/common/document_graders/binary_grader/__init__.py:17` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: 5427f755
- ... and 51 more

### haive-core

- `packages/haive-core/src/haive/core/schema/mixins/__init__.py:12` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: cd923305
- `packages/haive-core/src/haive/core/models/embeddings/filter/__init__.py:122` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: b05a0ac5
- `packages/haive-core/src/haive/core/graph/state_graph/utils/__init__.py:8` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: c857ce99
- `packages/haive-core/src/haive/core/schema/compatibility/field_mapping.py:266` - error: Need type annotation for "mapped_sources" (hint: "mapped_sources: set[<type>] = ...") [var-a
  - ID: e42ff05b
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:851` - error: Need type annotation for "hotspots" (hint: "hotspots: list[<type>] = ...") [var-annotated]
  - ID: 968b8620
- `packages/haive-core/src/haive/core/utils/haive_discovery/discovery_engine.py:37` - error: Need type annotation for "failed_modules" (hint: "failed_modules: list[<type>] = ...") [var-
  - ID: 17061cf3
- `packages/haive-core/src/haive/core/utils/haive_discovery/discovery_engine.py:38` - error: Need type annotation for "discovered_components" (hint: "discovered_components: list[<type>]
  - ID: 195a409b
- `packages/haive-core/src/haive/core/utils/haive_discovery/discovery_engine.py:104` - error: Need type annotation for "components" (hint: "components: list[<type>] = ...") [var-annotate
  - ID: 142043c2
- `packages/haive-core/src/haive/core/schema/composer/engine/engine_detector.py:26` - error: Need type annotation for "base_class_fields" (hint: "base_class_fields: set[<type>] = ...")
  - ID: 9fa653b0
- `packages/haive-core/src/haive/core/graph/state_graph/components/edge_manager.py:300` - error: Need type annotation for "visited" (hint: "visited: set[<type>] = ...") [var-annotated]
  - ID: f15e5140
- ... and 26 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/registry/registries/__init__.py:17` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: 5d11a422
- `packages/haive-dataflow/src/haive/dataflow/registry/providers/__init__.py:17` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: ceab4e27
- `packages/haive-dataflow/src/haive/dataflow/registries/__init__.py:17` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: d9353557
- `packages/haive-dataflow/src/haive/dataflow/providers/__init__.py:17` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: b5ac026d
- `packages/haive-dataflow/src/haive/dataflow/persistence/__init__.py:17` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: 54f09057
- `packages/haive-dataflow/src/haive/dataflow/llms/__init__.py:17` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: 942726a6
- `packages/haive-dataflow/src/haive/dataflow/internal_websockets/__init__.py:17` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: e68ed646
- `packages/haive-dataflow/src/haive/dataflow/fetchers/__init__.py:16` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: d18c8d88
- `packages/haive-dataflow/src/haive/dataflow/db/__init__.py:17` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: 45fbdbf5
- `packages/haive-dataflow/src/haive/dataflow/conversations/__init__.py:17` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: 5884c225
- ... and 10 more

### haive-games

- `packages/haive-games/src/haive/games/utils/__init__.py:12` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: 574ad4fa
- `packages/haive-games/src/haive/games/tic_tac_toe/__init__.py:3` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: dd2b93b9
- `packages/haive-games/src/haive/games/single_player/wordle/__init__.py:3` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: 5885c2c4
- `packages/haive-games/src/haive/games/single_player/twenty_fourty_eight/game/__init__.py:3` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: ac4df4d9
- `packages/haive-games/src/haive/games/single_player/twenty_fourty_eight/__init__.py:3` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: 81fb9f28
- `packages/haive-games/src/haive/games/single_player/sudoku/game/__init__.py:3` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: 5dd57f69
- `packages/haive-games/src/haive/games/single_player/rubiks/__init__.py:3` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: 57f056b7
- `packages/haive-games/src/haive/games/single_player/mine_sweeper/__init__.py:3` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: 9f867d07
- `packages/haive-games/src/haive/games/single_player/logic_grid/game/__init__.py:3` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: 4f7eb4f3
- `packages/haive-games/src/haive/games/single_player/flow_free/__init__.py:3` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: c3cb4c9f
- ... and 56 more

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/tools/server_tester.py:359` - error: Need type annotation for "capabilities" (hint: "capabilities: set[<type>] = ...") [var-annot
  - ID: 9802a30b
- `packages/haive-mcp/src/haive/mcp/enhance_mcp_data.py:318` - error: Need type annotation for "current_content" (hint: "current_content: list[<type>] = ...") [va
  - ID: 5dc2ea02
- `packages/haive-mcp/src/haive/mcp/downloader/discovery.py:547` - error: Need type annotation for "tags" (hint: "tags: set[<type>] = ...") [var-annotated]
  - ID: 86275f59
- `packages/haive-mcp/src/haive/mcp/mcp_simple_rag_agent.py:42` - error: Need type annotation for "documents" (hint: "documents: list[<type>] = ...") [var-annotated]
  - ID: 00714694
- `packages/haive-mcp/src/haive/mcp/documentation/doc_loader.py:389` - error: Need type annotation for "current_example" (hint: "current_example: list[<type>] = ...") [va
  - ID: fcacfd23
- `packages/haive-mcp/src/haive/mcp/simple_faiss_retriever.py:33` - error: Need type annotation for "documents" (hint: "documents: list[<type>] = ...") [var-annotated]
  - ID: b96c6be8
- `packages/haive-mcp/src/haive/mcp/mcp_simple_tool_agent.py:39` - error: Need type annotation for "documents" (hint: "documents: list[<type>] = ...") [var-annotated]
  - ID: b05d267b
- `packages/haive-mcp/src/haive/mcp/enhanced_parent_self_query_retriever.py:48` - error: Need type annotation for "metadata_fields" (hint: "metadata_fields: list[<type>] = ...") [va
  - ID: 5d75fa85

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:371` - error: Need type annotation for "routes" (hint: "routes: list[<type>] = ...") [var-annotated]
  - ID: 9bfe49f9

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/__init__.py:13` - error: Need type annotation for "**all**" (hint: "**all**: list[<type>] = ...") [var-annotated]
  - ID: 6e52c490
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/background_process_manager.py:249` - error: Need type annotation for "stdout" (hint: "stdout: list[<type>] = ...") [var-annotated]
  - ID: 1e9e7e8f
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/background_process_manager.py:249` - error: Need type annotation for "stdout" (hint: "stdout: list[<type>] = ...") [var-annotated]
  - ID: 1e9e7e8f

## mypy:<type>, <type> (207 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/task_analysis/tree/models.py:101` - error: Need type annotation for "dep_map" (hint: "dep_map: dict[<type>, <type>] = ...") [var-annota
  - ID: c5760053
- `packages/haive-agents/src/haive/agents/self_healing_code/agent.py:194` - error: Need type annotation for "namespace" (hint: "namespace: dict[<type>, <type>] = ...") [var-an
  - ID: 42174177
- `packages/haive-agents/src/haive/agents/rag/multi_agent_rag/compatibility.py:81` - error: Need type annotation for "\_test_cache" (hint: "\_test_cache: dict[<type>, <type>] = ...") [va
  - ID: c57d9d13
- `packages/haive-agents/src/haive/agents/supervisor/simple_test_runner.py:25` - error: Need type annotation for "tool_routes" (hint: "tool_routes: dict[<type>, <type>] = ...") [va
  - ID: 66110325
- `packages/haive-agents/src/haive/agents/supervisor/simple_test_runner.py:104` - error: Need type annotation for "agents" (hint: "agents: dict[<type>, <type>] = ...") [var-annotate
  - ID: b7f3a90f
- `packages/haive-agents/src/haive/agents/supervisor/simple_test_runner.py:105` - error: Need type annotation for "agent_configs" (hint: "agent_configs: dict[<type>, <type>] = ...")
  - ID: 496eda8a
- `packages/haive-agents/src/haive/agents/supervisor/simple_test_runner.py:107` - error: Need type annotation for "tool_to_agent_mapping" (hint: "tool_to_agent_mapping: dict[<type>,
  - ID: dea00ec9
- `packages/haive-agents/src/haive/agents/supervisor/archive/simple_test_runner.py:25` - error: Need type annotation for "tool_routes" (hint: "tool_routes: dict[<type>, <type>] = ...") [va
  - ID: 5ec30536
- `packages/haive-agents/src/haive/agents/supervisor/archive/simple_test_runner.py:104` - error: Need type annotation for "agents" (hint: "agents: dict[<type>, <type>] = ...") [var-annotate
  - ID: 007fdabd
- `packages/haive-agents/src/haive/agents/supervisor/archive/simple_test_runner.py:105` - error: Need type annotation for "agent_configs" (hint: "agent_configs: dict[<type>, <type>] = ...")
  - ID: a89245dc
- ... and 42 more

### haive-core

- `packages/haive-core/src/haive/core/graph/node/composer/update_functions.py:107` - error: Need type annotation for "updates" (hint: "updates: dict[<type>, <type>] = ...") [var-annota
  - ID: e5526caa
- `packages/haive-core/src/haive/core/utils/inspection.py:85` - error: Need type annotation for "present" (hint: "present: dict[<type>, <type>] = ...") [var-annota
  - ID: 068d44c6
- `packages/haive-core/src/haive/core/utils/inspection.py:86` - error: Need type annotation for "missing" (hint: "missing: dict[<type>, <type>] = ...") [var-annota
  - ID: dc29dfc4
- `packages/haive-core/src/haive/core/utils/haive_discovery/documentation_writer.py:30` - error: Need type annotation for "saved_files" (hint: "saved_files: dict[<type>, <type>] = ...") [va
  - ID: bf08962a
- `packages/haive-core/src/haive/core/utils/haive_discovery/documentation_writer.py:33` - error: Need type annotation for "by_type" (hint: "by_type: dict[<type>, <type>] = ...") [var-annota
  - ID: f2d1e369
- `packages/haive-core/src/haive/core/utils/haive_discovery/documentation_writer.py:162` - error: Need type annotation for "tools_by_source" (hint: "tools_by_source: dict[<type>, <type>] = ..
  - ID: f033a7e2
- `packages/haive-core/src/haive/core/utils/haive_discovery/documentation_writer.py:228` - error: Need type annotation for "engines_by_type" (hint: "engines_by_type: dict[<type>, <type>] = ..
  - ID: af0d99a9
- `packages/haive-core/src/haive/core/registry/memory.py:19` - error: Need type annotation for "engine_ids" (hint: "engine_ids: dict[<type>, <type>] = ...") [var-
  - ID: ee2cd941
- `packages/haive-core/src/haive/core/registry/manager.py:14` - error: Need type annotation for "\_registry_types" (hint: "\_registry_types: dict[<type>, <type>] = ..
  - ID: bb634f32
- `packages/haive-core/src/haive/core/registry/factory.py:13` - error: Need type annotation for "registry_types" (hint: "registry_types: dict[<type>, <type>] = ..."
  - ID: 5d07445b
- ... and 67 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/registry/registries/model_registry.py:1337` - error: Need type annotation for "env_matches" (hint: "env_matches: dict[<type>, <type>] = ...") [va
  - ID: 8bb2da0f
- `packages/haive-dataflow/src/haive/dataflow/registries/model_registry.py:1337` - error: Need type annotation for "env_matches" (hint: "env_matches: dict[<type>, <type>] = ...") [va
  - ID: 0cb63c08
- `packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:327` - error: Need type annotation for "patterns_by_type" (hint: "patterns_by_type: dict[<type>, <type>] =
  - ID: db2e4b75
- `packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:539` - error: Need type annotation for "patterns_by_type" (hint: "patterns_by_type: dict[<type>, <type>] =
  - ID: 3c53580f
- `packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:563` - error: Need type annotation for "patterns_by_type" (hint: "patterns_by_type: dict[<type>, <type>] =
  - ID: 66952a4a
- `packages/haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:579` - error: Need type annotation for "entities_by_type" (hint: "entities_by_type: dict[<type>, <type>] =
  - ID: 33666111
- `packages/haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:767` - error: Need type annotation for "entities_by_type" (hint: "entities_by_type: dict[<type>, <type>] =
  - ID: ece76a47
- `packages/haive-dataflow/src/haive/dataflow/bin/registry_cli.py:581` - error: Need type annotation for "entities_by_type" (hint: "entities_by_type: dict[<type>, <type>] =
  - ID: e2bc8938
- `packages/haive-dataflow/src/haive/dataflow/bin/registry_cli.py:769` - error: Need type annotation for "entities_by_type" (hint: "entities_by_type: dict[<type>, <type>] =
  - ID: 62b68aa7
- `packages/haive-dataflow/src/haive/dataflow/serialization.py:25` - error: Need type annotation for "\_serializers" (hint: "\_serializers: dict[<type>, <type>] = ...") [
  - ID: 42ade8d3
- ... and 25 more

### haive-games

- `packages/haive-games/src/haive/games/cards/standard/poker/scoring.py:165` - error: Need type annotation for "by_suit" (hint: "by_suit: dict[<type>, <type>] = ...") [var-annota
  - ID: f8997879
- `packages/haive-games/src/haive/games/cards/standard/poker/scoring.py:273` - error: Need type annotation for "by_suit" (hint: "by_suit: dict[<type>, <type>] = ...") [var-annota
  - ID: 51f177bd
- `packages/haive-games/src/haive/games/poker/debug.py:116` - error: Need type annotation for "action_counts" (hint: "action_counts: dict[<type>, <type>] = ...")
  - ID: d91e57f6
- `packages/haive-games/src/haive/games/monopoly/standalone_demo.py:764` - error: Need type annotation for "property_owners" (hint: "property_owners: dict[<type>, <type>] = ..
  - ID: b786c26f
- `packages/haive-games/src/haive/games/monopoly/main_agent.py:142` - error: Need type annotation for "event_counts" (hint: "event_counts: dict[<type>, <type>] = ...") [
  - ID: 34f4a143
- `packages/haive-games/src/haive/games/mastermind/state_manager.py:157` - error: Need type annotation for "secret_counts" (hint: "secret_counts: dict[<type>, <type>] = ...")
  - ID: 6ed619b8
- `packages/haive-games/src/haive/games/mastermind/state_manager.py:158` - error: Need type annotation for "guess_counts" (hint: "guess_counts: dict[<type>, <type>] = ...") [
  - ID: a76bfc34
- `packages/haive-games/src/haive/games/hold_em/utils.py:107` - error: Need type annotation for "rank_counts" (hint: "rank_counts: dict[<type>, <type>] = ...") [va
  - ID: 3354ac57
- `packages/haive-games/src/haive/games/hold_em/utils.py:108` - error: Need type annotation for "suit_counts" (hint: "suit_counts: dict[<type>, <type>] = ...") [va
  - ID: 2f99142e
- `packages/haive-games/src/haive/games/hold_em/utils.py:322` - error: Need type annotation for "suit_counts" (hint: "suit_counts: dict[<type>, <type>] = ...") [va
  - ID: ad135781
- ... and 19 more

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/tools/server_selector.py:100` - error: Need type annotation for "by_prefix" (hint: "by_prefix: dict[<type>, <type>] = ...") [var-an
  - ID: c96cf962
- `packages/haive-mcp/src/haive/mcp/tools/server_selector.py:101` - error: Need type annotation for "by_category" (hint: "by_category: dict[<type>, <type>] = ...") [va
  - ID: df64029c
- `packages/haive-mcp/src/haive/mcp/tools/server_selector.py:102` - error: Need type annotation for "by_capability" (hint: "by_capability: dict[<type>, <type>] = ...")
  - ID: e03de9f7
- `packages/haive-mcp/src/haive/mcp/tools/server_selector.py:308` - error: Need type annotation for "category_scores" (hint: "category_scores: dict[<type>, <type>] = ..
  - ID: f58338c6
- `packages/haive-mcp/src/haive/mcp/tools/server_selector.py:643` - error: Need type annotation for "categories" (hint: "categories: dict[<type>, <type>] = ...") [var-
  - ID: 01f8b69b
- `packages/haive-mcp/src/haive/mcp/tools/ai_assistant.py:278` - error: Need type annotation for "cached_configs" (hint: "cached_configs: dict[<type>, <type>] = ..."
  - ID: 26444240
- `packages/haive-mcp/src/haive/mcp/tools/server_tester.py:479` - error: Need type annotation for "by_server" (hint: "by_server: dict[<type>, <type>] = ...") [var-an
  - ID: 2d4a59e1
- `packages/haive-mcp/src/haive/mcp/integrated_mcp_system.py:592` - error: Need type annotation for "categories" (hint: "categories: dict[<type>, <type>] = ...") [var-
  - ID: 416c57eb
- `packages/haive-mcp/src/haive/mcp/integrated_launcher.py:138` - error: Need type annotation for "categories" (hint: "categories: dict[<type>, <type>] = ...") [var-
  - ID: ffaab99c
- `packages/haive-mcp/src/haive/mcp/servers/dataflow_mcp_server.py:300` - error: Need type annotation for "grouped" (hint: "grouped: dict[<type>, <type>] = ...") [var-annota
  - ID: 041011de
- ... and 1 more

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/ai_insight/tools.py:168` - error: Need type annotation for "grouped" (hint: "grouped: dict[<type>, <type>] = ...") [var-annota
  - ID: 9900c1b3
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:434` - error: Need type annotation for "speaker_counts" (hint: "speaker_counts: dict[<type>, <type>] = ..."
  - ID: 0fdb9cdf
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:294` - error: Need type annotation for "sources" (hint: "sources: dict[<type>, <type>] = ...") [var-annota
  - ID: eca0c349

## mypy:<typing special form>, Any (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/aug_llm/config.py:814` - error: Incompatible types in assignment (expression has type "tuple[<typing special form>, Any]", ta
  - ID: 5ed424a0

## mypy:<typing special form>, FieldMetadata | None (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/schema/field_utils.py:766` - error: Incompatible return value type (got "tuple[<typing special form>, FieldMetadata | None]", exp
  - ID: e66d336d

## mypy:<typing special form>, None (5 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/aug_llm/config.py:811` - error: Incompatible types in assignment (expression has type "tuple[<typing special form>, None]", t
  - ID: 9e705817
- `packages/haive-core/src/haive/core/engine/vectorstore/vectorstore.py:279` - error: Dict entry 1 has incompatible type "str": "tuple[<typing special form>, None]"; expected "str
  - ID: ea7f6a60
- `packages/haive-core/src/haive/core/engine/vectorstore/vectorstore.py:280` - error: Dict entry 2 has incompatible type "str": "tuple[<typing special form>, None]"; expected "str
  - ID: 2fa96594
- `packages/haive-core/src/haive/core/engine/vectorstore/vectorstore.py:281` - error: Dict entry 3 has incompatible type "str": "tuple[<typing special form>, None]"; expected "str
  - ID: c5456223
- `packages/haive-core/src/haive/core/engine/vectorstore/vectorstore.py:282` - error: Dict entry 4 has incompatible type "str": "tuple[<typing special form>, None]"; expected "str
  - ID: 256328bb

## mypy:AIMessage (12 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/simple/state.v2.py:63` - error: Argument 2 to "add_messages" has incompatible type "list[AIMessage]"; expected "list[BaseMess
  - ID: 6eac1873
- `packages/haive-agents/src/haive/agents/simple/state.py:50` - error: Argument 2 to "add_messages" has incompatible type "list[AIMessage]"; expected "list[BaseMess
  - ID: ac1be6a7

### haive-core

- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:281` - error: Incompatible return value type (got "list[AIMessage]", expected "list[BaseMessage]") [return
  - ID: 7a11bb19
- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:388` - error: Incompatible return value type (got "list[AIMessage]", expected "list[BaseMessage]") [return
  - ID: 4a80c790
- `packages/haive-core/src/haive/core/graph/node/message_transformation.py:210` - error: Incompatible return value type (got "list[AIMessage]", expected "list[BaseMessage]") [return
  - ID: 933e02e2
- `packages/haive-core/src/haive/core/graph/node/message_transformation.py:317` - error: Incompatible return value type (got "list[AIMessage]", expected "list[BaseMessage]") [return
  - ID: 88b91cb0
- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:477` - error: Argument 1 to "extend" of "list" has incompatible type "list[AIMessage]"; expected "Iterable[
  - ID: 752011f2

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/startup/agent.py:315` - error: Incompatible types in assignment (expression has type "str", target has type "list[AIMessage]
  - ID: 44ea9f0c
- `packages/haive-prebuilt/src/haive/prebuilt/startup/agent.py:322` - error: Incompatible types in assignment (expression has type "str", target has type "list[AIMessage]
  - ID: 1bfd1fac
- `packages/haive-prebuilt/src/haive/prebuilt/startup/agent.py:324` - error: Incompatible types in assignment (expression has type "str", target has type "list[AIMessage]
  - ID: 82c75030
- `packages/haive-prebuilt/src/haive/prebuilt/startup/agent.py:333` - error: Incompatible types in assignment (expression has type "str", target has type "list[AIMessage]
  - ID: 6f1d23c7
- `packages/haive-prebuilt/src/haive/prebuilt/startup/agent.py:337` - error: Incompatible types in assignment (expression has type "str", target has type "list[AIMessage]
  - ID: 5fd79334

## mypy:AIMessage | HumanMessage | ChatMessage | SystemMessage | FunctionMessage | <7 more items> (14 errors)

### haive-core

- `packages/haive-core/src/haive/core/schema/agent_schema_composer.py:88` - error: Returning Any from function declared to return "list[AIMessage | HumanMessage | ChatMessage |
  - ID: fcef2faa
- `packages/haive-core/src/haive/core/common/mixins/prompt_template_mixin.py:318` - error: Returning Any from function declared to return "str | list[AIMessage | HumanMessage | ChatMes
  - ID: 715ca8b5
- `packages/haive-core/src/haive/core/schema/prebuilt/messages_state.py:238` - error: Returning Any from function declared to return "list[AIMessage | HumanMessage | ChatMessage |
  - ID: f7cf6e91
- `packages/haive-core/src/haive/core/schema/prebuilt/messages_state.py:239` - error: Returning Any from function declared to return "list[AIMessage | HumanMessage | ChatMessage |
  - ID: 42a3219a
- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:155` - note: Perhaps you need a type annotation for "converted"? Suggestion: "list[AIMessage | HumanMessage
  - ID: 41150ae1
- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:318` - error: Return type "Iterator[AIMessage | HumanMessage | ChatMessage | SystemMessage | FunctionMessag
  - ID: b09728db
- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:370` - note: def copy(self) -> list[AIMessage | HumanMessage | ChatMessage | SystemMessage | Funct
  - ID: fc2fcffd
- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:479` - note: Perhaps you need a type annotation for "messages"? Suggestion: "list[AIMessage | HumanMessage
  - ID: bfa08be1
- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:827` - error: Returning Any from function declared to return "list[AIMessage | HumanMessage | ChatMessage |
  - ID: 2cbb7a4c
- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:828` - error: Returning Any from function declared to return "list[AIMessage | HumanMessage | ChatMessage |
  - ID: 20eebd60
- ... and 4 more

## mypy:AIMessage | HumanMessage | ChatMessage | SystemMessage | FunctionMessage | <7 more items> | str (2 errors)

### haive-core

- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:833` - error: Argument "root" to "MessageList" has incompatible type "list[AIMessage | HumanMessage | ChatM
  - ID: 93228ae6
- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:1093` - error: Argument "messages" to "MessagesState" has incompatible type "list[AIMessage | HumanMessage |
  - ID: ac61b133

## mypy:AIMessage | HumanMessage | SystemMessage | ToolMessage (1 errors)

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:81` - error: Returning Any from function declared to return "list[AIMessage | HumanMessage | SystemMessage
  - ID: 35d92a01

## mypy:Agent[Any (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/agent/agent.py:81` - error: "type[Agent[Any]]" has no attribute "config_class" [attr-defined]
  - ID: 09c0d9ae

## mypy:AgenticRAGCoordinator (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_reorganized/__init__.py:79` - error: Incompatible types in assignment (expression has type "None", variable has type "type[Agentic
  - ID: c8d3b4e5

## mypy:Any (241 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/planning/proper_plan_execute.py:208` - error: Incompatible types in assignment (expression has type "None", target has type "list[Any]") [
  - ID: d2878ca8
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/models.py:126` - note: def **add**(self, list[Any], /) -> list[Any]
  - ID: 8b63d4e1
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/models.py:126` - note: def **add**(self, list[Any], /) -> list[Any]
  - ID: 8b63d4e1
- `packages/haive-agents/src/haive/agents/planning/base/models.py:368` - error: Incompatible return value type (got "BasePlan[Any] | BaseStep | list[BaseStep] | Callable[...
  - ID: fd18c5a4
- `packages/haive-agents/src/haive/agents/planning/base/models.py:370` - error: Argument 1 of "append" is incompatible with supertype "builtins.list"; supertype defines the
  - ID: 4e7dbf63
- `packages/haive-agents/src/haive/agents/planning/base/models.py:370` - error: Argument 1 of "append" is incompatible with supertype "builtins.list"; supertype defines the
  - ID: 4e7dbf63
- `packages/haive-agents/src/haive/agents/planning/base/models.py:391` - error: Argument 2 of "insert" is incompatible with supertype "builtins.list"; supertype defines the
  - ID: f53bf81d
- `packages/haive-agents/src/haive/agents/planning/base/models.py:391` - error: Argument 2 of "insert" is incompatible with supertype "builtins.list"; supertype defines the
  - ID: f53bf81d
- `packages/haive-agents/src/haive/agents/planning/base/models.py:406` - error: Argument 1 of "remove" is incompatible with supertype "builtins.list"; supertype defines the
  - ID: 18a98be4
- `packages/haive-agents/src/haive/agents/planning/base/models.py:406` - error: Argument 1 of "remove" is incompatible with supertype "builtins.list"; supertype defines the
  - ID: 18a98be4
- ... and 85 more

### haive-core

- `packages/haive-core/src/haive/core/utils/debugkit/debugging.py:106` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: 0df610da
- `packages/haive-core/src/haive/core/utils/haive_discovery/utils.py:60` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: a3a85135
- `packages/haive-core/src/haive/core/utils/haive_discovery/utils.py:73` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: 6ddd6be1
- `packages/haive-core/src/haive/core/utils/haive_discovery/utils.py:82` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: 0368e783
- `packages/haive-core/src/haive/core/utils/haive_discovery/utils.py:91` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: fb783070
- `packages/haive-core/src/haive/core/utils/haive_discovery/utils.py:100` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: c3496db2
- `packages/haive-core/src/haive/core/utils/haive_discovery/utils.py:109` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: 0f448752
- `packages/haive-core/src/haive/core/utils/haive_discovery/haive_discovery.py:35` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: c4ffa905
- `packages/haive-core/src/haive/core/utils/haive_discovery/haive_discovery.py:52` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: 8fb59bce
- `packages/haive-core/src/haive/core/utils/haive_discovery/haive_discovery.py:187` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: aaafaf62
- ... and 85 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/mcp/client.py:193` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: 50bd4476
- `packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:122` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: 887ca2c5
- `packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_enhanced.py:148` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: 390a3e0c
- `packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_enhanced.py:162` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: 93506749
- `packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes.py:469` - error: Item "None" of "type[Any] | None" has no attribute "args_schema" [union-attr]
  - ID: f0e05a6c
- `packages/haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes_enhanced.py:166` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: 314db5d7
- `packages/haive-dataflow/src/haive/dataflow/api/middleware/supabase_logging.py:210` - error: Incompatible types in assignment (expression has type "list[Any]", target has type "str") [a
  - ID: a997bea9
- `packages/haive-dataflow/src/haive/dataflow/api/registry.py:270` - error: Returning Any from function declared to return "type[Any] | None" [no-any-return]
  - ID: 64f9e174

### haive-games

- `packages/haive-games/src/haive/games/checkers/example.py:496` - error: Incompatible return value type (got "object", expected "SupportsDunderLT[Any] | SupportsDunde
  - ID: 0595adbf
- `packages/haive-games/src/haive/games/chess/dynamic_config.py:137` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: 174721f4
- `packages/haive-games/src/haive/games/chess/dynamic_config.py:173` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: 2962f107
- `packages/haive-games/src/haive/games/chess/config.py:79` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: be1d2df8
- `packages/haive-games/src/haive/games/chess/config.py:89` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: 5a9555e8
- `packages/haive-games/src/haive/games/monopoly/state.py:563` - error: Unsupported target for indexed assignment ("Collection[Any]") [index]
  - ID: 2f14729a
- `packages/haive-games/src/haive/games/monopoly/state.py:569` - error: "Collection[Any]" has no attribute "append" [attr-defined]
  - ID: d3c8d6e5
- `packages/haive-games/src/haive/games/monopoly/state.py:579` - error: "Collection[Any]" has no attribute "append" [attr-defined]
  - ID: 5565eee5
- `packages/haive-games/src/haive/games/connect4/agent.py:165` - error: Returning Any from function declared to return "Command[Any]" [no-any-return]
  - ID: 2122a1b1
- `packages/haive-games/src/haive/games/connect4/agent.py:173` - error: Returning Any from function declared to return "Command[Any]" [no-any-return]
  - ID: 20e402bc
- ... and 3 more

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/fastmcp_runner.py:242` - error: Incompatible types in assignment (expression has type "Task[Any]", variable has type "None")
  - ID: 6da23de7
- `packages/haive-mcp/src/haive/mcp/tools/server_tester.py:126` - error: Incompatible types in assignment (expression has type "Task[Any]", variable has type "None")
  - ID: d4eb2d26
- `packages/haive-mcp/src/haive/mcp/downloader/core.py:440` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: 27cab0c6
- `packages/haive-mcp/src/haive/mcp/agents/transferable_mcp_agent.py:402` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: aaa9b3d8
- `packages/haive-mcp/src/haive/mcp/agents/transferable_mcp_agent.py:454` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: 67ba8529
- `packages/haive-mcp/src/haive/mcp/agents/documentation_agent.py:504` - error: Unsupported target for indexed assignment ("list[Any] | dict[Any, Any] | str | None") [index
  - ID: 819900e9
- `packages/haive-mcp/src/haive/mcp/agents/documentation_agent.py:519` - error: Item "list[Any]" of "list[Any] | dict[Any, Any] | str | None" has no attribute "values" [uni
  - ID: 2f922273
- `packages/haive-mcp/src/haive/mcp/agents/documentation_agent.py:519` - error: Item "list[Any]" of "list[Any] | dict[Any, Any] | str | None" has no attribute "values" [uni
  - ID: 2f922273
- `packages/haive-mcp/src/haive/mcp/agents/documentation_agent.py:519` - error: Item "list[Any]" of "list[Any] | dict[Any, Any] | str | None" has no attribute "values" [uni
  - ID: 2f922273
- `packages/haive-mcp/src/haive/mcp/agents/documentation_agent.py:524` - error: Item "str" of "list[Any] | dict[Any, Any] | str | None" has no attribute "extend" [union-att
  - ID: 17772606
- ... and 12 more

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:438` - error: Incompatible return value type (got "float | Any | None", expected "SupportsDunderLT[Any] | S
  - ID: d8943dca
- `packages/haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:374` - error: "list[Any]" has no attribute "values" [attr-defined]
  - ID: 43879e0e
- `packages/haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:385` - error: Incompatible return value type (got "list[Any]", expected "str") [return-value]
  - ID: 644a8547

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/report_of_the_week_tool.py:58` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: edc3aed7
- `packages/haive-tools/src/haive/tools/tools/report_of_the_week_tool.py:109` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: c6c01ac1
- `packages/haive-tools/src/haive/tools/tools/report_of_the_week_tool.py:157` - error: Returning Any from function declared to return "list[Any]" [no-any-return]
  - ID: a1519d1d
- `packages/haive-tools/src/haive/tools/tools/toolkits/amadues_toolkit.py:91` - error: Returning Any from function declared to return "BaseLanguageModel[Any] | None" [no-any-retur
  - ID: 62868674
- `packages/haive-tools/src/haive/tools/tools/toolkits/nla_toolkit.py:79` - error: Returning Any from function declared to return "BaseLanguageModel[Any] | None" [no-any-retur
  - ID: 2aca6205

## mypy:Any | BaseException (2 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/multi/enhanced_parallel_agent.py:256` - error: Argument 1 to "\_aggregate_results" of "ParallelAgent" has incompatible type "list[Any | BaseE
  - ID: c3bd4b55
- `packages/haive-agents/src/haive/agents/multi/archive/enhanced_parallel_agent.py:256` - error: Argument 1 to "\_aggregate_results" of "ParallelAgent" has incompatible type "list[Any | BaseE
  - ID: aed645b1

## mypy:Any | None (1 errors)

### haive-games

- `packages/haive-games/src/haive/games/battleship/utils.py:198` - error: Argument 1 to "set" has incompatible type "list[Any | None]"; expected "Iterable[str]" [arg-
  - ID: 03831e82

## mypy:Any | None, Any (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/planning/llm_compiler/output_parser.py:54` - error: Incompatible return value type (got "dict[Any | None, Any]", expected "list[Any]") [return-v
  - ID: 59d53863

## mypy:Any, ... (8 errors)

### haive-core

- `packages/haive-core/src/haive/core/utils/debugkit/analysis/types.py:48` - note: def get_args(tp: Any) -> tuple[Any, ...]
  - ID: 39477347
- `packages/haive-core/src/haive/core/utils/haive_collections.py:48` - error: Subclass of "tuple[Any, ...]" and "dict[Any, Any]" cannot exist: would have incompatible meth
  - ID: ac1e17c8
- `packages/haive-core/src/haive/core/common/structures/named_dict.py:40` - error: Subclass of "tuple[Any, ...]" and "dict[Any, Any]" cannot exist: would have incompatible meth
  - ID: 16e632a3
- `packages/haive-core/src/haive/core/persistence/serializers.py:159` - note: def \_encode_constructor_args(self, constructor: str, method: str, args: tuple[Any, ..
  - ID: 9aea2a41
- `packages/haive-core/src/haive/core/schema/state_schema.py:1213` - error: No overload variant of "**add**" of "list" matches argument type "tuple[Any, ...]" [operator
  - ID: f374ffe4
- `packages/haive-core/src/haive/core/schema/state_schema.py:1213` - error: No overload variant of "**add**" of "list" matches argument type "tuple[Any, ...]" [operator
  - ID: f374ffe4
- `packages/haive-core/src/haive/core/schema/field_utils.py:955` - error: No overload variant of "**add**" of "list" matches argument type "tuple[Any, ...]" [operator
  - ID: d51d8e9a
- `packages/haive-core/src/haive/core/schema/field_utils.py:955` - error: No overload variant of "**add**" of "list" matches argument type "tuple[Any, ...]" [operator
  - ID: d51d8e9a

## mypy:Any, Any (209 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/react_class/react_agent2/tool_utils.py:267` - error: Incompatible types in assignment (expression has type "dict[Any, Any]", variable has type "To
  - ID: 2249c562
- `packages/haive-agents/src/haive/agents/react_class/react_agent2/tool_utils.py:272` - error: Argument 1 to "append" of "list" has incompatible type "ToolMessage | dict[Any, Any]"; expect
  - ID: 6ba98bb5
- `packages/haive-agents/src/haive/agents/react_class/react_agent2/debug.py:147` - error: Incompatible types in assignment (expression has type "dict[Any, Any]", variable has type "To
  - ID: e68d3c57
- `packages/haive-agents/src/haive/agents/planning/llm_compiler/output_parser.py:129` - error: Incompatible types in "yield from" (actual type "dict[Any, Any]", expected type "Task") [mis
  - ID: 566157a8
- `packages/haive-agents/src/haive/agents/planning/llm_compiler/tools/math_tools.py:121` - error: Item "dict[Any, Any]" of "dict[Any, Any] | Any" has no attribute "code" [union-attr]
  - ID: 4c94482b
- `packages/haive-agents/src/haive/agents/memory_v2/standalone_rag_memory.py:670` - note: def tool(name_or_callable: str, runnable: Runnable[Any, Any], \*, description: str | None =
  - ID: 63a9e85b
- `packages/haive-agents/src/haive/agents/memory_v2/multi_memory_coordinator.py:636` - error: Item "int" of "int | dict[Any, Any] | list[Any] | str | None" has no attribute "append" [uni
  - ID: 81ac785d
- `packages/haive-agents/src/haive/agents/memory_v2/multi_memory_coordinator.py:636` - error: Item "int" of "int | dict[Any, Any] | list[Any] | str | None" has no attribute "append" [uni
  - ID: 81ac785d
- `packages/haive-agents/src/haive/agents/memory_v2/multi_memory_coordinator.py:636` - error: Item "int" of "int | dict[Any, Any] | list[Any] | str | None" has no attribute "append" [uni
  - ID: 81ac785d
- `packages/haive-agents/src/haive/agents/memory_v2/multi_memory_coordinator.py:636` - error: Item "int" of "int | dict[Any, Any] | list[Any] | str | None" has no attribute "append" [uni
  - ID: 81ac785d
- ... and 48 more

### haive-core

- `packages/haive-core/src/haive/core/utils/debugkit/debugging.py:83` - error: Returning Any from function declared to return "dict[Any, Any]" [no-any-return]
  - ID: 6c3220b1
- `packages/haive-core/src/haive/core/utils/debugkit/debugging.py:87` - error: Returning Any from function declared to return "dict[Any, Any]" [no-any-return]
  - ID: c6a1c47a
- `packages/haive-core/src/haive/core/utils/debugkit/debugging.py:114` - error: Returning Any from function declared to return "dict[Any, Any]" [no-any-return]
  - ID: f8e7a904
- `packages/haive-core/src/haive/core/graph/node/composer/update_functions.py:61` - error: Incompatible types in assignment (expression has type "dict[Any, Any]", variable has type "li
  - ID: b5349755
- `packages/haive-core/src/haive/core/engine/embedding/providers/__init__.py:164` - error: Returning Any from function declared to return "dict[Any, Any]" [no-any-return]
  - ID: c842e437
- `packages/haive-core/src/haive/core/engine/embedding/providers/__init__.py:165` - error: Returning Any from function declared to return "dict[Any, Any]" [no-any-return]
  - ID: fedc907b
- `packages/haive-core/src/haive/core/schema/compatibility/field_mapping.py:135` - error: Incompatible types in assignment (expression has type "dict[Any, Any] | None", variable has t
  - ID: 88317a41
- `packages/haive-core/src/haive/core/schema/prebuilt/messages/token_usage.py:118` - error: Incompatible types in assignment (expression has type "dict[Any, Any]", variable has type "Us
  - ID: 864f3f69
- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_with_token_usage.py:68` - error: Incompatible types in assignment (expression has type "BaseMessage", variable has type "AIMes
  - ID: d66ea754
- `packages/haive-core/src/haive/core/models/llm/providers/openai.py:178` - error: Returning Any from function declared to return "dict[Any, Any]" [no-any-return]
  - ID: ae2de8c7
- ... and 81 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/mcp/client.py:335` - error: Item "dict[Any, Any]" of "Any | dict[Any, Any]" has no attribute "schema" [union-attr]
  - ID: f4660eae
- `packages/haive-dataflow/src/haive/dataflow/mcp/client.py:394` - error: Item "dict[Any, Any]" of "Any | dict[Any, Any]" has no attribute "schema" [union-attr]
  - ID: 1999c9ae

### haive-games

- `packages/haive-games/src/haive/games/cards/standard/blackjack/factory.py:87` - error: Returning Any from function declared to return "dict[Any, Any]" [no-any-return]
  - ID: 400a4f72
- `packages/haive-games/src/haive/games/monopoly/standalone_demo.py:308` - error: Incompatible return value type (got "object", expected "dict[Any, Any] | None") [return-valu
  - ID: b04221ec
- `packages/haive-games/src/haive/games/mafia/agent.py:594` - error: Subclass of "str" and "dict[Any, Any]" cannot exist: would have incompatible method signature
  - ID: 658137fc
- `packages/haive-games/src/haive/games/core/game/core_position.py:198` - error: "dict[Any, Any]" has no attribute "data" [attr-defined]
  - ID: b0c6acc5
- `packages/haive-games/src/haive/games/core/game/core_position.py:199` - error: "dict[Any, Any]" has no attribute "data" [attr-defined]
  - ID: 9a60e910
- `packages/haive-games/src/haive/games/core/components/cards/standard.py:204` - error: Incompatible default for argument "context" (default has type "None", argument has type "dict
  - ID: 3225b21d
- `packages/haive-games/src/haive/games/core/components/cards/standard.py:248` - error: Incompatible default for argument "context" (default has type "None", argument has type "dict
  - ID: dc53ee6a
- `packages/haive-games/src/haive/games/core/components/cards/scoring.py:36` - error: Incompatible default for argument "context" (default has type "None", argument has type "dict
  - ID: ea5e0a4f
- `packages/haive-games/src/haive/games/core/components/cards/scoring.py:42` - error: Incompatible default for argument "context" (default has type "None", argument has type "dict
  - ID: a7912e5d
- `packages/haive-games/src/haive/games/core/components/cards/base.py:135` - error: Incompatible default for argument "context" (default has type "None", argument has type "dict
  - ID: 2add4e38
- ... and 18 more

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/cli/mcp_manager.py:123` - error: Returning Any from function declared to return "dict[Any, Any]" [no-any-return]
  - ID: d514711e
- `packages/haive-mcp/src/haive/mcp/cli/mcp_manager.py:164` - error: Returning Any from function declared to return "dict[Any, Any]" [no-any-return]
  - ID: b15f2c92
- `packages/haive-mcp/src/haive/mcp/cli/mcp_manager.py:285` - error: Returning Any from function declared to return "dict[Any, Any]" [no-any-return]
  - ID: e9c269b6
- `packages/haive-mcp/src/haive/mcp/agents/documentation_agent.py:524` - error: Item "dict[Any, Any]" of "list[Any] | dict[Any, Any] | str | None" has no attribute "extend"
  - ID: 4d543947

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/models.py:32` - error: Returning Any from function declared to return "dict[Any, Any]" [no-any-return]
  - ID: 5579d494
- `packages/haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:245` - error: Item "BaseModel" of "BaseModel | dict[Any, Any]" has no attribute "city" [union-attr]
  - ID: d0cc67ed
- `packages/haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:245` - error: Item "BaseModel" of "BaseModel | dict[Any, Any]" has no attribute "city" [union-attr]
  - ID: d0cc67ed
- `packages/haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:246` - error: Item "BaseModel" of "BaseModel | dict[Any, Any]" has no attribute "messages" [union-attr]
  - ID: bd3ce9e8
- `packages/haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:246` - error: Item "BaseModel" of "BaseModel | dict[Any, Any]" has no attribute "messages" [union-attr]
  - ID: bd3ce9e8
- `packages/haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:251` - error: Item "BaseModel" of "BaseModel | dict[Any, Any]" has no attribute "city" [union-attr]
  - ID: 8ec4de57
- `packages/haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:251` - error: Item "BaseModel" of "BaseModel | dict[Any, Any]" has no attribute "city" [union-attr]
  - ID: 8ec4de57
- `packages/haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:252` - error: Item "BaseModel" of "BaseModel | dict[Any, Any]" has no attribute "country" [union-attr]
  - ID: 09ae7bf6
- `packages/haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:252` - error: Item "BaseModel" of "BaseModel | dict[Any, Any]" has no attribute "country" [union-attr]
  - ID: 09ae7bf6

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/techy_phrase_tool.py:54` - error: Returning Any from function declared to return "dict[Any, Any]" [no-any-return]
  - ID: 0b812dcb
- `packages/haive-tools/src/haive/tools/tools/openaq_tool.py:55` - error: Returning Any from function declared to return "dict[Any, Any]" [no-any-return]
  - ID: 1755129d
- `packages/haive-tools/src/haive/tools/tools/open_food_tool.py:58` - error: Returning Any from function declared to return "dict[Any, Any]" [no-any-return]
  - ID: fbe9dec1
- `packages/haive-tools/src/haive/tools/tools/binlist_lookup.py:74` - error: Returning Any from function declared to return "dict[Any, Any]" [no-any-return]
  - ID: ab1762e0
- `packages/haive-tools/src/haive/tools/tools/toolkits/rps_101_toolkit.py:92` - error: Returning Any from function declared to return "dict[Any, Any]" [no-any-return]
  - ID: 0bf120cd
- `packages/haive-tools/src/haive/tools/tools/toolkits/rps_101_toolkit.py:140` - error: Returning Any from function declared to return "dict[Any, Any]" [no-any-return]
  - ID: 67104c72
- `packages/haive-tools/src/haive/tools/tools/toolkits/poetry_db_toolkit.py:95` - error: Returning Any from function declared to return "dict[Any, Any]" [no-any-return]
  - ID: 1ffff39b
- `packages/haive-tools/src/haive/tools/tools/toolkits/lcbo_toolkit.py:51` - error: Returning Any from function declared to return "dict[Any, Any]" [no-any-return]
  - ID: a54aa998
- `packages/haive-tools/src/haive/tools/tools/toolkits/lcbo_toolkit.py:97` - error: Returning Any from function declared to return "dict[Any, Any]" [no-any-return]
  - ID: f6a8288e
- `packages/haive-tools/src/haive/tools/tools/toolkits/free_to_game_toolkit.py:111` - error: Returning Any from function declared to return "dict[Any, Any]" [no-any-return]
  - ID: a8b96287
- ... and 7 more

## mypy:Any, Any, Any (60 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_v2/multi_memory_coordinator.py:641` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[Any], /) -> None
  - ID: 754f5ea4
- `packages/haive-agents/src/haive/agents/memory_v2/multi_memory_coordinator.py:655` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[Any], /) -> None
  - ID: b69e8640
- `packages/haive-agents/src/haive/agents/common/utils/pydantic_prompt_utils.py:89` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[Any], /) -> None
  - ID: dc3081fd
- `packages/haive-agents/src/haive/agents/base/agent.py:859` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[str], /) -> None
  - ID: e90a129b
- `packages/haive-agents/src/haive/agents/base/agent.py:863` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[str], /) -> None
  - ID: 532e1d8d
- `packages/haive-agents/src/haive/agents/base/agent.py:864` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[str], /) -> None
  - ID: 900a80c4
- `packages/haive-agents/src/haive/agents/base/agent.py:866` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[str], /) -> None
  - ID: fa528da5
- `packages/haive-agents/src/haive/agents/base/agent.py:870` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[str], /) -> None
  - ID: 88d0799b
- `packages/haive-agents/src/haive/agents/base/agent.py:872` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[str], /) -> None
  - ID: 67889e5a
- `packages/haive-agents/src/haive/agents/memory_v2/simple_memory_agent.py:794` - error: Invalid index type "str" for "str"; expected type "SupportsIndex | slice[Any, Any, Any]" [in
  - ID: 3af3f6a5
- ... and 1 more

### haive-core

- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:239` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[str | dict[Any, Any]], /) -> None
  - ID: 4d3b4120
- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:243` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[str | dict[Any, Any]], /) -> None
  - ID: 317e876c
- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:267` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[str | dict[Any, Any]], /) -> None
  - ID: f221f746
- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:271` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[str | dict[Any, Any]], /) -> None
  - ID: db157cf9
- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:354` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[str | dict[Any, Any]], /) -> None
  - ID: ec0fd0f6
- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:374` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[str | dict[Any, Any]], /) -> None
  - ID: e99b75f9
- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:376` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[str | dict[Any, Any]], /) -> None
  - ID: f268fde7
- `packages/haive-core/src/haive/core/graph/node/message_transformation.py:168` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[str | dict[Any, Any]], /) -> None
  - ID: 96b8b0b7
- `packages/haive-core/src/haive/core/graph/node/message_transformation.py:172` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[str | dict[Any, Any]], /) -> None
  - ID: fa6b7d1f
- `packages/haive-core/src/haive/core/graph/node/message_transformation.py:196` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[str | dict[Any, Any]], /) -> None
  - ID: 6af8ecef
- ... and 16 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py:206` - note: def **getitem**(self, slice[Any, Any, Any], /) -> list[Any]
  - ID: c2ef4dc5
- `packages/haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py:207` - note: def **getitem**(self, slice[Any, Any, Any], /) -> list[Any]
  - ID: c9f009ef
- `packages/haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py:208` - note: def **getitem**(self, slice[Any, Any, Any], /) -> list[Any]
  - ID: bdf279b7
- `packages/haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py:213` - note: def **getitem**(self, slice[Any, Any, Any], /) -> list[Any]
  - ID: 4488b9fe

### haive-games

- `packages/haive-games/src/haive/games/reversi/state_manager.py:51` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[None], /) -> None
  - ID: de53af64
- `packages/haive-games/src/haive/games/reversi/state_manager.py:52` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[None], /) -> None
  - ID: b6d95468
- `packages/haive-games/src/haive/games/reversi/state_manager.py:53` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[None], /) -> None
  - ID: 1c0d25a6
- `packages/haive-games/src/haive/games/reversi/state_manager.py:54` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[None], /) -> None
  - ID: a57d256f

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/agents/documentation_agent.py:504` - note: def **setitem**(self, slice[Any, Any, Any], Iterable[Any], /) -> None
  - ID: e28a92ba

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/tools.py:375` - error: Invalid index type "str" for "str"; expected type "SupportsIndex | slice[Any, Any, Any]" [in
  - ID: 47852ab9
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:495` - error: Invalid index type "str" for "str"; expected type "SupportsIndex | slice[Any, Any, Any]" [in
  - ID: fcffb3cc
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:497` - error: Invalid index type "str" for "str"; expected type "SupportsIndex | slice[Any, Any, Any]" [in
  - ID: 4ab88e95
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:499` - error: Invalid index type "str" for "str"; expected type "SupportsIndex | slice[Any, Any, Any]" [in
  - ID: 07acdaec
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:504` - error: Invalid index type "str" for "str"; expected type "SupportsIndex | slice[Any, Any, Any]" [in
  - ID: 7521d415
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:505` - error: Invalid index type "str" for "str"; expected type "SupportsIndex | slice[Any, Any, Any]" [in
  - ID: 0de39ecc
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:507` - error: Invalid index type "str" for "str"; expected type "SupportsIndex | slice[Any, Any, Any]" [in
  - ID: 9e688cdc
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:515` - error: Invalid index type "str" for "str"; expected type "SupportsIndex | slice[Any, Any, Any]" [in
  - ID: c47a0873
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:516` - error: Invalid index type "str" for "str"; expected type "SupportsIndex | slice[Any, Any, Any]" [in
  - ID: a3858e98
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:517` - error: Invalid index type "str" for "str"; expected type "SupportsIndex | slice[Any, Any, Any]" [in
  - ID: a104a415
- ... and 3 more

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/translate_tools.py:190` - note: def \_arun(self, \*args: Any, \*\*kwargs: Any) -> Coroutine[Any, Any, Any]
  - ID: 9c64e3c2

## mypy:Any, Any, AsyncPostgresSaverNoPreparedStatements (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/persistence/postgres_saver_override.py:86` - note: def from_conn_string(cls, conn_string: str) -> Coroutine[Any, Any, AsyncPostgresSaver
  - ID: b978b9b1

## mypy:Any, Any, None (2 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/utils/utils.py:33` - error: Value of type "Coroutine[Any, Any, None]" must be used [unused-coroutine]
  - ID: d712020c

### haive-core

- `packages/haive-core/src/haive/core/engine/document/loaders/auto_loader.py:1267` - error: Value of type "Coroutine[Any, Any, None]" must be used [unused-coroutine]
  - ID: 16b52038

## mypy:Any, Any, O (2 errors)

### haive-core

- `packages/haive-core/src/haive/core/runtime/base/base.py:41` - note: def ainvoke(self, input: I, config: RunnableConfig | None = ..., \*\*kwargs: Any) -> Co
  - ID: eb2d0e6b
- `packages/haive-core/src/haive/core/runtime/base/base.py:41` - note: def ainvoke(self, input: I, config: RunnableConfig | None = ..., \*\*kwargs: Any) -> Co
  - ID: eb2d0e6b

## mypy:Any, Any, VectorStore (2 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/vectorstore/vectorstore.py:479` - error: Incompatible return value type (got "Coroutine[Any, Any, VectorStore]", expected "VectorStore
  - ID: 7fa2ed47
- `packages/haive-core/src/haive/core/engine/vectorstore/vectorstore.py:493` - error: Incompatible return value type (got "Coroutine[Any, Any, VectorStore]", expected "VectorStore
  - ID: e1534b86

## mypy:Any, list[Any (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/graph/state_graph_manager.py:43` - error: Value of type "defaultdict[Any, list[Any]] | list[Any] | Any | dict[Any, Any] | bool | None"
  - ID: 635c031e

## mypy:Any, str (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/multi/archive/enhanced_base.py:547` - error: Incompatible types in assignment (expression has type "str", variable has type "dict[Any, str
  - ID: 2c4cd43b

## mypy:Any, tuple[<typing special form>, None (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/research/person/agent.py:408` - error: No overload variant of "create_model" matches argument types "str", "dict[Any, tuple[<typing
  - ID: 59861258

## mypy:Any, tuple[Any, Any (3 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/base/agent.py:348` - error: No overload variant of "create_model" matches argument types "str", "dict[Any, tuple[Any, Any
  - ID: 01c9b433

### haive-core

- `packages/haive-core/src/haive/core/schema/composer/schema_composer.py:188` - error: No overload variant of "create_model" matches argument types "str", "Any", "dict[Any, tuple[A
  - ID: ffc45e8f
- `packages/haive-core/src/haive/core/utils/tools/tool_schema_generator.py:113` - error: No overload variant of "create_model" matches argument types "str", "dict[Any, tuple[Any, Any
  - ID: 34553c7b

## mypy:Any, type[BaseModel (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/schema/schema_composer.py:3372` - error: No overload variant of "create_model" matches argument types "str", "tuple[Any, type[BaseMode
  - ID: a3750de0

## mypy:ArangoDBSource (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/document/loaders/sources/database_sources.py:607` - error: Argument 1 has incompatible type "type[ArangoDBSource]"; expected "type[DatabaseSource]" [ar
  - ID: 099a2ffa

## mypy:AsyncConnection[tuple[Any, ... (4 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/agent/persistence/manager.py:135` - error: Argument 1 to "AsyncPostgresSaver" has incompatible type "AsyncConnectionPool[AsyncConnection
  - ID: 953d2e93
- `packages/haive-core/src/haive/core/engine/agent/persistence/manager.py:136` - error: Incompatible types in assignment (expression has type "AsyncConnectionPool[AsyncConnection[tu
  - ID: a4c083a7
- `packages/haive-core/src/haive/core/engine/agent/persistence/manager.py:147` - error: Argument 1 to "PostgresSaver" has incompatible type "AsyncConnectionPool[AsyncConnection[tupl
  - ID: 64949cc1
- `packages/haive-core/src/haive/core/engine/agent/persistence/manager.py:148` - error: Incompatible types in assignment (expression has type "AsyncConnectionPool[AsyncConnection[tu
  - ID: 1f2efa19

## mypy:AsyncMongoDBSaver, None (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/agent/persistence/mongodb_config.py:74` - error: Incompatible types in "await" (actual type "\_AsyncGeneratorContextManager[AsyncMongoDBSaver,
  - ID: 1d9579a1

## mypy:AsyncPostgresSaver, None (2 errors)

### haive-core

- `packages/haive-core/src/haive/core/persistence/postgres_saver_override.py:86` - note: def from_conn_string(conn_string: str, \*, pipeline: bool = ..., serde: SerializerProt
  - ID: 733a0c1e
- `packages/haive-core/src/haive/core/engine/agent/persistence/manager.py:138` - error: Incompatible types in assignment (expression has type "\_AsyncGeneratorContextManager[AsyncPos
  - ID: 732bc614

## mypy:AsyncPostgresStoreWrapper (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/persistence/store/factory.py:17` - error: Incompatible types in assignment (expression has type "None", variable has type "type[AsyncPo
  - ID: ee3c5814

## mypy:BaseCallbackHandler (4 errors)

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/search_and_summarize/tools.py:108` - error: Argument 2 to "**call**" of "BaseTool" has incompatible type "int"; expected "list[BaseCallba
  - ID: 8abdb2e6
- `packages/haive-prebuilt/src/haive/prebuilt/search_and_summarize/tools.py:125` - error: Argument 2 to "**call**" of "BaseTool" has incompatible type "int"; expected "list[BaseCallba
  - ID: 26cfe280
- `packages/haive-prebuilt/src/haive/prebuilt/search_and_summarize/tools.py:142` - error: Argument 2 to "**call**" of "BaseTool" has incompatible type "int"; expected "list[BaseCallba
  - ID: 8624c232
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:489` - error: Argument 2 to "**call**" of "BaseTool" has incompatible type "int"; expected "list[BaseCallba
  - ID: 6bcbde2a

## mypy:BaseException (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/planning/llm_compiler/utils.py:153` - note: def format_exception(type[BaseException] | None, /, value: BaseException | None = ..., tb:
  - ID: f722dee7

## mypy:BaseLoader (2 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/document/loaders/registry.py:282` - error: "type[BaseLoader]" has no attribute "Config" [attr-defined]
  - ID: 577c2894
- `packages/haive-core/src/haive/core/engine/document/loaders/base_new.py:165` - error: Returning Any from function declared to return "type[BaseLoader]" [no-any-return]
  - ID: ab93378e

## mypy:BaseMessage (27 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/reflection/multi_agent_reflection.py:412` - note: Perhaps you need a type annotation for "transformed"? Suggestion: "list[BaseMessage]"
  - ID: 1a0e9eef
- `packages/haive-agents/src/haive/agents/simple/state.v2.py:47` - error: Argument 1 to "add_messages" has incompatible type "Sequence[BaseMessage]"; expected "list[Ba
  - ID: 8924ef85
- `packages/haive-agents/src/haive/agents/simple/state.v2.py:63` - error: Argument 1 to "add_messages" has incompatible type "Sequence[BaseMessage]"; expected "list[Ba
  - ID: dc273306
- `packages/haive-agents/src/haive/agents/simple/state.py:34` - error: Argument 1 to "add_messages" has incompatible type "Sequence[BaseMessage]"; expected "list[Ba
  - ID: 7d7e6245
- `packages/haive-agents/src/haive/agents/simple/state.py:50` - error: Argument 1 to "add_messages" has incompatible type "Sequence[BaseMessage]"; expected "list[Ba
  - ID: 7a7993e8
- `packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/agent.py:303` - error: Returning Any from function declared to return "list[BaseMessage]" [no-any-return]
  - ID: a97d8edd
- `packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/agent.py:305` - error: Returning Any from function declared to return "list[BaseMessage]" [no-any-return]
  - ID: 2c89581c

### haive-core

- `packages/haive-core/src/haive/core/engine/prompt_template/prompt_engine.py:382` - error: Incompatible types in assignment (expression has type "str", variable has type "list[BaseMess
  - ID: 9ae25c3f
- `packages/haive-core/src/haive/core/engine/prompt_template/prompt_engine.py:398` - error: Incompatible return value type (got "list[BaseMessage]", expected "str | list[AIMessage | Hum
  - ID: 249fc219
- `packages/haive-core/src/haive/core/engine/aug_llm/config.py:1020` - error: Dict entry 0 has incompatible type "str": "list[BaseMessage]"; expected "str": "list[HumanMes
  - ID: 58ef9c3e
- `packages/haive-core/src/haive/core/graph/node/parser_node_config_v2.py:488` - error: Incompatible types in assignment (expression has type "list[BaseMessage]", target has type "s
  - ID: 49dbb580
- `packages/haive-core/src/haive/core/graph/node/parser_node_config_v2.py:526` - error: Incompatible types in assignment (expression has type "list[BaseMessage]", target has type "s
  - ID: 80ece075
- `packages/haive-core/src/haive/core/graph/node/parser_node_config_v2.py:572` - error: Incompatible types in assignment (expression has type "list[BaseMessage]", target has type "s
  - ID: 64b3fe1a
- `packages/haive-core/src/haive/core/graph/node/parser_node_config_v2.py:594` - error: Incompatible types in assignment (expression has type "list[BaseMessage]", target has type "s
  - ID: 9cc191da
- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:253` - note: Perhaps you need a type annotation for "transformed"? Suggestion: "list[BaseMessage]"
  - ID: c616a77e
- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:281` - note: Perhaps you need a type annotation for "transformed"? Suggestion: "list[BaseMessage]"
  - ID: ac2c209f
- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:360` - note: Perhaps you need a type annotation for "transformed"? Suggestion: "list[BaseMessage]"
  - ID: 2eee1665
- ... and 10 more

## mypy:BaseMessage | list[str (6 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/simple/state.v2.py:47` - error: Incompatible types in assignment (expression has type "list[BaseMessage | list[str] | tuple[s
  - ID: 05c17d5e
- `packages/haive-agents/src/haive/agents/simple/state.v2.py:63` - error: Incompatible types in assignment (expression has type "list[BaseMessage | list[str] | tuple[s
  - ID: 40b046c4
- `packages/haive-agents/src/haive/agents/simple/state.py:34` - error: Incompatible types in assignment (expression has type "list[BaseMessage | list[str] | tuple[s
  - ID: 80fa62ca
- `packages/haive-agents/src/haive/agents/simple/state.py:50` - error: Incompatible types in assignment (expression has type "list[BaseMessage | list[str] | tuple[s
  - ID: ee48b870

### haive-core

- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:881` - error: Argument "root" to "MessageList" has incompatible type "list[BaseMessage | list[str] | tuple[
  - ID: 8059c13a
- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:883` - error: Argument "root" to "MessageList" has incompatible type "list[BaseMessage | list[str] | tuple[
  - ID: 9672cdd4

## mypy:BaseModel (134 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_v2/standalone_rag_memory.py:670` - note: def tool(\*, description: str | None = ..., return_direct: bool = ..., args_schema: type[Ba
  - ID: d8a894ad
- `packages/haive-agents/src/haive/agents/memory_v2/standalone_rag_memory.py:670` - note: def tool(\*, description: str | None = ..., return_direct: bool = ..., args_schema: type[Ba
  - ID: d8a894ad
- `packages/haive-agents/src/haive/agents/memory_v2/long_term_memory_agent.py:475` - note: def tool(\*, description: str | None = ..., return_direct: bool = ..., args_schema: type[Ba
  - ID: a2118e25
- `packages/haive-agents/src/haive/agents/memory_v2/long_term_memory_agent.py:475` - note: def tool(\*, description: str | None = ..., return_direct: bool = ..., args_schema: type[Ba
  - ID: a2118e25
- `packages/haive-agents/src/haive/agents/memory_reorganized/agents/ltm.py:464` - note: def tool(\*, description: str | None = ..., return_direct: bool = ..., args_schema: type[Ba
  - ID: 6873d7de
- `packages/haive-agents/src/haive/agents/memory_reorganized/agents/ltm.py:464` - note: def tool(\*, description: str | None = ..., return_direct: bool = ..., args_schema: type[Ba
  - ID: 6873d7de
- `packages/haive-agents/src/haive/agents/long_term_memory/tools.py:52` - error: Incompatible return value type (got "list[BaseModel]", expected "str") [return-value]
  - ID: 88bfb055
- `packages/haive-agents/src/haive/agents/common/utils/pydantic_prompt_utils.py:147` - error: Incompatible types in assignment (expression has type "type[BaseModel]", target has type "lis
  - ID: 843ef420
- `packages/haive-agents/src/haive/agents/memory_v2/rag_memory_agent.py:633` - note: def tool(\*, description: str | None = ..., return_direct: bool = ..., args_schema: type[Ba
  - ID: 4340da7a
- `packages/haive-agents/src/haive/agents/memory_v2/rag_memory_agent.py:633` - note: def tool(\*, description: str | None = ..., return_direct: bool = ..., args_schema: type[Ba
  - ID: 4340da7a
- ... and 11 more

### haive-core

- `packages/haive-core/src/haive/core/utils/pydantic_utils/ui.py:34` - error: Item "BaseModel" of "type[BaseModel] | BaseModel | overloaded function" has no attribute "\_\_n
  - ID: 04bc242c
- `packages/haive-core/src/haive/core/utils/pydantic_utils/ui.py:38` - error: Item "BaseModel" of "type[BaseModel] | BaseModel | overloaded function" has no attribute "\_\_n
  - ID: 7041cef8
- `packages/haive-core/src/haive/core/utils/pydantic_utils/ui.py:45` - error: Item "function" of "type[BaseModel] | BaseModel | overloaded function" has no attribute "mode
  - ID: 10272a14
- `packages/haive-core/src/haive/core/utils/pydantic_utils/ui.py:92` - error: Item "function" of "type[BaseModel] | BaseModel | overloaded function" has no attribute "mode
  - ID: 4acf2a55
- `packages/haive-core/src/haive/core/utils/haive_discovery/base_analyzer.py:159` - error: Returning Any from function declared to return "type[BaseModel]" [no-any-return]
  - ID: 26aecb92
- `packages/haive-core/src/haive/core/schema/utils.py:306` - error: No overload variant of "create_model" matches argument types "str", "type[BaseModel] | Any",
  - ID: 2924296b
- `packages/haive-core/src/haive/core/schema/utils.py:325` - error: Returning Any from function declared to return "type[BaseModel]" [no-any-return]
  - ID: 1a3ae41b
- `packages/haive-core/src/haive/core/schema/utils.py:392` - error: Returning Any from function declared to return "type[BaseModel]" [no-any-return]
  - ID: f19629f4
- `packages/haive-core/src/haive/core/schema/ui.py:129` - error: Argument 1 to "issubclass" has incompatible type "overloaded function | type[BaseModel] | Bas
  - ID: 1c5daaa1
- `packages/haive-core/src/haive/core/schema/ui.py:132` - error: Item "BaseModel" of "type[BaseModel] | BaseModel | overloaded function" has no attribute "\_\_n
  - ID: 4b18aff5
- ... and 96 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/serialization.py:357` - error: Returning Any from function declared to return "type[BaseModel] | None" [no-any-return]
  - ID: dc7bbbdd
- `packages/haive-dataflow/src/haive/dataflow/registry/serialization.py:438` - error: Returning Any from function declared to return "type[BaseModel] | None" [no-any-return]
  - ID: a3444f2f
- `packages/haive-dataflow/src/haive/dataflow/game_agent.py:372` - error: Item "ModelMetaclass" of "type[BaseModel] | None" has no attribute "initialize" [union-attr]
  - ID: 9a806f98
- `packages/haive-dataflow/src/haive/dataflow/game_agent.py:372` - error: Item "ModelMetaclass" of "type[BaseModel] | None" has no attribute "initialize" [union-attr]
  - ID: 9a806f98
- `packages/haive-dataflow/src/haive/dataflow/api/game_agent.py:372` - error: Item "ModelMetaclass" of "type[BaseModel] | None" has no attribute "initialize" [union-attr]
  - ID: 08c30071
- `packages/haive-dataflow/src/haive/dataflow/api/game_agent.py:372` - error: Item "ModelMetaclass" of "type[BaseModel] | None" has no attribute "initialize" [union-attr]
  - ID: 08c30071

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/company_researcher/config.py:124` - error: Returning Any from function declared to return "type[BaseModel]" [no-any-return]
  - ID: 08973d4c

## mypy:BasePlan[Any (2 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/planning/base/models.py:446` - error: Argument 1 to "\_restore_state" of "IntelligentSequence" has incompatible type "list[BasePlan[
  - ID: 97798a3b
- `packages/haive-agents/src/haive/agents/planning/base/models.py:745` - error: Incompatible return value type (got "list[BasePlan[Any] | BaseStep | list[BaseStep] | Callabl
  - ID: c4f04426

## mypy:BaseStatement (1 errors)

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1221` - error: Argument "body" to "IndentedBlock" has incompatible type "Sequence[BaseStatement] | Sequence[
  - ID: 7c0e1ab1

## mypy:BaseStep (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/planning/base/models.py:755` - error: Item "list[BaseStep]" of "BasePlan[Any] | Any | BaseStep | list[BaseStep] | Callable[..., Any
  - ID: b1b9ddb6

## mypy:BaseTool (6 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/react_class/react/agent.py:183` - error: Returning Any from function declared to return "list[BaseTool]" [no-any-return]
  - ID: f9d5b580

### haive-core

- `packages/haive-core/src/haive/core/utils/tools/tool_schema_generator.py:29` - error: Incompatible types in assignment (expression has type "None", variable has type "type[BaseToo
  - ID: 8836d70f
- `packages/haive-core/src/haive/core/engine/tool/base.py:140` - error: Argument 1 to "extend" of "list" has incompatible type "list[BaseTool]"; expected "Iterable[S
  - ID: 857d930e
- `packages/haive-core/src/haive/core/engine/tool/base.py:144` - error: Argument 1 to "extend" of "list" has incompatible type "list[BaseTool]"; expected "Iterable[S
  - ID: 49afeb1b

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/mixins/mcp_mixin.py:68` - error: Incompatible types in assignment (expression has type "None", variable has type "type[BaseToo
  - ID: 9b1fa24c

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/financialdatasets_toolkit.py:108` - error: Incompatible return value type (got "list[BaseTool]", expected "list[Tool]") [return-value]
  - ID: c924450b

## mypy:BaseTool | Tool | StructuredTool (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/tool/base.py:148` - note: Perhaps you need a type annotation for "all_tools"? Suggestion: "list[BaseTool | Tool | Struct
  - ID: a55355f3

## mypy:BaseToolkit (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/utils/tools/tool_schema_generator.py:31` - error: Incompatible types in assignment (expression has type "None", variable has type "type[BaseToo
  - ID: 2783dcbc

## mypy:BasicInfo (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/schema/compatibility/examples.py:159` - error: List item 0 has incompatible type "type[BasicInfo]"; expected "type[BaseModel]" [list-item]
  - ID: 74ce0310

## mypy:BigQuerySource (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/document/loaders/sources/database_sources.py:653` - error: Argument 1 has incompatible type "type[BigQuerySource]"; expected "type[DatabaseSource]" [ar
  - ID: 93d137f8

## mypy:C (2 errors)

### haive-games

- `packages/haive-games/src/haive/games/core/game/containers/deck.py:108` - error: Returning Any from function declared to return "list[C]" [no-any-return]
  - ID: 900d13ce
- `packages/haive-games/src/haive/games/core/game/containers/deck.py:120` - error: Returning Any from function declared to return "list[C]" [no-any-return]
  - ID: 20d6c038

## mypy:CardContainer[TCard (2 errors)

### haive-games

- `packages/haive-games/src/haive/games/core/components/cards/base.py:88` - error: Returning Any from function declared to return "type[CardContainer[TCard]]" [no-any-return]
  - ID: 91dd319a
- `packages/haive-games/src/haive/games/core/components/cards/base.py:88` - error: Returning Any from function declared to return "type[CardContainer[TCard]]" [no-any-return]
  - ID: 91dd319a

## mypy:CardGameTurn (1 errors)

### haive-games

- `packages/haive-games/src/haive/games/core/components/cards/turns.py:78` - error: The type "type[CardGameTurn]" is not generic and not indexable [misc]
  - ID: 12160dfd

## mypy:CassandraSource (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/document/loaders/sources/database_sources.py:484` - error: Argument 1 has incompatible type "type[CassandraSource]"; expected "type[DatabaseSource]" [a
  - ID: b45633a2

## mypy:ChatState (3 errors)

### haive-core

- `packages/haive-core/src/haive/core/schema/compatibility/examples.py:260` - error: "type[ChatState]" has no attribute "**shared_fields**" [attr-defined]
  - ID: 28796815
- `packages/haive-core/src/haive/core/schema/compatibility/examples.py:261` - error: "type[ChatState]" has no attribute "**reducer_fields**" [attr-defined]
  - ID: 2a8e52ce
- `packages/haive-core/src/haive/core/schema/compatibility/examples.py:262` - error: "type[ChatState]" has no attribute "**engine_io_mappings**" [attr-defined]
  - ID: e1e44a9e

## mypy:CheckpointTuple (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/persistence/sqlite_config.py:396` - error: Incompatible return value type (got "list[CheckpointTuple]", expected "list[tuple[dict[str, A
  - ID: 46da7738

## mypy:Collection[str (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/vectorstore/providers/WeaviateVectorStoreConfig.py:239` - error: "Sequence[Collection[str]]" has no attribute "append" [attr-defined]
  - ID: c05a7f84

## mypy:ComplexityHotspot (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:285` - error: Incompatible types in assignment (expression has type "None", variable has type "list[Complex
  - ID: 0ee31fd5

## mypy:Connection[dict[str, Any (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/persistence/postgres_saver_with_thread_creation.py:78` - error: Item "ConnectionPool[Connection[dict[str, Any]]]" of "Connection[dict[str, Any]] | Connection
  - ID: fbd79baf

## mypy:Connection[tuple[Any, ... (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/agent/persistence/manager.py:140` - error: Incompatible types in assignment (expression has type "ConnectionPool[Connection[tuple[Any, .
  - ID: 8a2998af

## mypy:DataProcessingState (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/schema/base_state_schemas.py:427` - error: Incompatible return value type (got "type[DataProcessingState]", expected "type[AgentState]")
  - ID: 7495ba0e

## mypy:DocArrayHnswSearch (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/vectorstore/providers/DocArrayVectorStoreConfig.py:206` - error: Incompatible import of "DocArrayStore" (imported name has type "type[DocArrayHnswSearch]", lo
  - ID: a48a411e

## mypy:DocArrayRetriever (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/retriever/providers/DocArrayRetrieverConfig.py:195` - error: "type[DocArrayRetriever]" has no attribute "from_documents" [attr-defined]
  - ID: 02b14960

## mypy:Document (22 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/rag/simple/multi_agent_simple_rag.py:195` - error: Returning Any from function declared to return "list[Document]" [no-any-return]
  - ID: d3d77b76
- `packages/haive-agents/src/haive/agents/rag/simple/clean_simple_rag.py:221` - error: Returning Any from function declared to return "list[Document]" [no-any-return]
  - ID: eb5a1823
- `packages/haive-agents/src/haive/agents/rag/simple/enhanced_v3/retriever_agent.py:181` - error: Returning Any from function declared to return "list[Document]" [no-any-return]
  - ID: 2bb412e4
- `packages/haive-agents/src/haive/agents/rag/simple/enhanced_v3/retriever_agent.py:183` - error: Returning Any from function declared to return "list[Document]" [no-any-return]
  - ID: ecdf2ee8
- `packages/haive-agents/src/haive/agents/document_modifiers/base/state.py:198` - error: Unsupported left operand type for - ("list[Document]") [operator]
  - ID: 11975cca
- `packages/haive-agents/src/haive/agents/document_modifiers/base/state.py:213` - error: Unsupported left operand type for - ("list[Document]") [operator]
  - ID: e219b210
- `packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_base/models.py:62` - note: def transform_documents(self, documents: Sequence[Document], \*\*kwargs: Any) -> Sequen
  - ID: 549c2fcf
- `packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_base/models.py:62` - note: def transform_documents(self, documents: Sequence[Document], \*\*kwargs: Any) -> Sequen
  - ID: 549c2fcf

### haive-core

- `packages/haive-core/src/haive/core/engine/document/engine.py:167` - error: Returning Any from function declared to return "list[Document]" [no-any-return]
  - ID: 3ade9e74
- `packages/haive-core/src/haive/core/engine/document/loaders/adapters/base.py:71` - error: Returning Any from function declared to return "list[Document]" [no-any-return]
  - ID: 371bc6f5
- `packages/haive-core/src/haive/core/engine/document/loaders/engine.py:194` - error: "list[Document]" has no attribute "documents" [attr-defined]
  - ID: 5215815b
- `packages/haive-core/src/haive/core/engine/document/loaders/engine.py:208` - error: "list[Document]" has no attribute "loader_name" [attr-defined]
  - ID: ae97329e
- `packages/haive-core/src/haive/core/engine/document/loaders/engine.py:213` - error: "list[Document]" has no attribute "source_type" [attr-defined]
  - ID: 51174c83
- `packages/haive-core/src/haive/core/engine/document/loaders/engine.py:234` - error: "list[Document]" has no attribute "source_type" [attr-defined]
  - ID: 8d36052e
- `packages/haive-core/src/haive/core/engine/document/loaders/engine.py:235` - error: "list[Document]" has no attribute "loader_name" [attr-defined]
  - ID: 76f1e404
- `packages/haive-core/src/haive/core/engine/document/loaders/engine.py:251` - error: "list[Document]" has no attribute "source_type" [attr-defined]
  - ID: fd7ba192
- `packages/haive-core/src/haive/core/engine/document/loaders/engine.py:270` - error: "list[Document]" has no attribute "loader_name" [attr-defined]
  - ID: 149d3db8
- `packages/haive-core/src/haive/core/engine/document/loaders/engine.py:271` - error: "list[Document]" has no attribute "source_type" [attr-defined]
  - ID: 8b8e7329
- ... and 3 more

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/simple_rag_mcp_agent.py:84` - error: Returning Any from function declared to return "list[Document]" [no-any-return]
  - ID: af51bfaf

## mypy:DocumentLike (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/document/loaders/base/schema.py:26` - note: (Hint: Use "Generic[DocumentLike]" or "Protocol[DocumentLike]" base class to bind "DocumentLik
  - ID: 929fd8af

## mypy:ElasticsearchSource (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/document/loaders/sources/database_sources.py:516` - error: Argument 1 has incompatible type "type[ElasticsearchSource]"; expected "type[DatabaseSource]"
  - ID: cbe5ca9d

## mypy:EnhancedMemoryItem (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_v2/memory_state_original.py:206` - error: "type[EnhancedMemoryItem]" has no attribute "from_schema_memory" [attr-defined]
  - ID: a7a2649c

## mypy:ExecutionResult (3 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/planning/enhanced_plan_execute_v6.py:287` - error: Argument 2 to "get_next_step_v6" has incompatible type "list[ExecutionResult] | list[str]"; e
  - ID: a12233c9
- `packages/haive-agents/src/haive/agents/planning/enhanced_plan_execute_v6.py:288` - error: Incompatible types in assignment (expression has type "str | None", target has type "list[Exe
  - ID: dc8f83f7
- `packages/haive-agents/src/haive/agents/planning/enhanced_plan_execute_v6.py:290` - error: Incompatible types in assignment (expression has type "None", target has type "list[Execution
  - ID: 714fd580

## mypy:FAISS (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/models/vectorstore/base.py:71` - error: Incompatible types in assignment (expression has type "type[FAISS]", variable has type "type[
  - ID: 02fec56b

## mypy:FlowGridSpace (1 errors)

### haive-games

- `packages/haive-games/src/haive/games/single_player/flow_free/base.py:177` - error: The type "type[FlowGridSpace]" is not generic and not indexable [misc]
  - ID: 8a0c17ea

## mypy:GetCardInfoInput (1 errors)

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/yugiioh_toolkit.py:88` - error: Argument "args_schema" to "from_function" of "StructuredTool" has incompatible type "type[Get
  - ID: 97560fa8

## mypy:GraphDocument (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_v2/graph_memory_agent.py:330` - error: Returning Any from function declared to return "list[GraphDocument]" [no-any-return]
  - ID: 0b39575b

## mypy:GraphMemoryAgent (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_v2/multi_memory_agent.py:31` - error: Incompatible types in assignment (expression has type "None", variable has type "type[GraphMe
  - ID: 02980540

## mypy:GraphMemoryConfig (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_v2/multi_memory_agent.py:32` - error: Incompatible types in assignment (expression has type "None", variable has type "type[GraphMe
  - ID: 8377f9a8

## mypy:HumanMessage (38 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/reflection/multi_agent_reflection.py:412` - error: Incompatible return value type (got "list[HumanMessage]", expected "list[BaseMessage]") [ret
  - ID: 9919abf9
- `packages/haive-agents/src/haive/agents/memory_v2/react_memory_coordinator.py:432` - error: Argument 1 to "add_conversation_batch" of "ReactMemoryCoordinator" has incompatible type "lis
  - ID: c1c90fc1
- `packages/haive-agents/src/haive/agents/memory_v2/long_term_memory_agent.py:521` - error: Argument 1 to "add_conversation" of "LongTermMemoryAgent" has incompatible type "list[HumanMe
  - ID: ad82778a
- `packages/haive-agents/src/haive/agents/memory_reorganized/agents/ltm.py:513` - error: Argument 1 to "add_conversation" of "LongTermMemoryAgent" has incompatible type "list[HumanMe
  - ID: 5c20ebf3
- `packages/haive-agents/src/haive/agents/base/mixins/execution_mixin.py:91` - error: Incompatible types in assignment (expression has type "list[HumanMessage]", target has type "
  - ID: 140afb5b
- `packages/haive-agents/src/haive/agents/base/mixins/execution_mixin.py:127` - error: Incompatible types in assignment (expression has type "list[HumanMessage]", target has type "
  - ID: 43544c8c
- `packages/haive-agents/src/haive/agents/simple/state.v2.py:47` - error: Argument 2 to "add_messages" has incompatible type "list[HumanMessage]"; expected "list[BaseM
  - ID: ca9ab99b
- `packages/haive-agents/src/haive/agents/simple/state.py:34` - error: Argument 2 to "add_messages" has incompatible type "list[HumanMessage]"; expected "list[BaseM
  - ID: f2cbc5b5

### haive-core

- `packages/haive-core/src/haive/core/engine/aug_llm/config.py:1016` - error: Incompatible types in assignment (expression has type "str", target has type "list[HumanMessa
  - ID: bb3b8542
- `packages/haive-core/src/haive/core/engine/agent/utils/state_handling.py:215` - error: Incompatible types in assignment (expression has type "str", target has type "list[HumanMessa
  - ID: 29d58d8d
- `packages/haive-core/src/haive/core/engine/agent/utils/state_handling.py:251` - error: Incompatible types in assignment (expression has type "str", target has type "list[HumanMessa
  - ID: 0afc87b4
- `packages/haive-core/src/haive/core/engine/agent/utils/input_handling.py:47` - error: Incompatible types in assignment (expression has type "RunnableConfig", target has type "list
  - ID: ca08bb46
- `packages/haive-core/src/haive/core/engine/agent/utils/input_handling.py:59` - error: Incompatible types in assignment (expression has type "str", target has type "list[HumanMessa
  - ID: 043bbc12
- `packages/haive-core/src/haive/core/engine/agent/utils/input_handling.py:71` - error: Incompatible types in assignment (expression has type "RunnableConfig", target has type "list
  - ID: c45082b3
- `packages/haive-core/src/haive/core/engine/agent/utils/input_handling.py:84` - error: Incompatible types in assignment (expression has type "str", target has type "list[HumanMessa
  - ID: 215d9100
- `packages/haive-core/src/haive/core/engine/agent/utils/input_handling.py:93` - error: Incompatible types in assignment (expression has type "RunnableConfig", target has type "list
  - ID: caa904c8
- `packages/haive-core/src/haive/core/engine/agent/utils/input_handling.py:101` - error: Argument "content" to "HumanMessage" has incompatible type "list[HumanMessage]"; expected "st
  - ID: 5a9b7130
- `packages/haive-core/src/haive/core/engine/agent/utils/input_handling.py:123` - error: Incompatible types in assignment (expression has type "RunnableConfig", target has type "list
  - ID: 6ef06c33
- ... and 16 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/router.py:201` - error: Dict entry 0 has incompatible type "str": "str"; expected "str": "list[HumanMessage]" [dict-
  - ID: 345656fb
- `packages/haive-dataflow/src/haive/dataflow/router.py:206` - error: Dict entry 0 has incompatible type "str": "str"; expected "str": "list[HumanMessage]" [dict-
  - ID: f005a95f
- `packages/haive-dataflow/src/haive/dataflow/api/router.py:201` - error: Dict entry 0 has incompatible type "str": "str"; expected "str": "list[HumanMessage]" [dict-
  - ID: 28f3e94c
- `packages/haive-dataflow/src/haive/dataflow/api/router.py:206` - error: Dict entry 0 has incompatible type "str": "str"; expected "str": "list[HumanMessage]" [dict-
  - ID: 63d5d7e1

## mypy:ImportAlias (1 errors)

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/import_analyzer.py:74` - error: Item "ImportStar" of "Sequence[ImportAlias] | ImportStar" has no attribute "**iter**" (not it
  - ID: 09d33ea6

## mypy:InMemoryVectorStore (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/models/vectorstore/base.py:95` - error: Incompatible types in assignment (expression has type "type[InMemoryVectorStore]", variable h
  - ID: 2f02167d

## mypy:Input, Output (4 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/aug_llm/utils.py:208` - note: def [Input, Output] chain(func: Callable[[Input], Coroutine[Any, Any, Output]]) -> Runnabl
  - ID: e70fc091
- `packages/haive-core/src/haive/core/engine/aug_llm/utils.py:208` - note: def [Input, Output] chain(func: Callable[[Input], Coroutine[Any, Any, Output]]) -> Runnabl
  - ID: e70fc091
- `packages/haive-core/src/haive/core/engine/aug_llm/utils.py:208` - note: def [Input, Output] chain(func: Callable[[Input], Coroutine[Any, Any, Output]]) -> Runnabl
  - ID: e70fc091
- `packages/haive-core/src/haive/core/engine/aug_llm/utils.py:208` - note: def [Input, Output] chain(func: Callable[[Input], Coroutine[Any, Any, Output]]) -> Runnabl
  - ID: e70fc091

## mypy:LTMAgent (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_reorganized/__init__.py:85` - error: Incompatible types in assignment (expression has type "None", variable has type "type[LTMAgen
  - ID: 252d0d75

## mypy:Literal['make_decision' (1 errors)

### haive-games

- `packages/haive-games/src/haive/games/hold_em/player_agent.py:540` - error: Returning Any from function declared to return "Command[Literal['make_decision']]" [no-any-r
  - ID: 892e4202

## mypy:LoaderCapability (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/document/loaders/auto_loader.py:1323` - error: Returning Any from function declared to return "list[LoaderCapability]" [no-any-return]
  - ID: c3c2ee20

## mypy:LogicGridSpace (1 errors)

### haive-games

- `packages/haive-games/src/haive/games/single_player/logic_grid/base.py:144` - error: The type "type[LogicGridSpace]" is not generic and not indexable [misc]
  - ID: 2a58319c

## mypy:LongTermMemoryAgent (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_reorganized/__init__.py:47` - error: Incompatible types in assignment (expression has type "None", variable has type "type[LongTer
  - ID: 59c3f18f

## mypy:M (3 errors)

### haive-games

- `packages/haive-games/src/haive/games/framework/core/player.py:96` - error: Argument 2 of "get_move" is incompatible with supertype "Player"; supertype defines the argum
  - ID: 2d6f008c
- `packages/haive-games/src/haive/games/framework/core/player.py:117` - error: Argument 2 of "get_move" is incompatible with supertype "Player"; supertype defines the argum
  - ID: 65b3ce10
- `packages/haive-games/src/haive/games/framework/core/player.py:143` - error: Argument 2 of "get_move" is incompatible with supertype "Player"; supertype defines the argum
  - ID: 797b7021

## mypy:MemoryRAGConfig (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_v2/multi_memory_agent.py:40` - error: Incompatible types in assignment (expression has type "None", variable has type "type[MemoryR
  - ID: 315afbaf

## mypy:MemoryStateWithTokens (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_reorganized/__init__.py:62` - error: Incompatible types in assignment (expression has type "None", variable has type "type[MemoryS
  - ID: b19d5a5b

## mypy:MemoryType (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_reorganized/__init__.py:63` - error: Incompatible types in assignment (expression has type "None", variable has type "type[MemoryT
  - ID: 4b13dd47

## mypy:Milvus (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/models/vectorstore/base.py:87` - error: Incompatible types in assignment (expression has type "type[Milvus]", variable has type "type
  - ID: 7be8b485

## mypy:Model (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/models/llm/base.py:762` - error: Incompatible return value type (got "list[Model]", expected "list[str]") [return-value]
  - ID: 40199ae7

## mypy:ModelInfo (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/models/llm/base.py:825` - error: Incompatible return value type (got "list[ModelInfo]", expected "list[str]") [return-value]
  - ID: fd1041d0

## mypy:ModelT: BaseModel (25 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/base/agent.py:348` - note: def [ModelT: BaseModel] create_model(str, /, \*, **config**: ConfigDict | None = ..., \_\_doc
  - ID: 50d67e2d
- `packages/haive-agents/src/haive/agents/research/person/agent.py:408` - note: def [ModelT: BaseModel] create_model(str, /, \*, **config**: ConfigDict | None = ..., \_\_doc
  - ID: 128bbb62

### haive-core

- `packages/haive-core/src/haive/core/utils/haive_discovery/base_analyzer.py:159` - note: def [ModelT: BaseModel] create_model(str, /, \*, **config**: ConfigDict | None = ..., \_\_doc
  - ID: f745a795
- `packages/haive-core/src/haive/core/schema/utils.py:306` - note: def [ModelT: BaseModel] create_model(str, /, \*, **config**: ConfigDict | None = ..., \_\_doc
  - ID: 4291af83
- `packages/haive-core/src/haive/core/schema/utils.py:363` - note: def [ModelT: BaseModel] create_model(str, /, \*, **config**: ConfigDict | None = ..., \_\_doc
  - ID: bb6b6d4b
- `packages/haive-core/src/haive/core/schema/schema_manager.py:915` - note: def [ModelT: BaseModel] create_model(str, /, \*, **config**: ConfigDict | None = ..., \_\_doc
  - ID: 7fac3f2d
- `packages/haive-core/src/haive/core/schema/multi_agent_state_schema.py:111` - note: def [ModelT: BaseModel] create_model(str, /, \*, **config**: ConfigDict | None = ..., \_\_doc
  - ID: 00356fa4
- `packages/haive-core/src/haive/core/schema/composer/schema_composer.py:188` - note: def [ModelT: BaseModel] create_model(str, /, \*, **config**: ConfigDict | None = ..., \_\_doc
  - ID: f05a9e6a
- `packages/haive-core/src/haive/core/schema/composer/_base.py:152` - note: def [ModelT: BaseModel] create_model(str, /, \*, **config**: ConfigDict | None = ..., \_\_doc
  - ID: 4816b9d6
- `packages/haive-core/src/haive/core/schema/compatibility/mergers.py:395` - note: def [ModelT: BaseModel] create_model(str, /, \*, **config**: ConfigDict | None = ..., \_\_doc
  - ID: b9bc4140
- `packages/haive-core/src/haive/core/engine/prompt_template/prompt_engine.py:294` - note: def [ModelT: BaseModel] create_model(str, /, \*, **config**: ConfigDict | None = ..., \_\_doc
  - ID: 3258d3ce
- `packages/haive-core/src/haive/core/engine/document/loaders/registry.py:275` - note: def [ModelT: BaseModel] create_model(str, /, \*, **config**: ConfigDict | None = ..., \_\_doc
  - ID: cbe4f345
- ... and 13 more

## mypy:ModelValidatorDecoratorInfo (6 errors)

### haive-core

- `packages/haive-core/src/haive/core/graph/state_graph/models/state_graph_model.py:226` - error: "PydanticDescriptorProxy[ModelValidatorDecoratorInfo]" not callable [operator]
  - ID: 02bef517
- `packages/haive-core/src/haive/core/engine/aug_llm/config.py:1174` - error: "PydanticDescriptorProxy[ModelValidatorDecoratorInfo]" not callable [operator]
  - ID: dc6c83f6
- `packages/haive-core/src/haive/core/engine/aug_llm/config.py:1194` - error: "PydanticDescriptorProxy[ModelValidatorDecoratorInfo]" not callable [operator]
  - ID: 9d63071d
- `packages/haive-core/src/haive/core/engine/aug_llm/config.py:1219` - error: "PydanticDescriptorProxy[ModelValidatorDecoratorInfo]" not callable [operator]
  - ID: 88ad9f39
- `packages/haive-core/src/haive/core/engine/aug_llm/config.py:1227` - error: "PydanticDescriptorProxy[ModelValidatorDecoratorInfo]" not callable [operator]
  - ID: bee8d81c
- `packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py:2547` - error: "PydanticDescriptorProxy[ModelValidatorDecoratorInfo]" not callable [operator]
  - ID: b5347a5a

## mypy:MongoDBSource (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/document/loaders/sources/database_sources.py:433` - error: Argument 1 has incompatible type "type[MongoDBSource]"; expected "type[DatabaseSource]" [arg
  - ID: 2ecd8df9

## mypy:MultiAgentStateSchema (2 errors)

### haive-core

- `packages/haive-core/src/haive/core/schema/multi_agent_state_schema.py:111` - error: No overload variant of "create_model" matches argument types "str", "type[MultiAgentStateSche
  - ID: 9a555484
- `packages/haive-core/src/haive/core/schema/multi_agent_state_schema.py:142` - error: Returning Any from function declared to return "type[MultiAgentStateSchema]" [no-any-return]
  - ID: 51f10585

## mypy:MultiMemoryAgent (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_reorganized/__init__.py:46` - error: Incompatible types in assignment (expression has type "None", variable has type "type[MultiMe
  - ID: 9963f9de

## mypy:MySQLSource (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/document/loaders/sources/database_sources.py:364` - error: Argument 1 has incompatible type "type[MySQLSource]"; expected "type[DatabaseSource]" [arg-t
  - ID: 542465ff

## mypy:Neo4jSource (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/document/loaders/sources/database_sources.py:570` - error: Argument 1 has incompatible type "type[Neo4jSource]"; expected "type[DatabaseSource]" [arg-t
  - ID: ea25580e

## mypy:Never (15 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/conversation/directed/agent.py:383` - error: Incompatible types in assignment (expression has type "list[Never]", target has type "dict[An
  - ID: 4a5fc4de
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/reflection/agent.py:182` - error: Incompatible return value type (got "Command[Never]", expected "dict[str, Any]") [return-val
  - ID: b80a99b4
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/reflection/agent.py:195` - error: Incompatible return value type (got "Command[Never]", expected "dict[str, Any]") [return-val
  - ID: 5b78b3b2
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/reflection/agent.py:232` - error: Incompatible return value type (got "Command[Never]", expected "dict[str, Any]") [return-val
  - ID: 4aaf32ed
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/reflection/agent.py:234` - error: Incompatible return value type (got "Command[Never]", expected "dict[str, Any]") [return-val
  - ID: 98d2c1cc
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/reflection/agent.py:238` - error: Incompatible return value type (got "Command[Never]", expected "dict[str, Any]") [return-val
  - ID: 8511e110
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/reflection/agent.py:385` - error: Incompatible return value type (got "Command[Never]", expected "dict[str, Any]") [return-val
  - ID: 3f7844bf
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/reflection/agent.py:392` - error: Incompatible return value type (got "Command[Never]", expected "dict[str, Any]") [return-val
  - ID: 1b5565e7
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/reflection/agent.py:398` - error: Incompatible return value type (got "Command[Never]", expected "dict[str, Any]") [return-val
  - ID: c4a79f98
- `packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/utils.py:21` - error: Incompatible return value type (got "Command[Never]", expected "dict[Any, Any]") [return-val
  - ID: e4535278
- ... and 2 more

### haive-core

- `packages/haive-core/src/haive/core/utils/model_utils.py:7` - error: Argument "pydantic_object" to "PydanticOutputParser" has incompatible type "BaseModel"; expec
  - ID: ab8f6e6c
- `packages/haive-core/src/haive/core/graph/node/agent_node_v2.py:275` - error: Incompatible types in assignment (expression has type "list[Never]", variable has type "dict[
  - ID: d7947ab3

### haive-games

- `packages/haive-games/src/haive/games/fox_and_geese/agent.py:147` - error: Incompatible return value type (got "Command[Never]", expected "dict[str, Any]") [return-val
  - ID: cacaec53

## mypy:Never, ... (2 errors)

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/background_process_manager.py:208` - error: Item "tuple[Never, ...]" of "addr | tuple[()]" has no attribute "port" [union-attr]
  - ID: 00d2ee26
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/background_process_manager.py:211` - error: Item "tuple[Never, ...]" of "addr | tuple[()]" has no attribute "ip" [union-attr]
  - ID: a3c1c520

## mypy:Never, Never (18 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_v3.py:174` - error: Incompatible types in assignment (expression has type "dict[Never, Never]", variable has type
  - ID: d244c5b2
- `packages/haive-agents/src/haive/agents/multi/enhanced/multi_agent_v3.py:221` - error: Incompatible types in assignment (expression has type "dict[Never, Never]", variable has type
  - ID: 6165cde4

### haive-core

- `packages/haive-core/src/haive/core/config/runnable.py:78` - error: Incompatible types in assignment (expression has type "dict[Never, Never]", target has type "
  - ID: cd751339
- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:238` - error: Incompatible types in assignment (expression has type "dict[Never, Never]", target has type "
  - ID: ae39a9b8
- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:242` - error: Incompatible types in assignment (expression has type "dict[Never, Never]", target has type "
  - ID: 7e71ec9d
- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:266` - error: Incompatible types in assignment (expression has type "dict[Never, Never]", target has type "
  - ID: f0f361f4
- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:270` - error: Incompatible types in assignment (expression has type "dict[Never, Never]", target has type "
  - ID: 8e1f352c
- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:353` - error: Incompatible types in assignment (expression has type "dict[Never, Never]", target has type "
  - ID: 451c0949
- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:373` - error: Incompatible types in assignment (expression has type "dict[Never, Never]", target has type "
  - ID: d6cb8e07
- `packages/haive-core/src/haive/core/graph/node/message_transformation.py:167` - error: Incompatible types in assignment (expression has type "dict[Never, Never]", target has type "
  - ID: 5bb5597e
- `packages/haive-core/src/haive/core/graph/node/message_transformation.py:171` - error: Incompatible types in assignment (expression has type "dict[Never, Never]", target has type "
  - ID: 8b92e398
- `packages/haive-core/src/haive/core/graph/node/message_transformation.py:195` - error: Incompatible types in assignment (expression has type "dict[Never, Never]", target has type "
  - ID: a3c0acc4
- ... and 6 more

## mypy:NodeStatus (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/graph/dynamic_graph_builder.py:1919` - error: "type[NodeStatus]" has no attribute "DEAD_END" [attr-defined]
  - ID: bc1c3b15

## mypy:None, int, None (1 errors)

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/enhance_mcp_data.py:159` - error: Invalid index type "slice[None, int, None]" for "dict[str, Any]"; expected type "str" [index
  - ID: f5e42f1e

## mypy:PathAnalyzer (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/document/loaders/path_analyzer.py:554` - error: "type[PathAnalyzer]" has no attribute "analyze_path" [attr-defined]
  - ID: 7d338574

## mypy:PegSpace (1 errors)

### haive-games

- `packages/haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:197` - error: The type "type[PegSpace]" is not generic and not indexable [misc]
  - ID: be5d965f

## mypy:Pinecone (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/models/vectorstore/base.py:75` - error: Incompatible types in assignment (expression has type "type[Pinecone]", variable has type "ty
  - ID: 8df30c02

## mypy:Player (1 errors)

### haive-games

- `packages/haive-games/src/haive/games/core/agent/game_config.py:27` - note: (Hint: Use "Generic[Player]" or "Protocol[Player]" base class to bind "Player" inside a class)
  - ID: 1645aa13

## mypy:PostgreSQLSource (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/document/loaders/sources/database_sources.py:321` - error: Argument 1 has incompatible type "type[PostgreSQLSource]"; expected "type[DatabaseSource]" [
  - ID: 36902dcc

## mypy:PostgresSaver, None, None (2 errors)

### haive-core

- `packages/haive-core/src/haive/core/persistence/postgres_saver_override.py:65` - note: def from_conn_string(conn_string: str, \*, pipeline: bool = ...) -> \_GeneratorContextM
  - ID: 80c9c730
- `packages/haive-core/src/haive/core/engine/agent/persistence/manager.py:150` - error: Incompatible types in assignment (expression has type "\_GeneratorContextManager[PostgresSaver
  - ID: d35a6fe6

## mypy:PostgresStoreWrapper (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/persistence/store/factory.py:18` - error: Incompatible types in assignment (expression has type "None", variable has type "type[Postgre
  - ID: 79588614

## mypy:ProSearchAgent (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_reorganized/__init__.py:71` - error: Incompatible types in assignment (expression has type "None", variable has type "type[ProSear
  - ID: dbe82b97

## mypy:Qdrant (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/models/vectorstore/base.py:91` - error: Incompatible types in assignment (expression has type "type[Qdrant]", variable has type "type
  - ID: b8f2bf2c

## mypy:QuickSearchAgent (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_reorganized/__init__.py:70` - error: Incompatible types in assignment (expression has type "None", variable has type "type[QuickSe
  - ID: 9146f4f3

## mypy:RAGStrategy, Any (5 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/rag/agentic_router/agent.py:443` - error: Value of type "dict[RAGStrategy, Any] | None" is not indexable [index]
  - ID: 08dd39e0
- `packages/haive-agents/src/haive/agents/rag/agentic_router/agent.py:449` - error: Value of type "dict[RAGStrategy, Any] | None" is not indexable [index]
  - ID: 47d51db3
- `packages/haive-agents/src/haive/agents/rag/agentic_router/agent.py:457` - error: Value of type "dict[RAGStrategy, Any] | None" is not indexable [index]
  - ID: c9ffa50f
- `packages/haive-agents/src/haive/agents/rag/agentic_router/agent.py:463` - error: Value of type "dict[RAGStrategy, Any] | None" is not indexable [index]
  - ID: 12ae3611
- `packages/haive-agents/src/haive/agents/rag/agentic_router/agent.py:469` - error: Value of type "dict[RAGStrategy, Any] | None" is not indexable [index]
  - ID: 08fcfbde

## mypy:ReactMemoryAgent (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_reorganized/__init__.py:45` - error: Incompatible types in assignment (expression has type "None", variable has type "type[ReactMe
  - ID: 66d0fa07

## mypy:Runnable[Any, Any (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/aug_llm/utils.py:208` - error: No overload variant of "chain" matches argument type "list[Runnable[Any, Any]]" [call-overlo
  - ID: 014a0131

## mypy:SQLiteSource (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/document/loaders/sources/database_sources.py:394` - error: Argument 1 has incompatible type "type[SQLiteSource]"; expected "type[DatabaseSource]" [arg-
  - ID: 77b1e53a

## mypy:Send (7 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/agent.py:563` - error: Incompatible return value type (got "list[Send] | str", expected "Literal['__end__'] | list[S
  - ID: 4bb73d65
- `packages/haive-agents/src/haive/agents/react_class/react_v2/agent.py:328` - error: Returning Any from function declared to return "str | list[Send]" [no-any-return]
  - ID: 08782058
- `packages/haive-agents/src/haive/agents/react_class/react_agent2/agent3.py:378` - error: Returning Any from function declared to return "str | list[Send] | Literal['END']" [no-any-r
  - ID: 1d235fa9

### haive-core

- `packages/haive-core/src/haive/core/graph/node/state_updating_validation_node.py:145` - error: Returning Any from function declared to return "list[Send] | str" [no-any-return]
  - ID: 4e5bbc10
- `packages/haive-core/src/haive/core/graph/node/routing_validation_node.py:79` - error: Returning Any from function declared to return "list[Send] | str" [no-any-return]
  - ID: 7798c6a4
- `packages/haive-core/src/haive/core/graph/node/routing_validation_node.py:234` - error: Returning Any from function declared to return "list[Send] | str" [no-any-return]
  - ID: 116eed41
- `packages/haive-core/src/haive/core/graph/node/routing_validation_node.py:260` - error: Returning Any from function declared to return "list[Send] | str" [no-any-return]
  - ID: 238d6997

## mypy:Send | str (28 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/multi/archive/agent.py:387` - error: Argument "goto" to "Command" has incompatible type "str | None"; expected "Send | Sequence[Se
  - ID: 2a59e946
- `packages/haive-agents/src/haive/agents/multi/archive/agent.py:646` - error: Argument "goto" to "Command" has incompatible type "str | None"; expected "Send | Sequence[Se
  - ID: ced253c8

### haive-core

- `packages/haive-core/src/haive/core/graph/node/multi_agent_node.py:69` - error: Argument "goto" to "Command" has incompatible type "str | None"; expected "Send | Sequence[Se
  - ID: fcbc4b6a
- `packages/haive-core/src/haive/core/graph/node/multi_agent_node.py:73` - error: Argument "goto" to "Command" has incompatible type "str | None"; expected "Send | Sequence[Se
  - ID: a93dae4e
- `packages/haive-core/src/haive/core/graph/node/callable_node.py:150` - error: Argument "goto" to "Command" has incompatible type "str | None"; expected "Send | Sequence[Se
  - ID: e006a8bb
- `packages/haive-core/src/haive/core/graph/node/agent_node_v3.py:351` - error: Argument "goto" to "Command" has incompatible type "str | None"; expected "Send | Sequence[Se
  - ID: c66a7e6f
- `packages/haive-core/src/haive/core/graph/node/agent_node_v3.py:358` - error: Argument "goto" to "Command" has incompatible type "str | None"; expected "Send | Sequence[Se
  - ID: 0d8c1faf
- `packages/haive-core/src/haive/core/graph/node/composer/node_schema_composer.py:447` - error: Argument "goto" to "Command" has incompatible type "Any | None"; expected "Send | Sequence[Se
  - ID: c0b04643
- `packages/haive-core/src/haive/core/graph/node/composer/integrated_node_composer.py:373` - error: Argument "goto" to "Command" has incompatible type "Any | None"; expected "Send | Sequence[Se
  - ID: bdf41196
- `packages/haive-core/src/haive/core/schema/state_schema.py:1616` - error: Argument "goto" to "Command" has incompatible type "str | None"; expected "Send | Sequence[Se
  - ID: 600b1417
- `packages/haive-core/src/haive/core/graph/graph_builder2.py:1146` - error: Incompatible return value type (got "Send | Sequence[Send | str]", expected "str") [return-v
  - ID: 8a06b98b
- `packages/haive-core/src/haive/core/graph/branches/branch.py:354` - error: Argument "goto" to "Command" has incompatible type "str | None"; expected "Send | Sequence[Se
  - ID: 233cfaab
- ... and 16 more

## mypy:Serializable (7 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/simple/config.v2.py:180` - error: Argument 1 to "from_messages" of "ChatPromptTemplate" has incompatible type "list[Serializabl
  - ID: beab61ab
- `packages/haive-agents/src/haive/agents/simple/config.py:177` - error: Argument 1 to "from_messages" of "ChatPromptTemplate" has incompatible type "list[Serializabl
  - ID: 15b16045
- `packages/haive-agents/src/haive/agents/react_class/react_v2/config.py:129` - error: Argument 1 to "from_messages" of "ChatPromptTemplate" has incompatible type "list[Serializabl
  - ID: cb93b3bc
- `packages/haive-agents/src/haive/agents/react_class/react_agent2/config2.py:197` - error: Argument 1 to "from_messages" of "ChatPromptTemplate" has incompatible type "list[Serializabl
  - ID: 091a3ba7
- `packages/haive-agents/src/haive/agents/react_class/react_agent2/example3.py:185` - error: Argument 1 to "from_messages" of "ChatPromptTemplate" has incompatible type "list[Serializabl
  - ID: 6b96c9aa
- `packages/haive-agents/src/haive/agents/react_class/react_agent2/agent.py:184` - error: Argument 1 to "from_messages" of "ChatPromptTemplate" has incompatible type "list[Serializabl
  - ID: 019309cf

### haive-core

- `packages/haive-core/src/haive/core/engine/aug_llm/config.py:727` - error: Argument 1 to "from_messages" of "ChatPromptTemplate" has incompatible type "list[Serializabl
  - ID: 83a070a3

## mypy:SimpleAgent (8 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_standalone.py:492` - error: Type argument "list[SimpleAgent]" of "MultiAgent" must be a subtype of "dict[str, Agent] | li
  - ID: aa8ff5cf
- `packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_standalone.py:492` - error: Type argument "list[SimpleAgent]" of "MultiAgent" must be a subtype of "dict[str, Agent] | li
  - ID: aa8ff5cf
- `packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_standalone.py:508` - error: Type argument "list[SimpleAgent]" of "MultiAgent" must be a subtype of "dict[str, Agent] | li
  - ID: e1943148
- `packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_standalone.py:508` - error: Type argument "list[SimpleAgent]" of "MultiAgent" must be a subtype of "dict[str, Agent] | li
  - ID: e1943148
- `packages/haive-agents/src/haive/agents/multi/archive/enhanced_multi_agent_standalone.py:492` - error: Type argument "list[SimpleAgent]" of "MultiAgent" must be a subtype of "dict[str, Agent] | li
  - ID: 79f2f235
- `packages/haive-agents/src/haive/agents/multi/archive/enhanced_multi_agent_standalone.py:492` - error: Type argument "list[SimpleAgent]" of "MultiAgent" must be a subtype of "dict[str, Agent] | li
  - ID: 79f2f235
- `packages/haive-agents/src/haive/agents/multi/archive/enhanced_multi_agent_standalone.py:508` - error: Type argument "list[SimpleAgent]" of "MultiAgent" must be a subtype of "dict[str, Agent] | li
  - ID: aa7ce40f
- `packages/haive-agents/src/haive/agents/multi/archive/enhanced_multi_agent_standalone.py:508` - error: Type argument "list[SimpleAgent]" of "MultiAgent" must be a subtype of "dict[str, Agent] | li
  - ID: aa7ce40f

## mypy:SimpleMemoryAgent (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_reorganized/__init__.py:44` - error: Incompatible types in assignment (expression has type "None", variable has type "type[SimpleM
  - ID: eef4e7d9

## mypy:SnowflakeSource (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/document/loaders/sources/database_sources.py:696` - error: Argument 1 has incompatible type "type[SnowflakeSource]"; expected "type[DatabaseSource]" [a
  - ID: d4310b47

## mypy:Step (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/planning/plan_and_execute/models.py:32` - error: Argument 2 to "map" has incompatible type "list[Step] | None"; expected "Iterable[Step]" [ar
  - ID: b80f561a

## mypy:StepStatus (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/planning/plan_execute_v3/engines.py:277` - error: "type[StepStatus]" has no attribute "RUNNING" [attr-defined]
  - ID: ec8f5996

## mypy:StructuredTool (9 errors)

### haive-core

- `packages/haive-core/src/haive/core/utils/tools/tool_schema_generator.py:30` - error: Incompatible types in assignment (expression has type "None", variable has type "type[Structu
  - ID: cab45115
- `packages/haive-core/src/haive/core/engine/tool/base.py:148` - error: Incompatible return value type (got "list[StructuredTool]", expected "list[BaseTool | Tool |
  - ID: e83ab1d9

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:316` - error: Returning Any from function declared to return "list[StructuredTool]" [no-any-return]
  - ID: cdc28d0b

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/rps_101_toolkit.py:164` - error: Return type "list[StructuredTool]" of "get_tools" incompatible with return type "list[BaseToo
  - ID: 8f23f64a
- `packages/haive-tools/src/haive/tools/tools/toolkits/rick_and_morty_toolkit.py:288` - error: Return type "list[StructuredTool]" of "get_tools" incompatible with return type "list[BaseToo
  - ID: 2f61c524
- `packages/haive-tools/src/haive/tools/tools/toolkits/lcbo_toolkit.py:117` - error: Return type "list[StructuredTool]" of "get_tools" incompatible with return type "list[BaseToo
  - ID: ac48cd01
- `packages/haive-tools/src/haive/tools/tools/toolkits/free_to_game_toolkit.py:163` - error: Return type "list[StructuredTool]" of "get_tools" incompatible with return type "list[BaseToo
  - ID: 5e860ad7
- `packages/haive-tools/src/haive/tools/tools/toolkits/fred_toolkit.py:213` - error: Return type "list[StructuredTool]" of "get_tools" incompatible with return type "list[BaseToo
  - ID: 11961550
- `packages/haive-tools/src/haive/tools/tools/toolkits/citydsk_toolkit.py:130` - error: Return type "list[StructuredTool]" of "get_tools" incompatible with return type "list[BaseToo
  - ID: f509e1a8

## mypy:SystemMessage (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/planning/llm_compiler/tools/math_tools.py:118` - error: Incompatible types in assignment (expression has type "list[SystemMessage]", target has type
  - ID: 3c59ce6d

## mypy:T (42 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/planning/base/models.py:310` - error: Incompatible default for argument "items" (default has type "None", argument has type "list[T
  - ID: d8c7be33

### haive-core

- `packages/haive-core/src/haive/core/registry/decorators.py:95` - error: "type[T]" has no attribute "register_instance" [attr-defined]
  - ID: 2362eb03
- `packages/haive-core/src/haive/core/registry/decorators.py:98` - error: "type[T]" has no attribute "**registry_info**" [attr-defined]
  - ID: a202bc84
- `packages/haive-core/src/haive/core/types/tree_leaf.py:48` - error: "NodeMixin[T]" has no attribute "children" [attr-defined]
  - ID: f1b24746
- `packages/haive-core/src/haive/core/types/tree_leaf.py:52` - note: (Hint: Use "Generic[T]" or "Protocol[T]" base class to bind "T" inside a class)
  - ID: e62382d2
- `packages/haive-core/src/haive/core/types/tree_leaf.py:53` - note: (Hint: Use "Generic[T]" or "Protocol[T]" base class to bind "T" inside a class)
  - ID: 3ca03410
- `packages/haive-core/src/haive/core/registry/dynamic_registry.py:548` - error: Item "RegistryItem[T]" of "RegistryItem[T] | dict[Never, Never]" has no attribute "get" [uni
  - ID: 205b657c
- `packages/haive-core/src/haive/core/common/models/named_list.py:76` - error: Argument 1 to "process_single_item" of "NamedList" has incompatible type "Sequence[T]"; expec
  - ID: 09f1fcaf
- `packages/haive-core/src/haive/core/common/models/named_list.py:93` - error: "Sequence[T]" has no attribute "append" [attr-defined]
  - ID: faca1975
- `packages/haive-core/src/haive/core/common/models/named_list.py:96` - error: "Sequence[T]" has no attribute "append" [attr-defined]
  - ID: 5120ccd0
- `packages/haive-core/src/haive/core/common/models/named_list.py:110` - error: "Sequence[T]" has no attribute "append" [attr-defined]
  - ID: 1c11f5f5
- ... and 16 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/registry/base.py:73` - error: "Registry[T]" has no attribute "entries" [attr-defined]
  - ID: dafeb0a6
- `packages/haive-dataflow/src/haive/dataflow/registry/base.py:75` - error: "Registry[T]" has no attribute "\_disabled_discovery" [attr-defined]
  - ID: bddbb4b8
- `packages/haive-dataflow/src/haive/dataflow/registry/base.py:133` - error: "Registry[T]" has no attribute "entries" [attr-defined]
  - ID: adde1eab
- `packages/haive-dataflow/src/haive/dataflow/registry/base.py:189` - error: "Registry[T]" has no attribute "\_disabled_discovery" [attr-defined]
  - ID: 27c01a03
- `packages/haive-dataflow/src/haive/dataflow/registry/base.py:193` - error: "Registry[T]" has no attribute "entries" [attr-defined]
  - ID: 156bf17f
- `packages/haive-dataflow/src/haive/dataflow/registry/base.py:195` - error: Returning Any from function declared to return "type[T] | None" [no-any-return]
  - ID: c8f95327
- `packages/haive-dataflow/src/haive/dataflow/registry/base.py:205` - error: Returning Any from function declared to return "type[T] | None" [no-any-return]
  - ID: 1289141c
- `packages/haive-dataflow/src/haive/dataflow/registry/base.py:242` - error: "Registry[T]" has no attribute "entries" [attr-defined]
  - ID: 20d4bba2
- `packages/haive-dataflow/src/haive/dataflow/registry/base.py:244` - error: Returning Any from function declared to return "type[T] | None" [no-any-return]
  - ID: 58a808d5
- `packages/haive-dataflow/src/haive/dataflow/registry/base.py:286` - error: "Registry[T]" has no attribute "\_disabled_discovery" [attr-defined]
  - ID: 3d1720a7
- ... and 5 more

## mypy:TCard | None (1 errors)

### haive-games

- `packages/haive-games/src/haive/games/core/components/cards/base.py:106` - error: List comprehension has incompatible type List[TCard | None]; expected List[TCard] [misc]
  - ID: d95850d4

## mypy:TNode (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/graph/state_graph/state_graph.py:467` - note: def validate(cls, value: Any) -> StateGraphSerializable[TNode]
  - ID: ee8974b6

## mypy:Task (3 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/planning/llm_compiler/output_parser.py:106` - error: Return type "Iterator[Task]" of "\_transform" incompatible with return type "Iterator[dict[Any
  - ID: 6569b91d
- `packages/haive-agents/src/haive/agents/planning/llm_compiler/output_parser.py:121` - error: Return type "list[Task]" of "parse" incompatible with return type "dict[Any, Any]" in superty
  - ID: 5621d2bb
- `packages/haive-agents/src/haive/agents/planning/llm_compiler/output_parser.py:124` - error: Return type "Iterator[Task]" of "stream" incompatible with return type "Iterator[dict[Any, An
  - ID: 9d50219e

## mypy:TavilySearchResults (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/research/open_perplexity/structured_tools.py:26` - error: Incompatible types in assignment (expression has type "None", variable has type "type[TavilyS
  - ID: 7f00bfd5

## mypy:TestResult | BaseException (1 errors)

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/tools/server_tester.py:321` - error: Incompatible return value type (got "list[TestResult | BaseException]", expected "list[TestRe
  - ID: 311c01db

## mypy:TextIO | Any (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/common/logging_config.py:171` - error: Incompatible types in assignment (expression has type "StreamHandler[TextIO | Any]", variable
  - ID: ce583960

## mypy:TextResult (1 errors)

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/translate_tools.py:186` - error: Item "list[TextResult]" of "TextResult | list[TextResult]" has no attribute "text" [union-at
  - ID: 3701a06a

## mypy:ToolCall (9 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/react_class/react_agent2/tool_utils.py:36` - error: Incompatible return value type (got "list[ToolCall]", expected "list[dict[str, Any]]") [retu
  - ID: 3426aa25

### haive-core

- `packages/haive-core/src/haive/core/schema/prebuilt/messages/utils.py:123` - error: Incompatible return value type (got "list[ToolCall]", expected "list[dict[str, Any]]") [retu
  - ID: ba0a98d6
- `packages/haive-core/src/haive/core/graph/node/state_updating_validation_node.py:199` - error: Incompatible return value type (got "list[ToolCall]", expected "list[dict[str, Any]]") [retu
  - ID: 1537310b
- `packages/haive-core/src/haive/core/graph/node/routing_validation_node.py:163` - error: Incompatible return value type (got "list[ToolCall]", expected "list[dict[str, Any]]") [retu
  - ID: cca5eb5e
- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:380` - error: Incompatible types in assignment (expression has type "list[ToolCall]", target has type "str
  - ID: 9f8e5b1d
- `packages/haive-core/src/haive/core/graph/node/message_transformation.py:309` - error: Incompatible types in assignment (expression has type "list[ToolCall]", target has type "str
  - ID: dee8736d
- `packages/haive-core/src/haive/core/schema/prebuilt/messages_state.py:294` - error: Incompatible return value type (got "list[ToolCall]", expected "list[dict[Any, Any]]") [retu
  - ID: 6b9e1369
- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:521` - error: Incompatible return value type (got "list[ToolCall] | Any", expected "list[dict[Any, Any]]")
  - ID: ee5ef18e
- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:674` - error: Argument 1 to "extend" of "list" has incompatible type "list[ToolCall]"; expected "Iterable[d
  - ID: b1554639

## mypy:ToolExecutorState (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/schema/base_state_schemas.py:425` - error: Incompatible return value type (got "type[ToolExecutorState]", expected "type[AgentState]")
  - ID: e3c16f0f

## mypy:ToolMessage (2 errors)

### haive-core

- `packages/haive-core/src/haive/core/graph/node/stateful_validation_node.py:182` - error: Incompatible types in assignment (expression has type "list[ToolMessage]", target has type "l
  - ID: e286784f
- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:478` - error: Argument 1 to "extend" of "list" has incompatible type "list[ToolMessage]"; expected "Iterabl
  - ID: a412c553

## mypy:ToolNode (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/utils/tools/tool_schema_generator.py:32` - error: Incompatible types in assignment (expression has type "None", variable has type "type[ToolNod
  - ID: b0a25758

## mypy:True (2 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/simple/agent_v3.py:715` - error: Argument 4 to "\_add_validation_nodes" of "SimpleAgentV3" has incompatible type "Literal[True]
  - ID: 872b544e
- `packages/haive-agents/src/haive/agents/simple/agent_v3.py:1407` - error: Argument 4 to "\_add_complex_routing" of "SimpleAgentV3" has incompatible type "Literal[True]
  - ID: 2d3effab

## mypy:TwitterTweetLoader (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/document/loaders/specific/web_social.py:167` - error: "type[TwitterTweetLoader]" has no attribute "from_username" [attr-defined]
  - ID: 1620c7fc

## mypy:TypeReference | None (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/graph/common/references.py:190` - error: List comprehension has incompatible type List[TypeReference | None]; expected List[TypeRefere
  - ID: 5f53f2d8

## mypy:Weaviate (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/models/vectorstore/base.py:79` - error: Incompatible types in assignment (expression has type "type[Weaviate]", variable has type "ty
  - ID: b5d07662

## mypy:Zilliz (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/models/vectorstore/base.py:83` - error: Incompatible types in assignment (expression has type "type[Zilliz]", variable has type "type
  - ID: 7d715bdd

## mypy:[ (25 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/research/perplexity/pro_search/models.py:78` - error: Argument "default_factory" to "Field" has incompatible type "Callable[[], list[str]]"; expect
  - ID: 90ddaf13
- `packages/haive-agents/src/haive/agents/research/perplexity/pro_search/tasks/models.py:130` - error: Argument "default_factory" to "Field" has incompatible type "Callable[[], list[str]]"; expect
  - ID: 0d43692c
- `packages/haive-agents/src/haive/agents/document_modifiers/tnt/engines.py:78` - error: Argument "summary_length" to "partial" of "BasePromptTemplate" has incompatible type "int"; e
  - ID: 8d62dda1
- `packages/haive-agents/src/haive/agents/document_modifiers/tnt/engines.py:78` - error: Argument "summary_length" to "partial" of "BasePromptTemplate" has incompatible type "int"; e
  - ID: 8d62dda1

### haive-core

- `packages/haive-core/src/haive/core/graph/state_graph/models/state_graph_model.py:41` - error: Argument "default_factory" to "Field" has incompatible type "Callable[[], defaultdict[Never,
  - ID: 02e94b14
- `packages/haive-core/src/haive/core/engine/document/sources/local.py:74` - error: Invalid index type "Callable[[], str]" for "dict[str, str]"; expected type "str" [index]
  - ID: c1bb6d8a
- `packages/haive-core/src/haive/core/engine/document/sources/local.py:86` - error: "Callable[[], datetime]" has no attribute "isoformat" [attr-defined]
  - ID: e219d1a0
- `packages/haive-core/src/haive/core/engine/document/sources/local.py:155` - error: "Callable[[], datetime]" has no attribute "isoformat" [attr-defined]
  - ID: a2831f11
- `packages/haive-core/src/haive/core/schema/schema_composer.py:1070` - error: Argument "default_factory" to "add_field" of "SchemaComposer" has incompatible type "Callable
  - ID: b78c90f0
- `packages/haive-core/src/haive/core/schema/field_utils.py:702` - error: No overload variant of "Field" matches argument types "Callable[[], T]", "dict[str, str]" [c
  - ID: 4a7adde9
- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:913` - error: Incompatible return value type (got "Callable[[], AIMessage | HumanMessage | ChatMessage | Sy
  - ID: d1a0dd5f
- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:918` - error: Incompatible return value type (got "Callable[[], HumanMessage | None]", expected "HumanMessa
  - ID: c05a2470
- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:923` - error: Incompatible return value type (got "Callable[[], AIMessage | None]", expected "AIMessage | N
  - ID: fc569abd
- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:928` - error: Incompatible return value type (got "Callable[[], HumanMessage | None]", expected "HumanMessa
  - ID: 15b75642
- ... and 5 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/registry/lazy_core.py:192` - error: "Callable[[], LazyRegistrySystem]" has no attribute "\_instance" [attr-defined]
  - ID: 707994bc
- `packages/haive-dataflow/src/haive/dataflow/registry/lazy_core.py:193` - error: "Callable[[], LazyRegistrySystem]" has no attribute "\_instance" [attr-defined]
  - ID: 555a3691

### haive-games

- `packages/haive-games/src/haive/games/go/state.py:72` - error: Argument "default_factory" to "Field" has incompatible type "Callable[[], dict[str, int]]"; e
  - ID: 2186b406
- `packages/haive-games/src/haive/games/chess/state.py:92` - error: Argument "default_factory" to "Field" has incompatible type "Callable[[], dict[str, list[Neve
  - ID: cd247e25
- `packages/haive-games/src/haive/games/checkers/state.py:225` - error: Argument "default_factory" to "Field" has incompatible type "Callable[[], list[list[int]]]";
  - ID: 66a2d442
- `packages/haive-games/src/haive/games/checkers/state.py:267` - error: Argument "default_factory" to "Field" has incompatible type "Callable[[], dict[str, list[Neve
  - ID: 4317efb8

## mypy:[<parameters> (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/graph/gb/__init__.py:21` - error: Please use "Callable[[<parameters>], <return type>]" or "Callable" [misc]
  - ID: 9903d243

## mypy:[Any, RunnableConfig | None (9 errors)

### haive-core

- `packages/haive-core/src/haive/core/graph/NodeFactory.py:484` - error: Incompatible return value type (got "Callable[[Any, RunnableConfig | None], Any]", expected "
  - ID: 2c8a3089
- `packages/haive-core/src/haive/core/graph/NodeFactory.py:659` - error: Incompatible return value type (got "Callable[[Any, RunnableConfig | None], Any]", expected "
  - ID: d12f8787
- `packages/haive-core/src/haive/core/graph/NodeFactory.py:711` - error: Incompatible return value type (got "Callable[[Any, RunnableConfig | None], Any]", expected "
  - ID: d26b7c27
- `packages/haive-core/src/haive/core/graph/NodeFactory.py:780` - error: Incompatible return value type (got "Callable[[Any, RunnableConfig | None], Any]", expected "
  - ID: 4005438c
- `packages/haive-core/src/haive/core/graph/NodeFactory.py:849` - error: Incompatible return value type (got "Callable[[Any, RunnableConfig | None], Any]", expected "
  - ID: b43a96a8
- `packages/haive-core/src/haive/core/graph/NodeFactory.py:897` - error: Incompatible return value type (got "Callable[[Any, RunnableConfig | None], Any]", expected "
  - ID: 95554413
- `packages/haive-core/src/haive/core/graph/NodeFactory.py:954` - error: Incompatible return value type (got "Callable[[Any, RunnableConfig | None], Any]", expected "
  - ID: d1b54577
- `packages/haive-core/src/haive/core/graph/NodeFactory.py:1037` - error: Incompatible return value type (got "Callable[[Any, RunnableConfig | None], Any]", expected "
  - ID: 144739c8
- `packages/haive-core/src/haive/core/graph/NodeFactory.py:1125` - error: Incompatible return value type (got "Callable[[Any, RunnableConfig | None], Any]", expected "
  - ID: 723890dc

## mypy:[Arg(Any, 'state'), DefaultArg(dict[str, Any (9 errors)

### haive-core

- `packages/haive-core/src/haive/core/graph/NodeFactory.py:484` - note: "NodeFunction.**call**" has type "Callable[[Arg(Any, 'state'), DefaultArg(dict[str, Any] | Non
  - ID: 75e4a873
- `packages/haive-core/src/haive/core/graph/NodeFactory.py:659` - note: "NodeFunction.**call**" has type "Callable[[Arg(Any, 'state'), DefaultArg(dict[str, Any] | Non
  - ID: ff8cc311
- `packages/haive-core/src/haive/core/graph/NodeFactory.py:711` - note: "NodeFunction.**call**" has type "Callable[[Arg(Any, 'state'), DefaultArg(dict[str, Any] | Non
  - ID: 4a3200a5
- `packages/haive-core/src/haive/core/graph/NodeFactory.py:780` - note: "NodeFunction.**call**" has type "Callable[[Arg(Any, 'state'), DefaultArg(dict[str, Any] | Non
  - ID: f0f7ecd6
- `packages/haive-core/src/haive/core/graph/NodeFactory.py:849` - note: "NodeFunction.**call**" has type "Callable[[Arg(Any, 'state'), DefaultArg(dict[str, Any] | Non
  - ID: 8295d2aa
- `packages/haive-core/src/haive/core/graph/NodeFactory.py:897` - note: "NodeFunction.**call**" has type "Callable[[Arg(Any, 'state'), DefaultArg(dict[str, Any] | Non
  - ID: ec1947b2
- `packages/haive-core/src/haive/core/graph/NodeFactory.py:954` - note: "NodeFunction.**call**" has type "Callable[[Arg(Any, 'state'), DefaultArg(dict[str, Any] | Non
  - ID: 1434d0ac
- `packages/haive-core/src/haive/core/graph/NodeFactory.py:1037` - note: "NodeFunction.**call**" has type "Callable[[Arg(Any, 'state'), DefaultArg(dict[str, Any] | Non
  - ID: 50d025de
- `packages/haive-core/src/haive/core/graph/NodeFactory.py:1125` - note: "NodeFunction.**call**" has type "Callable[[Arg(Any, 'state'), DefaultArg(dict[str, Any] | Non
  - ID: 74e8720f

## mypy:[BaseException, dict[str, Any (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/agent.py:655` - error: Argument "format_error" to "ValidationNode" has incompatible type "Callable[[BaseException, d
  - ID: 1b243488

## mypy:[BaseModel (6 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_reorganized/retrieval/enhanced_retriever.py:562` - error: Unsupported right operand type for in ("Callable[[BaseModel], dict[str, FieldInfo]]") [opera
  - ID: 0311fc1b
- `packages/haive-agents/src/haive/agents/memory/enhanced_retriever.py:536` - error: Unsupported right operand type for in ("Callable[[BaseModel], dict[str, FieldInfo]]") [opera
  - ID: b5184fbb

### haive-core

- `packages/haive-core/src/haive/core/graph/StateSchema.py:83` - error: "Callable[[BaseModel], dict[str, FieldInfo]]" has no attribute "items" [attr-defined]
  - ID: 0e3662f3
- `packages/haive-core/src/haive/core/engine/agent/utils/input_handling.py:39` - error: Incompatible types in assignment (expression has type "Callable[[BaseModel], dict[str, FieldI
  - ID: 2ec8bc41

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/serialization.py:328` - error: "Callable[[BaseModel], dict[str, FieldInfo]]" has no attribute "items" [attr-defined]
  - ID: 5351cf7e
- `packages/haive-dataflow/src/haive/dataflow/registry/serialization.py:409` - error: "Callable[[BaseModel], dict[str, FieldInfo]]" has no attribute "items" [attr-defined]
  - ID: cc9e3605

## mypy:[ChatPromptValue, RunnableConfig (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/agent.py:206` - error: Unsupported operand types for | ("ChatPromptTemplate" and "Callable[[ChatPromptValue, Runnabl
  - ID: 6e239846

## mypy:[JudgeScore (1 errors)

### haive-games

- `packages/haive-games/src/haive/games/debate_v2/judges.py:421` - note: def sort(self, \*, key: Callable[[JudgeScore], SupportsDunderLT[Any] | SupportsDunderGT[Any
  - ID: 6b70864d

## mypy:[StartupIdea (1 errors)

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:438` - error: Argument "key" to "sorted" has incompatible type "Callable[[StartupIdea], float | Any | None]
  - ID: 5df7fd6d

## mypy:[VarArg(Any), KwArg(Any) (3 errors)

### haive-core

- `packages/haive-core/src/haive/core/utils/debugkit/core/unified.py:539` - error: "\_Wrapped[[VarArg(Any), KwArg(Any)], Any, [VarArg(Any), KwArg(Any)], Any]" has no attribute "
  - ID: 7d3d5d7b
- `packages/haive-core/src/haive/core/schema/compatibility/utils.py:339` - error: "\_Wrapped[[VarArg(Any), KwArg(Any)], T, [VarArg(Any), KwArg(Any)], Any]" has no attribute "ca
  - ID: 895cd5cc
- `packages/haive-core/src/haive/core/schema/compatibility/utils.py:340` - error: "\_Wrapped[[VarArg(Any), KwArg(Any)], T, [VarArg(Any), KwArg(Any)], Any]" has no attribute "cl
  - ID: c3ac6f1a

## mypy:[bool, str (4 errors)

### haive-core

- `packages/haive-core/src/haive/core/graph/state_graph/state_graph.py:62` - error: Incompatible types in assignment (expression has type "Any | None", base class "BaseModel" de
  - ID: 1cc346a4
- `packages/haive-core/src/haive/core/engine/document/loaders/sources/database_sources.py:720` - error: Incompatible types in assignment (expression has type "str | None", base class "BaseModel" de
  - ID: 0e5540bf
- `packages/haive-core/src/haive/core/engine/document/loaders/sources/analytics_sources.py:133` - error: Incompatible types in assignment (expression has type "str", base class "BaseModel" defined t
  - ID: 7e49081d
- `packages/haive-core/src/haive/core/engine/document/loaders/sources/analytics_sources.py:222` - error: Incompatible types in assignment (expression has type "str", base class "BaseModel" defined t
  - ID: f08ac7b6

## mypy:[dict[Any, Any (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/document/loaders/specific/web_api.py:127` - error: Argument "dataset_mapping_function" to "ApifyDatasetLoader" has incompatible type "callable?
  - ID: adafc1cf

## mypy:[dict[str, Any (14 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/agent.py:148` - error: Argument 1 to "RunnableLambda" has incompatible type "Callable[[dict[str, Any]], Coroutine[An
  - ID: 462430f1
- `packages/haive-agents/src/haive/agents/agent.py:195` - error: Argument 1 to "RunnableLambda" has incompatible type "Callable[[dict[str, Any]], Coroutine[An
  - ID: adb41840

### haive-core

- `packages/haive-core/src/haive/core/graph/node/factory.py:115` - error: "Callable[[dict[str, Any], dict[str, Any] | None], Any]" has no attribute "**node_config**"
  - ID: dc6a8175
- `packages/haive-core/src/haive/core/graph/node/factory.py:116` - error: "Callable[[dict[str, Any], dict[str, Any] | None], Any]" has no attribute "**engine_id**" [a
  - ID: 5de91ace
- `packages/haive-core/src/haive/core/graph/node/factory.py:175` - error: "Callable[[dict[str, Any], dict[str, Any] | None], Any]" has no attribute "**node_config**"
  - ID: 65f7ada9
- `packages/haive-core/src/haive/core/graph/node/factory.py:176` - error: "Callable[[dict[str, Any], dict[str, Any] | None], Any]" has no attribute "**engine_id**" [a
  - ID: 94df230b
- `packages/haive-core/src/haive/core/graph/node/factory.py:286` - error: "Callable[[dict[str, Any], dict[str, Any] | None], Any]" has no attribute "ainvoke" [attr-de
  - ID: 7b8a4bcc
- `packages/haive-core/src/haive/core/graph/node/factory.py:289` - error: "Callable[[dict[str, Any], dict[str, Any] | None], Any]" has no attribute "**node_config**"
  - ID: e1163436
- `packages/haive-core/src/haive/core/graph/node/factory.py:406` - error: "Callable[[dict[str, Any], dict[str, Any] | None], Any]" has no attribute "ainvoke" [attr-de
  - ID: 3c03a939
- `packages/haive-core/src/haive/core/graph/node/factory.py:409` - error: "Callable[[dict[str, Any], dict[str, Any] | None], Any]" has no attribute "**node_config**"
  - ID: 746fa5b3
- `packages/haive-core/src/haive/core/graph/node/factory.py:485` - error: "Callable[[dict[str, Any], dict[str, Any] | None], Any]" has no attribute "**node_config**"
  - ID: 81a07a4c
- `packages/haive-core/src/haive/core/graph/node/factory.py:553` - error: "Callable[[dict[str, Any], dict[str, Any] | None], Any]" has no attribute "**node_config**"
  - ID: 52193ac3
- ... and 2 more

## mypy:[dict[str, object (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_v2/graph_memory_agent.py:580` - error: Argument "key" to "sort" of "list" has incompatible type "Callable[[dict[str, object]], objec
  - ID: 5960e2cb

## mypy:[list[BaseMessage | list[str (2 errors)

### haive-core

- `packages/haive-core/src/haive/core/schema/state_schema.py:1187` - error: Incompatible types in assignment (expression has type overloaded function, target has type "C
  - ID: 893ff1a9
- `packages/haive-core/src/haive/core/schema/state_schema.py:1188` - error: Incompatible types in assignment (expression has type overloaded function, target has type "C
  - ID: 61df9e18

## mypy:[object (2 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/planning/plan_and_execute/models.py:32` - error: Argument 1 to "filter" has incompatible type "Callable[[object], bool]"; expected "Callable[[
  - ID: 1f157d03
- `packages/haive-agents/src/haive/agents/planning/plan_and_execute/models.py:32` - error: Argument 1 to "filter" has incompatible type "Callable[[object], bool]"; expected "Callable[[
  - ID: 1f157d03

## mypy:[str (1 errors)

### haive-games

- `packages/haive-games/src/haive/games/checkers/example.py:496` - error: Argument "key" to "min" has incompatible type "Callable[[str], object]"; expected "Callable[[
  - ID: bea4abb3

## mypy:[str, FieldInfo (62 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/tot_multi_agent.py:35` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: a5222bc0
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/tot_multi_agent.py:35` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: a5222bc0
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/models.py:142` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: 149749f8
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/models.py:142` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: 149749f8
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/models.py:257` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: 55592f1f
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/models.py:257` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: 55592f1f
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/agents/solution_scorer.py:30` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: 51a9e2ad
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/agents/solution_scorer.py:30` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: 51a9e2ad
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/agents/candidate_generator.py:19` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: 3bcc684d
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/agents/candidate_generator.py:19` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: 3bcc684d
- ... and 12 more

### haive-core

- `packages/haive-core/src/haive/core/schema/field_utils.py:702` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: b5271a46
- `packages/haive-core/src/haive/core/schema/field_utils.py:702` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: b5271a46
- `packages/haive-core/src/haive/core/schema/field_utils.py:704` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: 0150822d
- `packages/haive-core/src/haive/core/schema/field_utils.py:704` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: 0150822d
- `packages/haive-core/src/haive/core/engine/retriever/providers/MergerRetrieverConfig.py:70` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: eaafc62a
- `packages/haive-core/src/haive/core/engine/retriever/providers/MergerRetrieverConfig.py:70` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: eaafc62a
- `packages/haive-core/src/haive/core/engine/retriever/providers/EnsembleRetrieverConfig.py:72` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: b2e90320
- `packages/haive-core/src/haive/core/engine/retriever/providers/EnsembleRetrieverConfig.py:72` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: b2e90320

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/base.py:139` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: 2a685ad6
- `packages/haive-dataflow/src/haive/dataflow/base.py:139` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: 2a685ad6
- `packages/haive-dataflow/src/haive/dataflow/api/base.py:139` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: c7637b5e
- `packages/haive-dataflow/src/haive/dataflow/api/base.py:139` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: c7637b5e
- `packages/haive-dataflow/src/haive/dataflow/api/routes/llm_routes.py:114` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: 07636ca2
- `packages/haive-dataflow/src/haive/dataflow/api/routes/llm_routes.py:114` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: 07636ca2

### haive-games

- `packages/haive-games/src/haive/games/mastermind/state.py:96` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: 8663aaa3
- `packages/haive-games/src/haive/games/mastermind/state.py:96` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: 8663aaa3
- `packages/haive-games/src/haive/games/mastermind/models.py:163` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: f1595559
- `packages/haive-games/src/haive/games/mastermind/models.py:163` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: f1595559
- `packages/haive-games/src/haive/games/mastermind/models.py:240` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: f3f6fff6
- `packages/haive-games/src/haive/games/mastermind/models.py:240` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: f3f6fff6
- `packages/haive-games/src/haive/games/dominoes/state.py:190` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: ffbc9f8e
- `packages/haive-games/src/haive/games/dominoes/state.py:190` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: ffbc9f8e

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:143` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: d173ff7a
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:143` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: d173ff7a
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:176` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: fe52ed60
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:176` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: fe52ed60
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:177` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: 11dec08a
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:177` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: 11dec08a
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:200` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: 02c383ef
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:200` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: 02c383ef
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:201` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: b4a42551
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:201` - note: def Field(default: EllipsisType, \*, alias: str | None = ..., alias_priority: int | None =
  - ID: b4a42551
- ... and 8 more

## mypy:[type[HexPosition (1 errors)

### haive-games

- `packages/haive-games/src/haive/games/core/game/core_position.py:194` - error: Value of type variable "\_V2BeforeAfterOrPlainValidatorType" of function cannot be "Callable[[
  - ID: 2d7ab2f0

## mypy:\_KT, \_VT (16 errors)

### haive-core

- `packages/haive-core/src/haive/core/utils/haive_discovery/utils.py:421` - note: def [_KT, _VT] dict(self) -> dict[_KT, _VT]
  - ID: 586bfa17
- `packages/haive-core/src/haive/core/utils/haive_discovery/utils.py:421` - note: def [_KT, _VT] dict(self) -> dict[_KT, _VT]
  - ID: 586bfa17
- `packages/haive-core/src/haive/core/utils/haive_discovery/utils.py:421` - note: def [_KT, _VT] dict(self) -> dict[_KT, _VT]
  - ID: 586bfa17
- `packages/haive-core/src/haive/core/utils/haive_discovery/utils.py:421` - note: def [_KT, _VT] dict(self) -> dict[_KT, _VT]
  - ID: 586bfa17
- `packages/haive-core/src/haive/core/utils/haive_discovery/utils.py:421` - note: def [_KT, _VT] dict(self) -> dict[_KT, _VT]
  - ID: 586bfa17
- `packages/haive-core/src/haive/core/utils/haive_discovery/utils.py:421` - note: def [_KT, _VT] dict(self) -> dict[_KT, _VT]
  - ID: 586bfa17
- `packages/haive-core/src/haive/core/utils/haive_discovery/utils.py:421` - note: def [_KT, _VT] dict(self) -> dict[_KT, _VT]
  - ID: 586bfa17
- `packages/haive-core/src/haive/core/utils/haive_discovery/utils.py:421` - note: def [_KT, _VT] dict(self) -> dict[_KT, _VT]
  - ID: 586bfa17
- `packages/haive-core/src/haive/core/utils/haive_discovery/utils.py:422` - note: def [_KT, _VT] dict(self) -> dict[_KT, _VT]
  - ID: 2d2b6c87
- `packages/haive-core/src/haive/core/utils/haive_discovery/utils.py:422` - note: def [_KT, _VT] dict(self) -> dict[_KT, _VT]
  - ID: 2d2b6c87
- ... and 6 more

## mypy:\_S (5 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/models.py:126` - note: def [_S] **add**(self, list[_S], /) -> list[_S | Any]
  - ID: 554e9a47
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/modular/state.py:37` - note: def [_S] **add**(self, list[_S], /) -> list[_S | Any]
  - ID: 5daadd8f

### haive-core

- `packages/haive-core/src/haive/core/schema/state_schema.py:1213` - note: def [_S] **add**(self, list[_S], /) -> list[_S | Any]
  - ID: 6e974425
- `packages/haive-core/src/haive/core/schema/field_utils.py:955` - note: def [_S] **add**(self, list[_S], /) -> list[_S | Any]
  - ID: 75780dcc

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:332` - note: def [_S] **add**(self, list[_S], /) -> list[\_S | str | dict[Any, Any]]
  - ID: 40e0a2bd

## mypy:\_T (67 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/tot_multi_agent.py:35` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: ae9523f1
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/tot_multi_agent.py:35` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: ae9523f1
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/models.py:142` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: e13f78c5
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/models.py:142` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: e13f78c5
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/models.py:257` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 19f30367
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/models.py:257` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 19f30367
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/agents/solution_scorer.py:30` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 4c75dfec
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/agents/solution_scorer.py:30` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 4c75dfec
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/agents/candidate_generator.py:19` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: ba1c6ec2
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/agents/candidate_generator.py:19` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: ba1c6ec2
- ... and 12 more

### haive-core

- `packages/haive-core/src/haive/core/registry/dynamic_registry.py:548` - note: def [_T] get(self, Never, \_T, /) -> \_T
  - ID: c58b4970
- `packages/haive-core/src/haive/core/schema/compatibility/langchain_converters.py:69` - note: def [_T] get(self, ModelMetaclass, \_T, /) -> int | \_T
  - ID: 7552b73f
- `packages/haive-core/src/haive/core/schema/compatibility/langchain_converters.py:70` - note: def [_T] get(self, ModelMetaclass, \_T, /) -> int | \_T
  - ID: 59c042ac
- `packages/haive-core/src/haive/core/schema/state_schema.py:1213` - note: def [_T] **add**(self, tuple[_T, ...], /) -> tuple[Any | _T, ...]
  - ID: 12c56164
- `packages/haive-core/src/haive/core/schema/field_utils.py:702` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 21dcd345
- `packages/haive-core/src/haive/core/schema/field_utils.py:702` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 21dcd345
- `packages/haive-core/src/haive/core/schema/field_utils.py:704` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 061e6f89
- `packages/haive-core/src/haive/core/schema/field_utils.py:704` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 061e6f89
- `packages/haive-core/src/haive/core/schema/field_utils.py:955` - note: def [_T] **add**(self, tuple[_T, ...], /) -> tuple[Any | _T, ...]
  - ID: c9532974
- `packages/haive-core/src/haive/core/engine/retriever/providers/MergerRetrieverConfig.py:70` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 7fad6416
- ... and 3 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/base.py:139` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 4493d396
- `packages/haive-dataflow/src/haive/dataflow/base.py:139` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 4493d396
- `packages/haive-dataflow/src/haive/dataflow/api/base.py:139` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 1be2b904
- `packages/haive-dataflow/src/haive/dataflow/api/base.py:139` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 1be2b904
- `packages/haive-dataflow/src/haive/dataflow/api/routes/llm_routes.py:114` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 87d1d2a3
- `packages/haive-dataflow/src/haive/dataflow/api/routes/llm_routes.py:114` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 87d1d2a3

### haive-games

- `packages/haive-games/src/haive/games/mastermind/state.py:96` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 13251358
- `packages/haive-games/src/haive/games/mastermind/state.py:96` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 13251358
- `packages/haive-games/src/haive/games/mastermind/models.py:163` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 401840c3
- `packages/haive-games/src/haive/games/mastermind/models.py:163` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 401840c3
- `packages/haive-games/src/haive/games/mastermind/models.py:240` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 5239675e
- `packages/haive-games/src/haive/games/mastermind/models.py:240` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 5239675e
- `packages/haive-games/src/haive/games/dominoes/state.py:190` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 1d6beb01
- `packages/haive-games/src/haive/games/dominoes/state.py:190` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 1d6beb01

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:143` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 3627c519
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:143` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 3627c519
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:176` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: e325415a
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:176` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: e325415a
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:177` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: d2e44133
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:177` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: d2e44133
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:200` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 01d681d3
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:200` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 01d681d3
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:201` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 1bb1b1df
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:201` - note: def [_T] Field(default: \_T, \*, alias: str | None = ..., alias_priority: int | None = ...,
  - ID: 1bb1b1df
- ... and 8 more

## mypy:abstract (9 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/base/typed_agent.py:492` - error: Cannot instantiate abstract class "WorkflowAgent" with abstract attribute "run_engine" [abst
  - ID: 13618f94
- `packages/haive-agents/src/haive/agents/base/typed_agent.py:494` - error: Cannot instantiate abstract class "MetaAgent" with abstract attribute "run_engine" [abstract
  - ID: 49039d58
- `packages/haive-agents/src/haive/agents/base/typed_agent.py:498` - error: Cannot instantiate abstract class "AdaptiveAgent" with abstract attribute "run_engine" [abst
  - ID: c25aef3a
- `packages/haive-agents/src/haive/agents/base/typed_agent.py:499` - error: Cannot instantiate abstract class "BaseAgent" with abstract attribute "run_engine" [abstract
  - ID: 5abf577e
- `packages/haive-agents/src/haive/agents/base/mixins/persistence_mixin.py:368` - error: Cannot instantiate abstract class "BaseStore" with abstract attributes "abatch" and "batch"
  - ID: 25f89420

### haive-core

- `packages/haive-core/src/haive/core/engine/agent/agent.py:967` - error: Cannot instantiate abstract class "BaseStore" with abstract attributes "abatch" and "batch"
  - ID: 925a2d5a
- `packages/haive-core/src/haive/core/engine/agent/agent.py:1002` - error: Cannot instantiate abstract class "BaseStore" with abstract attributes "abatch" and "batch"
  - ID: a54c8940
- `packages/haive-core/src/haive/core/engine/agent/agent.py:1086` - error: Cannot instantiate abstract class "BaseStore" with abstract attributes "abatch" and "batch"
  - ID: f80f5f3a
- `packages/haive-core/src/haive/core/engine/agent/agent.py:1145` - error: Cannot instantiate abstract class "BaseStore" with abstract attributes "abatch" and "batch"
  - ID: 0ac915f1

## mypy:arg-type (169 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/example.py:489` - error: Argument 1 to "exit" has incompatible type "int | float"; expected "str | int | None" [arg-t
  - ID: d3ea8d3a
- `packages/haive-agents/src/haive/agents/memory_v2/memory_state_original.py:130` - error: Argument "memory_type" to "UnifiedMemoryEntry" has incompatible type "agents.memory_v2.memory
  - ID: 20e9daf2
- `packages/haive-agents/src/haive/agents/reflection/multi_agent_reflection.py:411` - error: Argument 1 to "append" of "list" has incompatible type "BaseMessage"; expected "HumanMessage"
  - ID: 4c631a50
- `packages/haive-agents/src/haive/agents/react_class/react_v2/graph_utils.py:69` - error: Argument "name" to "add_human_node" of "ReactGraphBuilder" has incompatible type "str | None"
  - ID: beaab389
- `packages/haive-agents/src/haive/agents/react_class/react_agent2/config2.py:270` - error: Argument 1 to "append" of "list" has incompatible type "str"; expected "SystemMessage" [arg-
  - ID: 608999e2
- `packages/haive-agents/src/haive/agents/react_class/react_agent2/config2.py:273` - error: Argument 1 to "append" of "list" has incompatible type "MessagesPlaceholder"; expected "Syste
  - ID: e1e8cbed
- `packages/haive-agents/src/haive/agents/rag/unified_factory.py:292` - error: Argument "style" to "create_rag_pipeline" has incompatible type "str"; expected "RAGStyle" [
  - ID: bfa3fe37
- `packages/haive-agents/src/haive/agents/memory_v2/multi_memory_coordinator.py:559` - error: Argument 1 to "len" has incompatible type "object"; expected "Sized" [arg-type]
  - ID: 2a9fe3b9
- `packages/haive-agents/src/haive/agents/memory_v2/message_document_converter.py:142` - error: Argument "estimated_tokens" to "MessageMetadata" has incompatible type "float"; expected "int
  - ID: f27db9f8
- `packages/haive-agents/src/haive/agents/memory_v2/memory_tools.py:206` - error: Argument "importance" to "MemoryMetadata" has incompatible type "str"; expected "float" [arg
  - ID: 21235729
- ... and 25 more

### haive-core

- `packages/haive-core/src/haive/core/graph/node/engine_node_test.py:98` - error: Argument 1 to "exit" has incompatible type "int | float"; expected "str | int | None" [arg-t
  - ID: 138586c0
- `packages/haive-core/src/haive/core/utils/debugkit/debug/inspection.py:67` - error: Argument 1 to "getframeinfo" has incompatible type "FrameType | Any | None"; expected "FrameT
  - ID: ca3784db
- `packages/haive-core/src/haive/core/types/dynamic_literal.py:92` - error: Argument "base" to "PaintJob" has incompatible type "str"; expected "Colour" [arg-type]
  - ID: 2cb2f7ae
- `packages/haive-core/src/haive/core/types/dynamic_literal.py:92` - error: Argument "base" to "PaintJob" has incompatible type "str"; expected "Colour" [arg-type]
  - ID: 2cb2f7ae
- `packages/haive-core/src/haive/core/types/dynamic_literal.py:95` - error: Argument "base" to "PaintJob" has incompatible type "str"; expected "Colour" [arg-type]
  - ID: 5e05238e
- `packages/haive-core/src/haive/core/types/dynamic_literal.py:95` - error: Argument "base" to "PaintJob" has incompatible type "str"; expected "Colour" [arg-type]
  - ID: 5e05238e
- `packages/haive-core/src/haive/core/types/dynamic_literal.py:98` - error: Argument "base" to "PaintJob" has incompatible type "str"; expected "Colour" [arg-type]
  - ID: 2d15020e
- `packages/haive-core/src/haive/core/types/dynamic_literal.py:98` - error: Argument "base" to "PaintJob" has incompatible type "str"; expected "Colour" [arg-type]
  - ID: 2d15020e
- `packages/haive-core/src/haive/core/types/advanced_registry.py:129` - error: Argument 1 to "get_class" of "Registered" has incompatible type "str | None"; expected "str"
  - ID: d0b41e9b
- `packages/haive-core/src/haive/core/graph/StateSchema.py:132` - error: Argument 2 to "add_field" of "StateSchema" has incompatible type "<typing special form>"; exp
  - ID: 0045113a
- ... and 79 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/core.py:1526` - error: Argument 1 to "get_entities_by_type" of "RegistrySystem" has incompatible type "str"; expecte
  - ID: 7b84cb1c
- `packages/haive-dataflow/src/haive/dataflow/registry/registries/model_registry.py:737` - error: Argument 1 to "getenv" has incompatible type "Any | None"; expected "str" [arg-type]
  - ID: d74881e4
- `packages/haive-dataflow/src/haive/dataflow/registry/registries/model_registry.py:814` - error: Argument 1 to "getenv" has incompatible type "Any | None"; expected "str" [arg-type]
  - ID: 39a54759
- `packages/haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py:60` - error: Argument 1 to "module_from_spec" has incompatible type "ModuleSpec | None"; expected "ModuleS
  - ID: d5d24d63
- `packages/haive-dataflow/src/haive/dataflow/registries/model_registry.py:737` - error: Argument 1 to "getenv" has incompatible type "Any | None"; expected "str" [arg-type]
  - ID: def79d1c
- `packages/haive-dataflow/src/haive/dataflow/registries/model_registry.py:814` - error: Argument 1 to "getenv" has incompatible type "Any | None"; expected "str" [arg-type]
  - ID: 36059883
- `packages/haive-dataflow/src/haive/dataflow/bin/vault_cli.py:60` - error: Argument 1 to "module_from_spec" has incompatible type "ModuleSpec | None"; expected "ModuleS
  - ID: 84f5f60e
- `packages/haive-dataflow/src/haive/dataflow/registry/importers/litellm_importer.py:492` - error: Argument 1 to "int" has incompatible type "str | None"; expected "str | Buffer | SupportsInt
  - ID: 91e985c5
- `packages/haive-dataflow/src/haive/dataflow/importers/litellm_importer.py:449` - error: Argument 1 to "int" has incompatible type "str | None"; expected "str | Buffer | SupportsInt
  - ID: 2e2e3def
- `packages/haive-dataflow/src/haive/dataflow/registry/core.py:1597` - error: Argument 1 to "get_entities_by_type" of "RegistrySystem" has incompatible type "str"; expecte
  - ID: db21aec2
- ... and 2 more

### haive-games

- `packages/haive-games/src/haive/games/monopoly/game/game.py:816` - error: Argument 2 to "\_handle_sell_house_action" of "MonopolyGame" has incompatible type "Any | None
  - ID: fe22e4a2
- `packages/haive-games/src/haive/games/monopoly/game/game.py:820` - error: Argument 2 to "\_handle_build_house_action" of "MonopolyGame" has incompatible type "Any | Non
  - ID: 5a24180b
- `packages/haive-games/src/haive/games/monopoly/game/game.py:824` - error: Argument 2 to "\_handle_mortgage_action" of "MonopolyGame" has incompatible type "Any | None";
  - ID: ab286782
- `packages/haive-games/src/haive/games/monopoly/game/game.py:828` - error: Argument 2 to "\_handle_unmortgage_action" of "MonopolyGame" has incompatible type "Any | None
  - ID: 6484416b
- `packages/haive-games/src/haive/games/monopoly/game/game.py:850` - error: Argument 2 to "\_handle_trade_action" of "MonopolyGame" has incompatible type "Any | None"; ex
  - ID: 9fb144b2
- `packages/haive-games/src/haive/games/monopoly/game/game.py:859` - error: Argument 1 to "\_handle_auction_action" of "MonopolyGame" has incompatible type "Any | None";
  - ID: c026b701
- `packages/haive-games/src/haive/games/hold_em/ui.py:137` - error: Argument 2 to "\_get_player_at_position" of "HoldemRichUI" has incompatible type "str | int";
  - ID: 68060344
- `packages/haive-games/src/haive/games/hold_em/ui.py:151` - error: Argument 2 to "\_get_player_at_position" of "HoldemRichUI" has incompatible type "str | int";
  - ID: d3cdf4b3
- `packages/haive-games/src/haive/games/hold_em/ui.py:157` - error: Argument 1 to "append" of "Text" has incompatible type "str | Any | int"; expected "Text | st
  - ID: 754be210
- `packages/haive-games/src/haive/games/among_us/ui.py:665` - error: Argument "completed" to "add_task" of "Progress" has incompatible type "float"; expected "int
  - ID: a5409959
- ... and 6 more

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/tools/server_tester.py:311` - error: Argument 1 to "append" of "list" has incompatible type "TestResult | BaseException"; expected
  - ID: dbf4ea27
- `packages/haive-mcp/src/haive/mcp/servers/dataflow_mcp_server.py:151` - error: Argument 1 to "len" has incompatible type "object"; expected "Sized" [arg-type]
  - ID: 4665bc67
- `packages/haive-mcp/src/haive/mcp/installers/advanced_code_installer.py:389` - error: Argument 1 to "append" of "list" has incompatible type "BaseTool"; expected "StructuredTool"
  - ID: 7eb538f2
- `packages/haive-mcp/src/haive/mcp/working_enhanced_retriever.py:144` - error: Argument "vectorstore" to "from_llm" of "SelfQueryRetriever" has incompatible type "Any | Non
  - ID: 8746a076
- `packages/haive-mcp/src/haive/mcp/enhanced_parent_self_query_retriever.py:181` - error: Argument "vectorstore" to "ParentDocumentRetriever" has incompatible type "None"; expected "V
  - ID: edcc0b64
- `packages/haive-mcp/src/haive/mcp/enhanced_parent_self_query_retriever.py:202` - error: Argument "vectorstore" to "from_llm" of "SelfQueryRetriever" has incompatible type "None"; ex
  - ID: e7d4b370

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:79` - error: Argument 1 to "append" of "list" has incompatible type "AIMessage"; expected "HumanMessage"
  - ID: 32ef1d5a
- `packages/haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:130` - error: Argument 1 to "login" of "SMTP" has incompatible type "str | None"; expected "str" [arg-type
  - ID: bea41f52
- `packages/haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:130` - error: Argument 1 to "login" of "SMTP" has incompatible type "str | None"; expected "str" [arg-type
  - ID: bea41f52
- `packages/haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:132` - error: Argument 1 to "sendmail" of "SMTP" has incompatible type "str | None"; expected "str" [arg-t
  - ID: 2c9b36ae

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/import_analyzer.py:59` - error: Argument 1 to "add" of "set" has incompatible type "BaseExpression | str"; expected "str" [a
  - ID: 076e6ebe
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/import_analyzer.py:60` - error: Argument 1 to "add" of "set" has incompatible type "BaseExpression | str"; expected "str" [a
  - ID: fb34ee59
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/import_analyzer.py:76` - error: Argument 1 to "add" of "set" has incompatible type "BaseExpression | str"; expected "str" [a
  - ID: 52bd4ce4
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/import_analyzer.py:77` - error: Argument 1 to "add" of "set" has incompatible type "BaseExpression | str"; expected "str" [a
  - ID: 683fec41
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/import_analyzer.py:78` - error: Argument 1 to "add" of "set" has incompatible type "BaseExpression | str | Any"; expected "st
  - ID: c217d38b
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/import_consolidator.py:59` - error: Argument "asname" to "ImportAlias" has incompatible type "Any | Name"; expected "AsName | Non
  - ID: 01cd7262
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1215` - error: Argument "name" to "ExceptHandler" has incompatible type "Name"; expected "AsName | None" [a
  - ID: e91c2e1a

## mypy:assignment (269 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/task_analysis/tree/models.py:84` - error: Incompatible types in assignment (expression has type "float", variable has type "int") [ass
  - ID: 6c3be760
- `packages/haive-agents/src/haive/agents/simple/lazy_simple_agent.v2.py:199` - error: Incompatible types in assignment (expression has type "str", target has type "float") [assig
  - ID: 42315627
- `packages/haive-agents/src/haive/agents/simple/lazy_simple_agent.py:184` - error: Incompatible types in assignment (expression has type "str", target has type "float") [assig
  - ID: 3a312f44
- `packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/example.py:330` - error: Incompatible types in assignment (expression has type "float", variable has type "int") [ass
  - ID: 95e099c5
- `packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/example.py:335` - error: Incompatible types in assignment (expression has type "float", variable has type "int") [ass
  - ID: 8416d7e0
- `packages/haive-agents/src/haive/agents/research/storm/state.py:98` - error: Incompatible types in assignment (expression has type "TopicState", base class "TopicState" d
  - ID: fc659a9c
- `packages/haive-agents/src/haive/agents/research/storm/config.py:113` - error: Incompatible types in assignment (expression has type "None", variable has type "VectorStoreC
  - ID: 553a4680
- `packages/haive-agents/src/haive/agents/research/storm/config.py:117` - error: Incompatible types in assignment (expression has type "None", variable has type "BaseRetrieve
  - ID: 19e35874
- `packages/haive-agents/src/haive/agents/research/storm/config.py:122` - error: Incompatible types in assignment (expression has type "None", variable has type "ResearchAgen
  - ID: 56091c03
- `packages/haive-agents/src/haive/agents/research/storm/config.py:126` - error: Incompatible types in assignment (expression has type "None", variable has type "InterviewAge
  - ID: 81d3105c
- ... and 89 more

### haive-core

- `packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:281` - error: Incompatible types in assignment (expression has type "None", variable has type "ComplexityMe
  - ID: b88ede79
- `packages/haive-core/src/haive/core/graph/common/field_utils.py:46` - error: Incompatible types in assignment (expression has type "int", variable has type "str") [assig
  - ID: 1da762b6
- `packages/haive-core/src/haive/core/graph/common/field_utils.py:48` - error: Incompatible types in assignment (expression has type "int", variable has type "str") [assig
  - ID: a0d88ead
- `packages/haive-core/src/haive/core/graph/branches/utils.py:46` - error: Incompatible types in assignment (expression has type "int", variable has type "str") [assig
  - ID: 4d85f662
- `packages/haive-core/src/haive/core/graph/branches/utils.py:48` - error: Incompatible types in assignment (expression has type "int", variable has type "str") [assig
  - ID: aa113705
- `packages/haive-core/src/haive/core/engine/document/loaders/sources/registry.py:235` - error: Incompatible types in assignment (expression has type "SourceRegistration | None", variable h
  - ID: 3aa93681
- `packages/haive-core/src/haive/core/utils/debugkit/core/unified.py:410` - error: Incompatible default for argument "profile" (default has type "None", argument has type "bool
  - ID: 65af9a4a
- `packages/haive-core/src/haive/core/utils/debugkit/core/unified.py:411` - error: Incompatible default for argument "trace" (default has type "None", argument has type "bool")
  - ID: dbde0b89
- `packages/haive-core/src/haive/core/utils/debugkit/core/unified.py:412` - error: Incompatible default for argument "log" (default has type "None", argument has type "bool")
  - ID: 09896621
- `packages/haive-core/src/haive/core/common/logging_config.py:49` - error: Incompatible types in assignment (expression has type "None", variable has type "Console") [
  - ID: a9691bb4
- ... and 75 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/utils/vault_migration_script.py:239` - error: Incompatible types in assignment (expression has type "str | None", variable has type "str")
  - ID: 2720c775
- `packages/haive-dataflow/src/haive/dataflow/utils/vault_migration_script.py:458` - error: Incompatible types in assignment (expression has type "str | None", variable has type "str")
  - ID: ef933d51
- `packages/haive-dataflow/src/haive/dataflow/utils/vault_migration_script.py:598` - error: Incompatible types in assignment (expression has type "str | None", variable has type "str")
  - ID: 1ddcbe1e
- `packages/haive-dataflow/src/haive/dataflow/registry/utils/vault_migration_script.py:239` - error: Incompatible types in assignment (expression has type "str | None", variable has type "str")
  - ID: 0aa680d8
- `packages/haive-dataflow/src/haive/dataflow/registry/utils/vault_migration_script.py:458` - error: Incompatible types in assignment (expression has type "str | None", variable has type "str")
  - ID: 1ba32668
- `packages/haive-dataflow/src/haive/dataflow/registry/utils/vault_migration_script.py:598` - error: Incompatible types in assignment (expression has type "str | None", variable has type "str")
  - ID: 639f635e
- `packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:267` - error: Incompatible types in assignment (expression has type "bool", target has type "str") [assign
  - ID: 11d04efb
- `packages/haive-dataflow/src/haive/dataflow/registry/importers/litellm_importer.py:489` - error: Incompatible types in assignment (expression has type "object", variable has type "str | None
  - ID: 69f031ad
- `packages/haive-dataflow/src/haive/dataflow/registry/importers/litellm_importer.py:492` - error: Incompatible types in assignment (expression has type "int", variable has type "str | None")
  - ID: be815bd4
- `packages/haive-dataflow/src/haive/dataflow/registry/importers/litellm_importer.py:495` - error: Incompatible types in assignment (expression has type "object", variable has type "str | None
  - ID: 17def756
- ... and 19 more

### haive-games

- `packages/haive-games/src/haive/games/chess/llm_utils.py:173` - error: Incompatible types in assignment (expression has type "float", target has type "str") [assig
  - ID: 635f821d
- `packages/haive-games/src/haive/games/chess/llm_utils.py:179` - error: Incompatible types in assignment (expression has type "float", target has type "str") [assig
  - ID: 466a8c68
- `packages/haive-games/src/haive/games/framework/base/template_generator.py:98` - error: Incompatible default for argument "output_dir" (default has type "None", argument has type "s
  - ID: 941dcbb6
- `packages/haive-games/src/haive/games/chess/example_configurable.py:26` - error: Incompatible default for argument "white_model" (default has type "None", argument has type "
  - ID: ad628d34
- `packages/haive-games/src/haive/games/chess/example_configurable.py:28` - error: Incompatible default for argument "black_model" (default has type "None", argument has type "
  - ID: a1336363
- `packages/haive-games/src/haive/games/chess/example.py:23` - error: Incompatible default for argument "thread_id" (default has type "None", argument has type "st
  - ID: 3751f423
- `packages/haive-games/src/haive/games/checkers/example.py:265` - error: Incompatible types in assignment (expression has type "int | float", target has type "int")
  - ID: 0455d765
- `packages/haive-games/src/haive/games/checkers/example.py:266` - error: Incompatible types in assignment (expression has type "Any | float | int", target has type "i
  - ID: c910e383
- `packages/haive-games/src/haive/games/checkers/example.py:271` - error: Incompatible types in assignment (expression has type "int | float", target has type "int")
  - ID: ee83f308
- `packages/haive-games/src/haive/games/checkers/example.py:273` - error: Incompatible types in assignment (expression has type "int | float", target has type "int")
  - ID: 6c80bd87
- ... and 30 more

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/tools/ai_assistant.py:206` - error: Incompatible types in assignment (expression has type "float", variable has type "int") [ass
  - ID: 6800ec2c
- `packages/haive-mcp/src/haive/mcp/enhance_mcp_data.py:43` - error: Incompatible types in assignment (expression has type "ClientSession", variable has type "Non
  - ID: 1aae5aad
- `packages/haive-mcp/src/haive/mcp/downloader/legacy_core.py:33` - error: Incompatible types in assignment (expression has type "None", variable has type Module) [ass
  - ID: 124a129c
- `packages/haive-mcp/src/haive/mcp/downloader/legacy_core.py:38` - error: Incompatible types in assignment (expression has type "None", variable has type Module) [ass
  - ID: 9dc56f50
- `packages/haive-mcp/src/haive/mcp/simple_rag_mcp_agent.py:76` - error: Incompatible types in assignment (expression has type "ChatOpenAI", variable has type "None")
  - ID: 4ef2e091
- `packages/haive-mcp/src/haive/mcp/utils/extract_mcp_github_repos.py:575` - error: Incompatible types in assignment (expression has type "str", variable has type "MCPCategory")
  - ID: 466ca19d
- `packages/haive-mcp/src/haive/mcp/utils/extract_mcp_github_repos.py:602` - error: Incompatible types in assignment (expression has type "ClientSession", variable has type "Non
  - ID: ed4b074e
- `packages/haive-mcp/src/haive/mcp/simple_faiss_retriever.py:42` - error: Incompatible types in assignment (expression has type "FAISS", variable has type "None") [as
  - ID: e365cf1c
- `packages/haive-mcp/src/haive/mcp/simple_faiss_retriever.py:106` - error: Incompatible types in assignment (expression has type "FAISS", variable has type "None") [as
  - ID: 2f50bc85
- `packages/haive-mcp/src/haive/mcp/enhanced_parent_self_query_retriever.py:180` - error: Incompatible types in assignment (expression has type "ParentDocumentRetriever", variable has
  - ID: 21260609

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/open_researcher/models.py:26` - error: Incompatible types in assignment (expression has type "None", variable has type "str") [assi
  - ID: 9c9d5e32
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/tools.py:200` - error: Incompatible types in assignment (expression has type "str | None", variable has type "str")
  - ID: e5d202bf
- `packages/haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:118` - error: Incompatible types in assignment (expression has type "str | None", target has type "str") [
  - ID: 7f0bf50d
- `packages/haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:119` - error: Incompatible types in assignment (expression has type "str | None", target has type "str") [
  - ID: cd8f5e22

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1023` - error: Incompatible types in assignment (expression has type "Annotation | None", variable has type
  - ID: daf45af5
- `packages/haive-tools/src/haive/tools/tools/toolkits/polygon_toolkit.py:85` - error: Incompatible types in assignment (expression has type "None", variable has type "PolygonToolk
  - ID: 314f01d9

## mypy:attr-defined (515 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/rag/multi_agent_rag/specialized_workflows_v2.py:286` - error: "object" has no attribute "**iter**"; maybe "**dir**" or "**str**"? (not iterable) [attr-def
  - ID: e8f10469
- `packages/haive-agents/src/haive/agents/self_healing_code/__init__.py:3` - error: Module "agents.self_healing_code.agent" has no attribute "bug_report_node" [attr-defined]
  - ID: f60e49af
- `packages/haive-agents/src/haive/agents/self_healing_code/__init__.py:3` - error: Module "agents.self_healing_code.agent" has no attribute "bug_report_node" [attr-defined]
  - ID: f60e49af
- `packages/haive-agents/src/haive/agents/self_healing_code/__init__.py:3` - error: Module "agents.self_healing_code.agent" has no attribute "bug_report_node" [attr-defined]
  - ID: f60e49af
- `packages/haive-agents/src/haive/agents/self_healing_code/__init__.py:3` - error: Module "agents.self_healing_code.agent" has no attribute "bug_report_node" [attr-defined]
  - ID: f60e49af
- `packages/haive-agents/src/haive/agents/self_healing_code/__init__.py:3` - error: Module "agents.self_healing_code.agent" has no attribute "bug_report_node" [attr-defined]
  - ID: f60e49af
- `packages/haive-agents/src/haive/agents/self_healing_code/__init__.py:3` - error: Module "agents.self_healing_code.agent" has no attribute "bug_report_node" [attr-defined]
  - ID: f60e49af
- `packages/haive-agents/src/haive/agents/self_healing_code/__init__.py:3` - error: Module "agents.self_healing_code.agent" has no attribute "bug_report_node" [attr-defined]
  - ID: f60e49af
- `packages/haive-agents/src/haive/agents/self_healing_code/__init__.py:3` - error: Module "agents.self_healing_code.agent" has no attribute "bug_report_node" [attr-defined]
  - ID: f60e49af
- `packages/haive-agents/src/haive/agents/self_healing_code/__init__.py:3` - error: Module "agents.self_healing_code.agent" has no attribute "bug_report_node" [attr-defined]
  - ID: f60e49af
- ... and 222 more

### haive-core

- `packages/haive-core/src/haive/core/models/llm/export_llm_models_to_csv.py:71` - error: "type" has no attribute "get_models" [attr-defined]
  - ID: 7582da5c
- `packages/haive-core/src/haive/core/schema/composer/field/field_manager.py:152` - error: "type" has no attribute "**args**"; maybe "**flags**"? [attr-defined]
  - ID: a7fefe33
- `packages/haive-core/src/haive/core/schema/composer/field/field_manager.py:157` - error: "type" has no attribute "**args**"; maybe "**flags**"? [attr-defined]
  - ID: 8973bf44
- `packages/haive-core/src/haive/core/schema/composer/engine/engine_manager.py:170` - error: "EngineComposerMixin" has no attribute "fields" [attr-defined]
  - ID: 1b57a7a8
- `packages/haive-core/src/haive/core/schema/composer/engine/engine_manager.py:170` - error: "EngineComposerMixin" has no attribute "fields" [attr-defined]
  - ID: 1b57a7a8
- `packages/haive-core/src/haive/core/schema/composer/engine/engine_manager.py:171` - error: "EngineComposerMixin" has no attribute "add_field" [attr-defined]
  - ID: b9fb594c
- `packages/haive-core/src/haive/core/schema/composer/engine/engine_manager.py:181` - error: "EngineComposerMixin" has no attribute "fields" [attr-defined]
  - ID: ed68cda8
- `packages/haive-core/src/haive/core/schema/composer/engine/engine_manager.py:181` - error: "EngineComposerMixin" has no attribute "fields" [attr-defined]
  - ID: ed68cda8
- `packages/haive-core/src/haive/core/schema/composer/engine/engine_manager.py:182` - error: "EngineComposerMixin" has no attribute "add_field" [attr-defined]
  - ID: 48aad147
- `packages/haive-core/src/haive/core/schema/composer/engine/engine_detector.py:39` - error: "EngineDetectorMixin" has no attribute "fields" [attr-defined]
  - ID: 98cfcfcd
- ... and 107 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/registry/importers/embeddings_importer.py:264` - error: "object" has no attribute "upper" [attr-defined]
  - ID: c6f7574e
- `packages/haive-dataflow/src/haive/dataflow/registry/importers/embeddings_importer.py:289` - error: "object" has no attribute "title" [attr-defined]
  - ID: 457a674f
- `packages/haive-dataflow/src/haive/dataflow/registry/importers/embeddings_importer.py:513` - error: "object" has no attribute "replace" [attr-defined]
  - ID: d5079720
- `packages/haive-dataflow/src/haive/dataflow/importers/embeddings_importer.py:273` - error: "object" has no attribute "upper" [attr-defined]
  - ID: 58b28d41
- `packages/haive-dataflow/src/haive/dataflow/importers/embeddings_importer.py:298` - error: "object" has no attribute "title" [attr-defined]
  - ID: 1425208e
- `packages/haive-dataflow/src/haive/dataflow/importers/embeddings_importer.py:522` - error: "object" has no attribute "replace" [attr-defined]
  - ID: d28c9c28
- `packages/haive-dataflow/src/haive/dataflow/api/db.py:51` - error: "None" has no attribute "cursor" [attr-defined]
  - ID: 26ea476c
- `packages/haive-dataflow/src/haive/dataflow/api/db.py:58` - error: "None" has no attribute "commit" [attr-defined]
  - ID: 5d76879c
- `packages/haive-dataflow/src/haive/dataflow/api/db.py:63` - error: "None" has no attribute "rollback" [attr-defined]
  - ID: 681aa249
- `packages/haive-dataflow/src/haive/dataflow/api/db.py:76` - error: "None" has no attribute "cursor" [attr-defined]
  - ID: 9266950c
- ... and 20 more

### haive-games

- `packages/haive-games/src/haive/games/single_player/state_manager.py:74` - error: T? has no attribute "hint_count" [attr-defined]
  - ID: 1b25c28f
- `packages/haive-games/src/haive/games/single_player/state_manager.py:131` - error: T? has no attribute "error_message" [attr-defined]
  - ID: d4f5653b
- `packages/haive-games/src/haive/games/single_player/state_manager.py:133` - error: T? has no attribute "game_status" [attr-defined]
  - ID: 28ef7196
- `packages/haive-games/src/haive/games/single_player/state_manager.py:134` - error: T? has no attribute "error_message" [attr-defined]
  - ID: 8d572723
- `packages/haive-games/src/haive/games/single_player/state_manager.py:136` - error: T? has no attribute "move_count" [attr-defined]
  - ID: f93c1340
- `packages/haive-games/src/haive/games/single_player/state_manager.py:137` - error: T? has no attribute "hint_count" [attr-defined]
  - ID: 82926a2d
- `packages/haive-games/src/haive/games/single_player/state_manager.py:138` - error: T? has no attribute "error_message" [attr-defined]
  - ID: 5f9300a4
- `packages/haive-games/src/haive/games/single_player/wordle/state_manager.py:140` - error: "object" has no attribute "values" [attr-defined]
  - ID: 147a4bd4
- `packages/haive-games/src/haive/games/poker/debug.py:314` - error: "object" has no attribute "append" [attr-defined]
  - ID: 4fedc641
- `packages/haive-games/src/haive/games/poker/debug.py:320` - error: "object" has no attribute "append" [attr-defined]
  - ID: a3124adb
- ... and 65 more

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/tools/ai_assistant.py:696` - error: "object" has no attribute "append" [attr-defined]
  - ID: 6533c437
- `packages/haive-mcp/src/haive/mcp/tools/ai_assistant.py:701` - error: "object" has no attribute "extend" [attr-defined]
  - ID: cfe7e9ef
- `packages/haive-mcp/src/haive/mcp/tools/ai_assistant.py:707` - error: "object" has no attribute "append" [attr-defined]
  - ID: 9c39850a
- `packages/haive-mcp/src/haive/mcp/tools/ai_assistant.py:711` - error: "object" has no attribute "append" [attr-defined]
  - ID: 5d80314d
- `packages/haive-mcp/src/haive/mcp/tools/ai_assistant.py:716` - error: "object" has no attribute "append" [attr-defined]
  - ID: d4b78b2a
- `packages/haive-mcp/src/haive/mcp/enhance_mcp_data.py:78` - error: "None" has no attribute "get" [attr-defined]
  - ID: 62af8340
- `packages/haive-mcp/src/haive/mcp/agents/transferable_mcp_agent.py:557` - error: "object" has no attribute "append" [attr-defined]
  - ID: 797377fc
- `packages/haive-mcp/src/haive/mcp/integrated_mcp_system.py:480` - error: "DataframeState" has no attribute "selection" [attr-defined]
  - ID: a2bcf259
- `packages/haive-mcp/src/haive/mcp/integrated_mcp_system.py:481` - error: "DataframeState" has no attribute "selection" [attr-defined]
  - ID: 46d7bb93
- `packages/haive-mcp/src/haive/mcp/comprehensive_mcp_web.py:376` - error: "DataframeState" has no attribute "selection" [attr-defined]
  - ID: 83bf1936
- ... and 16 more

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/models.py:230` - error: "TContent" has no attribute "headline" [attr-defined]
  - ID: 32ec6cb1
- `packages/haive-prebuilt/src/haive/prebuilt/constituional_agent/utils.py:102` - error: "Lexer" has no attribute "name" [attr-defined]
  - ID: 647640c3
- `packages/haive-prebuilt/src/haive/prebuilt/search_and_summarize/tools.py:145` - error: "str" has no attribute "query" [attr-defined]
  - ID: d1da8f78
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:508` - error: "str" has no attribute "get" [attr-defined]
  - ID: 1d7aeedf
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:519` - error: "str" has no attribute "get" [attr-defined]
  - ID: 697d67c4
- `packages/haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/utils.py:5` - error: Module "langgraph.graph" has no attribute "CompiledStateGraph" [attr-defined]
  - ID: 2b00235a
- `packages/haive-prebuilt/src/haive/prebuilt/podcast_generator/nodes.py:3` - error: Module "langgraph.graph" has no attribute "Send" [attr-defined]
  - ID: 91eefe35
- `packages/haive-prebuilt/src/haive/prebuilt/podcast_generator/nodes.py:49` - error: "None" has no attribute "send_message" [attr-defined]
  - ID: 630858df
- `packages/haive-prebuilt/src/haive/prebuilt/podcast_generator/nodes.py:66` - error: "None" has no attribute "send_message" [attr-defined]
  - ID: 5284f35f
- `packages/haive-prebuilt/src/haive/prebuilt/podcast_generator/nodes.py:83` - error: "None" has no attribute "send_message" [attr-defined]
  - ID: 483448bc
- ... and 17 more

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/type_checking.py:62` - error: "BaseExpression" has no attribute "value" [attr-defined]
  - ID: 97cdaa0c
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/import_analyzer.py:58` - error: "AsName" has no attribute "value" [attr-defined]
  - ID: 608fb9bb
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:810` - error: "CSTNode" has no attribute "body" [attr-defined]
  - ID: 7eda2be0
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:885` - error: "CSTNode" has no attribute "body" [attr-defined]
  - ID: d5872078
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/permission.py:234` - error: "ValidationError" has no attribute "model" [attr-defined]
  - ID: 4a3f97c0
- `packages/haive-tools/src/haive/tools/tools/toolkits/jira_toolkit.py:116` - error: "JiraAPIWrapper" has no attribute "projects"; maybe "project"? [attr-defined]
  - ID: f5f2c688
- `packages/haive-tools/src/haive/tools/tools/toolkits/jira_toolkit.py:146` - error: "JiraAPIWrapper" has no attribute "create_issue" [attr-defined]
  - ID: 7394ccd1
- `packages/haive-tools/src/haive/tools/tools/toolkits/jira_toolkit.py:158` - error: "JiraAPIWrapper" has no attribute "jql_query" [attr-defined]
  - ID: 8f1dcd9c

## mypy:bool | str | int, str (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py:1581` - error: Incompatible types in assignment (expression has type "dict[bool | str | int, str]", variable
  - ID: c2abd1fc

## mypy:bool, str (11 errors)

### haive-core

- `packages/haive-core/src/haive/core/graph/state_graph/serializable.py:478` - error: Invalid index type "int" for "dict[bool, str]"; expected type "bool" [index]
  - ID: 53889008
- `packages/haive-core/src/haive/core/graph/state_graph/serializable.py:481` - error: Invalid index type "str" for "dict[bool, str]"; expected type "bool" [index]
  - ID: 5a8161c3
- `packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py:2586` - error: Invalid index type "str" for "dict[bool, str]"; expected type "bool" [index]
  - ID: a7458627
- `packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py:2587` - error: Invalid index type "str" for "dict[bool, str]"; expected type "bool" [index]
  - ID: b7611451
- `packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py:2588` - error: Invalid index type "str" for "dict[bool, str]"; expected type "bool" [index]
  - ID: 155d3286
- `packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py:2589` - error: Invalid index type "str" for "dict[bool, str]"; expected type "bool" [index]
  - ID: 1822d503
- `packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py:2590` - error: Invalid index type "str" for "dict[bool, str]"; expected type "bool" [index]
  - ID: f87c6e17
- `packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py:2591` - error: Invalid index type "str" for "dict[bool, str]"; expected type "bool" [index]
  - ID: bd24a3cf
- `packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py:2592` - error: Invalid index type "str" for "dict[bool, str]"; expected type "bool" [index]
  - ID: 831ceb55
- `packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py:2593` - error: Invalid index type "str" for "dict[bool, str]"; expected type "bool" [index]
  - ID: e5217bd4
- ... and 1 more

## mypy:call-arg (292 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/sequential/example.py:47` - error: Too many arguments for "pretty_print" [call-arg]
  - ID: c8b09119
- `packages/haive-agents/src/haive/agents/sequential/example.py:49` - error: Too many arguments for "pretty_print" [call-arg]
  - ID: 7de9e235
- `packages/haive-agents/src/haive/agents/experiments/supervisor/state_models.py:100` - error: Missing named argument "completed_at" for "ExecutionContext" [call-arg]
  - ID: 21d22644
- `packages/haive-agents/src/haive/agents/experiments/supervisor/state_models.py:100` - error: Missing named argument "completed_at" for "ExecutionContext" [call-arg]
  - ID: 21d22644
- `packages/haive-agents/src/haive/agents/experiments/supervisor/state_models.py:100` - error: Missing named argument "completed_at" for "ExecutionContext" [call-arg]
  - ID: 21d22644
- `packages/haive-agents/src/haive/agents/common/models/task_analysis/analysis.py:363` - error: Unexpected keyword argument "dimension_scores" for "TaskComplexity"; did you mean "dimensions
  - ID: 14a4cec3
- `packages/haive-agents/src/haive/agents/common/models/task_analysis/analysis.py:363` - error: Unexpected keyword argument "dimension_scores" for "TaskComplexity"; did you mean "dimensions
  - ID: 14a4cec3
- `packages/haive-agents/src/haive/agents/common/models/task_analysis/analysis.py:363` - error: Unexpected keyword argument "dimension_scores" for "TaskComplexity"; did you mean "dimensions
  - ID: 14a4cec3
- `packages/haive-agents/src/haive/agents/common/models/task_analysis/analysis.py:363` - error: Unexpected keyword argument "dimension_scores" for "TaskComplexity"; did you mean "dimensions
  - ID: 14a4cec3
- `packages/haive-agents/src/haive/agents/common/models/task_analysis/analysis.py:419` - error: Unexpected keyword argument "planning_depth" for "PlanningRequirement" [call-arg]
  - ID: 581b526d
- ... and 84 more

### haive-core

- `packages/haive-core/src/haive/core/utils/env_utils.py:111` - error: Too many arguments for "object" [call-arg]
  - ID: ab10da3d
- `packages/haive-core/src/haive/core/utils/env_utils.py:112` - error: Too many arguments for "object" [call-arg]
  - ID: ef8d5fb1
- `packages/haive-core/src/haive/core/schema/utils.py:154` - error: Too few arguments [call-arg]
  - ID: 6b63821e
- `packages/haive-core/src/haive/core/graph/graph_pattern_registry.py:212` - error: Unexpected keyword argument "\_apply_func" for "GraphPattern"; did you mean "apply_func"? [ca
  - ID: c9d62043
- `packages/haive-core/src/haive/core/graph/graph_pattern_registry.py:247` - error: Unexpected keyword argument "\_condition_func" for "BranchDefinition"; did you mean "condition
  - ID: 4b8b7a91
- `packages/haive-core/src/haive/core/engine/document/loaders/sources/implementation.py:321` - error: Missing named argument "source_type" for "EnhancedSource" [call-arg]
  - ID: 0ad371f8
- `packages/haive-core/src/haive/core/engine/retriever/mixins.py:63` - error: Unexpected keyword argument "engine" for "RetrieverMixin" [call-arg]
  - ID: 629939e2
- `packages/haive-core/src/haive/core/engine/retriever/mixins.py:111` - error: Unexpected keyword argument "engine" for "RetrieverMixin" [call-arg]
  - ID: 4c0700aa
- `packages/haive-core/src/haive/core/engine/retriever/mixins.py:124` - error: Unexpected keyword argument "engine" for "RetrieverMixin" [call-arg]
  - ID: 4ffaac49
- `packages/haive-core/src/haive/core/engine/aug_llm/factory.py:255` - error: Unexpected keyword argument "partial_variables" for "from_messages" of "ChatPromptTemplate"
  - ID: efa4cd65
- ... and 80 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:368` - error: Missing named argument "result" for "ToolInvokeResponse" [call-arg]
  - ID: 92b68dc3
- `packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:397` - error: Missing named argument "result" for "ToolInvokeResponse" [call-arg]
  - ID: a0424b54
- `packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:401` - error: Missing named argument "error" for "ToolInvokeResponse" [call-arg]
  - ID: 1b114653
- `packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:405` - error: Missing named argument "result" for "ToolInvokeResponse" [call-arg]
  - ID: 84007a1f
- `packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:409` - error: Missing named argument "result" for "ToolInvokeResponse" [call-arg]
  - ID: 4ac04ce9
- `packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes.py:720` - error: Missing named argument "result" for "ToolInvokeResponse" [call-arg]
  - ID: db4c18db
- `packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes.py:727` - error: Missing named argument "error" for "ToolInvokeResponse" [call-arg]
  - ID: 43e1f068
- `packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes.py:731` - error: Missing named argument "result" for "ToolInvokeResponse" [call-arg]
  - ID: 73dc1794
- `packages/haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:583` - error: Missing named argument "system_prompt" for "AgentChatConfig" [call-arg]
  - ID: f21306ea
- `packages/haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:640` - error: Missing named argument "thread_id" for "WSMessage" [call-arg]
  - ID: a99b0b1d
- ... and 17 more

### haive-games

- `packages/haive-games/src/haive/games/among_us/ui.py:400` - error: Unexpected keyword argument "size" for "Text" [call-arg]
  - ID: ff095f80
- `packages/haive-games/src/haive/games/risk/models.py:616` - error: Missing named argument "territory_name" for "Card" [call-arg]
  - ID: c0396834
- `packages/haive-games/src/haive/games/risk/models.py:874` - error: Missing named argument "territory_name" for "Card" [call-arg]
  - ID: 05df1471
- `packages/haive-games/src/haive/games/risk/models.py:875` - error: Missing named argument "territory_name" for "Card" [call-arg]
  - ID: 1cbef053
- `packages/haive-games/src/haive/games/risk/models.py:876` - error: Missing named argument "territory_name" for "Card" [call-arg]
  - ID: 91edb17d
- `packages/haive-games/src/haive/games/battleship/models.py:1015` - error: Missing named argument "sunk_ship" for "MoveOutcome" [call-arg]
  - ID: 1472580f
- `packages/haive-games/src/haive/games/battleship/models.py:1018` - error: Missing named argument "sunk_ship" for "MoveOutcome" [call-arg]
  - ID: 839f3b3c
- `packages/haive-games/src/haive/games/battleship/models.py:1027` - error: Missing named argument "sunk_ship" for "MoveOutcome" [call-arg]
  - ID: 314ce7d9
- `packages/haive-games/src/haive/games/battleship/models.py:1029` - error: Missing named argument "sunk_ship" for "MoveOutcome" [call-arg]
  - ID: 27b14745
- `packages/haive-games/src/haive/games/mancala/agent_original.py:342` - error: Unexpected keyword argument "stop" for "Command" [call-arg]
  - ID: 2ee120f3
- ... and 3 more

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/downloader/core.py:722` - error: Missing named argument "last_check" for "ServerStatus" [call-arg]
  - ID: b90c4a4e
- `packages/haive-mcp/src/haive/mcp/downloader/core.py:722` - error: Missing named argument "last_check" for "ServerStatus" [call-arg]
  - ID: b90c4a4e
- `packages/haive-mcp/src/haive/mcp/downloader/core.py:722` - error: Missing named argument "last_check" for "ServerStatus" [call-arg]
  - ID: b90c4a4e
- `packages/haive-mcp/src/haive/mcp/downloader/core.py:722` - error: Missing named argument "last_check" for "ServerStatus" [call-arg]
  - ID: b90c4a4e
- `packages/haive-mcp/src/haive/mcp/downloader/core.py:722` - error: Missing named argument "last_check" for "ServerStatus" [call-arg]
  - ID: b90c4a4e
- `packages/haive-mcp/src/haive/mcp/downloader/core.py:869` - error: Missing named argument "config_file" for "DownloadResult" [call-arg]
  - ID: 1f9e1a25
- `packages/haive-mcp/src/haive/mcp/downloader/core.py:908` - error: Missing named argument "last_check" for "ServerStatus" [call-arg]
  - ID: c314da05
- `packages/haive-mcp/src/haive/mcp/downloader/core.py:908` - error: Missing named argument "last_check" for "ServerStatus" [call-arg]
  - ID: c314da05
- `packages/haive-mcp/src/haive/mcp/downloader/core.py:908` - error: Missing named argument "last_check" for "ServerStatus" [call-arg]
  - ID: c314da05
- `packages/haive-mcp/src/haive/mcp/downloader/core.py:908` - error: Missing named argument "last_check" for "ServerStatus" [call-arg]
  - ID: c314da05
- ... and 9 more

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/models.py:394` - error: Missing named argument "quality_score" for "Slide" [call-arg]
  - ID: 0d38c4d5
- `packages/haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/models.py:394` - error: Missing named argument "quality_score" for "Slide" [call-arg]
  - ID: 0d38c4d5
- `packages/haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/models.py:394` - error: Missing named argument "quality_score" for "Slide" [call-arg]
  - ID: 0d38c4d5
- `packages/haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/models.py:394` - error: Missing named argument "quality_score" for "Slide" [call-arg]
  - ID: 0d38c4d5
- `packages/haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/models.py:394` - error: Missing named argument "quality_score" for "Slide" [call-arg]
  - ID: 0d38c4d5
- `packages/haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/models.py:394` - error: Missing named argument "quality_score" for "Slide" [call-arg]
  - ID: 0d38c4d5
- `packages/haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:450` - error: Missing named argument "emotional_impact" for "ProblemStatement" [call-arg]
  - ID: 6a2f1005
- `packages/haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:450` - error: Missing named argument "emotional_impact" for "ProblemStatement" [call-arg]
  - ID: 6a2f1005
- `packages/haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:450` - error: Missing named argument "emotional_impact" for "ProblemStatement" [call-arg]
  - ID: 6a2f1005
- `packages/haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:455` - error: Missing named argument "technical_feasibility" for "SolutionConcept" [call-arg]
  - ID: 1aeeeec5
- ... and 4 more

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1400` - error: Missing named argument "line_length" for "CodeStyleConfig" [call-arg]
  - ID: 825ce56b
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1400` - error: Missing named argument "line_length" for "CodeStyleConfig" [call-arg]
  - ID: 825ce56b
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1400` - error: Missing named argument "line_length" for "CodeStyleConfig" [call-arg]
  - ID: 825ce56b
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1400` - error: Missing named argument "line_length" for "CodeStyleConfig" [call-arg]
  - ID: 825ce56b
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1400` - error: Missing named argument "line_length" for "CodeStyleConfig" [call-arg]
  - ID: 825ce56b
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1400` - error: Missing named argument "line_length" for "CodeStyleConfig" [call-arg]
  - ID: 825ce56b
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1461` - error: Missing named argument "diff" for "EditResult" [call-arg]
  - ID: 3a68dedb
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1461` - error: Missing named argument "diff" for "EditResult" [call-arg]
  - ID: 3a68dedb
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1490` - error: Missing named argument "diff" for "EditResult" [call-arg]
  - ID: 7c2a516d
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1490` - error: Missing named argument "diff" for "EditResult" [call-arg]
  - ID: 7c2a516d
- ... and 25 more

## mypy:call-overload (79 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/tot_multi_agent.py:35` - error: No overload variant of "Field" matches argument types "str", "int", "int" [call-overload]
  - ID: 8f438f35
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/models.py:142` - error: No overload variant of "Field" matches argument types "str", "int" [call-overload]
  - ID: 12e65a4e
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/models.py:257` - error: No overload variant of "Field" matches argument types "str", "int" [call-overload]
  - ID: d4bac1a4
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/agents/solution_scorer.py:30` - error: No overload variant of "Field" matches argument types "str", "int" [call-overload]
  - ID: ce5142b5
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/agents/candidate_generator.py:19` - error: No overload variant of "Field" matches argument types "str", "int", "int" [call-overload]
  - ID: 158182cd
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/models.py:14` - error: No overload variant of "Field" matches argument types "str", "int", "int" [call-overload]
  - ID: c9086e53
- `packages/haive-agents/src/haive/agents/memory_v2/standalone_rag_memory.py:670` - error: No overload variant of "tool" matches argument types "str", "str" [call-overload]
  - ID: 2add17e4
- `packages/haive-agents/src/haive/agents/memory_v2/multi_memory_coordinator.py:641` - error: No overload variant of "**setitem**" of "list" matches argument types "str", "Any | BaseExcep
  - ID: 5c37702d
- `packages/haive-agents/src/haive/agents/memory_v2/multi_memory_coordinator.py:655` - error: No overload variant of "**setitem**" of "list" matches argument types "str", "Any" [call-ove
  - ID: 3c3033f8
- `packages/haive-agents/src/haive/agents/memory_v2/long_term_memory_agent.py:475` - error: No overload variant of "tool" matches argument types "str", "str" [call-overload]
  - ID: 7ed97090
- ... and 15 more

### haive-core

- `packages/haive-core/src/haive/core/utils/haive_discovery/utils.py:421` - error: No overload variant of "dict" matches argument type "object" [call-overload]
  - ID: e7963487
- `packages/haive-core/src/haive/core/utils/haive_discovery/utils.py:422` - error: No overload variant of "dict" matches argument type "object" [call-overload]
  - ID: 08aa8c1c
- `packages/haive-core/src/haive/core/registry/dynamic_registry.py:548` - error: No overload variant of "get" of "dict" matches argument types "str", "str" [call-overload]
  - ID: fce28f7d
- `packages/haive-core/src/haive/core/schema/compatibility/langchain_converters.py:69` - error: No overload variant of "get" of "dict" matches argument types "type", "int" [call-overload]
  - ID: ba9f325b
- `packages/haive-core/src/haive/core/schema/compatibility/langchain_converters.py:70` - error: No overload variant of "get" of "dict" matches argument types "type", "int" [call-overload]
  - ID: 093269dd
- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:239` - error: No overload variant of "**setitem**" of "list" matches argument types "str", "str" [call-ove
  - ID: d15fd47e
- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:243` - error: No overload variant of "**setitem**" of "list" matches argument types "str", "str" [call-ove
  - ID: fb03f425
- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:267` - error: No overload variant of "**setitem**" of "list" matches argument types "str", "str" [call-ove
  - ID: cb32b3a9
- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:271` - error: No overload variant of "**setitem**" of "list" matches argument types "str", "str" [call-ove
  - ID: fb6c107a
- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:354` - error: No overload variant of "**setitem**" of "list" matches argument types "str", "str" [call-ove
  - ID: 1adda6b9
- ... and 16 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py:206` - error: No overload variant of "**getitem**" of "list" matches argument type "str" [call-overload]
  - ID: 8bc878a9
- `packages/haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py:207` - error: No overload variant of "**getitem**" of "list" matches argument type "str" [call-overload]
  - ID: d73b7ef1
- `packages/haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py:208` - error: No overload variant of "**getitem**" of "list" matches argument type "str" [call-overload]
  - ID: 9dfd1832
- `packages/haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py:213` - error: No overload variant of "**getitem**" of "list" matches argument type "str" [call-overload]
  - ID: 6cdcf559
- `packages/haive-dataflow/src/haive/dataflow/base.py:139` - error: No overload variant of "Field" matches argument types "EllipsisType", "str", "str" [call-ove
  - ID: c1fb047c
- `packages/haive-dataflow/src/haive/dataflow/api/base.py:139` - error: No overload variant of "Field" matches argument types "EllipsisType", "str", "str" [call-ove
  - ID: 25d356c6
- `packages/haive-dataflow/src/haive/dataflow/api/routes/llm_routes.py:114` - error: No overload variant of "Field" matches argument types "EllipsisType", "str", "str" [call-ove
  - ID: eb040981

### haive-games

- `packages/haive-games/src/haive/games/reversi/state_manager.py:51` - error: No overload variant of "**setitem**" of "list" matches argument types "int", "str" [call-ove
  - ID: b541c1dd
- `packages/haive-games/src/haive/games/reversi/state_manager.py:52` - error: No overload variant of "**setitem**" of "list" matches argument types "int", "str" [call-ove
  - ID: 8998ecac
- `packages/haive-games/src/haive/games/reversi/state_manager.py:53` - error: No overload variant of "**setitem**" of "list" matches argument types "int", "str" [call-ove
  - ID: b296edb8
- `packages/haive-games/src/haive/games/reversi/state_manager.py:54` - error: No overload variant of "**setitem**" of "list" matches argument types "int", "str" [call-ove
  - ID: 37ea7120
- `packages/haive-games/src/haive/games/mastermind/state.py:96` - error: No overload variant of "Field" matches argument types "EllipsisType", "int", "int", "str" [c
  - ID: 4b6aa213
- `packages/haive-games/src/haive/games/mastermind/models.py:163` - error: No overload variant of "Field" matches argument types "EllipsisType", "int", "int", "str" [c
  - ID: fd978acf
- `packages/haive-games/src/haive/games/mastermind/models.py:240` - error: No overload variant of "Field" matches argument types "EllipsisType", "int", "int", "str" [c
  - ID: 01390e7d
- `packages/haive-games/src/haive/games/dominoes/state.py:190` - error: No overload variant of "Field" matches argument types "EllipsisType", "int", "int", "str" [c
  - ID: 91724dd8
- `packages/haive-games/src/haive/games/debate_v2/judges.py:421` - error: No overload variant of "sort" of "list" matches argument type "bool" [call-overload]
  - ID: 0a7d035a
- `packages/haive-games/src/haive/games/core/components/cards/standard.py:67` - error: No overload variant of "field_validator" matches argument types "str", "bool", "bool" [call-
  - ID: b48f2be5
- ... and 3 more

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:143` - error: No overload variant of "Field" matches argument types "str", "int", "int" [call-overload]
  - ID: 62b07e44
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:176` - error: No overload variant of "Field" matches argument types "str", "int" [call-overload]
  - ID: eb1ea41a
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:177` - error: No overload variant of "Field" matches argument types "str", "int" [call-overload]
  - ID: c83947ee
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:200` - error: No overload variant of "Field" matches argument types "str", "int" [call-overload]
  - ID: 25485516
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:201` - error: No overload variant of "Field" matches argument types "str", "int" [call-overload]
  - ID: c6a1be82
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/models.py:101` - error: No overload variant of "Field" matches argument types "str", "int", "int" [call-overload]
  - ID: a0350863
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/models.py:122` - error: No overload variant of "Field" matches argument types "str", "int", "int" [call-overload]
  - ID: 46eef27b
- `packages/haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:380` - error: No overload variant of "**getitem**" of "list" matches argument type "str" [call-overload]
  - ID: 84f3a640

## mypy:dict-item (15 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_v3.py:437` - error: Dict entry 3 has incompatible type "str": "None"; expected "str": "float" [dict-item]
  - ID: 400ac4c8
- `packages/haive-agents/src/haive/agents/multi/enhanced/multi_agent_v3.py:484` - error: Dict entry 3 has incompatible type "str": "None"; expected "str": "float" [dict-item]
  - ID: 33ed8d4f
- `packages/haive-agents/src/haive/agents/memory_reorganized/api/unified_memory_api.py:974` - error: Dict entry 1 has incompatible type "str": "int"; expected "str": "str" [dict-item]
  - ID: 0d66c683
- `packages/haive-agents/src/haive/agents/memory/unified_memory_api.py:972` - error: Dict entry 1 has incompatible type "str": "int"; expected "str": "str" [dict-item]
  - ID: 862bfe41
- `packages/haive-agents/src/haive/agents/rag/simple/enhanced_v3/state.py:244` - error: Dict entry 0 has incompatible type "str": "int | None"; expected "str": "int" [dict-item]
  - ID: dda89406
- `packages/haive-agents/src/haive/agents/rag/simple/enhanced_v3/state.py:245` - error: Dict entry 1 has incompatible type "str": "int | None"; expected "str": "int" [dict-item]
  - ID: b1c7e264
- `packages/haive-agents/src/haive/agents/rag/simple/enhanced_v3/state.py:246` - error: Dict entry 2 has incompatible type "str": "int | None"; expected "str": "int" [dict-item]
  - ID: 9ef4b5c6
- `packages/haive-agents/src/haive/agents/rag/simple/enhanced_v3/state.py:247` - error: Dict entry 3 has incompatible type "str": "float | None"; expected "str": "int" [dict-item]
  - ID: 5a950541
- `packages/haive-agents/src/haive/agents/rag/simple/enhanced_v3/state.py:248` - error: Dict entry 4 has incompatible type "str": "str | None"; expected "str": "int" [dict-item]
  - ID: a1d55bcd

### haive-core

- `packages/haive-core/src/haive/core/common/mixins/identifier.py:232` - error: Dict entry 4 has incompatible type "str": "bool"; expected "str": "str" [dict-item]
  - ID: 74827d57
- `packages/haive-core/src/haive/core/graph/node/practical_stateful_example.py:76` - error: Dict entry 0 has incompatible type "str": "Any | None"; expected "str": "str" [dict-item]
  - ID: cf82f840
- `packages/haive-core/src/haive/core/graph/node/practical_stateful_example.py:77` - error: Dict entry 1 has incompatible type "str": "Any | None"; expected "str": "str" [dict-item]
  - ID: 551fb30b

### haive-games

- `packages/haive-games/src/haive/games/debate/factory.py:138` - error: Dict entry 0 has incompatible type "str": "Any | None"; expected "str": "str" [dict-item]
  - ID: 224c2f65
- `packages/haive-games/src/haive/games/debate/factory.py:139` - error: Dict entry 1 has incompatible type "str": "Any | None"; expected "str": "str" [dict-item]
  - ID: 247e15d5
- `packages/haive-games/src/haive/games/debate/state_manager.py:213` - error: Dict entry 1 has incompatible type "str": "bool"; expected "str": "str" [dict-item]
  - ID: 907f444d

## mypy:dict[Any, Any (16 errors)

### haive-core

- `packages/haive-core/src/haive/core/schema/prebuilt/messages_state.py:298` - error: Returning Any from function declared to return "list[dict[Any, Any]]" [no-any-return]
  - ID: 31db2258
- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:525` - error: Returning Any from function declared to return "list[dict[Any, Any]]" [no-any-return]
  - ID: b3ea0053
- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:841` - error: Argument "root" to "MessageList" has incompatible type "list[dict[Any, Any]]"; expected "list
  - ID: 66920e4e
- `packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py:2053` - error: Argument 3 to "getattr" has incompatible type "type[dict[Any, Any]]"; expected "type[BaseMode
  - ID: 4e661dfb
- `packages/haive-core/src/haive/core/graph/state_graph/conversion/langgraph.py:45` - error: Incompatible types in assignment (expression has type "type[dict[Any, Any]]", variable has ty
  - ID: 0b66d43a

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/db/supabase.py:221` - error: Returning Any from function declared to return "list[dict[Any, Any]]" [no-any-return]
  - ID: 34dbc3d1
- `packages/haive-dataflow/src/haive/dataflow/db/supabase.py:246` - error: Returning Any from function declared to return "list[dict[Any, Any]]" [no-any-return]
  - ID: 1b434a54
- `packages/haive-dataflow/src/haive/dataflow/db/supabase.py:272` - error: Returning Any from function declared to return "list[dict[Any, Any]]" [no-any-return]
  - ID: 5f5e8e54
- `packages/haive-dataflow/src/haive/dataflow/db/supabase.py:293` - error: Returning Any from function declared to return "list[dict[Any, Any]]" [no-any-return]
  - ID: 88b6360a

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/poetry_db_toolkit.py:55` - error: Returning Any from function declared to return "list[dict[Any, Any]]" [no-any-return]
  - ID: 92131458
- `packages/haive-tools/src/haive/tools/tools/toolkits/poetry_db_toolkit.py:134` - error: Returning Any from function declared to return "list[dict[Any, Any]]" [no-any-return]
  - ID: 0529f2fe
- `packages/haive-tools/src/haive/tools/tools/toolkits/poetry_db_toolkit.py:173` - error: Returning Any from function declared to return "list[dict[Any, Any]]" [no-any-return]
  - ID: e663670f
- `packages/haive-tools/src/haive/tools/tools/toolkits/free_to_game_toolkit.py:82` - error: Returning Any from function declared to return "list[dict[Any, Any]]" [no-any-return]
  - ID: c5145adc
- `packages/haive-tools/src/haive/tools/tools/toolkits/free_to_game_toolkit.py:149` - error: Returning Any from function declared to return "list[dict[Any, Any]]" [no-any-return]
  - ID: c7b7fd2f
- `packages/haive-tools/src/haive/tools/tools/toolkits/yugiioh_toolkit.py:104` - error: Returning Any from function declared to return "list[dict[Any, Any]]" [no-any-return]
  - ID: 210a0406
- `packages/haive-tools/src/haive/tools/tools/toolkits/yugiioh_toolkit.py:117` - error: Returning Any from function declared to return "list[dict[Any, Any]]" [no-any-return]
  - ID: 1f317011

## mypy:dict[str, Any (61 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/base/typed_agent.py:496` - error: Argument 2 to "ReactiveAgent" has incompatible type "Any | None"; expected "list[dict[str, An
  - ID: aa0f8c10
- `packages/haive-agents/src/haive/agents/planning/rewoo/models/join_step.py:334` - error: Dict entry 2 has incompatible type "str": "list[dict[str, Any]]"; expected "str": "str" [dic
  - ID: 58ae00d4
- `packages/haive-agents/src/haive/agents/react_class/react_agent2/tool_utils.py:43` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: d77443d5
- `packages/haive-agents/src/haive/agents/react_class/react_agent2/tool_utils.py:48` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: 80565619
- `packages/haive-agents/src/haive/agents/memory_reorganized/coordination/multi_agent_coordinator.py:1342` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: ae747122
- `packages/haive-agents/src/haive/agents/memory_reorganized/coordination/agentic_rag_coordinator.py:1239` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: 6b69d1d4
- `packages/haive-agents/src/haive/agents/memory_reorganized/coordination/agentic_rag_coordinator.py:1241` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: 8d4917ad
- `packages/haive-agents/src/haive/agents/memory_reorganized/coordination/agentic_rag_coordinator.py:1262` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: a99c369a
- `packages/haive-agents/src/haive/agents/memory_reorganized/coordination/agentic_rag_coordinator.py:1264` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: 6c49ada7
- `packages/haive-agents/src/haive/agents/memory_reorganized/coordination/agentic_rag_coordinator.py:1280` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: beb7181b
- ... and 12 more

### haive-core

- `packages/haive-core/src/haive/core/schema/prebuilt/messages/utils.py:129` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: 9230c54c
- `packages/haive-core/src/haive/core/graph/node/validation_node_with_routing.py:309` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: 50c8f3f4
- `packages/haive-core/src/haive/core/graph/node/state_updating_validation_node.py:189` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: c1895e51
- `packages/haive-core/src/haive/core/graph/node/state_updating_validation_node.py:201` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: 2b47769f
- `packages/haive-core/src/haive/core/graph/node/routing_validation_node.py:150` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: eb78682f
- `packages/haive-core/src/haive/core/graph/node/routing_validation_node.py:165` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: 5630970d
- `packages/haive-core/src/haive/core/graph/node/composer/advanced_node_composer.py:206` - error: Incompatible default for argument "config_type" (default has type "type[dict[str, Any]]", arg
  - ID: 21388c06
- `packages/haive-core/src/haive/core/persistence/postgres_saver_with_thread_creation.py:66` - error: "BaseConnection[dict[str, Any]]" not callable [operator]
  - ID: 9b9845ac
- `packages/haive-core/src/haive/core/persistence/factory.py:102` - error: Argument 1 to "ShallowPostgresSaver" has incompatible type "Any | None"; expected "Connection
  - ID: 60aa6c40
- `packages/haive-core/src/haive/core/persistence/factory.py:204` - error: Argument 1 to "AsyncShallowPostgresSaver" has incompatible type "Any | None"; expected "Async
  - ID: c5378be8

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/core.py:1331` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: 2ed867fc
- `packages/haive-dataflow/src/haive/dataflow/core.py:1409` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: e28c95ce
- `packages/haive-dataflow/src/haive/dataflow/core.py:1518` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: 520e0172
- `packages/haive-dataflow/src/haive/dataflow/core.py:1552` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: 8db1d921
- `packages/haive-dataflow/src/haive/dataflow/core.py:1618` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: 1cb0ba62
- `packages/haive-dataflow/src/haive/dataflow/registry/registries/model_registry.py:709` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: fd217bea
- `packages/haive-dataflow/src/haive/dataflow/registry/registries/model_registry.py:726` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: 1402ad4d
- `packages/haive-dataflow/src/haive/dataflow/registry/registries/model_registry.py:763` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: 607a1dae
- `packages/haive-dataflow/src/haive/dataflow/registries/model_registry.py:709` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: f19a0695
- `packages/haive-dataflow/src/haive/dataflow/registries/model_registry.py:726` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: 85229885
- ... and 7 more

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/tools/server_selector.py:142` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: 35932259
- `packages/haive-mcp/src/haive/mcp/tools/server_selector.py:153` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: 8b6b90ea
- `packages/haive-mcp/src/haive/mcp/fastmcp_runner.py:327` - error: "list[dict[str, Any]]" has no attribute "items" [attr-defined]
  - ID: 4aa4ca3a
- `packages/haive-mcp/src/haive/mcp/enhance_mcp_data.py:241` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: c069605a
- `packages/haive-mcp/src/haive/mcp/downloader/legacy_core.py:642` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: 1a03c488
- `packages/haive-mcp/src/haive/mcp/csv_viewer.py:29` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: 3e9b1e6b
- `packages/haive-mcp/src/haive/mcp/fastapi_mcp_server.py:243` - error: List comprehension has incompatible type List[dict[str, Any]]; expected List[str] [misc]
  - ID: 3c9ab14d
- `packages/haive-mcp/src/haive/mcp/fastapi_mcp_server.py:262` - error: List comprehension has incompatible type List[dict[str, Any]]; expected List[str] [misc]
  - ID: 00d663d0
- `packages/haive-mcp/src/haive/mcp/fastapi_mcp_server.py:270` - error: List comprehension has incompatible type List[dict[str, Any]]; expected List[str] [misc]
  - ID: 024c4235

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:605` - error: Incompatible types in assignment (expression has type "None", variable has type "list[dict[st
  - ID: 758708a2
- `packages/haive-tools/src/haive/tools/tools/toolkits/jira_toolkit.py:116` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: 2f5bb001
- `packages/haive-tools/src/haive/tools/tools/toolkits/jira_toolkit.py:158` - error: Returning Any from function declared to return "list[dict[str, Any]]" [no-any-return]
  - ID: 43adbadf

## mypy:dict[str, Sequence[str (1 errors)

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/tools.py:408` - error: Incompatible return value type (got "list[dict[str, Sequence[str]]]", expected "list[dict[str
  - ID: 1c2e1e70

## mypy:dict[str, list[str (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/graph/ToolManager.py:623` - error: Incompatible return value type (got "list[dict[str, list[str] | str | Any | None]]", expected
  - ID: cd474ecc

## mypy:dict[str, object (2 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/retriever/providers/CohereRagRetrieverConfig.py:206` - error: Dict entry 1 has incompatible type "str": "float"; expected "str": "int | list[dict[str, obje
  - ID: 13022f65
- `packages/haive-core/src/haive/core/engine/retriever/providers/CohereRagRetrieverConfig.py:207` - error: Dict entry 2 has incompatible type "str": "str"; expected "str": "int | list[dict[str, object
  - ID: e300975d

## mypy:dict[str, str (1 errors)

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:192` - error: Argument "content" to "AIMessage" has incompatible type "list[dict[str, str]]"; expected "str
  - ID: ca05cbd2

## mypy:empty-body (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/schema/prebuilt/structured_output_state.py:195` - error: Missing return statement [empty-body]
  - ID: fe8d0e36

## mypy:error (8713 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/wiki_writer/utils.py:0` -
  - ID: dd6c05bc
- `packages/haive-agents/src/haive/agents/wiki_writer/utils.py:0` -
  - ID: dd6c05bc
- `packages/haive-agents/src/haive/agents/wiki_writer/utils.py:0` -
  - ID: dd6c05bc
- `packages/haive-agents/src/haive/agents/wiki_writer/interview/utils.py:0` -
  - ID: 01ba3dd4
- `packages/haive-agents/src/haive/agents/wiki_writer/interview/utils.py:0` -
  - ID: 01ba3dd4
- `packages/haive-agents/src/haive/agents/wiki_writer/interview/utils.py:0` -
  - ID: 01ba3dd4
- `packages/haive-agents/src/haive/agents/task_analysis/tree/models.py:0` -
  - ID: dcd8779e
- `packages/haive-agents/src/haive/agents/task_analysis/tree/models.py:0` -
  - ID: dcd8779e
- `packages/haive-agents/src/haive/agents/task_analysis/tree/models.py:26` - note: Use "-> None" if function does not return a value
  - ID: ed42c6ef
- `packages/haive-agents/src/haive/agents/task_analysis/tree/models.py:0` -
  - ID: dcd8779e
- ... and 3197 more

### haive-core

- `packages/haive-core/src/haive/core/errors.py:0` -
  - ID: 120f0503
- `packages/haive-core/src/haive/core/utils/visualize_graph_utils.py:0` -
  - ID: 0f8daecb
- `packages/haive-core/src/haive/core/utils/state_utils.py:0` -
  - ID: 330e7a56
- `packages/haive-core/src/haive/core/utils/getter_mixin.py:0` -
  - ID: d5eb97e8
- `packages/haive-core/src/haive/core/utils/getter_mixin.py:0` -
  - ID: d5eb97e8
- `packages/haive-core/src/haive/core/utils/pydantic_utils/sync_properties.py:0` -
  - ID: a4080e22
- `packages/haive-core/src/haive/core/utils/debugkit/debugging.py:0` -
  - ID: 142d00a5
- `packages/haive-core/src/haive/core/utils/debugkit/debugging.py:43` - note: Use "-> None" if function does not return a value
  - ID: 38ee36b4
- `packages/haive-core/src/haive/core/utils/debugkit/debugging.py:0` -
  - ID: 142d00a5
- `packages/haive-core/src/haive/core/utils/debugkit/debugging.py:0` -
  - ID: 142d00a5
- ... and 2589 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/db/inspect_supabase.py:0` -
  - ID: 37793fc8
- `packages/haive-dataflow/src/haive/dataflow/db/inspect_supabase.py:10` - note: Use "-> None" if function does not return a value
  - ID: 1a74e9ce
- `packages/haive-dataflow/src/haive/dataflow/__init__.py:45` - note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
  - ID: 62749808
- `packages/haive-dataflow/src/haive/dataflow/__init__.py:0` -
  - ID: 67c015e1
- `packages/haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:0` -
  - ID: 21aa7845
- `packages/haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:35` - note: Use "-> None" if function does not return a value
  - ID: fefab567
- `packages/haive-dataflow/src/haive/dataflow/providers/agent_provider.py:0` -
  - ID: 35b73a40
- `packages/haive-dataflow/src/haive/dataflow/providers/agent_provider.py:35` - note: Use "-> None" if function does not return a value
  - ID: e7c14d54
- `packages/haive-dataflow/src/haive/dataflow/core.py:0` -
  - ID: 7ac408d9
- `packages/haive-dataflow/src/haive/dataflow/core.py:74` - note: Use "-> None" if function does not return a value
  - ID: b05164f6
- ... and 602 more

### haive-games

- `packages/haive-games/src/haive/games/llm_config_factory.py:0` -
  - ID: 17e29c24
- `packages/haive-games/src/haive/games/tic_tac_toe/state_manager.py:0` -
  - ID: 36a44366
- `packages/haive-games/src/haive/games/tic_tac_toe/state_manager.py:0` -
  - ID: 36a44366
- `packages/haive-games/src/haive/games/single_player/example.py:0` -
  - ID: 8422ef20
- `packages/haive-games/src/haive/games/single_player/example.py:1` - note: PEP 484 prohibits implicit Optional. Accordingly, mypy has changed its default to no*implicit*
  - ID: f6e15efe
- `packages/haive-games/src/haive/games/single_player/example.py:1` - note: PEP 484 prohibits implicit Optional. Accordingly, mypy has changed its default to no*implicit*
  - ID: f6e15efe
- `packages/haive-games/src/haive/games/single_player/example.py:0` -
  - ID: 8422ef20
- `packages/haive-games/src/haive/games/reversi/state_manager.py:0` -
  - ID: 5cc8122f
- `packages/haive-games/src/haive/games/reversi/state_manager.py:51` - note: Possible overload variants:
  - ID: a732264a
- `packages/haive-games/src/haive/games/reversi/state_manager.py:51` - note: Possible overload variants:
  - ID: a732264a
- ... and 1507 more

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/discovery/server_discovery.py:0` -
  - ID: 40854195
- `packages/haive-mcp/src/haive/mcp/discovery/server_discovery.py:9` - note: Use "-> None" if function does not return a value
  - ID: 249f45e4
- `packages/haive-mcp/src/haive/mcp/__init__.py:3` - note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
  - ID: 46129cbb
- `packages/haive-mcp/src/haive/mcp/launcher.py:0` -
  - ID: 4ee7cd3c
- `packages/haive-mcp/src/haive/mcp/launcher.py:13` - note: Use "-> None" if function does not return a value
  - ID: 066db0f0
- `packages/haive-mcp/src/haive/mcp/launcher.py:0` -
  - ID: 4ee7cd3c
- `packages/haive-mcp/src/haive/mcp/launcher.py:19` - note: Use "-> None" if function does not return a value
  - ID: 3f664a88
- `packages/haive-mcp/src/haive/mcp/launcher.py:0` -
  - ID: 4ee7cd3c
- `packages/haive-mcp/src/haive/mcp/launcher.py:25` - note: Use "-> None" if function does not return a value
  - ID: 69ed0a94
- `packages/haive-mcp/src/haive/mcp/launcher.py:0` -
  - ID: 4ee7cd3c
- ... and 351 more

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/project_manager/aug_llms.py:0` -
  - ID: b3f99a7c
- `packages/haive-prebuilt/src/haive/prebuilt/project_manager/aug_llms.py:0` -
  - ID: b3f99a7c
- `packages/haive-prebuilt/src/haive/prebuilt/ai_insight/example.py:0` -
  - ID: 01bf5461
- `packages/haive-prebuilt/src/haive/prebuilt/ai_insight/example.py:0` -
  - ID: 01bf5461
- `packages/haive-prebuilt/src/haive/prebuilt/ai_insight/example.py:62` - note: Use "-> None" if function does not return a value
  - ID: 6464c273
- `packages/haive-prebuilt/src/haive/prebuilt/ai_insight/example.py:0` -
  - ID: 01bf5461
- `packages/haive-prebuilt/src/haive/prebuilt/ai_insight/example.py:112` - note: Use "-> None" if function does not return a value
  - ID: a7939cc8
- `packages/haive-prebuilt/src/haive/prebuilt/ai_insight/example.py:0` -
  - ID: 01bf5461
- `packages/haive-prebuilt/src/haive/prebuilt/ai_insight/example.py:157` - note: Use "-> None" if function does not return a value
  - ID: c1ab627e
- `packages/haive-prebuilt/src/haive/prebuilt/__init__.py:120` - note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
  - ID: e3cf1434
- ... and 240 more

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/remote_execution.py:14` - note: Hint: "python3 -m pip install types-paramiko"
  - ID: 6d1aead1
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/remote_execution.py:14` - note: Hint: "python3 -m pip install types-paramiko"
  - ID: 6d1aead1
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/remote_execution.py:0` -
  - ID: dbc8a640
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/remote_execution.py:27` - note: Use "-> None" if function does not return a value
  - ID: ab458797
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/remote_execution.py:0` -
  - ID: dbc8a640
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/remote_execution.py:0` -
  - ID: dbc8a640
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/remote_execution.py:41` - note: Use "-> None" if function does not return a value
  - ID: 4d7e4871
- `packages/haive-tools/src/haive/tools/__init__.py:79` - note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
  - ID: 8cabb5c2
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/logger.py:0` -
  - ID: df64ce77
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/logger.py:0` -
  - ID: df64ce77
- ... and 157 more

## mypy:float, dict[str, float (2 errors)

### haive-core

- `packages/haive-core/src/haive/core/utils/debugkit/benchmarking/timing.py:133` - error: Argument 1 to "\_display_comparison" of "TimingBenchmark" has incompatible type "dict[float, d
  - ID: b24ce74a
- `packages/haive-core/src/haive/core/utils/debugkit/benchmarking/timing.py:134` - error: Incompatible return value type (got "dict[float, dict[str, float]]", expected "dict[str, dict
  - ID: da8dfcac

## mypy:func-returns-value (5 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/experiments/static_supervisor_with_sync.py:179` - error: "\_update_engine_tools" of "StaticSupervisor" does not return a value (it only ever returns No
  - ID: 0a441653
- `packages/haive-agents/src/haive/agents/planning/llm_compiler/agent.py:539` - error: "main" does not return a value (it only ever returns None) [func-returns-value]
  - ID: 36d95283

### haive-core

- `packages/haive-core/src/haive/core/persistence/postgres_saver_with_thread_creation.py:285` - error: "put_writes" of "AsyncPostgresSaver" does not return a value (it only ever returns None) [fu
  - ID: b83c79c6

### haive-games

- `packages/haive-games/src/haive/games/dominoes/ui.py:306` - error: "split" of "Layout" does not return a value (it only ever returns None) [func-returns-value]
  - ID: 5851eab5

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/servers/dataflow_server.py:364` - error: "run" of "FastMCP" does not return a value (it only ever returns None) [func-returns-value]
  - ID: 2d8dcb4a

## mypy:has-type (122 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/multi/experiments/implementations/compatibility_enhanced_base.py:102` - error: Cannot determine type of "agents" [has-type]
  - ID: c8cbbf96
- `packages/haive-agents/src/haive/agents/multi/experiments/implementations/compatibility_enhanced_base.py:128` - error: Cannot determine type of "agents" [has-type]
  - ID: 46c9aa3a
- `packages/haive-agents/src/haive/agents/multi/archive/experiments/implementations/compatibility_enhanced_base.py:102` - error: Cannot determine type of "agents" [has-type]
  - ID: a298b382
- `packages/haive-agents/src/haive/agents/multi/archive/experiments/implementations/compatibility_enhanced_base.py:128` - error: Cannot determine type of "agents" [has-type]
  - ID: e14a8598
- `packages/haive-agents/src/haive/agents/supervisor/compatibility_bridge.py:39` - error: Cannot determine type of "agents" [has-type]
  - ID: 3ae46f36
- `packages/haive-agents/src/haive/agents/supervisor/compatibility_bridge.py:59` - error: Cannot determine type of "agents" [has-type]
  - ID: a1c2335e
- `packages/haive-agents/src/haive/agents/supervisor/compatibility_bridge.py:81` - error: Cannot determine type of "agents" [has-type]
  - ID: be872f29
- `packages/haive-agents/src/haive/agents/supervisor/compatibility_bridge.py:150` - error: Cannot determine type of "agents" [has-type]
  - ID: d9a92d8c
- `packages/haive-agents/src/haive/agents/supervisor/utils/compatibility_bridge.py:39` - error: Cannot determine type of "agents" [has-type]
  - ID: 666b99fe
- `packages/haive-agents/src/haive/agents/supervisor/utils/compatibility_bridge.py:59` - error: Cannot determine type of "agents" [has-type]
  - ID: bde7ea44
- ... and 58 more

### haive-core

- `packages/haive-core/src/haive/core/schema/typed_state_schema.py:150` - error: Cannot determine type of "engine" [has-type]
  - ID: bb89b6a7
- `packages/haive-core/src/haive/core/engine/aug_llm/mcp_config.py:112` - error: Cannot determine type of "tools" [has-type]
  - ID: 304443ad
- `packages/haive-core/src/haive/core/engine/aug_llm/mcp_config.py:130` - error: Cannot determine type of "system_message" [has-type]
  - ID: 409c91f5
- `packages/haive-core/src/haive/core/engine/aug_llm/mcp_config.py:131` - error: Cannot determine type of "system_message" [has-type]
  - ID: 3a44d32a
- `packages/haive-core/src/haive/core/engine/aug_llm/mcp_config.py:151` - error: Cannot determine type of "tools" [has-type]
  - ID: 29289f73
- `packages/haive-core/src/haive/core/schema/prebuilt/tool_state.py:85` - error: Cannot determine type of "tools" [has-type]
  - ID: 9a5bcd11
- `packages/haive-core/src/haive/core/schema/prebuilt/tool_state.py:87` - error: Cannot determine type of "tool_routes" [has-type]
  - ID: d14555b4
- `packages/haive-core/src/haive/core/schema/prebuilt/tool_state.py:91` - error: Cannot determine type of "tool_metadata" [has-type]
  - ID: f4fd9c51
- `packages/haive-core/src/haive/core/schema/prebuilt/tool_state.py:96` - error: Cannot determine type of "tool_instances" [has-type]
  - ID: bafd9240
- `packages/haive-core/src/haive/core/schema/prebuilt/tool_state.py:99` - error: Cannot determine type of "tools_dict" [has-type]
  - ID: a1c5c5c7
- ... and 30 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/registry/db.py:83` - error: Cannot determine type of "\_tables_created" [has-type]
  - ID: 8d3ac31b
- `packages/haive-dataflow/src/haive/dataflow/registry/db.py:106` - error: Cannot determine type of "\_tables_created" [has-type]
  - ID: 107eab08
- `packages/haive-dataflow/src/haive/dataflow/registry/base.py:74` - error: Cannot determine type of "\_discovered" [has-type]
  - ID: ad5601fc
- `packages/haive-dataflow/src/haive/dataflow/registry/base.py:189` - error: Cannot determine type of "\_discovered" [has-type]
  - ID: a2f31200
- `packages/haive-dataflow/src/haive/dataflow/registry/base.py:286` - error: Cannot determine type of "\_discovered" [has-type]
  - ID: ce2cf4bd
- `packages/haive-dataflow/src/haive/dataflow/registry/base.py:337` - error: Cannot determine type of "\_discovered" [has-type]
  - ID: 30e45123
- `packages/haive-dataflow/src/haive/dataflow/registry/base.py:412` - error: Cannot determine type of "\_discovered" [has-type]
  - ID: 8a08ad7e

### haive-games

- `packages/haive-games/src/haive/games/hold_em/engine_logging.py:276` - error: Cannot determine type of "invoke" [has-type]
  - ID: 512ad60a
- `packages/haive-games/src/haive/games/single_player/logic_grid/base.py:237` - error: Cannot determine type of "status" [has-type]
  - ID: ba693da5
- `packages/haive-games/src/haive/games/single_player/flow_free/base.py:453` - error: Cannot determine type of "status" [has-type]
  - ID: d0c8187b
- `packages/haive-games/src/haive/games/single_player/crossword_puzzle/base.py:117` - error: Cannot determine type of "status" [has-type]
  - ID: 74868fbf

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/mixins/mcp_mixin.py:174` - error: Cannot determine type of "engine" [has-type]
  - ID: 918963ae
- `packages/haive-mcp/src/haive/mcp/mixins/mcp_mixin.py:177` - error: Cannot determine type of "engine" [has-type]
  - ID: b0779d85
- `packages/haive-mcp/src/haive/mcp/integration/aug_llm_mcp_extension.py:175` - error: Cannot determine type of "tools" [has-type]
  - ID: 2c997910

## mypy:import-not-found (188 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/wiki_writer/interview/__init__.py:3` - error: Cannot find implementation or library stub for module named "interview.agent" [import-not-fo
  - ID: 941aabae
- `packages/haive-agents/src/haive/agents/wiki_writer/interview/__init__.py:4` - error: Cannot find implementation or library stub for module named "interview.models" [import-not-f
  - ID: 71ea4b6a
- `packages/haive-agents/src/haive/agents/wiki_writer/interview/__init__.py:5` - error: Cannot find implementation or library stub for module named "interview.state" [import-not-fo
  - ID: 1e4d37ac
- `packages/haive-agents/src/haive/agents/wiki_writer/interview/__init__.py:6` - error: Cannot find implementation or library stub for module named "interview.utils" [import-not-fo
  - ID: ba6dc7cf
- `packages/haive-agents/src/haive/agents/wiki_writer/__init__.py:3` - error: Cannot find implementation or library stub for module named "wiki_writer.agent" [import-not-
  - ID: 676da81c
- `packages/haive-agents/src/haive/agents/wiki_writer/__init__.py:4` - error: Cannot find implementation or library stub for module named "wiki_writer.models" [import-not
  - ID: 834bff52
- `packages/haive-agents/src/haive/agents/wiki_writer/__init__.py:14` - error: Cannot find implementation or library stub for module named "wiki_writer.state" [import-not-
  - ID: 4d400315
- `packages/haive-agents/src/haive/agents/wiki_writer/__init__.py:15` - error: Cannot find implementation or library stub for module named "wiki_writer.utils" [import-not-
  - ID: e1755a95
- `packages/haive-agents/src/haive/agents/task_analysis/tree/__init__.py:3` - error: Cannot find implementation or library stub for module named "tree.models" [import-not-found]
  - ID: 6ac6605e
- `packages/haive-agents/src/haive/agents/task_analysis/execution/__init__.py:3` - error: Cannot find implementation or library stub for module named "execution.models" [import-not-f
  - ID: 23545012
- ... and 75 more

### haive-core

- `packages/haive-core/src/haive/core/models/llm/export_llm_models_to_csv.py:21` - error: Cannot find implementation or library stub for module named "base" [import-not-found]
  - ID: b41928a5
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:26` - error: Cannot find implementation or library stub for module named "radon.complexity" [import-not-f
  - ID: 2d2d5e45
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:26` - error: Cannot find implementation or library stub for module named "radon.complexity" [import-not-f
  - ID: 2d2d5e45
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:27` - error: Cannot find implementation or library stub for module named "radon.metrics" [import-not-foun
  - ID: b5eaf6b1
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:28` - error: Cannot find implementation or library stub for module named "radon.visitors" [import-not-fou
  - ID: fbdb6321
- `packages/haive-core/src/haive/core/utils/debugkit/debug/interactive.py:33` - error: Cannot find implementation or library stub for module named "pudb" [import-not-found]
  - ID: 99848874
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/static.py:34` - error: Cannot find implementation or library stub for module named "radon.complexity" [import-not-f
  - ID: 538583d4
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/static.py:34` - error: Cannot find implementation or library stub for module named "radon.complexity" [import-not-f
  - ID: 538583d4
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/static.py:35` - error: Cannot find implementation or library stub for module named "radon.metrics" [import-not-foun
  - ID: 236932b1
- `packages/haive-core/src/haive/core/models/llm/providers/xai.py:100` - error: Cannot find implementation or library stub for module named "langchain_xai" [import-not-foun
  - ID: ae7e9eb1
- ... and 34 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/api/run_chess_api.py:23` - error: Cannot find implementation or library stub for module named "game_api" [import-not-found]
  - ID: 98423729
- `packages/haive-dataflow/src/haive/dataflow/api/run_simple.py:13` - error: Cannot find implementation or library stub for module named "game_router" [import-not-found]
  - ID: 2e355453
- `packages/haive-dataflow/src/haive/dataflow/tic_tac_toe_api.py:10` - error: Cannot find implementation or library stub for module named "haive_games.tic_tac_toe.agent"
  - ID: 6d9bfea4
- `packages/haive-dataflow/src/haive/dataflow/tic_tac_toe_api.py:11` - error: Cannot find implementation or library stub for module named "haive_games.tic_tac_toe.config"
  - ID: e69ef8d6
- `packages/haive-dataflow/src/haive/dataflow/tic_tac_toe_api.py:12` - error: Cannot find implementation or library stub for module named "haive_games.tic_tac_toe.state"
  - ID: 45e0f722
- `packages/haive-dataflow/src/haive/dataflow/tic_tac_toe_api.py:13` - error: Cannot find implementation or library stub for module named "haive_games.tic_tac_toe.state_ma
  - ID: 49cc64b9
- `packages/haive-dataflow/src/haive/dataflow/connect4_api.py:13` - error: Cannot find implementation or library stub for module named "haive_games.connect4.agent" [im
  - ID: 41acd6a4
- `packages/haive-dataflow/src/haive/dataflow/connect4_api.py:14` - error: Cannot find implementation or library stub for module named "haive_games.connect4.config" [i
  - ID: 85213be0
- `packages/haive-dataflow/src/haive/dataflow/connect4_api.py:15` - error: Cannot find implementation or library stub for module named "haive_games.connect4.state" [im
  - ID: 8ca4b0bb
- `packages/haive-dataflow/src/haive/dataflow/api/tic_tac_toe_api.py:10` - error: Cannot find implementation or library stub for module named "haive_games.tic_tac_toe.agent"
  - ID: 1c63d93e
- ... and 7 more

### haive-games

- `packages/haive-games/src/haive/games/mafia/verify_imports.py:8` - error: Cannot find implementation or library stub for module named "models" [import-not-found]
  - ID: 4e838c83
- `packages/haive-games/src/haive/games/single_player/mine_sweeper/base.py:8` - error: Cannot find implementation or library stub for module named "game_framework_base" [import-no
  - ID: be93e4d7
- `packages/haive-games/src/haive/games/single_player/logic_grid/base.py:4` - error: Cannot find implementation or library stub for module named "game_framework_base" [import-no
  - ID: f1f6ed22
- `packages/haive-games/src/haive/games/single_player/flow_free/base.py:7` - error: Cannot find implementation or library stub for module named "game_framework_base" [import-no
  - ID: acc8c9ec
- `packages/haive-games/src/haive/games/single_player/crossword_puzzle/base.py:5` - error: Cannot find implementation or library stub for module named "game_framework_base" [import-no
  - ID: 5d7e5861
- `packages/haive-games/src/haive/games/framework/core/container.py:9` - error: Cannot find implementation or library stub for module named "game_framework.core.piece" [imp
  - ID: da977365
- `packages/haive-games/src/haive/games/core/game/core_space.py:13` - error: Cannot find implementation or library stub for module named "game.core.piece" [import-not-fo
  - ID: d90ddd00
- `packages/haive-games/src/haive/games/core/game/core_space.py:14` - error: Cannot find implementation or library stub for module named "game.core.position" [import-not
  - ID: 842a0eb2
- `packages/haive-games/src/haive/games/core/game/core_game.py:16` - error: Cannot find implementation or library stub for module named "game.core.board" [import-not-fo
  - ID: 41232473
- `packages/haive-games/src/haive/games/core/game/core_game.py:17` - error: Cannot find implementation or library stub for module named "game.core.container" [import-no
  - ID: 67c97b01
- ... and 15 more

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/installers/__init__.py:3` - error: Cannot find implementation or library stub for module named "installers.advanced_code_install
  - ID: 95c208d4
- `packages/haive-mcp/src/haive/mcp/installers/__init__.py:16` - error: Cannot find implementation or library stub for module named "installers.config_manager" [imp
  - ID: 046cb1c5
- `packages/haive-mcp/src/haive/mcp/installers/__init__.py:28` - error: Cannot find implementation or library stub for module named "installers.safe_pattern_installe
  - ID: ea0c9bac
- `packages/haive-mcp/src/haive/mcp/discovery/__init__.py:3` - error: Cannot find implementation or library stub for module named "discovery.analyzer" [import-not
  - ID: 68eb62d3
- `packages/haive-mcp/src/haive/mcp/discovery/__init__.py:11` - error: Cannot find implementation or library stub for module named "discovery.server_discovery" [im
  - ID: b180c769
- `packages/haive-mcp/src/haive/mcp/integrated_mcp_system.py:26` - error: Cannot find implementation or library stub for module named "csv_viewer" [import-not-found]
  - ID: 01165bfc
- `packages/haive-mcp/src/haive/mcp/integrated_mcp_system.py:27` - error: Cannot find implementation or library stub for module named "self_query_mcp_agent" [import-n
  - ID: ce4c77ca
- `packages/haive-mcp/src/haive/mcp/comprehensive_mcp_web.py:18` - error: Cannot find implementation or library stub for module named "csv_viewer" [import-not-found]
  - ID: 57b488fb
- `packages/haive-mcp/src/haive/mcp/comprehensive_mcp_web.py:19` - error: Cannot find implementation or library stub for module named "self_query_mcp_agent" [import-n
  - ID: f99de183
- `packages/haive-mcp/src/haive/mcp/haive_agent_mcp_integration.py:16` - error: Cannot find implementation or library stub for module named "fastmcp_runner" [import-not-fou
  - ID: d77950a3
- ... and 1 more

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/tools.py:30` - error: Cannot find implementation or library stub for module named "newsapi" [import-not-found]
  - ID: 9435dd4d

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/ionic_tool.py:19` - error: Cannot find implementation or library stub for module named "ionic_langchain.tool" [import-n
  - ID: 49c3efe5
- `packages/haive-tools/src/haive/tools/tools/hinge_tools.py:22` - error: Cannot find implementation or library stub for module named "squeaky_hinge" [import-not-foun
  - ID: 3c17b86f
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/project_creation/__init__.py:3` - error: Cannot find implementation or library stub for module named "project_creation.github" [impor
  - ID: df2d21e2
- `packages/haive-tools/src/haive/tools/tools/toolkits/mongodb_toolkit.py:26` - error: Cannot find implementation or library stub for module named "langchain_mongodb.agent_toolkit.
  - ID: 651623d6
- `packages/haive-tools/src/haive/tools/tools/toolkits/mongodb_toolkit.py:27` - error: Cannot find implementation or library stub for module named "langchain_mongodb.agent_toolkit.
  - ID: f00385d2

## mypy:import-untyped (6010 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/utils/__init__.py:3` - error: Skipping analyzing "haive.agents.utils.utils": module is installed, but missing library stubs
  - ID: 85e90fbb
- `packages/haive-agents/src/haive/agents/task_analysis/tree/models.py:6` - error: Skipping analyzing "haive.core.common.structures.tree": module is installed, but missing libr
  - ID: e913336d
- `packages/haive-agents/src/haive/agents/task_analysis/tree/models.py:8` - error: Skipping analyzing "haive.agents.task_analysis.base.models": module is installed, but missing
  - ID: 04a55f31
- `packages/haive-agents/src/haive/agents/task_analysis/tree/engines.py:3` - error: Skipping analyzing "haive.core.engine.aug_llm": module is installed, but missing library stub
  - ID: 55a6bc00
- `packages/haive-agents/src/haive/agents/task_analysis/tree/engines.py:4` - error: Skipping analyzing "haive.core.models.llm.base": module is installed, but missing library stu
  - ID: 7f5ef6bc
- `packages/haive-agents/src/haive/agents/task_analysis/tree/engines.py:6` - error: Skipping analyzing "haive.agents.task_analysis.tree.prompts": module is installed, but missin
  - ID: 429a79c3
- `packages/haive-agents/src/haive/agents/task_analysis/execution/engines.py:3` - error: Skipping analyzing "haive.core.engine.aug_llm": module is installed, but missing library stub
  - ID: fa15b06a
- `packages/haive-agents/src/haive/agents/task_analysis/execution/engines.py:4` - error: Skipping analyzing "haive.core.models.llm.base": module is installed, but missing library stu
  - ID: bd9b5eb2
- `packages/haive-agents/src/haive/agents/task_analysis/execution/engines.py:6` - error: Skipping analyzing "haive.agents.task_analysis.execution.models": module is installed, but mi
  - ID: 8876468d
- `packages/haive-agents/src/haive/agents/task_analysis/execution/engines.py:10` - error: Skipping analyzing "haive.agents.task_analysis.execution.prompts": module is installed, but m
  - ID: 253d63e4
- ... and 2969 more

### haive-core

- `packages/haive-core/src/haive/core/utils/visualize_graph_utils.py:3` - error: Skipping analyzing "haive.core.config.constants": module is installed, but missing library st
  - ID: cae60fe7
- `packages/haive-core/src/haive/core/utils/pydantic_utils/__init__.py:3` - error: Skipping analyzing "haive.core.utils.pydantic_utils.general": module is installed, but missin
  - ID: 3dd2f80f
- `packages/haive-core/src/haive/core/utils/haive_discovery/__init__.py:7` - error: Skipping analyzing "haive.core.utils.haive_discovery.base_analyzer": module is installed, but
  - ID: c304fb99
- `packages/haive-core/src/haive/core/utils/haive_discovery/__init__.py:8` - error: Skipping analyzing "haive.core.utils.haive_discovery.component_info": module is installed, bu
  - ID: 52fd517c
- `packages/haive-core/src/haive/core/utils/haive_discovery/__init__.py:9` - error: Skipping analyzing "haive.core.utils.haive_discovery.discovery_engine": module is installed,
  - ID: 07edc4d7
- `packages/haive-core/src/haive/core/utils/haive_discovery/__init__.py:10` - error: Skipping analyzing "haive.core.utils.haive_discovery.documentation_writer": module is install
  - ID: 8e84fcea
- `packages/haive-core/src/haive/core/utils/haive_discovery/__init__.py:11` - error: Skipping analyzing "haive.core.utils.haive_discovery.engine_analyzer": module is installed, b
  - ID: 7fa00cda
- `packages/haive-core/src/haive/core/utils/haive_discovery/__init__.py:12` - error: Skipping analyzing "haive.core.utils.haive_discovery.haive_discovery": module is installed, b
  - ID: 05501943
- `packages/haive-core/src/haive/core/utils/haive_discovery/__init__.py:13` - error: Skipping analyzing "haive.core.utils.haive_discovery.retriever_analyzers": module is installe
  - ID: f6ef743e
- `packages/haive-core/src/haive/core/utils/haive_discovery/__init__.py:17` - error: Skipping analyzing "haive.core.utils.haive_discovery.tool_analyzers": module is installed, bu
  - ID: e20b7daa
- ... and 1360 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/__init___lazy.py:47` - error: Skipping analyzing "haive.dataflow.registry.discovery": module is installed, but missing libr
  - ID: 8fcac9a5
- `packages/haive-dataflow/src/haive/dataflow/__init___lazy.py:55` - error: Skipping analyzing "haive.dataflow.registry.lazy_core": module is installed, but missing libr
  - ID: f34db366
- `packages/haive-dataflow/src/haive/dataflow/__init___lazy.py:56` - error: Skipping analyzing "haive.dataflow.registry.models": module is installed, but missing library
  - ID: fe3966d2
- `packages/haive-dataflow/src/haive/dataflow/__init___lazy.py:74` - error: Skipping analyzing "haive.dataflow.registry.serialization": module is installed, but missing
  - ID: e1c96fae
- `packages/haive-dataflow/src/haive/dataflow/utils/__init__.py:7` - error: Skipping analyzing "haive.dataflow.utils.logging": module is installed, but missing library s
  - ID: d3e3e38c
- `packages/haive-dataflow/src/haive/dataflow/registry/utils/__init__.py:7` - error: Skipping analyzing "haive.dataflow.registry.utils.logging": module is installed, but missing
  - ID: 1a703d93
- `packages/haive-dataflow/src/haive/dataflow/registry/importers/__init__.py:8` - error: Skipping analyzing "haive.dataflow.registry.importers.litellm_importer": module is installed,
  - ID: 7547d02f
- `packages/haive-dataflow/src/haive/dataflow/registry/__init__.py:33` - error: Skipping analyzing "haive.dataflow.registry.core": module is installed, but missing library s
  - ID: b90f0bf6
- `packages/haive-dataflow/src/haive/dataflow/registry/__init__.py:34` - error: Skipping analyzing "haive.dataflow.registry.discovery": module is installed, but missing libr
  - ID: fa5c527c
- `packages/haive-dataflow/src/haive/dataflow/registry/__init__.py:42` - error: Skipping analyzing "haive.dataflow.registry.models": module is installed, but missing library
  - ID: 2cce4a77
- ... and 213 more

### haive-games

- `packages/haive-games/src/haive/games/llm_config_factory.py:10` - error: Skipping analyzing "haive.core.models.llm.base": module is installed, but missing library stu
  - ID: 04952e63
- `packages/haive-games/src/haive/games/llm_config_factory.py:12` - error: Skipping analyzing "haive.games.models.llm": module is installed, but missing library stubs o
  - ID: ee8be527
- `packages/haive-games/src/haive/games/utils/__init__.py:3` - error: Skipping analyzing "haive.games.utils.recursion_config": module is installed, but missing lib
  - ID: ab16914b
- `packages/haive-games/src/haive/games/utils/__init__.py:6` - error: Skipping analyzing "haive.games.utils.test_helpers": module is installed, but missing library
  - ID: 5b346340
- `packages/haive-games/src/haive/games/tic_tac_toe/state_manager.py:8` - error: Skipping analyzing "haive.games.framework.base.state_manager": module is installed, but missi
  - ID: 60b2a89b
- `packages/haive-games/src/haive/games/tic_tac_toe/state_manager.py:9` - error: Skipping analyzing "haive.games.tic_tac_toe.models": module is installed, but missing library
  - ID: 5632a017
- `packages/haive-games/src/haive/games/tic_tac_toe/state_manager.py:10` - error: Skipping analyzing "haive.games.tic_tac_toe.state": module is installed, but missing library
  - ID: af6c92db
- `packages/haive-games/src/haive/games/single_player/agent.py:10` - error: Skipping analyzing "haive.games.base.agent": module is installed, but missing library stubs o
  - ID: 9a5fdc93
- `packages/haive-games/src/haive/games/single_player/agent.py:11` - error: Skipping analyzing "haive.games.framework.base.config": module is installed, but missing libr
  - ID: aae9999d
- `packages/haive-games/src/haive/games/single_player/sudoku/game/board.py:5` - error: Skipping analyzing "haive.games.core.board.base": module is installed, but missing library st
  - ID: 2cedc0b9
- ... and 1034 more

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/utils/__init__.py:3` - error: Skipping analyzing "haive.mcp.utils.extract_mcp_github_repos": module is installed, but missi
  - ID: 8300580e
- `packages/haive-mcp/src/haive/mcp/tools/__init__.py:3` - error: Skipping analyzing "haive.mcp.tools.ai_assistant": module is installed, but missing library s
  - ID: a66ff332
- `packages/haive-mcp/src/haive/mcp/tools/__init__.py:13` - error: Skipping analyzing "haive.mcp.tools.server_selector": module is installed, but missing librar
  - ID: a743db55
- `packages/haive-mcp/src/haive/mcp/tools/__init__.py:30` - error: Skipping analyzing "haive.mcp.tools.server_tester": module is installed, but missing library
  - ID: e4aa902d
- `packages/haive-mcp/src/haive/mcp/servers/__init__.py:3` - error: Skipping analyzing "haive.mcp.servers.dataflow_mcp_server": module is installed, but missing
  - ID: 4f9eb1e2
- `packages/haive-mcp/src/haive/mcp/servers/__init__.py:4` - error: Skipping analyzing "haive.mcp.servers.http_server": module is installed, but missing library
  - ID: a54b3f01
- `packages/haive-mcp/src/haive/mcp/servers/__init__.py:5` - error: Skipping analyzing "haive.mcp.servers.simple_http_server": module is installed, but missing l
  - ID: 01c8ff81
- `packages/haive-mcp/src/haive/mcp/mixins/__init__.py:3` - error: Skipping analyzing "haive.mcp.mixins.mcp_mixin": module is installed, but missing library stu
  - ID: 346e4810
- `packages/haive-mcp/src/haive/mcp/downloader/__init__.py:3` - error: Skipping analyzing "haive.mcp.downloader.config": module is installed, but missing library st
  - ID: 03ace28f
- `packages/haive-mcp/src/haive/mcp/downloader/__init__.py:12` - error: Skipping analyzing "haive.mcp.downloader.core": module is installed, but missing library stub
  - ID: e16098bd
- ... and 117 more

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/weather_disaster_management/engines.py:1` - error: Skipping analyzing "haive.agents.react_agent2.config2": module is installed, but missing libr
  - ID: f4ee2421
- `packages/haive-prebuilt/src/haive/prebuilt/weather_disaster_management/engines.py:2` - error: Skipping analyzing "haive.core.engine.aug_llm": module is installed, but missing library stub
  - ID: 284cd688
- `packages/haive-prebuilt/src/haive/prebuilt/weather_disaster_management/engines.py:4` - error: Skipping analyzing "haive.haive.tools.search_tools": module is installed, but missing library
  - ID: e4a70e08
- `packages/haive-prebuilt/src/haive/prebuilt/weather_disaster_management/engines.py:5` - error: Skipping analyzing "haive.prebuilt.weather_disaster_management.models": module is installed,
  - ID: 04ab49b9
- `packages/haive-prebuilt/src/haive/prebuilt/weather_disaster_management/engines.py:9` - error: Skipping analyzing "haive.prebuilt.weather_disaster_management.prompts": module is installed,
  - ID: c9b24b3d
- `packages/haive-prebuilt/src/haive/prebuilt/weather_disaster_management/branches.py:1` - error: Skipping analyzing "haive.core.graph.branches": module is installed, but missing library stub
  - ID: bc00c93b
- `packages/haive-prebuilt/src/haive/prebuilt/project_manager/aug_llms.py:2` - error: Skipping analyzing "haive.prebuilt.project_manager.models": module is installed, but missing
  - ID: a127522b
- `packages/haive-prebuilt/src/haive/prebuilt/misc/__init__.py:19` - error: Skipping analyzing "haive.prebuilt.misc.agent_utilities_models": module is installed, but mis
  - ID: 5890dafd
- `packages/haive-prebuilt/src/haive/prebuilt/misc/__init__.py:50` - error: Skipping analyzing "haive.prebuilt.misc.agent_utilities_prompts": module is installed, but mi
  - ID: 10cd78ac
- `packages/haive-prebuilt/src/haive/prebuilt/ai_insight/example.py:6` - error: Skipping analyzing "haive.prebuilt.ai_insight.agent": module is installed, but missing librar
  - ID: 026222ef
- ... and 174 more

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/gradio_toolkit.py:21` - error: Skipping analyzing "gradio_tools.tools": module is installed, but missing library stubs or py
  - ID: fe21e824
- `packages/haive-tools/src/haive/tools/tools/toolkits/gmail_toolkit.py:27` - error: Skipping analyzing "langchain_google_community.gmail.toolkit": module is installed, but missi
  - ID: 733cccda
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/remote_execution.py:14` - error: Library stubs not installed for "paramiko" [import-untyped]
  - ID: d7629fe6
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/__init__.py:3` - error: Skipping analyzing "haive.tools.toolkits.dev.tools": module is installed, but missing library
  - ID: bd3ad1fc
- `packages/haive-tools/src/haive/tools/tools/toolkits/__init__.py:3` - error: Skipping analyzing "haive.tools.tools.toolkits.alpha_vantage": module is installed, but missi
  - ID: 1041cc78
- `packages/haive-tools/src/haive/tools/tools/toolkits/__init__.py:7` - error: Skipping analyzing "haive.tools.tools.toolkits.amadues_toolkit": module is installed, but mis
  - ID: 39127029
- `packages/haive-tools/src/haive/tools/tools/toolkits/__init__.py:15` - error: Skipping analyzing "haive.tools.tools.toolkits.base": module is installed, but missing librar
  - ID: 7d7b7e5f
- `packages/haive-tools/src/haive/tools/tools/toolkits/__init__.py:21` - error: Skipping analyzing "haive.tools.tools.toolkits.chuck_norris_jokes_toolkit": module is install
  - ID: ba458f5f
- `packages/haive-tools/src/haive/tools/tools/toolkits/__init__.py:28` - error: Skipping analyzing "haive.tools.tools.toolkits.citydsk_toolkit": module is installed, but mis
  - ID: 23244dcd
- `packages/haive-tools/src/haive/tools/tools/toolkits/__init__.py:36` - error: Skipping analyzing "haive.tools.tools.toolkits.clickup_toolkit": module is installed, but mis
  - ID: 3ce0e471
- ... and 73 more

## mypy:index (107 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/planning/base/models.py:908` - error: Unsupported target for indexed assignment ("object") [index]
  - ID: dae54ac6
- `packages/haive-agents/src/haive/agents/planning/base/models.py:914` - error: Unsupported target for indexed assignment ("object") [index]
  - ID: 16436aad
- `packages/haive-agents/src/haive/agents/planning/base/models.py:919` - error: Unsupported target for indexed assignment ("object") [index]
  - ID: f96f5412
- `packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_v3.py:885` - error: Unsupported target for indexed assignment ("object") [index]
  - ID: 925c34ad
- `packages/haive-agents/src/haive/agents/multi/enhanced/multi_agent_v3.py:932` - error: Unsupported target for indexed assignment ("object") [index]
  - ID: 32852708
- `packages/haive-agents/src/haive/agents/memory_reorganized/retrieval/enhanced_retriever.py:471` - error: Value of type "object" is not indexable [index]
  - ID: a7a89346
- `packages/haive-agents/src/haive/agents/memory_reorganized/retrieval/enhanced_retriever.py:471` - error: Value of type "object" is not indexable [index]
  - ID: a7a89346
- `packages/haive-agents/src/haive/agents/memory_reorganized/core/stores.py:505` - error: Unsupported target for indexed assignment ("object") [index]
  - ID: 18acdea5
- `packages/haive-agents/src/haive/agents/memory_reorganized/core/stores.py:510` - error: Unsupported target for indexed assignment ("object") [index]
  - ID: e1811c1f
- `packages/haive-agents/src/haive/agents/memory_reorganized/agents/multi.py:566` - error: Unsupported target for indexed assignment ("object") [index]
  - ID: 5601c181
- ... and 63 more

### haive-core

- `packages/haive-core/src/haive/core/utils/haive_discovery/utils.py:417` - error: Value of type "object" is not indexable [index]
  - ID: 7f29800c
- `packages/haive-core/src/haive/core/utils/haive_discovery/utils.py:417` - error: Value of type "object" is not indexable [index]
  - ID: 7f29800c
- `packages/haive-core/src/haive/core/utils/haive_discovery/utils.py:419` - error: Value of type "object" is not indexable [index]
  - ID: 6441363a
- `packages/haive-core/src/haive/core/utils/haive_discovery/utils.py:419` - error: Value of type "object" is not indexable [index]
  - ID: 6441363a
- `packages/haive-core/src/haive/core/utils/debugkit/benchmarking/load.py:153` - error: Value of type any? is not indexable [index]
  - ID: f7412f6a
- `packages/haive-core/src/haive/core/utils/debugkit/benchmarking/load.py:154` - error: Value of type any? is not indexable [index]
  - ID: ecb43fb0
- `packages/haive-core/src/haive/core/utils/debugkit/benchmarking/load.py:155` - error: Value of type any? is not indexable [index]
  - ID: bb0957f5
- `packages/haive-core/src/haive/core/utils/debugkit/benchmarking/load.py:198` - error: Value of type any? is not indexable [index]
  - ID: 250a9d11
- `packages/haive-core/src/haive/core/utils/debugkit/benchmarking/load.py:199` - error: Value of type any? is not indexable [index]
  - ID: 283ee815
- `packages/haive-core/src/haive/core/engine/document/loaders/sources/source_base.py:167` - error: Unsupported target for indexed assignment ("object") [index]
  - ID: d2033878
- ... and 1 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:532` - error: Unsupported target for indexed assignment ("object") [index]
  - ID: d56676fb
- `packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:533` - error: Value of type "object" is not indexable [index]
  - ID: d6425ea9
- `packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:533` - error: Value of type "object" is not indexable [index]
  - ID: d6425ea9
- `packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:541` - error: Unsupported target for indexed assignment ("object") [index]
  - ID: 909c55a3
- `packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:542` - error: Value of type "object" is not indexable [index]
  - ID: 94bcf897
- `packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:542` - error: Value of type "object" is not indexable [index]
  - ID: 94bcf897
- `packages/haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes_fixed.py:525` - error: Unsupported target for indexed assignment ("object") [index]
  - ID: 353994c9
- `packages/haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes_fixed.py:526` - error: Value of type "object" is not indexable [index]
  - ID: afde3460
- `packages/haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes_fixed.py:526` - error: Value of type "object" is not indexable [index]
  - ID: afde3460
- `packages/haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes_fixed.py:534` - error: Unsupported target for indexed assignment ("object") [index]
  - ID: d7be9b79
- ... and 2 more

### haive-games

- `packages/haive-games/src/haive/games/monopoly/standalone_demo.py:256` - error: Value of type "object" is not indexable [index]
  - ID: ddf089a8
- `packages/haive-games/src/haive/games/monopoly/standalone_demo.py:260` - error: Value of type "object" is not indexable [index]
  - ID: 2db2ab49
- `packages/haive-games/src/haive/games/monopoly/standalone_demo.py:261` - error: Value of type "object" is not indexable [index]
  - ID: 0ea34534
- `packages/haive-games/src/haive/games/monopoly/standalone_demo.py:264` - error: Value of type "object" is not indexable [index]
  - ID: f5febeb7
- `packages/haive-games/src/haive/games/monopoly/standalone_demo.py:272` - error: Value of type "object" is not indexable [index]
  - ID: 13d8abb8
- `packages/haive-games/src/haive/games/monopoly/standalone_demo.py:273` - error: Value of type "object" is not indexable [index]
  - ID: 817cb4b3
- `packages/haive-games/src/haive/games/monopoly/standalone_demo.py:276` - error: Value of type "object" is not indexable [index]
  - ID: f534355c
- `packages/haive-games/src/haive/games/single_player/crossword_puzzle/base.py:107` - error: Value of type any? is not indexable [index]
  - ID: 2031bf80
- `packages/haive-games/src/haive/games/single_player/crossword_puzzle/base.py:121` - error: Value of type any? is not indexable [index]
  - ID: fdef1276

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/downloader/github_mass_downloader.py:311` - error: Unsupported target for indexed assignment ("object") [index]
  - ID: 99fc04d9
- `packages/haive-mcp/src/haive/mcp/servers/dataflow_mcp_server.py:345` - error: Unsupported target for indexed assignment ("object") [index]
  - ID: 8fd40273

## mypy:int (4 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/planning/llm_compiler/output_parser.py:68` - error: Incompatible return value type (got "list[int]", expected "dict[str, list[str]]") [return-va
  - ID: 2fc042c6
- `packages/haive-agents/src/haive/agents/planning/llm_compiler/output_parser.py:69` - error: Incompatible return value type (got "list[int]", expected "dict[str, list[str]]") [return-va
  - ID: 877f40df

### haive-core

- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:370` - note: def copy(self, \*, include: AbstractSet[int] | AbstractSet[str] | Mapping[int, Any] |
  - ID: bdadceae

### haive-games

- `packages/haive-games/src/haive/games/nim/standalone_game.py:306` - error: Incompatible default for argument "pile_sizes" (default has type "None", argument has type "l
  - ID: 2da0c4ad

## mypy:int, Any (2 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/multi/enhanced_parallel_agent.py:293` - error: Incompatible types in assignment (expression has type "tuple[int, Any]", variable has type "t
  - ID: 85995016
- `packages/haive-agents/src/haive/agents/multi/archive/enhanced_parallel_agent.py:293` - error: Incompatible types in assignment (expression has type "tuple[int, Any]", variable has type "t
  - ID: 44905532

## mypy:int, None (3 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/agent2.py:202` - error: Argument 1 to "append" of "list" has incompatible type "tuple[int, None]"; expected "tuple[in
  - ID: fa9dff93
- `packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/agent2.py:479` - error: Argument 1 to "append" of "list" has incompatible type "tuple[int, None]"; expected "tuple[in
  - ID: d50f8a98
- `packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/agent2.py:508` - error: Argument 1 to "append" of "list" has incompatible type "tuple[int, None]"; expected "tuple[in
  - ID: 02de204e

## mypy:int, dict[str, int (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/chain/chain_agent_simple.py:166` - error: Argument 1 to "append" of "list" has incompatible type "tuple[int, dict[str, int], Callable[.
  - ID: 8dfc3ce8

## mypy:langchain_community.graphs.graph_document.GraphDocument (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_base/models.py:200` - error: Incompatible return value type (got "list[langchain_community.graphs.graph_document.GraphDocu
  - ID: 42dddef1

## mypy:langchain_community.vectorstores.mongodb_atlas.MongoDBAtlasVectorSearch (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/vectorstore/providers/MongoDBAtlasVectorStoreConfig.py:173` - error: Incompatible import of "MongoDBAtlasVectorSearch" (imported name has type "type[langchain_com
  - ID: 6786caa5

## mypy:langchain_community.vectorstores.neo4j_vector.Neo4jVector (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/vectorstore/providers/Neo4jVectorStoreConfig.py:185` - error: Incompatible import of "Neo4jVector" (imported name has type "type[langchain_community.vector
  - ID: 806758e7

## mypy:langchain_neo4j.graphs.graph_document.GraphDocument (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/utils.py:9` - error: Incompatible import of "GraphDocument" (imported name has type "type[langchain_neo4j.graphs.g
  - ID: 96d9fd85

## mypy:list-item (15 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_reorganized/search/labs/agent.py:284` - error: List item 0 has incompatible type "BaseTool"; expected "Tool" [list-item]
  - ID: e16c02dc
- `packages/haive-agents/src/haive/agents/memory_reorganized/search/labs/agent.py:285` - error: List item 1 has incompatible type "BaseTool"; expected "Tool" [list-item]
  - ID: e0e67290
- `packages/haive-agents/src/haive/agents/memory_reorganized/search/labs/agent.py:286` - error: List item 2 has incompatible type "BaseTool"; expected "Tool" [list-item]
  - ID: b2bcb086
- `packages/haive-agents/src/haive/agents/memory_reorganized/search/labs/agent.py:287` - error: List item 3 has incompatible type "BaseTool"; expected "Tool" [list-item]
  - ID: 969df45d
- `packages/haive-agents/src/haive/agents/memory/search/labs/agent.py:282` - error: List item 0 has incompatible type "BaseTool"; expected "Tool" [list-item]
  - ID: 44b59954
- `packages/haive-agents/src/haive/agents/memory/search/labs/agent.py:283` - error: List item 1 has incompatible type "BaseTool"; expected "Tool" [list-item]
  - ID: ea3ea1fe
- `packages/haive-agents/src/haive/agents/memory/search/labs/agent.py:284` - error: List item 2 has incompatible type "BaseTool"; expected "Tool" [list-item]
  - ID: 7ac4f8e3
- `packages/haive-agents/src/haive/agents/memory/search/labs/agent.py:285` - error: List item 3 has incompatible type "BaseTool"; expected "Tool" [list-item]
  - ID: 37329a86
- `packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/agent.py:745` - error: List item 0 has incompatible type "None"; expected "Tool" [list-item]
  - ID: ce9ba12b

### haive-core

- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:105` - error: List item 0 has incompatible type "BaseMessage"; expected "AIMessage | HumanMessage | ChatMes
  - ID: 57859731

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:380` - error: List item 0 has incompatible type "float"; expected "bool" [list-item]
  - ID: 17c0501c
- `packages/haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:380` - error: List item 0 has incompatible type "float"; expected "bool" [list-item]
  - ID: 17c0501c
- `packages/haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:380` - error: List item 0 has incompatible type "float"; expected "bool" [list-item]
  - ID: 17c0501c
- `packages/haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:380` - error: List item 0 has incompatible type "float"; expected "bool" [list-item]
  - ID: 17c0501c
- `packages/haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:380` - error: List item 0 has incompatible type "float"; expected "bool" [list-item]
  - ID: 17c0501c

## mypy:list[\_T (2 errors)

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/models.py:41` - error: No overload variant of "Field" matches argument types "str", "type[list[_T]]", "int" [call-o
  - ID: b43aed8e
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/models.py:226` - error: No overload variant of "Field" matches argument types "str", "type[list[_T]]", "int" [call-o
  - ID: 3b883ee3

## mypy:list[float (4 errors)

### haive-core

- `packages/haive-core/src/haive/core/persistence/store/embeddings.py:77` - error: Returning Any from function declared to return "list[list[float]]" [no-any-return]
  - ID: 78b09eea
- `packages/haive-core/src/haive/core/persistence/store/embeddings.py:93` - error: Returning Any from function declared to return "list[list[float]]" [no-any-return]
  - ID: b9b767c1
- `packages/haive-core/src/haive/core/persistence/store/embeddings.py:148` - error: Returning Any from function declared to return "list[list[float]]" [no-any-return]
  - ID: de15b28a
- `packages/haive-core/src/haive/core/persistence/store/embeddings.py:157` - error: Returning Any from function declared to return "list[list[float]]" [no-any-return]
  - ID: cb936dd9

## mypy:list[int (1 errors)

### haive-games

- `packages/haive-games/src/haive/games/checkers/state.py:713` - error: Argument "board" to "CheckersState" has incompatible type "list[list[int]]"; expected "list[l
  - ID: 01d4ca3b

## mypy:list[str (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/prompt_template/prompt_engine.py:314` - error: Incompatible types in assignment (expression has type "type[list[str]]", variable has type "t
  - ID: 79121d1a

## mypy:literal-required (2 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/aug_llm/utils.py:299` - error: TypedDict key must be a string literal; expected one of ("tags", "metadata", "callbacks", "ru
  - ID: 55754a65
- `packages/haive-core/src/haive/core/config/runnable.py:242` - error: TypedDict key must be a string literal; expected one of ("tags", "metadata", "callbacks", "ru
  - ID: 059bb504

## mypy:method-assign (5 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/planning/base/models.py:323` - error: Cannot assign to a method [method-assign]
  - ID: 47478ecf

### haive-core

- `packages/haive-core/src/haive/core/registry/decorators.py:77` - error: Cannot assign to a method [method-assign]
  - ID: d0f99e74

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/api/general_games_api.py:493` - error: Cannot assign to a method [method-assign]
  - ID: e3a38266
- `packages/haive-dataflow/src/haive/dataflow/api/middleware/supabase_logging.py:266` - error: Cannot assign to a method [method-assign]
  - ID: 877901f7

### haive-games

- `packages/haive-games/src/haive/games/api/general_api.py:428` - error: Cannot assign to a method [method-assign]
  - ID: 558f53f0

## mypy:misc (263 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_reorganized/models/procedural/models.py:27` - error: Untyped decorator makes function "validate_instruction_clarity" untyped [misc]
  - ID: 2b978cc5
- `packages/haive-agents/src/haive/agents/memory_reorganized/models/procedural/models.py:63` - error: Untyped decorator makes function "validate_reflection_logic" untyped [misc]
  - ID: 1e502857
- `packages/haive-agents/src/haive/agents/memory_reorganized/models/procedural/models.py:103` - error: Untyped decorator makes function "validate_instruction_set" untyped [misc]
  - ID: 86deff60
- `packages/haive-agents/src/haive/agents/memory_reorganized/models/procedural/models.py:129` - error: Untyped decorator makes function "validate_procedural_integrity" untyped [misc]
  - ID: 55c18876
- `packages/haive-agents/src/haive/agents/simple/lazy_simple_agent.v2.py:127` - error: "None" not callable [misc]
  - ID: a0328843
- `packages/haive-agents/src/haive/agents/simple/lazy_simple_agent.py:112` - error: "None" not callable [misc]
  - ID: da308aec
- `packages/haive-agents/src/haive/agents/models.py:8` - error: Right hand side values are not supported in TypedDict [misc]
  - ID: 10cde474
- `packages/haive-agents/src/haive/agents/models.py:9` - error: Right hand side values are not supported in TypedDict [misc]
  - ID: 8cd66f34
- `packages/haive-agents/src/haive/agents/models.py:10` - error: Right hand side values are not supported in TypedDict [misc]
  - ID: ab48fab8
- `packages/haive-agents/src/haive/agents/models.py:11` - error: Right hand side values are not supported in TypedDict [misc]
  - ID: d5380c45
- ... and 99 more

### haive-core

- `packages/haive-core/src/haive/core/graph/node/composer/update_functions.py:325` - error: callable? not callable [misc]
  - ID: d3ee562d
- `packages/haive-core/src/haive/core/engine/document/loaders/sources/database/types.py:4` - error: No non-enum mixin classes are allowed after "enum.Enum" [misc]
  - ID: 56c16271
- `packages/haive-core/src/haive/core/engine/base/protocols.py:17` - error: Invariant type variable "I" used in protocol where contravariant one is expected [misc]
  - ID: e50b677a
- `packages/haive-core/src/haive/core/engine/base/protocols.py:17` - error: Invariant type variable "I" used in protocol where contravariant one is expected [misc]
  - ID: e50b677a
- `packages/haive-core/src/haive/core/engine/base/protocols.py:58` - error: Invariant type variable "I" used in protocol where contravariant one is expected [misc]
  - ID: 4eda1039
- `packages/haive-core/src/haive/core/engine/base/protocols.py:58` - error: Invariant type variable "I" used in protocol where contravariant one is expected [misc]
  - ID: 4eda1039
- `packages/haive-core/src/haive/core/registry/decorators.py:80` - error: "classmethod" used with a non-method [misc]
  - ID: 8f48aedb
- `packages/haive-core/src/haive/core/graph/patterns/integration.py:161` - error: "classmethod" used with a non-method [misc]
  - ID: 87306b9a
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/types.py:48` - error: All conditional function variants must have identical signatures [misc]
  - ID: d0bd6995
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/static.py:1010` - error: Generator has incompatible item type "int"; expected "bool" [misc]
  - ID: f8476b7b
- ... and 88 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/registry/core.py:741` - error: All conditional function variants must have identical signatures [misc]
  - ID: e8593a3c
- `packages/haive-dataflow/src/haive/dataflow/tic_tac_toe_api.py:65` - error: Untyped decorator makes function "create_game" untyped [misc]
  - ID: 39644a0d
- `packages/haive-dataflow/src/haive/dataflow/tic_tac_toe_api.py:101` - error: Untyped decorator makes function "make_move" untyped [misc]
  - ID: 756e6d8e
- `packages/haive-dataflow/src/haive/dataflow/tic_tac_toe_api.py:128` - error: Untyped decorator makes function "ai_move" untyped [misc]
  - ID: caa6c62c
- `packages/haive-dataflow/src/haive/dataflow/tic_tac_toe_api.py:146` - error: Untyped decorator makes function "get_game" untyped [misc]
  - ID: a3e0ff9f
- `packages/haive-dataflow/src/haive/dataflow/connect4_api.py:91` - error: Untyped decorator makes function "create_game" untyped [misc]
  - ID: f7c70de9
- `packages/haive-dataflow/src/haive/dataflow/connect4_api.py:137` - error: Untyped decorator makes function "make_move" untyped [misc]
  - ID: 70903e9b
- `packages/haive-dataflow/src/haive/dataflow/connect4_api.py:166` - error: Untyped decorator makes function "make_ai_move" untyped [misc]
  - ID: dbd76e92
- `packages/haive-dataflow/src/haive/dataflow/connect4_api.py:190` - error: Untyped decorator makes function "get_game" untyped [misc]
  - ID: 697aa242
- `packages/haive-dataflow/src/haive/dataflow/connect4_api.py:228` - error: Untyped decorator makes function "connect4_websocket" untyped [misc]
  - ID: 86830ddb
- ... and 10 more

### haive-games

- `packages/haive-games/src/haive/games/tic_tac_toe/configurable_config.py:312` - error: Value expression in dictionary comprehension has incompatible type "object"; expected type "s
  - ID: 1d6b6290
- `packages/haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:188` - error: Untyped decorator makes function "is_complete" untyped [misc]
  - ID: fc7b3bac
- `packages/haive-games/src/haive/games/risk/configurable_config.py:319` - error: Value expression in dictionary comprehension has incompatible type "object"; expected type "s
  - ID: 46fdd015
- `packages/haive-games/src/haive/games/reversi/configurable_config.py:317` - error: Value expression in dictionary comprehension has incompatible type "object"; expected type "s
  - ID: 057b0d4c
- `packages/haive-games/src/haive/games/poker/configurable_config.py:319` - error: Value expression in dictionary comprehension has incompatible type "object"; expected type "s
  - ID: cc5dde91
- `packages/haive-games/src/haive/games/nim/configurable_config.py:319` - error: Value expression in dictionary comprehension has incompatible type "object"; expected type "s
  - ID: c7f22b9c
- `packages/haive-games/src/haive/games/monopoly/configurable_config.py:340` - error: Value expression in dictionary comprehension has incompatible type "object"; expected type "s
  - ID: 47ee051d
- `packages/haive-games/src/haive/games/mastermind/configurable_config.py:324` - error: Value expression in dictionary comprehension has incompatible type "object"; expected type "s
  - ID: cc9f0673
- `packages/haive-games/src/haive/games/mancala/configurable_config.py:319` - error: Value expression in dictionary comprehension has incompatible type "object"; expected type "s
  - ID: 015dc248
- `packages/haive-games/src/haive/games/mafia/configurable_config.py:315` - error: Value expression in dictionary comprehension has incompatible type "object"; expected type "s
  - ID: e2e5218b
- ... and 15 more

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/agents/mcp_agent.py:314` - error: Exception must be derived from BaseException [misc]
  - ID: f0d8e897
- `packages/haive-mcp/src/haive/mcp/servers/dataflow_server.py:333` - error: Untyped decorator makes function "get_server_info" untyped [misc]
  - ID: 7c6eb815
- `packages/haive-mcp/src/haive/mcp/utils/extract_mcp_github_repos.py:732` - error: callable? not callable [misc]
  - ID: dbca715f
- `packages/haive-mcp/src/haive/mcp/mixins/mcp_mixin.py:68` - error: Cannot assign to a type [misc]
  - ID: 2f8dfd84

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/essay_grading/state.py:18` - error: Cannot determine consistent method resolution order (MRO) for "EssayGradingState" [misc]
  - ID: 9953d447
- `packages/haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/tools.py:30` - error: "None" not callable [misc]
  - ID: 5268d167
- `packages/haive-prebuilt/src/haive/prebuilt/taskifier/agent.py:12` - error: Invalid base class "Agent" [misc]
  - ID: b1d29f24
- `packages/haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/utils.py:11` - error: All conditional function variants must have identical signatures [misc]
  - ID: b7b9feb7
- `packages/haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/agent.py:18` - error: Invalid base class "Agent" [misc]
  - ID: 7f71c29a
- `packages/haive-prebuilt/src/haive/prebuilt/podcast_generator/agent.py:20` - error: Invalid base class "Agent" [misc]
  - ID: a67bbd9d
- `packages/haive-prebuilt/src/haive/prebuilt/podcast_generator/interview/agent.py:16` - error: Invalid base class "Agent" [misc]
  - ID: 61804a00

## mypy:name-defined (711 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/research/storm/wiki_writer/prompt.py:1` - error: Name "ChatPromptTemplate" is not defined [name-defined]
  - ID: 096d121d
- `packages/haive-agents/src/haive/agents/research/storm/section_writer/prompt.py:1` - error: Name "ChatPromptTemplate" is not defined [name-defined]
  - ID: 22e217a9
- `packages/haive-agents/src/haive/agents/research/storm/section_writer/agent.py:4` - error: Name "BaseGraph" is not defined [name-defined]
  - ID: 95adfdfa
- `packages/haive-agents/src/haive/agents/research/storm/section_writer/agent.py:8` - error: Name "retriever" is not defined [name-defined]
  - ID: 5d6c2260
- `packages/haive-agents/src/haive/agents/research/storm/section_writer/agent.py:21` - error: Name "long_context_llm" is not defined [name-defined]
  - ID: efca8d12
- `packages/haive-agents/src/haive/agents/research/storm/related_topics_generator/prompt.py:1` - error: Name "gen_related_topics_prompt" is not defined [name-defined]
  - ID: 587289d1
- `packages/haive-agents/src/haive/agents/research/storm/related_topics_generator/prompt.py:1` - error: Name "gen_related_topics_prompt" is not defined [name-defined]
  - ID: 587289d1
- `packages/haive-agents/src/haive/agents/research/storm/related_topics_generator/prompt.py:2` - error: Name "RelatedSubjects" is not defined [name-defined]
  - ID: 07939c93
- `packages/haive-agents/src/haive/agents/research/storm/outline_refiner/agent.py:4` - error: Name "refine_outline_prompt" is not defined [name-defined]
  - ID: 2802d805
- `packages/haive-agents/src/haive/agents/research/storm/outline_refiner/agent.py:4` - error: Name "refine_outline_prompt" is not defined [name-defined]
  - ID: 2802d805
- ... and 408 more

### haive-core

- `packages/haive-core/src/haive/core/graph/state_graph/pattern_registry.py:6` - error: Name "PatternDefinition" is not defined [name-defined]
  - ID: 40ea8720
- `packages/haive-core/src/haive/core/graph/state_graph/pattern_registry.py:20` - error: Name "PatternDefinition" is not defined [name-defined]
  - ID: 3ba7eafc
- `packages/haive-core/src/haive/core/graph/state_graph/pattern_registry.py:21` - error: Name "PatternDefinition" is not defined [name-defined]
  - ID: 76b375ed
- `packages/haive-core/src/haive/core/graph/state_graph/pattern_registry.py:24` - error: Name "PatternDefinition" is not defined [name-defined]
  - ID: e162d94c
- `packages/haive-core/src/haive/core/graph/state_graph/pattern_registry.py:36` - error: Name "PatternDefinition" is not defined [name-defined]
  - ID: 3fb18f2b
- `packages/haive-core/src/haive/core/graph/state_graph/pattern_registry.py:40` - error: Name "PatternDefinition" is not defined [name-defined]
  - ID: cc6f576b
- `packages/haive-core/src/haive/core/graph/state_graph/pattern_registry.py:48` - error: Name "PatternDefinition" is not defined [name-defined]
  - ID: 0ed09c1b
- `packages/haive-core/src/haive/core/graph/state_graph/pattern_registry.py:58` - error: Name "builtins" is not defined [name-defined]
  - ID: b23abddd
- `packages/haive-core/src/haive/core/graph/state_graph/pattern_registry.py:62` - error: Name "PatternDefinition" is not defined [name-defined]
  - ID: d9bb07b2
- `packages/haive-core/src/haive/core/graph/state_graph/pattern_definition.py:1` - error: Name "SerializableModel" is not defined [name-defined]
  - ID: 0978f1b8
- ... and 144 more

### haive-games

- `packages/haive-games/src/haive/games/single_player/example.py:1` - error: Name "SinglePlayerGameAgent" is not defined [name-defined]
  - ID: 99801251
- `packages/haive-games/src/haive/games/single_player/example.py:89` - error: Name "SinglePlayerGameAgent" is not defined [name-defined]
  - ID: 3925e988
- `packages/haive-games/src/haive/games/framework/base/utils.py:23` - error: Name "GameAgent" is not defined [name-defined]
  - ID: dbac3a8c
- `packages/haive-games/src/haive/games/core/piece/tile.py:1` - error: Name "GamePiece" is not defined [name-defined]
  - ID: 46b0961c
- `packages/haive-games/src/haive/games/core/piece/tile.py:1` - error: Name "GamePiece" is not defined [name-defined]
  - ID: 46b0961c
- `packages/haive-games/src/haive/games/core/piece/tile.py:11` - error: Name "P" is not defined [name-defined]
  - ID: d9972700
- `packages/haive-games/src/haive/games/core/piece/tile.py:11` - error: Name "P" is not defined [name-defined]
  - ID: d9972700
- `packages/haive-games/src/haive/games/base/utils.py:23` - error: Name "GameAgent" is not defined [name-defined]
  - ID: ccec24e4
- `packages/haive-games/src/haive/games/single_player/state_manager.py:28` - error: Name "GameDifficulty" is not defined [name-defined]
  - ID: d4b28178
- `packages/haive-games/src/haive/games/single_player/state_manager.py:29` - error: Name "PlayerType" is not defined [name-defined]
  - ID: 4cbfe705
- ... and 123 more

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/downloader/integration.py:112` - error: Name "StdioServerParameters" is not defined [name-defined]
  - ID: 89d6e7ce
- `packages/haive-mcp/src/haive/mcp/downloader/integration.py:118` - error: Name "stdio_client" is not defined [name-defined]
  - ID: 0c74cdfd
- `packages/haive-mcp/src/haive/mcp/downloader/integration.py:124` - error: Name "SSEConnection" is not defined [name-defined]
  - ID: d5e44764
- `packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:546` - error: Name "discover_mcp_servers" is not defined [name-defined]
  - ID: 07eb27eb
- `packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:560` - error: Name "install_mcp_server" is not defined [name-defined]
  - ID: 545c2770

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/logger.py:49` - error: Name "SecureShellExecutor" is not defined [name-defined]
  - ID: f29f0ac8

## mypy:no-any-return (758 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/task_analysis/tree/models.py:160` - error: Returning Any from function declared to return "float" [no-any-return]
  - ID: 84ff055e
- `packages/haive-agents/src/haive/agents/task_analysis/tree/models.py:162` - error: Returning Any from function declared to return "float" [no-any-return]
  - ID: be54a4c3
- `packages/haive-agents/src/haive/agents/reflection/simple_agent.py:73` - error: Returning Any from function declared to return "ReflectionAgent" [no-any-return]
  - ID: 2e426c1d
- `packages/haive-agents/src/haive/agents/memory_reorganized/models/procedural/models.py:73` - error: Returning Any from function declared to return "ReflectionCycle" [no-any-return]
  - ID: 701b1263
- `packages/haive-agents/src/haive/agents/memory_reorganized/models/procedural/models.py:146` - error: Returning Any from function declared to return "ProceduralMemory" [no-any-return]
  - ID: 7b6202a2
- `packages/haive-agents/src/haive/agents/memory_reorganized/models/procedural/models.py:157` - error: Returning Any from function declared to return "bool" [no-any-return]
  - ID: 00659f81
- `packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_iterative_refinement/__init__.py:14` - error: Returning Any from function declared to return "str" [no-any-return]
  - ID: 73c8e9f3
- `packages/haive-agents/src/haive/agents/rag/multi_agent_rag/compatibility.py:102` - error: Returning Any from function declared to return "AgentCompatibilityReport" [no-any-return]
  - ID: 7cc74e69
- `packages/haive-agents/src/haive/agents/rag/multi_agent_rag/compatibility.py:282` - error: Returning Any from function declared to return "type | None" [no-any-return]
  - ID: 3e9d03ed
- `packages/haive-agents/src/haive/agents/rag/multi_agent_rag/compatibility.py:284` - error: Returning Any from function declared to return "type | None" [no-any-return]
  - ID: d04c4039
- ... and 275 more

### haive-core

- `packages/haive-core/src/haive/core/utils/debugkit/debugging.py:79` - error: Returning Any from function declared to return "str" [no-any-return]
  - ID: 78ee2d2b
- `packages/haive-core/src/haive/core/utils/debugkit/fallbacks.py:554` - error: Returning Any from function declared to return "float" [no-any-return]
  - ID: 022226b7
- `packages/haive-core/src/haive/core/registry/memory.py:42` - error: Returning Any from function declared to return "E | None" [no-any-return]
  - ID: fb9fc628
- `packages/haive-core/src/haive/core/models/metadata_mixin.py:33` - error: Returning Any from function declared to return "int" [no-any-return]
  - ID: 3db025c6
- `packages/haive-core/src/haive/core/models/metadata_mixin.py:41` - error: Returning Any from function declared to return "int" [no-any-return]
  - ID: 3bb6ed2e
- `packages/haive-core/src/haive/core/models/metadata_mixin.py:45` - error: Returning Any from function declared to return "int" [no-any-return]
  - ID: f792f863
- `packages/haive-core/src/haive/core/models/metadata_mixin.py:47` - error: Returning Any from function declared to return "int" [no-any-return]
  - ID: 07c1cc91
- `packages/haive-core/src/haive/core/models/metadata_mixin.py:60` - error: Returning Any from function declared to return "int" [no-any-return]
  - ID: 5d7ba7c2
- `packages/haive-core/src/haive/core/models/metadata_mixin.py:69` - error: Returning Any from function declared to return "int" [no-any-return]
  - ID: 23b66ce6
- `packages/haive-core/src/haive/core/models/metadata_mixin.py:175` - error: Returning Any from function declared to return "str" [no-any-return]
  - ID: 2abb7d78
- ... and 208 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/core.py:902` - error: Returning Any from function declared to return "str | None" [no-any-return]
  - ID: 8154a887
- `packages/haive-dataflow/src/haive/dataflow/utils/vault_migration_script.py:170` - error: Returning Any from function declared to return "str | None" [no-any-return]
  - ID: 6a490b92
- `packages/haive-dataflow/src/haive/dataflow/registry/lazy_core.py:193` - error: Returning Any from function declared to return "LazyRegistrySystem" [no-any-return]
  - ID: fb6a2715
- `packages/haive-dataflow/src/haive/dataflow/registry/utils/vault_migration_script.py:170` - error: Returning Any from function declared to return "str | None" [no-any-return]
  - ID: 4a5c21e0
- `packages/haive-dataflow/src/haive/dataflow/registry/registries/model_registry.py:596` - error: Returning Any from function declared to return "str | None" [no-any-return]
  - ID: f0e604f0
- `packages/haive-dataflow/src/haive/dataflow/registry/registries/model_registry.py:619` - error: Returning Any from function declared to return "str | None" [no-any-return]
  - ID: e6e67bff
- `packages/haive-dataflow/src/haive/dataflow/registry/registries/model_registry.py:670` - error: Returning Any from function declared to return "str | None" [no-any-return]
  - ID: 13ff5107
- `packages/haive-dataflow/src/haive/dataflow/registry/registries/model_registry.py:685` - error: Returning Any from function declared to return "str | None" [no-any-return]
  - ID: 6e05883c
- `packages/haive-dataflow/src/haive/dataflow/registries/model_registry.py:596` - error: Returning Any from function declared to return "str | None" [no-any-return]
  - ID: 8bbb0dba
- `packages/haive-dataflow/src/haive/dataflow/registries/model_registry.py:619` - error: Returning Any from function declared to return "str | None" [no-any-return]
  - ID: 4b71af86
- ... and 44 more

### haive-games

- `packages/haive-games/src/haive/games/tic_tac_toe/state_manager.py:186` - error: Returning Any from function declared to return "str | None" [no-any-return]
  - ID: 95090f37
- `packages/haive-games/src/haive/games/reversi/state_manager.py:211` - error: Returning Any from function declared to return "str | None" [no-any-return]
  - ID: 0cd4eefa
- `packages/haive-games/src/haive/games/framework/core/spaces/grid.py:24` - error: Returning Any from function declared to return "int" [no-any-return]
  - ID: 6338d8fc
- `packages/haive-games/src/haive/games/framework/core/spaces/grid.py:28` - error: Returning Any from function declared to return "int" [no-any-return]
  - ID: b696a637
- `packages/haive-games/src/haive/games/framework/core/spaces/grid.py:37` - error: Returning Any from function declared to return "bool" [no-any-return]
  - ID: 9bac0ef6
- `packages/haive-games/src/haive/games/clue/state_manager.py:117` - error: Returning Any from function declared to return "str | None" [no-any-return]
  - ID: 6ab5d64e
- `packages/haive-games/src/haive/games/cards/models/card.py:261` - error: Returning Any from function declared to return "int" [no-any-return]
  - ID: f6b595e5
- `packages/haive-games/src/haive/games/hold_em/state_manager.py:662` - error: Returning Any from function declared to return "int | None" [no-any-return]
  - ID: 7974d5e9
- `packages/haive-games/src/haive/games/monopoly/utils.py:473` - error: Returning Any from function declared to return "int" [no-any-return]
  - ID: 7e91bb3f
- `packages/haive-games/src/haive/games/monopoly/utils.py:491` - error: Returning Any from function declared to return "int" [no-any-return]
  - ID: e8a2db51
- ... and 153 more

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/tools/ai_assistant.py:302` - error: Returning Any from function declared to return "SmartConfiguration" [no-any-return]
  - ID: c854d910
- `packages/haive-mcp/src/haive/mcp/downloader/legacy_core.py:186` - error: Returning Any from function declared to return "bool" [no-any-return]
  - ID: e60efe72
- `packages/haive-mcp/src/haive/mcp/downloader/legacy_core.py:452` - error: Returning Any from function declared to return "bool" [no-any-return]
  - ID: ff3aa14f
- `packages/haive-mcp/src/haive/mcp/downloader/installers.py:192` - error: Returning Any from function declared to return "bool" [no-any-return]
  - ID: 3c170226
- `packages/haive-mcp/src/haive/mcp/downloader/installers.py:315` - error: Returning Any from function declared to return "bool" [no-any-return]
  - ID: 29f8c77d
- `packages/haive-mcp/src/haive/mcp/downloader/installers.py:377` - error: Returning Any from function declared to return "bool" [no-any-return]
  - ID: 95284f86
- `packages/haive-mcp/src/haive/mcp/downloader/installers.py:400` - error: Returning Any from function declared to return "bool" [no-any-return]
  - ID: a52d5199
- `packages/haive-mcp/src/haive/mcp/downloader/installers.py:492` - error: Returning Any from function declared to return "bool" [no-any-return]
  - ID: 97932d5e
- `packages/haive-mcp/src/haive/mcp/downloader/installers.py:515` - error: Returning Any from function declared to return "bool" [no-any-return]
  - ID: d9521a1c
- `packages/haive-mcp/src/haive/mcp/downloader/installers.py:586` - error: Returning Any from function declared to return "bool" [no-any-return]
  - ID: 70705d97
- ... and 13 more

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/search_and_summarize/state.py:71` - error: Returning Any from function declared to return "str" [no-any-return]
  - ID: 76b9ec68
- `packages/haive-prebuilt/src/haive/prebuilt/search_and_summarize/state.py:75` - error: Returning Any from function declared to return "str" [no-any-return]
  - ID: ca64aca5
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/state.py:204` - error: Returning Any from function declared to return "float | None" [no-any-return]
  - ID: 8a6add74
- `packages/haive-prebuilt/src/haive/prebuilt/constituional_agent/utils.py:102` - error: Returning Any from function declared to return "str | None" [no-any-return]
  - ID: a545be73
- `packages/haive-prebuilt/src/haive/prebuilt/constituional_agent/utils.py:114` - error: Returning Any from function declared to return "bool" [no-any-return]
  - ID: e9c6508d
- `packages/haive-prebuilt/src/haive/prebuilt/ai_insight/state.py:78` - error: Returning Any from function declared to return "str" [no-any-return]
  - ID: fc1b2f94
- `packages/haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/tools.py:30` - error: Returning Any from function declared to return "str" [no-any-return]
  - ID: a42a9c13
- `packages/haive-prebuilt/src/haive/prebuilt/startup/agent.py:457` - error: Returning Any from function declared to return "StartupDevelopmentResponse" [no-any-return]
  - ID: 9603a2c3
- `packages/haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/utils.py:49` - error: Returning Any from function declared to return "BaseMessage | None" [no-any-return]
  - ID: 4c949d1c

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/reddit_search.py:113` - error: Returning Any from function declared to return "str" [no-any-return]
  - ID: db5ba52a
- `packages/haive-tools/src/haive/tools/tools/geek_jokes_tool.py:57` - error: Returning Any from function declared to return "str" [no-any-return]
  - ID: c835ecd7
- `packages/haive-tools/src/haive/tools/tools/toolkits/useless_facts_toolkit.py:66` - error: Returning Any from function declared to return "str" [no-any-return]
  - ID: 828c47b8
- `packages/haive-tools/src/haive/tools/tools/toolkits/useless_facts_toolkit.py:88` - error: Returning Any from function declared to return "str" [no-any-return]
  - ID: 53c69360
- `packages/haive-tools/src/haive/tools/tools/search_tools.py:85` - error: Returning Any from function declared to return "str" [no-any-return]
  - ID: 12fe69b2
- `packages/haive-tools/src/haive/tools/tools/search_tools.py:164` - error: Returning Any from function declared to return "str" [no-any-return]
  - ID: d98cd048

## mypy:no-overload-impl (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/graph/node/engine_node_generic.py:730` - error: An overloaded function outside a stub file must have an implementation [no-overload-impl]
  - ID: eed33b72

## mypy:no-redef (67 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_reorganized/core/classifier.py:14` - error: Name "Union" already defined (possibly by an import) [no-redef]
  - ID: 281bf759
- `packages/haive-agents/src/haive/agents/reflection/message_transformer.py:35` - error: Name "TransformationType" already defined (possibly by an import) [no-redef]
  - ID: 53feef57
- `packages/haive-agents/src/haive/agents/memory_v2/memory_state_with_tokens.py:36` - error: Name "EntityNode" already defined (possibly by an import) [no-redef]
  - ID: 400275e8
- `packages/haive-agents/src/haive/agents/memory_v2/memory_state_with_tokens.py:39` - error: Name "EntityRelationship" already defined (possibly by an import) [no-redef]
  - ID: 31a14fab
- `packages/haive-agents/src/haive/agents/memory_v2/memory_state_with_tokens.py:42` - error: Name "KnowledgeGraph" already defined (possibly by an import) [no-redef]
  - ID: 2fdddd93
- `packages/haive-agents/src/haive/agents/memory_reorganized/base/token_state.py:35` - error: Name "EntityNode" already defined (possibly by an import) [no-redef]
  - ID: f1cffb47
- `packages/haive-agents/src/haive/agents/memory_reorganized/base/token_state.py:38` - error: Name "EntityRelationship" already defined (possibly by an import) [no-redef]
  - ID: 869f6dcb
- `packages/haive-agents/src/haive/agents/memory_reorganized/base/token_state.py:41` - error: Name "KnowledgeGraph" already defined (possibly by an import) [no-redef]
  - ID: 4f3a4fc2
- `packages/haive-agents/src/haive/agents/planning/llm_compiler/utils.py:157` - error: Name "schedule_pending_task" already defined on line 11 [no-redef]
  - ID: 5f3c7f0d
- `packages/haive-agents/src/haive/agents/simple/agent_with_validation.v2.py:8` - error: Name "Dict" already defined (possibly by an import) [no-redef]
  - ID: 26f9a543
- ... and 10 more

### haive-core

- `packages/haive-core/src/haive/core/models/embeddings/__init__.py:117` - error: Name "TestEmbeddingProviders" already defined (possibly by an import) [no-redef]
  - ID: b07afbaa
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/types.py:45` - error: Name "get_origin" already defined (possibly by an import) [no-redef]
  - ID: 5ca083be
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/types.py:51` - error: Name "get_origin" already defined (possibly by an import) [no-redef]
  - ID: 28b84d48
- `packages/haive-core/src/haive/core/schema/compatibility/mergers.py:68` - error: Name "MergeStrategy" already defined (possibly by an import) [no-redef]
  - ID: 9edd948d
- `packages/haive-core/src/haive/core/persistence/handlers.py:636` - error: Name "close_async_pool_if_needed" already defined on line 478 [no-redef]
  - ID: 5efd179f
- `packages/haive-core/src/haive/core/persistence/handlers.py:768` - error: Name "register_async_thread_if_needed" already defined on line 520 [no-redef]
  - ID: b7ca8bd2
- `packages/haive-core/src/haive/core/engine/document/loaders/sources/local/base.py:50` - error: Name "is_file" already defined on line 35 [no-redef]
  - ID: cb097d85
- `packages/haive-core/src/haive/core/engine/document/loaders/sources/base/base.py:42` - error: Name "source_class" already defined on line 33 [no-redef]
  - ID: 93870f5b
- `packages/haive-core/src/haive/core/graph/state_graph_manager.py:268` - error: Name "get_metadata" already defined on line 160 [no-redef]
  - ID: a7cff68f
- `packages/haive-core/src/haive/core/tools/__init__.py:36` - error: Name "tool" already defined (possibly by an import) [no-redef]
  - ID: 98396b03
- ... and 18 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/core.py:971` - error: Name "\_ensure_registry_schema" already defined on line 99 [no-redef]
  - ID: 64d55af4
- `packages/haive-dataflow/src/haive/dataflow/registry/core.py:1040` - error: Name "\_ensure_registry_schema" already defined on line 163 [no-redef]
  - ID: 36e0c85b
- `packages/haive-dataflow/src/haive/dataflow/internal_websockets/handlers.py:28` - error: Name "AgentRegistry" already defined (possibly by an import) [no-redef]
  - ID: 102f529e
- `packages/haive-dataflow/src/haive/dataflow/api/routes/conversation_routes.py:69` - error: Name "AgentRegistry" already defined (possibly by an import) [no-redef]
  - ID: 6a58b5b1

### haive-games

- `packages/haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:14` - error: Name "Game" already defined (possibly by an import) [no-redef]
  - ID: a38e6119
- `packages/haive-games/src/haive/games/mastermind/demo.py:283` - error: Name "MastermindUI" already defined on line 132 [no-redef]
  - ID: 38f75601
- `packages/haive-games/src/haive/games/multi_player/agent.py:625` - error: Name "get_player_role" already defined on line 181 [no-redef]
  - ID: 26fe1709
- `packages/haive-games/src/haive/games/framework/multi_player/agent.py:669` - error: Name "get_player_role" already defined on line 182 [no-redef]
  - ID: a743ec64
- `packages/haive-games/src/haive/games/battleship/agent.py:699` - error: Name "analyze_position" already defined on line 310 [no-redef]
  - ID: 394bba0d

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/downloader/legacy_core.py:190` - error: Name "\_run_command" already defined on line 119 [no-redef]
  - ID: 696c914d
- `packages/haive-mcp/src/haive/mcp/downloader/legacy_core.py:275` - error: Name "\_run_command" already defined on line 223 [no-redef]
  - ID: 9e864474
- `packages/haive-mcp/src/haive/mcp/downloader/legacy_core.py:369` - error: Name "\_run_command" already defined on line 303 [no-redef]
  - ID: d95ba9e4
- `packages/haive-mcp/src/haive/mcp/downloader/legacy_core.py:456` - error: Name "\_run_command" already defined on line 402 [no-redef]
  - ID: f03351ac

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/utils.py:14` - error: Name "Markdown" already defined (possibly by an import) [no-redef]
  - ID: 0889c390

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/vbible_toolkit.py:53` - error: Name "query_bible_by_reference" already defined (possibly by an import) [no-redef]
  - ID: 38aa54b9
- `packages/haive-tools/src/haive/tools/tools/toolkits/vbible_toolkit.py:102` - error: Name "get_random_verse" already defined (possibly by an import) [no-redef]
  - ID: f2986ac6
- `packages/haive-tools/src/haive/tools/tools/toolkits/vbible_toolkit.py:139` - error: Name "list_translations" already defined (possibly by an import) [no-redef]
  - ID: 5916f0ec
- `packages/haive-tools/src/haive/tools/tools/toolkits/vbible_toolkit.py:179` - error: Name "list_books" already defined (possibly by an import) [no-redef]
  - ID: eaeeb58c
- `packages/haive-tools/src/haive/tools/tools/toolkits/vbible_toolkit.py:225` - error: Name "get_chapter_verses" already defined (possibly by an import) [no-redef]
  - ID: 6f167567

## mypy:no-untyped-def (4566 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/wiki_writer/utils.py:6` - error: Function is missing a type annotation for one or more arguments [no-untyped-def]
  - ID: 05a6f6f9
- `packages/haive-agents/src/haive/agents/wiki_writer/utils.py:13` - error: Function is missing a type annotation for one or more arguments [no-untyped-def]
  - ID: c829b3a1
- `packages/haive-agents/src/haive/agents/wiki_writer/utils.py:20` - error: Function is missing a type annotation for one or more arguments [no-untyped-def]
  - ID: 821858b8
- `packages/haive-agents/src/haive/agents/wiki_writer/interview/utils.py:4` - error: Function is missing a type annotation for one or more arguments [no-untyped-def]
  - ID: 8f393de2
- `packages/haive-agents/src/haive/agents/wiki_writer/interview/utils.py:12` - error: Function is missing a type annotation for one or more arguments [no-untyped-def]
  - ID: 7c656ef6
- `packages/haive-agents/src/haive/agents/wiki_writer/interview/utils.py:19` - error: Function is missing a type annotation for one or more arguments [no-untyped-def]
  - ID: 1e8e9a3d
- `packages/haive-agents/src/haive/agents/task_analysis/tree/models.py:18` - error: Function is missing a type annotation for one or more arguments [no-untyped-def]
  - ID: d9f75df0
- `packages/haive-agents/src/haive/agents/task_analysis/tree/models.py:26` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 16de0f08
- `packages/haive-agents/src/haive/agents/task_analysis/tree/models.py:32` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 4f180a4a
- `packages/haive-agents/src/haive/agents/task_analysis/tree/models.py:50` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: a4ad5f82
- ... and 1805 more

### haive-core

- `packages/haive-core/src/haive/core/errors.py:4` - error: Function is missing a type annotation for one or more arguments [no-untyped-def]
  - ID: 24d10d4e
- `packages/haive-core/src/haive/core/utils/visualize_graph_utils.py:9` - error: Function is missing a type annotation [no-untyped-def]
  - ID: 87d1c98f
- `packages/haive-core/src/haive/core/utils/state_utils.py:1` - error: Function is missing a type annotation [no-untyped-def]
  - ID: b039aa35
- `packages/haive-core/src/haive/core/utils/getter_mixin.py:61` - error: Function is missing a type annotation for one or more arguments [no-untyped-def]
  - ID: 6c4a0c0c
- `packages/haive-core/src/haive/core/utils/getter_mixin.py:137` - error: Function is missing a type annotation for one or more arguments [no-untyped-def]
  - ID: a7ad3b95
- `packages/haive-core/src/haive/core/utils/pydantic_utils/sync_properties.py:7` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 7f2209a8
- `packages/haive-core/src/haive/core/utils/pydantic_utils/sync_properties.py:10` - error: Function is missing a type annotation for one or more arguments [no-untyped-def]
  - ID: 1919410a
- `packages/haive-core/src/haive/core/utils/pydantic_utils/sync_properties.py:13` - error: Function is missing a type annotation for one or more arguments [no-untyped-def]
  - ID: 993a53c1
- `packages/haive-core/src/haive/core/utils/pydantic_utils/sync_properties.py:14` - error: Function is missing a type annotation for one or more arguments [no-untyped-def]
  - ID: 6ff3c32a
- `packages/haive-core/src/haive/core/utils/pydantic_utils/sync_properties.py:17` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 2e31a1d2
- ... and 1252 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/db/inspect_supabase.py:10` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 9186fdc5
- `packages/haive-dataflow/src/haive/dataflow/__init__.py:112` - error: Function is missing a type annotation [no-untyped-def]
  - ID: 72cd9729
- `packages/haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:35` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 0707d7ad
- `packages/haive-dataflow/src/haive/dataflow/providers/agent_provider.py:35` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 531ac8ed
- `packages/haive-dataflow/src/haive/dataflow/core.py:74` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 6cd2a5e8
- `packages/haive-dataflow/src/haive/dataflow/core.py:99` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 59caf38b
- `packages/haive-dataflow/src/haive/dataflow/core.py:208` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 97de981b
- `packages/haive-dataflow/src/haive/dataflow/core.py:502` - error: Function is missing a type annotation [no-untyped-def]
  - ID: 460efcf4
- `packages/haive-dataflow/src/haive/dataflow/core.py:563` - error: Function is missing a type annotation [no-untyped-def]
  - ID: a7a58bf3
- `packages/haive-dataflow/src/haive/dataflow/core.py:672` - error: Function is missing a type annotation [no-untyped-def]
  - ID: 40c547ae
- ... and 395 more

### haive-games

- `packages/haive-games/src/haive/games/llm_config_factory.py:64` - error: Function is missing a type annotation for one or more arguments [no-untyped-def]
  - ID: d3b2a6e3
- `packages/haive-games/src/haive/games/tic_tac_toe/state_manager.py:17` - error: Function is missing a type annotation for one or more arguments [no-untyped-def]
  - ID: 0f30c763
- `packages/haive-games/src/haive/games/single_player/example.py:1` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 68217493
- `packages/haive-games/src/haive/games/single_player/example.py:89` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: d7736aa4
- `packages/haive-games/src/haive/games/reversi/state_manager.py:29` - error: Function is missing a type annotation for one or more arguments [no-untyped-def]
  - ID: e984a103
- `packages/haive-games/src/haive/games/reversi/example.py:42` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: c39db0ac
- `packages/haive-games/src/haive/games/multi_player/factory.py:128` - error: Function is missing a type annotation [no-untyped-def]
  - ID: 47a15250
- `packages/haive-games/src/haive/games/framework/multi_player/factory.py:128` - error: Function is missing a type annotation [no-untyped-def]
  - ID: 152a0b69
- `packages/haive-games/src/haive/games/framework/core/agent.py:18` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: f8141b1e
- `packages/haive-games/src/haive/games/framework/base/utils.py:23` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: e2f5bcb9
- ... and 715 more

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/discovery/server_discovery.py:9` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 9a765c98
- `packages/haive-mcp/src/haive/mcp/launcher.py:13` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 25007f02
- `packages/haive-mcp/src/haive/mcp/launcher.py:19` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 8ec2171f
- `packages/haive-mcp/src/haive/mcp/launcher.py:25` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 621691f6
- `packages/haive-mcp/src/haive/mcp/launcher.py:31` - error: Function is missing a type annotation [no-untyped-def]
  - ID: f0da9f82
- `packages/haive-mcp/src/haive/mcp/launcher.py:42` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 941681e6
- `packages/haive-mcp/src/haive/mcp/launcher.py:48` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 8ccb2941
- `packages/haive-mcp/src/haive/mcp/tools/server_selector.py:98` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: a97c3467
- `packages/haive-mcp/src/haive/mcp/tools/server_selector.py:236` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: e2487c52
- `packages/haive-mcp/src/haive/mcp/tools/ai_assistant.py:87` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: b47a53b8
- ... and 161 more

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/project_manager/aug_llms.py:5` - error: Function is missing a type annotation [no-untyped-def]
  - ID: 00bf5606
- `packages/haive-prebuilt/src/haive/prebuilt/project_manager/aug_llms.py:26` - error: Function is missing a type annotation [no-untyped-def]
  - ID: da04ef7a
- `packages/haive-prebuilt/src/haive/prebuilt/ai_insight/example.py:15` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 2439a6e7
- `packages/haive-prebuilt/src/haive/prebuilt/ai_insight/example.py:62` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: f561f219
- `packages/haive-prebuilt/src/haive/prebuilt/ai_insight/example.py:112` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 7dd14c38
- `packages/haive-prebuilt/src/haive/prebuilt/ai_insight/example.py:157` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 1727f4d2
- `packages/haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/models.py:103` - error: Function is missing a type annotation [no-untyped-def]
  - ID: 8b5d1e22
- `packages/haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/models.py:127` - error: Function is missing a type annotation [no-untyped-def]
  - ID: 571e941d
- `packages/haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/models.py:156` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 385c2cfa
- `packages/haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/models.py:214` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 0d3ff2aa
- ... and 110 more

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/remote_execution.py:27` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: bfc9fb6b
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/remote_execution.py:33` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 688903b8
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/remote_execution.py:41` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: f310b372
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/logger.py:25` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 63e52a0e
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/background_process_manager.py:41` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: c435a895
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/type_checking.py:32` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: ae85d4b0
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/import_analyzer.py:37` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: f0ed51bb
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/function_call_analyzer.py:33` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: f1565fcf
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/complexity_analyzer.py:39` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 69cdf6b7
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/code_smell_detector.py:30` - error: Function is missing a return type annotation [no-untyped-def]
  - ID: 15ec3678
- ... and 58 more

## mypy:object (6 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/conversation/debate/agent.py:144` - error: Incompatible types in assignment (expression has type "bool", target has type "Sequence[objec
  - ID: 6be87d60
- `packages/haive-agents/src/haive/agents/patterns/react_structured_agent_variants.py:415` - error: Argument "stages" to "create_multi_stage_reasoning_agent" has incompatible type "list[object]
  - ID: dea2fade
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/agent.py:491` - error: Argument "content" to "HumanMessage" has incompatible type "Sequence[object]"; expected "str
  - ID: 07000aac
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/agent.py:519` - error: Argument "content" to "HumanMessage" has incompatible type "Sequence[object]"; expected "str
  - ID: 87ebad79

### haive-games

- `packages/haive-games/src/haive/games/nim/example.py:825` - error: Argument 1 to "sum" has incompatible type "list[object]"; expected "Iterable[bool]" [arg-typ
  - ID: 690087cf
- `packages/haive-games/src/haive/games/nim/example.py:827` - error: Argument 1 to "sum" has incompatible type "list[object]"; expected "Iterable[bool]" [arg-typ
  - ID: 44939a4c

## mypy:operator (118 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/rag/self_rag2/nodes/grade_generation_v_documents_and_question.py:31` - error: Module not callable [operator]
  - ID: 3fa481d1
- `packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/example.py:463` - error: Unsupported operand types for - ("float" and "None") [operator]
  - ID: 09750691
- `packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/example.py:463` - error: Unsupported operand types for - ("float" and "None") [operator]
  - ID: 09750691
- `packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/example.py:463` - error: Unsupported operand types for - ("float" and "None") [operator]
  - ID: 09750691
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/models.py:126` - error: No overload variant of "**add**" of "list" matches argument type "str" [operator]
  - ID: fb893ad7
- `packages/haive-agents/src/haive/agents/memory_reorganized/retrieval/enhanced_retriever.py:458` - error: Unsupported operand types for + ("object" and "int") [operator]
  - ID: 263d0fcf
- `packages/haive-agents/src/haive/agents/memory_reorganized/retrieval/enhanced_retriever.py:463` - error: Unsupported operand types for \* ("object" and "int") [operator]
  - ID: 3765a5f7
- `packages/haive-agents/src/haive/agents/memory_reorganized/retrieval/enhanced_retriever.py:464` - error: Unsupported operand types for - ("object" and "int") [operator]
  - ID: 71848944
- `packages/haive-agents/src/haive/agents/memory_reorganized/retrieval/enhanced_retriever.py:464` - error: Unsupported operand types for - ("object" and "int") [operator]
  - ID: 71848944
- `packages/haive-agents/src/haive/agents/memory_reorganized/retrieval/enhanced_retriever.py:466` - error: Unsupported operand types for \* ("object" and "int") [operator]
  - ID: 5b108afc
- ... and 45 more

### haive-core

- `packages/haive-core/src/haive/core/utils/debugkit/benchmarking/load.py:97` - error: Unsupported operand types for - ("float" and "object") [operator]
  - ID: 53e202cb
- `packages/haive-core/src/haive/core/schema/compatibility/types.py:232` - error: "str" not callable [operator]
  - ID: f0e81169
- `packages/haive-core/src/haive/core/schema/compatibility/types.py:242` - error: "str" not callable [operator]
  - ID: 399d2cc5
- `packages/haive-core/src/haive/core/engine/document/loaders/sources/final_sources.py:1057` - error: Unsupported operand types for in ("LoaderCapability" and "SourceCapabilities") [operator]
  - ID: 59a53674
- `packages/haive-core/src/haive/core/engine/document/loaders/sources/final_sources.py:1067` - error: Unsupported operand types for in ("LoaderCapability" and "SourceCapabilities") [operator]
  - ID: 1e91234e
- `packages/haive-core/src/haive/core/engine/document/loaders/sources/communication_sources.py:1056` - error: Unsupported operand types for in ("LoaderCapability" and "SourceCapabilities") [operator]
  - ID: 35326669
- `packages/haive-core/src/haive/core/engine/document/loaders/sources/cloud_storage_sources.py:967` - error: Unsupported operand types for in ("LoaderCapability" and "SourceCapabilities") [operator]
  - ID: 77825236
- `packages/haive-core/src/haive/core/engine/document/loaders/sources/analytics_sources.py:995` - error: Unsupported operand types for in ("LoaderCapability" and "SourceCapabilities") [operator]
  - ID: 2d79000c
- `packages/haive-core/src/haive/core/engine/document/loaders/sources/analytics_sources.py:1005` - error: Unsupported operand types for in ("LoaderCapability" and "SourceCapabilities") [operator]
  - ID: 82d85672
- `packages/haive-core/src/haive/core/engine/document/loaders/auto_loader.py:1451` - error: "AutoLoader" not callable [operator]
  - ID: 86768ecd

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/registry/core.py:1257` - error: Unsupported operand types for + ("str" and "None") [operator]
  - ID: 332102a4
- `packages/haive-dataflow/src/haive/dataflow/registry/core.py:1259` - error: Unsupported operand types for + ("str" and "None") [operator]
  - ID: 13cd3e6f
- `packages/haive-dataflow/src/haive/dataflow/registry/core.py:1260` - error: Unsupported operand types for + ("str" and "None") [operator]
  - ID: 8f6dca6d
- `packages/haive-dataflow/src/haive/dataflow/registry/core.py:1261` - error: Unsupported operand types for + ("str" and "None") [operator]
  - ID: 37dfa63d
- `packages/haive-dataflow/src/haive/dataflow/registry/core.py:1262` - error: Unsupported operand types for + ("str" and "None") [operator]
  - ID: 72bd901a
- `packages/haive-dataflow/src/haive/dataflow/registry/core.py:1265` - error: Unsupported operand types for + ("str" and "None") [operator]
  - ID: c72c1e4e
- `packages/haive-dataflow/src/haive/dataflow/api/game_router.py:213` - error: "object" not callable [operator]
  - ID: 57f5e11e
- `packages/haive-dataflow/src/haive/dataflow/api/game_router.py:216` - error: "object" not callable [operator]
  - ID: f5ff5f3a
- `packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:531` - error: Unsupported right operand type for in ("object") [operator]
  - ID: 267fd1e3
- `packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:540` - error: Unsupported right operand type for in ("object") [operator]
  - ID: e07755f2
- ... and 2 more

### haive-games

- `packages/haive-games/src/haive/games/nim/example.py:812` - error: Unsupported operand types for / ("object" and "int") [operator]
  - ID: 9d496240
- `packages/haive-games/src/haive/games/hold_em/ui.py:157` - error: Unsupported operand types for + ("int" and "str") [operator]
  - ID: 3451bb70
- `packages/haive-games/src/haive/games/tic_tac_toe/configurable_config.py:301` - error: "object" not callable [operator]
  - ID: 3d49f4a0
- `packages/haive-games/src/haive/games/single_player/sudoku/game/cell.py:27` - error: "bool" not callable [operator]
  - ID: 4e83e09b
- `packages/haive-games/src/haive/games/single_player/sudoku/game/cell.py:40` - error: "bool" not callable [operator]
  - ID: 81391d53
- `packages/haive-games/src/haive/games/single_player/sudoku/game/cell.py:52` - error: "bool" not callable [operator]
  - ID: 431ea8e0
- `packages/haive-games/src/haive/games/single_player/flow_free/base.py:328` - error: Unsupported left operand type for == (any?) [operator]
  - ID: 77b5a1c6
- `packages/haive-games/src/haive/games/risk/configurable_config.py:308` - error: "object" not callable [operator]
  - ID: 07053ba9
- `packages/haive-games/src/haive/games/reversi/configurable_config.py:306` - error: "object" not callable [operator]
  - ID: ada6d366
- `packages/haive-games/src/haive/games/poker/configurable_config.py:308` - error: "object" not callable [operator]
  - ID: 88916f13
- ... and 15 more

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/tools/ai_assistant.py:702` - error: Unsupported operand types for + ("object" and "int") [operator]
  - ID: 6b2269fa
- `packages/haive-mcp/src/haive/mcp/tools/ai_assistant.py:715` - error: Unsupported operand types for < ("int" and "object") [operator]
  - ID: 32996707
- `packages/haive-mcp/src/haive/mcp/agents/transferable_mcp_agent.py:556` - error: Unsupported operand types for + ("object" and "int") [operator]
  - ID: 8c06319d

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:161` - error: Unsupported operand types for > ("float" and "None") [operator]
  - ID: 62c053d2
- `packages/haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:161` - error: Unsupported operand types for > ("float" and "None") [operator]
  - ID: 62c053d2
- `packages/haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:161` - error: Unsupported operand types for > ("float" and "None") [operator]
  - ID: 62c053d2
- `packages/haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:164` - error: Unsupported operand types for > ("float" and "None") [operator]
  - ID: afa00cd8
- `packages/haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:164` - error: Unsupported operand types for > ("float" and "None") [operator]
  - ID: afa00cd8
- `packages/haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:164` - error: Unsupported operand types for > ("float" and "None") [operator]
  - ID: afa00cd8
- `packages/haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:380` - error: Unsupported operand types for \* ("None" and "float") [operator]
  - ID: 6597bfd9
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/tools.py:459` - error: Unsupported operand types for <= ("float" and "object") [operator]
  - ID: bd232444
- `packages/haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:332` - error: No overload variant of "**add**" of "list" matches argument type "str" [operator]
  - ID: ea16c2e3
- `packages/haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:142` - error: Unsupported operand types for | ("PromptTemplate" and "None") [operator]
  - ID: 1565da12
- ... and 2 more

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/brave_search.py:24` - error: Module not callable [operator]
  - ID: b82254db

## mypy:overload-cannot-match (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/graph/node/engine_node_generic.py:737` - error: Overloaded function signature 2 will never be matched: signature 1's parameter type(s) are th
  - ID: b092b8c9

## mypy:override (25 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/planning/base/models.py:391` - error: Argument 1 of "insert" is incompatible with supertype "builtins.list"; supertype defines the
  - ID: 6c0fc8ec
- `packages/haive-agents/src/haive/agents/planning/base/models.py:419` - error: Argument 1 of "pop" is incompatible with supertype "builtins.list"; supertype defines the arg
  - ID: 5cf18c34
- `packages/haive-agents/src/haive/agents/reflection/message_transformer_posthook.py:207` - error: Signature of "**call**" incompatible with supertype "MessageTransformerPostHook" [override]
  - ID: 699654a2
- `packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_base/models.py:62` - error: Signature of "transform_documents" incompatible with supertype "langchain_core.documents.tran
  - ID: 682fbf46

### haive-core

- `packages/haive-core/src/haive/core/graph/state_graph/state_graph.py:467` - error: Signature of "validate" incompatible with supertype "pydantic.main.BaseModel" [override]
  - ID: a1b890bb
- `packages/haive-core/src/haive/core/engine/document/sources/base.py:40` - error: Signature of "validate" incompatible with supertype "pydantic.main.BaseModel" [override]
  - ID: 6214b18c
- `packages/haive-core/src/haive/core/runtime/base/base.py:36` - error: Signature of "invoke" incompatible with supertype "langchain_core.runnables.base.Runnable" [
  - ID: 77eea9cc
- `packages/haive-core/src/haive/core/runtime/base/base.py:41` - error: Signature of "ainvoke" incompatible with supertype "langchain_core.runnables.base.Runnable"
  - ID: ad19c6bf
- `packages/haive-core/src/haive/core/persistence/serializers.py:159` - error: Signature of "\_encode_constructor_args" incompatible with supertype "langgraph.checkpoint.ser
  - ID: b3c007d8
- `packages/haive-core/src/haive/core/persistence/postgres_saver_with_thread_creation.py:99` - error: Argument 1 of "put" is incompatible with supertype "langgraph.checkpoint.postgres.PostgresSav
  - ID: ef16dc46
- `packages/haive-core/src/haive/core/persistence/postgres_saver_with_thread_creation.py:99` - error: Argument 1 of "put" is incompatible with supertype "langgraph.checkpoint.postgres.PostgresSav
  - ID: ef16dc46
- `packages/haive-core/src/haive/core/persistence/postgres_saver_with_thread_creation.py:126` - error: Signature of "put_writes" incompatible with supertype "langgraph.checkpoint.postgres.Postgres
  - ID: ad73e0e9
- `packages/haive-core/src/haive/core/persistence/postgres_saver_with_thread_creation.py:126` - error: Signature of "put_writes" incompatible with supertype "langgraph.checkpoint.postgres.Postgres
  - ID: ad73e0e9
- `packages/haive-core/src/haive/core/persistence/postgres_saver_override.py:65` - error: Signature of "from_conn_string" incompatible with supertype "langgraph.checkpoint.postgres.Po
  - ID: 2cc80cd1
- ... and 2 more

### haive-games

- `packages/haive-games/src/haive/games/framework/core/rule.py:26` - error: Signature of "validate" incompatible with supertype "pydantic.main.BaseModel" [override]
  - ID: 28f1f196
- `packages/haive-games/src/haive/games/framework/core/player.py:96` - error: Return type "M@AIPlayer | None" of "get_move" incompatible with return type "M | None" in sup
  - ID: 21c59526
- `packages/haive-games/src/haive/games/framework/core/player.py:96` - error: Return type "M@AIPlayer | None" of "get_move" incompatible with return type "M | None" in sup
  - ID: 21c59526
- `packages/haive-games/src/haive/games/framework/core/player.py:117` - error: Return type "M@RandomAIPlayer | None" of "get_move" incompatible with return type "M | None"
  - ID: b29c853d
- `packages/haive-games/src/haive/games/framework/core/player.py:117` - error: Return type "M@RandomAIPlayer | None" of "get_move" incompatible with return type "M | None"
  - ID: b29c853d
- `packages/haive-games/src/haive/games/framework/core/player.py:143` - error: Return type "M@RuleBasedAIPlayer | None" of "get_move" incompatible with return type "M | Non
  - ID: b6b5baf1
- `packages/haive-games/src/haive/games/framework/core/player.py:143` - error: Return type "M@RuleBasedAIPlayer | None" of "get_move" incompatible with return type "M | Non
  - ID: b6b5baf1
- `packages/haive-games/src/haive/games/core/components/cards/scoring.py:23` - error: Argument 1 of "**eq**" is incompatible with supertype "builtins.object"; supertype defines th
  - ID: c9cf8f85

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/translate_tools.py:190` - error: Signature of "\_arun" incompatible with supertype "langchain_core.tools.base.BaseTool" [overr
  - ID: d0a43fc5

## mypy:prop-decorator (387 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/research/storm/state.py:109` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: d71e3cf6
- `packages/haive-agents/src/haive/agents/research/perplexity/pro_search/models.py:17` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 325502d7
- `packages/haive-agents/src/haive/agents/research/perplexity/pro_search/models.py:108` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: bf13e55f
- `packages/haive-agents/src/haive/agents/research/perplexity/pro_search/models.py:114` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 020b4896
- `packages/haive-agents/src/haive/agents/research/perplexity/pro_search/models.py:130` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: b4f24ac8
- `packages/haive-agents/src/haive/agents/research/perplexity/pro_search/models.py:138` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 456278ed
- `packages/haive-agents/src/haive/agents/research/perplexity/pro_search/models.py:151` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: c87dbabb
- `packages/haive-agents/src/haive/agents/research/perplexity/pro_search/models.py:157` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 5929726a
- `packages/haive-agents/src/haive/agents/research/perplexity/pro_search/models.py:190` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 38fd2e8a
- `packages/haive-agents/src/haive/agents/research/perplexity/pro_search/models.py:199` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: f6823f3a
- ... and 139 more

### haive-core

- `packages/haive-core/src/haive/core/schema/prebuilt/validation_aware_tool_state.py:53` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: bb5779ab
- `packages/haive-core/src/haive/core/schema/prebuilt/validation_aware_tool_state.py:62` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: f421be99
- `packages/haive-core/src/haive/core/schema/prebuilt/validation_aware_tool_state.py:71` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 2b8a8e1f
- `packages/haive-core/src/haive/core/schema/prebuilt/validation_aware_tool_state.py:90` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 58434141
- `packages/haive-core/src/haive/core/schema/prebuilt/validation_aware_tool_state.py:109` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 86fa25f6
- `packages/haive-core/src/haive/core/schema/prebuilt/validation_aware_tool_state.py:115` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: ac624e39
- `packages/haive-core/src/haive/core/schema/prebuilt/validation_aware_tool_state.py:125` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 43f1d1cf
- `packages/haive-core/src/haive/core/schema/prebuilt/validation_aware_tool_state.py:139` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 807c2d01
- `packages/haive-core/src/haive/core/schema/prebuilt/multi_agent_state.py:390` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 8fc6c544
- `packages/haive-core/src/haive/core/schema/prebuilt/multi_agent_state.py:396` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 4fed4a2c
- ... and 28 more

### haive-games

- `packages/haive-games/src/haive/games/tic_tac_toe/models.py:138` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 771c9501
- `packages/haive-games/src/haive/games/tic_tac_toe/models.py:154` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 87126963
- `packages/haive-games/src/haive/games/tic_tac_toe/models.py:165` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: c210c622
- `packages/haive-games/src/haive/games/tic_tac_toe/models.py:176` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: df879e51
- `packages/haive-games/src/haive/games/tic_tac_toe/models.py:408` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 6f10b2fc
- `packages/haive-games/src/haive/games/tic_tac_toe/models.py:419` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: dbe627d1
- `packages/haive-games/src/haive/games/tic_tac_toe/models.py:437` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 157382d3
- `packages/haive-games/src/haive/games/tic_tac_toe/config.py:212` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 0c1f034c
- `packages/haive-games/src/haive/games/tic_tac_toe/config.py:230` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 21a60fcf
- `packages/haive-games/src/haive/games/single_player/towers_of_hanoi/position.py:28` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: e573fac8
- ... and 162 more

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/state.py:148` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 30f8c736
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/state.py:155` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 590e8e4c
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/state.py:162` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 48e73a93
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/state.py:178` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: be018f44
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/state.py:185` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: e2618f5a
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/state.py:200` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 3b561f70
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/state.py:207` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: e11f5118
- `packages/haive-prebuilt/src/haive/prebuilt/search_and_summarize/state.py:66` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: b2119efb
- `packages/haive-prebuilt/src/haive/prebuilt/search_and_summarize/state.py:78` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 3d1cd667
- `packages/haive-prebuilt/src/haive/prebuilt/search_and_summarize/state.py:89` - error: Decorators on top of @property are not supported [prop-decorator]
  - ID: 2ddeec52
- ... and 18 more

## mypy:return (8 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/planning/rewoo/tests/test_tool_step.py:278` - error: Missing return statement [return]
  - ID: aa6bb9b5

### haive-core

- `packages/haive-core/src/haive/core/common/mixins/timestamp_mixin.py:164` - error: Missing return statement [return]
  - ID: 2aec4a43
- `packages/haive-core/src/haive/core/graph/node/callable_node.py:138` - error: Missing return statement [return]
  - ID: 6cf20eee
- `packages/haive-core/src/haive/core/graph/dynamic_graph_builder.py:1876` - error: Missing return statement [return]
  - ID: d5b01398

### haive-games

- `packages/haive-games/src/haive/games/chess/agent.py:127` - error: Missing return statement [return]
  - ID: 73325162

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/documentation/doc_loader.py:197` - error: Missing return statement [return]
  - ID: 86ce2e4b

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/models.py:19` - error: Missing return statement [return]
  - ID: 86f293de
- `packages/haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/tools.py:36` - error: Missing return statement [return]
  - ID: f48c60bf

## mypy:return-value (60 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/archive/meta/agent.py:168` - error: Incompatible return value type (got "None", expected "TAgent") [return-value]
  - ID: 635c39da
- `packages/haive-agents/src/haive/agents/rag/simple/enhanced_v3/agent.py:236` - error: Incompatible return value type (got "object", expected "RetrieverAgent") [return-value]
  - ID: 0e68d758
- `packages/haive-agents/src/haive/agents/rag/simple/enhanced_v3/agent.py:240` - error: Incompatible return value type (got "object", expected "SimpleAnswerAgent") [return-value]
  - ID: 81ff359f
- `packages/haive-agents/src/haive/agents/research/open_perplexity/agent.py:774` - error: Incompatible return value type (got "None", expected "str") [return-value]
  - ID: bc3f1d1c
- `packages/haive-agents/src/haive/agents/research/open_perplexity/agent.py:792` - error: Incompatible return value type (got "None", expected "str") [return-value]
  - ID: f292af5e

### haive-core

- `packages/haive-core/src/haive/core/schema/composer/engine/engine_detector.py:151` - error: Incompatible return value type (got "None", expected "type") [return-value]
  - ID: 38a0a038
- `packages/haive-core/src/haive/core/tools/store_tools.py:145` - error: Incompatible return value type (got "BaseTool", expected "Tool") [return-value]
  - ID: 7951f616
- `packages/haive-core/src/haive/core/tools/store_tools.py:227` - error: Incompatible return value type (got "BaseTool", expected "Tool") [return-value]
  - ID: ce2a62fc
- `packages/haive-core/src/haive/core/tools/store_tools.py:292` - error: Incompatible return value type (got "BaseTool", expected "Tool") [return-value]
  - ID: 93390e5b
- `packages/haive-core/src/haive/core/tools/store_tools.py:367` - error: Incompatible return value type (got "BaseTool", expected "Tool") [return-value]
  - ID: e499aa03
- `packages/haive-core/src/haive/core/tools/store_tools.py:422` - error: Incompatible return value type (got "BaseTool", expected "Tool") [return-value]
  - ID: 9bc0cace
- `packages/haive-core/src/haive/core/graph/node/validation_node_with_routing.py:527` - error: Incompatible return value type (got "Any | None", expected "str") [return-value]
  - ID: 93288c6a
- `packages/haive-core/src/haive/core/persistence/serializers.py:254` - error: Incompatible return value type (got "EncryptedSerializer", expected "JsonPlusSerializer") [r
  - ID: e56071ef
- `packages/haive-core/src/haive/core/persistence/serializers.py:328` - error: Incompatible return value type (got "EncryptedSerializer", expected "JsonPlusSerializer") [r
  - ID: 0d5fc20e
- `packages/haive-core/src/haive/core/models/vectorstore/base.py:176` - error: Incompatible return value type (got "VectorStoreConfig", expected "VectorStore") [return-val
  - ID: e585c654
- ... and 39 more

### haive-games

- `packages/haive-games/src/haive/games/checkers/example.py:574` - error: Incompatible return value type (got "None", expected "str") [return-value]
  - ID: b7dbb65e

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/downloader/discovery.py:624` - error: Incompatible return value type (got "None", expected "str") [return-value]
  - ID: 98dda5c8
- `packages/haive-mcp/src/haive/mcp/installers/advanced_code_installer.py:333` - error: Incompatible return value type (got "BaseTool", expected "StructuredTool") [return-value]
  - ID: a56e2bce

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:103` - error: Incompatible return value type (got "TavilySearchResults", expected "StructuredTool") [retur
  - ID: 54810ba5
- `packages/haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/agent.py:349` - error: Incompatible return value type (got "CompiledStateGraph", expected "StateGraph") [return-val
  - ID: 81f8702d
- `packages/haive-prebuilt/src/haive/prebuilt/startup/market_research/agent.py:266` - error: Incompatible return value type (got "CompiledStateGraph", expected "StateGraph") [return-val
  - ID: 673edc9f

## mypy:str (183 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/base/typed_agent.py:498` - error: Argument 2 to "AdaptiveAgent" has incompatible type "Any | None"; expected "list[str]" [arg-
  - ID: 86292aab
- `packages/haive-agents/src/haive/agents/supervisor/simple_test_runner.py:428` - error: Value of type "Collection[str]" is not indexable [index]
  - ID: fb4170ac
- `packages/haive-agents/src/haive/agents/supervisor/simple_test_runner.py:429` - error: Value of type "Collection[str]" is not indexable [index]
  - ID: d28ee633
- `packages/haive-agents/src/haive/agents/supervisor/simple_test_runner.py:430` - error: Value of type "Collection[str]" is not indexable [index]
  - ID: 79e6b5fa
- `packages/haive-agents/src/haive/agents/supervisor/simple_test_runner.py:433` - error: Value of type "Collection[str]" is not indexable [index]
  - ID: 586397cd
- `packages/haive-agents/src/haive/agents/supervisor/simple_test_runner.py:436` - error: Value of type "Collection[str]" is not indexable [index]
  - ID: 79929728
- `packages/haive-agents/src/haive/agents/supervisor/simple_test_runner.py:440` - error: Value of type "Collection[str]" is not indexable [index]
  - ID: 6479ee94
- `packages/haive-agents/src/haive/agents/supervisor/simple_test_runner.py:442` - error: Value of type "Collection[str]" is not indexable [index]
  - ID: 4d478b71
- `packages/haive-agents/src/haive/agents/supervisor/archive/simple_test_runner.py:428` - error: Value of type "Collection[str]" is not indexable [index]
  - ID: e6dd8e82
- `packages/haive-agents/src/haive/agents/supervisor/archive/simple_test_runner.py:429` - error: Value of type "Collection[str]" is not indexable [index]
  - ID: 30cba156
- ... and 60 more

### haive-core

- `packages/haive-core/src/haive/core/engine/vectorstore/discovery.py:71` - error: Incompatible types in assignment (expression has type "None", variable has type "list[str]")
  - ID: 2710c0d0
- `packages/haive-core/src/haive/core/engine/vectorstore/discovery.py:72` - error: Incompatible types in assignment (expression has type "None", variable has type "list[str]")
  - ID: 699920b7
- `packages/haive-core/src/haive/core/engine/vectorstore/discovery.py:75` - error: Incompatible types in assignment (expression has type "None", variable has type "list[str]")
  - ID: 24db1563
- `packages/haive-core/src/haive/core/engine/vectorstore/discovery.py:76` - error: Incompatible types in assignment (expression has type "None", variable has type "list[str]")
  - ID: 15aa6cbe
- `packages/haive-core/src/haive/core/engine/vectorstore/discovery.py:79` - error: Incompatible types in assignment (expression has type "None", variable has type "list[str]")
  - ID: 1030b524
- `packages/haive-core/src/haive/core/engine/embedding/providers/__init__.py:237` - error: Returning Any from function declared to return "list[str]" [no-any-return]
  - ID: 1abeca1b
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:284` - error: Incompatible types in assignment (expression has type "None", variable has type "list[str]")
  - ID: af0ff50c
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:290` - error: Incompatible types in assignment (expression has type "None", variable has type "list[str]")
  - ID: 9ab67779
- `packages/haive-core/src/haive/core/utils/haive_discovery/component_info.py:59` - error: Incompatible types in assignment (expression has type "bool", target has type "Sequence[str]"
  - ID: 17b8c430
- `packages/haive-core/src/haive/core/utils/haive_discovery/component_info.py:63` - error: Incompatible types in assignment (expression has type "bool", target has type "Sequence[str]"
  - ID: 1cb8223f
- ... and 55 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:814` - error: Unsupported target for indexed assignment ("Collection[str]") [index]
  - ID: bd42589e
- `packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:816` - error: Value of type "Collection[str]" is not indexable [index]
  - ID: 6cdb6bfc
- `packages/haive-dataflow/src/haive/dataflow/mcp/health.py:420` - error: Returning Any from function declared to return "list[str]" [no-any-return]
  - ID: 42ccae28
- `packages/haive-dataflow/src/haive/dataflow/mcp/discovery.py:163` - error: Argument 1 to "\_check_npm_package_available" of "MCPDiscovery" has incompatible type "Sequenc
  - ID: 74718e9d
- `packages/haive-dataflow/src/haive/dataflow/mcp/discovery.py:208` - error: Argument 1 to "\_check_pip_package_available" of "MCPDiscovery" has incompatible type "Sequenc
  - ID: 4e8c455a
- `packages/haive-dataflow/src/haive/dataflow/mcp/client.py:484` - error: Returning Any from function declared to return "list[str]" [no-any-return]
  - ID: 76812e12
- `packages/haive-dataflow/src/haive/dataflow/serialization.py:326` - error: "Sequence[str]" has no attribute "append" [attr-defined]
  - ID: e66673b1
- `packages/haive-dataflow/src/haive/dataflow/serialization.py:329` - error: "Sequence[str]" has no attribute "append" [attr-defined]
  - ID: bf80e130
- `packages/haive-dataflow/src/haive/dataflow/registry/serialization.py:407` - error: "Sequence[str]" has no attribute "append" [attr-defined]
  - ID: 4b58469a
- `packages/haive-dataflow/src/haive/dataflow/registry/serialization.py:410` - error: "Sequence[str]" has no attribute "append" [attr-defined]
  - ID: 8e6b9611
- ... and 2 more

### haive-games

- `packages/haive-games/src/haive/games/single_player/example.py:1` - error: Incompatible default for argument "commands" (default has type "None", argument has type "lis
  - ID: 383697d6
- `packages/haive-games/src/haive/games/chess/llm_utils.py:195` - error: Returning Any from function declared to return "list[str]" [no-any-return]
  - ID: cc86a4b1
- `packages/haive-games/src/haive/games/dominoes/state_manager.py:20` - error: Incompatible default for argument "player_names" (default has type "None", argument has type
  - ID: 90d04e35
- `packages/haive-games/src/haive/games/mafia/agent.py:329` - error: Incompatible types in assignment (expression has type "list[str]", target has type "str") [a
  - ID: 5dc9754d
- `packages/haive-games/src/haive/games/connect4/ui.py:126` - error: Argument "style" to "Text" has incompatible type "Collection[str]"; expected "str | Style" [
  - ID: 7206627e
- `packages/haive-games/src/haive/games/connect4/ui.py:127` - error: Argument "style" to "Text" has incompatible type "Collection[str]"; expected "str | Style" [
  - ID: 3e3e79b9
- `packages/haive-games/src/haive/games/connect4/ui.py:130` - error: Value of type "Collection[str]" is not indexable [index]
  - ID: cbdedcc6
- `packages/haive-games/src/haive/games/connect4/ui.py:133` - error: Value of type "Collection[str]" is not indexable [index]
  - ID: 59e11d0c
- `packages/haive-games/src/haive/games/connect4/ui.py:148` - error: Argument "border_style" to "Panel" has incompatible type "Collection[str]"; expected "str | S
  - ID: b0157389
- `packages/haive-games/src/haive/games/connect4/ui.py:167` - error: Argument "border_style" to "Table" has incompatible type "Collection[str]"; expected "str | S
  - ID: a744f5f4
- ... and 13 more

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/tools/server_selector.py:333` - error: List comprehension has incompatible type List[str]; expected List[tuple[str, int]] [misc]
  - ID: 6364e79b
- `packages/haive-mcp/src/haive/mcp/tools/server_tester.py:75` - error: Incompatible types in assignment (expression has type "None", variable has type "list[str]")
  - ID: 6c8c213f
- `packages/haive-mcp/src/haive/mcp/tools/server_tester.py:76` - error: Incompatible types in assignment (expression has type "None", variable has type "list[str]")
  - ID: 83b7d75a
- `packages/haive-mcp/src/haive/mcp/downloader/legacy_core.py:861` - error: Unsupported target for indexed assignment ("Collection[str]") [index]
  - ID: a1b53b55
- `packages/haive-mcp/src/haive/mcp/downloader/core.py:782` - error: Unsupported target for indexed assignment ("Collection[str]") [index]
  - ID: 40713dca
- `packages/haive-mcp/src/haive/mcp/agents/documentation_agent.py:636` - error: Returning Any from function declared to return "list[str]" [no-any-return]
  - ID: 575f2d0a
- `packages/haive-mcp/src/haive/mcp/fastapi_mcp_server.py:256` - error: Unsupported target for indexed assignment ("Collection[str]") [index]
  - ID: ab219b0f

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/constituional_agent/utils.py:159` - error: Argument 1 to "list" has incompatible type "set[str] | None"; expected "Iterable[str]" [arg-
  - ID: 9a881fe3
- `packages/haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:132` - error: Argument 2 to "sendmail" of "SMTP" has incompatible type "str | None"; expected "str | Sequen
  - ID: 5816d63e
- `packages/haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:338` - error: Returning Any from function declared to return "list[str]" [no-any-return]
  - ID: f6731748

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/dependency_analyzer.py:77` - error: Returning Any from function declared to return "set[str]" [no-any-return]
  - ID: 92d6e1e8
- `packages/haive-tools/src/haive/tools/tools/toolkits/rps_101_toolkit.py:50` - error: Returning Any from function declared to return "list[str]" [no-any-return]
  - ID: 45e18442
- `packages/haive-tools/src/haive/tools/tools/toolkits/chuck_norris_jokes_toolkit.py:88` - error: Returning Any from function declared to return "list[str]" [no-any-return]
  - ID: 0b7415f8

## mypy:str | Any (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/multi/archive/enhanced_base.py:521` - error: Item "None" of "list[str | Any] | None" has no attribute "**iter**" (not iterable) [union-at
  - ID: c2c7b203

## mypy:str | BaseMessage (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/planning/llm_compiler/output_parser.py:129` - error: Argument 1 to "transform" of "BaseTransformOutputParser" has incompatible type "list[str | Ba
  - ID: cb934499

## mypy:str | None, str | None (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_v2/kg_memory_agent.py:159` - error: Argument "auth" to "driver" of "AsyncGraphDatabase" has incompatible type "tuple[str | None,
  - ID: acbeff78

## mypy:str | dict[Any, Any (63 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/supervisor/registry_supervisor.py:398` - error: Incompatible return value type (got "str | list[str | dict[Any, Any]]", expected "str | None"
  - ID: c52587ea
- `packages/haive-agents/src/haive/agents/supervisor/archive/registry_supervisor.py:398` - error: Incompatible return value type (got "str | list[str | dict[Any, Any]]", expected "str | None"
  - ID: 8b40670d
- `packages/haive-agents/src/haive/agents/reflection/message_transformer.py:215` - error: Argument 1 to "loads" has incompatible type "str | list[str | dict[Any, Any]]"; expected "str
  - ID: a2619c4d
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/v2/state.py:91` - error: Incompatible return value type (got "str | list[str | dict[Any, Any]]", expected "str") [ret
  - ID: 700cba06
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/v2/state.py:68` - error: Incompatible return value type (got "str | list[str | dict[Any, Any]]", expected "str") [ret
  - ID: 0af761c9
- `packages/haive-agents/src/haive/agents/dynamic_supervisor/tools.py:175` - error: Argument "content" to "HumanMessage" has incompatible type "Any | str | None"; expected "str
  - ID: 904d038d
- `packages/haive-agents/src/haive/agents/discovery/dynamic_tool_selector.py:395` - error: Item "list[str | dict[Any, Any]]" of "str | list[str | dict[Any, Any]]" has no attribute "low
  - ID: ac5150e0
- `packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:319` - error: Incompatible return value type (got "str | list[str | dict[Any, Any]]", expected "str | None"
  - ID: c967be4b
- `packages/haive-agents/src/haive/agents/base/agent_structured_output_mixin.py:231` - error: Incompatible types in assignment (expression has type "str | list[str | dict[Any, Any]]", var
  - ID: 4e4db9ae
- `packages/haive-agents/src/haive/agents/simple/state.v2.py:76` - error: Incompatible return value type (got "str | list[str | dict[Any, Any]] | None", expected "str
  - ID: 295b0b3f
- ... and 12 more

### haive-core

- `packages/haive-core/src/haive/core/schema/prebuilt/structured_output_state.py:123` - error: Argument 1 to "parse" of "JsonOutputToolsParser" has incompatible type "str | list[str | dict
  - ID: 10324aa6
- `packages/haive-core/src/haive/core/schema/prebuilt/structured_output_state.py:136` - error: Argument 1 to "parse" of "PydanticOutputParser" has incompatible type "str | list[str | dict[
  - ID: 622c6bc7
- `packages/haive-core/src/haive/core/schema/compatibility/langchain_converters.py:133` - error: Argument 1 to "\_generate_id" of "MessageConverter" has incompatible type "str | list[str | di
  - ID: bff8989c
- `packages/haive-core/src/haive/core/schema/compatibility/langchain_converters.py:142` - error: Argument 1 to "\_generate_id" of "MessageConverter" has incompatible type "str | list[str | di
  - ID: ccbe1e80
- `packages/haive-core/src/haive/core/schema/compatibility/langchain_converters.py:309` - error: Argument "page_content" to "Document" has incompatible type "str | list[str | dict[Any, Any]]
  - ID: 50c6511a
- `packages/haive-core/src/haive/core/engine/aug_llm/config.py:705` - error: Argument "content" to "SystemMessage" has incompatible type "str | None"; expected "str | lis
  - ID: 5dfea1da
- `packages/haive-core/src/haive/core/graph/node/parser_node_config_v2.py:568` - error: Dict entry 0 has incompatible type "Any": "Any | str | list[str | dict[Any, Any]] | None"; ex
  - ID: d521c880
- `packages/haive-core/src/haive/core/graph/node/output_parsing_v2.py:214` - error: Incompatible return value type (got "str | list[str | dict[Any, Any]]", expected "str | None"
  - ID: 9d9395e0
- `packages/haive-core/src/haive/core/graph/node/output_parsing.py:130` - error: Incompatible return value type (got "str | list[str | dict[Any, Any]]", expected "str | None"
  - ID: 5bbcc796
- `packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:239` - error: Unsupported target for indexed assignment ("str | list[str | dict[Any, Any]]") [index]
  - ID: 7ceea6ed
- ... and 23 more

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:222` - error: Unsupported operand types for + ("str" and "list[str | dict[Any, Any]]") [operator]
  - ID: 34912061
- `packages/haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:222` - error: Unsupported operand types for + ("str" and "list[str | dict[Any, Any]]") [operator]
  - ID: 34912061
- `packages/haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:332` - note: def **add**(self, list[str | dict[Any, Any]], /) -> list[str | dict[Any, Any]]
  - ID: 2af079e2
- `packages/haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py:332` - note: def **add**(self, list[str | dict[Any, Any]], /) -> list[str | dict[Any, Any]]
  - ID: 2af079e2
- `packages/haive-prebuilt/src/haive/prebuilt/essay_grading/nodes.py:30` - error: Argument 1 to "extract_score" has incompatible type "str | list[str | dict[Any, Any]]"; expec
  - ID: 1dca8f10
- `packages/haive-prebuilt/src/haive/prebuilt/essay_grading/nodes.py:47` - error: Argument 1 to "extract_score" has incompatible type "str | list[str | dict[Any, Any]]"; expec
  - ID: 1100a29b
- `packages/haive-prebuilt/src/haive/prebuilt/essay_grading/nodes.py:64` - error: Argument 1 to "extract_score" has incompatible type "str | list[str | dict[Any, Any]]"; expec
  - ID: 430bf1fd
- `packages/haive-prebuilt/src/haive/prebuilt/essay_grading/nodes.py:81` - error: Argument 1 to "extract_score" has incompatible type "str | list[str | dict[Any, Any]]"; expec
  - ID: 63a040df

## mypy:str, Agent? (2 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_generic.py:334` - error: Type argument "ReportTeamAgents" of "MultiAgent" must be a subtype of "dict[str, Agent?] | li
  - ID: 2421a67a
- `packages/haive-agents/src/haive/agents/multi/archive/enhanced_multi_agent_generic.py:345` - error: Type argument "ReportTeamAgents" of "MultiAgent" must be a subtype of "dict[str, Agent?] | li
  - ID: 4676943e

## mypy:str, AnalysisResult (17 errors)

### haive-core

- `packages/haive-core/src/haive/core/utils/debugkit/analysis/static.py:1010` - error: Item "dict[str, AnalysisResult]" of "AnalysisResult | dict[str, AnalysisResult]" has no attri
  - ID: cd2f92ec
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/static.py:1016` - error: Item "dict[str, AnalysisResult]" of "AnalysisResult | dict[str, AnalysisResult]" has no attri
  - ID: dc42b673
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/static.py:1018` - error: Item "dict[str, AnalysisResult]" of "AnalysisResult | dict[str, AnalysisResult]" has no attri
  - ID: 8a6786e1
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/static.py:1019` - error: Item "dict[str, AnalysisResult]" of "AnalysisResult | dict[str, AnalysisResult]" has no attri
  - ID: 77ce41a6
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/static.py:1021` - error: Item "dict[str, AnalysisResult]" of "AnalysisResult | dict[str, AnalysisResult]" has no attri
  - ID: d2657153
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/static.py:1023` - error: Item "dict[str, AnalysisResult]" of "AnalysisResult | dict[str, AnalysisResult]" has no attri
  - ID: 89751713
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/static.py:1037` - error: Item "dict[str, AnalysisResult]" of "AnalysisResult | dict[str, AnalysisResult]" has no attri
  - ID: d7c7cc18
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/static.py:1039` - error: Item "dict[str, AnalysisResult]" of "AnalysisResult | dict[str, AnalysisResult]" has no attri
  - ID: 0e3f6b20
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/static.py:1043` - error: Item "dict[str, AnalysisResult]" of "AnalysisResult | dict[str, AnalysisResult]" has no attri
  - ID: 536faf18
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/static.py:1054` - error: Item "AnalysisResult" of "AnalysisResult | dict[str, AnalysisResult]" has no attribute "value
  - ID: e851ce65
- ... and 7 more

## mypy:str, Any (583 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/rag/multi_agent_rag/specialized_workflows_v2.py:96` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 28ec0cab
- `packages/haive-agents/src/haive/agents/rag/multi_agent_rag/specialized_workflows_v2.py:183` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 6e9452e8
- `packages/haive-agents/src/haive/agents/rag/multi_agent_rag/specialized_workflows_v2.py:289` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 4183c9c2
- `packages/haive-agents/src/haive/agents/rag/multi_agent_rag/specialized_workflows_v2.py:376` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 9138e71b
- `packages/haive-agents/src/haive/agents/rag/multi_agent_rag/graded_rag_workflows_v2.py:124` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 7fe3de7d
- `packages/haive-agents/src/haive/agents/rag/multi_agent_rag/graded_rag_workflows_v2.py:190` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: c0724b52
- `packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/example.py:85` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 8fc67601
- `packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/example.py:129` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 4dbfb1d7
- `packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/example.py:162` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 402e8de3
- `packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/example.py:215` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 28f5b162
- ... and 197 more

### haive-core

- `packages/haive-core/src/haive/core/graph/node/composer/update_functions.py:102` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 4d450693
- `packages/haive-core/src/haive/core/engine/document/loaders/sources/local/pdf.py:94` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 32e673bd
- `packages/haive-core/src/haive/core/engine/document/loaders/sources/local/pdf.py:156` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 898c5aae
- `packages/haive-core/src/haive/core/schema/compatibility/field_mapping.py:144` - error: Incompatible types in assignment (expression has type "Any | None", variable has type "dict[s
  - ID: 0d6d0aac
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:231` - error: Incompatible types in assignment (expression has type "None", variable has type "dict[str, An
  - ID: 2645e63f
- `packages/haive-core/src/haive/core/models/metadata_mixin.py:193` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: fdc3da41
- `packages/haive-core/src/haive/core/graph/state_graph/components/node_manager.py:439` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 9a99b5d9
- `packages/haive-core/src/haive/core/graph/state_graph/components/edge_manager.py:414` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: daa00feb
- `packages/haive-core/src/haive/core/engine/document/loaders/cache_manager.py:87` - error: Returning Any from function declared to return "dict[str, Any] | None" [no-any-return]
  - ID: c8a358ae
- `packages/haive-core/src/haive/core/engine/agent/persistence/factory.py:100` - error: Returning Any from function declared to return "dict[str, Any] | None" [no-any-return]
  - ID: 5325cced
- ... and 179 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/core.py:1251` - error: Returning Any from function declared to return "dict[str, Any] | None" [no-any-return]
  - ID: a1c80710
- `packages/haive-dataflow/src/haive/dataflow/core.py:1265` - error: Returning Any from function declared to return "dict[str, Any] | None" [no-any-return]
  - ID: 695d8814
- `packages/haive-dataflow/src/haive/dataflow/utils/logging.py:178` - error: Incompatible types in assignment (expression has type "dict[str, Any]", target has type "str"
  - ID: 939a1550
- `packages/haive-dataflow/src/haive/dataflow/registry/utils/logging.py:178` - error: Incompatible types in assignment (expression has type "dict[str, Any]", target has type "str"
  - ID: fbd4e16d
- `packages/haive-dataflow/src/haive/dataflow/registry/importers/litellm_importer.py:148` - error: Returning Any from function declared to return "dict[str, Any] | None" [no-any-return]
  - ID: 713c01f6
- `packages/haive-dataflow/src/haive/dataflow/registry/importers/litellm_importer.py:193` - error: Returning Any from function declared to return "dict[str, Any] | None" [no-any-return]
  - ID: 712385f2
- `packages/haive-dataflow/src/haive/dataflow/importers/litellm_importer.py:105` - error: Returning Any from function declared to return "dict[str, Any] | None" [no-any-return]
  - ID: 34c75952
- `packages/haive-dataflow/src/haive/dataflow/importers/litellm_importer.py:150` - error: Returning Any from function declared to return "dict[str, Any] | None" [no-any-return]
  - ID: 26ee3614
- `packages/haive-dataflow/src/haive/dataflow/serialization.py:341` - error: Incompatible types in assignment (expression has type "dict[str, Any]", target has type "Sequ
  - ID: 6d35cb6d
- `packages/haive-dataflow/src/haive/dataflow/serialization.py:362` - error: Incompatible return value type (got "dict[str, Any]", expected "type[BaseModel] | None") [re
  - ID: ec12be77
- ... and 21 more

### haive-games

- `packages/haive-games/src/haive/games/debate/state_manager.py:327` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 7a27f229
- `packages/haive-games/src/haive/games/clue/agent.py:264` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 1a2bef85
- `packages/haive-games/src/haive/games/clue/agent.py:475` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: b4607fb3
- `packages/haive-games/src/haive/games/clue/agent.py:476` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: d6a85c53
- `packages/haive-games/src/haive/games/mafia/agent.py:1271` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 482ffb37
- `packages/haive-games/src/haive/games/mafia/agent.py:1273` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: b1b0e41e
- `packages/haive-games/src/haive/games/tic_tac_toe/ui.py:407` - error: Incompatible return value type (got "Any | None", expected "dict[str, Any]") [return-value]
  - ID: c617bddd
- `packages/haive-games/src/haive/games/hold_em/ui.py:84` - error: Item "dict[str, Any]" of "dict[str, Any] | Any" has no attribute "current_phase" [union-attr
  - ID: 4d7b37ae
- `packages/haive-games/src/haive/games/hold_em/ui.py:85` - error: Item "dict[str, Any]" of "dict[str, Any] | Any" has no attribute "hand_number" [union-attr]
  - ID: e56d6fb9
- `packages/haive-games/src/haive/games/hold_em/ui.py:160` - error: "dict[str, Any]" has no attribute "dealer_position" [attr-defined]
  - ID: a407ee4f
- ... and 117 more

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/fastmcp_runner.py:43` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 963b450a
- `packages/haive-mcp/src/haive/mcp/fastmcp_runner.py:323` - error: Incompatible types in assignment (expression has type "dict[str, Any]", variable has type "li
  - ID: a80f8810
- `packages/haive-mcp/src/haive/mcp/enhance_mcp_data.py:90` - error: Returning Any from function declared to return "dict[str, Any] | None" [no-any-return]
  - ID: 2e3a916c
- `packages/haive-mcp/src/haive/mcp/downloader/legacy_core.py:755` - error: Item "BaseException" of "dict[str, Any] | BaseException" has no attribute "get" [union-attr]
  - ID: 0b7e9d7a
- `packages/haive-mcp/src/haive/mcp/downloader/legacy_core.py:761` - error: Item "BaseException" of "dict[str, Any] | BaseException" has no attribute "get" [union-attr]
  - ID: a74286c8
- `packages/haive-mcp/src/haive/mcp/downloader/legacy_core.py:898` - error: Incompatible types in assignment (expression has type "ServerConfig", variable has type "dict
  - ID: 59b4f820
- `packages/haive-mcp/src/haive/mcp/downloader/legacy_core.py:899` - error: "dict[str, Any]" has no attribute "name" [attr-defined]
  - ID: e70fd91b
- `packages/haive-mcp/src/haive/mcp/downloader/legacy_core.py:900` - error: Argument 1 to "append" of "list" has incompatible type "dict[str, Any]"; expected "ServerConf
  - ID: e6a6d9d8
- `packages/haive-mcp/src/haive/mcp/downloader/core.py:542` - error: Incompatible types in assignment (expression has type "DownloadResult", variable has type "di
  - ID: 94074eaf
- `packages/haive-mcp/src/haive/mcp/downloader/core.py:554` - error: Item "dict[str, Any]" of "dict[str, Any] | BaseException" has no attribute "success_rate" [u
  - ID: 9930be04
- ... and 8 more

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/project_creation/github.py:175` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: af0f46c0
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/project_creation/github.py:224` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 75a986f1
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/project_creation/github.py:253` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 24825a08
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/project_creation/github.py:289` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 66e80517
- `packages/haive-tools/src/haive/tools/tools/fruityvice_tool.py:57` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 16ff6be2
- `packages/haive-tools/src/haive/tools/tools/toolkits/rick_and_morty_toolkit.py:75` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 8380ad62
- `packages/haive-tools/src/haive/tools/tools/toolkits/rick_and_morty_toolkit.py:137` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 6778bdfe
- `packages/haive-tools/src/haive/tools/tools/toolkits/rick_and_morty_toolkit.py:210` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: 4488097d
- `packages/haive-tools/src/haive/tools/tools/toolkits/rick_and_morty_toolkit.py:262` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: dbff7eaa
- `packages/haive-tools/src/haive/tools/tools/toolkits/fred_toolkit.py:66` - error: Returning Any from function declared to return "dict[str, Any]" [no-any-return]
  - ID: e98d4c41
- ... and 1 more

## mypy:str, Callable[..., Any (28 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/base/agent.py:348` - note: def create_model(str, /, \*, **config**: ConfigDict | None = ..., **doc**: str | None = ...
  - ID: a1e36670
- `packages/haive-agents/src/haive/agents/research/person/agent.py:408` - note: def create_model(str, /, \*, **config**: ConfigDict | None = ..., **doc**: str | None = ...
  - ID: 564d3c71
- `packages/haive-agents/src/haive/agents/multi/archive/enhanced_base.py:517` - error: Item "None" of "dict[str, Callable[..., Any]] | None" has no attribute "items" [union-attr]
  - ID: 06cdd86e

### haive-core

- `packages/haive-core/src/haive/core/utils/haive_discovery/base_analyzer.py:159` - note: def create_model(str, /, \*, **config**: ConfigDict | None = ..., **doc**: str | None = ...
  - ID: f023cc2d
- `packages/haive-core/src/haive/core/schema/utils.py:306` - note: def create_model(str, /, \*, **config**: ConfigDict | None = ..., **doc**: str | None = ...
  - ID: 624ab847
- `packages/haive-core/src/haive/core/schema/utils.py:363` - note: def create_model(str, /, \*, **config**: ConfigDict | None = ..., **doc**: str | None = ...
  - ID: 09b7c4d1
- `packages/haive-core/src/haive/core/schema/schema_manager.py:915` - note: def create_model(str, /, \*, **config**: ConfigDict | None = ..., **doc**: str | None = ...
  - ID: f501a104
- `packages/haive-core/src/haive/core/schema/multi_agent_state_schema.py:111` - note: def create_model(str, /, \*, **config**: ConfigDict | None = ..., **doc**: str | None = ...
  - ID: 49c904b6
- `packages/haive-core/src/haive/core/schema/composer/schema_composer.py:188` - note: def create_model(str, /, \*, **config**: ConfigDict | None = ..., **doc**: str | None = ...
  - ID: a0d8b80e
- `packages/haive-core/src/haive/core/schema/composer/_base.py:152` - note: def create_model(str, /, \*, **config**: ConfigDict | None = ..., **doc**: str | None = ...
  - ID: ea133a96
- `packages/haive-core/src/haive/core/schema/compatibility/mergers.py:395` - note: def create_model(str, /, \*, **config**: ConfigDict | None = ..., **doc**: str | None = ...
  - ID: 3c80051c
- `packages/haive-core/src/haive/core/engine/prompt_template/prompt_engine.py:294` - note: def create_model(str, /, \*, **config**: ConfigDict | None = ..., **doc**: str | None = ...
  - ID: 34b47de1
- `packages/haive-core/src/haive/core/engine/document/loaders/registry.py:275` - note: def create_model(str, /, \*, **config**: ConfigDict | None = ..., **doc**: str | None = ...
  - ID: ab28bcf0
- ... and 13 more

### haive-games

- `packages/haive-games/src/haive/games/multi_player/factory.py:69` - error: Incompatible default for argument "custom_methods" (default has type "None", argument has typ
  - ID: 92c9201f
- `packages/haive-games/src/haive/games/framework/multi_player/factory.py:69` - error: Incompatible default for argument "custom_methods" (default has type "None", argument has typ
  - ID: 5afb7cf6

## mypy:str, Callable[[BaseCursor[Any, Any (12 errors)

### haive-core

- `packages/haive-core/src/haive/core/persistence/store/postgres.py:112` - error: Argument 2 has incompatible type "\*\*dict[str, Callable[[BaseCursor[Any, Any]], RowMaker[dict[
  - ID: f4d67063
- `packages/haive-core/src/haive/core/persistence/store/postgres.py:112` - error: Argument 2 has incompatible type "\*\*dict[str, Callable[[BaseCursor[Any, Any]], RowMaker[dict[
  - ID: f4d67063
- `packages/haive-core/src/haive/core/persistence/store/postgres.py:112` - error: Argument 2 has incompatible type "\*\*dict[str, Callable[[BaseCursor[Any, Any]], RowMaker[dict[
  - ID: f4d67063
- `packages/haive-core/src/haive/core/persistence/store/postgres.py:112` - error: Argument 2 has incompatible type "\*\*dict[str, Callable[[BaseCursor[Any, Any]], RowMaker[dict[
  - ID: f4d67063
- `packages/haive-core/src/haive/core/persistence/store/postgres.py:112` - error: Argument 2 has incompatible type "\*\*dict[str, Callable[[BaseCursor[Any, Any]], RowMaker[dict[
  - ID: f4d67063
- `packages/haive-core/src/haive/core/persistence/store/postgres.py:112` - error: Argument 2 has incompatible type "\*\*dict[str, Callable[[BaseCursor[Any, Any]], RowMaker[dict[
  - ID: f4d67063
- `packages/haive-core/src/haive/core/persistence/store/postgres.py:263` - error: Argument 2 to "connect" of "AsyncConnection" has incompatible type "\*\*dict[str, Callable[[Bas
  - ID: 35b5a73f
- `packages/haive-core/src/haive/core/persistence/store/postgres.py:263` - error: Argument 2 to "connect" of "AsyncConnection" has incompatible type "\*\*dict[str, Callable[[Bas
  - ID: 35b5a73f
- `packages/haive-core/src/haive/core/persistence/store/postgres.py:263` - error: Argument 2 to "connect" of "AsyncConnection" has incompatible type "\*\*dict[str, Callable[[Bas
  - ID: 35b5a73f
- `packages/haive-core/src/haive/core/persistence/store/postgres.py:263` - error: Argument 2 to "connect" of "AsyncConnection" has incompatible type "\*\*dict[str, Callable[[Bas
  - ID: 35b5a73f
- ... and 2 more

## mypy:str, Collection[str (4 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_v2/kg_memory_agent.py:134` - error: Incompatible types in assignment (expression has type "dict[str, Collection[str]]", variable
  - ID: 8969b036
- `packages/haive-agents/src/haive/agents/memory_v2/kg_memory_agent.py:142` - error: Incompatible types in assignment (expression has type "dict[str, Collection[str]]", variable
  - ID: 2db9bcc0
- `packages/haive-agents/src/haive/agents/memory_v2/kg_memory_agent.py:186` - error: Incompatible types in assignment (expression has type "dict[str, Collection[str]]", variable
  - ID: 1b7fac6e

### haive-games

- `packages/haive-games/src/haive/games/connect4/ui.py:287` - error: Invalid index type "str | None" for "dict[str, Collection[str]]"; expected type "str" [index
  - ID: ecea82d5

## mypy:str, Coroutine[Any, Any, list[dict[str, Any (2 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_v2/standalone_rag_memory.py:628` - error: Argument 1 to "append" of "list" has incompatible type "tuple[str, Coroutine[Any, Any, list[d
  - ID: 0486c896
- `packages/haive-agents/src/haive/agents/memory_v2/rag_memory_agent.py:591` - error: Argument 1 to "append" of "list" has incompatible type "tuple[str, Coroutine[Any, Any, list[d
  - ID: dcde84d4

## mypy:str, Coroutine[Any, Any, str (2 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_v2/standalone_rag_memory.py:631` - error: Argument 1 to "append" of "list" has incompatible type "tuple[str, Coroutine[Any, Any, str]]"
  - ID: dfc6b187
- `packages/haive-agents/src/haive/agents/memory_v2/rag_memory_agent.py:594` - error: Argument 1 to "append" of "list" has incompatible type "tuple[str, Coroutine[Any, Any, str]]"
  - ID: 256d5d20

## mypy:str, SerializableModel (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/graph/state_graph/base.py:110` - error: Returning Any from function declared to return "dict[str, SerializableModel]" [no-any-return
  - ID: ce2c4c0f

## mypy:str, SimpleAgent (4 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_standalone.py:589` - error: Type argument "dict[str, SimpleAgent]" of "MultiAgent" must be a subtype of "dict[str, Agent]
  - ID: b078aef2
- `packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_standalone.py:589` - error: Type argument "dict[str, SimpleAgent]" of "MultiAgent" must be a subtype of "dict[str, Agent]
  - ID: b078aef2
- `packages/haive-agents/src/haive/agents/multi/archive/enhanced_multi_agent_standalone.py:589` - error: Type argument "dict[str, SimpleAgent]" of "MultiAgent" must be a subtype of "dict[str, Agent]
  - ID: 490646c3
- `packages/haive-agents/src/haive/agents/multi/archive/enhanced_multi_agent_standalone.py:589` - error: Type argument "dict[str, SimpleAgent]" of "MultiAgent" must be a subtype of "dict[str, Agent]
  - ID: 490646c3

## mypy:str, StoreType (5 errors)

### haive-core

- `packages/haive-core/src/haive/core/persistence/store/factory.py:160` - error: Argument 1 to "StoreConfig" has incompatible type "\*\*dict[str, StoreType]"; expected "dict[st
  - ID: 054f0a42
- `packages/haive-core/src/haive/core/persistence/store/factory.py:160` - error: Argument 1 to "StoreConfig" has incompatible type "\*\*dict[str, StoreType]"; expected "dict[st
  - ID: 054f0a42
- `packages/haive-core/src/haive/core/persistence/store/factory.py:160` - error: Argument 1 to "StoreConfig" has incompatible type "\*\*dict[str, StoreType]"; expected "dict[st
  - ID: 054f0a42
- `packages/haive-core/src/haive/core/persistence/store/factory.py:160` - error: Argument 1 to "StoreConfig" has incompatible type "\*\*dict[str, StoreType]"; expected "dict[st
  - ID: 054f0a42
- `packages/haive-core/src/haive/core/persistence/store/factory.py:160` - error: Argument 1 to "StoreConfig" has incompatible type "\*\*dict[str, StoreType]"; expected "dict[st
  - ID: 054f0a42

## mypy:str, TypeInfo (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/utils/debugkit/analysis/types.py:261` - error: Incompatible types in assignment (expression has type "None", variable has type "dict[str, Ty
  - ID: 6f673977

## mypy:str, bool (2 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/base/universal_agent.py:143` - error: Returning Any from function declared to return "dict[str, bool]" [no-any-return]
  - ID: 2279209a

### haive-core

- `packages/haive-core/src/haive/core/schema/field_utils.py:381` - error: Argument 1 to "append" of "list" has incompatible type "dict[str, bool]"; expected "Callable[
  - ID: 75412c6e

## mypy:str, datetime (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/schema/prebuilt/query_state.py:480` - error: Incompatible types in assignment (expression has type "dict[str, datetime]", target has type
  - ID: 91d092d6

## mypy:str, dict[str, Any (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/aug_llm/config.py:414` - error: Returning Any from function declared to return "tuple[str, dict[str, Any] | None]" [no-any-r
  - ID: 15e2fbee

## mypy:str, dict[str, Collection[str (2 errors)

### haive-core

- `packages/haive-core/src/haive/core/types/advanced_registry.py:174` - error: Argument 1 to "TextPipeline" has incompatible type "\*\*dict[str, dict[str, Collection[str]]]";
  - ID: 39a1b550
- `packages/haive-core/src/haive/core/types/advanced_registry.py:174` - error: Argument 1 to "TextPipeline" has incompatible type "\*\*dict[str, dict[str, Collection[str]]]";
  - ID: 39a1b550

## mypy:str, dict[str, int (2 errors)

### haive-games

- `packages/haive-games/src/haive/games/framework/base/config.py:64` - error: Incompatible types in assignment (expression has type "dict[str, dict[str, int]]", variable h
  - ID: b8e66bae
- `packages/haive-games/src/haive/games/checkers/config.py:243` - error: Incompatible types in assignment (expression has type "dict[str, dict[str, int]]", variable h
  - ID: 10b921af

## mypy:str, dict[str, int | None (1 errors)

### haive-games

- `packages/haive-games/src/haive/games/battleship/config.py:132` - error: Incompatible types in assignment (expression has type "dict[str, dict[str, int | None]]", var
  - ID: 7a161f2f

## mypy:str, dict[str, object (2 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/base/mixins/persistence_mixin.py:467` - error: Incompatible return value type (got "dict[str, dict[str, object]]", expected "RunnableConfig"
  - ID: 56e8870a

### haive-core

- `packages/haive-core/src/haive/core/engine/agent/config.py:116` - error: Incompatible types in assignment (expression has type "dict[str, dict[str, object]]", variabl
  - ID: 08b6ec7e

## mypy:str, dict[str, str (5 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/react_class/react_agent2/config2.py:82` - error: Incompatible types in assignment (expression has type "dict[str, dict[str, str]]", variable h
  - ID: 18100837
- `packages/haive-agents/src/haive/agents/planning/llm_compiler/config.py:38` - error: Incompatible types in assignment (expression has type "dict[str, dict[str, str]]", variable h
  - ID: e46fd697
- `packages/haive-agents/src/haive/agents/react_class/react_agent/agent.py:48` - error: Incompatible types in assignment (expression has type "dict[str, dict[str, str]]", variable h
  - ID: cdbc956c

### haive-core

- `packages/haive-core/src/haive/core/config/auth_runnable.py:533` - error: Incompatible return value type (got "dict[str, dict[str, str]]", expected "RunnableConfig")
  - ID: cb72fc44

### haive-games

- `packages/haive-games/src/haive/games/debate/factory.py:137` - error: Invalid index type "Any | None" for "dict[str, dict[str, str]]"; expected type "str" [index]
  - ID: 8174d189

## mypy:str, float (4 errors)

### haive-core

- `packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:130` - error: Incompatible types in assignment (expression has type "None", variable has type "dict[str, fl
  - ID: 57514d64
- `packages/haive-core/src/haive/core/models/metadata_mixin.py:130` - error: Returning Any from function declared to return "dict[str, float]" [no-any-return]
  - ID: dc2bba5a
- `packages/haive-core/src/haive/core/tools/store_manager.py:264` - error: Incompatible types in assignment (expression has type "dict[str, float]", target has type "st
  - ID: 743e7a8d

### haive-games

- `packages/haive-games/src/haive/games/debate_v2/judges.py:420` - error: Argument 1 to "list" has incompatible type "dict_values[str, float]"; expected "Iterable[Judg
  - ID: 4bef78f5

## mypy:str, int (46 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/react/dynamic_react_agent.v2.py:1048` - error: Returning Any from function declared to return "dict[str, int]" [no-any-return]
  - ID: ba58b680
- `packages/haive-agents/src/haive/agents/react/dynamic_react_agent.py:1041` - error: Returning Any from function declared to return "dict[str, int]" [no-any-return]
  - ID: c26f36e8
- `packages/haive-agents/src/haive/agents/common/utils/pydantic_prompt_utils.py:272` - error: Item "None" of "dict[str, int] | None" has no attribute "get" [union-attr]
  - ID: 5efe6573
- `packages/haive-agents/src/haive/agents/memory_v2/graph_memory_agent.py:701` - error: Incompatible types in assignment (expression has type "dict[str, int]", target has type "str"
  - ID: 37c1cf08

### haive-core

- `packages/haive-core/src/haive/core/engine/document/splitters/engine.py:417` - error: Argument 3 to "CharacterTextSplitter" has incompatible type "\*\*dict[str, int]"; expected "boo
  - ID: cdabb010
- `packages/haive-core/src/haive/core/engine/document/splitters/engine.py:425` - error: Argument 3 to "RecursiveCharacterTextSplitter" has incompatible type "\*\*dict[str, int]"; expe
  - ID: a7c01f24
- `packages/haive-core/src/haive/core/engine/document/splitters/engine.py:429` - error: Argument 1 to "TokenTextSplitter" has incompatible type "\*\*dict[str, int]"; expected "str" [
  - ID: 3da648f8
- `packages/haive-core/src/haive/core/engine/document/splitters/engine.py:429` - error: Argument 1 to "TokenTextSplitter" has incompatible type "\*\*dict[str, int]"; expected "str" [
  - ID: 3da648f8
- `packages/haive-core/src/haive/core/engine/document/splitters/engine.py:429` - error: Argument 1 to "TokenTextSplitter" has incompatible type "\*\*dict[str, int]"; expected "str" [
  - ID: 3da648f8
- `packages/haive-core/src/haive/core/engine/document/splitters/engine.py:429` - error: Argument 1 to "TokenTextSplitter" has incompatible type "\*\*dict[str, int]"; expected "str" [
  - ID: 3da648f8
- `packages/haive-core/src/haive/core/engine/document/splitters/engine.py:432` - error: Argument 1 to "NLTKTextSplitter" has incompatible type "\*\*dict[str, int]"; expected "str" [a
  - ID: 85ba7f0e
- `packages/haive-core/src/haive/core/engine/document/splitters/engine.py:432` - error: Argument 1 to "NLTKTextSplitter" has incompatible type "\*\*dict[str, int]"; expected "str" [a
  - ID: 85ba7f0e
- `packages/haive-core/src/haive/core/engine/document/splitters/engine.py:435` - error: Argument 1 to "SpacyTextSplitter" has incompatible type "\*\*dict[str, int]"; expected "str" [
  - ID: cafddac7
- `packages/haive-core/src/haive/core/engine/document/splitters/engine.py:435` - error: Argument 1 to "SpacyTextSplitter" has incompatible type "\*\*dict[str, int]"; expected "str" [
  - ID: cafddac7
- ... and 19 more

### haive-games

- `packages/haive-games/src/haive/games/checkers/example.py:265` - error: Unsupported operand types for + ("int" and "dict[str, int]") [operator]
  - ID: 5fda1b6f
- `packages/haive-games/src/haive/games/checkers/example.py:265` - error: Unsupported operand types for + ("int" and "dict[str, int]") [operator]
  - ID: 5fda1b6f
- `packages/haive-games/src/haive/games/checkers/example.py:266` - error: Unsupported left operand type for \* ("dict[str, int]") [operator]
  - ID: 7103e89a
- `packages/haive-games/src/haive/games/checkers/example.py:266` - error: Unsupported left operand type for \* ("dict[str, int]") [operator]
  - ID: 7103e89a
- `packages/haive-games/src/haive/games/checkers/example.py:266` - error: Unsupported left operand type for \* ("dict[str, int]") [operator]
  - ID: 7103e89a
- `packages/haive-games/src/haive/games/checkers/example.py:266` - error: Unsupported left operand type for \* ("dict[str, int]") [operator]
  - ID: 7103e89a
- `packages/haive-games/src/haive/games/checkers/example.py:266` - error: Unsupported left operand type for \* ("dict[str, int]") [operator]
  - ID: 7103e89a
- `packages/haive-games/src/haive/games/checkers/example.py:270` - error: Value of type "dict[str, int] | float | int" is not indexable [index]
  - ID: 3dc2e579
- `packages/haive-games/src/haive/games/checkers/example.py:271` - error: Unsupported operand types for + ("int" and "dict[str, int]") [operator]
  - ID: 21e1698c
- `packages/haive-games/src/haive/games/checkers/example.py:271` - error: Unsupported operand types for + ("int" and "dict[str, int]") [operator]
  - ID: 21e1698c
- ... and 3 more

## mypy:str, int | list[dict[str, object (6 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/retriever/providers/CohereRagRetrieverConfig.py:211` - error: Argument 2 to "CohereRagRetriever" has incompatible type "\*\*dict[str, int | list[dict[str, ob
  - ID: f98b782b
- `packages/haive-core/src/haive/core/engine/retriever/providers/CohereRagRetrieverConfig.py:211` - error: Argument 2 to "CohereRagRetriever" has incompatible type "\*\*dict[str, int | list[dict[str, ob
  - ID: f98b782b
- `packages/haive-core/src/haive/core/engine/retriever/providers/CohereRagRetrieverConfig.py:211` - error: Argument 2 to "CohereRagRetriever" has incompatible type "\*\*dict[str, int | list[dict[str, ob
  - ID: f98b782b
- `packages/haive-core/src/haive/core/engine/retriever/providers/CohereRagRetrieverConfig.py:211` - error: Argument 2 to "CohereRagRetriever" has incompatible type "\*\*dict[str, int | list[dict[str, ob
  - ID: f98b782b
- `packages/haive-core/src/haive/core/engine/retriever/providers/CohereRagRetrieverConfig.py:211` - error: Argument 2 to "CohereRagRetriever" has incompatible type "\*\*dict[str, int | list[dict[str, ob
  - ID: f98b782b
- `packages/haive-core/src/haive/core/engine/retriever/providers/CohereRagRetrieverConfig.py:211` - error: Argument 2 to "CohereRagRetriever" has incompatible type "\*\*dict[str, int | list[dict[str, ob
  - ID: f98b782b

## mypy:str, int | list[str (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/config.py:175` - error: Argument 2 to "from_uri" of "SQLDatabase" has incompatible type "\*\*dict[str, int | list[str]
  - ID: 344329ec

## mypy:str, list[Any (6 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/base/agent.py:859` - error: Unsupported target for indexed assignment ("int | dict[str, list[Any] | Any | None] | dict[st
  - ID: 680b02c5
- `packages/haive-agents/src/haive/agents/base/agent.py:863` - error: Unsupported target for indexed assignment ("int | dict[str, list[Any] | Any | None] | dict[st
  - ID: 3787bfda
- `packages/haive-agents/src/haive/agents/base/agent.py:864` - error: Unsupported target for indexed assignment ("int | dict[str, list[Any] | Any | None] | dict[st
  - ID: d266e6a6
- `packages/haive-agents/src/haive/agents/base/agent.py:866` - error: Unsupported target for indexed assignment ("int | dict[str, list[Any] | Any | None] | dict[st
  - ID: 8ab518c8
- `packages/haive-agents/src/haive/agents/base/agent.py:870` - error: Unsupported target for indexed assignment ("int | dict[str, list[Any] | Any | None] | dict[st
  - ID: 3c11b0d9
- `packages/haive-agents/src/haive/agents/base/agent.py:872` - error: Unsupported target for indexed assignment ("int | dict[str, list[Any] | Any | None] | dict[st
  - ID: 86ccc905

## mypy:str, list[BaseTool | Tool | StructuredTool (4 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/tool/base.py:101` - error: Argument 1 to "ToolNode" has incompatible type "\*\*dict[str, list[BaseTool | Tool | Structured
  - ID: 975696fc
- `packages/haive-core/src/haive/core/engine/tool/base.py:101` - error: Argument 1 to "ToolNode" has incompatible type "\*\*dict[str, list[BaseTool | Tool | Structured
  - ID: 975696fc
- `packages/haive-core/src/haive/core/engine/tool/base.py:101` - error: Argument 1 to "ToolNode" has incompatible type "\*\*dict[str, list[BaseTool | Tool | Structured
  - ID: 975696fc
- `packages/haive-core/src/haive/core/engine/tool/base.py:101` - error: Argument 1 to "ToolNode" has incompatible type "\*\*dict[str, list[BaseTool | Tool | Structured
  - ID: 975696fc

## mypy:str, list[str (23 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_reorganized/base/memory_models_standalone.py:337` - error: Argument 1 to "EnhancedMemoryItem" has incompatible type "\*\*dict[str, list[str] | str | None]
  - ID: 324f44cc
- `packages/haive-agents/src/haive/agents/memory_reorganized/base/memory_models_standalone.py:337` - error: Argument 1 to "EnhancedMemoryItem" has incompatible type "\*\*dict[str, list[str] | str | None]
  - ID: 324f44cc
- `packages/haive-agents/src/haive/agents/memory_reorganized/base/memory_models_standalone.py:337` - error: Argument 1 to "EnhancedMemoryItem" has incompatible type "\*\*dict[str, list[str] | str | None]
  - ID: 324f44cc
- `packages/haive-agents/src/haive/agents/memory_reorganized/base/memory_models_standalone.py:337` - error: Argument 1 to "EnhancedMemoryItem" has incompatible type "\*\*dict[str, list[str] | str | None]
  - ID: 324f44cc
- `packages/haive-agents/src/haive/agents/memory_reorganized/base/memory_models_standalone.py:337` - error: Argument 1 to "EnhancedMemoryItem" has incompatible type "\*\*dict[str, list[str] | str | None]
  - ID: 324f44cc
- `packages/haive-agents/src/haive/agents/memory_reorganized/base/memory_models_standalone.py:337` - error: Argument 1 to "EnhancedMemoryItem" has incompatible type "\*\*dict[str, list[str] | str | None]
  - ID: 324f44cc
- `packages/haive-agents/src/haive/agents/memory_reorganized/base/memory_models_standalone.py:337` - error: Argument 1 to "EnhancedMemoryItem" has incompatible type "\*\*dict[str, list[str] | str | None]
  - ID: 324f44cc
- `packages/haive-agents/src/haive/agents/memory_reorganized/base/memory_models_standalone.py:337` - error: Argument 1 to "EnhancedMemoryItem" has incompatible type "\*\*dict[str, list[str] | str | None]
  - ID: 324f44cc
- `packages/haive-agents/src/haive/agents/memory_reorganized/base/memory_models_standalone.py:337` - error: Argument 1 to "EnhancedMemoryItem" has incompatible type "\*\*dict[str, list[str] | str | None]
  - ID: 324f44cc
- `packages/haive-agents/src/haive/agents/memory_reorganized/base/memory_models_standalone.py:337` - error: Argument 1 to "EnhancedMemoryItem" has incompatible type "\*\*dict[str, list[str] | str | None]
  - ID: 324f44cc
- ... and 12 more

### haive-core

- `packages/haive-core/src/haive/core/tools/store_manager.py:266` - error: Incompatible types in assignment (expression has type "dict[str, list[str]]", target has type
  - ID: 1abc8a36

## mypy:str, object (91 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_v2/kg_memory_agent.py:165` - error: Incompatible types in assignment (expression has type "dict[str, object]", variable has type
  - ID: 4e9c09ba
- `packages/haive-agents/src/haive/agents/planning/rewoo_tree_agent.py:515` - error: Argument 1 to "\_format_final_response" of "ReWOOTreeAgent" has incompatible type "dict[str, o
  - ID: d5a06cb7
- `packages/haive-agents/src/haive/agents/memory_v2/simple_memory_agent.py:767` - error: Incompatible types in assignment (expression has type "dict[str, object]", target has type "s
  - ID: 6f11d57d
- `packages/haive-agents/src/haive/agents/memory_v2/simple_memory_agent.py:786` - error: Incompatible types in assignment (expression has type "dict[str, object]", target has type "s
  - ID: 9c3b57d5
- `packages/haive-agents/src/haive/agents/memory_reorganized/agents/simple.py:756` - error: Incompatible types in assignment (expression has type "dict[str, object]", target has type "s
  - ID: b0f27c66
- `packages/haive-agents/src/haive/agents/memory_reorganized/agents/simple.py:775` - error: Incompatible types in assignment (expression has type "dict[str, object]", target has type "s
  - ID: 8cfe0089
- `packages/haive-agents/src/haive/agents/research/open_perplexity/structured_tools.py:380` - error: Incompatible return value type (got "dict[str, object]", expected "list[dict[str, Any]]") [r
  - ID: 3fc292d8

### haive-core

- `packages/haive-core/src/haive/core/utils/debugkit/benchmarking/timing.py:102` - error: Incompatible return value type (got "dict[str, object]", expected "dict[str, float]") [retur
  - ID: 35a2b35d
- `packages/haive-core/src/haive/core/engine/vectorstore/providers/RedisVectorStoreConfig.py:232` - error: Argument 1 to "Redis" has incompatible type "\*\*dict[str, object]"; expected "str" [arg-type]
  - ID: 8b9679cf
- `packages/haive-core/src/haive/core/engine/vectorstore/providers/RedisVectorStoreConfig.py:232` - error: Argument 1 to "Redis" has incompatible type "\*\*dict[str, object]"; expected "str" [arg-type]
  - ID: 8b9679cf
- `packages/haive-core/src/haive/core/engine/vectorstore/providers/RedisVectorStoreConfig.py:232` - error: Argument 1 to "Redis" has incompatible type "\*\*dict[str, object]"; expected "str" [arg-type]
  - ID: 8b9679cf
- `packages/haive-core/src/haive/core/engine/vectorstore/providers/RedisVectorStoreConfig.py:232` - error: Argument 1 to "Redis" has incompatible type "\*\*dict[str, object]"; expected "str" [arg-type]
  - ID: 8b9679cf
- `packages/haive-core/src/haive/core/engine/vectorstore/providers/RedisVectorStoreConfig.py:232` - error: Argument 1 to "Redis" has incompatible type "\*\*dict[str, object]"; expected "str" [arg-type]
  - ID: 8b9679cf
- `packages/haive-core/src/haive/core/engine/vectorstore/providers/RedisVectorStoreConfig.py:232` - error: Argument 1 to "Redis" has incompatible type "\*\*dict[str, object]"; expected "str" [arg-type]
  - ID: 8b9679cf
- `packages/haive-core/src/haive/core/engine/vectorstore/providers/RedisVectorStoreConfig.py:232` - error: Argument 1 to "Redis" has incompatible type "\*\*dict[str, object]"; expected "str" [arg-type]
  - ID: 8b9679cf
- `packages/haive-core/src/haive/core/engine/vectorstore/providers/RedisVectorStoreConfig.py:232` - error: Argument 1 to "Redis" has incompatible type "\*\*dict[str, object]"; expected "str" [arg-type]
  - ID: 8b9679cf
- `packages/haive-core/src/haive/core/engine/vectorstore/providers/RedisVectorStoreConfig.py:232` - error: Argument 1 to "Redis" has incompatible type "\*\*dict[str, object]"; expected "str" [arg-type]
  - ID: 8b9679cf
- ... and 71 more

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/systemic_review_of_scientific_articles/tools.py:52` - error: Argument "params" to "get" has incompatible type "dict[str, object]"; expected "SupportsItems
  - ID: 072962f8

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/openlibrary_toolkit.py:62` - error: Argument "params" to "get" has incompatible type "dict[str, object]"; expected "SupportsItems
  - ID: aeb28a3d
- `packages/haive-tools/src/haive/tools/tools/toolkits/lcbo_toolkit.py:95` - error: Argument "params" to "get" has incompatible type "dict[str, object]"; expected "SupportsItems
  - ID: f697669c

## mypy:str, set[str (2 errors)

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/import_analyzer.py:58` - error: Invalid index type "BaseExpression | str" for "dict[str, set[str]]"; expected type "str" [in
  - ID: d5a8c32e
- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/import_analyzer.py:77` - error: Invalid index type "BaseExpression | str | Any" for "dict[str, set[str]]"; expected type "str
  - ID: fa38e8bb

## mypy:str, str (78 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/research/open_perplexity/agent.py:176` - error: Incompatible return value type (got "dict[str, str]", expected "Command[Any]") [return-value
  - ID: 3adf6d19
- `packages/haive-agents/src/haive/agents/research/open_perplexity/agent.py:202` - error: Incompatible return value type (got "dict[str, str]", expected "Command[Any]") [return-value
  - ID: b5e46888
- `packages/haive-agents/src/haive/agents/research/open_perplexity/agent.py:241` - error: Incompatible return value type (got "dict[str, str]", expected "Command[Any]") [return-value
  - ID: f9b0a747
- `packages/haive-agents/src/haive/agents/research/open_perplexity/agent.py:250` - error: Incompatible return value type (got "dict[str, str]", expected "Command[Any]") [return-value
  - ID: 31dd2802
- `packages/haive-agents/src/haive/agents/research/open_perplexity/agent.py:284` - error: Incompatible return value type (got "dict[str, str]", expected "Command[Any]") [return-value
  - ID: 4e442794
- `packages/haive-agents/src/haive/agents/research/open_perplexity/agent.py:328` - error: Incompatible return value type (got "dict[str, str]", expected "Command[Any]") [return-value
  - ID: 3c6b4070
- `packages/haive-agents/src/haive/agents/research/open_perplexity/agent.py:333` - error: Incompatible return value type (got "dict[str, str]", expected "Command[Any]") [return-value
  - ID: 7c9c9b81
- `packages/haive-agents/src/haive/agents/research/open_perplexity/agent.py:414` - error: Incompatible return value type (got "dict[str, str]", expected "Command[Any]") [return-value
  - ID: 02dc0a55
- `packages/haive-agents/src/haive/agents/research/open_perplexity/agent.py:477` - error: Incompatible return value type (got "dict[str, str]", expected "Command[Any]") [return-value
  - ID: 3f03e654
- `packages/haive-agents/src/haive/agents/research/open_perplexity/agent.py:486` - error: Incompatible return value type (got "dict[str, str]", expected "Command[Any]") [return-value
  - ID: c9de8836
- ... and 9 more

### haive-core

- `packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:283` - error: Incompatible types in assignment (expression has type "None", variable has type "dict[str, st
  - ID: 77880f93
- `packages/haive-core/src/haive/core/utils/haive_discovery/haive_discovery.py:209` - error: Returning Any from function declared to return "dict[str, str]" [no-any-return]
  - ID: 7d61d8a9
- `packages/haive-core/src/haive/core/utils/haive_discovery/component_info.py:48` - error: Incompatible types in assignment (expression has type "dict[str, str]", target has type "Sequ
  - ID: 8a433d30
- `packages/haive-core/src/haive/core/utils/haive_discovery/component_info.py:55` - error: Incompatible types in assignment (expression has type "dict[str, str]", target has type "Sequ
  - ID: 2792bc59
- `packages/haive-core/src/haive/core/utils/haive_discovery/component_info.py:71` - error: Incompatible types in assignment (expression has type "dict[str, str]", target has type "Sequ
  - ID: 9e994868
- `packages/haive-core/src/haive/core/engine/document/loaders/sources/additional_sources.py:954` - error: Incompatible types in assignment (expression has type "dict[str, str] | None", base class "Ba
  - ID: 0df91216
- `packages/haive-core/src/haive/core/engine/retriever/providers/WeaviateHybridSearchRetrieverConfig.py:194` - error: Incompatible types in assignment (expression has type "dict[str, str]", target has type "tupl
  - ID: f9d27aa2
- `packages/haive-core/src/haive/core/engine/aug_llm/factory.py:469` - error: Argument 1 to "append" of "list" has incompatible type "dict[str, str]"; expected "type[BaseM
  - ID: 6911ef89
- `packages/haive-core/src/haive/core/engine/aug_llm/factory.py:476` - error: Argument 1 to "append" of "list" has incompatible type "tuple[str, str]"; expected "tuple[typ
  - ID: ea9f2ea6
- `packages/haive-core/src/haive/core/graph/node/validation_node_v2.py:119` - error: Returning Any from function declared to return "dict[str, str]" [no-any-return]
  - ID: 48b77759
- ... and 43 more

### haive-games

- `packages/haive-games/src/haive/games/clue/models.py:656` - error: Incompatible types in assignment (expression has type "dict[str, str]", target has type "bool
  - ID: 65825257
- `packages/haive-games/src/haive/games/chess/configurable_engines.py:223` - error: Incompatible default for argument "providers" (default has type "None", argument has type "di
  - ID: f30a4ee4

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/installers/config_manager.py:287` - error: Incompatible types in assignment (expression has type "dict[str, str]", target has type "list
  - ID: 67deeb30
- `packages/haive-mcp/src/haive/mcp/agents/mcp_agent.py:399` - error: Dict entry 3 has incompatible type "str": "dict[str, str]"; expected "str": "Sequence[str]"
  - ID: 15c04e3c

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/prompts.py:486` - error: Argument 1 to "append" of "list" has incompatible type "MessagesPlaceholder"; expected "tuple
  - ID: 8a7ed152
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/prompts.py:506` - error: Argument 1 to "append" of "list" has incompatible type "MessagesPlaceholder"; expected "tuple
  - ID: dbc954be

## mypy:str, str | Any (4 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/multi/experiments/routing_patterns.py:134` - error: Argument 3 to "add_route" of "RoutingMultiAgent" has incompatible type "dict[str, str | Any]"
  - ID: 90409446
- `packages/haive-agents/src/haive/agents/multi/archive/experiments/routing_patterns.py:134` - error: Argument 3 to "add_route" of "RoutingMultiAgent" has incompatible type "dict[str, str | Any]"
  - ID: f4642cff

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/weather.py:194` - error: Argument 1 to "WeatherData" has incompatible type "\*\*dict[str, str | Any]"; expected "float |
  - ID: 402a461e
- `packages/haive-tools/src/haive/tools/tools/toolkits/weather.py:194` - error: Argument 1 to "WeatherData" has incompatible type "\*\*dict[str, str | Any]"; expected "float |
  - ID: 402a461e

## mypy:str, str | float | None (7 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/retriever/providers/QdrantSparseVectorRetrieverConfig.py:192` - error: Argument 1 to "QdrantClient" has incompatible type "\*\*dict[str, str | float | None]"; expecte
  - ID: 4c4cbf99
- `packages/haive-core/src/haive/core/engine/retriever/providers/QdrantSparseVectorRetrieverConfig.py:192` - error: Argument 1 to "QdrantClient" has incompatible type "\*\*dict[str, str | float | None]"; expecte
  - ID: 4c4cbf99
- `packages/haive-core/src/haive/core/engine/retriever/providers/QdrantSparseVectorRetrieverConfig.py:192` - error: Argument 1 to "QdrantClient" has incompatible type "\*\*dict[str, str | float | None]"; expecte
  - ID: 4c4cbf99
- `packages/haive-core/src/haive/core/engine/retriever/providers/QdrantSparseVectorRetrieverConfig.py:192` - error: Argument 1 to "QdrantClient" has incompatible type "\*\*dict[str, str | float | None]"; expecte
  - ID: 4c4cbf99
- `packages/haive-core/src/haive/core/engine/retriever/providers/QdrantSparseVectorRetrieverConfig.py:192` - error: Argument 1 to "QdrantClient" has incompatible type "\*\*dict[str, str | float | None]"; expecte
  - ID: 4c4cbf99
- `packages/haive-core/src/haive/core/engine/retriever/providers/QdrantSparseVectorRetrieverConfig.py:192` - error: Argument 1 to "QdrantClient" has incompatible type "\*\*dict[str, str | float | None]"; expecte
  - ID: 4c4cbf99
- `packages/haive-core/src/haive/core/engine/retriever/providers/QdrantSparseVectorRetrieverConfig.py:192` - error: Argument 1 to "QdrantClient" has incompatible type "\*\*dict[str, str | float | None]"; expecte
  - ID: 4c4cbf99

## mypy:str, str | list[str | dict[Any, Any (2 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/engines.py:30` - error: List item 0 has incompatible type "tuple[str, str | list[str | dict[Any, Any]]]"; expected "B
  - ID: 590b0ccc
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/engines.py:54` - error: List item 0 has incompatible type "tuple[str, str | list[str | dict[Any, Any]]]"; expected "B
  - ID: 327b77fe

## mypy:str, tuple[<typing special form>, None (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/embeddings.py:220` - error: Incompatible return value type (got "dict[str, tuple[<typing special form>, None]]", expected
  - ID: 4681e38f

## mypy:str, tuple[Any, Any (5 errors)

### haive-core

- `packages/haive-core/src/haive/core/schema/composer/_base.py:152` - error: No overload variant of "create_model" matches argument types "str", "Any | type", "dict[str,
  - ID: e0916192
- `packages/haive-core/src/haive/core/engine/prompt_template/prompt_engine.py:294` - error: No overload variant of "create_model" matches argument types "str", "dict[str, tuple[Any, Any
  - ID: 956eb336
- `packages/haive-core/src/haive/core/schema/schema_composer.py:3099` - error: No overload variant of "create_model" matches argument types "str", "dict[str, tuple[Any, Any
  - ID: 723b5918
- `packages/haive-core/src/haive/core/schema/schema_composer.py:3223` - error: No overload variant of "create_model" matches argument types "str", "dict[str, tuple[Any, Any
  - ID: 0a60e00f
- `packages/haive-core/src/haive/core/utils/tools/tool_schema_generator.py:229` - error: No overload variant of "create_model" matches argument types "str", "dict[str, tuple[Any, Any
  - ID: 393c3b50

## mypy:str, tuple[Any, EllipsisType | Any (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/document/loaders/registry.py:275` - error: No overload variant of "create_model" matches argument types "str", "dict[str, tuple[Any, Ell
  - ID: b8076e07

## mypy:str, tuple[type, Any (7 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/base/base.py:168` - error: No overload variant of "create_model" matches argument types "str", "dict[str, tuple[type, An
  - ID: b4b9553e
- `packages/haive-core/src/haive/core/engine/base/base.py:195` - error: No overload variant of "create_model" matches argument types "str", "dict[str, tuple[type, An
  - ID: 76c251ec
- `packages/haive-core/src/haive/core/engine/aug_llm/config.py:815` - note: Perhaps you need a type annotation for "fields"? Suggestion: "dict[str, tuple[type, Any]]"
  - ID: 774d51b9
- `packages/haive-core/src/haive/core/engine/aug_llm/config.py:847` - note: Perhaps you need a type annotation for "fields"? Suggestion: "dict[str, tuple[type, Any]]"
  - ID: e534780b
- `packages/haive-core/src/haive/core/engine/aug_llm/config.py:849` - note: Perhaps you need a type annotation for "fields"? Suggestion: "dict[str, tuple[type, Any]]"
  - ID: 77750ae6
- `packages/haive-core/src/haive/core/engine/agent/config.py:617` - error: Returning Any from function declared to return "dict[str, tuple[type, Any]]" [no-any-return]
  - ID: 1f637b72
- `packages/haive-core/src/haive/core/engine/agent/config.py:619` - error: Returning Any from function declared to return "dict[str, tuple[type, Any]]" [no-any-return]
  - ID: e311d427

## mypy:str, tuple[type[Any (10 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/base/enhanced_agent.py:556` - error: Incompatible return value type (got "dict[str, tuple[type[Any] | None, Any]]", expected "dict
  - ID: 9944e7a2
- `packages/haive-agents/src/haive/agents/base/enhanced_agent.py:570` - error: Incompatible return value type (got "dict[str, tuple[type[Any] | None, Any]]", expected "dict
  - ID: 3e6253bf

### haive-core

- `packages/haive-core/src/haive/core/utils/haive_discovery/base_analyzer.py:159` - error: No overload variant of "create_model" matches argument types "str", "ConfigDict | None", "dic
  - ID: 8d4b64d9
- `packages/haive-core/src/haive/core/schema/utils.py:363` - error: No overload variant of "create_model" matches argument types "str", "type | None", "dict[str,
  - ID: 897fa576
- `packages/haive-core/src/haive/core/engine/retriever/retriever.py:190` - error: Incompatible return value type (got "dict[str, tuple[type[Any] | None, Any]]", expected "dict
  - ID: 7d1ad179
- `packages/haive-core/src/haive/core/engine/retriever/retriever.py:201` - error: Incompatible return value type (got "dict[str, tuple[type[Any] | None, Any]]", expected "dict
  - ID: a200a9c2
- `packages/haive-core/src/haive/core/engine/aug_llm/config.py:815` - error: Incompatible return value type (got "dict[str, tuple[type[Any], None]]", expected "dict[str,
  - ID: cde9705b
- `packages/haive-core/src/haive/core/common/mixins/prompt_template_mixin.py:386` - error: No overload variant of "create_model" matches argument types "str", "dict[str, tuple[type[Any
  - ID: b2dac187
- `packages/haive-core/src/haive/core/schema/state_schema.py:1389` - error: No overload variant of "create_model" matches argument types "str", "dict[str, tuple[type[Any
  - ID: dedc6099
- `packages/haive-core/src/haive/core/schema/state_schema.py:1500` - error: No overload variant of "create_model" matches argument types "str", "dict[str, tuple[type[Any
  - ID: 26ecb937

## mypy:str, tuple[type[str (2 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/aug_llm/config.py:847` - error: Incompatible return value type (got "dict[str, tuple[type[str], None]]", expected "dict[str,
  - ID: b73cc185
- `packages/haive-core/src/haive/core/engine/aug_llm/config.py:849` - error: Incompatible return value type (got "dict[str, tuple[type[str], None]]", expected "dict[str,
  - ID: c26fb90e

## mypy:truthy-function (4 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/rag/simple/enhanced_v3/agent.py:275` - error: Function "state_schema" could always be true in boolean context [truthy-function]
  - ID: b70d48d8

### haive-core

- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:245` - error: Function "last_ai" could always be true in boolean context [truthy-function]
  - ID: 5a4af052
- `packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:459` - error: Function "last_human_message" could always be true in boolean context [truthy-function]
  - ID: bf76bd9b

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:50` - error: Function "handler" could always be true in boolean context [truthy-function]
  - ID: b5b0d564

## mypy:tuple[Any, ... (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/persistence/postgres_saver_with_thread_creation.py:35` - error: Argument 1 to "**init**" of "PostgresSaver" has incompatible type "Connection[tuple[Any, ...]
  - ID: 6fe0b9f9

## mypy:tuple[int, Any | BaseException (2 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/multi/enhanced_parallel_agent.py:250` - error: Incompatible types in assignment (expression has type "list[tuple[int, Any | BaseException]]"
  - ID: 7ae34e59
- `packages/haive-agents/src/haive/agents/multi/archive/enhanced_parallel_agent.py:250` - error: Incompatible types in assignment (expression has type "list[tuple[int, Any | BaseException]]"
  - ID: a4fb6bd5

## mypy:tuple[str, Any (2 errors)

### haive-core

- `packages/haive-core/src/haive/core/persistence/postgres_saver_with_thread_creation.py:126` - note: def put*writes(self, config: RunnableConfig, writes: Sequence[tuple[str, Any]], task*
  - ID: 0f206251
- `packages/haive-core/src/haive/core/persistence/postgres_saver_with_thread_creation.py:126` - note: def put*writes(self, config: RunnableConfig, writes: Sequence[tuple[str, Any]], task*
  - ID: 0f206251

## mypy:tuple[str, float (1 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/discovery/semantic_discovery.py:262` - note: Perhaps you need a type annotation for "matches"? Suggestion: "list[tuple[str, float]]"
  - ID: 1b62c4b0

## mypy:tuple[str, int (2 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/discovery/semantic_discovery.py:262` - error: Incompatible return value type (got "list[tuple[str, int]]", expected "list[tuple[str, float]
  - ID: ac07623e

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/tools/server_selector.py:342` - error: Argument "suggested_servers" to "TaskRequirements" has incompatible type "list[tuple[str, int
  - ID: f3da0fbd

## mypy:tuple[str, str (3 errors)

### haive-core

- `packages/haive-core/src/haive/core/graph/state_graph/components/edge_manager.py:212` - error: Returning Any from function declared to return "list[tuple[str, str]]" [no-any-return]
  - ID: 5e0cdf7f
- `packages/haive-core/src/haive/core/graph/state_graph/components/modular_base_graph.py:229` - error: Returning Any from function declared to return "list[tuple[str, str]]" [no-any-return]
  - ID: 6ba98770
- `packages/haive-core/src/haive/core/graph/state_graph/components/modular_base_graph.py:241` - error: Returning Any from function declared to return "list[tuple[str, str]]" [no-any-return]
  - ID: f0bbb86a

## mypy:type (2 errors)

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/registry/registries/model_registry.py:353` - error: Returning Any from function declared to return "list[type]" [no-any-return]
  - ID: 70f96416
- `packages/haive-dataflow/src/haive/dataflow/registries/model_registry.py:353` - error: Returning Any from function declared to return "list[type]" [no-any-return]
  - ID: 13065f7e

## mypy:type-arg (8 errors)

### haive-games

- `packages/haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:160` - error: "PegSpace" expects no type arguments, but 1 given [type-arg]
  - ID: 08d1c96d
- `packages/haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:167` - error: "PegSpace" expects no type arguments, but 1 given [type-arg]
  - ID: 58a304e0
- `packages/haive-games/src/haive/games/single_player/logic_grid/base.py:127` - error: "LogicGridSpace" expects no type arguments, but 1 given [type-arg]
  - ID: e041c205
- `packages/haive-games/src/haive/games/single_player/logic_grid/base.py:129` - error: "LogicGridSpace" expects no type arguments, but 1 given [type-arg]
  - ID: 06ad5896
- `packages/haive-games/src/haive/games/core/components/cards/turns.py:57` - error: "CardGameTurn" expects no type arguments, but 3 given [type-arg]
  - ID: f25945f9
- `packages/haive-games/src/haive/games/core/components/cards/scoring.py:36` - error: "HandRank" expects no type arguments, but 1 given [type-arg]
  - ID: 89974e3d
- `packages/haive-games/src/haive/games/core/components/cards/actions.py:33` - error: "CardAction" expects no type arguments, but 2 given [type-arg]
  - ID: fe41c8f4
- `packages/haive-games/src/haive/games/core/components/cards/actions.py:58` - error: "CardAction" expects no type arguments, but 2 given [type-arg]
  - ID: 24856f1c

## mypy:type-var (10 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/agent/agent.py:2014` - error: A function returning TypeVar should receive at least one argument containing the same TypeVar
  - ID: 55077e66

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/discovery.py:59` - error: Value of type variable "AnyOrLiteralStr" of "dirname" cannot be "str | None" [type-var]
  - ID: fdd01098
- `packages/haive-dataflow/src/haive/dataflow/registry/discovery.py:102` - error: Value of type variable "AnyOrLiteralStr" of "dirname" cannot be "str | None" [type-var]
  - ID: aa514f7f
- `packages/haive-dataflow/src/haive/dataflow/registry/providers/base.py:151` - error: Value of type variable "AnyOrLiteralStr" of "dirname" cannot be "str | None" [type-var]
  - ID: 8bc906c8
- `packages/haive-dataflow/src/haive/dataflow/providers/base.py:80` - error: Value of type variable "AnyOrLiteralStr" of "dirname" cannot be "str | None" [type-var]
  - ID: 8faa8120
- `packages/haive-dataflow/src/haive/dataflow/api/game_router.py:105` - error: Value of type variable "AnyOrLiteralStr" of "dirname" cannot be "str | None" [type-var]
  - ID: e46fdc6a

### haive-games

- `packages/haive-games/src/haive/games/nim/example.py:826` - error: Value of type variable "SupportsRichComparisonT" of "min" cannot be "object" [type-var]
  - ID: 134fb346
- `packages/haive-games/src/haive/games/nim/example.py:826` - error: Value of type variable "SupportsRichComparisonT" of "min" cannot be "object" [type-var]
  - ID: 134fb346
- `packages/haive-games/src/haive/games/nim/example.py:828` - error: Value of type variable "SupportsRichComparisonT" of "min" cannot be "object" [type-var]
  - ID: af5fef2f
- `packages/haive-games/src/haive/games/nim/example.py:828` - error: Value of type variable "SupportsRichComparisonT" of "min" cannot be "object" [type-var]
  - ID: af5fef2f

## mypy:type[Any (7 errors)

### haive-core

- `packages/haive-core/src/haive/core/utils/debugkit/analysis/types.py:129` - error: Incompatible types in assignment (expression has type "None", variable has type "list[type[An
  - ID: 464c2028
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/types.py:130` - error: Incompatible types in assignment (expression has type "None", variable has type "list[type[An
  - ID: 5f25c2d5
- `packages/haive-core/src/haive/core/engine/aug_llm/config.py:844` - error: Incompatible types in assignment (expression has type "tuple[type[Any], None]", target has ty
  - ID: c8335bb5
- `packages/haive-core/src/haive/core/engine/agent/config.py:155` - error: Value expression in dictionary comprehension has incompatible type "tuple[type[Any] | Any | N
  - ID: a0eb9d3a
- `packages/haive-core/src/haive/core/engine/agent/config.py:157` - error: Value expression in dictionary comprehension has incompatible type "tuple[type[Any] | Any | N
  - ID: 4c4d7e14
- `packages/haive-core/src/haive/core/engine/agent/config.py:169` - error: Value expression in dictionary comprehension has incompatible type "tuple[type[Any] | Any | N
  - ID: a1bef07b
- `packages/haive-core/src/haive/core/engine/agent/config.py:171` - error: Value expression in dictionary comprehension has incompatible type "tuple[type[Any] | Any | N
  - ID: bfa9396e

## mypy:type[dict[str, Any (2 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/aug_llm/config.py:830` - error: Incompatible types in assignment (expression has type "tuple[type[dict[str, Any]], None]", ta
  - ID: 65b8d358
- `packages/haive-core/src/haive/core/engine/aug_llm/config.py:841` - error: Incompatible types in assignment (expression has type "tuple[type[dict[str, Any]], None]", ta
  - ID: 4a0f58e3

## mypy:type[list[BaseMessage (2 errors)

### haive-core

- `packages/haive-core/src/haive/core/engine/aug_llm/config.py:846` - error: Incompatible types in assignment (expression has type "tuple[type[list[BaseMessage]], list[Ne
  - ID: 4bde0773
- `packages/haive-core/src/haive/core/engine/aug_llm/config.py:848` - error: Incompatible types in assignment (expression has type "tuple[type[list[BaseMessage]], list[Ne
  - ID: 480c42c9

## mypy:typeddict-item (14 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/react_class/react_agent2/tool_utils.py:237` - error: TypedDict "ToolCall" has no key "function" [typeddict-item]
  - ID: 2f10815f
- `packages/haive-agents/src/haive/agents/react_class/react_agent2/debug.py:98` - error: TypedDict "ToolCall" has no key "function" [typeddict-item]
  - ID: bf2e2713
- `packages/haive-agents/src/haive/agents/planning/llm_compiler/output_parser.py:97` - error: Incompatible types (expression has type "str", TypedDict item "tool" has type "BaseTool") [t
  - ID: f584fef9

### haive-core

- `packages/haive-core/src/haive/core/schema/prebuilt/messages/token_usage.py:120` - error: TypedDict "UsageMetadata" has no key "usage" [typeddict-item]
  - ID: ba4ecb50
- `packages/haive-core/src/haive/core/schema/prebuilt/messages/token_usage.py:128` - error: TypedDict "UsageMetadata" has no key "usage" [typeddict-item]
  - ID: 65da84d9
- `packages/haive-core/src/haive/core/graph/node/state_updating_validation_node.py:392` - error: TypedDict "ToolCall" has no key "metadata" [typeddict-item]
  - ID: 67441a4c
- `packages/haive-core/src/haive/core/graph/node/state_updating_validation_node.py:393` - error: TypedDict "ToolCall" has no key "metadata" [typeddict-item]
  - ID: 11185e7a
- `packages/haive-core/src/haive/core/graph/node/state_updating_validation_node.py:396` - error: TypedDict "ToolCall" has no key "metadata" [typeddict-item]
  - ID: e6cd5702
- `packages/haive-core/src/haive/core/persistence/factory.py:586` - error: Missing keys ("v", "id", "ts", "channel_versions", "versions_seen") for TypedDict "Checkpoint
  - ID: 3032edaa

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:244` - error: Missing keys ("article_text", "current_query", "chunks", "summary_result", "fact_check_result
  - ID: 2ac2f26a
- `packages/haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:261` - error: Missing keys ("article_text", "current_query", "chunks", "actions", "summary_result", "tone_a
  - ID: 0c648b35
- `packages/haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:268` - error: Missing keys ("article_text", "current_query", "chunks", "actions", "summary_result", "fact_c
  - ID: 62867a69
- `packages/haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:275` - error: Missing keys ("article_text", "current_query", "chunks", "actions", "summary_result", "fact_c
  - ID: d0c8ed52
- `packages/haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:367` - error: Missing keys ("article_text", "current_query", "chunks", "actions", "summary_result", "fact_c
  - ID: dfefc37d

## mypy:typeddict-unknown-key (1 errors)

### haive-core

- `packages/haive-core/src/haive/core/graph/node/state_updating_validation_node.py:390` - error: TypedDict "ToolCall" has no key "metadata" [typeddict-unknown-key]
  - ID: 4297db11

## mypy:typing_extensions.TypeVar (2 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/base/enhanced_agent.py:26` - error: Incompatible import of "TypeVar" (imported name has type "type[typing_extensions.TypeVar]", l
  - ID: a5483ab8
- `packages/haive-agents/src/haive/agents/simple/agent_v3.py:56` - error: Incompatible import of "TypeVar" (imported name has type "type[typing_extensions.TypeVar]", l
  - ID: 858b7cb2

## mypy:union-attr (303 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/planning/plan_and_execute/state.py:25` - error: Item "None" of "Any | None" has no attribute "remove_completed_steps" [union-attr]
  - ID: 2c1495c5
- `packages/haive-agents/src/haive/agents/planning/plan_and_execute/state.py:26` - error: Item "None" of "Any | None" has no attribute "update_status" [union-attr]
  - ID: 61479486
- `packages/haive-agents/src/haive/agents/supervisor/registry_supervisor.py:232` - error: Item "None" of "Any | None" has no attribute "option_names" [union-attr]
  - ID: 7b6a918c
- `packages/haive-agents/src/haive/agents/supervisor/registry_supervisor.py:233` - error: Item "None" of "Any | None" has no attribute "option_descriptions" [union-attr]
  - ID: 931f1042
- `packages/haive-agents/src/haive/agents/supervisor/choice_model_supervisor.py:207` - error: Item "None" of "Any | None" has no attribute "option_names" [union-attr]
  - ID: 29c6b40c
- `packages/haive-agents/src/haive/agents/supervisor/choice_model_supervisor.py:208` - error: Item "None" of "Any | None" has no attribute "option_descriptions" [union-attr]
  - ID: 3b1f164e
- `packages/haive-agents/src/haive/agents/supervisor/archive/registry_supervisor.py:232` - error: Item "None" of "Any | None" has no attribute "option_names" [union-attr]
  - ID: 9c8f270c
- `packages/haive-agents/src/haive/agents/supervisor/archive/registry_supervisor.py:233` - error: Item "None" of "Any | None" has no attribute "option_descriptions" [union-attr]
  - ID: bfd03c45
- `packages/haive-agents/src/haive/agents/supervisor/archive/choice_model_supervisor.py:207` - error: Item "None" of "Any | None" has no attribute "option_names" [union-attr]
  - ID: e99a0991
- `packages/haive-agents/src/haive/agents/supervisor/archive/choice_model_supervisor.py:208` - error: Item "None" of "Any | None" has no attribute "option_descriptions" [union-attr]
  - ID: a215259a
- ... and 69 more

### haive-core

- `packages/haive-core/src/haive/core/utils/debugkit/debug/inspection.py:32` - error: Item "None" of "FrameType | None" has no attribute "f_back" [union-attr]
  - ID: 1ecea407
- `packages/haive-core/src/haive/core/utils/debugkit/debug/inspection.py:33` - error: Item "None" of "FrameType | Any | None" has no attribute "f_locals" [union-attr]
  - ID: b8341003
- `packages/haive-core/src/haive/core/utils/debugkit/debug/inspection.py:49` - error: Item "None" of "FrameType | None" has no attribute "f_back" [union-attr]
  - ID: a20c73a6
- `packages/haive-core/src/haive/core/utils/debugkit/debug/inspection.py:50` - error: Item "None" of "FrameType | Any | None" has no attribute "f_globals" [union-attr]
  - ID: a51dd5aa
- `packages/haive-core/src/haive/core/utils/debugkit/debug/inspection.py:66` - error: Item "None" of "FrameType | None" has no attribute "f_back" [union-attr]
  - ID: 80d92b7f
- `packages/haive-core/src/haive/core/utils/debugkit/debug/inspection.py:74` - error: Item "None" of "FrameType | Any | None" has no attribute "f_locals" [union-attr]
  - ID: 544444db
- `packages/haive-core/src/haive/core/utils/debugkit/debug/inspection.py:75` - error: Item "None" of "FrameType | Any | None" has no attribute "f_globals" [union-attr]
  - ID: 46f09722
- `packages/haive-core/src/haive/core/utils/debugkit/debug/interactive.py:80` - error: Item "None" of "FrameType | None" has no attribute "f_back" [union-attr]
  - ID: df18ebc1
- `packages/haive-core/src/haive/core/schema/composer/engine/engine_detector.py:70` - error: Item "None" of "Any | None" has no attribute "**name**" [union-attr]
  - ID: 639d2d68
- `packages/haive-core/src/haive/core/utils/env_utils.py:167` - error: Item "None" of "str | None" has no attribute "lower" [union-attr]
  - ID: ad8e6bf4
- ... and 98 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/core.py:105` - error: Item "None" of "Any | None" has no attribute "rpc" [union-attr]
  - ID: cc99f697
- `packages/haive-dataflow/src/haive/dataflow/core.py:114` - error: Item "None" of "Any | None" has no attribute "rpc" [union-attr]
  - ID: 03664f23
- `packages/haive-dataflow/src/haive/dataflow/core.py:186` - error: Item "None" of "Any | None" has no attribute "rpc" [union-attr]
  - ID: 23c66a0a
- `packages/haive-dataflow/src/haive/dataflow/core.py:195` - error: Item "None" of "Any | None" has no attribute "rpc" [union-attr]
  - ID: 9c9de971
- `packages/haive-dataflow/src/haive/dataflow/core.py:212` - error: Item "None" of "Any | None" has no attribute "rpc" [union-attr]
  - ID: 13586cc6
- `packages/haive-dataflow/src/haive/dataflow/core.py:542` - error: Item "None" of "Any | None" has no attribute "query" [union-attr]
  - ID: eac403c0
- `packages/haive-dataflow/src/haive/dataflow/core.py:603` - error: Item "None" of "Any | None" has no attribute "query" [union-attr]
  - ID: 0e39ce27
- `packages/haive-dataflow/src/haive/dataflow/core.py:977` - error: Item "None" of "Any | None" has no attribute "rpc" [union-attr]
  - ID: fd518150
- `packages/haive-dataflow/src/haive/dataflow/core.py:986` - error: Item "None" of "Any | None" has no attribute "rpc" [union-attr]
  - ID: 607e2fab
- `packages/haive-dataflow/src/haive/dataflow/core.py:1059` - error: Item "None" of "Any | None" has no attribute "rpc" [union-attr]
  - ID: de4e7e00
- ... and 44 more

### haive-games

- `packages/haive-games/src/haive/games/monopoly/game/game.py:1243` - error: Item "None" of "Any | None" has no attribute "owner" [union-attr]
  - ID: e9767669
- `packages/haive-games/src/haive/games/monopoly/game/game.py:1249` - error: Item "None" of "Any | None" has no attribute "owner" [union-attr]
  - ID: 91bc5427
- `packages/haive-games/src/haive/games/among_us/state_manager.py:1239` - error: Item "None" of "Any | None" has no attribute "upper" [union-attr]
  - ID: 213882a7
- `packages/haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:54` - error: Item "None" of "Any | None" has no attribute "is_solved" [union-attr]
  - ID: 01d9a115
- `packages/haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:81` - error: Item "None" of "Any | None" has no attribute "is_solved" [union-attr]
  - ID: eea6551f
- `packages/haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:83` - error: Item "None" of "Any | None" has no attribute "moves" [union-attr]
  - ID: ab2f0bbd
- `packages/haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:84` - error: Item "None" of "Any | None" has no attribute "optimal_moves" [union-attr]
  - ID: 31390731
- `packages/haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:85` - error: Item "None" of "Any | None" has no attribute "optimal_moves" [union-attr]
  - ID: b3ab9035
- `packages/haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:85` - error: Item "None" of "Any | None" has no attribute "optimal_moves" [union-attr]
  - ID: b3ab9035
- `packages/haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:98` - error: Item "None" of "Any | None" has no attribute "format_board_state" [union-attr]
  - ID: 099d38cb
- ... and 39 more

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/dynamic_activation_mcp.py:322` - error: Item "None" of "Any | None" has no attribute "execute_agent" [union-attr]
  - ID: fd1d83c8
- `packages/haive-mcp/src/haive/mcp/manager.py:607` - error: Item "None" of "MCPHealthStatus | None" has no attribute "dict" [union-attr]
  - ID: a7327089
- `packages/haive-mcp/src/haive/mcp/fastapi_mcp_server.py:103` - error: Item "None" of "Any | None" has no attribute "enhanced_query" [union-attr]
  - ID: f7be2885
- `packages/haive-mcp/src/haive/mcp/mixins/mcp_mixin.py:165` - error: Item "None" of "Any | None" has no attribute "lazy_init" [union-attr]
  - ID: ff9e6f04
- `packages/haive-mcp/src/haive/mcp/mixins/mcp_mixin.py:260` - error: Item "None" of "Any | None" has no attribute "servers" [union-attr]
  - ID: 5f2e9317
- `packages/haive-mcp/src/haive/mcp/downloader/integration.py:162` - error: Item "None" of "Any | None" has no attribute "list_tools" [union-attr]
  - ID: 078fa887
- `packages/haive-mcp/src/haive/mcp/downloader/integration.py:170` - error: Item "None" of "Any | None" has no attribute "list_resources" [union-attr]
  - ID: 943eaaf6
- `packages/haive-mcp/src/haive/mcp/downloader/integration.py:176` - error: Item "None" of "Any | None" has no attribute "list_prompts" [union-attr]
  - ID: 9f0944d1

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:438` - error: Item "None" of "IdeaMetrics | None" has no attribute "overall_score" [union-attr]
  - ID: 3ea8394e
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/tools.py:202` - error: Item "None" of "PageElement | None" has no attribute "get_text" [union-attr]
  - ID: bfdb1aff
- `packages/haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/agent.py:76` - error: Item "None" of "Any | None" has no attribute "to_pitch_deck_brief" [union-attr]
  - ID: b41f3871
- `packages/haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/agent.py:289` - error: Item "None" of "Any | None" has no attribute "slides" [union-attr]
  - ID: db74109d
- `packages/haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/example.py:29` - error: Item "None" of "BaseMessage | None" has no attribute "content" [union-attr]
  - ID: 3e24dced

## mypy:unreachable (253 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/planning/base/models.py:804` - error: Statement is unreachable [unreachable]
  - ID: dcc18661
- `packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_v3.py:255` - error: Statement is unreachable [unreachable]
  - ID: fd9c3270
- `packages/haive-agents/src/haive/agents/multi/clean.py:185` - error: Statement is unreachable [unreachable]
  - ID: 1d69535d
- `packages/haive-agents/src/haive/agents/multi/enhanced/multi_agent_v3.py:302` - error: Statement is unreachable [unreachable]
  - ID: 930d5146
- `packages/haive-agents/src/haive/agents/multi/core/clean_multi_agent.py:188` - error: Statement is unreachable [unreachable]
  - ID: c7f16bf5
- `packages/haive-agents/src/haive/agents/memory_reorganized/agents/multi.py:432` - error: Statement is unreachable [unreachable]
  - ID: 77a7d797
- `packages/haive-agents/src/haive/agents/planning/rewoo/models/join_step.py:359` - error: Statement is unreachable [unreachable]
  - ID: b2605299
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/utils.py:108` - error: Statement is unreachable [unreachable]
  - ID: 13ceb3f3
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/utils.py:110` - error: Statement is unreachable [unreachable]
  - ID: c2bcb5c9
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/utils.py:112` - error: Statement is unreachable [unreachable]
  - ID: 9c856307
- ... and 62 more

### haive-core

- `packages/haive-core/src/haive/core/types/serializable_callable.py:23` - error: Statement is unreachable [unreachable]
  - ID: 7c0b38b4
- `packages/haive-core/src/haive/core/engine/vectorstore/discovery.py:85` - error: Statement is unreachable [unreachable]
  - ID: 7bc7beab
- `packages/haive-core/src/haive/core/engine/vectorstore/discovery.py:87` - error: Statement is unreachable [unreachable]
  - ID: 70e3156e
- `packages/haive-core/src/haive/core/engine/vectorstore/discovery.py:89` - error: Statement is unreachable [unreachable]
  - ID: 262f36af
- `packages/haive-core/src/haive/core/engine/vectorstore/discovery.py:91` - error: Statement is unreachable [unreachable]
  - ID: 52c0c373
- `packages/haive-core/src/haive/core/engine/vectorstore/discovery.py:93` - error: Statement is unreachable [unreachable]
  - ID: ed10b817
- `packages/haive-core/src/haive/core/schema/compatibility/field_mapping.py:101` - error: Statement is unreachable [unreachable]
  - ID: 29654bf9
- `packages/haive-core/src/haive/core/schema/compatibility/field_mapping.py:145` - error: Statement is unreachable [unreachable]
  - ID: 0cbf427b
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:157` - error: Statement is unreachable [unreachable]
  - ID: 6148a93e
- `packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:236` - error: Statement is unreachable [unreachable]
  - ID: 3ff2ca05
- ... and 125 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/api/db.py:306` - error: Statement is unreachable [unreachable]
  - ID: 2f28a290
- `packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:51` - error: Statement is unreachable [unreachable]
  - ID: 675d1609
- `packages/haive-dataflow/src/haive/dataflow/api/routes/conversation_routes.py:167` - error: Statement is unreachable [unreachable]
  - ID: 1cf888a8

### haive-games

- `packages/haive-games/src/haive/games/cards/models/card.py:194` - error: Statement is unreachable [unreachable]
  - ID: a67d228a
- `packages/haive-games/src/haive/games/cards/models/card.py:208` - error: Statement is unreachable [unreachable]
  - ID: 56ea8926
- `packages/haive-games/src/haive/games/mafia/agent.py:595` - error: Statement is unreachable [unreachable]
  - ID: 65a9dda6
- `packages/haive-games/src/haive/games/mafia/state_manager.py:455` - error: Statement is unreachable [unreachable]
  - ID: 84ddfb2e
- `packages/haive-games/src/haive/games/mafia/state_manager.py:460` - error: Statement is unreachable [unreachable]
  - ID: f00a4361
- `packages/haive-games/src/haive/games/tic_tac_toe/state.py:114` - error: Statement is unreachable [unreachable]
  - ID: 734e0b71
- `packages/haive-games/src/haive/games/tic_tac_toe/state.py:116` - error: Statement is unreachable [unreachable]
  - ID: 090e116d
- `packages/haive-games/src/haive/games/risk/models.py:958` - error: Statement is unreachable [unreachable]
  - ID: 35462438
- `packages/haive-games/src/haive/games/mafia/models.py:190` - error: Statement is unreachable [unreachable]
  - ID: 921eddb6
- `packages/haive-games/src/haive/games/core/components/cards/scoring.py:20` - error: Statement is unreachable [unreachable]
  - ID: 8c66486c
- ... and 23 more

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/fastmcp_runner.py:248` - error: Statement is unreachable [unreachable]
  - ID: 2d3d0bab
- `packages/haive-mcp/src/haive/mcp/tools/server_tester.py:80` - error: Statement is unreachable [unreachable]
  - ID: e3e008cb
- `packages/haive-mcp/src/haive/mcp/tools/server_tester.py:82` - error: Statement is unreachable [unreachable]
  - ID: d58b5f21
- `packages/haive-mcp/src/haive/mcp/tools/server_tester.py:134` - error: Statement is unreachable [unreachable]
  - ID: 7f026836
- `packages/haive-mcp/src/haive/mcp/enhance_mcp_data.py:48` - error: Statement is unreachable [unreachable]
  - ID: 20b66ad7
- `packages/haive-mcp/src/haive/mcp/mcp_simple_rag_agent.py:570` - error: Statement is unreachable [unreachable]
  - ID: 3a03efcb
- `packages/haive-mcp/src/haive/mcp/simple_faiss_retriever.py:122` - error: Statement is unreachable [unreachable]
  - ID: 3543ea6f

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/weather_disaster_management/agent.py:493` - error: Statement is unreachable [unreachable]
  - ID: 77c5f1db
- `packages/haive-prebuilt/src/haive/prebuilt/project_manager/agent.py:48` - error: Statement is unreachable [unreachable]
  - ID: 429c6785

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:610` - error: Statement is unreachable [unreachable]
  - ID: 70f115a7

## mypy:unused-ignore (20 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/task_analysis/tree/models.py:35` - Unused "type: ignore" comment [unused-ignore]
  - ID: 04709a9c
- `packages/haive-agents/src/haive/agents/task_analysis/tree/models.py:103` - Unused "type: ignore" comment [unused-ignore]
  - ID: 089759df
- `packages/haive-agents/src/haive/agents/task_analysis/tree/models.py:115` - Unused "type: ignore" comment [unused-ignore]
  - ID: 3e350315
- `packages/haive-agents/src/haive/agents/task_analysis/tree/models.py:149` - Unused "type: ignore" comment [unused-ignore]
  - ID: 1b800f65
- `packages/haive-agents/src/haive/agents/task_analysis/tree/models.py:231` - Unused "type: ignore" comment [unused-ignore]
  - ID: 8d77af0a
- `packages/haive-agents/src/haive/agents/conversation/collaberative/example.py:111` - Unused "type: ignore" comment [unused-ignore]
  - ID: 34a1173a
- `packages/haive-agents/src/haive/agents/conversation/collaberative/example.py:173` - Unused "type: ignore" comment [unused-ignore]
  - ID: 9bccb194
- `packages/haive-agents/src/haive/agents/conversation/collaberative/example.py:238` - Unused "type: ignore" comment [unused-ignore]
  - ID: 570f0e3f
- `packages/haive-agents/src/haive/agents/memory_v2/test_deepseek_integration.py:95` - Unused "type: ignore" comment [unused-ignore]
  - ID: b8233547
- `packages/haive-agents/src/haive/agents/memory_v2/test_deepseek_integration.py:130` - Unused "type: ignore" comment [unused-ignore]
  - ID: 61a28b7f
- ... and 8 more

### haive-core

- `packages/haive-core/src/haive/core/schema/__init__.py:159` - Unused "type: ignore" comment [unused-ignore]
  - ID: bd2bb326
- `packages/haive-core/src/haive/core/types/tree_leaf.py:47` - Unused "type: ignore" comment [unused-ignore]
  - ID: 5f4b6517

## mypy:used-before-def (38 errors)

### haive-core

- `packages/haive-core/src/haive/core/graph/node/handlers.py:215` - error: Name "updates" is used before definition [used-before-def]
  - ID: 3cba51e3
- `packages/haive-core/src/haive/core/graph/node/handlers.py:217` - error: Name "updates" is used before definition [used-before-def]
  - ID: 9b29293f
- `packages/haive-core/src/haive/core/graph/node/handlers.py:233` - error: Name "updates" is used before definition [used-before-def]
  - ID: 6e6df588
- `packages/haive-core/src/haive/core/graph/node/handlers.py:243` - error: Name "updates" is used before definition [used-before-def]
  - ID: e46ff1be
- `packages/haive-core/src/haive/core/graph/node/handlers.py:255` - error: Name "updates" is used before definition [used-before-def]
  - ID: a0a58b6e
- `packages/haive-core/src/haive/core/graph/node/handlers.py:256` - error: Name "updates" is used before definition [used-before-def]
  - ID: bca3baf1
- `packages/haive-core/src/haive/core/graph/node/handlers.py:262` - error: Name "updates" is used before definition [used-before-def]
  - ID: f0dbd455
- `packages/haive-core/src/haive/core/graph/node/handlers.py:270` - error: Name "updates" is used before definition [used-before-def]
  - ID: ef67b47c
- `packages/haive-core/src/haive/core/graph/node/handlers.py:281` - error: Name "updates" is used before definition [used-before-def]
  - ID: a9556d51
- `packages/haive-core/src/haive/core/graph/node/handlers.py:293` - error: Name "updates" is used before definition [used-before-def]
  - ID: 722111ce
- ... and 26 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_enhanced.py:147` - error: Name "\_discovery_cache" is used before definition [used-before-def]
  - ID: 8d1a0663
- `packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_enhanced.py:148` - error: Name "\_discovery_cache" is used before definition [used-before-def]
  - ID: a9c7364f

## mypy:valid-type (99 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/memory_reorganized/models/meta.py:24` - error: Function "builtins.callable" is not valid as a type [valid-type]
  - ID: 559490f9
- `packages/haive-agents/src/haive/agents/memory/models_dir/meta.py:12` - error: Function "builtins.callable" is not valid as a type [valid-type]
  - ID: 7c07a103
- `packages/haive-agents/src/haive/agents/patterns/sequential_workflow_agent.py:128` - error: Function "builtins.callable" is not valid as a type [valid-type]
  - ID: 6d0d72ee
- `packages/haive-agents/src/haive/agents/patterns/sequential_workflow_agent.py:286` - error: Function "builtins.callable" is not valid as a type [valid-type]
  - ID: e712707d
- `packages/haive-agents/src/haive/agents/common/models/task_analysis/analysis.py:27` - error: Variable "agents.common.models.task_analysis.analysis.ComplexityType" is not valid as a type
  - ID: 3d2af07b
- `packages/haive-agents/src/haive/agents/research/person/agent.py:402` - error: Variable "python_item_type" is not valid as a type [valid-type]
  - ID: edf592b2
- `packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_generic.py:27` - error: Variable "agents.multi.enhanced_multi_agent_generic.Agent" is not valid as a type [valid-typ
  - ID: 175b73a3
- `packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_generic.py:30` - error: Variable "agents.multi.enhanced_multi_agent_generic.Agent" is not valid as a type [valid-typ
  - ID: 2ea71cb9
- `packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_generic.py:132` - error: Variable "agents.multi.enhanced_multi_agent_generic.Agent" is not valid as a type [valid-typ
  - ID: 464a1703
- `packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_generic.py:163` - error: Variable "agents.multi.enhanced_multi_agent_generic.Agent" is not valid as a type [valid-typ
  - ID: 74c4c04c
- ... and 14 more

### haive-core

- `packages/haive-core/src/haive/core/graph/node/protocols.py:12` - error: Function "builtins.callable" is not valid as a type [valid-type]
  - ID: 01adf755
- `packages/haive-core/src/haive/core/graph/node/composer/update_functions.py:297` - error: Function "builtins.callable" is not valid as a type [valid-type]
  - ID: c652c618
- `packages/haive-core/src/haive/core/graph/common/field_utils.py:101` - error: Function "builtins.callable" is not valid as a type [valid-type]
  - ID: e58f0872
- `packages/haive-core/src/haive/core/graph/branches/utils.py:101` - error: Function "builtins.callable" is not valid as a type [valid-type]
  - ID: e0db3d1f
- `packages/haive-core/src/haive/core/utils/debugkit/benchmarking/timing.py:104` - error: Function "builtins.any" is not valid as a type [valid-type]
  - ID: 86c00b8a
- `packages/haive-core/src/haive/core/utils/debugkit/benchmarking/load.py:35` - error: Function "builtins.any" is not valid as a type [valid-type]
  - ID: cae294d5
- `packages/haive-core/src/haive/core/utils/debugkit/benchmarking/load.py:136` - error: Function "builtins.any" is not valid as a type [valid-type]
  - ID: 3f647a64
- `packages/haive-core/src/haive/core/utils/debugkit/benchmarking/load.py:167` - error: Function "builtins.any" is not valid as a type [valid-type]
  - ID: 20bd0d36
- `packages/haive-core/src/haive/core/types/tree_leaf.py:52` - error: Type variable "core.types.tree_leaf.T" is unbound [valid-type]
  - ID: e747db76
- `packages/haive-core/src/haive/core/types/tree_leaf.py:53` - error: Type variable "core.types.tree_leaf.T" is unbound [valid-type]
  - ID: 8159dcea
- ... and 25 more

### haive-dataflow

- `packages/haive-dataflow/src/haive/dataflow/mcp/health.py:129` - error: Function "builtins.any" is not valid as a type [valid-type]
  - ID: c10e072a
- `packages/haive-dataflow/src/haive/dataflow/api/routes/example_tool.py:20` - error: Function "builtins.any" is not valid as a type [valid-type]
  - ID: 0afe43de

### haive-games

- `packages/haive-games/src/haive/games/single_player/state_manager.py:31` - error: Variable "re.T" is not valid as a type [valid-type]
  - ID: e15deb02
- `packages/haive-games/src/haive/games/single_player/state_manager.py:46` - error: Variable "re.T" is not valid as a type [valid-type]
  - ID: 1fdb69ce
- `packages/haive-games/src/haive/games/single_player/state_manager.py:60` - error: Variable "re.T" is not valid as a type [valid-type]
  - ID: 83d48d04
- `packages/haive-games/src/haive/games/single_player/state_manager.py:82` - error: Variable "re.T" is not valid as a type [valid-type]
  - ID: 01fa402e
- `packages/haive-games/src/haive/games/single_player/state_manager.py:95` - error: Variable "re.T" is not valid as a type [valid-type]
  - ID: eb2c647c
- `packages/haive-games/src/haive/games/single_player/state_manager.py:108` - error: Variable "re.T" is not valid as a type [valid-type]
  - ID: e93daf48
- `packages/haive-games/src/haive/games/hold_em/utils.py:86` - error: Function "builtins.any" is not valid as a type [valid-type]
  - ID: 73fdbc32
- `packages/haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:22` - error: Function "builtins.any" is not valid as a type [valid-type]
  - ID: 16d92a17
- `packages/haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:28` - error: Function "builtins.any" is not valid as a type [valid-type]
  - ID: 2d4cec5e
- `packages/haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:32` - error: Function "builtins.any" is not valid as a type [valid-type]
  - ID: 47bc3157
- ... and 8 more

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/utils/extract_mcp_github_repos.py:665` - error: Function "builtins.callable" is not valid as a type [valid-type]
  - ID: fe826320

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:53` - error: Invalid type comment or annotation [valid-type]
  - ID: 50c4a676
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:119` - error: Invalid type comment or annotation [valid-type]
  - ID: 42d8a4be
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:144` - error: Invalid type comment or annotation [valid-type]
  - ID: 3d25c25b
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:160` - error: Invalid type comment or annotation [valid-type]
  - ID: cdd9ba84
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:179` - error: Invalid type comment or annotation [valid-type]
  - ID: 6aa2daee
- `packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:203` - error: Invalid type comment or annotation [valid-type]
  - ID: 2516a276
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/models.py:42` - error: Invalid type comment or annotation [valid-type]
  - ID: 210c8315
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/models.py:72` - error: Invalid type comment or annotation [valid-type]
  - ID: 15eca7e3
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/models.py:121` - error: Invalid type comment or annotation [valid-type]
  - ID: 4feeeaa3
- `packages/haive-prebuilt/src/haive/prebuilt/journalism_/models.py:124` - error: Invalid type comment or annotation [valid-type]
  - ID: f1ceadc6
- ... and 9 more

## mypy:var-annotated (69 errors)

### haive-agents

- `packages/haive-agents/src/haive/agents/supervisor/multi_agent_dynamic_state.py:330` - error: Need type annotation for "results" [var-annotated]
  - ID: dfc462d7
- `packages/haive-agents/src/haive/agents/supervisor/archive/multi_agent_dynamic_state.py:330` - error: Need type annotation for "results" [var-annotated]
  - ID: 52cf88b6
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/models.py:119` - error: Need type annotation for "nodes" [var-annotated]
  - ID: 81f0eb1a
- `packages/haive-agents/src/haive/agents/rag/multi_agent_rag/agents.py:535` - error: Need type annotation for "run_grading" [var-annotated]
  - ID: ae3c8aff
- `packages/haive-agents/src/haive/agents/rag/multi_agent_rag/agents.py:536` - error: Need type annotation for "run_iterative_grading" [var-annotated]
  - ID: 24d960be
- `packages/haive-agents/src/haive/agents/planning/rewoo/models/tool_step.py:160` - error: Need type annotation for "issues" [var-annotated]
  - ID: 9473d7bf
- `packages/haive-agents/src/haive/agents/memory_v2/multi_memory_coordinator.py:611` - error: Need type annotation for "results" [var-annotated]
  - ID: bfc9342f
- `packages/haive-agents/src/haive/agents/memory_v2/multi_memory_coordinator.py:788` - error: Need type annotation for "migration_result" [var-annotated]
  - ID: ae19d519
- `packages/haive-agents/src/haive/agents/memory_v2/integrated_memory_system.py:262` - error: Need type annotation for "results" [var-annotated]
  - ID: 00618470
- `packages/haive-agents/src/haive/agents/memory_v2/integrated_memory_system.py:323` - error: Need type annotation for "results" [var-annotated]
  - ID: ff617d32
- ... and 15 more

### haive-core

- `packages/haive-core/src/haive/core/registry/memory.py:18` - error: Need type annotation for "engines" [var-annotated]
  - ID: 545a2d00
- `packages/haive-core/src/haive/core/graph/state_graph/components/edge_manager.py:292` - error: Need type annotation for "adjacency" [var-annotated]
  - ID: ae232334
- `packages/haive-core/src/haive/core/engine/base/registry.py:59` - error: Need type annotation for "engines" [var-annotated]
  - ID: aa0d016f
- `packages/haive-core/src/haive/core/schema/compatibility/utils.py:265` - error: Need type annotation for "diff" [var-annotated]
  - ID: f2c9b1a7
- `packages/haive-core/src/haive/core/graph/state_graph/state_graph.py:389` - error: Need type annotation for "result" [var-annotated]
  - ID: 8eb8c80b
- `packages/haive-core/src/haive/core/graph/state_graph_manager.py:23` - error: Need type annotation for "metadata" [var-annotated]
  - ID: 1d7e1561
- `packages/haive-core/src/haive/core/graph/state_graph_manager.py:174` - error: Need type annotation for "G" [var-annotated]
  - ID: 3032db05
- `packages/haive-core/src/haive/core/engine/document/loaders/sources/analytics_sources.py:730` - error: Need type annotation for "range_query" [var-annotated]
  - ID: 92b90053
- `packages/haive-core/src/haive/core/utils/tool_list.py:402` - error: Need type annotation for "categories" [var-annotated]
  - ID: eb564ef9
- `packages/haive-core/src/haive/core/utils/model_utils.py:7` - error: Need type annotation for "parser" [var-annotated]
  - ID: 4087d142
- ... and 19 more

### haive-games

- `packages/haive-games/src/haive/games/__init__.py:90` - error: Need type annotation for "submod_attrs" [var-annotated]
  - ID: 7e5e4dce
- `packages/haive-games/src/haive/games/core/game/containers/deck.py:68` - error: Need type annotation for "hands" [var-annotated]
  - ID: ae6814ea
- `packages/haive-games/src/haive/games/core/game/containers/container.py:98` - error: Need type annotation for "hands" [var-annotated]
  - ID: 9e3a25db
- `packages/haive-games/src/haive/games/core/game/containers/base.py:226` - error: Need type annotation for "hands" [var-annotated]
  - ID: 5b1db628
- `packages/haive-games/src/haive/games/monopoly/state.py:551` - error: Need type annotation for "analysis" [var-annotated]
  - ID: 7a03c515

### haive-mcp

- `packages/haive-mcp/src/haive/mcp/__init__.py:44` - error: Need type annotation for "submod_attrs" [var-annotated]
  - ID: aa3e1f26
- `packages/haive-mcp/src/haive/mcp/enhance_mcp_data.py:170` - error: Need type annotation for "dependencies" [var-annotated]
  - ID: ab3e69fe
- `packages/haive-mcp/src/haive/mcp/agents/documentation_agent.py:325` - error: Need type annotation for "result" [var-annotated]
  - ID: 85ce146d
- `packages/haive-mcp/src/haive/mcp/agents/documentation_agent.py:492` - error: Need type annotation for "guide" [var-annotated]
  - ID: f81e74d4
- `packages/haive-mcp/src/haive/mcp/downloader/integration.py:157` - error: Need type annotation for "capabilities" [var-annotated]
  - ID: 3cd3d19f

### haive-prebuilt

- `packages/haive-prebuilt/src/haive/prebuilt/__init__.py:172` - error: Need type annotation for "submod_attrs" [var-annotated]
  - ID: a44bea03
- `packages/haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:142` - error: Need type annotation for "tone_pipeline" [var-annotated]
  - ID: c3764456
- `packages/haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:173` - error: Need type annotation for "quote_extraction_pipeline" [var-annotated]
  - ID: 048fbe02
- `packages/haive-prebuilt/src/haive/prebuilt/essay_grading/__init__.py:204` - error: Need type annotation for "grammar_and_bias_review" [var-annotated]
  - ID: 7d4def07

### haive-tools

- `packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/dependency_analyzer.py:41` - error: Need type annotation for "imports" [var-annotated]
  - ID: d6f508d6

## ruff:A001 (3 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/specialized_sources.py:149` - Variable `id` is shadowing a Python builtin
  - ID: 54867d0c
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/vectorstore.py:408` - Variable `filter` is shadowing a Python builtin
  - ID: 01f0a09f
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/vectorstore.py:414` - Variable `filter` is shadowing a Python builtin
  - ID: 2d4a336a

## ruff:A002 (29 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/logging_config.py:119` - Function argument `format` is shadowing a Python builtin
  - ID: f83be95b
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/logging_config.py:493` - Function argument `format` is shadowing a Python builtin
  - ID: ba39aef5
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/base/registry.py:111` - Function argument `id` is shadowing a Python builtin
  - ID: 40c11586
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/base/base.py:226` - Function argument `input` is shadowing a Python builtin
  - ID: 53e888e7
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/registry.py:110` - Function argument `id` is shadowing a Python builtin
  - ID: 6cfd9b71
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/vsdx_source.py:16` - Function argument `input` is shadowing a Python builtin
  - ID: b9d4e2f4
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/arxiv_source.py:16` - Function argument `input` is shadowing a Python builtin
  - ID: bc6de050
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/web_api.py:226` - Function argument `format` is shadowing a Python builtin
  - ID: e4017415
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/transformers/base.py:466` - Function argument `id` is shadowing a Python builtin
  - ID: d9d4cdda
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/vectorstore.py:335` - Function argument `filter` is shadowing a Python builtin
  - ID: 4856886c
- ... and 19 more

## ruff:ARG001 (210 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/pre_post_agent_mixin.py:420` - Unused function argument: `name`
  - ID: a3da1b4f
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/pre_post_agent_mixin.py:421` - Unused function argument: `kwargs`
  - ID: 4d987057
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/pre_post_agent_mixin.py:459` - Unused function argument: `name`
  - ID: 2124194b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/pre_post_agent_mixin.py:460` - Unused function argument: `kwargs`
  - ID: 6e314443
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/pre_post_agent_mixin.py:510` - Unused function argument: `name`
  - ID: bde9e52e
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/pre_post_agent_mixin.py:511` - Unused function argument: `kwargs`
  - ID: e4c7dd29
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/chain_examples.py:167` - Unused function argument: `s`
  - ID: e0994341
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/examples.py:35` - Unused function argument: `state`
  - ID: f499dfe1
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/examples.py:174` - Unused function argument: `documents`
  - ID: 1dafeb71
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/examples.py:205` - Unused function argument: `documents`
  - ID: 41b87461
- ... and 94 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/dynamic_choice_model.py:101` - Unused function argument: `cls`
  - ID: 9ec9a016
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/handlers.py:180` - Unused function argument: `runtime_config`
  - ID: c8576eba
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/utils/state_handling.py:100` - Unused function argument: `runtime_config`
  - ID: 2e2860e9
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/base_new.py:228` - Unused function argument: `source_class`
  - ID: 069b41dd
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/enhanced_registry.py:386` - Unused function argument: `supports_scrape_all`
  - ID: ef9b93c5
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/NodeFactory.py:500` - Unused function argument: `state`
  - ID: b4523175
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/NodeFactory.py:531` - Unused function argument: `config`
  - ID: 9e2a20f7
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/NodeFactory.py:1429` - Unused function argument: `config`
  - ID: d24a5083
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/graph_pattern_registry.py:271` - Unused function argument: `fallback_node`
  - ID: 3dc91718
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/graph_pattern_registry.py:271` - Unused function argument: `fallback_node`
  - ID: 3dc91718
- ... and 63 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:308` - Unused function argument: `args`
  - ID: b4782626
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:308` - Unused function argument: `args`
  - ID: b4782626
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/llm_routes.py:348` - Unused function argument: `user_id`
  - ID: 3fb4eba8
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/bin/registry_cli.py:486` - Unused function argument: `args`
  - ID: cd6046f9
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/bin/vault_cli.py:175` - Unused function argument: `args`
  - ID: 27d61a34
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/bin/vault_cli.py:247` - Unused function argument: `args`
  - ID: e290cc11
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/bin/vault_cli.py:276` - Unused function argument: `args`
  - ID: 4b38c116
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:484` - Unused function argument: `args`
  - ID: aaeb57ec
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py:175` - Unused function argument: `args`
  - ID: c4b7e28c
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py:247` - Unused function argument: `args`
  - ID: 170d5974
- ... and 1 more

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/comprehensive_mcp_web.py:647` - Unused function argument: `query`
  - ID: 6a116aeb
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/fastapi_mcp_server.py:291` - Unused function argument: `app`
  - ID: bf53b551
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/servers/simple_http_server.py:37` - Unused function argument: `request`
  - ID: fd129c8f
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/servers/simple_http_server.py:53` - Unused function argument: `request`
  - ID: 6fa0e4ab

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_books.py:71` - Unused function argument: `args`
  - ID: e8edcd1f
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_books.py:71` - Unused function argument: `args`
  - ID: e8edcd1f
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_finance.py:71` - Unused function argument: `args`
  - ID: 804a4632
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_finance.py:71` - Unused function argument: `args`
  - ID: 804a4632
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_jobs.py:88` - Unused function argument: `args`
  - ID: 68715235
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_jobs.py:88` - Unused function argument: `args`
  - ID: 68715235
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_lens.py:85` - Unused function argument: `args`
  - ID: 1ebeb435
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_lens.py:85` - Unused function argument: `args`
  - ID: 1ebeb435
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_places.py:73` - Unused function argument: `args`
  - ID: 75e081aa
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_places.py:73` - Unused function argument: `args`
  - ID: 75e081aa
- ... and 8 more

## ruff:ARG002 (388 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:654` - Unused method argument: `state`
  - ID: 37eee8c7
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:660` - Unused method argument: `state`
  - ID: acc8fe2d
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:673` - Unused method argument: `state`
  - ID: b85ae4ed
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/debug_utils.py:139` - Unused method argument: `thread_id`
  - ID: a9e33405
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/enhanced_agent.py:573` - Unused method argument: `runnable_config`
  - ID: 9fbc6f36
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:285` - Unused method argument: `state`
  - ID: 2971b9be
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/typed_agent.py:200` - Unused method argument: `result`
  - ID: b333813d
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/typed_agent.py:266` - Unused method argument: `state`
  - ID: f13952b9
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/typed_agent.py:272` - Unused method argument: `state`
  - ID: 610a2239
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/typed_agent.py:315` - Unused method argument: `state`
  - ID: 807e332b
- ... and 184 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/logging_config.py:350` - Unused method argument: `decision_type`
  - ID: 2ef71e51
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/structured_output_mixin.py:147` - Unused method argument: `description`
  - ID: a4ccf1b6
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/structured_output_mixin.py:147` - Unused method argument: `description`
  - ID: a4ccf1b6
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/named_list.py:118` - Unused method argument: `default_name`
  - ID: ac6b4572
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/postgres_config.py:134` - Unused method argument: `name`
  - ID: 22b16ae4
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:1302` - Unused method argument: `description`
  - ID: 4434767b
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:1302` - Unused method argument: `description`
  - ID: 4434767b
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/engine.py:98` - Unused method argument: `config`
  - ID: 56a537ed
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/engine.py:182` - Unused method argument: `source_type`
  - ID: 3ef5e6a9
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/engine.py:182` - Unused method argument: `source_type`
  - ID: 3ef5e6a9
- ... and 131 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:246` - Unused method argument: `content`
  - ID: ed881901
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:272` - Unused method argument: `content`
  - ID: 68f1a97f
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_socket.py:284` - Unused method argument: `thread_id`
  - ID: 9db5a409

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/transferable_mcp_agent.py:406` - Unused method argument: `agent`
  - ID: 755db507
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/cli/mcp_manager.py:272` - Unused method argument: `force`
  - ID: 2a7ae275
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/installers.py:185` - Unused method argument: `server_config`
  - ID: 8268fa3f
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/installers.py:276` - Unused method argument: `install_dir`
  - ID: db80b0ce
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/installers.py:312` - Unused method argument: `server_config`
  - ID: 1e11c454
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/installers.py:318` - Unused method argument: `install_dir`
  - ID: 9e07d01f
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/installers.py:361` - Unused method argument: `install_dir`
  - ID: 0d581322
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/installers.py:397` - Unused method argument: `server_config`
  - ID: f6b83f9c
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/installers.py:482` - Unused method argument: `template`
  - ID: fddd68c5
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/installers.py:512` - Unused method argument: `server_config`
  - ID: ec12e4b3
- ... and 30 more

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/reddit_search.py:69` - Unused method argument: `args`
  - ID: 48354ef1
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/reddit_search.py:69` - Unused method argument: `args`
  - ID: 48354ef1
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/import_consolidator.py:43` - Unused method argument: `original_node`
  - ID: 2f79e72c
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/type_hints.py:57` - Unused method argument: `original_node`
  - ID: 28763e39
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/code_smell_detector.py:57` - Unused method argument: `original_node`
  - ID: da9cc28f
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/complexity_analyzer.py:71` - Unused method argument: `original_node`
  - ID: 8e8ff44b
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/complexity_analyzer.py:87` - Unused method argument: `node`
  - ID: 32b171c4
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/complexity_analyzer.py:99` - Unused method argument: `node`
  - ID: 0b282fb2
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/complexity_analyzer.py:111` - Unused method argument: `node`
  - ID: d70f3764
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/complexity_analyzer.py:123` - Unused method argument: `node`
  - ID: 409f26d9

## ruff:ARG003 (38 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/rubric.py:43` - Unused class method argument: `info`
  - ID: 31934b54
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/task_analysis/analysis.py:315` - Unused class method argument: `domain`
  - ID: 555ee44e
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/task_analysis/analysis.py:315` - Unused class method argument: `domain`
  - ID: 555ee44e
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/task_analysis/analysis.py:366` - Unused class method argument: `domain`
  - ID: 54016a56
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/task_analysis/analysis.py:407` - Unused class method argument: `solvability`
  - ID: 9e24321e
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/task_analysis/analysis.py:422` - Unused class method argument: `planning`
  - ID: 61e95a01
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models_dir/base.py:45` - Unused class method argument: `info`
  - ID: 4bee0ce1
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/models/base.py:86` - Unused class method argument: `info`
  - ID: ab309671
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo/models/tool_step.py:68` - Unused class method argument: `info`
  - ID: 38d4c571
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/corrective/agent.py:61` - Unused class method argument: `relevance_threshold`
  - ID: d588aca6
- ... and 14 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/named_list.py:47` - Unused class method argument: `info`
  - ID: c0c1327e
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/ContextualCompressionRetrieverConfig.py:102` - Unused class method argument: `info`
  - ID: 9b2b83b7
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/LlamaIndexGraphRetrieverConfig.py:160` - Unused class method argument: `info`
  - ID: 5d235ba3
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/ParentDocumentRetrieverConfig.py:123` - Unused class method argument: `info`
  - ID: c74336f3
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/ParentDocumentRetrieverConfig.py:133` - Unused class method argument: `info`
  - ID: dfdd2c60
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/TimeWeightedVectorStoreRetrieverConfig.py:123` - Unused class method argument: `info`
  - ID: fe80dfba
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/ClickHouseVectorStoreConfig.py:154` - Unused class method argument: `info`
  - ID: c6e14dbe
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/NodeFactory.py:518` - Unused class method argument: `runnable_config`
  - ID: 53553ce3
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/NodeFactory.py:1269` - Unused class method argument: `state`
  - ID: 46b021f4
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/NodeFactory.py:1321` - Unused class method argument: `state`
  - ID: 34010e07
- ... and 4 more

## ruff:ARG004 (11 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models_dir/meta.py:15` - Unused static method argument: `kwargs`
  - ID: a849fe19
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models_dir/meta.py:60` - Unused static method argument: `obj`
  - ID: 82c860f3
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models_dir/meta.py:66` - Unused static method argument: `obj`
  - ID: f2f7ae3b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/models/meta.py:27` - Unused static method argument: `kwargs`
  - ID: f36f70de
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/models/meta.py:72` - Unused static method argument: `obj`
  - ID: 5d0fdf8a
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/models/meta.py:78` - Unused static method argument: `obj`
  - ID: c8ff640a
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/agentic/react_rag_agent.py:124` - Unused static method argument: `retriever_config`
  - ID: 0dcf2a5b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/enhanced_multi_rag.py:195` - Unused static method argument: `documents`
  - ID: 13a358bb

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/embeddings.py:24` - Unused static method argument: `config`
  - ID: 9b219646

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/conversation_routes.py:71` - Unused static method argument: `agent_id`
  - ID: 4aac52d0
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/internal_websockets/handlers.py:30` - Unused static method argument: `agent_id`
  - ID: f9b6fbf1

## ruff:ARG005 (84 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:392` - Unused lambda argument: `x`
  - ID: b0e8cc80
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/chain_examples.py:72` - Unused lambda argument: `s`
  - ID: 975ba742
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/chain_examples.py:73` - Unused lambda argument: `s`
  - ID: 6bfca02b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/chain_examples.py:99` - Unused lambda argument: `s`
  - ID: 5ae6a469
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/chain_examples.py:101` - Unused lambda argument: `s`
  - ID: 321fd970
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/chain_examples.py:102` - Unused lambda argument: `s`
  - ID: 62bb19e7
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/chain_examples.py:128` - Unused lambda argument: `s`
  - ID: 153e2010
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/chain_examples.py:129` - Unused lambda argument: `s`
  - ID: 9525c43d
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/chain_examples.py:137` - Unused lambda argument: `s`
  - ID: e3524fab
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/examples.py:252` - Unused lambda argument: `s`
  - ID: c05ef6af
- ... and 52 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/output_parser/base.py:223` - Unused lambda argument: `s`
  - ID: e9c0101c
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/output_parser/base.py:230` - Unused lambda argument: `c`
  - ID: ffac2c90
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/output_parser/base.py:238` - Unused lambda argument: `s`
  - ID: 81ead7f5
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/output_parser/base.py:251` - Unused lambda argument: `s`
  - ID: 7be21d39
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/output_parser/base.py:258` - Unused lambda argument: `c`
  - ID: 55dd5541
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/output_parser/base.py:264` - Unused lambda argument: `s`
  - ID: 8901e25a
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/output_parser/base.py:269` - Unused lambda argument: `s`
  - ID: 66bea656
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/output_parser/base.py:274` - Unused lambda argument: `s`
  - ID: 08597b6b
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/output_parser/base.py:280` - Unused lambda argument: `c`
  - ID: dfafa89a
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/test_modular_graph.py:63` - Unused lambda argument: `state`
  - ID: 08507b66
- ... and 6 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/base.py:336` - Unused lambda argument: `x`
  - ID: f04fb732
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/llm_routes.py:312` - Unused lambda argument: `x`
  - ID: c2f14f98
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/llm_routes.py:451` - Unused lambda argument: `x`
  - ID: e645a3a8
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/base.py:336` - Unused lambda argument: `x`
  - ID: 4258b70a

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/techy_phrase_tool.py:60` - Unused lambda argument: `x`
  - ID: 620b94ee
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/techy_phrase_tool.py:66` - Unused lambda argument: `x`
  - ID: ebb7fd1f

## ruff:B004 (2 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/interrupt_utils.py:111` - Using `hasattr(x, "__call__")` to test if x is callable is unreliable. Use `callable(x)` for consist
  - ID: cb2d767a
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/interrupt_utils.py:113` - Using `hasattr(x, "__call__")` to test if x is callable is unreliable. Use `callable(x)` for consist
  - ID: e7ccd2e2

## ruff:B005 (1 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/utils.py:121` - Using `.strip()` with multi-character strings is misleading
  - ID: cb82696c

## ruff:B007 (79 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_processing/examples/comprehensive_query_example.py:138` - Loop control variable `result` not used within loop body
  - ID: 4214b93e
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/test_memory_models_only.py:116` - Loop control variable `mem_type` not used within loop body
  - ID: bbd03c05
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/test_memory_models_only.py:119` - Loop control variable `importance` not used within loop body
  - ID: 0c4ad7bb
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/test_with_free_resources.py:202` - Loop control variable `score` not used within loop body
  - ID: 3b4965b0
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/archive/enhanced_parallel_agent.py:219` - Loop control variable `i` not used within loop body
  - ID: 30a11d16
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/archive/experiments/implementations/multi_agent_v2.py:177` - Loop control variable `i` not used within loop body
  - ID: 0d5a854a
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/archive/experiments/routing_patterns.py:178` - Loop control variable `i` not used within loop body
  - ID: a201b887
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced_parallel_agent.py:219` - Loop control variable `i` not used within loop body
  - ID: 5bf02666
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/implementations/multi_agent_v2.py:177` - Loop control variable `i` not used within loop body
  - ID: c666e6fd
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/routing_patterns.py:178` - Loop control variable `i` not used within loop body
  - ID: ed0343c0
- ... and 13 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/examples.py:359` - Loop control variable `source_type` not used within loop body
  - ID: 9a18d37e
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/examples.py:506` - Loop control variable `category` not used within loop body
  - ID: 14607e73
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/examples.py:539` - Loop control variable `source_type` not used within loop body
  - ID: 50dea068
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/examples.py:609` - Loop control variable `source` not used within loop body
  - ID: 8f1a4925
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/examples/minimal_example.py:86` - Loop control variable `file_path` not used within loop body
  - ID: 21f829c4
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/dynamic_graph_builder.py:1003` - Loop control variable `key` not used within loop body
  - ID: 4d171af8
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/agent_node_v3.py:453` - Loop control variable `agent_name` not used within loop body
  - ID: 26021b5d
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/factory.py:794` - Loop control variable `output_key` not used within loop body
  - ID: 33d59104
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/handlers.py:821` - Loop control variable `output_key` not used within loop body
  - ID: 5465778e
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/handlers.py:929` - Loop control variable `output_key` not used within loop body
  - ID: 712ddf94
- ... and 13 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes.py:203` - Loop control variable `ispkg` not used within loop body
  - ID: d4762552
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/importers/tak.py:466` - Loop control variable `module` not used within loop body
  - ID: e7bae318
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/importers/tak.py:471` - Loop control variable `module` not used within loop body
  - ID: 556bf8c1
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/importers/tak.py:466` - Loop control variable `module` not used within loop body
  - ID: 8502686d
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/importers/tak.py:471` - Loop control variable `module` not used within loop body
  - ID: 9dc932f9
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/serialization.py:409` - Loop control variable `name` not used within loop body
  - ID: 9febaaf7
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/serialization.py:328` - Loop control variable `name` not used within loop body
  - ID: d3139400

### haive-games

- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/enhanced_ui.py:181` - Loop control variable `key` not used within loop body
  - ID: 8778b989
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/state_manager.py:806` - Loop control variable `pid` not used within loop body
  - ID: 488f8952
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/state_manager.py:870` - Loop control variable `pid` not used within loop body
  - ID: 60542c57
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/example.py:449` - Loop control variable `config` not used within loop body
  - ID: 84d58206
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/example.py:491` - Loop control variable `config_name` not used within loop body
  - ID: 68b713e0
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/example.py:608` - Loop control variable `strategy` not used within loop body
  - ID: aabd5cde
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/simple_test.py:166` - Loop control variable `test_name` not used within loop body
  - ID: 958918c8
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/test_judges.py:184` - Loop control variable `test_name` not used within loop body
  - ID: e4832a7b
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/rich_ui.py:144` - Loop control variable `key` not used within loop body
  - ID: 527b5e60
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/example.py:127` - Loop control variable `i` not used within loop body
  - ID: 6fba76fd
- ... and 15 more

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/integrated_launcher.py:143` - Loop control variable `cat` not used within loop body
  - ID: 11719a4d

## ruff:B008 (50 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/agent.py:158` - Do not perform function call `ComplexExtractionAgentConfig` in argument defaults; instead, perform t
  - ID: b1488851
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_base/models.py:65` - Do not perform function call `AzureLLMConfig` in argument defaults; instead, perform the call within
  - ID: 40d7d1dc
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_iterative_refinement/agent.py:127` - Do not perform function call `IterativeGraphTransformerConfig` in argument defaults; instead, perfor
  - ID: 704e4010
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/iterative_refinement/agent.py:20` - Do not perform function call `IterativeSummarizerConfig` in argument defaults; instead, perform the
  - ID: 8e53aeff
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/map_branch/agent.py:138` - Do not perform function call `SummarizerAgentConfig` in argument defaults; instead, perform the call
  - ID: 4ac8be53
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/agent.py:15` - Do not perform function call `PlanAndExecuteConfig` in argument defaults; instead, perform the call
  - ID: 28103cfa
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/agent.py:123` - Do not perform function call `GraphDBRAGConfig` in argument defaults; instead, perform the call with
  - ID: 9d9ef5a3
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent/agent.py:128` - Do not perform function call `ReactAgentConfig` in argument defaults; instead, perform the call with
  - ID: df2ec026
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent/agent.py:232` - Do not perform function call `ReactAgentConfig` in argument defaults; instead, perform the call with
  - ID: 60926c77
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent/agent.py:237` - Do not perform function call `ReactAgentConfig` in argument defaults; instead, perform the call with
  - ID: 7fdff488
- ... and 5 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/vectorstore/base.py:123` - Do not perform function call `HuggingFaceEmbeddingConfig` in argument defaults; instead, perform the
  - ID: 7bb5709b
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/vectorstore/base.py:136` - Do not perform function call `HuggingFaceEmbeddingConfig` in argument defaults; instead, perform the
  - ID: 085c8f7e
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/vectorstore/base.py:159` - Do not perform function call `HuggingFaceEmbeddingConfig` in argument defaults; instead, perform the
  - ID: a4dcd96d
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/vectorstore/base.py:171` - Do not perform function call `HuggingFaceEmbeddingConfig` in argument defaults; instead, perform the
  - ID: db067dde
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/vectorstore/base.py:183` - Do not perform function call `HuggingFaceEmbeddingConfig` in argument defaults; instead, perform the
  - ID: 6e8c581b

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/router.py:66` - Do not perform function call `Body` in argument defaults; instead, perform the call within the funct
  - ID: a8139218
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/router.py:67` - Do not perform function call `Body` in argument defaults; instead, perform the call within the funct
  - ID: ce0770ee
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/router.py:95` - Do not perform function call `Body` in argument defaults; instead, perform the call within the funct
  - ID: 2dda3fc3
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/router.py:125` - Do not perform function call `Body` in argument defaults; instead, perform the call within the funct
  - ID: 2946c8ee
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/router.py:127` - Do not perform function call `Body` in argument defaults; instead, perform the call within the funct
  - ID: c4fec763
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/router.py:171` - Do not perform function call `Body` in argument defaults; instead, perform the call within the funct
  - ID: 19f71cec
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/auth/dependencies.py:67` - Do not perform function call `Depends` in argument defaults; instead, perform the call within the fu
  - ID: c82cc2c9
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/auth/dependencies.py:68` - Do not perform function call `Depends` in argument defaults; instead, perform the call within the fu
  - ID: 006f0c79
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/auth/middleware.py:29` - Do not perform function call `Depends` in argument defaults; instead, perform the call within the fu
  - ID: 25adc907
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/auth/supabase.py:76` - Do not perform function call `Depends` in argument defaults; instead, perform the call within the fu
  - ID: 92286060
- ... and 7 more

### haive-games

- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/blackjack/agent.py:19` - Do not perform function call `BlackjackAgentConfig` in argument defaults; instead, perform the call
  - ID: 7bf04e18
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/bs/agent.py:21` - Do not perform function call `BullshitAgentConfig` in argument defaults; instead, perform the call w
  - ID: 1d5678b1
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/aug_llms.py:114` - Do not perform function call `AzureLLMConfig` in argument defaults; instead, perform the call within
  - ID: b9b428c5
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/aug_llms.py:115` - Do not perform function call `DeepSeekLLMConfig` in argument defaults; instead, perform the call wit
  - ID: 19ba3f5e
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/agent.py:148` - Do not perform function call `ClueConfig` in argument defaults; instead, perform the call within the
  - ID: 87dc776e
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/agent.py:102` - Do not perform function call `FoxAndGeeseConfig` in argument defaults; instead, perform the call wit
  - ID: 22d4edec
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/agent_original.py:84` - Do not perform function call `MancalaConfig` in argument defaults; instead, perform the call within
  - ID: f9b0f0b6
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/agent.py:82` - Do not perform function call `MastermindConfig` in argument defaults; instead, perform the call with
  - ID: c3c2c1c1
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/agent.py:82` - Do not perform function call `NimConfig` in argument defaults; instead, perform the call within the
  - ID: feb5e02d
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/agent.py:61` - Do not perform function call `PokerAgentConfig` in argument defaults; instead, perform the call with
  - ID: 3a5042e2
- ... and 3 more

## ruff:B009 (4 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/models.py:177` - Do not call `getattr` with a constant attribute value. It is not any safer than normal property acce
  - ID: ab492ac6
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/models.py:187` - Do not call `getattr` with a constant attribute value. It is not any safer than normal property acce
  - ID: 4660a28b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/models.py:210` - Do not call `getattr` with a constant attribute value. It is not any safer than normal property acce
  - ID: e01a3742
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/models.py:213` - Do not call `getattr` with a constant attribute value. It is not any safer than normal property acce
  - ID: ade047a8

## ruff:B018 (9 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/archive/multi_agent_v4.py:176` - Found useless attribute access. Either assign it to a variable or remove it.
  - ID: b09bf909
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced/multi_agent_v4.py:715` - Found useless attribute access. Either assign it to a variable or remove it.
  - ID: 899d69d5
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_v4.py:669` - Found useless attribute access. Either assign it to a variable or remove it.
  - ID: 2c0da475
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/multi_agent_v4.py:176` - Found useless attribute access. Either assign it to a variable or remove it.
  - ID: 1ce96bf9
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/nodes.py:90` - Found useless expression. Either assign it to a variable or remove it.
  - ID: 90b5f14b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v3/example.py:254` - Found useless attribute access. Either assign it to a variable or remove it.
  - ID: 6f605541
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/message_transformer.py:535` - Found useless attribute access. Either assign it to a variable or remove it.
  - ID: 2dd6b38e

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/types/dynamic_literal.py:51` - Found useless attribute access. Either assign it to a variable or remove it.
  - ID: 46ca11cf
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/debug/interactive.py:80` - Found useless attribute access. Either assign it to a variable or remove it.
  - ID: c4542e31

## ruff:B020 (1 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler/output_parser.py:113` - Loop control variable `thought` overrides iterable it iterates
  - ID: 477b88a7

## ruff:B021 (3 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/dynamic_react_agent.py:838` - f-string used as docstring. Python will interpret this as a joined string, rather than a docstring.
  - ID: c0181f84
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/dynamic_react_agent.v2.py:845` - f-string used as docstring. Python will interpret this as a joined string, rather than a docstring.
  - ID: ae9716ab

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/retriever.py:450` - f-string used as docstring. Python will interpret this as a joined string, rather than a docstring.
  - ID: ed3f8d3a

## ruff:B023 (12 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/routing_agent.py:89` - Function definition does not bind loop variable `source`
  - ID: b1be830a
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/routing_agent.py:91` - Function definition does not bind loop variable `source`
  - ID: df1ac40f
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/routing_agent.py:94` - Function definition does not bind loop variable `conditions`
  - ID: 1afa0216

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py:2147` - Function definition does not bind loop variable `is_validation_node`
  - ID: 622e6c58

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/base.py:336` - Function definition does not bind loop variable `tool_config`
  - ID: a97f009b
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/llm_routes.py:312` - Function definition does not bind loop variable `tool_config`
  - ID: 8247ab8d
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/llm_routes.py:451` - Function definition does not bind loop variable `tool_config`
  - ID: 4d55c88c
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/base.py:336` - Function definition does not bind loop variable `tool_config`
  - ID: f9ee443d
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/utils/vault_migration_script.py:567` - Function definition does not bind loop variable `api_key_patterns`
  - ID: 573267bd
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/utils/vault_migration_script.py:569` - Function definition does not bind loop variable `api_keys`
  - ID: 89370753
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/utils/vault_migration_script.py:567` - Function definition does not bind loop variable `api_key_patterns`
  - ID: b7317d8a
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/utils/vault_migration_script.py:569` - Function definition does not bind loop variable `api_keys`
  - ID: 6ba95145

## ruff:B024 (1 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/base_component.py:14` - `BaseGraphComponent` is an abstract base class, but it has no abstract methods or properties
  - ID: 38d0a55e

## ruff:B025 (1 errors)

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes.py:236` - try-except block with duplicate exception `ImportError`
  - ID: 2c7bdb0e

## ruff:B904 (287 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/__init__.py:281` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 6eebcc18
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/base/example.py:160` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: c50b3894
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler/tools/math_tools.py:88` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: f8804632
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo/models/tool_step.py:128` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 72430453
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/sequential_agent.py:245` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 08c6e12f
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/examples/run_from_file.py:45` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 46992f5c

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/documents/github_repo.py:174` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 2b8dd495
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/named_list.py:254` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 64a90fa0
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py:1213` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: a9ca9849
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:1300` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: b7b2d48d
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/base.py:315` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: e3772c56
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/base_new.py:167` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: d09d90f5
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/base_new.py:239` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 2e395de1
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/transformers/base.py:216` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 42143b80
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/transformers/base.py:222` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: b11af126
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/transformers/engine.py:436` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 4139808e
- ... and 154 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/base.py:364` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: ca145df1
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/connect4_api.py:133` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 82a42e1e
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/connect4_api.py:162` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 9fda64a1
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/connect4_api.py:186` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 072bed1c
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/connect4_api.py:210` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 7cf76b3d
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/connect4_api.py:222` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: de49ecc6
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_agent.py:362` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 37eafce7
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_agent.py:385` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 7930cf52
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_agent.py:408` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 2782286f
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_agent.py:419` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 255686a7
- ... and 72 more

### haive-games

- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/api_example.py:154` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 806feae2
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate/models.py:207` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 5a219074
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/go/go_engine.py:77` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: e18f0752
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/config.py:113` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: d5fc5863
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/config.py:151` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 0e7d7e21
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/config.py:290` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 6ee48b00
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/config.py:329` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 646fb03f
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/game_agent.py:170` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 051997b1
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/game_agent.py:389` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: b8e183df
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/game_agent.py:485` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: e0d3cea7
- ... and 12 more

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/config.py:303` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 4e9b5363
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mcp_rag_agent.py:338` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 7842f3fc
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mcp_simple_rag_agent.py:581` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 5cf79406
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mcp_simple_tool_agent.py:453` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 2bc0f142
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/simple_rag_mcp_agent.py:343` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 0efc9e47

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/function_logging_transformer.py:118` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: ee14ab50
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/complexity_analyzer.py:202` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 90f1395e
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/permission.py:195` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: d5b42adb
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/permission.py:228` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: a2ffc184
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/permission.py:230` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 369b2622
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/permission.py:234` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 1cba9dd0
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/google_calendar.py:104` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: 5999ba8a
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/wolfram_alpha_tool.py:52` - Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to di
  - ID: f30e037e

## ruff:C901 (215 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:215` - `update_scratchpad` is too complex (18 > 12)
  - ID: 5b75a6b7
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:538` - `tool_type` is too complex (16 > 12)
  - ID: 67326a06
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:228` - `_setup_schemas` is too complex (17 > 12)
  - ID: ebb623f3
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:296` - `_auto_derive_io_schemas` is too complex (31 > 12)
  - ID: 4dbe98a0
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:453` - `create_runnable` is too complex (15 > 12)
  - ID: 4cf58d81
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:553` - `compile` is too complex (15 > 12)
  - ID: 730199ff
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent_structured_output_mixin.py:184` - `ensure_structured_output` is too complex (14 > 12)
  - ID: d99c1b85
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/enhanced_agent.py:210` - `_auto_derive_io_schemas` is too complex (14 > 12)
  - ID: 3b7b6e3f
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/enhanced_agent.py:253` - `_setup_schemas` is too complex (14 > 12)
  - ID: 8fc10d7b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/execution_mixin.py:35` - `_prepare_input` is too complex (49 > 12)
  - ID: ff1c77d2
- ... and 114 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/connect4_api.py:87` - `_register_connect4_routes` is too complex (21 > 12)
  - ID: 2277c0cc
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_agent.py:321` - `_register_routes` is too complex (21 > 12)
  - ID: 51e753b2
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_api.py:144` - `_register_routes` is too complex (16 > 12)
  - ID: 5f1372e9
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router.py:48` - `discover_game_agents` is too complex (20 > 12)
  - ID: 261951a9
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router.py:243` - `create_game_router` is too complex (21 > 12)
  - ID: 8ec8b9b8
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router.py:252` - `game_websocket` is too complex (18 > 12)
  - ID: 677aa460
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router_fixed.py:39` - `discover_game_agents` is too complex (15 > 12)
  - ID: aa5b6974
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router_fixed.py:215` - `create_game_router` is too complex (21 > 12)
  - ID: 568c4bcf
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router_fixed.py:226` - `game_websocket` is too complex (18 > 12)
  - ID: 57025aee
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/general_games_api.py:149` - `_import_game` is too complex (15 > 12)
  - ID: e16bab00
- ... and 71 more

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:209` - `_create_discovery_tools` is too complex (13 > 12)
  - ID: bfd0df60
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:496` - `arun` is too complex (14 > 12)
  - ID: dbc89587
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/comprehensive_mcp_web.py:182` - `perform_advanced_search` is too complex (14 > 12)
  - ID: 686c0cb2
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/discovery/analyzer.py:309` - `discover_from_directory` is too complex (14 > 12)
  - ID: b85b4f47
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/discovery.py:574` - `determine_template` is too complex (13 > 12)
  - ID: c327a025
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/fastmcp_runner.py:274` - `run_command` is too complex (21 > 12)
  - ID: e34ab77f
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/integrated_mcp_system.py:58` - `detect_package_manager` is too complex (13 > 12)
  - ID: 06ddacf3
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mcp_simple_rag_agent.py:442` - `ask_agent` is too complex (22 > 12)
  - ID: 851c0e47
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/tools/server_selector.py:177` - `filter_by_multiple_criteria` is too complex (13 > 12)
  - ID: ad0fc398
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/tools/server_selector.py:482` - `interactive_select` is too complex (14 > 12)
  - ID: f23aea9f

## ruff:DTZ001 (2 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_processing/examples/comprehensive_query_example.py:325` - `datetime.datetime()` called without a `tzinfo` argument
  - ID: 46570f21
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_processing/examples/comprehensive_query_example.py:326` - `datetime.datetime()` called without a `tzinfo` argument
  - ID: 40c1c745

## ruff:DTZ003 (86 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/core/stores.py:84` - `datetime.datetime.utcnow()` used
  - ID: 3a3a606e
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/core/stores.py:238` - `datetime.datetime.utcnow()` used
  - ID: f90f150c
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/core/stores.py:373` - `datetime.datetime.utcnow()` used
  - ID: 90218647
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/core/stores.py:406` - `datetime.datetime.utcnow()` used
  - ID: a3cebb2c
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/core/stores.py:411` - `datetime.datetime.utcnow()` used
  - ID: 92843845
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/core/stores.py:436` - `datetime.datetime.utcnow()` used
  - ID: 667fd6f7
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/core/stores.py:443` - `datetime.datetime.utcnow()` used
  - ID: 4499ed15
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/core/stores.py:488` - `datetime.datetime.utcnow()` used
  - ID: 377059a8
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/core/stores.py:518` - `datetime.datetime.utcnow()` used
  - ID: d32ca354
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/core/stores.py:543` - `datetime.datetime.utcnow()` used
  - ID: 0262e911
- ... and 71 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:284` - `datetime.datetime.utcnow()` used
  - ID: e5522a46
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:286` - `datetime.datetime.utcnow()` used
  - ID: 44052fe4
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:331` - `datetime.datetime.utcnow()` used
  - ID: 05dfcf05
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:410` - `datetime.datetime.utcnow()` used
  - ID: 6fcae7b9
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:535` - `datetime.datetime.utcnow()` used
  - ID: 06a4b2cb

## ruff:DTZ005 (628 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:707` - `datetime.datetime.now()` called without a `tz` argument
  - ID: 97d269f5
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/state_mixin.py:61` - `datetime.datetime.now()` called without a `tz` argument
  - ID: 60c04a9f
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain_agent.py:89` - `datetime.datetime.now()` called without a `tz` argument
  - ID: 848a799b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_processing/agent.py:393` - `datetime.datetime.now()` called without a `tz` argument
  - ID: fad1cabf
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_processing/agent.py:421` - `datetime.datetime.now()` called without a `tz` argument
  - ID: de26673b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_processing/agent.py:492` - `datetime.datetime.now()` called without a `tz` argument
  - ID: 45bf019c
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_processing/agent.py:544` - `datetime.datetime.now()` called without a `tz` argument
  - ID: 11543be8
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_processing/agent.py:578` - `datetime.datetime.now()` called without a `tz` argument
  - ID: 8315ea6e
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_processing/agent.py:707` - `datetime.datetime.now()` called without a `tz` argument
  - ID: 40027db2
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_processing/examples/comprehensive_query_example.py:113` - `datetime.datetime.now()` called without a `tz` argument
  - ID: a4b32b10
- ... and 330 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:355` - `datetime.datetime.now()` called without a `tz` argument
  - ID: 8e5b71cf
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:516` - `datetime.datetime.now()` called without a `tz` argument
  - ID: 5f712fef
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:572` - `datetime.datetime.now()` called without a `tz` argument
  - ID: 75690e0f
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:798` - `datetime.datetime.now()` called without a `tz` argument
  - ID: 7e3c44e1
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/connect4_api.py:127` - `datetime.datetime.now()` called without a `tz` argument
  - ID: 9338659a
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/connect4_api.py:156` - `datetime.datetime.now()` called without a `tz` argument
  - ID: 343de84d
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/connect4_api.py:180` - `datetime.datetime.now()` called without a `tz` argument
  - ID: f0ae0257
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/connect4_api.py:204` - `datetime.datetime.now()` called without a `tz` argument
  - ID: c5ee271c
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/connect4_api.py:247` - `datetime.datetime.now()` called without a `tz` argument
  - ID: 3bb99def
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/connect4_api.py:279` - `datetime.datetime.now()` called without a `tz` argument
  - ID: 3da3f9a8
- ... and 238 more

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:410` - `datetime.datetime.now()` called without a `tz` argument
  - ID: c74331c9
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/comprehensive_mcp_web.py:594` - `datetime.datetime.now()` called without a `tz` argument
  - ID: bdeda89a
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/comprehensive_mcp_web.py:604` - `datetime.datetime.now()` called without a `tz` argument
  - ID: cc5a2d61
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/csv_viewer.py:74` - `datetime.datetime.now()` called without a `tz` argument
  - ID: 41a500a9
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/core.py:726` - `datetime.datetime.now()` called without a `tz` argument
  - ID: 2d918c87
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/core.py:729` - `datetime.datetime.now()` called without a `tz` argument
  - ID: 5ab4af43
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/core.py:748` - `datetime.datetime.now()` called without a `tz` argument
  - ID: a25affa6
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/core.py:940` - `datetime.datetime.now()` called without a `tz` argument
  - ID: 9811a7de
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/github_mass_downloader.py:298` - `datetime.datetime.now()` called without a `tz` argument
  - ID: 8a38b8a7
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/dynamic_activation_mcp.py:171` - `datetime.datetime.now()` called without a `tz` argument
  - ID: 7a560f9e
- ... and 29 more

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/logger.py:28` - `datetime.datetime.now()` called without a `tz` argument
  - ID: 81d51c6f

## ruff:DTZ901 (2 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/core/stores.py:489` - Use of `datetime.datetime.min` without timezone information
  - ID: 9ad04a9e
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/core/stores.py:495` - Use of `datetime.datetime.min` without timezone information
  - ID: 5201b209

## ruff:E402 (163 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/__init__.py:98` - Module level import not at top of file
  - ID: 0e37771f
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/__init__.py:99` - Module level import not at top of file
  - ID: ee00eb31
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/__init__.py:100` - Module level import not at top of file
  - ID: d3bbe7b2
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/__init__.py:101` - Module level import not at top of file
  - ID: 17838644
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/chain_examples.py:23` - Module level import not at top of file
  - ID: c6f8c6c6
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/task_analysis/analysis.py:40` - Module level import not at top of file
  - ID: 645a81f7
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/task_analysis/analysis.py:41` - Module level import not at top of file
  - ID: 5ef58e3e
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/base/example.py:18` - Module level import not at top of file
  - ID: b5895800
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/base/example.py:19` - Module level import not at top of file
  - ID: b4ecf481
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/base/example.py:21` - Module level import not at top of file
  - ID: 95066e01
- ... and 108 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/__init__.py:196` - Module level import not at top of file
  - ID: 05ea81c4
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/__init__.py:197` - Module level import not at top of file
  - ID: ff30db0c
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/__init__.py:198` - Module level import not at top of file
  - ID: f526682f
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/__init__.py:203` - Module level import not at top of file
  - ID: 322bdfe4
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/base.py:8` - Module level import not at top of file
  - ID: 7b8f7542
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/base.py:15` - Module level import not at top of file
  - ID: 8738dc5f
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/base.py:16` - Module level import not at top of file
  - ID: 77462884
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/base.py:17` - Module level import not at top of file
  - ID: 3c8d5723
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/base.py:18` - Module level import not at top of file
  - ID: 070c5353
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/base.py:19` - Module level import not at top of file
  - ID: 2f8fffe1
- ... and 30 more

### haive-games

- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/__init__.py:7` - Module level import not at top of file
  - ID: 6ad46606
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/__init__.py:8` - Module level import not at top of file
  - ID: 613364cf
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/__init__.py:9` - Module level import not at top of file
  - ID: 16c3a210
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/__init__.py:10` - Module level import not at top of file
  - ID: 2147a1c5
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/enhanced_example.py:273` - Module level import not at top of file
  - ID: 26af4d0f

## ruff:E501 (1250 errors)

### haive-games

- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/config.py:207` - Line too long (98 > 88)
  - ID: 1aa54446
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/configurable_config.py:212` - Line too long (106 > 88)
  - ID: 88557700
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/demo.py:95` - Line too long (95 > 88)
  - ID: 5c2c6972
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/demo.py:346` - Line too long (101 > 88)
  - ID: 48e1c04a
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/demo.py:499` - Line too long (106 > 88)
  - ID: bfaacbaf
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/demo.py:591` - Line too long (106 > 88)
  - ID: 6e3e6b75
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/demo.py:744` - Line too long (95 > 88)
  - ID: f6d75576
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/demo.py:1065` - Line too long (128 > 88)
  - ID: 753ac133
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/demo.py:1111` - Line too long (108 > 88)
  - ID: 000f247b
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/enhanced_ui.py:152` - Line too long (89 > 88)
  - ID: c6f80a0e
- ... and 1240 more

## ruff:E721 (28 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/composer/update_functions.py:201` - Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
  - ID: a1f8e131
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/composer/update_functions.py:203` - Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
  - ID: 0df569f5
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/composer/update_functions.py:205` - Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
  - ID: deea1ecc
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/composer/update_functions.py:207` - Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
  - ID: 034c5ab9
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/langchain_converters.py:217` - Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
  - ID: f6274351
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/langchain_converters.py:221` - Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
  - ID: 3eeac201
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/langchain_converters.py:354` - Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
  - ID: 01e6d996
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/langchain_converters.py:358` - Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
  - ID: 1464d31d
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/langchain_converters.py:368` - Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
  - ID: 31aa46b1
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/utils.py:395` - Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
  - ID: d23a1b12
- ... and 18 more

## ruff:E722 (6 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/agents/react.py:58` - Do not use bare `except`
  - ID: 0cc85af6
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/agents/react.py:478` - Do not use bare `except`
  - ID: 32b64a10
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/core/memory_tools.py:804` - Do not use bare `except`
  - ID: da262755
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/search/deep_research/agent.py:306` - Do not use bare `except`
  - ID: f78db8cd
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/patterns/react_structured_agent_variants.py:257` - Do not use bare `except`
  - ID: 0b7a1359
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/agent_v3.py:1293` - Do not use bare `except`
  - ID: c3264506

## ruff:E731 (15 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/semantic_discovery.py:31` - Do not assign a `lambda` expression, use a `def`
  - ID: fdde5104
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/semantic_discovery.py:32` - Do not assign a `lambda` expression, use a `def`
  - ID: 265635e9
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/models.py:377` - Do not assign a `lambda` expression, use a `def`
  - ID: 0c186e30
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/models.py:396` - Do not assign a `lambda` expression, use a `def`
  - ID: e1a35ee1
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/models.py:409` - Do not assign a `lambda` expression, use a `def`
  - ID: 01bec6ef
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/models.py:424` - Do not assign a `lambda` expression, use a `def`
  - ID: 4f6c70ba
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/models.py:446` - Do not assign a `lambda` expression, use a `def`
  - ID: 33dd392a
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/agents.py:527` - Do not assign a `lambda` expression, use a `def`
  - ID: acb801eb
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/agents.py:528` - Do not assign a `lambda` expression, use a `def`
  - ID: 188f84d0
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/agents.py:529` - Do not assign a `lambda` expression, use a `def`
  - ID: a8edbbad
- ... and 5 more

## ruff:E741 (13 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/base/protocols.py:12` - Ambiguous variable name: `I`
  - ID: 65a084f2
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/base/protocols.py:13` - Ambiguous variable name: `O`
  - ID: 85740b9e
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/registry.py:294` - Ambiguous variable name: `l`
  - ID: 06ffb793
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/registry.py:302` - Ambiguous variable name: `l`
  - ID: 1005792f
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/branch.py:48` - Ambiguous variable name: `O`
  - ID: 53206a6e
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/node.py:40` - Ambiguous variable name: `O`
  - ID: 07c3d8ff
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/runtime/base/base.py:13` - Ambiguous variable name: `I`
  - ID: 471bcdc9
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/runtime/base/base.py:14` - Ambiguous variable name: `O`
  - ID: 7a731927
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/runtime/base/protocols.py:10` - Ambiguous variable name: `I`
  - ID: 31702c0d
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/runtime/base/protocols.py:11` - Ambiguous variable name: `O`
  - ID: 19ecf2fd
- ... and 3 more

## ruff:ERA001 (189 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:10` - Found commented-out code
  - ID: 1fd9250c
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:761` - Found commented-out code
  - ID: 5e37d170
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:762` - Found commented-out code
  - ID: 6ee80430
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:763` - Found commented-out code
  - ID: 9b3b40f3
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:764` - Found commented-out code
  - ID: 0923e0e9
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:765` - Found commented-out code
  - ID: da8c80da
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/execution_mixin.py:594` - Found commented-out code
  - ID: 0f0f229d
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/types.py:185` - Found commented-out code
  - ID: 42951bfa
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/__init__.py:63` - Found commented-out code
  - ID: a89262cb
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/chain_examples.py:19` - Found commented-out code
  - ID: 70bcba7f
- ... and 91 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/__init__.py:49` - Found commented-out code
  - ID: 53110e46
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/__init__.py:164` - Found commented-out code
  - ID: 3cc20920
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/examples/universal_loader_demo.py:28` - Found commented-out code
  - ID: d0d790d9
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/examples/universal_loader_demo.py:29` - Found commented-out code
  - ID: 95e24405
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/examples/universal_loader_demo.py:30` - Found commented-out code
  - ID: e9bc75d0
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/base/base.py:17` - Found commented-out code
  - ID: 11a7ceb4
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/base.py:63` - Found commented-out code
  - ID: 15ee7e52
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/__init__.py:21` - Found commented-out code
  - ID: c4807fae
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/__init__.py:42` - Found commented-out code
  - ID: 1e33fcd0
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/__init__.py:56` - Found commented-out code
  - ID: 45fc56b4
- ... and 48 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/main.py:6` - Found commented-out code
  - ID: 530dcbcf
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/main.py:14` - Found commented-out code
  - ID: f6fd0782
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registries/model_registry.py:1064` - Found commented-out code
  - ID: 2a572694
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/registries/model_registry.py:1064` - Found commented-out code
  - ID: cbc30194

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/__init__.py:87` - Found commented-out code
  - ID: e737cf09
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:66` - Found commented-out code
  - ID: d17b21dc
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:205` - Found commented-out code
  - ID: f74579bb
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:206` - Found commented-out code
  - ID: 9d5e437b
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/integration.py:45` - Found commented-out code
  - ID: e0db1c19
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/installers/advanced_code_installer.py:24` - Found commented-out code
  - ID: 98e5d513
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/installers/advanced_code_installer.py:25` - Found commented-out code
  - ID: 941f3a0d
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/servers/__init__.py:6` - Found commented-out code
  - ID: f8f49cc9

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/hinge_tools.py:30` - Found commented-out code
  - ID: 8d09cb00
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/hinge_tools.py:33` - Found commented-out code
  - ID: 46bb26d3
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/hinge_tools.py:34` - Found commented-out code
  - ID: 8fd3780b
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/hinge_tools.py:37` - Found commented-out code
  - ID: 6a959d7e
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/import_consolidator.py:93` - Found commented-out code
  - ID: e46579a2
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/multi_file_rename.py:114` - Found commented-out code
  - ID: a90036a7
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/print_to_logging.py:84` - Found commented-out code
  - ID: c9c81169
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/automatic_test_case_generator.py:113` - Found commented-out code
  - ID: c26836b4
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/code_smell_detector.py:103` - Found commented-out code
  - ID: bd2f39d2
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/dependency_analyzer.py:109` - Found commented-out code
  - ID: e91f222c
- ... and 8 more

## ruff:F401 (225 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:8` - `typing.Generic` imported but unused
  - ID: 282c5b42
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:8` - `typing.Generic` imported but unused
  - ID: 282c5b42
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:18` - `haive.core.graph.node.output_parsing_v2.PydanticParserNodeConfig` imported but unused
  - ID: e75ee333
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:19` - `haive.core.graph.node.output_parsing_v2.create_pydantic_parser_node` imported but unused
  - ID: f2efdbc7
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/declarative_chain.py:9` - `pydantic.BaseModel` imported but unused
  - ID: 00da3ab9
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/extended_chain.py:9` - `typing.Union` imported but unused
  - ID: 98de4e07
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/extended_chain.py:10` - `abc.ABC` imported but unused
  - ID: 48246f1e
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/extended_chain.py:10` - `abc.ABC` imported but unused
  - ID: 48246f1e
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/extended_chain.py:13` - `langchain_core.messages.BaseMessage` imported but unused
  - ID: 9c62ca51
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/extended_chain.py:14` - `langchain_core.prompts.ChatPromptTemplate` imported but unused
  - ID: da0e55d2
- ... and 136 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/__init__.py:58` - `pkgutil` imported but unused
  - ID: 19c4c4b6
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/__init__.py:65` - `haive.core.engine.aug_llm.AugLLMFactory` imported but unused; consider removing, adding to `**all**
  - ID: 668e1910
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/__init__.py:66` - `haive.core.engine.aug_llm.compose_runnable` imported but unused; consider removing, adding to `\_\_al
  - ID: 9280f9d2
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/__init__.py:67` - `haive.core.engine.aug_llm.merge_configs` imported but unused; consider removing, adding to `**all**
  - ID: 70967381
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/__init__.py:74` - `haive.core.engine.base.NonInvokableEngine` imported but unused; consider removing, adding to `\_\_all
  - ID: 149cc672
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/__init__.py:87` - `haive.core.engine.tool.ToolEngine` imported but unused; consider removing, adding to `__all__`, or
  - ID: b6992abb
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/database_sources.py:13` - `pydantic.validator` imported but unused
  - ID: 67147bad
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/specialized_sources.py:15` - `pydantic.validator` imported but unused
  - ID: ef399e6e
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/AzureOpenAIEmbeddingConfig.py:6` - `pydantic.validator` imported but unused
  - ID: f467db51
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/CohereEmbeddingConfig.py:5` - `pydantic.validator` imported but unused
  - ID: 3aeaeca1
- ... and 39 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registries/model_registry.py:63` - `haive.dataflow.importers.embeddings_importer.import_embedding_models` imported but unused; consider
  - ID: 757a75c2
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registries/model_registry.py:75` - `haive.dataflow.importers.litellm_importer.import_llm_models` imported but unused; consider using `i
  - ID: 51031b17
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/registries/model_registry.py:63` - `haive.dataflow.importers.embeddings_importer.import_embedding_models` imported but unused; consider
  - ID: 0e75f419
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/registries/model_registry.py:75` - `haive.dataflow.importers.litellm_importer.import_llm_models` imported but unused; consider using `i
  - ID: 8a9164ea

### haive-games

- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/config/__init__.py:4` - `haive.games.core.config.base.BaseGameConfig` imported but unused; consider removing, adding to `\_\_a
  - ID: d680b69a
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/config/__init__.py:5` - `haive.games.core.config.base.ConfigMode` imported but unused; consider removing, adding to `**all**
  - ID: 78471152
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/config/__init__.py:6` - `haive.games.core.config.base.GamePlayerRole` imported but unused; consider removing, adding to `\_\_a
  - ID: c4e2f444
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/config/__init__.py:7` - `haive.games.core.config.base.create_advanced_config` imported but unused; consider removing, adding
  - ID: 0ab34517
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/config/__init__.py:8` - `haive.games.core.config.base.create_example_config` imported but unused; consider removing, adding
  - ID: 821fc7a5
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/config/__init__.py:9` - `haive.games.core.config.base.create_llm_config` imported but unused; consider removing, adding to `
  - ID: a053f854
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/config/__init__.py:10` - `haive.games.core.config.base.create_simple_config` imported but unused; consider removing, adding t
  - ID: 6bfe68b3
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/__init__.py:3` - `haive.games.debate_v2.agent.GameDebateAgent` imported but unused; consider removing, adding to `\_\_a
  - ID: abbde084
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/reversi/state.py:16` - `haive.games.reversi.state_manager.ReversiStateManager` imported but unused
  - ID: febf7b31
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/utils/__init__.py:4` - `haive.games.utils.recursion_config.RecursionConfig` imported but unused; consider removing, adding
  - ID: b7bf3610
- ... and 3 more

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/fastapi_mcp_server.py:708` - `fastmcp` imported but unused; consider using `importlib.util.find_spec` to test for availability
  - ID: babea391
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/integrated_launcher.py:23` - `streamlit` imported but unused; consider using `importlib.util.find_spec` to test for availability
  - ID: b47a7988
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/integrated_launcher.py:28` - `plotly` imported but unused; consider using `importlib.util.find_spec` to test for availability
  - ID: 2ce53e9e
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/integrated_launcher.py:33` - `pandas` imported but unused; consider using `importlib.util.find_spec` to test for availability
  - ID: 9f65e781
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/integrated_launcher.py:38` - `aiohttp` imported but unused; consider using `importlib.util.find_spec` to test for availability
  - ID: 442526bb
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/integrated_launcher.py:43` - `psutil` imported but unused; consider using `importlib.util.find_spec` to test for availability
  - ID: feaa4273
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/tools/server_tester.py:213` - `langchain_mcp_adapters.MCPAdapter` imported but unused; consider using `importlib.util.find_spec` t
  - ID: 8681e844

### haive-prebuilt

- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/misc/agent_utilities_prompts.py:7` - `typing.List` imported but unused
  - ID: a71736ae
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/simple/questiona_and_answer_generator/models.py:1` - `pydantic.BaseModel` imported but unused
  - ID: 63c3a8d7
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/simple/questiona_and_answer_generator/models.py:2` - `typing.List` imported but unused
  - ID: 8eca9555
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/simple/questiona_and_answer_generator/models.py:2` - `typing.List` imported but unused
  - ID: 8eca9555
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/simple/tagger/prompts.py:1` - `langchain_core.prompts.ChatPromptTemplate` imported but unused
  - ID: 75aaa439
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/simple/tagger/prompts.py:1` - `langchain_core.prompts.ChatPromptTemplate` imported but unused
  - ID: 75aaa439

## ruff:F402 (3 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v2/agent.py:294` - Import `tool` from line 9 shadowed by loop variable
  - ID: 1716d584
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/clean_dynamic_supervisor.py:211` - Import `tool` from line 15 shadowed by loop variable
  - ID: babaee1c
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic/dynamic_supervisor.py:284` - Import `tool` from line 88 shadowed by loop variable
  - ID: f21a5f9d

## ruff:F403 (7 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/__init__.py:12` - `from .models import *` used; unable to detect undefined names
  - ID: 66bfaa30
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/agent.py:2` - `from haive.core.engine.aug_llm import *` used; unable to detect undefined names
  - ID: 21d1d45b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/agent.py:7` - `from haive.agents.planning.plan_and_execute.engines import *` used; unable to detect undefined name
  - ID: 7f6a0fd7
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/agent.py:8` - `from haive.agents.planning.plan_and_execute.models import *` used; unable to detect undefined names
  - ID: bba23b52
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/agent.py:9` - `from haive.agents.planning.plan_and_execute.state import *` used; unable to detect undefined names
  - ID: d74b3440
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/factories/rag_workflow_factory.py:12` - `from haive.core.graph.node.rag_callables import *` used; unable to detect undefined names
  - ID: aab5c4ae

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/routers/test.py:1` - `from haive.core.graph.routers.conditions import *` used; unable to detect undefined names
  - ID: 24904b09

## ruff:F405 (54 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/compatibility.py:7` - `MultiAgent` may be undefined, or defined from star imports
  - ID: 2830eb43
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/compatibility.py:8` - `BaseMultiAgent` may be undefined, or defined from star imports
  - ID: 4f2820e1
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/compatibility.py:9` - `ExecutionMode` may be undefined, or defined from star imports
  - ID: e6801520
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/compatibility.py:10` - `SequentialAgent` may be undefined, or defined from star imports
  - ID: b609444a
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/compatibility.py:11` - `ParallelAgent` may be undefined, or defined from star imports
  - ID: 8261e3cf
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/compatibility.py:12` - `ConditionalAgent` may be undefined, or defined from star imports
  - ID: 443b9513
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/compatibility.py:13` - `BranchAgent` may be undefined, or defined from star imports
  - ID: 3a04424c
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/__init__.py:17` - `IntelligentStatusMixin` may be undefined, or defined from star imports
  - ID: f67cef84
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/__init__.py:18` - `IntelligentSequence` may be undefined, or defined from star imports
  - ID: 2054a24f
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/__init__.py:19` - `BaseStep` may be undefined, or defined from star imports
  - ID: 8bcebbb7
- ... and 43 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/routers/test.py:3` - `StateValueCondition` may be undefined, or defined from star imports
  - ID: 5f88bfe3

## ruff:F541 (2 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/static.py:1017` - f-string without any placeholders
  - ID: 4f1eb17e
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/static.py:1042` - f-string without any placeholders
  - ID: 9d953954

## ruff:F811 (170 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/enhanced_agent.py:26` - Redefinition of unused `TypeVar` from line 17
  - ID: fde52a3e
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/multi_integration.py:165` - Redefinition of unused `multi_to_chain` from line 100
  - ID: be8693a0
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/multi_integration.py:169` - Redefinition of unused `chain_to_multi` from line 95
  - ID: 0b1ccb33
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/task_analysis/__init__.py:27` - Redefinition of unused `ExecutionStrategy` from line 5
  - ID: 0f10b804
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/social_media/__init__.py:16` - Redefinition of unused `SocialMediaState` from line 15
  - ID: 2450f2ab
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/__init__.py:33` - Redefinition of unused `ToolSelectionStrategy` from line 13
  - ID: ab3357dc
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/__init__.py:18` - Redefinition of unused `RetryStrategy` from line 12
  - ID: bf431c14
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/agent.py:10` - Redefinition of unused `Send` from line 8
  - ID: 60749d1a
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/utils.py:9` - Redefinition of unused `GraphDocument` from line 7
  - ID: d0655eb5
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/map_branch/agent.py:58` - Redefinition of unused `Send` from line 56
  - ID: a278f935
- ... and 91 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/__init__.py:196` - Redefinition of unused `AugLLMConfig` from line 64
  - ID: d5ba4693
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/__init__.py:197` - Redefinition of unused `Engine` from line 70
  - ID: 286a11b3
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/__init__.py:197` - Redefinition of unused `Engine` from line 70
  - ID: 286a11b3
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/__init__.py:197` - Redefinition of unused `Engine` from line 70
  - ID: 286a11b3
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/__init__.py:197` - Redefinition of unused `Engine` from line 70
  - ID: 286a11b3
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/__init__.py:203` - Redefinition of unused `OutputParserEngine` from line 81
  - ID: 583b1cf7
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/__init__.py:203` - Redefinition of unused `OutputParserEngine` from line 81
  - ID: 583b1cf7
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:1602` - Redefinition of unused `add_prompt_template` from line 1222
  - ID: 5e19a3e7
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:1679` - Redefinition of unused `add_tool` from line 1231
  - ID: ad22e2f1
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:1694` - Redefinition of unused `remove_tool` from line 1243
  - ID: 6b256938
- ... and 16 more

### haive-games

- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/agent.py:699` - Redefinition of unused `analyze_position` from line 310
  - ID: bb4b31fa
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/__init__.py:26` - Redefinition of unused `Config` from line 5
  - ID: e581b986
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/__init__.py:46` - Redefinition of unused `get_property` from line 13
  - ID: 80c614d9
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/__init__.py:60` - Redefinition of unused `set_property` from line 21
  - ID: 884a7da9
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/__init__.py:71` - Redefinition of unused `Config` from line 26
  - ID: e3102de0
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/__init__.py:92` - Redefinition of unused `Config` from line 71
  - ID: d8f6b1cc
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/__init__.py:98` - Redefinition of unused `coordinates` from line 78
  - ID: 205d3393
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/__init__.py:100` - Redefinition of unused `get_property` from line 46
  - ID: 438f3ffd
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/__init__.py:103` - Redefinition of unused `place_piece` from line 19
  - ID: 1ba2d58e
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/__init__.py:105` - Redefinition of unused `remove_piece` from line 20
  - ID: 3a0a7568
- ... and 5 more

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/__init__.py:46` - Redefinition of unused `DockerInstaller` from line 27
  - ID: e8cae22c
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/__init__.py:47` - Redefinition of unused `GeneralMCPDownloader` from line 14
  - ID: bf47b71a
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/__init__.py:48` - Redefinition of unused `GitInstaller` from line 28
  - ID: 51ad383a
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/__init__.py:49` - Redefinition of unused `InstallationMethod` from line 6
  - ID: ca6b5a45
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/__init__.py:50` - Redefinition of unused `MCPInstaller` from line 29
  - ID: fd076984
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/__init__.py:51` - Redefinition of unused `NPMInstaller` from line 30
  - ID: 59fcd87a
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/__init__.py:52` - Redefinition of unused `PipInstaller` from line 31
  - ID: f0faa2f6
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/__init__.py:53` - Redefinition of unused `ServerConfig` from line 7
  - ID: e86ee07d
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/__init__.py:54` - Redefinition of unused `ServerTemplate` from line 8
  - ID: dbe40dcc
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/__init__.py:56` - Redefinition of unused `load_config` from line 9
  - ID: a364cfe3
- ... and 1 more

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/__init__.py:18` - Redefinition of unused `from_config` from line 12
  - ID: 821f4b8a
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/__init__.py:19` - Redefinition of unused `get_tools` from line 13
  - ID: 4ac67586
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/__init__.py:32` - Redefinition of unused `get_tools` from line 19
  - ID: dc67b67f
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/__init__.py:53` - Redefinition of unused `get_tools` from line 32
  - ID: 900ac0f9
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/__init__.py:63` - Redefinition of unused `get_tools` from line 53
  - ID: f11930a9
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/__init__.py:82` - Redefinition of unused `get_tools` from line 63
  - ID: fd3adfa7
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/__init__.py:89` - Redefinition of unused `create_llm` from line 11
  - ID: 751701fa
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/__init__.py:90` - Redefinition of unused `from_config` from line 18
  - ID: 3cbb73ea
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/__init__.py:91` - Redefinition of unused `get_tools` from line 82
  - ID: f1440995
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/__init__.py:102` - Redefinition of unused `AuthorSearchInput` from line 94
  - ID: 04090fdd
- ... and 7 more

## ruff:F821 (727 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:768` - Undefined name `config`
  - ID: b378ced1
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/compiled_agent.py:61` - Undefined name `cls`
  - ID: 02712ce3
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/compiled_agent.py:62` - Undefined name `cls`
  - ID: 5214ac04
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/compiled_agent.py:64` - Undefined name `cls`
  - ID: 4d375f51
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/compiled_agent.py:66` - Undefined name `cls`
  - ID: 3c3c93b2
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/compiled_agent.py:68` - Undefined name `cls`
  - ID: a5d099c9
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/compiled_agent.py:69` - Undefined name `cls`
  - ID: 88f5074e
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/compiled_agent.py:70` - Undefined name `cls`
  - ID: 91308b3d
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/compiled_agent.py:71` - Undefined name `cls`
  - ID: c377faa6
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/universal_agent.py:131` - Undefined name `is_reasoning_agent`
  - ID: c2293814
- ... and 410 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/auto_loader.py:1003` - Undefined name `Dict`
  - ID: 4d66d673
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/examples/minimal_example.py:26` - Undefined name `Any`
  - ID: 72fedcd2
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/path_analyzer.py:140` - Undefined name `LoaderCapability`
  - ID: 653ca979
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/chat/base.py:1` - Undefined name `BaseSource`
  - ID: a9a2ea45
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/database_sources.py:207` - Undefined name `field_validator`
  - ID: 54e8b8c5
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/factory.py:87` - Undefined name `SourceType`
  - ID: 1338029a
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/factory.py:114` - Undefined name `SourceType`
  - ID: b7dbe5cc
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/factory.py:125` - Undefined name `SourceType`
  - ID: 4c4b4687
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/factory.py:126` - Undefined name `SourceType`
  - ID: e28edf90
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/factory.py:127` - Undefined name `SourceType`
  - ID: b450cf81
- ... and 150 more

### haive-games

- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/demo.py:1200` - Undefined name `Progress`
  - ID: 94715e75
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/demo.py:1201` - Undefined name `SpinnerColumn`
  - ID: f7f38567
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/demo.py:1202` - Undefined name `TextColumn`
  - ID: 7ade0eb0
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/api/setup.py:126` - Undefined name `ChessAgent`
  - ID: e2b3f256
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base/utils.py:23` - Undefined name `GameAgent`
  - ID: 1bd41f03
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/generic_engines.py:293` - Undefined name `Any`
  - ID: 8571b8d2
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/example_configurable.py:74` - Undefined name `ChessAgent`
  - ID: 60154f6c
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/example_configurable.py:149` - Undefined name `ChessAgent`
  - ID: 80b6735e
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/generic_engines.py:102` - Undefined name `current_board_fen`
  - ID: 8ba366ea
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/generic_engines.py:104` - Undefined name `recent_moves`
  - ID: 5b94aabf
- ... and 131 more

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:546` - Undefined name `discover_mcp_servers`
  - ID: 2d0d128c
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:560` - Undefined name `install_mcp_server`
  - ID: 84320b35
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/integration.py:112` - Undefined name `StdioServerParameters`
  - ID: 83c3b6c5
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/integration.py:118` - Undefined name `stdio_client`
  - ID: 92f0f3f5
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/integration.py:124` - Undefined name `SSEConnection`
  - ID: 0ce057f2

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/logger.py:49` - Undefined name `SecureShellExecutor`
  - ID: 45a56669

## ruff:F822 (28 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute_multi.py:85` - Undefined name `create_plan_and_execute_agent` in `__all__`
  - ID: 82f1d01f
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/models.py:326` - Undefined name `QueryValidationOutput` in `__all__`
  - ID: dacd0ece
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/models.py:327` - Undefined name `DomainRelevanceOutput` in `__all__`
  - ID: ae47b983
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/factories/compatible_rag_factory.py:1451` - Undefined name `CompatibleRAGFactory.create_agentic_search_workflow` in `__all__`
  - ID: c4890b85
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/factories/compatible_rag_factory.py:1452` - Undefined name `CompatibleRAGFactory.create_decomposed_graded_workflow` in `__all__`
  - ID: c8813790
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/factories/compatible_rag_factory.py:1453` - Undefined name `CompatibleRAGFactory.create_full_pipeline_workflow` in `__all__`
  - ID: 27f13bb7
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/factories/compatible_rag_factory.py:1455` - Undefined name `CompatibleRAGFactory.create_graded_hyde_workflow` in `__all__`
  - ID: 938c6394
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/factories/compatible_rag_factory.py:1456` - Undefined name `CompatibleRAGFactory.create_modular_rag_workflow` in `__all__`
  - ID: ee155c94

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/config.py:4` - Undefined name `CharacterTextSplitter` in `__all__`
  - ID: 37425cc2
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/config.py:6` - Undefined name `ElementType` in `__all__`
  - ID: 9fe0f174
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/config.py:7` - Undefined name `HTMLHeaderTextSplitter` in `__all__`
  - ID: cb4cc4dd
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/config.py:8` - Undefined name `HeaderType` in `__all__`
  - ID: 10c89c82
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/config.py:9` - Undefined name `KonlpyTextSplitter` in `__all__`
  - ID: c0962874
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/config.py:10` - Undefined name `Language` in `__all__`
  - ID: aedc0769
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/config.py:11` - Undefined name `LatexTextSplitter` in `__all__`
  - ID: 5b1d474c
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/config.py:12` - Undefined name `LineType` in `__all__`
  - ID: 1c18888b
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/config.py:13` - Undefined name `MarkdownHeaderTextSplitter` in `__all__`
  - ID: 4be99e49
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/config.py:14` - Undefined name `MarkdownTextSplitter` in `__all__`
  - ID: 3a885529
- ... and 10 more

## ruff:F841 (11 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/supervisor/tools.py:286` - Local variable `e` is assigned to but never used
  - ID: b14af48b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/labs/agent.py:827` - Local variable `agent` is assigned to but never used
  - ID: e745d739
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/models.py:938` - Local variable `e` is assigned to but never used
  - ID: 458e6fe5
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/models.py:1168` - Local variable `e` is assigned to but never used
  - ID: 84d2c913
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/enhanced_plan_execute_v6.py:354` - Local variable `base_planner` is assigned to but never used
  - ID: 6014d847

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/registry/__init__.py:106` - Local variable `e` is assigned to but never used
  - ID: 5e1ee286
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:851` - Local variable `hotspots` is assigned to but never used
  - ID: 7eb707c3
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/types.py:484` - Local variable `e` is assigned to but never used
  - ID: 1d492884

### haive-games

- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/blackjack/state_manager.py:289` - Local variable `hand_bust` is assigned to but never used
  - ID: f3bd9262
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/example.py:51` - Local variable `logger` is assigned to but never used
  - ID: b58d4cd2
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/reversi/example.py:48` - Local variable `agent` is assigned to but never used
  - ID: 1b68f690

## ruff:G002 (1 errors)

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/serve_chess_client.py:62` - Logging statement uses `%`
  - ID: c05247d6

## ruff:G004 (3320 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:363` - Logging statement uses f-string
  - ID: 46504325
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:401` - Logging statement uses f-string
  - ID: 402d83a4
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:427` - Logging statement uses f-string
  - ID: cf880e79
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:438` - Logging statement uses f-string
  - ID: b5dc024b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:535` - Logging statement uses f-string
  - ID: 6897c96c
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:605` - Logging statement uses f-string
  - ID: 95bf6ead
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:610` - Logging statement uses f-string
  - ID: c122b04b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:613` - Logging statement uses f-string
  - ID: baf7bc0b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:651` - Logging statement uses f-string
  - ID: 3bae72e9
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:670` - Logging statement uses f-string
  - ID: 36417bda
- ... and 1864 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/app.py:142` - Logging statement uses f-string
  - ID: 9f79a7d1
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/app.py:150` - Logging statement uses f-string
  - ID: c157fbbd
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/app.py:166` - Logging statement uses f-string
  - ID: 777c41ea
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/app.py:168` - Logging statement uses f-string
  - ID: 1dfae1da
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/app_dep.py:37` - Logging statement uses f-string
  - ID: 1f293c45
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:121` - Logging statement uses f-string
  - ID: 32125299
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:124` - Logging statement uses f-string
  - ID: b3a66fd3
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:125` - Logging statement uses f-string
  - ID: 60725336
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:159` - Logging statement uses f-string
  - ID: 1eb4e7e8
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:339` - Logging statement uses f-string
  - ID: c89542c7
- ... and 1209 more

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/documentation_agent.py:337` - Logging statement uses f-string
  - ID: 1658c96e
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/documentation_agent.py:373` - Logging statement uses f-string
  - ID: 9f34c62f
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:254` - Logging statement uses f-string
  - ID: 74e7fffe
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:330` - Logging statement uses f-string
  - ID: 224e5c63
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:425` - Logging statement uses f-string
  - ID: c2685ff5
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:429` - Logging statement uses f-string
  - ID: 6ed74b15
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:430` - Logging statement uses f-string
  - ID: 10a138e0
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:431` - Logging statement uses f-string
  - ID: 8fa79d83
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:483` - Logging statement uses f-string
  - ID: 5e69f7ab
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:520` - Logging statement uses f-string
  - ID: 88101dd7
- ... and 206 more

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_books.py:69` - Logging statement uses f-string
  - ID: 4090fce0
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_finance.py:69` - Logging statement uses f-string
  - ID: 889cdee3
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_jobs.py:86` - Logging statement uses f-string
  - ID: f600eda9
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_lens.py:83` - Logging statement uses f-string
  - ID: bb8376aa
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_places.py:71` - Logging statement uses f-string
  - ID: cab994d5
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_scholar.py:68` - Logging statement uses f-string
  - ID: c0f89fb3
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_search.py:71` - Logging statement uses f-string
  - ID: 71b859df
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_trends.py:60` - Logging statement uses f-string
  - ID: 7ffd955e
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/reddit_search.py:66` - Logging statement uses f-string
  - ID: fccffb1a
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1421` - Logging statement uses f-string
  - ID: 009c7a91
- ... and 1 more

## ruff:G201 (75 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/agent.py:613` - Logging `.exception(...)` should be used instead of `.error(..., exc_info=True)`
  - ID: aa53c05c
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/agent.py:825` - Logging `.exception(...)` should be used instead of `.error(..., exc_info=True)`
  - ID: d44c37ca
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_iterative_refinement/agent.py:307` - Logging `.exception(...)` should be used instead of `.error(..., exc_info=True)`
  - ID: b858eaac
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/map_branch/agent.py:243` - Logging `.exception(...)` should be used instead of `.error(..., exc_info=True)`
  - ID: 810273f4
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/map_branch/agent.py:382` - Logging `.exception(...)` should be used instead of `.error(..., exc_info=True)`
  - ID: 3516c68f
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/archive/example_delegation.py:178` - Logging `.exception(...)` should be used instead of `.error(..., exc_info=True)`
  - ID: 8f7dd116
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/archive/example_delegation.py:263` - Logging `.exception(...)` should be used instead of `.error(..., exc_info=True)`
  - ID: 70fd0859
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/archive/simple_test.py:107` - Logging `.exception(...)` should be used instead of `.error(..., exc_info=True)`
  - ID: 39867702
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/archive/simple_test.py:159` - Logging `.exception(...)` should be used instead of `.error(..., exc_info=True)`
  - ID: 55f0303f
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/archive/simple_test.py:205` - Logging `.exception(...)` should be used instead of `.error(..., exc_info=True)`
  - ID: a100db38
- ... and 7 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/app.py:150` - Logging `.exception(...)` should be used instead of `.error(..., exc_info=True)`
  - ID: 3a65146f
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/connect4_api.py:132` - Logging `.exception(...)` should be used instead of `.error(..., exc_info=True)`
  - ID: 72c516b2
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/connect4_api.py:161` - Logging `.exception(...)` should be used instead of `.error(..., exc_info=True)`
  - ID: a26a7f1a
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/connect4_api.py:185` - Logging `.exception(...)` should be used instead of `.error(..., exc_info=True)`
  - ID: c2306817
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/connect4_api.py:209` - Logging `.exception(...)` should be used instead of `.error(..., exc_info=True)`
  - ID: 539fe2f4
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/connect4_api.py:221` - Logging `.exception(...)` should be used instead of `.error(..., exc_info=True)`
  - ID: e2936bc2
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/connect4_api.py:360` - Logging `.exception(...)` should be used instead of `.error(..., exc_info=True)`
  - ID: b4cd9ad8
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_agent.py:361` - Logging `.exception(...)` should be used instead of `.error(..., exc_info=True)`
  - ID: 3b3812fb
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_agent.py:384` - Logging `.exception(...)` should be used instead of `.error(..., exc_info=True)`
  - ID: 8969c4e7
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_agent.py:407` - Logging `.exception(...)` should be used instead of `.error(..., exc_info=True)`
  - ID: 03c86b97
- ... and 48 more

## ruff:I001 (1372 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/__init__.py:52` - Import block is un-sorted or un-formatted
  - ID: 10b8c358
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/__init__.py:98` - Import block is un-sorted or un-formatted
  - ID: dd55dceb
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:1` - Import block is un-sorted or un-formatted
  - ID: caeadfbd
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/archive/meta/__init__.py:3` - Import block is un-sorted or un-formatted
  - ID: 23cbc692
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/archive/meta/agent.py:3` - Import block is un-sorted or un-formatted
  - ID: 8d2368ff
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base.py:1` - Import block is un-sorted or un-formatted
  - ID: 0b436ca3
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/__init__.py:51` - Import block is un-sorted or un-formatted
  - ID: 690638af
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:5` - Import block is un-sorted or un-formatted
  - ID: d39e85dc
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent_structured_output_mixin.py:8` - Import block is un-sorted or un-formatted
  - ID: e71238e9
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent_with_token_tracking.py:8` - Import block is un-sorted or un-formatted
  - ID: aa3d78f3
- ... and 948 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/agent_node_v2.py:1` - Import block is un-sorted or un-formatted
  - ID: 7f82d592
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/multi_agent_node.py:6` - Import block is un-sorted or un-formatted
  - ID: c52f25e8
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/supabase_config.py:22` - Import block is un-sorted or un-formatted
  - ID: 102fc8a6
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/__init__.py:110` - Import block is un-sorted or un-formatted
  - ID: f1df72b9

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/__init__.py:45` - Import block is un-sorted or un-formatted
  - ID: ba0eb6f4
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/__init___lazy.py:47` - Import block is un-sorted or un-formatted
  - ID: ded80312
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/app.py:24` - Import block is un-sorted or un-formatted
  - ID: 560c927e
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/app_dep.py:3` - Import block is un-sorted or un-formatted
  - ID: b44bb324
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:11` - Import block is un-sorted or un-formatted
  - ID: bc7af2fe
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/base.py:1` - Import block is un-sorted or un-formatted
  - ID: ca5224b1
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/connect4_api.py:1` - Import block is un-sorted or un-formatted
  - ID: b7be3cf9
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/db.py:3` - Import block is un-sorted or un-formatted
  - ID: 54c6e5b6
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_agent.py:1` - Import block is un-sorted or un-formatted
  - ID: 70ca0d51
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_api.py:15` - Import block is un-sorted or un-formatted
  - ID: da2f3d21
- ... and 102 more

### haive-games

- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/agent.py:3` - Import block is un-sorted or un-formatted
  - ID: 5905ef24
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/config.py:3` - Import block is un-sorted or un-formatted
  - ID: d916f879
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/engines.py:3` - Import block is un-sorted or un-formatted
  - ID: 7b9064f6
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/factory.py:3` - Import block is un-sorted or un-formatted
  - ID: deb7aafe
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/generic_engines.py:8` - Import block is un-sorted or un-formatted
  - ID: 939554d2
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/state_manager.py:43` - Import block is un-sorted or un-formatted
  - ID: 2814b9c3
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/api/general_api.py:9` - Import block is un-sorted or un-formatted
  - ID: 0fb9c013
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/api/setup.py:8` - Import block is un-sorted or un-formatted
  - ID: 43ac2c29
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base/agent.py:20` - Import block is un-sorted or un-formatted
  - ID: 11f9230a
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base/config.py:20` - Import block is un-sorted or un-formatted
  - ID: a0b665d1
- ... and 166 more

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/__init__.py:3` - Import block is un-sorted or un-formatted
  - ID: f3657f29
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/__init__.py:3` - Import block is un-sorted or un-formatted
  - ID: 2719425f
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/__init__.py:42` - Import block is un-sorted or un-formatted
  - ID: 9d645ad5
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/documentation_agent.py:63` - Import block is un-sorted or un-formatted
  - ID: e9c5120d
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:47` - Import block is un-sorted or un-formatted
  - ID: 3d8d1661
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/transferable_mcp_agent.py:59` - Import block is un-sorted or un-formatted
  - ID: e55e98f0
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/cli.py:16` - Import block is un-sorted or un-formatted
  - ID: fafa9dbf
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/cli/__init__.py:3` - Import block is un-sorted or un-formatted
  - ID: df7984cb
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/cli/mcp_manager.py:20` - Import block is un-sorted or un-formatted
  - ID: 38fbb410
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/complete_mcp_with_parent_retriever.py:16` - Import block is un-sorted or un-formatted
  - ID: 18d9c65d
- ... and 51 more

### haive-prebuilt

- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/ai_insight/agent.py:6` - Import block is un-sorted or un-formatted
  - ID: ac708459
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/ai_insight/state.py:6` - Import block is un-sorted or un-formatted
  - ID: 57042d61
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/company_researcher/agent.py:1` - Import block is un-sorted or un-formatted
  - ID: df1881ee
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/company_researcher/config.py:1` - Import block is un-sorted or un-formatted
  - ID: 3cf5aa88
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/content/document_extractor.py:7` - Import block is un-sorted or un-formatted
  - ID: eb0d207c
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/content/qa_for_rag.py:6` - Import block is un-sorted or un-formatted
  - ID: 81eb33bc
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/content/summarizer.py:1` - Import block is un-sorted or un-formatted
  - ID: dd0cd2c7
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/content/tagger.py:8` - Import block is un-sorted or un-formatted
  - ID: c5e9a8d8
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/contract_analysis/agent.py:1` - Import block is un-sorted or un-formatted
  - ID: d21514c9
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/contract_analysis/aug_llms.py:1` - Import block is un-sorted or un-formatted
  - ID: bb30c126
- ... and 37 more

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/__init__.py:79` - Import block is un-sorted or un-formatted
  - ID: a87002f8
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/search/__init__.py:7` - Import block is un-sorted or un-formatted
  - ID: cbab648d
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/__init__.py:3` - Import block is un-sorted or un-formatted
  - ID: 5cc968b7
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/duckduckgo_search.py:27` - Import block is un-sorted or un-formatted
  - ID: 61e8251a
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/pokebase_tool.py:18` - Import block is un-sorted or un-formatted
  - ID: f3e9f02b
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/reddit_search.py:1` - Import block is un-sorted or un-formatted
  - ID: f9cb28e4
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/search_tools.py:14` - Import block is un-sorted or un-formatted
  - ID: 1471b116
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/__init__.py:3` - Import block is un-sorted or un-formatted
  - ID: 8982d8b7
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/amadues_toolkit.py:1` - Import block is un-sorted or un-formatted
  - ID: 3fed35a1
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/complexity_analyzer.py:19` - Import block is un-sorted or un-formatted
  - ID: fb67eaba
- ... and 4 more

## ruff:N801 (1 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/extended_sources.py:1010` - Class name `phpBBSource` should use CapWords convention
  - ID: 23102492

## ruff:N802 (49 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute_multi.py:45` - Function name `PlanAndExecuteAgent` should be lowercase
  - ID: 796ad9cc

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:858` - Function name `visit_If` should be lowercase
  - ID: 0cdc6d77
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:887` - Function name `visit_For` should be lowercase
  - ID: deb4cd05
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:947` - Function name `visit_FunctionDef` should be lowercase
  - ID: d9efd8a6
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:952` - Function name `visit_If` should be lowercase
  - ID: 3228be2a
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:965` - Function name `visit_For` should be lowercase
  - ID: f8a46b60
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:978` - Function name `visit_While` should be lowercase
  - ID: acdbaeb1
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:991` - Function name `visit_Try` should be lowercase
  - ID: b0292249
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:997` - Function name `visit_BoolOp` should be lowercase
  - ID: baf80482
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:1003` - Function name `visit_Return` should be lowercase
  - ID: e9327c9e
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:1008` - Function name `visit_Call` should be lowercase
  - ID: f70081f3
- ... and 2 more

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/function_logging_transformer.py:54` - Function name `leave_FunctionDef` should be lowercase
  - ID: 56ccb2bd
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/import_consolidator.py:32` - Function name `visit_Import` should be lowercase
  - ID: e96fcecb
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/import_consolidator.py:43` - Function name `leave_Module` should be lowercase
  - ID: d56eef21
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/multi_file_rename.py:42` - Function name `leave_FunctionDef` should be lowercase
  - ID: 25c85b7c
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/multi_file_rename.py:60` - Function name `leave_Call` should be lowercase
  - ID: 589184bc
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/print_to_logging.py:33` - Function name `leave_Expr` should be lowercase
  - ID: a6af74b2
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/refactor.py:53` - Function name `leave_FunctionDef` should be lowercase
  - ID: b98a8a2f
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/refactor.py:71` - Function name `leave_ClassDef` should be lowercase
  - ID: 11a518b4
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/refactor.py:89` - Function name `leave_Name` should be lowercase
  - ID: eeceee72
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/type_hints.py:57` - Function name `leave_FunctionDef` should be lowercase
  - ID: 0a0e73c0
- ... and 26 more

## ruff:N806 (47 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/selection_strategies.py:81` - Variable `TSR` in function should be lowercase
  - ID: a9fd985c
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/selection_strategies.py:122` - Variable `TSR` in function should be lowercase
  - ID: 07b88962
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/selection_strategies.py:199` - Variable `TSR` in function should be lowercase
  - ID: a5a92c98
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/selection_strategies.py:267` - Variable `TSR` in function should be lowercase
  - ID: a1e64bfe
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/selection_strategies.py:381` - Variable `TSR` in function should be lowercase
  - ID: d86d389c
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/selection_strategies.py:412` - Variable `TSR` in function should be lowercase
  - ID: ddd037a7
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/selection_strategies.py:464` - Variable `TSR` in function should be lowercase
  - ID: ed529a3c
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/utils.py:24` - Variable `G` in function should be lowercase
  - ID: ef69fdad
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/dynamic_supervisor/tools.py:256` - Variable `ChoiceModel` in function should be lowercase
  - ID: b8253585
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler/utils.py:126` - Variable `ID_PATTERN` in function should be lowercase
  - ID: 5afeec29
- ... and 17 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/output_parser/base.py:203` - Variable `MODULES` in function should be lowercase
  - ID: 1005f323
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/output_parser/base.py:213` - Variable `PARSER_MAP` in function should be lowercase
  - ID: 6ac4d09c
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/output_parser/base.py:279` - Variable `SPECIAL_HANDLERS` in function should be lowercase
  - ID: 94f80da9
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/output_parser/base.py:286` - Variable `REQUIRED_ATTRS` in function should be lowercase
  - ID: 1a9b1197
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/output_parser/base.py:293` - Variable `REQUIRED_PARAMS` in function should be lowercase
  - ID: 6bf4dd7a
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph_manager.py:174` - Variable `G` in function should be lowercase
  - ID: 011e679d
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/examples.py:150` - Variable `UnionUser` in function should be lowercase
  - ID: f028214e
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/examples.py:158` - Variable `CommonUser` in function should be lowercase
  - ID: 96f74972
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/example.py:55` - Variable `QuickState` in function should be lowercase
  - ID: c0a7d12b
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/example.py:113` - Variable `DynamicRAGState` in function should be lowercase
  - ID: b306e4a2
- ... and 3 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/base.py:289` - Variable `LLMConfigClass` in function should be lowercase
  - ID: 79d2a75d
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_api.py:402` - Variable `ChessResponse` in function should be lowercase
  - ID: 28bfb25d
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:501` - Variable `LLMConfigClass` in function should be lowercase
  - ID: 1e5dc59a
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/llm_routes.py:265` - Variable `LLMConfigClass` in function should be lowercase
  - ID: 80a408b9
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/llm_routes.py:406` - Variable `LLMConfigClass` in function should be lowercase
  - ID: 4e974f6e
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/base.py:289` - Variable `LLMConfigClass` in function should be lowercase
  - ID: b40aebb9

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/google_calendar.py:91` - Variable `CREDENTIALS_FILE` in function should be lowercase
  - ID: f4f63fbc

## ruff:N815 (1 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:45` - Variable `ariaLabel` in class scope should not be mixedCase
  - ID: c6f9c34d

## ruff:N817 (1 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/selection_strategies.py:27` - CamelCase `ToolSelectionResult` imported as acronym `TSR`
  - ID: 6ced5807

## ruff:N999 (105 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/agent.v2.py:1` - Invalid module name: 'agent.v2'
  - ID: 276da519
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/agent_v3.v2.py:1` - Invalid module name: 'agent_v3.v2'
  - ID: 2713e901
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/config.v2.py:1` - Invalid module name: 'config.v2'
  - ID: c1f48ace
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/dynamic_react_agent.v2.py:1` - Invalid module name: 'dynamic_react_agent.v2'
  - ID: c8b01a29
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/enhanced_agent_v3.v2.py:1` - Invalid module name: 'enhanced_agent_v3.v2'
  - ID: 32948af0
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/enhanced_react_agent.v2.py:1` - Invalid module name: 'enhanced_react_agent.v2'
  - ID: 93de9caf
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/state.v2.py:1` - Invalid module name: 'state.v2'
  - ID: c7c6d33a
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/agent.v2.py:1` - Invalid module name: 'agent.v2'
  - ID: e2716264
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/agent_v2.v2.py:1` - Invalid module name: 'agent_v2.v2'
  - ID: 0b651ccd
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/agent_v3_minimal.v2.py:1` - Invalid module name: 'agent_v3_minimal.v2'
  - ID: 443d787d
- ... and 13 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/AzureOpenAIEmbeddingConfig.py:1` - Invalid module name: 'AzureOpenAIEmbeddingConfig'
  - ID: cebc0f2a
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/CohereEmbeddingConfig.py:1` - Invalid module name: 'CohereEmbeddingConfig'
  - ID: f50d568c
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/FakeEmbeddingConfig.py:1` - Invalid module name: 'FakeEmbeddingConfig'
  - ID: ff0ac80d
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/GoogleVertexAIEmbeddingConfig.py:1` - Invalid module name: 'GoogleVertexAIEmbeddingConfig'
  - ID: 8c3b8c44
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/HuggingFaceEmbeddingConfig.py:1` - Invalid module name: 'HuggingFaceEmbeddingConfig'
  - ID: 040aa765
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/OllamaEmbeddingConfig.py:1` - Invalid module name: 'OllamaEmbeddingConfig'
  - ID: d2a03db6
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/OpenAIEmbeddingConfig.py:1` - Invalid module name: 'OpenAIEmbeddingConfig'
  - ID: 543df6d4
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/AmazonKnowledgeBasesRetrieverConfig.py:1` - Invalid module name: 'AmazonKnowledgeBasesRetrieverConfig'
  - ID: b6d5133f
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/ArceeRetrieverConfig.py:1` - Invalid module name: 'ArceeRetrieverConfig'
  - ID: 2899c642
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/ArxivRetrieverConfig.py:1` - Invalid module name: 'ArxivRetrieverConfig'
  - ID: 85b0d4ab
- ... and 71 more

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/bing_search_tool_INC.py:1` - Invalid module name: 'bing_search_tool_INC'
  - ID: c4733786

## ruff:PIE790 (43 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/__init__.py:68` - Unnecessary `pass` statement
  - ID: 604e9d51
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/__init__.py:72` - Unnecessary `pass` statement
  - ID: 395d51b2
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/__init__.py:76` - Unnecessary `pass` statement
  - ID: d7f0a37c
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/__init__.py:80` - Unnecessary `pass` statement
  - ID: af1d6525
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/__init__.py:84` - Unnecessary `pass` statement
  - ID: 7a0c2690
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/__init__.py:88` - Unnecessary `pass` statement
  - ID: 11960cd8
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/__init__.py:93` - Unnecessary `pass` statement
  - ID: 1e426aca
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/__init__.py:97` - Unnecessary `pass` statement
  - ID: 3984b4ad
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/__init__.py:101` - Unnecessary `pass` statement
  - ID: ca2e71c5
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/__init__.py:105` - Unnecessary `pass` statement
  - ID: 0f2d9872
- ... and 20 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/embeddings/__init__.py:107` - Unnecessary `pass` statement
  - ID: db2c8245
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/embeddings/__init__.py:111` - Unnecessary `pass` statement
  - ID: 8bad111b
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/embeddings/__init__.py:115` - Unnecessary `pass` statement
  - ID: 316cd7f2
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/embeddings/__init__.py:120` - Unnecessary `pass` statement
  - ID: bec8e985
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/vectorstore/__init__.py:138` - Unnecessary `pass` statement
  - ID: 9ca52578
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/vectorstore/__init__.py:142` - Unnecessary `pass` statement
  - ID: be16e650
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/vectorstore/__init__.py:146` - Unnecessary `pass` statement
  - ID: 0079715b
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/vectorstore/__init__.py:150` - Unnecessary `pass` statement
  - ID: a332fcac
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/vectorstore/__init__.py:154` - Unnecessary `pass` statement
  - ID: 2716afaf
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/vectorstore/__init__.py:158` - Unnecessary `pass` statement
  - ID: ba19255a
- ... and 3 more

## ruff:PIE796 (2 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/types.py:61` - Enum contains duplicate value: `"async"`
  - ID: f3d2a948
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/types.py:106` - Enum contains duplicate value: `"full"`
  - ID: f13b5810

## ruff:PIE807 (2 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/semantic_discovery.py:31` - Prefer `list` over useless lambda
  - ID: b37da301
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/semantic_discovery.py:32` - Prefer `list` over useless lambda
  - ID: d6f078d6

## ruff:PLC0206 (3 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/auto_registry.py:583` - Extracting value from dictionary without calling `.items()`
  - ID: 484cbb5a

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_enhanced.py:502` - Extracting value from dictionary without calling `.items()`
  - ID: 50765813
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:569` - Extracting value from dictionary without calling `.items()`
  - ID: 3382f09f

## ruff:PLE0605 (1 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/__init__.py:118` - Invalid format for `__all__`, must be `tuple` or `list`
  - ID: de44b7d7

## ruff:PLR0911 (141 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:538` - Too many return statements (7 > 6)
  - ID: 62c13bb1
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:296` - Too many return statements (8 > 6)
  - ID: 1ba3a3ad
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent_structured_output_mixin.py:184` - Too many return statements (7 > 6)
  - ID: 510fc7c9
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/execution_mixin.py:35` - Too many return statements (15 > 6)
  - ID: d8b75cec
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/execution_mixin.py:904` - Too many return statements (12 > 6)
  - ID: ea768424
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/composite.py:109` - Too many return statements (13 > 6)
  - ID: 2e797031
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/debate/agent.py:225` - Too many return statements (7 > 6)
  - ID: 9ff43c8a
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/agent.py:913` - Too many return statements (8 > 6)
  - ID: 4a832e42
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/quick_search/agent.py:190` - Too many return statements (8 > 6)
  - ID: f4aacb6d
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/base/token_state.py:338` - Too many return statements (8 > 6)
  - ID: 46be8e23
- ... and 27 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/tool_list_mixin.py:197` - Too many return statements (9 > 6)
  - ID: 354e3b19
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py:1661` - Too many return statements (13 > 6)
  - ID: b7277789
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py:2647` - Too many return statements (11 > 6)
  - ID: 8aa2f0a1
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/handlers.py:11` - Too many return statements (20 > 6)
  - ID: c0746071
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/handlers.py:313` - Too many return statements (7 > 6)
  - ID: 116cfa08
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/utils/state_handling.py:56` - Too many return statements (7 > 6)
  - ID: a90f558f
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/utils/state_handling.py:180` - Too many return statements (10 > 6)
  - ID: 777d959f
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:764` - Too many return statements (7 > 6)
  - ID: 81c2e66d
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/factory.py:370` - Too many return statements (9 > 6)
  - ID: 8cc5e6fc
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/factory.py:569` - Too many return statements (9 > 6)
  - ID: ae6d477a
- ... and 80 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes.py:588` - Too many return statements (7 > 6)
  - ID: ddac4b81
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_enhanced.py:169` - Too many return statements (12 > 6)
  - ID: b62635ff
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/bin/vault_cli.py:455` - Too many return statements (7 > 6)
  - ID: 1145ce66
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registries/model_registry.py:625` - Too many return statements (7 > 6)
  - ID: 9d059872
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py:455` - Too many return statements (7 > 6)
  - ID: fd479089
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/registries/model_registry.py:625` - Too many return statements (7 > 6)
  - ID: 513434e1
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/serialization.py:170` - Too many return statements (14 > 6)
  - ID: 5ceeed85
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/serialization.py:254` - Too many return statements (15 > 6)
  - ID: 86071ce8
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/serialization.py:89` - Too many return statements (14 > 6)
  - ID: 0e4232d9
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/serialization.py:173` - Too many return statements (15 > 6)
  - ID: 22bdea38

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/cli/mcp_manager.py:125` - Too many return statements (7 > 6)
  - ID: 6185a2bb
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/discovery.py:574` - Too many return statements (13 > 6)
  - ID: 0e359746
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/installers/safe_pattern_installer.py:140` - Too many return statements (7 > 6)
  - ID: 0ed5b261
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/integrated_mcp_system.py:58` - Too many return statements (12 > 6)
  - ID: 123e1b19

## ruff:PLR0912 (364 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:215` - Too many branches (23 > 12)
  - ID: 73d0912e
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:538` - Too many branches (16 > 12)
  - ID: 8aec9a26
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:121` - Too many branches (14 > 12)
  - ID: 0b3bd70d
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:228` - Too many branches (18 > 12)
  - ID: 64afc8be
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:296` - Too many branches (31 > 12)
  - ID: b169f4bc
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:453` - Too many branches (15 > 12)
  - ID: 6a81194a
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:553` - Too many branches (15 > 12)
  - ID: 526378ca
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent_structured_output_mixin.py:184` - Too many branches (14 > 12)
  - ID: 3913de19
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/debug_utils.py:43` - Too many branches (13 > 12)
  - ID: e6ed9b58
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/enhanced_agent.py:143` - Too many branches (14 > 12)
  - ID: 53160dc1
- ... and 81 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/checkpointer_mixin.py:143` - Too many branches (13 > 12)
  - ID: 4421a9d9
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/checkpointer_mixin.py:463` - Too many branches (18 > 12)
  - ID: cdf585e0
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/engine_mixin.py:411` - Too many branches (26 > 12)
  - ID: a19340ba
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/engine_mixin.py:526` - Too many branches (16 > 12)
  - ID: 56816113
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/tool_list_mixin.py:102` - Too many branches (13 > 12)
  - ID: 869713ec
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/tool_route_mixin.py:650` - Too many branches (13 > 12)
  - ID: e644e61e
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/documents/github_repo.py:176` - Too many branches (19 > 12)
  - ID: 41a89266
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py:420` - Too many branches (50 > 12)
  - ID: 046c9b28
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py:1005` - Too many branches (19 > 12)
  - ID: 862e7481
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py:1398` - Too many branches (14 > 12)
  - ID: 81415f3d
- ... and 188 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router.py:48` - Too many branches (20 > 12)
  - ID: 6dcd5eaa
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router.py:252` - Too many branches (19 > 12)
  - ID: 8372e09f
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router_fixed.py:39` - Too many branches (14 > 12)
  - ID: de254ad1
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router_fixed.py:226` - Too many branches (19 > 12)
  - ID: 579126ca
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/general_games_api.py:149` - Too many branches (15 > 12)
  - ID: d6bcc5ca
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/general_games_api.py:282` - Too many branches (13 > 12)
  - ID: 26b45245
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/registry.py:93` - Too many branches (16 > 12)
  - ID: fca183ec
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes.py:333` - Too many branches (18 > 12)
  - ID: 896dcd67
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:548` - Too many branches (34 > 12)
  - ID: a2c2e5d7
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes.py:75` - Too many branches (24 > 12)
  - ID: 9250976e
- ... and 57 more

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:496` - Too many branches (14 > 12)
  - ID: 157853d4
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/comprehensive_mcp_web.py:182` - Too many branches (14 > 12)
  - ID: b2dca7e3
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/comprehensive_mcp_web.py:405` - Too many branches (14 > 12)
  - ID: ae4020ee
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/discovery/analyzer.py:309` - Too many branches (13 > 12)
  - ID: 2c281924
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/fastmcp_runner.py:274` - Too many branches (27 > 12)
  - ID: 18b125ca
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/installers/advanced_code_installer.py:269` - Too many branches (14 > 12)
  - ID: 6d96fc42
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mcp_simple_rag_agent.py:442` - Too many branches (26 > 12)
  - ID: ce8f850b
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/tools/server_selector.py:482` - Too many branches (14 > 12)
  - ID: 4875e821

## ruff:PLR0913 (201 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/hooks_mixin.py:65` - Too many arguments in function definition (6 > 5)
  - ID: 3dfa1551
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/__init__.py:349` - Too many arguments in function definition (6 > 5)
  - ID: 4c720812
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/debate/agent.py:357` - Too many arguments in function definition (6 > 5)
  - ID: dbae99fb
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/factory.py:13` - Too many arguments in function definition (7 > 5)
  - ID: fa755475
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_base/models.py:62` - Too many arguments in function definition (10 > 5)
  - ID: bea1caba
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/utils.py:106` - Too many arguments in function definition (8 > 5)
  - ID: 2c72245c
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/ltm/agent.py:199` - Too many arguments in function definition (6 > 5)
  - ID: 0cc1240f
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/core/stores.py:86` - Too many arguments in function definition (6 > 5)
  - ID: b121ce4e
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/core/stores.py:177` - Too many arguments in function definition (6 > 5)
  - ID: 1c9a829e
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/enhanced_retriever.py:176` - Too many arguments in function definition (7 > 5)
  - ID: 3feed683
- ... and 81 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/structures/tree.py:297` - Too many arguments in function definition (7 > 5)
  - ID: d34fa934
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/config/auth_runnable.py:70` - Too many arguments in function definition (6 > 5)
  - ID: d7f840a2
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/manager.py:775` - Too many arguments in function definition (8 > 5)
  - ID: c1141962
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:1389` - Too many arguments in function definition (6 > 5)
  - ID: 3a578913
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:1422` - Too many arguments in function definition (7 > 5)
  - ID: c34c4c81
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/registry.py:224` - Too many arguments in function definition (7 > 5)
  - ID: 8cb4ea6f
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/enhanced_registry.py:94` - Too many arguments in function definition (22 > 5)
  - ID: 474bbf56
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/enhanced_registry.py:370` - Too many arguments in function definition (25 > 5)
  - ID: 5082931a
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/registry.py:93` - Too many arguments in function definition (11 > 5)
  - ID: c3cb9c6f
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/registry.py:333` - Too many arguments in function definition (10 > 5)
  - ID: c362fd01
- ... and 84 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:27` - Too many arguments in function definition (6 > 5)
  - ID: 62bf4d2b
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_agent.py:273` - Too many arguments in function definition (6 > 5)
  - ID: 9a1d545a
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_api.py:86` - Too many arguments in function definition (7 > 5)
  - ID: b04ae888
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_api.py:353` - Too many arguments in function definition (7 > 5)
  - ID: 552ceed6
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/middleware/supabase_logging.py:41` - Too many arguments in function definition (10 > 5)
  - ID: 934f00d8
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/middleware/supabase_logging.py:110` - Too many arguments in function definition (12 > 5)
  - ID: 84728ee6
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/middleware/supabase_logging.py:389` - Too many arguments in function definition (11 > 5)
  - ID: cd4dace9
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/core.py:1085` - Too many arguments in function definition (6 > 5)
  - ID: 0e00bbf8
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/game_agent.py:273` - Too many arguments in function definition (6 > 5)
  - ID: bad4bf7c
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/core.py:1154` - Too many arguments in function definition (6 > 5)
  - ID: 00192c1c
- ... and 3 more

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/search_tools.py:38` - Too many arguments in function definition (9 > 5)
  - ID: c44fe8c3
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/search_tools.py:113` - Too many arguments in function definition (8 > 5)
  - ID: fb97a5b5
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/search_tools.py:168` - Too many arguments in function definition (9 > 5)
  - ID: 64668202

## ruff:PLR0915 (164 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:215` - Too many statements (57 > 50)
  - ID: 4b0ca0bd
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:228` - Too many statements (53 > 50)
  - ID: b84fd8c6
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:296` - Too many statements (86 > 50)
  - ID: e8d2aba0
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/execution_mixin.py:35` - Too many statements (118 > 50)
  - ID: b86bfcf1
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/execution_mixin.py:483` - Too many statements (70 > 50)
  - ID: db81cd83
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/execution_mixin.py:621` - Too many statements (58 > 50)
  - ID: f661aa26
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/execution_mixin.py:764` - Too many statements (64 > 50)
  - ID: 697dac53
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/pre_post_agent_mixin.py:199` - Too many statements (58 > 50)
  - ID: fe417d90
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain_agent.py:200` - Too many statements (77 > 50)
  - ID: 6caaecab
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain_agent.py:203` - Too many statements (75 > 50)
  - ID: 83c973e0
- ... and 29 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/engine_mixin.py:411` - Too many statements (59 > 50)
  - ID: c5d1736a
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/engine_mixin.py:526` - Too many statements (56 > 50)
  - ID: 4738df64
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py:420` - Too many statements (147 > 50)
  - ID: fdd7a219
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py:1005` - Too many statements (72 > 50)
  - ID: b447fba9
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py:1661` - Too many statements (80 > 50)
  - ID: 50e87e12
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py:2007` - Too many statements (71 > 50)
  - ID: 09a470ac
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py:2190` - Too many statements (99 > 50)
  - ID: a4fbb661
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py:2473` - Too many statements (52 > 50)
  - ID: ba63f425
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py:2688` - Too many statements (101 > 50)
  - ID: ea3e6fa6
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py:3371` - Too many statements (71 > 50)
  - ID: 2dbf8540
- ... and 63 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/connect4_api.py:87` - Too many statements (85 > 50)
  - ID: cc00499b
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_agent.py:321` - Too many statements (80 > 50)
  - ID: 1c5d0117
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_api.py:144` - Too many statements (60 > 50)
  - ID: 8bb19cda
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router.py:48` - Too many statements (67 > 50)
  - ID: c3de1c7e
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router.py:243` - Too many statements (82 > 50)
  - ID: 5482398f
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router.py:252` - Too many statements (73 > 50)
  - ID: b9c9cecf
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router_fixed.py:215` - Too many statements (84 > 50)
  - ID: b5d2ab65
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router_fixed.py:226` - Too many statements (73 > 50)
  - ID: 53bdfc30
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/middleware/supabase_logging.py:237` - Too many statements (56 > 50)
  - ID: 9b710db3
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/registry.py:93` - Too many statements (67 > 50)
  - ID: c56bc9a0
- ... and 37 more

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/comprehensive_mcp_web.py:283` - Too many statements (55 > 50)
  - ID: 25e4d637
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/comprehensive_mcp_web.py:405` - Too many statements (62 > 50)
  - ID: 4143ad69
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/csv_viewer.py:81` - Too many statements (54 > 50)
  - ID: 9de5e86d
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/fastmcp_runner.py:274` - Too many statements (51 > 50)
  - ID: 9467e119
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mcp_simple_rag_agent.py:442` - Too many statements (72 > 50)
  - ID: de870711

## ruff:PLR1704 (9 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/config.py:111` - Redefining argument with the local name `name`
  - ID: 27dfc0b2
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/sequential/config.py:126` - Redefining argument with the local name `name`
  - ID: 5a7f5945

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/models/state_graph_model.py:211` - Redefining argument with the local name `name`
  - ID: f6c41d6d
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/schema_composer.py:3094` - Redefining argument with the local name `name`
  - ID: 24f7ef56
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/schema_composer.py:3218` - Redefining argument with the local name `name`
  - ID: 2cb004f9
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/schema_composer.py:3276` - Redefining argument with the local name `name`
  - ID: 6ec0192f
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/schema_composer.py:3355` - Redefining argument with the local name `name`
  - ID: 69efe975
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/schema_manager.py:906` - Redefining argument with the local name `name`
  - ID: d36105ba

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py:202` - Redefining argument with the local name `components`
  - ID: 2f25738a

## ruff:PLR2004 (700 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:559` - Magic value used in comparison, consider replacing `2` with a constant variable
  - ID: 408530d5
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:624` - Magic value used in comparison, consider replacing `2` with a constant variable
  - ID: 38b31dd0
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:368` - Magic value used in comparison, consider replacing `5` with a constant variable
  - ID: cec800fe
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/debug_utils.py:90` - Magic value used in comparison, consider replacing `50` with a constant variable
  - ID: 5500943a
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/debug_utils.py:101` - Magic value used in comparison, consider replacing `50` with a constant variable
  - ID: b7e5eacd
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/debug_utils.py:170` - Magic value used in comparison, consider replacing `8` with a constant variable
  - ID: 111d7dc8
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/debug_utils.py:184` - Magic value used in comparison, consider replacing `8` with a constant variable
  - ID: c555d017
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/chain_agent_simple.py:97` - Magic value used in comparison, consider replacing `2` with a constant variable
  - ID: 0a8c0b06
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/chain_agent_simple.py:121` - Magic value used in comparison, consider replacing `2` with a constant variable
  - ID: e177dede
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/chain_agent_simple.py:127` - Magic value used in comparison, consider replacing `3` with a constant variable
  - ID: fbb17388
- ... and 445 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/engine_mixin.py:572` - Magic value used in comparison, consider replacing `3` with a constant variable
  - ID: a71a40be
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/engine_mixin.py:581` - Magic value used in comparison, consider replacing `3` with a constant variable
  - ID: 6cbd63c8
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/mcp_mixin.py:426` - Magic value used in comparison, consider replacing `2` with a constant variable
  - ID: 9cc44902
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/tool_route_mixin.py:495` - Magic value used in comparison, consider replacing `2` with a constant variable
  - ID: 12b0bdf8
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/documents/github_repo.py:156` - Magic value used in comparison, consider replacing `404` with a constant variable
  - ID: d41c08ff
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/documents/github_repo.py:158` - Magic value used in comparison, consider replacing `403` with a constant variable
  - ID: f8bae063
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/documents/github_repo.py:162` - Magic value used in comparison, consider replacing `200` with a constant variable
  - ID: 22a7c83e
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/documents/github_repo.py:181` - Magic value used in comparison, consider replacing `200` with a constant variable
  - ID: c7f6bad2
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/documents/github_repo.py:211` - Magic value used in comparison, consider replacing `5` with a constant variable
  - ID: fcbebfc1
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/documents/github_repo.py:216` - Magic value used in comparison, consider replacing `5` with a constant variable
  - ID: 65e16187
- ... and 154 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py:184` - Magic value used in comparison, consider replacing `2` with a constant variable
  - ID: 8bb6add8
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/middleware/supabase_logging.py:203` - Magic value used in comparison, consider replacing `1000` with a constant variable
  - ID: b8a92ee3
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/middleware/supabase_logging.py:274` - Magic value used in comparison, consider replacing `1000` with a constant variable
  - ID: 59d3a009
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/middleware/supabase_logging.py:306` - Magic value used in comparison, consider replacing `1000` with a constant variable
  - ID: eb5b56aa
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes_fixed.py:531` - Magic value used in comparison, consider replacing `2` with a constant variable
  - ID: e287a919
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:538` - Magic value used in comparison, consider replacing `2` with a constant variable
  - ID: df72819e
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/bin/registry_cli.py:297` - Magic value used in comparison, consider replacing `50` with a constant variable
  - ID: 2f9614b8
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/bin/registry_cli.py:331` - Magic value used in comparison, consider replacing `50` with a constant variable
  - ID: 38169452
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/bin/registry_cli.py:372` - Magic value used in comparison, consider replacing `50` with a constant variable
  - ID: 261c138b
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/bin/registry_cli.py:420` - Magic value used in comparison, consider replacing `50` with a constant variable
  - ID: 1d2fe8ee
- ... and 25 more

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/cli.py:46` - Magic value used in comparison, consider replacing `5` with a constant variable
  - ID: df506456
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/cli.py:49` - Magic value used in comparison, consider replacing `60` with a constant variable
  - ID: aa94b682
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/comprehensive_mcp_web.py:254` - Magic value used in comparison, consider replacing `1000` with a constant variable
  - ID: 9fe91b7d
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/comprehensive_mcp_web.py:673` - Magic value used in comparison, consider replacing `300` with a constant variable
  - ID: 7cbf4df6
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/documentation/doc_loader.py:214` - Magic value used in comparison, consider replacing `2` with a constant variable
  - ID: 37e4b101
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/documentation/doc_loader.py:373` - Magic value used in comparison, consider replacing `2` with a constant variable
  - ID: e82de83f
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/discovery.py:233` - Magic value used in comparison, consider replacing `200` with a constant variable
  - ID: 4dfdfa63
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/discovery.py:356` - Magic value used in comparison, consider replacing `200` with a constant variable
  - ID: 93b0e33f
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/discovery.py:418` - Magic value used in comparison, consider replacing `200` with a constant variable
  - ID: 6b25c8f3
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/github_mass_downloader.py:339` - Magic value used in comparison, consider replacing `5` with a constant variable
  - ID: c40bf2e9
- ... and 32 more

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/binlist_lookup.py:71` - Magic value used in comparison, consider replacing `404` with a constant variable
  - ID: dd9794f2
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/fruityvice_tool.py:54` - Magic value used in comparison, consider replacing `404` with a constant variable
  - ID: 70161db5
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/open_food_tool.py:53` - Magic value used in comparison, consider replacing `200` with a constant variable
  - ID: 947d564e
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/code_smell_detector.py:47` - Magic value used in comparison, consider replacing `3` with a constant variable
  - ID: b8c6097f

## ruff:PLR5501 (1 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/enhanced_multi_agent_state.py:225` - Use `elif` instead of `else` then `if`, to reduce indentation
  - ID: 5b86839d

## ruff:PLW0127 (1 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py:1237` - Self-assignment of variable `new_path`
  - ID: e2dfab1c

## ruff:PLW0128 (1 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py:1237` - Redeclared variable `new_path` in assignment
  - ID: 3256fc16

## ruff:PLW0602 (10 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/core/memory_tools.py:193` - Using global for `_MEMORY_STORAGE` but no assignment is done
  - ID: 8207a08b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/core/memory_tools.py:300` - Using global for `_MEMORY_STORAGE` but no assignment is done
  - ID: 60141ec0
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/core/memory_tools.py:412` - Using global for `_MEMORY_STORAGE` but no assignment is done
  - ID: 7b98763c
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/core/memory_tools.py:746` - Using global for `_MEMORY_STORAGE` but no assignment is done
  - ID: f5abec96
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/memory_tools.py:193` - Using global for `_MEMORY_STORAGE` but no assignment is done
  - ID: 7f4b0cf9
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/memory_tools.py:300` - Using global for `_MEMORY_STORAGE` but no assignment is done
  - ID: c4ccb459
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/memory_tools.py:412` - Using global for `_MEMORY_STORAGE` but no assignment is done
  - ID: c0873d59
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/memory_tools.py:748` - Using global for `_MEMORY_STORAGE` but no assignment is done
  - ID: b5f47074

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/importers/tak.py:479` - Using global for `all_tools` but no assignment is done
  - ID: ce452a86
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/importers/tak.py:479` - Using global for `all_tools` but no assignment is done
  - ID: c720020c

## ruff:PLW0603 (45 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/debug_utils.py:253` - Using the global statement to update `_global_debugger` is discouraged
  - ID: f57a9877
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/selection_strategies.py:25` - Using the global statement to update `ToolSelectionResult` is discouraged
  - ID: 613c9077
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/semantic_discovery.py:51` - Using the global statement to update `BaseSelectionStrategy` is discouraged
  - ID: 881f5127
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/semantic_discovery.py:51` - Using the global statement to update `BaseSelectionStrategy` is discouraged
  - ID: 881f5127
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/semantic_discovery.py:51` - Using the global statement to update `BaseSelectionStrategy` is discouraged
  - ID: 881f5127
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/semantic_discovery.py:52` - Using the global statement to update `AdaptiveSelectionStrategy` is discouraged
  - ID: 64b33391
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/semantic_discovery.py:52` - Using the global statement to update `AdaptiveSelectionStrategy` is discouraged
  - ID: 64b33391
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/semantic_discovery.py:52` - Using the global statement to update `AdaptiveSelectionStrategy` is discouraged
  - ID: 64b33391
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/core/memory_tools.py:193` - Using the global statement to update `_MEMORY_CONFIG` is discouraged
  - ID: a69e0e72
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/core/memory_tools.py:300` - Using the global statement to update `_MEMORY_CONFIG` is discouraged
  - ID: e1cb21bf
- ... and 6 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/auto_loader.py:1437` - Using the global statement to update `_default_loader` is discouraged
  - ID: b592d25d
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/auto_registry.py:734` - Using the global statement to update `_registration_done` is discouraged
  - ID: fc66286b
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/auto_registry.py:734` - Using the global statement to update `_registration_done` is discouraged
  - ID: fc66286b
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/metadata.py:112` - Using the global statement to update `_MODEL_METADATA_CACHE` is discouraged
  - ID: 0f1f8602
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/metadata.py:112` - Using the global statement to update `_MODEL_METADATA_CACHE` is discouraged
  - ID: 0f1f8602
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/metadata.py:112` - Using the global statement to update `_MODEL_METADATA_CACHE` is discouraged
  - ID: 0f1f8602
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/metadata.py:112` - Using the global statement to update `_MODEL_METADATA_CACHE` is discouraged
  - ID: 0f1f8602
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/__init__.py:33` - Using the global statement to update `_type_analyzer` is discouraged
  - ID: 08bc2a47
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/__init__.py:57` - Using the global statement to update `_complexity_analyzer` is discouraged
  - ID: 4778ee58
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/__init__.py:71` - Using the global statement to update `_static_orchestrator` is discouraged
  - ID: 64e743cc

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes_enhanced.py:139` - Using the global statement to update `_discovery_instance` is discouraged
  - ID: 8e18e498
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes_enhanced.py:161` - Using the global statement to update `_discovery_cache` is discouraged
  - ID: caa1c2c2
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes_fixed.py:104` - Using the global statement to update `_discovery_instance` is discouraged
  - ID: 77bf96ef
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes_fixed.py:115` - Using the global statement to update `_cached_agents` is discouraged
  - ID: eb5a06a9
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_enhanced.py:145` - Using the global statement to update `_discovery_cache` is discouraged
  - ID: 42f56a65
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:93` - Using the global statement to update `_discovery_instance` is discouraged
  - ID: 76c63fbb
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:104` - Using the global statement to update `_cached_tools` is discouraged
  - ID: 7e0ea07e
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/bin/litellm_cli.py:104` - Using the global statement to update `TQDM_AVAILABLE` is discouraged
  - ID: 846ff342
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/bin/litellm_cli.py:104` - Using the global statement to update `TQDM_AVAILABLE` is discouraged
  - ID: 846ff342
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/bin/litellm_cli.py:104` - Using the global statement to update `TQDM_AVAILABLE` is discouraged
  - ID: c7c994f5
- ... and 3 more

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mcp_rag_agent.py:94` - Using the global statement to update `rag_agent` is discouraged
  - ID: 1979cd99
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mcp_simple_rag_agent.py:176` - Using the global statement to update `mcp_agent` is discouraged
  - ID: 05de04f6
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mcp_simple_tool_agent.py:113` - Using the global statement to update `VECTOR_STORE` is discouraged
  - ID: 1cabf26f
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mcp_simple_tool_agent.py:232` - Using the global statement to update `mcp_agent` is discouraged
  - ID: 464635f2
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/servers/http_server.py:182` - Using the global statement to update `sse_transport` is discouraged
  - ID: cb612ef4
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/simple_rag_mcp_agent.py:160` - Using the global statement to update `rag_agent` is discouraged
  - ID: 4b34025b

## ruff:PLW1508 (1 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/manager.py:832` - Invalid type for environment variable default; expected `str` or `None`
  - ID: eaedb8fe

## ruff:PLW1510 (2 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/static.py:277` - `subprocess.run` without explicit `check` argument
  - ID: ee5d4fa0
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/static.py:312` - `subprocess.run` without explicit `check` argument
  - ID: 0e6fda9a

## ruff:PLW2901 (33 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/time_weighted_retriever.py:347` - `for` loop variable `score` overwritten by assignment target
  - ID: dbcef4ce
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/dynamic_react_agent.py:773` - `for` loop variable `line` overwritten by assignment target
  - ID: 2d5fbe64
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/dynamic_react_agent.v2.py:781` - `for` loop variable `line` overwritten by assignment target
  - ID: 14e7d24a
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v2/example.py:106` - `for` loop variable `state` overwritten by assignment target
  - ID: 8a18a2f9
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/agent.py:237` - `for` loop variable `line` overwritten by assignment target
  - ID: be708202
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/orchestrator.py:223` - `for` loop variable `line` overwritten by assignment target
  - ID: 39547dea
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/archive/dynamic_agent_discovery_supervisor.py:298` - `for` loop variable `line` overwritten by assignment target
  - ID: 2d15fac6
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/archive/dynamic_tool_discovery_supervisor.py:390` - `for` loop variable `line` overwritten by assignment target
  - ID: 0894d8c5
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic_agent_discovery_supervisor.py:298` - `for` loop variable `line` overwritten by assignment target
  - ID: e9ed4ef4
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic_tool_discovery_supervisor.py:390` - `for` loop variable `line` overwritten by assignment target
  - ID: 289a0060

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/tool_route_mixin.py:241` - `for` loop variable `tool` overwritten by assignment target
  - ID: 3c50447d
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/tool_route_mixin.py:271` - `for` loop variable `tool` overwritten by assignment target
  - ID: 0e973332
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/engine.py:361` - `for` loop variable `sentence` overwritten by assignment target
  - ID: 84910a9f
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/processors.py:181` - `for` loop variable `sentence` overwritten by assignment target
  - ID: a0418a73
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/branches/utils.py:46` - `for` loop variable `part` overwritten by assignment target
  - ID: 6d6d6547
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/branches/utils.py:48` - `for` loop variable `part` overwritten by assignment target
  - ID: b30e6145
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/common/field_utils.py:46` - `for` loop variable `part` overwritten by assignment target
  - ID: cb937c4f
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/common/field_utils.py:48` - `for` loop variable `part` overwritten by assignment target
  - ID: 39e5ee7e
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/dynamic_graph_builder.py:301` - `for` loop variable `component` overwritten by assignment target
  - ID: 557edb8b
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/dynamic_graph_builder.py:324` - `for` loop variable `component` overwritten by assignment target
  - ID: ca1277b9
- ... and 12 more

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/type_hints.py:77` - `for` loop variable `param` overwritten by assignment target
  - ID: 4c36ae3e

## ruff:Q000 (7811 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:32` - Single quotes found but double quotes preferred
  - ID: 0648fd8f
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:89` - Single quotes found but double quotes preferred
  - ID: 7d895488
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:90` - Single quotes found but double quotes preferred
  - ID: 80882800
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:90` - Single quotes found but double quotes preferred
  - ID: 80882800
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:91` - Single quotes found but double quotes preferred
  - ID: bc30b01f
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:92` - Single quotes found but double quotes preferred
  - ID: b38c647b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:93` - Single quotes found but double quotes preferred
  - ID: 3d674aa9
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:94` - Single quotes found but double quotes preferred
  - ID: 58766d68
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:95` - Single quotes found but double quotes preferred
  - ID: 7d3eeca1
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:96` - Single quotes found but double quotes preferred
  - ID: 8c0c082a
- ... and 5192 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/documents/github_repo.py:23` - Single quotes found but double quotes preferred
  - ID: 41d808b9
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/documents/github_repo.py:23` - Single quotes found but double quotes preferred
  - ID: 41d808b9
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/documents/github_repo.py:24` - Single quotes found but double quotes preferred
  - ID: f108efe8
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/documents/github_repo.py:24` - Single quotes found but double quotes preferred
  - ID: f108efe8
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/documents/github_repo.py:25` - Single quotes found but double quotes preferred
  - ID: b7ee1a81
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/documents/github_repo.py:25` - Single quotes found but double quotes preferred
  - ID: b7ee1a81
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/documents/github_repo.py:26` - Single quotes found but double quotes preferred
  - ID: fdf1b2f2
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/documents/github_repo.py:26` - Single quotes found but double quotes preferred
  - ID: fdf1b2f2
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/documents/github_repo.py:26` - Single quotes found but double quotes preferred
  - ID: fdf1b2f2
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/documents/github_repo.py:27` - Single quotes found but double quotes preferred
  - ID: d4a0986e
- ... and 2508 more

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/dynamic_activation_mcp.py:44` - Single quotes found but double quotes preferred
  - ID: 47aa16c1
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/dynamic_activation_mcp.py:45` - Single quotes found but double quotes preferred
  - ID: 6821f155
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/dynamic_activation_mcp.py:46` - Single quotes found but double quotes preferred
  - ID: b3f6516b
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/dynamic_activation_mcp.py:47` - Single quotes found but double quotes preferred
  - ID: 36ebfc75
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/dynamic_activation_mcp.py:48` - Single quotes found but double quotes preferred
  - ID: 4c9f0ad4
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/dynamic_activation_mcp.py:97` - Single quotes found but double quotes preferred
  - ID: 8be61a75
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/dynamic_activation_mcp.py:149` - Single quotes found but double quotes preferred
  - ID: 77d069dc
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/dynamic_activation_mcp.py:150` - Single quotes found but double quotes preferred
  - ID: 2efc0de6
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/dynamic_activation_mcp.py:151` - Single quotes found but double quotes preferred
  - ID: 18930a6a
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/dynamic_activation_mcp.py:151` - Single quotes found but double quotes preferred
  - ID: 18930a6a
- ... and 81 more

## ruff:RET501 (1 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/hyde/enhanced_agent.py:30` - Do not explicitly `return None` in function if it is the only possible return value
  - ID: 89b8bc14

## ruff:RET505 (28 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:74` - Unnecessary `elif` after `return` statement
  - ID: 07dc9b66
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:90` - Unnecessary `elif` after `return` statement
  - ID: f0c50085
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:252` - Unnecessary `elif` after `return` statement
  - ID: 9e07e19d
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:320` - Unnecessary `elif` after `return` statement
  - ID: bb346728
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:410` - Unnecessary `elif` after `return` statement
  - ID: a73587b4
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/extended_chain.py:109` - Unnecessary `else` after `return` statement
  - ID: 5e6d2f4c
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/base/utils.py:28` - Unnecessary `elif` after `return` statement
  - ID: 6fe7ffdd
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/supervisor/tools.py:226` - Unnecessary `else` after `return` statement
  - ID: 521d1df2
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/base.py:34` - Unnecessary `elif` after `return` statement
  - ID: 7fbb3694
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/base.py:37` - Unnecessary `elif` after `return` statement
  - ID: 314a17f9
- ... and 18 more

## ruff:RET506 (1 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/agent.py:214` - Unnecessary `elif` after `raise` statement
  - ID: b3dc8a91

## ruff:RUF001 (36 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/models/base.py:321` - String contains ambiguous `⨯` (VECTOR OR CROSS PRODUCT). Did you mean `x` (LATIN SMALL LETTER X)?
  - ID: 08d2e566
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/smart_parsing_example.py:334` - String contains ambiguous `ℹ` (INFORMATION SOURCE). Did you mean `i` (LATIN SMALL LETTER I)?
  - ID: 088b6dd6
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v3/example.py:82` - String contains ambiguous `×` (MULTIPLICATION SIGN). Did you mean `x` (LATIN SMALL LETTER X)?
  - ID: e9a849d9
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/engines/logical_reasoner.py:30` - String contains ambiguous `∨` (LOGICAL OR). Did you mean `v` (LATIN SMALL LETTER V)?
  - ID: 76e2cf70
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/engines/uncertainty_analyzer.py:82` - String contains ambiguous `×` (MULTIPLICATION SIGN). Did you mean `x` (LATIN SMALL LETTER X)?
  - ID: e88e6178
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/engines/uncertainty_analyzer.py:86` - String contains ambiguous `×` (MULTIPLICATION SIGN). Did you mean `x` (LATIN SMALL LETTER X)?
  - ID: 22e4b30c
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/engines/uncertainty_analyzer.py:86` - String contains ambiguous `×` (MULTIPLICATION SIGN). Did you mean `x` (LATIN SMALL LETTER X)?
  - ID: 22e4b30c
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/engines/uncertainty_analyzer.py:87` - String contains ambiguous `×` (MULTIPLICATION SIGN). Did you mean `x` (LATIN SMALL LETTER X)?
  - ID: e89a4b38
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/engines/uncertainty_analyzer.py:87` - String contains ambiguous `×` (MULTIPLICATION SIGN). Did you mean `x` (LATIN SMALL LETTER X)?
  - ID: e89a4b38
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/engines/uncertainty_analyzer.py:120` - String contains ambiguous `×` (MULTIPLICATION SIGN). Did you mean `x` (LATIN SMALL LETTER X)?
  - ID: 2cd6ad45
- ... and 10 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/dynamic_choice_model.py:147` - String contains ambiguous `➕` (HEAVY PLUS SIGN). Did you mean `+` (PLUS SIGN)?
  - ID: abe01a7c
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/dynamic_choice_model.py:167` - String contains ambiguous `➖` (HEAVY MINUS SIGN). Did you mean `-` (HYPHEN-MINUS)?
  - ID: 2f31b328
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/dynamic_choice_model.py:185` - String contains ambiguous `➖` (HEAVY MINUS SIGN). Did you mean `-` (HYPHEN-MINUS)?
  - ID: dfeaf7f7
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/dynamic_choice_model.py:228` - String contains ambiguous `➕` (HEAVY PLUS SIGN). Did you mean `+` (PLUS SIGN)?
  - ID: 52d1f29c
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/dynamic_choice_model.py:228` - String contains ambiguous `➕` (HEAVY PLUS SIGN). Did you mean `+` (PLUS SIGN)?
  - ID: 52d1f29c
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:438` - String contains ambiguous `➕` (HEAVY PLUS SIGN). Did you mean `+` (PLUS SIGN)?
  - ID: a98cf748
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:535` - String contains ambiguous `➕` (HEAVY PLUS SIGN). Did you mean `+` (PLUS SIGN)?
  - ID: 1c2789fb
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:679` - String contains ambiguous `➕` (HEAVY PLUS SIGN). Did you mean `+` (PLUS SIGN)?
  - ID: d9a30c9a
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:1239` - String contains ambiguous `➕` (HEAVY PLUS SIGN). Did you mean `+` (PLUS SIGN)?
  - ID: b2b6a2cc
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:1252` - String contains ambiguous `➖` (HEAVY MINUS SIGN). Did you mean `-` (HYPHEN-MINUS)?
  - ID: 1b5f160b
- ... and 4 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/base.py:70` - String contains ambiguous `–` (EN DASH). Did you mean `-` (HYPHEN-MINUS)?
  - ID: 740e87a4
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/base.py:70` - String contains ambiguous `–` (EN DASH). Did you mean `-` (HYPHEN-MINUS)?
  - ID: a4f5ed73

## ruff:RUF002 (10 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/iterative_refinement/state.py:9` - Docstring contains ambiguous `–` (EN DASH). Did you mean `-` (HYPHEN-MINUS)?
  - ID: bb081850
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/iterative_refinement/state.py:35` - Docstring contains ambiguous `–` (EN DASH). Did you mean `-` (HYPHEN-MINUS)?
  - ID: fd98c7d9
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/iterative_refinement/state.py:43` - Docstring contains ambiguous `–` (EN DASH). Did you mean `-` (HYPHEN-MINUS)?
  - ID: 738dce73

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/arxiv_source.py:21` - Docstring contains ambiguous `–` (EN DASH). Did you mean `-` (HYPHEN-MINUS)?
  - ID: ce69d49d
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/arxiv_source.py:23` - Docstring contains ambiguous `–` (EN DASH). Did you mean `-` (HYPHEN-MINUS)?
  - ID: 02f67e5c
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/arxiv_source.py:23` - Docstring contains ambiguous `–` (EN DASH). Did you mean `-` (HYPHEN-MINUS)?
  - ID: 02f67e5c
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/arxiv_source.py:65` - Docstring contains ambiguous `–` (EN DASH). Did you mean `-` (HYPHEN-MINUS)?
  - ID: c5c83b44
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/arxiv_source.py:67` - Docstring contains ambiguous `–` (EN DASH). Did you mean `-` (HYPHEN-MINUS)?
  - ID: 95aeaea4
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/arxiv_source.py:67` - Docstring contains ambiguous `–` (EN DASH). Did you mean `-` (HYPHEN-MINUS)?
  - ID: 95aeaea4
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/arxiv_source.py:115` - Docstring contains ambiguous `–` (EN DASH). Did you mean `-` (HYPHEN-MINUS)?
  - ID: 85c2b030

## ruff:RUF003 (3 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/field_definition.py:114` - Comment contains ambiguous `–` (EN DASH). Did you mean `-` (HYPHEN-MINUS)?
  - ID: 8d746d88
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/types/tree_leaf.py:26` - Comment contains ambiguous `‑` (NON-BREAKING HYPHEN). Did you mean `-` (HYPHEN-MINUS)?
  - ID: 1e2d59d9
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/types/tree_leaf.py:51` - Comment contains ambiguous `‑` (NON-BREAKING HYPHEN). Did you mean `-` (HYPHEN-MINUS)?
  - ID: a6839780

## ruff:RUF005 (2 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo/tests/test_tool_step.py:228` - Consider `[*available_tools, calculator]` instead of concatenation
  - ID: 177dc2d4
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/factories/compatible_rag_factory.py:1123` - Consider iterable unpacking instead of concatenation
  - ID: 4d7d8385

## ruff:RUF006 (4 errors)

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/middleware/supabase_logging.py:363` - Store a reference to the return value of `asyncio.create_task`
  - ID: b644ec01
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/middleware/supabase_logging.py:435` - Store a reference to the return value of `asyncio.create_task`
  - ID: 00428839
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/discovery.py:992` - Store a reference to the return value of `asyncio.create_task`
  - ID: 55a7f4ae

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mixins/mcp_mixin.py:161` - Store a reference to the return value of `asyncio.create_task`
  - ID: 4a03a086

## ruff:RUF009 (4 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/declarative_chain.py:49` - Do not perform function call `Field` in dataclass defaults
  - ID: c0d96613
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/declarative_chain.py:50` - Do not perform function call `Field` in dataclass defaults
  - ID: ea945ce8
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/declarative_chain.py:51` - Do not perform function call `Field` in dataclass defaults
  - ID: 00f8eaaa
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/declarative_chain.py:53` - Do not perform function call `Field` in dataclass defaults
  - ID: 3b9a18e2

## ruff:RUF010 (15 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/supervisor/base_supervisor.py:150` - Use explicit conversion flag
  - ID: c90d59f3
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/supervisor/tools.py:70` - Use explicit conversion flag
  - ID: 6a607beb
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/supervisor/tools.py:132` - Use explicit conversion flag
  - ID: 08252a85
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/supervisor/tools.py:178` - Use explicit conversion flag
  - ID: 0fa4695d
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/supervisor/tools.py:230` - Use explicit conversion flag
  - ID: d46e7ce8
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/archive/example_dynamic_supervisor.py:211` - Use explicit conversion flag
  - ID: 1d123188
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/example_dynamic_supervisor.py:211` - Use explicit conversion flag
  - ID: ec39f54d

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:511` - Use explicit conversion flag
  - ID: 522c7894
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/types.py:533` - Use explicit conversion flag
  - ID: 4832717a
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/types.py:618` - Use explicit conversion flag
  - ID: 33af78c9
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/types.py:677` - Use explicit conversion flag
  - ID: 77655f7d
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/core/unified.py:480` - Use explicit conversion flag
  - ID: 2822ab4f
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/fallbacks.py:63` - Use explicit conversion flag
  - ID: b68ccbd3
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/fallbacks.py:179` - Use explicit conversion flag
  - ID: 3c3dfd3c
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/fallbacks.py:379` - Use explicit conversion flag
  - ID: f466a49c

## ruff:RUF012 (201 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/base/example.py:38` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: 49a0a329
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/base/examples/basic_state_management.py:133` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: 5fd3ff30
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/base/state.py:186` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: 35e8a6a0
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/collaberative/state.py:71` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: 9db88da5
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/debate/state.py:74` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: b7017f72
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/directed/agent.py:112` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: ebb4eb66
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/dynamic_supervisor/state.py:51` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: 44df37a5
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/dynamic_supervisor/state.py:273` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: 90e1db3b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models_dir/base.py:28` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: ab6d9d0f
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models_dir/meta.py:11` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: 0bfc0a4c
- ... and 94 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/tool_list_mixin.py:83` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: 3e2e2d19
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/config.py:124` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: c176bc79
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/config.py:128` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: 1fbc4894
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/base.py:73` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: 263bec73
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/base_new.py:105` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: 0d3f4c7a
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/base_new.py:108` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: 0cf1d331
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/base_new.py:114` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: 3b9815c1
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/path_analyzer.py:202` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: 8523bb87
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/path_analyzer.py:253` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: f3d9123a
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/path_analyzer.py:265` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: 35f1f637
- ... and 82 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:166` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: 2930e814
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/serialization.py:103` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: 7c54e068
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/serialization.py:104` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: a446ad46
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/serialization.py:25` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: 1d3ba0f4
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/serialization.py:26` - Mutable class attributes should be annotated with `typing.ClassVar`
  - ID: f6b56bc8

## ruff:RUF013 (27 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/agents/ltm.py:75` - PEP 484 prohibits implicit `Optional`
  - ID: c7208d64
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/agents/ltm.py:75` - PEP 484 prohibits implicit `Optional`
  - ID: c7208d64
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/agents/ltm.py:150` - PEP 484 prohibits implicit `Optional`
  - ID: 30de411e
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/agents/ltm.py:150` - PEP 484 prohibits implicit `Optional`
  - ID: 30de411e
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/agents/ltm.py:166` - PEP 484 prohibits implicit `Optional`
  - ID: a1c85502
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/models.py:310` - PEP 484 prohibits implicit `Optional`
  - ID: ff03798e
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/models.py:327` - PEP 484 prohibits implicit `Optional`
  - ID: 5b4f7ec5
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/models.py:923` - PEP 484 prohibits implicit `Optional`
  - ID: 1211e4fd
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/enhanced_plan_execute_v5/planner/prompts.py:189` - PEP 484 prohibits implicit `Optional`
  - ID: bd7dc1dc
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/enhanced_plan_execute_v5/planner/prompts.py:191` - PEP 484 prohibits implicit `Optional`
  - ID: 2bce6bf0
- ... and 14 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/core/unified.py:410` - PEP 484 prohibits implicit `Optional`
  - ID: fd0e164c
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/core/unified.py:411` - PEP 484 prohibits implicit `Optional`
  - ID: a6a07ebc
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/core/unified.py:412` - PEP 484 prohibits implicit `Optional`
  - ID: c1aac5e3

## ruff:RUF015 (2 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/static.py:1006` - Prefer `next(iter(results.values()))` over single element slice
  - ID: 4ab1b964
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/static.py:1104` - Prefer `next(iter(results.values()))` over single element slice
  - ID: a58c1886

## ruff:RUF021 (9 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/perplexity/pro_search/models.py:230` - Parenthesize `a and b` expressions when chaining `and` and `or` together, to make the precedence cle
  - ID: 40186edd

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:1363` - Parenthesize `a and b` expressions when chaining `and` and `or` together, to make the precedence cle
  - ID: 285043f4
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/agent_node_v3.py:320` - Parenthesize `a and b` expressions when chaining `and` and `or` together, to make the precedence cle
  - ID: 4e6d373e
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/message_transformation.py:247` - Parenthesize `a and b` expressions when chaining `and` and `or` together, to make the precedence cle
  - ID: 09030aa1
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/message_transformation.py:328` - Parenthesize `a and b` expressions when chaining `and` and `or` together, to make the precedence cle
  - ID: 47c6f6be
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:318` - Parenthesize `a and b` expressions when chaining `and` and `or` together, to make the precedence cle
  - ID: 4dcf0dd8
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py:399` - Parenthesize `a and b` expressions when chaining `and` and `or` together, to make the precedence cle
  - ID: fa41baae
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py:436` - Parenthesize `a and b` expressions when chaining `and` and `or` together, to make the precedence cle
  - ID: 34e3c1b9
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/tool_state.py:294` - Parenthesize `a and b` expressions when chaining `and` and `or` together, to make the precedence cle
  - ID: 117f042d

## ruff:RUF022 (39 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/__init__.py:104` - `__all__` is not sorted
  - ID: d738d637
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/__init__.py:119` - `__all__` is not sorted
  - ID: edfe03de
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/extended_chain.py:171` - `__all__` is not sorted
  - ID: fbd1225d
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/__init__.py:28` - `__all__` is not sorted
  - ID: 1dd218b2
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/__init__.py:231` - `__all__` is not sorted
  - ID: e3b2d5b8
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/__init__.py:70` - `__all__` is not sorted
  - ID: 7955fede
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/base/__init__.py:10` - `__all__` is not sorted
  - ID: 58968c94
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/__init__.py:87` - `__all__` is not sorted
  - ID: a6b3f017
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/base/memory_models_standalone.py:404` - `__all__` is not sorted
  - ID: 4f866880
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/base/memory_state_original.py:274` - `__all__` is not sorted
  - ID: b4d215ca
- ... and 13 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/__init__.py:158` - `__all__` is not sorted
  - ID: 207471b8
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/__init__.py:209` - `__all__` is not sorted
  - ID: d16b8647
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/__init__.py:167` - `__all__` is not sorted
  - ID: 541f8e21
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/embeddings/__init__.py:123` - `__all__` is not sorted
  - ID: a105a4df
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/retriever/__init__.py:129` - `__all__` is not sorted
  - ID: 59b10dde
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/vectorstore/__init__.py:161` - `__all__` is not sorted
  - ID: b408931f
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/__init__.py:110` - `__all__` is not sorted
  - ID: e8e104da
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/__init__.py:79` - `__all__` is not sorted
  - ID: 8ddf0845
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/benchmarking/__init__.py:21` - `__all__` is not sorted
  - ID: 49fe4d27
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/core/__init__.py:11` - `__all__` is not sorted
  - ID: 60ce456c
- ... and 4 more

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/servers/__init__.py:8` - `__all__` is not sorted
  - ID: 5947a288

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/search/__init__.py:24` - `__all__` is not sorted
  - ID: a1e54b0a

## ruff:RUF100 (1 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/compatibility.py:4` - Unused `noqa` directive (unused: `F401`)
  - ID: ebf8e32c

## ruff:SIM102 (129 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/hooks.py:388` - Use a single `if` statement instead of nested `if` statements
  - ID: 6624461e
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/execution_mixin.py:253` - Use a single `if` statement instead of nested `if` statements
  - ID: 039627f4
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/pre_post_agent_mixin.py:254` - Use a single `if` statement instead of nested `if` statements
  - ID: dece8946
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/pre_post_agent_mixin.py:299` - Use a single `if` statement instead of nested `if` statements
  - ID: 417f4c15
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/universal_agent.py:183` - Use a single `if` statement instead of nested `if` statements
  - ID: 445c504d
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/extended_chain.py:116` - Use a single `if` statement instead of nested `if` statements
  - ID: af4d7188
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/composite.py:91` - Use a single `if` statement instead of nested `if` statements
  - ID: fa8b6578
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/numeric.py:71` - Use a single `if` statement instead of nested `if` statements
  - ID: f280083b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/task_analysis/parallelization.py:703` - Use a single `if` statement instead of nested `if` statements
  - ID: fbfe0abd
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/task_analysis/solvability.py:123` - Use a single `if` statement instead of nested `if` statements
  - ID: c3920dcf
- ... and 54 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/prompt_template_mixin.py:247` - Use a single `if` statement instead of nested `if` statements
  - ID: b0a04b45
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/prompt_template_mixin.py:249` - Use a single `if` statement instead of nested `if` statements
  - ID: c7c3496e
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/structured_output_mixin.py:176` - Use a single `if` statement instead of nested `if` statements
  - ID: 216b9001
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py:2587` - Use a single `if` statement instead of nested `if` statements
  - ID: 8bf659cc
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py:2829` - Use a single `if` statement instead of nested `if` statements
  - ID: a78186ef
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py:2925` - Use a single `if` statement instead of nested `if` statements
  - ID: d6805186
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/config.py:359` - Use a single `if` statement instead of nested `if` statements
  - ID: 70e07f62
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/config.py:393` - Use a single `if` statement instead of nested `if` statements
  - ID: 9fbe4caa
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/config.py:436` - Use a single `if` statement instead of nested `if` statements
  - ID: b09b2d02
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/config.py:680` - Use a single `if` statement instead of nested `if` statements
  - ID: 1211760f
- ... and 45 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py:167` - Use a single `if` statement instead of nested `if` statements
  - ID: 50e61f94
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/discovery.py:704` - Use a single `if` statement instead of nested `if` statements
  - ID: ff84bc3b
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/importers/tak.py:405` - Use a single `if` statement instead of nested `if` statements
  - ID: 6690e166
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/discovery.py:747` - Use a single `if` statement instead of nested `if` statements
  - ID: cb208564
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/importers/tak.py:405` - Use a single `if` statement instead of nested `if` statements
  - ID: 2aa03e6f

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/transferable_mcp_agent.py:294` - Use a single `if` statement instead of nested `if` statements
  - ID: acd7fa05
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/github_mass_downloader.py:191` - Use a single `if` statement instead of nested `if` statements
  - ID: 0035ea52
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mixins/mcp_mixin.py:157` - Use a single `if` statement instead of nested `if` statements
  - ID: 1851c798

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/shell.py:123` - Use a single `if` statement instead of nested `if` statements
  - ID: a01dc2b8
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/shell.py:131` - Use a single `if` statement instead of nested `if` statements
  - ID: 0baee848

## ruff:SIM103 (7 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/llm_rag/agent.py:246` - Return the negated condition directly
  - ID: 0a9e452d
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/state2.py:83` - Return the condition directly
  - ID: 21e015e2
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/enhanced_agent_v3.v2.py:66` - Return the condition directly
  - ID: fc4f11c8
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic/dynamic_multi_agent.py:365` - Return the condition directly
  - ID: 4a0c9b89
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic_multi_agent.py:365` - Return the condition directly
  - ID: e8bf6552

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/pdf.py:98` - Return the negated condition directly
  - ID: 302fca55
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/tool_state.py:231` - Return the condition `bool(hasattr(engine, "tool_routes"))` directly
  - ID: a1080d4e

## ruff:SIM105 (37 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/enhanced_agent.py:35` - Use `contextlib.suppress(ImportError)` instead of `try`-`except`-`pass`
  - ID: ddb1671e
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/base/examples/basic_state_management.py:116` - Use `contextlib.suppress(ValueError)` instead of `try`-`except`-`pass`
  - ID: c904d4da
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_base/example.py:88` - Use `contextlib.suppress(Exception)` instead of `try`-`except`-`pass`
  - ID: adc9fbec
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/dynamic_supervisor.py:574` - Use `contextlib.suppress(Exception)` instead of `try`-`except`-`pass`
  - ID: b31bbb25
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/test_simple_memory_with_deepseek.py:42` - Use `contextlib.suppress(Exception)` instead of `try`-`except`-`pass`
  - ID: 147d07c9
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced/multi_agent_v4.py:109` - Use `contextlib.suppress(ImportError)` instead of `try`-`except`-`pass`
  - ID: 3a97451b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_v4.py:63` - Use `contextlib.suppress(ImportError)` instead of `try`-`except`-`pass`
  - ID: e772a55a
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react/agent.py:175` - Use `contextlib.suppress(Exception)` instead of `try`-`except`-`pass`
  - ID: 17186f3b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/example.py:30` - Use `contextlib.suppress(ImportError)` instead of `try`-`except`-`pass`
  - ID: 5d757622

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py:3598` - Use `contextlib.suppress(BaseException)` instead of `try`-`except`-`pass`
  - ID: 896dec43
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/factory.py:86` - Use `contextlib.suppress(ValueError)` instead of `try`-`except`-`pass`
  - ID: fb7aa371
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/Neo4jVectorStoreConfig.py:252` - Use `contextlib.suppress(Exception)` instead of `try`-`except`-`pass`
  - ID: 29072142
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/RedisVectorStoreConfig.py:279` - Use `contextlib.suppress(Exception)` instead of `try`-`except`-`pass`
  - ID: 83913e37
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/branches/branch.py:239` - Use `contextlib.suppress(ValueError)` instead of `try`-`except`-`pass`
  - ID: 3afb4e92
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/branch.py:277` - Use `contextlib.suppress(ValueError)` instead of `try`-`except`-`pass`
  - ID: 309f3c84
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/modular_base_graph.py:468` - Use `contextlib.suppress(Exception)` instead of `try`-`except`-`pass`
  - ID: 1a234d44
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/recompilation_demo.py:80` - Use `contextlib.suppress(Exception)` instead of `try`-`except`-`pass`
  - ID: 4ea5c492
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/serializable.py:414` - Use `contextlib.suppress(ValueError, TypeError)` instead of `try`-`except`-`pass`
  - ID: 24d3d116
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/serializable.py:422` - Use `contextlib.suppress(ValueError, TypeError)` instead of `try`-`except`-`pass`
  - ID: a2e9b12b
- ... and 5 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router.py:407` - Use `contextlib.suppress(BaseException)` instead of `try`-`except`-`pass`
  - ID: d1b96d94
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router_fixed.py:395` - Use `contextlib.suppress(BaseException)` instead of `try`-`except`-`pass`
  - ID: c3b788fc
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_socket.py:508` - Use `contextlib.suppress(ImportError)` instead of `try`-`except`-`pass`
  - ID: 0b5f30e7
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_socket.py:514` - Use `contextlib.suppress(ImportError)` instead of `try`-`except`-`pass`
  - ID: cc85df5d
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_socket.py:520` - Use `contextlib.suppress(ImportError)` instead of `try`-`except`-`pass`
  - ID: 0857c102
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/discovery.py:318` - Use `contextlib.suppress(Exception)` instead of `try`-`except`-`pass`
  - ID: b03ba43e
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/discovery.py:477` - Use `contextlib.suppress(Exception)` instead of `try`-`except`-`pass`
  - ID: 320b9e34
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/discovery.py:649` - Use `contextlib.suppress(Exception)` instead of `try`-`except`-`pass`
  - ID: e976cd1e
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/discovery.py:361` - Use `contextlib.suppress(Exception)` instead of `try`-`except`-`pass`
  - ID: 023f9018
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/discovery.py:520` - Use `contextlib.suppress(Exception)` instead of `try`-`except`-`pass`
  - ID: b4692289
- ... and 1 more

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/dynamic_activation_mcp.py:389` - Use `contextlib.suppress(Exception)` instead of `try`-`except`-`pass`
  - ID: c8363e1e
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mixins/mcp_mixin.py:146` - Use `contextlib.suppress(AttributeError)` instead of `try`-`except`-`pass`
  - ID: 3ea01ef4

## ruff:SIM108 (10 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain_agent.py:279` - Use ternary operator `result_str = result["output"] if "output" in result else json.dumps(result)` i
  - ID: 4e5f785f
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/utils.py:8` - Use ternary operator `msg_type = m.get("type", "") if isinstance(m, dict) else getattr(m, "type", ""
  - ID: f4765463
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/perplexity/pro_search/tasks/models.py:178` - Use ternary operator `level = 0 if not task.dependencies else 1` instead of `if`-`else`-block
  - ID: 1a51be83

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/config/runnable.py:439` - Use ternary operator `model_dict = model.model_dump() if hasattr(model, "model_dump") else model.dic
  - ID: 43b6640c
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/ToolManager.py:684` - Use ternary operator `result = tool_obj.run(args[0]) if len(args) == 1 else tool_obj.run(*args)` ins
  - ID: 2226dc80
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/composer/update_functions.py:112` - Use ternary operator `key = part.split("[")[0] if "[" in part else part` instead of `if`-`else`-bloc
  - ID: d09fa9c8
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/meta_agent_node.py:384` - Use ternary operator `updated_state = state.model_copy() if hasattr(state, "model_copy") else dict(s
  - ID: 2cd6ff96
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py:1567` - Use ternary operator `use_default = None if isinstance(destinations, dict) else default` instead of
  - ID: 389132e1
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/config.py:18` - Use ternary operator `env_name = "development" if env_var.endswith(".env") or "/" in env_var else en
  - ID: 75dd233f
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/config.py:302` - Use ternary operator `env_name = "development" if env_var.endswith(".env") or "/" in env_var else en
  - ID: 83640089

## ruff:SIM113 (4 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/execution_mixin.py:888` - Use `enumerate()` for index variable `chunk_count` in `for` loop
  - ID: d193d7b7
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/example.py:65` - Use `enumerate()` for index variable `step_count` in `for` loop
  - ID: 3b56be84
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/mcts/example.py:69` - Use `enumerate()` for index variable `step_count` in `for` loop
  - ID: e8d29a85

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/auto_loader.py:1050` - Use `enumerate()` for index variable `completed` in `for` loop
  - ID: 3d4076a6

## ruff:SIM114 (2 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:318` - Combine `if` branches using logical `or` operator
  - ID: 42cad66a
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/models.py:343` - Combine `if` branches using logical `or` operator
  - ID: 80bb4d16

## ruff:SIM117 (13 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py:3258` - Use a single `with` statement with multiple contexts instead of nested `with` statements
  - ID: a9fadf19
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py:3280` - Use a single `with` statement with multiple contexts instead of nested `with` statements
  - ID: 2677f753
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py:3345` - Use a single `with` statement with multiple contexts instead of nested `with` statements
  - ID: 0521eb01
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/manager.py:341` - Use a single `with` statement with multiple contexts instead of nested `with` statements
  - ID: d7ab5db8
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/postgres_config.py:164` - Use a single `with` statement with multiple contexts instead of nested `with` statements
  - ID: 7948d519

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/persistence/supabase_adapter.py:214` - Use a single `with` statement with multiple contexts instead of nested `with` statements
  - ID: 8c269183
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/persistence/supabase_adapter.py:266` - Use a single `with` statement with multiple contexts instead of nested `with` statements
  - ID: 8ced0941
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/persistence/supabase_adapter.py:302` - Use a single `with` statement with multiple contexts instead of nested `with` statements
  - ID: 5834b156
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/persistence/supabase_adapter.py:336` - Use a single `with` statement with multiple contexts instead of nested `with` statements
  - ID: f87bee28
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/persistence/supabase_adapter.py:410` - Use a single `with` statement with multiple contexts instead of nested `with` statements
  - ID: d80bf5e4

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/installers.py:644` - Use a single `with` statement with multiple contexts instead of nested `with` statements
  - ID: 7b333ce1
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/installers.py:766` - Use a single `with` statement with multiple contexts instead of nested `with` statements
  - ID: e1b9158c
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/legacy_core.py:617` - Use a single `with` statement with multiple contexts instead of nested `with` statements
  - ID: 5898b6eb

## ruff:SIM401 (3 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/archive/experiments/routing_patterns.py:195` - Use `node_routes[key] = agent_nodes.get(dest, dest)` instead of an `if` block
  - ID: e4f27e41
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/routing_patterns.py:195` - Use `node_routes[key] = agent_nodes.get(dest, dest)` instead of an `if` block
  - ID: e75f6df9
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler/models.py:77` - Use `resolved_args[key] = results.get(step_id, value)` instead of an `if` block
  - ID: 3414ced4

## ruff:T201 (128 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/agents/ltm.py:497` - `print` found
  - ID: bb75dbb1
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/agents/ltm.py:504` - `print` found
  - ID: 25941a53
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/agents/ltm.py:514` - `print` found
  - ID: db489b5f
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/agents/ltm.py:527` - `print` found
  - ID: ed105cf7
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/agents/ltm.py:528` - `print` found
  - ID: 69742b72
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/agents/ltm.py:529` - `print` found
  - ID: ea891955
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/agents/ltm.py:532` - `print` found
  - ID: 7ca3e658
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/agents/ltm.py:536` - `print` found
  - ID: 754403ce
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/agents/ltm.py:537` - `print` found
  - ID: 7c0d49b4
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/agents/ltm.py:538` - `print` found
  - ID: 30eb395f
- ... and 95 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/fallbacks.py:66` - `print` found
  - ID: a52ccc87
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/fallbacks.py:94` - `print` found
  - ID: e2af72a0
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/fallbacks.py:114` - `print` found
  - ID: 444a72d8
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/fallbacks.py:117` - `print` found
  - ID: bd40d625
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/fallbacks.py:123` - `print` found
  - ID: 5e0ae626
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/fallbacks.py:194` - `print` found
  - ID: 7c81b482
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/fallbacks.py:205` - `print` found
  - ID: a8b078e7
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/fallbacks.py:216` - `print` found
  - ID: 74642812
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/fallbacks.py:227` - `print` found
  - ID: d5c4f6c5
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/fallbacks.py:238` - `print` found
  - ID: 5e8762d6
- ... and 13 more

## ruff:TID252 (2 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/agents/planner.py:12` - Prefer absolute imports over relative imports from parent modules
  - ID: d0d5c14c
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/agents/planner.py:12` - Prefer absolute imports over relative imports from parent modules
  - ID: d0d5c14c

## ruff:TRY002 (18 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/hooks.py:428` - Create your own exception
  - ID: 4dc37496
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/unified_memory_api.py:709` - Create your own exception
  - ID: 81e87fda
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/unified_memory_api.py:758` - Create your own exception
  - ID: cb671a44
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/unified_memory_api.py:904` - Create your own exception
  - ID: 2c625d17
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/api/unified_memory_api.py:711` - Create your own exception
  - ID: 914ec991
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/api/unified_memory_api.py:760` - Create your own exception
  - ID: 19842ec6
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/api/unified_memory_api.py:906` - Create your own exception
  - ID: 00550691
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler_v3/examples/basic_example.py:124` - Create your own exception
  - ID: bd3b0718

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/importers/tak.py:175` - Create your own exception
  - ID: 80f0fc35
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/importers/tak.py:239` - Create your own exception
  - ID: e3fe1d7f
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/importers/tak.py:309` - Create your own exception
  - ID: c86d7653
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/importers/tak.py:175` - Create your own exception
  - ID: b1732bf2
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/importers/tak.py:239` - Create your own exception
  - ID: f50a6348
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/importers/tak.py:309` - Create your own exception
  - ID: 847b2db2

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/dynamic_mcp_tool.py:267` - Create your own exception
  - ID: bdcd8753
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/production_mcp_tool.py:383` - Create your own exception
  - ID: 1c4e056b
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/production_mcp_tool.py:404` - Create your own exception
  - ID: 1e689e15

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/google_calendar.py:104` - Create your own exception
  - ID: 5bde2251

## ruff:TRY004 (21 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/rubric.py:351` - Prefer `TypeError` exception for invalid type
  - ID: fee955ee
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/__init__.py:480` - Prefer `TypeError` exception for invalid type
  - ID: 52a414e0
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_iterative_refinement/state.py:46` - Prefer `TypeError` exception for invalid type
  - ID: 93d1c62b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/archive/enhanced_multi_agent_generic.py:132` - Prefer `TypeError` exception for invalid type
  - ID: a069fc64
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/archive/enhanced_multi_agent_standalone.py:153` - Prefer `TypeError` exception for invalid type
  - ID: b82e9f3c
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/archive/enhanced_supervisor_agent.py:103` - Prefer `TypeError` exception for invalid type
  - ID: 3bb8fffc
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/archive/experiments/implementations/clean_base.py:48` - Prefer `TypeError` exception for invalid type
  - ID: 062ddb6c
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/archive/experiments/implementations/clean_multi_agent.py:92` - Prefer `TypeError` exception for invalid type
  - ID: 39486a3a
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/archive/experiments/implementations/proper_base.py:146` - Prefer `TypeError` exception for invalid type
  - ID: 40d1b71a
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced/multi_agent_v3.py:416` - Prefer `TypeError` exception for invalid type
  - ID: 573d4891
- ... and 11 more

## ruff:TRY203 (3 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/archive/experiments/test_proper_usage.py:312` - Remove exception handler; error is immediately re-raised
  - ID: d279a900
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/test_proper_usage.py:312` - Remove exception handler; error is immediately re-raised
  - ID: fb13c56c
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/enhanced_multi_rag.py:312` - Remove exception handler; error is immediately re-raised
  - ID: 861fbf48

## ruff:TRY300 (448 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:361` - Consider moving this statement to an `else` block
  - ID: 81c46412
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:430` - Consider moving this statement to an `else` block
  - ID: e2ce3e99
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:532` - Consider moving this statement to an `else` block
  - ID: 7911610c
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:607` - Consider moving this statement to an `else` block
  - ID: 6cc56249
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:648` - Consider moving this statement to an `else` block
  - ID: 80c5b573
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:668` - Consider moving this statement to an `else` block
  - ID: 78de9033
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:681` - Consider moving this statement to an `else` block
  - ID: dab063a4
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:392` - Consider moving this statement to an `else` block
  - ID: 69da83d0
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/enhanced_agent.py:538` - Consider moving this statement to an `else` block
  - ID: 2480633f
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/execution_mixin.py:106` - Consider moving this statement to an `else` block
  - ID: 60845947
- ... and 248 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/db.py:36` - Consider moving this statement to an `else` block
  - ID: 321831a1
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_api.py:314` - Consider moving this statement to an `else` block
  - ID: 124db728
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py:292` - Consider moving this statement to an `else` block
  - ID: a0ec32e0
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py:300` - Consider moving this statement to an `else` block
  - ID: 74c08f18
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py:308` - Consider moving this statement to an `else` block
  - ID: 18b9fad4
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py:494` - Consider moving this statement to an `else` block
  - ID: eb08d804
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/general_games_api.py:246` - Consider moving this statement to an `else` block
  - ID: 524941bc
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/integrate_games.py:91` - Consider moving this statement to an `else` block
  - ID: 3fb3ece9
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/middleware.py:54` - Consider moving this statement to an `else` block
  - ID: 6f2b2971
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/middleware/logging.py:51` - Consider moving this statement to an `else` block
  - ID: cdd49dcb
- ... and 137 more

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/comprehensive_mcp_web.py:640` - Consider moving this statement to an `else` block
  - ID: 4e32aedc
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/discovery/analyzer.py:249` - Consider moving this statement to an `else` block
  - ID: 6c7fd27b
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/discovery/analyzer.py:303` - Consider moving this statement to an `else` block
  - ID: 22aa9723
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/documentation/doc_loader.py:118` - Consider moving this statement to an `else` block
  - ID: aaf5e879
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/core.py:697` - Consider moving this statement to an `else` block
  - ID: f4157ae8
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/integration.py:135` - Consider moving this statement to an `else` block
  - ID: 86cb9507
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/legacy_core.py:271` - Consider moving this statement to an `else` block
  - ID: 5d67fd1e
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/legacy_core.py:701` - Consider moving this statement to an `else` block
  - ID: a464b76f
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/dynamic_activation_mcp.py:362` - Consider moving this statement to an `else` block
  - ID: e960720c
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/enhance_mcp_data.py:303` - Consider moving this statement to an `else` block
  - ID: c46573b7
- ... and 28 more

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/pokebase_tool.py:83` - Consider moving this statement to an `else` block
  - ID: ea90b487
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/background_process_manager.py:90` - Consider moving this statement to an `else` block
  - ID: 7f8649e7
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/background_process_manager.py:180` - Consider moving this statement to an `else` block
  - ID: 08e16893
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/google_calendar.py:101` - Consider moving this statement to an `else` block
  - ID: 90f37454
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/translate_tools.py:186` - Consider moving this statement to an `else` block
  - ID: 517ead23

## ruff:TRY301 (70 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent_structured_output_mixin.py:262` - Abstract `raise` to an inner function
  - ID: e1f5eea8
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/state_mixin.py:302` - Abstract `raise` to an inner function
  - ID: 20e7c19f
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_processing/agent.py:326` - Abstract `raise` to an inner function
  - ID: e927b493
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_processing/agent.py:340` - Abstract `raise` to an inner function
  - ID: 625b6edb
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_processing/agent.py:354` - Abstract `raise` to an inner function
  - ID: a521849b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_processing/agent.py:366` - Abstract `raise` to an inner function
  - ID: 9eb6eef8
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/multi_agent_coordinator.py:861` - Abstract `raise` to an inner function
  - ID: 21feb6a8
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/unified_memory_api.py:709` - Abstract `raise` to an inner function
  - ID: 289be025
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/unified_memory_api.py:758` - Abstract `raise` to an inner function
  - ID: 1334aeea
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/unified_memory_api.py:904` - Abstract `raise` to an inner function
  - ID: b9f02b27
- ... and 19 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/base.py:292` - Abstract `raise` to an inner function
  - ID: 9e656c69
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/base.py:301` - Abstract `raise` to an inner function
  - ID: 8822514d
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_api.py:289` - Abstract `raise` to an inner function
  - ID: 4dd7835b
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router.py:100` - Abstract `raise` to an inner function
  - ID: ce95d41d
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router_fixed.py:186` - Abstract `raise` to an inner function
  - ID: a1ea16c9
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/registry.py:356` - Abstract `raise` to an inner function
  - ID: 324b2ee5
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/router.py:111` - Abstract `raise` to an inner function
  - ID: 0ff6c02f
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routers/games.py:87` - Abstract `raise` to an inner function
  - ID: 5503e9cd
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes.py:347` - Abstract `raise` to an inner function
  - ID: 9ce27b4e
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes.py:451` - Abstract `raise` to an inner function
  - ID: 662a0a4d
- ... and 27 more

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/dynamic_mcp_tool.py:267` - Abstract `raise` to an inner function
  - ID: 7ef16cc7
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/manager.py:360` - Abstract `raise` to an inner function
  - ID: f4222ba3
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/manager.py:362` - Abstract `raise` to an inner function
  - ID: 515ad10a
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/production_mcp_tool.py:404` - Abstract `raise` to an inner function
  - ID: 9fa7f318

## ruff:TRY400 (9 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/agent.py:178` - Use `logging.exception` instead of `logging.error`
  - ID: f5319851
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/agent.py:210` - Use `logging.exception` instead of `logging.error`
  - ID: ab4a3af5
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/agent.py:262` - Use `logging.exception` instead of `logging.error`
  - ID: 32c1de86
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/agent.py:294` - Use `logging.exception` instead of `logging.error`
  - ID: 4c2d80a6
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/agent.py:333` - Use `logging.exception` instead of `logging.error`
  - ID: 59f3d467
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/agent.py:382` - Use `logging.exception` instead of `logging.error`
  - ID: 9d56e80a
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/smart_parsing_example.py:337` - Use `logging.exception` instead of `logging.error`
  - ID: 9571ceaa
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/structured_tools.py:674` - Use `logging.exception` instead of `logging.error`
  - ID: f00eebcc
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/structured_tools.py:700` - Use `logging.exception` instead of `logging.error`
  - ID: d99eebf3

## ruff:TRY401 (908 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:363` - Redundant exception object included in `logging.exception` call
  - ID: 05cc01a2
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:438` - Redundant exception object included in `logging.exception` call
  - ID: 77299915
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:535` - Redundant exception object included in `logging.exception` call
  - ID: 9219124b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:610` - Redundant exception object included in `logging.exception` call
  - ID: 82cb114f
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:613` - Redundant exception object included in `logging.exception` call
  - ID: 25f8de22
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:651` - Redundant exception object included in `logging.exception` call
  - ID: 04cf50d1
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:670` - Redundant exception object included in `logging.exception` call
  - ID: ae4e0c4c
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py:683` - Redundant exception object included in `logging.exception` call
  - ID: 5b283744
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:185` - Redundant exception object included in `logging.exception` call
  - ID: 6799f94a
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:485` - Redundant exception object included in `logging.exception` call
  - ID: 034c1b45
- ... and 433 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/db.py:38` - Redundant exception object included in `logging.exception` call
  - ID: 95a6594d
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/db.py:62` - Redundant exception object included in `logging.exception` call
  - ID: 9bbaba98
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/db.py:152` - Redundant exception object included in `logging.exception` call
  - ID: f510b783
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/db.py:249` - Redundant exception object included in `logging.exception` call
  - ID: 70f5c588
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/db.py:300` - Redundant exception object included in `logging.exception` call
  - ID: 637c0619
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_agent.py:230` - Redundant exception object included in `logging.exception` call
  - ID: e1a29601
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_agent.py:261` - Redundant exception object included in `logging.exception` call
  - ID: bb5a506a
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router.py:72` - Redundant exception object included in `logging.exception` call
  - ID: 73e6c137
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router.py:75` - Redundant exception object included in `logging.exception` call
  - ID: 58f06042
- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router.py:95` - Redundant exception object included in `logging.exception` call
  - ID: 5dabd289
- ... and 381 more

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/documentation_agent.py:373` - Redundant exception object included in `logging.exception` call
  - ID: 1310bed8
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:254` - Redundant exception object included in `logging.exception` call
  - ID: 4d216622
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:330` - Redundant exception object included in `logging.exception` call
  - ID: 4bcfc87f
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:425` - Redundant exception object included in `logging.exception` call
  - ID: 73b745d6
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:483` - Redundant exception object included in `logging.exception` call
  - ID: a874c728
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:573` - Redundant exception object included in `logging.exception` call
  - ID: 16506620
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/discovery/analyzer.py:187` - Redundant exception object included in `logging.exception` call
  - ID: f027be80
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/discovery/analyzer.py:252` - Redundant exception object included in `logging.exception` call
  - ID: 2e56ad9c
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/discovery/analyzer.py:306` - Redundant exception object included in `logging.exception` call
  - ID: f8ceba7a
- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/discovery/analyzer.py:462` - Redundant exception object included in `logging.exception` call
  - ID: 7766449c
- ... and 64 more

## ruff:UP006 (371 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/declarative_chain.py:24` - Use `list` instead of `List` for type annotation
  - ID: 4b2cf16a
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/declarative_chain.py:31` - Use `dict` instead of `Dict` for type annotation
  - ID: 515eafe3
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/declarative_chain.py:32` - Use `dict` instead of `Dict` for type annotation
  - ID: 0a02bf53
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/declarative_chain.py:41` - Use `dict` instead of `Dict` for type annotation
  - ID: bcb62c62
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/declarative_chain.py:48` - Use `list` instead of `List` for type annotation
  - ID: 617fb93b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/declarative_chain.py:49` - Use `list` instead of `List` for type annotation
  - ID: a6147bdd
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/declarative_chain.py:50` - Use `list` instead of `List` for type annotation
  - ID: c6d96554
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/declarative_chain.py:51` - Use `list` instead of `List` for type annotation
  - ID: 08b9cdc9
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/declarative_chain.py:53` - Use `list` instead of `List` for type annotation
  - ID: c50638f3
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/declarative_chain.py:61` - Use `list` instead of `List` for type annotation
  - ID: c1336633
- ... and 199 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/registry/__init__.py:98` - Use `dict` instead of `Dict` for type annotation
  - ID: 5fbaaedb
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/compatibility.py:22` - Use `dict` instead of `Dict` for type annotation
  - ID: d903db04
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/compatibility.py:23` - Use `type` instead of `Type` for type annotation
  - ID: 82aff55d
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/compatibility.py:23` - Use `type` instead of `Type` for type annotation
  - ID: 82aff55d
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/compatibility.py:27` - Use `type` instead of `Type` for type annotation
  - ID: 4dcaaf59
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/compatibility.py:27` - Use `type` instead of `Type` for type annotation
  - ID: 4dcaaf59
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/compatibility.py:40` - Use `type` instead of `Type` for type annotation
  - ID: 70f7c56f
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/compatibility.py:40` - Use `type` instead of `Type` for type annotation
  - ID: 70f7c56f
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/compatibility.py:74` - Use `type` instead of `Type` for type annotation
  - ID: ed90bf65
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/compatibility.py:74` - Use `type` instead of `Type` for type annotation
  - ID: ed90bf65
- ... and 152 more

## ruff:UP007 (333 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:60` - Use `X | Y` for type annotations
  - ID: 9b7f73b0
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:260` - Use `X | Y` for type annotations
  - ID: 000db284
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:298` - Use `X | Y` for type annotations
  - ID: 1452f502
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:316` - Use `X | Y` for type annotations
  - ID: 374a2ee3
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:335` - Use `X | Y` for type annotations
  - ID: e436fbf7
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:367` - Use `X | Y` for type annotations
  - ID: ad1f85dc
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:368` - Use `X | Y` for type annotations
  - ID: a3d320e4
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:369` - Use `X | Y` for type annotations
  - ID: 8df3c7a1
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/chain_agent_simple.py:24` - Use `X | Y` for type annotations
  - ID: 4e9f7661
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/chain_agent_simple.py:27` - Use `X | Y` for type annotations
  - ID: 2cbbda74
- ... and 165 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/types/__init__.py:10` - Use `X | Y` for type annotations
  - ID: fc807a1e
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/types/__init__.py:11` - Use `X | Y` for type annotations
  - ID: ecbb8cb2
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/types/general.py:40` - Use `X | Y` for type annotations
  - ID: 419dc4b6
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/types/general.py:41` - Use `X | Y` for type annotations
  - ID: cdba4a7f
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/types/general.py:42` - Use `X | Y` for type annotations
  - ID: bf519a0b
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:100` - Use `X | Y` for type annotations
  - ID: 4b4bf575
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:100` - Use `X | Y` for type annotations
  - ID: 4b4bf575
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:803` - Use `X | Y` for type annotations
  - ID: d51ca6a6
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:811` - Use `X | Y` for type annotations
  - ID: 4a06e72b
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:814` - Use `X | Y` for type annotations
  - ID: e6fb5934
- ... and 147 more

### haive-dataflow

- `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_api.py:410` - Use `X | Y` for type annotations
  - ID: 295b6d75

## ruff:UP015 (1 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/types.py:597` - Unnecessary mode argument
  - ID: 46ad78eb

## ruff:UP034 (132 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/composite.py:87` - Avoid extraneous parentheses
  - ID: 1ceaaa5a
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/composite.py:142` - Avoid extraneous parentheses
  - ID: df72d13b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/composite.py:193` - Avoid extraneous parentheses
  - ID: 652e3a58
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/composite.py:208` - Avoid extraneous parentheses
  - ID: 722b25ab
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/composite.py:282` - Avoid extraneous parentheses
  - ID: 4a20239b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/rubric.py:185` - Avoid extraneous parentheses
  - ID: a20b8a8b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/rubric.py:186` - Avoid extraneous parentheses
  - ID: 0d3fd191
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/rubric.py:197` - Avoid extraneous parentheses
  - ID: 079e4328
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/rubric.py:205` - Avoid extraneous parentheses
  - ID: 981a0932
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/task_analysis/analysis.py:307` - Avoid extraneous parentheses
  - ID: 26194925
- ... and 67 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/config.py:323` - Avoid extraneous parentheses
  - ID: e7a265f0
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:91` - Avoid extraneous parentheses
  - ID: c7b65625
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:969` - Avoid extraneous parentheses
  - ID: 986251ea
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:1019` - Avoid extraneous parentheses
  - ID: 207e1936
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:1363` - Avoid extraneous parentheses
  - ID: 65c58f98
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/config.py:289` - Avoid extraneous parentheses
  - ID: 2c65f921
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/config.py:291` - Avoid extraneous parentheses
  - ID: 426bdb97
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/config.py:292` - Avoid extraneous parentheses
  - ID: 5a0f2d93
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/config.py:293` - Avoid extraneous parentheses
  - ID: b9f17f98
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/branches/branch.py:94` - Avoid extraneous parentheses
  - ID: a8f92890
- ... and 37 more

### haive-games

- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/models.py:593` - Avoid extraneous parentheses
  - ID: 2821242d
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/models.py:596` - Avoid extraneous parentheses
  - ID: 24d90a18
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/models.py:1044` - Avoid extraneous parentheses
  - ID: 236efc0f
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/models.py:1070` - Avoid extraneous parentheses
  - ID: 2907b63f
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/models.py:1081` - Avoid extraneous parentheses
  - ID: a4918682
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/components/cards/actions.py:71` - Avoid extraneous parentheses
  - ID: a827131c
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/agent.py:150` - Avoid extraneous parentheses
  - ID: 3ecfc341
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:188` - Avoid extraneous parentheses
  - ID: a30bfb49

## ruff:UP035 (104 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:8` - Import from `collections.abc` instead: `Callable`
  - ID: 2672ba05
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/declarative_chain.py:8` - Import from `collections.abc` instead: `Callable`
  - ID: 57269219
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/declarative_chain.py:8` - Import from `collections.abc` instead: `Callable`
  - ID: 57269219
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/declarative_chain.py:8` - Import from `collections.abc` instead: `Callable`
  - ID: 57269219
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/extended_chain.py:9` - Import from `collections.abc` instead: `Callable`
  - ID: 7d15e881
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/extended_chain.py:9` - Import from `collections.abc` instead: `Callable`
  - ID: 7d15e881
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/extended_chain.py:9` - Import from `collections.abc` instead: `Callable`
  - ID: 7d15e881
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/__init__.py:133` - `typing.Dict` is deprecated, use `dict` instead
  - ID: 8d2ef6c0
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/__init__.py:133` - `typing.Dict` is deprecated, use `dict` instead
  - ID: 8d2ef6c0
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/__init__.py:133` - `typing.Dict` is deprecated, use `dict` instead
  - ID: 8d2ef6c0
- ... and 57 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/registry/__init__.py:89` - `typing.Dict` is deprecated, use `dict` instead
  - ID: e9d54e0f
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/compatibility.py:6` - `typing.Dict` is deprecated, use `dict` instead
  - ID: 8d31a6f6
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/compatibility.py:6` - `typing.Dict` is deprecated, use `dict` instead
  - ID: 8d31a6f6
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/compatibility.py:6` - `typing.Dict` is deprecated, use `dict` instead
  - ID: 8d31a6f6
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/compatibility.py:6` - `typing.Dict` is deprecated, use `dict` instead
  - ID: 8d31a6f6
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/converters.py:6` - Import from `collections.abc` instead: `Callable`
  - ID: 42d02a78
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/converters.py:6` - Import from `collections.abc` instead: `Callable`
  - ID: 42d02a78
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/converters.py:6` - Import from `collections.abc` instead: `Callable`
  - ID: 42d02a78
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/converters.py:6` - Import from `collections.abc` instead: `Callable`
  - ID: 42d02a78
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/converters.py:6` - Import from `collections.abc` instead: `Callable`
  - ID: 42d02a78
- ... and 27 more

## ruff:UP037 (12 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/extended_chain.py:64` - Remove quotes from type annotation
  - ID: f3b963c2
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/extended_chain.py:70` - Remove quotes from type annotation
  - ID: 209b8826
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/base/memory_models_standalone.py:66` - Remove quotes from type annotation
  - ID: f2de9347
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/base/memory_models_standalone.py:159` - Remove quotes from type annotation
  - ID: 22780a33
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/base/memory_models_standalone.py:296` - Remove quotes from type annotation
  - ID: 91abd005
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/base/memory_models_standalone.py:307` - Remove quotes from type annotation
  - ID: c8f0b81f
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/models.py:134` - Remove quotes from type annotation
  - ID: 391f8625
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/models.py:310` - Remove quotes from type annotation
  - ID: 689b4a65
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/base/models.py:735` - Remove quotes from type annotation
  - ID: 6ff95fc1

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/core/unified.py:241` - Remove quotes from type annotation
  - ID: b1d0af4b
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/core/unified.py:242` - Remove quotes from type annotation
  - ID: a2e87e2a
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/core/unified.py:243` - Remove quotes from type annotation
  - ID: a139a3fa

## ruff:UP038 (3 errors)

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/handlers.py:320` - Use `X | Y` in `isinstance` call instead of `(X, Y)`
  - ID: 9ab04175
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/analysis/complexity.py:891` - Use `X | Y` in `isinstance` call instead of `(X, Y)`
  - ID: 917070e3
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/debugkit/config.py:478` - Use `X | Y` in `isinstance` call instead of `(X, Y)`
  - ID: 0fb8909f

## ruff:W291 (76 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:176` - Trailing whitespace
  - ID: 16ad18b3
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/extended_chain.py:173` - Trailing whitespace
  - ID: 542d064b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/__init__.py:62` - Trailing whitespace
  - ID: 47078928
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/__init__.py:73` - Trailing whitespace
  - ID: 6a9eaa23
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/base/__init__.py:12` - Trailing whitespace
  - ID: a5bed85d
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/config.py:79` - Trailing whitespace
  - ID: 92e16c24
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/config.py:96` - Trailing whitespace
  - ID: 4378fb31
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/supervisor/state_models.py:62` - Trailing whitespace
  - ID: 4f109203
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/supervisor/state_models.py:66` - Trailing whitespace
  - ID: b9c49627
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/supervisor/state_models.py:70` - Trailing whitespace
  - ID: bd60f853
- ... and 64 more

### haive-prebuilt

- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/simple/tagger/prompts.py:7` - Trailing whitespace
  - ID: c298face
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/simple/tagger/prompts.py:8` - Trailing whitespace
  - ID: 870dda2c

## ruff:W292 (142 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py:983` - No newline at end of file
  - ID: e95e8fab
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/compiled_agent.py:210` - No newline at end of file
  - ID: 898feb7e
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/enhanced_agent.py:584` - No newline at end of file
  - ID: 133710bd
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:448` - No newline at end of file
  - ID: f2db9a62
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/extended_chain.py:182` - No newline at end of file
  - ID: b05d16b2
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/composite.py:315` - No newline at end of file
  - ID: fdd806bf
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/numeric.py:266` - No newline at end of file
  - ID: 6abfa28b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/qualitative.py:285` - No newline at end of file
  - ID: fc6fb831
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/rubric.py:353` - No newline at end of file
  - ID: 487a5104
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/scale.py:324` - No newline at end of file
  - ID: 4fce8cf5
- ... and 97 more

### haive-core

- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/documents/github_repo.py:306` - No newline at end of file
  - ID: 01e39f77
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/config.py:924` - No newline at end of file
  - ID: 77c1a2da
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py:1725` - No newline at end of file
  - ID: 511ade53
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/engine.py:444` - No newline at end of file
  - ID: c64687f1
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/agent_node_v2.py:299` - No newline at end of file
  - ID: b7a58acb
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/agent_node_v3.py:973` - No newline at end of file
  - ID: 5d0c68d5
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/intelligent_multi_agent_node.py:245` - No newline at end of file
  - ID: f756fc02
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/multi_agent_node.py:202` - No newline at end of file
  - ID: cf172a72
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/tool_node_config_v2.py:276` - No newline at end of file
  - ID: 3194dff1
- `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py:2937` - No newline at end of file
  - ID: 43fab21e
- ... and 3 more

### haive-games

- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/config.py:266` - No newline at end of file
  - ID: 967bdd7a
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/models.py:1126` - No newline at end of file
  - ID: 84e56747
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/poker/actions.py:223` - No newline at end of file
  - ID: fbd27ed3
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/poker/state.py:196` - No newline at end of file
  - ID: dbf670b7
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/config.py:117` - No newline at end of file
  - ID: 2ce9ea28
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/configurable_config.py:189` - No newline at end of file
  - ID: 3e9a609c
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/configurable_config.py:184` - No newline at end of file
  - ID: dcfeaf1e
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/components/cards/actions.py:84` - No newline at end of file
  - ID: 8c3ab88c
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/config/base.py:226` - No newline at end of file
  - ID: 9287a632
- `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/agent.py:229` - No newline at end of file
  - ID: b6a9dbfc
- ... and 5 more

### haive-mcp

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/dynamic_activation_mcp.py:499` - No newline at end of file
  - ID: f1b5f614

### haive-prebuilt

- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/journalism_/models.py:354` - No newline at end of file
  - ID: efa927ff
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/simple/questiona_and_answer_generator/models.py:12` - No newline at end of file
  - ID: aa53e4bd
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/startup/ideation/models.py:470` - No newline at end of file
  - ID: 32751c6c
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/startup/pitchdeck/models.py:415` - No newline at end of file
  - ID: 4f68e0e0
- `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive/prebuilt/tldr2/models.py:254` - No newline at end of file
  - ID: d07319e7

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/search/__init__.py:35` - No newline at end of file
  - ID: 5f2ba3cc

## ruff:W293 (915 errors)

### haive-agents

- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent_structured_output_mixin.py:253` - Blank line contains whitespace
  - ID: 54b1bcff
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/execution_mixin.py:371` - Blank line contains whitespace
  - ID: 8b9b0e57
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:31` - Blank line contains whitespace
  - ID: b2d7f896
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:36` - Blank line contains whitespace
  - ID: 87df53ce
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:42` - Blank line contains whitespace
  - ID: 75e00fca
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:47` - Blank line contains whitespace
  - ID: f3247a7b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:50` - Blank line contains whitespace
  - ID: 57151d1b
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:54` - Blank line contains whitespace
  - ID: a340a823
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:59` - Blank line contains whitespace
  - ID: 7781b613
- `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/smart_output_parsing.py:63` - Blank line contains whitespace
  - ID: d09c3347
- ... and 889 more

### haive-tools

- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_books.py:70` - Blank line contains whitespace
  - ID: cffde41a
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_books.py:76` - Blank line contains whitespace
  - ID: 50a84938
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_finance.py:70` - Blank line contains whitespace
  - ID: 78fc6f13
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_finance.py:76` - Blank line contains whitespace
  - ID: 65328860
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_jobs.py:87` - Blank line contains whitespace
  - ID: c9d1336b
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_jobs.py:93` - Blank line contains whitespace
  - ID: 869b880b
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_lens.py:84` - Blank line contains whitespace
  - ID: 10ddd7d8
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_lens.py:90` - Blank line contains whitespace
  - ID: a2c7e57f
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_places.py:72` - Blank line contains whitespace
  - ID: 71419512
- `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_places.py:78` - Blank line contains whitespace
  - ID: d0853922
- ... and 6 more
