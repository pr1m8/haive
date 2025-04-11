from src.haive.core.engine.agent.agent import Agent, AgentConfig, register_agent
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.embeddings.base import EmbeddingsConfig
from langgraph.graph import END
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional, Union, Type, ClassVar, Annotated, Callable, Sequence
from langchain_core.documents import Document
from enum import Enum
import logging
import os
import re
import asyncio
from datetime import datetime
from urllib.parse import urljoin, urlparse
from src.haive.agents.flstaesr.document_annotator import DocumentAnnotatorRegistry
from src.haive.agents.flstaesr.fetch.models import (
    DocumentSource, URLSource, SitemapSource, ReadTheDocsSource, 
    GithubSource, RecursiveURLSource, FileSource, DirectorySource,
    HuggingFaceModelSource, HuggingFaceDatasetSource, WeatherSource
)
# Set up logging
logger = logging.getLogger(__name__)

# Define the Enum for vector store providers

from src.haive.agents.flstaesr.config import FLSTAESRAgentConfig

@register_agent(FLSTAESRAgentConfig)
class FLSTAESRAgent(Agent[FLSTAESRAgentConfig]):
    """
    FLSTAESR Agent for RAG workflows implementing the Find-Load-Split-Transform-Annotate-Embed-Store-Retrieve pattern.
    """
    
    def setup_workflow(self) -> None:
        """Set up the FLSTAESR workflow graph."""
        logger.debug(f"Setting up workflow for FLSTAESR agent {self.config.name}")
        
        # Create DynamicGraph with our state schema
        from src.haive.core.graph.GraphBuilder import DynamicGraph
        gb = DynamicGraph(
            components=[self.config.engine],
            state_schema=self.state_schema
        )
        
        # Add routing node
        gb.add_node(
            name="router",
            config=self._create_router_function(),
            command_goto="dynamic"  # Will be determined by router
        )
        
        # Add task nodes for each FLSTAESR component
        gb.add_node(
            name="find",
            config=self._create_find_function(),
            command_goto="load"
        )
        
        gb.add_node(
            name="load",
            config=self._create_load_function(),
            command_goto="split"
        )
        
        gb.add_node(
            name="split",
            config=self._create_split_function(),
            command_goto="transform"
        )
        
        gb.add_node(
            name="transform",
            config=self._create_transform_function(),
            command_goto="annotate"
        )
        
        gb.add_node(
            name="annotate",
            config=self._create_annotate_function(),
            command_goto="embed"
        )
        
        gb.add_node(
            name="embed",
            config=self._create_embed_function(),
            command_goto="retrieve"
        )
        
        gb.add_node(
            name="retrieve",
            config=self._create_retrieve_function(),
            command_goto="generate"
        )
        
        gb.add_node(
            name="generate",
            config=self._create_generate_function(),
            command_goto=END
        )
        
        # Build the graph
        self.graph = gb.build()
        
        # Set entry point
        self.graph.set_entry_point("router")
        
        logger.info(f"FLSTAESR workflow setup complete for {self.config.name}")
    
    def _create_router_function(self):
        """Create the router function to determine the next step in the workflow."""
        
        def router_function(state):
            """Route to the appropriate node based on the input and current state."""
            # Extract query from messages if present
            if state.get("messages") and not state.get("query"):
                last_message = state["messages"][-1]
                query = last_message.content if hasattr(last_message, "content") else str(last_message)
                state["query"] = query
            
            # Determine which action to take based on the query and state
            current_step = state.get("current_step", "route")
            
            # If already in progress, continue from current step
            if current_step == "retrieve" and state.get("retriever"):
                return {"goto": "retrieve"}
            elif current_step == "generate" and state.get("context"):
                return {"goto": "generate"}
            elif current_step == "embed" and state.get("annotated_splits"):
                return {"goto": "embed"}
            elif current_step == "annotate" and state.get("transformed_splits"):
                return {"goto": "annotate"}
            elif current_step == "transform" and state.get("splits"):
                return {"goto": "transform"}
            elif current_step == "split" and state.get("documents"):
                return {"goto": "split"}
            elif current_step == "load" and state.get("document_sources"):
                return {"goto": "load"}
            
            # Default: start from the beginning - find sources
            state["current_step"] = "find"
            return {"goto": "find"}
        
        return router_function
    
    def _create_find_function(self):
        """Create the function to find sources based on the query."""
        
        def find_sources(state):
            """Find sources for the given query using search or file access."""
            query = state.get("query", "")
            logger.info(f"Finding sources for query: {query}")
            
            document_sources = []
            try:
                # Analyze the query to determine the best source type
                if "code" in query.lower() or "programming" in query.lower() or "github" in query.lower():
                    # Code-related queries might benefit from GitHub or documentation sources
                    if "python" in query.lower():
                        # Add Python documentation
                        document_sources.append(DocumentSource.from_readthedocs("python", "3", "library/index.html"))
                    
                    # Add HuggingFace models/datasets for AI related queries
                    if "model" in query.lower() or "ai" in query.lower() or "machine learning" in query.lower():
                        document_sources.append(DocumentSource.from_huggingface_model(query, limit=2))
                
                # Check for weather-related queries
                elif any(term in query.lower() for term in ["weather", "temperature", "forecast", "climate"]):
                    # Extract location info (simplified - in production would use NER)
                    # This is just a placeholder since we'd need an API key
                    logger.info("Weather related query detected, but API key required")
                
                # For general queries, use web search
                if not document_sources or "search" in query.lower():
                    # Use search API (e.g., Tavily) to find sources
                    from langchain_community.tools.tavily_search import TavilySearchResults
                    search_tool = TavilySearchResults(k=3)
                    search_results = search_tool.invoke(query)
                    
                    # Process search results into document sources
                    for result in search_results:
                        url = result.get("url")
                        if url:
                            # Decide whether to use recursive loading based on the URL
                            if "documentation" in url or "docs" in url:
                                document_source = DocumentSource.from_recursive_url(url, max_depth=2)
                            else:
                                document_source = DocumentSource.from_url(url)
                                
                            document_sources.append(document_source)
                            
                            # Also add as a source for tracking
                            state["sources"].append({
                                "url": url,
                                "title": result.get("title", ""),
                                "snippet": result.get("content", ""),
                                "source_type": "web_search"
                            })
                
                # Check for sitemap for documentation sites
                for source in state["sources"]:
                    url = source.get("url", "")
                    if ("documentation" in url or "docs" in url) and "/sitemap" not in url:
                        try:
                            # Try to find and use sitemap
                            sitemap = self._find_sitemap(url)
                            if sitemap and sitemap not in [s.source.url for s in document_sources if isinstance(s.source, SitemapSource)]:
                                document_sources.append(DocumentSource.from_sitemap(sitemap))
                        except Exception as sitemap_error:
                            logger.warning(f"Error finding sitemap for {url}: {str(sitemap_error)}")
                
                logger.info(f"Found {len(document_sources)} sources")
                state["document_sources"] = document_sources
                state["current_step"] = "load"
                
            except Exception as e:
                logger.error(f"Error finding sources: {str(e)}")
                state["error"] = f"Failed to find sources: {str(e)}"
            
            return state
        
        return find_sources
    
    def _find_sitemap(self, base_url):
        """Helper method to find sitemap URL for a given base URL."""
        if base_url.endswith("/"):
            base_url = base_url[:-1]

        # Possible sitemap locations
        common_sitemap_paths = ["sitemap.xml", "sitemap_index.xml", "sitemap/sitemap.xml"]

        for sitemap in common_sitemap_paths:
            sitemap_url = urljoin(base_url, sitemap)
            try:
                import requests
                response = requests.head(sitemap_url, timeout=5)
                if response.status_code == 200:
                    logger.info(f"Found sitemap: {sitemap_url}")
                    return sitemap_url
            except Exception:
                continue
            
        return None
    
    def _create_load_function(self):
        """Create the function to load documents from sources."""
        
        def load_documents(state):
            """Load documents from the identified sources."""
            document_sources = state.get("document_sources", [])
            logger.info(f"Loading documents from {len(document_sources)} sources")
            
            documents = []
            try:
                for doc_source in document_sources:
                    try:
                        # Get appropriate loader for the source
                        loader = self.config.document_loader_registry.get_loader_for_source(doc_source)
                        docs = loader.load()
                        
                        # Add metadata about the source to the documents
                        source_obj = doc_source.source
                        for doc in docs:
                            if isinstance(source_obj, URLSource):
                                doc.metadata["source_url"] = source_obj.url
                                doc.metadata["source_type"] = "url"
                                
                                if isinstance(source_obj, SitemapSource):
                                    doc.metadata["source_subtype"] = "sitemap"
                                elif isinstance(source_obj, ReadTheDocsSource):
                                    doc.metadata["source_subtype"] = "readthedocs"
                                    doc.metadata["project_name"] = source_obj.project_name
                                    doc.metadata["version"] = source_obj.version
                                elif isinstance(source_obj, RecursiveURLSource):
                                    doc.metadata["source_subtype"] = "recursive"
                                    doc.metadata["max_depth"] = source_obj.max_depth
                                    
                            elif isinstance(source_obj, GithubSource):
                                doc.metadata["source_url"] = source_obj.url
                                doc.metadata["source_type"] = "github"
                                doc.metadata["repo_url"] = source_obj.repo_url
                                doc.metadata["branch"] = source_obj.branch
                                doc.metadata["file_path"] = source_obj.file_path
                                
                            elif isinstance(source_obj, FileSource):
                                doc.metadata["source_file"] = source_obj.file_path
                                doc.metadata["source_type"] = "file"
                                doc.metadata["file_type"] = source_obj.file_type
                                
                            elif isinstance(source_obj, DirectorySource):
                                doc.metadata["source_directory"] = source_obj.directory_path
                                doc.metadata["source_type"] = "directory"
                                
                            elif isinstance(source_obj, HuggingFaceModelSource):
                                doc.metadata["source_type"] = "huggingface_model"
                                doc.metadata["search"] = source_obj.search
                                
                            elif isinstance(source_obj, HuggingFaceDatasetSource):
                                doc.metadata["source_type"] = "huggingface_dataset"
                                doc.metadata["search"] = source_obj.search
                                
                            elif isinstance(source_obj, WeatherSource):
                                doc.metadata["source_type"] = "weather"
                                doc.metadata["city"] = source_obj.city
                                doc.metadata["country"] = source_obj.country
                            
                        documents.extend(docs)
                        logger.info(f"Loaded {len(docs)} documents from {type(source_obj).__name__}")
                        
                    except Exception as source_error:
                        logger.error(f"Error loading from source {doc_source}: {str(source_error)}")
                        # Continue with other sources
                
                # Post-process documents
                documents = self._clean_documents(documents)
                
                logger.info(f"Loaded {len(documents)} documents total")
                state["documents"] = documents
                state["current_step"] = "split"
                
            except Exception as e:
                logger.error(f"Error loading documents: {str(e)}")
                state["error"] = f"Failed to load documents: {str(e)}"
            
            return state
        
        return load_documents
    
    def _clean_documents(self, documents):
        """Helper method to clean loaded documents."""
        cleaned_docs = []
        for doc in documents:
            if not doc.page_content or doc.page_content.isspace():
                # Skip empty documents
                continue
                
            # Clean up content
            content = doc.page_content
            
            # Remove excessive whitespace
            content = re.sub(r'\n{3,}', '\n\n', content)
            
            # Create new document with cleaned content
            metadata = doc.metadata.copy()
            cleaned_docs.append(Document(page_content=content, metadata=metadata))
            
        return cleaned_docs
    

a = FLSTAESRAgent(config=FLSTAESRAgentConfig())

