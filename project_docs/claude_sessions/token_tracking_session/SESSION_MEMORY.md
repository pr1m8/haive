# Token Tracking and State Schema Session Memory

## Session Overview
**Date**: 2025-01-09
**Goal**: Implement token tracking for messages and create a clean state schema hierarchy

## Key Accomplishments

### 1. Token Tracking Implementation
- Created `MessagesStateWithTokenUsage` as THE standard for token-aware conversations
- Automatically tracks tokens for ALL messages (not just AI messages)
- Includes cost calculation, usage aggregation, and capacity monitoring
- Added `TokenUsageMixin` for reusable token tracking functionality

### 2. State Schema Hierarchy
```
MessagesState (basic, no tokens)
└── MessagesStateWithTokenUsage (with token tracking)
    ├── ToolState (tools + tokens)
    └── LLMState (single engine + tokens + thresholds)
```

### 3. LLMState Features
- Single engine focus (not multiple engines)
- Auto-detects context length from model name (gpt-4-turbo → 128k)
- Configurable thresholds (warning at 75%, critical at 90%)
- Context length override option
- Rich metadata extraction from engine

### 4. Field Registry Updates
- Added `PrebuiltStates` registry for easy access
- Created aliases:
  - `TokenAwareState` = `MessagesStateWithTokenUsage`
  - `TokenToolState` = `ToolState`
  - `AgentState` = `LLMState`
- StandardFields.messages(use_enhanced=True) now uses MessageList

### 5. Schema Composer Integration
- Fixed to use StandardFields instead of hardcoded List[BaseMessage]
- Now uses field registry for messages field
- Replaced BaseMessage with AnyMessage for compatibility

## Key Design Decisions

1. **Explicit over Implicit**: Rather than auto-detecting when to use token tracking, we have clear separate classes
2. **Token Tracking Everywhere**: When using MessagesStateWithTokenUsage, ALL messages are tracked
3. **Single Engine for LLMState**: Cleaner design for LLM agents that don't need multiple engines
4. **Model-Aware Context**: LLMState knows about different model context lengths

## Issues Identified

1. **Schema Composer Complexity**: The schema composer auto-adds messages in multiple places, making it hard to ensure the enhanced MessageList is used
2. **MessageList vs List[AnyMessage]**: The RootModel structure means the actual type is List[AnyMessage], not MessageList
3. **Complex Prebuilt States**: ToolStateWithValidation and MetaState are overengineered - putting on back burner

## Next Steps

1. Consider creating PromptState for handling prompt template variables
2. Simplify schema composer to reduce auto-magic behavior
3. Document the clear hierarchy of states for users
4. Test token tracking with actual LLM responses

## Code Locations

- `/packages/haive-core/src/haive/core/schema/prebuilt/messages/messages_with_token_usage.py` - Main token tracking state
- `/packages/haive-core/src/haive/core/schema/prebuilt/llm_state.py` - Single engine LLM state
- `/packages/haive-core/src/haive/core/schema/field_registry.py` - Updated with PrebuiltStates
- `/packages/haive-core/src/haive/core/schema/prebuilt/tool_state.py` - Now extends MessagesStateWithTokenUsage