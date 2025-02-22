import asyncio
import inspect
import logging
import re
from typing import (
    Callable,
    Iterator,
    List,
    Optional,
    Sequence,
    Set,
    Union,
    cast,
    TypeVar,
)

import aiohttp
import requests
from langchain_core.documents import Document
from langchain_core.utils.html import extract_sub_links
from typing import Any
from typing_extensions import Optional,List,Dict
from langchain_community.document_loaders import (
    SitemapLoader, RecursiveUrlLoader, PlaywrightURLLoader, SeleniumURLLoader, \
        UnstructuredURLLoader, AsyncHtmlLoader, AsyncChromiumLoader, \
        WebBaseLoader,BSHTMLLoader
)
from langchain.tools import tool
from urllib.parse import urljoin, urlparse



logger = logging.getLogger(__name__)

# Add type definition before the functions
_MetadataExtractorType = Callable[
    [str, str, Union[requests.Response, aiohttp.ClientResponse]], dict
]

def _metadata_extractor(
    raw_html: str, url: str, response: Union[requests.Response, aiohttp.ClientResponse]
) -> dict:
    """Extract metadata from raw html using BeautifulSoup."""
    content_type = getattr(response, "headers").get("Content-Type", "")
    metadata = {"source": url, "content_type": content_type}

    try:
        from bs4 import BeautifulSoup
    except ImportError:
        logger.warning(
            "The bs4 package is required for default metadata extraction. "
            "Please install it with `pip install -U beautifulsoup4`."
        )
        return metadata
    soup = BeautifulSoup(raw_html, "html.parser")
    if title := soup.find("title"):
        metadata["title"] = title.get_text()
    if description := soup.find("meta", attrs={"name": "description"}):
        metadata["description"] = description.get("content", None)
    if html := soup.find("html"):
        metadata["language"] = html.get("lang", None)
    return metadata

@tool
def find_sitemap(base_url: str, keep_path_segment: Optional[str] = None) -> Optional[str]:
    """
    Tries to find the sitemap URL for a given base URL by checking common paths.
    
    Args:
        base_url (str): The base URL to start from.
        keep_path_segment (str, optional): A path segment to keep in the URL.

    Returns:
        str: The first valid sitemap URL found or None if no sitemap is found.
    """
    # Normalize the base URL (remove trailing slash if present)
    if base_url.endswith("/"):
        base_url = base_url[:-1]

    # Possible sitemap locations to try
    common_sitemap_paths = ["sitemap.xml", "sitemap_index.xml"]

    # Keep trimming the path and checking
    while base_url:
        for sitemap in common_sitemap_paths:
            sitemap_url = urljoin(base_url, sitemap)
            try:
                response = requests.head(sitemap_url, timeout=5)
                if response.status_code == 200:
                    print(f"Found sitemap: {sitemap_url}")
                    return sitemap_url
            except requests.RequestException as e:
                print(f"Failed to connect to {sitemap_url}: {e}")
        
        # Trim the URL path but keep the specified path segment
        parsed = urlparse(base_url)
        path = parsed.path.rsplit("/", 1)[0]  # Remove last segment of the path
        if keep_path_segment and keep_path_segment in path:
            break  # Stop if the specified path segment is in the path
        if not path or path == "/":
            break  # Stop if there's no more path to trim
        base_url = f"{parsed.scheme}://{parsed.netloc}{path}"

    print("No sitemap found.")
    return None

@tool
def load_sitemap_documents(base_url: str, keep_path_segment: Optional[str] = None) -> List[Dict]:
    """
    Load documents from a sitemap URL.

    Args:
        base_url: The base URL to start from.
        keep_path_segment: A path segment to keep in the URL.

    Returns:
        A list of dictionaries containing document content.
    """
    sitemap_url = find_sitemap(base_url, keep_path_segment)
    if sitemap_url:
        sitemap_loader = SitemapLoader(web_path=sitemap_url)
        # Replace multiple newline characters and whitespace with a single newline

        documents = [re.sub(r'\n+', '\n', doc.page_content) for doc in sitemap_loader.load()]
        #documents = sitemap_loader.aload()
        return documents 
    else:
        return []

@tool
def load_recursive_url_documents(
    url: str,
    max_depth: Optional[int] = 20,
    use_async: Optional[bool] = None,
    extractor: Optional[Callable[[str], str]] = None,
    metadata_extractor: Optional[_MetadataExtractorType] = None,
    exclude_dirs: Optional[Sequence[str]] = (),
    timeout: Optional[int] = 10,
    prevent_outside: bool = True,
    link_regex: Union[str, re.Pattern, None] = None,
    headers: Optional[dict] = None,
    check_response_status: bool = False,
    continue_on_failure: bool = True,
    base_url: Optional[str] = None,
    autoset_encoding: bool = True,
    encoding: Optional[str] = None,
    proxies: Optional[dict] = None,
) -> List[Dict]:
    """
    Load documents from a website recursively.

    Args:
        url: The URL to crawl.
        max_depth: The max depth of the recursive loading.
        use_async: Whether to use asynchronous loading.
        extractor: A function to extract document contents from raw HTML.
        metadata_extractor: A function to extract metadata from raw HTML.
        exclude_dirs: A list of subdirectories to exclude.
        timeout: The timeout for the requests, in seconds.
        prevent_outside: If True, prevent loading from URLs which are not children of the root URL.
        link_regex: Regex for extracting sub-links from the raw HTML of a web page.
        headers: Default request headers to use for all requests.
        check_response_status: If True, check HTTP response status and skip URLs with error responses (400-599).
        continue_on_failure: If True, continue if getting or parsing a link raises an exception.
        base_url: The base URL to check for outside links against.
        autoset_encoding: Whether to automatically set the encoding of the response.
        encoding: The encoding of the response.
        proxies: A dictionary mapping protocol names to the proxy URLs to be used for requests.

    Returns:
        A list of dictionaries containing document content.
    """
    loader = RecursiveUrlLoader(
        url=url,
        max_depth=max_depth,
        use_async=use_async,
        extractor=extractor,
        metadata_extractor=metadata_extractor,
        exclude_dirs=exclude_dirs,
        timeout=timeout,
        prevent_outside=prevent_outside,
        link_regex=link_regex,
        headers=headers,
        check_response_status=check_response_status,
        continue_on_failure=continue_on_failure,
        base_url=base_url,
        autoset_encoding=autoset_encoding,
        encoding=encoding,
        proxies=proxies,
    )
    documents = loader.load()
    return [{"content": doc.page_content} for doc in documents]

@tool
def load_playwright_url_documents(
    url: str,
    timeout: Optional[int] = 10,
    headers: Optional[dict] = None,
    check_response_status: bool = False,
    continue_on_failure: bool = True,
    **kwargs
) -> List[Dict]:
    """
    Load documents from a URL using Playwright.

    Args:
        url: The URL to load documents from.
        timeout: The timeout for the requests, in seconds.
        headers: Default request headers to use for all requests.
        check_response_status: If True, check HTTP response status and skip URLs with error responses (400-599).
        continue_on_failure: If True, continue if getting or parsing a link raises an exception.
        **kwargs: Additional keyword arguments for the PlaywrightURLLoader.

    Returns:
        A list of dictionaries containing document content.
    """
    loader = PlaywrightURLLoader(
        url=url,
        timeout=timeout,
        headers=headers,
        check_response_status=check_response_status,
        continue_on_failure=continue_on_failure,
        **kwargs
    )
    documents = loader.load()
    return [{"content": doc.page_content} for doc in documents]

@tool
def load_selenium_url_documents(
    url: str,
    timeout: Optional[int] = 10,
    headers: Optional[dict] = None,
    check_response_status: bool = False,
    continue_on_failure: bool = True,
    **kwargs
) -> List[Dict]:
    """
    Load documents from a URL using Selenium.

    Args:
        url: The URL to load documents from.
        timeout: The timeout for the requests, in seconds.
        headers: Default request headers to use for all requests.
        check_response_status: If True, check HTTP response status and skip URLs with error responses (400-599).
        continue_on_failure: If True, continue if getting or parsing a link raises an exception.
        **kwargs: Additional keyword arguments for the SeleniumURLLoader.

    Returns:
        A list of dictionaries containing document content.
    """
    loader = SeleniumURLLoader(
        url=url,
        timeout=timeout,
        headers=headers,
        check_response_status=check_response_status,
        continue_on_failure=continue_on_failure,
        **kwargs
    )
    documents = loader.load()
    return [{"content": doc.page_content} for doc in documents]

@tool
def load_unstructured_url_documents(
    url: str,
    continue_on_failure: bool = True,
    mode: str = "single",
    show_progress_bar: bool = False,
    **unstructured_kwargs: Any,
) -> List[Dict]:
    """
    Load documents from a URL using UnstructuredURLLoader.

    Args:
        url: The URL to load documents from.
        continue_on_failure: If True, continue if getting or parsing a link raises an exception.
        mode: The mode to run the loader in. Default is "single".
        show_progress_bar: If True, show a progress bar during loading.
        **unstructured_kwargs: Additional keyword arguments for the UnstructuredURLLoader.

    Returns:
        A list of dictionaries containing document content.
    """
    loader = UnstructuredURLLoader(
        url=url,
        continue_on_failure=continue_on_failure,
        mode=mode,
        show_progress_bar=show_progress_bar,
        **unstructured_kwargs
    )
    documents = loader.load()
    return [{"content": doc.page_content} for doc in documents]

#@tool
#def load_async_html_documents(
#    url: str,#
#    timeout: Optional[int]
#anggraph_sitemap_url='https://langchain-ai.github.io/langgraph/sitemap.xml'
#docs = load_sitemap_documents(langgraph_sitemap_url)
#print(docs)
