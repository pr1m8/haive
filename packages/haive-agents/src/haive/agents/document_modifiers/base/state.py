"""Base state schema for document modification agents.

This module defines the DocumentModifierState class which serves as the
foundation for all document processing agents in the haive framework.
"""

from typing import List, Optional

from haive.core.schema import StateSchema
from langchain_core.documents import Document
from pydantic import Field, computed_field, field_validator, model_validator


class DocumentModifierState(StateSchema):
    """Base state schema for document modification agents.

    This class provides the core state management for all document processing
    operations. It handles document collections, provides computed properties
    for common operations, and includes validation to ensure data integrity.

    The state maintains a list of documents and provides utilities for:
    - Accessing combined document text
    - Counting documents
    - Adding/removing documents
    - Validating document collections

    Attributes:
        name: Optional identifier for this document modifier instance.
        description: Optional description of the modifier's purpose.
        documents: List of Document objects to be processed.

    Properties:
        documents_text: Combined text content of all documents.
        num_documents: Total count of documents in the collection.

    Example:
        Creating and using document state::

            >>> from langchain_core.documents import Document
            >>> docs = [Document(page_content="Hello"), Document(page_content="World")]
            >>> state = DocumentModifierState.from_documents(docs)
            >>> print(state.documents_text)
            'Hello\nWorld'
            >>> print(state.num_documents)
            2

        Adding documents dynamically::

            >>> new_doc = Document(page_content="New content")
            >>> state.documents.append(new_doc)
            >>> print(state.num_documents)
            3

    Raises:
        ValueError: If no documents are provided (empty list).

    Note:
        The state automatically validates that at least one document
        is present to prevent processing empty collections.
    """

    name: Optional[str] = Field(
        default=None, description="The name of the document modifier."
    )
    description: Optional[str] = Field(
        default=None, description="The description of the document modifier."
    )
    documents: List[Document] = Field(
        default_factory=list, description="The documents to process."
    )

    # is_split: bool = Field(default=False,description="Whether the documents are split.")
    # embeded_documents:List[Document] = Field(default_factory=list,description="The embeded documents.")
    # split_documents:List[Document] = Field(default_factory=list,description="The split documents.")
    # transformed_documents:List[Document] = Field(default_factory=list,description="The transformed documents.")
    # annotations:List[Annotation]
    @classmethod
    def from_documents(cls, documents: List[Document]) -> "DocumentModifierState":
        """Create a DocumentModifierState from a list of documents.

        This is a convenience factory method for creating state instances
        when you already have a collection of documents.

        Args:
            documents: List of Document objects to initialize the state with.

        Returns:
            New DocumentModifierState instance containing the provided documents.

        Raises:
            ValueError: If the documents list is empty.

        Example:
            >>> docs = [Document(page_content="Content 1"), Document(page_content="Content 2")]
            >>> state = DocumentModifierState.from_documents(docs)
            >>> print(state.num_documents)
            2
        """
        return cls(documents=documents)

    @computed_field
    @property
    def documents_text(self) -> str:
        """Get the combined text content of all documents.

        This property concatenates the page_content of all documents
        in the collection, separated by newlines. Useful for operations
        that need to process all document text at once.

        Returns:
            String containing all document texts joined by newlines.

        Example:
            >>> state.documents = [Document(page_content="First"), Document(page_content="Second")]
            >>> print(state.documents_text)
            'First\nSecond'
        """
        return "\n".join([doc.page_content for doc in self.documents])

    @computed_field
    @property
    def num_documents(self) -> int:
        """Get the total number of documents in the collection.

        Returns:
            Integer count of documents currently in the state.

        Example:
            >>> print(f"Processing {state.num_documents} documents")
            Processing 5 documents
        """
        return len(self.documents)

    @model_validator(mode="after")
    def validate_documents(self):
        """Validate that at least one document is present.

        This validator runs after model initialization to ensure
        the state contains at least one document for processing.

        Returns:
            Self if validation passes.

        Raises:
            ValueError: If documents list is empty.
        """
        if self.num_documents == 0:
            raise ValueError("At least one document is required.")
        return self

    @field_validator("documents")
    def validate_documents_field(cls, v):
        """Validate the documents field during assignment.

        Args:
            v: The documents list being validated.

        Returns:
            The validated documents list.

        Note:
            This validator ensures type safety but allows empty lists
            during field assignment. The model validator handles the
            non-empty requirement.
        """
        return v

    @classmethod
    def add_document(cls, document: Document) -> "DocumentModifierState":
        """Add a single document to the state.

        Note: This method has issues with the class method implementation.
        Consider using instance methods instead for document manipulation.

        Args:
            document: Document to add to the collection.

        Returns:
            New state instance with the document added.
        """
        # NOTE: This implementation appears incorrect - should be instance method
        return cls(documents=cls.documents + [document])

    @classmethod
    def add_documents(cls, documents: List[Document]) -> "DocumentModifierState":
        """Add multiple documents to the state.

        Note: This method has issues with the class method implementation.
        Consider using instance methods instead for document manipulation.

        Args:
            documents: List of documents to add.

        Returns:
            New state instance with documents added.
        """
        # NOTE: This implementation appears incorrect - should be instance method
        return cls(documents=cls.documents + documents)

    @classmethod
    def remove_document(cls, document: Document) -> "DocumentModifierState":
        """Remove a specific document from the state.

        Note: This method has issues with the class method implementation.
        Consider using instance methods instead for document manipulation.

        Args:
            document: Document to remove from the collection.

        Returns:
            New state instance with the document removed.
        """
        # NOTE: This implementation appears incorrect - should be instance method
        return cls(documents=cls.documents - [document])

    @classmethod
    def remove_documents(cls, documents: List[Document]) -> "DocumentModifierState":
        """Remove multiple documents from the state.

        Note: This method has issues with the class method implementation.
        Consider using instance methods instead for document manipulation.

        Args:
            documents: List of documents to remove.

        Returns:
            New state instance with documents removed.
        """
        # NOTE: This implementation appears incorrect - should be instance method
        return cls(documents=cls.documents - documents)
