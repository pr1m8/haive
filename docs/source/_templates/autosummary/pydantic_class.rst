{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autopydantic_model:: {{ objname }}
   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:
   :special-members: __init__, __call__
   :model-show-config-member: true
   :model-show-config-summary: true
   :model-show-validator-members: true
   :model-show-validator-summary: true
   :model-show-field-summary: true
   :field-show-constraints: true
   :field-show-alias: true
   :field-show-default: true
   :field-show-required: true

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
   
   {% block fields %}
   .. rubric:: {{ _('Pydantic Fields') }}
   
   The field summary will be automatically generated showing constraints, types, and defaults.
   {% endblock %}
   
   {% block validators %}
   .. rubric:: {{ _('Validators') }}
   
   Field validators and model validators will be documented automatically.
   {% endblock %}
   
   .. rubric:: Examples
   
   The Examples section from the class docstring will be displayed here automatically if present.