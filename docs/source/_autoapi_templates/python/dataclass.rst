{# Enhanced template for dataclasses using sphinx-apischema #}
{% if not obj.display %}:orphan:{% endif %}

{% if obj.type == "class" and obj.bases and "dataclass" in (obj.bases | join(" ")) %}

:py:class:`{{ obj.id }}`
{{ "=" * (obj.id | length + 12) }}

.. py:currentmodule:: {{ obj.module.name }}

.. py:class:: {{ obj.id }}
{% if obj.bases %}

   Bases: {% for base in obj.bases %}:py:class:`{{ base }}`{% if not loop.last %}, {% endif %}{% endfor %}
{% endif %}

{% if obj.docstring %}
   {{ obj.docstring|indent(3) }}
{% endif %}

{% if obj.type == "class" %}
.. apischema-dataclass:: {{ obj.id }}
   :show-json-schema:
   :show-examples:
   :group-by-type:
{% endif %}

{% if obj.attributes %}
Fields
------

{% for attribute in obj.attributes %}
.. py:attribute:: {{ attribute.name }}
   :type: {{ attribute.annotation }}
   
   {{ attribute.docstring|default("Field documentation")|indent(3) }}

{% endfor %}
{% endif %}

{% if obj.methods %}
Methods
-------

{% for method in obj.methods %}
{{ method.render()|indent(0, true) }}
{% endfor %}
{% endif %}

{% endif %}