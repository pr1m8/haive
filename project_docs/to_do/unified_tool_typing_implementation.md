# TODO: Unified Tool Typing Implementation

**Created**: 2025-08-08  
**Priority**: HIGH  
**Status**: Planning Complete, Ready for Implementation  
**Related Docs**: @project_docs/guides/tools/

## Overview

We need to create a unified tool typing system where ToolEngine is the single source of truth for tool types and capabilities, and all components (ToolRouteMixin, ToolList, ValidationNodes, etc.) use these definitions.

## Current Problems

1. **Multiple Tool Type Definitions**:
   - ToolRouteMixin has its own analysis
   - ToolList has complex Union types
   - AugLLMConfig has another definition
   - Various agents use `list[Any]`

2. **Inconsistent Tool Routing**:
   - ValidationNodeConfigV2 has hardcoded routing logic
   - Different components determine tool types differently
   - No unified capability system

3. **Missing Tool Properties**:
   - No standard way to check if tool is interruptible
   - No unified state interaction detection
   - No consistent structured output handling

## Implementation Plan

### Phase 1: Core ToolEngine Types (Week 1)

1. **Create `haive/core/engine/tool/types.py`**:
   - Define `ToolType` TypeAlias
   - Define `ToolCapabilities` enum
   - Create `ToolProperties` model
   - Add capability checking helpers

2. **Create `haive/core/engine/tool/analyzer.py`**:
   - Build `ToolAnalyzer` class
   - Implement capability detection methods
   - Use existing utilities (interrupt_utils, tool_schema_generator)
   - Fix `is_interruptible()` bug

3. **Fix ToolEngine Base**:
   - Implement missing `get_input_fields()`
   - Implement missing `get_output_fields()`
   - Add proper type annotations

### Phase 2: Core Mixin Updates (Week 1-2)

1. **Update ToolRouteMixin**:
   - Import ToolEngine types
   - Replace `_analyze_tool()` to use ToolAnalyzer
   - Add `get_tools_by_capability()` method
   - Keep backward compatibility

2. **Update ToolListMixin**:
   - Use ToolEngine's `ToolType` instead of complex Union
   - Update type annotations throughout

3. **Update ToolList Utility**:
   - Replace type detection with ToolAnalyzer
   - Use unified ToolType

### Phase 3: Critical Component Updates (Week 2)

1. **Update AugLLMConfig**:
   - Change `tools` field to use `ToolSequence` from ToolEngine
   - Update tool binding logic to use capabilities

2. **Update ValidationNodeConfigV2**:
   - Replace hardcoded routing with capability-based routing
   - Use ToolProperties for decision making
   - Keep legacy routing as fallback

3. **Update Tool State Schemas**:
   - Add capability helper methods
   - Ensure proper type propagation

### Phase 4: Node Updates (Week 3)

1. **Update ToolNodeConfigV2 Subclasses**:
   - LangChainToolNode
   - FunctionToolNode
   - PydanticToolNode
   - Use ToolAnalyzer for type detection

2. **Update Execution Nodes**:
   - Use capability-based execution strategies
   - Handle new tool properties

### Phase 5: Integration & Testing (Week 4)

1. **Update Agent Patterns**:
   - Ensure all agents use unified typing
   - Add capability-based tool selection

2. **Migration Helpers**:
   - Create compatibility layer
   - Add deprecation warnings
   - Provide update scripts

3. **Comprehensive Testing**:
   - Test all tool types
   - Verify capability detection
   - Ensure backward compatibility

## Key Files to Modify

### New Files to Create:

- `packages/haive-core/src/haive/core/engine/tool/types.py`
- `packages/haive-core/src/haive/core/engine/tool/analyzer.py`

### High Priority Updates:

- `packages/haive-core/src/haive/core/common/mixins/tool_route_mixin.py`
- `packages/haive-core/src/haive/core/common/mixins/tool_list_mixin.py`
- `packages/haive-core/src/haive/core/utils/tool_list.py`
- `packages/haive-core/src/haive/core/engine/aug_llm/config.py`
- `packages/haive-core/src/haive/core/graph/node/validation_node_config_v2.py`

### Medium Priority Updates:

- `packages/haive-core/src/haive/core/graph/node/tool_node_config_v2.py`
- `packages/haive-core/src/haive/core/schema/prebuilt/tool_state.py`
- `packages/haive-agents/src/haive/agents/tool_utils.py`

## Success Criteria

1. **Single Source of Truth**: All tool types defined in ToolEngine
2. **Consistent Analysis**: All components use ToolAnalyzer
3. **Capability-Based Routing**: Replace type checking with capabilities
4. **Backward Compatible**: Existing code continues to work
5. **Better Developer Experience**: Easy to find tools by capability

## Notes

- Fix the `is_interruptible()` bug in interrupt_utils (line 107)
- Ensure ToolEngine can be imported without circular dependencies
- Keep performance in mind - tool analysis may be called frequently
- Document the new capability system thoroughly
- Consider caching analyzed tool properties

## Dependencies

- Complete ToolEngine base implementation first
- Coordinate with team on breaking changes
- May need to update documentation and examples

## Tags

`#tool-engine` `#unified-typing` `#refactoring` `#high-priority`
