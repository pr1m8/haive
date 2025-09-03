/**
 * Haive Graph Visualizations
 * Missing JavaScript classes that are referenced in documentation
 * Version: 1.0
 */

// Agent Graph Visualizer
class AgentGraphVisualizer {
  constructor(containerId, graphData) {
    this.container = document.getElementById(containerId);
    this.data = graphData || {};

    if (!this.container) {
      console.warn(
        `AgentGraphVisualizer: Container '${containerId}' not found`,
      );
      return;
    }

    this.init();
  }

  init() {
    // Clear container and add loading state
    this.container.innerHTML = "";
    this.container.className = "haive-graph-container loading";

    // Create placeholder visualization
    this.renderPlaceholder();

    // TODO: Implement actual D3.js visualization
    console.log("AgentGraphVisualizer initialized with data:", this.data);
  }

  renderPlaceholder() {
    const placeholder = document.createElement("div");
    placeholder.className = "graph-placeholder enhanced";
    placeholder.innerHTML = `
            <div class="placeholder-content enhanced">
                <div class="graph-header">
                    <div class="placeholder-icon">🤖</div>
                    <div class="placeholder-text">Agent Execution Graph</div>
                    <div class="placeholder-subtext">Interactive workflow visualization</div>
                </div>
                <div class="graph-preview">
                    <svg viewBox="0 0 400 200" class="preview-svg">
                        <defs>
                            <linearGradient id="nodeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" style="stop-color:#0066cc;stop-opacity:1" />
                                <stop offset="100%" style="stop-color:#4da6ff;stop-opacity:1" />
                            </linearGradient>
                            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                                <polygon points="0 0, 10 3.5, 0 7" fill="#0066cc" />
                            </marker>
                        </defs>
                        <circle cx="70" cy="100" r="20" fill="url(#nodeGradient)" class="graph-node" />
                        <circle cx="170" cy="100" r="20" fill="url(#nodeGradient)" class="graph-node" />
                        <circle cx="270" cy="100" r="20" fill="url(#nodeGradient)" class="graph-node" />
                        <circle cx="330" cy="100" r="15" fill="#28a745" class="graph-node" />
                        <path d="M 90 100 L 150 100" stroke="#0066cc" stroke-width="2" marker-end="url(#arrowhead)" />
                        <path d="M 190 100 L 250 100" stroke="#0066cc" stroke-width="2" marker-end="url(#arrowhead)" />
                        <path d="M 290 100 L 315 100" stroke="#0066cc" stroke-width="2" marker-end="url(#arrowhead)" />
                        <text x="70" y="140" text-anchor="middle" class="node-label">Start</text>
                        <text x="170" y="140" text-anchor="middle" class="node-label">Process</text>
                        <text x="270" y="140" text-anchor="middle" class="node-label">Execute</text>
                        <text x="330" y="140" text-anchor="middle" class="node-label">End</text>
                    </svg>
                </div>
                <div class="graph-stats">
                    <div class="stat-item">
                        <span class="stat-label">Nodes:</span>
                        <span class="stat-value">${this.data.nodes?.length || 4}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Edges:</span>
                        <span class="stat-value">${this.data.edges?.length || 3}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Type:</span>
                        <span class="stat-value">${this.data.type || "Workflow"}</span>
                    </div>
                </div>
            </div>
        `;
    this.container.appendChild(placeholder);
    this.container.classList.remove("loading");
    this.addInteractivity();

    // Add basic styling
    const style = document.createElement("style");
    style.textContent = `
            .graph-placeholder {
                display: flex;
                align-items: center;
                justify-content: center;
                height: 300px;
                background: var(--haive-bg-secondary, #f8fafc);
                border: 1px solid var(--haive-border-primary, #e2e8f0);
                border-radius: 8px;
                color: var(--haive-text-secondary, #64748b);
            }
            .placeholder-content {
                text-align: center;
            }
            .placeholder-icon {
                font-size: 2rem;
                margin-bottom: 0.5rem;
            }
            .placeholder-text {
                font-weight: 600;
                margin-bottom: 0.25rem;
            }
            .placeholder-subtext {
                font-size: 0.875rem;
            }
            .graph-preview {
                margin: 1rem 0;
                background: white;
                border-radius: 8px;
                padding: 1rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .preview-svg {
                width: 100%;
                height: auto;
                max-height: 200px;
            }
            .graph-node {
                transition: transform 0.2s ease;
                cursor: pointer;
            }
            .graph-node:hover {
                transform: scale(1.1);
            }
            .node-label {
                font-size: 12px;
                fill: #64748b;
                font-family: system-ui, sans-serif;
            }
            .graph-stats {
                display: flex;
                justify-content: space-around;
                margin-top: 1rem;
                padding: 0.5rem;
                background: #f1f5f9;
                border-radius: 6px;
            }
            .stat-item {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 0.25rem;
            }
            .stat-label {
                font-size: 0.75rem;
                color: #64748b;
                font-weight: 500;
            }
            .stat-value {
                font-size: 1.25rem;
                color: #0066cc;
                font-weight: 600;
            }
        `;
    document.head.appendChild(style);
  }

  addInteractivity() {
    // Add hover effects and click handlers to nodes
    const nodes = this.container.querySelectorAll(".graph-node");
    nodes.forEach((node, index) => {
      node.addEventListener("mouseenter", () => {
        node.style.filter = "brightness(1.2)";
      });
      node.addEventListener("mouseleave", () => {
        node.style.filter = "brightness(1)";
      });
      node.addEventListener("click", () => {
        this.showNodeDetails(index);
      });
    });
  }

  showNodeDetails(nodeIndex) {
    // Show detailed information about the clicked node
    const nodeNames = ["Start", "Process", "Execute", "End"];
    const nodeDescriptions = [
      "Initial state and input processing",
      "Main logic execution and reasoning",
      "Tool calls and action execution",
      "Final output and state update",
    ];

    // Create a modal or tooltip (simple alert for now)
    const details = `Node: ${nodeNames[nodeIndex]}\nDescription: ${nodeDescriptions[nodeIndex]}`;

    // TODO: Replace with proper modal
    if (window.confirm(`${details}\n\nWould you like to see more details?`)) {
      // Could navigate to detailed documentation
      console.log(
        `Showing details for node ${nodeIndex}: ${nodeNames[nodeIndex]}`,
      );
    }
  }
}

// State History Visualizer
class StateHistoryVisualizer {
  constructor(containerId, stateData) {
    this.container = document.getElementById(containerId);
    this.data = stateData || {};

    if (!this.container) {
      console.warn(
        `StateHistoryVisualizer: Container '${containerId}' not found`,
      );
      return;
    }

    this.init();
  }

  init() {
    this.container.innerHTML = "";
    this.container.className = "haive-graph-container";

    const placeholder = document.createElement("div");
    placeholder.className = "graph-placeholder";
    placeholder.innerHTML = `
            <div class="placeholder-content">
                <div class="placeholder-icon">📈</div>
                <div class="placeholder-text">State History Timeline</div>
                <div class="placeholder-subtext">Timeline visualization coming soon</div>
            </div>
        `;
    this.container.appendChild(placeholder);

    console.log("StateHistoryVisualizer initialized with data:", this.data);
  }
}

// Execution Trace Visualizer
class ExecutionTraceVisualizer {
  constructor(containerId, traceData) {
    this.container = document.getElementById(containerId);
    this.data = traceData || {};

    if (!this.container) {
      console.warn(
        `ExecutionTraceVisualizer: Container '${containerId}' not found`,
      );
      return;
    }

    this.init();
  }

  init() {
    this.container.innerHTML = "";
    this.container.className = "haive-graph-container";

    const placeholder = document.createElement("div");
    placeholder.className = "graph-placeholder";
    placeholder.innerHTML = `
            <div class="placeholder-content">
                <div class="placeholder-icon">🔍</div>
                <div class="placeholder-text">Execution Trace</div>
                <div class="placeholder-subtext">Execution flow visualization coming soon</div>
            </div>
        `;
    this.container.appendChild(placeholder);

    console.log("ExecutionTraceVisualizer initialized with data:", this.data);
  }
}

// Auto-initialize visualizations on page load
document.addEventListener("DOMContentLoaded", function () {
  // Look for visualization containers and initialize them
  const containers = document.querySelectorAll(
    '[id*="graph"], [id*="trace"], [id*="history"]',
  );

  containers.forEach((container) => {
    const id = container.id;

    if (id.includes("graph")) {
      new AgentGraphVisualizer(id, {});
    } else if (id.includes("history")) {
      new StateHistoryVisualizer(id, {});
    } else if (id.includes("trace")) {
      new ExecutionTraceVisualizer(id, {});
    }
  });
});

// Export for use in other scripts
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    AgentGraphVisualizer,
    StateHistoryVisualizer,
    ExecutionTraceVisualizer,
  };
}
