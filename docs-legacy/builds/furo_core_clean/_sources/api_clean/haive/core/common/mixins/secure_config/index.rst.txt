
haive.core.common.mixins.secure_config
======================================

.. py:module:: haive.core.common.mixins.secure_config

.. autoapi-nested-parse::

   Secure configuration mixin for API credentials.

   This module provides a mixin for secure handling of API credentials
   with environment variable fallbacks and validation logic. It enables
   automatic resolution of API keys from environment variables based on
   the provider type, with proper secure storage using Pydantic's SecretStr.

   Usage:
       ```python
       from pydantic import BaseModel, Field
       from typing import Optional
       from haive.core.common.mixins import SecureConfigMixin

       class APIConfig(SecureConfigMixin, BaseModel):
           provider: str = Field(default="openai")
           api_key: Optional[SecretStr] = Field(default=None)

           def make_api_call(self):
               # Securely retrieve the API key
               key = self.get_api_key()
               if not key:
                   raise ValueError("No API key available")
               # Use key for API call
               # ...

       # Will try to use OPENAI_API_KEY from environment
       config = APIConfig(provider="openai")

       # Will use the explicitly provided key
       config = APIConfig(provider="anthropic", api_key="sk-ant-...")
       ```







Classes
-------

* :py:class:`SecureConfigMixin` - A mixin to provide secure and flexible configuration for API keys.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/common/mixins/secure_config/SecureConfigMixin

Package Contents
----------------

