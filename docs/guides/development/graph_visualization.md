# Graph Visualization Guide for Haive Documentation

This guide covers how to implement graph visualizations in Haive documentation using the cached agent execution data and visualization framework.

## 🎯 Overview

The Haive documentation system includes a comprehensive graph visualization framework that can display:

- Agent execution graphs
- State transition diagrams
- Tool routing visualizations
- Message flow charts
- Mermaid diagrams

## 🏗️ Architecture

### Core Components

1. **JavaScript Visualizer** (`agent-demo-utils.js`)
2. **CSS Styling** (`agent-demo-visualizations.css`)
3. **Cached Graph Data** (from agent execution)
4. **Jinja2 Templates** (for dynamic content)
5. **Mermaid Integration** (for flowcharts)

## 📊 Graph Data Structure

### Agent Graph Data

```json
{
  "has_graph": true,
  "graph_type": "react_agent",
  "nodes": [
    { "id": "agent_node", "type": "agent_node" },
    { "id": "tool_node", "type": "tool_node" }
  ],
  "edges": [{ "from": "agent_node", "to": "tool_node" }],
  "mermaid_available": true
}
```

### Execution Trace Data

```json
{
  "execution_trace": [
    {
      "step": 1,
      "node": "agent_node",
      "action": "start",
      "timestamp": "2025-07-18T12:00:00",
      "data": {}
    },
    {
      "step": 2,
      "node": "tool_node",
      "action": "execute",
      "timestamp": "2025-07-18T12:00:01",
      "output": "345"
    }
  ]
}
```

## 🎨 Visualization Types

### 1. Basic Agent Graph

**Template Pattern**:

```rst
.. jinja:: agent_demo
   :ctx: {"agent_type": "react", "include_graph": true}

   {% set agent_data = get_agent_demo_context(agent_type) %}

   Agent Architecture
   ==================

   {% if agent_data.graph_data and agent_data.graph_data.has_graph %}
   .. raw:: html

       <div class="agent-graph-container">
           <div id="agent-graph-{{ agent_type }}" class="graph-display"></div>
           <div class="graph-controls">
               <button onclick="resetGraph('{{ agent_type }}')">Reset View</button>
               <button onclick="toggleLabels('{{ agent_type }}')">Toggle Labels</button>
           </div>
       </div>

       <script>
       document.addEventListener('DOMContentLoaded', function() {
           const graphData = {{ agent_data.graph_data|tojson }};
           const visualizer = new AgentDemoVisualizer();
           visualizer.createGraphVisualization(graphData, 'agent-graph-{{ agent_type }}');
       });
       </script>

   **Graph Properties**:
   - Nodes: {{ agent_data.graph_data.nodes|length }}
   - Edges: {{ agent_data.graph_data.edges|length }}
   - Type: {{ agent_data.graph_data.graph_type }}
   {% else %}
   *This agent doesn't expose graph structure.*
   {% endif %}
```

### 2. Interactive Mermaid Diagrams

**Template Pattern**:

```rst
.. jinja:: agent_demo
   :ctx: {"agent_type": "react", "mermaid": true}

   {% set agent_data = get_agent_demo_context(agent_type) %}

   Execution Flow
   ==============

   {% if agent_data.graph_data.mermaid_available %}
   .. raw:: html

       <div class="mermaid-container">
           <div class="mermaid" id="mermaid-{{ agent_type }}">
           graph TD
               Start([User Input])
               {% for node in agent_data.graph_data.nodes %}
               {{ node.id }}[{{ node.type.title().replace('_', ' ') }}]
               {% endfor %}
               End([Response])

               Start --> agent_node
               {% for edge in agent_data.graph_data.edges %}
               {{ edge.from }} --> {{ edge.to }}
               {% endfor %}
               {% for node in agent_data.graph_data.nodes %}
               {% if loop.last %}
               {{ node.id }} --> End
               {% endif %}
               {% endfor %}
           </div>
       </div>

       <script>
       // Initialize Mermaid with custom theme
       mermaid.initialize({
           startOnLoad: true,
           theme: 'default',
           flowchart: {
               curve: 'basis',
               padding: 20
           }
       });
       </script>
   {% endif %}
```

### 3. State Transition Visualization

**Template Pattern**:

```rst
.. jinja:: agent_demo
   :ctx: {"agent_type": "react", "show_state_transitions": true}

   {% set agent_data = get_agent_demo_context(agent_type) %}

   State Transitions
   =================

   {% if agent_data.execution_data.executions[0].state_history %}
   .. raw:: html

       <div class="state-timeline-container">
           <div id="state-timeline-{{ agent_type }}" class="timeline-display"></div>
       </div>

       <script>
       document.addEventListener('DOMContentLoaded', function() {
           const stateHistory = {{ agent_data.execution_data.executions[0].state_history|tojson }};
           const visualizer = new AgentDemoVisualizer();
           visualizer.createStateTimelineVisualization(stateHistory, 'state-timeline-{{ agent_type }}');
       });
       </script>

   **State Changes**:
   {% for state in agent_data.execution_data.executions[0].state_history %}
   {{ loop.index }}. **{{ state.timestamp }}** - Step {{ state.step }}
   {% endfor %}
   {% endif %}
```

### 4. Tool Routing Diagram

**Template Pattern**:

```rst
.. jinja:: agent_demo
   :ctx: {"agent_type": "react", "show_tool_routing": true}

   {% set agent_data = get_agent_demo_context(agent_type) %}

   Tool Routing
   ============

   {% if agent_data.tool_calls %}
   .. raw:: html

       <div class="tool-routing-container">
           <div class="mermaid">
           graph LR
               Input([User Query])
               Agent[ReactAgent]
               {% for call in agent_data.tool_calls %}
               {{ call.tool_name }}[{{ call.tool_name.title() }}]
               {% endfor %}
               Output([Response])

               Input --> Agent
               {% for call in agent_data.tool_calls %}
               Agent --> {{ call.tool_name }}
               {{ call.tool_name }} --> Agent
               {% endfor %}
               Agent --> Output
           </div>
       </div>

       <script>
       mermaid.initialize({startOnLoad: true});
       </script>

   **Tool Execution Order**:
   {% for call in agent_data.tool_calls %}
   {{ loop.index }}. **{{ call.tool_name }}** - {{ call.tool_args }}
   {% endfor %}
   {% endif %}
```

### 5. Message Flow Visualization

**Template Pattern**:

```rst
.. jinja:: agent_demo
   :ctx: {"agent_type": "simple", "show_message_flow": true}

   {% set agent_data = get_agent_demo_context(agent_type) %}

   Message Flow
   ============

   {% if agent_data.visualization_data.conversation_history %}
   .. raw:: html

       <div class="message-flow-container">
           <div id="message-flow-{{ agent_type }}" class="message-display"></div>
           <div class="message-controls">
               <button onclick="playMessageFlow('{{ agent_type }}')">Play Flow</button>
               <button onclick="pauseMessageFlow('{{ agent_type }}')">Pause</button>
               <button onclick="resetMessageFlow('{{ agent_type }}')">Reset</button>
           </div>
       </div>

       <script>
       document.addEventListener('DOMContentLoaded', function() {
           const messageHistory = {{ agent_data.visualization_data.conversation_history|tojson }};
           const visualizer = new AgentDemoVisualizer();
           visualizer.createMessageFlowVisualization(messageHistory, 'message-flow-{{ agent_type }}');
       });
       </script>

   **Message Types**:
   {% for msg in agent_data.visualization_data.conversation_history %}
   - **{{ msg.type.title() }}**: {{ msg.content[:50] }}...
   {% endfor %}
   {% endif %}
```

## 🎛️ Advanced Graph Features

### Multi-Agent Coordination

**Template Pattern**:

```rst
.. jinja:: agent_demo
   :ctx: {"agent_type": "multi", "show_coordination": true}

   {% set agent_data = get_agent_demo_context(agent_type) %}

   Multi-Agent Coordination
   ========================

   .. raw:: html

       <div class="coordination-container">
           <div class="mermaid">
           graph TB
               subgraph "Coordinator"
               Coord[Coordinator Agent]
               end

               subgraph "Worker Agents"
               Agent1[Planning Agent]
               Agent2[Execution Agent]
               Agent3[Validation Agent]
               end

               subgraph "Shared State"
               State[(Shared State)]
               end

               Coord --> Agent1
               Coord --> Agent2
               Coord --> Agent3

               Agent1 --> State
               Agent2 --> State
               Agent3 --> State

               State --> Agent1
               State --> Agent2
               State --> Agent3
           </div>
       </div>

       <script>
       mermaid.initialize({startOnLoad: true});
       </script>
```

### Dynamic Graph Updates

**Template Pattern**:

```rst
.. jinja:: agent_demo
   :ctx: {"agent_type": "react", "dynamic_graph": true}

   {% set agent_data = get_agent_demo_context(agent_type) %}

   Dynamic Graph Evolution
   =======================

   .. raw:: html

       <div class="dynamic-graph-container">
           <div id="dynamic-graph-{{ agent_type }}" class="graph-display"></div>
           <div class="graph-timeline">
               <input type="range" id="graph-timeline-{{ agent_type }}"
                      min="0" max="{{ agent_data.execution_data.executions[0].execution_trace|length - 1 }}"
                      value="0" class="timeline-slider">
               <div class="timeline-labels">
                   <span>Start</span>
                   <span>End</span>
               </div>
           </div>
       </div>

       <script>
       document.addEventListener('DOMContentLoaded', function() {
           const executionTrace = {{ agent_data.execution_data.executions[0].execution_trace|tojson }};
           const visualizer = new AgentDemoVisualizer();
           visualizer.createDynamicGraphVisualization(executionTrace, 'dynamic-graph-{{ agent_type }}');

           // Timeline control
           const slider = document.getElementById('graph-timeline-{{ agent_type }}');
           slider.addEventListener('input', function() {
               visualizer.updateGraphToStep(parseInt(this.value));
           });
       });
       </script>
```

## 📱 Responsive Graph Design

### Mobile-Friendly Graphs

**CSS Pattern**:

```css
/* Mobile-first responsive design */
.graph-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .graph-container {
    padding: 10px;
  }

  .graph-display {
    height: 300px;
    font-size: 12px;
  }

  .graph-controls {
    flex-direction: column;
    gap: 10px;
  }
}

@media (max-width: 480px) {
  .graph-display {
    height: 250px;
    font-size: 10px;
  }
}
```

### Touch-Friendly Controls

**Template Pattern**:

```rst
.. raw:: html

    <div class="mobile-friendly-controls">
        <button class="touch-button" onclick="zoomIn('{{ agent_type }}')">
            <span class="icon">🔍+</span>
            <span class="label">Zoom In</span>
        </button>
        <button class="touch-button" onclick="zoomOut('{{ agent_type }}')">
            <span class="icon">🔍-</span>
            <span class="label">Zoom Out</span>
        </button>
        <button class="touch-button" onclick="resetView('{{ agent_type }}')">
            <span class="icon">🔄</span>
            <span class="label">Reset</span>
        </button>
    </div>
```

## 🔧 JavaScript API Reference

### AgentDemoVisualizer Class

```javascript
class AgentDemoVisualizer {
  constructor(options = {}) {
    this.options = {
      theme: "default",
      animations: true,
      interactive: true,
      ...options,
    };
  }

  // Create basic graph visualization
  createGraphVisualization(graphData, containerId) {
    // Implementation creates interactive graph
  }

  // Create Mermaid diagram
  createMermaidDiagram(mermaidCode, containerId) {
    // Implementation renders Mermaid
  }

  // Create state timeline
  createStateTimelineVisualization(stateHistory, containerId) {
    // Implementation creates timeline
  }

  // Create message flow
  createMessageFlowVisualization(messageHistory, containerId) {
    // Implementation creates message flow
  }

  // Create dynamic graph with timeline
  createDynamicGraphVisualization(executionTrace, containerId) {
    // Implementation creates dynamic graph
  }
}
```

### Available Methods

```javascript
// Graph manipulation
visualizer.zoomIn(containerId);
visualizer.zoomOut(containerId);
visualizer.resetView(containerId);
visualizer.fitToView(containerId);

// Animation control
visualizer.playAnimation(containerId);
visualizer.pauseAnimation(containerId);
visualizer.stopAnimation(containerId);

// Data updates
visualizer.updateGraphData(newData);
visualizer.highlightNode(nodeId);
visualizer.highlightPath(nodeIds);
```

## 🎨 Styling and Themes

### Default Theme

```css
:root {
  --graph-node-color: #4a90e2;
  --graph-edge-color: #666;
  --graph-text-color: #333;
  --graph-bg-color: #f8f9fa;
  --graph-highlight-color: #e74c3c;
}

.graph-node {
  fill: var(--graph-node-color);
  stroke: var(--graph-edge-color);
  stroke-width: 2px;
}

.graph-edge {
  stroke: var(--graph-edge-color);
  stroke-width: 1.5px;
  marker-end: url(#arrowhead);
}

.graph-text {
  fill: var(--graph-text-color);
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  font-size: 12px;
}
```

### Dark Theme

```css
[data-theme="dark"] {
  --graph-node-color: #61dafb;
  --graph-edge-color: #ccc;
  --graph-text-color: #f8f9fa;
  --graph-bg-color: #2d3748;
  --graph-highlight-color: #ffd700;
}
```

## 📋 Graph Implementation Checklist

### Before Adding Graphs

- [ ] Verify graph data is available in cache
- [ ] Check if agent supports graph visualization
- [ ] Determine appropriate visualization type
- [ ] Plan responsive design needs

### During Implementation

- [ ] Add graph container with unique ID
- [ ] Include necessary JavaScript and CSS
- [ ] Set up graph data in template
- [ ] Add interactive controls if needed
- [ ] Test responsive behavior

### After Implementation

- [ ] Test graph rendering
- [ ] Verify all controls work
- [ ] Test on mobile devices
- [ ] Ensure accessibility compliance
- [ ] Add fallback for graph-less agents

## 🔍 Debugging Graph Issues

### Common Problems

1. **Graph not rendering**: Check JavaScript console for errors
2. **Data not loading**: Verify cache data and template context
3. **Styling issues**: Check CSS specificity and theme variables
4. **Mobile issues**: Test responsive breakpoints
5. **Performance**: Optimize for large graphs

### Debug Commands

```bash
# Check if graph data exists
poetry run python -c "
from docs.scripts.agent_demos.agent_cache_loader import AgentCacheLoader
loader = AgentCacheLoader()
data = loader.get_agent_demo_context('react')
print('Graph data:', data.get('graph_data', {}))
"

# Test JavaScript visualization
# Open browser console and run:
console.log(AgentDemoVisualizer);
```

## 🎯 Best Practices

### Performance

- Use SVG for scalable graphics
- Implement lazy loading for large graphs
- Optimize animations for smooth performance
- Cache graph layouts when possible

### Accessibility

- Add ARIA labels to graph elements
- Provide keyboard navigation
- Include alternative text descriptions
- Support screen readers

### User Experience

- Provide clear visual feedback
- Include helpful controls and labels
- Make graphs interactive but not overwhelming
- Ensure mobile usability

---

This guide provides everything needed to implement comprehensive graph visualizations in Haive documentation. The combination of cached data, Jinja2 templates, and JavaScript visualization creates rich, interactive documentation that helps users understand agent behavior and architecture.
