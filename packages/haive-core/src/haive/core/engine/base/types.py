"""Engine type definitions for the Haive framework.

This module defines the core engine type classifications used throughout
the Haive system. These types are used for registration, factory creation,
and type checking of various engine components.
"""

from enum import Enum


class EngineType(str, Enum):
    """Enumeration of engine types supported by the Haive system.

    This enum defines the various types of engines that can be registered and
    instantiated within the Haive framework. Each engine type serves a specific
    purpose in the AI/ML pipeline.

    Attributes:
        LLM (str): Large Language Model engines for text generation and processing.
        VECTOR_STORE (str): Vector database engines for storing and retrieving embeddings.
        RETRIEVER (str): Engines for retrieving relevant information from vector stores.
        TOOL (str): Tool engines that provide specific functionalities or services.
        EMBEDDINGS (str): Engines for converting text to vector embeddings.
        AGENT (str): Agent engines that can autonomously perform complex tasks.
        DOCUMENT_LOADER (str): Engines for loading documents from various sources.
        DOCUMENT_TRANSFORMER (str): Engines for transforming document content.
        DOCUMENT_SPLITTER (str): Engines for splitting documents into chunks.
        OUTPUT_PARSER (str): Engines for parsing and structuring model outputs.
        PROMPT (str): Engines for prompt template formatting and management.

    Examples:
        >>> from haive.core.engine.base.types import EngineType
        >>> engine_type = EngineType.LLM
        >>> print(engine_type)
        'llm'
        >>> print(isinstance(engine_type, EngineType))
        True
    """

    LLM = "llm"
    VECTOR_STORE = "vector_store"
    RETRIEVER = "retriever"
    TOOL = "tool"
    EMBEDDINGS = "embeddings"
    AGENT = "agent"
    DOCUMENT_LOADER = "document_loader"
    DOCUMENT_TRANSFORMER = "document_transformer"
    DOCUMENT_SPLITTER = "document_splitter"
    OUTPUT_PARSER = "output_parser"
    PROMPT = "prompt"
