{% from "cli-macros.html" import auto_cli, cli_detect_and_document, smart_prompt %}

Automatic CLI Documentation
============================

This page demonstrates automatic CLI documentation detection using `sphinx-argparse` and Jinja templates.

Automatic Detection Demo
------------------------

Using our Jinja macro to automatically detect and document CLI scripts:

{{ cli_detect_and_document('scripts/build-docs', 'Enhanced documentation builder with error reporting and debugging capabilities.') }}

Smart Prompt Detection
-----------------------

Our `smart_prompt` macro automatically detects command types and applies appropriate formatting:

**Bash Command:**
{{ smart_prompt('$ poetry install --with docs') }}

**Python REPL:**
{{ smart_prompt('>>> from pyautodoc import DocumentationBuilder') }}

**Comment/Script:**
{{ smart_prompt('# This is a comment or script line') }}

**Generic Text:**
{{ smart_prompt('some generic command or text') }}

Direct CLI Integration
----------------------

You can also use the `auto_cli` macro directly for more control:

{{ auto_cli('scripts.build-docs', 'get_argument_parser', 'build-docs.py', 'Direct integration example with custom description and enhanced error reporting.') }}

Manual Sphinx-Prompt Examples
------------------------------

Traditional sphinx-prompt usage for comparison:

**Basic Bash:**

.. prompt:: bash

   $ python scripts/build-docs.py --help

**Python Session:**

.. prompt:: python

   >>> import subprocess
   >>> result = subprocess.run(['python', 'scripts/build-docs.py', '--quiet'])
   >>> print(f"Exit code: {result.returncode}")
   Exit code: 0

**Multi-line Commands:**

.. prompt:: bash

   $ python scripts/build-docs.py \
       --builder html \
       --source docs/source \
       --build docs/build

Benefits of Auto-Detection
---------------------------

1. **Consistency**: Automatic formatting ensures all CLI documentation looks the same
2. **Maintenance**: Changes to CLI arguments are automatically reflected in docs
3. **Accuracy**: No risk of manual documentation being out of sync
4. **Efficiency**: Less manual work to document CLI tools

Usage in Templates
------------------

To use these macros in your own documentation:

.. code-block:: jinja

   {% from "cli-macros.html" import auto_cli, smart_prompt %}
   
   {# Automatic CLI documentation #}
   {{ auto_cli('mymodule.cli', 'get_parser', 'mycli.py', 'Description here') }}
   
   {# Smart prompt detection #}
   {{ smart_prompt('$ some command here') }}

This approach combines the power of `sphinx-argparse` for automatic argument parsing with the flexibility of Jinja templates for consistent formatting.