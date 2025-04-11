from src.haive.agents.flstaesr.config import EmbeddingsConfig
from src.haive.core.engine.agent.agent import LLMConfig
from langchain_core.documents import Document
from typing import List, Optional

class DocumentTransformerRegistry:
    """Registry for document transformers with factory methods for different transformations."""
    
    @staticmethod
    def get_html_cleaner():
        """Get a transformer for cleaning HTML documents."""
        from langchain_community.document_transformers import Html2TextTransformer
        return Html2TextTransformer()
    
    @staticmethod
    def get_markdown_transformer():
        """Get a transformer for converting HTML to Markdown."""
        from langchain_community.document_transformers import MarkdownifyTransformer
        return MarkdownifyTransformer()
    
    @staticmethod
    def get_embeddings_filter(embeddings: EmbeddingsConfig, threshold=0.75):
        """Get a transformer for filtering redundant documents using embeddings."""
        from langchain_community.document_transformers import EmbeddingsRedundantFilter
        return EmbeddingsRedundantFilter(embeddings=embeddings, threshold=threshold)
    
    @staticmethod
    def get_embeddings_cluster_filter(embeddings: EmbeddingsConfig, num_clusters=5, num_closest=3):
        """Get a transformer for filtering documents using clustering."""
        from langchain_community.document_transformers import EmbeddingsClusteringFilter
        return EmbeddingsClusteringFilter(
            embeddings=embeddings,
            num_clusters=num_clusters,
            num_closest=num_closest
        )
    
    @staticmethod
    def get_long_context_reorder():
        """Get a transformer for reordering long contexts to address the 'lost in the middle' problem."""
        from langchain_community.document_transformers import LongContextReorder
        return LongContextReorder()
    
    @staticmethod
    def get_transformer_for_content_type(content_type: str, **kwargs):
        """Get an appropriate transformer for a given content type."""
        content_type = content_type.lower() if content_type else ""
        
        if content_type in ["html", "htm"]:
            if kwargs.get("format") == "markdown":
                return DocumentTransformerRegistry.get_markdown_transformer()
            else:
                return DocumentTransformerRegistry.get_html_cleaner()
        
        # For other types, return None as no specific transformer is needed
        return None
    
    @staticmethod
    def get_transformer_pipeline(docs: List[Document], embedding_model: Optional[EmbeddingsConfig] = None):
        """Create a pipeline of transformers based on document types."""
        transformers = []
        embedding_model = embedding_model or EmbeddingsConfig().create_embeddings()
        # Check if documents contain HTML content
        has_html = any("html" in doc.metadata.get("content_type", "").lower() for doc in docs)
        if has_html:
            transformers.append(DocumentTransformerRegistry.get_html_cleaner())
        
        # Add clustering filter if embedding model provided and enough documents
        if embedding_model and len(docs) > 20:
            transformers.append(DocumentTransformerRegistry.get_embeddings_filter(embedding_model))
        
        # Add long context reordering if there are many documents
        if len(docs) > 5:
            transformers.append(DocumentTransformerRegistry.get_long_context_reorder())
        
        return transformers

    #return OpenAIMetadataTagger(tagging_chain=tagging_chain)
    
    @staticmethod
    def get_property_extractor(properties, llm_config: LLMConfig):
        """Get an annotator for extracting properties from documents."""
        from langchain_community.document_transformers import DoctranPropertyExtractor
        return DoctranPropertyExtractor(properties=properties, llm=llm_config.instantiate_llm())
    
    @staticmethod
    def get_qa_transformer(llm_config: LLMConfig):
        """Get an annotator for generating QA pairs from documents."""
        from langchain_community.document_transformers import DoctranQATransformer
        return DoctranQATransformer(llm=llm_config.instantiate_llm())
