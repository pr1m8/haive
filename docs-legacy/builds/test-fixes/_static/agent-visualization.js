/**
 * Agent Graph Visualization & State History JavaScript
 * Interactive components for visualizing agent workflows and execution
 */

// Agent Graph Visualization Class
class AgentGraphVisualizer {
  constructor(containerId, graphData) {
    this.container = document.getElementById(containerId);
    this.graphData = graphData;
    this.svg = null;
    this.currentStep = 0;
    this.isPlaying = false;
    this.playInterval = null;

    this.init();
  }

  init() {
    this.createGraphContainer();
    this.renderGraph();
    this.setupControls();
  }

  createGraphContainer() {
    this.container.innerHTML = `
            <div class="agent-graph-header">
                <h3 class="agent-graph-title">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="18" cy="5" r="3"></circle>
                        <circle cx="6" cy="12" r="3"></circle>
                        <circle cx="18" cy="19" r="3"></circle>
                        <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
                        <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
                    </svg>
                    Agent Workflow Graph
                </h3>
                <div class="agent-graph-controls">
                    <button class="graph-control-button" data-action="reset">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="1 4 1 10 7 10"></polyline>
                            <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"></path>
                        </svg>
                        Reset
                    </button>
                    <button class="graph-control-button" data-action="step">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polygon points="5,3 19,12 5,21"></polygon>
                        </svg>
                        Step
                    </button>
                    <button class="graph-control-button" data-action="play">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polygon points="5,3 19,12 5,21"></polygon>
                        </svg>
                        Play
                    </button>
                    <button class="graph-control-button" data-action="export">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                            <polyline points="7,10 12,15 17,10"></polyline>
                            <line x1="12" y1="15" x2="12" y2="3"></line>
                        </svg>
                        Export
                    </button>
                </div>
            </div>
            <div class="agent-graph-canvas" id="graph-canvas-${this.container.id}">
                <svg class="agent-graph-svg" id="graph-svg-${this.container.id}">
                    <defs>
                        <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                            <polygon points="0 0, 10 3.5, 0 7" />
                        </marker>
                    </defs>
                </svg>
            </div>
            <div class="graph-legend">
                <h4 class="legend-title">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                        <line x1="9" y1="9" x2="15" y2="15"></line>
                        <line x1="15" y1="9" x2="9" y2="15"></line>
                    </svg>
                    Node Types
                </h4>
                <div class="legend-items">
                    <div class="legend-item">
                        <div class="legend-symbol start"></div>
                        <span>Start Node</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-symbol agent"></div>
                        <span>Agent Node</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-symbol tool"></div>
                        <span>Tool Node</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-symbol conditional"></div>
                        <span>Conditional Edge</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-symbol end"></div>
                        <span>End Node</span>
                    </div>
                </div>
            </div>
        `;

    this.svg = document.getElementById(`graph-svg-${this.container.id}`);
  }

  renderGraph() {
    const nodes = this.graphData.nodes;
    const edges = this.graphData.edges;

    // Clear existing content
    this.svg.innerHTML = this.svg.querySelector("defs").outerHTML;

    // Calculate layout
    const layout = this.calculateLayout(nodes, edges);

    // Render edges first (so they appear behind nodes)
    edges.forEach((edge) => {
      this.renderEdge(edge, layout);
    });

    // Render nodes
    nodes.forEach((node) => {
      this.renderNode(node, layout);
    });
  }

  calculateLayout(nodes, edges) {
    // Simple layout algorithm - arrange nodes in levels
    const levels = this.assignLevels(nodes, edges);
    const layout = {};

    const canvasWidth = this.svg.clientWidth || 600;
    const canvasHeight = this.svg.clientHeight || 400;
    const nodeWidth = 120;
    const nodeHeight = 60;
    const levelHeight = canvasHeight / (Object.keys(levels).length + 1);

    Object.keys(levels).forEach((level, levelIndex) => {
      const nodesInLevel = levels[level];
      const levelWidth = canvasWidth / (nodesInLevel.length + 1);

      nodesInLevel.forEach((nodeId, nodeIndex) => {
        layout[nodeId] = {
          x: levelWidth * (nodeIndex + 1) - nodeWidth / 2,
          y: levelHeight * (levelIndex + 1) - nodeHeight / 2,
          width: nodeWidth,
          height: nodeHeight,
        };
      });
    });

    return layout;
  }

  assignLevels(nodes, edges) {
    const levels = { 0: [] };
    const nodeLevel = {};

    // Find start nodes
    const startNodes = nodes.filter(
      (node) =>
        node.type === "start" || !edges.some((edge) => edge.target === node.id),
    );

    startNodes.forEach((node) => {
      levels[0].push(node.id);
      nodeLevel[node.id] = 0;
    });

    // Assign levels using BFS
    let currentLevel = 0;
    let hasChanges = true;

    while (hasChanges) {
      hasChanges = false;
      currentLevel++;
      levels[currentLevel] = [];

      edges.forEach((edge) => {
        if (
          nodeLevel[edge.source] === currentLevel - 1 &&
          !nodeLevel.hasOwnProperty(edge.target)
        ) {
          levels[currentLevel].push(edge.target);
          nodeLevel[edge.target] = currentLevel;
          hasChanges = true;
        }
      });
    }

    // Remove empty levels
    Object.keys(levels).forEach((level) => {
      if (levels[level].length === 0) {
        delete levels[level];
      }
    });

    return levels;
  }

  renderNode(node, layout) {
    const pos = layout[node.id];
    if (!pos) return;

    const nodeGroup = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "g",
    );
    nodeGroup.setAttribute("class", "graph-node");
    nodeGroup.setAttribute("data-node-id", node.id);
    nodeGroup.setAttribute("transform", `translate(${pos.x}, ${pos.y})`);

    // Node rectangle
    const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rect.setAttribute("class", `node-rect ${node.type}-node`);
    rect.setAttribute("width", pos.width);
    rect.setAttribute("height", pos.height);

    // Node text
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute(
      "class",
      `node-text ${["start", "end", "tool", "agent"].includes(node.type) ? "light-text" : ""}`,
    );
    text.setAttribute("x", pos.width / 2);
    text.setAttribute("y", pos.height / 2);
    text.textContent = node.label || node.id;

    nodeGroup.appendChild(rect);
    nodeGroup.appendChild(text);

    // Add click handler
    nodeGroup.addEventListener("click", () => {
      this.onNodeClick(node);
    });

    this.svg.appendChild(nodeGroup);
  }

  renderEdge(edge, layout) {
    const sourcePos = layout[edge.source];
    const targetPos = layout[edge.target];

    if (!sourcePos || !targetPos) return;

    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("class", `graph-edge ${edge.type || ""}`);
    path.setAttribute("data-edge-id", `${edge.source}-${edge.target}`);

    const startX = sourcePos.x + sourcePos.width / 2;
    const startY = sourcePos.y + sourcePos.height;
    const endX = targetPos.x + targetPos.width / 2;
    const endY = targetPos.y;

    // Create curved path
    const controlY = startY + (endY - startY) / 2;
    const pathData = `M ${startX} ${startY} Q ${startX} ${controlY} ${endX} ${endY}`;

    path.setAttribute("d", pathData);

    this.svg.appendChild(path);
  }

  setupControls() {
    const controls = this.container.querySelectorAll(".graph-control-button");

    controls.forEach((button) => {
      button.addEventListener("click", () => {
        const action = button.getAttribute("data-action");
        this.handleControlAction(action, button);
      });
    });
  }

  handleControlAction(action, button) {
    switch (action) {
      case "reset":
        this.resetVisualization();
        break;
      case "step":
        this.stepForward();
        break;
      case "play":
        this.togglePlayback(button);
        break;
      case "export":
        this.exportGraph();
        break;
    }
  }

  resetVisualization() {
    this.currentStep = 0;
    this.clearActiveStates();
  }

  stepForward() {
    if (this.currentStep < this.graphData.executionTrace.length) {
      this.highlightStep(this.currentStep);
      this.currentStep++;
    }
  }

  togglePlayback(button) {
    if (this.isPlaying) {
      this.stopPlayback(button);
    } else {
      this.startPlayback(button);
    }
  }

  startPlayback(button) {
    this.isPlaying = true;
    button.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="6" y="4" width="4" height="16"></rect>
                <rect x="14" y="4" width="4" height="16"></rect>
            </svg>
            Pause
        `;
    button.classList.add("active");

    this.playInterval = setInterval(() => {
      if (this.currentStep >= this.graphData.executionTrace.length) {
        this.stopPlayback(button);
        return;
      }
      this.stepForward();
    }, 1500);
  }

  stopPlayback(button) {
    this.isPlaying = false;
    button.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="5,3 19,12 5,21"></polygon>
            </svg>
            Play
        `;
    button.classList.remove("active");

    if (this.playInterval) {
      clearInterval(this.playInterval);
      this.playInterval = null;
    }
  }

  highlightStep(stepIndex) {
    const step = this.graphData.executionTrace[stepIndex];
    if (!step) return;

    // Clear previous highlights
    this.clearActiveStates();

    // Highlight current node
    const node = this.svg.querySelector(`[data-node-id="${step.nodeId}"]`);
    if (node) {
      node.classList.add("active");
    }

    // Highlight current edge
    if (step.fromNodeId) {
      const edge = this.svg.querySelector(
        `[data-edge-id="${step.fromNodeId}-${step.nodeId}"]`,
      );
      if (edge) {
        edge.classList.add("active");
      }
    }
  }

  clearActiveStates() {
    this.svg.querySelectorAll(".active").forEach((element) => {
      element.classList.remove("active");
    });
  }

  onNodeClick(node) {
    // Show node details in a modal or sidebar
    this.showNodeDetails(node);
  }

  showNodeDetails(node) {
    // Create a simple tooltip or modal
    const existingTooltip = document.querySelector(".node-tooltip");
    if (existingTooltip) {
      existingTooltip.remove();
    }

    const tooltip = document.createElement("div");
    tooltip.className = "node-tooltip";
    tooltip.innerHTML = `
            <div class="tooltip-header">
                <h4>${node.label || node.id}</h4>
                <span class="badge">${node.type}</span>
            </div>
            <div class="tooltip-content">
                <p><strong>Type:</strong> ${node.type}</p>
                <p><strong>Description:</strong> ${node.description || "No description available"}</p>
                ${node.config ? `<p><strong>Config:</strong> <code>${JSON.stringify(node.config, null, 2)}</code></p>` : ""}
            </div>
        `;

    document.body.appendChild(tooltip);

    // Position tooltip
    const rect = event.target.getBoundingClientRect();
    tooltip.style.position = "fixed";
    tooltip.style.left = rect.right + 10 + "px";
    tooltip.style.top = rect.top + "px";
    tooltip.style.zIndex = "10000";
    tooltip.style.background = "var(--color-background-primary)";
    tooltip.style.border = "1px solid var(--color-background-border)";
    tooltip.style.borderRadius = "8px";
    tooltip.style.padding = "16px";
    tooltip.style.maxWidth = "300px";
    tooltip.style.boxShadow = "var(--shadow-lg)";

    // Auto-remove after 5 seconds
    setTimeout(() => {
      if (tooltip.parentNode) {
        tooltip.remove();
      }
    }, 5000);
  }

  exportGraph() {
    // Export as SVG
    const svgData = new XMLSerializer().serializeToString(this.svg);
    const svgBlob = new Blob([svgData], {
      type: "image/svg+xml;charset=utf-8",
    });
    const svgUrl = URL.createObjectURL(svgBlob);

    const downloadLink = document.createElement("a");
    downloadLink.href = svgUrl;
    downloadLink.download = "agent-graph.svg";
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
    URL.revokeObjectURL(svgUrl);
  }
}

// State History Visualizer Class
class StateHistoryVisualizer {
  constructor(containerId, stateHistory) {
    this.container = document.getElementById(containerId);
    this.stateHistory = stateHistory;
    this.currentState = 0;

    this.init();
  }

  init() {
    this.render();
    this.setupInteractions();
  }

  render() {
    this.container.innerHTML = `
            <div class="state-history-header">
                <h3 class="state-history-title">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"></circle>
                        <polyline points="12,6 12,12 16,14"></polyline>
                    </svg>
                    State Evolution Timeline
                </h3>
                <div class="state-history-controls">
                    <span class="current-state-indicator">Step ${this.currentState + 1} of ${this.stateHistory.length}</span>
                </div>
            </div>
            <div class="state-history-timeline">
                <div class="timeline">
                    ${this.renderTimelineItems()}
                </div>
            </div>
        `;
  }

  renderTimelineItems() {
    return this.stateHistory
      .map(
        (state, index) => `
            <div class="timeline-item ${index === this.currentState ? "active" : ""}" data-step="${index}">
                <div class="timeline-step">
                    <div class="timeline-step-number">${index + 1}</div>
                    <div class="timeline-step-content">
                        <div class="timeline-step-title">${state.action || "State Update"}</div>
                        <div class="timeline-step-description">${state.description || "Agent state was modified"}</div>
                        <div class="timeline-step-meta">
                            <span class="timestamp">${new Date(state.timestamp).toLocaleTimeString()}</span>
                            <span class="duration">${state.duration || "0"}ms</span>
                        </div>
                    </div>
                </div>
                ${this.renderStateDiff(state, index)}
            </div>
        `,
      )
      .join("");
  }

  renderStateDiff(state, index) {
    if (index === 0) {
      return `
                <div class="state-diff">
                    <div class="state-diff-header">Initial State</div>
                    <div class="state-diff-content">${this.formatStateData(state.state)}</div>
                </div>
            `;
    }

    const previousState = this.stateHistory[index - 1];
    const diff = this.calculateStateDiff(previousState.state, state.state);

    return `
            <div class="state-diff">
                <div class="state-diff-header">State Changes</div>
                <div class="state-diff-content">${this.formatStateDiff(diff)}</div>
            </div>
        `;
  }

  calculateStateDiff(oldState, newState) {
    const diff = {
      added: {},
      removed: {},
      modified: {},
    };

    // Find added and modified
    Object.keys(newState).forEach((key) => {
      if (!(key in oldState)) {
        diff.added[key] = newState[key];
      } else if (
        JSON.stringify(oldState[key]) !== JSON.stringify(newState[key])
      ) {
        diff.modified[key] = {
          old: oldState[key],
          new: newState[key],
        };
      }
    });

    // Find removed
    Object.keys(oldState).forEach((key) => {
      if (!(key in newState)) {
        diff.removed[key] = oldState[key];
      }
    });

    return diff;
  }

  formatStateDiff(diff) {
    let html = "";

    if (Object.keys(diff.added).length > 0) {
      html += '<div class="diff-section"><strong>Added:</strong><br>';
      Object.keys(diff.added).forEach((key) => {
        html += `<span class="diff-added">+ ${key}: ${this.formatValue(diff.added[key])}</span><br>`;
      });
      html += "</div>";
    }

    if (Object.keys(diff.modified).length > 0) {
      html += '<div class="diff-section"><strong>Modified:</strong><br>';
      Object.keys(diff.modified).forEach((key) => {
        html += `<span class="diff-modified">~ ${key}: ${this.formatValue(diff.modified[key].old)} → ${this.formatValue(diff.modified[key].new)}</span><br>`;
      });
      html += "</div>";
    }

    if (Object.keys(diff.removed).length > 0) {
      html += '<div class="diff-section"><strong>Removed:</strong><br>';
      Object.keys(diff.removed).forEach((key) => {
        html += `<span class="diff-removed">- ${key}: ${this.formatValue(diff.removed[key])}</span><br>`;
      });
      html += "</div>";
    }

    return html || "<em>No changes detected</em>";
  }

  formatStateData(state) {
    return JSON.stringify(state, null, 2);
  }

  formatValue(value) {
    if (typeof value === "string") {
      return `"${value}"`;
    }
    return JSON.stringify(value);
  }

  setupInteractions() {
    const timelineItems = this.container.querySelectorAll(".timeline-item");

    timelineItems.forEach((item) => {
      item.addEventListener("click", () => {
        const step = parseInt(item.getAttribute("data-step"));
        this.setCurrentState(step);
      });
    });
  }

  setCurrentState(step) {
    // Remove active class from all items
    this.container.querySelectorAll(".timeline-item").forEach((item) => {
      item.classList.remove("active");
    });

    // Add active class to selected item
    const targetItem = this.container.querySelector(`[data-step="${step}"]`);
    if (targetItem) {
      targetItem.classList.add("active");
      this.currentState = step;

      // Update indicator
      const indicator = this.container.querySelector(
        ".current-state-indicator",
      );
      if (indicator) {
        indicator.textContent = `Step ${step + 1} of ${this.stateHistory.length}`;
      }
    }
  }
}

// Execution Trace Visualizer
class ExecutionTraceVisualizer {
  constructor(containerId, traceData) {
    this.container = document.getElementById(containerId);
    this.traceData = traceData;

    this.init();
  }

  init() {
    this.render();
    this.setupInteractions();
  }

  render() {
    this.container.innerHTML = `
            <div class="trace-header">
                <h3 class="state-history-title">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                        <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
                    </svg>
                    Execution Trace
                </h3>
                <div class="performance-metrics">
                    <div class="metric-card">
                        <div class="metric-value">${this.traceData.length}</div>
                        <div class="metric-label">Total Steps</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${this.calculateTotalTime()}ms</div>
                        <div class="metric-label">Total Time</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${this.calculateAverageTime()}ms</div>
                        <div class="metric-label">Avg Step Time</div>
                    </div>
                </div>
            </div>
            <div class="trace-content">
                ${this.renderTraceSteps()}
            </div>
        `;
  }

  renderTraceSteps() {
    return this.traceData
      .map(
        (step, index) => `
            <div class="trace-step" data-step="${index}">
                <div class="trace-step-header">
                    <div class="trace-step-info">
                        <span class="trace-step-badge">${step.type || "Action"}</span>
                        <span class="trace-step-title">${step.action || step.node}</span>
                        <span class="trace-step-time">${step.duration || 0}ms</span>
                    </div>
                    <span class="trace-step-expand">▶</span>
                </div>
                <div class="trace-step-details">
                    ${
                      step.input
                        ? `
                        <div class="trace-input">
                            <div class="trace-input-header">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                                    <polyline points="14,2 14,8 20,8"></polyline>
                                    <line x1="16" y1="13" x2="8" y2="13"></line>
                                    <line x1="16" y1="17" x2="8" y2="17"></line>
                                </svg>
                                Input
                            </div>
                            <div class="trace-data">${this.formatTraceData(step.input)}</div>
                        </div>
                    `
                        : ""
                    }
                    ${
                      step.output
                        ? `
                        <div class="trace-output">
                            <div class="trace-output-header">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                                    <polyline points="14,2 14,8 20,8"></polyline>
                                    <line x1="16" y1="13" x2="8" y2="13"></line>
                                    <line x1="16" y1="17" x2="8" y2="17"></line>
                                </svg>
                                Output
                            </div>
                            <div class="trace-data">${this.formatTraceData(step.output)}</div>
                        </div>
                    `
                        : ""
                    }
                </div>
            </div>
        `,
      )
      .join("");
  }

  formatTraceData(data) {
    return JSON.stringify(data, null, 2);
  }

  calculateTotalTime() {
    return this.traceData.reduce(
      (total, step) => total + (step.duration || 0),
      0,
    );
  }

  calculateAverageTime() {
    const total = this.calculateTotalTime();
    return Math.round(total / this.traceData.length);
  }

  setupInteractions() {
    const stepHeaders = this.container.querySelectorAll(".trace-step-header");

    stepHeaders.forEach((header) => {
      header.addEventListener("click", () => {
        const step = header.closest(".trace-step");
        step.classList.toggle("expanded");
      });
    });
  }
}

// Initialize visualizations when DOM is ready
document.addEventListener("DOMContentLoaded", function () {
  // Look for visualization containers and initialize them
  initializeAgentVisualizations();
});

function initializeAgentVisualizations() {
  // Initialize graph visualizers
  document.querySelectorAll("[data-agent-graph]").forEach((container) => {
    const graphData = JSON.parse(container.getAttribute("data-agent-graph"));
    new AgentGraphVisualizer(container.id, graphData);
  });

  // Initialize state history visualizers
  document.querySelectorAll("[data-state-history]").forEach((container) => {
    const stateHistory = JSON.parse(
      container.getAttribute("data-state-history"),
    );
    new StateHistoryVisualizer(container.id, stateHistory);
  });

  // Initialize execution trace visualizers
  document.querySelectorAll("[data-execution-trace]").forEach((container) => {
    const traceData = JSON.parse(
      container.getAttribute("data-execution-trace"),
    );
    new ExecutionTraceVisualizer(container.id, traceData);
  });
}

// Export classes for external use
window.AgentGraphVisualizer = AgentGraphVisualizer;
window.StateHistoryVisualizer = StateHistoryVisualizer;
window.ExecutionTraceVisualizer = ExecutionTraceVisualizer;
