# Dynamic Choice Model Insight

## Agent ID: claude_agent_20250107_165800

## What is DynamicChoiceModel?

Found in `/haive-core/src/haive/core/common/models/dynamic_choice_model.py`

**Purpose**: Generic Pydantic model that dynamically creates choice validation models

**Key Features**:

1. Takes list of options (strings, dicts, or objects with name attribute)
2. Dynamically creates Pydantic model with validated "choice" field
3. Add/remove options → automatically regenerates model
4. Always includes "END" option
5. Uses field validators for choice validation

## How This Helps Supervisor

**Current Approach**: Route tools (`route_to_math_agent`, `route_to_planning_agent`)
**Enhanced Approach**: DynamicChoiceModel + Route tools

### Integration Pattern:

```python
class SupervisorWithChoiceModel(ReactAgent):
    # Choice model that updates with available agents
    agent_choice_model: DynamicChoiceModel = Field(default_factory=DynamicChoiceModel)

    @model_validator(mode="after")
    def setup_choice_model(self):
        # Add agents to choice model
        for agent_name in self.registry.list_available():
            self.agent_choice_model.add_option(agent_name)

        # Create structured decision tool
        @tool
        def choose_agent(task: str) -> str:
            """Analyze task and choose appropriate agent"""
            # Use LLM with choice model for structured decision
            ChoiceModel = self.agent_choice_model.current_model
            # ... decision logic
            choice = ChoiceModel(choice="math_agent")  # Validated!
            return choice.choice
```

### Benefits:

1. **Validation**: Ensures chosen agent exists in registry
2. **Dynamic**: Choice model updates when agents added/removed
3. **Structured**: Forces explicit decision making
4. **Traceable**: Clear record of routing decisions

### Two-Stage Flow:

1. **Stage 1**: Choose agent using DynamicChoiceModel (structured decision)
2. **Stage 2**: Route to chosen agent using route tools

This combines:

- **Structured decision making** (choice model)
- **Dynamic execution** (route tools)
- **Automatic validation** (field validators)

## Implementation Strategy

1. Keep current route tools approach working ✅
2. Add DynamicChoiceModel for decision enhancement
3. Test both approaches
4. Show how choice model adds validation layer

This is a perfect complement to the registry + route tools pattern!
