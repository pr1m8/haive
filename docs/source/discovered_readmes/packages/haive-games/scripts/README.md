# Haive Games Documentation Scripts

This directory contains scripts for maintaining and enhancing documentation in the haive-games package.

## Available Scripts

### `add_docstrings.py`

Automatically adds Google-style docstrings to Python modules, classes, and functions in the haive-games package.

#### Features:

- Adds module-level docstrings to describe overall functionality
- Adds class docstrings with attributes and examples
- Adds function docstrings with arguments, return values, and examples
- Creates README.md files for game modules
- Intelligently generates documentation based on naming conventions and context

#### Usage:

```bash
# Add docstrings to all files (default path)
./add_docstrings.py

# Add docstrings to a specific module
./add_docstrings.py --path ../src/haive/games/chess

# Test what would be changed without modifying files
./add_docstrings.py --dry-run
```

## Documentation Standards

All documentation in the haive-games package follows these guidelines:

1. **Module-level docstrings**:

   ```python
   """
   Module Name and Brief Description

   Detailed description of the module's purpose and functionality.
   Any important details about usage, requirements, or limitations.

   Example:
       >>> from module import function
       >>> result = function()
       >>> print(result)
   """
   ```

2. **Class docstrings**:

   ```python
   class ClassName:
       """
       Brief description of the class.

       Detailed description of the class's purpose and functionality.

       Attributes:
           attr1 (type): Description of attribute 1.
           attr2 (type): Description of attribute 2.
       """
   ```

3. **Method/Function docstrings**:

   ```python
   def function_name(param1, param2=default):
       """
       Brief description of the function.

       Args:
           param1 (type): Description of parameter 1.
           param2 (type, optional): Description of parameter 2. Defaults to default.

       Returns:
           type: Description of the return value.

       Raises:
           Exception: Description of when this exception is raised.
       """
   ```

4. **Pydantic Models**:

   ```python
   class ModelName(BaseModel):
       """
       Brief description of the model.

       Attributes:
           field1 (type): Description of field 1.
           field2 (type): Description of field 2.
       """
       field1: type = Field(..., description="Description of field 1")
       field2: type = Field(default, description="Description of field 2")
   ```

## Integration with Sphinx

These docstrings are designed to work with Sphinx for generating API documentation. To build the documentation:

```bash
# From the project root
nox -s docs
```

This will process all docstrings and generate API documentation for the entire project.
