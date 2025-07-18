# Centralized Schema Architecture Documentation

**Location**: `/home/will/Projects/haive/backend/haive/project_docs/claude_agent_memory/centralized_schema_architecture/`

## Overview

This centralized folder contains all documentation related to fixing the schema architecture and agent/component confusion in the Haive framework.

## Document Index

### 📁 **Core Architecture Issues**

1. **[AGENT_VS_COMPONENT_ARCHITECTURE.md](./AGENT_VS_COMPONENT_ARCHITECTURE.md)**
   - Fundamental distinction between agents and components
   - Clear definitions and proposed architecture
   - Migration strategy

2. **[SCHEMA_COMPOSITION_BEST_PRACTICES.md](./SCHEMA_COMPOSITION_BEST_PRACTICES.md)**
   - When to use AgentSchemaComposer vs SchemaComposer
   - Anti-patterns to avoid
   - Decision tree for schema composition

3. **[FIXING_AGENT_CONFUSION.md](./FIXING_AGENT_CONFUSION.md)**
   - Concrete implementation fixes
   - Code examples with minimal breaking changes
   - Phase-by-phase migration plan

### 📁 **Technical Analysis**

4. **[layered_architecture_analysis.md](./layered_architecture_analysis.md)**
   - Engine → Node → Schema → Graph → Agent flow
   - Type safety degradation analysis
   - Information loss between layers

5. **[dynamic_schema_architecture.md](./dynamic_schema_architecture.md)**
   - Analysis of dynamic typing issues
   - Feature creep in base classes
   - Optional/Any type problems

6. **[type_weak_aspects.md](./type_weak_aspects.md)**
   - Where type safety breaks down
   - Information discarding patterns
   - Runtime type guessing issues

### 📁 **Schema Composition Analysis**

7. **[complete_schema_analysis.md](./complete_schema_analysis.md)**
   - Analysis of all agent types
   - Schema handling patterns comparison
   - SimpleAgent, ChainAgent, MultiAgent analysis

8. **[multi_vs_chain_analysis.md](./multi_vs_chain_analysis.md)**
   - Detailed comparison of MultiAgent vs ChainAgent
   - Schema handling differences
   - Why ChainAgent has NO schema handling

### 📁 **Enhancement Approaches**

9. **[engine_reference_pattern.md](./engine_reference_pattern.md)**
   - How engine_name references work
   - Type information flow
   - Enhancement strategies

10. **[computed_field_approach.md](./computed_field_approach.md)**
    - Using Pydantic computed fields
    - Zero breaking changes approach
    - State-aware methods

11. **[pydantic_validators_approach.md](./pydantic_validators_approach.md)**
    - Using field_validator and model_validator
    - Dynamic schema generation
    - Type-safe execution

12. **[inherit_engine_schemas.md](./inherit_engine_schemas.md)**
    - Direct schema inheritance from engines
    - Engine type overloading
    - Factory pattern approach

13. **[generic_engine_type_approach.md](./generic_engine_type_approach.md)**
    - Generic EngineNodeConfig approach
    - Type aliases for convenience
    - Single class, multiple types

14. **[runnable_config_approach.md](./runnable_config_approach.md)**
    - Using RunnableConfig for engine parameters
    - Clean separation of concerns
    - LangGraph standard patterns

### 📁 **Historical Approaches**

15. **[compatibility_inheritance_approach.md](./compatibility_inheritance_approach.md)**
    - Compatibility protocols
    - Better inheritance patterns
    - Progressive type enhancement

16. **[backward_compatible_approach.md](./backward_compatible_approach.md)**
    - Non-breaking enhancement strategies
    - Wrapper patterns
    - Detection-based adaptation

17. **[enhance_existing_infrastructure.md](./enhance_existing_infrastructure.md)**
    - Building on existing smart infrastructure
    - Enhancement without rebuilding

## Quick Reference

### **The Core Problem**

- **Type safety lost** between Engine → Node → Schema → Graph → Agent layers
- **Agent vs Component confusion** - everything treated as an agent
- **Schema composition inconsistency** - each agent type handles differently

### **The Gold Standard**

- **MultiAgent with AgentSchemaComposer** - handles schema composition correctly
- **Message preservation** with `preserve_messages_reducer`
- **Field separation strategies** (smart/shared/namespaced)

### **Key Insights**

1. **Not everything is an agent** - agents need reasoning capability (LLM)
2. **Components are different** - retrievers, embeddings don't need agent complexity
3. **Use the right tool** - AgentSchemaComposer for agents, SchemaComposer for components
4. **Don't modify engine schemas** - keep modifications local to agents

### **Implementation Priority**

1. Fix ChainAgent schema handling (add it)
2. Fix SimpleAgent schema modification (stop it)
3. Add ComponentNode for non-agents
4. Standardize on AgentSchemaComposer patterns

## Navigation

- **Start here**: [AGENT_VS_COMPONENT_ARCHITECTURE.md](./AGENT_VS_COMPONENT_ARCHITECTURE.md) for conceptual understanding
- **Best practices**: [SCHEMA_COMPOSITION_BEST_PRACTICES.md](./SCHEMA_COMPOSITION_BEST_PRACTICES.md) for when to use what
- **Implementation**: [FIXING_AGENT_CONFUSION.md](./FIXING_AGENT_CONFUSION.md) for concrete fixes
- **Deep dive**: Browse the technical analysis docs for detailed understanding
