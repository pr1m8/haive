{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autofunction:: {{ objname }}

{% if examples %}

Examples



{{ examples }}

{% endif %}

{% if see_also %}

See Also



{{ see_also }}

{% endif %}
