API Reference
=============

This is the complete API reference for all Haive packages.

.. toctree::
   :titlesonly:
   :maxdepth: 2

{% for page in pages %}
   {% if page.type == "package" %}
   {{ page.include_path }}
   {% endif %}
{% endfor %}

Package Overview
----------------

.. grid:: 1 2 2 3
   :gutter: 2

{% for page in pages %}
{% if page.type == "package" %}
   .. grid-item-card:: {{ page.name }}
      :link: {{ page.include_path }}
      :link-type: doc

      {{ page.summary|default("Package " + page.name, true) }}
{% endif %}
{% endfor %}

Quick Navigation
----------------

By Category
^^^^^^^^^^^

.. tab-set::

   .. tab-item:: Core
      :sync: core

      .. autosummary::
         :nosignatures:
         :template: autosummary/module.rst

         haive.core
         haive.core.engine
         haive.core.schema
         haive.core.graph

   .. tab-item:: Agents
      :sync: agents

      .. autosummary::
         :nosignatures:
         :template: autosummary/module.rst

         haive.agents
         haive.agents.simple
         haive.agents.react
         haive.agents.multi

   .. tab-item:: Tools
      :sync: tools

      .. autosummary::
         :nosignatures:
         :template: autosummary/module.rst

         haive.tools
         haive.tools.base
         haive.tools.decorator
         haive.tools.toolkit

   .. tab-item:: Pre-built
      :sync: prebuilt

      .. autosummary::
         :nosignatures:
         :template: autosummary/module.rst

         haive.prebuilt
         haive.prebuilt.search_and_summarize
         haive.prebuilt.scientific_paper_agent
         haive.prebuilt.company_researcher

All Modules
-----------

.. autosummary::
   :nosignatures:
   :recursive:
   :template: autosummary/module.rst

{% for page in pages %}
{% if page.type in ["module", "package"] %}
   {{ page.name }}
{% endif %}
{% endfor %}