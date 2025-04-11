import asyncio
import hashlib
from typing import List, Dict, Any, Optional, Tuple, Set,Union
import logging
from urllib.parse import urljoin, urlparse

import aiohttp
from bs4 import BeautifulSoup
from langchain_community.document_loaders import RecursiveUrlLoader, WebBaseLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Models for structured output
class WebResearchNote(BaseModel):
    """Structured research note from web content"""
    source_url: str = Field(description="URL of the content source")
    summary: str = Field(description="Summary of key information from the source")
    key_findings: List[str] = Field(description="List of key findings relevant to KYC")
    risk_indicators: List[Dict[str, str]] = Field(
        description="Potential risk indicators found",
        default_factory=list
    )
    confidence: float = Field(
        description="Confidence in the findings (0.0-1.0)",
        ge=0.0,
        le=1.0
    )

class WebPageResearchResult(BaseModel):
    """Result from analyzing a web page"""
    url: str = Field(description="URL of the analyzed webpage")
    title: str = Field(description="Title of the webpage")
    research_note: WebResearchNote = Field(description="Structured research note from analysis")
    raw_content: Optional[str] = Field(description="Raw content from the webpage")
    extracted_links: List[str] = Field(
        description="URLs extracted from the webpage for further analysis",
        default_factory=list
    )

# Constants for research
MAX_LINKS_PER_PAGE = 5  # Maximum links to follow from a single page
MAX_PAGES_TOTAL = 20    # Maximum total pages to analyze
MAX_DEPTH = 2           # Maximum recursion depth
DEFAULT_TIMEOUT = 30    # Default timeout in seconds

class KYCWebResearcher:
    """
    Performs web research for KYC compliance purposes using recursive URL loading
    and summarization of web content.
    """
    
    def __init__(
        self,
        llm_model: str = "claude-3-5-sonnet-latest",
        temperature: float = 0.0,
        max_links_per_page: int = MAX_LINKS_PER_PAGE,
        max_pages_total: int = MAX_PAGES_TOTAL,
        max_depth: int = MAX_DEPTH,
        timeout: int = DEFAULT_TIMEOUT
    ):
        """
        Initialize the web researcher with configuration.
        
        Args:
            llm_model: Model to use for analysis and summarization
            temperature: Temperature for generation (0.0 for deterministic)
            max_links_per_page: Maximum links to follow from a single page
            max_pages_total: Maximum total pages to analyze
            max_depth: Maximum recursion depth
            timeout: Default timeout in seconds for HTTP requests
        """
        self.llm = ChatAnthropic(model=llm_model, temperature=temperature)
        self.max_links_per_page = max_links_per_page
        self.max_pages_total = max_pages_total
        self.max_depth = max_depth
        self.timeout = timeout
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=8000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        self.html2text = Html2TextTransformer()
        self.visited_urls = set()
        self.session = None  # Will be initialized in research method
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout))
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def research_client(
        self, 
        client_name: str,
        search_queries: List[str],
        risk_appetite_statement: str,
        initial_search_urls: Optional[List[str]] = None
    ) -> Tuple[List[WebPageResearchResult], List[str]]:
        """
        Perform comprehensive web research on a client.
        
        Args:
            client_name: Name of the client to research
            search_queries: List of search queries to use for initial research
            risk_appetite_statement: Risk appetite statement for context
            initial_search_urls: Optional list of URLs to start with
            
        Returns:
            Tuple containing:
            - List of WebPageResearchResult objects
            - List of research notes in text format
        """
        # Initialize session if not already done
        if not self.session:
            self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout))
        
        try:
            # Step 1: Get initial URLs from search queries if not provided
            if not initial_search_urls:
                # This would use a search API like Google, Bing, DuckDuckGo, Tavily, etc.
                # For demonstration, we'll simulate search results
                initial_search_urls = await self._simulate_search_results(search_queries)
            
            # Step 2: Research each URL recursively
            all_results = []
            for start_url in initial_search_urls[:10]:  # Limit to top 10 URLs for efficiency
                logger.info(f"Starting recursive exploration from: {start_url}")
                
                # Skip if we've reached maximum pages
                if len(all_results) >= self.max_pages_total:
                    logger.info(f"Reached maximum total pages ({self.max_pages_total})")
                    break
                
                # Process this URL and follow links recursively
                page_results = await self._process_url_recursively(
                    start_url, 
                    client_name,
                    risk_appetite_statement,
                    depth=0
                )
                all_results.extend(page_results)
            
            # Step 3: Convert research results to notes format
            research_notes = self._format_research_notes(all_results)
            
            return all_results, research_notes
            
        finally:
            # Close session if we created it here
            if self.session and not hasattr(self, '_session_from_context'):
                await self.session.close()
                self.session = None
    
    async def _simulate_search_results(self, search_queries: List[str]) -> List[str]:
        """
        Simulate search results for demonstration.
        In a real implementation, this would use a search API.
        
        Args:
            search_queries: List of search queries
            
        Returns:
            List of URLs from search results
        """
        # For demonstration, return fictional URLs
        # In a real implementation, use a search API like Google Custom Search, Tavily, etc.
        simulated_urls = [
            "https://example.com/company-profile",
            "https://example.com/financial-services",
            "https://example.com/news/recent-activities",
            "https://example.com/regulatory-filings",
            "https://example.com/about-us/leadership",
            "https://example.com/services/money-transfer",
            "https://example.com/compliance",
            "https://example.com/locations",
            "https://example.com/partnerships",
            "https://example.com/investor-relations",
        ]
        
        # In real implementation, append query-specific URLs:
        # for query in search_queries:
        #     # Encode query and use search API
        #     search_results = await search_api.search(query, max_results=5)
        #     simulated_urls.extend([r['url'] for r in search_results])
        
        return list(set(simulated_urls))  # Deduplicate
    
    async def _process_url_recursively(
        self,
        url: str,
        client_name: str,
        risk_appetite_statement: str,
        depth: int = 0,
        visited: Optional[Set[str]] = None
    ) -> List[WebPageResearchResult]:
        """
        Process a URL and recursively follow links up to max depth.
        
        Args:
            url: URL to process
            client_name: Name of client (for context in analysis)
            risk_appetite_statement: Risk appetite statement (for context in analysis)
            depth: Current recursion depth
            visited: Set of visited URLs (to avoid cycles)
            
        Returns:
            List of WebPageResearchResult objects
        """
        if visited is None:
            visited = set()
        
        # Skip if we've visited this URL already
        url_hash = hashlib.md5(url.encode()).hexdigest()
        if url_hash in visited:
            return []
        
        # Skip if we've reached maximum depth
        if depth > self.max_depth:
            return []
        
        # Add URL to visited set
        visited.add(url_hash)
        self.visited_urls.add(url)
        
        # Try to fetch and process the page
        try:
            # Fetch the page
            logger.info(f"Fetching URL (depth {depth}): {url}")
            
            # In a real implementation, use the session to fetch the page
            # For demonstration, simulate page content
            # page_content = await self._fetch_page(url)
            
            # Simulate page content for demonstration
            page_title = f"Example page for {url.split('/')[-1]}"
            page_content = f"""
            <html>
                <head><title>{page_title}</title></head>
                <body>
                    <h1>{page_title}</h1>
                    <p>This company provides financial services and money transfer capabilities.</p>
                    <p>They operate in multiple jurisdictions including the US, UK, and Canada.</p>
                    <div class="services">
                        <h2>Services</h2>
                        <ul>
                            <li>Currency exchange</li>
                            <li>International wire transfers</li>
                            <li>Corporate payment solutions</li>
                        </ul>
                    </div>
                    <div class="links">
                        <a href="https://example.com/about">About</a>
                        <a href="https://example.com/services">Services</a>
                        <a href="https://example.com/compliance">Compliance</a>
                        <a href="https://example.com/contact">Contact</a>
                    </div>
                </body>
            </html>
            """
            
            # Extract text and links
            clean_text, extracted_links = self._process_html(page_content, url)
            
            # Analyze page content for KYC relevance
            research_note = await self._analyze_page_content(
                url=url,
                title=page_title,
                text=clean_text,
                client_name=client_name,
                risk_appetite_statement=risk_appetite_statement
            )
            
            # Create research result
            result = WebPageResearchResult(
                url=url,
                title=page_title,
                research_note=research_note,
                raw_content=clean_text[:5000],  # Limit raw content size
                extracted_links=extracted_links[:self.max_links_per_page]
            )
            
            # Recursively process links if not at max depth
            results = [result]
            if depth < self.max_depth:
                # Process a limited number of links from this page
                links_to_process = extracted_links[:self.max_links_per_page]
                for link in links_to_process:
                    # Process link with increased depth
                    link_results = await self._process_url_recursively(
                        link, 
                        client_name,
                        risk_appetite_statement,
                        depth + 1,
                        visited
                    )
                    results.extend(link_results)
                    
                    # Check if we've reached total page limit
                    if len(results) >= self.max_pages_total:
                        break
            
            return results
        except Exception as e:
            logger.error(f"Error processing URL {url}: {str(e)}")
            return []
    
    async def _fetch_page(self, url: str) -> str:
        """
        Fetch a web page content.
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content as string
        """
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.warning(f"Failed to fetch {url}: HTTP {response.status}")
                    return ""
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return ""
    
    def _process_html(self, html: str, base_url: str) -> Tuple[str, List[str]]:
        """
        Process HTML to extract clean text and links.
        
        Args:
            html: HTML content
            base_url: Base URL for resolving relative links
            
        Returns:
            Tuple of (clean text, list of extracted links)
        """
        # Parse HTML
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract links
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            
            # Only include HTTP/HTTPS links
            parsed = urlparse(full_url)
            if parsed.scheme in ('http', 'https') and len(parsed.netloc) > 0:
                links.append(full_url)
        
        # Extract text
        # Option 1: Use BeautifulSoup directly
        text = soup.get_text(separator='\n', strip=True)
        
        # Option 2: Use Html2TextTransformer (better formatting)
        # doc = Document(page_content=html, metadata={"source": base_url})
        # transformed_docs = self.html2text.transform_documents([doc])
        # text = transformed_docs[0].page_content if transformed_docs else ""
        
        return text, links
    
    async def _analyze_page_content(
        self,
        url: str,
        title: str,
        text: str,
        client_name: str,
        risk_appetite_statement: str
    ) -> WebResearchNote:
        """
        Analyze page content for KYC relevance.
        
        Args:
            url: URL of the page
            title: Page title
            text: Clean text content
            client_name: Name of client (for context)
            risk_appetite_statement: Risk appetite statement (for context)
            
        Returns:
            WebResearchNote object with analysis
        """
        # Split text if too long
        if len(text) > 10000:
            text = text[:10000]  # Use first 10K chars for analysis
        
        # Create prompt for analysis
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=f"""
            You are a KYC (Know Your Customer) compliance analyst extracting relevant information from web pages.
            The client you are researching is: {client_name}
            
            Your task is to extract and summarize information that helps determine if this client is engaged in 
            prohibited or restricted activities according to our risk appetite statement.
            
            Prohibited activities include:
            - Illegal or illicit activities (arms dealing, unlawful drugs, adult entertainment, etc.)
            - Money laundering or terrorism financing
            - Unauthorized virtual currency exchanges
            - Unlicensed financial services
            
            Restricted activities requiring enhanced due diligence include:
            - Arms, defense, military
            - Cash-intensive businesses
            - Financial service providers
            - Offshore entities
            - Casino or gambling operations
            
            Analyze the provided web content for:
            1. Evidence of prohibited or restricted activities
            2. Geographic locations of operation (especially high-risk jurisdictions)
            3. Types of services or products offered
            4. Regulatory compliance information
            5. Ownership structure and key personnel
            """),
            HumanMessage(content=f"""
            URL: {url}
            Title: {title}
            
            Web Content:
            {text}
            
            Extract key information relevant to KYC compliance analysis.
            """)
        ])
        
        # Use structured LLM output
        analysis_result = await self.llm.with_structured_output(WebResearchNote).ainvoke(prompt)
        
        return analysis_result
    
    def _format_research_notes(self, results: List[WebPageResearchResult]) -> List[str]:
        """
        Format research results as text notes.
        
        Args:
            results: List of WebPageResearchResult objects
            
        Returns:
            List of formatted research notes
        """
        notes = []
        
        for idx, result in enumerate(results, 1):
            note = f"=== Research Note {idx} ===\n"
            note += f"Source: {result.url}\n"
            note += f"Title: {result.title}\n\n"
            
            # Add research note content
            note += f"Summary: {result.research_note.summary}\n\n"
            
            # Add key findings
            note += "Key Findings:\n"
            for i, finding in enumerate(result.research_note.key_findings, 1):
                note += f"{i}. {finding}\n"
            note += "\n"
            
            # Add risk indicators if present
            if result.research_note.risk_indicators:
                note += "Risk Indicators:\n"
                for indicator in result.research_note.risk_indicators:
                    note += f"• {indicator.get('type', 'Risk')}: {indicator.get('description', '')}\n"
                note += "\n"
            
            # Add confidence score
            note += f"Confidence: {result.research_note.confidence:.2f}\n"
            
            notes.append(note)
        
        return notes


class TavilySearch:
    """
    Simplified interface for Tavily search API.
    In a real implementation, this would use the actual Tavily API.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize with optional API key.
        
        Args:
            api_key: Optional Tavily API key
        """
        self.api_key = api_key
    
    async def search(
        self, 
        query: str, 
        max_results: int = 5,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform a search with Tavily.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            include_domains: Optional list of domains to include
            exclude_domains: Optional list of domains to exclude
            
        Returns:
            List of search result dictionaries
        """
        # In a real implementation, this would use the Tavily API
        # For demonstration, return simulated results
        
        # Simulate different results based on the query
        base_url = "https://example.com"
        if "financial" in query.lower():
            results = [
                {
                    "url": f"{base_url}/financial-services",
                    "title": "Financial Services Overview",
                    "content": "Overview of financial service offerings including money transfer."
                },
                {
                    "url": f"{base_url}/licenses",
                    "title": "Licenses and Regulations",
                    "content": "Information about financial licenses and regulatory compliance."
                }
            ]
        elif "compliance" in query.lower():
            results = [
                {
                    "url": f"{base_url}/compliance",
                    "title": "Compliance Framework",
                    "content": "Details about the compliance and risk management framework."
                },
                {
                    "url": f"{base_url}/aml-policy",
                    "title": "Anti-Money Laundering Policy",
                    "content": "Overview of anti-money laundering policies and procedures."
                }
            ]
        else:
            results = [
                {
                    "url": f"{base_url}/about",
                    "title": "About the Company",
                    "content": "General information about the company's history and activities."
                },
                {
                    "url": f"{base_url}/services",
                    "title": "Services Offered",
                    "content": "Details about the various services offered by the company."
                }
            ]
        
        # Add some generic results
        generic_results = [
            {
                "url": f"{base_url}/contact",
                "title": "Contact Information",
                "content": "Contact details and office locations."
            },
            {
                "url": f"{base_url}/news",
                "title": "Recent News",
                "content": "Recent news and announcements from the company."
            },
            {
                "url": f"{base_url}/team",
                "title": "Leadership Team",
                "content": "Profiles of the executive leadership team."
            }
        ]
        
        # Combine and limit results
        all_results = results + generic_results
        return all_results[:max_results]


# Function to deduplicate search results
def deduplicate_sources(search_response: Union[Dict[str, Any], List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """
    Deduplicate search results based on URL.
    
    Args:
        search_response: Search results from Tavily
        
    Returns:
        Deduplicated list of search results
    """
    # Convert input to list of results
    if isinstance(search_response, dict):
        sources_list = search_response.get("results", [])
    elif isinstance(search_response, list):
        sources_list = []
        for response in search_response:
            if isinstance(response, dict) and "results" in response:
                sources_list.extend(response["results"])
            else:
                sources_list.append(response)
    else:
        raise ValueError("Input must be either a dict with 'results' or a list of search results")
    
    # Deduplicate by URL
    unique_urls = set()
    unique_sources_list = []
    
    for source in sources_list:
        url = source.get("url")
        if url and url not in unique_urls:
            unique_urls.add(url)
            unique_sources_list.append(source)
    
    return unique_sources_list


# Example usage
async def main():
    # Create researcher
    async with KYCWebResearcher(max_depth=1, max_pages_total=5) as researcher:
        # Test search and research
        client_name = "Example Financial Services Inc."
        search_queries = [
            "Example Financial Services compliance",
            "Example Financial Services money laundering policy",
            "Example Financial Services business activities"
        ]
        
        risk_appetite = """
        Prohibited activities include:
        - Illegal or illicit activities (arms dealing, unlawful drugs, adult entertainment, etc.)
        - Money laundering or terrorism financing
        - Unauthorized virtual currency exchanges
        - Unlicensed financial services
        
        Restricted activities requiring enhanced due diligence include:
        - Arms, defense, military
        - Cash-intensive businesses
        - Financial service providers
        - Offshore entities
        - Casino or gambling operations
        """
        
        # Perform research
        results, notes = await researcher.research_client(
            client_name=client_name,
            search_queries=search_queries,
            risk_appetite_statement=risk_appetite
        )
        
        # Print results
        print(f"Researched {len(results)} pages")
        print(f"Generated {len(notes)} research notes")
        
        # Print first note
        if notes:
            print("\nSample Research Note:")
            print(notes[0])


if __name__ == "__main__":
    # Run example
    asyncio.run(main())