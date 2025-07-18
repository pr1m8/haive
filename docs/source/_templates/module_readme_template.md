# {Module Name}

{Brief description of the module's purpose - one sentence}

## Overview

{Detailed explanation of what this module provides. Include the main purpose, key functionality, and how it fits into the larger Haive ecosystem.}

## Key Components

### Classes
- **{ClassName}**: {Brief description of the class and its purpose}
- **{ClassName}**: {Brief description of the class and its purpose}

### Functions
- **{function_name}()**: {Brief description of what the function does}
- **{function_name}()**: {Brief description of what the function does}

### Submodules
- **{submodule}**: {Brief description of the submodule}
- **{submodule}**: {Brief description of the submodule}

## Installation

This module is part of the `haive-{package}` package. Install it using:

```bash
pip install haive-{package}
```

## Usage Examples

### Basic Usage

```python
from haive.{module} import {Component}

# Initialize the component
component = {Component}()

# Use the component
result = component.{method}({parameters})
print(result)
```

### Advanced Usage

```python
from haive.{module} import {Component1}, {Component2}

# Example of more complex usage
config = {
    "option1": "value1",
    "option2": "value2"
}

component = {Component1}(config)
result = component.process(data)
```

## Configuration

{Describe any configuration options, environment variables, or settings that affect this module}

### Environment Variables
- `HAIVE_{MODULE}_CONFIG`: {Description}
- `HAIVE_{MODULE}_DEBUG`: {Description}

### Configuration Options
```python
{
    "option1": "default_value",  # Description
    "option2": 100,              # Description
}
```

## API Reference

For detailed API documentation, see the [API Reference](../api/{module}/index.rst).

### Quick Reference

#### {ClassName}
```python
class {ClassName}({BaseClass}):
    """Brief description."""
    
    def method1(self, param1: Type) -> ReturnType:
        """Brief description of method."""
        pass
```

## Best Practices

1. **{Practice 1}**: {Description of the best practice}
2. **{Practice 2}**: {Description of the best practice}
3. **{Practice 3}**: {Description of the best practice}

## Common Issues and Solutions

### Issue: {Common issue description}
**Solution**: {How to resolve the issue}

### Issue: {Common issue description}
**Solution**: {How to resolve the issue}

## See Also

- [`haive.{related_module1}`](../{related_module1}/): {Description of relationship}
- [`haive.{related_module2}`](../{related_module2}/): {Description of relationship}
- [User Guide: {Guide Name}](../../guides/{guide}.rst): {Description}

## Contributing

Contributions to this module are welcome! Please see the [Contributing Guide](../../development/contributing.rst) for more information.

## Changelog

See the [Changelog](../../reference/changelog.rst) for version history and updates.