Haive Agents
============

Pre-built agent implementations

Modules
-------

.. grid:: 1 2 2 3
   :gutter: 3

   .. grid-item-card:: **Base**
      :link: base/index
      :link-type: doc
      
      1 submodules
   .. grid-item-card:: **Simple**
      :link: simple/index
      :link-type: doc
      
      2 submodules
   .. grid-item-card:: **Conversation**
      :link: conversation/index
      :link-type: doc
      
      6 submodules
   .. grid-item-card:: **Rag**
      :link: rag/index
      :link-type: doc
      
      6 submodules
   .. grid-item-card:: **React**
      :link: react/index
      :link-type: doc
      
      Core module
   .. grid-item-card:: **Reasoning And Critique**
      :link: reasoning_and_critique/index
      :link-type: doc
      
      6 submodules
   .. grid-item-card:: **Multi**
      :link: multi/index
      :link-type: doc
      
      1 submodules
   .. grid-item-card:: **Planning**
      :link: planning/index
      :link-type: doc
      
      3 submodules
   .. grid-item-card:: **Research**
      :link: research/index
      :link-type: doc
      
      3 submodules

.. toctree::
   :maxdepth: 3
   :caption: Agents Modules
   :hidden:
   
   base/index
   simple/index
   conversation/index
   rag/index
   react/index
   reasoning_and_critique/index
   multi/index
   planning/index
   research/index

Module Path
-----------

.. code-block:: python

   import haive.agents
   # or
   from haive.agents import *

Package Structure
-----------------

This package contains the following module hierarchy:


**base**
  - mixins

**simple**
  - structured
  - v2

**conversation**
  - base
  - collaborative
  - debate
  - directed
  - round_robin
  - social_media

**rag**
  - base
  - adaptive_rag
  - self_rag
  - multi_strategy
  - hyde
  - db_rag

**react**
  - *(no submodules)*

**reasoning_and_critique**
  - lats
  - reflection
  - reflexion
  - tot
  - mcts
  - self_discover

**multi**
  - sequential

**planning**
  - plan_and_execute
  - llm_compiler
  - rewoo

**research**
  - person
  - storm
  - perplexity
