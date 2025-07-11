#!/usr/bin/env python3
"""Example usage of the GraphTransformer class.

This script demonstrates how to use the GraphTransformer to extract
knowledge graphs from documents with various configurations.
"""

from typing import List

from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.documents import Document

from haive.agents.document_modifiers.kg.kg_base.models import GraphTransformer


def basic_example() -> None:
    """Demonstrate basic graph transformation."""

    # Create transformer instance
    GraphTransformer()

    # Sample documents
    documents = [
        Document(page_content="John Smith works at Acme Corporation in New York."),
        Document(
            page_content="Acme Corporation is a technology company founded in 2010."
        ),
        Document(page_content="Sarah Johnson is the CEO of Acme Corporation."),
    ]

    # Define allowed entities and relationships
    allowed_nodes = ["Person", "Organization", "Location"]
    allowed_relationships = [
        ("Person", "WORKS_FOR", "Organization"),
        ("Person", "LEADS", "Organization"),
        ("Organization", "LOCATED_IN", "Location"),
    ]


    try:
        # Transform documents (this would normally use an actual LLM)
        # For demonstration, we'll just show the structure
        for i, doc in enumerate(documents):
            pass

        # In a real scenario:


    except Exception as e:


def advanced_example() -> None:
    """Demonstrate advanced configuration with properties."""

    GraphTransformer()

    # Sample document with rich information
    documents = [
        Document(
            page_content=(
                "Dr. Emily Chen, a 35-year-old software engineer, has been working "
                "at TechCorp since 2018. She leads the AI research team and has "
                "published 15 papers on machine learning."
            )
        )
    ]

    # Extended schema with properties

    # Properties to extract
    node_properties = ["age", "title", "experience_years", "expertise"]
    relationship_properties = ["since", "duration", "role"]


    # Additional instructions for better extraction
    additional_instructions = (
        "Extract specific details about experience, education, and achievements. "
        "Include temporal information where available."
    )



def schema_validation_example() -> None:
    """Demonstrate schema validation and error handling."""

    GraphTransformer()

    # Test with invalid inputs
    test_cases = [
        {
            "name": "Empty documents",
            "documents": [],
            "expected_error": "Documents list cannot be empty",
        },
        {
            "name": "Invalid relationships type",
            "documents": [Document(page_content="Test")],
            "allowed_relationships": "not_a_list",
            "expected_error": "allowed_relationships must be a list",
        },
        {
            "name": "Non-list documents",
            "documents": "not_a_list",
            "expected_error": "Documents must be a list",
        },
    ]

    for test in test_cases:
        try:
            # This would trigger the validation error
            pass
        except Exception as e:
            pass")


def type_hints_example() -> None:
    """Demonstrate proper type usage."""

    # Type-annotated function using GraphTransformer
    def extract_knowledge_graph(
        text_content: str,
        entity_types: list[str],
        relation_types: list[tuple[str, str, str]],
    ) -> list[str]:
        """Extract knowledge graph and return entity names.

        Args:
            text_content: Raw text to process
            entity_types: Allowed entity types
            relation_types: Allowed relationship patterns

        Returns:
            List of extracted entity names
        """
        GraphTransformer()
        [Document(page_content=text_content)]

        # This demonstrates the type-safe API
        # In real usage, would call:

        # Mock return for demonstration
        return ["Entity1", "Entity2", "Entity3"]

    # Example usage with proper types
    entities = extract_knowledge_graph(
        text_content="Sample text about companies and people",
        entity_types=["Person", "Company"],
        relation_types=[("Person", "WORKS_FOR", "Company")],
    )



if __name__ == "__main__":
    """Run all examples."""

    basic_example()
    advanced_example()
    schema_validation_example()
    type_hints_example()

