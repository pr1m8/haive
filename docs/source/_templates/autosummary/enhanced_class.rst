{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

{% if objname is match('.*Config$') or objname is match('.Schema$') or objname is match('.*Model$') %}*
{# Pydantic model template #}
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

   .. rubric:: {{ _('Configuration') }}

   The Pydantic model configuration and validation rules.

   .. rubric:: {{ _('Field Details') }}

   Detailed field information with types, constraints, and validation.

{% else %}
{# Regular class template with enhanced features #}
.. autoclass:: {{ objname }}

   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:
   :special-members: __init__, __call__

{% endif %}

   {% block methods %}
   {% if methods %}
   .. rubric:: {{ _('Methods') }}

   .. autosummary::

      :nosignatures:
      :toctree: .
      :template: method.rst

   {% for item in methods %}

      ~{{ name }}.{{ item }}

   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block attributes %}
   {% if attributes %}
   .. rubric:: {{ _('Attributes') }}

   .. autosummary::

      :toctree: .
      :template: attribute.rst

   {% for item in attributes %}

      ~{{ name }}.{{ item }}

   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block diagrams %}
   {% if objname is match('.*Agent$') %}*
   .. rubric:: {{ _('Class Diagram') }}

   .. inheritance-diagram:: {{ objname }}

      :parts: 1
      :private-bases:
      :caption: Inheritance diagram for {{ objname }}

   {% endif %}
   {% endblock %}

   .. rubric:: {{ _('Examples') }}

   {% if objname is match('.*Agent$') %}*
   Usage examples for this agent type:


.. code-block:: python

    # Code example here

      :caption: Basic usage

      from {{ module }} import {{ objname }}

      # Create and configure agent
      agent = {{ objname }}(name="example")

      # Use agent
      result = await agent.arun("Your input here")
      print(result)


      For more examples, see the :doc:`agent examples </agents/demos/index>.`
      {% else %}
      The Examples section from the class docstring will be displayed here automatically if present.
      {% endif %}
