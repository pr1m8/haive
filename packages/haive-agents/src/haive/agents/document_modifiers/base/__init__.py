"""Base classes and utilities for document modification agents.

This module provides the foundational components shared across all document
modifier agents. It includes the base state schema for document processing,
utilities for document management, and common models used throughout the
document modifiers module.

The primary component is DocumentModifierState, which provides:
    - Document collection management
    - Text extraction and aggregation
    - Document validation
    - State manipulation methods

Classes:
    DocumentModifierState: Base state schema for document processing agents

Example:
    Basic usage with documents::

        from haive.agents.document_modifiers.base.state import DocumentModifierState
        from langchain_core.documents import Document

        # Create state from documents
        docs = [
            Document(page_content="First document"),
            Document(page_content="Second document")
        ]
        state = DocumentModifierState.from_documents(docs)

        # Access document properties
        print(f"Number of documents: {state.num_documents}")
        print(f"Combined text: {state.documents_text}")

    Extending the base state::

        from haive.agents.document_modifiers.base.state import DocumentModifierState
        from pydantic import Field

        class ExtendedDocumentState(DocumentModifierState):
            '''Custom state with additional fields.'''

            processed_count: int = Field(default=0)
            metadata: dict = Field(default_factory=dict)

            def mark_processed(self) -> None:
                '''Mark current documents as processed.'''
                self.processed_count = self.num_documents

See Also:
    :mod:`haive.agents.document_modifiers.base.models`: Additional model definitions
    :class:`haive.agents.document_modifiers.base.state.DocumentModifierState`: Main state class

Note:
    This module is typically not used directly but inherited by specific
    document modifier agents that build upon its functionality.
"""
