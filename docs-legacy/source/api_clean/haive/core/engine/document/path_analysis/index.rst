
haive.core.engine.document.path_analysis
========================================

.. py:module:: haive.core.engine.document.path_analysis

.. autoapi-nested-parse::

   Path Analysis System for Document Loader Engine.

   This module provides a path analysis system for the document loader engine,
   which analyzes paths and URLs to determine their nature and properties.






Functions
---------

   detect_mime_type   is_binary_file   detect_encoding   extract_url_components   extract_domain_info   analyze_local_path   analyze_url   analyze_database_uri   analyze_cloud_path   analyze_network_path   analyze_special_path   analyze_path_comprehensive
.. autofunction:: detect_mime_type
.. autofunction:: is_binary_file
.. autofunction:: detect_encoding
.. autofunction:: extract_url_components
.. autofunction:: extract_domain_info
.. autofunction:: analyze_local_path
.. autofunction:: analyze_url
.. autofunction:: analyze_database_uri
.. autofunction:: analyze_cloud_path
.. autofunction:: analyze_network_path
.. autofunction:: analyze_special_path
.. autofunction:: analyze_path_comprehensive

Classes
-------

* :py:class:`PathType` - Primary path type classification.* :py:class:`FileCategory` - High-level file category.* :py:class:`DatabaseType` - Database type classification.* :py:class:`CloudProvider` - Cloud storage provider classification.* :py:class:`URLComponents` - Components of a URL.* :py:class:`DomainInfo` - Information about a domain.* :py:class:`PathAnalysisResult` - Result of path analysis.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/document/path_analysis/PathType   /api_clean/haive/core/engine/document/path_analysis/FileCategory   /api_clean/haive/core/engine/document/path_analysis/DatabaseType   /api_clean/haive/core/engine/document/path_analysis/CloudProvider   /api_clean/haive/core/engine/document/path_analysis/URLComponents   /api_clean/haive/core/engine/document/path_analysis/DomainInfo   /api_clean/haive/core/engine/document/path_analysis/PathAnalysisResult

Package Contents
----------------

.. rubric:: haive.core.engine.document.path_analysis.__all__

.. autosummary::
   :nosignatures:

   CloudProvider   DatabaseType   DomainInfo   FileCategory   PathAnalysisResult   PathType   URLComponents   analyze_cloud_path   analyze_database_uri   analyze_local_path   analyze_network_path   analyze_path_comprehensive   analyze_special_path   analyze_url   detect_encoding   detect_mime_type   extract_domain_info   extract_url_components   is_binary_file
.. automodule:: haive.core.engine.document.path_analysis
   :members:
   :show-inheritance:
