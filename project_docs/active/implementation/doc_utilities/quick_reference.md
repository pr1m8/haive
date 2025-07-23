# Documentation Utilities - Quick Reference

**Date**: 2025-01-22  
**Status**: Ready for Use  
**Location**: `/scripts/doc_utils/`

## 🚀 Quick Commands

### Nox Commands (Recommended)

```bash
# Complete workflow - generates everything
nox -s doc_utils_full

# Individual components
nox -s doc_utils_analyze      # Agent analysis report
nox -s doc_utils_examples     # Example validation
nox -s doc_utils_visualize    # Generate visualizations
nox -s doc_utils_generate     # Create documentation
```

### Direct CLI Commands

```bash
# Agent analysis
python scripts/doc_utils_runner.py analyze --report --output analysis.md

# Example discovery and validation
python scripts/doc_utils_runner.py run --discover
python scripts/doc_utils_runner.py run --run-all --timeout 60

# Visualization generation
python scripts/doc_utils_runner.py visualize --compare --format html
python scripts/doc_utils_runner.py visualize --agent-name SimpleAgent --format png

# Documentation generation
python scripts/doc_utils_runner.py docs --format markdown --api-docs
```

## 📁 Output Locations

After running `nox -s doc_utils_full`:

```
docs/build/
├── agent_analysis/agent_analysis_report.md    # 📊 Agent analysis
├── examples/example_validation_report.md      # 🧪 Example validation
├── visualizations/agent_comparison.html       # 🎨 Visual comparison
├── generated_docs/index.md                   # 📚 Generated documentation
└── doc_utils_summary.md                      # 📋 Summary index
```

## 🎯 Common Use Cases

### Daily Development

```bash
# Check if your new agent is discovered
nox -s doc_utils_analyze

# Validate examples after changes
nox -s doc_utils_examples

# Quick visualization check
python scripts/doc_utils_runner.py visualize --agent-name YourAgent
```

### Documentation Updates

```bash
# Full documentation refresh for releases
nox -s doc_utils_full

# Update specific agent documentation
python scripts/doc_utils_runner.py docs --agent-name SimpleAgent --style comprehensive
```

### Debugging & Analysis

```bash
# Find all agents of specific type
python scripts/doc_utils_runner.py analyze --report | grep "haive.agents"

# Test specific example
python scripts/doc_utils_runner.py run --example-path path/to/example.py --visualize

# Generate comparison visualization
python scripts/doc_utils_runner.py visualize --compare --theme dark
```

## 🔧 Configuration Examples

### ExecutionConfig (Python API)

```python
from scripts.doc_utils import ExecutionConfig

config = ExecutionConfig(
    max_output_size=50_000_000,    # 50MB limit
    stream_output=True,            # Enable streaming
    timeout_seconds=120,           # 2 minute timeout
    enable_visualization=True       # Generate visualizations
)
```

### CLI Parameters

```bash
# Customize timeouts
python scripts/doc_utils_runner.py run --timeout 300 --max-output-size 100000000

# Visualization options
python scripts/doc_utils_runner.py visualize --format svg --theme dark --width 1200

# Documentation formats
python scripts/doc_utils_runner.py docs --format html --style minimal --no-examples
```

## 📊 What Gets Analyzed

### Agent Types Discovered

- **haive.agents**: SimpleAgent, ReactAgent, RAG agents, Memory agents, etc.
- **haive.core**: Protocol-based agents, Engine configurations
- **haive.games**: Chess, Go, Poker, all board game agents

### Capabilities Detected

- **Visualization**: Native `visualize_graph()` method support
- **Tools**: Tool integration and usage patterns
- **Streaming**: Async execution and streaming capabilities
- **Architecture**: Inheritance patterns and base classes

### Example Patterns Found

- **Standalone examples**: In `/examples/` directories
- **Embedded examples**: `example.py` files within modules
- **Agent files**: Often contain usage examples in docstrings

## 🎨 Visualization Formats

| Format      | Use Case                     | Features                        |
| ----------- | ---------------------------- | ------------------------------- |
| **PNG**     | Documentation, presentations | High quality, widely supported  |
| **SVG**     | Web documentation            | Scalable, lightweight           |
| **HTML**    | Interactive viewing          | Metadata, responsive, themeable |
| **Mermaid** | Diagram-as-code              | Version controllable, editable  |

## 🧪 Programmatic Usage

### Quick Agent Discovery

```python
from scripts.doc_utils import AgentAnalyzer

analyzer = AgentAnalyzer()
agents = analyzer.discover_all_agents()
print(f"Found {len(agents)} agents")

# Find specific agent
simple_agent = analyzer.get_agent_by_name("SimpleAgent")
print(f"Architecture: {simple_agent.architecture}")
```

### Example Execution

```python
import asyncio
from scripts.doc_utils import UniversalExampleRunner

async def run_example():
    runner = UniversalExampleRunner()
    examples = await runner.discover_all_examples()

    result = await runner.run_example(examples[0])
    print(f"Success: {result.success}, Time: {result.execution_time:.2f}s")

asyncio.run(run_example())
```

### Visualization Generation

```python
import asyncio
from scripts.doc_utils import VisualizationManager, VisualizationConfig

async def create_viz():
    viz_manager = VisualizationManager()
    analyzer = AgentAnalyzer()
    agents = analyzer.discover_all_agents()

    config = VisualizationConfig(output_format="html", theme="dark")
    result = await viz_manager.create_comparison_visualization(
        agents, Path("comparison.html"), config
    )
    print(f"Comparison created: {result.output_path}")

asyncio.run(create_viz())
```

## ⚡ Performance Tips

### Fast Analysis

```bash
# Quick analysis without full validation
nox -s doc_utils_analyze  # ~30 seconds

# Skip slow examples during validation
python scripts/doc_utils_runner.py run --timeout 30 --max-concurrent 5
```

### Efficient Visualization

```bash
# HTML is fastest for comparison
python scripts/doc_utils_runner.py visualize --compare --format html

# PNG generation may require additional dependencies
pip install matplotlib graphviz
```

### Documentation Generation

```bash
# Minimal docs for speed
python scripts/doc_utils_runner.py docs --style minimal --no-visualizations

# Full docs with everything
python scripts/doc_utils_runner.py docs --style comprehensive --api-docs
```

## 🔍 Troubleshooting

### Common Issues

**Import Errors**:

```bash
# Ensure proper environment
cd /path/to/haive/backend/haive
poetry run python scripts/doc_utils_runner.py analyze
```

**Missing Dependencies**:

```bash
# Install optional visualization libraries
pip install graphviz matplotlib
```

**Large Output**:

```bash
# System automatically saves large outputs
# Look for: [OUTPUT TOO LARGE - Saved to: filename.txt]
```

**Timeout Issues**:

```bash
# Increase timeout for slow examples
python scripts/doc_utils_runner.py run --timeout 600
```

### Debug Commands

```bash
# Check what agents are discovered
python scripts/doc_utils_runner.py analyze --agent-name SimpleAgent

# Validate specific example
python scripts/doc_utils_runner.py run --example-path packages/haive-agents/examples/simple_agent_example.py

# Test visualization capabilities
python scripts/doc_utils_runner.py visualize --agent-name SimpleAgent --format html
```

## 📚 Related Documentation

- **[Implementation Guide](README.md)** - Complete implementation details
- **[UNIFIED_AGENT_EXAMPLE_RESEARCH_NOTES.md](../../../UNIFIED_AGENT_EXAMPLE_RESEARCH_NOTES.md)** - Original research
- **[EXAMPLES_AND_AGENTS_NOTESHEET.md](../../../EXAMPLES_AND_AGENTS_NOTESHEET.md)** - Example catalog
- **[noxfile.py](../../../../noxfile.py)** - Build system integration

## 🎯 Next Steps

1. **Try the quick commands** above to familiarize yourself
2. **Run `nox -s doc_utils_full`** to generate complete documentation
3. **Check the output** in `docs/build/` directory
4. **Integrate into your workflow** for regular documentation updates

This system provides the **unified approach** we planned for handling all Haive agent types with consistent visualization and streaming capabilities!

## 🎮 **Game & Agent Visualization Testing - 2025-01-23**

### **Current Status: READY FOR LIVE TESTING**

**System Validation Results**:
- ✅ **403 Agents Discovered** (haive.agents: 281, haive.games: 82, haive.core: 10)
- ✅ **264+ Examples Found** across all packages and patterns  
- ✅ **Streaming System Working** with 10MB+ output handling
- ✅ **Universal Visualization** supports all architectures
- ✅ **Build System Integrated** with Sphinx documentation

### **Game Agent Testing Commands**

```bash
# Discover all game agents
poetry run python -c "
from pathlib import Path
from scripts.doc_utils.agent_analyzer import AgentAnalyzer
analyzer = AgentAnalyzer(Path('.'))
games = [a for a in analyzer.discover_all_agents() if 'games' in str(a.file_path)]
print(f'🎮 Found {len(games)} game agents:')
for game in games[:10]:
    print(f'  • {game.name} ({game.architecture.value})')
"

# Test game visualization
poetry run python scripts/doc_utils_runner.py visualize --agent-name ChessAgent --format html --theme dark

# Run game examples with visualization
poetry run python scripts/doc_utils_runner.py run --example-path packages/haive-games/examples/ --visualize --timeout 180
```

### **Multi-Agent Visualization Testing**

```bash
# Compare multiple agents visually
poetry run python scripts/doc_utils_runner.py visualize --compare --format html --output agents_comparison.html

# Test agent workflow visualization
poetry run python -c "
from scripts.doc_utils import AgentAnalyzer, VisualizationManager
import asyncio
from pathlib import Path

async def test_multi_viz():
    analyzer = AgentAnalyzer(Path('.'))
    agents = analyzer.discover_all_agents()
    
    # Get diverse agent sample
    sample = []
    for arch in ['haive.agents', 'haive.games', 'haive.core']:
        arch_agents = [a for a in agents if arch in a.architecture.value]
        if arch_agents:
            sample.append(arch_agents[0])
    
    print(f'🎯 Testing visualization with {len(sample)} diverse agents')
    for agent in sample:
        print(f'  • {agent.name} ({agent.architecture.value})')

asyncio.run(test_multi_viz())
"
```

### **Documentation Audit Commands**

```bash
# Full system health check
poetry run python -c "
from pathlib import Path
from scripts.doc_utils.agent_analyzer import AgentAnalyzer
analyzer = AgentAnalyzer(Path('.'))
agents = analyzer.discover_all_agents()

print('📊 SYSTEM AUDIT RESULTS:')
print(f'  🔍 Total Agents: {len(agents)}')

# Group by architecture  
arch_counts = {}
for agent in agents:
    arch = agent.architecture.value
    arch_counts[arch] = arch_counts.get(arch, 0) + 1

for arch, count in sorted(arch_counts.items()):
    print(f'  📦 {arch}: {count} agents')
"

# Test streaming capabilities
poetry run python scripts/doc_utils_runner.py run --example-path examples/complex_multi_agent_workflows.py --stream --max-output-size 50000000
```

### **Next Testing Phase**

**Ready to Execute**:
1. 🎮 **Game Agent Visualization**: Test Chess, Go, Poker agent visualizations
2. 🔄 **Multi-Agent Workflows**: Test sequential and parallel agent patterns  
3. 📊 **Streaming Validation**: Test large output handling with game simulations
4. 🎨 **Theme Testing**: Validate dark/light themes with game visualizations
5. 📈 **Performance Testing**: Benchmark visualization generation times

**Post-Testing**: Complete systematic syntax fixes across all packages with trunk
