
:py:mod:`base.config.system`
============================

.. py:module:: base.config.system


Classes
-------

.. autoapisummary::

   base.config.system.Environment
   base.config.system.SystemConfig


Module Contents
---------------

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

.. autoclass:: base.config.system.Environment
   :members:
   :undoc-members:
   :show-inheritance:

   .. note::

      **Environment** is an Enum defined in ``base.config.system``.





.. toggle:: Show Inheritance Diagram

   Inheritance diagram for SystemConfig:

   .. graphviz::
      :align: center

      digraph inheritance_SystemConfig {
        node [shape=record];
        "SystemConfig" [label="SystemConfig"];
        "pydantic.BaseModel" -> "SystemConfig";
      }

.. autopydantic_model:: base.config.system.SystemConfig
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

   base.config.system.get_system_config

.. py:function:: get_system_config() -> SystemConfig

   Get system configuration.


   .. autolink-examples:: get_system_config
      :collapse:



.. rubric:: Related Links

.. autolink-examples:: base.config.system
   :collapse:
   
.. autolink-skip:: next
