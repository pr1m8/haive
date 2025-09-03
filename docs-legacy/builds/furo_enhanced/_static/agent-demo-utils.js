/**
 * Agent Demo Visualization Utils
 *
 * Comprehensive utilities for visualizing agent execution data including:
 * - Mermaid graph visualization
 * - Message/tool conversation flows
 * - State history timelines
 * - Token usage charts
 * - Interactive execution traces
 */

class AgentDemoVisualizer {
  constructor() {
    this.mermaidLoaded = false;
    this.d3Loaded = false;
    this.initializeMermaid();
  }

  /**
   * Initialize Mermaid for graph visualization
   */
  async initializeMermaid() {
    if (typeof mermaid === "undefined") {
      // Load Mermaid if not available
      const script = document.createElement("script");
      script.src =
        "https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js";
      script.onload = () => {
        mermaid.initialize({
          startOnLoad: true,
          theme: "default",
          themeVariables: {
            primaryColor: "#0066cc",
            primaryTextColor: "#ffffff",
            primaryBorderColor: "#0066cc",
            lineColor: "#666666",
            secondaryColor: "#f0f0f0",
            tertiaryColor: "#ffffff",
          },
        });
        this.mermaidLoaded = true;
      };
      document.head.appendChild(script);
    } else {
      this.mermaidLoaded = true;
    }
  }

  /**
   * Initialize all visualizations for an agent demo
   */
  static initialize(config) {
    const visualizer = new AgentDemoVisualizer();

    // Initialize different visualization types
    if (config.agentData.stateHistory) {
      visualizer.createStateHistoryVisualization(config.agentData.stateHistory);
    }

    if (config.agentData.executionTrace) {
      visualizer.createExecutionTraceVisualization(
        config.agentData.executionTrace,
      );
    }

    if (config.agentData.graphData) {
      visualizer.createGraphVisualization(config.agentData.graphData);
    }

    // Create message flow visualization from state history
    if (config.agentData.stateHistory) {
      visualizer.createMessageFlowVisualization(config.agentData.stateHistory);
    }
  }

  /**
   * Create Mermaid graph visualization from agent graph data
   */
  createGraphVisualization(graphData) {
    const container = document.getElementById("agent-graph-viz");
    if (!container) return;

    // Generate Mermaid diagram from graph data
    const mermaidCode = this.generateMermaidFromGraphData(graphData);

    if (this.mermaidLoaded) {
      container.innerHTML = `<div class="mermaid">${mermaidCode}</div>`;
      mermaid.init(undefined, container.querySelector(".mermaid"));
    } else {
      // Retry when Mermaid loads
      setTimeout(() => this.createGraphVisualization(graphData), 100);
    }
  }

  /**
   * Generate Mermaid diagram code from agent graph data
   */
  generateMermaidFromGraphData(graphData) {
    if (!graphData || !graphData.nodes) {
      return `graph TD
                A[Agent Start] --> B[LLM Processing]
                B --> C[Response Generation]
                C --> D[Agent End]
                style A fill:#e1f5fe
                style B fill:#f3e5f5
                style C fill:#e8f5e8
                style D fill:#fff3e0`;
    }

    // Build Mermaid from actual graph data
    let mermaid = "graph TD\n";

    // Add nodes
    graphData.nodes.forEach((node) => {
      const nodeId = node.id || node.name;
      const nodeLabel = node.label || node.name || nodeId;
      const nodeStyle = this.getNodeStyle(node.type);

      mermaid += `    ${nodeId}[${nodeLabel}]\n`;
      if (nodeStyle) {
        mermaid += `    style ${nodeId} ${nodeStyle}\n`;
      }
    });

    // Add edges
    if (graphData.edges) {
      graphData.edges.forEach((edge) => {
        const fromId = edge.from || edge.source;
        const toId = edge.to || edge.target;
        const label = edge.label ? `|${edge.label}|` : "";

        mermaid += `    ${fromId} -->${label} ${toId}\n`;
      });
    }

    return mermaid;
  }

  /**
   * Get Mermaid node styling based on node type
   */
  getNodeStyle(nodeType) {
    const styles = {
      start: "fill:#e1f5fe,stroke:#0277bd",
      end: "fill:#fff3e0,stroke:#f57c00",
      llm: "fill:#f3e5f5,stroke:#7b1fa2",
      tool: "fill:#e8f5e8,stroke:#388e3c",
      decision: "fill:#fef7e0,stroke:#f9a825",
      agent: "fill:#e3f2fd,stroke:#1976d2",
    };
    return styles[nodeType] || styles["agent"];
  }

  /**
   * Create message flow visualization from conversation history
   */
  createMessageFlowVisualization(stateHistory) {
    const container = document.getElementById("message-flow-viz");
    if (!container) return;

    // Extract messages from state history
    const messages = this.extractMessagesFromState(stateHistory);

    // Create interactive message flow
    const messageFlow = this.createMessageFlowHTML(messages);
    container.innerHTML = messageFlow;

    // Add interactivity
    this.addMessageFlowInteractivity(container);
  }

  /**
   * Extract messages from agent state history
   */
  extractMessagesFromState(stateHistory) {
    const messages = [];

    stateHistory.forEach((stateSnapshot) => {
      const state = stateSnapshot.state;

      // Look for messages in different formats
      if (state.messages && Array.isArray(state.messages)) {
        messages.push(...state.messages);
      } else if (state.output && typeof state.output === "string") {
        // Parse messages from output string
        const parsedMessages = this.parseMessagesFromOutput(state.output);
        messages.push(...parsedMessages);
      }
    });

    return this.deduplicateMessages(messages);
  }

  /**
   * Parse messages from agent output string
   */
  parseMessagesFromOutput(output) {
    const messages = [];

    // Look for HumanMessage and AIMessage patterns
    const humanMessagePattern = /HumanMessage\(content='([^']+)'/g;
    const aiMessagePattern = /AIMessage\(content="([^"]+)"/g;

    let match;

    // Extract human messages
    while ((match = humanMessagePattern.exec(output)) !== null) {
      messages.push({
        type: "human",
        content: match[1],
        timestamp: new Date().toISOString(),
      });
    }

    // Extract AI messages
    while ((match = aiMessagePattern.exec(output)) !== null) {
      messages.push({
        type: "ai",
        content: match[1],
        timestamp: new Date().toISOString(),
      });
    }

    return messages;
  }

  /**
   * Remove duplicate messages
   */
  deduplicateMessages(messages) {
    const seen = new Set();
    return messages.filter((msg) => {
      const key = `${msg.type}:${msg.content}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  /**
   * Create HTML for message flow visualization
   */
  createMessageFlowHTML(messages) {
    if (!messages.length) {
      return '<p class="no-messages">No messages found in execution trace</p>';
    }

    let html = '<div class="message-flow-container">';

    messages.forEach((message, index) => {
      const messageClass =
        message.type === "human" ? "human-message" : "ai-message";
      const icon = message.type === "human" ? "👤" : "🤖";
      const sender = message.type === "human" ? "Human" : "Assistant";

      html += `
                <div class="message-item ${messageClass}" data-index="${index}">
                    <div class="message-header">
                        <span class="message-icon">${icon}</span>
                        <span class="message-sender">${sender}</span>
                        <span class="message-timestamp">${this.formatTimestamp(message.timestamp)}</span>
                    </div>
                    <div class="message-content">
                        <div class="message-text">${this.escapeHtml(message.content)}</div>
                        ${this.createMessageMetadata(message)}
                    </div>
                </div>
            `;
    });

    html += "</div>";

    return html;
  }

  /**
   * Create metadata section for messages
   */
  createMessageMetadata(message) {
    let metadata = '<div class="message-metadata">';

    if (message.token_usage) {
      metadata += `<span class="token-count">Tokens: ${message.token_usage.total_tokens}</span>`;
    }

    if (message.model_name) {
      metadata += `<span class="model-name">Model: ${message.model_name}</span>`;
    }

    if (message.finish_reason) {
      metadata += `<span class="finish-reason">Finish: ${message.finish_reason}</span>`;
    }

    metadata += "</div>";

    return metadata;
  }

  /**
   * Add interactivity to message flow
   */
  addMessageFlowInteractivity(container) {
    // Add click handlers for message expansion
    container.querySelectorAll(".message-item").forEach((item) => {
      item.addEventListener("click", (e) => {
        item.classList.toggle("expanded");
      });
    });

    // Add copy functionality
    container.querySelectorAll(".message-text").forEach((textElement) => {
      textElement.addEventListener("dblclick", (e) => {
        navigator.clipboard.writeText(textElement.textContent);
        this.showToast("Message copied to clipboard");
      });
    });
  }

  /**
   * Create state history timeline visualization
   */
  createStateHistoryVisualization(stateHistory) {
    const container = document.getElementById("state-history-viz");
    if (!container) return;

    const timeline = this.createTimelineHTML(stateHistory);
    container.innerHTML = timeline;

    // Add timeline interactivity
    this.addTimelineInteractivity(container);
  }

  /**
   * Create timeline HTML for state history
   */
  createTimelineHTML(stateHistory) {
    let html = '<div class="state-timeline">';

    stateHistory.forEach((snapshot, index) => {
      const timestamp = new Date(snapshot.timestamp);
      const isActive = index === stateHistory.length - 1;

      html += `
                <div class="timeline-item ${isActive ? "active" : ""}" data-step="${snapshot.step}">
                    <div class="timeline-marker"></div>
                    <div class="timeline-content">
                        <div class="timeline-header">
                            <span class="timeline-step">Step ${snapshot.step}</span>
                            <span class="timeline-time">${this.formatTimestamp(timestamp)}</span>
                        </div>
                        <div class="timeline-state">
                            ${this.createStatePreview(snapshot.state)}
                        </div>
                    </div>
                </div>
            `;
    });

    html += "</div>";
    return html;
  }

  /**
   * Create state preview for timeline
   */
  createStatePreview(state) {
    let preview = '<div class="state-preview">';

    Object.keys(state).forEach((key) => {
      if (
        key === "output" &&
        typeof state[key] === "string" &&
        state[key].length > 100
      ) {
        preview += `<div class="state-field"><strong>${key}:</strong> <span class="truncated">${state[key].substring(0, 100)}...</span></div>`;
      } else if (typeof state[key] === "object") {
        preview += `<div class="state-field"><strong>${key}:</strong> <span class="object-type">[${Array.isArray(state[key]) ? "Array" : "Object"}]</span></div>`;
      } else {
        preview += `<div class="state-field"><strong>${key}:</strong> ${this.escapeHtml(String(state[key]))}</div>`;
      }
    });

    preview += "</div>";
    return preview;
  }

  /**
   * Add timeline interactivity
   */
  addTimelineInteractivity(container) {
    container.querySelectorAll(".timeline-item").forEach((item) => {
      item.addEventListener("click", () => {
        // Expand/collapse state details
        item.classList.toggle("expanded");
      });
    });
  }

  /**
   * Create execution trace visualization
   */
  createExecutionTraceVisualization(executionTrace) {
    const container = document.getElementById("execution-trace-viz");
    if (!container) return;

    if (!executionTrace.length) {
      container.innerHTML =
        '<p class="no-trace">No execution trace available</p>';
      return;
    }

    const trace = this.createTraceHTML(executionTrace);
    container.innerHTML = trace;
  }

  /**
   * Create trace HTML
   */
  createTraceHTML(executionTrace) {
    let html = '<div class="execution-trace">';

    executionTrace.forEach((step) => {
      const stepClass = step.action === "start" ? "trace-start" : "trace-end";

      html += `
                <div class="trace-step ${stepClass}">
                    <div class="trace-marker"></div>
                    <div class="trace-content">
                        <div class="trace-header">
                            <span class="trace-node">${step.node}</span>
                            <span class="trace-action">${step.action}</span>
                            <span class="trace-time">${this.formatTimestamp(step.timestamp)}</span>
                        </div>
                        ${step.data ? `<div class="trace-data">${JSON.stringify(step.data, null, 2)}</div>` : ""}
                    </div>
                </div>
            `;
    });

    html += "</div>";
    return html;
  }

  /**
   * Utility functions
   */
  formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString();
  }

  escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  showToast(message) {
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
      toast.remove();
    }, 3000);
  }
}

// Export for use in other modules
window.AgentDemoVisualizer = AgentDemoVisualizer;
