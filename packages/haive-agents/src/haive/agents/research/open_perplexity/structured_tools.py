import os
import re
from datetime import datetime
from typing import Any

from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Import LangChain document loaders
from langchain_community.document_loaders import (
    ArxivLoader,
    GitHubIssuesLoader,
    HNLoader,
    RecursiveUrlLoader,
    WebBaseLoader,
)
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

# Import search tools
try:
    from langchain_community.tools.tavily_search import TavilySearchResults
    from tavily import TavilyClient
except ImportError:
    # Provide fallbacks if Tavily not available
    pass

# Load environment variables
load_dotenv(dotenv_path=".env")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Dynamic document loader registry
DOCUMENT_LOADERS = {}


def register_document_loader(loader_type: str):
    """Decorator to register document loaders with metadata"""

    def decorator(loader_class):
        DOCUMENT_LOADERS[loader_type] = {
            "class": loader_class,
            "metadata": getattr(loader_class, "loader_metadata", {}),
        }
        return loader_class

    return decorator


# Metadata for each loader type
@register_document_loader("web")
class EnhancedWebBaseLoader(WebBaseLoader):
    """Enhanced web page loader with metadata extraction"""

    loader_metadata = {
        "name": "Web Page Loader",
        "description": "Loads content from web pages",
        "best_for": ["news articles", "blog posts", "web content"],
        "source_type": "web",
        "structured_data": False,
        "parameters": ["url"],
    }

    def __init__(self, web_path):
        super().__init__(web_path)
        self.web_path = web_path

    def load(self):
        """Override load method to add metadata"""
        docs = super().load()
        for doc in docs:
            # Add enhanced metadata
            doc.metadata.update(
                {
                    "source_type": "web",
                    "url": self.web_path,
                    "access_time": datetime.now().isoformat(),
                    "loader_type": "web",
                }
            )
        return docs


@register_document_loader("recursive_web")
class EnhancedRecursiveUrlLoader(RecursiveUrlLoader):
    """Enhanced recursive web crawler with metadata extraction"""

    loader_metadata = {
        "name": "Recursive Web Crawler",
        "description": "Recursively crawls websites starting from a URL",
        "best_for": ["company websites", "documentation", "interconnected content"],
        "source_type": "web",
        "structured_data": False,
        "parameters": ["url", "max_depth"],
    }

    def __init__(self, url, max_depth=2, extractor=None, prevent_outside=True):
        # Use BS4 extractor if not provided
        if extractor is None:
            extractor = self._default_extractor

        super().__init__(
            url=url,
            max_depth=max_depth,
            extractor=extractor,
            prevent_outside=prevent_outside,
            check_response_status=True,
            continue_on_failure=True,
        )
        self.root_url = url

    @staticmethod
    def _default_extractor(html):
        """Default extractor using BeautifulSoup"""
        soup = BeautifulSoup(html, "html.parser")

        # Remove script and style elements
        for script in soup(["script", "style", "header", "footer", "nav"]):
            script.extract()

        # Get text
        text = soup.get_text(separator="\n")

        # Clean up text - remove excessive newlines
        text = re.sub(r"\n\s*\n", "\n\n", text)

        return text.strip()

    def load(self):
        """Override load method to add metadata"""
        docs = super().load()
        for doc in docs:
            # Add enhanced metadata
            doc.metadata.update(
                {
                    "source_type": "web",
                    "root_url": self.root_url,
                    "crawl_depth": doc.metadata.get("depth", 0),
                    "access_time": datetime.now().isoformat(),
                    "loader_type": "recursive_web",
                }
            )
        return docs


@register_document_loader("github")
class EnhancedGitHubIssuesLoader(GitHubIssuesLoader):
    """Enhanced GitHub issues loader with metadata extraction"""

    loader_metadata = {
        "name": "GitHub Issues Loader",
        "description": "Loads issues from GitHub repositories",
        "best_for": [
            "software development",
            "open source projects",
            "bug reports",
            "feature requests",
        ],
        "source_type": "github",
        "structured_data": True,
        "parameters": ["repo", "access_token"],
    }

    def load(self):
        """Override load method to add metadata"""
        docs = super().load()
        for doc in docs:
            # Add enhanced metadata
            doc.metadata.update(
                {
                    "source_type": "github",
                    "access_time": datetime.now().isoformat(),
                    "loader_type": "github",
                    "platform": "GitHub",
                    "content_type": "issues",
                }
            )
        return docs


@register_document_loader("arxiv")
class EnhancedArxivLoader(ArxivLoader):
    """Enhanced Arxiv paper loader with metadata extraction"""

    loader_metadata = {
        "name": "ArXiv Papers Loader",
        "description": "Loads academic papers from ArXiv",
        "best_for": ["academic research", "scientific papers", "technical topics"],
        "source_type": "academic",
        "structured_data": False,
        "parameters": ["query", "load_all_available_meta"],
    }

    def load(self):
        """Override load method to add metadata"""
        docs = super().load()
        for doc in docs:
            # Add enhanced metadata
            doc.metadata.update(
                {
                    "source_type": "academic",
                    "platform": "ArXiv",
                    "access_time": datetime.now().isoformat(),
                    "loader_type": "arxiv",
                    "content_type": "research_paper",
                }
            )
        return docs


@register_document_loader("hackernews")
class EnhancedHNLoader(HNLoader):
    """Enhanced Hacker News loader with metadata extraction"""

    loader_metadata = {
        "name": "Hacker News Loader",
        "description": "Loads posts and comments from Hacker News",
        "best_for": [
            "technology news",
            "tech community discussions",
            "startup information",
        ],
        "source_type": "news",
        "structured_data": True,
        "parameters": ["story_id"],
    }

    def load(self):
        """Override load method to add metadata"""
        docs = super().load()
        for doc in docs:
            # Add enhanced metadata
            doc.metadata.update(
                {
                    "source_type": "news",
                    "platform": "Hacker News",
                    "access_time": datetime.now().isoformat(),
                    "loader_type": "hackernews",
                    "content_type": "forum_discussion",
                }
            )
        return docs


# Document Loader Selection Tool Schemas
class DocumentLoaderDescriptionInput(BaseModel):
    """Input for document loader description"""

    loader_type: str = Field(description="Type of document loader to describe")


class DocumentLoaderRecommendationInput(BaseModel):
    """Input for document loader recommendation"""

    research_topic: str = Field(
        description="Research topic to find appropriate loaders for"
    )
    research_question: str | None = Field(
        None, description="Specific research question"
    )
    data_types: list[str] | None = Field(
        None, description="Types of data needed (web, academic, news, etc.)"
    )


class WebLoaderInput(BaseModel):
    """Input for web page loader"""

    url: str = Field(description="URL of the web page to load")


class RecursiveWebLoaderInput(BaseModel):
    """Input for recursive web loader"""

    url: str = Field(description="Root URL to crawl")
    max_depth: int = Field(2, description="Maximum crawl depth (1-3 recommended)")
    prevent_outside: bool = Field(
        True, description="Only crawl URLs on the same domain"
    )


class ArxivLoaderInput(BaseModel):
    """Input for ArXiv loader"""

    query: str = Field(description="Query to search for papers on ArXiv")
    max_results: int = Field(5, description="Maximum number of papers to return")
    load_all_available_meta: bool = Field(
        True, description="Load all available metadata for papers"
    )


class GitHubIssuesLoaderInput(BaseModel):
    """Input for GitHub issues loader"""

    repo: str = Field(description="GitHub repository in format 'owner/repo'")
    access_token: str | None = Field(
        None, description="GitHub access token for private repos"
    )
    state: str = Field("open", description="Issue state: 'open', 'closed', or 'all'")


class HackerNewsLoaderInput(BaseModel):
    """Input for Hacker News loader"""

    story_id: int = Field(description="ID of the Hacker News story to load")


# Dynamic document loader functions
def get_available_loaders() -> dict[str, dict]:
    """Get all available document loaders with their metadata"""
    return DOCUMENT_LOADERS


def describe_document_loader(loader_type: str) -> dict[str, Any]:
    """Get detailed description of a document loader"""
    if loader_type not in DOCUMENT_LOADERS:
        return {"error": f"Loader type '{loader_type}' not found"}

    loader_info = DOCUMENT_LOADERS[loader_type]
    return {
        "type": loader_type,
        "metadata": loader_info.get("metadata", {}),
        "parameters": loader_info.get("metadata", {}).get("parameters", []),
    }


def recommend_document_loaders(
    research_topic: str,
    research_question: str | None = None,
    data_types: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Recommend document loaders based on research topic and question"""
    # Get all available loaders
    loaders = get_available_loaders()

    # Filter by data types if specified
    if data_types:
        filtered_loaders = {}
        for loader_type, loader_info in loaders.items():
            source_type = loader_info.get("metadata", {}).get("source_type")
            if source_type in data_types:
                filtered_loaders[loader_type] = loader_info
        loaders = filtered_loaders

    # Return recommendations
    recommendations = []
    for loader_type, loader_info in loaders.items():
        metadata = loader_info.get("metadata", {})
        recommendations.append(
            {
                "type": loader_type,
                "name": metadata.get("name", loader_type),
                "description": metadata.get("description", ""),
                "best_for": metadata.get("best_for", []),
                "source_type": metadata.get("source_type", "unknown"),
            }
        )

    return recommendations


# Document loader execution functions
def load_web_page(url: str) -> list[dict[str, Any]]:
    """Load content from a web page"""
    try:
        loader = EnhancedWebBaseLoader(url)
        docs = loader.load()

        # Convert to serializable format
        results = []
        for doc in docs:
            results.append(
                {
                    "content": (
                        doc.page_content[:2000] + "..."
                        if len(doc.page_content) > 2000
                        else doc.page_content
                    ),
                    "metadata": doc.metadata,
                }
            )

        return {"documents": results, "source": url, "document_count": len(results)}
    except Exception as e:
        return {"error": str(e)}


def load_recursive_web(
    url: str, max_depth: int = 2, prevent_outside: bool = True
) -> dict[str, Any]:
    """Recursively crawl a website"""
    try:
        loader = EnhancedRecursiveUrlLoader(
            url=url, max_depth=max_depth, prevent_outside=prevent_outside
        )
        docs = loader.load()

        # Convert to serializable format with page summaries
        results = []
        for doc in docs:
            # Add a summary for each page
            content = doc.page_content
            summary = content[:1000] + "..." if len(content) > 1000 else content

            results.append(
                {
                    "url": doc.metadata.get("source", "Unknown"),
                    "summary": summary,
                    "metadata": doc.metadata,
                }
            )

        return {
            "documents": results,
            "root_url": url,
            "document_count": len(results),
            "max_depth_reached": (
                max(doc.metadata.get("depth", 0) for doc in docs) if docs else 0
            ),
        }
    except Exception as e:
        return {"error": str(e)}


def load_arxiv_papers(
    query: str, max_results: int = 5, load_all_available_meta: bool = True
) -> dict[str, Any]:
    """Load papers from ArXiv"""
    try:
        loader = EnhancedArxivLoader(
            query=query,
            load_all_available_meta=load_all_available_meta,
            max_results=max_results,
        )
        docs = loader.load()

        # Convert to serializable format
        results = []
        for doc in docs:
            # Extract key metadata for papers
            meta = doc.metadata
            paper_info = {
                "title": meta.get("Title", "Unknown"),
                "authors": meta.get("Authors", "Unknown"),
                "summary": meta.get("Summary", "No summary available"),
                "published": meta.get("Published", "Unknown date"),
                "url": meta.get("entry_id", ""),
            }

            # Add abbreviated content
            content_preview = (
                doc.page_content[:1500] + "..."
                if len(doc.page_content) > 1500
                else doc.page_content
            )

            results.append(
                {"paper_info": paper_info, "content_preview": content_preview}
            )

        return {"papers": results, "query": query, "paper_count": len(results)}
    except Exception as e:
        return {"error": str(e)}


def load_github_issues(
    repo: str, access_token: str | None = None, state: str = "open"
) -> dict[str, Any]:
    """Load issues from a GitHub repository"""
    try:
        if access_token:
            os.environ["GITHUB_TOKEN"] = access_token

        loader = EnhancedGitHubIssuesLoader(repo=repo, state=state)
        docs = loader.load()

        # Convert to serializable format
        results = []
        for doc in docs:
            # Extract issue info
            meta = doc.metadata
            issue_info = {
                "issue_number": meta.get("number", "Unknown"),
                "title": meta.get("title", "Unknown"),
                "state": meta.get("state", "Unknown"),
                "created_at": meta.get("created_at", "Unknown"),
                "updated_at": meta.get("updated_at", "Unknown"),
                "url": meta.get("html_url", ""),
            }

            results.append(
                {
                    "issue_info": issue_info,
                    "content": (
                        doc.page_content[:1000] + "..."
                        if len(doc.page_content) > 1000
                        else doc.page_content
                    ),
                }
            )

        return {
            "issues": results,
            "repository": repo,
            "issue_count": len(results),
            "state_filter": state,
        }
    except Exception as e:
        return {"error": str(e)}


def load_hackernews_thread(story_id: int) -> dict[str, Any]:
    """Load a Hacker News thread"""
    try:
        loader = EnhancedHNLoader(story_id=story_id)
        docs = loader.load()

        # Convert to serializable format
        results = []
        story_info = {}

        for doc in docs:
            meta = doc.metadata
            comment_info = {
                "id": meta.get("id", "Unknown"),
                "author": meta.get("author", "Unknown"),
                "created_at": meta.get("created_at", "Unknown"),
                "depth": meta.get("depth", 0),
            }

            # Extract story info from first document
            if not story_info and meta.get("is_story", False):
                story_info = {
                    "title": meta.get("title", "Unknown"),
                    "url": meta.get("url", ""),
                    "points": meta.get("points", 0),
                    "author": meta.get("author", "Unknown"),
                    "created_at": meta.get("created_at", "Unknown"),
                }

            results.append({"comment_info": comment_info, "content": doc.page_content})

        return {
            "story": story_info,
            "comments": results,
            "story_id": story_id,
            "comment_count": len(results),
        }
    except Exception as e:
        return {"error": str(e)}


# Create structured tools for research
document_loader_description_tool = StructuredTool.from_function(
    func=describe_document_loader,
    name="document_loader_description",
    description="Get detailed information about a specific document loader",
    args_schema=DocumentLoaderDescriptionInput,
)

recommend_document_loaders_tool = StructuredTool.from_function(
    func=recommend_document_loaders,
    name="recommend_document_loaders",
    description="Recommend document loaders based on research topic and question",
    args_schema=DocumentLoaderRecommendationInput,
)

web_loader_tool = StructuredTool.from_function(
    func=load_web_page,
    name="web_loader",
    description="Load and extract content from a web page",
    args_schema=WebLoaderInput,
)

recursive_web_loader_tool = StructuredTool.from_function(
    func=load_recursive_web,
    name="recursive_web_loader",
    description="Recursively crawl a website to extract content from multiple pages",
    args_schema=RecursiveWebLoaderInput,
)

arxiv_loader_tool = StructuredTool.from_function(
    func=load_arxiv_papers,
    name="arxiv_loader",
    description="Search and load academic papers from ArXiv repository",
    args_schema=ArxivLoaderInput,
)

github_issues_loader_tool = StructuredTool.from_function(
    func=load_github_issues,
    name="github_issues_loader",
    description="Load issues from a GitHub repository",
    args_schema=GitHubIssuesLoaderInput,
)

hackernews_loader_tool = StructuredTool.from_function(
    func=load_hackernews_thread,
    name="hackernews_loader",
    description="Load a discussion thread from Hacker News",
    args_schema=HackerNewsLoaderInput,
)

# Tavily search tools (if available)
try:

    class TavilySearchInput(BaseModel):
        """Input for Tavily search"""

        query: str = Field(description="Search query")
        max_results: int | None = Field(
            5, description="Maximum number of results to return"
        )
        search_depth: str | None = Field(
            "basic", description="Search depth (basic or comprehensive)"
        )

    def tavily_search(
        query: str, max_results: int = 5, search_depth: str = "basic"
    ) -> dict[str, Any]:
        """Search the web using Tavily"""
        try:
            client = TavilyClient(api_key=TAVILY_API_KEY)
            response = client.search(
                query=query, search_depth=search_depth, max_results=max_results
            )
            return response
        except Exception as e:
            return {"error": str(e)}

    tavily_search_tool = StructuredTool.from_function(
        func=tavily_search,
        name="tavily_search",
        description="Search the web for information on research topics",
        args_schema=TavilySearchInput,
    )

    SEARCH_TOOLS = [tavily_search_tool]
except (ImportError, NameError):
    SEARCH_TOOLS = []

# Combined document loader tools
DOCUMENT_LOADER_TOOLS = [
    document_loader_description_tool,
    recommend_document_loaders_tool,
    web_loader_tool,
    recursive_web_loader_tool,
    arxiv_loader_tool,
    github_issues_loader_tool,
    hackernews_loader_tool,
]

# Final list of all research tools
RESEARCH_TOOLS = DOCUMENT_LOADER_TOOLS + SEARCH_TOOLS
