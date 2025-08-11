
haive.core.persistence.serializers
==================================

.. py:module:: haive.core.persistence.serializers

.. autoapi-nested-parse::

   Custom serializers for LangGraph persistence with SecretStr support.

   This module provides secure serialization for SecretStr and other sensitive data
   while maintaining security and avoiding the pickle_fallback security issue.
   Supports both basic secure serialization and production-grade encryption.






Functions
---------

   create_production_serializer   create_encrypted_serializer_for_postgres
.. autofunction:: create_production_serializer
.. autofunction:: create_encrypted_serializer_for_postgres

Classes
-------

* :py:class:`SecureSecretStrSerializer` - Custom serializer that handles SecretStr securely.* :py:class:`SecretStrSerializer` - Alternative serializer that preserves SecretStr values using model_dump.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/persistence/serializers/SecureSecretStrSerializer   /api_clean/haive/core/persistence/serializers/SecretStrSerializer

Package Contents
----------------

