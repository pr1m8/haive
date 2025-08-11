
haive.core.engine.document.loaders.sources.web_sources
======================================================

.. py:module:: haive.core.engine.document.loaders.sources.web_sources

.. autoapi-nested-parse::

   Web-based source registrations with sitemap detection and crawling.

   This module implements comprehensive web scraping sources from langchain_community
   with intelligent sitemap detection, recursive crawling, and browser automation.






Functions
---------

   find_sitemap   extract_metadata_from_html   get_web_sources_statistics   validate_web_sources
.. autofunction:: find_sitemap
.. autofunction:: extract_metadata_from_html
.. autofunction:: get_web_sources_statistics
.. autofunction:: validate_web_sources

Classes
-------

* :py:class:`CrawlStrategy` - Web crawling strategies.* :py:class:`BrowserEngine` - Browser automation engines.* :py:class:`WebBaseSource` - Base web page source with multiple loading strategies.* :py:class:`AsyncHTMLSource` - Asynchronous HTML source for concurrent processing.* :py:class:`PlaywrightWebSource` - Playwright browser automation source.* :py:class:`SeleniumWebSource` - Selenium browser automation source.* :py:class:`ChromiumAsyncSource` - Async Chromium browser source.* :py:class:`RecursiveWebSource` - Recursive web crawling source with advanced filtering.* :py:class:`SitemapCrawlerSource` - Sitemap-based crawling source with auto-detection.* :py:class:`ReadTheDocsSource` - Read the Docs documentation source.* :py:class:`DocusaurusSource` - Docusaurus documentation site source.* :py:class:`FireCrawlSource` - FireCrawl web scraping service source.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/document/loaders/sources/web_sources/CrawlStrategy   /api_clean/haive/core/engine/document/loaders/sources/web_sources/BrowserEngine   /api_clean/haive/core/engine/document/loaders/sources/web_sources/WebBaseSource   /api_clean/haive/core/engine/document/loaders/sources/web_sources/AsyncHTMLSource   /api_clean/haive/core/engine/document/loaders/sources/web_sources/PlaywrightWebSource   /api_clean/haive/core/engine/document/loaders/sources/web_sources/SeleniumWebSource   /api_clean/haive/core/engine/document/loaders/sources/web_sources/ChromiumAsyncSource   /api_clean/haive/core/engine/document/loaders/sources/web_sources/RecursiveWebSource   /api_clean/haive/core/engine/document/loaders/sources/web_sources/SitemapCrawlerSource   /api_clean/haive/core/engine/document/loaders/sources/web_sources/ReadTheDocsSource   /api_clean/haive/core/engine/document/loaders/sources/web_sources/DocusaurusSource   /api_clean/haive/core/engine/document/loaders/sources/web_sources/FireCrawlSource

Package Contents
----------------

