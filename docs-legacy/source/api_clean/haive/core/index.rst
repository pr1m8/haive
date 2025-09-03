
:py:mod:`haive.core`
========================

.. py:module:: haive.core

.. autoapi-nested-parse::

   Haive Core - Foundation for the Haive AI Agent Framework.

   This package provides the core building blocks for creating AI agents:

   Engine System
   -------------
   Universal interface for AI components:
   - **InvokableEngine**: For LLMs, retrievers, and tools
   - **AugLLM**: Enhanced LLM with tools and structured output
   - **EngineConfig**: Runtime configuration management

   Graph System
   ------------
   Dynamic workflow builder:
   - **BaseGraph**: Foundation for graph-based workflows

   Schema System
   -------------
   Intelligent state management:
   - **SchemaBuilder**: Auto-generate schemas
   - **StateComposer**: Merge and manage states
   - **Reducers**: Define state update logic

   Persistence
   -----------
   Conversation and state persistence:
   - **PostgreSQL/Supabase**: Auto-persistence support
   - **Checkpointers**: Save/restore agent state
   - **Thread management**: Conversation continuity

   Quick Start
   -----------
   >>> from haive.core.engine import AugLLMConfig
   >>> from haive.core.graph import BaseGraph
   >>>
   >>> # Create an enhanced LLM
   >>> llm = AugLLMConfig(model="gpt-4", temperature=0.7)
   >>>
   >>> # Build a workflow
   >>> graph = BaseGraph()
   >>> # Add nodes to graph as needed

   See Also:
   --------
   - haive.agents: Pre-built agent implementations
   - haive.tools: Tool library
   - haive.core.engine: Engine system documentation
   - haive.core.graph: Graph building guide



.. admonition:: ⚙️ Core Package
   :class: tip

   This package contains the core framework components that power the Haive system.
   
   **Quick Start**:
   
   .. code-block:: python
   
      from haive.core.engine import AugLLMConfig
      from haive.core.schema import StateSchema
      

Subpackages
-----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.common   haive.core.config   haive.core.engine   haive.core.graph   haive.core.models   haive.core.persistence   haive.core.registry   haive.core.runtime   haive.core.schema   haive.core.tools   haive.core.types   haive.core.utils
.. toctree::
   :maxdepth: 2
   :hidden:

   /api_clean/haive/core/common/index   /api_clean/haive/core/config/index   /api_clean/haive/core/engine/index   /api_clean/haive/core/graph/index   /api_clean/haive/core/models/index   /api_clean/haive/core/persistence/index   /api_clean/haive/core/registry/index   /api_clean/haive/core/runtime/index   /api_clean/haive/core/schema/index   /api_clean/haive/core/tools/index   /api_clean/haive/core/types/index   /api_clean/haive/core/utils/index

Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.errors
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/errors/index





Package Contents
----------------

.. rubric:: haive.core.__all__

.. autosummary::
   :nosignatures:

   haive.core.engine   haive.core.graph   haive.core.schema   haive.core.tools   haive.core.types   haive.core.utils   haive.core.models   haive.core.registry   haive.core.runtime   haive.core.persistence   haive.core.config   haive.core.common   haive.core.errors   haive.core.AugLLMConfig   haive.core.AugLLMFactory   haive.core.BaseGraph   haive.core.DynamicRegistry   haive.core.Engine   haive.core.InvokableEngine   haive.core.NonInvokableEngine   haive.core.RegistryItem   haive.core.SchemaComposer   haive.core.__version__

.. automodule:: haive.core
   :members:
   :undoc-members:
   :show-inheritance: