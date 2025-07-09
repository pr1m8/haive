"""Core models for knowledge graph document transformation.

This module provides the fundamental GraphTransformer class for converting
documents into knowledge graphs using LLM-based extraction techniques.
"""

from typing import Any, List, Optional, Union

from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.documents import BaseDocumentTransformer, Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_neo4j.graphs.graph_document import GraphDocument


class GraphTransformer(BaseDocumentTransformer):
    """A document transformer that converts documents into knowledge graphs.

    This transformer uses LLM-based extraction to identify entities, relationships,
    and their properties from unstructured text documents. It builds structured
    knowledge graphs that can be used for various downstream tasks.

    The transformer supports both strict and flexible modes, allowing users to
    define specific entity types and relationship patterns or let the LLM
    discover them automatically.

    Examples:
        Basic entity and relationship extraction::

            from haive.agents.document_modifiers.kg.kg_base.models import GraphTransformer
            from langchain_core.documents import Document

            transformer = GraphTransformer()
            docs = [Document(page_content="John works at Acme Corp in Boston.")]
            graphs = transformer.transform_documents(
                documents=docs,
                allowed_nodes=["Person", "Organization", "Location"],
                allowed_relationships=[
                    ("Person", "WORKS_FOR", "Organization"),
                    ("Organization", "LOCATED_IN", "Location")
                ]
            )

            # Access extracted entities and relationships
            for graph in graphs:
                print(f"Entities: {[node.id for node in graph.nodes]}")
                print(f"Relations: {[rel.type for rel in graph.relationships]}")

        With property extraction::

            graphs = transformer.transform_documents(
                documents=docs,
                allowed_nodes=["Person", "Organization"],
                allowed_relationships=[("Person", "WORKS_FOR", "Organization")],
                node_properties=["role", "founded_year"],
                relationship_properties=["since", "department"],
                additional_instructions="Extract job roles and employment details."
            )

    Attributes:
        None - This class is stateless and can be reused for multiple transformations.
    """

    def transform_documents(
        self,
        documents: List[Document],
        llm_config: LLMConfig = AzureLLMConfig(),
        allowed_nodes: List[str] = None,
        allowed_relationships: Union[List[str], List[tuple[str, str, str]]] = None,
        prompt: Optional[ChatPromptTemplate] = None,
        strict_mode: bool = True,
        node_properties: Union[bool, List[str]] = False,
        relationship_properties: Union[bool, List[str]] = False,
        ignore_tool_usage: bool = True,
        additional_instructions: str = "",
    ) -> List[GraphDocument]:
        """Transform documents into knowledge graphs using LLM-based extraction.

        Processes a list of documents and extracts entities, relationships, and
        their properties to construct structured knowledge graphs. The method
        supports various configuration options to control the extraction process.

        Args:
            documents: List of documents to transform into graphs. Each document
                should contain meaningful text content for entity extraction.
            llm_config: Configuration for the LLM to use for extraction.
                Defaults to AzureLLMConfig() for Azure OpenAI integration.
            allowed_nodes: List of allowed entity types (e.g., ["Person", "Organization"]).
                If None or empty, the LLM will discover entity types automatically.
            allowed_relationships: List of allowed relationship types or tuples.
                Can be either:
                - List of relationship names: ["WORKS_FOR", "LOCATED_IN"]
                - List of (source, relation, target) tuples: [("Person", "WORKS_FOR", "Organization")]
                If None or empty, the LLM will discover relationships automatically.
            prompt: Custom prompt template for extraction. If None, uses the
                default LLMGraphTransformer prompt.
            strict_mode: Whether to enforce strict adherence to allowed_nodes and
                allowed_relationships. If True, only specified types are extracted.
                If False, additional types may be discovered.
            node_properties: Properties to extract for entities. Can be:
                - False: No properties extracted
                - True: Extract all discoverable properties
                - List[str]: Extract specific properties by name
            relationship_properties: Properties to extract for relationships.
                Follows same format as node_properties.
            ignore_tool_usage: Whether to ignore function calling capabilities
                for property extraction. If True, uses text-based extraction only.
            additional_instructions: Additional instructions to guide the LLM
                during extraction (e.g., "Focus on temporal relationships").

        Returns:
            List of GraphDocument objects, one per input document. Each
            GraphDocument contains:
            - nodes: List of extracted entities with their properties
            - relationships: List of extracted relationships with their properties
            - source: Reference to the original document

        Raises:
            TypeError: If allowed_relationships is not a list.
            ValueError: If documents list is empty or contains invalid documents.
            LLMError: If the LLM fails to process the documents.

        Example:
            Extract entities and relationships from multiple documents::

                docs = [
                    Document(page_content="Alice works at TechCorp as a software engineer."),
                    Document(page_content="TechCorp is located in San Francisco."),
                    Document(page_content="Bob also works at TechCorp in the marketing department.")
                ]

                graphs = transformer.transform_documents(
                    documents=docs,
                    allowed_nodes=["Person", "Organization", "Location"],
                    allowed_relationships=[
                        ("Person", "WORKS_FOR", "Organization"),
                        ("Organization", "LOCATED_IN", "Location")
                    ],
                    node_properties=["role", "department"],
                    relationship_properties=["since"]
                )

                # Process results
                for i, graph in enumerate(graphs):
                    print(f"Document {i+1} extracted {len(graph.nodes)} entities")
                    for node in graph.nodes:
                        print(f"  Entity: {node.id} ({node.type})")
                        if node.properties:
                            print(f"    Properties: {node.properties}")

        Note:
            Property extraction requires LLMs with function calling capabilities.
            If the LLM doesn't support function calling, node_properties and
            relationship_properties will be ignored to prevent errors.
        """
        # Validate inputs
        if not documents:
            raise ValueError("Documents list cannot be empty")

        if not isinstance(documents, list):
            raise TypeError("Documents must be a list")

        # Handle default values
        if allowed_nodes is None:
            allowed_nodes = []
        if allowed_relationships is None:
            allowed_relationships = []

        # Validate allowed_relationships type
        if not isinstance(allowed_relationships, list):
            raise TypeError(
                "allowed_relationships must be a list of strings or tuples, "
                f"got {type(allowed_relationships)}"
            )

        # Instantiate the LLM from config
        llm = llm_config.instantiate()

        # Prepare transformer arguments
        graph_transformer_kwargs = {
            "llm": llm,
            "allowed_nodes": allowed_nodes,
            "allowed_relationships": allowed_relationships,
            "prompt": prompt,
            "strict_mode": strict_mode,
            "ignore_tool_usage": ignore_tool_usage,
            "additional_instructions": additional_instructions,
        }

        # Only add property extraction if LLM supports function calling
        # This prevents errors with LLMs that don't support tool usage
        if hasattr(llm, "supports_function_calling") and getattr(
            llm, "supports_function_calling", False
        ):
            graph_transformer_kwargs["node_properties"] = node_properties
            graph_transformer_kwargs["relationship_properties"] = (
                relationship_properties
            )

        # Create the graph transformer and process documents
        graph_transformer = LLMGraphTransformer(**graph_transformer_kwargs)

        return graph_transformer.convert_to_graph_documents(documents)
