# Test File Migration Summary for Haive Project

## Overview
This document provides a comprehensive analysis of test files in the haive project and identifies which tests need to be moved to the proper `packages/haive-*/tests/` structure.

## 1. Tests Already in Correct Location

These tests are already properly organized in their respective package test directories:

### haive-agents (packages/haive-agents/tests/)
- ✅ base/checkpointer/test_postgres.py
- ✅ base/checkpointer/test_postgres_persistent_agent.py
- ✅ base/checkpointer/test_utils.py
- ✅ chain_test.py
- ✅ conftest.py
- ✅ multi/debug_test.py
- ✅ multi/minimal_test.py
- ✅ multi/test_debug_tools.py
- ✅ multi/test_fix_messages.py
- ✅ multi/test_fix_tool_messages.py
- ✅ multi/test_message_serialization.py
- ✅ multi/test_messages_debug.py
- ✅ multi/test_multi_agent.py
- ✅ multi/test_new_multi_agent.py
- ✅ multi/test_simple_debug.py
- ✅ multi/test_simple_fix.py
- ✅ multi/test_simple_user.py
- ✅ multi/test_state_transfer.py
- ✅ multi/test_user_example.py
- ✅ rag/base/test_base_rag_agent.py
- ✅ rag/llm/test_llm_rag_agent.py
- ✅ react/test_react_agent.py
- ✅ react/test_react_human.py
- ✅ react/test_react_many_tools.py
- ✅ react/test_react_memory.py
- ✅ react_class/test_3.py
- ✅ research/test_deep_research.py
- ✅ research/test_person_researcher.py
- ✅ simple/test_examples.py
- ✅ simple/test_persistence.py
- ✅ simple/test_simple_agent.py
- ✅ simple/test_simple_agent_schema.py
- ✅ test_agent_fix.py
- ✅ test_agent_serialization.py
- ✅ test_basic.py
- ✅ test_individual_agent_serialization.py
- ✅ test_multi_agent.py
- ✅ test_multi_agent_example.py
- ✅ test_react_agent.py
- ✅ test_react_base.py
- ✅ test_serialization_issue.py
- ✅ test_simple_agent_state.py
- ✅ test_single_vs_multi.py

### haive-core (packages/haive-core/tests/)
- ✅ config/test_runnable_config_manager.py
- ✅ conftest.py
- ✅ engine/agent/persistence/test_persistence.py
- ✅ engine/agent/persistence/test_persistence2.py
- ✅ engine/agent/persistence/test_persistence_manager.py
- ✅ engine/agent/test_agent.py
- ✅ engine/agent/test_agent_io_to_state_schema.py
- ✅ engine/agent/test_config.py
- ✅ engine/agent/test_debug_test.py
- ✅ engine/agent/test_pattern.py
- ✅ engine/aug_llm/test_aug_llm.py
- ✅ engine/aug_llm/test_aug_llm_composition.py
- ✅ engine/aug_llm/test_aug_llm_composition_examples.py
- ✅ engine/aug_llm/test_aug_llm_examples.py
- ✅ engine/aug_llm/test_schema_composer.py
- ✅ engine/base/test_base_engine.py
- ✅ engine/base/test_reference.py
- ✅ engine/output_parsers/test_output_parsers.py
- ✅ engine/retriever/test_retriever.py
- ✅ engine/retriever/test_retriever_in_graph.py
- ✅ engine/retriever/test_svm_retriever.py
- ✅ engine/vectorstore/test_vectorstore.py
- ✅ graph/branch/test_branch.py
- ✅ graph/node/test_node_config.py
- ✅ graph/node/test_node_diagnostic.py
- ✅ graph/node/test_node_factory.py
- ✅ graph/node/test_node_factory_integration.py
- ✅ graph/node/test_node_simple.py
- ✅ graph/node/test_node_system.py
- ✅ graph/node/test_node_system_v2.py
- ✅ graph/node/test_tool_node_config.py
- ✅ graph/test_complex_visualization.py
- ✅ graph/test_dynamic_graph.py
- ✅ graph/test_graph_builder.py
- ✅ graph/test_rag_workflow.py
- ✅ graph/test_state_graph.py
- ✅ test_abstract_registry.py
- ✅ test_agent_schema_fix.py
- ✅ test_basic.py
- ✅ test_engine_serialization.py
- ✅ test_general.py
- ✅ test_improved_subgraph_visualization.py
- ✅ test_introspection.py
- ✅ test_prompt_template_integration.py
- ✅ test_react_agent.py
- ✅ test_real_agent_schema.py
- ✅ test_schema_composer_demo.py
- ✅ test_schema_optional.py
- ✅ test_structured_output_mixin.py
- ✅ test_subgraph_visualization.py
- ✅ test_tool_manager.py
- ✅ test_tool_sync.py
- ✅ test_v1_structured_output.py

### haive-dataflow (packages/haive-dataflow/tests/)
- ✅ conftest.py
- ✅ test_basic.py
- ✅ test_debug_jwt.py
- ✅ test_supabase_client.py
- ✅ test_supabase_debug.py
- ✅ test_supabase_direct.py
- ✅ test_supabase_env.py
- ✅ test_supabase_schema.py

### haive-games (packages/haive-games/tests/)
- ✅ conftest.py
- ✅ test_basic.py
- ✅ test_monopoly.py
- ✅ test_monopoly_config.py

### haive-mcp (packages/haive-mcp/tests/)
- ✅ test_mcp.py

### haive-prebuilt (packages/haive-prebuilt/tests/)
- ✅ conftest.py
- ✅ test_basic.py

### haive-tools (packages/haive-tools/tests/)
- ✅ conftest.py
- ✅ test_chucknorris_toolkit.py
- ✅ test_corporate_bs_tool.py
- ✅ test_tool_manager.py
- ✅ toolkits/test_chucknorris_toolkit.py
- ✅ tools/test_corporate_bs_tool.py

## 2. Tests That Need to Be Moved

### From /tests/ (root tests directory) → Target Package

#### Agent-related tests → packages/haive-agents/tests/
- **tests/agents/test_react_agent.py** → packages/haive-agents/tests/test_react_agent.py (duplicate?)
- **tests/agents/react/test_react_agent.py** → packages/haive-agents/tests/react/test_react_agent.py (merge with existing)
- **tests/agents/react/test_react_human.py** → packages/haive-agents/tests/react/test_react_human.py (merge with existing)
- **tests/agents/react/test_react_many_tools.py** → packages/haive-agents/tests/react/test_react_many_tools.py (merge with existing)
- **tests/agents/react/test_react_memory.py** → packages/haive-agents/tests/react/test_react_memory.py (merge with existing)
- **tests/agents/research/test_deep_research.py** → packages/haive-agents/tests/research/test_deep_research.py (merge with existing)
- **tests/agents/research/test_person_researcher.py** → packages/haive-agents/tests/research/test_person_researcher.py (merge with existing)
- **tests/agents/simple/test_simple_agent.py** → packages/haive-agents/tests/simple/test_simple_agent.py (merge with existing)
- **tests/test_react_agent.py** → packages/haive-agents/tests/test_react_agent.py (merge with existing)

#### Core-related tests → packages/haive-core/tests/
- **tests/core/graph/schema/test_schema_composer.py** → packages/haive-core/tests/graph/schema/test_schema_composer.py
- **tests/core/graph/schema/test_schema_manager.py** → packages/haive-core/tests/graph/schema/test_schema_manager.py
- **tests/core/graph/test_graph_builder.py** → packages/haive-core/tests/graph/test_graph_builder.py (merge with existing)
- **tests/core/graph/node/test_node_config.py** → packages/haive-core/tests/graph/node/test_node_config.py (merge with existing)
- **tests/core/graph/node/test_node_system.py** → packages/haive-core/tests/graph/node/test_node_system.py (merge with existing)
- **tests/graph/patterns/test_integration.py** → packages/haive-core/tests/graph/patterns/test_integration.py
- **tests/test_abstract_registry.py** → packages/haive-core/tests/test_abstract_registry.py (merge with existing)
- **tests/test_general.py** → packages/haive-core/tests/test_general.py (merge with existing)
- **tests/test_introspection.py** → packages/haive-core/tests/test_introspection.py (merge with existing)

#### Tools-related tests → packages/haive-tools/tests/
- **tests/test_tool_manager.py** → packages/haive-tools/tests/test_tool_manager.py (merge with existing)
- **tests/tools/test_corporate_bs_tool.py** → packages/haive-tools/tests/tools/test_corporate_bs_tool.py (merge with existing)
- **tests/toolkits/test_chucknorris_toolkit.py** → packages/haive-tools/tests/toolkits/test_chucknorris_toolkit.py (merge with existing)

#### Games-related tests → packages/haive-games/tests/
- **tests/test_monopoly.py** → packages/haive-games/tests/test_monopoly.py (merge with existing)
- **tests/test_monopoly_config.py** → packages/haive-games/tests/test_monopoly_config.py (merge with existing)

### From src directories (these should be moved out of src)

#### haive-dataflow src tests → packages/haive-dataflow/tests/
- **packages/haive-dataflow/src/haive/dataflow/api/test_api.py** → packages/haive-dataflow/tests/api/test_api.py
- **packages/haive-dataflow/src/haive/dataflow/test_api.py** → packages/haive-dataflow/tests/test_api.py
- **packages/haive-dataflow/src/haive/dataflow/test_supabase.py** → packages/haive-dataflow/tests/test_supabase.py
- **packages/haive-dataflow/src/haive/dataflow/api/test_chess_connection.py** → packages/haive-dataflow/tests/api/test_chess_connection.py
- **packages/haive-dataflow/src/haive/dataflow/api/test_integration.py** → packages/haive-dataflow/tests/api/test_integration.py

#### haive-agents src tests → packages/haive-agents/tests/
- **packages/haive-agents/src/haive/agents/rag/llm_rag/test.py** → packages/haive-agents/tests/rag/llm_rag/test_llm_rag.py
- **packages/haive-agents/src/haive/agents/react_class/react_agent2/test2.py** → packages/haive-agents/tests/react_class/test_react_agent2.py
- **packages/haive-agents/src/haive/agents/simple/test2.py** → packages/haive-agents/tests/simple/test_simple2.py
- **packages/haive-agents/src/haive/agents/rag/base/test.py** → packages/haive-agents/tests/rag/base/test_base_rag.py
- **packages/haive-agents/src/haive/agents/simple/test.py** → packages/haive-agents/tests/simple/test_simple.py
- **packages/haive-agents/src/haive/agents/multi/test.py** → packages/haive-agents/tests/multi/test_multi.py
- **packages/haive-agents/src/haive/agents/document_loader/tests/test_document_loader_agent.py** → packages/haive-agents/tests/document_loader/test_document_loader_agent.py

#### haive-games src tests → packages/haive-games/tests/
- **packages/haive-games/src/haive/games/poker/test.py** → packages/haive-games/tests/poker/test_poker.py
- **packages/haive-games/src/haive/games/fox_and_geese/standalone_test.py** → packages/haive-games/tests/fox_and_geese/test_standalone.py
- **packages/haive-games/src/haive/games/fox_and_geese/test_fixes.py** → packages/haive-games/tests/fox_and_geese/test_fixes.py
- **packages/haive-games/src/haive/games/fox_and_geese/minimal_fix_test.py** → packages/haive-games/tests/fox_and_geese/test_minimal_fix.py
- **packages/haive-games/src/haive/games/hold_em/test.py** → packages/haive-games/tests/hold_em/test_hold_em.py
- **packages/haive-games/src/haive/games/mafia/mock_test.py** → packages/haive-games/tests/mafia/test_mock.py
- **packages/haive-games/src/haive/games/mafia/test_mafia.py** → packages/haive-games/tests/mafia/test_mafia.py
- **packages/haive-games/src/haive/games/mancala/fixes_test.py** → packages/haive-games/tests/mancala/test_fixes.py
- **packages/haive-games/src/haive/games/mancala/standalone_test.py** → packages/haive-games/tests/mancala/test_standalone.py
- **packages/haive-games/src/haive/games/mancala/relative_test.py** → packages/haive-games/tests/mancala/test_relative.py
- **packages/haive-games/src/haive/games/mancala/minimal_test.py** → packages/haive-games/tests/mancala/test_minimal.py
- **packages/haive-games/src/haive/games/mastermind/standalone_test.py** → packages/haive-games/tests/mastermind/test_standalone.py
- **packages/haive-games/src/haive/games/mastermind/standalone_ui_test.py** → packages/haive-games/tests/mastermind/test_standalone_ui.py
- **packages/haive-games/src/haive/games/mastermind/test_fixes.py** → packages/haive-games/tests/mastermind/test_fixes.py
- **packages/haive-games/src/haive/games/mastermind/test_ui.py** → packages/haive-games/tests/mastermind/test_ui.py
- **packages/haive-games/src/haive/games/single_player/wordle/test_custom_game.py** → packages/haive-games/tests/single_player/wordle/test_custom_game.py
- **packages/haive-games/src/haive/games/nim/standalone_test.py** → packages/haive-games/tests/nim/test_standalone.py

#### haive-core src tests → packages/haive-core/tests/
- **packages/haive-core/src/haive/core/graph/node/test.py** → packages/haive-core/tests/graph/node/test_node.py
- **packages/haive-core/src/haive/core/graph/routers/test.py** → packages/haive-core/tests/graph/routers/test_routers.py

### Miscellaneous test files to review/move

#### Script and example tests
- **scripts/migration/agent_tests.py** → Likely a migration script, not a test file
- **packages/haive-agents/examples/debug_test.py** → Example file, not a test
- **scratches/transformer_test.py** → Scratch file, should be removed or moved to proper test location
- **scratches/dl_import_test.py** → Scratch file, should be removed or moved to proper test location
- **notebooks/test.py** → Notebook test file, needs proper placement

## 3. Test Directories That Need to Be Created

Based on the tests that need to be moved, the following test subdirectories should be created:

### packages/haive-core/tests/
- graph/schema/ (for schema-related tests)
- graph/patterns/ (for pattern integration tests)

### packages/haive-dataflow/tests/
- api/ (for API-related tests)

### packages/haive-agents/tests/
- document_loader/ (for document loader tests)
- rag/llm_rag/ (if not exists)

### packages/haive-games/tests/
- poker/
- fox_and_geese/
- hold_em/
- mafia/
- mancala/
- mastermind/
- single_player/wordle/
- nim/

### packages/haive-core/tests/
- graph/routers/

## 4. Duplicate Test Files

Several test files appear to exist in multiple locations and need to be consolidated:

1. **test_react_agent.py** exists in:
   - tests/agents/test_react_agent.py
   - tests/agents/react/test_react_agent.py
   - tests/test_react_agent.py
   - packages/haive-agents/tests/test_react_agent.py
   - packages/haive-agents/tests/react/test_react_agent.py

2. **test_simple_agent.py** exists in:
   - tests/agents/simple/test_simple_agent.py
   - packages/haive-agents/tests/simple/test_simple_agent.py

3. **test_monopoly.py** and **test_monopoly_config.py** exist in:
   - tests/test_monopoly.py
   - tests/test_monopoly_config.py
   - packages/haive-games/tests/test_monopoly.py
   - packages/haive-games/tests/test_monopoly_config.py

4. Many other duplicates between /tests/ directory and package test directories

## 5. Recommendations

1. **Consolidate Duplicates**: Review duplicate test files to determine which version is most current and merge any unique tests.

2. **Remove Root Tests Directory**: After migration, the `/tests/` directory at the root should be removed to avoid confusion.

3. **Standardize Test Names**: Ensure all test files follow the `test_*.py` naming convention (not `*_test.py` or generic names like `test.py`).

4. **Clean Up Src Tests**: No test files should be in `src` directories - all should be in the package's `tests/` directory.

5. **Remove Scratch Files**: Files in `/scratches/` and similar locations should be reviewed and either converted to proper tests or removed.

6. **Update Imports**: After moving tests, update all import statements to reflect the new locations.

7. **Configure Test Discovery**: Ensure pytest.ini or pyproject.toml in each package is configured to discover tests in the new locations.