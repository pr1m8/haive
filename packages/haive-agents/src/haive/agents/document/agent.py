"""Document Agent for comprehensive document processing pipeline.

This module provides the DocumentAgent class which implements the full document processing
pipeline: FETCH -> LOAD -> TRANSFORM -> SPLIT -> ANNOTATE -> EMBED -> STORE -> RETRIEVE.

The agent leverages the Document Engine from haive-core to handle 97+ document types
and sources with advanced processing capabilities including chunking, metadata
extraction, and parallel processing.

Classes:
    DocumentAgent: Main agent for document processing pipeline
    DocumentProcessingResult: Structured result from document processing

Examples:
    Basic usage::

        from haive.agents.document import DocumentAgent
        from haive.core.engine.document import DocumentEngineConfig

        agent = DocumentAgent(name="doc_processor")
        result = agent.process_sources(["document.pdf"])
        print(f"Processed {result.total_documents} documents")

    Advanced configuration::

        config = DocumentEngineConfig(
            chunking_strategy=ChunkingStrategy.SEMANTIC,
            parallel_processing=True,
            max_workers=8
        )
        agent = DocumentAgent(name="enterprise_processor", engine=config)
        result = agent.process_directory("/path/to/documents")

See Also:
    - :class:`~haive.core.engine.document.DocumentEngine`: Core processing engine
    - :class:`~haive.agents.base.Agent`: Base agent class
"""

import logging
from typing import Any, Dict, List, Optional, Union

from haive.core.engine.document import DocumentEngine, DocumentEngineConfig
from haive.core.engine.document.config import (
    ChunkingStrategy,
    DocumentFormat,
    DocumentInput,
    DocumentOutput,
    DocumentSourceType,
    ProcessedDocument,
    ProcessingStrategy,
)
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langgraph.graph import END, START
from pydantic import BaseModel, Field, field_validator

from haive.agents.base.agent import Agent

logger = logging.getLogger(__name__)


class DocumentProcessingResult(BaseModel):
    """Comprehensive result of document processing pipeline."""

    # Pipeline Results
    fetched_sources: list[str] = Field(
        default_factory=list, description="Sources successfully fetched"
    )
    loaded_documents: list[dict[str, Any]] = Field(
        default_factory=list, description="Documents loaded from sources"
    )
    transformed_documents: list[dict[str, Any]] = Field(
        default_factory=list, description="Documents after transformation/normalization"
    )
    document_chunks: list[dict[str, Any]] = Field(
        default_factory=list, description="Document chunks created by splitting"
    )
    annotated_chunks: list[dict[str, Any]] = Field(
        default_factory=list, description="Chunks with extracted metadata annotations"
    )
    embedded_chunks: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Chunks with embeddings (if embedding enabled)",
    )
    stored_documents: list[str] = Field(
        default_factory=list,
        description="Document IDs stored in vector store (if storage enabled)",
    )

    # Pipeline Statistics
    total_sources: int = Field(default=0, description="Total sources processed")
    total_documents: int = Field(default=0, description="Total documents loaded")
    total_chunks: int = Field(default=0, description="Total chunks created")
    total_annotations: int = Field(default=0, description="Total annotations extracted")

    # Processing Metadata
    processing_time: float = Field(default=0.0, description="Total processing time")
    pipeline_strategy: str = Field(default="", description="Processing strategy used")
    chunking_strategy: str = Field(default="", description="Chunking strategy used")

    # Source Analysis
    source_types: dict[str, int] = Field(
        default_factory=dict, description="Count of each source type processed"
    )
    document_formats: dict[str, int] = Field(
        default_factory=dict, description="Count of each document format processed"
    )

    # Quality Metrics
    successful_sources: int = Field(
        default=0, description="Successfully processed sources"
    )
    failed_sources: int = Field(default=0, description="Failed source processing")
    processing_errors: list[str] = Field(
        default_factory=list, description="Errors encountered during processing"
    )

    # Content Analysis
    total_characters: int = Field(default=0, description="Total characters processed")
    total_words: int = Field(default=0, description="Total words processed")
    average_chunk_size: float = Field(default=0.0, description="Average chunk size")


class DocumentAgent(Agent):
    """Comprehensive Document Processing Agent.

    This agent implements the complete document processing pipeline for enterprise-grade
    document ingestion and analysis. It provides a unified interface for the full
    document lifecycle from source discovery to retrievable storage.

    ## Processing Pipeline:

    1. **FETCH**: Discover and validate document sources (files, URLs, databases, cloud)
    2. **LOAD**: Load documents using 97+ specialized loaders with auto-detection
    3. **TRANSFORM**: Normalize content, extract metadata, detect language/encoding
    4. **SPLIT**: Apply intelligent chunking strategies (recursive, semantic, paragraph)
    5. **ANNOTATE**: Extract and enrich metadata, apply content classification
    6. **EMBED**: Generate vector embeddings for semantic search (optional)
    7. **STORE**: Persist to vector databases and document stores (optional)
    8. **RETRIEVE**: Enable search and retrieval capabilities (optional)

    ## Key Features:

    - **Universal Source Support**: 97+ document sources including files, URLs, databases, cloud storage
    - **Intelligent Processing**: Auto-detection of source types and optimal processing strategies
    - **Parallel Processing**: Multi-threaded processing for high-throughput scenarios
    - **Advanced Chunking**: Multiple strategies including recursive, semantic, and paragraph-based
    - **Metadata Enrichment**: Comprehensive metadata extraction and annotation
    - **Error Resilience**: Graceful error handling with detailed reporting
    - **Extensible Pipeline**: Configurable stages for custom processing workflows

    ## Configuration Options:

    Args:
        engine: Document engine configuration for processing pipeline

        # Source Configuration
        source_types: List of allowed source types (files, URLs, databases, etc.)
        auto_detect_sources: Whether to auto-detect source types
        max_sources: Maximum number of sources to process

        # Processing Configuration
        processing_strategy: Processing strategy (simple, enhanced, parallel)
        parallel_processing: Enable parallel processing
        max_workers: Maximum worker threads for parallel processing

        # Chunking Configuration
        chunking_strategy: Strategy for document chunking
        chunk_size: Size of chunks in characters
        chunk_overlap: Overlap between consecutive chunks

        # Content Processing
        normalize_content: Whether to normalize content (whitespace, encoding)
        extract_metadata: Whether to extract document metadata
        detect_language: Whether to detect document language

        # Pipeline Stages (optional)
        enable_embedding: Whether to generate embeddings
        enable_storage: Whether to store in vector database
        enable_retrieval: Whether to enable retrieval capabilities

        # Error Handling
        raise_on_error: Whether to raise exceptions on errors
        skip_invalid: Whether to skip invalid documents

    ## Example Usage:

    ### Basic Document Processing:
    ```python
    from haive.agents.document import DocumentAgent
    from haive.core.engine.document import DocumentEngineConfig

    # Create agent for PDF processing
    agent = DocumentAgent(
        engine=DocumentEngineConfig(
            chunking_strategy=ChunkingStrategy.PARAGRAPH,
            chunk_size=1000,
            parallel_processing=True
        )
    )

    # Process a single document
    result = agent.invoke({
        "source": "document.pdf",
        "extract_metadata": True
    })
    ```

    ### Multi-Source Processing:
    ```python
    # Process multiple sources with different types
    agent = DocumentAgent.create_for_enterprise()

    result = agent.process_sources([
        "documents/reports/",  # Directory
        "https://example.com/api/docs",  # Web API
        "s3://bucket/documents/",  # Cloud storage
        "postgresql://db/documents"  # Database
    ])
    ```

    ### Custom Pipeline Configuration:
    ```python
    # Configure custom processing pipeline
    agent = DocumentAgent(
        processing_strategy=ProcessingStrategy.ENHANCED,
        chunking_strategy=ChunkingStrategy.SEMANTIC,
        chunk_size=1500,
        enable_embedding=True,
        enable_storage=True,
        normalize_content=True,
        detect_language=True
    )
    ```

    ## Document Source Types Supported:

    - **Files**: PDF, DOCX, TXT, HTML, MD, JSON, CSV, XML, YAML, and 50+ more
    - **Web**: HTTP/HTTPS URLs, APIs, web scraping, RSS feeds
    - **Cloud**: AWS S3, Google Cloud Storage, Azure Blob, Dropbox, Box
    - **Databases**: PostgreSQL, MySQL, MongoDB, Elasticsearch, and 15+ more
    - **Chat/Messaging**: Slack, Discord, WhatsApp, Telegram exports
    - **Knowledge Bases**: Notion, Confluence, Obsidian, Roam Research
    - **Version Control**: Git repositories, GitHub, GitLab
    - **Archives**: ZIP, TAR, 7Z with recursive extraction

    ## Processing Strategies:

    - **Simple**: Basic loading and chunking for development/testing
    - **Enhanced**: Full metadata extraction, content normalization, language detection
    - **Parallel**: Multi-threaded processing for high-throughput production use

    ## Chunking Strategies:

    - **None**: No chunking, process documents as whole units
    - **Fixed Size**: Fixed character-based chunks with overlap
    - **Recursive**: Hierarchical splitting using multiple separators
    - **Paragraph**: Split on paragraph boundaries with size limits
    - **Sentence**: Split on sentence boundaries with size limits
    - **Semantic**: AI-powered semantic boundary detection (experimental)

    Note:
        This agent integrates with the haive-core Document Engine which provides
        the underlying processing capabilities. The agent adds workflow orchestration,
        error handling, and result aggregation on top of the engine.
    """

    # ========================================================================
    # CORE ENGINE CONFIGURATION
    # ========================================================================

    engine: DocumentEngineConfig = Field(
        default_factory=lambda: DocumentEngineConfig(
            name="comprehensive_document_engine",
            processing_strategy=ProcessingStrategy.ENHANCED,
            chunking_strategy=ChunkingStrategy.RECURSIVE,
            chunk_size=1000,
            chunk_overlap=200,
            parallel_processing=True,
            max_workers=4,
            extract_metadata=True,
            normalize_content=True,
            skip_invalid=True,
        ),
        description="Document engine configuration for the processing pipeline",
    )

    # ========================================================================
    # SOURCE CONFIGURATION
    # ========================================================================

    allowed_source_types: list[DocumentSourceType] = Field(
        default_factory=lambda: [
            DocumentSourceType.FILE,
            DocumentSourceType.DIRECTORY,
            DocumentSourceType.URL,
            DocumentSourceType.DATABASE,
            DocumentSourceType.CLOUD,
        ],
        description="Allowed source types for processing",
    )

    auto_detect_sources: bool = Field(
        default=True, description="Whether to auto-detect source types"
    )

    max_sources: int | None = Field(
        default=None, description="Maximum number of sources to process"
    )

    # ========================================================================
    # PROCESSING CONFIGURATION
    # ========================================================================

    processing_strategy: ProcessingStrategy = Field(
        default=ProcessingStrategy.ENHANCED,
        description="Strategy for document processing",
    )

    parallel_processing: bool = Field(
        default=True, description="Whether to enable parallel processing"
    )

    max_workers: int = Field(
        default=4,
        description="Maximum worker threads for parallel processing",
        ge=1,
        le=32,
    )

    # ========================================================================
    # CHUNKING CONFIGURATION
    # ========================================================================

    chunking_strategy: ChunkingStrategy = Field(
        default=ChunkingStrategy.RECURSIVE, description="Strategy for document chunking"
    )

    chunk_size: int = Field(
        default=1000, description="Size of chunks in characters", ge=10, le=10000
    )

    chunk_overlap: int = Field(
        default=200, description="Overlap between consecutive chunks", ge=0
    )

    # ========================================================================
    # CONTENT PROCESSING OPTIONS
    # ========================================================================

    normalize_content: bool = Field(
        default=True, description="Whether to normalize content (whitespace, encoding)"
    )

    extract_metadata: bool = Field(
        default=True, description="Whether to extract document metadata"
    )

    detect_language: bool = Field(
        default=False, description="Whether to detect document language"
    )

    # ========================================================================
    # PIPELINE STAGES (OPTIONAL)
    # ========================================================================

    enable_embedding: bool = Field(
        default=False, description="Whether to generate vector embeddings"
    )

    enable_storage: bool = Field(
        default=False, description="Whether to store in vector database"
    )

    enable_retrieval: bool = Field(
        default=False, description="Whether to enable retrieval capabilities"
    )

    # ========================================================================
    # ERROR HANDLING
    # ========================================================================

    raise_on_error: bool = Field(
        default=False, description="Whether to raise exceptions on individual errors"
    )

    skip_invalid: bool = Field(
        default=True, description="Whether to skip invalid documents"
    )

    # ========================================================================
    # STRUCTURED OUTPUT
    # ========================================================================

    structured_output_model: type[BaseModel] = Field(
        default=DocumentProcessingResult,
        description="Structured output model for processing results",
    )

    # ========================================================================
    # VALIDATION AND SETUP
    # ========================================================================

    @field_validator("engine")
    @classmethod
    def validate_engine_type(cls, v):
        """Ensure engine is DocumentEngineConfig."""
        if v is not None and not isinstance(v, DocumentEngineConfig):
            raise ValueError("DocumentAgent engine must be DocumentEngineConfig")
        return v

    @field_validator("chunk_overlap")
    @classmethod
    def validate_chunk_overlap(cls, v, info):
        """Ensure chunk overlap is less than chunk size."""
        if hasattr(info, "data") and "chunk_size" in info.data:
            chunk_size = info.data["chunk_size"]
            if v >= chunk_size:
                raise ValueError("chunk_overlap must be less than chunk_size")
        return v

    def setup_agent(self):
        """Configure the document engine with agent settings."""
        if self.engine:
            # Create actual engine instance from config
            from haive.core.engine.document import DocumentEngine

            actual_engine = DocumentEngine(config=self.engine)

            # Add engine to engines dict
            self.engines["main"] = actual_engine

            # Register engine in EngineRegistry
            self._register_engine_in_registry()

            # Sync configuration to engine
            self._sync_configuration_to_engine()

            # Force schema regeneration
            self.set_schema = True

    def _register_engine_in_registry(self) -> None:
        """Register the engine in EngineRegistry."""
        actual_engine = self.engines.get("main")
        if not actual_engine:
            return

        try:
            from haive.core.engine.base import EngineRegistry

            registry = EngineRegistry.get_instance()

            if not registry.find(actual_engine.config.name):
                registry.register(actual_engine)
                logger.info(
                    f"Registered engine '{actual_engine.config.name}' in EngineRegistry"
                )
            else:
                logger.debug(f"Engine '{self.engine.name}' already registered")

        except ImportError:
            logger.warning("Could not import EngineRegistry - registration skipped")
        except Exception as e:
            logger.warning(f"Failed to register engine: {e}")

    def _sync_configuration_to_engine(self) -> None:
        """Sync agent configuration to the document engine."""
        if not self.engine:
            return

        # Sync processing configuration
        self.engine.processing_strategy = self.processing_strategy
        self.engine.parallel_processing = self.parallel_processing
        self.engine.max_workers = self.max_workers

        # Sync chunking configuration
        self.engine.chunking_strategy = self.chunking_strategy
        self.engine.chunk_size = self.chunk_size
        self.engine.chunk_overlap = self.chunk_overlap

        # Sync content processing options
        self.engine.normalize_content = self.normalize_content
        self.engine.extract_metadata = self.extract_metadata
        self.engine.detect_language = self.detect_language

        # Sync error handling
        self.engine.raise_on_error = self.raise_on_error
        self.engine.skip_invalid = self.skip_invalid

        logger.debug("Synchronized agent configuration to document engine")

    # ========================================================================
    # GRAPH BUILDING
    # ========================================================================

    def build_graph(self) -> BaseGraph:
        """Build the document processing graph."""
        graph = BaseGraph(name=f"{self.name}_document_pipeline")

        # Get actual engine instance from engines dict
        actual_engine = self.engines.get("main")
        if not actual_engine:
            raise ValueError("No engine found in engines dict")

        # Add document processing node
        engine_node = EngineNodeConfig(name="document_processor", engine=actual_engine)
        graph.add_node("document_processor", engine_node)

        # Simple linear pipeline: START -> document_processor -> END
        graph.add_edge(START, "document_processor")
        graph.add_edge("document_processor", END)

        # Store pipeline configuration in metadata
        graph.metadata.update(
            {
                "pipeline_stages": self._get_pipeline_stages(),
                "processing_strategy": self.processing_strategy.value,
                "chunking_strategy": self.chunking_strategy.value,
                "allowed_source_types": [st.value for st in self.allowed_source_types],
            }
        )

        return graph

    def _get_pipeline_stages(self) -> list[str]:
        """Get list of enabled pipeline stages."""
        stages = ["fetch", "load", "transform", "split", "annotate"]

        if self.enable_embedding:
            stages.append("embed")
        if self.enable_storage:
            stages.append("store")
        if self.enable_retrieval:
            stages.append("retrieve")

        return stages

    # ========================================================================
    # DOCUMENT PROCESSING METHODS
    # ========================================================================

    def process_sources(
        self, sources: str | List[str], **kwargs
    ) -> DocumentProcessingResult:
        """Process multiple document sources through the full pipeline.

        Args:
            sources: Single source or list of sources to process
            **kwargs: Additional processing options

        Returns:
            DocumentProcessingResult with comprehensive pipeline results
        """
        # Normalize sources to list and filter out invalid ones
        if isinstance(sources, str):
            sources = [sources]

        # Filter out None values and invalid sources
        sources = [s for s in sources if s is not None]

        # Validate source count
        if self.max_sources and len(sources) > self.max_sources:
            sources = sources[: self.max_sources]
            logger.warning(f"Limited processing to {self.max_sources} sources")

        # Process each source
        all_results = []
        total_processing_time = 0.0

        for source in sources:
            try:
                # Create input for engine
                input_data = DocumentInput(source=source, **kwargs)

                # Process through actual engine directly
                actual_engine = self.engines.get("main")
                if actual_engine:
                    engine_result = actual_engine.invoke(input_data)
                    all_results.append(engine_result)

                    if hasattr(engine_result, "operation_time"):
                        total_processing_time += engine_result.operation_time
                else:
                    logger.error("No engine available for processing")

            except Exception as e:
                logger.exception(f"Failed to process source {source}: {e}")
                if not self.skip_invalid:
                    raise

        # Aggregate results
        return self._aggregate_results(all_results, sources, total_processing_time)

    def process_directory(
        self,
        directory_path: str,
        recursive: bool = True,
        include_patterns: List[str] | None = None,
        exclude_patterns: List[str] | None = None,
        **kwargs,
    ) -> DocumentProcessingResult:
        """Process all documents in a directory.

        Args:
            directory_path: Path to directory
            recursive: Whether to process subdirectories
            include_patterns: Glob patterns for files to include
            exclude_patterns: Glob patterns for files to exclude
            **kwargs: Additional processing options

        Returns:
            DocumentProcessingResult with directory processing results
        """
        input_data = DocumentInput(
            source=directory_path,
            include_patterns=include_patterns or [],
            exclude_patterns=exclude_patterns or [],
            **kwargs,
        )

        # Update engine configuration for directory processing
        original_recursive = self.engine.recursive
        self.engine.recursive = recursive

        try:
            result = self.invoke(input_data)
            return self._convert_engine_result_to_agent_result(result, [directory_path])
        finally:
            # Restore original setting
            self.engine.recursive = original_recursive

    def process_urls(self, urls: list[str], **kwargs) -> DocumentProcessingResult:
        """Process documents from web URLs.

        Args:
            urls: List of URLs to process
            **kwargs: Additional processing options

        Returns:
            DocumentProcessingResult with web processing results
        """
        return self.process_sources(urls, **kwargs)

    def process_cloud_storage(
        self, cloud_paths: list[str], **kwargs
    ) -> DocumentProcessingResult:
        """Process documents from cloud storage.

        Args:
            cloud_paths: List of cloud storage paths (s3://, gs://, etc.)
            **kwargs: Additional processing options

        Returns:
            DocumentProcessingResult with cloud processing results
        """
        return self.process_sources(cloud_paths, **kwargs)

    def analyze_source_structure(self, source: str, **kwargs) -> dict[str, Any]:
        """Analyze the structure of a source without full processing.

        Args:
            source: Source to analyze
            **kwargs: Additional analysis options

        Returns:
            Dictionary with source structure analysis
        """
        # Temporarily disable chunking for structure analysis
        original_strategy = self.chunking_strategy
        self.engine.chunking_strategy = ChunkingStrategy.NONE

        try:
            input_data = DocumentInput(source=source, **kwargs)
            result = self.invoke(input_data)

            return {
                "source": source,
                "source_type": (
                    result.source_type.value
                    if hasattr(result, "source_type")
                    else "unknown"
                ),
                "document_count": (
                    result.total_documents if hasattr(result, "total_documents") else 0
                ),
                "total_size": (
                    sum(doc.character_count for doc in result.documents)
                    if hasattr(result, "documents")
                    else 0
                ),
                "formats": (
                    list(set(doc.format.value for doc in result.documents})
                    if hasattr(result, "documents")
                    else []
                ),
                "analysis_time": (
                    result.operation_time if hasattr(result, "operation_time") else 0.0
                ),
            }
        finally:
            # Restore original chunking strategy
            self.engine.chunking_strategy = original_strategy

    # ========================================================================
    # RESULT PROCESSING
    # ========================================================================

    def _aggregate_results(
        self,
        engine_results: list[DocumentOutput],
        sources: list[str],
        total_time: float,
    ) -> DocumentProcessingResult:
        """Aggregate multiple engine results into a comprehensive result."""
        # Initialize counters
        total_documents = 0
        total_chunks = 0
        total_characters = 0
        total_words = 0
        successful_sources = 0
        failed_sources = 0
        processing_errors = []
        source_types = {}
        document_formats = {}

        # Aggregate all processed documents
        all_documents = []
        all_chunks = []

        for result in engine_results:
            if result.has_errors:
                failed_sources += 1
                processing_errors.extend(
                    [error.get("error", str(error)) for error in result.errors]
                )
            else:
                successful_sources += 1

            total_documents += result.total_documents
            total_chunks += result.total_chunks
            total_characters += result.total_characters
            total_words += result.total_words

            # Track source types
            source_type = result.source_type.value
            source_types[source_type] = source_types.get(source_type, 0) + 1

            # Track document formats and collect documents/chunks
            for doc in result.documents:
                all_documents.append(
                    doc.model_dump() if hasattr(doc, "model_dump") else doc
                )

                # Track format
                doc_format = doc.format.value if hasattr(doc, "format") else "unknown"
                document_formats[doc_format] = document_formats.get(doc_format, 0) + 1

                # Collect chunks
                if hasattr(doc, "chunks"):
                    for chunk in doc.chunks:
                        chunk_data = (
                            chunk.model_dump()
                            if hasattr(chunk, "model_dump")
                            else chunk
                        )
                        all_chunks.append(chunk_data)

        # Calculate average chunk size
        average_chunk_size = 0.0
        if total_chunks > 0:
            average_chunk_size = total_characters / total_chunks

        return DocumentProcessingResult(
            # Pipeline Results
            fetched_sources=[str(s) for s in sources if s is not None],
            loaded_documents=all_documents,
            transformed_documents=all_documents,  # Same as loaded for now
            document_chunks=all_chunks,
            annotated_chunks=all_chunks,  # Same as chunks for now
            embedded_chunks=[] if not self.enable_embedding else all_chunks,
            stored_documents=(
                []
                if not self.enable_storage
                else [f"doc_{i}" for i in range(total_documents)]
            ),
            # Pipeline Statistics
            total_sources=len(sources),
            total_documents=total_documents,
            total_chunks=total_chunks,
            total_annotations=total_chunks,  # One annotation per chunk for now
            # Processing Metadata
            processing_time=total_time,
            pipeline_strategy=self.processing_strategy.value,
            chunking_strategy=self.chunking_strategy.value,
            # Source Analysis
            source_types=source_types,
            document_formats=document_formats,
            # Quality Metrics
            successful_sources=successful_sources,
            failed_sources=failed_sources,
            processing_errors=processing_errors,
            # Content Analysis
            total_characters=total_characters,
            total_words=total_words,
            average_chunk_size=average_chunk_size,
        )

    def _convert_engine_result_to_agent_result(
        self, engine_result: DocumentOutput, sources: list[str]
    ) -> DocumentProcessingResult:
        """Convert a single engine result to agent result format."""
        return self._aggregate_results(
            [engine_result], sources, engine_result.operation_time
        )

    # ========================================================================
    # CONVENIENCE CONSTRUCTORS
    # ========================================================================

    @classmethod
    def create_for_pdfs(
        cls, name: str = "PDF Document Agent", chunk_size: int = 1000, **kwargs
    ) -> "DocumentAgent":
        """Create DocumentAgent optimized for PDF processing."""
        return cls(
            name=name,
            chunking_strategy=ChunkingStrategy.PARAGRAPH,
            chunk_size=chunk_size,
            processing_strategy=ProcessingStrategy.ENHANCED,
            parallel_processing=True,
            extract_metadata=True,
            normalize_content=True,
            **kwargs,
        )

    @classmethod
    def create_for_web_scraping(
        cls, name: str = "Web Scraping Agent", **kwargs
    ) -> "DocumentAgent":
        """Create DocumentAgent optimized for web content processing."""
        return cls(
            name=name,
            allowed_source_types=[DocumentSourceType.URL],
            chunking_strategy=ChunkingStrategy.SEMANTIC,
            chunk_size=1500,
            processing_strategy=ProcessingStrategy.ENHANCED,
            normalize_content=True,
            detect_language=True,
            **kwargs,
        )

    @classmethod
    def create_for_databases(
        cls, name: str = "Database Document Agent", **kwargs
    ) -> "DocumentAgent":
        """Create DocumentAgent optimized for database document processing."""
        return cls(
            name=name,
            allowed_source_types=[DocumentSourceType.DATABASE],
            chunking_strategy=ChunkingStrategy.FIXED_SIZE,
            chunk_size=500,
            processing_strategy=ProcessingStrategy.PARALLEL,
            parallel_processing=True,
            max_workers=8,
            **kwargs,
        )

    @classmethod
    def create_for_enterprise(
        cls, name: str = "Enterprise Document Agent", **kwargs
    ) -> "DocumentAgent":
        """Create DocumentAgent optimized for enterprise-scale processing."""
        return cls(
            name=name,
            processing_strategy=ProcessingStrategy.PARALLEL,
            chunking_strategy=ChunkingStrategy.RECURSIVE,
            chunk_size=1200,
            chunk_overlap=150,
            parallel_processing=True,
            max_workers=16,
            extract_metadata=True,
            normalize_content=True,
            detect_language=True,
            enable_embedding=True,
            enable_storage=True,
            skip_invalid=True,
            **kwargs,
        )

    @classmethod
    def create_for_research(
        cls, name: str = "Research Document Agent", **kwargs
    ) -> "DocumentAgent":
        """Create DocumentAgent optimized for research document processing."""
        return cls(
            name=name,
            allowed_source_types=[
                DocumentSourceType.FILE,
                DocumentSourceType.URL,
                DocumentSourceType.DATABASE,
            ],
            chunking_strategy=ChunkingStrategy.SEMANTIC,
            chunk_size=2000,
            chunk_overlap=300,
            processing_strategy=ProcessingStrategy.ENHANCED,
            extract_metadata=True,
            normalize_content=True,
            detect_language=True,
            enable_embedding=True,
            **kwargs,
        )

    def __repr__(self) -> str:
        pipeline_stages = "->".join(self._get_pipeline_stages())
        return (
            f"DocumentAgent("
            f"name='{self.name}', "
            f"strategy={self.processing_strategy.value}, "
            f"chunking={self.chunking_strategy.value}, "
            f"pipeline={pipeline_stages}"
            f")"
        )
