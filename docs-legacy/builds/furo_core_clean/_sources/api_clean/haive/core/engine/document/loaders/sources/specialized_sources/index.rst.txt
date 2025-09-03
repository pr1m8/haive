
haive.core.engine.document.loaders.sources.specialized_sources
==============================================================

.. py:module:: haive.core.engine.document.loaders.sources.specialized_sources

.. autoapi-nested-parse::

   Specialized platform source registrations.

   from typing import Any
   This module implements specialized loaders from langchain_community including:
   - Academic and research platforms (arXiv, PubMed, bioRxiv)
   - Media platforms (YouTube, audio/video processing)
   - Development platforms (GitHub, GitLab, Git repositories)
   - Domain-specific systems (Wikipedia, weather data, financial data)






Functions
---------

   get_specialized_sources_statistics   validate_specialized_sources   detect_specialized_platform
.. autofunction:: get_specialized_sources_statistics
.. autofunction:: validate_specialized_sources
.. autofunction:: detect_specialized_platform

Classes
-------

* :py:class:`SpecializedPlatform` - Specialized platform types.* :py:class:`ResearchField` - Academic research fields.* :py:class:`MediaType` - Media content types.* :py:class:`DevelopmentDataType` - Development platform data types.* :py:class:`ArxivSource` - arXiv research paper source.* :py:class:`PubMedSource` - PubMed biomedical literature source.* :py:class:`SemanticScholarSource` - Semantic Scholar academic source.* :py:class:`YouTubeSource` - YouTube video source.* :py:class:`BilibiliSource` - Bilibili video platform source.* :py:class:`AudioFileSource` - Audio file transcription source.* :py:class:`GitHubSource` - GitHub repository source.* :py:class:`GitSource` - Local Git repository source.* :py:class:`WikipediaSource` - Wikipedia knowledge source.* :py:class:`MediaWikiSource` - MediaWiki dump source.* :py:class:`WeatherSource` - Weather data source.* :py:class:`FinancialNewsSource` - Financial news and data source.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/document/loaders/sources/specialized_sources/SpecializedPlatform   /api_clean/haive/core/engine/document/loaders/sources/specialized_sources/ResearchField   /api_clean/haive/core/engine/document/loaders/sources/specialized_sources/MediaType   /api_clean/haive/core/engine/document/loaders/sources/specialized_sources/DevelopmentDataType   /api_clean/haive/core/engine/document/loaders/sources/specialized_sources/ArxivSource   /api_clean/haive/core/engine/document/loaders/sources/specialized_sources/PubMedSource   /api_clean/haive/core/engine/document/loaders/sources/specialized_sources/SemanticScholarSource   /api_clean/haive/core/engine/document/loaders/sources/specialized_sources/YouTubeSource   /api_clean/haive/core/engine/document/loaders/sources/specialized_sources/BilibiliSource   /api_clean/haive/core/engine/document/loaders/sources/specialized_sources/AudioFileSource   /api_clean/haive/core/engine/document/loaders/sources/specialized_sources/GitHubSource   /api_clean/haive/core/engine/document/loaders/sources/specialized_sources/GitSource   /api_clean/haive/core/engine/document/loaders/sources/specialized_sources/WikipediaSource   /api_clean/haive/core/engine/document/loaders/sources/specialized_sources/MediaWikiSource   /api_clean/haive/core/engine/document/loaders/sources/specialized_sources/WeatherSource   /api_clean/haive/core/engine/document/loaders/sources/specialized_sources/FinancialNewsSource

Package Contents
----------------

