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
    print("=== Basic Graph Transformation Example ===")

    # Create transformer instance
    transformer = GraphTransformer()

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

    print(f"Processing {len(documents)} documents...")
    print(f"Allowed nodes: {allowed_nodes}")
    print(f"Allowed relationships: {allowed_relationships}")

    try:
        # Transform documents (this would normally use an actual LLM)
        # For demonstration, we'll just show the structure
        print("\nThis would normally call the LLM to extract:")
        for i, doc in enumerate(documents):
            print(f"Document {i+1}: {doc.page_content}")

        # In a real scenario:
        # graphs = transformer.transform_documents(
        #     documents=documents,
        #     allowed_nodes=allowed_nodes,
        #     allowed_relationships=allowed_relationships,
        #     strict_mode=True
        # )

        print("\nExpected output structure:")
        print("- GraphDocument objects with nodes and relationships")
        print("- Nodes: Person entities (John Smith, Sarah Johnson)")
        print("- Nodes: Organization entities (Acme Corporation)")
        print("- Nodes: Location entities (New York)")
        print("- Relationships: WORKS_FOR, LEADS, LOCATED_IN")

    except Exception as e:
        print(f"Error: {e}")
        print("Note: This example requires a configured LLM to run fully.")


def advanced_example() -> None:
    """Demonstrate advanced configuration with properties."""
    print("\n=== Advanced Configuration Example ===")

    transformer = GraphTransformer()

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
    allowed_nodes = ["Person", "Organization", "Field", "Publication"]
    allowed_relationships = [
        ("Person", "WORKS_FOR", "Organization"),
        ("Person", "LEADS", "Organization"),
        ("Person", "RESEARCHES", "Field"),
        ("Person", "AUTHORED", "Publication"),
    ]

    # Properties to extract
    node_properties = ["age", "title", "experience_years", "expertise"]
    relationship_properties = ["since", "duration", "role"]

    print(f"Document: {documents[0].page_content}")
    print(f"Node properties to extract: {node_properties}")
    print(f"Relationship properties to extract: {relationship_properties}")

    # Additional instructions for better extraction
    additional_instructions = (
        "Extract specific details about experience, education, and achievements. "
        "Include temporal information where available."
    )

    print(f"\nAdditional instructions: {additional_instructions}")
    print("\nExpected enhanced output:")
    print("- Nodes with properties (age: 35, title: software engineer)")
    print("- Relationships with properties (since: 2018, role: team lead)")


def schema_validation_example() -> None:
    """Demonstrate schema validation and error handling."""
    print("\n=== Schema Validation Example ===")

    transformer = GraphTransformer()

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
        print(f"\nTesting: {test['name']}")
        try:
            # This would trigger the validation error
            print(f"Expected error: {test['expected_error']}")
            # transformer.transform_documents(**test)
        except Exception as e:
            print(f"✓ Correctly caught error: {e}")


def type_hints_example() -> None:
    """Demonstrate proper type usage."""
    print("\n=== Type Hints Example ===")

    # Type-annotated function using GraphTransformer
    def extract_knowledge_graph(
        text_content: str,
        entity_types: List[str],
        relation_types: List[tuple[str, str, str]],
    ) -> List[str]:
        """Extract knowledge graph and return entity names.

        Args:
            text_content: Raw text to process
            entity_types: Allowed entity types
            relation_types: Allowed relationship patterns

        Returns:
            List of extracted entity names
        """
        transformer = GraphTransformer()
        documents = [Document(page_content=text_content)]

        # This demonstrates the type-safe API
        # In real usage, would call:
        # graphs = transformer.transform_documents(
        #     documents=documents,
        #     allowed_nodes=entity_types,
        #     allowed_relationships=relation_types
        # )

        # Mock return for demonstration
        return ["Entity1", "Entity2", "Entity3"]

    # Example usage with proper types
    entities = extract_knowledge_graph(
        text_content="Sample text about companies and people",
        entity_types=["Person", "Company"],
        relation_types=[("Person", "WORKS_FOR", "Company")],
    )

    print(f"Function with type hints executed successfully")
    print(f"Mock extracted entities: {entities}")


if __name__ == "__main__":
    """Run all examples."""
    print("GraphTransformer Examples")
    print("=" * 50)

    basic_example()
    advanced_example()
    schema_validation_example()
    type_hints_example()

    print("\n" + "=" * 50)
    print("Examples completed successfully!")
    print("\nNote: Full functionality requires LLM configuration.")
    print("See the module documentation for complete setup instructions.")
