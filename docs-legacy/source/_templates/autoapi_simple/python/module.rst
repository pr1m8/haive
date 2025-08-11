{% if not obj.display %}
:orphan:
{% endif %}

{{ obj.name }}
{{ "=" * obj.name|length }}

.. py:module:: {{ obj.name }}

{% if obj.docstring %}
.. autoapi-nested-parse::

   {{ obj.docstring|indent(3) }}

{% endif %}

{% block subpackages %}
{% set visible_subpackages = obj.subpackages|selectattr("display")|list %}
{% if visible_subpackages %}
Subpackages
-----------

.. toctree::
   :maxdepth: 1

{% for subpackage in visible_subpackages %}
   {{ subpackage.include_path }}
{%- endfor %}

{% for subpackage in visible_subpackages %}
   * :py:mod:`{{ subpackage.name }}` - {{ subpackage.summary|default("Subpackage", true) }}
{%- endfor %}

{% endif %}
{% endblock %}

{% block submodules %}
{% set visible_submodules = obj.submodules|selectattr("display")|list %}
{% if visible_submodules %}
Submodules
----------

.. toctree::
   :maxdepth: 1

{% for submodule in visible_submodules %}
   {{ submodule.include_path }}
{%- endfor %}

{% for submodule in visible_submodules %}
   * :py:mod:`{{ submodule.name }}` - {{ submodule.summary|default("Submodule", true) }}
{%- endfor %}

{% endif %}
{% endblock %}

{% block attributes %}
{% set visible_attributes = obj.attributes|selectattr("display")|list %}
{% if visible_attributes %}
Module Attributes
-----------------

{% for attribute in visible_attributes %}
.. py:data:: {{ attribute.name }}
   :type: {{ attribute.type|default("", true) }}
   {% if attribute.value %}
   :value: {{ attribute.value|truncate(50) }}
   {% endif %}

   {% if attribute.docstring %}
   {{ attribute.docstring|indent(3) }}
   {% else %}
   {{ attribute.summary|default("Module attribute", true) }}
   {% endif %}

{% endfor %}
{% endif %}
{% endblock %}

{% block functions %}
{% set visible_functions = obj.functions|selectattr("display")|list %}
{% if visible_functions %}
Functions
---------

{% for function in visible_functions %}
   {{ function.name }}
{%- endfor %}

{% for function in visible_functions %}
.. autofunction:: {{ function.name }}
{% endfor %}
{% endif %}
{% endblock %}

{% block classes %}
{% set visible_classes = obj.classes|selectattr("display")|list %}
{% if visible_classes %}
Classes
-------

{% for class in visible_classes %}
* :py:class:`{{ class.name }}` - {{ class.summary|default("Class", true) }}
{%- endfor %}

.. toctree::
   :hidden:
   :maxdepth: 1

{% for class in visible_classes %}
   {{ class.include_path }}
{%- endfor %}
{% endif %}
{% endblock %}

{% block exceptions %}
{% set visible_exceptions = obj.exceptions|selectattr("display")|list %}
{% if visible_exceptions %}
Exceptions
----------

{% for exception in visible_exceptions %}
.. py:exception:: {{ exception.name }}

   {% if exception.bases %}
   Bases: {% for base in exception.bases %}{{ base }}{% if not loop.last %}, {% endif %}{% endfor %}
   {% endif %}

   {% if exception.docstring %}
   {{ exception.docstring|indent(3) }}
   {% else %}
   {{ exception.summary|default("Exception class", true) }}
   {% endif %}

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
   {{ item }}
{%- endfor %}

.. automodule:: {{ obj.name }}
   :members:
   :show-inheritance:
{% endif %}