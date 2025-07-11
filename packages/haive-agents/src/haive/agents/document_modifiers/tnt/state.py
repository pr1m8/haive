"""State management for taxonomy generation workflow.

This module defines the state schema used throughout the taxonomy generation process.
It provides a structured way to track documents, their groupings into minibatches,
and the evolution of taxonomy clusters over multiple iterations.

Example:
    Basic usage of the state class::

        state = TaxonomyGenerationState(
            documents=[Doc(id="1", content="text")],
            minibatches=[[0]],
            clusters=[[{"id": 1, "name": "Category"}]]
        )
"""

import operator
from typing import Annotated

from langchain_core.documents import Document
from pydantic import BaseModel, Field

from haive.agents.document_modifiers.tnt.models import Doc


class TaxonomyGenerationState(BaseModel):
    """Represents the state passed between graph nodes in the taxonomy generation process.

    This class maintains the complete state of the taxonomy generation workflow,
    tracking raw documents, their organization into processing batches, and the
    history of taxonomy revisions.

    Attributes:
        documents (List[Doc]): List of document objects, each containing:
            - id: Unique identifier
            - content: Raw text
            - summary: Generated summary (added in first step)
            - explanation: Summary explanation (added in first step)
            - category: Assigned taxonomy category (added later)
        minibatches (List[List[int]]): Groups of document indices for batch processing.
            Each inner list contains indices referencing documents in the documents list.
        clusters (List[List[dict]]): History of taxonomy revisions. Each revision is a
            list of cluster dictionaries containing:
            - id: Cluster identifier
            - name: Category name
            - description: Category description

    Example:
        >>> docs = [Doc(id="1", content="text")]
        >>> state = TaxonomyGenerationState(
        ...     documents=docs,
        ...     minibatches=[[0]],
        ...     clusters=[[{"id": 1, "name": "Tech", "description": "Technology"}]]
        ... )
    """

    # The raw docs; we inject summaries within them in the first step
    documents: list[Doc] = Field(description="The raw documents.")
    # Indices to be concise
    minibatches: list[list[int]] = Field(
        default=[], description="The indices to be concise."
    )
    # Candidate Taxonomies (full trajectory)
    clusters: Annotated[list[list[dict]], operator.add] = Field(
        default=[], description="The candidate taxonomies."
    )

    @classmethod
    def from_documents(cls, documents: list[Document]) -> "TaxonomyGenerationState":
        """Initialize state from a list of LangChain Document objects."""
        docs = [Doc.from_document(doc) for doc in documents]
        return cls(documents=docs, minibatches=[], clusters=[])
