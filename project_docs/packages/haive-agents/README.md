# Haive-Agents Package Documentation

**Version**: 1.0
**Last Updated**: 2025-01-23
**Status**: Newly Organized

This directory contains comprehensive documentation for the haive-agents package, which provides pre-built agent implementations for the Haive framework.

## 📋 Recent Organization (January 2025)

The haive-agents documentation has been reorganized from scattered files throughout the project into a logical structure:

- **✅ Documentation Consolidation**: ~20 agent-related files moved from various project_docs locations
- **✅ Logical Structure**: Organized by function (guides, implementation, patterns, examples, etc.)
- **✅ Clear Navigation**: Easy to find relevant documentation for specific agent types
- **✅ Cross-References**: Links to related core framework and tool documentation

## 🏗️ Directory Structure

```
packages/haive-agents/
├── README.md                    # This file - main navigation
├── guides/                      # User guides and tutorials
│   ├── enhanced_multi_agent_v3_complete_guide.md
│   ├── enhanced_multi_agent_v3_quick_reference.md
│   ├── simple_rag_complete.md
│   ├── simple_rag_guide.md
│   ├── multi_agent_workflows.md
│   └── agent_guide.md
├── implementation/              # Implementation details and status
│   ├── AGENT_MODULE_STATUS.md
│   ├── SIMPLERAG_V3_IMPLEMENTATION_SUMMARY.md
│   ├── SimpleRAG_V3_Implementation_Summary.md
│   ├── PLAN_AND_EXECUTE_V2_DOCUMENTATION.md
│   ├── SUPERVISOR_CLEANUP_MIGRATION_PLAN.md
│   ├── SUPERVISOR_IMPLEMENTATIONS_ANALYSIS.md
│   └── THREE_AGENT_INACTIVE_TEST_ANALYSIS.md
├── patterns/                    # Design patterns and fixes
│   ├── comprehensive_agent_patterns_analysis.md
│   ├── AGENT_NODE_COMMAND_PATTERN_FIX.md
│   ├── AGENT_NODE_INPUT_EXTRACTION_FIX.md
│   └── agent_fixes/
├── examples/                    # Examples and research notes
│   ├── EXAMPLES_AND_AGENTS_NOTESHEET.md
│   ├── COMPREHENSIVE_RAG_PROMPT_EXAMPLE.md
│   └── UNIFIED_AGENT_EXAMPLE_RESEARCH_NOTES.md
├── architecture/                # Architecture design and analysis
│   ├── AGENT_ARCHITECTURE_REDESIGN.md
│   ├── ENHANCED_MEMORY_AGENT_ARCHITECTURE.md
│   ├── ENHANCED_MEMORY_AGENT_ARCHITECTURE_PHASE2.md
│   ├── AGENT_ARCHITECTURE_ANALYSIS.md
│   ├── AGENT_NODE_TYPED_IO_PATTERN.md
│   ├── AGENT_OUTPUT_FIELD_STRATEGY.md
│   └── BASERAG_OUTPUT_SCHEMA_ANALYSIS.md
├── testing/                     # Testing issues and troubleshooting
│   └── MULTIAGENT_EXECUTION_ISSUES_NOTESHEET.md
├── analysis/                    # Analysis and evaluation
│   └── agent_analysis/
└── haive_agents_overview/       # Package overview
    ├── README.md
    ├── AGENT_ARCHITECTURE.md
    ├── DOCUMENT_AGENTS.md
    ├── IMPLEMENTATION_GUIDE.md
    └── RAG_AGENTS.md
```

## 🎯 Agent Types Overview

### Core Agent Categories

#### 1. **Simple Agents**

Basic conversational agents with memory and context management.

**Key Files:**

- `guides/agent_guide.md` - Basic agent usage
- `implementation/SIMPLERAG_V3_IMPLEMENTATION_SUMMARY.md` - Simple RAG implementation

**Package Location:** `packages/haive-agents/src/haive/agents/simple/`

#### 2. **React Agents**

Reasoning and action agents that can use tools and make decisions.

**Key Files:**

- `guides/enhanced_multi_agent_v3_complete_guide.md` - React agent integration
- `patterns/AGENT_NODE_COMMAND_PATTERN_FIX.md` - Command patterns

**Package Location:** `packages/haive-agents/src/haive/agents/react/`

#### 3. **Multi-Agent Systems**

Coordination and orchestration of multiple agents working together.

**Key Files:**

- `guides/multi_agent_workflows.md` - Multi-agent coordination
- `guides/enhanced_multi_agent_v3_complete_guide.md` - Comprehensive guide
- `implementation/SUPERVISOR_IMPLEMENTATIONS_ANALYSIS.md` - Supervisor patterns

**Package Location:** `packages/haive-agents/src/haive/agents/multi/`

#### 4. **RAG Agents**

Retrieval-augmented generation for document processing and knowledge systems.

**Key Files:**

- `guides/simple_rag_complete.md` - Complete RAG guide
- `guides/simple_rag_guide.md` - Basic RAG usage
- `examples/COMPREHENSIVE_RAG_PROMPT_EXAMPLE.md` - Prompt examples
- `haive_agents_overview/RAG_AGENTS.md` - RAG architecture

**Package Location:** `packages/haive-agents/src/haive/agents/rag/`

#### 5. **Planning Agents**

Task planning and execution agents (Plan & Execute pattern).

**Key Files:**

- `implementation/PLAN_AND_EXECUTE_V2_DOCUMENTATION.md` - P&E implementation

**Package Location:** `packages/haive-agents/src/haive/agents/planning/`

#### 6. **Specialized Agents**

- **Research Agents**: Web search and information gathering
- **Memory Agents**: Long-term memory and context management
- **Conversation Agents**: Specialized conversational patterns

## 🚀 Quick Start Navigation

### For New Users

1. **[Package Overview](haive_agents_overview/README.md)** - Start here for a complete overview
2. **[Agent Guide](guides/agent_guide.md)** - Basic agent usage patterns
3. **[Implementation Guide](haive_agents_overview/IMPLEMENTATION_GUIDE.md)** - How to implement agents

### For Developers

1. **[Agent Architecture](haive_agents_overview/AGENT_ARCHITECTURE.md)** - Core architecture concepts
2. **[Architecture Analysis](architecture/AGENT_ARCHITECTURE_ANALYSIS.md)** - Detailed architecture
3. **[Pattern Analysis](patterns/comprehensive_agent_patterns_analysis.md)** - Design patterns

### For Multi-Agent Systems

1. **[Multi-Agent Workflows](guides/multi_agent_workflows.md)** - Basic workflows
2. **[Enhanced Multi-Agent Guide](guides/enhanced_multi_agent_v3_complete_guide.md)** - Complete guide
3. **[Supervisor Analysis](implementation/SUPERVISOR_IMPLEMENTATIONS_ANALYSIS.md)** - Supervision patterns

### For RAG Implementation

1. **[Simple RAG Guide](guides/simple_rag_guide.md)** - Getting started
2. **[Complete RAG Guide](guides/simple_rag_complete.md)** - Advanced implementation
3. **[RAG Agents Overview](haive_agents_overview/RAG_AGENTS.md)** - Architecture details

## 🔗 Cross-Package Integration

### Core Framework Links

- **Engine Configuration**: See [haive-core engine documentation](../haive-core/README.md)
- **State Management**: See [active architecture docs](../../active/architecture/README.md)
- **Memory System**: See [memory index](../../memory_index/README.md)

### Tool Integration

- **Tool Development**: See [haive-tools documentation](../haive-tools/README.md)
- **Dynamic Tools**: See [dynamic tool routing system](../../dynamic_tool_routing_system/README.md)

### Testing and Development

- **Testing Philosophy**: See [active standards](../../active/standards/testing/philosophy.md)
- **Development Workflow**: See [coding standards](../../active/standards/coding/README.md)

## 🧪 Testing and Validation

### Key Testing Principles

- **No Mocks**: All tests use real LLM components (see testing/philosophy.md)
- **Real Integration**: Tests validate actual agent behavior
- **Comprehensive Coverage**: Tests cover all major agent patterns

### Test Locations

- **Package Tests**: `packages/haive-agents/tests/`
- **Integration Tests**: `packages/haive-agents/tests/integration/`
- **Example Tests**: `packages/haive-agents/tests/examples/`

### Common Issues

- **[Execution Issues](testing/MULTIAGENT_EXECUTION_ISSUES_NOTESHEET.md)** - Multi-agent troubleshooting
- **[Inactive Tests](implementation/THREE_AGENT_INACTIVE_TEST_ANALYSIS.md)** - Test analysis

## 📊 Development Status

### ✅ Mature Components

- SimpleAgent: Stable, well-documented
- ReactAgent: Feature-complete with tool integration
- RAG Agents: Multiple implementations available
- Multi-Agent: Basic coordination working

### 🔄 Active Development

- Enhanced multi-agent patterns (v3)
- Dynamic supervisor systems
- Advanced memory integration
- Performance optimizations

### 📋 Planned Improvements

- Better documentation organization (this effort!)
- Enhanced testing coverage
- Performance benchmarking
- Advanced pattern documentation

## 🆘 Getting Help

### Documentation Issues

- Check [troubleshooting guide](testing/MULTIAGENT_EXECUTION_ISSUES_NOTESHEET.md)
- Review [common patterns](patterns/comprehensive_agent_patterns_analysis.md)
- See [implementation guides](implementation/README.md)

### Development Support

- **Memory References**: Use `@memory_index/by_agent/` for agent-specific memories
- **Active Issues**: See [current issues](../../sessions/active/current_issues.md)
- **Architecture Questions**: Review [architecture documentation](architecture/README.md)

### Contributing

- Follow [development standards](../../active/standards/README.md)
- Use [real component testing](../../active/standards/testing/philosophy.md)
- Reference [coding patterns](../../active/standards/coding/README.md)

---

**Note**: This documentation structure is newly organized (January 2025) to provide better navigation and clearer organization of haive-agents related information. For the most current code examples, always refer to the package source code and test suite.
