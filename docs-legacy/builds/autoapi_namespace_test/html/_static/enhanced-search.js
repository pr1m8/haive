// Enhanced Search Functionality for Haive Documentation

document.addEventListener("DOMContentLoaded", function () {
  // Enhanced search with real-time suggestions
  const searchInput = document.querySelector(".search-bar input");
  if (searchInput) {
    let searchTimeout;

    searchInput.addEventListener("input", function () {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(() => {
        performEnhancedSearch(this.value);
      }, 300);
    });
  }

  // Enhanced copy button functionality
  initializeEnhancedCopyButtons();

  // Enhanced tab switching
  initializeEnhancedTabs();

  // Enhanced toggle buttons
  initializeEnhancedToggleButtons();

  // Enhanced navigation
  initializeEnhancedNavigation();
});

function performEnhancedSearch(query) {
  if (query.length < 2) return;

  // This would integrate with ReadTheDocs search or custom search
  console.log("Performing enhanced search for:", query);

  // Add search suggestions
  const suggestions = [
    "Agent",
    "SimpleAgent",
    "ReactAgent",
    "StateSchema",
    "AugLLMConfig",
    "BaseGraph",
    "Tool",
    "MultiAgent",
  ];

  const filteredSuggestions = suggestions.filter((s) =>
    s.toLowerCase().includes(query.toLowerCase()),
  );

  showSearchSuggestions(filteredSuggestions);
}

function showSearchSuggestions(suggestions) {
  const existingSuggestions = document.querySelector(".search-suggestions");
  if (existingSuggestions) {
    existingSuggestions.remove();
  }

  if (suggestions.length === 0) return;

  const searchBar = document.querySelector(".search-bar");
  if (!searchBar) return;

  const suggestionsDiv = document.createElement("div");
  suggestionsDiv.className = "search-suggestions";
  suggestionsDiv.innerHTML = suggestions
    .map(
      (s) =>
        `<div class="search-suggestion" onclick="selectSearchSuggestion('${s}')">${s}</div>`,
    )
    .join("");

  searchBar.appendChild(suggestionsDiv);
}

function selectSearchSuggestion(suggestion) {
  const searchInput = document.querySelector(".search-bar input");
  if (searchInput) {
    searchInput.value = suggestion;
    searchInput.dispatchEvent(new Event("change"));
  }

  const suggestions = document.querySelector(".search-suggestions");
  if (suggestions) {
    suggestions.remove();
  }
}

function initializeEnhancedCopyButtons() {
  // Enhanced copy button with feedback
  document.querySelectorAll(".copybtn").forEach((button) => {
    button.addEventListener("click", function () {
      const originalText = this.textContent;
      this.textContent = "Copied!";
      this.style.background = "#28a745";

      setTimeout(() => {
        this.textContent = originalText;
        this.style.background = "";
      }, 2000);
    });
  });
}

function initializeEnhancedTabs() {
  // Enhanced tab switching with keyboard navigation
  document.querySelectorAll(".sphinx-tabs-tab").forEach((tab) => {
    tab.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        this.click();
      } else if (e.key === "ArrowRight") {
        const nextTab = this.nextElementSibling;
        if (nextTab) {
          nextTab.focus();
        }
      } else if (e.key === "ArrowLeft") {
        const prevTab = this.previousElementSibling;
        if (prevTab) {
          prevTab.focus();
        }
      }
    });
  });
}

function initializeEnhancedToggleButtons() {
  // Enhanced toggle buttons with smooth animations
  document.querySelectorAll(".toggle-button").forEach((button) => {
    button.addEventListener("click", function () {
      const content = this.nextElementSibling;
      if (content && content.classList.contains("toggle-content")) {
        if (content.style.display === "none") {
          content.style.display = "block";
          content.style.opacity = "0";
          content.style.transform = "translateY(-10px)";

          setTimeout(() => {
            content.style.transition = "opacity 0.3s ease, transform 0.3s ease";
            content.style.opacity = "1";
            content.style.transform = "translateY(0)";
          }, 10);

          this.textContent = this.textContent.replace("Show", "Hide");
          this.setAttribute("aria-expanded", "true");
        } else {
          content.style.transition = "opacity 0.3s ease, transform 0.3s ease";
          content.style.opacity = "0";
          content.style.transform = "translateY(-10px)";

          setTimeout(() => {
            content.style.display = "none";
          }, 300);

          this.textContent = this.textContent.replace("Hide", "Show");
          this.setAttribute("aria-expanded", "false");
        }
      }
    });
  });
}

function initializeEnhancedNavigation() {
  // Enhanced navigation with smooth scrolling
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });

  // Enhanced sidebar navigation
  const sidebar = document.querySelector(".bd-sidebar");
  if (sidebar) {
    // Add scroll spy functionality
    const sections = document.querySelectorAll("section[id]");
    const navLinks = sidebar.querySelectorAll('a[href^="#"]');

    window.addEventListener("scroll", () => {
      let current = "";
      sections.forEach((section) => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (pageYOffset >= sectionTop - 60) {
          current = section.getAttribute("id");
        }
      });

      navLinks.forEach((link) => {
        link.classList.remove("active");
        if (link.getAttribute("href") === `#${current}`) {
          link.classList.add("active");
        }
      });
    });
  }
}

// Enhanced keyboard navigation
document.addEventListener("keydown", function (e) {
  // Alt + S for search
  if (e.altKey && e.key === "s") {
    e.preventDefault();
    const searchInput = document.querySelector(".search-bar input");
    if (searchInput) {
      searchInput.focus();
    }
  }

  // Alt + H for home
  if (e.altKey && e.key === "h") {
    e.preventDefault();
    window.location.href = "/";
  }

  // Alt + N for navigation
  if (e.altKey && e.key === "n") {
    e.preventDefault();
    const sidebar = document.querySelector(".bd-sidebar");
    if (sidebar) {
      const firstLink = sidebar.querySelector("a");
      if (firstLink) {
        firstLink.focus();
      }
    }
  }
});

// Enhanced responsive behavior
window.addEventListener("resize", function () {
  // Adjust layout for mobile
  if (window.innerWidth < 768) {
    document.querySelectorAll(".sd-col").forEach((col) => {
      col.style.padding = "0.25rem";
    });
  } else {
    document.querySelectorAll(".sd-col").forEach((col) => {
      col.style.padding = "0.5rem";
    });
  }
});

// Enhanced error handling
window.addEventListener("error", function (e) {
  console.error("Documentation error:", e.error);

  // Show user-friendly error message
  const errorDiv = document.createElement("div");
  errorDiv.className = "error-message";
  errorDiv.innerHTML = `
        <strong>Documentation Error:</strong>
        Something went wrong. Please refresh the page or
        <a href="https://github.com/will-astley/haive/issues">report this issue</a>.
    `;
  errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #dc3545;
        color: white;
        padding: 1rem;
        border-radius: 0.375rem;
        z-index: 1000;
        max-width: 300px;
    `;

  document.body.appendChild(errorDiv);

  setTimeout(() => {
    errorDiv.remove();
  }, 5000);
});

// Enhanced loading indicators
function showLoadingIndicator() {
  const loader = document.createElement("div");
  loader.className = "loading-indicator";
  loader.innerHTML = `
        <div class="spinner"></div>
        <div>Loading documentation...</div>
    `;
  loader.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        padding: 2rem;
        border-radius: 0.375rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        text-align: center;
    `;

  document.body.appendChild(loader);
  return loader;
}

function hideLoadingIndicator(loader) {
  if (loader) {
    loader.remove();
  }
}
