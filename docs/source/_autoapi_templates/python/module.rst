{# Custom module template for pyautodoc #}
{% if not obj.display %}:orphan:{% endif %}

:py:mod:`{{ obj.name }}`
{{ "=" * (obj.name | length + 10) }}

.. py:module:: {{ obj.name }}

{% if obj.docstring %}
{{ obj.docstring }}
{% endif %}

{% if obj.classes %}
Classes
-------

.. autoapisummary::

{% for class in obj.classes | sort(attribute='name') %}
   {{ class.id }}
{% endfor %}


Module Contents
---------------

{% for class in obj.classes %}
{{ class.render()|indent(0, true) }}
{% endfor %}
{% endif %}

{% if obj.functions %}
Functions
---------

.. autoapisummary::

{% for function in obj.functions %}
   {{ function.id }}
{% endfor %}

{% for function in obj.functions %}
{{ function.render()|indent(0, true) }}
{% endfor %}
{% endif %}

{% if obj.attributes %}
Attributes
----------

.. autoapisummary::

{% for attribute in obj.attributes %}
   {{ attribute.id }}
{% endfor %}

{% for attribute in obj.attributes %}
{{ attribute.render()|indent(0, true) }}
{% endfor %}
{% endif %}

{# ---------------------------- #}
{#    Autolink References       #}
{# ---------------------------- #}
{% if obj.classes or obj.functions or obj.attributes %}
.. rubric:: Related Links

.. autolink-examples:: {{ obj.name }}
   :collapse:
   
.. autolink-skip:: next
{% endif %}