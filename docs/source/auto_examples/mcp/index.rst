:orphan:

# AI-Enhanced MCP Server Selection Examples

This directory contains examples demonstrating the intelligent MCP server selection and configuration tools designed specifically to help AI agents make better decisions about which servers to use for different tasks.

## 🎯 What Makes This Special for AI

These tools solve a key problem for AI agents: **how to automatically choose the right MCP servers for a task without manual configuration**. Instead of requiring humans to manually select and configure servers, AI agents can now:

1. **Analyze task descriptions** and automatically understand what capabilities are needed
2. **Filter servers by prefix/namespace** to work with specific organizations or types
3. **Get intelligent recommendations** based on task analysis and server capabilities
4. **Auto-generate configurations** with proper fallbacks and error handling
5. **Test and validate servers** before using them in production
6. **Switch contexts dynamically** as tasks change

## 🚀 Quick Start for AI Agents

```python
from haive.mcp.tools import MCPAssistant

# Create AI assistant for server selection
assistant = MCPAssistant()

# Automatically configure for any task
task = "I need to analyze a GitHub repository for security vulnerabilities"
config = await assistant.auto_configure_for_task(task)

# Create agent with optimal configuration
agent = MCPAgent(engine=engine, mcp_config=config.config)
await agent.setup()

# The assistant explains its reasoning
print(assistant.get_selection_reasoning())
```

## 📋 Available Examples

### 1. `ai_enhanced_coding.py` - Complete AI Workflow Demo

**What it shows**: How an AI agent can automatically adapt its capabilities for different coding tasks.

**Key features**:

- Automatic server selection based on task analysis
- Dynamic reconfiguration for different scenarios
- Intelligent fallback strategies
- Performance-aware recommendations

**Run it**:

```bash
cd examples
python ai_enhanced_coding.py
```

**Sample scenarios**:

- 🔒 Security analysis (→ github, filesystem, brave-search)
- 📊 Data research (→ arxiv, postgres, brave-search)
- 🌐 Web development (→ fetch, filesystem, github)
- 🎨 Content creation (→ everart, notion, filesystem)

### 2. CLI Tool - Interactive Server Management

**What it provides**: Command-line interface for exploring and configuring servers.

**Key commands**:

```bash
# List servers by organization/prefix
python -m haive.mcp.cli list-servers --prefix "modelcontextprotocol/"

# Get AI recommendations for a task
python -m haive.mcp.cli recommend "build a web scraper" --ai-mode --reasoning

# Interactive selection with filtering
python -m haive.mcp.cli select --save-config my_config.json

# Auto-configure with full analysis
python -m haive.mcp.cli auto-config "research machine learning papers" --output research.json --generate-script
```

## 🔍 Core Tools Overview

### MCPServerSelector - Basic Filtering and Selection

```python
from haive.mcp.tools import MCPServerSelector

selector = MCPServerSelector()

# Filter by organization/namespace
anthropic_servers = selector.filter_by_prefix("anthropic/")
official_servers = selector.filter_by_prefix("modelcontextprotocol/")

# Get recommendations for tasks
recommendations = selector.recommend_for_task(
    "analyze database performance issues",
    max_servers=3
)

# Interactive selection
chosen = await selector.interactive_select(
    "Choose servers for data analysis:",
    categories=["database", "development"]
)
```

### MCPAssistant - AI-Powered Configuration

```python
from haive.mcp.tools import MCPAssistant

assistant = MCPAssistant()

# Smart configuration with validation
config = await assistant.auto_configure_for_task(
    "Create a content management system with calendar integration",
    prefer_simple_setup=True,
    max_servers=4
)

# Get detailed explanations
explanation = assistant.explain_recommendation("github")
print(f"GitHub is recommended because: {explanation}")

# Validate before use
validation = await assistant.validate_configuration(config.config)
if not validation["valid"]:
    print("Issues found:", validation["issues"])
```

### MCPServerTester - Validation and Monitoring

```python
from haive.mcp.tools import MCPServerTester

tester = MCPServerTester()

# Test individual servers
result = await tester.test_server(server_config)
if result.success:
    print(f"✅ {result.server_name} working ({result.tools_discovered} tools)")
else:
    print(f"❌ {result.server_name} failed: {result.error}")

# Continuous health monitoring
monitor = tester.create_health_monitor(check_interval=60)
await monitor.start_monitoring([server_config])

# Generate comprehensive reports
report = tester.generate_test_report()
print(f"Overall success rate: {report['summary']['overall_success_rate']:.1f}%")
```

## 🎨 Use Cases for AI Agents

### 1. Adaptive Code Analysis Agent

```python
async def analyze_codebase(repo_url: str, analysis_type: str):
    # AI selects appropriate tools based on analysis type
    task = f"Analyze {repo_url} for {analysis_type} issues"
    config = await assistant.auto_configure_for_task(task)

    agent = MCPAgent(engine=engine, mcp_config=config.config)
    await agent.setup()

    # Agent now has optimal tools for the specific analysis
    return await agent.arun({"messages": [{"role": "user", "content": task}]})
```

### 2. Research Assistant with Dynamic Capabilities

```python
async def research_topic(topic: str, sources: List[str]):
    # Different source types need different tools
    if "arxiv" in sources:
        task += " using academic papers from arxiv"
    if "github" in sources:
        task += " including code repositories"
    if "web" in sources:
        task += " with web search"

    config = await assistant.auto_configure_for_task(f"Research {topic} {task}")
    # Agent gets exactly the tools it needs
```

### 3. Development Workflow Automation

```python
async def setup_development_environment(project_type: str):
    # Different project types need different tools
    task = f"Set up development environment for {project_type} project"

    config = await assistant.auto_configure_for_task(task)

    # Automatically gets file system, git, appropriate databases, etc.
    agent = MCPAgent(engine=engine, mcp_config=config.config)
    await agent.setup()

    return agent  # Ready to work on the specific project type
```

## 🔧 Advanced Features

### Prefix-Based Organization

Perfect for working with specific organizations or server types:

```python
# Work only with official servers
official = selector.filter_by_prefix("modelcontextprotocol/")

# Use community servers from specific org
community = selector.filter_by_prefix("awesome-mcp/")

# Experimental features
experimental = selector.filter_by_prefix("experimental/")
```

### Smart Fallback Strategies

AI assistant automatically includes fallback options:

```python
config = await assistant.auto_configure_for_task(
    "process large datasets",
    include_fallbacks=True
)

# If postgres fails, automatically try sqlite
# If github fails, fall back to filesystem
```

### Performance-Aware Selection

Takes setup complexity and reliability into account:

```python
config = await assistant.auto_configure_for_task(
    task,
    prefer_simple_setup=True,  # Prioritize easy-to-setup servers
    max_servers=3             # Limit for performance
)

print(f"Setup complexity: {config.setup_complexity}")  # simple/moderate/complex
print(f"Warnings: {config.warnings}")  # Potential issues
```

### Context Switching for Multi-Task Agents

```python
class AdaptiveAgent:
    async def switch_context(self, new_task: str):
        # Automatically reconfigure for new task type
        new_config = await self.assistant.auto_configure_for_task(new_task)

        # Update capabilities without manual reconfiguration
        self.agent = MCPAgent(engine=self.engine, mcp_config=new_config.config)
        await self.agent.setup()
```

## 🎯 Benefits for AI Development

1. **Reduced Configuration Overhead**: No need to manually research and configure servers
2. **Task-Aware Selection**: Automatically gets the right tools for each job
3. **Intelligent Fallbacks**: Handles failures gracefully with backup options
4. **Performance Optimization**: Considers setup time and complexity
5. **Namespace Organization**: Work with specific server ecosystems
6. **Validation & Testing**: Ensures servers work before using them
7. **Dynamic Adaptation**: Change capabilities as tasks evolve

## 🚀 Getting Started

1. **Install the package**:

   ```bash
   pip install haive-mcp[tools]
   ```

2. **Try the basic demo**:

   ```bash
   python examples/ai_enhanced_coding.py
   ```

3. **Explore with CLI**:

   ```bash
   python -m haive.mcp.cli recommend "your task here" --ai-mode
   ```

4. **Integrate into your agent**:

   ```python
   from haive.mcp.tools import MCPAssistant

   assistant = MCPAssistant()
   config = await assistant.auto_configure_for_task("your task")
   # Use config with your MCPAgent
   ```

## 💡 Pro Tips

- Use `prefer_simple_setup=True` for faster initialization
- Include `include_fallbacks=True` for robust operation
- Test configurations with `MCPServerTester` before production
- Monitor server health in long-running applications
- Use prefix filtering to work with trusted server sources
- Validate configurations to catch issues early

The goal is to make MCP server selection as intelligent and automatic as possible, so AI agents can focus on their core tasks rather than configuration management!



.. raw:: html

    <div class="sphx-glr-thumbnails">

.. thumbnail-parent-div-open

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrates how an AI agent can use the intelligent MCP server selection tools to automatically configure itself for various coding tasks. The agent analyzes tasks and dynamically selects the most appropriate servers.">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_ai_enhanced_coding_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_ai_enhanced_coding.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example: AI-enhanced coding workflow with intelligent MCP server selection.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example shows how the MCPMixin can be used to add MCP support to AugLLMConfig, enabling automatic tool discovery, resource management, and prompt enhancement.">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_aug_llm_mcp_integration_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_aug_llm_mcp_integration.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example demonstrating MCP integration with AugLLMConfig using the MCPMixin.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example shows how to use our MCPDocumentationAgent to automatically discover new MCP servers and other ecosystem resources, then implement agents that can use them.">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_automated_discovery_agent_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_automated_discovery_agent.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Automated Discovery Agent Example</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="A continuous background service that discovers, downloads, processes, and organizes MCP servers with comprehensive documentation, categorization, and quality assessment.">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_background_mcp_processor_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_background_mcp_processor.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Background MCP Server Processing Service</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example shows the simplest way to download and install MCP servers.">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_basic_download_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_basic_download.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Basic example of downloading MCP servers.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Example demonstrating basic MCP agent usage with type-checked integration.">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_basic_mcp_agent_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_basic_mcp_agent.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example demonstrating basic MCP agent usage with type-checked integration.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Example demonstrating basic MCP agent usage with type-checked integration.">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_basic_mcp_agent_fixed_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_basic_mcp_agent_fixed.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example demonstrating basic MCP agent usage with type-checked integration.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrates downloading many servers efficiently and managing them in bulk.">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_batch_operations_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_batch_operations.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example of batch operations with MCP servers.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrates the full MCP integration with haive-agents: 1. Type-checked MCP configuration 2. Resource/prompt/tool transfer between agents 3. Documentation-based setup 4. Dynamic server discovery">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_complete_mcp_integration_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_complete_mcp_integration.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Complete MCP Integration Example</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Discovers MCP servers from all major sources and updates our database. Fixes the issues from the previous demo and implements robust parsing.">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_comprehensive_mcp_discovery_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_comprehensive_mcp_discovery.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Comprehensive MCP Server Discovery System</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example shows how to extend the installer system with custom installation methods.">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_custom_installer_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_custom_installer.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example of creating a custom installer plugin.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example shows how to: 1. Start the dataflow MCP server 2. Connect to it from a client 3. Use the exposed tools to query registry, discover components, and create agents 4. Access resources for registry information">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_dataflow_mcp_example_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_dataflow_mcp_example.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example demonstrating the Haive Dataflow MCP Server.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Processes discovered MCP servers to extract README content and convert to the same format as our original all_mcp_documents.json database.">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_documentation_processing_pipeline_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_documentation_processing_pipeline.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Documentation Processing Pipeline</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Shows both Version 1 (Safe Pattern) and Version 2 (Advanced Code Generation) installers. Both support human approval via interrupt_tool_wrapper.py integration.">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_dual_mcp_installer_demo_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_dual_mcp_installer_demo.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Dual MCP Installer Demo</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrates the MCP (Model Context Protocol) integration with the Dynamic Activation Pattern using real components.">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_dynamic_activation_mcp_example_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_dynamic_activation_mcp_example.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Dynamic Activation MCP Server Example.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Flow: 1. Agent checks what tools are available vs installed 2. Self-query retrieval to find needed tools 3. Dynamic installation if tool missing 4. Hot-reload tools into agent 5. Agent uses new tool automatically">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_dynamic_mcp_agent_system_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_dynamic_mcp_agent_system.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Dynamic MCP Agent System</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example shows how to use the IntelligentMCPAgent to: 1. Automatically discover needed MCP servers based on user requests 2. Get HITL approval for installations 3. Install and configure servers dynamically 4. Use newly available tools without restart">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_dynamic_mcp_workflow_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_dynamic_mcp_workflow.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example demonstrating dynamic MCP server discovery and installation workflow.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This demonstrates the CORRECT way to create MCP tools: 1. Use @tool decorator or StructuredTool.from_function 2. External server management (not inside tool classes) 3. Real MCP protocol communication 4. Proper integration with haive agents">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_final_working_integration_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_final_working_integration.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Final Working MCP Integration - CORRECTED VERSION</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example shows how to: 1. Load MCP server documentation 2. Generate setup instructions 3. Create MCP configurations 4. Build implementation guides">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_mcp_documentation_example_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_mcp_documentation_example.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example demonstrating MCP Documentation Agent for setting up MCP servers.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Automatically installs, sets up, and reads documentation for discovered MCP servers. Creates a complete integration pipeline from discovery to agent configuration.">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_mcp_integration_pipeline_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_mcp_integration_pipeline.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">MCP Integration Pipeline</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrates: 1. Searching for MCP tools by query 2. Creating a haive agent with discovered tool capabilities 3. Using the agent to perform tasks">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_practical_mcp_haive_integration_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_practical_mcp_haive_integration.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Practical MCP + Haive Agent Integration Example</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This script demonstrates how to use the MCPManager to add MCP servers one by one during runtime, as requested: &quot;add all mcps procueduely one by obne&quot;.">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_procedural_mcp_addition_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_procedural_mcp_addition.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Demonstration of procedural MCP server addition.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Process ALL MCP servers immediately in one batch.">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_process_all_now_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_process_all_now.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Process ALL MCP servers immediately in one batch.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This script processes all available MCP servers in one go, generating documentation, quality assessments, and categorization for everything.">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_process_all_servers_now_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_process_all_servers_now.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Process ALL MCP servers immediately without waiting.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Downloads and parses MCP servers from all major sources in standardized format. Keeps track of sources, deduplicates, and maintains data quality.">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_production_mcp_harvester_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_production_mcp_harvester.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Production MCP Server Harvester</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This demonstrates the RIGHT way to create MCP tools: 1. Using @tool decorator 2. Using StructuredTool.from_function 3. Proper state management outside the tool class 4. Real MCP server integration">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_proper_mcp_integration_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_proper_mcp_integration.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Proper MCP Integration - Using correct langchain tool patterns</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Shows how to use existing haive-mcp components to discover and analyze MCP servers and other ecosystem resources.">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_simple_discovery_demo_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_simple_discovery_demo.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Simple Discovery Demo</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example shows how to use the MCPAugLLMConfig class which provides full type checking for MCP configurations while integrating seamlessly with the existing AugLLMConfig functionality.">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_typed_mcp_aug_llm_example_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_typed_mcp_aug_llm_example.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example demonstrating type-safe MCP integration with AugLLMConfig.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Actually install MCP server, run it, and integrate with haive agent using proper Tool structure.">

.. only:: html

  .. image:: /auto_examples/mcp/images/thumb/sphx_glr_working_mcp_haive_integration_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_mcp_working_mcp_haive_integration.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Working MCP + Haive Integration</div>
    </div>


.. thumbnail-parent-div-close

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_examples/mcp/ai_enhanced_coding
   /auto_examples/mcp/aug_llm_mcp_integration
   /auto_examples/mcp/automated_discovery_agent
   /auto_examples/mcp/background_mcp_processor
   /auto_examples/mcp/basic_download
   /auto_examples/mcp/basic_mcp_agent
   /auto_examples/mcp/basic_mcp_agent_fixed
   /auto_examples/mcp/batch_operations
   /auto_examples/mcp/complete_mcp_integration
   /auto_examples/mcp/comprehensive_mcp_discovery
   /auto_examples/mcp/custom_installer
   /auto_examples/mcp/dataflow_mcp_example
   /auto_examples/mcp/documentation_processing_pipeline
   /auto_examples/mcp/dual_mcp_installer_demo
   /auto_examples/mcp/dynamic_activation_mcp_example
   /auto_examples/mcp/dynamic_mcp_agent_system
   /auto_examples/mcp/dynamic_mcp_workflow
   /auto_examples/mcp/final_working_integration
   /auto_examples/mcp/mcp_documentation_example
   /auto_examples/mcp/mcp_integration_pipeline
   /auto_examples/mcp/practical_mcp_haive_integration
   /auto_examples/mcp/procedural_mcp_addition
   /auto_examples/mcp/process_all_now
   /auto_examples/mcp/process_all_servers_now
   /auto_examples/mcp/production_mcp_harvester
   /auto_examples/mcp/proper_mcp_integration
   /auto_examples/mcp/simple_discovery_demo
   /auto_examples/mcp/typed_mcp_aug_llm_example
   /auto_examples/mcp/working_mcp_haive_integration



.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
