# HAIVE-GAMES - Pyright Issues Checklist

**Total Errors**: 1460
**Total Warnings**: 0
**Priority**: 📋 Standard

## Summary by Issue Type

### Error Categories

- **reportAttributeAccessIssue**: 561 issues
- **reportCallIssue**: 185 issues
- **reportArgumentType**: 182 issues
- **reportOptionalMemberAccess**: 147 issues
- **reportUndefinedVariable**: 140 issues
- **reportMissingImports**: 75 issues
- **reportGeneralTypeIssues**: 30 issues
- **reportReturnType**: 26 issues
- **reportInvalidTypeForm**: 23 issues
- **reportIndexIssue**: 20 issues
- **reportAbstractUsage**: 19 issues
- **reportOperatorIssue**: 17 issues
- **reportInvalidTypeArguments**: 11 issues
- **reportOptionalSubscript**: 8 issues
- **reportAssignmentType**: 6 issues
- **reportRedeclaration**: 4 issues
- **reportTypedDictNotRequiredAccess**: 2 issues
- **reportOptionalOperand**: 2 issues
- **reportUnboundVariable**: 1 issues
- **reportOptionalIterable**: 1 issues

## 🚨 ERRORS (Must Fix)

### 📄 haive-games/src/haive/games/among_us/agent.py

- [ ] **Line 134** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "\_get_task_completion_percentage" for class "AmongUsAgent\*"
      Attribute "\_get_task_completion_percentage" is unknown
  - **Location**: `haive-games/src/haive/games/among_us/agent.py:134:25`

- [ ] **Line 243** (`reportOperatorIssue`)
  - **Issue**: Operator "+=" not supported for types "str | Any | Unbound" and "str"
      Operator "+" not supported for types "Unbound" and "str"
  - **Location**: `haive-games/src/haive/games/among_us/agent.py:243:8`

- [ ] **Line 269** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "map_locations" for class "MultiPlayerGameConfig"
      Attribute "map_locations" is unknown
  - **Location**: `haive-games/src/haive/games/among_us/agent.py:269:44`

- [ ] **Line 281** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player_names" for class "MultiPlayerGameConfig"
      Attribute "player_names" is unknown
  - **Location**: `haive-games/src/haive/games/among_us/agent.py:281:42`

- [ ] **Line 293** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player_names" for class "MultiPlayerGameConfig"
      Attribute "player_names" is unknown
  - **Location**: `haive-games/src/haive/games/among_us/agent.py:293:42`

### 📄 haive-games/src/haive/games/among_us/config.py

- [ ] **Line 37** (`reportAssignmentType`)
  - **Issue**: Type "None" is not assignable to declared type "int"
      "None" is not assignable to "int"
  - **Location**: `haive-games/src/haive/games/among_us/config.py:37:25`

### 📄 haive-games/src/haive/games/among_us/configurable_config.py

- [ ] **Line 12** (`reportAttributeAccessIssue`)
  - **Issue**: "AmongUsConfig" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/among_us/configurable_config.py:12:40`

### 📄 haive-games/src/haive/games/among_us/demo.py

- [ ] **Line 64** (`reportArgumentType`)
  - **Issue**: Expression of type "None" cannot be assigned to parameter of type "str"
      "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/among_us/demo.py:64:21`

- [ ] **Line 65** (`reportArgumentType`)
  - **Issue**: Expression of type "None" cannot be assigned to parameter of type "str"
      "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/among_us/demo.py:65:21`

- [ ] **Line 195** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "ui" for class "Agent[Unknown]"
      Attribute "ui" is unknown
  - **Location**: `haive-games/src/haive/games/among_us/demo.py:195:14`

- [ ] **Line 210** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "initialize" for class "Agent[Unknown]"
      Attribute "initialize" is unknown
  - **Location**: `haive-games/src/haive/games/among_us/demo.py:210:22`

- [ ] **Line 216** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "visualize_state" for class "Agent[Unknown]"
      Attribute "visualize_state" is unknown
  - **Location**: `haive-games/src/haive/games/among_us/demo.py:216:14`

- [ ] **Line 302** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "display_game_over_panel" for class "EnhancedAmongUsUI"
      Attribute "display_game_over_panel" is unknown
  - **Location**: `haive-games/src/haive/games/among_us/demo.py:302:11`

- [ ] **Line 305** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "visualize_state" for class "Agent[Unknown]"
      Attribute "visualize_state" is unknown
  - **Location**: `haive-games/src/haive/games/among_us/demo.py:305:14`

- [ ] **Line 308** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "winner" for class "AmongUsState"
      Attribute "winner" is unknown
  - **Location**: `haive-games/src/haive/games/among_us/demo.py:308:17`

- [ ] **Line 1200** (`reportUndefinedVariable`)
  - **Issue**: "Progress" is not defined
  - **Location**: `haive-games/src/haive/games/among_us/demo.py:1200:17`

- [ ] **Line 1201** (`reportUndefinedVariable`)
  - **Issue**: "SpinnerColumn" is not defined
  - **Location**: `haive-games/src/haive/games/among_us/demo.py:1201:16`

- [ ] **Line 1202** (`reportUndefinedVariable`)
  - **Issue**: "TextColumn" is not defined
  - **Location**: `haive-games/src/haive/games/among_us/demo.py:1202:16`

### 📄 haive-games/src/haive/games/among_us/generic_engines.py

- [ ] **Line 134** (`reportAbstractUsage`)
  - **Issue**: Cannot instantiate abstract class "AmongUsPromptGenerator"
      "GenericPromptGenerator.create_analysis_prompt" is not implemented
      "GenericPromptGenerator.get_move_output_model" is not implemented
      and 1 more...
  - **Location**: `haive-games/src/haive/games/among_us/generic_engines.py:134:27`

- [ ] **Line 134** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "players"
  - **Location**: `haive-games/src/haive/games/among_us/generic_engines.py:134:27`

- [ ] **Line 167** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "create_engines" for class "AmongUsEngineFactory"
      Attribute "create_engines" is unknown
  - **Location**: `haive-games/src/haive/games/among_us/generic_engines.py:167:28`

### 📄 haive-games/src/haive/games/among_us/state_manager.py

- [ ] **Line 1212** (`reportArgumentType`)
  - **Issue**: Argument of type "Any | None" cannot be assigned to parameter "type" of type "str" in function "**init**"
      Type "Any | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/among_us/state_manager.py:1212:21`

- [ ] **Line 1229** (`reportArgumentType`)
  - **Issue**: Argument of type "Any | None" cannot be assigned to parameter "type" of type "str" in function "**init**"
      Type "Any | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/among_us/state_manager.py:1229:17`

- [ ] **Line 1230** (`reportArgumentType`)
  - **Issue**: Argument of type "Any | None" cannot be assigned to parameter "location" of type "str" in function "**init**"
      Type "Any | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/among_us/state_manager.py:1230:21`

- [ ] **Line 1239** (`reportOptionalMemberAccess`)
  - **Issue**: "upper" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/among_us/state_manager.py:1239:50`

- [ ] **Line 1396** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "vent_id" of type "str" in function "get_vent"
      Type "str | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/among_us/state_manager.py:1396:42`

- [ ] **Line 1762** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "winner" for class "AmongUsState"
      Attribute "winner" is unknown
  - **Location**: `haive-games/src/haive/games/among_us/state_manager.py:1762:18`

### 📄 haive-games/src/haive/games/among_us/ui.py

- [ ] **Line 129** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PlayerState"
  - **Location**: `haive-games/src/haive/games/among_us/ui.py:129:29`

- [ ] **Line 133** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PlayerState"
  - **Location**: `haive-games/src/haive/games/among_us/ui.py:133:28`

- [ ] **Line 145** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PlayerState"
  - **Location**: `haive-games/src/haive/games/among_us/ui.py:145:29`

- [ ] **Line 149** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PlayerState"
  - **Location**: `haive-games/src/haive/games/among_us/ui.py:149:11`

- [ ] **Line 153** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PlayerState"
  - **Location**: `haive-games/src/haive/games/among_us/ui.py:153:19`

- [ ] **Line 180** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PlayerState"
  - **Location**: `haive-games/src/haive/games/among_us/ui.py:180:20`

- [ ] **Line 191** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PlayerState"
  - **Location**: `haive-games/src/haive/games/among_us/ui.py:191:36`

- [ ] **Line 201** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PlayerState"
  - **Location**: `haive-games/src/haive/games/among_us/ui.py:201:44`

- [ ] **Line 209** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PlayerState"
  - **Location**: `haive-games/src/haive/games/among_us/ui.py:209:23`

- [ ] **Line 216** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PlayerState"
  - **Location**: `haive-games/src/haive/games/among_us/ui.py:216:11`

- [ ] **Line 218** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PlayerState"
  - **Location**: `haive-games/src/haive/games/among_us/ui.py:218:39`

- [ ] **Line 302** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PlayerState"
  - **Location**: `haive-games/src/haive/games/among_us/ui.py:302:20`

- [ ] **Line 304** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PlayerState"
  - **Location**: `haive-games/src/haive/games/among_us/ui.py:304:23`

- [ ] **Line 331** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PlayerState"
  - **Location**: `haive-games/src/haive/games/among_us/ui.py:331:20`

- [ ] **Line 350** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PlayerState"
  - **Location**: `haive-games/src/haive/games/among_us/ui.py:350:102`

- [ ] **Line 400** (`reportCallIssue`)
  - **Issue**: No parameter named "size"
  - **Location**: `haive-games/src/haive/games/among_us/ui.py:400:60`

- [ ] **Line 421** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PlayerState"
  - **Location**: `haive-games/src/haive/games/among_us/ui.py:421:19`

- [ ] **Line 430** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "PlayerState"
  - **Location**: `haive-games/src/haive/games/among_us/ui.py:430:32`

- [ ] **Line 665** (`reportArgumentType`)
  - **Issue**: Argument of type "float" cannot be assigned to parameter "completed" of type "int" in function "add_task"
      "float" is not assignable to "int"
  - **Location**: `haive-games/src/haive/games/among_us/ui.py:665:56`

- [ ] **Line 734** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "winner" for class "AmongUsState"
      Attribute "winner" is unknown
  - **Location**: `haive-games/src/haive/games/among_us/ui.py:734:25`

### 📄 haive-games/src/haive/games/api/general_api.py

- [ ] **Line 104** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "args" of type "StrPath" in function "**new**"
      Type "str | None" is not assignable to type "StrPath"
        Type "None" is not assignable to type "StrPath"
          "None" is not assignable to "str"
          "None" is incompatible with protocol "PathLike[str]"
            "**fspath**" is not present
  - **Location**: `haive-games/src/haive/games/api/general_api.py:104:30`

- [ ] **Line 104** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "args" of type "StrPath" in function "**init**"
      Type "str | None" is not assignable to type "StrPath"
        Type "None" is not assignable to type "StrPath"
          "None" is not assignable to "str"
          "None" is incompatible with protocol "PathLike[str]"
            "**fspath**" is not present
  - **Location**: `haive-games/src/haive/games/api/general_api.py:104:30`

- [ ] **Line 150** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get_config_class" for class "type[Agent[Unknown]]"
      Attribute "get_config_class" is unknown
  - **Location**: `haive-games/src/haive/games/api/general_api.py:150:39`

- [ ] **Line 329** (`reportOptionalMemberAccess`)
  - **Issue**: "default" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/api/general_api.py:329:40`

### 📄 haive-games/src/haive/games/api/setup.py

- [ ] **Line 58** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get_config_class" for class "type[Agent[Unknown]]"
      Attribute "get_config_class" is unknown
  - **Location**: `haive-games/src/haive/games/api/setup.py:58:31`

- [ ] **Line 126** (`reportUndefinedVariable`)
  - **Issue**: "ChessAgent" is not defined
  - **Location**: `haive-games/src/haive/games/api/setup.py:126:32`

### 📄 haive-games/src/haive/games/base/agent.py

- [ ] **Line 92** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/base/agent.py:92:19`

- [ ] **Line 93** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/base/agent.py:93:19`

- [ ] **Line 94** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/base/agent.py:94:19`

- [ ] **Line 97** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/base/agent.py:97:19`

- [ ] **Line 101** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/base/agent.py:101:23`

- [ ] **Line 102** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/base/agent.py:102:23`

- [ ] **Line 105** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/base/agent.py:105:23`

- [ ] **Line 106** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/base/agent.py:106:23`

- [ ] **Line 108** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/base/agent.py:108:23`

- [ ] **Line 114** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/base/agent.py:114:23`

- [ ] **Line 116** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/base/agent.py:116:23`

- [ ] **Line 123** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/base/agent.py:123:23`

- [ ] **Line 125** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/base/agent.py:125:23`

- [ ] **Line 131** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/base/agent.py:131:23`

- [ ] **Line 152** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "GameAgent[T@GameAgent]\*"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/base/agent.py:152:26`

- [ ] **Line 200** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "GameAgent[T@GameAgent]\*"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/base/agent.py:200:29`

- [ ] **Line 274** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "game_status" for class "BaseModel\*"
      Attribute "game_status" is unknown
  - **Location**: `haive-games/src/haive/games/base/agent.py:274:21`

- [ ] **Line 500** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "visualize_state" for class "GameAgent[Unknown]"
      Attribute "visualize_state" is unknown
  - **Location**: `haive-games/src/haive/games/base/agent.py:500:14`

### 📄 haive-games/src/haive/games/base/config.py

- [ ] **Line 50** (`reportAssignmentType`)
  - **Issue**: Type "GameState" is not assignable to declared type "type[GameState]"
      Type "GameState" is not assignable to type "type[GameState]"
  - **Location**: `haive-games/src/haive/games/base/config.py:50:36`

### 📄 haive-games/src/haive/games/base/factory.py

- [ ] **Line 138** (`reportCallIssue`)
  - **Issue**: No parameter named "state_schema"
  - **Location**: `haive-games/src/haive/games/base/factory.py:138:24`

- [ ] **Line 139** (`reportCallIssue`)
  - **Issue**: No parameter named "aug_llm_configs"
  - **Location**: `haive-games/src/haive/games/base/factory.py:139:24`

- [ ] **Line 140** (`reportCallIssue`)
  - **Issue**: No parameter named "enable_analysis"
  - **Location**: `haive-games/src/haive/games/base/factory.py:140:24`

- [ ] **Line 141** (`reportCallIssue`)
  - **Issue**: No parameter named "visualize"
  - **Location**: `haive-games/src/haive/games/base/factory.py:141:24`

- [ ] **Line 150** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, Any]" cannot be assigned to parameter "config" of type "GameConfig" in function "**init**"
      "dict[str, Any]" is not assignable to "GameConfig"
  - **Location**: `haive-games/src/haive/games/base/factory.py:150:37`

- [ ] **Line 191** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_conditional_edge" for class "DynamicGraph"
      Attribute "add_conditional_edge" is unknown
  - **Location**: `haive-games/src/haive/games/base/factory.py:191:30`

- [ ] **Line 199** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_conditional_edge" for class "DynamicGraph"
      Attribute "add_conditional_edge" is unknown
  - **Location**: `haive-games/src/haive/games/base/factory.py:199:30`

- [ ] **Line 209** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_conditional_edge" for class "DynamicGraph"
      Attribute "add_conditional_edge" is unknown
  - **Location**: `haive-games/src/haive/games/base/factory.py:209:30`

- [ ] **Line 215** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_conditional_edge" for class "DynamicGraph"
      Attribute "add_conditional_edge" is unknown
  - **Location**: `haive-games/src/haive/games/base/factory.py:215:30`

- [ ] **Line 229** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_conditional_edge" for class "DynamicGraph"
      Attribute "add_conditional_edge" is unknown
  - **Location**: `haive-games/src/haive/games/base/factory.py:229:34`

### 📄 haive-games/src/haive/games/base/utils.py

- [ ] **Line 23** (`reportUndefinedVariable`)
  - **Issue**: "GameAgent" is not defined
  - **Location**: `haive-games/src/haive/games/base/utils.py:23:21`

### 📄 haive-games/src/haive/games/battleship/agent.py

- [ ] **Line 310** (`reportRedeclaration`)
  - **Issue**: Method declaration "analyze_position" is obscured by a declaration of the same name
  - **Location**: `haive-games/src/haive/games/battleship/agent.py:310:8`

- [ ] **Line 355** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "analysis" for class "dict[Unknown, Unknown]"
      Attribute "analysis" is unknown
  - **Location**: `haive-games/src/haive/games/battleship/agent.py:355:34`

- [ ] **Line 741** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "analysis" for class "dict[Unknown, Unknown]"
      Attribute "analysis" is unknown
  - **Location**: `haive-games/src/haive/games/battleship/agent.py:741:34`

- [ ] **Line 967** (`reportReturnType`)
  - **Issue**: Type "Any | None" is not assignable to return type "dict[str, Any]"
      Type "Any | None" is not assignable to type "dict[str, Any]"
        "None" is not assignable to "dict[str, Any]"
  - **Location**: `haive-games/src/haive/games/battleship/agent.py:967:23`

### 📄 haive-games/src/haive/games/battleship/config.py

- [ ] **Line 210** (`reportTypedDictNotRequiredAccess`)
  - **Issue**: Could not access item in TypedDict
      "configurable" is not a required key in "RunnableConfig", so access may result in runtime exception
  - **Location**: `haive-games/src/haive/games/battleship/config.py:210:15`

- [ ] **Line 212** (`reportTypedDictNotRequiredAccess`)
  - **Issue**: Could not access item in TypedDict
      "configurable" is not a required key in "RunnableConfig", so access may result in runtime exception
  - **Location**: `haive-games/src/haive/games/battleship/config.py:212:12`

### 📄 haive-games/src/haive/games/battleship/engines.py

- [ ] **Line 37** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/battleship/engines.py:37:56`

### 📄 haive-games/src/haive/games/battleship/generic_engines.py

- [ ] **Line 103** (`reportAbstractUsage`)
  - **Issue**: Cannot instantiate abstract class "BattleshipPromptGenerator"
      "GenericPromptGenerator.create_analysis_prompt" is not implemented
      "GenericPromptGenerator.get_move_output_model" is not implemented
      and 1 more...
  - **Location**: `haive-games/src/haive/games/battleship/generic_engines.py:103:27`

- [ ] **Line 103** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "players"
  - **Location**: `haive-games/src/haive/games/battleship/generic_engines.py:103:27`

- [ ] **Line 136** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "create_engines" for class "BattleshipEngineFactory"
      Attribute "create_engines" is unknown
  - **Location**: `haive-games/src/haive/games/battleship/generic_engines.py:136:30`

### 📄 haive-games/src/haive/games/battleship/models.py

- [ ] **Line 1352** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "sunk_ship"
  - **Location**: `haive-games/src/haive/games/battleship/models.py:1352:23`

- [ ] **Line 1356** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "sunk_ship"
  - **Location**: `haive-games/src/haive/games/battleship/models.py:1356:23`

- [ ] **Line 1376** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "sunk_ship"
  - **Location**: `haive-games/src/haive/games/battleship/models.py:1376:27`

- [ ] **Line 1380** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "sunk_ship"
  - **Location**: `haive-games/src/haive/games/battleship/models.py:1380:15`

### 📄 haive-games/src/haive/games/battleship/state_manager.py

- [ ] **Line 239** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "winner" for class "BattleshipState"
      Type "str" is not assignable to type "Literal['player1', 'player2'] | None"
        "str" is not assignable to "None"
        "str" is not assignable to type "Literal['player1']"
        "str" is not assignable to type "Literal['player2']"
  - **Location**: `haive-games/src/haive/games/battleship/state_manager.py:239:31`

- [ ] **Line 242** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "current_player" for class "BattleshipState"
      Type "str" is not assignable to type "Literal['player1', 'player2']"
        "str" is not assignable to type "Literal['player1']"
        "str" is not assignable to type "Literal['player2']"
  - **Location**: `haive-games/src/haive/games/battleship/state_manager.py:242:39`

### 📄 haive-games/src/haive/games/benchmark.py

- [ ] **Line 16** (`reportMissingImports`)
  - **Issue**: Import "haive.games.monopoly.test" could not be resolved
  - **Location**: `haive-games/src/haive/games/benchmark.py:16:5`

- [ ] **Line 17** (`reportMissingImports`)
  - **Issue**: Import "haive.games.poker.test" could not be resolved
  - **Location**: `haive-games/src/haive/games/benchmark.py:17:5`

### 📄 haive-games/src/haive/games/cards/standard/blackjack/agent.py

- [ ] **Line 9** (`reportMissingImports`)
  - **Issue**: Import "haive.games.cards.blackjack.config" could not be resolved
  - **Location**: `haive-games/src/haive/games/cards/standard/blackjack/agent.py:9:5`

- [ ] **Line 10** (`reportMissingImports`)
  - **Issue**: Import "haive.games.cards.blackjack.models" could not be resolved
  - **Location**: `haive-games/src/haive/games/cards/standard/blackjack/agent.py:10:5`

- [ ] **Line 11** (`reportMissingImports`)
  - **Issue**: Import "haive.games.cards.blackjack.state_manager" could not be resolved
  - **Location**: `haive-games/src/haive/games/cards/standard/blackjack/agent.py:11:5`

- [ ] **Line 40** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "num_players" for class "GameConfig"
      Attribute "num_players" is unknown
  - **Location**: `haive-games/src/haive/games/cards/standard/blackjack/agent.py:40:36`

- [ ] **Line 197** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "max_rounds" for class "GameConfig"
      Attribute "max_rounds" is unknown
  - **Location**: `haive-games/src/haive/games/cards/standard/blackjack/agent.py:197:45`

### 📄 haive-games/src/haive/games/cards/standard/blackjack/config.py

- [ ] **Line 7** (`reportMissingImports`)
  - **Issue**: Import "haive.games.cards.blackjack.models" could not be resolved
  - **Location**: `haive-games/src/haive/games/cards/standard/blackjack/config.py:7:5`

- [ ] **Line 103** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, AugLLMConfig]" cannot be assigned to parameter "engines" of type "dict[str, Engine[Unknown, Unknown] | str]" in function "**init**"
      "dict[str, AugLLMConfig]" is not assignable to "dict[str, Engine[Unknown, Unknown] | str]"
        Type parameter "\_VT@dict" is invariant, but "AugLLMConfig" is not the same as "Engine[Unknown, Unknown] | str"
        Consider switching from "dict" to "Mapping" which is covariant in the value type
  - **Location**: `haive-games/src/haive/games/cards/standard/blackjack/config.py:103:20`

### 📄 haive-games/src/haive/games/cards/standard/blackjack/factory.py

- [ ] **Line 3** (`reportMissingImports`)
  - **Issue**: Import "haive.games.cards.blackjack.agent" could not be resolved
  - **Location**: `haive-games/src/haive/games/cards/standard/blackjack/factory.py:3:5`

- [ ] **Line 4** (`reportMissingImports`)
  - **Issue**: Import "haive.games.cards.blackjack.config" could not be resolved
  - **Location**: `haive-games/src/haive/games/cards/standard/blackjack/factory.py:4:5`

- [ ] **Line 5** (`reportMissingImports`)
  - **Issue**: Import "haive.games.cards.blackjack.models" could not be resolved
  - **Location**: `haive-games/src/haive/games/cards/standard/blackjack/factory.py:5:5`

### 📄 haive-games/src/haive/games/cards/standard/blackjack/state_manager.py

- [ ] **Line 4** (`reportMissingImports`)
  - **Issue**: Import "haive.games.cards.blackjack.models" could not be resolved
  - **Location**: `haive-games/src/haive/games/cards/standard/blackjack/state_manager.py:4:5`

### 📄 haive-games/src/haive/games/cards/standard/bs/agent.py

- [ ] **Line 10** (`reportMissingImports`)
  - **Issue**: Import "haive.games.cards.bs.config" could not be resolved
  - **Location**: `haive-games/src/haive/games/cards/standard/bs/agent.py:10:5`

- [ ] **Line 11** (`reportMissingImports`)
  - **Issue**: Import "haive.games.cards.bs.models" could not be resolved
  - **Location**: `haive-games/src/haive/games/cards/standard/bs/agent.py:11:5`

- [ ] **Line 12** (`reportMissingImports`)
  - **Issue**: Import "haive.games.cards.bs.state" could not be resolved
  - **Location**: `haive-games/src/haive/games/cards/standard/bs/agent.py:12:5`

- [ ] **Line 13** (`reportMissingImports`)
  - **Issue**: Import "haive.games.cards.bs.state_manager" could not be resolved
  - **Location**: `haive-games/src/haive/games/cards/standard/bs/agent.py:13:5`

- [ ] **Line 42** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "num_players" for class "GameConfig"
      Attribute "num_players" is unknown
  - **Location**: `haive-games/src/haive/games/cards/standard/bs/agent.py:42:36`

- [ ] **Line 176** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "max_rounds" for class "GameConfig"
      Attribute "max_rounds" is unknown
  - **Location**: `haive-games/src/haive/games/cards/standard/bs/agent.py:176:45`

- [ ] **Line 372** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "visualize_state" for class "Agent[Unknown]"
      Attribute "visualize_state" is unknown
  - **Location**: `haive-games/src/haive/games/cards/standard/bs/agent.py:372:22`

### 📄 haive-games/src/haive/games/cards/standard/bs/config.py

- [ ] **Line 8** (`reportAttributeAccessIssue`)
  - **Issue**: "Any" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/cards/standard/bs/config.py:8:4`

- [ ] **Line 104** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, AugLLMConfig]" cannot be assigned to parameter "engines" of type "dict[str, Engine[Unknown, Unknown] | str]" in function "**init**"
      "dict[str, AugLLMConfig]" is not assignable to "dict[str, Engine[Unknown, Unknown] | str]"
        Type parameter "\_VT@dict" is invariant, but "AugLLMConfig" is not the same as "Engine[Unknown, Unknown] | str"
        Consider switching from "dict" to "Mapping" which is covariant in the value type
  - **Location**: `haive-games/src/haive/games/cards/standard/bs/config.py:104:20`

### 📄 haive-games/src/haive/games/cards/standard/bs/models.py

- [ ] **Line 30** (`reportReturnType`)
  - **Issue**: Type "list[Self@Card]" is not assignable to return type "list[Card]"
      "list[Self@Card]" is not assignable to "list[Card]"
        Type parameter "\_T@list" is invariant, but "Self@Card" is not the same as "Card"
        Consider switching from "list" to "Sequence" which is covariant
  - **Location**: `haive-games/src/haive/games/cards/standard/bs/models.py:30:15`

### 📄 haive-games/src/haive/games/cards/standard/bs/state_manager.py

- [ ] **Line 4** (`reportMissingImports`)
  - **Issue**: Import "haive.games.cards.bs.models" could not be resolved
  - **Location**: `haive-games/src/haive/games/cards/standard/bs/state_manager.py:4:5`

- [ ] **Line 10** (`reportMissingImports`)
  - **Issue**: Import "haive.games.cards.bs.state" could not be resolved
  - **Location**: `haive-games/src/haive/games/cards/standard/bs/state_manager.py:10:5`

### 📄 haive-games/src/haive/games/cards/standard/poker/actions.py

- [ ] **Line 7** (`reportMissingImports`)
  - **Issue**: Import "haive.games.cards.card.components.actions" could not be resolved
  - **Location**: `haive-games/src/haive/games/cards/standard/poker/actions.py:7:5`

- [ ] **Line 8** (`reportMissingImports`)
  - **Issue**: Import "haive.games.cards.card.components.standard" could not be resolved
  - **Location**: `haive-games/src/haive/games/cards/standard/poker/actions.py:8:5`

### 📄 haive-games/src/haive/games/cards/standard/poker/scoring.py

- [ ] **Line 6** (`reportMissingImports`)
  - **Issue**: Import "haive.games.cards.card.components.scoring" could not be resolved
  - **Location**: `haive-games/src/haive/games/cards/standard/poker/scoring.py:6:5`

- [ ] **Line 7** (`reportMissingImports`)
  - **Issue**: Import "haive.games.cards.card.components.standard" could not be resolved
  - **Location**: `haive-games/src/haive/games/cards/standard/poker/scoring.py:7:5`

### 📄 haive-games/src/haive/games/cards/standard/poker/state.py

- [ ] **Line 8** (`reportMissingImports`)
  - **Issue**: Import "haive.games.cards.card.components.actions" could not be resolved
  - **Location**: `haive-games/src/haive/games/cards/standard/poker/state.py:8:5`

- [ ] **Line 9** (`reportMissingImports`)
  - **Issue**: Import "haive.games.cards.card.components.betting" could not be resolved
  - **Location**: `haive-games/src/haive/games/cards/standard/poker/state.py:9:5`

- [ ] **Line 10** (`reportMissingImports`)
  - **Issue**: Import "haive.games.cards.card.components.standard" could not be resolved
  - **Location**: `haive-games/src/haive/games/cards/standard/poker/state.py:10:5`

- [ ] **Line 11** (`reportMissingImports`)
  - **Issue**: Import "haive.games.cards.card.components.state" could not be resolved
  - **Location**: `haive-games/src/haive/games/cards/standard/poker/state.py:11:5`

- [ ] **Line 178** (`reportOptionalOperand`)
  - **Issue**: Operator "+" not supported for "None"
  - **Location**: `haive-games/src/haive/games/cards/standard/poker/state.py:178:19`

### 📄 haive-games/src/haive/games/checkers/agent.py

- [ ] **Line 82** (`reportArgumentType`)
  - **Issue**: Argument of type "CheckersAgentConfig" cannot be assigned to parameter "config" of type "GameConfig" in function "**init**"
      "CheckersAgentConfig" is not assignable to "GameConfig"
  - **Location**: `haive-games/src/haive/games/checkers/agent.py:82:25`

- [ ] **Line 328** (`reportReturnType`)
  - **Issue**: Type "None" is not assignable to return type "Command[Unknown]"
      "None" is not assignable to "Command[Unknown]"
  - **Location**: `haive-games/src/haive/games/checkers/agent.py:328:15`

- [ ] **Line 448** (`reportArgumentType`)
  - **Issue**: Argument of type "CheckersAnalysis" cannot be assigned to parameter "analysis" of type "dict[str, Any]" in function "update_analysis"
      "CheckersAnalysis" is not assignable to "dict[str, Any]"
  - **Location**: `haive-games/src/haive/games/checkers/agent.py:448:23`

- [ ] **Line 533** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, dict[str, Unknown]]" cannot be assigned to parameter "config" of type "RunnableConfig | None" in function "run"
      Type "dict[str, dict[str, Unknown]]" is not assignable to type "RunnableConfig | None"
        "dict[str, dict[str, Unknown]]" is not assignable to "RunnableConfig"
        "dict[str, dict[str, Unknown]]" is not assignable to "None"
  - **Location**: `haive-games/src/haive/games/checkers/agent.py:533:35`

### 📄 haive-games/src/haive/games/checkers/engines.py

- [ ] **Line 190** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/checkers/engines.py:190:56`

### 📄 haive-games/src/haive/games/checkers/example.py

- [ ] **Line 127** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_game" for class "Agent[Unknown]"
      Attribute "run_game" is unknown
  - **Location**: `haive-games/src/haive/games/checkers/example.py:127:23`

- [ ] **Line 184** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_game" for class "Agent[Unknown]"
      Attribute "run_game" is unknown
  - **Location**: `haive-games/src/haive/games/checkers/example.py:184:23`

- [ ] **Line 237** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_game" for class "Agent[Unknown]"
      Attribute "run_game" is unknown
  - **Location**: `haive-games/src/haive/games/checkers/example.py:237:31`

- [ ] **Line 296** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "initialize_game" for class "CheckersStateManager"
      Attribute "initialize_game" is unknown
  - **Location**: `haive-games/src/haive/games/checkers/example.py:296:34`

- [ ] **Line 312** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "make_move" for class "CheckersStateManager"
      Attribute "make_move" is unknown
  - **Location**: `haive-games/src/haive/games/checkers/example.py:312:42`

- [ ] **Line 331** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "analyze_position" for class "CheckersStateManager"
      Attribute "analyze_position" is unknown
  - **Location**: `haive-games/src/haive/games/checkers/example.py:331:37`

- [ ] **Line 355** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "validate_move" for class "CheckersStateManager"
      Attribute "validate_move" is unknown
  - **Location**: `haive-games/src/haive/games/checkers/example.py:355:22`

- [ ] **Line 409** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_game" for class "Agent[Unknown]"
      Attribute "run_game" is unknown
  - **Location**: `haive-games/src/haive/games/checkers/example.py:409:14`

- [ ] **Line 465** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_game" for class "Agent[Unknown]"
      Attribute "run_game" is unknown
  - **Location**: `haive-games/src/haive/games/checkers/example.py:465:31`

- [ ] **Line 536** (`reportOperatorIssue`)
  - **Issue**: Operator "in" not supported for types "str" and "Literal[0, 1, 2, 3, 4]"
      Operator "in" not supported for types "str" and "Literal[0]"
      Operator "in" not supported for types "str" and "Literal[1]"
      Operator "in" not supported for types "str" and "Literal[2]"
      Operator "in" not supported for types "str" and "Literal[3]"
      Operator "in" not supported for types "str" and "Literal[4]"
  - **Location**: `haive-games/src/haive/games/checkers/example.py:536:23`

- [ ] **Line 538** (`reportOperatorIssue`)
  - **Issue**: Operator "in" not supported for types "Literal['K']" and "Literal[0, 1, 2, 3, 4]"
      Operator "in" not supported for types "Literal['K']" and "Literal[0]"
      Operator "in" not supported for types "Literal['K']" and "Literal[1]"
      Operator "in" not supported for types "Literal['K']" and "Literal[2]"
      Operator "in" not supported for types "Literal['K']" and "Literal[3]"
      Operator "in" not supported for types "Literal['K']" and "Literal[4]"
  - **Location**: `haive-games/src/haive/games/checkers/example.py:538:33`

- [ ] **Line 541** (`reportOperatorIssue`)
  - **Issue**: Operator "in" not supported for types "Literal['K']" and "Literal[0, 1, 2, 3, 4]"
      Operator "in" not supported for types "Literal['K']" and "Literal[0]"
      Operator "in" not supported for types "Literal['K']" and "Literal[1]"
      Operator "in" not supported for types "Literal['K']" and "Literal[2]"
      Operator "in" not supported for types "Literal['K']" and "Literal[3]"
      Operator "in" not supported for types "Literal['K']" and "Literal[4]"
  - **Location**: `haive-games/src/haive/games/checkers/example.py:541:48`

- [ ] **Line 556** (`reportOperatorIssue`)
  - **Issue**: Operator "in" not supported for types "str" and "Literal[0, 1, 2, 3, 4]"
      Operator "in" not supported for types "str" and "Literal[0]"
      Operator "in" not supported for types "str" and "Literal[1]"
      Operator "in" not supported for types "str" and "Literal[2]"
      Operator "in" not supported for types "str" and "Literal[3]"
      Operator "in" not supported for types "str" and "Literal[4]"
  - **Location**: `haive-games/src/haive/games/checkers/example.py:556:23`

- [ ] **Line 574** (`reportReturnType`)
  - **Issue**: Type "None" is not assignable to return type "str"
      "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/checkers/example.py:574:23`

- [ ] **Line 585** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "make_move" for class "CheckersStateManager"
      Attribute "make_move" is unknown
  - **Location**: `haive-games/src/haive/games/checkers/example.py:585:46`

- [ ] **Line 615** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "initialize_game" for class "CheckersStateManager"
      Attribute "initialize_game" is unknown
  - **Location**: `haive-games/src/haive/games/checkers/example.py:615:31`

- [ ] **Line 627** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "make_move" for class "CheckersStateManager"
      Attribute "make_move" is unknown
  - **Location**: `haive-games/src/haive/games/checkers/example.py:627:39`

- [ ] **Line 632** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get_valid_moves" for class "CheckersStateManager"
      Attribute "get_valid_moves" is unknown
  - **Location**: `haive-games/src/haive/games/checkers/example.py:632:32`

- [ ] **Line 667** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_game" for class "Agent[Unknown]"
      Attribute "run_game" is unknown
  - **Location**: `haive-games/src/haive/games/checkers/example.py:667:14`

- [ ] **Line 671** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get_current_state" for class "Agent[Unknown]"
      Attribute "get_current_state" is unknown
  - **Location**: `haive-games/src/haive/games/checkers/example.py:671:18`

### 📄 haive-games/src/haive/games/checkers/generic_engines.py

- [ ] **Line 20** (`reportMissingImports`)
  - **Issue**: Import "haive.games.models.llm" could not be resolved
  - **Location**: `haive-games/src/haive/games/checkers/generic_engines.py:20:5`

- [ ] **Line 293** (`reportUndefinedVariable`)
  - **Issue**: "Any" is not defined
  - **Location**: `haive-games/src/haive/games/checkers/generic_engines.py:293:41`

### 📄 haive-games/src/haive/games/checkers/state.py

- [ ] **Line 224** (`reportAssignmentType`)
  - **Issue**: Type "list[list[int]]" is not assignable to declared type "list[list[Literal[0, 1, 2, 3, 4]]]"
      "list[list[int]]" is not assignable to "list[list[Literal[0, 1, 2, 3, 4]]]"
        Type parameter "\_T@list" is invariant, but "list[int]" is not the same as "list[Literal[0, 1, 2, 3, 4]]"
        Consider switching from "list" to "Sequence" which is covariant
  - **Location**: `haive-games/src/haive/games/checkers/state.py:224:48`

- [ ] **Line 713** (`reportArgumentType`)
  - **Issue**: Argument of type "list[list[int]]" cannot be assigned to parameter "board" of type "list[list[Literal[0, 1, 2, 3, 4]]]" in function "**init**"
      "list[list[int]]" is not assignable to "list[list[Literal[0, 1, 2, 3, 4]]]"
        Type parameter "\_T@list" is invariant, but "list[int]" is not the same as "list[Literal[0, 1, 2, 3, 4]]"
        Consider switching from "list" to "Sequence" which is covariant
  - **Location**: `haive-games/src/haive/games/checkers/state.py:713:25`

### 📄 haive-games/src/haive/games/checkers/state_manager.py

- [ ] **Line 84** (`reportArgumentType`)
  - **Issue**: Argument of type "list[list[int]]" cannot be assigned to parameter "board" of type "list[list[Literal[0, 1, 2, 3, 4]]]" in function "**init**"
      "list[list[int]]" is not assignable to "list[list[Literal[0, 1, 2, 3, 4]]]"
        Type parameter "\_T@list" is invariant, but "list[int]" is not the same as "list[Literal[0, 1, 2, 3, 4]]"
        Consider switching from "list" to "Sequence" which is covariant
  - **Location**: `haive-games/src/haive/games/checkers/state_manager.py:84:18`

- [ ] **Line 175** (`reportArgumentType`)
  - **Issue**: Argument of type "list[list[Literal[0, 1, 2, 3, 4]]]" cannot be assigned to parameter "board" of type "list[list[int]]" in function "\_get_jump_moves"
      "list[list[Literal[0, 1, 2, 3, 4]]]" is not assignable to "list[list[int]]"
        Type parameter "\_T@list" is invariant, but "list[Literal[0, 1, 2, 3, 4]]" is not the same as "list[int]"
        Consider switching from "list" to "Sequence" which is covariant
  - **Location**: `haive-games/src/haive/games/checkers/state_manager.py:175:41`

- [ ] **Line 182** (`reportArgumentType`)
  - **Issue**: Argument of type "list[list[Literal[0, 1, 2, 3, 4]]]" cannot be assigned to parameter "board" of type "list[list[int]]" in function "\_get_regular_moves"
      "list[list[Literal[0, 1, 2, 3, 4]]]" is not assignable to "list[list[int]]"
        Type parameter "\_T@list" is invariant, but "list[Literal[0, 1, 2, 3, 4]]" is not the same as "list[int]"
        Consider switching from "list" to "Sequence" which is covariant
  - **Location**: `haive-games/src/haive/games/checkers/state_manager.py:182:38`

- [ ] **Line 273** (`reportArgumentType`)
  - **Issue**: Argument of type "str" cannot be assigned to parameter "player" of type "Literal['red', 'black']" in function "**init**"
      Type "str" is not assignable to type "Literal['red', 'black']"
        "str" is not assignable to type "Literal['red']"
        "str" is not assignable to type "Literal['black']"
  - **Location**: `haive-games/src/haive/games/checkers/state_manager.py:273:35`

- [ ] **Line 365** (`reportArgumentType`)
  - **Issue**: Argument of type "str" cannot be assigned to parameter "player" of type "Literal['red', 'black']" in function "**init**"
      Type "str" is not assignable to type "Literal['red', 'black']"
        "str" is not assignable to type "Literal['red']"
        "str" is not assignable to type "Literal['black']"
  - **Location**: `haive-games/src/haive/games/checkers/state_manager.py:365:31`

- [ ] **Line 483** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "append" for class "Sequence[CheckersMove]"
      Attribute "append" is unknown
  - **Location**: `haive-games/src/haive/games/checkers/state_manager.py:483:31`

- [ ] **Line 489** (`reportArgumentType`)
  - **Issue**: Argument of type "list[list[Literal[0, 1, 2, 3, 4]]]" cannot be assigned to parameter "board" of type "list[list[int]]" in function "\_create_board_string"
      "list[list[Literal[0, 1, 2, 3, 4]]]" is not assignable to "list[list[int]]"
        Type parameter "\_T@list" is invariant, but "list[Literal[0, 1, 2, 3, 4]]" is not the same as "list[int]"
        Consider switching from "list" to "Sequence" which is covariant
  - **Location**: `haive-games/src/haive/games/checkers/state_manager.py:489:58`

- [ ] **Line 565** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "append" for class "Sequence[CheckersAnalysis]"
      Attribute "append" is unknown
  - **Location**: `haive-games/src/haive/games/checkers/state_manager.py:565:35`

- [ ] **Line 569** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "append" for class "Sequence[CheckersAnalysis]"
      Attribute "append" is unknown
  - **Location**: `haive-games/src/haive/games/checkers/state_manager.py:569:37`

### 📄 haive-games/src/haive/games/chess/agent.py

- [ ] **Line 63** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "items" for class "list[Any]"
      Attribute "items" is unknown
  - **Location**: `haive-games/src/haive/games/chess/agent.py:63:49`

- [ ] **Line 63** (`reportOptionalMemberAccess`)
  - **Issue**: "items" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/chess/agent.py:63:49`

- [ ] **Line 127** (`reportReturnType`)
  - **Issue**: Function with declared return type "Command[Unknown]" must return value on all code paths
      "None" is not assignable to "Command[Unknown]"
  - **Location**: `haive-games/src/haive/games/chess/agent.py:127:58`

### 📄 haive-games/src/haive/games/chess/api_example.py

- [ ] **Line 130** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, AugLLMConfig]" cannot be assigned to parameter "engines" of type "list[Any] | None" in function "**init**"
      Type "dict[str, AugLLMConfig]" is not assignable to type "list[Any] | None"
        "dict[str, AugLLMConfig]" is not assignable to "list[Any]"
        "dict[str, AugLLMConfig]" is not assignable to "None"
  - **Location**: `haive-games/src/haive/games/chess/api_example.py:130:20`

### 📄 haive-games/src/haive/games/chess/config.py

- [ ] **Line 161** (`reportReturnType`)
  - **Issue**: Type "dict[str, AugLLMConfig]" is not assignable to return type "list[Any]"
      "dict[str, AugLLMConfig]" is not assignable to "list[Any]"
  - **Location**: `haive-games/src/haive/games/chess/config.py:161:15`

- [ ] **Line 197** (`reportReturnType`)
  - **Issue**: Type "dict[str, AugLLMConfig]" is not assignable to return type "list[Any]"
      "dict[str, AugLLMConfig]" is not assignable to "list[Any]"
  - **Location**: `haive-games/src/haive/games/chess/config.py:197:15`

- [ ] **Line 203** (`reportCallIssue`)
  - **Issue**: Object of type "PydanticDescriptorProxy[ModelValidatorDecoratorInfo]" is not callable
      Attribute "**call**" is unknown
  - **Location**: `haive-games/src/haive/games/chess/config.py:203:8`

### 📄 haive-games/src/haive/games/chess/configurable_config.py

- [ ] **Line 218** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "value" for class "str"
      Attribute "value" is unknown
  - **Location**: `haive-games/src/haive/games/chess/configurable_config.py:218:32`

### 📄 haive-games/src/haive/games/chess/configurable_engines.py

- [ ] **Line 223** (`reportArgumentType`)
  - **Issue**: Expression of type "None" cannot be assigned to parameter of type "dict[str, str]"
      "None" is not assignable to "dict[str, str]"
  - **Location**: `haive-games/src/haive/games/chess/configurable_engines.py:223:32`

### 📄 haive-games/src/haive/games/chess/dynamic_config.py

- [ ] **Line 137** (`reportReturnType`)
  - **Issue**: Type "dict[str, AugLLMConfig]" is not assignable to return type "list[Any]"
      "dict[str, AugLLMConfig]" is not assignable to "list[Any]"
  - **Location**: `haive-games/src/haive/games/chess/dynamic_config.py:137:15`

- [ ] **Line 173** (`reportReturnType`)
  - **Issue**: Type "dict[str, AugLLMConfig]" is not assignable to return type "list[Any]"
      "dict[str, AugLLMConfig]" is not assignable to "list[Any]"
  - **Location**: `haive-games/src/haive/games/chess/dynamic_config.py:173:15`

### 📄 haive-games/src/haive/games/chess/engines.py

- [ ] **Line 213** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/chess/engines.py:213:50`

### 📄 haive-games/src/haive/games/chess/example.py

- [ ] **Line 23** (`reportArgumentType`)
  - **Issue**: Expression of type "None" cannot be assigned to parameter of type "str"
      "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/chess/example.py:23:36`

### 📄 haive-games/src/haive/games/chess/example_configurable.py

- [ ] **Line 26** (`reportArgumentType`)
  - **Issue**: Expression of type "None" cannot be assigned to parameter of type "str"
      "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/chess/example_configurable.py:26:23`

- [ ] **Line 28** (`reportArgumentType`)
  - **Issue**: Expression of type "None" cannot be assigned to parameter of type "str"
      "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/chess/example_configurable.py:28:23`

- [ ] **Line 61** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, AugLLMConfig]" cannot be assigned to parameter "engines" of type "list[Any] | None" in function "**init**"
      Type "dict[str, AugLLMConfig]" is not assignable to type "list[Any] | None"
        "dict[str, AugLLMConfig]" is not assignable to "list[Any]"
        "dict[str, AugLLMConfig]" is not assignable to "None"
  - **Location**: `haive-games/src/haive/games/chess/example_configurable.py:61:16`

- [ ] **Line 74** (`reportUndefinedVariable`)
  - **Issue**: "ChessAgent" is not defined
  - **Location**: `haive-games/src/haive/games/chess/example_configurable.py:74:12`

- [ ] **Line 143** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, AugLLMConfig]" cannot be assigned to parameter "engines" of type "list[Any] | None" in function "**init**"
      Type "dict[str, AugLLMConfig]" is not assignable to type "list[Any] | None"
        "dict[str, AugLLMConfig]" is not assignable to "list[Any]"
        "dict[str, AugLLMConfig]" is not assignable to "None"
  - **Location**: `haive-games/src/haive/games/chess/example_configurable.py:143:16`

- [ ] **Line 149** (`reportUndefinedVariable`)
  - **Issue**: "ChessAgent" is not defined
  - **Location**: `haive-games/src/haive/games/chess/example_configurable.py:149:4`

### 📄 haive-games/src/haive/games/chess/generic_engines.py

- [ ] **Line 102** (`reportUndefinedVariable`)
  - **Issue**: "current_board_fen" is not defined
  - **Location**: `haive-games/src/haive/games/chess/generic_engines.py:102:41`

- [ ] **Line 104** (`reportUndefinedVariable`)
  - **Issue**: "recent_moves" is not defined
  - **Location**: `haive-games/src/haive/games/chess/generic_engines.py:104:15`

- [ ] **Line 106** (`reportUndefinedVariable`)
  - **Issue**: "captured_pieces" is not defined
  - **Location**: `haive-games/src/haive/games/chess/generic_engines.py:106:18`

### 📄 haive-games/src/haive/games/chess/llm_utils.py

- [ ] **Line 173** (`reportArgumentType`)
  - **Issue**: Argument of type "float" cannot be assigned to parameter "value" of type "str" in function "**setitem**"
      "float" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/chess/llm_utils.py:173:8`

- [ ] **Line 179** (`reportArgumentType`)
  - **Issue**: Argument of type "float" cannot be assigned to parameter "value" of type "str" in function "**setitem**"
      "float" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/chess/llm_utils.py:179:8`

- [ ] **Line 195** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get_available_providers" for class "type[GameLLMFactory]"
      Attribute "get_available_providers" is unknown
  - **Location**: `haive-games/src/haive/games/chess/llm_utils.py:195:26`

### 📄 haive-games/src/haive/games/chess/state_manager.py

- [ ] **Line 70** (`reportCallIssue`)
  - **Issue**: No parameter named "board_fen"
  - **Location**: `haive-games/src/haive/games/chess/state_manager.py:70:12`

- [ ] **Line 75** (`reportCallIssue`)
  - **Issue**: No parameter named "analysis"
  - **Location**: `haive-games/src/haive/games/chess/state_manager.py:75:12`

- [ ] **Line 130** (`reportCallIssue`)
  - **Issue**: No parameter named "board_fen"
  - **Location**: `haive-games/src/haive/games/chess/state_manager.py:130:12`

- [ ] **Line 135** (`reportCallIssue`)
  - **Issue**: No parameter named "analysis"
  - **Location**: `haive-games/src/haive/games/chess/state_manager.py:135:12`

- [ ] **Line 135** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "analysis" for class "ChessState"
      Attribute "analysis" is unknown
  - **Location**: `haive-games/src/haive/games/chess/state_manager.py:135:27`

### 📄 haive-games/src/haive/games/chess/ui.py

- [ ] **Line 18** (`reportAttributeAccessIssue`)
  - **Issue**: "ChessAgentConfig" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/chess/ui.py:18:37`

- [ ] **Line 464** (`reportOptionalMemberAccess`)
  - **Issue**: "stream" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/chess/ui.py:464:32`

- [ ] **Line 476** (`reportOptionalMemberAccess`)
  - **Issue**: "move_history" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/chess/ui.py:476:34`

- [ ] **Line 477** (`reportOptionalMemberAccess`)
  - **Issue**: "move_history" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/chess/ui.py:477:52`

- [ ] **Line 478** (`reportOptionalMemberAccess`)
  - **Issue**: "move_history" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/chess/ui.py:478:57`

- [ ] **Line 500** (`reportOptionalMemberAccess`)
  - **Issue**: "game_status" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/chess/ui.py:500:34`

- [ ] **Line 517** (`reportOptionalMemberAccess`)
  - **Issue**: "error_message" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/chess/ui.py:517:34`

- [ ] **Line 519** (`reportOptionalMemberAccess`)
  - **Issue**: "error_message" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/chess/ui.py:519:61`

### 📄 haive-games/src/haive/games/clue/agent.py

- [ ] **Line 259** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "solution" for class "GameConfig"
      Attribute "solution" is unknown
  - **Location**: `haive-games/src/haive/games/clue/agent.py:259:33`

- [ ] **Line 260** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "first_player" for class "GameConfig"
      Attribute "first_player" is unknown
  - **Location**: `haive-games/src/haive/games/clue/agent.py:260:37`

- [ ] **Line 261** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "max_turns" for class "GameConfig"
      Attribute "max_turns" is unknown
  - **Location**: `haive-games/src/haive/games/clue/agent.py:261:34`

- [ ] **Line 432** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "solution" for class "GameConfig"
      Attribute "solution" is unknown
  - **Location**: `haive-games/src/haive/games/clue/agent.py:432:33`

- [ ] **Line 433** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "first_player" for class "GameConfig"
      Attribute "first_player" is unknown
  - **Location**: `haive-games/src/haive/games/clue/agent.py:433:37`

- [ ] **Line 434** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "max_turns" for class "GameConfig"
      Attribute "max_turns" is unknown
  - **Location**: `haive-games/src/haive/games/clue/agent.py:434:34`

- [ ] **Line 468** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "game_status" for class "ClueState"
      Type "Literal['ongoing_win']" is not assignable to type "Literal['ongoing', 'player1_win', 'player2_win']"
        "Literal['ongoing_win']" is not assignable to type "Literal['ongoing']"
        "Literal['ongoing_win']" is not assignable to type "Literal['player1_win']"
        "Literal['ongoing_win']" is not assignable to type "Literal['player2_win']"
  - **Location**: `haive-games/src/haive/games/clue/agent.py:468:56`

### 📄 haive-games/src/haive/games/clue/controller.py

- [ ] **Line 11** (`reportAttributeAccessIssue`)
  - **Issue**: "AugLLMEngine" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/clue/controller.py:11:38`

- [ ] **Line 89** (`reportArgumentType`)
  - **Issue**: Argument of type "list[ValidSuspect]" cannot be assigned to parameter "iterable" of type "Iterable[ClueCard]" in function "extend"
      "list[ValidSuspect]" is not assignable to "Iterable[ClueCard]"
        Type parameter "\_T_co@Iterable" is covariant, but "ValidSuspect" is not a subtype of "ClueCard"
          "ValidSuspect" is not assignable to "ClueCard"
  - **Location**: `haive-games/src/haive/games/clue/controller.py:89:20`

- [ ] **Line 90** (`reportArgumentType`)
  - **Issue**: Argument of type "list[ValidWeapon]" cannot be assigned to parameter "iterable" of type "Iterable[ClueCard]" in function "extend"
      "list[ValidWeapon]" is not assignable to "Iterable[ClueCard]"
        Type parameter "\_T_co@Iterable" is covariant, but "ValidWeapon" is not a subtype of "ClueCard"
          "ValidWeapon" is not assignable to "ClueCard"
  - **Location**: `haive-games/src/haive/games/clue/controller.py:90:20`

- [ ] **Line 91** (`reportArgumentType`)
  - **Issue**: Argument of type "list[ValidRoom]" cannot be assigned to parameter "iterable" of type "Iterable[ClueCard]" in function "extend"
      "list[ValidRoom]" is not assignable to "Iterable[ClueCard]"
        Type parameter "\_T_co@Iterable" is covariant, but "ValidRoom" is not a subtype of "ClueCard"
          "ValidRoom" is not assignable to "ClueCard"
  - **Location**: `haive-games/src/haive/games/clue/controller.py:91:20`

- [ ] **Line 147** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "FINISHED" for class "type[GameStatus]"
      Attribute "FINISHED" is unknown
  - **Location**: `haive-games/src/haive/games/clue/controller.py:147:48`

- [ ] **Line 193** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "FINISHED" for class "type[GameStatus]"
      Attribute "FINISHED" is unknown
  - **Location**: `haive-games/src/haive/games/clue/controller.py:193:56`

- [ ] **Line 216** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "FINISHED" for class "type[GameStatus]"
      Attribute "FINISHED" is unknown
  - **Location**: `haive-games/src/haive/games/clue/controller.py:216:48`

### 📄 haive-games/src/haive/games/clue/example.py

- [ ] **Line 236** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "game_status" for class "ClueState"
      Type "str" is not assignable to type "Literal['ongoing', 'player1_win', 'player2_win']"
        "str" is not assignable to type "Literal['ongoing']"
        "str" is not assignable to type "Literal['player1_win']"
        "str" is not assignable to type "Literal['player2_win']"
  - **Location**: `haive-games/src/haive/games/clue/example.py:236:36`

- [ ] **Line 312** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "game_status" for class "ClueState"
      Type "Literal['draw']" is not assignable to type "Literal['ongoing', 'player1_win', 'player2_win']"
        "Literal['draw']" is not assignable to type "Literal['ongoing']"
        "Literal['draw']" is not assignable to type "Literal['player1_win']"
        "Literal['draw']" is not assignable to type "Literal['player2_win']"
  - **Location**: `haive-games/src/haive/games/clue/example.py:312:36`

### 📄 haive-games/src/haive/games/clue/generic_engines.py

- [ ] **Line 101** (`reportAbstractUsage`)
  - **Issue**: Cannot instantiate abstract class "CluePromptGenerator"
      "GenericPromptGenerator.create_analysis_prompt" is not implemented
      "GenericPromptGenerator.get_move_output_model" is not implemented
      and 1 more...
  - **Location**: `haive-games/src/haive/games/clue/generic_engines.py:101:27`

- [ ] **Line 101** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "players"
  - **Location**: `haive-games/src/haive/games/clue/generic_engines.py:101:27`

- [ ] **Line 133** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "create_engines" for class "ClueEngineFactory"
      Attribute "create_engines" is unknown
  - **Location**: `haive-games/src/haive/games/clue/generic_engines.py:133:24`

### 📄 haive-games/src/haive/games/clue/runner.py

- [ ] **Line 61** (`reportOptionalMemberAccess`)
  - **Issue**: "name" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/clue/runner.py:61:47`

- [ ] **Line 111** (`reportOptionalMemberAccess`)
  - **Issue**: "name" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/clue/runner.py:111:47`

### 📄 haive-games/src/haive/games/clue/state_manager.py

- [ ] **Line 79** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "game_status" for class "ClueState"
      Type "str" is not assignable to type "Literal['ongoing', 'player1_win', 'player2_win']"
        "str" is not assignable to type "Literal['ongoing']"
        "str" is not assignable to type "Literal['player1_win']"
        "str" is not assignable to type "Literal['player2_win']"
  - **Location**: `haive-games/src/haive/games/clue/state_manager.py:79:36`

- [ ] **Line 79** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player" for class "ClueGuess"
      Attribute "player" is unknown
  - **Location**: `haive-games/src/haive/games/clue/state_manager.py:79:44`

- [ ] **Line 80** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player" for class "ClueGuess"
      Attribute "player" is unknown
  - **Location**: `haive-games/src/haive/games/clue/state_manager.py:80:36`

- [ ] **Line 84** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player" for class "ClueGuess"
      Attribute "player" is unknown
  - **Location**: `haive-games/src/haive/games/clue/state_manager.py:84:53`

- [ ] **Line 88** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "game_status" for class "ClueState"
      Type "str" is not assignable to type "Literal['ongoing', 'player1_win', 'player2_win']"
        "str" is not assignable to type "Literal['ongoing']"
        "str" is not assignable to type "Literal['player1_win']"
        "str" is not assignable to type "Literal['player2_win']"
  - **Location**: `haive-games/src/haive/games/clue/state_manager.py:88:36`

- [ ] **Line 89** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "winner" for class "ClueState"
      Type "ValidSuspect" is not assignable to type "str | None"
        "ValidSuspect" is not assignable to "str"
        "ValidSuspect" is not assignable to "None"
  - **Location**: `haive-games/src/haive/games/clue/state_manager.py:89:31`

### 📄 haive-games/src/haive/games/common/voting_system.py

- [ ] **Line 18** (`reportMissingImports`)
  - **Issue**: Import "haive.games.simple.agent" could not be resolved
  - **Location**: `haive-games/src/haive/games/common/voting_system.py:18:5`

### 📄 haive-games/src/haive/games/connect4/agent.py

- [ ] **Line 41** (`reportArgumentType`)
  - **Issue**: Argument of type "Connect4AgentConfig" cannot be assigned to parameter "config" of type "GameConfig" in function "**init**"
      "Connect4AgentConfig" is not assignable to "GameConfig"
  - **Location**: `haive-games/src/haive/games/connect4/agent.py:41:25`

- [ ] **Line 104** (`reportCallIssue`)
  - **Issue**: No overloads for "**getitem**" match the provided arguments
  - **Location**: `haive-games/src/haive/games/connect4/agent.py:104:12`

- [ ] **Line 104** (`reportArgumentType`)
  - **Issue**: Argument of type "int | None" cannot be assigned to parameter "s" of type "slice[Any, Any, Any]" in function "**getitem**"
      Type "int | None" is not assignable to type "slice[Any, Any, Any]"
        "int" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-games/src/haive/games/connect4/agent.py:104:12`

- [ ] **Line 105** (`reportArgumentType`)
  - **Issue**: Argument of type "int | None" cannot be assigned to parameter "row" of type "int" in function "\_check_win"
      Type "int | None" is not assignable to type "int"
        "None" is not assignable to "int"
  - **Location**: `haive-games/src/haive/games/connect4/agent.py:105:57`

- [ ] **Line 110** (`reportCallIssue`)
  - **Issue**: No overloads for "**getitem**" match the provided arguments
  - **Location**: `haive-games/src/haive/games/connect4/agent.py:110:12`

- [ ] **Line 110** (`reportArgumentType`)
  - **Issue**: Argument of type "int | None" cannot be assigned to parameter "s" of type "slice[Any, Any, Any]" in function "**getitem**"
      Type "int | None" is not assignable to type "slice[Any, Any, Any]"
        "int" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-games/src/haive/games/connect4/agent.py:110:12`

- [ ] **Line 111** (`reportArgumentType`)
  - **Issue**: Argument of type "int | None" cannot be assigned to parameter "row" of type "int" in function "\_check_win"
      Type "int | None" is not assignable to type "int"
        "None" is not assignable to "int"
  - **Location**: `haive-games/src/haive/games/connect4/agent.py:111:57`

- [ ] **Line 165** (`reportArgumentType`)
  - **Issue**: Argument of type "Connect4State" cannot be assigned to parameter "state" of type "Connect4AgentConfig" in function "make_move"
      "Connect4State" is not assignable to "Connect4AgentConfig"
  - **Location**: `haive-games/src/haive/games/connect4/agent.py:165:30`

- [ ] **Line 173** (`reportArgumentType`)
  - **Issue**: Argument of type "Connect4State" cannot be assigned to parameter "state" of type "Connect4AgentConfig" in function "make_move"
      "Connect4State" is not assignable to "Connect4AgentConfig"
  - **Location**: `haive-games/src/haive/games/connect4/agent.py:173:30`

- [ ] **Line 181** (`reportArgumentType`)
  - **Issue**: Argument of type "Connect4State" cannot be assigned to parameter "state" of type "Connect4AgentConfig" in function "analyze_position"
      "Connect4State" is not assignable to "Connect4AgentConfig"
  - **Location**: `haive-games/src/haive/games/connect4/agent.py:181:37`

- [ ] **Line 190** (`reportArgumentType`)
  - **Issue**: Argument of type "Connect4State" cannot be assigned to parameter "state" of type "Connect4AgentConfig" in function "analyze_position"
      "Connect4State" is not assignable to "Connect4AgentConfig"
  - **Location**: `haive-games/src/haive/games/connect4/agent.py:190:37`

### 📄 haive-games/src/haive/games/connect4/configurable_config.py

- [ ] **Line 139** (`reportArgumentType`)
  - **Issue**: Argument of type "float | None" cannot be assigned to parameter "temperature" of type "float" in function "create_generic_connect4_engines_simple"
      Type "float | None" is not assignable to type "float"
        "None" is not assignable to "float"
  - **Location**: `haive-games/src/haive/games/connect4/configurable_config.py:139:28`

- [ ] **Line 199** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "value" for class "str"
      Attribute "value" is unknown
  - **Location**: `haive-games/src/haive/games/connect4/configurable_config.py:199:32`

### 📄 haive-games/src/haive/games/connect4/factory.py

- [ ] **Line 41** (`reportArgumentType`)
  - **Issue**: Argument of type "PostgresCheckpointerConfig" cannot be assigned to parameter "persistence" of type "CheckpointerConfig[Unknown] | None" in function "**init**"
      Type "PostgresCheckpointerConfig" is not assignable to type "CheckpointerConfig[Unknown] | None"
        "PostgresCheckpointerConfig" is not assignable to "CheckpointerConfig[Unknown]"
        "PostgresCheckpointerConfig" is not assignable to "None"
  - **Location**: `haive-games/src/haive/games/connect4/factory.py:41:20`

- [ ] **Line 67** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "visualize_state" for class "Agent[Unknown]"
      Attribute "visualize_state" is unknown
  - **Location**: `haive-games/src/haive/games/connect4/factory.py:67:10`

- [ ] **Line 72** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "visualize_state" for class "Agent[Unknown]"
      Attribute "visualize_state" is unknown
  - **Location**: `haive-games/src/haive/games/connect4/factory.py:72:14`

### 📄 haive-games/src/haive/games/connect4/state.py

- [ ] **Line 65** (`reportGeneralTypeIssues`)
  - **Issue**: "turn" overrides a field of the same name but is missing a default value
  - **Location**: `haive-games/src/haive/games/connect4/state.py:65:4`

- [ ] **Line 209** (`reportArgumentType`)
  - **Issue**: Argument of type "list[list[None]]" cannot be assigned to parameter "board" of type "list[list[str | None]]" in function "**init**"
      "list[list[None]]" is not assignable to "list[list[str | None]]"
        Type parameter "\_T@list" is invariant, but "list[None]" is not the same as "list[str | None]"
        Consider switching from "list" to "Sequence" which is covariant
  - **Location**: `haive-games/src/haive/games/connect4/state.py:209:25`

### 📄 haive-games/src/haive/games/connect4/state_manager.py

- [ ] **Line 64** (`reportArgumentType`)
  - **Issue**: Argument of type "list[list[None]]" cannot be assigned to parameter "board" of type "list[list[str | None]]" in function "**init**"
      "list[list[None]]" is not assignable to "list[list[str | None]]"
        Type parameter "\_T@list" is invariant, but "list[None]" is not the same as "list[str | None]"
        Consider switching from "list" to "Sequence" which is covariant
  - **Location**: `haive-games/src/haive/games/connect4/state_manager.py:64:18`

- [ ] **Line 111** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "game_status" for class "Connect4State"
      Type "LiteralString" is not assignable to type "Literal['ongoing', 'red_win', 'yellow_win', 'draw']"
        "str" is not assignable to "Literal['ongoing']"
        "str" is not assignable to "Literal['red_win']"
        "str" is not assignable to "Literal['yellow_win']"
        "str" is not assignable to "Literal['draw']"
  - **Location**: `haive-games/src/haive/games/connect4/state_manager.py:111:36`

### 📄 haive-games/src/haive/games/connect4/ui.py

- [ ] **Line 287** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['red', 'yellow'] | None" cannot be assigned to parameter "key" of type "str" in function "**getitem**"
      Type "Literal['red', 'yellow'] | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/connect4/ui.py:287:23`

- [ ] **Line 289** (`reportOptionalMemberAccess`)
  - **Issue**: "upper" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/connect4/ui.py:289:62`

### 📄 haive-games/src/haive/games/core/agent/game_config.py

- [ ] **Line 27** (`reportGeneralTypeIssues`)
  - **Issue**: Type variable "Player" has no meaning in this context
  - **Location**: `haive-games/src/haive/games/core/agent/game_config.py:27:18`

- [ ] **Line 28** (`reportArgumentType`)
  - **Issue**: Argument of type "type[GameState]" cannot be assigned to parameter "default_factory" of type "(() -> \_T@Field) | ((dict[str, Any]) -> \_T@Field)" in function "Field"
      Type "type[GameState]" is not assignable to type "(() -> \_T@Field) | ((dict[str, Any]) -> \_T@Field)"
        Type "type[GameState]" is not assignable to type "(dict[str, Any]) -> \_T@Field"
          Function accepts too many positional parameters; expected 0 but received 1
            Extra parameter "board"
            Extra parameter "players"
            Extra parameter "current_player"
            Extra parameter "game_status"
            Extra parameter "game_result"
    ...
  - **Location**: `haive-games/src/haive/games/core/agent/game_config.py:28:58`

### 📄 haive-games/src/haive/games/core/base/config.py

- [ ] **Line 6** (`reportAttributeAccessIssue`)
  - **Issue**: "GameState" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/base/config.py:6:40`

- [ ] **Line 15** (`reportUndefinedVariable`)
  - **Issue**: "Game" is not defined
  - **Location**: `haive-games/src/haive/games/core/base/config.py:15:15`

- [ ] **Line 16** (`reportUndefinedVariable`)
  - **Issue**: "Game" is not defined
  - **Location**: `haive-games/src/haive/games/core/base/config.py:16:24`

### 📄 haive-games/src/haive/games/core/components/cards/base.py

- [ ] **Line 17** (`reportUndefinedVariable`)
  - **Issue**: "CardGameState" is not defined
  - **Location**: `haive-games/src/haive/games/core/components/cards/base.py:17:34`

- [ ] **Line 88** (`reportInvalidTypeArguments`)
  - **Issue**: Type "CardContainer[TCard@CardContainer]\*" is already specialized
  - **Location**: `haive-games/src/haive/games/core/components/cards/base.py:88:15`

- [ ] **Line 106** (`reportReturnType`)
  - **Issue**: Type "list[TCard@Deck | None]" is not assignable to return type "list[TCard@Deck]"
  - **Location**: `haive-games/src/haive/games/core/components/cards/base.py:106:15`

- [ ] **Line 135** (`reportArgumentType`)
  - **Issue**: Expression of type "None" cannot be assigned to parameter of type "dict[Unknown, Unknown]"
      "None" is not assignable to "dict[Unknown, Unknown]"
  - **Location**: `haive-games/src/haive/games/core/components/cards/base.py:135:65`

- [ ] **Line 140** (`reportArgumentType`)
  - **Issue**: Expression of type "None" cannot be assigned to parameter of type "dict[Unknown, Unknown]"
      "None" is not assignable to "dict[Unknown, Unknown]"
  - **Location**: `haive-games/src/haive/games/core/components/cards/base.py:140:64`

### 📄 haive-games/src/haive/games/core/components/cards/scoring.py

- [ ] **Line 7** (`reportMissingImports`)
  - **Issue**: Import "haive.games.core.components.models" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/components/cards/scoring.py:7:5`

- [ ] **Line 10** (`reportInvalidTypeForm`)
  - **Issue**: Type argument for "Generic" must be a type variable
  - **Location**: `haive-games/src/haive/games/core/components/cards/scoring.py:10:34`

- [ ] **Line 29** (`reportInvalidTypeForm`)
  - **Issue**: Type argument for "Generic" must be a type variable
  - **Location**: `haive-games/src/haive/games/core/components/cards/scoring.py:29:39`

- [ ] **Line 36** (`reportArgumentType`)
  - **Issue**: Expression of type "None" cannot be assigned to parameter of type "dict[Unknown, Unknown]"
      "None" is not assignable to "dict[Unknown, Unknown]"
  - **Location**: `haive-games/src/haive/games/core/components/cards/scoring.py:36:58`

- [ ] **Line 42** (`reportArgumentType`)
  - **Issue**: Expression of type "None" cannot be assigned to parameter of type "dict[Unknown, Unknown]"
      "None" is not assignable to "dict[Unknown, Unknown]"
  - **Location**: `haive-games/src/haive/games/core/components/cards/scoring.py:42:69`

### 📄 haive-games/src/haive/games/core/components/cards/standard.py

- [ ] **Line 9** (`reportMissingImports`)
  - **Issue**: Import "haive.games.core.components.models" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/components/cards/standard.py:9:5`

- [ ] **Line 67** (`reportCallIssue`)
  - **Issue**: No overloads for "field_validator" match the provided arguments
      Argument types: (Literal['value'], Literal[True], Literal[True])
  - **Location**: `haive-games/src/haive/games/core/components/cards/standard.py:67:5`

- [ ] **Line 80** (`reportCallIssue`)
  - **Issue**: No overloads for "field_validator" match the provided arguments
      Argument types: (Literal['is_face_card'], Literal[True], Literal[True])
  - **Location**: `haive-games/src/haive/games/core/components/cards/standard.py:80:5`

- [ ] **Line 90** (`reportCallIssue`)
  - **Issue**: No overloads for "field_validator" match the provided arguments
      Argument types: (Literal['color'], Literal[True], Literal[True])
  - **Location**: `haive-games/src/haive/games/core/components/cards/standard.py:90:5`

- [ ] **Line 105** (`reportCallIssue`)
  - **Issue**: No overloads for "field_validator" match the provided arguments
      Argument types: (Literal['name'], Literal[True], Literal[True])
  - **Location**: `haive-games/src/haive/games/core/components/cards/standard.py:105:5`

- [ ] **Line 204** (`reportArgumentType`)
  - **Issue**: Expression of type "None" cannot be assigned to parameter of type "dict[Unknown, Unknown]"
      "None" is not assignable to "dict[Unknown, Unknown]"
  - **Location**: `haive-games/src/haive/games/core/components/cards/standard.py:204:71`

- [ ] **Line 248** (`reportArgumentType`)
  - **Issue**: Expression of type "None" cannot be assigned to parameter of type "dict[Unknown, Unknown]"
      "None" is not assignable to "dict[Unknown, Unknown]"
  - **Location**: `haive-games/src/haive/games/core/components/cards/standard.py:248:56`

### 📄 haive-games/src/haive/games/core/components/cards/turns.py

- [ ] **Line 8** (`reportMissingImports`)
  - **Issue**: Import "haive.games.core.components.actions" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/components/cards/turns.py:8:5`

- [ ] **Line 9** (`reportMissingImports`)
  - **Issue**: Import "haive.games.core.components.models" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/components/cards/turns.py:9:5`

- [ ] **Line 21** (`reportInvalidTypeForm`)
  - **Issue**: Type argument for "Generic" must be a type variable
  - **Location**: `haive-games/src/haive/games/core/components/cards/turns.py:21:38`

- [ ] **Line 21** (`reportInvalidTypeForm`)
  - **Issue**: Type argument for "Generic" must be a type variable
  - **Location**: `haive-games/src/haive/games/core/components/cards/turns.py:21:45`

- [ ] **Line 21** (`reportInvalidTypeForm`)
  - **Issue**: Type argument for "Generic" must be a type variable
  - **Location**: `haive-games/src/haive/games/core/components/cards/turns.py:21:54`

- [ ] **Line 54** (`reportInvalidTypeForm`)
  - **Issue**: Type argument for "Generic" must be a type variable
  - **Location**: `haive-games/src/haive/games/core/components/cards/turns.py:54:37`

- [ ] **Line 54** (`reportInvalidTypeForm`)
  - **Issue**: Type argument for "Generic" must be a type variable
  - **Location**: `haive-games/src/haive/games/core/components/cards/turns.py:54:44`

- [ ] **Line 54** (`reportInvalidTypeForm`)
  - **Issue**: Type argument for "Generic" must be a type variable
  - **Location**: `haive-games/src/haive/games/core/components/cards/turns.py:54:53`

- [ ] **Line 108** (`reportOptionalMemberAccess`)
  - **Issue**: "add_action" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/core/components/cards/turns.py:108:34`

- [ ] **Line 114** (`reportOptionalMemberAccess`)
  - **Issue**: "is_complete" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/core/components/cards/turns.py:114:37`

### 📄 haive-games/src/haive/games/core/config/base.py

- [ ] **Line 225** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "engines" for class "BaseGameConfig\*"
      "list[Any]" is not assignable to "dict[str, Engine[Unknown, Unknown] | str]"
  - **Location**: `haive-games/src/haive/games/core/config/base.py:225:27`

- [ ] **Line 230** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "engines" for class "BaseGameConfig\*"
      "list[Any]" is not assignable to "dict[str, Engine[Unknown, Unknown] | str]"
  - **Location**: `haive-games/src/haive/games/core/config/base.py:230:27`

- [ ] **Line 236** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "engines" for class "BaseGameConfig\*"
      "list[Any]" is not assignable to "dict[str, Engine[Unknown, Unknown] | str]"
  - **Location**: `haive-games/src/haive/games/core/config/base.py:236:27`

- [ ] **Line 240** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "engines" for class "BaseGameConfig\*"
      "list[Any]" is not assignable to "dict[str, Engine[Unknown, Unknown] | str]"
  - **Location**: `haive-games/src/haive/games/core/config/base.py:240:27`

### 📄 haive-games/src/haive/games/core/game/**init**.py

- [ ] **Line 5** (`reportAttributeAccessIssue`)
  - **Issue**: "Config" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:5:4`

- [ ] **Line 7** (`reportAttributeAccessIssue`)
  - **Issue**: "add_space" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:7:4`

- [ ] **Line 8** (`reportAttributeAccessIssue`)
  - **Issue**: "connect_spaces" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:8:4`

- [ ] **Line 9** (`reportAttributeAccessIssue`)
  - **Issue**: "get_all_pieces" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:9:4`

- [ ] **Line 10** (`reportAttributeAccessIssue`)
  - **Issue**: "get_column" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:10:4`

- [ ] **Line 11** (`reportAttributeAccessIssue`)
  - **Issue**: "get_connected_spaces" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:11:4`

- [ ] **Line 12** (`reportAttributeAccessIssue`)
  - **Issue**: "get_player_pieces" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:12:4`

- [ ] **Line 13** (`reportAttributeAccessIssue`)
  - **Issue**: "get_property" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:13:4`

- [ ] **Line 14** (`reportAttributeAccessIssue`)
  - **Issue**: "get_row" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:14:4`

- [ ] **Line 15** (`reportAttributeAccessIssue`)
  - **Issue**: "get_space_at" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:15:4`

- [ ] **Line 16** (`reportAttributeAccessIssue`)
  - **Issue**: "get_space_at_position" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:16:4`

- [ ] **Line 17** (`reportAttributeAccessIssue`)
  - **Issue**: "initialize_grid" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:17:4`

- [ ] **Line 18** (`reportAttributeAccessIssue`)
  - **Issue**: "is_position_valid" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:18:4`

- [ ] **Line 19** (`reportAttributeAccessIssue`)
  - **Issue**: "place_piece" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:19:4`

- [ ] **Line 20** (`reportAttributeAccessIssue`)
  - **Issue**: "remove_piece" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:20:4`

- [ ] **Line 21** (`reportAttributeAccessIssue`)
  - **Issue**: "set_property" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:21:4`

- [ ] **Line 22** (`reportAttributeAccessIssue`)
  - **Issue**: "size" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:22:4`

- [ ] **Line 23** (`reportAttributeAccessIssue`)
  - **Issue**: "validate_dimensions" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:23:4`

- [ ] **Line 26** (`reportAttributeAccessIssue`)
  - **Issue**: "Config" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:26:4`

- [ ] **Line 34** (`reportAttributeAccessIssue`)
  - **Issue**: "abort" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:34:4`

- [ ] **Line 35** (`reportAttributeAccessIssue`)
  - **Issue**: "add_player" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:35:4`

- [ ] **Line 36** (`reportAttributeAccessIssue`)
  - **Issue**: "can_take_action" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:36:4`

- [ ] **Line 37** (`reportAttributeAccessIssue`)
  - **Issue**: "check_end_condition" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:37:4`

- [ ] **Line 38** (`reportAttributeAccessIssue`)
  - **Issue**: "create_game" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:38:4`

- [ ] **Line 39** (`reportAttributeAccessIssue`)
  - **Issue**: "create_position" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:39:4`

- [ ] **Line 40** (`reportAttributeAccessIssue`)
  - **Issue**: "determine_winner" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:40:4`

- [ ] **Line 41** (`reportAttributeAccessIssue`)
  - **Issue**: "end_turn" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:41:4`

- [ ] **Line 42** (`reportAttributeAccessIssue`)
  - **Issue**: "finish" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:42:4`

- [ ] **Line 43** (`reportAttributeAccessIssue`)
  - **Issue**: "get_container" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:43:4`

- [ ] **Line 44** (`reportAttributeAccessIssue`)
  - **Issue**: "get_current_player" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:44:4`

- [ ] **Line 45** (`reportAttributeAccessIssue`)
  - **Issue**: "get_piece" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:45:4`

- [ ] **Line 46** (`reportAttributeAccessIssue`)
  - **Issue**: "get_property" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:46:4`

- [ ] **Line 47** (`reportAttributeAccessIssue`)
  - **Issue**: "get_state_for_player" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:47:4`

- [ ] **Line 48** (`reportAttributeAccessIssue`)
  - **Issue**: "get_valid_moves" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:48:4`

- [ ] **Line 49** (`reportAttributeAccessIssue`)
  - **Issue**: "initialize" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:49:4`

- [ ] **Line 50** (`reportAttributeAccessIssue`)
  - **Issue**: "is_action_on_cooldown" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:50:4`

- [ ] **Line 51** (`reportAttributeAccessIssue`)
  - **Issue**: "is_finished" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:51:4`

- [ ] **Line 52** (`reportAttributeAccessIssue`)
  - **Issue**: "is_valid_player_count" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:52:4`

- [ ] **Line 53** (`reportAttributeAccessIssue`)
  - **Issue**: "pause" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:53:4`

- [ ] **Line 54** (`reportAttributeAccessIssue`)
  - **Issue**: "process_move" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:54:4`

- [ ] **Line 55** (`reportAttributeAccessIssue`)
  - **Issue**: "record_action" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:55:4`

- [ ] **Line 56** (`reportAttributeAccessIssue`)
  - **Issue**: "register_callback" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:56:4`

- [ ] **Line 57** (`reportAttributeAccessIssue`)
  - **Issue**: "resume" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:57:4`

- [ ] **Line 58** (`reportAttributeAccessIssue`)
  - **Issue**: "reverse_turn_order" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:58:4`

- [ ] **Line 59** (`reportAttributeAccessIssue`)
  - **Issue**: "set_cooldown" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:59:4`

- [ ] **Line 60** (`reportAttributeAccessIssue`)
  - **Issue**: "set_property" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:60:4`

- [ ] **Line 61** (`reportAttributeAccessIssue`)
  - **Issue**: "setup_game" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:61:4`

- [ ] **Line 62** (`reportAttributeAccessIssue`)
  - **Issue**: "skip_turn" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:62:4`

- [ ] **Line 63** (`reportAttributeAccessIssue`)
  - **Issue**: "start" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:63:4`

- [ ] **Line 64** (`reportAttributeAccessIssue`)
  - **Issue**: "start_turn" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:64:4`

- [ ] **Line 65** (`reportAttributeAccessIssue`)
  - **Issue**: "unregister_callback" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:65:4`

- [ ] **Line 66** (`reportAttributeAccessIssue`)
  - **Issue**: "update" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:66:4`

- [ ] **Line 67** (`reportAttributeAccessIssue`)
  - **Issue**: "update_game_state" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:67:4`

- [ ] **Line 68** (`reportAttributeAccessIssue`)
  - **Issue**: "validate_player_count" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:68:4`

- [ ] **Line 71** (`reportAttributeAccessIssue`)
  - **Issue**: "Config" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:71:4`

- [ ] **Line 76** (`reportAttributeAccessIssue`)
  - **Issue**: "axial_coords" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:76:4`

- [ ] **Line 77** (`reportAttributeAccessIssue`)
  - **Issue**: "chebyshev_distance" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:77:4`

- [ ] **Line 78** (`reportAttributeAccessIssue`)
  - **Issue**: "coordinates" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:78:4`

- [ ] **Line 79** (`reportAttributeAccessIssue`)
  - **Issue**: "display_coords" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:79:4`

- [ ] **Line 80** (`reportAttributeAccessIssue`)
  - **Issue**: "distance" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:80:4`

- [ ] **Line 81** (`reportAttributeAccessIssue`)
  - **Issue**: "distance_to" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:81:4`

- [ ] **Line 82** (`reportAttributeAccessIssue`)
  - **Issue**: "from_axial" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:82:4`

- [ ] **Line 83** (`reportAttributeAccessIssue`)
  - **Issue**: "manhattan_distance" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:83:4`

- [ ] **Line 84** (`reportAttributeAccessIssue`)
  - **Issue**: "neighbors" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:84:4`

- [ ] **Line 85** (`reportAttributeAccessIssue`)
  - **Issue**: "neighbors_with_diagonals" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:85:4`

- [ ] **Line 86** (`reportAttributeAccessIssue`)
  - **Issue**: "offset" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:86:4`

- [ ] **Line 87** (`reportAttributeAccessIssue`)
  - **Issue**: "serialize" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:87:4`

- [ ] **Line 88** (`reportAttributeAccessIssue`)
  - **Issue**: "validate_coordinates" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:88:4`

- [ ] **Line 89** (`reportAttributeAccessIssue`)
  - **Issue**: "validate_cube_coords" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:89:4`

- [ ] **Line 92** (`reportAttributeAccessIssue`)
  - **Issue**: "Config" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:92:4`

- [ ] **Line 97** (`reportAttributeAccessIssue`)
  - **Issue**: "add_connection" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:97:4`

- [ ] **Line 98** (`reportAttributeAccessIssue`)
  - **Issue**: "coordinates" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:98:4`

- [ ] **Line 99** (`reportAttributeAccessIssue`)
  - **Issue**: "get_grid_position" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:99:4`

- [ ] **Line 100** (`reportAttributeAccessIssue`)
  - **Issue**: "get_property" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:100:4`

- [ ] **Line 101** (`reportAttributeAccessIssue`)
  - **Issue**: "is_connected_to" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:101:4`

- [ ] **Line 102** (`reportAttributeAccessIssue`)
  - **Issue**: "is_occupied" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:102:4`

- [ ] **Line 103** (`reportAttributeAccessIssue`)
  - **Issue**: "place_piece" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:103:4`

- [ ] **Line 104** (`reportAttributeAccessIssue`)
  - **Issue**: "remove_connection" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:104:4`

- [ ] **Line 105** (`reportAttributeAccessIssue`)
  - **Issue**: "remove_piece" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:105:4`

- [ ] **Line 106** (`reportAttributeAccessIssue`)
  - **Issue**: "set_property" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:106:4`

- [ ] **Line 111** (`reportAttributeAccessIssue`)
  - **Issue**: "assign_to_player" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:111:4`

- [ ] **Line 112** (`reportAttributeAccessIssue`)
  - **Issue**: "can_move_to" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:112:4`

- [ ] **Line 113** (`reportAttributeAccessIssue`)
  - **Issue**: "place_at" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/game/__init__.py:113:4`

### 📄 haive-games/src/haive/games/core/game/containers/base.py

- [ ] **Line 15** (`reportMissingImports`)
  - **Issue**: Import "game.core.piece" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/game/containers/base.py:15:5`

### 📄 haive-games/src/haive/games/core/game/containers/container.py

- [ ] **Line 38** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "id" for class "object\*"
      Attribute "id" is unknown
  - **Location**: `haive-games/src/haive/games/core/game/containers/container.py:38:21`

- [ ] **Line 83** (`reportUndefinedVariable`)
  - **Issue**: "Card" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/containers/container.py:83:30`

- [ ] **Line 88** (`reportUndefinedVariable`)
  - **Issue**: "Card" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/containers/container.py:88:22`

- [ ] **Line 96** (`reportUndefinedVariable`)
  - **Issue**: "Card" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/containers/container.py:96:73`

- [ ] **Line 111** (`reportUndefinedVariable`)
  - **Issue**: "PlayingCard" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/containers/container.py:111:20`

- [ ] **Line 112** (`reportUndefinedVariable`)
  - **Issue**: "PlayingCard" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/containers/container.py:112:24`

- [ ] **Line 113** (`reportUndefinedVariable`)
  - **Issue**: "PlayingCard" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/containers/container.py:113:23`

- [ ] **Line 119** (`reportUndefinedVariable`)
  - **Issue**: "Tile" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/containers/container.py:119:33`

- [ ] **Line 122** (`reportUndefinedVariable`)
  - **Issue**: "Tile" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/containers/container.py:122:29`

- [ ] **Line 129** (`reportUndefinedVariable`)
  - **Issue**: "Tile" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/containers/container.py:129:51`

- [ ] **Line 144** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "owner_id" for class "object\*"
      Attribute "owner_id" is unknown
  - **Location**: `haive-games/src/haive/games/core/game/containers/container.py:144:14`

- [ ] **Line 151** (`reportUndefinedVariable`)
  - **Issue**: "Position" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/containers/container.py:151:48`

- [ ] **Line 151** (`reportUndefinedVariable`)
  - **Issue**: "Board" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/containers/container.py:151:65`

- [ ] **Line 153** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "id" for class "object\*"
      Attribute "id" is unknown
  - **Location**: `haive-games/src/haive/games/core/game/containers/container.py:153:50`

- [ ] **Line 157** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "can_move_to" for class "object\*"
      Attribute "can_move_to" is unknown
  - **Location**: `haive-games/src/haive/games/core/game/containers/container.py:157:60`

- [ ] **Line 158** (`reportReturnType`)
  - **Issue**: Type "object" is not assignable to return type "bool"
      "object" is not assignable to "bool"
  - **Location**: `haive-games/src/haive/games/core/game/containers/container.py:158:19`

- [ ] **Line 158** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "can_move_to" for class "object\*"
      Attribute "can_move_to" is unknown
  - **Location**: `haive-games/src/haive/games/core/game/containers/container.py:158:25`

### 📄 haive-games/src/haive/games/core/game/containers/deck.py

- [ ] **Line 12** (`reportMissingImports`)
  - **Issue**: Import "game_framework.containers.base" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/game/containers/deck.py:12:5`

- [ ] **Line 13** (`reportMissingImports`)
  - **Issue**: Import "game_framework.pieces.base" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/game/containers/deck.py:13:5`

- [ ] **Line 42** (`reportGeneralTypeIssues`)
  - **Issue**: Type variable "C" has no meaning in this context
  - **Location**: `haive-games/src/haive/games/core/game/containers/deck.py:42:23`

### 📄 haive-games/src/haive/games/core/game/core_board.py

- [ ] **Line 15** (`reportMissingImports`)
  - **Issue**: Import "game.core.piece" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/game/core_board.py:15:5`

- [ ] **Line 16** (`reportMissingImports`)
  - **Issue**: Import "game.core.position" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/game/core_board.py:16:5`

- [ ] **Line 17** (`reportMissingImports`)
  - **Issue**: Import "game.core.space" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/game/core_board.py:17:5`

- [ ] **Line 224** (`reportUndefinedVariable`)
  - **Issue**: "field_validator" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/core_board.py:224:5`

### 📄 haive-games/src/haive/games/core/game/core_game.py

- [ ] **Line 16** (`reportMissingImports`)
  - **Issue**: Import "game.core.board" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/game/core_game.py:16:5`

- [ ] **Line 17** (`reportMissingImports`)
  - **Issue**: Import "game.core.container" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/game/core_game.py:17:5`

- [ ] **Line 18** (`reportMissingImports`)
  - **Issue**: Import "game.core.move" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/game/core_game.py:18:5`

- [ ] **Line 19** (`reportMissingImports`)
  - **Issue**: Import "game.core.piece" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/game/core_game.py:19:5`

- [ ] **Line 20** (`reportMissingImports`)
  - **Issue**: Import "game.core.player" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/game/core_game.py:20:5`

- [ ] **Line 21** (`reportMissingImports`)
  - **Issue**: Import "game.core.position" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/game/core_game.py:21:5`

- [ ] **Line 22** (`reportMissingImports`)
  - **Issue**: Import "game.core.space" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/game/core_game.py:22:5`

- [ ] **Line 207** (`reportArgumentType`)
  - **Issue**: Expression of type "None" cannot be assigned to parameter of type "list[str]"
      "None" is not assignable to "list[str]"
  - **Location**: `haive-games/src/haive/games/core/game/core_game.py:207:62`

- [ ] **Line 379** (`reportOptionalMemberAccess`)
  - **Issue**: "id" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/core/game/core_game.py:379:42`

- [ ] **Line 386** (`reportOptionalMemberAccess`)
  - **Issue**: "id" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/core/game/core_game.py:386:42`

- [ ] **Line 615** (`reportUndefinedVariable`)
  - **Issue**: "move_type" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/core_game.py:615:20`

### 📄 haive-games/src/haive/games/core/game/core_position.py

- [ ] **Line 194** (`reportArgumentType`)
  - **Issue**: Argument of type "(cls: type[Self@HexPosition], v: int, values: dict[Unknown, Unknown]) -> int" cannot be assigned to parameter of type "\_V2BeforeAfterOrPlainValidatorType@field_validator"
      Type "(cls: type[Self@HexPosition], v: int, values: dict[Unknown, Unknown]) -> int" is not assignable to type "\_V2Validator | \_PartialClsOrStaticMethod"
        Type "(cls: type[Self@HexPosition], v: int, values: dict[Unknown, Unknown]) -> int" is not assignable to type "\_V2Validator | \_PartialClsOrStaticMethod"
          Type "(cls: type[Self@HexPosition], v: int, values: dict[Unknown, Unknown]) -> int" is not assignable to type "(cls: Any, value: Any, info: ValidationInfo, /) -> Any"
            Parameter 3: type "ValidationInfo" is incompatible with type "dict[Unknown, Unknown]"
              "ValidationInfo" is not assignable to "dict[Unknown, Unknown]"
          Type "(cls: type[Self@HexPosition], v: int, values: dict[Unknown, Unknown]) -> int" is not assignable to type "WithInfoValidatorFunction"
            Parameter 2: type "ValidationInfo" is incompatible with type "int"
              "ValidationInfo" is not assignable to "int"
  - **Location**: `haive-games/src/haive/games/core/game/core_position.py:194:5`

- [ ] **Line 198** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "data" for class "dict[Unknown, Unknown]"
      Attribute "data" is unknown
  - **Location**: `haive-games/src/haive/games/core/game/core_position.py:198:19`

- [ ] **Line 199** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "data" for class "dict[Unknown, Unknown]"
      Attribute "data" is unknown
  - **Location**: `haive-games/src/haive/games/core/game/core_position.py:199:19`

### 📄 haive-games/src/haive/games/core/game/core_space.py

- [ ] **Line 13** (`reportMissingImports`)
  - **Issue**: Import "game.core.piece" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/game/core_space.py:13:5`

- [ ] **Line 14** (`reportMissingImports`)
  - **Issue**: Import "game.core.position" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/game/core_space.py:14:5`

- [ ] **Line 163** (`reportUndefinedVariable`)
  - **Issue**: "computed_field" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/core_space.py:163:5`

- [ ] **Line 184** (`reportUndefinedVariable`)
  - **Issue**: "computed_field" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/core_space.py:184:5`

### 📄 haive-games/src/haive/games/core/game/piece.py

- [ ] **Line 12** (`reportUndefinedVariable`)
  - **Issue**: "P" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/piece.py:12:35`

- [ ] **Line 12** (`reportInvalidTypeForm`)
  - **Issue**: Type argument for "Generic" must be a type variable
  - **Location**: `haive-games/src/haive/games/core/game/piece.py:12:35`

- [ ] **Line 17** (`reportUndefinedVariable`)
  - **Issue**: "P" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/piece.py:17:14`

- [ ] **Line 20** (`reportUndefinedVariable`)
  - **Issue**: "P" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/piece.py:20:36`

- [ ] **Line 20** (`reportUndefinedVariable`)
  - **Issue**: "Board" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/piece.py:20:47`

- [ ] **Line 27** (`reportUndefinedVariable`)
  - **Issue**: "P" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/piece.py:27:33`

- [ ] **Line 37** (`reportUndefinedVariable`)
  - **Issue**: "Position" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/piece.py:37:14`

- [ ] **Line 39** (`reportUndefinedVariable`)
  - **Issue**: "Position" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/piece.py:39:36`

- [ ] **Line 39** (`reportUndefinedVariable`)
  - **Issue**: "Board" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/piece.py:39:54`

- [ ] **Line 41** (`reportUndefinedVariable`)
  - **Issue**: "Position" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/piece.py:41:33`

### 📄 haive-games/src/haive/games/core/game/pieces/core_game.py

- [ ] **Line 16** (`reportMissingImports`)
  - **Issue**: Import "game.core.board" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/game/pieces/core_game.py:16:5`

- [ ] **Line 17** (`reportMissingImports`)
  - **Issue**: Import "game.core.container" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/game/pieces/core_game.py:17:5`

- [ ] **Line 18** (`reportMissingImports`)
  - **Issue**: Import "game.core.move" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/game/pieces/core_game.py:18:5`

- [ ] **Line 19** (`reportMissingImports`)
  - **Issue**: Import "game.core.piece" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/game/pieces/core_game.py:19:5`

- [ ] **Line 20** (`reportMissingImports`)
  - **Issue**: Import "game.core.player" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/game/pieces/core_game.py:20:5`

- [ ] **Line 21** (`reportMissingImports`)
  - **Issue**: Import "game.core.position" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/game/pieces/core_game.py:21:5`

- [ ] **Line 22** (`reportMissingImports`)
  - **Issue**: Import "game.core.space" could not be resolved
  - **Location**: `haive-games/src/haive/games/core/game/pieces/core_game.py:22:5`

- [ ] **Line 207** (`reportArgumentType`)
  - **Issue**: Expression of type "None" cannot be assigned to parameter of type "list[str]"
      "None" is not assignable to "list[str]"
  - **Location**: `haive-games/src/haive/games/core/game/pieces/core_game.py:207:62`

- [ ] **Line 379** (`reportOptionalMemberAccess`)
  - **Issue**: "id" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/core/game/pieces/core_game.py:379:42`

- [ ] **Line 386** (`reportOptionalMemberAccess`)
  - **Issue**: "id" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/core/game/pieces/core_game.py:386:42`

- [ ] **Line 615** (`reportUndefinedVariable`)
  - **Issue**: "move_type" is not defined
  - **Location**: `haive-games/src/haive/games/core/game/pieces/core_game.py:615:20`

### 📄 haive-games/src/haive/games/core/piece/tile.py

- [ ] **Line 1** (`reportUndefinedVariable`)
  - **Issue**: "GamePiece" is not defined
  - **Location**: `haive-games/src/haive/games/core/piece/tile.py:1:11`

- [ ] **Line 1** (`reportUndefinedVariable`)
  - **Issue**: "P" is not defined
  - **Location**: `haive-games/src/haive/games/core/piece/tile.py:1:21`

- [ ] **Line 11** (`reportUndefinedVariable`)
  - **Issue**: "P" is not defined
  - **Location**: `haive-games/src/haive/games/core/piece/tile.py:11:36`

- [ ] **Line 11** (`reportUndefinedVariable`)
  - **Issue**: "Board" is not defined
  - **Location**: `haive-games/src/haive/games/core/piece/tile.py:11:47`

### 📄 haive-games/src/haive/games/core/players/agent.py

- [ ] **Line 7** (`reportAttributeAccessIssue`)
  - **Issue**: "GameConfig" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/core/players/agent.py:7:47`

- [ ] **Line 20** (`reportUndefinedVariable`)
  - **Issue**: "PlayerConfig" is not defined
  - **Location**: `haive-games/src/haive/games/core/players/agent.py:20:63`

- [ ] **Line 21** (`reportCallIssue`)
  - **Issue**: Expected 0 positional arguments
  - **Location**: `haive-games/src/haive/games/core/players/agent.py:21:25`

### 📄 haive-games/src/haive/games/debate/agent.py

- [ ] **Line 152** (`reportArgumentType`)
  - **Issue**: Argument of type "DebateAgentConfig" cannot be assigned to parameter "config" of type "MultiPlayerGameConfig" in function "**init**"
      "DebateAgentConfig" is not assignable to "MultiPlayerGameConfig"
  - **Location**: `haive-games/src/haive/games/debate/agent.py:152:25`

- [ ] **Line 199** (`reportUndefinedVariable`)
  - **Issue**: "logger" is not defined
  - **Location**: `haive-games/src/haive/games/debate/agent.py:199:8`

- [ ] **Line 200** (`reportUndefinedVariable`)
  - **Issue**: "logger" is not defined
  - **Location**: `haive-games/src/haive/games/debate/agent.py:200:8`

- [ ] **Line 201** (`reportUndefinedVariable`)
  - **Issue**: "logger" is not defined
  - **Location**: `haive-games/src/haive/games/debate/agent.py:201:8`

- [ ] **Line 208** (`reportUndefinedVariable`)
  - **Issue**: "logger" is not defined
  - **Location**: `haive-games/src/haive/games/debate/agent.py:208:16`

- [ ] **Line 225** (`reportArgumentType`)
  - **Issue**: Argument of type "str" cannot be assigned to parameter "keywords" of type "list[str]" in function "**init**"
      "str" is not assignable to "list[str]"
  - **Location**: `haive-games/src/haive/games/debate/agent.py:225:24`

- [ ] **Line 225** (`reportArgumentType`)
  - **Issue**: Argument of type "str" cannot be assigned to parameter "constraints" of type "dict[str, str] | None" in function "**init**"
      Type "str" is not assignable to type "dict[str, str] | None"
        "str" is not assignable to "dict[str, str]"
        "str" is not assignable to "None"
  - **Location**: `haive-games/src/haive/games/debate/agent.py:225:24`

- [ ] **Line 236** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "debate_format" for class "MultiPlayerGameConfig"
      Attribute "debate_format" is unknown
  - **Location**: `haive-games/src/haive/games/debate/agent.py:236:36`

- [ ] **Line 237** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "time_limit" for class "MultiPlayerGameConfig"
      Attribute "time_limit" is unknown
  - **Location**: `haive-games/src/haive/games/debate/agent.py:237:35`

- [ ] **Line 238** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "max_statements" for class "MultiPlayerGameConfig"
      Attribute "max_statements" is unknown
  - **Location**: `haive-games/src/haive/games/debate/agent.py:238:39`

- [ ] **Line 239** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "allow_interruptions" for class "MultiPlayerGameConfig"
      Attribute "allow_interruptions" is unknown
  - **Location**: `haive-games/src/haive/games/debate/agent.py:239:44`

- [ ] **Line 362** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "position", "persona", "bias"
  - **Location**: `haive-games/src/haive/games/debate/agent.py:362:16`

- [ ] **Line 401** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "position", "persona", "bias"
  - **Location**: `haive-games/src/haive/games/debate/agent.py:401:20`

- [ ] **Line 412** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "position", "persona", "bias"
  - **Location**: `haive-games/src/haive/games/debate/agent.py:412:24`

- [ ] **Line 440** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "position", "persona", "bias"
  - **Location**: `haive-games/src/haive/games/debate/agent.py:440:34`

- [ ] **Line 680** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "content" for class "dict[Unknown, Unknown]"
      Attribute "content" is unknown
  - **Location**: `haive-games/src/haive/games/debate/agent.py:680:31`

- [ ] **Line 724** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "participant_roles" for class "MultiPlayerGameConfig"
      Attribute "participant_roles" is unknown
  - **Location**: `haive-games/src/haive/games/debate/agent.py:724:23`

- [ ] **Line 725** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "participant_roles" for class "MultiPlayerGameConfig"
      Attribute "participant_roles" is unknown
  - **Location**: `haive-games/src/haive/games/debate/agent.py:725:47`

- [ ] **Line 730** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "moderator_role" for class "MultiPlayerGameConfig"
      Attribute "moderator_role" is unknown
  - **Location**: `haive-games/src/haive/games/debate/agent.py:730:23`

- [ ] **Line 808** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "position", "persona", "bias"
  - **Location**: `haive-games/src/haive/games/debate/agent.py:808:33`

- [ ] **Line 1087** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "position", "persona", "bias"
  - **Location**: `haive-games/src/haive/games/debate/agent.py:1087:20`

- [ ] **Line 1107** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "position", "persona", "bias"
  - **Location**: `haive-games/src/haive/games/debate/agent.py:1107:20`

- [ ] **Line 1115** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "position", "persona", "bias"
  - **Location**: `haive-games/src/haive/games/debate/agent.py:1115:24`

### 📄 haive-games/src/haive/games/debate/config.py

- [ ] **Line 221** (`reportAssignmentType`)
  - **Issue**: Type "dict[str, dict[str, AugLLMConfig]]" is not assignable to declared type "dict[str, AugLLMConfig]"
      "dict[str, dict[str, AugLLMConfig]]" is not assignable to "dict[str, AugLLMConfig]"
        Type parameter "\_VT@dict" is invariant, but "dict[str, AugLLMConfig]" is not the same as "AugLLMConfig"
        Consider switching from "dict" to "Mapping" which is covariant in the value type
  - **Location**: `haive-games/src/haive/games/debate/config.py:221:39`

### 📄 haive-games/src/haive/games/debate/engines.py

- [ ] **Line 38** (`reportArgumentType`)
  - **Issue**: Expression of type "None" cannot be assigned to parameter of type "str"
      "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/debate/engines.py:38:44`

### 📄 haive-games/src/haive/games/debate/example.py

- [ ] **Line 34** (`reportCallIssue`)
  - **Issue**: No parameter named "topic"
  - **Location**: `haive-games/src/haive/games/debate/example.py:34:8`

- [ ] **Line 36** (`reportCallIssue`)
  - **Issue**: No parameter named "max_rounds"
  - **Location**: `haive-games/src/haive/games/debate/example.py:36:8`

- [ ] **Line 37** (`reportCallIssue`)
  - **Issue**: No parameter named "num_debaters"
  - **Location**: `haive-games/src/haive/games/debate/example.py:37:8`

- [ ] **Line 38** (`reportCallIssue`)
  - **Issue**: No parameter named "num_judges"
  - **Location**: `haive-games/src/haive/games/debate/example.py:38:8`

- [ ] **Line 39** (`reportCallIssue`)
  - **Issue**: No parameter named "participant_generator_llm"
  - **Location**: `haive-games/src/haive/games/debate/example.py:39:8`

- [ ] **Line 41** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/debate/example.py:41:54`

- [ ] **Line 43** (`reportCallIssue`)
  - **Issue**: No parameter named "debater_llm"
  - **Location**: `haive-games/src/haive/games/debate/example.py:43:8`

- [ ] **Line 45** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/debate/example.py:45:54`

- [ ] **Line 47** (`reportCallIssue`)
  - **Issue**: No parameter named "judge_llm"
  - **Location**: `haive-games/src/haive/games/debate/example.py:47:8`

- [ ] **Line 49** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/debate/example.py:49:54`

### 📄 haive-games/src/haive/games/debate/generic_engines.py

- [ ] **Line 101** (`reportAbstractUsage`)
  - **Issue**: Cannot instantiate abstract class "DebatePromptGenerator"
      "GenericPromptGenerator.create_analysis_prompt" is not implemented
      "GenericPromptGenerator.get_move_output_model" is not implemented
      and 1 more...
  - **Location**: `haive-games/src/haive/games/debate/generic_engines.py:101:27`

- [ ] **Line 101** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "players"
  - **Location**: `haive-games/src/haive/games/debate/generic_engines.py:101:27`

- [ ] **Line 134** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "create_engines" for class "DebateEngineFactory"
      Attribute "create_engines" is unknown
  - **Location**: `haive-games/src/haive/games/debate/generic_engines.py:134:26`

### 📄 haive-games/src/haive/games/debate/state_manager.py

- [ ] **Line 36** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "current_speaker_idx", "phase_time_limit", "phase_statement_limit", "interruptions_allowed", "moderator_id"
  - **Location**: `haive-games/src/haive/games/debate/state_manager.py:36:16`

- [ ] **Line 67** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "persona", "bias"
  - **Location**: `haive-games/src/haive/games/debate/state_manager.py:67:38`

- [ ] **Line 113** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "sentiment"
  - **Location**: `haive-games/src/haive/games/debate/state_manager.py:113:24`

- [ ] **Line 136** (`reportArgumentType`)
  - **Issue**: Argument of type "Any | None" cannot be assigned to parameter "vote_value" of type "str | int | float" in function "**init**"
      Type "Any | None" is not assignable to type "str | int | float"
        Type "None" is not assignable to type "str | int | float"
          "None" is not assignable to "str"
          "None" is not assignable to "int"
          "None" is not assignable to "float"
  - **Location**: `haive-games/src/haive/games/debate/state_manager.py:136:27`

- [ ] **Line 271** (`reportCallIssue`)
  - **Issue**: No overloads for "get" match the provided arguments
  - **Location**: `haive-games/src/haive/games/debate/state_manager.py:271:33`

- [ ] **Line 272** (`reportArgumentType`)
  - **Issue**: Argument of type "str" cannot be assigned to parameter "key" of type "DebatePhase" in function "get"
      "str" is not assignable to "DebatePhase"
  - **Location**: `haive-games/src/haive/games/debate/state_manager.py:272:12`

### 📄 haive-games/src/haive/games/debate/test_topic_handling.py

- [ ] **Line 9** (`reportMissingImports`)
  - **Issue**: Import "haive.games.debate.input_schema" could not be resolved
  - **Location**: `haive-games/src/haive/games/debate/test_topic_handling.py:9:5`

### 📄 haive-games/src/haive/games/debate_v2/**init**.py

- [ ] **Line 3** (`reportAttributeAccessIssue`)
  - **Issue**: "DebateV2Agent" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/debate_v2/__init__.py:3:40`

- [ ] **Line 3** (`reportAttributeAccessIssue`)
  - **Issue**: "DebateV2AgentConfig" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/debate_v2/__init__.py:3:55`

- [ ] **Line 5** (`reportMissingImports`)
  - **Issue**: Import "haive.games.debate_v2.state" could not be resolved
  - **Location**: `haive-games/src/haive/games/debate_v2/__init__.py:5:5`

- [ ] **Line 6** (`reportMissingImports`)
  - **Issue**: Import "haive.games.debate_v2.state_manager" could not be resolved
  - **Location**: `haive-games/src/haive/games/debate_v2/__init__.py:6:5`

- [ ] **Line 7** (`reportMissingImports`)
  - **Issue**: Import "haive.games.debate_v2.ui" could not be resolved
  - **Location**: `haive-games/src/haive/games/debate_v2/__init__.py:7:5`

### 📄 haive-games/src/haive/games/debate_v2/agent.py

- [ ] **Line 474** (`reportOptionalMemberAccess`)
  - **Issue**: "update" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/debate_v2/agent.py:474:21`

### 📄 haive-games/src/haive/games/debate_v2/agent_with_judges.py

- [ ] **Line 134** (`reportOptionalSubscript`)
  - **Issue**: Object of type "None" is not subscriptable
  - **Location**: `haive-games/src/haive/games/debate_v2/agent_with_judges.py:134:20`

- [ ] **Line 135** (`reportOptionalSubscript`)
  - **Issue**: Object of type "None" is not subscriptable
  - **Location**: `haive-games/src/haive/games/debate_v2/agent_with_judges.py:135:20`

- [ ] **Line 139** (`reportOptionalSubscript`)
  - **Issue**: Object of type "None" is not subscriptable
  - **Location**: `haive-games/src/haive/games/debate_v2/agent_with_judges.py:139:20`

- [ ] **Line 140** (`reportOptionalSubscript`)
  - **Issue**: Object of type "None" is not subscriptable
  - **Location**: `haive-games/src/haive/games/debate_v2/agent_with_judges.py:140:20`

- [ ] **Line 144** (`reportOptionalSubscript`)
  - **Issue**: Object of type "None" is not subscriptable
  - **Location**: `haive-games/src/haive/games/debate_v2/agent_with_judges.py:144:16`

- [ ] **Line 153** (`reportGeneralTypeIssues`)
  - **Issue**: Expected mapping for dictionary unpack operator
  - **Location**: `haive-games/src/haive/games/debate_v2/agent_with_judges.py:153:12`

- [ ] **Line 171** (`reportOptionalMemberAccess`)
  - **Issue**: "judge_debate" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/debate_v2/agent_with_judges.py:171:44`

- [ ] **Line 364** (`reportReturnType`)
  - **Issue**: Type "GameDebateAgent" is not assignable to return type "JudgedGameDebateAgent"
      "GameDebateAgent" is not assignable to "JudgedGameDebateAgent"
  - **Location**: `haive-games/src/haive/games/debate_v2/agent_with_judges.py:364:15`

### 📄 haive-games/src/haive/games/debate_v2/example.py

- [ ] **Line 65** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run" for class "GameDebateAgent"
      Could not bind method "run" because "GameDebateAgent" is not assignable to parameter "self"
        "GameDebateAgent" is incompatible with protocol "AgentProtocol"
          "config" is not present
          "\_disable_checkpointing" is not present
            "input_schema" is invariant because it is mutable
            "input_schema" is an incompatible type
              Type "type[BaseModel] | dict[str, Any] | None" is not assignable to type "type[BaseModel] | None"
            "output_schema" is invariant because it is mutable
  - **Location**: `haive-games/src/haive/games/debate_v2/example.py:65:24`

- [ ] **Line 145** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run" for class "GameDebateAgent"
      Could not bind method "run" because "GameDebateAgent" is not assignable to parameter "self"
        "GameDebateAgent" is incompatible with protocol "AgentProtocol"
          "config" is not present
          "\_disable_checkpointing" is not present
            "input_schema" is invariant because it is mutable
            "input_schema" is an incompatible type
              Type "type[BaseModel] | dict[str, Any] | None" is not assignable to type "type[BaseModel] | None"
            "output_schema" is invariant because it is mutable
  - **Location**: `haive-games/src/haive/games/debate_v2/example.py:145:24`

- [ ] **Line 239** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run" for class "GameDebateAgent"
      Could not bind method "run" because "GameDebateAgent" is not assignable to parameter "self"
        "GameDebateAgent" is incompatible with protocol "AgentProtocol"
          "config" is not present
          "\_disable_checkpointing" is not present
            "input_schema" is invariant because it is mutable
            "input_schema" is an incompatible type
              Type "type[BaseModel] | dict[str, Any] | None" is not assignable to type "type[BaseModel] | None"
            "output_schema" is invariant because it is mutable
  - **Location**: `haive-games/src/haive/games/debate_v2/example.py:239:24`

### 📄 haive-games/src/haive/games/debate_v2/example_with_judges.py

- [ ] **Line 70** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "arun" for class "JudgedGameDebateAgent"
      Could not bind method "arun" because "JudgedGameDebateAgent" is not assignable to parameter "self"
        "JudgedGameDebateAgent" is incompatible with protocol "AgentProtocol"
          "config" is not present
          "\_disable_checkpointing" is not present
            "input_schema" is invariant because it is mutable
            "input_schema" is an incompatible type
              Type "type[BaseModel] | dict[str, Any] | None" is not assignable to type "type[BaseModel] | None"
            "output_schema" is invariant because it is mutable
  - **Location**: `haive-games/src/haive/games/debate_v2/example_with_judges.py:70:30`

- [ ] **Line 172** (`reportOperatorIssue`)
  - **Issue**: Operator "in" not supported for types "Literal['Ethics']" and "str | None"
      Operator "in" not supported for types "Literal['Ethics']" and "None"
  - **Location**: `haive-games/src/haive/games/debate_v2/example_with_judges.py:172:15`

- [ ] **Line 175** (`reportOperatorIssue`)
  - **Issue**: Operator "in" not supported for types "Literal['Policy']" and "str | None"
      Operator "in" not supported for types "Literal['Policy']" and "None"
  - **Location**: `haive-games/src/haive/games/debate_v2/example_with_judges.py:175:19`

### 📄 haive-games/src/haive/games/debate_v2/judges.py

- [ ] **Line 211** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "arun" for class "SimpleAgent"
      Could not bind method "arun" because "SimpleAgent" is not assignable to parameter "self"
        "SimpleAgent" is incompatible with protocol "AgentProtocol"
          "config" is not present
          "\_disable_checkpointing" is not present
            "input_schema" is invariant because it is mutable
            "input_schema" is an incompatible type
              Type "type[BaseModel] | dict[str, Any] | None" is not assignable to type "type[BaseModel] | None"
            "output_schema" is invariant because it is mutable
  - **Location**: `haive-games/src/haive/games/debate_v2/judges.py:211:40`

### 📄 haive-games/src/haive/games/dominoes/agent.py

- [ ] **Line 257** (`reportReturnType`)
  - **Issue**: Type "DominoMove | None" is not assignable to return type "DominoMove | Literal['pass']"
      Type "DominoMove | None" is not assignable to type "DominoMove | Literal['pass']"
        Type "None" is not assignable to type "DominoMove | Literal['pass']"
          "None" is not assignable to "DominoMove"
          "None" is not assignable to "Literal['pass']"
  - **Location**: `haive-games/src/haive/games/dominoes/agent.py:257:19`

- [ ] **Line 264** (`reportReturnType`)
  - **Issue**: Type "DominoMove | None" is not assignable to return type "DominoMove | Literal['pass']"
      Type "DominoMove | None" is not assignable to type "DominoMove | Literal['pass']"
        Type "None" is not assignable to type "DominoMove | Literal['pass']"
          "None" is not assignable to "DominoMove"
          "None" is not assignable to "Literal['pass']"
  - **Location**: `haive-games/src/haive/games/dominoes/agent.py:264:23`

- [ ] **Line 270** (`reportReturnType`)
  - **Issue**: Type "DominoMove | None" is not assignable to return type "DominoMove | Literal['pass']"
      Type "DominoMove | None" is not assignable to type "DominoMove | Literal['pass']"
        Type "None" is not assignable to type "DominoMove | Literal['pass']"
          "None" is not assignable to "DominoMove"
          "None" is not assignable to "Literal['pass']"
  - **Location**: `haive-games/src/haive/games/dominoes/agent.py:270:27`

- [ ] **Line 282** (`reportReturnType`)
  - **Issue**: Type "DominoMove | None" is not assignable to return type "DominoMove | Literal['pass']"
      Type "DominoMove | None" is not assignable to type "DominoMove | Literal['pass']"
        Type "None" is not assignable to type "DominoMove | Literal['pass']"
          "None" is not assignable to "DominoMove"
          "None" is not assignable to "Literal['pass']"
  - **Location**: `haive-games/src/haive/games/dominoes/agent.py:282:27`

- [ ] **Line 291** (`reportReturnType`)
  - **Issue**: Type "DominoMove | None" is not assignable to return type "DominoMove | Literal['pass']"
      Type "DominoMove | None" is not assignable to type "DominoMove | Literal['pass']"
        Type "None" is not assignable to type "DominoMove | Literal['pass']"
          "None" is not assignable to "DominoMove"
          "None" is not assignable to "Literal['pass']"
  - **Location**: `haive-games/src/haive/games/dominoes/agent.py:291:27`

- [ ] **Line 309** (`reportReturnType`)
  - **Issue**: Type "DominoMove | None" is not assignable to return type "DominoMove | Literal['pass']"
      Type "DominoMove | None" is not assignable to type "DominoMove | Literal['pass']"
        Type "None" is not assignable to type "DominoMove | Literal['pass']"
          "None" is not assignable to "DominoMove"
          "None" is not assignable to "Literal['pass']"
  - **Location**: `haive-games/src/haive/games/dominoes/agent.py:309:31`

- [ ] **Line 322** (`reportReturnType`)
  - **Issue**: Type "DominoMove | None" is not assignable to return type "DominoMove | Literal['pass']"
      Type "DominoMove | None" is not assignable to type "DominoMove | Literal['pass']"
        Type "None" is not assignable to type "DominoMove | Literal['pass']"
          "None" is not assignable to "DominoMove"
          "None" is not assignable to "Literal['pass']"
  - **Location**: `haive-games/src/haive/games/dominoes/agent.py:322:23`

- [ ] **Line 717** (`reportReturnType`)
  - **Issue**: Type "DominoesState" is not assignable to return type "dict[str, Any]"
      "DominoesState" is not assignable to "dict[str, Any]"
  - **Location**: `haive-games/src/haive/games/dominoes/agent.py:717:15`

- [ ] **Line 756** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[bool, str]" cannot be assigned to parameter "routes" of type "dict[str, str]" in function "add_conditional_edges"
      "Literal[True]" is not assignable to "str"
      "Literal[False]" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/dominoes/agent.py:756:12`

- [ ] **Line 762** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[bool, str]" cannot be assigned to parameter "routes" of type "dict[str, str]" in function "add_conditional_edges"
      "Literal[True]" is not assignable to "str"
      "Literal[False]" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/dominoes/agent.py:762:12`

- [ ] **Line 777** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "config"
  - **Location**: `haive-games/src/haive/games/dominoes/agent.py:777:12`

- [ ] **Line 778** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_game" for class "Agent[Unknown]"
      Attribute "run_game" is unknown
  - **Location**: `haive-games/src/haive/games/dominoes/agent.py:778:10`

### 📄 haive-games/src/haive/games/dominoes/enhanced_example.py

- [ ] **Line 62** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_game_with_ui" for class "DominoesUI"
      Attribute "run_game_with_ui" is unknown
  - **Location**: `haive-games/src/haive/games/dominoes/enhanced_example.py:62:29`

- [ ] **Line 65** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_game_with_ui" for class "Agent[Unknown]"
      Attribute "run_game_with_ui" is unknown
  - **Location**: `haive-games/src/haive/games/dominoes/enhanced_example.py:65:32`

### 📄 haive-games/src/haive/games/dominoes/example.py

- [ ] **Line 36** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_game_with_ui" for class "Agent[Unknown]"
      Attribute "run_game_with_ui" is unknown
  - **Location**: `haive-games/src/haive/games/dominoes/example.py:36:28`

### 📄 haive-games/src/haive/games/dominoes/generic_engines.py

- [ ] **Line 101** (`reportAbstractUsage`)
  - **Issue**: Cannot instantiate abstract class "DominoesPromptGenerator"
      "GenericPromptGenerator.create_analysis_prompt" is not implemented
      "GenericPromptGenerator.get_move_output_model" is not implemented
      and 1 more...
  - **Location**: `haive-games/src/haive/games/dominoes/generic_engines.py:101:27`

- [ ] **Line 101** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "players"
  - **Location**: `haive-games/src/haive/games/dominoes/generic_engines.py:101:27`

- [ ] **Line 133** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "create_engines" for class "DominoesEngineFactory"
      Attribute "create_engines" is unknown
  - **Location**: `haive-games/src/haive/games/dominoes/generic_engines.py:133:28`

### 📄 haive-games/src/haive/games/dominoes/rich_ui.py

- [ ] **Line 791** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "tile" for class "str"
      Attribute "tile" is unknown
  - **Location**: `haive-games/src/haive/games/dominoes/rich_ui.py:791:32`

- [ ] **Line 791** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "tile" for class "str"
      Attribute "tile" is unknown
  - **Location**: `haive-games/src/haive/games/dominoes/rich_ui.py:791:49`

- [ ] **Line 792** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "tile" for class "str"
      Attribute "tile" is unknown
  - **Location**: `haive-games/src/haive/games/dominoes/rich_ui.py:792:20`

- [ ] **Line 798** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "location" for class "str"
      Attribute "location" is unknown
  - **Location**: `haive-games/src/haive/games/dominoes/rich_ui.py:798:84`

### 📄 haive-games/src/haive/games/dominoes/state.py

- [ ] **Line 190** (`reportGeneralTypeIssues`)
  - **Issue**: "players" overrides a field of the same name but is missing a default value
  - **Location**: `haive-games/src/haive/games/dominoes/state.py:190:4`

- [ ] **Line 190** (`reportCallIssue`)
  - **Issue**: No overloads for "Field" match the provided arguments
      Argument types: (EllipsisType, Literal[2], Literal[4], Literal['List of player names in turn order (2-4 players su…'])
  - **Location**: `haive-games/src/haive/games/dominoes/state.py:190:25`

- [ ] **Line 207** (`reportGeneralTypeIssues`)
  - **Issue**: "turn" overrides a field of the same name but is missing a default value
  - **Location**: `haive-games/src/haive/games/dominoes/state.py:207:4`

### 📄 haive-games/src/haive/games/dominoes/state_manager.py

- [ ] **Line 20** (`reportArgumentType`)
  - **Issue**: Expression of type "None" cannot be assigned to parameter of type "list[str]"
      "None" is not assignable to "list[str]"
  - **Location**: `haive-games/src/haive/games/dominoes/state_manager.py:20:39`

- [ ] **Line 160** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "game_status" for class "DominoesState"
      Type "str" is not assignable to type "Literal['ongoing', 'player1_win', 'player2_win', 'draw']"
        "str" is not assignable to type "Literal['ongoing']"
        "str" is not assignable to type "Literal['player1_win']"
        "str" is not assignable to type "Literal['player2_win']"
        "str" is not assignable to type "Literal['draw']"
  - **Location**: `haive-games/src/haive/games/dominoes/state_manager.py:160:36`

- [ ] **Line 195** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "game_status" for class "DominoesState"
      Type "str" is not assignable to type "Literal['ongoing', 'player1_win', 'player2_win', 'draw']"
        "str" is not assignable to type "Literal['ongoing']"
        "str" is not assignable to type "Literal['player1_win']"
        "str" is not assignable to type "Literal['player2_win']"
        "str" is not assignable to type "Literal['draw']"
  - **Location**: `haive-games/src/haive/games/dominoes/state_manager.py:195:36`

- [ ] **Line 216** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "game_status" for class "DominoesState"
      Type "str" is not assignable to type "Literal['ongoing', 'player1_win', 'player2_win', 'draw']"
        "str" is not assignable to type "Literal['ongoing']"
        "str" is not assignable to type "Literal['player1_win']"
        "str" is not assignable to type "Literal['player2_win']"
        "str" is not assignable to type "Literal['draw']"
  - **Location**: `haive-games/src/haive/games/dominoes/state_manager.py:216:36`

### 📄 haive-games/src/haive/games/dominoes/ui.py

- [ ] **Line 306** (`reportArgumentType`)
  - **Issue**: Argument of type "None" cannot be assigned to parameter "renderable" of type "RenderableType" in function "**init**"
      Type "None" is not assignable to type "RenderableType"
        "None" is incompatible with protocol "ConsoleRenderable"
          "**rich_console**" is not present
        "None" is incompatible with protocol "RichCast"
          "**rich**" is not present
        "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/dominoes/ui.py:306:12`

- [ ] **Line 576** (`reportCallIssue`)
  - **Issue**: No overloads for "get" match the provided arguments
  - **Location**: `haive-games/src/haive/games/dominoes/ui.py:576:47`

- [ ] **Line 576** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "key" of type "str" in function "get"
      Type "str | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/dominoes/ui.py:576:69`

### 📄 haive-games/src/haive/games/example.py

- [ ] **Line 19** (`reportAttributeAccessIssue`)
  - **Issue**: "GameAgent" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/example.py:19:34`

- [ ] **Line 19** (`reportAttributeAccessIssue`)
  - **Issue**: "GameConfig" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/example.py:19:45`

- [ ] **Line 19** (`reportAttributeAccessIssue`)
  - **Issue**: "GameState" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/example.py:19:57`

- [ ] **Line 19** (`reportAttributeAccessIssue`)
  - **Issue**: "GameStateManager" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/example.py:19:68`

- [ ] **Line 21** (`reportAttributeAccessIssue`)
  - **Issue**: "PokerConfig" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/example.py:21:37`

- [ ] **Line 22** (`reportAttributeAccessIssue`)
  - **Issue**: "WordleAgent" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/example.py:22:51`

- [ ] **Line 23** (`reportAttributeAccessIssue`)
  - **Issue**: "WordleConfig" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/example.py:23:52`

- [ ] **Line 26** (`reportMissingImports`)
  - **Issue**: Import "haive.games.utils.observers" could not be resolved
  - **Location**: `haive-games/src/haive/games/example.py:26:5`

- [ ] **Line 37** (`reportCallIssue`)
  - **Issue**: No parameter named "player_names"
  - **Location**: `haive-games/src/haive/games/example.py:37:8`

- [ ] **Line 38** (`reportCallIssue`)
  - **Issue**: No parameter named "llm_config"
  - **Location**: `haive-games/src/haive/games/example.py:38:8`

- [ ] **Line 46** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "input_data"
  - **Location**: `haive-games/src/haive/games/example.py:46:4`

- [ ] **Line 72** (`reportCallIssue`)
  - **Issue**: No parameter named "white_engine"
  - **Location**: `haive-games/src/haive/games/example.py:72:8`

- [ ] **Line 73** (`reportCallIssue`)
  - **Issue**: No parameter named "black_engine"
  - **Location**: `haive-games/src/haive/games/example.py:73:8`

- [ ] **Line 74** (`reportCallIssue`)
  - **Issue**: No parameter named "time_limit"
  - **Location**: `haive-games/src/haive/games/example.py:74:8`

- [ ] **Line 79** (`reportUndefinedVariable`)
  - **Issue**: "ChessAgent" is not defined
  - **Location**: `haive-games/src/haive/games/example.py:79:11`

- [ ] **Line 124** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "input_data"
  - **Location**: `haive-games/src/haive/games/example.py:124:19`

- [ ] **Line 246** (`reportCallIssue`)
  - **Issue**: No parameter named "player_names"
  - **Location**: `haive-games/src/haive/games/example.py:246:12`

- [ ] **Line 247** (`reportCallIssue`)
  - **Issue**: No parameter named "player1_engine"
  - **Location**: `haive-games/src/haive/games/example.py:247:12`

- [ ] **Line 248** (`reportCallIssue`)
  - **Issue**: No parameter named "player2_engine"
  - **Location**: `haive-games/src/haive/games/example.py:248:12`

- [ ] **Line 256** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "input_data"
  - **Location**: `haive-games/src/haive/games/example.py:256:21`

- [ ] **Line 365** (`reportCallIssue`)
  - **Issue**: No parameter named "player_names"
  - **Location**: `haive-games/src/haive/games/example.py:365:29`

- [ ] **Line 369** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_observer" for class "Agent[Unknown]"
      Attribute "add_observer" is unknown
  - **Location**: `haive-games/src/haive/games/example.py:369:9`

- [ ] **Line 370** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_observer" for class "Agent[Unknown]"
      Attribute "add_observer" is unknown
  - **Location**: `haive-games/src/haive/games/example.py:370:9`

- [ ] **Line 371** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_observer" for class "Agent[Unknown]"
      Attribute "add_observer" is unknown
  - **Location**: `haive-games/src/haive/games/example.py:371:9`

- [ ] **Line 374** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "input_data"
  - **Location**: `haive-games/src/haive/games/example.py:374:4`

- [ ] **Line 383** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "input_data"
  - **Location**: `haive-games/src/haive/games/example.py:383:23`

- [ ] **Line 391** (`reportCallIssue`)
  - **Issue**: No parameter named "player_names"
  - **Location**: `haive-games/src/haive/games/example.py:391:16`

- [ ] **Line 392** (`reportCallIssue`)
  - **Issue**: No parameter named "llm_config"
  - **Location**: `haive-games/src/haive/games/example.py:392:16`

- [ ] **Line 412** (`reportCallIssue`)
  - **Issue**: No parameter named "player_names"
  - **Location**: `haive-games/src/haive/games/example.py:412:25`

- [ ] **Line 413** (`reportUndefinedVariable`)
  - **Issue**: "ChessAgent" is not defined
  - **Location**: `haive-games/src/haive/games/example.py:413:11`

- [ ] **Line 439** (`reportUndefinedVariable`)
  - **Issue**: "ChessAgent" is not defined
  - **Location**: `haive-games/src/haive/games/example.py:439:18`

### 📄 haive-games/src/haive/games/fox_and_geese/agent.py

- [ ] **Line 67** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state" for class "<subclass of dict[str, Any] and Command>"
      Attribute "state" is unknown
  - **Location**: `haive-games/src/haive/games/fox_and_geese/agent.py:67:57`

- [ ] **Line 68** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state" for class "<subclass of dict[str, Any] and Command>"
      Attribute "state" is unknown
  - **Location**: `haive-games/src/haive/games/fox_and_geese/agent.py:68:49`

- [ ] **Line 147** (`reportReturnType`)
  - **Issue**: Type "Command[Unknown]" is not assignable to return type "dict[str, Any]"
      "Command[Unknown]" is not assignable to "dict[str, Any]"
  - **Location**: `haive-games/src/haive/games/fox_and_geese/agent.py:147:15`

- [ ] **Line 286** (`reportArgumentType`)
  - **Issue**: Argument of type "str" cannot be assigned to parameter "piece_type" of type "Literal['fox', 'goose']" in function "**init**"
      Type "str" is not assignable to type "Literal['fox', 'goose']"
        "str" is not assignable to type "Literal['fox']"
        "str" is not assignable to type "Literal['goose']"
  - **Location**: `haive-games/src/haive/games/fox_and_geese/agent.py:286:39`

- [ ] **Line 840** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[bool, str]" cannot be assigned to parameter "routes" of type "dict[str, str]" in function "add_conditional_edges"
      "Literal[True]" is not assignable to "str"
      "Literal[False]" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/fox_and_geese/agent.py:840:16`

- [ ] **Line 848** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[bool, str]" cannot be assigned to parameter "routes" of type "dict[str, str]" in function "add_conditional_edges"
      "Literal[True]" is not assignable to "str"
      "Literal[False]" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/fox_and_geese/agent.py:848:16`

- [ ] **Line 857** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[bool, str]" cannot be assigned to parameter "routes" of type "dict[str, str]" in function "add_conditional_edges"
      "Literal[True]" is not assignable to "str"
      "Literal[False]" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/fox_and_geese/agent.py:857:16`

- [ ] **Line 863** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[bool, str]" cannot be assigned to parameter "routes" of type "dict[str, str]" in function "add_conditional_edges"
      "Literal[True]" is not assignable to "str"
      "Literal[False]" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/fox_and_geese/agent.py:863:16`

- [ ] **Line 910** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "recursion_limit" for class "GameConfig"
      Attribute "recursion_limit" is unknown
  - **Location**: `haive-games/src/haive/games/fox_and_geese/agent.py:910:64`

- [ ] **Line 986** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "recursion_limit" for class "GameConfig"
      Attribute "recursion_limit" is unknown
  - **Location**: `haive-games/src/haive/games/fox_and_geese/agent.py:986:60`

- [ ] **Line 1023** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "visualize_state" for class "FoxAndGeeseAgent\*"
      Attribute "visualize_state" is unknown
  - **Location**: `haive-games/src/haive/games/fox_and_geese/agent.py:1023:25`

- [ ] **Line 1081** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, dict[str, Unknown]]" cannot be assigned to parameter "config" of type "RunnableConfig | None" in function "stream"
      Type "dict[str, dict[str, Unknown]]" is not assignable to type "RunnableConfig | None"
        "dict[str, dict[str, Unknown]]" is not assignable to "RunnableConfig"
        "dict[str, dict[str, Unknown]]" is not assignable to "None"
  - **Location**: `haive-games/src/haive/games/fox_and_geese/agent.py:1081:38`

- [ ] **Line 1113** (`reportReturnType`)
  - **Issue**: Type "dict[str, Any] | <subclass of dict[str, Any] and FoxAndGeeseState> | FoxAndGeeseState" is not assignable to return type "dict[str, Any]"
      Type "dict[str, Any] | <subclass of dict[str, Any] and FoxAndGeeseState> | FoxAndGeeseState" is not assignable to type "dict[str, Any]"
        "FoxAndGeeseState" is not assignable to "dict[str, Any]"
  - **Location**: `haive-games/src/haive/games/fox_and_geese/agent.py:1113:19`

- [ ] **Line 1123** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "game_status" for class "FoxAndGeeseState"
      Type "Literal['ended']" is not assignable to type "Literal['ongoing', 'fox_win', 'geese_win']"
        "Literal['ended']" is not assignable to type "Literal['ongoing']"
        "Literal['ended']" is not assignable to type "Literal['fox_win']"
        "Literal['ended']" is not assignable to type "Literal['geese_win']"
  - **Location**: `haive-games/src/haive/games/fox_and_geese/agent.py:1123:38`

### 📄 haive-games/src/haive/games/fox_and_geese/enhanced_example.py

- [ ] **Line 61** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_fox_and_geese_game" for class "FoxAndGeeseUI"
      Attribute "run_fox_and_geese_game" is unknown
  - **Location**: `haive-games/src/haive/games/fox_and_geese/enhanced_example.py:61:29`

- [ ] **Line 65** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "ui" for class "Agent[Unknown]"
      Attribute "ui" is unknown
  - **Location**: `haive-games/src/haive/games/fox_and_geese/enhanced_example.py:65:22`

- [ ] **Line 66** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_game_with_ui" for class "Agent[Unknown]"
      Attribute "run_game_with_ui" is unknown
  - **Location**: `haive-games/src/haive/games/fox_and_geese/enhanced_example.py:66:32`

- [ ] **Line 200** (`reportArgumentType`)
  - **Issue**: Argument of type "FoxAndGeesePosition | None" cannot be assigned to parameter "element" of type "FoxAndGeesePosition" in function "remove"
      Type "FoxAndGeesePosition | None" is not assignable to type "FoxAndGeesePosition"
        "None" is not assignable to "FoxAndGeesePosition"
  - **Location**: `haive-games/src/haive/games/fox_and_geese/enhanced_example.py:200:42`

- [ ] **Line 259** (`reportUnboundVariable`)
  - **Issue**: "traceback" is unbound
  - **Location**: `haive-games/src/haive/games/fox_and_geese/enhanced_example.py:259:16`

- [ ] **Line 259** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "print_exc" for class "Unbound"
  - **Location**: `haive-games/src/haive/games/fox_and_geese/enhanced_example.py:259:26`

### 📄 haive-games/src/haive/games/fox_and_geese/example.py

- [ ] **Line 27** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "Agent[Unknown]"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/fox_and_geese/example.py:27:26`

- [ ] **Line 102** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_game_with_ui" for class "Agent[Unknown]"
      Attribute "run_game_with_ui" is unknown
  - **Location**: `haive-games/src/haive/games/fox_and_geese/example.py:102:28`

### 📄 haive-games/src/haive/games/fox_and_geese/fixed_runner.py

- [ ] **Line 53** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "FixedFoxAndGeeseAgent\*"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/fox_and_geese/fixed_runner.py:53:21`

- [ ] **Line 69** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "analyze_player1" for class "FixedFoxAndGeeseAgent\*"
      Attribute "analyze_player1" is unknown
  - **Location**: `haive-games/src/haive/games/fox_and_geese/fixed_runner.py:69:48`

- [ ] **Line 83** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "make_fox_move" for class "FixedFoxAndGeeseAgent\*"
      Attribute "make_fox_move" is unknown
  - **Location**: `haive-games/src/haive/games/fox_and_geese/fixed_runner.py:83:37`

- [ ] **Line 90** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "analyze_player2" for class "FixedFoxAndGeeseAgent\*"
      Attribute "analyze_player2" is unknown
  - **Location**: `haive-games/src/haive/games/fox_and_geese/fixed_runner.py:90:48`

- [ ] **Line 104** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "make_geese_move" for class "FixedFoxAndGeeseAgent\*"
      Attribute "make_geese_move" is unknown
  - **Location**: `haive-games/src/haive/games/fox_and_geese/fixed_runner.py:104:37`

- [ ] **Line 176** (`reportAbstractUsage`)
  - **Issue**: Cannot instantiate abstract class "FixedFoxAndGeeseAgent"
      "Agent.setup_workflow" is not implemented
  - **Location**: `haive-games/src/haive/games/fox_and_geese/fixed_runner.py:176:16`

### 📄 haive-games/src/haive/games/fox_and_geese/generic_engines.py

- [ ] **Line 101** (`reportAbstractUsage`)
  - **Issue**: Cannot instantiate abstract class "FoxAndGeesePromptGenerator"
      "GenericPromptGenerator.create_analysis_prompt" is not implemented
      "GenericPromptGenerator.get_move_output_model" is not implemented
      and 1 more...
  - **Location**: `haive-games/src/haive/games/fox_and_geese/generic_engines.py:101:27`

- [ ] **Line 101** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "players"
  - **Location**: `haive-games/src/haive/games/fox_and_geese/generic_engines.py:101:27`

- [ ] **Line 134** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "create_engines" for class "FoxAndGeeseEngineFactory"
      Attribute "create_engines" is unknown
  - **Location**: `haive-games/src/haive/games/fox_and_geese/generic_engines.py:134:33`

### 📄 haive-games/src/haive/games/fox_and_geese/state.py

- [ ] **Line 196** (`reportGeneralTypeIssues`)
  - **Issue**: "turn" overrides a field of the same name but is missing a default value
  - **Location**: `haive-games/src/haive/games/fox_and_geese/state.py:196:4`

### 📄 haive-games/src/haive/games/framework/base/agent.py

- [ ] **Line 92** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/framework/base/agent.py:92:19`

- [ ] **Line 93** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/framework/base/agent.py:93:19`

- [ ] **Line 94** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/framework/base/agent.py:94:19`

- [ ] **Line 97** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/framework/base/agent.py:97:19`

- [ ] **Line 101** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/framework/base/agent.py:101:23`

- [ ] **Line 102** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/framework/base/agent.py:102:23`

- [ ] **Line 105** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/framework/base/agent.py:105:23`

- [ ] **Line 106** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/framework/base/agent.py:106:23`

- [ ] **Line 108** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/framework/base/agent.py:108:23`

- [ ] **Line 114** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/framework/base/agent.py:114:23`

- [ ] **Line 116** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/framework/base/agent.py:116:23`

- [ ] **Line 123** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/framework/base/agent.py:123:23`

- [ ] **Line 125** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/framework/base/agent.py:125:23`

- [ ] **Line 131** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/framework/base/agent.py:131:23`

- [ ] **Line 152** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "GameAgent[T@GameAgent]\*"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/framework/base/agent.py:152:26`

- [ ] **Line 200** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "GameAgent[T@GameAgent]\*"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/framework/base/agent.py:200:29`

- [ ] **Line 274** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "game_status" for class "BaseModel\*"
      Attribute "game_status" is unknown
  - **Location**: `haive-games/src/haive/games/framework/base/agent.py:274:21`

- [ ] **Line 502** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "visualize_state" for class "GameAgent[Unknown]"
      Attribute "visualize_state" is unknown
  - **Location**: `haive-games/src/haive/games/framework/base/agent.py:502:14`

### 📄 haive-games/src/haive/games/framework/base/factory.py

- [ ] **Line 137** (`reportCallIssue`)
  - **Issue**: No parameter named "state_schema"
  - **Location**: `haive-games/src/haive/games/framework/base/factory.py:137:24`

- [ ] **Line 138** (`reportCallIssue`)
  - **Issue**: No parameter named "aug_llm_configs"
  - **Location**: `haive-games/src/haive/games/framework/base/factory.py:138:24`

- [ ] **Line 139** (`reportCallIssue`)
  - **Issue**: No parameter named "enable_analysis"
  - **Location**: `haive-games/src/haive/games/framework/base/factory.py:139:24`

- [ ] **Line 140** (`reportCallIssue`)
  - **Issue**: No parameter named "visualize"
  - **Location**: `haive-games/src/haive/games/framework/base/factory.py:140:24`

- [ ] **Line 190** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_conditional_edge" for class "DynamicGraph"
      Attribute "add_conditional_edge" is unknown
  - **Location**: `haive-games/src/haive/games/framework/base/factory.py:190:30`

- [ ] **Line 198** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_conditional_edge" for class "DynamicGraph"
      Attribute "add_conditional_edge" is unknown
  - **Location**: `haive-games/src/haive/games/framework/base/factory.py:198:30`

- [ ] **Line 208** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_conditional_edge" for class "DynamicGraph"
      Attribute "add_conditional_edge" is unknown
  - **Location**: `haive-games/src/haive/games/framework/base/factory.py:208:30`

- [ ] **Line 214** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_conditional_edge" for class "DynamicGraph"
      Attribute "add_conditional_edge" is unknown
  - **Location**: `haive-games/src/haive/games/framework/base/factory.py:214:30`

- [ ] **Line 228** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "add_conditional_edge" for class "DynamicGraph"
      Attribute "add_conditional_edge" is unknown
  - **Location**: `haive-games/src/haive/games/framework/base/factory.py:228:34`

### 📄 haive-games/src/haive/games/framework/base/template_generator.py

- [ ] **Line 98** (`reportArgumentType`)
  - **Issue**: Expression of type "None" cannot be assigned to parameter of type "str"
      "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/framework/base/template_generator.py:98:51`

### 📄 haive-games/src/haive/games/framework/base/utils.py

- [ ] **Line 23** (`reportUndefinedVariable`)
  - **Issue**: "GameAgent" is not defined
  - **Location**: `haive-games/src/haive/games/framework/base/utils.py:23:21`

### 📄 haive-games/src/haive/games/framework/core/agent.py

- [ ] **Line 7** (`reportGeneralTypeIssues`)
  - **Issue**: "engines" overrides a field of the same name but is missing a default value
  - **Location**: `haive-games/src/haive/games/framework/core/agent.py:7:4`

- [ ] **Line 14** (`reportCallIssue`)
  - **Issue**: Expected 0 positional arguments
  - **Location**: `haive-games/src/haive/games/framework/core/agent.py:14:25`

- [ ] **Line 15** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "engines" for class "BasePlayerAgent\*"
      "dict[str, Engine[Unknown, Unknown] | str]" is not assignable to "dict[str, AugLLMConfig]"
        Type parameter "\_VT@dict" is invariant, but "Engine[Unknown, Unknown] | str" is not the same as "AugLLMConfig"
        Consider switching from "dict" to "Mapping" which is covariant in the value type
  - **Location**: `haive-games/src/haive/games/framework/core/agent.py:15:23`

- [ ] **Line 16** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "graph" for class "AgentConfig[Unknown, Unknown, Unknown]"
      Attribute "graph" is unknown
  - **Location**: `haive-games/src/haive/games/framework/core/agent.py:16:28`

### 📄 haive-games/src/haive/games/framework/core/container.py

- [ ] **Line 9** (`reportMissingImports`)
  - **Issue**: Import "game_framework.core.piece" could not be resolved
  - **Location**: `haive-games/src/haive/games/framework/core/container.py:9:5`

### 📄 haive-games/src/haive/games/framework/core/containers/deck.py

- [ ] **Line 10** (`reportMissingImports`)
  - **Issue**: Import "haive.games.framework.pieces.card" could not be resolved
  - **Location**: `haive-games/src/haive/games/framework/core/containers/deck.py:10:5`

### 📄 haive-games/src/haive/games/framework/multi_player/agent.py

- [ ] **Line 154** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[bool, str]" cannot be assigned to parameter "routes" of type "dict[str, str]" in function "add_conditional_edges"
      "Literal[True]" is not assignable to "str"
      "Literal[False]" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:154:12`

- [ ] **Line 173** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[bool, str]" cannot be assigned to parameter "routes" of type "dict[str, str]" in function "add_conditional_edges"
      "Literal[True]" is not assignable to "str"
      "Literal[False]" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:173:12`

- [ ] **Line 182** (`reportRedeclaration`)
  - **Issue**: Method declaration "get_player_role" is obscured by a declaration of the same name
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:182:8`

- [ ] **Line 208** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "roles" for class "MultiPlayerGameState"
      Attribute "roles" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:208:30`

- [ ] **Line 209** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "roles" for class "MultiPlayerGameState"
      Attribute "roles" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:209:25`

- [ ] **Line 213** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "roles" for class "MultiPlayerGameState"
      Attribute "roles" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:213:40`

- [ ] **Line 214** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "roles" for class "MultiPlayerGameState"
      Attribute "roles" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:214:25`

- [ ] **Line 259** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "roles" for class "MultiPlayerGameState"
      Attribute "roles" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:259:41`

- [ ] **Line 263** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player_states" for class "MultiPlayerGameState"
      Attribute "player_states" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:263:25`

- [ ] **Line 269** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "action_history" for class "MultiPlayerGameState"
      Attribute "action_history" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:269:49`

- [ ] **Line 291** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player_states" for class "MultiPlayerGameState"
      Attribute "player_states" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:291:46`

- [ ] **Line 293** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "votes" for class "MultiPlayerGameState"
      Attribute "votes" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:293:25`

- [ ] **Line 301** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "roles" for class "MultiPlayerGameState"
      Attribute "roles" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:301:35`

- [ ] **Line 302** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "roles" for class "MultiPlayerGameState"
      Attribute "roles" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:302:40`

- [ ] **Line 304** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "roles" for class "MultiPlayerGameState"
      Attribute "roles" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:304:45`

- [ ] **Line 305** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "roles" for class "MultiPlayerGameState"
      Attribute "roles" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:305:40`

- [ ] **Line 317** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "action_history" for class "MultiPlayerGameState"
      Attribute "action_history" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:317:45`

- [ ] **Line 326** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player_states" for class "MultiPlayerGameState"
      Attribute "player_states" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:326:38`

- [ ] **Line 388** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "MultiPlayerGameAgent[T@MultiPlayerGameAgent]\*"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:388:29`

- [ ] **Line 440** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "MultiPlayerGameAgent[T@MultiPlayerGameAgent]\*"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:440:20`

- [ ] **Line 449** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "players" for class "BaseModel"
      Attribute "players" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:449:49`

- [ ] **Line 451** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "players" for class "BaseModel"
      Attribute "players" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:451:32`

- [ ] **Line 461** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "MultiPlayerGameAgent[T@MultiPlayerGameAgent]\*"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:461:26`

- [ ] **Line 481** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "MultiPlayerGameAgent[T@MultiPlayerGameAgent]\*"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:481:29`

- [ ] **Line 541** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "current_player" for class "BaseModel\*"
      Attribute "current_player" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:541:26`

- [ ] **Line 555** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "MultiPlayerGameAgent[T@MultiPlayerGameAgent]\*"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:555:17`

- [ ] **Line 565** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "MultiPlayerGameAgent[T@MultiPlayerGameAgent]\*"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:565:29`

- [ ] **Line 568** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "MultiPlayerGameAgent[T@MultiPlayerGameAgent]\*"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:568:29`

- [ ] **Line 593** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "MultiPlayerGameAgent[T@MultiPlayerGameAgent]\*"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:593:29`

- [ ] **Line 596** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "MultiPlayerGameAgent[T@MultiPlayerGameAgent]\*"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:596:29`

- [ ] **Line 639** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "game_status" for class "BaseModel\*"
      Attribute "game_status" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:639:21`

- [ ] **Line 652** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "game_status" for class "BaseModel\*"
      Attribute "game_status" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:652:21`

- [ ] **Line 666** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "current_player_idx" for class "BaseModel\*"
      Attribute "current_player_idx" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:666:21`

- [ ] **Line 666** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "round_number" for class "BaseModel\*"
      Attribute "round_number" is unknown
  - **Location**: `haive-games/src/haive/games/framework/multi_player/agent.py:666:55`

### 📄 haive-games/src/haive/games/framework/multi_player/config.py

- [ ] **Line 65** (`reportGeneralTypeIssues`)
  - **Issue**: "state_schema" overrides a field of the same name but is missing a default value
  - **Location**: `haive-games/src/haive/games/framework/multi_player/config.py:65:4`

- [ ] **Line 71** (`reportGeneralTypeIssues`)
  - **Issue**: "engines" overrides a field of the same name but is missing a default value
  - **Location**: `haive-games/src/haive/games/framework/multi_player/config.py:71:4`

### 📄 haive-games/src/haive/games/framework/multi_player/factory.py

- [ ] **Line 69** (`reportArgumentType`)
  - **Issue**: Expression of type "None" cannot be assigned to parameter of type "dict[str, (...) -> Unknown]"
      "None" is not assignable to "dict[str, (...) -> Unknown]"
  - **Location**: `haive-games/src/haive/games/framework/multi_player/factory.py:69:46`

- [ ] **Line 118** (`reportCallIssue`)
  - **Issue**: No parameter named "state_schema"
  - **Location**: `haive-games/src/haive/games/framework/multi_player/factory.py:118:24`

- [ ] **Line 119** (`reportCallIssue`)
  - **Issue**: No parameter named "aug_llm_configs"
  - **Location**: `haive-games/src/haive/games/framework/multi_player/factory.py:119:24`

- [ ] **Line 120** (`reportCallIssue`)
  - **Issue**: No parameter named "player_roles"
  - **Location**: `haive-games/src/haive/games/framework/multi_player/factory.py:120:24`

- [ ] **Line 121** (`reportCallIssue`)
  - **Issue**: No parameter named "visualize"
  - **Location**: `haive-games/src/haive/games/framework/multi_player/factory.py:121:24`

### 📄 haive-games/src/haive/games/go/agent.py

- [ ] **Line 85** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/go/agent.py:85:19`

- [ ] **Line 86** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/go/agent.py:86:19`

- [ ] **Line 87** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/go/agent.py:87:19`

- [ ] **Line 88** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/go/agent.py:88:19`

- [ ] **Line 89** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/go/agent.py:89:19`

- [ ] **Line 90** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/go/agent.py:90:19`

- [ ] **Line 93** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/go/agent.py:93:19`

- [ ] **Line 94** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/go/agent.py:94:19`

- [ ] **Line 98** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/go/agent.py:98:23`

- [ ] **Line 99** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/go/agent.py:99:23`

- [ ] **Line 105** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/go/agent.py:105:23`

- [ ] **Line 106** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/go/agent.py:106:23`

- [ ] **Line 112** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/go/agent.py:112:23`

- [ ] **Line 117** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/go/agent.py:117:23`

- [ ] **Line 167** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "black_analysis" for class "GoGameState"
      Attribute "black_analysis" is unknown
  - **Location**: `haive-games/src/haive/games/go/agent.py:167:26`

- [ ] **Line 168** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "black_analysis" for class "GoGameState"
      Attribute "black_analysis" is unknown
  - **Location**: `haive-games/src/haive/games/go/agent.py:168:50`

- [ ] **Line 170** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "white_analysis" for class "GoGameState"
      Attribute "white_analysis" is unknown
  - **Location**: `haive-games/src/haive/games/go/agent.py:170:30`

- [ ] **Line 171** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "white_analysis" for class "GoGameState"
      Attribute "white_analysis" is unknown
  - **Location**: `haive-games/src/haive/games/go/agent.py:171:54`

- [ ] **Line 217** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "black_analysis" for class "GoGameState"
      Attribute "black_analysis" is unknown
  - **Location**: `haive-games/src/haive/games/go/agent.py:217:48`

- [ ] **Line 220** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "white_analysis" for class "GoGameState"
      Attribute "white_analysis" is unknown
  - **Location**: `haive-games/src/haive/games/go/agent.py:220:44`

- [ ] **Line 241** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "is_over" for class "GoGame"
      Attribute "is_over" is unknown
  - **Location**: `haive-games/src/haive/games/go/agent.py:241:16`

### 📄 haive-games/src/haive/games/go/engines.py

- [ ] **Line 149** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/go/engines.py:149:51`

- [ ] **Line 160** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/go/engines.py:160:48`

- [ ] **Line 171** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/go/engines.py:171:51`

### 📄 haive-games/src/haive/games/go/go_engine.py

- [ ] **Line 102** (`reportReturnType`)
  - **Issue**: Type "bytes" is not assignable to return type "str"
      "bytes" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/go/go_engine.py:102:15`

### 📄 haive-games/src/haive/games/go/state_manager.py

- [ ] **Line 120** (`reportArgumentType`)
  - **Issue**: Argument of type "list[tuple[Literal['black', 'white'], tuple[int, int]] | tuple[str, int, int]]" cannot be assigned to parameter "move_history" of type "list[tuple[str, int, int]]" in function "**init**"
      "list[tuple[Literal['black', 'white'], tuple[int, int]] | tuple[str, int, int]]" is not assignable to "list[tuple[str, int, int]]"
        Type parameter "\_T@list" is invariant, but "tuple[Literal['black', 'white'], tuple[int, int]] | tuple[str, int, int]" is not the same as "tuple[str, int, int]"
        Consider switching from "list" to "Sequence" which is covariant
  - **Location**: `haive-games/src/haive/games/go/state_manager.py:120:25`

### 📄 haive-games/src/haive/games/hold_em/aug_llms.py

- [ ] **Line 63** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/aug_llms.py:63:52`

- [ ] **Line 66** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/aug_llms.py:66:71`

- [ ] **Line 69** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/aug_llms.py:69:47`

- [ ] **Line 148** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/aug_llms.py:148:52`

- [ ] **Line 151** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/aug_llms.py:151:71`

- [ ] **Line 154** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/aug_llms.py:154:47`

- [ ] **Line 233** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/aug_llms.py:233:71`

- [ ] **Line 236** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/aug_llms.py:236:47`

- [ ] **Line 239** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/aug_llms.py:239:47`

- [ ] **Line 242** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/aug_llms.py:242:47`

- [ ] **Line 331** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/aug_llms.py:331:71`

- [ ] **Line 334** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/aug_llms.py:334:47`

- [ ] **Line 422** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/aug_llms.py:422:47`

- [ ] **Line 425** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/aug_llms.py:425:71`

- [ ] **Line 428** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/aug_llms.py:428:47`

- [ ] **Line 510** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/aug_llms.py:510:43`

### 📄 haive-games/src/haive/games/hold_em/config.py

- [ ] **Line 430** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/config.py:430:57`

- [ ] **Line 492** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/config.py:492:57`

### 📄 haive-games/src/haive/games/hold_em/engine_logging.py

- [ ] **Line 293** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "invoke" for class "Runnable[Unknown, Unknown]"
      Type "(input_data: Unknown, **kwargs: Unknown) -> Unknown" is not assignable to type "(input: Unknown, config: RunnableConfig | None = None, **kwargs: Any) -> Unknown"
        Function accepts too many positional parameters; expected 1 but received 2
          Parameter name mismatch: "input" versus "input_data"
  - **Location**: `haive-games/src/haive/games/hold_em/engine_logging.py:293:30`

### 📄 haive-games/src/haive/games/hold_em/engines.py

- [ ] **Line 185** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/engines.py:185:48`

- [ ] **Line 187** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/engines.py:187:56`

- [ ] **Line 190** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/engines.py:190:56`

- [ ] **Line 191** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/engines.py:191:56`

- [ ] **Line 233** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/engines.py:233:53`

- [ ] **Line 364** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/engines.py:364:71`

- [ ] **Line 367** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/engines.py:367:47`

- [ ] **Line 370** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/engines.py:370:47`

- [ ] **Line 373** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/hold_em/engines.py:373:47`

### 📄 haive-games/src/haive/games/hold_em/generic_engines.py

- [ ] **Line 121** (`reportAbstractUsage`)
  - **Issue**: Cannot instantiate abstract class "HoldemPromptGenerator"
      "GenericPromptGenerator.create_analysis_prompt" is not implemented
      "GenericPromptGenerator.get_move_output_model" is not implemented
      and 1 more...
  - **Location**: `haive-games/src/haive/games/hold_em/generic_engines.py:121:27`

- [ ] **Line 121** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "players"
  - **Location**: `haive-games/src/haive/games/hold_em/generic_engines.py:121:27`

- [ ] **Line 155** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "create_engines" for class "HoldemEngineFactory"
      Attribute "create_engines" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/generic_engines.py:155:26`

### 📄 haive-games/src/haive/games/hold_em/player_agent.py

- [ ] **Line 530** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player_name" for class "HoldemPlayerAgent\*"
      Attribute "player_name" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/player_agent.py:530:77`

- [ ] **Line 543** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player_name" for class "HoldemPlayerAgent\*"
      Attribute "player_name" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/player_agent.py:543:61`

- [ ] **Line 635** (`reportInvalidTypeForm`)
  - **Issue**: Variable not allowed in type expression
  - **Location**: `haive-games/src/haive/games/hold_em/player_agent.py:635:75`

- [ ] **Line 635** (`reportInvalidTypeForm`)
  - **Issue**: Type arguments for "Literal" must be None, a literal value (int, bool, str, or bytes), or an enum value
  - **Location**: `haive-games/src/haive/games/hold_em/player_agent.py:635:75`

### 📄 haive-games/src/haive/games/hold_em/ui.py

- [ ] **Line 82** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "state" for class "HoldemRichUI\*"
      Type "HoldemState" is not assignable to type "dict[str, Any] | None"
        "HoldemState" is not assignable to "dict[str, Any]"
        "HoldemState" is not assignable to "None"
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:82:25`

- [ ] **Line 84** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "current_phase" for class "dict[str, Any]"
      Attribute "current_phase" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:84:32`

- [ ] **Line 84** (`reportOptionalMemberAccess`)
  - **Issue**: "current_phase" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:84:32`

- [ ] **Line 85** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "hand_number" for class "dict[str, Any]"
      Attribute "hand_number" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:85:30`

- [ ] **Line 85** (`reportOptionalMemberAccess`)
  - **Issue**: "hand_number" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:85:30`

- [ ] **Line 137** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, Any]" cannot be assigned to parameter "game_state" of type "HoldemState" in function "\_get_player_at_position"
      "dict[str, Any]" is not assignable to "HoldemState"
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:137:54`

- [ ] **Line 139** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, Any]" cannot be assigned to parameter "game_state" of type "HoldemState" in function "\_format_player_short"
      "dict[str, Any]" is not assignable to "HoldemState"
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:139:68`

- [ ] **Line 151** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, Any]" cannot be assigned to parameter "game_state" of type "HoldemState" in function "\_get_player_at_position"
      "dict[str, Any]" is not assignable to "HoldemState"
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:151:58`

- [ ] **Line 153** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, Any]" cannot be assigned to parameter "game_state" of type "HoldemState" in function "\_format_player_short"
      "dict[str, Any]" is not assignable to "HoldemState"
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:153:72`

- [ ] **Line 160** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "dealer_position" for class "dict[str, Any]"
      Attribute "dealer_position" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:160:32`

- [ ] **Line 174** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "community_cards" for class "dict[str, Any]"
      Attribute "community_cards" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:174:26`

- [ ] **Line 183** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "community_cards" for class "dict[str, Any]"
      Attribute "community_cards" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:183:44`

- [ ] **Line 198** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "current_phase" for class "dict[str, Any]"
      Attribute "current_phase" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:198:22`

- [ ] **Line 200** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "current_phase" for class "dict[str, Any]"
      Attribute "current_phase" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:200:24`

- [ ] **Line 202** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "current_phase" for class "dict[str, Any]"
      Attribute "current_phase" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:202:24`

- [ ] **Line 222** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "total_pot" for class "dict[str, Any]"
      Attribute "total_pot" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:222:38`

- [ ] **Line 224** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "current_bet" for class "dict[str, Any]"
      Attribute "current_bet" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:224:22`

- [ ] **Line 226** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "current_bet" for class "dict[str, Any]"
      Attribute "current_bet" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:226:42`

- [ ] **Line 228** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "side_pots" for class "dict[str, Any]"
      Attribute "side_pots" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:228:22`

- [ ] **Line 229** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "side_pots" for class "dict[str, Any]"
      Attribute "side_pots" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:229:57`

- [ ] **Line 232** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "current_player" for class "dict[str, Any]"
      Attribute "current_player" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:232:22`

- [ ] **Line 234** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "current_player" for class "dict[str, Any]"
      Attribute "current_player" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:234:42`

- [ ] **Line 251** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "players" for class "dict[str, Any]"
      Attribute "players" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:251:33`

- [ ] **Line 265** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "big_blind" for class "dict[str, Any]"
      Attribute "big_blind" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:265:43`

- [ ] **Line 300** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "actions_this_round" for class "dict[str, Any]"
      Attribute "actions_this_round" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:300:26`

- [ ] **Line 307** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "actions_this_round" for class "dict[str, Any]"
      Attribute "actions_this_round" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:307:36`

- [ ] **Line 311** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, Any]" cannot be assigned to parameter "game_state" of type "HoldemState" in function "\_get_player_name_by_id"
      "dict[str, Any]" is not assignable to "HoldemState"
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:311:16`

- [ ] **Line 345** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "hand_history" for class "dict[str, Any]"
      Attribute "hand_history" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:345:26`

- [ ] **Line 351** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "hand_history" for class "dict[str, Any]"
      Attribute "hand_history" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:351:34`

- [ ] **Line 355** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, Any]" cannot be assigned to parameter "game_state" of type "HoldemState" in function "\_get_player_name_by_id"
      "dict[str, Any]" is not assignable to "HoldemState"
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:355:49`

- [ ] **Line 373** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "hand_number" for class "dict[str, Any]"
      Attribute "hand_number" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:373:46`

- [ ] **Line 374** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "players" for class "dict[str, Any]"
      Attribute "players" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:374:53`

- [ ] **Line 375** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "active_players" for class "dict[str, Any]"
      Attribute "active_players" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:375:52`

- [ ] **Line 376** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "players_in_hand" for class "dict[str, Any]"
      Attribute "players_in_hand" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:376:53`

- [ ] **Line 380** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "small_blind" for class "dict[str, Any]"
      Attribute "small_blind" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:380:36`

- [ ] **Line 380** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "big_blind" for class "dict[str, Any]"
      Attribute "big_blind" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:380:61`

- [ ] **Line 385** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "players" for class "dict[str, Any]"
      Attribute "players" is unknown
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:385:68`

- [ ] **Line 402** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "state" for class "HoldemRichUI\*"
      Type "HoldemState" is not assignable to type "dict[str, Any] | None"
        "HoldemState" is not assignable to "dict[str, Any]"
        "HoldemState" is not assignable to "None"
  - **Location**: `haive-games/src/haive/games/hold_em/ui.py:402:21`

### 📄 haive-games/src/haive/games/hold_em/utils.py

- [ ] **Line 86** (`reportGeneralTypeIssues`)
  - **Issue**: Expected class but received "(iterable: Iterable[object], /) -> bool"
  - **Location**: `haive-games/src/haive/games/hold_em/utils.py:86:15`

### 📄 haive-games/src/haive/games/llm_config_factory.py

- [ ] **Line 12** (`reportMissingImports`)
  - **Issue**: Import "haive.games.models.llm" could not be resolved
  - **Location**: `haive-games/src/haive/games/llm_config_factory.py:12:5`

- [ ] **Line 115** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/llm_config_factory.py:115:51`

- [ ] **Line 117** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/llm_config_factory.py:117:48`

### 📄 haive-games/src/haive/games/mafia/agent.py

- [ ] **Line 329** (`reportArgumentType`)
  - **Issue**: Argument of type "list[Unknown]" cannot be assigned to parameter "value" of type "str" in function "**setitem**"
      "list[Unknown]" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/mafia/agent.py:329:12`

- [ ] **Line 377** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "value" for class "str"
      Attribute "value" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/agent.py:377:55`

- [ ] **Line 513** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "action_type" for class "str"
      Attribute "action_type" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/agent.py:513:39`

- [ ] **Line 534** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "target_id" for class "str"
      Attribute "target_id" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/agent.py:534:35`

- [ ] **Line 535** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "message" for class "str"
      Attribute "message" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/agent.py:535:33`

- [ ] **Line 539** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "target_id" for class "str"
      Attribute "target_id" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/agent.py:539:62`

- [ ] **Line 546** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "announcement" for class "str"
      Attribute "announcement" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/agent.py:546:38`

- [ ] **Line 547** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "phase_transition" for class "str"
      Attribute "phase_transition" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/agent.py:547:42`

- [ ] **Line 597** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['action_type']" cannot be assigned to parameter "key" of type "SupportsIndex | slice[Any, Any, Any]" in function "**getitem**"
      Type "Literal['action_type']" is not assignable to type "SupportsIndex | slice[Any, Any, Any]"
        "Literal['action_type']" is incompatible with protocol "SupportsIndex"
          "**index**" is not present
        "Literal['action_type']" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-games/src/haive/games/mafia/agent.py:597:34`

- [ ] **Line 630** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['action']" cannot be assigned to parameter "key" of type "SupportsIndex | slice[Any, Any, Any]" in function "**getitem**"
      Type "Literal['action']" is not assignable to type "SupportsIndex | slice[Any, Any, Any]"
        "Literal['action']" is incompatible with protocol "SupportsIndex"
          "**index**" is not present
        "Literal['action']" is not assignable to "slice[Any, Any, Any]"
  - **Location**: `haive-games/src/haive/games/mafia/agent.py:630:25`

- [ ] **Line 635** (`reportArgumentType`)
  - **Issue**: Argument of type "str" cannot be assigned to parameter "player_state_updates" of type "dict[str, dict[str, Any]]" in function "**init**"
      "str" is not assignable to "dict[str, dict[str, Any]]"
  - **Location**: `haive-games/src/haive/games/mafia/agent.py:635:48`

- [ ] **Line 635** (`reportArgumentType`)
  - **Issue**: Argument of type "str" cannot be assigned to parameter "phase_transition" of type "bool" in function "**init**"
      "str" is not assignable to "bool"
  - **Location**: `haive-games/src/haive/games/mafia/agent.py:635:48`

- [ ] **Line 635** (`reportArgumentType`)
  - **Issue**: Argument of type "str" cannot be assigned to parameter "next_phase" of type "GamePhase | None" in function "**init**"
      Type "str" is not assignable to type "GamePhase | None"
        "str" is not assignable to "GamePhase"
        "str" is not assignable to "None"
  - **Location**: `haive-games/src/haive/games/mafia/agent.py:635:48`

- [ ] **Line 635** (`reportArgumentType`)
  - **Issue**: Argument of type "str" cannot be assigned to parameter "round_number" of type "int" in function "**init**"
      "str" is not assignable to "int"
  - **Location**: `haive-games/src/haive/games/mafia/agent.py:635:48`

- [ ] **Line 641** (`reportReturnType`)
  - **Issue**: Type "str" is not assignable to return type "MafiaAction | NarratorAction"
      Type "str" is not assignable to type "MafiaAction | NarratorAction"
        "str" is not assignable to "MafiaAction"
        "str" is not assignable to "NarratorAction"
  - **Location**: `haive-games/src/haive/games/mafia/agent.py:641:23`

- [ ] **Line 856** (`reportArgumentType`)
  - **Issue**: Argument of type "MafiaAction | Any" cannot be assigned to parameter "response" of type "str" in function "extract_move"
      Type "MafiaAction | Any" is not assignable to type "str"
        "MafiaAction" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/mafia/agent.py:856:37`

- [ ] **Line 958** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "phase_transition" for class "MafiaAction"
      Attribute "phase_transition" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/agent.py:958:27`

- [ ] **Line 1000** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "max_days" for class "MultiPlayerGameConfig"
      Attribute "max_days" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/agent.py:1000:79`

- [ ] **Line 1002** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "max_days" for class "MultiPlayerGameConfig"
      Attribute "max_days" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/agent.py:1002:59`

- [ ] **Line 1160** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "model_dump" for class "dict[Unknown, Unknown]"
      Attribute "model_dump" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/agent.py:1160:35`

- [ ] **Line 1162** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "dict" for class "dict[Unknown, Unknown]"
      Attribute "dict" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/agent.py:1162:35`

### 📄 haive-games/src/haive/games/mafia/aug_llms.py

- [ ] **Line 25** (`reportAttributeAccessIssue`)
  - **Issue**: "MafiaAnalysis" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/mafia/aug_llms.py:25:37`

### 📄 haive-games/src/haive/games/mafia/configurable_config.py

- [ ] **Line 13** (`reportAttributeAccessIssue`)
  - **Issue**: "MafiaConfig" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/mafia/configurable_config.py:13:37`

### 📄 haive-games/src/haive/games/mafia/example.py

- [ ] **Line 117** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "role_enum_mapping" for class "Agent[Unknown]"
      Attribute "role_enum_mapping" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/example.py:117:42`

- [ ] **Line 156** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "visualize_state" for class "Agent[Unknown]"
      Attribute "visualize_state" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/example.py:156:26`

- [ ] **Line 198** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "visualize_state" for class "Agent[Unknown]"
      Attribute "visualize_state" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/example.py:198:34`

### 📄 haive-games/src/haive/games/mafia/generic_engines.py

- [ ] **Line 101** (`reportAbstractUsage`)
  - **Issue**: Cannot instantiate abstract class "MafiaPromptGenerator"
      "GenericPromptGenerator.create_analysis_prompt" is not implemented
      "GenericPromptGenerator.get_move_output_model" is not implemented
      and 1 more...
  - **Location**: `haive-games/src/haive/games/mafia/generic_engines.py:101:27`

- [ ] **Line 101** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "players"
  - **Location**: `haive-games/src/haive/games/mafia/generic_engines.py:101:27`

- [ ] **Line 133** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "create_engines" for class "MafiaEngineFactory"
      Attribute "create_engines" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/generic_engines.py:133:25`

### 📄 haive-games/src/haive/games/mafia/mock_runner.py

- [ ] **Line 426** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "visualize_state" for class "Agent[Unknown]"
      Attribute "visualize_state" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/mock_runner.py:426:18`

- [ ] **Line 457** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get_player_role" for class "Agent[Unknown]"
      Attribute "get_player_role" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/mock_runner.py:457:32`

- [ ] **Line 462** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "prepare_narrator_context" for class "Agent[Unknown]"
      Attribute "prepare_narrator_context" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/mock_runner.py:462:32`

- [ ] **Line 477** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "extract_move" for class "Agent[Unknown]"
      Attribute "extract_move" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/mock_runner.py:477:39`

- [ ] **Line 496** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get_engine_for_player" for class "Agent[Unknown]"
      Attribute "get_engine_for_player" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/mock_runner.py:496:36`

- [ ] **Line 501** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "prepare_move_context" for class "Agent[Unknown]"
      Attribute "prepare_move_context" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/mock_runner.py:501:40`

- [ ] **Line 507** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "extract_move" for class "Agent[Unknown]"
      Attribute "extract_move" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/mock_runner.py:507:37`

- [ ] **Line 610** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "visualize_state" for class "Agent[Unknown]"
      Attribute "visualize_state" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/mock_runner.py:610:14`

### 📄 haive-games/src/haive/games/mafia/simple_runner.py

- [ ] **Line 83** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "role_enum_mapping" for class "Agent[Unknown]"
      Attribute "role_enum_mapping" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/simple_runner.py:83:43`

- [ ] **Line 104** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "visualize_state" for class "Agent[Unknown]"
      Attribute "visualize_state" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/simple_runner.py:104:18`

- [ ] **Line 123** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "NARRATOR" for class "type[GamePhase]"
      Attribute "NARRATOR" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/simple_runner.py:123:65`

- [ ] **Line 131** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get_player_role" for class "Agent[Unknown]"
      Attribute "get_player_role" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/simple_runner.py:131:32`

- [ ] **Line 136** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "prepare_narrator_context" for class "Agent[Unknown]"
      Attribute "prepare_narrator_context" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/simple_runner.py:136:32`

- [ ] **Line 151** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "extract_move" for class "Agent[Unknown]"
      Attribute "extract_move" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/simple_runner.py:151:39`

- [ ] **Line 170** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get_engine_for_player" for class "Agent[Unknown]"
      Attribute "get_engine_for_player" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/simple_runner.py:170:36`

- [ ] **Line 175** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "prepare_move_context" for class "Agent[Unknown]"
      Attribute "prepare_move_context" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/simple_runner.py:175:40`

- [ ] **Line 181** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "extract_move" for class "Agent[Unknown]"
      Attribute "extract_move" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/simple_runner.py:181:37`

- [ ] **Line 272** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "visualize_state" for class "Agent[Unknown]"
      Attribute "visualize_state" is unknown
  - **Location**: `haive-games/src/haive/games/mafia/simple_runner.py:272:14`

### 📄 haive-games/src/haive/games/mafia/state_manager.py

- [ ] **Line 361** (`reportArgumentType`)
  - **Issue**: Argument of type "MafiaAction" cannot be assigned to parameter "object" of type "dict[str, Any]" in function "append"
      "MafiaAction" is not assignable to "dict[str, Any]"
  - **Location**: `haive-games/src/haive/games/mafia/state_manager.py:361:44`

- [ ] **Line 419** (`reportArgumentType`)
  - **Issue**: Argument of type "NarratorAction" cannot be assigned to parameter "object" of type "dict[str, Any]" in function "append"
      "NarratorAction" is not assignable to "dict[str, Any]"
  - **Location**: `haive-games/src/haive/games/mafia/state_manager.py:419:44`

### 📄 haive-games/src/haive/games/mafia/verify_imports.py

- [ ] **Line 8** (`reportMissingImports`)
  - **Issue**: Import "models" could not be resolved
  - **Location**: `haive-games/src/haive/games/mafia/verify_imports.py:8:5`

### 📄 haive-games/src/haive/games/mancala/agent.py

- [ ] **Line 92** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "tool_calls" for class "dict[Unknown, Unknown]"
      Attribute "tool_calls" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/agent.py:92:52`

- [ ] **Line 93** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "tool_calls" for class "dict[Unknown, Unknown]"
      Attribute "tool_calls" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/agent.py:93:34`

- [ ] **Line 193** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "set_finish_point" for class "DynamicGraph"
      Attribute "set_finish_point" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/agent.py:193:22`

- [ ] **Line 279** (`reportArgumentType`)
  - **Issue**: Argument of type "str" cannot be assigned to parameter "player" of type "Literal['player1', 'player2']" in function "get_valid_moves"
      Type "str" is not assignable to type "Literal['player1', 'player2']"
        "str" is not assignable to type "Literal['player1']"
        "str" is not assignable to type "Literal['player2']"
  - **Location**: `haive-games/src/haive/games/mancala/agent.py:279:44`

- [ ] **Line 290** (`reportArgumentType`)
  - **Issue**: Argument of type "str" cannot be assigned to parameter "player" of type "Literal['player1', 'player2']" in function "**init**"
      Type "str" is not assignable to type "Literal['player1', 'player2']"
        "str" is not assignable to type "Literal['player1']"
        "str" is not assignable to type "Literal['player2']"
  - **Location**: `haive-games/src/haive/games/mancala/agent.py:290:64`

- [ ] **Line 311** (`reportArgumentType`)
  - **Issue**: Argument of type "str" cannot be assigned to parameter "player" of type "Literal['player1', 'player2']" in function "**init**"
      Type "str" is not assignable to type "Literal['player1', 'player2']"
        "str" is not assignable to type "Literal['player1']"
        "str" is not assignable to type "Literal['player2']"
  - **Location**: `haive-games/src/haive/games/mancala/agent.py:311:71`

- [ ] **Line 324** (`reportArgumentType`)
  - **Issue**: Argument of type "str" cannot be assigned to parameter "player" of type "Literal['player1', 'player2']" in function "**init**"
      Type "str" is not assignable to type "Literal['player1', 'player2']"
        "str" is not assignable to type "Literal['player1']"
        "str" is not assignable to type "Literal['player2']"
  - **Location**: `haive-games/src/haive/games/mancala/agent.py:324:60`

- [ ] **Line 431** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "stones_per_pit" for class "GameConfig"
      Attribute "stones_per_pit" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/agent.py:431:41`

### 📄 haive-games/src/haive/games/mancala/agent_original.py

- [ ] **Line 49** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state" for class "Command[Unknown]"
      Attribute "state" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/agent_original.py:49:57`

- [ ] **Line 50** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state" for class "Command[Unknown]"
      Attribute "state" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/agent_original.py:50:49`

- [ ] **Line 93** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "aug_llm_configs" for class "MancalaConfig"
      Attribute "aug_llm_configs" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/agent_original.py:93:30`

- [ ] **Line 106** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "stones_per_pit" for class "GameConfig"
      Attribute "stones_per_pit" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/agent_original.py:106:39`

- [ ] **Line 117** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player1_analysis" for class "MancalaState"
      Attribute "player1_analysis" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/agent_original.py:117:47`

- [ ] **Line 118** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player2_analysis" for class "MancalaState"
      Attribute "player2_analysis" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/agent_original.py:118:47`

- [ ] **Line 165** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "board_string" for class "MancalaState"
      Attribute "board_string" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/agent_original.py:165:43`

- [ ] **Line 211** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "board_string" for class "MancalaState"
      Attribute "board_string" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/agent_original.py:211:43`

- [ ] **Line 213** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player1_score" for class "MancalaState"
      Attribute "player1_score" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/agent_original.py:213:44`

- [ ] **Line 214** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player2_score" for class "MancalaState"
      Attribute "player2_score" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/agent_original.py:214:44`

- [ ] **Line 254** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "args" for class "ToolCall"
      Attribute "args" is unknown
      Use ["args"] to reference item in TypedDict
  - **Location**: `haive-games/src/haive/games/mancala/agent_original.py:254:37`

- [ ] **Line 284** (`reportArgumentType`)
  - **Issue**: Argument of type "Unknown | None" cannot be assigned to parameter "pit_index" of type "int" in function "**init**"
      Type "Unknown | None" is not assignable to type "int"
        "None" is not assignable to "int"
  - **Location**: `haive-games/src/haive/games/mancala/agent_original.py:284:26`

- [ ] **Line 342** (`reportCallIssue`)
  - **Issue**: No parameter named "stop"
  - **Location**: `haive-games/src/haive/games/mancala/agent_original.py:342:31`

- [ ] **Line 361** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "player" for class "MancalaMove"
      Type "str" is not assignable to type "Literal['player1', 'player2']"
        "str" is not assignable to type "Literal['player1']"
        "str" is not assignable to type "Literal['player2']"
  - **Location**: `haive-games/src/haive/games/mancala/agent_original.py:361:38`

- [ ] **Line 418** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "args" for class "ToolCall"
      Attribute "args" is unknown
      Use ["args"] to reference item in TypedDict
  - **Location**: `haive-games/src/haive/games/mancala/agent_original.py:418:55`

- [ ] **Line 508** (`reportCallIssue`)
  - **Issue**: No parameter named "stop"
  - **Location**: `haive-games/src/haive/games/mancala/agent_original.py:508:31`

- [ ] **Line 574** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "board_string" for class "MancalaState"
      Attribute "board_string" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/agent_original.py:574:29`

- [ ] **Line 588** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get_winner" for class "MancalaState"
      Attribute "get_winner" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/agent_original.py:588:36`

- [ ] **Line 640** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "stones_per_pit" for class "GameConfig"
      Attribute "stones_per_pit" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/agent_original.py:640:39`

- [ ] **Line 661** (`reportReturnType`)
  - **Issue**: Type "Any | None" is not assignable to return type "MancalaState"
      Type "Any | None" is not assignable to type "MancalaState"
        "None" is not assignable to "MancalaState"
  - **Location**: `haive-games/src/haive/games/mancala/agent_original.py:661:23`

### 📄 haive-games/src/haive/games/mancala/engines.py

- [ ] **Line 90** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/mancala/engines.py:90:50`

- [ ] **Line 96** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/mancala/engines.py:96:50`

- [ ] **Line 102** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/mancala/engines.py:102:50`

- [ ] **Line 108** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/mancala/engines.py:108:50`

### 📄 haive-games/src/haive/games/mancala/generic_engines.py

- [ ] **Line 101** (`reportAbstractUsage`)
  - **Issue**: Cannot instantiate abstract class "MancalaPromptGenerator"
      "GenericPromptGenerator.create_analysis_prompt" is not implemented
      "GenericPromptGenerator.get_move_output_model" is not implemented
      and 1 more...
  - **Location**: `haive-games/src/haive/games/mancala/generic_engines.py:101:27`

- [ ] **Line 101** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "players"
  - **Location**: `haive-games/src/haive/games/mancala/generic_engines.py:101:27`

- [ ] **Line 134** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "create_engines" for class "MancalaEngineFactory"
      Attribute "create_engines" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/generic_engines.py:134:27`

### 📄 haive-games/src/haive/games/mancala/state.py

- [ ] **Line 35** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "additional_kwargs" for class "dict[Unknown, Unknown]"
      Attribute "additional_kwargs" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/state.py:35:37`

- [ ] **Line 38** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "additional_kwargs" for class "dict[Unknown, Unknown]"
      Attribute "additional_kwargs" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/state.py:38:34`

### 📄 haive-games/src/haive/games/mancala/state_manager.py

- [ ] **Line 231** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player1_score" for class "MancalaState"
      Attribute "player1_score" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/state_manager.py:231:21`

- [ ] **Line 231** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player2_score" for class "MancalaState"
      Attribute "player2_score" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/state_manager.py:231:43`

- [ ] **Line 232** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "game_status" for class "MancalaState"
      Type "Literal['player1_win']" is not assignable to type "Literal['ongoing', 'ended']"
        "Literal['player1_win']" is not assignable to type "Literal['ongoing']"
        "Literal['player1_win']" is not assignable to type "Literal['ended']"
  - **Location**: `haive-games/src/haive/games/mancala/state_manager.py:232:36`

- [ ] **Line 234** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player2_score" for class "MancalaState"
      Attribute "player2_score" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/state_manager.py:234:23`

- [ ] **Line 234** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player1_score" for class "MancalaState"
      Attribute "player1_score" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/state_manager.py:234:45`

- [ ] **Line 235** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "game_status" for class "MancalaState"
      Type "Literal['player2_win']" is not assignable to type "Literal['ongoing', 'ended']"
        "Literal['player2_win']" is not assignable to type "Literal['ongoing']"
        "Literal['player2_win']" is not assignable to type "Literal['ended']"
  - **Location**: `haive-games/src/haive/games/mancala/state_manager.py:235:36`

- [ ] **Line 238** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "game_status" for class "MancalaState"
      Type "Literal['draw']" is not assignable to type "Literal['ongoing', 'ended']"
        "Literal['draw']" is not assignable to type "Literal['ongoing']"
        "Literal['draw']" is not assignable to type "Literal['ended']"
  - **Location**: `haive-games/src/haive/games/mancala/state_manager.py:238:36`

### 📄 haive-games/src/haive/games/mancala/state_original.py

- [ ] **Line 162** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "additional_kwargs" for class "dict[Unknown, Unknown]"
      Attribute "additional_kwargs" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/state_original.py:162:53`

- [ ] **Line 165** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "additional_kwargs" for class "dict[Unknown, Unknown]"
      Attribute "additional_kwargs" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/state_original.py:165:50`

- [ ] **Line 195** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "additional_kwargs" for class "dict[Unknown, Unknown]"
      Attribute "additional_kwargs" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/state_original.py:195:53`

- [ ] **Line 198** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "additional_kwargs" for class "dict[Unknown, Unknown]"
      Attribute "additional_kwargs" is unknown
  - **Location**: `haive-games/src/haive/games/mancala/state_original.py:198:50`

### 📄 haive-games/src/haive/games/mastermind/agent.py

- [ ] **Line 47** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state" for class "Command[Unknown]"
      Attribute "state" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/agent.py:47:57`

- [ ] **Line 48** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state" for class "Command[Unknown]"
      Attribute "state" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/agent.py:48:49`

- [ ] **Line 113** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "secret_code" for class "GameConfig"
      Attribute "secret_code" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/agent.py:113:34`

- [ ] **Line 121** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "codemaker" for class "GameConfig"
      Attribute "codemaker" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/agent.py:121:34`

- [ ] **Line 122** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "colors" for class "GameConfig"
      Attribute "colors" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/agent.py:122:31`

- [ ] **Line 123** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "code_length" for class "GameConfig"
      Attribute "code_length" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/agent.py:123:36`

- [ ] **Line 124** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "max_turns" for class "GameConfig"
      Attribute "max_turns" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/agent.py:124:34`

- [ ] **Line 558** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "codemaker" for class "GameConfig"
      Attribute "codemaker" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/agent.py:558:23`

- [ ] **Line 597** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "secret_code" for class "GameConfig"
      Attribute "secret_code" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/agent.py:597:34`

- [ ] **Line 603** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "codemaker" for class "GameConfig"
      Attribute "codemaker" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/agent.py:603:34`

- [ ] **Line 604** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "colors" for class "GameConfig"
      Attribute "colors" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/agent.py:604:31`

- [ ] **Line 605** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "code_length" for class "GameConfig"
      Attribute "code_length" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/agent.py:605:36`

- [ ] **Line 606** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "max_turns" for class "GameConfig"
      Attribute "max_turns" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/agent.py:606:34`

- [ ] **Line 644** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "game_status" for class "MastermindState"
      Type "LiteralString" is not assignable to type "Literal['ongoing', 'player1_win', 'player2_win']"
        "str" is not assignable to "Literal['ongoing']"
        "str" is not assignable to "Literal['player1_win']"
        "str" is not assignable to "Literal['player2_win']"
  - **Location**: `haive-games/src/haive/games/mastermind/agent.py:644:56`

- [ ] **Line 685** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "secret_code" for class "GameConfig"
      Attribute "secret_code" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/agent.py:685:23`

- [ ] **Line 686** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "secret_code" for class "GameConfig"
      Attribute "secret_code" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/agent.py:686:38`

- [ ] **Line 695** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "code" for class "dict[Unknown, Unknown]"
      Attribute "code" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/agent.py:695:70`

- [ ] **Line 697** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "code" for class "dict[Unknown, Unknown]"
      Attribute "code" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/agent.py:697:43`

- [ ] **Line 722** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "codemaker" for class "GameConfig"
      Attribute "codemaker" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/agent.py:722:34`

- [ ] **Line 723** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "colors" for class "GameConfig"
      Attribute "colors" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/agent.py:723:31`

- [ ] **Line 724** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "code_length" for class "GameConfig"
      Attribute "code_length" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/agent.py:724:36`

- [ ] **Line 725** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "max_turns" for class "GameConfig"
      Attribute "max_turns" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/agent.py:725:34`

- [ ] **Line 778** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "game_status" for class "MastermindState"
      Type "LiteralString" is not assignable to type "Literal['ongoing', 'player1_win', 'player2_win']"
        "str" is not assignable to "Literal['ongoing']"
        "str" is not assignable to "Literal['player1_win']"
        "str" is not assignable to "Literal['player2_win']"
  - **Location**: `haive-games/src/haive/games/mastermind/agent.py:778:64`

### 📄 haive-games/src/haive/games/mastermind/demo.py

- [ ] **Line 132** (`reportRedeclaration`)
  - **Issue**: Class declaration "MastermindUI" is obscured by a declaration of the same name
  - **Location**: `haive-games/src/haive/games/mastermind/demo.py:132:10`

### 📄 haive-games/src/haive/games/mastermind/engines.py

- [ ] **Line 115** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/mastermind/engines.py:115:50`

- [ ] **Line 122** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/mastermind/engines.py:122:50`

- [ ] **Line 129** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/mastermind/engines.py:129:50`

- [ ] **Line 136** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/mastermind/engines.py:136:50`

- [ ] **Line 143** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/mastermind/engines.py:143:50`

### 📄 haive-games/src/haive/games/mastermind/example.py

- [ ] **Line 84** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_game_with_ui" for class "Agent[Unknown]"
      Attribute "run_game_with_ui" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/example.py:84:14`

- [ ] **Line 86** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_game" for class "Agent[Unknown]"
      Attribute "run_game" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/example.py:86:14`

### 📄 haive-games/src/haive/games/mastermind/generic_engines.py

- [ ] **Line 101** (`reportAbstractUsage`)
  - **Issue**: Cannot instantiate abstract class "MastermindPromptGenerator"
      "GenericPromptGenerator.create_analysis_prompt" is not implemented
      "GenericPromptGenerator.get_move_output_model" is not implemented
      and 1 more...
  - **Location**: `haive-games/src/haive/games/mastermind/generic_engines.py:101:27`

- [ ] **Line 101** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "players"
  - **Location**: `haive-games/src/haive/games/mastermind/generic_engines.py:101:27`

- [ ] **Line 133** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "create_engines" for class "MastermindEngineFactory"
      Attribute "create_engines" is unknown
  - **Location**: `haive-games/src/haive/games/mastermind/generic_engines.py:133:30`

### 📄 haive-games/src/haive/games/mastermind/models.py

- [ ] **Line 163** (`reportCallIssue`)
  - **Issue**: No overloads for "Field" match the provided arguments
      Argument types: (EllipsisType, Literal[4], Literal[4], Literal['The secret code: 4 colors chosen from the allowed …'])
  - **Location**: `haive-games/src/haive/games/mastermind/models.py:163:29`

- [ ] **Line 240** (`reportCallIssue`)
  - **Issue**: No overloads for "Field" match the provided arguments
      Argument types: (EllipsisType, Literal[4], Literal[4], Literal['List of 4 colors'])
  - **Location**: `haive-games/src/haive/games/mastermind/models.py:240:31`

### 📄 haive-games/src/haive/games/mastermind/state.py

- [ ] **Line 96** (`reportCallIssue`)
  - **Issue**: No overloads for "Field" match the provided arguments
      Argument types: (EllipsisType, Literal[4], Literal[4], Literal['Secret color code (4 colors)'])
  - **Location**: `haive-games/src/haive/games/mastermind/state.py:96:29`

- [ ] **Line 105** (`reportGeneralTypeIssues`)
  - **Issue**: "turn" overrides a field of the same name but is missing a default value
  - **Location**: `haive-games/src/haive/games/mastermind/state.py:105:4`

- [ ] **Line 137** (`reportAssignmentType`)
  - **Issue**: Type "list[ValidColor]" is not assignable to declared type "list[str] | ColorCode | dict[Unknown, Unknown] | None"
      Type "list[ValidColor]" is not assignable to type "list[str] | ColorCode | dict[Unknown, Unknown] | None"
        "list[ValidColor]" is not assignable to "list[str]"
          Type parameter "\_T@list" is invariant, but "ValidColor" is not the same as "str"
          Consider switching from "list" to "Sequence" which is covariant
        "list[ValidColor]" is not assignable to "ColorCode"
        "list[ValidColor]" is not assignable to "dict[Unknown, Unknown]"
        "list[ValidColor]" is not assignable to "None"
  - **Location**: `haive-games/src/haive/games/mastermind/state.py:137:26`

- [ ] **Line 144** (`reportArgumentType`)
  - **Issue**: Argument of type "list[str] | ColorCode | dict[Unknown, Unknown] | Unknown | None" cannot be assigned to parameter "secret_code" of type "list[str]" in function "**init**"
      Type "list[str] | ColorCode | dict[Unknown, Unknown] | Unknown | None" is not assignable to type "list[str]"
        "ColorCode" is not assignable to "list[str]"
  - **Location**: `haive-games/src/haive/games/mastermind/state.py:144:24`

- [ ] **Line 148** (`reportArgumentType`)
  - **Issue**: Argument of type "str" cannot be assigned to parameter "codemaker" of type "Literal['player1', 'player2']" in function "**init**"
      Type "str" is not assignable to type "Literal['player1', 'player2']"
        "str" is not assignable to type "Literal['player1']"
        "str" is not assignable to type "Literal['player2']"
  - **Location**: `haive-games/src/haive/games/mastermind/state.py:148:22`

### 📄 haive-games/src/haive/games/mastermind/state_manager.py

- [ ] **Line 64** (`reportArgumentType`)
  - **Issue**: Argument of type "list[ValidColor] | Unknown | list[Unknown] | dict[Unknown, Unknown]" cannot be assigned to parameter "secret_code" of type "list[str]" in function "**init**"
      Type "list[ValidColor] | Unknown | list[Unknown] | dict[Unknown, Unknown]" is not assignable to type "list[str]"
        "dict[Unknown, Unknown]" is not assignable to "list[str]"
  - **Location**: `haive-games/src/haive/games/mastermind/state_manager.py:64:24`

- [ ] **Line 121** (`reportArgumentType`)
  - **Issue**: Argument of type "list[ValidColor]" cannot be assigned to parameter "guess" of type "list[str]" in function "\_calculate_feedback"
      "list[ValidColor]" is not assignable to "list[str]"
        Type parameter "\_T@list" is invariant, but "ValidColor" is not the same as "str"
        Consider switching from "list" to "Sequence" which is covariant
  - **Location**: `haive-games/src/haive/games/mastermind/state_manager.py:121:66`

- [ ] **Line 127** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "game_status" for class "MastermindState"
      Type "LiteralString" is not assignable to type "Literal['ongoing', 'player1_win', 'player2_win']"
        "str" is not assignable to "Literal['ongoing']"
        "str" is not assignable to "Literal['player1_win']"
        "str" is not assignable to "Literal['player2_win']"
  - **Location**: `haive-games/src/haive/games/mastermind/state_manager.py:127:36`

- [ ] **Line 131** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "game_status" for class "MastermindState"
      Type "LiteralString" is not assignable to type "Literal['ongoing', 'player1_win', 'player2_win']"
        "str" is not assignable to "Literal['ongoing']"
        "str" is not assignable to "Literal['player1_win']"
        "str" is not assignable to "Literal['player2_win']"
  - **Location**: `haive-games/src/haive/games/mastermind/state_manager.py:131:36`

### 📄 haive-games/src/haive/games/monopoly/**init**.py

- [ ] **Line 5** (`reportAttributeAccessIssue`)
  - **Issue**: "MonopolyGame" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/monopoly/__init__.py:5:44`

### 📄 haive-games/src/haive/games/monopoly/config.py

- [ ] **Line 692** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['waiting']" cannot be assigned to parameter "game_status" of type "GameStatus" in function "**init**"
      "Literal['waiting']" is not assignable to "GameStatus"
  - **Location**: `haive-games/src/haive/games/monopoly/config.py:692:24`

### 📄 haive-games/src/haive/games/monopoly/configurable_config.py

- [ ] **Line 64** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "engines" for class "ConfigurableMonopolyConfig\*"
      "dict[str, AugLLMConfig]" is not assignable to "dict[str, Engine[Unknown, Unknown] | str]"
        Type parameter "\_VT@dict" is invariant, but "AugLLMConfig" is not the same as "Engine[Unknown, Unknown] | str"
        Consider switching from "dict" to "Mapping" which is covariant in the value type
  - **Location**: `haive-games/src/haive/games/monopoly/configurable_config.py:64:27`

- [ ] **Line 69** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "engines" for class "ConfigurableMonopolyConfig\*"
      "dict[str, AugLLMConfig]" is not assignable to "dict[str, Engine[Unknown, Unknown] | str]"
        Type parameter "\_VT@dict" is invariant, but "AugLLMConfig" is not the same as "Engine[Unknown, Unknown] | str"
        Consider switching from "dict" to "Mapping" which is covariant in the value type
  - **Location**: `haive-games/src/haive/games/monopoly/configurable_config.py:69:27`

- [ ] **Line 79** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "engines" for class "ConfigurableMonopolyConfig\*"
      "dict[str, AugLLMConfig]" is not assignable to "dict[str, Engine[Unknown, Unknown] | str]"
        Type parameter "\_VT@dict" is invariant, but "AugLLMConfig" is not the same as "Engine[Unknown, Unknown] | str"
        Consider switching from "dict" to "Mapping" which is covariant in the value type
  - **Location**: `haive-games/src/haive/games/monopoly/configurable_config.py:79:27`

### 📄 haive-games/src/haive/games/monopoly/engines.py

- [ ] **Line 153** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/monopoly/engines.py:153:56`

- [ ] **Line 157** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/monopoly/engines.py:157:44`

### 📄 haive-games/src/haive/games/monopoly/game/game.py

- [ ] **Line 686** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "color_group" of type "str" in function "player_owns_all_in_group"
      Type "str | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/monopoly/game/game.py:686:57`

- [ ] **Line 698** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "color_group" of type "str" in function "get_properties_by_group"
      Type "str | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/monopoly/game/game.py:698:51`

- [ ] **Line 723** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "color_group" of type "str" in function "get_properties_by_group"
      Type "str | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/monopoly/game/game.py:723:51`

- [ ] **Line 754** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "color_group" of type "str" in function "get_properties_by_group"
      Type "str | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/monopoly/game/game.py:754:55`

- [ ] **Line 816** (`reportArgumentType`)
  - **Issue**: Argument of type "Unknown | None" cannot be assigned to parameter "property_position" of type "int" in function "\_handle_sell_house_action"
      Type "Unknown | None" is not assignable to type "int"
        "None" is not assignable to "int"
  - **Location**: `haive-games/src/haive/games/monopoly/game/game.py:816:58`

- [ ] **Line 820** (`reportArgumentType`)
  - **Issue**: Argument of type "Unknown | None" cannot be assigned to parameter "property_position" of type "int" in function "\_handle_build_house_action"
      Type "Unknown | None" is not assignable to type "int"
        "None" is not assignable to "int"
  - **Location**: `haive-games/src/haive/games/monopoly/game/game.py:820:59`

- [ ] **Line 824** (`reportArgumentType`)
  - **Issue**: Argument of type "Unknown | None" cannot be assigned to parameter "property_position" of type "int" in function "\_handle_mortgage_action"
      Type "Unknown | None" is not assignable to type "int"
        "None" is not assignable to "int"
  - **Location**: `haive-games/src/haive/games/monopoly/game/game.py:824:56`

- [ ] **Line 828** (`reportArgumentType`)
  - **Issue**: Argument of type "Unknown | None" cannot be assigned to parameter "property_position" of type "int" in function "\_handle_unmortgage_action"
      Type "Unknown | None" is not assignable to type "int"
        "None" is not assignable to "int"
  - **Location**: `haive-games/src/haive/games/monopoly/game/game.py:828:58`

- [ ] **Line 850** (`reportArgumentType`)
  - **Issue**: Argument of type "Unknown | None" cannot be assigned to parameter "other_player_idx" of type "int" in function "\_handle_trade_action"
      Type "Unknown | None" is not assignable to type "int"
        "None" is not assignable to "int"
  - **Location**: `haive-games/src/haive/games/monopoly/game/game.py:850:16`

- [ ] **Line 859** (`reportArgumentType`)
  - **Issue**: Argument of type "Unknown | None" cannot be assigned to parameter "property_position" of type "int" in function "\_handle_auction_action"
      Type "Unknown | None" is not assignable to type "int"
        "None" is not assignable to "int"
  - **Location**: `haive-games/src/haive/games/monopoly/game/game.py:859:47`

- [ ] **Line 1243** (`reportOptionalMemberAccess`)
  - **Issue**: "owner" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/game/game.py:1243:17`

- [ ] **Line 1249** (`reportOptionalMemberAccess`)
  - **Issue**: "owner" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/game/game.py:1249:17`

### 📄 haive-games/src/haive/games/monopoly/game_agent.py

- [ ] **Line 62** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:62:19`

- [ ] **Line 63** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:63:19`

- [ ] **Line 64** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:64:19`

- [ ] **Line 65** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:65:19`

- [ ] **Line 66** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:66:19`

- [ ] **Line 67** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:67:19`

- [ ] **Line 68** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:68:19`

- [ ] **Line 71** (`reportOptionalMemberAccess`)
  - **Issue**: "set_entry_point" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:71:19`

- [ ] **Line 74** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:74:19`

- [ ] **Line 75** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:75:19`

- [ ] **Line 76** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:76:19`

- [ ] **Line 77** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:77:19`

- [ ] **Line 80** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:80:19`

- [ ] **Line 91** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:91:19`

- [ ] **Line 94** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:94:19`

- [ ] **Line 107** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "current_player" for class "BaseModel"
      Attribute "current_player" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:107:40`

- [ ] **Line 107** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "current_player" for class "dict[str, Any]"
      Attribute "current_player" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:107:40`

- [ ] **Line 110** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "doubles_rolled" for class "BaseModel"
      Attribute "doubles_rolled" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:110:30`

- [ ] **Line 110** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "doubles_rolled" for class "dict[str, Any]"
      Attribute "doubles_rolled" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:110:30`

- [ ] **Line 208** (`reportArgumentType`)
  - **Issue**: Argument of type "list[Player]" cannot be assigned to parameter "value" of type "list[GameEvent]" in function "**setitem**"
      "list[Player]" is not assignable to "list[GameEvent]"
        Type parameter "\_T@list" is invariant, but "Player" is not the same as "GameEvent"
        Consider switching from "list" to "Sequence" which is covariant
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:208:12`

- [ ] **Line 212** (`reportArgumentType`)
  - **Issue**: Argument of type "list[Player]" cannot be assigned to parameter "value" of type "list[GameEvent]" in function "**setitem**"
      "list[Player]" is not assignable to "list[GameEvent]"
        Type parameter "\_T@list" is invariant, but "Player" is not the same as "GameEvent"
        Consider switching from "list" to "Sequence" which is covariant
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:212:12`

- [ ] **Line 224** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "current_player" for class "BaseModel"
      Attribute "current_player" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:224:40`

- [ ] **Line 236** (`reportArgumentType`)
  - **Issue**: Argument of type "MonopolyState | BaseModel" cannot be assigned to parameter "state" of type "MonopolyState" in function "handle_special_space"
      Type "MonopolyState | BaseModel" is not assignable to type "MonopolyState"
        "BaseModel" is not assignable to "MonopolyState"
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:236:45`

- [ ] **Line 237** (`reportArgumentType`)
  - **Issue**: Argument of type "MonopolyState | BaseModel" cannot be assigned to parameter "state" of type "MonopolyState" in function "handle_property_space"
      Type "MonopolyState | BaseModel" is not assignable to type "MonopolyState"
        "BaseModel" is not assignable to "MonopolyState"
  - **Location**: `haive-games/src/haive/games/monopoly/game_agent.py:237:42`

### 📄 haive-games/src/haive/games/monopoly/generic_engines.py

- [ ] **Line 178** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "create_engines" for class "MonopolyEngineFactory"
      Attribute "create_engines" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/generic_engines.py:178:28`

### 📄 haive-games/src/haive/games/monopoly/main_agent.py

- [ ] **Line 42** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "setup_player_agent_engines" for class "MonopolyGameAgentConfig"
      Attribute "setup_player_agent_engines" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/main_agent.py:42:15`

- [ ] **Line 45** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "create_player_agent" for class "MonopolyGameAgentConfig"
      Attribute "create_player_agent" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/main_agent.py:45:35`

- [ ] **Line 48** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "create_initial_state" for class "MonopolyGameAgentConfig"
      Attribute "create_initial_state" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/main_agent.py:48:36`

- [ ] **Line 167** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "enable_building" for class "MonopolyGameAgentConfig"
      Attribute "enable_building" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/main_agent.py:167:48`

- [ ] **Line 168** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "enable_auctions" for class "MonopolyGameAgentConfig"
      Attribute "enable_auctions" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/main_agent.py:168:48`

### 📄 haive-games/src/haive/games/monopoly/player_agent.py

- [ ] **Line 197** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['waiting']" cannot be assigned to parameter "game_status" of type "GameStatus" in function "**init**"
      "Literal['waiting']" is not assignable to "GameStatus"
  - **Location**: `haive-games/src/haive/games/monopoly/player_agent.py:197:24`

- [ ] **Line 252** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/player_agent.py:252:19`

- [ ] **Line 253** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/player_agent.py:253:19`

- [ ] **Line 254** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/player_agent.py:254:19`

- [ ] **Line 255** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/player_agent.py:255:19`

- [ ] **Line 256** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/player_agent.py:256:19`

- [ ] **Line 259** (`reportOptionalMemberAccess`)
  - **Issue**: "set_entry_point" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/player_agent.py:259:19`

- [ ] **Line 262** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/player_agent.py:262:19`

- [ ] **Line 281** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/player_agent.py:281:23`

- [ ] **Line 323** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "decision_type" for class "BaseModel"
      Attribute "decision_type" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/player_agent.py:323:49`

- [ ] **Line 328** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "decision_type" for class "BaseModel"
      Attribute "decision_type" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/player_agent.py:328:78`

- [ ] **Line 525** (`reportCallIssue`)
  - **Issue**: Argument expression after \*\* must be a mapping with a "str" key type
  - **Location**: `haive-games/src/haive/games/monopoly/player_agent.py:525:37`

### 📄 haive-games/src/haive/games/monopoly/state.py

- [ ] **Line 501** (`reportCallIssue`)
  - **Issue**: No overloads for "sum" match the provided arguments
  - **Location**: `haive-games/src/haive/games/monopoly/state.py:501:23`

- [ ] **Line 501** (`reportArgumentType`)
  - **Issue**: Argument of type "Generator[(properties_dict: dict[str, Property]) -> int, None, None]" cannot be assigned to parameter "iterable" of type "Iterable[_SupportsSumNoDefaultT@sum]" in function "sum"
      "Generator[(properties_dict: dict[str, Property]) -> int, None, None]" is not assignable to "Iterable[_SupportsSumNoDefaultT@sum]"
        Type parameter "\_T_co@Iterable" is covariant, but "(properties_dict: dict[str, Property]) -> int" is not a subtype of "\_SupportsSumNoDefaultT@sum"
          Type "(properties_dict: dict[str, Property]) -> int" is not assignable to type "\_SupportsSumWithNoDefaultGiven"
            "MethodType" is incompatible with protocol "\_SupportsSumWithNoDefaultGiven"
              "**add**" is not present
              "**radd**" is not present
  - **Location**: `haive-games/src/haive/games/monopoly/state.py:501:27`

- [ ] **Line 505** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "key"
  - **Location**: `haive-games/src/haive/games/monopoly/state.py:505:8`

- [ ] **Line 513** (`reportOperatorIssue`)
  - **Issue**: Operator "+=" not supported for types "Literal[0]" and "(properties_dict: dict[str, Property]) -> int"
      Operator "+" not supported for types "Literal[0]" and "(properties_dict: dict[str, Property]) -> int"
  - **Location**: `haive-games/src/haive/games/monopoly/state.py:513:16`

- [ ] **Line 519** (`reportOperatorIssue`)
  - **Issue**: Operator "\*" not supported for types "int" and "(properties_dict: dict[str, Property]) -> int"
  - **Location**: `haive-games/src/haive/games/monopoly/state.py:519:24`

- [ ] **Line 520** (`reportCallIssue`)
  - **Issue**: No overloads for "sum" match the provided arguments
  - **Location**: `haive-games/src/haive/games/monopoly/state.py:520:31`

- [ ] **Line 520** (`reportArgumentType`)
  - **Issue**: Argument of type "list[(properties_dict: dict[str, Property]) -> int]" cannot be assigned to parameter "iterable" of type "Iterable[_SupportsSumNoDefaultT@sum]" in function "sum"
      "list[(properties_dict: dict[str, Property]) -> int]" is not assignable to "Iterable[_SupportsSumNoDefaultT@sum]"
        Type parameter "\_T_co@Iterable" is covariant, but "(properties_dict: dict[str, Property]) -> int" is not a subtype of "\_SupportsSumNoDefaultT@sum"
          Type "(properties_dict: dict[str, Property]) -> int" is not assignable to type "\_SupportsSumWithNoDefaultGiven"
            "MethodType" is incompatible with protocol "\_SupportsSumWithNoDefaultGiven"
              "**add**" is not present
              "**radd**" is not present
  - **Location**: `haive-games/src/haive/games/monopoly/state.py:520:35`

- [ ] **Line 520** (`reportCallIssue`)
  - **Issue**: No overloads for "sum" match the provided arguments
  - **Location**: `haive-games/src/haive/games/monopoly/state.py:520:54`

- [ ] **Line 520** (`reportArgumentType`)
  - **Issue**: Argument of type "list[(properties_dict: dict[str, Property]) -> int]" cannot be assigned to parameter "iterable" of type "Iterable[_SupportsSumNoDefaultT@sum]" in function "sum"
      "list[(properties_dict: dict[str, Property]) -> int]" is not assignable to "Iterable[_SupportsSumNoDefaultT@sum]"
        Type parameter "\_T_co@Iterable" is covariant, but "(properties_dict: dict[str, Property]) -> int" is not a subtype of "\_SupportsSumNoDefaultT@sum"
          Type "(properties_dict: dict[str, Property]) -> int" is not assignable to type "\_SupportsSumWithNoDefaultGiven"
            "MethodType" is incompatible with protocol "\_SupportsSumWithNoDefaultGiven"
              "**add**" is not present
              "**radd**" is not present
  - **Location**: `haive-games/src/haive/games/monopoly/state.py:520:58`

- [ ] **Line 568** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "hotels" for class "Property"
      Attribute "hotels" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/state.py:568:43`

- [ ] **Line 574** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "hotels" for class "Property"
      Attribute "hotels" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/state.py:574:43`

- [ ] **Line 583** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "type" for class "Property"
      Attribute "type" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/state.py:583:58`

- [ ] **Line 692** (`reportArgumentType`)
  - **Issue**: Argument of type "str" cannot be assigned to parameter "color" of type "PropertyColor" in function "get_properties_by_color"
      "str" is not assignable to "PropertyColor"
  - **Location**: `haive-games/src/haive/games/monopoly/state.py:692:46`

- [ ] **Line 925** (`reportOperatorIssue`)
  - **Issue**: Operator "+=" not supported for types "(properties_dict: dict[str, Property]) -> int" and "int"
      Operator "+" not supported for types "(properties_dict: dict[str, Property]) -> int" and "int"
  - **Location**: `haive-games/src/haive/games/monopoly/state.py:925:8`

- [ ] **Line 935** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "name", "position", "property_type", "color", "price", "rent", "mortgage_value"
  - **Location**: `haive-games/src/haive/games/monopoly/state.py:935:46`

- [ ] **Line 935** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "type" for class "Property"
      Attribute "type" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/state.py:935:58`

- [ ] **Line 962** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "name", "position", "property_type", "color", "price", "rent", "mortgage_value"
  - **Location**: `haive-games/src/haive/games/monopoly/state.py:962:46`

- [ ] **Line 962** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "type" for class "Property"
      Attribute "type" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/state.py:962:58`

- [ ] **Line 1046** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "hotels" for class "Property"
      Attribute "hotels" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/state.py:1046:31`

- [ ] **Line 1048** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "type" for class "Property"
      Attribute "type" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/state.py:1048:29`

- [ ] **Line 1048** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "type" for class "Property"
      Attribute "type" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/state.py:1048:48`

### 📄 haive-games/src/haive/games/monopoly/ui.py

- [ ] **Line 65** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "state" for class "MonopolyRichUI\*"
      Type "dict[str, Any]" is not assignable to type "MonopolyState | None"
        "dict[str, Any]" is not assignable to "MonopolyState"
        "dict[str, Any]" is not assignable to "None"
  - **Location**: `haive-games/src/haive/games/monopoly/ui.py:65:29`

- [ ] **Line 67** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "MonopolyState"
  - **Location**: `haive-games/src/haive/games/monopoly/ui.py:67:27`

- [ ] **Line 67** (`reportOptionalSubscript`)
  - **Issue**: Object of type "None" is not subscriptable
  - **Location**: `haive-games/src/haive/games/monopoly/ui.py:67:27`

- [ ] **Line 70** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "MonopolyState"
  - **Location**: `haive-games/src/haive/games/monopoly/ui.py:70:43`

- [ ] **Line 70** (`reportOptionalSubscript`)
  - **Issue**: Object of type "None" is not subscriptable
  - **Location**: `haive-games/src/haive/games/monopoly/ui.py:70:43`

- [ ] **Line 70** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "MonopolyState"
  - **Location**: `haive-games/src/haive/games/monopoly/ui.py:70:73`

- [ ] **Line 70** (`reportOptionalSubscript`)
  - **Issue**: Object of type "None" is not subscriptable
  - **Location**: `haive-games/src/haive/games/monopoly/ui.py:70:73`

- [ ] **Line 260** (`reportOptionalMemberAccess`)
  - **Issue**: "get_recent_events" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/ui.py:260:39`

- [ ] **Line 334** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "initial_state" for class "Agent[Unknown]"
      Attribute "initial_state" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/ui.py:334:30`

- [ ] **Line 337** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "initial_state" for class "Agent[Unknown]"
      Attribute "initial_state" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/ui.py:337:27`

- [ ] **Line 380** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "save_game_history" for class "Agent[Unknown]"
      Attribute "save_game_history" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/ui.py:380:18`

### 📄 haive-games/src/haive/games/monopoly/ui_fixed.py

- [ ] **Line 301** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "initial_state" for class "Agent[Unknown]"
      Attribute "initial_state" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/ui_fixed.py:301:30`

- [ ] **Line 330** (`reportOptionalMemberAccess`)
  - **Issue**: "error_message" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/ui_fixed.py:330:39`

- [ ] **Line 333** (`reportOptionalMemberAccess`)
  - **Issue**: "error_message" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/ui_fixed.py:333:61`

- [ ] **Line 338** (`reportOptionalMemberAccess`)
  - **Issue**: "game_status" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/monopoly/ui_fixed.py:338:34`

- [ ] **Line 353** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "save_game_history" for class "Agent[Unknown]"
      Attribute "save_game_history" is unknown
  - **Location**: `haive-games/src/haive/games/monopoly/ui_fixed.py:353:18`

### 📄 haive-games/src/haive/games/multi_player/agent.py

- [ ] **Line 153** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[bool, str]" cannot be assigned to parameter "routes" of type "dict[str, str]" in function "add_conditional_edges"
      "Literal[True]" is not assignable to "str"
      "Literal[False]" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:153:12`

- [ ] **Line 172** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[bool, str]" cannot be assigned to parameter "routes" of type "dict[str, str]" in function "add_conditional_edges"
      "Literal[True]" is not assignable to "str"
      "Literal[False]" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:172:12`

- [ ] **Line 181** (`reportRedeclaration`)
  - **Issue**: Method declaration "get_player_role" is obscured by a declaration of the same name
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:181:8`

- [ ] **Line 207** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "roles" for class "MultiPlayerGameState"
      Attribute "roles" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:207:30`

- [ ] **Line 208** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "roles" for class "MultiPlayerGameState"
      Attribute "roles" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:208:25`

- [ ] **Line 212** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "roles" for class "MultiPlayerGameState"
      Attribute "roles" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:212:40`

- [ ] **Line 213** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "roles" for class "MultiPlayerGameState"
      Attribute "roles" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:213:25`

- [ ] **Line 258** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "roles" for class "MultiPlayerGameState"
      Attribute "roles" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:258:41`

- [ ] **Line 262** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player_states" for class "MultiPlayerGameState"
      Attribute "player_states" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:262:25`

- [ ] **Line 268** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "action_history" for class "MultiPlayerGameState"
      Attribute "action_history" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:268:49`

- [ ] **Line 290** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player_states" for class "MultiPlayerGameState"
      Attribute "player_states" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:290:46`

- [ ] **Line 292** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "votes" for class "MultiPlayerGameState"
      Attribute "votes" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:292:25`

- [ ] **Line 300** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "roles" for class "MultiPlayerGameState"
      Attribute "roles" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:300:35`

- [ ] **Line 301** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "roles" for class "MultiPlayerGameState"
      Attribute "roles" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:301:40`

- [ ] **Line 303** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "roles" for class "MultiPlayerGameState"
      Attribute "roles" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:303:45`

- [ ] **Line 304** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "roles" for class "MultiPlayerGameState"
      Attribute "roles" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:304:40`

- [ ] **Line 316** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "action_history" for class "MultiPlayerGameState"
      Attribute "action_history" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:316:45`

- [ ] **Line 325** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player_states" for class "MultiPlayerGameState"
      Attribute "player_states" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:325:38`

- [ ] **Line 387** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "MultiPlayerGameAgent[T@MultiPlayerGameAgent]\*"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:387:29`

- [ ] **Line 439** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "MultiPlayerGameAgent[T@MultiPlayerGameAgent]\*"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:439:20`

- [ ] **Line 446** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "players" for class "BaseModel"
      Attribute "players" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:446:19`

- [ ] **Line 451** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "players" for class "BaseModel"
      Attribute "players" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:451:32`

- [ ] **Line 453** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "MultiPlayerGameAgent[T@MultiPlayerGameAgent]\*"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:453:26`

- [ ] **Line 472** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "MultiPlayerGameAgent[T@MultiPlayerGameAgent]\*"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:472:21`

- [ ] **Line 497** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "current_player" for class "BaseModel\*"
      Attribute "current_player" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:497:26`

- [ ] **Line 511** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "MultiPlayerGameAgent[T@MultiPlayerGameAgent]\*"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:511:17`

- [ ] **Line 521** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "MultiPlayerGameAgent[T@MultiPlayerGameAgent]\*"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:521:29`

- [ ] **Line 524** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "MultiPlayerGameAgent[T@MultiPlayerGameAgent]\*"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:524:29`

- [ ] **Line 549** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "MultiPlayerGameAgent[T@MultiPlayerGameAgent]\*"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:549:29`

- [ ] **Line 552** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "MultiPlayerGameAgent[T@MultiPlayerGameAgent]\*"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:552:29`

- [ ] **Line 595** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "game_status" for class "BaseModel\*"
      Attribute "game_status" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:595:21`

- [ ] **Line 608** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "game_status" for class "BaseModel\*"
      Attribute "game_status" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:608:21`

- [ ] **Line 622** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "current_player_idx" for class "BaseModel\*"
      Attribute "current_player_idx" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:622:21`

- [ ] **Line 622** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "round_number" for class "BaseModel\*"
      Attribute "round_number" is unknown
  - **Location**: `haive-games/src/haive/games/multi_player/agent.py:622:55`

### 📄 haive-games/src/haive/games/multi_player/config.py

- [ ] **Line 65** (`reportGeneralTypeIssues`)
  - **Issue**: "state_schema" overrides a field of the same name but is missing a default value
  - **Location**: `haive-games/src/haive/games/multi_player/config.py:65:4`

- [ ] **Line 71** (`reportGeneralTypeIssues`)
  - **Issue**: "engines" overrides a field of the same name but is missing a default value
  - **Location**: `haive-games/src/haive/games/multi_player/config.py:71:4`

### 📄 haive-games/src/haive/games/multi_player/factory.py

- [ ] **Line 69** (`reportArgumentType`)
  - **Issue**: Expression of type "None" cannot be assigned to parameter of type "dict[str, (...) -> Unknown]"
      "None" is not assignable to "dict[str, (...) -> Unknown]"
  - **Location**: `haive-games/src/haive/games/multi_player/factory.py:69:46`

- [ ] **Line 118** (`reportCallIssue`)
  - **Issue**: No parameter named "state_schema"
  - **Location**: `haive-games/src/haive/games/multi_player/factory.py:118:24`

- [ ] **Line 119** (`reportCallIssue`)
  - **Issue**: No parameter named "aug_llm_configs"
  - **Location**: `haive-games/src/haive/games/multi_player/factory.py:119:24`

- [ ] **Line 120** (`reportCallIssue`)
  - **Issue**: No parameter named "player_roles"
  - **Location**: `haive-games/src/haive/games/multi_player/factory.py:120:24`

- [ ] **Line 121** (`reportCallIssue`)
  - **Issue**: No parameter named "visualize"
  - **Location**: `haive-games/src/haive/games/multi_player/factory.py:121:24`

### 📄 haive-games/src/haive/games/nim/agent.py

- [ ] **Line 53** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state" for class "Command[Unknown]"
      Attribute "state" is unknown
  - **Location**: `haive-games/src/haive/games/nim/agent.py:53:57`

- [ ] **Line 54** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state" for class "Command[Unknown]"
      Attribute "state" is unknown
  - **Location**: `haive-games/src/haive/games/nim/agent.py:54:49`

- [ ] **Line 107** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "pile_sizes" for class "GameConfig"
      Attribute "pile_sizes" is unknown
  - **Location**: `haive-games/src/haive/games/nim/agent.py:107:35`

- [ ] **Line 107** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "misere_mode" for class "GameConfig"
      Attribute "misere_mode" is unknown
  - **Location**: `haive-games/src/haive/games/nim/agent.py:107:71`

- [ ] **Line 338** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "pile_sizes" for class "GameConfig"
      Attribute "pile_sizes" is unknown
  - **Location**: `haive-games/src/haive/games/nim/agent.py:338:35`

- [ ] **Line 338** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "misere_mode" for class "GameConfig"
      Attribute "misere_mode" is unknown
  - **Location**: `haive-games/src/haive/games/nim/agent.py:338:71`

- [ ] **Line 430** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "pile_sizes" for class "GameConfig"
      Attribute "pile_sizes" is unknown
  - **Location**: `haive-games/src/haive/games/nim/agent.py:430:35`

- [ ] **Line 430** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "misere_mode" for class "GameConfig"
      Attribute "misere_mode" is unknown
  - **Location**: `haive-games/src/haive/games/nim/agent.py:430:71`

### 📄 haive-games/src/haive/games/nim/engines.py

- [ ] **Line 84** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/nim/engines.py:84:50`

- [ ] **Line 90** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/nim/engines.py:90:50`

- [ ] **Line 96** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/nim/engines.py:96:50`

- [ ] **Line 102** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/nim/engines.py:102:50`

### 📄 haive-games/src/haive/games/nim/example.py

- [ ] **Line 782** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "key" of type "str" in function "**getitem**"
      Type "str | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/nim/example.py:782:12`

- [ ] **Line 782** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "key" of type "str" in function "**setitem**"
      Type "str | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/nim/example.py:782:12`

### 📄 haive-games/src/haive/games/nim/generic_engines.py

- [ ] **Line 101** (`reportAbstractUsage`)
  - **Issue**: Cannot instantiate abstract class "NimPromptGenerator"
      "GenericPromptGenerator.create_analysis_prompt" is not implemented
      "GenericPromptGenerator.get_move_output_model" is not implemented
      and 1 more...
  - **Location**: `haive-games/src/haive/games/nim/generic_engines.py:101:27`

- [ ] **Line 101** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "players"
  - **Location**: `haive-games/src/haive/games/nim/generic_engines.py:101:27`

- [ ] **Line 134** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "create_engines" for class "NimEngineFactory"
      Attribute "create_engines" is unknown
  - **Location**: `haive-games/src/haive/games/nim/generic_engines.py:134:23`

### 📄 haive-games/src/haive/games/nim/standalone_game.py

- [ ] **Line 109** (`reportOptionalMemberAccess`)
  - **Issue**: "clear" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/nim/standalone_game.py:109:21`

- [ ] **Line 158** (`reportOptionalMemberAccess`)
  - **Issue**: "print" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/nim/standalone_game.py:158:21`

- [ ] **Line 159** (`reportOptionalMemberAccess`)
  - **Issue**: "print" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/nim/standalone_game.py:159:21`

- [ ] **Line 162** (`reportOptionalMemberAccess`)
  - **Issue**: "print" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/nim/standalone_game.py:162:25`

- [ ] **Line 306** (`reportArgumentType`)
  - **Issue**: Expression of type "None" cannot be assigned to parameter of type "list[int]"
      "None" is not assignable to "list[int]"
  - **Location**: `haive-games/src/haive/games/nim/standalone_game.py:306:43`

### 📄 haive-games/src/haive/games/nim/state_manager.py

- [ ] **Line 36** (`reportArgumentType`)
  - **Issue**: Expression of type "None" cannot be assigned to parameter of type "str"
      "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/nim/state_manager.py:36:60`

- [ ] **Line 201** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "game_status" for class "NimState"
      Type "LiteralString" is not assignable to type "Literal['in_progress', 'player1_win', 'player2_win']"
        "str" is not assignable to "Literal['in_progress']"
        "str" is not assignable to "Literal['player1_win']"
        "str" is not assignable to "Literal['player2_win']"
  - **Location**: `haive-games/src/haive/games/nim/state_manager.py:201:36`

### 📄 haive-games/src/haive/games/nim/ui.py

- [ ] **Line 376** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "player"
  - **Location**: `haive-games/src/haive/games/nim/ui.py:376:23`

### 📄 haive-games/src/haive/games/poker/agent.py

- [ ] **Line 86** (`reportOptionalOperand`)
  - **Issue**: Operator "|" not supported for "None"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:86:37`

- [ ] **Line 161** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:161:23`

- [ ] **Line 162** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:162:23`

- [ ] **Line 163** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:163:23`

- [ ] **Line 164** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:164:23`

- [ ] **Line 165** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:165:23`

- [ ] **Line 166** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:166:23`

- [ ] **Line 169** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:169:23`

- [ ] **Line 170** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:170:23`

- [ ] **Line 171** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:171:23`

- [ ] **Line 174** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:174:23`

- [ ] **Line 185** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:185:23`

- [ ] **Line 192** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:192:23`

- [ ] **Line 199** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:199:23`

- [ ] **Line 334** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "has_folded" for class "Player"
      Attribute "has_folded" is unknown
  - **Location**: `haive-games/src/haive/games/poker/agent.py:334:59`

- [ ] **Line 343** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "has_folded" for class "Player"
      Attribute "has_folded" is unknown
  - **Location**: `haive-games/src/haive/games/poker/agent.py:343:26`

- [ ] **Line 347** (`reportArgumentType`)
  - **Issue**: Argument of type "PokerGameState" cannot be assigned to parameter "game" of type "PokerState" in function "\_get_next_player_idx"
      "PokerGameState" is not assignable to "PokerState"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:347:64`

- [ ] **Line 355** (`reportArgumentType`)
  - **Issue**: Argument of type "PokerGameState" cannot be assigned to parameter "game" of type "PokerState" in function "\_get_next_player_idx"
      "PokerGameState" is not assignable to "PokerState"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:355:64`

- [ ] **Line 375** (`reportArgumentType`)
  - **Issue**: Argument of type "PokerGameState" cannot be assigned to parameter "state" of type "PokerState" in function "\_get_legal_actions"
      "PokerGameState" is not assignable to "PokerState"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:375:48`

- [ ] **Line 420** (`reportArgumentType`)
  - **Issue**: Argument of type "PokerGameState" cannot be assigned to parameter "game" of type "PokerState" in function "\_apply_player_decision"
      "PokerGameState" is not assignable to "PokerState"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:420:20`

- [ ] **Line 431** (`reportArgumentType`)
  - **Issue**: Argument of type "PokerGameState" cannot be assigned to parameter "game" of type "PokerState" in function "\_get_next_player_idx"
      "PokerGameState" is not assignable to "PokerState"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:431:68`

- [ ] **Line 439** (`reportArgumentType`)
  - **Issue**: Argument of type "PokerGameState" cannot be assigned to parameter "game" of type "PokerState" in function "\_apply_player_decision"
      "PokerGameState" is not assignable to "PokerState"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:439:20`

- [ ] **Line 441** (`reportArgumentType`)
  - **Issue**: Argument of type "PokerGameState" cannot be assigned to parameter "game" of type "PokerState" in function "\_get_next_player_idx"
      "PokerGameState" is not assignable to "PokerState"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:441:68`

- [ ] **Line 451** (`reportArgumentType`)
  - **Issue**: Argument of type "PokerGameState" cannot be assigned to parameter "game" of type "PokerState" in function "\_apply_player_decision"
      "PokerGameState" is not assignable to "PokerState"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:451:16`

- [ ] **Line 453** (`reportArgumentType`)
  - **Issue**: Argument of type "PokerGameState" cannot be assigned to parameter "game" of type "PokerState" in function "\_get_next_player_idx"
      "PokerGameState" is not assignable to "PokerState"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:453:64`

- [ ] **Line 486** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "content" for class "dict[Unknown, Unknown]"
      Attribute "content" is unknown
  - **Location**: `haive-games/src/haive/games/poker/agent.py:486:43`

- [ ] **Line 519** (`reportArgumentType`)
  - **Issue**: Argument of type "str | Any" cannot be assigned to parameter "action" of type "PlayerAction" in function "**init**"
      Type "str | Any" is not assignable to type "PlayerAction"
        "str" is not assignable to "PlayerAction"
  - **Location**: `haive-games/src/haive/games/poker/agent.py:519:43`

- [ ] **Line 736** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "has_folded" for class "Player"
      Attribute "has_folded" is unknown
  - **Location**: `haive-games/src/haive/games/poker/agent.py:736:19`

- [ ] **Line 737** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "current_player_idx" for class "PokerState"
      Attribute "current_player_idx" is unknown
  - **Location**: `haive-games/src/haive/games/poker/agent.py:737:17`

- [ ] **Line 744** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "current_player_idx" for class "PokerState"
      Attribute "current_player_idx" is unknown
  - **Location**: `haive-games/src/haive/games/poker/agent.py:744:17`

- [ ] **Line 747** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "current_player_idx" for class "PokerState"
      Attribute "current_player_idx" is unknown
  - **Location**: `haive-games/src/haive/games/poker/agent.py:747:17`

- [ ] **Line 753** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "current_player_idx" for class "PokerState"
      Attribute "current_player_idx" is unknown
  - **Location**: `haive-games/src/haive/games/poker/agent.py:753:27`

- [ ] **Line 754** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "players" for class "PokerState"
      Attribute "players" is unknown
  - **Location**: `haive-games/src/haive/games/poker/agent.py:754:48`

- [ ] **Line 755** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "players" for class "PokerState"
      Attribute "players" is unknown
  - **Location**: `haive-games/src/haive/games/poker/agent.py:755:19`

- [ ] **Line 756** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "players" for class "PokerState"
      Attribute "players" is unknown
  - **Location**: `haive-games/src/haive/games/poker/agent.py:756:49`

- [ ] **Line 918** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "winner" for class "PokerGameState"
      Attribute "winner" is unknown
  - **Location**: `haive-games/src/haive/games/poker/agent.py:918:23`

### 📄 haive-games/src/haive/games/poker/example.py

- [ ] **Line 244** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "current_game_state" for class "PokerUI"
      Expression of type "dict[str, PokerGameState]" cannot be assigned to attribute "current_game_state" of class "PokerUI"
        "dict[str, PokerGameState]" is not assignable to "None"
  - **Location**: `haive-games/src/haive/games/poker/example.py:244:15`

### 📄 haive-games/src/haive/games/poker/generic_engines.py

- [ ] **Line 101** (`reportAbstractUsage`)
  - **Issue**: Cannot instantiate abstract class "PokerPromptGenerator"
      "GenericPromptGenerator.create_analysis_prompt" is not implemented
      "GenericPromptGenerator.get_move_output_model" is not implemented
      and 1 more...
  - **Location**: `haive-games/src/haive/games/poker/generic_engines.py:101:27`

- [ ] **Line 101** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "players"
  - **Location**: `haive-games/src/haive/games/poker/generic_engines.py:101:27`

- [ ] **Line 134** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "create_engines" for class "PokerEngineFactory"
      Attribute "create_engines" is unknown
  - **Location**: `haive-games/src/haive/games/poker/generic_engines.py:134:25`

### 📄 haive-games/src/haive/games/poker/state.py

- [ ] **Line 730** (`reportArgumentType`)
  - **Issue**: Argument of type "list[int]" cannot be assigned to parameter "high_cards" of type "list[CardValue]" in function "**init**"
      "list[int]" is not assignable to "list[CardValue]"
        Type parameter "\_T@list" is invariant, but "int" is not the same as "CardValue"
        Consider switching from "list" to "Sequence" which is covariant
  - **Location**: `haive-games/src/haive/games/poker/state.py:730:31`

### 📄 haive-games/src/haive/games/poker/ui.py

- [ ] **Line 114** (`reportGeneralTypeIssues`)
  - **Issue**: "Never" is not iterable
  - **Location**: `haive-games/src/haive/games/poker/ui.py:114:46`

- [ ] **Line 146** (`reportGeneralTypeIssues`)
  - **Issue**: "Never" is not iterable
  - **Location**: `haive-games/src/haive/games/poker/ui.py:146:38`

- [ ] **Line 183** (`reportGeneralTypeIssues`)
  - **Issue**: "Never" is not iterable
  - **Location**: `haive-games/src/haive/games/poker/ui.py:183:52`

- [ ] **Line 191** (`reportGeneralTypeIssues`)
  - **Issue**: "Never" is not iterable
  - **Location**: `haive-games/src/haive/games/poker/ui.py:191:46`

- [ ] **Line 235** (`reportGeneralTypeIssues`)
  - **Issue**: "Never" is not iterable
  - **Location**: `haive-games/src/haive/games/poker/ui.py:235:22`

### 📄 haive-games/src/haive/games/reversi/agent.py

- [ ] **Line 42** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "first_player" for class "GameConfig"
      Attribute "first_player" is unknown
  - **Location**: `haive-games/src/haive/games/reversi/agent.py:42:37`

- [ ] **Line 43** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player_B" for class "GameConfig"
      Attribute "player_B" is unknown
  - **Location**: `haive-games/src/haive/games/reversi/agent.py:43:33`

- [ ] **Line 44** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player_W" for class "GameConfig"
      Attribute "player_W" is unknown
  - **Location**: `haive-games/src/haive/games/reversi/agent.py:44:33`

- [ ] **Line 453** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "first_player" for class "GameConfig"
      Attribute "first_player" is unknown
  - **Location**: `haive-games/src/haive/games/reversi/agent.py:453:41`

### 📄 haive-games/src/haive/games/reversi/engines.py

- [ ] **Line 78** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/reversi/engines.py:78:50`

- [ ] **Line 84** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/reversi/engines.py:84:50`

- [ ] **Line 90** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/reversi/engines.py:90:50`

- [ ] **Line 96** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/reversi/engines.py:96:50`

### 📄 haive-games/src/haive/games/reversi/example.py

- [ ] **Line 46** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "config"
  - **Location**: `haive-games/src/haive/games/reversi/example.py:46:12`

### 📄 haive-games/src/haive/games/reversi/generic_engines.py

- [ ] **Line 101** (`reportAbstractUsage`)
  - **Issue**: Cannot instantiate abstract class "ReversiPromptGenerator"
      "GenericPromptGenerator.create_analysis_prompt" is not implemented
      "GenericPromptGenerator.get_move_output_model" is not implemented
      and 1 more...
  - **Location**: `haive-games/src/haive/games/reversi/generic_engines.py:101:27`

- [ ] **Line 101** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "players"
  - **Location**: `haive-games/src/haive/games/reversi/generic_engines.py:101:27`

- [ ] **Line 134** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "create_engines" for class "ReversiEngineFactory"
      Attribute "create_engines" is unknown
  - **Location**: `haive-games/src/haive/games/reversi/generic_engines.py:134:27`

### 📄 haive-games/src/haive/games/reversi/state.py

- [ ] **Line 37** (`reportGeneralTypeIssues`)
  - **Issue**: "turn" overrides a field of the same name but is missing a default value
  - **Location**: `haive-games/src/haive/games/reversi/state.py:37:4`

### 📄 haive-games/src/haive/games/reversi/state_manager.py

- [ ] **Line 51** (`reportCallIssue`)
  - **Issue**: No overloads for "**setitem**" match the provided arguments
  - **Location**: `haive-games/src/haive/games/reversi/state_manager.py:51:8`

- [ ] **Line 51** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['W']" cannot be assigned to parameter "value" of type "None" in function "**setitem**"
      "Literal['W']" is not assignable to "None"
  - **Location**: `haive-games/src/haive/games/reversi/state_manager.py:51:8`

- [ ] **Line 52** (`reportCallIssue`)
  - **Issue**: No overloads for "**setitem**" match the provided arguments
  - **Location**: `haive-games/src/haive/games/reversi/state_manager.py:52:8`

- [ ] **Line 52** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['B']" cannot be assigned to parameter "value" of type "None" in function "**setitem**"
      "Literal['B']" is not assignable to "None"
  - **Location**: `haive-games/src/haive/games/reversi/state_manager.py:52:8`

- [ ] **Line 53** (`reportCallIssue`)
  - **Issue**: No overloads for "**setitem**" match the provided arguments
  - **Location**: `haive-games/src/haive/games/reversi/state_manager.py:53:8`

- [ ] **Line 53** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['B']" cannot be assigned to parameter "value" of type "None" in function "**setitem**"
      "Literal['B']" is not assignable to "None"
  - **Location**: `haive-games/src/haive/games/reversi/state_manager.py:53:8`

- [ ] **Line 54** (`reportCallIssue`)
  - **Issue**: No overloads for "**setitem**" match the provided arguments
  - **Location**: `haive-games/src/haive/games/reversi/state_manager.py:54:8`

- [ ] **Line 54** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['W']" cannot be assigned to parameter "value" of type "None" in function "**setitem**"
      "Literal['W']" is not assignable to "None"
  - **Location**: `haive-games/src/haive/games/reversi/state_manager.py:54:8`

- [ ] **Line 57** (`reportArgumentType`)
  - **Issue**: Argument of type "list[list[None]]" cannot be assigned to parameter "board" of type "list[list[str | None]]" in function "**init**"
      "list[list[None]]" is not assignable to "list[list[str | None]]"
        Type parameter "\_T@list" is invariant, but "list[None]" is not the same as "list[str | None]"
        Consider switching from "list" to "Sequence" which is covariant
  - **Location**: `haive-games/src/haive/games/reversi/state_manager.py:57:18`

- [ ] **Line 231** (`reportArgumentType`)
  - **Issue**: Argument of type "ReversiAnalysis" cannot be assigned to parameter "object" of type "dict[str, Any]" in function "append"
      "ReversiAnalysis" is not assignable to "dict[str, Any]"
  - **Location**: `haive-games/src/haive/games/reversi/state_manager.py:231:46`

- [ ] **Line 233** (`reportArgumentType`)
  - **Issue**: Argument of type "ReversiAnalysis" cannot be assigned to parameter "object" of type "dict[str, Any]" in function "append"
      "ReversiAnalysis" is not assignable to "dict[str, Any]"
  - **Location**: `haive-games/src/haive/games/reversi/state_manager.py:233:46`

### 📄 haive-games/src/haive/games/risk/agent.py

- [ ] **Line 420** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "from_territory", "to_territory", "armies", "cards", "attack_dice"
  - **Location**: `haive-games/src/haive/games/risk/agent.py:420:19`

- [ ] **Line 420** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "END_TURN" for class "type[MoveType]"
      Attribute "END_TURN" is unknown
  - **Location**: `haive-games/src/haive/games/risk/agent.py:420:47`

- [ ] **Line 456** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "armies", "cards"
  - **Location**: `haive-games/src/haive/games/risk/agent.py:456:19`

- [ ] **Line 482** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "from_territory", "cards", "attack_dice"
  - **Location**: `haive-games/src/haive/games/risk/agent.py:482:15`

### 📄 haive-games/src/haive/games/risk/example.py

- [ ] **Line 42** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "strategic_assessment" for class "RiskAnalysis"
      Attribute "strategic_assessment" is unknown
  - **Location**: `haive-games/src/haive/games/risk/example.py:42:54`

### 📄 haive-games/src/haive/games/risk/generic_engines.py

- [ ] **Line 101** (`reportAbstractUsage`)
  - **Issue**: Cannot instantiate abstract class "RiskPromptGenerator"
      "GenericPromptGenerator.create_analysis_prompt" is not implemented
      "GenericPromptGenerator.get_move_output_model" is not implemented
      and 1 more...
  - **Location**: `haive-games/src/haive/games/risk/generic_engines.py:101:27`

- [ ] **Line 101** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "players"
  - **Location**: `haive-games/src/haive/games/risk/generic_engines.py:101:27`

- [ ] **Line 134** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "create_engines" for class "RiskEngineFactory"
      Attribute "create_engines" is unknown
  - **Location**: `haive-games/src/haive/games/risk/generic_engines.py:134:24`

### 📄 haive-games/src/haive/games/risk/models.py

- [ ] **Line 616** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "territory_name"
  - **Location**: `haive-games/src/haive/games/risk/models.py:616:13`

- [ ] **Line 874** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "territory_name"
  - **Location**: `haive-games/src/haive/games/risk/models.py:874:16`

- [ ] **Line 875** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "territory_name"
  - **Location**: `haive-games/src/haive/games/risk/models.py:875:16`

- [ ] **Line 876** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "territory_name"
  - **Location**: `haive-games/src/haive/games/risk/models.py:876:16`

### 📄 haive-games/src/haive/games/risk/state.py

- [ ] **Line 316** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "owner"
  - **Location**: `haive-games/src/haive/games/risk/state.py:316:51`

- [ ] **Line 337** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "territory_name"
  - **Location**: `haive-games/src/haive/games/risk/state.py:337:25`

- [ ] **Line 338** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "territory_name"
  - **Location**: `haive-games/src/haive/games/risk/state.py:338:25`

### 📄 haive-games/src/haive/games/risk/state_manager.py

- [ ] **Line 322** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "key" of type "str" in function "**getitem**"
      Type "str | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/risk/state_manager.py:322:20`

- [ ] **Line 323** (`reportOperatorIssue`)
  - **Issue**: Operator "+=" not supported for types "int" and "int | None"
      Operator "+" not supported for types "int" and "None"
  - **Location**: `haive-games/src/haive/games/risk/state_manager.py:323:8`

- [ ] **Line 327** (`reportOperatorIssue`)
  - **Issue**: Operator "-=" not supported for types "int" and "int | None"
      Operator "-" not supported for types "int" and "None"
  - **Location**: `haive-games/src/haive/games/risk/state_manager.py:327:8`

- [ ] **Line 348** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "key" of type "str" in function "**getitem**"
      Type "str | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/risk/state_manager.py:348:29`

- [ ] **Line 349** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "key" of type "str" in function "**getitem**"
      Type "str | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/risk/state_manager.py:349:29`

- [ ] **Line 355** (`reportArgumentType`)
  - **Issue**: Argument of type "int | None" cannot be assigned to parameter "stop" of type "SupportsIndex" in function "**new**"
      Type "int | None" is not assignable to type "SupportsIndex"
        "None" is incompatible with protocol "SupportsIndex"
          "**index**" is not present
  - **Location**: `haive-games/src/haive/games/risk/state_manager.py:355:62`

- [ ] **Line 395** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "player_name" of type "str" in function "get_controlled_territories"
      Type "str | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/risk/state_manager.py:395:16`

- [ ] **Line 398** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "key" of type "str" in function "**getitem**"
      Type "str | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/risk/state_manager.py:398:16`

- [ ] **Line 401** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "key" of type "str" in function "**getitem**"
      Type "str | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/risk/state_manager.py:401:33`

- [ ] **Line 403** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "key" of type "str" in function "**getitem**"
      Type "str | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/risk/state_manager.py:403:16`

- [ ] **Line 424** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "key" of type "str" in function "**getitem**"
      Type "str | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/risk/state_manager.py:424:25`

- [ ] **Line 425** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "key" of type "str" in function "**getitem**"
      Type "str | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/risk/state_manager.py:425:23`

- [ ] **Line 427** (`reportOperatorIssue`)
  - **Issue**: Operator "-=" not supported for types "int" and "int | None"
      Operator "-" not supported for types "int" and "None"
  - **Location**: `haive-games/src/haive/games/risk/state_manager.py:427:8`

- [ ] **Line 428** (`reportOperatorIssue`)
  - **Issue**: Operator "+=" not supported for types "int" and "int | None"
      Operator "+" not supported for types "int" and "None"
  - **Location**: `haive-games/src/haive/games/risk/state_manager.py:428:8`

- [ ] **Line 455** (`reportOptionalIterable`)
  - **Issue**: Object of type "None" cannot be used as iterable value
  - **Location**: `haive-games/src/haive/games/risk/state_manager.py:455:20`

- [ ] **Line 459** (`reportArgumentType`)
  - **Issue**: Argument of type "list[Card] | None" cannot be assigned to parameter "iterable" of type "Iterable[Card]" in function "extend"
      Type "list[Card] | None" is not assignable to type "Iterable[Card]"
        "None" is incompatible with protocol "Iterable[Card]"
          "**iter**" is not present
  - **Location**: `haive-games/src/haive/games/risk/state_manager.py:459:31`

### 📄 haive-games/src/haive/games/single_player/base.py

- [ ] **Line 198** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "hint_count" for class "BaseModel\*"
      Attribute "hint_count" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/base.py:198:18`

- [ ] **Line 198** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "hint_count" for class "BaseModel\*"
      Attribute "hint_count" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/base.py:198:18`

- [ ] **Line 255** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "error_message" for class "BaseModel\*"
      Attribute "error_message" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/base.py:255:22`

- [ ] **Line 257** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "game_status" for class "BaseModel\*"
      Attribute "game_status" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/base.py:257:22`

- [ ] **Line 258** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "error_message" for class "BaseModel\*"
      Attribute "error_message" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/base.py:258:22`

- [ ] **Line 260** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "move_count" for class "BaseModel\*"
      Attribute "move_count" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/base.py:260:30`

- [ ] **Line 261** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "hint_count" for class "BaseModel\*"
      Attribute "hint_count" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/base.py:261:30`

- [ ] **Line 262** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "error_message" for class "BaseModel\*"
      Attribute "error_message" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/base.py:262:22`

- [ ] **Line 402** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "initialize" for class "None"
      Attribute "initialize" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/base.py:402:40`

- [ ] **Line 442** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "apply_move" for class "None"
      Attribute "apply_move" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/base.py:442:47`

- [ ] **Line 492** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "analysis_history" for class "BaseModel\*"
      Attribute "analysis_history" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/base.py:492:46`

- [ ] **Line 509** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "hint_count" for class "BaseModel\*"
      Attribute "hint_count" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/base.py:509:17`

- [ ] **Line 513** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "generate_hint" for class "None"
      Attribute "generate_hint" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/base.py:513:50`

- [ ] **Line 551** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "interactive_input" for class "None"
      Attribute "interactive_input" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/base.py:551:39`

- [ ] **Line 618** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "game_status" for class "BaseModel\*"
      Attribute "game_status" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/base.py:618:21`

### 📄 haive-games/src/haive/games/single_player/crossword_puzzle/base.py

- [ ] **Line 7** (`reportMissingImports`)
  - **Issue**: Import "game_framework_base" could not be resolved
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/base.py:7:5`

- [ ] **Line 36** (`reportUndefinedVariable`)
  - **Issue**: "CrosswordLetter" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/base.py:36:30`

- [ ] **Line 58** (`reportUndefinedVariable`)
  - **Issue**: "CrosswordLetter" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/base.py:58:57`

- [ ] **Line 66** (`reportUndefinedVariable`)
  - **Issue**: "CrosswordLetter" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/base.py:66:57`

- [ ] **Line 145** (`reportUndefinedVariable`)
  - **Issue**: "CrosswordLetter" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/base.py:145:39`

- [ ] **Line 148** (`reportUndefinedVariable`)
  - **Issue**: "CrosswordBoard" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/base.py:148:11`

- [ ] **Line 157** (`reportGeneralTypeIssues`)
  - **Issue**: Expected class but received "(iterable: Iterable[object], /) -> bool"
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/base.py:157:60`

- [ ] **Line 179** (`reportGeneralTypeIssues`)
  - **Issue**: Expected class but received "(iterable: Iterable[object], /) -> bool"
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/base.py:179:56`

- [ ] **Line 323** (`reportGeneralTypeIssues`)
  - **Issue**: Expected class but received "(iterable: Iterable[object], /) -> bool"
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/base.py:323:26`

- [ ] **Line 328** (`reportUndefinedVariable`)
  - **Issue**: "CrosswordBoard" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/base.py:328:16`

### 📄 haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py

- [ ] **Line 5** (`reportUndefinedVariable`)
  - **Issue**: "GridBoard" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:5:4`

- [ ] **Line 5** (`reportUndefinedVariable`)
  - **Issue**: "CrosswordCell" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:5:14`

- [ ] **Line 5** (`reportUndefinedVariable`)
  - **Issue**: "CrosswordLetter" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:5:28`

- [ ] **Line 5** (`reportUndefinedVariable`)
  - **Issue**: "GridPosition" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:5:46`

- [ ] **Line 5** (`reportUndefinedVariable`)
  - **Issue**: "CrosswordLetter" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:5:60`

- [ ] **Line 9** (`reportUndefinedVariable`)
  - **Issue**: "CrosswordWord" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:9:21`

- [ ] **Line 10** (`reportUndefinedVariable`)
  - **Issue**: "CrosswordClue" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:10:21`

- [ ] **Line 17** (`reportUndefinedVariable`)
  - **Issue**: "GridPosition" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:17:27`

- [ ] **Line 18** (`reportUndefinedVariable`)
  - **Issue**: "CrosswordCell" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:18:23`

- [ ] **Line 18** (`reportUndefinedVariable`)
  - **Issue**: "CrosswordLetter" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:18:37`

- [ ] **Line 34** (`reportUndefinedVariable`)
  - **Issue**: "GridPosition" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:34:38`

- [ ] **Line 34** (`reportUndefinedVariable`)
  - **Issue**: "CellType" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:34:63`

- [ ] **Line 51** (`reportUndefinedVariable`)
  - **Issue**: "Direction" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:51:19`

- [ ] **Line 54** (`reportUndefinedVariable`)
  - **Issue**: "GridPosition" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:54:24`

- [ ] **Line 62** (`reportUndefinedVariable`)
  - **Issue**: "CrosswordClue" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:62:15`

- [ ] **Line 76** (`reportUndefinedVariable`)
  - **Issue**: "CrosswordWord" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:76:15`

- [ ] **Line 95** (`reportUndefinedVariable`)
  - **Issue**: "GridPosition" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:95:24`

- [ ] **Line 103** (`reportUndefinedVariable`)
  - **Issue**: "CrosswordLetter" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:103:23`

- [ ] **Line 114** (`reportUndefinedVariable`)
  - **Issue**: "GridPosition" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:114:37`

- [ ] **Line 120** (`reportUndefinedVariable`)
  - **Issue**: "CrosswordLetter" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:120:42`

- [ ] **Line 143** (`reportUndefinedVariable`)
  - **Issue**: "GridPosition" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:143:41`

- [ ] **Line 143** (`reportUndefinedVariable`)
  - **Issue**: "Direction" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:143:66`

- [ ] **Line 165** (`reportUndefinedVariable`)
  - **Issue**: "CrosswordLetter" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:165:42`

- [ ] **Line 173** (`reportUndefinedVariable`)
  - **Issue**: "GridPosition" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:173:41`

- [ ] **Line 173** (`reportUndefinedVariable`)
  - **Issue**: "Direction" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:173:66`

- [ ] **Line 174** (`reportUndefinedVariable`)
  - **Issue**: "GridPosition" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:174:14`

- [ ] **Line 179** (`reportUndefinedVariable`)
  - **Issue**: "Direction" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:179:28`

- [ ] **Line 180** (`reportUndefinedVariable`)
  - **Issue**: "GridPosition" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:180:22`

- [ ] **Line 182** (`reportUndefinedVariable`)
  - **Issue**: "GridPosition" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:182:22`

- [ ] **Line 188** (`reportUndefinedVariable`)
  - **Issue**: "computed_field" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:188:5`

- [ ] **Line 194** (`reportUndefinedVariable`)
  - **Issue**: "CrosswordCell" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:194:33`

- [ ] **Line 196** (`reportUndefinedVariable`)
  - **Issue**: "CrosswordLetter" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/board.py:196:33`

### 📄 haive-games/src/haive/games/single_player/crossword_puzzle/game/piece.py

- [ ] **Line 3** (`reportMissingImports`)
  - **Issue**: Import "haive.games.core.piece.base" could not be resolved
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/piece.py:3:5`

- [ ] **Line 6** (`reportAttributeAccessIssue`)
  - **Issue**: "CrosswordCell" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/single_player/crossword_puzzle/game/piece.py:6:65`

### 📄 haive-games/src/haive/games/single_player/example.py

- [ ] **Line 1** (`reportUndefinedVariable`)
  - **Issue**: "SinglePlayerGameAgent" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/example.py:1:32`

- [ ] **Line 1** (`reportArgumentType`)
  - **Issue**: Expression of type "None" cannot be assigned to parameter of type "list[str]"
      "None" is not assignable to "list[str]"
  - **Location**: `haive-games/src/haive/games/single_player/example.py:1:77`

- [ ] **Line 89** (`reportUndefinedVariable`)
  - **Issue**: "SinglePlayerGameAgent" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/example.py:89:25`

### 📄 haive-games/src/haive/games/single_player/flow_free/agent.py

- [ ] **Line 24** (`reportArgumentType`)
  - **Issue**: Argument of type "type[FlowFreeAgent]" cannot be assigned to parameter "agent_class" of type "type[Agent[Unknown]]" in function "decorator"
      "type[FlowFreeAgent]" is not assignable to "type[Agent[Unknown]]"
      Type "type[FlowFreeAgent]" is not assignable to type "type[Agent[Unknown]]"
  - **Location**: `haive-games/src/haive/games/single_player/flow_free/agent.py:24:1`

- [ ] **Line 24** (`reportArgumentType`)
  - **Issue**: Argument of type "type[FlowFreeConfig]" cannot be assigned to parameter "config_class" of type "type[AgentConfig[Unknown, Unknown, Unknown]]" in function "register_agent"
      "type[FlowFreeConfig]" is not assignable to "type[AgentConfig[Unknown, Unknown, Unknown]]"
      Type "type[FlowFreeConfig]" is not assignable to type "type[AgentConfig[Unknown, Unknown, Unknown]]"
  - **Location**: `haive-games/src/haive/games/single_player/flow_free/agent.py:24:16`

- [ ] **Line 351** (`reportArgumentType`)
  - **Issue**: Argument of type "FlowFreeState" cannot be assigned to parameter "state" of type "dict[str, Any]" in function "visualize_state"
      "FlowFreeState" is not assignable to "dict[str, Any]"
  - **Location**: `haive-games/src/haive/games/single_player/flow_free/agent.py:351:33`

- [ ] **Line 372** (`reportArgumentType`)
  - **Issue**: Argument of type "FlowFreeState" cannot be assigned to parameter "state" of type "dict[str, Any]" in function "visualize_state"
      "FlowFreeState" is not assignable to "dict[str, Any]"
  - **Location**: `haive-games/src/haive/games/single_player/flow_free/agent.py:372:41`

### 📄 haive-games/src/haive/games/single_player/flow_free/base.py

- [ ] **Line 7** (`reportMissingImports`)
  - **Issue**: Import "game_framework_base" could not be resolved
  - **Location**: `haive-games/src/haive/games/single_player/flow_free/base.py:7:5`

- [ ] **Line 166** (`reportInvalidTypeArguments`)
  - **Issue**: Expected no type arguments for class "FlowGridSpace"
  - **Location**: `haive-games/src/haive/games/single_player/flow_free/base.py:166:40`

- [ ] **Line 169** (`reportGeneralTypeIssues`)
  - **Issue**: Expected class but received "(iterable: Iterable[object], /) -> bool"
  - **Location**: `haive-games/src/haive/games/single_player/flow_free/base.py:169:31`

- [ ] **Line 177** (`reportInvalidTypeArguments`)
  - **Issue**: Expected no type arguments for class "FlowGridSpace"
  - **Location**: `haive-games/src/haive/games/single_player/flow_free/base.py:177:38`

### 📄 haive-games/src/haive/games/single_player/flow_free/engines.py

- [ ] **Line 113** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/single_player/flow_free/engines.py:113:50`

- [ ] **Line 119** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/single_player/flow_free/engines.py:119:50`

### 📄 haive-games/src/haive/games/single_player/flow_free/example.py

- [ ] **Line 52** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "state_manager" for class "Agent[Unknown]"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/flow_free/example.py:52:14`

- [ ] **Line 57** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_game" for class "Agent[Unknown]"
      Attribute "run_game" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/flow_free/example.py:57:14`

### 📄 haive-games/src/haive/games/single_player/logic_grid/base.py

- [ ] **Line 6** (`reportMissingImports`)
  - **Issue**: Import "game_framework_base" could not be resolved
  - **Location**: `haive-games/src/haive/games/single_player/logic_grid/base.py:6:5`

- [ ] **Line 208** (`reportInvalidTypeArguments`)
  - **Issue**: Expected no type arguments for class "LogicGridSpace"
  - **Location**: `haive-games/src/haive/games/single_player/logic_grid/base.py:208:37`

- [ ] **Line 214** (`reportInvalidTypeArguments`)
  - **Issue**: Expected no type arguments for class "LogicGridSpace"
  - **Location**: `haive-games/src/haive/games/single_player/logic_grid/base.py:214:55`

- [ ] **Line 220** (`reportInvalidTypeArguments`)
  - **Issue**: Expected no type arguments for class "LogicGridSpace"
  - **Location**: `haive-games/src/haive/games/single_player/logic_grid/base.py:220:24`

- [ ] **Line 244** (`reportInvalidTypeArguments`)
  - **Issue**: Expected no type arguments for class "LogicGridSpace"
  - **Location**: `haive-games/src/haive/games/single_player/logic_grid/base.py:244:51`

- [ ] **Line 457** (`reportGeneralTypeIssues`)
  - **Issue**: Expected class but received "(iterable: Iterable[object], /) -> bool"
  - **Location**: `haive-games/src/haive/games/single_player/logic_grid/base.py:457:26`

### 📄 haive-games/src/haive/games/single_player/mine_sweeper/base.py

- [ ] **Line 10** (`reportMissingImports`)
  - **Issue**: Import "game_framework_base" could not be resolved
  - **Location**: `haive-games/src/haive/games/single_player/mine_sweeper/base.py:10:5`

- [ ] **Line 32** (`reportUndefinedVariable`)
  - **Issue**: "Board" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/mine_sweeper/base.py:32:57`

### 📄 haive-games/src/haive/games/single_player/rubiks/agent.py

- [ ] **Line 10** (`reportMissingImports`)
  - **Issue**: Import "haive.games.single_player.rubiks.config" could not be resolved
  - **Location**: `haive-games/src/haive/games/single_player/rubiks/agent.py:10:5`

- [ ] **Line 11** (`reportMissingImports`)
  - **Issue**: Import "haive.games.single_player.rubiks.cube_ops" could not be resolved
  - **Location**: `haive-games/src/haive/games/single_player/rubiks/agent.py:11:5`

- [ ] **Line 12** (`reportMissingImports`)
  - **Issue**: Import "haive.games.single_player.rubiks.engines" could not be resolved
  - **Location**: `haive-games/src/haive/games/single_player/rubiks/agent.py:12:5`

- [ ] **Line 13** (`reportAttributeAccessIssue`)
  - **Issue**: "RubiksCubeState" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/single_player/rubiks/agent.py:13:51`

- [ ] **Line 39** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/rubiks/agent.py:39:19`

- [ ] **Line 40** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/rubiks/agent.py:40:19`

- [ ] **Line 41** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/rubiks/agent.py:41:19`

- [ ] **Line 42** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/rubiks/agent.py:42:19`

- [ ] **Line 43** (`reportOptionalMemberAccess`)
  - **Issue**: "add_node" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/rubiks/agent.py:43:19`

- [ ] **Line 46** (`reportOptionalMemberAccess`)
  - **Issue**: "set_entry_point" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/rubiks/agent.py:46:19`

- [ ] **Line 49** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/rubiks/agent.py:49:19`

- [ ] **Line 52** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/rubiks/agent.py:52:19`

- [ ] **Line 64** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/rubiks/agent.py:64:19`

- [ ] **Line 67** (`reportOptionalMemberAccess`)
  - **Issue**: "add_conditional_edges" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/rubiks/agent.py:67:19`

- [ ] **Line 73** (`reportOptionalMemberAccess`)
  - **Issue**: "add_edge" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/rubiks/agent.py:73:19`

### 📄 haive-games/src/haive/games/single_player/state_manager.py

- [ ] **Line 5** (`reportAttributeAccessIssue`)
  - **Issue**: "WordConnectionsState" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/single_player/state_manager.py:5:35`

- [ ] **Line 28** (`reportUndefinedVariable`)
  - **Issue**: "GameDifficulty" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/state_manager.py:28:20`

- [ ] **Line 28** (`reportUndefinedVariable`)
  - **Issue**: "GameDifficulty" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/state_manager.py:28:37`

- [ ] **Line 29** (`reportUndefinedVariable`)
  - **Issue**: "PlayerType" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/state_manager.py:29:21`

- [ ] **Line 29** (`reportUndefinedVariable`)
  - **Issue**: "PlayerType" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/state_manager.py:29:34`

- [ ] **Line 31** (`reportInvalidTypeForm`)
  - **Issue**: Variable not allowed in type expression
  - **Location**: `haive-games/src/haive/games/single_player/state_manager.py:31:9`

- [ ] **Line 46** (`reportInvalidTypeForm`)
  - **Issue**: Variable not allowed in type expression
  - **Location**: `haive-games/src/haive/games/single_player/state_manager.py:46:31`

- [ ] **Line 46** (`reportInvalidTypeForm`)
  - **Issue**: Variable not allowed in type expression
  - **Location**: `haive-games/src/haive/games/single_player/state_manager.py:46:48`

- [ ] **Line 60** (`reportInvalidTypeForm`)
  - **Issue**: Variable not allowed in type expression
  - **Location**: `haive-games/src/haive/games/single_player/state_manager.py:60:34`

- [ ] **Line 60** (`reportInvalidTypeForm`)
  - **Issue**: Variable not allowed in type expression
  - **Location**: `haive-games/src/haive/games/single_player/state_manager.py:60:46`

- [ ] **Line 82** (`reportInvalidTypeForm`)
  - **Issue**: Variable not allowed in type expression
  - **Location**: `haive-games/src/haive/games/single_player/state_manager.py:82:38`

- [ ] **Line 82** (`reportInvalidTypeForm`)
  - **Issue**: Variable not allowed in type expression
  - **Location**: `haive-games/src/haive/games/single_player/state_manager.py:82:44`

- [ ] **Line 95** (`reportInvalidTypeForm`)
  - **Issue**: Variable not allowed in type expression
  - **Location**: `haive-games/src/haive/games/single_player/state_manager.py:95:36`

- [ ] **Line 108** (`reportInvalidTypeForm`)
  - **Issue**: Variable not allowed in type expression
  - **Location**: `haive-games/src/haive/games/single_player/state_manager.py:108:38`

- [ ] **Line 108** (`reportInvalidTypeForm`)
  - **Issue**: Variable not allowed in type expression
  - **Location**: `haive-games/src/haive/games/single_player/state_manager.py:108:61`

### 📄 haive-games/src/haive/games/single_player/sudoku/game/board.py

- [ ] **Line 5** (`reportMissingImports`)
  - **Issue**: Import "haive.games.core.board.base" could not be resolved
  - **Location**: `haive-games/src/haive/games/single_player/sudoku/game/board.py:5:5`

### 📄 haive-games/src/haive/games/single_player/sudoku/game/cell.py

- [ ] **Line 3** (`reportAttributeAccessIssue`)
  - **Issue**: "GridSpace" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/single_player/sudoku/game/cell.py:3:43`

- [ ] **Line 27** (`reportCallIssue`)
  - **Issue**: Object of type "bool" is not callable
      Attribute "**call**" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/sudoku/game/cell.py:27:11`

- [ ] **Line 40** (`reportCallIssue`)
  - **Issue**: Object of type "bool" is not callable
      Attribute "**call**" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/sudoku/game/cell.py:40:11`

- [ ] **Line 52** (`reportCallIssue`)
  - **Issue**: Object of type "bool" is not callable
      Attribute "**call**" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/sudoku/game/cell.py:52:11`

### 📄 haive-games/src/haive/games/single_player/sudoku/game/piece.py

- [ ] **Line 7** (`reportMissingImports`)
  - **Issue**: Import "haive.games.core.piece.base" could not be resolved
  - **Location**: `haive-games/src/haive/games/single_player/sudoku/game/piece.py:7:5`

- [ ] **Line 26** (`reportUndefinedVariable`)
  - **Issue**: "Board" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/sudoku/game/piece.py:26:58`

### 📄 haive-games/src/haive/games/single_player/towers_of_hanoi/base.py

- [ ] **Line 12** (`reportAssignmentType`)
  - **Issue**: Type "type[Game[S@Game, M@Game]]" is not assignable to declared type "type[Game[Unknown, Unknown]]"
      "type[Game[S@Game, M@Game]]" is not assignable to "type[Game[Unknown, Unknown]]"
      Type "type[Game[S@Game, M@Game]]" is not assignable to type "type[Game[Unknown, Unknown]]"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:12:44`

- [ ] **Line 24** (`reportUndefinedVariable`)
  - **Issue**: "P" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:24:30`

- [ ] **Line 24** (`reportInvalidTypeForm`)
  - **Issue**: Type argument for "Generic" must be a type variable
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:24:30`

- [ ] **Line 24** (`reportInvalidTypeForm`)
  - **Issue**: Type argument for "Generic" must be a type variable
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:24:33`

- [ ] **Line 33** (`reportGeneralTypeIssues`)
  - **Issue**: Expected class but received "(iterable: Iterable[object], /) -> bool"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:33:26`

- [ ] **Line 39** (`reportGeneralTypeIssues`)
  - **Issue**: Expected class but received "(iterable: Iterable[object], /) -> bool"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:39:44`

- [ ] **Line 43** (`reportGeneralTypeIssues`)
  - **Issue**: Expected class but received "(iterable: Iterable[object], /) -> bool"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:43:40`

- [ ] **Line 209** (`reportInvalidTypeArguments`)
  - **Issue**: Expected no type arguments for class "PegSpace"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:209:32`

- [ ] **Line 223** (`reportInvalidTypeArguments`)
  - **Issue**: Expected no type arguments for class "PegSpace"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:223:71`

- [ ] **Line 234** (`reportInvalidTypeArguments`)
  - **Issue**: Expected no type arguments for class "PegSpace"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:234:62`

- [ ] **Line 272** (`reportInvalidTypeArguments`)
  - **Issue**: Expected no type arguments for class "PegSpace"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:272:33`

- [ ] **Line 279** (`reportArgumentType`)
  - **Issue**: Argument of type "PegPosition | None" cannot be assigned to parameter "position" of type "PegPosition" in function "place_piece"
      Type "PegPosition | None" is not assignable to type "PegPosition"
        "None" is not assignable to "PegPosition"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:279:35`

- [ ] **Line 299** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "remove_piece" for class "HanoiBoard\*"
      Attribute "remove_piece" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:299:17`

- [ ] **Line 351** (`reportGeneralTypeIssues`)
  - **Issue**: Expected class but received "(iterable: Iterable[object], /) -> bool"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:351:44`

- [ ] **Line 371** (`reportGeneralTypeIssues`)
  - **Issue**: Expected class but received "(iterable: Iterable[object], /) -> bool"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/base.py:371:40`

### 📄 haive-games/src/haive/games/single_player/towers_of_hanoi/position.py

- [ ] **Line 9** (`reportUndefinedVariable`)
  - **Issue**: "PegNumber" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/position.py:9:9`

### 📄 haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py

- [ ] **Line 11** (`reportMissingImports`)
  - **Issue**: Import "haive.games.single_player.towers_of_hanoi.agent" could not be resolved
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:11:5`

- [ ] **Line 12** (`reportMissingImports`)
  - **Issue**: Import "haive.games.single_player.towers_of_hanoi.config" could not be resolved
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:12:5`

- [ ] **Line 13** (`reportMissingImports`)
  - **Issue**: Import "haive.games.single_player.towers_of_hanoi.game" could not be resolved
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:13:5`

- [ ] **Line 39** (`reportOptionalMemberAccess`)
  - **Issue**: "initialize" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:39:18`

- [ ] **Line 54** (`reportOptionalMemberAccess`)
  - **Issue**: "is_solved" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:54:32`

- [ ] **Line 81** (`reportOptionalMemberAccess`)
  - **Issue**: "is_solved" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:81:21`

- [ ] **Line 83** (`reportOptionalMemberAccess`)
  - **Issue**: "moves" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:83:56`

- [ ] **Line 84** (`reportOptionalMemberAccess`)
  - **Issue**: "optimal_moves" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:84:54`

- [ ] **Line 85** (`reportOptionalMemberAccess`)
  - **Issue**: "optimal_moves" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:85:36`

- [ ] **Line 85** (`reportOptionalMemberAccess`)
  - **Issue**: "moves" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:85:66`

- [ ] **Line 98** (`reportOptionalMemberAccess`)
  - **Issue**: "format_board_state" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:98:36`

- [ ] **Line 107** (`reportOptionalMemberAccess`)
  - **Issue**: "num_disks" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:107:51`

- [ ] **Line 108** (`reportOptionalMemberAccess`)
  - **Issue**: "num_pegs" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:108:50`

- [ ] **Line 109** (`reportOptionalMemberAccess`)
  - **Issue**: "moves" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:109:55`

- [ ] **Line 110** (`reportOptionalMemberAccess`)
  - **Issue**: "optimal_moves" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:110:53`

- [ ] **Line 112** (`reportOptionalMemberAccess`)
  - **Issue**: "moves" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:112:21`

- [ ] **Line 113** (`reportOptionalMemberAccess`)
  - **Issue**: "optimal_moves" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:113:36`

- [ ] **Line 113** (`reportOptionalMemberAccess`)
  - **Issue**: "moves" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:113:66`

- [ ] **Line 128** (`reportOptionalMemberAccess`)
  - **Issue**: "moves" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:128:25`

- [ ] **Line 132** (`reportOptionalMemberAccess`)
  - **Issue**: "moves" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:132:43`

- [ ] **Line 133** (`reportOptionalMemberAccess`)
  - **Issue**: "moves" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:133:37`

- [ ] **Line 147** (`reportOptionalMemberAccess`)
  - **Issue**: "invoke" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:147:28`

- [ ] **Line 159** (`reportOptionalMemberAccess`)
  - **Issue**: "get_valid_moves" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:159:32`

- [ ] **Line 174** (`reportOptionalMemberAccess`)
  - **Issue**: "make_move" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:174:18`

- [ ] **Line 181** (`reportOptionalMemberAccess`)
  - **Issue**: "is_solved" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:181:28`

- [ ] **Line 183** (`reportOptionalMemberAccess`)
  - **Issue**: "invoke" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/towers_of_hanoi/ui.py:183:23`

### 📄 haive-games/src/haive/games/single_player/twenty_fourty_eight/game.py

- [ ] **Line 7** (`reportMissingImports`)
  - **Issue**: Import "game_framework_base" could not be resolved
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game.py:7:5`

- [ ] **Line 41** (`reportUndefinedVariable`)
  - **Issue**: "Board" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game.py:41:57`

- [ ] **Line 108** (`reportUndefinedVariable`)
  - **Issue**: "TwentyFortyEightBoard" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game.py:108:11`

- [ ] **Line 126** (`reportUndefinedVariable`)
  - **Issue**: "TwentyFortyEightBoard" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game.py:126:16`

### 📄 haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py

- [ ] **Line 5** (`reportUndefinedVariable`)
  - **Issue**: "GridBoard" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py:5:4`

- [ ] **Line 5** (`reportUndefinedVariable`)
  - **Issue**: "TwentyFortyEightSquare" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py:5:14`

- [ ] **Line 5** (`reportUndefinedVariable`)
  - **Issue**: "GridPosition" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py:5:38`

- [ ] **Line 5** (`reportUndefinedVariable`)
  - **Issue**: "NumberTile" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py:5:52`

- [ ] **Line 17** (`reportUndefinedVariable`)
  - **Issue**: "GridPosition" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py:17:27`

- [ ] **Line 18** (`reportUndefinedVariable`)
  - **Issue**: "TwentyFortyEightSquare" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py:18:25`

- [ ] **Line 21** (`reportUndefinedVariable`)
  - **Issue**: "NumberTile" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py:21:35`

- [ ] **Line 39** (`reportUndefinedVariable`)
  - **Issue**: "NumberTile" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py:39:15`

- [ ] **Line 48** (`reportUndefinedVariable`)
  - **Issue**: "Direction" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py:48:36`

- [ ] **Line 57** (`reportUndefinedVariable`)
  - **Issue**: "NumberTile" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py:57:63`

- [ ] **Line 64** (`reportUndefinedVariable`)
  - **Issue**: "Direction" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py:64:24`

- [ ] **Line 70** (`reportUndefinedVariable`)
  - **Issue**: "Direction" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py:70:26`

- [ ] **Line 76** (`reportUndefinedVariable`)
  - **Issue**: "Direction" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py:76:26`

- [ ] **Line 82** (`reportUndefinedVariable`)
  - **Issue**: "Direction" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py:82:26`

- [ ] **Line 103** (`reportUndefinedVariable`)
  - **Issue**: "NumberTile" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py:103:32`

- [ ] **Line 125** (`reportUndefinedVariable`)
  - **Issue**: "NumberTile" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py:125:40`

- [ ] **Line 179** (`reportUndefinedVariable`)
  - **Issue**: "NumberTile" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py:179:40`

- [ ] **Line 194** (`reportUndefinedVariable`)
  - **Issue**: "NumberTile" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py:194:45`

- [ ] **Line 204** (`reportUndefinedVariable`)
  - **Issue**: "NumberTile" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py:204:63`

- [ ] **Line 213** (`reportUndefinedVariable`)
  - **Issue**: "NumberTile" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py:213:63`

- [ ] **Line 232** (`reportUndefinedVariable`)
  - **Issue**: "NumberTile" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/twenty_fourty_eight/game/board.py:232:49`

### 📄 haive-games/src/haive/games/single_player/wordle/agent.py

- [ ] **Line 25** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[bool, str]" cannot be assigned to parameter "routes" of type "dict[str, str]" in function "add_conditional_edges"
      "Literal[True]" is not assignable to "str"
      "Literal[False]" is not assignable to "str"
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:25:47`

- [ ] **Line 33** (`reportAbstractUsage`)
  - **Issue**: Cannot instantiate abstract class "WordConnectionsState"
      "GameState.initialize" is not implemented
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:33:21`

- [ ] **Line 57** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "game_engine" for class "GameConfig"
      Attribute "game_engine" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:57:31`

- [ ] **Line 128** (`reportArgumentType`)
  - **Issue**: Expression of type "None" cannot be assigned to parameter of type "dict[Unknown, Unknown]"
      "None" is not assignable to "dict[Unknown, Unknown]"
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:128:50`

- [ ] **Line 169** (`reportAbstractUsage`)
  - **Issue**: Cannot instantiate abstract class "WordConnectionsState"
      "GameState.initialize" is not implemented
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:169:15`

- [ ] **Line 183** (`reportUndefinedVariable`)
  - **Issue**: "console" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:183:8`

- [ ] **Line 193** (`reportUndefinedVariable`)
  - **Issue**: "console" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:193:8`

- [ ] **Line 194** (`reportUndefinedVariable`)
  - **Issue**: "console" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:194:8`

- [ ] **Line 235** (`reportUndefinedVariable`)
  - **Issue**: "console" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:235:8`

- [ ] **Line 237** (`reportUndefinedVariable`)
  - **Issue**: "console" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:237:8`

- [ ] **Line 240** (`reportUndefinedVariable`)
  - **Issue**: "console" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:240:8`

- [ ] **Line 245** (`reportUndefinedVariable`)
  - **Issue**: "ValidationNodeConfig" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:245:28`

- [ ] **Line 247** (`reportUndefinedVariable`)
  - **Issue**: "schemas" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:247:20`

- [ ] **Line 248** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "tools" for class "Engine[Unknown, Unknown]"
      Attribute "tools" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:248:30`

- [ ] **Line 248** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "tools" for class "str"
      Attribute "tools" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:248:30`

- [ ] **Line 254** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "has_tool_node" for class "WordConnectionsAgent\*"
      Attribute "has_tool_node" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:254:36`

- [ ] **Line 257** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "has_parser_node" for class "WordConnectionsAgent\*"
      Attribute "has_parser_node" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:257:39`

- [ ] **Line 261** (`reportUndefinedVariable`)
  - **Issue**: "console" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:261:8`

- [ ] **Line 264** (`reportUndefinedVariable`)
  - **Issue**: "console" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:264:8`

- [ ] **Line 264** (`reportUndefinedVariable`)
  - **Issue**: "schemas" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:264:40`

- [ ] **Line 265** (`reportUndefinedVariable`)
  - **Issue**: "console" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:265:8`

- [ ] **Line 266** (`reportUndefinedVariable`)
  - **Issue**: "console" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:266:8`

- [ ] **Line 267** (`reportUndefinedVariable`)
  - **Issue**: "console" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:267:8`

- [ ] **Line 268** (`reportUndefinedVariable`)
  - **Issue**: "console" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:268:8`

- [ ] **Line 269** (`reportUndefinedVariable`)
  - **Issue**: "console" is not defined
  - **Location**: `haive-games/src/haive/games/single_player/wordle/agent.py:269:8`

### 📄 haive-games/src/haive/games/single_player/wordle/config.py

- [ ] **Line 73** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-games/src/haive/games/single_player/wordle/config.py:73:54`

### 📄 haive-games/src/haive/games/single_player/wordle/example.py

- [ ] **Line 117** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "initialize_game" for class "Agent[Unknown]"
      Attribute "initialize_game" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/wordle/example.py:117:32`

- [ ] **Line 156** (`reportArgumentType`)
  - **Issue**: Argument of type "Unknown | WordConnectionsState | None" cannot be assigned to parameter "state" of type "WordConnectionsState" in function "display_grid"
      Type "Unknown | WordConnectionsState | None" is not assignable to type "WordConnectionsState"
        "None" is not assignable to "WordConnectionsState"
  - **Location**: `haive-games/src/haive/games/single_player/wordle/example.py:156:26`

- [ ] **Line 160** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "ainvoke" for class "StateGraph"
      Attribute "ainvoke" is unknown
  - **Location**: `haive-games/src/haive/games/single_player/wordle/example.py:160:40`

- [ ] **Line 160** (`reportOptionalMemberAccess`)
  - **Issue**: "ainvoke" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/wordle/example.py:160:40`

- [ ] **Line 161** (`reportOptionalMemberAccess`)
  - **Issue**: "model_dump" is not a known attribute of "None"
  - **Location**: `haive-games/src/haive/games/single_player/wordle/example.py:161:23`

- [ ] **Line 165** (`reportAbstractUsage`)
  - **Issue**: Cannot instantiate abstract class "WordConnectionsState"
      "GameState.initialize" is not implemented
  - **Location**: `haive-games/src/haive/games/single_player/wordle/example.py:165:22`

### 📄 haive-games/src/haive/games/single_player/wordle/state.py

- [ ] **Line 7** (`reportAttributeAccessIssue`)
  - **Issue**: "GameSource" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/single_player/wordle/state.py:7:4`

- [ ] **Line 8** (`reportAttributeAccessIssue`)
  - **Issue**: "WordCell" is unknown import symbol
  - **Location**: `haive-games/src/haive/games/single_player/wordle/state.py:8:4`

### 📄 haive-games/src/haive/games/single_player/wordle/state_manager.py

- [ ] **Line 145** (`reportAbstractUsage`)
  - **Issue**: Cannot instantiate abstract class "WordConnectionsState"
      "GameState.initialize" is not implemented
  - **Location**: `haive-games/src/haive/games/single_player/wordle/state_manager.py:145:15`

### 📄 haive-games/src/haive/games/tic_tac_toe/agent.py

- [ ] **Line 171** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "first_player" for class "GameConfig"
      Attribute "first_player" is unknown
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/agent.py:171:37`

- [ ] **Line 172** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player_X" for class "GameConfig"
      Attribute "player_X" is unknown
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/agent.py:172:33`

- [ ] **Line 173** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player_O" for class "GameConfig"
      Attribute "player_O" is unknown
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/agent.py:173:33`

- [ ] **Line 537** (`reportCallIssue`)
  - **Issue**: Argument expression after \*\* must be a mapping with a "str" key type
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/agent.py:537:42`

- [ ] **Line 648** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "first_player" for class "GameConfig"
      Attribute "first_player" is unknown
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/agent.py:648:37`

- [ ] **Line 649** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player_X" for class "GameConfig"
      Attribute "player_X" is unknown
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/agent.py:649:33`

- [ ] **Line 650** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "player_O" for class "GameConfig"
      Attribute "player_O" is unknown
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/agent.py:650:33`

### 📄 haive-games/src/haive/games/tic_tac_toe/engines.py

- [ ] **Line 97** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/engines.py:97:50`

- [ ] **Line 104** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/engines.py:104:50`

- [ ] **Line 111** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/engines.py:111:50`

- [ ] **Line 118** (`reportCallIssue`)
  - **Issue**: No parameter named "parameters"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/engines.py:118:50`

### 📄 haive-games/src/haive/games/tic_tac_toe/example.py

- [ ] **Line 90** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "config"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:90:16`

- [ ] **Line 94** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_game" for class "Agent[Unknown]"
      Attribute "run_game" is unknown
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:94:28`

- [ ] **Line 133** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['AI Player 1']" cannot be assigned to parameter "player_X" of type "Literal['player1', 'player2']" in function "**init**"
      Type "Literal['AI Player 1']" is not assignable to type "Literal['player1', 'player2']"
        "Literal['AI Player 1']" is not assignable to type "Literal['player1']"
        "Literal['AI Player 1']" is not assignable to type "Literal['player2']"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:133:21`

- [ ] **Line 134** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['AI Player 2']" cannot be assigned to parameter "player_O" of type "Literal['player1', 'player2']" in function "**init**"
      Type "Literal['AI Player 2']" is not assignable to type "Literal['player1', 'player2']"
        "Literal['AI Player 2']" is not assignable to type "Literal['player1']"
        "Literal['AI Player 2']" is not assignable to type "Literal['player2']"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:134:21`

- [ ] **Line 183** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['Strategic AI']" cannot be assigned to parameter "player_X" of type "Literal['player1', 'player2']" in function "**init**"
      Type "Literal['Strategic AI']" is not assignable to type "Literal['player1', 'player2']"
        "Literal['Strategic AI']" is not assignable to type "Literal['player1']"
        "Literal['Strategic AI']" is not assignable to type "Literal['player2']"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:183:21`

- [ ] **Line 184** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['Analytical AI']" cannot be assigned to parameter "player_O" of type "Literal['player1', 'player2']" in function "**init**"
      Type "Literal['Analytical AI']" is not assignable to type "Literal['player1', 'player2']"
        "Literal['Analytical AI']" is not assignable to type "Literal['player1']"
        "Literal['Analytical AI']" is not assignable to type "Literal['player2']"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:184:21`

- [ ] **Line 281** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_game" for class "Agent[Unknown]"
      Attribute "run_game" is unknown
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:281:27`

- [ ] **Line 294** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_game" for class "Agent[Unknown]"
      Attribute "run_game" is unknown
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:294:27`

- [ ] **Line 392** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_game" for class "Agent[Unknown]"
      Attribute "run_game" is unknown
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:392:32`

- [ ] **Line 494** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_game" for class "Agent[Unknown]"
      Attribute "run_game" is unknown
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:494:48`

- [ ] **Line 501** (`reportArgumentType`)
  - **Issue**: Argument of type "float" cannot be assigned to parameter "value" of type "int" in function "**setitem**"
      "float" is not assignable to "int"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:501:20`

- [ ] **Line 502** (`reportArgumentType`)
  - **Issue**: Argument of type "float | Literal[0]" cannot be assigned to parameter "value" of type "int" in function "**setitem**"
      Type "float | Literal[0]" is not assignable to type "int"
        "float" is not assignable to "int"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:502:20`

- [ ] **Line 570** (`reportOperatorIssue`)
  - **Issue**: Operator ">" not supported for types "str | Unknown" and "Literal[80]"
      Operator ">" not supported for types "str" and "Literal[80]"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:570:11`

- [ ] **Line 572** (`reportOperatorIssue`)
  - **Issue**: Operator "<" not supported for types "str | Unknown" and "float"
      Operator "<" not supported for types "str" and "float"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:572:11`

- [ ] **Line 574** (`reportOperatorIssue`)
  - **Issue**: Operator ">" not supported for types "str | Unknown" and "Literal[55]"
      Operator ">" not supported for types "str" and "Literal[55]"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:574:11`

- [ ] **Line 612** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "arun_game" for class "Agent[Unknown]"
      Attribute "arun_game" is unknown
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:612:37`

- [ ] **Line 651** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_game" for class "Agent[Unknown]"
      Attribute "run_game" is unknown
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:651:31`

- [ ] **Line 723** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['Aggressive AI']" cannot be assigned to parameter "player_X" of type "Literal['player1', 'player2']" in function "**init**"
      Type "Literal['Aggressive AI']" is not assignable to type "Literal['player1', 'player2']"
        "Literal['Aggressive AI']" is not assignable to type "Literal['player1']"
        "Literal['Aggressive AI']" is not assignable to type "Literal['player2']"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:723:21`

- [ ] **Line 724** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['Defensive AI']" cannot be assigned to parameter "player_O" of type "Literal['player1', 'player2']" in function "**init**"
      Type "Literal['Defensive AI']" is not assignable to type "Literal['player1', 'player2']"
        "Literal['Defensive AI']" is not assignable to type "Literal['player1']"
        "Literal['Defensive AI']" is not assignable to type "Literal['player2']"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:724:21`

- [ ] **Line 733** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['Teacher AI']" cannot be assigned to parameter "player_X" of type "Literal['player1', 'player2']" in function "**init**"
      Type "Literal['Teacher AI']" is not assignable to type "Literal['player1', 'player2']"
        "Literal['Teacher AI']" is not assignable to type "Literal['player1']"
        "Literal['Teacher AI']" is not assignable to type "Literal['player2']"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:733:21`

- [ ] **Line 734** (`reportArgumentType`)
  - **Issue**: Argument of type "Literal['Student AI']" cannot be assigned to parameter "player_O" of type "Literal['player1', 'player2']" in function "**init**"
      Type "Literal['Student AI']" is not assignable to type "Literal['player1', 'player2']"
        "Literal['Student AI']" is not assignable to type "Literal['player1']"
        "Literal['Student AI']" is not assignable to type "Literal['player2']"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:734:21`

- [ ] **Line 743** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_game" for class "Agent[Unknown]"
      Attribute "run_game" is unknown
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:743:45`

- [ ] **Line 751** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "run_game" for class "Agent[Unknown]"
      Attribute "run_game" is unknown
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:751:47`

- [ ] **Line 944** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "config"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/example.py:944:20`

### 📄 haive-games/src/haive/games/tic_tac_toe/state_manager.py

- [ ] **Line 39** (`reportArgumentType`)
  - **Issue**: Argument of type "list[list[None]]" cannot be assigned to parameter "board" of type "list[list[str | None]]" in function "**init**"
      "list[list[None]]" is not assignable to "list[list[str | None]]"
        Type parameter "\_T@list" is invariant, but "list[None]" is not the same as "list[str | None]"
        Consider switching from "list" to "Sequence" which is covariant
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/state_manager.py:39:18`

- [ ] **Line 132** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "game_status" for class "TicTacToeState"
      Type "str" is not assignable to type "Literal['ongoing', 'X_win', 'O_win', 'draw']"
        "str" is not assignable to type "Literal['ongoing']"
        "str" is not assignable to type "Literal['X_win']"
        "str" is not assignable to type "Literal['O_win']"
        "str" is not assignable to type "Literal['draw']"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/state_manager.py:132:36`

- [ ] **Line 143** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "game_status" for class "TicTacToeState"
      Type "str" is not assignable to type "Literal['ongoing', 'X_win', 'O_win', 'draw']"
        "str" is not assignable to type "Literal['ongoing']"
        "str" is not assignable to type "Literal['X_win']"
        "str" is not assignable to type "Literal['O_win']"
        "str" is not assignable to type "Literal['draw']"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/state_manager.py:143:36`

- [ ] **Line 153** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "game_status" for class "TicTacToeState"
      Type "str" is not assignable to type "Literal['ongoing', 'X_win', 'O_win', 'draw']"
        "str" is not assignable to type "Literal['ongoing']"
        "str" is not assignable to type "Literal['X_win']"
        "str" is not assignable to type "Literal['O_win']"
        "str" is not assignable to type "Literal['draw']"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/state_manager.py:153:32`

- [ ] **Line 162** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "game_status" for class "TicTacToeState"
      Type "str" is not assignable to type "Literal['ongoing', 'X_win', 'O_win', 'draw']"
        "str" is not assignable to type "Literal['ongoing']"
        "str" is not assignable to type "Literal['X_win']"
        "str" is not assignable to type "Literal['O_win']"
        "str" is not assignable to type "Literal['draw']"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/state_manager.py:162:32`

### 📄 haive-games/src/haive/games/tic_tac_toe/ui.py

- [ ] **Line 313** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "state_manager" for class "Agent[Unknown]"
      Attribute "state_manager" is unknown
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/ui.py:313:39`

- [ ] **Line 407** (`reportReturnType`)
  - **Issue**: Type "dict[str, Any] | TicTacToeState | None" is not assignable to return type "dict[str, Any]"
      Type "dict[str, Any] | TicTacToeState | None" is not assignable to type "dict[str, Any]"
        "TicTacToeState" is not assignable to "dict[str, Any]"
  - **Location**: `haive-games/src/haive/games/tic_tac_toe/ui.py:407:15`

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
poetry run python -c "from haive.games import *; print('✅ Imports OK')"

# Re-run pyright to verify fixes
poetry run pyright packages/haive-games/src/ --level error

# Run any existing tests
poetry run pytest packages/haive-games/tests/ -v
```

---

**Generated**: 2025-08-02  
**Source**: `project_docs/build-reports/pyright-issues/haive-games-*.json`
