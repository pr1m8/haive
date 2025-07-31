/**
 * Haive Agent Showcase JavaScript
 * Interactive, impressive agent gallery with smooth animations
 */

(function () {
  "use strict";

  // ==========================================================================
  // State Management
  // ==========================================================================

  const state = {
    agents: [],
    filteredAgents: [],
    currentView: "comfortable", // compact, comfortable, showcase
    currentCategory: "all",
    currentPage: 1,
    itemsPerPage: 12,
    searchQuery: "",
    loading: false,
  };

  // ==========================================================================
  // Agent Data Fetching & Processing
  // ==========================================================================

  async function fetchAgentData() {
    try {
      // Try to get data from the Haive extension first
      const showcaseData = window.haiveShowcaseData;
      if (showcaseData && showcaseData.agents) {
        return showcaseData.agents;
      }

      // Fallback: Parse from existing HTML content
      return parseAgentsFromHTML();
    } catch (error) {
      console.warn("Could not fetch agent data:", error);
      return generateMockAgents(); // For demo purposes
    }
  }

  function parseAgentsFromHTML() {
    const agents = [];

    // Look for existing agent cards or lists in the HTML
    document
      .querySelectorAll(".agent-item, .py.class, .toctree-l1")
      .forEach((element, index) => {
        const nameElement =
          element.querySelector(".reference, .py-class, a") || element;
        const name = nameElement.textContent?.trim() || `Agent ${index + 1}`;

        if (
          name.toLowerCase().includes("agent") ||
          name.toLowerCase().includes("bot") ||
          name.toLowerCase().includes("assistant")
        ) {
          agents.push({
            id: `agent-${index}`,
            name: name,
            category: inferCategory(name),
            description: `Advanced AI agent for ${inferCategory(name).toLowerCase()} tasks`,
            features: generateFeatures(),
            complexity: inferComplexity(name),
            package: inferPackage(name),
            hasTools: Math.random() > 0.3,
            hasMemory: Math.random() > 0.5,
            isActive: true,
          });
        }
      });

    return agents.length > 0 ? agents : generateMockAgents();
  }

  function generateMockAgents() {
    const categories = [
      "Research",
      "Conversation",
      "Analysis",
      "Creative",
      "Automation",
      "Game",
      "Tool",
    ];
    const names = [
      "ResearchMaster",
      "ConversationExpert",
      "DataAnalyzer",
      "CreativeWriter",
      "TaskAutomator",
      "GamePlayer",
      "ToolSpecialist",
      "DocumentProcessor",
      "CodeGenerator",
      "EmailAssistant",
      "SocialMediaBot",
      "TranslationAgent",
      "SentimentAnalyzer",
      "ImageProcessor",
      "VoiceAssistant",
      "SchedulingBot",
      "WeatherAgent",
      "NewsAggregator",
      "PriceTracker",
      "ContentModerator",
      "RecommendationEngine",
      "ChatBot",
      "SummaryGenerator",
      "QuestionAnswerer",
    ];

    return names.map((name, index) => ({
      id: `agent-${index}`,
      name: name,
      category: categories[index % categories.length],
      description: `Powerful AI agent specialized in ${categories[index % categories.length].toLowerCase()} tasks with advanced capabilities`,
      features: generateFeatures(),
      complexity: ["Simple", "Medium", "Complex"][index % 3],
      package: `haive-${["core", "agents", "tools", "games"][index % 4]}`,
      hasTools: Math.random() > 0.3,
      hasMemory: Math.random() > 0.4,
      isActive: Math.random() > 0.1,
    }));
  }

  function generateFeatures() {
    const allFeatures = [
      "Natural Language Processing",
      "Machine Learning",
      "Data Analysis",
      "Real-time Processing",
      "Multi-modal Input",
      "Memory Management",
      "Tool Integration",
      "API Connectivity",
      "Async Processing",
      "Error Handling",
      "Logging",
      "Caching",
      "Authentication",
    ];

    const numFeatures = Math.floor(Math.random() * 5) + 2;
    return allFeatures.sort(() => 0.5 - Math.random()).slice(0, numFeatures);
  }

  function inferCategory(name) {
    const categoryMap = {
      research: "Research",
      conversation: "Conversation",
      chat: "Conversation",
      game: "Game",
      tool: "Tool",
      data: "Analysis",
      creative: "Creative",
      automation: "Automation",
    };

    for (const [key, category] of Object.entries(categoryMap)) {
      if (name.toLowerCase().includes(key)) {
        return category;
      }
    }
    return "General";
  }

  function inferComplexity(name) {
    if (
      name.toLowerCase().includes("simple") ||
      name.toLowerCase().includes("basic")
    ) {
      return "Simple";
    }
    if (
      name.toLowerCase().includes("advanced") ||
      name.toLowerCase().includes("complex")
    ) {
      return "Complex";
    }
    return "Medium";
  }

  function inferPackage(name) {
    if (name.toLowerCase().includes("game")) return "haive-games";
    if (name.toLowerCase().includes("tool")) return "haive-tools";
    if (name.toLowerCase().includes("agent")) return "haive-agents";
    return "haive-core";
  }

  // ==========================================================================
  // UI Rendering
  // ==========================================================================

  function createShowcaseHTML() {
    return `
      <div class="hero-section">
        <div class="hero-content">
          <h1 class="hero-title">AI Agent Showcase</h1>
          <p class="hero-subtitle">Explore our comprehensive collection of intelligent agents</p>
          <div class="agent-count-display">
            <span>🤖</span>
            <span class="agent-count-number">${state.agents.length}</span>
            <span>Agents Built & Ready</span>
          </div>
        </div>
      </div>

      <div class="stats-dashboard">
        <div class="stats-card">
          <div class="stats-icon">🏗️</div>
          <div class="stats-number">${state.agents.length}</div>
          <div class="stats-label">Total Agents</div>
        </div>
        <div class="stats-card">
          <div class="stats-icon">📂</div>
          <div class="stats-number">${getUniqueCategories().length}</div>
          <div class="stats-label">Categories</div>
        </div>
        <div class="stats-card">
          <div class="stats-icon">⚡</div>
          <div class="stats-number">${state.agents.filter((a) => a.isActive).length}</div>
          <div class="stats-label">Active</div>
        </div>
        <div class="stats-card">
          <div class="stats-icon">🔧</div>
          <div class="stats-number">${state.agents.filter((a) => a.hasTools).length}</div>
          <div class="stats-label">With Tools</div>
        </div>
      </div>

      <div class="agent-gallery">
        <div class="search-container">
          <div class="search-icon">🔍</div>
          <input type="text" class="search-input" placeholder="Search agents..." />
        </div>

        <div class="gallery-controls">
          <div class="view-toggle">
            <button data-view="compact">Compact</button>
            <button data-view="comfortable" class="active">Comfortable</button>
            <button data-view="showcase">Showcase</button>
          </div>
          
          <div class="category-filter">
            <button class="category-chip active" data-category="all">All</button>
            ${getUniqueCategories()
              .map(
                (cat) =>
                  `<button class="category-chip" data-category="${cat.toLowerCase()}">${cat}</button>`,
              )
              .join("")}
          </div>
        </div>

        <div class="agents-grid grid-${state.currentView}" id="agents-container">
          <!-- Agent cards will be inserted here -->
        </div>

        <div class="gallery-pagination">
          <div class="pagination-info">
            Showing <span id="items-shown">0</span> of <span id="total-items">0</span> agents
          </div>
          <button class="load-more-btn" id="load-more" style="display: none;">
            Show More Agents
          </button>
        </div>
      </div>
    `;
  }

  function createAgentCard(agent) {
    const complexityColors = {
      Simple: "#24a148",
      Medium: "#f1c21b",
      Complex: "#da1e28",
    };

    return `
      <div class="agent-card" data-category="${agent.category.toLowerCase()}" data-agent-id="${agent.id}">
        <div class="agent-card-header">
          <div class="agent-name">
            ${agent.name}
            <span class="agent-category">${agent.category}</span>
          </div>
          <div class="agent-description">${agent.description}</div>
        </div>
        
        <div class="agent-card-body">
          <div class="agent-features">
            ${agent.features
              .slice(0, 3)
              .map(
                (feature) => `<span class="feature-badge">✨ ${feature}</span>`,
              )
              .join("")}
          </div>
          
          <div class="agent-stats">
            <div class="stat-item">
              <span class="stat-value" style="color: ${complexityColors[agent.complexity]}">${agent.complexity[0]}</span>
              <span class="stat-label">Complexity</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">${agent.hasTools ? "🔧" : "–"}</span>
              <span class="stat-label">Tools</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">${agent.hasMemory ? "🧠" : "–"}</span>
              <span class="stat-label">Memory</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">${agent.isActive ? "✅" : "⏸️"}</span>
              <span class="stat-label">Status</span>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  function renderAgents() {
    const container = document.getElementById("agents-container");
    if (!container) return;

    const startIndex = (state.currentPage - 1) * state.itemsPerPage;
    const endIndex = startIndex + state.itemsPerPage;
    const agentsToShow = state.filteredAgents.slice(0, endIndex);

    // Update grid class
    container.className = `agents-grid grid-${state.currentView}`;

    // Add loading shimmer
    if (state.loading) {
      container.innerHTML = Array(8)
        .fill(0)
        .map(
          () =>
            '<div class="agent-card loading-shimmer" style="height: 300px;"></div>',
        )
        .join("");
      return;
    }

    // Render agent cards
    container.innerHTML = agentsToShow.map(createAgentCard).join("");

    // Update pagination info
    document.getElementById("items-shown").textContent = agentsToShow.length;
    document.getElementById("total-items").textContent =
      state.filteredAgents.length;

    // Show/hide load more button
    const loadMoreBtn = document.getElementById("load-more");
    if (loadMoreBtn) {
      loadMoreBtn.style.display =
        agentsToShow.length < state.filteredAgents.length ? "block" : "none";
    }

    // Animate in
    setTimeout(() => {
      container.querySelectorAll(".agent-card").forEach((card, index) => {
        card.style.animationDelay = `${index * 50}ms`;
        card.style.animation = "fadeInUp 500ms ease-out forwards";
      });
    }, 50);
  }

  function getUniqueCategories() {
    return [...new Set(state.agents.map((agent) => agent.category))].sort();
  }

  // ==========================================================================
  // Event Handlers
  // ==========================================================================

  function setupEventListeners() {
    // View toggle
    document.querySelectorAll(".view-toggle button").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        document
          .querySelectorAll(".view-toggle button")
          .forEach((b) => b.classList.remove("active"));
        e.target.classList.add("active");
        state.currentView = e.target.dataset.view;
        renderAgents();
      });
    });

    // Category filter
    document.querySelectorAll(".category-chip").forEach((chip) => {
      chip.addEventListener("click", (e) => {
        document
          .querySelectorAll(".category-chip")
          .forEach((c) => c.classList.remove("active"));
        e.target.classList.add("active");
        state.currentCategory = e.target.dataset.category;
        filterAgents();
        renderAgents();
      });
    });

    // Search
    const searchInput = document.querySelector(".search-input");
    if (searchInput) {
      searchInput.addEventListener(
        "input",
        debounce((e) => {
          state.searchQuery = e.target.value.toLowerCase();
          filterAgents();
          renderAgents();
        }, 300),
      );
    }

    // Load more
    const loadMoreBtn = document.getElementById("load-more");
    if (loadMoreBtn) {
      loadMoreBtn.addEventListener("click", () => {
        state.currentPage++;
        renderAgents();
      });
    }

    // Agent card clicks
    document.addEventListener("click", (e) => {
      const card = e.target.closest(".agent-card");
      if (card) {
        const agentId = card.dataset.agentId;
        const agent = state.agents.find((a) => a.id === agentId);
        if (agent) {
          showAgentDetails(agent);
        }
      }
    });
  }

  function filterAgents() {
    state.filteredAgents = state.agents.filter((agent) => {
      const matchesCategory =
        state.currentCategory === "all" ||
        agent.category.toLowerCase() === state.currentCategory;
      const matchesSearch =
        state.searchQuery === "" ||
        agent.name.toLowerCase().includes(state.searchQuery) ||
        agent.description.toLowerCase().includes(state.searchQuery) ||
        agent.features.some((f) => f.toLowerCase().includes(state.searchQuery));
      return matchesCategory && matchesSearch;
    });

    state.currentPage = 1; // Reset pagination
  }

  function showAgentDetails(agent) {
    // Create modal or navigate to agent page
    console.log("Show details for:", agent);
    // For now, just log - could implement modal or navigation
  }

  // ==========================================================================
  // Utilities
  // ==========================================================================

  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  function addPulseAnimation() {
    const countNumber = document.querySelector(".agent-count-number");
    if (countNumber) {
      countNumber.style.animation = "pulse 2s infinite";
    }
  }

  // ==========================================================================
  // Initialization
  // ==========================================================================

  async function init() {
    // Load agent data
    state.loading = true;
    state.agents = await fetchAgentData();
    state.loading = false;

    filterAgents();

    // Find the main content area and inject our showcase
    const mainContent =
      document.querySelector(".rst-content, .content, main, .main") ||
      document.querySelector("body");

    if (mainContent) {
      // Create showcase container
      const showcaseContainer = document.createElement("div");
      showcaseContainer.innerHTML = createShowcaseHTML();

      // Insert at the beginning of main content
      mainContent.insertBefore(showcaseContainer, mainContent.firstChild);

      // Setup interactivity
      setupEventListeners();
      renderAgents();
      addPulseAnimation();

      console.log(
        `🚀 Agent Showcase initialized with ${state.agents.length} agents`,
      );
    }
  }

  // ==========================================================================
  // Auto-initialize when DOM is ready
  // ==========================================================================

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  // Export for external use
  window.HaiveShowcase = {
    state,
    renderAgents,
    addAgent: (agent) => {
      state.agents.push(agent);
      filterAgents();
      renderAgents();
    },
  };
})();
