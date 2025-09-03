{% if not obj.display %}
:orphan:
{% endif %}

:py:mod:`{{ obj.name }}`
========================

.. py:module:: {{ obj.name }}

{% if obj.docstring %}
.. autoapi-nested-parse::

   {{ obj.docstring|indent(3) }}

{% else %}
Package ``{{ obj.name }}``
{% endif %}

{% if obj.name.endswith('.agents') %}
.. admonition:: 🤖 Agent Package
   :class: tip

   This package contains AI agent implementations for various use cases and patterns.
   
   **Quick Start**:
   
   .. code-block:: python
   
      from {{ obj.name }} import SimpleAgent
      from haive.core.engine import AugLLMConfig
      
      agent = SimpleAgent(name="assistant", engine=AugLLMConfig())
      result = await agent.arun("Hello!")
      
{% elif obj.name.endswith('.tools') %}
.. admonition:: 🔧 Tools Package
   :class: tip

   This package contains tools and integrations that agents can use.
   
   **Quick Start**:
   
   .. code-block:: python
   
      from {{ obj.name }} import WebSearchTool
      from haive.agents import ReactAgent
      
      tool = WebSearchTool()
      agent = ReactAgent(name="researcher", tools=[tool])
      
{% elif obj.name.endswith('.core') %}
.. admonition:: ⚙️ Core Package
   :class: tip

   This package contains the core framework components that power the Haive system.
   
   **Quick Start**:
   
   .. code-block:: python
   
      from {{ obj.name }}.engine import AugLLMConfig
      from {{ obj.name }}.schema import StateSchema
      
{% endif %}

{% block subpackages %}
{% set visible_subpackages = obj.subpackages|selectattr("display")|list %}
{% if visible_subpackages %}
Subpackages
-----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

{% for subpackage in visible_subpackages %}
   {{ subpackage.name }}
{%- endfor %}

.. toctree::
   :maxdepth: 2
   :hidden:

{% for subpackage in visible_subpackages %}
   {{ subpackage.include_path }}
{%- endfor %}

{% endif %}
{% endblock %}

{% block submodules %}
{% set visible_submodules = obj.submodules|selectattr("display")|list %}
{% if visible_submodules %}
Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

{% for submodule in visible_submodules %}
   {{ submodule.name }}
{%- endfor %}

.. toctree::
   :maxdepth: 1
   :hidden:

{% for submodule in visible_submodules %}
   {{ submodule.include_path }}
{%- endfor %}

{% endif %}
{% endblock %}

{% block attributes %}
{% set visible_attributes = obj.attributes|selectattr("display")|list %}
{% if visible_attributes %}

Package Attributes
------------------

.. autosummary::
   :nosignatures:

{% for attribute in visible_attributes %}
   ~{{ obj.name }}.{{ attribute.short_name }}
{%- endfor %}

{% for attribute in visible_attributes %}
.. autodata:: {{ obj.name }}.{{ attribute.short_name }}
   :annotation:

   {% if attribute.docstring %}
   {{ attribute.docstring|indent(3) }}
   {% endif %}

{% endfor %}
{% endif %}
{% endblock %}

{% block functions %}
{% set visible_functions = obj.functions|selectattr("display")|list %}
{% if visible_functions %}

Package Functions
-----------------

.. autosummary::
   :nosignatures:
   :template: autosummary/function.rst

{% for function in visible_functions %}
   {{ obj.name }}.{{ function.short_name }}
{%- endfor %}

{% for function in visible_functions %}
.. autofunction:: {{ obj.name }}.{{ function.short_name }}
{% endfor %}
{% endif %}
{% endblock %}

{% block classes %}
{% set visible_classes = obj.classes|selectattr("display")|list %}
{% if visible_classes %}

Classes
-------

.. autosummary::
   :nosignatures:
   :template: autosummary/class.rst
   :toctree: _autosummary

{% for class in visible_classes %}
   {{ obj.name }}.{{ class.short_name }}
{%- endfor %}

Overview
^^^^^^^^

{% for class in visible_classes %}
.. autoclass:: {{ obj.name }}.{{ class.short_name }}
   :members:
   :show-inheritance:
   :noindex:

   {% if class.docstring %}
   {{ class.docstring|truncate(200)|indent(3) }}
   {% endif %}

{% endfor %}
{% endif %}
{% endblock %}

{% block exceptions %}
{% set visible_exceptions = obj.exceptions|selectattr("display")|list %}
{% if visible_exceptions %}

Exceptions
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/exception.rst

{% for exception in visible_exceptions %}
   {{ obj.name }}.{{ exception.short_name }}
{%- endfor %}

{% for exception in visible_exceptions %}
.. autoexception:: {{ obj.name }}.{{ exception.short_name }}
   :show-inheritance:
{% endfor %}
{% endif %}
{% endblock %}

Package Contents
----------------

{% if obj.all %}
.. rubric:: {{ obj.name }}.__all__

.. autosummary::
   :nosignatures:

{% for item in obj.all %}
   {{ obj.name }}.{{ item }}
{%- endfor %}

{% endif %}

.. automodule:: {{ obj.name }}
   :members:
   :undoc-members:
   :show-inheritance: