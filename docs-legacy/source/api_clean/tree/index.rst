
tree
====

.. py:module:: tree

.. autoapi-nested-parse::

   Automatic tree structure generator for Pydantic BaseModels with Union type support.

   This module provides the AutoTree class that automatically wraps any BaseModel
   in a tree structure, handling complex type relationships including Union types.
   It enables hierarchical visualization and analysis of nested BaseModel structures.

   The AutoTree automatically detects fields containing BaseModels (including those
   in Union types) and creates child tree nodes, making it perfect for visualizing
   complex data structures like plans with mixed content types.

   Usage:
       ```python
       from pydantic import BaseModel, Field
       from typing import List, Union
       from haive.core.common.structures.tree import AutoTree

       class Step(BaseModel):
           name: str
           duration_hours: float = 1.0

       class Plan(BaseModel):
           name: str
           # Can contain either Steps OR other Plans
           items: List[Union[Step, 'Plan']] = Field(default_factory=list)

       # Create nested structure
       main_plan = Plan(name="Project Alpha")
       main_plan.items.append(Step(name="Setup", duration_hours=2))

       sub_plan = Plan(name="Development Phase")
       sub_plan.items.append(Step(name="Code", duration_hours=40))
       main_plan.items.append(sub_plan)

       # Visualize as tree
       tree = AutoTree(main_plan)
       print(tree.visualize())
       ```







Classes
-------

* :py:class:`AutoTree` - Automatically wraps any BaseModel in a tree structure with Union type support.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/tree/AutoTree

Package Contents
----------------

