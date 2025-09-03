// API Reference Page Enhancements
document.addEventListener("DOMContentLoaded", function () {
  // Add descriptions to API Reference modules
  const apiDescriptions = {
    base: {
      icon: "🏗️",
      title: "Base Module",
      description:
        "Core foundation classes including models, enums, and configuration management.",
    },
    core: {
      icon: "⚙️",
      title: "Core Module",
      description:
        "Essential data structures, services, utilities, and business logic components.",
    },
  };

  // Enhance API Reference index page
  if (window.location.pathname.includes("autoapi/index")) {
    const moduleLinks = document.querySelectorAll(
      'body[data-pagename="autoapi/index"] .section > ul > li',
    );

    moduleLinks.forEach((li) => {
      const link = li.querySelector("a");
      if (link) {
        const moduleName = link.textContent.trim();
        const desc = apiDescriptions[moduleName];

        if (desc) {
          // Create enhanced content
          const enhancedContent = `
                        <div class="api-module-card">
                            <div class="api-module-icon">${desc.icon}</div>
                            <div class="api-module-content">
                                <h3 class="api-module-title">${desc.title}</h3>
                                <p class="api-module-description">${desc.description}</p>
                                <a href="${link.href}" class="api-module-link">Explore ${desc.title} →</a>
                            </div>
                        </div>
                    `;

          li.innerHTML = enhancedContent;
        }
      }
    });
  }

  // Collapse repetitive View Source Code links
  const viewCodeLinks = document.querySelectorAll(".viewcode-link");
  if (viewCodeLinks.length > 1) {
    // Keep only the first one, hide the rest
    for (let i = 1; i < viewCodeLinks.length; i++) {
      const link = viewCodeLinks[i];
      if (link.textContent.includes("View Source Code")) {
        link.style.display = "none";
      }
    }
  }

  // Add expand/collapse for method lists
  const methodSections = document.querySelectorAll("dl.py");
  methodSections.forEach((section) => {
    if (section.children.length > 10) {
      // Add collapse functionality for long method lists
      const methods = Array.from(section.children).slice(6);
      const toggleBtn = document.createElement("button");
      toggleBtn.className = "method-toggle-btn";
      toggleBtn.innerHTML = `<span>Show ${methods.length} more methods</span> ▼`;
      toggleBtn.onclick = function () {
        const isHidden = methods[0].style.display === "none";
        methods.forEach((method) => {
          method.style.display = isHidden ? "block" : "none";
        });
        toggleBtn.innerHTML = isHidden
          ? `<span>Show fewer methods</span> ▲`
          : `<span>Show ${methods.length} more methods</span> ▼`;
      };

      // Initially hide extra methods
      methods.forEach((method) => (method.style.display = "none"));

      section.appendChild(toggleBtn);
    }
  });
});
