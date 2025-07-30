# Node I/O Patterns

## Key Insights

### Tool Node Pattern

- **Input**: AIMessage with tool_calls (in messages field)
- **Output**: ToolMessages appended to messages field
- **Key Point**: Always works with the 'messages' field (or whatever the messages_key is set to)

### Validation Node V2 Pattern

- **Input**: AIMessage with tool_calls (in messages field)
- **Output**: Validation results, but routes differently based on validation outcome
- **Key Point**: Also works primarily with the messages field

### Common Pattern

Most nodes follow this pattern:

1. Read from messages field (List[BaseMessage])
2. Process the last message or all messages
3. Either append new messages or update other fields
4. The 'messages' field is the primary communication channel

## Implications for Schema Design

1. **Messages Field is Central**: The messages field should be:
   - Shared across nodes
   - Use the enhanced MessageList type for token counting
   - Have proper reducers (add_messages)

2. **Node-Specific Fields**: Each node can have additional fields for:
   - Configuration (tool_routes, validation_rules, etc.)
   - Results (parsed_output, validation_result, etc.)
   - Errors (parse_error, tool_error, etc.)

3. **Engine Fields**: Should be separate from messages:
   - Used for configuration and tool discovery
   - Not part of the main message flow
