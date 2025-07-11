"""Document agent for loading and processing documents from various sources.

This module provides the DocumentAgent class, which is a Haive agent for loading,
processing, and managing documents from various sources. It also includes factory
functions for creating specialized document agents.
"""

from __future__ import annotations

import datetime
import logging
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Any, cast

from haive.agents.base.agent import Agent
from haive.core.graph.node import node
from haive.core.schema.base import StateSchema
from langgraph.graph import END, StateGraph
from pydantic import BaseModel, Field

# Import document processor functions
from .document_processors import process_document, split_document
from .document_state import (ChunkingOptions, ChunkingStrategy, Document,
                             DocumentChunk, DocumentFormat, DocumentSource,
                             DocumentSourceType, DocumentState, LoadingOptions,
                             LoadingStrategy, ProcessingStage)
from .loader_strategy import get_loader_for_source
from .path_analysis_implementation import analyze_path


class DocumentAgentOptions(BaseModel):
    """Options for document agent configuration.

    Attributes:
        default_loading_options (LoadingOptions): Default options for document loading.
        default_chunking_options (ChunkingOptions): Default options for document chunking.
        parallel_processing (bool): Whether to process documents in parallel.
        max_workers (int): Maximum number of parallel workers for document processing.
        source_timeout_seconds (int): Timeout in seconds for source analysis.
        loading_timeout_seconds (int): Timeout in seconds for document loading.
        chunking_timeout_seconds (int): Timeout in seconds for document chunking.
        max_documents (Optional[int]): Maximum number of documents to process.
        max_document_size_bytes (Optional[int]): Maximum size of documents to process in bytes.
        skip_errors (bool): Whether to skip errors and continue processing.
    """

    default_loading_options: LoadingOptions = Field(default_factory=LoadingOptions)
    default_chunking_options: ChunkingOptions = Field(default_factory=ChunkingOptions)
    parallel_processing: bool = True
    max_workers: int = 4
    source_timeout_seconds: int = 30
    loading_timeout_seconds: int = 120
    chunking_timeout_seconds: int = 60
    max_documents: int | None = None
    max_document_size_bytes: int | None = None
    skip_errors: bool = True


class DocumentAgent(Agent):
    """Agent for loading and processing documents from various sources.

    The DocumentAgent class provides functionality for loading documents from various
    sources, processing them, and preparing them for downstream tasks. It uses a
    state-based approach to track document sources, loaded documents, and processing
    state.

    Attributes:
        options (DocumentAgentOptions): Options for agent configuration.
    """

    def __init__(
        self,
        state_schema: StateSchema | None = None,
        options: DocumentAgentOptions | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize a DocumentAgent.

        Args:
            state_schema: Optional state schema. If not provided, a DocumentState will be created.
            options: Optional document agent options. If not provided, default options will be used.
            **kwargs: Additional arguments to pass to the base Agent constructor.
        """
        if state_schema is None:
            state_schema = DocumentState()

        self.options = options or DocumentAgentOptions()

        # Initialize state with default options
        if isinstance(state_schema, DocumentState):
            self._initialize_state(state_schema)

        super().__init__(state_schema=state_schema, **kwargs)

    def _initialize_state(self, state: DocumentState) -> None:
        """Initialize the state with default options and starting values.

        This method sets up the initial state for document processing, ensuring
        that all necessary options and statistics are properly initialized.

        Args:
            state: The document state to initialize.
        """
        # Set default options
        state.loading_options = self.options.default_loading_options
        state.chunking_options = self.options.default_chunking_options
        state.parallel_processing = self.options.parallel_processing
        state.max_workers = self.options.max_workers

        # Initialize processing statistics
        state.processing_stats.start_time = datetime.datetime.now()

        # Log initialization
        logger = logging.getLogger(__name__)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Initialized DocumentAgent with options: {self.options}")
            logger.debug(f"Loading strategy: {state.loading_options.strategy}")
            logger.debug(f"Chunking strategy: {state.chunking_options.strategy}")
            logger.debug(
                f"Parallel processing: {state.parallel_processing} (max workers: {state.max_workers})"
            )

    def add_source(self, path: str, **kwargs: Any) -> DocumentSource:
        """Add a document source to be processed.

        Args:
            path: Path or URL to the document source.
            **kwargs: Additional fields to set on the DocumentSource.

        Returns:
            DocumentSource: The created source.
        """
        state = cast(DocumentState, self.state)
        return state.add_source(path, **kwargs)

    def add_sources(self, paths: list[str]) -> list[DocumentSource]:
        """Add multiple document sources to be processed.

        Args:
            paths: List of paths or URLs to document sources.

        Returns:
            List[DocumentSource]: The created sources.
        """
        state = cast(DocumentState, self.state)
        return state.add_sources(paths)

    def get_documents(self) -> list[Document]:
        """Get all loaded documents.

        Returns:
            List[Document]: All loaded documents.
        """
        state = cast(DocumentState, self.state)
        return state.documents

    def get_document(self, document_id: str) -> Document | None:
        """Get a document by ID.

        Args:
            document_id: The ID of the document.

        Returns:
            Optional[Document]: The document, or None if not found.
        """
        state = cast(DocumentState, self.state)
        return state.get_document(document_id)

    def get_documents_by_source(self, source_path: str) -> list[Document]:
        """Get all documents from a specific source.

        Args:
            source_path: Path of the source.

        Returns:
            List[Document]: Documents from the source.
        """
        state = cast(DocumentState, self.state)
        return state.get_documents_by_source(source_path)

    def get_documents_by_format(self, format: DocumentFormat | str) -> list[Document]:
        """Get all documents of a specific format.

        Args:
            format: The format to filter by.

        Returns:
            List[Document]: Documents with the specified format.
        """
        state = cast(DocumentState, self.state)
        return state.get_documents_by_format(format)

    def get_all_chunks(self) -> list[DocumentChunk]:
        """Get all document chunks across all documents.

        Returns:
            List[DocumentChunk]: All document chunks.
        """
        state = cast(DocumentState, self.state)
        return state.get_all_chunks()

    def clear(self) -> None:
        """Clear the agent state."""
        self.state = DocumentState()

    @node
    def analyze_source(self, state: DocumentState) -> DocumentState:
        """Analyze document sources and prepare them for loading.

        This node function analyzes each document source, determines its type
        and format, and prepares it for loading. It updates the source stage to
        ANALYZING during processing and to QUEUED when ready for loading.

        Args:
            state: The current document state.

        Returns:
            DocumentState: The updated document state.
        """
        for source in state.sources:
            if source.stage == ProcessingStage.INITIALIZED:
                try:
                    source.update_stage(ProcessingStage.ANALYZING)

                    # Use path analysis to determine source type and format
                    path_info = analyze_path(source.path)

                    # Update source with analysis results
                    if path_info.source_type != DocumentSourceType.UNKNOWN:
                        source.source_type = path_info.source_type

                    if path_info.document_format != DocumentFormat.UNKNOWN:
                        source.format = path_info.document_format

                    # Update metadata with analysis results
                    if path_info.metadata:
                        for key, value in path_info.metadata.items():
                            if hasattr(source.metadata, key):
                                setattr(source.metadata, key, value)
                            else:
                                source.metadata.custom[key] = value

                    # Update stage to QUEUED for loading
                    source.update_stage(ProcessingStage.QUEUED)

                except Exception as e:
                    error_msg = f"Error analyzing source: {e!s}"
                    source.update_stage(ProcessingStage.FAILED, error_msg)
                    state.error_messages.append(error_msg)
                    if not self.options.skip_errors:
                        raise

        return state

    @node
    def load_documents(self, state: DocumentState) -> DocumentState:
        """Load documents from sources.

        This node function loads documents from each source that is in the QUEUED
        stage. It updates the source stage to LOADING during processing and to
        COMPLETED when loading is complete. If chunking is disabled, it updates to
        CHUNKING when loading is complete.

        Args:
            state: The current document state.

        Returns:
            DocumentState: The updated document state.
        """
        queued_sources = state.get_sources_by_stage(ProcessingStage.QUEUED)

        if not queued_sources:
            return state

        def load_source(
            source: DocumentSource,
        ) -> tuple[DocumentSource, list[Document], str | None]:
            """Helper function to load a single source.

            Args:
                source: The source to load.

            Returns:
                Tuple containing the source, loaded documents, and optional error message.
            """
            documents = []
            error = None

            try:
                source.update_stage(ProcessingStage.LOADING)

                # Get loader for this source
                loader = get_loader_for_source(source.path, source.source_type)

                if loader is None:
                    error = f"No loader found for source: {source.path}"
                    return source, documents, error

                # Load documents
                raw_docs = loader.load()

                # Convert to Document objects
                for _i, raw_doc in enumerate(raw_docs):
                    doc_id = f"{uuid.uuid4()}"
                    content = raw_doc.page_content

                    # Create document
                    doc = Document(
                        document_id=doc_id,
                        content=content,
                        source_path=source.path,
                        source_type=source.source_type,
                        format=source.format,
                        metadata={**raw_doc.metadata, **source.metadata.custom},
                    )
                    documents.append(doc)

                # Update source stage
                if state.chunking_options.strategy == ChunkingStrategy.NONE:
                    source.update_stage(ProcessingStage.COMPLETED)
                else:
                    source.update_stage(ProcessingStage.CHUNKING)

            except Exception as e:
                error = f"Error loading source: {e!s}"
                source.update_stage(ProcessingStage.FAILED, error)

            return source, documents, error

        # Process sources in parallel or sequentially
        if state.parallel_processing and len(queued_sources) > 1:
            with ThreadPoolExecutor(max_workers=state.max_workers) as executor:
                results = list(executor.map(load_source, queued_sources))
        else:
            results = [load_source(source) for source in queued_sources]

        # Process results
        for source, documents, error in results:
            if error:
                state.error_messages.append(f"Error processing {source.path}: {error}")
                if not self.options.skip_errors:
                    raise Exception(error)
            else:
                # Add documents to state
                for doc in documents:
                    state.documents.append(doc)
                    state.processing_stats.total_documents += 1

        return state

    @node
    def chunk_documents(self, state: DocumentState) -> DocumentState:
        """Chunk documents into smaller pieces.

        This node function chunks documents associated with sources in the CHUNKING
        stage. It updates the source stage to COMPLETED when chunking is complete.
        It uses the document processors to transform and split documents based on
        their format and the configured chunking strategy.

        Args:
            state: The current document state.

        Returns:
            DocumentState: The updated document state.
        """
        chunking_sources = state.get_sources_by_stage(ProcessingStage.CHUNKING)

        if (
            not chunking_sources
            or state.chunking_options.strategy == ChunkingStrategy.NONE
        ):
            return state

        for source in chunking_sources:
            try:
                # Get documents for this source
                docs = state.get_documents_by_source(source.path)

                for doc in docs:
                    # Skip already chunked documents
                    if doc.chunks:
                        continue

                    # Get chunking strategy
                    chunking_options = source.chunking_options or state.chunking_options

                    # Process the document (transform and split) using our document processors
                    try:
                        # Use the process_document function from document_processors
                        # This will handle both transformation and splitting
                        processed_doc = process_document(doc)

                        # Set the chunking options for the document if it's not already set
                        if (
                            hasattr(processed_doc, "chunking_options")
                            and processed_doc.chunking_options is None
                        ):
                            processed_doc.chunking_options = chunking_options

                        # If process_document didn't handle chunking (no chunking_options attribute)
                        if not processed_doc.chunks:
                            # Then split the document using the appropriate splitter
                            chunks = split_document(
                                processed_doc,
                                chunking_options.strategy,
                                chunking_options,
                            )
                            processed_doc.chunks = chunks

                        # Update the document in our state
                        # Note: we need to update the reference to ensure state changes
                        for i, state_doc in enumerate(state.documents):
                            if state_doc.document_id == doc.document_id:
                                state.documents[i] = processed_doc
                                break
                    except Exception as e:
                        # If there's an error in the document processors, log it and continue
                        logger = logging.getLogger(__name__)
                        logger.warning(
                            f"Error processing document {doc.document_id}: {e!s}. Using basic chunking."
                        )

                        # Fall back to basic chunking
                        if not doc.chunks:
                            if chunking_options.strategy == ChunkingStrategy.FIXED_SIZE:
                                self._chunk_fixed_size(doc, chunking_options)
                            elif (
                                chunking_options.strategy == ChunkingStrategy.PARAGRAPH
                            ):
                                self._chunk_paragraphs(doc, chunking_options)
                            elif chunking_options.strategy == ChunkingStrategy.SENTENCE:
                                self._chunk_sentences(doc, chunking_options)
                            else:
                                # Default to fixed size if strategy not implemented
                                self._chunk_fixed_size(doc, chunking_options)

                # Update source stage
                source.update_stage(ProcessingStage.COMPLETED)

            except Exception as e:
                error_msg = f"Error chunking documents: {e!s}"
                source.update_stage(ProcessingStage.FAILED, error_msg)
                state.error_messages.append(error_msg)
                if not self.options.skip_errors:
                    raise

        return state

    def _chunk_fixed_size(self, doc: Document, options: ChunkingOptions) -> None:
        """Chunk a document into fixed-size chunks.

        Note: This is a fallback method used when document processors aren't available.

        Args:
            doc: The document to chunk.
            options: The chunking options.
        """
        content = doc.content
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
                "document_id": doc.document_id,
                "source_path": doc.source_path,
            }

            # Add metadata from document if scope includes document
            if options.metadata_scope in ["all", "document"]:
                for key, value in doc.metadata.items():
                    if key not in chunk_metadata:
                        chunk_metadata[key] = value

            # Add chunk to document
            doc.add_chunk(chunk_content, chunk_metadata)

            # Move to next chunk position, accounting for overlap
            start = end - chunk_overlap if end < len(content) else len(content)
            chunk_index += 1

    def _chunk_paragraphs(self, doc: Document, options: ChunkingOptions) -> None:
        """Chunk a document by paragraphs.

        Note: This is a fallback method used when document processors aren't available.

        Args:
            doc: The document to chunk.
            options: The chunking options.
        """
        content = doc.content

        # Split by double newlines (paragraph breaks)
        paragraphs = content.split("\n\n")

        for i, paragraph in enumerate(paragraphs):
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            # Create chunk metadata
            chunk_metadata = {
                "chunk_index": i,
                "paragraph_index": i,
                "document_id": doc.document_id,
                "source_path": doc.source_path,
            }

            # Add metadata from document if scope includes document
            if options.metadata_scope in ["all", "document"]:
                for key, value in doc.metadata.items():
                    if key not in chunk_metadata:
                        chunk_metadata[key] = value

            # Add chunk to document
            doc.add_chunk(paragraph, chunk_metadata)

    def _chunk_sentences(self, doc: Document, options: ChunkingOptions) -> None:
        """Chunk a document by sentences.

        Note: This is a fallback method used when document processors aren't available.

        Args:
            doc: The document to chunk.
            options: The chunking options.
        """
        content = doc.content

        # Simple sentence splitting by ., !, ?
        # This is a simplified approach; a more robust approach would use NLP
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
                "document_id": doc.document_id,
                "source_path": doc.source_path,
            }

            # Add metadata from document if scope includes document
            if options.metadata_scope in ["all", "document"]:
                for key, value in doc.metadata.items():
                    if key not in chunk_metadata:
                        chunk_metadata[key] = value

            # Add chunk to document
            doc.add_chunk(sentence, chunk_metadata)

    @node
    def finalize_processing(self, state: DocumentState) -> DocumentState:
        """Finalize document processing.

        This node function completes the document processing workflow by updating
        processing statistics and marking processing as complete.

        Args:
            state: The current document state.

        Returns:
            DocumentState: The updated document state.
        """
        # Update statistics
        state.processing_stats.total_chunks = state.total_chunks

        # Estimate total tokens (very rough approximation)
        total_tokens = 0
        for doc in state.documents:
            # Estimate 4 characters per token on average
            doc_tokens = len(doc.content) // 4
            total_tokens += doc_tokens

        state.processing_stats.total_tokens = total_tokens

        # Mark processing as complete
        state.mark_processing_complete()

        return state

    def _should_chunk_documents(self, state: DocumentState) -> bool:
        """Determine if we should proceed to chunking.

        This conditional function checks if there are any documents to chunk and
        if the chunking strategy is not NONE.

        Args:
            state: The current document state.

        Returns:
            bool: True if we should proceed to chunking, False otherwise.
        """
        # Skip chunking if chunking strategy is NONE
        if state.chunking_options.strategy == ChunkingStrategy.NONE:
            return False

        # Skip chunking if no documents need chunking
        chunking_sources = state.get_sources_by_stage(ProcessingStage.CHUNKING)
        return chunking_sources

    def build_graph(self) -> StateGraph:
        """Build the document agent graph.

        This method builds a LangGraph workflow for document processing, with the
        following nodes:
        - analyze_source: Analyze document sources
        - load_documents: Load documents from sources
        - chunk_documents: Chunk documents into smaller pieces (conditional)
        - finalize_processing: Finalize document processing

        The state expands progressively from source analysis to loading to chunking,
        with each step building on the previous state. The flow includes conditional
        paths based on the state.

        Returns:
            StateGraph: The constructed graph.
        """
        builder = StateGraph(DocumentState)

        # Add nodes
        builder.add_node("analyze_source", self.analyze_source)
        builder.add_node("load_documents", self.load_documents)
        builder.add_node("chunk_documents", self.chunk_documents)
        builder.add_node("finalize_processing", self.finalize_processing)

        # Define edges with conditions to ensure proper state progression
        builder.add_edge("analyze_source", "load_documents")

        # Conditional edge: Either go to chunking or skip to finalization
        builder.add_conditional_edges(
            "load_documents",
            # Condition function to determine if chunking is needed
            self._should_chunk_documents,
            {
                True: "chunk_documents",  # If chunking is needed
                False: "finalize_processing",  # Skip chunking if not needed
            },
        )

        builder.add_edge("chunk_documents", "finalize_processing")
        builder.add_edge("finalize_processing", END)

        # Set entry point
        builder.set_entry_point("analyze_source")

        return builder.compile()

    def process_documents(self) -> None:
        """Process all documents in the agent's state.

        This method runs the document processing workflow, which progressively
        expands the state from source analysis to loading to chunking to finalization.
        Each step builds on the previous state, enriching it with new information.
        """
        # Get the graph
        graph = self.build_graph()

        # Execute the workflow - the state expands progressively through each node
        self.state = graph.invoke(self.state)

        # Log summary of processing results
        logger = logging.getLogger(__name__)
        if logger.isEnabledFor(logging.INFO):
            stats = self.state.processing_stats
            logger.info("Document processing complete:")
            logger.info(
                f"- Sources: {stats.processed_sources} processed, {stats.failed_sources} failed"
            )
            logger.info(f"- Documents: {stats.total_documents} documents loaded")
            logger.info(f"- Chunks: {stats.total_chunks} chunks created")
            logger.info(
                f"- Processing time: {stats.processing_time_seconds:.2f} seconds"
            )


def create_document_agent(
    options: DocumentAgentOptions | None = None,
    sources: list[str] | None = None,
    **kwargs: Any,
) -> DocumentAgent:
    """Create a general-purpose document agent.

    Args:
        options: Optional document agent options.
        sources: Optional list of document sources to process.
        **kwargs: Additional arguments to pass to the DocumentAgent constructor.

    Returns:
        DocumentAgent: The created document agent.
    """
    agent = DocumentAgent(options=options, **kwargs)

    if sources:
        agent.add_sources(sources)

    return agent


def create_file_document_agent(
    file_paths: list[str],
    chunking_strategy: ChunkingStrategy = ChunkingStrategy.FIXED_SIZE,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    **kwargs: Any,
) -> DocumentAgent:
    """Create a document agent optimized for file loading.

    Args:
        file_paths: List of file paths to process.
        chunking_strategy: Strategy for chunking documents.
        chunk_size: Size of chunks in characters.
        chunk_overlap: Overlap between chunks in characters.
        **kwargs: Additional arguments to pass to the DocumentAgent constructor.

    Returns:
        DocumentAgent: The created document agent.
    """
    options = DocumentAgentOptions(
        default_loading_options=LoadingOptions(
            strategy=LoadingStrategy.DIRECT,
            max_files=len(file_paths),
        ),
        default_chunking_options=ChunkingOptions(
            strategy=chunking_strategy,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        ),
    )

    agent = DocumentAgent(options=options, **kwargs)
    agent.add_sources(file_paths)

    return agent


def create_web_document_agent(
    urls: list[str],
    chunking_strategy: ChunkingStrategy = ChunkingStrategy.PARAGRAPH,
    **kwargs: Any,
) -> DocumentAgent:
    """Create a document agent optimized for web loading.

    Args:
        urls: List of URLs to process.
        chunking_strategy: Strategy for chunking documents.
        **kwargs: Additional arguments to pass to the DocumentAgent constructor.

    Returns:
        DocumentAgent: The created document agent.
    """
    options = DocumentAgentOptions(
        default_loading_options=LoadingOptions(
            strategy=LoadingStrategy.DIRECT,
            timeout_seconds=120,
        ),
        default_chunking_options=ChunkingOptions(
            strategy=chunking_strategy,
        ),
    )

    agent = DocumentAgent(options=options, **kwargs)
    agent.add_sources(urls)

    return agent


def create_directory_document_agent(
    directory_paths: list[str],
    include_patterns: list[str] | None = None,
    exclude_patterns: list[str] | None = None,
    recursive: bool = True,
    recursive_depth: int = 3,
    **kwargs: Any,
) -> DocumentAgent:
    """Create a document agent optimized for directory loading.

    Args:
        directory_paths: List of directory paths to process.
        include_patterns: Optional list of glob patterns to include.
        exclude_patterns: Optional list of glob patterns to exclude.
        recursive: Whether to recursively process subdirectories.
        recursive_depth: Maximum depth for recursive processing.
        **kwargs: Additional arguments to pass to the DocumentAgent constructor.

    Returns:
        DocumentAgent: The created document agent.
    """
    if include_patterns is None:
        include_patterns = ["*.txt", "*.md", "*.pdf", "*.docx", "*.html"]

    if exclude_patterns is None:
        exclude_patterns = ["*.tmp", "*.temp", "*.log", ".git/*", "__pycache__/*"]

    loading_strategy = (
        LoadingStrategy.RECURSIVE if recursive else LoadingStrategy.DIRECT
    )

    options = DocumentAgentOptions(
        default_loading_options=LoadingOptions(
            strategy=loading_strategy,
            recursive_depth=recursive_depth,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
        ),
        parallel_processing=True,
        max_workers=8,
    )

    agent = DocumentAgent(options=options, **kwargs)
    agent.add_sources(directory_paths)

    return agent
