# LangChain Core Prompts: Comprehensive Deep Dive

**Created**: 2025-01-30  
**Purpose**: Deep technical exploration of LangChain's prompt system internals, typing, and implementation details

## Table of Contents

1. [Overview](#overview)
2. [Class Hierarchy](#class-hierarchy)
3. [Core Concepts](#core-concepts)
4. [Template Formats & Security](#template-formats--security)
5. [ChatPromptTemplate](#chatprompttemplate)
6. [MessagesPlaceholder](#messagesplaceholder)
7. [Partial Variables Deep Dive](#partial-variables-deep-dive)
8. [Optional Variables & Typing](#optional-variables--typing)
9. [Advanced Patterns](#advanced-patterns)
10. [Implementation Details](#implementation-details)
11. [Do's and Don'ts](#dos-and-donts)
12. [Best Practices](#best-practices)

## Overview

LangChain's prompt system is built around the concept of **templates that can be composed, formatted, and reused**. The system is designed to:

- Support multiple message formats (chat, string, few-shot)
- Enable dynamic content injection through variables
- Allow partial pre-population of templates
- Handle optional content gracefully
- Compose complex prompts from simpler building blocks

## Class Hierarchy

```
BasePromptTemplate (Abstract base for all prompts)
├── StringPromptTemplate (String-based prompts)
│   ├── PromptTemplate (Standard f-string templates)
│   ├── FewShotPromptTemplate (Few-shot learning)
│   └── FewShotPromptWithTemplates (Few-shot with examples)
└── BaseChatPromptTemplate (Chat-based prompts)
    └── ChatPromptTemplate (Main chat prompt class)

BaseMessagePromptTemplate (Base for message templates)
├── MessagesPlaceholder (Placeholder for message lists)
└── BaseStringMessagePromptTemplate
    ├── ChatMessagePromptTemplate (Generic role messages)
    ├── HumanMessagePromptTemplate (Human/user messages)
    ├── AIMessagePromptTemplate (AI/assistant messages)
    └── SystemMessagePromptTemplate (System messages)
```

## Core Concepts

### 1. Input Variables

Variables that MUST be provided when formatting the prompt. These are automatically detected from the template:

```python
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages([
    ("system", "You are a {role} assistant."),
    ("human", "{question}")
])

# Automatic detection from template parsing
print(template.input_variables)  # ["role", "question"]

# Both MUST be provided:
result = template.invoke({"role": "helpful", "question": "Hello"})
```

**How it works internally:**
- Templates are parsed using the specified format (f-string, jinja2, mustache)
- Variables are extracted using regex for f-strings, AST parsing for jinja2
- Variables in `partial_variables` are excluded from `input_variables`

### 2. Partial Variables

Variables that are pre-populated and don't need to be provided at runtime. Support both static values and callables:

```python
# Type signature shows Union[str, Callable[[], str]]
def partial(self, **kwargs: Union[str, Callable[[], str]]) -> BasePromptTemplate:
    ...

# Static partial
template_with_time = template.partial(time="2025-01-30 10:00 AM")

# Dynamic partial with callable
from datetime import datetime
template_with_dynamic_time = template.partial(
    time=lambda: datetime.now().isoformat()
)

# The callable is invoked during _merge_partial_and_user_variables:
partial_kwargs = {
    k: v if not callable(v) else v() 
    for k, v in self.partial_variables.items()
}
```

### 3. Optional Variables

Variables that CAN be provided but don't have to be. These are primarily used with MessagesPlaceholder:

```python
# Optional variables are tracked separately
class BasePromptTemplate:
    input_variables: list[str]  # Required variables
    optional_variables: list[str] = Field(default=[])  # Optional ones
    
# MessagesPlaceholder automatically registers as optional when optional=True
template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder("history", optional=True),  # Auto-added to optional_variables
    ("human", "{question}")
])

print(template.input_variables)     # ["question"]
print(template.optional_variables)  # ["history"]
```

## Template Formats & Security

### Supported Formats

LangChain supports three template formats, each with different capabilities and security implications:

```python
PromptTemplateFormat = Literal["f-string", "mustache", "jinja2"]

DEFAULT_FORMATTER_MAPPING: dict[str, Callable] = {
    "f-string": formatter.format,      # Default, safest
    "mustache": mustache_formatter,    # Logic-less templates
    "jinja2": jinja2_formatter,        # Powerful but dangerous
}
```

### 1. F-String Format (Default & Recommended)

```python
# Simple variable substitution using Python's str.format()
template = PromptTemplate.from_template(
    "Hello {name}, you have {count} messages",
    template_format="f-string"  # Default
)
```

**Pros:**
- Safe - no code execution
- Fast - uses Python's built-in formatting
- Simple - just variable substitution

**Cons:**
- Limited - no logic or conditionals
- Basic formatting only

### 2. Mustache Format

```python
# Logic-less templates with sections and conditionals
template = PromptTemplate.from_template(
    """
    {{#users}}
    Hello {{name}}!
    {{/users}}
    {{^users}}
    No users found.
    {{/users}}
    """,
    template_format="mustache"
)
```

**Features:**
- Sections for iteration: `{{#items}}...{{/items}}`
- Inverted sections: `{{^empty}}...{{/empty}}`
- Comments: `{{! This is a comment }}`
- Partials: `{{> partial_name }}`

**Note:** Cannot be validated at template creation time.

### 3. Jinja2 Format (⚠️ SECURITY WARNING)

```python
# DANGEROUS - Only use with trusted templates!
template = PromptTemplate.from_template(
    """
    {% for item in items %}
    - {{ item.name }}: {{ item.value }}
    {% endfor %}
    
    Total: {{ items | length }}
    """,
    template_format="jinja2"
)
```

**Security Considerations:**
- Uses `SandboxedEnvironment` by default (since v0.0.329)
- Sandboxing is **best-effort**, not a security guarantee
- **NEVER** accept jinja2 templates from untrusted sources
- Can lead to arbitrary Python code execution

**Jinja2 Security Implementation:**
```python
def jinja2_formatter(template: str, /, **kwargs: Any) -> str:
    from jinja2.sandbox import SandboxedEnvironment
    # Sandboxed, but not foolproof!
    return SandboxedEnvironment().from_string(template).render(**kwargs)
```

### Template Validation

```python
# Validation is format-specific
DEFAULT_VALIDATOR_MAPPING: dict[str, Callable] = {
    "f-string": formatter.validate_input_variables,
    "jinja2": validate_jinja2,
    # Note: mustache has no validator
}

# Enable validation
template = PromptTemplate(
    template="Hello {name}",
    input_variables=["name", "extra"],  # Will warn about 'extra'
    validate_template=True  # Triggers validation
)
```

## ChatPromptTemplate

The main class for creating chat-based prompts. Supports multiple message formats:

### Creating Templates

```python
from langchain_core.prompts import ChatPromptTemplate

# Method 1: From messages list (most common)
template = ChatPromptTemplate.from_messages([
    ("system", "You are a {role} assistant."),
    ("human", "{input}"),
])

# Method 2: Direct instantiation
template = ChatPromptTemplate([
    ("system", "You are a helpful AI."),
    ("human", "{question}"),
])

# Method 3: Mixed message types
from langchain_core.messages import SystemMessage, HumanMessage

template = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are helpful."),
    ("human", "{input}"),
    ("placeholder", "{conversation}"),  # Shorthand for MessagesPlaceholder
])
```

### Message Format Options

```python
# 1. Tuple format: (role, template)
("system", "You are {name}")
("human", "Hello {user}")
("ai", "Nice to meet you")

# 2. Message instances
SystemMessage(content="Fixed system message")
HumanMessage(content="Fixed human message")

# 3. Placeholder format (creates MessagesPlaceholder)
("placeholder", "{variable_name}")

# 4. String shorthand (becomes human message)
"Hello {name}"  # Same as ("human", "Hello {name}")
```

### Template Variables

```python
template = ChatPromptTemplate.from_messages([
    ("system", "You are a {role} assistant named {name}."),
    MessagesPlaceholder("history", optional=True),
    ("human", "{question}")
])

# Automatic variable detection:
print(template.input_variables)  # ["role", "name", "question"]
print(template.optional_variables)  # ["history"]
```

## MessagesPlaceholder

A special component for injecting lists of messages into templates:

### Basic Usage

```python
from langchain_core.prompts import MessagesPlaceholder

# Required placeholder (must provide messages)
placeholder = MessagesPlaceholder("conversation")

# Optional placeholder (can be omitted)
placeholder = MessagesPlaceholder("history", optional=True)

# Limited messages (only last N)
placeholder = MessagesPlaceholder("recent_history", n_messages=5)
```

### In Templates

```python
template = ChatPromptTemplate.from_messages([
    ("system", "You are an AI assistant."),
    MessagesPlaceholder("conversation", optional=True),
    ("human", "{current_input}")
])

# Invoke with messages
result = template.invoke({
    "current_input": "What's the weather?",
    "conversation": [
        ("human", "Hi!"),
        ("ai", "Hello! How can I help?"),
    ]
})
```

### Behavior

- **Required** (optional=False): Must provide the variable, even if empty list
- **Optional** (optional=True): Can omit entirely, defaults to empty list
- **n_messages**: Only includes last N messages from the provided list

## Partial Variables Deep Dive

Partial variables are a powerful feature for pre-populating template values. They support both static values and dynamic callables.

### Type Signature & Implementation

```python
# From BasePromptTemplate
def partial(self, **kwargs: Union[str, Callable[[], str]]) -> BasePromptTemplate:
    """Return a partial of the prompt template."""
    prompt_dict = self.__dict__.copy()
    prompt_dict["input_variables"] = list(
        set(self.input_variables).difference(kwargs)  # Remove partialed vars
    )
    prompt_dict["partial_variables"] = {**self.partial_variables, **kwargs}
    return type(self)(**prompt_dict)

# How partials are merged at runtime
def _merge_partial_and_user_variables(self, **kwargs: Any) -> dict[str, Any]:
    partial_kwargs = {
        k: v if not callable(v) else v()  # Call functions here!
        for k, v in self.partial_variables.items()
    }
    return {**partial_kwargs, **kwargs}  # User vars override partials
```

### Creating Partials

```python
# Original template
base_template = ChatPromptTemplate.from_messages([
    ("system", "You are a {role} assistant. Location: {location}. Time: {time}"),
    ("human", "{question}")
])

# Method 1: Using partial() - creates new instance
specialized = base_template.partial(
    role="technical support",
    location="Seattle"
)
print(base_template.input_variables)  # ["role", "location", "time", "question"]
print(specialized.input_variables)    # ["time", "question"] - role/location removed!

# Method 2: During creation
template = ChatPromptTemplate.from_messages(
    [("system", "Time: {time}"), ("human", "{question}")],
    partial_variables={"time": "2025-01-30"}
)
```

### Dynamic Partials with Callables

```python
import uuid
from datetime import datetime

# Callable partials are invoked every time the template is formatted
template = ChatPromptTemplate.from_messages([
    ("system", "Session: {session_id}, Time: {current_time}"),
    ("human", "{message}")
]).partial(
    session_id=lambda: str(uuid.uuid4()),  # New UUID each time!
    current_time=lambda: datetime.now().isoformat()
)

# Each invocation gets fresh values
result1 = template.invoke({"message": "Hello"})
# session_id: "abc-123", current_time: "2025-01-30T10:00:00"

result2 = template.invoke({"message": "Hi again"})  
# session_id: "xyz-789", current_time: "2025-01-30T10:00:05"
```

### Partial Variable Precedence

```python
template = ChatPromptTemplate.from_messages([
    ("system", "Mode: {mode}"),
    ("human", "{input}")
]).partial(mode="default")

# User input OVERRIDES partial
result = template.invoke({
    "input": "Hello",
    "mode": "custom"  # This wins over partial "default"
})
# System message will be "Mode: custom"
```

### Advanced Partial Patterns

```python
# 1. Chaining partials
template = base_template.partial(env="prod").partial(version="1.0")

# 2. Conditional partials
def get_system_info():
    import platform
    return f"Python {platform.python_version()} on {platform.system()}"

debug_template = template.partial(
    debug_info=get_system_info if DEBUG else lambda: ""
)

# 3. Partial with complex objects (must be string or callable returning string!)
template = base_template.partial(
    config=lambda: json.dumps(load_config(), indent=2)
)
```

## Optional Variables & Typing

Optional variables provide flexibility in template invocation. They're primarily used with MessagesPlaceholder but can be manually specified.

### Type Definitions

```python
# From BasePromptTemplate
class BasePromptTemplate(RunnableSerializable[dict, PromptValue], ABC):
    input_variables: list[str]
    """Required variables."""
    
    optional_variables: list[str] = Field(default=[])
    """Optional variables - auto inferred from prompt."""
    
    input_types: dict[str, Any] = Field(default_factory=dict, exclude=True)
    """Types of variables - defaults to str if not specified."""
```

### Automatic Detection in ChatPromptTemplate

```python
# During ChatPromptTemplate initialization
for _message in messages_:
    if isinstance(_message, MessagesPlaceholder) and _message.optional:
        partial_vars[_message.variable_name] = []  # Default to empty list
        optional_variables.add(_message.variable_name)
    elif isinstance(_message, (BaseChatPromptTemplate, BaseMessagePromptTemplate)):
        input_vars.update(_message.input_variables)

# Sets are sorted for consistent ordering
kwargs = {
    "input_variables": sorted(input_vars),
    "optional_variables": sorted(optional_variables),
    "partial_variables": partial_vars,
}
```

### Input Schema Generation

```python
# How optional variables affect schema generation
def get_input_schema(self, config: Optional[RunnableConfig] = None) -> type[BaseModel]:
    # Required variables with ... (Ellipsis)
    required_input_variables = {
        k: (self.input_types.get(k, str), ...) 
        for k in self.input_variables
    }
    
    # Optional variables with None default
    optional_input_variables = {
        k: (self.input_types.get(k, str), None) 
        for k in self.optional_variables
    }
    
    return create_model_v2(
        "PromptInput",
        __module__="langchain_core.prompts.base",
        **required_input_variables,
        **optional_input_variables,
    )
```

### MessagesPlaceholder Behavior

```python
class MessagesPlaceholder(BaseMessagePromptTemplate):
    variable_name: str
    optional: bool = False
    n_messages: Optional[PositiveInt] = None
    
    @property
    def input_variables(self) -> list[str]:
        """Input variables for this prompt template."""
        return [self.variable_name] if not self.optional else []
    
    def format_messages(self, **kwargs: Any) -> list[BaseMessage]:
        value = (
            kwargs.get(self.variable_name, [])  # Default to [] if optional
            if self.optional
            else kwargs[self.variable_name]      # KeyError if not optional
        )
```

### Type Safety with Optional Variables

```python
# Example with typed optional variables
from typing import TypedDict, Optional, List
from langchain_core.messages import BaseMessage

class PromptInput(TypedDict, total=False):
    question: str  # Required
    history: Optional[List[BaseMessage]]  # Optional
    context: Optional[List[BaseMessage]]  # Optional

template = ChatPromptTemplate.from_messages([
    ("system", "You are helpful."),
    MessagesPlaceholder("history", optional=True),
    MessagesPlaceholder("context", optional=True),
    ("human", "{question}")
])

# Type-safe invocation
result = template.invoke(PromptInput(question="Hello"))  # history/context omitted
```

## Advanced Patterns

### 1. Conditional Content with Optional Placeholders

```python
template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder("examples", optional=True),
    MessagesPlaceholder("context", optional=True),
    MessagesPlaceholder("history", optional=True),
    ("human", "{question}")
])

# Flexible invocation - provide what you need
result = template.invoke({
    "question": "Explain quantum computing",
    "examples": [("human", "Example Q"), ("ai", "Example A")],
    # context and history omitted
})
```

### 2. Nested Templates

```python
# Sub-template for formatting context
context_template = ChatPromptTemplate.from_messages([
    ("system", "Context from {source}:"),
    ("human", "{content}")
])

# Main template
main_template = ChatPromptTemplate.from_messages([
    ("system", "You are a research assistant."),
    MessagesPlaceholder("formatted_contexts", optional=True),
    ("human", "{question}")
])

# Format contexts first
contexts = []
for ctx in data_sources:
    formatted = context_template.format_messages(source=ctx.name, content=ctx.text)
    contexts.extend(formatted)

# Then use in main template
result = main_template.invoke({
    "question": "Summarize the findings",
    "formatted_contexts": contexts
})
```

### 3. Dynamic System Messages

```python
def create_system_message(config):
    """Dynamically create system message based on config."""
    base = "You are a helpful AI assistant"
    
    if config.get("mode") == "creative":
        base += " with a creative and imaginative personality"
    elif config.get("mode") == "analytical":
        base += " focused on logical analysis and facts"
    
    if config.get("expertise"):
        base += f" with expertise in {config['expertise']}"
    
    return base + "."

# Use in template
template = ChatPromptTemplate.from_messages([
    ("system", "{system_message}"),
    MessagesPlaceholder("history", optional=True),
    ("human", "{question}")
])

# Invoke with dynamic system message
result = template.invoke({
    "system_message": create_system_message({"mode": "creative", "expertise": "poetry"}),
    "question": "Write a haiku"
})
```

### 4. Multi-Stage Templates

```python
# Stage 1: Planning template
planning_template = ChatPromptTemplate.from_messages([
    ("system", "You are a planning assistant."),
    ("human", "Create a plan for: {objective}")
])

# Stage 2: Execution template with plan context
execution_template = ChatPromptTemplate.from_messages([
    ("system", "You are an execution assistant."),
    MessagesPlaceholder("planning_context"),
    ("human", "Execute step: {step}")
])

# Use in sequence
plan_result = planning_template.invoke({"objective": "Build a web app"})
exec_result = execution_template.invoke({
    "planning_context": plan_result.messages,
    "step": "Set up the development environment"
})
```

### 5. Template Composition

```python
# Base template with common structure
base = ChatPromptTemplate.from_messages([
    ("system", "{system_message}"),
    MessagesPlaceholder("history", optional=True),
])

# Specialized templates by adding messages
qa_template = base + [("human", "Question: {question}\nAnswer:")]
chat_template = base + [("human", "{message}")]
instruction_template = base + [
    ("human", "Instruction: {instruction}\nInput: {input}\nOutput:")
]

# Or compose with other templates
combined = base + other_template
```

## Implementation Details

### Message Conversion Pipeline

```python
def _convert_to_message_template(
    message: MessageLikeRepresentation,
    template_format: PromptTemplateFormat = "f-string",
) -> Union[BaseMessage, BaseMessagePromptTemplate, BaseChatPromptTemplate]:
    """
    Converts various message representations to proper template objects.
    
    Supported formats:
    1. BaseMessagePromptTemplate - returned as-is
    2. BaseMessage - returned as-is
    3. str - converted to HumanMessagePromptTemplate
    4. ("role", "template") - converted based on role
    5. (MessageClass, "template") - uses MessageClass
    6. {"role": "...", "content": "..."} - dict format
    """
    
    # Shorthand conversions
    if isinstance(message, str):
        # "Hello {name}" → HumanMessagePromptTemplate
        return HumanMessagePromptTemplate.from_template(message, template_format)
    
    # Tuple format handling
    if isinstance(message, tuple):
        role, template = message
        if role == "placeholder":
            # ("placeholder", "{var}") → MessagesPlaceholder(variable_name="var", optional=True)
            return MessagesPlaceholder(variable_name=template.strip("{}"), optional=True)
```

### Variable Extraction

```python
# F-string variable extraction (uses Python's string.Formatter)
def get_template_variables(template: str, template_format: str) -> list[str]:
    if template_format == "f-string":
        # Uses formatter.parse() to find {variable} patterns
        variables = []
        for _, field_name, _, _ in Formatter().parse(template):
            if field_name:
                variables.append(field_name)
        return variables
    
    elif template_format == "jinja2":
        # Uses Jinja2 AST parsing
        from jinja2 import Environment, meta
        env = Environment()
        ast = env.parse(template)
        return list(meta.find_undeclared_variables(ast))
    
    elif template_format == "mustache":
        # Custom tokenizer for mustache templates
        return list(mustache_template_vars(template))
```

### Template Composition

```python
# How templates are combined with + operator
def __add__(self, other: Any) -> ChatPromptTemplate:
    # ChatPromptTemplate + ChatPromptTemplate
    if isinstance(other, ChatPromptTemplate):
        return ChatPromptTemplate(messages=self.messages + other.messages)
    
    # ChatPromptTemplate + list of messages
    elif isinstance(other, list):
        return ChatPromptTemplate(messages=self.messages + other)
    
    # ChatPromptTemplate + string (converts to human message)
    elif isinstance(other, str):
        prompt = PromptTemplate.from_template(other)
        return self + prompt
```

### Validation Process

```python
@model_validator(mode="before")
@classmethod
def pre_init_validation(cls, values: dict) -> Any:
    """Validates template consistency before initialization."""
    
    if values.get("validate_template"):
        # Combine input and partial variables for validation
        all_inputs = values["input_variables"] + list(values["partial_variables"])
        check_valid_template(
            values["template"], 
            values["template_format"], 
            all_inputs
        )
    
    # Auto-detect variables if not provided
    if values["template_format"]:
        detected_vars = get_template_variables(
            values["template"], 
            values["template_format"]
        )
        # Exclude partial variables from input variables
        values["input_variables"] = [
            var for var in detected_vars 
            if var not in values["partial_variables"]
        ]
```

## Do's and Don'ts

### ✅ DO's

1. **DO use f-string format by default**
```python
# Safe and simple
template = ChatPromptTemplate.from_messages([
    ("system", "You are a {role} assistant"),
    ("human", "{question}")
])
```

2. **DO use optional MessagesPlaceholder for flexibility**
```python
# Allows template to work with or without history
MessagesPlaceholder("history", optional=True)
```

3. **DO use partials for environment-specific values**
```python
# Keep base template generic
prod_template = base_template.partial(env="production", debug=False)
dev_template = base_template.partial(env="development", debug=True)
```

4. **DO validate templates when accepting user input**
```python
# If template comes from user/config
template = PromptTemplate(
    template=user_template,
    validate_template=True,  # Ensure it's valid
    template_format="f-string"  # Never jinja2 from users!
)
```

5. **DO use callable partials for dynamic values**
```python
# Fresh timestamp on each invocation
template.partial(timestamp=lambda: datetime.now().isoformat())
```

### ❌ DON'Ts

1. **DON'T use jinja2 with untrusted input**
```python
# NEVER DO THIS with user input!
user_template = request.form.get("template")
template = PromptTemplate(
    template=user_template,
    template_format="jinja2"  # SECURITY RISK!
)
```

2. **DON'T forget to make MessagesPlaceholder optional**
```python
# Bad - requires history even if empty
MessagesPlaceholder("history")  # Will throw KeyError if not provided

# Good - works without history
MessagesPlaceholder("history", optional=True)
```

3. **DON'T use mutable defaults in partials**
```python
# Bad - shared mutable state!
template.partial(items=[])  # Same list instance for all!

# Good - use callable for fresh instance
template.partial(items=lambda: [])
```

4. **DON'T override partial variables unnecessarily**
```python
# Confusing - partial says one thing, user input another
template = base.partial(mode="read-only")
result = template.invoke({"mode": "write"})  # Overrides partial

# Better - use different variable names
template = base.partial(default_mode="read-only")
```

5. **DON'T mix template formats**
```python
# Bad - trying to combine different formats
f_string_template + mustache_template  # Will raise ValueError

# Good - convert to same format first
```

6. **DON'T ignore validation warnings**
```python
# If you see: "Warning: Missing variables: ['foo']"
# It means your template expects 'foo' but input_variables doesn't include it
```

## Best Practices

### 1. Use Optional Placeholders for Flexibility

```python
# Good - flexible template
template = ChatPromptTemplate.from_messages([
    ("system", "You are helpful."),
    MessagesPlaceholder("context", optional=True),
    MessagesPlaceholder("examples", optional=True),
    MessagesPlaceholder("history", optional=True),
    ("human", "{input}")
])

# Bad - rigid template requiring all fields
template = ChatPromptTemplate.from_messages([
    ("system", "Context: {context}\nExamples: {examples}"),
    MessagesPlaceholder("history"),  # Required!
    ("human", "{input}")
])
```

### 2. Leverage Partial Variables

```python
# Good - use partials for environment config
base_template = ChatPromptTemplate.from_messages([
    ("system", "Environment: {env}\nVersion: {version}\n{instructions}"),
    ("human", "{input}")
])

prod_template = base_template.partial(env="production", version="1.0")
dev_template = base_template.partial(env="development", version="dev")

# Bad - hardcoding environment values
prod_template = ChatPromptTemplate.from_messages([
    ("system", "Environment: production\nVersion: 1.0\n{instructions}"),
    ("human", "{input}")
])
```

### 3. Clear Variable Names

```python
# Good - descriptive names
template = ChatPromptTemplate.from_messages([
    ("system", "You are a {agent_role} assistant."),
    MessagesPlaceholder("conversation_history", optional=True),
    ("human", "{user_question}")
])

# Bad - ambiguous names
template = ChatPromptTemplate.from_messages([
    ("system", "You are a {role} assistant."),
    MessagesPlaceholder("msgs", optional=True),
    ("human", "{q}")
])
```

### 4. Validate Template Usage

```python
# Good - check what variables are needed
template = create_complex_template()
print(f"Required: {template.input_variables}")
print(f"Optional: {template.optional_variables}")
print(f"Partial: {list(template.partial_variables.keys())}")

# Create helper for validation
def validate_inputs(template, inputs):
    missing = set(template.input_variables) - set(inputs.keys())
    if missing:
        raise ValueError(f"Missing required variables: {missing}")
    
    extra = set(inputs.keys()) - set(template.input_variables) - set(template.optional_variables)
    if extra:
        print(f"Warning: Extra variables provided: {extra}")
```

### 5. Template Reuse

```python
# Good - create reusable base templates
class PromptLibrary:
    @staticmethod
    def qa_template():
        return ChatPromptTemplate.from_messages([
            ("system", "You are a helpful Q&A assistant."),
            MessagesPlaceholder("context", optional=True),
            ("human", "{question}")
        ])
    
    @staticmethod
    def chat_template():
        return ChatPromptTemplate.from_messages([
            ("system", "You are a conversational AI."),
            MessagesPlaceholder("history", optional=True),
            ("human", "{message}")
        ])
    
    @staticmethod
    def instruction_template():
        return ChatPromptTemplate.from_messages([
            ("system", "Follow the instructions precisely."),
            MessagesPlaceholder("examples", optional=True),
            ("human", "Instruction: {instruction}\nInput: {input}")
        ])

# Use throughout application
qa_prompt = PromptLibrary.qa_template()
```

## Common Pitfalls and Solutions

### 1. Forgetting Optional on MessagesPlaceholder

```python
# Problem - KeyError when history not provided
bad_template = ChatPromptTemplate.from_messages([
    ("system", "You are helpful."),
    MessagesPlaceholder("history"),  # Required by default!
    ("human", "{question}")
])

# Solution - make it optional
good_template = ChatPromptTemplate.from_messages([
    ("system", "You are helpful."),
    MessagesPlaceholder("history", optional=True),
    ("human", "{question}")
])
```

### 2. Variable Name Conflicts

```python
# Problem - same variable in multiple places
bad_template = ChatPromptTemplate.from_messages([
    ("system", "Mode: {mode}"),
    ("human", "Set mode to: {mode}")  # Conflict!
])

# Solution - use different names or partial
good_template = ChatPromptTemplate.from_messages([
    ("system", "Current mode: {current_mode}"),
    ("human", "Switch to mode: {new_mode}")
])
```

### 3. Not Using Shorthand

```python
# Verbose
template = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="history", optional=True),
    HumanMessagePromptTemplate.from_template("{input}")
])

# Clean shorthand
template = ChatPromptTemplate.from_messages([
    ("placeholder", "{history}"),  # Auto-optional for placeholders
    ("human", "{input}")
])
```

## Summary of Key Insights

### Core Capabilities

1. **Three Template Formats**: 
   - `f-string` (default, safe) - Simple variable substitution
   - `mustache` (logic-less) - Sections and conditionals without code execution
   - `jinja2` (powerful but risky) - Full templating with sandboxed execution

2. **Variable Types**:
   - **Input Variables**: Auto-detected, must be provided
   - **Partial Variables**: Pre-populated, support callables for dynamic values
   - **Optional Variables**: Can be omitted, primarily via MessagesPlaceholder

3. **Type System**:
   - Full typing support with `Union[str, Callable[[], str]]` for partials
   - Automatic schema generation with Pydantic
   - Type-safe variable detection and validation

### Implementation Details

- **Variable Detection**: Uses regex (f-string), AST parsing (jinja2), or tokenization (mustache)
- **Partial Merging**: Callables invoked at format time, user vars override partials
- **Message Conversion**: Flexible pipeline supporting tuples, strings, dicts, and objects
- **Validation**: Format-specific with warnings for missing/extra variables

### Security Considerations

- **Jinja2 Risk**: Even with `SandboxedEnvironment`, never trust user templates
- **Default Safety**: f-string format prevents code execution
- **Validation**: Always validate templates from external sources

### Best Practices Summary

1. **Flexibility First**: Use optional placeholders and partials
2. **Safety Always**: Default to f-string format
3. **Type Awareness**: Understand how variables are detected and typed
4. **Composition Power**: Leverage template addition and message building
5. **Dynamic Values**: Use callable partials for runtime values

The prompt system is designed for safety, flexibility, and composability. Understanding the internals helps you build better, more maintainable prompt templates.