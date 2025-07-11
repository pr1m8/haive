"""Document Transformer Engine that works with DocumentState and proper field mappings.

This module provides the DocumentTransformerEngine that takes DocumentState and
transforms documents while preserving and enhancing metadata with parent-child
relationships and transformation details.
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

from .types import DocTransformerType


class DocTransformerConfig(BaseModel):
    """Configuration for document transformer engine."""

    name: str = Field(default="doc_transformer", description="Engine name")
    transformer_type: DocTransformerType = Field(
        default=DocTransformerType.HTML_TO_TEXT,
        description="Type of document transformer to use",
    )

    # HTML transformer options
    ignore_links: bool = Field(
        default=True, description="Whether to ignore links in HTML"
    )
    ignore_images: bool = Field(
        default=True, description="Whether to ignore images in HTML"
    )

    # BeautifulSoup options
    unwanted_tags: List[str] = Field(
        default_factory=lambda: ["script", "style"],
        description="Tags to remove from HTML",
    )
    tags_to_extract: List[str] = Field(
        default_factory=lambda: ["p", "li", "div", "a"],
        description="Tags to extract from HTML",
    )
    unwanted_classnames: List[str] = Field(
        default_factory=list, description="Classnames to remove from HTML"
    )
    remove_comments: bool = Field(
        default=False, description="Whether to remove comments from HTML"
    )

    # Markdown options
    heading_style: str = Field(
        default="ATX", description="Heading style for markdown conversion"
    )
    autolinks: bool = Field(
        default=True, description="Whether to use automatic link style"
    )

    # Embeddings filter options
    similarity_threshold: float = Field(
        default=0.95, description="Threshold for embedding similarity filtering"
    )
    embeddings_model: Optional[Any] = Field(
        default=None, description="Embeddings model for similarity filtering"
    )

    # Translation options
    target_language: str = Field(
        default="en", description="Target language for translation"
    )

    # Document tracking options
    preserve_hierarchy: bool = Field(
        default=True,
        description="Whether to preserve document hierarchy during transformation",
    )
    add_transformation_metadata: bool = Field(
        default=True, description="Whether to add transformation metadata to documents"
    )

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True


class DocumentTransformerEngine(InvokableEngine[DocumentState, DocumentState]):
    """Document transformer engine for transforming documents.

    This engine takes DocumentState and transforms the documents using various
    transformation strategies while maintaining parent-child relationships and
    adding transformation metadata.

    Examples:
        Basic usage::

            engine = DocumentTransformerEngine(config=DocTransformerConfig())
            result = engine.invoke(document_state)

        With custom configuration::

            config = DocTransformerConfig(
                transformer_type=DocTransformerType.HTML_TO_MARKDOWN,
                heading_style="Setext",
                autolinks=False
            )
            engine = DocumentTransformerEngine(config=config)
            runnable = engine.create_runnable({"ignore_links": False})
            result = runnable.invoke(document_state)
    """

    def __init__(self, config: Optional[DocTransformerConfig] = None):
        """Initialize the document transformer engine.

        Args:
            config: Configuration for the transformer engine
        """
        super().__init__()
        self.config = config or DocTransformerConfig()
        self.engine_type = EngineType.DOCUMENT_TRANSFORMER

    def create_runnable(
        self, runnable_config: Optional[Dict[str, Any]] = None
    ) -> "DocumentTransformerEngine":
        """Create a runnable instance with optional configuration overrides.

        Args:
            runnable_config: Configuration overrides for this runnable

        Returns:
            New DocumentTransformerEngine instance with updated configuration
        """
        if runnable_config:
            # Merge configurations
            config_dict = self.config.model_dump()
            config_dict.update(runnable_config)

            # Create new config and engine
            new_config = DocTransformerConfig.model_validate(config_dict)
            return DocumentTransformerEngine(config=new_config)

        return self

    def invoke(
        self,
        input_data: Union[DocumentState, List[Document], Dict[str, Any]],
        config: Optional[RunnableConfig] = None,
    ) -> DocumentState:
        """Transform documents using the configured transformer.

        Args:
            input_data: Document state or raw documents
            config: Optional runnable configuration

        Returns:
            DocumentState with transformed documents and metadata
        """
        start_time = time.time()

        try:
            # Normalize input to DocumentState
            if isinstance(input_data, DocumentState):
                # Already document state
                document_state = input_data
                documents_to_transform = document_state.raw_documents or []
            elif isinstance(input_data, list):
                # List of raw documents
                document_state = DocumentState(raw_documents=input_data)
                documents_to_transform = input_data
            elif isinstance(input_data, dict):
                # Dictionary input
                document_state = DocumentState.model_validate(input_data)
                documents_to_transform = document_state.raw_documents or []
            else:
                raise ValueError(f"Invalid input type: {type(input_data)}")

            if not documents_to_transform:
                # No documents to transform, return as-is
                document_state.processing_stage = "transform_skipped"
                return document_state

            # Create the actual transformer
            transformer = self._create_transformer()

            # Transform documents and maintain relationships
            transformed_raw_documents = []
            transformed_processed_documents = []

            for doc_index, document in enumerate(documents_to_transform):
                # Transform the document
                transformed_docs = transformer.transform_documents([document])

                for transform_index, transformed_doc in enumerate(transformed_docs):
                    # Generate IDs for transformation tracking
                    original_doc_id = (
                        document.metadata.get("document_id")
                        or f"doc_{doc_index}_{int(start_time)}"
                    )
                    transform_id = f"{original_doc_id}_transform_{transform_index}"

                    # Add transformation metadata
                    enhanced_metadata = {
                        **transformed_doc.metadata,
                        # Document identity and relationships
                        "document_id": transform_id,
                        "original_document_id": original_doc_id,
                        "is_transformed": True,
                        "transformation_index": transform_index,
                        # Preserve hierarchy if it exists
                        "parent_document_id": document.metadata.get(
                            "parent_document_id"
                        ),
                        "is_child_document": document.metadata.get(
                            "is_child_document", False
                        ),
                        "document_hierarchy_level": document.metadata.get(
                            "document_hierarchy_level", 0
                        ),
                        # Transformation details
                        "transformer_type": self.config.transformer_type.value,
                        "transformer_engine": "DocumentTransformerEngine",
                        "transformation_timestamp": start_time,
                        # Original document information
                        "original_document_metadata": {
                            "original_length": len(document.page_content),
                            "original_document_type": document.metadata.get(
                                "document_type", "unknown"
                            ),
                            "was_split": document.metadata.get("is_split", False),
                            "splitter_type": document.metadata.get("splitter_type"),
                        },
                        # Transformation characteristics
                        "transformed_length": len(transformed_doc.page_content),
                        "length_change": len(transformed_doc.page_content)
                        - len(document.page_content),
                        "transformation_config": {
                            "transformer_type": self.config.transformer_type.value,
                            "ignore_links": self.config.ignore_links,
                            "ignore_images": self.config.ignore_images,
                            "target_language": self.config.target_language,
                        },
                    }

                    # Create enhanced transformed document
                    enhanced_transformed_doc = Document(
                        page_content=transformed_doc.page_content,
                        metadata=enhanced_metadata,
                    )
                    transformed_raw_documents.append(enhanced_transformed_doc)

                    # Create processed document
                    processed_doc = ProcessedDocument(
                        content=transformed_doc.page_content,
                        metadata=enhanced_metadata,
                        source_type=document_state.source_type,
                        loader_name=f"transformer_{self.config.transformer_type.value}",
                        character_count=len(transformed_doc.page_content),
                        word_count=len(transformed_doc.page_content.split()),
                        chunk_count=1,
                        chunks=[enhanced_transformed_doc],
                        format=None,  # Will be determined from metadata
                        processing_time=0.0,  # Individual transformation time
                    )
                    transformed_processed_documents.append(processed_doc)

            operation_time = time.time() - start_time

            # Update document state with transformed results
            document_state.raw_documents = transformed_raw_documents
            document_state.documents = transformed_processed_documents
            document_state.total_documents = len(transformed_raw_documents)
            document_state.successful_documents = len(transformed_raw_documents)
            document_state.processing_stage = "transform_completed"

            # Add transformation metadata to workflow metadata
            document_state.workflow_metadata.update(
                {
                    "transformer_config": {
                        "transformer_type": self.config.transformer_type.value,
                        "ignore_links": self.config.ignore_links,
                        "ignore_images": self.config.ignore_images,
                        "target_language": self.config.target_language,
                        "preserve_hierarchy": self.config.preserve_hierarchy,
                    },
                    "transformation_operation_time": operation_time,
                    "total_transformed_documents": len(transformed_raw_documents),
                    "original_documents_count": len(documents_to_transform),
                }
            )

            return document_state

        except Exception as e:
            operation_time = time.time() - start_time

            # Create error document state
            if "document_state" not in locals():
                document_state = DocumentState()

            document_state.processing_stage = "transform_failed"
            document_state.errors.append(
                {
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "stage": "transformation",
                    "timestamp": start_time,
                }
            )
            document_state.workflow_metadata.update(
                {
                    "transformer_error": {
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
        """Asynchronously transform documents.

        Args:
            input_data: Document state or raw documents
            config: Optional runnable configuration

        Returns:
            DocumentState with transformed documents and metadata
        """
        # For now, run synchronously in thread pool
        # TODO: Implement true async processing if needed
        import asyncio

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.invoke, input_data, config)

    def _create_transformer(self):
        """Create the appropriate langchain transformer based on configuration.

        Returns:
            Configured langchain document transformer instance
        """
        transformer_type = self.config.transformer_type

        try:
            if transformer_type == DocTransformerType.HTML_TO_TEXT:
                from langchain_community.document_transformers import (
                    Html2TextTransformer,
                )

                return Html2TextTransformer(
                    ignore_links=self.config.ignore_links,
                    ignore_images=self.config.ignore_images,
                )

            elif transformer_type == DocTransformerType.HTML_TO_MARKDOWN:
                from langchain_community.document_transformers import (
                    MarkdownifyTransformer,
                )

                return MarkdownifyTransformer(
                    heading_style=self.config.heading_style,
                    autolinks=self.config.autolinks,
                )

            elif transformer_type == DocTransformerType.BEAUTIFUL_SOUP:
                from langchain_community.document_transformers import (
                    BeautifulSoupTransformer,
                )

                return BeautifulSoupTransformer()

            elif transformer_type == DocTransformerType.LONG_CONTEXT_REORDER:
                from langchain_community.document_transformers import LongContextReorder

                return LongContextReorder()

            elif transformer_type == DocTransformerType.EMBEDDINGS_REDUNDANT_FILTER:
                from langchain_community.document_transformers import (
                    EmbeddingsRedundantFilter,
                )

                if self.config.embeddings_model is None:
                    raise ValueError(
                        "Embeddings model is required for EmbeddingsRedundantFilter"
                    )
                return EmbeddingsRedundantFilter(
                    embeddings=self.config.embeddings_model,
                    similarity_threshold=self.config.similarity_threshold,
                )

            elif transformer_type == DocTransformerType.EMBEDDINGS_CLUSTERING_FILTER:
                from langchain_community.document_transformers import (
                    EmbeddingsClusteringFilter,
                )

                if self.config.embeddings_model is None:
                    raise ValueError(
                        "Embeddings model is required for EmbeddingsClusteringFilter"
                    )
                return EmbeddingsClusteringFilter(
                    embeddings=self.config.embeddings_model
                )

            elif transformer_type == DocTransformerType.GOOGLE_TRANSLATE:
                from langchain_community.document_transformers import (
                    GoogleTranslateTransformer,
                )

                return GoogleTranslateTransformer(
                    target_language=self.config.target_language
                )

            elif transformer_type == DocTransformerType.OPENAI_METADATA_TAGGER:
                from langchain_community.document_transformers import (
                    OpenAIMetadataTagger,
                )

                return OpenAIMetadataTagger()

            else:
                # Default to HTML to text transformer
                from langchain_community.document_transformers import (
                    Html2TextTransformer,
                )

                return Html2TextTransformer()

        except ImportError as e:
            raise ValueError(
                f"Required package not installed for {transformer_type}: {e}"
            )
        except Exception as e:
            raise ValueError(f"Failed to create transformer: {e}")

    @staticmethod
    def get_transformed_docs(
        document_state: DocumentState, original_id: str
    ) -> List[Document]:
        """Get all transformed documents for a given original document ID.

        Args:
            document_state: Document state containing transformed documents
            original_id: Original document ID to find transforms for

        Returns:
            List of transformed documents
        """
        return [
            doc
            for doc in document_state.raw_documents
            if doc.metadata.get("original_document_id") == original_id
        ]

    @staticmethod
    def get_original_doc(
        document_state: DocumentState, transform_id: str
    ) -> Optional[Document]:
        """Get original document for a given transformed document ID.

        Args:
            document_state: Document state containing documents
            transform_id: Transformed document ID to find original for

        Returns:
            Original document if found, None otherwise
        """
        # Find the transformed document first
        transformed_doc = None
        for doc in document_state.raw_documents:
            if doc.metadata.get("document_id") == transform_id:
                transformed_doc = doc
                break

        if not transformed_doc:
            return None

        original_id = transformed_doc.metadata.get("original_document_id")
        if not original_id:
            return None

        # Find original document (might be in workflow metadata or previous states)
        # For now, return None as original might not be in current state
        return None

    @staticmethod
    def build_transformation_tree(document_state: DocumentState) -> Dict[str, Any]:
        """Build a tree structure showing document transformation relationships.

        Args:
            document_state: Document state containing documents

        Returns:
            Dictionary representing the transformation tree structure
        """
        tree = {}

        # Group documents by transformation status
        transformed_docs = []
        original_docs = []

        for doc in document_state.raw_documents:
            if doc.metadata.get("is_transformed"):
                transformed_docs.append(doc)
            else:
                original_docs.append(doc)

        # Build tree structure
        for doc in document_state.raw_documents:
            doc_id = doc.metadata.get("document_id", "unknown")
            original_id = doc.metadata.get("original_document_id")
            is_transformed = doc.metadata.get("is_transformed", False)

            doc_info = {
                "document_id": doc_id,
                "content_preview": (
                    doc.page_content[:100] + "..."
                    if len(doc.page_content) > 100
                    else doc.page_content
                ),
                "is_transformed": is_transformed,
                "transformer_type": doc.metadata.get("transformer_type"),
                "document_length": len(doc.page_content),
                "transformations": [],
            }

            if original_id and original_id in tree:
                # Add as transformation of original
                tree[original_id]["transformations"].append(doc_info)
            else:
                # Root level document (original or orphaned transform)
                tree[doc_id] = doc_info

        return tree


# Factory functions for common transformations
def create_html_to_text_transformer(
    ignore_links: bool = True,
    ignore_images: bool = True,
) -> DocumentTransformerEngine:
    """Create an HTML to text transformer engine.

    Args:
        ignore_links: Whether to ignore links in HTML
        ignore_images: Whether to ignore images in HTML

    Returns:
        DocumentTransformerEngine configured for HTML to text transformation
    """
    config = DocTransformerConfig(
        transformer_type=DocTransformerType.HTML_TO_TEXT,
        ignore_links=ignore_links,
        ignore_images=ignore_images,
    )
    return DocumentTransformerEngine(config=config)


def create_html_to_markdown_transformer(
    heading_style: str = "ATX",
    autolinks: bool = True,
) -> DocumentTransformerEngine:
    """Create an HTML to markdown transformer engine.

    Args:
        heading_style: Heading style for markdown conversion
        autolinks: Whether to use automatic link style

    Returns:
        DocumentTransformerEngine configured for HTML to markdown transformation
    """
    config = DocTransformerConfig(
        transformer_type=DocTransformerType.HTML_TO_MARKDOWN,
        heading_style=heading_style,
        autolinks=autolinks,
    )
    return DocumentTransformerEngine(config=config)


def create_translation_transformer(
    target_language: str = "en",
) -> DocumentTransformerEngine:
    """Create a document translation transformer engine.

    Args:
        target_language: Target language code for translation

    Returns:
        DocumentTransformerEngine configured for translation
    """
    config = DocTransformerConfig(
        transformer_type=DocTransformerType.GOOGLE_TRANSLATE,
        target_language=target_language,
    )
    return DocumentTransformerEngine(config=config)


def create_deduplication_transformer(
    embeddings_model: Any,
    similarity_threshold: float = 0.95,
) -> DocumentTransformerEngine:
    """Create a document deduplication transformer engine.

    Args:
        embeddings_model: Embeddings model for similarity calculation
        similarity_threshold: Threshold for considering documents similar

    Returns:
        DocumentTransformerEngine configured for deduplication
    """
    config = DocTransformerConfig(
        transformer_type=DocTransformerType.EMBEDDINGS_REDUNDANT_FILTER,
        embeddings_model=embeddings_model,
        similarity_threshold=similarity_threshold,
    )
    return DocumentTransformerEngine(config=config)
