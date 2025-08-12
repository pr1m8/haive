Intersphinx Demo
================

This page demonstrates the automatic intersphinx mapping functionality provided by
``seed-intersphinx-mapping``.

Testing Cross-References
------------------------

Let's test some cross-references to see which packages have been automatically mapped:

Python Standard Library
~~~~~~~~~~~~~~~~~~~~~~~

- :py:func:`print` - Python builtin function
- :py:mod:`os` - OS interface module
- :py:class:`dict` - Dictionary type
- :py:exc:`ValueError` - Common exception

Pydantic (Manually Configured)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- :py:class:`pydantic.BaseModel` - Base model class
- :py:mod:`pydantic` - Main pydantic module
- :py:func:`pydantic.Field` - Field function

Sphinx (Manually Configured)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- :py:class:`sphinx.application.Sphinx` - Main Sphinx application class
- :py:mod:`sphinx.ext.autodoc` - Autodoc extension
- :py:mod:`sphinx.ext.intersphinx` - Intersphinx extension

Potential Auto-Mapped Packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's test if seed-intersphinx-mapping has automatically added these:

**MyST Parser:**

- :py:mod:`myst_parser` - MyST parser module
- :py:class:`myst_parser.main.MystParser` - Main parser class

**NumPy (if available):**

- :py:mod:`numpy` - NumPy module
- :py:func:`numpy.array` - Array creation function

**Requests (if available):**

- :py:mod:`requests` - Requests module
- :py:func:`requests.get` - GET request function

How seed-intersphinx-mapping Works
-----------------------------------

The ``seed-intersphinx-mapping`` extension:

1. Reads your project dependencies from ``pyproject.toml``
2. Queries PyPI for package metadata
3. Extracts documentation URLs from package metadata
4. Automatically adds them to ``intersphinx_mapping``

Configuration
~~~~~~~~~~~~~

In ``conf.py``:

.. code-block:: python

   # Enable the extension
   extensions = [
       "sphinx.ext.intersphinx",
       "seed_intersphinx_mapping",
   ]
   
   # Configure to read from pyproject.toml
   pkg_requirements_source = "pyproject"
   repository_root = "../.."
   
   # Manual mappings (these are always included)
   intersphinx_mapping = {
       "python": ("https://docs.python.org/3", None),
       "pydantic": ("https://docs.pydantic.dev/latest", None),
       "sphinx": ("https://www.sphinx-doc.org/en/master", None),
   }

Benefits
--------

- **Automatic Updates**: No need to manually maintain documentation URLs
- **Dependency Sync**: Documentation links stay in sync with your dependencies
- **Reduced Errors**: Less chance of broken cross-references
- **Time Saving**: Especially beneficial for projects with many dependencies

Troubleshooting
---------------

If cross-references aren't working:

1. **Check Package Metadata**: Not all packages include documentation URLs in their PyPI metadata
2. **Clear Cache**: Run ``python -m seed_intersphinx_mapping`` to clear the cache
3. **Manual Override**: Add manual entries to ``intersphinx_mapping`` for packages without metadata
4. **Build Verbosely**: Use ``sphinx-build -vvv`` to see what mappings are loaded

Current Status
--------------

Based on our configuration, seed-intersphinx-mapping should be reading dependencies from:

- Main dependencies in ``[tool.poetry.dependencies]``
- Documentation dependencies in ``[tool.poetry.group.docs.dependencies]``

The extension caches package information to avoid repeated PyPI queries.