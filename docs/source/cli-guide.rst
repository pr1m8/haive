{% from "cli-macros.html" import cli_command, cli_multiline, cli_with_output, python_repl, install_guide %}

PyAutoDoc CLI Guide
===================

This guide covers using PyAutoDoc's command-line interface for documentation generation.

{{ install_guide("PyAutoDoc", [
    {
        "name": "Poetry (Recommended)",
        "command": "poetry install --with docs",
        "note": "Installs all dependencies including optional documentation tools."
    },
    {
        "name": "pip",
        "command": "pip install pyautodoc[docs]",
        "note": "Basic installation with documentation dependencies."
    }
]) }}

Quick Start
-----------

**Basic Documentation Build:**

{{ cli_command("poetry run sphinx-build -b html docs/source docs/build") }}

**Live Development Server:**

{{ cli_command("poetry run sphinx-autobuild docs/source docs/build --host 0.0.0.0 --port 8000") }}

**Enhanced Build with Error Reporting:**

{{ cli_command("python scripts/build-docs.py") }}

Common Commands
---------------

**Clean Build:**

{{ cli_multiline([
    "rm -rf docs/build",
    "poetry run sphinx-build -b html docs/source docs/build"
]) }}

**Check for Warnings:**

{{ cli_command("poetry run sphinx-build -b html -W docs/source docs/build") }}

**Build Multiple Formats:**

{{ cli_multiline([
    "poetry run sphinx-build -b html docs/source docs/build/html", 
    "poetry run sphinx-build -b latex docs/source docs/build/latex",
    "poetry run sphinx-build -b epub docs/source docs/build/epub"
]) }}

Python API Usage
----------------

You can also use PyAutoDoc programmatically:

{{ python_repl([
    {
        "input": "from pyautodoc import DocumentationBuilder",
        "output": ""
    },
    {
        "input": "builder = DocumentationBuilder('src/', 'docs/source')",
        "output": ""
    },
    {
        "input": "builder.build()",
        "output": "✅ Documentation built successfully!"
    }
]) }}

Configuration
-------------

**Basic conf.py setup:**

.. code-block:: python

   # Minimal configuration
   extensions = [
       'autoapi.extension',
       'sphinx.ext.napoleon',
       'sphinx_copybutton',
       'sphinx_prompt'
   ]
   
   autoapi_dirs = ['../../src']
   autoapi_type = 'python'

Advanced Usage
--------------

**Custom Build Script:**

{{ cli_with_output(
    "python scripts/build-docs.py --builder html --source docs/source --build docs/build",
    "🏗️  Building Sphinx documentation...\n📁 Source: docs/source\n📁 Build:  docs/build\n✅ Build successful!"
) }}

**Watch for Changes:**

{{ cli_command("poetry run sphinx-autobuild docs/source docs/build --ignore '*.swp' --ignore '*.tmp'") }}

Troubleshooting
---------------

**Extension Import Error:**

Problem: ``Could not import extension sphinxcontrib.needs``

Solution:

{{ cli_command("poetry install --with docs") }}

Make sure all documentation dependencies are installed.

**Build Failures:**

Problem: Sphinx build fails with cryptic errors

Solution:

{{ cli_command("python scripts/build-docs.py") }}

Use our enhanced build script for better error reporting with context and line numbers.