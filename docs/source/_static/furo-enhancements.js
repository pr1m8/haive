// Furo Theme Enhancements for PyAutoDoc
// Custom JavaScript for intense theming and interactive features

document.addEventListener("DOMContentLoaded", function () {
  console.log("🚀 Furo enhancements loaded!");

  // Initialize all enhancements
  initializeAPIEnhancements();
  initializeInteractiveElements();
  initializeSearchEnhancements();
  initializeScrollEffects();
  initializeKeyboardShortcuts();
});

function initializeAPIEnhancements() {
  console.log("🔧 Initializing API documentation enhancements...");

  // Add hover effects to API objects
  document
    .querySelectorAll(".py.class, .py.function, .py.method")
    .forEach((element) => {
      element.addEventListener("mouseenter", function () {
        this.style.transform = "translateY(-2px)";
        this.style.boxShadow = "0 8px 16px rgba(37, 99, 235, 0.15)";
      });

      element.addEventListener("mouseleave", function () {
        this.style.transform = "translateY(0)";
        this.style.boxShadow = "none";
      });
    });

  // Enhance Pydantic model displays
  document.querySelectorAll(".pydantic-model").forEach((model) => {
    // Add expand/collapse for large models
    const content = model.querySelector(".pydantic-model-content");
    if (content && content.offsetHeight > 400) {
      addExpandCollapseButton(model, content);
    }
  });

  // Add copy buttons to code signatures
  document.querySelectorAll(".sig").forEach((sig) => {
    addCopyButton(sig);
  });
}

function initializeInteractiveElements() {
  console.log("⚡ Initializing interactive elements...");

  // Enhance sphinx-design cards
  document.querySelectorAll(".sd-card").forEach((card) => {
    card.addEventListener("mouseenter", function () {
      this.style.transform = "translateY(-4px) scale(1.02)";
      this.style.boxShadow = "0 20px 25px -5px rgba(0, 0, 0, 0.15)";
    });

    card.addEventListener("mouseleave", function () {
      this.style.transform = "translateY(0) scale(1)";
      this.style.boxShadow = "0 4px 6px -1px rgba(0, 0, 0, 0.1)";
    });
  });

  // Enhance buttons with ripple effect
  document.querySelectorAll(".sd-btn, .btn, button").forEach((button) => {
    button.addEventListener("click", createRippleEffect);
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });

        // Add highlight effect
        target.style.backgroundColor = "rgba(37, 99, 235, 0.1)";
        target.style.borderRadius = "8px";
        target.style.transition = "background-color 0.5s ease";

        setTimeout(() => {
          target.style.backgroundColor = "";
        }, 2000);
      }
    });
  });
}

function initializeSearchEnhancements() {
  console.log("🔍 Initializing search enhancements...");

  // Add search keyboard shortcut (Ctrl/Cmd + K)
  document.addEventListener("keydown", function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key === "k") {
      e.preventDefault();
      const searchInput = document.querySelector(
        'input[type="search"], .search-input',
      );
      if (searchInput) {
        searchInput.focus();
        searchInput.select();
      }
    }
  });

  // Enhance search results with highlighting
  const observer = new MutationObserver(function (mutations) {
    mutations.forEach(function (mutation) {
      if (mutation.type === "childList") {
        mutation.addedNodes.forEach(function (node) {
          if (
            node.nodeType === 1 &&
            node.classList.contains("search-results")
          ) {
            enhanceSearchResults(node);
          }
        });
      }
    });
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true,
  });
}

function initializeScrollEffects() {
  console.log("📜 Initializing scroll effects...");

  // Add scroll progress indicator
  const progressBar = document.createElement("div");
  progressBar.className = "scroll-progress";
  progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background: linear-gradient(90deg, #2563eb, #60a5fa);
        z-index: 9999;
        transition: width 0.1s ease;
        border-radius: 0 3px 3px 0;
    `;
  document.body.appendChild(progressBar);

  // Update progress on scroll
  window.addEventListener("scroll", function () {
    const scrolled = window.scrollY;
    const maxScroll =
      document.documentElement.scrollHeight - window.innerHeight;
    const progress = (scrolled / maxScroll) * 100;
    progressBar.style.width = Math.min(progress, 100) + "%";
  });

  // Add "back to top" button
  const backToTop = document.createElement("button");
  backToTop.innerHTML = "⬆️";
  backToTop.className = "back-to-top";
  backToTop.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 50px;
        height: 50px;
        border: none;
        border-radius: 50%;
        background: var(--color-brand-primary);
        color: white;
        font-size: 1.25rem;
        cursor: pointer;
        z-index: 1000;
        transition: all 0.3s ease;
        opacity: 0;
        transform: translateY(100px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    `;

  backToTop.addEventListener("click", function () {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  });

  // Show/hide back to top button
  window.addEventListener("scroll", function () {
    if (window.scrollY > 500) {
      backToTop.style.opacity = "1";
      backToTop.style.transform = "translateY(0)";
    } else {
      backToTop.style.opacity = "0";
      backToTop.style.transform = "translateY(100px)";
    }
  });

  document.body.appendChild(backToTop);
}

function initializeKeyboardShortcuts() {
  console.log("⌨️ Initializing keyboard shortcuts...");

  // Add keyboard navigation for tabs
  document.querySelectorAll(".sd-tab-label").forEach((tab, index, tabs) => {
    tab.addEventListener("keydown", function (e) {
      let nextIndex;

      switch (e.key) {
        case "ArrowLeft":
          nextIndex = index > 0 ? index - 1 : tabs.length - 1;
          tabs[nextIndex].click();
          tabs[nextIndex].focus();
          break;
        case "ArrowRight":
          nextIndex = index < tabs.length - 1 ? index + 1 : 0;
          tabs[nextIndex].click();
          tabs[nextIndex].focus();
          break;
        case "Home":
          tabs[0].click();
          tabs[0].focus();
          break;
        case "End":
          tabs[tabs.length - 1].click();
          tabs[tabs.length - 1].focus();
          break;
      }
    });
  });
}

// Helper functions
function addExpandCollapseButton(container, content) {
  const button = document.createElement("button");
  button.textContent = "Show More";
  button.className = "expand-collapse-btn";
  button.style.cssText = `
        background: var(--color-brand-primary);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        cursor: pointer;
        margin-top: 1rem;
        transition: all 0.2s ease;
    `;

  let isExpanded = false;
  content.style.maxHeight = "400px";
  content.style.overflow = "hidden";
  content.style.transition = "max-height 0.3s ease";

  button.addEventListener("click", function () {
    if (isExpanded) {
      content.style.maxHeight = "400px";
      button.textContent = "Show More";
      isExpanded = false;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
      button.textContent = "Show Less";
      isExpanded = true;
    }
  });

  container.appendChild(button);
}

function addCopyButton(element) {
  const button = document.createElement("button");
  button.innerHTML = "📋";
  button.className = "copy-signature-btn";
  button.style.cssText = `
        background: var(--color-brand-primary);
        color: white;
        border: none;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        cursor: pointer;
        font-size: 0.875rem;
        margin-left: 0.5rem;
        opacity: 0;
        transition: all 0.2s ease;
    `;

  element.addEventListener("mouseenter", function () {
    button.style.opacity = "1";
  });

  element.addEventListener("mouseleave", function () {
    button.style.opacity = "0";
  });

  button.addEventListener("click", function () {
    const text = element.textContent;
    navigator.clipboard.writeText(text).then(function () {
      button.innerHTML = "✅";
      setTimeout(() => {
        button.innerHTML = "📋";
      }, 1500);
    });
  });

  element.style.position = "relative";
  element.appendChild(button);
}

function createRippleEffect(e) {
  const button = e.currentTarget;
  const circle = document.createElement("span");
  const diameter = Math.max(button.clientWidth, button.clientHeight);
  const radius = diameter / 2;

  const rect = button.getBoundingClientRect();
  circle.style.width = circle.style.height = diameter + "px";
  circle.style.left = e.clientX - rect.left - radius + "px";
  circle.style.top = e.clientY - rect.top - radius + "px";
  circle.classList.add("ripple");

  circle.style.cssText += `
        position: absolute;
        border-radius: 50%;
        transform: scale(0);
        animation: rippleEffect 0.6s linear;
        background-color: rgba(255, 255, 255, 0.6);
        pointer-events: none;
    `;

  const style = document.createElement("style");
  style.textContent = `
        @keyframes rippleEffect {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
  document.head.appendChild(style);

  const ripple = button.getElementsByClassName("ripple")[0];
  if (ripple) {
    ripple.remove();
  }

  button.style.position = "relative";
  button.style.overflow = "hidden";
  button.appendChild(circle);

  setTimeout(() => {
    circle.remove();
  }, 600);
}

function enhanceSearchResults(container) {
  // Add icons and styling to search results
  container.querySelectorAll(".search-result").forEach((result) => {
    const type = result.dataset.type || "page";
    const icon = getTypeIcon(type);

    const iconSpan = document.createElement("span");
    iconSpan.innerHTML = icon;
    iconSpan.style.cssText = "margin-right: 0.5rem; font-size: 1.125rem;";

    result.insertBefore(iconSpan, result.firstChild);

    // Add hover effects
    result.addEventListener("mouseenter", function () {
      this.style.backgroundColor = "rgba(37, 99, 235, 0.1)";
      this.style.transform = "translateX(4px)";
    });

    result.addEventListener("mouseleave", function () {
      this.style.backgroundColor = "";
      this.style.transform = "translateX(0)";
    });
  });
}

function getTypeIcon(type) {
  const icons = {
    class: "🏗️",
    function: "⚡",
    method: "🔧",
    module: "📦",
    page: "📄",
    section: "📝",
  };
  return icons[type] || "📄";
}

// Theme detection and dynamic adjustments
function detectThemeChange() {
  const observer = new MutationObserver(function (mutations) {
    mutations.forEach(function (mutation) {
      if (
        mutation.type === "attributes" &&
        mutation.attributeName === "data-theme"
      ) {
        console.log("🎨 Theme changed, updating enhancements...");
        // Re-initialize enhancements for new theme
        setTimeout(() => {
          initializeAPIEnhancements();
        }, 100);
      }
    });
  });

  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["data-theme"],
  });
}

// Initialize theme detection
detectThemeChange();

// Export for debugging
window.PyAutoDocEnhancements = {
  initializeAPIEnhancements,
  initializeInteractiveElements,
  initializeSearchEnhancements,
  initializeScrollEffects,
  initializeKeyboardShortcuts,
};

console.log("✨ All Furo enhancements loaded successfully!");
