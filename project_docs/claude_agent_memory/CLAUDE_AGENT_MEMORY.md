# CLAUDE_AGENT_MEMORY.md - Agent & Schema Memory System

**Version**: 1.0
**Purpose**: Centralized memory system for Claude to track, understand, and solve agent/schema-related issues
**Date**: 2025-01-06
**Memory Tag**: [MEM-100]

## 🧠 Memory Architecture Overview

This memory system helps Claude (me) better understand and solve issues in the Haive agent framework, with special focus on:

- Agent implementations and patterns
- Schema composition and state management
- Tool routing and validation
- Cross-package dependencies
- Common issue patterns and solutions

## 📁 Memory Structure

```
project_docs/claude_agent_memory/
├── CLAUDE_AGENT_MEMORY.md (This file) [MEM-100]
├── schema_analysis/ [MEM-101]
│   ├── 01_STATE_SCHEMA_PATTERNS.md [MEM-101-A]
│   ├── 02_SCHEMA_COMPOSER_ANALYSIS.md [MEM-101-B]
│   ├── 03_TOOL_ROUTING_PATTERNS.md [MEM-101-C]
│   └── 04_VALIDATION_SCHEMAS.md [MEM-101-D]
├── agent_patterns/ [MEM-102]
│   ├── 01_BASE_AGENT_ARCHITECTURE.md [MEM-102-A]
│   ├── 02_SIMPLE_AGENT_PATTERNS.md [MEM-102-B]
│   ├── 03_REACT_AGENT_PATTERNS.md [MEM-102-C]
│   └── 04_CUSTOM_AGENT_TEMPLATES.md [MEM-102-D]
├── implementation_tracking/ [MEM-103]
│   ├── 01_CURRENT_ISSUES.md [MEM-103-A]
│   ├── 02_SOLVED_PATTERNS.md [MEM-103-B]
│   ├── 03_PERFORMANCE_NOTES.md [MEM-103-C]
│   └── 04_INTEGRATION_GOTCHAS.md [MEM-103-D]
├── cross_references/ [MEM-104]
│   ├── 01_ENGINE_TO_SCHEMA_MAPPING.md [MEM-104-A]
│   ├── 02_TOOL_REGISTRY_MAP.md [MEM-104-B]
│   ├── 03_MIXIN_DEPENDENCIES.md [MEM-104-C]
│   └── 04_PACKAGE_BOUNDARIES.md [MEM-104-D]
└── issue_resolution/ [MEM-105]
    ├── 01_COMMON_ERRORS.md [MEM-105-A]
    ├── 02_DEBUGGING_PATTERNS.md [MEM-105-B]
    ├── 03_FIX_TEMPLATES.md [MEM-105-C]
    └── 04_TEST_STRATEGIES.md [MEM-105-D]
```

## 🎯 Core Focus Areas

### 1. Schema System Understanding [MEM-101]

- **StateSchema**: Base class for all agent states
- **SchemaComposer**: Dynamic schema generation from engines
- **AgentSchemaComposer**: Multi-agent schema composition
- **Tool routing**: How tools are assigned to engines

### 2. Agent Architecture [MEM-102]

- **Base Agent**: Abstract foundation with mixins
- **SimpleAgent**: Streamlined single-engine agent
- **ReactAgent**: Reasoning and acting agent
- **Custom patterns**: Templates for new agents

### 3. Common Issues & Solutions [MEM-105]

- Schema generation failures
- Tool routing errors
- Engine registration problems
- State persistence issues

## 🔗 Quick Navigation

### Essential References

- **Main Haive Docs**: [CLAUDE.md](../../CLAUDE.md) [MEM-002-A]
- **Memory Methodology**: [CLAUDE_MEMORY_METHODOLOGY.md](../CLAUDE_MEMORY_METHODOLOGY.md) [MEM-002-B]
- **Quick Reference**: [CLAUDE_QUICKREF.md](../claude_documentation/CLAUDE_QUICKREF.md) [MEM-005-B]

### Package Documentation

- **haive-core schema**: `/packages/haive-core/src/haive/core/schema/`
- **haive-agents**: `/packages/haive-agents/src/haive/agents/`
- **Agent tests**: `/packages/haive-agents/tests/`

## 📊 Key Insights & Patterns

### Schema Generation Pattern

```python
# Agents auto-generate schemas from engines
agent = SimpleAgent(engine=aug_llm_engine)
# This triggers:
# 1. setup_agent() - field syncing
# 2. _setup_schemas() - schema generation
# 3. _build_initial_graph() - graph construction
```

### Tool Routing Pattern

```python
# Tools are routed based on type
tool_routes = {
    calculator: "pydantic_model",     # Pydantic BaseModel tools
    web_search: "langchain_tool",     # LangChain BaseTool
    custom_fn: "function"             # Regular functions
}
```

### Engine Registration Pattern

```python
# Engines must be registered for nodes to find them
from haive.core.engine.base import EngineRegistry
registry = EngineRegistry.get_instance()
registry.register(engine)
```

## 🚀 Common Tasks

### Creating a New Agent

1. Extend `Agent` base class
2. Implement `setup_agent()` for initialization
3. Implement `build_graph()` for workflow
4. Use mixins for execution/persistence

### Adding Tool Support

1. Define tools in engine configuration
2. Set up tool routing in state schema
3. Add tool nodes to graph
4. Configure validation routing

### Debugging Schema Issues

1. Check engine output fields
2. Verify schema composer logic
3. Validate field compatibility
4. Review inheritance chain

## 📈 Memory Maintenance

### Update Triggers

- New agent implementation
- Schema system changes
- Tool routing updates
- Issue resolution patterns

### Cross-Reference Updates

- When adding new patterns
- After solving complex issues
- On discovering dependencies
- During refactoring

## 🎓 Key Learnings

1. **Schema Composition**: Schemas are dynamically built from engine capabilities
2. **Tool Routing**: Tools are assigned to engines based on type/route
3. **Graph Building**: Agents define workflow through BaseGraph
4. **Mixin Architecture**: Functionality separated into focused mixins
5. **State Management**: StateSchema provides unified state interface

---

**Next Steps**: Populate subdirectories with detailed analysis and patterns
**Last Updated**: 2025-01-06
**Memory Status**: Active and growing
