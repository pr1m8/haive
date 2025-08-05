.. .. jinja:: agent_demo

   :ctx: {"agent_id": "simple"}

   {% set agent_data = get_agent_context(agent_id) %}
   {{ agent_data.agent_name }} Demo
   {{ '=' * (agent_data.agent_name|length + 5) }}*

   {{ agent_data.agent_description }}

   <div class="agent-demo-container">
   <!-- Agent Overview Card -->

   <div class="agent-overview-card">

   <div class="agent-header">

   <div class="agent-icon">{{ agent_data.agent_icon }}</div>

   <div>
   <h2>{{ agent_data.agent_name }}</h2>
   <p class="agent-type">{{ agent_data.agent_type }}</p>
   </div>

   </div>



   <div class="agent-features">
   {% for feature in agent_data.agent_features %}
   <span class="feature-tag">{{ feature }}</span>
   {% endfor %}
   </div>

   </div>

   <!-- Graph Visualization -->

   <div id="{{ agent_data.agent_id }}-graph"
   class="agent-graph-container"
   data-agent-graph='{{ agent_data.graph_data_json }}'>
   </div>

   <!-- State History Timeline -->

   <div id="{{ agent_data.agent_id }}-state-history"
   class="state-history-container"
   data-state-history='{{ agent_data.state_history_json }}'>
   </div>

   <!-- Execution Trace -->

   <div id="{{ agent_data.agent_id }}-execution-trace"
   class="execution-trace-container"
   data-execution-trace='{{ agent_data.execution_trace_json }}'>
   </div>

   <!-- Interactive Example -->

   <div class="interactive-example">
   <h3>Try it Live</h3>

   <div class="example-input">
   <label>Input:</label>
   <textarea id="{{ agent_data.agent_id }}-input" placeholder="{{ agent_data.example_input }}"></textarea>
   </div>

   <button onclick="runAgent('{{ agent_data.agent_id }}')" class="run-button">

                   Run {{ agent_data.agent_name }}
   </button>

   <div id="{{ agent_data.agent_id }}-output" class="example-output"></div>
   </div>

   </div>

   <script>

       // Initialize visualization on page load
       document.addEventListener('DOMContentLoaded', function() {
           // Initialize graph
           const graphData = JSON.parse(document.getElementById('{{ agent_data.agent_id }}-graph').dataset.agentGraph);
           new AgentGraphVisualizer('{{ agent_data.agent_id }}-graph', graphData);

           // Initialize state history
           const stateData = JSON.parse(document.getElementById('{{ agent_data.agent_id }}-state-history').dataset.stateHistory);
           new StateHistoryVisualizer('{{ agent_data.agent_id }}-state-history', stateData);

           // Initialize execution trace
           const traceData = JSON.parse(document.getElementById('{{ agent_data.agent_id }}-execution-trace').dataset.executionTrace);
           new ExecutionTraceVisualizer('{{ agent_data.agent_id }}-execution-trace', traceData);
       });
   </script>

    Code Example
    ------------

.. code-block:: python

    # Code example here

       from {{ agent_data.agent_module_import }} import {{ agent_data.agent_class }}

       # Initialize the agent
       agent = {{ agent_data.agent_class }}(
       name="{{ agent_data.agent_id }}",
       {{ agent_data.agent_config }}
       )

       # Run the agent
       result = await agent.arun("{{ agent_data.example_input }}")
       print(result)

       Architecture Details

   --------------------

       {{ agent_data.agent_architecture_details }}

       See Also
       --------

       - :doc:`/api/{{ agent_data.agent_module_path }} - Full API documentation`
       - :doc:`/guides/{{ agent_data.agent_guide }} - Usage guide`
       - :doc:`/examples/{{ agent_data.agent_example }} - More examples`
