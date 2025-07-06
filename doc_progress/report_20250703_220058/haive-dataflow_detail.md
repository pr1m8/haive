# haive-dataflow Documentation Report

## Package Overview

- **Package Path**: /home/will/Projects/haive/backend/haive/packages/haive-dataflow
- **Type Signature Issues**: 95
- **Pydantic Field Issues**: 168
- **Has Main **init**.py**: ❌
- **Has README**: ✅
- **Has Examples**: ✅
- **Total Issues**: 416

## Issues by File

### src/haive/dataflow/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 1**: Function 'get_env_api_key' parameter 'provider' name doesn't match type hint

### src/haive/dataflow/app_dep.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 15**: Function 'create_app' missing type hints

### src/haive/dataflow/core.py

- 🔵 **Line 1**: Function 'RegistrySystem.add_configuration' uses overly generic type 'Any' for parameter 'config_data'
- 🔵 **Line 1**: Function 'RegistrySystem.add_configuration' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'RegistrySystem.add_dependency' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'RegistrySystem.add_import_log' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'RegistrySystem.get_entity' might return None but type signature doesn't indicate Optional

### src/haive/dataflow/main.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 37**: Function 'display_startup_info' missing type hints
- 🔵 **Line 58**: Function 'main' missing type hints

### src/haive/dataflow/registry.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 272**: Method 'AgentRegistryService.list_available_agents' missing type hints
- 🔵 **Line 276**: Method 'AgentRegistryService.list_failed_agents' missing type hints
- 🔵 **Line 1**: Function 'AgentRegistryService.get_agent_config' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'AgentRegistryService.get_agent_type' might return None but type signature doesn't indicate Optional

### src/haive/dataflow/router.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/dataflow/tic_tac_toe_api.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 19**: Class 'TicTacToeMoveRequest' missing docstring
- 🟡 **Line 27**: Class 'TicTacToeRequest' missing docstring
- 🟡 **Line 35**: Class 'TicTacToeResponse' missing docstring
- 🟡 **Line 46**: Class 'TicTacToeAPI' missing docstring
- 🔵 **Line 170**: Function 'run' missing type hints

### src/haive/dataflow/game_agent.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 42**: Class 'AgentResponseBase' missing docstring
- 🔵 **Line 138**: Method 'AgentManager.register_connection' missing type hints
- 🔵 **Line 143**: Method 'AgentManager.unregister_connection' missing type hints
- 🔵 **Line 156**: Method 'AgentManager.get_active_threads' missing type hints
- 🔵 **Line 160**: Method 'AgentManager.cleanup' missing type hints
- 🔵 **Line 537**: Method 'GenericAgentAPI.run' missing type hints
- 🔵 **Line 1**: Function 'AgentManager.get_or_create_agent' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'AgentManager.get_agent_for_connection' might return None but type signature doesn't indicate Optional

### src/haive/dataflow/connect4_api.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 381**: Function 'run' missing type hints

### src/haive/dataflow/db.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 25**: Method 'DatabaseManager.connect' missing type hints
- 🔵 **Line 39**: Method 'DatabaseManager.create_schema' missing type hints
- 🔵 **Line 65**: Method 'DatabaseManager.create_tables' missing type hints
- 🔵 **Line 307**: Method 'DatabaseManager.close' missing type hints
- 🔵 **Line 1**: Function 'DatabaseManager.register_agent_config' uses overly generic type 'Any' for parameter 'class_obj'

### src/haive/dataflow/discovery.py

- 🔵 **Line 850**: Function 'discover_all' missing type hints
- 🔵 **Line 1**: Function 'is_pydantic_model' uses overly generic type 'Any' for parameter 'obj'

### src/haive/dataflow/serialization.py

- 🔵 **Line 29**: Method 'SerializationRegistry.register' missing type hints
- 🔵 **Line 1**: Function 'SerializationRegistry.can_serialize' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'SerializationRegistry.\_resolve_type' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'SerializationRegistry.serialize' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'SerializationRegistry.serialize' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'SerializationRegistry.serialize' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'SerializationRegistry.deserialize' uses overly generic type 'Any' for parameter 'data'
- 🔵 **Line 1**: Function 'SerializationRegistry.deserialize' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'SerializationRegistry.deserialize' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'serialize_object' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'deserialize_object' returns overly generic type 'Any'

### src/haive/dataflow/llms/models.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 4**: Class 'Provider' missing docstring
- 🟡 **Line 19**: Class 'ModelCapabilities' missing docstring
- 🟡 **Line 54**: Class 'Pricing' missing docstring
- 🟡 **Line 74**: Class 'SearchPricing' missing docstring
- 🟡 **Line 86**: Class 'Model' missing docstring

### src/haive/dataflow/llms/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/dataflow/llms/api.py

- 🔵 **Line 45**: Function 'get_providers' missing type hints
- 🔵 **Line 1**: Function 'get_model_by_id' might return None but type signature doesn't indicate Optional

### src/haive/dataflow/persistence/conversations.py

- 🔵 **Line 119**: Method 'ConversationManager.client' missing type hints

### src/haive/dataflow/persistence/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/dataflow/internal_websockets/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/dataflow/internal_websockets/handlers.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 20**: Class 'AgentRegistry' missing docstring
- 🔵 **Line 1**: Function 'format_chunk_for_client' uses overly generic type 'Any' for parameter 'chunk'

### src/haive/dataflow/internal_websockets/manager.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/dataflow/fetchers/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/dataflow/fetchers/lite_llm_import.py

- 🔵 **Line 34**: Function 'import_llm_models' missing type hints

### src/haive/dataflow/api/run_integrated_api.py

- 🔵 **Line 33**: Function 'main' missing type hints

### src/haive/dataflow/api/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 1**: Function 'get_env_api_key' parameter 'provider' name doesn't match type hint

### src/haive/dataflow/api/simple_chess_ws.py

- 🔵 **Line 266**: Function 'get_empty_board' missing type hints
- 🔵 **Line 271**: Function 'make_random_move' missing type hints
- 🔵 **Line 281**: Function 'get_game_state' missing type hints
- 🔵 **Line 378**: Function 'main' missing type hints

### src/haive/dataflow/api/integrate_games.py

- 🔵 **Line 31**: Function 'configure_import_paths' missing type hints
- 🔵 **Line 51**: Function 'add_game_routes' missing type hints

### src/haive/dataflow/api/auto_discovery.py

- 🔵 **Line 106**: Method 'APIDiscovery.discover_all_patterns' missing type hints

### src/haive/dataflow/api/app.py

- 🔵 **Line 47**: Function 'create_app' missing type hints

### src/haive/dataflow/api/game_socket.py

- 🔵 **Line 309**: Method 'GameSocketServer.register_connection' missing type hints
- 🔵 **Line 314**: Method 'GameSocketServer.unregister_connection' missing type hints
- 🔵 **Line 360**: Method 'GameSocketServer.cleanup' missing type hints

### src/haive/dataflow/api/app_dep.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 14**: Function 'create_app' missing type hints

### src/haive/dataflow/api/serve_chess_client.py

- 🔵 **Line 31**: Function 'get_static_dir' missing type hints
- 🔵 **Line 60**: Method 'ChessClientHandler.log_message' missing type hints
- 🔵 **Line 65**: Function 'run_server' missing type hints
- 🔵 **Line 97**: Function 'main' missing type hints

### src/haive/dataflow/api/middleware.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/dataflow/api/run_simple.py

- 🔵 **Line 28**: Function 'main' missing type hints

### src/haive/dataflow/api/game_api.py

- 🔵 **Line 315**: Method 'GameAPI.run' missing type hints
- 🔵 **Line 381**: Method 'GameAPIFactory.create_chess_api' missing type hints
- 🔵 **Line 423**: Method 'GameAPIFactory.create_connect4_api' missing type hints
- 🔵 **Line 441**: Method 'GameAPIFactory.create_tic_tac_toe_api' missing type hints

### src/haive/dataflow/api/main.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 18**: Function 'read_root' missing docstring
- 🔵 **Line 18**: Function 'read_root' missing type hints

### src/haive/dataflow/api/run_chess_api.py

- 🔵 **Line 33**: Function 'verify_environment' missing type hints
- 🔵 **Line 56**: Function 'run_chess_api' missing type hints
- 🔵 **Line 95**: Function 'main' missing type hints

### src/haive/dataflow/api/registry.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 272**: Method 'AgentRegistryService.list_available_agents' missing type hints
- 🔵 **Line 276**: Method 'AgentRegistryService.list_failed_agents' missing type hints
- 🔵 **Line 1**: Function 'AgentRegistryService.get_agent_config' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'AgentRegistryService.get_agent_type' might return None but type signature doesn't indicate Optional

### src/haive/dataflow/api/router.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/dataflow/api/tic_tac_toe_api.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 19**: Class 'TicTacToeMoveRequest' missing docstring
- 🟡 **Line 27**: Class 'TicTacToeRequest' missing docstring
- 🟡 **Line 35**: Class 'TicTacToeResponse' missing docstring
- 🟡 **Line 46**: Class 'TicTacToeAPI' missing docstring
- 🔵 **Line 170**: Function 'run' missing type hints

### src/haive/dataflow/api/run_simplified.py

- 🔵 **Line 43**: Function 'get_empty_board' missing type hints
- 🔵 **Line 48**: Function 'move_is_valid' missing type hints
- 🔵 **Line 57**: Function 'make_move' missing type hints
- 🔵 **Line 69**: Function 'get_game_status' missing type hints
- 🔵 **Line 82**: Function 'get_current_player' missing type hints
- 🔵 **Line 87**: Function 'get_game_state' missing type hints
- 🔵 **Line 470**: Function 'main' missing type hints

### src/haive/dataflow/api/game_router_fixed.py

- 🔵 **Line 40**: Function 'discover_game_agents' missing type hints
- 🔵 **Line 432**: Function 'get_index_html' missing type hints
- 🔵 **Line 486**: Function 'get_game_client_html' missing type hints
- 🔵 **Line 714**: Function 'get_router' missing type hints
- 🔵 **Line 750**: Function 'create_game_router_app' missing type hints
- 🔵 **Line 802**: Function 'main' missing type hints
- 🔵 **Line 1**: Function 'create_game_router' might return None but type signature doesn't indicate Optional

### src/haive/dataflow/api/game_router.py

- 🔵 **Line 47**: Function 'discover_game_agents' missing type hints
- 🔵 **Line 189**: Function 'create_game_instance' missing type hints
- 🔵 **Line 237**: Function 'get_game_instance' missing type hints
- 🔵 **Line 243**: Function 'create_game_router' missing type hints
- 🔵 **Line 437**: Function 'get_index_html' missing type hints
- 🔵 **Line 469**: Function 'get_game_client_html' missing type hints
- 🔵 **Line 644**: Function 'create_game_router_app' missing type hints
- 🔵 **Line 689**: Function 'setup_routes' missing type hints
- 🔵 **Line 701**: Function 'get_router' missing type hints
- 🔵 **Line 737**: Function 'main' missing type hints

### src/haive/dataflow/api/game_agent.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 42**: Class 'AgentResponseBase' missing docstring
- 🔵 **Line 138**: Method 'AgentManager.register_connection' missing type hints
- 🔵 **Line 143**: Method 'AgentManager.unregister_connection' missing type hints
- 🔵 **Line 156**: Method 'AgentManager.get_active_threads' missing type hints
- 🔵 **Line 160**: Method 'AgentManager.cleanup' missing type hints
- 🔵 **Line 537**: Method 'GenericAgentAPI.run' missing type hints
- 🔵 **Line 1**: Function 'AgentManager.get_or_create_agent' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'AgentManager.get_agent_for_connection' might return None but type signature doesn't indicate Optional

### src/haive/dataflow/api/connect4_api.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 381**: Function 'run' missing type hints

### src/haive/dataflow/api/db.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 25**: Method 'DatabaseManager.connect' missing type hints
- 🔵 **Line 39**: Method 'DatabaseManager.create_schema' missing type hints
- 🔵 **Line 65**: Method 'DatabaseManager.create_tables' missing type hints
- 🔵 **Line 307**: Method 'DatabaseManager.close' missing type hints
- 🔵 **Line 1**: Function 'DatabaseManager.register_agent_config' uses overly generic type 'Any' for parameter 'class_obj'

### src/haive/dataflow/api/run_game_api.py

- 🔵 **Line 42**: Function 'create_app' missing type hints
- 🔵 **Line 88**: Function 'main' missing type hints

### src/haive/dataflow/api/game_router_enhanced.py

- 🔵 **Line 69**: Function 'discover_game_agents' missing type hints
- 🔵 **Line 613**: Function 'get_router' missing type hints
- 🔵 **Line 671**: Function 'get_index_html' missing type hints
- 🔵 **Line 979**: Function 'create_game_router_app' missing type hints
- 🔵 **Line 1049**: Function 'main' missing type hints
- 🔵 **Line 1**: Function 'discover_game_agents' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function '\_instantiate_agent' returns overly generic type 'Any'

### src/haive/dataflow/api/run_games_api.py

- 🔵 **Line 43**: Function 'create_app' missing type hints
- 🔵 **Line 141**: Function 'main' missing type hints

### src/haive/dataflow/registry/base.py

- 🔵 **Line 506**: Method 'Registry.get_default_search_paths' missing type hints
- 🔵 **Line 527**: Method 'Registry.get_item_type' missing type hints
- 🔵 **Line 540**: Function 'register' missing type hints
- 🔵 **Line 545**: Function 'get' missing type hints
- 🔵 **Line 550**: Function 'create' missing type hints
- 🔵 **Line 1**: Function 'Registry.\_register_in_supabase' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'Registry.get' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'Registry.create' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'Registry.discover_components' might return None but type signature doesn't indicate Optional

### src/haive/dataflow/registry/core.py

- 🔵 **Line 1**: Function 'RegistrySystem.add_configuration' uses overly generic type 'Any' for parameter 'config_data'
- 🔵 **Line 1**: Function 'RegistrySystem.add_configuration' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'RegistrySystem.add_dependency' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'RegistrySystem.add_import_log' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'RegistrySystem.get_entity' might return None but type signature doesn't indicate Optional

### src/haive/dataflow/registry/main.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/dataflow/registry/db.py

- 🟡 **Line 44**: Class 'Config' missing docstring
- 🔵 **Line 1**: Function 'RegistryDB.upsert_registry_item' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'RegistryDB.get_registry_item' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'RegistryDB.upsert_schema_definition' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'RegistryDB.upsert_agent_graph' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'RegistryDB.get_agent_graph' might return None but type signature doesn't indicate Optional

### src/haive/dataflow/registry/discovery.py

- 🔵 **Line 895**: Function 'discover_all' missing type hints
- 🔵 **Line 924**: Function 'discover_mcp_servers' missing type hints
- 🔵 **Line 1**: Function 'is_pydantic_model' uses overly generic type 'Any' for parameter 'obj'

### src/haive/dataflow/registry/serialization.py

- 🔵 **Line 109**: Method 'SerializationRegistry.register' missing type hints
- 🔵 **Line 1**: Function 'SerializationRegistry.can_serialize' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'SerializationRegistry.\_resolve_type' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'SerializationRegistry.serialize' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'SerializationRegistry.serialize' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'SerializationRegistry.serialize' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'SerializationRegistry.deserialize' uses overly generic type 'Any' for parameter 'data'
- 🔵 **Line 1**: Function 'SerializationRegistry.deserialize' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'SerializationRegistry.deserialize' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'serialize_object' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'deserialize_object' returns overly generic type 'Any'

### src/haive/dataflow/auth/middleware.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/dataflow/auth/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/dataflow/auth/dependencies.py

- 🔵 **Line 43**: Function 'get_auth_instance' missing type hints

### src/haive/dataflow/auth/supabase.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 70**: Function 'get_auth_instance' missing type hints
- 🔵 **Line 1**: Function 'SupabaseAuth.verify_token' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'SupabaseAuth.get_user_id' might return None but type signature doesn't indicate Optional

### src/haive/dataflow/auth/credits.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 34**: Method 'CreditsManager.client' missing type hints

### src/haive/dataflow/providers/base.py

- 🔵 **Line 52**: Method 'EntityProvider.get_default_search_paths' missing type hints
- 🔵 **Line 1**: Function 'EntityProvider.is_pydantic_model' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'EntityProvider.add_configuration' uses overly generic type 'Any' for parameter 'config_data'

### src/haive/dataflow/providers/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/dataflow/providers/agent_provider.py

- 🔵 **Line 37**: Method 'AgentProvider.get_default_search_paths' missing type hints

### src/haive/dataflow/mcp/client.py

- 🔵 **Line 462**: Method 'MCPServerAdapter.get_health_status' missing type hints

### src/haive/dataflow/importers/tak.py

- 🔵 **Line 367**: Function 'import_tools_to_database' missing type hints
- 🔵 **Line 441**: Function 'print_tool_stats' missing type hints
- 🔵 **Line 473**: Function 'main' missing type hints

### src/haive/dataflow/importers/litellm_importer.py

- 🔵 **Line 157**: Function 'import_llm_models' missing type hints
- 🔵 **Line 374**: Function 'import_from_env' missing type hints
- 🔵 **Line 508**: Function 'import_embedding_models' missing type hints
- 🔵 **Line 667**: Function 'main' missing type hints
- 🔵 **Line 1**: Function 'get_or_create_provider_type' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'get_or_create_provider' might return None but type signature doesn't indicate Optional

### src/haive/dataflow/importers/embeddings_importer.py

- 🔵 **Line 230**: Function 'import_embedding_models' missing type hints

### src/haive/dataflow/db/schema.py

- 🔵 **Line 32**: Function 'create_schema_sql' missing type hints
- 🔵 **Line 210**: Function 'execute_schema_sql' missing type hints
- 🔵 **Line 261**: Function 'check_schema_exists' missing type hints
- 🔵 **Line 296**: Function 'check_table_exists' missing type hints
- 🔵 **Line 333**: Function 'setup_schema' missing type hints
- 🔵 **Line 395**: Function 'setup_execute_sql_function' missing type hints
- 🔵 **Line 483**: Function 'initialize_database' missing type hints

### src/haive/dataflow/db/inspect_supabase.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 10**: Function 'main' missing docstring
- 🔵 **Line 10**: Function 'main' missing type hints

### src/haive/dataflow/db/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/dataflow/db/supabase.py

- 🔵 **Line 1**: Function 'table' returns overly generic type 'Any'

### src/haive/dataflow/utils/vault_migration_script.py

- 🔵 **Line 124**: Function 'get_existing_vault_secrets' missing type hints
- 🔵 **Line 176**: Function 'migrate_environment_variables' missing type hints
- 🔵 **Line 281**: Function 'migrate_component_env_mappings' missing type hints
- 🔵 **Line 389**: Function 'migrate_provider_api_keys' missing type hints
- 🔵 **Line 500**: Function 'migrate_engine_api_keys' missing type hints
- 🔵 **Line 654**: Function 'add_vault_helper_functions' missing type hints
- 🔵 **Line 772**: Function 'main' missing type hints
- 🟡 **Line 558**: Function 'find_api_keys' missing docstring
- 🔵 **Line 558**: Function 'find_api_keys' missing type hints
- 🔵 **Line 1**: Function 'execute_sql' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'execute_sql' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'create_vault_secret' might return None but type signature doesn't indicate Optional

### src/haive/dataflow/utils/logging.py

- 🔵 **Line 100**: Function 'setup_import_logger' missing type hints
- 🔵 **Line 122**: Function 'setup_operation_logger' missing type hints

### src/haive/dataflow/conversations/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/dataflow/conversations/manager.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 45**: Method 'ConversationManager.client' missing type hints

### src/haive/dataflow/bin/registry_cli.py

- 🔵 **Line 70**: Function 'print_rich' missing type hints
- 🔵 **Line 78**: Function 'print_header' missing type hints
- 🔵 **Line 88**: Function 'print_subheader' missing type hints
- 🔵 **Line 98**: Function 'print_table' missing type hints
- 🔵 **Line 158**: Function 'setup_parser' missing type hints
- 🔵 **Line 250**: Function 'format_json' missing type hints
- 🔵 **Line 257**: Function 'handle_discover' missing type hints
- 🔵 **Line 479**: Function 'handle_import' missing type hints
- 🔵 **Line 496**: Function 'handle_stats' missing type hints
- 🔵 **Line 534**: Function 'handle_search' missing type hints
- 🔵 **Line 621**: Function 'handle_show' missing type hints
- 🔵 **Line 753**: Function 'handle_list' missing type hints
- 🔵 **Line 828**: Function 'handle_clear' missing type hints
- 🔵 **Line 854**: Function 'main' missing type hints

### src/haive/dataflow/bin/vault_cli.py

- 🔵 **Line 33**: Function 'find_module_path' missing type hints
- 🔵 **Line 50**: Function 'import_module' missing type hints
- 🔵 **Line 173**: Function 'run_migrate' missing type hints
- 🔵 **Line 202**: Function 'run_import' missing type hints
- 🔵 **Line 245**: Function 'run_verify' missing type hints
- 🔵 **Line 274**: Function 'add_columns' missing type hints
- 🔵 **Line 373**: Function 'run_export' missing type hints
- 🔵 **Line 458**: Function 'run_import_secrets' missing type hints
- 🔵 **Line 587**: Function 'main' missing type hints
- 🔵 **Line 1**: Function 'execute_sql' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'execute_sql' might return None but type signature doesn't indicate Optional

### src/haive/dataflow/bin/litellm_cli.py

- 🔵 **Line 44**: Function 'run_migrate' missing type hints
- 🔵 **Line 91**: Function 'run_import' missing type hints
- 🔵 **Line 149**: Function 'run_verify' missing type hints
- 🟡 **Line 170**: Function 'main' missing docstring
- 🔵 **Line 170**: Function 'main' missing type hints

### src/haive/dataflow/config/settings.py

- 🔵 **Line 109**: Method 'AppSettings.is_production' missing type hints
- 🔵 **Line 114**: Method 'AppSettings.is_development' missing type hints
- 🔵 **Line 119**: Function 'get_settings' missing type hints

### src/haive/dataflow/config/environment.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 46**: Method 'PostgresConfig.get_connection_uri' missing type hints
- 🔵 **Line 58**: Function 'get_supabase_client_config' missing type hints
- 🔵 **Line 63**: Function 'get_supabase_server_config' missing type hints
- 🔵 **Line 68**: Function 'get_postgres_config' missing type hints

### src/haive/dataflow/registries/main.py

- 🔵 **Line 21**: Function 'ensure_registry_schema' missing type hints
- 🔵 **Line 47**: Function 'ensure_provider_types' missing type hints
- 🔵 **Line 122**: Function 'main' missing type hints

### src/haive/dataflow/registries/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/dataflow/registries/model_registry.py

- 🔵 **Line 72**: Method 'ModelRegistry.update_provider_availability' missing type hints
- 🔵 **Line 111**: Method 'ModelRegistry.get_required_environment_vars' missing type hints
- 🔵 **Line 528**: Method 'ModelRegistry.get_available_llm_providers' missing type hints
- 🔵 **Line 569**: Method 'ModelRegistry.get_available_embedding_providers' missing type hints
- 🔵 **Line 1053**: Method 'ModelRegistry.detect_environment_variables' missing type hints
- 🔵 **Line 1**: Function 'ModelRegistry.\_get_current_user_id' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'ModelRegistry.\_get_default_team_id' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'ModelRegistry.get_secret_from_vault' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'ModelRegistry.get_llm_model' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'ModelRegistry.get_embedding_model' might return None but type signature doesn't indicate Optional

### src/haive/dataflow/api/llms/models.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 4**: Class 'Provider' missing docstring
- 🟡 **Line 19**: Class 'ModelCapabilities' missing docstring
- 🟡 **Line 54**: Class 'Pricing' missing docstring
- 🟡 **Line 74**: Class 'SearchPricing' missing docstring
- 🟡 **Line 86**: Class 'Model' missing docstring

### src/haive/dataflow/api/llms/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/dataflow/api/llms/api.py

- 🔵 **Line 45**: Function 'get_providers' missing type hints
- 🔵 **Line 1**: Function 'get_model_by_id' might return None but type signature doesn't indicate Optional

### src/haive/dataflow/api/routes/agent_discovery_routes_enhanced.py

- 🔵 **Line 123**: Function 'get_discovery_instance' missing type hints

### src/haive/dataflow/api/routes/tools_routes_fixed.py

- 🔵 **Line 90**: Function 'get_discovery_instance' missing type hints
- 🔵 **Line 129**: Function 'discover_tools_fallback' missing type hints

### src/haive/dataflow/api/routes/agent_discovery_routes_fixed.py

- 🔵 **Line 101**: Function 'get_discovery_instance' missing type hints

### src/haive/dataflow/api/routes/agent_routes.py

- 🟡 **Line 161**: Class 'Config' missing docstring
- 🔵 **Line 1**: Function 'get_user_from_token' might return None but type signature doesn't indicate Optional

### src/haive/dataflow/api/routes/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/dataflow/api/routes/conversation_routes.py

- 🟡 **Line 66**: Class 'AgentRegistry' missing docstring

### src/haive/dataflow/api/routes/tools_routes.py

- 🔵 **Line 64**: Function 'discover_tools' missing type hints
- 🔵 **Line 299**: Function 'simple_discover_tools' missing type hints

### src/haive/dataflow/api/routes/agent_discovery_routes.py

- 🔵 **Line 81**: Function 'discover_v1_agents' missing type hints
- 🔵 **Line 156**: Function 'discover_v2_agents' missing type hints
- 🔵 **Line 247**: Function 'discover_all_agents' missing type hints

### src/haive/dataflow/api/routes/games.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/dataflow/api/routes/llm_routes.py

- 🔵 **Line 1**: Function 'get_env_api_key' parameter 'provider' name doesn't match type hint

### src/haive/dataflow/api/routers/games.py

- 🔵 **Line 161**: Function 'get_game_api' missing type hints

### src/haive/dataflow/api/middleware/supabase_logging.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 31**: Method 'SupabaseLogger.client' missing type hints
- 🔵 **Line 1**: Function 'SupabaseLogger.\_sanitize_data' uses overly generic type 'Any' for parameter 'data'
- 🔵 **Line 1**: Function 'SupabaseLogger.\_sanitize_data' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'SupabaseLogger.\_sanitize_data' might return None but type signature doesn't indicate Optional

### src/haive/dataflow/api/middleware/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/dataflow/api/middleware/rate_limit.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/dataflow/api/middleware/auth.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/dataflow/api/middleware/logging.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/dataflow/registry/providers/base.py

- 🔵 **Line 98**: Method 'EntityProvider.get_default_search_paths' missing type hints
- 🔵 **Line 1**: Function 'EntityProvider.is_pydantic_model' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'EntityProvider.add_configuration' uses overly generic type 'Any' for parameter 'config_data'

### src/haive/dataflow/registry/providers/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/dataflow/registry/providers/agent_provider.py

- 🔵 **Line 37**: Method 'AgentProvider.get_default_search_paths' missing type hints

### src/haive/dataflow/registry/importers/tak.py

- 🔵 **Line 367**: Function 'import_tools_to_database' missing type hints
- 🔵 **Line 441**: Function 'print_tool_stats' missing type hints
- 🔵 **Line 473**: Function 'main' missing type hints

### src/haive/dataflow/registry/importers/litellm_importer.py

- 🔵 **Line 200**: Function 'import_llm_models' missing type hints
- 🔵 **Line 417**: Function 'import_from_env' missing type hints
- 🔵 **Line 551**: Function 'import_embedding_models' missing type hints
- 🔵 **Line 710**: Function 'main' missing type hints
- 🔵 **Line 1**: Function 'get_or_create_provider_type' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'get_or_create_provider' might return None but type signature doesn't indicate Optional

### src/haive/dataflow/registry/importers/embeddings_importer.py

- 🔴 **Line 1**: Could not parse file: expected an indented block after 'try' statement on line 303 (<unknown>, line 304)

### src/haive/dataflow/registry/utils/vault_migration_script.py

- 🔵 **Line 124**: Function 'get_existing_vault_secrets' missing type hints
- 🔵 **Line 176**: Function 'migrate_environment_variables' missing type hints
- 🔵 **Line 281**: Function 'migrate_component_env_mappings' missing type hints
- 🔵 **Line 389**: Function 'migrate_provider_api_keys' missing type hints
- 🔵 **Line 500**: Function 'migrate_engine_api_keys' missing type hints
- 🔵 **Line 654**: Function 'add_vault_helper_functions' missing type hints
- 🔵 **Line 772**: Function 'main' missing type hints
- 🟡 **Line 558**: Function 'find_api_keys' missing docstring
- 🔵 **Line 558**: Function 'find_api_keys' missing type hints
- 🔵 **Line 1**: Function 'execute_sql' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'execute_sql' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'create_vault_secret' might return None but type signature doesn't indicate Optional

### src/haive/dataflow/registry/utils/logging.py

- 🔵 **Line 100**: Function 'setup_import_logger' missing type hints
- 🔵 **Line 122**: Function 'setup_operation_logger' missing type hints

### src/haive/dataflow/registry/bin/registry_cli.py

- 🔵 **Line 70**: Function 'print_rich' missing type hints
- 🔵 **Line 78**: Function 'print_header' missing type hints
- 🔵 **Line 88**: Function 'print_subheader' missing type hints
- 🔵 **Line 98**: Function 'print_table' missing type hints
- 🔵 **Line 158**: Function 'setup_parser' missing type hints
- 🔵 **Line 250**: Function 'format_json' missing type hints
- 🔵 **Line 257**: Function 'handle_discover' missing type hints
- 🔵 **Line 479**: Function 'handle_import' missing type hints
- 🔵 **Line 496**: Function 'handle_stats' missing type hints
- 🔵 **Line 534**: Function 'handle_search' missing type hints
- 🔵 **Line 621**: Function 'handle_show' missing type hints
- 🔵 **Line 753**: Function 'handle_list' missing type hints
- 🔵 **Line 828**: Function 'handle_clear' missing type hints
- 🔵 **Line 854**: Function 'main' missing type hints

### src/haive/dataflow/registry/bin/vault_cli.py

- 🔵 **Line 33**: Function 'find_module_path' missing type hints
- 🔵 **Line 50**: Function 'import_module' missing type hints
- 🔵 **Line 173**: Function 'run_migrate' missing type hints
- 🔵 **Line 202**: Function 'run_import' missing type hints
- 🔵 **Line 245**: Function 'run_verify' missing type hints
- 🔵 **Line 274**: Function 'add_columns' missing type hints
- 🔵 **Line 373**: Function 'run_export' missing type hints
- 🔵 **Line 458**: Function 'run_import_secrets' missing type hints
- 🔵 **Line 587**: Function 'main' missing type hints
- 🔵 **Line 1**: Function 'execute_sql' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'execute_sql' might return None but type signature doesn't indicate Optional

### src/haive/dataflow/registry/bin/litellm_cli.py

- 🔵 **Line 44**: Function 'run_migrate' missing type hints
- 🔵 **Line 91**: Function 'run_import' missing type hints
- 🔵 **Line 149**: Function 'run_verify' missing type hints
- 🟡 **Line 170**: Function 'main' missing docstring
- 🔵 **Line 170**: Function 'main' missing type hints

### src/haive/dataflow/registry/registries/main.py

- 🔵 **Line 21**: Function 'ensure_registry_schema' missing type hints
- 🔵 **Line 47**: Function 'ensure_provider_types' missing type hints
- 🔵 **Line 122**: Function 'main' missing type hints

### src/haive/dataflow/registry/registries/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/dataflow/registry/registries/model_registry.py

- 🔵 **Line 72**: Method 'ModelRegistry.update_provider_availability' missing type hints
- 🔵 **Line 111**: Method 'ModelRegistry.get_required_environment_vars' missing type hints
- 🔵 **Line 528**: Method 'ModelRegistry.get_available_llm_providers' missing type hints
- 🔵 **Line 569**: Method 'ModelRegistry.get_available_embedding_providers' missing type hints
- 🔵 **Line 1053**: Method 'ModelRegistry.detect_environment_variables' missing type hints
- 🔵 **Line 1**: Function 'ModelRegistry.\_get_current_user_id' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'ModelRegistry.\_get_default_team_id' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'ModelRegistry.get_secret_from_vault' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'ModelRegistry.get_llm_model' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'ModelRegistry.get_embedding_model' might return None but type signature doesn't indicate Optional
