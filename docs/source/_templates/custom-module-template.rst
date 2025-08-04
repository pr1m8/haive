{{ fullname | escape | underline}}

.. automodule:: {{ fullname }}
    :members:
    :undoc-members:
    :show-inheritance:
    :special-members: __init__, __call__

{% block modules %}

{% if modules %}
Submodules
----------

.. toctree::

   :maxdepth: 1

{% for item in modules %}

   {{ item }}

{%- endfor %}
{% endif %}
{% endblock %}

{% block attributes %}

{% if attributes %}
Module Attributes
-----------------

.. autosummary::
    :nosignatures:
    {% for item in attributes %}
    {{ item }}
    {%- endfor %}

{% endif %}
{% endblock %}

{% block functions %}

{% if functions %}
Functions
---------

.. autosummary::
    :nosignatures:
    {% for item in functions %}
    {{ item }}
    {%- endfor %}

.. automodsumm:: {{ fullname }}
    :functions-only:

{% endif %}
{% endblock %}

{% block classes %}

{% if classes %}
Classes
-------

.. autosummary::
    :nosignatures:
    {% for item in classes %}
    {{ item }}
    {%- endfor %}

.. automodsumm:: {{ fullname }}
    :classes-only:

{% endif %}
{% endblock %}

{% block exceptions %}

{% if exceptions %}
Exceptions
----------

.. autosummary::
    :nosignatures:
    {% for item in exceptions %}
    {{ item }}
    {%- endfor %}

.. automodsumm:: {{ fullname }}
    :exceptions-only:

{% endif %}
{% endblock %}
