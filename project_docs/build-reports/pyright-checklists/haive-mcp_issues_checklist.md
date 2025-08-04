# HAIVE-MCP - Pyright Issues Checklist

**Total Errors**: 239
**Total Warnings**: 0
**Priority**: 📋 Standard

## Summary by Issue Type

### Error Categories

- **reportAttributeAccessIssue**: 72 issues
- **reportCallIssue**: 51 issues
- **reportOptionalMemberAccess**: 33 issues
- **reportMissingImports**: 28 issues
- **reportArgumentType**: 22 issues
- **reportReturnType**: 6 issues
- **reportUndefinedVariable**: 5 issues
- **reportGeneralTypeIssues**: 4 issues
- **reportRedeclaration**: 4 issues
- **reportPrivateImportUsage**: 3 issues
- **reportAssignmentType**: 3 issues
- **reportIndexIssue**: 2 issues
- **reportInvalidTypeForm**: 2 issues
- **reportOptionalCall**: 2 issues
- **reportOptionalIterable**: 2 issues

## 🚨 ERRORS (Must Fix)

### 📄 haive-mcp/src/haive/mcp/agents/**init**.py

- [ ] **Line 5** (`reportAttributeAccessIssue`)
  - **Issue**: "create_for_mcp_research" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/agents/__init__.py:5:4`

- [ ] **Line 6** (`reportAttributeAccessIssue`)
  - **Issue**: "create_for_mcp_setup" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/agents/__init__.py:6:4`

- [ ] **Line 15** (`reportAttributeAccessIssue`)
  - **Issue**: "get_pending_approvals" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/agents/__init__.py:15:4`

- [ ] **Line 16** (`reportAttributeAccessIssue`)
  - **Issue**: "get_recommendation_history" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/agents/__init__.py:16:4`

- [ ] **Line 26** (`reportAttributeAccessIssue`)
  - **Issue**: "create_with_mcp_servers" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/agents/__init__.py:26:8`

- [ ] **Line 27** (`reportAttributeAccessIssue`)
  - **Issue**: "get_available_capabilities" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/agents/__init__.py:27:8`

- [ ] **Line 28** (`reportAttributeAccessIssue`)
  - **Issue**: "setup_agent" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/agents/__init__.py:28:8`

- [ ] **Line 29** (`reportAttributeAccessIssue`)
  - **Issue**: "tool_count" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/agents/__init__.py:29:8`

- [ ] **Line 44** (`reportAttributeAccessIssue`)
  - **Issue**: "create_collaborative_agents" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/agents/__init__.py:44:4`

- [ ] **Line 45** (`reportAttributeAccessIssue`)
  - **Issue**: "get_transfer_status" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/agents/__init__.py:45:4`

### 📄 haive-mcp/src/haive/mcp/agents/documentation_agent.py

- [ ] **Line 353** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "arun" for class "MCPDocumentationAgent*"
      Could not bind method "arun" because "Self@MCPDocumentationAgent" is not assignable to parameter "self"
        "MCPDocumentationAgent*" is incompatible with protocol "AgentProtocol"
          "config" is not present
          "\_disable_checkpointing" is not present
            "input_schema" is invariant because it is mutable
            "input_schema" is an incompatible type
              Type "type[BaseModel] | dict[str, Any] | None" is not assignable to type "type[BaseModel] | None"
            "output_schema" is invariant because it is mutable
  - **Location**: `haive-mcp/src/haive/mcp/agents/documentation_agent.py:353:47`

- [ ] **Line 598** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "api_key", "health_check_interval"
  - **Location**: `haive-mcp/src/haive/mcp/agents/documentation_agent.py:598:15`

- [ ] **Line 622** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "\_extract_setup_info" for class "MCPDocumentationLoader"
      Attribute "\_extract_setup_info" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/agents/documentation_agent.py:622:31`

- [ ] **Line 656** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "categories", "required_capabilities", "on_server_connected", "on_server_failed", "on_tool_discovered"
  - **Location**: `haive-mcp/src/haive/mcp/agents/documentation_agent.py:656:15`

### 📄 haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py

- [ ] **Line 279** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "url", "api_key", "category", "description", "health_check_interval"
  - **Location**: `haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:279:29`

- [ ] **Line 546** (`reportUndefinedVariable`)
  - **Issue**: "discover_mcp_servers" is not defined
  - **Location**: `haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:546:53`

- [ ] **Line 560** (`reportUndefinedVariable`)
  - **Issue**: "install_mcp_server" is not defined
  - **Location**: `haive-mcp/src/haive/mcp/agents/intelligent_mcp_agent.py:560:59`

### 📄 haive-mcp/src/haive/mcp/agents/mcp_agent.py

- [ ] **Line 247** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "categories", "required_capabilities", "on_server_connected", "on_server_failed", "on_tool_discovered"
  - **Location**: `haive-mcp/src/haive/mcp/agents/mcp_agent.py:247:21`

- [ ] **Line 250** (`reportCallIssue`)
  - **Issue**: No parameter named "engine"
  - **Location**: `haive-mcp/src/haive/mcp/agents/mcp_agent.py:250:12`

- [ ] **Line 250** (`reportCallIssue`)
  - **Issue**: No parameter named "name"
  - **Location**: `haive-mcp/src/haive/mcp/agents/mcp_agent.py:250:50`

- [ ] **Line 314** (`reportGeneralTypeIssues`)
  - **Issue**: Invalid exception class or object
      "None" does not derive from BaseException
  - **Location**: `haive-mcp/src/haive/mcp/agents/mcp_agent.py:314:14`

### 📄 haive-mcp/src/haive/mcp/agents/transferable_mcp_agent.py

- [ ] **Line 224** (`reportOptionalMemberAccess`)
  - **Issue**: "model_dump" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/agents/transferable_mcp_agent.py:224:48`

- [ ] **Line 627** (`reportCallIssue`)
  - **Issue**: No parameter named "engine"
  - **Location**: `haive-mcp/src/haive/mcp/agents/transferable_mcp_agent.py:627:16`

- [ ] **Line 629** (`reportCallIssue`)
  - **Issue**: No parameter named "name"
  - **Location**: `haive-mcp/src/haive/mcp/agents/transferable_mcp_agent.py:629:16`

- [ ] **Line 630** (`reportCallIssue`)
  - **Issue**: No parameter named "share_client"
  - **Location**: `haive-mcp/src/haive/mcp/agents/transferable_mcp_agent.py:630:16`

- [ ] **Line 631** (`reportCallIssue`)
  - **Issue**: No parameter named "client_pool_key"
  - **Location**: `haive-mcp/src/haive/mcp/agents/transferable_mcp_agent.py:631:16`

### 📄 haive-mcp/src/haive/mcp/cli.py

- [ ] **Line 85** (`reportArgumentType`)
  - **Issue**: Argument of type "list[dict[str, Any]] | None" cannot be assigned to parameter "servers" of type "list[dict[Unknown, Unknown]]" in function "print_servers"
      Type "list[dict[str, Any]] | None" is not assignable to type "list[dict[Unknown, Unknown]]"
        "None" is not assignable to "list[dict[Unknown, Unknown]]"
  - **Location**: `haive-mcp/src/haive/mcp/cli.py:85:18`

### 📄 haive-mcp/src/haive/mcp/cli/mcp_manager.py

- [ ] **Line 41** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "install_dir" for class "GeneralMCPDownloader"
      Attribute "install_dir" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/cli/mcp_manager.py:41:43`

- [ ] **Line 53** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "patterns" for class "GeneralMCPDownloader"
      Attribute "patterns" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/cli/mcp_manager.py:53:38`

- [ ] **Line 56** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "discover_servers_from_registry" for class "GeneralMCPDownloader"
      Attribute "discover_servers_from_registry" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/cli/mcp_manager.py:56:48`

- [ ] **Line 109** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "version"
  - **Location**: `haive-mcp/src/haive/mcp/cli/mcp_manager.py:109:21`

- [ ] **Line 123** (`reportReturnType`)
  - **Issue**: Type "DownloadResult" is not assignable to return type "dict[Unknown, Unknown]"
      "DownloadResult" is not assignable to "dict[Unknown, Unknown]"
  - **Location**: `haive-mcp/src/haive/mcp/cli/mcp_manager.py:123:15`

- [ ] **Line 162** (`reportArgumentType`)
  - **Issue**: Argument of type "DownloadResult" cannot be assigned to parameter "install_result" of type "dict[Unknown, Unknown]" in function "\_update_server_status"
      "DownloadResult" is not assignable to "dict[Unknown, Unknown]"
  - **Location**: `haive-mcp/src/haive/mcp/cli/mcp_manager.py:162:41`

- [ ] **Line 164** (`reportReturnType`)
  - **Issue**: Type "DownloadResult" is not assignable to return type "dict[Unknown, Unknown]"
      "DownloadResult" is not assignable to "dict[Unknown, Unknown]"
  - **Location**: `haive-mcp/src/haive/mcp/cli/mcp_manager.py:164:15`

### 📄 haive-mcp/src/haive/mcp/complete_mcp_example.py

- [ ] **Line 28** (`reportAttributeAccessIssue`)
  - **Issue**: "MCPDocumentationLoader" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/complete_mcp_example.py:28:36`

- [ ] **Line 260** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "servers" for class "MCPServer"
      Attribute "servers" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/complete_mcp_example.py:260:50`

- [ ] **Line 276** (`reportOptionalMemberAccess`)
  - **Issue**: "aget_relevant_documents" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/complete_mcp_example.py:276:36`

- [ ] **Line 390** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, dict[str, Unknown]]" cannot be assigned to parameter "connections" of type "dict[str, Connection] | None" in function "**init**"
      Type "dict[str, dict[str, Unknown]]" is not assignable to type "dict[str, Connection] | None"
        "dict[str, dict[str, Unknown]]" is not assignable to "dict[str, Connection]"
          Type parameter "\_VT@dict" is invariant, but "dict[str, Unknown]" is not the same as "Connection"
          Consider switching from "dict" to "Mapping" which is covariant in the value type
        "dict[str, dict[str, Unknown]]" is not assignable to "None"
  - **Location**: `haive-mcp/src/haive/mcp/complete_mcp_example.py:390:38`

- [ ] **Line 455** (`reportOptionalMemberAccess`)
  - **Issue**: "aget_relevant_documents" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/complete_mcp_example.py:455:40`

### 📄 haive-mcp/src/haive/mcp/complete_mcp_with_parent_retriever.py

- [ ] **Line 38** (`reportAttributeAccessIssue`)
  - **Issue**: "MCPDocumentationLoader" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/complete_mcp_with_parent_retriever.py:38:36`

- [ ] **Line 220** (`reportOptionalMemberAccess`)
  - **Issue**: "aget_relevant_documents" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/complete_mcp_with_parent_retriever.py:220:50`

- [ ] **Line 228** (`reportOptionalMemberAccess`)
  - **Issue**: "aget_relevant_documents" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/complete_mcp_with_parent_retriever.py:228:58`

- [ ] **Line 236** (`reportOptionalMemberAccess`)
  - **Issue**: "arun" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/complete_mcp_with_parent_retriever.py:236:42`

- [ ] **Line 236** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "arun" for class "BaseRAGAgent"
      Could not bind method "arun" because "BaseRAGAgent" is not assignable to parameter "self"
        "BaseRAGAgent" is incompatible with protocol "AgentProtocol"
          "config" is not present
          "\_disable_checkpointing" is not present
            "input_schema" is invariant because it is mutable
            "input_schema" is an incompatible type
              Type "type[BaseModel] | dict[str, Any] | None" is not assignable to type "type[BaseModel] | None"
            "output_schema" is invariant because it is mutable
  - **Location**: `haive-mcp/src/haive/mcp/complete_mcp_with_parent_retriever.py:236:42`

- [ ] **Line 248** (`reportOptionalMemberAccess`)
  - **Issue**: "aget_relevant_documents" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/complete_mcp_with_parent_retriever.py:248:47`

- [ ] **Line 354** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, dict[str, Unknown]]" cannot be assigned to parameter "connections" of type "dict[str, Connection] | None" in function "**init**"
      Type "dict[str, dict[str, Unknown]]" is not assignable to type "dict[str, Connection] | None"
        "dict[str, dict[str, Unknown]]" is not assignable to "dict[str, Connection]"
          Type parameter "\_VT@dict" is invariant, but "dict[str, Unknown]" is not the same as "Connection"
          Consider switching from "dict" to "Mapping" which is covariant in the value type
        "dict[str, dict[str, Unknown]]" is not assignable to "None"
  - **Location**: `haive-mcp/src/haive/mcp/complete_mcp_with_parent_retriever.py:354:38`

### 📄 haive-mcp/src/haive/mcp/comprehensive_mcp_web.py

- [ ] **Line 16** (`reportMissingImports`)
  - **Issue**: Import "plotly.express" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/comprehensive_mcp_web.py:16:7`

- [ ] **Line 17** (`reportMissingImports`)
  - **Issue**: Import "streamlit" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/comprehensive_mcp_web.py:17:7`

- [ ] **Line 18** (`reportMissingImports`)
  - **Issue**: Import "csv_viewer" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/comprehensive_mcp_web.py:18:5`

- [ ] **Line 19** (`reportMissingImports`)
  - **Issue**: Import "self_query_mcp_agent" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/comprehensive_mcp_web.py:19:5`

### 📄 haive-mcp/src/haive/mcp/csv_viewer.py

- [ ] **Line 15** (`reportMissingImports`)
  - **Issue**: Import "streamlit" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/csv_viewer.py:15:7`

### 📄 haive-mcp/src/haive/mcp/discovery/**init**.py

- [ ] **Line 3** (`reportMissingImports`)
  - **Issue**: Import "discovery.analyzer" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/discovery/__init__.py:3:5`

- [ ] **Line 11** (`reportMissingImports`)
  - **Issue**: Import "discovery.server_discovery" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/discovery/__init__.py:11:5`

### 📄 haive-mcp/src/haive/mcp/documentation/**init**.py

- [ ] **Line 3** (`reportMissingImports`)
  - **Issue**: Import "documentation.doc_loader" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/documentation/__init__.py:3:5`

### 📄 haive-mcp/src/haive/mcp/documentation/doc_loader.py

- [ ] **Line 52** (`reportAttributeAccessIssue`)
  - **Issue**: "GitHubLoader" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/documentation/doc_loader.py:52:4`

- [ ] **Line 53** (`reportAttributeAccessIssue`)
  - **Issue**: "WebScraper" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/documentation/doc_loader.py:53:4`

### 📄 haive-mcp/src/haive/mcp/downloader/**init**.py

- [ ] **Line 34** (`reportAttributeAccessIssue`)
  - **Issue**: "Config" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/downloader/__init__.py:34:4`

- [ ] **Line 38** (`reportAttributeAccessIssue`)
  - **Issue**: "get_all_prompts" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/downloader/__init__.py:38:4`

- [ ] **Line 39** (`reportAttributeAccessIssue`)
  - **Issue**: "get_all_resources" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/downloader/__init__.py:39:4`

- [ ] **Line 40** (`reportAttributeAccessIssue`)
  - **Issue**: "get_all_tools" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/downloader/__init__.py:40:4`

- [ ] **Line 41** (`reportAttributeAccessIssue`)
  - **Issue**: "get_capability_summary" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/downloader/__init__.py:41:4`

- [ ] **Line 42** (`reportAttributeAccessIssue`)
  - **Issue**: "get_tools_by_capability" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/downloader/__init__.py:42:4`

- [ ] **Line 43** (`reportAttributeAccessIssue`)
  - **Issue**: "get_tools_by_server" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/downloader/__init__.py:43:4`

- [ ] **Line 55** (`reportAttributeAccessIssue`)
  - **Issue**: "create_default_config" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/downloader/__init__.py:55:4`

- [ ] **Line 56** (`reportAttributeAccessIssue`)
  - **Issue**: "load_config" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/downloader/__init__.py:56:4`

### 📄 haive-mcp/src/haive/mcp/downloader/core.py

- [ ] **Line 223** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "health_check"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/core.py:223:12`

- [ ] **Line 231** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "health_check"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/core.py:231:12`

- [ ] **Line 239** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "health_check"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/core.py:239:12`

- [ ] **Line 248** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "health_check"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/core.py:248:12`

- [ ] **Line 256** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "health_check"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/core.py:256:12`

- [ ] **Line 268** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "version"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/core.py:268:12`

- [ ] **Line 275** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "version"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/core.py:275:12`

- [ ] **Line 282** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "version"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/core.py:282:12`

- [ ] **Line 722** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "last_check", "last_success", "install_result", "health_status", "error"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/core.py:722:40`

- [ ] **Line 850** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "version"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/core.py:850:21`

- [ ] **Line 869** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "config_file"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/core.py:869:15`

- [ ] **Line 908** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "last_check", "last_success", "install_result", "health_status", "error"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/core.py:908:51`

### 📄 haive-mcp/src/haive/mcp/downloader/discovery.py

- [ ] **Line 624** (`reportReturnType`)
  - **Issue**: Type "None" is not assignable to return type "str"
      "None" is not assignable to "str"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/discovery.py:624:19`

### 📄 haive-mcp/src/haive/mcp/downloader/github_mass_downloader.py

- [ ] **Line 146** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "version"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/github_mass_downloader.py:146:15`

- [ ] **Line 226** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get" for class "DownloadResult"
      Attribute "get" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/downloader/github_mass_downloader.py:226:49`

- [ ] **Line 227** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get" for class "DownloadResult"
      Attribute "get" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/downloader/github_mass_downloader.py:227:45`

### 📄 haive-mcp/src/haive/mcp/downloader/integration.py

- [ ] **Line 112** (`reportUndefinedVariable`)
  - **Issue**: "StdioServerParameters" is not defined
  - **Location**: `haive-mcp/src/haive/mcp/downloader/integration.py:112:32`

- [ ] **Line 118** (`reportUndefinedVariable`)
  - **Issue**: "stdio_client" is not defined
  - **Location**: `haive-mcp/src/haive/mcp/downloader/integration.py:118:40`

- [ ] **Line 124** (`reportUndefinedVariable`)
  - **Issue**: "SSEConnection" is not defined
  - **Location**: `haive-mcp/src/haive/mcp/downloader/integration.py:124:34`

- [ ] **Line 127** (`reportOptionalMemberAccess`)
  - **Issue**: "connect" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/integration.py:127:38`

- [ ] **Line 162** (`reportOptionalMemberAccess`)
  - **Issue**: "list_tools" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/integration.py:162:46`

- [ ] **Line 170** (`reportOptionalMemberAccess`)
  - **Issue**: "list_resources" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/integration.py:170:50`

- [ ] **Line 176** (`reportOptionalMemberAccess`)
  - **Issue**: "list_prompts" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/integration.py:176:48`

- [ ] **Line 234** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "connection"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/integration.py:234:21`

- [ ] **Line 359** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "capabilities" for class "BaseTool"
      Attribute "capabilities" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/downloader/integration.py:359:68`

- [ ] **Line 432** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "DownloadResult"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/integration.py:432:15`

- [ ] **Line 434** (`reportIndexIssue`)
  - **Issue**: "**getitem**" method not defined on type "DownloadResult"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/integration.py:434:55`

- [ ] **Line 440** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "install_dir" for class "GeneralMCPDownloader"
      Attribute "install_dir" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/downloader/integration.py:440:28`

- [ ] **Line 657** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "install_dir" for class "GeneralMCPDownloader"
      Attribute "install_dir" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/downloader/integration.py:657:38`

- [ ] **Line 673** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "api_key", "category", "description", "health_check_interval"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/integration.py:673:28`

- [ ] **Line 683** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "categories", "required_capabilities", "on_server_connected", "on_server_failed", "on_tool_discovered"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/integration.py:683:15`

### 📄 haive-mcp/src/haive/mcp/downloader/legacy_core.py

- [ ] **Line 119** (`reportRedeclaration`)
  - **Issue**: Method declaration "\_run_command" is obscured by a declaration of the same name
  - **Location**: `haive-mcp/src/haive/mcp/downloader/legacy_core.py:119:14`

- [ ] **Line 223** (`reportRedeclaration`)
  - **Issue**: Method declaration "\_run_command" is obscured by a declaration of the same name
  - **Location**: `haive-mcp/src/haive/mcp/downloader/legacy_core.py:223:14`

- [ ] **Line 303** (`reportRedeclaration`)
  - **Issue**: Method declaration "\_run_command" is obscured by a declaration of the same name
  - **Location**: `haive-mcp/src/haive/mcp/downloader/legacy_core.py:303:14`

- [ ] **Line 402** (`reportRedeclaration`)
  - **Issue**: Method declaration "\_run_command" is obscured by a declaration of the same name
  - **Location**: `haive-mcp/src/haive/mcp/downloader/legacy_core.py:402:14`

- [ ] **Line 514** (`reportOptionalMemberAccess`)
  - **Issue**: "safe_load" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/legacy_core.py:514:30`

- [ ] **Line 605** (`reportOptionalMemberAccess`)
  - **Issue**: "dump" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/legacy_core.py:605:17`

- [ ] **Line 617** (`reportOptionalMemberAccess`)
  - **Issue**: "ClientSession" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/downloader/legacy_core.py:617:31`

- [ ] **Line 755** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get" for class "BaseException"
      Attribute "get" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/downloader/legacy_core.py:755:24`

- [ ] **Line 761** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "get" for class "BaseException"
      Attribute "get" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/downloader/legacy_core.py:761:40`

- [ ] **Line 859** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "env_vars" for class "ServerConfig"
      Attribute "env_vars" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/downloader/legacy_core.py:859:55`

### 📄 haive-mcp/src/haive/mcp/dynamic_activation_mcp.py

- [ ] **Line 423** (`reportOptionalMemberAccess`)
  - **Issue**: "execute_agent" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/dynamic_activation_mcp.py:423:43`

### 📄 haive-mcp/src/haive/mcp/dynamic_mcp_tool.py

- [ ] **Line 23** (`reportAttributeAccessIssue`)
  - **Issue**: "MCPDocumentationLoader" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/dynamic_mcp_tool.py:23:36`

- [ ] **Line 101** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "setup" for class "MCPDocumentationAgent"
      Attribute "setup" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/dynamic_mcp_tool.py:101:28`

- [ ] **Line 214** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[Unknown, dict[str, Unknown]]" cannot be assigned to parameter "connections" of type "dict[str, Connection] | None" in function "**init**"
      Type "dict[Unknown, dict[str, Unknown]]" is not assignable to type "dict[str, Connection] | None"
        "dict[Unknown, dict[str, Unknown]]" is not assignable to "dict[str, Connection]"
          Type parameter "\_VT@dict" is invariant, but "dict[str, Unknown]" is not the same as "Connection"
          Consider switching from "dict" to "Mapping" which is covariant in the value type
        "dict[Unknown, dict[str, Unknown]]" is not assignable to "None"
  - **Location**: `haive-mcp/src/haive/mcp/dynamic_mcp_tool.py:214:42`

- [ ] **Line 279** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[Unknown, dict[str, Unknown]]" cannot be assigned to parameter "connections" of type "dict[str, Connection] | None" in function "**init**"
      Type "dict[Unknown, dict[str, Unknown]]" is not assignable to type "dict[str, Connection] | None"
        "dict[Unknown, dict[str, Unknown]]" is not assignable to "dict[str, Connection]"
          Type parameter "\_VT@dict" is invariant, but "dict[str, Unknown]" is not the same as "Connection"
          Consider switching from "dict" to "Mapping" which is covariant in the value type
        "dict[Unknown, dict[str, Unknown]]" is not assignable to "None"
  - **Location**: `haive-mcp/src/haive/mcp/dynamic_mcp_tool.py:279:42`

### 📄 haive-mcp/src/haive/mcp/enhance_mcp_data.py

- [ ] **Line 78** (`reportOptionalMemberAccess`)
  - **Issue**: "get" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/enhance_mcp_data.py:78:36`

- [ ] **Line 159** (`reportArgumentType`)
  - **Issue**: Argument of type "slice[None, Literal[3], None]" cannot be assigned to parameter "key" of type "str" in function "**getitem**"
      "slice[None, Literal[3], None]" is not assignable to "str"
  - **Location**: `haive-mcp/src/haive/mcp/enhance_mcp_data.py:159:24`

### 📄 haive-mcp/src/haive/mcp/enhanced_parent_self_query_retriever.py

- [ ] **Line 19** (`reportPrivateImportUsage`)
  - **Issue**: "AttributeInfo" is not exported from module "langchain.chains.query_constructor.base"
      Import from "langchain.chains.query_constructor.schema" instead
  - **Location**: `haive-mcp/src/haive/mcp/enhanced_parent_self_query_retriever.py:19:52`

- [ ] **Line 26** (`reportAttributeAccessIssue`)
  - **Issue**: "MCPDocumentationLoader" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/enhanced_parent_self_query_retriever.py:26:36`

- [ ] **Line 202** (`reportArgumentType`)
  - **Issue**: Argument of type "Any | None" cannot be assigned to parameter "vectorstore" of type "VectorStore" in function "from_llm"
      Type "Any | None" is not assignable to type "VectorStore"
        "None" is not assignable to "VectorStore"
  - **Location**: `haive-mcp/src/haive/mcp/enhanced_parent_self_query_retriever.py:202:24`

### 📄 haive-mcp/src/haive/mcp/fastapi_mcp_server.py

- [ ] **Line 103** (`reportOptionalMemberAccess`)
  - **Issue**: "enhanced_query" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/fastapi_mcp_server.py:103:36`

- [ ] **Line 228** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, dict[str, Unknown]]" cannot be assigned to parameter "connections" of type "dict[str, Connection] | None" in function "**init**"
      Type "dict[str, dict[str, Unknown]]" is not assignable to type "dict[str, Connection] | None"
        "dict[str, dict[str, Unknown]]" is not assignable to "dict[str, Connection]"
          Type parameter "\_VT@dict" is invariant, but "dict[str, Unknown]" is not the same as "Connection"
          Consider switching from "dict" to "Mapping" which is covariant in the value type
        "dict[str, dict[str, Unknown]]" is not assignable to "None"
  - **Location**: `haive-mcp/src/haive/mcp/fastapi_mcp_server.py:228:38`

### 📄 haive-mcp/src/haive/mcp/haive_agent_mcp_integration.py

- [ ] **Line 16** (`reportMissingImports`)
  - **Issue**: Import "fastmcp_runner" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/haive_agent_mcp_integration.py:16:5`

- [ ] **Line 20** (`reportMissingImports`)
  - **Issue**: Import "integrated_mcp_system" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/haive_agent_mcp_integration.py:20:5`

### 📄 haive-mcp/src/haive/mcp/installers/**init**.py

- [ ] **Line 3** (`reportMissingImports`)
  - **Issue**: Import "installers.advanced_code_installer" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/installers/__init__.py:3:5`

- [ ] **Line 16** (`reportMissingImports`)
  - **Issue**: Import "installers.config_manager" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/installers/__init__.py:16:5`

- [ ] **Line 28** (`reportMissingImports`)
  - **Issue**: Import "installers.safe_pattern_installer" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/installers/__init__.py:28:5`

### 📄 haive-mcp/src/haive/mcp/installers/advanced_code_installer.py

- [ ] **Line 254** (`reportReturnType`)
  - **Issue**: Type "BaseTool" is not assignable to return type "StructuredTool"
      "BaseTool" is not assignable to "StructuredTool"
  - **Location**: `haive-mcp/src/haive/mcp/installers/advanced_code_installer.py:254:15`

- [ ] **Line 256** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, bool]" cannot be assigned to parameter "interrupt_config" of type "HumanInterruptConfig" in function "add_human_in_the_loop"
      "allow_ignore" is required in "HumanInterruptConfig"
  - **Location**: `haive-mcp/src/haive/mcp/installers/advanced_code_installer.py:256:29`

- [ ] **Line 333** (`reportReturnType`)
  - **Issue**: Type "BaseTool" is not assignable to return type "StructuredTool"
      "BaseTool" is not assignable to "StructuredTool"
  - **Location**: `haive-mcp/src/haive/mcp/installers/advanced_code_installer.py:333:15`

### 📄 haive-mcp/src/haive/mcp/installers/safe_pattern_installer.py

- [ ] **Line 229** (`reportReturnType`)
  - **Issue**: Type "BaseTool" is not assignable to return type "StructuredTool"
      "BaseTool" is not assignable to "StructuredTool"
  - **Location**: `haive-mcp/src/haive/mcp/installers/safe_pattern_installer.py:229:19`

- [ ] **Line 231** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, bool]" cannot be assigned to parameter "interrupt_config" of type "HumanInterruptConfig" in function "add_human_in_the_loop"
      "allow_ignore" is required in "HumanInterruptConfig"
  - **Location**: `haive-mcp/src/haive/mcp/installers/safe_pattern_installer.py:231:33`

- [ ] **Line 340** (`reportOptionalMemberAccess`)
  - **Issue**: "write" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/installers/safe_pattern_installer.py:340:26`

- [ ] **Line 341** (`reportOptionalMemberAccess`)
  - **Issue**: "flush" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/installers/safe_pattern_installer.py:341:26`

- [ ] **Line 345** (`reportOptionalMemberAccess`)
  - **Issue**: "readline" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/installers/safe_pattern_installer.py:345:38`

- [ ] **Line 351** (`reportOptionalMemberAccess`)
  - **Issue**: "write" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/installers/safe_pattern_installer.py:351:34`

- [ ] **Line 352** (`reportOptionalMemberAccess`)
  - **Issue**: "flush" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/installers/safe_pattern_installer.py:352:34`

- [ ] **Line 361** (`reportOptionalMemberAccess`)
  - **Issue**: "write" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/installers/safe_pattern_installer.py:361:34`

- [ ] **Line 362** (`reportOptionalMemberAccess`)
  - **Issue**: "flush" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/installers/safe_pattern_installer.py:362:34`

- [ ] **Line 365** (`reportOptionalMemberAccess`)
  - **Issue**: "readline" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/installers/safe_pattern_installer.py:365:52`

### 📄 haive-mcp/src/haive/mcp/integrated_launcher.py

- [ ] **Line 23** (`reportMissingImports`)
  - **Issue**: Import "streamlit" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/integrated_launcher.py:23:15`

- [ ] **Line 28** (`reportMissingImports`)
  - **Issue**: Import "plotly" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/integrated_launcher.py:28:15`

### 📄 haive-mcp/src/haive/mcp/integrated_mcp_system.py

- [ ] **Line 24** (`reportMissingImports`)
  - **Issue**: Import "plotly.express" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/integrated_mcp_system.py:24:7`

- [ ] **Line 25** (`reportMissingImports`)
  - **Issue**: Import "streamlit" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/integrated_mcp_system.py:25:7`

- [ ] **Line 26** (`reportMissingImports`)
  - **Issue**: Import "csv_viewer" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/integrated_mcp_system.py:26:5`

- [ ] **Line 27** (`reportMissingImports`)
  - **Issue**: Import "self_query_mcp_agent" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/integrated_mcp_system.py:27:5`

### 📄 haive-mcp/src/haive/mcp/integration/aug_llm_mcp_extension.py

- [ ] **Line 49** (`reportGeneralTypeIssues`)
  - **Issue**: "name" overrides a field of the same name but is missing a default value
  - **Location**: `haive-mcp/src/haive/mcp/integration/aug_llm_mcp_extension.py:49:4`

- [ ] **Line 125** (`reportCallIssue`)
  - **Issue**: Expected 0 positional arguments
  - **Location**: `haive-mcp/src/haive/mcp/integration/aug_llm_mcp_extension.py:125:42`

- [ ] **Line 126** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "initialize" for class "MCPManager"
      Attribute "initialize" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/integration/aug_llm_mcp_extension.py:126:35`

- [ ] **Line 153** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "clients" for class "MCPManager"
      Attribute "clients" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/integration/aug_llm_mcp_extension.py:153:52`

- [ ] **Line 190** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "clients" for class "MCPManager"
      Attribute "clients" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/integration/aug_llm_mcp_extension.py:190:52`

- [ ] **Line 196** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "content"
  - **Location**: `haive-mcp/src/haive/mcp/integration/aug_llm_mcp_extension.py:196:35`

- [ ] **Line 216** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "clients" for class "MCPManager"
      Attribute "clients" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/integration/aug_llm_mcp_extension.py:216:52`

- [ ] **Line 284** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "clients" for class "MCPManager"
      Attribute "clients" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/integration/aug_llm_mcp_extension.py:284:52`

- [ ] **Line 343** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "categories", "required_capabilities", "on_server_connected", "on_server_failed", "on_tool_discovered"
  - **Location**: `haive-mcp/src/haive/mcp/integration/aug_llm_mcp_extension.py:343:17`

### 📄 haive-mcp/src/haive/mcp/manager.py

- [ ] **Line 76** (`reportAttributeAccessIssue`)
  - **Issue**: "stdio_client" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/manager.py:76:4`

- [ ] **Line 346** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "command" of type "str" in function "**init**"
      Type "str | None" is not assignable to type "str"
        "None" is not assignable to "str"
  - **Location**: `haive-mcp/src/haive/mcp/manager.py:346:28`

- [ ] **Line 455** (`reportCallIssue`)
  - **Issue**: No overloads for "run" match the provided arguments
  - **Location**: `haive-mcp/src/haive/mcp/manager.py:455:25`

- [ ] **Line 456** (`reportArgumentType`)
  - **Issue**: Argument of type "list[str | None]" cannot be assigned to parameter "args" of type "\_CMD" in function "run"
      Type "str | None" is not assignable to type "StrOrBytesPath"
        Type "None" is not assignable to type "StrOrBytesPath"
          "None" is not assignable to "str"
          "None" is not assignable to "bytes"
          "None" is incompatible with protocol "PathLike[str]"
            "**fspath**" is not present
          "None" is incompatible with protocol "PathLike[bytes]"
            "**fspath**" is not present
  - **Location**: `haive-mcp/src/haive/mcp/manager.py:456:21`

- [ ] **Line 469** (`reportArgumentType`)
  - **Issue**: Argument of type "str | None" cannot be assigned to parameter "url" of type "StrOrURL" in function "get"
      Type "str | None" is not assignable to type "StrOrURL"
        Type "None" is not assignable to type "StrOrURL"
          "None" is not assignable to "str"
          "None" is not assignable to "URL"
  - **Location**: `haive-mcp/src/haive/mcp/manager.py:469:20`

- [ ] **Line 607** (`reportOptionalMemberAccess`)
  - **Issue**: "dict" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/manager.py:607:54`

### 📄 haive-mcp/src/haive/mcp/mcp_rag_agent.py

- [ ] **Line 48** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot assign to attribute "system_message" for class "BaseRAGAgent"
      Attribute "system_message" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/mcp_rag_agent.py:48:10`

- [ ] **Line 331** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "arun" for class "BaseRAGAgent"
      Could not bind method "arun" because "BaseRAGAgent" is not assignable to parameter "self"
        "BaseRAGAgent" is incompatible with protocol "AgentProtocol"
          "config" is not present
          "\_disable_checkpointing" is not present
            "input_schema" is invariant because it is mutable
            "input_schema" is an incompatible type
              Type "type[BaseModel] | dict[str, Any] | None" is not assignable to type "type[BaseModel] | None"
            "output_schema" is invariant because it is mutable
  - **Location**: `haive-mcp/src/haive/mcp/mcp_rag_agent.py:331:33`

### 📄 haive-mcp/src/haive/mcp/mcp_simple_rag_agent.py

- [ ] **Line 132** (`reportCallIssue`)
  - **Issue**: No parameter named "provider"
  - **Location**: `haive-mcp/src/haive/mcp/mcp_simple_rag_agent.py:132:8`

- [ ] **Line 453** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "arun" for class "BaseRAGAgent"
      Could not bind method "arun" because "BaseRAGAgent" is not assignable to parameter "self"
        "BaseRAGAgent" is incompatible with protocol "AgentProtocol"
          "config" is not present
          "\_disable_checkpointing" is not present
            "input_schema" is invariant because it is mutable
            "input_schema" is an incompatible type
              Type "type[BaseModel] | dict[str, Any] | None" is not assignable to type "type[BaseModel] | None"
            "output_schema" is invariant because it is mutable
  - **Location**: `haive-mcp/src/haive/mcp/mcp_simple_rag_agent.py:453:33`

- [ ] **Line 501** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "\_compiled_app" for class "BaseRAGAgent"
      Attribute "\_compiled_app" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/mcp_simple_rag_agent.py:501:34`

- [ ] **Line 506** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "create_vectorstore" for class "BaseRetrieverConfig"
      Attribute "create_vectorstore" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/mcp_simple_rag_agent.py:506:62`

### 📄 haive-mcp/src/haive/mcp/mcp_simple_tool_agent.py

- [ ] **Line 20** (`reportAttributeAccessIssue`)
  - **Issue**: "MCPDocumentationLoader" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/mcp_simple_tool_agent.py:20:36`

- [ ] **Line 192** (`reportCallIssue`)
  - **Issue**: No parameter named "tools"
  - **Location**: `haive-mcp/src/haive/mcp/mcp_simple_tool_agent.py:192:8`

- [ ] **Line 193** (`reportCallIssue`)
  - **Issue**: No parameter named "system_prompt"
  - **Location**: `haive-mcp/src/haive/mcp/mcp_simple_tool_agent.py:193:8`

- [ ] **Line 444** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "arun" for class "SimpleAgent"
      Could not bind method "arun" because "SimpleAgent" is not assignable to parameter "self"
        "SimpleAgent" is incompatible with protocol "AgentProtocol"
          "config" is not present
          "\_disable_checkpointing" is not present
            "input_schema" is invariant because it is mutable
            "input_schema" is an incompatible type
              Type "type[BaseModel] | dict[str, Any] | None" is not assignable to type "type[BaseModel] | None"
            "output_schema" is invariant because it is mutable
  - **Location**: `haive-mcp/src/haive/mcp/mcp_simple_tool_agent.py:444:33`

### 📄 haive-mcp/src/haive/mcp/mixins/**init**.py

- [ ] **Line 3** (`reportMissingImports`)
  - **Issue**: Import "mixins.mcp_mixin" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/mixins/__init__.py:3:5`

### 📄 haive-mcp/src/haive/mcp/mixins/mcp_mixin.py

- [ ] **Line 50** (`reportMissingImports`)
  - **Issue**: Import "haive.core.utils.component_discovery" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/mixins/mcp_mixin.py:50:5`

- [ ] **Line 136** (`reportInvalidTypeForm`)
  - **Issue**: Variable not allowed in type expression
  - **Location**: `haive-mcp/src/haive/mcp/mixins/mcp_mixin.py:136:17`

- [ ] **Line 138** (`reportInvalidTypeForm`)
  - **Issue**: Variable not allowed in type expression
  - **Location**: `haive-mcp/src/haive/mcp/mixins/mcp_mixin.py:138:26`

- [ ] **Line 165** (`reportOptionalMemberAccess`)
  - **Issue**: "lazy_init" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/mixins/mcp_mixin.py:165:61`

- [ ] **Line 170** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "tools" for class "MCPMixin\*"
      Attribute "tools" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/mixins/mcp_mixin.py:170:58`

- [ ] **Line 172** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "tools" for class "MCPMixin\*"
      Attribute "tools" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/mixins/mcp_mixin.py:172:40`

- [ ] **Line 173** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "tools" for class "MCPMixin\*"
      Attribute "tools" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/mixins/mcp_mixin.py:173:29`

- [ ] **Line 229** (`reportOptionalCall`)
  - **Issue**: Object of type "None" cannot be called
  - **Location**: `haive-mcp/src/haive/mcp/mixins/mcp_mixin.py:229:35`

- [ ] **Line 229** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, dict[str, Any]]" cannot be assigned to parameter "connections" of type "dict[str, Connection] | None" in function "**init**"
      Type "dict[str, dict[str, Any]]" is not assignable to type "dict[str, Connection] | None"
        "dict[str, dict[str, Any]]" is not assignable to "dict[str, Connection]"
          Type parameter "\_VT@dict" is invariant, but "dict[str, Any]" is not the same as "Connection"
          Consider switching from "dict" to "Mapping" which is covariant in the value type
        "dict[str, dict[str, Any]]" is not assignable to "None"
  - **Location**: `haive-mcp/src/haive/mcp/mixins/mcp_mixin.py:229:56`

- [ ] **Line 260** (`reportOptionalMemberAccess`)
  - **Issue**: "servers" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/mixins/mcp_mixin.py:260:58`

- [ ] **Line 280** (`reportOptionalCall`)
  - **Issue**: Object of type "None" cannot be called
  - **Location**: `haive-mcp/src/haive/mcp/mixins/mcp_mixin.py:280:26`

- [ ] **Line 280** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, dict[str, Any]]" cannot be assigned to parameter "connections" of type "dict[str, Connection] | None" in function "**init**"
      Type "dict[str, dict[str, Any]]" is not assignable to type "dict[str, Connection] | None"
        "dict[str, dict[str, Any]]" is not assignable to "dict[str, Connection]"
          Type parameter "\_VT@dict" is invariant, but "dict[str, Any]" is not the same as "Connection"
          Consider switching from "dict" to "Mapping" which is covariant in the value type
        "dict[str, dict[str, Any]]" is not assignable to "None"
  - **Location**: `haive-mcp/src/haive/mcp/mixins/mcp_mixin.py:280:47`

- [ ] **Line 289** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "close" for class "MultiServerMCPClient"
      Attribute "close" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/mixins/mcp_mixin.py:289:34`

### 📄 haive-mcp/src/haive/mcp/production_mcp_tool.py

- [ ] **Line 25** (`reportAttributeAccessIssue`)
  - **Issue**: "MCPDocumentationLoader" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/production_mcp_tool.py:25:36`

- [ ] **Line 159** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "setup" for class "MCPDocumentationAgent"
      Attribute "setup" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/production_mcp_tool.py:159:28`

- [ ] **Line 344** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, dict[str, Unknown]]" cannot be assigned to parameter "connections" of type "dict[str, Connection] | None" in function "**init**"
      Type "dict[str, dict[str, Unknown]]" is not assignable to type "dict[str, Connection] | None"
        "dict[str, dict[str, Unknown]]" is not assignable to "dict[str, Connection]"
          Type parameter "\_VT@dict" is invariant, but "dict[str, Unknown]" is not the same as "Connection"
          Consider switching from "dict" to "Mapping" which is covariant in the value type
        "dict[str, dict[str, Unknown]]" is not assignable to "None"
  - **Location**: `haive-mcp/src/haive/mcp/production_mcp_tool.py:344:47`

- [ ] **Line 421** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, dict[str, Unknown]]" cannot be assigned to parameter "connections" of type "dict[str, Connection] | None" in function "**init**"
      Type "dict[str, dict[str, Unknown]]" is not assignable to type "dict[str, Connection] | None"
        "dict[str, dict[str, Unknown]]" is not assignable to "dict[str, Connection]"
          Type parameter "\_VT@dict" is invariant, but "dict[str, Unknown]" is not the same as "Connection"
          Consider switching from "dict" to "Mapping" which is covariant in the value type
        "dict[str, dict[str, Unknown]]" is not assignable to "None"
  - **Location**: `haive-mcp/src/haive/mcp/production_mcp_tool.py:421:47`

- [ ] **Line 477** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "\_generate_generic_tools" for class "ProductionMCPTool\*"
      Attribute "\_generate_generic_tools" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/production_mcp_tool.py:477:25`

### 📄 haive-mcp/src/haive/mcp/self_query_mcp_agent.py

- [ ] **Line 12** (`reportPrivateImportUsage`)
  - **Issue**: "AttributeInfo" is not exported from module "langchain.chains.query_constructor.base"
      Import from "langchain.chains.query_constructor.schema" instead
  - **Location**: `haive-mcp/src/haive/mcp/self_query_mcp_agent.py:12:52`

### 📄 haive-mcp/src/haive/mcp/servers/**init**.py

- [ ] **Line 3** (`reportMissingImports`)
  - **Issue**: Import "servers.dataflow_mcp_server" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/servers/__init__.py:3:5`

- [ ] **Line 4** (`reportMissingImports`)
  - **Issue**: Import "servers.http_server" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/servers/__init__.py:4:5`

- [ ] **Line 5** (`reportMissingImports`)
  - **Issue**: Import "servers.simple_http_server" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/servers/__init__.py:5:5`

### 📄 haive-mcp/src/haive/mcp/servers/dataflow_mcp_server.py

- [ ] **Line 71** (`reportCallIssue`)
  - **Issue**: Object of type "ModuleType" is not callable
      Attribute "**call**" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/servers/dataflow_mcp_server.py:71:60`

- [ ] **Line 130** (`reportCallIssue`)
  - **Issue**: No parameter named "auto_register"
  - **Location**: `haive-mcp/src/haive/mcp/servers/dataflow_mcp_server.py:130:37`

- [ ] **Line 141** (`reportCallIssue`)
  - **Issue**: No parameter named "auto_register"
  - **Location**: `haive-mcp/src/haive/mcp/servers/dataflow_mcp_server.py:141:35`

- [ ] **Line 189** (`reportCallIssue`)
  - **Issue**: No parameter named "temperature"
  - **Location**: `haive-mcp/src/haive/mcp/servers/dataflow_mcp_server.py:189:52`

### 📄 haive-mcp/src/haive/mcp/servers/dataflow_server.py

- [ ] **Line 52** (`reportGeneralTypeIssues`)
  - **Issue**: "ModuleType" is not iterable
      "**iter**" method not defined
  - **Location**: `haive-mcp/src/haive/mcp/servers/dataflow_server.py:52:31`

- [ ] **Line 65** (`reportCallIssue`)
  - **Issue**: Object of type "ModuleType" is not callable
      Attribute "**call**" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/servers/dataflow_server.py:65:30`

- [ ] **Line 147** (`reportCallIssue`)
  - **Issue**: Object of type "ModuleType" is not callable
      Attribute "**call**" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/servers/dataflow_server.py:147:22`

- [ ] **Line 183** (`reportCallIssue`)
  - **Issue**: Object of type "ModuleType" is not callable
      Attribute "**call**" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/servers/dataflow_server.py:183:18`

- [ ] **Line 186** (`reportCallIssue`)
  - **Issue**: Object of type "ModuleType" is not callable
      Attribute "**call**" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/servers/dataflow_server.py:186:18`

- [ ] **Line 189** (`reportCallIssue`)
  - **Issue**: Object of type "ModuleType" is not callable
      Attribute "**call**" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/servers/dataflow_server.py:189:18`

- [ ] **Line 333** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "server_info" for class "FastMCP"
      Attribute "server_info" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/servers/dataflow_server.py:333:5`

- [ ] **Line 364** (`reportArgumentType`)
  - **Issue**: Argument of type "None" cannot be assigned to parameter "main" of type "Coroutine[Any, Any, _T@run]" in function "run"
      "None" is not assignable to "Coroutine[Any, Any, _T@run]"
  - **Location**: `haive-mcp/src/haive/mcp/servers/dataflow_server.py:364:16`

### 📄 haive-mcp/src/haive/mcp/servers/http_server.py

- [ ] **Line 15** (`reportAttributeAccessIssue`)
  - **Issue**: "SSEServerTransport" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/servers/http_server.py:15:27`

- [ ] **Line 191** (`reportOptionalMemberAccess`)
  - **Issue**: "handle_connection" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/servers/http_server.py:191:47`

### 📄 haive-mcp/src/haive/mcp/simple_faiss_retriever.py

- [ ] **Line 17** (`reportAttributeAccessIssue`)
  - **Issue**: "MCPDocumentationLoader" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/simple_faiss_retriever.py:17:36`

### 📄 haive-mcp/src/haive/mcp/simple_rag_mcp_agent.py

- [ ] **Line 42** (`reportCallIssue`)
  - **Issue**: No parameter named "retriever_config"
  - **Location**: `haive-mcp/src/haive/mcp/simple_rag_mcp_agent.py:42:36`

- [ ] **Line 125** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "arun" for class "MCPSimpleRAGAgent"
      Could not bind method "arun" because "MCPSimpleRAGAgent" is not assignable to parameter "self"
        "MCPSimpleRAGAgent" is incompatible with protocol "AgentProtocol"
          "config" is not present
          "\_disable_checkpointing" is not present
            "input_schema" is invariant because it is mutable
            "input_schema" is an incompatible type
              Type "type[BaseModel] | dict[str, Any] | None" is not assignable to type "type[BaseModel] | None"
            "output_schema" is invariant because it is mutable
  - **Location**: `haive-mcp/src/haive/mcp/simple_rag_mcp_agent.py:125:20`

- [ ] **Line 319** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "arun" for class "MCPSimpleRAGAgent"
      Could not bind method "arun" because "MCPSimpleRAGAgent" is not assignable to parameter "self"
        "MCPSimpleRAGAgent" is incompatible with protocol "AgentProtocol"
          "config" is not present
          "\_disable_checkpointing" is not present
            "input_schema" is invariant because it is mutable
            "input_schema" is an incompatible type
              Type "type[BaseModel] | dict[str, Any] | None" is not assignable to type "type[BaseModel] | None"
            "output_schema" is invariant because it is mutable
  - **Location**: `haive-mcp/src/haive/mcp/simple_rag_mcp_agent.py:319:35`

- [ ] **Line 322** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "retriever_config" for class "MCPSimpleRAGAgent"
      Attribute "retriever_config" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/simple_rag_mcp_agent.py:322:38`

### 📄 haive-mcp/src/haive/mcp/test_direct.py

- [ ] **Line 24** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "arun" for class "BaseRAGAgent"
      Could not bind method "arun" because "BaseRAGAgent" is not assignable to parameter "self"
        "BaseRAGAgent" is incompatible with protocol "AgentProtocol"
          "config" is not present
          "\_disable_checkpointing" is not present
            "input_schema" is invariant because it is mutable
            "input_schema" is an incompatible type
              Type "type[BaseModel] | dict[str, Any] | None" is not assignable to type "type[BaseModel] | None"
            "output_schema" is invariant because it is mutable
  - **Location**: `haive-mcp/src/haive/mcp/test_direct.py:24:33`

- [ ] **Line 43** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "create_vectorstore" for class "BaseRetrieverConfig"
      Attribute "create_vectorstore" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/test_direct.py:43:43`

### 📄 haive-mcp/src/haive/mcp/tools/**init**.py

- [ ] **Line 3** (`reportMissingImports`)
  - **Issue**: Import "tools.ai_assistant" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/tools/__init__.py:3:5`

- [ ] **Line 13** (`reportMissingImports`)
  - **Issue**: Import "tools.server_selector" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/tools/__init__.py:13:5`

- [ ] **Line 30** (`reportMissingImports`)
  - **Issue**: Import "tools.server_tester" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/tools/__init__.py:30:5`

### 📄 haive-mcp/src/haive/mcp/tools/ai_assistant.py

- [ ] **Line 437** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "categories", "required_capabilities", "on_server_connected", "on_server_failed", "on_tool_discovered"
  - **Location**: `haive-mcp/src/haive/mcp/tools/ai_assistant.py:437:15`

- [ ] **Line 485** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "url", "api_key", "category", "health_check_interval"
  - **Location**: `haive-mcp/src/haive/mcp/tools/ai_assistant.py:485:21`

- [ ] **Line 493** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "url", "api_key", "category", "health_check_interval"
  - **Location**: `haive-mcp/src/haive/mcp/tools/ai_assistant.py:493:26`

### 📄 haive-mcp/src/haive/mcp/tools/server_selector.py

- [ ] **Line 358** (`reportAssignmentType`)
  - **Issue**: Type "dict[str, dict[str, Any]]" is not assignable to declared type "list[dict[str, Any]] | None"
      Type "dict[str, dict[str, Any]]" is not assignable to type "list[dict[str, Any]] | None"
        "dict[str, dict[str, Any]]" is not assignable to "list[dict[str, Any]]"
        "dict[str, dict[str, Any]]" is not assignable to "None"
  - **Location**: `haive-mcp/src/haive/mcp/tools/server_selector.py:358:22`

- [ ] **Line 361** (`reportArgumentType`)
  - **Issue**: Argument of type "list[dict[str, Any]] | None" cannot be assigned to parameter "servers" of type "list[dict[str, Any]]" in function "**init**"
      Type "list[dict[str, Any]] | None" is not assignable to type "list[dict[str, Any]]"
        "None" is not assignable to "list[dict[str, Any]]"
  - **Location**: `haive-mcp/src/haive/mcp/tools/server_selector.py:361:35`

- [ ] **Line 366** (`reportOptionalIterable`)
  - **Issue**: Object of type "None" cannot be used as iterable value
  - **Location**: `haive-mcp/src/haive/mcp/tools/server_selector.py:366:22`

- [ ] **Line 418** (`reportOptionalIterable`)
  - **Issue**: Object of type "None" cannot be used as iterable value
  - **Location**: `haive-mcp/src/haive/mcp/tools/server_selector.py:418:22`

- [ ] **Line 590** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "categories", "required_capabilities", "on_server_connected", "on_server_failed", "on_tool_discovered"
  - **Location**: `haive-mcp/src/haive/mcp/tools/server_selector.py:590:15`

- [ ] **Line 619** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "api_key", "health_check_interval"
  - **Location**: `haive-mcp/src/haive/mcp/tools/server_selector.py:619:19`

### 📄 haive-mcp/src/haive/mcp/tools/server_tester.py

- [ ] **Line 75** (`reportAssignmentType`)
  - **Issue**: Type "None" is not assignable to declared type "list[str]"
      "None" is not assignable to "list[str]"
  - **Location**: `haive-mcp/src/haive/mcp/tools/server_tester.py:75:36`

- [ ] **Line 76** (`reportAssignmentType`)
  - **Issue**: Type "None" is not assignable to declared type "list[str]"
      "None" is not assignable to "list[str]"
  - **Location**: `haive-mcp/src/haive/mcp/tools/server_tester.py:76:26`

- [ ] **Line 213** (`reportAttributeAccessIssue`)
  - **Issue**: "MCPAdapter" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/tools/server_tester.py:213:51`

- [ ] **Line 230** (`reportArgumentType`)
  - **Issue**: Argument of type "dict[str, dict[str, Any]]" cannot be assigned to parameter "connections" of type "dict[str, Connection] | None" in function "**init**"
      Type "dict[str, dict[str, Any]]" is not assignable to type "dict[str, Connection] | None"
        "dict[str, dict[str, Any]]" is not assignable to "dict[str, Connection]"
          Type parameter "\_VT@dict" is invariant, but "dict[str, Any]" is not the same as "Connection"
          Consider switching from "dict" to "Mapping" which is covariant in the value type
        "dict[str, dict[str, Any]]" is not assignable to "None"
  - **Location**: `haive-mcp/src/haive/mcp/tools/server_tester.py:230:46`

- [ ] **Line 257** (`reportAttributeAccessIssue`)
  - **Issue**: Cannot access attribute "close" for class "MultiServerMCPClient"
      Attribute "close" is unknown
  - **Location**: `haive-mcp/src/haive/mcp/tools/server_tester.py:257:37`

### 📄 haive-mcp/src/haive/mcp/utils/**init**.py

- [ ] **Line 3** (`reportMissingImports`)
  - **Issue**: Import "utils.extract_mcp_github_repos" could not be resolved
  - **Location**: `haive-mcp/src/haive/mcp/utils/__init__.py:3:5`

### 📄 haive-mcp/src/haive/mcp/utils/extract_mcp_github_repos.py

- [ ] **Line 289** (`reportOptionalMemberAccess`)
  - **Issue**: "get" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/utils/extract_mcp_github_repos.py:289:36`

- [ ] **Line 345** (`reportCallIssue`)
  - **Issue**: Arguments missing for parameters "stars", "last_updated", "license", "readme_url", "api_base_url"
  - **Location**: `haive-mcp/src/haive/mcp/utils/extract_mcp_github_repos.py:345:31`

- [ ] **Line 378** (`reportOptionalMemberAccess`)
  - **Issue**: "get" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/utils/extract_mcp_github_repos.py:378:40`

- [ ] **Line 389** (`reportOptionalMemberAccess`)
  - **Issue**: "get" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/utils/extract_mcp_github_repos.py:389:40`

- [ ] **Line 421** (`reportOptionalMemberAccess`)
  - **Issue**: "get" is not a known attribute of "None"
  - **Location**: `haive-mcp/src/haive/mcp/utils/extract_mcp_github_repos.py:421:36`

- [ ] **Line 455** (`reportCallIssue`)
  - **Issue**: Argument missing for parameter "content_hash"
  - **Location**: `haive-mcp/src/haive/mcp/utils/extract_mcp_github_repos.py:455:23`

- [ ] **Line 665** (`reportGeneralTypeIssues`)
  - **Issue**: Expected class but received "(obj: object, /) -> TypeIs[(...) -> object]"
  - **Location**: `haive-mcp/src/haive/mcp/utils/extract_mcp_github_repos.py:665:76`

### 📄 haive-mcp/src/haive/mcp/working_enhanced_retriever.py

- [ ] **Line 12** (`reportPrivateImportUsage`)
  - **Issue**: "AttributeInfo" is not exported from module "langchain.chains.query_constructor.base"
      Import from "langchain.chains.query_constructor.schema" instead
  - **Location**: `haive-mcp/src/haive/mcp/working_enhanced_retriever.py:12:52`

- [ ] **Line 21** (`reportAttributeAccessIssue`)
  - **Issue**: "MCPDocumentationLoader" is unknown import symbol
  - **Location**: `haive-mcp/src/haive/mcp/working_enhanced_retriever.py:21:36`

- [ ] **Line 144** (`reportArgumentType`)
  - **Issue**: Argument of type "Chroma | None" cannot be assigned to parameter "vectorstore" of type "VectorStore" in function "from_llm"
      Type "Chroma | None" is not assignable to type "VectorStore"
        "None" is not assignable to "VectorStore"
  - **Location**: `haive-mcp/src/haive/mcp/working_enhanced_retriever.py:144:24`

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
poetry run python -c "from haive.mcp import *; print('✅ Imports OK')"

# Re-run pyright to verify fixes
poetry run pyright packages/haive-mcp/src/ --level error

# Run any existing tests
poetry run pytest packages/haive-mcp/tests/ -v
```

---

**Generated**: 2025-08-02
**Source**: `project_docs/build-reports/pyright-issues/haive-mcp-*.json`
