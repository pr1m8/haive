
:py:mod:`haive.core.engine.document.transformers`
========================

.. py:module:: haive.core.engine.document.transformers

.. autoapi-nested-parse::

   Document transformers module for the Haive framework.

   This module provides utilities for transforming and processing documents after
   loading. It includes text normalization, format conversion, metadata enrichment,
   and content enhancement capabilities.

   Document transformers are applied after loading and before/after chunking to
   normalize content, clean formatting, enrich metadata, convert formats, and
   enhance document quality.

   Key Components:
       DocumentTransformerEngine: Main engine for document transformation
       DocTransformerType: Enumeration of available transformer types
       Various transformers for different document processing needs

   Transformer Types:
       - HTML_TO_TEXT: Convert HTML documents to plain text
       - BEAUTIFUL_SOUP: HTML parsing with BeautifulSoup
       - EMBED_QUERY: Add query embeddings to documents
       - TRANSLATE: Language translation
       - DOCTRAN_EXTRACT_PROPERTIES: Extract structured properties
       - DOCTRAN_INTERROGATE: Generate questions about documents
       - DOCTRAN_REFINE: Refine and improve document content
       - DOCTRAN_SUMMARIZE: Generate document summaries
       - OPENAI_FUNCTIONS: Extract structured data using OpenAI functions
       - CROSS_ENCODER_RERANK: Rerank documents using cross-encoder

   .. admonition:: Examples

      HTML to text conversion::
      
          from haive.core.engine.document.transformers import (
              DocumentTransformerEngine,
              DocTransformerType
          )
      
          # Create HTML to text transformer
          transformer = DocumentTransformerEngine(
              transformer_type=DocTransformerType.HTML_TO_TEXT,
              ignore_links=True,
              ignore_images=True
          )
      
          # Transform HTML documents
          text_docs = transformer.invoke(html_documents)
      
      BeautifulSoup HTML parsing::
      
          # Parse HTML with specific tags
          parser = DocumentTransformerEngine(
              transformer_type=DocTransformerType.BEAUTIFUL_SOUP,
              tags_to_extract=["p", "h1", "h2", "li"],
              unwanted_tags=["script", "style", "nav"]
          )
      
          clean_docs = parser.invoke(html_documents)
      
      Document enrichment::
      
          # Extract properties from documents
          extractor = DocumentTransformerEngine(
              transformer_type=DocTransformerType.DOCTRAN_EXTRACT_PROPERTIES,
              properties=[
                  {"name": "category", "description": "Document category"},
                  {"name": "sentiment", "description": "Overall sentiment"}
              ]
          )
      
          enriched_docs = extractor.invoke(documents)

   .. seealso::

      - Document loader module for loading documents
      - Document splitter module for chunking documents
      - LangChain document transformers documentation





Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.engine.document.transformers.base   haive.core.engine.document.transformers.engine   haive.core.engine.document.transformers.types
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/engine/document/transformers/base/index   /api_clean/haive/core/engine/document/transformers/engine/index   /api_clean/haive/core/engine/document/transformers/types/index





Package Contents
----------------

.. rubric:: haive.core.engine.document.transformers.__all__

.. autosummary::
   :nosignatures:

   haive.core.engine.document.transformers.DocTransformerConfig   haive.core.engine.document.transformers.DocTransformerType   haive.core.engine.document.transformers.DocumentTransformerEngine   haive.core.engine.document.transformers.Html2TextTransformer

.. automodule:: haive.core.engine.document.transformers
   :members:
   :undoc-members:
   :show-inheritance: