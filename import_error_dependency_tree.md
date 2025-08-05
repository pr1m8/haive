# Import Error Dependency Tree Visualization

Total Errors: 1069

## Error Type Hierarchy

```
Import Errors (1069 total)
├── AttributeError (19)
│   ├── haive-agents (16 errors)
│   │   ├── haive.agents.reflection.state → no attribute: MESSAGE_TRANSFORMER
│   │   ├── haive.agents.reflection.models → no attribute: MESSAGE_TRANSFORMER
│   │   ├── haive.agents.reflection.multi_agent_reflection → no attribute: MESSAGE_TRANSFORMER
│   │   └── ... and 13 more
│   ├── haive-core (3 errors)
│   │   ├── haive.core.graph.node.agent_node_v2 → no attribute: COORDINATOR
│   │   ├── haive.core.graph.node.message_transformation_v2 → no attribute: MESSAGE_TRANSFORMER
│   │   ├── haive.core.graph.node.multi_agent_node → no attribute: TRANSFORM
├── ImportError (390)
│   ├── haive-agents (200 errors)
│   │   ├── haive.agents.qa_agent → cannot import: SimpleAgentConfig
│   │   ├── haive.agents.routing_agent → cannot import: SimpleAgentSchema
│   │   ├── haive.agents.chain.multi_integration → cannot import: build_graph
│   │   └── ... and 197 more
│   ├── haive-core (34 errors)
│   │   ├── haive.core.persistence.supabase_config → cannot import: SupabaseCheckpointerConfig
│   │   ├── haive.core.schema.example → cannot import: create_age
│   │   ├── haive.core.graph.graph_builder2 → cannot import: register_node
│   │   └── ... and 31 more
│   ├── haive-dataflow (5 errors)
│   │   ├── haive.dataflow.conversations.manager → cannot import: SupabaseServerConfig
│   │   ├── haive.dataflow.bin.litellm_cli → cannot import: update_availability_status
│   │   ├── haive.dataflow.api.routes.conversation_routes → cannot import: AgentRegistry
│   │   └── ... and 2 more
│   ├── haive-games (43 errors)
│   │   ├── haive.games.benchmark → cannot import: MonopolyPlayerAgent
│   │   ├── haive.games.example → cannot import: GameAgent
│   │   ├── haive.games.clue.controller → cannot import: AugLLMEngine
│   │   └── ... and 40 more
│   ├── haive-mcp (34 errors)
│   │   ├── haive.mcp.mcp_simple_tool_agent → cannot import: GitHubLoader
│   │   ├── haive.mcp.enhanced_parent_self_query_retriever → cannot import: GitHubLoader
│   │   ├── haive.mcp.simple_faiss_retriever → cannot import: GitHubLoader
│   │   └── ... and 31 more
│   ├── haive-prebuilt (10 errors)
│   │   ├── haive.prebuilt.podcast_generator.nodes → cannot import: Send
│   │   ├── haive.prebuilt.podcast_generator.agent → cannot import: Send
│   │   ├── haive.prebuilt.startup.prompts → cannot import: BusinessModelCanvas
│   │   └── ... and 7 more
│   ├── haive-tools (64 errors)
│   │   ├── haive.tools.tools.toolkits.google_calendar → cannot import: get_client
│   │   ├── haive.tools.tools.toolkits.base → cannot import: get_client
│   │   ├── haive.tools.tools.toolkits.nasa_toolkit → cannot import: get_client
│   │   └── ... and 61 more
├── KeyError (3)
│   ├── haive-prebuilt (3 errors)
│   │   ├── haive.prebuilt.scientific_paper_agent.models
│   │   ├── haive.prebuilt.scientific_paper_agent.nodes
│   │   ├── haive.prebuilt.scientific_paper_agent.agent
├── ModuleNotFoundError (537)
│   ├── haive-agents (305 errors)
│   │   ├── haive.agents.state → missing: haive.agents.web_nav
│   │   ├── haive.agents.task_analysis → missing: task_analysis
│   │   ├── haive.agents.task_analysis.agent → missing: task_analysis
│   │   └── ... and 302 more
│   ├── haive-core (70 errors)
│   │   ├── haive.core.utils.parser_utils → missing: haive_agents_dep
│   │   ├── haive.core.utils.tool_list → missing: haive.core.utils.collections
│   │   ├── haive.core.persistence.store.postgres → missing: core
│   │   └── ... and 67 more
│   ├── haive-dataflow (56 errors)
│   │   ├── haive.dataflow.base → missing: haive.core.aug_llm
│   │   ├── haive.dataflow.app_dep → missing: haive.api
│   │   ├── haive.dataflow.main → missing: haive.dataflow.api.api
│   │   └── ... and 53 more
│   ├── haive-games (46 errors)
│   │   ├── haive.games.llm_config_factory → missing: haive.games.models
│   │   ├── haive.games.common.voting_system → missing: haive.games.simple
│   │   ├── haive.games.checkers.configurable_config → missing: haive.games.models
│   │   └── ... and 43 more
│   ├── haive-mcp (13 errors)
│   │   ├── haive.mcp.comprehensive_mcp_web → missing: plotly
│   │   ├── haive.mcp.haive_agent_mcp_integration → missing: fastmcp_runner
│   │   ├── haive.mcp.csv_viewer → missing: streamlit
│   │   └── ... and 10 more
│   ├── haive-prebuilt (42 errors)
│   │   ├── haive.prebuilt.project_manager.agent → missing: haive_agents
│   │   ├── haive.prebuilt.tldr2.engines → missing: newsapi
│   │   ├── haive.prebuilt.tldr2.agent → missing: newsapi
│   │   └── ... and 39 more
│   ├── haive-tools (5 errors)
│   │   ├── haive.tools.tools.dataforseo_tool → missing: haive.config
│   │   ├── haive.tools.tools.hinge_tools → missing: squeaky_hinge
│   │   ├── haive.tools.tools.wolfram_alpha_tool → missing: haive.config
│   │   └── ... and 2 more
├── NameError (37)
│   ├── haive-agents (16 errors)
│   │   ├── haive.agents.simple.example.v2
│   │   ├── haive.agents.simple.example
│   │   ├── haive.agents.self_healing_code.state
│   │   └── ... and 13 more
│   ├── haive-core (16 errors)
│   │   ├── haive.core.engine.document.loaders.sources.specialized_sources
│   │   ├── haive.core.engine.document.loaders.sources.database_sources
│   │   ├── haive.core.engine.document.loaders.sources.chat.base
│   │   └── ... and 13 more
│   ├── haive-games (5 errors)
│   │   ├── haive.games.single_player.example
│   │   ├── haive.games.core.piece.tile
│   │   ├── haive.games.single_player.towers_of_hanoi.position
│   │   └── ... and 2 more
├── PydanticSchemaGenerationError (2)
│   ├── haive-agents (2 errors)
│   │   ├── haive.agents.multi.enhanced_clean_multi_agent
│   │   ├── haive.agents.multi.archive.enhanced_clean_multi_agent
├── PydanticUndefinedAnnotation (1)
│   ├── haive-agents (1 errors)
│   │   ├── haive.agents.react.agent_v4
├── PydanticUserError (3)
│   ├── haive-agents (2 errors)
│   │   ├── haive.agents.multi.archive.experiments.implementations.clean_multi_agent
│   │   ├── haive.agents.multi.experiments.implementations.clean_multi_agent
│   ├── haive-tools (1 errors)
│   │   ├── haive.tools.tools.discord_tools
├── TypeError (73)
│   ├── haive-agents (36 errors)
│   │   ├── haive.agents.memory_reorganized.models.base
│   │   ├── haive.agents.reasoning_and_critique.tot.state
│   │   ├── haive.agents.reasoning_and_critique.tot.engines
│   │   └── ... and 33 more
│   ├── haive-core (9 errors)
│   │   ├── haive.core.types.tree_leaf
│   │   ├── haive.core.schema.typed_state_schema
│   │   ├── haive.core.graph.state_graph_manager
│   │   └── ... and 6 more
│   ├── haive-games (26 errors)
│   │   ├── haive.games.clue.configurable_config
│   │   ├── haive.games.clue.generic_engines
│   │   ├── haive.games.mastermind.configurable_config
│   │   └── ... and 23 more
│   ├── haive-prebuilt (1 errors)
│   │   ├── haive.prebuilt.taskifier.agent
│   ├── haive-tools (1 errors)
│   │   ├── haive.tools.tools.brave_search
├── ValidationError (4)
│   ├── haive-agents (2 errors)
│   │   ├── haive.agents.simple.debug.v2
│   │   ├── haive.agents.simple.debug
│   ├── haive-core (2 errors)
│   │   ├── haive.core.graph.node.test
│   │   ├── haive.core.graph.routers.test
```

## Major Dependency Chains

```
Root Causes (affecting multiple modules)
├── haive.agents.planning.plan_and_execute_multi import ( (72 modules)
│   ├── Packages: haive-agents
│   └── Affected modules:
│       ├── haive.agents.planning
│       ├── haive.agents.planning.base
│       ├── haive.agents.planning.base.agents
│       ├── haive.agents.planning.base.agents.executor
│       ├── haive.agents.planning.base.agents.planner
│       └── ... and 67 more
├── haive.tools.tools.toolkits.alpha_vantage import ( (64 modules)
│   ├── Packages: haive-tools
│   └── Affected modules:
│       ├── haive.tools.tools.toolkits
│       ├── haive.tools.tools.toolkits.amadues_toolkit
│       ├── haive.tools.tools.toolkits.azure_ai_services_toolkit
│       ├── haive.tools.tools.toolkits.base
│       ├── haive.tools.tools.toolkits.chuck_norris_jokes_toolkit
│       └── ... and 59 more
├── haive.core.engine.loaders (53 modules)
│   ├── Packages: haive-core
│   └── Affected modules:
│       ├── haive.core.engine.document.loaders.adapters
│       ├── haive.core.engine.document.loaders.adapters.base
│       ├── haive.core.engine.document.loaders.adapters.local
│       ├── haive.core.engine.document.loaders.sources.base.base
│       ├── haive.core.engine.document.loaders.sources.factory
│       └── ... and 48 more
├── haive.agents.multi.base_multi_agent (49 modules)
│   ├── Packages: haive-agents
│   └── Affected modules:
│       ├── haive.agents.supervisor
│       ├── haive.agents.supervisor.archive.agent_v2
│       ├── haive.agents.supervisor.archive.choice_model_supervisor
│       ├── haive.agents.supervisor.archive.dynamic_activation_supervisor
│       ├── haive.agents.supervisor.archive.dynamic_agent_discovery_supervisor
│       └── ... and 44 more
├── task_analysis (30 modules)
│   ├── Packages: haive-agents
│   └── Affected modules:
│       ├── haive.agents.task_analysis
│       ├── haive.agents.task_analysis.agent
│       ├── haive.agents.task_analysis.analysis
│       ├── haive.agents.task_analysis.analysis.engines
│       ├── haive.agents.task_analysis.analysis.models
│       └── ... and 25 more
├── haive.agents.react_class.react_agent2.advanced_agent3 import ( (20 modules)
│   ├── Packages: haive-agents
│   └── Affected modules:
│       ├── haive.agents.react_class.react_agent2
│       ├── haive.agents.react_class.react_agent2.agent
│       ├── haive.agents.react_class.react_agent2.agent2
│       ├── haive.agents.react_class.react_agent2.agent3
│       ├── haive.agents.react_class.react_agent2.aug_llms
│       └── ... and 15 more
├── haive.games.monopoly.agent import MonopolyAgent, MonopolyAgentConfig (20 modules)
│   ├── Packages: haive-games
│   └── Affected modules:
│       ├── haive.games.monopoly
│       ├── haive.games.monopoly.agent
│       ├── haive.games.monopoly.config
│       ├── haive.games.monopoly.configurable_config
│       ├── haive.games.monopoly.example
│       └── ... and 15 more
├── haive.core.schema.prebuilt.rag_state (17 modules)
│   ├── Packages: haive-agents
│   └── Affected modules:
│       ├── haive.agents.rag.multi_agent_rag
│       ├── haive.agents.rag.multi_agent_rag.additional_workflows
│       ├── haive.agents.rag.multi_agent_rag.advanced_workflows
│       ├── haive.agents.rag.multi_agent_rag.agents
│       ├── haive.agents.rag.multi_agent_rag.compatibility
│       └── ... and 12 more
├── AttributeError:MESSAGE_TRANSFORMER (16 modules)
│   ├── Packages: haive-agents, haive-core
│   └── Affected modules:
│       ├── haive.agents.reasoning_and_critique.reflection
│       ├── haive.agents.reasoning_and_critique.reflection.agent
│       ├── haive.agents.reasoning_and_critique.reflection.config
│       ├── haive.agents.reasoning_and_critique.reflection.models
│       ├── haive.agents.reasoning_and_critique.reflection.state
│       └── ... and 11 more
├── wiki_writer (16 modules)
│   ├── Packages: haive-agents
│   └── Affected modules:
│       ├── haive.agents.wiki_writer
│       ├── haive.agents.wiki_writer.agent
│       ├── haive.agents.wiki_writer.aug_llms
│       ├── haive.agents.wiki_writer.base
│       ├── haive.agents.wiki_writer.interview
│       └── ... and 11 more
├── .base import ( (14 modules)
│   ├── Packages: haive-agents
│   └── Affected modules:
│       ├── haive.agents.memory.search
│       ├── haive.agents.memory.search.base
│       ├── haive.agents.memory.search.deep_research
│       ├── haive.agents.memory.search.deep_research.agent
│       ├── haive.agents.memory.search.deep_research.models
│       └── ... and 9 more
├── haive.agents.memory_reorganized.search.base import ( (13 modules)
│   ├── Packages: haive-agents
│   └── Affected modules:
│       ├── haive.agents.memory_reorganized.search
│       ├── haive.agents.memory_reorganized.search.deep_research
│       ├── haive.agents.memory_reorganized.search.deep_research.agent
│       ├── haive.agents.memory_reorganized.search.deep_research.models
│       ├── haive.agents.memory_reorganized.search.labs
│       └── ... and 8 more
├── self_rag2 (12 modules)
│   ├── Packages: haive-agents
│   └── Affected modules:
│       ├── haive.agents.rag.self_rag2
│       ├── haive.agents.rag.self_rag2.configuration
│       ├── haive.agents.rag.self_rag2.graph
│       ├── haive.agents.rag.self_rag2.nodes
│       ├── haive.agents.rag.self_rag2.nodes.decide_to_generate
│       └── ... and 7 more
├── haive.agents.reflexion (11 modules)
│   ├── Packages: haive-agents
│   └── Affected modules:
│       ├── haive.agents.reasoning_and_critique.reflexion
│       ├── haive.agents.reasoning_and_critique.reflexion.agent
│       ├── haive.agents.reasoning_and_critique.reflexion.aug_llms
│       ├── haive.agents.reasoning_and_critique.reflexion.config
│       ├── haive.agents.reasoning_and_critique.reflexion.example
│       └── ... and 6 more
└── haive.dataflow.api.api (11 modules)
    ├── Packages: haive-dataflow, haive-games
    └── Affected modules:
        ├── haive.dataflow.api.app
        ├── haive.dataflow.api.app_dep
        ├── haive.dataflow.api.game_api
        ├── haive.dataflow.api.general_games_api
        ├── haive.dataflow.api.main
        └── ... and 6 more
```

## Package-Level Error Distribution

```
haive-agents
├── AttributeError: 16
├── ImportError: 200
├── ModuleNotFoundError: 305
├── NameError: 16
├── PydanticSchemaGenerationError: 2
├── PydanticUndefinedAnnotation: 1
├── PydanticUserError: 2
├── TypeError: 36
└── ValidationError: 2
haive-core
├── AttributeError: 3
├── ImportError: 34
├── ModuleNotFoundError: 70
├── NameError: 16
├── TypeError: 9
└── ValidationError: 2
haive-dataflow
├── ImportError: 5
└── ModuleNotFoundError: 56
haive-games
├── ImportError: 43
├── ModuleNotFoundError: 46
├── NameError: 5
└── TypeError: 26
haive-mcp
├── ImportError: 34
└── ModuleNotFoundError: 13
haive-prebuilt
├── ImportError: 10
├── KeyError: 3
├── ModuleNotFoundError: 42
└── TypeError: 1
haive-tools
├── ImportError: 64
├── ModuleNotFoundError: 5
├── PydanticUserError: 1
└── TypeError: 1
```

## Cross-Package Dependencies

Modules that import from other packages and fail:

```
haive-agents depends on:
├── haive-core (286 modules)
│   ├── haive.agents.chain.chain_agent_simple
│   ├── haive.agents.chain.examples_simple
│   ├── haive.agents.chain.extended_examples
│   └── ... and 283 more
├── haive-haive (1 modules)
│   ├── haive.agents.rag.self_rag2.graph
├── haive-tools (8 modules)
│   ├── haive.agents.planning.base.agents.executor
│   ├── haive.agents.planning.enhanced_plan_execute_v5
│   ├── haive.agents.planning.enhanced_plan_execute_v6
│   └── ... and 5 more
haive-core depends on:
├── haive-agents (3 modules)
│   ├── haive.core.graph.node.agent_node_v2
│   ├── haive.core.graph.node.multi_agent_node
│   ├── haive.core.graph.node.stateful_integration_example
├── haive-dataflow (1 modules)
│   ├── haive.core.persistence.supabase_config
haive-dataflow depends on:
├── haive-api (3 modules)
│   ├── haive.dataflow.api.connect4_api
│   ├── haive.dataflow.api.registry
│   ├── haive.dataflow.connect4_api
├── haive-core (10 modules)
│   ├── haive.dataflow.api.base
│   ├── haive.dataflow.api.general_games_api
│   ├── haive.dataflow.api.registry
│   └── ... and 7 more
├── haive-games (3 modules)
│   ├── haive.dataflow.api.game_api
│   ├── haive.dataflow.api.general_games_api
│   ├── haive.dataflow.api.routers.games
├── haive-tools (1 modules)
│   ├── haive.dataflow.api.routes.tools_routes
haive-games depends on:
├── haive-agents (3 modules)
│   ├── haive.games.core.players.agent
│   ├── haive.games.debate_v2.agent_with_judges
│   ├── haive.games.debate_v2.judges
├── haive-core (34 modules)
│   ├── haive.games.among_us.generic_engines
│   ├── haive.games.api.general_api
│   ├── haive.games.api.setup
│   └── ... and 31 more
├── haive-dataflow (2 modules)
│   ├── haive.games.api.general_api
│   ├── haive.games.api.setup
haive-mcp depends on:
├── haive-agents (10 modules)
│   ├── haive.mcp.agents.documentation_agent
│   ├── haive.mcp.agents.intelligent_mcp_agent
│   ├── haive.mcp.agents.mcp_agent
│   └── ... and 7 more
├── haive-core (16 modules)
│   ├── haive.mcp.agents.intelligent_mcp_agent
│   ├── haive.mcp.complete_mcp_with_parent_retriever
│   ├── haive.mcp.downloader.integration
│   └── ... and 13 more
├── haive-dataflow (1 modules)
│   ├── haive.mcp.servers.dataflow_server
haive-prebuilt depends on:
├── haive-agents (5 modules)
│   ├── haive.prebuilt.essay_grading.agent
│   ├── haive.prebuilt.perplexity.base.engines
│   ├── haive.prebuilt.startup.agent
│   └── ... and 2 more
├── haive-core (25 modules)
│   ├── haive.prebuilt.company_researcher.agent
│   ├── haive.prebuilt.company_researcher.config
│   ├── haive.prebuilt.content.document_extractor
│   └── ... and 22 more
├── haive-haive (5 modules)
│   ├── haive.prebuilt.scientific_paper_agent.state
│   ├── haive.prebuilt.systemic_review_of_scientific_articles.state
│   ├── haive.prebuilt.weather_disaster_management.agent
│   └── ... and 2 more
├── haive-tools (1 modules)
│   ├── haive.prebuilt.startup.prompts
haive-tools depends on:
├── haive-config (9 modules)
│   ├── haive.tools.tools.bing_search_tool_INC
│   ├── haive.tools.tools.dataforseo_tool
│   ├── haive.tools.tools.toolkits.clickup_toolkit
│   └── ... and 6 more
├── haive-core (2 modules)
│   ├── haive.tools.tools.toolkits.amadues_toolkit
│   ├── haive.tools.tools.toolkits.nla_toolkit
├── haive-haive (1 modules)
│   ├── haive.tools.tools.toolkits.vbible_toolkit
```
