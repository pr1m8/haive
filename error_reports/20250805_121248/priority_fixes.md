# Priority Fix Recommendations

Fix these files first - they contain runtime-breaking errors:

## Critical Files (Top 20)


### 1. `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/factories/compatible_rag_factory.py` (98 critical errors)

**Other Errors:**
- Line 207: "SequentialAgent" is not defined
- Line 207: "ConditionalAgent" is not defined
- Line 207: "ParallelAgent" is not defined


### 2. `/home/will/Projects/haive/backend/haive/packages/haive-games/tests/test_reversi_state.py` (82 critical errors)

**Other Errors:**
- Line 21: No overloads for "__setitem__" match the provided arguments
- Line 22: No overloads for "__setitem__" match the provided arguments
- Line 23: No overloads for "__setitem__" match the provided arguments

**Type Errors:**
- Line 21: Argument of type "Literal['W']" cannot be assigned to parameter "value" of type "None" in function "__setitem__"
  - *Fix*: Fix type annotation or cast
- Line 22: Argument of type "Literal['B']" cannot be assigned to parameter "value" of type "None" in function "__setitem__"
  - *Fix*: Fix type annotation or cast


### 3. `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/NodeFactory.py` (48 critical errors)

**Type Errors:**
- Line 122: Argument of type "InvokableEngine[Unknown, Unknown]" cannot be assigned to parameter "engine" of type "VectorStoreConfig" in function "_create_vectorstore_node"
  - *Fix*: Fix type annotation or cast
- Line 130: Argument of type "InvokableEngine[Unknown, Unknown]" cannot be assigned to parameter "engine" of type "BaseRetrieverConfig" in function "_create_retriever_node"
  - *Fix*: Fix type annotation or cast
- Line 153: Argument of type "NonInvokableEngine[Unknown, Unknown]" cannot be assigned to parameter "engine" of type "EmbeddingsEngineConfig" in function "_create_embeddings_node"
  - *Fix*: Fix type annotation or cast


### 4. `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/self_healing_code/agent.py` (43 critical errors)

**Other Errors:**
- Line 4: "AgentArchitectureConfig" is not defined
- Line 5: "SelfHealingCodeState" is not defined
- Line 8: "AgentArchitecture" is not defined


### 5. `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py` (39 critical errors)

**Other Errors:**
- Line 359: No overloads for "update" match the provided arguments
- Line 361: No overloads for "update" match the provided arguments
- Line 365: No overloads for "update" match the provided arguments

**Type Errors:**
- Line 359: Argument of type "dict[str, NodeType | dict[str, (...) -> object] | Unknown]" cannot be assigned to parameter "m" of type "Iterable[tuple[str, str]]" in function "update"
  - *Fix*: Fix type annotation or cast
- Line 361: Argument of type "dict[str, NodeType | dict[str, Any] | Unknown]" cannot be assigned to parameter "m" of type "Iterable[tuple[str, str]]" in function "update"
  - *Fix*: Fix type annotation or cast


### 6. `/home/will/Projects/haive/backend/haive/packages/haive-games/tests/test_reversi_state_manager.py` (34 critical errors)

**Other Errors:**
- Line 99: No overloads for "__setitem__" match the provided arguments
- Line 198: No overloads for "__setitem__" match the provided arguments

**Type Errors:**
- Line 99: Argument of type "Literal['W']" cannot be assigned to parameter "value" of type "None" in function "__setitem__"
  - *Fix*: Fix type annotation or cast
- Line 101: Argument of type "list[list[None]]" cannot be assigned to parameter "board" of type "list[list[str | None]]" in function "__init__"
  - *Fix*: Fix type annotation or cast
- Line 198: Argument of type "Literal['W']" cannot be assigned to parameter "value" of type "None" in function "__setitem__"
  - *Fix*: Fix type annotation or cast


### 7. `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/loaders/sources/factory.py` (32 critical errors)

**Type Errors:**
- Line 87: "SourceType" is not defined
  - *Fix*: Fix type annotation or cast
- Line 114: "SourceType" is not defined
  - *Fix*: Fix type annotation or cast
- Line 125: "SourceType" is not defined
  - *Fix*: Fix type annotation or cast


### 8. `/home/will/Projects/haive/backend/haive/packages/haive-core/tests/schema/test_new_messages_state.py` (32 critical errors)

**Type Errors:**
- Line 25: Argument of type "Literal['Hello world']" cannot be assigned to parameter "root" of type "list[AnyMessage]" in function "__init__"
  - *Fix*: Fix type annotation or cast
- Line 78: Argument of type "list[str]" cannot be assigned to parameter "root" of type "list[AnyMessage]" in function "__init__"
  - *Fix*: Fix type annotation or cast
- Line 90: Argument of type "AnyMessage | list[AnyMessage]" cannot be assigned to parameter "obj" of type "Sized" in function "len"
  - *Fix*: Fix type annotation or cast


### 9. `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py` (32 critical errors)

**Other Errors:**
- Line 5: "GridBoard" is not defined
- Line 5: "CrosswordCell" is not defined
- Line 5: "CrosswordLetter" is not defined


### 10. `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/factories/rag_workflow_factory.py` (31 critical errors)

**Type Errors:**
- Line 95: Argument of type "dict[str, str]" cannot be assigned to parameter "destinations" of type "str | list[str] | dict[bool | str | int, str] | None" in function "add_conditional_edges"
  - *Fix*: Fix type annotation or cast

**Other Errors:**
- Line 120: "rag_workflow_router" is not defined
- Line 123: "advanced_document_grader" is not defined
- Line 124: "relevance_threshold_check" is not defined


### 11. `/home/will/Projects/haive/backend/haive/packages/haive-mcp/examples/production_mcp_harvester.py` (31 critical errors)

**Type Errors:**
- Line 252: Argument of type "str" cannot be assigned to parameter "tags" of type "list[str]" in function "__init__"
  - *Fix*: Fix type annotation or cast
- Line 252: Argument of type "str" cannot be assigned to parameter "transport_types" of type "list[str]" in function "__init__"
  - *Fix*: Fix type annotation or cast
- Line 252: Argument of type "str" cannot be assigned to parameter "capabilities" of type "list[str]" in function "__init__"
  - *Fix*: Fix type annotation or cast


### 12. `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/agent.py` (29 critical errors)

**Other Errors:**
- Line 321: No overloads for "create_model" match the provided arguments

**Type Errors:**
- Line 321: Argument of type "tuple[type, Any]" cannot be assigned to parameter "__config__" of type "ConfigDict | None" in function "create_model"
  - *Fix*: Fix type annotation or cast
- Line 321: Argument of type "tuple[type, Any]" cannot be assigned to parameter "__doc__" of type "str | None" in function "create_model"
  - *Fix*: Fix type annotation or cast
- Line 321: Argument of type "tuple[type, Any]" cannot be assigned to parameter "__module__" of type "str" in function "create_model"
  - *Fix*: Fix type annotation or cast


### 13. `/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/models/procedural/models.py` (29 critical errors)

**Other Errors:**
- Line 63: "Dict" is not defined
- Line 64: "List" is not defined
- Line 65: "List" is not defined


### 14. `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/agent/agent.py` (29 critical errors)

**Type Errors:**
- Line 182: Argument of type "TConfig@Agent" cannot be assigned to parameter "config_schema" of type "type[Any] | None" in function "__init__"
  - *Fix*: Fix type annotation or cast

**Other Errors:**
- Line 967: Cannot instantiate abstract class "BaseStore"
- Line 1002: Cannot instantiate abstract class "BaseStore"
- Line 1086: Cannot instantiate abstract class "BaseStore"


### 15. `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_state.py` (28 critical errors)

**Other Errors:**
- Line 187: No overloads for "__setitem__" match the provided arguments
- Line 411: No overloads for "search" match the provided arguments

**Type Errors:**
- Line 187: Argument of type "BaseMessage" cannot be assigned to parameter "value" of type "AnyMessage" in function "__setitem__"
  - *Fix*: Fix type annotation or cast
- Line 411: Argument of type "str | list[str | dict[Unknown, Unknown]]" cannot be assigned to parameter "string" of type "str" in function "search"
  - *Fix*: Fix type annotation or cast
- Line 477: Argument of type "list[AIMessage]" cannot be assigned to parameter "iterable" of type "Iterable[HumanMessage]" in function "extend"
  - *Fix*: Fix type annotation or cast


### 16. `/home/will/Projects/haive/backend/haive/packages/haive-agents/tests/test_planning/test_p_and_e_multi_agent.py` (27 critical errors)

**Type Errors:**
- Line 47: Argument of type "Literal['pending']" cannot be assigned to parameter "status" of type "StepStatus" in function "__init__"
  - *Fix*: Fix type annotation or cast
- Line 53: Argument of type "Literal['pending']" cannot be assigned to parameter "status" of type "StepStatus" in function "__init__"
  - *Fix*: Fix type annotation or cast
- Line 59: Argument of type "Literal['pending']" cannot be assigned to parameter "status" of type "StepStatus" in function "__init__"
  - *Fix*: Fix type annotation or cast


### 17. `/home/will/Projects/haive/backend/haive/packages/haive-core/tests/test_dynamic_activation_pattern.py` (27 critical errors)

**Other Errors:**
- Line 49: "MockTool" is not defined
- Line 56: "MockComponent" is not defined
- Line 64: "MockTool" is not defined


### 18. `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/message_transformation.py` (25 critical errors)

**Type Errors:**
- Line 114: Argument of type "str | Send | list[Send | str] | None" cannot be assigned to parameter "goto" of type "Send | Sequence[Send | str] | str" in function "__init__"
  - *Fix*: Fix type annotation or cast
- Line 123: Argument of type "str | Send | list[Send | str] | None" cannot be assigned to parameter "goto" of type "Send | Sequence[Send | str] | str" in function "__init__"
  - *Fix*: Fix type annotation or cast
- Line 127: Argument of type "str | Send | list[Send | str] | None" cannot be assigned to parameter "goto" of type "Send | Sequence[Send | str] | str" in function "__init__"
  - *Fix*: Fix type annotation or cast


### 19. `/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py` (25 critical errors)

**Type Errors:**
- Line 152: Argument of type "UnionType" cannot be assigned to parameter "field_type" of type "type[Any] | None" in function "__init__"
  - *Fix*: Fix type annotation or cast
- Line 235: Argument of type "dict[Unknown, Unknown]" cannot be assigned to parameter "value" of type "str | list[str | dict[Unknown, Unknown]]" in function "__setitem__"
  - *Fix*: Fix type annotation or cast
- Line 238: Argument of type "dict[Any, Any]" cannot be assigned to parameter "value" of type "str | list[str | dict[Unknown, Unknown]]" in function "__setitem__"
  - *Fix*: Fix type annotation or cast

**Other Errors:**
- Line 239: No overloads for "__setitem__" match the provided arguments


### 20. `/home/will/Projects/haive/backend/haive/packages/haive-core/tests/graph/node/test_node_system.py` (25 critical errors)

**Type Errors:**
- Line 171: Object of type "None" is not subscriptable
  - *Fix*: Fix type annotation or cast
- Line 172: Object of type "None" is not subscriptable
  - *Fix*: Fix type annotation or cast
- Line 174: Object of type "None" is not subscriptable
  - *Fix*: Fix type annotation or cast


## Quick Wins

These patterns appear frequently and can be fixed systematically:

- Add `from typing import Dict` (4 occurrences)
- Add `from typing import Any` (2 occurrences)
- Add `from typing import Optional` (1 occurrences)
