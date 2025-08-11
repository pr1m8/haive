
:py:mod:`haive.core.utils.tools`
========================

.. py:module:: haive.core.utils.tools

Package ``haive.core.utils.tools``

.. admonition:: 🔧 Tools Package
   :class: tip

   This package contains tools and integrations that agents can use.
   
   **Quick Start**:
   
   .. code-block:: python
   
      from haive.core.utils.tools import WebSearchTool
      from haive.agents import ReactAgent
      
      tool = WebSearchTool()
      agent = ReactAgent(name="researcher", tools=[tool])
      


Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.utils.tools.tool_schema_generator
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/utils/tools/tool_schema_generator/index





Package Contents
----------------


.. automodule:: haive.core.utils.tools
   :members:
   :undoc-members:
   :show-inheritance: