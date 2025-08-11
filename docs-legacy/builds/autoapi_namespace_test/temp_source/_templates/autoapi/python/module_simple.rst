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

{% endif %}
{% endblock %}

{% block functions %}
{% set visible_functions = obj.functions|selectattr("display")|list %}
{% if visible_functions %}
Functions
---------

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
.. autoclass:: {{ class.name }}
   :members:
   :show-inheritance:
   :inherited-members:
   :special-members: __init__

   {% if class.docstring %}
   {{ class.docstring|indent(3) }}
   {% endif %}

{% endfor %}
{% endif %}
{% endblock %}

{% block exceptions %}
{% set visible_exceptions = obj.exceptions|selectattr("display")|list %}
{% if visible_exceptions %}
Exceptions
----------

{% for exception in visible_exceptions %}
.. autoexception:: {{ exception.name }}
   :show-inheritance:
{% endfor %}
{% endif %}
{% endblock %}

{% block attributes %}
{% set visible_attributes = obj.attributes|selectattr("display")|list %}
{% if visible_attributes %}
Module Attributes
-----------------

{% for attribute in visible_attributes %}
.. autoattribute:: {{ attribute.name }}
   :annotation:

   {% if attribute.docstring %}
   {{ attribute.docstring|indent(3) }}
   {% endif %}

{% endfor %}
{% endif %}
{% endblock %}

Package Contents
----------------

{% if obj.all %}
.. rubric:: {{ obj.name }}.__all__

{% for item in obj.all %}
* **{{ item }}**
{%- endfor %}

.. automodule:: {{ obj.name }}
   :members:
   :show-inheritance:
{% endif %}