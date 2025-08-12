// Mermaid Configuration for Intense Furo Theme
// Custom styling and initialization for Mermaid diagrams

// Mermaid theme configuration
const mermaidConfig = {
  startOnLoad: true,
  theme: "neutral",
  themeVariables: {
    // Primary colors from Furo theme
    primaryColor: "#2563eb",
    primaryTextColor: "#ffffff",
    primaryBorderColor: "#1d4ed8",

    // Secondary colors
    secondaryColor: "#f8fafc",
    secondaryTextColor: "#1e293b",
    secondaryBorderColor: "#cbd5e1",

    // Tertiary colors
    tertiaryColor: "#e2e8f0",
    tertiaryTextColor: "#475569",
    tertiaryBorderColor: "#94a3b8",

    // Background and lines
    background: "#ffffff",
    mainBkg: "#f8fafc",
    secondBkg: "#e2e8f0",
    lineColor: "#cbd5e1",

    // Text styling
    textColor: "#1e293b",
    fontFamily: "ui-sans-serif, system-ui, sans-serif",
    fontSize: "14px",

    // Node styling
    nodeBorder: "#1d4ed8",
    clusterBkg: "#dbeafe",
    clusterBorder: "#3b82f6",

    // Flowchart specific
    edgeLabelBackground: "#ffffff",
    activeTaskBkgColor: "#2563eb",
    activeTaskBorderColor: "#1d4ed8",
    gridColor: "#e5e7eb",

    // Sequence diagram
    actorBkg: "#dbeafe",
    actorBorder: "#3b82f6",
    actorTextColor: "#1e293b",
    actorLineColor: "#9ca3af",
    signalColor: "#1e293b",
    signalTextColor: "#1e293b",

    // State diagram
    labelBoxBkgColor: "#dbeafe",
    labelBoxBorderColor: "#3b82f6",
    labelTextColor: "#1e293b",
    loopTextColor: "#1e293b",

    // Class diagram
    classText: "#1e293b",

    // Git diagram
    git0: "#2563eb",
    git1: "#10b981",
    git2: "#f59e0b",
    git3: "#ef4444",
    git4: "#8b5cf6",
    git5: "#06b6d4",
    git6: "#f97316",
    git7: "#84cc16",

    // Pie chart
    pie1: "#2563eb",
    pie2: "#10b981",
    pie3: "#f59e0b",
    pie4: "#ef4444",
    pie5: "#8b5cf6",
    pie6: "#06b6d4",
    pie7: "#f97316",
    pie8: "#84cc16",
    pie9: "#ec4899",
    pie10: "#14b8a6",
    pie11: "#f43f5e",
    pie12: "#6366f1",
  },

  // Flowchart configuration
  flowchart: {
    nodeSpacing: 50,
    rankSpacing: 50,
    curve: "basis",
    padding: 20,
    useMaxWidth: true,
    htmlLabels: true,
  },

  // Sequence diagram configuration
  sequence: {
    diagramMarginX: 50,
    diagramMarginY: 30,
    actorMargin: 50,
    width: 150,
    height: 65,
    boxMargin: 10,
    boxTextMargin: 5,
    noteMargin: 10,
    messageMargin: 35,
    mirrorActors: false,
    bottomMarginAdj: 1,
    useMaxWidth: true,
    rightAngles: false,
    showSequenceNumbers: true,
  },

  // Gantt configuration
  gantt: {
    titleTopMargin: 25,
    barHeight: 20,
    fontSizTitle: 16,
    fontSize: 11,
    fontFamily: "ui-sans-serif, system-ui, sans-serif",
    gridLineStartPadding: 35,
    leftPadding: 75,
    topPadding: 50,
    rightPadding: 25,
    bottomPadding: 25,
  },

  // State diagram configuration
  state: {
    dividerMargin: 10,
    sizeUnit: 5,
    padding: 8,
    textHeight: 10,
    titleShift: -15,
    noteMargin: 10,
    forkWidth: 70,
    forkHeight: 7,
    miniMumStateFontSize: 10,
    fontSizeFactor: 5.02,
    fontSize: 24,
  },

  // Class diagram configuration
  class: {
    titleTopMargin: 25,
    arrowMarkerAbsolute: false,
    dividerMargin: 10,
    padding: 5,
    textHeight: 10,
    defaultRenderer: "dagre-wrapper",
    nodeSpacing: 50,
    rankSpacing: 50,
    useMaxWidth: true,
    htmlLabels: false,
  },

  // Security level
  securityLevel: "loose",

  // Error handling
  logLevel: 1, // 1: debug, 2: info, 3: warn, 4: error, 5: fatal

  // Maximum text size
  maxTextSize: 50000,

  // Maximum number of edges
  maxEdges: 500,
};

// Initialize Mermaid with dark mode detection
function initializeMermaid() {
  // Check if dark mode is active (Furo theme detection)
  const isDarkMode =
    document.documentElement.dataset.theme === "dark" ||
    window.matchMedia("(prefers-color-scheme: dark)").matches;

  if (isDarkMode) {
    // Override theme variables for dark mode
    mermaidConfig.themeVariables = {
      ...mermaidConfig.themeVariables,
      primaryColor: "#60a5fa",
      primaryTextColor: "#000000",
      primaryBorderColor: "#3b82f6",

      secondaryColor: "#1e293b",
      secondaryTextColor: "#cbd5e1",
      secondaryBorderColor: "#475569",

      background: "#0f172a",
      mainBkg: "#1e293b",
      secondBkg: "#334155",
      lineColor: "#475569",
      textColor: "#cbd5e1",

      actorBkg: "#1e293b",
      actorBorder: "#60a5fa",
      actorTextColor: "#cbd5e1",

      labelBoxBkgColor: "#1e293b",
      labelBoxBorderColor: "#60a5fa",
      labelTextColor: "#cbd5e1",
    };
  }

  // Initialize Mermaid
  mermaid.initialize(mermaidConfig);
}

// Auto-initialize when DOM is ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initializeMermaid);
} else {
  initializeMermaid();
}

// Re-initialize when theme changes (Furo theme switcher)
const observer = new MutationObserver(function (mutations) {
  mutations.forEach(function (mutation) {
    if (
      mutation.type === "attributes" &&
      mutation.attributeName === "data-theme"
    ) {
      // Theme changed, re-initialize Mermaid
      setTimeout(initializeMermaid, 100);
    }
  });
});

observer.observe(document.documentElement, {
  attributes: true,
  attributeFilter: ["data-theme"],
});

// Helper function to create Mermaid diagrams programmatically
window.createMermaidDiagram = function (elementId, definition, config = {}) {
  const element = document.getElementById(elementId);
  if (!element) return;

  const mergedConfig = { ...mermaidConfig, ...config };
  mermaid
    .render(`mermaid-${elementId}`, definition, mergedConfig)
    .then((result) => {
      element.innerHTML = result.svg;
    });
};
