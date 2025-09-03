
haive.core.graph.state_graph.components.node
============================================

.. py:module:: haive.core.graph.state_graph.components.node

.. autoapi-nested-parse::

   Node component implementation for the Haive graph system.

   This module defines the Node class which represents a processing unit in a graph.
   Nodes are responsible for transforming state and producing outputs that can be used
   by subsequent nodes in the graph flow.

   Classes:
       Node: Base node class for state processing in a graph

   Typical usage:
       ```python
       from haive.core.graph.state_graph.components import Node
       from haive.core.graph.common.types import NodeType

       # Create a simple processing node
       node = Node(
           name="transform_data",
           node_type=NodeType.CALLABLE,
           metadata={"callable": lambda state: {"output": state["input"] * 2}}
       )

       # Process state through the node
       result = node.process({"input": 5})
       assert result["output"] == 10
       ```







Classes
-------

* :py:class:`Node` - Base node in a graph system.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/graph/state_graph/components/node/Node

Package Contents
----------------

