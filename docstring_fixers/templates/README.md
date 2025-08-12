# Docstring Templates

This directory contains Jinja2 templates for generating docstrings with the doq tool.

## Available Templates

### module.j2

Template for module-level docstrings (D100 fixes). Variables available:

- `module_name`: Name of the module
- `has_classes`, `has_functions`: Boolean flags
- `class_count`, `function_count`: Number of classes/functions
- `main_classes`, `main_functions`: List of main components
- `has_main`: Whether module has a main() function
- `purpose`: Module purpose description

### init.j2

Template for `__init__` method docstrings (D107 fixes). Variables:

- `class_name`: Name of the containing class
- `args`: List of arguments with name, annotation, description, default
- `attributes`: Instance attributes created
- `raises`: Exceptions that may be raised
- `examples`: Usage examples

### function.j2

Template for function docstrings. Variables:

- `function_name`: Function name
- `function_description`: Brief description
- `args`, `returns`, `yields`, `raises`: Function signature details
- `examples`: Usage examples with input/output

### class.j2

Template for class docstrings. Variables:

- `class_name`: Class name
- `base_classes`: List of parent classes
- `attributes`: Class attributes
- `class_methods`, `properties`: Class members

### method.j2

Template for method docstrings. Variables:

- `method_name`: Method name
- `is_property_setter`, `is_property_getter`: Property method flags
- `is_magic_method`: Magic method flag
- Standard function variables (args, returns, etc.)

## Using Custom Templates

### 1. Configure in pyproject.toml

```toml
[tool.doq]
template_path = "docstring_fixers/templates"
formatter = "custom"  # Use custom templates
```

### 2. Configure per-file with CLI

```bash
doq --template_path=docstring_fixers/templates --formatter=custom myfile.py
```

### 3. Use with our fixers

```python
from docstring_fixers.d100_d107_configurable_fixer import ConfigurableDocstringFixer

fixer = ConfigurableDocstringFixer()
result = fixer.fix_file(Path("myfile.py"))
```

## Template Customization

You can customize these templates by:

1. Editing the existing templates to match your style guide
2. Adding new variables in the template context
3. Creating conditional sections for different scenarios
4. Using Jinja2 filters for text transformation

## Example Context Data

The fixer analyzes your Python code and provides context like:

```python
{
    "module_name": "data_processor",
    "has_classes": True,
    "class_count": 3,
    "main_classes": [
        {"name": "DataProcessor", "description": "Main processing class"},
        {"name": "DataValidator", "description": "Validation utilities"}
    ],
    "has_functions": True,
    "function_count": 5,
    "purpose": "data processing and validation"
}
```

## Tips

1. Keep templates concise but informative
2. Use sensible defaults for missing information
3. Follow your project's docstring style guide
4. Test templates on sample files before bulk application
5. Use the `|default()` filter for optional fields
