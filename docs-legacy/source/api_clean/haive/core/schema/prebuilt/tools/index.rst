
:py:mod:`haive.core.schema.prebuilt.tools`
========================

.. py:module:: haive.core.schema.prebuilt.tools

.. autoapi-nested-parse::

   Tool management utilities for prebuilt schemas.



.. admonition:: 🔧 Tools Package
   :class: tip

   This package contains tools and integrations that agents can use.
   
   **Quick Start**:
   
   .. code-block:: python
   
      from haive.core.schema.prebuilt.tools import WebSearchTool
      from haive.agents import ReactAgent
      
      tool = WebSearchTool()
      agent = ReactAgent(name="researcher", tools=[tool])
      


Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.schema.prebuilt.tools.validation_state
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/schema/prebuilt/tools/validation_state/index





Package Contents
----------------

.. rubric:: haive.core.schema.prebuilt.tools.__all__

.. autosummary::
   :nosignatures:

   haive.core.schema.prebuilt.tools.RouteRecommendation   haive.core.schema.prebuilt.tools.ToolValidationResult   haive.core.schema.prebuilt.tools.ValidationRoutingState   haive.core.schema.prebuilt.tools.ValidationStateManager   haive.core.schema.prebuilt.tools.ValidationStatus

.. automodule:: haive.core.schema.prebuilt.tools
   :members:
   :undoc-members:
   :show-inheritance: