{{ agent_name }} Demo
{{ '=' * (len(agent_name) + 5) }}*

{{ agent_description }}

.. raw:: html

   .. raw:: html

   <div class="agent-demo-container">
   <!-- Agent Overview Card -->

.. raw:: html

   <div class="agent-overview-card">

.. raw:: html

   <div class="agent-header">

.. raw:: html

   <div class="agent-icon">{{ agent_icon }}</div>

.. raw:: html

   <div>
   <h2>{{ agent_name }}</h2>
   <p class="agent-type">{{ agent_type }}</p>
   </div>

.. raw:: html

   </div>

            

.. raw:: html

   <div class="agent-features">
   {% for feature in agent_features %}
   <span class="feature-tag">{{ feature }}</span>
   {% endfor %}
   </div>

.. raw:: html

   </div>

.. raw:: html

   <!-- Graph Visualization -->

.. raw:: html

   <div id="{{ agent_id }}-graph" 
   class="agent-graph-container"
   data-agent-graph='{{ graph_data | tojson }}'>
   </div>

.. raw:: html

   <!-- State History Timeline -->

.. raw:: html

   <div id="{{ agent_id }}-state-history" 
   class="state-history-container"
   data-state-history='{{ state_history | tojson }}'>
   </div>

.. raw:: html

   <!-- Execution Trace -->

.. raw:: html

   <div id="{{ agent_id }}-execution-trace" 
   class="execution-trace-container"
   data-execution-trace='{{ execution_trace | tojson }}'>
   </div>

.. raw:: html

   <!-- Interactive Example -->

.. raw:: html

   <div class="interactive-example">
   <h3>Try it Live</h3>

.. raw:: html

   <div class="example-input">
   <label>Input:</label>
   <textarea id="{{ agent_id }}-input" placeholder="{{ example_input }}"></textarea>
   </div>

.. raw:: html

   <button onclick="runAgent('{{ agent_id }}')" class="run-button">

                Run {{ agent_name }}
.. raw:: html

   </button>

.. raw:: html

   <div id="{{ agent_id }}-output" class="example-output"></div>
   </div>

.. raw:: html

   </div>

.. raw:: html

   <script>

    // Initialize visualization on page load
    document.addEventListener('DOMContentLoaded', function() {
        // Initialize graph
        const graphData = JSON.parse(document.getElementById('{{ agent_id }}-graph').dataset.agentGraph);
        new AgentGraphVisualizer('{{ agent_id }}-graph', graphData);
        
        // Initialize state history
        const stateData = JSON.parse(document.getElementById('{{ agent_id }}-state-history').dataset.stateHistory);
        new StateHistoryVisualizer('{{ agent_id }}-state-history', stateData);
        
        // Initialize execution trace
        const traceData = JSON.parse(document.getElementById('{{ agent_id }}-execution-trace').dataset.executionTrace);
        new ExecutionTraceVisualizer('{{ agent_id }}-execution-trace', traceData);
    });
.. raw:: html

   </script>

Code Example
------------

.. code-block:: python

    from {{ agent_module_import }} import {{ agent_class }}

    # Initialize the agent
    agent = {{ agent_class }}(
    name="{{ agent_id }}",
    {{ agent_config }}
    )

    # Run the agent
    result = await agent.arun("{{ example_input }}")
    print(result)

    Architecture Details
    --------------------

    {{ agent_architecture_details }}

    See Also
    --------

    - :doc:`/api/{{ agent_module_path }}` - Full API documentation
    - :doc:`/guides/{{ agent_guide }}` - Usage guide
    - :doc:`/examples/{{ agent_example }}` - More examples
