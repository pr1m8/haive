
:py:mod:`core.data_structures`
==============================

.. py:module:: core.data_structures

Core data structures using dataclasses.

This module provides fundamental data structures used throughout
the application, implemented using Python's dataclasses for clean,
type-safe code.


.. autolink-examples:: core.data_structures
   :collapse:

Classes
-------

.. autoapisummary::

   core.data_structures.Point
   core.data_structures.Priority
   core.data_structures.Result
   core.data_structures.Status
   core.data_structures.Task


Module Contents
---------------




.. toggle:: Show Inheritance Diagram

   Inheritance diagram for Point:

   .. graphviz::
      :align: center

      digraph inheritance_Point {
        node [shape=record];
        "Point" [label="Point"];
      }

.. autoclass:: core.data_structures.Point
   :members:
   :undoc-members:
   :show-inheritance:

   .. note::

      **Point** is a dataclass. Enhanced schema documentation will be available soon.





.. toggle:: Show Inheritance Diagram

   Inheritance diagram for Priority:

   .. graphviz::
      :align: center

      digraph inheritance_Priority {
        node [shape=record];
        "Priority" [label="Priority"];
        "enum.Enum" -> "Priority";
      }

.. autoclass:: core.data_structures.Priority
   :members:
   :undoc-members:
   :show-inheritance:

   .. note::

      **Priority** is an Enum defined in ``core.data_structures``.





.. toggle:: Show Inheritance Diagram

   Inheritance diagram for Result:

   .. graphviz::
      :align: center

      digraph inheritance_Result {
        node [shape=record];
        "Result" [label="Result"];
        "Generic[T]" -> "Result";
      }

.. autoclass:: core.data_structures.Result
   :members:
   :undoc-members:
   :show-inheritance:




.. toggle:: Show Inheritance Diagram

   Inheritance diagram for Status:

   .. graphviz::
      :align: center

      digraph inheritance_Status {
        node [shape=record];
        "Status" [label="Status"];
        "enum.Enum" -> "Status";
      }

.. autoclass:: core.data_structures.Status
   :members:
   :undoc-members:
   :show-inheritance:

   .. note::

      **Status** is an Enum defined in ``core.data_structures``.





.. toggle:: Show Inheritance Diagram

   Inheritance diagram for Task:

   .. graphviz::
      :align: center

      digraph inheritance_Task {
        node [shape=record];
        "Task" [label="Task"];
      }

.. autoclass:: core.data_structures.Task
   :members:
   :undoc-members:
   :show-inheritance:




.. rubric:: Related Links

.. autolink-examples:: core.data_structures
   :collapse:
   
.. autolink-skip:: next
