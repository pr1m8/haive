"""Base models and utilities for knowledge graph construction.

This module provides the foundational components for building knowledge graphs
from documents. It includes the GraphTransformer class that uses LLMs to extract
entities and relationships according to defined schemas.

The module serves as the foundation for all knowledge graph agents, providing:
    - Document to graph transformation capabilities
    - Entity and relationship extraction with LLMs
    - Schema validation and enforcement
    - Property extraction for rich graph data
    - Integration with graph databases

Key Components:
    - :class:`~haive.agents.document_modifiers.kg.kg_base.models.GraphTransformer`: Main transformer class
    - GraphDocument: Standard representation of extracted graphs
    - Node/Relationship models: Core graph elements with properties

Example:
    Basic graph extraction::

        from haive.agents.document_modifiers.kg.kg_base.models import GraphTransformer
        from langchain_core.documents import Document

        # Initialize transformer
        transformer = GraphTransformer()

        # Define schema
        allowed_nodes = ["Person", "Organization", "Location"]
        allowed_relationships = [
            ("Person", "WORKS_FOR", "Organization"),
            ("Organization", "LOCATED_IN", "Location")
        ]

        # Transform documents
        docs = [Document(page_content="John works at Acme Corp in Boston.")]
        graphs = transformer.transform_documents(
            documents=docs,
            allowed_nodes=allowed_nodes,
            allowed_relationships=allowed_relationships
        )

        # Access results
        for graph in graphs:
            print(f"Found {len(graph.nodes)} entities")
            print(f"Found {len(graph.relationships)} relationships")

    With property extraction::

        # Extract additional properties
        graphs = transformer.transform_documents(
            documents=docs,
            allowed_nodes=allowed_nodes,
            allowed_relationships=allowed_relationships,
            node_properties=["role", "founded_year"],
            relationship_properties=["since", "department"],
            additional_instructions="Extract job roles and employment dates."
        )

See Also:
    - :mod:`haive.agents.document_modifiers.kg.kg_iterative_refinement`: Iterative graph building
    - :mod:`haive.agents.document_modifiers.kg.kg_map_merge`: Parallel graph extraction
    - :mod:`langchain_experimental.graph_transformers`: Underlying LangChain utilities

Note:
    This module requires an LLM with function calling capabilities for
    optimal property extraction. The transformer will adapt based on the
    LLM's capabilities.
"""

from haive.agents.document_modifiers.kg.kg_base.models import GraphTransformer

__all__ = ["GraphTransformer"]

# Example usage available in the example module
# Run: python -m haive.agents.document_modifiers.kg.kg_base.example
