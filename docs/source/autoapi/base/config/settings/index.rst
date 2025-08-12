
:py:mod:`base.config.settings`
==============================

.. py:module:: base.config.settings

Application settings and configuration.

This module provides settings management using Pydantic v2,
supporting environment variables and configuration files.


.. autolink-examples:: base.config.settings
   :collapse:

Classes
-------

.. autoapisummary::

   base.config.settings.AppSettings
   base.config.settings.CacheBackend
   base.config.settings.CacheSettings
   base.config.settings.DatabaseSettings
   base.config.settings.DatabaseType
   base.config.settings.Environment
   base.config.settings.LoggingSettings
   base.config.settings.LogLevel
   base.config.settings.Settings


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

.. autopydantic_model:: base.config.settings.AppSettings
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

.. autoclass:: base.config.settings.CacheBackend
   :members:
   :undoc-members:
   :show-inheritance:

   .. note::

      **CacheBackend** is an Enum defined in ``base.config.settings``.





.. toggle:: Show Inheritance Diagram

   Inheritance diagram for CacheSettings:

   .. graphviz::
      :align: center

      digraph inheritance_CacheSettings {
        node [shape=record];
        "CacheSettings" [label="CacheSettings"];
        "pydantic_settings.BaseSettings" -> "CacheSettings";
      }

.. autopydantic_model:: base.config.settings.CacheSettings
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

.. autopydantic_model:: base.config.settings.DatabaseSettings
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

.. autoclass:: base.config.settings.DatabaseType
   :members:
   :undoc-members:
   :show-inheritance:

   .. note::

      **DatabaseType** is an Enum defined in ``base.config.settings``.


:orphan:



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

.. autoclass:: base.config.settings.Environment
   :members:
   :undoc-members:
   :show-inheritance:

   .. note::

      **Environment** is an Enum defined in ``base.config.settings``.





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

.. autoclass:: base.config.settings.LogLevel
   :members:
   :undoc-members:
   :show-inheritance:

   .. note::

      **LogLevel** is an Enum defined in ``base.config.settings``.





.. toggle:: Show Inheritance Diagram

   Inheritance diagram for LoggingSettings:

   .. graphviz::
      :align: center

      digraph inheritance_LoggingSettings {
        node [shape=record];
        "LoggingSettings" [label="LoggingSettings"];
        "pydantic_settings.BaseSettings" -> "LoggingSettings";
      }

.. autopydantic_model:: base.config.settings.LoggingSettings
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

.. autopydantic_model:: base.config.settings.Settings
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





.. rubric:: Related Links

.. autolink-examples:: base.config.settings
   :collapse:
   
.. autolink-skip:: next
