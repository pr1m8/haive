# Agent Graph Visualization Inventory for Haive

## 🎯 Found Visualization Tools and Scripts

### 1. **Main Visualization Script** (⭐ COMPLETE)
**Location**: `packages/haive-core/tests/examples/visualize_agent_example.py`

**Features**:
- **Example Discovery**: Automatically finds all `example.py` files across packages
- **Agent Detection**: Analyzes AST to find agent creations and graph methods
- **Multi-format Output**: Generates HTML, PNG, Mermaid, and debug JSON
- **CLI Interface**: Command-line tool for running and visualizing examples

**Usage**:
```bash
cd packages/haive-core/tests/examples/
python visualize_agent_example.py --help
python visualize_agent_example.py --list                    # List all examples
python visualize_agent_example.py --discover react          # Find react examples  
python visualize_agent_example.py agents_simple             # Visualize specific example
python visualize_agent_example.py --category agents         # Filter by category
```

**Output Structure**:
```
./graph_visualizations/
├── agents_simple/
│   ├── agents_simple_create_agent_graph_visualizer.html
│   ├── agents_simple_create_agent_graph_visualizer.mmd
│   ├── agents_simple_create_agent_mermaid_visualizer.html
│   ├── agents_simple_create_agent_basic.png
│   └── agents_simple_create_agent_debug_info.json
```

### 2. **Core Visualization Classes**

#### **GraphVisualizer** (⭐ ADVANCED)
**Location**: `packages/haive-core/src/haive/core/graph/state_graph/graph_visualizer.py`

**Key Features**:
- **Agent Detection**: Automatically detects nodes with Agent engines
- **Recursive Expansion**: Shows internal structure of nested agents
- **Professional Styling**: Consistent color scheme and node types
- **Smart Edge Routing**: Handles complex agent hierarchies
- **Debug Information**: Comprehensive graph structure analysis

**Usage**:
```python
from haive.core.graph.state_graph.graph_visualizer import GraphVisualizer

# Generate Mermaid code
mermaid_code = GraphVisualizer.generate_mermaid(
    graph, 
    include_subgraphs=True, 
    theme="base", 
    direction="TB",
    debug=True
)

# Display graph with multiple outputs
GraphVisualizer.display_graph(
    graph,
    output_path="agent_graph.html",
    include_subgraphs=True,
    save_png=True,
    title="My Agent Graph",
    debug=True
)

# Debug graph structure
debug_info = GraphVisualizer.debug_graph_structure(graph)
```

#### **MermaidVisualizer** (⭐ INTERACTIVE)
**Location**: `packages/haive-core/src/haive/core/graph/utils/mermaid_visualizer.py`

**Features**:
- **Interactive Diagrams**: Rich web-based visualization
- **Multiple Output Formats**: HTML, PNG, SVG
- **Custom Styling**: Professional themes and colors
- **Legend Support**: Automatic legend generation
- **Browser Integration**: Opens results automatically

**Usage**:
```python
from haive.core.graph.utils.mermaid_visualizer import MermaidVisualizer

visualizer = MermaidVisualizer(graph)
visualizer.render_to_file(
    output_file="agent_graph.html",
    open_browser=True,
    include_legend=True
)
```

### 3. **Utility Functions**

#### **Basic Graph Rendering**
**Location**: `packages/haive-core/src/haive/core/utils/visualize_graph_utils.py`

**Function**: `render_and_display_graph(compiled_graph, output_dir, output_name)`
- Simple PNG generation using LangGraph's built-in Mermaid renderer
- Lightweight option for basic visualization needs

#### **Mermaid Utilities**
**Location**: `packages/haive-core/src/haive/core/utils/mermaid_utils.py`
- `display_mermaid()` function for inline Mermaid rendering
- HTML template generation for Mermaid diagrams

### 4. **Debug and Development Scripts**

#### **Debug Agent Node V3** (Root)
**Location**: `debug_agent_node_v3.py`
- Debugs AgentNodeV3 execution and state handling
- Tests dict/StateSchema compatibility
- Direct agent graph inspection

#### **Visualization Examples** (haive-core)
**Location**: `packages/haive-core/temp_refactor/state_graph/visualization/examples.py`
- Example scripts for different visualization scenarios
- Demonstrates various agent graph patterns

### 5. **Documentation Scripts**

#### **Agent Documentation** (Extensions)
**Location**: `docs/scripts/extensions_dev/_extensions/agent_docs.py`
- Generates documentation for agent classes
- Potentially includes graph visualization in docs

#### **Comprehensive Documentation Scripts**
**Found in**: `docs/scripts/` (20+ scripts)
- Documentation building and enhancement
- API documentation generation
- Screenshot and visualization automation

## 🚀 Usage Patterns for Different Scenarios

### **Scenario 1: Quick Agent Graph Visualization**
```bash
# For a single agent
python packages/haive-core/tests/examples/visualize_agent_example.py agents_simple

# For all agents
python packages/haive-core/tests/examples/visualize_agent_example.py --category agents
```

### **Scenario 2: Programmatic Visualization**
```python
from haive.core.graph.state_graph.graph_visualizer import GraphVisualizer
from haive.agents.simple.agent import SimpleAgent

# Create agent
agent = SimpleAgent(name="test", engine=config)
graph = agent.build_graph()

# Visualize
GraphVisualizer.display_graph(
    graph,
    output_path="my_agent.html",
    save_png=True,
    title="My Agent Visualization"
)
```

### **Scenario 3: Embedded in Documentation**
```python
# For Sphinx docs with sphinx_exec_directive
from haive.core.graph.state_graph.graph_visualizer import GraphVisualizer

mermaid_code = GraphVisualizer.generate_mermaid(graph)
print(f"```mermaid\n{mermaid_code}\n```")
```

### **Scenario 4: Batch Visualization of All Examples**
```bash
cd packages/haive-core/tests/examples/

# Discover and visualize all agent examples
python visualize_agent_example.py --category agents --output-dir ./all_visualizations

# Discover and visualize all game examples  
python visualize_agent_example.py --category games --output-dir ./game_visualizations
```

## 🎨 Visualization Features

### **Node Types and Styling**
The GraphVisualizer supports professional styling for:
- **Engine Nodes**: Blue (#3B82F6) - Core agent engines
- **Tool Nodes**: Red (#EF4444) - Tool integrations
- **Validation Nodes**: Green (#10B981) - Validation steps
- **Agent Nodes**: Purple - Nested agents
- **Start/End Nodes**: Special styling for graph boundaries

### **Output Formats**
1. **HTML**: Interactive web-based visualization
2. **PNG**: High-quality static images
3. **Mermaid**: Text-based diagram code
4. **JSON**: Debug information and structure data

### **Advanced Features**
- **Subgraph Detection**: Automatically groups related nodes
- **Agent Expansion**: Shows internal structure of agent nodes
- **Smart Labeling**: Meaningful node names and descriptions
- **Error Handling**: Graceful handling of complex graphs
- **Debug Mode**: Comprehensive analysis output

## 📁 File Organization

```
haive/
├── debug_agent_node_v3.py                    # Root debug script
├── packages/haive-core/
│   ├── src/haive/core/
│   │   ├── graph/state_graph/
│   │   │   └── graph_visualizer.py           # Main visualizer class
│   │   ├── graph/utils/
│   │   │   └── mermaid_visualizer.py         # Mermaid-specific visualizer
│   │   └── utils/
│   │       ├── visualize_graph_utils.py      # Utility functions
│   │       └── mermaid_utils.py              # Mermaid utilities
│   ├── tests/examples/
│   │   └── visualize_agent_example.py        # ⭐ Main CLI tool
│   └── temp_refactor/state_graph/visualization/
│       ├── mermaid_generator.py              # Mermaid generation
│       └── examples.py                       # Visualization examples
└── docs/scripts/
    └── extensions_dev/_extensions/
        └── agent_docs.py                     # Agent documentation
```

## 🎯 Recommended Workflow

1. **Discovery**: Use `visualize_agent_example.py --list` to see all available examples
2. **Quick Test**: Run `visualize_agent_example.py agents_simple` for basic validation
3. **Batch Generation**: Use category filters to generate all visualizations
4. **Custom Integration**: Use GraphVisualizer class for programmatic access
5. **Documentation**: Embed Mermaid code in docs using generated output

## 💡 Enhancement Opportunities

1. **Sphinx Integration**: Add custom directive for automatic graph embedding
2. **Live Updates**: Real-time graph updates during agent execution
3. **Comparison Views**: Side-by-side visualization of different agent versions
4. **Performance Metrics**: Overlay execution timing on graph nodes
5. **Interactive Debugging**: Click nodes to inspect state and execution details

The Haive project has a comprehensive and sophisticated graph visualization system that's ready for immediate use!