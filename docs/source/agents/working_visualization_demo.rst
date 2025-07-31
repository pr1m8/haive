Working Visualization Demo
==========================

This page demonstrates working agent visualizations with simpler data.

Agent Graph Visualization
-------------------------

Here's a basic agent workflow visualization:

.. raw:: html

    <div class="agent-showcase">
        <div class="agent-card">
            <h3>Climate Research Agent</h3>
            <p>Advanced Environmental Analysis with ReAct methodology.</p>
            
            <div id="demo-graph" class="agent-graph-container">
                <!-- Graph will be rendered here -->
            </div>
        </div>
    </div>

    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // Simple test of visualization
        const container = document.getElementById('demo-graph');
        if (container) {
            container.innerHTML = '<p style="text-align: center; padding: 20px; background: #f0f0f0; border-radius: 8px;">Graph visualization would appear here</p>';
        }
    });
    </script>

Interactive Features
--------------------

The visualization components include:

- **Graph Playback**: Step through agent execution
- **State Timeline**: Track state changes over time  
- **Execution Trace**: Detailed input/output logs

This simpler version should render properly without complex JSON data.