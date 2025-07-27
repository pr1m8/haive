# AutoAPI Fix Baseline - Sun Jul 27 16:18:46 EDT 2025

## Current Build Output

Running Sphinx v8.2.3
2025-07-27 16:19:33,827 - builtins - INFO - Found packages directory: /home/will/Projects/haive/backend/haive/packages
2025-07-27 16:19:33,827 - builtins - INFO - Adding to sys.path: /home/will/Projects/haive/backend/haive/packages/haive-core/src
2025-07-27 16:19:33,829 - builtins - INFO - Successfully imported haive.core
2025-07-27 16:19:33,829 - builtins - INFO - Adding to sys.path: /home/will/Projects/haive/backend/haive/packages/haive-agents/src
2025-07-27 16:19:37,141 - haive.core.persistence.serializers - WARNING - Using unencrypted SecureSecretStrSerializer for PostgreSQL. This is not recommended for production use.
2025-07-27 16:19:37,461 - haive.core.persistence.store.factory - WARNING - PostgresStore not available, falling back to memory store. Install with: pip install langgraph-checkpoint-postgres
2025-07-27 16:19:37,461 - haive.core.graph.node.engine_node - DEBUG - Engine derived input fields: ['messages', 'context']
2025-07-27 16:19:37,464 - haive.core.graph.node.engine_node - DEBUG - Engine derived input fields: ['messages', 'plan_status', 'current_step', 'previous_results']
2025-07-27 16:19:37,465 - haive.core.graph.node.engine_node - DEBUG - Engine derived input fields: ['messages', 'objective', 'plan_progress', 'execution_results']
2025-07-27 16:19:37,479 - haive.core.persistence.serializers - WARNING - Using unencrypted SecureSecretStrSerializer for PostgreSQL. This is not recommended for production use.
2025-07-27 16:19:37,714 - haive.core.persistence.store.factory - WARNING - PostgresStore not available, falling back to memory store. Install with: pip install langgraph-checkpoint-postgres
2025-07-27 16:19:37,714 - haive.core.graph.node.engine_node - DEBUG - Engine derived input fields: ['messages', 'context']
2025-07-27 16:19:37,716 - haive.core.graph.node.engine_node - DEBUG - Engine derived input fields: ['messages', 'plan_status', 'current_step', 'previous_results']
2025-07-27 16:19:37,718 - haive.core.graph.node.engine_node - DEBUG - Engine derived input fields: ['messages', 'objective', 'plan_progress', 'execution_results']
SchemaComposer: SimpleAgentState
└── Ready to compose schema
╭──────── Schema Detection ─────────╮
│ Detecting Base Class Requirements │
│ Components: 0 │
╰───────────────────────────────────╯
2025-07-27 16:19:37,739 - haive.core.persistence.serializers - WARNING - Using unencrypted SecureSecretStrSerializer for PostgreSQL. This is not recommended for production use.
2025-07-27 16:19:37,974 - haive.core.persistence.store.factory - WARNING - PostgresStore not available, falling back to memory store. Install with: pip install langgraph-checkpoint-postgres
2025-07-27 16:19:37,975 - haive.core.graph.node.engine_node - DEBUG - Engine derived input fields: ['messages', 'context']
╭──────────────────── Simple Agent - Recursion Limit Flow ─────────────────────╮
│ ✅ Initial base_config: recursion_limit=100 (from agent.runnable_config or │
│ agent.config.runnable_config) │
╰──────────────────────────────────────────────────────────────────────────────╯
2025-07-27 16:19:39,091 - haive.core.graph.node.engine_node - INFO - ================================================================================
2025-07-27 16:19:39,091 - haive.core.graph.node.engine_node - INFO - ENGINE NODE EXECUTION: agent_node
2025-07-27 16:19:39,091 - haive.core.graph.node.engine_node - INFO - ================================================================================
2025-07-27 16:19:39,091 - haive.core.graph.node.engine_node - DEBUG - Starting execution of node agent_node
2025-07-27 16:19:39,091 - haive.core.graph.node.engine_node - INFO - Step 1: Getting Engine
2025-07-27 16:19:39,091 - haive.core.graph.node.engine_node - DEBUG - Getting engine...
2025-07-27 16:19:39,091 - haive.core.graph.node.engine_node - DEBUG - Using direct engine reference: planner
2025-07-27 16:19:39,091 - haive.core.graph.node.engine_node - INFO - ✅ Got engine: planner (type: llm)
2025-07-27 16:19:39,091 - haive.core.graph.node.engine_node - INFO - Step 2: Extracting Input
2025-07-27 16:19:39,091 - haive.core.graph.node.engine_node - DEBUG - Node input_schema: <class 'haive.core.graph.node.base_config.agent_nodeInput'>
2025-07-27 16:19:39,091 - haive.core.graph.node.engine_node - DEBUG - Node input_field_defs: [<haive.core.schema.field_definition.FieldDefinition object at 0x7f767a4ebcb0>, <haive.core.schema.field_definition.FieldDefinition object at 0x7f767a4ebc20>]
2025-07-27 16:19:39,092 - haive.core.graph.node.engine_node - DEBUG - State fields available: ['add_engine', 'add_engine_route', 'add_message', 'add_messages', 'add_routed_tool', 'add_system_message', 'add_tool', 'add_tool_to_engine', 'add_tools_from_list', 'add_tools_to_category', 'apply_reducers', 'as_table', 'auto_track_all_tokens', 'before_tool_validator', 'calculate_costs', 'clear_messages', 'clear_token_usage', 'clear_tool_routes', 'clear_tools', 'combine_with', 'compare_with', 'configure_engine_routes', 'construct', 'content', 'context', 'context_length', 'context_length_override', 'copy', 'create_input_schema', 'create_output_schema', 'critical_threshold', 'debug_tool_routes', 'decide_next_node', 'deduplicate_tool_calls', 'deep_copy', 'derive_input_schema', 'derive_output_schema', 'dict', 'differences_from', 'display_code', 'display_schema', 'display_table', 'enable_structured_output_parsing', 'engine', 'engine_route_config', 'engines', 'engines_by_type', 'ensure_system_before_human', 'extract_values', 'format_for_structured_output', 'from_dict', 'from_engine', 'from_json', 'from_orm', 'from_partial_dict', 'from_runnable_config', 'from_snapshot', 'get', 'get_all_class_engines', 'get_all_instance_engines', 'get_all_tools_flat', 'get_capacity_status', 'get_class_engine', 'get_completed_tool_calls', 'get_conversation_cost_analysis', 'get_conversation_rounds', 'get_engine', 'get_engine_metadata', 'get_engines', 'get_filtered_messages', 'get_instance_engine', 'get_last_ai_message', 'get_last_human_message', 'get_last_message', 'get_last_token_usage', 'get_last_tool_message', 'get_latest_structured_output', 'get_parsed_tool_calls', 'get_state_values', 'get_structured_model', 'get_system_message', 'get_token_usage', 'get_token_usage_summary', 'get_tool', 'get_tool_by_name', 'get_tool_calls', 'get_tool_metadata', 'get_tool_route', 'get_tool_type', 'get_tools_by_category', 'get_tools_by_route', 'get_tools_by_type', 'has_engine', 'has_tool_calls', 'has_tool_route', 'has_tool_type', 'inject_state_into_tool_calls', 'is_approaching_token_limit', 'is_at_critical_limit', 'is_at_token_limit', 'is_last_message_from_ai', 'is_last_message_from_human', 'is_last_message_from_tool', 'is_real_human_message', 'is_shared', 'is_tool_error', 'json', 'list_engines', 'list_structured_models', 'list_tools_by_route', 'llm', 'main_engine', 'manager', 'merge_engine_output', 'merge_messages', 'messages', 'model_computed_fields', 'model_config', 'model_construct', 'model_copy', 'model_dump', 'model_dump_json', 'model_extra', 'model_fields', 'model_fields_set', 'model_json_schema', 'model_parametrized_name', 'model_post_init', 'model_rebuild', 'model_validate', 'model_validate_json', 'model_validate_strings', 'output_schemas', 'parse_ai_structured_outputs', 'parse_file', 'parse_obj', 'parse_raw', 'parse_structured_outputs', 'patch', 'plan', 'prepare_for_engine', 'pretty_print', 'recalculate_token_usage', 'refresh_tool_routes', 'remaining_tokens', 'remove_engine', 'remove_engine_route', 'remove_tool', 'remove_tool_route', 'routed_tools', 'schema', 'schema_json', 'send_tool_calls', 'set_tool_route', 'set_tool_route_for_existing', 'setup_engines_and_tools', 'setup_primary_engine_references', 'setup_structured_output_parser', 'shared_fields', 'should_summarize_context', 'structured_output_models', 'structured_output_parser', 'sync_engine_fields', 'sync_message_engine_settings', 'sync_tool_routes_from_tools', 'sync_tools_and_update_routes', 'to_command', 'to_dict', 'to_json', 'to_langchain_prompt', 'to_manager', 'to_openai_format', 'to_python_code', 'to_runnable_config', 'to_tool', 'token_usage', 'token_usage_history', 'token_usage_percentage', 'tool_instances', 'tool_metadata', 'tool_routes', 'tool_types', 'tools', 'tools_dict', 'track_message_tokens', 'transform_ai_to_human', 'update', 'update_forward_refs', 'update_tool_route', 'update_tool_routes', 'update_tool_types', 'validate', 'validate_engine', 'validate_engines', 'validate_message_format', 'warning_threshold', 'with_shared_fields', 'with_system_message', 'with_system_message_and_tracking']
2025-07-27 16:19:39,092 - haive.core.graph.node.engine_node - DEBUG - Engine node extracting input from state...
2025-07-27 16:19:39,092 - haive.core.graph.node.engine_node - DEBUG - Schema-based extraction: ['messages', 'context']
2025-07-27 16:19:39,092 - haive.core.graph.node.engine_node - INFO - Using schema-based input extraction: ['messages', 'context']
2025-07-27 16:19:39,092 - haive.core.graph.node.engine_node - DEBUG - Extracted input_data: {'messages': [HumanMessage(content='What is the population of Tokyo and calculate its population density if the area is 2194 km²?', additional_kwargs={}, response_metadata={}, id='eeed875c-cc1a-4727-8a35-d516bd0a882b')], 'context': ''}
2025-07-27 16:19:39,092 - haive.core.graph.node.engine_node - DEBUG - Input data type: dict
2025-07-27 16:19:39,092 - haive.core.graph.node.engine_node - DEBUG - Input keys: ['messages', 'context']
2025-07-27 16:19:39,092 - haive.core.graph.node.engine_node - DEBUG - messages: list = [HumanMessage(content='What is the population of Tokyo and calculate its population density if the a...
2025-07-27 16:19:39,092 - haive.core.graph.node.engine_node - DEBUG - context: str = ...
2025-07-27 16:19:39,093 - haive.core.graph.node.engine_node - INFO - Step 3: Executing Engine
2025-07-27 16:19:39,093 - haive.core.graph.node.engine_node - INFO - 🔍 DETAILED PRE-INVOKE ANALYSIS
2025-07-27 16:19:39,093 - haive.core.graph.node.engine_node - INFO - Engine: planner (type: EngineType.LLM)
2025-07-27 16:19:39,093 - haive.core.graph.node.engine_node - INFO - Input data type: dict
2025-07-27 16:19:39,093 - haive.core.graph.node.engine_node - INFO - Input dict keys: ['messages', 'context']
2025-07-27 16:19:39,093 - haive.core.graph.node.engine_node - INFO - 🔑 messages: list
2025-07-27 16:19:39,093 - haive.core.graph.node.engine_node - INFO - Value: [HumanMessage(content='What is the population of Tokyo and calculate its population density if the area is 2194 km²?', additional_kwargs={}, response_metadata={}, id='eeed875c-cc1a-4727-8a35-d516bd0a882b')]
2025-07-27 16:19:39,093 - haive.core.graph.node.engine_node - INFO - 🔑 context: str
2025-07-27 16:19:39,093 - haive.core.graph.node.engine_node - INFO - Value:
2025-07-27 16:19:39,093 - haive.core.graph.node.engine_node - INFO - 🎯 Engine has prompt_template: ChatPromptTemplate
2025-07-27 16:19:39,094 - haive.core.graph.node.engine_node - INFO - Required input_variables: []
2025-07-27 16:19:39,094 - haive.core.graph.node.engine_node - INFO - Optional variables: ['messages']
2025-07-27 16:19:39,094 - haive.core.graph.node.engine_node - INFO - Partial variables: ['messages', 'context']
2025-07-27 16:19:39,094 - haive.core.graph.node.engine_node - INFO - 📦 Extra input keys (not in template): ['context']
2025-07-27 16:19:39,094 - haive.core.graph.node.engine_node - INFO - ✅ Available template variables: []
2025-07-27 16:19:39,094 - haive.core.graph.node.engine_node - INFO - Merged config keys: ['metadata', 'recursion_limit', 'configurable', 'callbacks']
2025-07-27 16:19:39,094 - haive.core.graph.node.engine_node - INFO - 🚀 CALLING engine.invoke() NOW...
2025-07-27 16:19:39,094 - haive.core.graph.node.engine_node - DEBUG - Standard engine invoke
2025-07-27 16:19:39,095 - haive.core.engine.aug_llm.factory - WARNING - Added messages to optional_variables during runnable creation
2025-07-27 16:19:42,052 - haive.core.graph.node.engine_node - DEBUG - Result type: AIMessage
2025-07-27 16:19:42,052 - haive.core.graph.node.engine_node - INFO - ✅ Result is a AIMessage
2025-07-27 16:19:42,052 - haive.core.graph.node.engine_node - DEBUG - Content: ...
2025-07-27 16:19:42,052 - haive.core.graph.node.engine_node - DEBUG - Tool Calls: 1
2025-07-27 16:19:42,053 - haive.core.graph.node.engine_node - DEBUG - Result: content='' additional_kwargs={'tool_calls': [{'id': 'call_Ndxt9xr9nsa5eEbXOPEveRRd', 'function': {'arguments': '{"objective":"Determine the population density of Tokyo using current population data an...
2025-07-27 16:19:42,053 - haive.core.graph.node.engine_node - INFO - Step 4: Creating Update
2025-07-27 16:19:42,053 - haive.core.graph.node.engine_node - INFO - Using schema-based output creation: ['messages', 'engine_name']
2025-07-27 16:19:42,053 - haive.core.graph.node.engine_node - INFO - Final Update:
2025-07-27 16:19:42,053 - haive.core.graph.node.engine_node - INFO - ✅ ENGINE NODE COMPLETED: agent_node
2025-07-27 16:19:42,055 - haive.core.graph.node.validation_node_config_v2 - WARNING - Engine not found: planner
2025-07-27 16:19:42,297 - haive.agents.base.mixins.execution_mixin - WARNING - Error validating output with schema: 1 validation error for Simple AgentOutput
plan
Field required [type=missing, input_value={'messages': [HumanMessag...veRRd')], 'context': ''}, input_type=dict]
For further information visit https://errors.pydantic.dev/2.11/v/missing
2025-07-27 16:19:54,130 - numexpr.utils - INFO - NumExpr defaulting to 12 threads.
2025-07-27 16:19:56,134 - builtins - WARNING - Failed to import haive.agents: Expected a list of types, an ellipsis, ParamSpec, or Concatenate. Got ~P
2025-07-27 16:19:56,134 - builtins - INFO - Adding to sys.path: /home/will/Projects/haive/backend/haive/packages/haive-tools/src
2025-07-27 16:19:57,432 - builtins - WARNING - Failed to import haive.tools: google-search-results is not installed. Please install it with `pip install google-search-results>=2.4.2`
2025-07-27 16:19:57,433 - builtins - INFO - Adding to sys.path: /home/will/Projects/haive/backend/haive/packages/haive-games/src
2025-07-27 16:19:57,434 - builtins - INFO - Successfully imported haive.games
2025-07-27 16:19:57,434 - builtins - INFO - Adding to sys.path: /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src
2025-07-27 16:19:57,462 - builtins - INFO - Successfully imported haive.dataflow
2025-07-27 16:19:57,462 - builtins - INFO - Adding to sys.path: /home/will/Projects/haive/backend/haive/packages/haive-mcp/src
2025-07-27 16:19:57,489 - builtins - INFO - Successfully imported haive.mcp
loading translations [en]... done
WARNING: while setting up extension sphinx_tabs: extension 'sphinx_tabs' has no setup() function; is it really a Sphinx extension module?
WARNING: while setting up extension sphinx_gallery: extension 'sphinx_gallery' has no setup() function; is it really a Sphinx extension module?
2025-07-27 16:19:59,093 - builtins - INFO - Running optimized Sphinx setup function
loading pickled environment... The configuration has changed (16 options: 'autoapi_dirs', 'autoapi_ignore', 'autoapi_options', 'autoapi_prepare_jinja_env', 'epub_css_files', ...)
done
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/rich_logger_mixin.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/checkpointer_mixin.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/.ipynb_checkpoints/supabase_config-checkpoint.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/embeddings/test_embeddings.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/haive_discovery/discovery_engine.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/haive_discovery/base_analyzer.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/haive_discovery/retriever_analyzers.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/haive_discovery/**init**.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/haive_discovery/tool_analyzers.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/haive_discovery/documentation_writer.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/haive_discovery/utils.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/haive_discovery/haive_discovery.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/haive_discovery/engine_analyzer.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/haive_discovery/component_info.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/examples.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/examples/minimal_example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/examples/universal_loader_demo.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/.ipynb_checkpoints/agent-checkpoint.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/validation_routing_example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/messages/examples.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/examples.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/practical_stateful_example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/stateful_integration_example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/engine_node_test.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/test_modular_graph.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/demo_modular_benefits.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/cli.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/examples/run_with_visualization.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/examples/**init**.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/examples/run_from_file.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/examples/batch_research.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/examples/simple_research.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/debug_utils.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/example_integrated.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/example_dynamic_supervisor.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/example_delegation.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/simple_test.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/example_dynamic.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/examples.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/examples_simple.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/sequential/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/.ipynb_checkpoints/**init**-checkpoint.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo/tests/**init**.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo/tests/test_join_step.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo/tests/test_basic.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo/tests/test_tool_step.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler_v3/examples/basic_example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/p_and_e/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler/aug_llms.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/debug.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/.ipynb_checkpoints/**init**-checkpoint.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/.ipynb_checkpoints/agent-checkpoint.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/list_iteration_example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/llm_rag/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_loader/tests/**init**.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_loader/examples/**init**.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_loader/examples/usage_examples.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/archive/meta/agent.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/aug_llms.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/aug_llms.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/aug_llms.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/v2/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/modular/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/mcts/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v3/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/example3.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/example2.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/aug_llms.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/debug.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent/aug_llms.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v2/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/tnt/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/iterative_refinement/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/map_branch/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_base/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/archive/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/test_proper_usage.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/implementations/debug_with_logging.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_processing/examples/comprehensive_query_example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/collaberative/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/base/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/base/examples/basic_state_management.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/round_robin/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/debate/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/directed/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/social_media/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/aug_llms.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/interview/aug_llms.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/test_advanced_rag_memory_agent.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/test_input_prep.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/test_simple_memory_with_deepseek.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/test_react_memory_coordinator.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/test_with_free_resources.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/test_graph_memory_simple.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/test_simple_minimal.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/test_simple_memory_agent_fixed.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/test_deepseek_integration.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/test_multi_memory_agent.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/test_with_deepseek.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/test_graph_memory_agent.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/test_simple_debug.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/test_complete_memory_system.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/test_react_memory_agent.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/test_memory_models_only.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/test_simple_components.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/test_memory_operations.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/self_healing_code/agent.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/logger.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/main.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/app.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/main.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/example_tool.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/main.py
[AutoAPI] Ignoring directory: /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/bin/**pycache**/
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/bin/litellm_cli.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/registries/main.py
[AutoAPI] Ignoring directory: /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/bin/**pycache**/
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/bin/registry_cli.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/bin/vault_cli.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/bin/litellm_cli.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registries/main.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/demo.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/aug_llms.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/enhanced_example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/aug_llms.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/tic_tac_toe/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/example_with_judges.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/simple_test.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/test_judges.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/demo.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/example_configurable.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/api_example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/aug_llms.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/example_configurable_players.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/debug_schema.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/api_client_example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/blackjack/state_manager.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/blackjack/config.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/blackjack/models.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/blackjack/factory.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/blackjack/**init**.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/blackjack/agent.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/utils/test_helpers.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/debug.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate/test_topic_handling.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/enhanced_example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/go/aug_llms.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/go/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/reversi/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/risk/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/wordle/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/flow_free/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/debug.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/haive_agent_mcp_integration.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/test_direct.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/complete_mcp_example.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/test_vectorstore.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/cli.py
[AutoAPI] Ignoring file: /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/servers/example_server_fastmcp.py
[AutoAPI] Reading files... [ 0%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/errors.py
[AutoAPI] Reading files... [ 0%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/**init**.py
[AutoAPI] Reading files... [ 0%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/**init**.py
[AutoAPI] Reading files... [ 0%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/logging_config.py
[AutoAPI] Reading files... [ 0%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/**init**.py
[AutoAPI] Reading files... [ 0%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/dynamic_choice_model.py
[AutoAPI] Reading files... [ 0%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/named_list.py
[AutoAPI] Reading files... [ 0%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/documents/**init**.py
[AutoAPI] Reading files... [ 0%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/documents/github_repo.py
[AutoAPI] Reading files... [ 0%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/structures/tree.py
[AutoAPI] Reading files... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/structures/named_dict.py
[AutoAPI] Reading files... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/timestamp_mixin.py
[AutoAPI] Reading files... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/mcp_mixin.py
[AutoAPI] Reading files... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/recompile_mixin.py
[AutoAPI] Reading files... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/engine_mixin.py
[AutoAPI] Reading files... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/structured_output_mixin.py
[AutoAPI] Reading files... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/tool_route_mixin.py
[AutoAPI] Reading files... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/getter_mixin.py
[AutoAPI] Reading files... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/**init**.py
[AutoAPI] Reading files... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/prompt_template_mixin.py
[AutoAPI] Reading files... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/tool_list_mixin.py
[AutoAPI] Reading files... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/identifier.py
[AutoAPI] Reading files... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/secure_config.py
[AutoAPI] Reading files... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/dynamic_tool_route_mixin.py
[AutoAPI] Reading files... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/state_interface_mixin.py
[AutoAPI] Reading files... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/general/state.py
[AutoAPI] Reading files... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/general/id.py
[AutoAPI] Reading files... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/general/**init**.py
[AutoAPI] Reading files... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/general/metadata.py
[AutoAPI] Reading files... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/general/timestamp.py
[AutoAPI] Reading files... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/general/serialization.py
[AutoAPI] Reading files... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/general/version.py
[AutoAPI] Reading files... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/mixins/**init**.py
[AutoAPI] Reading files... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/types/abc_root_wrapper.py
[AutoAPI] Reading files... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/types/general.py
[AutoAPI] Reading files... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/types/**init**.py
[AutoAPI] Reading files... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/types/protocols/general_protocols.py
[AutoAPI] Reading files... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/types/protocols/**init**.py
[AutoAPI] Reading files... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/types/protocols/schema_protocols.py
[AutoAPI] Reading files... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/types/protocols/engine_protocols.py
[AutoAPI] Reading files... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/base.py
[AutoAPI] Reading files... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/memory.py
[AutoAPI] Reading files... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/factory.py
[AutoAPI] Reading files... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/sqlite_config.py
[AutoAPI] Reading files... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/postgres_saver_override.py
[AutoAPI] Reading files... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/**init**.py
[AutoAPI] Reading files... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/handlers.py
[AutoAPI] Reading files... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/serializers.py
[AutoAPI] Reading files... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/utils.py
[AutoAPI] Reading files... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/types.py
[AutoAPI] Reading files... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/postgres_config.py
[AutoAPI] Reading files... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/postgres_saver_with_thread_creation.py
[AutoAPI] Reading files... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/supabase_config.py
[AutoAPI] Reading files... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/base.py
[AutoAPI] Reading files... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/connection.py
[AutoAPI] Reading files... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/memory.py
[AutoAPI] Reading files... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/factory.py
[AutoAPI] Reading files... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/postgres.py
[AutoAPI] Reading files... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/**init**.py
[AutoAPI] Reading files... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/types.py
[AutoAPI] Reading files... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/embeddings.py
[AutoAPI] Reading files... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/wrappers/memory.py
[AutoAPI] Reading files... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/wrappers/postgres.py
[AutoAPI] Reading files... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/wrappers/**init**.py
[AutoAPI] Reading files... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/**init**.py
[AutoAPI] Reading files... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/metadata_mixin.py
[AutoAPI] Reading files... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/metadata.py
[AutoAPI] Reading files... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/export_llm_models_to_csv.py
[AutoAPI] Reading files... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/base.py
[AutoAPI] Reading files... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/factory.py
[AutoAPI] Reading files... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/rate_limiting_mixin.py
[AutoAPI] Reading files... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/**init**.py
[AutoAPI] Reading files... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/provider_types.py
[AutoAPI] Reading files... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers.py
[AutoAPI] Reading files... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/together.py
[AutoAPI] Reading files... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/cohere.py
[AutoAPI] Reading files... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/anthropic.py
[AutoAPI] Reading files... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/base.py
[AutoAPI] Reading files... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/openai.py
[AutoAPI] Reading files... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/fireworks.py
[AutoAPI] Reading files... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/mistral.py
[AutoAPI] Reading files... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/groq.py
[AutoAPI] Reading files... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/xai.py
[AutoAPI] Reading files... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/**init**.py
[AutoAPI] Reading files... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/ollama.py
[AutoAPI] Reading files... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/huggingface.py
[AutoAPI] Reading files... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/azure.py
[AutoAPI] Reading files... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/bedrock.py
[AutoAPI] Reading files... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/ai21.py
[AutoAPI] Reading files... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/replicate.py
[AutoAPI] Reading files... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/google.py
[AutoAPI] Reading files... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/nvidia.py
[AutoAPI] Reading files... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/embeddings/base.py
[AutoAPI] Reading files... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/embeddings/**init**.py
[AutoAPI] Reading files... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/embeddings/provider_types.py
[AutoAPI] Reading files... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/embeddings/filter/base.py
[AutoAPI] Reading files... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/embeddings/filter/**init**.py
[AutoAPI] Reading files... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/vectorstore/base.py
[AutoAPI] Reading files... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/vectorstore/**init**.py
[AutoAPI] Reading files... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/retriever/base.py
[AutoAPI] Reading files... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/retriever/asknews_retriever.py
[AutoAPI] Reading files... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/retriever/vectorstore_retriever.py
[AutoAPI] Reading files... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/retriever/**init**.py
[AutoAPI] Reading files... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/retriever/community/base.py
[AutoAPI] Reading files... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/retriever/retrievers/time_weighted.py
[AutoAPI] Reading files... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/retriever/retrievers/parent_document.py
[AutoAPI] Reading files... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/retriever/retrievers/self_query.py
[AutoAPI] Reading files... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/retriever/retrievers/multiqery.py
[AutoAPI] Reading files... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/retriever/retrievers/ensemble.py
[AutoAPI] Reading files... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/registry/base.py
[AutoAPI] Reading files... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/registry/memory.py
[AutoAPI] Reading files... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/registry/factory.py
[AutoAPI] Reading files... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/registry/**init**.py
[AutoAPI] Reading files... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/registry/decorators.py
[AutoAPI] Reading files... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/registry/dynamic_registry.py
[AutoAPI] Reading files... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/registry/manager.py
[AutoAPI] Reading files... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/tools/store_tools.py
[AutoAPI] Reading files... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/tools/interrupt_tool_wrapper.py
[AutoAPI] Reading files... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/tools/store_manager.py
[AutoAPI] Reading files... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/tools/**init**.py
[AutoAPI] Reading files... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/runtime/**init**.py
[AutoAPI] Reading files... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/runtime/base/base.py
[AutoAPI] Reading files... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/runtime/base/protocols.py
[AutoAPI] Reading files... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/runtime/extension/base.py
[AutoAPI] Reading files... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/runtime/extension/protocols.py
[AutoAPI] Reading files... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/config.py
[AutoAPI] Reading files... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/model_utils.py
[AutoAPI] Reading files... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/parser_utils.py
[AutoAPI] Reading files... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/tool_utils.py
[AutoAPI] Reading files... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/file_utils.py
[AutoAPI] Reading files... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/config_utils.py
[AutoAPI] Reading files... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/inspection.py
[AutoAPI] Reading files... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/getter_mixin.py
[AutoAPI] Reading files... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/mermaid_utils.py
[AutoAPI] Reading files... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/collections.py
[AutoAPI] Reading files... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/**init**.py
[AutoAPI] Reading files... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/chat_utils.py
[AutoAPI] Reading files... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/runnable_config_utils.py
[AutoAPI] Reading files... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/visualize_graph_utils.py
[AutoAPI] Reading files... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/tool_list.py
[AutoAPI] Reading files... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/message_utils.py
[AutoAPI] Reading files... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/logging_utils.py
[AutoAPI] Reading files... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/env_utils.py
[AutoAPI] Reading files... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/state_utils.py
[AutoAPI] Reading files... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/doc_utils.py
[AutoAPI] Reading files... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/interrupt_utils.py
[AutoAPI] Reading files... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/serialization.py
[AutoAPI] Reading files... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/pydantic_utils/ui.py
[AutoAPI] Reading files... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/pydantic_utils/general.py
[AutoAPI] Reading files... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/pydantic_utils/**init**.py
[AutoAPI] Reading files... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/pydantic_utils/sync_properties.py
[AutoAPI] Reading files... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/tools/**init**.py
[AutoAPI] Reading files... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/tools/tool_schema_generator.py
[AutoAPI] Reading files... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/types/tree_leaf.py
[AutoAPI] Reading files... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/types/dynamic_enum.py
[AutoAPI] Reading files... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/types/serializable_callable.py
[AutoAPI] Reading files... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/types/**init**.py
[AutoAPI] Reading files... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/types/advanced_registry.py
[AutoAPI] Reading files... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/types/dynamic_literal.py
[AutoAPI] Reading files... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/types/general/file_types.py
[AutoAPI] Reading files... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/types/general/**init**.py
[AutoAPI] Reading files... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/types/general/programming_languages.py
[AutoAPI] Reading files... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/**init**.py
[AutoAPI] Reading files... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embeddings.py
[AutoAPI] Reading files... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py
[AutoAPI] Reading files... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/factory.py
[AutoAPI] Reading files... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/mcp_config.py
[AutoAPI] Reading files... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/**init**.py
[AutoAPI] Reading files... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/utils.py
[AutoAPI] Reading files... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/base/base.py
[AutoAPI] Reading files... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/base/factory.py
[AutoAPI] Reading files... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/base/protocols.py
[AutoAPI] Reading files... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/base/registry.py
[AutoAPI] Reading files... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/base/**init**.py
[AutoAPI] Reading files... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/base/types.py
[AutoAPI] Reading files... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/base/reference.py
[AutoAPI] Reading files... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/universal_loader.py
[AutoAPI] Reading files... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/config.py
[AutoAPI] Reading files... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/factory.py
[AutoAPI] Reading files... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/**init**.py
[AutoAPI] Reading files... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/engine.py
[AutoAPI] Reading files... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/processors.py
[AutoAPI] Reading files... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/agents.py
[AutoAPI] Reading files... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/path_analysis.py
[AutoAPI] Reading files... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/transformers/base.py
[AutoAPI] Reading files... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/transformers/**init**.py
[AutoAPI] Reading files... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/transformers/engine.py
[AutoAPI] Reading files... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/transformers/types.py
[AutoAPI] Reading files... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/base/schema.py
[AutoAPI] Reading files... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/base/**init**.py
[AutoAPI] Reading files... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/sources/base.py
[AutoAPI] Reading files... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/sources/**init**.py
[AutoAPI] Reading files... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/sources/web.py
[AutoAPI] Reading files... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/sources/local.py
[AutoAPI] Reading files... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/cache_manager.py
[AutoAPI] Reading files... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/base.py
[AutoAPI] Reading files... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/strategy.py
[AutoAPI] Reading files... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/path_analyzer.py
[AutoAPI] Reading files... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/registry.py
[AutoAPI] Reading files... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/**init**.py
[AutoAPI] Reading files... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/source_base.py
[AutoAPI] Reading files... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/engine.py
[AutoAPI] Reading files... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/auto_loader.py
[AutoAPI] Reading files... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/base_new.py
[AutoAPI] Reading files... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/auto_registry.py
[AutoAPI] Reading files... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/auto_factory.py
[AutoAPI] Reading files... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/base/base.py
[AutoAPI] Reading files... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/base/schema.py
[AutoAPI] Reading files... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/base/**init**.py
[AutoAPI] Reading files... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/base/methods.py
[AutoAPI] Reading files... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/adapters/base.py
[AutoAPI] Reading files... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/adapters/**init**.py
[AutoAPI] Reading files... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/adapters/local.py
[AutoAPI] Reading files... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/web_huggingface_enhanced.py
[AutoAPI] Reading files... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/files_scientific.py
[AutoAPI] Reading files... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/web_advanced.py
[AutoAPI] Reading files... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/web_social.py
[AutoAPI] Reading files... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/file_advanced.py
[AutoAPI] Reading files... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/**init**.py
[AutoAPI] Reading files... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/cloud.py
[AutoAPI] Reading files... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/database_advanced.py
[AutoAPI] Reading files... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/web_github_enhanced.py
[AutoAPI] Reading files... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/files_text.py
[AutoAPI] Reading files... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/services.py
[AutoAPI] Reading files... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/database.py
[AutoAPI] Reading files... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/web_api.py
[AutoAPI] Reading files... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/files_office.py
[AutoAPI] Reading files... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/web.py
[AutoAPI] Reading files... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/files_code.py
[AutoAPI] Reading files... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/files_data.py
[AutoAPI] Reading files... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/files_media.py
[AutoAPI] Reading files... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/chat_gpt_loader.py
[AutoAPI] Reading files... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/final_missing_source.py
[AutoAPI] Reading files... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/analytics_sources.py
[AutoAPI] Reading files... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/factory.py
[AutoAPI] Reading files... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/implementation.py
[AutoAPI] Reading files... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/file_sources.py
[AutoAPI] Reading files... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/final_sources.py
[AutoAPI] Reading files... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/enhanced_registry.py
[AutoAPI] Reading files... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/additional_sources.py
[AutoAPI] Reading files... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/completion_sources.py
[AutoAPI] Reading files... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/messaging_sources.py
[AutoAPI] Reading files... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/web_sources.py
[AutoAPI] Reading files... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/registry.py
[AutoAPI] Reading files... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/**init**.py
[AutoAPI] Reading files... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/source_types.py
[AutoAPI] Reading files... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/essential_sources.py
[AutoAPI] Reading files... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/groups.py
[AutoAPI] Reading files... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/communication_sources.py
[AutoAPI] Reading files... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/cloud_storage_sources.py
[AutoAPI] Reading files... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/source_base.py
[AutoAPI] Reading files... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/source_analysis.py
[AutoAPI] Reading files... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/extended_sources.py
[AutoAPI] Reading files... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/business_sources.py
[AutoAPI] Reading files... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/specialized_sources.py
[AutoAPI] Reading files... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/bulk_sources.py
[AutoAPI] Reading files... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/database_sources.py
[AutoAPI] Reading files... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/base.py
[AutoAPI] Reading files... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/blackboard_source.py
[AutoAPI] Reading files... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/youtube_audio_source.py
[AutoAPI] Reading files... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/ifixit_source.py
[AutoAPI] Reading files... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/college_confidential.py
[AutoAPI] Reading files... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/wikipedia_source.py
[AutoAPI] Reading files... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/imsdb_source.py
[AutoAPI] Reading files... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/**init**.py
[AutoAPI] Reading files... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/bilibili_source.py
[AutoAPI] Reading files... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/youtube_source.py
[AutoAPI] Reading files... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/hacker_news_source.py
[AutoAPI] Reading files... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/arxiv_source.py
[AutoAPI] Reading files... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/az_lyrics_source.py
[AutoAPI] Reading files... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/read_the_docs_source.py
[AutoAPI] Reading files... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/diffbot_source.py
[AutoAPI] Reading files... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/base/base.py
[AutoAPI] Reading files... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/base/**init**.py
[AutoAPI] Reading files... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/chat/base.py
[AutoAPI] Reading files... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/chat/**init**.py
[AutoAPI] Reading files... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/database/**init**.py
[AutoAPI] Reading files... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/database/types.py
[AutoAPI] Reading files... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/json_source.py
[AutoAPI] Reading files... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/yaml_source.py
[AutoAPI] Reading files... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/base.py
[AutoAPI] Reading files... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/rtf_source.py
[AutoAPI] Reading files... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/docx_source.py
[AutoAPI] Reading files... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/ppt_source.py
[AutoAPI] Reading files... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/txt_source.py
[AutoAPI] Reading files... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/srt_source.py
[AutoAPI] Reading files... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/enex_source.py
[AutoAPI] Reading files... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/git_source.py
[AutoAPI] Reading files... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/mhtml_source.py
[AutoAPI] Reading files... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/pdf.py
[AutoAPI] Reading files... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/**init**.py
[AutoAPI] Reading files... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/html_source.py
[AutoAPI] Reading files... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/md_source.py
[AutoAPI] Reading files... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/pdf_source.py
[AutoAPI] Reading files... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/python_source.py
[AutoAPI] Reading files... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/toml_source.py
[AutoAPI] Reading files... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/csv_source.py
[AutoAPI] Reading files... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/excel_source.py
[AutoAPI] Reading files... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/types.py
[AutoAPI] Reading files... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/notebook_source.py
[AutoAPI] Reading files... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/bibtex_source.py
[AutoAPI] Reading files... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/vsdx_source.py
[AutoAPI] Reading files... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/xml_source.py
[AutoAPI] Reading files... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/xlsx_source.py
[AutoAPI] Reading files... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/rst_source.py
[AutoAPI] Reading files... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/chm_source.py
[AutoAPI] Reading files... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/odt_source.py
[AutoAPI] Reading files... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/xls_source.py
[AutoAPI] Reading files... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/markdown_source.py
[AutoAPI] Reading files... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/epub_source.py
[AutoAPI] Reading files... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/programming_languages/**init**.py
[AutoAPI] Reading files... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/utils/**init**.py
[AutoAPI] Reading files... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/base.py
[AutoAPI] Reading files... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/config.py
[AutoAPI] Reading files... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/**init**.py
[AutoAPI] Reading files... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/engine.py
[AutoAPI] Reading files... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/types/**init**.py
[AutoAPI] Reading files... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/types/enums.py
[AutoAPI] Reading files... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/base.py
[AutoAPI] Reading files... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/**init**.py
[AutoAPI] Reading files... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/types.py
[AutoAPI] Reading files... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/discovery.py
[AutoAPI] Reading files... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/vectorstore.py
[AutoAPI] Reading files... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/ZillizVectorStoreConfig.py
[AutoAPI] Reading files... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/ClickHouseVectorStoreConfig.py
[AutoAPI] Reading files... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/MongoDBAtlasVectorStoreConfig.py
[AutoAPI] Reading files... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/InMemoryVectorStoreConfig.py
[AutoAPI] Reading files... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/VectaraVectorStoreConfig.py
[AutoAPI] Reading files... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/ElasticsearchVectorStoreConfig.py
[AutoAPI] Reading files... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/USearchVectorStoreConfig.py
[AutoAPI] Reading files... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/WeaviateVectorStoreConfig.py
[AutoAPI] Reading files... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/MarqoVectorStoreConfig.py
[AutoAPI] Reading files... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/**init**.py
[AutoAPI] Reading files... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/PGVectorStoreConfig.py
[AutoAPI] Reading files... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/AnnoyVectorStoreConfig.py
[AutoAPI] Reading files... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/SupabaseVectorStoreConfig.py
[AutoAPI] Reading files... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/CassandraVectorStoreConfig.py
[AutoAPI] Reading files... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/AzureSearchVectorStoreConfig.py
[AutoAPI] Reading files... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/OpenSearchVectorStoreConfig.py
[AutoAPI] Reading files... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/PineconeVectorStoreConfig.py
[AutoAPI] Reading files... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/ChromaVectorStoreConfig.py
[AutoAPI] Reading files... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/AmazonOpenSearchVectorStoreConfig.py
[AutoAPI] Reading files... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/Neo4jVectorStoreConfig.py
[AutoAPI] Reading files... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/QdrantVectorStoreConfig.py
[AutoAPI] Reading files... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/TypesenseVectorStoreConfig.py
[AutoAPI] Reading files... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/DocArrayVectorStoreConfig.py
[AutoAPI] Reading files... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/LanceDBVectorStoreConfig.py
[AutoAPI] Reading files... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/MilvusVectorStoreConfig.py
[AutoAPI] Reading files... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/RedisVectorStoreConfig.py
[AutoAPI] Reading files... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/FAISSVectorStoreConfig.py
[AutoAPI] Reading files... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/SKLearnVectorStoreConfig.py
[AutoAPI] Reading files... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/**init**.py
[AutoAPI] Reading files... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/mixins.py
[AutoAPI] Reading files... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/types.py
[AutoAPI] Reading files... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/retriever.py
[AutoAPI] Reading files... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/EnsembleRetrieverConfig.py
[AutoAPI] Reading files... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/BedrockRetrieverConfig.py
[AutoAPI] Reading files... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/TFIDFRetrieverConfig.py
[AutoAPI] Reading files... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/YouRetrieverConfig.py
[AutoAPI] Reading files... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/GoogleDocumentAIWarehouseRetrieverConfig.py
[AutoAPI] Reading files... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/MultiVectorRetrieverConfig.py
[AutoAPI] Reading files... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/ZepCloudRetrieverConfig.py
[AutoAPI] Reading files... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/AzureAISearchRetrieverConfig.py
[AutoAPI] Reading files... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/ContextualCompressionRetrieverConfig.py
[AutoAPI] Reading files... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/MilvusRetrieverConfig.py
[AutoAPI] Reading files... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/GoogleVertexAISearchRetrieverConfig.py
[AutoAPI] Reading files... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/PineconeHybridSearchRetrieverConfig.py
[AutoAPI] Reading files... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/KNNRetrieverConfig.py
[AutoAPI] Reading files... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/ChatGPTPluginRetrieverConfig.py
[AutoAPI] Reading files... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/TimeWeightedVectorStoreRetrieverConfig.py
[AutoAPI] Reading files... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/SVMRetrieverConfig.py
[AutoAPI] Reading files... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/SelfQueryRetrieverConfig.py
[AutoAPI] Reading files... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/WeaviateHybridSearchRetrieverConfig.py
[AutoAPI] Reading files... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/ElasticsearchRetrieverConfig.py
[AutoAPI] Reading files... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/**init**.py
[AutoAPI] Reading files... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/MergerRetrieverConfig.py
[AutoAPI] Reading files... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/WikipediaRetrieverConfig.py
[AutoAPI] Reading files... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/TavilySearchAPIRetrieverConfig.py
[AutoAPI] Reading files... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/AmazonKnowledgeBasesRetrieverConfig.py
[AutoAPI] Reading files... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/AskNewsRetrieverConfig.py
[AutoAPI] Reading files... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/ZepRetrieverConfig.py
[AutoAPI] Reading files... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/MultiQueryRetrieverConfig.py
[AutoAPI] Reading files... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/ParentDocumentRetrieverConfig.py
[AutoAPI] Reading files... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/VespaRetrieverConfig.py
[AutoAPI] Reading files... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/LlamaIndexRetrieverConfig.py
[AutoAPI] Reading files... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/ArceeRetrieverConfig.py
[AutoAPI] Reading files... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/NeuralDBRetrieverConfig.py
[AutoAPI] Reading files... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/CohereRagRetrieverConfig.py
[AutoAPI] Reading files... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/DocArrayRetrieverConfig.py
[AutoAPI] Reading files... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/QdrantSparseVectorRetrieverConfig.py
[AutoAPI] Reading files... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/LlamaIndexGraphRetrieverConfig.py
[AutoAPI] Reading files... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/BM25RetrieverConfig.py
[AutoAPI] Reading files... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/RePhraseQueryRetrieverConfig.py
[AutoAPI] Reading files... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/MetalRetrieverConfig.py
[AutoAPI] Reading files... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/KendraRetrieverConfig.py
[AutoAPI] Reading files... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/PubMedRetrieverConfig.py
[AutoAPI] Reading files... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/ArxivRetrieverConfig.py
[AutoAPI] Reading files... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/WebResearchRetrieverConfig.py
[AutoAPI] Reading files... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/RemoteLangChainRetrieverConfig.py
[AutoAPI] Reading files... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/pattern.py
[AutoAPI] Reading files... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/config.py
[AutoAPI] Reading files... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/protocols.py
[AutoAPI] Reading files... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/registry.py
[AutoAPI] Reading files... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/**init**.py
[AutoAPI] Reading files... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py
[AutoAPI] Reading files... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/integration.py
[AutoAPI] Reading files... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/base.py
[AutoAPI] Reading files... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/factory.py
[AutoAPI] Reading files... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/**init**.py
[AutoAPI] Reading files... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/handlers.py
[AutoAPI] Reading files... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/memory_config.py
[AutoAPI] Reading files... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/types.py
[AutoAPI] Reading files... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/postgres_config.py
[AutoAPI] Reading files... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/manager.py
[AutoAPI] Reading files... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/mongodb_config.py
[AutoAPI] Reading files... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/utils/**init**.py
[AutoAPI] Reading files... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/utils/state_handling.py
[AutoAPI] Reading files... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/utils/input_handling.py
[AutoAPI] Reading files... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/base.py
[AutoAPI] Reading files... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/config.py
[AutoAPI] Reading files... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/**init**.py
[AutoAPI] Reading files... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/types.py
[AutoAPI] Reading files... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/OllamaEmbeddingConfig.py
[AutoAPI] Reading files... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/AzureOpenAIEmbeddingConfig.py
[AutoAPI] Reading files... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/**init**.py
[AutoAPI] Reading files... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/FakeEmbeddingConfig.py
[AutoAPI] Reading files... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/OpenAIEmbeddingConfig.py
[AutoAPI] Reading files... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/GoogleVertexAIEmbeddingConfig.py
[AutoAPI] Reading files... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/CohereEmbeddingConfig.py
[AutoAPI] Reading files... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/HuggingFaceEmbeddingConfig.py
[AutoAPI] Reading files... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/prompt_template/**init**.py
[AutoAPI] Reading files... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/prompt_template/prompt_engine.py
[AutoAPI] Reading files... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/output_parser/base.py
[AutoAPI] Reading files... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/output_parser/**init**.py
[AutoAPI] Reading files... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/output_parser/types.py
[AutoAPI] Reading files... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/tool/base.py
[AutoAPI] Reading files... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/tool/**init**.py
[AutoAPI] Reading files... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/config/auth_runnable.py
[AutoAPI] Reading files... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/config/protocols.py
[AutoAPI] Reading files... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/config/**init**.py
[AutoAPI] Reading files... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/config/constants.py
[AutoAPI] Reading files... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/config/runnable.py
[AutoAPI] Reading files... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/agent_schema_composer.py
[AutoAPI] Reading files... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/state_schema.py
[AutoAPI] Reading files... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/schema_composer.py
[AutoAPI] Reading files... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/ui.py
[AutoAPI] Reading files... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/meta_agent_state.py
[AutoAPI] Reading files... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/schema_manager.py
[AutoAPI] Reading files... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/**init**.py
[AutoAPI] Reading files... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/utils.py
[AutoAPI] Reading files... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/multi_agent_state_schema.py
[AutoAPI] Reading files... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/field_registry.py
[AutoAPI] Reading files... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/preserve_messages_reducer.py
[AutoAPI] Reading files... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/engine_io_mixin.py
[AutoAPI] Reading files... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/base_state_schemas.py
[AutoAPI] Reading files... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/field_utils.py
[AutoAPI] Reading files... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/typed_state_schema.py
[AutoAPI] Reading files... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/field_extractor.py
[AutoAPI] Reading files... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/field_definition.py
[AutoAPI] Reading files... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/composer/schema_composer.py
[AutoAPI] Reading files... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/composer/**init**.py
[AutoAPI] Reading files... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/composer/\_base.py
[AutoAPI] Reading files... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/composer/engine/engine_detector.py
[AutoAPI] Reading files... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/composer/engine/**init**.py
[AutoAPI] Reading files... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/composer/engine/engine_manager.py
[AutoAPI] Reading files... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/composer/field/**init**.py
[AutoAPI] Reading files... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/composer/field/field_manager.py
[AutoAPI] Reading files... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/flexible_multi_agent_state.py
[AutoAPI] Reading files... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/query_state.py
[AutoAPI] Reading files... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/tool_state_with_validation.py
[AutoAPI] Reading files... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/**init**.py
[AutoAPI] Reading files... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/messages_state.py
[AutoAPI] Reading files... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/structured_output_state.py
[AutoAPI] Reading files... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/validation_aware_tool_state.py
[AutoAPI] Reading files... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/multi_agent_state.py
[AutoAPI] Reading files... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/dynamic_activation_state.py
[AutoAPI] Reading files... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/document_state.py
[AutoAPI] Reading files... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/llm_state.py
[AutoAPI] Reading files... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/meta_state.py
[AutoAPI] Reading files... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/tool_state.py
[AutoAPI] Reading files... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/tools/**init**.py
[AutoAPI] Reading files... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/tools/validation_state.py
[AutoAPI] Reading files... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_with_token_usage.py
[AutoAPI] Reading files... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/messages/compatibility.py
[AutoAPI] Reading files... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/messages/**init**.py
[AutoAPI] Reading files... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py
[AutoAPI] Reading files... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/messages/utils.py
[AutoAPI] Reading files... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/messages/token_usage.py
[AutoAPI] Reading files... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/messages/token_usage_mixin.py
[AutoAPI] Reading files... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/mixins/**init**.py
[AutoAPI] Reading files... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/state/**init**.py
[AutoAPI] Reading files... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/validators.py
[AutoAPI] Reading files... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/compatibility.py
[AutoAPI] Reading files... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/langchain_converters.py
[AutoAPI] Reading files... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/protocols.py
[AutoAPI] Reading files... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/analyzer.py
[AutoAPI] Reading files... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/field_mapping.py
[AutoAPI] Reading files... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/**init**.py
[AutoAPI] Reading files... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/converters.py
[AutoAPI] Reading files... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/utils.py
[AutoAPI] Reading files... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/reports.py
[AutoAPI] Reading files... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/types.py
[AutoAPI] Reading files... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/mergers.py
[AutoAPI] Reading files... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/tool_manager.py
[AutoAPI] Reading files... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/tool_config.py
[AutoAPI] Reading files... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph_manager.py
[AutoAPI] Reading files... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/graph_pattern_registry.py
[AutoAPI] Reading files... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/tool_injector.py
[AutoAPI] Reading files... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/StateSchema.py
[AutoAPI] Reading files... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/ToolManager.py
[AutoAPI] Reading files... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/graph_builder2.py
[AutoAPI] Reading files... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/NodeFactory.py
[AutoAPI] Reading files... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/**init**.py
[AutoAPI] Reading files... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/dynamic_graph_builder.py
[AutoAPI] Reading files... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph.py
[AutoAPI] Reading files... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/StateGraphEditor.py
[AutoAPI] Reading files... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/routing.py
[AutoAPI] Reading files... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/agent_node_v2.py
[AutoAPI] Reading files... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/config.py
[AutoAPI] Reading files... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/message_transformation.py
[AutoAPI] Reading files... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/factory.py
[AutoAPI] Reading files... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/intelligent_multi_agent_node.py
[AutoAPI] Reading files... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/routing_validation_node.py
[AutoAPI] Reading files... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/unified_validation_node.py
[AutoAPI] Reading files... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/state_updating_validation_node.py
[AutoAPI] Reading files... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/agent_node.py
[AutoAPI] Reading files... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/protocols.py
[AutoAPI] Reading files... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/validation_node_v2.py
[AutoAPI] Reading files... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/meta_agent_node.py
[AutoAPI] Reading files... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/registry.py
[AutoAPI] Reading files... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/**init**.py
[AutoAPI] Reading files... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/output_parsing_v2.py
[AutoAPI] Reading files... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/tool_node_config_v2.py
[AutoAPI] Reading files... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/decorators.py
[AutoAPI] Reading files... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/stateful_node_config.py
[AutoAPI] Reading files... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/engine_node.py
[AutoAPI] Reading files... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/agent_node_v3.py
[AutoAPI] Reading files... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/callable_node.py
[AutoAPI] Reading files... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/handlers.py
[AutoAPI] Reading files... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/output_parsing.py
[AutoAPI] Reading files... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/utils.py
[AutoAPI] Reading files... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/types.py
[AutoAPI] Reading files... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/validation_node_with_routing.py
[AutoAPI] Reading files... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/tool_node_config.py
[AutoAPI] Reading files... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/stateful_validation_node.py
[AutoAPI] Reading files... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/validation_node_config.py
[AutoAPI] Reading files... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/base_config.py
[AutoAPI] Reading files... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/engine_node_generic.py
[AutoAPI] Reading files... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/parser_node_config_v2.py
[AutoAPI] Reading files... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/base_node_config.py
[AutoAPI] Reading files... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/parser_node_config.py
[AutoAPI] Reading files... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/test.py
[AutoAPI] Reading files... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/processors.py
[AutoAPI] Reading files... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/placeholder_node.py
[AutoAPI] Reading files... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py
[AutoAPI] Reading files... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/validation_node_config_v2.py
[AutoAPI] Reading files... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/validation_router_v2.py
[AutoAPI] Reading files... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/multi_agent_node.py
[AutoAPI] Reading files... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/composer/protocols.py
[AutoAPI] Reading files... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/composer/node_schema_composer.py
[AutoAPI] Reading files... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/composer/field_mapping.py
[AutoAPI] Reading files... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/composer/**init**.py
[AutoAPI] Reading files... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/composer/extract_functions.py
[AutoAPI] Reading files... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/composer/update_functions.py
[AutoAPI] Reading files... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/composer/advanced_node_composer.py
[AutoAPI] Reading files... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/composer/integrated_node_composer.py
[AutoAPI] Reading files... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/composer/path_resolver.py
[AutoAPI] Reading files... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/common/**init**.py
[AutoAPI] Reading files... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/common/types.py
[AutoAPI] Reading files... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/common/field_utils.py
[AutoAPI] Reading files... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/common/serialization.py
[AutoAPI] Reading files... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/common/references.py
[AutoAPI] Reading files... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/base.py
[AutoAPI] Reading files... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/mixin.py
[AutoAPI] Reading files... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/serializable.py
[AutoAPI] Reading files... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/recompilation_demo.py
[AutoAPI] Reading files... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/pattern_registry.py
[AutoAPI] Reading files... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/state_graph_builder.py
[AutoAPI] Reading files... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/registry.py
[AutoAPI] Reading files... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/**init**.py
[AutoAPI] Reading files... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/validation_mixin.py
[AutoAPI] Reading files... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/types.py
[AutoAPI] Reading files... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/graph_path.py
[AutoAPI] Reading files... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/pattern_definition.py
[AutoAPI] Reading files... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/schema_graph.py
[AutoAPI] Reading files... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/state_graph.py
[AutoAPI] Reading files... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py
[AutoAPI] Reading files... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/graph_visualizer.py
[AutoAPI] Reading files... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/schema_mixin.py
[AutoAPI] Reading files... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/pattern_decorator.py
[AutoAPI] Reading files... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/packages/haive-core/src/haive/core/graph/state_graph/conversion/**init**.py
[AutoAPI] Reading files... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/packages/haive-core/src/haive/core/graph/state_graph/utils/**init**.py
[AutoAPI] Reading files... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/packages/haive-core/src/haive/core/graph/state_graph/components/**init**.py
[AutoAPI] Reading files... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/conversion/**init**.py
[AutoAPI] Reading files... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/conversion/langgraph.py
[AutoAPI] Reading files... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/models/edge_model.py
[AutoAPI] Reading files... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/models/function_ref.py
[AutoAPI] Reading files... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/models/node_model.py
[AutoAPI] Reading files... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/models/state_graph_model.py
[AutoAPI] Reading files... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/models/branch_model.py
[AutoAPI] Reading files... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/utils/**init**.py
[AutoAPI] Reading files... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/pattern/base.py
[AutoAPI] Reading files... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/pattern/**init**.py
[AutoAPI] Reading files... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/pattern/implementations.py
[AutoAPI] Reading files... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/node.py
[AutoAPI] Reading files... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/architecture_summary.py
[AutoAPI] Reading files... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/modular_base_graph.py
[AutoAPI] Reading files... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/branch.py
[AutoAPI] Reading files... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/**init**.py
[AutoAPI] Reading files... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/branch_manager.py
[AutoAPI] Reading files... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/node_manager.py
[AutoAPI] Reading files... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/base_component.py
[AutoAPI] Reading files... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/edge_manager.py
[AutoAPI] Reading files... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/gb/**init**.py
[AutoAPI] Reading files... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/gb/types.py
[AutoAPI] Reading files... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/utils/**init**.py
[AutoAPI] Reading files... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/utils/mermaid_visualizer.py
[AutoAPI] Reading files... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/routers/base.py
[AutoAPI] Reading files... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/routers/**init**.py
[AutoAPI] Reading files... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/routers/conditions.py
[AutoAPI] Reading files... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/routers/test.py
[AutoAPI] Reading files... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/branches/branch.py
[AutoAPI] Reading files... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/branches/**init**.py
[AutoAPI] Reading files... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/branches/utils.py
[AutoAPI] Reading files... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/branches/dynamic.py
[AutoAPI] Reading files... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/branches/types.py
[AutoAPI] Reading files... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/branches/send_mapping.py
[AutoAPI] Reading files... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/retry/base.py
[AutoAPI] Reading files... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/retry/**init**.py
[AutoAPI] Reading files... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/patterns/integration.py
[AutoAPI] Reading files... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/patterns/base.py
[AutoAPI] Reading files... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/patterns/registry.py
[AutoAPI] Reading files... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/patterns/**init**.py
[AutoAPI] Reading files... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/state.py
[AutoAPI] Reading files... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base.py
[AutoAPI] Reading files... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/config.py
[AutoAPI] Reading files... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/models.py
[AutoAPI] Reading files... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/factory.py
[AutoAPI] Reading files... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/tool_utils.py
[AutoAPI] Reading files... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/**init**.py
[AutoAPI] Reading files... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/state_wrapper.py
[AutoAPI] Reading files... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/qa_agent.py
[AutoAPI] Reading files... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py
[AutoAPI] Reading files... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/routing_agent.py
[AutoAPI] Reading files... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain_agent.py
[AutoAPI] Reading files... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/tools.py
[AutoAPI] Reading files... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/**init**.py
[AutoAPI] Reading files... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/perplexity/pro_search/models.py
[AutoAPI] Reading files... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/perplexity/pro_search/**init**.py
[AutoAPI] Reading files... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/perplexity/pro_search/tasks/models.py
[AutoAPI] Reading files... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/perplexity/pro_search/tasks/**init**.py
[AutoAPI] Reading files... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/perplexity/pro_search/tasks/prompts.py
[AutoAPI] Reading files... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/perplexity/pro_search/search/models.py
[AutoAPI] Reading files... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/perplexity/pro_search/search/**init**.py
[AutoAPI] Reading files... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/perplexity/pro_search/search/prompts.py
[AutoAPI] Reading files... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/state.py
[AutoAPI] Reading files... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/config.py
[AutoAPI] Reading files... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/**init**.py
[AutoAPI] Reading files... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/related_topics_generator/models.py
[AutoAPI] Reading files... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/related_topics_generator/**init**.py
[AutoAPI] Reading files... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/related_topics_generator/agent.py
[AutoAPI] Reading files... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/related_topics_generator/prompt.py
[AutoAPI] Reading files... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/section_writer/models.py
[AutoAPI] Reading files... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/section_writer/**init**.py
[AutoAPI] Reading files... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/section_writer/agent.py
[AutoAPI] Reading files... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/section_writer/prompt.py
[AutoAPI] Reading files... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/outline_generator/models.py
[AutoAPI] Reading files... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/outline_generator/**init**.py
[AutoAPI] Reading files... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/outline_generator/agent.py
[AutoAPI] Reading files... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/outline_generator/prompt.py
[AutoAPI] Reading files... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/outline_refiner/**init**.py
[AutoAPI] Reading files... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/outline_refiner/agent.py
[AutoAPI] Reading files... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/outline_refiner/prompt.py
[AutoAPI] Reading files... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/wiki_writer/**init**.py
[AutoAPI] Reading files... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/wiki_writer/agent.py
[AutoAPI] Reading files... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/wiki_writer/prompt.py
[AutoAPI] Reading files... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/generate_perspectives/models.py
[AutoAPI] Reading files... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/generate_perspectives/**init**.py
[AutoAPI] Reading files... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/generate_perspectives/agent.py
[AutoAPI] Reading files... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/generate_perspectives/prompt.py
[AutoAPI] Reading files... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/person/state.py
[AutoAPI] Reading files... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/person/config.py
[AutoAPI] Reading files... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/person/models.py
[AutoAPI] Reading files... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/person/**init**.py
[AutoAPI] Reading files... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/person/utils.py
[AutoAPI] Reading files... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/person/agent.py
[AutoAPI] Reading files... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/person/prompts.py
[AutoAPI] Reading files... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/state.py
[AutoAPI] Reading files... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/structured_tools.py
[AutoAPI] Reading files... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/engines.py
[AutoAPI] Reading files... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/config.py
[AutoAPI] Reading files... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/models.py
[AutoAPI] Reading files... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/react_agent_config.py
[AutoAPI] Reading files... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/**init**.py
[AutoAPI] Reading files... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/agent.py
[AutoAPI] Reading files... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/prompts.py
[AutoAPI] Reading files... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/**init**.py
[AutoAPI] Reading files... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/mixins.py
[AutoAPI] Reading files... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/task_analysis/base.py
[AutoAPI] Reading files... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/task_analysis/solvability.py
[AutoAPI] Reading files... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/task_analysis/parallelization.py
[AutoAPI] Reading files... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/task_analysis/**init**.py
[AutoAPI] Reading files... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/task_analysis/branching.py
[AutoAPI] Reading files... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/task_analysis/analysis.py
[AutoAPI] Reading files... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/composite.py
[AutoAPI] Reading files... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/base.py
[AutoAPI] Reading files... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/rubric.py
[AutoAPI] Reading files... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/numeric.py
[AutoAPI] Reading files... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/**init**.py
[AutoAPI] Reading files... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/scale.py
[AutoAPI] Reading files... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/qualitative.py
[AutoAPI] Reading files... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/letter_grade.py
[AutoAPI] Reading files... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/binary.py
[AutoAPI] Reading files... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/utils/pydantic_prompt_utils.py
[AutoAPI] Reading files... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/state.py
[AutoAPI] Reading files... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/models.py
[AutoAPI] Reading files... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/multi_agent_reflection.py
[AutoAPI] Reading files... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/simple_agent.py
[AutoAPI] Reading files... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/**init**.py
[AutoAPI] Reading files... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/message_transformer_posthook.py
[AutoAPI] Reading files... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/agent.py
[AutoAPI] Reading files... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/structured_output.py
[AutoAPI] Reading files... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/message_transformer.py
[AutoAPI] Reading files... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/prompts.py
[AutoAPI] Reading files... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/universal_agent.py
[AutoAPI] Reading files... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/hooks.py
[AutoAPI] Reading files... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/enhanced_init.py
[AutoAPI] Reading files... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/**init**.py
[AutoAPI] Reading files... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/typed_agent.py
[AutoAPI] Reading files... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/compiled_agent.py
[AutoAPI] Reading files... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent_with_token_tracking.py
[AutoAPI] Reading files... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py
[AutoAPI] Reading files... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/types.py
[AutoAPI] Reading files... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent_structured_output_mixin.py
[AutoAPI] Reading files... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/enhanced_agent.py
[AutoAPI] Reading files... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/pre_post_agent_mixin.py
[AutoAPI] Reading files... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/serialization_mixin.py
[AutoAPI] Reading files... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/agent_protocol.py
[AutoAPI] Reading files... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/**init**.py
[AutoAPI] Reading files... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/hooks_mixin.py
[AutoAPI] Reading files... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/persistence_mixin.py
[AutoAPI] Reading files... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/state_mixin.py
[AutoAPI] Reading files... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/execution_mixin.py
[AutoAPI] Reading files... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/structured_output/models.py
[AutoAPI] Reading files... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/structured_output/**init**.py
[AutoAPI] Reading files... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/structured_output/agent.py
[AutoAPI] Reading files... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document/agent.py
[AutoAPI] Reading files... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/dynamic_tool_selector.py
[AutoAPI] Reading files... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/semantic_discovery.py
[AutoAPI] Reading files... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/**init**.py
[AutoAPI] Reading files... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/selection_strategies.py
[AutoAPI] Reading files... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/component_discovery_agent.py
[AutoAPI] Reading files... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/**init**.py
[AutoAPI] Reading files... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/agent.py
[AutoAPI] Reading files... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/prompts.py
[AutoAPI] Reading files... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/complexity/engines.py
[AutoAPI] Reading files... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/complexity/models.py
[AutoAPI] Reading files... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/complexity/prompts.py
[AutoAPI] Reading files... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/base/models.py
[AutoAPI] Reading files... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/base/**init**.py
[AutoAPI] Reading files... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/decomposer/engines.py
[AutoAPI] Reading files... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/decomposer/models.py
[AutoAPI] Reading files... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/decomposer/**init**.py
[AutoAPI] Reading files... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/decomposer/prompts.py
[AutoAPI] Reading files... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/decomposer/prompt.py
[AutoAPI] Reading files... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/tree/engines.py
[AutoAPI] Reading files... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/tree/models.py
[AutoAPI] Reading files... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/tree/**init**.py
[AutoAPI] Reading files... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/tree/prompts.py
[AutoAPI] Reading files... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/analysis/engines.py
[AutoAPI] Reading files... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/analysis/models.py
[AutoAPI] Reading files... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/analysis/**init**.py
[AutoAPI] Reading files... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/analysis/prompts.py
[AutoAPI] Reading files... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/execution/engines.py
[AutoAPI] Reading files... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/execution/models.py
[AutoAPI] Reading files... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/execution/**init**.py
[AutoAPI] Reading files... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/execution/prompts.py
[AutoAPI] Reading files... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/context/engines.py
[AutoAPI] Reading files... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/context/models.py
[AutoAPI] Reading files... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/context/**init**.py
[AutoAPI] Reading files... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/context/prompts.py
[AutoAPI] Reading files... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic_tool_discovery_supervisor.py
[AutoAPI] Reading files... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic_multi_agent.py
[AutoAPI] Reading files... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/compatibility_bridge.py
[AutoAPI] Reading files... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic_state.py
[AutoAPI] Reading files... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic_supervisor_fixed.py
[AutoAPI] Reading files... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/internal_dynamic_supervisor.py
[AutoAPI] Reading files... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/choice_model_supervisor.py
[AutoAPI] Reading files... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic_activation_supervisor.py
[AutoAPI] Reading files... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/integrated_supervisor.py
[AutoAPI] Reading files... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/simple_supervisor.py
[AutoAPI] Reading files... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic_agent_tools.py
[AutoAPI] Reading files... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/registry.py
[AutoAPI] Reading files... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic_executor_node.py
[AutoAPI] Reading files... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/**init**.py
[AutoAPI] Reading files... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/proper_dynamic_supervisor.py
[AutoAPI] Reading files... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/clean_dynamic_supervisor.py
[AutoAPI] Reading files... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic_supervisor.py
[AutoAPI] Reading files... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/agent.py
[AutoAPI] Reading files... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/simple_test_runner.py
[AutoAPI] Reading files... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/multi_agent_dynamic_state.py
[AutoAPI] Reading files... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic_agent_discovery_supervisor.py
[AutoAPI] Reading files... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/registry_supervisor.py
[AutoAPI] Reading files... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/routing.py
[AutoAPI] Reading files... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/agent_v2.py
[AutoAPI] Reading files... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/rebuild_dynamic_supervisor.py
[AutoAPI] Reading files... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/multi_integration.py
[AutoAPI] Reading files... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/chain_agent_simple.py
[AutoAPI] Reading files... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/**init**.py
[AutoAPI] Reading files... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/chain_examples.py
[AutoAPI] Reading files... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/extended_examples.py
[AutoAPI] Reading files... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/sequential/config.py
[AutoAPI] Reading files... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/sequential/**init**.py
[AutoAPI] Reading files... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/sequential/agent.py
[AutoAPI] Reading files... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/proper_plan_execute.py
[AutoAPI] Reading files... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/langgraph_plan_execute.py
[AutoAPI] Reading files... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/**init**.py
[AutoAPI] Reading files... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo_tree_agent.py
[AutoAPI] Reading files... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo_tree_agent_v2.py
[AutoAPI] Reading files... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo_tree_agent_v3.py
[AutoAPI] Reading files... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/clean_plan_execute.py
[AutoAPI] Reading files... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute_multi.py
[AutoAPI] Reading files... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/state.py
[AutoAPI] Reading files... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/engines.py
[AutoAPI] Reading files... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/simple.py
[AutoAPI] Reading files... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/config.py
[AutoAPI] Reading files... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/models.py
[AutoAPI] Reading files... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/**init**.py
[AutoAPI] Reading files... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/agent.py
[AutoAPI] Reading files... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/v2/state.py
[AutoAPI] Reading files... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/v2/models.py
[AutoAPI] Reading files... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/v2/**init**.py
[AutoAPI] Reading files... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/v2/agent.py
[AutoAPI] Reading files... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/v2/prompts.py
[AutoAPI] Reading files... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_execute_v3/state.py
[AutoAPI] Reading files... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_execute_v3/engines.py
[AutoAPI] Reading files... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_execute_v3/config.py
[AutoAPI] Reading files... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_execute_v3/models.py
[AutoAPI] Reading files... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_execute_v3/**init**.py
[AutoAPI] Reading files... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_execute_v3/agent.py
[AutoAPI] Reading files... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_execute_v3/prompts.py
[AutoAPI] Reading files... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo/**init**.py
[AutoAPI] Reading files... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo/agents/**init**.py
[AutoAPI] Reading files... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo/models/join_step.py
[AutoAPI] Reading files... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo/models/**init**.py
[AutoAPI] Reading files... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo/models/tool_step.py
[AutoAPI] Reading files... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo/models/steps.py
[AutoAPI] Reading files... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo/models/plans.py
[AutoAPI] Reading files... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/models/base.py
[AutoAPI] Reading files... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/models/**init**.py
[AutoAPI] Reading files... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler_v3/state.py
[AutoAPI] Reading files... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler_v3/config.py
[AutoAPI] Reading files... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler_v3/models.py
[AutoAPI] Reading files... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler_v3/**init**.py
[AutoAPI] Reading files... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler_v3/agent.py
[AutoAPI] Reading files... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler_v3/prompts.py
[AutoAPI] Reading files... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/p_and_e/state.py
[AutoAPI] Reading files... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/p_and_e/engines.py
[AutoAPI] Reading files... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/p_and_e/models.py
[AutoAPI] Reading files... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/p_and_e/**init**.py
[AutoAPI] Reading files... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/p_and_e/agent.py
[AutoAPI] Reading files... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/p_and_e/multi_agent.py
[AutoAPI] Reading files... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/p_and_e/enhanced_multi_agent.py
[AutoAPI] Reading files... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/p_and_e/prompts.py
[AutoAPI] Reading files... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo_v3/state.py
[AutoAPI] Reading files... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo_v3/models.py
[AutoAPI] Reading files... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo_v3/**init**.py
[AutoAPI] Reading files... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo_v3/agent.py
[AutoAPI] Reading files... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo_v3/prompts.py
[AutoAPI] Reading files... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler/state.py
[AutoAPI] Reading files... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler/config.py
[AutoAPI] Reading files... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler/models.py
[AutoAPI] Reading files... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler/**init**.py
[AutoAPI] Reading files... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler/utils.py
[AutoAPI] Reading files... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler/agent.py
[AutoAPI] Reading files... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler/output_parser.py
[AutoAPI] Reading files... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler/tools/math_tools.py
[AutoAPI] Reading files... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/state.py
[AutoAPI] Reading files... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/enhanced_agent_v3.py
[AutoAPI] Reading files... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/enhanced_simple_minimal.py
[AutoAPI] Reading files... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/config.py
[AutoAPI] Reading files... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/factory.py
[AutoAPI] Reading files... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/enhanced_simple_real.py
[AutoAPI] Reading files... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/ultra_lazy_agent.py
[AutoAPI] Reading files... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/lazy_simple_agent.py
[AutoAPI] Reading files... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/**init**.py
[AutoAPI] Reading files... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/agent_v3_minimal.py
[AutoAPI] Reading files... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/agent.py
[AutoAPI] Reading files... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/agent_with_validation.py
[AutoAPI] Reading files... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/clean_enhanced_simple.py
[AutoAPI] Reading files... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/enhanced_simple_agent_v2.py
[AutoAPI] Reading files... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/enhanced_simple_agent.py
[AutoAPI] Reading files... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/agent_v2.py
[AutoAPI] Reading files... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/agent_v3.py
[AutoAPI] Reading files... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/structured/config.py
[AutoAPI] Reading files... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/structured/**init**.py
[AutoAPI] Reading files... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/structured/agent.py
[AutoAPI] Reading files... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/v2/config.py
[AutoAPI] Reading files... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/v2/graph.py
[AutoAPI] Reading files... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/v2/**init**.py
[AutoAPI] Reading files... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/ltm/memory_schemas.py
[AutoAPI] Reading files... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/ltm/agent.py
[AutoAPI] Reading files... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/models.py
[AutoAPI] Reading files... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/branched_chain.py
[AutoAPI] Reading files... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/enhanced_memory_react.py
[AutoAPI] Reading files... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/unified_factory.py
[AutoAPI] Reading files... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/**init**.py
[AutoAPI] Reading files... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/answer_agent.py
[AutoAPI] Reading files... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/synthesis_agent.py
[AutoAPI] Reading files... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/collective_rag_agent_v4.py
[AutoAPI] Reading files... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple_rag_agent_v4.py
[AutoAPI] Reading files... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/chain_collection.py
[AutoAPI] Reading files... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/modular_chain.py
[AutoAPI] Reading files... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/agentic_router/**init**.py
[AutoAPI] Reading files... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/agentic_router/agent.py
[AutoAPI] Reading files... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/agentic_router/agent_chain.py
[AutoAPI] Reading files... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/agentic_router/agent_v2.py
[AutoAPI] Reading files... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/document_graders/comprehensive_grader.py
[AutoAPI] Reading files... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/document_graders/models.py
[AutoAPI] Reading files... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/document_graders/**init**.py
[AutoAPI] Reading files... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/document_graders/binary_grader/**init**.py
[AutoAPI] Reading files... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/document_graders/binary_grader/prompt.py
[AutoAPI] Reading files... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/document_graders/comprehensive_grader/models.py
[AutoAPI] Reading files... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/document_graders/comprehensive_grader/prompt.py
[AutoAPI] Reading files... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/hallucination_graders/models.py
[AutoAPI] Reading files... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/hallucination_graders/**init**.py
[AutoAPI] Reading files... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/hallucination_graders/prompts.py
[AutoAPI] Reading files... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/query_refinement/models.py
[AutoAPI] Reading files... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/query_refinement/**init**.py
[AutoAPI] Reading files... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/query_refinement/prompt.py
[AutoAPI] Reading files... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/answer_generators/**init**.py
[AutoAPI] Reading files... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/answer_generators/prompts.py
[AutoAPI] Reading files... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/query_constructors/flare/models.py
[AutoAPI] Reading files... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/query_constructors/flare/**init**.py
[AutoAPI] Reading files... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/query_constructors/flare/prompt.py
[AutoAPI] Reading files... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/query_constructors/hyde/models.py
[AutoAPI] Reading files... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/query_constructors/hyde/**init**.py
[AutoAPI] Reading files... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/query_constructors/hyde/enhanced_prompts.py
[AutoAPI] Reading files... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/query_constructors/hyde/prompt.py
[AutoAPI] Reading files... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/fusion/**init**.py
[AutoAPI] Reading files... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/fusion/agent.py
[AutoAPI] Reading files... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_strategy/state.py
[AutoAPI] Reading files... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_strategy/config.py
[AutoAPI] Reading files... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_strategy/**init**.py
[AutoAPI] Reading files... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_strategy/query_types.py
[AutoAPI] Reading files... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_strategy/agent.py
[AutoAPI] Reading files... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/base/state.py
[AutoAPI] Reading files... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/base/base_agent.py
[AutoAPI] Reading files... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/base/config.py
[AutoAPI] Reading files... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/base/models.py
[AutoAPI] Reading files... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/base/**init**.py
[AutoAPI] Reading files... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/base/utils.py
[AutoAPI] Reading files... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/base/agent.py
[AutoAPI] Reading files... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/base/branches.py
[AutoAPI] Reading files... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/base/prompts.py
[AutoAPI] Reading files... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_reflective/**init**.py
[AutoAPI] Reading files... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_reflective/agent.py
[AutoAPI] Reading files... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/state.py
[AutoAPI] Reading files... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/nodes.py
[AutoAPI] Reading files... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/graph.py
[AutoAPI] Reading files... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/configuration.py
[AutoAPI] Reading files... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/**init**.py
[AutoAPI] Reading files... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/prompts.py
[AutoAPI] Reading files... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/nodes/grade_documents.py
[AutoAPI] Reading files... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/nodes/generate.py
[AutoAPI] Reading files... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/nodes/grade_generation_v_documents_and_question.py
[AutoAPI] Reading files... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/nodes/decide_to_generate.py
[AutoAPI] Reading files... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/nodes/retreive.py
[AutoAPI] Reading files... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/nodes/transform_query.py
[AutoAPI] Reading files... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/flare/**init**.py
[AutoAPI] Reading files... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/flare/agent.py
[AutoAPI] Reading files... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/document_grading/**init**.py
[AutoAPI] Reading files... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/document_grading/agent.py
[AutoAPI] Reading files... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/factories/compatible_rag_factory_simple.py
[AutoAPI] Reading files... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/factories/rag_workflow_factory.py
[AutoAPI] Reading files... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/factories/compatible_rag_factory.py
[AutoAPI] Reading files... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/adaptive_rag/**init**.py
[AutoAPI] Reading files... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/adaptive_rag/agent.py
[AutoAPI] Reading files... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/adaptive/agent.py
[AutoAPI] Reading files... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/step_back/**init**.py
[AutoAPI] Reading files... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/step_back/agent.py
[AutoAPI] Reading files... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/memory_aware/**init**.py
[AutoAPI] Reading files... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/memory_aware/agent.py
[AutoAPI] Reading files... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/hyde/models.py
[AutoAPI] Reading files... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/hyde/enhanced_agent_v2.py
[AutoAPI] Reading files... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/hyde/**init**.py
[AutoAPI] Reading files... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/hyde/agent.py
[AutoAPI] Reading files... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/hyde/enhanced_agent.py
[AutoAPI] Reading files... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/hyde/prompts.py
[AutoAPI] Reading files... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/hyde/agent_v2.py
[AutoAPI] Reading files... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/simple_rag.py
[AutoAPI] Reading files... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/clean_simple_rag.py
[AutoAPI] Reading files... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/sequential_agent.py
[AutoAPI] Reading files... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/**init**.py
[AutoAPI] Reading files... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/answer_agent.py
[AutoAPI] Reading files... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/simple_rag_state.py
[AutoAPI] Reading files... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/agent.py
[AutoAPI] Reading files... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/multi_agent_simple_rag.py
[AutoAPI] Reading files... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/answer_generator/models.py
[AutoAPI] Reading files... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/answer_generator/**init**.py
[AutoAPI] Reading files... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/answer_generator/prompts.py
[AutoAPI] Reading files... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/enhanced_v3/state.py
[AutoAPI] Reading files... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/enhanced_v3/retriever_agent.py
[AutoAPI] Reading files... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/enhanced_v3/**init**.py
[AutoAPI] Reading files... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/enhanced_v3/answer_generator_agent.py
[AutoAPI] Reading files... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/enhanced_v3/agent.py
[AutoAPI] Reading files... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/state.py
[AutoAPI] Reading files... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/additional_workflows.py
[AutoAPI] Reading files... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/complete_rag_workflows.py
[AutoAPI] Reading files... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/enhanced_workflows.py
[AutoAPI] Reading files... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/compatibility.py
[AutoAPI] Reading files... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/specialized_workflows_v2.py
[AutoAPI] Reading files... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/**init**.py
[AutoAPI] Reading files... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/specialized_workflows.py
[AutoAPI] Reading files... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/enhanced_state_schemas.py
[AutoAPI] Reading files... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/advanced_workflows.py
[AutoAPI] Reading files... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/graded_rag_workflows_v2.py
[AutoAPI] Reading files... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/multi_rag.py
[AutoAPI] Reading files... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/simple_enhanced_workflows.py
[AutoAPI] Reading files... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/enhanced_multi_rag.py
[AutoAPI] Reading files... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/graded_rag_workflows.py
[AutoAPI] Reading files... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/agents.py
[AutoAPI] Reading files... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/grading_components.py
[AutoAPI] Reading files... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/dynamic/state.py
[AutoAPI] Reading files... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/dynamic/config.py
[AutoAPI] Reading files... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/dynamic/models.py
[AutoAPI] Reading files... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/dynamic/data_source_types.py
[AutoAPI] Reading files... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/dynamic/agent.py
[AutoAPI] Reading files... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_route/**init**.py
[AutoAPI] Reading files... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_route/agent.py
[AutoAPI] Reading files... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/typed/state.py
[AutoAPI] Reading files... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/typed/config.py
[AutoAPI] Reading files... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/typed/query_types.py
[AutoAPI] Reading files... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/typed/agent.py
[AutoAPI] Reading files... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/utils/structured_output_enhancer.py
[AutoAPI] Reading files... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/adaptive_tools/**init**.py
[AutoAPI] Reading files... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/adaptive_tools/agent.py
[AutoAPI] Reading files... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/query_decomposition/**init**.py
[AutoAPI] Reading files... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/query_decomposition/agent.py
[AutoAPI] Reading files... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/**init**.py
[AutoAPI] Reading files... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/state.py
[AutoAPI] Reading files... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/engines.py
[AutoAPI] Reading files... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/config.py
[AutoAPI] Reading files... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/models.py
[AutoAPI] Reading files... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/**init**.py
[AutoAPI] Reading files... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/utils.py
[AutoAPI] Reading files... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/agent.py
[AutoAPI] Reading files... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/prompts.py
[AutoAPI] Reading files... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/state.py
[AutoAPI] Reading files... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/engines.py
[AutoAPI] Reading files... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/config.py
[AutoAPI] Reading files... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/models.py
[AutoAPI] Reading files... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/**init**.py
[AutoAPI] Reading files... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/agent.py
[AutoAPI] Reading files... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/branches.py
[AutoAPI] Reading files... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/scratch.py
[AutoAPI] Reading files... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/base/db_config.py
[AutoAPI] Reading files... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/base/**init**.py
[AutoAPI] Reading files... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/filtered/state.py
[AutoAPI] Reading files... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/filtered/config.py
[AutoAPI] Reading files... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/filtered/**init**.py
[AutoAPI] Reading files... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/filtered/agent.py
[AutoAPI] Reading files... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/speculative/**init**.py
[AutoAPI] Reading files... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/speculative/agent.py
[AutoAPI] Reading files... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/hallucination_grading/**init**.py
[AutoAPI] Reading files... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/hallucination_grading/agent.py
[AutoAPI] Reading files... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/query_planning/**init**.py
[AutoAPI] Reading files... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/query_planning/agent.py
[AutoAPI] Reading files... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/query_planning/agent_chain.py
[AutoAPI] Reading files... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/agentic/react_rag_agent.py
[AutoAPI] Reading files... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/agentic/**init**.py
[AutoAPI] Reading files... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/agentic/agentic_rag_agent.py
[AutoAPI] Reading files... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/agentic/agent.py
[AutoAPI] Reading files... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/agentic/document_grader.py
[AutoAPI] Reading files... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/agentic/query_rewriter.py
[AutoAPI] Reading files... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_corr/state.py
[AutoAPI] Reading files... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_corr/engines.py
[AutoAPI] Reading files... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_corr/config.py
[AutoAPI] Reading files... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_corr/**init**.py
[AutoAPI] Reading files... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_corr/agent.py
[AutoAPI] Reading files... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/corrective/**init**.py
[AutoAPI] Reading files... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/corrective/agent.py
[AutoAPI] Reading files... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/corrective/agent_v2.py
[AutoAPI] Reading files... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/llm_rag/state.py
[AutoAPI] Reading files... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/llm_rag/config.py
[AutoAPI] Reading files... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/llm_rag/**init**.py
[AutoAPI] Reading files... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/llm_rag/engine.py
[AutoAPI] Reading files... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/llm_rag/agent.py
[AutoAPI] Reading files... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_query/agent.py
[AutoAPI] Reading files... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/long_term_memory/state.py
[AutoAPI] Reading files... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/long_term_memory/engines.py
[AutoAPI] Reading files... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/long_term_memory/models.py
[AutoAPI] Reading files... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/long_term_memory/aug_llm.py
[AutoAPI] Reading files... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/long_term_memory/nodes.py
[AutoAPI] Reading files... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/long_term_memory/**init**.py
[AutoAPI] Reading files... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/long_term_memory/agent.py
[AutoAPI] Reading files... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/long_term_memory/tools.py
[AutoAPI] Reading files... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/dynamic_supervisor/state.py
[AutoAPI] Reading files... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/dynamic_supervisor/models.py
[AutoAPI] Reading files... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/dynamic_supervisor/**init**.py
[AutoAPI] Reading files... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/dynamic_supervisor/agent.py
[AutoAPI] Reading files... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/dynamic_supervisor/prompts.py
[AutoAPI] Reading files... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/dynamic_supervisor/tools.py
[AutoAPI] Reading files... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_loader/**init**.py
[AutoAPI] Reading files... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_loader/directory/**init**.py
[AutoAPI] Reading files... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_loader/directory/agent.py
[AutoAPI] Reading files... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_loader/base/**init**.py
[AutoAPI] Reading files... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_loader/base/agent.py
[AutoAPI] Reading files... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_loader/web/**init**.py
[AutoAPI] Reading files... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_loader/web/agent.py
[AutoAPI] Reading files... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_loader/file/**init**.py
[AutoAPI] Reading files... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_loader/file/agent.py
[AutoAPI] Reading files... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/structured/models.py
[AutoAPI] Reading files... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/structured/**init**.py
[AutoAPI] Reading files... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/structured/agent.py
[AutoAPI] Reading files... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/structured/prompts.py
[AutoAPI] Reading files... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/state.py
[AutoAPI] Reading files... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/enhanced_agent_v3.py
[AutoAPI] Reading files... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/config.py
[AutoAPI] Reading files... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/**init**.py
[AutoAPI] Reading files... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/enhanced_react_agent.py
[AutoAPI] Reading files... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/agent.py
[AutoAPI] Reading files... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/dynamic_react_agent.py
[AutoAPI] Reading files... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/agent_v3.py
[AutoAPI] Reading files... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/archive/meta/**init**.py
[AutoAPI] Reading files... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/**init**.py
[AutoAPI] Reading files... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflection/state.py
[AutoAPI] Reading files... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflection/config.py
[AutoAPI] Reading files... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflection/models.py
[AutoAPI] Reading files... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflection/**init**.py
[AutoAPI] Reading files... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflection/agent.py
[AutoAPI] Reading files... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/state.py
[AutoAPI] Reading files... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/node.py
[AutoAPI] Reading files... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/config.py
[AutoAPI] Reading files... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/models.py
[AutoAPI] Reading files... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/**init**.py
[AutoAPI] Reading files... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/utils.py
[AutoAPI] Reading files... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/agent.py
[AutoAPI] Reading files... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/v2/state.py
[AutoAPI] Reading files... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/v2/models.py
[AutoAPI] Reading files... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/v2/**init**.py
[AutoAPI] Reading files... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/v2/prompts.py
[AutoAPI] Reading files... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/v2/agents.py
[AutoAPI] Reading files... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/state.py
[AutoAPI] Reading files... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/config.py
[AutoAPI] Reading files... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/models.py
[AutoAPI] Reading files... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/**init**.py
[AutoAPI] Reading files... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/utils.py
[AutoAPI] Reading files... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/agent.py
[AutoAPI] Reading files... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/responder_with_retries.py
[AutoAPI] Reading files... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/prompts.py
[AutoAPI] Reading files... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/tools.py
[AutoAPI] Reading files... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/state.py
[AutoAPI] Reading files... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/engines.py
[AutoAPI] Reading files... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/config.py
[AutoAPI] Reading files... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/models.py
[AutoAPI] Reading files... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/selector.py
[AutoAPI] Reading files... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/self_discover_simple_v4.py
[AutoAPI] Reading files... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/fixed_selector.py
[AutoAPI] Reading files... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/self_discover_multiagent.py
[AutoAPI] Reading files... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/**init**.py
[AutoAPI] Reading files... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/self_discover_enhanced_v4.py
[AutoAPI] Reading files... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/agent.py
[AutoAPI] Reading files... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/self_discover_sequential_v2.py
[AutoAPI] Reading files... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/agent2.py
[AutoAPI] Reading files... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/self_discover_working_v4.py
[AutoAPI] Reading files... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/self_discover_v4.py
[AutoAPI] Reading files... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/structurer/models.py
[AutoAPI] Reading files... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/structurer/**init**.py
[AutoAPI] Reading files... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/structurer/agent.py
[AutoAPI] Reading files... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/structurer/prompts.py
[AutoAPI] Reading files... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/executor/models.py
[AutoAPI] Reading files... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/executor/**init**.py
[AutoAPI] Reading files... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/executor/agent.py
[AutoAPI] Reading files... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/executor/prompts.py
[AutoAPI] Reading files... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/v2/state.py
[AutoAPI] Reading files... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/v2/models.py
[AutoAPI] Reading files... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/v2/**init**.py
[AutoAPI] Reading files... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/v2/agent.py
[AutoAPI] Reading files... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/v2/prompts.py
[AutoAPI] Reading files... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/adapter/models.py
[AutoAPI] Reading files... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/adapter/**init**.py
[AutoAPI] Reading files... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/adapter/agent.py
[AutoAPI] Reading files... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/adapter/prompts.py
[AutoAPI] Reading files... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/selector/models.py
[AutoAPI] Reading files... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/selector/**init**.py
[AutoAPI] Reading files... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/selector/agent.py
[AutoAPI] Reading files... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/selector/prompts.py
[AutoAPI] Reading files... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/models.py
[AutoAPI] Reading files... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/**init**.py
[AutoAPI] Reading files... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/agent.py
[AutoAPI] Reading files... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/engines/premise_extractor.py
[AutoAPI] Reading files... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/engines/uncertainty_analyzer.py
[AutoAPI] Reading files... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/engines/bias_detector.py
[AutoAPI] Reading files... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/engines/**init**.py
[AutoAPI] Reading files... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/engines/synthesis_agent.py
[AutoAPI] Reading files... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/engines/logical_reasoner.py
[AutoAPI] Reading files... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/state.py
[AutoAPI] Reading files... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/engines.py
[AutoAPI] Reading files... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/config.py
[AutoAPI] Reading files... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/models.py
[AutoAPI] Reading files... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/**init**.py
[AutoAPI] Reading files... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/agent.py
[AutoAPI] Reading files... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/modular/state.py
[AutoAPI] Reading files... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/modular/config.py
[AutoAPI] Reading files... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/modular/models.py
[AutoAPI] Reading files... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/modular/factory.py
[AutoAPI] Reading files... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/modular/**init**.py
[AutoAPI] Reading files... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/modular/agent.py
[AutoAPI] Reading files... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/modular/branches.py
[AutoAPI] Reading files... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/v2/state.py
[AutoAPI] Reading files... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/v2/engines.py
[AutoAPI] Reading files... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/v2/models.py
[AutoAPI] Reading files... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/v2/**init**.py
[AutoAPI] Reading files... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/v2/agent.py
[AutoAPI] Reading files... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/v2/prompts.py
[AutoAPI] Reading files... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/mcts/state.py
[AutoAPI] Reading files... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/mcts/config.py
[AutoAPI] Reading files... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/mcts/models.py
[AutoAPI] Reading files... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/mcts/**init**.py
[AutoAPI] Reading files... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/mcts/utils.py
[AutoAPI] Reading files... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/mcts/agent.py
[AutoAPI] Reading files... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/**init**.py
[AutoAPI] Reading files... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v3/config.py
[AutoAPI] Reading files... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v3/**init**.py
[AutoAPI] Reading files... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v3/agent.py
[AutoAPI] Reading files... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/tool_handler.py
[AutoAPI] Reading files... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/agent3.py
[AutoAPI] Reading files... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/config.py
[AutoAPI] Reading files... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/models.py
[AutoAPI] Reading files... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/tool_utils.py
[AutoAPI] Reading files... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/nodes.py
[AutoAPI] Reading files... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/config2.py
[AutoAPI] Reading files... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/advanced_agent3.py
[AutoAPI] Reading files... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/dynamic_agent.py
[AutoAPI] Reading files... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/**init**.py
[AutoAPI] Reading files... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/state2.py
[AutoAPI] Reading files... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/agent.py
[AutoAPI] Reading files... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/agent2.py
[AutoAPI] Reading files... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/many_tools/state.py
[AutoAPI] Reading files... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/many_tools/engines.py
[AutoAPI] Reading files... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/many_tools/models.py
[AutoAPI] Reading files... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/many_tools/nodes.py
[AutoAPI] Reading files... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/many_tools/**init**.py
[AutoAPI] Reading files... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react/state.py
[AutoAPI] Reading files... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react/config.py
[AutoAPI] Reading files... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react/tool_utils.py
[AutoAPI] Reading files... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react/agent.py
[AutoAPI] Reading files... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_many_tools/state.py
[AutoAPI] Reading files... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_many_tools/config.py
[AutoAPI] Reading files... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_many_tools/**init**.py
[AutoAPI] Reading files... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_many_tools/agent.py
[AutoAPI] Reading files... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent/state.py
[AutoAPI] Reading files... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent/**init**.py
[AutoAPI] Reading files... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent/agent.py
[AutoAPI] Reading files... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v2/state.py
[AutoAPI] Reading files... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v2/graph_utils.py
[AutoAPI] Reading files... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v2/tool_handling.py
[AutoAPI] Reading files... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v2/config.py
[AutoAPI] Reading files... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v2/**init**.py
[AutoAPI] Reading files... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v2/utils.py
[AutoAPI] Reading files... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v2/agent.py
[AutoAPI] Reading files... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v2/prompts.py
[AutoAPI] Reading files... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/**init**.py
[AutoAPI] Reading files... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/tnt/state.py
[AutoAPI] Reading files... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/tnt/engines.py
[AutoAPI] Reading files... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/tnt/models.py
[AutoAPI] Reading files... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/tnt/**init**.py
[AutoAPI] Reading files... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/tnt/utils.py
[AutoAPI] Reading files... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/tnt/agent.py
[AutoAPI] Reading files... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/tnt/branches.py
[AutoAPI] Reading files... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/base/state.py
[AutoAPI] Reading files... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/base/**init**.py
[AutoAPI] Reading files... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/base/models/**init**.py
[AutoAPI] Reading files... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/**init**.py
[AutoAPI] Reading files... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/iterative_refinement/state.py
[AutoAPI] Reading files... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/iterative_refinement/engines.py
[AutoAPI] Reading files... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/iterative_refinement/config.py
[AutoAPI] Reading files... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/iterative_refinement/**init**.py
[AutoAPI] Reading files... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/iterative_refinement/agent.py
[AutoAPI] Reading files... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/map_branch/state.py
[AutoAPI] Reading files... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/map_branch/engines.py
[AutoAPI] Reading files... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/map_branch/config.py
[AutoAPI] Reading files... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/map_branch/**init**.py
[AutoAPI] Reading files... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/map_branch/agent.py
[AutoAPI] Reading files... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/map_branch/prompts.py
[AutoAPI] Reading files... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/**init**.py
[AutoAPI] Reading files... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/state.py
[AutoAPI] Reading files... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/engines.py
[AutoAPI] Reading files... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/config.py
[AutoAPI] Reading files... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/models.py
[AutoAPI] Reading files... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/**init**.py
[AutoAPI] Reading files... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/utils.py
[AutoAPI] Reading files... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/agent.py
[AutoAPI] Reading files... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/agent2.py
[AutoAPI] Reading files... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_base/models.py
[AutoAPI] Reading files... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_base/**init**.py
[AutoAPI] Reading files... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_iterative_refinement/state.py
[AutoAPI] Reading files... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_iterative_refinement/engines.py
[AutoAPI] Reading files... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_iterative_refinement/config.py
[AutoAPI] Reading files... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_iterative_refinement/**init**.py
[AutoAPI] Reading files... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_iterative_refinement/utils.py
[AutoAPI] Reading files... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_iterative_refinement/agent.py
[AutoAPI] Reading files... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/state.py
[AutoAPI] Reading files... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/config.py
[AutoAPI] Reading files... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/models.py
[AutoAPI] Reading files... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/factory.py
[AutoAPI] Reading files... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/**init**.py
[AutoAPI] Reading files... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/utils.py
[AutoAPI] Reading files... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/agent.py
[AutoAPI] Reading files... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/utils/**init**.py
[AutoAPI] Reading files... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/utils/utils.py
[AutoAPI] Reading files... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_standalone.py
[AutoAPI] Reading files... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/base.py
[AutoAPI] Reading files... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced_clean_multi_agent.py
[AutoAPI] Reading files... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_generic.py
[AutoAPI] Reading files... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced_sequential_agent.py
[AutoAPI] Reading files... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced_parallel_agent.py
[AutoAPI] Reading files... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/**init**.py
[AutoAPI] Reading files... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced_dynamic_supervisor.py
[AutoAPI] Reading files... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced_supervisor_agent.py
[AutoAPI] Reading files... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/multi_agent.py
[AutoAPI] Reading files... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/clean.py
[AutoAPI] Reading files... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/multi_agent_v4.py
[AutoAPI] Reading files... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_v3.py
[AutoAPI] Reading files... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_v4.py
[AutoAPI] Reading files... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/sequential/**init**.py
[AutoAPI] Reading files... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/sequential/agent.py
[AutoAPI] Reading files... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/archive/enhanced_base.py
[AutoAPI] Reading files... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/archive/base.py
[AutoAPI] Reading files... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/archive/agent.py
[AutoAPI] Reading files... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/archive/configurable_base.py
[AutoAPI] Reading files... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/routing_patterns.py
[AutoAPI] Reading files... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/list_multi_agent.py
[AutoAPI] Reading files... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/proper_list_multi_agent.py
[AutoAPI] Reading files... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/implementations/clean_multi_agent.py
[AutoAPI] Reading files... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/implementations/simple_debug.py
[AutoAPI] Reading files... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/implementations/compatibility_enhanced_base.py
[AutoAPI] Reading files... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/implementations/multi_agent_v2.py
[AutoAPI] Reading files... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/implementations/clean_base.py
[AutoAPI] Reading files... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/implementations/self_discover_state.py
[AutoAPI] Reading files... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/implementations/proper_base.py
[AutoAPI] Reading files... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_processing/**init**.py
[AutoAPI] Reading files... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_processing/agent.py
[AutoAPI] Reading files... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/state.py
[AutoAPI] Reading files... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/graph_rag_retriever.py
[AutoAPI] Reading files... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/config.py
[AutoAPI] Reading files... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models.py
[AutoAPI] Reading files... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/multi_agent_coordinator.py
[AutoAPI] Reading files... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/kg_generator_agent.py
[AutoAPI] Reading files... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/unified_memory_api.py
[AutoAPI] Reading files... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/memory_utils.py
[AutoAPI] Reading files... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/**init**.py
[AutoAPI] Reading files... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/agentic_rag_coordinator.py
[AutoAPI] Reading files... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/agent.py
[AutoAPI] Reading files... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/sphinx_config.py
[AutoAPI] Reading files... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/enhanced_retriever.py
[AutoAPI] Reading files... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models/base.py
[AutoAPI] Reading files... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models/**init**.py
[AutoAPI] Reading files... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models/meta.py
[AutoAPI] Reading files... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models/procedural/models.py
[AutoAPI] Reading files... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models/procedural/**init**.py
[AutoAPI] Reading files... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models/semantic/models.py
[AutoAPI] Reading files... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models/semantic/**init**.py
[AutoAPI] Reading files... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models/semantic/mixins.py
[AutoAPI] Reading files... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models/episodic/models.py
[AutoAPI] Reading files... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models/episodic/**init**.py
[AutoAPI] Reading files... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models/episodic/mixins.py
[AutoAPI] Reading files... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/core/classifier.py
[AutoAPI] Reading files... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/core/**init**.py
[AutoAPI] Reading files... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/core/types.py
[AutoAPI] Reading files... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/core/stores.py
[AutoAPI] Reading files... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/base.py
[AutoAPI] Reading files... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/**init**.py
[AutoAPI] Reading files... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/pro_search/models.py
[AutoAPI] Reading files... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/pro_search/**init**.py
[AutoAPI] Reading files... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/pro_search/agent.py
[AutoAPI] Reading files... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/labs/models.py
[AutoAPI] Reading files... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/labs/**init**.py
[AutoAPI] Reading files... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/labs/agent.py
[AutoAPI] Reading files... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/deep_research/models.py
[AutoAPI] Reading files... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/deep_research/**init**.py
[AutoAPI] Reading files... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/deep_research/agent.py
[AutoAPI] Reading files... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/quick_search/models.py
[AutoAPI] Reading files... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/quick_search/**init**.py
[AutoAPI] Reading files... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/quick_search/agent.py
[AutoAPI] Reading files... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/**init**.py
[AutoAPI] Reading files... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/collaberative/state.py
[AutoAPI] Reading files... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/collaberative/**init**.py
[AutoAPI] Reading files... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/collaberative/agent.py
[AutoAPI] Reading files... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/base/state.py
[AutoAPI] Reading files... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/base/**init**.py
[AutoAPI] Reading files... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/base/agent.py
[AutoAPI] Reading files... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/round_robin/**init**.py
[AutoAPI] Reading files... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/round_robin/agent.py
[AutoAPI] Reading files... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/debate/state.py
[AutoAPI] Reading files... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/debate/**init**.py
[AutoAPI] Reading files... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/debate/agent.py
[AutoAPI] Reading files... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/directed/state.py
[AutoAPI] Reading files... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/directed/**init**.py
[AutoAPI] Reading files... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/directed/agent.py
[AutoAPI] Reading files... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/social_media/state.py
[AutoAPI] Reading files... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/social_media/models.py
[AutoAPI] Reading files... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/social_media/**init**.py
[AutoAPI] Reading files... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/social_media/agent.py
[AutoAPI] Reading files... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/state.py
[AutoAPI] Reading files... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/base.py
[AutoAPI] Reading files... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/models.py
[AutoAPI] Reading files... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/nodes.py
[AutoAPI] Reading files... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/**init**.py
[AutoAPI] Reading files... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/utils.py
[AutoAPI] Reading files... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/agent.py
[AutoAPI] Reading files... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/interview/state.py
[AutoAPI] Reading files... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/interview/models.py
[AutoAPI] Reading files... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/interview/nodes.py
[AutoAPI] Reading files... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/interview/**init**.py
[AutoAPI] Reading files... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/interview/utils.py
[AutoAPI] Reading files... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/interview/agent.py
[AutoAPI] Reading files... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/interview/tools.py
[AutoAPI] Reading files... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/static_supervisor_with_sync.py
[AutoAPI] Reading files... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/summarizer.py
[AutoAPI] Reading files... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/dynamic_supervisor_enhanced.py
[AutoAPI] Reading files... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/**init**.py
[AutoAPI] Reading files... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/dynamic_supervisor.py
[AutoAPI] Reading files... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/supervisor.py
[AutoAPI] Reading files... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/supervisor/**init**.py
[AutoAPI] Reading files... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/rag_memory_agent.py
[AutoAPI] Reading files... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/extraction_prompts.py
[AutoAPI] Reading files... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/react_memory_agent.py
[AutoAPI] Reading files... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/standalone_rag_memory.py
[AutoAPI] Reading files... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/memory_state_original.py
[AutoAPI] Reading files... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/multi_memory_agent.py
[AutoAPI] Reading files... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/standalone_memory_agent_free.py
[AutoAPI] Reading files... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/integrated_memory_system.py
[AutoAPI] Reading files... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/react_memory_coordinator.py
[AutoAPI] Reading files... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/long_term_memory_agent.py
[AutoAPI] Reading files... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/memory_models_standalone.py
[AutoAPI] Reading files... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/time_weighted_retriever.py
[AutoAPI] Reading files... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/**init**.py
[AutoAPI] Reading files... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/memory_state_with_tokens.py
[AutoAPI] Reading files... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/kg_memory_agent.py
[AutoAPI] Reading files... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/message_document_converter.py
[AutoAPI] Reading files... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/memory_state.py
[AutoAPI] Reading files... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/advanced_rag_memory_agent.py
[AutoAPI] Reading files... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/memory_tools.py
[AutoAPI] Reading files... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/graph_memory_agent.py
[AutoAPI] Reading files... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/multi_react_memory_system.py
[AutoAPI] Reading files... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/simple_memory_agent_deepseek.py
[AutoAPI] Reading files... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/token_tracker.py
[AutoAPI] Reading files... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/multi_memory_coordinator.py
[AutoAPI] Reading files... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/conversation_memory_agent.py
[AutoAPI] Reading files... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/simple_memory_agent.py
[AutoAPI] Reading files... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/patterns/react_structured_agent_variants.py
[AutoAPI] Reading files... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/patterns/sequential_workflow_agent.py
[AutoAPI] Reading files... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/patterns/react_with_structured_output.py
[AutoAPI] Reading files... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/patterns/**init**.py
[AutoAPI] Reading files... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/patterns/react_structured_reflection_patterns.py
[AutoAPI] Reading files... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/patterns/sequential_with_structured_output.py
[AutoAPI] Reading files... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/patterns/hybrid_multi_agent_patterns.py
[AutoAPI] Reading files... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/patterns/simple_rag_agent_pattern.py
[AutoAPI] Reading files... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/self_healing_code/state.py
[AutoAPI] Reading files... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/self_healing_code/**init**.py
[AutoAPI] Reading files... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/self_healing_code/branches.py
[AutoAPI] Reading files... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/**init**.py
[AutoAPI] Reading files... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/report_of_the_week_tool.py
[AutoAPI] Reading files... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/arxiv.py
[AutoAPI] Reading files... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/genderize_tool.py
[AutoAPI] Reading files... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/pokebase_tool.py
[AutoAPI] Reading files... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/dataforseo_tool.py
[AutoAPI] Reading files... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/techy_phrase_tool.py
[AutoAPI] Reading files... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/duckduckgo_search.py
[AutoAPI] Reading files... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/eleven_labs.py
[AutoAPI] Reading files... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/hinge_tools.py
[AutoAPI] Reading files... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/youtube_search_tool.py
[AutoAPI] Reading files... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/stack_exchange.py
[AutoAPI] Reading files... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/binlist_lookup.py
[AutoAPI] Reading files... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/geek_jokes_tool.py
[AutoAPI] Reading files... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/corporate_bs_tool.py
[AutoAPI] Reading files... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/wolfram_alpha_tool.py
[AutoAPI] Reading files... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/bing_search_tool_INC.py
[AutoAPI] Reading files... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/**init**.py
[AutoAPI] Reading files... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/scene_explain_tool.py
[AutoAPI] Reading files... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/translate_tools.py
[AutoAPI] Reading files... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/search_tools.py
[AutoAPI] Reading files... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/openaq_tool.py
[AutoAPI] Reading files... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/yfinance_tool.py
[AutoAPI] Reading files... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/dalle_image_generator_tool.py
[AutoAPI] Reading files... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/open_food_tool.py
[AutoAPI] Reading files... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/merriam_webster.py
[AutoAPI] Reading files... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/apify_tools.py
[AutoAPI] Reading files... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/agify_tool.py
[AutoAPI] Reading files... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/domain_search_tool.py
[AutoAPI] Reading files... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/asknews_tool.py
[AutoAPI] Reading files... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/dev_tools.py
[AutoAPI] Reading files... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/discord_tools.py
[AutoAPI] Reading files... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/ionic_tool.py
[AutoAPI] Reading files... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/brave_search.py
[AutoAPI] Reading files... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/pubmed.py
[AutoAPI] Reading files... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/reddit_search.py
[AutoAPI] Reading files... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/fruityvice_tool.py
[AutoAPI] Reading files... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_places.py
[AutoAPI] Reading files... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_jobs.py
[AutoAPI] Reading files... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_trends.py
[AutoAPI] Reading files... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_search.py
[AutoAPI] Reading files... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_finance.py
[AutoAPI] Reading files... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_books.py
[AutoAPI] Reading files... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/**init**.py
[AutoAPI] Reading files... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_lens.py
[AutoAPI] Reading files... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_scholar.py
[AutoAPI] Reading files... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/google_calendar.py
[AutoAPI] Reading files... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/base.py
[AutoAPI] Reading files... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/nasa_toolkit.py
[AutoAPI] Reading files... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/jira_toolkit.py
[AutoAPI] Reading files... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/nla_toolkit.py
[AutoAPI] Reading files... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/gmail_toolkit.py
[AutoAPI] Reading files... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/twilio_toolkit.py
[AutoAPI] Reading files... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/free_to_game_toolkit.py
[AutoAPI] Reading files... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/rick_and_morty_toolkit.py
[AutoAPI] Reading files... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/yugiioh_toolkit.py
[AutoAPI] Reading files... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/citydsk_toolkit.py
[AutoAPI] Reading files... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/poetry_db_toolkit.py
[AutoAPI] Reading files... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/mongodb_toolkit.py
[AutoAPI] Reading files... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/powerbi_toolkit.py
[AutoAPI] Reading files... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/gitlab_toolkit.py
[AutoAPI] Reading files... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/office_365.py
[AutoAPI] Reading files... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dataforseo_toolkit.py
[AutoAPI] Reading files... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/**init**.py
[AutoAPI] Reading files... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/alpha_vantage.py
[AutoAPI] Reading files... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/lcbo_toolkit.py
[AutoAPI] Reading files... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/trip_advisor_toolkit.py
[AutoAPI] Reading files... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/fred_toolkit.py
[AutoAPI] Reading files... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/clickup_toolkit.py
[AutoAPI] Reading files... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/sql_db_toolkit.py
[AutoAPI] Reading files... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/rps_101_toolkit.py
[AutoAPI] Reading files... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/slack_toolkit.py
[AutoAPI] Reading files... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/stack_exchange_toolkit.py
[AutoAPI] Reading files... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/chuck_norris_jokes_toolkit.py
[AutoAPI] Reading files... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/stripe_toolkit.py
[AutoAPI] Reading files... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/azure_ai_services_toolkit.py
[AutoAPI] Reading files... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/weather.py
[AutoAPI] Reading files... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/pandas_toolkits.py
[AutoAPI] Reading files... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/steam_toolkit.py
[AutoAPI] Reading files... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/github_toolkit.py
[AutoAPI] Reading files... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/request_tools.py
[AutoAPI] Reading files... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/amadues_toolkit.py
[AutoAPI] Reading files... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/polygon_toolkit.py
[AutoAPI] Reading files... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/useless_facts_toolkit.py
[AutoAPI] Reading files... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/vbible_toolkit.py
[AutoAPI] Reading files... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/openlibrary_toolkit.py
[AutoAPI] Reading files... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/financialdatasets_toolkit.py
[AutoAPI] Reading files... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/gradio_toolkit.py
[AutoAPI] Reading files... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/**init**.py
[AutoAPI] Reading files... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/tools.py
[AutoAPI] Reading files... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/permission.py
[AutoAPI] Reading files... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/shell.py
[AutoAPI] Reading files... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/background_process_manager.py
[AutoAPI] Reading files... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/remote_execution.py
[AutoAPI] Reading files... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/**init**.py
[AutoAPI] Reading files... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/multi_file_rename.py
[AutoAPI] Reading files... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/import_consolidator.py
[AutoAPI] Reading files... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/refactor.py
[AutoAPI] Reading files... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/type_hints.py
[AutoAPI] Reading files... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/function_logging_transformer.py
[AutoAPI] Reading files... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/print_to_logging.py
[AutoAPI] Reading files... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/type_checking.py
[AutoAPI] Reading files... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/dependency_analyzer.py
[AutoAPI] Reading files... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/complexity_analyzer.py
[AutoAPI] Reading files... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/code_smell_detector.py
[AutoAPI] Reading files... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/function_call_analyzer.py
[AutoAPI] Reading files... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/import_analyzer.py
[AutoAPI] Reading files... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/automatic_test_case_generator.py
[AutoAPI] Reading files... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/project_creation/**init**.py
[AutoAPI] Reading files... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/project_creation/github.py
[AutoAPI] Reading files... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/base.py
[AutoAPI] Reading files... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/models.py
[AutoAPI] Reading files... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/app_dep.py
[AutoAPI] Reading files... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/core.py
[AutoAPI] Reading files... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry.py
[AutoAPI] Reading files... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/**init**.py
[AutoAPI] Reading files... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/router.py
[AutoAPI] Reading files... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/tic_tac_toe_api.py
[AutoAPI] Reading files... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/game_agent.py
[AutoAPI] Reading files... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/connect4_api.py
[AutoAPI] Reading files... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/db.py
[AutoAPI] Reading files... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/discovery.py
[AutoAPI] Reading files... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/serialization.py
[AutoAPI] Reading files... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/**init\_**lazy.py
[AutoAPI] Reading files... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/llms/models.py
[AutoAPI] Reading files... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/llms/**init**.py
[AutoAPI] Reading files... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/llms/api.py
[AutoAPI] Reading files... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/persistence/conversations.py
[AutoAPI] Reading files... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/persistence/**init**.py
[AutoAPI] Reading files... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/persistence/supabase_adapter.py
[AutoAPI] Reading files... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/internal_websockets/**init**.py
[AutoAPI] Reading files... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/internal_websockets/handlers.py
[AutoAPI] Reading files... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/internal_websockets/manager.py
[AutoAPI] Reading files... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/fetchers/**init**.py
[AutoAPI] Reading files... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/fetchers/lite_llm_import.py
[AutoAPI] Reading files... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/run_integrated_api.py
[AutoAPI] Reading files... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/base.py
[AutoAPI] Reading files... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/simple_chess_ws.py
[AutoAPI] Reading files... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/integrate_games.py
[AutoAPI] Reading files... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py
[AutoAPI] Reading files... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/general_games_api.py
[AutoAPI] Reading files... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_socket.py
[AutoAPI] Reading files... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/app_dep.py
[AutoAPI] Reading files... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/serve_chess_client.py
[AutoAPI] Reading files... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/middleware.py
[AutoAPI] Reading files... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/run_simple.py
[AutoAPI] Reading files... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_api.py
[AutoAPI] Reading files... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/run_chess_api.py
[AutoAPI] Reading files... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/registry.py
[AutoAPI] Reading files... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/router.py
[AutoAPI] Reading files... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/tic_tac_toe_api.py
[AutoAPI] Reading files... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/run_simplified.py
[AutoAPI] Reading files... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router_fixed.py
[AutoAPI] Reading files... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router.py
[AutoAPI] Reading files... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_agent.py
[AutoAPI] Reading files... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/connect4_api.py
[AutoAPI] Reading files... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/db.py
[AutoAPI] Reading files... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/run_game_api.py
[AutoAPI] Reading files... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py
[AutoAPI] Reading files... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/run_games_api.py
[AutoAPI] Reading files... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/llms/models.py
[AutoAPI] Reading files... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/llms/**init**.py
[AutoAPI] Reading files... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/llms/api.py
[AutoAPI] Reading files... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes_enhanced.py
[AutoAPI] Reading files... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py
[AutoAPI] Reading files... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes_fixed.py
[AutoAPI] Reading files... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py
[AutoAPI] Reading files... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/**init**.py
[AutoAPI] Reading files... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/conversation_routes.py
[AutoAPI] Reading files... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes.py
[AutoAPI] Reading files... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes.py
[AutoAPI] Reading files... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/games.py
[AutoAPI] Reading files... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/llm_routes.py
[AutoAPI] Reading files... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_enhanced.py
[AutoAPI] Reading files... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routers/games.py
[AutoAPI] Reading files... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/middleware/supabase_logging.py
[AutoAPI] Reading files... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/middleware/**init**.py
[AutoAPI] Reading files... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/middleware/rate_limit.py
[AutoAPI] Reading files... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/middleware/auth.py
[AutoAPI] Reading files... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/middleware/logging.py
[AutoAPI] Reading files... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/base.py
[AutoAPI] Reading files... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/models.py
[AutoAPI] Reading files... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/core.py
[AutoAPI] Reading files... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/**init**.py
[AutoAPI] Reading files... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/lazy_core.py
[AutoAPI] Reading files... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/db.py
[AutoAPI] Reading files... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/discovery.py
[AutoAPI] Reading files... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/serialization.py
[AutoAPI] Reading files... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/providers/base.py
[AutoAPI] Reading files... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/providers/**init**.py
[AutoAPI] Reading files... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py
[AutoAPI] Reading files... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/importers/tak.py
[AutoAPI] Reading files... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/importers/litellm_importer.py
[AutoAPI] Reading files... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/importers/**init**.py
[AutoAPI] Reading files... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/importers/embeddings_importer.py
[AutoAPI] Reading files... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/utils/vault_migration_script.py
[AutoAPI] Reading files... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/utils/**init**.py
[AutoAPI] Reading files... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/utils/logging.py
[AutoAPI] Reading files... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/registries/**init**.py
[AutoAPI] Reading files... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/registries/model_registry.py
[AutoAPI] Reading files... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/auth/middleware.py
[AutoAPI] Reading files... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/auth/**init**.py
[AutoAPI] Reading files... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/auth/dependencies.py
[AutoAPI] Reading files... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/auth/supabase.py
[AutoAPI] Reading files... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/auth/credits.py
[AutoAPI] Reading files... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/providers/base.py
[AutoAPI] Reading files... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/providers/**init**.py
[AutoAPI] Reading files... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/providers/agent_provider.py
[AutoAPI] Reading files... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/mcp/**init**.py
[AutoAPI] Reading files... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/mcp/health.py
[AutoAPI] Reading files... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/mcp/client.py
[AutoAPI] Reading files... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/mcp/discovery.py
[AutoAPI] Reading files... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/importers/tak.py
[AutoAPI] Reading files... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/importers/litellm_importer.py
[AutoAPI] Reading files... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/importers/**init**.py
[AutoAPI] Reading files... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/importers/embeddings_importer.py
[AutoAPI] Reading files... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/db/schema.py
[AutoAPI] Reading files... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/db/inspect_supabase.py
[AutoAPI] Reading files... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/db/**init**.py
[AutoAPI] Reading files... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/db/supabase.py
[AutoAPI] Reading files... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/utils/vault_migration_script.py
[AutoAPI] Reading files... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/utils/**init**.py
[AutoAPI] Reading files... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/utils/logging.py
[AutoAPI] Reading files... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/conversations/**init**.py
[AutoAPI] Reading files... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/conversations/manager.py
[AutoAPI] Reading files... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/config/settings.py
[AutoAPI] Reading files... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/config/**init**.py
[AutoAPI] Reading files... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/config/environment.py
[AutoAPI] Reading files... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registries/**init**.py
[AutoAPI] Reading files... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registries/model_registry.py
[AutoAPI] Reading files... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/benchmark.py
[AutoAPI] Reading files... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/**init**.py
[AutoAPI] Reading files... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/llm_config_factory.py
[AutoAPI] Reading files... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/common/voting_system.py
[AutoAPI] Reading files... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/state.py
[AutoAPI] Reading files... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/engines.py
[AutoAPI] Reading files... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/state_manager.py
[AutoAPI] Reading files... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/config.py
[AutoAPI] Reading files... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/models.py
[AutoAPI] Reading files... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/configurable_config.py
[AutoAPI] Reading files... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/ui.py
[AutoAPI] Reading files... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/controller.py
[AutoAPI] Reading files... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/**init**.py
[AutoAPI] Reading files... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/generic_engines.py
[AutoAPI] Reading files... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/agent.py
[AutoAPI] Reading files... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/runner.py
[AutoAPI] Reading files... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/state.py
[AutoAPI] Reading files... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/engines.py
[AutoAPI] Reading files... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/state_manager.py
[AutoAPI] Reading files... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/config.py
[AutoAPI] Reading files... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/models.py
[AutoAPI] Reading files... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/configurable_config.py
[AutoAPI] Reading files... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/ui.py
[AutoAPI] Reading files... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/**init**.py
[AutoAPI] Reading files... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/generic_engines.py
[AutoAPI] Reading files... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/agent.py
[AutoAPI] Reading files... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/state.py
[AutoAPI] Reading files... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/engines.py
[AutoAPI] Reading files... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/state_manager.py
[AutoAPI] Reading files... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/config.py
[AutoAPI] Reading files... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/models.py
[AutoAPI] Reading files... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/configurable_config.py
[AutoAPI] Reading files... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/ui.py
[AutoAPI] Reading files... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/**init**.py
[AutoAPI] Reading files... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/generic_engines.py
[AutoAPI] Reading files... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/agent.py
[AutoAPI] Reading files... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/state.py
[AutoAPI] Reading files... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/engines.py
[AutoAPI] Reading files... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/state_manager.py
[AutoAPI] Reading files... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/config.py
[AutoAPI] Reading files... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/simple_demo.py
[AutoAPI] Reading files... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/verify_imports.py
[AutoAPI] Reading files... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/models.py
[AutoAPI] Reading files... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/mock_runner.py
[AutoAPI] Reading files... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/configurable_config.py
[AutoAPI] Reading files... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/**init**.py
[AutoAPI] Reading files... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/generic_engines.py
[AutoAPI] Reading files... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/agent.py
[AutoAPI] Reading files... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/simple_runner.py
[AutoAPI] Reading files... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/state.py
[AutoAPI] Reading files... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/engines.py
[AutoAPI] Reading files... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/state_manager.py
[AutoAPI] Reading files... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/config.py
[AutoAPI] Reading files... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/models.py
[AutoAPI] Reading files... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/configurable_config.py
[AutoAPI] Reading files... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/ui.py
[AutoAPI] Reading files... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/**init**.py
[AutoAPI] Reading files... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/generic_engines.py
[AutoAPI] Reading files... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/agent.py
[AutoAPI] Reading files... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/rich_ui.py
[AutoAPI] Reading files... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base/state.py
[AutoAPI] Reading files... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base/state_manager.py
[AutoAPI] Reading files... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base/config.py
[AutoAPI] Reading files... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base/models.py
[AutoAPI] Reading files... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base/factory.py
[AutoAPI] Reading files... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base/**init**.py
[AutoAPI] Reading files... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base/utils.py
[AutoAPI] Reading files... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base/agent.py
[AutoAPI] Reading files... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/state.py
[AutoAPI] Reading files... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/engines.py
[AutoAPI] Reading files... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/player_agent.py
[AutoAPI] Reading files... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/config.py
[AutoAPI] Reading files... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/simple_demo.py
[AutoAPI] Reading files... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/models.py
[AutoAPI] Reading files... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/standalone_demo.py
[AutoAPI] Reading files... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/configurable_config.py
[AutoAPI] Reading files... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/ui.py
[AutoAPI] Reading files... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/**init**.py
[AutoAPI] Reading files... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/generic_engines.py
[AutoAPI] Reading files... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/utils.py
[AutoAPI] Reading files... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/agent.py
[AutoAPI] Reading files... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/run_game.py
[AutoAPI] Reading files... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/game_agent.py
[AutoAPI] Reading files... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/ui_fixed.py
[AutoAPI] Reading files... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/prompts.py
[AutoAPI] Reading files... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/main_agent.py
[AutoAPI] Reading files... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/game/property.py
[AutoAPI] Reading files... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/game/player.py
[AutoAPI] Reading files... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/game/**init**.py
[AutoAPI] Reading files... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/game/types.py
[AutoAPI] Reading files... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/game/card.py
[AutoAPI] Reading files... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/game/game.py
[AutoAPI] Reading files... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/state.py
[AutoAPI] Reading files... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/engines.py
[AutoAPI] Reading files... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/state_manager.py
[AutoAPI] Reading files... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/player_agent.py
[AutoAPI] Reading files... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/config.py
[AutoAPI] Reading files... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/models.py
[AutoAPI] Reading files... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/configurable_config.py
[AutoAPI] Reading files... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/ui.py
[AutoAPI] Reading files... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/**init**.py
[AutoAPI] Reading files... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/generic_engines.py
[AutoAPI] Reading files... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/utils.py
[AutoAPI] Reading files... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/agent.py
[AutoAPI] Reading files... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/game_agent.py
[AutoAPI] Reading files... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/engine_logging.py
[AutoAPI] Reading files... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/api/setup.py
[AutoAPI] Reading files... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/api/**init**.py
[AutoAPI] Reading files... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/api/general_api.py
[AutoAPI] Reading files... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/state.py
[AutoAPI] Reading files... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/engines.py
[AutoAPI] Reading files... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/state_manager.py
[AutoAPI] Reading files... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/config.py
[AutoAPI] Reading files... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/models.py
[AutoAPI] Reading files... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/configurable_config.py
[AutoAPI] Reading files... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/ui.py
[AutoAPI] Reading files... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/standalone_game.py
[AutoAPI] Reading files... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/**init**.py
[AutoAPI] Reading files... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/generic_engines.py
[AutoAPI] Reading files... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/agent.py
[AutoAPI] Reading files... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/multi_player/state.py
[AutoAPI] Reading files... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/multi_player/state_manager.py
[AutoAPI] Reading files... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/multi_player/config.py
[AutoAPI] Reading files... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/multi_player/models.py
[AutoAPI] Reading files... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/multi_player/factory.py
[AutoAPI] Reading files... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/multi_player/**init**.py
[AutoAPI] Reading files... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/multi_player/agent.py
[AutoAPI] Reading files... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/**init**.py
[AutoAPI] Reading files... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/base/state.py
[AutoAPI] Reading files... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/base/state_manager.py
[AutoAPI] Reading files... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/base/config.py
[AutoAPI] Reading files... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/base/factory.py
[AutoAPI] Reading files... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/base/**init**.py
[AutoAPI] Reading files... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/base/template_generator.py
[AutoAPI] Reading files... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/base/utils.py
[AutoAPI] Reading files... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/base/agent.py
[AutoAPI] Reading files... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/multi_player/state.py
[AutoAPI] Reading files... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/multi_player/state_manager.py
[AutoAPI] Reading files... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/multi_player/config.py
[AutoAPI] Reading files... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/multi_player/models.py
[AutoAPI] Reading files... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/multi_player/factory.py
[AutoAPI] Reading files... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/multi_player/**init**.py
[AutoAPI] Reading files... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/multi_player/agent.py
[AutoAPI] Reading files... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/turn.py
[AutoAPI] Reading files... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/move.py
[AutoAPI] Reading files... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/player.py
[AutoAPI] Reading files... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/**init**.py
[AutoAPI] Reading files... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/board.py
[AutoAPI] Reading files... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/agent.py
[AutoAPI] Reading files... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/container.py
[AutoAPI] Reading files... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/grid.py
[AutoAPI] Reading files... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/position.py
[AutoAPI] Reading files... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/game.py
[AutoAPI] Reading files... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/space.py
[AutoAPI] Reading files... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/rule.py
[AutoAPI] Reading files... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/piece.py
[AutoAPI] Reading files... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/boards/grid.py
[AutoAPI] Reading files... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/spaces/grid.py
[AutoAPI] Reading files... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/positions/grid.py
[AutoAPI] Reading files... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/containers/deck.py
[AutoAPI] Reading files... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/tic_tac_toe/state.py
[AutoAPI] Reading files... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/tic_tac_toe/engines.py
[AutoAPI] Reading files... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/tic_tac_toe/state_manager.py
[AutoAPI] Reading files... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/tic_tac_toe/config.py
[AutoAPI] Reading files... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/tic_tac_toe/models.py
[AutoAPI] Reading files... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/tic_tac_toe/configurable_config.py
[AutoAPI] Reading files... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/tic_tac_toe/ui.py
[AutoAPI] Reading files... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/tic_tac_toe/**init**.py
[AutoAPI] Reading files... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/tic_tac_toe/generic_engines.py
[AutoAPI] Reading files... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/tic_tac_toe/agent.py
[AutoAPI] Reading files... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/tic_tac_toe/configurable_engines.py
[AutoAPI] Reading files... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/state.py
[AutoAPI] Reading files... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/engines.py
[AutoAPI] Reading files... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/state_manager.py
[AutoAPI] Reading files... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/config.py
[AutoAPI] Reading files... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/models.py
[AutoAPI] Reading files... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/agent_original.py
[AutoAPI] Reading files... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/configurable_config.py
[AutoAPI] Reading files... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/**init**.py
[AutoAPI] Reading files... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/generic_engines.py
[AutoAPI] Reading files... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/agent.py
[AutoAPI] Reading files... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/state_original.py
[AutoAPI] Reading files... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/**init**.py
[AutoAPI] Reading files... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/agent_with_judges.py
[AutoAPI] Reading files... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/agent.py
[AutoAPI] Reading files... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/judges.py
[AutoAPI] Reading files... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/state.py
[AutoAPI] Reading files... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/engines.py
[AutoAPI] Reading files... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/state_manager.py
[AutoAPI] Reading files... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/config.py
[AutoAPI] Reading files... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/models.py
[AutoAPI] Reading files... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/factory.py
[AutoAPI] Reading files... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/configurable_config.py
[AutoAPI] Reading files... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/ui.py
[AutoAPI] Reading files... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/**init**.py
[AutoAPI] Reading files... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/generic_engines.py
[AutoAPI] Reading files... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/agent.py
[AutoAPI] Reading files... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/state.py
[AutoAPI] Reading files... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/engines.py
[AutoAPI] Reading files... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/state_manager.py
[AutoAPI] Reading files... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/config.py
[AutoAPI] Reading files... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/models.py
[AutoAPI] Reading files... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/factory.py
[AutoAPI] Reading files... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/configurable_config.py
[AutoAPI] Reading files... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/ui.py
[AutoAPI] Reading files... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/enhanced_ui.py
[AutoAPI] Reading files... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/**init**.py
[AutoAPI] Reading files... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/generic_engines.py
[AutoAPI] Reading files... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/agent.py
[AutoAPI] Reading files... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/prompts.py
[AutoAPI] Reading files... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/state.py
[AutoAPI] Reading files... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/engines.py
[AutoAPI] Reading files... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/state_manager.py
[AutoAPI] Reading files... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/config.py
[AutoAPI] Reading files... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/models.py
[AutoAPI] Reading files... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/configurable_config.py
[AutoAPI] Reading files... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/ui.py
[AutoAPI] Reading files... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/llm_utils.py
[AutoAPI] Reading files... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/**init**.py
[AutoAPI] Reading files... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/generic_engines.py
[AutoAPI] Reading files... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/utils.py
[AutoAPI] Reading files... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/agent.py
[AutoAPI] Reading files... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/configurable_engines.py
[AutoAPI] Reading files... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/dynamic_config.py
[AutoAPI] Reading files... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/**init**.py
[AutoAPI] Reading files... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/uno/**init**.py
[AutoAPI] Reading files... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/models/**init**.py
[AutoAPI] Reading files... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/models/card.py
[AutoAPI] Reading files... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/bs/state.py
[AutoAPI] Reading files... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/bs/state_manager.py
[AutoAPI] Reading files... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/bs/config.py
[AutoAPI] Reading files... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/bs/models.py
[AutoAPI] Reading files... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/bs/**init**.py
[AutoAPI] Reading files... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/bs/agent.py
[AutoAPI] Reading files... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/bs/prompts.py
[AutoAPI] Reading files... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/poker/state.py
[AutoAPI] Reading files... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/poker/actions.py
[AutoAPI] Reading files... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/poker/**init**.py
[AutoAPI] Reading files... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/poker/scoring.py
[AutoAPI] Reading files... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/utils/recursion_config.py
[AutoAPI] Reading files... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/utils/**init**.py
[AutoAPI] Reading files... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/**init**.py
[AutoAPI] Reading files... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/piece/tile.py
[AutoAPI] Reading files... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/players/base.py
[AutoAPI] Reading files... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/players/agent.py
[AutoAPI] Reading files... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/base/state.py
[AutoAPI] Reading files... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/base/engines.py
[AutoAPI] Reading files... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/base/state_manager.py
[AutoAPI] Reading files... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/base/config.py
[AutoAPI] Reading files... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/base/models.py
[AutoAPI] Reading files... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/base/player.py
[AutoAPI] Reading files... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/core_space.py
[AutoAPI] Reading files... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/**init**.py
[AutoAPI] Reading files... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/core_position.py
[AutoAPI] Reading files... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/core_game.py
[AutoAPI] Reading files... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/core_board.py
[AutoAPI] Reading files... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/piece.py
[AutoAPI] Reading files... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/pieces/core_game.py
[AutoAPI] Reading files... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/containers/base.py
[AutoAPI] Reading files... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/containers/deck.py
[AutoAPI] Reading files... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/containers/**init**.py
[AutoAPI] Reading files... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/containers/container.py
[AutoAPI] Reading files... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/move/**init**.py
[AutoAPI] Reading files... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/agent/player_agent.py
[AutoAPI] Reading files... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/agent/game_config.py
[AutoAPI] Reading files... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/agent/generic_player_agent.py
[AutoAPI] Reading files... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/agent/**init**.py
[AutoAPI] Reading files... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/position/base.py
[AutoAPI] Reading files... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/position/**init**.py
[AutoAPI] Reading files... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/components/**init**.py
[AutoAPI] Reading files... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/components/cards/base.py
[AutoAPI] Reading files... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/components/cards/actions.py
[AutoAPI] Reading files... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/components/cards/**init**.py
[AutoAPI] Reading files... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/components/cards/scoring.py
[AutoAPI] Reading files... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/components/cards/turns.py
[AutoAPI] Reading files... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/components/cards/standard.py
[AutoAPI] Reading files... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/config/base.py
[AutoAPI] Reading files... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/config/**init**.py
[AutoAPI] Reading files... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/board/**init**.py
[AutoAPI] Reading files... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/state.py
[AutoAPI] Reading files... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/engines.py
[AutoAPI] Reading files... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/state_manager.py
[AutoAPI] Reading files... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/config.py
[AutoAPI] Reading files... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/models.py
[AutoAPI] Reading files... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/configurable_config.py
[AutoAPI] Reading files... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/ui.py
[AutoAPI] Reading files... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/**init**.py
[AutoAPI] Reading files... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/generic_engines.py
[AutoAPI] Reading files... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/agent.py
[AutoAPI] Reading files... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/prompts.py
[AutoAPI] Reading files... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate/state.py
[AutoAPI] Reading files... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate/engines.py
[AutoAPI] Reading files... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate/state_manager.py
[AutoAPI] Reading files... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate/config.py
[AutoAPI] Reading files... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate/models.py
[AutoAPI] Reading files... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate/factory.py
[AutoAPI] Reading files... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate/configurable_config.py
[AutoAPI] Reading files... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate/**init**.py
[AutoAPI] Reading files... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate/generic_engines.py
[AutoAPI] Reading files... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate/agent.py
[AutoAPI] Reading files... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/state.py
[AutoAPI] Reading files... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/engines.py
[AutoAPI] Reading files... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/state_manager.py
[AutoAPI] Reading files... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/config.py
[AutoAPI] Reading files... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/models.py
[AutoAPI] Reading files... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/configurable_config.py
[AutoAPI] Reading files... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/ui.py
[AutoAPI] Reading files... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/**init**.py
[AutoAPI] Reading files... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/generic_engines.py
[AutoAPI] Reading files... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/agent.py
[AutoAPI] Reading files... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/rich_ui.py
[AutoAPI] Reading files... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/fixed_runner.py
[AutoAPI] Reading files... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base_v2/state.py
[AutoAPI] Reading files... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base_v2/player_agent.py
[AutoAPI] Reading files... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base_v2/models.py
[AutoAPI] Reading files... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base_v2/**init**.py
[AutoAPI] Reading files... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/go/state.py
[AutoAPI] Reading files... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/go/engines.py
[AutoAPI] Reading files... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/go/state_manager.py
[AutoAPI] Reading files... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/go/config.py
[AutoAPI] Reading files... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/go/models.py
[AutoAPI] Reading files... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/go/**init**.py
[AutoAPI] Reading files... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/go/agent.py
[AutoAPI] Reading files... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/go/go_engine.py
[AutoAPI] Reading files... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/reversi/state.py
[AutoAPI] Reading files... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/reversi/engines.py
[AutoAPI] Reading files... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/reversi/state_manager.py
[AutoAPI] Reading files... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/reversi/config.py
[AutoAPI] Reading files... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/reversi/models.py
[AutoAPI] Reading files... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/reversi/configurable_config.py
[AutoAPI] Reading files... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/reversi/**init**.py
[AutoAPI] Reading files... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/reversi/generic_engines.py
[AutoAPI] Reading files... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/reversi/agent.py
[AutoAPI] Reading files... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/board/**init**.py
[AutoAPI] Reading files... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/risk/state.py
[AutoAPI] Reading files... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/risk/engines.py
[AutoAPI] Reading files... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/risk/state_manager.py
[AutoAPI] Reading files... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/risk/config.py
[AutoAPI] Reading files... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/risk/models.py
[AutoAPI] Reading files... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/risk/configurable_config.py
[AutoAPI] Reading files... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/risk/**init**.py
[AutoAPI] Reading files... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/risk/generic_engines.py
[AutoAPI] Reading files... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/risk/agent.py
[AutoAPI] Reading files... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/state_manager.py
[AutoAPI] Reading files... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/base.py
[AutoAPI] Reading files... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/config.py
[AutoAPI] Reading files... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/**init**.py
[AutoAPI] Reading files... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/agent.py
[AutoAPI] Reading files... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/rubiks/state.py
[AutoAPI] Reading files... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/rubiks/**init**.py
[AutoAPI] Reading files... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/rubiks/agent.py
[AutoAPI] Reading files... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/wordle/state.py
[AutoAPI] Reading files... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/wordle/engines.py
[AutoAPI] Reading files... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/wordle/state_manager.py
[AutoAPI] Reading files... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/wordle/config.py
[AutoAPI] Reading files... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/wordle/models.py
[AutoAPI] Reading files... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/wordle/**init**.py
[AutoAPI] Reading files... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/wordle/agent.py
[AutoAPI] Reading files... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/flow_free/state.py
[AutoAPI] Reading files... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/flow_free/engines.py
[AutoAPI] Reading files... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/flow_free/state_manager.py
[AutoAPI] Reading files... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/flow_free/base.py
[AutoAPI] Reading files... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/flow_free/config.py
[AutoAPI] Reading files... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/flow_free/models.py
[AutoAPI] Reading files... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/flow_free/**init**.py
[AutoAPI] Reading files... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/flow_free/agent.py
[AutoAPI] Reading files... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/logic_grid/base.py
[AutoAPI] Reading files... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/logic_grid/game/**init**.py
[AutoAPI] Reading files... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/sudoku/**init**.py
[AutoAPI] Reading files... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/sudoku/game/**init**.py
[AutoAPI] Reading files... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/sudoku/game/board.py
[AutoAPI] Reading files... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/sudoku/game/cell.py
[AutoAPI] Reading files... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/sudoku/game/piece.py
[AutoAPI] Reading files... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/towers_of_hanoi/base.py
[AutoAPI] Reading files... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py
[AutoAPI] Reading files... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/towers_of_hanoi/postiition.py
[AutoAPI] Reading files... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/towers_of_hanoi/move.py
[AutoAPI] Reading files... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/towers_of_hanoi/container.py
[AutoAPI] Reading files... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/towers_of_hanoi/position.py
[AutoAPI] Reading files... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/towers_of_hanoi/prompts.py
[AutoAPI] Reading files... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/towers_of_hanoi/promopts.py
[AutoAPI] Reading files... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/towers_of_hanoi/piece.py
[AutoAPI] Reading files... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/twenty_fourty_eight/**init**.py
[AutoAPI] Reading files... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/twenty_fourty_eight/game.py
[AutoAPI] Reading files... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/twenty_fourty_eight/game/**init**.py
[AutoAPI] Reading files... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py
[AutoAPI] Reading files... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/twenty_fourty_eight/game/piece.py
[AutoAPI] Reading files... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/crossword_puzzle/base.py
[AutoAPI] Reading files... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py
[AutoAPI] Reading files... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/crossword_puzzle/game/cell.py
[AutoAPI] Reading files... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/crossword_puzzle/game/piece.py
[AutoAPI] Reading files... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/word_search/base.py
[AutoAPI] Reading files... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/testing/base.py
[AutoAPI] Reading files... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/testing/**init**.py
[AutoAPI] Reading files... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/mine_sweeper/base.py
[AutoAPI] Reading files... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/mine_sweeper/**init**.py
[AutoAPI] Reading files... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/state.py
[AutoAPI] Reading files... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/engines.py
[AutoAPI] Reading files... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/state_manager.py
[AutoAPI] Reading files... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/config.py
[AutoAPI] Reading files... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/models.py
[AutoAPI] Reading files... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/configurable_config.py
[AutoAPI] Reading files... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/**init**.py
[AutoAPI] Reading files... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/generic_engines.py
[AutoAPI] Reading files... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/utils.py
[AutoAPI] Reading files... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/agent.py
[AutoAPI] Reading files... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/prompts.py
[AutoAPI] Reading files... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/comprehensive_mcp_web.py
[AutoAPI] Reading files... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/launcher.py
[AutoAPI] Reading files... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/config.py
[AutoAPI] Reading files... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mcp_simple_tool_agent.py
[AutoAPI] Reading files... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/integrated_launcher.py
[AutoAPI] Reading files... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/enhanced_parent_self_query_retriever.py
[AutoAPI] Reading files... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/simple_faiss_retriever.py
[AutoAPI] Reading files... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/**init**.py
[AutoAPI] Reading files... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/dynamic_mcp_tool.py
[AutoAPI] Reading files... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mcp_rag_agent.py
[AutoAPI] Reading files... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/fastmcp_runner.py
[AutoAPI] Reading files... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/working_enhanced_retriever.py
[AutoAPI] Reading files... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/csv_viewer.py
[AutoAPI] Reading files... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/fastapi_mcp_server.py
[AutoAPI] Reading files... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/integrated_mcp_system.py
[AutoAPI] Reading files... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/dynamic_activation_mcp.py
[AutoAPI] Reading files... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/enhance_mcp_data.py
[AutoAPI] Reading files... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/simple_rag_mcp_agent.py
[AutoAPI] Reading files... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mcp_simple_rag_agent.py
[AutoAPI] Reading files... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/production_mcp_tool.py
[AutoAPI] Reading files... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/self_query_mcp_agent.py
[AutoAPI] Reading files... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/manager.py
[AutoAPI] Reading files... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/complete_mcp_with_parent_retriever.py
[AutoAPI] Reading files... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/mcp_agent.py
[AutoAPI] Reading files... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/transferable_mcp_agent.py
[AutoAPI] Reading files... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/**init**.py
[AutoAPI] Reading files... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/documentation_agent.py
[AutoAPI] Reading files... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py
[AutoAPI] Reading files... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/cli/**init**.py
[AutoAPI] Reading files... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/cli/mcp_manager.py
[AutoAPI] Reading files... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/discovery/server_discovery.py
[AutoAPI] Reading files... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/discovery/analyzer.py
[AutoAPI] Reading files... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/discovery/**init**.py
[AutoAPI] Reading files... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/tools/server_selector.py
[AutoAPI] Reading files... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/tools/**init**.py
[AutoAPI] Reading files... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/tools/server_tester.py
[AutoAPI] Reading files... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/tools/ai_assistant.py
[AutoAPI] Reading files... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/integration/aug_llm_mcp_extension.py
[AutoAPI] Reading files... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mixins/mcp_mixin.py
[AutoAPI] Reading files... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mixins/**init**.py
[AutoAPI] Reading files... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/servers/http_server.py
[AutoAPI] Reading files... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/servers/**init**.py
[AutoAPI] Reading files... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/servers/dataflow_mcp_server.py
[AutoAPI] Reading files... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/servers/simple_http_server.py
[AutoAPI] Reading files... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/servers/dataflow_server.py
[AutoAPI] Reading files... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/documentation/doc_loader.py
[AutoAPI] Reading files... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/documentation/**init**.py
[AutoAPI] Reading files... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/utils/extract_mcp_github_repos.py
[AutoAPI] Reading files... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/utils/**init**.py
[AutoAPI] Reading files... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/installers/advanced_code_installer.py
[AutoAPI] Reading files... [100%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/installers/**init**.py
[AutoAPI] Reading files... [100%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/installers/safe_pattern_installer.py
[AutoAPI] Reading files... [100%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/installers/config_manager.py
[AutoAPI] Reading files... [100%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/integration.py
[AutoAPI] Reading files... [100%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/config.py
[AutoAPI] Reading files... [100%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/github_mass_downloader.py
[AutoAPI] Reading files... [100%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/core.py
[AutoAPI] Reading files... [100%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/**init**.py
[AutoAPI] Reading files... [100%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/discovery.py
[AutoAPI] Reading files... [100%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/installers.py
[AutoAPI] Reading files... [100%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/legacy_core.py

WARNING: Cannot resolve import of src.haive.core.engine.document.splitters.base.CharacterTextSplitter in src.haive.core.engine.document.splitters.engine [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.core.engine.document.splitters.base.HTMLHeaderTextSplitter in src.haive.core.engine.document.splitters.engine [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.core.engine.document.splitters.base.LatexTextSplitter in src.haive.core.engine.document.splitters.engine [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.core.engine.document.splitters.base.MarkdownTextSplitter in src.haive.core.engine.document.splitters.engine [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.core.engine.document.splitters.base.NLTKTextSplitter in src.haive.core.engine.document.splitters.engine [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.core.engine.document.splitters.base.PythonCodeTextSplitter in src.haive.core.engine.document.splitters.engine [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.core.engine.document.splitters.base.RecursiveCharacterTextSplitter in src.haive.core.engine.document.splitters.engine [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.core.engine.document.splitters.base.RecursiveJsonSplitter in src.haive.core.engine.document.splitters.engine [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.core.engine.document.splitters.base.SentenceTransformersTokenTextSplitter in src.haive.core.engine.document.splitters.engine [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.core.engine.document.splitters.base.SpacyTextSplitter in src.haive.core.engine.document.splitters.engine [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.core.engine.document.splitters.base.TokenTextSplitter in src.haive.core.engine.document.splitters.engine [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.agents.reflection.models.Improvement in src.haive.agents.reflection [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.agents.reflection.models.to_prompt in src.haive.agents.reflection [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.agents.reflection.models.validate_grade_matches_score in src.haive.agents.reflection [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.agents.planning.plan_execute_v3.models.Plan in src.haive.agents.planning.plan_execute_v3.engines [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.agents.planning.plan_execute_v3.models.PlanValidationResult in src.haive.agents.planning.plan_execute_v3.engines [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.agents.planning.plan_execute_v3.models.Step in src.haive.agents.planning.plan_execute_v3.engines [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.agents.planning.plan_execute_v3.models.StepType in src.haive.agents.planning.plan_execute_v3.engines [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.agents.planning.plan_execute_v3.prompts.format_executor_prompt in src.haive.agents.planning.plan_execute_v3.engines [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.agents.planning.plan_execute_v3.prompts.format_monitor_prompt in src.haive.agents.planning.plan_execute_v3.engines [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.agents.planning.plan_execute_v3.prompts.format_planner_prompt in src.haive.agents.planning.plan_execute_v3.engines [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.agents.planning.plan_execute_v3.prompts.format_replanner_prompt in src.haive.agents.planning.plan_execute_v3.engines [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.agents.planning.plan_execute_v3.prompts.format_validator_prompt in src.haive.agents.planning.plan_execute_v3.engines [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.agents.archive.meta.agent in src.haive.agents.archive.meta [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.agents.archive.meta.agent in src.haive.agents.archive.meta [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.agents.archive.meta.agent in src.haive.agents.archive.meta [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.agents.archive.meta.agent in src.haive.agents.archive.meta [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.agents.archive.meta.agent in src.haive.agents.archive.meta [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.agents.archive.meta.agent in src.haive.agents.archive.meta [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.agents.archive.meta.agent in src.haive.agents.archive.meta [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.agents.archive.meta.agent in src.haive.agents.archive.meta [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.agents.archive.meta.agent in src.haive.agents.archive.meta [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.agents.archive.meta.agent in src.haive.agents.archive.meta [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.agents.archive.meta.agent in src.haive.agents.archive.meta [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.agents.archive.meta.agent in src.haive.agents.archive.meta [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.models.llm.base in src.haive.dataflow.base [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.models.llm.base in src.haive.dataflow.base [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.models.llm.base in src.haive.dataflow.base [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.models.llm.base in src.haive.dataflow.base [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.models.llm.base in src.haive.dataflow.base [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.models.llm.base in src.haive.dataflow.base [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.models.llm.provider_types in src.haive.dataflow.base [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.engine.agent.agent in src.haive.dataflow.api.registry [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.engine.agent.agent in src.haive.dataflow.api.registry [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.api.registry in src.haive.dataflow.api.router [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.engine.agent.persistence.memory_config in src.haive.dataflow.api.game_agent [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.engine.agent.persistence.postgres_config in src.haive.dataflow.api.game_agent [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.engine.agent.persistence.memory_config in src.haive.dataflow.game_agent [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.engine.agent.persistence.postgres_config in src.haive.dataflow.game_agent [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.registry.registry.models in src.haive.dataflow.registry.lazy_core [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.llms.api.llms.models in src.haive.dataflow.llms.api [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.persistence.config.environment in src.haive.dataflow.persistence.conversations [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.persistence.persistence.supabase_adapter in src.haive.dataflow.persistence.conversations [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.persistence.config.environment in src.haive.dataflow.persistence.supabase_adapter [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.persistence.persistence.factory in src.haive.dataflow.persistence.supabase_adapter [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.persistence.persistence.factory in src.haive.dataflow.persistence.supabase_adapter [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.persistence.persistence.factory in src.haive.dataflow.persistence.supabase_adapter [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.persistence.persistence.factory in src.haive.dataflow.persistence.supabase_adapter [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.internal_websockets.auth.credits in src.haive.dataflow.internal_websockets.handlers [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.internal_websockets.auth.credits in src.haive.dataflow.internal_websockets.handlers [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.internal_websockets.config.settings in src.haive.dataflow.internal_websockets.handlers [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.internal_websockets.internal_websockets.manager in src.haive.dataflow.internal_websockets.handlers [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.internal_websockets.persistence.conversations in src.haive.dataflow.internal_websockets.handlers [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.internal_websockets.auth.supabase in src.haive.dataflow.internal_websockets.manager [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.internal_websockets.config.environment in src.haive.dataflow.internal_websockets.manager [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.engine.aug_llm in src.haive.dataflow.api.base [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.models.llm.base in src.haive.dataflow.api.base [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.models.llm.base in src.haive.dataflow.api.base [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.models.llm.base in src.haive.dataflow.api.base [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.models.llm.base in src.haive.dataflow.api.base [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.models.llm.base in src.haive.dataflow.api.base [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.models.llm.base in src.haive.dataflow.api.base [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.models.llm.provider_types in src.haive.dataflow.api.base [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.api.registry in src.haive.dataflow.api.app_dep [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.api.router in src.haive.dataflow.api.app_dep [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.api.game_socket in src.haive.dataflow.api.game_api [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.engine.agent.agent in src.haive.dataflow.api.game_api [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.persistence.supabase_config in src.haive.dataflow.api.game_api [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.schema.state_schema in src.haive.dataflow.api.game_api [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.api.game_agent in src.haive.dataflow.api.tic_tac_toe_api [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.api.game_agent in src.haive.dataflow.api.tic_tac_toe_api [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.api.game_agent in src.haive.dataflow.api.connect4_api [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.api.game_agent in src.haive.dataflow.api.connect4_api [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.api.game_router in src.haive.dataflow.api.run_game_api [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.api.game_router in src.haive.dataflow.api.run_game_api [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.api.game_router in src.haive.dataflow.api.run_game_api [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.utils.haive_discovery in src.haive.dataflow.api.game_router_enhanced [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.utils.haive_discovery in src.haive.dataflow.api.game_router_enhanced [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.llms.api.llms.models in src.haive.dataflow.api.llms.api [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.utils.haive_discovery in src.haive.dataflow.api.routes.agent_discovery_routes_enhanced [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.utils.haive_discovery in src.haive.dataflow.api.routes.agent_discovery_routes_enhanced [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.utils.haive_discovery in src.haive.dataflow.api.routes.tools_routes_fixed [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.utils.haive_discovery in src.haive.dataflow.api.routes.tools_routes_fixed [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.utils.haive_discovery in src.haive.dataflow.api.routes.tools_routes_fixed [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.utils.haive_discovery in src.haive.dataflow.api.routes.tools_routes_fixed [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.utils.haive_discovery in src.haive.dataflow.api.routes.tools_routes_fixed [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.utils.haive_discovery in src.haive.dataflow.api.routes.tools_routes_fixed [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.utils.haive_discovery in src.haive.dataflow.api.routes.agent_discovery_routes_fixed [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.utils.haive_discovery in src.haive.dataflow.api.routes.agent_discovery_routes_fixed [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.utils.haive_discovery in src.haive.dataflow.api.routes.agent_discovery_routes_fixed [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.utils.haive_discovery in src.haive.dataflow.api.routes.agent_discovery_routes_fixed [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.auth.dependencies in src.haive.dataflow.api.routes.agent_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.auth.supabase in src.haive.dataflow.api.routes.agent_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.engine.agent.config in src.haive.dataflow.api.routes.agent_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.engine.aug_llm in src.haive.dataflow.api.routes.agent_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.models.llm.base in src.haive.dataflow.api.routes.agent_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.models.llm.base in src.haive.dataflow.api.routes.agent_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.models.llm.base in src.haive.dataflow.api.routes.agent_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.models.llm.base in src.haive.dataflow.api.routes.agent_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.models.llm.base in src.haive.dataflow.api.routes.agent_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.models.llm.base in src.haive.dataflow.api.routes.agent_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.models.llm.provider_types in src.haive.dataflow.api.routes.agent_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.auth.credits in src.haive.dataflow.api.routes.conversation_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.auth.credits in src.haive.dataflow.api.routes.conversation_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.auth.dependencies in src.haive.dataflow.api.routes.conversation_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.config.settings in src.haive.dataflow.api.routes.conversation_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.persistence.conversations in src.haive.dataflow.api.routes.conversation_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.auth.middleware in src.haive.dataflow.api.routes.llm_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.engine.aug_llm in src.haive.dataflow.api.routes.llm_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.models.llm.base in src.haive.dataflow.api.routes.llm_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.models.llm.base in src.haive.dataflow.api.routes.llm_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.models.llm.base in src.haive.dataflow.api.routes.llm_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.models.llm.base in src.haive.dataflow.api.routes.llm_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.models.llm.base in src.haive.dataflow.api.routes.llm_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.models.llm.base in src.haive.dataflow.api.routes.llm_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.models.llm.provider_types in src.haive.dataflow.api.routes.llm_routes [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.utils.haive_discovery in src.haive.dataflow.api.routes.tools_routes_enhanced [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.utils.haive_discovery in src.haive.dataflow.api.routes.tools_routes_enhanced [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.routes.utils.haive_discovery in src.haive.dataflow.api.routes.tools_routes_enhanced [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.middleware.config.environment in src.haive.dataflow.api.middleware.supabase_logging [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.middleware.auth.supabase in src.haive.dataflow.api.middleware.auth [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.api.middleware.config.environment in src.haive.dataflow.api.middleware.auth [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.registry.providers.utils.logging in src.haive.dataflow.registry.providers.base [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.registry.providers.providers.base in src.haive.dataflow.registry.providers.agent_provider [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.registry.providers.utils.logging in src.haive.dataflow.registry.providers.agent_provider [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.registry.importers.registry.core in src.haive.dataflow.registry.importers.embeddings_importer [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.registry.importers.registry.core in src.haive.dataflow.registry.importers.embeddings_importer [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.registry.importers.registry.core in src.haive.dataflow.registry.importers.embeddings_importer [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.registry.importers.registry.core in src.haive.dataflow.registry.importers.embeddings_importer [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.registry.importers.registry.serialization in src.haive.dataflow.registry.importers.embeddings_importer [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.registry.registries.db.supabase in src.haive.dataflow.registry.registries.model_registry [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.registry.registries.db.supabase in src.haive.dataflow.registry.registries.model_registry [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.auth.auth.supabase in src.haive.dataflow.auth.middleware [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.auth.auth.supabase in src.haive.dataflow.auth.dependencies [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.auth.config.environment in src.haive.dataflow.auth.dependencies [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.auth.config.environment in src.haive.dataflow.auth.supabase [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.auth.config.environment in src.haive.dataflow.auth.credits [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.providers.utils.logging in src.haive.dataflow.providers.base [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.providers.providers.base in src.haive.dataflow.providers.agent_provider [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.providers.utils.logging in src.haive.dataflow.providers.agent_provider [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.mcp.registry.models in src.haive.dataflow.mcp.health [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.mcp.registry.models in src.haive.dataflow.mcp.health [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.mcp.registry.models in src.haive.dataflow.mcp.client [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.mcp.registry.models in src.haive.dataflow.mcp.client [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.mcp.registry.models in src.haive.dataflow.mcp.client [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.mcp.registry.models in src.haive.dataflow.mcp.client [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.mcp.registry.models in src.haive.dataflow.mcp.client [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.mcp.registry.models in src.haive.dataflow.mcp.discovery [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.mcp.registry.models in src.haive.dataflow.mcp.discovery [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.mcp.registry.models in src.haive.dataflow.mcp.discovery [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.mcp.registry.models in src.haive.dataflow.mcp.discovery [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.mcp.registry.models in src.haive.dataflow.mcp.discovery [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.mcp.registry.models in src.haive.dataflow.mcp.discovery [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.mcp.registry.models in src.haive.dataflow.mcp.discovery [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.db.db.supabase in src.haive.dataflow.db.inspect_supabase [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.db.db.supabase in src.haive.dataflow.db.inspect_supabase [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.db.db.supabase in src.haive.dataflow.db.inspect_supabase [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.db.db.supabase in src.haive.dataflow.db.inspect_supabase [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.db.db.supabase in src.haive.dataflow.db.inspect_supabase [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.conversations.persistence.factory in src.haive.dataflow.conversations.manager [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.conversations.persistence.factory in src.haive.dataflow.conversations.manager [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.conversations.persistence.factory in src.haive.dataflow.conversations.manager [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.conversations.persistence.factory in src.haive.dataflow.conversations.manager [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.conversations.persistence.postgres_config in src.haive.dataflow.conversations.manager [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.registries.db.supabase in src.haive.dataflow.registries.model_registry [autoapi.python_import_resolution]
WARNING: Cannot resolve import of unknown module src.haive.dataflow.registries.db.supabase in src.haive.dataflow.registries.model_registry [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_space.Config in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_board.add_space in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_board.connect_spaces in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_board.get_all_pieces in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_board.get_column in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_board.get_connected_spaces in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_board.get_player_pieces in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_space.get_property in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_board.get_row in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_board.get_space_at in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_board.get_space_at_position in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_board.initialize_grid in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_board.is_position_valid in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_space.place_piece in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_space.remove_piece in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_space.set_property in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_board.size in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_board.validate_dimensions in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.abort in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.add_player in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.can_take_action in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.check_end_condition in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.create_game in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.create_position in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.determine_winner in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.end_turn in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.finish in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.get_container in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.get_current_player in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.get_piece in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.get_state_for_player in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.get_valid_moves in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.initialize in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.is_action_on_cooldown in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.is_finished in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.is_valid_player_count in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.pause in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.process_move in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.record_action in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.register_callback in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.resume in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.reverse_turn_order in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.set_cooldown in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.setup_game in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.skip_turn in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.start in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.start_turn in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.unregister_callback in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.update in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.update_game_state in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_game.validate_player_count in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_position.axial_coords in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_position.chebyshev_distance in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_space.coordinates in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_position.display_coords in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_position.distance in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_position.distance_to in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_position.from_axial in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_position.manhattan_distance in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_position.neighbors in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_position.neighbors_with_diagonals in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_position.offset in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_position.serialize in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_position.validate_coordinates in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_position.validate_cube_coords in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_space.add_connection in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_space.get_grid_position in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_space.is_connected_to in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_space.is_occupied in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.core_space.remove_connection in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.piece.assign_to_player in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.piece.can_move_to in src.haive.games.core.game [autoapi.python_import_resolution]
WARNING: Cannot resolve import of src.haive.games.core.game.piece.place_at in src.haive.games.core.game [autoapi.python_import_resolution]
[AutoAPI] Mapping Data... [ 0%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/errors.py
[AutoAPI] Mapping Data... [ 0%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/**init**.py
[AutoAPI] Mapping Data... [ 0%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/**init**.py
[AutoAPI] Mapping Data... [ 0%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/logging_config.py
[AutoAPI] Mapping Data... [ 0%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/**init**.py
[AutoAPI] Mapping Data... [ 0%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/dynamic_choice_model.py
[AutoAPI] Mapping Data... [ 0%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/named_list.py
[AutoAPI] Mapping Data... [ 0%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/documents/**init**.py
[AutoAPI] Mapping Data... [ 0%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/models/documents/github_repo.py
[AutoAPI] Mapping Data... [ 0%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/structures/tree.py
[AutoAPI] Mapping Data... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/structures/named_dict.py
[AutoAPI] Mapping Data... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/timestamp_mixin.py
[AutoAPI] Mapping Data... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/mcp_mixin.py
[AutoAPI] Mapping Data... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/recompile_mixin.py
[AutoAPI] Mapping Data... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/engine_mixin.py
[AutoAPI] Mapping Data... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/structured_output_mixin.py
[AutoAPI] Mapping Data... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/tool_route_mixin.py
[AutoAPI] Mapping Data... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/getter_mixin.py
[AutoAPI] Mapping Data... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/**init**.py
[AutoAPI] Mapping Data... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/prompt_template_mixin.py
[AutoAPI] Mapping Data... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/tool_list_mixin.py
[AutoAPI] Mapping Data... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/identifier.py
[AutoAPI] Mapping Data... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/secure_config.py
[AutoAPI] Mapping Data... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/dynamic_tool_route_mixin.py
[AutoAPI] Mapping Data... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/state_interface_mixin.py
[AutoAPI] Mapping Data... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/general/state.py
[AutoAPI] Mapping Data... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/general/id.py
[AutoAPI] Mapping Data... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/general/**init**.py
[AutoAPI] Mapping Data... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/general/metadata.py
[AutoAPI] Mapping Data... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/general/timestamp.py
[AutoAPI] Mapping Data... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/general/serialization.py
[AutoAPI] Mapping Data... [ 1%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/general/version.py
[AutoAPI] Mapping Data... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/mixins/mixins/**init**.py
[AutoAPI] Mapping Data... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/types/abc_root_wrapper.py
[AutoAPI] Mapping Data... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/types/general.py
[AutoAPI] Mapping Data... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/types/**init**.py
[AutoAPI] Mapping Data... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/types/protocols/general_protocols.py
[AutoAPI] Mapping Data... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/types/protocols/**init**.py
[AutoAPI] Mapping Data... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/types/protocols/schema_protocols.py
[AutoAPI] Mapping Data... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/common/types/protocols/engine_protocols.py
[AutoAPI] Mapping Data... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/base.py
[AutoAPI] Mapping Data... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/memory.py
[AutoAPI] Mapping Data... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/factory.py
[AutoAPI] Mapping Data... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/sqlite_config.py
[AutoAPI] Mapping Data... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/postgres_saver_override.py
[AutoAPI] Mapping Data... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/**init**.py
[AutoAPI] Mapping Data... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/handlers.py
[AutoAPI] Mapping Data... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/serializers.py
[AutoAPI] Mapping Data... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/utils.py
[AutoAPI] Mapping Data... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/types.py
[AutoAPI] Mapping Data... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/postgres_config.py
[AutoAPI] Mapping Data... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/postgres_saver_with_thread_creation.py
[AutoAPI] Mapping Data... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/supabase_config.py
[AutoAPI] Mapping Data... [ 2%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/base.py
[AutoAPI] Mapping Data... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/connection.py
[AutoAPI] Mapping Data... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/memory.py
[AutoAPI] Mapping Data... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/factory.py
[AutoAPI] Mapping Data... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/postgres.py
[AutoAPI] Mapping Data... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/**init**.py
[AutoAPI] Mapping Data... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/types.py
[AutoAPI] Mapping Data... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/embeddings.py
[AutoAPI] Mapping Data... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/wrappers/memory.py
[AutoAPI] Mapping Data... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/wrappers/postgres.py
[AutoAPI] Mapping Data... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/wrappers/**init**.py
[AutoAPI] Mapping Data... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/**init**.py
[AutoAPI] Mapping Data... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/metadata_mixin.py
[AutoAPI] Mapping Data... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/metadata.py
[AutoAPI] Mapping Data... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/export_llm_models_to_csv.py
[AutoAPI] Mapping Data... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/base.py
[AutoAPI] Mapping Data... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/factory.py
[AutoAPI] Mapping Data... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/rate_limiting_mixin.py
[AutoAPI] Mapping Data... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/**init**.py
[AutoAPI] Mapping Data... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/provider_types.py
[AutoAPI] Mapping Data... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers.py
[AutoAPI] Mapping Data... [ 3%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/together.py
[AutoAPI] Mapping Data... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/cohere.py
[AutoAPI] Mapping Data... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/anthropic.py
[AutoAPI] Mapping Data... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/base.py
[AutoAPI] Mapping Data... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/openai.py
[AutoAPI] Mapping Data... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/fireworks.py
[AutoAPI] Mapping Data... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/mistral.py
[AutoAPI] Mapping Data... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/groq.py
[AutoAPI] Mapping Data... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/xai.py
[AutoAPI] Mapping Data... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/**init**.py
[AutoAPI] Mapping Data... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/ollama.py
[AutoAPI] Mapping Data... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/huggingface.py
[AutoAPI] Mapping Data... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/azure.py
[AutoAPI] Mapping Data... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/bedrock.py
[AutoAPI] Mapping Data... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/ai21.py
[AutoAPI] Mapping Data... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/replicate.py
[AutoAPI] Mapping Data... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/google.py
[AutoAPI] Mapping Data... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/llm/providers/nvidia.py
[AutoAPI] Mapping Data... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/embeddings/base.py
[AutoAPI] Mapping Data... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/embeddings/**init**.py
[AutoAPI] Mapping Data... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/embeddings/provider_types.py
[AutoAPI] Mapping Data... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/embeddings/filter/base.py
[AutoAPI] Mapping Data... [ 4%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/embeddings/filter/**init**.py
[AutoAPI] Mapping Data... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/vectorstore/base.py
[AutoAPI] Mapping Data... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/vectorstore/**init**.py
[AutoAPI] Mapping Data... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/retriever/base.py
[AutoAPI] Mapping Data... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/retriever/asknews_retriever.py
[AutoAPI] Mapping Data... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/retriever/vectorstore_retriever.py
[AutoAPI] Mapping Data... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/retriever/**init**.py
[AutoAPI] Mapping Data... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/retriever/community/base.py
[AutoAPI] Mapping Data... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/retriever/retrievers/time_weighted.py
[AutoAPI] Mapping Data... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/retriever/retrievers/parent_document.py
[AutoAPI] Mapping Data... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/retriever/retrievers/self_query.py
[AutoAPI] Mapping Data... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/retriever/retrievers/multiqery.py
[AutoAPI] Mapping Data... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/models/retriever/retrievers/ensemble.py
[AutoAPI] Mapping Data... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/registry/base.py
[AutoAPI] Mapping Data... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/registry/memory.py
[AutoAPI] Mapping Data... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/registry/factory.py
[AutoAPI] Mapping Data... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/registry/**init**.py
[AutoAPI] Mapping Data... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/registry/decorators.py
[AutoAPI] Mapping Data... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/registry/dynamic_registry.py
[AutoAPI] Mapping Data... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/registry/manager.py
[AutoAPI] Mapping Data... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/tools/store_tools.py
[AutoAPI] Mapping Data... [ 5%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/tools/interrupt_tool_wrapper.py
[AutoAPI] Mapping Data... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/tools/store_manager.py
[AutoAPI] Mapping Data... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/tools/**init**.py
[AutoAPI] Mapping Data... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/runtime/**init**.py
[AutoAPI] Mapping Data... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/runtime/base/base.py
[AutoAPI] Mapping Data... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/runtime/base/protocols.py
[AutoAPI] Mapping Data... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/runtime/extension/base.py
[AutoAPI] Mapping Data... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/runtime/extension/protocols.py
[AutoAPI] Mapping Data... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/config.py
[AutoAPI] Mapping Data... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/model_utils.py
[AutoAPI] Mapping Data... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/parser_utils.py
[AutoAPI] Mapping Data... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/tool_utils.py
[AutoAPI] Mapping Data... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/file_utils.py
[AutoAPI] Mapping Data... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/config_utils.py
[AutoAPI] Mapping Data... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/inspection.py
[AutoAPI] Mapping Data... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/getter_mixin.py
[AutoAPI] Mapping Data... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/mermaid_utils.py
[AutoAPI] Mapping Data... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/collections.py
[AutoAPI] Mapping Data... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/**init**.py
[AutoAPI] Mapping Data... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/chat_utils.py
[AutoAPI] Mapping Data... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/runnable_config_utils.py
[AutoAPI] Mapping Data... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/visualize_graph_utils.py
[AutoAPI] Mapping Data... [ 6%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/tool_list.py
[AutoAPI] Mapping Data... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/message_utils.py
[AutoAPI] Mapping Data... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/logging_utils.py
[AutoAPI] Mapping Data... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/env_utils.py
[AutoAPI] Mapping Data... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/state_utils.py
[AutoAPI] Mapping Data... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/doc_utils.py
[AutoAPI] Mapping Data... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/interrupt_utils.py
[AutoAPI] Mapping Data... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/serialization.py
[AutoAPI] Mapping Data... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/pydantic_utils/ui.py
[AutoAPI] Mapping Data... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/pydantic_utils/general.py
[AutoAPI] Mapping Data... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/pydantic_utils/**init**.py
[AutoAPI] Mapping Data... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/pydantic_utils/sync_properties.py
[AutoAPI] Mapping Data... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/tools/**init**.py
[AutoAPI] Mapping Data... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/utils/tools/tool_schema_generator.py
[AutoAPI] Mapping Data... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/types/tree_leaf.py
[AutoAPI] Mapping Data... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/types/dynamic_enum.py
[AutoAPI] Mapping Data... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/types/serializable_callable.py
[AutoAPI] Mapping Data... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/types/**init**.py
[AutoAPI] Mapping Data... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/types/advanced_registry.py
[AutoAPI] Mapping Data... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/types/dynamic_literal.py
[AutoAPI] Mapping Data... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/types/general/file_types.py
[AutoAPI] Mapping Data... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/types/general/**init**.py
[AutoAPI] Mapping Data... [ 7%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/types/general/programming_languages.py
[AutoAPI] Mapping Data... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/**init**.py
[AutoAPI] Mapping Data... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embeddings.py
[AutoAPI] Mapping Data... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/config.py
[AutoAPI] Mapping Data... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/factory.py
[AutoAPI] Mapping Data... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/mcp_config.py
[AutoAPI] Mapping Data... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/**init**.py
[AutoAPI] Mapping Data... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/aug_llm/utils.py
[AutoAPI] Mapping Data... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/base/base.py
[AutoAPI] Mapping Data... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/base/factory.py
[AutoAPI] Mapping Data... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/base/protocols.py
[AutoAPI] Mapping Data... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/base/registry.py
[AutoAPI] Mapping Data... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/base/**init**.py
[AutoAPI] Mapping Data... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/base/types.py
[AutoAPI] Mapping Data... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/base/reference.py
[AutoAPI] Mapping Data... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/universal_loader.py
[AutoAPI] Mapping Data... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/config.py
[AutoAPI] Mapping Data... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/factory.py
[AutoAPI] Mapping Data... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/**init**.py
[AutoAPI] Mapping Data... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/engine.py
[AutoAPI] Mapping Data... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/processors.py
[AutoAPI] Mapping Data... [ 8%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/agents.py
[AutoAPI] Mapping Data... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/path_analysis.py
[AutoAPI] Mapping Data... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/transformers/base.py
[AutoAPI] Mapping Data... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/transformers/**init**.py
[AutoAPI] Mapping Data... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/transformers/engine.py
[AutoAPI] Mapping Data... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/transformers/types.py
[AutoAPI] Mapping Data... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/base/schema.py
[AutoAPI] Mapping Data... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/base/**init**.py
[AutoAPI] Mapping Data... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/sources/base.py
[AutoAPI] Mapping Data... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/sources/**init**.py
[AutoAPI] Mapping Data... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/sources/web.py
[AutoAPI] Mapping Data... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/sources/local.py
[AutoAPI] Mapping Data... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/cache_manager.py
[AutoAPI] Mapping Data... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/base.py
[AutoAPI] Mapping Data... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/strategy.py
[AutoAPI] Mapping Data... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/path_analyzer.py
[AutoAPI] Mapping Data... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/registry.py
[AutoAPI] Mapping Data... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/**init**.py
[AutoAPI] Mapping Data... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/source_base.py
[AutoAPI] Mapping Data... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/engine.py
[AutoAPI] Mapping Data... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/auto_loader.py
[AutoAPI] Mapping Data... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/base_new.py
[AutoAPI] Mapping Data... [ 9%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/auto_registry.py
[AutoAPI] Mapping Data... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/auto_factory.py
[AutoAPI] Mapping Data... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/base/base.py
[AutoAPI] Mapping Data... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/base/schema.py
[AutoAPI] Mapping Data... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/base/**init**.py
[AutoAPI] Mapping Data... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/base/methods.py
[AutoAPI] Mapping Data... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/adapters/base.py
[AutoAPI] Mapping Data... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/adapters/**init**.py
[AutoAPI] Mapping Data... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/adapters/local.py
[AutoAPI] Mapping Data... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/web_huggingface_enhanced.py
[AutoAPI] Mapping Data... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/files_scientific.py
[AutoAPI] Mapping Data... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/web_advanced.py
[AutoAPI] Mapping Data... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/web_social.py
[AutoAPI] Mapping Data... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/file_advanced.py
[AutoAPI] Mapping Data... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/**init**.py
[AutoAPI] Mapping Data... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/cloud.py
[AutoAPI] Mapping Data... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/database_advanced.py
[AutoAPI] Mapping Data... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/web_github_enhanced.py
[AutoAPI] Mapping Data... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/files_text.py
[AutoAPI] Mapping Data... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/services.py
[AutoAPI] Mapping Data... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/database.py
[AutoAPI] Mapping Data... [ 10%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/web_api.py
[AutoAPI] Mapping Data... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/files_office.py
[AutoAPI] Mapping Data... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/web.py
[AutoAPI] Mapping Data... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/files_code.py
[AutoAPI] Mapping Data... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/files_data.py
[AutoAPI] Mapping Data... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/specific/files_media.py
[AutoAPI] Mapping Data... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/chat_gpt_loader.py
[AutoAPI] Mapping Data... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/final_missing_source.py
[AutoAPI] Mapping Data... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/analytics_sources.py
[AutoAPI] Mapping Data... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/factory.py
[AutoAPI] Mapping Data... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/implementation.py
[AutoAPI] Mapping Data... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/file_sources.py
[AutoAPI] Mapping Data... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/final_sources.py
[AutoAPI] Mapping Data... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/enhanced_registry.py
[AutoAPI] Mapping Data... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/additional_sources.py
[AutoAPI] Mapping Data... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/completion_sources.py
[AutoAPI] Mapping Data... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/messaging_sources.py
[AutoAPI] Mapping Data... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/web_sources.py
[AutoAPI] Mapping Data... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/registry.py
[AutoAPI] Mapping Data... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/**init**.py
[AutoAPI] Mapping Data... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/source_types.py
[AutoAPI] Mapping Data... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/essential_sources.py
[AutoAPI] Mapping Data... [ 11%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/groups.py
[AutoAPI] Mapping Data... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/communication_sources.py
[AutoAPI] Mapping Data... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/cloud_storage_sources.py
[AutoAPI] Mapping Data... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/source_base.py
[AutoAPI] Mapping Data... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/source_analysis.py
[AutoAPI] Mapping Data... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/extended_sources.py
[AutoAPI] Mapping Data... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/business_sources.py
[AutoAPI] Mapping Data... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/specialized_sources.py
[AutoAPI] Mapping Data... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/bulk_sources.py
[AutoAPI] Mapping Data... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/database_sources.py
[AutoAPI] Mapping Data... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/base.py
[AutoAPI] Mapping Data... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/blackboard_source.py
[AutoAPI] Mapping Data... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/youtube_audio_source.py
[AutoAPI] Mapping Data... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/ifixit_source.py
[AutoAPI] Mapping Data... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/college_confidential.py
[AutoAPI] Mapping Data... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/wikipedia_source.py
[AutoAPI] Mapping Data... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/imsdb_source.py
[AutoAPI] Mapping Data... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/**init**.py
[AutoAPI] Mapping Data... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/bilibili_source.py
[AutoAPI] Mapping Data... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/youtube_source.py
[AutoAPI] Mapping Data... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/hacker_news_source.py
[AutoAPI] Mapping Data... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/arxiv_source.py
[AutoAPI] Mapping Data... [ 12%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/az_lyrics_source.py
[AutoAPI] Mapping Data... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/read_the_docs_source.py
[AutoAPI] Mapping Data... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/remote/diffbot_source.py
[AutoAPI] Mapping Data... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/base/base.py
[AutoAPI] Mapping Data... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/base/**init**.py
[AutoAPI] Mapping Data... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/chat/base.py
[AutoAPI] Mapping Data... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/chat/**init**.py
[AutoAPI] Mapping Data... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/database/**init**.py
[AutoAPI] Mapping Data... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/database/types.py
[AutoAPI] Mapping Data... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/json_source.py
[AutoAPI] Mapping Data... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/yaml_source.py
[AutoAPI] Mapping Data... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/base.py
[AutoAPI] Mapping Data... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/rtf_source.py
[AutoAPI] Mapping Data... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/docx_source.py
[AutoAPI] Mapping Data... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/ppt_source.py
[AutoAPI] Mapping Data... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/txt_source.py
[AutoAPI] Mapping Data... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/srt_source.py
[AutoAPI] Mapping Data... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/enex_source.py
[AutoAPI] Mapping Data... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/git_source.py
[AutoAPI] Mapping Data... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/mhtml_source.py
[AutoAPI] Mapping Data... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/pdf.py
[AutoAPI] Mapping Data... [ 13%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/**init**.py
[AutoAPI] Mapping Data... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/html_source.py
[AutoAPI] Mapping Data... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/md_source.py
[AutoAPI] Mapping Data... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/pdf_source.py
[AutoAPI] Mapping Data... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/python_source.py
[AutoAPI] Mapping Data... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/toml_source.py
[AutoAPI] Mapping Data... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/csv_source.py
[AutoAPI] Mapping Data... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/excel_source.py
[AutoAPI] Mapping Data... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/types.py
[AutoAPI] Mapping Data... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/notebook_source.py
[AutoAPI] Mapping Data... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/bibtex_source.py
[AutoAPI] Mapping Data... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/vsdx_source.py
[AutoAPI] Mapping Data... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/xml_source.py
[AutoAPI] Mapping Data... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/xlsx_source.py
[AutoAPI] Mapping Data... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/rst_source.py
[AutoAPI] Mapping Data... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/chm_source.py
[AutoAPI] Mapping Data... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/odt_source.py
[AutoAPI] Mapping Data... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/xls_source.py
[AutoAPI] Mapping Data... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/markdown_source.py
[AutoAPI] Mapping Data... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/epub_source.py
[AutoAPI] Mapping Data... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/local/programming_languages/**init**.py
[AutoAPI] Mapping Data... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/utils/**init**.py
[AutoAPI] Mapping Data... [ 14%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/base.py
[AutoAPI] Mapping Data... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/config.py
[AutoAPI] Mapping Data... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/**init**.py
[AutoAPI] Mapping Data... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/engine.py
[AutoAPI] Mapping Data... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/types/**init**.py
[AutoAPI] Mapping Data... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/types/enums.py
[AutoAPI] Mapping Data... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/base.py
[AutoAPI] Mapping Data... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/**init**.py
[AutoAPI] Mapping Data... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/types.py
[AutoAPI] Mapping Data... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/discovery.py
[AutoAPI] Mapping Data... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/vectorstore.py
[AutoAPI] Mapping Data... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/ZillizVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/ClickHouseVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/MongoDBAtlasVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/InMemoryVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/VectaraVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/ElasticsearchVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/USearchVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/WeaviateVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/MarqoVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/**init**.py
[AutoAPI] Mapping Data... [ 15%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/PGVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/AnnoyVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/SupabaseVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/CassandraVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/AzureSearchVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/OpenSearchVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/PineconeVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/ChromaVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/AmazonOpenSearchVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/Neo4jVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/QdrantVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/TypesenseVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/DocArrayVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/LanceDBVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/MilvusVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/RedisVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/FAISSVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/vectorstore/providers/SKLearnVectorStoreConfig.py
[AutoAPI] Mapping Data... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/**init**.py
[AutoAPI] Mapping Data... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/mixins.py
[AutoAPI] Mapping Data... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/types.py
[AutoAPI] Mapping Data... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/retriever.py
[AutoAPI] Mapping Data... [ 16%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/EnsembleRetrieverConfig.py
[AutoAPI] Mapping Data... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/BedrockRetrieverConfig.py
[AutoAPI] Mapping Data... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/TFIDFRetrieverConfig.py
[AutoAPI] Mapping Data... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/YouRetrieverConfig.py
[AutoAPI] Mapping Data... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/GoogleDocumentAIWarehouseRetrieverConfig.py
[AutoAPI] Mapping Data... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/MultiVectorRetrieverConfig.py
[AutoAPI] Mapping Data... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/ZepCloudRetrieverConfig.py
[AutoAPI] Mapping Data... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/AzureAISearchRetrieverConfig.py
[AutoAPI] Mapping Data... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/ContextualCompressionRetrieverConfig.py
[AutoAPI] Mapping Data... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/MilvusRetrieverConfig.py
[AutoAPI] Mapping Data... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/GoogleVertexAISearchRetrieverConfig.py
[AutoAPI] Mapping Data... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/PineconeHybridSearchRetrieverConfig.py
[AutoAPI] Mapping Data... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/KNNRetrieverConfig.py
[AutoAPI] Mapping Data... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/ChatGPTPluginRetrieverConfig.py
[AutoAPI] Mapping Data... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/TimeWeightedVectorStoreRetrieverConfig.py
[AutoAPI] Mapping Data... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/SVMRetrieverConfig.py
[AutoAPI] Mapping Data... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/SelfQueryRetrieverConfig.py
[AutoAPI] Mapping Data... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/WeaviateHybridSearchRetrieverConfig.py
[AutoAPI] Mapping Data... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/ElasticsearchRetrieverConfig.py
[AutoAPI] Mapping Data... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/**init**.py
[AutoAPI] Mapping Data... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/MergerRetrieverConfig.py
[AutoAPI] Mapping Data... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/WikipediaRetrieverConfig.py
[AutoAPI] Mapping Data... [ 17%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/TavilySearchAPIRetrieverConfig.py
[AutoAPI] Mapping Data... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/AmazonKnowledgeBasesRetrieverConfig.py
[AutoAPI] Mapping Data... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/AskNewsRetrieverConfig.py
[AutoAPI] Mapping Data... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/ZepRetrieverConfig.py
[AutoAPI] Mapping Data... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/MultiQueryRetrieverConfig.py
[AutoAPI] Mapping Data... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/ParentDocumentRetrieverConfig.py
[AutoAPI] Mapping Data... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/VespaRetrieverConfig.py
[AutoAPI] Mapping Data... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/LlamaIndexRetrieverConfig.py
[AutoAPI] Mapping Data... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/ArceeRetrieverConfig.py
[AutoAPI] Mapping Data... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/NeuralDBRetrieverConfig.py
[AutoAPI] Mapping Data... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/CohereRagRetrieverConfig.py
[AutoAPI] Mapping Data... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/DocArrayRetrieverConfig.py
[AutoAPI] Mapping Data... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/QdrantSparseVectorRetrieverConfig.py
[AutoAPI] Mapping Data... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/LlamaIndexGraphRetrieverConfig.py
[AutoAPI] Mapping Data... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/BM25RetrieverConfig.py
[AutoAPI] Mapping Data... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/RePhraseQueryRetrieverConfig.py
[AutoAPI] Mapping Data... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/MetalRetrieverConfig.py
[AutoAPI] Mapping Data... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/KendraRetrieverConfig.py
[AutoAPI] Mapping Data... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/PubMedRetrieverConfig.py
[AutoAPI] Mapping Data... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/ArxivRetrieverConfig.py
[AutoAPI] Mapping Data... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/WebResearchRetrieverConfig.py
[AutoAPI] Mapping Data... [ 18%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/retriever/providers/RemoteLangChainRetrieverConfig.py
[AutoAPI] Mapping Data... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/pattern.py
[AutoAPI] Mapping Data... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/config.py
[AutoAPI] Mapping Data... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/protocols.py
[AutoAPI] Mapping Data... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/registry.py
[AutoAPI] Mapping Data... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/**init**.py
[AutoAPI] Mapping Data... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py
[AutoAPI] Mapping Data... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/integration.py
[AutoAPI] Mapping Data... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/base.py
[AutoAPI] Mapping Data... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/factory.py
[AutoAPI] Mapping Data... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/**init**.py
[AutoAPI] Mapping Data... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/handlers.py
[AutoAPI] Mapping Data... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/memory_config.py
[AutoAPI] Mapping Data... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/types.py
[AutoAPI] Mapping Data... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/postgres_config.py
[AutoAPI] Mapping Data... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/manager.py
[AutoAPI] Mapping Data... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/persistence/mongodb_config.py
[AutoAPI] Mapping Data... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/utils/**init**.py
[AutoAPI] Mapping Data... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/utils/state_handling.py
[AutoAPI] Mapping Data... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/utils/input_handling.py
[AutoAPI] Mapping Data... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/base.py
[AutoAPI] Mapping Data... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/config.py
[AutoAPI] Mapping Data... [ 19%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/**init**.py
[AutoAPI] Mapping Data... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/types.py
[AutoAPI] Mapping Data... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/OllamaEmbeddingConfig.py
[AutoAPI] Mapping Data... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/AzureOpenAIEmbeddingConfig.py
[AutoAPI] Mapping Data... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/**init**.py
[AutoAPI] Mapping Data... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/FakeEmbeddingConfig.py
[AutoAPI] Mapping Data... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/OpenAIEmbeddingConfig.py
[AutoAPI] Mapping Data... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/GoogleVertexAIEmbeddingConfig.py
[AutoAPI] Mapping Data... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/CohereEmbeddingConfig.py
[AutoAPI] Mapping Data... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/HuggingFaceEmbeddingConfig.py
[AutoAPI] Mapping Data... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/prompt_template/**init**.py
[AutoAPI] Mapping Data... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/prompt_template/prompt_engine.py
[AutoAPI] Mapping Data... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/output_parser/base.py
[AutoAPI] Mapping Data... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/output_parser/**init**.py
[AutoAPI] Mapping Data... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/output_parser/types.py
[AutoAPI] Mapping Data... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/tool/base.py
[AutoAPI] Mapping Data... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/tool/**init**.py
[AutoAPI] Mapping Data... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/config/auth_runnable.py
[AutoAPI] Mapping Data... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/config/protocols.py
[AutoAPI] Mapping Data... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/config/**init**.py
[AutoAPI] Mapping Data... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/config/constants.py
[AutoAPI] Mapping Data... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/config/runnable.py
[AutoAPI] Mapping Data... [ 20%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/agent_schema_composer.py
[AutoAPI] Mapping Data... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/state_schema.py
[AutoAPI] Mapping Data... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/schema_composer.py
[AutoAPI] Mapping Data... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/ui.py
[AutoAPI] Mapping Data... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/meta_agent_state.py
[AutoAPI] Mapping Data... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/schema_manager.py
[AutoAPI] Mapping Data... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/**init**.py
[AutoAPI] Mapping Data... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/utils.py
[AutoAPI] Mapping Data... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/multi_agent_state_schema.py
[AutoAPI] Mapping Data... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/field_registry.py
[AutoAPI] Mapping Data... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/preserve_messages_reducer.py
[AutoAPI] Mapping Data... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/engine_io_mixin.py
[AutoAPI] Mapping Data... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/base_state_schemas.py
[AutoAPI] Mapping Data... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/field_utils.py
[AutoAPI] Mapping Data... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/typed_state_schema.py
[AutoAPI] Mapping Data... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/field_extractor.py
[AutoAPI] Mapping Data... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/field_definition.py
[AutoAPI] Mapping Data... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/composer/schema_composer.py
[AutoAPI] Mapping Data... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/composer/**init**.py
[AutoAPI] Mapping Data... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/composer/\_base.py
[AutoAPI] Mapping Data... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/composer/engine/engine_detector.py
[AutoAPI] Mapping Data... [ 21%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/composer/engine/**init**.py
[AutoAPI] Mapping Data... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/composer/engine/engine_manager.py
[AutoAPI] Mapping Data... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/composer/field/**init**.py
[AutoAPI] Mapping Data... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/composer/field/field_manager.py
[AutoAPI] Mapping Data... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/flexible_multi_agent_state.py
[AutoAPI] Mapping Data... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/query_state.py
[AutoAPI] Mapping Data... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/tool_state_with_validation.py
[AutoAPI] Mapping Data... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/**init**.py
[AutoAPI] Mapping Data... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/messages_state.py
[AutoAPI] Mapping Data... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/structured_output_state.py
[AutoAPI] Mapping Data... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/validation_aware_tool_state.py
[AutoAPI] Mapping Data... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/multi_agent_state.py
[AutoAPI] Mapping Data... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/dynamic_activation_state.py
[AutoAPI] Mapping Data... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/document_state.py
[AutoAPI] Mapping Data... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/llm_state.py
[AutoAPI] Mapping Data... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/meta_state.py
[AutoAPI] Mapping Data... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/tool_state.py
[AutoAPI] Mapping Data... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/tools/**init**.py
[AutoAPI] Mapping Data... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/tools/validation_state.py
[AutoAPI] Mapping Data... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_with_token_usage.py
[AutoAPI] Mapping Data... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/messages/compatibility.py
[AutoAPI] Mapping Data... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/messages/**init**.py
[AutoAPI] Mapping Data... [ 22%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py
[AutoAPI] Mapping Data... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/messages/utils.py
[AutoAPI] Mapping Data... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/messages/token_usage.py
[AutoAPI] Mapping Data... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/messages/token_usage_mixin.py
[AutoAPI] Mapping Data... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/mixins/**init**.py
[AutoAPI] Mapping Data... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/state/**init**.py
[AutoAPI] Mapping Data... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/validators.py
[AutoAPI] Mapping Data... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/compatibility.py
[AutoAPI] Mapping Data... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/langchain_converters.py
[AutoAPI] Mapping Data... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/protocols.py
[AutoAPI] Mapping Data... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/analyzer.py
[AutoAPI] Mapping Data... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/field_mapping.py
[AutoAPI] Mapping Data... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/**init**.py
[AutoAPI] Mapping Data... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/converters.py
[AutoAPI] Mapping Data... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/utils.py
[AutoAPI] Mapping Data... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/reports.py
[AutoAPI] Mapping Data... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/types.py
[AutoAPI] Mapping Data... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/compatibility/mergers.py
[AutoAPI] Mapping Data... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/tool_manager.py
[AutoAPI] Mapping Data... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/tool_config.py
[AutoAPI] Mapping Data... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph_manager.py
[AutoAPI] Mapping Data... [ 23%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/graph_pattern_registry.py
[AutoAPI] Mapping Data... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/tool_injector.py
[AutoAPI] Mapping Data... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/StateSchema.py
[AutoAPI] Mapping Data... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/ToolManager.py
[AutoAPI] Mapping Data... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/graph_builder2.py
[AutoAPI] Mapping Data... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/NodeFactory.py
[AutoAPI] Mapping Data... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/**init**.py
[AutoAPI] Mapping Data... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/dynamic_graph_builder.py
[AutoAPI] Mapping Data... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph.py
[AutoAPI] Mapping Data... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/StateGraphEditor.py
[AutoAPI] Mapping Data... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/routing.py
[AutoAPI] Mapping Data... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/agent_node_v2.py
[AutoAPI] Mapping Data... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/config.py
[AutoAPI] Mapping Data... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/message_transformation.py
[AutoAPI] Mapping Data... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/factory.py
[AutoAPI] Mapping Data... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/intelligent_multi_agent_node.py
[AutoAPI] Mapping Data... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/routing_validation_node.py
[AutoAPI] Mapping Data... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/unified_validation_node.py
[AutoAPI] Mapping Data... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/state_updating_validation_node.py
[AutoAPI] Mapping Data... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/agent_node.py
[AutoAPI] Mapping Data... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/protocols.py
[AutoAPI] Mapping Data... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/validation_node_v2.py
[AutoAPI] Mapping Data... [ 24%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/meta_agent_node.py
[AutoAPI] Mapping Data... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/registry.py
[AutoAPI] Mapping Data... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/**init**.py
[AutoAPI] Mapping Data... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/output_parsing_v2.py
[AutoAPI] Mapping Data... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/tool_node_config_v2.py
[AutoAPI] Mapping Data... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/decorators.py
[AutoAPI] Mapping Data... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/stateful_node_config.py
[AutoAPI] Mapping Data... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/engine_node.py
[AutoAPI] Mapping Data... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/agent_node_v3.py
[AutoAPI] Mapping Data... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/callable_node.py
[AutoAPI] Mapping Data... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/handlers.py
[AutoAPI] Mapping Data... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/output_parsing.py
[AutoAPI] Mapping Data... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/utils.py
[AutoAPI] Mapping Data... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/types.py
[AutoAPI] Mapping Data... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/validation_node_with_routing.py
[AutoAPI] Mapping Data... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/tool_node_config.py
[AutoAPI] Mapping Data... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/stateful_validation_node.py
[AutoAPI] Mapping Data... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/validation_node_config.py
[AutoAPI] Mapping Data... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/base_config.py
[AutoAPI] Mapping Data... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/engine_node_generic.py
[AutoAPI] Mapping Data... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/parser_node_config_v2.py
[AutoAPI] Mapping Data... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/base_node_config.py
[AutoAPI] Mapping Data... [ 25%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/parser_node_config.py
[AutoAPI] Mapping Data... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/test.py
[AutoAPI] Mapping Data... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/processors.py
[AutoAPI] Mapping Data... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/placeholder_node.py
[AutoAPI] Mapping Data... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py
[AutoAPI] Mapping Data... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/validation_node_config_v2.py
[AutoAPI] Mapping Data... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/validation_router_v2.py
[AutoAPI] Mapping Data... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/multi_agent_node.py
[AutoAPI] Mapping Data... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/composer/protocols.py
[AutoAPI] Mapping Data... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/composer/node_schema_composer.py
[AutoAPI] Mapping Data... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/composer/field_mapping.py
[AutoAPI] Mapping Data... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/composer/**init**.py
[AutoAPI] Mapping Data... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/composer/extract_functions.py
[AutoAPI] Mapping Data... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/composer/update_functions.py
[AutoAPI] Mapping Data... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/composer/advanced_node_composer.py
[AutoAPI] Mapping Data... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/composer/integrated_node_composer.py
[AutoAPI] Mapping Data... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/composer/path_resolver.py
[AutoAPI] Mapping Data... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/common/**init**.py
[AutoAPI] Mapping Data... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/common/types.py
[AutoAPI] Mapping Data... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/common/field_utils.py
[AutoAPI] Mapping Data... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/common/serialization.py
[AutoAPI] Mapping Data... [ 26%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/common/references.py
[AutoAPI] Mapping Data... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/base.py
[AutoAPI] Mapping Data... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/mixin.py
[AutoAPI] Mapping Data... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/serializable.py
[AutoAPI] Mapping Data... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/recompilation_demo.py
[AutoAPI] Mapping Data... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/pattern_registry.py
[AutoAPI] Mapping Data... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/state_graph_builder.py
[AutoAPI] Mapping Data... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/registry.py
[AutoAPI] Mapping Data... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/**init**.py
[AutoAPI] Mapping Data... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/validation_mixin.py
[AutoAPI] Mapping Data... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/types.py
[AutoAPI] Mapping Data... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/graph_path.py
[AutoAPI] Mapping Data... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/pattern_definition.py
[AutoAPI] Mapping Data... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/schema_graph.py
[AutoAPI] Mapping Data... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/state_graph.py
[AutoAPI] Mapping Data... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py
[AutoAPI] Mapping Data... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/graph_visualizer.py
[AutoAPI] Mapping Data... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/schema_mixin.py
[AutoAPI] Mapping Data... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/pattern_decorator.py
[AutoAPI] Mapping Data... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/packages/haive-core/src/haive/core/graph/state_graph/conversion/**init**.py
[AutoAPI] Mapping Data... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/packages/haive-core/src/haive/core/graph/state_graph/utils/**init**.py
[AutoAPI] Mapping Data... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/packages/haive-core/src/haive/core/graph/state_graph/components/**init**.py
[AutoAPI] Mapping Data... [ 27%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/conversion/**init**.py
[AutoAPI] Mapping Data... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/conversion/langgraph.py
[AutoAPI] Mapping Data... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/models/edge_model.py
[AutoAPI] Mapping Data... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/models/function_ref.py
[AutoAPI] Mapping Data... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/models/node_model.py
[AutoAPI] Mapping Data... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/models/state_graph_model.py
[AutoAPI] Mapping Data... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/models/branch_model.py
[AutoAPI] Mapping Data... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/utils/**init**.py
[AutoAPI] Mapping Data... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/pattern/base.py
[AutoAPI] Mapping Data... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/pattern/**init**.py
[AutoAPI] Mapping Data... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/pattern/implementations.py
[AutoAPI] Mapping Data... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/node.py
[AutoAPI] Mapping Data... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/architecture_summary.py
[AutoAPI] Mapping Data... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/modular_base_graph.py
[AutoAPI] Mapping Data... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/branch.py
[AutoAPI] Mapping Data... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/**init**.py
[AutoAPI] Mapping Data... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/branch_manager.py
[AutoAPI] Mapping Data... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/node_manager.py
[AutoAPI] Mapping Data... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/base_component.py
[AutoAPI] Mapping Data... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/components/edge_manager.py
[AutoAPI] Mapping Data... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/gb/**init**.py
[AutoAPI] Mapping Data... [ 28%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/gb/types.py
[AutoAPI] Mapping Data... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/utils/**init**.py
[AutoAPI] Mapping Data... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/utils/mermaid_visualizer.py
[AutoAPI] Mapping Data... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/routers/base.py
[AutoAPI] Mapping Data... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/routers/**init**.py
[AutoAPI] Mapping Data... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/routers/conditions.py
[AutoAPI] Mapping Data... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/routers/test.py
[AutoAPI] Mapping Data... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/branches/branch.py
[AutoAPI] Mapping Data... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/branches/**init**.py
[AutoAPI] Mapping Data... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/branches/utils.py
[AutoAPI] Mapping Data... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/branches/dynamic.py
[AutoAPI] Mapping Data... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/branches/types.py
[AutoAPI] Mapping Data... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/branches/send_mapping.py
[AutoAPI] Mapping Data... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/retry/base.py
[AutoAPI] Mapping Data... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/retry/**init**.py
[AutoAPI] Mapping Data... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/patterns/integration.py
[AutoAPI] Mapping Data... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/patterns/base.py
[AutoAPI] Mapping Data... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/patterns/registry.py
[AutoAPI] Mapping Data... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/patterns/**init**.py
[AutoAPI] Mapping Data... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/state.py
[AutoAPI] Mapping Data... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base.py
[AutoAPI] Mapping Data... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/config.py
[AutoAPI] Mapping Data... [ 29%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/models.py
[AutoAPI] Mapping Data... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/factory.py
[AutoAPI] Mapping Data... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/tool_utils.py
[AutoAPI] Mapping Data... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/**init**.py
[AutoAPI] Mapping Data... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/state_wrapper.py
[AutoAPI] Mapping Data... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/qa_agent.py
[AutoAPI] Mapping Data... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/agent.py
[AutoAPI] Mapping Data... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/routing_agent.py
[AutoAPI] Mapping Data... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain_agent.py
[AutoAPI] Mapping Data... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/tools.py
[AutoAPI] Mapping Data... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/**init**.py
[AutoAPI] Mapping Data... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/perplexity/pro_search/models.py
[AutoAPI] Mapping Data... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/perplexity/pro_search/**init**.py
[AutoAPI] Mapping Data... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/perplexity/pro_search/tasks/models.py
[AutoAPI] Mapping Data... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/perplexity/pro_search/tasks/**init**.py
[AutoAPI] Mapping Data... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/perplexity/pro_search/tasks/prompts.py
[AutoAPI] Mapping Data... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/perplexity/pro_search/search/models.py
[AutoAPI] Mapping Data... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/perplexity/pro_search/search/**init**.py
[AutoAPI] Mapping Data... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/perplexity/pro_search/search/prompts.py
[AutoAPI] Mapping Data... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/state.py
[AutoAPI] Mapping Data... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/config.py
[AutoAPI] Mapping Data... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/**init**.py
[AutoAPI] Mapping Data... [ 30%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/related_topics_generator/models.py
[AutoAPI] Mapping Data... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/related_topics_generator/**init**.py
[AutoAPI] Mapping Data... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/related_topics_generator/agent.py
[AutoAPI] Mapping Data... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/related_topics_generator/prompt.py
[AutoAPI] Mapping Data... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/section_writer/models.py
[AutoAPI] Mapping Data... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/section_writer/**init**.py
[AutoAPI] Mapping Data... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/section_writer/agent.py
[AutoAPI] Mapping Data... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/section_writer/prompt.py
[AutoAPI] Mapping Data... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/outline_generator/models.py
[AutoAPI] Mapping Data... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/outline_generator/**init**.py
[AutoAPI] Mapping Data... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/outline_generator/agent.py
[AutoAPI] Mapping Data... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/outline_generator/prompt.py
[AutoAPI] Mapping Data... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/outline_refiner/**init**.py
[AutoAPI] Mapping Data... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/outline_refiner/agent.py
[AutoAPI] Mapping Data... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/outline_refiner/prompt.py
[AutoAPI] Mapping Data... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/wiki_writer/**init**.py
[AutoAPI] Mapping Data... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/wiki_writer/agent.py
[AutoAPI] Mapping Data... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/wiki_writer/prompt.py
[AutoAPI] Mapping Data... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/generate_perspectives/models.py
[AutoAPI] Mapping Data... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/generate_perspectives/**init**.py
[AutoAPI] Mapping Data... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/generate_perspectives/agent.py
[AutoAPI] Mapping Data... [ 31%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/storm/generate_perspectives/prompt.py
[AutoAPI] Mapping Data... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/person/state.py
[AutoAPI] Mapping Data... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/person/config.py
[AutoAPI] Mapping Data... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/person/models.py
[AutoAPI] Mapping Data... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/person/**init**.py
[AutoAPI] Mapping Data... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/person/utils.py
[AutoAPI] Mapping Data... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/person/agent.py
[AutoAPI] Mapping Data... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/person/prompts.py
[AutoAPI] Mapping Data... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/state.py
[AutoAPI] Mapping Data... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/structured_tools.py
[AutoAPI] Mapping Data... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/engines.py
[AutoAPI] Mapping Data... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/config.py
[AutoAPI] Mapping Data... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/models.py
[AutoAPI] Mapping Data... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/react_agent_config.py
[AutoAPI] Mapping Data... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/**init**.py
[AutoAPI] Mapping Data... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/agent.py
[AutoAPI] Mapping Data... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/open_perplexity/prompts.py
[AutoAPI] Mapping Data... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/**init**.py
[AutoAPI] Mapping Data... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/mixins.py
[AutoAPI] Mapping Data... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/task_analysis/base.py
[AutoAPI] Mapping Data... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/task_analysis/solvability.py
[AutoAPI] Mapping Data... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/task_analysis/parallelization.py
[AutoAPI] Mapping Data... [ 32%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/task_analysis/**init**.py
[AutoAPI] Mapping Data... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/task_analysis/branching.py
[AutoAPI] Mapping Data... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/task_analysis/analysis.py
[AutoAPI] Mapping Data... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/composite.py
[AutoAPI] Mapping Data... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/base.py
[AutoAPI] Mapping Data... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/rubric.py
[AutoAPI] Mapping Data... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/numeric.py
[AutoAPI] Mapping Data... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/**init**.py
[AutoAPI] Mapping Data... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/scale.py
[AutoAPI] Mapping Data... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/qualitative.py
[AutoAPI] Mapping Data... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/letter_grade.py
[AutoAPI] Mapping Data... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/models/grade/binary.py
[AutoAPI] Mapping Data... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/common/utils/pydantic_prompt_utils.py
[AutoAPI] Mapping Data... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/state.py
[AutoAPI] Mapping Data... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/models.py
[AutoAPI] Mapping Data... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/multi_agent_reflection.py
[AutoAPI] Mapping Data... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/simple_agent.py
[AutoAPI] Mapping Data... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/**init**.py
[AutoAPI] Mapping Data... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/message_transformer_posthook.py
[AutoAPI] Mapping Data... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/agent.py
[AutoAPI] Mapping Data... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/structured_output.py
[AutoAPI] Mapping Data... [ 33%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/message_transformer.py
[AutoAPI] Mapping Data... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/prompts.py
[AutoAPI] Mapping Data... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/universal_agent.py
[AutoAPI] Mapping Data... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/hooks.py
[AutoAPI] Mapping Data... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/enhanced_init.py
[AutoAPI] Mapping Data... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/**init**.py
[AutoAPI] Mapping Data... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/typed_agent.py
[AutoAPI] Mapping Data... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/compiled_agent.py
[AutoAPI] Mapping Data... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent_with_token_tracking.py
[AutoAPI] Mapping Data... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py
[AutoAPI] Mapping Data... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/types.py
[AutoAPI] Mapping Data... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent_structured_output_mixin.py
[AutoAPI] Mapping Data... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/enhanced_agent.py
[AutoAPI] Mapping Data... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/pre_post_agent_mixin.py
[AutoAPI] Mapping Data... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/serialization_mixin.py
[AutoAPI] Mapping Data... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/agent_protocol.py
[AutoAPI] Mapping Data... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/**init**.py
[AutoAPI] Mapping Data... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/hooks_mixin.py
[AutoAPI] Mapping Data... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/persistence_mixin.py
[AutoAPI] Mapping Data... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/state_mixin.py
[AutoAPI] Mapping Data... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/execution_mixin.py
[AutoAPI] Mapping Data... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/structured_output/models.py
[AutoAPI] Mapping Data... [ 34%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/structured_output/**init**.py
[AutoAPI] Mapping Data... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/structured_output/agent.py
[AutoAPI] Mapping Data... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document/agent.py
[AutoAPI] Mapping Data... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/dynamic_tool_selector.py
[AutoAPI] Mapping Data... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/semantic_discovery.py
[AutoAPI] Mapping Data... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/**init**.py
[AutoAPI] Mapping Data... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/selection_strategies.py
[AutoAPI] Mapping Data... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/discovery/component_discovery_agent.py
[AutoAPI] Mapping Data... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/**init**.py
[AutoAPI] Mapping Data... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/agent.py
[AutoAPI] Mapping Data... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/prompts.py
[AutoAPI] Mapping Data... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/complexity/engines.py
[AutoAPI] Mapping Data... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/complexity/models.py
[AutoAPI] Mapping Data... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/complexity/prompts.py
[AutoAPI] Mapping Data... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/base/models.py
[AutoAPI] Mapping Data... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/base/**init**.py
[AutoAPI] Mapping Data... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/decomposer/engines.py
[AutoAPI] Mapping Data... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/decomposer/models.py
[AutoAPI] Mapping Data... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/decomposer/**init**.py
[AutoAPI] Mapping Data... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/decomposer/prompts.py
[AutoAPI] Mapping Data... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/decomposer/prompt.py
[AutoAPI] Mapping Data... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/tree/engines.py
[AutoAPI] Mapping Data... [ 35%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/tree/models.py
[AutoAPI] Mapping Data... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/tree/**init**.py
[AutoAPI] Mapping Data... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/tree/prompts.py
[AutoAPI] Mapping Data... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/analysis/engines.py
[AutoAPI] Mapping Data... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/analysis/models.py
[AutoAPI] Mapping Data... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/analysis/**init**.py
[AutoAPI] Mapping Data... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/analysis/prompts.py
[AutoAPI] Mapping Data... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/execution/engines.py
[AutoAPI] Mapping Data... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/execution/models.py
[AutoAPI] Mapping Data... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/execution/**init**.py
[AutoAPI] Mapping Data... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/execution/prompts.py
[AutoAPI] Mapping Data... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/context/engines.py
[AutoAPI] Mapping Data... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/context/models.py
[AutoAPI] Mapping Data... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/context/**init**.py
[AutoAPI] Mapping Data... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/context/prompts.py
[AutoAPI] Mapping Data... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic_tool_discovery_supervisor.py
[AutoAPI] Mapping Data... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic_multi_agent.py
[AutoAPI] Mapping Data... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/compatibility_bridge.py
[AutoAPI] Mapping Data... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic_state.py
[AutoAPI] Mapping Data... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic_supervisor_fixed.py
[AutoAPI] Mapping Data... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/internal_dynamic_supervisor.py
[AutoAPI] Mapping Data... [ 36%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/choice_model_supervisor.py
[AutoAPI] Mapping Data... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic_activation_supervisor.py
[AutoAPI] Mapping Data... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/integrated_supervisor.py
[AutoAPI] Mapping Data... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/simple_supervisor.py
[AutoAPI] Mapping Data... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic_agent_tools.py
[AutoAPI] Mapping Data... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/registry.py
[AutoAPI] Mapping Data... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic_executor_node.py
[AutoAPI] Mapping Data... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/**init**.py
[AutoAPI] Mapping Data... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/proper_dynamic_supervisor.py
[AutoAPI] Mapping Data... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/clean_dynamic_supervisor.py
[AutoAPI] Mapping Data... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic_supervisor.py
[AutoAPI] Mapping Data... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/agent.py
[AutoAPI] Mapping Data... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/simple_test_runner.py
[AutoAPI] Mapping Data... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/multi_agent_dynamic_state.py
[AutoAPI] Mapping Data... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic_agent_discovery_supervisor.py
[AutoAPI] Mapping Data... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/registry_supervisor.py
[AutoAPI] Mapping Data... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/routing.py
[AutoAPI] Mapping Data... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/agent_v2.py
[AutoAPI] Mapping Data... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/rebuild_dynamic_supervisor.py
[AutoAPI] Mapping Data... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/multi_integration.py
[AutoAPI] Mapping Data... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/chain_agent_simple.py
[AutoAPI] Mapping Data... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/**init**.py
[AutoAPI] Mapping Data... [ 37%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/chain_examples.py
[AutoAPI] Mapping Data... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/extended_examples.py
[AutoAPI] Mapping Data... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/sequential/config.py
[AutoAPI] Mapping Data... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/sequential/**init**.py
[AutoAPI] Mapping Data... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/sequential/agent.py
[AutoAPI] Mapping Data... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/proper_plan_execute.py
[AutoAPI] Mapping Data... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/langgraph_plan_execute.py
[AutoAPI] Mapping Data... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/**init**.py
[AutoAPI] Mapping Data... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo_tree_agent.py
[AutoAPI] Mapping Data... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo_tree_agent_v2.py
[AutoAPI] Mapping Data... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo_tree_agent_v3.py
[AutoAPI] Mapping Data... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/clean_plan_execute.py
[AutoAPI] Mapping Data... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute_multi.py
[AutoAPI] Mapping Data... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/state.py
[AutoAPI] Mapping Data... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/engines.py
[AutoAPI] Mapping Data... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/simple.py
[AutoAPI] Mapping Data... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/config.py
[AutoAPI] Mapping Data... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/models.py
[AutoAPI] Mapping Data... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/**init**.py
[AutoAPI] Mapping Data... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/agent.py
[AutoAPI] Mapping Data... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/v2/state.py
[AutoAPI] Mapping Data... [ 38%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/v2/models.py
[AutoAPI] Mapping Data... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/v2/**init**.py
[AutoAPI] Mapping Data... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/v2/agent.py
[AutoAPI] Mapping Data... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/v2/prompts.py
[AutoAPI] Mapping Data... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_execute_v3/state.py
[AutoAPI] Mapping Data... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_execute_v3/engines.py
[AutoAPI] Mapping Data... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_execute_v3/config.py
[AutoAPI] Mapping Data... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_execute_v3/models.py
[AutoAPI] Mapping Data... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_execute_v3/**init**.py
[AutoAPI] Mapping Data... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_execute_v3/agent.py
[AutoAPI] Mapping Data... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_execute_v3/prompts.py
[AutoAPI] Mapping Data... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo/**init**.py
[AutoAPI] Mapping Data... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo/agents/**init**.py
[AutoAPI] Mapping Data... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo/models/join_step.py
[AutoAPI] Mapping Data... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo/models/**init**.py
[AutoAPI] Mapping Data... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo/models/tool_step.py
[AutoAPI] Mapping Data... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo/models/steps.py
[AutoAPI] Mapping Data... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo/models/plans.py
[AutoAPI] Mapping Data... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/models/base.py
[AutoAPI] Mapping Data... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/models/**init**.py
[AutoAPI] Mapping Data... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler_v3/state.py
[AutoAPI] Mapping Data... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler_v3/config.py
[AutoAPI] Mapping Data... [ 39%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler_v3/models.py
[AutoAPI] Mapping Data... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler_v3/**init**.py
[AutoAPI] Mapping Data... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler_v3/agent.py
[AutoAPI] Mapping Data... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler_v3/prompts.py
[AutoAPI] Mapping Data... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/p_and_e/state.py
[AutoAPI] Mapping Data... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/p_and_e/engines.py
[AutoAPI] Mapping Data... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/p_and_e/models.py
[AutoAPI] Mapping Data... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/p_and_e/**init**.py
[AutoAPI] Mapping Data... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/p_and_e/agent.py
[AutoAPI] Mapping Data... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/p_and_e/multi_agent.py
[AutoAPI] Mapping Data... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/p_and_e/enhanced_multi_agent.py
[AutoAPI] Mapping Data... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/p_and_e/prompts.py
[AutoAPI] Mapping Data... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo_v3/state.py
[AutoAPI] Mapping Data... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo_v3/models.py
[AutoAPI] Mapping Data... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo_v3/**init**.py
[AutoAPI] Mapping Data... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo_v3/agent.py
[AutoAPI] Mapping Data... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo_v3/prompts.py
[AutoAPI] Mapping Data... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler/state.py
[AutoAPI] Mapping Data... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler/config.py
[AutoAPI] Mapping Data... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler/models.py
[AutoAPI] Mapping Data... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler/**init**.py
[AutoAPI] Mapping Data... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler/utils.py
[AutoAPI] Mapping Data... [ 40%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler/agent.py
[AutoAPI] Mapping Data... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler/output_parser.py
[AutoAPI] Mapping Data... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler/tools/math_tools.py
[AutoAPI] Mapping Data... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/state.py
[AutoAPI] Mapping Data... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/enhanced_agent_v3.py
[AutoAPI] Mapping Data... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/enhanced_simple_minimal.py
[AutoAPI] Mapping Data... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/config.py
[AutoAPI] Mapping Data... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/factory.py
[AutoAPI] Mapping Data... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/enhanced_simple_real.py
[AutoAPI] Mapping Data... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/ultra_lazy_agent.py
[AutoAPI] Mapping Data... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/lazy_simple_agent.py
[AutoAPI] Mapping Data... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/**init**.py
[AutoAPI] Mapping Data... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/agent_v3_minimal.py
[AutoAPI] Mapping Data... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/agent.py
[AutoAPI] Mapping Data... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/agent_with_validation.py
[AutoAPI] Mapping Data... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/clean_enhanced_simple.py
[AutoAPI] Mapping Data... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/enhanced_simple_agent_v2.py
[AutoAPI] Mapping Data... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/enhanced_simple_agent.py
[AutoAPI] Mapping Data... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/agent_v2.py
[AutoAPI] Mapping Data... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/agent_v3.py
[AutoAPI] Mapping Data... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/structured/config.py
[AutoAPI] Mapping Data... [ 41%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/structured/**init**.py
[AutoAPI] Mapping Data... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/structured/agent.py
[AutoAPI] Mapping Data... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/v2/config.py
[AutoAPI] Mapping Data... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/v2/graph.py
[AutoAPI] Mapping Data... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/v2/**init**.py
[AutoAPI] Mapping Data... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/ltm/memory_schemas.py
[AutoAPI] Mapping Data... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/ltm/agent.py
[AutoAPI] Mapping Data... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/models.py
[AutoAPI] Mapping Data... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/branched_chain.py
[AutoAPI] Mapping Data... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/enhanced_memory_react.py
[AutoAPI] Mapping Data... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/unified_factory.py
[AutoAPI] Mapping Data... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/**init**.py
[AutoAPI] Mapping Data... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/answer_agent.py
[AutoAPI] Mapping Data... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/synthesis_agent.py
[AutoAPI] Mapping Data... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/collective_rag_agent_v4.py
[AutoAPI] Mapping Data... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple_rag_agent_v4.py
[AutoAPI] Mapping Data... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/chain_collection.py
[AutoAPI] Mapping Data... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/modular_chain.py
[AutoAPI] Mapping Data... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/agentic_router/**init**.py
[AutoAPI] Mapping Data... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/agentic_router/agent.py
[AutoAPI] Mapping Data... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/agentic_router/agent_chain.py
[AutoAPI] Mapping Data... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/agentic_router/agent_v2.py
[AutoAPI] Mapping Data... [ 42%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/document_graders/comprehensive_grader.py
[AutoAPI] Mapping Data... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/document_graders/models.py
[AutoAPI] Mapping Data... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/document_graders/**init**.py
[AutoAPI] Mapping Data... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/document_graders/binary_grader/**init**.py
[AutoAPI] Mapping Data... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/document_graders/binary_grader/prompt.py
[AutoAPI] Mapping Data... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/document_graders/comprehensive_grader/models.py
[AutoAPI] Mapping Data... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/document_graders/comprehensive_grader/prompt.py
[AutoAPI] Mapping Data... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/hallucination_graders/models.py
[AutoAPI] Mapping Data... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/hallucination_graders/**init**.py
[AutoAPI] Mapping Data... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/hallucination_graders/prompts.py
[AutoAPI] Mapping Data... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/query_refinement/models.py
[AutoAPI] Mapping Data... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/query_refinement/**init**.py
[AutoAPI] Mapping Data... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/query_refinement/prompt.py
[AutoAPI] Mapping Data... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/answer_generators/**init**.py
[AutoAPI] Mapping Data... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/answer_generators/prompts.py
[AutoAPI] Mapping Data... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/query_constructors/flare/models.py
[AutoAPI] Mapping Data... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/query_constructors/flare/**init**.py
[AutoAPI] Mapping Data... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/query_constructors/flare/prompt.py
[AutoAPI] Mapping Data... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/query_constructors/hyde/models.py
[AutoAPI] Mapping Data... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/query_constructors/hyde/**init**.py
[AutoAPI] Mapping Data... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/query_constructors/hyde/enhanced_prompts.py
[AutoAPI] Mapping Data... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/common/query_constructors/hyde/prompt.py
[AutoAPI] Mapping Data... [ 43%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/fusion/**init**.py
[AutoAPI] Mapping Data... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/fusion/agent.py
[AutoAPI] Mapping Data... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_strategy/state.py
[AutoAPI] Mapping Data... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_strategy/config.py
[AutoAPI] Mapping Data... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_strategy/**init**.py
[AutoAPI] Mapping Data... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_strategy/query_types.py
[AutoAPI] Mapping Data... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_strategy/agent.py
[AutoAPI] Mapping Data... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/base/state.py
[AutoAPI] Mapping Data... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/base/base_agent.py
[AutoAPI] Mapping Data... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/base/config.py
[AutoAPI] Mapping Data... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/base/models.py
[AutoAPI] Mapping Data... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/base/**init**.py
[AutoAPI] Mapping Data... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/base/utils.py
[AutoAPI] Mapping Data... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/base/agent.py
[AutoAPI] Mapping Data... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/base/branches.py
[AutoAPI] Mapping Data... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/base/prompts.py
[AutoAPI] Mapping Data... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_reflective/**init**.py
[AutoAPI] Mapping Data... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_reflective/agent.py
[AutoAPI] Mapping Data... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/state.py
[AutoAPI] Mapping Data... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/nodes.py
[AutoAPI] Mapping Data... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/graph.py
[AutoAPI] Mapping Data... [ 44%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/configuration.py
[AutoAPI] Mapping Data... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/**init**.py
[AutoAPI] Mapping Data... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/prompts.py
[AutoAPI] Mapping Data... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/nodes/grade_documents.py
[AutoAPI] Mapping Data... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/nodes/generate.py
[AutoAPI] Mapping Data... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/nodes/grade_generation_v_documents_and_question.py
[AutoAPI] Mapping Data... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/nodes/decide_to_generate.py
[AutoAPI] Mapping Data... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/nodes/retreive.py
[AutoAPI] Mapping Data... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_rag2/nodes/transform_query.py
[AutoAPI] Mapping Data... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/flare/**init**.py
[AutoAPI] Mapping Data... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/flare/agent.py
[AutoAPI] Mapping Data... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/document_grading/**init**.py
[AutoAPI] Mapping Data... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/document_grading/agent.py
[AutoAPI] Mapping Data... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/factories/compatible_rag_factory_simple.py
[AutoAPI] Mapping Data... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/factories/rag_workflow_factory.py
[AutoAPI] Mapping Data... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/factories/compatible_rag_factory.py
[AutoAPI] Mapping Data... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/adaptive_rag/**init**.py
[AutoAPI] Mapping Data... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/adaptive_rag/agent.py
[AutoAPI] Mapping Data... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/adaptive/agent.py
[AutoAPI] Mapping Data... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/step_back/**init**.py
[AutoAPI] Mapping Data... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/step_back/agent.py
[AutoAPI] Mapping Data... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/memory_aware/**init**.py
[AutoAPI] Mapping Data... [ 45%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/memory_aware/agent.py
[AutoAPI] Mapping Data... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/hyde/models.py
[AutoAPI] Mapping Data... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/hyde/enhanced_agent_v2.py
[AutoAPI] Mapping Data... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/hyde/**init**.py
[AutoAPI] Mapping Data... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/hyde/agent.py
[AutoAPI] Mapping Data... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/hyde/enhanced_agent.py
[AutoAPI] Mapping Data... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/hyde/prompts.py
[AutoAPI] Mapping Data... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/hyde/agent_v2.py
[AutoAPI] Mapping Data... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/simple_rag.py
[AutoAPI] Mapping Data... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/clean_simple_rag.py
[AutoAPI] Mapping Data... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/sequential_agent.py
[AutoAPI] Mapping Data... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/**init**.py
[AutoAPI] Mapping Data... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/answer_agent.py
[AutoAPI] Mapping Data... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/simple_rag_state.py
[AutoAPI] Mapping Data... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/agent.py
[AutoAPI] Mapping Data... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/multi_agent_simple_rag.py
[AutoAPI] Mapping Data... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/answer_generator/models.py
[AutoAPI] Mapping Data... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/answer_generator/**init**.py
[AutoAPI] Mapping Data... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/answer_generator/prompts.py
[AutoAPI] Mapping Data... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/enhanced_v3/state.py
[AutoAPI] Mapping Data... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/enhanced_v3/retriever_agent.py
[AutoAPI] Mapping Data... [ 46%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/enhanced_v3/**init**.py
[AutoAPI] Mapping Data... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/enhanced_v3/answer_generator_agent.py
[AutoAPI] Mapping Data... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/simple/enhanced_v3/agent.py
[AutoAPI] Mapping Data... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/state.py
[AutoAPI] Mapping Data... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/additional_workflows.py
[AutoAPI] Mapping Data... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/complete_rag_workflows.py
[AutoAPI] Mapping Data... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/enhanced_workflows.py
[AutoAPI] Mapping Data... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/compatibility.py
[AutoAPI] Mapping Data... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/specialized_workflows_v2.py
[AutoAPI] Mapping Data... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/**init**.py
[AutoAPI] Mapping Data... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/specialized_workflows.py
[AutoAPI] Mapping Data... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/enhanced_state_schemas.py
[AutoAPI] Mapping Data... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/advanced_workflows.py
[AutoAPI] Mapping Data... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/graded_rag_workflows_v2.py
[AutoAPI] Mapping Data... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/multi_rag.py
[AutoAPI] Mapping Data... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/simple_enhanced_workflows.py
[AutoAPI] Mapping Data... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/enhanced_multi_rag.py
[AutoAPI] Mapping Data... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/graded_rag_workflows.py
[AutoAPI] Mapping Data... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/agents.py
[AutoAPI] Mapping Data... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/grading_components.py
[AutoAPI] Mapping Data... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/dynamic/state.py
[AutoAPI] Mapping Data... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/dynamic/config.py
[AutoAPI] Mapping Data... [ 47%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/dynamic/models.py
[AutoAPI] Mapping Data... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/dynamic/data_source_types.py
[AutoAPI] Mapping Data... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/dynamic/agent.py
[AutoAPI] Mapping Data... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_route/**init**.py
[AutoAPI] Mapping Data... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_route/agent.py
[AutoAPI] Mapping Data... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/typed/state.py
[AutoAPI] Mapping Data... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/typed/config.py
[AutoAPI] Mapping Data... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/typed/query_types.py
[AutoAPI] Mapping Data... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/typed/agent.py
[AutoAPI] Mapping Data... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/utils/structured_output_enhancer.py
[AutoAPI] Mapping Data... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/adaptive_tools/**init**.py
[AutoAPI] Mapping Data... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/adaptive_tools/agent.py
[AutoAPI] Mapping Data... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/query_decomposition/**init**.py
[AutoAPI] Mapping Data... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/query_decomposition/agent.py
[AutoAPI] Mapping Data... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/**init**.py
[AutoAPI] Mapping Data... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/state.py
[AutoAPI] Mapping Data... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/engines.py
[AutoAPI] Mapping Data... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/config.py
[AutoAPI] Mapping Data... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/models.py
[AutoAPI] Mapping Data... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/**init**.py
[AutoAPI] Mapping Data... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/utils.py
[AutoAPI] Mapping Data... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/agent.py
[AutoAPI] Mapping Data... [ 48%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/prompts.py
[AutoAPI] Mapping Data... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/state.py
[AutoAPI] Mapping Data... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/engines.py
[AutoAPI] Mapping Data... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/config.py
[AutoAPI] Mapping Data... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/models.py
[AutoAPI] Mapping Data... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/**init**.py
[AutoAPI] Mapping Data... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/agent.py
[AutoAPI] Mapping Data... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/branches.py
[AutoAPI] Mapping Data... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/scratch.py
[AutoAPI] Mapping Data... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/base/db_config.py
[AutoAPI] Mapping Data... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/base/**init**.py
[AutoAPI] Mapping Data... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/filtered/state.py
[AutoAPI] Mapping Data... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/filtered/config.py
[AutoAPI] Mapping Data... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/filtered/**init**.py
[AutoAPI] Mapping Data... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/filtered/agent.py
[AutoAPI] Mapping Data... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/speculative/**init**.py
[AutoAPI] Mapping Data... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/speculative/agent.py
[AutoAPI] Mapping Data... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/hallucination_grading/**init**.py
[AutoAPI] Mapping Data... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/hallucination_grading/agent.py
[AutoAPI] Mapping Data... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/query_planning/**init**.py
[AutoAPI] Mapping Data... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/query_planning/agent.py
[AutoAPI] Mapping Data... [ 49%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/query_planning/agent_chain.py
[AutoAPI] Mapping Data... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/agentic/react_rag_agent.py
[AutoAPI] Mapping Data... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/agentic/**init**.py
[AutoAPI] Mapping Data... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/agentic/agentic_rag_agent.py
[AutoAPI] Mapping Data... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/agentic/agent.py
[AutoAPI] Mapping Data... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/agentic/document_grader.py
[AutoAPI] Mapping Data... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/agentic/query_rewriter.py
[AutoAPI] Mapping Data... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_corr/state.py
[AutoAPI] Mapping Data... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_corr/engines.py
[AutoAPI] Mapping Data... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_corr/config.py
[AutoAPI] Mapping Data... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_corr/**init**.py
[AutoAPI] Mapping Data... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_corr/agent.py
[AutoAPI] Mapping Data... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/corrective/**init**.py
[AutoAPI] Mapping Data... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/corrective/agent.py
[AutoAPI] Mapping Data... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/corrective/agent_v2.py
[AutoAPI] Mapping Data... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/llm_rag/state.py
[AutoAPI] Mapping Data... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/llm_rag/config.py
[AutoAPI] Mapping Data... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/llm_rag/**init**.py
[AutoAPI] Mapping Data... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/llm_rag/engine.py
[AutoAPI] Mapping Data... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/llm_rag/agent.py
[AutoAPI] Mapping Data... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_query/agent.py
[AutoAPI] Mapping Data... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/long_term_memory/state.py
[AutoAPI] Mapping Data... [ 50%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/long_term_memory/engines.py
[AutoAPI] Mapping Data... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/long_term_memory/models.py
[AutoAPI] Mapping Data... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/long_term_memory/aug_llm.py
[AutoAPI] Mapping Data... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/long_term_memory/nodes.py
[AutoAPI] Mapping Data... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/long_term_memory/**init**.py
[AutoAPI] Mapping Data... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/long_term_memory/agent.py
[AutoAPI] Mapping Data... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/long_term_memory/tools.py
[AutoAPI] Mapping Data... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/dynamic_supervisor/state.py
[AutoAPI] Mapping Data... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/dynamic_supervisor/models.py
[AutoAPI] Mapping Data... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/dynamic_supervisor/**init**.py
[AutoAPI] Mapping Data... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/dynamic_supervisor/agent.py
[AutoAPI] Mapping Data... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/dynamic_supervisor/prompts.py
[AutoAPI] Mapping Data... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/dynamic_supervisor/tools.py
[AutoAPI] Mapping Data... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_loader/**init**.py
[AutoAPI] Mapping Data... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_loader/directory/**init**.py
[AutoAPI] Mapping Data... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_loader/directory/agent.py
[AutoAPI] Mapping Data... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_loader/base/**init**.py
[AutoAPI] Mapping Data... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_loader/base/agent.py
[AutoAPI] Mapping Data... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_loader/web/**init**.py
[AutoAPI] Mapping Data... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_loader/web/agent.py
[AutoAPI] Mapping Data... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_loader/file/**init**.py
[AutoAPI] Mapping Data... [ 51%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_loader/file/agent.py
[AutoAPI] Mapping Data... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/structured/models.py
[AutoAPI] Mapping Data... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/structured/**init**.py
[AutoAPI] Mapping Data... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/structured/agent.py
[AutoAPI] Mapping Data... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/structured/prompts.py
[AutoAPI] Mapping Data... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/state.py
[AutoAPI] Mapping Data... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/enhanced_agent_v3.py
[AutoAPI] Mapping Data... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/config.py
[AutoAPI] Mapping Data... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/**init**.py
[AutoAPI] Mapping Data... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/enhanced_react_agent.py
[AutoAPI] Mapping Data... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/agent.py
[AutoAPI] Mapping Data... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/dynamic_react_agent.py
[AutoAPI] Mapping Data... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/agent_v3.py
[AutoAPI] Mapping Data... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/archive/meta/**init**.py
[AutoAPI] Mapping Data... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/**init**.py
[AutoAPI] Mapping Data... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflection/state.py
[AutoAPI] Mapping Data... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflection/config.py
[AutoAPI] Mapping Data... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflection/models.py
[AutoAPI] Mapping Data... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflection/**init**.py
[AutoAPI] Mapping Data... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflection/agent.py
[AutoAPI] Mapping Data... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/state.py
[AutoAPI] Mapping Data... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/node.py
[AutoAPI] Mapping Data... [ 52%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/config.py
[AutoAPI] Mapping Data... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/models.py
[AutoAPI] Mapping Data... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/**init**.py
[AutoAPI] Mapping Data... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/utils.py
[AutoAPI] Mapping Data... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/agent.py
[AutoAPI] Mapping Data... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/v2/state.py
[AutoAPI] Mapping Data... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/v2/models.py
[AutoAPI] Mapping Data... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/v2/**init**.py
[AutoAPI] Mapping Data... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/v2/prompts.py
[AutoAPI] Mapping Data... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/v2/agents.py
[AutoAPI] Mapping Data... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/state.py
[AutoAPI] Mapping Data... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/config.py
[AutoAPI] Mapping Data... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/models.py
[AutoAPI] Mapping Data... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/**init**.py
[AutoAPI] Mapping Data... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/utils.py
[AutoAPI] Mapping Data... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/agent.py
[AutoAPI] Mapping Data... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/responder_with_retries.py
[AutoAPI] Mapping Data... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/prompts.py
[AutoAPI] Mapping Data... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/tools.py
[AutoAPI] Mapping Data... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/state.py
[AutoAPI] Mapping Data... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/engines.py
[AutoAPI] Mapping Data... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/config.py
[AutoAPI] Mapping Data... [ 53%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/models.py
[AutoAPI] Mapping Data... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/selector.py
[AutoAPI] Mapping Data... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/self_discover_simple_v4.py
[AutoAPI] Mapping Data... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/fixed_selector.py
[AutoAPI] Mapping Data... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/self_discover_multiagent.py
[AutoAPI] Mapping Data... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/**init**.py
[AutoAPI] Mapping Data... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/self_discover_enhanced_v4.py
[AutoAPI] Mapping Data... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/agent.py
[AutoAPI] Mapping Data... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/self_discover_sequential_v2.py
[AutoAPI] Mapping Data... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/agent2.py
[AutoAPI] Mapping Data... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/self_discover_working_v4.py
[AutoAPI] Mapping Data... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/self_discover_v4.py
[AutoAPI] Mapping Data... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/structurer/models.py
[AutoAPI] Mapping Data... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/structurer/**init**.py
[AutoAPI] Mapping Data... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/structurer/agent.py
[AutoAPI] Mapping Data... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/structurer/prompts.py
[AutoAPI] Mapping Data... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/executor/models.py
[AutoAPI] Mapping Data... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/executor/**init**.py
[AutoAPI] Mapping Data... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/executor/agent.py
[AutoAPI] Mapping Data... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/executor/prompts.py
[AutoAPI] Mapping Data... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/v2/state.py
[AutoAPI] Mapping Data... [ 54%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/v2/models.py
[AutoAPI] Mapping Data... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/v2/**init**.py
[AutoAPI] Mapping Data... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/v2/agent.py
[AutoAPI] Mapping Data... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/v2/prompts.py
[AutoAPI] Mapping Data... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/adapter/models.py
[AutoAPI] Mapping Data... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/adapter/**init**.py
[AutoAPI] Mapping Data... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/adapter/agent.py
[AutoAPI] Mapping Data... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/adapter/prompts.py
[AutoAPI] Mapping Data... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/selector/models.py
[AutoAPI] Mapping Data... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/selector/**init**.py
[AutoAPI] Mapping Data... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/selector/agent.py
[AutoAPI] Mapping Data... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/selector/prompts.py
[AutoAPI] Mapping Data... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/models.py
[AutoAPI] Mapping Data... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/**init**.py
[AutoAPI] Mapping Data... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/agent.py
[AutoAPI] Mapping Data... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/engines/premise_extractor.py
[AutoAPI] Mapping Data... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/engines/uncertainty_analyzer.py
[AutoAPI] Mapping Data... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/engines/bias_detector.py
[AutoAPI] Mapping Data... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/engines/**init**.py
[AutoAPI] Mapping Data... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/engines/synthesis_agent.py
[AutoAPI] Mapping Data... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/engines/logical_reasoner.py
[AutoAPI] Mapping Data... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/state.py
[AutoAPI] Mapping Data... [ 55%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/engines.py
[AutoAPI] Mapping Data... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/config.py
[AutoAPI] Mapping Data... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/models.py
[AutoAPI] Mapping Data... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/**init**.py
[AutoAPI] Mapping Data... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/agent.py
[AutoAPI] Mapping Data... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/modular/state.py
[AutoAPI] Mapping Data... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/modular/config.py
[AutoAPI] Mapping Data... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/modular/models.py
[AutoAPI] Mapping Data... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/modular/factory.py
[AutoAPI] Mapping Data... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/modular/**init**.py
[AutoAPI] Mapping Data... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/modular/agent.py
[AutoAPI] Mapping Data... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/modular/branches.py
[AutoAPI] Mapping Data... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/v2/state.py
[AutoAPI] Mapping Data... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/v2/engines.py
[AutoAPI] Mapping Data... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/v2/models.py
[AutoAPI] Mapping Data... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/v2/**init**.py
[AutoAPI] Mapping Data... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/v2/agent.py
[AutoAPI] Mapping Data... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/v2/prompts.py
[AutoAPI] Mapping Data... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/mcts/state.py
[AutoAPI] Mapping Data... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/mcts/config.py
[AutoAPI] Mapping Data... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/mcts/models.py
[AutoAPI] Mapping Data... [ 56%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/mcts/**init**.py
[AutoAPI] Mapping Data... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/mcts/utils.py
[AutoAPI] Mapping Data... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/mcts/agent.py
[AutoAPI] Mapping Data... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/**init**.py
[AutoAPI] Mapping Data... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v3/config.py
[AutoAPI] Mapping Data... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v3/**init**.py
[AutoAPI] Mapping Data... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v3/agent.py
[AutoAPI] Mapping Data... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/tool_handler.py
[AutoAPI] Mapping Data... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/agent3.py
[AutoAPI] Mapping Data... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/config.py
[AutoAPI] Mapping Data... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/models.py
[AutoAPI] Mapping Data... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/tool_utils.py
[AutoAPI] Mapping Data... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/nodes.py
[AutoAPI] Mapping Data... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/config2.py
[AutoAPI] Mapping Data... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/advanced_agent3.py
[AutoAPI] Mapping Data... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/dynamic_agent.py
[AutoAPI] Mapping Data... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/**init**.py
[AutoAPI] Mapping Data... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/state2.py
[AutoAPI] Mapping Data... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/agent.py
[AutoAPI] Mapping Data... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/agent2.py
[AutoAPI] Mapping Data... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/many_tools/state.py
[AutoAPI] Mapping Data... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/many_tools/engines.py
[AutoAPI] Mapping Data... [ 57%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/many_tools/models.py
[AutoAPI] Mapping Data... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/many_tools/nodes.py
[AutoAPI] Mapping Data... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/many_tools/**init**.py
[AutoAPI] Mapping Data... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react/state.py
[AutoAPI] Mapping Data... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react/config.py
[AutoAPI] Mapping Data... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react/tool_utils.py
[AutoAPI] Mapping Data... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react/agent.py
[AutoAPI] Mapping Data... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_many_tools/state.py
[AutoAPI] Mapping Data... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_many_tools/config.py
[AutoAPI] Mapping Data... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_many_tools/**init**.py
[AutoAPI] Mapping Data... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_many_tools/agent.py
[AutoAPI] Mapping Data... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent/state.py
[AutoAPI] Mapping Data... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent/**init**.py
[AutoAPI] Mapping Data... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent/agent.py
[AutoAPI] Mapping Data... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v2/state.py
[AutoAPI] Mapping Data... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v2/graph_utils.py
[AutoAPI] Mapping Data... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v2/tool_handling.py
[AutoAPI] Mapping Data... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v2/config.py
[AutoAPI] Mapping Data... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v2/**init**.py
[AutoAPI] Mapping Data... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v2/utils.py
[AutoAPI] Mapping Data... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v2/agent.py
[AutoAPI] Mapping Data... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v2/prompts.py
[AutoAPI] Mapping Data... [ 58%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/**init**.py
[AutoAPI] Mapping Data... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/tnt/state.py
[AutoAPI] Mapping Data... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/tnt/engines.py
[AutoAPI] Mapping Data... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/tnt/models.py
[AutoAPI] Mapping Data... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/tnt/**init**.py
[AutoAPI] Mapping Data... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/tnt/utils.py
[AutoAPI] Mapping Data... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/tnt/agent.py
[AutoAPI] Mapping Data... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/tnt/branches.py
[AutoAPI] Mapping Data... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/base/state.py
[AutoAPI] Mapping Data... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/base/**init**.py
[AutoAPI] Mapping Data... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/base/models/**init**.py
[AutoAPI] Mapping Data... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/**init**.py
[AutoAPI] Mapping Data... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/iterative_refinement/state.py
[AutoAPI] Mapping Data... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/iterative_refinement/engines.py
[AutoAPI] Mapping Data... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/iterative_refinement/config.py
[AutoAPI] Mapping Data... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/iterative_refinement/**init**.py
[AutoAPI] Mapping Data... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/iterative_refinement/agent.py
[AutoAPI] Mapping Data... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/map_branch/state.py
[AutoAPI] Mapping Data... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/map_branch/engines.py
[AutoAPI] Mapping Data... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/map_branch/config.py
[AutoAPI] Mapping Data... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/map_branch/**init**.py
[AutoAPI] Mapping Data... [ 59%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/map_branch/agent.py
[AutoAPI] Mapping Data... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/summarizer/map_branch/prompts.py
[AutoAPI] Mapping Data... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/**init**.py
[AutoAPI] Mapping Data... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/state.py
[AutoAPI] Mapping Data... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/engines.py
[AutoAPI] Mapping Data... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/config.py
[AutoAPI] Mapping Data... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/models.py
[AutoAPI] Mapping Data... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/**init**.py
[AutoAPI] Mapping Data... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/utils.py
[AutoAPI] Mapping Data... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/agent.py
[AutoAPI] Mapping Data... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_map_merge/agent2.py
[AutoAPI] Mapping Data... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_base/models.py
[AutoAPI] Mapping Data... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_base/**init**.py
[AutoAPI] Mapping Data... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_iterative_refinement/state.py
[AutoAPI] Mapping Data... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_iterative_refinement/engines.py
[AutoAPI] Mapping Data... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_iterative_refinement/config.py
[AutoAPI] Mapping Data... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_iterative_refinement/**init**.py
[AutoAPI] Mapping Data... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_iterative_refinement/utils.py
[AutoAPI] Mapping Data... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/kg/kg_iterative_refinement/agent.py
[AutoAPI] Mapping Data... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/state.py
[AutoAPI] Mapping Data... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/config.py
[AutoAPI] Mapping Data... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/models.py
[AutoAPI] Mapping Data... [ 60%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/factory.py
[AutoAPI] Mapping Data... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/**init**.py
[AutoAPI] Mapping Data... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/utils.py
[AutoAPI] Mapping Data... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_modifiers/complex_extraction/agent.py
[AutoAPI] Mapping Data... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/utils/**init**.py
[AutoAPI] Mapping Data... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/utils/utils.py
[AutoAPI] Mapping Data... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_standalone.py
[AutoAPI] Mapping Data... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/base.py
[AutoAPI] Mapping Data... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced_clean_multi_agent.py
[AutoAPI] Mapping Data... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_generic.py
[AutoAPI] Mapping Data... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced_sequential_agent.py
[AutoAPI] Mapping Data... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced_parallel_agent.py
[AutoAPI] Mapping Data... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/**init**.py
[AutoAPI] Mapping Data... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced_dynamic_supervisor.py
[AutoAPI] Mapping Data... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced_supervisor_agent.py
[AutoAPI] Mapping Data... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/multi_agent.py
[AutoAPI] Mapping Data... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/clean.py
[AutoAPI] Mapping Data... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/multi_agent_v4.py
[AutoAPI] Mapping Data... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_v3.py
[AutoAPI] Mapping Data... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_v4.py
[AutoAPI] Mapping Data... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/sequential/**init**.py
[AutoAPI] Mapping Data... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/sequential/agent.py
[AutoAPI] Mapping Data... [ 61%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/archive/enhanced_base.py
[AutoAPI] Mapping Data... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/archive/base.py
[AutoAPI] Mapping Data... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/archive/agent.py
[AutoAPI] Mapping Data... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/archive/configurable_base.py
[AutoAPI] Mapping Data... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/routing_patterns.py
[AutoAPI] Mapping Data... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/list_multi_agent.py
[AutoAPI] Mapping Data... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/proper_list_multi_agent.py
[AutoAPI] Mapping Data... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/implementations/clean_multi_agent.py
[AutoAPI] Mapping Data... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/implementations/simple_debug.py
[AutoAPI] Mapping Data... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/implementations/compatibility_enhanced_base.py
[AutoAPI] Mapping Data... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/implementations/multi_agent_v2.py
[AutoAPI] Mapping Data... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/implementations/clean_base.py
[AutoAPI] Mapping Data... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/implementations/self_discover_state.py
[AutoAPI] Mapping Data... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/experiments/implementations/proper_base.py
[AutoAPI] Mapping Data... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_processing/**init**.py
[AutoAPI] Mapping Data... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/document_processing/agent.py
[AutoAPI] Mapping Data... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/state.py
[AutoAPI] Mapping Data... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/graph_rag_retriever.py
[AutoAPI] Mapping Data... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/config.py
[AutoAPI] Mapping Data... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models.py
[AutoAPI] Mapping Data... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/multi_agent_coordinator.py
[AutoAPI] Mapping Data... [ 62%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/kg_generator_agent.py
[AutoAPI] Mapping Data... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/unified_memory_api.py
[AutoAPI] Mapping Data... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/memory_utils.py
[AutoAPI] Mapping Data... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/**init**.py
[AutoAPI] Mapping Data... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/agentic_rag_coordinator.py
[AutoAPI] Mapping Data... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/agent.py
[AutoAPI] Mapping Data... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/sphinx_config.py
[AutoAPI] Mapping Data... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/enhanced_retriever.py
[AutoAPI] Mapping Data... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models/base.py
[AutoAPI] Mapping Data... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models/**init**.py
[AutoAPI] Mapping Data... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models/meta.py
[AutoAPI] Mapping Data... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models/procedural/models.py
[AutoAPI] Mapping Data... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models/procedural/**init**.py
[AutoAPI] Mapping Data... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models/semantic/models.py
[AutoAPI] Mapping Data... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models/semantic/**init**.py
[AutoAPI] Mapping Data... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models/semantic/mixins.py
[AutoAPI] Mapping Data... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models/episodic/models.py
[AutoAPI] Mapping Data... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models/episodic/**init**.py
[AutoAPI] Mapping Data... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/models/episodic/mixins.py
[AutoAPI] Mapping Data... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/core/classifier.py
[AutoAPI] Mapping Data... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/core/**init**.py
[AutoAPI] Mapping Data... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/core/types.py
[AutoAPI] Mapping Data... [ 63%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/core/stores.py
[AutoAPI] Mapping Data... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/base.py
[AutoAPI] Mapping Data... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/**init**.py
[AutoAPI] Mapping Data... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/pro_search/models.py
[AutoAPI] Mapping Data... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/pro_search/**init**.py
[AutoAPI] Mapping Data... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/pro_search/agent.py
[AutoAPI] Mapping Data... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/labs/models.py
[AutoAPI] Mapping Data... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/labs/**init**.py
[AutoAPI] Mapping Data... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/labs/agent.py
[AutoAPI] Mapping Data... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/deep_research/models.py
[AutoAPI] Mapping Data... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/deep_research/**init**.py
[AutoAPI] Mapping Data... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/deep_research/agent.py
[AutoAPI] Mapping Data... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/quick_search/models.py
[AutoAPI] Mapping Data... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/quick_search/**init**.py
[AutoAPI] Mapping Data... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/quick_search/agent.py
[AutoAPI] Mapping Data... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/**init**.py
[AutoAPI] Mapping Data... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/collaberative/state.py
[AutoAPI] Mapping Data... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/collaberative/**init**.py
[AutoAPI] Mapping Data... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/collaberative/agent.py
[AutoAPI] Mapping Data... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/base/state.py
[AutoAPI] Mapping Data... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/base/**init**.py
[AutoAPI] Mapping Data... [ 64%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/base/agent.py
[AutoAPI] Mapping Data... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/round_robin/**init**.py
[AutoAPI] Mapping Data... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/round_robin/agent.py
[AutoAPI] Mapping Data... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/debate/state.py
[AutoAPI] Mapping Data... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/debate/**init**.py
[AutoAPI] Mapping Data... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/debate/agent.py
[AutoAPI] Mapping Data... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/directed/state.py
[AutoAPI] Mapping Data... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/directed/**init**.py
[AutoAPI] Mapping Data... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/directed/agent.py
[AutoAPI] Mapping Data... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/social_media/state.py
[AutoAPI] Mapping Data... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/social_media/models.py
[AutoAPI] Mapping Data... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/social_media/**init**.py
[AutoAPI] Mapping Data... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/social_media/agent.py
[AutoAPI] Mapping Data... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/state.py
[AutoAPI] Mapping Data... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/base.py
[AutoAPI] Mapping Data... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/models.py
[AutoAPI] Mapping Data... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/nodes.py
[AutoAPI] Mapping Data... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/**init**.py
[AutoAPI] Mapping Data... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/utils.py
[AutoAPI] Mapping Data... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/agent.py
[AutoAPI] Mapping Data... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/interview/state.py
[AutoAPI] Mapping Data... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/interview/models.py
[AutoAPI] Mapping Data... [ 65%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/interview/nodes.py
[AutoAPI] Mapping Data... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/interview/**init**.py
[AutoAPI] Mapping Data... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/interview/utils.py
[AutoAPI] Mapping Data... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/interview/agent.py
[AutoAPI] Mapping Data... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/interview/tools.py
[AutoAPI] Mapping Data... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/static_supervisor_with_sync.py
[AutoAPI] Mapping Data... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/summarizer.py
[AutoAPI] Mapping Data... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/dynamic_supervisor_enhanced.py
[AutoAPI] Mapping Data... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/**init**.py
[AutoAPI] Mapping Data... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/dynamic_supervisor.py
[AutoAPI] Mapping Data... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/supervisor.py
[AutoAPI] Mapping Data... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/supervisor/**init**.py
[AutoAPI] Mapping Data... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/rag_memory_agent.py
[AutoAPI] Mapping Data... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/extraction_prompts.py
[AutoAPI] Mapping Data... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/react_memory_agent.py
[AutoAPI] Mapping Data... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/standalone_rag_memory.py
[AutoAPI] Mapping Data... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/memory_state_original.py
[AutoAPI] Mapping Data... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/multi_memory_agent.py
[AutoAPI] Mapping Data... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/standalone_memory_agent_free.py
[AutoAPI] Mapping Data... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/integrated_memory_system.py
[AutoAPI] Mapping Data... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/react_memory_coordinator.py
[AutoAPI] Mapping Data... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/long_term_memory_agent.py
[AutoAPI] Mapping Data... [ 66%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/memory_models_standalone.py
[AutoAPI] Mapping Data... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/time_weighted_retriever.py
[AutoAPI] Mapping Data... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/**init**.py
[AutoAPI] Mapping Data... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/memory_state_with_tokens.py
[AutoAPI] Mapping Data... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/kg_memory_agent.py
[AutoAPI] Mapping Data... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/message_document_converter.py
[AutoAPI] Mapping Data... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/memory_state.py
[AutoAPI] Mapping Data... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/advanced_rag_memory_agent.py
[AutoAPI] Mapping Data... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/memory_tools.py
[AutoAPI] Mapping Data... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/graph_memory_agent.py
[AutoAPI] Mapping Data... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/multi_react_memory_system.py
[AutoAPI] Mapping Data... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/simple_memory_agent_deepseek.py
[AutoAPI] Mapping Data... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/token_tracker.py
[AutoAPI] Mapping Data... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/multi_memory_coordinator.py
[AutoAPI] Mapping Data... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/conversation_memory_agent.py
[AutoAPI] Mapping Data... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/simple_memory_agent.py
[AutoAPI] Mapping Data... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/patterns/react_structured_agent_variants.py
[AutoAPI] Mapping Data... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/patterns/sequential_workflow_agent.py
[AutoAPI] Mapping Data... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/patterns/react_with_structured_output.py
[AutoAPI] Mapping Data... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/patterns/**init**.py
[AutoAPI] Mapping Data... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/patterns/react_structured_reflection_patterns.py
[AutoAPI] Mapping Data... [ 67%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/patterns/sequential_with_structured_output.py
[AutoAPI] Mapping Data... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/patterns/hybrid_multi_agent_patterns.py
[AutoAPI] Mapping Data... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/patterns/simple_rag_agent_pattern.py
[AutoAPI] Mapping Data... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/self_healing_code/state.py
[AutoAPI] Mapping Data... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/self_healing_code/**init**.py
[AutoAPI] Mapping Data... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/self_healing_code/branches.py
[AutoAPI] Mapping Data... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/**init**.py
[AutoAPI] Mapping Data... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/report_of_the_week_tool.py
[AutoAPI] Mapping Data... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/arxiv.py
[AutoAPI] Mapping Data... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/genderize_tool.py
[AutoAPI] Mapping Data... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/pokebase_tool.py
[AutoAPI] Mapping Data... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/dataforseo_tool.py
[AutoAPI] Mapping Data... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/techy_phrase_tool.py
[AutoAPI] Mapping Data... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/duckduckgo_search.py
[AutoAPI] Mapping Data... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/eleven_labs.py
[AutoAPI] Mapping Data... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/hinge_tools.py
[AutoAPI] Mapping Data... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/youtube_search_tool.py
[AutoAPI] Mapping Data... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/stack_exchange.py
[AutoAPI] Mapping Data... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/binlist_lookup.py
[AutoAPI] Mapping Data... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/geek_jokes_tool.py
[AutoAPI] Mapping Data... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/corporate_bs_tool.py
[AutoAPI] Mapping Data... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/wolfram_alpha_tool.py
[AutoAPI] Mapping Data... [ 68%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/bing_search_tool_INC.py
[AutoAPI] Mapping Data... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/**init**.py
[AutoAPI] Mapping Data... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/scene_explain_tool.py
[AutoAPI] Mapping Data... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/translate_tools.py
[AutoAPI] Mapping Data... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/search_tools.py
[AutoAPI] Mapping Data... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/openaq_tool.py
[AutoAPI] Mapping Data... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/yfinance_tool.py
[AutoAPI] Mapping Data... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/dalle_image_generator_tool.py
[AutoAPI] Mapping Data... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/open_food_tool.py
[AutoAPI] Mapping Data... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/merriam_webster.py
[AutoAPI] Mapping Data... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/apify_tools.py
[AutoAPI] Mapping Data... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/agify_tool.py
[AutoAPI] Mapping Data... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/domain_search_tool.py
[AutoAPI] Mapping Data... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/asknews_tool.py
[AutoAPI] Mapping Data... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/dev_tools.py
[AutoAPI] Mapping Data... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/discord_tools.py
[AutoAPI] Mapping Data... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/ionic_tool.py
[AutoAPI] Mapping Data... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/brave_search.py
[AutoAPI] Mapping Data... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/pubmed.py
[AutoAPI] Mapping Data... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/reddit_search.py
[AutoAPI] Mapping Data... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/fruityvice_tool.py
[AutoAPI] Mapping Data... [ 69%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_places.py
[AutoAPI] Mapping Data... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_jobs.py
[AutoAPI] Mapping Data... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_trends.py
[AutoAPI] Mapping Data... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_search.py
[AutoAPI] Mapping Data... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_finance.py
[AutoAPI] Mapping Data... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_books.py
[AutoAPI] Mapping Data... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/**init**.py
[AutoAPI] Mapping Data... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_lens.py
[AutoAPI] Mapping Data... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/google/google_scholar.py
[AutoAPI] Mapping Data... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/google_calendar.py
[AutoAPI] Mapping Data... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/base.py
[AutoAPI] Mapping Data... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/nasa_toolkit.py
[AutoAPI] Mapping Data... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/jira_toolkit.py
[AutoAPI] Mapping Data... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/nla_toolkit.py
[AutoAPI] Mapping Data... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/gmail_toolkit.py
[AutoAPI] Mapping Data... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/twilio_toolkit.py
[AutoAPI] Mapping Data... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/free_to_game_toolkit.py
[AutoAPI] Mapping Data... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/rick_and_morty_toolkit.py
[AutoAPI] Mapping Data... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/yugiioh_toolkit.py
[AutoAPI] Mapping Data... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/citydsk_toolkit.py
[AutoAPI] Mapping Data... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/poetry_db_toolkit.py
[AutoAPI] Mapping Data... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/mongodb_toolkit.py
[AutoAPI] Mapping Data... [ 70%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/powerbi_toolkit.py
[AutoAPI] Mapping Data... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/gitlab_toolkit.py
[AutoAPI] Mapping Data... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/office_365.py
[AutoAPI] Mapping Data... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dataforseo_toolkit.py
[AutoAPI] Mapping Data... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/**init**.py
[AutoAPI] Mapping Data... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/alpha_vantage.py
[AutoAPI] Mapping Data... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/lcbo_toolkit.py
[AutoAPI] Mapping Data... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/trip_advisor_toolkit.py
[AutoAPI] Mapping Data... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/fred_toolkit.py
[AutoAPI] Mapping Data... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/clickup_toolkit.py
[AutoAPI] Mapping Data... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/sql_db_toolkit.py
[AutoAPI] Mapping Data... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/rps_101_toolkit.py
[AutoAPI] Mapping Data... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/slack_toolkit.py
[AutoAPI] Mapping Data... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/stack_exchange_toolkit.py
[AutoAPI] Mapping Data... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/chuck_norris_jokes_toolkit.py
[AutoAPI] Mapping Data... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/stripe_toolkit.py
[AutoAPI] Mapping Data... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/azure_ai_services_toolkit.py
[AutoAPI] Mapping Data... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/weather.py
[AutoAPI] Mapping Data... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/pandas_toolkits.py
[AutoAPI] Mapping Data... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/steam_toolkit.py
[AutoAPI] Mapping Data... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/github_toolkit.py
[AutoAPI] Mapping Data... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/request_tools.py
[AutoAPI] Mapping Data... [ 71%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/amadues_toolkit.py
[AutoAPI] Mapping Data... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/polygon_toolkit.py
[AutoAPI] Mapping Data... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/useless_facts_toolkit.py
[AutoAPI] Mapping Data... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/vbible_toolkit.py
[AutoAPI] Mapping Data... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/openlibrary_toolkit.py
[AutoAPI] Mapping Data... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/financialdatasets_toolkit.py
[AutoAPI] Mapping Data... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/gradio_toolkit.py
[AutoAPI] Mapping Data... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/**init**.py
[AutoAPI] Mapping Data... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/tools.py
[AutoAPI] Mapping Data... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/permission.py
[AutoAPI] Mapping Data... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/shell.py
[AutoAPI] Mapping Data... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/background_process_manager.py
[AutoAPI] Mapping Data... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/shell/remote_execution.py
[AutoAPI] Mapping Data... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/**init**.py
[AutoAPI] Mapping Data... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/multi_file_rename.py
[AutoAPI] Mapping Data... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/import_consolidator.py
[AutoAPI] Mapping Data... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/refactor.py
[AutoAPI] Mapping Data... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/type_hints.py
[AutoAPI] Mapping Data... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/function_logging_transformer.py
[AutoAPI] Mapping Data... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/print_to_logging.py
[AutoAPI] Mapping Data... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/type_checking.py
[AutoAPI] Mapping Data... [ 72%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/dependency_analyzer.py
[AutoAPI] Mapping Data... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/complexity_analyzer.py
[AutoAPI] Mapping Data... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/code_smell_detector.py
[AutoAPI] Mapping Data... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/function_call_analyzer.py
[AutoAPI] Mapping Data... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/import_analyzer.py
[AutoAPI] Mapping Data... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/automatic_test_case_generator.py
[AutoAPI] Mapping Data... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/project_creation/**init**.py
[AutoAPI] Mapping Data... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/dev/project_creation/github.py
[AutoAPI] Mapping Data... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/base.py
[AutoAPI] Mapping Data... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/models.py
[AutoAPI] Mapping Data... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/app_dep.py
[AutoAPI] Mapping Data... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/core.py
[AutoAPI] Mapping Data... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry.py
WARNING: Unknown type: placeholder
WARNING: Unknown type: placeholder
[AutoAPI] Mapping Data... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/**init**.py
[AutoAPI] Mapping Data... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/router.py
[AutoAPI] Mapping Data... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/tic_tac_toe_api.py
[AutoAPI] Mapping Data... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/game_agent.py
[AutoAPI] Mapping Data... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/connect4_api.py
[AutoAPI] Mapping Data... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/db.py
[AutoAPI] Mapping Data... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/discovery.py
[AutoAPI] Mapping Data... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/serialization.py
[AutoAPI] Mapping Data... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/**init\_**lazy.py
[AutoAPI] Mapping Data... [ 73%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/llms/models.py
[AutoAPI] Mapping Data... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/llms/**init**.py
[AutoAPI] Mapping Data... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/llms/api.py
[AutoAPI] Mapping Data... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/persistence/conversations.py
[AutoAPI] Mapping Data... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/persistence/**init**.py
[AutoAPI] Mapping Data... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/persistence/supabase_adapter.py
[AutoAPI] Mapping Data... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/internal_websockets/**init**.py
[AutoAPI] Mapping Data... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/internal_websockets/handlers.py
[AutoAPI] Mapping Data... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/internal_websockets/manager.py
[AutoAPI] Mapping Data... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/fetchers/**init**.py
[AutoAPI] Mapping Data... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/fetchers/lite_llm_import.py
[AutoAPI] Mapping Data... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/run_integrated_api.py
[AutoAPI] Mapping Data... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/base.py
[AutoAPI] Mapping Data... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/simple_chess_ws.py
[AutoAPI] Mapping Data... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/integrate_games.py
[AutoAPI] Mapping Data... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/auto_discovery.py
[AutoAPI] Mapping Data... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/general_games_api.py
[AutoAPI] Mapping Data... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_socket.py
[AutoAPI] Mapping Data... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/app_dep.py
[AutoAPI] Mapping Data... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/serve_chess_client.py
[AutoAPI] Mapping Data... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/middleware.py
[AutoAPI] Mapping Data... [ 74%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/run_simple.py
[AutoAPI] Mapping Data... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_api.py
[AutoAPI] Mapping Data... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/run_chess_api.py
[AutoAPI] Mapping Data... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/registry.py
[AutoAPI] Mapping Data... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/router.py
[AutoAPI] Mapping Data... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/tic_tac_toe_api.py
[AutoAPI] Mapping Data... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/run_simplified.py
[AutoAPI] Mapping Data... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router_fixed.py
[AutoAPI] Mapping Data... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router.py
[AutoAPI] Mapping Data... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_agent.py
[AutoAPI] Mapping Data... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/connect4_api.py
[AutoAPI] Mapping Data... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/db.py
[AutoAPI] Mapping Data... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/run_game_api.py
[AutoAPI] Mapping Data... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py
[AutoAPI] Mapping Data... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/run_games_api.py
[AutoAPI] Mapping Data... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/llms/models.py
[AutoAPI] Mapping Data... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/llms/**init**.py
[AutoAPI] Mapping Data... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/llms/api.py
[AutoAPI] Mapping Data... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes_enhanced.py
[AutoAPI] Mapping Data... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py
[AutoAPI] Mapping Data... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes_fixed.py
[AutoAPI] Mapping Data... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py
[AutoAPI] Mapping Data... [ 75%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/**init**.py
[AutoAPI] Mapping Data... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/conversation_routes.py
[AutoAPI] Mapping Data... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes.py
[AutoAPI] Mapping Data... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes.py
[AutoAPI] Mapping Data... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/games.py
[AutoAPI] Mapping Data... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/llm_routes.py
[AutoAPI] Mapping Data... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routes/tools_routes_enhanced.py
[AutoAPI] Mapping Data... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/routers/games.py
[AutoAPI] Mapping Data... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/middleware/supabase_logging.py
[AutoAPI] Mapping Data... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/middleware/**init**.py
[AutoAPI] Mapping Data... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/middleware/rate_limit.py
[AutoAPI] Mapping Data... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/middleware/auth.py
[AutoAPI] Mapping Data... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/middleware/logging.py
[AutoAPI] Mapping Data... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/base.py
[AutoAPI] Mapping Data... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/models.py
[AutoAPI] Mapping Data... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/core.py
[AutoAPI] Mapping Data... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/**init**.py
[AutoAPI] Mapping Data... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/lazy_core.py
[AutoAPI] Mapping Data... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/db.py
[AutoAPI] Mapping Data... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/discovery.py
[AutoAPI] Mapping Data... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/serialization.py
[AutoAPI] Mapping Data... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/providers/base.py
[AutoAPI] Mapping Data... [ 76%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/providers/**init**.py
[AutoAPI] Mapping Data... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py
[AutoAPI] Mapping Data... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/importers/tak.py
[AutoAPI] Mapping Data... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/importers/litellm_importer.py
[AutoAPI] Mapping Data... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/importers/**init**.py
[AutoAPI] Mapping Data... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/importers/embeddings_importer.py
[AutoAPI] Mapping Data... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/utils/vault_migration_script.py
[AutoAPI] Mapping Data... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/utils/**init**.py
[AutoAPI] Mapping Data... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/utils/logging.py
[AutoAPI] Mapping Data... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/registries/**init**.py
[AutoAPI] Mapping Data... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registry/registries/model_registry.py
[AutoAPI] Mapping Data... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/auth/middleware.py
[AutoAPI] Mapping Data... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/auth/**init**.py
[AutoAPI] Mapping Data... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/auth/dependencies.py
[AutoAPI] Mapping Data... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/auth/supabase.py
[AutoAPI] Mapping Data... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/auth/credits.py
[AutoAPI] Mapping Data... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/providers/base.py
[AutoAPI] Mapping Data... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/providers/**init**.py
[AutoAPI] Mapping Data... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/providers/agent_provider.py
[AutoAPI] Mapping Data... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/mcp/**init**.py
[AutoAPI] Mapping Data... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/mcp/health.py
[AutoAPI] Mapping Data... [ 77%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/mcp/client.py
[AutoAPI] Mapping Data... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/mcp/discovery.py
[AutoAPI] Mapping Data... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/importers/tak.py
[AutoAPI] Mapping Data... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/importers/litellm_importer.py
[AutoAPI] Mapping Data... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/importers/**init**.py
[AutoAPI] Mapping Data... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/importers/embeddings_importer.py
[AutoAPI] Mapping Data... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/db/schema.py
[AutoAPI] Mapping Data... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/db/inspect_supabase.py
[AutoAPI] Mapping Data... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/db/**init**.py
[AutoAPI] Mapping Data... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/db/supabase.py
[AutoAPI] Mapping Data... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/utils/vault_migration_script.py
[AutoAPI] Mapping Data... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/utils/**init**.py
[AutoAPI] Mapping Data... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/utils/logging.py
[AutoAPI] Mapping Data... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/conversations/**init**.py
[AutoAPI] Mapping Data... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/conversations/manager.py
[AutoAPI] Mapping Data... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/config/settings.py
[AutoAPI] Mapping Data... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/config/**init**.py
[AutoAPI] Mapping Data... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/config/environment.py
[AutoAPI] Mapping Data... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registries/**init**.py
[AutoAPI] Mapping Data... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/registries/model_registry.py
[AutoAPI] Mapping Data... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/benchmark.py
[AutoAPI] Mapping Data... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/**init**.py
[AutoAPI] Mapping Data... [ 78%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/llm_config_factory.py
[AutoAPI] Mapping Data... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/common/voting_system.py
[AutoAPI] Mapping Data... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/state.py
[AutoAPI] Mapping Data... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/engines.py
[AutoAPI] Mapping Data... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/state_manager.py
[AutoAPI] Mapping Data... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/config.py
[AutoAPI] Mapping Data... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/models.py
[AutoAPI] Mapping Data... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/configurable_config.py
[AutoAPI] Mapping Data... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/ui.py
[AutoAPI] Mapping Data... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/controller.py
[AutoAPI] Mapping Data... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/**init**.py
[AutoAPI] Mapping Data... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/generic_engines.py
[AutoAPI] Mapping Data... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/agent.py
[AutoAPI] Mapping Data... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/clue/runner.py
[AutoAPI] Mapping Data... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/state.py
[AutoAPI] Mapping Data... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/engines.py
[AutoAPI] Mapping Data... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/state_manager.py
[AutoAPI] Mapping Data... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/config.py
[AutoAPI] Mapping Data... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/models.py
[AutoAPI] Mapping Data... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/configurable_config.py
[AutoAPI] Mapping Data... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/ui.py
[AutoAPI] Mapping Data... [ 79%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/**init**.py
[AutoAPI] Mapping Data... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/generic_engines.py
[AutoAPI] Mapping Data... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/checkers/agent.py
[AutoAPI] Mapping Data... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/state.py
[AutoAPI] Mapping Data... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/engines.py
[AutoAPI] Mapping Data... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/state_manager.py
[AutoAPI] Mapping Data... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/config.py
[AutoAPI] Mapping Data... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/models.py
[AutoAPI] Mapping Data... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/configurable_config.py
[AutoAPI] Mapping Data... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/ui.py
[AutoAPI] Mapping Data... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/**init**.py
[AutoAPI] Mapping Data... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/generic_engines.py
[AutoAPI] Mapping Data... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mastermind/agent.py
[AutoAPI] Mapping Data... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/state.py
[AutoAPI] Mapping Data... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/engines.py
[AutoAPI] Mapping Data... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/state_manager.py
[AutoAPI] Mapping Data... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/config.py
[AutoAPI] Mapping Data... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/simple_demo.py
[AutoAPI] Mapping Data... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/verify_imports.py
[AutoAPI] Mapping Data... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/models.py
[AutoAPI] Mapping Data... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/mock_runner.py
[AutoAPI] Mapping Data... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/configurable_config.py
[AutoAPI] Mapping Data... [ 80%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/**init**.py
[AutoAPI] Mapping Data... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/generic_engines.py
[AutoAPI] Mapping Data... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/agent.py
[AutoAPI] Mapping Data... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mafia/simple_runner.py
[AutoAPI] Mapping Data... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/state.py
[AutoAPI] Mapping Data... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/engines.py
[AutoAPI] Mapping Data... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/state_manager.py
[AutoAPI] Mapping Data... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/config.py
[AutoAPI] Mapping Data... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/models.py
[AutoAPI] Mapping Data... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/configurable_config.py
[AutoAPI] Mapping Data... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/ui.py
[AutoAPI] Mapping Data... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/**init**.py
[AutoAPI] Mapping Data... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/generic_engines.py
[AutoAPI] Mapping Data... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/agent.py
[AutoAPI] Mapping Data... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/dominoes/rich_ui.py
[AutoAPI] Mapping Data... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base/state.py
[AutoAPI] Mapping Data... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base/state_manager.py
[AutoAPI] Mapping Data... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base/config.py
[AutoAPI] Mapping Data... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base/models.py
[AutoAPI] Mapping Data... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base/factory.py
[AutoAPI] Mapping Data... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base/**init**.py
[AutoAPI] Mapping Data... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base/utils.py
[AutoAPI] Mapping Data... [ 81%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base/agent.py
[AutoAPI] Mapping Data... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/state.py
[AutoAPI] Mapping Data... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/engines.py
[AutoAPI] Mapping Data... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/player_agent.py
[AutoAPI] Mapping Data... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/config.py
[AutoAPI] Mapping Data... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/simple_demo.py
[AutoAPI] Mapping Data... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/models.py
[AutoAPI] Mapping Data... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/standalone_demo.py
[AutoAPI] Mapping Data... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/configurable_config.py
[AutoAPI] Mapping Data... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/ui.py
[AutoAPI] Mapping Data... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/**init**.py
[AutoAPI] Mapping Data... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/generic_engines.py
[AutoAPI] Mapping Data... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/utils.py
[AutoAPI] Mapping Data... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/agent.py
[AutoAPI] Mapping Data... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/run_game.py
[AutoAPI] Mapping Data... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/game_agent.py
[AutoAPI] Mapping Data... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/ui_fixed.py
[AutoAPI] Mapping Data... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/prompts.py
[AutoAPI] Mapping Data... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/main_agent.py
[AutoAPI] Mapping Data... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/game/property.py
[AutoAPI] Mapping Data... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/game/player.py
[AutoAPI] Mapping Data... [ 82%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/game/**init**.py
[AutoAPI] Mapping Data... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/game/types.py
[AutoAPI] Mapping Data... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/game/card.py
[AutoAPI] Mapping Data... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/game/game.py
[AutoAPI] Mapping Data... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/state.py
[AutoAPI] Mapping Data... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/engines.py
[AutoAPI] Mapping Data... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/state_manager.py
[AutoAPI] Mapping Data... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/player_agent.py
[AutoAPI] Mapping Data... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/config.py
[AutoAPI] Mapping Data... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/models.py
[AutoAPI] Mapping Data... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/configurable_config.py
[AutoAPI] Mapping Data... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/ui.py
[AutoAPI] Mapping Data... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/**init**.py
[AutoAPI] Mapping Data... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/generic_engines.py
[AutoAPI] Mapping Data... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/utils.py
[AutoAPI] Mapping Data... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/agent.py
[AutoAPI] Mapping Data... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/game_agent.py
[AutoAPI] Mapping Data... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/hold_em/engine_logging.py
[AutoAPI] Mapping Data... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/api/setup.py
[AutoAPI] Mapping Data... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/api/**init**.py
[AutoAPI] Mapping Data... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/api/general_api.py
[AutoAPI] Mapping Data... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/state.py
[AutoAPI] Mapping Data... [ 83%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/engines.py
[AutoAPI] Mapping Data... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/state_manager.py
[AutoAPI] Mapping Data... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/config.py
[AutoAPI] Mapping Data... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/models.py
[AutoAPI] Mapping Data... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/configurable_config.py
[AutoAPI] Mapping Data... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/ui.py
[AutoAPI] Mapping Data... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/standalone_game.py
[AutoAPI] Mapping Data... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/**init**.py
[AutoAPI] Mapping Data... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/generic_engines.py
[AutoAPI] Mapping Data... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/nim/agent.py
[AutoAPI] Mapping Data... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/multi_player/state.py
[AutoAPI] Mapping Data... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/multi_player/state_manager.py
[AutoAPI] Mapping Data... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/multi_player/config.py
[AutoAPI] Mapping Data... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/multi_player/models.py
[AutoAPI] Mapping Data... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/multi_player/factory.py
[AutoAPI] Mapping Data... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/multi_player/**init**.py
[AutoAPI] Mapping Data... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/multi_player/agent.py
[AutoAPI] Mapping Data... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/**init**.py
[AutoAPI] Mapping Data... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/base/state.py
[AutoAPI] Mapping Data... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/base/state_manager.py
[AutoAPI] Mapping Data... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/base/config.py
[AutoAPI] Mapping Data... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/base/factory.py
[AutoAPI] Mapping Data... [ 84%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/base/**init**.py
[AutoAPI] Mapping Data... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/base/template_generator.py
[AutoAPI] Mapping Data... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/base/utils.py
[AutoAPI] Mapping Data... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/base/agent.py
[AutoAPI] Mapping Data... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/multi_player/state.py
[AutoAPI] Mapping Data... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/multi_player/state_manager.py
[AutoAPI] Mapping Data... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/multi_player/config.py
[AutoAPI] Mapping Data... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/multi_player/models.py
[AutoAPI] Mapping Data... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/multi_player/factory.py
[AutoAPI] Mapping Data... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/multi_player/**init**.py
[AutoAPI] Mapping Data... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/multi_player/agent.py
[AutoAPI] Mapping Data... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/turn.py
[AutoAPI] Mapping Data... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/move.py
[AutoAPI] Mapping Data... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/player.py
[AutoAPI] Mapping Data... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/**init**.py
[AutoAPI] Mapping Data... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/board.py
[AutoAPI] Mapping Data... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/agent.py
[AutoAPI] Mapping Data... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/container.py
[AutoAPI] Mapping Data... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/grid.py
[AutoAPI] Mapping Data... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/position.py
[AutoAPI] Mapping Data... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/game.py
[AutoAPI] Mapping Data... [ 85%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/space.py
[AutoAPI] Mapping Data... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/rule.py
[AutoAPI] Mapping Data... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/piece.py
[AutoAPI] Mapping Data... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/boards/grid.py
[AutoAPI] Mapping Data... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/spaces/grid.py
[AutoAPI] Mapping Data... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/positions/grid.py
[AutoAPI] Mapping Data... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/framework/core/containers/deck.py
[AutoAPI] Mapping Data... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/tic_tac_toe/state.py
[AutoAPI] Mapping Data... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/tic_tac_toe/engines.py
[AutoAPI] Mapping Data... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/tic_tac_toe/state_manager.py
[AutoAPI] Mapping Data... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/tic_tac_toe/config.py
[AutoAPI] Mapping Data... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/tic_tac_toe/models.py
[AutoAPI] Mapping Data... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/tic_tac_toe/configurable_config.py
[AutoAPI] Mapping Data... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/tic_tac_toe/ui.py
[AutoAPI] Mapping Data... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/tic_tac_toe/**init**.py
[AutoAPI] Mapping Data... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/tic_tac_toe/generic_engines.py
[AutoAPI] Mapping Data... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/tic_tac_toe/agent.py
[AutoAPI] Mapping Data... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/tic_tac_toe/configurable_engines.py
[AutoAPI] Mapping Data... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/state.py
[AutoAPI] Mapping Data... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/engines.py
[AutoAPI] Mapping Data... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/state_manager.py
[AutoAPI] Mapping Data... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/config.py
[AutoAPI] Mapping Data... [ 86%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/models.py
[AutoAPI] Mapping Data... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/agent_original.py
[AutoAPI] Mapping Data... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/configurable_config.py
[AutoAPI] Mapping Data... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/**init**.py
[AutoAPI] Mapping Data... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/generic_engines.py
[AutoAPI] Mapping Data... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/agent.py
[AutoAPI] Mapping Data... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/mancala/state_original.py
[AutoAPI] Mapping Data... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/**init**.py
[AutoAPI] Mapping Data... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/agent_with_judges.py
[AutoAPI] Mapping Data... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/agent.py
[AutoAPI] Mapping Data... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/judges.py
[AutoAPI] Mapping Data... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/state.py
[AutoAPI] Mapping Data... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/engines.py
[AutoAPI] Mapping Data... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/state_manager.py
[AutoAPI] Mapping Data... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/config.py
[AutoAPI] Mapping Data... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/models.py
[AutoAPI] Mapping Data... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/factory.py
[AutoAPI] Mapping Data... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/configurable_config.py
[AutoAPI] Mapping Data... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/ui.py
[AutoAPI] Mapping Data... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/**init**.py
[AutoAPI] Mapping Data... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/generic_engines.py
[AutoAPI] Mapping Data... [ 87%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/connect4/agent.py
[AutoAPI] Mapping Data... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/state.py
[AutoAPI] Mapping Data... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/engines.py
[AutoAPI] Mapping Data... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/state_manager.py
[AutoAPI] Mapping Data... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/config.py
[AutoAPI] Mapping Data... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/models.py
[AutoAPI] Mapping Data... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/factory.py
[AutoAPI] Mapping Data... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/configurable_config.py
[AutoAPI] Mapping Data... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/ui.py
[AutoAPI] Mapping Data... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/enhanced_ui.py
[AutoAPI] Mapping Data... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/**init**.py
[AutoAPI] Mapping Data... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/generic_engines.py
[AutoAPI] Mapping Data... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/agent.py
[AutoAPI] Mapping Data... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/among_us/prompts.py
[AutoAPI] Mapping Data... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/state.py
[AutoAPI] Mapping Data... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/engines.py
[AutoAPI] Mapping Data... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/state_manager.py
[AutoAPI] Mapping Data... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/config.py
[AutoAPI] Mapping Data... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/models.py
[AutoAPI] Mapping Data... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/configurable_config.py
[AutoAPI] Mapping Data... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/ui.py
[AutoAPI] Mapping Data... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/llm_utils.py
[AutoAPI] Mapping Data... [ 88%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/**init**.py
[AutoAPI] Mapping Data... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/generic_engines.py
[AutoAPI] Mapping Data... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/utils.py
[AutoAPI] Mapping Data... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/agent.py
[AutoAPI] Mapping Data... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/configurable_engines.py
[AutoAPI] Mapping Data... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/chess/dynamic_config.py
[AutoAPI] Mapping Data... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/**init**.py
[AutoAPI] Mapping Data... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/uno/**init**.py
[AutoAPI] Mapping Data... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/models/**init**.py
[AutoAPI] Mapping Data... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/models/card.py
[AutoAPI] Mapping Data... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/bs/state.py
[AutoAPI] Mapping Data... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/bs/state_manager.py
[AutoAPI] Mapping Data... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/bs/config.py
[AutoAPI] Mapping Data... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/bs/models.py
[AutoAPI] Mapping Data... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/bs/**init**.py
[AutoAPI] Mapping Data... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/bs/agent.py
[AutoAPI] Mapping Data... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/bs/prompts.py
[AutoAPI] Mapping Data... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/poker/state.py
[AutoAPI] Mapping Data... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/poker/actions.py
[AutoAPI] Mapping Data... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/poker/**init**.py
[AutoAPI] Mapping Data... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/cards/standard/poker/scoring.py
[AutoAPI] Mapping Data... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/utils/recursion_config.py
[AutoAPI] Mapping Data... [ 89%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/utils/**init**.py
[AutoAPI] Mapping Data... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/**init**.py
[AutoAPI] Mapping Data... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/piece/tile.py
[AutoAPI] Mapping Data... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/players/base.py
[AutoAPI] Mapping Data... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/players/agent.py
[AutoAPI] Mapping Data... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/base/state.py
[AutoAPI] Mapping Data... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/base/engines.py
[AutoAPI] Mapping Data... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/base/state_manager.py
[AutoAPI] Mapping Data... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/base/config.py
[AutoAPI] Mapping Data... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/base/models.py
[AutoAPI] Mapping Data... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/base/player.py
[AutoAPI] Mapping Data... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/core_space.py
[AutoAPI] Mapping Data... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/**init**.py
WARNING: Unknown type: placeholder
WARNING: Unknown type: placeholder
WARNING: Unknown type: placeholder
WARNING: Unknown type: placeholder
WARNING: Unknown type: placeholder
WARNING: Unknown type: placeholder
WARNING: Unknown type: placeholder
WARNING: Unknown type: placeholder
WARNING: Unknown type: placeholder
WARNING: Unknown type: placeholder
[AutoAPI] Mapping Data... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/core_position.py
[AutoAPI] Mapping Data... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/core_game.py
[AutoAPI] Mapping Data... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/core_board.py
[AutoAPI] Mapping Data... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/piece.py
[AutoAPI] Mapping Data... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/pieces/core_game.py
[AutoAPI] Mapping Data... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/containers/base.py
[AutoAPI] Mapping Data... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/containers/deck.py
[AutoAPI] Mapping Data... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/containers/**init**.py
[AutoAPI] Mapping Data... [ 90%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/containers/container.py
[AutoAPI] Mapping Data... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/move/**init**.py
[AutoAPI] Mapping Data... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/agent/player_agent.py
[AutoAPI] Mapping Data... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/agent/game_config.py
[AutoAPI] Mapping Data... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/agent/generic_player_agent.py
[AutoAPI] Mapping Data... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/agent/**init**.py
[AutoAPI] Mapping Data... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/position/base.py
[AutoAPI] Mapping Data... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/position/**init**.py
[AutoAPI] Mapping Data... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/components/**init**.py
[AutoAPI] Mapping Data... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/components/cards/base.py
[AutoAPI] Mapping Data... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/components/cards/actions.py
[AutoAPI] Mapping Data... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/components/cards/**init**.py
[AutoAPI] Mapping Data... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/components/cards/scoring.py
[AutoAPI] Mapping Data... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/components/cards/turns.py
[AutoAPI] Mapping Data... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/components/cards/standard.py
[AutoAPI] Mapping Data... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/config/base.py
[AutoAPI] Mapping Data... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/config/**init**.py
[AutoAPI] Mapping Data... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/board/**init**.py
[AutoAPI] Mapping Data... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/state.py
[AutoAPI] Mapping Data... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/engines.py
[AutoAPI] Mapping Data... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/state_manager.py
[AutoAPI] Mapping Data... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/config.py
[AutoAPI] Mapping Data... [ 91%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/models.py
[AutoAPI] Mapping Data... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/configurable_config.py
[AutoAPI] Mapping Data... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/ui.py
[AutoAPI] Mapping Data... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/**init**.py
[AutoAPI] Mapping Data... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/generic_engines.py
[AutoAPI] Mapping Data... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/agent.py
[AutoAPI] Mapping Data... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/poker/prompts.py
[AutoAPI] Mapping Data... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate/state.py
[AutoAPI] Mapping Data... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate/engines.py
[AutoAPI] Mapping Data... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate/state_manager.py
[AutoAPI] Mapping Data... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate/config.py
[AutoAPI] Mapping Data... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate/models.py
[AutoAPI] Mapping Data... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate/factory.py
[AutoAPI] Mapping Data... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate/configurable_config.py
[AutoAPI] Mapping Data... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate/**init**.py
[AutoAPI] Mapping Data... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate/generic_engines.py
[AutoAPI] Mapping Data... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate/agent.py
[AutoAPI] Mapping Data... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/state.py
[AutoAPI] Mapping Data... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/engines.py
[AutoAPI] Mapping Data... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/state_manager.py
[AutoAPI] Mapping Data... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/config.py
[AutoAPI] Mapping Data... [ 92%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/models.py
[AutoAPI] Mapping Data... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/configurable_config.py
[AutoAPI] Mapping Data... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/ui.py
[AutoAPI] Mapping Data... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/**init**.py
[AutoAPI] Mapping Data... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/generic_engines.py
[AutoAPI] Mapping Data... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/agent.py
[AutoAPI] Mapping Data... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/rich_ui.py
[AutoAPI] Mapping Data... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/fox_and_geese/fixed_runner.py
[AutoAPI] Mapping Data... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base_v2/state.py
[AutoAPI] Mapping Data... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base_v2/player_agent.py
[AutoAPI] Mapping Data... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base_v2/models.py
[AutoAPI] Mapping Data... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/base_v2/**init**.py
[AutoAPI] Mapping Data... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/go/state.py
[AutoAPI] Mapping Data... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/go/engines.py
[AutoAPI] Mapping Data... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/go/state_manager.py
[AutoAPI] Mapping Data... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/go/config.py
[AutoAPI] Mapping Data... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/go/models.py
[AutoAPI] Mapping Data... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/go/**init**.py
[AutoAPI] Mapping Data... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/go/agent.py
[AutoAPI] Mapping Data... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/go/go_engine.py
[AutoAPI] Mapping Data... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/reversi/state.py
[AutoAPI] Mapping Data... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/reversi/engines.py
[AutoAPI] Mapping Data... [ 93%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/reversi/state_manager.py
[AutoAPI] Mapping Data... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/reversi/config.py
[AutoAPI] Mapping Data... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/reversi/models.py
[AutoAPI] Mapping Data... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/reversi/configurable_config.py
[AutoAPI] Mapping Data... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/reversi/**init**.py
[AutoAPI] Mapping Data... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/reversi/generic_engines.py
[AutoAPI] Mapping Data... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/reversi/agent.py
[AutoAPI] Mapping Data... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/board/**init**.py
[AutoAPI] Mapping Data... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/risk/state.py
[AutoAPI] Mapping Data... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/risk/engines.py
[AutoAPI] Mapping Data... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/risk/state_manager.py
[AutoAPI] Mapping Data... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/risk/config.py
[AutoAPI] Mapping Data... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/risk/models.py
[AutoAPI] Mapping Data... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/risk/configurable_config.py
[AutoAPI] Mapping Data... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/risk/**init**.py
[AutoAPI] Mapping Data... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/risk/generic_engines.py
[AutoAPI] Mapping Data... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/risk/agent.py
[AutoAPI] Mapping Data... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/state_manager.py
[AutoAPI] Mapping Data... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/base.py
[AutoAPI] Mapping Data... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/config.py
[AutoAPI] Mapping Data... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/**init**.py
[AutoAPI] Mapping Data... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/agent.py
[AutoAPI] Mapping Data... [ 94%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/rubiks/state.py
[AutoAPI] Mapping Data... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/rubiks/**init**.py
[AutoAPI] Mapping Data... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/rubiks/agent.py
[AutoAPI] Mapping Data... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/wordle/state.py
[AutoAPI] Mapping Data... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/wordle/engines.py
[AutoAPI] Mapping Data... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/wordle/state_manager.py
[AutoAPI] Mapping Data... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/wordle/config.py
[AutoAPI] Mapping Data... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/wordle/models.py
[AutoAPI] Mapping Data... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/wordle/**init**.py
[AutoAPI] Mapping Data... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/wordle/agent.py
[AutoAPI] Mapping Data... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/flow_free/state.py
[AutoAPI] Mapping Data... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/flow_free/engines.py
[AutoAPI] Mapping Data... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/flow_free/state_manager.py
[AutoAPI] Mapping Data... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/flow_free/base.py
[AutoAPI] Mapping Data... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/flow_free/config.py
[AutoAPI] Mapping Data... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/flow_free/models.py
[AutoAPI] Mapping Data... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/flow_free/**init**.py
[AutoAPI] Mapping Data... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/flow_free/agent.py
[AutoAPI] Mapping Data... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/logic_grid/base.py
[AutoAPI] Mapping Data... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/logic_grid/game/**init**.py
[AutoAPI] Mapping Data... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/sudoku/**init**.py
[AutoAPI] Mapping Data... [ 95%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/sudoku/game/**init**.py
[AutoAPI] Mapping Data... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/sudoku/game/board.py
[AutoAPI] Mapping Data... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/sudoku/game/cell.py
[AutoAPI] Mapping Data... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/sudoku/game/piece.py
[AutoAPI] Mapping Data... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/towers_of_hanoi/base.py
[AutoAPI] Mapping Data... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py
[AutoAPI] Mapping Data... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/towers_of_hanoi/postiition.py
[AutoAPI] Mapping Data... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/towers_of_hanoi/move.py
[AutoAPI] Mapping Data... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/towers_of_hanoi/container.py
[AutoAPI] Mapping Data... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/towers_of_hanoi/position.py
[AutoAPI] Mapping Data... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/towers_of_hanoi/prompts.py
[AutoAPI] Mapping Data... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/towers_of_hanoi/promopts.py
[AutoAPI] Mapping Data... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/towers_of_hanoi/piece.py
[AutoAPI] Mapping Data... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/twenty_fourty_eight/**init**.py
[AutoAPI] Mapping Data... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/twenty_fourty_eight/game.py
[AutoAPI] Mapping Data... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/twenty_fourty_eight/game/**init**.py
[AutoAPI] Mapping Data... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py
[AutoAPI] Mapping Data... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/twenty_fourty_eight/game/piece.py
[AutoAPI] Mapping Data... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/crossword_puzzle/base.py
[AutoAPI] Mapping Data... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py
[AutoAPI] Mapping Data... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/crossword_puzzle/game/cell.py
[AutoAPI] Mapping Data... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/crossword_puzzle/game/piece.py
[AutoAPI] Mapping Data... [ 96%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/word_search/base.py
[AutoAPI] Mapping Data... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/testing/base.py
[AutoAPI] Mapping Data... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/testing/**init**.py
[AutoAPI] Mapping Data... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/mine_sweeper/base.py
[AutoAPI] Mapping Data... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/mine_sweeper/**init**.py
[AutoAPI] Mapping Data... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/state.py
[AutoAPI] Mapping Data... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/engines.py
[AutoAPI] Mapping Data... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/state_manager.py
[AutoAPI] Mapping Data... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/config.py
[AutoAPI] Mapping Data... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/models.py
[AutoAPI] Mapping Data... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/configurable_config.py
[AutoAPI] Mapping Data... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/**init**.py
[AutoAPI] Mapping Data... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/generic_engines.py
[AutoAPI] Mapping Data... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/utils.py
[AutoAPI] Mapping Data... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/agent.py
[AutoAPI] Mapping Data... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/battleship/prompts.py
[AutoAPI] Mapping Data... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/comprehensive_mcp_web.py
[AutoAPI] Mapping Data... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/launcher.py
[AutoAPI] Mapping Data... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/config.py
[AutoAPI] Mapping Data... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mcp_simple_tool_agent.py
[AutoAPI] Mapping Data... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/integrated_launcher.py
[AutoAPI] Mapping Data... [ 97%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/enhanced_parent_self_query_retriever.py
[AutoAPI] Mapping Data... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/simple_faiss_retriever.py
[AutoAPI] Mapping Data... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/**init**.py
[AutoAPI] Mapping Data... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/dynamic_mcp_tool.py
[AutoAPI] Mapping Data... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mcp_rag_agent.py
[AutoAPI] Mapping Data... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/fastmcp_runner.py
[AutoAPI] Mapping Data... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/working_enhanced_retriever.py
[AutoAPI] Mapping Data... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/csv_viewer.py
[AutoAPI] Mapping Data... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/fastapi_mcp_server.py
[AutoAPI] Mapping Data... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/integrated_mcp_system.py
[AutoAPI] Mapping Data... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/dynamic_activation_mcp.py
[AutoAPI] Mapping Data... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/enhance_mcp_data.py
[AutoAPI] Mapping Data... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/simple_rag_mcp_agent.py
[AutoAPI] Mapping Data... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mcp_simple_rag_agent.py
[AutoAPI] Mapping Data... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/production_mcp_tool.py
[AutoAPI] Mapping Data... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/self_query_mcp_agent.py
[AutoAPI] Mapping Data... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/manager.py
[AutoAPI] Mapping Data... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/complete_mcp_with_parent_retriever.py
[AutoAPI] Mapping Data... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/mcp_agent.py
[AutoAPI] Mapping Data... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/transferable_mcp_agent.py
[AutoAPI] Mapping Data... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/**init**.py
[AutoAPI] Mapping Data... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/documentation_agent.py
[AutoAPI] Mapping Data... [ 98%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py
[AutoAPI] Mapping Data... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/cli/**init**.py
[AutoAPI] Mapping Data... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/cli/mcp_manager.py
[AutoAPI] Mapping Data... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/discovery/server_discovery.py
[AutoAPI] Mapping Data... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/discovery/analyzer.py
[AutoAPI] Mapping Data... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/discovery/**init**.py
[AutoAPI] Mapping Data... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/tools/server_selector.py
[AutoAPI] Mapping Data... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/tools/**init**.py
[AutoAPI] Mapping Data... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/tools/server_tester.py
[AutoAPI] Mapping Data... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/tools/ai_assistant.py
[AutoAPI] Mapping Data... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/integration/aug_llm_mcp_extension.py
[AutoAPI] Mapping Data... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mixins/mcp_mixin.py
[AutoAPI] Mapping Data... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mixins/**init**.py
[AutoAPI] Mapping Data... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/servers/http_server.py
[AutoAPI] Mapping Data... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/servers/**init**.py
[AutoAPI] Mapping Data... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/servers/dataflow_mcp_server.py
[AutoAPI] Mapping Data... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/servers/simple_http_server.py
[AutoAPI] Mapping Data... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/servers/dataflow_server.py
[AutoAPI] Mapping Data... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/documentation/doc_loader.py
[AutoAPI] Mapping Data... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/documentation/**init**.py
[AutoAPI] Mapping Data... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/utils/extract_mcp_github_repos.py
[AutoAPI] Mapping Data... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/utils/**init**.py
[AutoAPI] Mapping Data... [ 99%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/installers/advanced_code_installer.py
[AutoAPI] Mapping Data... [100%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/installers/**init**.py
[AutoAPI] Mapping Data... [100%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/installers/safe_pattern_installer.py
[AutoAPI] Mapping Data... [100%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/installers/config_manager.py
[AutoAPI] Mapping Data... [100%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/integration.py
[AutoAPI] Mapping Data... [100%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/config.py
[AutoAPI] Mapping Data... [100%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/github_mass_downloader.py
[AutoAPI] Mapping Data... [100%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/core.py
[AutoAPI] Mapping Data... [100%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/**init**.py
[AutoAPI] Mapping Data... [100%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/discovery.py
[AutoAPI] Mapping Data... [100%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/installers.py
[AutoAPI] Mapping Data... [100%] /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/legacy_core.py

[AutoAPI] Rendering Data... [ 0%] src.haive.mcp
[AutoAPI] Rendering Data... [ 0%] src.haive.core
[AutoAPI] Rendering Data... [ 0%] src.haive.tools
[AutoAPI] Rendering Data... [ 0%] src.haive.games
[AutoAPI] Rendering Data... [ 0%] src.haive.agents
[AutoAPI] Rendering Data... [ 0%] src.haive.mcp.cli
[AutoAPI] Rendering Data... [ 0%] src.haive.dataflow
[AutoAPI] Rendering Data... [ 1%] src.haive.games.go
[AutoAPI] Rendering Data... [ 1%] src.haive.games.api
[AutoAPI] Rendering Data... [ 1%] src.haive.games.nim
[AutoAPI] Rendering Data... [ 1%] src.haive.mcp.tools
[AutoAPI] Rendering Data... [ 1%] src.haive.mcp.utils
[AutoAPI] Rendering Data... [ 1%] src.haive.core.tools
[AutoAPI] Rendering Data... [ 1%] src.haive.core.utils
[AutoAPI] Rendering Data... [ 1%] src.haive.core.types
[AutoAPI] Rendering Data... [ 1%] src.haive.core.graph
[AutoAPI] Rendering Data... [ 1%] src.haive.agents.rag
[AutoAPI] Rendering Data... [ 1%] src.haive.games.clue
[AutoAPI] Rendering Data... [ 1%] src.haive.games.base
[AutoAPI] Rendering Data... [ 1%] src.haive.games.core
[AutoAPI] Rendering Data... [ 1%] src.haive.games.risk
[AutoAPI] Rendering Data... [ 1%] src.haive.mcp.config
[AutoAPI] Rendering Data... [ 2%] src.haive.mcp.agents
[AutoAPI] Rendering Data... [ 2%] src.haive.mcp.mixins
[AutoAPI] Rendering Data... [ 2%] src.haive.core.common
[AutoAPI] Rendering Data... [ 2%] src.haive.core.models
[AutoAPI] Rendering Data... [ 2%] src.haive.core.engine
[AutoAPI] Rendering Data... [ 2%] src.haive.core.config
[AutoAPI] Rendering Data... [ 2%] src.haive.core.schema
[AutoAPI] Rendering Data... [ 2%] src.haive.agents.base
[AutoAPI] Rendering Data... [ 2%] src.haive.tools.tools
[AutoAPI] Rendering Data... [ 2%] src.haive.dataflow.db
[AutoAPI] Rendering Data... [ 2%] src.haive.games.mafia
[AutoAPI] Rendering Data... [ 2%] src.haive.games.chess
[AutoAPI] Rendering Data... [ 2%] src.haive.games.cards
[AutoAPI] Rendering Data... [ 2%] src.haive.games.utils
[AutoAPI] Rendering Data... [ 2%] src.haive.games.poker
[AutoAPI] Rendering Data... [ 3%] src.haive.games.board
[AutoAPI] Rendering Data... [ 3%] src.haive.mcp.manager
[AutoAPI] Rendering Data... [ 3%] src.haive.mcp.servers
[AutoAPI] Rendering Data... [ 3%] src.haive.core.runtime
[AutoAPI] Rendering Data... [ 3%] src.haive.agents.chain
[AutoAPI] Rendering Data... [ 3%] src.haive.agents.react
[AutoAPI] Rendering Data... [ 3%] src.haive.agents.utils
[AutoAPI] Rendering Data... [ 3%] src.haive.agents.multi
[AutoAPI] Rendering Data... [ 3%] src.haive.dataflow.mcp
[AutoAPI] Rendering Data... [ 3%] src.haive.games.nim.ui
[AutoAPI] Rendering Data... [ 3%] src.haive.games.debate
[AutoAPI] Rendering Data... [ 3%] src.haive.mcp.launcher
[AutoAPI] Rendering Data... [ 3%] src.haive.core.registry
[AutoAPI] Rendering Data... [ 3%] src.haive.agents.simple
[AutoAPI] Rendering Data... [ 3%] src.haive.agents.memory
[AutoAPI] Rendering Data... [ 4%] src.haive.dataflow.core
[AutoAPI] Rendering Data... [ 4%] src.haive.dataflow.llms
[AutoAPI] Rendering Data... [ 4%] src.haive.dataflow.auth
[AutoAPI] Rendering Data... [ 4%] src.haive.games.clue.ui
[AutoAPI] Rendering Data... [ 4%] src.haive.games.hold_em
[AutoAPI] Rendering Data... [ 4%] src.haive.games.mancala
[AutoAPI] Rendering Data... [ 4%] src.haive.games.base_v2
[AutoAPI] Rendering Data... [ 4%] src.haive.games.reversi
[AutoAPI] Rendering Data... [ 4%] src.haive.mcp.discovery
[AutoAPI] Rendering Data... [ 4%] src.haive.core.schema.ui
[AutoAPI] Rendering Data... [ 4%] src.haive.dataflow.utils
[AutoAPI] Rendering Data... [ 4%] src.haive.games.checkers
[AutoAPI] Rendering Data... [ 4%] src.haive.games.dominoes
[AutoAPI] Rendering Data... [ 4%] src.haive.games.monopoly
[AutoAPI] Rendering Data... [ 4%] src.haive.games.connect4
[AutoAPI] Rendering Data... [ 5%] src.haive.games.among_us
[AutoAPI] Rendering Data... [ 5%] src.haive.games.chess.ui
[AutoAPI] Rendering Data... [ 5%] src.haive.games.go.state
[AutoAPI] Rendering Data... [ 5%] src.haive.games.go.agent
[AutoAPI] Rendering Data... [ 5%] src.haive.mcp.csv_viewer
[AutoAPI] Rendering Data... [ 5%] src.haive.mcp.installers
[AutoAPI] Rendering Data... [ 5%] src.haive.mcp.downloader
[AutoAPI] Rendering Data... [ 5%] src.haive.core.models.llm
[AutoAPI] Rendering Data... [ 5%] src.haive.core.graph.node
[AutoAPI] Rendering Data... [ 5%] src.haive.agents.research
[AutoAPI] Rendering Data... [ 5%] src.haive.agents.planning
[AutoAPI] Rendering Data... [ 5%] src.haive.agents.rag.base
[AutoAPI] Rendering Data... [ 5%] src.haive.agents.rag.hyde
[AutoAPI] Rendering Data... [ 5%] src.haive.agents.patterns
[AutoAPI] Rendering Data... [ 5%] src.haive.dataflow.models
[AutoAPI] Rendering Data... [ 6%] src.haive.dataflow.config
[AutoAPI] Rendering Data... [ 6%] src.haive.games.benchmark
[AutoAPI] Rendering Data... [ 6%] src.haive.games.api.setup
[AutoAPI] Rendering Data... [ 6%] src.haive.games.nim.agent
[AutoAPI] Rendering Data... [ 6%] src.haive.games.framework
[AutoAPI] Rendering Data... [ 6%] src.haive.games.debate_v2
[AutoAPI] Rendering Data... [ 6%] src.haive.games.cards.uno
[AutoAPI] Rendering Data... [ 6%] src.haive.games.core.game
[AutoAPI] Rendering Data... [ 6%] src.haive.games.core.move
[AutoAPI] Rendering Data... [ 6%] src.haive.games.go.config
[AutoAPI] Rendering Data... [ 6%] src.haive.games.go.models
[AutoAPI] Rendering Data... [ 6%] src.haive.core.persistence
[AutoAPI] Rendering Data... [ 6%] src.haive.core.engine.base
[AutoAPI] Rendering Data... [ 6%] src.haive.core.engine.tool
[AutoAPI] Rendering Data... [ 6%] src.haive.agents.discovery
[AutoAPI] Rendering Data... [ 7%] src.haive.agents.simple.v2
[AutoAPI] Rendering Data... [ 7%] src.haive.agents.ltm.agent
[AutoAPI] Rendering Data... [ 7%] src.haive.agents.rag.flare
[AutoAPI] Rendering Data... [ 7%] src.haive.agents.memory_v2
[AutoAPI] Rendering Data... [ 7%] src.haive.games.clue.state
[AutoAPI] Rendering Data... [ 7%] src.haive.games.clue.agent
[AutoAPI] Rendering Data... [ 7%] src.haive.games.mastermind
[AutoAPI] Rendering Data... [ 7%] src.haive.games.base.state
[AutoAPI] Rendering Data... [ 7%] src.haive.games.base.utils
[AutoAPI] Rendering Data... [ 7%] src.haive.games.base.agent
[AutoAPI] Rendering Data... [ 7%] src.haive.games.hold_em.ui
[AutoAPI] Rendering Data... [ 7%] src.haive.games.nim.config
[AutoAPI] Rendering Data... [ 7%] src.haive.games.nim.models
[AutoAPI] Rendering Data... [ 7%] src.haive.games.core.agent
[AutoAPI] Rendering Data... [ 7%] src.haive.games.core.board
[AutoAPI] Rendering Data... [ 8%] src.haive.games.go.engines
[AutoAPI] Rendering Data... [ 8%] src.haive.games.risk.state
[AutoAPI] Rendering Data... [ 8%] src.haive.games.risk.agent
[AutoAPI] Rendering Data... [ 8%] src.haive.games.battleship
[AutoAPI] Rendering Data... [ 8%] src.haive.core.common.types
[AutoAPI] Rendering Data... [ 8%] src.haive.core.engine.agent
[AutoAPI] Rendering Data... [ 8%] src.haive.core.schema.utils
[AutoAPI] Rendering Data... [ 8%] src.haive.core.schema.state
[AutoAPI] Rendering Data... [ 8%] src.haive.core.graph.common
[AutoAPI] Rendering Data... [ 8%] src.haive.agents.reflection
[AutoAPI] Rendering Data... [ 8%] src.haive.agents.base.hooks
[AutoAPI] Rendering Data... [ 8%] src.haive.agents.base.agent
[AutoAPI] Rendering Data... [ 8%] src.haive.agents.base.types
[AutoAPI] Rendering Data... [ 8%] src.haive.agents.supervisor
[AutoAPI] Rendering Data... [ 8%] src.haive.agents.sequential
[AutoAPI] Rendering Data... [ 9%] src.haive.agents.rag.models
[AutoAPI] Rendering Data... [ 9%] src.haive.agents.rag.fusion
[AutoAPI] Rendering Data... [ 9%] src.haive.agents.rag.simple
[AutoAPI] Rendering Data... [ 9%] src.haive.agents.rag.db_rag
[AutoAPI] Rendering Data... [ 9%] src.haive.agents.structured
[AutoAPI] Rendering Data... [ 9%] src.haive.agents.multi.base
[AutoAPI] Rendering Data... [ 9%] src.haive.tools.tools.arxiv
[AutoAPI] Rendering Data... [ 9%] src.haive.dataflow.registry
[AutoAPI] Rendering Data... [ 9%] src.haive.dataflow.llms.api
[AutoAPI] Rendering Data... [ 9%] src.haive.dataflow.fetchers
[AutoAPI] Rendering Data... [ 9%] src.haive.dataflow.api.llms
[AutoAPI] Rendering Data... [ 9%] src.haive.games.clue.config
[AutoAPI] Rendering Data... [ 9%] src.haive.games.clue.models
[AutoAPI] Rendering Data... [ 9%] src.haive.games.clue.runner
[AutoAPI] Rendering Data... [ 9%] src.haive.games.checkers.ui
[AutoAPI] Rendering Data... [ 10%] src.haive.games.mafia.state
[AutoAPI] Rendering Data... [ 10%] src.haive.games.mafia.agent
[AutoAPI] Rendering Data... [ 10%] src.haive.games.dominoes.ui
[AutoAPI] Rendering Data... [ 10%] src.haive.games.base.config
[AutoAPI] Rendering Data... [ 10%] src.haive.games.base.models
[AutoAPI] Rendering Data... [ 10%] src.haive.games.monopoly.ui
[AutoAPI] Rendering Data... [ 10%] src.haive.games.nim.engines
[AutoAPI] Rendering Data... [ 10%] src.haive.games.tic_tac_toe
[AutoAPI] Rendering Data... [ 10%] src.haive.games.connect4.ui
[AutoAPI] Rendering Data... [ 10%] src.haive.games.chess.state
[AutoAPI] Rendering Data... [ 10%] src.haive.games.chess.utils
[AutoAPI] Rendering Data... [ 10%] src.haive.games.chess.agent
[AutoAPI] Rendering Data... [ 10%] src.haive.games.core.config
[AutoAPI] Rendering Data... [ 10%] src.haive.games.poker.state
[AutoAPI] Rendering Data... [ 10%] src.haive.games.poker.agent
[AutoAPI] Rendering Data... [ 10%] src.haive.games.risk.config
[AutoAPI] Rendering Data... [ 11%] src.haive.games.risk.models
[AutoAPI] Rendering Data... [ 11%] src.haive.mcp.mcp_rag_agent
[AutoAPI] Rendering Data... [ 11%] src.haive.mcp.documentation
[AutoAPI] Rendering Data... [ 11%] src.haive.core.common.models
[AutoAPI] Rendering Data... [ 11%] src.haive.core.common.mixins
[AutoAPI] Rendering Data... [ 11%] src.haive.core.types.general
[AutoAPI] Rendering Data... [ 11%] src.haive.core.schema.mixins
[AutoAPI] Rendering Data... [ 11%] src.haive.agents.base.mixins
[AutoAPI] Rendering Data... [ 11%] src.haive.agents.rag.agentic
[AutoAPI] Rendering Data... [ 11%] src.haive.agents.rag.llm_rag
[AutoAPI] Rendering Data... [ 11%] src.haive.agents.react_class
[AutoAPI] Rendering Data... [ 11%] src.haive.agents.multi.clean
[AutoAPI] Rendering Data... [ 11%] src.haive.agents.memory.core
[AutoAPI] Rendering Data... [ 11%] src.haive.agents.wiki_writer
[AutoAPI] Rendering Data... [ 11%] src.haive.agents.experiments
[AutoAPI] Rendering Data... [ 12%] src.haive.tools.tools.pubmed
[AutoAPI] Rendering Data... [ 12%] src.haive.tools.tools.google
[AutoAPI] Rendering Data... [ 12%] src.haive.dataflow.discovery
[AutoAPI] Rendering Data... [ 12%] src.haive.dataflow.providers
[AutoAPI] Rendering Data... [ 12%] src.haive.dataflow.importers
[AutoAPI] Rendering Data... [ 12%] src.haive.dataflow.db.schema
[AutoAPI] Rendering Data... [ 12%] src.haive.games.clue.engines
[AutoAPI] Rendering Data... [ 12%] src.haive.games.mafia.config
[AutoAPI] Rendering Data... [ 12%] src.haive.games.mafia.models
[AutoAPI] Rendering Data... [ 12%] src.haive.games.base.factory
[AutoAPI] Rendering Data... [ 12%] src.haive.games.multi_player
[AutoAPI] Rendering Data... [ 12%] src.haive.games.chess.config
[AutoAPI] Rendering Data... [ 12%] src.haive.games.chess.models
[AutoAPI] Rendering Data... [ 12%] src.haive.games.cards.models
[AutoAPI] Rendering Data... [ 12%] src.haive.games.poker.config
[AutoAPI] Rendering Data... [ 13%] src.haive.games.poker.models
[AutoAPI] Rendering Data... [ 13%] src.haive.games.debate.agent
[AutoAPI] Rendering Data... [ 13%] src.haive.games.go.go_engine
[AutoAPI] Rendering Data... [ 13%] src.haive.games.risk.engines
[AutoAPI] Rendering Data... [ 13%] src.haive.mcp.fastmcp_runner
[AutoAPI] Rendering Data... [ 13%] src.haive.core.engine.aug_llm
[AutoAPI] Rendering Data... [ 13%] src.haive.core.graph.branches
[AutoAPI] Rendering Data... [ 13%] src.haive.agents.rag.filtered
[AutoAPI] Rendering Data... [ 13%] src.haive.agents.archive.meta
[AutoAPI] Rendering Data... [ 13%] src.haive.agents.conversation
[AutoAPI] Rendering Data... [ 13%] src.haive.dataflow.api.routes
[AutoAPI] Rendering Data... [ 13%] src.haive.dataflow.mcp.health
[AutoAPI] Rendering Data... [ 13%] src.haive.dataflow.mcp.client
[AutoAPI] Rendering Data... [ 13%] src.haive.dataflow.registries
[AutoAPI] Rendering Data... [ 13%] src.haive.games.mastermind.ui
[AutoAPI] Rendering Data... [ 14%] src.haive.games.mafia.engines
[AutoAPI] Rendering Data... [ 14%] src.haive.games.monopoly.game
[AutoAPI] Rendering Data... [ 14%] src.haive.games.hold_em.state
[AutoAPI] Rendering Data... [ 14%] src.haive.games.hold_em.utils
[AutoAPI] Rendering Data... [ 14%] src.haive.games.hold_em.agent
[AutoAPI] Rendering Data... [ 14%] src.haive.games.mancala.state
[AutoAPI] Rendering Data... [ 14%] src.haive.games.mancala.agent
[AutoAPI] Rendering Data... [ 14%] src.haive.games.chess.engines
[AutoAPI] Rendering Data... [ 14%] src.haive.games.core.position
[AutoAPI] Rendering Data... [ 14%] src.haive.games.poker.engines
[AutoAPI] Rendering Data... [ 14%] src.haive.games.poker.prompts
[AutoAPI] Rendering Data... [ 14%] src.haive.games.debate.config
[AutoAPI] Rendering Data... [ 14%] src.haive.games.debate.models
[AutoAPI] Rendering Data... [ 14%] src.haive.games.fox_and_geese
[AutoAPI] Rendering Data... [ 14%] src.haive.games.reversi.state
[AutoAPI] Rendering Data... [ 15%] src.haive.games.single_player
[AutoAPI] Rendering Data... [ 15%] src.haive.mcp.cli.mcp_manager
[AutoAPI] Rendering Data... [ 15%] src.haive.mcp.downloader.core
[AutoAPI] Rendering Data... [ 15%] src.haive.core.models.metadata
[AutoAPI] Rendering Data... [ 15%] src.haive.core.models.llm.base
[AutoAPI] Rendering Data... [ 15%] src.haive.core.utils.tool_list
[AutoAPI] Rendering Data... [ 15%] src.haive.core.engine.document
[AutoAPI] Rendering Data... [ 15%] src.haive.core.config.runnable
[AutoAPI] Rendering Data... [ 15%] src.haive.core.schema.composer
[AutoAPI] Rendering Data... [ 15%] src.haive.core.schema.prebuilt
[AutoAPI] Rendering Data... [ 15%] src.haive.agents.common.models
[AutoAPI] Rendering Data... [ 15%] src.haive.agents.task_analysis
[AutoAPI] Rendering Data... [ 15%] src.haive.agents.simple.config
[AutoAPI] Rendering Data... [ 15%] src.haive.agents.rag.self_rag2
[AutoAPI] Rendering Data... [ 15%] src.haive.agents.rag.step_back
[AutoAPI] Rendering Data... [ 16%] src.haive.agents.rag.self_corr
[AutoAPI] Rendering Data... [ 16%] src.haive.agents.memory.models
[AutoAPI] Rendering Data... [ 16%] src.haive.agents.memory.search
[AutoAPI] Rendering Data... [ 16%] src.haive.tools.tools.toolkits
[AutoAPI] Rendering Data... [ 16%] src.haive.dataflow.llms.models
[AutoAPI] Rendering Data... [ 16%] src.haive.dataflow.persistence
[AutoAPI] Rendering Data... [ 16%] src.haive.dataflow.registry.db
[AutoAPI] Rendering Data... [ 16%] src.haive.dataflow.db.supabase
[AutoAPI] Rendering Data... [ 16%] src.haive.games.checkers.state
[AutoAPI] Rendering Data... [ 16%] src.haive.games.checkers.agent
[AutoAPI] Rendering Data... [ 16%] src.haive.games.dominoes.state
[AutoAPI] Rendering Data... [ 16%] src.haive.games.monopoly.state
[AutoAPI] Rendering Data... [ 16%] src.haive.games.monopoly.utils
[AutoAPI] Rendering Data... [ 16%] src.haive.games.monopoly.agent
[AutoAPI] Rendering Data... [ 16%] src.haive.games.hold_em.config
[AutoAPI] Rendering Data... [ 17%] src.haive.games.hold_em.models
[AutoAPI] Rendering Data... [ 17%] src.haive.games.framework.base
[AutoAPI] Rendering Data... [ 17%] src.haive.games.framework.core
[AutoAPI] Rendering Data... [ 17%] src.haive.games.tic_tac_toe.ui
[AutoAPI] Rendering Data... [ 17%] src.haive.games.mancala.config
[AutoAPI] Rendering Data... [ 17%] src.haive.games.mancala.models
[AutoAPI] Rendering Data... [ 17%] src.haive.games.connect4.state
[AutoAPI] Rendering Data... [ 17%] src.haive.games.connect4.agent
[AutoAPI] Rendering Data... [ 17%] src.haive.games.among_us.state
[AutoAPI] Rendering Data... [ 17%] src.haive.games.reversi.config
[AutoAPI] Rendering Data... [ 17%] src.haive.games.reversi.models
[AutoAPI] Rendering Data... [ 17%] src.haive.mcp.dynamic_mcp_tool
[AutoAPI] Rendering Data... [ 17%] src.haive.mcp.enhance_mcp_data
[AutoAPI] Rendering Data... [ 17%] src.haive.mcp.agents.mcp_agent
[AutoAPI] Rendering Data... [ 17%] src.haive.mcp.mixins.mcp_mixin
[AutoAPI] Rendering Data... [ 18%] src.haive.core.persistence.base
[AutoAPI] Rendering Data... [ 18%] src.haive.core.models.retriever
[AutoAPI] Rendering Data... [ 18%] src.haive.core.engine.base.base
[AutoAPI] Rendering Data... [ 18%] src.haive.core.engine.retriever
[AutoAPI] Rendering Data... [ 18%] src.haive.core.engine.embedding
[AutoAPI] Rendering Data... [ 18%] src.haive.core.config.constants
[AutoAPI] Rendering Data... [ 18%] src.haive.core.graph.node.utils
[AutoAPI] Rendering Data... [ 18%] src.haive.core.graph.node.types
[AutoAPI] Rendering Data... [ 18%] src.haive.agents.research.storm
[AutoAPI] Rendering Data... [ 18%] src.haive.agents.document.agent
[AutoAPI] Rendering Data... [ 18%] src.haive.agents.planning.rewoo
[AutoAPI] Rendering Data... [ 18%] src.haive.agents.simple.factory
[AutoAPI] Rendering Data... [ 18%] src.haive.agents.rag.hyde.agent
[AutoAPI] Rendering Data... [ 18%] src.haive.agents.rag.self_route
[AutoAPI] Rendering Data... [ 18%] src.haive.agents.rag.corrective
[AutoAPI] Rendering Data... [ 19%] src.haive.agents.react.agent_v3
[AutoAPI] Rendering Data... [ 19%] src.haive.dataflow.api.game_api
[AutoAPI] Rendering Data... [ 19%] src.haive.dataflow.api.llms.api
[AutoAPI] Rendering Data... [ 19%] src.haive.games.clue.controller
[AutoAPI] Rendering Data... [ 19%] src.haive.games.checkers.config
[AutoAPI] Rendering Data... [ 19%] src.haive.games.checkers.models
[AutoAPI] Rendering Data... [ 19%] src.haive.games.dominoes.models
[AutoAPI] Rendering Data... [ 19%] src.haive.games.monopoly.config
[AutoAPI] Rendering Data... [ 19%] src.haive.games.monopoly.models
[AutoAPI] Rendering Data... [ 19%] src.haive.games.hold_em.engines
[AutoAPI] Rendering Data... [ 19%] src.haive.games.api.general_api
[AutoAPI] Rendering Data... [ 19%] src.haive.games.mancala.engines
[AutoAPI] Rendering Data... [ 19%] src.haive.games.debate_v2.agent
[AutoAPI] Rendering Data... [ 19%] src.haive.games.connect4.config
[AutoAPI] Rendering Data... [ 19%] src.haive.games.connect4.models
[AutoAPI] Rendering Data... [ 20%] src.haive.games.among_us.models
[AutoAPI] Rendering Data... [ 20%] src.haive.games.chess.llm_utils
[AutoAPI] Rendering Data... [ 20%] src.haive.games.core.components
[AutoAPI] Rendering Data... [ 20%] src.haive.mcp.downloader.config
[AutoAPI] Rendering Data... [ 20%] src.haive.core.persistence.utils
[AutoAPI] Rendering Data... [ 20%] src.haive.core.persistence.types
[AutoAPI] Rendering Data... [ 20%] src.haive.core.persistence.store
[AutoAPI] Rendering Data... [ 20%] src.haive.core.models.embeddings
[AutoAPI] Rendering Data... [ 20%] src.haive.core.tools.store_tools
[AutoAPI] Rendering Data... [ 20%] src.haive.core.utils.collections
[AutoAPI] Rendering Data... [ 20%] src.haive.core.engine.base.types
[AutoAPI] Rendering Data... [ 20%] src.haive.core.graph.state_graph
[AutoAPI] Rendering Data... [ 20%] src.haive.agents.research.person
[AutoAPI] Rendering Data... [ 20%] src.haive.agents.planning.models
[AutoAPI] Rendering Data... [ 20%] src.haive.agents.simple.agent_v2
[AutoAPI] Rendering Data... [ 21%] src.haive.agents.simple.agent_v3
[AutoAPI] Rendering Data... [ 21%] src.haive.agents.rag.flare.agent
[AutoAPI] Rendering Data... [ 21%] src.haive.agents.rag.db_rag.base
[AutoAPI] Rendering Data... [ 21%] src.haive.agents.rag.speculative
[AutoAPI] Rendering Data... [ 21%] src.haive.agents.document_loader
[AutoAPI] Rendering Data... [ 21%] src.haive.tools.tools.agify_tool
[AutoAPI] Rendering Data... [ 21%] src.haive.tools.tools.ionic_tool
[AutoAPI] Rendering Data... [ 21%] src.haive.dataflow.serialization
[AutoAPI] Rendering Data... [ 21%] src.haive.dataflow.**init\_**lazy
[AutoAPI] Rendering Data... [ 21%] src.haive.dataflow.registry.base
[AutoAPI] Rendering Data... [ 21%] src.haive.dataflow.registry.core
[AutoAPI] Rendering Data... [ 21%] src.haive.dataflow.mcp.discovery
[AutoAPI] Rendering Data... [ 21%] src.haive.dataflow.importers.tak
[AutoAPI] Rendering Data... [ 21%] src.haive.dataflow.utils.logging
[AutoAPI] Rendering Data... [ 21%] src.haive.dataflow.conversations
[AutoAPI] Rendering Data... [ 22%] src.haive.games.checkers.engines
[AutoAPI] Rendering Data... [ 22%] src.haive.games.dominoes.rich_ui
[AutoAPI] Rendering Data... [ 22%] src.haive.games.monopoly.engines
[AutoAPI] Rendering Data... [ 22%] src.haive.games.debate_v2.judges
[AutoAPI] Rendering Data... [ 22%] src.haive.games.core.config.base
[AutoAPI] Rendering Data... [ 22%] src.haive.games.fox_and_geese.ui
[AutoAPI] Rendering Data... [ 22%] src.haive.games.go.state_manager
[AutoAPI] Rendering Data... [ 22%] src.haive.games.battleship.state
[AutoAPI] Rendering Data... [ 22%] src.haive.games.battleship.utils
[AutoAPI] Rendering Data... [ 22%] src.haive.games.battleship.agent
[AutoAPI] Rendering Data... [ 22%] src.haive.mcp.fastapi_mcp_server
[AutoAPI] Rendering Data... [ 22%] src.haive.mcp.discovery.analyzer
[AutoAPI] Rendering Data... [ 22%] src.haive.mcp.tools.ai_assistant
[AutoAPI] Rendering Data... [ 22%] src.haive.core.persistence.memory
[AutoAPI] Rendering Data... [ 22%] src.haive.core.models.llm.factory
[AutoAPI] Rendering Data... [ 23%] src.haive.core.models.vectorstore
[AutoAPI] Rendering Data... [ 23%] src.haive.core.utils.getter_mixin
[AutoAPI] Rendering Data... [ 23%] src.haive.core.engine.vectorstore
[AutoAPI] Rendering Data... [ 23%] src.haive.core.engine.agent.agent
[AutoAPI] Rendering Data... [ 23%] src.haive.core.schema.field_utils
[AutoAPI] Rendering Data... [ 23%] src.haive.core.graph.tool_manager
[AutoAPI] Rendering Data... [ 23%] src.haive.agents.reflection.state
[AutoAPI] Rendering Data... [ 23%] src.haive.agents.reflection.agent
[AutoAPI] Rendering Data... [ 23%] src.haive.agents.base.typed_agent
[AutoAPI] Rendering Data... [ 23%] src.haive.agents.supervisor.agent
[AutoAPI] Rendering Data... [ 23%] src.haive.agents.planning.p_and_e
[AutoAPI] Rendering Data... [ 23%] src.haive.agents.simple.v2.config
[AutoAPI] Rendering Data... [ 23%] src.haive.agents.rag.answer_agent
[AutoAPI] Rendering Data... [ 23%] src.haive.agents.rag.fusion.agent
[AutoAPI] Rendering Data... [ 23%] src.haive.agents.rag.adaptive_rag
[AutoAPI] Rendering Data... [ 24%] src.haive.agents.rag.memory_aware
[AutoAPI] Rendering Data... [ 24%] src.haive.agents.rag.simple.agent
[AutoAPI] Rendering Data... [ 24%] src.haive.agents.long_term_memory
[AutoAPI] Rendering Data... [ 24%] src.haive.agents.structured.agent
[AutoAPI] Rendering Data... [ 24%] src.haive.agents.multi.sequential
[AutoAPI] Rendering Data... [ 24%] src.haive.tools.tools.eleven_labs
[AutoAPI] Rendering Data... [ 24%] src.haive.tools.tools.hinge_tools
[AutoAPI] Rendering Data... [ 24%] src.haive.tools.tools.openaq_tool
[AutoAPI] Rendering Data... [ 24%] src.haive.tools.tools.apify_tools
[AutoAPI] Rendering Data... [ 24%] src.haive.dataflow.api.middleware
[AutoAPI] Rendering Data... [ 24%] src.haive.dataflow.api.run_simple
[AutoAPI] Rendering Data... [ 24%] src.haive.dataflow.registry.utils
[AutoAPI] Rendering Data... [ 24%] src.haive.dataflow.providers.base
[AutoAPI] Rendering Data... [ 24%] src.haive.games.mastermind.config
[AutoAPI] Rendering Data... [ 24%] src.haive.games.mastermind.models
[AutoAPI] Rendering Data... [ 25%] src.haive.games.mafia.mock_runner
[AutoAPI] Rendering Data... [ 25%] src.haive.games.monopoly.run_game
[AutoAPI] Rendering Data... [ 25%] src.haive.games.monopoly.ui_fixed
[AutoAPI] Rendering Data... [ 25%] src.haive.games.nim.state_manager
[AutoAPI] Rendering Data... [ 25%] src.haive.games.tic_tac_toe.state
[AutoAPI] Rendering Data... [ 25%] src.haive.games.tic_tac_toe.agent
[AutoAPI] Rendering Data... [ 25%] src.haive.games.cards.models.card
[AutoAPI] Rendering Data... [ 25%] src.haive.games.cards.standard.bs
[AutoAPI] Rendering Data... [ 25%] src.haive.games.battleship.models
[AutoAPI] Rendering Data... [ 25%] src.haive.mcp.integrated_launcher
[AutoAPI] Rendering Data... [ 25%] src.haive.mcp.production_mcp_tool
[AutoAPI] Rendering Data... [ 25%] src.haive.mcp.servers.http_server
[AutoAPI] Rendering Data... [ 25%] src.haive.core.tools.store_manager
[AutoAPI] Rendering Data... [ 25%] src.haive.core.utils.mermaid_utils
[AutoAPI] Rendering Data... [ 25%] src.haive.core.engine.base.factory
[AutoAPI] Rendering Data... [ 26%] src.haive.core.engine.agent.config
[AutoAPI] Rendering Data... [ 26%] src.haive.core.schema.state_schema
[AutoAPI] Rendering Data... [ 26%] src.haive.core.graph.node.registry
[AutoAPI] Rendering Data... [ 26%] src.haive.core.graph.node.composer
[AutoAPI] Rendering Data... [ 26%] src.haive.agents.reflection.models
[AutoAPI] Rendering Data... [ 26%] src.haive.agents.structured_output
[AutoAPI] Rendering Data... [ 26%] src.haive.agents.sequential.config
[AutoAPI] Rendering Data... [ 26%] src.haive.agents.planning.rewoo_v3
[AutoAPI] Rendering Data... [ 26%] src.haive.agents.simple.structured
[AutoAPI] Rendering Data... [ 26%] src.haive.agents.rag.modular_chain
[AutoAPI] Rendering Data... [ 26%] src.haive.agents.rag.hyde.agent_v2
[AutoAPI] Rendering Data... [ 26%] src.haive.agents.rag.agentic.agent
[AutoAPI] Rendering Data... [ 26%] src.haive.agents.structured.models
[AutoAPI] Rendering Data... [ 26%] src.haive.agents.memory.core.types
[AutoAPI] Rendering Data... [ 26%] src.haive.agents.conversation.base
[AutoAPI] Rendering Data... [ 27%] src.haive.agents.self_healing_code
[AutoAPI] Rendering Data... [ 27%] src.haive.tools.tools.search_tools
[AutoAPI] Rendering Data... [ 27%] src.haive.tools.tools.asknews_tool
[AutoAPI] Rendering Data... [ 27%] src.haive.tools.tools.brave_search
[AutoAPI] Rendering Data... [ 27%] src.haive.tools.tools.toolkits.dev
[AutoAPI] Rendering Data... [ 27%] src.haive.dataflow.api.game_socket
[AutoAPI] Rendering Data... [ 27%] src.haive.dataflow.api.game_router
[AutoAPI] Rendering Data... [ 27%] src.haive.dataflow.registry.models
[AutoAPI] Rendering Data... [ 27%] src.haive.dataflow.config.settings
[AutoAPI] Rendering Data... [ 27%] src.haive.games.llm_config_factory
[AutoAPI] Rendering Data... [ 27%] src.haive.games.clue.state_manager
[AutoAPI] Rendering Data... [ 27%] src.haive.games.mastermind.engines
[AutoAPI] Rendering Data... [ 27%] src.haive.games.base.state_manager
[AutoAPI] Rendering Data... [ 27%] src.haive.games.monopoly.game.game
[AutoAPI] Rendering Data... [ 27%] src.haive.games.hold_em.game_agent
[AutoAPI] Rendering Data... [ 28%] src.haive.games.multi_player.state
[AutoAPI] Rendering Data... [ 28%] src.haive.games.multi_player.agent
[AutoAPI] Rendering Data... [ 28%] src.haive.games.tic_tac_toe.config
[AutoAPI] Rendering Data... [ 28%] src.haive.games.tic_tac_toe.models
[AutoAPI] Rendering Data... [ 28%] src.haive.games.risk.state_manager
[AutoAPI] Rendering Data... [ 28%] src.haive.games.single_player.base
[AutoAPI] Rendering Data... [ 28%] src.haive.games.battleship.engines
[AutoAPI] Rendering Data... [ 28%] src.haive.games.battleship.prompts
[AutoAPI] Rendering Data... [ 28%] src.haive.mcp.simple_rag_mcp_agent
[AutoAPI] Rendering Data... [ 28%] src.haive.mcp.mcp_simple_rag_agent
[AutoAPI] Rendering Data... [ 28%] src.haive.mcp.self_query_mcp_agent
[AutoAPI] Rendering Data... [ 28%] src.haive.mcp.downloader.discovery
[AutoAPI] Rendering Data... [ 28%] src.haive.core.common.mixins.mixins
[AutoAPI] Rendering Data... [ 28%] src.haive.core.persistence.handlers
[AutoAPI] Rendering Data... [ 28%] src.haive.core.models.llm.providers
[AutoAPI] Rendering Data... [ 29%] src.haive.core.engine.aug_llm.utils
[AutoAPI] Rendering Data... [ 29%] src.haive.core.engine.base.registry
[AutoAPI] Rendering Data... [ 29%] src.haive.core.engine.agent.pattern
[AutoAPI] Rendering Data... [ 29%] src.haive.core.engine.output_parser
[AutoAPI] Rendering Data... [ 29%] src.haive.core.config.auth_runnable
[AutoAPI] Rendering Data... [ 29%] src.haive.core.schema.compatibility
[AutoAPI] Rendering Data... [ 29%] src.haive.core.graph.branches.utils
[AutoAPI] Rendering Data... [ 29%] src.haive.core.graph.branches.types
[AutoAPI] Rendering Data... [ 29%] src.haive.agents.reflection.prompts
[AutoAPI] Rendering Data... [ 29%] src.haive.agents.base.enhanced_init
[AutoAPI] Rendering Data... [ 29%] src.haive.agents.task_analysis.base
[AutoAPI] Rendering Data... [ 29%] src.haive.agents.task_analysis.tree
[AutoAPI] Rendering Data... [ 29%] src.haive.agents.supervisor.routing
[AutoAPI] Rendering Data... [ 29%] src.haive.agents.ltm.memory_schemas
[AutoAPI] Rendering Data... [ 29%] src.haive.agents.rag.branched_chain
[AutoAPI] Rendering Data... [ 30%] src.haive.agents.rag.agentic_router
[AutoAPI] Rendering Data... [ 30%] src.haive.agents.rag.multi_strategy
[AutoAPI] Rendering Data... [ 30%] src.haive.agents.rag.adaptive.agent
[AutoAPI] Rendering Data... [ 30%] src.haive.agents.rag.adaptive_tools
[AutoAPI] Rendering Data... [ 30%] src.haive.agents.rag.db_rag.sql_rag
[AutoAPI] Rendering Data... [ 30%] src.haive.agents.rag.query_planning
[AutoAPI] Rendering Data... [ 30%] src.haive.agents.dynamic_supervisor
[AutoAPI] Rendering Data... [ 30%] src.haive.agents.structured.prompts
[AutoAPI] Rendering Data... [ 30%] src.haive.agents.document_modifiers
[AutoAPI] Rendering Data... [ 30%] src.haive.agents.multi.archive.base
[AutoAPI] Rendering Data... [ 30%] src.haive.agents.memory.core.stores
[AutoAPI] Rendering Data... [ 30%] src.haive.agents.memory.search.base
[AutoAPI] Rendering Data... [ 30%] src.haive.agents.memory.search.labs
[AutoAPI] Rendering Data... [ 30%] src.haive.tools.tools.pokebase_tool
[AutoAPI] Rendering Data... [ 30%] src.haive.tools.tools.yfinance_tool
[AutoAPI] Rendering Data... [ 30%] src.haive.tools.tools.discord_tools
[AutoAPI] Rendering Data... [ 31%] src.haive.tools.tools.reddit_search
[AutoAPI] Rendering Data... [ 31%] src.haive.tools.tools.toolkits.base
[AutoAPI] Rendering Data... [ 31%] src.haive.dataflow.api.run_game_api
[AutoAPI] Rendering Data... [ 31%] src.haive.games.mafia.state_manager
[AutoAPI] Rendering Data... [ 31%] src.haive.games.mafia.simple_runner
[AutoAPI] Rendering Data... [ 31%] src.haive.games.monopoly.game_agent
[AutoAPI] Rendering Data... [ 31%] src.haive.games.monopoly.main_agent
[AutoAPI] Rendering Data... [ 31%] src.haive.games.nim.standalone_game
[AutoAPI] Rendering Data... [ 31%] src.haive.games.nim.generic_engines
[AutoAPI] Rendering Data... [ 31%] src.haive.games.multi_player.config
[AutoAPI] Rendering Data... [ 31%] src.haive.games.multi_player.models
[AutoAPI] Rendering Data... [ 31%] src.haive.games.tic_tac_toe.engines
[AutoAPI] Rendering Data... [ 31%] src.haive.games.chess.state_manager
[AutoAPI] Rendering Data... [ 31%] src.haive.games.core.game.core_game
[AutoAPI] Rendering Data... [ 31%] src.haive.games.fox_and_geese.state
[AutoAPI] Rendering Data... [ 32%] src.haive.games.fox_and_geese.agent
[AutoAPI] Rendering Data... [ 32%] src.haive.games.single_player.agent
[AutoAPI] Rendering Data... [ 32%] src.haive.mcp.comprehensive_mcp_web
[AutoAPI] Rendering Data... [ 32%] src.haive.mcp.mcp_simple_tool_agent
[AutoAPI] Rendering Data... [ 32%] src.haive.mcp.integrated_mcp_system
[AutoAPI] Rendering Data... [ 32%] src.haive.mcp.tools.server_selector
[AutoAPI] Rendering Data... [ 32%] src.haive.mcp.downloader.installers
[AutoAPI] Rendering Data... [ 32%] src.haive.core.common.logging_config
[AutoAPI] Rendering Data... [ 32%] src.haive.core.common.mixins.general
[AutoAPI] Rendering Data... [ 32%] src.haive.core.models.metadata_mixin
[AutoAPI] Rendering Data... [ 32%] src.haive.core.utils.interrupt_utils
[AutoAPI] Rendering Data... [ 32%] src.haive.core.engine.aug_llm.config
[AutoAPI] Rendering Data... [ 32%] src.haive.core.engine.base.protocols
[AutoAPI] Rendering Data... [ 32%] src.haive.core.engine.base.reference
[AutoAPI] Rendering Data... [ 32%] src.haive.core.engine.document.types
[AutoAPI] Rendering Data... [ 33%] src.haive.core.engine.agent.registry
[AutoAPI] Rendering Data... [ 33%] src.haive.core.engine.embedding.base
[AutoAPI] Rendering Data... [ 33%] src.haive.core.schema.schema_manager
[AutoAPI] Rendering Data... [ 33%] src.haive.core.schema.field_registry
[AutoAPI] Rendering Data... [ 33%] src.haive.core.schema.composer.field
[AutoAPI] Rendering Data... [ 33%] src.haive.core.schema.prebuilt.tools
[AutoAPI] Rendering Data... [ 33%] src.haive.core.graph.node.agent_node
[AutoAPI] Rendering Data... [ 33%] src.haive.core.graph.node.decorators
[AutoAPI] Rendering Data... [ 33%] src.haive.core.graph.branches.branch
[AutoAPI] Rendering Data... [ 33%] src.haive.agents.common.models.grade
[AutoAPI] Rendering Data... [ 33%] src.haive.agents.base.compiled_agent
[AutoAPI] Rendering Data... [ 33%] src.haive.agents.base.enhanced_agent
[AutoAPI] Rendering Data... [ 33%] src.haive.agents.supervisor.registry
[AutoAPI] Rendering Data... [ 33%] src.haive.agents.supervisor.agent_v2
[AutoAPI] Rendering Data... [ 33%] src.haive.agents.rag.unified_factory
[AutoAPI] Rendering Data... [ 34%] src.haive.agents.rag.synthesis_agent
[AutoAPI] Rendering Data... [ 34%] src.haive.agents.rag.self_reflective
[AutoAPI] Rendering Data... [ 34%] src.haive.agents.rag.self_rag2.state
[AutoAPI] Rendering Data... [ 34%] src.haive.agents.rag.step_back.agent
[AutoAPI] Rendering Data... [ 34%] src.haive.agents.rag.multi_agent_rag
[AutoAPI] Rendering Data... [ 34%] src.haive.agents.rag.db_rag.graph_db
[AutoAPI] Rendering Data... [ 34%] src.haive.agents.document_loader.web
[AutoAPI] Rendering Data... [ 34%] src.haive.agents.multi.archive.agent
[AutoAPI] Rendering Data... [ 34%] src.haive.agents.document_processing
[AutoAPI] Rendering Data... [ 34%] src.haive.agents.conversation.debate
[AutoAPI] Rendering Data... [ 34%] src.haive.tools.tools.genderize_tool
[AutoAPI] Rendering Data... [ 34%] src.haive.tools.tools.binlist_lookup
[AutoAPI] Rendering Data... [ 34%] src.haive.tools.tools.open_food_tool
[AutoAPI] Rendering Data... [ 34%] src.haive.dataflow.api.run_chess_api
[AutoAPI] Rendering Data... [ 34%] src.haive.dataflow.api.run_games_api
[AutoAPI] Rendering Data... [ 35%] src.haive.dataflow.api.routers.games
[AutoAPI] Rendering Data... [ 35%] src.haive.dataflow.auth.dependencies
[AutoAPI] Rendering Data... [ 35%] src.haive.games.common.voting_system
[AutoAPI] Rendering Data... [ 35%] src.haive.games.clue.generic_engines
[AutoAPI] Rendering Data... [ 35%] src.haive.games.mafia.verify_imports
[AutoAPI] Rendering Data... [ 35%] src.haive.games.hold_em.player_agent
[AutoAPI] Rendering Data... [ 35%] src.haive.games.multi_player.factory
[AutoAPI] Rendering Data... [ 35%] src.haive.games.framework.base.state
[AutoAPI] Rendering Data... [ 35%] src.haive.games.framework.base.utils
[AutoAPI] Rendering Data... [ 35%] src.haive.games.framework.base.agent
[AutoAPI] Rendering Data... [ 35%] src.haive.games.among_us.enhanced_ui
[AutoAPI] Rendering Data... [ 35%] src.haive.games.chess.dynamic_config
[AutoAPI] Rendering Data... [ 35%] src.haive.games.cards.standard.poker
[AutoAPI] Rendering Data... [ 35%] src.haive.games.core.game.core_space
[AutoAPI] Rendering Data... [ 35%] src.haive.games.core.game.core_board
[AutoAPI] Rendering Data... [ 36%] src.haive.games.core.game.containers
[AutoAPI] Rendering Data... [ 36%] src.haive.games.fox_and_geese.config
[AutoAPI] Rendering Data... [ 36%] src.haive.games.fox_and_geese.models
[AutoAPI] Rendering Data... [ 36%] src.haive.games.risk.generic_engines
[AutoAPI] Rendering Data... [ 36%] src.haive.games.single_player.rubiks
[AutoAPI] Rendering Data... [ 36%] src.haive.games.single_player.wordle
[AutoAPI] Rendering Data... [ 36%] src.haive.games.single_player.sudoku
[AutoAPI] Rendering Data... [ 36%] src.haive.mcp.simple_faiss_retriever
[AutoAPI] Rendering Data... [ 36%] src.haive.mcp.dynamic_activation_mcp
[AutoAPI] Rendering Data... [ 36%] src.haive.mcp.downloader.integration
[AutoAPI] Rendering Data... [ 36%] src.haive.mcp.downloader.legacy_core
[AutoAPI] Rendering Data... [ 36%] src.haive.core.common.structures.tree
[AutoAPI] Rendering Data... [ 36%] src.haive.core.common.types.protocols
[AutoAPI] Rendering Data... [ 36%] src.haive.core.persistence.store.base
[AutoAPI] Rendering Data... [ 36%] src.haive.core.models.embeddings.base
[AutoAPI] Rendering Data... [ 37%] src.haive.core.engine.aug_llm.factory
[AutoAPI] Rendering Data... [ 37%] src.haive.core.engine.document.config
[AutoAPI] Rendering Data... [ 37%] src.haive.core.engine.document.engine
[AutoAPI] Rendering Data... [ 37%] src.haive.core.engine.document.agents
[AutoAPI] Rendering Data... [ 37%] src.haive.core.engine.retriever.types
[AutoAPI] Rendering Data... [ 37%] src.haive.core.engine.agent.protocols
[AutoAPI] Rendering Data... [ 37%] src.haive.core.engine.embedding.types
[AutoAPI] Rendering Data... [ 37%] src.haive.core.engine.prompt_template
[AutoAPI] Rendering Data... [ 37%] src.haive.core.schema.schema_composer
[AutoAPI] Rendering Data... [ 37%] src.haive.core.schema.engine_io_mixin
[AutoAPI] Rendering Data... [ 37%] src.haive.core.schema.field_extractor
[AutoAPI] Rendering Data... [ 37%] src.haive.core.schema.composer.engine
[AutoAPI] Rendering Data... [ 37%] src.haive.core.graph.branches.dynamic
[AutoAPI] Rendering Data... [ 37%] src.haive.agents.base.universal_agent
[AutoAPI] Rendering Data... [ 37%] src.haive.agents.planning.models.base
[AutoAPI] Rendering Data... [ 38%] src.haive.agents.rag.chain_collection
[AutoAPI] Rendering Data... [ 38%] src.haive.agents.rag.document_grading
[AutoAPI] Rendering Data... [ 38%] src.haive.agents.rag.self_route.agent
[AutoAPI] Rendering Data... [ 38%] src.haive.agents.rag.corrective.agent
[AutoAPI] Rendering Data... [ 38%] src.haive.agents.document_loader.base
[AutoAPI] Rendering Data... [ 38%] src.haive.agents.document_loader.file
[AutoAPI] Rendering Data... [ 38%] src.haive.agents.react_class.react_v3
[AutoAPI] Rendering Data... [ 38%] src.haive.agents.react_class.react_v2
[AutoAPI] Rendering Data... [ 38%] src.haive.agents.multi.multi_agent_v4
[AutoAPI] Rendering Data... [ 38%] src.haive.agents.memory.sphinx_config
[AutoAPI] Rendering Data... [ 38%] src.haive.tools.tools.dataforseo_tool
[AutoAPI] Rendering Data... [ 38%] src.haive.tools.tools.geek_jokes_tool
[AutoAPI] Rendering Data... [ 38%] src.haive.tools.tools.translate_tools
[AutoAPI] Rendering Data... [ 38%] src.haive.tools.tools.merriam_webster
[AutoAPI] Rendering Data... [ 38%] src.haive.tools.tools.fruityvice_tool
[AutoAPI] Rendering Data... [ 39%] src.haive.dataflow.api.auto_discovery
[AutoAPI] Rendering Data... [ 39%] src.haive.dataflow.api.run_simplified
[AutoAPI] Rendering Data... [ 39%] src.haive.dataflow.registry.lazy_core
[AutoAPI] Rendering Data... [ 39%] src.haive.dataflow.registry.discovery
[AutoAPI] Rendering Data... [ 39%] src.haive.dataflow.registry.providers
[AutoAPI] Rendering Data... [ 39%] src.haive.dataflow.registry.importers
[AutoAPI] Rendering Data... [ 39%] src.haive.games.mafia.generic_engines
[AutoAPI] Rendering Data... [ 39%] src.haive.games.monopoly.player_agent
[AutoAPI] Rendering Data... [ 39%] src.haive.games.hold_em.state_manager
[AutoAPI] Rendering Data... [ 39%] src.haive.games.framework.base.config
[AutoAPI] Rendering Data... [ 39%] src.haive.games.mancala.state_manager
[AutoAPI] Rendering Data... [ 39%] src.haive.games.chess.generic_engines
[AutoAPI] Rendering Data... [ 39%] src.haive.games.core.components.cards
[AutoAPI] Rendering Data... [ 39%] src.haive.games.poker.generic_engines
[AutoAPI] Rendering Data... [ 39%] src.haive.games.fox_and_geese.engines
[AutoAPI] Rendering Data... [ 40%] src.haive.games.fox_and_geese.rich_ui
[AutoAPI] Rendering Data... [ 40%] src.haive.games.reversi.state_manager
[AutoAPI] Rendering Data... [ 40%] src.haive.games.single_player.testing
[AutoAPI] Rendering Data... [ 40%] src.haive.mcp.servers.dataflow_server
[AutoAPI] Rendering Data... [ 40%] src.haive.core.common.models.documents
[AutoAPI] Rendering Data... [ 40%] src.haive.core.common.mixins.mcp_mixin
[AutoAPI] Rendering Data... [ 40%] src.haive.core.persistence.serializers
[AutoAPI] Rendering Data... [ 40%] src.haive.core.persistence.store.types
[AutoAPI] Rendering Data... [ 40%] src.haive.core.engine.document.factory
[AutoAPI] Rendering Data... [ 40%] src.haive.core.engine.document.loaders
[AutoAPI] Rendering Data... [ 40%] src.haive.core.engine.vectorstore.base
[AutoAPI] Rendering Data... [ 40%] src.haive.core.engine.retriever.mixins
[AutoAPI] Rendering Data... [ 40%] src.haive.core.engine.embedding.config
[AutoAPI] Rendering Data... [ 40%] src.haive.core.schema.meta_agent_state
[AutoAPI] Rendering Data... [ 40%] src.haive.core.schema.field_definition
[AutoAPI] Rendering Data... [ 41%] src.haive.core.graph.common.references
[AutoAPI] Rendering Data... [ 41%] src.haive.core.graph.state_graph.utils
[AutoAPI] Rendering Data... [ 41%] src.haive.agents.research.person.agent
[AutoAPI] Rendering Data... [ 41%] src.haive.agents.task_analysis.context
[AutoAPI] Rendering Data... [ 41%] src.haive.agents.planning.rewoo.agents
[AutoAPI] Rendering Data... [ 41%] src.haive.agents.planning.rewoo.models
[AutoAPI] Rendering Data... [ 41%] src.haive.agents.planning.llm_compiler
[AutoAPI] Rendering Data... [ 41%] src.haive.agents.rag.simple.simple_rag
[AutoAPI] Rendering Data... [ 41%] src.haive.agents.rag.speculative.agent
[AutoAPI] Rendering Data... [ 41%] src.haive.agents.rag.multi_query.agent
[AutoAPI] Rendering Data... [ 41%] src.haive.agents.document_modifiers.kg
[AutoAPI] Rendering Data... [ 41%] src.haive.agents.conversation.directed
[AutoAPI] Rendering Data... [ 41%] src.haive.agents.wiki_writer.interview
[AutoAPI] Rendering Data... [ 41%] src.haive.tools.tools.toolkits.weather
[AutoAPI] Rendering Data... [ 41%] src.haive.dataflow.internal_websockets
[AutoAPI] Rendering Data... [ 42%] src.haive.dataflow.api.simple_chess_ws
[AutoAPI] Rendering Data... [ 42%] src.haive.dataflow.api.integrate_games
[AutoAPI] Rendering Data... [ 42%] src.haive.dataflow.registry.registries
[AutoAPI] Rendering Data... [ 42%] src.haive.games.checkers.state_manager
[AutoAPI] Rendering Data... [ 42%] src.haive.games.hold_em.engine_logging
[AutoAPI] Rendering Data... [ 42%] src.haive.games.framework.base.factory
[AutoAPI] Rendering Data... [ 42%] src.haive.games.framework.multi_player
[AutoAPI] Rendering Data... [ 42%] src.haive.games.mancala.agent_original
[AutoAPI] Rendering Data... [ 42%] src.haive.games.mancala.state_original
[AutoAPI] Rendering Data... [ 42%] src.haive.games.connect4.state_manager
[AutoAPI] Rendering Data... [ 42%] src.haive.games.among_us.state_manager
[AutoAPI] Rendering Data... [ 42%] src.haive.games.utils.recursion_config
[AutoAPI] Rendering Data... [ 42%] src.haive.games.debate.generic_engines
[AutoAPI] Rendering Data... [ 42%] src.haive.mcp.documentation.doc_loader
[AutoAPI] Rendering Data... [ 42%] src.haive.core.common.mixins.identifier
[AutoAPI] Rendering Data... [ 43%] src.haive.core.common.mixins.general.id
[AutoAPI] Rendering Data... [ 43%] src.haive.core.models.llm.providers.xai
[AutoAPI] Rendering Data... [ 43%] src.haive.core.types.general.file_types
[AutoAPI] Rendering Data... [ 43%] src.haive.core.engine.vectorstore.types
[AutoAPI] Rendering Data... [ 43%] src.haive.core.engine.agent.persistence
[AutoAPI] Rendering Data... [ 43%] src.haive.core.schema.prebuilt.messages
[AutoAPI] Rendering Data... [ 43%] src.haive.core.graph.node.agent_node_v3
[AutoAPI] Rendering Data... [ 43%] src.haive.core.graph.node.callable_node
[AutoAPI] Rendering Data... [ 43%] src.haive.core.graph.common.field_utils
[AutoAPI] Rendering Data... [ 43%] src.haive.agents.task_analysis.analysis
[AutoAPI] Rendering Data... [ 43%] src.haive.agents.planning.p_and_e.state
[AutoAPI] Rendering Data... [ 43%] src.haive.agents.planning.p_and_e.agent
[AutoAPI] Rendering Data... [ 43%] src.haive.agents.rag.memory_aware.agent
[AutoAPI] Rendering Data... [ 43%] src.haive.agents.rag.simple.enhanced_v3
[AutoAPI] Rendering Data... [ 43%] src.haive.agents.reasoning_and_critique
[AutoAPI] Rendering Data... [ 44%] src.haive.agents.document_modifiers.tnt
[AutoAPI] Rendering Data... [ 44%] src.haive.agents.multi.sequential.agent
[AutoAPI] Rendering Data... [ 44%] src.haive.agents.memory.models.semantic
[AutoAPI] Rendering Data... [ 44%] src.haive.agents.memory.models.episodic
[AutoAPI] Rendering Data... [ 44%] src.haive.agents.memory.core.classifier
[AutoAPI] Rendering Data... [ 44%] src.haive.agents.experiments.supervisor
[AutoAPI] Rendering Data... [ 44%] src.haive.agents.memory_v2.memory_state
[AutoAPI] Rendering Data... [ 44%] src.haive.agents.memory_v2.memory_tools
[AutoAPI] Rendering Data... [ 44%] src.haive.tools.tools.techy_phrase_tool
[AutoAPI] Rendering Data... [ 44%] src.haive.tools.tools.duckduckgo_search
[AutoAPI] Rendering Data... [ 44%] src.haive.tools.tools.corporate_bs_tool
[AutoAPI] Rendering Data... [ 44%] src.haive.games.hold_em.generic_engines
[AutoAPI] Rendering Data... [ 44%] src.haive.games.nim.configurable_config
[AutoAPI] Rendering Data... [ 44%] src.haive.games.mancala.generic_engines
[AutoAPI] Rendering Data... [ 44%] src.haive.games.core.game.core_position
[AutoAPI] Rendering Data... [ 45%] src.haive.games.core.agent.player_agent
[AutoAPI] Rendering Data... [ 45%] src.haive.games.reversi.generic_engines
[AutoAPI] Rendering Data... [ 45%] src.haive.games.single_player.flow_free
[AutoAPI] Rendering Data... [ 45%] src.haive.mcp.installers.config_manager
[AutoAPI] Rendering Data... [ 45%] src.haive.core.persistence.sqlite_config
[AutoAPI] Rendering Data... [ 45%] src.haive.core.persistence.store.factory
[AutoAPI] Rendering Data... [ 45%] src.haive.core.models.llm.provider_types
[AutoAPI] Rendering Data... [ 45%] src.haive.core.models.llm.providers.base
[AutoAPI] Rendering Data... [ 45%] src.haive.core.models.llm.providers.groq
[AutoAPI] Rendering Data... [ 45%] src.haive.core.models.llm.providers.ai21
[AutoAPI] Rendering Data... [ 45%] src.haive.core.registry.dynamic_registry
[AutoAPI] Rendering Data... [ 45%] src.haive.core.engine.aug_llm.mcp_config
[AutoAPI] Rendering Data... [ 45%] src.haive.core.engine.document.splitters
[AutoAPI] Rendering Data... [ 45%] src.haive.core.schema.base_state_schemas
[AutoAPI] Rendering Data... [ 45%] src.haive.core.schema.typed_state_schema
[AutoAPI] Rendering Data... [ 46%] src.haive.core.schema.prebuilt.llm_state
[AutoAPI] Rendering Data... [ 46%] src.haive.agents.reflection.simple_agent
[AutoAPI] Rendering Data... [ 46%] src.haive.agents.base.mixins.hooks_mixin
[AutoAPI] Rendering Data... [ 46%] src.haive.agents.structured_output.agent
[AutoAPI] Rendering Data... [ 46%] src.haive.agents.task_analysis.execution
[AutoAPI] Rendering Data... [ 46%] src.haive.agents.chain.multi_integration
[AutoAPI] Rendering Data... [ 46%] src.haive.agents.planning.p_and_e.models
[AutoAPI] Rendering Data... [ 46%] src.haive.agents.planning.rewoo_v3.state
[AutoAPI] Rendering Data... [ 46%] src.haive.agents.planning.rewoo_v3.agent
[AutoAPI] Rendering Data... [ 46%] src.haive.agents.simple.ultra_lazy_agent
[AutoAPI] Rendering Data... [ 46%] src.haive.agents.simple.agent_v3_minimal
[AutoAPI] Rendering Data... [ 46%] src.haive.agents.rag.simple_rag_agent_v4
[AutoAPI] Rendering Data... [ 46%] src.haive.agents.rag.hyde.enhanced_agent
[AutoAPI] Rendering Data... [ 46%] src.haive.agents.rag.simple.answer_agent
[AutoAPI] Rendering Data... [ 46%] src.haive.agents.rag.query_decomposition
[AutoAPI] Rendering Data... [ 47%] src.haive.agents.rag.corrective.agent_v2
[AutoAPI] Rendering Data... [ 47%] src.haive.agents.react.enhanced_agent_v3
[AutoAPI] Rendering Data... [ 47%] src.haive.agents.react_class.react_agent
[AutoAPI] Rendering Data... [ 47%] src.haive.agents.document_modifiers.base
[AutoAPI] Rendering Data... [ 47%] src.haive.agents.conversation.base.state
[AutoAPI] Rendering Data... [ 47%] src.haive.agents.conversation.base.agent
[AutoAPI] Rendering Data... [ 47%] src.haive.agents.memory_v2.token_tracker
[AutoAPI] Rendering Data... [ 47%] src.haive.tools.tools.wolfram_alpha_tool
[AutoAPI] Rendering Data... [ 47%] src.haive.tools.tools.scene_explain_tool
[AutoAPI] Rendering Data... [ 47%] src.haive.tools.tools.domain_search_tool
[AutoAPI] Rendering Data... [ 47%] src.haive.tools.tools.google.google_jobs
[AutoAPI] Rendering Data... [ 47%] src.haive.tools.tools.google.google_lens
[AutoAPI] Rendering Data... [ 47%] src.haive.tools.tools.toolkits.dev.tools
[AutoAPI] Rendering Data... [ 47%] src.haive.dataflow.api.general_games_api
[AutoAPI] Rendering Data... [ 47%] src.haive.dataflow.api.game_router_fixed
[AutoAPI] Rendering Data... [ 48%] src.haive.dataflow.api.routes.llm_routes
[AutoAPI] Rendering Data... [ 48%] src.haive.games.clue.configurable_config
[AutoAPI] Rendering Data... [ 48%] src.haive.games.checkers.generic_engines
[AutoAPI] Rendering Data... [ 48%] src.haive.games.mastermind.state_manager
[AutoAPI] Rendering Data... [ 48%] src.haive.games.dominoes.generic_engines
[AutoAPI] Rendering Data... [ 48%] src.haive.games.monopoly.generic_engines
[AutoAPI] Rendering Data... [ 48%] src.haive.games.connect4.generic_engines
[AutoAPI] Rendering Data... [ 48%] src.haive.games.among_us.generic_engines
[AutoAPI] Rendering Data... [ 48%] src.haive.games.risk.configurable_config
[AutoAPI] Rendering Data... [ 48%] src.haive.games.battleship.state_manager
[AutoAPI] Rendering Data... [ 48%] src.haive.mcp.working_enhanced_retriever
[AutoAPI] Rendering Data... [ 48%] src.haive.mcp.agents.documentation_agent
[AutoAPI] Rendering Data... [ 48%] src.haive.mcp.discovery.server_discovery
[AutoAPI] Rendering Data... [ 48%] src.haive.mcp.servers.simple_http_server
[AutoAPI] Rendering Data... [ 48%] src.haive.core.common.mixins.engine_mixin
[AutoAPI] Rendering Data... [ 49%] src.haive.core.common.mixins.getter_mixin
[AutoAPI] Rendering Data... [ 49%] src.haive.core.persistence.store.postgres
[AutoAPI] Rendering Data... [ 49%] src.haive.core.persistence.store.wrappers
[AutoAPI] Rendering Data... [ 49%] src.haive.core.models.llm.providers.azure
[AutoAPI] Rendering Data... [ 49%] src.haive.core.engine.document.processors
[AutoAPI] Rendering Data... [ 49%] src.haive.core.engine.retriever.retriever
[AutoAPI] Rendering Data... [ 49%] src.haive.core.engine.retriever.providers
[AutoAPI] Rendering Data... [ 49%] src.haive.core.engine.embedding.providers
[AutoAPI] Rendering Data... [ 49%] src.haive.core.schema.prebuilt.meta_state
[AutoAPI] Rendering Data... [ 49%] src.haive.core.schema.compatibility.utils
[AutoAPI] Rendering Data... [ 49%] src.haive.core.schema.compatibility.types
[AutoAPI] Rendering Data... [ 49%] src.haive.core.graph.node.meta_agent_node
[AutoAPI] Rendering Data... [ 49%] src.haive.core.graph.common.serialization
[AutoAPI] Rendering Data... [ 49%] src.haive.core.graph.state_graph.registry
[AutoAPI] Rendering Data... [ 49%] src.haive.agents.research.open_perplexity
[AutoAPI] Rendering Data... [ 50%] src.haive.agents.common.models.grade.base
[AutoAPI] Rendering Data... [ 50%] src.haive.agents.base.serialization_mixin
[AutoAPI] Rendering Data... [ 50%] src.haive.agents.structured_output.models
[AutoAPI] Rendering Data... [ 50%] src.haive.agents.task_analysis.decomposer
[AutoAPI] Rendering Data... [ 50%] src.haive.agents.supervisor.dynamic_state
[AutoAPI] Rendering Data... [ 50%] src.haive.agents.chain.chain_agent_simple
[AutoAPI] Rendering Data... [ 50%] src.haive.agents.planning.plan_execute_v3
[AutoAPI] Rendering Data... [ 50%] src.haive.agents.planning.llm_compiler_v3
[AutoAPI] Rendering Data... [ 50%] src.haive.agents.planning.p_and_e.engines
[AutoAPI] Rendering Data... [ 50%] src.haive.agents.planning.p_and_e.prompts
[AutoAPI] Rendering Data... [ 50%] src.haive.agents.planning.rewoo_v3.models
[AutoAPI] Rendering Data... [ 50%] src.haive.agents.simple.enhanced_agent_v3
[AutoAPI] Rendering Data... [ 50%] src.haive.agents.simple.lazy_simple_agent
[AutoAPI] Rendering Data... [ 50%] src.haive.agents.rag.agentic_router.agent
[AutoAPI] Rendering Data... [ 50%] src.haive.agents.rag.adaptive_tools.agent
[AutoAPI] Rendering Data... [ 50%] src.haive.agents.rag.db_rag.sql_rag.state
[AutoAPI] Rendering Data... [ 51%] src.haive.agents.rag.db_rag.sql_rag.utils
[AutoAPI] Rendering Data... [ 51%] src.haive.agents.rag.db_rag.sql_rag.agent
[AutoAPI] Rendering Data... [ 51%] src.haive.agents.rag.query_planning.agent
[AutoAPI] Rendering Data... [ 51%] src.haive.agents.dynamic_supervisor.state
[AutoAPI] Rendering Data... [ 51%] src.haive.agents.dynamic_supervisor.agent
[AutoAPI] Rendering Data... [ 51%] src.haive.agents.dynamic_supervisor.tools
[AutoAPI] Rendering Data... [ 51%] src.haive.agents.react_class.react_agent2
[AutoAPI] Rendering Data... [ 51%] src.haive.agents.memory.models.procedural
[AutoAPI] Rendering Data... [ 51%] src.haive.agents.memory.search.pro_search
[AutoAPI] Rendering Data... [ 51%] src.haive.agents.memory.search.labs.agent
[AutoAPI] Rendering Data... [ 51%] src.haive.agents.conversation.round_robin
[AutoAPI] Rendering Data... [ 51%] src.haive.tools.tools.youtube_search_tool
[AutoAPI] Rendering Data... [ 51%] src.haive.tools.tools.google.google_books
[AutoAPI] Rendering Data... [ 51%] src.haive.tools.tools.toolkits.office_365
[AutoAPI] Rendering Data... [ 51%] src.haive.tools.tools.toolkits.dev.python
[AutoAPI] Rendering Data... [ 52%] src.haive.dataflow.api.run_integrated_api
[AutoAPI] Rendering Data... [ 52%] src.haive.dataflow.api.serve_chess_client
[AutoAPI] Rendering Data... [ 52%] src.haive.dataflow.registry.serialization
[AutoAPI] Rendering Data... [ 52%] src.haive.dataflow.registry.importers.tak
[AutoAPI] Rendering Data... [ 52%] src.haive.dataflow.registry.utils.logging
[AutoAPI] Rendering Data... [ 52%] src.haive.games.mafia.configurable_config
[AutoAPI] Rendering Data... [ 52%] src.haive.games.tic_tac_toe.state_manager
[AutoAPI] Rendering Data... [ 52%] src.haive.games.chess.configurable_config
[AutoAPI] Rendering Data... [ 52%] src.haive.games.core.game.containers.base
[AutoAPI] Rendering Data... [ 52%] src.haive.games.core.game.containers.deck
[AutoAPI] Rendering Data... [ 52%] src.haive.games.poker.configurable_config
[AutoAPI] Rendering Data... [ 52%] src.haive.games.single_player.sudoku.game
[AutoAPI] Rendering Data... [ 52%] src.haive.mcp.servers.dataflow_mcp_server
[AutoAPI] Rendering Data... [ 52%] src.haive.core.common.mixins.secure_config
[AutoAPI] Rendering Data... [ 52%] src.haive.core.common.mixins.general.state
[AutoAPI] Rendering Data... [ 53%] src.haive.core.persistence.postgres_config
[AutoAPI] Rendering Data... [ 53%] src.haive.core.persistence.supabase_config
[AutoAPI] Rendering Data... [ 53%] src.haive.core.models.llm.providers.cohere
[AutoAPI] Rendering Data... [ 53%] src.haive.core.models.llm.providers.openai
[AutoAPI] Rendering Data... [ 53%] src.haive.core.models.llm.providers.ollama
[AutoAPI] Rendering Data... [ 53%] src.haive.core.models.llm.providers.google
[AutoAPI] Rendering Data... [ 53%] src.haive.core.models.llm.providers.nvidia
[AutoAPI] Rendering Data... [ 53%] src.haive.core.engine.document.types.enums
[AutoAPI] Rendering Data... [ 53%] src.haive.core.schema.prebuilt.query_state
[AutoAPI] Rendering Data... [ 53%] src.haive.core.graph.node.base_node_config
[AutoAPI] Rendering Data... [ 53%] src.haive.core.graph.node.multi_agent_node
[AutoAPI] Rendering Data... [ 53%] src.haive.core.graph.branches.send_mapping
[AutoAPI] Rendering Data... [ 53%] src.haive.agents.common.models.grade.scale
[AutoAPI] Rendering Data... [ 53%] src.haive.agents.base.pre_post_agent_mixin
[AutoAPI] Rendering Data... [ 53%] src.haive.agents.planning.rewoo_tree_agent
[AutoAPI] Rendering Data... [ 54%] src.haive.agents.planning.plan_and_execute
[AutoAPI] Rendering Data... [ 54%] src.haive.agents.planning.rewoo_v3.prompts
[AutoAPI] Rendering Data... [ 54%] src.haive.agents.rag.enhanced_memory_react
[AutoAPI] Rendering Data... [ 54%] src.haive.agents.rag.self_reflective.agent
[AutoAPI] Rendering Data... [ 54%] src.haive.agents.rag.multi_agent_rag.state
[AutoAPI] Rendering Data... [ 54%] src.haive.agents.rag.db_rag.sql_rag.config
[AutoAPI] Rendering Data... [ 54%] src.haive.agents.rag.db_rag.graph_db.state
[AutoAPI] Rendering Data... [ 54%] src.haive.agents.rag.db_rag.graph_db.agent
[AutoAPI] Rendering Data... [ 54%] src.haive.agents.rag.hallucination_grading
[AutoAPI] Rendering Data... [ 54%] src.haive.agents.dynamic_supervisor.models
[AutoAPI] Rendering Data... [ 54%] src.haive.agents.document_loader.directory
[AutoAPI] Rendering Data... [ 54%] src.haive.agents.document_loader.web.agent
[AutoAPI] Rendering Data... [ 54%] src.haive.agents.react.dynamic_react_agent
[AutoAPI] Rendering Data... [ 54%] src.haive.agents.document_processing.agent
[AutoAPI] Rendering Data... [ 54%] src.haive.agents.memory.kg_generator_agent
[AutoAPI] Rendering Data... [ 55%] src.haive.agents.memory.unified_memory_api
[AutoAPI] Rendering Data... [ 55%] src.haive.agents.memory.enhanced_retriever
[AutoAPI] Rendering Data... [ 55%] src.haive.agents.memory.search.labs.models
[AutoAPI] Rendering Data... [ 55%] src.haive.agents.conversation.debate.state
[AutoAPI] Rendering Data... [ 55%] src.haive.agents.conversation.debate.agent
[AutoAPI] Rendering Data... [ 55%] src.haive.agents.conversation.social_media
[AutoAPI] Rendering Data... [ 55%] src.haive.agents.memory_v2.kg_memory_agent
[AutoAPI] Rendering Data... [ 55%] src.haive.tools.tools.google.google_places
[AutoAPI] Rendering Data... [ 55%] src.haive.tools.tools.google.google_trends
[AutoAPI] Rendering Data... [ 55%] src.haive.tools.tools.google.google_search
[AutoAPI] Rendering Data... [ 55%] src.haive.tools.tools.toolkits.nla_toolkit
[AutoAPI] Rendering Data... [ 55%] src.haive.dataflow.api.routes.agent_routes
[AutoAPI] Rendering Data... [ 55%] src.haive.dataflow.api.routes.tools_routes
[AutoAPI] Rendering Data... [ 55%] src.haive.dataflow.registry.providers.base
[AutoAPI] Rendering Data... [ 55%] src.haive.games.mastermind.generic_engines
[AutoAPI] Rendering Data... [ 56%] src.haive.games.multi_player.state_manager
[AutoAPI] Rendering Data... [ 56%] src.haive.games.chess.configurable_engines
[AutoAPI] Rendering Data... [ 56%] src.haive.games.core.game.pieces.core_game
[AutoAPI] Rendering Data... [ 56%] src.haive.games.debate.configurable_config
[AutoAPI] Rendering Data... [ 56%] src.haive.games.fox_and_geese.fixed_runner
[AutoAPI] Rendering Data... [ 56%] src.haive.games.single_player.rubiks.agent
[AutoAPI] Rendering Data... [ 56%] src.haive.games.single_player.mine_sweeper
[AutoAPI] Rendering Data... [ 56%] src.haive.games.battleship.generic_engines
[AutoAPI] Rendering Data... [ 56%] src.haive.mcp.agents.intelligent_mcp_agent
[AutoAPI] Rendering Data... [ 56%] src.haive.core.persistence.store.connection
[AutoAPI] Rendering Data... [ 56%] src.haive.core.persistence.store.embeddings
[AutoAPI] Rendering Data... [ 56%] src.haive.core.models.llm.providers.mistral
[AutoAPI] Rendering Data... [ 56%] src.haive.core.models.llm.providers.bedrock
[AutoAPI] Rendering Data... [ 56%] src.haive.core.tools.interrupt_tool_wrapper
[AutoAPI] Rendering Data... [ 56%] src.haive.core.engine.document.transformers
[AutoAPI] Rendering Data... [ 57%] src.haive.core.engine.document.loaders.base
[AutoAPI] Rendering Data... [ 57%] src.haive.core.engine.vectorstore.discovery
[AutoAPI] Rendering Data... [ 57%] src.haive.core.engine.vectorstore.providers
[AutoAPI] Rendering Data... [ 57%] src.haive.core.schema.agent_schema_composer
[AutoAPI] Rendering Data... [ 57%] src.haive.core.schema.compatibility.reports
[AutoAPI] Rendering Data... [ 57%] src.haive.core.schema.compatibility.mergers
[AutoAPI] Rendering Data... [ 57%] src.haive.core.graph.state_graph.conversion
[AutoAPI] Rendering Data... [ 57%] src.haive.core.graph.state_graph.components
[AutoAPI] Rendering Data... [ 57%] src.haive.agents.common.models.grade.rubric
[AutoAPI] Rendering Data... [ 57%] src.haive.agents.common.models.grade.binary
[AutoAPI] Rendering Data... [ 57%] src.haive.agents.rag.document_grading.agent
[AutoAPI] Rendering Data... [ 57%] src.haive.agents.rag.hyde.enhanced_agent_v2
[AutoAPI] Rendering Data... [ 57%] src.haive.agents.rag.multi_agent_rag.agents
[AutoAPI] Rendering Data... [ 57%] src.haive.agents.rag.db_rag.sql_rag.engines
[AutoAPI] Rendering Data... [ 57%] src.haive.agents.rag.db_rag.sql_rag.prompts
[AutoAPI] Rendering Data... [ 58%] src.haive.agents.rag.db_rag.graph_db.config
[AutoAPI] Rendering Data... [ 58%] src.haive.agents.rag.db_rag.graph_db.models
[AutoAPI] Rendering Data... [ 58%] src.haive.agents.rag.agentic.query_rewriter
[AutoAPI] Rendering Data... [ 58%] src.haive.agents.dynamic_supervisor.prompts
[AutoAPI] Rendering Data... [ 58%] src.haive.agents.document_loader.base.agent
[AutoAPI] Rendering Data... [ 58%] src.haive.agents.document_loader.file.agent
[AutoAPI] Rendering Data... [ 58%] src.haive.agents.react.enhanced_react_agent
[AutoAPI] Rendering Data... [ 58%] src.haive.agents.reasoning_and_critique.tot
[AutoAPI] Rendering Data... [ 58%] src.haive.agents.react_class.react_v3.agent
[AutoAPI] Rendering Data... [ 58%] src.haive.agents.react_class.react_v2.utils
[AutoAPI] Rendering Data... [ 58%] src.haive.agents.react_class.react_v2.agent
[AutoAPI] Rendering Data... [ 58%] src.haive.agents.memory.graph_rag_retriever
[AutoAPI] Rendering Data... [ 58%] src.haive.agents.memory.search.quick_search
[AutoAPI] Rendering Data... [ 58%] src.haive.agents.conversation.collaberative
[AutoAPI] Rendering Data... [ 58%] src.haive.agents.memory_v2.rag_memory_agent
[AutoAPI] Rendering Data... [ 59%] src.haive.tools.tools.google.google_finance
[AutoAPI] Rendering Data... [ 59%] src.haive.tools.tools.google.google_scholar
[AutoAPI] Rendering Data... [ 59%] src.haive.tools.tools.toolkits.jira_toolkit
[AutoAPI] Rendering Data... [ 59%] src.haive.tools.tools.toolkits.lcbo_toolkit
[AutoAPI] Rendering Data... [ 59%] src.haive.tools.tools.toolkits.fred_toolkit
[AutoAPI] Rendering Data... [ 59%] src.haive.dataflow.fetchers.lite_llm_import
[AutoAPI] Rendering Data... [ 59%] src.haive.dataflow.api.game_router_enhanced
[AutoAPI] Rendering Data... [ 59%] src.haive.dataflow.providers.agent_provider
[AutoAPI] Rendering Data... [ 59%] src.haive.games.hold_em.configurable_config
[AutoAPI] Rendering Data... [ 59%] src.haive.games.tic_tac_toe.generic_engines
[AutoAPI] Rendering Data... [ 59%] src.haive.games.mancala.configurable_config
[AutoAPI] Rendering Data... [ 59%] src.haive.games.debate_v2.agent_with_judges
[AutoAPI] Rendering Data... [ 59%] src.haive.games.fox_and_geese.state_manager
[AutoAPI] Rendering Data... [ 59%] src.haive.games.reversi.configurable_config
[AutoAPI] Rendering Data... [ 59%] src.haive.mcp.agents.transferable_mcp_agent
[AutoAPI] Rendering Data... [ 60%] src.haive.core.common.mixins.timestamp_mixin
[AutoAPI] Rendering Data... [ 60%] src.haive.core.common.mixins.recompile_mixin
[AutoAPI] Rendering Data... [ 60%] src.haive.core.common.mixins.tool_list_mixin
[AutoAPI] Rendering Data... [ 60%] src.haive.core.common.mixins.general.version
[AutoAPI] Rendering Data... [ 60%] src.haive.core.common.types.abc_root_wrapper
[AutoAPI] Rendering Data... [ 60%] src.haive.core.models.llm.providers.together
[AutoAPI] Rendering Data... [ 60%] src.haive.core.engine.document.path_analysis
[AutoAPI] Rendering Data... [ 60%] src.haive.core.schema.compatibility.analyzer
[AutoAPI] Rendering Data... [ 60%] src.haive.core.graph.node.validation_node_v2
[AutoAPI] Rendering Data... [ 60%] src.haive.core.graph.node.composer.protocols
[AutoAPI] Rendering Data... [ 60%] src.haive.core.graph.state_graph.base_graph2
[AutoAPI] Rendering Data... [ 60%] src.haive.agents.common.models.task_analysis
[AutoAPI] Rendering Data... [ 60%] src.haive.agents.common.models.grade.numeric
[AutoAPI] Rendering Data... [ 60%] src.haive.agents.planning.clean_plan_execute
[AutoAPI] Rendering Data... [ 60%] src.haive.agents.planning.rewoo.models.steps
[AutoAPI] Rendering Data... [ 61%] src.haive.agents.planning.rewoo.models.plans
[AutoAPI] Rendering Data... [ 61%] src.haive.agents.planning.llm_compiler.agent
[AutoAPI] Rendering Data... [ 61%] src.haive.agents.simple.enhanced_simple_real
[AutoAPI] Rendering Data... [ 61%] src.haive.agents.rag.collective_rag_agent_v4
[AutoAPI] Rendering Data... [ 61%] src.haive.agents.rag.agentic_router.agent_v2
[AutoAPI] Rendering Data... [ 61%] src.haive.agents.rag.common.document_graders
[AutoAPI] Rendering Data... [ 61%] src.haive.agents.rag.common.query_refinement
[AutoAPI] Rendering Data... [ 61%] src.haive.agents.rag.simple.clean_simple_rag
[AutoAPI] Rendering Data... [ 61%] src.haive.agents.rag.simple.sequential_agent
[AutoAPI] Rendering Data... [ 61%] src.haive.agents.rag.simple.simple_rag_state
[AutoAPI] Rendering Data... [ 61%] src.haive.agents.rag.simple.answer_generator
[AutoAPI] Rendering Data... [ 61%] src.haive.agents.rag.db_rag.graph_db.engines
[AutoAPI] Rendering Data... [ 61%] src.haive.agents.rag.agentic.react_rag_agent
[AutoAPI] Rendering Data... [ 61%] src.haive.agents.rag.agentic.document_grader
[AutoAPI] Rendering Data... [ 61%] src.haive.agents.reasoning_and_critique.lats
[AutoAPI] Rendering Data... [ 62%] src.haive.agents.reasoning_and_critique.mcts
[AutoAPI] Rendering Data... [ 62%] src.haive.agents.react_class.react_v3.config
[AutoAPI] Rendering Data... [ 62%] src.haive.agents.react_class.react_v2.config
[AutoAPI] Rendering Data... [ 62%] src.haive.agents.multi.archive.enhanced_base
[AutoAPI] Rendering Data... [ 62%] src.haive.agents.memory.search.deep_research
[AutoAPI] Rendering Data... [ 62%] src.haive.agents.conversation.directed.state
[AutoAPI] Rendering Data... [ 62%] src.haive.agents.conversation.directed.agent
[AutoAPI] Rendering Data... [ 62%] src.haive.tools.tools.toolkits.gmail_toolkit
[AutoAPI] Rendering Data... [ 62%] src.haive.tools.tools.toolkits.alpha_vantage
[AutoAPI] Rendering Data... [ 62%] src.haive.tools.tools.toolkits.slack_toolkit
[AutoAPI] Rendering Data... [ 62%] src.haive.tools.tools.toolkits.steam_toolkit
[AutoAPI] Rendering Data... [ 62%] src.haive.tools.tools.toolkits.request_tools
[AutoAPI] Rendering Data... [ 62%] src.haive.dataflow.persistence.conversations
[AutoAPI] Rendering Data... [ 62%] src.haive.dataflow.registries.model_registry
[AutoAPI] Rendering Data... [ 62%] src.haive.games.checkers.configurable_config
[AutoAPI] Rendering Data... [ 63%] src.haive.games.dominoes.configurable_config
[AutoAPI] Rendering Data... [ 63%] src.haive.games.monopoly.configurable_config
[AutoAPI] Rendering Data... [ 63%] src.haive.games.framework.base.state_manager
[AutoAPI] Rendering Data... [ 63%] src.haive.games.framework.multi_player.state
[AutoAPI] Rendering Data... [ 63%] src.haive.games.framework.multi_player.agent
[AutoAPI] Rendering Data... [ 63%] src.haive.games.connect4.configurable_config
[AutoAPI] Rendering Data... [ 63%] src.haive.games.among_us.configurable_config
[AutoAPI] Rendering Data... [ 63%] src.haive.mcp.utils.extract_mcp_github_repos
[AutoAPI] Rendering Data... [ 63%] src.haive.core.common.mixins.tool_route_mixin
[AutoAPI] Rendering Data... [ 63%] src.haive.core.common.mixins.general.metadata
[AutoAPI] Rendering Data... [ 63%] src.haive.core.models.llm.rate_limiting_mixin
[AutoAPI] Rendering Data... [ 63%] src.haive.core.models.llm.providers.anthropic
[AutoAPI] Rendering Data... [ 63%] src.haive.core.models.llm.providers.fireworks
[AutoAPI] Rendering Data... [ 63%] src.haive.core.models.llm.providers.replicate
[AutoAPI] Rendering Data... [ 63%] src.haive.core.engine.document.loaders.engine
[AutoAPI] Rendering Data... [ 64%] src.haive.core.engine.vectorstore.vectorstore
[AutoAPI] Rendering Data... [ 64%] src.haive.core.schema.prebuilt.document_state
[AutoAPI] Rendering Data... [ 64%] src.haive.core.schema.prebuilt.messages.utils
[AutoAPI] Rendering Data... [ 64%] src.haive.core.schema.compatibility.protocols
[AutoAPI] Rendering Data... [ 64%] src.haive.core.graph.node.engine_node_generic
[AutoAPI] Rendering Data... [ 64%] src.haive.core.graph.state_graph.serializable
[AutoAPI] Rendering Data... [ 64%] src.haive.agents.reflection.structured_output
[AutoAPI] Rendering Data... [ 64%] src.haive.agents.discovery.semantic_discovery
[AutoAPI] Rendering Data... [ 64%] src.haive.agents.supervisor.simple_supervisor
[AutoAPI] Rendering Data... [ 64%] src.haive.agents.planning.proper_plan_execute
[AutoAPI] Rendering Data... [ 64%] src.haive.agents.planning.rewoo_tree_agent_v2
[AutoAPI] Rendering Data... [ 64%] src.haive.agents.planning.rewoo_tree_agent_v3
[AutoAPI] Rendering Data... [ 64%] src.haive.agents.planning.plan_and_execute.v2
[AutoAPI] Rendering Data... [ 64%] src.haive.agents.planning.p_and_e.multi_agent
[AutoAPI] Rendering Data... [ 64%] src.haive.agents.planning.llm_compiler.config
[AutoAPI] Rendering Data... [ 65%] src.haive.agents.planning.llm_compiler.models
[AutoAPI] Rendering Data... [ 65%] src.haive.agents.simple.agent_with_validation
[AutoAPI] Rendering Data... [ 65%] src.haive.agents.simple.clean_enhanced_simple
[AutoAPI] Rendering Data... [ 65%] src.haive.agents.simple.enhanced_simple_agent
[AutoAPI] Rendering Data... [ 65%] src.haive.agents.rag.common.answer_generators
[AutoAPI] Rendering Data... [ 65%] src.haive.agents.rag.simple.enhanced_v3.state
[AutoAPI] Rendering Data... [ 65%] src.haive.agents.rag.simple.enhanced_v3.agent
[AutoAPI] Rendering Data... [ 65%] src.haive.agents.reasoning_and_critique.logic
[AutoAPI] Rendering Data... [ 65%] src.haive.agents.react_class.react_many_tools
[AutoAPI] Rendering Data... [ 65%] src.haive.agents.document_modifiers.tnt.state
[AutoAPI] Rendering Data... [ 65%] src.haive.agents.document_modifiers.tnt.utils
[AutoAPI] Rendering Data... [ 65%] src.haive.agents.document_modifiers.tnt.agent
[AutoAPI] Rendering Data... [ 65%] src.haive.agents.memory_v2.extraction_prompts
[AutoAPI] Rendering Data... [ 65%] src.haive.agents.memory_v2.react_memory_agent
[AutoAPI] Rendering Data... [ 65%] src.haive.agents.memory_v2.multi_memory_agent
[AutoAPI] Rendering Data... [ 66%] src.haive.agents.memory_v2.graph_memory_agent
[AutoAPI] Rendering Data... [ 66%] src.haive.tools.tools.report_of_the_week_tool
[AutoAPI] Rendering Data... [ 66%] src.haive.tools.tools.toolkits.twilio_toolkit
[AutoAPI] Rendering Data... [ 66%] src.haive.tools.tools.toolkits.gitlab_toolkit
[AutoAPI] Rendering Data... [ 66%] src.haive.tools.tools.toolkits.sql_db_toolkit
[AutoAPI] Rendering Data... [ 66%] src.haive.tools.tools.toolkits.stripe_toolkit
[AutoAPI] Rendering Data... [ 66%] src.haive.tools.tools.toolkits.github_toolkit
[AutoAPI] Rendering Data... [ 66%] src.haive.tools.tools.toolkits.vbible_toolkit
[AutoAPI] Rendering Data... [ 66%] src.haive.tools.tools.toolkits.gradio_toolkit
[AutoAPI] Rendering Data... [ 66%] src.haive.dataflow.importers.litellm_importer
[AutoAPI] Rendering Data... [ 66%] src.haive.games.framework.multi_player.config
[AutoAPI] Rendering Data... [ 66%] src.haive.games.framework.multi_player.models
[AutoAPI] Rendering Data... [ 66%] src.haive.games.fox_and_geese.generic_engines
[AutoAPI] Rendering Data... [ 66%] src.haive.games.single_player.flow_free.state
[AutoAPI] Rendering Data... [ 66%] src.haive.games.single_player.flow_free.agent
[AutoAPI] Rendering Data... [ 67%] src.haive.games.single_player.logic_grid.game
[AutoAPI] Rendering Data... [ 67%] src.haive.core.common.mixins.general.timestamp
[AutoAPI] Rendering Data... [ 67%] src.haive.core.engine.document.loaders.sources
[AutoAPI] Rendering Data... [ 67%] src.haive.core.schema.multi_agent_state_schema
[AutoAPI] Rendering Data... [ 67%] src.haive.core.schema.composer.schema_composer
[AutoAPI] Rendering Data... [ 67%] src.haive.core.schema.compatibility.validators
[AutoAPI] Rendering Data... [ 67%] src.haive.core.graph.node.stateful_node_config
[AutoAPI] Rendering Data... [ 67%] src.haive.core.graph.node.validation_router_v2
[AutoAPI] Rendering Data... [ 67%] src.haive.agents.research.storm.section_writer
[AutoAPI] Rendering Data... [ 67%] src.haive.agents.common.models.grade.composite
[AutoAPI] Rendering Data... [ 67%] src.haive.agents.base.mixins.persistence_mixin
[AutoAPI] Rendering Data... [ 67%] src.haive.agents.supervisor.dynamic_supervisor
[AutoAPI] Rendering Data... [ 67%] src.haive.agents.rag.multi_agent_rag.multi_rag
[AutoAPI] Rendering Data... [ 67%] src.haive.agents.rag.query_decomposition.agent
[AutoAPI] Rendering Data... [ 67%] src.haive.agents.rag.agentic.agentic_rag_agent
[AutoAPI] Rendering Data... [ 68%] src.haive.agents.reasoning_and_critique.tot.v2
[AutoAPI] Rendering Data... [ 68%] src.haive.agents.document_modifiers.tnt.models
[AutoAPI] Rendering Data... [ 68%] src.haive.agents.document_modifiers.base.state
[AutoAPI] Rendering Data... [ 68%] src.haive.agents.document_modifiers.summarizer
[AutoAPI] Rendering Data... [ 68%] src.haive.agents.document_modifiers.kg.kg_base
[AutoAPI] Rendering Data... [ 68%] src.haive.agents.multi.enhanced_parallel_agent
[AutoAPI] Rendering Data... [ 68%] src.haive.agents.multi.enhanced_multi_agent_v3
[AutoAPI] Rendering Data... [ 68%] src.haive.agents.multi.enhanced_multi_agent_v4
[AutoAPI] Rendering Data... [ 68%] src.haive.agents.memory_v2.simple_memory_agent
[AutoAPI] Rendering Data... [ 68%] src.haive.tools.tools.toolkits.google_calendar
[AutoAPI] Rendering Data... [ 68%] src.haive.tools.tools.toolkits.yugiioh_toolkit
[AutoAPI] Rendering Data... [ 68%] src.haive.tools.tools.toolkits.citydsk_toolkit
[AutoAPI] Rendering Data... [ 68%] src.haive.tools.tools.toolkits.mongodb_toolkit
[AutoAPI] Rendering Data... [ 68%] src.haive.tools.tools.toolkits.clickup_toolkit
[AutoAPI] Rendering Data... [ 68%] src.haive.tools.tools.toolkits.rps_101_toolkit
[AutoAPI] Rendering Data... [ 69%] src.haive.tools.tools.toolkits.amadues_toolkit
[AutoAPI] Rendering Data... [ 69%] src.haive.tools.tools.toolkits.polygon_toolkit
[AutoAPI] Rendering Data... [ 69%] src.haive.tools.tools.toolkits.dev.shell.shell
[AutoAPI] Rendering Data... [ 69%] src.haive.games.mastermind.configurable_config
[AutoAPI] Rendering Data... [ 69%] src.haive.games.framework.multi_player.factory
[AutoAPI] Rendering Data... [ 69%] src.haive.games.single_player.flow_free.config
[AutoAPI] Rendering Data... [ 69%] src.haive.games.single_player.flow_free.models
[AutoAPI] Rendering Data... [ 69%] src.haive.games.battleship.configurable_config
[AutoAPI] Rendering Data... [ 69%] src.haive.core.models.llm.providers.huggingface
[AutoAPI] Rendering Data... [ 69%] src.haive.core.models.embeddings.provider_types
[AutoAPI] Rendering Data... [ 69%] src.haive.core.engine.document.universal_loader
[AutoAPI] Rendering Data... [ 69%] src.haive.core.engine.document.loaders.strategy
[AutoAPI] Rendering Data... [ 69%] src.haive.core.engine.document.loaders.registry
[AutoAPI] Rendering Data... [ 69%] src.haive.core.engine.document.loaders.base_new
[AutoAPI] Rendering Data... [ 69%] src.haive.core.engine.document.loaders.adapters
[AutoAPI] Rendering Data... [ 70%] src.haive.core.engine.document.loaders.specific
[AutoAPI] Rendering Data... [ 70%] src.haive.core.engine.document.splitters.engine
[AutoAPI] Rendering Data... [ 70%] src.haive.core.engine.agent.persistence.manager
[AutoAPI] Rendering Data... [ 70%] src.haive.core.schema.preserve_messages_reducer
[AutoAPI] Rendering Data... [ 70%] src.haive.core.graph.node.parser_node_config_v2
[AutoAPI] Rendering Data... [ 70%] src.haive.agents.research.perplexity.pro_search
[AutoAPI] Rendering Data... [ 70%] src.haive.agents.research.open_perplexity.state
[AutoAPI] Rendering Data... [ 70%] src.haive.agents.reflection.message_transformer
[AutoAPI] Rendering Data... [ 70%] src.haive.agents.base.agent_with_token_tracking
[AutoAPI] Rendering Data... [ 70%] src.haive.agents.discovery.selection_strategies
[AutoAPI] Rendering Data... [ 70%] src.haive.agents.supervisor.dynamic_multi_agent
[AutoAPI] Rendering Data... [ 70%] src.haive.agents.supervisor.dynamic_agent_tools
[AutoAPI] Rendering Data... [ 70%] src.haive.agents.supervisor.registry_supervisor
[AutoAPI] Rendering Data... [ 70%] src.haive.agents.planning.plan_execute_v3.state
[AutoAPI] Rendering Data... [ 70%] src.haive.agents.planning.plan_execute_v3.agent
[AutoAPI] Rendering Data... [ 70%] src.haive.agents.planning.llm_compiler_v3.state
[AutoAPI] Rendering Data... [ 71%] src.haive.agents.planning.llm_compiler_v3.agent
[AutoAPI] Rendering Data... [ 71%] src.haive.agents.simple.enhanced_simple_minimal
[AutoAPI] Rendering Data... [ 71%] src.haive.agents.rag.agentic_router.agent_chain
[AutoAPI] Rendering Data... [ 71%] src.haive.agents.rag.query_planning.agent_chain
[AutoAPI] Rendering Data... [ 71%] src.haive.agents.reasoning_and_critique.lats.v2
[AutoAPI] Rendering Data... [ 71%] src.haive.agents.document_modifiers.tnt.engines
[AutoAPI] Rendering Data... [ 71%] src.haive.agents.document_modifiers.base.models
[AutoAPI] Rendering Data... [ 71%] src.haive.agents.memory.multi_agent_coordinator
[AutoAPI] Rendering Data... [ 71%] src.haive.agents.memory.agentic_rag_coordinator
[AutoAPI] Rendering Data... [ 71%] src.haive.agents.memory.search.pro_search.agent
[AutoAPI] Rendering Data... [ 71%] src.haive.agents.conversation.round_robin.agent
[AutoAPI] Rendering Data... [ 71%] src.haive.agents.experiments.dynamic_supervisor
[AutoAPI] Rendering Data... [ 71%] src.haive.dataflow.persistence.supabase_adapter
[AutoAPI] Rendering Data... [ 71%] src.haive.dataflow.utils.vault_migration_script
[AutoAPI] Rendering Data... [ 71%] src.haive.games.tic_tac_toe.configurable_config
[AutoAPI] Rendering Data... [ 72%] src.haive.games.core.agent.generic_player_agent
[AutoAPI] Rendering Data... [ 72%] src.haive.games.single_player.flow_free.engines
[AutoAPI] Rendering Data... [ 72%] src.haive.mcp.integration.aug_llm_mcp_extension
[AutoAPI] Rendering Data... [ 72%] src.haive.mcp.installers.safe_pattern_installer
[AutoAPI] Rendering Data... [ 72%] src.haive.mcp.downloader.github_mass_downloader
[AutoAPI] Rendering Data... [ 72%] src.haive.core.persistence.store.wrappers.memory
[AutoAPI] Rendering Data... [ 72%] src.haive.core.engine.document.transformers.base
[AutoAPI] Rendering Data... [ 72%] src.haive.core.engine.document.loaders.base.base
[AutoAPI] Rendering Data... [ 72%] src.haive.core.schema.prebuilt.multi_agent_state
[AutoAPI] Rendering Data... [ 72%] src.haive.core.graph.node.composer.field_mapping
[AutoAPI] Rendering Data... [ 72%] src.haive.core.graph.node.composer.path_resolver
[AutoAPI] Rendering Data... [ 72%] src.haive.core.graph.state_graph.components.node
[AutoAPI] Rendering Data... [ 72%] src.haive.agents.research.open_perplexity.config
[AutoAPI] Rendering Data... [ 72%] src.haive.agents.research.open_perplexity.models
[AutoAPI] Rendering Data... [ 72%] src.haive.agents.common.models.grade.qualitative
[AutoAPI] Rendering Data... [ 73%] src.haive.agents.discovery.dynamic_tool_selector
[AutoAPI] Rendering Data... [ 73%] src.haive.agents.supervisor.compatibility_bridge
[AutoAPI] Rendering Data... [ 73%] src.haive.agents.planning.langgraph_plan_execute
[AutoAPI] Rendering Data... [ 73%] src.haive.agents.planning.plan_and_execute_multi
[AutoAPI] Rendering Data... [ 73%] src.haive.agents.planning.plan_execute_v3.config
[AutoAPI] Rendering Data... [ 73%] src.haive.agents.planning.plan_execute_v3.models
[AutoAPI] Rendering Data... [ 73%] src.haive.agents.planning.rewoo.models.join_step
[AutoAPI] Rendering Data... [ 73%] src.haive.agents.planning.rewoo.models.tool_step
[AutoAPI] Rendering Data... [ 73%] src.haive.agents.planning.llm_compiler_v3.config
[AutoAPI] Rendering Data... [ 73%] src.haive.agents.planning.llm_compiler_v3.models
[AutoAPI] Rendering Data... [ 73%] src.haive.agents.simple.enhanced_simple_agent_v2
[AutoAPI] Rendering Data... [ 73%] src.haive.agents.rag.hallucination_grading.agent
[AutoAPI] Rendering Data... [ 73%] src.haive.agents.document_loader.directory.agent
[AutoAPI] Rendering Data... [ 73%] src.haive.agents.document_modifiers.tnt.branches
[AutoAPI] Rendering Data... [ 73%] src.haive.agents.multi.enhanced_sequential_agent
[AutoAPI] Rendering Data... [ 74%] src.haive.agents.multi.enhanced_supervisor_agent
[AutoAPI] Rendering Data... [ 74%] src.haive.agents.multi.archive.configurable_base
[AutoAPI] Rendering Data... [ 74%] src.haive.agents.memory.search.pro_search.models
[AutoAPI] Rendering Data... [ 74%] src.haive.agents.memory_v2.standalone_rag_memory
[AutoAPI] Rendering Data... [ 74%] src.haive.agents.memory_v2.memory_state_original
[AutoAPI] Rendering Data... [ 74%] src.haive.tools.tools.dalle_image_generator_tool
[AutoAPI] Rendering Data... [ 74%] src.haive.tools.tools.toolkits.poetry_db_toolkit
[AutoAPI] Rendering Data... [ 74%] src.haive.dataflow.api.routes.tools_routes_fixed
[AutoAPI] Rendering Data... [ 74%] src.haive.dataflow.importers.embeddings_importer
[AutoAPI] Rendering Data... [ 74%] src.haive.games.tic_tac_toe.configurable_engines
[AutoAPI] Rendering Data... [ 74%] src.haive.mcp.complete_mcp_with_parent_retriever
[AutoAPI] Rendering Data... [ 74%] src.haive.mcp.installers.advanced_code_installer
[AutoAPI] Rendering Data... [ 74%] src.haive.core.common.models.dynamic_choice_model
[AutoAPI] Rendering Data... [ 74%] src.haive.core.schema.compatibility.compatibility
[AutoAPI] Rendering Data... [ 74%] src.haive.core.schema.compatibility.field_mapping
[AutoAPI] Rendering Data... [ 75%] src.haive.core.graph.node.routing_validation_node
[AutoAPI] Rendering Data... [ 75%] src.haive.core.graph.node.unified_validation_node
[AutoAPI] Rendering Data... [ 75%] src.haive.core.graph.state_graph.graph_visualizer
[AutoAPI] Rendering Data... [ 75%] src.haive.agents.research.storm.outline_generator
[AutoAPI] Rendering Data... [ 75%] src.haive.agents.research.open_perplexity.prompts
[AutoAPI] Rendering Data... [ 75%] src.haive.agents.common.models.task_analysis.base
[AutoAPI] Rendering Data... [ 75%] src.haive.agents.common.models.grade.letter_grade
[AutoAPI] Rendering Data... [ 75%] src.haive.agents.supervisor.integrated_supervisor
[AutoAPI] Rendering Data... [ 75%] src.haive.agents.supervisor.dynamic_executor_node
[AutoAPI] Rendering Data... [ 75%] src.haive.agents.planning.plan_and_execute.simple
[AutoAPI] Rendering Data... [ 75%] src.haive.agents.planning.plan_execute_v3.engines
[AutoAPI] Rendering Data... [ 75%] src.haive.agents.planning.plan_execute_v3.prompts
[AutoAPI] Rendering Data... [ 75%] src.haive.agents.planning.llm_compiler_v3.prompts
[AutoAPI] Rendering Data... [ 75%] src.haive.agents.rag.common.hallucination_graders
[AutoAPI] Rendering Data... [ 75%] src.haive.agents.reasoning_and_critique.reflexion
[AutoAPI] Rendering Data... [ 76%] src.haive.agents.reasoning_and_critique.tot.agent
[AutoAPI] Rendering Data... [ 76%] src.haive.agents.multi.enhanced_clean_multi_agent
[AutoAPI] Rendering Data... [ 76%] src.haive.agents.memory.search.quick_search.agent
[AutoAPI] Rendering Data... [ 76%] src.haive.agents.conversation.collaberative.state
[AutoAPI] Rendering Data... [ 76%] src.haive.agents.conversation.collaberative.agent
[AutoAPI] Rendering Data... [ 76%] src.haive.agents.conversation.social_media.models
[AutoAPI] Rendering Data... [ 76%] src.haive.agents.memory_v2.long_term_memory_agent
[AutoAPI] Rendering Data... [ 76%] src.haive.tools.tools.toolkits.dataforseo_toolkit
[AutoAPI] Rendering Data... [ 76%] src.haive.dataflow.api.routes.conversation_routes
[AutoAPI] Rendering Data... [ 76%] src.haive.games.framework.base.template_generator
[AutoAPI] Rendering Data... [ 76%] src.haive.games.fox_and_geese.configurable_config
[AutoAPI] Rendering Data... [ 76%] src.haive.games.single_player.twenty_fourty_eight
[AutoAPI] Rendering Data... [ 76%] src.haive.core.common.mixins.prompt_template_mixin
[AutoAPI] Rendering Data... [ 76%] src.haive.core.common.mixins.state_interface_mixin
[AutoAPI] Rendering Data... [ 76%] src.haive.core.common.mixins.general.serialization
[AutoAPI] Rendering Data... [ 77%] src.haive.core.persistence.postgres_saver_override
[AutoAPI] Rendering Data... [ 77%] src.haive.core.persistence.store.wrappers.postgres
[AutoAPI] Rendering Data... [ 77%] src.haive.core.models.llm.export_llm_models_to_csv
[AutoAPI] Rendering Data... [ 77%] src.haive.core.types.general.programming_languages
[AutoAPI] Rendering Data... [ 77%] src.haive.core.engine.document.transformers.engine
[AutoAPI] Rendering Data... [ 77%] src.haive.core.engine.document.loaders.source_base
[AutoAPI] Rendering Data... [ 77%] src.haive.core.engine.document.loaders.auto_loader
[AutoAPI] Rendering Data... [ 77%] src.haive.core.schema.composer.field.field_manager
[AutoAPI] Rendering Data... [ 77%] src.haive.core.graph.node.stateful_validation_node
[AutoAPI] Rendering Data... [ 77%] src.haive.core.graph.state_graph.pattern_decorator
[AutoAPI] Rendering Data... [ 77%] src.haive.core.graph.state_graph.components.branch
[AutoAPI] Rendering Data... [ 77%] src.haive.agents.reflection.multi_agent_reflection
[AutoAPI] Rendering Data... [ 77%] src.haive.agents.rag.simple.multi_agent_simple_rag
[AutoAPI] Rendering Data... [ 77%] src.haive.agents.rag.multi_agent_rag.compatibility
[AutoAPI] Rendering Data... [ 77%] src.haive.agents.reasoning_and_critique.reflection
[AutoAPI] Rendering Data... [ 78%] src.haive.agents.reasoning_and_critique.tot.config
[AutoAPI] Rendering Data... [ 78%] src.haive.agents.reasoning_and_critique.tot.models
[AutoAPI] Rendering Data... [ 78%] src.haive.agents.multi.enhanced_dynamic_supervisor
[AutoAPI] Rendering Data... [ 78%] src.haive.agents.memory.search.deep_research.agent
[AutoAPI] Rendering Data... [ 78%] src.haive.agents.memory.search.quick_search.models
[AutoAPI] Rendering Data... [ 78%] src.haive.agents.memory_v2.time_weighted_retriever
[AutoAPI] Rendering Data... [ 78%] src.haive.agents.patterns.simple_rag_agent_pattern
[AutoAPI] Rendering Data... [ 78%] src.haive.tools.tools.toolkits.openlibrary_toolkit
[AutoAPI] Rendering Data... [ 78%] src.haive.games.single_player.towers_of_hanoi.move
[AutoAPI] Rendering Data... [ 78%] src.haive.mcp.enhanced_parent_self_query_retriever
[AutoAPI] Rendering Data... [ 78%] src.haive.core.engine.document.loaders.auto_factory
[AutoAPI] Rendering Data... [ 78%] src.haive.core.engine.document.loaders.specific.web
[AutoAPI] Rendering Data... [ 78%] src.haive.core.schema.prebuilt.messages.token_usage
[AutoAPI] Rendering Data... [ 78%] src.haive.core.graph.node.validation_node_config_v2
[AutoAPI] Rendering Data... [ 78%] src.haive.core.graph.node.composer.update_functions
[AutoAPI] Rendering Data... [ 79%] src.haive.agents.common.utils.pydantic_prompt_utils
[AutoAPI] Rendering Data... [ 79%] src.haive.agents.base.agent_structured_output_mixin
[AutoAPI] Rendering Data... [ 79%] src.haive.agents.supervisor.choice_model_supervisor
[AutoAPI] Rendering Data... [ 79%] src.haive.agents.planning.plan_and_execute.v2.state
[AutoAPI] Rendering Data... [ 79%] src.haive.agents.planning.plan_and_execute.v2.agent
[AutoAPI] Rendering Data... [ 79%] src.haive.agents.rag.common.document_graders.models
[AutoAPI] Rendering Data... [ 79%] src.haive.agents.rag.common.query_constructors.hyde
[AutoAPI] Rendering Data... [ 79%] src.haive.agents.rag.factories.rag_workflow_factory
[AutoAPI] Rendering Data... [ 79%] src.haive.agents.rag.simple.answer_generator.models
[AutoAPI] Rendering Data... [ 79%] src.haive.agents.reasoning_and_critique.lats.config
[AutoAPI] Rendering Data... [ 79%] src.haive.agents.reasoning_and_critique.tot.engines
[AutoAPI] Rendering Data... [ 79%] src.haive.agents.reasoning_and_critique.tot.modular
[AutoAPI] Rendering Data... [ 79%] src.haive.agents.document_modifiers.kg.kg_map_merge
[AutoAPI] Rendering Data... [ 79%] src.haive.agents.multi.enhanced_multi_agent_generic
[AutoAPI] Rendering Data... [ 79%] src.haive.agents.multi.experiments.routing_patterns
[AutoAPI] Rendering Data... [ 80%] src.haive.agents.multi.experiments.list_multi_agent
[AutoAPI] Rendering Data... [ 80%] src.haive.agents.memory.search.deep_research.models
[AutoAPI] Rendering Data... [ 80%] src.haive.agents.memory_v2.integrated_memory_system
[AutoAPI] Rendering Data... [ 80%] src.haive.agents.memory_v2.react_memory_coordinator
[AutoAPI] Rendering Data... [ 80%] src.haive.agents.memory_v2.memory_models_standalone
[AutoAPI] Rendering Data... [ 80%] src.haive.agents.memory_v2.memory_state_with_tokens
[AutoAPI] Rendering Data... [ 80%] src.haive.agents.memory_v2.multi_memory_coordinator
[AutoAPI] Rendering Data... [ 80%] src.haive.agents.patterns.sequential_workflow_agent
[AutoAPI] Rendering Data... [ 80%] src.haive.tools.tools.toolkits.free_to_game_toolkit
[AutoAPI] Rendering Data... [ 80%] src.haive.tools.tools.toolkits.trip_advisor_toolkit
[AutoAPI] Rendering Data... [ 80%] src.haive.tools.tools.toolkits.dev.shell.permission
[AutoAPI] Rendering Data... [ 80%] src.haive.tools.tools.toolkits.dev.project_creation
[AutoAPI] Rendering Data... [ 80%] src.haive.dataflow.api.routes.tools_routes_enhanced
[AutoAPI] Rendering Data... [ 80%] src.haive.core.common.mixins.structured_output_mixin
[AutoAPI] Rendering Data... [ 80%] src.haive.core.engine.document.loaders.cache_manager
[AutoAPI] Rendering Data... [ 81%] src.haive.core.engine.document.loaders.path_analyzer
[AutoAPI] Rendering Data... [ 81%] src.haive.core.engine.document.loaders.auto_registry
[AutoAPI] Rendering Data... [ 81%] src.haive.core.engine.document.loaders.adapters.base
[AutoAPI] Rendering Data... [ 81%] src.haive.core.schema.composer.engine.engine_manager
[AutoAPI] Rendering Data... [ 81%] src.haive.core.graph.node.composer.extract_functions
[AutoAPI] Rendering Data... [ 81%] src.haive.agents.discovery.component_discovery_agent
[AutoAPI] Rendering Data... [ 81%] src.haive.agents.supervisor.dynamic_supervisor_fixed
[AutoAPI] Rendering Data... [ 81%] src.haive.agents.supervisor.clean_dynamic_supervisor
[AutoAPI] Rendering Data... [ 81%] src.haive.agents.planning.plan_and_execute.v2.models
[AutoAPI] Rendering Data... [ 81%] src.haive.agents.rag.common.query_constructors.flare
[AutoAPI] Rendering Data... [ 81%] src.haive.agents.rag.simple.answer_generator.prompts
[AutoAPI] Rendering Data... [ 81%] src.haive.agents.react_class.react_agent2.many_tools
[AutoAPI] Rendering Data... [ 81%] src.haive.agents.memory_v2.advanced_rag_memory_agent
[AutoAPI] Rendering Data... [ 81%] src.haive.agents.memory_v2.multi_react_memory_system
[AutoAPI] Rendering Data... [ 81%] src.haive.agents.memory_v2.conversation_memory_agent
[AutoAPI] Rendering Data... [ 82%] src.haive.tools.tools.toolkits.useless_facts_toolkit
[AutoAPI] Rendering Data... [ 82%] src.haive.dataflow.api.routes.agent_discovery_routes
[AutoAPI] Rendering Data... [ 82%] src.haive.dataflow.registry.providers.agent_provider
[AutoAPI] Rendering Data... [ 82%] src.haive.games.framework.multi_player.state_manager
[AutoAPI] Rendering Data... [ 82%] src.haive.core.common.mixins.dynamic_tool_route_mixin
[AutoAPI] Rendering Data... [ 82%] src.haive.core.engine.document.loaders.specific.cloud
[AutoAPI] Rendering Data... [ 82%] src.haive.core.schema.composer.engine.engine_detector
[AutoAPI] Rendering Data... [ 82%] src.haive.core.schema.prebuilt.tools.validation_state
[AutoAPI] Rendering Data... [ 82%] src.haive.core.schema.prebuilt.messages.compatibility
[AutoAPI] Rendering Data... [ 82%] src.haive.core.graph.state_graph.conversion.langgraph
[AutoAPI] Rendering Data... [ 82%] src.haive.agents.research.perplexity.pro_search.tasks
[AutoAPI] Rendering Data... [ 82%] src.haive.agents.research.storm.generate_perspectives
[AutoAPI] Rendering Data... [ 82%] src.haive.agents.common.models.task_analysis.analysis
[AutoAPI] Rendering Data... [ 82%] src.haive.agents.supervisor.proper_dynamic_supervisor
[AutoAPI] Rendering Data... [ 82%] src.haive.agents.supervisor.multi_agent_dynamic_state
[AutoAPI] Rendering Data... [ 83%] src.haive.agents.planning.plan_and_execute.v2.prompts
[AutoAPI] Rendering Data... [ 83%] src.haive.agents.rag.factories.compatible_rag_factory
[AutoAPI] Rendering Data... [ 83%] src.haive.agents.rag.utils.structured_output_enhancer
[AutoAPI] Rendering Data... [ 83%] src.haive.agents.reasoning_and_critique.self_discover
[AutoAPI] Rendering Data... [ 83%] src.haive.agents.reasoning_and_critique.logic.engines
[AutoAPI] Rendering Data... [ 83%] src.haive.agents.document_modifiers.kg.kg_base.models
[AutoAPI] Rendering Data... [ 83%] src.haive.agents.memory_v2.message_document_converter
[AutoAPI] Rendering Data... [ 83%] src.haive.agents.patterns.hybrid_multi_agent_patterns
[AutoAPI] Rendering Data... [ 83%] src.haive.tools.tools.toolkits.rick_and_morty_toolkit
[AutoAPI] Rendering Data... [ 83%] src.haive.tools.tools.toolkits.stack_exchange_toolkit
[AutoAPI] Rendering Data... [ 83%] src.haive.dataflow.registry.registries.model_registry
[AutoAPI] Rendering Data... [ 83%] src.haive.games.single_player.flow_free.state_manager
[AutoAPI] Rendering Data... [ 83%] src.haive.games.single_player.towers_of_hanoi.prompts
[AutoAPI] Rendering Data... [ 83%] src.haive.core.engine.document.loaders.sources.factory
[AutoAPI] Rendering Data... [ 83%] src.haive.core.schema.prebuilt.structured_output_state
[AutoAPI] Rendering Data... [ 84%] src.haive.core.graph.node.intelligent_multi_agent_node
[AutoAPI] Rendering Data... [ 84%] src.haive.core.graph.node.validation_node_with_routing
[AutoAPI] Rendering Data... [ 84%] src.haive.agents.research.perplexity.pro_search.models
[AutoAPI] Rendering Data... [ 84%] src.haive.agents.research.perplexity.pro_search.search
[AutoAPI] Rendering Data... [ 84%] src.haive.agents.common.models.task_analysis.branching
[AutoAPI] Rendering Data... [ 84%] src.haive.agents.supervisor.rebuild_dynamic_supervisor
[AutoAPI] Rendering Data... [ 84%] src.haive.agents.planning.p_and_e.enhanced_multi_agent
[AutoAPI] Rendering Data... [ 84%] src.haive.agents.document_modifiers.complex_extraction
[AutoAPI] Rendering Data... [ 84%] src.haive.agents.multi.enhanced_multi_agent_standalone
[AutoAPI] Rendering Data... [ 84%] src.haive.agents.patterns.react_with_structured_output
[AutoAPI] Rendering Data... [ 84%] src.haive.dataflow.registry.importers.litellm_importer
[AutoAPI] Rendering Data... [ 84%] src.haive.games.single_player.twenty_fourty_eight.game
[AutoAPI] Rendering Data... [ 84%] src.haive.core.engine.document.loaders.specific.web_api
[AutoAPI] Rendering Data... [ 84%] src.haive.core.engine.document.loaders.sources.registry
[AutoAPI] Rendering Data... [ 84%] src.haive.core.schema.prebuilt.dynamic_activation_state
[AutoAPI] Rendering Data... [ 85%] src.haive.core.graph.node.composer.node_schema_composer
[AutoAPI] Rendering Data... [ 85%] src.haive.agents.supervisor.internal_dynamic_supervisor
[AutoAPI] Rendering Data... [ 85%] src.haive.agents.rag.simple.enhanced_v3.retriever_agent
[AutoAPI] Rendering Data... [ 85%] src.haive.agents.rag.multi_agent_rag.enhanced_workflows
[AutoAPI] Rendering Data... [ 85%] src.haive.agents.rag.multi_agent_rag.advanced_workflows
[AutoAPI] Rendering Data... [ 85%] src.haive.agents.rag.multi_agent_rag.enhanced_multi_rag
[AutoAPI] Rendering Data... [ 85%] src.haive.agents.rag.multi_agent_rag.grading_components
[AutoAPI] Rendering Data... [ 85%] src.haive.agents.react_class.react_agent2.dynamic_agent
[AutoAPI] Rendering Data... [ 85%] src.haive.agents.memory_v2.standalone_memory_agent_free
[AutoAPI] Rendering Data... [ 85%] src.haive.agents.memory_v2.simple_memory_agent_deepseek
[AutoAPI] Rendering Data... [ 85%] src.haive.core.engine.document.loaders.specific.services
[AutoAPI] Rendering Data... [ 85%] src.haive.core.engine.document.loaders.specific.database
[AutoAPI] Rendering Data... [ 85%] src.haive.core.schema.compatibility.langchain_converters
[AutoAPI] Rendering Data... [ 85%] src.haive.core.graph.node.state_updating_validation_node
[AutoAPI] Rendering Data... [ 85%] src.haive.core.graph.state_graph.components.node_manager
[AutoAPI] Rendering Data... [ 86%] src.haive.core.graph.state_graph.components.edge_manager
[AutoAPI] Rendering Data... [ 86%] src.haive.agents.research.storm.related_topics_generator
[AutoAPI] Rendering Data... [ 86%] src.haive.agents.common.models.task_analysis.solvability
[AutoAPI] Rendering Data... [ 86%] src.haive.agents.reflection.message_transformer_posthook
[AutoAPI] Rendering Data... [ 86%] src.haive.agents.reasoning_and_critique.reflection.state
[AutoAPI] Rendering Data... [ 86%] src.haive.agents.reasoning_and_critique.reflection.agent
[AutoAPI] Rendering Data... [ 86%] src.haive.agents.reasoning_and_critique.self_discover.v2
[AutoAPI] Rendering Data... [ 86%] src.haive.agents.experiments.static_supervisor_with_sync
[AutoAPI] Rendering Data... [ 86%] src.haive.agents.experiments.dynamic_supervisor_enhanced
[AutoAPI] Rendering Data... [ 86%] src.haive.tools.tools.toolkits.financialdatasets_toolkit
[AutoAPI] Rendering Data... [ 86%] src.haive.dataflow.registry.utils.vault_migration_script
[AutoAPI] Rendering Data... [ 86%] src.haive.core.schema.prebuilt.flexible_multi_agent_state
[AutoAPI] Rendering Data... [ 86%] src.haive.core.schema.prebuilt.tool_state_with_validation
[AutoAPI] Rendering Data... [ 86%] src.haive.core.schema.prebuilt.messages.token_usage_mixin
[AutoAPI] Rendering Data... [ 86%] src.haive.core.graph.node.composer.advanced_node_composer
[AutoAPI] Rendering Data... [ 87%] src.haive.agents.supervisor.dynamic_activation_supervisor
[AutoAPI] Rendering Data... [ 87%] src.haive.agents.rag.multi_agent_rag.additional_workflows
[AutoAPI] Rendering Data... [ 87%] src.haive.agents.rag.multi_agent_rag.graded_rag_workflows
[AutoAPI] Rendering Data... [ 87%] src.haive.agents.reasoning_and_critique.reflection.config
[AutoAPI] Rendering Data... [ 87%] src.haive.agents.reasoning_and_critique.reflection.models
[AutoAPI] Rendering Data... [ 87%] src.haive.agents.document_modifiers.summarizer.map_branch
[AutoAPI] Rendering Data... [ 87%] src.haive.agents.patterns.react_structured_agent_variants
[AutoAPI] Rendering Data... [ 87%] src.haive.tools.tools.toolkits.chuck_norris_jokes_toolkit
[AutoAPI] Rendering Data... [ 87%] src.haive.dataflow.registry.importers.embeddings_importer
[AutoAPI] Rendering Data... [ 87%] src.haive.core.engine.document.loaders.specific.web_social
[AutoAPI] Rendering Data... [ 87%] src.haive.core.engine.document.loaders.specific.files_text
[AutoAPI] Rendering Data... [ 87%] src.haive.core.engine.document.loaders.specific.files_code
[AutoAPI] Rendering Data... [ 87%] src.haive.core.engine.document.loaders.specific.files_data
[AutoAPI] Rendering Data... [ 87%] src.haive.core.engine.document.loaders.sources.web_sources
[AutoAPI] Rendering Data... [ 87%] src.haive.core.engine.document.loaders.sources.source_base
[AutoAPI] Rendering Data... [ 88%] src.haive.core.schema.prebuilt.validation_aware_tool_state
[AutoAPI] Rendering Data... [ 88%] src.haive.core.graph.state_graph.components.branch_manager
[AutoAPI] Rendering Data... [ 88%] src.haive.core.graph.state_graph.components.base_component
[AutoAPI] Rendering Data... [ 88%] src.haive.agents.rag.common.document_graders.binary_grader
[AutoAPI] Rendering Data... [ 88%] src.haive.agents.rag.multi_agent_rag.specialized_workflows
[AutoAPI] Rendering Data... [ 88%] src.haive.agents.multi.experiments.proper_list_multi_agent
[AutoAPI] Rendering Data... [ 88%] src.haive.tools.tools.toolkits.dev.project_creation.github
[AutoAPI] Rendering Data... [ 88%] src.haive.dataflow.api.routes.agent_discovery_routes_fixed
[AutoAPI] Rendering Data... [ 88%] src.haive.core.engine.document.loaders.specific.files_media
[AutoAPI] Rendering Data... [ 88%] src.haive.core.engine.document.loaders.sources.file_sources
[AutoAPI] Rendering Data... [ 88%] src.haive.core.engine.document.loaders.sources.source_types
[AutoAPI] Rendering Data... [ 88%] src.haive.core.engine.document.loaders.sources.bulk_sources
[AutoAPI] Rendering Data... [ 88%] src.haive.core.graph.node.composer.integrated_node_composer
[AutoAPI] Rendering Data... [ 88%] src.haive.agents.rag.multi_agent_rag.complete_rag_workflows
[AutoAPI] Rendering Data... [ 88%] src.haive.agents.rag.multi_agent_rag.enhanced_state_schemas
[AutoAPI] Rendering Data... [ 89%] src.haive.agents.reasoning_and_critique.self_discover.agent
[AutoAPI] Rendering Data... [ 89%] src.haive.agents.patterns.sequential_with_structured_output
[AutoAPI] Rendering Data... [ 89%] src.haive.core.engine.document.loaders.specific.web_advanced
[AutoAPI] Rendering Data... [ 89%] src.haive.core.engine.document.loaders.specific.files_office
[AutoAPI] Rendering Data... [ 89%] src.haive.core.engine.document.loaders.sources.final_sources
[AutoAPI] Rendering Data... [ 89%] src.haive.core.engine.retriever.providers.YouRetrieverConfig
[AutoAPI] Rendering Data... [ 89%] src.haive.core.engine.retriever.providers.KNNRetrieverConfig
[AutoAPI] Rendering Data... [ 89%] src.haive.core.engine.retriever.providers.SVMRetrieverConfig
[AutoAPI] Rendering Data... [ 89%] src.haive.core.engine.retriever.providers.ZepRetrieverConfig
[AutoAPI] Rendering Data... [ 89%] src.haive.agents.research.perplexity.pro_search.tasks.models
[AutoAPI] Rendering Data... [ 89%] src.haive.agents.common.models.task_analysis.parallelization
[AutoAPI] Rendering Data... [ 89%] src.haive.agents.rag.factories.compatible_rag_factory_simple
[AutoAPI] Rendering Data... [ 89%] src.haive.agents.rag.multi_agent_rag.graded_rag_workflows_v2
[AutoAPI] Rendering Data... [ 89%] src.haive.agents.document_modifiers.complex_extraction.agent
[AutoAPI] Rendering Data... [ 89%] src.haive.core.engine.document.loaders.specific.file_advanced
[AutoAPI] Rendering Data... [ 90%] src.haive.core.engine.document.loaders.sources.implementation
[AutoAPI] Rendering Data... [ 90%] src.haive.core.engine.retriever.providers.BM25RetrieverConfig
[AutoAPI] Rendering Data... [ 90%] src.haive.core.engine.embedding.providers.FakeEmbeddingConfig
[AutoAPI] Rendering Data... [ 90%] src.haive.agents.research.perplexity.pro_search.tasks.prompts
[AutoAPI] Rendering Data... [ 90%] src.haive.agents.research.perplexity.pro_search.search.models
[AutoAPI] Rendering Data... [ 90%] src.haive.agents.supervisor.dynamic_tool_discovery_supervisor
[AutoAPI] Rendering Data... [ 90%] src.haive.agents.rag.multi_agent_rag.specialized_workflows_v2
[AutoAPI] Rendering Data... [ 90%] src.haive.agents.reasoning_and_critique.self_discover.adapter
[AutoAPI] Rendering Data... [ 90%] src.haive.agents.multi.experiments.implementations.clean_base
[AutoAPI] Rendering Data... [ 90%] src.haive.dataflow.api.routes.agent_discovery_routes_enhanced
[AutoAPI] Rendering Data... [ 90%] src.haive.core.persistence.postgres_saver_with_thread_creation
[AutoAPI] Rendering Data... [ 90%] src.haive.core.engine.document.loaders.sources.chat_gpt_loader
[AutoAPI] Rendering Data... [ 90%] src.haive.core.engine.retriever.providers.TFIDFRetrieverConfig
[AutoAPI] Rendering Data... [ 90%] src.haive.core.engine.retriever.providers.VespaRetrieverConfig
[AutoAPI] Rendering Data... [ 90%] src.haive.core.engine.retriever.providers.ArceeRetrieverConfig
[AutoAPI] Rendering Data... [ 90%] src.haive.core.engine.retriever.providers.MetalRetrieverConfig
[AutoAPI] Rendering Data... [ 91%] src.haive.core.engine.retriever.providers.ArxivRetrieverConfig
[AutoAPI] Rendering Data... [ 91%] src.haive.core.graph.state_graph.components.modular_base_graph
[AutoAPI] Rendering Data... [ 91%] src.haive.agents.research.perplexity.pro_search.search.prompts
[AutoAPI] Rendering Data... [ 91%] src.haive.agents.supervisor.dynamic_agent_discovery_supervisor
[AutoAPI] Rendering Data... [ 91%] src.haive.agents.rag.simple.enhanced_v3.answer_generator_agent
[AutoAPI] Rendering Data... [ 91%] src.haive.agents.rag.multi_agent_rag.simple_enhanced_workflows
[AutoAPI] Rendering Data... [ 91%] src.haive.agents.reasoning_and_critique.self_discover.selector
[AutoAPI] Rendering Data... [ 91%] src.haive.agents.reasoning_and_critique.self_discover.executor
[AutoAPI] Rendering Data... [ 91%] src.haive.agents.reasoning_and_critique.self_discover.v2.state
[AutoAPI] Rendering Data... [ 91%] src.haive.agents.reasoning_and_critique.self_discover.v2.agent
[AutoAPI] Rendering Data... [ 91%] src.haive.agents.document_modifiers.kg.kg_iterative_refinement
[AutoAPI] Rendering Data... [ 91%] src.haive.agents.multi.experiments.implementations.proper_base
[AutoAPI] Rendering Data... [ 91%] src.haive.agents.patterns.react_structured_reflection_patterns
[AutoAPI] Rendering Data... [ 91%] src.haive.core.engine.document.loaders.sources.extended_sources
[AutoAPI] Rendering Data... [ 91%] src.haive.core.engine.document.loaders.sources.business_sources
[AutoAPI] Rendering Data... [ 92%] src.haive.core.engine.document.loaders.sources.database_sources
[AutoAPI] Rendering Data... [ 92%] src.haive.core.engine.vectorstore.providers.PGVectorStoreConfig
[AutoAPI] Rendering Data... [ 92%] src.haive.core.engine.retriever.providers.MilvusRetrieverConfig
[AutoAPI] Rendering Data... [ 92%] src.haive.core.engine.retriever.providers.MergerRetrieverConfig
[AutoAPI] Rendering Data... [ 92%] src.haive.core.engine.retriever.providers.KendraRetrieverConfig
[AutoAPI] Rendering Data... [ 92%] src.haive.core.engine.retriever.providers.PubMedRetrieverConfig
[AutoAPI] Rendering Data... [ 92%] src.haive.core.engine.embedding.providers.OllamaEmbeddingConfig
[AutoAPI] Rendering Data... [ 92%] src.haive.core.engine.embedding.providers.OpenAIEmbeddingConfig
[AutoAPI] Rendering Data... [ 92%] src.haive.core.engine.embedding.providers.CohereEmbeddingConfig
[AutoAPI] Rendering Data... [ 92%] src.haive.agents.reasoning_and_critique.self_discover.v2.models
[AutoAPI] Rendering Data... [ 92%] src.haive.agents.document_modifiers.summarizer.map_branch.state
[AutoAPI] Rendering Data... [ 92%] src.haive.agents.document_modifiers.summarizer.map_branch.agent
[AutoAPI] Rendering Data... [ 92%] src.haive.core.engine.document.loaders.specific.files_scientific
[AutoAPI] Rendering Data... [ 92%] src.haive.core.engine.document.loaders.sources.analytics_sources
[AutoAPI] Rendering Data... [ 92%] src.haive.core.engine.document.loaders.sources.enhanced_registry
[AutoAPI] Rendering Data... [ 93%] src.haive.core.engine.document.loaders.sources.messaging_sources
[AutoAPI] Rendering Data... [ 93%] src.haive.core.engine.document.loaders.sources.essential_sources
[AutoAPI] Rendering Data... [ 93%] src.haive.core.engine.retriever.providers.BedrockRetrieverConfig
[AutoAPI] Rendering Data... [ 93%] src.haive.core.engine.retriever.providers.AskNewsRetrieverConfig
[AutoAPI] Rendering Data... [ 93%] src.haive.core.graph.state_graph.components.architecture_summary
[AutoAPI] Rendering Data... [ 93%] src.haive.agents.reasoning_and_critique.self_discover.structurer
[AutoAPI] Rendering Data... [ 93%] src.haive.agents.reasoning_and_critique.self_discover.v2.prompts
[AutoAPI] Rendering Data... [ 93%] src.haive.core.engine.document.loaders.specific.database_advanced
[AutoAPI] Rendering Data... [ 93%] src.haive.core.engine.document.loaders.sources.additional_sources
[AutoAPI] Rendering Data... [ 93%] src.haive.core.engine.document.loaders.sources.completion_sources
[AutoAPI] Rendering Data... [ 93%] src.haive.core.engine.retriever.providers.EnsembleRetrieverConfig
[AutoAPI] Rendering Data... [ 93%] src.haive.core.engine.retriever.providers.ZepCloudRetrieverConfig
[AutoAPI] Rendering Data... [ 93%] src.haive.core.engine.retriever.providers.NeuralDBRetrieverConfig
[AutoAPI] Rendering Data... [ 93%] src.haive.core.engine.retriever.providers.DocArrayRetrieverConfig
[AutoAPI] Rendering Data... [ 93%] src.haive.agents.rag.common.document_graders.comprehensive_grader
[AutoAPI] Rendering Data... [ 94%] src.haive.agents.document_modifiers.summarizer.map_branch.prompts
[AutoAPI] Rendering Data... [ 94%] src.haive.agents.multi.experiments.implementations.multi_agent_v2
[AutoAPI] Rendering Data... [ 94%] src.haive.core.engine.document.loaders.sources.specialized_sources
[AutoAPI] Rendering Data... [ 94%] src.haive.core.engine.vectorstore.providers.MarqoVectorStoreConfig
[AutoAPI] Rendering Data... [ 94%] src.haive.core.engine.vectorstore.providers.AnnoyVectorStoreConfig
[AutoAPI] Rendering Data... [ 94%] src.haive.core.engine.vectorstore.providers.Neo4jVectorStoreConfig
[AutoAPI] Rendering Data... [ 94%] src.haive.core.engine.vectorstore.providers.RedisVectorStoreConfig
[AutoAPI] Rendering Data... [ 94%] src.haive.core.engine.vectorstore.providers.FAISSVectorStoreConfig
[AutoAPI] Rendering Data... [ 94%] src.haive.core.engine.retriever.providers.SelfQueryRetrieverConfig
[AutoAPI] Rendering Data... [ 94%] src.haive.core.engine.retriever.providers.WikipediaRetrieverConfig
[AutoAPI] Rendering Data... [ 94%] src.haive.core.engine.retriever.providers.CohereRagRetrieverConfig
[AutoAPI] Rendering Data... [ 94%] src.haive.core.engine.document.loaders.specific.web_github_enhanced
[AutoAPI] Rendering Data... [ 94%] src.haive.core.engine.document.loaders.sources.final_missing_source
[AutoAPI] Rendering Data... [ 94%] src.haive.core.engine.vectorstore.providers.ZillizVectorStoreConfig
[AutoAPI] Rendering Data... [ 94%] src.haive.core.engine.vectorstore.providers.ChromaVectorStoreConfig
[AutoAPI] Rendering Data... [ 95%] src.haive.core.engine.vectorstore.providers.QdrantVectorStoreConfig
[AutoAPI] Rendering Data... [ 95%] src.haive.core.engine.vectorstore.providers.MilvusVectorStoreConfig
[AutoAPI] Rendering Data... [ 95%] src.haive.core.engine.retriever.providers.MultiQueryRetrieverConfig
[AutoAPI] Rendering Data... [ 95%] src.haive.core.engine.retriever.providers.LlamaIndexRetrieverConfig
[AutoAPI] Rendering Data... [ 95%] src.haive.agents.reasoning_and_critique.self_discover.adapter.agent
[AutoAPI] Rendering Data... [ 95%] src.haive.agents.document_modifiers.summarizer.iterative_refinement
[AutoAPI] Rendering Data... [ 95%] src.haive.tools.tools.toolkits.dev.shell.background_process_manager
[AutoAPI] Rendering Data... [ 95%] src.haive.core.engine.document.loaders.sources.communication_sources
[AutoAPI] Rendering Data... [ 95%] src.haive.core.engine.document.loaders.sources.cloud_storage_sources
[AutoAPI] Rendering Data... [ 95%] src.haive.core.engine.vectorstore.providers.VectaraVectorStoreConfig
[AutoAPI] Rendering Data... [ 95%] src.haive.core.engine.vectorstore.providers.USearchVectorStoreConfig
[AutoAPI] Rendering Data... [ 95%] src.haive.core.engine.vectorstore.providers.LanceDBVectorStoreConfig
[AutoAPI] Rendering Data... [ 95%] src.haive.core.engine.vectorstore.providers.SKLearnVectorStoreConfig
[AutoAPI] Rendering Data... [ 95%] src.haive.core.engine.retriever.providers.MultiVectorRetrieverConfig
[AutoAPI] Rendering Data... [ 95%] src.haive.core.engine.retriever.providers.WebResearchRetrieverConfig
[AutoAPI] Rendering Data... [ 96%] src.haive.core.engine.embedding.providers.AzureOpenAIEmbeddingConfig
[AutoAPI] Rendering Data... [ 96%] src.haive.core.engine.embedding.providers.HuggingFaceEmbeddingConfig
[AutoAPI] Rendering Data... [ 96%] src.haive.agents.rag.common.query_constructors.hyde.enhanced_prompts
[AutoAPI] Rendering Data... [ 96%] src.haive.agents.reasoning_and_critique.self_discover.fixed_selector
[AutoAPI] Rendering Data... [ 96%] src.haive.agents.reasoning_and_critique.self_discover.executor.agent
[AutoAPI] Rendering Data... [ 96%] src.haive.agents.reasoning_and_critique.self_discover.adapter.models
[AutoAPI] Rendering Data... [ 96%] src.haive.agents.reasoning_and_critique.self_discover.selector.agent
[AutoAPI] Rendering Data... [ 96%] src.haive.agents.document_modifiers.kg.kg_iterative_refinement.agent
[AutoAPI] Rendering Data... [ 96%] src.haive.agents.multi.experiments.implementations.clean_multi_agent
[AutoAPI] Rendering Data... [ 96%] src.haive.core.engine.vectorstore.providers.InMemoryVectorStoreConfig
[AutoAPI] Rendering Data... [ 96%] src.haive.core.engine.vectorstore.providers.WeaviateVectorStoreConfig
[AutoAPI] Rendering Data... [ 96%] src.haive.core.engine.vectorstore.providers.SupabaseVectorStoreConfig
[AutoAPI] Rendering Data... [ 96%] src.haive.core.engine.vectorstore.providers.PineconeVectorStoreConfig
[AutoAPI] Rendering Data... [ 96%] src.haive.core.engine.vectorstore.providers.DocArrayVectorStoreConfig
[AutoAPI] Rendering Data... [ 96%] src.haive.agents.reasoning_and_critique.self_discover.executor.models
[AutoAPI] Rendering Data... [ 97%] src.haive.agents.reasoning_and_critique.self_discover.adapter.prompts
[AutoAPI] Rendering Data... [ 97%] src.haive.agents.reasoning_and_critique.self_discover.selector.models
[AutoAPI] Rendering Data... [ 97%] src.haive.core.engine.vectorstore.providers.CassandraVectorStoreConfig
[AutoAPI] Rendering Data... [ 97%] src.haive.core.engine.vectorstore.providers.TypesenseVectorStoreConfig
[AutoAPI] Rendering Data... [ 97%] src.haive.core.engine.retriever.providers.AzureAISearchRetrieverConfig
[AutoAPI] Rendering Data... [ 97%] src.haive.core.engine.retriever.providers.ChatGPTPluginRetrieverConfig
[AutoAPI] Rendering Data... [ 97%] src.haive.core.engine.retriever.providers.ElasticsearchRetrieverConfig
[AutoAPI] Rendering Data... [ 97%] src.haive.core.engine.retriever.providers.RePhraseQueryRetrieverConfig
[AutoAPI] Rendering Data... [ 97%] src.haive.agents.reasoning_and_critique.self_discover.self_discover_v4
[AutoAPI] Rendering Data... [ 97%] src.haive.agents.reasoning_and_critique.self_discover.structurer.agent
[AutoAPI] Rendering Data... [ 97%] src.haive.agents.reasoning_and_critique.self_discover.executor.prompts
[AutoAPI] Rendering Data... [ 97%] src.haive.agents.reasoning_and_critique.self_discover.selector.prompts
[AutoAPI] Rendering Data... [ 97%] src.haive.agents.multi.experiments.implementations.self_discover_state
[AutoAPI] Rendering Data... [ 97%] src.haive.core.engine.vectorstore.providers.ClickHouseVectorStoreConfig
[AutoAPI] Rendering Data... [ 97%] src.haive.core.engine.vectorstore.providers.OpenSearchVectorStoreConfig
[AutoAPI] Rendering Data... [ 98%] src.haive.core.engine.retriever.providers.ParentDocumentRetrieverConfig
[AutoAPI] Rendering Data... [ 98%] src.haive.core.engine.embedding.providers.GoogleVertexAIEmbeddingConfig
[AutoAPI] Rendering Data... [ 98%] src.haive.agents.reasoning_and_critique.self_discover.structurer.models
[AutoAPI] Rendering Data... [ 98%] src.haive.core.engine.document.loaders.specific.web_huggingface_enhanced
[AutoAPI] Rendering Data... [ 98%] src.haive.core.engine.vectorstore.providers.AzureSearchVectorStoreConfig
[AutoAPI] Rendering Data... [ 98%] src.haive.core.engine.retriever.providers.TavilySearchAPIRetrieverConfig
[AutoAPI] Rendering Data... [ 98%] src.haive.core.engine.retriever.providers.LlamaIndexGraphRetrieverConfig
[AutoAPI] Rendering Data... [ 98%] src.haive.core.engine.retriever.providers.RemoteLangChainRetrieverConfig
[AutoAPI] Rendering Data... [ 98%] src.haive.agents.reasoning_and_critique.self_discover.structurer.prompts
[AutoAPI] Rendering Data... [ 98%] src.haive.core.engine.vectorstore.providers.MongoDBAtlasVectorStoreConfig
[AutoAPI] Rendering Data... [ 98%] src.haive.core.engine.vectorstore.providers.ElasticsearchVectorStoreConfig
[AutoAPI] Rendering Data... [ 98%] src.haive.core.engine.retriever.providers.QdrantSparseVectorRetrieverConfig
[AutoAPI] Rendering Data... [ 98%] src.haive.tools.tools.toolkits.dev.python.cst_toolkit.transformers.refactor
[AutoAPI] Rendering Data... [ 98%] src.haive.tools.tools.toolkits.dev.python.cst_toolkit.visitors.type_checking
[AutoAPI] Rendering Data... [ 98%] src.haive.core.engine.vectorstore.providers.AmazonOpenSearchVectorStoreConfig
[AutoAPI] Rendering Data... [ 99%] src.haive.core.engine.retriever.providers.GoogleVertexAISearchRetrieverConfig
[AutoAPI] Rendering Data... [ 99%] src.haive.core.engine.retriever.providers.PineconeHybridSearchRetrieverConfig
[AutoAPI] Rendering Data... [ 99%] src.haive.core.engine.retriever.providers.WeaviateHybridSearchRetrieverConfig
[AutoAPI] Rendering Data... [ 99%] src.haive.core.engine.retriever.providers.AmazonKnowledgeBasesRetrieverConfig
[AutoAPI] Rendering Data... [ 99%] src.haive.agents.reasoning_and_critique.self_discover.self_discover_simple_v4
[AutoAPI] Rendering Data... [ 99%] src.haive.tools.tools.toolkits.dev.python.cst_toolkit.transformers.type_hints
[AutoAPI] Rendering Data... [ 99%] src.haive.core.engine.retriever.providers.ContextualCompressionRetrieverConfig
[AutoAPI] Rendering Data... [ 99%] src.haive.agents.reasoning_and_critique.self_discover.self_discover_multiagent
[AutoAPI] Rendering Data... [ 99%] src.haive.agents.reasoning_and_critique.self_discover.self_discover_working_v4
[AutoAPI] Rendering Data... [ 99%] src.haive.agents.multi.experiments.implementations.compatibility_enhanced_base
[AutoAPI] Rendering Data... [ 99%] src.haive.tools.tools.toolkits.dev.python.cst_toolkit.visitors.import_analyzer
[AutoAPI] Rendering Data... [ 99%] src.haive.agents.reasoning_and_critique.self_discover.self_discover_enhanced_v4
[AutoAPI] Rendering Data... [ 99%] src.haive.core.engine.retriever.providers.TimeWeightedVectorStoreRetrieverConfig
[AutoAPI] Rendering Data... [ 99%] src.haive.agents.reasoning_and_critique.self_discover.self_discover_sequential_v2
[AutoAPI] Rendering Data... [ 99%] src.haive.core.engine.retriever.providers.GoogleDocumentAIWarehouseRetrieverConfig
[AutoAPI] Rendering Data... [100%] src.haive.tools.tools.toolkits.dev.python.cst_toolkit.visitors.dependency_analyzer
[AutoAPI] Rendering Data... [100%] src.haive.tools.tools.toolkits.dev.python.cst_toolkit.visitors.complexity_analyzer
[AutoAPI] Rendering Data... [100%] src.haive.tools.tools.toolkits.dev.python.cst_toolkit.visitors.code_smell_detector
[AutoAPI] Rendering Data... [100%] src.haive.tools.tools.toolkits.dev.python.cst_toolkit.transformers.print_to_logging
[AutoAPI] Rendering Data... [100%] src.haive.tools.tools.toolkits.dev.python.cst_toolkit.transformers.multi_file_rename
[AutoAPI] Rendering Data... [100%] src.haive.tools.tools.toolkits.dev.python.cst_toolkit.visitors.function_call_analyzer
[AutoAPI] Rendering Data... [100%] src.haive.tools.tools.toolkits.dev.python.cst_toolkit.transformers.import_consolidator
[AutoAPI] Rendering Data... [100%] src.haive.tools.tools.toolkits.dev.python.cst_toolkit.transformers.function_logging_transformer

[autosummary] generating autosummary for: NAVIGATION_STRUCTURE.md, agents/api_reference.rst, agents/climateresearchagent_showcase.rst, agents/complete_index.md, agents/conversation/collaborative.rst, agents/conversation/custom_patterns.rst, agents/conversation/debate.rst, agents/conversation/directed.rst, agents/conversation/index.rst, agents/conversation/round_robin.rst, ..., reference/legacy_project_notes/document_loaders/path_analysis_system.md, reference/legacy_project_notes/document_loaders/specific_loaders/database_loaders.md, reference/legacy_project_notes/document_loaders/specific_loaders/pdf_loaders.md, reference/legacy_project_notes/document_loaders/specific_loaders/web_loaders.md, reference/legacy_project_notes/multi_agent_engine_state_issues.md, reference/technical/AGENT_SCHEMA_COMPOSER_FIXES.md, reference/technical/COMPREHENSIVE_AGENT_DISCOVERY_REPORT.md, reference/technical/multi_agent_msgpack_issue_summary.md, tools/index.rst, tools/search/index.rst
WARNING: Failed to import haive.agents.sequential.
Possible hints:

- AttributeError: module 'haive' has no attribute 'agents'
- TypeError: Expected a list of types, an ellipsis, ParamSpec, or Concatenate. Got ~P
  WARNING: Failed to import haive.agents.supervisor.
  Possible hints:
- AttributeError: module 'haive' has no attribute 'agents'
- TypeError: Expected a list of types, an ellipsis, ParamSpec, or Concatenate. Got ~P
  WARNING: Failed to import haive.agents.research.
  Possible hints:
- AttributeError: module 'haive' has no attribute 'agents'
- TypeError: Expected a list of types, an ellipsis, ParamSpec, or Concatenate. Got ~P
  WARNING: Failed to import haive.tools.search.
  Possible hints:
- AttributeError: module 'haive' has no attribute 'tools'
- ImportError: google-search-results is not installed. Please install it with `pip install google-search-results>=2.4.2`
  WARNING: [autosummary] failed to import AI21Provider.
  Possible hints:
- ModuleNotFoundError: No module named 'AI21Provider'
- ValueError: not enough values to unpack (expected 2, got 1)
- KeyError: 'AI21Provider'
  WARNING: [autosummary] failed to import Agent.
  Possible hints:
- ModuleNotFoundError: No module named 'Agent'
- KeyError: 'Agent'
- ValueError: not enough values to unpack (expected 2, got 1)
  WARNING: [autosummary] failed to import AgentNodeV3.
  Possible hints:
- KeyError: 'AgentNodeV3'
- ModuleNotFoundError: No module named 'AgentNodeV3'
- ValueError: not enough values to unpack (expected 2, got 1)
  WARNING: [autosummary] failed to import AnthropicProvider.
  Possible hints:
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'AnthropicProvider'
- KeyError: 'AnthropicProvider'
  WARNING: [autosummary] failed to import AnthropicProvider.
  Possible hints:
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'AnthropicProvider'
- KeyError: 'AnthropicProvider'
  WARNING: [autosummary] failed to import AzureOpenAIProvider.
  Possible hints:
- ModuleNotFoundError: No module named 'AzureOpenAIProvider'
- ValueError: not enough values to unpack (expected 2, got 1)
- KeyError: 'AzureOpenAIProvider'
  WARNING: [autosummary] failed to import AzureOpenAIProvider.
  Possible hints:
- ModuleNotFoundError: No module named 'AzureOpenAIProvider'
- ValueError: not enough values to unpack (expected 2, got 1)
- KeyError: 'AzureOpenAIProvider'
  WARNING: [autosummary] failed to import BaseLLMProvider.
  Possible hints:
- KeyError: 'BaseLLMProvider'
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'BaseLLMProvider'
  WARNING: [autosummary] failed to import BedrockProvider.
  Possible hints:
- ModuleNotFoundError: No module named 'BedrockProvider'
- ValueError: not enough values to unpack (expected 2, got 1)
- KeyError: 'BedrockProvider'
  WARNING: [autosummary] failed to import CohereProvider.
  Possible hints:
- KeyError: 'CohereProvider'
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'CohereProvider'
  WARNING: [autosummary] failed to import CohereProvider.
  Possible hints:
- KeyError: 'CohereProvider'
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'CohereProvider'
  WARNING: [autosummary] failed to import EngineNodeConfig.
  Possible hints:
- ModuleNotFoundError: No module named 'EngineNodeConfig'
- KeyError: 'EngineNodeConfig'
- ValueError: not enough values to unpack (expected 2, got 1)
  WARNING: [autosummary] failed to import Field.
  Possible hints:
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'Field'
- KeyError: 'Field'
  WARNING: [autosummary] failed to import FieldMapping.
  Possible hints:
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'FieldMapping'
- KeyError: 'FieldMapping'
  WARNING: [autosummary] failed to import FireworksProvider.
  Possible hints:
- KeyError: 'FireworksProvider'
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'FireworksProvider'
  WARNING: [autosummary] failed to import GeminiProvider.
  Possible hints:
- KeyError: 'GeminiProvider'
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'GeminiProvider'
  WARNING: [autosummary] failed to import GeminiProvider.
  Possible hints:
- KeyError: 'GeminiProvider'
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'GeminiProvider'
  WARNING: [autosummary] failed to import GroqProvider.
  Possible hints:
- ModuleNotFoundError: No module named 'GroqProvider'
- ValueError: not enough values to unpack (expected 2, got 1)
- KeyError: 'GroqProvider'
  WARNING: [autosummary] failed to import GroqProvider.
  Possible hints:
- ModuleNotFoundError: No module named 'GroqProvider'
- ValueError: not enough values to unpack (expected 2, got 1)
- KeyError: 'GroqProvider'
  WARNING: [autosummary] failed to import HuggingFaceProvider.
  Possible hints:
- KeyError: 'HuggingFaceProvider'
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'HuggingFaceProvider'
  WARNING: [autosummary] failed to import LLMFactory.
  Possible hints:
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'LLMFactory'
- KeyError: 'LLMFactory'
  WARNING: [autosummary] failed to import MistralProvider.
  Possible hints:
- KeyError: 'MistralProvider'
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'MistralProvider'
  WARNING: [autosummary] failed to import MistralProvider.
  Possible hints:
- KeyError: 'MistralProvider'
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'MistralProvider'
  WARNING: [autosummary] failed to import NVIDIAProvider.
  Possible hints:
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'NVIDIAProvider'
- KeyError: 'NVIDIAProvider'
  WARNING: [autosummary] failed to import NodeFactory.
  Possible hints:
- KeyError: 'NodeFactory'
- ModuleNotFoundError: No module named 'NodeFactory'
- ValueError: not enough values to unpack (expected 2, got 1)
  WARNING: [autosummary] failed to import NodeRegistry.
  Possible hints:
- KeyError: 'NodeRegistry'
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'NodeRegistry'
  WARNING: [autosummary] failed to import NodeSchemaComposer.
  Possible hints:
- ModuleNotFoundError: No module named 'NodeSchemaComposer'
- ValueError: not enough values to unpack (expected 2, got 1)
- KeyError: 'NodeSchemaComposer'
  WARNING: [autosummary] failed to import OllamaProvider.
  Possible hints:
- ModuleNotFoundError: No module named 'OllamaProvider'
- ValueError: not enough values to unpack (expected 2, got 1)
- KeyError: 'OllamaProvider'
  WARNING: [autosummary] failed to import OpenAIProvider.
  Possible hints:
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'OpenAIProvider'
- KeyError: 'OpenAIProvider'
  WARNING: [autosummary] failed to import OpenAIProvider.
  Possible hints:
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'OpenAIProvider'
- KeyError: 'OpenAIProvider'
  WARNING: [autosummary] failed to import ProviderImportError.
  Possible hints:
- ValueError: not enough values to unpack (expected 2, got 1)
- KeyError: 'ProviderImportError'
- ModuleNotFoundError: No module named 'ProviderImportError'
  WARNING: [autosummary] failed to import Quick.
  Possible hints:
- KeyError: 'Quick'
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'Quick'
  WARNING: [autosummary] failed to import ReplicateProvider.
  Possible hints:
- KeyError: 'ReplicateProvider'
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'ReplicateProvider'
  WARNING: [autosummary] failed to import RoutingValidationNode.
  Possible hints:
- ModuleNotFoundError: No module named 'RoutingValidationNode'
- ValueError: not enough values to unpack (expected 2, got 1)
- KeyError: 'RoutingValidationNode'
  WARNING: [autosummary] failed to import TogetherProvider.
  Possible hints:
- ValueError: not enough values to unpack (expected 2, got 1)
- KeyError: 'TogetherProvider'
- ModuleNotFoundError: No module named 'TogetherProvider'
  WARNING: [autosummary] failed to import UnifiedValidationNode.
  Possible hints:
- KeyError: 'UnifiedValidationNode'
- ModuleNotFoundError: No module named 'UnifiedValidationNode'
- ValueError: not enough values to unpack (expected 2, got 1)
  WARNING: [autosummary] failed to import Utilities.
  Possible hints:
- ModuleNotFoundError: No module named 'Utilities'
- ValueError: not enough values to unpack (expected 2, got 1)
- KeyError: 'Utilities'
  WARNING: [autosummary] failed to import Validation.
  Possible hints:
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'Validation'
- KeyError: 'Validation'
  WARNING: [autosummary] failed to import ValidationNodeConfig.
  Possible hints:
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'ValidationNodeConfig'
- KeyError: 'ValidationNodeConfig'
  WARNING: [autosummary] failed to import VertexAIProvider.
  Possible hints:
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'VertexAIProvider'
- KeyError: 'VertexAIProvider'
  WARNING: [autosummary] failed to import VertexAIProvider.
  Possible hints:
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'VertexAIProvider'
- KeyError: 'VertexAIProvider'
  WARNING: [autosummary] failed to import XAIProvider.
  Possible hints:
- KeyError: 'XAIProvider'
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'XAIProvider'
  WARNING: [autosummary] failed to import create_engine_node.
  Possible hints:
- ModuleNotFoundError: No module named 'create_engine_node'
- ValueError: not enough values to unpack (expected 2, got 1)
- KeyError: 'create_engine_node'
  WARNING: [autosummary] failed to import create_llm.
  Possible hints:
- KeyError: 'create_llm'
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'create_llm'
  WARNING: [autosummary] failed to import create_node.
  Possible hints:
- ModuleNotFoundError: No module named 'create_node'
- KeyError: 'create_node'
- ValueError: not enough values to unpack (expected 2, got 1)
  WARNING: [autosummary] failed to import get_available_providers.
  Possible hints:
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'get_available_providers'
- KeyError: 'get_available_providers'
  WARNING: [autosummary] failed to import get_provider.
  Possible hints:
- ModuleNotFoundError: No module named 'get_provider'
- KeyError: 'get_provider'
- ValueError: not enough values to unpack (expected 2, got 1)
  WARNING: [autosummary] failed to import get_provider_models.
  Possible hints:
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'get_provider_models'
- KeyError: 'get_provider_models'
  WARNING: [autosummary] failed to import list_providers.
  Possible hints:
- KeyError: 'list_providers'
- ValueError: not enough values to unpack (expected 2, got 1)
- ModuleNotFoundError: No module named 'list_providers'
  loading intersphinx inventory 'langchain' from https://python.langchain.com/objects.inv ...
  loading intersphinx inventory 'pydantic' from https://docs.pydantic.dev/objects.inv ...
  WARNING: failed to reach any of the inventories with the following issues:
  intersphinx inventory 'https://python.langchain.com/objects.inv' not fetchable due to <class 'requests.exceptions.HTTPError'>: 404 Client Error: Not Found for url: https://python.langchain.com/objects.inv
  WARNING: failed to reach any of the inventories with the following issues:
  intersphinx inventory 'https://docs.pydantic.dev/objects.inv' not fetchable due to <class 'requests.exceptions.HTTPError'>: 404 Client Error: Not Found for url: https://docs.pydantic.dev/objects.inv
  myst v4.0.1: MdParserConfig(commonmark_only=False, gfm_only=False, enable_extensions={'substitution', 'attrs_block', 'colon_fence', 'attrs_inline', 'dollarmath', 'linkify', 'smartquotes', 'deflist', 'tasklist', 'strikethrough'}, disable_syntax=[], all_links_external=False, links_external_new_tab=False, url_schemes=('http', 'https', 'mailto', 'ftp'), ref_domains=None, fence_as_directive=set(), number_code_blocks=[], title_to_header=False, heading_anchors=0, heading_slug_func=None, html_meta={}, footnote_sort=True, footnote_transition=True, words_per_minute=200, substitutions={}, linkify_fuzzy_links=True, dmath_allow_labels=True, dmath_allow_space=True, dmath_allow_digits=True, dmath_double_inline=False, update_mathjax=True, mathjax_classes='tex2jax_process|mathjax_process|math|output_area', enable_checkboxes=False, suppress_warnings=[], highlight_code_blocks=True)
  building [mo]: targets for 0 po files that are out of date
  writing output...
  building [html]: build_info mismatch, copying .buildinfo to .buildinfo.bak
  building [html]: targets for 1746 source files that are out of date
  updating environment: [config changed ('suppress_warnings')] 3161 added, 0 changed, 90 removed
  reading sources... [ 0%] NAVIGATION_STRUCTURE
  reading sources... [ 0%] agents/api_reference
  :17: (ERROR/3) Unexpected indentation.
  :18: (WARNING/2) Block quote ends without a blank line; unexpected unindent.
  reading sources... [ 0%] agents/climateresearchagent_showcase
  reading sources... [ 0%] agents/complete_index
  reading sources... [ 0%] agents/conversation/collaborative
  reading sources... [ 0%] agents/conversation/custom_patterns
  reading sources... [ 0%] agents/conversation/debate
  reading sources... [ 0%] agents/conversation/directed
  reading sources... [ 0%] agents/conversation/index
  reading sources... [ 0%] agents/conversation/round_robin
  reading sources... [ 0%] agents/conversation/social_media
  reading sources... [ 0%] agents/conversation_examples
  reading sources... [ 0%] agents/demos/adaptiverag-demo
  reading sources... [ 0%] agents/demos/baserag-demo
  reading sources... [ 0%] agents/demos/debate-demo
  reading sources... [ 1%] agents/demos/index
  reading sources... [ 1%] agents/demos/personresearch-demo
  reading sources... [ 1%] agents/demos/planandexecute-demo
  reading sources... [ 1%] agents/demos/react-demo
  reading sources... [ 1%] agents/demos/reactwithmemory-demo
  reading sources... [ 1%] agents/demos/reflection-demo
  reading sources... [ 1%] agents/demos/simple-demo
  reading sources... [ 1%] agents/demos/simple-demo-cached
  2025-07-27 16:23:05,944 - agent_cache_loader - INFO - ✅ Loaded cache for simple with 1 executions
  reading sources... [ 1%] agents/demos/simple-demo-test
  reading sources... [ 1%] agents/demos/structuredoutput-demo
  reading sources... [ 1%] agents/demos/summarizer-demo
  reading sources... [ 1%] agents/enhanced_agent_template
  reading sources... [ 1%] agents/enhanced_agent_with_graphs
  reading sources... [ 1%] agents/gallery
  reading sources... [ 1%] agents/index
  reading sources... [ 1%] agents/multi/index
  reading sources... [ 1%] agents/quantumexplaineragent_showcase
  reading sources... [ 1%] agents/rag/index
  reading sources... [ 1%] agents/react/index
  reading sources... [ 1%] agents/reactresearchagent_showcase
  reading sources... [ 1%] agents/showcase
  reading sources... [ 1%] agents/showcase_index
  reading sources... [ 1%] agents/showcase_modern
  reading sources... [ 1%] agents/simple/index
  reading sources... [ 1%] agents/simple_visualization_test
  reading sources... [ 1%] agents/simpleanalysisagent_showcase
  reading sources... [ 1%] agents/textsummarizeragent_showcase
  reading sources... [ 1%] agents/working_visualization_demo
  reading sources... [ 1%] api/haive/agents/base/agent_structured_output_mixin/index
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/**init**.py:docstring of haive.agents.simple:1: WARNING: duplicate object description of haive.agents.simple, other instance in api/haive/agents/simple/index, use :no-index: for one of them
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/**init**.py:docstring of haive.agents.simple.agent_v2.SimpleAgentV2:1: WARNING: duplicate object description of haive.agents.simple.SimpleAgent, other instance in agents/simple/index, use :no-index: for one of them
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/**init**.py:docstring of haive.agents.react:1: WARNING: duplicate object description of haive.agents.react, other instance in api/haive/agents/react/index, use :no-index: for one of them
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/**init**.py:docstring of haive.agents.react.agent.ReactAgent:1: WARNING: duplicate object description of haive.agents.react.ReactAgent, other instance in agents/react/index, use :no-index: for one of them
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/**init**.py:docstring of haive.agents.react.agent.ReactAgent:1: WARNING: duplicate object description of haive.agents.react.agent.ReactAgent, other instance in agents/react/index, use :no-index: for one of them
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/**init**.py:docstring of haive.agents.react.agent.ReactAgent.build_graph:1: WARNING: duplicate object description of haive.agents.react.ReactAgent.build_graph, other instance in agents/react/index, use :no-index: for one of them
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/**init**.py:docstring of pydantic.\_internal.\_model_construction.init_private_attributes:1: WARNING: duplicate object description of haive.agents.react.ReactAgent.model_post_init, other instance in agents/react/index, use :no-index: for one of them
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/**init**.py:docstring of haive.agents.react.ReactAgent.model_config:1: WARNING: duplicate object description of haive.agents.react.ReactAgent.model_config, other instance in agents/react/index, use :no-index: for one of them
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/**init**.py:docstring of haive.agents.react.agent_v3.ReactAgentV3.build_graph:11: ERROR: Unexpected indentation. [docutils]
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/**init**.py:docstring of haive.agents.react.agent_v3.ReactAgentV3.build_graph:8: WARNING: Inline literal start-string without end-string. [docutils]
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/**init**.py:docstring of haive.agents.react.agent_v3.ReactAgentV3.build_graph:15: ERROR: Unexpected indentation. [docutils]
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/**init**.py:docstring of haive.agents.react.agent_v3.ReactAgentV3.build_graph:16: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/**init**.py:docstring of haive.agents.react.agent_v3.ReactAgentV3.build_graph:17: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/**init**.py:docstring of haive.agents.react.agent_v3.ReactAgentV3.build_graph:17: WARNING: Inline literal start-string without end-string. [docutils]
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/**init**.py:docstring of haive.agents.react.agent_v3.ReactAgentV3.build_graph:17: WARNING: Inline interpreted text or phrase reference start-string without end-string. [docutils]
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/**init**.py:docstring of haive.agents.rag:1: WARNING: duplicate object description of haive.agents.rag, other instance in api/haive/agents/rag/index, use :no-index: for one of them
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/**init**.py:docstring of haive.agents.conversation:1: WARNING: duplicate object description of haive.agents.conversation, other instance in api/haive/agents/conversation/index, use :no-index: for one of them
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/**init**.py:docstring of haive.agents.conversation.CollaborativeConfig:1: WARNING: duplicate object description of haive.agents.conversation.CollaborativeConfig, other instance in api/haive/agents/conversation/index, use :no-index: for one of them
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/**init**.py:docstring of haive.agents.conversation.ConversationConfig:1: WARNING: duplicate object description of haive.agents.conversation.ConversationConfig, other instance in api/haive/agents/conversation/index, use :no-index: for one of them
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/**init**.py:docstring of haive.agents.conversation.ConversationParticipant:1: WARNING: duplicate object description of haive.agents.conversation.ConversationParticipant, other instance in api/haive/agents/conversation/index, use :no-index: for one of them
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/**init**.py:docstring of haive.agents.conversation.ConversationParticipant.arun:1: WARNING: duplicate object description of haive.agents.conversation.ConversationParticipant.arun, other instance in api/haive/agents/conversation/index, use :no-index: for one of them
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/**init**.py:docstring of haive.agents.conversation.ConversationParticipant.get_role:1: WARNING: duplicate object description of haive.agents.conversation.ConversationParticipant.get_role, other instance in api/haive/agents/conversation/index, use :no-index: for one of them
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/**init**.py:docstring of haive.agents.conversation.DebateConfig:1: WARNING: duplicate object description of haive.agents.conversation.DebateConfig, other instance in api/haive/agents/conversation/index, use :no-index: for one of them
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/**init**.py:docstring of haive.agents.conversation.create_collaboration:1: WARNING: duplicate object description of haive.agents.conversation.create_collaboration, other instance in api/haive/agents/conversation/index, use :no-index: for one of them
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/**init**.py:docstring of haive.agents.conversation.create_conversation:1: WARNING: duplicate object description of haive.agents.conversation.create_conversation, other instance in api/haive/agents/conversation/index, use :no-index: for one of them
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/**init**.py:docstring of haive.agents.conversation.create_debate:1: WARNING: duplicate object description of haive.agents.conversation.create_debate, other instance in api/haive/agents/conversation/index, use :no-index: for one of them
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/**init**.py:docstring of haive.agents.conversation.get_conversation_types:1: WARNING: duplicate object description of haive.agents.conversation.get_conversation_types, other instance in api/haive/agents/conversation/index, use :no-index: for one of them
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/conversation/**init**.py:docstring of haive.agents.conversation.validate_participants:1: WARNING: duplicate object description of haive.agents.conversation.validate_participants, other instance in api/haive/agents/conversation/index, use :no-index: for one of them
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/**init**.py:docstring of haive.agents.planning:1: WARNING: duplicate object description of haive.agents.planning, other instance in api/haive/agents/planning/index, use :no-index: for one of them
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/**init**.py:docstring of haive.agents.multi:1: WARNING: duplicate object description of haive.agents.multi, other instance in api/haive/agents/multi/index, use :no-index: for one of them
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/**init**.py:docstring of haive.agents.multi.clean.MultiAgent.add_conditional_edges:18: ERROR: Unexpected indentation. [docutils]
  /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/**init**.py:docstring of haive.agents.multi.clean.MultiAgent.add_conditional_edges:19: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
  /home/will/Projects/haive/backend/haive/docs/source/agents/conversation/collaborative.rst:13: WARNING: Include file '/home/will/Projects/haive/backend/packages/haive-agents/src/haive/agents/conversation/collaberative/example.py' not found or reading it failed [docutils]
  /home/will/Projects/haive/backend/haive/docs/source/agents/conversation/collaborative.rst:81: WARNING: Include file '/home/will/Projects/haive/backend/packages/haive-agents/src/haive/agents/conversation/collaberative/example.py' not found or reading it failed [docutils]
  /home/will/Projects/haive/backend/haive/docs/source/agents/conversation/debate.rst:13: WARNING: Include file '/home/will/Projects/haive/backend/packages/haive-agents/src/haive/agents/conversation/debate/example.py' not found or reading it failed [docutils]
  /home/will/Projects/haive/backend/haive/docs/source/agents/conversation/debate.rst:135: WARNING: Include file '/home/will/Projects/haive/backend/packages/haive-agents/src/haive/agents/conversation/debate/example.py' not found or reading it failed [docutils]
  /home/will/Projects/haive/backend/haive/docs/source/agents/conversation/directed.rst:13: WARNING: Include file '/home/will/Projects/haive/backend/packages/haive-agents/src/haive/agents/conversation/directed/example.py' not found or reading it failed [docutils]
  /home/will/Projects/haive/backend/haive/docs/source/agents/conversation/directed.rst:73: WARNING: Include file '/home/will/Projects/haive/backend/packages/haive-agents/src/haive/agents/conversation/directed/example.py' not found or reading it failed [docutils]
  /home/will/Projects/haive/backend/haive/docs/source/agents/conversation/index.rst:283: WARNING: toctree contains reference to nonexisting document 'agents/conversation/examples/education' [toc.not_readable]
  /home/will/Projects/haive/backend/haive/docs/source/agents/conversation/index.rst:283: WARNING: toctree contains reference to nonexisting document 'agents/conversation/examples/business' [toc.not_readable]
  /home/will/Projects/haive/backend/haive/docs/source/agents/conversation/index.rst:283: WARNING: toctree contains reference to nonexisting document 'agents/conversation/examples/research' [toc.not_readable]
  /home/will/Projects/haive/backend/haive/docs/source/agents/conversation/index.rst:283: WARNING: toctree contains reference to nonexisting document 'agents/conversation/examples/creative' [toc.not_readable]
  /home/will/Projects/haive/backend/haive/docs/source/agents/conversation/index.rst:283: WARNING: toctree contains reference to nonexisting document 'agents/conversation/examples/support' [toc.not_readable]
  /home/will/Projects/haive/backend/haive/docs/source/agents/conversation/round_robin.rst:13: WARNING: Include file '/home/will/Projects/haive/backend/packages/haive-agents/src/haive/agents/conversation/round_robin/example.py' not found or reading it failed [docutils]
  /home/will/Projects/haive/backend/haive/docs/source/agents/conversation/round_robin.rst:93: WARNING: Include file '/home/will/Projects/haive/backend/packages/haive-agents/src/haive/agents/conversation/round_robin/example.py' not found or reading it failed [docutils]
  /home/will/Projects/haive/backend/haive/docs/source/agents/conversation/social_media.rst:13: WARNING: Include file '/home/will/Projects/haive/backend/packages/haive-agents/src/haive/agents/conversation/social_media/example.py' not found or reading it failed [docutils]
  /home/will/Projects/haive/backend/haive/docs/source/agents/conversation/social_media.rst:123: WARNING: Include file '/home/will/Projects/haive/backend/packages/haive-agents/src/haive/agents/conversation/social_media/example.py' not found or reading it failed [docutils]
  /home/will/Projects/haive/backend/haive/docs/source/agents/conversation_examples.rst:13: WARNING: Include file '/home/will/Projects/haive/backend/packages/haive-agents/src/haive/agents/conversation/directed/example.py' not found or reading it failed [docutils]
  /home/will/Projects/haive/backend/haive/docs/source/agents/conversation_examples.rst:104: WARNING: Include file '/home/will/Projects/haive/backend/packages/haive-agents/src/haive/agents/conversation/collaberative/example.py' not found or reading it failed [docutils]
  /home/will/Projects/haive/backend/haive/docs/source/agents/conversation_examples.rst:225: WARNING: Include file '/home/will/Projects/haive/backend/packages/haive-agents/src/haive/agents/conversation/social_media/example.py' not found or reading it failed [docutils]
  /home/will/Projects/haive/backend/haive/docs/source/agents/demos/simple-demo-cached.rst:1: WARNING: Title underline too short.

🤖 SimpleAgent Demo
================== [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:37: WARNING: Explicit markup ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:41: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:44: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:48: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:49: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:51: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:61: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:63: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:65: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:68: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:70: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:71: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:72: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:76: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:79: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:81: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:82: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:88: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:95: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:101: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:103: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:107: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:110: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:114: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:115: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:117: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:127: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:129: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:131: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:134: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:136: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:137: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:138: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:142: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:145: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:147: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:148: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:154: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:161: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:167: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:169: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:173: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:176: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:180: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:181: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:183: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:193: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:195: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:197: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:200: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:202: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:203: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:204: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:208: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:211: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:213: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:214: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:220: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:227: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:233: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:235: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:239: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:242: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:246: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:248: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:250: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:260: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:262: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:264: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:267: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:269: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:270: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:271: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:275: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:278: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:280: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:281: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:287: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:294: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:300: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:302: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:306: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:309: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:313: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:315: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:317: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:327: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:329: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:331: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:334: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:336: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:337: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:338: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:342: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:345: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:347: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:348: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:354: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:361: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:367: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:369: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:382: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:383: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:393: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:395: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:397: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:401: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:403: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:404: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_template.rst:405: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:212: WARNING: Explicit markup ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:216: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:221: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:225: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:228: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:238: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:239: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:249: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:251: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:253: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:256: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:258: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:260: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:263: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:265: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:266: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:267: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:271: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:274: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:276: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:277: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:282: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:289: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:293: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:295: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:304: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:306: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:316: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:318: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:328: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:329: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:330: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:336: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:338: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:350: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:352: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:355: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:357: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:361: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:362: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:364: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:374: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:376: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:378: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:381: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:383: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:384: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/enhanced_agent_with_graphs.rst:385: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/index.rst:182: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/index.rst:187: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/index.rst:188: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/index.rst:189: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/index.rst:195: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/index.rst:200: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/index.rst:201: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/index.rst:202: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/index.rst:208: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/index.rst:214: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/index.rst:215: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/index.rst:216: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/index.rst:222: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/index.rst:227: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/index.rst:228: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/index.rst:229: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/index.rst:235: ERROR: Unexpected indentation. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/index.rst:241: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/index.rst:242: WARNING: Block quote ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/index.rst:243: WARNING: Definition list ends without a blank line; unexpected unindent. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/index.rst:179: WARNING: All children of a 'grid-row' should be 'grid-item' [design.grid] [design.grid]
/home/will/Projects/haive/backend/haive/docs/source/agents/index.rst:653: WARNING: toctree contains reference to nonexisting document 'api/agents/index' [toc.not_readable]
/home/will/Projects/haive/backend/haive/docs/source/agents/multi/index.rst:81: WARNING: toctree contains reference to nonexisting document 'agents/multi/sequential' [toc.not_readable]
/home/will/Projects/haive/backend/haive/docs/source/agents/multi/index.rst:81: WARNING: toctree contains reference to nonexisting document 'agents/multi/parallel' [toc.not_readable]
/home/will/Projects/haive/backend/haive/docs/source/agents/multi/index.rst:81: WARNING: toctree contains reference to nonexisting document 'agents/multi/hierarchical' [toc.not_readable]
/home/will/Projects/haive/backend/haive/docs/source/agents/multi/index.rst:81: WARNING: toctree contains reference to nonexisting document 'agents/multi/collaborative' [toc.not_readable]
/home/will/Projects/haive/backend/haive/docs/source/agents/rag/index.rst:74: WARNING: toctree contains reference to nonexisting document 'agents/rag/base_rag' [toc.not_readable]
/home/will/Projects/haive/backend/haive/docs/source/agents/rag/index.rst:74: WARNING: toctree contains reference to nonexisting document 'agents/rag/hybrid_rag' [toc.not_readable]
/home/will/Projects/haive/backend/haive/docs/source/agents/rag/index.rst:74: WARNING: toctree contains reference to nonexisting document 'agents/rag/adaptive_rag' [toc.not_readable]
/home/will/Projects/haive/backend/haive/docs/source/agents/rag/index.rst:74: WARNING: toctree contains reference to nonexisting document 'agents/rag/graph_rag' [toc.not_readable]
/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/agent.py:docstring of haive.agents.react.agent.ReactAgent:1: WARNING: duplicate object description of haive.agents.react.ReactAgent, other instance in agents/api_reference, use :no-index: for one of them
/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/agent.py:docstring of haive.agents.react.agent.ReactAgent:1: WARNING: duplicate object description of haive.agents.react.agent.ReactAgent, other instance in agents/api_reference, use :no-index: for one of them
/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/agent.py:docstring of haive.core.engine.base.base.Engine.from_dict:15: WARNING: Inline interpreted text or phrase reference start-string without end-string. [docutils]
/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/agent.py:docstring of haive.agents.react.agent.ReactAgent.build_graph:1: WARNING: duplicate object description of haive.agents.react.ReactAgent.build_graph, other instance in agents/api_reference, use :no-index: for one of them
/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/agent.py:docstring of pydantic.\_internal.\_model_construction.init_private_attributes:1: WARNING: duplicate object description of haive.agents.react.ReactAgent.model_post_init, other instance in agents/api_reference, use :no-index: for one of them
/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react/agent.py:docstring of haive.agents.react.ReactAgent.model_config:1: WARNING: duplicate object description of haive.agents.react.ReactAgent.model_config, other instance in agents/api_reference, use :no-index: for one of them
/home/will/Projects/haive/backend/haive/docs/source/agents/showcase_index.rst:22: WARNING: Inline substitution_reference start-string without end-string. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/showcase_index.rst:22: WARNING: Inline substitution_reference start-string without end-string. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/showcase_index.rst:28: WARNING: Inline substitution_reference start-string without end-string. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/showcase_index.rst:28: WARNING: Inline substitution_reference start-string without end-string. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/showcase_index.rst:34: WARNING: Inline substitution_reference start-string without end-string. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/showcase_index.rst:34: WARNING: Inline substitution_reference start-string without end-string. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/showcase_index.rst:68: WARNING: Inline strong start-string without end-string. [docutils]
/home/will/Projects/haive/backend/haive/docs/source/agents/showcase_index.rst:68: WARNING: Inline emphasis start-string without end-string. [docutils]
/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/agent_v2.py:docstring of haive.agents.simple.agent_v2.SimpleAgentV2:1: WARNING: duplicate object description of haive.agents.simple.SimpleAgent, other instance in agents/api_reference, use :no-index: for one of them
sphinx-sitemap: No pages generated for sitemap.xml
2025-07-27 16:23:08,709 - builtins - INFO - 🔧 Running fix_autoapi_paths function
2025-07-27 16:23:08,709 - builtins - WARNING - Build had exception: 'haive.agents.base.agent_structured_output_mixin.StructuredOutputMixin'

# Versions

- Platform: linux; (Linux-6.6.87.2-microsoft-standard-WSL2-x86_64-with-glibc2.39)
- Python version: 3.12.3 (CPython)
- Sphinx version: 8.2.3
- Docutils version: 0.21.2
- Jinja2 version: 3.1.6
- Pygments version: 2.19.1

# Last Messages

    reading sources... [  1%]
    agents/textsummarizeragent_showcase

    reading sources... [  1%]
    agents/working_visualization_demo

    reading sources... [  1%]
    api/haive/agents/base/agent_structured_output_mixin/index

    sphinx-sitemap: No pages generated for sitemap.xml

# Loaded Extensions

- sphinx.ext.mathjax (8.2.3)
- alabaster (1.0.0)
- sphinxcontrib.applehelp (2.0.0)
- sphinxcontrib.devhelp (2.0.0)
- sphinxcontrib.htmlhelp (2.1.0)
- sphinxcontrib.serializinghtml (2.0.0)
- sphinxcontrib.qthelp (2.0.0)
- sphinx.ext.autodoc.preserve_defaults (8.2.3)
- sphinx.ext.autodoc.type_comment (8.2.3)
- sphinx.ext.autodoc.typehints (8.2.3)
- sphinx.ext.autodoc (8.2.3)
- sphinx.ext.autosummary (8.2.3)
- sphinx.ext.graphviz (8.2.3)
- sphinx.ext.inheritance_diagram (8.2.3)
- autoapi.extension (unknown version)
- sphinx.ext.napoleon (8.2.3)
- sphinx.ext.viewcode (8.2.3)
- sphinx.ext.linkcode (8.2.3)
- sphinx.ext.intersphinx (8.2.3)
- sphinx_design (0.6.1)
- sphinx_tabs (unknown version)
- sphinx_inline_tabs (2023.04.21)
- sphinx_togglebutton (0.3.2)
- sphinx_copybutton (0.5.2)
- sphinx_exec_directive (0.5)
- myst_parser (4.0.1)
- sphinxcontrib.mermaid (8.2.3)
- sphinxcontrib.youtube (1.4.1)
- sphinx_sitemap (2.6.0)
- sphinxcontrib.httpdomain (unknown version)
- sphinxcontrib.openapi (0.8.4)
- sphinxext.opengraph (0.10.0)
- sphinx_gallery (unknown version)
- sphinx_autodoc_typehints (unknown version)
- sphinx_data_viewer (0.1.5)
- sphinxcontrib.jquery (4.1)
- sphinx_needs (5.1.0)
- sphinx_prompt (unknown version)
- sphinx_jinja2 (0.0.1)
- furo (2024.08.06)
- sphinx_basic_ng (1.0.0.beta2)

# Traceback

      File "/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/autoapi/directives.py", line 22, in get_items
        obj = all_objects[name]
              ~~~~~~~~~~~^^^^^^
    KeyError: 'haive.agents.base.agent_structured_output_mixin.StructuredOutputMixin'

The full traceback has been saved in:
/tmp/sphinx-err-fo3ri0hz.log

To report this error to the developers, please open an issue at <https://github.com/sphinx-doc/sphinx/issues/>. Thanks!
Please also report this if it was a user error, so that a better error message can be provided next time.

## Metrics

- Errors: 51
- Warnings: 535
- Build Status: FAILED (KeyError)
- Fatal Error: KeyError on 'haive.agents.base.agent_structured_output_mixin.StructuredOutputMixin'
