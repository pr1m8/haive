# Architecture Design Documentation

This folder contains design documentation for architectural improvements to the Haive framework.

## Organization

### `/component_hierarchy/`

Design documents for the Component-Agent hierarchy and type system:

- Component as high-level base class
- Agent as LLM reasoning specialization
- Specialized component types (Retriever, Processor, etc.)
- Migration strategies and backward compatibility

### `/schema_composition/`

Design documents for schema composition improvements:

- Schema composition consistency across agent types
- AgentSchemaComposer vs SchemaComposer usage patterns
- Message preservation and tool_call_id handling
- NodeConfig-Schema integration

### `/agent_fixes/`

Specific fixes for identified agent issues:

- ChainAgent schema composition fix
- SimpleAgent engine modification issues
- MultiAgent workflow standardization
- Hook system integration

## Context

These designs address the critical consistency and coherency issues identified in the framework analysis. The goal is to provide a clear architectural foundation that:

1. **Maintains backward compatibility** - existing code continues to work
2. **Provides clear upgrade paths** - gradual migration to better patterns
3. **Fixes critical issues** - tool_call_id loss, schema composition problems
4. **Enables future growth** - consistent patterns for new components

## Design Principles

- **Additive, not disruptive** - new patterns alongside existing ones
- **Gradual evolution** - optional migration, not forced breaking changes
- **Clear separation of concerns** - Component vs Agent, reasoning vs processing
- **Consistent interfaces** - unified patterns across all component types
