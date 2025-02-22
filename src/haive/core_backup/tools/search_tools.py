from typing import Annotated, List

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from typing import List, Optional, Dict
from dotenv import load_dotenv
from tavily import TavilyClient
load_dotenv(dotenv_path='.env.example')
import os
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
from typing import Literal, Sequence

client = TavilyClient(api_key=TAVILY_API_KEY)

@tool
def tavily_qna(query: str, max_results: Optional[int] = 5, 
               include_answer: Optional[bool] = True,
                 search_depth: Optional[str] = "advanced", 
                 verbose: Optional[bool] = False,
                 topic: Optional[str] = "general",
                 days: Optional[int] = 3,
                 include_domains: Optional[List[str]] = [],
                 exclude_domains: Optional[List[str]] = []
                 ) -> Dict:
    """
    Search tool for getting a quick answer to a question.
    Args:
        query (str): The search query string.
        max_results (Optional[int]): Maximum number of results to return. Default is 5.
        include_answer (Optional[bool]): Include short answer in response. Default is True.
        search_depth (Optional[str]): Search depth, either 'basic' or 'advanced'. Default is 'advanced'.
        verbose (Optional[bool]): Log the tool’s progress. Default is False.
    Returns:
        Dict: The search results in a structured format.
    """
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
@tool 
def tavily_extract(urls: List[str], **kwargs) -> Dict:
    """
    The Tavily Extract API allows you to effortlessly retrieve raw content from a list of websites, 
    making it ideal for data collection, content analysis, and research. You can also combine Tavily
    Extract with our Search method: first, obtain a list of relevant documents,
    then perform further processing on selected links to gather additional information and use it as 
    context for your research tasks.
    Args:
        urls (List[str]): The list of URLs to search.
        **kwargs: Accept custom arguments.
    Returns:
        Dict: The search results in a structured format.
    """
    response = client.extract(
        urls=urls,
        **kwargs
    )
    return response

@tool 
def tavily_search_context(query: str,
                           search_depth: Literal["basic", "advanced"] = "basic",
                           topic: Literal["general", "news"] = "general",
                           days: int = 3,
                           max_results: int = 5,
                           include_domains: Sequence[str] = None,
                           exclude_domains: Sequence[str] = None,
                           max_tokens: int = 4000,
                           **kwargs,  # Accept custom arguments
                           ) -> str:
    """
    Generating context for a RAG Application.
    Args:
        query (str): The search query string.
        search_depth (Literal["basic", "advanced"]): Search depth, either 'basic' or 'advanced'. Default is 'basic'.
        topic (Literal["general", "news"]): The topic of the search. Default is 'general'.
        days (int): The number of days to search for. Default is 3.
        max_results (int): Maximum number of results to return. Default is 5.
        include_domains (Sequence[str]): Specific domains to include in search. Default is None.
        exclude_domains (Sequence[str]): Specific domains to exclude in search. Default is None.
        max_tokens (int): Maximum number of tokens to return. Default is 4000.
        **kwargs: Accept custom arguments.
    Returns:
        str: The search results in a structured format.
    """
    response = client.get_search_context(   
                           query=query,
                           search_depth=search_depth,
                           topic=topic,
                           days=days,
                           max_results=max_results,
                           include_domains=include_domains,
                           exclude_domains=exclude_domains,
                           max_tokens=max_tokens,
                           **kwargs,
    )
    return response
@tool
def tavily_search_tool(
    query: str,
    max_results: Optional[int] = 5,
    include_answer: Optional[bool] = True,
    include_raw_content: Optional[bool] = False,
    include_images: Optional[bool] = False,
    search_depth: Optional[str] = "advanced",
    include_domains: Optional[List[str]] = [],
    exclude_domains: Optional[List[str]] = [],
    verbose: Optional[bool] = False,
) -> Dict:
    """
    Query Tavily Search API with full configurability.

    Args:
        query (str): The search query string.
        max_results (Optional[int]): Maximum number of results to return. Default is 5.
        include_answer (Optional[bool]): Include short answer in response. Default is True.
        include_raw_content (Optional[bool]): Include raw content of the search results. Default is False.
        include_images (Optional[bool]): Include images in the response. Default is False.
        search_depth (Optional[str]): Search depth, either 'basic' or 'advanced'. Default is 'advanced'.
        include_domains (Optional[List[str]]): Specific domains to include in search. Default is None.
        exclude_domains (Optional[List[str]]): Specific domains to exclude in search. Default is None.
        verbose (Optional[bool]): Log the tool’s progress. Default is False.

    Returns:
        Dict: The search results in a structured format.
    """
    # Initialize TavilySearchResults with provided parameters
    tavily_tool = TavilySearchResults(
        max_results=max_results,
        include_answer=include_answer,
        include_raw_content=include_raw_content,
        include_images=include_images,
        search_depth=search_depth,
        include_domains=include_domains,
        exclude_domains=exclude_domains,
        verbose=verbose,
    )

    # Execute the query and return results
    return tavily_tool.invoke({"query": query})


@tool
def scrape_webpages(urls: List[str]) -> str:
    """
    Use requests and bs4 to scrape the provided web pages for detailed information.
    Args:
        urls (List[str]): The list of URLs to scrape.
    Returns:
        str: The scraped content in a structured format.
    """
    loader = WebBaseLoader(urls)
    docs = loader.load()
    return "\n\n".join(
        [
            f'<Document name="{doc.metadata.get("title", "")}">\n{doc.page_content}\n</Document>'
            for doc in docs
        ]
    )