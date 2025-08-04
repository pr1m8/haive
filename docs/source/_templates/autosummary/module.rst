{%- set readable_title = module_readable_title|default(fullname.split('.')[-1].replace('_', ' ').title()) -%}
{{ readable_title | escape | underline}}

.. py:module:: {{ fullname }}

.. currentmodule:: {{ fullname }}

.. automodule:: {{ fullname }}

{# Module path for breadcrumb #}
.. raw:: html

   .. raw:: html

   <div class="module-path" style="margin-bottom: 1rem; color: var(--color-foreground-secondary);">
   <code>{{ fullname }}</code>
   </div>

{# Try to include module docstring or README #}
{%- set module_parts = fullname.split('.') %}
{%- if module_parts|length >= 2 %}
{%- set package_name = 'haive-' + module_parts[1] %}
{%- set submodule_path = '/'.join(module_parts[2:]) if module_parts|length > 2 else '' %}
{%- set readme_path = '../../../packages/' + package_name + '/src/haive/' + module_parts[1] %}
{%- if submodule_path %}
    {%- set readme_path = readme_path + '/' + submodule_path %}
{%- endif %}
{%- set readme_path = readme_path + '/README.md' %}

{# Try to include README if it exists #}
.. ifconfig:: False

     .. include:: {{ readme_path }}
        :parser: myst_parser.sphinx_
{%- endif %}

.. automodule:: {{ fullname }}

   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:
   :special-members: __init__, __call__, __new__
   :imported-members:
   :exclude-members: logger

   {# Show module-level docstring with examples #}
   {% if fullname.endswith('.agent') or fullname.endswith('.agents') %}
   .. rubric:: Module Overview

   This module contains agent implementations. See the class documentation below for detailed usage.
   {% endif %}

   {% block attributes %}
   {% if attributes %}
   .. rubric:: {{ _('Module Attributes') }}

   .. autosummary::

      :nosignatures:
      :toctree: .
      :template: attribute.rst

   {% for item in attributes %}

      {{ item }}

   {%- endfor %}

   {# Detailed attribute documentation #}
   {% for item in attributes %}
   .. autodata:: {{ item }}

      :annotation:

   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block functions %}
   {% if functions %}
   .. rubric:: {{ _('Functions') }}

   .. autosummary::

      :nosignatures:
      :toctree: .
      :template: function.rst

   {% for item in functions %}

      {{ item }}

   {%- endfor %}

   {# Detailed function documentation with examples #}
   {% for item in functions %}

   .. autofunction:: {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block classes %}
   {% if classes %}
   .. rubric:: {{ _('Classes') }}

   .. autosummary::

      :nosignatures:
      :toctree: .
      :template: class.rst

   {% for item in classes %}

      {{ item }}

   {%- endfor %}

   {# Detailed class documentation #}
   {% for item in classes %}

   .. autoclass:: {{ item }}

      :members:
      :undoc-members:
      :show-inheritance:
      :inherited-members:
      :special-members: __init__, __call__

      .. rubric:: Examples

      .. note::
         See the class docstring for usage examples.

   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block exceptions %}
   {% if exceptions %}
   .. rubric:: {{ _('Exceptions') }}

   .. autosummary::

      :nosignatures:
      :toctree: .
      :template: exception.rst

   {% for item in exceptions %}

      {{ item }}

   {%- endfor %}

   {% for item in exceptions %}
   .. autoexception:: {{ item }}

      :members:
      :show-inheritance:

   {%- endfor %}
   {% endif %}
   {% endblock %}

{% block modules %}
{% if modules %}
.. rubric:: {{ _('Submodules') }}

.. autosummary::

   :toctree: .
   :template: module.rst


{% for item in modules %}

   {{ item }}

{%- endfor %}

{# Also show submodule details inline for better navigation #}
.. toctree::

   :maxdepth: 1
   :caption: Submodules


{% for item in modules %}

   {{ item }} <{{ item }}>

{%- endfor %}
{% endif %}
{% endblock %}
