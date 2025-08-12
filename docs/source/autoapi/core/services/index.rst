
:py:mod:`core.services`
=======================

.. py:module:: core.services

Core service classes and utilities.

This module provides service layer implementations including
abstract base classes, concrete services, and utility functions.


.. autolink-examples:: core.services
   :collapse:

Classes
-------

.. autoapisummary::

   core.services.CacheProtocol
   core.services.InMemoryTaskRepository
   core.services.MetricsCollector
   core.services.Priority
   core.services.Repository
   core.services.Result
   core.services.Status
   core.services.Task
   core.services.TaskService


Module Contents
---------------




.. toggle:: Show Inheritance Diagram

   Inheritance diagram for CacheProtocol:

   .. graphviz::
      :align: center

      digraph inheritance_CacheProtocol {
        node [shape=record];
        "CacheProtocol" [label="CacheProtocol"];
        "Protocol" -> "CacheProtocol";
      }

.. autoclass:: core.services.CacheProtocol
   :members:
   :undoc-members:
   :show-inheritance:




.. toggle:: Show Inheritance Diagram

   Inheritance diagram for InMemoryTaskRepository:

   .. graphviz::
      :align: center

      digraph inheritance_InMemoryTaskRepository {
        node [shape=record];
        "InMemoryTaskRepository" [label="InMemoryTaskRepository"];
        "Repository[core.data_structures.Task]" -> "InMemoryTaskRepository";
      }

.. autoclass:: core.services.InMemoryTaskRepository
   :members:
   :undoc-members:
   :show-inheritance:




.. toggle:: Show Inheritance Diagram

   Inheritance diagram for MetricsCollector:

   .. graphviz::
      :align: center

      digraph inheritance_MetricsCollector {
        node [shape=record];
        "MetricsCollector" [label="MetricsCollector"];
      }

.. autoclass:: core.services.MetricsCollector
   :members:
   :undoc-members:
   :show-inheritance:

:orphan:



.. toggle:: Show Inheritance Diagram

   Inheritance diagram for Priority:

   .. graphviz::
      :align: center

      digraph inheritance_Priority {
        node [shape=record];
        "Priority" [label="Priority"];
        "enum.Enum" -> "Priority";
      }

.. autoclass:: core.services.Priority
   :members:
   :undoc-members:
   :show-inheritance:

   .. note::

      **Priority** is an Enum defined in ``core.services``.





.. toggle:: Show Inheritance Diagram

   Inheritance diagram for Repository:

   .. graphviz::
      :align: center

      digraph inheritance_Repository {
        node [shape=record];
        "Repository" [label="Repository"];
        "abc.ABC" -> "Repository";
        "Generic[T]" -> "Repository";
      }

.. autoclass:: core.services.Repository
   :members:
   :undoc-members:
   :show-inheritance:

:orphan:



.. toggle:: Show Inheritance Diagram

   Inheritance diagram for Result:

   .. graphviz::
      :align: center

      digraph inheritance_Result {
        node [shape=record];
        "Result" [label="Result"];
        "Generic[T]" -> "Result";
      }

.. autoclass:: core.services.Result
   :members:
   :undoc-members:
   :show-inheritance:

:orphan:



.. toggle:: Show Inheritance Diagram

   Inheritance diagram for Status:

   .. graphviz::
      :align: center

      digraph inheritance_Status {
        node [shape=record];
        "Status" [label="Status"];
        "enum.Enum" -> "Status";
      }

.. autoclass:: core.services.Status
   :members:
   :undoc-members:
   :show-inheritance:

   .. note::

      **Status** is an Enum defined in ``core.services``.


:orphan:



.. toggle:: Show Inheritance Diagram

   Inheritance diagram for Task:

   .. graphviz::
      :align: center

      digraph inheritance_Task {
        node [shape=record];
        "Task" [label="Task"];
      }

.. autoclass:: core.services.Task
   :members:
   :undoc-members:
   :show-inheritance:




.. toggle:: Show Inheritance Diagram

   Inheritance diagram for TaskService:

   .. graphviz::
      :align: center

      digraph inheritance_TaskService {
        node [shape=record];
        "TaskService" [label="TaskService"];
      }

.. autoclass:: core.services.TaskService
   :members:
   :undoc-members:
   :show-inheritance:


Functions
---------

.. autoapisummary::

   core.services.retry

.. py:function:: retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0)

   Decorator for retrying failed operations.

   :param max_attempts: Maximum number of retry attempts
   :param delay: Initial delay between retries in seconds
   :param backoff: Backoff multiplier for each retry

   .. rubric:: Example

   >>> @retry(max_attempts=3, delay=0.5)
   ... async def flaky_operation():
   ...     # Operation that might fail
   ...     pass


   .. autolink-examples:: retry
      :collapse:



.. rubric:: Related Links

.. autolink-examples:: core.services
   :collapse:
   
.. autolink-skip:: next
