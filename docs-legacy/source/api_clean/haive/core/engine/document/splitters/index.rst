
:py:mod:`haive.core.engine.document.splitters`
========================

.. py:module:: haive.core.engine.document.splitters

.. autoapi-nested-parse::

   Document splitters module for the Haive framework.

   This module provides various text splitting strategies for chunking documents
   into smaller, manageable segments suitable for processing by LLMs, vector
   databases, and other components that have size constraints.

   The splitters subsystem supports multiple splitting algorithms optimized for
   different document types and use cases, from simple character-based splitting
   to sophisticated semantic and structural splitting.

   Key Components:
       DocumentSplitterEngine: Main engine for splitting documents
       DocSplitterType: Enumeration of available splitter types
       Various text splitters from LangChain

   Splitter Types:
       - RecursiveCharacterTextSplitter: Most versatile, tries multiple separators
       - CharacterTextSplitter: Simple character-based splitting
       - TokenTextSplitter: Split based on token count
       - SentenceTransformersTokenTextSplitter: Token splitting with sentence transformers
       - MarkdownTextSplitter: Preserves Markdown structure
       - HTMLHeaderTextSplitter: Splits HTML by headers
       - LatexTextSplitter: Preserves LaTeX structure
       - PythonCodeTextSplitter: Code-aware splitting for Python
       - RecursiveJsonSplitter: JSON structure-aware splitting
       - SpacyTextSplitter: Uses spaCy for linguistic splitting
       - NLTKTextSplitter: Uses NLTK for sentence splitting

   .. admonition:: Examples

      Basic document splitting::
      
          from haive.core.engine.document.splitters import (
              DocumentSplitterEngine,
              DocSplitterType
          )
      
          # Create splitter engine
          splitter = DocumentSplitterEngine(
              splitter_type=DocSplitterType.RECURSIVE_CHARACTER,
              chunk_size=1000,
              chunk_overlap=200
          )
      
          # Split documents
          chunks = splitter.invoke({"documents": documents})
      
      Code-aware splitting::
      
          from haive.core.engine.document.splitters import (
              DocumentSplitterEngine,
              DocSplitterType
          )
      
          # Python code splitter
          code_splitter = DocumentSplitterEngine(
              splitter_type=DocSplitterType.PYTHON_CODE,
              chunk_size=2000,
              chunk_overlap=100
          )
      
          code_chunks = code_splitter.invoke({"documents": python_docs})
      
      Markdown-aware splitting::
      
          # Markdown splitter preserves structure
          md_splitter = DocumentSplitterEngine(
              splitter_type=DocSplitterType.MARKDOWN,
              chunk_size=1500,
              strip_whitespace=True
          )
      
          md_chunks = md_splitter.invoke({"documents": markdown_docs})

   .. seealso::

      - Document loader module for loading documents
      - Document transformer module for document transformation
      - LangChain text splitters documentation





Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.engine.document.splitters.base   haive.core.engine.document.splitters.config   haive.core.engine.document.splitters.engine
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/engine/document/splitters/base/index   /api_clean/haive/core/engine/document/splitters/config/index   /api_clean/haive/core/engine/document/splitters/engine/index





Package Contents
----------------

.. rubric:: haive.core.engine.document.splitters.__all__

.. autosummary::
   :nosignatures:

   haive.core.engine.document.splitters.CharacterTextSplitter   haive.core.engine.document.splitters.DocSplitterInputSchema   haive.core.engine.document.splitters.DocSplitterOutputSchema   haive.core.engine.document.splitters.DocSplitterType   haive.core.engine.document.splitters.DocumentSplitterEngine   haive.core.engine.document.splitters.ElementType   haive.core.engine.document.splitters.HTMLHeaderTextSplitter   haive.core.engine.document.splitters.HeaderType   haive.core.engine.document.splitters.KonlpyTextSplitter   haive.core.engine.document.splitters.Language   haive.core.engine.document.splitters.LatexTextSplitter   haive.core.engine.document.splitters.LineType   haive.core.engine.document.splitters.MarkdownHeaderTextSplitter   haive.core.engine.document.splitters.MarkdownTextSplitter   haive.core.engine.document.splitters.NLTKTextSplitter   haive.core.engine.document.splitters.PythonCodeTextSplitter   haive.core.engine.document.splitters.RecursiveCharacterTextSplitter   haive.core.engine.document.splitters.RecursiveJsonSplitter   haive.core.engine.document.splitters.SentenceTransformersTokenTextSplitter   haive.core.engine.document.splitters.SpacyTextSplitter   haive.core.engine.document.splitters.SplitterConfig   haive.core.engine.document.splitters.TextSplitter   haive.core.engine.document.splitters.TokenTextSplitter   haive.core.engine.document.splitters.Tokenizer   haive.core.engine.document.splitters.split_text_on_tokens

.. automodule:: haive.core.engine.document.splitters
   :members:
   :undoc-members:
   :show-inheritance: