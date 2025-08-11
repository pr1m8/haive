Documentation Tools



The Haive framework includes tools to automate and streamline the documentation process. This page describes the available tools and how to use them.

Automatic Docstring Generator


----------------------------

The ``add_docstrings`.py`` script automatically adds Google-style docstrings to Python modules, classes, and functions based on naming conventions and context.

Location


~~~~~~~

The script is located at:

.. code-block:: bash

    /home/will/Projects/haive/backend/haive/packages/haive-games/scripts/add_docstrings.py

    Features




    - Analyzes Python files to find missing docstrings

    - Generates context-appropriate docstrings for modules, classes, and functions
    - Creates README.md files for game modules
    - Supports dry-run mode to preview changes without modifying files

    Usage




.. code-block:: bash

    # From the haive-games package directory

    # Add docstrings to all files
    python scripts/add_docstrings.py

    # Add docstrings to a specific module
    python scripts/add_docstrings.py --path src/haive/games/chess

    # Test what would be changed without modifying files
    python scripts/add_docstrings.py --dry-run

    Examples




    Running the script on a module without docstrings:

.. code-block:: bash

    python scripts/add_docstrings.py --path src/haive/games/chess

    Will add:

    1. Module-level docstrings` to`` __init__`.p``y`` and other Python files

    2. Class docstrings to classes` like`` ChessAgen``t``,` ``ChessStat``e``, etc.

    3. Function docstrings to methods and functions
    4. Create` a`` README`.m``d`` if one doesn't exist

    Documentation Templates




    The script uses templates to ensure consistent documentation. These templates are located in:

.. code-block:: bash

    /home/will/Projects/haive/backend/haive/packages/haive-games/scripts/templates/

    Available Templates




    1`.`` README_TEMPLATE`.m``d`` - Template for module-level README files

    2`.`` MODULE_DOCSTRING_TEMPLATE`.tx``t`` - Template for module-level docstrings

    Sphinx Integration




    The documentation tools are designed to work with Sphinx for generating API documentation.

    Building Documentation




.. code-block:: bash

    # From the project root
    nox -s docs

    # For live documentation editing with auto-reload
    nox -s docs-live

    # For checking documentation without building
    nox -s docs-check

    Custom Documentation Building




   ` The`` noxfile`.p``y`` in the project root provides several commands for documentation management:

    .. list-table::


    :header-rows: 1

    * - Command*

     - Description
    * *` -`` nox -s` doc``s`

``
     - Build documentation
    * *` -`` nox -s docs --` --clea``n`

``
     - Clean build and rebuild
    * *` -`` nox -s` docs-liv``e`

``
     - Start live server with auto-rebuild
    * *` -`` nox -s` docs-clea``n`

``
     - Clean all documentation builds
    * *` -`` nox -s` docs-chec``k`

``
     - Check documentation for errors

    Adding to Documentation Tools




    If you want to extend the documentation tools, you can:

    1. Add new templates to` the`` template``s`` directory

    2. Enhance` the`` add_docstrings`.p``y`` script with new docstring patterns

    3. Update the Sphinx configuration` in`` docs/source/conf`.p``y``*`

`
`
