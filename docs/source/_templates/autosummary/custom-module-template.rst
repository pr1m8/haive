{{ fullname | escape | underline}}

.. automodule:: {{ fullname }}

   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:
   :special-members: __init__, __call__

   {% block modules %}
   {% if modules %}
   .. rubric:: Modules

   .. autosummary::

      :toctree:
      :template: custom-module-template.rst
      :recursive:

   {% for item in modules %}

      {{ item }}

   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block classes %}
   {% if classes %}
   .. rubric:: Classes

   .. autosummary::

      :toctree:

   {% for item in classes %}

      {{ item }}

   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block functions %}
   {% if functions %}
   .. rubric:: Functions

   .. autosummary::

      :toctree:

   {% for item in functions %}

      {{ item }}

   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block exceptions %}
   {% if exceptions %}
   .. rubric:: Exceptions

   .. autosummary::

      :toctree:

   {% for item in exceptions %}

      {{ item }}

   {%- endfor %}
   {% endif %}
   {% endblock %}
