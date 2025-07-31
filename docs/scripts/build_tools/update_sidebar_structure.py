#!/usr/bin/env python3
"""Update the main index.rst and sidebar to properly integrate the new haive-based navigation."""

from pathlib import Path

DOCS_SOURCE = Path("/home/will/Projects/haive/backend/haive/docs/source")


def update_main_index():
    """Update the main documentation index.rst to feature the new API structure."""
    main_index_content = """Haive Documentation
===================

Welcome to the Haive framework documentation.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: 🚀 **Getting Started**
      :link: introduction/index
      :link-type: doc

      Installation, quickstart guide, and basic concepts

   .. grid-item-card:: 📚 **API Reference**
      :link: api/haive/index
      :link-type: doc

      Complete API documentation organized by package and module

   .. grid-item-card:: 🤖 **Agent Gallery**
      :link: agents/gallery
      :link-type: doc

      Explore pre-built agents and their capabilities

   .. grid-item-card:: 🛠️ **Tools Library**
      :link: tools/index
      :link-type: doc

      Browse available tools and integrations

   .. grid-item-card:: 🎮 **Games**
      :link: games/index
      :link-type: doc

      Interactive environments and demonstrations

   .. grid-item-card:: 📖 **Reference**
      :link: reference/index
      :link-type: doc

      Technical documentation and architecture

.. toctree::
   :maxdepth: 2
   :caption: Contents
   :hidden:

   introduction/index
   api/haive/index
   agents/gallery
   tools/index
   games/index
   examples/index
   reference/index

Quick Links
-----------

- :doc:`api/haive/core/index` - Core infrastructure
- :doc:`api/haive/agents/index` - Agent implementations
- :doc:`api/haive/tools/index` - Tool integrations
- :ref:`genindex` - Complete index
- :ref:`modindex` - Module index
- :ref:`search` - Search documentation

What's New
----------

.. note::

   **New Navigation Structure!**

   The API documentation now uses a hierarchical structure with Haive as the root.
   Navigate through packages → modules → submodules for better organization.

Latest Updates
^^^^^^^^^^^^^^

- Restructured API documentation for better navigation
- Added contextual navigation that changes based on your location
- Improved module discovery and documentation generation
"""

    (DOCS_SOURCE / "index.rst").write_text(main_index_content)


def create_conf_sidebar_config():
    """Create a configuration snippet for conf.py to set up proper sidebar."""


def create_navigation_css():
    """Create CSS for the new navigation structure."""
    css_content = """/* Haive Navigation Enhancements */

/* Highlight the current package in sidebar */
.sidebar-tree li.current > a {
    font-weight: 600;
    color: var(--color-brand-primary);
}

/* Style package-level navigation */
.sidebar-tree .toctree-l1 > a[href*="/haive/"] {
    font-weight: 500;
    padding-left: 0.5rem;
}

/* Indent module navigation */
.sidebar-tree .toctree-l2 > a[href*="/haive/"] {
    padding-left: 1.5rem;
}

/* Indent submodule navigation */
.sidebar-tree .toctree-l3 > a[href*="/haive/"] {
    padding-left: 2.5rem;
    font-size: 0.9em;
}

/* Style the Haive root link specially */
.sidebar-tree a[href$="/haive/index.html"] {
    font-weight: 700;
    background: var(--color-api-background);
    padding: 0.5rem;
    border-radius: 0.25rem;
    margin-bottom: 0.5rem;
    display: block;
}

/* Improve visibility of current location */
.sidebar-tree .current-page > a {
    background-color: var(--color-api-background-hover);
    border-left: 3px solid var(--color-brand-primary);
    margin-left: -3px;
}

/* Collapse indicator for expandable sections */
.sidebar-tree .has-children > label::before {
    content: "▶";
    display: inline-block;
    margin-right: 0.25rem;
    transition: transform 0.2s;
}

.sidebar-tree .has-children > input:checked ~ label::before {
    transform: rotate(90deg);
}

/* Module path styling in content */
code.docutils.literal {
    background: var(--color-api-background);
    padding: 0.1rem 0.3rem;
    border-radius: 0.2rem;
    font-size: 0.875em;
}

/* Breadcrumb navigation enhancement */
.module-breadcrumb {
    background: var(--color-api-background);
    padding: 0.75rem 1rem;
    border-radius: 0.25rem;
    margin-bottom: 1.5rem;
}

/* Package overview grid enhancement */
.sd-card-title {
    font-size: 1.1em;
    font-weight: 600;
}

.sd-card-text {
    font-size: 0.9em;
    color: var(--color-foreground-secondary);
}

/* Improve module grid layout */
.sd-container-fluid.sd-sphinx-override.sd-mb-4 {
    margin-top: 1.5rem;
}

/* Navigation depth indicators */
@media (min-width: 67em) {
    .sidebar-drawer {
        width: 17rem;
    }
}
"""

    css_path = DOCS_SOURCE / "_static" / "haive-navigation.css"
    css_path.write_text(css_content)


if __name__ == "__main__":
    # Update main index
    update_main_index()

    # Create navigation CSS
    create_navigation_css()

    # Show config snippet
    create_conf_sidebar_config()
