# HAIVE-DATAFLOW - Pyright Issues Checklist

**Total Errors**: 666
**Total Warnings**: 0
**Priority**: 📋 Standard

## Summary by Issue Type

### Error Categories

- **reportAttributeAccessIssue**: 281 issues
- **reportMissingImports**: 113 issues
- **reportCallIssue**: 89 issues
- **reportOptionalMemberAccess**: 78 issues
- **reportArgumentType**: 76 issues
- **reportGeneralTypeIssues**: 20 issues
- **reportRedeclaration**: 4 issues
- **reportReturnType**: 3 issues
- **reportInvalidTypeForm**: 1 issues
- **reportUnusedExcept**: 1 issues

## 🚨 ERRORS (Must Fix)

### 📄 haive-dataflow/src/haive/dataflow/api/app.py

- [ ] **Line 33** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.api.middleware.logging" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/app.py:33:5`

- [ ] **Line 34** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.api.middleware.rate_limit" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/app.py:34:5`

- [ ] **Line 35** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.api.routes.agent_discovery_routes" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/app.py:35:5`

- [ ] **Line 38** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.api.routes.agent_routes" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/app.py:38:5`

- [ ] **Line 39** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.api.routes.conversation_routes" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/app.py:39:5`

- [ ] **Line 42** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.api.routes.llm_routes" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/app.py:42:5`

- [ ] **Line 43** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.api.routes.tools_routes" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/app.py:43:5`

- [ ] **Line 44** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.auth.middleware" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/app.py:44:5`

- [ ] **Line 45** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.config.settings" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/app.py:45:5`

### 📄 haive-dataflow/src/haive/dataflow/api/app_dep.py

- [ ] **Line 9** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.api.registry" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/app_dep.py:9:5`

- [ ] **Line 10** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.api.router" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/app_dep.py:10:5`

### 📄 haive-dataflow/src/haive/dataflow/api/base.py

- [ ] **Line 15** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.models.llm.base" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/base.py:15:5`

- [ ] **Line 23** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.models.llm.provider_types" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/base.py:23:5`

- [ ] **Line 139** (`reportCallIssue`)
  - **Issue**: No overloads for "Field" match the provided arguments
      Argument types: (EllipsisType, Literal['Name of the tool'], Literal['calculator'])
  - **Location**: `haive-dataflow/src/haive/dataflow/api/base.py:139:16`

### 📄 haive-dataflow/src/haive/dataflow/api/connect4_api.py

- [ ] **Line 12** (`reportMissingImports`)
  - **Issue**: Import "haive.api.api.game_agent" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/connect4_api.py:12:5`

- [ ] **Line 13** (`reportMissingImports`)
  - **Issue**: Import "haive_games.connect4.agent" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/connect4_api.py:13:5`

- [ ] **Line 14** (`reportMissingImports`)
  - **Issue**: Import "haive_games.connect4.config" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/connect4_api.py:14:5`

- [ ] **Line 15** (`reportMissingImports`)
  - **Issue**: Import "haive_games.connect4.state" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/connect4_api.py:15:5`

- [ ] **Line 18** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.api.game_agent" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/connect4_api.py:18:5`

- [ ] **Line 388** (`reportAttributeAccessIssue`)
  - **Issue**: "WindowsSelectorEventLoopPolicy" is not a known attribute of module "asyncio"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/connect4_api.py:388:50`

### 📄 haive-dataflow/src/haive/dataflow/api/db.py

- [ ] **Line 51** (`reportOptionalMemberAccess`)
  - **Issue**: "cursor" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/db.py:51:33`

- [ ] **Line 58** (`reportOptionalMemberAccess`)
  - **Issue**: "commit" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/db.py:58:32`

- [ ] **Line 63** (`reportOptionalMemberAccess`)
  - **Issue**: "rollback" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/db.py:63:28`

- [ ] **Line 76** (`reportOptionalMemberAccess`)
  - **Issue**: "cursor" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/db.py:76:33`

- [ ] **Line 146** (`reportOptionalMemberAccess`)
  - **Issue**: "commit" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/db.py:146:32`

- [ ] **Line 153** (`reportOptionalMemberAccess`)
  - **Issue**: "rollback" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/db.py:153:28`

- [ ] **Line 173** (`reportOptionalMemberAccess`)
  - **Issue**: "cursor" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/db.py:173:33`

- [ ] **Line 241** (`reportAttributeAccessIssue`)
  - **Issue**: "extras" is not a known attribute of module "psycopg2"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/db.py:241:33`

- [ ] **Line 245** (`reportOptionalMemberAccess`)
  - **Issue**: "commit" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/db.py:245:32`

- [ ] **Line 250** (`reportOptionalMemberAccess`)
  - **Issue**: "rollback" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/db.py:250:28`

- [ ] **Line 266** (`reportOptionalMemberAccess`)
  - **Issue**: "cursor" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/db.py:266:33`

### 📄 haive-dataflow/src/haive/dataflow/api/game_agent.py

- [ ] **Line 14** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.engine.agent.persistence.memory_config" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_agent.py:14:5`

- [ ] **Line 17** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.engine.agent.persistence.postgres_config" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_agent.py:17:5`

- [ ] **Line 345** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "initialize" for class "type[BaseModel]"
      Attribute "initialize" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_agent.py:345:51`

- [ ] **Line 347** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "initialize" for class "type[BaseModel]"
      Attribute "initialize" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_agent.py:347:52`

- [ ] **Line 347** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "model_dump" for class "object"
      Attribute "model_dump" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_agent.py:347:65`

- [ ] **Line 372** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "initialize" for class "type[BaseModel]"
      Attribute "initialize" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_agent.py:372:47`

- [ ] **Line 372** (`reportOptionalMemberAccess`)
  - **Issue**: "initialize" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_agent.py:372:47`

### 📄 haive-dataflow/src/haive/dataflow/api/game_api.py

- [ ] **Line 35** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.api.game_socket" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_api.py:35:5`

- [ ] **Line 36** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.engine.agent.agent" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_api.py:36:5`

- [ ] **Line 37** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.persistence.supabase_config" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_api.py:37:5`

- [ ] **Line 38** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.schema.state_schema" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_api.py:38:5`

- [ ] **Line 184** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "model_dump" for class "object"
      Attribute "model_dump" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_api.py:184:67`

- [ ] **Line 330** (`reportAttributeAccessIssue`)
  - **Issue**: "WindowsSelectorEventLoopPolicy" is not a known attribute of module "asyncio"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_api.py:330:54`

### 📄 haive-dataflow/src/haive/dataflow/api/game_router.py

- [ ] **Line 105** (`reportCallIssue`)
  - **Issue**: No overloads for "dirname" match the provided arguments
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_router.py:105:20`

- [ ] **Line 105** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "p" of type "AnyOrLiteralStr@dirname" in function "dirname"
      Type "str | None" is not assignable to constrained type variable "AnyOrLiteralStr"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_router.py:105:36`

### 📄 haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py

- [ ] **Line 52** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.utils.haive_discovery" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py:52:5`

- [ ] **Line 206** (`reportCallIssue`)
  - **Issue**: No overloads for "**getitem**" match the provided arguments
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py:206:31`

- [ ] **Line 206** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['agent']" cannot be assigned to parameter "s" of type "slice[Any, Any, Any]" in function "**getitem**"
      "Literal['agent']" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py:206:31`

- [ ] **Line 207** (`reportCallIssue`)
  - **Issue**: No overloads for "**getitem**" match the provided arguments
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py:207:26`

- [ ] **Line 207** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['agent']" cannot be assigned to parameter "s" of type "slice[Any, Any, Any]" in function "**getitem**"
      "Literal['agent']" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py:207:26`

- [ ] **Line 208** (`reportCallIssue`)
  - **Issue**: No overloads for "**getitem**" match the provided arguments
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py:208:34`

- [ ] **Line 208** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['agent']" cannot be assigned to parameter "s" of type "slice[Any, Any, Any]" in function "**getitem**"
      "Literal['agent']" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py:208:34`

- [ ] **Line 213** (`reportCallIssue`)
  - **Issue**: No overloads for "**getitem**" match the provided arguments
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py:213:56`

- [ ] **Line 213** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['state']" cannot be assigned to parameter "s" of type "slice[Any, Any, Any]" in function "**getitem**"
      "Literal['state']" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_router_enhanced.py:213:56`

### 📄 haive-dataflow/src/haive/dataflow/api/game_router_fixed.py

- [ ] **Line 69** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "class_obj" for class "ComponentInfo"
      Attribute "class_obj" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_router_fixed.py:69:62`

- [ ] **Line 79** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "class_obj" for class "ComponentInfo"
      Attribute "class_obj" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_router_fixed.py:79:45`

- [ ] **Line 90** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "class_obj" for class "ComponentInfo"
      Attribute "class_obj" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_router_fixed.py:90:22`

- [ ] **Line 212** (`reportReturnType`)
  - **Issue**: Type "dict[str, Any] | None" is not assignable to return type "dict[str, Any]"
      Type "dict[str, Any] | None" is not assignable to type "dict[str, Any]"
        "None" is not assignable to "dict[str, Any]"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_router_fixed.py:212:11`

### 📄 haive-dataflow/src/haive/dataflow/api/game_socket.py

- [ ] **Line 349** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get_config_class" for class "type[Agent[Unknown]]"
      Attribute "get_config_class" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_socket.py:349:40`

- [ ] **Line 480** (`reportArgumentType`)
  - **Issue**: Argument of type "type[Connect4State]" cannot be assigned to parameter "state_schema" of type "type[StateSchema[Unknown, Unknown]]" in function "create_socket"
      "type[Connect4State]" is not assignable to "type[StateSchema[Unknown, Unknown]]"
      Type "type[Connect4State]" is not assignable to type "type[StateSchema[Unknown, Unknown]]"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_socket.py:480:25`

- [ ] **Line 499** (`reportArgumentType`)
  - **Issue**: Argument of type "type[TicTacToeState]" cannot be assigned to parameter "state_schema" of type "type[StateSchema[Unknown, Unknown]]" in function "create_socket"
      "type[TicTacToeState]" is not assignable to "type[StateSchema[Unknown, Unknown]]"
      Type "type[TicTacToeState]" is not assignable to type "type[StateSchema[Unknown, Unknown]]"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/game_socket.py:499:25`

### 📄 haive-dataflow/src/haive/dataflow/api/general_games_api.py

- [ ] **Line 40** (`reportMissingImports`)
  - **Issue**: Import "haive.games.common.config" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/general_games_api.py:40:9`

- [ ] **Line 123** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "args" of type "StrPath" in function "**new**"
      Type "str | None" is not assignable to type "StrPath"
        Type "None" is not assignable to type "StrPath"
          "None" is not assignable to "str"
          "None" is incompatible with protocol "PathLike[str]"
            "**fspath**" is not present
  - **Location**: `haive-dataflow/src/haive/dataflow/api/general_games_api.py:123:30`

- [ ] **Line 123** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "args" of type "StrPath" in function "**init**"
      Type "str | None" is not assignable to type "StrPath"
        Type "None" is not assignable to type "StrPath"
          "None" is not assignable to "str"
          "None" is incompatible with protocol "PathLike[str]"
            "**fspath**" is not present
  - **Location**: `haive-dataflow/src/haive/dataflow/api/general_games_api.py:123:30`

- [ ] **Line 177** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get_config_class" for class "type[Agent[Unknown]]"
      Attribute "get_config_class" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/api/general_games_api.py:177:47`

- [ ] **Line 391** (`reportOptionalMemberAccess`)
  - **Issue**: "default" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/general_games_api.py:391:40`

### 📄 haive-dataflow/src/haive/dataflow/api/integrate_games.py

- [ ] **Line 22** (`reportMissingImports`)
  - **Issue**: Import "game_router" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/integrate_games.py:22:7`

### 📄 haive-dataflow/src/haive/dataflow/api/llms/api.py

- [ ] **Line 17** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.llms.api.llms.models" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/llms/api.py:17:5`

### 📄 haive-dataflow/src/haive/dataflow/api/main.py

- [ ] **Line 3** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.api.connect4_api" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/main.py:3:5`

- [ ] **Line 4** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.api.tic_tac_toe_api" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/main.py:4:5`

### 📄 haive-dataflow/src/haive/dataflow/api/middleware.py

- [ ] **Line 84** (`reportOptionalMemberAccess`)
  - **Issue**: "host" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/middleware.py:84:76`

### 📄 haive-dataflow/src/haive/dataflow/api/middleware/auth.py

- [ ] **Line 8** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.middleware.auth.supabase" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/middleware/auth.py:8:5`

- [ ] **Line 9** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.middleware.config.environment" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/middleware/auth.py:9:5`

### 📄 haive-dataflow/src/haive/dataflow/api/middleware/rate_limit.py

- [ ] **Line 37** (`reportOptionalMemberAccess`)
  - **Issue**: "host" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/middleware/rate_limit.py:37:47`

### 📄 haive-dataflow/src/haive/dataflow/api/middleware/supabase_logging.py

- [ ] **Line 16** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.middleware.config.environment" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/middleware/supabase_logging.py:16:5`

- [ ] **Line 98** (`reportGeneralTypeIssues`)
  - **Issue**: "APIResponse[_TableT]" is not awaitable
      "APIResponse[_TableT]" is incompatible with protocol "Awaitable[_T_co@Awaitable]"
        "**await**" is not present
  - **Location**: `haive-dataflow/src/haive/dataflow/api/middleware/supabase_logging.py:98:22`

- [ ] **Line 164** (`reportGeneralTypeIssues`)
  - **Issue**: "APIResponse[_TableT]" is not awaitable
      "APIResponse[_TableT]" is incompatible with protocol "Awaitable[_T_co@Awaitable]"
        "**await**" is not present
  - **Location**: `haive-dataflow/src/haive/dataflow/api/middleware/supabase_logging.py:164:22`

- [ ] **Line 297** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "body_iterator" for class "Response"
      Attribute "body_iterator" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/api/middleware/supabase_logging.py:297:49`

### 📄 haive-dataflow/src/haive/dataflow/api/registry.py

- [ ] **Line 14** (`reportMissingImports`)
  - **Issue**: Import "haive.api.api.db" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/registry.py:14:5`

- [ ] **Line 18** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.engine.agent.agent" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/registry.py:18:5`

- [ ] **Line 374** (`reportAttributeAccessIssue`)
  - **Issue**: "load_checkpointer_config" is unknown import symbol
  - **Location**: `haive-dataflow/src/haive/dataflow/api/registry.py:374:24`

### 📄 haive-dataflow/src/haive/dataflow/api/router.py

- [ ] **Line 13** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.api.registry" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/router.py:13:5`

### 📄 haive-dataflow/src/haive/dataflow/api/routers/games.py

- [ ] **Line 11** (`reportAttributeAccessIssue`)
  - **Issue**: "GameInfo" is unknown import symbol
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routers/games.py:11:28`

- [ ] **Line 11** (`reportAttributeAccessIssue`)
  - **Issue**: "GameSelectionRequest" is unknown import symbol
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routers/games.py:11:38`

- [ ] **Line 11** (`reportAttributeAccessIssue`)
  - **Issue**: "create_general_game_api" is unknown import symbol
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routers/games.py:11:60`

- [ ] **Line 41** (`reportArgumentType`)
  - **Issue**: Argument of type "list[str] | list[str | Enum]" cannot be assigned to parameter "tags" of type "List[str | Enum] | None" in function "**init**"
      Type "list[str] | list[str | Enum]" is not assignable to type "List[str | Enum] | None"
        Type "list[str]" is not assignable to type "List[str | Enum] | None"
          "list[str]" is not assignable to "List[str | Enum]"
            Type parameter "\_T@list" is invariant, but "str" is not the same as "str | Enum"
            Consider switching from "list" to "Sequence" which is covariant
          "list[str]" is not assignable to "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routers/games.py:41:13`

- [ ] **Line 77** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "endpoint" for class "BaseRoute"
      Attribute "endpoint" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routers/games.py:77:52`

- [ ] **Line 80** (`reportInvalidTypeForm`)
  - **Issue**: Variable not allowed in type expression
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routers/games.py:80:39`

- [ ] **Line 84** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "path" for class "BaseRoute"
      Attribute "path" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routers/games.py:84:25`

- [ ] **Line 84** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "methods" for class "BaseRoute"
      Attribute "methods" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routers/games.py:84:63`

- [ ] **Line 85** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "endpoint" for class "BaseRoute"
      Attribute "endpoint" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routers/games.py:85:39`

### 📄 haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes.py

- [ ] **Line 351** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "config_schema", "init_schema"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes.py:351:22`

### 📄 haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes_enhanced.py

- [ ] **Line 43** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.routes.utils.haive_discovery" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes_enhanced.py:43:5`

### 📄 haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes_fixed.py

- [ ] **Line 15** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.routes.utils.haive_discovery" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes_fixed.py:15:5`

- [ ] **Line 360** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "config_schema", "init_schema"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_discovery_routes_fixed.py:360:22`

### 📄 haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py

- [ ] **Line 81** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.routes.auth.dependencies" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:81:5`

- [ ] **Line 82** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.routes.auth.supabase" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:82:5`

- [ ] **Line 83** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.routes.engine.agent.config" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:83:5`

- [ ] **Line 84** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.routes.engine.aug_llm" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:84:5`

- [ ] **Line 85** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.routes.models.llm.base" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:85:5`

- [ ] **Line 93** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.routes.models.llm.provider_types" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:93:5`

- [ ] **Line 385** (`reportArgumentType`)
  - **Issue**: Argument of type "ModuleSpec | None" cannot be assigned to parameter "spec" of type "ModuleSpec" in function "module_from_spec"
      Type "ModuleSpec | None" is not assignable to type "ModuleSpec"
        "None" is not assignable to "ModuleSpec"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:385:60`

- [ ] **Line 386** (`reportOptionalMemberAccess`)
  - **Issue**: "loader" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:386:17`

- [ ] **Line 386** (`reportOptionalMemberAccess`)
  - **Issue**: "exec_module" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:386:24`

- [ ] **Line 434** (`reportArgumentType`)
  - **Issue**: Argument of type "ModuleSpec | None" cannot be assigned to parameter "spec" of type "ModuleSpec" in function "module_from_spec"
      Type "ModuleSpec | None" is not assignable to type "ModuleSpec"
        "None" is not assignable to "ModuleSpec"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:434:67`

- [ ] **Line 435** (`reportOptionalMemberAccess`)
  - **Issue**: "loader" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:435:31`

- [ ] **Line 435** (`reportOptionalMemberAccess`)
  - **Issue**: "exec_module" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:435:38`

- [ ] **Line 583** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "system_prompt"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:583:17`

- [ ] **Line 640** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "thread_id", "stream_index"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:640:22`

- [ ] **Line 693** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "thread_id", "stream_index"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:693:36`

- [ ] **Line 764** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "thread_id", "stream_index"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:764:39`

- [ ] **Line 781** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "stream_index"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:781:39`

- [ ] **Line 796** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "stream_index"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:796:44`

- [ ] **Line 806** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "thread_id", "stream_index"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:806:32`

- [ ] **Line 814** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "thread_id", "stream_index"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:814:32`

- [ ] **Line 823** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "thread_id", "stream_index"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py:823:24`

### 📄 haive-dataflow/src/haive/dataflow/api/routes/conversation_routes.py

- [ ] **Line 55** (`reportAttributeAccessIssue`)
  - **Issue**: "AgentRegistry" is unknown import symbol
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/conversation_routes.py:55:32`

- [ ] **Line 58** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.routes.auth.credits" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/conversation_routes.py:58:5`

- [ ] **Line 59** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.routes.auth.dependencies" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/conversation_routes.py:59:5`

- [ ] **Line 60** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.routes.config.settings" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/conversation_routes.py:60:5`

- [ ] **Line 61** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.routes.persistence.conversations" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/conversation_routes.py:61:5`

- [ ] **Line 66** (`reportAttributeAccessIssue`)
  - **Issue**: "AgentRegistry" is unknown import symbol
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/conversation_routes.py:66:40`

- [ ] **Line 175** (`reportGeneralTypeIssues`)
  - **Issue**: "Never" is not awaitable
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/conversation_routes.py:175:19`

### 📄 haive-dataflow/src/haive/dataflow/api/routes/example_tool.py

- [ ] **Line 20** (`reportGeneralTypeIssues`)
  - **Issue**: Expected class but received "(iterable: Iterable[object], /) -> bool"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/example_tool.py:20:68`

### 📄 haive-dataflow/src/haive/dataflow/api/routes/llm_routes.py

- [ ] **Line 56** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.routes.auth.middleware" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/llm_routes.py:56:5`

- [ ] **Line 57** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.routes.engine.aug_llm" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/llm_routes.py:57:5`

- [ ] **Line 58** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.routes.models.llm.base" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/llm_routes.py:58:5`

- [ ] **Line 66** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.routes.models.llm.provider_types" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/llm_routes.py:66:5`

- [ ] **Line 114** (`reportCallIssue`)
  - **Issue**: No overloads for "Field" match the provided arguments
      Argument types: (EllipsisType, Literal['Name of the tool'], Literal['calculator'])
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/llm_routes.py:114:16`

### 📄 haive-dataflow/src/haive/dataflow/api/routes/tools_routes.py

- [ ] **Line 19** (`reportMissingImports`)
  - **Issue**: Import "haive.core.utils.haive_discovery.enhanced_tool_discovery" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/tools_routes.py:19:5`

- [ ] **Line 236** (`reportUnusedExcept`)
  - **Issue**: Except clause is unreachable because exception is already handled
      "ImportError" is a subclass of "ImportError"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/tools_routes.py:236:11`

- [ ] **Line 469** (`reportOptionalMemberAccess`)
  - **Issue**: "args_schema" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/tools_routes.py:469:32`

- [ ] **Line 720** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "result"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/tools_routes.py:720:19`

- [ ] **Line 727** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "error"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/tools_routes.py:727:15`

- [ ] **Line 731** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "result"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/tools_routes.py:731:15`

### 📄 haive-dataflow/src/haive/dataflow/api/routes/tools_routes_enhanced.py

- [ ] **Line 43** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.routes.utils.haive_discovery" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/tools_routes_enhanced.py:43:5`

### 📄 haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py

- [ ] **Line 16** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.routes.utils.haive_discovery" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:16:5`

- [ ] **Line 368** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "result"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:368:19`

- [ ] **Line 397** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "result"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:397:23`

- [ ] **Line 401** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "error"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:401:19`

- [ ] **Line 405** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "result"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:405:19`

- [ ] **Line 409** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "result"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/routes/tools_routes_fixed.py:409:15`

### 📄 haive-dataflow/src/haive/dataflow/api/run_chess_api.py

- [ ] **Line 23** (`reportMissingImports`)
  - **Issue**: Import "game_api" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/run_chess_api.py:23:5`

### 📄 haive-dataflow/src/haive/dataflow/api/run_game_api.py

- [ ] **Line 21** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.api.game_router" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/run_game_api.py:21:5`

### 📄 haive-dataflow/src/haive/dataflow/api/run_games_api.py

- [ ] **Line 83** (`reportRedeclaration`)
  - **Issue**: Function declaration "root" is obscured by a declaration of the same name
  - **Location**: `haive-dataflow/src/haive/dataflow/api/run_games_api.py:83:22`

- [ ] **Line 102** (`reportRedeclaration`)
  - **Issue**: Function declaration "root" is obscured by a declaration of the same name
  - **Location**: `haive-dataflow/src/haive/dataflow/api/run_games_api.py:102:22`

### 📄 haive-dataflow/src/haive/dataflow/api/run_simple.py

- [ ] **Line 13** (`reportMissingImports`)
  - **Issue**: Import "game_router" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/run_simple.py:13:7`

### 📄 haive-dataflow/src/haive/dataflow/api/tic_tac_toe_api.py

- [ ] **Line 10** (`reportMissingImports`)
  - **Issue**: Import "haive_games.tic_tac_toe.agent" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/tic_tac_toe_api.py:10:5`

- [ ] **Line 11** (`reportMissingImports`)
  - **Issue**: Import "haive_games.tic_tac_toe.config" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/tic_tac_toe_api.py:11:5`

- [ ] **Line 12** (`reportMissingImports`)
  - **Issue**: Import "haive_games.tic_tac_toe.state" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/tic_tac_toe_api.py:12:5`

- [ ] **Line 13** (`reportMissingImports`)
  - **Issue**: Import "haive_games.tic_tac_toe.state_manager" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/tic_tac_toe_api.py:13:5`

- [ ] **Line 16** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.api.api.game_agent" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/api/tic_tac_toe_api.py:16:5`

- [ ] **Line 176** (`reportAttributeAccessIssue`)
  - **Issue**: "WindowsSelectorEventLoopPolicy" is not a known attribute of module "asyncio"
  - **Location**: `haive-dataflow/src/haive/dataflow/api/tic_tac_toe_api.py:176:50`

### 📄 haive-dataflow/src/haive/dataflow/auth/credits.py

- [ ] **Line 10** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.auth.config.environment" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/auth/credits.py:10:5`

- [ ] **Line 56** (`reportGeneralTypeIssues`)
  - **Issue**: "APIResponse[_TableT]" is not awaitable
      "APIResponse[_TableT]" is incompatible with protocol "Awaitable[_T_co@Awaitable]"
        "**await**" is not present
  - **Location**: `haive-dataflow/src/haive/dataflow/auth/credits.py:56:22`

- [ ] **Line 85** (`reportGeneralTypeIssues`)
  - **Issue**: "SingleAPIResponse[Any]" is not awaitable
      "SingleAPIResponse[Any]" is incompatible with protocol "Awaitable[_T_co@Awaitable]"
        "**await**" is not present
  - **Location**: `haive-dataflow/src/haive/dataflow/auth/credits.py:85:29`

- [ ] **Line 106** (`reportGeneralTypeIssues`)
  - **Issue**: "APIResponse[_TableT]" is not awaitable
      "APIResponse[_TableT]" is incompatible with protocol "Awaitable[_T_co@Awaitable]"
        "**await**" is not present
  - **Location**: `haive-dataflow/src/haive/dataflow/auth/credits.py:106:22`

### 📄 haive-dataflow/src/haive/dataflow/auth/dependencies.py

- [ ] **Line 35** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.auth.auth.supabase" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/auth/dependencies.py:35:5`

- [ ] **Line 36** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.auth.config.environment" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/auth/dependencies.py:36:5`

### 📄 haive-dataflow/src/haive/dataflow/auth/middleware.py

- [ ] **Line 9** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.auth.auth.supabase" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/auth/middleware.py:9:5`

### 📄 haive-dataflow/src/haive/dataflow/auth/supabase.py

- [ ] **Line 13** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.auth.config.environment" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/auth/supabase.py:13:5`

### 📄 haive-dataflow/src/haive/dataflow/base.py

- [ ] **Line 9** (`reportMissingImports`)
  - **Issue**: Import "haive.core.aug_llm" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/base.py:9:5`

- [ ] **Line 15** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.models.llm.base" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/base.py:15:5`

- [ ] **Line 23** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.models.llm.provider_types" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/base.py:23:5`

- [ ] **Line 139** (`reportCallIssue`)
  - **Issue**: No overloads for "Field" match the provided arguments
      Argument types: (EllipsisType, Literal['Name of the tool'], Literal['calculator'])
  - **Location**: `haive-dataflow/src/haive/dataflow/base.py:139:16`

### 📄 haive-dataflow/src/haive/dataflow/bin/litellm_cli.py

- [ ] **Line 24** (`reportAttributeAccessIssue`)
  - **Issue**: "update_availability_status" is unknown import symbol
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/litellm_cli.py:24:4`

- [ ] **Line 28** (`reportAttributeAccessIssue`)
  - **Issue**: "generate_report" is unknown import symbol
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/litellm_cli.py:28:4`

- [ ] **Line 31** (`reportAttributeAccessIssue`)
  - **Issue**: "migrate_env_vars_to_vault" is unknown import symbol
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/litellm_cli.py:31:4`

### 📄 haive-dataflow/src/haive/dataflow/bin/registry_cli.py

- [ ] **Line 76** (`reportOptionalMemberAccess`)
  - **Issue**: "print" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/registry_cli.py:76:16`

- [ ] **Line 84** (`reportOptionalMemberAccess`)
  - **Issue**: "print" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/registry_cli.py:84:16`

- [ ] **Line 85** (`reportOptionalMemberAccess`)
  - **Issue**: "print" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/registry_cli.py:85:16`

- [ ] **Line 93** (`reportOptionalMemberAccess`)
  - **Issue**: "print" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/registry_cli.py:93:16`

- [ ] **Line 94** (`reportOptionalMemberAccess`)
  - **Issue**: "print" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/registry_cli.py:94:16`

- [ ] **Line 114** (`reportOptionalMemberAccess`)
  - **Issue**: "print" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/registry_cli.py:114:16`

- [ ] **Line 288** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get_entity" for class "LazyRegistrySystem"
      Attribute "get_entity" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/registry_cli.py:288:44`

- [ ] **Line 322** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get_entity" for class "LazyRegistrySystem"
      Attribute "get_entity" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/registry_cli.py:322:43`

- [ ] **Line 356** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get_entity" for class "LazyRegistrySystem"
      Attribute "get_entity" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/registry_cli.py:356:46`

- [ ] **Line 399** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get_entity" for class "LazyRegistrySystem"
      Attribute "get_entity" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/registry_cli.py:399:45`

- [ ] **Line 447** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get_entity" for class "LazyRegistrySystem"
      Attribute "get_entity" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/registry_cli.py:447:43`

- [ ] **Line 491** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get_registry_stats" for class "LazyRegistrySystem"
      Attribute "get_registry_stats" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/registry_cli.py:491:32`

- [ ] **Line 550** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "list_entities" for class "LazyRegistrySystem"
      Attribute "list_entities" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/registry_cli.py:550:39`

- [ ] **Line 552** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "list_entities" for class "LazyRegistrySystem"
      Attribute "list_entities" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/registry_cli.py:552:39`

- [ ] **Line 616** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get_entity_details" for class "LazyRegistrySystem"
      Attribute "get_entity_details" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/registry_cli.py:616:34`

- [ ] **Line 629** (`reportOptionalMemberAccess`)
  - **Issue**: "print" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/registry_cli.py:629:20`

- [ ] **Line 643** (`reportOptionalMemberAccess`)
  - **Issue**: "print" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/registry_cli.py:643:24`

- [ ] **Line 761** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "list_entities" for class "LazyRegistrySystem"
      Attribute "list_entities" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/registry_cli.py:761:39`

- [ ] **Line 763** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "list_entities" for class "LazyRegistrySystem"
      Attribute "list_entities" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/registry_cli.py:763:39`

- [ ] **Line 826** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "clear_registry" for class "LazyRegistrySystem"
      Attribute "clear_registry" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/registry_cli.py:826:34`

### 📄 haive-dataflow/src/haive/dataflow/bin/vault_cli.py

- [ ] **Line 60** (`reportArgumentType`)
  - **Issue**: Argument of type "ModuleSpec | None" cannot be assigned to parameter "spec" of type "ModuleSpec" in function "module_from_spec"
      Type "ModuleSpec | None" is not assignable to type "ModuleSpec"
        "None" is not assignable to "ModuleSpec"
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/vault_cli.py:60:49`

- [ ] **Line 61** (`reportOptionalMemberAccess`)
  - **Issue**: "loader" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/vault_cli.py:61:13`

- [ ] **Line 61** (`reportOptionalMemberAccess`)
  - **Issue**: "exec_module" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/vault_cli.py:61:20`

- [ ] **Line 86** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/vault_cli.py:86:51`

- [ ] **Line 87** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/vault_cli.py:87:58`

- [ ] **Line 137** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/vault_cli.py:137:47`

- [ ] **Line 138** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/vault_cli.py:138:73`

- [ ] **Line 154** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/vault_cli.py:154:61`

- [ ] **Line 157** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/vault_cli.py:157:36`

- [ ] **Line 183** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "execute_sql" for class "ModuleType"
      Attribute "execute_sql" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/vault_cli.py:183:33`

- [ ] **Line 184** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "ensure_vault_reference_column" for class "ModuleType"
      Attribute "ensure_vault_reference_column" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/vault_cli.py:184:33`

- [ ] **Line 213** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "execute_sql" for class "ModuleType"
      Attribute "execute_sql" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/vault_cli.py:213:36`

- [ ] **Line 256** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "execute_sql" for class "ModuleType"
      Attribute "execute_sql" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/vault_cli.py:256:34`

- [ ] **Line 329** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/vault_cli.py:329:54`

- [ ] **Line 332** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/vault_cli.py:332:79`

- [ ] **Line 358** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/vault_cli.py:358:54`

- [ ] **Line 362** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/vault_cli.py:362:78`

- [ ] **Line 565** (`reportOptionalMemberAccess`)
  - **Issue**: "exec_module" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/bin/vault_cli.py:565:24`

### 📄 haive-dataflow/src/haive/dataflow/connect4_api.py

- [ ] **Line 12** (`reportMissingImports`)
  - **Issue**: Import "haive.api.api.game_agent" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/connect4_api.py:12:5`

- [ ] **Line 13** (`reportMissingImports`)
  - **Issue**: Import "haive_games.connect4.agent" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/connect4_api.py:13:5`

- [ ] **Line 14** (`reportMissingImports`)
  - **Issue**: Import "haive_games.connect4.config" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/connect4_api.py:14:5`

- [ ] **Line 15** (`reportMissingImports`)
  - **Issue**: Import "haive_games.connect4.state" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/connect4_api.py:15:5`

- [ ] **Line 388** (`reportAttributeAccessIssue`)
  - **Issue**: "WindowsSelectorEventLoopPolicy" is not a known attribute of module "asyncio"
  - **Location**: `haive-dataflow/src/haive/dataflow/connect4_api.py:388:50`

### 📄 haive-dataflow/src/haive/dataflow/conversations/manager.py

- [ ] **Line 11** (`reportAttributeAccessIssue`)
  - **Issue**: "SupabaseServerConfig" is unknown import symbol
  - **Location**: `haive-dataflow/src/haive/dataflow/conversations/manager.py:11:34`

- [ ] **Line 12** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.conversations.persistence.factory" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/conversations/manager.py:12:5`

- [ ] **Line 18** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.conversations.persistence.postgres_config" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/conversations/manager.py:18:5`

- [ ] **Line 69** (`reportGeneralTypeIssues`)
  - **Issue**: "APIResponse[_TableT]" is not awaitable
      "APIResponse[_TableT]" is incompatible with protocol "Awaitable[_T_co@Awaitable]"
        "**await**" is not present
  - **Location**: `haive-dataflow/src/haive/dataflow/conversations/manager.py:69:22`

- [ ] **Line 111** (`reportGeneralTypeIssues`)
  - **Issue**: "APIResponse[_TableT]" is not awaitable
      "APIResponse[_TableT]" is incompatible with protocol "Awaitable[_T_co@Awaitable]"
        "**await**" is not present
  - **Location**: `haive-dataflow/src/haive/dataflow/conversations/manager.py:111:22`

- [ ] **Line 135** (`reportGeneralTypeIssues`)
  - **Issue**: "APIResponse[_TableT]" is not awaitable
      "APIResponse[_TableT]" is incompatible with protocol "Awaitable[_T_co@Awaitable]"
        "**await**" is not present
  - **Location**: `haive-dataflow/src/haive/dataflow/conversations/manager.py:135:22`

- [ ] **Line 169** (`reportGeneralTypeIssues`)
  - **Issue**: "APIResponse[_TableT]" is not awaitable
      "APIResponse[_TableT]" is incompatible with protocol "Awaitable[_T_co@Awaitable]"
        "**await**" is not present
  - **Location**: `haive-dataflow/src/haive/dataflow/conversations/manager.py:169:22`

- [ ] **Line 187** (`reportGeneralTypeIssues`)
  - **Issue**: "APIResponse[_TableT]" is not awaitable
      "APIResponse[_TableT]" is incompatible with protocol "Awaitable[_T_co@Awaitable]"
        "**await**" is not present
  - **Location**: `haive-dataflow/src/haive/dataflow/conversations/manager.py:187:18`

### 📄 haive-dataflow/src/haive/dataflow/core.py

- [ ] **Line 99** (`reportRedeclaration`)
  - **Issue**: Method declaration "\_ensure_registry_schema" is obscured by a declaration of the same name
  - **Location**: `haive-dataflow/src/haive/dataflow/core.py:99:8`

- [ ] **Line 105** (`reportOptionalMemberAccess`)
  - **Issue**: "rpc" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/core.py:105:42`

- [ ] **Line 114** (`reportOptionalMemberAccess`)
  - **Issue**: "rpc" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/core.py:114:31`

- [ ] **Line 186** (`reportOptionalMemberAccess`)
  - **Issue**: "rpc" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/core.py:186:45`

- [ ] **Line 195** (`reportOptionalMemberAccess`)
  - **Issue**: "rpc" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/core.py:195:35`

- [ ] **Line 212** (`reportOptionalMemberAccess`)
  - **Issue**: "rpc" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/core.py:212:41`

- [ ] **Line 223** (`reportArgumentType`)
  - **Issue**: Argument of type "SyncClient | None" cannot be assigned to parameter "client" of type "SyncClient" in function "table"
      Type "SyncClient | None" is not assignable to type "SyncClient"
        "None" is not assignable to "SyncClient"
  - **Location**: `haive-dataflow/src/haive/dataflow/core.py:223:26`

- [ ] **Line 253** (`reportArgumentType`)
  - **Issue**: Argument of type "SyncClient | None" cannot be assigned to parameter "client" of type "SyncClient" in function "table"
      Type "SyncClient | None" is not assignable to type "SyncClient"
        "None" is not assignable to "SyncClient"
  - **Location**: `haive-dataflow/src/haive/dataflow/core.py:253:30`

- [ ] **Line 508** (`reportArgumentType`)
  - **Issue**: Argument of type "SyncClient | None" cannot be assigned to parameter "client" of type "SyncClient" in function "table"
      Type "SyncClient | None" is not assignable to type "SyncClient"
        "None" is not assignable to "SyncClient"
  - **Location**: `haive-dataflow/src/haive/dataflow/core.py:508:22`

- [ ] **Line 527** (`reportArgumentType`)
  - **Issue**: Argument of type "SyncClient | None" cannot be assigned to parameter "client" of type "SyncClient" in function "table"
      Type "SyncClient | None" is not assignable to type "SyncClient"
        "None" is not assignable to "SyncClient"
  - **Location**: `haive-dataflow/src/haive/dataflow/core.py:527:22`

- [ ] **Line 542** (`reportOptionalMemberAccess`)
  - **Issue**: "query" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/core.py:542:42`

- [ ] **Line 542** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "query" for class "SyncClient"
      Attribute "query" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/core.py:542:42`

- [ ] **Line 569** (`reportArgumentType`)
  - **Issue**: Argument of type "SyncClient | None" cannot be assigned to parameter "client" of type "SyncClient" in function "table"
      Type "SyncClient | None" is not assignable to type "SyncClient"
        "None" is not assignable to "SyncClient"
  - **Location**: `haive-dataflow/src/haive/dataflow/core.py:569:22`

- [ ] **Line 588** (`reportArgumentType`)
  - **Issue**: Argument of type "SyncClient | None" cannot be assigned to parameter "client" of type "SyncClient" in function "table"
      Type "SyncClient | None" is not assignable to type "SyncClient"
        "None" is not assignable to "SyncClient"
  - **Location**: `haive-dataflow/src/haive/dataflow/core.py:588:22`

- [ ] **Line 603** (`reportOptionalMemberAccess`)
  - **Issue**: "query" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/core.py:603:42`

- [ ] **Line 603** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "query" for class "SyncClient"
      Attribute "query" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/core.py:603:42`

- [ ] **Line 977** (`reportOptionalMemberAccess`)
  - **Issue**: "rpc" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/core.py:977:42`

- [ ] **Line 986** (`reportOptionalMemberAccess`)
  - **Issue**: "rpc" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/core.py:986:31`

- [ ] **Line 1059** (`reportOptionalMemberAccess`)
  - **Issue**: "rpc" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/core.py:1059:49`

- [ ] **Line 1068** (`reportOptionalMemberAccess`)
  - **Issue**: "rpc" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/core.py:1068:39`

- [ ] **Line 1140** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "code" for class "Exception"
      Attribute "code" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/core.py:1140:49`

- [ ] **Line 1184** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "query" for class "SyncClient"
      Attribute "query" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/core.py:1184:35`

- [ ] **Line 1526** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['llm', 'llm_provider', 'embedding', 'embedding_provider', 'agent', 'tool', 'workflow', 'data_source', 'custom']" cannot be assigned to parameter "entity_type" of type "EntityType" in function "get_entities_by_type"
      Type "Literal['llm', 'llm_provider', 'embedding', 'embedding_provider', 'agent', 'tool', 'workflow', 'data_source', 'custom']" is not assignable to type "EntityType"
        "Literal['agent']" is not assignable to "EntityType"
  - **Location**: `haive-dataflow/src/haive/dataflow/core.py:1526:50`

### 📄 haive-dataflow/src/haive/dataflow/db.py

- [ ] **Line 51** (`reportOptionalMemberAccess`)
  - **Issue**: "cursor" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/db.py:51:33`

- [ ] **Line 58** (`reportOptionalMemberAccess`)
  - **Issue**: "commit" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/db.py:58:32`

- [ ] **Line 63** (`reportOptionalMemberAccess`)
  - **Issue**: "rollback" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/db.py:63:28`

- [ ] **Line 76** (`reportOptionalMemberAccess`)
  - **Issue**: "cursor" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/db.py:76:33`

- [ ] **Line 146** (`reportOptionalMemberAccess`)
  - **Issue**: "commit" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/db.py:146:32`

- [ ] **Line 153** (`reportOptionalMemberAccess`)
  - **Issue**: "rollback" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/db.py:153:28`

- [ ] **Line 173** (`reportOptionalMemberAccess`)
  - **Issue**: "cursor" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/db.py:173:33`

- [ ] **Line 241** (`reportAttributeAccessIssue`)
  - **Issue**: "extras" is not a known attribute of module "psycopg2"
  - **Location**: `haive-dataflow/src/haive/dataflow/db.py:241:33`

- [ ] **Line 245** (`reportOptionalMemberAccess`)
  - **Issue**: "commit" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/db.py:245:32`

- [ ] **Line 250** (`reportOptionalMemberAccess`)
  - **Issue**: "rollback" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/db.py:250:28`

- [ ] **Line 266** (`reportOptionalMemberAccess`)
  - **Issue**: "cursor" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/db.py:266:33`

### 📄 haive-dataflow/src/haive/dataflow/db/inspect_supabase.py

- [ ] **Line 1** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.db.db.supabase" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/db/inspect_supabase.py:1:5`

### 📄 haive-dataflow/src/haive/dataflow/db/schema.py

- [ ] **Line 246** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/db/schema.py:246:59`

- [ ] **Line 247** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/db/schema.py:247:68`

- [ ] **Line 455** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/db/schema.py:455:51`

- [ ] **Line 459** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/db/schema.py:459:76`

### 📄 haive-dataflow/src/haive/dataflow/discovery.py

- [ ] **Line 59** (`reportCallIssue`)
  - **Issue**: No overloads for "dirname" match the provided arguments
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:59:23`

- [ ] **Line 59** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "p" of type "AnyOrLiteralStr@dirname" in function "dirname"
      Type "str | None" is not assignable to constrained type variable "AnyOrLiteralStr"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:59:39`

- [ ] **Line 162** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "name" for class "object"
      Attribute "name" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:162:41`

- [ ] **Line 174** (`reportCallIssue`)
  - **Issue**: No parameter named "module_path"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:174:32`

- [ ] **Line 175** (`reportCallIssue`)
  - **Issue**: No parameter named "class_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:175:32`

- [ ] **Line 188** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal[ConfigType.STATE_SCHEMA]" cannot be assigned to parameter "config_type" of type "ConfigType" in function "add_configuration"
      "Literal[ConfigType.STATE_SCHEMA]" is not assignable to "ConfigType"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:188:52`

- [ ] **Line 189** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_schema" for class "object"
      Attribute "state_schema" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:189:61`

- [ ] **Line 196** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal[ConfigType.INPUT_SCHEMA]" cannot be assigned to parameter "config_type" of type "ConfigType" in function "add_configuration"
      "Literal[ConfigType.INPUT_SCHEMA]" is not assignable to "ConfigType"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:196:52`

- [ ] **Line 197** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "input_schema" for class "object"
      Attribute "input_schema" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:197:61`

- [ ] **Line 204** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal[ConfigType.OUTPUT_SCHEMA]" cannot be assigned to parameter "config_type" of type "ConfigType" in function "add_configuration"
      "Literal[ConfigType.OUTPUT_SCHEMA]" is not assignable to "ConfigType"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:204:52`

- [ ] **Line 205** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "output_schema" for class "object"
      Attribute "output_schema" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:205:61`

- [ ] **Line 212** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal[ConfigType.ENGINE]" cannot be assigned to parameter "config_type" of type "ConfigType" in function "add_configuration"
      "Literal[ConfigType.ENGINE]" is not assignable to "ConfigType"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:212:52`

- [ ] **Line 213** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:213:61`

- [ ] **Line 225** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal[ImportStatus.SUCCESS]" cannot be assigned to parameter "status" of type "ImportStatus" in function "add_import_log"
      "Literal[ImportStatus.SUCCESS]" is not assignable to "ImportStatus"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:225:39`

- [ ] **Line 242** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal[ImportStatus.FAILURE]" cannot be assigned to parameter "status" of type "ImportStatus" in function "add_import_log"
      "Literal[ImportStatus.FAILURE]" is not assignable to "ImportStatus"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:242:39`

- [ ] **Line 370** (`reportCallIssue`)
  - **Issue**: No parameter named "module_path"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:370:32`

- [ ] **Line 371** (`reportCallIssue`)
  - **Issue**: No parameter named "class_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:371:32`

- [ ] **Line 382** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "var_name", "provider_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:382:32`

- [ ] **Line 383** (`reportCallIssue`)
  - **Issue**: No parameter named "registry_id"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:383:36`

- [ ] **Line 384** (`reportCallIssue`)
  - **Issue**: No parameter named "env_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:384:36`

- [ ] **Line 393** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal[ImportStatus.SUCCESS]" cannot be assigned to parameter "status" of type "ImportStatus" in function "add_import_log"
      "Literal[ImportStatus.SUCCESS]" is not assignable to "ImportStatus"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:393:39`

- [ ] **Line 410** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal[ImportStatus.FAILURE]" cannot be assigned to parameter "status" of type "ImportStatus" in function "add_import_log"
      "Literal[ImportStatus.FAILURE]" is not assignable to "ImportStatus"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:410:39`

- [ ] **Line 512** (`reportGeneralTypeIssues`)
  - **Issue**: "object" is not iterable
      "**iter**" method not defined
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:512:56`

- [ ] **Line 522** (`reportCallIssue`)
  - **Issue**: No parameter named "module_path"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:522:32`

- [ ] **Line 523** (`reportCallIssue`)
  - **Issue**: No parameter named "class_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:523:32`

- [ ] **Line 543** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "var_name", "provider_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:543:40`

- [ ] **Line 544** (`reportCallIssue`)
  - **Issue**: No parameter named "registry_id"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:544:44`

- [ ] **Line 545** (`reportCallIssue`)
  - **Issue**: No parameter named "env_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:545:44`

- [ ] **Line 554** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal[ImportStatus.SUCCESS]" cannot be assigned to parameter "status" of type "ImportStatus" in function "add_import_log"
      "Literal[ImportStatus.SUCCESS]" is not assignable to "ImportStatus"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:554:39`

- [ ] **Line 571** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal[ImportStatus.FAILURE]" cannot be assigned to parameter "status" of type "ImportStatus" in function "add_import_log"
      "Literal[ImportStatus.FAILURE]" is not assignable to "ImportStatus"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:571:39`

- [ ] **Line 693** (`reportCallIssue`)
  - **Issue**: No parameter named "module_path"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:693:32`

- [ ] **Line 694** (`reportCallIssue`)
  - **Issue**: No parameter named "class_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:694:32`

- [ ] **Line 716** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "var_name", "provider_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:716:44`

- [ ] **Line 717** (`reportCallIssue`)
  - **Issue**: No parameter named "registry_id"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:717:48`

- [ ] **Line 718** (`reportCallIssue`)
  - **Issue**: No parameter named "env_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:718:48`

- [ ] **Line 724** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "var_name", "provider_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:724:40`

- [ ] **Line 725** (`reportCallIssue`)
  - **Issue**: No parameter named "registry_id"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:725:44`

- [ ] **Line 726** (`reportCallIssue`)
  - **Issue**: No parameter named "env_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:726:44`

- [ ] **Line 735** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal[ImportStatus.SUCCESS]" cannot be assigned to parameter "status" of type "ImportStatus" in function "add_import_log"
      "Literal[ImportStatus.SUCCESS]" is not assignable to "ImportStatus"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:735:39`

- [ ] **Line 752** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal[ImportStatus.FAILURE]" cannot be assigned to parameter "status" of type "ImportStatus" in function "add_import_log"
      "Literal[ImportStatus.FAILURE]" is not assignable to "ImportStatus"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:752:39`

- [ ] **Line 826** (`reportCallIssue`)
  - **Issue**: No parameter named "module_path"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:826:32`

- [ ] **Line 827** (`reportCallIssue`)
  - **Issue**: No parameter named "class_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:827:32`

- [ ] **Line 836** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal[ImportStatus.SUCCESS]" cannot be assigned to parameter "status" of type "ImportStatus" in function "add_import_log"
      "Literal[ImportStatus.SUCCESS]" is not assignable to "ImportStatus"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:836:39`

- [ ] **Line 853** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal[ImportStatus.FAILURE]" cannot be assigned to parameter "status" of type "ImportStatus" in function "add_import_log"
      "Literal[ImportStatus.FAILURE]" is not assignable to "ImportStatus"
  - **Location**: `haive-dataflow/src/haive/dataflow/discovery.py:853:39`

### 📄 haive-dataflow/src/haive/dataflow/fetchers/lite_llm_import.py

- [ ] **Line 146** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal[EntityType.LLM_PROVIDER]" cannot be assigned to parameter "entity_type" of type "EntityType" in function "register_entity"
      "Literal[EntityType.LLM_PROVIDER]" is not assignable to "EntityType"
  - **Location**: `haive-dataflow/src/haive/dataflow/fetchers/lite_llm_import.py:146:32`

- [ ] **Line 157** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "var_name", "provider_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/fetchers/lite_llm_import.py:157:20`

- [ ] **Line 158** (`reportCallIssue`)
  - **Issue**: No parameter named "registry_id"
  - **Location**: `haive-dataflow/src/haive/dataflow/fetchers/lite_llm_import.py:158:24`

- [ ] **Line 158** (`reportCallIssue`)
  - **Issue**: No parameter named "env_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/fetchers/lite_llm_import.py:158:49`

- [ ] **Line 168** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal[ImportStatus.SUCCESS]" cannot be assigned to parameter "status" of type "ImportStatus" in function "add_import_log"
      "Literal[ImportStatus.SUCCESS]" is not assignable to "ImportStatus"
  - **Location**: `haive-dataflow/src/haive/dataflow/fetchers/lite_llm_import.py:168:27`

- [ ] **Line 186** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal[ImportStatus.FAILURE]" cannot be assigned to parameter "status" of type "ImportStatus" in function "add_import_log"
      "Literal[ImportStatus.FAILURE]" is not assignable to "ImportStatus"
  - **Location**: `haive-dataflow/src/haive/dataflow/fetchers/lite_llm_import.py:186:27`

- [ ] **Line 463** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal[ImportStatus.SUCCESS]" cannot be assigned to parameter "status" of type "ImportStatus" in function "add_import_log"
      "Literal[ImportStatus.SUCCESS]" is not assignable to "ImportStatus"
  - **Location**: `haive-dataflow/src/haive/dataflow/fetchers/lite_llm_import.py:463:31`

- [ ] **Line 479** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal[ImportStatus.FAILURE]" cannot be assigned to parameter "status" of type "ImportStatus" in function "add_import_log"
      "Literal[ImportStatus.FAILURE]" is not assignable to "ImportStatus"
  - **Location**: `haive-dataflow/src/haive/dataflow/fetchers/lite_llm_import.py:479:31`

- [ ] **Line 608** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "LLM" for class "type[EntityType]"
      Attribute "LLM" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/fetchers/lite_llm_import.py:608:47`

- [ ] **Line 635** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal[DependencyType.REQUIRES]" cannot be assigned to parameter "dependency_type" of type "DependencyType" in function "add_dependency"
      "Literal[DependencyType.REQUIRES]" is not assignable to "DependencyType"
  - **Location**: `haive-dataflow/src/haive/dataflow/fetchers/lite_llm_import.py:635:44`

- [ ] **Line 643** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal[ImportStatus.SUCCESS]" cannot be assigned to parameter "status" of type "ImportStatus" in function "add_import_log"
      "Literal[ImportStatus.SUCCESS]" is not assignable to "ImportStatus"
  - **Location**: `haive-dataflow/src/haive/dataflow/fetchers/lite_llm_import.py:643:31`

- [ ] **Line 659** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal[ImportStatus.FAILURE]" cannot be assigned to parameter "status" of type "ImportStatus" in function "add_import_log"
      "Literal[ImportStatus.FAILURE]" is not assignable to "ImportStatus"
  - **Location**: `haive-dataflow/src/haive/dataflow/fetchers/lite_llm_import.py:659:31`

### 📄 haive-dataflow/src/haive/dataflow/game_agent.py

- [ ] **Line 14** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.engine.agent.persistence.memory_config" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/game_agent.py:14:5`

- [ ] **Line 17** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.engine.agent.persistence.postgres_config" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/game_agent.py:17:5`

- [ ] **Line 345** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "initialize" for class "type[BaseModel]"
      Attribute "initialize" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/game_agent.py:345:51`

- [ ] **Line 347** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "initialize" for class "type[BaseModel]"
      Attribute "initialize" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/game_agent.py:347:52`

- [ ] **Line 347** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "model_dump" for class "object"
      Attribute "model_dump" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/game_agent.py:347:65`

- [ ] **Line 372** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "initialize" for class "type[BaseModel]"
      Attribute "initialize" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/game_agent.py:372:47`

- [ ] **Line 372** (`reportOptionalMemberAccess`)
  - **Issue**: "initialize" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/game_agent.py:372:47`

### 📄 haive-dataflow/src/haive/dataflow/importers/litellm_importer.py

- [ ] **Line 449** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "x" of type "ConvertibleToInt" in function "**new**"
      Type "str | None" is not assignable to type "ConvertibleToInt"
        Type "None" is not assignable to type "ConvertibleToInt"
          "None" is not assignable to "str"
          "None" is incompatible with protocol "Buffer"
            "**buffer**" is not present
          "None" is incompatible with protocol "SupportsInt"
            "**int**" is not present
          "None" is incompatible with protocol "SupportsIndex"
    ...
  - **Location**: `haive-dataflow/src/haive/dataflow/importers/litellm_importer.py:449:37`

- [ ] **Line 449** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "x" of type "ConvertibleToInt" in function "**new**"
      Type "str | None" is not assignable to type "ConvertibleToInt"
        Type "None" is not assignable to type "ConvertibleToInt"
          "None" is not assignable to "str"
          "None" is incompatible with protocol "Buffer"
            "**buffer**" is not present
          "None" is incompatible with protocol "SupportsInt"
            "**int**" is not present
          "None" is incompatible with protocol "SupportsIndex"
  - **Location**: `haive-dataflow/src/haive/dataflow/importers/litellm_importer.py:449:37`

### 📄 haive-dataflow/src/haive/dataflow/internal_websockets/handlers.py

- [ ] **Line 12** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.internal_websockets.auth.credits" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/internal_websockets/handlers.py:12:5`

- [ ] **Line 13** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.internal_websockets.config.settings" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/internal_websockets/handlers.py:13:5`

- [ ] **Line 14** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.internal_websockets.internal_websockets.manager" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/internal_websockets/handlers.py:14:5`

- [ ] **Line 17** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.internal_websockets.persistence.conversations" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/internal_websockets/handlers.py:17:5`

- [ ] **Line 21** (`reportAttributeAccessIssue`)
  - **Issue**: "AgentRegistry" is unknown import symbol
  - **Location**: `haive-dataflow/src/haive/dataflow/internal_websockets/handlers.py:21:36`

- [ ] **Line 25** (`reportMissingImports`)
  - **Issue**: Import "dataflow.registry" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/internal_websockets/handlers.py:25:9`

- [ ] **Line 131** (`reportGeneralTypeIssues`)
  - **Issue**: "Never" is not iterable
  - **Location**: `haive-dataflow/src/haive/dataflow/internal_websockets/handlers.py:131:29`

- [ ] **Line 141** (`reportGeneralTypeIssues`)
  - **Issue**: "Never" is not awaitable
  - **Location**: `haive-dataflow/src/haive/dataflow/internal_websockets/handlers.py:141:36`

### 📄 haive-dataflow/src/haive/dataflow/internal_websockets/manager.py

- [ ] **Line 8** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.internal_websockets.auth.supabase" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/internal_websockets/manager.py:8:5`

- [ ] **Line 9** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.internal_websockets.config.environment" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/internal_websockets/manager.py:9:5`

### 📄 haive-dataflow/src/haive/dataflow/llms/api.py

- [ ] **Line 17** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.llms.api.llms.models" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/llms/api.py:17:5`

### 📄 haive-dataflow/src/haive/dataflow/mcp/client.py

- [ ] **Line 310** (`reportArgumentType`)
  - **Issue**: Argument of type "list[str]" cannot be assigned to parameter "value" of type "str" in function "**setitem**"
      "list[str]" is not assignable to "str"
  - **Location**: `haive-dataflow/src/haive/dataflow/mcp/client.py:310:20`

- [ ] **Line 315** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, str]" cannot be assigned to parameter "value" of type "str" in function "**setitem**"
      "dict[str, str]" is not assignable to "str"
  - **Location**: `haive-dataflow/src/haive/dataflow/mcp/client.py:315:12`

- [ ] **Line 335** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "schema" for class "dict[Any, Any]"
      Attribute "schema" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/mcp/client.py:335:57`

- [ ] **Line 394** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "schema" for class "dict[Any, Any]"
      Attribute "schema" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/mcp/client.py:394:61`

### 📄 haive-dataflow/src/haive/dataflow/mcp/discovery.py

- [ ] **Line 474** (`reportCallIssue`)
  - **Issue**: No parameter named "config"
  - **Location**: `haive-dataflow/src/haive/dataflow/mcp/discovery.py:474:12`

- [ ] **Line 475** (`reportCallIssue`)
  - **Issue**: No parameter named "tags"
  - **Location**: `haive-dataflow/src/haive/dataflow/mcp/discovery.py:475:12`

### 📄 haive-dataflow/src/haive/dataflow/mcp/health.py

- [ ] **Line 129** (`reportGeneralTypeIssues`)
  - **Issue**: Expected class but received "(iterable: Iterable[object], /) -> bool"
  - **Location**: `haive-dataflow/src/haive/dataflow/mcp/health.py:129:52`

### 📄 haive-dataflow/src/haive/dataflow/persistence/conversations.py

- [ ] **Line 51** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.persistence.config.environment" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/persistence/conversations.py:51:5`

- [ ] **Line 52** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.persistence.persistence.supabase_adapter" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/persistence/conversations.py:52:5`

- [ ] **Line 159** (`reportGeneralTypeIssues`)
  - **Issue**: "APIResponse[_TableT]" is not awaitable
      "APIResponse[_TableT]" is incompatible with protocol "Awaitable[_T_co@Awaitable]"
        "**await**" is not present
  - **Location**: `haive-dataflow/src/haive/dataflow/persistence/conversations.py:159:22`

- [ ] **Line 197** (`reportGeneralTypeIssues`)
  - **Issue**: "APIResponse[_TableT]" is not awaitable
      "APIResponse[_TableT]" is incompatible with protocol "Awaitable[_T_co@Awaitable]"
        "**await**" is not present
  - **Location**: `haive-dataflow/src/haive/dataflow/persistence/conversations.py:197:22`

- [ ] **Line 230** (`reportGeneralTypeIssues`)
  - **Issue**: "APIResponse[_TableT]" is not awaitable
      "APIResponse[_TableT]" is incompatible with protocol "Awaitable[_T_co@Awaitable]"
        "**await**" is not present
  - **Location**: `haive-dataflow/src/haive/dataflow/persistence/conversations.py:230:22`

- [ ] **Line 272** (`reportCallIssue`)
  - **Issue**: No parameter named "options"
  - **Location**: `haive-dataflow/src/haive/dataflow/persistence/conversations.py:272:37`

### 📄 haive-dataflow/src/haive/dataflow/persistence/supabase_adapter.py

- [ ] **Line 58** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.persistence.persistence.factory" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/persistence/supabase_adapter.py:58:5`

- [ ] **Line 140** (`reportArgumentType`)
  - **Issue**: Argument of type "str" cannot be assigned to parameter "db_pass" of type "SecretStr" in function "**init**"
      "str" is not assignable to "SecretStr"
  - **Location**: `haive-dataflow/src/haive/dataflow/persistence/supabase_adapter.py:140:20`

### 📄 haive-dataflow/src/haive/dataflow/providers/agent_provider.py

- [ ] **Line 14** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.providers.providers.base" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:14:5`

- [ ] **Line 15** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.providers.utils.logging" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:15:5`

- [ ] **Line 111** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "name" for class "object"
      Attribute "name" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:111:45`

- [ ] **Line 123** (`reportCallIssue`)
  - **Issue**: No parameter named "module_path"
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:123:36`

- [ ] **Line 124** (`reportCallIssue`)
  - **Issue**: No parameter named "class_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:124:36`

- [ ] **Line 138** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_schema" for class "object"
      Attribute "state_schema" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:138:65`

- [ ] **Line 146** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "input_schema" for class "object"
      Attribute "input_schema" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:146:65`

- [ ] **Line 154** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "output_schema" for class "object"
      Attribute "output_schema" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:154:65`

- [ ] **Line 160** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:160:60`

- [ ] **Line 161** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:161:67`

- [ ] **Line 166** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:166:60`

- [ ] **Line 176** (`reportCallIssue`)
  - **Issue**: No parameter named "module_path"
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:176:44`

- [ ] **Line 177** (`reportCallIssue`)
  - **Issue**: No parameter named "class_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:177:44`

- [ ] **Line 177** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:177:64`

- [ ] **Line 195** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:195:65`

- [ ] **Line 203** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:203:57`

- [ ] **Line 207** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "PROMPT_TEMPLATE" for class "type[EntityType]"
      Attribute "PROMPT_TEMPLATE" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:207:75`

- [ ] **Line 209** (`reportCallIssue`)
  - **Issue**: No parameter named "module_path"
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:209:52`

- [ ] **Line 210** (`reportCallIssue`)
  - **Issue**: No parameter named "class_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:210:52`

- [ ] **Line 210** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:210:72`

- [ ] **Line 228** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:228:73`

- [ ] **Line 233** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:233:57`

- [ ] **Line 238** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "STATE_SCHEMA" for class "type[EntityType]"
      Attribute "STATE_SCHEMA" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:238:75`

- [ ] **Line 240** (`reportCallIssue`)
  - **Issue**: No parameter named "module_path"
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:240:52`

- [ ] **Line 241** (`reportCallIssue`)
  - **Issue**: No parameter named "class_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:241:52`

- [ ] **Line 241** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:241:72`

- [ ] **Line 259** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:259:73`

- [ ] **Line 264** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:264:65`

- [ ] **Line 265** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:265:61`

- [ ] **Line 270** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:270:61`

- [ ] **Line 288** (`reportCallIssue`)
  - **Issue**: No parameter named "module_path"
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:288:56`

- [ ] **Line 289** (`reportCallIssue`)
  - **Issue**: No parameter named "class_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:289:56`

- [ ] **Line 309** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "TOOLS" for class "type[ConfigType]"
      Attribute "TOOLS" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:309:75`

- [ ] **Line 310** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:310:73`

- [ ] **Line 316** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engines" for class "object"
      Attribute "engines" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:316:53`

- [ ] **Line 321** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engines" for class "object"
      Attribute "engines" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:321:54`

- [ ] **Line 327** (`reportCallIssue`)
  - **Issue**: No parameter named "module_path"
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:327:48`

- [ ] **Line 328** (`reportCallIssue`)
  - **Issue**: No parameter named "class_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:328:48`

- [ ] **Line 346** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "PERSISTENCE" for class "type[ConfigType]"
      Attribute "PERSISTENCE" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:346:67`

- [ ] **Line 347** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "persistence" for class "object"
      Attribute "persistence" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:347:65`

- [ ] **Line 353** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "agent_settings" for class "object"
      Attribute "agent_settings" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:353:53`

- [ ] **Line 358** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "agent_settings" for class "object"
      Attribute "agent_settings" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:358:54`

- [ ] **Line 359** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "update_entity" for class "RegistrySystem"
      Attribute "update_entity" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/agent_provider.py:359:60`

### 📄 haive-dataflow/src/haive/dataflow/providers/base.py

- [ ] **Line 18** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.providers.utils.logging" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/base.py:18:5`

- [ ] **Line 80** (`reportCallIssue`)
  - **Issue**: No overloads for "dirname" match the provided arguments
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/base.py:80:27`

- [ ] **Line 80** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "p" of type "AnyOrLiteralStr@dirname" in function "dirname"
      Type "str | None" is not assignable to constrained type variable "AnyOrLiteralStr"
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/base.py:80:43`

- [ ] **Line 126** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "var_name", "provider_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/base.py:126:12`

- [ ] **Line 127** (`reportCallIssue`)
  - **Issue**: No parameter named "registry_id"
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/base.py:127:16`

- [ ] **Line 127** (`reportCallIssue`)
  - **Issue**: No parameter named "env_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/base.py:127:41`

- [ ] **Line 143** (`reportArgumentType`)
  - **Issue**: Argument of type "DependencyType" cannot be assigned to parameter "dependency_type" of type "DependencyType" in function "add_dependency"
      "haive.dataflow.models.DependencyType" is not assignable to "haive.dataflow.core.DependencyType"
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/base.py:143:28`

- [ ] **Line 157** (`reportArgumentType`)
  - **Issue**: Argument of type "ConfigType" cannot be assigned to parameter "config_type" of type "ConfigType" in function "add_configuration"
      "haive.dataflow.models.ConfigType" is not assignable to "haive.dataflow.core.ConfigType"
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/base.py:157:49`

- [ ] **Line 181** (`reportArgumentType`)
  - **Issue**: Argument of type "ImportStatus" cannot be assigned to parameter "status" of type "ImportStatus" in function "add_import_log"
      "haive.dataflow.models.ImportStatus" is not assignable to "haive.dataflow.core.ImportStatus"
  - **Location**: `haive-dataflow/src/haive/dataflow/providers/base.py:181:19`

### 📄 haive-dataflow/src/haive/dataflow/registries/model_registry.py

- [ ] **Line 16** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.registries.db.supabase" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/registries/model_registry.py:16:5`

- [ ] **Line 737** (`reportArgumentType`)
  - **Issue**: Argument of type "Any | None" cannot be assigned to parameter "key" of type "str" in function "getenv"
      Type "Any | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-dataflow/src/haive/dataflow/registries/model_registry.py:737:25`

- [ ] **Line 814** (`reportArgumentType`)
  - **Issue**: Argument of type "Any | None" cannot be assigned to parameter "key" of type "str" in function "getenv"
      Type "Any | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-dataflow/src/haive/dataflow/registries/model_registry.py:814:25`

- [ ] **Line 1081** (`reportOptionalMemberAccess`)
  - **Issue**: "replace" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registries/model_registry.py:1081:60`

- [ ] **Line 1130** (`reportOptionalMemberAccess`)
  - **Issue**: "replace" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registries/model_registry.py:1130:29`

### 📄 haive-dataflow/src/haive/dataflow/registry.py

- [ ] **Line 14** (`reportMissingImports`)
  - **Issue**: Import "haive.api.api.db" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/registry.py:14:5`

- [ ] **Line 18** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.engine.agent.agent" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/registry.py:18:5`

- [ ] **Line 374** (`reportAttributeAccessIssue`)
  - **Issue**: "load_checkpointer_config" is unknown import symbol
  - **Location**: `haive-dataflow/src/haive/dataflow/registry.py:374:24`

### 📄 haive-dataflow/src/haive/dataflow/registry/base.py

- [ ] **Line 73** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "entries" for class "Registry[T@Registry]\*"
      Attribute "entries" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/base.py:73:26`

- [ ] **Line 75** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "\_disabled_discovery" for class "Registry[T@Registry]\*"
      Attribute "\_disabled_discovery" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/base.py:75:26`

- [ ] **Line 133** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "entries" for class "Registry[T@Registry]\*"
      Attribute "entries" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/base.py:133:17`

- [ ] **Line 189** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "\_disabled_discovery" for class "Registry[T@Registry]\*"
      Attribute "\_disabled_discovery" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/base.py:189:45`

- [ ] **Line 193** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "entries" for class "Registry[T@Registry]\*"
      Attribute "entries" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/base.py:193:20`

- [ ] **Line 242** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "entries" for class "Registry[T@Registry]\*"
      Attribute "entries" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/base.py:242:29`

- [ ] **Line 286** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "\_disabled_discovery" for class "Registry[T@Registry]\*"
      Attribute "\_disabled_discovery" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/base.py:286:45`

- [ ] **Line 290** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "entries" for class "Registry[T@Registry]\*"
      Attribute "entries" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/base.py:290:20`

- [ ] **Line 337** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "\_disabled_discovery" for class "Registry[T@Registry]\*"
      Attribute "\_disabled_discovery" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/base.py:337:45`

- [ ] **Line 346** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "entries" for class "Registry[T@Registry]\*"
      Attribute "entries" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/base.py:346:32`

- [ ] **Line 408** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "\_disabled_discovery" for class "Registry[T@Registry]\*"
      Attribute "\_disabled_discovery" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/base.py:408:16`

- [ ] **Line 502** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "entries" for class "Registry[T@Registry]\*"
      Attribute "entries" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/base.py:502:44`

### 📄 haive-dataflow/src/haive/dataflow/registry/bin/litellm_cli.py

- [ ] **Line 24** (`reportAttributeAccessIssue`)
  - **Issue**: "update_availability_status" is unknown import symbol
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/litellm_cli.py:24:4`

- [ ] **Line 28** (`reportAttributeAccessIssue`)
  - **Issue**: "generate_report" is unknown import symbol
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/litellm_cli.py:28:4`

- [ ] **Line 31** (`reportAttributeAccessIssue`)
  - **Issue**: "migrate_env_vars_to_vault" is unknown import symbol
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/litellm_cli.py:31:4`

### 📄 haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py

- [ ] **Line 74** (`reportOptionalMemberAccess`)
  - **Issue**: "print" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:74:16`

- [ ] **Line 82** (`reportOptionalMemberAccess`)
  - **Issue**: "print" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:82:16`

- [ ] **Line 83** (`reportOptionalMemberAccess`)
  - **Issue**: "print" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:83:16`

- [ ] **Line 91** (`reportOptionalMemberAccess`)
  - **Issue**: "print" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:91:16`

- [ ] **Line 92** (`reportOptionalMemberAccess`)
  - **Issue**: "print" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:92:16`

- [ ] **Line 112** (`reportOptionalMemberAccess`)
  - **Issue**: "print" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:112:16`

- [ ] **Line 290** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "name" for class "dict[str, Any]"
      Attribute "name" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:290:38`

- [ ] **Line 291** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "id" for class "dict[str, Any]"
      Attribute "id" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:291:38`

- [ ] **Line 292** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "module_path" for class "dict[str, Any]"
      Attribute "module_path" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:292:38`

- [ ] **Line 294** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "description" for class "dict[str, Any]"
      Attribute "description" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:294:42`

- [ ] **Line 295** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "description" for class "dict[str, Any]"
      Attribute "description" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:295:45`

- [ ] **Line 295** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "description" for class "dict[str, Any]"
      Attribute "description" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:295:71`

- [ ] **Line 296** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "description" for class "dict[str, Any]"
      Attribute "description" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:296:47`

- [ ] **Line 324** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "name" for class "dict[str, Any]"
      Attribute "name" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:324:37`

- [ ] **Line 325** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "id" for class "dict[str, Any]"
      Attribute "id" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:325:37`

- [ ] **Line 326** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "module_path" for class "dict[str, Any]"
      Attribute "module_path" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:326:37`

- [ ] **Line 328** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "description" for class "dict[str, Any]"
      Attribute "description" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:328:41`

- [ ] **Line 329** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "description" for class "dict[str, Any]"
      Attribute "description" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:329:44`

- [ ] **Line 329** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "description" for class "dict[str, Any]"
      Attribute "description" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:329:69`

- [ ] **Line 330** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "description" for class "dict[str, Any]"
      Attribute "description" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:330:46`

- [ ] **Line 358** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "metadata" for class "dict[str, Any]"
      Attribute "metadata" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:358:35`

- [ ] **Line 358** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "metadata" for class "dict[str, Any]"
      Attribute "metadata" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:358:67`

- [ ] **Line 359** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "metadata" for class "dict[str, Any]"
      Attribute "metadata" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:359:44`

- [ ] **Line 364** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "name" for class "dict[str, Any]"
      Attribute "name" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:364:40`

- [ ] **Line 365** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "id" for class "dict[str, Any]"
      Attribute "id" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:365:40`

- [ ] **Line 368** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "description" for class "dict[str, Any]"
      Attribute "description" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:368:44`

- [ ] **Line 369** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "description" for class "dict[str, Any]"
      Attribute "description" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:369:47`

- [ ] **Line 370** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "description" for class "dict[str, Any]"
      Attribute "description" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:370:52`

- [ ] **Line 371** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "description" for class "dict[str, Any]"
      Attribute "description" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:371:49`

- [ ] **Line 401** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "metadata" for class "dict[str, Any]"
      Attribute "metadata" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:401:35`

- [ ] **Line 402** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "metadata" for class "dict[str, Any]"
      Attribute "metadata" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:402:38`

- [ ] **Line 406** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "metadata" for class "dict[str, Any]"
      Attribute "metadata" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:406:35`

- [ ] **Line 406** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "metadata" for class "dict[str, Any]"
      Attribute "metadata" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:406:71`

- [ ] **Line 411** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "name" for class "dict[str, Any]"
      Attribute "name" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:411:39`

- [ ] **Line 412** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "id" for class "dict[str, Any]"
      Attribute "id" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:412:39`

- [ ] **Line 416** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "description" for class "dict[str, Any]"
      Attribute "description" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:416:43`

- [ ] **Line 417** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "description" for class "dict[str, Any]"
      Attribute "description" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:417:46`

- [ ] **Line 418** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "description" for class "dict[str, Any]"
      Attribute "description" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:418:51`

- [ ] **Line 419** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "description" for class "dict[str, Any]"
      Attribute "description" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:419:48`

- [ ] **Line 449** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "name" for class "dict[str, Any]"
      Attribute "name" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:449:37`

- [ ] **Line 450** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "id" for class "dict[str, Any]"
      Attribute "id" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:450:37`

- [ ] **Line 451** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "module_path" for class "dict[str, Any]"
      Attribute "module_path" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:451:37`

- [ ] **Line 453** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "description" for class "dict[str, Any]"
      Attribute "description" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:453:41`

- [ ] **Line 454** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "description" for class "dict[str, Any]"
      Attribute "description" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:454:44`

- [ ] **Line 454** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "description" for class "dict[str, Any]"
      Attribute "description" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:454:69`

- [ ] **Line 455** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "description" for class "dict[str, Any]"
      Attribute "description" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:455:46`

- [ ] **Line 489** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get_registry_stats" for class "RegistrySystem"
      Attribute "get_registry_stats" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:489:32`

- [ ] **Line 548** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "list_entities" for class "RegistrySystem"
      Attribute "list_entities" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:548:39`

- [ ] **Line 550** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "list_entities" for class "RegistrySystem"
      Attribute "list_entities" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:550:39`

- [ ] **Line 614** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get_entity_details" for class "RegistrySystem"
      Attribute "get_entity_details" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:614:34`

- [ ] **Line 627** (`reportOptionalMemberAccess`)
  - **Issue**: "print" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:627:20`

- [ ] **Line 641** (`reportOptionalMemberAccess`)
  - **Issue**: "print" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:641:24`

- [ ] **Line 759** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "list_entities" for class "RegistrySystem"
      Attribute "list_entities" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:759:39`

- [ ] **Line 761** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "list_entities" for class "RegistrySystem"
      Attribute "list_entities" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:761:39`

- [ ] **Line 824** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "clear_registry" for class "RegistrySystem"
      Attribute "clear_registry" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/registry_cli.py:824:34`

### 📄 haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py

- [ ] **Line 60** (`reportArgumentType`)
  - **Issue**: Argument of type "ModuleSpec | None" cannot be assigned to parameter "spec" of type "ModuleSpec" in function "module_from_spec"
      Type "ModuleSpec | None" is not assignable to type "ModuleSpec"
        "None" is not assignable to "ModuleSpec"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py:60:49`

- [ ] **Line 61** (`reportOptionalMemberAccess`)
  - **Issue**: "loader" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py:61:13`

- [ ] **Line 61** (`reportOptionalMemberAccess`)
  - **Issue**: "exec_module" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py:61:20`

- [ ] **Line 86** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py:86:51`

- [ ] **Line 87** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py:87:58`

- [ ] **Line 137** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py:137:47`

- [ ] **Line 138** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py:138:73`

- [ ] **Line 154** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py:154:61`

- [ ] **Line 157** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py:157:36`

- [ ] **Line 183** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "execute_sql" for class "ModuleType"
      Attribute "execute_sql" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py:183:33`

- [ ] **Line 184** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "ensure_vault_reference_column" for class "ModuleType"
      Attribute "ensure_vault_reference_column" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py:184:33`

- [ ] **Line 213** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "execute_sql" for class "ModuleType"
      Attribute "execute_sql" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py:213:36`

- [ ] **Line 256** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "execute_sql" for class "ModuleType"
      Attribute "execute_sql" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py:256:34`

- [ ] **Line 329** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py:329:54`

- [ ] **Line 332** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py:332:79`

- [ ] **Line 358** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py:358:54`

- [ ] **Line 362** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py:362:78`

- [ ] **Line 565** (`reportOptionalMemberAccess`)
  - **Issue**: "exec_module" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/bin/vault_cli.py:565:24`

### 📄 haive-dataflow/src/haive/dataflow/registry/core.py

- [ ] **Line 163** (`reportRedeclaration`)
  - **Issue**: Method declaration "\_ensure_registry_schema" is obscured by a declaration of the same name
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/core.py:163:8`

- [ ] **Line 169** (`reportOptionalMemberAccess`)
  - **Issue**: "rpc" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/core.py:169:42`

- [ ] **Line 178** (`reportOptionalMemberAccess`)
  - **Issue**: "rpc" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/core.py:178:31`

- [ ] **Line 250** (`reportOptionalMemberAccess`)
  - **Issue**: "rpc" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/core.py:250:45`

- [ ] **Line 259** (`reportOptionalMemberAccess`)
  - **Issue**: "rpc" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/core.py:259:35`

- [ ] **Line 276** (`reportOptionalMemberAccess`)
  - **Issue**: "rpc" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/core.py:276:41`

- [ ] **Line 287** (`reportArgumentType`)
  - **Issue**: Argument of type "SyncClient | None" cannot be assigned to parameter "client" of type "SyncClient" in function "table"
      Type "SyncClient | None" is not assignable to type "SyncClient"
        "None" is not assignable to "SyncClient"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/core.py:287:26`

- [ ] **Line 317** (`reportArgumentType`)
  - **Issue**: Argument of type "SyncClient | None" cannot be assigned to parameter "client" of type "SyncClient" in function "table"
      Type "SyncClient | None" is not assignable to type "SyncClient"
        "None" is not assignable to "SyncClient"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/core.py:317:30`

- [ ] **Line 572** (`reportArgumentType`)
  - **Issue**: Argument of type "SyncClient | None" cannot be assigned to parameter "client" of type "SyncClient" in function "table"
      Type "SyncClient | None" is not assignable to type "SyncClient"
        "None" is not assignable to "SyncClient"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/core.py:572:22`

- [ ] **Line 591** (`reportArgumentType`)
  - **Issue**: Argument of type "SyncClient | None" cannot be assigned to parameter "client" of type "SyncClient" in function "table"
      Type "SyncClient | None" is not assignable to type "SyncClient"
        "None" is not assignable to "SyncClient"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/core.py:591:22`

- [ ] **Line 606** (`reportOptionalMemberAccess`)
  - **Issue**: "rpc" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/core.py:606:42`

- [ ] **Line 636** (`reportArgumentType`)
  - **Issue**: Argument of type "SyncClient | None" cannot be assigned to parameter "client" of type "SyncClient" in function "table"
      Type "SyncClient | None" is not assignable to type "SyncClient"
        "None" is not assignable to "SyncClient"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/core.py:636:22`

- [ ] **Line 655** (`reportArgumentType`)
  - **Issue**: Argument of type "SyncClient | None" cannot be assigned to parameter "client" of type "SyncClient" in function "table"
      Type "SyncClient | None" is not assignable to type "SyncClient"
        "None" is not assignable to "SyncClient"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/core.py:655:22`

- [ ] **Line 670** (`reportOptionalMemberAccess`)
  - **Issue**: "rpc" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/core.py:670:42`

- [ ] **Line 738** (`reportMissingImports`)
  - **Issue**: Import "dataflow.serialization" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/core.py:738:25`

- [ ] **Line 1046** (`reportOptionalMemberAccess`)
  - **Issue**: "rpc" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/core.py:1046:42`

- [ ] **Line 1055** (`reportOptionalMemberAccess`)
  - **Issue**: "rpc" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/core.py:1055:31`

- [ ] **Line 1128** (`reportOptionalMemberAccess`)
  - **Issue**: "rpc" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/core.py:1128:49`

- [ ] **Line 1137** (`reportOptionalMemberAccess`)
  - **Issue**: "rpc" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/core.py:1137:39`

- [ ] **Line 1209** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "code" for class "Exception"
      Attribute "code" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/core.py:1209:49`

- [ ] **Line 1597** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['llm', 'llm_provider', 'embedding', 'embedding_provider', 'agent', 'tool', 'workflow', 'data_source', 'custom']" cannot be assigned to parameter "entity_type" of type "EntityType" in function "get_entities_by_type"
      Type "Literal['llm', 'llm_provider', 'embedding', 'embedding_provider', 'agent', 'tool', 'workflow', 'data_source', 'custom']" is not assignable to type "EntityType"
        "Literal['agent']" is not assignable to "EntityType"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/core.py:1597:50`

### 📄 haive-dataflow/src/haive/dataflow/registry/db.py

- [ ] **Line 149** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['exact']" cannot be assigned to parameter "count" of type "CountMethod | None" in function "select"
      Type "Literal['exact']" is not assignable to type "CountMethod | None"
        "Literal['exact']" is not assignable to "CountMethod"
        "Literal['exact']" is not assignable to "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/db.py:149:38`

- [ ] **Line 182** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['exact']" cannot be assigned to parameter "count" of type "CountMethod | None" in function "select"
      Type "Literal['exact']" is not assignable to type "CountMethod | None"
        "Literal['exact']" is not assignable to "CountMethod"
        "Literal['exact']" is not assignable to "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/db.py:182:38`

- [ ] **Line 208** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['exact']" cannot be assigned to parameter "count" of type "CountMethod | None" in function "select"
      Type "Literal['exact']" is not assignable to type "CountMethod | None"
        "Literal['exact']" is not assignable to "CountMethod"
        "Literal['exact']" is not assignable to "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/db.py:208:38`

### 📄 haive-dataflow/src/haive/dataflow/registry/discovery.py

- [ ] **Line 102** (`reportCallIssue`)
  - **Issue**: No overloads for "dirname" match the provided arguments
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:102:23`

- [ ] **Line 102** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "p" of type "AnyOrLiteralStr@dirname" in function "dirname"
      Type "str | None" is not assignable to constrained type variable "AnyOrLiteralStr"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:102:39`

- [ ] **Line 205** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "name" for class "object"
      Attribute "name" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:205:41`

- [ ] **Line 209** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "register_entity" for class "LazyRegistrySystem"
      Attribute "register_entity" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:209:55`

- [ ] **Line 229** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_configuration" for class "LazyRegistrySystem"
      Attribute "add_configuration" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:229:52`

- [ ] **Line 232** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_schema" for class "object"
      Attribute "state_schema" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:232:61`

- [ ] **Line 237** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_configuration" for class "LazyRegistrySystem"
      Attribute "add_configuration" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:237:52`

- [ ] **Line 240** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "input_schema" for class "object"
      Attribute "input_schema" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:240:61`

- [ ] **Line 245** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_configuration" for class "LazyRegistrySystem"
      Attribute "add_configuration" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:245:52`

- [ ] **Line 248** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "output_schema" for class "object"
      Attribute "output_schema" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:248:61`

- [ ] **Line 253** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_configuration" for class "LazyRegistrySystem"
      Attribute "add_configuration" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:253:52`

- [ ] **Line 256** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:256:61`

- [ ] **Line 264** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_import_log" for class "LazyRegistrySystem"
      Attribute "add_import_log" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:264:44`

- [ ] **Line 281** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_import_log" for class "LazyRegistrySystem"
      Attribute "add_import_log" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:281:44`

- [ ] **Line 409** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "register_entity" for class "LazyRegistrySystem"
      Attribute "register_entity" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:409:54`

- [ ] **Line 425** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_environment_var" for class "LazyRegistrySystem"
      Attribute "add_environment_var" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:425:48`

- [ ] **Line 432** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_import_log" for class "LazyRegistrySystem"
      Attribute "add_import_log" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:432:44`

- [ ] **Line 449** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_import_log" for class "LazyRegistrySystem"
      Attribute "add_import_log" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:449:44`

- [ ] **Line 555** (`reportGeneralTypeIssues`)
  - **Issue**: "object" is not iterable
      "**iter**" method not defined
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:555:56`

- [ ] **Line 561** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "register_entity" for class "LazyRegistrySystem"
      Attribute "register_entity" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:561:57`

- [ ] **Line 586** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_environment_var" for class "LazyRegistrySystem"
      Attribute "add_environment_var" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:586:56`

- [ ] **Line 593** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_import_log" for class "LazyRegistrySystem"
      Attribute "add_import_log" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:593:44`

- [ ] **Line 610** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_import_log" for class "LazyRegistrySystem"
      Attribute "add_import_log" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:610:44`

- [ ] **Line 732** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "register_entity" for class "LazyRegistrySystem"
      Attribute "register_entity" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:732:56`

- [ ] **Line 759** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_environment_var" for class "LazyRegistrySystem"
      Attribute "add_environment_var" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:759:60`

- [ ] **Line 767** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_environment_var" for class "LazyRegistrySystem"
      Attribute "add_environment_var" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:767:56`

- [ ] **Line 774** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_import_log" for class "LazyRegistrySystem"
      Attribute "add_import_log" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:774:44`

- [ ] **Line 791** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_import_log" for class "LazyRegistrySystem"
      Attribute "add_import_log" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:791:44`

- [ ] **Line 865** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "register_entity" for class "LazyRegistrySystem"
      Attribute "register_entity" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:865:54`

- [ ] **Line 875** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_import_log" for class "LazyRegistrySystem"
      Attribute "add_import_log" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:875:44`

- [ ] **Line 892** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_import_log" for class "LazyRegistrySystem"
      Attribute "add_import_log" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:892:44`

- [ ] **Line 969** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "register_entity" for class "LazyRegistrySystem"
      Attribute "register_entity" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:969:48`

- [ ] **Line 975** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "config" for class "RegistryItem"
      Attribute "config" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:975:36`

- [ ] **Line 976** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "tags" for class "RegistryItem"
      Attribute "tags" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/discovery.py:976:34`

### 📄 haive-dataflow/src/haive/dataflow/registry/importers/embeddings_importer.py

- [ ] **Line 13** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.registry.db.supabase" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/importers/embeddings_importer.py:13:5`

- [ ] **Line 14** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.registry.importers.registry.core" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/importers/embeddings_importer.py:14:5`

- [ ] **Line 20** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.registry.importers.registry.serialization" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/importers/embeddings_importer.py:20:5`

### 📄 haive-dataflow/src/haive/dataflow/registry/importers/litellm_importer.py

- [ ] **Line 492** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "x" of type "ConvertibleToInt" in function "**new**"
      Type "str | None" is not assignable to type "ConvertibleToInt"
        Type "None" is not assignable to type "ConvertibleToInt"
          "None" is not assignable to "str"
          "None" is incompatible with protocol "Buffer"
            "**buffer**" is not present
          "None" is incompatible with protocol "SupportsInt"
            "**int**" is not present
          "None" is incompatible with protocol "SupportsIndex"
    ...
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/importers/litellm_importer.py:492:37`

- [ ] **Line 492** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "x" of type "ConvertibleToInt" in function "**new**"
      Type "str | None" is not assignable to type "ConvertibleToInt"
        Type "None" is not assignable to type "ConvertibleToInt"
          "None" is not assignable to "str"
          "None" is incompatible with protocol "Buffer"
            "**buffer**" is not present
          "None" is incompatible with protocol "SupportsInt"
            "**int**" is not present
          "None" is incompatible with protocol "SupportsIndex"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/importers/litellm_importer.py:492:37`

### 📄 haive-dataflow/src/haive/dataflow/registry/lazy_core.py

- [ ] **Line 15** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.registry.registry.models" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/lazy_core.py:15:5`

### 📄 haive-dataflow/src/haive/dataflow/registry/main.py

- [ ] **Line 5** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.registry.registry.core" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/main.py:5:5`

- [ ] **Line 6** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.registry.registry.models" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/main.py:6:5`

- [ ] **Line 7** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.registry.registry.providers.agent_provider" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/main.py:7:5`

### 📄 haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py

- [ ] **Line 14** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.registry.providers.providers.base" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:14:5`

- [ ] **Line 15** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.registry.providers.utils.logging" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:15:5`

- [ ] **Line 111** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "name" for class "object"
      Attribute "name" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:111:45`

- [ ] **Line 123** (`reportCallIssue`)
  - **Issue**: No parameter named "module_path"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:123:36`

- [ ] **Line 124** (`reportCallIssue`)
  - **Issue**: No parameter named "class_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:124:36`

- [ ] **Line 138** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_schema" for class "object"
      Attribute "state_schema" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:138:65`

- [ ] **Line 146** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "input_schema" for class "object"
      Attribute "input_schema" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:146:65`

- [ ] **Line 154** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "output_schema" for class "object"
      Attribute "output_schema" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:154:65`

- [ ] **Line 160** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:160:60`

- [ ] **Line 161** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:161:67`

- [ ] **Line 166** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:166:60`

- [ ] **Line 176** (`reportCallIssue`)
  - **Issue**: No parameter named "module_path"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:176:44`

- [ ] **Line 177** (`reportCallIssue`)
  - **Issue**: No parameter named "class_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:177:44`

- [ ] **Line 177** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:177:64`

- [ ] **Line 195** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:195:65`

- [ ] **Line 203** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:203:57`

- [ ] **Line 207** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "PROMPT_TEMPLATE" for class "type[EntityType]"
      Attribute "PROMPT_TEMPLATE" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:207:75`

- [ ] **Line 209** (`reportCallIssue`)
  - **Issue**: No parameter named "module_path"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:209:52`

- [ ] **Line 210** (`reportCallIssue`)
  - **Issue**: No parameter named "class_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:210:52`

- [ ] **Line 210** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:210:72`

- [ ] **Line 228** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:228:73`

- [ ] **Line 233** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:233:57`

- [ ] **Line 238** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "STATE_SCHEMA" for class "type[EntityType]"
      Attribute "STATE_SCHEMA" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:238:75`

- [ ] **Line 240** (`reportCallIssue`)
  - **Issue**: No parameter named "module_path"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:240:52`

- [ ] **Line 241** (`reportCallIssue`)
  - **Issue**: No parameter named "class_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:241:52`

- [ ] **Line 241** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:241:72`

- [ ] **Line 259** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:259:73`

- [ ] **Line 264** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:264:65`

- [ ] **Line 265** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:265:61`

- [ ] **Line 270** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:270:61`

- [ ] **Line 288** (`reportCallIssue`)
  - **Issue**: No parameter named "module_path"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:288:56`

- [ ] **Line 289** (`reportCallIssue`)
  - **Issue**: No parameter named "class_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:289:56`

- [ ] **Line 309** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "TOOLS" for class "type[ConfigType]"
      Attribute "TOOLS" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:309:75`

- [ ] **Line 310** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engine" for class "object"
      Attribute "engine" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:310:73`

- [ ] **Line 316** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engines" for class "object"
      Attribute "engines" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:316:53`

- [ ] **Line 321** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "engines" for class "object"
      Attribute "engines" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:321:54`

- [ ] **Line 327** (`reportCallIssue`)
  - **Issue**: No parameter named "module_path"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:327:48`

- [ ] **Line 328** (`reportCallIssue`)
  - **Issue**: No parameter named "class_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:328:48`

- [ ] **Line 346** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "PERSISTENCE" for class "type[ConfigType]"
      Attribute "PERSISTENCE" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:346:67`

- [ ] **Line 347** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "persistence" for class "object"
      Attribute "persistence" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:347:65`

- [ ] **Line 353** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "agent_settings" for class "object"
      Attribute "agent_settings" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:353:53`

- [ ] **Line 358** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "agent_settings" for class "object"
      Attribute "agent_settings" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:358:54`

- [ ] **Line 359** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "update_entity" for class "RegistrySystem"
      Attribute "update_entity" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/agent_provider.py:359:60`

### 📄 haive-dataflow/src/haive/dataflow/registry/providers/base.py

- [ ] **Line 46** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.registry.providers.utils.logging" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/base.py:46:5`

- [ ] **Line 151** (`reportCallIssue`)
  - **Issue**: No overloads for "dirname" match the provided arguments
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/base.py:151:27`

- [ ] **Line 151** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "p" of type "AnyOrLiteralStr@dirname" in function "dirname"
      Type "str | None" is not assignable to constrained type variable "AnyOrLiteralStr"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/base.py:151:43`

- [ ] **Line 197** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "var_name", "provider_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/base.py:197:12`

- [ ] **Line 198** (`reportCallIssue`)
  - **Issue**: No parameter named "registry_id"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/base.py:198:16`

- [ ] **Line 198** (`reportCallIssue`)
  - **Issue**: No parameter named "env_name"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/base.py:198:41`

- [ ] **Line 214** (`reportArgumentType`)
  - **Issue**: Argument of type "DependencyType" cannot be assigned to parameter "dependency_type" of type "DependencyType" in function "add_dependency"
      "haive.dataflow.models.DependencyType" is not assignable to "haive.dataflow.core.DependencyType"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/base.py:214:28`

- [ ] **Line 228** (`reportArgumentType`)
  - **Issue**: Argument of type "ConfigType" cannot be assigned to parameter "config_type" of type "ConfigType" in function "add_configuration"
      "haive.dataflow.models.ConfigType" is not assignable to "haive.dataflow.core.ConfigType"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/base.py:228:49`

- [ ] **Line 252** (`reportArgumentType`)
  - **Issue**: Argument of type "ImportStatus" cannot be assigned to parameter "status" of type "ImportStatus" in function "add_import_log"
      "haive.dataflow.models.ImportStatus" is not assignable to "haive.dataflow.core.ImportStatus"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/providers/base.py:252:19`

### 📄 haive-dataflow/src/haive/dataflow/registry/registries/model_registry.py

- [ ] **Line 16** (`reportMissingImports`)
  - **Issue**: Import "haive.dataflow.registry.registries.db.supabase" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/registries/model_registry.py:16:5`

- [ ] **Line 737** (`reportArgumentType`)
  - **Issue**: Argument of type "Any | None" cannot be assigned to parameter "key" of type "str" in function "getenv"
      Type "Any | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/registries/model_registry.py:737:25`

- [ ] **Line 814** (`reportArgumentType`)
  - **Issue**: Argument of type "Any | None" cannot be assigned to parameter "key" of type "str" in function "getenv"
      Type "Any | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/registries/model_registry.py:814:25`

- [ ] **Line 1081** (`reportOptionalMemberAccess`)
  - **Issue**: "replace" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/registries/model_registry.py:1081:60`

- [ ] **Line 1130** (`reportOptionalMemberAccess`)
  - **Issue**: "replace" is not a known attribute of "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/registries/model_registry.py:1130:29`

### 📄 haive-dataflow/src/haive/dataflow/registry/serialization.py

- [ ] **Line 414** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "**validators**" for class "type[BaseModel]"
      Attribute "**validators**" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/serialization.py:414:40`

- [ ] **Line 419** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "Config" for class "type[BaseModel]"
      Attribute "Config" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/serialization.py:419:29`

- [ ] **Line 421** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "Config" for class "type[BaseModel]"
      Attribute "Config" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/serialization.py:421:49`

- [ ] **Line 443** (`reportReturnType`)
  - **Issue**: Type "dict[str, Any | bool]" is not assignable to return type "type[BaseModel] | None"
      Type "dict[str, Any | bool]" is not assignable to type "type[BaseModel] | None"
        Type "dict[str, Any | bool]" is not assignable to type "type[BaseModel]"
        "dict[str, Any | bool]" is not assignable to "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/serialization.py:443:15`

### 📄 haive-dataflow/src/haive/dataflow/registry/utils/logging.py

- [ ] **Line 178** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, Any]" cannot be assigned to parameter "value" of type "str" in function "**setitem**"
      "dict[str, Any]" is not assignable to "str"
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/utils/logging.py:178:8`

### 📄 haive-dataflow/src/haive/dataflow/registry/utils/vault_migration_script.py

- [ ] **Line 42** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/utils/vault_migration_script.py:42:51`

- [ ] **Line 43** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/utils/vault_migration_script.py:43:58`

- [ ] **Line 91** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/utils/vault_migration_script.py:91:47`

- [ ] **Line 92** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/utils/vault_migration_script.py:92:73`

- [ ] **Line 108** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/utils/vault_migration_script.py:108:61`

- [ ] **Line 111** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/utils/vault_migration_script.py:111:36`

- [ ] **Line 689** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/utils/vault_migration_script.py:689:47`

- [ ] **Line 691** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/utils/vault_migration_script.py:691:70`

- [ ] **Line 719** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/utils/vault_migration_script.py:719:47`

- [ ] **Line 721** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/registry/utils/vault_migration_script.py:721:78`

### 📄 haive-dataflow/src/haive/dataflow/router.py

- [ ] **Line 83** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "arun" for class "tuple[Unknown | None, str | None]"
      Attribute "arun" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/router.py:83:28`

- [ ] **Line 109** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "app" for class "tuple[Unknown | None, str | None]"
      Attribute "app" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/router.py:109:26`

- [ ] **Line 141** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "astream" for class "tuple[Unknown | None, str | None]"
      Attribute "astream" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/router.py:141:45`

- [ ] **Line 158** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "arun" for class "tuple[Unknown | None, str | None]"
      Attribute "arun" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/router.py:158:33`

- [ ] **Line 186** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_schema" for class "tuple[Unknown | None, str | None]"
      Attribute "state_schema" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/router.py:186:18`

- [ ] **Line 188** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_schema" for class "tuple[Unknown | None, str | None]"
      Attribute "state_schema" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/router.py:188:47`

- [ ] **Line 198** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_schema" for class "tuple[Unknown | None, str | None]"
      Attribute "state_schema" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/router.py:198:38`

- [ ] **Line 199** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_schema" for class "tuple[Unknown | None, str | None]"
      Attribute "state_schema" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/router.py:199:39`

- [ ] **Line 249** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "list_agents_by_type" for class "AgentRegistryService"
      Attribute "list_agents_by_type" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/router.py:249:36`

### 📄 haive-dataflow/src/haive/dataflow/serialization.py

- [ ] **Line 333** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "**validators**" for class "type[BaseModel]"
      Attribute "**validators**" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/serialization.py:333:40`

- [ ] **Line 338** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "Config" for class "type[BaseModel]"
      Attribute "Config" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/serialization.py:338:29`

- [ ] **Line 340** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "Config" for class "type[BaseModel]"
      Attribute "Config" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/serialization.py:340:49`

- [ ] **Line 362** (`reportReturnType`)
  - **Issue**: Type "dict[str, Any | bool]" is not assignable to return type "type[BaseModel] | None"
      Type "dict[str, Any | bool]" is not assignable to type "type[BaseModel] | None"
        Type "dict[str, Any | bool]" is not assignable to type "type[BaseModel]"
        "dict[str, Any | bool]" is not assignable to "None"
  - **Location**: `haive-dataflow/src/haive/dataflow/serialization.py:362:15`

### 📄 haive-dataflow/src/haive/dataflow/tic_tac_toe_api.py

- [ ] **Line 10** (`reportMissingImports`)
  - **Issue**: Import "haive_games.tic_tac_toe.agent" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/tic_tac_toe_api.py:10:5`

- [ ] **Line 11** (`reportMissingImports`)
  - **Issue**: Import "haive_games.tic_tac_toe.config" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/tic_tac_toe_api.py:11:5`

- [ ] **Line 12** (`reportMissingImports`)
  - **Issue**: Import "haive_games.tic_tac_toe.state" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/tic_tac_toe_api.py:12:5`

- [ ] **Line 13** (`reportMissingImports`)
  - **Issue**: Import "haive_games.tic_tac_toe.state_manager" could not be resolved
  - **Location**: `haive-dataflow/src/haive/dataflow/tic_tac_toe_api.py:13:5`

- [ ] **Line 176** (`reportAttributeAccessIssue`)
  - **Issue**: "WindowsSelectorEventLoopPolicy" is not a known attribute of module "asyncio"
  - **Location**: `haive-dataflow/src/haive/dataflow/tic_tac_toe_api.py:176:50`

### 📄 haive-dataflow/src/haive/dataflow/utils/logging.py

- [ ] **Line 178** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, Any]" cannot be assigned to parameter "value" of type "str" in function "**setitem**"
      "dict[str, Any]" is not assignable to "str"
  - **Location**: `haive-dataflow/src/haive/dataflow/utils/logging.py:178:8`

### 📄 haive-dataflow/src/haive/dataflow/utils/vault_migration_script.py

- [ ] **Line 42** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/utils/vault_migration_script.py:42:51`

- [ ] **Line 43** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/utils/vault_migration_script.py:43:58`

- [ ] **Line 91** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/utils/vault_migration_script.py:91:47`

- [ ] **Line 92** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/utils/vault_migration_script.py:92:73`

- [ ] **Line 108** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/utils/vault_migration_script.py:108:61`

- [ ] **Line 111** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/utils/vault_migration_script.py:111:36`

- [ ] **Line 689** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/utils/vault_migration_script.py:689:47`

- [ ] **Line 691** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/utils/vault_migration_script.py:691:70`

- [ ] **Line 719** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/utils/vault_migration_script.py:719:47`

- [ ] **Line 721** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "error" for class "SingleAPIResponse[Any]"
      Attribute "error" is unknown
  - **Location**: `haive-dataflow/src/haive/dataflow/utils/vault_migration_script.py:721:78`

## Fix Priority Guidelines

### High Priority (Fix First)

1. `reportAttributeAccessIssue` - Missing/unknown attributes
2. `reportArgumentType` - Type mismatches in function calls
3. `reportOptionalMemberAccess` - Accessing potentially None objects

### Medium Priority

4. `reportTypedDictNotRequiredAccess` - Unsafe TypedDict access
5. `reportCallIssue` - Function call problems
6. `reportOptionalSubscript` - Subscripting None objects

### Low Priority (Polish)

7. `reportUnusedImport` - Cleanup unused imports
8. `reportUnnecessaryTypeIgnore` - Remove unnecessary ignores

## Testing After Fixes

```bash
# Test imports still work
poetry run python -c "from haive.dataflow import *; print('✅ Imports OK')"

# Re-run pyright to verify fixes
poetry run pyright packages/haive-dataflow/src/ --level error

# Run any existing tests
poetry run pytest packages/haive-dataflow/tests/ -v
```

---

**Generated**: 2025-08-02  
**Source**: `project_docs/build-reports/pyright-issues/haive-dataflow-*.json`
