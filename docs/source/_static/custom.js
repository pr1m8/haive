// docs/source/_static/custom.js

// Wait for DOM to be ready
document.addEventListener("DOMContentLoaded", function () {
  // ========================================================================
  // Smooth Scrolling for Anchor Links
  // ========================================================================

  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      const href = this.getAttribute("href");
      if (href !== "#" && href !== "#0") {
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
          target.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
        }
      }
    });
  });

  // ========================================================================
  // Copy Code Button Enhancement
  // ========================================================================

  // Add copy feedback
  document.querySelectorAll(".copybtn").forEach((button) => {
    button.addEventListener("click", function () {
      const originalText = this.textContent;
      this.textContent = "✓ Copied!";
      this.style.backgroundColor = "#00c853";

      setTimeout(() => {
        this.textContent = originalText;
        this.style.backgroundColor = "";
      }, 2000);
    });
  });

  // ========================================================================
  // Example Output Collapsible
  // ========================================================================

  // Make example outputs collapsible
  document.querySelectorAll(".example-output").forEach((output) => {
    if (output.scrollHeight > 400) {
      const toggleBtn = document.createElement("button");
      toggleBtn.className = "toggle-output-btn";
      toggleBtn.textContent = "Show More";
      toggleBtn.style.cssText = `
                display: block;
                margin: 10px auto 0;
                padding: 5px 15px;
                background: var(--color-brand-primary);
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            `;

      output.style.maxHeight = "400px";
      output.parentNode.insertBefore(toggleBtn, output.nextSibling);

      toggleBtn.addEventListener("click", function () {
        if (output.style.maxHeight === "400px") {
          output.style.maxHeight = "none";
          this.textContent = "Show Less";
        } else {
          output.style.maxHeight = "400px";
          output.scrollTop = 0;
          this.textContent = "Show More";
        }
      });
    }
  });

  // ========================================================================
  // Image Lightbox for Screenshots
  // ========================================================================

  function createLightbox() {
    const lightbox = document.createElement("div");
    lightbox.id = "lightbox";
    lightbox.style.cssText = `
            display: none;
            position: fixed;
            z-index: 9999;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.9);
            cursor: pointer;
        `;

    const img = document.createElement("img");
    img.style.cssText = `
            display: block;
            max-width: 90%;
            max-height: 90%;
            margin: auto;
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
        `;

    lightbox.appendChild(img);
    document.body.appendChild(lightbox);

    lightbox.addEventListener("click", () => {
      lightbox.style.display = "none";
    });

    return { lightbox, img };
  }

  const { lightbox, img: lightboxImg } = createLightbox();

  // Add click handler to images
  document
    .querySelectorAll('.game-screenshot, img[alt*="UI"], img[alt*="Graph"]')
    .forEach((img) => {
      img.style.cursor = "pointer";
      img.addEventListener("click", function () {
        lightboxImg.src = this.src;
        lightbox.style.display = "block";
      });
    });

  // ========================================================================
  // Search Enhancement
  // ========================================================================

  // Add search shortcuts
  document.addEventListener("keydown", function (e) {
    // Ctrl/Cmd + K to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === "k") {
      e.preventDefault();
      const searchInput = document.querySelector(
        '.sidebar-search-container input[type="search"]',
      );
      if (searchInput) {
        searchInput.focus();
      }
    }
  });

  // ========================================================================
  // Sidebar Navigation Enhancement
  // ========================================================================

  // Expand parent sections of the current page
  const currentLinks = document.querySelectorAll(
    ".sidebar-tree .reference.current",
  );
  currentLinks.forEach((currentLink) => {
    let parent = currentLink.parentNode;
    while (parent && parent.classList) {
      if (
        parent.classList.contains("toctree-l1") ||
        parent.classList.contains("toctree-l2") ||
        parent.classList.contains("toctree-l3")
      ) {
        // Find and check the corresponding checkbox for this parent
        const checkbox = parent.querySelector("input.toctree-checkbox");
        if (checkbox) {
          checkbox.checked = true;
        }
      }
      parent = parent.parentNode;
    }
  });

  // ========================================================================
  // API Reference Navigation
  // ========================================================================

  // Add expand/collapse all for API reference
  const apiSections = document.querySelectorAll(
    ".py.class, .py.function, .py.method",
  );
  if (apiSections.length > 10) {
    const controlsDiv = document.createElement("div");
    controlsDiv.style.cssText = `
            margin: 1rem 0;
            text-align: right;
        `;

    const expandBtn = document.createElement("button");
    expandBtn.textContent = "Expand All";
    expandBtn.style.cssText = `
            margin-right: 10px;
            padding: 5px 15px;
            background: var(--color-brand-primary);
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        `;

    const collapseBtn = document.createElement("button");
    collapseBtn.textContent = "Collapse All";
    collapseBtn.style.cssText = expandBtn.style.cssText;

    controlsDiv.appendChild(expandBtn);
    controlsDiv.appendChild(collapseBtn);

    // Insert controls before first API section
    const firstSection = document.querySelector(".section#module-");
    if (firstSection) {
      firstSection.insertBefore(controlsDiv, firstSection.firstChild);
    }
  }

  // ========================================================================
  // Progress Indicator
  // ========================================================================

  const progressBar = document.createElement("div");
  progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--color-brand-primary), var(--color-brand-content));
        transition: width 0.3s ease;
        z-index: 9999;
    `;
  document.body.appendChild(progressBar);

  function updateProgressBar() {
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight - windowHeight;
    const scrolled = window.scrollY;
    const progress = (scrolled / documentHeight) * 100;
    progressBar.style.width = progress + "%";
  }

  window.addEventListener("scroll", updateProgressBar);
  updateProgressBar();

  // ========================================================================
  // Tooltip for Abbreviations
  // ========================================================================

  const abbreviations = {
    LLM: "Large Language Model",
    RAG: "Retrieval-Augmented Generation",
    API: "Application Programming Interface",
    UI: "User Interface",
    AI: "Artificial Intelligence",
  };

  // Auto-add tooltips to abbreviations
  Object.keys(abbreviations).forEach((abbr) => {
    document
      .querySelectorAll(`body :not(script):not(style)`)
      .forEach((element) => {
        if (
          element.childNodes.length === 1 &&
          element.childNodes[0].nodeType === 3
        ) {
          const text = element.textContent;
          const regex = new RegExp(`\\b${abbr}\\b`, "g");
          if (regex.test(text)) {
            element.innerHTML = text.replace(
              regex,
              `<abbr title="${abbreviations[abbr]}">${abbr}</abbr>`,
            );
          }
        }
      });
  });
});

// ============================================================================
// Console Easter Egg
// ============================================================================

console.log(
  "%c🤖 Welcome to Haive Documentation! 🤖",
  "font-size: 20px; font-weight: bold; color: #2962ff;",
);
console.log(
  "%cBuild amazing AI agents with Haive!",
  "font-size: 14px; color: #4fc3f7;",
);
console.log(
  "%cVisit our GitHub: https://github.com/will-astley/haive",
  "font-size: 12px; color: #666;",
);
