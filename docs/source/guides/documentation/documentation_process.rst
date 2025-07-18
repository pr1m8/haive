Documentation Process
=====================

This guide outlines the recommended process for maintaining and updating documentation in the Haive framework.

Documentation Lifecycle

-----------------------

The documentation process follows these key steps:

1. **Code Implementatio***n**: Write code with initial docstrings

2.*** **Automated Enhancemen***t**: Run documentation tools to fill gaps

3.*** **Manual Revie***w**: Review and enhance generated documentation
4.*** **Documentation Buildin***g**: Build documentation with Sphinx
5.*** **Review and Testin***g**: Review built documentation for accuracy
6.*** **Deploymen***t**: Update public documentation

Starting with New Code

----------------------

When creating new modules or classes:

1.*** **Write Basic Docstring***s**: Include brief descriptions for modules, classes, and functions

2.*** **Run Automated Tool***s**: Use the ``add_docstrings.p``y`` script to expand docstrings

3.*** **Create README***s**: Either manually or using the automated tools
4.*** **Build and Revie***w**: Ensure documentation builds correctly

.. code-block:: bash

    # After implementing a new module
    python scripts/add_docstrings.py --path src/haive/games/new_game
    nox -s docs

Updating Existing Documentation

-------------------------------

When updating existing code:

1.*** **Update Code Docstring***s**: Ensure docstrings reflect the current behavior

2.*** **Check for Consistenc***y**: Make sure documentation follows the established patterns

3.*** **Rebuild Documentatio***n**: Verify changes are reflected in the built docs

.. code-block:: bash

    # After updating code
    nox -s docs-check
    nox -s docs

Documentation Review Checklist

------------------------------

Before considering documentation complete, check:

1.*** **Completenes***s**: All modules, classes, and functions have docstrings

2.*** **Example***s**: Usage examples are provided and working

3.*** **Accurac***y**: Documentation matches actual code behavior
4.*** **Formattin***g**: Google-style docstring format is followed
5.*** **Module README***s**: Each module has a README with overview and usage
6.*** **Cross-reference***s**: Documentation properly links related concepts
7.*** **Builds Successfull***y**: Documentation builds without errors

Documentation Quality Levels

----------------------------

Haive uses three levels of documentation quality:

.. list-table::
   :header-rows: 1

  *** * - Level
     - Description
     - Requirements
  * * -* **Basi***c**
     - Minimum acceptable level
     - All public APIs have brief docstrings, README exists
  *** * -* **Standar***d**
     - Expected quality level
     - Complete docstrings with examples, comprehensive README
  *** * -* **Complet***e**
     - Highest quality level
     - Extended examples, cross-references, diagrams, tutorials

Best Practices

--------------

1.*** **Document as You Cod***e**: Write docstrings while implementing features

2.*** **Run Tools Regularl***y**: Integrate documentation tools into your workflow

3.*** **Check Documentation Build***s**: Verify Sphinx builds successfully
4.*** **Review Rendered Outpu***t**: Check how documentation looks when built
5.*** **Keep READMEs Update***d**: Update module READMEs when adding features
6.*** **Think About New User***s**: Documentation should guide new users effectively

Handling Breaking Changes

-------------------------

When making breaking changes:

1.*** **Update All Docstring***s**: Ensure all affected docstrings reflect the changes

2.*** **Update Example***s**: Make sure all examples work with the new API

3.*** **Highlight Change***s**: Note breaking changes prominently in documentation
4.*** **Version Documentatio***n**: Consider maintaining documentation for older versions

Documentation Roadmap

---------------------

For larger documentation improvements:

1.*** **Assessmen***t**: Evaluate current documentation coverage and quality

2.*** **Prioritizatio***n**: Identify critical areas for improvement

3.*** **Plannin***g**: Develop a plan with specific tasks and timelines
4.*** **Implementatio***n**: Execute the plan, starting with high-priority items
5.*** **Revie***w**: Regularly review progress and adjust the plan as needed

Troubleshooting Documentation Issues

------------------------------------

Common documentation issues and solutions:

1.*** **Missing docstring***s**: Run the automated docstring generator

2.*** **Sphinx build error***s**: Check the error log and fix the specific issues

3.*** **Inconsistent formattin***g**: Review against the style guide and correct
4.*** **Outdated example***s**: Update examples to match current code behavior
5.*** **Documentation doesn't match cod***e**: Update docstrings to reflect current implementation``***