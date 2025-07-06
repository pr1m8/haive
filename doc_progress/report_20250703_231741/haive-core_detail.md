# haive-core Documentation Report

## Package Overview

- **Package Path**: /home/will/Projects/haive/backend/haive/packages/haive-core
- **Type Signature Issues**: 513
- **Pydantic Field Issues**: 317
- **Has Main **init**.py**: ❌
- **Has README**: ✅
- **Has Examples**: ✅
- **Total Issues**: 2515

## Missing Example Files

- core/engine
- core/engine/agent

## Issues by File

### src/haive/core/persistence/base.py

- 🔵 **Line 68**: Method 'CheckpointerConfig.is_async_mode' missing type hints
- 🔵 **Line 92**: Method 'CheckpointerConfig.create_checkpointer' missing type hints
- 🔵 **Line 175**: Method 'CheckpointerConfig.to_dict' missing type hints
- 🟡 **Line 65**: Class 'Config' missing docstring
- 🔵 **Line 1**: Function 'CheckpointerConfig.create_checkpointer' returns overly generic type 'Any'

### src/haive/core/persistence/memory.py

- 🔵 **Line 78**: Method 'MemoryCheckpointerConfig.is_async_mode' missing type hints
- 🔵 **Line 91**: Method 'MemoryCheckpointerConfig.create_checkpointer' missing type hints
- 🟡 **Line 75**: Class 'Config' missing docstring
- 🔵 **Line 1**: Function 'MemoryCheckpointerConfig.create_checkpointer' returns overly generic type 'Any'

### src/haive/core/persistence/factory.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 868**: Function 'close_all_postgres_pools' missing type hints
- 🔵 **Line 1**: Function 'create_postgres_checkpointer' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'register_postgres_thread' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'put_postgres_checkpoint' uses overly generic type 'Any' for parameter 'data'

### src/haive/core/persistence/sqlite_config.py

- 🔵 **Line 95**: Method 'SQLiteSaver.setup' missing type hints
- 🔵 **Line 467**: Method 'SQLiteCheckpointerConfig.create_checkpointer' missing type hints
- 🔵 **Line 656**: Method 'SQLiteCheckpointerConfig.close' missing type hints
- 🟡 **Line 379**: Class 'CheckpointTuple' missing docstring
- 🔵 **Line 1**: Function 'SQLiteCheckpointerConfig.create_checkpointer' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'SQLiteCheckpointerConfig.put_checkpoint' uses overly generic type 'Any' for parameter 'data'

### src/haive/core/persistence/handlers.py

- 🔵 **Line 810**: Function 'prepare_merged_input' missing type hints
- 🔵 **Line 1**: Function 'setup_checkpointer' uses overly generic type 'Any' for parameter 'config'
- 🔵 **Line 1**: Function 'setup_checkpointer' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'ensure_pool_open' uses overly generic type 'Any' for parameter 'checkpointer'
- 🔵 **Line 1**: Function 'close_pool_if_needed' uses overly generic type 'Any' for parameter 'checkpointer'
- 🔵 **Line 1**: Function 'close_pool_if_needed' uses overly generic type 'Any' for parameter 'pool'
- 🔵 **Line 1**: Function 'close_pool_if_needed' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'register_thread_if_needed' uses overly generic type 'Any' for parameter 'checkpointer'
- 🔵 **Line 1**: Function 'register_thread_if_needed' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'prepare_merged_input' returns overly generic type 'Any'

### src/haive/core/persistence/utils.py

- 🔵 **Line 1**: Function 'ensure_pool_open' uses overly generic type 'Any' for parameter 'checkpointer'
- 🔵 **Line 1**: Function 'register_thread' uses overly generic type 'Any' for parameter 'checkpointer'

### src/haive/core/persistence/types.py

- 🔵 **Line 143**: Method 'ConnectionOptions.get_postgres_ssl_modes' missing type hints

### src/haive/core/persistence/postgres_config.py

- 🔵 **Line 140**: Method 'PostgresCheckpointerConfig.is_async_mode' missing type hints
- 🔵 **Line 156**: Method 'PostgresCheckpointerConfig.get_connection_uri' missing type hints
- 🔵 **Line 197**: Method 'PostgresCheckpointerConfig.get_connection_kwargs' missing type hints
- 🔵 **Line 236**: Method 'PostgresCheckpointerConfig.create_checkpointer' missing type hints
- 🟡 **Line 137**: Class 'Config' missing docstring
- 🔵 **Line 1**: Function 'PostgresCheckpointerConfig.create_checkpointer' returns overly generic type 'Any'

### src/haive/core/persistence/supabase_config.py

- 🔵 **Line 147**: Method 'SupabaseSaver.setup' missing type hints
- 🔵 **Line 1065**: Method 'SupabaseCheckpointerConfig.validate_supabase_available' missing type hints
- 🔵 **Line 1074**: Method 'SupabaseCheckpointerConfig.create_checkpointer' missing type hints
- 🔵 **Line 1277**: Method 'SupabaseCheckpointerConfig.close' missing type hints
- 🟡 **Line 927**: Class 'CheckpointTuple' missing docstring
- 🔵 **Line 1**: Function 'SupabaseCheckpointerConfig.create_checkpointer' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'SupabaseCheckpointerConfig.register_thread' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'SupabaseCheckpointerConfig.put_checkpoint' uses overly generic type 'Any' for parameter 'data'

### src/haive/core/models/metadata_mixin.py

- 🔵 **Line 25**: Method 'ModelMetadataMixin.get_context_window' missing type hints
- 🔵 **Line 56**: Method 'ModelMetadataMixin.get_max_input_tokens' missing type hints
- 🔵 **Line 66**: Method 'ModelMetadataMixin.get_max_output_tokens' missing type hints
- 🔵 **Line 76**: Method 'ModelMetadataMixin.get_token_pricing' missing type hints
- 🔵 **Line 88**: Method 'ModelMetadataMixin.get_batch_token_pricing' missing type hints
- 🔵 **Line 130**: Method 'ModelMetadataMixin.get_search_context_costs' missing type hints
- 🔵 **Line 141**: Method 'ModelMetadataMixin.get_supported_endpoints' missing type hints
- 🔵 **Line 151**: Method 'ModelMetadataMixin.get_supported_modalities' missing type hints
- 🔵 **Line 161**: Method 'ModelMetadataMixin.get_supported_output_modalities' missing type hints
- 🔵 **Line 171**: Method 'ModelMetadataMixin.get_deprecation_date' missing type hints
- 🔵 **Line 181**: Method 'ModelMetadataMixin.get_model_mode' missing type hints
- 🔵 **Line 213**: Method 'ModelMetadataMixin.supports_vision' missing type hints
- 🔵 **Line 218**: Method 'ModelMetadataMixin.supports_function_calling' missing type hints
- 🔵 **Line 223**: Method 'ModelMetadataMixin.supports_parallel_function_calling' missing type hints
- 🔵 **Line 228**: Method 'ModelMetadataMixin.supports_system_messages' missing type hints
- 🔵 **Line 233**: Method 'ModelMetadataMixin.supports_tool_choice' missing type hints
- 🔵 **Line 238**: Method 'ModelMetadataMixin.supports_response_schema' missing type hints
- 🔵 **Line 243**: Method 'ModelMetadataMixin.supports_reasoning' missing type hints
- 🔵 **Line 248**: Method 'ModelMetadataMixin.supports_web_search' missing type hints
- 🔵 **Line 253**: Method 'ModelMetadataMixin.supports_audio_input' missing type hints
- 🔵 **Line 258**: Method 'ModelMetadataMixin.supports_audio_output' missing type hints
- 🔵 **Line 263**: Method 'ModelMetadataMixin.supports_pdf_input' missing type hints
- 🔵 **Line 268**: Method 'ModelMetadataMixin.supports_prompt_caching' missing type hints
- 🔵 **Line 273**: Method 'ModelMetadataMixin.supports_native_streaming' missing type hints
- 🔵 **Line 278**: Method 'ModelMetadataMixin.max_tokens' missing type hints
- 🔵 **Line 283**: Method 'ModelMetadataMixin.max_input_tokens' missing type hints
- 🔵 **Line 288**: Method 'ModelMetadataMixin.max_output_tokens' missing type hints

### src/haive/core/models/metadata.py

- 🔵 **Line 29**: Method 'ModelMetadata.context_window' missing type hints
- 🔵 **Line 34**: Method 'ModelMetadata.pricing' missing type hints

### src/haive/core/registry/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 38**: Method 'AbstractRegistry.clear' missing type hints
- 🔵 **Line 1**: Function 'AbstractRegistry.get' uses overly generic type 'Any' for parameter 'item_type'
- 🔵 **Line 1**: Function 'AbstractRegistry.list' uses overly generic type 'Any' for parameter 'item_type'
- 🔵 **Line 1**: Function 'AbstractRegistry.get_all' uses overly generic type 'Any' for parameter 'item_type'

### src/haive/core/registry/memory.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 59**: Method 'MemoryRegistry.clear' missing type hints

### src/haive/core/registry/factory.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 17**: Method 'RegistryFactory.register_registry_type' missing type hints

### src/haive/core/registry/decorators.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 24**: Function 'register_component' missing type hints
- 🟡 **Line 49**: Function 'decorator' missing docstring
- 🔵 **Line 49**: Function 'decorator' missing type hints
- 🟡 **Line 54**: Function 'new_init' missing docstring
- 🔵 **Line 54**: Function 'new_init' missing type hints
- 🔵 **Line 86**: Function 'register_instance' missing type hints
- 🔵 **Line 1**: Function 'register_component' uses overly generic type 'Any' for parameter 'component_type'

### src/haive/core/registry/manager.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 18**: Method 'RegistryManager.register_registry_type' missing type hints
- 🔵 **Line 23**: Method 'RegistryManager.get_instance' missing type hints
- 🔵 **Line 34**: Method 'RegistryManager.get_registry' missing type hints

### src/haive/core/logging/ui.py

- 🔵 **Line 102**: Method 'LoggingUI.create_layout' missing type hints
- 🔵 **Line 130**: Method 'LoggingUI.render_header' missing type hints
- 🔵 **Line 139**: Method 'LoggingUI.render_menu' missing type hints
- 🔵 **Line 151**: Method 'LoggingUI.render_status' missing type hints
- 🔵 **Line 186**: Method 'LoggingUI.render_logs' missing type hints
- 🔵 **Line 229**: Method 'LoggingUI.render_footer' missing type hints
- 🔵 **Line 244**: Method 'LoggingUI.set_global_level' missing type hints
- 🔵 **Line 268**: Method 'LoggingUI.module_levels_menu' missing type hints
- 🔵 **Line 292**: Method 'LoggingUI.quick_presets_menu' missing type hints
- 🔵 **Line 320**: Method 'LoggingUI.suppress_menu' missing type hints
- 🔵 **Line 336**: Method 'LoggingUI.filter_menu' missing type hints
- 🔵 **Line 355**: Method 'LoggingUI.toggle_logs' missing type hints
- 🔵 **Line 359**: Method 'LoggingUI.save_config' missing type hints
- 🔵 **Line 365**: Method 'LoggingUI.clear_logs' missing type hints
- 🔵 **Line 369**: Method 'LoggingUI.quit' missing type hints
- 🔵 **Line 373**: Method 'LoggingUI.handle_input' missing type hints
- 🔵 **Line 390**: Method 'LoggingUI.run' missing type hints
- 🔵 **Line 452**: Method 'LoggingMonitor.monitor' missing type hints
- 🔵 **Line 524**: Function 'launch_ui' missing type hints
- 🔵 **Line 530**: Function 'monitor_logs' missing type hints
- 🟡 **Line 75**: Class 'UILogHandler' missing docstring
- 🔵 **Line 80**: Method 'UILogHandler.emit' missing docstring
- 🔵 **Line 80**: Method 'UILogHandler.emit' missing type hints
- 🟡 **Line 477**: Class 'MonitorHandler' missing docstring
- 🔵 **Line 482**: Method 'MonitorHandler.emit' missing docstring
- 🔵 **Line 482**: Method 'MonitorHandler.emit' missing type hints

### src/haive/core/logging/quiet_imports.py

- 🔵 **Line 38**: Function 'restore_rich_print' missing type hints
- 🟡 **Line 17**: Function 'silent_print' missing docstring
- 🔵 **Line 17**: Function 'silent_print' missing type hints

### src/haive/core/logging/control.py

- 🔵 **Line 106**: Method 'HaiveLoggingControl.save_config' missing type hints
- 🔵 **Line 123**: Method 'HaiveLoggingControl.set_level' missing type hints
- 🔵 **Line 142**: Method 'HaiveLoggingControl.set_module_level' missing type hints
- 🔵 **Line 158**: Method 'HaiveLoggingControl.suppress' missing type hints
- 🔵 **Line 170**: Method 'HaiveLoggingControl.unsuppress' missing type hints
- 🔵 **Line 184**: Method 'HaiveLoggingControl.suppress_third_party' missing type hints
- 🔵 **Line 188**: Method 'HaiveLoggingControl.only_show' missing type hints
- 🔵 **Line 198**: Method 'HaiveLoggingControl.show_all' missing type hints
- 🔵 **Line 251**: Method 'HaiveLoggingControl.status' missing type hints
- 🔵 **Line 289**: Method 'HaiveLoggingControl.quick_setup' missing type hints
- 🔵 **Line 337**: Method 'HaiveLoggingControl.set_verbosity' missing type hints
- 🔵 **Line 356**: Method 'HaiveLoggingControl.enable_debug_for' missing type hints
- 🔵 **Line 373**: Function 'set_log_level' missing type hints
- 🔵 **Line 378**: Function 'suppress_modules' missing type hints
- 🔵 **Line 383**: Function 'only_show_modules' missing type hints
- 🔵 **Line 388**: Function 'debug_mode' missing type hints
- 🔵 **Line 393**: Function 'quiet_mode' missing type hints
- 🔵 **Line 398**: Function 'haive_only' missing type hints

### src/haive/core/logging/enhanced_formatter.py

- 🔵 **Line 224**: Method 'AutoSourceHandler.emit' missing type hints
- 🔵 **Line 257**: Function 'setup_source_aware_logging' missing type hints
- 🔵 **Line 288**: Function 'demo_source_logging' missing type hints
- 🟡 **Line 295**: Class 'DemoClass' missing docstring
- 🔵 **Line 299**: Method 'DemoClass.do_something' missing docstring
- 🔵 **Line 299**: Method 'DemoClass.do_something' missing type hints

### src/haive/core/logging/rich_logger.py

- 🔵 **Line 62**: Function 'silence_third_party_loggers' missing type hints
- 🔵 **Line 134**: Method 'RichLogger.set_debug_mode' missing type hints
- 🔵 **Line 150**: Method 'RichLogger.is_debug_mode' missing type hints
- 🔵 **Line 155**: Method 'RichLogger.debug' missing type hints
- 🔵 **Line 160**: Method 'RichLogger.info' missing type hints
- 🔵 **Line 164**: Method 'RichLogger.warning' missing type hints
- 🔵 **Line 168**: Method 'RichLogger.error' missing type hints
- 🔵 **Line 172**: Method 'RichLogger.critical' missing type hints
- 🔵 **Line 177**: Method 'RichLogger.table' missing type hints
- 🔵 **Line 196**: Method 'RichLogger.panel' missing type hints
- 🔵 **Line 208**: Method 'RichLogger.success' missing type hints
- 🔵 **Line 212**: Method 'RichLogger.failure' missing type hints
- 🔵 **Line 216**: Method 'RichLogger.progress' missing type hints
- 🔵 **Line 220**: Method 'RichLogger.debug_table' missing type hints
- 🔵 **Line 225**: Method 'RichLogger.debug_panel' missing type hints
- 🔵 **Line 231**: Method 'RichLogger.track_time' missing type hints
- 🔵 **Line 241**: Method 'RichLogger.log_exception' missing type hints
- 🔵 **Line 258**: Method 'RichLogger.set_level' missing type hints
- 🔵 **Line 271**: Function 'enable_debug_mode' missing type hints
- 🔵 **Line 276**: Function 'disable_debug_mode' missing type hints
- 🔵 **Line 281**: Function 'configure_logging' missing type hints
- 🔵 **Line 1**: Function 'RichLogger.\_format_value' uses overly generic type 'Any' for parameter 'value'

### src/haive/core/logging/dashboard.py

- 🔵 **Line 145**: Method 'LoggingDashboard.create_layout' missing type hints
- 🔵 **Line 170**: Method 'LoggingDashboard.render_header' missing type hints
- 🔵 **Line 197**: Method 'LoggingDashboard.render_main_panel' missing type hints
- 🔵 **Line 252**: Method 'LoggingDashboard.render_stats' missing type hints
- 🔵 **Line 270**: Method 'LoggingDashboard.render_controls' missing type hints
- 🔵 **Line 289**: Method 'LoggingDashboard.render_errors' missing type hints
- 🔵 **Line 312**: Method 'LoggingDashboard.render_footer' missing type hints
- 🔵 **Line 341**: Method 'LoggingDashboard.handle_key_press' missing type hints
- 🔵 **Line 364**: Method 'LoggingDashboard.show_level_filter_menu' missing type hints
- 🔵 **Line 384**: Method 'LoggingDashboard.show_module_filter_menu' missing type hints
- 🔵 **Line 401**: Method 'LoggingDashboard.show_search_dialog' missing type hints
- 🔵 **Line 411**: Method 'LoggingDashboard.clear_filters' missing type hints
- 🔵 **Line 418**: Method 'LoggingDashboard.show_preset_menu' missing type hints
- 🔵 **Line 432**: Method 'LoggingDashboard.export_logs' missing type hints
- 🔵 **Line 473**: Method 'LoggingDashboard.run' missing type hints
- 🔵 **Line 483**: Function 'launch_dashboard' missing type hints
- 🔵 **Line 499**: Method 'ModuleActivityVisualizer.visualize' missing type hints
- 🟡 **Line 79**: Class 'DashboardHandler' missing docstring
- 🔵 **Line 84**: Method 'DashboardHandler.emit' missing docstring
- 🔵 **Line 84**: Method 'DashboardHandler.emit' missing type hints
- 🟡 **Line 516**: Class 'ActivityHandler' missing docstring
- 🔵 **Line 521**: Method 'ActivityHandler.emit' missing docstring
- 🔵 **Line 521**: Method 'ActivityHandler.emit' missing type hints

### src/haive/core/logging/decorators.py

- 🔵 **Line 17**: Function 'log_calls' missing type hints
- 🔵 **Line 84**: Function 'log_performance' missing type hints
- 🔵 **Line 160**: Function 'log_errors' missing type hints
- 🔵 **Line 224**: Function 'log_method_calls' missing type hints
- 🟡 **Line 35**: Function 'decorator' missing docstring
- 🟡 **Line 100**: Function 'decorator' missing docstring
- 🟡 **Line 176**: Function 'decorator' missing docstring
- 🟡 **Line 236**: Function 'class_decorator' missing docstring
- 🔵 **Line 236**: Function 'class_decorator' missing type hints
- 🟡 **Line 48**: Function 'wrapper' missing docstring
- 🔵 **Line 48**: Function 'wrapper' missing type hints
- 🟡 **Line 112**: Function 'wrapper' missing docstring
- 🔵 **Line 112**: Function 'wrapper' missing type hints
- 🟡 **Line 188**: Function 'wrapper' missing docstring
- 🔵 **Line 188**: Function 'wrapper' missing type hints
- 🔵 **Line 1**: Function 'decorator' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'wrapper' might return None but type signature doesn't indicate Optional

### src/haive/core/logging/auto_config.py

- 🔵 **Line 93**: Function 'auto_configure_logging' missing type hints
- 🔵 **Line 182**: Function 'configure_for_game_development' missing type hints
- 🔵 **Line 197**: Function 'configure_for_agent_development' missing type hints
- 🔵 **Line 209**: Function 'show_clean_logs' missing type hints
- 🔵 **Line 224**: Function 'enable_source_tracking' missing type hints

### src/haive/core/logging/mixins.py

- 🔵 **Line 31**: Method 'LoggingMixin.initialize_logger' missing type hints
- 🔵 **Line 43**: Method 'LoggingMixin.logger_name' missing type hints
- 🔵 **Line 48**: Method 'LoggingMixin.logger' missing type hints
- 🔵 **Line 268**: Method 'RichLoggerMixin.log_component_init' missing type hints
- 🔵 **Line 308**: Method 'PerformanceLoggerMixin.time_operation' missing type hints

### src/haive/core/logging/utils.py

- 🔵 **Line 36**: Function 'setup_project_logging' missing type hints
- 🔵 **Line 107**: Function 'log_context' missing type hints
- 🟡 **Line 116**: Function 'context_filter' missing docstring
- 🔵 **Line 116**: Function 'context_filter' missing type hints

### src/haive/core/logging/interactive_cli.py

- 🔵 **Line 69**: Method 'LogLevelValidator.validate' missing docstring
- 🔵 **Line 69**: Method 'LogLevelValidator.validate' missing type hints
- 🔵 **Line 275**: Method 'InteractiveLoggingCLI.show_help' missing type hints
- 🔵 **Line 463**: Method 'InteractiveLoggingCLI.monitor_logs' missing type hints
- 🔵 **Line 518**: Method 'InteractiveLoggingCLI.generate_test_logs' missing type hints
- 🔵 **Line 548**: Method 'InteractiveLoggingCLI.export_logs' missing type hints
- 🔵 **Line 560**: Method 'InteractiveLoggingCLI.set_breakpoint' missing type hints
- 🔵 **Line 576**: Method 'InteractiveLoggingCLI.run' missing type hints
- 🔵 **Line 621**: Function 'main' missing type hints
- 🟡 **Line 164**: Class 'CLILogHandler' missing docstring
- 🔵 **Line 169**: Method 'CLILogHandler.emit' missing docstring
- 🔵 **Line 169**: Method 'CLILogHandler.emit' missing type hints
- 🟡 **Line 563**: Class 'BreakpointHandler' missing docstring
- 🔵 **Line 564**: Method 'BreakpointHandler.emit' missing docstring
- 🔵 **Line 564**: Method 'BreakpointHandler.emit' missing type hints

### src/haive/core/logging/debug_toggle.py

- 🔵 **Line 25**: Function 'toggle_debug' missing type hints
- 🔵 **Line 74**: Function 'main' missing type hints

### src/haive/core/logging/auto_wrapper.py

- 🔵 **Line 17**: Function 'setup_logging' missing type hints
- 🔵 **Line 29**: Function 'main' missing type hints

### src/haive/core/logging/sitecustomize.py

- 🔴 **Line 1**: Could not parse file: unterminated string literal (detected at line 26) (<unknown>, line 26)

### src/haive/core/logging/quick_setup.py

- 🔵 **Line 15**: Function 'show_all_sources' missing type hints
- 🔵 **Line 37**: Function 'show_haive_sources' missing type hints
- 🔵 **Line 53**: Function 'track_specific_modules' missing type hints
- 🔵 **Line 74**: Function 'debug_with_source' missing type hints
- 🔵 **Line 94**: Function 'intercept_prints' missing type hints
- 🔵 **Line 156**: Function 'intercept_prints_silent' missing type hints
- 🔵 **Line 212**: Function 'setup_development_logging' missing type hints
- 🔵 **Line 235**: Function 'i_want_to_see_everything' missing type hints
- 🔵 **Line 243**: Function 'just_show_my_code' missing type hints
- 🔵 **Line 256**: Function 'where_is_this_coming_from' missing type hints
- 🔵 **Line 288**: Function 'debug_on' missing type hints
- 🔵 **Line 293**: Function 'debug_off' missing type hints
- 🔵 **Line 299**: Function 'check_status' missing type hints
- 🔵 **Line 341**: Function 'redirect_rich_print_to_logging' missing type hints
- 🔵 **Line 109**: Function 'tracked_print' missing type hints
- 🔵 **Line 171**: Function 'tracked_print' missing type hints
- 🟡 **Line 275**: Class 'HighlightFilter' missing docstring
- 🔵 **Line 276**: Method 'HighlightFilter.filter' missing docstring
- 🔵 **Line 276**: Method 'HighlightFilter.filter' missing type hints
- 🟡 **Line 359**: Function 'logged_print' missing docstring
- 🔵 **Line 359**: Function 'logged_print' missing type hints

### src/haive/core/logging/manager.py

- 🔵 **Line 59**: Method 'LoggingManager.get_instance' missing type hints
- 🔵 **Line 308**: Method 'LoggingManager.print_startup_banner' missing type hints
- 🔵 **Line 402**: Method 'LoggingManager.close' missing type hints
- 🔵 **Line 417**: Function 'get_logging_manager' missing type hints

### src/haive/core/logging/cli.py

- 🔵 **Line 16**: Function 'create_parser' missing type hints
- 🔵 **Line 153**: Function 'main' missing type hints

### src/haive/core/ui/debug_interface.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 90**: Method 'HaiveDebugger.display_engine' missing type hints
- 🔵 **Line 139**: Method 'HaiveDebugger.display_graph' missing type hints
- 🔵 **Line 203**: Method 'HaiveDebugger.display_state' missing type hints
- 🔵 **Line 231**: Method 'HaiveDebugger.timer' missing type hints
- 🔵 **Line 244**: Method 'HaiveDebugger.trace_execution' missing type hints
- 🔵 **Line 318**: Method 'HaiveDebugger.show_performance_summary' missing type hints
- 🔵 **Line 335**: Method 'HaiveDebugger.show_trace_summary' missing type hints
- 🔵 **Line 356**: Method 'HaiveDebugger.capture_output' missing type hints
- 🔵 **Line 368**: Method 'HaiveDebugger.watch_object' missing type hints
- 🔵 **Line 391**: Method 'HaiveDebugger.check_watched_object' missing type hints
- 🔵 **Line 1**: Function 'HaiveDebugger.display_engine' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'HaiveDebugger.display_graph' uses overly generic type 'Any' for parameter 'graph'

### src/haive/core/ui/interactive_ui.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 40**: Method 'HaiveInteractiveUI.start' missing type hints

### src/haive/core/ui/cli.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/runtime/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/utils/config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/utils/model_utils.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/utils/parser_utils.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/utils/tool_utils.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/utils/file_utils.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 4**: Function 'read_yaml_file' missing docstring
- 🔵 **Line 4**: Function 'read_yaml_file' missing type hints
- 🔵 **Line 10**: Function 'read_file_content' missing type hints

### src/haive/core/utils/config_utils.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 35**: Function 'prepare_compile_kwargs' missing type hints
- 🔵 **Line 1**: Function 'apply_config_to_app' uses overly generic type 'Any' for parameter 'app'
- 🔵 **Line 1**: Function 'apply_config_to_app' returns overly generic type 'Any'

### src/haive/core/utils/inspection.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 1**: Function 'check_interfaces' uses overly generic type 'Any' for parameter 'obj'

### src/haive/core/utils/getter_mixin.py

- 🔴 **Line 1**: Could not parse file: unterminated triple-quoted string literal (detected at line 167) (<unknown>, line 167)

### src/haive/core/utils/mermaid_utils.py

- 🔵 **Line 26**: Function 'detect_environment' missing type hints
- 🔵 **Line 1**: Function 'display_mermaid' might return None but type signature doesn't indicate Optional

### src/haive/core/utils/collections.py

- 🔴 **Line 1**: Could not parse file: unterminated triple-quoted string literal (detected at line 212) (<unknown>, line 212)

### src/haive/core/utils/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/utils/chat_utils.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 4**: Function 'create_response' missing type hints

### src/haive/core/utils/runnable_config_utils.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 4**: Function 'get_user_id' missing docstring

### src/haive/core/utils/visualize_graph_utils.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 10**: Function 'render_and_display_graph' missing docstring
- 🔵 **Line 10**: Function 'render_and_display_graph' missing type hints

### src/haive/core/utils/tool_list.py

- 🔴 **Line 1**: Could not parse file: unterminated triple-quoted string literal (detected at line 442) (<unknown>, line 442)

### src/haive/core/utils/message_utils.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 16**: Function 'has_tool_calls' missing type hints
- 🔵 **Line 38**: Function 'has_tool_call' missing type hints
- 🔵 **Line 51**: Function 'has_tool_error' missing type hints
- 🔵 **Line 69**: Function 'add_messages' missing type hints
- 🔵 **Line 78**: Function 'tag_with_name' missing type hints
- 🔵 **Line 84**: Function 'tag_ai_messages_transform' missing type hints
- 🔵 **Line 113**: Function 'swap_roles_transform' missing type hints
- 🟡 **Line 123**: Function 'route_messages' missing docstring
- 🟡 **Line 149**: Function 'reduce_messages' missing docstring
- 🔵 **Line 1**: Function 'get_last_message' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'MessageNormalizingToolNode.run_tool' returns overly generic type 'Any'

### src/haive/core/utils/logging_utils.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/utils/env_utils.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 122**: Function 'load_project_env_files' missing type hints
- 🔵 **Line 164**: Function 'is_production' missing type hints
- 🔵 **Line 169**: Function 'is_development' missing type hints
- 🔵 **Line 174**: Function 'is_test' missing type hints
- 🔵 **Line 179**: Function 'is_testing' missing type hints
- 🔵 **Line 1**: Function 'load_env_file' parameter 'override' name doesn't match type hint
- 🔵 **Line 1**: Function 'get_env_var' uses overly generic type 'Any' for parameter 'default'

### src/haive/core/utils/state_utils.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/utils/doc_utils.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 6**: Function 'save_docs_to_jsonl' missing docstring
- 🟡 **Line 13**: Function 'format_docs' missing docstring

### src/haive/core/utils/serialization.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 1**: Function 'ensure_json_serializable' uses overly generic type 'Any' for parameter 'data'
- 🔵 **Line 1**: Function 'ensure_json_serializable' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'ensure_json_serializable' might return None but type signature doesn't indicate Optional

### src/haive/core/types/tree_leaf.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 11**: Class 'Leaf' missing docstring
- 🟡 **Line 18**: Class 'Branch' missing docstring
- 🔵 **Line 34**: Method 'NodeMixin.is_leaf' missing docstring
- 🔵 **Line 34**: Method 'NodeMixin.is_leaf' missing type hints
- 🔵 **Line 37**: Method 'NodeMixin.add' missing docstring
- 🔵 **Line 37**: Method 'NodeMixin.add' missing type hints
- 🔵 **Line 43**: Method 'NodeMixin.size' missing docstring
- 🔵 **Line 43**: Method 'NodeMixin.size' missing type hints

### src/haive/core/types/dynamic_enum.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 49**: Method 'DynamicEnum.register' missing docstring
- 🔵 **Line 49**: Method 'DynamicEnum.register' missing type hints
- 🔵 **Line 54**: Method 'DynamicEnum.unregister' missing docstring
- 🔵 **Line 54**: Method 'DynamicEnum.unregister' missing type hints
- 🔵 **Line 59**: Method 'DynamicEnum.choices' missing docstring
- 🔵 **Line 59**: Method 'DynamicEnum.choices' missing type hints
- 🔵 **Line 63**: Method 'DynamicEnum.enum_type' missing docstring
- 🔵 **Line 63**: Method 'DynamicEnum.enum_type' missing type hints
- 🟡 **Line 89**: Function 'create_dynamic_enum' missing docstring
- 🔵 **Line 1**: Function 'DynamicEnum.**get_pydantic_core_schema**' uses overly generic type 'Any' for parameter '\_handler'
- 🔵 **Line 1**: Function 'DynamicEnum.**get_pydantic_json_schema**' uses overly generic type 'Any' for parameter '\_handler'

### src/haive/core/types/**intit**.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/types/serializable_callable.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 21**: Method 'SerializableCallable.is_serializable' missing docstring
- 🔵 **Line 1**: Function 'SerializableCallable.**call**' returns overly generic type 'Any'

### src/haive/core/types/advanced_registry.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 34**: Class 'Buildable' missing docstring
- 🔵 **Line 35**: Method 'Buildable.build' missing docstring
- 🔵 **Line 35**: Method 'Buildable.build' missing type hints
- 🔵 **Line 77**: Method 'Registered.factory' missing docstring
- 🔵 **Line 77**: Method 'Registered.factory' missing type hints
- 🔵 **Line 81**: Method 'Registered.get_class' missing docstring
- 🔵 **Line 89**: Method 'Registered.list_available' missing docstring
- 🔵 **Line 89**: Method 'Registered.list_available' missing type hints
- 🔵 **Line 93**: Method 'Registered.discover_entry_points' missing docstring
- 🔵 **Line 93**: Method 'Registered.discover_entry_points' missing type hints
- 🔵 **Line 98**: Method 'Registered.summary' missing docstring
- 🔵 **Line 98**: Method 'Registered.summary' missing type hints
- 🔵 **Line 104**: Method 'Registered.build' missing docstring
- 🔵 **Line 104**: Method 'Registered.build' missing type hints
- 🔵 **Line 146**: Method 'ComponentSpec.build' missing docstring
- 🔵 **Line 146**: Method 'ComponentSpec.build' missing type hints
- 🟡 **Line 155**: Class 'Tokenizer' missing docstring
- 🔵 **Line 160**: Method 'Tokenizer.build' missing docstring
- 🔵 **Line 160**: Method 'Tokenizer.build' missing type hints
- 🟡 **Line 164**: Class 'Lowercaser' missing docstring
- 🔵 **Line 169**: Method 'Lowercaser.build' missing docstring
- 🔵 **Line 169**: Method 'Lowercaser.build' missing type hints
- 🟡 **Line 174**: Class 'TextPipeline' missing docstring
- 🔵 **Line 181**: Method 'TextPipeline.build' missing docstring
- 🔵 **Line 181**: Method 'TextPipeline.build' missing type hints

### src/haive/core/types/dynamic_literal.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 23**: Class '\_DynLitMeta' missing docstring
- 🔵 **Line 44**: Method 'DynamicLiteral.register' missing docstring
- 🔵 **Line 44**: Method 'DynamicLiteral.register' missing type hints
- 🔵 **Line 48**: Method 'DynamicLiteral.unregister' missing docstring
- 🔵 **Line 48**: Method 'DynamicLiteral.unregister' missing type hints
- 🔵 **Line 52**: Method 'DynamicLiteral.choices' missing docstring
- 🔵 **Line 52**: Method 'DynamicLiteral.choices' missing type hints
- 🔵 **Line 83**: Method 'DynamicLiteral.literal_type' missing docstring
- 🔵 **Line 83**: Method 'DynamicLiteral.literal_type' missing type hints
- 🟡 **Line 87**: Function 'create_dynamic_literal' missing docstring
- 🟡 **Line 95**: Class 'Colour' missing docstring
- 🟡 **Line 99**: Class 'PaintJob' missing docstring
- 🟡 **Line 103**: Class 'Config' missing docstring
- 🔵 **Line 1**: Function 'DynamicLiteral.**get_pydantic_core_schema**' uses overly generic type 'Any' for parameter '\_handler'
- 🔵 **Line 1**: Function 'DynamicLiteral.**get_pydantic_json_schema**' uses overly generic type 'Any' for parameter '\_handler'
- 🔵 **Line 1**: Function 'DynamicLiteral.literal_type' returns overly generic type 'Any'

### src/haive/core/engine/embeddings.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 45**: Method 'EmbeddingsEngineConfig.validate_engine_type' missing docstring
- 🔵 **Line 45**: Method 'EmbeddingsEngineConfig.validate_engine_type' missing type hints
- 🔵 **Line 167**: Method 'EmbeddingsEngineConfig.derive_input_schema' missing type hints
- 🔵 **Line 186**: Method 'EmbeddingsEngineConfig.derive_output_schema' missing type hints
- 🔵 **Line 202**: Method 'EmbeddingsEngineConfig.get_schema_fields' missing type hints

### src/haive/core/config/protocols.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 10**: Method 'ConfigurableProtocol.apply_runnable_config' missing docstring

### src/haive/core/config/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/config/constants.py

- 🔵 **Line 76**: Function 'create_directories' missing type hints

### src/haive/core/config/runnable.py

- 🔵 **Line 1**: Function 'RunnableConfigManager.create_with_engine' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'RunnableConfigManager.merge' parameter 'override' name doesn't match type hint
- 🔵 **Line 1**: Function 'RunnableConfigManager.extract_value' uses overly generic type 'Any' for parameter 'default'
- 🔵 **Line 1**: Function 'RunnableConfigManager.extract_value' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'RunnableConfigManager.add_engine' uses overly generic type 'Any' for parameter 'engine'

### src/haive/core/schema/state_schema.py

- 🔵 **Line 177**: Method 'StateSchema.model_dump' missing type hints
- 🔵 **Line 208**: Method 'StateSchema.setup_engines_and_tools' missing type hints
- 🔵 **Line 329**: Method 'StateSchema.dict' missing type hints
- 🔵 **Line 341**: Method 'StateSchema.to_dict' missing type hints
- 🔵 **Line 350**: Method 'StateSchema.to_json' missing type hints
- 🔵 **Line 463**: Method 'StateSchema.get_engines' missing type hints
- 🔵 **Line 510**: Method 'StateSchema.get_all_class_engines' missing type hints
- 🔵 **Line 552**: Method 'StateSchema.get_all_instance_engines' missing type hints
- 🔵 **Line 861**: Method 'StateSchema.clear_messages' missing type hints
- 🔵 **Line 872**: Method 'StateSchema.get_last_message' missing type hints
- 🔵 **Line 883**: Method 'StateSchema.copy' missing type hints
- 🔵 **Line 896**: Method 'StateSchema.deep_copy' missing type hints
- 🔵 **Line 978**: Method 'StateSchema.shared_fields' missing type hints
- 🔵 **Line 1016**: Method 'StateSchema.manager' missing type hints
- 🔵 **Line 1789**: Method 'StateSchema.to_python_code' missing type hints
- 🔵 **Line 1893**: Method 'StateSchema.list_structured_models' missing type hints
- 🔵 **Line 2031**: Method 'StateSchema.as_table' missing type hints
- 🔵 **Line 2101**: Method 'StateSchema.display_table' missing type hints
- 🔵 **Line 1**: Function 'StateSchema.get' uses overly generic type 'Any' for parameter 'default'
- 🔵 **Line 1**: Function 'StateSchema.get' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'StateSchema.to_command' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'StateSchema.from_snapshot' uses overly generic type 'Any' for parameter 'snapshot'
- 🔵 **Line 1**: Function 'StateSchema.\_format_field_value' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'StateSchema.\_format_field_info' uses overly generic type 'Any' for parameter 'field_info'

### src/haive/core/schema/schema_composer.py

- 🔵 **Line 1865**: Method 'SchemaComposer.build' missing type hints
- 🔵 **Line 2235**: Method 'SchemaComposer.to_manager' missing type hints
- 🔵 **Line 2441**: Method 'SchemaComposer.show_engines' missing type hints
- 🔵 **Line 1**: Function 'SchemaComposer.add_engine' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'SchemaComposer.add_field' uses overly generic type 'Any' for parameter 'default'
- 🔵 **Line 1**: Function 'SchemaComposer.add_fields_from_engine' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'SchemaComposer.\_display_schema_summary' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'SchemaComposer.show_engines' might return None but type signature doesn't indicate Optional

### src/haive/core/schema/ui.py

- 🔵 **Line 1**: Function 'SchemaUI.\_create_schema_content' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'SchemaUI.\_format_value' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'SchemaUI.\_format_field' uses overly generic type 'Any' for parameter 'field_info'

### src/haive/core/schema/meta_agent_state.py

- 🔵 **Line 1**: Function 'MetaAgentState.record_agent_completion' uses overly generic type 'Any' for parameter 'output'
- 🔵 **Line 1**: Function 'MetaAgentState.set_shared_context' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'MetaAgentState.get_shared_context' uses overly generic type 'Any' for parameter 'default'
- 🔵 **Line 1**: Function 'MetaAgentState.get_shared_context' returns overly generic type 'Any'

### src/haive/core/schema/schema_manager.py

- 🔵 **Line 1081**: Method 'StateSchemaManager.to_composer' missing type hints
- 🔵 **Line 1**: Function 'StateSchemaManager.\_load_from_composer' uses overly generic type 'Any' for parameter 'composer'
- 🔵 **Line 1**: Function 'StateSchemaManager.add_field' uses overly generic type 'Any' for parameter 'default'
- 🔵 **Line 1**: Function 'StateSchemaManager.modify_field' uses overly generic type 'Any' for parameter 'new_default'

### src/haive/core/schema/utils.py

- 🔵 **Line 1**: Function 'SchemaUtils.format_type_annotation' uses overly generic type 'Any' for parameter 'type_hint'
- 🔵 **Line 1**: Function 'SchemaUtils.add_field_to_schema' uses overly generic type 'Any' for parameter 'default'

### src/haive/core/schema/multi_agent_state_schema.py

- 🔵 **Line 47**: Method 'MultiAgentStateSchema.populate_engines_dict' missing type hints

### src/haive/core/schema/field_utils.py

- 🔵 **Line 155**: Method 'FieldMetadata.to_dict' missing type hints
- 🔵 **Line 196**: Method 'FieldMetadata.to_annotation_metadata' missing type hints
- 🔵 **Line 261**: Method 'FieldMetadata.get_reducer_name' missing type hints
- 🔵 **Line 708**: Function 'get_common_reducers' missing type hints
- 🟡 **Line 728**: Function 'add_lists' missing docstring
- 🔵 **Line 728**: Function 'add_lists' missing type hints
- 🟡 **Line 733**: Function 'concat_lists' missing docstring
- 🔵 **Line 733**: Function 'concat_lists' missing type hints
- 🟡 **Line 751**: Function 'concat_strings' missing docstring
- 🔵 **Line 751**: Function 'concat_strings' missing type hints
- 🟡 **Line 757**: Function 'sum_values' missing docstring
- 🔵 **Line 757**: Function 'sum_values' missing type hints
- 🟡 **Line 803**: Function 'generic_lambda_reducer' missing docstring
- 🔵 **Line 803**: Function 'generic_lambda_reducer' missing type hints
- 🟡 **Line 745**: Function 'add_messages' missing docstring
- 🔵 **Line 745**: Function 'add_messages' missing type hints
- 🔵 **Line 1**: Function 'create_field' uses overly generic type 'Any' for parameter 'default'
- 🔵 **Line 1**: Function 'create_annotated_field' uses overly generic type 'Any' for parameter 'default'
- 🔵 **Line 1**: Function 'infer_field_type' uses overly generic type 'Any' for parameter 'value'

### src/haive/core/schema/field_extractor.py

- 🔵 **Line 1**: Function 'FieldExtractor.extract_from_engine' uses overly generic type 'Any' for parameter 'engine'

### src/haive/core/schema/field_definition.py

- 🔵 **Line 258**: Method 'FieldDefinition.to_field_info' missing type hints
- 🔵 **Line 310**: Method 'FieldDefinition.to_annotated_field' missing type hints
- 🔵 **Line 363**: Method 'FieldDefinition.get_reducer_name' missing type hints
- 🔵 **Line 412**: Method 'FieldDefinition.to_dict' missing type hints
- 🔵 **Line 1**: Function 'FieldDefinition.**init**' uses overly generic type 'Any' for parameter 'field_info'
- 🔵 **Line 1**: Function 'FieldDefinition.**init**' uses overly generic type 'Any' for parameter 'default'
- 🔵 **Line 1**: Function 'FieldDefinition.extract_from_model_field' uses overly generic type 'Any' for parameter 'field_info'

### src/haive/core/graph/tool_manager.py

- 🔵 **Line 34**: Method 'ToolManager.list_tools' missing type hints
- 🔵 **Line 1**: Function 'ToolManager.add_tool' uses overly generic type 'Any' for parameter 'tool'
- 🔵 **Line 1**: Function 'ToolManager.get_tool' returns overly generic type 'Any'

### src/haive/core/graph/tool_config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/graph/state_graph_manager.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 21**: Method 'StateGraphManager.extract_metadata' missing type hints
- 🔵 **Line 49**: Method 'StateGraphManager.ensure_compiled' missing type hints
- 🔵 **Line 57**: Method 'StateGraphManager.add_node' missing type hints
- 🔵 **Line 63**: Method 'StateGraphManager.remove_edge' missing type hints
- 🔵 **Line 70**: Method 'StateGraphManager.insert_node' missing type hints
- 🔵 **Line 108**: Method 'StateGraphManager.insert_start_node' missing type hints
- 🔵 **Line 133**: Method 'StateGraphManager.insert_end_node' missing type hints
- 🔵 **Line 158**: Method 'StateGraphManager.update_branch' missing type hints
- 🔵 **Line 168**: Method 'StateGraphManager.get_metadata' missing type hints
- 🔵 **Line 176**: Method 'StateGraphManager.visualize' missing type hints
- 🔵 **Line 277**: Method 'StateGraphManager.get_metadata' missing type hints
- 🔵 **Line 283**: Method 'StateGraphManager.attach_to_graph' missing type hints
- 🔵 **Line 1**: Function 'StateGraphManager.**init**' uses overly generic type 'Any' for parameter 'graph'

### src/haive/core/graph/graph_pattern_registry.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 72**: Method 'BranchDefinition.create_condition' missing type hints
- 🔵 **Line 104**: Method 'GraphPatternRegistry.get_instance' missing type hints
- 🔵 **Line 172**: Method 'GraphPatternRegistry.list_patterns' missing type hints
- 🔵 **Line 180**: Method 'GraphPatternRegistry.list_branches' missing type hints
- 🔵 **Line 188**: Method 'GraphPatternRegistry.clear' missing type hints
- 🔵 **Line 196**: Function 'register_pattern' missing type hints
- 🔵 **Line 226**: Function 'register_branch' missing type hints
- 🔵 **Line 271**: Function 'apply_error_handling' missing type hints
- 🔵 **Line 306**: Function 'apply_persistence' missing type hints
- 🔵 **Line 338**: Function 'intent_router' missing type hints
- 🟡 **Line 211**: Function 'decorator' missing docstring
- 🔵 **Line 211**: Function 'decorator' missing type hints
- 🟡 **Line 246**: Function 'decorator' missing docstring
- 🔵 **Line 246**: Function 'decorator' missing type hints
- 🔵 **Line 1**: Function 'GraphPattern.apply' uses overly generic type 'Any' for parameter 'graph'
- 🔵 **Line 1**: Function 'GraphPattern.apply' returns overly generic type 'Any'

### src/haive/core/graph/tool_injector.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 251**: Function 'state_tool' missing type hints
- 🔵 **Line 270**: Function 'store_tool' missing type hints
- 🔵 **Line 286**: Function 'hybrid_tool' missing type hints
- 🟡 **Line 262**: Function 'decorator' missing docstring
- 🟡 **Line 280**: Function 'decorator' missing docstring
- 🟡 **Line 297**: Function 'decorator' missing docstring

### src/haive/core/graph/StateSchema.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 36**: Method 'StateSchema.create_model' missing type hints
- 🔵 **Line 67**: Method 'StateSchema.from_models' missing type hints
- 🔵 **Line 99**: Method 'StateSchema.from_aug_llm' missing type hints
- 🔵 **Line 1**: Function 'StateSchema.add_field' uses overly generic type 'Any' for parameter 'default'

### src/haive/core/graph/ToolManager.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 851**: Method 'ToolManager.reset' missing type hints
- 🔵 **Line 856**: Method 'ToolManager.get_execution_history' missing type hints
- 🔵 **Line 861**: Method 'ToolManager.executed_tools' missing type hints
- 🔵 **Line 871**: Function 'state_tool' missing type hints
- 🔵 **Line 886**: Function 'store_tool' missing type hints
- 🔵 **Line 900**: Function 'hybrid_tool' missing type hints
- 🟡 **Line 879**: Function 'decorator' missing docstring
- 🟡 **Line 893**: Function 'decorator' missing docstring
- 🟡 **Line 908**: Function 'decorator' missing docstring
- 🔵 **Line 1**: Function 'ToolManager.\_execute_sync_tool' uses overly generic type 'Any' for parameter 'tool_obj'
- 🔵 **Line 1**: Function 'ToolManager.\_execute_with_timeout' uses overly generic type 'Any' for parameter 'tool_obj'
- 🔵 **Line 1**: Function 'ToolManager.\_execute_with_timeout' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'ToolManager.\_execute_func' uses overly generic type 'Any' for parameter 'tool_obj'
- 🔵 **Line 1**: Function 'ToolManager.\_execute_func' returns overly generic type 'Any'

### src/haive/core/graph/graph_builder2.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 1410**: Function 'node' missing type hints
- 🔵 **Line 1442**: Function 'processing_node' missing type hints
- 🔵 **Line 1456**: Function 'tool_node' missing type hints
- 🔵 **Line 1472**: Function 'router_node' missing type hints
- 🔵 **Line 1496**: Function 'interrupt_node' missing type hints
- 🟡 **Line 1421**: Function 'decorator' missing docstring
- 🔵 **Line 1**: Function 'EnhancedNodeFactory.\_process_inputs' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'EnhancedNodeFactory.\_process_output' uses overly generic type 'Any' for parameter 'result'
- 🔵 **Line 1**: Function 'EnhancedNodeFactory.\_get_next_node' uses overly generic type 'Any' for parameter 'result'
- 🔵 **Line 1**: Function 'EnhancedNodeFactory.\_validate_state' parameter 'validation_mode' name doesn't match type hint
- 🔵 **Line 1**: Function 'EnhancedNodeFactory.\_execute_with_timeout' uses overly generic type 'Any' for parameter 'arg'
- 🔵 **Line 1**: Function 'EnhancedNodeFactory.\_execute_with_timeout' returns overly generic type 'Any'

### src/haive/core/graph/NodeFactory.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 1**: Function 'NodeFunction.**call**' uses overly generic type 'Any' for parameter 'state'
- 🔵 **Line 1**: Function 'NodeFunction.**call**' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'NodeFactory.\_extract_input' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'NodeFactory.\_merge_configs' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'NodeFactory.\_extract_from_config' uses overly generic type 'Any' for parameter 'default'
- 🔵 **Line 1**: Function 'NodeFactory.\_extract_from_config' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'NodeFactory.\_derive_input_mapping' uses overly generic type 'Any' for parameter 'component'
- 🔵 **Line 1**: Function 'NodeFactory.\_derive_output_mapping' uses overly generic type 'Any' for parameter 'component'

### src/haive/core/graph/state_schema_old.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 107**: Method 'StateSchema.model' missing type hints
- 🔵 **Line 130**: Method 'StateSchema.add_tool_fields' missing type hints
- 🔵 **Line 175**: Method 'StateSchema.add_agent_fields' missing type hints
- 🔵 **Line 355**: Method 'StateSchema.to_dict' missing type hints
- 🔵 **Line 366**: Method 'StateSchema.to_json' missing type hints
- 🔵 **Line 372**: Method 'StateSchema.create_state_graph' missing type hints
- 🔵 **Line 451**: Method 'StateSchema.list_registered_schemas' missing type hints
- 🔵 **Line 1**: Function 'StateSchema.add_field' uses overly generic type 'Any' for parameter 'default'
- 🔵 **Line 1**: Function 'StateSchema.add_to_memory' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'StateSchema.get_last_message' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'StateSchema.get_last_user_message' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'StateSchema.get_system_prompt' might return None but type signature doesn't indicate Optional

### src/haive/core/graph/dynamic_graph_builder.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 471**: Method 'DynamicGraph.update_default_runnable_config' missing type hints
- 🔵 **Line 1417**: Method 'DynamicGraph.build' missing type hints
- 🔵 **Line 1545**: Method 'DynamicGraph.visualize_graph' missing type hints
- 🔵 **Line 1648**: Method 'DynamicGraph.compile' missing type hints
- 🔵 **Line 1728**: Method 'DynamicGraph.debug_graph' missing type hints
- 🟡 **Line 87**: Class 'Config' missing docstring
- 🔵 **Line 1**: Function 'DynamicGraph.build' returns overly generic type 'Any'

### src/haive/core/graph/dynamic_graph.py

- 🔵 **Line 28**: Method 'DynamicGraph.build' missing type hints
- 🔵 **Line 1**: Function 'DynamicGraph.add_node' uses overly generic type 'Any' for parameter 'node_config'
- 🔵 **Line 1**: Function 'DynamicGraph.build' returns overly generic type 'Any'

### src/haive/core/graph/state_graph.py

- 🔵 **Line 35**: Method 'StateGraph.compile' missing type hints
- 🔵 **Line 1**: Function 'StateGraph.add_node' uses overly generic type 'Any' for parameter 'node_function'
- 🔵 **Line 1**: Function 'StateGraph.compile' returns overly generic type 'Any'

### src/haive/core/graph/StateGraphEditor.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 40**: Method 'NodeConfig.validate_command_goto' missing docstring
- 🔵 **Line 40**: Method 'NodeConfig.validate_command_goto' missing type hints
- 🔵 **Line 57**: Method 'EdgeConfig.validate_to_node' missing docstring
- 🔵 **Line 57**: Method 'EdgeConfig.validate_to_node' missing type hints
- 🔵 **Line 75**: Method 'BranchConfig.validate_destinations' missing docstring
- 🔵 **Line 75**: Method 'BranchConfig.validate_destinations' missing type hints
- 🔵 **Line 113**: Method 'StateGraphEditor.validate_schemas' missing type hints
- 🔵 **Line 124**: Method 'StateGraphEditor.initialize_graph' missing type hints
- 🔵 **Line 143**: Method 'StateGraphEditor.get_graph' missing type hints
- 🔵 **Line 334**: Method 'StateGraphEditor.build_graph' missing type hints
- 🔵 **Line 415**: Method 'StateGraphEditor.compile' missing type hints
- 🔵 **Line 429**: Method 'StateGraphEditor.to_dict' missing type hints
- 🔵 **Line 1**: Function 'StateGraphEditor.compile' returns overly generic type 'Any'

### src/haive/core/graph/routing.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 369**: Method 'Router.create_router_function' missing type hints
- 🔵 **Line 504**: Method 'Router.to_node_config' missing type hints
- 🔵 **Line 1**: Function 'Router.add_state_route' uses overly generic type 'Any' for parameter 'value'

### src/haive/core/common/models/dynamic_choice_model.py

- 🔵 **Line 153**: Method 'DynamicChoiceModel.current_model' missing type hints
- 🔵 **Line 158**: Method 'DynamicChoiceModel.option_names' missing type hints
- 🔵 **Line 274**: Method 'DynamicChoiceModel.print_full_state' missing type hints
- 🔵 **Line 301**: Method 'DynamicChoiceModel.interactive_demo' missing type hints
- 🟡 **Line 70**: Class 'Config' missing docstring

### src/haive/core/common/models/named_list.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 60**: Method 'NamedList.validate_items' missing type hints
- 🔵 **Line 69**: Method 'NamedList.process_input' missing type hints
- 🔵 **Line 157**: Method 'NamedList.resolve_references' missing type hints
- 🔵 **Line 275**: Method 'NamedList.keys' missing type hints
- 🔵 **Line 279**: Method 'NamedList.values' missing type hints
- 🔵 **Line 283**: Method 'NamedList.to_dict' missing type hints
- 🔵 **Line 287**: Method 'NamedList.to_list' missing type hints
- 🔵 **Line 291**: Method 'NamedList.has_unresolved_references' missing type hints
- 🔵 **Line 295**: Method 'NamedList.get_unresolved_references' missing type hints
- 🔵 **Line 314**: Method 'NamedList.validate_input' missing type hints
- 🔵 **Line 1**: Function 'NamedList.resolve_references' might return None but type signature doesn't indicate Optional

### src/haive/core/common/structures/tree.py

- 🔵 **Line 226**: Method 'AutoTree.node_name' missing type hints
- 🔵 **Line 240**: Method 'AutoTree.node_type' missing type hints
- 🔵 **Line 245**: Method 'AutoTree.children' missing type hints
- 🔵 **Line 250**: Method 'AutoTree.children_by_field' missing type hints
- 🔵 **Line 261**: Method 'AutoTree.children_by_type' missing type hints
- 🔵 **Line 1**: Function 'AutoTree.\_is_basemodel_type' uses overly generic type 'Any' for parameter 'type_hint'
- 🔵 **Line 1**: Function 'AutoTree.\_extract_basemodel_types' uses overly generic type 'Any' for parameter 'type_hint'

### src/haive/core/common/structures/named_dict.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 167**: Method 'NamedDict.keys' missing type hints
- 🔵 **Line 171**: Method 'NamedDict.items' missing type hints
- 🔵 **Line 175**: Method 'NamedDict.values_list' missing type hints
- 🔵 **Line 183**: Method 'NamedDict.clear' missing type hints
- 🔵 **Line 208**: Method 'NamedDict.to_dict' missing type hints
- 🔵 **Line 1**: Function 'NamedDict.convert_input' uses overly generic type 'Any' for parameter 'data'
- 🔵 **Line 1**: Function 'NamedDict.convert_input' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'NamedDict.\_extract_key' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'NamedDict.get' uses overly generic type 'Any' for parameter 'default'
- 🔵 **Line 1**: Function 'NamedDict.get' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'NamedDict.pop' uses overly generic type 'Any' for parameter 'default'
- 🔵 **Line 1**: Function 'NamedDict.pop' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'NamedDict.**getattr**' returns overly generic type 'Any'

### src/haive/core/common/mixins/engine_mixin.py

- 🔵 **Line 94**: Method 'EngineStateMixin.validate_and_organize_engines' missing type hints
- 🔵 **Line 215**: Method 'EngineStateMixin.get_all_engines' missing type hints
- 🔵 **Line 225**: Method 'EngineStateMixin.get_llms' missing type hints
- 🔵 **Line 233**: Method 'EngineStateMixin.get_retrievers' missing type hints
- 🔵 **Line 241**: Method 'EngineStateMixin.get_agents' missing type hints
- 🔵 **Line 249**: Method 'EngineStateMixin.get_vector_stores' missing type hints
- 🔵 **Line 257**: Method 'EngineStateMixin.get_tools' missing type hints
- 🔵 **Line 265**: Method 'EngineStateMixin.get_embeddings' missing type hints
- 🔵 **Line 689**: Method 'EngineStateMixin.get_engine_summary' missing type hints
- 🔵 **Line 1**: Function 'EngineStateMixin.display_engine_details' might return None but type signature doesn't indicate Optional

### src/haive/core/common/mixins/structured_output_mixin.py

- 🔵 **Line 1**: Function 'StructuredOutputMixin.\_create_structured_output_tool' returns overly generic type 'Any'

### src/haive/core/common/mixins/tool_route_mixin.py

- 🔵 **Line 198**: Method 'ToolRouteMixin.clear_tool_routes' missing type hints
- 🔵 **Line 389**: Method 'ToolRouteMixin.get_all_tools_flat' missing type hints
- 🔵 **Line 581**: Method 'ToolRouteMixin.debug_tool_routes' missing type hints
- 🔵 **Line 1**: Function 'ToolRouteMixin.\_generate_tool_name' uses overly generic type 'Any' for parameter 'tool'
- 🔵 **Line 1**: Function 'ToolRouteMixin.\_analyze_tool' uses overly generic type 'Any' for parameter 'tool'
- 🔵 **Line 1**: Function 'ToolRouteMixin.add_routed_tool' uses overly generic type 'Any' for parameter 'tool'
- 🔵 **Line 1**: Function 'ToolRouteMixin.to_tool' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'ToolRouteMixin.\_create_tool_implementation' returns overly generic type 'Any'

### src/haive/core/common/mixins/rich_logger_mixin.py

- 🔵 **Line 60**: Method 'RichLoggerMixin.logger' missing type hints

### src/haive/core/common/mixins/getter_mixin.py

- 🔵 **Line 111**: Method 'GetterMixin.filter' missing type hints
- 🔵 **Line 235**: Method 'GetterMixin.first' missing type hints
- 🔵 **Line 1**: Function 'GetterMixin.get_by_attr' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'GetterMixin.get_all_by_attr' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'GetterMixin.\_has_attr_value' uses overly generic type 'Any' for parameter 'item'
- 🔵 **Line 1**: Function 'GetterMixin.\_has_attr_value' uses overly generic type 'Any' for parameter 'value'

### src/haive/core/common/mixins/prompt_template_mixin.py

- 🔵 **Line 163**: Method 'PromptTemplateMixin.derive_input_schema' missing type hints
- 🔵 **Line 240**: Method 'PromptTemplateMixin.validate_prompt_template' missing type hints
- 🔵 **Line 259**: Method 'PromptTemplateMixin.get_prompt_engine' missing type hints
- 🔵 **Line 298**: Method 'PromptTemplateMixin.derive_prompt_input_schema' missing type hints
- 🔵 **Line 305**: Method 'PromptTemplateMixin.derive_prompt_output_schema' missing type hints
- 🔵 **Line 321**: Method 'PromptTemplateMixin.get_prompt_variables' missing type hints
- 🔵 **Line 341**: Method 'PromptTemplateMixin.update_prompt_partials' missing type hints
- 🔵 **Line 389**: Method 'PromptTemplateMixin.set_base_input_schema' missing type hints
- 🔵 **Line 393**: Method 'PromptTemplateMixin.enable_prompt_schema_derivation' missing type hints
- 🔵 **Line 397**: Method 'PromptTemplateMixin.get_effective_input_schema' missing type hints
- 🔵 **Line 451**: Method 'PromptTemplateMixin.get_prompt_aware_input_fields' missing type hints

### src/haive/core/common/mixins/tool_list_mixin.py

- 🔵 **Line 175**: Method 'ToolList.model_post_init' missing type hints
- 🔵 **Line 373**: Method 'ToolList.get_tool_type_mapping' missing type hints
- 🔵 **Line 446**: Method 'ToolList.get_model_classes' missing type hints
- 🔵 **Line 458**: Method 'ToolList.get_model_instances' missing type hints
- 🔵 **Line 470**: Method 'ToolList.get_tools_by_category' missing type hints
- 🔵 **Line 498**: Method 'ToolList.to_list' missing type hints
- 🔵 **Line 1**: Function 'ToolList.process_tools' uses overly generic type 'Any' for parameter 'data'
- 🔵 **Line 1**: Function 'ToolList.process_tools' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'ToolList.\_determine_tool_type' uses overly generic type 'Any' for parameter 'tool'
- 🔵 **Line 1**: Function 'ToolList.add' uses overly generic type 'Any' for parameter 'tool'
- 🔵 **Line 1**: Function 'ToolList.update' uses overly generic type 'Any' for parameter 'items'

### src/haive/core/common/mixins/identifier.py

- 🔵 **Line 111**: Method 'IdentifierMixin.initialize_uuid_obj' missing type hints
- 🔵 **Line 127**: Method 'IdentifierMixin.short_id' missing type hints
- 🔵 **Line 137**: Method 'IdentifierMixin.display_name' missing type hints
- 🔵 **Line 147**: Method 'IdentifierMixin.uuid_obj' missing type hints
- 🔵 **Line 159**: Method 'IdentifierMixin.has_custom_name' missing type hints
- 🔵 **Line 167**: Method 'IdentifierMixin.regenerate_id' missing type hints
- 🔵 **Line 191**: Method 'IdentifierMixin.clear_name' missing type hints
- 🔵 **Line 224**: Method 'IdentifierMixin.identifier_info' missing type hints

### src/haive/core/common/mixins/secure_config.py

- 🔵 **Line 147**: Method 'SecureConfigMixin.get_api_key' missing type hints

### src/haive/core/common/mixins/checkpointer_mixin.py

- 🔵 **Line 1**: Function 'CheckpointerMixin.\_ensure_checkpointer_initialized' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'CheckpointerMixin.get_checkpointer' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'CheckpointerMixin.run' uses overly generic type 'Any' for parameter 'input_data'
- 🔵 **Line 1**: Function 'CheckpointerMixin.run' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'CheckpointerMixin.stream' uses overly generic type 'Any' for parameter 'input_data'

### src/haive/core/common/types/general.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/common/types/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/common/models/documents/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/common/models/documents/github_repo.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 71**: Method 'GithubSettings.active_token' missing type hints
- 🔵 **Line 77**: Function 'get_github_settings' missing type hints
- 🔵 **Line 203**: Method 'GithubRepo.settings' missing type hints
- 🔵 **Line 210**: Method 'GithubRepo.http_client' missing type hints
- 🔵 **Line 236**: Method 'GithubRepo.extract_from_url_and_validate' missing type hints
- 🔵 **Line 462**: Method 'GithubRepo.get_api_headers' missing type hints
- 🔵 **Line 476**: Method 'GithubRepo.full_name' missing type hints
- 🔵 **Line 481**: Method 'GithubRepo.working_branch' missing type hints
- 🔵 **Line 486**: Method 'GithubRepo.ssh_url' missing type hints
- 🔵 **Line 491**: Method 'GithubRepo.requires_auth' missing type hints
- 🔵 **Line 518**: Method 'GithubRepo.refresh' missing type hints
- 🔵 **Line 522**: Method 'GithubRepo.to_safe_dict' missing type hints
- 🔵 **Line 1**: Function 'GithubRepo.switch_branch' parameter 'validate' name doesn't match type hint

### src/haive/core/common/mixins/general/state.py

- 🔵 **Line 93**: Method 'StateMixin.get_state_changes' missing type hints

### src/haive/core/common/mixins/general/id.py

- 🔵 **Line 48**: Method 'IdMixin.regenerate_id' missing type hints
- 🔵 **Line 60**: Method 'IdMixin.with_id' missing type hints

### src/haive/core/common/mixins/general/metadata.py

- 🔵 **Line 106**: Method 'MetadataMixin.clear_metadata' missing type hints
- 🔵 **Line 1**: Function 'MetadataMixin.add_metadata' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'MetadataMixin.get_metadata' uses overly generic type 'Any' for parameter 'default'
- 🔵 **Line 1**: Function 'MetadataMixin.get_metadata' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'MetadataMixin.remove_metadata' returns overly generic type 'Any'

### src/haive/core/common/mixins/general/timestamp.py

- 🔵 **Line 60**: Method 'TimestampMixin.update_timestamp' missing type hints
- 🔵 **Line 68**: Method 'TimestampMixin.age_in_seconds' missing type hints
- 🔵 **Line 79**: Method 'TimestampMixin.time_since_update' missing type hints

### src/haive/core/common/mixins/general/serialization.py

- 🔵 **Line 99**: Method 'SerializationMixin.from_dict' missing type hints
- 🔵 **Line 114**: Method 'SerializationMixin.from_json' missing type hints

### src/haive/core/common/mixins/general/version.py

- 🔵 **Line 62**: Method 'VersionMixin.get_version_history' missing type hints

### src/haive/core/common/types/protocols/general_protocols.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 88**: Method 'IOFieldAware.get_input_fields' missing type hints
- 🔵 **Line 92**: Method 'IOFieldAware.get_output_fields' missing type hints

### src/haive/core/common/types/protocols/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/common/types/protocols/schema_protocols.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 70**: Method 'IOFieldAware.get_input_fields' missing type hints
- 🔵 **Line 74**: Method 'IOFieldAware.get_output_fields' missing type hints

### src/haive/core/common/types/protocols/engine_protocols.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/persistence/store/base.py

- 🔵 **Line 73**: Method 'SerializableStoreWrapper.get_store' missing type hints

### src/haive/core/persistence/store/connection.py

- 🔵 **Line 1**: Function 'ConnectionManager.get_or_create_sync_pool' returns overly generic type 'Any'

### src/haive/core/persistence/store/memory.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/persistence/store/factory.py

- 🔵 **Line 45**: Method 'StoreFactory.create_with_lifecycle' missing type hints

### src/haive/core/persistence/store/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/persistence/store/wrappers/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/models/llm/export_llm_models_to_csv.py

- 🔵 **Line 58**: Function 'main' missing type hints

### src/haive/core/models/llm/base.py

- 🔵 **Line 169**: Method 'LLMConfig.set_default_name' missing type hints
- 🔵 **Line 179**: Method 'LLMConfig.load_model_metadata' missing type hints
- 🔵 **Line 281**: Method 'LLMConfig.format_metadata_for_display' missing type hints
- 🔵 **Line 329**: Method 'LLMConfig.instantiate' missing type hints
- 🔵 **Line 346**: Method 'LLMConfig.create_graph_transformer' missing type hints
- 🔵 **Line 418**: Method 'AzureLLMConfig.instantiate' missing type hints
- 🔵 **Line 482**: Method 'OpenAILLMConfig.get_models' missing type hints
- 🔵 **Line 489**: Method 'OpenAILLMConfig.instantiate' missing type hints
- 🔵 **Line 547**: Method 'AnthropicLLMConfig.get_models' missing type hints
- 🔵 **Line 554**: Method 'AnthropicLLMConfig.instantiate' missing type hints
- 🔵 **Line 600**: Method 'GeminiLLMConfig.instantiate' missing type hints
- 🔵 **Line 636**: Method 'DeepSeekLLMConfig.get_models' missing type hints
- 🔵 **Line 643**: Method 'DeepSeekLLMConfig.instantiate' missing type hints
- 🔵 **Line 690**: Method 'MistralLLMConfig.get_models' missing type hints
- 🔵 **Line 697**: Method 'MistralLLMConfig.instantiate' missing type hints
- 🔵 **Line 741**: Method 'GroqLLMConfig.instantiate' missing type hints
- 🔵 **Line 785**: Method 'CohereLLMConfig.instantiate' missing type hints
- 🔵 **Line 831**: Method 'TogetherAILLMConfig.instantiate' missing type hints
- 🔵 **Line 879**: Method 'FireworksAILLMConfig.instantiate' missing type hints
- 🔵 **Line 927**: Method 'PerplexityLLMConfig.instantiate' missing type hints
- 🔵 **Line 976**: Method 'HuggingFaceLLMConfig.instantiate' missing type hints
- 🔵 **Line 1042**: Method 'AI21LLMConfig.instantiate' missing type hints
- 🔵 **Line 1092**: Method 'AlephAlphaLLMConfig.instantiate' missing type hints
- 🔵 **Line 1138**: Method 'GooseAILLMConfig.instantiate' missing type hints
- 🔵 **Line 1188**: Method 'MosaicMLLLMConfig.instantiate' missing type hints
- 🔵 **Line 1234**: Method 'NLPCloudLLMConfig.instantiate' missing type hints
- 🔵 **Line 1286**: Method 'OpenLMLLMConfig.instantiate' missing type hints
- 🔵 **Line 1318**: Method 'PetalsLLMConfig.instantiate' missing type hints
- 🔵 **Line 1357**: Method 'ReplicateLLMConfig.instantiate' missing type hints
- 🔵 **Line 1404**: Method 'VertexAILLMConfig.instantiate' missing type hints
- 🔵 **Line 1470**: Method 'BedrockLLMConfig.instantiate' missing type hints
- 🔵 **Line 1516**: Method 'NVIDIALLMConfig.instantiate' missing type hints
- 🔵 **Line 1555**: Method 'OllamaLLMConfig.instantiate' missing type hints
- 🔵 **Line 1588**: Method 'LlamaCppLLMConfig.instantiate' missing type hints
- 🔵 **Line 1628**: Method 'UpstageLLMConfig.instantiate' missing type hints
- 🔵 **Line 1673**: Method 'DatabricksLLMConfig.instantiate' missing type hints
- 🔵 **Line 1722**: Method 'WatsonxLLMConfig.instantiate' missing type hints
- 🔵 **Line 1774**: Method 'XAILLMConfig.instantiate' missing type hints
- 🔵 **Line 1**: Function 'LLMConfig.\_display_debug_info' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'LLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'LLMConfig.create_graph_transformer' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'AzureLLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'OpenAILLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'AnthropicLLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'GeminiLLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'DeepSeekLLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'MistralLLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'GroqLLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'CohereLLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'TogetherAILLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'FireworksAILLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'PerplexityLLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'HuggingFaceLLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'AI21LLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'AlephAlphaLLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'GooseAILLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'MosaicMLLLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'NLPCloudLLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'OpenLMLLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'PetalsLLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'ReplicateLLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'VertexAILLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'BedrockLLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'NVIDIALLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'OllamaLLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'LlamaCppLLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'UpstageLLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'DatabricksLLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'WatsonxLLMConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'XAILLMConfig.instantiate' returns overly generic type 'Any'

### src/haive/core/models/llm/factory.py

- 🔵 **Line 215**: Method 'LLMFactory.get_available_providers' missing type hints
- 🔵 **Line 337**: Function 'get_available_providers' missing type hints
- 🔵 **Line 1**: Function 'LLMFactory.create' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'create_llm' returns overly generic type 'Any'

### src/haive/core/models/llm/rate_limiting_mixin.py

- 🔵 **Line 109**: Method 'RateLimitingMixin.get_rate_limit_info' missing type hints
- 🔵 **Line 1**: Function 'RateLimitingMixin.apply_rate_limiting' uses overly generic type 'Any' for parameter 'llm'
- 🔵 **Line 1**: Function 'RateLimitingMixin.apply_rate_limiting' returns overly generic type 'Any'

### src/haive/core/models/llm/engine.py

- 🔵 **Line 73**: Method 'LLMEngine.initialize' missing type hints
- 🔵 **Line 83**: Method 'LLMEngine.cleanup' missing type hints
- 🔵 **Line 138**: Method 'LLMEngine.get_model' missing type hints

### src/haive/core/models/llm/providers.py

- 🔵 **Line 63**: Method 'OpenAIConfig.instantiate' missing type hints
- 🔵 **Line 103**: Method 'OpenAIEngine.initialize' missing type hints
- 🔵 **Line 125**: Method 'OpenAIEngine.cleanup' missing type hints
- 🔵 **Line 208**: Method 'AzureConfig.instantiate' missing type hints
- 🔵 **Line 248**: Method 'AzureEngine.initialize' missing type hints
- 🔵 **Line 271**: Method 'AzureEngine.cleanup' missing type hints

### src/haive/core/models/embeddings/base.py

- 🔵 **Line 69**: Method 'SecureConfigMixin.resolve_api_key' missing type hints
- 🔵 **Line 128**: Method 'BaseEmbeddingConfig.instantiate' missing type hints
- 🔵 **Line 176**: Method 'AzureEmbeddingConfig.instantiate' missing type hints
- 🔵 **Line 194**: Method 'AzureEmbeddingConfig.get_api_key' missing type hints
- 🔵 **Line 255**: Method 'HuggingFaceEmbeddingConfig.instantiate' missing type hints
- 🔵 **Line 349**: Method 'OpenAIEmbeddingConfig.instantiate' missing type hints
- 🔵 **Line 392**: Method 'CohereEmbeddingConfig.instantiate' missing type hints
- 🔵 **Line 429**: Method 'OllamaEmbeddingConfig.instantiate' missing type hints
- 🔵 **Line 471**: Method 'SentenceTransformerEmbeddingConfig.instantiate' missing type hints
- 🔵 **Line 525**: Method 'FastEmbedEmbeddingConfig.instantiate' missing type hints
- 🔵 **Line 569**: Method 'JinaEmbeddingConfig.instantiate' missing type hints
- 🔵 **Line 609**: Method 'VertexAIEmbeddingConfig.instantiate' missing type hints
- 🔵 **Line 652**: Method 'BedrockEmbeddingConfig.instantiate' missing type hints
- 🔵 **Line 695**: Method 'CloudflareEmbeddingConfig.instantiate' missing type hints
- 🔵 **Line 739**: Method 'LlamaCppEmbeddingConfig.instantiate' missing type hints
- 🔵 **Line 781**: Method 'VoyageAIEmbeddingConfig.instantiate' missing type hints
- 🔵 **Line 818**: Method 'AnyscaleEmbeddingConfig.instantiate' missing type hints
- 🔵 **Line 1**: Function 'BaseEmbeddingConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'create_embeddings' returns overly generic type 'Any'

### src/haive/core/models/embeddings/test_embeddings.py

- 🔵 **Line 35**: Method 'TestEmbeddingProviders.test_provider_enum_values' missing type hints
- 🔵 **Line 42**: Method 'TestEmbeddingProviders.test_config_classes_exist' missing type hints
- 🔵 **Line 77**: Method 'TestEmbeddingProviders.test_factory_function' missing type hints

### src/haive/core/models/vectorstore/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 57**: Method 'VectorStoreConfig.add_document' missing type hints
- 🔵 **Line 61**: Method 'VectorStoreConfig.create_vectorstore' missing type hints
- 🔵 **Line 115**: Method 'VectorStoreConfig.create_retriever' missing type hints
- 🟡 **Line 150**: Function 'create_vectorstore' missing docstring
- 🔵 **Line 150**: Function 'create_vectorstore' missing type hints
- 🟡 **Line 154**: Function 'create_retriever' missing docstring
- 🔵 **Line 154**: Function 'create_retriever' missing type hints
- 🟡 **Line 158**: Function 'create_vs_config_from_documents' missing docstring
- 🟡 **Line 170**: Function 'create_vs_from_documents' missing docstring
- 🟡 **Line 182**: Function 'create_retriever_from_documents' missing docstring

### src/haive/core/models/vectorstore/com.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 125**: Method 'DynamicModuleConfig.get_available_classes' missing type hints
- 🔵 **Line 134**: Method 'DynamicModuleConfig.set_class_type' missing type hints
- 🔵 **Line 148**: Method 'DynamicModuleConfig.load_instance' missing type hints
- 🔵 **Line 184**: Method 'DynamicModuleConfig.get_class_metadata' missing type hints
- 🔵 **Line 199**: Method 'DynamicModuleConfig.get_tools' missing type hints
- 🔵 **Line 1**: Function 'DynamicModuleConfig.load_instance' returns overly generic type 'Any'

### src/haive/core/models/vectorstore/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/models/retriever/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 75**: Method 'RetrieverConfig.instantiate' missing type hints
- 🔵 **Line 80**: Method 'RetrieverConfig.register' missing type hints

### src/haive/core/models/retriever/asknews_retriever.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/models/retriever/vectorstore_retriever.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 61**: Method 'VectorStoreRetrieverConfig.instantiate' missing type hints
- 🔵 **Line 133**: Method 'VectorStoreRetrieverConfig.get_retriever' missing type hints

### src/haive/core/models/retriever/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/models/llm/providers/anthropic.py

- 🔵 **Line 189**: Method 'AnthropicProvider.get_models' missing type hints

### src/haive/core/models/llm/providers/base.py

- 🔵 **Line 190**: Method 'BaseLLMProvider.set_defaults' missing type hints
- 🔵 **Line 260**: Method 'BaseLLMProvider.load_api_key' missing type hints
- 🔵 **Line 322**: Method 'BaseLLMProvider.instantiate' missing type hints
- 🔵 **Line 398**: Method 'BaseLLMProvider.get_models' missing type hints
- 🔵 **Line 414**: Method 'BaseLLMProvider.create_graph_transformer' missing type hints
- 🔵 **Line 1**: Function 'BaseLLMProvider.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'BaseLLMProvider.create_graph_transformer' returns overly generic type 'Any'

### src/haive/core/models/llm/providers/openai.py

- 🔵 **Line 205**: Method 'OpenAIProvider.get_models' missing type hints

### src/haive/core/models/llm/providers/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition
- 🔵 **Line 191**: Function 'list_providers' missing type hints
- 🔵 **Line 1**: Function '\_lazy_import_provider' parameter 'provider' name doesn't match type hint
- 🔵 **Line 1**: Function 'get_provider' parameter 'provider' name doesn't match type hint

### src/haive/core/models/llm/providers/ollama.py

- 🔵 **Line 238**: Method 'OllamaProvider.get_models' missing type hints

### src/haive/core/models/llm/providers/google.py

- 🔵 **Line 200**: Method 'GeminiProvider.get_models' missing type hints
- 🔵 **Line 387**: Method 'VertexAIProvider.get_models' missing type hints

### src/haive/core/models/embeddings/filter/base.py

- 🔴 **Line 1**: Could not parse file: invalid syntax (<unknown>, line 1)

### src/haive/core/models/embeddings/filter/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/models/retriever/community/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 15**: Method 'BaseRetrieverConfig.create' missing docstring
- 🔵 **Line 15**: Method 'BaseRetrieverConfig.create' missing type hints
- 🟡 **Line 22**: Class 'CommunityRetrieverType' missing docstring
- 🟡 **Line 33**: Class 'CommunityRetrieverConfig' missing docstring
- 🔵 **Line 37**: Method 'CommunityRetrieverConfig.create' missing docstring
- 🔵 **Line 37**: Method 'CommunityRetrieverConfig.create' missing type hints

### src/haive/core/models/retriever/retrievers/time_weighted.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 32**: Method 'TimeWeightedRetrieverConfig.instantiate' missing type hints

### src/haive/core/models/retriever/retrievers/parent_document.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 29**: Method 'ParentDocumentRetrieverConfig.instantiate' missing type hints

### src/haive/core/models/retriever/retrievers/self_query.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 31**: Method 'SelfQueryRetrieverConfig.instantiate' missing type hints

### src/haive/core/models/retriever/retrievers/multiqery.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 28**: Method 'MultiQueryRetrieverConfig.instantiate' missing type hints

### src/haive/core/models/retriever/retrievers/ensemble.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 20**: Method 'EnsembleRetrieverConfig.instantiate' missing type hints

### src/haive/core/runtime/base/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 26**: Method 'RuntimeComponent.initialize' missing type hints

### src/haive/core/runtime/base/protocols.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 17**: Method 'RuntimeComponentProtocol.initialize' missing docstring
- 🔵 **Line 17**: Method 'RuntimeComponentProtocol.initialize' missing type hints
- 🔵 **Line 18**: Method 'RuntimeComponentProtocol.invoke' missing docstring

### src/haive/core/runtime/extension/base.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/runtime/extension/protocols.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 11**: Method 'ExtensionProtocol.apply_to' missing docstring
- 🔵 **Line 12**: Method 'ExtensionProtocol.apply' missing docstring

### src/haive/core/utils/pydantic_utils/ui.py

- 🔵 **Line 1**: Function 'format_type_annotation' uses overly generic type 'Any' for parameter 'type_annotation'
- 🔵 **Line 1**: Function 'format_default_value' uses overly generic type 'Any' for parameter 'field_info'
- 🔵 **Line 1**: Function 'format_value' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'format_field_info' uses overly generic type 'Any' for parameter 'field_info'
- 🔵 **Line 1**: Function 'schema_to_code' uses overly generic type 'Any' for parameter 'schema'

### src/haive/core/utils/pydantic_utils/general.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 1**: Function 'ensure_json_serializable' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'ensure_json_serializable' returns overly generic type 'Any'

### src/haive/core/utils/pydantic_utils/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/utils/pydantic_utils/sync_properties.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 8**: Function 'create_sync_properties' missing type hints
- 🟡 **Line 11**: Function 'decorator' missing docstring
- 🔵 **Line 11**: Function 'decorator' missing type hints
- 🟡 **Line 14**: Function 'make_property' missing docstring
- 🔵 **Line 14**: Function 'make_property' missing type hints
- 🟡 **Line 15**: Function 'getter' missing docstring
- 🔵 **Line 15**: Function 'getter' missing type hints
- 🟡 **Line 18**: Function 'setter' missing docstring
- 🔵 **Line 18**: Function 'setter' missing type hints

### src/haive/core/utils/tools/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/utils/tools/tool_schema_generator.py

- 🟡 **Line 773**: Class 'SearchQueries' missing docstring
- 🟡 **Line 778**: Class 'AnswerQuestion' missing docstring
- 🔵 **Line 785**: Function 'execute_search_goal' missing type hints
- 🟡 **Line 611**: Function 'create_wrapper' missing docstring
- 🔵 **Line 611**: Function 'create_wrapper' missing type hints
- 🔵 **Line 803**: Function 'run_queries' missing type hints
- 🟡 **Line 612**: Function 'wrapper' missing docstring
- 🔵 **Line 612**: Function 'wrapper' missing type hints
- 🔵 **Line 1**: Function '\_extract_from_langchain_tool' uses overly generic type 'Any' for parameter 'tool'
- 🔵 **Line 1**: Function 'invoke_from_schema' returns overly generic type 'Any'

### src/haive/core/utils/haive_discovery/discovery_engine.py

- 🔵 **Line 42**: Method 'EnhancedComponentDiscovery.add_analyzer' missing type hints
- 🔵 **Line 1**: Function 'EnhancedComponentDiscovery.\_analyze_object' uses overly generic type 'Any' for parameter 'obj'

### src/haive/core/utils/haive_discovery/base_analyzer.py

- 🔵 **Line 1**: Function 'ComponentAnalyzer.can_analyze' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'ComponentAnalyzer.analyze' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'ComponentAnalyzer.safe_get_name' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'ComponentAnalyzer.safe_get_class_name' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'ComponentAnalyzer.get_source_code' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'ComponentAnalyzer.extract_schema' uses overly generic type 'Any' for parameter 'obj'

### src/haive/core/utils/haive_discovery/retriever_analyzers.py

- 🔵 **Line 30**: Method 'RetrieverAnalyzer.can_analyze' missing docstring
- 🔵 **Line 49**: Method 'RetrieverAnalyzer.analyze' missing docstring
- 🔵 **Line 167**: Method 'VectorStoreAnalyzer.can_analyze' missing docstring
- 🔵 **Line 185**: Method 'VectorStoreAnalyzer.analyze' missing docstring
- 🟡 **Line 85**: Class 'RetrieverArgs' missing docstring
- 🟡 **Line 212**: Class 'VectorStoreArgs' missing docstring
- 🔵 **Line 1**: Function 'RetrieverAnalyzer.can_analyze' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'RetrieverAnalyzer.analyze' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'VectorStoreAnalyzer.can_analyze' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'VectorStoreAnalyzer.analyze' uses overly generic type 'Any' for parameter 'obj'

### src/haive/core/utils/haive_discovery/tool_analyzers.py

- 🔵 **Line 30**: Method 'ToolAnalyzer.can_analyze' missing docstring
- 🔵 **Line 38**: Method 'ToolAnalyzer.analyze' missing docstring
- 🔵 **Line 57**: Method 'DocumentLoaderAnalyzer.can_analyze' missing docstring
- 🔵 **Line 64**: Method 'DocumentLoaderAnalyzer.analyze' missing docstring
- 🔵 **Line 1**: Function 'ToolAnalyzer.can_analyze' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'ToolAnalyzer.analyze' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'DocumentLoaderAnalyzer.can_analyze' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'DocumentLoaderAnalyzer.analyze' uses overly generic type 'Any' for parameter 'obj'

### src/haive/core/utils/haive_discovery/utils.py

- 🔴 **Line 1**: Could not parse file: unexpected indent (<unknown>, line 214)

### src/haive/core/utils/haive_discovery/engine_analyzer.py

- 🔵 **Line 19**: Method 'EngineAnalyzer.can_analyze' missing docstring
- 🔵 **Line 26**: Method 'EngineAnalyzer.analyze' missing docstring
- 🔵 **Line 1**: Function 'EngineAnalyzer.can_analyze' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'EngineAnalyzer.analyze' uses overly generic type 'Any' for parameter 'obj'

### src/haive/core/utils/haive_discovery/component_info.py

- 🔵 **Line 33**: Method 'ComponentInfo.to_dict' missing type hints
- 🔵 **Line 138**: Method 'ComponentInfo.to_document_content' missing type hints
- 🔵 **Line 1**: Function 'ComponentInfo.\_make_json_serializable' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'ComponentInfo.\_make_json_serializable' returns overly generic type 'Any'

### src/haive/core/types/general/file_types.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/types/general/programming_languages.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/aug_llm/config.py

- 🔵 **Line 83**: Function 'debug_print' missing type hints
- 🔵 **Line 445**: Method 'AugLLMConfig.validate_tools' missing type hints
- 🔵 **Line 461**: Method 'AugLLMConfig.validate_schemas' missing type hints
- 🔵 **Line 468**: Method 'AugLLMConfig.validate_structured_output_model' missing type hints
- 🔵 **Line 480**: Method 'AugLLMConfig.set_default_structured_output_version' missing type hints
- 🔵 **Line 493**: Method 'AugLLMConfig.ensure_structured_output_as_tool' missing type hints
- 🔵 **Line 528**: Method 'AugLLMConfig.default_schemas_to_tools' missing type hints
- 🔵 **Line 541**: Method 'AugLLMConfig.comprehensive_validation_and_setup' missing type hints
- 🔵 **Line 1657**: Method 'AugLLMConfig.get_input_fields' missing type hints
- 🔵 **Line 1661**: Method 'AugLLMConfig.get_output_fields' missing type hints
- 🔵 **Line 2175**: Method 'AugLLMConfig.instantiate_llm' missing type hints
- 🔵 **Line 2338**: Method 'AugLLMConfig.from_llm_config' missing type hints
- 🔵 **Line 2343**: Method 'AugLLMConfig.from_prompt' missing type hints
- 🔵 **Line 2402**: Method 'AugLLMConfig.from_system_prompt' missing type hints
- 🔵 **Line 2443**: Method 'AugLLMConfig.from_few_shot' missing type hints
- 🔵 **Line 2491**: Method 'AugLLMConfig.from_few_shot_chat' missing type hints
- 🔵 **Line 2551**: Method 'AugLLMConfig.from_system_and_few_shot' missing type hints
- 🔵 **Line 2606**: Method 'AugLLMConfig.from_tools' missing type hints
- 🔵 **Line 2667**: Method 'AugLLMConfig.from_pydantic_tools' missing type hints
- 🔵 **Line 2740**: Method 'AugLLMConfig.from_format_instructions' missing type hints
- 🔵 **Line 2765**: Method 'AugLLMConfig.from_structured_output_v1' missing type hints
- 🔵 **Line 2834**: Method 'AugLLMConfig.from_structured_output_v2' missing type hints
- 🔵 **Line 2918**: Method 'AugLLMConfig.debug_tool_configuration' missing type hints
- 🔵 **Line 2982**: Method 'AugLLMConfig.instantiate_llm' missing type hints
- 🟡 **Line 2211**: Class 'LLMInput' missing docstring
- 🔵 **Line 1**: Function 'AugLLMConfig.add_tool' uses overly generic type 'Any' for parameter 'tool'
- 🔵 **Line 1**: Function 'AugLLMConfig.remove_tool' uses overly generic type 'Any' for parameter 'tool'
- 🔵 **Line 1**: Function 'AugLLMConfig.instantiate_llm' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'AugLLMConfig.\_create_tool_implementation' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'AugLLMConfig.\_create_llm_function_tool' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'AugLLMConfig.\_create_structured_output_tool' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'AugLLMConfig.add_tool_with_route' uses overly generic type 'Any' for parameter 'tool'
- 🔵 **Line 1**: Function 'AugLLMConfig.create_tool_from_config' uses overly generic type 'Any' for parameter 'config'
- 🔵 **Line 1**: Function 'AugLLMConfig.create_tool_from_config' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'AugLLMConfig.instantiate_llm' returns overly generic type 'Any'

### src/haive/core/engine/aug_llm/factory.py

- 🔵 **Line 269**: Method 'AugLLMFactory.create_runnable' missing type hints
- 🟡 **Line 846**: Class 'PydanticModelTool' missing docstring
- 🔵 **Line 1**: Function 'AugLLMFactory.**init**' uses overly generic type 'Any' for parameter 'aug_config'

### src/haive/core/engine/base/base.py

- 🔵 **Line 89**: Method 'Engine.get_input_fields' missing type hints
- 🔵 **Line 102**: Method 'Engine.get_output_fields' missing type hints
- 🔵 **Line 130**: Method 'Engine.get_schema_fields' missing type hints
- 🔵 **Line 154**: Method 'Engine.derive_input_schema' missing type hints
- 🔵 **Line 182**: Method 'Engine.derive_output_schema' missing type hints
- 🔵 **Line 232**: Method 'Engine.register' missing type hints
- 🔵 **Line 330**: Method 'Engine.extract_params' missing type hints
- 🔵 **Line 384**: Method 'Engine.to_dict' missing type hints
- 🔵 **Line 477**: Method 'Engine.to_json' missing type hints
- 🔵 **Line 1**: Function 'Engine.create_runnable' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'Engine.instantiate' returns overly generic type 'Any'

### src/haive/core/engine/base/factory.py

- 🔵 **Line 65**: Method 'ComponentFactory.create' missing type hints
- 🔵 **Line 104**: Method 'ComponentFactory.invalidate_cache' missing type hints
- 🔵 **Line 1**: Function 'ComponentFactory.for_engine' uses overly generic type 'Any' for parameter 'engine'

### src/haive/core/engine/base/registry.py

- 🔵 **Line 36**: Method 'EngineRegistry.get_instance' missing type hints
- 🔵 **Line 208**: Method 'EngineRegistry.clear' missing type hints

### src/haive/core/engine/base/reference.py

- 🔵 **Line 69**: Method 'ComponentRef.resolve' missing type hints
- 🔵 **Line 90**: Method 'ComponentRef.invalidate_cache' missing type hints

### src/haive/core/engine/document/universal_loader.py

- 🔵 **Line 587**: Method 'UniversalDocumentLoader.get_supported_sources' missing type hints

### src/haive/core/engine/document/config.py

- 🔵 **Line 200**: Method 'DocumentEngineConfig.validate_chunk_overlap' missing type hints
- 🔵 **Line 309**: Method 'ProcessedDocument.update_statistics' missing type hints
- 🔵 **Line 365**: Method 'DocumentOutput.update_statistics' missing type hints

### src/haive/core/engine/document/factory.py

- 🔴 **Line 1**: Could not parse file: expected an indented block after 'if' statement on line 133 (<unknown>, line 134)

### src/haive/core/engine/document/**init**.py

- 🔵 **Line 80**: Function 'load_documents' missing type hints

### src/haive/core/engine/document/engine.py

- 🔵 **Line 107**: Method 'DocumentEngine.validate_config' missing type hints
- 🔵 **Line 119**: Method 'DocumentEngine.get_input_fields' missing type hints
- 🔵 **Line 131**: Method 'DocumentEngine.get_output_fields' missing type hints

### src/haive/core/engine/document/agents.py

- 🔵 **Line 77**: Method 'DocumentAgent.setup_agent' missing type hints
- 🔵 **Line 94**: Method 'DocumentAgent.build_graph' missing type hints
- 🔵 **Line 215**: Method 'FileDocumentAgent.setup_agent' missing type hints
- 🔵 **Line 248**: Method 'WebDocumentAgent.setup_agent' missing type hints
- 🔵 **Line 294**: Method 'DirectoryDocumentAgent.setup_agent' missing type hints

### src/haive/core/engine/document/path_analysis.py

- 🔵 **Line 215**: Method 'PathAnalysisResult.source_summary' missing type hints
- 🔵 **Line 1**: Function 'extract_cloud_storage_info' parameter 'provider' name doesn't match type hint

### src/haive/core/engine/vectorstore/vectorstore.py

- 🔵 **Line 263**: Method 'VectorStoreConfig.validate_engine_type' missing docstring
- 🔵 **Line 263**: Method 'VectorStoreConfig.validate_engine_type' missing type hints
- 🔵 **Line 268**: Method 'VectorStoreConfig.get_input_fields' missing type hints
- 🔵 **Line 285**: Method 'VectorStoreConfig.get_output_fields' missing type hints
- 🔵 **Line 653**: Method 'VectorStoreConfig.get_vectorstore' missing type hints
- 🔵 **Line 675**: Method 'VectorStoreConfig.extract_params' missing type hints
- 🔵 **Line 882**: Method 'VectorStoreProviderRegistry.list_providers' missing type hints

### src/haive/core/engine/retriever/mixins.py

- 🔵 **Line 32**: Method 'RetrieverMixin.convert_vectorstore_to_retriever' missing type hints
- 🔵 **Line 41**: Method 'RetrieverMixin.from_vectorstore' missing type hints
- 🔵 **Line 66**: Method 'RetrieverMixin.from_documents' missing type hints
- 🔵 **Line 114**: Method 'RetrieverMixin.from_retriever' missing type hints

### src/haive/core/engine/retriever/retriever.py

- 🔵 **Line 91**: Method 'RetrieverOutput.validate_documents' missing type hints
- 🔵 **Line 172**: Method 'BaseRetrieverConfig.validate_engine_type' missing type hints
- 🔵 **Line 178**: Method 'BaseRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 189**: Method 'BaseRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 270**: Method 'BaseRetrieverConfig.instantiate' missing type hints
- 🔵 **Line 309**: Method 'BaseRetrieverConfig.register' missing type hints
- 🔵 **Line 482**: Method 'VectorStoreRetrieverConfig.validate_retriever_type' missing type hints
- 🔵 **Line 488**: Method 'VectorStoreRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/agent/pattern.py

- 🔵 **Line 182**: Method 'PatternManager.get_pattern_order' missing type hints
- 🔵 **Line 235**: Method 'PatternManager.patterns_as_list' missing type hints
- 🔵 **Line 243**: Method 'PatternManager.parameters_as_dict' missing type hints
- 🔵 **Line 251**: Method 'PatternManager.applied_patterns_as_set' missing type hints
- 🔵 **Line 259**: Method 'PatternManager.validate_patterns' missing type hints
- 🔵 **Line 280**: Method 'PatternManager.get_required_components' missing type hints
- 🔵 **Line 307**: Method 'PatternManager.to_dict' missing type hints

### src/haive/core/engine/agent/config.py

- 🔵 **Line 250**: Method 'AgentConfig.ensure_engine' missing type hints
- 🔵 **Line 259**: Method 'AgentConfig.ensure_state_schema' missing type hints
- 🔵 **Line 266**: Method 'AgentConfig.get_input_fields' missing type hints
- 🔵 **Line 291**: Method 'AgentConfig.get_output_fields' missing type hints
- 🔵 **Line 384**: Method 'AgentConfig.get_schema_manager' missing type hints
- 🔵 **Line 435**: Method 'AgentConfig.derive_schema' missing type hints
- 🔵 **Line 603**: Method 'AgentConfig.derive_input_schema' missing type hints
- 🔵 **Line 672**: Method 'AgentConfig.derive_output_schema' missing type hints
- 🔵 **Line 743**: Method 'AgentConfig.resolve_engine' missing type hints
- 🔵 **Line 781**: Method 'AgentConfig.build_agent' missing type hints
- 🔵 **Line 996**: Method 'AgentConfig.get_schema_fields' missing type hints
- 🔵 **Line 1013**: Method 'AgentConfig.extract_params' missing type hints
- 🔵 **Line 1043**: Method 'AgentConfig.to_dict' missing type hints
- 🔵 **Line 1139**: Method 'AgentConfig.to_json' missing type hints
- 🔵 **Line 1165**: Method 'AgentConfig.clear_schema_caches' missing type hints
- 🔵 **Line 1251**: Method 'AgentConfig.set_testing_mode' missing type hints
- 🔵 **Line 1320**: Method 'AgentConfig.get_pattern_order' missing type hints
- 🔵 **Line 1**: Function 'AgentConfig.\_validate_agent_protocols' uses overly generic type 'Any' for parameter 'agent'
- 🔵 **Line 1**: Function 'AgentConfig.create_runnable' returns overly generic type 'Any'

### src/haive/core/engine/agent/protocols.py

- 🔵 **Line 37**: Method 'AgentProtocol.app' missing type hints
- 🔵 **Line 83**: Method 'AgentProtocol.compile' missing type hints
- 🔵 **Line 87**: Method 'AgentProtocol.setup_workflow' missing type hints
- 🔵 **Line 254**: Function 'assert_agent_protocols' missing type hints
- 🔵 **Line 1**: Function 'AgentProtocol.app' returns overly generic type 'Any'

### src/haive/core/engine/agent/registry.py

- 🔵 **Line 18**: Function 'register_agent' missing type hints
- 🟡 **Line 28**: Function 'decorator' missing docstring
- 🔵 **Line 28**: Function 'decorator' missing type hints
- 🔵 **Line 1**: Function '\_resolve_agent_class_by_name' might return None but type signature doesn't indicate Optional

### src/haive/core/engine/agent/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/engine/agent/agent.py

- 🔵 **Line 85**: Function 'register_agent' missing type hints
- 🔵 **Line 214**: Method 'Agent.set_traceback_mode' missing type hints
- 🔵 **Line 232**: Method 'Agent.debug_simple' missing type hints
- 🔵 **Line 1475**: Method 'Agent.setup_workflow' missing type hints
- 🔵 **Line 1485**: Method 'Agent.app' missing type hints
- 🔵 **Line 1491**: Method 'Agent.compile' missing type hints
- 🟡 **Line 88**: Function 'decorator' missing docstring
- 🔵 **Line 88**: Function 'decorator' missing type hints
- 🔵 **Line 1**: Function 'Agent.debug_simple' uses overly generic type 'Any' for parameter 'data'
- 🔵 **Line 1**: Function 'Agent.app' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'Agent.\_prepare_input' uses overly generic type 'Any' for parameter 'input_data'
- 🔵 **Line 1**: Function 'Agent.\_prepare_input' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'Agent.\_process_output' uses overly generic type 'Any' for parameter 'output_data'
- 🔵 **Line 1**: Function 'Agent.\_process_output' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'Agent.\_process_stream_chunk' uses overly generic type 'Any' for parameter 'chunk'
- 🔵 **Line 1**: Function 'Agent.inspect_state' might return None but type signature doesn't indicate Optional

### src/haive/core/engine/embedding/base.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 18**: Class 'SecureConfigMixin' missing docstring
- 🔵 **Line 21**: Method 'SecureConfigMixin.resolve_api_key' missing docstring
- 🔵 **Line 21**: Method 'SecureConfigMixin.resolve_api_key' missing type hints
- 🟡 **Line 42**: Class 'BaseEmbeddingConfig' missing docstring
- 🔵 **Line 47**: Method 'BaseEmbeddingConfig.instantiate' missing docstring
- 🔵 **Line 47**: Method 'BaseEmbeddingConfig.instantiate' missing type hints
- 🟡 **Line 51**: Class 'AzureEmbeddingConfig' missing docstring
- 🔵 **Line 66**: Method 'AzureEmbeddingConfig.instantiate' missing docstring
- 🔵 **Line 66**: Method 'AzureEmbeddingConfig.instantiate' missing type hints
- 🔵 **Line 75**: Method 'AzureEmbeddingConfig.get_api_key' missing docstring
- 🔵 **Line 75**: Method 'AzureEmbeddingConfig.get_api_key' missing type hints
- 🟡 **Line 79**: Class 'HuggingFaceEmbeddingConfig' missing docstring
- 🔵 **Line 94**: Method 'HuggingFaceEmbeddingConfig.instantiate' missing docstring
- 🔵 **Line 94**: Method 'HuggingFaceEmbeddingConfig.instantiate' missing type hints
- 🟡 **Line 144**: Function 'create_embeddings' missing docstring
- 🔵 **Line 1**: Function 'BaseEmbeddingConfig.instantiate' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'create_embeddings' returns overly generic type 'Any'

### src/haive/core/engine/embedding/config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/embedding/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/engine/embedding/types.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/prompt_template/prompt_engine.py

- 🔵 **Line 202**: Method 'PromptTemplateEngine.derive_input_schema' missing type hints
- 🔵 **Line 334**: Method 'PromptTemplateEngine.derive_output_schema' missing type hints
- 🔵 **Line 427**: Method 'PromptTemplateEngine.get_input_fields' missing type hints
- 🔵 **Line 437**: Method 'PromptTemplateEngine.get_output_fields' missing type hints
- 🔵 **Line 447**: Method 'PromptTemplateEngine.create_runnable' missing type hints
- 🔵 **Line 452**: Method 'PromptTemplateEngine.to_runnable' missing type hints

### src/haive/core/engine/output_parser/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 119**: Method 'OutputParserEngine.get_input_fields' missing type hints
- 🔵 **Line 130**: Method 'OutputParserEngine.get_output_fields' missing type hints
- 🔵 **Line 1**: Function 'OutputParserEngine.create_runnable' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'OutputParserEngine.\_create_structured_parser' returns overly generic type 'Any'

### src/haive/core/engine/output_parser/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/engine/output_parser/types.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/tool/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 71**: Method 'ToolEngine.create_runnable' missing type hints
- 🔵 **Line 261**: Method 'ToolEngine.validate_engine_type' missing type hints
- 🔵 **Line 268**: Method 'ToolEngine.validate_tools' missing type hints
- 🔵 **Line 283**: Method 'ToolEngine.validate_toolkit' missing type hints
- 🔵 **Line 305**: Method 'ToolEngine.validate_tool_choice' missing type hints
- 🟡 **Line 68**: Class 'Config' missing docstring
- 🔵 **Line 1**: Function 'ToolEngine.create_runnable' returns overly generic type 'Any'

### src/haive/core/engine/tool/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/engine/document/transformers/base.py

- 🔵 **Line 91**: Method 'DocTransformerEngine.get_input_fields' missing type hints
- 🔵 **Line 102**: Method 'DocTransformerEngine.get_output_fields' missing type hints
- 🔵 **Line 457**: Method 'DocTransformerRegistry.get_instance' missing type hints
- 🔵 **Line 490**: Method 'DocTransformerRegistry.clear' missing type hints
- 🔵 **Line 1**: Function 'DocTransformerEngine.create_runnable' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'DocTransformerRegistry.get' uses overly generic type 'Any' for parameter 'item_type'
- 🔵 **Line 1**: Function 'DocTransformerRegistry.list' uses overly generic type 'Any' for parameter 'item_type'
- 🔵 **Line 1**: Function 'DocTransformerRegistry.get_all' uses overly generic type 'Any' for parameter 'item_type'

### src/haive/core/engine/document/transformers/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/engine/document/transformers/types.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/base/schema.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/sources/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 16**: Method 'SourceInterface.get_source_value' missing docstring
- 🔵 **Line 16**: Method 'SourceInterface.get_source_value' missing type hints
- 🔵 **Line 17**: Method 'SourceInterface.validate' missing docstring
- 🔵 **Line 17**: Method 'SourceInterface.validate' missing type hints
- 🔵 **Line 18**: Method 'SourceInterface.get_metadata' missing docstring
- 🔵 **Line 18**: Method 'SourceInterface.get_metadata' missing type hints
- 🔵 **Line 39**: Method 'BaseSource.get_source_value' missing type hints
- 🔵 **Line 44**: Method 'BaseSource.validate' missing type hints
- 🔵 **Line 49**: Method 'BaseSource.source_id' missing type hints
- 🔵 **Line 55**: Method 'BaseSource.source_category' missing type hints
- 🔵 **Line 61**: Method 'BaseSource.get_metadata' missing type hints
- 🔵 **Line 1**: Function 'SourceInterface.get_source_value' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'BaseSource.get_source_value' returns overly generic type 'Any'

### src/haive/core/engine/document/sources/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/engine/document/sources/web.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 37**: Method 'WebSource.validate_source_type' missing type hints
- 🔵 **Line 51**: Method 'WebSource.get_source_value' missing type hints
- 🔵 **Line 55**: Method 'WebSource.validate' missing type hints
- 🔵 **Line 63**: Method 'WebSource.domain' missing type hints
- 🔵 **Line 69**: Method 'WebSource.scheme' missing type hints
- 🔵 **Line 75**: Method 'WebSource.path' missing type hints
- 🔵 **Line 81**: Method 'WebSource.query_params' missing type hints
- 🔵 **Line 86**: Method 'WebSource.get_metadata' missing type hints
- 🔵 **Line 126**: Method 'ApiSource.get_metadata' missing type hints

### src/haive/core/engine/document/sources/local.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 39**: Method 'FileSource.validate_file_exists' missing type hints
- 🔵 **Line 45**: Method 'FileSource.get_source_value' missing type hints
- 🔵 **Line 49**: Method 'FileSource.validate' missing type hints
- 🔵 **Line 54**: Method 'FileSource.file_name' missing type hints
- 🔵 **Line 59**: Method 'FileSource.file_extension' missing type hints
- 🔵 **Line 64**: Method 'FileSource.file_size' missing type hints
- 🔵 **Line 69**: Method 'FileSource.last_modified' missing type hints
- 🔵 **Line 75**: Method 'FileSource.content_type' missing type hints
- 🔵 **Line 85**: Method 'FileSource.get_metadata' missing type hints
- 🔵 **Line 125**: Method 'DirectorySource.validate_directory_exists' missing type hints
- 🔵 **Line 131**: Method 'DirectorySource.get_source_value' missing type hints
- 🔵 **Line 135**: Method 'DirectorySource.validate' missing type hints
- 🔵 **Line 142**: Method 'DirectorySource.directory_name' missing type hints
- 🔵 **Line 147**: Method 'DirectorySource.file_count' missing type hints
- 🔵 **Line 158**: Method 'DirectorySource.last_modified' missing type hints
- 🔵 **Line 163**: Method 'DirectorySource.get_metadata' missing type hints
- 🔵 **Line 191**: Method 'DirectorySource.list_subdirectories' missing type hints

### src/haive/core/engine/document/loaders/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 75**: Method 'DocumentLoaderEngine.supported_source_types_names' missing type hints
- 🔵 **Line 79**: Method 'DocumentLoaderEngine.get_input_fields' missing type hints
- 🔵 **Line 118**: Method 'DocumentLoaderEngine.get_output_fields' missing type hints
- 🔵 **Line 322**: Method 'DocumentLoaderEngine.execution_log' missing type hints
- 🔵 **Line 327**: Method 'DocumentLoaderEngine.loaded_sources' missing type hints

### src/haive/core/engine/document/loaders/strategy.py

- 🔵 **Line 128**: Method 'LoaderStrategy.check_availability' missing type hints
- 🔵 **Line 1854**: Method 'LoaderStrategyRegistry.register' missing type hints

### src/haive/core/engine/document/loaders/registry.py

- 🔵 **Line 58**: Method 'DocumentLoaderRegistry.get_instance' missing type hints
- 🔵 **Line 170**: Method 'DocumentLoaderRegistry.get_all_metadata' missing type hints
- 🔵 **Line 225**: Method 'DocumentLoaderRegistry.clear' missing type hints
- 🔵 **Line 318**: Function 'get_default_registry' missing type hints
- 🟡 **Line 257**: Function 'decorator' missing docstring

### src/haive/core/engine/document/loaders/source_base.py

- 🔵 **Line 27**: Method 'BaseSource.validate_source' missing type hints
- 🔵 **Line 32**: Method 'BaseSource.get_loader_kwargs' missing type hints
- 🔵 **Line 43**: Method 'LocalSource.validate_source' missing type hints
- 🔵 **Line 48**: Method 'LocalSource.get_loader_kwargs' missing type hints
- 🔵 **Line 65**: Method 'DirectorySource.validate_source' missing type hints
- 🔵 **Line 70**: Method 'DirectorySource.get_loader_kwargs' missing type hints
- 🔵 **Line 90**: Method 'RemoteSource.validate_source' missing type hints
- 🔵 **Line 99**: Method 'RemoteSource.get_loader_kwargs' missing type hints
- 🔵 **Line 124**: Method 'DatabaseSource.validate_source' missing type hints
- 🔵 **Line 128**: Method 'DatabaseSource.get_loader_kwargs' missing type hints
- 🔵 **Line 152**: Method 'CloudSource.get_loader_kwargs' missing type hints

### src/haive/core/engine/document/loaders/engine.py

- 🔵 **Line 79**: Method 'DocumentLoaderEngine.ensure_valid_configuration' missing type hints
- 🔵 **Line 91**: Method 'DocumentLoaderEngine.get_input_fields' missing type hints
- 🔵 **Line 126**: Method 'DocumentLoaderEngine.get_output_fields' missing type hints
- 🔵 **Line 1**: Function 'DocumentLoaderEngine.create_runnable' returns overly generic type 'Any'

### src/haive/core/engine/document/loaders/base_new.py

- 🔵 **Line 121**: Method 'BaseSource.get_patterns' missing type hints
- 🔵 **Line 126**: Method 'BaseSource.get_loader_strategies' missing type hints
- 🔵 **Line 188**: Method 'LocalSource.validate_file_exists' missing type hints
- 🔵 **Line 205**: Method 'RemoteSource.requires_authentication' missing type hints

### src/haive/core/engine/document/splitters/base.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/splitters/config.py

- 🔴 **Line 1**: Could not parse file: unexpected indent (<unknown>, line 3)

### src/haive/core/engine/document/splitters/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/engine/document/types/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/engine/document/examples/universal_loader_demo.py

- 🔵 **Line 22**: Function 'demo_universal_loader' missing type hints
- 🔵 **Line 146**: Function 'show_supported_sources' missing type hints

### src/haive/core/engine/document/loaders/base/base.py

- 🔵 **Line 35**: Method 'BaseDocumentLoader.load' missing type hints
- 🔵 **Line 44**: Method 'BaseDocumentLoader.lazy_load' missing type hints
- 🔵 **Line 56**: Method 'SimpleDocumentLoader.load' missing type hints
- 🔵 **Line 86**: Method 'SimpleDocumentLoader.lazy_load' missing type hints
- 🔵 **Line 208**: Method 'TextDocumentLoader.load' missing type hints
- 🔵 **Line 219**: Method 'TextDocumentLoader.lazy_load' missing type hints

### src/haive/core/engine/document/loaders/base/schema.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/base/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/engine/document/loaders/base/methods.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/adapters/base.py

- 🔵 **Line 42**: Method 'LoaderAdapter.load' missing type hints
- 🔵 **Line 53**: Method 'LoaderAdapter.load_and_split' missing type hints
- 🔵 **Line 80**: Method 'LoaderAdapter.fetch_all' missing type hints

### src/haive/core/engine/document/loaders/adapters/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/engine/document/loaders/adapters/local.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/specific/web_huggingface_enhanced.py

- 🔵 **Line 48**: Method 'HuggingFacePapersSource.create_loader' missing type hints
- 🔵 **Line 91**: Method 'HuggingFaceCollectionsSource.create_loader' missing type hints
- 🔵 **Line 127**: Method 'HuggingFaceOrganizationsSource.create_loader' missing type hints
- 🔵 **Line 169**: Method 'HuggingFaceExtendedDatasetSource.create_loader' missing type hints
- 🔵 **Line 226**: Method 'HuggingFaceModelCardSource.create_loader' missing type hints
- 🔵 **Line 265**: Method 'HuggingFacePapersLoader.load' missing type hints
- 🔵 **Line 358**: Method 'HuggingFaceCollectionsLoader.load' missing type hints
- 🔵 **Line 419**: Method 'HuggingFaceOrganizationsLoader.load' missing type hints
- 🔵 **Line 515**: Method 'ExtendedHuggingFaceDatasetLoader.load' missing type hints
- 🔵 **Line 582**: Method 'HuggingFaceModelCardLoader.load' missing type hints

### src/haive/core/engine/document/loaders/specific/files_scientific.py

- 🔵 **Line 27**: Method 'BibtexSource.create_loader' missing type hints
- 🔵 **Line 56**: Method 'CONLLUSource.create_loader' missing type hints
- 🔵 **Line 86**: Method 'MathMLSource.create_loader' missing type hints
- 🔵 **Line 119**: Method 'FortranSource.create_loader' missing type hints
- 🔵 **Line 139**: Method 'MatlabSource.create_loader' missing type hints
- 🔵 **Line 161**: Method 'RSource.create_loader' missing type hints

### src/haive/core/engine/document/loaders/specific/web_advanced.py

- 🔵 **Line 55**: Method 'HuggingFaceSource.requires_authentication' missing type hints
- 🔵 **Line 59**: Method 'HuggingFaceSource.get_credential_requirements' missing type hints
- 🔵 **Line 63**: Method 'HuggingFaceSource.create_loader' missing type hints
- 🔵 **Line 134**: Method 'PubMedSource.create_loader' missing type hints
- 🔵 **Line 179**: Method 'RSSFeedSource.create_loader' missing type hints
- 🔵 **Line 230**: Method 'NewsURLSource.create_loader' missing type hints
- 🔵 **Line 270**: Method 'SeleniumWebSource.create_loader' missing type hints
- 🔵 **Line 319**: Method 'RecursiveURLSource.create_loader' missing type hints
- 🔵 **Line 361**: Method 'SitemapSource.create_loader' missing type hints

### src/haive/core/engine/document/loaders/specific/web_social.py

- 🔵 **Line 56**: Method 'RedditSource.create_loader' missing type hints
- 🔵 **Line 105**: Method 'HackerNewsSource.create_loader' missing type hints
- 🔵 **Line 155**: Method 'TwitterSource.create_loader' missing type hints
- 🔵 **Line 218**: Method 'DiscordSource.create_loader' missing type hints
- 🔵 **Line 264**: Method 'MastodonSource.create_loader' missing type hints
- 🔵 **Line 295**: Method 'WhatsAppSource.create_loader' missing type hints
- 🔵 **Line 317**: Method 'FacebookChatSource.create_loader' missing type hints
- 🔵 **Line 345**: Method 'IFixitSource.create_loader' missing type hints
- 🔵 **Line 370**: Method 'IMSDbSource.create_loader' missing type hints
- 🔵 **Line 402**: Method 'BiliBiliSource.create_loader' missing type hints

### src/haive/core/engine/document/loaders/specific/file_advanced.py

- 🔵 **Line 30**: Method 'BibtexSource.create_loader' missing type hints
- 🔵 **Line 59**: Method 'ReStructuredTextSource.create_loader' missing type hints
- 🔵 **Line 90**: Method 'TSVSource.create_loader' missing type hints
- 🔵 **Line 112**: Method 'OrgModeSource.create_loader' missing type hints
- 🔵 **Line 138**: Method 'MHTMLSource.create_loader' missing type hints
- 🔵 **Line 169**: Method 'VisioSource.create_loader' missing type hints
- 🔵 **Line 201**: Method 'SubtitleSource.create_loader' missing type hints
- 🔵 **Line 237**: Method 'JupyterNotebookSource.create_loader' missing type hints
- 🔵 **Line 267**: Method 'PythonCodeSource.create_loader' missing type hints

### src/haive/core/engine/document/loaders/specific/cloud.py

- 🔵 **Line 54**: Method 'S3Source.requires_authentication' missing type hints
- 🔵 **Line 58**: Method 'S3Source.get_credential_requirements' missing type hints
- 🔵 **Line 62**: Method 'S3Source.create_loader' missing type hints
- 🔵 **Line 142**: Method 'GCSSource.requires_authentication' missing type hints
- 🔵 **Line 146**: Method 'GCSSource.get_credential_requirements' missing type hints
- 🔵 **Line 150**: Method 'GCSSource.create_loader' missing type hints
- 🔵 **Line 230**: Method 'AzureBlobSource.requires_authentication' missing type hints
- 🔵 **Line 234**: Method 'AzureBlobSource.get_credential_requirements' missing type hints
- 🔵 **Line 238**: Method 'AzureBlobSource.create_loader' missing type hints
- 🔵 **Line 1**: Function 'AzureBlobSource.**init**' parameter 'account_name' name doesn't match type hint

### src/haive/core/engine/document/loaders/specific/database_advanced.py

- 🔵 **Line 63**: Method 'BigQuerySource.requires_authentication' missing type hints
- 🔵 **Line 67**: Method 'BigQuerySource.get_credential_requirements' missing type hints
- 🔵 **Line 71**: Method 'BigQuerySource.create_loader' missing type hints
- 🔵 **Line 107**: Method 'BigQuerySource.analyze_schema' missing type hints
- 🔵 **Line 211**: Method 'SQLiteSource.create_loader' missing type hints
- 🔵 **Line 279**: Method 'MySQLSource.requires_authentication' missing type hints
- 🔵 **Line 283**: Method 'MySQLSource.get_credential_requirements' missing type hints
- 🔵 **Line 287**: Method 'MySQLSource.create_loader' missing type hints

### src/haive/core/engine/document/loaders/specific/web_github_enhanced.py

- 🔵 **Line 44**: Method 'GitHubDiscussionsSource.create_loader' missing type hints
- 🔵 **Line 93**: Method 'GitHubGistsSource.create_loader' missing type hints
- 🔵 **Line 141**: Method 'GitHubReleasesSource.create_loader' missing type hints
- 🔵 **Line 189**: Method 'GitHubActionsSource.create_loader' missing type hints
- 🔵 **Line 232**: Method 'GitHubWikiSource.create_loader' missing type hints
- 🔵 **Line 291**: Method 'GitHubDiscussionsLoader.load' missing type hints
- 🔵 **Line 419**: Method 'GitHubGistsLoader.load' missing type hints
- 🔵 **Line 518**: Method 'GitHubReleasesLoader.load' missing type hints
- 🔵 **Line 609**: Method 'GitHubActionsLoader.load' missing type hints
- 🔵 **Line 700**: Method 'GitHubWikiLoader.load' missing type hints

### src/haive/core/engine/document/loaders/specific/files_text.py

- 🔵 **Line 27**: Method 'TextFileSource.create_loader' missing type hints
- 🔵 **Line 51**: Method 'MarkdownSource.create_loader' missing type hints
- 🔵 **Line 81**: Method 'ReStructuredTextSource.create_loader' missing type hints
- 🔵 **Line 107**: Method 'LaTeXSource.create_loader' missing type hints
- 🔵 **Line 136**: Method 'OrgModeSource.create_loader' missing type hints
- 🔵 **Line 164**: Method 'AsciiDocSource.create_loader' missing type hints

### src/haive/core/engine/document/loaders/specific/services.py

- 🔵 **Line 48**: Method 'NotionSource.requires_authentication' missing type hints
- 🔵 **Line 52**: Method 'NotionSource.get_credential_requirements' missing type hints
- 🔵 **Line 56**: Method 'NotionSource.create_loader' missing type hints
- 🔵 **Line 122**: Method 'ObsidianSource.create_loader' missing type hints
- 🔵 **Line 165**: Method 'SlackSource.requires_authentication' missing type hints
- 🔵 **Line 169**: Method 'SlackSource.get_credential_requirements' missing type hints
- 🔵 **Line 173**: Method 'SlackSource.create_loader' missing type hints
- 🔵 **Line 219**: Method 'GutenbergSource.create_loader' missing type hints
- 🔵 **Line 266**: Method 'ConfluenceSource.requires_authentication' missing type hints
- 🔵 **Line 270**: Method 'ConfluenceSource.get_credential_requirements' missing type hints
- 🔵 **Line 274**: Method 'ConfluenceSource.create_loader' missing type hints
- 🔵 **Line 337**: Method 'ReadTheDocsSource.create_loader' missing type hints

### src/haive/core/engine/document/loaders/specific/database.py

- 🔵 **Line 53**: Method 'MongoDBSource.requires_authentication' missing type hints
- 🔵 **Line 57**: Method 'MongoDBSource.get_credential_requirements' missing type hints
- 🔵 **Line 61**: Method 'MongoDBSource.create_loader' missing type hints
- 🔵 **Line 141**: Method 'PostgreSQLSource.requires_authentication' missing type hints
- 🔵 **Line 145**: Method 'PostgreSQLSource.get_credential_requirements' missing type hints
- 🔵 **Line 149**: Method 'PostgreSQLSource.create_loader' missing type hints

### src/haive/core/engine/document/loaders/specific/web_api.py

- 🔵 **Line 41**: Method 'BraveSearchSource.create_loader' missing type hints
- 🔵 **Line 82**: Method 'GoogleSearchSource.create_loader' missing type hints
- 🔵 **Line 121**: Method 'ApifyDatasetSource.create_loader' missing type hints
- 🔵 **Line 159**: Method 'DiffbotSource.create_loader' missing type hints
- 🔵 **Line 203**: Method 'ScrapingBeeSource.create_loader' missing type hints
- 🔵 **Line 244**: Method 'ScrapflySource.create_loader' missing type hints
- 🔵 **Line 299**: Method 'NewsAPISource.create_loader' missing type hints
- 🔵 **Line 347**: Method 'AssemblyAITranscriptSource.create_loader' missing type hints
- 🔵 **Line 407**: Method 'EtherscanSource.create_loader' missing type hints
- 🔵 **Line 460**: Method 'ScrapingBeeLoader.load' missing type hints
- 🔵 **Line 1**: Function 'BraveSearchSource.**init**' parameter 'country' name doesn't match type hint

### src/haive/core/engine/document/loaders/specific/files_office.py

- 🔵 **Line 30**: Method 'WordDocumentSource.create_loader' missing type hints
- 🔵 **Line 71**: Method 'ExcelSource.create_loader' missing type hints
- 🔵 **Line 99**: Method 'PowerPointSource.create_loader' missing type hints
- 🔵 **Line 125**: Method 'OpenDocumentTextSource.create_loader' missing type hints
- 🔵 **Line 151**: Method 'VisioSource.create_loader' missing type hints
- 🔵 **Line 179**: Method 'RTFSource.create_loader' missing type hints

### src/haive/core/engine/document/loaders/specific/web.py

- 🔵 **Line 54**: Method 'GitHubSource.requires_authentication' missing type hints
- 🔵 **Line 58**: Method 'GitHubSource.get_credential_requirements' missing type hints
- 🔵 **Line 62**: Method 'GitHubSource.create_loader' missing type hints
- 🔵 **Line 150**: Method 'ArXivSource.create_loader' missing type hints
- 🔵 **Line 206**: Method 'WikipediaSource.create_loader' missing type hints
- 🔵 **Line 260**: Method 'PlaywrightWebSource.create_loader' missing type hints
- 🔵 **Line 309**: Method 'BasicWebSource.create_loader' missing type hints

### src/haive/core/engine/document/loaders/specific/files_code.py

- 🔵 **Line 27**: Method 'PythonCodeSource.create_loader' missing type hints
- 🔵 **Line 63**: Method 'JupyterNotebookSource.create_loader' missing type hints
- 🔵 **Line 95**: Method 'JavaScriptSource.create_loader' missing type hints
- 🔵 **Line 117**: Method 'CppSource.create_loader' missing type hints
- 🔵 **Line 135**: Method 'JavaSource.create_loader' missing type hints
- 🔵 **Line 153**: Method 'GoSource.create_loader' missing type hints
- 🔵 **Line 171**: Method 'RustSource.create_loader' missing type hints
- 🔵 **Line 189**: Method 'RubySource.create_loader' missing type hints
- 🔵 **Line 211**: Method 'ShellScriptSource.create_loader' missing type hints

### src/haive/core/engine/document/loaders/specific/files_data.py

- 🔵 **Line 27**: Method 'CSVSource.create_loader' missing type hints
- 🔵 **Line 56**: Method 'TSVSource.create_loader' missing type hints
- 🔵 **Line 81**: Method 'JSONSource.create_loader' missing type hints
- 🔵 **Line 106**: Method 'XMLSource.create_loader' missing type hints
- 🔵 **Line 132**: Method 'YAMLSource.create_loader' missing type hints
- 🔵 **Line 161**: Method 'TOMLSource.create_loader' missing type hints

### src/haive/core/engine/document/loaders/specific/files_media.py

- 🔵 **Line 32**: Method 'PDFSource.create_loader' missing type hints
- 🔵 **Line 84**: Method 'ImageSource.create_loader' missing type hints
- 🔵 **Line 117**: Method 'SubtitleSource.create_loader' missing type hints
- 🔵 **Line 145**: Method 'EPubSource.create_loader' missing type hints
- 🔵 **Line 171**: Method 'MHTMLSource.create_loader' missing type hints
- 🔵 **Line 202**: Method 'HTMLSource.create_loader' missing type hints
- 🔵 **Line 231**: Method 'CHMSource.create_loader' missing type hints

### src/haive/core/engine/document/loaders/sources/chat_gpt_loader.py

- 🔴 **Line 1**: Could not parse file: expected ':' (<unknown>, line 3)

### src/haive/core/engine/document/loaders/sources/implementation.py

- 🔵 **Line 115**: Method 'EnhancedSource.requires_authentication' missing type hints
- 🔵 **Line 119**: Method 'EnhancedSource.get_credential_requirements' missing type hints
- 🔵 **Line 229**: Method 'DatabaseSource.requires_authentication' missing type hints
- 🔵 **Line 233**: Method 'DatabaseSource.get_credential_requirements' missing type hints
- 🔵 **Line 260**: Method 'CloudStorageSource.requires_authentication' missing type hints
- 🔵 **Line 264**: Method 'CloudStorageSource.get_credential_requirements' missing type hints
- 🔵 **Line 302**: Method 'SourceRegistry.register' missing type hints
- 🟡 **Line 60**: Class 'Config' missing docstring
- 🟡 **Line 102**: Class 'Config' missing docstring

### src/haive/core/engine/document/loaders/sources/file_sources.py

- 🔵 **Line 54**: Method 'UnstructuredFileSource.get_loader_kwargs' missing docstring
- 🔵 **Line 54**: Method 'UnstructuredFileSource.get_loader_kwargs' missing type hints
- 🔵 **Line 93**: Method 'GenericFileSource.get_loader_kwargs' missing docstring
- 🔵 **Line 93**: Method 'GenericFileSource.get_loader_kwargs' missing type hints
- 🔵 **Line 135**: Method 'PythonCodeSource.get_loader_kwargs' missing docstring
- 🔵 **Line 135**: Method 'PythonCodeSource.get_loader_kwargs' missing type hints
- 🔵 **Line 167**: Method 'NotebookSource.get_loader_kwargs' missing docstring
- 🔵 **Line 167**: Method 'NotebookSource.get_loader_kwargs' missing type hints
- 🔵 **Line 203**: Method 'PowerPointSource.get_loader_kwargs' missing docstring
- 🔵 **Line 203**: Method 'PowerPointSource.get_loader_kwargs' missing type hints
- 🔵 **Line 230**: Method 'ODTDocumentSource.get_loader_kwargs' missing docstring
- 🔵 **Line 230**: Method 'ODTDocumentSource.get_loader_kwargs' missing type hints
- 🔵 **Line 257**: Method 'RTFDocumentSource.get_loader_kwargs' missing docstring
- 🔵 **Line 257**: Method 'RTFDocumentSource.get_loader_kwargs' missing type hints
- 🔵 **Line 297**: Method 'EmailSource.get_loader_kwargs' missing docstring
- 🔵 **Line 297**: Method 'EmailSource.get_loader_kwargs' missing type hints
- 🔵 **Line 332**: Method 'EPubSource.get_loader_kwargs' missing docstring
- 🔵 **Line 332**: Method 'EPubSource.get_loader_kwargs' missing type hints
- 🔵 **Line 363**: Method 'CHMHelpSource.get_loader_kwargs' missing docstring
- 🔵 **Line 363**: Method 'CHMHelpSource.get_loader_kwargs' missing type hints
- 🔵 **Line 393**: Method 'TOMLConfigSource.get_loader_kwargs' missing docstring
- 🔵 **Line 393**: Method 'TOMLConfigSource.get_loader_kwargs' missing type hints
- 🔵 **Line 426**: Method 'YAMLConfigSource.get_loader_kwargs' missing docstring
- 🔵 **Line 426**: Method 'YAMLConfigSource.get_loader_kwargs' missing type hints
- 🔵 **Line 454**: Method 'XMLDataSource.get_loader_kwargs' missing docstring
- 🔵 **Line 454**: Method 'XMLDataSource.get_loader_kwargs' missing type hints
- 🔵 **Line 491**: Method 'SubtitleSource.get_loader_kwargs' missing docstring
- 🔵 **Line 491**: Method 'SubtitleSource.get_loader_kwargs' missing type hints
- 🔵 **Line 525**: Method 'PDFDirectorySource.get_loader_kwargs' missing docstring
- 🔵 **Line 525**: Method 'PDFDirectorySource.get_loader_kwargs' missing type hints
- 🔵 **Line 558**: Method 'UnstructuredDirectorySource.get_loader_kwargs' missing docstring
- 🔵 **Line 558**: Method 'UnstructuredDirectorySource.get_loader_kwargs' missing type hints
- 🔵 **Line 602**: Method 'ImageDocumentSource.get_loader_kwargs' missing docstring
- 🔵 **Line 602**: Method 'ImageDocumentSource.get_loader_kwargs' missing type hints
- 🔵 **Line 638**: Method 'BibtexSource.get_loader_kwargs' missing docstring
- 🔵 **Line 638**: Method 'BibtexSource.get_loader_kwargs' missing type hints
- 🔵 **Line 664**: Method 'CoNLLULinguisticSource.get_loader_kwargs' missing docstring
- 🔵 **Line 664**: Method 'CoNLLULinguisticSource.get_loader_kwargs' missing type hints
- 🔵 **Line 672**: Function 'get_file_sources_statistics' missing type hints
- 🔵 **Line 712**: Function 'validate_file_sources' missing type hints

### src/haive/core/engine/document/loaders/sources/enhanced_registry.py

- 🔵 **Line 245**: Method 'EnhancedSourceRegistry.find_bulk_loaders' missing type hints
- 🔵 **Line 249**: Method 'EnhancedSourceRegistry.find_recursive_loaders' missing type hints
- 🔵 **Line 265**: Method 'EnhancedSourceRegistry.get_statistics' missing type hints
- 🟡 **Line 402**: Function 'decorator' missing docstring

### src/haive/core/engine/document/loaders/sources/registry.py

- 🔵 **Line 310**: Method 'SourceRegistry.list_sources' missing type hints
- 🟡 **Line 369**: Function 'decorator' missing docstring

### src/haive/core/engine/document/loaders/sources/source_types.py

- 🔵 **Line 121**: Method 'BaseSource.get_loader_kwargs' missing type hints
- 🔵 **Line 141**: Method 'LocalFileSource.get_loader_kwargs' missing docstring
- 🔵 **Line 141**: Method 'LocalFileSource.get_loader_kwargs' missing type hints
- 🔵 **Line 166**: Method 'RemoteSource.get_loader_kwargs' missing docstring
- 🔵 **Line 166**: Method 'RemoteSource.get_loader_kwargs' missing type hints
- 🔵 **Line 178**: Method 'RemoteSource.get_auth_headers' missing type hints
- 🔵 **Line 200**: Method 'DatabaseSource.get_loader_kwargs' missing docstring
- 🔵 **Line 200**: Method 'DatabaseSource.get_loader_kwargs' missing type hints
- 🔵 **Line 227**: Method 'CloudStorageSource.get_loader_kwargs' missing docstring
- 🔵 **Line 227**: Method 'CloudStorageSource.get_loader_kwargs' missing type hints
- 🔵 **Line 244**: Method 'DirectorySource.get_loader_kwargs' missing docstring
- 🔵 **Line 244**: Method 'DirectorySource.get_loader_kwargs' missing type hints
- 🔵 **Line 269**: Method 'MessagingSource.get_loader_kwargs' missing docstring
- 🔵 **Line 269**: Method 'MessagingSource.get_loader_kwargs' missing type hints
- 🔵 **Line 296**: Method 'BusinessSource.get_loader_kwargs' missing docstring
- 🔵 **Line 296**: Method 'BusinessSource.get_loader_kwargs' missing type hints
- 🔵 **Line 313**: Method 'AcademicSource.get_loader_kwargs' missing docstring
- 🔵 **Line 313**: Method 'AcademicSource.get_loader_kwargs' missing type hints
- 🔵 **Line 338**: Method 'MediaSource.get_loader_kwargs' missing docstring
- 🔵 **Line 338**: Method 'MediaSource.get_loader_kwargs' missing type hints
- 🔵 **Line 367**: Method 'KnowledgeSource.get_loader_kwargs' missing docstring
- 🔵 **Line 367**: Method 'KnowledgeSource.get_loader_kwargs' missing type hints
- 🔵 **Line 392**: Method 'DevelopmentSource.get_loader_kwargs' missing docstring
- 🔵 **Line 392**: Method 'DevelopmentSource.get_loader_kwargs' missing type hints
- 🔵 **Line 413**: Method 'PDFSource.get_loader_kwargs' missing docstring
- 🔵 **Line 413**: Method 'PDFSource.get_loader_kwargs' missing type hints
- 🔵 **Line 432**: Method 'WebScrapingSource.get_loader_kwargs' missing docstring
- 🔵 **Line 432**: Method 'WebScrapingSource.get_loader_kwargs' missing type hints
- 🔵 **Line 450**: Method 'DatabaseQuerySource.get_loader_kwargs' missing docstring
- 🔵 **Line 450**: Method 'DatabaseQuerySource.get_loader_kwargs' missing type hints
- 🔵 **Line 467**: Method 'BulkDirectorySource.get_loader_kwargs' missing docstring
- 🔵 **Line 467**: Method 'BulkDirectorySource.get_loader_kwargs' missing type hints
- 🟡 **Line 117**: Class 'Config' missing docstring
- 🟡 **Line 163**: Class 'Config' missing docstring
- 🟡 **Line 197**: Class 'Config' missing docstring
- 🟡 **Line 224**: Class 'Config' missing docstring
- 🟡 **Line 266**: Class 'Config' missing docstring
- 🟡 **Line 293**: Class 'Config' missing docstring
- 🟡 **Line 335**: Class 'Config' missing docstring
- 🟡 **Line 364**: Class 'Config' missing docstring
- 🟡 **Line 389**: Class 'Config' missing docstring

### src/haive/core/engine/document/loaders/sources/essential_sources.py

- 🔵 **Line 62**: Method 'PDFSource.get_loader_kwargs' missing docstring
- 🔵 **Line 62**: Method 'PDFSource.get_loader_kwargs' missing type hints
- 🔵 **Line 101**: Method 'CSVSource.get_loader_kwargs' missing docstring
- 🔵 **Line 101**: Method 'CSVSource.get_loader_kwargs' missing type hints
- 🔵 **Line 134**: Method 'JSONSource.get_loader_kwargs' missing docstring
- 🔵 **Line 134**: Method 'JSONSource.get_loader_kwargs' missing type hints
- 🔵 **Line 162**: Method 'TextSource.get_loader_kwargs' missing docstring
- 🔵 **Line 162**: Method 'TextSource.get_loader_kwargs' missing type hints
- 🔵 **Line 189**: Method 'MarkdownSource.get_loader_kwargs' missing docstring
- 🔵 **Line 189**: Method 'MarkdownSource.get_loader_kwargs' missing type hints
- 🔵 **Line 223**: Method 'WordDocumentSource.get_loader_kwargs' missing docstring
- 🔵 **Line 223**: Method 'WordDocumentSource.get_loader_kwargs' missing type hints
- 🔵 **Line 250**: Method 'ExcelSource.get_loader_kwargs' missing docstring
- 🔵 **Line 250**: Method 'ExcelSource.get_loader_kwargs' missing type hints
- 🔵 **Line 284**: Method 'HTMLSource.get_loader_kwargs' missing docstring
- 🔵 **Line 284**: Method 'HTMLSource.get_loader_kwargs' missing type hints
- 🔵 **Line 330**: Method 'WebPageSource.get_loader_kwargs' missing docstring
- 🔵 **Line 330**: Method 'WebPageSource.get_loader_kwargs' missing type hints
- 🔵 **Line 364**: Method 'GitHubSource.get_loader_kwargs' missing docstring
- 🔵 **Line 364**: Method 'GitHubSource.get_loader_kwargs' missing type hints
- 🔵 **Line 401**: Method 'LocalDirectorySource.get_loader_kwargs' missing docstring
- 🔵 **Line 401**: Method 'LocalDirectorySource.get_loader_kwargs' missing type hints
- 🔵 **Line 435**: Method 'PostgreSQLSource.get_loader_kwargs' missing docstring
- 🔵 **Line 435**: Method 'PostgreSQLSource.get_loader_kwargs' missing type hints
- 🔵 **Line 462**: Method 'MongoDBSource.get_loader_kwargs' missing docstring
- 🔵 **Line 462**: Method 'MongoDBSource.get_loader_kwargs' missing type hints
- 🔵 **Line 475**: Function 'get_essential_sources_statistics' missing type hints
- 🔵 **Line 498**: Function 'validate_essential_sources' missing type hints

### src/haive/core/engine/document/loaders/sources/groups.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 4**: Class 'SourceGroups' missing docstring

### src/haive/core/engine/document/loaders/sources/source_base.py

- 🔵 **Line 37**: Method 'BaseSource.validate_source' missing type hints
- 🔵 **Line 46**: Method 'BaseSource.get_loader_kwargs' missing type hints
- 🔵 **Line 54**: Method 'BaseSource.to_dict' missing type hints
- 🔵 **Line 69**: Method 'LocalSource.validate_source' missing type hints
- 🔵 **Line 78**: Method 'LocalSource.get_loader_kwargs' missing type hints
- 🔵 **Line 99**: Method 'DirectorySource.validate_source' missing type hints
- 🔵 **Line 108**: Method 'DirectorySource.get_loader_kwargs' missing type hints
- 🔵 **Line 139**: Method 'RemoteSource.validate_source' missing type hints
- 🔵 **Line 148**: Method 'RemoteSource.get_loader_kwargs' missing type hints
- 🔵 **Line 195**: Method 'DatabaseSource.validate_source' missing type hints
- 🔵 **Line 201**: Method 'DatabaseSource.get_loader_kwargs' missing type hints
- 🔵 **Line 253**: Method 'CloudSource.get_loader_kwargs' missing type hints

### src/haive/core/engine/document/loaders/sources/types.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/bulk_sources.py

- 🔵 **Line 92**: Method 'RecursiveDirectorySource.get_loader_kwargs' missing docstring
- 🔵 **Line 92**: Method 'RecursiveDirectorySource.get_loader_kwargs' missing type hints
- 🔵 **Line 151**: Method 'FilteredDirectorySource.get_loader_kwargs' missing docstring
- 🔵 **Line 151**: Method 'FilteredDirectorySource.get_loader_kwargs' missing type hints
- 🔵 **Line 208**: Method 'S3BucketSource.get_loader_kwargs' missing docstring
- 🔵 **Line 208**: Method 'S3BucketSource.get_loader_kwargs' missing type hints
- 🔵 **Line 251**: Method 'GCSBucketSource.get_loader_kwargs' missing docstring
- 🔵 **Line 251**: Method 'GCSBucketSource.get_loader_kwargs' missing type hints
- 🔵 **Line 293**: Method 'AzureContainerSource.get_loader_kwargs' missing docstring
- 🔵 **Line 293**: Method 'AzureContainerSource.get_loader_kwargs' missing type hints
- 🔵 **Line 340**: Method 'MergedDataSource.get_loader_kwargs' missing docstring
- 🔵 **Line 340**: Method 'MergedDataSource.get_loader_kwargs' missing type hints
- 🔵 **Line 390**: Method 'FileSystemBlobSource.get_loader_kwargs' missing docstring
- 🔵 **Line 390**: Method 'FileSystemBlobSource.get_loader_kwargs' missing type hints
- 🔵 **Line 434**: Method 'CloudBlobSource.get_loader_kwargs' missing docstring
- 🔵 **Line 434**: Method 'CloudBlobSource.get_loader_kwargs' missing type hints
- 🔵 **Line 483**: Method 'StreamingDirectorySource.get_loader_kwargs' missing docstring
- 🔵 **Line 483**: Method 'StreamingDirectorySource.get_loader_kwargs' missing type hints
- 🔵 **Line 497**: Function 'get_bulk_sources_statistics' missing type hints
- 🔵 **Line 532**: Function 'get_scrape_all_sources' missing type hints
- 🔵 **Line 548**: Function 'validate_bulk_sources' missing type hints

### src/haive/core/engine/document/loaders/utils/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/engine/document/loaders/sources/remote/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 19**: Method 'URLSource.validate_url' missing docstring
- 🔵 **Line 19**: Method 'URLSource.validate_url' missing type hints
- 🔵 **Line 25**: Method 'URLSource.source' missing type hints
- 🔵 **Line 41**: Method 'URLSource.validate_url' missing docstring
- 🔵 **Line 41**: Method 'URLSource.validate_url' missing type hints

### src/haive/core/engine/document/loaders/sources/remote/blackboard_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/remote/youtube_audio_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/remote/ifixit_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/remote/college_confidential.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/remote/wikipedia_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/remote/imsdb_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/remote/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition
- 🔵 **Line 20**: Method 'RemoteSource.validate_url' missing docstring
- 🔵 **Line 20**: Method 'RemoteSource.validate_url' missing type hints
- 🔵 **Line 26**: Method 'RemoteSource.source' missing docstring
- 🔵 **Line 26**: Method 'RemoteSource.source' missing type hints
- 🔵 **Line 30**: Method 'RemoteSource.from_url' missing docstring

### src/haive/core/engine/document/loaders/sources/remote/bilibili_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/remote/youtube_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/remote/hacker_news_source.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 16**: Method 'HackerNewsSource.validate_url' missing docstring
- 🔵 **Line 16**: Method 'HackerNewsSource.validate_url' missing type hints

### src/haive/core/engine/document/loaders/sources/remote/arxiv_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/remote/az_lyrics_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/remote/read_the_docs_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/remote/diffbot_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/base/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 41**: Method 'BaseSource.source' missing type hints
- 🔵 **Line 50**: Method 'BaseSource.source_class' missing type hints

### src/haive/core/engine/document/loaders/sources/base/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/engine/document/loaders/sources/chat/base.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/chat/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/engine/document/loaders/sources/database/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/engine/document/loaders/sources/database/types.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 4**: Class 'DatabaseSourceType' missing docstring

### src/haive/core/engine/document/loaders/sources/local/json_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/yaml_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 24**: Method 'LocalSource.validate_file_path' missing docstring
- 🔵 **Line 24**: Method 'LocalSource.validate_file_path' missing type hints
- 🔵 **Line 30**: Method 'LocalSource.convert_to_path' missing docstring
- 🔵 **Line 30**: Method 'LocalSource.convert_to_path' missing type hints
- 🔵 **Line 36**: Method 'LocalSource.is_file' missing docstring
- 🔵 **Line 36**: Method 'LocalSource.is_file' missing type hints
- 🔵 **Line 42**: Method 'LocalSource.source' missing docstring
- 🔵 **Line 42**: Method 'LocalSource.source' missing type hints
- 🔵 **Line 46**: Method 'LocalSource.from_file_path' missing docstring
- 🔵 **Line 50**: Method 'LocalSource.is_file' missing docstring
- 🔵 **Line 50**: Method 'LocalSource.is_file' missing type hints
- 🔵 **Line 54**: Method 'LocalSource.is_directory' missing docstring
- 🔵 **Line 54**: Method 'LocalSource.is_directory' missing type hints
- 🔵 **Line 67**: Method 'FileSource.validate_file_path' missing docstring
- 🔵 **Line 67**: Method 'FileSource.validate_file_path' missing type hints
- 🔵 **Line 73**: Method 'FileSource.convert_to_path' missing docstring
- 🔵 **Line 73**: Method 'FileSource.convert_to_path' missing type hints
- 🔵 **Line 79**: Method 'FileSource.validate_file_type' missing docstring
- 🔵 **Line 79**: Method 'FileSource.validate_file_type' missing type hints
- 🔵 **Line 85**: Method 'FileSource.file_type' missing docstring
- 🔵 **Line 85**: Method 'FileSource.file_type' missing type hints
- 🔵 **Line 89**: Method 'FileSource.file_name' missing docstring
- 🔵 **Line 89**: Method 'FileSource.file_name' missing type hints
- 🔵 **Line 93**: Method 'FileSource.file_size' missing docstring
- 🔵 **Line 93**: Method 'FileSource.file_size' missing type hints
- 🔵 **Line 97**: Method 'FileSource.source' missing docstring
- 🔵 **Line 97**: Method 'FileSource.source' missing type hints
- 🔵 **Line 111**: Method 'DirectorySource.validate_directory_path' missing docstring
- 🔵 **Line 111**: Method 'DirectorySource.validate_directory_path' missing type hints
- 🔵 **Line 117**: Method 'DirectorySource.from_directory_path' missing docstring
- 🔵 **Line 121**: Method 'DirectorySource.list_files' missing docstring
- 🔵 **Line 125**: Method 'DirectorySource.list_directories' missing docstring

### src/haive/core/engine/document/loaders/sources/local/rtf_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/docx_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/ppt_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/txt_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/srt_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/enex_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/git_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/mhtml_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/pdf.py

- 🔵 **Line 72**: Method 'PDFSource.get_loader_kwargs' missing type hints
- 🔵 **Line 94**: Method 'PDFSource.validate_source' missing type hints
- 🔵 **Line 140**: Method 'AcademicPDFSource.get_loader_kwargs' missing type hints

### src/haive/core/engine/document/loaders/sources/local/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/engine/document/loaders/sources/local/html_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/md_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/pdf_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/python_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/toml_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/csv_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/excel_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/types.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/notebook_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/bibtex_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/vsdx_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/xml_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/xlsx_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/rst_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/chm_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/odt_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/xls_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/markdown_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/epub_source.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/engine/document/loaders/sources/local/programming_languages/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/engine/vectorstore/providers/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/engine/retriever/providers/BedrockRetrieverConfig.py

- 🔵 **Line 136**: Method 'BedrockRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 142**: Method 'BedrockRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 153**: Method 'BedrockRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/TFIDFRetrieverConfig.py

- 🔵 **Line 95**: Method 'TFIDFRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 101**: Method 'TFIDFRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 112**: Method 'TFIDFRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/YouRetrieverConfig.py

- 🔵 **Line 123**: Method 'YouRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 129**: Method 'YouRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 140**: Method 'YouRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/GoogleDocumentAIWarehouseRetrieverConfig.py

- 🔵 **Line 134**: Method 'GoogleDocumentAIWarehouseRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 140**: Method 'GoogleDocumentAIWarehouseRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 151**: Method 'GoogleDocumentAIWarehouseRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/KNN.py

- 🔵 **Line 111**: Method 'KNNRetrieverConfig.validate_config' missing type hints
- 🔵 **Line 129**: Method 'KNNRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 150**: Method 'KNNRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 170**: Method 'KNNRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/MultiVectorRetriever.py

- 🔴 **Line 1**: Could not parse file: invalid syntax (<unknown>, line 4)

### src/haive/core/engine/retriever/providers/AzureAISearchRetrieverConfig.py

- 🔵 **Line 104**: Method 'AzureAISearchRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 110**: Method 'AzureAISearchRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 121**: Method 'AzureAISearchRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/ContextualCompressionRetrieverConfig.py

- 🔵 **Line 107**: Method 'ContextualCompressionRetrieverConfig.validate_config' missing type hints
- 🔵 **Line 119**: Method 'ContextualCompressionRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 129**: Method 'ContextualCompressionRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 140**: Method 'ContextualCompressionRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/MilvusRetrieverConfig.py

- 🔵 **Line 126**: Method 'MilvusRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 132**: Method 'MilvusRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 143**: Method 'MilvusRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/GoogleVertexAISearchRetrieverConfig.py

- 🔵 **Line 144**: Method 'GoogleVertexAISearchRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 150**: Method 'GoogleVertexAISearchRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 161**: Method 'GoogleVertexAISearchRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/PineconeHybridSearchRetrieverConfig.py

- 🔵 **Line 101**: Method 'PineconeHybridSearchRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 107**: Method 'PineconeHybridSearchRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 118**: Method 'PineconeHybridSearchRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/KNNRetrieverConfig.py

- 🔵 **Line 108**: Method 'KNNRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 114**: Method 'KNNRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 125**: Method 'KNNRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/SVMRetrieverConfig.py

- 🔵 **Line 125**: Method 'SVMRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 131**: Method 'SVMRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 142**: Method 'SVMRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/SelfQueryRetrieverConfig.py

- 🔵 **Line 128**: Method 'SelfQueryRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 138**: Method 'SelfQueryRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 149**: Method 'SelfQueryRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/WeaviateHybridSearchRetrieverConfig.py

- 🔵 **Line 146**: Method 'WeaviateHybridSearchRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 152**: Method 'WeaviateHybridSearchRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 163**: Method 'WeaviateHybridSearchRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/TimeWeightedRetriever.py

- 🔵 **Line 137**: Method 'TimeWeightedRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 156**: Method 'TimeWeightedRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 174**: Method 'TimeWeightedRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/ElasticsearchRetrieverConfig.py

- 🔵 **Line 147**: Method 'ElasticsearchRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 153**: Method 'ElasticsearchRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 164**: Method 'ElasticsearchRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/engine/retriever/providers/MergerRetrieverConfig.py

- 🔵 **Line 80**: Method 'MergerRetrieverConfig.validate_retrievers' missing type hints
- 🔵 **Line 86**: Method 'MergerRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 96**: Method 'MergerRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 107**: Method 'MergerRetrieverConfig.instantiate' missing type hints
- 🔵 **Line 160**: Method 'MergerRetrieverConfig.get_merger_info' missing type hints

### src/haive/core/engine/retriever/providers/TFIDFRetriever.py

- 🔵 **Line 103**: Method 'TFIDFRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 123**: Method 'TFIDFRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 141**: Method 'TFIDFRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/WikipediaRetrieverConfig.py

- 🔵 **Line 88**: Method 'WikipediaRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 94**: Method 'WikipediaRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 105**: Method 'WikipediaRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/TavilySearchAPIRetrieverConfig.py

- 🔵 **Line 105**: Method 'TavilySearchAPIRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 111**: Method 'TavilySearchAPIRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 122**: Method 'TavilySearchAPIRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/BM25.py

- 🔵 **Line 147**: Method 'BM25RetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 169**: Method 'BM25RetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 188**: Method 'BM25RetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/AmazonKnowledgeBasesRetrieverConfig.py

- 🔵 **Line 128**: Method 'AmazonKnowledgeBasesRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 134**: Method 'AmazonKnowledgeBasesRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 145**: Method 'AmazonKnowledgeBasesRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/AskNewsRetrieverConfig.py

- 🔵 **Line 134**: Method 'AskNewsRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 140**: Method 'AskNewsRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 151**: Method 'AskNewsRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/ZepRetrieverConfig.py

- 🔵 **Line 132**: Method 'ZepRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 138**: Method 'ZepRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 149**: Method 'ZepRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/MultiQueryRetrieverConfig.py

- 🔵 **Line 135**: Method 'MultiQueryRetrieverConfig.validate_config' missing type hints
- 🔵 **Line 143**: Method 'MultiQueryRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 153**: Method 'MultiQueryRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 164**: Method 'MultiQueryRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/ParentDocumentRetrieverConfig.py

- 🔵 **Line 99**: Method 'ParentDocumentRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 109**: Method 'ParentDocumentRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 120**: Method 'ParentDocumentRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/SVM.py

- 🔵 **Line 109**: Method 'SVMRetrieverConfig.validate_config' missing type hints
- 🔵 **Line 127**: Method 'SVMRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 147**: Method 'SVMRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 167**: Method 'SVMRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/VespaRetrieverConfig.py

- 🔵 **Line 135**: Method 'VespaRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 141**: Method 'VespaRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 152**: Method 'VespaRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/CohereRagRetrieverConfig.py

- 🔵 **Line 145**: Method 'CohereRagRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 151**: Method 'CohereRagRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 162**: Method 'CohereRagRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/QdrantSparseVectorRetrieverConfig.py

- 🔵 **Line 157**: Method 'QdrantSparseVectorRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 163**: Method 'QdrantSparseVectorRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 174**: Method 'QdrantSparseVectorRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/BM25RetrieverConfig.py

- 🔵 **Line 115**: Method 'BM25RetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 121**: Method 'BM25RetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 132**: Method 'BM25RetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/RePhraseQueryRetrieverConfig.py

- 🔵 **Line 137**: Method 'RePhraseQueryRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 155**: Method 'RePhraseQueryRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 173**: Method 'RePhraseQueryRetrieverConfig.validate_config' missing type hints
- 🔵 **Line 195**: Method 'RePhraseQueryRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/CohereRAGRetrieverConfig.py

- 🔵 **Line 100**: Method 'CohereRAGRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 106**: Method 'CohereRAGRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 117**: Method 'CohereRAGRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/KendraRetrieverConfig.py

- 🔵 **Line 132**: Method 'KendraRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 138**: Method 'KendraRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 149**: Method 'KendraRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/PubMedRetrieverConfig.py

- 🔵 **Line 124**: Method 'PubMedRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 130**: Method 'PubMedRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 141**: Method 'PubMedRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/ArxivRetrieverConfig.py

- 🔵 **Line 82**: Method 'ArxivRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 88**: Method 'ArxivRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 99**: Method 'ArxivRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/WebResearchRetrieverConfig.py

- 🔵 **Line 140**: Method 'WebResearchRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 146**: Method 'WebResearchRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 157**: Method 'WebResearchRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/retriever/providers/EnsembleRetriever.py

- 🔵 **Line 127**: Method 'EnsembleRetrieverConfig.validate_and_set_weights' missing type hints
- 🔵 **Line 152**: Method 'EnsembleRetrieverConfig.get_input_fields' missing type hints
- 🔵 **Line 172**: Method 'EnsembleRetrieverConfig.get_output_fields' missing type hints
- 🔵 **Line 192**: Method 'EnsembleRetrieverConfig.instantiate' missing type hints

### src/haive/core/engine/agent/persistence/integration.py

- 🔴 **Line 1**: Could not parse file: expected an indented block after 'if' statement on line 102 (<unknown>, line 103)

### src/haive/core/engine/agent/persistence/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 27**: Method 'CheckpointerConfig.create_checkpointer' missing type hints
- 🔵 **Line 46**: Method 'CheckpointerConfig.to_dict' missing type hints
- 🟡 **Line 24**: Class 'Config' missing docstring

### src/haive/core/engine/agent/persistence/factory.py

- 🔴 **Line 1**: Could not parse file: unexpected indent (<unknown>, line 61)

### src/haive/core/engine/agent/persistence/handlers.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 11**: Function 'process_input' missing type hints
- 🔵 **Line 179**: Function 'prepare_merged_input' missing type hints
- 🔵 **Line 278**: Function 'extract_output' missing type hints
- 🔵 **Line 1**: Function 'prepare_merged_input' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'extract_output' uses overly generic type 'Any' for parameter 'output_data'
- 🔵 **Line 1**: Function 'extract_state_snapshot' uses overly generic type 'Any' for parameter 'snapshot'

### src/haive/core/engine/agent/persistence/memory_config.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 19**: Method 'MemoryCheckpointerConfig.create_checkpointer' missing type hints

### src/haive/core/engine/agent/persistence/types.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 4**: Class 'CheckpointerType' missing docstring

### src/haive/core/engine/agent/persistence/postgres_config.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 61**: Method 'PostgresCheckpointerConfig.validate_postgres_available' missing type hints
- 🔵 **Line 70**: Method 'PostgresCheckpointerConfig.create_checkpointer' missing type hints
- 🔵 **Line 124**: Method 'PostgresCheckpointerConfig.close' missing type hints
- 🔵 **Line 137**: Method 'PostgresCheckpointerConfig.register_thread' missing type hints
- 🔵 **Line 1**: Function 'PostgresCheckpointerConfig.create_checkpointer' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'PostgresCheckpointerConfig.put_checkpoint' uses overly generic type 'Any' for parameter 'data'

### src/haive/core/engine/agent/persistence/manager.py

- 🔵 **Line 66**: Method 'PersistenceManager.get_checkpointer' missing type hints
- 🔵 **Line 208**: Method 'PersistenceManager.setup' missing type hints
- 🔵 **Line 236**: Method 'PersistenceManager.ensure_pool_open' missing type hints
- 🔵 **Line 275**: Method 'PersistenceManager.close_pool_if_needed' missing type hints
- 🔵 **Line 297**: Method 'PersistenceManager.register_thread' missing type hints
- 🔵 **Line 447**: Method 'PersistenceManager.create_runnable_config' missing type hints
- 🔵 **Line 488**: Method 'PersistenceManager.prepare_for_agent_run' missing type hints
- 🔵 **Line 530**: Method 'PersistenceManager.get_or_create_thread_id' missing type hints
- 🔵 **Line 547**: Method 'PersistenceManager.list_threads' missing type hints
- 🔵 **Line 703**: Method 'PersistenceManager.delete_thread' missing type hints
- 🔵 **Line 767**: Method 'PersistenceManager.from_config' missing type hints
- 🔵 **Line 812**: Method 'PersistenceManager.from_env' missing type hints

### src/haive/core/engine/agent/persistence/mongodb_config.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 34**: Method 'MongoDBCheckpointerConfig.create_checkpointer' missing type hints

### src/haive/core/engine/agent/utils/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/engine/agent/utils/state_handling.py

- 🔵 **Line 19**: Function 'extract_output' missing type hints
- 🔵 **Line 100**: Function 'prepare_merged_input' missing type hints
- 🔵 **Line 184**: Function 'process_input' missing type hints
- 🔵 **Line 1**: Function 'extract_output' uses overly generic type 'Any' for parameter 'output_data'
- 🔵 **Line 1**: Function 'extract_state_snapshot' uses overly generic type 'Any' for parameter 'snapshot'
- 🔵 **Line 1**: Function 'prepare_merged_input' uses overly generic type 'Any' for parameter 'input_data'
- 🔵 **Line 1**: Function 'prepare_merged_input' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'save_state_history' uses overly generic type 'Any' for parameter 'app'

### src/haive/core/engine/agent/utils/input_handling.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 1**: Function 'prepare_merged_input' returns overly generic type 'Any'

### src/haive/core/schema/prebuilt/messages_state.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 128**: Method 'MessagesState.get_last_message' missing type hints
- 🔵 **Line 162**: Method 'MessagesState.get_system_message' missing type hints
- 🔵 **Line 169**: Method 'MessagesState.get_filtered_messages' missing type hints
- 🔵 **Line 197**: Method 'MessagesState.get_last_human_message' missing type hints
- 🔵 **Line 202**: Method 'MessagesState.get_last_ai_message' missing type hints
- 🔵 **Line 207**: Method 'MessagesState.get_last_tool_message' missing type hints
- 🔵 **Line 214**: Method 'MessagesState.is_last_message_from_ai' missing type hints
- 🔵 **Line 219**: Method 'MessagesState.is_last_message_from_human' missing type hints
- 🔵 **Line 224**: Method 'MessagesState.is_last_message_from_tool' missing type hints
- 🔵 **Line 231**: Method 'MessagesState.has_tool_calls' missing type hints
- 🔵 **Line 330**: Method 'MessagesState.decide_next_node' missing type hints
- 🔵 **Line 366**: Method 'MessagesState.to_openai_format' missing type hints
- 🔵 **Line 370**: Method 'MessagesState.to_langchain_prompt' missing type hints
- 🔵 **Line 397**: Method 'MessagesState.get_conversation_rounds' missing type hints
- 🔵 **Line 415**: Method 'MessagesState.deduplicate_tool_calls' missing type hints
- 🔵 **Line 433**: Method 'MessagesState.get_completed_tool_calls' missing type hints
- 🔵 **Line 1**: Function 'MessagesState.validate_message_format' uses overly generic type 'Any' for parameter 'data'
- 🔵 **Line 1**: Function 'MessagesState.validate_message_format' returns overly generic type 'Any'

### src/haive/core/schema/prebuilt/tool_state.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 85**: Method 'ToolState.sync_tools_and_update_routes' missing type hints
- 🔵 **Line 330**: Method 'ToolState.tool_types' missing type hints
- 🔵 **Line 654**: Method 'ToolState.refresh_tool_routes' missing type hints
- 🔵 **Line 660**: Method 'ToolState.update_tool_types' missing type hints
- 🔵 **Line 1**: Function 'ToolState.\_sync_tools_from_class_engines' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'ToolState.\_sync_tools_to_engine_by_route' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'ToolState.\_sync_tools_to_engine_by_route' uses overly generic type 'Any' for parameter 'engine_type'
- 🔵 **Line 1**: Function 'ToolState.\_should_sync_tool_to_engine' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'ToolState.\_get_tool_name' uses overly generic type 'Any' for parameter 'tool'
- 🔵 **Line 1**: Function 'ToolState.\_get_tool_route' uses overly generic type 'Any' for parameter 'tool'
- 🔵 **Line 1**: Function 'ToolState.\_is_basemodel_subclass' uses overly generic type 'Any' for parameter 'tool'
- 🔵 **Line 1**: Function 'ToolState.add_tool' uses overly generic type 'Any' for parameter 'tool'
- 🔵 **Line 1**: Function 'ToolState.add_tool_to_engine' uses overly generic type 'Any' for parameter 'tool'
- 🔵 **Line 1**: Function 'ToolState.\_sync_tool_to_specific_engine' uses overly generic type 'Any' for parameter 'tool'
- 🔵 **Line 1**: Function 'ToolState.\_sync_tool_to_specific_engine' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'ToolState.\_sync_single_tool_to_engines' uses overly generic type 'Any' for parameter 'tool'
- 🔵 **Line 1**: Function 'ToolState.remove_tool' uses overly generic type 'Any' for parameter 'tool'
- 🔵 **Line 1**: Function 'ToolState.\_remove_tool_from_engines' uses overly generic type 'Any' for parameter 'tool'

### src/haive/core/schema/compatibility/validators.py

- 🔵 **Line 38**: Method 'ValidationContext.pop_path' missing type hints
- 🔵 **Line 43**: Method 'ValidationContext.current_path_str' missing type hints
- 🔵 **Line 62**: Method 'Validator.supports_async' missing type hints
- 🔵 **Line 348**: Method 'ValidatorBuilder.combine' missing type hints
- 🔵 **Line 1**: Function 'Validator.validate' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'FieldValidator.validate' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'ModelValidator.add_field_validator' parameter 'validator' name doesn't match type hint
- 🔵 **Line 1**: Function 'ModelValidator.add_cross_field_validator' parameter 'validator' name doesn't match type hint
- 🔵 **Line 1**: Function 'ModelValidator.validate' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'ValidatorChain.validate' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'CommonValidators.not_empty' uses overly generic type 'Any' for parameter 'value'

### src/haive/core/schema/compatibility/compatibility.py

- 🔵 **Line 45**: Method 'MessageConverter.name' missing docstring
- 🔵 **Line 45**: Method 'MessageConverter.name' missing type hints
- 🔵 **Line 49**: Method 'MessageConverter.priority' missing docstring
- 🔵 **Line 49**: Method 'MessageConverter.priority' missing type hints
- 🔵 **Line 192**: Method 'DocumentConverter.name' missing docstring
- 🔵 **Line 192**: Method 'DocumentConverter.name' missing type hints
- 🔵 **Line 196**: Method 'DocumentConverter.priority' missing docstring
- 🔵 **Line 196**: Method 'DocumentConverter.priority' missing type hints
- 🔵 **Line 359**: Method 'PromptConverter.name' missing docstring
- 🔵 **Line 359**: Method 'PromptConverter.name' missing type hints
- 🔵 **Line 363**: Method 'PromptConverter.priority' missing docstring
- 🔵 **Line 363**: Method 'PromptConverter.priority' missing type hints
- 🔵 **Line 1**: Function 'DocumentConverter.convert' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'DocumentConverter.convert' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'PromptConverter.convert' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'PromptConverter.convert' returns overly generic type 'Any'

### src/haive/core/schema/compatibility/langchain_converters.py

- 🔵 **Line 45**: Method 'MessageConverter.name' missing docstring
- 🔵 **Line 45**: Method 'MessageConverter.name' missing type hints
- 🔵 **Line 49**: Method 'MessageConverter.priority' missing docstring
- 🔵 **Line 49**: Method 'MessageConverter.priority' missing type hints
- 🔵 **Line 192**: Method 'DocumentConverter.name' missing docstring
- 🔵 **Line 192**: Method 'DocumentConverter.name' missing type hints
- 🔵 **Line 196**: Method 'DocumentConverter.priority' missing docstring
- 🔵 **Line 196**: Method 'DocumentConverter.priority' missing type hints
- 🔵 **Line 359**: Method 'PromptConverter.name' missing docstring
- 🔵 **Line 359**: Method 'PromptConverter.name' missing type hints
- 🔵 **Line 363**: Method 'PromptConverter.priority' missing docstring
- 🔵 **Line 363**: Method 'PromptConverter.priority' missing type hints
- 🔵 **Line 1**: Function 'DocumentConverter.convert' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'DocumentConverter.convert' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'PromptConverter.convert' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'PromptConverter.convert' returns overly generic type 'Any'

### src/haive/core/schema/compatibility/protocols.py

- 🔵 **Line 38**: Method 'SchemaConvertible.to_schema' missing type hints
- 🔵 **Line 79**: Method 'ConversionStrategy.name' missing type hints
- 🔵 **Line 141**: Method 'SchemaEvolution.version' missing type hints
- 🔵 **Line 164**: Method 'CompatibilityPlugin.name' missing type hints
- 🔵 **Line 169**: Method 'CompatibilityPlugin.priority' missing type hints
- 🔵 **Line 204**: Method 'AsyncConverter.supports_sync' missing type hints
- 🔵 **Line 221**: Method 'SchemaRegistry.list_schemas' missing type hints
- 🔵 **Line 271**: Method 'PluginManager.get_converters' missing type hints
- 🔵 **Line 275**: Method 'PluginManager.get_validators' missing type hints
- 🔵 **Line 279**: Method 'PluginManager.get_inspectors' missing type hints
- 🔵 **Line 283**: Method 'PluginManager.get_compatibility_plugins' missing type hints
- 🔵 **Line 287**: Method 'PluginManager.get_resolvers' missing type hints
- 🔵 **Line 297**: Function 'converter_plugin' missing type hints
- 🔵 **Line 303**: Function 'validator_plugin' missing type hints
- 🔵 **Line 309**: Function 'compatibility_plugin' missing type hints
- 🟡 **Line 312**: Function 'decorator' missing docstring
- 🔵 **Line 312**: Function 'decorator' missing type hints
- 🔵 **Line 1**: Function 'FieldTransformer.**call**' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'FieldTransformer.**call**' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'ConversionStrategy.convert' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'ConversionStrategy.convert' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'CompatibilityPlugin.enhance_report' uses overly generic type 'Any' for parameter 'report'
- 🔵 **Line 1**: Function 'PluginManager.register_validator' parameter 'validator' name doesn't match type hint

### src/haive/core/schema/compatibility/field_mapping.py

- 🔵 **Line 343**: Method 'FieldMapper.to_dict' missing type hints
- 🔵 **Line 1**: Function 'FieldMapping.\_extract_path_value' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'FieldMapping.\_extract_path_value' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'FieldMapper.add_mapping' uses overly generic type 'Any' for parameter 'default'
- 🔵 **Line 1**: Function 'FieldMapper.add_aggregate_field' uses overly generic type 'Any' for parameter 'default'

### src/haive/core/schema/compatibility/converters.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/schema/compatibility/utils.py

- 🔵 **Line 235**: Function 'merge_dicts' missing type hints
- 🔵 **Line 364**: Function 'get_all_subclasses' missing type hints
- 🟡 **Line 349**: Function 'wrapper' missing docstring
- 🔵 **Line 349**: Function 'wrapper' missing type hints
- 🔵 **Line 1**: Function 'extract_path_value' uses overly generic type 'Any' for parameter 'default'
- 🔵 **Line 1**: Function 'extract_path_value' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'create_example_value' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'create_example_value' might return None but type signature doesn't indicate Optional

### src/haive/core/schema/compatibility/reports.py

- 🔵 **Line 53**: Method 'CompatibilityReport.to_dict' missing type hints
- 🔵 **Line 79**: Method 'CompatibilityReport.to_markdown' missing type hints

### src/haive/core/schema/compatibility/types.py

- 🔵 **Line 77**: Method 'TypeInfo.full_name' missing type hints
- 🔵 **Line 109**: Method 'FieldInfo.field_path' missing type hints
- 🔵 **Line 137**: Method 'SchemaInfo.get_required_fields' missing type hints
- 🔵 **Line 141**: Method 'SchemaInfo.get_optional_fields' missing type hints
- 🔵 **Line 164**: Method 'ConversionPath.step_count' missing type hints
- 🔵 **Line 1**: Function 'ConversionContext.track_lost_field' uses overly generic type 'Any' for parameter 'value'

### src/haive/core/schema/compatibility/mergers.py

- 🔵 **Line 434**: Function 'create_union_schema' missing type hints
- 🔵 **Line 442**: Function 'create_intersection_schema' missing type hints

### src/haive/core/schema/compatibility/examples.py

- 🔵 **Line 32**: Function 'example_basic_compatibility' missing type hints
- 🔵 **Line 62**: Function 'example_langchain_conversion' missing type hints
- 🔵 **Line 96**: Function 'example_field_mapping' missing type hints
- 🔵 **Line 150**: Function 'example_schema_merging' missing type hints
- 🔵 **Line 192**: Function 'example_custom_converter' missing type hints
- 🔵 **Line 253**: Function 'example_compatibility_report' missing type hints
- 🔵 **Line 280**: Function 'example_state_schema_compatibility' missing type hints
- 🔵 **Line 315**: Function 'example_field_validation' missing type hints
- 🔵 **Line 376**: Function 'example_schema_evolution' missing type hints
- 🔵 **Line 433**: Function 'example_performance_optimization' missing type hints
- 🟡 **Line 37**: Class 'UserInput' missing docstring
- 🟡 **Line 44**: Class 'UserProfile' missing docstring
- 🟡 **Line 155**: Class 'BasicInfo' missing docstring
- 🟡 **Line 160**: Class 'ContactInfo' missing docstring
- 🟡 **Line 165**: Class 'Preferences' missing docstring
- 🟡 **Line 203**: Class 'Temperature' missing docstring
- 🟡 **Line 207**: Class 'Celsius' missing docstring
- 🟡 **Line 211**: Class 'TemperatureConverter' missing docstring
- 🔵 **Line 213**: Method 'TemperatureConverter.name' missing docstring
- 🔵 **Line 213**: Method 'TemperatureConverter.name' missing type hints
- 🔵 **Line 216**: Method 'TemperatureConverter.can_convert' missing docstring
- 🔵 **Line 221**: Method 'TemperatureConverter.get_quality' missing docstring
- 🔵 **Line 226**: Method 'TemperatureConverter.convert' missing docstring
- 🟡 **Line 258**: Class 'SourceAgent' missing docstring
- 🟡 **Line 264**: Class 'TargetAgent' missing docstring
- 🟡 **Line 287**: Class 'ChatState' missing docstring
- 🟡 **Line 327**: Class 'UserRegistration' missing docstring
- 🟡 **Line 352**: Function 'passwords_match' missing docstring
- 🟡 **Line 381**: Class 'UserV1' missing docstring
- 🟡 **Line 390**: Class 'Role' missing docstring
- 🟡 **Line 395**: Class 'UserV2' missing docstring
- 🟡 **Line 443**: Class 'ComplexSchema' missing docstring
- 🟡 **Line 293**: Class 'Config' missing docstring
- 🔵 **Line 1**: Function 'TemperatureConverter.convert' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'TemperatureConverter.convert' returns overly generic type 'Any'

### src/haive/core/schema/prebuilt/messages/compatibility.py

- 🔵 **Line 50**: Method 'MessagesStateAdapter.get_conversation_rounds' missing type hints
- 🔵 **Line 131**: Method 'MessagesStateAdapter.deduplicate_tool_calls' missing type hints
- 🔵 **Line 180**: Method 'MessagesStateAdapter.get_completed_tool_calls' missing type hints

### src/haive/core/schema/prebuilt/messages/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/schema/prebuilt/messages/messages_state.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 162**: Method 'MessageList.ensure_system_before_human' missing type hints
- 🔵 **Line 191**: Method 'MessageList.last_message' missing type hints
- 🔵 **Line 197**: Method 'MessageList.last_human_message' missing type hints
- 🔵 **Line 206**: Method 'MessageList.last_ai_message' missing type hints
- 🔵 **Line 215**: Method 'MessageList.first_real_human_message' missing type hints
- 🔵 **Line 224**: Method 'MessageList.system_message' missing type hints
- 🔵 **Line 233**: Method 'MessageList.has_tool_calls' missing type hints
- 🔵 **Line 253**: Method 'MessageList.has_tool_errors' missing type hints
- 🔵 **Line 262**: Method 'MessageList.message_count' missing type hints
- 🔵 **Line 268**: Method 'MessageList.round_count' missing type hints
- 🔵 **Line 274**: Method 'MessageList.tool_call_errors' missing type hints
- 🔵 **Line 284**: Method 'MessageList.completed_tool_calls' missing type hints
- 🔵 **Line 290**: Method 'MessageList.conversation_rounds' missing type hints
- 🔵 **Line 296**: Method 'MessageList.real_human_messages' missing type hints
- 🔵 **Line 306**: Method 'MessageList.transformed_human_messages' missing type hints
- 🔵 **Line 367**: Method 'MessageList.clear' missing type hints
- 🔵 **Line 372**: Method 'MessageList.copy' missing type hints
- 🔵 **Line 483**: Method 'MessageList.get_messages_in_current_round' missing type hints
- 🔵 **Line 499**: Method 'MessageList.deduplicate_tool_calls' missing type hints
- 🔵 **Line 559**: Method 'MessageList.get_pending_tool_calls' missing type hints
- 🔵 **Line 946**: Method 'MessageList.to_openai_format' missing type hints
- 🔵 **Line 950**: Method 'MessageList.to_langchain_prompt' missing type hints
- 🔵 **Line 954**: Method 'MessageList.get_filtered_messages' missing type hints
- 🔵 **Line 999**: Method 'MessageList.model_dump' missing type hints
- 🔵 **Line 1046**: Method 'MessagesState.last_message' missing type hints
- 🔵 **Line 1051**: Method 'MessagesState.last_human_message' missing type hints
- 🔵 **Line 1056**: Method 'MessagesState.last_ai_message' missing type hints
- 🔵 **Line 1061**: Method 'MessagesState.first_real_human_message' missing type hints
- 🔵 **Line 1066**: Method 'MessagesState.system_message' missing type hints
- 🔵 **Line 1071**: Method 'MessagesState.has_tool_calls' missing type hints
- 🔵 **Line 1076**: Method 'MessagesState.has_tool_errors' missing type hints
- 🔵 **Line 1081**: Method 'MessagesState.message_count' missing type hints
- 🔵 **Line 1086**: Method 'MessagesState.round_count' missing type hints
- 🔵 **Line 1091**: Method 'MessagesState.tool_call_errors' missing type hints
- 🔵 **Line 1096**: Method 'MessagesState.completed_tool_calls' missing type hints
- 🔵 **Line 1101**: Method 'MessagesState.conversation_rounds' missing type hints
- 🔵 **Line 1106**: Method 'MessagesState.real_human_messages' missing type hints
- 🔵 **Line 1111**: Method 'MessagesState.transformed_human_messages' missing type hints
- 🔵 **Line 1153**: Method 'MessagesState.clear' missing type hints
- 🔵 **Line 1165**: Method 'MessagesState.deduplicate_tool_calls' missing type hints
- 🔵 **Line 1169**: Method 'MessagesState.get_pending_tool_calls' missing type hints
- 🔵 **Line 1**: Function 'MessageList.convert_strings_to_messages' uses overly generic type 'Any' for parameter 'v'
- 🔵 **Line 1**: Function 'MessageList.\_convert_message_data' uses overly generic type 'Any' for parameter 'data'
- 🔵 **Line 1**: Function 'MessageList.filter_by_metadata' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'MessageList.transform_for_reflection' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'MessageList.model_dump' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'MessagesState.filter_by_metadata' uses overly generic type 'Any' for parameter 'value'

### src/haive/core/schema/prebuilt/messages/examples.py

- 🔵 **Line 22**: Function 'basic_usage_example' missing type hints
- 🔵 **Line 54**: Function 'tool_usage_example' missing type hints
- 🔵 **Line 101**: Function 'enhanced_features_example' missing type hints
- 🔵 **Line 144**: Function 'agent_handoff_example' missing type hints
- 🔵 **Line 196**: Function 'enhanced_implementation_example' missing type hints

### src/haive/core/graph/node/config.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 136**: Method 'NodeConfig.to_dict' missing type hints
- 🔵 **Line 184**: Method 'NodeConfig.validate_and_determine_node_type' missing type hints
- 🔵 **Line 282**: Method 'NodeConfig.get_engine' missing type hints
- 🔵 **Line 316**: Method 'NodeConfig.get_input_mapping' missing type hints
- 🔵 **Line 327**: Method 'NodeConfig.get_output_mapping' missing type hints

### src/haive/core/graph/node/message_transformation.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 103**: Method 'MessageTransformationNodeConfig.validate_transformation_config' missing type hints

### src/haive/core/graph/node/factory.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 1**: Function 'NodeFactory.\_create_generic_node' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'NodeFactory.\_extract_input' uses overly generic type 'Any' for parameter 'state'
- 🔵 **Line 1**: Function 'NodeFactory.\_extract_input' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'NodeFactory.\_process_output' uses overly generic type 'Any' for parameter 'output'

### src/haive/core/graph/node/agent_node.py

- 🔵 **Line 1**: Function 'AgentNodeConfig.\_process_agent_output' uses overly generic type 'Any' for parameter 'result'

### src/haive/core/graph/node/protocols.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 15**: Method 'NodeProcessor.can_process' missing docstring
- 🔵 **Line 16**: Method 'NodeProcessor.create_node_function' missing docstring
- 🔵 **Line 23**: Method 'CommandHandler.process_result' missing docstring
- 🔵 **Line 32**: Method 'InputProcessor.extract_input' missing docstring
- 🔵 **Line 39**: Method 'OutputProcessor.process_output' missing docstring
- 🔵 **Line 1**: Function 'NodeProcessor.can_process' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'NodeProcessor.create_node_function' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'NodeProcessor.create_node_function' uses overly generic type 'Any' for parameter 'node_config'
- 🔵 **Line 1**: Function 'CommandHandler.process_result' uses overly generic type 'Any' for parameter 'result'
- 🔵 **Line 1**: Function 'CommandHandler.process_result' uses overly generic type 'Any' for parameter 'config'
- 🔵 **Line 1**: Function 'CommandHandler.process_result' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'InputProcessor.extract_input' uses overly generic type 'Any' for parameter 'config'
- 🔵 **Line 1**: Function 'InputProcessor.extract_input' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'OutputProcessor.process_output' uses overly generic type 'Any' for parameter 'result'
- 🔵 **Line 1**: Function 'OutputProcessor.process_output' uses overly generic type 'Any' for parameter 'config'

### src/haive/core/graph/node/registry.py

- 🔵 **Line 36**: Method 'NodeRegistry.get_instance' missing type hints
- 🔵 **Line 129**: Method 'NodeRegistry.list_all_names' missing type hints
- 🔵 **Line 154**: Method 'NodeRegistry.clear' missing type hints

### src/haive/core/graph/node/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition
- 🔵 **Line 274**: Function 'get_registry' missing type hints
- 🔵 **Line 1**: Function 'create_node' uses overly generic type 'Any' for parameter 'engine_or_callable'
- 🔵 **Line 1**: Function 'create_engine_node' uses overly generic type 'Any' for parameter 'engine'

### src/haive/core/graph/node/decorators.py

- 🔵 **Line 27**: Function 'register_node' missing type hints
- 🔵 **Line 83**: Function 'tool_node' missing type hints
- 🔵 **Line 116**: Function 'validation_node' missing type hints
- 🔵 **Line 146**: Function 'branch_node' missing type hints
- 🔵 **Line 173**: Function 'send_node' missing type hints
- 🔵 **Line 201**: Function 'debug_node' missing type hints
- 🟡 **Line 55**: Function 'decorator' missing docstring
- 🔵 **Line 55**: Function 'decorator' missing type hints
- 🟡 **Line 218**: Function 'decorator' missing docstring
- 🔵 **Line 218**: Function 'decorator' missing type hints
- 🟡 **Line 221**: Function 'wrapper' missing docstring
- 🔵 **Line 221**: Function 'wrapper' missing type hints

### src/haive/core/graph/node/engine_node.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 1**: Function 'EngineNodeConfig.\_log_result_details' uses overly generic type 'Any' for parameter 'result'
- 🔵 **Line 1**: Function 'EngineNodeConfig.\_extract_smart_input' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'EngineNodeConfig.\_extract_embeddings_fields' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'EngineNodeConfig.\_extract_default_input' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'EngineNodeConfig.\_wrap_smart_result' uses overly generic type 'Any' for parameter 'result'
- 🔵 **Line 1**: Function 'EngineNodeConfig.\_create_update_dict' uses overly generic type 'Any' for parameter 'result'
- 🔵 **Line 1**: Function 'EngineNodeConfig.\_smart_result_mapping' uses overly generic type 'Any' for parameter 'result'
- 🔵 **Line 1**: Function 'EngineNodeConfig.\_update_messages' uses overly generic type 'Any' for parameter 'result'
- 🔵 **Line 1**: Function 'EngineNodeConfig.\_is_message_like' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'EngineNodeConfig.\_get_state_value' uses overly generic type 'Any' for parameter 'default'
- 🔵 **Line 1**: Function 'EngineNodeConfig.\_get_state_value' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'EngineNodeConfig.\_apply_output_mapping' uses overly generic type 'Any' for parameter 'result'
- 🔵 **Line 1**: Function 'EngineNodeConfig.\_map_to_outputs' uses overly generic type 'Any' for parameter 'result'
- 🔵 **Line 1**: Function 'EngineNodeConfig.\_execute_with_config' uses overly generic type 'Any' for parameter 'input_data'
- 🔵 **Line 1**: Function 'EngineNodeConfig.\_execute_with_config' returns overly generic type 'Any'

### src/haive/core/graph/node/handlers.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 1**: Function 'StandardCommandHandler.process_result' uses overly generic type 'Any' for parameter 'result'
- 🔵 **Line 1**: Function 'StandardCommandHandler.process_result' uses overly generic type 'Any' for parameter 'config'
- 🔵 **Line 1**: Function 'StandardCommandHandler.process_result' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'DirectInputProcessor.extract_input' uses overly generic type 'Any' for parameter 'config'
- 🔵 **Line 1**: Function 'DirectInputProcessor.extract_input' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'MappedInputProcessor.extract_input' uses overly generic type 'Any' for parameter 'config'
- 🔵 **Line 1**: Function 'MappedInputProcessor.extract_input' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'StandardOutputProcessor.process_output' uses overly generic type 'Any' for parameter 'result'
- 🔵 **Line 1**: Function 'StandardOutputProcessor.process_output' uses overly generic type 'Any' for parameter 'config'
- 🔵 **Line 1**: Function 'StructuredOutputProcessor.process_output' uses overly generic type 'Any' for parameter 'result'
- 🔵 **Line 1**: Function 'StructuredOutputProcessor.process_output' uses overly generic type 'Any' for parameter 'config'
- 🔵 **Line 1**: Function 'StructuredOutputProcessor.process_output' returns overly generic type 'Any'

### src/haive/core/graph/node/output_parsing.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 256**: Function 'detect_output_parser_need' missing type hints
- 🔵 **Line 270**: Function 'create_output_parser_node_for_agent' missing type hints
- 🔵 **Line 1**: Function 'OutputParserNodeConfig.\_extract_content_from_message' uses overly generic type 'Any' for parameter 'message'

### src/haive/core/graph/node/utils.py

- 🔵 **Line 1**: Function 'create_node' uses overly generic type 'Any' for parameter 'engine_or_callable'

### src/haive/core/graph/node/tool_node_config.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 295**: Method 'ToolNodeConfig.from_route_filter' missing type hints

### src/haive/core/graph/node/validation_node_config.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 1**: Function 'get_tool_name' uses overly generic type 'Any' for parameter 'tool_call'
- 🔵 **Line 1**: Function 'get_tool_args' uses overly generic type 'Any' for parameter 'tool_call'
- 🔵 **Line 1**: Function 'get_tool_id' uses overly generic type 'Any' for parameter 'tool_call'
- 🔵 **Line 1**: Function 'ValidationNodeConfig.\_get_tools_and_schemas_from_engine' uses overly generic type 'Any' for parameter 'engine'

### src/haive/core/graph/node/base_config.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 49**: Method 'NodeConfig.to_dict' missing type hints
- 🔵 **Line 1**: Function 'NodeConfig.**call**' returns overly generic type 'Any'

### src/haive/core/graph/node/parser_node_config.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 1**: Function 'ParserNodeConfig.\_find_tool_in_engine' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'ParserNodeConfig.\_parse_tool_content' uses overly generic type 'Any' for parameter 'content'
- 🔵 **Line 1**: Function 'ParserNodeConfig.\_parse_tool_content' returns overly generic type 'Any'

### src/haive/core/graph/node/test.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 17**: Class 'Plan' missing docstring

### src/haive/core/graph/node/processors.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 1**: Function 'process_state' uses overly generic type 'Any' for parameter 'state'
- 🔵 **Line 1**: Function 'process_state' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'extract_input' uses overly generic type 'Any' for parameter 'state'
- 🔵 **Line 1**: Function 'extract_input' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'process_output' uses overly generic type 'Any' for parameter 'result'
- 🔵 **Line 1**: Function 'process_output' uses overly generic type 'Any' for parameter 'original_state'
- 🔵 **Line 1**: Function 'process_output' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'handle_command_pattern' uses overly generic type 'Any' for parameter 'result'
- 🔵 **Line 1**: Function 'handle_command_pattern' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'create_error_result' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'InvokableNodeProcessor.can_process' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'InvokableNodeProcessor.create_node_function' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'AsyncInvokableNodeProcessor.can_process' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'AsyncInvokableNodeProcessor.create_node_function' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'CallableNodeProcessor.can_process' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'CallableNodeProcessor.create_node_function' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'AsyncNodeProcessor.can_process' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'AsyncNodeProcessor.create_node_function' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'MappingNodeProcessor.can_process' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'MappingNodeProcessor.create_node_function' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'GenericNodeProcessor.can_process' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'GenericNodeProcessor.create_node_function' uses overly generic type 'Any' for parameter 'engine'

### src/haive/core/graph/node/placeholder_node.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 9**: Function 'placeholder_node' missing docstring

### src/haive/core/graph/common/types.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/graph/common/field_utils.py

- 🔵 **Line 1**: Function 'extract_field' uses overly generic type 'Any' for parameter 'state'
- 🔵 **Line 1**: Function 'extract_field' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'extract_field' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'get_field_value' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'get_field_value' uses overly generic type 'Any' for parameter 'key'
- 🔵 **Line 1**: Function 'get_field_value' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'get_field_value' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'get_last_message_content' uses overly generic type 'Any' for parameter 'state'

### src/haive/core/graph/common/serialization.py

- 🔵 **Line 1**: Function 'ensure_serializable' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'ensure_serializable' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'to_json' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'from_json' returns overly generic type 'Any'

### src/haive/core/graph/common/references.py

- 🔵 **Line 102**: Method 'CallableReference.resolve' missing type hints
- 🔵 **Line 208**: Method 'TypeReference.resolve' missing type hints

### src/haive/core/graph/state_graph/base_graph.py

- 🔵 **Line 103**: Method 'Node.display_name' missing type hints
- 🔵 **Line 107**: Method 'Node.to_dict' missing type hints
- 🔵 **Line 156**: Method 'BaseGraph.validate_graph' missing type hints
- 🔵 **Line 1438**: Method 'BaseGraph.validate' missing type hints
- 🔵 **Line 1546**: Method 'BaseGraph.get_execution_paths' missing type hints
- 🔵 **Line 1581**: Method 'BaseGraph.get_start_nodes' missing type hints
- 🔵 **Line 1592**: Method 'BaseGraph.get_end_nodes' missing type hints
- 🔵 **Line 1603**: Method 'BaseGraph.get_orphan_nodes' missing type hints
- 🔵 **Line 1826**: Method 'BaseGraph.to_dict' missing type hints
- 🔵 **Line 1862**: Method 'BaseGraph.to_json' missing type hints
- 🔵 **Line 1901**: Method 'BaseGraph.to_mermaid' missing type hints
- 🔵 **Line 1**: Function 'BaseGraph.add_key_value_branch' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'BaseGraph.get_execution_paths' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'BaseGraph.to_langgraph' uses overly generic type 'Any' for parameter 'state_schema'
- 🔵 **Line 1**: Function 'BaseGraph.to_langgraph' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'BaseGraph.from_langgraph' uses overly generic type 'Any' for parameter 'state_graph'

### src/haive/core/graph/state_graph/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 64**: Method 'SerializableModel.mark_modified' missing type hints
- 🔵 **Line 69**: Method 'SerializableModel.is_modified' missing type hints
- 🔵 **Line 73**: Method 'SerializableModel.reset_modified' missing type hints
- 🔵 **Line 99**: Method 'SerializableModel.list_all' missing type hints
- 🔵 **Line 106**: Method 'SerializableModel.get_all' missing type hints

### src/haive/core/graph/state_graph/mixin.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 61**: Class 'PassThroughState' missing docstring
- 🔵 **Line 1**: Function 'GraphSchemaMixin.validate_input' uses overly generic type 'Any' for parameter 'data'
- 🔵 **Line 1**: Function 'GraphSchemaMixin.validate_input' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'GraphSchemaMixin.validate_output' uses overly generic type 'Any' for parameter 'data'
- 🔵 **Line 1**: Function 'GraphSchemaMixin.validate_output' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'GraphSchemaMixin.create_state' returns overly generic type 'Any'

### src/haive/core/graph/state_graph/serializable.py

- 🔵 **Line 36**: Method 'TypeReference.from_type' missing docstring
- 🔵 **Line 36**: Method 'TypeReference.from_type' missing type hints
- 🔵 **Line 48**: Method 'TypeReference.resolve' missing type hints
- 🔵 **Line 155**: Method 'SerializableGraph.from_graph' missing type hints
- 🔵 **Line 330**: Method 'SerializableGraph.to_graph' missing type hints
- 🔵 **Line 540**: Method 'SerializableGraph.to_dict' missing type hints
- 🔵 **Line 545**: Method 'SerializableGraph.from_dict' missing type hints
- 🔵 **Line 550**: Method 'SerializableGraph.to_json' missing type hints
- 🔵 **Line 562**: Method 'SerializableGraph.from_json' missing type hints

### src/haive/core/graph/state_graph/pattern_registry.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 12**: Method 'PatternRegistry.get_instance' missing type hints
- 🔵 **Line 52**: Method 'PatternRegistry.clear' missing type hints
- 🔵 **Line 1**: Function 'PatternRegistry.get' uses overly generic type 'Any' for parameter 'item_type'
- 🔵 **Line 1**: Function 'PatternRegistry.list' uses overly generic type 'Any' for parameter 'item_type'
- 🔵 **Line 1**: Function 'PatternRegistry.get_all' uses overly generic type 'Any' for parameter 'item_type'

### src/haive/core/graph/state_graph/state_graph_builder.py

- 🔴 **Line 1**: Could not parse file: unexpected indent (<unknown>, line 166)

### src/haive/core/graph/state_graph/registry.py

- 🔴 **Line 1**: Could not parse file: unterminated triple-quoted string literal (detected at line 105) (<unknown>, line 103)

### src/haive/core/graph/state_graph/validation_mixin.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 25**: Method 'GraphValidationProtocol.analyze_cycles' missing type hints
- 🔵 **Line 30**: Method 'GraphValidationProtocol.find_orphan_nodes' missing type hints
- 🔵 **Line 35**: Method 'GraphValidationProtocol.find_dangling_edges' missing type hints
- 🔵 **Line 40**: Method 'GraphValidationProtocol.find_unreachable_nodes' missing type hints
- 🔵 **Line 45**: Method 'GraphValidationProtocol.find_nodes_without_end_path' missing type hints
- 🔵 **Line 50**: Method 'GraphValidationProtocol.has_entry_point' missing type hints
- 🔵 **Line 68**: Method 'ValidationMixin.validate_graph' missing type hints
- 🔵 **Line 114**: Method 'ValidationMixin.display_validation_report' missing type hints
- 🔵 **Line 1**: Function 'ValidationMixin.display_validation_report' might return None but type signature doesn't indicate Optional

### src/haive/core/graph/state_graph/types.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/graph/state_graph/graph_path.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 34**: Method 'GraphPath.display' missing type hints
- 🔵 **Line 1**: Function 'GraphPath.display' might return None but type signature doesn't indicate Optional

### src/haive/core/graph/state_graph/pattern_definition.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/graph/state_graph/schema_graph.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 29**: Method 'SchemaGraph.to_langgraph' missing type hints
- 🔵 **Line 38**: Method 'SchemaGraph.compile' missing type hints
- 🔵 **Line 51**: Method 'SchemaGraph.display' missing type hints

### src/haive/core/graph/state_graph/state_graph.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 143**: Method 'StateGraphSerializable.validate_graph_structure' missing type hints
- 🔵 **Line 160**: Method 'StateGraphSerializable.node_count' missing type hints
- 🔵 **Line 166**: Method 'StateGraphSerializable.edge_count' missing type hints
- 🔵 **Line 176**: Method 'StateGraphSerializable.all_edges' missing type hints
- 🔵 **Line 216**: Method 'StateGraphSerializable.mark_modified' missing type hints
- 🔵 **Line 603**: Method 'StateGraphSerializable.validate' missing type hints
- 🔵 **Line 671**: Method 'StateGraphSerializable.is_modified' missing type hints
- 🔵 **Line 675**: Method 'StateGraphSerializable.reset_modified' missing type hints
- 🔵 **Line 679**: Method 'StateGraphSerializable.to_dict' missing type hints
- 🔵 **Line 688**: Method 'StateGraphSerializable.to_json' missing type hints
- 🔵 **Line 1**: Function 'StateGraphSerializable.add_node' uses overly generic type 'Any' for parameter 'node_spec'
- 🔵 **Line 1**: Function 'StateGraphSerializable.from_state_graph' uses overly generic type 'Any' for parameter 'graph'

### src/haive/core/graph/state_graph/base_graph2.py

- 🔵 **Line 114**: Method 'Node.display_name' missing type hints
- 🔵 **Line 118**: Method 'Node.to_dict' missing type hints
- 🔵 **Line 195**: Method 'BaseGraph.validate_graph' missing type hints
- 🔵 **Line 695**: Method 'BaseGraph.get_conditional_entries' missing type hints
- 🔵 **Line 704**: Method 'BaseGraph.get_conditional_exits' missing type hints
- 🔵 **Line 714**: Method 'BaseGraph.all_entry_points' missing type hints
- 🔵 **Line 735**: Method 'BaseGraph.all_finish_points' missing type hints
- 🔵 **Line 756**: Method 'BaseGraph.entry_points_data' missing type hints
- 🔵 **Line 761**: Method 'BaseGraph.exit_points' missing type hints
- 🔵 **Line 766**: Method 'BaseGraph.all_exit_points' missing type hints
- 🔵 **Line 1730**: Method 'BaseGraph.find_all_paths' missing type hints
- 🔵 **Line 1977**: Method 'BaseGraph.check_graph_validity' missing type hints
- 🔵 **Line 2006**: Method 'BaseGraph.find_unreachable_nodes' missing type hints
- 🔵 **Line 2045**: Method 'BaseGraph.find_nodes_without_end_path' missing type hints
- 🔵 **Line 2065**: Method 'BaseGraph.find_nodes_without_finish_path' missing type hints
- 🔵 **Line 2075**: Method 'BaseGraph.get_source_nodes' missing type hints
- 🔵 **Line 2104**: Method 'BaseGraph.get_sink_nodes' missing type hints
- 🔵 **Line 2703**: Method 'BaseGraph.conditional_edges' missing type hints
- 🔵 **Line 3023**: Method 'BaseGraph.extend_from' missing type hints
- 🔵 **Line 3656**: Method 'BaseGraph.to_dict' missing type hints
- 🔵 **Line 3692**: Method 'BaseGraph.to_json' missing type hints
- 🔵 **Line 4050**: Method 'BaseGraph.analyze_cycles' missing type hints
- 🔵 **Line 4096**: Method 'BaseGraph.find_orphan_nodes' missing type hints
- 🔵 **Line 4139**: Method 'BaseGraph.find_dangling_edges' missing type hints
- 🔵 **Line 4170**: Method 'BaseGraph.has_entry_point' missing type hints
- 🔵 **Line 4340**: Function 'has_tool_calls_fixed' missing type hints
- 🔵 **Line 4410**: Function 'create_debug_has_tool_calls' missing type hints
- 🟡 **Line 4421**: Function 'debug_wrapper' missing docstring
- 🔵 **Line 4421**: Function 'debug_wrapper' missing type hints
- 🟡 **Line 3207**: Class 'PassThroughState' missing docstring
- 🔵 **Line 1**: Function 'BaseGraph.\_infer_node_type' uses overly generic type 'Any' for parameter 'node'
- 🔵 **Line 1**: Function 'BaseGraph.add_key_value_branch' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'BaseGraph.to_langgraph' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'BaseGraph.from_langgraph' uses overly generic type 'Any' for parameter 'state_graph'
- 🔵 **Line 1**: Function 'BaseGraph.analyze_cycles' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'BaseGraph.compile' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'BaseGraph.compile' parameter 'raise_on_validation_error' name doesn't match type hint
- 🔵 **Line 1**: Function 'BaseGraph.debug_conditional_routing' might return None but type signature doesn't indicate Optional

### src/haive/core/graph/state_graph/graph_visualizer.py

- 🔵 **Line 1**: Function 'GraphVisualizer.generate_mermaid' uses overly generic type 'Any' for parameter 'graph'
- 🔵 **Line 1**: Function 'GraphVisualizer.\_detect_all_agents' uses overly generic type 'Any' for parameter 'graph'
- 🔵 **Line 1**: Function 'GraphVisualizer.\_check_if_agent' uses overly generic type 'Any' for parameter 'node'
- 🔵 **Line 1**: Function 'GraphVisualizer.\_is_agent_class' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'GraphVisualizer.\_get_engine_type' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'GraphVisualizer.\_get_graph_from_object' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'GraphVisualizer.\_build_graph' uses overly generic type 'Any' for parameter 'graph'
- 🔵 **Line 1**: Function 'GraphVisualizer.\_process_nodes' uses overly generic type 'Any' for parameter 'graph'
- 🔵 **Line 1**: Function 'GraphVisualizer.\_add_regular_node' uses overly generic type 'Any' for parameter 'node'
- 🔵 **Line 1**: Function 'GraphVisualizer.\_add_regular_node' uses overly generic type 'Any' for parameter 'graph'
- 🔵 **Line 1**: Function 'GraphVisualizer.\_process_edges' uses overly generic type 'Any' for parameter 'graph'
- 🔵 **Line 1**: Function 'GraphVisualizer.\_process_branches' uses overly generic type 'Any' for parameter 'graph'
- 🔵 **Line 1**: Function 'GraphVisualizer.\_determine_node_style' uses overly generic type 'Any' for parameter 'node'
- 🔵 **Line 1**: Function 'GraphVisualizer.\_determine_node_style' uses overly generic type 'Any' for parameter 'graph'
- 🔵 **Line 1**: Function 'GraphVisualizer.\_create_node_label' uses overly generic type 'Any' for parameter 'node'
- 🔵 **Line 1**: Function 'GraphVisualizer.\_get_branch_destinations' uses overly generic type 'Any' for parameter 'branch'
- 🔵 **Line 1**: Function 'GraphVisualizer.\_format_condition_label' uses overly generic type 'Any' for parameter 'condition'
- 🔵 **Line 1**: Function 'GraphVisualizer.\_add_agent_connections' uses overly generic type 'Any' for parameter 'graph'
- 🔵 **Line 1**: Function 'GraphVisualizer.display_graph' uses overly generic type 'Any' for parameter 'graph'
- 🔵 **Line 1**: Function 'GraphVisualizer.debug_graph_structure' uses overly generic type 'Any' for parameter 'graph'

### src/haive/core/graph/state_graph/schema_mixin.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 137**: Method 'GraphSchemaMixin.get_shared_fields' missing type hints
- 🔵 **Line 150**: Method 'GraphSchemaMixin.get_reducer_fields' missing type hints
- 🟡 **Line 64**: Class 'PassThroughState' missing docstring
- 🔵 **Line 1**: Function 'GraphSchemaMixin.validate_input' uses overly generic type 'Any' for parameter 'data'
- 🔵 **Line 1**: Function 'GraphSchemaMixin.validate_input' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'GraphSchemaMixin.validate_output' uses overly generic type 'Any' for parameter 'data'
- 🔵 **Line 1**: Function 'GraphSchemaMixin.validate_output' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'GraphSchemaMixin.create_state' returns overly generic type 'Any'

### src/haive/core/graph/state_graph/pattern_decorator.py

- 🔵 **Line 17**: Function 'register_pattern' missing type hints
- 🟡 **Line 35**: Function 'decorator' missing docstring
- 🔵 **Line 35**: Function 'decorator' missing type hints
- 🟡 **Line 50**: Function 'wrapper' missing docstring
- 🔵 **Line 50**: Function 'wrapper' missing type hints

### src/haive/core/graph/gb/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition
- 🔵 **Line 78**: Method 'BaseGraph.number_of_nodes' missing type hints
- 🔵 **Line 86**: Method 'BaseGraph.number_of_edges' missing type hints

### src/haive/core/graph/gb/types.py

- 🔵 **Line 83**: Method 'NamedEntity.name' missing docstring
- 🔵 **Line 83**: Method 'NamedEntity.name' missing type hints

### src/haive/core/graph/utils/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/graph/utils/mermaid_visualizer.py

- 🔴 **Line 1**: Could not parse file: closing parenthesis ']' does not match opening parenthesis '(' (<unknown>, line 256)

### src/haive/core/graph/routers/base.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/graph/routers/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/graph/routers/conditions.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/graph/routers/test.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/graph/branches/branch.py

- 🔵 **Line 82**: Method 'Branch.setup_function_and_mappings' missing type hints
- 🔵 **Line 102**: Method 'Branch.validate_destinations_and_default' missing type hints
- 🔵 **Line 498**: Method 'Branch.extract_field_references' missing type hints
- 🔵 **Line 1**: Function 'Branch.\_process_result' uses overly generic type 'Any' for parameter 'result'
- 🔵 **Line 1**: Function 'Branch.\_compare' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'Branch.\_evaluate_dynamic' returns overly generic type 'Any'

### src/haive/core/graph/branches/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition
- 🔵 **Line 69**: Function 'chain' missing type hints
- 🔵 **Line 1**: Function 'key_equals' uses overly generic type 'Any' for parameter 'value'

### src/haive/core/graph/branches/utils.py

- 🔵 **Line 1**: Function 'extract_field' uses overly generic type 'Any' for parameter 'state'
- 🔵 **Line 1**: Function 'extract_field' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'extract_field' might return None but type signature doesn't indicate Optional
- 🔵 **Line 1**: Function 'get_field_value' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'get_field_value' uses overly generic type 'Any' for parameter 'key'
- 🔵 **Line 1**: Function 'get_field_value' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'get_field_value' might return None but type signature doesn't indicate Optional

### src/haive/core/graph/branches/dynamic.py

- 🔵 **Line 43**: Method 'DynamicMapping.validate_mappings' missing docstring
- 🔵 **Line 43**: Method 'DynamicMapping.validate_mappings' missing type hints

### src/haive/core/graph/branches/types.py

- 🔵 **Line 70**: Method 'BranchResult.is_send' missing type hints
- 🔵 **Line 79**: Method 'BranchResult.is_command' missing type hints
- 🔵 **Line 88**: Method 'BranchResult.has_mapping' missing type hints

### src/haive/core/graph/retry/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 1**: Function 'execute_with_retry' returns overly generic type 'Any'

### src/haive/core/graph/patterns/integration.py

- 🔵 **Line 149**: Function 'register_node_factory_integration' missing type hints
- 🔵 **Line 185**: Function 'register_dynamic_graph_integration' missing type hints
- 🔵 **Line 297**: Function 'register_callable_processor' missing type hints
- 🔵 **Line 314**: Function 'register_integrations' missing type hints
- 🔵 **Line 122**: Function 'pattern_node' missing type hints
- 🔵 **Line 197**: Function 'enhanced_apply_pattern' missing type hints
- 🔵 **Line 161**: Function 'create_pattern_node' missing type hints
- 🔵 **Line 230**: Function 'apply_branch' missing type hints
- 🔵 **Line 1**: Function 'apply_pattern_to_graph' uses overly generic type 'Any' for parameter 'graph'
- 🔵 **Line 1**: Function 'apply_pattern_to_graph' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'apply_branch_to_graph' uses overly generic type 'Any' for parameter 'graph'
- 🔵 **Line 1**: Function 'apply_branch_to_graph' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'create_pattern_node_config' returns overly generic type 'Any'

### src/haive/core/graph/patterns/base.py

- 🔵 **Line 236**: Method 'GraphPattern.name' missing type hints
- 🔵 **Line 290**: Method 'GraphPattern.to_dict' missing type hints
- 🔵 **Line 441**: Method 'BranchDefinition.create_condition' missing type hints
- 🔵 **Line 522**: Method 'BranchDefinition.to_dict' missing type hints
- 🔵 **Line 1**: Function 'ComponentRequirement.validate_component' uses overly generic type 'Any' for parameter 'component'
- 🔵 **Line 1**: Function 'ParameterDefinition.validate_value' uses overly generic type 'Any' for parameter 'value'
- 🔵 **Line 1**: Function 'GraphPattern.apply' uses overly generic type 'Any' for parameter 'graph'
- 🔵 **Line 1**: Function 'GraphPattern.apply' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'GraphPattern.create_node_config' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'BranchDefinition.apply_to_graph' uses overly generic type 'Any' for parameter 'graph'
- 🔵 **Line 1**: Function 'BranchDefinition.apply_to_graph' returns overly generic type 'Any'

### src/haive/core/graph/patterns/registry.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 26**: Method 'GraphPatternRegistry.get_instance' missing type hints
- 🔵 **Line 114**: Method 'GraphPatternRegistry.clear' missing type hints
- 🔵 **Line 1**: Function 'GraphPatternRegistry.get' uses overly generic type 'Any' for parameter 'item_type'
- 🔵 **Line 1**: Function 'GraphPatternRegistry.list' uses overly generic type 'Any' for parameter 'item_type'
- 🔵 **Line 1**: Function 'GraphPatternRegistry.get_all' uses overly generic type 'Any' for parameter 'item_type'

### src/haive/core/graph/patterns/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/graph/state_graph/conversion/langgraph.py

- 🟡 **Line 156**: Function 'wrapper' missing docstring
- 🔵 **Line 156**: Function 'wrapper' missing type hints
- 🟡 **Line 135**: Function 'action' missing docstring
- 🔵 **Line 135**: Function 'action' missing type hints
- 🔵 **Line 1**: Function 'convert_to_langgraph' uses overly generic type 'Any' for parameter 'graph'
- 🔵 **Line 1**: Function 'extract_callable' uses overly generic type 'Any' for parameter 'node'
- 🔵 **Line 1**: Function 'extract_callable' returns overly generic type 'Any'
- 🔵 **Line 1**: Function 'create_parameter_aware_wrapper' uses overly generic type 'Any' for parameter 'func'
- 🔵 **Line 1**: Function 'create_parameter_aware_wrapper' returns overly generic type 'Any'

### src/haive/core/graph/state_graph/models/edge_model.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 38**: Method 'EdgeModel.validate_edge_structure' missing type hints

### src/haive/core/graph/state_graph/models/function_ref.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 29**: Method 'FunctionReference.ensure_valid_reference' missing type hints
- 🔵 **Line 87**: Method 'FunctionReference.resolve' missing type hints
- 🔵 **Line 1**: Function 'FunctionReference.from_callable' uses overly generic type 'Any' for parameter 'callable_obj'

### src/haive/core/graph/state_graph/models/node_model.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 1**: Function 'NodeModel.from_node_spec' uses overly generic type 'Any' for parameter 'node_spec'

### src/haive/core/graph/state_graph/models/state_graph_model.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 68**: Method 'GraphModel.node_count' missing type hints
- 🔵 **Line 74**: Method 'GraphModel.edge_count' missing type hints
- 🔵 **Line 87**: Method 'GraphModel.all_edges' missing type hints
- 🔵 **Line 115**: Method 'GraphModel.validate_graph_structure' missing type hints
- 🔵 **Line 299**: Method 'GraphModel.validate' missing type hints
- 🔵 **Line 1**: Function 'GraphModel.add_node' uses overly generic type 'Any' for parameter 'node_spec'
- 🔵 **Line 1**: Function 'GraphModel.from_state_graph' uses overly generic type 'Any' for parameter 'graph'

### src/haive/core/graph/state_graph/models/branch_model.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 39**: Method 'BranchModel.ensure_valid_branch' missing type hints
- 🔵 **Line 1**: Function 'BranchModel.from_branch' uses overly generic type 'Any' for parameter 'branch'

### src/haive/core/graph/state_graph/pattern/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 63**: Method 'GraphPattern.build' missing type hints
- 🔵 **Line 170**: Method 'GraphPattern.get_source_nodes' missing type hints
- 🔵 **Line 199**: Method 'GraphPattern.register' missing type hints
- 🔵 **Line 237**: Method 'GraphPattern.list_patterns' missing type hints
- 🔵 **Line 1**: Function 'GraphPattern.set_implementation' uses overly generic type 'Any' for parameter 'implementation'

### src/haive/core/graph/state_graph/pattern/implementations.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/core/graph/state_graph/components/node.py

- 🔵 **Line 110**: Method 'Node.display_name' missing type hints
- 🔵 **Line 118**: Method 'Node.to_dict' missing type hints

### src/haive/core/graph/state_graph/components/branch.py

- 🔵 **Line 137**: Method 'Branch.setup_function_and_mappings' missing type hints
- 🔵 **Line 157**: Method 'Branch.validate_destinations_and_default' missing type hints
- 🔵 **Line 1**: Function 'Branch.\_process_result' uses overly generic type 'Any' for parameter 'result'
- 🔵 **Line 1**: Function 'Branch.\_compare' uses overly generic type 'Any' for parameter 'value'

### src/haive/core/graph/state_graph/packages/haive-core/src/haive/core/graph/state_graph/conversion/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/graph/state_graph/packages/haive-core/src/haive/core/graph/state_graph/utils/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/core/graph/state_graph/packages/haive-core/src/haive/core/graph/state_graph/components/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition
