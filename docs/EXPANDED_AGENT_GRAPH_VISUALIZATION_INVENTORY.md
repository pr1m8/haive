# 🎯 EXPANDED Agent Graph Visualization Inventory - Complete Collection

**Generated**: 2025-07-28  
**Status**: Complete discovery across docs/scripts and root directories  
**Scope**: ALL agent graph visualization tools in the Haive project

## 🚀 **NEW DISCOVERIES in docs/scripts/**

### 1. **Agent Demo Generation** (`docs/scripts/agent_demos/generate_agent_demos.py`)
**Purpose**: Generate interactive demo pages for all Haive agents  
**Features**:
- **Mock Graph Data Generation** - Creates realistic graph visualizations for different agent types
- **Agent Categories** - Supports simple, react, rag, planning, conversation, research, document_modifiers, reasoning_and_critique
- **Execution Trace Simulation** - Generates realistic execution traces with timing data
- **State History Visualization** - Creates mock state transitions for documentation

**Agent Types Supported**:
```python
AGENT_CATEGORIES = {
    "simple": {"icon": "🤖", "color": "#4589ff"},
    "react": {"icon": "🧠", "color": "#8a3ffc"}, 
    "rag": {"icon": "📚", "color": "#24a148"},
    "planning": {"icon": "📋", "color": "#ff832b"},
    "conversation": {"icon": "💬", "color": "#f1c21b"},
    "research": {"icon": "🔬", "color": "#0f62fe"},
    "document_modifiers": {"icon": "📄", "color": "#da1e28"},
    "reasoning_and_critique": {"icon": "🎯", "color": "#6929c4"}
}
```

**Graph Generation Examples**:
```python
# ReactAgent graph structure
nodes = [
    {"id": "reason", "type": "agent", "label": "Reasoning"},
    {"id": "act", "type": "tool", "label": "Action"}, 
    {"id": "observe", "type": "validation", "label": "Observe"}
]
edges = [
    {"source": "reason", "target": "act", "type": "conditional"},
    {"source": "act", "target": "observe"},
    {"source": "observe", "target": "reason"}
]
```

### 2. **Agent Cache Generation** (`docs/scripts/cache_generation/generate_agent_cache.py`)
**Purpose**: Generate cached agent execution data for documentation demos  
**Features**:
- **Real Agent Execution** - Runs actual SimpleAgent and ReactAgent instances
- **Comprehensive Data Capture** - Streaming events, state history, graph data, visualization data
- **Graph Structure Extraction** - Attempts to extract real graph nodes/edges from agents
- **Tool Call Tracking** - Captures tool usage and reasoning steps

**Key Capabilities**:
```python
# Tries to extract actual graph visualization
if hasattr(agent, 'get_graph'):
    graph = agent.get_graph()
    graph_info = {
        "nodes": list(graph.nodes.keys()),
        "edges": list(graph.edges),
        "mermaid_available": hasattr(graph, 'draw_mermaid_png')
    }

# Captures visualization methods from agents
if hasattr(agent, 'get_visualization_data'):
    viz_data['visualization_data'] = agent.get_visualization_data()
if hasattr(agent, 'get_graph_visualization'): 
    viz_data['graph_visualization'] = agent.get_graph_visualization()
```

### 3. **Games AutoDoc Extension** (`docs/scripts/extensions_dev/_extensions/games_autodoc.py`)
**Purpose**: Enhanced documentation generation for game environments  
**Features**:
- **Game Categorization** - Automatic categorization into board games, card games, single player, etc.
- **Quality Assessment** - Evaluates game completeness and documentation quality
- **Component Scanning** - Detects agent.py, config.py, state.py, models.py, ui.py files
- **Visual Game Grid** - Creates interactive game galleries with quality indicators

**Categories**:
```python
CATEGORIES = {
    "board_games": {"icon": "♟️", "description": "Classic board games with strategic depth"},
    "card_games": {"icon": "🃏", "description": "Traditional and modern card games"},
    "social_deduction": {"icon": "🎭", "description": "Games involving deception and social reasoning"},
    "strategy_games": {"icon": "🏰", "description": "Complex strategic and tactical games"}
}
```

### 4. **Agent Documentation Extension** (`docs/scripts/extensions_dev/_extensions/agent_docs.py`)  
**Purpose**: Sphinx extension for automatic agent documentation with examples and visualization  
**Features**:
- **Agent Metadata Registry** - Comprehensive metadata for major agent types
- **Visualization Integration** - Built-in visualization code generation
- **Example Code Generation** - Automatic usage examples and configuration
- **Graph Type Detection** - Identifies simple, cyclic, dag, multi_agent graph types

**Visualization Support**:
```python
AGENT_METADATA = {
    "SimpleAgent": {
        "visualization": {
            "supports_graph": True,
            "graph_type": "simple", 
            "state_schema": "MessageState"
        }
    },
    "ReactAgent": {
        "visualization": {
            "supports_graph": True,
            "graph_type": "cyclic",
            "includes_tools": True,
            "state_schema": "ReactState"
        }
    }
}
```

**Generated Visualization Code**:
```python
# Auto-generated visualization examples
agent.visualize_graph("agent_graph.png")
agent.visualize_graph("agent_graph.html", format="html")
```

## 📋 **COMPLETE Visualization Tools Inventory**

### **Root Level Scripts**
1. **`debug_agent_node_v3.py`** - Debugs AgentNodeV3 execution and state handling

### **Core Visualization Classes** 
1. **`packages/haive-core/src/haive/core/graph/state_graph/graph_visualizer.py`** - Advanced GraphVisualizer with Agent detection  
2. **`packages/haive-core/src/haive/core/graph/utils/mermaid_visualizer.py`** - Interactive MermaidVisualizer
3. **`packages/haive-core/src/haive/core/utils/visualize_graph_utils.py`** - Basic graph rendering utilities

### **Main CLI Tool**
1. **`packages/haive-core/tests/examples/visualize_agent_example.py`** - Comprehensive CLI visualization tool

### **Documentation Scripts** (docs/scripts/)
1. **`agent_demos/generate_agent_demos.py`** - Interactive demo page generation
2. **`cache_generation/generate_agent_cache.py`** - Real execution data capture  
3. **`extensions_dev/_extensions/agent_docs.py`** - Sphinx agent documentation extension
4. **`extensions_dev/_extensions/games_autodoc.py`** - Games documentation and visualization

## 🎨 **Visualization Formats Supported**

### **Graph Formats**
- **Mermaid Diagrams** - Interactive HTML with zoom/pan
- **PNG Images** - High-quality static images via mermaid.ink
- **SVG Diagrams** - Vector graphics for documentation
- **JSON Data** - Graph structure for programmatic use

### **Documentation Formats**  
- **Interactive HTML Pages** - Full demo pages with execution traces
- **Sphinx RST** - Auto-generated documentation with examples
- **Agent Galleries** - Visual grid layouts with filtering
- **Game Documentation** - Specialized game environment docs

### **Data Capture Formats**
- **Execution Traces** - Step-by-step agent execution logs
- **State History** - State transitions over time
- **Tool Call Logs** - Tool usage and reasoning traces  
- **Performance Metrics** - Timing and resource usage

## 🔧 **Usage Patterns by Purpose**

### **For Agent Development**
```bash
# Visualize specific agent during development
python packages/haive-core/tests/examples/visualize_agent_example.py agents_simple

# Debug agent execution
python debug_agent_node_v3.py

# Generate real execution data 
python docs/scripts/cache_generation/generate_agent_cache.py simple
```

### **For Documentation Generation**
```bash
# Generate interactive demo pages
python docs/scripts/agent_demos/generate_agent_demos.py

# Build agent docs with visualization
sphinx-build -b html docs/source docs/build -E
```

### **For Research & Analysis**
```python
# Programmatic graph analysis
from haive.core.graph.state_graph.graph_visualizer import GraphVisualizer
GraphVisualizer.debug_graph_structure(agent.get_graph())

# Capture live execution data
from docs.scripts.cache_generation.generate_agent_cache import run_simple_agent_with_streaming
execution_data = await run_simple_agent_with_streaming("Test query")
```

## 🎯 **Specialized Tools for Different Contexts**

### **Agent Graph Visualization** (haive.core.engine.agent, haive.agents.base.agent)
- **GraphVisualizer.generate_mermaid()** - Professional graph diagrams with agent detection
- **MermaidVisualizer.render_to_file()** - Interactive HTML with controls
- **Agent cache generation** - Real execution traces and state history

### **Game Environment Visualization**
- **games_autodoc.py** - Game categorization and component analysis  
- **Quality assessment** - Excellent, good, basic, minimal ratings
- **Interactive game grids** - Visual browsing with filters

### **Multi-Agent System Visualization**  
- **Mock conversation flows** - DebateConversation visualization
- **Agent coordination** - Turn management and state sharing
- **Cross-agent data flow** - Tool calls and reasoning chains

## 💡 **Key Insights from Discovery**

### **1. Rich Ecosystem of Visualization Tools**
The project has a comprehensive visualization ecosystem spanning:
- Core graph rendering (GraphVisualizer, MermaidVisualizer)
- Real execution capture (cache generation)
- Documentation automation (Sphinx extensions)  
- Interactive demos (agent demos)
- Game environment analysis (games autodoc)

### **2. Multiple Approaches to Agent Visualization**
- **Static Mock Data** - generate_agent_demos.py creates realistic demo graphs
- **Real Execution Data** - generate_agent_cache.py captures actual agent runs
- **Live Graph Analysis** - GraphVisualizer detects and expands agent nodes
- **Documentation Integration** - agent_docs.py embeds visualization in docs

### **3. Comprehensive Agent Type Support**
All major agent categories are supported:
- SimpleAgent, ReactAgent, BaseRAGAgent
- Planning agents, conversation agents  
- Research agents, document modifiers
- Multi-agent systems and coordination

The visualization system is mature, comprehensive, and production-ready! 🚀

## 🔗 **Sphinx Integration & conf.py Configuration**

### **Extensions to Add to conf.py**
```python
# Add these paths to sys.path in conf.py
import sys
from pathlib import Path

# Add docs scripts to Python path for Sphinx extensions
docs_scripts_path = Path(__file__).parent / "scripts"
sys.path.insert(0, str(docs_scripts_path))
sys.path.insert(0, str(docs_scripts_path / "extensions_dev" / "_extensions"))

# Extensions list
extensions = [
    # Existing extensions...
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'autoapi.extension',
    
    # NEW: Agent visualization extensions
    'agent_docs',           # From docs/scripts/extensions_dev/_extensions/
    'games_autodoc',        # From docs/scripts/extensions_dev/_extensions/
    'haive_sphinx_ext',     # From docs/scripts/extensions_dev/_extensions/
    
    # Enable exec directive for running agent demos
    'sphinx_exec_directive',  # Already installed but needs config
    
    # Enable gallery for agent examples  
    'sphinx_gallery.gen_gallery',  # Already installed but needs config
]
```

### **Required Dependencies (Already Installed!)**
From our analysis, these are **already available** in pyproject.toml:
```toml
# ✅ Already installed and ready
sphinx-exec-directive = "^0.6"       # Execute Python code in docs
sphinx-gallery = "^0.14.0"           # Generate example galleries  
sphinx-autodoc-typehints = "^1.25.2" # Type hints in docs
myst-nb = "^1.0.0"                   # Jupyter notebook support
sphinx-codeautolink = "^0.15.0"      # Auto-link code references
```

### **Configuration for Agent Visualization**

#### **sphinx_exec_directive config:**
```python
# In conf.py - Execute agent demos in docs
exec_directive_timeout = 120
exec_directive_output_location = "after"
exec_directive_hide_code = False

# Allow importing agent visualization modules
exec_directive_imports = [
    'import sys',
    'sys.path.append("../../docs/scripts")',
    'sys.path.append("../../docs/scripts/extensions_dev/_extensions")',
    'from agent_demos.generate_agent_demos import *',
    'from cache_generation.generate_agent_cache import *'
]
```

#### **sphinx_gallery config:**
```python
# Generate galleries from agent examples
sphinx_gallery_conf = {
    'examples_dirs': [
        '../../packages/haive-core/tests/examples',
        '../../packages/haive-games/src/haive/games',  # Game examples
        '../../examples'  # Root examples
    ],
    'gallery_dirs': [
        'auto_examples',      # Generated examples
        'auto_games',         # Generated game examples  
        'auto_agents'         # Generated agent examples
    ],
    'filename_pattern': '/example',
    'plot_gallery': True,
    'download_all_examples': False,
    'show_memory': True,
    'show_signature': False
}
```

### **Agent Documentation Directives**
Once configured, you can use these in RST files:

```rst
.. agent-doc:: SimpleAgent
   :show-example: true
   :show-visualization: true
   :show-config: true

.. agent-gallery:: simple

.. games-autodoc:: 
   :category: board_games

.. exec::
   :context: close-figs
   
   # Generate real agent visualization
   from docs.scripts.cache_generation.generate_agent_cache import run_simple_agent_with_streaming
   import asyncio
   
   result = asyncio.run(run_simple_agent_with_streaming("Hello!"))
   print(f"Agent executed in {result['execution_summary']['duration_seconds']:.2f}s")
```

### **File Paths for conf.py Integration**

#### **Extension Paths:**
```python
# Add to sys.path in conf.py
extension_paths = [
    "docs/scripts/extensions_dev/_extensions/agent_docs.py",
    "docs/scripts/extensions_dev/_extensions/games_autodoc.py", 
    "docs/scripts/extensions_dev/_extensions/haive_sphinx_ext.py",
    "docs/scripts/extensions_dev/_extensions/namespace_autosummary.py",
    "docs/scripts/extensions_dev/_extensions/safe_autosummary.py"
]
```

#### **Example Source Paths:**
```python
# For sphinx_gallery
example_source_paths = [
    "packages/haive-core/tests/examples/",
    "packages/haive-games/src/haive/games/*/example.py", 
    "packages/haive-agents/examples/",
    "packages/haive-tools/examples/",
    "examples/"
]
```

#### **Visualization Output Paths:**
```python
# Where to put generated visualizations
visualization_output_paths = {
    'agent_graphs': 'docs/build/html/_static/agent_graphs/',
    'game_screenshots': 'docs/build/html/_static/game_screenshots/', 
    'execution_traces': 'docs/build/html/_static/execution_traces/',
    'interactive_demos': 'docs/build/html/_static/interactive_demos/'
}
```

### **Complete conf.py Integration Script**
```python
# Complete integration for conf.py
import sys
from pathlib import Path

# === ADD PATHS ===
project_root = Path(__file__).parent.parent
docs_scripts = project_root / "docs" / "scripts"
extensions_dir = docs_scripts / "extensions_dev" / "_extensions"

# Add to Python path
sys.path.insert(0, str(docs_scripts))
sys.path.insert(0, str(extensions_dir))

# === EXTENSIONS ===
extensions = [
    # Existing...
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'autoapi.extension',
    
    # NEW: Agent visualization
    'agent_docs',
    'games_autodoc', 
    'haive_sphinx_ext',
    
    # Already installed - need config
    'sphinx_exec_directive',
    'sphinx_gallery.gen_gallery',
    'sphinx_codeautolink',
    'myst_nb'
]

# === CONFIGURATIONS ===
# Agent documentation
agent_docs_config = {
    'show_visualization': True,
    'generate_examples': True,
    'include_execution_traces': True
}

# Executable code in docs
exec_directive_timeout = 120
exec_directive_imports = [
    'import sys',
    f'sys.path.append("{docs_scripts}")',
    'from agent_demos.generate_agent_demos import *',
    'from cache_generation.generate_agent_cache import *'
]

# Example galleries
sphinx_gallery_conf = {
    'examples_dirs': [
        str(project_root / "packages" / "haive-core" / "tests" / "examples"),
        str(project_root / "packages" / "haive-games" / "src" / "haive" / "games"),
        str(project_root / "examples")
    ],
    'gallery_dirs': ['auto_examples', 'auto_games', 'auto_agents'],
    'filename_pattern': '/example',
    'plot_gallery': True
}

# Code auto-linking for visualization functions
codeautolink_global_preface = """
from haive.core.graph.state_graph.graph_visualizer import GraphVisualizer
from haive.core.graph.utils.mermaid_visualizer import MermaidVisualizer
from docs.scripts.agent_demos.generate_agent_demos import *
from docs.scripts.cache_generation.generate_agent_cache import *
"""
```

### **Next Steps for Integration**
1. **Update docs/source/conf.py** with the paths and extensions above
2. **Test extension loading**: `sphinx-build -b html docs/source docs/build/html`
3. **Add agent documentation pages** using the new directives
4. **Configure sphinx_gallery** to generate agent example galleries
5. **Enable sphinx_exec_directive** for live agent execution in docs

The visualization tools are ready - they just need to be **connected to Sphinx** through conf.py! 🚀