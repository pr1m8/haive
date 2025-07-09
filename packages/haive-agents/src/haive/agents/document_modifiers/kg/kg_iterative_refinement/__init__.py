"""Iterative knowledge graph construction with progressive refinement.

This module provides an agent that builds knowledge graphs incrementally by
processing documents one at a time. Each document refines and expands the
existing graph, making it ideal for processing document sequences where
later documents provide additional context or updates about previously
discovered entities.

The iterative approach offers several advantages:
    - Memory efficiency by processing one document at a time
    - Context preservation across document sequences
    - Intelligent conflict resolution for contradictory information
    - Progressive enhancement of entity details
    - Support for temporal evolution of relationships

Key Features:
    - Incremental graph construction from document streams
    - Entity coreference resolution across documents
    - Conflict detection and resolution strategies
    - Graph versioning and provenance tracking
    - Streaming support for continuous processing

Classes:
    - :class:`~haive.agents.document_modifiers.kg.kg_iterative_refinement.agent.IterativeGraphTransformer`: Main agent
    - :class:`~haive.agents.document_modifiers.kg.kg_iterative_refinement.config.IterativeGraphTransformerConfig`: Configuration
    - :class:`~haive.agents.document_modifiers.kg.kg_iterative_refinement.state.IterativeGraphTransformerState`: State management

Example:
    Basic iterative graph building::

        from haive.agents.document_modifiers.kg.kg_iterative_refinement import IterativeGraphTransformer
        from haive.agents.document_modifiers.kg.kg_iterative_refinement.config import IterativeGraphTransformerConfig

        # Configure agent
        config = IterativeGraphTransformerConfig(
            allowed_nodes=["Person", "Organization", "Event"],
            allowed_relationships=[
                ("Person", "WORKS_FOR", "Organization"),
                ("Person", "PARTICIPATED_IN", "Event")
            ]
        )

        agent = IterativeGraphTransformer(config)

        # Process documents sequentially
        documents = [
            "Marie Curie was a physicist.",
            "Curie won the Nobel Prize in 1903.",
            "She won another Nobel Prize in 1911."
        ]

        result = agent.run({"contents": documents})
        graph = result["graph_doc"]

        # Graph progressively built with each document
        # Marie Curie entity enhanced with Nobel Prize relationships

    Handling document streams::

        # Configure for streaming
        config = IterativeGraphTransformerConfig(
            streaming_mode=True,
            conflict_resolution="latest"
        )

        agent = IterativeGraphTransformer(config)

        # Process documents as they arrive
        async for doc in document_stream:
            result = await agent.arun({
                "contents": [doc],
                "existing_graph": current_graph
            })
            current_graph = result["graph_doc"]

See Also:
    - :mod:`haive.agents.document_modifiers.kg.kg_base`: Base graph components
    - :mod:`haive.agents.document_modifiers.kg.kg_map_merge`: Parallel graph construction
    - :mod:`langchain_neo4j`: Graph database integration

Note:
    This module is optimized for scenarios where document order matters
    and relationships evolve over time. For parallel processing of
    independent documents, consider using kg_map_merge instead.
"""
