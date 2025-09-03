
:py:mod:`haive.core.tools`
========================

.. py:module:: haive.core.tools

.. autoapi-nested-parse::

   Haive Core Tools Package.

   This package provides tools that agents can use, including store management
   tools for memory operations similar to LangMem.



.. admonition:: 🔧 Tools Package
   :class: tip

   This package contains tools and integrations that agents can use.
   
   **Quick Start**:
   
   .. code-block:: python
   
      from haive.core.tools import WebSearchTool
      from haive.agents import ReactAgent
      
      tool = WebSearchTool()
      agent = ReactAgent(name="researcher", tools=[tool])
      


Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.tools.interrupt_tool_wrapper   haive.core.tools.store_manager   haive.core.tools.store_tools
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/tools/interrupt_tool_wrapper/index   /api_clean/haive/core/tools/store_manager/index   /api_clean/haive/core/tools/store_tools/index





Package Contents
----------------


.. automodule:: haive.core.tools
   :members:
   :undoc-members:
   :show-inheritance: