# haive-mcp Documentation Report

## Package Overview

- **Package Path**: /home/will/Projects/haive/backend/haive/packages/haive-mcp
- **Type Signature Issues**: 11
- **Pydantic Field Issues**: 25
- **Has Main **init**.py**: ❌
- **Has README**: ✅
- **Has Examples**: ✅
- **Total Issues**: 65

## Missing Example Files

- mcp/agents

## Issues by File

### src/haive/mcp/config.py

- 🟡 **Line 139**: Class 'Config' missing docstring

### src/haive/mcp/manager.py

- 🔵 **Line 158**: Method 'MCPManager.model_post_init' missing type hints
- 🔵 **Line 511**: Method 'MCPManager.get_all_server_status' missing type hints

### src/haive/mcp/cli.py

- 🔵 **Line 28**: Function 'print_servers' missing type hints
- 🔵 **Line 64**: Function 'print_recommendations' missing type hints
- 🔵 **Line 312**: Function 'generate_setup_script' missing type hints
- 🔵 **Line 371**: Function 'main' missing type hints

### src/haive/mcp/agents/mcp_agent.py

- 🔵 **Line 122**: Method 'MCPAgent.setup_agent' missing type hints
- 🔵 **Line 210**: Method 'MCPAgent.get_available_capabilities' missing type hints
- 🔵 **Line 276**: Method 'MCPAgent.tool_count' missing type hints
- 🔵 **Line 1**: Function 'MCPAgent.create_with_mcp_servers' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'create_filesystem_agent' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'create_github_agent' uses overly generic type 'Any' for parameter 'engine'
- 🔵 **Line 1**: Function 'create_multi_mcp_agent' uses overly generic type 'Any' for parameter 'engine'

### src/haive/mcp/agents/transferable_mcp_agent.py

- 🔵 **Line 579**: Method 'TransferableMCPAgent.get_transfer_status' missing type hints
- 🔵 **Line 1**: Function 'TransferableMCPAgent.create_collaborative_agents' uses overly generic type 'Any' for parameter 'engine'

### src/haive/mcp/agents/documentation_agent.py

- 🔵 **Line 185**: Method 'MCPDocumentationAgent.create_for_mcp_setup' missing type hints
- 🔵 **Line 233**: Method 'MCPDocumentationAgent.create_for_mcp_research' missing type hints

### src/haive/mcp/cli/mcp_manager.py

- 🔵 **Line 324**: Function 'cli' missing type hints
- 🔵 **Line 334**: Function 'discover' missing type hints
- 🔵 **Line 350**: Function 'install' missing type hints
- 🔵 **Line 375**: Function 'list_servers' missing type hints
- 🔵 **Line 407**: Function 'health_check' missing type hints
- 🔵 **Line 419**: Function 'update' missing type hints
- 🔵 **Line 438**: Function 'config' missing type hints

### src/haive/mcp/discovery/server_discovery.py

- 🔵 **Line 17**: Method 'MCPServerDiscovery.get_discovery_report' missing type hints
- 🔵 **Line 21**: Method 'MCPServerDiscovery.create_mcp_config' missing type hints

### src/haive/mcp/discovery/analyzer.py

- 🔵 **Line 1**: Function 'MCPServerAnalyzer.can_analyze' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'MCPServerAnalyzer.analyze' uses overly generic type 'Any' for parameter 'obj'
- 🔵 **Line 1**: Function 'MCPServerAnalyzer.\_analyze_object' uses overly generic type 'Any' for parameter 'obj'

### src/haive/mcp/tools/server_selector.py

- 🔵 **Line 376**: Method 'MCPServerSelector.get_available_prefixes' missing type hints
- 🔵 **Line 384**: Method 'MCPServerSelector.get_available_categories' missing type hints

### src/haive/mcp/tools/server_tester.py

- 🔵 **Line 176**: Method 'HealthMonitor.get_health_report' missing type hints
- 🔵 **Line 180**: Method 'HealthMonitor.get_unhealthy_servers' missing type hints
- 🔵 **Line 445**: Method 'MCPServerTester.get_test_history' missing type hints
- 🔵 **Line 471**: Method 'MCPServerTester.generate_test_report' missing type hints

### src/haive/mcp/tools/ai_assistant.py

- 🔵 **Line 639**: Method 'MCPAssistant.get_selection_reasoning' missing type hints
- 🔵 **Line 1**: Function 'MCPAssistant.\_get_smart_recommendations' uses overly generic type 'Any' for parameter 'requirements'
- 🔵 **Line 1**: Function 'MCPAssistant.\_suggest_fallbacks' uses overly generic type 'Any' for parameter 'requirements'
- 🔵 **Line 1**: Function 'MCPAssistant.\_generate_reasoning' uses overly generic type 'Any' for parameter 'requirements'

### src/haive/mcp/mixins/mcp_mixin.py

- 🔵 **Line 88**: Method 'MCPMixin.model_post_init' missing type hints
- 🔵 **Line 100**: Method 'MCPMixin.setup_mcp' missing type hints
- 🔵 **Line 430**: Method 'MCPMixin.get_mcp_status' missing type hints

### src/haive/mcp/servers/http_server.py

- 🔵 **Line 212**: Function 'run_server' missing type hints

### src/haive/mcp/servers/simple_http_server.py

- 🔵 **Line 124**: Function 'create_app' missing type hints

### src/haive/mcp/documentation/doc_loader.py

- 🔵 **Line 89**: Method 'MCPDocumentationLoader.load_all_mcp_documents' missing type hints

### src/haive/mcp/utils/extract_mcp_github_repos.py

- 🔵 **Line 134**: Method 'MCPServerMetadata.get_unique_id' missing type hints
- 🔵 **Line 138**: Method 'MCPServerMetadata.to_langchain_metadata' missing type hints
- 🔵 **Line 171**: Method 'MCPServerDocument.compute_content_hash' missing type hints
- 🔵 **Line 177**: Method 'MCPServerDocument.to_langchain_document' missing type hints

### src/haive/mcp/downloader/integration.py

- 🔵 **Line 307**: Method 'MCPCapabilityExtractor.get_all_tools' missing type hints
- 🔵 **Line 322**: Method 'MCPCapabilityExtractor.get_all_resources' missing type hints
- 🔵 **Line 330**: Method 'MCPCapabilityExtractor.get_all_prompts' missing type hints
- 🔵 **Line 621**: Method 'MCPAgentIntegration.get_capability_summary' missing type hints
- 🟡 **Line 90**: Class 'Config' missing docstring

### src/haive/mcp/downloader/github_mass_downloader.py

- 🔵 **Line 52**: Method 'GitHubMCPDownloader.load_all_servers' missing type hints
- 🔵 **Line 61**: Method 'GitHubMCPDownloader.categorize_servers' missing type hints
- 🔵 **Line 87**: Method 'GitHubMCPDownloader.create_server_config' missing type hints
- 🔵 **Line 228**: Method 'GitHubMCPDownloader.show_results' missing type hints
- 🔵 **Line 275**: Method 'GitHubMCPDownloader.create_master_config' missing type hints

### src/haive/mcp/downloader/core.py

- 🔵 **Line 406**: Method 'GeneralMCPDownloader.templates' missing type hints
- 🔵 **Line 421**: Method 'GeneralMCPDownloader.servers' missing type hints
- 🔵 **Line 1011**: Method 'GeneralMCPDownloader.get_all_status' missing type hints

### src/haive/mcp/downloader/legacy_core.py

- 🔵 **Line 451**: Method 'GeneralMCPDownloader.load_config' missing type hints
- 🔵 **Line 486**: Method 'GeneralMCPDownloader.create_default_config' missing type hints
