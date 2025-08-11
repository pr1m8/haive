
:py:mod:`haive.core.types.general`
========================

.. py:module:: haive.core.types.general

.. autoapi-nested-parse::

   General type definitions for common domains.

   This module provides pre-defined type definitions for common domains like
   file types and programming languages. These types are used throughout the
   Haive framework for validation, categorization, and processing logic.

   The general types module includes comprehensive lists of file extensions,
   programming languages, and other domain-specific categories that are
   frequently needed in document processing, code analysis, and AI workflows.

   Key Components:
       FileTypes: Comprehensive file type definitions and extensions
       ProgrammingLanguages: Programming language definitions and metadata

   .. admonition:: Examples

      File type validation::
      
          from haive.core.types.general import FileTypes
      
          # Check if file is a supported document type
          if file_ext in FileTypes.DOCUMENTS:
              process_document(file_path)
          elif file_ext in FileTypes.CODE:
              analyze_code(file_path)
      
      Programming language detection::
      
          from haive.core.types.general import ProgrammingLanguages
      
          # Get language info by extension
          lang_info = ProgrammingLanguages.get_by_extension(".py")
          print(f"Language: {lang_info.name}")
          print(f"Type: {lang_info.type}")

   .. seealso::

      - Document processing utilities
      - Code analysis tools
      - File type detection systems





Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.types.general.file_types   haive.core.types.general.programming_languages
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/types/general/file_types/index   /api_clean/haive/core/types/general/programming_languages/index





Package Contents
----------------

.. rubric:: haive.core.types.general.__all__

.. autosummary::
   :nosignatures:

   haive.core.types.general.FileTypes   haive.core.types.general.ProgrammingLanguages

.. automodule:: haive.core.types.general
   :members:
   :undoc-members:
   :show-inheritance: