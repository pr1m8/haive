"""Document processor adapters for transformers and splitters.

This module provides adapters and factories for using the core engine's document
transformers and splitters with the DocumentAgent and DocumentState classes.
"""

from __future__ import annotations

import importlib.util
import logging
from typing import Any, cast

# Import core document models
from langchain_core.documents import Document as LCDocument


# Import document splitters from core engine
try:
    # Check if we can import the core splitters
    has_splitters = (
        importlib.util.find_spec("haive.core.engine.document.splitters") is not None
    )

    if has_splitters:
        from langchain_text_splitters import (
            CharacterTextSplitter,
            HTMLHeaderTextSplitter,
            MarkdownTextSplitter,
            NLTKTextSplitter,
            RecursiveCharacterTextSplitter,
            SpacyTextSplitter,
            TokenTextSplitter,
        )

        from haive.core.engine.document.splitters.base import (
            DocSplitterType,
            TextSplitter,
        )
        from haive.core.engine.document.splitters.engine import DocSplitterEngine

        SPLITTERS_AVAILABLE = True
    else:
        raise ImportError("Core splitters module not found")
except ImportError:
    # Fall back to a simplified splitter interface if core splitters aren't available
    TextSplitter = object
    DocSplitterType = object
    DocSplitterEngine = object
    RecursiveCharacterTextSplitter = TokenTextSplitter = CharacterTextSplitter = object
    MarkdownTextSplitter = HTMLHeaderTextSplitter = NLTKTextSplitter = (
        SpacyTextSplitter
    ) = object

    SPLITTERS_AVAILABLE = False

# Import document transformers from core engine
try:
    # Check if we can import the core transformers
    has_transformers = (
        importlib.util.find_spec("haive.core.engine.document.transformers") is not None
    )

    if has_transformers:
        from haive.core.engine.document.transformers.base import (
            DocTransformer,
            DocTransformerType,
        )
        from haive.core.engine.document.transformers.engine import DocTransformerEngine
        from haive.core.engine.document.transformers.html import (
            HtmlToMarkdownTransformer,
            HtmlToTextTransformer,
        )
        from haive.core.engine.document.transformers.utils import (
            BeautifulSoupTransformer,
        )

        TRANSFORMERS_AVAILABLE = True
    else:
        raise ImportError("Core transformers module not found")
except ImportError:
    # Fall back to placeholder classes if transformers aren't available
    DocTransformer = object
    DocTransformerType = object
    DocTransformerEngine = object
    HtmlToTextTransformer = HtmlToMarkdownTransformer = BeautifulSoupTransformer = (
        object
    )

    TRANSFORMERS_AVAILABLE = False

# Import our document state classes
from .document_models import (
    ChunkingOptions,
    ChunkingStrategy,
    Document,
    DocumentChunk,
    DocumentFormat,
)


logger = logging.getLogger(__name__)


# ===== Document Adapters =====


def document_to_langchain(doc: Document) -> LCDocument:
    """Convert a Document to a LangChain Document.

    Args:
        doc: The Document to convert.

    Returns:
        A LangChain Document.
    """
    return LCDocument(
        page_content=doc.content,
        metadata={
            "source": doc.source_path,
            "document_id": doc.document_id,
            "source_type": doc.source_type.value if doc.source_type else "unknown",
            "format": doc.format.value if doc.format else "unknown",
            **doc.metadata,
        },
    )


def langchain_to_document(lc_doc: LCDocument, doc: Document) -> Document:
    """Update a Document with content from a LangChain Document.

    Args:
        lc_doc: The LangChain Document to get content from.
        doc: The Document to update.

    Returns:
        The updated Document.
    """
    # Update content
    doc.content = lc_doc.page_content

    # Update metadata (excluding fields that were added during conversion)
    for key, value in lc_doc.metadata.items():
        if key not in ["source", "document_id", "source_type", "format"]:
            doc.metadata[key] = value

    return doc


def langchain_to_document_chunk(
    lc_doc: LCDocument, parent_doc: Document, chunk_index: int
) -> DocumentChunk:
    """Convert a LangChain Document to a DocumentChunk.

    Args:
        lc_doc: The LangChain Document to convert.
        parent_doc: The parent Document.
        chunk_index: The index of this chunk.

    Returns:
        A DocumentChunk.
    """
    # Extract metadata, removing fields that were added during conversion
    metadata = lc_doc.metadata.copy()
    for field in ["source", "document_id", "source_type", "format"]:
        if field in metadata:
            del metadata[field]

    # Add chunk-specific metadata
    metadata["chunk_index"] = chunk_index

    return DocumentChunk(
        content=lc_doc.page_content,
        document_id=parent_doc.document_id,
        chunk_index=chunk_index,
        metadata=metadata,
    )


def documents_to_langchain_list(docs: list[Document]) -> list[LCDocument]:
    """Convert a list of Documents to a list of LangChain Documents.

    Args:
        docs: The Documents to convert.

    Returns:
        A list of LangChain Documents.
    """
    return [document_to_langchain(doc) for doc in docs]


# ===== Splitter Factory =====


class SplitterFactory:
    """Factory for creating text splitters based on chunking strategy and document format."""

    @staticmethod
    def get_splitter_type(
        strategy: ChunkingStrategy, document_format: DocumentFormat | None = None
    ) -> DocSplitterType | str | None:
        """Get the appropriate splitter type for the given strategy and format.

        Args:
            strategy: The chunking strategy to use.
            document_format: Optional document format for format-specific splitters.

        Returns:
            A DocSplitterType or None if not available.
        """
        if not SPLITTERS_AVAILABLE:
            return None

        # Map chunking strategy to splitter type
        strategy_to_type = {
            ChunkingStrategy.FIXED_SIZE: DocSplitterType.CHARACTER,
            ChunkingStrategy.RECURSIVE: DocSplitterType.RECURSIVE_CHARACTER,
            ChunkingStrategy.PARAGRAPH: DocSplitterType.CHARACTER,  # Use character with \n\n separator
            ChunkingStrategy.SENTENCE: DocSplitterType.NLTK,
            ChunkingStrategy.SEMANTIC: DocSplitterType.SEMANTIC,
        }

        # Format-specific overrides
        if document_format == DocumentFormat.MARKDOWN:
            return DocSplitterType.MARKDOWN
        if document_format == DocumentFormat.HTML:
            return DocSplitterType.HTML_HEADER

        return strategy_to_type.get(strategy)

    @staticmethod
    def create_splitter(
        strategy: ChunkingStrategy,
        options: ChunkingOptions,
        document_format: DocumentFormat | None = None,
    ) -> TextSplitter | None:
        """Create a text splitter based on the chunking strategy and document format.

        This method uses the core engine's splitter system when available.

        Args:
            strategy: The chunking strategy to use.
            options: The chunking options.
            document_format: Optional document format for format-specific splitters.

        Returns:
            A TextSplitter instance, or None if splitters are not available.
        """
        if not SPLITTERS_AVAILABLE:
            logger.warning("Core document splitters are not available.")
            return None

        # Get the appropriate splitter type
        splitter_type = SplitterFactory.get_splitter_type(strategy, document_format)
        if not splitter_type:
            logger.warning(f"No splitter type available for strategy {strategy}.")
            return None

        # Common parameters for all splitters
        chunk_size = options.chunk_size
        chunk_overlap = options.chunk_overlap

        # Create splitter configuration
        kwargs = {
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
        }

        # Add strategy-specific parameters
        if strategy == ChunkingStrategy.PARAGRAPH:
            kwargs["separator"] = "\n\n"
        elif strategy == ChunkingStrategy.RECURSIVE:
            kwargs["separators"] = options.custom_separators or ["\n\n", "\n", " ", ""]

        # Create the splitter using the engine
        try:
            return cast(TextSplitter, DocSplitterEngine.create(splitter_type, **kwargs))
        except Exception as e:
            logger.warning(f"Failed to create splitter of type {splitter_type}: {e}")

            # Fallback to basic implementations
            if strategy == ChunkingStrategy.FIXED_SIZE:
                return CharacterTextSplitter(
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                    separator="\n\n" if options.keep_separator else "",
                )
            if strategy == ChunkingStrategy.RECURSIVE:
                separators = options.custom_separators or ["\n\n", "\n", " ", ""]
                return RecursiveCharacterTextSplitter(
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                    separators=separators,
                )
            if strategy == ChunkingStrategy.PARAGRAPH:
                return CharacterTextSplitter(
                    chunk_size=chunk_size, chunk_overlap=chunk_overlap, separator="\n\n"
                )
            # Default fallback
            return RecursiveCharacterTextSplitter(
                chunk_size=chunk_size, chunk_overlap=chunk_overlap
            )


# ===== Transformer Factory =====


class TransformerFactory:
    """Factory for creating document transformers based on document format."""

    @staticmethod
    def get_transformer_type(
        document_format: DocumentFormat,
    ) -> DocTransformerType | None:
        """Get the appropriate transformer type for the given document format.

        Args:
            document_format: The format of the document.

        Returns:
            A DocTransformerType or None if not available.
        """
        if not TRANSFORMERS_AVAILABLE:
            return None

        # Map document format to transformer type
        format_to_transformer = {
            DocumentFormat.HTML: DocTransformerType.HTML_TO_TEXT,
            DocumentFormat.MARKDOWN: None,  # No transformation needed
        }

        return format_to_transformer.get(document_format)

    @staticmethod
    def create_transformer(
        document_format: DocumentFormat, **kwargs: Any
    ) -> DocTransformer | None:
        """Create a document transformer based on the document format.

        This method uses the core engine's transformer system when available.

        Args:
            document_format: The format of the document.
            **kwargs: Additional arguments for the transformer.

        Returns:
            A DocTransformer instance, or None if transformers are not available.
        """
        if not TRANSFORMERS_AVAILABLE:
            logger.warning("Core document transformers are not available.")
            return None

        # Get the appropriate transformer type
        transformer_type = TransformerFactory.get_transformer_type(document_format)
        if not transformer_type:
            return None

        # Create the transformer using the engine
        try:
            return cast(
                DocTransformer, DocTransformerEngine.create(transformer_type, **kwargs)
            )
        except Exception as e:
            logger.warning(
                f"Failed to create transformer of type {transformer_type}: {e}"
            )

            # Fallback to basic implementations
            if document_format == DocumentFormat.HTML:
                return HtmlToTextTransformer()

            return None


# ===== Processing Functions =====


def process_document(doc: Document) -> Document:
    """Process a document using appropriate transformers and splitters.

    This is a convenience function that combines transform_document and split_document.

    Args:
        doc: The document to process.

    Returns:
        The processed document with chunks.
    """
    # First transform the document
    transformed_doc = transform_document(doc)

    # Then split it (if chunking options are provided)
    if (
        hasattr(doc, "chunking_options")
        and doc.chunking_options.strategy != ChunkingStrategy.NONE
    ):
        chunks = split_document(
            transformed_doc, doc.chunking_options.strategy, doc.chunking_options
        )
        transformed_doc.chunks = chunks

    return transformed_doc


def split_document(
    doc: Document, strategy: ChunkingStrategy, options: ChunkingOptions
) -> list[DocumentChunk]:
    """Split a document into chunks using the appropriate splitter.

    Args:
        doc: The document to split.
        strategy: The chunking strategy to use.
        options: The chunking options.

    Returns:
        A list of DocumentChunks.
    """
    # If strategy is NONE, return empty list
    if strategy == ChunkingStrategy.NONE:
        return []

    # If splitters aren't available, use a simplified approach
    if not SPLITTERS_AVAILABLE:
        logger.warning(
            "Using simplified document splitting since core splitters are not available."
        )
        return _simple_split_document(doc, strategy, options)

    # Get the appropriate splitter
    splitter = SplitterFactory.create_splitter(
        strategy=strategy, options=options, document_format=doc.format
    )

    if not splitter:
        logger.warning(
            f"No splitter available for strategy {strategy}. Using simplified splitting."
        )
        return _simple_split_document(doc, strategy, options)

    # Convert to LangChain document
    lc_doc = document_to_langchain(doc)

    # Split the document
    try:
        split_docs = splitter.split_documents([lc_doc])

        # Convert back to DocumentChunks
        chunks = []
        for i, split_doc in enumerate(split_docs):
            chunks.append(langchain_to_document_chunk(split_doc, doc, i))

        return chunks
    except Exception as e:
        logger.warning(
            f"Error splitting document with {splitter.__class__.__name__}: {e}. Using simplified splitting."
        )
        return _simple_split_document(doc, strategy, options)


def transform_document(doc: Document) -> Document:
    """Apply appropriate transformations to a document based on its format.

    Args:
        doc: The document to transform.

    Returns:
        The transformed document.
    """
    # Check if we need transformation
    if doc.format not in [DocumentFormat.HTML, DocumentFormat.MARKDOWN]:
        return doc

    # If transformers aren't available, return original document
    if not TRANSFORMERS_AVAILABLE:
        return doc

    # Get the appropriate transformer
    transformer = TransformerFactory.create_transformer(doc.format)

    if not transformer:
        return doc

    # Convert to LangChain document
    lc_doc = document_to_langchain(doc)

    # Transform the document
    try:
        transformed_docs = transformer.transform_documents([lc_doc])
        if transformed_docs:
            # Update the document with transformed content
            return langchain_to_document(transformed_docs[0], doc)
    except Exception as e:
        logger.warning(
            f"Error transforming document with {transformer.__class__.__name__}: {e}"
        )

    return doc


# ===== Simplified Implementations =====


def _simple_split_document(
    doc: Document, strategy: ChunkingStrategy, options: ChunkingOptions
) -> list[DocumentChunk]:
    """Simple document splitting implementation when core splitters aren't available.

    Args:
        doc: The document to split.
        strategy: The chunking strategy to use.
        options: The chunking options.

    Returns:
        A list of DocumentChunks.
    """
    content = doc.content
    chunks = []

    if (
        strategy == ChunkingStrategy.FIXED_SIZE
        or strategy == ChunkingStrategy.RECURSIVE
    ):
        # Fixed size chunking
        chunk_size = options.chunk_size
        chunk_overlap = options.chunk_overlap

        # Simple chunking implementation
        start = 0
        chunk_index = 0

        while start < len(content):
            # Calculate end position with overlap
            end = min(start + chunk_size, len(content))

            # Extract chunk content
            chunk_content = content[start:end]

            # Create chunk metadata
            chunk_metadata = {
                "chunk_index": chunk_index,
                "start": start,
                "end": end,
                "source_path": doc.source_path,
            }

            # Add metadata from document if scope includes document
            if options.metadata_scope in ["all", "document"]:
                for key, value in doc.metadata.items():
                    if key not in chunk_metadata:
                        chunk_metadata[key] = value

            # Create chunk
            chunks.append(
                DocumentChunk(
                    content=chunk_content,
                    document_id=doc.document_id,
                    chunk_index=chunk_index,
                    metadata=chunk_metadata,
                )
            )

            # Move to next chunk position, accounting for overlap
            start = end - chunk_overlap if end < len(content) else len(content)
            chunk_index += 1

    elif strategy == ChunkingStrategy.PARAGRAPH:
        # Paragraph chunking
        paragraphs = content.split("\n\n")

        for i, paragraph in enumerate(paragraphs):
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            # Create chunk metadata
            chunk_metadata = {
                "chunk_index": i,
                "paragraph_index": i,
                "source_path": doc.source_path,
            }

            # Add metadata from document if scope includes document
            if options.metadata_scope in ["all", "document"]:
                for key, value in doc.metadata.items():
                    if key not in chunk_metadata:
                        chunk_metadata[key] = value

            # Create chunk
            chunks.append(
                DocumentChunk(
                    content=paragraph,
                    document_id=doc.document_id,
                    chunk_index=i,
                    metadata=chunk_metadata,
                )
            )

    elif strategy == ChunkingStrategy.SENTENCE:
        # Sentence chunking - simplified
        sentence_endings = [". ", "! ", "? ", ".\n", "!\n", "?\n"]
        current_sentence = ""
        sentences = []

        for char in content:
            current_sentence += char
            for ending in sentence_endings:
                if current_sentence.endswith(ending):
                    sentences.append(current_sentence.strip())
                    current_sentence = ""
                    break

        if current_sentence.strip():
            sentences.append(current_sentence.strip())

        for i, sentence in enumerate(sentences):
            if not sentence:
                continue

            # Create chunk metadata
            chunk_metadata = {
                "chunk_index": i,
                "sentence_index": i,
                "source_path": doc.source_path,
            }

            # Add metadata from document
            if options.metadata_scope in ["all", "document"]:
                for key, value in doc.metadata.items():
                    if key not in chunk_metadata:
                        chunk_metadata[key] = value

            # Create chunk
            chunks.append(
                DocumentChunk(
                    content=sentence,
                    document_id=doc.document_id,
                    chunk_index=i,
                    metadata=chunk_metadata,
                )
            )

    return chunks
