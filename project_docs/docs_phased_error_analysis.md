# Docs Phased Error Analysis

## Error Categories

### 1. Missing Functions/Classes
- `build_graph` from `haive.agents.archive.meta.agent`
- `get_agent_capabilities` from `haive.core.engine.base.agent_types`
- `BranchSpec` from `haive.agents.chain.declarative_chain`
- `get_conversation_progress` from `haive.agents.conversation.base`
- `create_conversation_state` from `haive.agents.conversation.base`
- `normalize_contents` from various state modules
- `ParallelKGAgentConfig` from `haive.agents.document_modifiers.kg.kg_map_merge.config`
- `clean_and_format_text` from `haive.core.utils.doc_utils`
- `MemoryCheckpointerConfig` from `haive.core.engine.agent.persistence.base`
- `format_search_context` from `haive.agents.memory.search.base`

### 2. Missing Modules
- `examples.usage_examples`
- `langgraph_supervisor`
- `haive.agents.react_agent`
- `haive.agents.memory.models.base` (package structure issue)
- `haive.agents.memory_reorganized.base.memory_models_standalone`
- Various memory_reorganized modules

### 3. Syntax Errors
- `haive.agents.memory_reorganized.knowledge.kg_generator_agent` line 1023

### 4. Import Path Issues
- Various relative import problems
- Package structure conflicts

### 5. Pydantic Errors
- Forward reference issues
- Schema generation errors
- Metaclass conflicts

### 6. Missing Dependencies
- `google-search-results` package

## Fix Strategy

1. Start with missing dependencies
2. Fix syntax errors
3. Create missing functions/classes
4. Fix import paths
5. Resolve pydantic issues
