Model Detection Demo
====================

.. tags:: tutorial, api, config

This page demonstrates the enhanced Jinja macros for automatically detecting and documenting dataclasses and Pydantic models.

Enhanced Model Documentation Macros
------------------------------------

Our custom Jinja macros can automatically detect and provide appropriate documentation for:

- **Pydantic Models**: Models that inherit from ``BaseModel`` or ``BaseSettings``
- **Python Dataclasses**: Classes decorated with ``@dataclass`` or with ``__dataclass_fields__``
- **Enums**: Classes that inherit from ``enum.Enum``
- **Regular Classes**: Standard Python classes with fallback documentation

Available Macros
-----------------

The following macros are available in ``_templates/cli-macros.html``:

detect_model_type(obj_module, obj_name, obj_info)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Automatically detects the model type and generates appropriate Sphinx directives:

.. code-block:: jinja

   {{ detect_model_type('base.config.settings', 'AppSettings', obj_info) }}

This would generate either:

- ``.. autopydantic_model::`` for Pydantic models with full field documentation
- ``.. autoclass::`` for dataclasses with field listings
- Standard ``.. autoclass::`` for regular classes

document_model_with_diagram(obj_module, obj_name, obj_info, show_diagram=True)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generates comprehensive documentation including inheritance diagrams:

.. code-block:: jinja

   {{ document_model_with_diagram('base.models', 'User', obj_info, true) }}

auto_document_object(obj_module, obj_name, obj_info, context="")
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Smart documentation that routes to the appropriate documentation method based on object type:

.. code-block:: jinja

   {{ auto_document_object('core.services', 'DataProcessor', obj_info, "Core Services") }}

Detection Helper Macros
~~~~~~~~~~~~~~~~~~~~~~~~

- ``is_pydantic_model(obj_module, obj_info)`` - Returns "True" if object is a Pydantic model
- ``is_dataclass(obj_info)`` - Returns "True" if object is a dataclass
- ``smart_model_doc(obj_module, obj_name, obj_info)`` - Provides smart documentation with type indicators

Example Usage in Templates
---------------------------

Here's how you might use these macros in an AutoAPI template:

.. code-block:: jinja

   {% extends "base.rst.jinja2" %}
   
   {% from "cli-macros.html" import smart_model_doc, is_pydantic_model, is_dataclass %}
   
   {% block content %}
   {% for obj in objects %}
     {% if obj.type == "class" %}
       {% if is_pydantic_model(obj.id, obj) == "True" %}
   
   🏗️ Pydantic Model: {{ obj.name }}
   {% elif is_dataclass(obj) == "True" %}
   
   📦 Dataclass: {{ obj.name }}
       {% endif %}
       
       {{ smart_model_doc(obj.id, obj.name, obj) }}
       
     {% endif %}
   {% endfor %}
   {% endblock %}

Benefits
--------

1. **Automatic Detection**: No manual configuration needed - detects model types from code structure
2. **Appropriate Documentation**: Uses the right Sphinx directive for each model type
3. **Enhanced Features**: Pydantic models get validation info, dataclasses get field listings
4. **Consistent Formatting**: Standardized documentation across all model types
5. **Template Reusability**: Macros can be used across multiple documentation templates

Integration with AutoAPI
-------------------------

These macros are designed to work with Sphinx AutoAPI and can be used in custom templates to enhance the automatic documentation generation.

.. note::

   The macros expect object information in the format provided by AutoAPI, including
   properties like ``bases``, ``dataclass_fields``, ``decorators``, and ``obj_type``.

Configuration
-------------

To use these macros, ensure that ``cli-macros.html`` is in your ``_templates`` directory and that your Sphinx configuration includes:

.. code-block:: python

   # conf.py
   templates_path = ["_templates", "_autoapi_templates"]
   
   # Enable Jinja2 extensions for advanced template features
   jinja_env_options = {"extensions": ["jinja2.ext.do"]}

.. tip::

   These macros work best when combined with ``sphinxcontrib.autodoc_pydantic`` for
   Pydantic model documentation and can complement ``sphinx-apischema`` when compatibility
   issues are resolved.