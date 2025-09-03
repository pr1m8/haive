# Comprehensive Import Error Fix Plan

Based on documentation build errors, here are the fixes needed:

## 1. Add to autodoc_mock_imports

```python
autodoc_mock_imports.extend([
    "game",
    "game_api",
    "game_router",
    "haive.api",
    "haive.core.schema.example",
    "haive.core.schema.prebuilt.messages.examples",
    "haive.core.types.tree_leaf",
    "haive.core.utils.collections",
    "haive.core.utils.debugkit.benchmarking.core",
    "haive.core.utils.debugkit.debugging",
    "haive.core.utils.dev",
    "haive.core.utils.parser_utils",
    "haive.core.utils.tool_list",
    "haive.dataflow.api.api",
    "haive.dataflow.api.engine",
    "haive.dataflow.api.llms.api.llms",
    "haive.dataflow.api.middleware.auth.supabase",
    "haive.dataflow.api.middleware.config",
    "haive.dataflow.api.models",
    "haive.dataflow.api.routes.auth",
    "haive.dataflow.api.routes.utils",
    "haive.dataflow.api.utils",
    "haive.dataflow.auth.auth",
    "haive.dataflow.auth.config",
    "haive.dataflow.db.db",
    "haive.dataflow.engine",
    "haive.dataflow.internal_websockets.auth",
    "haive.dataflow.persistence.config",
    "haive.dataflow.persistence.persistence",
    "haive.dataflow.providers.providers",
    "haive.dataflow.providers.utils",
    "haive.dataflow.registries.db",
    "haive.dataflow.registry.db.supabase",
    "haive.dataflow.registry.registry",
    "haive.games.cards.blackjack",
    "haive.games.cards.bs",
    "haive.games.cards.card",
    "haive.games.models",
    "haive.games.simple",
    "haive_agents_dep",
    "haive_games",
    "AgentRegistry",
    "AmongUsConfig",
    "AugLLMEngine",
    "CardAction",
    "ChessAgentConfig",
    "GameConfig",
    "GameInfo",
    "GameState",
    "MonopolyPlayerAgent",
    "SupabaseServerConfig",
    "TCard",
    "create_age",
    "update_availability_status",
    "AgentRegistry",
    "AmongUsConfig",
    "Any",
    "AugLLMEngine",
    "CardAction",
    "ChessAgentConfig",
    "GameConfig",
    "GameInfo",
    "GamePiece",
    "GameState",
    "MonopolyPlayerAgent",
    "SupabaseServerConfig",
    "TCard",
    "create_age",
    "update_availability_status",
])
```

## 2. Add to autoapi_ignore

```python
autoapi_ignore.extend([
    "**/dataflow/**/*.py",
    "**/configurable_config.py",
    "**/generic_engines.py",
    "**/cards/standard/blackjack/**/*.py",
    "**/cards/standard/bs/**/*.py",
    "**/cards/standard/poker/**/*.py",
    "**/core/game/**/*.py",
    "**/memory/models_dir/**/*.py",
    "**/memory/search/**/*.py",
    "**/api_example.py",
    "**/example_configurable.py",
])
```

## 3. Specific Module Fixes

- **haive.core.schema.__init__.py**: Add missing 'create_age' export
- **haive.core.registry.__init__.py**: Add missing 'AgentRegistry' export
- **haive.games.api.__init__.py**: Add missing 'GameInfo' export
- **haive.games.among_us.config.py**: Add missing 'AmongUsConfig' export
- **haive.games.chess.config.py**: Add missing 'ChessAgentConfig' export
- **haive.core.engine.aug_llm.__init__.py**: Add missing 'AugLLMEngine' export
- **haive.games.core.base.state.py**: Add missing 'GameState' export

## 4. Summary

- **Total issues identified**: 62
- **Missing modules**: 41
- **Import errors**: 13
- **Type errors**: 6
- **Name errors**: 2

**Strategy**: Focus on mock imports and ignore patterns first, then address specific missing exports.
