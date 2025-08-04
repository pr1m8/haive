{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

   :members:
   :show-inheritance:
   :inherited-members:
   :special-members: __init__, __call__
   
   {% block methods %}
   {% if methods %}
   .. rubric:: Methods
   
   .. autosummary::

      :nosignatures:

   {% for item in methods %}

      ~{{ name }}.{{ item }}

   {%- endfor %}
   {% endif %}
   {% endblock %}
   
   {% block attributes %}
   {% if attributes %}
   .. rubric:: Attributes
   
   .. autosummary::

      :nosignatures:

   {% for item in attributes %}

      ~{{ name }}.{{ item }}

   {%- endfor %}
   {% endif %}
   {% endblock %}
