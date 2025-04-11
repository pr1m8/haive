from typing import List, Optional, Dict, Any, Callable, Union
import os
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import time
import re
from dotenv import load_dotenv
from langchain_core.tools import tool, StructuredTool
from pydantic import BaseModel, Field, validator

# Import LangChain document loaders
from langchain_community.document_loaders import WebBaseLoader, RecursiveUrlLoader
from langchain_community.tools.tavily_search import TavilySearchResults

# Load environment variables
load_dotenv(dotenv_path='.env')
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

try:
    from tavily import TavilyClient
    client = TavilyClient(api_key=TAVILY_API_KEY)
except ImportError:
    # Provide a mock client for environments without Tavily
    class MockTavilyClient:
        def qna_search(self, **kwargs):
            return {"answer": "This is a mock answer as Tavily client is not available."}
        
        def extract(self, **kwargs):
            return {"content": "This is mock extracted content as Tavily client is not available."}
        
        def get_search_context(self, **kwargs):
            return "This is mock search context as Tavily client is not available."
    
    client = MockTavilyClient()

# Input/Output schemas for structured tools
class TavilyQnAInput(BaseModel):
    query: str = Field(..., description="The search query string about a company or individual")
    max_results: Optional[int] = Field(5, description="Maximum number of results to return")
    include_answer: Optional[bool] = Field(True, description="Include short answer in response")
    search_depth: Optional[str] = Field("advanced", description="Search depth, either 'basic' or 'advanced'")
    topic: Optional[str] = Field("general", description="Topic of search")
    days: Optional[int] = Field(3, description="Number of days to search back")
    include_domains: Optional[List[str]] = Field(default_factory=list, description="Domains to include")
    exclude_domains: Optional[List[str]] = Field(default_factory=list, description="Domains to exclude")

class TavilyExtractInput(BaseModel):
    urls: List[str] = Field(..., description="The list of URLs to extract content from")
    max_characters: Optional[int] = Field(None, description="Maximum number of characters to extract")

class TavilySearchContextInput(BaseModel):
    query: str = Field(..., description="The search query string")
    search_depth: str = Field("advanced", description="Search depth, either 'basic' or 'advanced'")
    topic: str = Field("general", description="The topic of the search")
    days: int = Field(7, description="The number of days to search for")
    max_results: int = Field(5, description="Maximum number of results to return")
    include_domains: Optional[List[str]] = Field(default_factory=list, description="Specific domains to include in search")
    exclude_domains: Optional[List[str]] = Field(default_factory=list, description="Specific domains to exclude in search")
    max_tokens: int = Field(4000, description="Maximum number of tokens to return")

class TavilySearchToolInput(BaseModel):
    query: str = Field(..., description="The search query string about a company or individual")
    max_results: Optional[int] = Field(5, description="Maximum number of results to return")
    include_answer: Optional[bool] = Field(True, description="Include short answer in response")
    include_raw_content: Optional[bool] = Field(False, description="Include raw content of the search results")
    include_images: Optional[bool] = Field(False, description="Include images in the response")
    search_depth: Optional[str] = Field("advanced", description="Search depth, either 'basic' or 'advanced'")
    include_domains: Optional[List[str]] = Field(default_factory=list, description="Specific domains to include in search")
    exclude_domains: Optional[List[str]] = Field(default_factory=list, description="Specific domains to exclude in search")

class ScrapeWebpagesInput(BaseModel):
    urls: List[str] = Field(..., description="The list of URLs to scrape")

class RecursiveUrlLoaderInput(BaseModel):
    url: str = Field(..., description="The root URL to start crawling from")
    max_depth: int = Field(2, description="Maximum depth to crawl (1-3 recommended)")
    exclude_dirs: Optional[List[str]] = Field(default_factory=list, description="URL patterns to exclude")
    timeout: int = Field(10, description="Timeout for HTTP requests in seconds")
    prevent_outside: bool = Field(True, description="Only crawl URLs on the same domain")
    use_async: bool = Field(False, description="Use async loading for faster crawling")
    check_response_status: bool = Field(True, description="Check response status and raise exception if not 200")
    continue_on_failure: bool = Field(True, description="Continue on failure or stop")

def bs4_extractor(html: str) -> str:
    """Extract readable text from HTML content using BeautifulSoup."""
    soup = BeautifulSoup(html, "html.parser")
    
    # Remove script and style elements
    for script in soup(["script", "style", "header", "footer", "nav"]):
        script.extract()
    
    # Get text
    text = soup.get_text(separator="\n")
    
    # Clean up text - remove excessive newlines
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    return text.strip()

# Define the structured tools

def tavily_qna_func(query: str, max_results: Optional[int] = 5,
               include_answer: Optional[bool] = True,
               search_depth: Optional[str] = "advanced", 
               topic: Optional[str] = "general",
               days: Optional[int] = 3,
               include_domains: Optional[List[str]] = None,
               exclude_domains: Optional[List[str]] = None) -> Dict:
    """
    Search tool for getting a quick answer to a KYC-related question.
    """
    if include_domains is None:
        include_domains = []
    if exclude_domains is None:
        exclude_domains = []
        
    response = client.qna_search(
        query=query, 
        search_depth=search_depth,
        topic=topic,
        days=days,
        max_results=max_results,
        include_domains=include_domains,
        exclude_domains=exclude_domains
    )
    return response

tavily_qna_tool = StructuredTool.from_function(
    func=tavily_qna_func,
    name="tavily_qna",
    description="Search tool for getting a quick answer to a KYC-related question",
    args_schema=TavilyQnAInput
)

def tavily_extract_func(urls: List[str], max_characters: Optional[int] = None) -> Dict:
    """
    Extract content from company websites or regulatory websites for KYC verification.
    """
    kwargs = {}
    if max_characters:
        kwargs["max_characters"] = max_characters
        
    response = client.extract(
        urls=urls,
        **kwargs
    )
    return response

tavily_extract_tool = StructuredTool.from_function(
    func=tavily_extract_func,
    name="tavily_extract",
    description="Extract content from company websites or regulatory websites for KYC verification",
    args_schema=TavilyExtractInput
)

def tavily_search_context_func(query: str,
                          search_depth: str = "advanced",
                          topic: str = "general",
                          days: int = 7,
                          max_results: int = 5,
                          include_domains: Optional[List[str]] = None,
                          exclude_domains: Optional[List[str]] = None,
                          max_tokens: int = 4000) -> str:
    """
    Generate search context for KYC-related queries about companies or individuals.
    """
    if include_domains is None:
        include_domains = []
    if exclude_domains is None:
        exclude_domains = []
        
    response = client.get_search_context(   
        query=query,
        search_depth=search_depth,
        topic=topic,
        days=days,
        max_results=max_results,
        include_domains=include_domains,
        exclude_domains=exclude_domains,
        max_tokens=max_tokens
    )
    return response

tavily_search_context_tool = StructuredTool.from_function(
    func=tavily_search_context_func,
    name="tavily_search_context",
    description="Generate search context for KYC-related queries about companies or individuals",
    args_schema=TavilySearchContextInput
)

def tavily_search_tool_func(
    query: str,
    max_results: Optional[int] = 5,
    include_answer: Optional[bool] = True,
    include_raw_content: Optional[bool] = False,
    include_images: Optional[bool] = False,
    search_depth: Optional[str] = "advanced",
    include_domains: Optional[List[str]] = None,
    exclude_domains: Optional[List[str]] = None,
) -> Dict:
    """
    Advanced search tool for comprehensive KYC research with full configurability.
    """
    if include_domains is None:
        include_domains = []
    if exclude_domains is None:
        exclude_domains = []
        
    # Initialize TavilySearchResults with provided parameters
    tavily_tool = TavilySearchResults(
        max_results=max_results,
        include_answer=include_answer,
        include_raw_content=include_raw_content,
        include_images=include_images,
        search_depth=search_depth,
        include_domains=include_domains,
        exclude_domains=exclude_domains,
    )

    # Execute the query and return results
    return tavily_tool.invoke({"query": query})

tavily_search_tool_structured = StructuredTool.from_function(
    func=tavily_search_tool_func,
    name="tavily_search_tool",
    description="Advanced search tool for comprehensive KYC research with full configurability",
    args_schema=TavilySearchToolInput
)

def scrape_webpages_func(urls: List[str]) -> str:
    """
    Scrape company websites, regulatory databases, or news articles for KYC verification.
    """
    all_content = []
    
    for url in urls:
        try:
            # Use RecursiveUrlLoader for deeper scraping
            loader = RecursiveUrlLoader(
                url=url,
                max_depth=2,
                extractor=bs4_extractor,
                prevent_outside=True,
                timeout=10,
                check_response_status=True,
                continue_on_failure=True
            )
            
            # Load the documents
            docs = loader.load()
            
            # Format the content
            site_content = f"## Website: {url}\n\n"
            site_content += f"Found {len(docs)} pages on this website.\n\n"
            
            # Add content from the first 5 pages (or fewer if less available)
            for i, doc in enumerate(docs[:5]):
                page_url = doc.metadata.get("source", "Unknown URL")
                page_title = doc.metadata.get("title", "No title")
                
                site_content += f"### Page {i+1}: {page_title}\n"
                site_content += f"URL: {page_url}\n\n"
                
                # Limit content length for readability
                content_preview = doc.page_content[:2000] + ("..." if len(doc.page_content) > 2000 else "")
                site_content += content_preview + "\n\n"
                
            all_content.append(site_content)
                
        except Exception as e:
            error_content = f'## Error scraping {url}\n\nError message: {str(e)}\n\n'
            all_content.append(error_content)
    
    return "\n\n".join(all_content)

scrape_webpages_tool = StructuredTool.from_function(
    func=scrape_webpages_func,
    name="scrape_webpages",
    description="Recursively scrape company websites for KYC verification, capturing content from multiple pages",
    args_schema=ScrapeWebpagesInput
)

def recursive_url_loader_func(
    url: str,
    max_depth: int = 2,
    exclude_dirs: Optional[List[str]] = None,
    timeout: int = 10,
    prevent_outside: bool = True,
    use_async: bool = False,
    check_response_status: bool = True,
    continue_on_failure: bool = True
) -> str:
    """
    Recursively crawl a website starting from a URL, useful for extracting company information for KYC.
    
    This tool uses LangChain's RecursiveUrlLoader to deeply crawl a website and extract information
    relevant for KYC analysis, such as business descriptions, services, and compliance information.
    """
    if exclude_dirs is None:
        exclude_dirs = []
    
    try:
        # Create the loader
        loader = RecursiveUrlLoader(
            url=url,
            max_depth=max_depth,
            extractor=bs4_extractor,
            exclude_dirs=exclude_dirs,
            timeout=timeout,
            prevent_outside=prevent_outside,
            use_async=use_async,
            check_response_status=check_response_status,
            continue_on_failure=continue_on_failure
        )
        
        # Load the documents
        docs = loader.load()
        
        # Format the output
        result = f"# Website Crawl Results: {url}\n\n"
        result += f"Found {len(docs)} pages.\n\n"
        
        # Add summary of each page
        for i, doc in enumerate(docs):
            page_url = doc.metadata.get("source", "Unknown URL")
            page_title = doc.metadata.get("title", "No title")
            
            result += f"## Page {i+1}: {page_title}\n"
            result += f"URL: {page_url}\n\n"
            
            # Add a content preview
            content_preview = doc.page_content[:2000] + ("..." if len(doc.page_content) > 2000 else "")
            result += content_preview + "\n\n"
            
            # Add separator between pages
            if i < len(docs) - 1:
                result += "---\n\n"
        
        return result
        
    except Exception as e:
        return f"Error crawling website {url}: {str(e)}"

recursive_url_loader_tool = StructuredTool.from_function(
    func=recursive_url_loader_func,
    name="recursive_url_loader",
    description="Recursively crawl a website starting from a URL, useful for extracting company information for KYC",
    args_schema=RecursiveUrlLoaderInput
)

# List of all tools
KYC_TOOLS = [
    tavily_qna_tool,
    tavily_extract_tool,
    tavily_search_context_tool,
    tavily_search_tool_structured,
    scrape_webpages_tool,
    recursive_url_loader_tool
]