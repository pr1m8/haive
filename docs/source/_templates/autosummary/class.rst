{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:
   :special-members: __init__, __call__

   {% block methods %}
   {% if methods %}
   .. rubric:: {{ _('Methods') }}

   .. autosummary::

      :nosignatures:

   {% for item in methods %}

      ~{{ name }}.{{ item }}

   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block attributes %}
   {% if attributes %}
   .. rubric:: {{ _('Attributes') }}

   .. autosummary::
   {% for item in attributes %}

      ~{{ name }}.{{ item }}

   {%- endfor %}
   {% endif %}
   {% endblock %}
   
   .. rubric:: Examples
   
   The Examples section from the class docstring will be displayed here automatically if present.
