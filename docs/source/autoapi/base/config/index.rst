
:py:mod:`base.config`
=====================

.. py:module:: base.config

Configuration management package.

This package provides comprehensive configuration management for the application,
including system configuration, settings management, and environment handling.

Modules:
    system: System-level configuration and environment detection
    settings: Application settings using Pydantic BaseSettings

.. rubric:: Example

>>> from base.config import settings, Environment
>>>
>>> # Access application settings
>>> print(settings.app.app_name)
PyAutoDoc
>>>
>>> # Check environment
>>> if settings.app.environment == Environment.PROD:
...     print("Running in production")


.. autolink-examples:: base.config
   :collapse:

Classes
-------

.. autoapisummary::

   base.config.AppSettings
   base.config.CacheBackend
   base.config.CacheSettings
   base.config.DatabaseSettings
   base.config.DatabaseType
   base.config.Environment
   base.config.LoggingSettings
   base.config.LogLevel
   base.config.Settings
   base.config.SystemConfig


Module Contents
---------------




.. toggle:: Show Inheritance Diagram

   Inheritance diagram for AppSettings:

   .. graphviz::
      :align: center

      digraph inheritance_AppSettings {
        node [shape=record];
        "AppSettings" [label="AppSettings"];
        "pydantic_settings.BaseSettings" -> "AppSettings";
      }

.. autopydantic_model:: base.config.AppSettings
   :members:
   :undoc-members:
   :show-inheritance:
   :model-show-field-summary:
   :model-show-config-summary:
   :model-show-validator-members:
   :model-show-validator-summary:
   :model-show-json:
   :field-list-validators:
   :field-show-constraints:





.. toggle:: Show Inheritance Diagram

   Inheritance diagram for CacheBackend:

   .. graphviz::
      :align: center

      digraph inheritance_CacheBackend {
        node [shape=record];
        "CacheBackend" [label="CacheBackend"];
        "str" -> "CacheBackend";
        "enum.Enum" -> "CacheBackend";
      }

.. autoclass:: base.config.CacheBackend
   :members:
   :undoc-members:
   :show-inheritance:

   .. note::

      **CacheBackend** is an Enum defined in ``base.config``.





.. toggle:: Show Inheritance Diagram

   Inheritance diagram for CacheSettings:

   .. graphviz::
      :align: center

      digraph inheritance_CacheSettings {
        node [shape=record];
        "CacheSettings" [label="CacheSettings"];
        "pydantic_settings.BaseSettings" -> "CacheSettings";
      }

.. autopydantic_model:: base.config.CacheSettings
   :members:
   :undoc-members:
   :show-inheritance:
   :model-show-field-summary:
   :model-show-config-summary:
   :model-show-validator-members:
   :model-show-validator-summary:
   :model-show-json:
   :field-list-validators:
   :field-show-constraints:





.. toggle:: Show Inheritance Diagram

   Inheritance diagram for DatabaseSettings:

   .. graphviz::
      :align: center

      digraph inheritance_DatabaseSettings {
        node [shape=record];
        "DatabaseSettings" [label="DatabaseSettings"];
        "pydantic_settings.BaseSettings" -> "DatabaseSettings";
      }

.. autopydantic_model:: base.config.DatabaseSettings
   :members:
   :undoc-members:
   :show-inheritance:
   :model-show-field-summary:
   :model-show-config-summary:
   :model-show-validator-members:
   :model-show-validator-summary:
   :model-show-json:
   :field-list-validators:
   :field-show-constraints:





.. toggle:: Show Inheritance Diagram

   Inheritance diagram for DatabaseType:

   .. graphviz::
      :align: center

      digraph inheritance_DatabaseType {
        node [shape=record];
        "DatabaseType" [label="DatabaseType"];
        "str" -> "DatabaseType";
        "enum.Enum" -> "DatabaseType";
      }

.. autoclass:: base.config.DatabaseType
   :members:
   :undoc-members:
   :show-inheritance:

   .. note::

      **DatabaseType** is an Enum defined in ``base.config``.





.. toggle:: Show Inheritance Diagram

   Inheritance diagram for Environment:

   .. graphviz::
      :align: center

      digraph inheritance_Environment {
        node [shape=record];
        "Environment" [label="Environment"];
        "str" -> "Environment";
        "enum.Enum" -> "Environment";
      }

.. autoclass:: base.config.Environment
   :members:
   :undoc-members:
   :show-inheritance:

   .. note::

      **Environment** is an Enum defined in ``base.config``.





.. toggle:: Show Inheritance Diagram

   Inheritance diagram for LogLevel:

   .. graphviz::
      :align: center

      digraph inheritance_LogLevel {
        node [shape=record];
        "LogLevel" [label="LogLevel"];
        "str" -> "LogLevel";
        "enum.Enum" -> "LogLevel";
      }

.. autoclass:: base.config.LogLevel
   :members:
   :undoc-members:
   :show-inheritance:

   .. note::

      **LogLevel** is an Enum defined in ``base.config``.





.. toggle:: Show Inheritance Diagram

   Inheritance diagram for LoggingSettings:

   .. graphviz::
      :align: center

      digraph inheritance_LoggingSettings {
        node [shape=record];
        "LoggingSettings" [label="LoggingSettings"];
        "pydantic_settings.BaseSettings" -> "LoggingSettings";
      }

.. autopydantic_model:: base.config.LoggingSettings
   :members:
   :undoc-members:
   :show-inheritance:
   :model-show-field-summary:
   :model-show-config-summary:
   :model-show-validator-members:
   :model-show-validator-summary:
   :model-show-json:
   :field-list-validators:
   :field-show-constraints:





.. toggle:: Show Inheritance Diagram

   Inheritance diagram for Settings:

   .. graphviz::
      :align: center

      digraph inheritance_Settings {
        node [shape=record];
        "Settings" [label="Settings"];
        "pydantic.BaseModel" -> "Settings";
      }

.. autopydantic_model:: base.config.Settings
   :members:
   :undoc-members:
   :show-inheritance:
   :model-show-field-summary:
   :model-show-config-summary:
   :model-show-validator-members:
   :model-show-validator-summary:
   :model-show-json:
   :field-list-validators:
   :field-show-constraints:





.. toggle:: Show Inheritance Diagram

   Inheritance diagram for SystemConfig:

   .. graphviz::
      :align: center

      digraph inheritance_SystemConfig {
        node [shape=record];
        "SystemConfig" [label="SystemConfig"];
        "pydantic.BaseModel" -> "SystemConfig";
      }

.. autopydantic_model:: base.config.SystemConfig
   :members:
   :undoc-members:
   :show-inheritance:
   :model-show-field-summary:
   :model-show-config-summary:
   :model-show-validator-members:
   :model-show-validator-summary:
   :model-show-json:
   :field-list-validators:
   :field-show-constraints:



Functions
---------

.. autoapisummary::

   base.config.get_system_config

.. py:function:: get_system_config() -> SystemConfig

   Get system configuration.


   .. autolink-examples:: get_system_config
      :collapse:



.. rubric:: Related Links

.. autolink-examples:: base.config
   :collapse:
   
.. autolink-skip:: next
