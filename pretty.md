# Intelligent Agent Routing with Early Termination

This improved implementation makes routing decisions more intelligently by detecting task completion early and avoiding unnecessary steps.

```python
def _route_agent_output(self, state: Any) -> Union[str, List[Send]]:
    """
    Route output from agent to appropriate next node(s).
    
    This function implements complex routing, supporting:
    1. Single tool execution (returns the node name)
    2. Parallel tool execution (returns list of Send objects)
    3. End of reasoning (returns "end")
    4. Structured output (returns "structured_output")
    """
    # Early termination for completed tasks
    # If the last message contains completion indicators, skip further processing
    messages = getattr(state, 'messages', [])
    if messages:
        last_message = messages[-1]
        if isinstance(last_message, AIMessage):
            # Check for completion indicators in the message
            content = getattr(last_message, 'content', '').lower()
            if content and any(marker in content for marker in [
                "task completed", "completed successfully", "final answer:", 
                "conclusion:", "final response:", "completed the task"
            ]):
                logger.info("Task completion detected in message content, ending workflow")
                return "structured_output" if self.config.use_structured_output_node else "end"
    
    # Check for remaining steps
    if hasattr(state, 'remaining_steps'):
        if state.remaining_steps <= 0:
            logger.info("No remaining steps, ending")
            return "structured_output" if self.config.use_structured_output_node else "end"
        # Decrement the steps counter
        state.remaining_steps -= 1
    
    # Check if there's any message
    if not messages:
        logger.warning("No messages in state")
        return "end"
    
    # Get the last message
    last_message = messages[-1]
    
    # If not an AIMessage or no tool calls, return end or structured output
    if not isinstance(last_message, AIMessage) or not getattr(last_message, 'tool_calls', None):
        # Check if this appears to be a final answer
        if isinstance(last_message, AIMessage) and getattr(last_message, 'content', None):
            # If we have structured output node, use it
            if hasattr(self.config, 'use_structured_output_node') and self.config.use_structured_output_node:
                return "structured_output"
        return "end"
    
    # Extract tool calls
    tool_calls = last_message.tool_calls
    
    # Map each tool call to its appropriate node
    tools_to_nodes = {}
    
    # Create mapping of tool names to node names
    tool_to_node_map = {}
    for node_name, tools_list in self.tools_map.items():
        for tool in tools_list:
            if hasattr(tool, 'name'):
                tool_to_node_map[tool.name] = node_name
    
    # Group tool calls by node
    for tool_call in tool_calls:
        tool_name = tool_call.get('name')
        if tool_name in tool_to_node_map:
            node_name = tool_to_node_map[tool_name]
            if node_name not in tools_to_nodes:
                tools_to_nodes[node_name] = []
            tools_to_nodes[node_name].append(tool_call)
    
    # If no valid tool calls found but the message has content, treat as a final answer
    if not tools_to_nodes and isinstance(last_message, AIMessage) and getattr(last_message, 'content', None):
        if hasattr(self.config, 'use_structured_output_node') and self.config.use_structured_output_node:
            return "structured_output"
        return "end"
        
    # Check if we need parallel execution
    if self.config.parallel_tool_execution and len(tools_to_nodes) > 1:
        # Return Send objects for parallel execution
        return [Send(node, [tool_call]) for node, tool_calls in tools_to_nodes.items() for tool_call in tool_calls]
    elif tools_to_nodes:
        # Return the first node (sequential execution)
        return next(iter(tools_to_nodes.keys()))
    else:
        # No valid tool calls, end
        if hasattr(self.config, 'use_structured_output_node') and self.config.use_structured_output_node:
            return "structured_output"
        return "end"
```

## Key Improvements

1. **Early Termination Detection**
   - Recognizes completion markers in message content
   - Prevents unnecessary processing when tasks are already complete

2. **Smart Fallback Handling**
   - Better handles cases where a message has content but no tool calls
   - Properly routes to structured output when appropriate

3. **Optimized Flow Control**
   - Removes redundant code
   - Provides clear decision paths for different scenarios

4. **Enhanced Error Handling**
   - More robust checking of message attributes
   - Safer access to potentially missing state properties 