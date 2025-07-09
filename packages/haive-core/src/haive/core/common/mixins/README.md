# Haive Core Mixins

A collection of powerful mixins that add specialized functionality to engine classes through multiple inheritance. These mixins follow composition-over-inheritance principles to provide modular, reusable capabilities.

## Overview

Mixins in Haive Core provide a clean way to add complex functionality to engine classes without requiring deep inheritance hierarchies. Each mixin is designed to be:

- **Non-invasive**: Preserves existing functionality
- **Composable**: Works with other mixins and base classes
- **Configurable**: Behavior can be customized and disabled
- **Well-integrated**: Follows Haive's architectural patterns

## Available Mixins

### PromptTemplateMixin

Advanced prompt template integration for any engine class.

```python
from haive.core.common.mixins.prompt_template_mixin import PromptTemplateMixin

class MyEngine(PromptTemplateMixin, InvokableEngine):
    prompt_template: Optional[BasePromptTemplate] = None
```

**Features:**

- Automatic input schema derivation from prompt templates
- Intelligent schema composition with existing schemas
- Prompt template validation and preprocessing
- Support for both text and chat templates
- Configurable behavior and graceful fallbacks

**Key Methods:**

- `derive_input_schema()` - Enhanced to include prompt variables
- `get_prompt_engine()` - Access to underlying PromptTemplateEngine
- `format_prompt()` - Format templates with input data
- `compose_with_prompt_schema()` - Intelligent schema composition

### StructuredOutputMixin

Adds structured output capabilities with Pydantic model generation.

```python
from haive.core.common.mixins.structured_output_mixin import StructuredOutputMixin

class MyEngine(StructuredOutputMixin, InvokableEngine):
    output_schema: Optional[Type[BaseModel]] = None
```

**Features:**

- Automatic output schema derivation
- Support for multiple structured output versions
- Integration with LLM tool calling
- Format instruction generation
- Output parsing and validation

### ToolRouteMixin

Enables tool routing and management capabilities.

```python
from haive.core.common.mixins.tool_route_mixin import ToolRouteMixin

class MyEngine(ToolRouteMixin, InvokableEngine):
    tools: List[BaseTool] = Field(default_factory=list)
```

**Features:**

- Tool registration and management
- Route-based tool selection
- Tool schema integration
- Automatic tool binding for LLMs
- Tool call validation and execution

## Usage Patterns

### Single Mixin

```python
class SimpleEngine(PromptTemplateMixin, InvokableEngine):
    prompt_template: Optional[BasePromptTemplate] = None

    def invoke(self, input_data):
        # Custom logic here
        return self.format_prompt(input_data)
```

### Multiple Mixins

```python
class AdvancedEngine(
    PromptTemplateMixin,
    StructuredOutputMixin,
    ToolRouteMixin,
    InvokableEngine
):
    prompt_template: Optional[BasePromptTemplate] = None
    output_schema: Optional[Type[BaseModel]] = None
    tools: List[BaseTool] = Field(default_factory=list)

    # All mixin capabilities are available
```

### AugLLMConfig Integration

The primary example of comprehensive mixin usage:

```python
class AugLLMConfig(
    PromptTemplateMixin,
    StructuredOutputMixin,
    ToolRouteMixin,
    InvokableEngine[...]
):
    # Combines all mixin capabilities for powerful LLM configuration
    pass
```

## Mixin Design Principles

### 1. Method Override Pattern

Mixins use safe method override patterns:

```python
def derive_input_schema(self) -> Optional[Type[BaseModel]]:
    # Try parent class implementation first
    parent_schema = None
    if hasattr(super(), 'derive_input_schema'):
        try:
            parent_schema = super().derive_input_schema()
        except:
            pass

    # Add mixin functionality
    if self.should_enhance():
        return self.enhance_schema(parent_schema)

    return parent_schema
```

### 2. Graceful Error Handling

All mixins include comprehensive error handling:

```python
try:
    enhanced_result = self.enhance_functionality()
    return enhanced_result
except Exception:
    # Fall back to original behavior
    return original_result
```

### 3. Configuration Controls

Mixins provide configuration options:

```python
class MyMixin:
    _enable_feature: bool = True

    def enhanced_method(self):
        if not self._enable_feature:
            return super().enhanced_method()
        # Enhanced functionality
```

## Integration Guidelines

### Field Requirements

When using mixins, ensure required fields are defined:

```python
class MyEngine(PromptTemplateMixin, InvokableEngine):
    # Required by PromptTemplateMixin
    prompt_template: Optional[BasePromptTemplate] = None

    # Optional configuration
    _use_prompt_for_input_schema: bool = True
```

### Method Resolution Order (MRO)

Consider method resolution order with multiple mixins:

```python
# Correct order: specific to general
class MyEngine(
    SpecificMixin,      # Most specific
    GeneralMixin,       # More general
    InvokableEngine     # Base class
):
    pass
```

### Configuration Management

Manage mixin configuration consistently:

```python
engine = MyEngine(
    prompt_template=template,
    output_schema=MySchema,
    tools=[tool1, tool2],
    _use_prompt_for_input_schema=True  # Mixin config
)
```

## Testing Mixins

### Unit Testing

Test mixin functionality in isolation:

```python
def test_prompt_template_mixin():
    class TestEngine(PromptTemplateMixin, InvokableEngine):
        prompt_template: Optional[BasePromptTemplate] = None

    engine = TestEngine(prompt_template=template)
    schema = engine.derive_input_schema()
    assert 'prompt_variable' in schema.model_fields
```

### Integration Testing

Test mixin combinations:

```python
def test_multiple_mixins():
    class CombinedEngine(
        PromptTemplateMixin,
        StructuredOutputMixin,
        InvokableEngine
    ):
        # Test that mixins work together
        pass
```

## Best Practices

1. **Order Matters**: Place mixins before base classes in inheritance
2. **Field Validation**: Use Pydantic validators for mixin fields
3. **Documentation**: Document required fields and configuration options
4. **Error Handling**: Implement graceful fallbacks for all enhanced methods
5. **Testing**: Test both individual mixins and combinations
6. **Configuration**: Provide clear configuration options and defaults

## Performance Considerations

- **Lazy Initialization**: Mixins should initialize expensive resources lazily
- **Caching**: Cache computed results where appropriate
- **Method Call Overhead**: Minimize overhead in frequently called methods
- **Memory Usage**: Be mindful of additional state stored by mixins

## Extending Mixins

### Creating New Mixins

Follow the established patterns:

```python
class MyNewMixin:
    """Docstring with examples and usage."""

    # Required fields that subclasses must define
    my_field: Optional[SomeType]

    # Configuration options
    _enable_my_feature: bool = True

    def enhance_existing_method(self) -> ReturnType:
        """Override with safe pattern."""
        # Get parent result
        parent_result = None
        if hasattr(super(), 'enhance_existing_method'):
            try:
                parent_result = super().enhance_existing_method()
            except:
                pass

        # Add enhancement if enabled
        if self._enable_my_feature and self.my_field:
            return self._apply_enhancement(parent_result)

        return parent_result
```

## Troubleshooting

### Common Issues

1. **MRO Conflicts**: Resolve by reordering inheritance
2. **Missing Fields**: Ensure all required mixin fields are defined
3. **Configuration Conflicts**: Use clear naming for mixin-specific settings
4. **Method Override Issues**: Follow the safe override pattern

### Debugging Tips

- Use `super()` calls to understand inheritance chain
- Check `__mro__` attribute to see method resolution order
- Test mixins individually before combining
- Use logging to trace method calls through inheritance chain

## API Reference

See individual mixin files for complete API documentation including all methods, fields, and configuration options.
