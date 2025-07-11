"""Document Splitter Engine for chunking documents into smaller segments.

This module provides the DocumentSplitterEngine that takes a list of documents and
splits them into chunks using various splitting strategies while preserving
and enhancing metadata.
"""

import time
from typing import Any, Dict, List, Optional, Union

from langchain.schema import Document
from pydantic import BaseModel, Field

from haive.core.common.config.runnable import RunnableConfig
from haive.core.engine.base.base import InvokableEngine
from haive.core.engine.base.types import EngineType
from haive.core.engine.document.config import ProcessedDocument
from haive.core.schema.prebuilt.document_state import DocumentState

from .base import (
    CharacterTextSplitter,
    HTMLHeaderTextSplitter,
    LatexTextSplitter,
    MarkdownHeaderTextSplitter,
    MarkdownTextSplitter,
    NLTKTextSplitter,
    PythonCodeTextSplitter,
    RecursiveCharacterTextSplitter,
    RecursiveJsonSplitter,
    SentenceTransformersTokenTextSplitter,
    SpacyTextSplitter,
    TokenTextSplitter,
)
from .config import DocSplitterType


class DocSplitterInputSchema(BaseModel):
    """Input schema for document splitter engine."""

    documents: List[Document] = Field(..., description="List of documents to split")
    splitter_type: Optional[DocSplitterType] = Field(
        default=DocSplitterType.RECURSIVE_CHARACTER,
        description="Type of splitter to use",
    )
    chunk_size: int = Field(default=1000, description="Target chunk size")
    chunk_overlap: int = Field(default=200, description="Overlap between chunks")
    separators: Optional[List[str]] = Field(
        default=None, description="Custom separators for splitting"
    )
    keep_separator: bool = Field(default=True, description="Keep separators in chunks")
    strip_whitespace: bool = Field(
        default=True, description="Strip whitespace from chunks"
    )

    # Advanced options
    length_function: str = Field(
        default="len", description="Function to measure chunk length"
    )
    add_start_index: bool = Field(
        default=True, description="Add start index to metadata"
    )

    class Config:
        arbitrary_types_allowed = True


class DocSplitterOutputSchema(BaseModel):
    """Output schema for document splitter engine."""

    documents: List[Document] = Field(..., description="Split documents with metadata")
    total_documents: int = Field(..., description="Total number of output documents")
    total_chunks: int = Field(..., description="Total number of chunks created")
    original_documents: int = Field(
        ..., description="Number of original input documents"
    )
    operation_time: float = Field(..., description="Time taken for splitting operation")
    splitter_type: str = Field(..., description="Splitter type used")
    splitter_config: Dict[str, Any] = Field(
        ..., description="Splitter configuration used"
    )

    class Config:
        arbitrary_types_allowed = True


class DocSplitterConfig(BaseModel):
    """Configuration for document splitter engine."""

    name: str = Field(default="doc_splitter", description="Engine name")
    splitter_type: DocSplitterType = Field(
        default=DocSplitterType.RECURSIVE_CHARACTER, description="Default splitter type"
    )
    chunk_size: int = Field(default=1000, description="Default chunk size")
    chunk_overlap: int = Field(default=200, description="Default chunk overlap")
    separators: Optional[List[str]] = Field(
        default=None, description="Default separators"
    )
    keep_separator: bool = Field(default=True, description="Keep separators by default")
    strip_whitespace: bool = Field(
        default=True, description="Strip whitespace by default"
    )
    add_start_index: bool = Field(
        default=True, description="Add start index by default"
    )

    class Config:
        use_enum_values = True


class DocumentSplitterEngine(InvokableEngine[DocumentState, DocumentState]):
    """Document splitter engine for chunking documents.

    This engine takes a list of documents and splits them into smaller chunks
    using various splitting strategies. Each output document includes metadata
    indicating it's a split document and details about the splitting process.

    Examples:
        Basic usage::

            engine = DocumentSplitterEngine(config=DocSplitterConfig())
            input_data = DocSplitterInputSchema(documents=docs)
            result = engine.invoke(input_data)

        With custom configuration::

            config = DocSplitterConfig(
                splitter_type=DocSplitterType.RECURSIVE_CHARACTER,
                chunk_size=1500,
                chunk_overlap=100
            )
            engine = DocumentSplitterEngine(config=config)
            runnable = engine.create_runnable({"chunk_size": 2000})
            result = runnable.invoke(input_data)
    """

    def __init__(self, config: Optional[DocSplitterConfig] = None):
        """Initialize the document splitter engine.

        Args:
            config: Configuration for the splitter engine
        """
        super().__init__()
        self.config = config or DocSplitterConfig()
        self.engine_type = EngineType.DOCUMENT_SPLITTER

    def create_runnable(
        self, runnable_config: Optional[Dict[str, Any]] = None
    ) -> "DocumentSplitterEngine":
        """Create a runnable instance with optional configuration overrides.

        Args:
            runnable_config: Configuration overrides for this runnable

        Returns:
            New DocumentSplitterEngine instance with updated configuration
        """
        if runnable_config:
            # Merge configurations
            config_dict = self.config.model_dump()
            config_dict.update(runnable_config)

            # Create new config and engine
            new_config = DocSplitterConfig.model_validate(config_dict)
            return DocumentSplitterEngine(config=new_config)

        return self

    def invoke(
        self,
        input_data: Union[DocumentState, List[Document], Dict[str, Any]],
        config: Optional[RunnableConfig] = None,
    ) -> DocumentState:
        """Split documents into chunks.

        Args:
            input_data: Document state or raw documents
            config: Optional runnable configuration

        Returns:
            DocumentState with split documents and metadata
        """
        start_time = time.time()

        try:
            # Normalize input to DocumentState
            if isinstance(input_data, DocumentState):
                # Already document state
                document_state = input_data
                documents_to_split = document_state.raw_documents or []
            elif isinstance(input_data, list):
                # List of raw documents
                document_state = DocumentState(raw_documents=input_data)
                documents_to_split = input_data
            elif isinstance(input_data, dict):
                # Dictionary input
                document_state = DocumentState.model_validate(input_data)
                documents_to_split = document_state.raw_documents or []
            else:
                raise ValueError(f"Invalid input type: {type(input_data)}")

            # Use engine config for splitting parameters
            splitter_type = self.config.splitter_type
            chunk_size = self.config.chunk_size
            chunk_overlap = self.config.chunk_overlap
            separators = self.config.separators
            keep_separator = self.config.keep_separator
            strip_whitespace = self.config.strip_whitespace
            add_start_index = self.config.add_start_index

            # Create splitter based on type
            splitter = self._create_splitter(
                splitter_type=splitter_type,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=separators,
                keep_separator=keep_separator,
                add_start_index=add_start_index,
            )

            # Split documents and add metadata
            split_raw_documents = []
            split_processed_documents = []
            total_chunks = 0

            for doc_index, document in enumerate(documents_to_split):
                chunks = splitter.split_documents([document])

                for chunk_index, chunk in enumerate(chunks):
                    # Generate unique IDs for parent-child linking
                    parent_doc_id = (
                        document.metadata.get("document_id")
                        or f"doc_{doc_index}_{int(start_time)}"
                    )
                    chunk_id = f"{parent_doc_id}_chunk_{chunk_index}"

                    # Add splitter metadata to raw document
                    enhanced_metadata = {
                        **chunk.metadata,
                        # Document hierarchy and linking
                        "document_id": chunk_id,
                        "parent_document_id": parent_doc_id,
                        "is_split": True,
                        "is_child_document": True,
                        "document_hierarchy_level": (
                            document.metadata.get("document_hierarchy_level", 0) + 1
                        ),
                        # Splitter identification
                        "splitter_type": splitter_type.value,
                        "splitter_engine": "DocumentSplitterEngine",
                        # Chunk information and relationships
                        "chunk_index": chunk_index,
                        "chunk_id": chunk_id,
                        "total_chunks_in_doc": len(chunks),
                        "original_doc_index": doc_index,
                        "sibling_chunk_ids": [
                            f"{parent_doc_id}_chunk_{i}" for i in range(len(chunks))
                        ],
                        # Parent document information
                        "parent_document_metadata": {
                            "source": document.metadata.get("source", "unknown"),
                            "original_length": len(document.page_content),
                            "parent_document_type": document.metadata.get(
                                "document_type", "unknown"
                            ),
                        },
                        # Splitting configuration
                        "chunk_size": chunk_size,
                        "chunk_overlap": chunk_overlap,
                        "split_timestamp": start_time,
                        # Chunk characteristics
                        "chunk_length": len(chunk.page_content),
                        "chunk_length_function": "len",
                        "chunk_position_in_parent": {
                            "start_char": getattr(chunk.metadata, "start_index", None),
                            "end_char": (
                                getattr(chunk.metadata, "start_index", 0)
                                + len(chunk.page_content)
                                if hasattr(chunk.metadata, "start_index")
                                else None
                            ),
                        },
                    }

                    # Add separators info if used
                    if separators:
                        enhanced_metadata["separators_used"] = separators

                    # Create enhanced raw document
                    enhanced_chunk = Document(
                        page_content=chunk.page_content, metadata=enhanced_metadata
                    )
                    split_raw_documents.append(enhanced_chunk)

                    # Create processed document
                    processed_chunk = ProcessedDocument(
                        content=chunk.page_content,
                        metadata=enhanced_metadata,
                        source_type=document_state.source_type,
                        loader_name=f"splitter_{splitter_type.value}",
                        character_count=len(chunk.page_content),
                        word_count=len(chunk.page_content.split()),
                        chunk_count=1,  # Each chunk is one chunk
                        chunks=[enhanced_chunk],
                        format=None,  # Will be determined from metadata
                        processing_time=0.0,  # Individual chunk processing time
                    )
                    split_processed_documents.append(processed_chunk)
                    total_chunks += 1

            operation_time = time.time() - start_time

            # Update document state with split results
            document_state.raw_documents = split_raw_documents
            document_state.documents = split_processed_documents
            document_state.total_documents = len(split_raw_documents)
            document_state.successful_documents = len(split_raw_documents)
            document_state.processing_stage = "split_completed"

            # Add splitter metadata to workflow metadata
            document_state.workflow_metadata.update(
                {
                    "splitter_config": {
                        "splitter_type": splitter_type.value,
                        "chunk_size": chunk_size,
                        "chunk_overlap": chunk_overlap,
                        "separators": separators,
                        "keep_separator": keep_separator,
                        "strip_whitespace": strip_whitespace,
                        "add_start_index": add_start_index,
                    },
                    "splitting_operation_time": operation_time,
                    "total_chunks_created": total_chunks,
                    "original_documents_count": len(documents_to_split),
                }
            )

            return document_state

        except Exception as e:
            operation_time = time.time() - start_time

            # Create error document state
            if "document_state" not in locals():
                document_state = DocumentState()

            document_state.processing_stage = "split_failed"
            document_state.errors.append(
                {
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "stage": "splitting",
                    "timestamp": start_time,
                }
            )
            document_state.workflow_metadata.update(
                {
                    "splitter_error": {
                        "error": str(e),
                        "error_type": type(e).__name__,
                        "operation_time": operation_time,
                    }
                }
            )

            return document_state

    async def ainvoke(
        self,
        input_data: Union[DocumentState, List[Document], Dict[str, Any]],
        config: Optional[RunnableConfig] = None,
    ) -> DocumentState:
        """Asynchronously split documents into chunks.

        Args:
            input_data: Input documents and configuration
            config: Optional runnable configuration

        Returns:
            DocSplitterOutputSchema with split documents and metadata
        """
        # For now, run synchronously in thread pool
        # TODO: Implement true async processing if needed
        import asyncio

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.invoke, input_data, config)

    def _create_splitter(
        self,
        splitter_type: DocSplitterType,
        chunk_size: int,
        chunk_overlap: int,
        separators: Optional[List[str]],
        keep_separator: bool,
        add_start_index: bool,
    ):
        """Create the appropriate text splitter based on type.

        Args:
            splitter_type: Type of splitter to create
            chunk_size: Target chunk size
            chunk_overlap: Overlap between chunks
            separators: Custom separators (for applicable splitters)
            keep_separator: Whether to keep separators
            add_start_index: Whether to add start index

        Returns:
            Configured text splitter instance
        """
        common_kwargs = {
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "add_start_index": add_start_index,
        }

        if splitter_type == DocSplitterType.CHARACTER:
            return CharacterTextSplitter(
                separator="\n\n" if not separators else separators[0],
                keep_separator=keep_separator,
                **common_kwargs,
            )

        elif splitter_type == DocSplitterType.RECURSIVE_CHARACTER:
            splitter_separators = separators or ["\n\n", "\n", ". ", " ", ""]
            return RecursiveCharacterTextSplitter(
                separators=splitter_separators,
                keep_separator=keep_separator,
                **common_kwargs,
            )

        elif splitter_type == DocSplitterType.TOKEN:
            return TokenTextSplitter(**common_kwargs)

        elif splitter_type == DocSplitterType.NLTK:
            return NLTKTextSplitter(**common_kwargs)

        elif splitter_type == DocSplitterType.SPACY:
            return SpacyTextSplitter(**common_kwargs)

        elif splitter_type == DocSplitterType.SENTENCE_TRANSFORMERS:
            return SentenceTransformersTokenTextSplitter(**common_kwargs)

        elif splitter_type == DocSplitterType.HTML:
            return HTMLHeaderTextSplitter()

        elif splitter_type == DocSplitterType.MARKDOWN:
            return MarkdownTextSplitter(**common_kwargs)

        elif splitter_type == DocSplitterType.LATEX:
            return LatexTextSplitter(**common_kwargs)

        elif splitter_type == DocSplitterType.PYTHON:
            return PythonCodeTextSplitter(**common_kwargs)

        elif splitter_type == DocSplitterType.JSON:
            return RecursiveJsonSplitter()

        else:
            # Default to recursive character splitter
            return RecursiveCharacterTextSplitter(**common_kwargs)

    @staticmethod
    def get_children_docs(
        document_state: DocumentState, parent_id: str
    ) -> List[Document]:
        """Get all child documents for a given parent document ID.

        Args:
            document_state: Document state containing split documents
            parent_id: Parent document ID to find children for

        Returns:
            List of child documents
        """
        return [
            doc
            for doc in document_state.raw_documents
            if doc.metadata.get("parent_document_id") == parent_id
        ]

    @staticmethod
    def get_parent_doc(
        document_state: DocumentState, child_id: str
    ) -> Optional[Document]:
        """Get parent document for a given child document ID.

        Args:
            document_state: Document state containing documents
            child_id: Child document ID to find parent for

        Returns:
            Parent document if found, None otherwise
        """
        # Find the child document first
        child_doc = None
        for doc in document_state.raw_documents:
            if doc.metadata.get("document_id") == child_id:
                child_doc = doc
                break

        if not child_doc:
            return None

        parent_id = child_doc.metadata.get("parent_document_id")
        if not parent_id:
            return None

        # Find parent document
        for doc in document_state.raw_documents:
            if doc.metadata.get("document_id") == parent_id:
                return doc

        return None

    @staticmethod
    def get_sibling_docs(
        document_state: DocumentState, chunk_id: str
    ) -> List[Document]:
        """Get all sibling documents (same parent) for a given chunk.

        Args:
            document_state: Document state containing documents
            chunk_id: Chunk ID to find siblings for

        Returns:
            List of sibling documents (including the original chunk)
        """
        # Find the document and its parent
        target_doc = None
        for doc in document_state.raw_documents:
            if doc.metadata.get("document_id") == chunk_id:
                target_doc = doc
                break

        if not target_doc:
            return []

        parent_id = target_doc.metadata.get("parent_document_id")
        if not parent_id:
            return [target_doc]  # No siblings if no parent

        # Return all documents with same parent
        return DocumentSplitterEngine.get_children_docs(document_state, parent_id)

    @staticmethod
    def build_document_tree(document_state: DocumentState) -> Dict[str, Any]:
        """Build a tree structure showing document relationships.

        Args:
            document_state: Document state containing documents

        Returns:
            Dictionary representing the document tree structure
        """
        tree = {}

        # Group documents by hierarchy level
        by_level = {}
        for doc in document_state.raw_documents:
            level = doc.metadata.get("document_hierarchy_level", 0)
            if level not in by_level:
                by_level[level] = []
            by_level[level].append(doc)

        # Build tree structure
        for level in sorted(by_level.keys()):
            for doc in by_level[level]:
                doc_id = doc.metadata.get("document_id", "unknown")
                parent_id = doc.metadata.get("parent_document_id")

                doc_info = {
                    "document_id": doc_id,
                    "content_preview": (
                        doc.page_content[:100] + "..."
                        if len(doc.page_content) > 100
                        else doc.page_content
                    ),
                    "chunk_index": doc.metadata.get("chunk_index"),
                    "chunk_length": doc.metadata.get(
                        "chunk_length", len(doc.page_content)
                    ),
                    "is_split": doc.metadata.get("is_split", False),
                    "children": [],
                }

                if parent_id and parent_id in tree:
                    # Add as child to parent
                    tree[parent_id]["children"].append(doc_info)
                else:
                    # Root level document
                    tree[doc_id] = doc_info

        return tree


# Factory functions for common use cases
def create_document_splitter(
    splitter_type: DocSplitterType = DocSplitterType.RECURSIVE_CHARACTER,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    **kwargs,
) -> DocumentSplitterEngine:
    """Create a document splitter engine with specified configuration.

    Args:
        splitter_type: Type of splitter to use
        chunk_size: Target chunk size
        chunk_overlap: Overlap between chunks
        **kwargs: Additional configuration options

    Returns:
        Configured DocumentSplitterEngine instance
    """
    config = DocSplitterConfig(
        splitter_type=splitter_type,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        **kwargs,
    )
    return DocumentSplitterEngine(config=config)


def create_recursive_splitter(
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    separators: Optional[List[str]] = None,
) -> DocumentSplitterEngine:
    """Create a recursive character text splitter engine.

    Args:
        chunk_size: Target chunk size
        chunk_overlap: Overlap between chunks
        separators: Custom separators to use

    Returns:
        DocumentSplitterEngine configured for recursive splitting
    """
    config = DocSplitterConfig(
        splitter_type=DocSplitterType.RECURSIVE_CHARACTER,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
    )
    return DocumentSplitterEngine(config=config)


def create_semantic_splitter(
    chunk_size: int = 1000,
    chunk_overlap: int = 100,
) -> DocumentSplitterEngine:
    """Create a semantic text splitter engine.

    Args:
        chunk_size: Target chunk size
        chunk_overlap: Overlap between chunks

    Returns:
        DocumentSplitterEngine configured for semantic splitting
    """
    # For now, use recursive as semantic isn't fully implemented
    config = DocSplitterConfig(
        splitter_type=DocSplitterType.RECURSIVE_CHARACTER,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " "],
    )
    return DocumentSplitterEngine(config=config)
