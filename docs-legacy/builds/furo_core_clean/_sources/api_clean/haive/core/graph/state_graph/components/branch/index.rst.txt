
haive.core.graph.state_graph.components.branch
==============================================

.. py:module:: haive.core.graph.state_graph.components.branch

.. autoapi-nested-parse::

   Branch component implementation for the Haive graph system.

   This module defines the Branch class which represents a decision point in a graph
   that routes execution based on state conditions. Branches enable the creation of
   dynamic, conditional flows within the graph system.

   Classes:
       Branch: Conditional routing component for decision branching in a graph

   Typical usage:
       ```python
       from haive.core.graph.state_graph.components import Branch
       from haive.core.graph.branches.types import BranchMode

       # Create a branch for routing based on state values
       branch = Branch(
           name="route_by_score",
           source_node="evaluate",
           mode=BranchMode.DIRECT,
           key="score",
           comparison="greater_than",
           value=80,
           destinations={"True": "high_score_path", "False": "low_score_path"}
       )

       # Evaluate state to determine the next node
       next_node = branch({"score": 95})  # Returns "high_score_path"
       ```







Classes
-------

* :py:class:`Branch` - Unified branch for dynamic routing based on state values.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/graph/state_graph/components/branch/Branch

Package Contents
----------------

