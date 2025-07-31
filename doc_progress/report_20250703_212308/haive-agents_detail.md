# haive-agents Documentation Report

## Package Overview

- **Package Path**: /home/will/Projects/haive/backend/haive/packages/haive-agents
- **Has Main **init**.py**: ❌
- **Has README**: ✅
- **Has Examples**: ✅
- **Total Issues**: 1395

## Missing Example Files

- agents
- agents/rag/agentic_router
- agents/rag/multi_agent_rag
- agents/rag/agentic
- agents/react_class/react_agent
- agents/reasoning_and_critique/logic/engines

## Issues by File

### src/haive/agents/state.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 15**: Function 'debug_print' missing type hints
- 🔵 **Line 70**: Method 'WebNavState.ensure_prediction' missing type hints
- 🔵 **Line 79**: Method 'WebNavState.page' missing type hints
- 🔵 **Line 84**: Method 'WebNavState.page' missing type hints
- 🔵 **Line 90**: Method 'WebNavState.model_dump' missing type hints
- 🔵 **Line 98**: Method 'WebNavState.dict' missing type hints

### src/haive/agents/base.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 23**: Class 'DocumentAgent' missing docstring
- 🔵 **Line 27**: Method 'DocumentAgent.run' missing docstring
- 🔵 **Line 27**: Method 'DocumentAgent.run' missing type hints

### src/haive/agents/config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/models.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 18**: Class 'Prediction' missing docstring

### src/haive/agents/factory.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/tool_utils.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/aug_llms.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/state_wrapper.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 25**: Method 'StateWrapper.get_page' missing type hints

### src/haive/agents/qa_agent.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 26**: Function 'debug_print' missing type hints
- 🔵 **Line 55**: Method 'Prediction.ensure_args' missing type hints
- 🔵 **Line 94**: Method 'WebNavState.ensure_prediction' missing type hints
- 🔵 **Line 167**: Method 'WebNavAgent.setup_workflow' missing type hints
- 🔵 **Line 212**: Method 'WebNavAgent.update_scratchpad' missing type hints

### src/haive/agents/routing_agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 54**: Method 'RoutingAgent.setup_workflow' missing type hints
- 🟡 **Line 194**: Function 'route_to_question_handler' missing docstring
- 🔵 **Line 194**: Function 'route_to_question_handler' missing type hints
- 🟡 **Line 203**: Function 'route_to_task_handler' missing docstring
- 🔵 **Line 203**: Function 'route_to_task_handler' missing type hints

### src/haive/agents/chain_agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 103**: Method 'ChainAgent.setup_workflow' missing type hints

### src/haive/agents/tools.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/base/generic_agent.py

- 🔵 **Line 249**: Method 'GenericAgent.setup_agent' missing type hints
- 🔵 **Line 405**: Method 'GenericAgent.create_input_instance' missing type hints
- 🔵 **Line 418**: Method 'GenericAgent.create_output_instance' missing type hints
- 🔵 **Line 431**: Method 'GenericAgent.create_state_instance' missing type hints
- 🔵 **Line 444**: Method 'GenericAgent.get_type_info' missing type hints
- 🟡 **Line 556**: Class 'TypedAgent' missing docstring
- 🟡 **Line 582**: Class 'AutoTypedAgent' missing docstring

### src/haive/agents/base/universal_agent.py

- 🔵 **Line 77**: Method 'Agent.build_graph' missing type hints
- 🔵 **Line 88**: Method 'Agent.compile' missing type hints
- 🔵 **Line 129**: Method 'Agent.is_reasoning_agent' missing type hints
- 🔵 **Line 135**: Method 'Agent.is_processing_agent' missing type hints
- 🔵 **Line 141**: Method 'Agent.is_orchestration_agent' missing type hints
- 🔵 **Line 147**: Method 'Agent.get_capabilities' missing type hints
- 🔵 **Line 151**: Method 'Agent.can_reason' missing type hints
- 🔵 **Line 155**: Method 'Agent.can_process_batch' missing type hints
- 🔵 **Line 159**: Method 'Agent.can_orchestrate' missing type hints

### src/haive/agents/base/simple_agent_base.py

- 🔵 **Line 74**: Method 'Agent.validate_agent_requirements' missing type hints
- 🔵 **Line 159**: Method 'Agent.get_available_tools' missing type hints
- 🔵 **Line 168**: Method 'Agent.can_reason' missing type hints
- 🔵 **Line 172**: Method 'Agent.get_agent_capabilities' missing type hints
- 🔵 **Line 183**: Method 'Agent.get_node_type' missing type hints
- 🔵 **Line 188**: Method 'Agent.setup_agent' missing type hints

### src/haive/agents/base/debug_utils.py

- 🔵 **Line 33**: Method 'AgentDebugger.enable' missing type hints
- 🔵 **Line 38**: Method 'AgentDebugger.disable' missing type hints
- 🔵 **Line 43**: Method 'AgentDebugger.log_runnable_config' missing type hints
- 🔵 **Line 98**: Method 'AgentDebugger.log_recursion_limit_flow' missing type hints
- 🔵 **Line 122**: Method 'AgentDebugger.log_config_preparation' missing type hints
- 🔵 **Line 206**: Method 'AgentDebugger.log_agent_execution_start' missing type hints
- 🔵 **Line 256**: Function 'enable_agent_debugging' missing type hints
- 🔵 **Line 266**: Function 'disable_agent_debugging' missing type hints
- 🔵 **Line 272**: Function 'debug_runnable_config' missing type hints

### src/haive/agents/base/compiled_agent.py

- 🔵 **Line 97**: Method 'CompiledAgent.validate_agent_requirements' missing type hints
- 🔵 **Line 209**: Method 'CompiledAgent.get_available_tools' missing type hints
- 🔵 **Line 217**: Method 'CompiledAgent.can_reason' missing type hints
- 🔵 **Line 225**: Method 'CompiledAgent.get_component_type' missing type hints
- 🔵 **Line 229**: Method 'CompiledAgent.get_agent_capabilities' missing type hints
- 🔵 **Line 245**: Method 'CompiledAgent.setup_agent' missing type hints

### src/haive/agents/base/agent.py

- 🔵 **Line 257**: Method 'Agent.complete_agent_setup' missing type hints
- 🔵 **Line 304**: Method 'Agent.ensure_basic_schema' missing type hints
- 🔵 **Line 334**: Method 'Agent.setup_agent' missing type hints
- 🔵 **Line 689**: Method 'Agent.get_input_fields' missing type hints
- 🔵 **Line 712**: Method 'Agent.get_output_fields' missing type hints
- 🔵 **Line 816**: Method 'Agent.main_engine' missing type hints
- 🔵 **Line 838**: Method 'Agent.build_graph' missing type hints
- 🔵 **Line 851**: Method 'Agent.rebuild_graph' missing type hints
- 🔵 **Line 862**: Method 'Agent.regenerate_schemas' missing type hints
- 🔵 **Line 872**: Method 'Agent.compile' missing type hints
- 🔵 **Line 1010**: Method 'Agent.get_all_tools' missing type hints
- 🔵 **Line 1059**: Method 'Agent.get_all_tool_schemas' missing type hints
- 🔵 **Line 1135**: Method 'Agent.get_all_class_engines' missing type hints
- 🔵 **Line 1168**: Method 'Agent.get_all_instance_engines' missing type hints
- 🔵 **Line 1260**: Method 'Agent.get_state_tools' missing type hints
- 🔵 **Line 1279**: Method 'Agent.sync_tools_to_engines' missing type hints
- 🔵 **Line 1297**: Method 'Agent.get_schema_info' missing type hints
- 🔵 **Line 1377**: Method 'Agent.display_schema_info' missing type hints
- 🔵 **Line 1492**: Method 'Agent.auto_derive_schemas' missing type hints
- 🔵 **Line 1511**: Method 'Agent.get_derived_schemas' missing type hints

### src/haive/agents/base/types.py

- 🔵 **Line 50**: Method 'GraphProvider.build_graph' missing type hints
- 🔵 **Line 60**: Method 'StateProvider.state_schema' missing type hints
- 🔵 **Line 87**: Method 'EngineProvider.engine' missing type hints
- 🔵 **Line 92**: Method 'EngineProvider.engines' missing type hints

### src/haive/agents/document/agent.py

- 🔵 **Line 378**: Method 'DocumentAgent.validate_engine_type' missing type hints
- 🔵 **Line 386**: Method 'DocumentAgent.validate_chunk_overlap' missing type hints
- 🔵 **Line 394**: Method 'DocumentAgent.setup_agent' missing type hints
- 🔵 **Line 468**: Method 'DocumentAgent.build_graph' missing type hints

### src/haive/agents/discovery/dynamic_tool_selector.py

- 🔵 **Line 145**: Method 'DynamicToolSelector.setup_selector' missing type hints
- 🔵 **Line 687**: Method 'LangGraphStyleSelector.create_tool_selection_node' missing type hints

### src/haive/agents/discovery/semantic_discovery.py

- 🔵 **Line 120**: Method 'VectorBasedToolSelector.setup_vector_store' missing type hints
- 🔵 **Line 515**: Method 'SemanticDiscoveryEngine.setup_registry' missing type hints

### src/haive/agents/task_analysis/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/task_analysis/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 306**: Method 'TaskAnalysisAgent.setup_agent' missing type hints
- 🔵 **Line 325**: Method 'TaskAnalysisAgent.build_graph' missing type hints

### src/haive/agents/task_analysis/prompts.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/supervisor/registry.py

- 🔵 **Line 144**: Method 'AgentRegistry.get_available_agents' missing type hints
- 🔵 **Line 152**: Method 'AgentRegistry.get_routing_options' missing type hints
- 🔵 **Line 160**: Method 'AgentRegistry.get_agent_capabilities' missing type hints
- 🔵 **Line 190**: Method 'AgentRegistry.get_agent_count' missing type hints
- 🔵 **Line 198**: Method 'AgentRegistry.needs_rebuild' missing type hints
- 🔵 **Line 206**: Method 'AgentRegistry.mark_rebuilt' missing type hints
- 🔵 **Line 221**: Method 'AgentRegistry.clear_all' missing type hints
- 🔵 **Line 269**: Method 'AgentRegistry.print_registry_state' missing type hints
- 🔵 **Line 300**: Method 'AgentRegistry.get_registry_stats' missing type hints

### src/haive/agents/supervisor/example_delegation.py

- 🔵 **Line 27**: Function 'create_mock_research_agent' missing type hints
- 🔵 **Line 45**: Function 'create_mock_math_agent' missing type hints
- 🔵 **Line 62**: Function 'create_mock_writing_agent' missing type hints
- 🔵 **Line 79**: Function 'create_supervisor_agent' missing type hints
- 🔵 **Line 245**: Function 'main' missing type hints

### src/haive/agents/supervisor/simple_test.py

- 🔵 **Line 213**: Function 'main' missing type hints

### src/haive/agents/supervisor/agent.py

- 🔵 **Line 173**: Method 'SupervisorAgent.build_graph' missing type hints
- 🔵 **Line 368**: Method 'SupervisorAgent.get_registered_agents' missing type hints
- 🔵 **Line 372**: Method 'SupervisorAgent.print_supervisor_status' missing type hints

### src/haive/agents/supervisor/routing.py

- 🔵 **Line 465**: Method 'DynamicRoutingEngine.print_routing_stats' missing type hints

### src/haive/agents/supervisor/agent_v2.py

- 🔵 **Line 103**: Method 'SupervisorAgent.setup_agent' missing type hints
- 🔵 **Line 117**: Method 'SupervisorAgent.build_graph' missing type hints
- 🔵 **Line 277**: Method 'SupervisorAgent.get_worker_agents' missing type hints
- 🔵 **Line 281**: Method 'SupervisorAgent.create_generic_agent_execution_node' missing type hints
- 🔵 **Line 355**: Method 'SupervisorAgent.print_supervisor_status' missing type hints

### src/haive/agents/chain/multi_integration.py

- 🔵 **Line 77**: Method 'ChainNodeWrapper.build_graph' missing type hints
- 🔵 **Line 121**: Function 'chain_multi' missing type hints
- 🔵 **Line 126**: Function 'sequential_multi' missing type hints

### src/haive/agents/chain/chain_agent_simple.py

- 🔵 **Line 56**: Method 'ChainAgent.build_graph' missing type hints
- 🔵 **Line 175**: Function 'flow' missing type hints
- 🔵 **Line 227**: Method 'FlowBuilder.build' missing type hints

### src/haive/agents/chain/chain_examples.py

- 🔵 **Line 21**: Function 'example_sequential_mixed' missing type hints
- 🔵 **Line 62**: Function 'example_mapped_flow' missing type hints
- 🔵 **Line 94**: Function 'example_incremental_building' missing type hints
- 🔵 **Line 126**: Function 'example_nested_chains' missing type hints
- 🔵 **Line 151**: Function 'example_rag_router_simplified' missing type hints
- 🔵 **Line 189**: Function 'example_engines_as_nodes' missing type hints
- 🟡 **Line 42**: Function 'process_summary' missing docstring
- 🔵 **Line 42**: Function 'process_summary' missing type hints

### src/haive/agents/chain/extended_examples.py

- 🔵 **Line 18**: Function 'example_simple_sequential' missing type hints
- 🔵 **Line 31**: Function 'example_with_agents_and_engines' missing type hints
- 🔵 **Line 62**: Function 'example_custom_edges' missing type hints
- 🔵 **Line 84**: Function 'example_with_branching' missing type hints
- 🔵 **Line 119**: Function 'example_with_loop' missing type hints
- 🔵 **Line 132**: Function 'example_rag_router_super_simple' missing type hints
- 🔵 **Line 167**: Function 'example_start_and_end' missing type hints
- 🔵 **Line 187**: Function 'example_operator_chaining' missing type hints
- 🔵 **Line 201**: Function 'example_mixed_indices_and_names' missing type hints

### src/haive/agents/chain/examples.py

- 🔵 **Line 29**: Function 'create_agentic_router_declarative' missing type hints
- 🔵 **Line 110**: Function 'create_query_planning_declarative' missing type hints
- 🔵 **Line 181**: Function 'create_self_reflective_declarative' missing type hints
- 🔵 **Line 253**: Function 'create_complex_flow_from_spec' missing type hints
- 🔵 **Line 311**: Function 'create_rag_with_fallback' missing type hints
- 🟡 **Line 39**: Class 'StrategyDecision' missing docstring

### src/haive/agents/chain/examples_simple.py

- 🔵 **Line 17**: Function 'example_basic' missing type hints
- 🔵 **Line 30**: Function 'example_mixed' missing type hints
- 🔵 **Line 62**: Function 'example_routing' missing type hints
- 🔵 **Line 86**: Function 'example_direct' missing type hints
- 🔵 **Line 101**: Function 'example_incremental' missing type hints
- 🔵 **Line 121**: Function 'example_rag_router' missing type hints

### src/haive/agents/sequential/config.py

- 🔵 **Line 92**: Method 'SequentialAgentConfig.validate_steps' missing type hints
- 🔵 **Line 99**: Method 'SequentialAgentConfig.setup_components' missing type hints
- 🔵 **Line 125**: Method 'SequentialAgentConfig.build_agent' missing type hints

### src/haive/agents/sequential/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/sequential/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 32**: Method 'SequentialAgent.validate_agents' missing type hints
- 🔵 **Line 53**: Method 'SequentialAgent.set_state_schema' missing docstring
- 🔵 **Line 53**: Method 'SequentialAgent.set_state_schema' missing type hints
- 🔵 **Line 63**: Method 'SequentialAgent.validate_non_empty_agents' missing type hints
- 🔵 **Line 69**: Method 'SequentialAgent.build_graph' missing type hints

### src/haive/agents/sequential/example.py

- 🟡 **Line 31**: Function 'run_example' missing docstring
- 🔵 **Line 31**: Function 'run_example' missing type hints

### src/haive/agents/planning/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/simple/state.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 53**: Method 'SimpleAgentState.extract_last_message_content' missing type hints

### src/haive/agents/simple/config.py

- 🔵 **Line 75**: Method 'SimpleAgentConfig.validate_engine' missing type hints
- 🔵 **Line 82**: Method 'SimpleAgentConfig.validate_mappings' missing type hints

### src/haive/agents/simple/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 26**: Function 'has_tool_calls' missing type hints
- 🔵 **Line 40**: Function 'placeholder_node' missing type hints
- 🔵 **Line 149**: Method 'SimpleAgent.validate_engine_type' missing type hints
- 🔵 **Line 155**: Method 'SimpleAgent.setup_agent' missing type hints
- 🔵 **Line 337**: Method 'SimpleAgent.get_tool_routes' missing type hints
- 🔵 **Line 347**: Method 'SimpleAgent.build_graph' missing type hints
- 🔵 **Line 432**: Method 'SimpleAgent.create_runnable' missing type hints
- 🔵 **Line 466**: Method 'SimpleAgent.from_engine' missing type hints
- 🔵 **Line 471**: Method 'SimpleAgent.create_with_tools' missing type hints

### src/haive/agents/simple/example.py

- 🔵 **Line 44**: Function 'debug_print' missing type hints
- 🔵 **Line 56**: Function 'example_with_custom_state_schema' missing type hints
- 🟡 **Line 61**: Class 'CustomAgentState' missing docstring

### src/haive/agents/simple/debug.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/ltm/agent.py

- 🔵 **Line 246**: Method 'LTMAgent.setup_agent' missing type hints
- 🔵 **Line 262**: Method 'LTMAgent.build_graph' missing type hints

### src/haive/agents/rag/branched_chain.py

- 🔵 **Line 503**: Function 'get_branched_rag_io_schema' missing type hints
- 🟡 **Line 380**: Function 'add_context' missing docstring
- 🟡 **Line 421**: Function 'prepare_context' missing docstring

### src/haive/agents/rag/enhanced_memory_react.py

- 🔵 **Line 516**: Function 'get_enhanced_memory_react_io_schema' missing type hints
- 🟡 **Line 391**: Function 'check_memory' missing docstring
- 🟡 **Line 446**: Function 'add_context' missing docstring
- 🟡 **Line 472**: Function 'check_tools' missing docstring
- 🟡 **Line 506**: Function 'add_context' missing docstring

### src/haive/agents/rag/unified_factory.py

- 🔵 **Line 279**: Function 'create_rag_multi' missing type hints
- 🔵 **Line 303**: Function 'example_usage' missing type hints

### src/haive/agents/rag/list_iteration_example.py

- 🔵 **Line 23**: Function 'create_multi_query_processor' missing type hints
- 🔵 **Line 56**: Function 'create_document_summarizer' missing type hints
- 🔵 **Line 98**: Function 'create_entity_extractor' missing type hints
- 🔵 **Line 140**: Function 'create_parallel_document_grader' missing type hints
- 🔵 **Line 165**: Function 'example_graph_usage' missing type hints

### src/haive/agents/rag/modular_chain.py

- 🟡 **Line 74**: Function 'filter_documents' missing docstring
- 🟡 **Line 137**: Function 'verify_answer' missing docstring

### src/haive/agents/long_term_memory/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/long_term_memory/engines.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/long_term_memory/models.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/long_term_memory/aug_llm.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/long_term_memory/nodes.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/long_term_memory/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/long_term_memory/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 48**: Method 'LongTermMemoryAgent.setup_workflow' missing docstring
- 🔵 **Line 48**: Method 'LongTermMemoryAgent.setup_workflow' missing type hints

### src/haive/agents/long_term_memory/tools.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/react/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/react/config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/react/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/react/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 37**: Method 'ReactAgent.build_graph' missing type hints

### src/haive/agents/reasoning_and_critique/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/react_class/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/document_modifiers/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/utils/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/utils/utils.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 33**: Function 'parse' missing docstring

### src/haive/agents/multi/base.py

- 🔵 **Line 214**: Method 'MultiAgent.setup_multi_agent' missing type hints
- 🔵 **Line 347**: Method 'MultiAgent.build_graph' missing type hints
- 🔵 **Line 491**: Method 'MultiAgent.analyze_io_compatibility' missing type hints
- 🔵 **Line 849**: Method 'MultiAgent.optimize_agent_order' missing type hints
- 🔵 **Line 1048**: Method 'MultiAgent.visualize_structure' missing type hints

### src/haive/agents/multi/simple_debug.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 26**: Class 'Plan' missing docstring

### src/haive/agents/multi/multi_agent_base (1).py

- 🔵 **Line 117**: Method 'MultiAgent.setup_agent' missing type hints
- 🔵 **Line 154**: Method 'MultiAgent.build_graph' missing type hints

### src/haive/agents/multi/compatibility_enhanced_base.py

- 🔵 **Line 363**: Method 'CompatibilityEnhancedMultiAgent.build_graph' missing type hints
- 🔵 **Line 477**: Method 'CompatibilityEnhancedMultiAgent.visualize_compatibility' missing type hints

### src/haive/agents/multi/agent.py

- 🔵 **Line 151**: Method 'MultiAgent.setup_agent' missing type hints
- 🔵 **Line 207**: Method 'MultiAgent.build_graph' missing type hints

### src/haive/agents/multi/example.py

- 🔵 **Line 23**: Method 'ResearchAgent.setup_agent' missing type hints
- 🔵 **Line 68**: Method 'WritingAgent.setup_agent' missing type hints
- 🔵 **Line 109**: Function 'create_research_writing_system' missing type hints
- 🔵 **Line 138**: Function 'demo_multi_agent_system' missing type hints
- 🔵 **Line 204**: Function 'create_parallel_specialist_system' missing type hints
- 🔵 **Line 227**: Function 'save_and_load_demo' missing type hints

### src/haive/agents/multi/debug_with_logging.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 36**: Class 'Plan' missing docstring

### src/haive/agents/memory/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/memory/config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/memory/models.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/memory/memory_utils.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 229**: Function 'create_memory_tools' missing type hints

### src/haive/agents/memory/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/memory/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 149**: Method 'MemoryAgent.setup_workflow' missing type hints

### src/haive/agents/wiki_writer/state.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 9**: Class 'InterviewState' missing docstring

### src/haive/agents/wiki_writer/base.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/wiki_writer/models.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 6**: Class 'Subsection' missing docstring
- 🔵 **Line 11**: Method 'Subsection.as_str' missing docstring
- 🔵 **Line 11**: Method 'Subsection.as_str' missing type hints
- 🟡 **Line 15**: Class 'Section' missing docstring
- 🔵 **Line 24**: Method 'Section.as_str' missing docstring
- 🔵 **Line 24**: Method 'Section.as_str' missing type hints
- 🟡 **Line 32**: Class 'WikiSection' missing docstring
- 🔵 **Line 42**: Method 'WikiSection.as_str' missing docstring
- 🔵 **Line 42**: Method 'WikiSection.as_str' missing type hints
- 🟡 **Line 53**: Class 'Outline' missing docstring
- 🔵 **Line 61**: Method 'Outline.as_str' missing docstring
- 🔵 **Line 61**: Method 'Outline.as_str' missing type hints
- 🟡 **Line 67**: Class 'RelatedSubjects' missing docstring
- 🟡 **Line 76**: Class 'Editor' missing docstring
- 🔵 **Line 91**: Method 'Editor.persona' missing docstring
- 🔵 **Line 91**: Method 'Editor.persona' missing type hints
- 🟡 **Line 95**: Class 'Perspectives' missing docstring

### src/haive/agents/wiki_writer/nodes.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/wiki_writer/aug_llms.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/wiki_writer/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/wiki_writer/utils.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 4**: Function 'update_references' missing docstring
- 🔵 **Line 4**: Function 'update_references' missing type hints
- 🟡 **Line 11**: Function 'update_editor' missing docstring
- 🔵 **Line 11**: Function 'update_editor' missing type hints
- 🟡 **Line 18**: Function 'format_doc' missing docstring
- 🔵 **Line 18**: Function 'format_doc' missing type hints

### src/haive/agents/wiki_writer/agent.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/self_healing_code/state.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 6**: Class 'SelfHealingCodeState' missing docstring

### src/haive/agents/self_healing_code/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/self_healing_code/agent.py

- 🔴 **Line 1**: Could not parse file: expected 'except' or 'finally' block (<unknown>, line 166)

### src/haive/agents/self_healing_code/branches.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 5**: Function 'error_router' missing docstring
- 🔵 **Line 5**: Function 'error_router' missing type hints
- 🟡 **Line 11**: Function 'memory_filter_router' missing docstring
- 🔵 **Line 11**: Function 'memory_filter_router' missing type hints
- 🟡 **Line 17**: Function 'memory_generation_router' missing docstring
- 🔵 **Line 17**: Function 'memory_generation_router' missing type hints
- 🟡 **Line 23**: Function 'memory_update_router' missing docstring
- 🔵 **Line 23**: Function 'memory_update_router' missing type hints

### src/haive/agents/research/storm/config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/research/storm/example.py

- 🔵 **Line 25**: Function 'setup_environment' missing type hints
- 🔵 **Line 171**: Function 'main' missing type hints

### src/haive/agents/research/person/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/research/person/config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/research/person/models.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/research/person/utils.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/research/person/agent.py

- 🔵 **Line 173**: Method 'PersonResearchAgent.setup_workflow' missing type hints

### src/haive/agents/research/person/prompts.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/research/open_perplexity/structured_tools.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 36**: Function 'register_document_loader' missing type hints
- 🔵 **Line 67**: Method 'EnhancedWebBaseLoader.load' missing type hints
- 🔵 **Line 128**: Method 'EnhancedRecursiveUrlLoader.load' missing type hints
- 🔵 **Line 163**: Method 'EnhancedGitHubIssuesLoader.load' missing type hints
- 🔵 **Line 193**: Method 'EnhancedArxivLoader.load' missing type hints
- 🔵 **Line 227**: Method 'EnhancedHNLoader.load' missing type hints
- 🔵 **Line 308**: Function 'get_available_loaders' missing type hints
- 🟡 **Line 39**: Function 'decorator' missing docstring
- 🔵 **Line 39**: Function 'decorator' missing type hints

### src/haive/agents/research/open_perplexity/engines.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/research/open_perplexity/config.py

- 🔵 **Line 164**: Method 'ResearchAgentConfig.from_scratch' missing type hints

### src/haive/agents/research/open_perplexity/models.py

- 🔵 **Line 139**: Method 'ResearchSource.validate_relevance_score' missing type hints
- 🔵 **Line 183**: Method 'ResearchFinding.validate_confidence' missing type hints
- 🔵 **Line 240**: Method 'ResearchSummary.validate_confidence_score' missing type hints
- 🔵 **Line 251**: Method 'ResearchSummary.assess_depth' missing type hints
- 🔵 **Line 302**: Method 'DataSourceConfig.validate_priority' missing type hints

### src/haive/agents/research/open_perplexity/react_agent_config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/research/open_perplexity/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 48**: Method 'ResearchAgent.react_agent' missing type hints
- 🔵 **Line 57**: Method 'ResearchAgent.rag_agent' missing type hints
- 🔵 **Line 67**: Method 'ResearchAgent.vectorstore' missing type hints
- 🔵 **Line 77**: Method 'ResearchAgent.retriever' missing type hints
- 🔵 **Line 118**: Method 'ResearchAgent.setup_workflow' missing type hints

### src/haive/agents/research/open_perplexity/cli.py

- 🔵 **Line 148**: Function 'main' missing type hints

### src/haive/agents/research/perplexity/pro_search/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/research/open_perplexity/examples/run_with_visualization.py

- 🔵 **Line 34**: Function 'run_example' missing type hints

### src/haive/agents/research/open_perplexity/examples/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/research/open_perplexity/examples/run_from_file.py

- 🔵 **Line 22**: Function 'setup_logging' missing type hints
- 🔵 **Line 37**: Function 'load_research_question' missing type hints
- 🔵 **Line 46**: Function 'run_research' missing type hints
- 🔵 **Line 138**: Function 'parse_arguments' missing type hints

### src/haive/agents/research/open_perplexity/examples/batch_research.py

- 🔵 **Line 94**: Function 'main' missing type hints

### src/haive/agents/research/open_perplexity/examples/simple_research.py

- 🔵 **Line 23**: Function 'main' missing type hints

### src/haive/agents/common/models/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/common/models/mixins.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/common/models/task_analysis/base.py

- 🔵 **Line 297**: Method 'TaskStep.get_duration_hours' missing type hints
- 🔵 **Line 305**: Method 'TaskStep.is_blocking' missing type hints
- 🔵 **Line 313**: Method 'TaskStep.get_complexity_score' missing type hints
- 🔵 **Line 409**: Method 'DependencyNode.is_blocking' missing type hints
- 🔵 **Line 421**: Method 'DependencyNode.allows_parallelization' missing type hints
- 🔵 **Line 429**: Method 'DependencyNode.creates_join_point' missing type hints
- 🔵 **Line 567**: Method 'Task.get_all_steps' missing type hints
- 🔵 **Line 583**: Method 'Task.get_all_tasks' missing type hints
- 🔵 **Line 597**: Method 'Task.calculate_total_duration' missing type hints
- 🔵 **Line 615**: Method 'Task.get_max_depth' missing type hints
- 🔵 **Line 632**: Method 'Task.get_breadth' missing type hints
- 🔵 **Line 640**: Method 'Task.has_parallel_opportunities' missing type hints
- 🔵 **Line 661**: Method 'Task.create_auto_tree' missing type hints

### src/haive/agents/common/models/task_analysis/solvability.py

- 🔵 **Line 206**: Method 'SolvabilityAssessment.validate_solvability_consistency' missing type hints
- 🔵 **Line 260**: Method 'SolvabilityAssessment.get_solvability_score' missing type hints
- 🔵 **Line 290**: Method 'SolvabilityAssessment.has_showstopper_barriers' missing type hints
- 🔵 **Line 304**: Method 'SolvabilityAssessment.get_addressable_barriers' missing type hints
- 🔵 **Line 328**: Method 'SolvabilityAssessment.estimate_breakthrough_timeline' missing type hints
- 🔵 **Line 393**: Method 'SolvabilityAssessment.get_immediate_actions' missing type hints
- 🔵 **Line 437**: Method 'SolvabilityAssessment.generate_solvability_report' missing type hints

### src/haive/agents/common/models/task_analysis/parallelization.py

- 🔵 **Line 122**: Method 'JoinPoint.get_input_count' missing type hints
- 🔵 **Line 130**: Method 'JoinPoint.get_output_count' missing type hints
- 🔵 **Line 138**: Method 'JoinPoint.is_merge_point' missing type hints
- 🔵 **Line 146**: Method 'JoinPoint.is_split_point' missing type hints
- 🔵 **Line 235**: Method 'ParallelGroup.get_task_count' missing type hints
- 🔵 **Line 243**: Method 'ParallelGroup.get_theoretical_speedup' missing type hints
- 🔵 **Line 337**: Method 'ExecutionPhase.get_total_task_count' missing type hints
- 🔵 **Line 345**: Method 'ExecutionPhase.get_max_parallelism' missing type hints
- 🔵 **Line 356**: Method 'ExecutionPhase.calculate_sequential_duration' missing type hints
- 🔵 **Line 367**: Method 'ExecutionPhase.get_parallelization_benefit' missing type hints
- 🔵 **Line 472**: Method 'ParallelizationAnalysis.get_total_phases' missing type hints
- 🔵 **Line 480**: Method 'ParallelizationAnalysis.get_max_parallelism' missing type hints
- 🔵 **Line 491**: Method 'ParallelizationAnalysis.get_critical_path_duration' missing type hints
- 🔵 **Line 499**: Method 'ParallelizationAnalysis.calculate_time_savings' missing type hints
- 🔵 **Line 509**: Method 'ParallelizationAnalysis.get_efficiency_percentage' missing type hints

### src/haive/agents/common/models/task_analysis/branching.py

- 🔵 **Line 211**: Method 'TaskBranch.get_effort_category' missing type hints
- 🔵 **Line 227**: Method 'TaskBranch.get_duration_category' missing type hints
- 🔵 **Line 247**: Method 'TaskBranch.has_dependencies' missing type hints
- 🔵 **Line 255**: Method 'TaskBranch.is_enabling' missing type hints
- 🔵 **Line 263**: Method 'TaskBranch.is_high_risk' missing type hints
- 🔵 **Line 415**: Method 'TaskDecomposition.validate_decomposition_consistency' missing type hints
- 🔵 **Line 462**: Method 'TaskDecomposition.get_dependency_graph' missing type hints
- 🔵 **Line 470**: Method 'TaskDecomposition.get_enables_graph' missing type hints
- 🔵 **Line 478**: Method 'TaskDecomposition.find_independent_branches' missing type hints
- 🔵 **Line 490**: Method 'TaskDecomposition.find_terminal_branches' missing type hints
- 🔵 **Line 500**: Method 'TaskDecomposition.calculate_parallelization_speedup' missing type hints
- 🔵 **Line 514**: Method 'TaskDecomposition.get_complexity_metrics' missing type hints
- 🔵 **Line 544**: Method 'TaskDecomposition.get_execution_recommendations' missing type hints

### src/haive/agents/common/models/task_analysis/analysis.py

- 🔵 **Line 328**: Method 'TaskAnalysis.validate_analysis_consistency' missing type hints
- 🔵 **Line 371**: Method 'TaskAnalysis.get_overall_assessment' missing type hints
- 🔵 **Line 390**: Method 'TaskAnalysis.generate_executive_summary' missing type hints
- 🔵 **Line 459**: Method 'TaskAnalysis.get_execution_recommendations' missing type hints

### src/haive/agents/common/models/grade/composite.py

- 🔵 **Line 127**: Method 'CompositeGrade.validate_weights_and_indices' missing type hints
- 🔵 **Line 158**: Method 'CompositeGrade.get_normalized_weights' missing type hints
- 🔵 **Line 175**: Method 'CompositeGrade.get_normalized_score' missing type hints
- 🔵 **Line 280**: Method 'CompositeGrade.has_consensus' missing type hints
- 🔵 **Line 303**: Method 'CompositeGrade.get_grade_statistics' missing type hints
- 🔵 **Line 338**: Method 'CompositeGrade.get_grade_breakdown' missing type hints
- 🔵 **Line 386**: Method 'CompositeGrade.get_consensus_analysis' missing type hints
- 🔵 **Line 411**: Method 'CompositeGrade.to_display_string' missing type hints

### src/haive/agents/common/models/grade/base.py

- 🔵 **Line 164**: Method 'Grade.get_normalized_score' missing type hints
- 🔵 **Line 186**: Method 'Grade.get_grade_summary' missing type hints
- 🔵 **Line 255**: Method 'Grade.to_display_string' missing type hints

### src/haive/agents/common/models/grade/rubric.py

- 🔵 **Line 79**: Method 'RubricCriterion.validate_score_range' missing type hints
- 🔵 **Line 99**: Method 'RubricCriterion.validate_score_within_max' missing type hints
- 🔵 **Line 114**: Method 'RubricCriterion.get_normalized_score' missing type hints
- 🔵 **Line 124**: Method 'RubricCriterion.get_percentage_score' missing type hints
- 🔵 **Line 132**: Method 'RubricCriterion.get_weighted_score' missing type hints
- 🔵 **Line 140**: Method 'RubricCriterion.get_weighted_max_score' missing type hints
- 🔵 **Line 226**: Method 'RubricGrade.get_normalized_score' missing type hints
- 🔵 **Line 248**: Method 'RubricGrade.get_raw_weighted_score' missing type hints
- 🔵 **Line 256**: Method 'RubricGrade.get_max_weighted_score' missing type hints
- 🔵 **Line 294**: Method 'RubricGrade.get_criteria_summary' missing type hints
- 🔵 **Line 339**: Method 'RubricGrade.get_improvement_suggestions' missing type hints
- 🔵 **Line 358**: Method 'RubricGrade.to_display_string' missing type hints

### src/haive/agents/common/models/grade/numeric.py

- 🔵 **Line 82**: Method 'NumericGrade.validate_score_range' missing type hints
- 🔵 **Line 110**: Method 'NumericGrade.get_normalized_score' missing type hints
- 🔵 **Line 122**: Method 'NumericGrade.get_percentage_score' missing type hints
- 🔵 **Line 150**: Method 'NumericGrade.get_letter_equivalent' missing type hints
- 🔵 **Line 190**: Method 'NumericGrade.to_display_string' missing type hints
- 🔵 **Line 304**: Method 'PercentageGrade.get_normalized_score' missing type hints
- 🔵 **Line 314**: Method 'PercentageGrade.get_percentage_score' missing type hints
- 🔵 **Line 324**: Method 'PercentageGrade.to_display_string' missing type hints

### src/haive/agents/common/models/grade/scale.py

- 🔵 **Line 144**: Method 'ScaleGrade.validate_scale_value_and_set_numeric' missing type hints
- 🔵 **Line 168**: Method 'ScaleGrade.get_normalized_score' missing type hints
- 🔵 **Line 184**: Method 'ScaleGrade.get_scale_position' missing type hints
- 🔵 **Line 192**: Method 'ScaleGrade.get_scale_percentage' missing type hints
- 🔵 **Line 239**: Method 'ScaleGrade.distance_from_neutral' missing type hints
- 🔵 **Line 249**: Method 'ScaleGrade.get_descriptive_assessment' missing type hints
- 🔵 **Line 267**: Method 'ScaleGrade.get_adjacent_values' missing type hints
- 🔵 **Line 286**: Method 'ScaleGrade.to_display_string' missing type hints

### src/haive/agents/common/models/grade/qualitative.py

- 🔵 **Line 182**: Method 'QualitativeGrade.validate_feedback_consistency' missing type hints
- 🔵 **Line 218**: Method 'QualitativeGrade.get_normalized_score' missing type hints
- 🔵 **Line 259**: Method 'QualitativeGrade.get_feedback_summary' missing type hints
- 🔵 **Line 298**: Method 'QualitativeGrade.get_improvement_priority' missing type hints
- 🔵 **Line 322**: Method 'QualitativeGrade.generate_narrative_summary' missing type hints
- 🔵 **Line 350**: Method 'QualitativeGrade.to_display_string' missing type hints

### src/haive/agents/common/models/grade/letter_grade.py

- 🔵 **Line 187**: Method 'LetterGrade.get_normalized_score' missing type hints
- 🔵 **Line 214**: Method 'LetterGrade.get_gpa_points' missing type hints
- 🔵 **Line 302**: Method 'LetterGrade.get_letter_quality_description' missing type hints
- 🔵 **Line 326**: Method 'LetterGrade.to_display_string' missing type hints

### src/haive/agents/common/models/grade/binary.py

- 🔵 **Line 121**: Method 'BinaryGrade.get_normalized_score' missing type hints
- 🔵 **Line 143**: Method 'BinaryGrade.get_display_value' missing type hints
- 🔵 **Line 151**: Method 'BinaryGrade.get_emoji_representation' missing type hints
- 🔵 **Line 174**: Method 'BinaryGrade.flip' missing type hints
- 🔵 **Line 190**: Method 'BinaryGrade.to_display_string' missing type hints

### src/haive/agents/base/mixins/hooks_mixin.py

- 🔵 **Line 177**: Method 'HooksMixin.clear_hook_results' missing type hints
- 🔵 **Line 197**: Method 'HooksMixin.enable_hooks' missing type hints
- 🔵 **Line 201**: Method 'HooksMixin.disable_hooks' missing type hints
- 🔵 **Line 205**: Method 'HooksMixin.list_hooks' missing type hints
- 🔵 **Line 223**: Function 'hook' missing type hints
- 🟡 **Line 239**: Function 'decorator' missing docstring

### src/haive/agents/base/mixins/persistence_mixin.py

- 🔵 **Line 321**: Method 'PersistenceMixin.get_persistence_config' missing type hints
- 🔵 **Line 332**: Method 'PersistenceMixin.update_persistence_config' missing type hints
- 🔵 **Line 348**: Method 'PersistenceMixin.get_effective_runnable_config' missing type hints
- 🟡 **Line 196**: Class 'PersistenceConfig' missing docstring
- 🟡 **Line 233**: Class 'PersistenceConfig' missing docstring
- 🟡 **Line 304**: Class 'PersistenceConfig' missing docstring

### src/haive/agents/base/mixins/state_mixin.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 339**: Method 'StateMixin.get_state_filename' missing type hints

### src/haive/agents/base/mixins/reasoning_mixin.py

- 🔵 **Line 81**: Method 'ReasoningMixin.get_available_tools' missing type hints
- 🔵 **Line 113**: Method 'ReasoningMixin.has_reasoning_capability' missing type hints
- 🔵 **Line 126**: Method 'ReasoningMixin.get_reasoning_metrics' missing type hints

### src/haive/agents/base/mixins/execution_mixin.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/task_analysis/complexity/engines.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/task_analysis/complexity/models.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 64**: Method 'ComplexityVector.determine_level' missing type hints
- 🔵 **Line 83**: Method 'ComplexityVector.validate_scores' missing type hints

### src/haive/agents/task_analysis/complexity/prompts.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/task_analysis/base/models.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 141**: Method 'TaskNode.calculate_total_duration' missing type hints
- 🔵 **Line 159**: Method 'TaskNode.get_all_steps' missing type hints
- 🔵 **Line 215**: Method 'TaskPlan.calculate_stats' missing type hints

### src/haive/agents/task_analysis/base/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/task_analysis/decomposer/engines.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/task_analysis/decomposer/models.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/task_analysis/decomposer/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/task_analysis/decomposer/prompts.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/task_analysis/decomposer/prompt.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/task_analysis/tree/engines.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/task_analysis/tree/models.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 169**: Method 'TaskTree.get_join_points' missing type hints
- 🔵 **Line 173**: Method 'TaskTree.get_parallel_groups' missing type hints
- 🔵 **Line 177**: Method 'TaskTree.get_critical_path' missing type hints
- 🔵 **Line 181**: Method 'TaskTree.get_execution_phases' missing type hints
- 🔵 **Line 258**: Method 'TaskTree.get_analysis_summary' missing type hints

### src/haive/agents/task_analysis/tree/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/task_analysis/tree/prompts.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/task_analysis/analysis/engines.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/task_analysis/analysis/models.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/task_analysis/analysis/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/task_analysis/analysis/prompts.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/task_analysis/execution/engines.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/task_analysis/execution/models.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 51**: Method 'ExecutionPhase.add_task' missing type hints
- 🔵 **Line 144**: Method 'ExecutionPlan.add_phase' missing type hints
- 🔵 **Line 150**: Method 'ExecutionPlan.calculate_critical_path' missing type hints

### src/haive/agents/task_analysis/execution/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/task_analysis/execution/prompts.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/task_analysis/context/engines.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/task_analysis/context/models.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/task_analysis/context/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/task_analysis/context/prompts.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/planning/plan_and_execute/state.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 19**: Method 'PlanAndExecuteState.update_past_steps' missing type hints
- 🔵 **Line 26**: Method 'PlanAndExecuteState.get_next_step' missing type hints
- 🔵 **Line 32**: Method 'PlanAndExecuteState.is_plan_complete' missing type hints

### src/haive/agents/planning/plan_and_execute/engines.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/planning/plan_and_execute/config.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 9**: Class 'PlanAndExecuteConfig' missing docstring

### src/haive/agents/planning/plan_and_execute/models.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 18**: Method 'Step.add_result' missing type hints
- 🔵 **Line 23**: Method 'Step.is_complete' missing type hints
- 🔵 **Line 29**: Method 'Step.remove_completed_substeps' missing type hints
- 🔵 **Line 60**: Method 'Plan.update_status' missing type hints
- 🔵 **Line 69**: Method 'Plan.add_step' missing type hints
- 🔵 **Line 73**: Method 'Plan.remove_completed_steps' missing type hints
- 🔵 **Line 79**: Method 'Plan.get_last_incomplete_step' missing type hints

### src/haive/agents/planning/plan_and_execute/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/planning/plan_and_execute/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 14**: Class 'PlanAndExecuteAgent' missing docstring
- 🔵 **Line 40**: Method 'PlanAndExecuteAgent.setup_workflow' missing docstring
- 🔵 **Line 40**: Method 'PlanAndExecuteAgent.setup_workflow' missing type hints
- 🔵 **Line 140**: Method 'PlanAndExecuteAgent.should_end' missing type hints

### src/haive/agents/planning/rewoo/state.py

- 🔵 **Line 28**: Method 'ReWOOState.get_current_step' missing type hints
- 🔵 **Line 43**: Method 'ReWOOState.is_plan_complete' missing type hints

### src/haive/agents/planning/rewoo/config.py

- 🟡 **Line 10**: Class 'Configuration' missing docstring

### src/haive/agents/planning/rewoo/models.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 21**: Method 'ToolCall.set_available_tools' missing type hints
- 🔵 **Line 27**: Method 'ToolCall.validate_tool_name' missing type hints
- 🔵 **Line 36**: Method 'ToolCall.validate_tool_input' missing type hints
- 🔵 **Line 60**: Method 'RewooStep.validate_evidence_ref' missing type hints
- 🔵 **Line 74**: Method 'RewooPlan.add_rewoo_step' missing type hints
- 🔵 **Line 78**: Method 'RewooPlan.remove_completed_steps' missing type hints
- 🔵 **Line 82**: Method 'RewooPlan.update_evidence_references' missing type hints

### src/haive/agents/planning/rewoo/graph.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/planning/rewoo/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/planning/rewoo/utils.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/planning/rewoo/agent.py

- 🔵 **Line 85**: Method 'RewooAgentConfig.validate_and_register_tools' missing type hints
- 🔵 **Line 112**: Method 'RewooAgentConfig.format_planning_prompt_with_tools' missing type hints
- 🔵 **Line 565**: Method 'RewooAgent.setup_workflow' missing type hints

### src/haive/agents/planning/rewoo/prompts.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/planning/rewoo/tools.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/planning/models/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition
- 🔵 **Line 96**: Method 'ResourceRequirement.validate_minimum' missing type hints
- 🔵 **Line 153**: Method 'ExecutionMetrics.duration_seconds' missing type hints
- 🔵 **Line 161**: Method 'ExecutionMetrics.success_rate' missing type hints
- 🔵 **Line 310**: Method 'PlanNode.validate_dependencies' missing type hints
- 🔵 **Line 366**: Method 'PlanNode.estimate_total_tokens' missing type hints
- 🔵 **Line 374**: Method 'PlanNode.to_dict' missing type hints

### src/haive/agents/planning/llm_compiler/state.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 31**: Method 'CompilerState.get_highest_step_id' missing type hints
- 🔵 **Line 37**: Method 'CompilerState.get_executable_steps' missing type hints
- 🔵 **Line 43**: Method 'CompilerState.all_steps_complete' missing type hints
- 🔵 **Line 49**: Method 'CompilerState.has_join_result' missing type hints

### src/haive/agents/planning/llm_compiler/config.py

- 🔵 **Line 232**: Method 'LLMCompilerAgentConfig.validate_configs' missing type hints

### src/haive/agents/planning/llm_compiler/models.py

- 🔵 **Line 52**: Method 'CompilerTask.is_join' missing type hints
- 🔵 **Line 98**: Method 'CompilerStep.dependencies' missing type hints
- 🔵 **Line 182**: Method 'CompilerPlan.get_join_step' missing type hints

### src/haive/agents/planning/llm_compiler/utils.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 10**: Function 'schedule_pending_task' missing docstring
- 🔵 **Line 10**: Function 'schedule_pending_task' missing type hints
- 🟡 **Line 146**: Function 'schedule_task' missing docstring
- 🔵 **Line 146**: Function 'schedule_task' missing type hints
- 🟡 **Line 158**: Function 'schedule_pending_task' missing docstring
- 🔵 **Line 158**: Function 'schedule_pending_task' missing type hints
- 🟡 **Line 129**: Function 'replace_match' missing docstring
- 🔵 **Line 129**: Function 'replace_match' missing type hints

### src/haive/agents/planning/llm_compiler/agent.py

- 🔵 **Line 379**: Method 'LLMCompilerAgent.should_execute_more' missing type hints
- 🔵 **Line 405**: Method 'LLMCompilerAgent.setup_workflow' missing type hints
- 🔵 **Line 462**: Method 'LLMCompilerAgent.run' missing type hints
- 🔵 **Line 524**: Method 'LLMCompilerAgent.stream' missing type hints
- 🟡 **Line 549**: Function 'main' missing docstring
- 🔵 **Line 549**: Function 'main' missing type hints

### src/haive/agents/planning/llm_compiler/output_parser.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 59**: Function 'default_dependency_rule' missing docstring
- 🔵 **Line 59**: Function 'default_dependency_rule' missing type hints
- 🟡 **Line 74**: Class 'Task' missing docstring
- 🟡 **Line 82**: Function 'instantiate_task' missing docstring
- 🔵 **Line 128**: Method 'LLMCompilerPlanParser.parse' missing docstring
- 🔵 **Line 131**: Method 'LLMCompilerPlanParser.stream' missing docstring
- 🔵 **Line 139**: Method 'LLMCompilerPlanParser.ingest_token' missing docstring

### src/haive/agents/planning/llm_compiler/tools/math_tools.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 97**: Function 'get_math_tool' missing docstring
- 🔵 **Line 97**: Function 'get_math_tool' missing type hints
- 🟡 **Line 107**: Function 'calculate_expression' missing docstring
- 🔵 **Line 107**: Function 'calculate_expression' missing type hints

### src/haive/agents/simple/structured/config.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 29**: Method 'StructuredOutputAgentConfig.validate_and_setup' missing type hints

### src/haive/agents/simple/structured/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/simple/structured/agent.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/simple/v2/config.py

- 🔵 **Line 40**: Method 'SimpleAgent.setup_workflow' missing type hints
- 🔵 **Line 91**: Method 'SimpleAgent.has_messages_input' missing type hints

### src/haive/agents/simple/v2/graph.py

- 🔴 **Line 1**: Could not parse file: invalid syntax (<unknown>, line 9)

### src/haive/agents/simple/v2/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/rag/agentic_router/agent.py

- 🔵 **Line 371**: Method 'AgenticRAGRouterAgent.setup_agent' missing type hints
- 🔵 **Line 561**: Method 'AgenticRAGRouterAgent.build_graph' missing type hints
- 🔵 **Line 603**: Method 'AgenticRAGRouterAgent.from_documents' missing type hints
- 🔵 **Line 670**: Function 'get_agentic_rag_router_io_schema' missing type hints

### src/haive/agents/rag/agentic_router/agent_chain.py

- 🔵 **Line 185**: Function 'get_agentic_router_chain_io_schema' missing type hints

### src/haive/agents/rag/agentic_router/agent_v2.py

- 🔵 **Line 71**: Method 'AgenticRAGRouterV2.build_graph' missing type hints

### src/haive/agents/rag/fusion/agent.py

- 🔵 **Line 145**: Method 'ReciprocalRankFusionAgent.build_graph' missing type hints
- 🔵 **Line 304**: Method 'RAGFusionAgent.from_documents' missing type hints
- 🔵 **Line 375**: Function 'create_multi_query_retrieval_callable' missing type hints
- 🔵 **Line 463**: Method 'MultiQueryRetrievalAgent.build_graph' missing type hints
- 🔵 **Line 517**: Function 'get_rag_fusion_io_schema' missing type hints

### src/haive/agents/rag/multi_strategy/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/multi_strategy/config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/multi_strategy/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/rag/multi_strategy/query_types.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/multi_strategy/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 40**: Method 'MultiStrategyRAGAgent.analyze_query' missing type hints
- 🔵 **Line 75**: Method 'MultiStrategyRAGAgent.rewrite_query' missing type hints
- 🔵 **Line 101**: Method 'MultiStrategyRAGAgent.retrieve_with_strategy' missing type hints
- 🔵 **Line 123**: Method 'MultiStrategyRAGAgent.setup_workflow' missing type hints

### src/haive/agents/rag/base/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/base/base_agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 16**: Method 'BaseRAGAgent.retrieve' missing type hints
- 🔵 **Line 22**: Method 'BaseRAGAgent.generate_answer' missing type hints
- 🔵 **Line 36**: Method 'BaseRAGAgent.setup_workflow' missing type hints

### src/haive/agents/rag/base/config.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 52**: Method 'BaseRAGConfig.setup_engine' missing type hints

### src/haive/agents/rag/base/models.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 4**: Class 'Query' missing docstring

### src/haive/agents/rag/base/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/rag/base/utils.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/base/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 47**: Method 'BaseRAGAgent.build_graph' missing type hints

### src/haive/agents/rag/base/branches.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/base/prompts.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/self_reflective/agent.py

- 🔵 **Line 332**: Method 'SelfReflectiveRAGAgent.setup_agent' missing type hints
- 🔵 **Line 386**: Method 'SelfReflectiveRAGAgent.from_documents' missing type hints
- 🔵 **Line 575**: Method 'SelfReflectiveRAGAgent.build_graph' missing type hints
- 🔵 **Line 643**: Function 'get_self_reflective_rag_io_schema' missing type hints

### src/haive/agents/rag/self_rag2/nodes.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 6**: Function 'retrieve' missing type hints
- 🔵 **Line 23**: Function 'generate' missing type hints
- 🔵 **Line 41**: Function 'grade_documents' missing type hints
- 🔵 **Line 70**: Function 'transform_query' missing type hints
- 🔵 **Line 91**: Function 'transform_query' missing type hints

### src/haive/agents/rag/self_rag2/graph.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/self_rag2/configuration.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/self_rag2/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/rag/self_rag2/prompts.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/flare/agent.py

- 🔵 **Line 238**: Function 'create_flare_planner_callable' missing type hints
- 🔵 **Line 305**: Function 'create_active_retrieval_callable' missing type hints
- 🔵 **Line 371**: Method 'FLAREPlannerAgent.build_graph' missing type hints
- 🔵 **Line 393**: Method 'ActiveRetrievalAgent.build_graph' missing type hints
- 🔵 **Line 414**: Method 'FLARERAGAgent.from_documents' missing type hints
- 🔵 **Line 529**: Function 'get_flare_rag_io_schema' missing type hints

### src/haive/agents/rag/document_grading/agent.py

- 🔵 **Line 78**: Method 'DocumentGradingAgent.build_graph' missing type hints
- 🔵 **Line 127**: Method 'DocumentGradingRAGAgent.from_documents' missing type hints

### src/haive/agents/rag/factories/rag_workflow_factory.py

- 🔵 **Line 31**: Method 'GenericCallableAgent.build_graph' missing type hints
- 🔵 **Line 66**: Method 'ConditionalCallableAgent.build_graph' missing type hints
- 🟡 **Line 146**: Function 'self_rag_router' missing docstring
- 🟡 **Line 171**: Function 'retrieval_decision' missing docstring
- 🟡 **Line 239**: Function 'adaptive_router' missing docstring
- 🔵 **Line 239**: Function 'adaptive_router' missing type hints
- 🟡 **Line 257**: Class 'AdaptiveRAGAgent' missing docstring

### src/haive/agents/rag/factories/compatible_rag_factory.py

- 🔵 **Line 882**: Method 'CompatibleRAGFactory.build_graph' missing type hints
- 🔵 **Line 1455**: Function 'example_modular_rag_usage' missing type hints
- 🟡 **Line 1246**: Function 'self_rag_retrieval_decision' missing docstring
- 🟡 **Line 1359**: Class 'CompatibleAdaptiveRAG' missing docstring

### src/haive/agents/rag/adaptive_rag/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/rag/adaptive_rag/agent.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/adaptive/agent.py

- 🔵 **Line 87**: Method 'AdaptiveRAGAgent.from_documents' missing type hints

### src/haive/agents/rag/step_back/agent.py

- 🔵 **Line 177**: Method 'StepBackQueryGeneratorAgent.build_graph' missing type hints
- 🔵 **Line 267**: Method 'DualRetrievalAgent.build_graph' missing type hints
- 🔵 **Line 360**: Method 'StepBackRAGAgent.from_documents' missing type hints
- 🔵 **Line 454**: Function 'get_step_back_rag_io_schema' missing type hints

### src/haive/agents/rag/memory_aware/agent.py

- 🔵 **Line 79**: Method 'MemoryRetrievalAgent.build_graph' missing type hints
- 🔵 **Line 134**: Method 'MemoryAwareRAGAgent.from_documents' missing type hints
- 🔵 **Line 205**: Function 'get_memory_aware_rag_io_schema' missing type hints

### src/haive/agents/rag/hyde/models.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/hyde/enhanced_agent_v2.py

- 🔵 **Line 102**: Method 'EnhancedHyDERAGAgentV2.setup_hyde_agent' missing type hints
- 🔵 **Line 596**: Method 'EnhancedHyDERetrieverV2.build_graph' missing docstring
- 🔵 **Line 596**: Method 'EnhancedHyDERetrieverV2.build_graph' missing type hints
- 🔵 **Line 670**: Method 'EnsembleHyDERetriever.build_graph' missing docstring
- 🔵 **Line 670**: Method 'EnsembleHyDERetriever.build_graph' missing type hints
- 🔵 **Line 762**: Method 'MultiDomainHyDERetriever.build_graph' missing docstring
- 🔵 **Line 762**: Method 'MultiDomainHyDERetriever.build_graph' missing type hints

### src/haive/agents/rag/hyde/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/rag/hyde/agent.py

- 🔴 **Line 1**: Could not parse file: 'utf-8' codec can't decode byte 0x92 in position 191: invalid start byte

### src/haive/agents/rag/hyde/enhanced_agent.py

- 🔵 **Line 77**: Method 'EnhancedHyDERAGAgent.from_documents' missing type hints
- 🔵 **Line 235**: Method 'EnhancedHyDERetriever.build_graph' missing type hints
- 🔵 **Line 341**: Function 'demonstrate_enhancement_vs_traditional' missing type hints

### src/haive/agents/rag/hyde/prompts.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/hyde/agent_v2.py

- 🔵 **Line 78**: Method 'HyDERetrieverAgent.build_graph' missing type hints
- 🔵 **Line 131**: Method 'HyDERAGAgentV2.from_documents' missing type hints

### src/haive/agents/rag/simple/agent.py

- 🔵 **Line 23**: Method 'SimpleRAGAgent.from_documents' missing type hints

### src/haive/agents/rag/multi_agent_rag/state.py

- 🔵 **Line 239**: Method 'MultiAgentRAGState.update_quality_metrics' missing type hints
- 🔵 **Line 252**: Method 'MultiAgentRAGState.should_refine_query' missing type hints

### src/haive/agents/rag/multi_agent_rag/additional_workflows.py

- 🔵 **Line 99**: Method 'SimpleRAGWithMemoryAgent.build_custom_graph' missing type hints
- 🔵 **Line 170**: Method 'SelfRAGAgent.build_custom_graph' missing type hints
- 🔵 **Line 237**: Method 'MultiQueryRAGAgent.build_custom_graph' missing type hints
- 🔵 **Line 310**: Method 'RAGFusionAgent.build_custom_graph' missing type hints
- 🔵 **Line 384**: Method 'StepBackPromptingRAGAgent.build_custom_graph' missing type hints
- 🔵 **Line 453**: Method 'QueryDecompositionRAGAgent.build_custom_graph' missing type hints

### src/haive/agents/rag/multi_agent_rag/enhanced_workflows.py

- 🔵 **Line 32**: Method 'DocumentGradingAgent.build_graph' missing type hints
- 🔵 **Line 54**: Method 'RequeryDecisionAgent.build_graph' missing type hints

### src/haive/agents/rag/multi_agent_rag/compatibility.py

- 🔵 **Line 240**: Method 'SafeCompatibilityTester.test_rag_agents_safely' missing type hints
- 🔵 **Line 585**: Function 'safe_test_rag_compatibility' missing type hints
- 🟡 **Line 545**: Class 'BasicResult' missing docstring

### src/haive/agents/rag/multi_agent_rag/specialized_workflows_v2.py

- 🔵 **Line 108**: Method 'FLAREAgentV2.build_custom_graph' missing type hints
- 🔵 **Line 203**: Method 'DynamicRAGAgentV2.build_custom_graph' missing type hints
- 🔵 **Line 317**: Method 'DebateRAGAgentV2.build_custom_graph' missing type hints
- 🔵 **Line 412**: Method 'AdaptiveThresholdRAGAgentV2.build_custom_graph' missing type hints

### src/haive/agents/rag/multi_agent_rag/specialized_workflows.py

- 🔵 **Line 150**: Method 'FLAREAgent.build_custom_graph' missing type hints
- 🔵 **Line 252**: Method 'DynamicRAGAgent.build_custom_graph' missing type hints
- 🔵 **Line 364**: Method 'DebateRAGAgent.build_custom_graph' missing type hints
- 🔵 **Line 469**: Method 'AdaptiveThresholdRAGAgent.build_custom_graph' missing type hints

### src/haive/agents/rag/multi_agent_rag/advanced_workflows.py

- 🔵 **Line 117**: Method 'GraphRAGAgent.build_custom_graph' missing type hints
- 🔵 **Line 194**: Method 'AgenticGraphRAGAgent.build_custom_graph' missing type hints
- 🔵 **Line 270**: Method 'AgenticRAGRouterAgent.build_custom_graph' missing type hints
- 🔵 **Line 331**: Method 'QueryPlanningAgenticRAGAgent.build_custom_graph' missing type hints
- 🔵 **Line 410**: Method 'SelfReflectiveAgenticRAGAgent.build_custom_graph' missing type hints
- 🔵 **Line 486**: Method 'SpeculativeRAGAgent.build_custom_graph' missing type hints
- 🔵 **Line 556**: Method 'SelfRouteRAGAgent.build_custom_graph' missing type hints

### src/haive/agents/rag/multi_agent_rag/graded_rag_workflows_v2.py

- 🔵 **Line 119**: Method 'FullyGradedRAGAgentV2.build_custom_graph' missing type hints
- 🔵 **Line 240**: Method 'FLAREAgentV2Example.build_custom_graph' missing type hints

### src/haive/agents/rag/multi_agent_rag/multi_rag.py

- 🔵 **Line 359**: Function 'test_agent_compatibility' missing type hints

### src/haive/agents/rag/multi_agent_rag/simple_enhanced_workflows.py

- 🔵 **Line 31**: Method 'DocumentGradingAgent.build_graph' missing type hints
- 🔵 **Line 53**: Method 'RequeryDecisionAgent.build_graph' missing type hints

### src/haive/agents/rag/multi_agent_rag/enhanced_multi_rag.py

- 🔵 **Line 354**: Function 'demonstrate_enhanced_rag_compatibility' missing type hints

### src/haive/agents/rag/multi_agent_rag/graded_rag_workflows.py

- 🔵 **Line 162**: Method 'FullyGradedRAGAgent.build_custom_graph' missing type hints
- 🔵 **Line 260**: Method 'AdaptiveGradedRAGAgent.build_custom_graph' missing type hints
- 🔵 **Line 355**: Method 'MultiCriteriaGradedRAGAgent.build_custom_graph' missing type hints
- 🔵 **Line 432**: Method 'ReflexiveGradedRAGAgent.build_custom_graph' missing type hints

### src/haive/agents/rag/multi_agent_rag/agents.py

- 🔵 **Line 135**: Method 'SimpleRAGAgent.documents' missing type hints
- 🔵 **Line 140**: Method 'SimpleRAGAgent.documents' missing type hints
- 🔵 **Line 145**: Method 'SimpleRAGAgent.max_documents' missing type hints
- 🔵 **Line 150**: Method 'SimpleRAGAgent.max_documents' missing type hints
- 🔵 **Line 227**: Method 'SimpleRAGAnswerAgent.use_citations' missing type hints
- 🔵 **Line 232**: Method 'SimpleRAGAnswerAgent.use_citations' missing type hints
- 🔵 **Line 309**: Method 'DocumentGradingAgent.grading_mode' missing type hints
- 🔵 **Line 314**: Method 'DocumentGradingAgent.grading_mode' missing type hints
- 🔵 **Line 319**: Method 'DocumentGradingAgent.min_relevance_threshold' missing type hints
- 🔵 **Line 324**: Method 'DocumentGradingAgent.min_relevance_threshold' missing type hints

### src/haive/agents/rag/dynamic/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/dynamic/config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/dynamic/models.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 14**: Method 'DataSourceConfig.create_retriever' missing type hints

### src/haive/agents/rag/dynamic/data_source_types.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/dynamic/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 48**: Method 'DynamicRAGAgent.route_query' missing type hints
- 🔵 **Line 125**: Method 'DynamicRAGAgent.retrieve_from_sources' missing type hints
- 🔵 **Line 193**: Method 'DynamicRAGAgent.merge_results' missing type hints
- 🔵 **Line 261**: Method 'DynamicRAGAgent.setup_workflow' missing type hints

### src/haive/agents/rag/self_route/agent.py

- 🔵 **Line 340**: Method 'QueryAnalyzerAgent.build_graph' missing type hints
- 🔵 **Line 460**: Method 'IterativePlannerAgent.build_graph' missing type hints
- 🔵 **Line 566**: Method 'RoutingDecisionAgent.build_graph' missing type hints
- 🔵 **Line 635**: Method 'SelfRouteRAGAgent.from_documents' missing type hints
- 🔵 **Line 753**: Function 'get_self_route_rag_io_schema' missing type hints

### src/haive/agents/rag/typed/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/typed/config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/typed/query_types.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/typed/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 51**: Method 'TypedRAGAgent.classify_query' missing type hints
- 🔵 **Line 93**: Method 'TypedRAGAgent.generate_subqueries' missing type hints
- 🔵 **Line 136**: Method 'TypedRAGAgent.retrieve_for_subqueries' missing type hints
- 🔵 **Line 161**: Method 'TypedRAGAgent.filter_documents' missing type hints
- 🔵 **Line 169**: Method 'TypedRAGAgent.aggregate_answers' missing type hints
- 🔵 **Line 218**: Method 'TypedRAGAgent.generate_answer' missing type hints
- 🔵 **Line 249**: Method 'TypedRAGAgent.setup_workflow' missing type hints

### src/haive/agents/rag/utils/structured_output_enhancer.py

- 🔵 **Line 61**: Method 'StructuredOutputEnhancer.create_format_instructions' missing type hints
- 🔵 **Line 179**: Function 'create_hyde_enhancer' missing type hints
- 🔵 **Line 188**: Function 'create_fusion_enhancer' missing type hints
- 🔵 **Line 197**: Function 'create_speculative_enhancer' missing type hints
- 🔵 **Line 206**: Function 'create_memory_enhancer' missing type hints
- 🔵 **Line 216**: Function 'demonstrate_enhancement_patterns' missing type hints

### src/haive/agents/rag/adaptive_tools/agent.py

- 🔵 **Line 287**: Function 'create_tool_selector_callable' missing type hints
- 🔵 **Line 338**: Function 'create_google_search_callable' missing type hints
- 🔵 **Line 390**: Function 'create_adaptive_synthesis_callable' missing type hints
- 🔵 **Line 469**: Method 'ToolSelectionAgent.build_graph' missing type hints
- 🔵 **Line 490**: Method 'SearchIntegrationAgent.build_graph' missing type hints
- 🔵 **Line 509**: Method 'AdaptiveToolsRAGAgent.from_documents' missing type hints
- 🔵 **Line 609**: Function 'get_adaptive_tools_rag_io_schema' missing type hints

### src/haive/agents/rag/query_decomposition/agent.py

- 🔵 **Line 288**: Method 'QueryDecomposerAgent.build_graph' missing type hints
- 🔵 **Line 375**: Method 'HierarchicalQueryDecomposerAgent.build_graph' missing type hints
- 🔵 **Line 460**: Method 'ContextualQueryDecomposerAgent.build_graph' missing type hints
- 🔵 **Line 554**: Method 'AdaptiveQueryDecomposerAgent.build_graph' missing type hints
- 🔵 **Line 673**: Function 'get_query_decomposer_io_schema' missing type hints

### src/haive/agents/rag/db_rag/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/rag/filtered/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/filtered/config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/filtered/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/rag/filtered/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 55**: Method 'FilteredRAGAgent.retriever' missing type hints
- 🔵 **Line 207**: Method 'FilteredRAGAgent.setup_workflow' missing type hints

### src/haive/agents/rag/speculative/agent.py

- 🔵 **Line 370**: Method 'HypothesisGeneratorAgent.build_graph' missing type hints
- 🔵 **Line 497**: Method 'ParallelVerificationAgent.build_graph' missing type hints
- 🔵 **Line 678**: Method 'SpeculativeRAGAgent.from_documents' missing type hints
- 🔵 **Line 773**: Function 'get_speculative_rag_io_schema' missing type hints

### src/haive/agents/rag/hallucination_grading/agent.py

- 🔵 **Line 249**: Method 'HallucinationGraderAgent.build_graph' missing type hints
- 🔵 **Line 344**: Method 'AdvancedHallucinationGraderAgent.build_graph' missing type hints
- 🔵 **Line 455**: Method 'RealtimeHallucinationGraderAgent.build_graph' missing type hints
- 🔵 **Line 546**: Function 'get_hallucination_grader_io_schema' missing type hints

### src/haive/agents/rag/query_planning/agent.py

- 🔵 **Line 353**: Method 'QueryPlanningRAGAgent.setup_agent' missing type hints
- 🔵 **Line 385**: Method 'QueryPlanningRAGAgent.from_documents' missing type hints
- 🔵 **Line 572**: Method 'QueryPlanningRAGAgent.build_graph' missing type hints
- 🔵 **Line 632**: Function 'get_query_planning_rag_io_schema' missing type hints

### src/haive/agents/rag/query_planning/agent_chain.py

- 🔵 **Line 195**: Function 'get_query_planning_chain_io_schema' missing type hints
- 🟡 **Line 128**: Function 'answer_all' missing docstring

### src/haive/agents/rag/agentic/agent.py

- 🔵 **Line 98**: Method 'AgenticRAGAgent.setup_agentic_rag' missing type hints
- 🔵 **Line 285**: Method 'AgenticRAGAgent.state_schema' missing type hints

### src/haive/agents/rag/self_corr/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/self_corr/engines.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/self_corr/config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/self_corr/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/rag/self_corr/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 66**: Method 'SelfCorrectiveRAGAgent.retriever' missing type hints
- 🔵 **Line 413**: Method 'SelfCorrectiveRAGAgent.setup_workflow' missing type hints

### src/haive/agents/rag/corrective/agent.py

- 🔵 **Line 60**: Method 'CorrectiveRAGAgent.from_documents' missing type hints

### src/haive/agents/rag/corrective/agent_v2.py

- 🔵 **Line 69**: Method 'CorrectiveRAGAgentV2.from_documents' missing type hints

### src/haive/agents/rag/llm_rag/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/llm_rag/config.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 81**: Method 'LLMRAGConfig.setup_engines' missing type hints

### src/haive/agents/rag/llm_rag/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/rag/llm_rag/engine.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/llm_rag/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 27**: Method 'LLMRAGAgent.setup_workflow' missing type hints

### src/haive/agents/rag/llm_rag/example.py

- 🔵 **Line 56**: Function 'create_llm_rag_agent' missing type hints
- 🔵 **Line 140**: Function 'run_example_queries' missing type hints
- 🔵 **Line 185**: Function 'compare_agent_configurations' missing type hints
- 🔵 **Line 220**: Function 'main' missing type hints

### src/haive/agents/rag/multi_query/agent.py

- 🔵 **Line 62**: Method 'MultiRetrievalAgent.build_graph' missing type hints
- 🔵 **Line 141**: Method 'MultiQueryRAGAgent.from_documents' missing type hints

### src/haive/agents/rag/common/document_graders/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/rag/common/hallucination_graders/models.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/common/hallucination_graders/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/rag/common/hallucination_graders/prompts.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/common/query_refinement/models.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/common/query_refinement/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/rag/common/query_refinement/prompt.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/common/answer_generators/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/rag/common/answer_generators/prompts.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/common/document_graders/binary_grader/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/rag/common/document_graders/binary_grader/prompt.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/common/document_graders/comprehensive_grader/models.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/common/document_graders/comprehensive_grader/prompt.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/common/query_constructors/flare/models.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/common/query_constructors/flare/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/rag/common/query_constructors/flare/prompt.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/common/query_constructors/hyde/models.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 18**: Method 'HypotheticalDocument.to_query' missing type hints

### src/haive/agents/rag/common/query_constructors/hyde/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/rag/common/query_constructors/hyde/prompt.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/self_rag2/nodes/grade_documents.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/self_rag2/nodes/generate.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 1**: Function 'generate' missing type hints

### src/haive/agents/rag/self_rag2/nodes/grade_generation_v_documents_and_question.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 1**: Function 'grade_generation_v_documents_and_question' missing type hints

### src/haive/agents/rag/self_rag2/nodes/decide_to_generate.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 1**: Function 'decide_to_generate' missing type hints

### src/haive/agents/rag/self_rag2/nodes/retreive.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 1**: Function 'retrieve' missing type hints

### src/haive/agents/rag/self_rag2/nodes/transform_query.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 1**: Function 'transform_query' missing type hints

### src/haive/agents/rag/db_rag/sql_rag/config.py

- 🔵 **Line 159**: Method 'SQLDatabaseConfig.get_connection_string' missing type hints
- 🔵 **Line 194**: Method 'SQLDatabaseConfig.get_sql_db' missing type hints
- 🔵 **Line 234**: Method 'SQLDatabaseConfig.get_db_schema' missing type hints

### src/haive/agents/rag/db_rag/sql_rag/models.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/db_rag/sql_rag/agent.py

- 🔵 **Line 959**: Method 'SQLRAGAgent.setup_workflow' missing type hints

### src/haive/agents/rag/db_rag/sql_rag/example.py

- 🔵 **Line 58**: Function 'basic_example' missing type hints
- 🔵 **Line 93**: Function 'postgresql_example' missing type hints
- 🔵 **Line 147**: Function 'sqlite_example' missing type hints
- 🔵 **Line 187**: Function 'mysql_example' missing type hints
- 🔵 **Line 249**: Function 'error_handling_example' missing type hints
- 🔵 **Line 285**: Function 'custom_llm_example' missing type hints
- 🔵 **Line 334**: Function 'batch_processing_example' missing type hints
- 🔵 **Line 404**: Function 'interactive_mode' missing type hints
- 🔵 **Line 473**: Function 'main' missing type hints

### src/haive/agents/rag/db_rag/graph_db/config.py

- 🔵 **Line 105**: Method 'GraphDBConfig.get_graph_db' missing type hints
- 🔵 **Line 140**: Method 'GraphDBConfig.get_graph_db_schema' missing type hints

### src/haive/agents/rag/db_rag/graph_db/models.py

- 🔵 **Line 72**: Method 'PropertyFilter.validate_filter_type' missing type hints
- 🔵 **Line 245**: Method 'GuardrailsOutput.validate_decision' missing type hints

### src/haive/agents/rag/db_rag/graph_db/agent.py

- 🔵 **Line 758**: Method 'GraphDBRAGAgent.setup_workflow' missing type hints

### src/haive/agents/rag/db_rag/graph_db/example.py

- 🔵 **Line 52**: Function 'basic_example' missing type hints
- 🔵 **Line 107**: Function 'streaming_example' missing type hints
- 🔵 **Line 198**: Function 'custom_domain_example' missing type hints
- 🔵 **Line 292**: Function 'batch_processing_example' missing type hints
- 🔵 **Line 400**: Function 'error_handling_example' missing type hints
- 🔵 **Line 477**: Function 'performance_monitoring_example' missing type hints
- 🔵 **Line 665**: Function 'main' missing type hints
- 🔵 **Line 737**: Function 'run_all_examples' missing type hints

### src/haive/agents/rag/db_rag/graph_db/branches.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/db_rag/graph_db/scratch.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/rag/db_rag/base/db_config.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 22**: Method 'BaseDBConfig.get_connection_string' missing type hints
- 🔵 **Line 26**: Method 'BaseDBConfig.get_db' missing type hints
- 🔵 **Line 30**: Method 'BaseDBConfig.get_db_schema' missing type hints

### src/haive/agents/rag/db_rag/base/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/document_loader/directory/agent.py

- 🔵 **Line 53**: Method 'DirectoryLoaderAgent.setup_agent' missing type hints

### src/haive/agents/document_loader/base/agent.py

- 🔵 **Line 81**: Method 'DocumentLoaderAgent.setup_agent' missing type hints
- 🔵 **Line 100**: Method 'DocumentLoaderAgent.build_graph' missing type hints

### src/haive/agents/document_loader/web/agent.py

- 🔵 **Line 50**: Method 'WebLoaderAgent.setup_agent' missing type hints

### src/haive/agents/document_loader/file/agent.py

- 🔵 **Line 43**: Method 'FileLoaderAgent.setup_agent' missing type hints

### src/haive/agents/document_loader/tests/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/document_loader/examples/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/document_loader/examples/usage_examples.py

- 🔵 **Line 16**: Function 'example_basic_document_loader' missing type hints
- 🔵 **Line 46**: Function 'example_file_loader' missing type hints
- 🔵 **Line 80**: Function 'example_web_loader' missing type hints
- 🔵 **Line 116**: Function 'example_directory_loader' missing type hints
- 🔵 **Line 187**: Function 'example_rag_integration' missing type hints

### src/haive/agents/dynamic/resources/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/dynamic/resources/unified_manager.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 190**: Method 'UnifiedResourceManager.get_vector_store' missing type hints
- 🔵 **Line 194**: Method 'UnifiedResourceManager.get_all_tools' missing type hints

### src/haive/agents/dynamic/resources/discovery.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 398**: Method 'ToolDiscovery.get_discovery_summary' missing type hints

### src/haive/agents/reasoning_and_critique/reflection/state.py

- 🔵 **Line 30**: Method 'ReflectionAgentState.last_human_message' missing type hints
- 🔵 **Line 38**: Method 'ReflectionAgentState.last_ai_message' missing type hints

### src/haive/agents/reasoning_and_critique/reflection/models.py

- 🔵 **Line 24**: Method 'ReflectionResult.normalized_score' missing type hints
- 🔵 **Line 28**: Method 'ReflectionResult.as_message' missing type hints

### src/haive/agents/reasoning_and_critique/reflection/agent.py

- 🔵 **Line 44**: Method 'ReflectionAgent.setup_workflow' missing type hints

### src/haive/agents/reasoning_and_critique/lats/state.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 5**: Class 'TreeState' missing docstring

### src/haive/agents/reasoning_and_critique/lats/node.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 40**: Method 'Node.serialize_model' missing type hints
- 🔵 **Line 58**: Method 'Node.get_path' missing type hints
- 🔵 **Line 97**: Method 'NodeManager.rebuild_references' missing type hints

### src/haive/agents/reasoning_and_critique/lats/models.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 9**: Class 'Reflection' missing docstring
- 🔵 **Line 23**: Method 'Reflection.as_message' missing docstring
- 🔵 **Line 23**: Method 'Reflection.as_message' missing type hints
- 🔵 **Line 29**: Method 'Reflection.normalized_score' missing docstring
- 🔵 **Line 29**: Method 'Reflection.normalized_score' missing type hints
- 🟡 **Line 33**: Class 'Node' missing docstring
- 🔵 **Line 59**: Method 'Node.is_solved' missing type hints
- 🔵 **Line 64**: Method 'Node.is_terminal' missing docstring
- 🔵 **Line 64**: Method 'Node.is_terminal' missing type hints
- 🔵 **Line 68**: Method 'Node.best_child_score' missing type hints
- 🔵 **Line 75**: Method 'Node.height' missing type hints
- 🔵 **Line 81**: Method 'Node.upper_confidence_bound' missing type hints
- 🔵 **Line 93**: Method 'Node.backpropagate' missing type hints
- 🔵 **Line 101**: Method 'Node.get_messages' missing docstring
- 🔵 **Line 101**: Method 'Node.get_messages' missing type hints
- 🔵 **Line 129**: Method 'Node.get_best_solution' missing type hints

### src/haive/agents/reasoning_and_critique/lats/aug_llms.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/reasoning_and_critique/lats/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/reasoning_and_critique/lats/utils.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 8**: Function 'create_reflection_chain' missing type hints

### src/haive/agents/reasoning_and_critique/lats/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 131**: Method 'LATSAgent.setup_workflow' missing type hints
- 🔵 **Line 508**: Method 'LATSAgent.stream' missing type hints

### src/haive/agents/reasoning_and_critique/lats/example.py

- 🔵 **Line 19**: Function 'main' missing type hints

### src/haive/agents/reasoning_and_critique/reflexion/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/reasoning_and_critique/reflexion/config.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 27**: Method 'ReflexionConfig.create_agent' missing docstring
- 🔵 **Line 27**: Method 'ReflexionConfig.create_agent' missing type hints

### src/haive/agents/reasoning_and_critique/reflexion/models.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/reasoning_and_critique/reflexion/aug_llms.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/reasoning_and_critique/reflexion/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/reasoning_and_critique/reflexion/utils.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/reasoning_and_critique/reflexion/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 59**: Method 'ReflexionAgent.final_answer' missing type hints
- 🔵 **Line 73**: Method 'ReflexionAgent.setup_workflow' missing docstring
- 🔵 **Line 73**: Method 'ReflexionAgent.setup_workflow' missing type hints

### src/haive/agents/reasoning_and_critique/reflexion/responder_with_retries.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 32**: Method 'ResponderWithRetries.respond' missing type hints

### src/haive/agents/reasoning_and_critique/reflexion/prompts.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/reasoning_and_critique/reflexion/tools.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 7**: Function 'run_queries' missing type hints

### src/haive/agents/reasoning_and_critique/self_discover/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/reasoning_and_critique/self_discover/engines.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/reasoning_and_critique/self_discover/config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/reasoning_and_critique/self_discover/models.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 27**: Method 'ModuleSelectionResult.format_for_next_stage' missing type hints
- 🔵 **Line 36**: Method 'ModuleSelectionResult.validate_modules' missing type hints
- 🔵 **Line 64**: Method 'ModuleAdaptationResult.format_for_next_stage' missing type hints
- 🔵 **Line 93**: Method 'ReasoningStructure.format_for_next_stage' missing type hints
- 🔵 **Line 103**: Method 'ReasoningStructure.validate_steps' missing type hints
- 🔵 **Line 131**: Method 'ReasoningOutput.format_complete_reasoning' missing type hints

### src/haive/agents/reasoning_and_critique/self_discover/aug_llms.py

- 🔴 **Line 1**: Could not parse file: invalid syntax (<unknown>, line 2)

### src/haive/agents/reasoning_and_critique/self_discover/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/reasoning_and_critique/self_discover/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 49**: Method 'SelfDiscoverAgent.select' missing type hints
- 🔵 **Line 54**: Method 'SelfDiscoverAgent.adapt' missing type hints
- 🔵 **Line 68**: Method 'SelfDiscoverAgent.structure' missing type hints
- 🔵 **Line 112**: Method 'SelfDiscoverAgent.setup_workflow' missing type hints
- 🟡 **Line 136**: Function 'main' missing docstring
- 🔵 **Line 136**: Function 'main' missing type hints

### src/haive/agents/reasoning_and_critique/self_discover/agent2.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 41**: Method 'SelfDiscoverAgent.setup_workflow' missing type hints

### src/haive/agents/reasoning_and_critique/self_discover/example.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 18**: Function 'example_math_problem' missing type hints
- 🔵 **Line 44**: Function 'example_svg_interpretation' missing type hints
- 🔵 **Line 88**: Function 'example_logical_reasoning' missing type hints
- 🔵 **Line 207**: Function 'run_batch_problems' missing type hints
- 🔵 **Line 257**: Function 'example_advanced_configuration' missing type hints
- 🔵 **Line 391**: Function 'analyze_reasoning_process' missing type hints
- 🔵 **Line 480**: Function 'example_compare_models' missing type hints

### src/haive/agents/reasoning_and_critique/logic/models.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 232**: Method 'ReasoningChain.num_steps' missing type hints
- 🔵 **Line 238**: Method 'ReasoningChain.max_inference_chain' missing type hints

### src/haive/agents/reasoning_and_critique/logic/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/reasoning_and_critique/logic/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 67**: Method 'ReasoningSystem.setup_agent' missing type hints
- 🔵 **Line 82**: Method 'ReasoningSystem.build_graph' missing type hints

### src/haive/agents/reasoning_and_critique/logic/example.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 11**: Function 'example_business_decision' missing type hints
- 🔵 **Line 81**: Function 'example_quick_reasoning' missing type hints

### src/haive/agents/reasoning_and_critique/tot/state.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 12**: Class 'TOTInput' missing docstring
- 🟡 **Line 16**: Class 'TOTOutput' missing docstring
- 🔵 **Line 62**: Method 'TOTState.convert_candidates' missing type hints
- 🔵 **Line 92**: Method 'TOTState.convert_single_candidate' missing type hints

### src/haive/agents/reasoning_and_critique/tot/models.py

- 🔵 **Line 87**: Method 'ScoredCandidate.content' missing type hints
- 🔵 **Line 92**: Method 'ScoredCandidate.value' missing type hints
- 🔵 **Line 97**: Method 'ScoredCandidate.feedback' missing type hints
- 🔵 **Line 102**: Method 'ScoredCandidate.metadata' missing type hints
- 🔵 **Line 165**: Method 'CandidateGeneration.to_candidates' missing type hints
- 🔵 **Line 193**: Method 'CandidateEvaluation.to_score' missing type hints
- 🔵 **Line 226**: Method 'Equation.compute' missing type hints
- 🔵 **Line 288**: Method 'EquationGeneration.to_candidates' missing type hints

### src/haive/agents/reasoning_and_critique/tot/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/reasoning_and_critique/tot/agent.py

- 🔵 **Line 100**: Method 'ToTAgent.setup_workflow' missing type hints

### src/haive/agents/reasoning_and_critique/mcts/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/reasoning_and_critique/mcts/config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/reasoning_and_critique/mcts/models.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 11**: Class 'Reflection' missing docstring
- 🔵 **Line 16**: Method 'Reflection.as_message' missing docstring
- 🔵 **Line 16**: Method 'Reflection.as_message' missing type hints
- 🔵 **Line 22**: Method 'Reflection.normalized_score' missing docstring
- 🔵 **Line 22**: Method 'Reflection.normalized_score' missing type hints
- 🟡 **Line 26**: Class 'TreeNode' missing docstring
- 🔵 **Line 44**: Method 'TreeNode.backpropagate' missing docstring
- 🔵 **Line 44**: Method 'TreeNode.backpropagate' missing type hints
- 🔵 **Line 57**: Method 'TreeNode.get_messages' missing docstring
- 🔵 **Line 62**: Method 'TreeNode.get_trajectory' missing docstring
- 🔵 **Line 79**: Method 'TreeNode.get_best_solution' missing docstring
- 🔵 **Line 79**: Method 'TreeNode.get_best_solution' missing type hints
- 🔵 **Line 87**: Method 'TreeNode.upper_confidence_bound' missing docstring
- 🔵 **Line 87**: Method 'TreeNode.upper_confidence_bound' missing type hints
- 🔵 **Line 97**: Method 'TreeNode.is_solved' missing docstring
- 🔵 **Line 97**: Method 'TreeNode.is_solved' missing type hints
- 🔵 **Line 101**: Method 'TreeNode.is_terminal' missing docstring
- 🔵 **Line 101**: Method 'TreeNode.is_terminal' missing type hints
- 🔵 **Line 105**: Method 'TreeNode.best_child_score' missing docstring
- 🔵 **Line 105**: Method 'TreeNode.best_child_score' missing type hints
- 🔵 **Line 112**: Method 'TreeNode.height' missing docstring
- 🔵 **Line 112**: Method 'TreeNode.height' missing type hints
- 🔵 **Line 118**: Method 'TreeNode.serialize_children' missing docstring
- 🔵 **Line 118**: Method 'TreeNode.serialize_children' missing type hints

### src/haive/agents/reasoning_and_critique/mcts/utils.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/reasoning_and_critique/mcts/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 34**: Method 'MCTSAgent.setup_workflow' missing type hints

### src/haive/agents/reasoning_and_critique/mcts/example.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 17**: Function 'setup_tavily_tool' missing type hints

### src/haive/agents/reasoning_and_critique/logic/engines/premise_extractor.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 119**: Function 'create_premise_extractor' missing type hints

### src/haive/agents/reasoning_and_critique/logic/engines/uncertainty_analyzer.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 177**: Function 'create_uncertainty_analyzer' missing type hints

### src/haive/agents/reasoning_and_critique/logic/engines/bias_detector.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 181**: Function 'create_bias_detector' missing type hints

### src/haive/agents/reasoning_and_critique/logic/engines/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/reasoning_and_critique/logic/engines/synthesis_agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 220**: Function 'create_synthesis_agent' missing type hints

### src/haive/agents/reasoning_and_critique/logic/engines/logical_reasoner.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 148**: Function 'create_logical_reasoner' missing type hints

### src/haive/agents/reasoning_and_critique/tot/modular/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/reasoning_and_critique/tot/modular/config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/reasoning_and_critique/tot/modular/models.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/reasoning_and_critique/tot/modular/factory.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 135**: Function 'score_math_solution' missing docstring
- 🔵 **Line 221**: Method 'Equation.validate_formula' missing type hints
- 🟡 **Line 262**: Function 'score_equation' missing docstring

### src/haive/agents/reasoning_and_critique/tot/modular/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/reasoning_and_critique/tot/modular/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 18**: Class 'ToTAgent' missing docstring
- 🔵 **Line 20**: Method 'ToTAgent.get_state_value' missing docstring
- 🔵 **Line 20**: Method 'ToTAgent.get_state_value' missing type hints
- 🔵 **Line 27**: Method 'ToTAgent.setup_workflow' missing docstring
- 🔵 **Line 27**: Method 'ToTAgent.setup_workflow' missing type hints
- 🔵 **Line 189**: Method 'ToTAgent.run' missing docstring

### src/haive/agents/reasoning_and_critique/tot/modular/example.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 50**: Function 'run_tot_example' missing type hints
- 🔵 **Line 76**: Function 'run_game24_example' missing type hints
- 🔵 **Line 97**: Function 'run_math_example' missing type hints

### src/haive/agents/reasoning_and_critique/tot/modular/branches.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/react_class/react_v3/config.py

- 🔵 **Line 89**: Method 'ReactAgentConfig.setup_defaults' missing type hints
- 🔵 **Line 119**: Method 'ReactAgentConfig.get_tool_schemas' missing type hints
- 🔵 **Line 142**: Method 'ReactAgentConfig.get_tools_by_name' missing type hints
- 🔵 **Line 150**: Method 'ReactAgentConfig.build_agent' missing type hints

### src/haive/agents/react_class/react_v3/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/react_class/react_v3/agent.py

- 🔵 **Line 36**: Method 'ReactAgent.setup_workflow' missing type hints

### src/haive/agents/react_class/react_v3/example.py

- 🔵 **Line 101**: Function 'test_basic_react_agent' missing type hints
- 🔵 **Line 142**: Function 'test_structured_tool_agent' missing type hints
- 🔵 **Line 192**: Function 'test_retry_policy' missing type hints
- 🔵 **Line 248**: Function 'test_multi_turn_conversation' missing type hints
- 🔵 **Line 305**: Function 'test_all' missing type hints

### src/haive/agents/react_class/react_agent2/tool_handler.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/react_class/react_agent2/agent3.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 126**: Method 'ReactAgent.setup_workflow' missing type hints
- 🔵 **Line 383**: Method 'ReactAgent.run' missing type hints

### src/haive/agents/react_class/react_agent2/config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/react_class/react_agent2/models.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/react_class/react_agent2/tool_utils.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/react_class/react_agent2/nodes.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 12**: Function 'get_tool_by_name' missing type hints
- 🔵 **Line 39**: Function 'get_tool_description' missing type hints
- 🔵 **Line 55**: Function 'get_tool_name' missing type hints
- 🔵 **Line 75**: Function 'execute_tool' missing type hints
- 🟡 **Line 456**: Function 'tool_node' missing docstring

### src/haive/agents/react_class/react_agent2/config2.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 138**: Method 'ReactAgentConfig.ensure_tools_list' missing type hints
- 🔵 **Line 147**: Method 'ReactAgentConfig.align_output_format' missing type hints
- 🔵 **Line 160**: Method 'ReactAgentConfig.update_system_prompt' missing type hints

### src/haive/agents/react_class/react_agent2/example3.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 232**: Method 'ReactAgent.setup_workflow' missing type hints

### src/haive/agents/react_class/react_agent2/advanced_agent3.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 100**: Method 'AdvancedReactAgent.setup_workflow' missing type hints

### src/haive/agents/react_class/react_agent2/example2.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 17**: Function 'print_latest_message' missing type hints
- 🔵 **Line 36**: Function 'example_basic_react_agent' missing type hints
- 🔵 **Line 79**: Function 'example_structured_output_agent' missing type hints
- 🔵 **Line 145**: Function 'example_memory_agent' missing type hints
- 🔵 **Line 191**: Function 'example_business_intelligence_agent' missing type hints
- 🔵 **Line 260**: Function 'interactive_chat' missing type hints
- 🔵 **Line 299**: Function 'run_examples' missing type hints

### src/haive/agents/react_class/react_agent2/dynamic_agent.py

- 🔵 **Line 187**: Method 'DynamicReactAgent.setup_workflow' missing type hints
- 🔵 **Line 384**: Method 'DynamicReactAgent.vector_store' missing type hints

### src/haive/agents/react_class/react_agent2/aug_llms.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/react_class/react_agent2/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/react_class/react_agent2/state2.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 67**: Method 'ReactAgentState.has_tool_calls' missing type hints
- 🔵 **Line 71**: Method 'ReactAgentState.should_continue' missing type hints
- 🔵 **Line 88**: Method 'ReactAgentState.increment_step' missing type hints

### src/haive/agents/react_class/react_agent2/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 230**: Method 'ReactAgent.setup_workflow' missing type hints

### src/haive/agents/react_class/react_agent2/agent2.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 25**: Function 'has_tool_calls' missing type hints
- 🔵 **Line 206**: Method 'ReactAgent.setup_workflow' missing type hints
- 🔵 **Line 421**: Method 'ReactAgent.chat' missing type hints
- 🔵 **Line 474**: Method 'ReactAgent.stream' missing type hints

### src/haive/agents/react_class/react_agent2/example.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 133**: Function 'run_custom_tool_routing_example' missing type hints

### src/haive/agents/react_class/react_agent2/debug.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 167**: Function 'create_debug_tool_node' missing type hints

### src/haive/agents/react_class/react/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/react_class/react/config.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 51**: Method 'ReactAgentConfig.ensure_valid_configuration' missing type hints

### src/haive/agents/react_class/react/tool_utils.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/react_class/react/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 42**: Method 'ReactAgent.setup_workflow' missing type hints

### src/haive/agents/react_class/react_many_tools/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/react_class/react_many_tools/config.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 72**: Method 'ReactManyToolsConfig.ensure_valid_configuration' missing type hints

### src/haive/agents/react_class/react_many_tools/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/react_class/react_many_tools/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 74**: Method 'ReactManyToolsAgent.retriever' missing type hints
- 🔵 **Line 113**: Method 'ReactManyToolsAgent.setup_workflow' missing type hints

### src/haive/agents/react_class/react_agent/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/react_class/react_agent/aug_llms.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/react_class/react_agent/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/react_class/react_agent/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 25**: Function 'should_continue' missing docstring
- 🟡 **Line 39**: Class 'ReactAgentConfig' missing docstring
- 🔵 **Line 99**: Method 'ReactAgentConfig.validate_engine' missing type hints
- 🔵 **Line 109**: Method 'ReactAgentConfig.ensure_list' missing type hints
- 🔵 **Line 118**: Method 'ReactAgentConfig.ensure_serializable' missing type hints
- 🔵 **Line 126**: Method 'ReactAgentConfig.build_agent' missing docstring
- 🔵 **Line 126**: Method 'ReactAgentConfig.build_agent' missing type hints
- 🟡 **Line 134**: Class 'ReactAgent' missing docstring
- 🔵 **Line 177**: Method 'ReactAgent.replace_agent_node' missing type hints
- 🔵 **Line 191**: Method 'ReactAgent.setup_workflow' missing type hints
- 🔵 **Line 209**: Method 'ReactAgent.visualize_graph' missing type hints
- 🔵 **Line 214**: Method 'ReactAgent.run' missing type hints
- 🔵 **Line 227**: Method 'ReactAgent.chat' missing type hints
- 🔵 **Line 249**: Function 'run_react_agent' missing type hints
- 🔵 **Line 256**: Function 'chat_react_agent' missing type hints
- 🔵 **Line 261**: Function 'chat_react_agent_with_tool_node' missing type hints

### src/haive/agents/react_class/react_v2/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/react_class/react_v2/graph_utils.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 20**: Method 'ReactGraphBuilder.add_human_node' missing type hints
- 🔵 **Line 35**: Method 'ReactGraphBuilder.add_tool_node' missing type hints

### src/haive/agents/react_class/react_v2/tool_handling.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/react_class/react_v2/config.py

- 🔵 **Line 223**: Method 'ReactAgentConfig.validate_tools' missing type hints

### src/haive/agents/react_class/react_v2/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/react_class/react_v2/agent.py

- 🔵 **Line 142**: Method 'ReactAgent.setup_workflow' missing type hints
- 🔵 **Line 333**: Method 'ReactAgent.run' missing type hints

### src/haive/agents/react_class/react_v2/example.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 93**: Function 'simulate_react_agent_with_human' missing docstring
- 🔵 **Line 93**: Function 'simulate_react_agent_with_human' missing type hints

### src/haive/agents/react_class/react_v2/prompts.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/react_class/react_agent2/many_tools/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/react_class/react_agent2/many_tools/engines.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/react_class/react_agent2/many_tools/models.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/react_class/react_agent2/many_tools/nodes.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 9**: Function 'select_tools_with_repeat' missing type hints
- 🟡 **Line 46**: Function 'select_tools' missing docstring
- 🔵 **Line 46**: Function 'select_tools' missing type hints

### src/haive/agents/react_class/react_agent2/many_tools/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/document_modifiers/tnt/models.py

- 🔵 **Line 65**: Method 'Doc.from_document' missing docstring

### src/haive/agents/document_modifiers/tnt/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/document_modifiers/tnt/agent.py

- 🔵 **Line 118**: Method 'TaxonomyAgent.get_content' missing type hints
- 🔵 **Line 197**: Method 'TaxonomyAgent.get_minibatches' missing type hints
- 🔵 **Line 291**: Method 'TaxonomyAgent.setup_workflow' missing type hints

### src/haive/agents/document_modifiers/tnt/example.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/document_modifiers/base/state.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 32**: Method 'DocumentModifierState.documents_text' missing type hints
- 🔵 **Line 38**: Method 'DocumentModifierState.num_documents' missing type hints
- 🔵 **Line 43**: Method 'DocumentModifierState.validate_documents' missing type hints
- 🔵 **Line 50**: Method 'DocumentModifierState.validate_documents' missing type hints

### src/haive/agents/document_modifiers/base/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/document_modifiers/summarizer/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/document_modifiers/complex_extraction/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/document_modifiers/complex_extraction/config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/document_modifiers/complex_extraction/models.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/document_modifiers/complex_extraction/factory.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/document_modifiers/complex_extraction/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/document_modifiers/complex_extraction/utils.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 92**: Function 'aggregate_messages' missing docstring

### src/haive/agents/document_modifiers/complex_extraction/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 445**: Method 'ComplexExtractionAgent.setup_workflow' missing type hints

### src/haive/agents/document_modifiers/complex_extraction/example.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 13**: Class 'PersonInfo' missing docstring

### src/haive/agents/document_modifiers/base/models/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/document_modifiers/summarizer/iterative_refinement/state.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 17**: Method 'IterativeSummarizerInput.normalize_contents' missing type hints
- 🔵 **Line 49**: Method 'IterativeSummarizerState.should_refine' missing docstring
- 🔵 **Line 49**: Method 'IterativeSummarizerState.should_refine' missing type hints

### src/haive/agents/document_modifiers/summarizer/iterative_refinement/engines.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/document_modifiers/summarizer/iterative_refinement/config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/document_modifiers/summarizer/iterative_refinement/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/document_modifiers/summarizer/iterative_refinement/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 48**: Method 'IterativeSummarizer.setup_workflow' missing docstring
- 🔵 **Line 48**: Method 'IterativeSummarizer.setup_workflow' missing type hints

### src/haive/agents/document_modifiers/summarizer/iterative_refinement/example.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/document_modifiers/summarizer/map_branch/state.py

- 🟡 **Line 10**: Class 'InputState' missing docstring
- 🔵 **Line 17**: Method 'InputState.normalize_contents' missing type hints

### src/haive/agents/document_modifiers/summarizer/map_branch/engines.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/document_modifiers/summarizer/map_branch/config.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 16**: Class 'SummarizerAgentConfig' missing docstring
- 🔵 **Line 39**: Method 'SummarizerAgentConfig.build_agent' missing docstring
- 🔵 **Line 39**: Method 'SummarizerAgentConfig.build_agent' missing type hints

### src/haive/agents/document_modifiers/summarizer/map_branch/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/document_modifiers/summarizer/map_branch/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 50**: Method 'SummarizerAgent.setup_workflow' missing type hints
- 🔵 **Line 141**: Method 'SummarizerAgent.map_summaries' missing type hints
- 🔵 **Line 147**: Method 'SummarizerAgent.collect_summaries' missing type hints
- 🟡 **Line 196**: Function 'build_agent' missing docstring
- 🔵 **Line 196**: Function 'build_agent' missing type hints

### src/haive/agents/document_modifiers/summarizer/map_branch/example.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/document_modifiers/kg/kg_map_merge/state.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 37**: Method 'KnowledgeGraphState.should_continue' missing type hints

### src/haive/agents/document_modifiers/kg/kg_map_merge/engines.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 220**: Function 'create_parallel_kg_transformer_configs' missing type hints
- 🟡 **Line 235**: Function 'main' missing docstring
- 🔵 **Line 235**: Function 'main' missing type hints

### src/haive/agents/document_modifiers/kg/kg_map_merge/config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/document_modifiers/kg/kg_map_merge/models.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 19**: Method 'EntityNode.validate_node' missing type hints
- 🔵 **Line 32**: Method 'EntityNode.from_graph_node' missing type hints
- 🔵 **Line 65**: Method 'EntityRelationship.validate_relationship' missing type hints
- 🔵 **Line 80**: Method 'EntityRelationship.from_graph_relationship' missing type hints
- 🔵 **Line 116**: Method 'KnowledgeGraph.add_node' missing type hints
- 🔵 **Line 126**: Method 'KnowledgeGraph.add_relationship' missing type hints
- 🔵 **Line 143**: Method 'KnowledgeGraph.merge' missing type hints
- 🟡 **Line 157**: Function 'main' missing docstring
- 🔵 **Line 157**: Function 'main' missing type hints

### src/haive/agents/document_modifiers/kg/kg_map_merge/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/document_modifiers/kg/kg_map_merge/utils.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 12**: Function 'visualize_graph' missing type hints

### src/haive/agents/document_modifiers/kg/kg_map_merge/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 68**: Method 'ParallelKGTransformer.setup_workflow' missing docstring
- 🔵 **Line 68**: Method 'ParallelKGTransformer.setup_workflow' missing type hints
- 🔵 **Line 107**: Method 'ParallelKGTransformer.map_graph_documents' missing docstring
- 🔵 **Line 107**: Method 'ParallelKGTransformer.map_graph_documents' missing type hints
- 🔵 **Line 140**: Method 'ParallelKGTransformer.map_nodes' missing type hints
- 🔵 **Line 186**: Method 'ParallelKGTransformer.map_relationships' missing type hints
- 🔵 **Line 275**: Method 'ParallelKGTransformer.merge_graphs' missing type hints

### src/haive/agents/document_modifiers/kg/kg_map_merge/agent2.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 62**: Method 'StructuredKGAgent.initialize_workflow' missing type hints
- 🔵 **Line 125**: Method 'StructuredKGAgent.distribute_documents' missing type hints
- 🔵 **Line 132**: Method 'StructuredKGAgent.map_documents' missing type hints
- 🔵 **Line 189**: Method 'StructuredKGAgent.distribute_graph_document_pairs' missing type hints
- 🔵 **Line 249**: Method 'StructuredKGAgent.route_after_collection' missing type hints
- 🔵 **Line 268**: Method 'StructuredKGAgent.map_merge_pairs' missing type hints
- 🔵 **Line 457**: Method 'StructuredKGAgent.collect_merged' missing type hints
- 🔵 **Line 476**: Method 'StructuredKGAgent.continue_merging' missing type hints
- 🔵 **Line 566**: Method 'StructuredKGAgent.finalize_graph' missing type hints
- 🔵 **Line 609**: Method 'StructuredKGAgent.setup_workflow' missing type hints

### src/haive/agents/document_modifiers/kg/kg_map_merge/example.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/document_modifiers/kg/kg_base/models.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/document_modifiers/kg/kg_base/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/document_modifiers/kg/kg_iterative_refinement/state.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 18**: Method 'IterativeGraphTransformerState.should_refine' missing docstring
- 🔵 **Line 18**: Method 'IterativeGraphTransformerState.should_refine' missing type hints

### src/haive/agents/document_modifiers/kg/kg_iterative_refinement/engines.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/document_modifiers/kg/kg_iterative_refinement/config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/document_modifiers/kg/kg_iterative_refinement/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/document_modifiers/kg/kg_iterative_refinement/utils.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/document_modifiers/kg/kg_iterative_refinement/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 37**: Method 'IterativeGraphTransformer.generate_initial_summary' missing docstring
- 🔵 **Line 37**: Method 'IterativeGraphTransformer.generate_initial_summary' missing type hints
- 🔵 **Line 57**: Method 'IterativeGraphTransformer.refine_summary' missing docstring
- 🔵 **Line 57**: Method 'IterativeGraphTransformer.refine_summary' missing type hints
- 🔵 **Line 102**: Method 'IterativeGraphTransformer.setup_workflow' missing docstring
- 🔵 **Line 102**: Method 'IterativeGraphTransformer.setup_workflow' missing type hints
- 🟡 **Line 134**: Function 'main' missing docstring
- 🔵 **Line 134**: Function 'main' missing type hints

### src/haive/agents/multi/sequential/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/multi/sequential/agent.py

- 🔵 **Line 17**: Function 'placeholder_node' missing type hints
- 🔵 **Line 34**: Method 'SequentialMultiAgent.build_graph' missing type hints

### src/haive/agents/conversation/collaberative/agent.py

- 🔵 **Line 57**: Method 'CollaborativeConversation.get_conversation_state_schema' missing type hints
- 🔵 **Line 368**: Method 'CollaborativeConversation.create_brainstorming_session' missing type hints
- 🔵 **Line 427**: Method 'CollaborativeConversation.create_code_review' missing type hints

### src/haive/agents/conversation/collaberative/example.py

- 🔵 **Line 19**: Function 'example_brainstorming_session' missing type hints
- 🔵 **Line 54**: Function 'example_code_review' missing type hints
- 🔵 **Line 80**: Function 'example_project_planning' missing type hints
- 🔵 **Line 159**: Function 'example_research_paper' missing type hints
- 🔵 **Line 239**: Function 'example_creative_writing' missing type hints

### src/haive/agents/conversation/base/state.py

- 🔵 **Line 92**: Method 'ConversationState.round_number' missing type hints
- 🔵 **Line 105**: Method 'ConversationState.current_round_speakers' missing type hints
- 🔵 **Line 124**: Method 'ConversationState.remaining_speakers_this_round' missing type hints
- 🔵 **Line 138**: Method 'ConversationState.should_end_by_rounds' missing type hints
- 🔵 **Line 148**: Method 'ConversationState.turns_per_round' missing type hints
- 🔵 **Line 158**: Method 'ConversationState.conversation_progress' missing type hints

### src/haive/agents/conversation/base/agent.py

- 🔵 **Line 176**: Method 'BaseConversationAgent.setup_agent' missing type hints
- 🔵 **Line 206**: Method 'BaseConversationAgent.get_conversation_state_schema' missing type hints
- 🔵 **Line 235**: Method 'BaseConversationAgent.build_graph' missing type hints
- 🔵 **Line 576**: Method 'BaseConversationAgent.get_input_fields' missing type hints
- 🔵 **Line 580**: Method 'BaseConversationAgent.get_output_fields' missing type hints

### src/haive/agents/conversation/round_robin/agent.py

- 🔵 **Line 105**: Method 'RoundRobinConversation.create_simple' missing type hints

### src/haive/agents/conversation/round_robin/example.py

- 🔵 **Line 17**: Function 'example_simple_round_robin' missing type hints
- 🔵 **Line 44**: Function 'example_custom_round_robin' missing type hints
- 🔵 **Line 88**: Function 'example_panel_discussion' missing type hints

### src/haive/agents/conversation/debate/state.py

- 🔵 **Line 87**: Method 'DebateState.in_rebuttal_phase' missing type hints
- 🔵 **Line 93**: Method 'DebateState.all_arguments_complete' missing type hints
- 🔵 **Line 105**: Method 'DebateState.debate_progress' missing type hints
- 🔵 **Line 115**: Method 'DebateState.phase_should_transition' missing type hints
- 🔵 **Line 129**: Method 'DebateState.all_rebuttals_complete' missing type hints
- 🔵 **Line 139**: Method 'DebateState.next_phase' missing type hints
- 🔵 **Line 152**: Method 'DebateState.debate_statistics' missing type hints
- 🔵 **Line 172**: Method 'DebateState.should_end_debate' missing type hints

### src/haive/agents/conversation/debate/agent.py

- 🔵 **Line 95**: Method 'DebateConversation.validate_debate_setup' missing type hints
- 🔵 **Line 120**: Method 'DebateConversation.setup_agent' missing type hints
- 🔵 **Line 135**: Method 'DebateConversation.get_conversation_state_schema' missing type hints

### src/haive/agents/conversation/debate/example.py

- 🔵 **Line 17**: Function 'example_simple_debate' missing type hints
- 🔵 **Line 63**: Function 'example_panel_debate' missing type hints
- 🔵 **Line 143**: Function 'example_oxford_debate' missing type hints
- 🔵 **Line 243**: Function 'example_socratic_debate' missing type hints

### src/haive/agents/conversation/directed/agent.py

- 🔵 **Line 114**: Method 'DirectedConversation.get_conversation_state_schema' missing type hints
- 🔵 **Line 454**: Method 'DirectedConversation.create_classroom' missing type hints

### src/haive/agents/conversation/directed/example.py

- 🔵 **Line 16**: Function 'example_classroom_discussion' missing type hints
- 🔵 **Line 40**: Function 'example_team_meeting' missing type hints
- 🔵 **Line 120**: Function 'example_customer_support' missing type hints
- 🔵 **Line 188**: Function 'example_interactive_story' missing type hints

### src/haive/agents/conversation/social_media/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/conversation/social_media/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 58**: Method 'SocialMediaConversation.get_conversation_state_schema' missing type hints
- 🔵 **Line 364**: Method 'SocialMediaConversation.create_twitter_thread' missing type hints

### src/haive/agents/conversation/social_media/example.py

- 🔵 **Line 16**: Function 'example_twitter_thread' missing type hints
- 🔵 **Line 67**: Function 'example_instagram_discussion' missing type hints
- 🔵 **Line 124**: Function 'example_tiktok_comments' missing type hints
- 🔵 **Line 177**: Function 'example_linkedin_professional' missing type hints
- 🔵 **Line 262**: Function 'example_viral_moment' missing type hints

### src/haive/agents/wiki_writer/interview/state.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 12**: Class 'InterviewState' missing docstring

### src/haive/agents/wiki_writer/interview/models.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 4**: Class 'AnswerWithCitations' missing docstring
- 🔵 **Line 13**: Method 'AnswerWithCitations.as_str' missing docstring
- 🔵 **Line 13**: Method 'AnswerWithCitations.as_str' missing type hints

### src/haive/agents/wiki_writer/interview/nodes.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/wiki_writer/interview/aug_llms.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/agents/wiki_writer/interview/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/agents/wiki_writer/interview/utils.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 1**: Function 'add_messages' missing docstring
- 🔵 **Line 1**: Function 'add_messages' missing type hints
- 🟡 **Line 9**: Function 'update_references' missing docstring
- 🔵 **Line 9**: Function 'update_references' missing type hints
- 🟡 **Line 16**: Function 'update_editor' missing docstring
- 🔵 **Line 16**: Function 'update_editor' missing type hints

### src/haive/agents/wiki_writer/interview/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 42**: Method 'InterviewAgent.setup_workflow' missing type hints

### src/haive/agents/wiki_writer/interview/tools.py

- 🟡 **Line 1**: Module missing docstring
