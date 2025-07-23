# Haive Documentation Utilities

A comprehensive toolkit for analyzing, running, visualizing, and documenting all Haive agents across the entire ecosystem.

## 🎯 Overview

This system provides unified tools to:

- **Analyze** any agent type, regardless of architecture
- **Run** any example with streaming output and error handling
- **Visualize** agent workflows with automatic diagram generation
- **Document** agents and examples with comprehensive reports

## 🚀 Quick Start

### Command Line Usage

```bash
# Analyze all agents and generate report
python doc_utils_runner.py analyze --report --output analysis_report.md

# Discover and run all examples
python doc_utils_runner.py run --discover
python doc_utils_runner.py run --run-all --visualize

# Create agent visualizations
python doc_utils_runner.py visualize --compare --format html
python doc_utils_runner.py visualize --agent-name SimpleAgent --format png

# Generate comprehensive documentation
python doc_utils_runner.py docs --api-docs --output ./documentation
```

### Programmatic Usage

```python
import asyncio
from scripts.doc_utils import AgentAnalyzer, UniversalExampleRunner, VisualizationManager

# Analyze agents
analyzer = AgentAnalyzer()
agents = analyzer.discover_all_agents()
print(f"Found {len(agents)} agents")

# Run examples
async def run_examples():
    runner = UniversalExampleRunner()
    examples = await runner.discover_all_examples()

    # Run a specific example
    result = await runner.run_example(examples[0])
    print(f"Success: {result.success}, Time: {result.execution_time:.2f}s")

asyncio.run(run_examples())

# Generate visualizations
async def create_viz():
    viz_manager = VisualizationManager()
    result = await viz_manager.visualize_agent(agents[0], Path("agent_viz.png"))
    print(f"Visualization: {result.output_path}")

asyncio.run(create_viz())
```

## 📋 Core Components

### 1. AgentAnalyzer

Comprehensive agent discovery and analysis:

- **Auto-detects** all agent types across packages
- **Analyzes inheritance** patterns and capabilities
- **Identifies architecture** (haive.agents, haive.core, haive.games)
- **Maps relationships** between agents

```python
analyzer = AgentAnalyzer()
agents = analyzer.discover_all_agents()

# Get specific agent
simple_agent = analyzer.get_agent_by_name("SimpleAgent")
print(f"Architecture: {simple_agent.architecture}")
print(f"Has visualization: {simple_agent.has_visualization}")

# Generate analysis report
report = analyzer.generate_analysis_report()
```

### 2. UniversalExampleRunner

Execute any example with advanced features:

- **Universal compatibility** - handles any agent type
- **Streaming output** with intelligent chunking
- **Large response handling** - automatically saves to file
- **Timeout protection** and error recovery
- **Async/sync detection** and appropriate execution

```python
runner = UniversalExampleRunner()

# Configure execution
config = ExecutionConfig(
    max_output_size=10_000_000,  # 10MB limit
    stream_output=True,
    enable_visualization=True,
    timeout_seconds=300
)

# Run example
result = await runner.run_example("path/to/example.py", config)

if result.success:
    print(f"Execution completed in {result.execution_time:.2f}s")
    if result.output_file:
        print(f"Large output saved to: {result.output_file}")
```

### 3. VisualizationManager

Universal visualization for all agent types:

- **Native visualization** when available
- **Synthetic diagrams** for agents without visualization
- **Multiple formats** - PNG, SVG, HTML, Mermaid
- **Comparison views** across multiple agents
- **Theme support** - default, dark, minimal

```python
viz_manager = VisualizationManager()

# Create visualization
config = VisualizationConfig(
    output_format="html",
    theme="dark",
    include_metadata=True
)

result = await viz_manager.visualize_agent(agent_info, output_path, config)

# Create comparison visualization
agents = analyzer.discover_all_agents()
await viz_manager.create_comparison_visualization(
    agents, Path("comparison.html"), config
)
```

### 4. DocumentationGenerator

Automated documentation creation:

- **Comprehensive docs** for individual agents
- **Project-wide** documentation with cross-references
- **Multiple formats** - Markdown, reStructuredText, HTML
- **API documentation** extraction from code
- **Example integration** with code snippets

```python
doc_generator = DocumentationGenerator()

# Generate docs for specific agent
config = DocumentationConfig(
    include_examples=True,
    include_visualizations=True,
    include_api_docs=True,
    output_format="markdown"
)

result = await doc_generator.generate_agent_documentation(
    agent_info, output_dir, config
)

# Generate project-wide docs
await doc_generator.generate_project_documentation(output_dir, config)
```

## 🔧 Configuration Options

### ExecutionConfig

```python
ExecutionConfig(
    max_output_size=10_000_000,    # Maximum output size in bytes
    chunk_size=1024,               # Streaming chunk size
    enable_visualization=True,      # Generate visualizations
    timeout_seconds=300,           # Execution timeout
    stream_output=True,            # Enable streaming
    save_full_output=True          # Save large outputs to file
)
```

### VisualizationConfig

```python
VisualizationConfig(
    output_format="png",           # png, svg, html, mermaid
    theme="default",               # default, dark, minimal
    include_metadata=True,         # Include agent metadata
    width=800,                     # Image width
    height=600,                    # Image height
    dpi=300                        # Image DPI
)
```

### DocumentationConfig

```python
DocumentationConfig(
    include_examples=True,         # Include example files
    include_visualizations=True,   # Generate diagrams
    include_code_snippets=True,    # Add code examples
    include_api_docs=True,         # Extract API docs
    output_format="markdown",      # markdown, rst, html
    template_style="comprehensive" # minimal, standard, comprehensive
)
```

## 📊 Supported Agent Types

The system automatically handles all Haive agent architectures:

### Haive.Agents (Mixin-based)

- SimpleAgent, ReactAgent, MultiAgent
- RAG agents, Memory agents, Planning agents
- Conversation agents, Document processing agents

### Haive.Core.Engine (Protocol-based)

- Registry-based agents
- Configurable execution patterns

### Haive.Games (Game-specific)

- All game agents: Chess, Tic-tac-toe, Battleship, etc.
- Player agents and game managers
- Multi-player game coordination

## 🎯 Key Features

### Intelligent Agent Detection

- **Automatic discovery** of all agent files
- **Architecture classification** based on imports and inheritance
- **Capability detection** (visualization, tools, streaming)
- **Relationship mapping** between related agents

### Universal Example Execution

- **Handles any execution pattern** (sync/async/both)
- **Smart output management** with streaming and file saving
- **Error recovery** and graceful degradation
- **Performance monitoring** and timing

### Flexible Visualization

- **Works with any agent type** regardless of native support
- **Multiple output formats** for different use cases
- **Comparison views** to analyze multiple agents
- **Customizable themes** and styling

### Comprehensive Documentation

- **Auto-generated** from code analysis
- **Cross-referenced** with related agents
- **Example integration** with runnable code
- **Multiple output formats** for different audiences

## 📝 Examples

### Analyze Project Architecture

```bash
# Get comprehensive analysis
python doc_utils_runner.py analyze --report --output architecture_analysis.md

# Check specific agent
python doc_utils_runner.py analyze --agent-name ReactAgent
```

### Run Examples with Monitoring

```bash
# Discover all examples
python doc_utils_runner.py run --discover

# Run all with visualization and streaming
python doc_utils_runner.py run --run-all --visualize --output execution_report.md

# Run specific example with custom config
python doc_utils_runner.py run --example-path packages/haive-games/src/haive/games/chess/example.py --max-output-size 50000000
```

### Create Visual Documentation

```bash
# Generate comparison view
python doc_utils_runner.py visualize --compare --format html --theme dark

# Create individual visualizations
python doc_utils_runner.py visualize --format png --output ./visualizations/

# Specific agent with custom theme
python doc_utils_runner.py visualize --agent-name SimpleAgent --format svg --theme minimal
```

### Generate Complete Documentation

```bash
# Comprehensive project docs
python doc_utils_runner.py docs --api-docs --output ./complete_documentation

# Specific agent with all features
python doc_utils_runner.py docs --agent-name ReactAgent --api-docs --format html

# Minimal documentation
python doc_utils_runner.py docs --style minimal --no-visualizations --output ./minimal_docs
```

## 🚀 Performance Notes

- **Concurrent execution** for multiple examples (configurable)
- **Streaming output** prevents memory issues with large responses
- **Intelligent caching** for repeated operations
- **Timeout protection** prevents hanging on problematic examples
- **Graceful degradation** when dependencies are missing

## 🔍 Troubleshooting

### Common Issues

**Import Errors**: Ensure you're running from the project root with proper Python path

```bash
cd /home/will/Projects/haive/backend/haive
python doc_utils_runner.py analyze
```

**Missing Dependencies**: Some visualizations require optional packages

```bash
pip install graphviz matplotlib  # For advanced visualizations
```

**Large Output**: System automatically handles large responses by saving to files

- Look for `[OUTPUT TOO LARGE - Saved to: filename.txt]` messages

**Timeout Issues**: Increase timeout for slow examples

```bash
python doc_utils_runner.py run --timeout 600  # 10 minutes
```

This system provides the foundation for comprehensive documentation and analysis of the entire Haive agent ecosystem. All components work together to create a unified, maintainable documentation workflow.
