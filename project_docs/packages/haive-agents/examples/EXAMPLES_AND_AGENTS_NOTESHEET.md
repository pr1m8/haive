# Haive Examples and Agents Consolidation Notesheet

**Date**: 2025-01-22
**Purpose**: Comprehensive mapping of all examples and agent files across the Haive project
**Status**: Analysis for consolidation and standardization

## 🎯 Executive Summary

### What We Have:

- **50+ embedded examples** within game modules alone
- **Multiple agent architectures** (haive.agents vs haive.core.engine)
- **Inconsistent patterns** across modules
- **Mixed visualization capabilities**
- **Duplicate example patterns**

### Key Opportunities:

- **Standardize visualization** across all agent types
- **Create unified example runner** script
- **Consolidate duplicate patterns**
- **Stream large outputs** consistently

---

## 📁 Embedded Examples Inventory

### 🎮 Haive-Games Module Examples

**Location**: `/packages/haive-games/src/haive/games/*/`

#### Board Games with Examples:

- `battleship/example.py` ✅
- `checkers/example.py` ✅
- `chess/example.py` ✅
- `chess/example_configurable.py` ✅
- `chess/example_configurable_players.py` ✅
- `clue/example.py` ✅
- `connect4/example.py` ✅
- `debate/example.py` ✅
- `debate_v2/example.py` ✅
- `debate_v2/example_with_judges.py` ✅
- `dominoes/example.py` ✅
- `dominoes/enhanced_example.py` ✅
- `fox_and_geese/example.py` ✅
- `fox_and_geese/enhanced_example.py` ✅
- `go/example.py` ✅
- `hold_em/example.py` ✅
- `mafia/example.py` ✅
- `mancala/example.py` ✅
- `mastermind/example.py` ✅
- `monopoly/example.py` ✅
- `nim/example.py` ✅
- `poker/example.py` ✅
- `reversi/example.py` ✅
- `tic_tac_toe/example.py` ✅

#### Card Games:

- `cards/standard/blackjack/` (no example.py) ❌
- `cards/standard/bs/` (no example.py) ❌
- `cards/uno/` (no example.py) ❌

#### Single Player Games:

- `single_player/example.py` ✅
- `single_player/flow_free/example.py` ✅
- `single_player/wordle/example.py` ✅

### 🔧 Other Modules Examples

#### Haive-Core Examples:

**Location**: `/packages/haive-core/examples/`

- `advanced_node_patterns.py`
- `logging_advanced_demo.py`
- `logging_control_demo.py`
- `logging_source_demo.py`
- `logging_where_from_demo.py`
- `meta_agent_example.py` ⭐ **Key**
- `node_composer_examples.py`
- `provider_discovery_demo.py`
- `simple_store_test.py`
- `simple_validation_test.py`
- `state_schema_integration_example.py`
- `state_updating_validation_example.py`
- `store_memory_agent.py`
- `unified_schema_integration.py`

#### Haive-Agents Examples:

**Location**: `/packages/haive-agents/examples/`

- `agent_with_structured_output.py`
- `dynamic_activation_basic_example.py`
- `dynamic_react_agent_example.py`
- `dynamic_supervisor_demo.py`
- `dynamic_supervisor_example.py`
- `enhanced_agent_pattern_demo.py`
- `enhanced_memory_retriever_demo.py`
- `full_supervisor_demo.py`
- `output_adapter_demo.py`
- `plan_and_execute_example.py`
- `structured_output_example.py`
- `token_tracking_example.py`
- `validation_integration_example.py`

#### Haive-MCP Examples:

**Location**: `/packages/haive-mcp/examples/`

- `ai_enhanced_coding.py`
- `aug_llm_mcp_integration.py`
- `automated_discovery_agent.py`
- `background_mcp_processor.py`
- `basic_download.py`
- `basic_mcp_agent.py`
- `basic_mcp_agent_fixed.py`
- `batch_operations.py`
- `complete_mcp_integration.py`
- `comprehensive_mcp_discovery.py`
- `custom_installer.py`
- `dataflow_mcp_example.py`
- `dynamic_activation_mcp_example.py`
- `dynamic_mcp_agent_system.py`
- `dynamic_mcp_workflow.py`
- `final_working_integration.py`
- `mcp_documentation_example.py`
- `practical_mcp_haive_integration.py`
- `real_mcp_server_test.py`
- `simple_discovery_demo.py`
- `working_mcp_haive_integration.py`

#### Haive-Tools Examples:

**Location**: `/packages/haive-tools/examples/`

- `custom_tools_example.py`

---

## 🤖 Agent Architecture Mapping

### Primary Agent Locations:

#### 1. Haive-Agents Architecture (Mixin-based)

**Location**: `/packages/haive-agents/src/haive/agents/`

- `base/agent.py` - **Main Agent Base Class**
- `simple/agent.py` - SimpleAgent
- `react/agent.py` - ReactAgent
- `multi/*/agent.py` - MultiAgent variants
- `rag/*/agent.py` - RAG Agents

#### 2. Haive-Core Architecture (Protocol-based)

**Location**: `/packages/haive-core/src/haive/core/engine/agent/`

- `agent/agent.py` - **Registry-based Agent**
- `config.py` - AgentConfig
- `protocols.py` - Agent Protocols

#### 3. Game-Specific Agents

**Pattern**: `/packages/haive-games/src/haive/games/*/agent.py`

**Complete List**:

- `among_us/agent.py`
- `base/agent.py`
- `base_v2/player_agent.py`
- `battleship/agent.py`
- `cards/standard/blackjack/agent.py`
- `cards/standard/bs/agent.py`
- `checkers/agent.py`
- `chess/agent.py`
- `clue/agent.py`
- `connect4/agent.py`
- `core/agent/generic_player_agent.py`
- `core/agent/player_agent.py`
- `core/players/agent.py`
- `debate/agent.py`
- `debate_v2/agent.py`
- `debate_v2/agent_with_judges.py`
- `dominoes/agent.py`
- `fox_and_geese/agent.py`
- `framework/base/agent.py`
- `framework/core/agent.py`
- `framework/multi_player/agent.py`
- `go/agent.py`
- `hold_em/agent.py`
- `hold_em/game_agent.py`
- `hold_em/player_agent.py`
- `mafia/agent.py`
- `mancala/agent.py`
- `mastermind/agent.py`
- `monopoly/agent.py`
- `monopoly/game_agent.py`
- `monopoly/main_agent.py`
- `monopoly/player_agent.py`
- `multi_player/agent.py`
- `nim/agent.py`
- `poker/agent.py`
- `reversi/agent.py`
- `risk/agent.py`
- `single_player/flow_free/agent.py`
- `single_player/rubiks/agent.py`
- `single_player/wordle/agent.py`
- `tic_tac_toe/agent.py`

---

## 🎨 Visualization Capabilities Analysis

### ✅ Agents with Visualization Methods:

1. **SimpleAgent** - `visualize_graph()` method ✅
2. **ReactAgent** - Inherits visualization ✅
3. **MultiAgent variants** - Should inherit ✅
4. **Game Agents** - Most inherit from base ✅

### 🎯 Visualization Patterns Found:

1. **Graph PNG Generation** - `agent.visualize_graph(path)`
2. **Mermaid Diagrams** - Via LangGraph
3. **Rich Console Output** - Terminal visualization
4. **HTML Reports** - Some debug visualizations

### 📊 Visualization Status by Module:

#### Working Visualizations:

- ✅ **SimpleAgent** - Confirmed working (`simple_agent_workflow_demo.png` generated)
- ✅ **ReactAgent** - Should work (inherits from base)
- ✅ **Game Agents** - Most inherit visualization capability

#### Unknown/Untested:

- ❓ **Core Engine Agents** - Need to verify visualization methods
- ❓ **MCP Agents** - Need to check visualization support
- ❓ **RAG Agents** - Need to verify graph generation

---

## 🔄 Execution Patterns Analysis

### Sync vs Async Usage:

#### Async Examples (Modern Pattern):

- Most game examples use `asyncio.run(main())`
- MCP examples use async patterns
- Modern agent examples use `await agent.arun()`

#### Sync Examples (Legacy Pattern):

- Some older examples use `agent.run()`
- Tool examples often sync
- Simple demonstrations sync

### Streaming Capabilities:

- ❓ **Unknown** - Need to investigate which agents support streaming
- 🎯 **Opportunity** - Create unified streaming example

### Large Output Handling:

- ❌ **Missing** - No standard pattern for handling large outputs
- 🎯 **Opportunity** - Create chunking/pagination system

---

## 🚨 Issues and Duplications

### Duplicate Patterns:

1. **Multiple chess examples** - `example.py`, `example_configurable.py`, `example_configurable_players.py`
2. **Enhanced vs basic** - `dominoes/example.py` vs `dominoes/enhanced_example.py`
3. **Similar game patterns** - Many games follow identical structure
4. **Agent initialization** - Repeated config patterns

### Inconsistencies:

1. **Import patterns** - Mixed import styles across examples
2. **Error handling** - Inconsistent error handling approaches
3. **Visualization calls** - Some use visualization, others don't
4. **Output formatting** - No standard output format

### Broken/Outdated:

- ❌ Some examples may have import errors
- ❌ Version compatibility issues
- ❌ Missing dependencies in some modules

---

## 🎯 Consolidation Opportunities

### 1. **Unified Example Runner Script**

Create a script that can:

- Discover all examples across modules
- Detect agent type automatically
- Visualize any agent regardless of version
- Stream output with chunking for large responses
- Handle both sync and async execution

### 2. **Standard Example Template**

Create a template with:

- Consistent imports
- Standard error handling
- Automatic visualization
- Streaming output handling
- Performance timing

### 3. **Visualization Standardization**

Ensure all agents can:

- Generate PNG workflow diagrams
- Create Mermaid diagrams
- Show rich console output
- Export execution traces

### 4. **Output Streaming System**

Create utilities for:

- Chunked output display
- Real-time streaming
- Large response handling
- Progress indicators

---

## 🛠️ Proposed Unified Script Structure

```python
# unified_example_runner.py
class UniversalAgentRunner:
    def discover_examples()      # Find all example files
    def detect_agent_type()      # Identify agent architecture
    def visualize_agent()        # Generate visualization regardless of type
    def stream_execution()       # Handle streaming output with chunking
    def handle_large_output()    # Manage large responses
    def run_example()           # Execute with proper error handling
```

### Key Features:

- **Auto-discovery** of examples across all modules
- **Version-agnostic** agent handling
- **Streaming output** with intelligent chunking
- **Automatic visualization** generation
- **Performance metrics** and timing
- **Error recovery** and graceful degradation

---

## 📝 Action Items

### Immediate (High Priority):

1. ✅ **Create this notesheet** - DONE
2. 🔄 **Build unified example runner script**
3. 🔄 **Test visualization across agent types**
4. 🔄 **Create streaming output system**

### Short Term:

1. **Audit broken examples** - Fix import/dependency issues
2. **Standardize example templates** - Create consistent patterns
3. **Document visualization methods** - Map all visualization capabilities
4. **Create example consolidation plan** - Merge duplicates

### Long Term:

1. **Build example gallery system** - Interactive example browser
2. **Create benchmark suite** - Performance comparison across agents
3. **Develop visualization dashboard** - Real-time agent monitoring
4. **Build example generation tools** - Auto-create examples for new agents

---

## 🎯 Success Metrics

### Technical Goals:

- ✅ Single script can run any example
- ✅ All agents have working visualization
- ✅ Streaming works for large outputs (>10MB responses)
- ✅ <2 second startup time for any example

### User Experience Goals:

- 🎯 One command to visualize any agent
- 🎯 Real-time streaming for long-running examples
- 🎯 Automatic discovery of new examples
- 🎯 Consistent visual output across all agent types

### Consolidation Goals:

- 📉 Reduce duplicate examples by 50%
- 📈 Increase example consistency by 90%
- 🔧 Standardize all visualization patterns
- 📚 Complete example documentation coverage

---

**Next Steps**: Start building the unified example runner script that can handle agent discovery, visualization, and streaming across all Haive modules.
