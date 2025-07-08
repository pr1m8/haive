haive.core.engine.document
==========================

Document loading and processing engine.

.. currentmodule:: haive.core.engine.document

Overview
--------

The document engine provides intelligent document loading capabilities using a source-based architecture. Sources define **what** and **where** to load, while loaders define **how** to process the content.

.. automodule:: haive.core.engine.document
   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:
   :private-members:
   :special-members: __init__, __call__

Classes
-------

.. autosummary::
   :nosignatures:
   :toctree: _autosummary

Functions
---------

.. autosummary::
   :nosignatures:
   :toctree: _autosummary

Sources
-------

.. toctree::
   :maxdepth: 1
   :caption: Available Sources
   :hidden:
   
   sources/index
   sources/local
   sources/web
   sources/cloud
   sources/database
   sources/social

Loaders
-------

.. toctree::
   :maxdepth: 1
   :caption: Document Loaders
   :hidden:
   
   loaders/index
   loaders/auto_loader
   loaders/registry

Examples
--------

**Auto-Loading (Recommended):**

.. code-block:: python

   from haive.core.engine.document.loaders import AutoLoader
   
   # Auto-detect and load from any source
   loader = AutoLoader()
   
   # Local files
   documents = loader.load("./documents/report.pdf")
   
   # Web content
   documents = loader.load("https://docs.python.org")
   
   # Cloud storage
   documents = loader.load("s3://mybucket/documents/")
   
   # Directory/bulk loading
   documents = loader.load_all("./entire_directory")

**Manual Source Configuration:**

.. code-block:: python

   from haive.core.engine.document.loaders.sources import WebSource, FileSource
   from haive.core.engine.document.loaders import SourceLoader
   
   # Web source
   web_source = WebSource(
       url="https://example.com/docs",
       recursive=True,
       max_depth=3
   )
   
   # File source  
   file_source = FileSource(
       path="./documents",
       file_types=[".pdf", ".docx", ".md"],
       recursive=True
   )
   
   # Load with specific configurations
   loader = SourceLoader()
   web_docs = loader.load(web_source)
   file_docs = loader.load(file_source)

**Source Types:**

.. code-block:: python

   from haive.core.engine.document.loaders.sources.types import SourceType
   
   # Available source types
   print(f"Web sources: {[s for s in SourceType if s.value.startswith('web')]}")
   print(f"File sources: {[s for s in SourceType if 'file' in s.value]}")
   print(f"Database sources: {[s for s in SourceType if 'db' in s.value]}")

See Also
--------

- :doc:`/api/haive/core/index` - Package overview
- :doc:`/api/haive/core/engine/index` - Module overview
- :doc:`sources/index` - All document sources
- :doc:`loaders/index` - Document loaders
