{% if not obj.display %}
:orphan:
{% endif %}

:py:class:`{{ obj.short_name }}`
{{ "=" * (obj.short_name|length + 11) }}

{% if obj.parent %}
.. currentmodule:: {{ obj.parent.name }}
{% endif %}

.. py:class:: {{ obj.short_name }}{% if obj.args %}({{ obj.args }}){% endif %}
   {% if obj.bases %}

   Bases: {% for base in obj.bases %}{{ base }}{% if not loop.last %}, {% endif %}{% endfor %}
   {% endif %}

   {% if obj.docstring %}
   {{ obj.docstring|indent(3) }}
   {% else %}
   {{ obj.summary }}
   {% endif %}

   {% if obj.name.endswith('Agent') %}
   .. admonition:: 🤖 Agent Class
      :class: tip

      This is an AI agent that can process inputs and generate responses.

      **Basic Usage**:

      .. code-block:: python

         agent = {{ obj.short_name }}(name="my_agent", engine=config)
         result = await agent.arun("Your input here")

   {% elif obj.name.endswith('Tool') %}
   .. admonition:: 🔧 Tool Class
      :class: tip

      This is a tool that agents can use to perform specific actions.

      **Basic Usage**:

      .. code-block:: python

         tool = {{ obj.short_name }}()
         agent = ReactAgent(name="agent", tools=[tool])

   {% elif obj.name.endswith('Config') %}
   .. admonition:: ⚙️ Configuration Class
      :class: tip

      This is a configuration class for customizing behavior.

   {% endif %}

   {% block methods_summary %}
   {% set visible_methods = obj.methods|selectattr("display")|list %}
   {% set init_method = visible_methods|selectattr("short_name", "equalto", "__init__")|list %}
   {% set regular_methods = visible_methods|rejectattr("short_name", "equalto", "__init__")|list %}
   
   {% if init_method or regular_methods %}
   .. rubric:: Methods Summary

   .. autosummary::
      :nosignatures:

   {% for method in init_method %}
      ~{{ obj.name }}.__init__
   {% endfor %}
   {% for method in regular_methods %}
      ~{{ obj.name }}.{{ method.short_name }}
   {% endfor %}
   {% endif %}
   {% endblock %}

   {% block attributes_summary %}
   {% set visible_attributes = obj.attributes|selectattr("display")|list %}
   {% if visible_attributes %}

   .. rubric:: Attributes Summary

   .. autosummary::
      :nosignatures:

   {% for attribute in visible_attributes %}
      ~{{ obj.name }}.{{ attribute.short_name }}
   {% endfor %}
   {% endif %}
   {% endblock %}

   {% if obj.bases %}
   .. rubric:: Inheritance Diagram

   .. inheritance-diagram:: {{ obj.name }}
      :parts: 1
      :caption: Class inheritance for {{ obj.short_name }}
   {% endif %}

   {% block attributes_documentation %}
   {% set visible_attributes = obj.attributes|selectattr("display")|list %}
   {% if visible_attributes %}

   Attributes
   ----------

   {% for attribute in visible_attributes %}
   .. py:attribute:: {{ attribute.short_name }}
      :type: {{ attribute.type }}
      {% if attribute.value %}
      :value: {{ attribute.value|truncate(100) }}
      {% endif %}

      {% if attribute.docstring %}
      {{ attribute.docstring|indent(6) }}
      {% else %}
      Attribute ``{{ attribute.short_name }}``
      {% endif %}

   {% endfor %}
   {% endif %}
   {% endblock %}

   {% block methods_documentation %}
   {% set visible_methods = obj.methods|selectattr("display")|list %}
   {% if visible_methods %}

   Methods
   -------

   {% for method in visible_methods %}
   .. py:method:: {{ method.short_name }}({{ method.args }})
      {% if method.returns %}
      :rtype: {{ method.returns }}
      {% endif %}
      {% if method.properties %}
      {% for property in method.properties %}
      :{{ property }}:
      {% endfor %}
      {% endif %}

      {% if method.docstring %}
      {{ method.docstring|indent(6) }}
      {% else %}
      Method ``{{ method.short_name }}``
      {% endif %}

      {% if method.short_name == "__init__" %}
      .. rubric:: Parameters

      See class parameters above.
      {% endif %}

   {% endfor %}
   {% endif %}
   {% endblock %}

   {% block inner_classes %}
   {% set visible_classes = obj.classes|selectattr("display")|list %}
   {% if visible_classes %}

   Inner Classes
   -------------

   .. autosummary::
      :nosignatures:
      :template: autosummary/class.rst

   {% for class in visible_classes %}
      {{ obj.name }}.{{ class.short_name }}
   {% endfor %}
   {% endif %}
   {% endblock %}

   {% block examples %}
   {% if obj.name.endswith('Agent') or obj.name.endswith('Tool') %}

   Examples
   --------

   {% if obj.name.endswith('Agent') %}
   Basic agent usage:

   .. code-block:: python

      {% if obj.parent %}
      from {{ obj.parent.name }} import {{ obj.short_name }}
      {% else %}
      from {{ obj.name.rsplit('.', 1)[0] }} import {{ obj.short_name }}
      {% endif %}
      from haive.core.engine import AugLLMConfig

      # Create agent configuration
      config = AugLLMConfig(
          temperature=0.7,
          max_tokens=1000
      )

      # Initialize agent
      agent = {{ obj.short_name }}(
          name="my_{{ obj.short_name|lower }}",
          engine=config
      )

      # Use the agent
      result = await agent.arun("Process this input")
      print(result)

   {% elif obj.name.endswith('Tool') %}
   Basic tool usage:

   .. code-block:: python

      {% if obj.parent %}
      from {{ obj.parent.name }} import {{ obj.short_name }}
      {% else %}
      from {{ obj.name.rsplit('.', 1)[0] }} import {{ obj.short_name }}
      {% endif %}
      from haive.agents import ReactAgent

      # Create tool instance
      tool = {{ obj.short_name }}()

      # Use with an agent
      agent = ReactAgent(
          name="agent_with_tool",
          tools=[tool]
      )

      # Execute with tool
      result = await agent.arun("Use the tool to...")

   {% endif %}
   {% endif %}
   {% endblock %}

   {% block see_also %}

   See Also
   --------

   {% if obj.name.endswith('Agent') %}
   * :py:class:`haive.agents.base.agent.Agent` - Base agent class
   * :py:class:`haive.core.engine.aug_llm.AugLLMConfig` - LLM configuration
   {% elif obj.name.endswith('Tool') %}
   * :py:class:`haive.tools.base.BaseTool` - Base tool class
   * :py:func:`haive.tools.decorator.tool` - Tool decorator
   {% elif obj.name.endswith('Config') %}
   * :py:class:`pydantic.BaseModel` - Pydantic base model
   {% endif %}
   {% if obj.parent %}
   * :doc:`/api/{{ obj.parent.name.replace('.', '/') }}/index` - Parent module
   {% endif %}

   {% endblock %}