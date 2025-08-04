{{ fullname | escape | underline}}

.. automodule:: {{ fullname }}

   :members:
   :undoc-members:
   :show-inheritance:

   {% block attributes %}
   {% if attributes %}
   .. rubric:: {{ _('Module Attributes') }}

   .. autosummary::

      :toctree: .

   {% for item in attributes %}

      {{ item }}

   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block functions %}
   {% if functions %}
   .. rubric:: {{ _('Functions') }}

   .. autosummary::

      :toctree: .
      :nosignatures:

   {% for item in functions %}

      {{ item }}

   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block classes %}
   {% if classes %}
   .. rubric:: {{ _('Classes') }}

   .. autosummary::

      :toctree: .
      :template: enhanced_class.rst
      :nosignatures:

   {% for item in classes %}

      {{ item }}

   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block exceptions %}
   {% if exceptions %}
   .. rubric:: {{ _('Exceptions') }}

   .. autosummary::

      :toctree: .

   {% for item in exceptions %}

      {{ item }}

   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block diagrams %}
   {% if classes and fullname is match('.*\.agents\..*') %}
   .. rubric:: {{ _('Module Structure') }}

   .. inheritance-diagram:: {% for item in classes %}{{ item }}{% if not loop.last %} {% endif %}{% endfor %}

      :parts: 2
      :caption: Class relationships in {{ fullname }}

   {% endif %}
   {% endblock %}

   {% block related %}
   .. rubric:: {{ _('Related') }}

   {% if fullname is match('.*\.agents\..*') %}
   * :doc:`Agent Demos </agents/demos/index>`*
   * :doc:`Agent Examples </examples/agents/index>`*
   * :doc:`Agent Development Guide </guides/agent_development>`*
   {% elif fullname is match('.*\.tools\..*') %}
   * :doc:`Tool Creation Guide </guides/tool_creation>`*
   * :doc:`Using Tools </guides/using_tools>`*
   * :doc:`Custom Tools </guides/custom_tools>`*
   {% elif fullname is match('.*\.games\..*') %}
   * :doc:`Game Demos </games/demos/index>`*
   * :doc:`Game Examples </examples/games/index>`*
   * :doc:`Agent Games Guide </guides/agent_games>`*
   {% endif %}
   {% endblock %}
