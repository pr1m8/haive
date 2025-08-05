{{ name }} Example
{{ "=" * (name|length + 8) }}*

   <div class="agent-example-container">

   <div class="agent-header">

   <div class="agent-icon">🤖</div>

   <div class="agent-info">
   <h2>{{ name }} Usage Example</h2>
   <p class="agent-description">{{ description }}</p>
   </div>

   </div>
   </div>

Overview



This example demonstrates how to use the {{ name }} for {{ purpose }}.

**Key Features:**
{% for feature in features %}
- {{ feature }}

{% endfor %}

**Use Cases:**
{% for use_case in use_cases %}
- {{ use_case }}

{% endfor %}

Basic Example



.. code-block:: python

    # Code example here

    from haive.{{ module_path }} import {{ name }}
    from haive.core.engine.aug_llm import AugLLMConfig

    # Create the agent
    agent = {{ name }}(
        name="{{ name|lower }}_example",
        engine=AugLLMConfig(
            temperature={{ temperature|default(0.7) }},
            system_message="{{ system_message }}"
        ){% if tools %},
        tools=[{{ tools|join(", ") }}]{% endif %}
    )

    # Basic usage
    import asyncio

    async def run_example():
        result = await agent.arun("{{ example_input }}")
        print(result)
        return result

    # Run the example
    result = asyncio.run(run_example())

    {% if advanced_example %}
    Advanced Example


---------------

    {{ advanced_example }}
    {% endif %}

    {% if configuration_options %}
    Configuration Options



    .. list-table::


    :header-rows: 1
    :widths: 20 20 60

    * - Parameter*

     - Type
     - Description

    {% for option in configuration_options %}

    * - {{ option.name }}*

     - {{ option.type }}
     - {{ option.description }}

    {% endfor %}

    {% endif %}

    Graph Visualization



    <div id="agent-graph-{{ name|lower }}" class="agent-graph-container">
    <script>
    document.addEventListener('DOMContentLoaded', function() {
    new AgentGraphVisualizer('agent-graph-{{ name|lower }}', {
    nodes: [
    {id: 'start', label: 'Start', type: 'input'},
    {id: 'process', label: '{{ name }}', type: 'agent'},
    {id: 'end', label: 'Output', type: 'output'}
    ],
    edges: [
    {from: 'start', to: 'process'},
    {from: 'process', to: 'end'}
    ],
    type: '{{ name }}'
    });
    });

    </script>
    </div>

    {% if state_schema %}
    State Schema



    .. autoclass:: {{ state_schema }}

    :members:
    :undoc-members:
    :show-inheritance:

    {% endif %}

    Best Practices



    {% for practice in best_practices %}
    {{ loop.index }}. **{{ practice.title }}**: {{ practice.description }}
    {% endfor %}

    Related Examples



    {% for related in related_examples %}
    - :doc:`{{ related.path }} - {{ related.description }}`

`
    {% endfor %}

    API Reference



    .. autoclass:: {{ module_path }}.{{ name }}

    :members:
    :undoc-members:
    :show-inheritance:

    .. seealso::


    - :doc`:`../api/{{ module_path|replace('.', '/') }}/index`

`
    - :doc`:`../guides/building_agents`

`
    - :doc`:`../guides/agent_patterns`

`
`
