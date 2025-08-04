from __future__ import annotations
"""Template for __init__.py module docstrings following Google style guide.

Copy this template and customize it for each module's __init__.py file.
"""
# Example 1: Simple module
"""Simple module name - Brief one-line description.

This module provides functionality for [specific purpose]. It includes
classes and functions for [main use cases].

Example:
    Basic usage::

        from haive.module import MainClass

        instance = MainClass()
        result = instance.process(data)
"""
# Example 2: Complex module with multiple components
"""Module name - Brief one-line description.

This module provides [detailed functionality description]. It is designed to
[purpose and primary use cases]. The module integrates with [other components]
to provide [key capabilities].

The module is organized into the following submodules:
    * submodule1: Handles [functionality]
    * submodule2: Provides [functionality]
    * submodule3: Implements [functionality]

Key Features:
    * Feature 1: [Description of what it does and why it's useful]
    * Feature 2: [Description of what it does and why it's useful]
    * Feature 3: [Description of what it does and why it's useful]

Example:
    Basic usage example::

        from haive.module import Component1, Component2

        # Initialize components
        comp1 = Component1(config={'key': 'value'})
        comp2 = Component2()

        # Process data
        intermediate = comp1.process(input_data)
        result = comp2.transform(intermediate)

    Advanced usage with configuration::

        from haive.module import Pipeline
        from haive.module.config import PipelineConfig

        # Configure pipeline
        config = PipelineConfig(
            steps=['preprocess', 'analyze', 'postprocess'],
            parallel=True
        )

        # Create and run pipeline
        pipeline = Pipeline(config)
        results = pipeline.run(data_batch)

Attributes:
    DEFAULT_CONFIG (dict): Default configuration values
    SUPPORTED_TYPES (list): List of supported data types
    VERSION (str): Current module version

Note:
    This module requires [dependencies or prerequisites].
    For production use, ensure [specific configuration or setup].

Warnings:
    * [Any important warnings about usage]
    * [Potential issues to be aware of]

See Also:
    :mod:`haive.related_module1`: [Description of relationship]
    :mod:`haive.related_module2`: [Description of relationship]
    :class:`haive.module.MainClass`: Main class for this module

References:
    * [Link to documentation or paper]
    * [Link to related resources]
"""
# Example 3: Package-level __init__.py
"""Haive {Package} - Brief description of the package.

The haive-{package} package provides [overall functionality]. This package
includes modules for [list main areas of functionality].

Modules:
    * module1: [Brief description]
    * module2: [Brief description]
    * module3: [Brief description]

The package follows these design principles:
    1. [Principle 1]
    2. [Principle 2]
    3. [Principle 3]

Quick Start:
    Install the package::

        pip install haive-{package}

    Basic usage::

        from haive.{package} import MainComponent

        component = MainComponent()
        result = component.execute(task)

For detailed documentation, see the package README and API reference.
"""
# Example 4: Submodule with specific focus
"""Submodule name - Specific functionality provider.

This submodule implements [specific functionality] for the parent module.
It provides specialized classes and functions for [use case].

Classes:
    * SpecializedClass: [What it does]
    * HelperClass: [What it does]

Functions:
    * process_data(): [What it does]
    * validate_input(): [What it does]

The submodule is designed to work with [specific data types or formats]
and integrates with [other components].

Example:
    >>> from haive.module.submodule import SpecializedClass
    >>> processor = SpecializedClass(mode='advanced')
    >>> output = processor.run(input_data)

Technical Details:
    This implementation uses [algorithm/approach] to achieve
    [performance characteristic]. The core algorithm has
    O(n) time complexity and O(1) space complexity.

Limitations:
    * [Limitation 1]
    * [Limitation 2]
"""
# Template structure to follow:
"""
Required sections:

1. Module name - One-line description
2. Extended description paragraph
3. Example section with code
4. (Optional) Key Features/Attributes/Classes/Functions lists
5. (Optional) Note/Warning sections
6. (Optional) See Also section

Guidelines:
- Keep the one-line description under 80 characters
- Use present tense ("provides" not "will provide")
- Include practical examples that can be copy-pasted
- List actual module contents in attributes/classes/functions
- Cross-reference related modules with :mod: syntax
- Use Google-style formatting throughout
"""
