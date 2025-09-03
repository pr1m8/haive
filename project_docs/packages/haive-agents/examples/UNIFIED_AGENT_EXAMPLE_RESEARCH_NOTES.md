# Unified Agent Example Research & Approach Notes

**Date**: 2025-01-22
**Purpose**: Research notes and memory for building a unified agent example runner
**Focus**: Haive-Agents + Haive-Games comprehensive analysis

---

## 🧠 **Memory Notes: What We Discovered**

### **Scale of the Challenge:**

- **100+ agent implementations** across haive-agents alone
- **50+ game-specific agents** in haive-games
- **Multiple architectural patterns** (mixin-based, protocol-based, inheritance)
- **Embedded examples everywhere** - not just in `/examples/` directories
- **Complex dependency chains** between agent types

### **Critical Insight: Examples Are Scattered**

Examples exist in **3 different patterns**:

1. **Standalone `/examples/` directories** - Traditional approach
2. **Embedded `example.py` files** - Within each module/game
3. **`agent.py` files themselves** - Often contain example usage

**This means our unified runner needs to handle ALL THREE patterns.**

---

## 📊 **Haive-Agents Architecture Analysis**

### **Primary Agent Types Found:**

#### **Core Infrastructure:**

- `base/agent.py` - **Main base class** (mixin-based)
- `simple/agent.py` - **Basic conversational agent** ⭐ **Most Important**
- `react/agent.py` - **Reasoning & Action agent** ⭐ **Key for complex tasks**

#### **Specialized Agent Categories:**

1. **Conversation Agents** (5 types):
   - `conversation/base/agent.py` + `example.py`
   - `conversation/collaborative/agent.py` + `example.py`
   - `conversation/debate/agent.py` + `example.py`
   - `conversation/directed/agent.py` + `example.py`
   - `conversation/social_media/agent.py` + `example.py`

2. **RAG Agents** (15+ variants):
   - `rag/base/agent.py` - Base RAG implementation
   - `rag/adaptive/agent.py` - Adaptive retrieval
   - `rag/agentic/agent.py` - Agentic RAG with routing
   - `rag/corrective/agent.py` - Self-correcting RAG
   - `rag/hyde/agent.py` - Hypothetical Document Embeddings
   - `rag/fusion/agent.py` - Multi-query fusion
   - `rag/flare/agent.py` - Forward-looking active retrieval
   - `rag/filtered/agent.py` - Document filtering
   - `rag/multi_agent_rag/` - Multi-agent RAG workflows

3. **Multi-Agent Systems** (10+ implementations):
   - `multi/multi_agent.py` - Basic multi-agent
   - `multi/clean.py` - Clean multi-agent implementation
   - `multi/enhanced_multi_agent_v3.py` - Latest version
   - `supervisor/dynamic_supervisor.py` - Dynamic routing supervisor

4. **Planning Agents** (8+ types):
   - `planning/plan_and_execute/agent.py`
   - `planning/llm_compiler/agent.py`
   - `planning/rewoo/` - ReWOO methodology

5. **Memory Agents** (12+ implementations):
   - `memory/agent.py` - Base memory agent
   - `memory_v2/long_term_memory_agent.py`
   - `memory_v2/graph_memory_agent.py`
   - `long_term_memory/agent.py`

6. **Document Processing** (8+ types):
   - `document_processing/agent.py`
   - `document_loader/base/agent.py`
   - `document_loader/file/agent.py`
   - `document_loader/web/agent.py`
   - `document_modifiers/complex_extraction/agent.py`

7. **Utility Agents**:
   - `reflection/agent.py` - Self-reflection
   - `structured_output/agent.py` - Structured responses
   - `task_analysis/agent.py` - Task decomposition
   - `wiki_writer/agent.py` - Content generation

---

## 🎮 **Haive-Games Integration Points**

### **Key Insight: Games Use Different Base Classes**

- Some inherit from `haive.agents.simple.SimpleAgent`
- Others use `haive.games.base.agent.Agent`
- Some use custom agent architectures entirely

### **Game Agent Patterns:**

1. **Standard Game Agent** - Inherits from base, follows template
2. **Configurable Game Agent** - Uses dynamic configuration
3. **Enhanced Game Agent** - Extended with additional features
4. **Multi-Player Game Agent** - Handles multiple players

---

## 🔍 **Research Questions We Need to Answer**

### **1. Agent Discovery:**

- ❓ How do we automatically detect which agent architecture each uses?
- ❓ What's the inheritance chain for each agent type?
- ❓ How do we handle circular imports between modules?

### **2. Visualization Compatibility:**

- ❓ Which agents have native `visualize_graph()` methods?
- ❓ How do we add visualization to agents that don't support it?
- ❓ Can we create a universal visualization wrapper?

### **3. Execution Patterns:**

- ❓ Which agents are sync vs async?
- ❓ How do we handle different input/output schemas?
- ❓ What's the pattern for streaming large outputs?

### **4. Configuration Complexity:**

- ❓ How do we handle different engine configurations?
- ❓ What's the standard way to pass tools to agents?
- ❓ How do we manage dependencies (vector stores, APIs, etc.)?

---

## 🛠️ **Approach Strategy**

### **Phase 1: Discovery & Cataloging**

**Goal**: Build a comprehensive map of all agents and examples

```python
# Pseudo-approach:
def catalog_all_agents_and_examples():
    discoveries = {
        'agents': scan_for_agent_files(),      # Find all agent.py files
        'examples': scan_for_examples(),       # Find all example files
        'patterns': analyze_inheritance(),     # Map inheritance chains
        'configs': extract_configurations(),   # Document config patterns
    }
```

**Key Tasks:**

- ✅ **Scan file system** - Find all agent.py and example.py files
- 🔄 **Parse imports** - Understand dependency relationships
- 🔄 **Identify base classes** - Map inheritance hierarchies
- 🔄 **Extract example patterns** - Standardize execution approaches

### **Phase 2: Universal Wrapper Creation**

**Goal**: Create adapters that can handle any agent type

```python
class UniversalAgentWrapper:
    def __init__(self, agent_path: str):
        self.agent_type = self._detect_agent_type(agent_path)
        self.visualization_method = self._get_visualization_method()
        self.execution_pattern = self._detect_execution_pattern()

    def run_with_streaming(self, input_data):
        # Handle both sync and async, with chunked output

    def visualize_universal(self, output_path):
        # Work regardless of agent architecture
```

**Key Tasks:**

- 🔄 **Agent type detection** - Automatically classify agent types
- 🔄 **Execution normalization** - Handle sync/async uniformly
- 🔄 **Visualization standardization** - Universal graph generation
- 🔄 **Output streaming** - Chunked display for large responses

### **Phase 3: Example Execution Engine**

**Goal**: Run any example with consistent interface

```python
class UnifiedExampleRunner:
    def discover_all_examples(self) -> List[ExampleInfo]:
        # Find examples across all modules and patterns

    def run_example(self, example_path: str,
                   stream_output: bool = True,
                   generate_visualization: bool = True,
                   max_output_size: int = 10_000_000):
        # Execute with all safety and streaming features
```

---

## 🧪 **Research Tasks Breakdown**

### **Immediate Research Needed:**

#### **1. Agent Architecture Mapping**

```bash
# Commands to run:
find packages/haive-agents/src -name "agent.py" | head -10
# Then analyze inheritance for each found agent
```

#### **2. Example Pattern Analysis**

```bash
# Commands to run:
find packages/haive-agents/src -name "example.py" | wc -l
find packages/haive-games/src -name "example.py" | wc -l
# Then categorize execution patterns
```

#### **3. Visualization Method Survey**

```bash
# Research needed:
grep -r "visualize_graph" packages/haive-agents/src/ | head -5
grep -r "def visualize" packages/haive-agents/src/ | head -5
# Document which methods exist
```

#### **4. Import Dependency Mapping**

```python
# Script needed to analyze:
def analyze_agent_imports(agent_file):
    # Parse imports and map dependencies
    # Identify base classes and mixins
    # Find potential circular imports
```

### **Key Files to Study:**

#### **Most Important Agents (Priority Order):**

1. `haive-agents/src/haive/agents/simple/agent.py` ⭐ **Start here**
2. `haive-agents/src/haive/agents/base/agent.py` ⭐ **Base class**
3. `haive-agents/src/haive/agents/react/agent.py` ⭐ **Complex logic**
4. `haive-agents/src/haive/agents/multi/clean.py` ⭐ **Multi-agent**
5. `haive-games/src/haive/games/tic_tac_toe/agent.py` ⭐ **Game example**

#### **Example Files to Test:**

1. `haive-agents/src/haive/agents/simple/example.py`
2. `haive-agents/src/haive/agents/conversation/base/example.py`
3. `haive-games/src/haive/games/tic_tac_toe/example.py`
4. `haive-games/src/haive/games/chess/example.py`

---

## 💭 **Strategic Decisions Needed**

### **1. Scope Decision:**

**Option A**: Start with just SimpleAgent and ReactAgent (narrow, fast)
**Option B**: Handle all agent types from the start (comprehensive, slow)
**Recommendation**: **Option A** - Prove concept with 2-3 agents first

### **2. Visualization Strategy:**

**Option A**: Require all agents to support `visualize_graph()`
**Option B**: Create external visualization wrapper
**Option C**: Generate visualizations from execution traces
**Recommendation**: **Option B** - Most flexible

### **3. Output Streaming Approach:**

**Option A**: Real-time streaming with progress bars
**Option B**: Chunked output with "More..." prompts
**Option C**: Smart truncation with full output saved to file
**Recommendation**: **Option C** - Best user experience

### **4. Example Discovery Method:**

**Option A**: Static file scanning (fast, might miss dynamic examples)
**Option B**: Dynamic import and inspection (slow, comprehensive)
**Option C**: Hybrid approach with caching
**Recommendation**: **Option C** - Best of both worlds

---

## 🎯 **Next Actions Plan**

### **Research Session 1: Agent Architecture Analysis**

**Time**: 30-45 minutes
**Goal**: Understand inheritance patterns and dependencies

1. **Read base agent classes**:
   - `haive.agents.base.agent`
   - `haive.core.engine.agent`
   - `haive.games.base.agent`

2. **Map inheritance chains** for top 5 agent types

3. **Document configuration patterns** - how do they take engines/tools?

### **Research Session 2: Example Pattern Analysis**

**Time**: 20-30 minutes
**Goal**: Understand how examples are structured

1. **Run 3 examples manually** to understand patterns:
   - SimpleAgent example
   - Game example (tic-tac-toe)
   - RAG example

2. **Document execution patterns**:
   - Sync vs async
   - Input/output formats
   - Error handling approaches

### **Research Session 3: Visualization Survey**

**Time**: 20-30 minutes
**Goal**: Map visualization capabilities

1. **Test visualization** on working agents
2. **Identify gaps** - which agents lack visualization
3. **Plan universal wrapper** approach

---

## 📋 **Research Checklist**

### **Core Questions to Answer:**

- [ ] **What are the 5 most important agent types?**
- [ ] **How many total examples exist across all modules?**
- [ ] **What's the standard pattern for agent initialization?**
- [ ] **Which agents support visualization out of the box?**
- [ ] **What's the pattern for handling large outputs?**
- [ ] **How do we detect agent type from file path/content?**
- [ ] **What are the common failure modes when running examples?**

### **Technical Validation:**

- [ ] **Can we import all agent types successfully?**
- [ ] **Do all agent examples actually run?**
- [ ] **What's the performance baseline for different agents?**
- [ ] **How do we handle missing dependencies gracefully?**

---

## 🚀 **Success Criteria**

### **Research Phase Success:**

- ✅ **Complete mapping** of all agent types and examples
- ✅ **Working prototype** that can run SimpleAgent + 1 game agent
- ✅ **Visualization working** for at least 2 agent types
- ✅ **Streaming output** handling for responses >1MB

### **Implementation Phase Success:**

- 🎯 **Single command** to run any agent example
- 🎯 **Universal visualization** for all agent types
- 🎯 **Smart output handling** for massive responses
- 🎯 **Automatic discovery** of new examples as they're added

---

**Next Step**: Start with Research Session 1 - analyze the core agent architectures to understand inheritance patterns and build our foundation.
