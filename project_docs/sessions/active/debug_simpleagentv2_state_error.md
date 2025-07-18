# Debug SimpleAgentV2 State Validation Error

**Issue**: SimpleAgentV2State validation error - engine field expects dict/Engine but gets None
**Date**: 2025-01-09
**Status**: In Progress

## Problem Description

When running the notebook `Untitled83.ipynb`, the SimpleAgentV2 agent fails with:

```
ERROR    Error during agent execution: 1 validation error for SimpleAgentV2State
         engine
           Input should be a valid dictionary or instance of Engine
             For further information visit https://errors.pydantic.dev/2.11/v/model_type
```

The debug output shows the state at step 0 has `engine: None`:

```
[0:tasks] Starting 1 task for step 0:
- __start__ -> {'content': None,
 'engine': None,
 'engine_route_config': {...},
 'engines': {},
 'messages': [],
 ...
}
```

## Root Cause Analysis

Looking at the notebook code:

```python
def agent_tester(prompt,model,test_prompt):
    agent=SimpleAgentV2(engine=AugLLMConfig(prompt_template=prompt,structured_output_model=model,structured_output_version='v2'))
    return agent.run(test_prompt,debug=True)
```

The issue is that when the agent runs, the initial state is created with `engine: None` even though the agent has a valid engine configured.

## Investigation Path

1. **SimpleAgentV2 initialization**: The agent is created with `engine=AugLLMConfig(...)` which should be valid.

2. **State creation**: The state is showing `engine: None` at the **start** node, which suggests the engine field is not being properly initialized in the state.

3. **Schema composition**: The SimpleAgentV2State is created by SchemaComposer, and it's expecting the engine field to be populated.

## Hypothesis

The issue appears to be that:

1. The SimpleAgentV2State schema includes an `engine` field (from the composed schema)
2. When the graph starts execution, it initializes the state with default values
3. The `engine` field defaults to `None` which fails validation

## Solution Options

1. **Option 1**: The engine should not be part of the state schema - it should be managed separately
2. **Option 2**: The initial state should include the engine from the agent
3. **Option 3**: The engine field should be Optional in the state schema

## Code Analysis

From SimpleAgentV2:

- Line 141: `self.engines["main"] = self.engine` - The engine is stored in the engines dict
- Line 144: `self._register_engine_in_registry()` - The engine is registered globally
- Line 249: `self.engine.output_schema = enhanced_schema` - The engine's output schema is modified

The issue is likely that the composed state schema includes an `engine` field that expects an Engine instance, but the initial state doesn't populate it.

## Next Steps

1. Check how the SimpleAgentV2State is composed
2. Look at the base Agent class to see how state initialization works
3. Determine if the engine field should be excluded from the state schema
4. Or ensure the engine is properly initialized in the state

## Working Solution

The problem is that:

1. The SimpleAgentV2State schema includes an `engine` field (from schema composition)
2. When `run()` is called with just a string, it creates initial state with default values
3. The `engine` field defaults to `None` which fails validation

### Root Cause

The schema composer is including engine-related fields in the state schema, but these should be excluded. The engine is not part of the state - it's part of the agent configuration.

### Solution

The issue is in how the state schema is being composed. The engine should not be included as a field in the state schema. We need to:

1. Check the schema composition process to exclude engine fields
2. Or ensure the engine field is Optional in the state schema
3. Or populate the engine field when creating initial state

### Temporary Workaround

Instead of calling:

```python
agent.run(test_prompt, debug=True)
```

Try passing a proper state dict:

```python
agent.run({"query": test_prompt}, debug=True)
```

Or modify the agent to not include engine in state schema.
