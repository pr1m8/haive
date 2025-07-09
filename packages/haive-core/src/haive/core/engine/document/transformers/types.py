from enum import Enum


class DocTransformerType(str, Enum):
    """Types of document transformers supported by the engine."""

    HTML_TO_TEXT = "html_to_text"
    HTML_TO_MARKDOWN = "html_to_markdown"
    BEAUTIFUL_SOUP = "beautiful_soup"
    LONG_CONTEXT_REORDER = "long_context_reorder"
    EMBEDDINGS_REDUNDANT_FILTER = "embeddings_redundant_filter"
    EMBEDDINGS_CLUSTERING_FILTER = "embeddings_clustering_filter"
    GOOGLE_TRANSLATE = "google_translate"
    NUCLIA_TEXT = "nuclia_text"
    OPENAI_METADATA_TAGGER = "openai_metadata_tagger"
