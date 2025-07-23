# Prompt-State Pattern Memory

**Date**: 2025-01-21
**Status**: Critical Pattern Discovered
**Context**: Plan-and-Execute V3 Implementation

## 🔑 Key Discovery: ChatPromptTemplate with State Field Mapping

### Critical Pattern

**ALWAYS use `engine.prompt_template` with ChatPromptTemplate, NOT `system_message` strings**

```python
# ✅ CORRECT - Use ChatPromptTemplate in engine config
planner_config = AugLLMConfig.model_copy(self.config)
planner_config.prompt_template = planner_prompt  # ChatPromptTemplate from prompts.py
self.planner = SimpleAgent(
    name=f"{name}_planner",
    engine=planner_config,
    structured_output_model=ExecutionPlan
)

# ❌ WRONG - Don't use system_message string
self.planner = SimpleAgent(
    name=f"{name}_planner",
    engine=self.config,
    system_message=PLANNER_SYSTEM_MESSAGE,  # This bypasses state field mapping
    structured_output_model=ExecutionPlan
)
```

### Why This Matters

1. **State Field Auto-Population**: Computed fields automatically populate prompt variables
2. **Dynamic Content**: Variables like `{current_step}`, `{plan_status}` update in real-time
3. **Type Safety**: State schema ensures all required fields are available
4. **Enhanced MultiAgent V3 Integration**: Coordinator handles `prompt.format_messages()` automatically

### Computed Fields Pattern

```python
class PlanExecuteV3State(MessagesState):
    @computed_field
    @property
    def current_step(self) -> Optional[str]:
        """Get formatted current step for executor"""
        # Dynamically generated from plan state

    @computed_field
    @property
    def plan_status(self) -> str:
        """Get formatted plan status"""
        # Real-time status from plan progress

    @computed_field
    @property
    def previous_results(self) -> str:
        """Get formatted previous step results"""
        # Latest execution results formatted
```

### Prompt Template Structure

```python
executor_prompt = ChatPromptTemplate.from_messages([
    ("system", EXECUTOR_SYSTEM_MESSAGE),
    MessagesPlaceholder(variable_name="messages", optional=True),
    ("human", """Current Plan Status: {plan_status}
Current Step to Execute: {current_step}
Previous Steps Results: {previous_results}
Execute the current step...""")
])
```

## 🎯 Implementation Requirements

### For All Advanced Agent Patterns:

1. **Define computed fields** in state schema for dynamic prompt variables
2. **Create ChatPromptTemplates** with state field placeholders
3. **Configure engine.prompt_template** instead of system_message
4. **Use AugLLMConfig.model_copy()** to create per-agent configs
5. **Document prompt-to-state mapping** for each agent

### File Organization:

- `state.py` - State schema with computed fields
- `prompts.py` - ChatPromptTemplate definitions
- `agent.py` - Agent configuration with prompt_template
- `PROMPT_STATE_MAPPING.md` - Documentation of field mappings

## 🚨 Critical Errors to Avoid

1. **Using system_message strings** - bypasses state integration
2. **Hardcoded prompt variables** - use computed fields instead
3. **Direct state access in prompts** - use field placeholders
4. **Missing MessagesPlaceholder** - breaks conversation context

## 🔄 Next Applications

Apply this pattern to:

- Tree of Thoughts (ToT) V3
- Reflexion V3
- LATS V3
- ReWOO V3

Each will need:

- State schema with computed fields for their specific variables
- ChatPromptTemplate with proper placeholders
- Engine configuration with prompt_template
