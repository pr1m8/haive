"""Document Processing Components.

This module provides document processing capabilities including chunking and
content transformation that integrate with the DocumentEngine.

The processors handle:
- Content normalization
- Document chunking strategies
- Metadata extraction
- Format conversion
"""

import logging
from typing import Any, Dict, List, Optional

from langchain_core.documents import Document as LCDocument

from haive.core.engine.document.config import (
    ChunkingStrategy,
    DocumentChunk,
    DocumentFormat,
    ProcessedDocument,
)

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Base class for document processing operations."""

    def __init__(self, **kwargs):
        """Initialize the processor."""
        self.config = kwargs

    def process(self, document: LCDocument) -> ProcessedDocument:
        """Process a document.

        Args:
            document: Document to process

        Returns:
            Processed document
        """
        raise NotImplementedError("Subclasses must implement process method")


class ChunkingProcessor(DocumentProcessor):
    """Processor for chunking documents into smaller pieces."""

    def __init__(
        self,
        chunking_strategy: ChunkingStrategy = ChunkingStrategy.RECURSIVE,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        **kwargs,
    ):
        """Initialize the chunking processor.

        Args:
            chunking_strategy: Strategy for chunking
            chunk_size: Size of chunks in characters
            chunk_overlap: Overlap between chunks
            **kwargs: Additional configuration
        """
        super().__init__(**kwargs)
        self.chunking_strategy = chunking_strategy
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(
        self,
        text: str,
        strategy: ChunkingStrategy,
        chunk_size: int,
        chunk_overlap: int,
        metadata: Dict[str, Any],
    ) -> List[DocumentChunk]:
        """Chunk text according to the specified strategy.

        Args:
            text: Text to chunk
            strategy: Chunking strategy
            chunk_size: Size of chunks
            chunk_overlap: Overlap between chunks
            metadata: Base metadata for chunks

        Returns:
            List of document chunks
        """
        if strategy == ChunkingStrategy.NONE:
            return []

        chunks = []

        if strategy == ChunkingStrategy.FIXED_SIZE:
            chunks = self._chunk_fixed_size(text, chunk_size, chunk_overlap)
        elif strategy == ChunkingStrategy.PARAGRAPH:
            chunks = self._chunk_by_paragraph(text, chunk_size)
        elif strategy == ChunkingStrategy.SENTENCE:
            chunks = self._chunk_by_sentence(text, chunk_size)
        elif strategy == ChunkingStrategy.RECURSIVE:
            chunks = self._chunk_recursive(text, chunk_size, chunk_overlap)
        elif strategy == ChunkingStrategy.SEMANTIC:
            chunks = self._chunk_semantic(text, chunk_size)
        else:
            # Default to fixed size
            chunks = self._chunk_fixed_size(text, chunk_size, chunk_overlap)

        # Convert to DocumentChunk objects
        doc_chunks = []
        for i, chunk_text in enumerate(chunks):
            chunk_metadata = metadata.copy()
            chunk_metadata.update(
                {
                    "chunk_index": i,
                    "chunk_strategy": strategy.value,
                    "chunk_size": len(chunk_text),
                }
            )

            doc_chunks.append(
                DocumentChunk(
                    content=chunk_text,
                    metadata=chunk_metadata,
                    chunk_index=i,
                    chunk_id=f"{metadata.get('source', 'unknown')}_{i}",
                )
            )

        return doc_chunks

    def _chunk_fixed_size(self, content: str, size: int, overlap: int) -> List[str]:
        """Chunk content into fixed-size pieces."""
        chunks = []
        start = 0

        while start < len(content):
            end = start + size
            chunk = content[start:end]
            chunks.append(chunk)

            if end >= len(content):
                break

            start = end - overlap

        return chunks

    def _chunk_by_paragraph(self, content: str, max_size: int) -> List[str]:
        """Chunk content by paragraphs."""
        paragraphs = content.split("\n\n")
        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) + 2 <= max_size:
                if current_chunk:
                    current_chunk += "\n\n"
                current_chunk += paragraph
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = paragraph

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def _chunk_by_sentence(self, content: str, max_size: int) -> List[str]:
        """Chunk content by sentences."""
        # Simple sentence splitting
        import re

        sentences = re.split(r"[.!?]+", content)

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            if len(current_chunk) + len(sentence) + 1 <= max_size:
                if current_chunk:
                    current_chunk += " "
                current_chunk += sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def _chunk_recursive(self, content: str, size: int, overlap: int) -> List[str]:
        """Chunk content recursively using multiple separators."""
        separators = ["\n\n", "\n", " ", ""]

        def split_recursive(text: str, separators: List[str]) -> List[str]:
            if len(text) <= size:
                return [text]

            if not separators:
                # Fall back to character splitting
                return self._chunk_fixed_size(text, size, overlap)

            separator = separators[0]
            remaining_separators = separators[1:]

            if separator not in text:
                return split_recursive(text, remaining_separators)

            splits = text.split(separator)
            chunks = []
            current_chunk = ""

            for split in splits:
                test_chunk = (
                    current_chunk + (separator if current_chunk else "") + split
                )

                if len(test_chunk) <= size:
                    current_chunk = test_chunk
                else:
                    if current_chunk:
                        chunks.append(current_chunk)

                    if len(split) > size:
                        # Split is too large, recursively split it
                        chunks.extend(split_recursive(split, remaining_separators))
                        current_chunk = ""
                    else:
                        current_chunk = split

            if current_chunk:
                chunks.append(current_chunk)

            return chunks

        return split_recursive(content, separators)

    def _chunk_semantic(self, content: str, size: int) -> List[str]:
        """Chunk content semantically (placeholder implementation)."""
        # This would require more sophisticated NLP
        # For now, fall back to paragraph chunking
        return self._chunk_by_paragraph(content, size)


class ContentNormalizer(DocumentProcessor):
    """Processor for normalizing document content."""

    def __init__(
        self,
        normalize_whitespace: bool = True,
        remove_extra_newlines: bool = True,
        strip_content: bool = True,
        **kwargs,
    ):
        """Initialize the content normalizer.

        Args:
            normalize_whitespace: Whether to normalize whitespace
            remove_extra_newlines: Whether to remove extra newlines
            strip_content: Whether to strip leading/trailing whitespace
            **kwargs: Additional configuration
        """
        super().__init__(**kwargs)
        self.normalize_whitespace = normalize_whitespace
        self.remove_extra_newlines = remove_extra_newlines
        self.strip_content = strip_content

    def normalize_content(self, content: str) -> str:
        """Normalize document content.

        Args:
            content: Content to normalize

        Returns:
            Normalized content
        """
        if not content:
            return content

        normalized = content

        # Strip leading/trailing whitespace
        if self.strip_content:
            normalized = normalized.strip()

        # Normalize whitespace
        if self.normalize_whitespace:
            import re

            normalized = re.sub(r"\s+", " ", normalized)

        # Remove extra newlines
        if self.remove_extra_newlines:
            import re

            normalized = re.sub(r"\n\s*\n", "\n\n", normalized)

        return normalized


class FormatDetector(DocumentProcessor):
    """Processor for detecting document formats."""

    def detect_format(self, content: str, metadata: Dict[str, Any]) -> DocumentFormat:
        """Detect document format from content and metadata.

        Args:
            content: Document content
            metadata: Document metadata

        Returns:
            Detected document format
        """
        # Check metadata first
        if "format" in metadata:
            try:
                return DocumentFormat(metadata["format"].lower())
            except ValueError:
                pass

        # Check file extension
        source = metadata.get("source", "")
        if source:
            from pathlib import Path

            ext = Path(source).suffix.lower()
            format_map = {
                ".pdf": DocumentFormat.PDF,
                ".docx": DocumentFormat.DOCX,
                ".txt": DocumentFormat.TXT,
                ".html": DocumentFormat.HTML,
                ".md": DocumentFormat.MARKDOWN,
                ".json": DocumentFormat.JSON,
                ".csv": DocumentFormat.CSV,
                ".xml": DocumentFormat.XML,
            }
            if ext in format_map:
                return format_map[ext]

        # Content-based detection
        if content:
            content_lower = content.lower().strip()
            if content_lower.startswith("<!doctype html") or content_lower.startswith(
                "<html"
            ):
                return DocumentFormat.HTML
            elif content_lower.startswith("{") and content_lower.endswith("}"):
                return DocumentFormat.JSON
            elif content_lower.startswith("<?xml"):
                return DocumentFormat.XML

        return DocumentFormat.UNKNOWN


class MetadataExtractor(DocumentProcessor):
    """Processor for extracting metadata from documents."""

    def extract_metadata(
        self, content: str, existing_metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract additional metadata from document content.

        Args:
            content: Document content
            existing_metadata: Existing metadata

        Returns:
            Enhanced metadata dictionary
        """
        metadata = existing_metadata.copy()

        # Add basic statistics
        metadata.update(
            {
                "character_count": len(content),
                "word_count": len(content.split()) if content else 0,
                "line_count": content.count("\n") + 1 if content else 0,
            }
        )

        # Extract language (basic heuristic)
        if content and len(content) > 50:
            # Very basic language detection based on character patterns
            ascii_ratio = sum(1 for c in content if ord(c) < 128) / len(content)
            if ascii_ratio > 0.95:
                metadata["estimated_language"] = "en"
            else:
                metadata["estimated_language"] = "unknown"

        return metadata


# Export processing components
__all__ = [
    "DocumentProcessor",
    "ChunkingProcessor",
    "ContentNormalizer",
    "FormatDetector",
    "MetadataExtractor",
]
