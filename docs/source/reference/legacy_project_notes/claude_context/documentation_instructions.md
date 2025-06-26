# Haive Tools Documentation Instructions

This document provides instructions for completing the documentation of all tools and toolkits in the haive-tools package.

## Overview

The goal is to add comprehensive Google-style docstrings to all modules, classes, methods, and functions in the haive-tools package. These docstrings will be used by Sphinx to generate API documentation.

## Documentation Format

All documentation should follow these guidelines:

1. **Module-level docstrings**:

   ```python
   """
   Module Name and Brief Description

   Detailed description of the module's purpose and functionality.
   Any important details about usage, requirements, or limitations.

   Examples:
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

## Process for Documenting Each File

1. **Understand the file**: Read through the file to understand what it does, what APIs it interacts with, and how it's used.

2. **Add module-level docstring**: Add a comprehensive module-level docstring that explains the purpose of the file and includes usage examples.

3. **Document models**: Add docstrings to all Pydantic models and ensure each field has a description using the Field class.

4. **Document functions**: Add docstrings to all functions, including Args, Returns, and Raises sections.

5. **Document classes**: Add docstrings to all classes, including Attributes sections.

6. **Update tool/toolkit definitions**: Ensure the tool/toolkit definitions have clear and detailed descriptions.

## Templates

Use the templates provided in the `tools_documentation_checklist.md` file as a starting point for each file type.

## Tracking Progress

Use the checklist in `tools_documentation_checklist.md` to track progress. Mark each file as complete when documentation has been added.

## Examples

See the following files for examples of well-documented tools and toolkits:

1. `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/corporate_bs_tool.py`
2. `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/chuck_norris_jokes_toolkit.py`
3. `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/dev/shell/shell.py`
4. `/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/toolkits/jira_toolkit.py`

## Additional Resources

- Google Python Style Guide: https://google.github.io/styleguide/pyguide.html
- Sphinx Napoleon Extension: https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
- Pydantic Documentation: https://docs.pydantic.dev/latest/
- LangChain Documentation: https://python.langchain.com/docs/get_started/introduction
