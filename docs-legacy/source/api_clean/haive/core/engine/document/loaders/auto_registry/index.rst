
haive.core.engine.document.loaders.auto_registry
================================================

.. py:module:: haive.core.engine.document.loaders.auto_registry

.. autoapi-nested-parse::

   Auto-Registry System for Document Loaders.

   from typing import Any
   This module provides automatic registration and discovery of all document loader
   sources and loaders. It scans the sources directory and automatically imports
   and registers all available source types without manual intervention.

   The auto-registry ensures that all 230+ implemented loaders are automatically
   available when the system starts, providing a seamless developer experience.

   .. admonition:: Examples

      Auto-register all sources::
      
          from haive.core.engine.document.loaders import auto_register_all
      
          # Automatically discover and register all sources
          auto_register_all()
      
      Check registration status::
      
          from haive.core.engine.document.loaders import get_registration_status
      
          status = get_registration_status()
          print(f"Registered {status['total_sources']} sources")

   Author: Claude (Haive Document Loader System)
   Version: 1.0.0






Functions
---------

   auto_register_all   get_registration_status   list_available_sources   get_sources_by_category
.. autofunction:: auto_register_all
.. autofunction:: get_registration_status
.. autofunction:: list_available_sources
.. autofunction:: get_sources_by_category

Classes
-------

* :py:class:`RegistrationInfo` - Information about a registered source.* :py:class:`RegistrationStats` - Statistics about the registration process.* :py:class:`AutoRegistry` - Automatic registry for document loader sources.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/document/loaders/auto_registry/RegistrationInfo   /api_clean/haive/core/engine/document/loaders/auto_registry/RegistrationStats   /api_clean/haive/core/engine/document/loaders/auto_registry/AutoRegistry

Package Contents
----------------

.. rubric:: haive.core.engine.document.loaders.auto_registry.__all__

.. autosummary::
   :nosignatures:

   AutoRegistry   RegistrationInfo   RegistrationStats   auto_register_all   auto_registry   get_registration_status   get_sources_by_category   list_available_sources
.. automodule:: haive.core.engine.document.loaders.auto_registry
   :members:
   :show-inheritance:
