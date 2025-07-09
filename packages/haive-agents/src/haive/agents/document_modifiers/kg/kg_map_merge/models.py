from typing import Any

from langchain_community.graphs.graph_document import Node, Relationship
from pydantic import BaseModel, Field, model_validator


class EntityNode(BaseModel):
    """Represents an entity node in the knowledge graph.
    Extends the basic Node class with additional metadata and validation.
    """

    id: str = Field(..., description="Unique identifier for the entity")
    type: str = Field(..., description="Type or category of the entity")
    properties: dict[str, Any] = Field(
        default_factory=dict, description="Additional properties of the entity"
    )

    @model_validator(mode="after")
    def validate_node(self):
        """Validate the node properties."""
        # Ensure ID is not empty
        if not self.id or not isinstance(self.id, str):
            raise ValueError("Node ID must be a non-empty string")

        # Ensure type is not empty
        if not self.type or not isinstance(self.type, str):
            raise ValueError("Node type must be a non-empty string")

        return self

    @classmethod
    def from_graph_node(cls, node: Node):
        """Create an EntityNode from a GraphDocument Node.

        Args:
            node (Node): The input graph node

        Returns:
            EntityNode: Converted node with additional validation
        """
        return cls(id=node.id, type=node.type, properties=node.properties or {})


class EntityRelationship(BaseModel):
    """Represents a relationship between two entities in a knowledge graph.
    Extends the basic Relationship class with additional metadata and validation.
    """

    source: str = Field(..., description="Source entity ID")
    target: str = Field(..., description="Target entity ID")
    type: str = Field(..., description="Type of relationship")
    properties: dict[str, Any] = Field(
        default_factory=dict, description="Additional relationship properties"
    )

    # Additional fields for enhanced relationship representation
    confidence_score: float = Field(
        default=0.5, ge=0, le=1, description="Confidence score for the relationship"
    )
    supporting_evidence: str | None = Field(
        default=None, description="Textual evidence supporting the relationship"
    )

    @model_validator(mode="after")
    def validate_relationship(self):
        """Validate the relationship properties."""
        # Ensure source and target are non-empty strings
        if not self.source or not isinstance(self.source, str):
            raise ValueError("Source must be a non-empty string")

        if not self.target or not isinstance(self.target, str):
            raise ValueError("Target must be a non-empty string")

        if not self.type or not isinstance(self.type, str):
            raise ValueError("Relationship type must be a non-empty string")

        return self

    @classmethod
    def from_graph_relationship(
        cls,
        relationship: Relationship,
        confidence_score: float = 0.5,
        supporting_evidence: str | None = None,
    ):
        """Create an EntityRelationship from a GraphDocument Relationship.

        Args:
            relationship (Relationship): The input graph relationship
            confidence_score (float, optional): Confidence score for the relationship
            supporting_evidence (str, optional): Evidence supporting the relationship

        Returns:
            EntityRelationship: Converted relationship with additional validation
        """
        return cls(
            source=relationship.source,
            target=relationship.target,
            type=relationship.type,
            properties=relationship.properties or {},
            confidence_score=confidence_score,
            supporting_evidence=supporting_evidence,
        )


class KnowledgeGraph(BaseModel):
    """Represents a comprehensive knowledge graph."""

    nodes: list[EntityNode] = Field(
        default_factory=list, description="Nodes in the knowledge graph"
    )
    relationships: list[EntityRelationship] = Field(
        default_factory=list, description="Relationships in the knowledge graph"
    )

    def add_node(self, node: EntityNode):
        """Add a node to the knowledge graph.

        Args:
            node (EntityNode): Node to add
        """
        # Check for duplicates based on ID
        if not any(existing.id == node.id for existing in self.nodes):
            self.nodes.append(node)

    def add_relationship(self, relationship: EntityRelationship):
        """Add a relationship to the knowledge graph.

        Args:
            relationship (EntityRelationship): Relationship to add
        """
        # Check for duplicate relationships
        if not any(
            (
                existing.source == relationship.source
                and existing.target == relationship.target
                and existing.type == relationship.type
            )
            for existing in self.relationships
        ):
            self.relationships.append(relationship)

    def merge(self, other_graph: "KnowledgeGraph"):
        """Merge another knowledge graph into this one.

        Args:
            other_graph (KnowledgeGraph): Graph to merge
        """
        for node in other_graph.nodes:
            self.add_node(node)

        for relationship in other_graph.relationships:
            self.add_relationship(relationship)


# Example usage demonstrator
def main():
    # Create some example nodes
    person_node = EntityNode(
        id="marie_curie",
        type="Scientist",
        properties={
            "name": "Marie Curie",
            "nationality": "Polish-French",
            "field": "Physics and Chemistry",
        },
    )

    country_node = EntityNode(
        id="poland",
        type="Country",
        properties={"name": "Poland", "continent": "Europe"},
    )

    # Create an example relationship
    relationship = EntityRelationship(
        source="marie_curie",
        target="poland",
        type="BORN_IN",
        confidence_score=0.9,
        supporting_evidence="Marie Curie was born in Warsaw, Poland in 1867",
    )

    # Create a knowledge graph
    kg = KnowledgeGraph()
    kg.add_node(person_node)
    kg.add_node(country_node)
    kg.add_relationship(relationship)

    # Print out the graph details
    print("Nodes:")
    for node in kg.nodes:
        print(f"- {node.id} (Type: {node.type})")

    print("\nRelationships:")
    for rel in kg.relationships:
        print(
            f"- {rel.source} --({rel.type})--> {rel.target} (Confidence: {rel.confidence_score})"
        )


if __name__ == "__main__":
    main()
