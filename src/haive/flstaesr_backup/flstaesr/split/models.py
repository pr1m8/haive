from langchain.text_splitter import RecursiveCharacterTextSplitter, TokenTextSplitter, MarkdownTextSplitter, LatexTextSplitter, HTMLTextSplitter, PythonCodeTextSplitter, RecursiveJsonSplitter
from langchain_core.documents import Document
import logging

logger = logging.getLogger(__name__)

class TextSplitterRegistry:
    """Registry for text splitters with factory methods for different content types."""
    
    @staticmethod
    def get_default_splitter(chunk_size=1000, chunk_overlap=200):
        """Get the default text splitter."""
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        return RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    @staticmethod
    def get_token_text_splitter(chunk_size=1000, chunk_overlap=200, encoding_name="cl100k_base"):
        """Get a token-based text splitter."""
        from langchain.text_splitter import TokenTextSplitter
        return TokenTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            encoding_name=encoding_name
        )
    
    @staticmethod
    def get_splitter_for_content_type(content_type, chunk_size=1000, chunk_overlap=200):
        """Get a specialized text splitter for a given content type."""
        content_type = content_type.lower() if content_type else ""
        
        if content_type in ["python", "py"]:
            from langchain.text_splitter import PythonCodeTextSplitter
            return PythonCodeTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        
        elif content_type in ["html", "htm"]:
            from langchain.text_splitter import HTMLTextSplitter
            return HTMLTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        
        elif content_type in ["markdown", "md"]:
            from langchain.text_splitter import MarkdownTextSplitter
            return MarkdownTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        
        elif content_type in ["latex", "tex"]:
            from langchain.text_splitter import LatexTextSplitter
            return LatexTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        
        elif content_type in ["json"]:
            from langchain.text_splitter import RecursiveJsonSplitter
            return RecursiveJsonSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        
        elif content_type in ["notebook", "ipynb"]:
            # For notebook files, use either TokenTextSplitter or RecursiveCharacterTextSplitter
            return TextSplitterRegistry.get_token_text_splitter(chunk_size, chunk_overlap)
        
        elif content_type in ["javascript", "js"]:
            # No specific splitter for JS yet, use default with appropriate separators
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            return RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=["\nfunction ", "\nclass ", "\nconst ", "\nlet ", "\nvar ", "\n\n", "\n", " ", ""]
            )
            
        elif content_type in ["java"]:
            # No specific splitter for Java yet, use default with appropriate separators
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            return RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=["\npublic class ", "\nclass ", "\npublic void ", "\nprivate void ", "\n\n", "\n", " ", ""]
            )
        
        else:
            return TextSplitterRegistry.get_default_splitter(chunk_size, chunk_overlap)
    
    @staticmethod
    def get_splitter_for_document(document: Document, chunk_size=1000, chunk_overlap=200):
        """Get appropriate text splitter based on document metadata."""
        metadata = document.metadata
        
        # Check source type
        if "source_type" in metadata:
            source_type = metadata["source_type"]
            if source_type == "file":
                # Use file type for content-specific splitting
                if "file_type" in metadata:
                    return TextSplitterRegistry.get_splitter_for_content_type(
                        metadata["file_type"], chunk_size, chunk_overlap
                    )
        
        # Check content type header if available
        if "content_type" in metadata:
            content_type = metadata["content_type"]
            if "text/html" in content_type:
                return TextSplitterRegistry.get_splitter_for_content_type("html", chunk_size, chunk_overlap)
            elif "application/json" in content_type:
                return TextSplitterRegistry.get_splitter_for_content_type("json", chunk_size, chunk_overlap)
            elif "text/markdown" in content_type:
                return TextSplitterRegistry.get_splitter_for_content_type("markdown", chunk_size, chunk_overlap)
        
        # Default to normal text splitter
        return TextSplitterRegistry.get_default_splitter(chunk_size, chunk_overlap)
