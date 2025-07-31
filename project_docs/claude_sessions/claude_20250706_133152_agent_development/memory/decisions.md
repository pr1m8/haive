# Design Decisions

## Decision: Simplify Base Agent Architecture

**Date**: 2025-01-06
**Context**: Base agent is overly complex with multiple mixins and 1500+ lines
**Rationale**:

- Multiple inheritance causes MRO issues
- Hard to debug and understand
- Over-engineered for most use cases
  **Trade-offs**:
- May lose some functionality initially
- Need to ensure backward compatibility
  **Alternative**: Keep complex structure (rejected - too maintainability issues)
  **Solution**: Refactor to use composition over inheritance where possible

## Decision: Centralize Tool Management

**Date**: 2025-01-06
**Context**: Tool handling spread across agents, state schemas, and graph nodes
**Rationale**:

- Current system is fragmented and hard to follow
- Tool routing logic duplicated in multiple places
- Difficult to add new tool types
  **Trade-offs**:
- Breaking changes to existing tool usage
- Need migration strategy
  **Alternative**: Keep distributed tool system (rejected - too fragmented)
  **Solution**: Create unified ToolManager class

## Decision: Explicit Schema Generation

**Date**: 2025-01-06
**Context**: Current automatic schema generation is complex and brittle
**Rationale**:

- Schema modification in SimpleAgent is error-prone
- Too much "magic" happening automatically
- Hard to debug schema issues
  **Trade-offs**:
- More verbose agent creation
- Users need to understand schemas better
  **Alternative**: Keep automatic generation (rejected - too brittle)
  **Solution**: Make schema generation explicit and configurable

## Decision: Reduce Mixin Usage

**Date**: 2025-01-06
**Context**: Base agent uses 4+ mixins creating complex inheritance
**Rationale**:

- MRO conflicts
- Hard to understand method resolution
- Debugging complexity
  **Trade-offs**:
- Need to move functionality to composition
- Some code duplication initially
  **Alternative**: Keep mixin architecture (rejected - causes MRO issues)
  **Solution**: Convert mixins to composition pattern where possible
