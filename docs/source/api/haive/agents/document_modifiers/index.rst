Document Modifiers
==================

Document processing and transformation agents for text analysis, summarization, and knowledge extraction.

Modules
-------

.. grid:: 1 2 2 3
   :gutter: 3

   .. grid-item-card:: **Summarizer**
      :link: summarizer/index
      :link-type: doc
      
      Text summarization agents
      
   .. grid-item-card:: **Knowledge Graph**
      :link: kg/index
      :link-type: doc
      
      Knowledge graph extraction
      
   .. grid-item-card:: **Complex Extraction**
      :link: complex_extraction/index
      :link-type: doc
      
      Advanced information extraction
      
   .. grid-item-card:: **TNT (Taxonomy)**
      :link: tnt/index
      :link-type: doc
      
      Taxonomy and tagging

.. toctree::
   :maxdepth: 2
   :caption: Document Modifier Modules
   :hidden:
   
   summarizer/index
   kg/index
   complex_extraction/index
   tnt/index

Overview
--------

The document modifiers package provides specialized agents for processing and transforming documents:

- **Summarization**: Map-branch and iterative refinement approaches
- **Knowledge Graphs**: Parallel and iterative graph construction
- **Complex Extraction**: Advanced information extraction patterns
- **Taxonomy (TNT)**: Document classification and tagging

Usage Example
-------------

.. code-block:: python

   from haive.agents.document_modifiers.summarizer import SummarizerAgent
   from haive.agents.document_modifiers.kg import ParallelKGTransformer
   
   # Create a summarizer
   summarizer = SummarizerAgent(
       name="doc_summarizer",
       engine=llm_engine
   )
   
   # Process documents
   result = await summarizer.arun({
       "documents": documents,
       "summary_type": "comprehensive"
   })

Module Path
-----------

.. code-block:: python

   import haive.agents.document_modifiers
   # or specific agents
   from haive.agents.document_modifiers.summarizer import SummarizerAgent