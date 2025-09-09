# Prompt Extraction Gap Analysis

**Date**: 2025-01-09
**Status**: 🔴 INCOMPLETE - Missing Critical Features

## What We Created vs What's Actually Needed

### ✅ What We Created

1. **PromptConfig** - Basic prompt configuration
2. **PromptLibrary** - Template storage and versioning
3. **PromptContract** - Variable validation

### ❌ What We Missed

## 1. Few-Shot Prompting (MISSING)

```python
# AugLLMConfig supports:
examples: List[Dict[str, str]]  # Few-shot examples
example_prompt: PromptTemplate  # Template for examples
prefix: str  # Text before examples
suffix: str  # Text after examples
example_separator: str  # Separator between examples

# Creates FewShotPromptTemplate or FewShotChatMessagePromptTemplate
```

## 2. Messages Placeholder Management (MISSING)

```python
# AugLLMConfig handles:
add_messages_placeholder: bool
messages_placeholder_name: str = "messages"
force_messages_optional: bool
optional_variables: List[str]

# Dynamic insertion of MessagesPlaceholder in ChatPromptTemplate
```

## 3. Dynamic Template Creation (MISSING)

```python
# AugLLMConfig creates templates from:
- System message only → ChatPromptTemplate
- Examples + prefix/suffix → FewShotPromptTemplate
- Examples + ChatPromptTemplate → FewShotChatMessagePromptTemplate
- Nothing → Default template with messages placeholder
```

## 4. Format Instructions Integration (MISSING)

```python
# AugLLMConfig features:
include_format_instructions: bool
format_instructions_key: str = "format_instructions"
use_tool_for_format_instructions: bool
get_format_instructions(model, as_tool)
add_format_instructions(model)
with_format_instructions(model)
```

## 5. Partial Variables Management (PARTIAL)

```python
# We have basic partial_variables dict
# But missing:
- Dynamic application based on template type
- Validation of partial variable compatibility
- Merging with format instructions
```

## 6. Template Storage and Switching (MISSING)

```python
# AugLLMConfig supports:
add_prompt_template(name, template)
use_prompt_template(name)
remove_prompt_template(name)
list_prompt_templates()
```

## 7. Input Variables Management (MISSING)

```python
# AugLLMConfig handles:
input_variables: List[str]
optional_variables: List[str]
_compute_input_variables()
_merge_input_variables()
```

## 8. Template Reconstruction from Dict (MISSING)

```python
# AugLLMConfig can reconstruct templates from:
- Serialized dict representations
- LangChain saved formats
- Custom message formats
```

## Complete PromptConfig Should Include:

```python
class EnhancedPromptConfig(BaseModel):
    """Complete prompt configuration matching AugLLMConfig capabilities."""

    # Basic templates
    prompt_template: Optional[BasePromptTemplate]
    system_message: Optional[str]

    # Few-shot prompting
    examples: List[Dict[str, str]] = Field(default_factory=list)
    example_prompt: Optional[PromptTemplate]
    prefix: Optional[str]
    suffix: Optional[str]
    example_separator: str = "\n\n"

    # Messages handling
    add_messages_placeholder: bool = True
    messages_placeholder_name: str = "messages"
    force_messages_optional: bool = False
    uses_messages_field: bool = False

    # Variables
    input_variables: List[str] = Field(default_factory=list)
    optional_variables: List[str] = Field(default_factory=list)
    partial_variables: Dict[str, Any] = Field(default_factory=dict)

    # Format instructions
    include_format_instructions: bool = True
    format_instructions_key: str = "format_instructions"
    use_tool_for_format_instructions: bool = False
    format_instructions_text: Optional[str] = None

    # Template management
    stored_templates: Dict[str, BasePromptTemplate] = Field(default_factory=dict)
    active_template_name: Optional[str] = None

    # Contracts (our addition)
    contracts: Dict[str, PromptContract] = Field(default_factory=dict)

    def create_template(self) -> BasePromptTemplate:
        """Create appropriate template based on configuration."""
        if self.prompt_template:
            return self.prompt_template

        if self.examples and self.example_prompt:
            if self.prefix and self.suffix:
                return self._create_few_shot_template()
            elif isinstance(self.example_prompt, ChatPromptTemplate):
                return self._create_few_shot_chat_template()

        if self.system_message:
            return self._create_chat_from_system()

        if self.add_messages_placeholder:
            return self._create_default_with_placeholder()

        return PromptTemplate.from_template("{input}")

    def _create_few_shot_template(self) -> FewShotPromptTemplate:
        """Create few-shot template with examples."""
        return FewShotPromptTemplate(
            examples=self.examples,
            example_prompt=self.example_prompt,
            prefix=self.prefix,
            suffix=self.suffix,
            example_separator=self.example_separator,
            input_variables=self.input_variables
        )

    def _create_few_shot_chat_template(self) -> FewShotChatMessagePromptTemplate:
        """Create few-shot chat template."""
        return FewShotChatMessagePromptTemplate(
            examples=self.examples,
            example_prompt=self.example_prompt,
            input_variables=self.input_variables
        )

    def _create_chat_from_system(self) -> ChatPromptTemplate:
        """Create chat template from system message."""
        messages = [
            ("system", self.system_message)
        ]

        if self.add_messages_placeholder:
            messages.append(
                MessagesPlaceholder(
                    variable_name=self.messages_placeholder_name,
                    optional=self.force_messages_optional
                )
            )

        messages.append(("human", "{input}"))
        return ChatPromptTemplate.from_messages(messages)

    def _create_default_with_placeholder(self) -> ChatPromptTemplate:
        """Create default template with messages placeholder."""
        return ChatPromptTemplate.from_messages([
            MessagesPlaceholder(
                variable_name=self.messages_placeholder_name,
                optional=True
            ),
            ("human", "{input}")
        ])

    def apply_partial_variables(self) -> None:
        """Apply partial variables to template."""
        if self.prompt_template and self.partial_variables:
            self.prompt_template = self.prompt_template.partial(**self.partial_variables)

    def add_format_instructions(self, model: type[BaseModel]) -> None:
        """Add format instructions for structured output."""
        if self.include_format_instructions:
            parser = PydanticOutputParser(pydantic_object=model)
            instructions = parser.get_format_instructions()
            self.partial_variables[self.format_instructions_key] = instructions
            self.format_instructions_text = instructions
            self.apply_partial_variables()

    def store_template(self, name: str, template: BasePromptTemplate) -> None:
        """Store a template for later use."""
        self.stored_templates[name] = template

    def use_template(self, name: str) -> None:
        """Switch to a stored template."""
        if name in self.stored_templates:
            self.prompt_template = self.stored_templates[name]
            self.active_template_name = name

    def compute_input_variables(self) -> List[str]:
        """Compute required input variables."""
        if self.prompt_template:
            return list(self.prompt_template.input_variables)
        return self.input_variables
```

## Impact of Missing Features

### 1. **Few-Shot Learning** - CRITICAL

- Cannot create few-shot prompts
- No example management
- Missing prefix/suffix support

### 2. **Chat Message Handling** - CRITICAL

- Cannot properly handle conversation history
- Missing messages placeholder management
- No optional message support

### 3. **Dynamic Template Creation** - HIGH

- Cannot auto-create templates from components
- Missing intelligent template selection
- No fallback template creation

### 4. **Format Instructions** - HIGH

- Cannot add structured output instructions
- Missing Pydantic parser integration
- No automatic instruction injection

### 5. **Template Storage** - MEDIUM

- Cannot switch between templates
- Missing template versioning within session
- No template reuse patterns

## Recommendation

We need to either:

1. **Enhance our PromptConfig** to include ALL these features
2. **Create specialized configs**:
   - `FewShotPromptConfig`
   - `ChatPromptConfig`
   - `FormatInstructionConfig`
   - `TemplateManagerConfig`

3. **Keep some complexity in AugLLMConfig** for prompt orchestration

The current extraction is only ~30% complete for prompts. We got tools mostly right, but prompts need significant expansion.
