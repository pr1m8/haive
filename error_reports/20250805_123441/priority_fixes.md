# Priority Fix Recommendations

Fix these files first - they contain runtime-breaking errors:

## Critical Files (Top 20)


### 1. `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/factories/compatible_rag_factory.py` (98 critical errors)

**Other Errors:**
- Line 211: "SequentialAgent" is not defined
- Line 211: "ConditionalAgent" is not defined
- Line 211: "ParallelAgent" is not defined


### 2. `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/NodeFactory.py` (48 critical errors)

**Type Errors:**
- Line 122: Argument of type "InvokableEngine[Unknown, Unknown]" cannot be assigned to parameter "engine" of type "VectorStoreConfig" in function "_create_vectorstore_node"
  - *Fix*: Fix type annotation or cast
- Line 130: Argument of type "InvokableEngine[Unknown, Unknown]" cannot be assigned to parameter "engine" of type "BaseRetrieverConfig" in function "_create_retriever_node"
  - *Fix*: Fix type annotation or cast
- Line 153: Argument of type "NonInvokableEngine[Unknown, Unknown]" cannot be assigned to parameter "engine" of type "EmbeddingsEngineConfig" in function "_create_embeddings_node"
  - *Fix*: Fix type annotation or cast


### 3. `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/self_healing_code/agent.py` (43 critical errors)

**Other Errors:**
- Line 4: "AgentArchitectureConfig" is not defined
- Line 5: "SelfHealingCodeState" is not defined
- Line 8: "AgentArchitecture" is not defined


### 4. `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py` (39 critical errors)

**Other Errors:**
- Line 457: No overloads for "update" match the provided arguments
- Line 461: No overloads for "update" match the provided arguments
- Line 471: No overloads for "update" match the provided arguments

**Type Errors:**
- Line 458: Argument of type "dict[str, NodeType | dict[str, (...) -> object] | Unknown]" cannot be assigned to parameter "m" of type "Iterable[tuple[str, str]]" in function "update"
  - *Fix*: Fix type annotation or cast
- Line 462: Argument of type "dict[str, NodeType | dict[str, Any] | Unknown]" cannot be assigned to parameter "m" of type "Iterable[tuple[str, str]]" in function "update"
  - *Fix*: Fix type annotation or cast


### 5. `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/factory.py` (32 critical errors)

**Type Errors:**
- Line 87: "SourceType" is not defined
  - *Fix*: Fix type annotation or cast
- Line 114: "SourceType" is not defined
  - *Fix*: Fix type annotation or cast
- Line 125: "SourceType" is not defined
  - *Fix*: Fix type annotation or cast


### 6. `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py` (32 critical errors)

**Other Errors:**
- Line 5: "GridBoard" is not defined
- Line 5: "CrosswordCell" is not defined
- Line 5: "CrosswordLetter" is not defined


### 7. `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/factories/rag_workflow_factory.py` (31 critical errors)

**Type Errors:**
- Line 93: Argument of type "dict[str, str]" cannot be assigned to parameter "destinations" of type "str | list[str] | dict[bool | str | int, str] | None" in function "add_conditional_edges"
  - *Fix*: Fix type annotation or cast

**Other Errors:**
- Line 115: "rag_workflow_router" is not defined
- Line 118: "advanced_document_grader" is not defined
- Line 119: "relevance_threshold_check" is not defined


### 8. `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py` (29 critical errors)

**Other Errors:**
- Line 396: No overloads for "create_model" match the provided arguments

**Type Errors:**
- Line 396: Argument of type "tuple[type, Any]" cannot be assigned to parameter "__config__" of type "ConfigDict | None" in function "create_model"
  - *Fix*: Fix type annotation or cast
- Line 396: Argument of type "tuple[type, Any]" cannot be assigned to parameter "__doc__" of type "str | None" in function "create_model"
  - *Fix*: Fix type annotation or cast
- Line 396: Argument of type "tuple[type, Any]" cannot be assigned to parameter "__module__" of type "str" in function "create_model"
  - *Fix*: Fix type annotation or cast


### 9. `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/models/procedural/models.py` (29 critical errors)

**Other Errors:**
- Line 63: "Dict" is not defined
- Line 64: "List" is not defined
- Line 65: "List" is not defined


### 10. `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py` (29 critical errors)

**Type Errors:**
- Line 180: Argument of type "TConfig@Agent" cannot be assigned to parameter "config_schema" of type "type[Any] | None" in function "__init__"
  - *Fix*: Fix type annotation or cast

**Other Errors:**
- Line 893: Cannot instantiate abstract class "BaseStore"
- Line 928: Cannot instantiate abstract class "BaseStore"
- Line 1000: Cannot instantiate abstract class "BaseStore"


### 11. `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py` (28 critical errors)

**Other Errors:**
- Line 167: No overloads for "__setitem__" match the provided arguments
- Line 378: No overloads for "search" match the provided arguments

**Type Errors:**
- Line 167: Argument of type "BaseMessage" cannot be assigned to parameter "value" of type "AnyMessage" in function "__setitem__"
  - *Fix*: Fix type annotation or cast
- Line 378: Argument of type "str | list[str | dict[Unknown, Unknown]]" cannot be assigned to parameter "string" of type "str" in function "search"
  - *Fix*: Fix type annotation or cast
- Line 439: Argument of type "list[AIMessage]" cannot be assigned to parameter "iterable" of type "Iterable[HumanMessage]" in function "extend"
  - *Fix*: Fix type annotation or cast


### 12. `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/message_transformation.py` (25 critical errors)

**Type Errors:**
- Line 110: Argument of type "str | Send | list[Send | str] | None" cannot be assigned to parameter "goto" of type "Send | Sequence[Send | str] | str" in function "__init__"
  - *Fix*: Fix type annotation or cast
- Line 117: Argument of type "str | Send | list[Send | str] | None" cannot be assigned to parameter "goto" of type "Send | Sequence[Send | str] | str" in function "__init__"
  - *Fix*: Fix type annotation or cast
- Line 120: Argument of type "str | Send | list[Send | str] | None" cannot be assigned to parameter "goto" of type "Send | Sequence[Send | str] | str" in function "__init__"
  - *Fix*: Fix type annotation or cast


### 13. `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py` (25 critical errors)

**Type Errors:**
- Line 146: Argument of type "UnionType" cannot be assigned to parameter "field_type" of type "type[Any] | None" in function "__init__"
  - *Fix*: Fix type annotation or cast
- Line 225: Argument of type "dict[Unknown, Unknown]" cannot be assigned to parameter "value" of type "str | list[str | dict[Unknown, Unknown]]" in function "__setitem__"
  - *Fix*: Fix type annotation or cast
- Line 228: Argument of type "dict[Any, Any]" cannot be assigned to parameter "value" of type "str | list[str | dict[Unknown, Unknown]]" in function "__setitem__"
  - *Fix*: Fix type annotation or cast

**Other Errors:**
- Line 229: No overloads for "__setitem__" match the provided arguments


### 14. `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/api/unified_memory_api.py` (23 critical errors)

**Type Errors:**
- Line 483: Argument of type "MemoryStoreManager" cannot be assigned to parameter "memory_store" of type "MemoryStoreManager" in function "__init__"
  - *Fix*: Fix type annotation or cast
- Line 484: Argument of type "MemoryClassifier" cannot be assigned to parameter "classifier" of type "MemoryClassifier" in function "__init__"
  - *Fix*: Fix type annotation or cast
- Line 494: Argument of type "MemoryStoreManager" cannot be assigned to parameter "memory_store_manager" of type "MemoryStoreManager" in function "__init__"
  - *Fix*: Fix type annotation or cast


### 15. `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/embedding/providers/OllamaEmbeddingConfig.py` (23 critical errors)

**Other Errors:**
- Line 75: "field_validator" is not defined
- Line 96: "field_validator" is not defined

**Type Errors:**
- Line 143: Argument of type "dict[str, str]" cannot be assigned to parameter "value" of type "str" in function "__setitem__"
  - *Fix*: Fix type annotation or cast
- Line 145: Argument of type "dict[str, Any]" cannot be assigned to parameter "value" of type "str" in function "__setitem__"
  - *Fix*: Fix type annotation or cast
- Line 147: Argument of type "float" cannot be assigned to parameter "value" of type "str" in function "__setitem__"
  - *Fix*: Fix type annotation or cast


### 16. `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py` (21 critical errors)

**Other Errors:**
- Line 5: "GridBoard" is not defined
- Line 5: "TwentyFortyEightSquare" is not defined
- Line 5: "GridPosition" is not defined


### 17. `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_v2/kg_memory_agent.py` (20 critical errors)

**Type Errors:**
- Line 154: Argument of type "str | None" cannot be assigned to parameter "uri" of type "str" in function "driver"
  - *Fix*: Fix type annotation or cast
- Line 154: Argument of type "tuple[str | None, str | None]" cannot be assigned to parameter "auth" of type "_TAuth | AsyncAuthManager" in function "driver"
  - *Fix*: Fix type annotation or cast
- Line 191: Object of type "None" is not subscriptable
  - *Fix*: Fix type annotation or cast


### 18. `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/meta_agent_node.py` (20 critical errors)

**Other Errors:**
- Line 224: No overloads for "__init__" match the provided arguments
- Line 273: No overloads for "update" match the provided arguments
- Line 378: No overloads for "__init__" match the provided arguments

**Type Errors:**
- Line 224: Argument of type "StateLike@_prepare_agent_input" cannot be assigned to parameter "iterable" of type "Iterable[list[bytes]]" in function "__init__"
  - *Fix*: Fix type annotation or cast
- Line 273: Argument of type "ConfigLike@_prepare_execution_config" cannot be assigned to parameter "m" of type "Iterable[tuple[str, Unknown]]" in function "update"
  - *Fix*: Fix type annotation or cast


### 19. `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/schema_composer.py` (20 critical errors)

**Type Errors:**
- Line 887: Argument of type "type[Any] | type | Any | tuple[()] | tuple[Unknown] | dict[Unknown, Unknown]" cannot be assigned to parameter "field_type" of type "type" in function "add_field"
  - *Fix*: Fix type annotation or cast
- Line 1006: Argument of type "type[Any]" cannot be assigned to parameter "cls" of type "type" in function "issubclass"
  - *Fix*: Fix type annotation or cast
- Line 1022: Argument of type "type[StateSchema[Unknown, Unknown]] | type[Any]" cannot be assigned to parameter "field_type" of type "type" in function "add_field"
  - *Fix*: Fix type annotation or cast


### 20. `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/simple/agent_v3.py` (19 critical errors)

**Type Errors:**
- Line 275: Argument of type "(change_type: str, tool_name: str, **kwargs: Unknown) -> None" cannot be assigned to parameter "callback" of type "(str, str, str | None) -> None" in function "register_route_change_callback"
  - *Fix*: Fix type annotation or cast
- Line 537: Argument of type "(change_type: str, tool_name: str, **kwargs: Unknown) -> None" cannot be assigned to parameter "callback" of type "(str, str, str | None) -> None" in function "register_route_change_callback"
  - *Fix*: Fix type annotation or cast
- Line 704: Argument of type "BaseOutputParser[Unknown] | Literal[True] | None" cannot be assigned to parameter "needs_parsing" of type "bool" in function "_add_validation_nodes"
  - *Fix*: Fix type annotation or cast

**Other Errors:**
- Line 741: "context" is not defined


## Quick Wins

These patterns appear frequently and can be fixed systematically:

- Add `from typing import Dict` (4 occurrences)
- Add `from typing import Any` (2 occurrences)
- Add `from typing import Optional` (1 occurrences)
