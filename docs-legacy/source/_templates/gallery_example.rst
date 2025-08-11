{{ title }}
{{ "=" * title|length }}

.. currentmodule:: {{ module }}

.. card:: 📖 Example: {{ title }}
   :class-card: sd-rounded-3 sd-shadow-lg
   :class-header: sd-bg-success sd-text-white

   **{{ title }}**

   {{ description if description else 'Interactive code example demonstrating Haive functionality.' }}

.. tab-set::

   .. tab-item:: 🚀 Run Example
      :sync: run

      .. exec_code::
         :caption: {{ title }} - Live Execution
         :linenos:
         :hide_output:

         {% if example_code %}
         {{ example_code }}
         {% else %}
         # Example code for {{ title }}
         print("🤖 {{ title }} Example")
         print("=" * 40)
         
         try:
             # Import required modules
             {% if imports %}
             {% for import_line in imports %}
             {{ import_line }}
             {% endfor %}
             {% else %}
             from haive.core.engine.aug_llm import AugLLMConfig
             from haive.agents.simple import SimpleAgent
             {% endif %}
             
             print("✅ Imports successful")
             
             # Create configuration
             config = AugLLMConfig(
                 temperature=0.7,
                 max_tokens=1000
             )
             print(f"⚙️ Configuration: {type(config).__name__}")
             
             {% if agent_type %}
             # Create {{ agent_type }} agent
             agent = {{ agent_type }}(name="example_agent", engine=config)
             {% else %}
             # Create example agent
             agent = SimpleAgent(name="example_agent", engine=config)
             {% endif %}
             
             print(f"🤖 Agent created: {agent.name}")
             print("🎯 Ready for execution!")
             
         except Exception as e:
             print(f"ℹ️ Example info: {e}")
         {% endif %}

   .. tab-item:: 📝 Code
      :sync: code

      .. rubric:: Source Code

      .. code-block:: python
         :caption: {{ title }} implementation
         :linenos:
         :emphasize-lines: {% if highlight_lines %}{{ highlight_lines|join(',') }}{% else %}1{% endif %}

         {% if example_code %}
         {{ example_code }}
         {% else %}
         """
         {{ title }}
         {{ "=" * title|length }}
         
         {{ description if description else 'Example demonstrating Haive functionality.' }}
         """
         
         {% if imports %}
         {% for import_line in imports %}
         {{ import_line }}
         {% endfor %}
         {% else %}
         from haive.core.engine.aug_llm import AugLLMConfig
         from haive.agents.simple import SimpleAgent
         {% endif %}
         
         # Configuration
         config = AugLLMConfig(
             temperature=0.7,
             max_tokens=1000,
             system_message="You are a helpful assistant."
         )
         
         # Create agent
         {% if agent_type %}
         agent = {{ agent_type }}(name="example", engine=config)
         {% else %}
         agent = SimpleAgent(name="example", engine=config)
         {% endif %}
         
         # Example usage
         async def main():
             result = await agent.arun("{{ example_query if example_query else 'Hello, how can you help me?' }}")
             print(f"Response: {result}")
         
         # Run the example
         import asyncio
         asyncio.run(main())
         {% endif %}

   .. tab-item:: 🔧 Configuration
      :sync: config

      .. rubric:: Example Configuration

      .. jsonschema:: 
         {% if config_schema %}
         {{ config_schema }}
         {% else %}
         {
           "type": "object",
           "properties": {
             "agent_name": {
               "type": "string", 
               "description": "Name of the agent",
               "default": "example_agent"
             },
             "temperature": {
               "type": "number",
               "description": "LLM temperature for creativity",
               "minimum": 0.0,
               "maximum": 2.0,
               "default": 0.7
             },
             "max_tokens": {
               "type": "integer",
               "description": "Maximum response tokens",
               "minimum": 100,
               "maximum": 4000,
               "default": 1000
             }
           }
         }
         {% endif %}

      .. admonition:: ⚙️ Configuration Tips
         :class: tip

         * Adjust :paramlink:`temperature <Higher values = more creative>` for different response styles
         * Use :tippy:`max_tokens <Controls response length>` to limit response size
         * Try different :emoji:`robot` agent types for various use cases

.. dropdown:: 🧪 Interactive Demo
   :color: primary
   :icon: play
   :open:

   .. autorun::

      print("🎮 {{ title }} Interactive Demo")
      print("=" * 50)
      
      # Show example capabilities
      capabilities = [
          {% if capabilities %}
          {% for capability in capabilities %}
          "{{ capability }}",
          {% endfor %}
          {% else %}
          "💬 Natural language conversation",
          "🔧 Tool integration support", 
          "💾 State persistence",
          "🎯 Configurable behavior",
          "⚡ Async execution"
          {% endif %}
      ]
      
      print(f"🌟 Example demonstrates ({len(capabilities)} features):")
      for i, cap in enumerate(capabilities, 1):
          print(f"  {i}. {cap}")
      
      print(f"\n🚀 Ready to explore {{ title }}!")

.. admonition:: 📊 Example Metrics
   :class: note

   .. grid:: 1 2 4 4
      :gutter: 2

      .. grid-item::
         :class: metric-item

         **{{ lines_of_code if lines_of_code else '~50' }}**
         
         *Lines of Code*

      .. grid-item::
         :class: metric-item

         **{{ complexity if complexity else 'Beginner' }}**
         
         *Complexity Level*

      .. grid-item::
         :class: metric-item

         **{{ execution_time if execution_time else '<5s' }}**
         
         *Avg. Execution*

      .. grid-item::
         :class: metric-item

         **{{ features_count if features_count else '5+' }}**
         
         *Features Used*

{% if related_examples %}
.. seealso::

   **Related Examples:**
   
   {% for example in related_examples %}
   * :doc:`{{ example.link }}` - {{ example.title }}
   {% endfor %}
   
   * :doc:`/examples/index` - All examples
   * :doc:`/guides/index` - User guides  
   * :doc:`/api/index` - API reference
{% else %}
.. seealso::

   * :doc:`/examples/index` - More examples
   * :doc:`/guides/getting-started` - Getting started guide
   * :doc:`/api/index` - API reference
   * :issue:`new` - Request more examples
{% endif %}

.. req:: Example Requirements
   :id: EX_{{ title.upper().replace(' ', '_') }}_001
   :status: implemented
   :priority: medium
   :tags: example, documentation

   {{ title }} example should demonstrate key {{ module }} functionality with clear, working code.

.. note::

   **Quick Start**

   1. Copy the code from the "Code" tab
   2. Install dependencies: ``pip install haive``
   3. Run the example: ``python your_example.py``
   4. Customize for your use case

   Need help? :tippy:`Check the documentation <Links to comprehensive guides>` or :emoji:`speech_balloon` ask questions!