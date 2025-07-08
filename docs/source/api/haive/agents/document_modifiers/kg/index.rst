Knowledge Graph Agents
======================

Agents for extracting and building knowledge graphs from documents.

Agents
------

.. autosummary::
   :toctree: generated
   :maxdepth: 1
   
   haive.agents.document_modifiers.kg.kg_base.ParallelKGTransformer
   haive.agents.document_modifiers.kg.kg_iterative_refinement.IterativeGraphTransformer
   haive.agents.document_modifiers.kg.kg_map_merge.StructuredKGAgent

Parallel KG Transformer
-----------------------

Builds knowledge graphs using parallel processing:

.. code-block:: python

   from haive.agents.document_modifiers.kg import ParallelKGTransformer
   
   kg_builder = ParallelKGTransformer(
       name="parallel_kg",
       engine=llm_engine,
       chunk_size=500,
       num_workers=4
   )
   
   graph = await kg_builder.arun({
       "documents": documents,
       "entity_types": ["Person", "Organization", "Location"],
       "relationship_types": ["WORKS_FOR", "LOCATED_IN", "KNOWS"]
   })

Iterative Graph Transformer
---------------------------

Refines knowledge graphs through iterative passes:

.. code-block:: python

   from haive.agents.document_modifiers.kg import IterativeGraphTransformer
   
   refiner = IterativeGraphTransformer(
       name="iterative_kg",
       engine=llm_engine,
       max_iterations=3
   )
   
   refined_graph = await refiner.arun({
       "initial_graph": graph,
       "refinement_goals": ["merge_duplicates", "infer_relationships"]
   })

Features
--------

- Entity extraction and classification
- Relationship discovery
- Graph merging and deduplication
- Iterative refinement
- Multiple output formats (NetworkX, JSON, RDF)