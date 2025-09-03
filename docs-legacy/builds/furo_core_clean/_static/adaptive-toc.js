/**
 * Adaptive TOC for Haive Documentation
 * Works with Furo theme's checkbox-based navigation
 */

(function () {
  "use strict";

  // Configuration
  const CONFIG = {
    maxAutoExpandLevel: 2, // Auto-expand up to level 2
    collapseDistantItems: true, // Collapse items far from current
    rememberState: true, // Remember user's expand/collapse choices
    showRecentPages: true, // Show recently visited pages
    maxRecentPages: 5, // Number of recent pages to show
  };

  // State management
  const STATE_KEY = "haive-toc-state";
  const RECENT_KEY = "haive-recent-pages";

  class AdaptiveTOC {
    constructor() {
      this.checkboxes = document.querySelectorAll(".toctree-checkbox");
      this.currentItem = document.querySelector(".current");
      this.state = this.loadState();
      this.recentPages = this.loadRecentPages();
      this.init();
    }

    init() {
      if (!this.checkboxes.length) return;

      // Apply adaptive behavior
      this.applyAdaptiveBehavior();

      // Add recent pages section
      if (CONFIG.showRecentPages) {
        this.addRecentPagesSection();
      }

      // Track current page
      this.trackCurrentPage();

      // Add event listeners
      this.addEventListeners();

      // Add controls
      this.addTOCControls();
    }

    applyAdaptiveBehavior() {
      // First, restore user's saved state
      if (CONFIG.rememberState && this.state.expanded) {
        this.restoreState();
      }

      // Then apply adaptive rules
      this.checkboxes.forEach((checkbox) => {
        const item = checkbox.closest("li");
        const level = this.getItemLevel(item);
        const isParentOfCurrent = this.isParentOfCurrent(item);
        const isSiblingOfCurrent = this.isSiblingOfCurrent(item);

        // Don't override user's explicit choices
        if (this.state.userModified && this.state.userModified[item.id]) {
          return;
        }

        // Adaptive rules
        if (isParentOfCurrent) {
          checkbox.checked = true;
        } else if (level === 1) {
          // Always show top level
          checkbox.checked = true;
        } else if (level === 2 && isSiblingOfCurrent) {
          // Show siblings at level 2
          checkbox.checked = true;
        } else if (level > CONFIG.maxAutoExpandLevel) {
          // Collapse deep levels
          checkbox.checked = false;
        }
      });
    }

    getItemLevel(item) {
      let level = 0;
      let parent = item.parentElement;
      while (parent) {
        if (parent.classList.contains("toctree-l1")) level = 1;
        else if (parent.classList.contains("toctree-l2")) level = 2;
        else if (parent.classList.contains("toctree-l3")) level = 3;
        else if (parent.classList.contains("toctree-l4")) level = 4;
        parent = parent.parentElement;
      }
      return level || 1;
    }

    isParentOfCurrent(item) {
      return this.currentItem && item.contains(this.currentItem);
    }

    isSiblingOfCurrent(item) {
      if (!this.currentItem) return false;
      const currentParent = this.currentItem.parentElement;
      const itemParent = item.parentElement;
      return currentParent === itemParent;
    }

    addTOCControls() {
      const sidebar = document.querySelector(".sidebar-drawer");
      if (!sidebar) return;

      const controls = document.createElement("div");
      controls.className = "toc-controls";
      controls.innerHTML = `
                <button class="toc-control-btn" id="expand-all" title="Expand all sections">
                    <svg width="16" height="16" viewBox="0 0 16 16">
                        <path d="M1 8h14m-7-7v14" stroke="currentColor" stroke-width="2" fill="none"/>
                    </svg>
                </button>
                <button class="toc-control-btn" id="collapse-all" title="Collapse all sections">
                    <svg width="16" height="16" viewBox="0 0 16 16">
                        <path d="M1 8h14" stroke="currentColor" stroke-width="2" fill="none"/>
                    </svg>
                </button>
                <button class="toc-control-btn" id="reset-toc" title="Reset to default">
                    <svg width="16" height="16" viewBox="0 0 16 16">
                        <path d="M2 8a6 6 0 1 1 10.4 4.1l-.1.1m-2.3-8.2v4h4" stroke="currentColor" stroke-width="2" fill="none"/>
                    </svg>
                </button>
            `;

      // Insert controls after the search box
      const searchBox = sidebar.querySelector(".sidebar-search-container");
      if (searchBox) {
        searchBox.after(controls);
      } else {
        sidebar.prepend(controls);
      }

      // Add control event listeners
      document
        .getElementById("expand-all")
        .addEventListener("click", () => this.expandAll());
      document
        .getElementById("collapse-all")
        .addEventListener("click", () => this.collapseAll());
      document
        .getElementById("reset-toc")
        .addEventListener("click", () => this.resetTOC());
    }

    expandAll() {
      this.checkboxes.forEach((cb) => (cb.checked = true));
      this.saveState();
    }

    collapseAll() {
      this.checkboxes.forEach((cb) => (cb.checked = false));
      // Keep current section expanded
      this.expandCurrentSection();
      this.saveState();
    }

    resetTOC() {
      localStorage.removeItem(STATE_KEY);
      this.state = { expanded: {}, userModified: {} };
      this.applyAdaptiveBehavior();
    }

    expandCurrentSection() {
      if (!this.currentItem) return;

      let parent = this.currentItem.closest("li");
      while (parent) {
        const checkbox = parent.querySelector(
          ":scope > input.toctree-checkbox",
        );
        if (checkbox) {
          checkbox.checked = true;
        }
        parent = parent.parentElement.closest("li");
      }
    }

    addRecentPagesSection() {
      if (!this.recentPages.length) return;

      const sidebar = document.querySelector(".sidebar-tree");
      if (!sidebar) return;

      const recentSection = document.createElement("div");
      recentSection.className = "recent-pages-section";
      recentSection.innerHTML = `
                <h4 class="recent-pages-title">Recent Pages</h4>
                <ul class="recent-pages-list">
                    ${this.recentPages
                      .map(
                        (page) => `
                        <li><a href="${page.url}">${page.title}</a></li>
                    `,
                      )
                      .join("")}
                </ul>
            `;

      sidebar.before(recentSection);
    }

    trackCurrentPage() {
      const currentLink = document.querySelector(".current > a");
      if (!currentLink) return;

      const pageData = {
        url: currentLink.href,
        title: currentLink.textContent.trim(),
        timestamp: Date.now(),
      };

      // Update recent pages
      this.recentPages = this.recentPages.filter((p) => p.url !== pageData.url);
      this.recentPages.unshift(pageData);
      this.recentPages = this.recentPages.slice(0, CONFIG.maxRecentPages);

      this.saveRecentPages();
    }

    addEventListeners() {
      // Track manual checkbox changes
      this.checkboxes.forEach((checkbox) => {
        checkbox.addEventListener("change", (e) => {
          const item = e.target.closest("li");
          if (item.id) {
            if (!this.state.userModified) {
              this.state.userModified = {};
            }
            this.state.userModified[item.id] = true;
          }
          this.saveState();
        });
      });

      // Handle window focus to refresh state
      window.addEventListener("focus", () => {
        this.state = this.loadState();
        this.recentPages = this.loadRecentPages();
      });
    }

    saveState() {
      if (!CONFIG.rememberState) return;

      const expanded = {};
      this.checkboxes.forEach((checkbox) => {
        const item = checkbox.closest("li");
        if (item.id && checkbox.checked) {
          expanded[item.id] = true;
        }
      });

      this.state.expanded = expanded;
      localStorage.setItem(STATE_KEY, JSON.stringify(this.state));
    }

    loadState() {
      if (!CONFIG.rememberState) return { expanded: {}, userModified: {} };

      try {
        const saved = localStorage.getItem(STATE_KEY);
        return saved ? JSON.parse(saved) : { expanded: {}, userModified: {} };
      } catch (e) {
        return { expanded: {}, userModified: {} };
      }
    }

    restoreState() {
      if (!this.state.expanded) return;

      this.checkboxes.forEach((checkbox) => {
        const item = checkbox.closest("li");
        if (item.id && this.state.expanded[item.id]) {
          checkbox.checked = true;
        }
      });
    }

    saveRecentPages() {
      localStorage.setItem(RECENT_KEY, JSON.stringify(this.recentPages));
    }

    loadRecentPages() {
      try {
        const saved = localStorage.getItem(RECENT_KEY);
        return saved ? JSON.parse(saved) : [];
      } catch (e) {
        return [];
      }
    }
  }

  // Initialize when DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => new AdaptiveTOC());
  } else {
    new AdaptiveTOC();
  }
})();
