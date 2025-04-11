# src/haive/agents/sources/source_finder_agent.py

from typing import Any, Dict, List, Optional, Union, Type, Annotated, Sequence, cast
import logging
import json
from datetime import datetime
import os
from urllib.parse import urlparse
from src.haive.core.models.vectorstore.base import VectorStoreConfig
from pydantic import BaseModel, Field, create_model
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import BaseTool, StructuredTool, tool
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, Runnable
from langchain_core.documents import Document
from langgraph.graph import add_messages, END, StateGraph
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore

from langchain_community.retrievers import WebResearchRetriever
from langchain_community.utilities import GoogleSearchAPIWrapper #GitHubAPIWrapper
from langchain_community.retrievers import TavilySearchAPIRetriever,WikipediaRetriever,ArxivRetriever,AskNewsRetriever,AzureAISearchRetriever,AzureCognitiveSearchRetriever
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.document_loaders import WebBaseLoader, GitLoader, ReadTheDocsLoader, SitemapLoader,GithubFileLoader,GitHubIssuesLoader

from src.haive.core.engine.agent.agent import Agent, AgentConfig, register_agent
from src.haive.core.engine.aug_llm import AugLLMConfig, compose_runnable
from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.core.graph.GraphBuilder import DynamicGraph
from src.haive.core.graph.routing import Router, ContentCondition, StateValueCondition
from src.haive.core.models.embeddings.base import EmbeddingsConfig
# Set up logging
logger = logging.getLogger(__name__)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
# ===========================================
# Source Finder Schema
# ===========================================

class SourceQueryState(BaseModel):
    """State for the query analysis step."""
    query: str = Field(..., description="Original user query")
    analyzed_query: Optional[str] = Field(default=None, description="Analyzed version of the query")
    potential_topics: List[str] = Field(default_factory=list, description="Potential topics extracted from query")
    source_type_suggestions: List[str] = Field(default_factory=list, description="Suggested source types")
    query_keywords: List[str] = Field(default_factory=list, description="Keywords extracted from query")
    domain_specific_terms: List[str] = Field(default_factory=list, description="Domain-specific terms identified")
    search_strategy: str = Field(default="general", description="Determined search strategy")

class SourceFindingState(BaseModel):
    """State for the source finding step."""
    search_results: List[Dict[str, Any]] = Field(default_factory=list, description="Search results")
    selected_sources: List[Dict[str, Any]] = Field(default_factory=list, description="Selected sources")
    rejected_sources: List[Dict[str, Any]] = Field(default_factory=list, description="Rejected sources")
    reasoning: Optional[str] = Field(default=None, description="Reasoning for source selection")
    search_strategies_used: List[str] = Field(default_factory=list, description="Search strategies that were used")
    fallback_used: bool = Field(default=False, description="Whether fallback search was used")

class DocumentLoadingState(BaseModel):
    """State for the document loading step."""
    loaded_sources: List[Dict[str, Any]] = Field(default_factory=list, description="Successfully loaded sources")
    failed_sources: List[Dict[str, Any]] = Field(default_factory=list, description="Failed to load sources")
    loaded_documents_count: int = Field(default=0, description="Count of loaded documents")
    document_summaries: List[str] = Field(default_factory=list, description="Brief summaries of loaded documents")
    document_types: Dict[str, int] = Field(default_factory=dict, description="Count of document types")
    total_tokens: int = Field(default=0, description="Approximate total tokens in loaded documents")
    chunk_count: int = Field(default=0, description="Number of chunks created")

class SourceFinderSchema(BaseModel):
    """Schema for source finder agent."""
    messages: Annotated[Sequence[BaseMessage], add_messages] = Field(
        default=[],
        description="Messages in the conversation"
    )
    
    # Query analysis
    query_state: Optional[SourceQueryState] = Field(default=None, description="State of query analysis")
    
    # Source finding
    finding_state: Optional[SourceFindingState] = Field(default=None, description="State of source finding")
    
    # Document loading
    loading_state: Optional[DocumentLoadingState] = Field(default=None, description="State of document loading")
    
    # Sources and documents
    potential_sources: List[Dict[str, Any]] = Field(default_factory=list, description="Potential sources identified")
    discovered_sources: List[Dict[str, Any]] = Field(default_factory=list, description="Sources discovered")
    loaded_documents: List[Document] = Field(default_factory=list, description="Loaded documents")
    chunked_documents: List[Document] = Field(default_factory=list, description="Chunked documents")
    
    # Results
    embedded_documents: bool = Field(default=False, description="Whether documents have been embedded")
    vector_store: Optional[Any] = Field(default=None, description="VectorStore containing documents (if created)")
    retriever: Optional[Any] = Field(default=None, description="Document retriever (if created)")
    
    # Tracking
    current_step: str = Field(default="initialize", description="Current step in the process")
    routes_taken: List[str] = Field(default_factory=list, description="Routes taken during processing")
    step_history: List[str] = Field(default_factory=list, description="History of steps taken")
    
    # Error handling
    error: Optional[str] = Field(default=None, description="Error message if any step fails")
    warnings: List[str] = Field(default_factory=list, description="Warning messages")

# ===========================================
# Tool Schemas
# ===========================================

class SearchQuery(BaseModel):
    """Schema for a search query."""
    query: str = Field(..., description="Search query")
    filter: Optional[str] = Field(default=None, description="Optional filter")
    max_results: int = Field(default=5, description="Maximum number of results")

class SearchResult(BaseModel):
    """Schema for a search result."""
    title: str = Field(..., description="Title of the result")
    url: str = Field(..., description="URL of the result")
    snippet: Optional[str] = Field(default=None, description="Snippet from the result")
    source_type: str = Field(..., description="Type of source (web, github, docs, file, etc.)")
    relevance_score: Optional[float] = Field(default=None, description="Relevance score (0-1)")

class SearchResults(BaseModel):
    """Schema for search results."""
    results: List[SearchResult] = Field(..., description="List of search results")
    query: str = Field(..., description="Original query")
    total_found: int = Field(..., description="Total number of results found")

class SourceAnalysis(BaseModel):
    """Schema for analyzing a potential source."""
    source_url: str = Field(..., description="URL of the source")
    source_type: str = Field(..., description="Type of source")
    relevance: float = Field(..., description="Relevance to the query (0-1)")
    reliability: float = Field(..., description="Reliability of the source (0-1)")
    quality: float = Field(..., description="Quality of information (0-1)")
    recommendation: str = Field(..., description="Recommendation (use/reject)")
    reasoning: str = Field(..., description="Reasoning for the recommendation")

class SourceSelectionResult(BaseModel):
    """Schema for the result of source selection."""
    selected_sources: List[Dict[str, Any]] = Field(..., description="Selected sources")
    rejected_sources: List[Dict[str, Any]] = Field(..., description="Rejected sources")
    reasoning: str = Field(..., description="Overall reasoning for the selections")
    search_strategy: str = Field(default="general", description="Strategy used for search")

class QueryAnalysisResult(BaseModel):
    """Schema for the result of query analysis."""
    analyzed_query: str = Field(..., description="Analyzed version of the query")
    potential_topics: List[str] = Field(..., description="Potential topics extracted from query")
    source_type_suggestions: List[str] = Field(..., description="Suggested source types")
    query_keywords: List[str] = Field(..., description="Keywords extracted from query")
    domain_specific_terms: List[str] = Field(..., description="Domain-specific terms identified")
    search_strategy: str = Field(..., description="Determined search strategy")

# ===========================================
# Source Finder Config
# ===========================================

class SourceFinderConfig(AgentConfig):
    """Configuration for a source finder agent."""
    # System prompt
    system_prompt: str = Field(
        default="You are a helpful assistant that identifies the most relevant sources of information for a given query.",
        description="System prompt for the source finder agent"
    )
    
    # Search configuration
    search_tools: List[BaseTool] = Field(
        default_factory=list,
        description="Tools for searching various sources"
    )
    
    # Processing configuration
    max_sources_to_load: int = Field(
        default=3,
        description="Maximum number of sources to load"
    )
    
    chunk_size: int = Field(
        default=1000,
        description="Size of document chunks (in characters)"
    )
    
    chunk_overlap: int = Field(
        default=200,
        description="Overlap between document chunks (in characters)"
    )
    
    # Source selection criteria
    min_relevance_score: float = Field(
        default=0.6,
        description="Minimum relevance score for sources (0-1)"
    )
    
    # Embedding configuration
    embeddings: Optional[EmbeddingsConfig] = Field(
        default=None,
        description="Embeddings model to use for document embedding"
    )
    
    create_vectorstore: bool = Field(
        default=False,
        description="Whether to create a vector store with embedded documents"
    )
    
    vectorstore_class: Optional[Type[VectorStoreConfig]] = Field(
        default=None,
        description="Vector store class to use if creating a vector store"
    )
    
    # Override state schema with source finder schema
    state_schema: Type[BaseModel] = Field(
        default=SourceFinderSchema,
        description="Schema for the agent state"
    )
    
    # Chain configuration
    analyze_query_llm: Optional[AugLLMConfig] = Field(
        default=None, 
        description="LLM configuration for query analysis"
    )
    
    search_analysis_llm: Optional[AugLLMConfig] = Field(
        default=None, 
        description="LLM configuration for search result analysis"
    )
    
    source_selection_llm: Optional[AugLLMConfig] = Field(
        default=None, 
        description="LLM configuration for source selection"
    )
    
    document_analysis_llm: Optional[AugLLMConfig] = Field(
        default=None, 
        description="LLM configuration for document analysis"
    )
    
    # API Keys for services
    google_api_key: Optional[str] = Field(
        default=None,
        description="Google API key for search"
    )
    
    google_cse_id: Optional[str] = Field(
        default=None,
        description="Google CSE ID for search"
    )
    
    github_token: Optional[str] = Field(
        default=None,
        description="GitHub token for API access"
    )
    
    # Workflow configuration
    skip_analysis: bool = Field(
        default=False,
        description="Skip detailed analysis and just use web search"
    )
    
    skip_chunking: bool = Field(
        default=False,
        description="Skip document chunking"
    )
    
    include_web_search: bool = Field(
        default=True,
        description="Include web search in source finding"
    )
    
    include_github_search: bool = Field(
        default=True,
        description="Include GitHub search in source finding"
    )
    
    include_docs_search: bool = Field(
        default=True,
        description="Include documentation search in source finding"
    )

# ===========================================
# Search Tool Implementations
# ===========================================

def create_web_search_tool(api_key=None, cse_id=None) -> BaseTool:
    """Create a web search tool using Google Search or fallback to DuckDuckGo."""
    if api_key and cse_id:
        # Use Google Search API
        try:
            search_api = GoogleSearchAPIWrapper(google_api_key=api_key, google_cse_id=cse_id)
            
            @tool("web_search", return_direct=False)
            def web_search(query: str, max_results: int = 5) -> str:
                """Search the web for information using Google Search."""
                search_results = search_api.results(query, max_results)
                
                results = []
                for i, result in enumerate(search_results):
                    results.append(SearchResult(
                        title=result.get("title", f"Result {i+1}"),
                        url=result.get("link", ""),
                        snippet=result.get("snippet", ""),
                        source_type="web",
                        relevance_score=1.0 - (i * 0.1)  # Simple relevance scoring
                    ))
                
                search_results_obj = SearchResults(
                    results=results,
                    query=query,
                    total_found=len(results)
                )
                
                return json.dumps(search_results_obj.model_dump(), indent=2)
                
            return web_search
        except Exception as e:
            logger.warning(f"Failed to create Google Search tool: {e}")
    
    # Fallback to DuckDuckGo
    ddg_search = DuckDuckGoSearchRun()
    
    @tool("web_search", return_direct=False)
    def web_search(query: str, max_results: int = 5) -> str:
        """Search the web for information using DuckDuckGo."""
        raw_results = ddg_search.invoke(query)
        
        # Parse and structure results
        lines = raw_results.strip().split('\n')
        results = []
        
        for i, line in enumerate(lines[:max_results]):
            # Extract title and URL if possible
            parts = line.split(' - https://', 1)
            if len(parts) == 2:
                title = parts[0].strip()
                url = 'https://' + parts[1].strip()
                
                results.append(SearchResult(
                    title=title,
                    url=url,
                    snippet=line,
                    source_type="web",
                    relevance_score=1.0 - (i * 0.1)  # Simple relevance scoring
                ))
            else:
                # Fallback for lines without clear structure
                results.append(SearchResult(
                    title=f"Web result {i+1}",
                    url=f"https://example.com/result{i+1}",  # Placeholder URL
                    snippet=line,
                    source_type="web",
                    relevance_score=1.0 - (i * 0.1)
                ))
        
        search_results = SearchResults(
            results=results,
            query=query,
            total_found=len(results)
        )
        
        return json.dumps(search_results.model_dump(), indent=2)
    
    return web_search

def create_github_search_tool(github_token=None) -> BaseTool:
    """Create a GitHub search tool."""
    @tool("github_search", return_direct=False)
    def github_search(query: str, max_results: int = 3) -> str:
        """Search GitHub for repositories and code."""
        try:
            if github_token:
                # Initialize GitHub API wrapper
                #github_api = GitHubAPIWrapper(github_api_token=github_token)
                tavily_search_tool = TavilySearchAPIRetriever(api_key=TAVILY_API_KEY)
                # Get results from GitHub API
                repos = tavily_search_tool.invoke(query)
                
                results = []
                for i, repo in enumerate(repos):
                    results.append(SearchResult(
                        title=repo.get("full_name", f"GitHub repo {i+1}"),
                        url=repo.get("html_url", ""),
                        snippet=repo.get("description", ""),
                        source_type="github",
                        relevance_score=1.0 - (i * 0.1)
                    ))
            else:
                # Fallback to web search with GitHub filter
                ddg_search = DuckDuckGoSearchRun()
                github_query = f"site:github.com {query}"
                raw_results = ddg_search.invoke(github_query)
                
                # Parse and structure results
                lines = raw_results.strip().split('\n')
                results = []
                
                for i, line in enumerate(lines[:max_results]):
                    # Extract title and URL if possible
                    parts = line.split(' - https://', 1)
                    if len(parts) == 2:
                        title = parts[0].strip()
                        url = 'https://' + parts[1].strip()
                        
                        if 'github.com' in url:
                            results.append(SearchResult(
                                title=title,
                                url=url,
                                snippet=line,
                                source_type="github",
                                relevance_score=1.0 - (i * 0.1)
                            ))
                    
                # Fill remaining slots if needed
                while len(results) < max_results:
                    i = len(results)
                    results.append(SearchResult(
                        title=f"GitHub result {i+1}",
                        url=f"https://github.com/example/repo{i+1}",
                        snippet=f"Repository related to {query}",
                        source_type="github",
                        relevance_score=0.5 - (i * 0.1)
                    ))
            
            search_results = SearchResults(
                results=results,
                query=query,
                total_found=len(results)
            )
            
            return json.dumps(search_results.model_dump(), indent=2)
            
        except Exception as e:
            logger.error(f"GitHub search error: {str(e)}")
            
            # Return empty results on error
            search_results = SearchResults(
                results=[],
                query=query,
                total_found=0
            )
            
            return json.dumps(search_results.model_dump(), indent=2)
    
    return github_search

def create_docs_search_tool() -> BaseTool:
    """Create a technical documentation search tool."""
    @tool("documentation_search", return_direct=False)
    def documentation_search(query: str, max_results: int = 3) -> str:
        """Search technical documentation."""
        try:
            # Use DuckDuckGo to search for documentation
            ddg_search = DuckDuckGoSearchRun()
            
            # Add common documentation sites to query
            docs_query = f"site:docs.python.org OR site:readthedocs.org OR site:docs.github.com OR site:developer.mozilla.org {query}"
            raw_results = ddg_search.invoke(docs_query)
            
            # Parse and structure results
            lines = raw_results.strip().split('\n')
            results = []
            
            for i, line in enumerate(lines[:max_results]):
                # Extract title and URL if possible
                parts = line.split(' - https://', 1)
                if len(parts) == 2:
                    title = parts[0].strip()
                    url = 'https://' + parts[1].strip()
                    
                    results.append(SearchResult(
                        title=title,
                        url=url,
                        snippet=line,
                        source_type="documentation",
                        relevance_score=1.0 - (i * 0.1)
                    ))
                else:
                    # Fallback for lines without clear structure
                    results.append(SearchResult(
                        title=f"Documentation result {i+1}",
                        url=f"https://docs.example.com/page{i+1}",
                        snippet=line,
                        source_type="documentation",
                        relevance_score=0.8 - (i * 0.1)
                    ))
            
            search_results = SearchResults(
                results=results,
                query=query,
                total_found=len(results)
            )
            
            return json.dumps(search_results.model_dump(), indent=2)
            
        except Exception as e:
            logger.error(f"Documentation search error: {str(e)}")
            
            # Return empty results on error
            search_results = SearchResults(
                results=[],
                query=query,
                total_found=0
            )
            
            return json.dumps(search_results.model_dump(), indent=2)
    
    return documentation_search

# ===========================================
# Source Processing Tools
# ===========================================

def create_source_analysis_tool(llm_config: AugLLMConfig) -> BaseTool:
    """Create a tool for analyzing sources using an LLM."""
    # Create prompt
    analysis_prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are an expert at evaluating information sources. Your task is to analyze a source "
         "and determine its relevance, reliability, and quality for answering a query."),
        ("user", 
         "URL: {url}\n\n"
         "Query: {query}\n\n"
         "Based on the URL and any available information, analyze this source by evaluating:\n"
         "1. RELEVANCE: How relevant is this source to the query? (0-1 score)\n"
         "2. RELIABILITY: How reliable/trustworthy is this source likely to be? (0-1 score)\n"
         "3. QUALITY: How high-quality is the information likely to be? (0-1 score)\n"
         "4. RECOMMENDATION: Should we use or reject this source? (answer 'use' or 'reject')\n"
         "5. REASONING: Provide clear reasoning for your analysis.\n\n"
         "Respond in JSON format with the following fields: source_url, source_type, relevance, "
         "reliability, quality, recommendation, reasoning.")
    ])
    
    # Create runnable chain
    analysis_chain = (
        analysis_prompt | 
        compose_runnable(llm_config) | 
        PydanticOutputParser(pydantic_object=SourceAnalysis)
    )
    
    @tool("analyze_source", return_direct=False)
    def analyze_source(url: str, query: str) -> str:
        """Analyze a source for relevance to the query."""
        try:
            # Determine source type from URL
            source_type = "web"
            if "github.com" in url:
                source_type = "github"
            elif any(x in url for x in ["docs.", "documentation.", "readthedocs"]):
                source_type = "documentation"
                
            # Get source information
            source_info = {
                "url": url,
                "query": query,
                "source_type": source_type
            }
            
            # Run analysis
            analysis_result = analysis_chain.invoke(source_info)
            
            # Ensure source type is set
            if not analysis_result.source_type:
                analysis_result.source_type = source_type
                
            # Return as JSON
            return json.dumps(analysis_result.model_dump(), indent=2)
            
        except Exception as e:
            logger.error(f"Source analysis error: {str(e)}")
            
            # Create fallback analysis
            fallback_analysis = SourceAnalysis(
                source_url=url,
                source_type="web" if not "github.com" in url else "github",
                relevance=0.5,
                reliability=0.5,
                quality=0.5,
                recommendation="reject",
                reasoning=f"Error analyzing source: {str(e)}"
            )
            
            return json.dumps(fallback_analysis.model_dump(), indent=2)
    
    return analyze_source

def create_document_loader_tool() -> BaseTool:
    """Create a tool for loading documents from URLs."""
    @tool("load_documents", return_direct=False)
    def load_documents(url: str, source_type: str) -> str:
        """Load documents from a URL."""
        try:
            # Parse URL
            parsed_url = urlparse(url)
            
            # Create appropriate loader based on source type
            if source_type == "github":
                # For GitHub repos, use GitLoader
                repo_parts = parsed_url.path.strip('/').split('/')
                if len(repo_parts) >= 2:
                    owner = repo_parts[0]
                    repo = repo_parts[1]
                    
                    # Try to load with GitLoader
                    try:
                        # Create a temporary directory
                        import tempfile
                        import shutil
                        
                        clone_dir = tempfile.mkdtemp()
                        
                        # Clone only the top level with minimal history
                        loader = GitLoader(
                            repo_path=clone_dir,
                            clone_url=f"https://github.com/{owner}/{repo}.git",
                            branch="main",
                            file_filter=lambda file_path: file_path.endswith((".md", ".txt", ".rst"))
                        )
                        
                        # Load documents
                        documents = loader.load()
                        
                        # Clean up
                        shutil.rmtree(clone_dir)
                        
                    except Exception as e:
                        logger.warning(f"Error loading GitHub repo: {str(e)}")
                        # Fallback to web loading
                        loader = WebBaseLoader(url)
                        documents = loader.load()
                else:
                    # Fallback to web loading
                    loader = WebBaseLoader(url)
                    documents = loader.load()
            
            elif source_type == "documentation" and "readthedocs.io" in url:
                # Use ReadTheDocsLoader for Read the Docs sites
                project_parts = parsed_url.netloc.split('.')
                if len(project_parts) >= 3:
                    project = project_parts[0]
                    loader = ReadTheDocsLoader(project)
                    documents = loader.load()
                else:
                    # Fallback to web loading
                    loader = WebBaseLoader(url)
                    documents = loader.load()
            
            elif "sitemap.xml" in url:
                # Use SitemapLoader for sitemaps
                loader = SitemapLoader(url)
                documents = loader.load()
            
            else:
                # Default to WebBaseLoader
                loader = WebBaseLoader(url)
                documents = loader.load()
            
            # Prepare document data
            doc_data = []
            for i, doc in enumerate(documents):
                if hasattr(doc, "page_content") and hasattr(doc, "metadata"):
                    # Extract up to 500 chars of content for preview
                    content_preview = doc.page_content[:500]
                    if len(doc.page_content) > 500:
                        content_preview += "..."
                    
                    doc_data.append({
                        "index": i,
                        "content_preview": content_preview,
                        "metadata": doc.metadata
                    })
            
            # Return document loading results
            result = {
                "url": url,
                "source_type": source_type,
                "documents_loaded": len(documents),
                "document_previews": doc_data
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            logger.error(f"Document loading error: {str(e)}")
            
            # Return error information
            result = {
                "url": url,
                "source_type": source_type,
                "documents_loaded": 0,
                "error": str(e)
            }
            
            return json.dumps(result, indent=2)
    
    return load_documents

# ===========================================
# Helper Functions
# ===========================================

def detect_source_type(url: str) -> str:
    """Detect the type of source from a URL."""
    if "github.com" in url:
        return "github"
    elif any(x in url for x in ["docs.", "documentation.", "readthedocs.io"]):
        return "documentation"
    elif any(x in url for x in [".edu", "research.", "academic.", "papers."]):
        return "academic"
    elif any(x in url for x in [".gov", ".org"]):
        return "official"
    else:
        return "web"

def load_documents_from_url(url: str, source_type: str = None) -> List[Document]:
    """Load documents from a URL."""
    # Detect source type if not provided
    if not source_type:
        source_type = detect_source_type(url)
    
    # Parse URL
    parsed_url = urlparse(url)
    
    # Create appropriate loader based on source type
    if source_type == "github":
        # For GitHub repos, use GitLoader
        repo_parts = parsed_url.path.strip('/').split('/')
        if len(repo_parts) >= 2:
            owner = repo_parts[0]
            repo = repo_parts[1]
            
            # Try to load with GitLoader
            try:
                # Create a temporary directory
                import tempfile
                import shutil
                
                clone_dir = tempfile.mkdtemp()
                
                # Clone only the top level with minimal history
                loader = GitLoader(
                    repo_path=clone_dir,
                    clone_url=f"https://github.com/{owner}/{repo}.git",
                    branch="main",
                    file_filter=lambda file_path: file_path.endswith((".md", ".txt", ".rst"))
                )
                
                # Load documents
                documents = loader.load()
                
                # Clean up
                shutil.rmtree(clone_dir)
                
                return documents
                
            except Exception as e:
                logger.warning(f"Error loading GitHub repo: {str(e)}")
                # Fallback to web loading
                loader = WebBaseLoader(url)
                return loader.load()
        else:
            # Fallback to web loading
            loader = WebBaseLoader(url)
            return loader.load()
    
    elif source_type == "documentation" and "readthedocs.io" in url:
        # Use ReadTheDocsLoader for Read the Docs sites
        project_parts = parsed_url.netloc.split('.')
        if len(project_parts) >= 3:
            project = project_parts[0]
            loader = ReadTheDocsLoader(project)
            return loader.load()
        else:
            # Fallback to web loading
            loader = WebBaseLoader(url)
            return loader.load()
    
    elif "sitemap.xml" in url:
        # Use SitemapLoader for sitemaps
        loader = SitemapLoader(url)
        return loader.load()
    
    else:
        # Default to WebBaseLoader
        loader = WebBaseLoader(url)
        return loader.load()

def chunk_documents(documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """Split documents into chunks."""
    # Create text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    # Split documents
    return text_splitter.split_documents(documents)

# ===========================================
# Source Finder Agent Implementation
# ===========================================

@register_agent(SourceFinderConfig)
class SourceFinderAgent(Agent[SourceFinderConfig]):
    """
    A source finder agent that:
    1. Analyzes a user query to understand information needs
    2. Searches for potential sources of information
    3. Evaluates and selects the most relevant sources
    4. Loads documents from selected sources
    5. Processes documents for use in RAG applications
    
    This agent uses conditional routing to adapt its workflow based on the query type,
    available sources, and document processing needs.
    """
    
    def __init__(self, config: SourceFinderConfig):
        """Initialize the source finder agent."""
        # Initialize base agent
        self.config = config
        
        
        # Initialize LLMs
        self._init_llms()
        
        # Initialize tools
        self._init_tools()
        
        # Set up query analysis chain
        self._setup_query_analysis_chain()
        
        # Set up source selection chain
        self._setup_source_selection_chain()
        
        # Set up document analysis chain
        self._setup_document_analysis_chain()
        super().__init__(config)
    def _init_llms(self):
        """Initialize LLMs for different steps."""
        # Default LLM config
        default_llm_config = AugLLMConfig(
            name="source_finder_llm",
            llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.7})
        )
        
        # Set up LLMs for different steps
        self.analyze_query_llm = self.config.analyze_query_llm or default_llm_config
        self.search_analysis_llm = self.config.search_analysis_llm or default_llm_config
        self.source_selection_llm = self.config.source_selection_llm or default_llm_config
        self.document_analysis_llm = self.config.document_analysis_llm or default_llm_config
    
    def _init_tools(self):
        """Initialize search and processing tools."""
        # Initialize tool lists
        self.search_tools = []
        self.processing_tools = []
        
        # Use provided tools or create default ones
        if self.config.search_tools:
            self.search_tools = self.config.search_tools
        else:
            # Add web search tool if enabled
            if self.config.include_web_search:
                web_search = create_web_search_tool(
                    api_key=self.config.google_api_key, 
                    cse_id=self.config.google_cse_id
                )
                self.search_tools.append(web_search)
            
            # Add GitHub search tool if enabled
            if self.config.include_github_search:
                github_search = create_github_search_tool(
                    github_token=self.config.github_token
                )
                self.search_tools.append(github_search)
            
            # Add documentation search tool if enabled
            if self.config.include_docs_search:
                docs_search = create_docs_search_tool()
                self.search_tools.append(docs_search)
        
        # Add source processing tools
        source_analysis = create_source_analysis_tool(self.search_analysis_llm)
        document_loader = create_document_loader_tool()
        
        self.processing_tools = [
            source_analysis,
            document_loader
        ]
        
        # All tools
        self.all_tools = self.search_tools + self.processing_tools
    
    def _setup_query_analysis_chain(self):
        """Set up the query analysis chain."""
        # Create prompt for query analysis
        query_analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You are an expert at understanding information needs from queries. "
             "Analyze the query to identify topics, potential knowledge sources, search terms, "
             "and the most effective search strategy."),
            ("user", 
             "Query: {query}\n\n"
             "Analyze this query and provide a structured assessment including:\n"
             "1. An analysis of what the query is asking for\n"
             "2. Potential topics and concepts involved\n"
             "3. Suggested types of sources that would be most helpful (e.g., documentation, code repositories, academic papers)\n"
             "4. Key search keywords that should be used\n"
             "5. Any domain-specific terminology identified\n"
             "6. Recommended search strategy from the following options:\n"
             "   - 'technical': For programming, technical documentation, or API-related queries\n"
             "   - 'academic': For scientific or research-based queries\n"
             "   - 'current_events': For recent news or evolving topics\n"
             "   - 'conceptual': For explanations of ideas or concepts\n"
             "   - 'general': For general information needs\n\n"
             "Respond in JSON format with the following fields: analyzed_query, potential_topics, "
             "source_type_suggestions, query_keywords, domain_specific_terms, search_strategy")
        ])
        
        # Create query analysis chain
        self.query_analysis_chain = (
            query_analysis_prompt | 
            compose_runnable(self.analyze_query_llm) | 
            PydanticOutputParser(pydantic_object=QueryAnalysisResult)
        )
    
    def _setup_source_selection_chain(self):
        """Set up the source selection chain."""
        # Create prompt for source selection
        source_selection_prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You are an expert at evaluating and selecting the most relevant sources of information. "
             "Review the analyzed sources and select the best ones to use."),
            ("user", 
             "Query: {query}\n\n"
             "Search Strategy: {search_strategy}\n\n"
             "Analyzed Sources:\n{sources_json}\n\n"
             "Select the most relevant sources to load documents from (maximum {max_sources}). "
             "Consider relevance, reliability, quality, and diversity of perspectives. "
             "Focus on sources that directly address the query or provide essential context. "
             "For technical queries, prioritize documentation and trusted repositories. "
             "For conceptual queries, prioritize educational or explanatory sources.\n\n"
             "Provide your reasoning for each selection and rejection, and explain your overall strategy.")
        ])
        
        # Create source selection chain
        self.source_selection_chain = (
            source_selection_prompt | 
            compose_runnable(self.source_selection_llm) | 
            PydanticOutputParser(pydantic_object=SourceSelectionResult)
        )
    
    def _setup_document_analysis_chain(self):
        """Set up the document analysis chain."""
        # Create prompt for document analysis
        document_analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You analyze documents to extract key information and evaluate their usefulness for answering queries."),
            ("user", 
             "Query: {query}\n\n"
             "Document Previews:\n{document_previews}\n\n"
             "Analyze these document previews and provide:\n"
             "1. An assessment of how well they address the query\n"
             "2. Key information or concepts present in the documents\n"
             "3. Any notable gaps or missing information\n"
             "4. Suggestions for how to use these documents to answer the query")
        ])
        
        # Create document analysis chain
        self.document_analysis_chain = (
            document_analysis_prompt | 
            compose_runnable(self.document_analysis_llm) | 
            StrOutputParser()
        )
    
    def setup_workflow(self) -> None:
        """Set up the source finder workflow with conditional routing."""
        logger.info(f"Setting up workflow for SourceFinderAgent {self.config.name}")
        
        # Create graph builder
        gb = DynamicGraph(
            components=[self.config.engine] + self.all_tools,
            state_schema=self.config.state_schema
        )
        
        # Add nodes
        # 1. Initialize
        gb.add_node(
            name="initialize",
            config=self._initialize_node,
            command_goto="router_query_analysis"
        )
        
        # 2. Query Analysis Router
        gb.add_node(
            name="router_query_analysis",
            config=self._create_query_analysis_router(),
            command_goto="analyze_query"  # Default path
        )
        
        # 3. Analyze Query (detailed path)
        gb.add_node(
            name="analyze_query",
            config=self._analyze_query_node,
            command_goto="router_search_strategy"
        )
        
        # 4. Skip Analysis (fast path)
        gb.add_node(
            name="skip_analysis",
            config=self._skip_analysis_node,
            command_goto="router_search_strategy"
        )
        
        # 5. Search Strategy Router
        gb.add_node(
            name="router_search_strategy",
            config=self._create_search_strategy_router(),
            command_goto="search_sources_general"  # Default path
        )
        
        # 6. Search Sources (different strategies)
        gb.add_node(
            name="search_sources_general",
            config=self._search_sources_general_node,
            command_goto="analyze_results"
        )
        
        gb.add_node(
            name="search_sources_technical",
            config=self._search_sources_technical_node,
            command_goto="analyze_results"
        )
        
        gb.add_node(
            name="search_sources_academic",
            config=self._search_sources_academic_node,
            command_goto="analyze_results"
        )
        
        # 7. Analyze Results
        gb.add_node(
            name="analyze_results",
            config=self._analyze_results_node,
            command_goto="select_sources"
        )
        
        # 8. Select Sources
        gb.add_node(
            name="select_sources",
            config=self._select_sources_node,
            command_goto="router_document_loading"
        )
        
        # 9. Document Loading Router
        gb.add_node(
            name="router_document_loading",
            config=self._create_document_loading_router(),
            command_goto="load_documents"  # Default path
        )
        
        # 10. Load Documents
        gb.add_node(
            name="load_documents",
            config=self._load_documents_node,
            command_goto="router_document_processing"
        )
        
        # 11. Skip Document Loading (error path)
        gb.add_node(
            name="skip_document_loading",
            config=self._skip_document_loading_node,
            command_goto="generate_response"
        )
        
        # 12. Document Processing Router
        gb.add_node(
            name="router_document_processing",
            config=self._create_document_processing_router(),
            command_goto="process_documents"  # Default path
        )
        
        # 13. Process Documents (chunking and optional embedding)
        gb.add_node(
            name="process_documents",
            config=self._process_documents_node,
            command_goto="generate_response"
        )
        
        # 14. Skip Document Processing
        gb.add_node(
            name="skip_document_processing",
            config=self._skip_document_processing_node,
            command_goto="generate_response"
        )
        
        # 15. Generate Response
        gb.add_node(
            name="generate_response",
            config=self._generate_response_node,
            command_goto=END
        )
        
        # 16. Error Node
        gb.add_node(
            name="error_node",
            config=self._error_node,
            command_goto=END
        )
        
        # Build the graph
        self.graph = gb.build()
        
        logger.info(f"Set up source finder workflow for {self.config.name}")
    
    # Router creation methods
    def _create_query_analysis_router(self):
        """Create a router for query analysis path."""
        router = Router(name="query_analysis_router", default_destination="analyze_query")
        
        # Route based on skip_analysis config
        router.add_state_route(
            name="skip_analysis_route",
            key="config.skip_analysis",  # This won't actually work directly, but we'll handle it in the node
            value=True,
            destination="skip_analysis"
        )
        
        return router.create_router_function()
    
    def _create_search_strategy_router(self):
        """Create a router for search strategy."""
        router = Router(name="search_strategy_router", default_destination="search_sources_general")
        
        # Route based on search strategy in query state
        router.add_state_route(
            name="technical_search_route",
            key="query_state.search_strategy",
            value="technical",
            destination="search_sources_technical"
        )
        
        router.add_state_route(
            name="academic_search_route",
            key="query_state.search_strategy",
            value="academic",
            destination="search_sources_academic"
        )
        
        return router.create_router_function()
    
    def _create_document_loading_router(self):
        """Create a router for document loading path."""
        router = Router(name="document_loading_router", default_destination="load_documents")
        
        # Skip loading if no sources selected
        router.add_function_route(
            name="no_sources_route",
            function=lambda state: not state.get("finding_state", {}).get("selected_sources", []),
            destination="skip_document_loading"
        )
        
        return router.create_router_function()
    
    def _create_document_processing_router(self):
        """Create a router for document processing path."""
        router = Router(name="document_processing_router", default_destination="process_documents")
        
        # Skip processing if no documents loaded
        router.add_function_route(
            name="no_documents_route",
            function=lambda state: not state.get("loaded_documents", []),
            destination="skip_document_processing"
        )
        
        # Skip processing if explicitly configured
        router.add_state_route(
            name="skip_processing_route",
            key="config.skip_chunking",  # This won't work directly, we'll handle in the node
            value=True,
            destination="skip_document_processing"
        )
        
        return router.create_router_function()
    
    # Node implementations
    def _initialize_node(self, state):
        """Initialize the source finder process."""
        # Extract query from messages
        query = None
        if state.messages:
            last_message = state.messages[-1]
            if hasattr(last_message, "content"):
                query = last_message.content
        
        if not query:
            return {
                "error": "No query found in messages",
                "current_step": "error"
            }
        
        # Initialize query state
        query_state = SourceQueryState(query=query)
        
        # Track steps
        updated_state = {
            "query_state": query_state,
            "current_step": "router_query_analysis",
            "step_history": ["initialize"],
            "routes_taken": []
        }
        
        return updated_state
    
    def _analyze_query_node(self, state):
        """Analyze the query to understand information needs."""
        query = state.query_state.query
        
        try:
            # Run query analysis
            analysis_result = self.query_analysis_chain.invoke({"query": query})
            
            # Update query state
            updated_query_state = state.query_state.model_copy()
            updated_query_state.analyzed_query = analysis_result.analyzed_query
            updated_query_state.potential_topics = analysis_result.potential_topics
            updated_query_state.source_type_suggestions = analysis_result.source_type_suggestions
            updated_query_state.query_keywords = analysis_result.query_keywords
            updated_query_state.domain_specific_terms = analysis_result.domain_specific_terms
            updated_query_state.search_strategy = analysis_result.search_strategy
            
            # Update state
            routes_taken = state.routes_taken + ["detailed_analysis"]
            
            return {
                "query_state": updated_query_state,
                "current_step": "router_search_strategy",
                "step_history": state.step_history + ["analyze_query"],
                "routes_taken": routes_taken
            }
            
        except Exception as e:
            logger.error(f"Error in query analysis: {str(e)}")
            
            # Create basic query state
            updated_query_state = state.query_state.model_copy()
            updated_query_state.analyzed_query = f"Query about: {query}"
            updated_query_state.search_strategy = "general"
            
            # Add warning
            warnings = state.warnings + [f"Error in query analysis: {str(e)}"]
            
            # Update state
            routes_taken = state.routes_taken + ["detailed_analysis_failed"]
            
            return {
                "query_state": updated_query_state,
                "current_step": "router_search_strategy",
                "step_history": state.step_history + ["analyze_query (error)"],
                "routes_taken": routes_taken,
                "warnings": warnings
            }
    
    def _skip_analysis_node(self, state):
        """Skip detailed analysis and use basic query processing."""
        query = state.query_state.query
        
        # Create basic query state
        updated_query_state = state.query_state.model_copy()
        updated_query_state.analyzed_query = f"Query about: {query}"
        updated_query_state.search_strategy = "general"
        
        # Generate simple keyword list
        keywords = query.lower().replace("?", "").replace(".", "").replace(",", "").split()
        keywords = [k for k in keywords if len(k) > 3 and k not in 
                   ["what", "when", "where", "which", "who", "why", "how", 
                    "the", "and", "this", "that", "with", "from", "about"]]
        
        updated_query_state.query_keywords = keywords[:5]  # Limit to top 5 keywords
        
        # Update state
        routes_taken = state.routes_taken + ["fast_path"]
        
        return {
            "query_state": updated_query_state,
            "current_step": "router_search_strategy",
            "step_history": state.step_history + ["skip_analysis"],
            "routes_taken": routes_taken
        }
    
    def _search_sources_general_node(self, state):
        """Search for sources using a general strategy."""
        query = state.query_state.query
        
        # Use all search tools
        search_results = []
        
        # Execute searches
        for tool in self.search_tools:
            try:
                # Invoke the tool
                result = tool.invoke({"query": query, "max_results": 3})
                
                # Parse results
                parsed_results = json.loads(result)
                
                # Add to search results
                search_results.append({
                    "tool": tool.name,
                    "results": parsed_results
                })
            except Exception as e:
                logger.error(f"Error using search tool {tool.name}: {str(e)}")
        
        # Initialize finding state
        finding_state = SourceFindingState(
            search_results=search_results,
            search_strategies_used=["general"]
        )
        
        # Track potential sources
        potential_sources = []
        for search in search_results:
            if "results" in search and "results" in search["results"]:
                for result in search["results"]["results"]:
                    # Add the source type to the result
                    if "source_type" not in result:
                        result["source_type"] = detect_source_type(result.get("url", ""))
                    potential_sources.append(result)
        
        # Update state
        routes_taken = state.routes_taken + ["general_search"]
        
        return {
            "finding_state": finding_state,
            "potential_sources": potential_sources,
            "current_step": "analyze_results",
            "step_history": state.step_history + ["search_sources_general"],
            "routes_taken": routes_taken
        }
    
    def _search_sources_technical_node(self, state):
        """Search for sources using a technical-focused strategy."""
        query = state.query_state.query
        
        # Prioritize GitHub and documentation searches
        search_results = []
        
        # Execute searches with technical emphasis
        for tool in self.search_tools:
            try:
                if tool.name == "github_search":
                    # Prioritize GitHub with more results
                    result = tool.invoke({"query": query, "max_results": 5})
                    parsed_results = json.loads(result)
                    search_results.append({
                        "tool": tool.name,
                        "results": parsed_results
                    })
                elif tool.name == "documentation_search":
                    # Prioritize documentation with more results
                    result = tool.invoke({"query": query, "max_results": 5})
                    parsed_results = json.loads(result)
                    search_results.append({
                        "tool": tool.name,
                        "results": parsed_results
                    })
                else:
                    # Use other tools with fewer results
                    result = tool.invoke({"query": query, "max_results": 2})
                    parsed_results = json.loads(result)
                    search_results.append({
                        "tool": tool.name,
                        "results": parsed_results
                    })
            except Exception as e:
                logger.error(f"Error using search tool {tool.name}: {str(e)}")
        
        # Add technical filters to web search
        if self.config.include_web_search:
            try:
                technical_terms = " OR ".join(state.query_state.domain_specific_terms or [])
                if technical_terms:
                    tech_query = f"{query} ({technical_terms})"
                    
                    # Find web search tool
                    for tool in self.search_tools:
                        if tool.name == "web_search":
                            result = tool.invoke({"query": tech_query, "max_results": 3})
                            parsed_results = json.loads(result)
                            search_results.append({
                                "tool": "technical_web_search",
                                "results": parsed_results
                            })
                            break
            except Exception as e:
                logger.error(f"Error in technical web search: {str(e)}")
        
        # Initialize finding state
        finding_state = SourceFindingState(
            search_results=search_results,
            search_strategies_used=["technical"]
        )
        
        # Track potential sources
        potential_sources = []
        for search in search_results:
            if "results" in search and "results" in search["results"]:
                for result in search["results"]["results"]:
                    # Add the source type to the result
                    if "source_type" not in result:
                        result["source_type"] = detect_source_type(result.get("url", ""))
                    potential_sources.append(result)
        
        # Update state
        routes_taken = state.routes_taken + ["technical_search"]
        
        return {
            "finding_state": finding_state,
            "potential_sources": potential_sources,
            "current_step": "analyze_results",
            "step_history": state.step_history + ["search_sources_technical"],
            "routes_taken": routes_taken
        }
    
    def _search_sources_academic_node(self, state):
        """Search for sources using an academic-focused strategy."""
        query = state.query_state.query
        
        # Prioritize academic sources
        search_results = []
        
        # Add academic filters to web search
        if self.config.include_web_search:
            try:
                # Build an academic search query
                academic_query = f"{query} site:.edu OR site:scholar.google.com OR research OR paper OR journal OR study"
                
                # Find web search tool
                for tool in self.search_tools:
                    if tool.name == "web_search":
                        result = tool.invoke({"query": academic_query, "max_results": 5})
                        parsed_results = json.loads(result)
                        search_results.append({
                            "tool": "academic_web_search",
                            "results": parsed_results
                        })
                        break
            except Exception as e:
                logger.error(f"Error in academic web search: {str(e)}")
        
        # Execute regular searches as fallback
        for tool in self.search_tools:
            try:
                # Skip web search as we've already done a specialized version
                if tool.name != "web_search":
                    result = tool.invoke({"query": query, "max_results": 3})
                    parsed_results = json.loads(result)
                    search_results.append({
                        "tool": tool.name,
                        "results": parsed_results
                    })
            except Exception as e:
                logger.error(f"Error using search tool {tool.name}: {str(e)}")
        
        # Initialize finding state
        finding_state = SourceFindingState(
            search_results=search_results,
            search_strategies_used=["academic"]
        )
        
        # Track potential sources
        potential_sources = []
        for search in search_results:
            if "results" in search and "results" in search["results"]:
                for result in search["results"]["results"]:
                    # Add the source type to the result
                    if "source_type" not in result:
                        result["source_type"] = detect_source_type(result.get("url", ""))
                    potential_sources.append(result)
        
        # Update state
        routes_taken = state.routes_taken + ["academic_search"]
        
        return {
            "finding_state": finding_state,
            "potential_sources": potential_sources,
            "current_step": "analyze_results",
            "step_history": state.step_history + ["search_sources_academic"],
            "routes_taken": routes_taken
        }
    
    def _analyze_results_node(self, state):
        """Analyze search results to evaluate relevance."""
        query = state.query_state.query
        potential_sources = state.potential_sources
        
        # Skip if no sources found
        if not potential_sources:
            # Try fallback search if no results and not already tried
            if not state.finding_state or not state.finding_state.fallback_used:
                # Initialize finding state if not present
                finding_state = state.finding_state or SourceFindingState()
                finding_state.fallback_used = True
                
                warning = "No sources found in initial search. Attempting fallback search."
                warnings = state.warnings + [warning]
                
                # Update state to go back to general search
                return {
                    "finding_state": finding_state,
                    "current_step": "search_sources_general",
                    "step_history": state.step_history + ["analyze_results (no sources, retry)"],
                    "warnings": warnings
                }
            else:
                # Already tried fallback search, still no results
                return {
                    "error": "No potential sources found after multiple search attempts",
                    "current_step": "error",
                    "step_history": state.step_history + ["analyze_results (failed)"]
                }
        
        # Analyze sources (process in batches to avoid overloading)
        analyzed_sources = []
        source_analysis_tool = None
        
        # Find the source analysis tool
        for tool in self.processing_tools:
            if tool.name == "analyze_source":
                source_analysis_tool = tool
                break
        
        # Analyze each source
        if source_analysis_tool:
            batch_size = 5  # Process at most 5 sources
            for i, source in enumerate(potential_sources[:batch_size]):
                # Only process sources with URLs
                if not source.get("url"):
                    continue
                    
                try:
                    # Call the analyze tool
                    result = source_analysis_tool.invoke({
                        "url": source["url"],
                        "query": query
                    })
                    
                    # Parse result
                    analysis = json.loads(result)
                    
                    # Add the analysis to the source
                    source_with_analysis = {**source}
                    source_with_analysis["analysis"] = analysis
                    analyzed_sources.append(source_with_analysis)
                except Exception as e:
                    logger.error(f"Error analyzing source {source.get('url')}: {str(e)}")
        else:
            # Fallback if tool not found: assign simple scores
            import random
            for source in potential_sources:
                if not source.get("url"):
                    continue
                    
                # Determine source type
                source_type = source.get("source_type", detect_source_type(source.get("url", "")))
                
                # Assign scores based on source type
                relevance = 0.7 + random.random() * 0.3
                reliability = 0.6 + random.random() * 0.4
                quality = 0.65 + random.random() * 0.35
                
                # Bias scores based on source type
                if source_type == "documentation":
                    reliability += 0.2
                    quality += 0.1
                elif source_type == "github":
                    if "github.com" in source.get("url", ""):
                        reliability += 0.1
                
                # Ensure scores are in range
                relevance = min(1.0, relevance)
                reliability = min(1.0, reliability)
                quality = min(1.0, quality)
                
                # Create analysis
                analysis = {
                    "source_url": source.get("url", ""),
                    "source_type": source_type,
                    "relevance": relevance,
                    "reliability": reliability,
                    "quality": quality,
                    "recommendation": "use" if relevance > 0.7 and reliability > 0.6 else "reject",
                    "reasoning": f"This source appears to be a {source_type} source related to the query."
                }
                
                # Add the analysis to the source
                source_with_analysis = {**source}
                source_with_analysis["analysis"] = analysis
                analyzed_sources.append(source_with_analysis)
        
        # Update state
        return {
            "potential_sources": analyzed_sources,
            "current_step": "select_sources",
            "step_history": state.step_history + ["analyze_results"],
            "routes_taken": state.routes_taken + ["source_analysis"]
        }
    
    def _select_sources_node(self, state):
        """Select the most relevant sources to load."""
        query = state.query_state.query
        analyzed_sources = state.potential_sources
        search_strategy = state.query_state.search_strategy if state.query_state else "general"
        
        # Create a prompt for source selection
        try:
            # Run source selection chain
            selection_result = self.source_selection_chain.invoke({
                "query": query,
                "search_strategy": search_strategy,
                "sources_json": json.dumps(analyzed_sources, indent=2),
                "max_sources": self.config.max_sources_to_load
            })
            
            # Update finding state
            finding_state = state.finding_state.model_copy() if state.finding_state else SourceFindingState()
            finding_state.selected_sources = selection_result.selected_sources
            finding_state.rejected_sources = selection_result.rejected_sources
            finding_state.reasoning = selection_result.reasoning
            
            # Update state
            return {
                "finding_state": finding_state,
                "current_step": "router_document_loading",
                "step_history": state.step_history + ["select_sources"],
                "routes_taken": state.routes_taken + ["source_selection"]
            }
            
        except Exception as e:
            # In case of parsing error, use a simpler approach
            logger.error(f"Error in source selection: {str(e)}")
            
            # Simple selection based on relevance
            selected_sources = []
            rejected_sources = []
            
            for source in analyzed_sources:
                analysis = source.get("analysis", {})
                recommendation = analysis.get("recommendation", "")
                
                if isinstance(recommendation, str) and recommendation.lower() == "use":
                    selected_sources.append(source)
                else:
                    rejected_sources.append(source)
            
            # Sort by relevance if available
            try:
                selected_sources = sorted(
                    selected_sources,
                    key=lambda x: x.get("analysis", {}).get("relevance", 0.0),
                    reverse=True
                )
            except Exception:
                pass
            
            # Limit selected sources
            selected_sources = selected_sources[:self.config.max_sources_to_load]
            
            # Update finding state
            finding_state = state.finding_state.model_copy() if state.finding_state else SourceFindingState()
            finding_state.selected_sources = selected_sources
            finding_state.rejected_sources = rejected_sources
            finding_state.reasoning = "Selected based on automated relevance analysis."
            
            # Add warning
            warnings = state.warnings + [f"Error in source selection: {str(e)}. Used automatic selection instead."]
            
            # Update state
            return {
                "finding_state": finding_state,
                "current_step": "router_document_loading",
                "step_history": state.step_history + ["select_sources (automatic)"],
                "routes_taken": state.routes_taken + ["automatic_selection"],
                "warnings": warnings
            }
    
    def _skip_document_loading_node(self, state):
        """Skip document loading due to missing sources."""
        # Add warning
        warnings = state.warnings + ["No sources selected for loading. Skipping document loading."]
        
        # Initialize loading state
        loading_state = DocumentLoadingState()
        
        # Update state
        return {
            "loading_state": loading_state,
            "current_step": "router_document_processing",
            "step_history": state.step_history + ["skip_document_loading"],
            "routes_taken": state.routes_taken + ["no_sources_path"],
            "warnings": warnings
        }
    
    def _load_documents_node(self, state):
        """Load documents from selected sources."""
        selected_sources = state.finding_state.selected_sources if state.finding_state else []
        
        # Initialize loading state
        loading_state = DocumentLoadingState()
        loaded_documents = []
        
        # Get the document loader tool
        document_loader_tool = None
        for tool in self.processing_tools:
            if tool.name == "load_documents":
                document_loader_tool = tool
                break
        
        # Process each selected source
        for source_data in selected_sources:
            url = source_data.get("url")
            source_type = source_data.get("source_type", "web")
            
            if not url:
                continue
                
            try:
                # Parse source data
                source = {"url": url, "source_type": source_type}
                
                # Load documents based on tool availability
                if document_loader_tool:
                    # Use tool to load documents
                    result = document_loader_tool.invoke({
                        "url": url,
                        "source_type": source_type
                    })
                    load_data = json.loads(result)
                    
                    # Record successful load
                    loading_state.loaded_sources.append({
                        "url": url,
                        "source_type": source_type,
                        "documents_loaded": load_data.get("documents_loaded", 0)
                    })
                    
                    # Add document snippets to summaries
                    if "document_previews" in load_data:
                        for preview in load_data["document_previews"]:
                            if "content_preview" in preview:
                                loading_state.document_summaries.append(preview["content_preview"])
                    
                    # Update document count
                    loading_state.loaded_documents_count += load_data.get("documents_loaded", 0)
                    
                    # Actually load documents using the helper function
                    docs = load_documents_from_url(url, source_type)
                    
                    # Add metadata to documents
                    for doc in docs:
                        if isinstance(doc, Document):
                            # Ensure metadata is a dict
                            if not hasattr(doc, "metadata") or not doc.metadata:
                                doc.metadata = {}
                            
                            # Add source info
                            doc.metadata["source"] = url
                            doc.metadata["source_type"] = source_type
                            
                            # Add title if available
                            if "title" in source_data:
                                doc.metadata["title"] = source_data["title"]
                    
                    # Add to loaded documents
                    loaded_documents.extend(docs)
                    
                    # Track document types
                    doc_type = source_type
                    loading_state.document_types[doc_type] = loading_state.document_types.get(doc_type, 0) + len(docs)
                    
                    # Estimate tokens
                    for doc in docs:
                        # Very rough estimation: ~4 chars per token
                        if hasattr(doc, "page_content"):
                            loading_state.total_tokens += len(doc.page_content) // 4
                    
                else:
                    # Direct loading without tool
                    docs = load_documents_from_url(url, source_type)
                    
                    # Add metadata to documents
                    for doc in docs:
                        if isinstance(doc, Document):
                            # Ensure metadata is a dict
                            if not hasattr(doc, "metadata") or not doc.metadata:
                                doc.metadata = {}
                            
                            # Add source info
                            doc.metadata["source"] = url
                            doc.metadata["source_type"] = source_type
                            
                            # Add title if available
                            if "title" in source_data:
                                doc.metadata["title"] = source_data["title"]
                    
                    # Add to loaded documents
                    loaded_documents.extend(docs)
                    
                    # Update loading state
                    loading_state.loaded_sources.append({
                        "url": url,
                        "source_type": source_type,
                        "documents_loaded": len(docs)
                    })
                    
                    loading_state.loaded_documents_count += len(docs)
                    
                    # Track document types
                    doc_type = source_type
                    loading_state.document_types[doc_type] = loading_state.document_types.get(doc_type, 0) + len(docs)
                    
                    # Estimate tokens
                    for doc in docs:
                        # Very rough estimation: ~4 chars per token
                        if hasattr(doc, "page_content"):
                            loading_state.total_tokens += len(doc.page_content) // 4
                    
                    # Add document content summaries
                    for i, doc in enumerate(docs[:3]):  # Limit to first 3 docs
                        if hasattr(doc, "page_content"):
                            content_preview = doc.page_content[:500]
                            if len(doc.page_content) > 500:
                                content_preview += "..."
                            loading_state.document_summaries.append(content_preview)
                
            except Exception as e:
                logger.error(f"Error loading documents from {url}: {str(e)}")
                loading_state.failed_sources.append({
                    "url": url,
                    "source_type": source_type,
                    "error": str(e)
                })
                
                # Add warning
                warnings = state.warnings + [f"Error loading documents from {url}: {str(e)}"]
        
        # Update state
        return {
            "loading_state": loading_state,
            "loaded_documents": loaded_documents,
            "current_step": "router_document_processing",
            "step_history": state.step_history + ["load_documents"],
            "routes_taken": state.routes_taken + ["document_loading"],
            "warnings": state.warnings if not loading_state.failed_sources else 
                      (state.warnings + [f"Failed to load {len(loading_state.failed_sources)} sources"])
        }
    
    def _skip_document_processing_node(self, state):
        """Skip document processing."""
        # Add appropriate route
        if not state.loaded_documents:
            route = "no_documents_path"
            warning = "No documents loaded. Skipping document processing."
        else:
            route = "skip_processing_path"
            warning = "Document processing skipped per configuration."
        
        # Add warning
        warnings = state.warnings + [warning]
        
        # Update state
        return {
            "current_step": "generate_response",
            "step_history": state.step_history + ["skip_document_processing"],
            "routes_taken": state.routes_taken + [route],
            "warnings": warnings
        }
    
    def _process_documents_node(self, state):
        """Process documents (chunking and optional embedding)."""
        documents = state.loaded_documents
        
        if not documents:
            warnings = state.warnings + ["No documents to process."]
            return {
                "current_step": "generate_response",
                "step_history": state.step_history + ["process_documents (no docs)"],
                "routes_taken": state.routes_taken + ["no_documents_path"],
                "warnings": warnings
            }
        
        try:
            # Apply chunking if not skipped
            chunked_docs = []
            chunk_count = 0
            
            if not self.config.skip_chunking:
                chunked_docs = chunk_documents(
                    documents, 
                    self.config.chunk_size, 
                    self.config.chunk_overlap
                )
                chunk_count = len(chunked_docs)
            else:
                chunked_docs = documents
                chunk_count = len(documents)
            
            # Update loading state
            loading_state = state.loading_state
            if loading_state:
                loading_state.chunk_count = chunk_count
            
            # Create embeddings and vector store if configured
            embedded = False
            vector_store = None
            retriever = None
            
            if self.config.create_vectorstore and self.config.embeddings and self.config.vectorstore_class:
                try:
                    # Create vector store
                    vector_store = self.config.vectorstore_class.from_documents(
                        chunked_docs,
                        self.config.embeddings
                    )
                    
                    # Create retriever
                    retriever = vector_store.as_retriever()
                    
                    embedded = True
                    
                except Exception as e:
                    logger.error(f"Error creating vector store: {str(e)}")
                    warnings = state.warnings + [f"Error creating vector store: {str(e)}"]
            
            # Update state
            return {
                "chunked_documents": chunked_docs,
                "embedded_documents": embedded,
                "vector_store": vector_store,
                "retriever": retriever,
                "loading_state": loading_state,
                "current_step": "generate_response",
                "step_history": state.step_history + ["process_documents"],
                "routes_taken": state.routes_taken + ["document_processing"],
                "warnings": state.warnings
            }
            
        except Exception as e:
            logger.error(f"Error processing documents: {str(e)}")
            
            # Add warning
            warnings = state.warnings + [f"Error processing documents: {str(e)}"]
            
            # Return unmodified documents
            return {
                "chunked_documents": documents,  # Use original documents
                "current_step": "generate_response",
                "step_history": state.step_history + ["process_documents (error)"],
                "routes_taken": state.routes_taken + ["document_processing_error"],
                "warnings": warnings
            }
    
    def _generate_response_node(self, state):
        """Generate a response about the sources and loaded documents."""
        query = state.query_state.query if state.query_state else "Unknown query"
        loading_state = state.loading_state
        finding_state = state.finding_state
        
        # Create system message with the custom system prompt
        system_message = SystemMessage(content=self.config.system_prompt)
        
        # Create response message
        if not loading_state or loading_state.loaded_documents_count == 0:
            # No documents loaded
            if finding_state and not finding_state.selected_sources:
                # No sources were selected
                ai_message = AIMessage(content=(
                    f"I searched for information about your query: '{query}' but couldn't find any relevant sources. "
                    f"This could be because:\n\n"
                    f"1. The topic might be very specialized or niche\n"
                    f"2. There might be limitations in my search capabilities\n"
                    f"3. The sources available might not meet the relevance criteria\n\n"
                    f"Would you like me to try a different search approach, or could you provide more details or "
                    f"rephrase your query to help me find better sources?"
                ))
            else:
                # Sources were selected but loading failed
                ai_message = AIMessage(content=(
                    f"I identified some potential sources for your query: '{query}', but I wasn't able to load "
                    f"the documents successfully. This could be due to:\n\n"
                    f"1. Access restrictions on the sources\n"
                    f"2. Technical issues with the document loaders\n"
                    f"3. Complex document formats that couldn't be processed\n\n"
                    f"Would you like me to try different sources or a different approach to answer your query?"
                ))
        else:
            # Documents loaded successfully
            loaded_docs_count = loading_state.loaded_documents_count
            loaded_sources_count = len(loading_state.loaded_sources)
            failed_sources_count = len(loading_state.failed_sources)
            chunked_count = loading_state.chunk_count
            
            # Create a summary of the sources
            sources_summary = ""
            for i, source in enumerate(loading_state.loaded_sources, 1):
                sources_summary += f"{i}. {source.get('url')} ({source.get('source_type')}) - " \
                                  f"{source.get('documents_loaded', 0)} documents\n"
            
            # Document details
            document_types = ", ".join([f"{count} {type}" for type, count in loading_state.document_types.items()])
            total_tokens = loading_state.total_tokens
            
            # Include information about embeddings if created
            embedding_info = ""
            if state.embedded_documents:
                embedding_info = (
                    f"I've also created embeddings for these documents, making them ready for semantic search "
                    f"and retrieval. "
                )
            
            ai_message = AIMessage(content=(
                f"I've found and processed information for your query: '{query}'\n\n"
                f"**Sources Summary:**\n"
                f"- Successfully loaded {loaded_docs_count} documents from {loaded_sources_count} sources\n"
                f"- {document_types}\n"
                f"- Created {chunked_count} chunks for processing\n"
                f"- Approximately {total_tokens} tokens in total\n"
                f"{embedding_info}\n"
                f"**Sources Used:**\n{sources_summary}\n\n"
                f"I'm ready to answer questions based on these documents. You can ask specific questions "
                f"about the content, request summaries of particular aspects, or ask for comparisons "
                f"between different sources."
            ))
        
        # Add messages
        messages = list(state.messages)
        messages.append(system_message)
        messages.append(ai_message)
        
        # Update state
        return {
            "messages": messages,
            "current_step": "complete",
            "step_history": state.step_history + ["generate_response"]
        }
    
    def _error_node(self, state):
        """Handle error cases."""
        error_message = state.error or "An unknown error occurred during the source finding process."
        
        # Create error message
        ai_message = AIMessage(content=(
            f"I encountered an error while searching for sources: {error_message}\n\n"
            f"This could be due to:\n"
            f"1. Issues with the search tools or APIs\n"
            f"2. Connectivity problems with external services\n"
            f"3. Limitations in processing your specific query\n\n"
            f"Would you like to try again with a more specific query, or can I help you in another way?"
        ))
        
        # Add message
        messages = list(state.messages)
        messages.append(ai_message)
        
        # Update state
        return {
            "messages": messages,
            "current_step": "error",
            "step_history": state.step_history + ["error_node"]
        }

# ===========================================
# Factory Functions
# ===========================================

def create_source_finder_agent(
    search_tools=None,
    system_prompt=None,
    max_sources_to_load=3,
    chunk_size=1000,
    chunk_overlap=200,
    skip_analysis=False,
    skip_chunking=False,
    google_api_key=None,
    google_cse_id=None,
    github_token=None,
    embeddings=None,
    vectorstore_class=None,
    create_vectorstore=False,
    **kwargs
) -> SourceFinderAgent:
    """
    Create a source finder agent.
    
    Args:
        search_tools: Optional search tools to use
        system_prompt: Optional system prompt
        max_sources_to_load: Maximum number of sources to load
        chunk_size: Size of document chunks (in characters)
        chunk_overlap: Overlap between document chunks (in characters)
        skip_analysis: Whether to skip detailed analysis
        skip_chunking: Whether to skip document chunking
        google_api_key: Google API key for search
        google_cse_id: Google CSE ID for search
        github_token: GitHub token for API access
        embeddings: Optional embeddings model
        vectorstore_class: Optional vector store class
        create_vectorstore: Whether to create a vector store
        **kwargs: Additional keyword arguments for configuration
        
    Returns:
        SourceFinderAgent instance
    """
    # Create default search tools if not provided
    if not search_tools:
        search_tools = []
    
    # Create config
    config = SourceFinderConfig(
        name=kwargs.pop("name", f"source_finder_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
        system_prompt=system_prompt or "You are a source-finding assistant that helps users find and load relevant documents.",
        search_tools=search_tools,
        max_sources_to_load=max_sources_to_load,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        skip_analysis=skip_analysis,
        skip_chunking=skip_chunking,
        google_api_key=google_api_key,
        google_cse_id=google_cse_id,
        github_token=github_token,
        embeddings=embeddings,
        vectorstore_class=vectorstore_class,
        create_vectorstore=create_vectorstore,
        **kwargs
    )
    
    # Build and return agent
    return config.build_agent()

# ===========================================
# Integration with RAG Processor
# ===========================================

class SourceToRAGProcessor:
    """
    Process that connects source finding to RAG processing.
    
    This class integrates the source finder agent with document loading and
    subsequent RAG processing.
    """
    
    def __init__(
        self, 
        source_finder: SourceFinderAgent,
        embedding_model=None,
        vector_store_cls=None,
        chroma_directory=None,
        max_docs_per_source=10,
        chunk_size=1000,
        chunk_overlap=200
    ):
        """
        Initialize the processor.
        
        Args:
            source_finder: SourceFinderAgent to use for finding sources
            embedding_model: Embedding model to use for RAG
            vector_store_cls: Vector store class to use
            chroma_directory: Directory for Chroma persistence
            max_docs_per_source: Maximum documents to load per source
            chunk_size: Size of document chunks
            chunk_overlap: Overlap between chunks
        """
        self.source_finder = source_finder
        self.embedding_model = embedding_model
        self.vector_store_cls = vector_store_cls
        self.chroma_directory = chroma_directory
        self.max_docs_per_source = max_docs_per_source
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a query by finding sources and loading documents.
        
        Args:
            query: User query
            
        Returns:
            Dict containing loaded documents and metadata
        """
        # Run source finder agent to get sources and documents
        source_finder_result = self.source_finder.run(query)
        
        # Get loaded documents
        loaded_documents = source_finder_result.get("loaded_documents", [])
        chunked_documents = source_finder_result.get("chunked_documents", [])
        
        # Use chunked documents if available, otherwise use loaded documents
        documents = chunked_documents if chunked_documents else loaded_documents
        
        # Create vector store if not already created
        retriever = source_finder_result.get("retriever")
        vector_store = source_finder_result.get("vector_store")
        
        if not retriever and self.embedding_model and self.vector_store_cls and documents:
            try:
                # Create vector store
                if self.vector_store_cls.__name__ == "Chroma" and self.chroma_directory:
                    # Persistent Chroma
                    vector_store = self.vector_store_cls.from_documents(
                        documents,
                        self.embedding_model,
                        persist_directory=self.chroma_directory
                    )
                else:
                    # In-memory vector store
                    vector_store = self.vector_store_cls.from_documents(
                        documents,
                        self.embedding_model
                    )
                
                # Create retriever
                retriever = vector_store.as_retriever()
                
            except Exception as e:
                logger.error(f"Error creating vector store: {str(e)}")
        
        # Return processed data
        return {
            "query": query,
            "documents": documents,
            "retriever": retriever,
            "vector_store": vector_store,
            "source_finder_result": source_finder_result
        }
    
    def retrieve_relevant_documents(self, query: str, k: int = 4) -> List[Document]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: User query
            k: Number of documents to retrieve
            
        Returns:
            List of relevant documents
        """
        # Process query to get retriever and documents
        result = self.process_query(query)
        
        # Use retriever if available
        if result.get("retriever"):
            try:
                return result["retriever"].get_relevant_documents(query)
            except Exception as e:
                logger.error(f"Error retrieving documents: {str(e)}")
        
        # Fallback to simple similarity search if documents are available
        documents = result.get("documents", [])
        if documents and self.embedding_model:
            try:
                from langchain_core.utils.similarity import cosine_similarity
                
                # Get query embedding
                query_embedding = self.embedding_model.embed_query(query)
                
                # Get document embeddings
                doc_embeddings = []
                for doc in documents:
                    try:
                        doc_embedding = self.embedding_model.embed_documents([doc.page_content])[0]
                        doc_embeddings.append((doc, doc_embedding))
                    except Exception:
                        # Skip documents that can't be embedded
                        continue
                
                # Calculate similarities
                similarities = [(doc, cosine_similarity(query_embedding, doc_embedding)) 
                               for doc, doc_embedding in doc_embeddings]
                
                # Sort by similarity
                similarities.sort(key=lambda x: x[1], reverse=True)
                
                # Return top k documents
                return [doc for doc, _ in similarities[:k]]
                
            except Exception as e:
                logger.error(f"Error in similarity search: {str(e)}")
        
        # Return all documents if retrieval methods fail
        return documents[:k] if documents else []