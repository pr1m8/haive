import operator
from typing import Annotated, Literal

from langchain_community.graphs.graph_document import GraphDocument
from langchain_core.documents import Document
from pydantic import BaseModel, Field

# Import models
from haive.agents.document_modifiers.kg.kg_map_merge.models import (
    EntityNode,
    EntityRelationship,
    KnowledgeGraph,
)


class KnowledgeGraphState(BaseModel):
    """State model for the parallel knowledge graph transformer."""

    contents: list[Document]

    # Graph documents and knowledge graphs
    graph_documents: Annotated[list[GraphDocument], operator.add] = Field(
        default_factory=list
    )
    knowledge_graphs: Annotated[list[KnowledgeGraph], operator.add] = Field(
        default_factory=list
    )
    final_knowledge_graph: KnowledgeGraph | None = Field(default=None)

    # Extracted components
    nodes: list[EntityNode] = Field(default_factory=list)
    relationships: list[EntityRelationship] = Field(default_factory=list)

    # Concurrent-safe index tracking
    index: int = Field(default=0)

    def should_continue(
        self,
    ) -> Literal[
        "map_graph_documents", "map_nodes", "map_relationships", "merge_graphs", "end"
    ]:
        """Determine the next step in the graph creation process."""
        if self.index < len(self.contents):
            return "map_graph_documents"
        if not self.nodes:
            return "map_nodes"
        if not self.relationships:
            return "map_relationships"
        if self.graph_documents or self.knowledge_graphs:
            return "merge_graphs"
        return "end"
