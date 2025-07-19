.. jinja:: agent_demo
   :ctx: {"agent_type": "simple"}

   {% set agent_data = get_agent_demo_context(agent_type) %}
   {% set title = agent_data.agent_icon ~ ' ' ~ agent_data.agent_name ~ ' Demo' %}
   {{ title }}
   {{ '=' * (title|length) }}

   .. raw:: html

      <div class="agent-demo-container">
         <div class="agent-demo-header">
            <div class="agent-demo-icon">{{ agent_data.agent_icon }}</div>
            <div class="agent-demo-title">
               <h3>{{ agent_data.agent_name }}</h3>
               <p class="agent-demo-description">{{ agent_data.agent_description }}</p>
            </div>
         </div>

   Overview
   --------

   The **{{ agent_data.agent_name }}** is {{ agent_data.agent_description|lower }}. This demo showcases {% if agent_data.cache_available %}real execution data{% else %}example capabilities{% endif %} captured from actual agent runs.

   .. raw:: html

      <div class="agent-demo-features">
         <h4>🎯 Key Features</h4>
         <ul>
            {% for feature in agent_data.agent_features %}
            <li>{{ feature }}</li>
            {% endfor %}
         </ul>
      </div>

   Quick Start
   -----------

   .. code-block:: python

      from {{ agent_data.agent_module_import }} import {{ agent_data.agent_name }}
      from haive.core.engine.aug_llm import AugLLMConfig

      # Configure the agent
      config = {{ agent_data.agent_config }}
      agent = {{ agent_data.agent_name }}(
          name="demo_agent",
          engine=config
      )

      # Execute the agent
      result = agent.run("{{ agent_data.example_input }}")
      print(result)

   Live Demo Results
   -----------------

   {% if agent_data.cache_available %}
   .. note::
      
      The following results are from **real agent execution** using actual LLM calls, cached for documentation purposes.
      
      * **Generated**: {{ agent_data.cache_generated_at }}
      * **Duration**: {{ agent_data.execution_duration }}
      * **Token Usage**: {{ agent_data.token_usage }} tokens

   **Input:**

   .. code-block:: text

      {{ agent_data.example_input }}

   **Output:**

   .. code-block:: text

      {{ agent_data.example_output }}

   {% else %}
   .. warning::
      
      Cached execution data not available. Showing example capabilities.

   **Example Input:**

   .. code-block:: text

      {{ agent_data.example_input }}

   **Example Output:**

   .. code-block:: text

      {{ agent_data.example_output }}

   {% endif %}

   .. raw:: html

      <div class="agent-demo-metrics">
         <div class="metric">
            <div class="metric-value">{{ agent_data.execution_duration }}</div>
            <div class="metric-label">Execution Time</div>
         </div>
         <div class="metric">
            <div class="metric-value">{{ agent_data.token_usage }}</div>
            <div class="metric-label">Tokens Used</div>
         </div>
         <div class="metric">
            <div class="metric-value">{{ agent_data.agent_features|length }}</div>
            <div class="metric-label">Features</div>
         </div>
      </div>

   Architecture
   ------------

   The {{ agent_data.agent_name }} uses {{ agent_data.agent_architecture_details|lower }}.

   .. raw:: html

      <div class="agent-demo-architecture">
         <p><strong>Architecture:</strong> {{ agent_data.agent_architecture_details }}</p>
         <p><strong>Module:</strong> <code>{{ agent_data.agent_module_import }}</code></p>
         <p><strong>Class:</strong> <code>{{ agent_data.agent_class }}</code></p>
      </div>

   {% if agent_data.state_history %}
   State History
   -------------

   The agent maintains conversation state across interactions:

   .. raw:: html

      <div class="agent-demo-state">
         <h4>📊 State Updates</h4>
         <div id="state-history-viz" class="visualization-container">
            <p><em>Interactive state visualization will be available when JavaScript libraries are loaded.</em></p>
         </div>
         <script>
            // Store state history data for visualization
            window.agentStateHistory = {{ agent_data.state_history_json }};
         </script>
      </div>

   {% endif %}

   {% if agent_data.execution_trace %}
   Execution Trace
   ---------------

   Step-by-step execution trace:

   .. raw:: html

      <div class="agent-demo-trace">
         <h4>🔍 Execution Steps</h4>
         <div id="execution-trace-viz" class="visualization-container">
            <p><em>Interactive execution trace will be available when JavaScript libraries are loaded.</em></p>
         </div>
         <script>
            // Store execution trace data for visualization
            window.agentExecutionTrace = {{ agent_data.execution_trace_json }};
         </script>
      </div>

   {% endif %}

   Next Steps
   ----------

   * Learn more about :doc:`../../introduction/concepts`
   * Explore :doc:`../base/index` for core agent patterns
   * Check out :doc:`../react/index` for tool-enabled agents
   * Browse :doc:`../rag/index` for knowledge-based agents

   .. raw:: html

      </div> <!-- Close agent-demo-container -->

      <script>
         // Initialize agent demo visualizations when libraries are loaded
         document.addEventListener('DOMContentLoaded', function() {
            if (typeof AgentDemoVisualizer !== 'undefined') {
               AgentDemoVisualizer.initialize({
                  agentType: '{{ agent_type }}',
                  agentData: {
                     stateHistory: window.agentStateHistory,
                     executionTrace: window.agentExecutionTrace,
                     graphData: {{ agent_data.graph_data_json }}
                  }
               });
            }
         });
      </script>