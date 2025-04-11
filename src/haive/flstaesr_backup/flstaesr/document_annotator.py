from typing import List, Dict, Any, Optional, Union, Type, Callable
from langchain_core.documents import Document
import logging

logger = logging.getLogger(__name__)

class DocumentAnnotatorRegistry:
    """Registry for document annotators with factory methods for different annotations."""
    
    @staticmethod
    def get_metadata_tagger(schema, llm):
        """Get an annotator for tagging documents with metadata."""
        from langchain.chains import create_tagging_chain
        from langchain_community.document_transformers import OpenAIMetadataTagger
        
        tagging_chain = create_tagging_chain(schema, llm)
        return OpenAIMetadataTagger(tagging_chain=tagging_chain)
    
    @staticmethod
    def get_property_extractor(properties, llm):
        """Get an annotator for extracting properties from documents."""
        from langchain_community.document_transformers import DoctranPropertyExtractor
        return DoctranPropertyExtractor(properties=properties, llm=llm)
    
    @staticmethod
    def get_qa_transformer(llm):
        """Get an annotator for generating QA pairs from documents."""
        from langchain_community.document_transformers import DoctranQATransformer
        return DoctranQATransformer(llm=llm)
    
    @staticmethod
    def get_text_translator(language, llm):
        """Get an annotator for translating documents."""
        from langchain_community.document_transformers import DoctranTextTranslator
        return DoctranTextTranslator(language=language, llm=llm)
    
    @staticmethod
    def get_nuclia_text_transformer():
        """Get the Nuclia text transformer for advanced document understanding."""
        from langchain_community.document_transformers import NucliaTextTransformer
        return NucliaTextTransformer()
    
    @staticmethod
    def get_document_compressor(base_compressor, llm):
        """Get a document compressor for contextual compression."""
        from langchain.retrievers.document_compressors import LLMChainExtractor
        return LLMChainExtractor.from_llm(llm=llm)
    
    @staticmethod
    def create_summary_annotation(docs: List[Document], llm):
        """Add summary annotations to documents."""
        from langchain_core.prompts import PromptTemplate
        from langchain_core.output_parsers import StrOutputParser
        
        # Create summarization chain
        summary_prompt = PromptTemplate.from_template(
            "Summarize the following text in a concise paragraph:\n\n{text}"
        )
        summary_chain = summary_prompt | llm | StrOutputParser()
        
        # Process each document and add summary as metadata
        processed_docs = []
        for doc in docs:
            try:
                summary = summary_chain.invoke({"text": doc.page_content})
                # Create a new document with updated metadata
                metadata = dict(doc.metadata)
                metadata["summary"] = summary
                processed_doc = Document(page_content=doc.page_content, metadata=metadata)
                processed_docs.append(processed_doc)
            except Exception as e:
                logger.warning(f"Failed to summarize document: {str(e)}")
                processed_docs.append(doc)  # Keep original on failure
        
        return processed_docs
    
    @staticmethod
    def create_entity_annotation(docs: List[Document], llm):
        """Add entity annotations to documents (people, organizations, locations, etc.)."""
        schema = {
            "properties": {
                "entities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "type": {"type": "string", "enum": ["PERSON", "ORGANIZATION", "LOCATION", "DATE", "OTHER"]},
                        },
                        "required": ["name", "type"]
                    },
                    "description": "List of entities mentioned in the text"
                }
            },
            "required": ["entities"]
        }
        
        # Create entity extraction chain
        from langchain.chains import create_extraction_chain
        extraction_chain = create_extraction_chain(schema, llm)
        
        # Process each document and add entities as metadata
        processed_docs = []
        for doc in docs:
            try:
                content = doc.page_content
                # Limit content length for extraction
                if len(content) > 5000:
                    content = content[:5000]
                    
                entities = extraction_chain.invoke(content)
                
                # Create a new document with updated metadata
                metadata = dict(doc.metadata)
                metadata["entities"] = entities
                processed_doc = Document(page_content=doc.page_content, metadata=metadata)
                processed_docs.append(processed_doc)
            except Exception as e:
                logger.warning(f"Failed to extract entities: {str(e)}")
                processed_docs.append(doc)  # Keep original on failure
        
        return processed_docs
    
    @staticmethod
    def create_hyde_annotation(query: str, docs: List[Document], llm):
        """Add HyDE (Hypothetical Document Embedding) annotations based on query."""
        from langchain_core.prompts import PromptTemplate
        from langchain_core.output_parsers import StrOutputParser
        
        # Create HyDE generation chain
        hyde_prompt = PromptTemplate.from_template(
            "Based on the question, generate a hypothetical document that would contain the answer.\n\n"
            "Question: {query}\n\n"
            "Hypothetical Document:"
        )
        hyde_chain = hyde_prompt | llm | StrOutputParser()
        
        # Generate hypothetical document
        try:
            hyde_content = hyde_chain.invoke({"query": query})
            
            # Create a new document with the hypothetical content
            hyde_doc = Document(
                page_content=hyde_content,
                metadata={
                    "source": "hyde_generated",
                    "query": query,
                    "is_hypothetical": True
                }
            )
            
            # Add the HyDE document to the list
            return docs + [hyde_doc]
        except Exception as e:
            logger.warning(f"Failed to create HyDE annotation: {str(e)}")
            return docs  # Return original docs on failure
    
    @staticmethod
    def create_keyword_annotation(docs: List[Document], llm, num_keywords=5):
        """Add keyword annotations to documents."""
        from langchain_core.prompts import PromptTemplate
        from langchain_core.output_parsers import StrOutputParser
        
        keyword_prompt = PromptTemplate.from_template(
            "Extract the top {num_keywords} keywords from the following text. "
            "Provide them as a comma-separated list:\n\n{text}"
        )
        keyword_chain = keyword_prompt | llm | StrOutputParser()
        
        # Process each document and add keywords as metadata
        processed_docs = []
        for doc in docs:
            try:
                # Limit content length
                content = doc.page_content
                if len(content) > 2000:
                    content = content[:2000]
                    
                keywords = keyword_chain.invoke({"text": content, "num_keywords": num_keywords})
                
                # Clean up keywords
                keyword_list = [k.strip() for k in keywords.split(",")]
                
                # Create a new document with updated metadata
                metadata = dict(doc.metadata)
                metadata["keywords"] = keyword_list
                processed_doc = Document(page_content=doc.page_content, metadata=metadata)
                processed_docs.append(processed_doc)
            except Exception as e:
                logger.warning(f"Failed to extract keywords: {str(e)}")
                processed_docs.append(doc)  # Keep original on failure
        
        return processed_docs