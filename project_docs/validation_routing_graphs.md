# Validation Routing Graphs - Visual Comparison

## Current SimpleAgent Graph (BROKEN)

```mermaid
graph LR
    START([START]) --> agent_node[agent_node]
    agent_node --> validation[validation]
    validation --> ???[No Edge!]

    style ??? fill:#ff6666,stroke:#ff0000,stroke-width:4px
```

### What Happens:

1. Agent generates tool calls
2. Goes to validation node
3. Validation processes and creates ToolMessages
4. **STUCK** - No edges from validation, graph doesn't know where to go
5. LangGraph retries from START
6. Hits recursion limit after 100 attempts

## SimpleAgentV2 Graph (WORKING)

```mermaid
graph LR
    START([START]) --> agent_node[agent_node]
    agent_node --> validation_v2[validation_v2]
    validation_v2 --> router{validation_router_v2}
    router -->|parse_output route| parse_output[parse_output]
    router -->|langchain_tool route| tool_node[tool_node]
    router -->|errors| agent_node
    parse_output --> END([END])
    tool_node --> agent_node
```

### What Happens:

1. Agent generates tool calls
2. Goes to validation_v2 node
3. Validation processes and adds ToolMessages to state
4. validation_router_v2 function examines tool routes:
   - Structured output (`parse_output` route) → parse_output node
   - Regular tools (`langchain_tool` route) → tool_node
   - Errors → back to agent_node
5. Flow continues properly

## The Fix - Add Conditional Edges

```mermaid
graph LR
    START([START]) --> agent_node[agent_node]
    agent_node --> validation[validation]
    validation --> router{validation_router_v2}
    router -->|parse_output| parse_output[parse_output]
    router -->|tool_node| tool_node[tool_node]
    router -->|errors| agent_node
    parse_output --> END([END])
    tool_node --> agent_node

    style router fill:#90EE90,stroke:#006400,stroke-width:2px
```

## Tool Route Flow for Plan[Task]

```
1. User Input: "Create a plan"
   ↓
2. Agent generates:
   tool_call = {
     "name": "plan_task_generic",  // Sanitized from Plan[Task]
     "args": {...}
   }
   ↓
3. AugLLMConfig has route:
   "plan_task_generic" → "parse_output"
   ↓
4. Validation node processes tool call
   ↓
5. validation_router_v2 checks route:
   - Sees "parse_output" route
   - Routes to parse_output node
   ↓
6. parse_output node handles structured output
   ↓
7. END
```

## Key Insight

The validation node is just a state updater - it needs a routing function to decide where to go next. SimpleAgent is missing this critical routing step.
