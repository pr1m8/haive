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
