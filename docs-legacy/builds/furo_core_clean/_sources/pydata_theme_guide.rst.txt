PyData Sphinx Theme - Complete Configuration Guide
==================================================

This guide covers all aspects of configuring the PyData Sphinx Theme for beautiful, functional documentation.

Overview
--------

The PyData Sphinx Theme is a Bootstrap-based theme designed for scientific Python documentation. It provides:

- **Responsive design** that works on all devices
- **Flexible navigation** with collapsible sidebars
- **Modern UI** with customizable colors and fonts
- **Accessibility** features built-in
- **Integration** with Jupyter, GitHub, and scientific tools

Installation
------------

.. code-block:: bash

   pip install pydata-sphinx-theme

Or with Poetry:

.. code-block:: bash

   poetry add pydata-sphinx-theme --group docs

Basic Configuration
-------------------

In your ``conf.py``:

.. code-block:: python

   html_theme = "pydata_sphinx_theme"

Navigation Configuration
------------------------

Sidebar Navigation Depth
^^^^^^^^^^^^^^^^^^^^^^^^

Control how many levels of navigation appear in the sidebar:

.. code-block:: python

   html_theme_options = {
       "navigation_depth": 4,      # Maximum depth (default: 4)
       "show_nav_level": 1,        # Levels shown by default (default: 1)
       "collapse_navigation": False,  # Enable collapsible navigation
   }

- ``navigation_depth``: Maximum levels displayed in sidebar (1-4)
- ``show_nav_level``: How many levels are expanded on page load
- ``collapse_navigation``: If True, disables expandable navigation entirely

Table of Contents Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Configure the page-level table of contents:

.. code-block:: python

   html_theme_options = {
       "show_toc_level": 2,  # Depth of in-page TOC
   }

Previous/Next Navigation
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   html_theme_options = {
       "show_prev_next": True,  # Show prev/next buttons
   }

Toctree Best Practices
----------------------

Basic Toctree
^^^^^^^^^^^^^

.. code-block:: rst

   .. toctree::
      :maxdepth: 2
      :caption: User Guide
      :hidden:

      getting_started
      tutorials/index
      how_to_guides/index

- Use ``:maxdepth:`` to control depth (2-3 recommended)
- Use ``:caption:`` to create collapsible sections
- Use ``:hidden:`` to hide from main content (shows in sidebar only)

Organizing with Captions
^^^^^^^^^^^^^^^^^^^^^^^^

Captions create collapsible groups in the navigation:

.. code-block:: rst

   .. toctree::
      :maxdepth: 2
      :caption: Getting Started
      :titlesonly:

      installation
      quickstart
      first_steps

   .. toctree::
      :maxdepth: 3
      :caption: API Reference

      api/modules
      api/classes
      api/functions

Header Navigation
-----------------

Top Navigation Bar
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   html_theme_options = {
       "navbar_align": "left",      # left, right, or content
       "navbar_center": ["navbar-nav"],  # Center navigation items
       "navbar_end": ["theme-switcher", "navbar-icon-links"],
       "header_links_before_dropdown": 5,  # Links before "More" dropdown
   }

Icon Links
^^^^^^^^^^

Add social/repository links:

.. code-block:: python

   html_theme_options = {
       "icon_links": [
           {
               "name": "GitHub",
               "url": "https://github.com/your/repo",
               "icon": "fa-brands fa-github",
               "type": "fontawesome",
           },
           {
               "name": "PyPI", 
               "url": "https://pypi.org/project/your-package",
               "icon": "fa-brands fa-python",
           },
       ],
   }

Sidebar Configuration
---------------------

Sidebar Elements
^^^^^^^^^^^^^^^^

.. code-block:: python

   html_sidebars = {
       "**": ["sidebar-nav-bs", "sidebar-ethical-ads"],
       "index": [],  # No sidebar on index page
   }

Primary Sidebar End
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   html_theme_options = {
       "primary_sidebar_end": ["indices.html", "sidebar-ethical-ads.html"],
   }

Secondary Sidebar
^^^^^^^^^^^^^^^^^

Configure the right sidebar (page TOC):

.. code-block:: python

   html_theme_options = {
       "secondary_sidebar_items": ["page-toc", "edit-this-page", "sourcelink"],
   }

Theming and Styling
-------------------

Logo Configuration
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   html_theme_options = {
       "logo": {
           "text": "My Project",
           "image_light": "_static/logo-light.png",
           "image_dark": "_static/logo-dark.png",
           "alt_text": "My Project Documentation",
       },
   }

Color Customization
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   html_theme_options = {
       "pygment_light_style": "default",
       "pygment_dark_style": "monokai",
   }

Footer Configuration
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   html_theme_options = {
       "footer_start": ["copyright"],
       "footer_center": ["sphinx-version"],
       "footer_end": ["theme-version"],
   }

Advanced Features
-----------------

Search Configuration
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   html_theme_options = {
       "search_bar_text": "Search the docs ...",
       "search_bar_position": "navbar",  # navbar or sidebar
   }

Analytics
^^^^^^^^^

.. code-block:: python

   html_theme_options = {
       "analytics": {
           "google_analytics_id": "UA-XXXXXXX",
       },
   }

Edit Buttons
^^^^^^^^^^^^

.. code-block:: python

   html_theme_options = {
       "use_edit_page_button": True,
       "github_url": "https://github.com/your/repo",
       "path_to_docs": "docs/source",
       "repository_branch": "main",
   }

Version Switcher
^^^^^^^^^^^^^^^^

.. code-block:: python

   html_theme_options = {
       "switcher": {
           "json_url": "https://your-docs.com/versions.json",
           "version_match": version,
       },
       "navbar_end": ["version-switcher", "theme-switcher", "navbar-icon-links"],
   }

Custom CSS
----------

Add custom styles in ``_static/custom.css``:

.. code-block:: css

   /* Custom navigation styles */
   .bd-sidebar-primary .caption {
       font-weight: 700;
       text-transform: uppercase;
       font-size: 0.8rem;
       letter-spacing: 0.05em;
       color: var(--pst-color-text-muted);
       margin-top: 1.5rem;
   }

   /* Custom breadcrumb styles */
   .bd-breadcrumbs {
       background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
       border-radius: 8px;
       padding: 0.75rem 1.25rem;
       margin-bottom: 1.5rem;
   }

Include in ``conf.py``:

.. code-block:: python

   html_static_path = ["_static"]
   html_css_files = ["custom.css"]

Complete Example Configuration
------------------------------

Here's a comprehensive ``conf.py`` configuration:

.. code-block:: python

   # Theme
   html_theme = "pydata_sphinx_theme"

   # Theme options
   html_theme_options = {
       # Logo
       "logo": {
           "text": "Haive AI Framework",
           "alt_text": "Haive Documentation",
       },
       
       # Navigation
       "navigation_with_keys": True,
       "navigation_depth": 4,
       "show_nav_level": 1,
       "collapse_navigation": False,
       "show_toc_level": 3,
       "show_prev_next": True,
       
       # Header
       "navbar_align": "content",
       "header_links_before_dropdown": 5,
       "navbar_center": ["navbar-nav"],
       "navbar_end": ["theme-switcher", "navbar-icon-links"],
       
       # Sidebar
       "primary_sidebar_end": ["indices.html"],
       "secondary_sidebar_items": ["page-toc", "edit-this-page"],
       
       # Footer
       "footer_start": ["copyright"],
       "footer_center": ["sphinx-version"],
       "footer_end": ["theme-version"],
       
       # Icons
       "icon_links": [
           {
               "name": "GitHub",
               "url": "https://github.com/pr1m8/haive",
               "icon": "fa-brands fa-github",
               "type": "fontawesome",
           },
       ],
       
       # Styling
       "pygment_light_style": "default",
       "pygment_dark_style": "monokai",
       
       # Features
       "use_edit_page_button": True,
       "github_url": "https://github.com/pr1m8/haive",
       "path_to_docs": "docs/source",
       "repository_branch": "main",
   }

   # Sidebars
   html_sidebars = {
       "**": ["sidebar-nav-bs"],
   }

Tips and Best Practices
-----------------------

1. **Navigation Depth**: Keep ``navigation_depth`` at 3-4 for best UX
2. **Captions**: Always use captions in toctrees for better organization
3. **Hidden Toctrees**: Use ``:hidden:`` to keep pages out of main content
4. **Custom CSS**: Use CSS variables for consistent theming
5. **Mobile**: Test navigation on mobile devices
6. **Accessibility**: Use semantic HTML and ARIA labels

Common Issues and Solutions
---------------------------

Flat Navigation
^^^^^^^^^^^^^^^

**Problem**: All navigation items appear at same level

**Solution**: 

- Increase ``:maxdepth:`` in toctrees
- Use ``:caption:`` to create groups
- Set ``show_nav_level: 1`` to show only top level initially

Duplicate Entries
^^^^^^^^^^^^^^^^^

**Problem**: Same page appears multiple times

**Solution**: 

- Use ``:hidden:`` on secondary toctrees
- Check for duplicate toctree entries
- Use unique document names

Missing Navigation
^^^^^^^^^^^^^^^^^^

**Problem**: Pages don't appear in sidebar

**Solution**:

- Ensure pages are in a toctree
- Check ``navigation_depth`` setting
- Verify file paths are correct

Resources
---------

- `PyData Theme Documentation <https://pydata-sphinx-theme.readthedocs.io/>`_
- `Theme Gallery <https://sphinx-themes.org/sample-sites/pydata-sphinx-theme/>`_
- `GitHub Repository <https://github.com/pydata/pydata-sphinx-theme>`_
- `Accessibility Guide <https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/accessibility.html>`_