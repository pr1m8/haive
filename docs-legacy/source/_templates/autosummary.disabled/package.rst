{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. automodule:: {{ fullname }}

   :no-members:
   :no-inherited-members:

{% block modules %}
{% if modules %}
.. toctree::


   :maxdepth: 2

{% for item in modules %}

   {{ item }}

{%- endfor %}
{% endif %}
{% endblock %}
