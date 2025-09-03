# HAIVE-TOOLS - Pyright Issues Checklist

**Total Errors**: 110
**Total Warnings**: 0
**Priority**: 📋 Standard

## Summary by Issue Type

### Error Categories

- **reportMissingImports**: 46 issues
- **reportAttributeAccessIssue**: 27 issues
- **reportCallIssue**: 23 issues
- **reportArgumentType**: 10 issues
- **reportGeneralTypeIssues**: 1 issues
- **reportUndefinedVariable**: 1 issues
- **reportAssignmentType**: 1 issues
- **reportReturnType**: 1 issues

## 🚨 ERRORS (Must Fix)

### 📄 haive-tools/src/haive/tools/tools/bing_search_tool_INC.py

- [ ] **Line 11** (`reportMissingImports`)
  - **Issue**: Import "haive.config.config" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/bing_search_tool_INC.py:11:5`

### 📄 haive-tools/src/haive/tools/tools/brave_search.py

- [ ] **Line 24** (`reportCallIssue`)
  - **Issue**: Module is not callable
  - **Location**: `haive-tools/src/haive/tools/tools/brave_search.py:24:20`

### 📄 haive-tools/src/haive/tools/tools/dataforseo_tool.py

- [ ] **Line 23** (`reportMissingImports`)
  - **Issue**: Import "haive.config.config" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/dataforseo_tool.py:23:5`

### 📄 haive-tools/src/haive/tools/tools/hinge_tools.py

- [ ] **Line 22** (`reportMissingImports`)
  - **Issue**: Import "squeaky_hinge" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/hinge_tools.py:22:5`

### 📄 haive-tools/src/haive/tools/tools/ionic_tool.py

- [ ] **Line 19** (`reportMissingImports`)
  - **Issue**: Import "ionic_langchain.tool" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/ionic_tool.py:19:5`

### 📄 haive-tools/src/haive/tools/tools/reddit_search.py

- [ ] **Line 49** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "reddit_client", "reddit_client_id", "reddit_client_secret", "reddit_user_agent"
  - **Location**: `haive-tools/src/haive/tools/tools/reddit_search.py:49:13`

### 📄 haive-tools/src/haive/tools/tools/toolkits/**init**.py

- [ ] **Line 3** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.alpha_vantage" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:3:5`

- [ ] **Line 8** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.amadues_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:8:5`

- [ ] **Line 16** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.base" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:16:5`

- [ ] **Line 22** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.chuck_norris_jokes_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:22:5`

- [ ] **Line 29** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.citydsk_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:29:5`

- [ ] **Line 37** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.clickup_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:37:5`

- [ ] **Line 38** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.financialdatasets_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:38:5`

- [ ] **Line 43** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.fred_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:43:5`

- [ ] **Line 56** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.free_to_game_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:56:5`

- [ ] **Line 66** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.google_calendar" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:66:5`

- [ ] **Line 71** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.jira_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:71:5`

- [ ] **Line 78** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.lcbo_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:78:5`

- [ ] **Line 86** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.mongodb_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:86:5`

- [ ] **Line 87** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.nla_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:87:5`

- [ ] **Line 94** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.openlibrary_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:94:5`

- [ ] **Line 102** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.poetry_db_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:102:5`

- [ ] **Line 113** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.polygon_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:113:5`

- [ ] **Line 114** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.request_tools" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:114:5`

- [ ] **Line 115** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.rick_and_morty_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:115:5`

- [ ] **Line 127** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.rps_101_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:127:5`

- [ ] **Line 133** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.slack_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:133:5`

- [ ] **Line 134** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.stack_exchange_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:134:5`

- [ ] **Line 135** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.stripe_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:135:5`

- [ ] **Line 136** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.trip_advisor_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:136:5`

- [ ] **Line 149** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.twilio_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:149:5`

- [ ] **Line 150** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.useless_facts_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:150:5`

- [ ] **Line 155** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.vbible_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:155:5`

- [ ] **Line 172** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.weather" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:172:5`

- [ ] **Line 180** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.yugiioh_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/__init__.py:180:5`

### 📄 haive-tools/src/haive/tools/tools/toolkits/clickup_toolkit.py

- [ ] **Line 31** (`reportMissingImports`)
  - **Issue**: Import "haive.config.config" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/clickup_toolkit.py:31:5`

- [ ] **Line 49** (`reportCallIssue`)
  - **Issue**: No parameter named "api_key"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/clickup_toolkit.py:49:8`

- [ ] **Line 50** (`reportCallIssue`)
  - **Issue**: No parameter named "redirect_uri"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/clickup_toolkit.py:50:8`

- [ ] **Line 51** (`reportCallIssue`)
  - **Issue**: No parameter named "client_id"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/clickup_toolkit.py:51:8`

- [ ] **Line 52** (`reportCallIssue`)
  - **Issue**: No parameter named "client_secret"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/clickup_toolkit.py:52:8`

- [ ] **Line 55** (`reportCallIssue`)
  - **Issue**: No parameter named "api_wrapper"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/clickup_toolkit.py:55:26`

### 📄 haive-tools/src/haive/tools/tools/toolkits/dev/**init**.py

- [ ] **Line 3** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.dev.tools" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/__init__.py:3:5`

### 📄 haive-tools/src/haive/tools/tools/toolkits/dev/project_creation/**init**.py

- [ ] **Line 3** (`reportMissingImports`)
  - **Issue**: Import "project_creation.github" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/project_creation/__init__.py:3:5`

### 📄 haive-tools/src/haive/tools/tools/toolkits/dev/project_creation/github.py

- [ ] **Line 200** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "required_approvals", "dismiss_stale_reviews", "require_code_owner_reviews", "enforce_admins"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/project_creation/github.py:200:20`

### 📄 haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/import_consolidator.py

- [ ] **Line 41** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "value" for class "AsName"
      Attribute "value" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/import_consolidator.py:41:53`

- [ ] **Line 59** (`reportArgumentType`)
  - **Issue**: Argument of type "Unknown | Name" cannot be assigned to parameter "asname" of type "AsName | None" in function "**init**"
      Type "Unknown | Name" is not assignable to type "AsName | None"
        Type "Name" is not assignable to type "AsName | None"
          "Name" is not assignable to "AsName"
          "Name" is not assignable to "None"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/transformers/import_consolidator.py:59:31`

### 📄 haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/code_smell_detector.py

- [ ] **Line 51** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "lineno" for class "For"
      Attribute "lineno" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/code_smell_detector.py:51:25`

### 📄 haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/import_analyzer.py

- [ ] **Line 58** (`reportArgumentType`)
  - **Issue**: Argument of type "BaseExpression | str" cannot be assigned to parameter "key" of type "str" in function "**getitem**"
      Type "BaseExpression | str" is not assignable to type "str"
        "BaseExpression" is not assignable to "str"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/import_analyzer.py:58:16`

- [ ] **Line 58** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "value" for class "AsName"
      Attribute "value" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/import_analyzer.py:58:68`

- [ ] **Line 59** (`reportArgumentType`)
  - **Issue**: Argument of type "BaseExpression | str" cannot be assigned to parameter "element" of type "str" in function "add"
      Type "BaseExpression | str" is not assignable to type "str"
        "BaseExpression" is not assignable to "str"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/import_analyzer.py:59:29`

- [ ] **Line 60** (`reportArgumentType`)
  - **Issue**: Argument of type "BaseExpression | str" cannot be assigned to parameter "element" of type "str" in function "add"
      Type "BaseExpression | str" is not assignable to type "str"
        "BaseExpression" is not assignable to "str"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/import_analyzer.py:60:36`

- [ ] **Line 74** (`reportGeneralTypeIssues`)
  - **Issue**: "ImportStar" is not iterable
      "**iter**" method not defined
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/import_analyzer.py:74:25`

- [ ] **Line 76** (`reportArgumentType`)
  - **Issue**: Argument of type "BaseExpression | str" cannot be assigned to parameter "element" of type "str" in function "add"
      Type "BaseExpression | str" is not assignable to type "str"
        "BaseExpression" is not assignable to "str"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/import_analyzer.py:76:33`

- [ ] **Line 77** (`reportArgumentType`)
  - **Issue**: Argument of type "BaseExpression | str" cannot be assigned to parameter "element" of type "str" in function "add"
      Type "BaseExpression | str" is not assignable to type "str"
        "BaseExpression" is not assignable to "str"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/import_analyzer.py:77:57`

### 📄 haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/type_checking.py

- [ ] **Line 62** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "value" for class "BaseExpression"
      Attribute "value" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/python/cst_toolkit/visitors/type_checking.py:62:55`

### 📄 haive-tools/src/haive/tools/tools/toolkits/dev/shell/background_process_manager.py

- [ ] **Line 208** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "port" for class "tuple[()]"
      Attribute "port" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/shell/background_process_manager.py:208:51`

- [ ] **Line 211** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "ip" for class "tuple[()]"
      Attribute "ip" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/shell/background_process_manager.py:211:54`

### 📄 haive-tools/src/haive/tools/tools/toolkits/dev/shell/logger.py

- [ ] **Line 49** (`reportUndefinedVariable`)
  - **Issue**: "SecureShellExecutor" is not defined
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/shell/logger.py:49:11`

### 📄 haive-tools/src/haive/tools/tools/toolkits/dev/shell/permission.py

- [ ] **Line 234** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "model" for class "ValidationError"
      Attribute "model" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/shell/permission.py:234:81`

### 📄 haive-tools/src/haive/tools/tools/toolkits/dev/shell/shell.py

- [ ] **Line 29** (`reportMissingImports`)
  - **Issue**: Import "haive.tools.toolkits.dev.permission" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/shell/shell.py:29:5`

### 📄 haive-tools/src/haive/tools/tools/toolkits/dev/tools.py

- [ ] **Line 605** (`reportAssignmentType`)
  - **Issue**: Type "None" is not assignable to declared type "list[dict[str, Any]]"
      "None" is not assignable to "list[dict[str, Any]]"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:605:36`

- [ ] **Line 693** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "lineno" for class "Name"
      Attribute "lineno" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:693:39`

- [ ] **Line 745** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "lineno" for class "Name"
      Attribute "lineno" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:745:39`

- [ ] **Line 810** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "body" for class "BaseSmallStatement"
      Attribute "body" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:810:38`

- [ ] **Line 810** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "body" for class "BaseStatement"
      Attribute "body" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:810:38`

- [ ] **Line 819** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "lineno" for class "Name"
      Attribute "lineno" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:819:43`

- [ ] **Line 842** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "lineno" for class "Name"
      Attribute "lineno" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:842:43`

- [ ] **Line 885** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "body" for class "BaseSmallStatement"
      Attribute "body" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:885:38`

- [ ] **Line 885** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "body" for class "BaseStatement"
      Attribute "body" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:885:38`

- [ ] **Line 894** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "lineno" for class "Name"
      Attribute "lineno" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:894:43`

- [ ] **Line 917** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "lineno" for class "Name"
      Attribute "lineno" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:917:43`

- [ ] **Line 996** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "lineno" for class "Param"
      Attribute "lineno" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:996:31`

- [ ] **Line 1015** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "lineno" for class "Name"
      Attribute "lineno" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1015:39`

- [ ] **Line 1122** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "lineno" for class "Name"
      Attribute "lineno" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1122:43`

- [ ] **Line 1137** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "lineno" for class "Name"
      Attribute "lineno" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1137:43`

- [ ] **Line 1215** (`reportArgumentType`)
  - **Issue**: Argument of type "Name" cannot be assigned to parameter "name" of type "AsName | None" in function "**init**"
      Type "Name" is not assignable to type "AsName | None"
        "Name" is not assignable to "AsName"
        "Name" is not assignable to "None"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1215:17`

- [ ] **Line 1221** (`reportArgumentType`)
  - **Issue**: Argument of type "Sequence[BaseStatement] | Sequence[BaseSmallStatement]" cannot be assigned to parameter "body" of type "Sequence[BaseStatement]" in function "**init**"
      Type "Sequence[BaseStatement] | Sequence[BaseSmallStatement]" is not assignable to type "Sequence[BaseStatement]"
        "Sequence[BaseSmallStatement]" is not assignable to "Sequence[BaseStatement]"
          Type parameter "\_T_co@Sequence" is covariant, but "BaseSmallStatement" is not a subtype of "BaseStatement"
            "BaseSmallStatement" is not assignable to "BaseStatement"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1221:40`

- [ ] **Line 1233** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "lineno" for class "Name"
      Attribute "lineno" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1233:35`

- [ ] **Line 1329** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "lineno" for class "Name"
      Attribute "lineno" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1329:35`

- [ ] **Line 1400** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "line_length", "use_black", "use_isort", "use_autoflake", "fix", "show_diff"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1400:44`

- [ ] **Line 1461** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "diff", "backup_path"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1461:19`

- [ ] **Line 1490** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "diff", "backup_path"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1490:19`

- [ ] **Line 1508** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "error", "backup_path"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/dev/tools.py:1508:15`

### 📄 haive-tools/src/haive/tools/tools/toolkits/financialdatasets_toolkit.py

- [ ] **Line 108** (`reportReturnType`)
  - **Issue**: Type "List[BaseTool]" is not assignable to return type "list[Tool]"
      "List[BaseTool]" is not assignable to "list[Tool]"
        Type parameter "\_T@list" is invariant, but "BaseTool" is not the same as "Tool"
        Consider switching from "list" to "Sequence" which is covariant
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/financialdatasets_toolkit.py:108:11`

### 📄 haive-tools/src/haive/tools/tools/toolkits/github_toolkit.py

- [ ] **Line 23** (`reportMissingImports`)
  - **Issue**: Import "haive.config.config" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/github_toolkit.py:23:5`

- [ ] **Line 35** (`reportCallIssue`)
  - **Issue**: No parameter named "app_id"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/github_toolkit.py:35:4`

- [ ] **Line 35** (`reportCallIssue`)
  - **Issue**: No parameter named "private_key"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/github_toolkit.py:35:33`

### 📄 haive-tools/src/haive/tools/tools/toolkits/jira_toolkit.py

- [ ] **Line 116** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "projects" for class "JiraAPIWrapper"
      Attribute "projects" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/jira_toolkit.py:116:29`

- [ ] **Line 146** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "create_issue" for class "JiraAPIWrapper"
      Attribute "create_issue" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/jira_toolkit.py:146:29`

- [ ] **Line 158** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "jql_query" for class "JiraAPIWrapper"
      Attribute "jql_query" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/jira_toolkit.py:158:29`

### 📄 haive-tools/src/haive/tools/tools/toolkits/mongodb_toolkit.py

- [ ] **Line 26** (`reportMissingImports`)
  - **Issue**: Import "langchain_mongodb.agent_toolkit.database" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/mongodb_toolkit.py:26:5`

- [ ] **Line 27** (`reportMissingImports`)
  - **Issue**: Import "langchain_mongodb.agent_toolkit.toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/mongodb_toolkit.py:27:5`

### 📄 haive-tools/src/haive/tools/tools/toolkits/office_365.py

- [ ] **Line 21** (`reportMissingImports`)
  - **Issue**: Import "haive.config.config" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/office_365.py:21:5`

- [ ] **Line 36** (`reportCallIssue`)
  - **Issue**: No parameter named "client_id"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/office_365.py:36:4`

- [ ] **Line 37** (`reportCallIssue`)
  - **Issue**: No parameter named "client_secret"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/office_365.py:37:4`

- [ ] **Line 38** (`reportCallIssue`)
  - **Issue**: No parameter named "tenant_id"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/office_365.py:38:4`

- [ ] **Line 39** (`reportCallIssue`)
  - **Issue**: No parameter named "scopes"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/office_365.py:39:4`

### 📄 haive-tools/src/haive/tools/tools/toolkits/powerbi_toolkit.py

- [ ] **Line 13** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "powerbi", "llm"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/powerbi_toolkit.py:13:14`

- [ ] **Line 14** (`reportCallIssue`)
  - **Issue**: No parameter named "dataset_id"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/powerbi_toolkit.py:14:4`

- [ ] **Line 15** (`reportCallIssue`)
  - **Issue**: No parameter named "credential"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/powerbi_toolkit.py:15:4`

### 📄 haive-tools/src/haive/tools/tools/toolkits/request_tools.py

- [ ] **Line 65** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "requests_wrapper"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/request_tools.py:65:9`

- [ ] **Line 72** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "requests_wrapper"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/request_tools.py:72:9`

### 📄 haive-tools/src/haive/tools/tools/toolkits/slack_toolkit.py

- [ ] **Line 32** (`reportMissingImports`)
  - **Issue**: Import "haive.config.config" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/slack_toolkit.py:32:5`

### 📄 haive-tools/src/haive/tools/tools/toolkits/stripe_toolkit.py

- [ ] **Line 88** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, Any]" cannot be assigned to parameter "configuration" of type "Configuration | None" in function "**init**"
      Type "dict[str, Any]" is not assignable to type "Configuration | None"
        "dict[str, Any]" is not assignable to "Configuration"
        "dict[str, Any]" is not assignable to "None"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/stripe_toolkit.py:88:67`

### 📄 haive-tools/src/haive/tools/tools/toolkits/twilio_toolkit.py

- [ ] **Line 27** (`reportMissingImports`)
  - **Issue**: Import "haive.config.config" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/twilio_toolkit.py:27:5`

### 📄 haive-tools/src/haive/tools/tools/toolkits/vbible_toolkit.py

- [ ] **Line 23** (`reportMissingImports`)
  - **Issue**: Import "haive.haive.toolkits.vbible_toolkit" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/vbible_toolkit.py:23:5`

### 📄 haive-tools/src/haive/tools/tools/toolkits/weather.py

- [ ] **Line 38** (`reportMissingImports`)
  - **Issue**: Import "haive.config.config" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/weather.py:38:5`

### 📄 haive-tools/src/haive/tools/tools/toolkits/yugiioh_toolkit.py

- [ ] **Line 88** (`reportArgumentType`)
  - **Issue**: Argument of type "type[GetCardInfoInput]" cannot be assigned to parameter "args_schema" of type "ArgsSchema | None" in function "from_function"
      Type "type[GetCardInfoInput]" is not assignable to type "ArgsSchema | None"
        "type[GetCardInfoInput]" is not assignable to "type[BaseModel]"
        Type "type[GetCardInfoInput]" is not assignable to type "type[BaseModel]"
        Type "type[GetCardInfoInput]" is not assignable to type "dict[str, Any]"
        Type is not assignable to "None"
  - **Location**: `haive-tools/src/haive/tools/tools/toolkits/yugiioh_toolkit.py:88:16`

### 📄 haive-tools/src/haive/tools/tools/translate_tools.py

- [ ] **Line 186** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "text" for class "List[TextResult]"
      Attribute "text" is unknown
  - **Location**: `haive-tools/src/haive/tools/tools/translate_tools.py:186:26`

### 📄 haive-tools/src/haive/tools/tools/wolfram_alpha_tool.py

- [ ] **Line 39** (`reportMissingImports`)
  - **Issue**: Import "haive.config.config" could not be resolved
  - **Location**: `haive-tools/src/haive/tools/tools/wolfram_alpha_tool.py:39:5`

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
poetry run python -c "from haive.tools import *; print('✅ Imports OK')"

# Re-run pyright to verify fixes
poetry run pyright packages/haive-tools/src/ --level error

# Run any existing tests
poetry run pytest packages/haive-tools/tests/ -v
```

---

**Generated**: 2025-08-02
**Source**: `project_docs/build-reports/pyright-issues/haive-tools-*.json`
