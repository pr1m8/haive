# src/haive/prebuilt/priv/kyc_web_retriever.py

from typing import List, Dict, Any, Optional, Tuple, Set
import logging
import hashlib
from urllib.parse import urljoin, urlparse
import asyncio

from langchain_community.utilities import TavilySearchAPIWrapper
from langchain_community.document_loaders import RecursiveUrlLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from bs4 import BeautifulSoup
import aiohttp

logger = logging.getLogger(__name__)

class KYCWebRetriever:
    """
    Web retriever for KYC compliance research.
    """
    
    def __init__(
        self,
        search_api_key=None,
        max_recursive_depth=2,
        max_links_per_page=5,
        max_pages_total=20,
    ):
        """Initialize the KYC web retriever"""
        # Initialize search tool
        self.search_tool = TavilySearchAPIWrapper(api_key=search_api_key)
            
        # Set up document transformers
        self.html2text = Html2TextTransformer()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=8000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Set up tracking variables
        self.visited_urls = set()
        self.max_recursive_depth = max_recursive_depth
        self.max_links_per_page = max_links_per_page
        self.max_pages_total = max_pages_total
    
    async def research_client(
        self, 
        client_name: str,
        search_queries: List[str],
        risk_appetite_statement: str,
    ) -> Tuple[List[Dict[str, Any]], List[str]]:
        """
        Perform comprehensive web research on a client.
        """
        search_results = []
        research_notes = []
        
        # Perform searches with each query
        for query in search_queries:
            results = self.search_tool.results(query, max_results=5)
            if isinstance(results, list):
                search_results.extend(results)
        
        # Deduplicate results
        unique_results = self._deduplicate_results(search_results)
        
        # Process results recursively
        async with aiohttp.ClientSession() as session:
            for result in unique_results[:self.max_pages_total]:
                url = result.get("url", "")
                if url and url not in self.visited_urls:
                    try:
                        # Load content recursively
                        loader = RecursiveUrlLoader(
                            url=url,
                            max_depth=self.max_recursive_depth,
                            extractor=lambda x: self._extract_content_and_links(x, url)
                        )
                        documents = loader.load()
                        
                        # Process documents
                        for doc in documents:
                            # Create research note
                            note = self._analyze_document(doc, client_name, risk_appetite_statement)
                            research_notes.append(note)
                            
                            # Add to visited URLs
                            self.visited_urls.add(doc.metadata.get("source", ""))
                            
                            # Limit total pages
                            if len(self.visited_urls) >= self.max_pages_total:
                                break
                    except Exception as e:
                        logger.error(f"Error processing URL {url}: {str(e)}")
        
        return unique_results, research_notes
    
    def _deduplicate_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate search results by URL"""
        unique_urls = set()
        unique_results = []
        
        for result in results:
            url = result.get("url", "")
            if url and url not in unique_urls:
                unique_urls.add(url)
                unique_results.append(result)
                
        return unique_results
    
    def _extract_content_and_links(self, html: str, base_url: str) -> Tuple[str, List[str]]:
        """Extract clean text and links from HTML"""
        # Parse HTML
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract text
        text = soup.get_text(separator='\n', strip=True)
        
        # Extract links
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            
            # Only include HTTP/HTTPS links
            parsed = urlparse(full_url)
            if parsed.scheme in ('http', 'https') and len(parsed.netloc) > 0:
                links.append(full_url)
        
        return text, links[:self.max_links_per_page]
    
    def _analyze_document(self, document: Document, client_name: str, risk_appetite_statement: str) -> str:
        """Analyze a document for KYC compliance information"""
        # In a real implementation, this would use the LLM to analyze the content
        # For now, return a simple research note
        url = document.metadata.get("source", "Unknown source")
        content = document.page_content[:500]  # Truncate for example
        
        note = f"=== Research Note ===\n"
        note += f"Source: {url}\n\n"
        note += f"Content summary:\n{content}...\n\n"
        note += f"Key findings relevant to KYC for {client_name}:\n"
        note += "- Example finding 1\n"
        note += "- Example finding 2\n"
        
        return note