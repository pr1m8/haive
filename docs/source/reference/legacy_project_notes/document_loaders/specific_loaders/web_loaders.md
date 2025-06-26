# Web Content Loaders in Haive Framework

This document outlines the implementation of web content loaders in the Haive framework.

## Web Loader Options

LangChain provides several web content loader implementations, each with different characteristics:

| Loader              | Speed  | Quality | Features                  | Dependencies             |
| ------------------- | ------ | ------- | ------------------------- | ------------------------ |
| WebBaseLoader       | Fast   | Medium  | Basic HTML parsing        | requests, beautifulsoup4 |
| AsyncHtmlLoader     | Fast   | Medium  | Asynchronous loading      | aiohttp, beautifulsoup4  |
| PlaywrightURLLoader | Slow   | High    | JavaScript rendering      | playwright               |
| SeleniumURLLoader   | Slow   | Medium  | JavaScript rendering      | selenium                 |
| RecursiveUrlLoader  | Slow   | High    | Follows links recursively | beautifulsoup4           |
| SitemapLoader       | Medium | Medium  | Uses XML sitemaps         | beautifulsoup4           |
| GitHubFileLoader    | Medium | High    | GitHub specific           | -                        |
| WikipediaLoader     | Fast   | High    | Wikipedia specific        | wikipedia                |
| ArxivLoader         | Medium | High    | ArXiv specific            | arxiv, pypdf             |
| NewsURLLoader       | Medium | Medium  | News article extraction   | newspaper3k              |
| BraveSearchLoader   | Medium | Medium  | Search results            | requests                 |
| BrowserlessLoader   | Medium | High    | Hosted browser            | requests                 |

## Implementation Strategy

Our approach is to create a hierarchy of web sources with a base `WebPageSource` and specialized sources for specific websites:

```python
@auto_source
class WebPageSource(RemoteSource):
    """General web page source."""
    url: HttpUrl
    max_depth: int = 1
    javascript_needed: bool = False

    class Config:
        loader_strategies = {
            'basic': {
                'class': 'WebBaseLoader',
                'speed': 'fast',
                'quality': 'medium',
                'best_for': ['simple_pages']
            },
            'async': {
                'class': 'AsyncHtmlLoader',
                'speed': 'fast',
                'quality': 'medium',
                'best_for': ['multiple_pages']
            },
            'javascript': {
                'class': 'PlaywrightURLLoader',
                'speed': 'slow',
                'quality': 'high',
                'best_for': ['spa', 'dynamic']
            },
            'recursive': {
                'class': 'RecursiveUrlLoader',
                'speed': 'slow',
                'quality': 'high',
                'best_for': ['documentation', 'wikis']
            }
        }
```

### Specialized Web Sources

```python
@auto_source(domain_patterns=["github.com"])
class GitHubSource(WebPageSource):
    """GitHub repository source."""
    repo_url: HttpUrl
    include_issues: bool = True
    include_code: bool = True

    class Config:
        path_patterns = ["/*/*"]  # user/repo pattern
        loader_strategies = {
            'issues': {
                'class': 'GitHubIssuesLoader',
                'speed': 'medium',
                'quality': 'high',
                'best_for': ['issues', 'discussions'],
                'requires_auth': True,
                'required_credentials': ['github_token']
            },
            'file': {
                'class': 'GitHubFileLoader',
                'speed': 'medium',
                'quality': 'high',
                'best_for': ['code', 'documentation'],
                'requires_auth': True,
                'required_credentials': ['github_token']
            }
        }
        required_credentials = ['github_token']

@auto_source(domain_patterns=["wikipedia.org"])
class WikipediaSource(WebPageSource):
    """Wikipedia article source."""
    url: HttpUrl
    lang: str = "en"

    class Config:
        loader_strategies = {
            'wiki': {
                'class': 'WikipediaLoader',
                'speed': 'fast',
                'quality': 'high',
                'best_for': ['encyclopedia', 'articles']
            }
        }

@auto_source(domain_patterns=["arxiv.org"])
class ArxivSource(WebPageSource):
    """ArXiv paper source."""
    url: HttpUrl
    load_all_available_pdfs: bool = False

    class Config:
        loader_strategies = {
            'arxiv': {
                'class': 'ArxivLoader',
                'speed': 'medium',
                'quality': 'high',
                'best_for': ['scientific_papers', 'research']
            }
        }

@auto_source(domain_patterns=["youtube.com", "youtu.be"])
class YouTubeSource(WebPageSource):
    """YouTube video source."""
    video_url: HttpUrl
    include_transcript: bool = True

    class Config:
        loader_strategies = {
            'transcript': {
                'class': 'YoutubeLoader',
                'speed': 'medium',
                'quality': 'high',
                'best_for': ['transcripts', 'captions']
            },
            'audio': {
                'class': 'YoutubeAudioLoader',
                'speed': 'slow',
                'quality': 'medium',
                'best_for': ['audio', 'speech']
            }
        }
```

## Loader Implementation Details

### WebBaseLoader

```python
def create_web_base_loader(self):
    """Create a WebBaseLoader instance."""
    # Import here to avoid dependency issues
    from langchain_community.document_loaders import WebBaseLoader

    # Create and return the loader
    return WebBaseLoader(web_path=str(self.url))
```

### PlaywrightURLLoader

```python
def create_playwright_loader(self, **kwargs):
    """Create a PlaywrightURLLoader for JavaScript-heavy sites."""
    # Import here to avoid dependency issues
    from langchain_community.document_loaders import PlaywrightURLLoader

    # Default configuration
    config = {
        "remove_selectors": ["nav", "header", "footer"],  # Elements to remove
        "wait_until": "domcontentloaded",                 # When to consider page loaded
        "wait_for": 5000                                  # Max wait time in ms
    }

    # Update with any user-provided settings
    config.update(kwargs)

    # Create and return the loader
    return PlaywrightURLLoader(
        urls=[str(self.url)],
        remove_selectors=config["remove_selectors"],
        wait_until=config["wait_until"],
        wait_for=config["wait_for"]
    )
```

### RecursiveUrlLoader

```python
def create_recursive_loader(self, **kwargs):
    """Create a RecursiveUrlLoader for documentation sites."""
    # Import here to avoid dependency issues
    from langchain_community.document_loaders import RecursiveUrlLoader
    from bs4 import BeautifulSoup

    # Default configuration
    config = {
        "max_depth": self.max_depth,
        "extractor": lambda x: BeautifulSoup(x, "html.parser").text,
        "prevent_outside": True,   # Stay within the same domain
        "link_regex": None         # Filter links by regex if provided
    }

    # Update with any user-provided settings
    config.update(kwargs)

    # Create and return the loader
    return RecursiveUrlLoader(
        url=str(self.url),
        max_depth=config["max_depth"],
        extractor=config["extractor"],
        prevent_outside=config["prevent_outside"],
        link_regex=config["link_regex"]
    )
```

## Web Content Analysis

We'll implement analysis functions to determine the best loader:

```python
def analyze_webpage(self):
    """Analyze the web page to determine its characteristics."""
    # Import required libraries
    import requests
    from bs4 import BeautifulSoup
    import re

    # Initialize analysis results
    analysis = {
        "status_code": None,
        "has_html": False,
        "html_size": 0,
        "script_count": 0,
        "link_count": 0,
        "is_javascript_heavy": False,
        "has_sitemap": False,
        "likely_documentation": False,
        "likely_blog": False,
        "likely_news": False,
        "likely_spa": False
    }

    try:
        # Fetch the page with a timeout
        response = requests.get(str(self.url), timeout=10)
        analysis["status_code"] = response.status_code

        # If not successful, return limited analysis
        if response.status_code != 200:
            return analysis

        # Check content type
        content_type = response.headers.get('Content-Type', '').lower()
        analysis["has_html"] = 'text/html' in content_type

        # If not HTML, return limited analysis
        if not analysis["has_html"]:
            return analysis

        # Parse HTML
        html_content = response.text
        analysis["html_size"] = len(html_content)
        soup = BeautifulSoup(html_content, 'html.parser')

        # Count scripts
        scripts = soup.find_all('script')
        analysis["script_count"] = len(scripts)

        # Determine if JavaScript-heavy
        analysis["is_javascript_heavy"] = (
            analysis["script_count"] > 10 or
            'react' in html_content.lower() or
            'vue' in html_content.lower() or
            'angular' in html_content.lower() or
            'spa' in html_content.lower()
        )

        # Count links
        links = soup.find_all('a', href=True)
        analysis["link_count"] = len(links)

        # Check for sitemap
        try:
            sitemap_response = requests.head(f"{self.url.scheme}://{self.url.netloc}/sitemap.xml", timeout=5)
            analysis["has_sitemap"] = sitemap_response.status_code == 200
        except:
            pass

        # Check for documentation patterns
        analysis["likely_documentation"] = (
            '/docs/' in str(self.url) or
            '/documentation/' in str(self.url) or
            '/guide/' in str(self.url) or
            '/help/' in str(self.url) or
            'documentation' in soup.title.text.lower() if soup.title else False
        )

        # Check for blog patterns
        analysis["likely_blog"] = (
            '/blog/' in str(self.url) or
            'blog' in soup.title.text.lower() if soup.title else False
        )

        # Check for news patterns
        analysis["likely_news"] = (
            '/news/' in str(self.url) or
            '/article/' in str(self.url) or
            'news' in soup.title.text.lower() if soup.title else False or
            any(h.name in ['h1', 'h2'] and 'news' in h.text.lower() for h in soup.find_all(['h1', 'h2']))
        )

        # Check for SPA patterns
        analysis["likely_spa"] = (
            soup.find('div', id='app') is not None or
            soup.find('div', id='root') is not None or
            analysis["is_javascript_heavy"]
        )

        return analysis

    except Exception as e:
        analysis["error"] = str(e)
        return analysis
```

## Auto-Selection Logic

We'll implement logic to select the most appropriate loader based on the web page analysis:

```python
def select_best_loader(self, criteria=None):
    """Select the best loader based on web page analysis and criteria."""
    criteria = criteria or {}
    prefer_speed = criteria.get("prefer_speed", False)
    prefer_quality = criteria.get("prefer_quality", False)

    # Check if we already know this is a special domain
    if isinstance(self, GitHubSource):
        return 'issues' if self.include_issues else 'file'
    elif isinstance(self, WikipediaSource):
        return 'wiki'
    elif isinstance(self, ArxivSource):
        return 'arxiv'
    elif isinstance(self, YouTubeSource):
        return 'transcript' if self.include_transcript else 'audio'

    # For general web pages, analyze first
    analysis = self.analyze_webpage()

    # Select loader based on analysis
    if self.javascript_needed or analysis["is_javascript_heavy"] or analysis["likely_spa"]:
        return 'javascript'  # Use PlaywrightURLLoader for JS-heavy sites

    elif analysis["likely_documentation"] and self.max_depth > 1:
        return 'recursive'   # Use RecursiveUrlLoader for documentation

    elif prefer_speed:
        return 'basic'       # Use WebBaseLoader for speed

    elif prefer_quality:
        if analysis["link_count"] > 20:  # Many links suggest documentation
            return 'recursive'
        else:
            return 'javascript'  # Best quality for most sites

    # Default to basic loader
    return 'basic'
```

## Authentication Handling

Many web sources require authentication. We'll implement credential management:

```python
def authenticate_github(self, credential_manager):
    """Authenticate for GitHub API access."""
    if not credential_manager:
        return False

    github_token = credential_manager.get_credential('github_token')
    if not github_token:
        return False

    self.github_token = github_token.get('value')
    self.is_authenticated = bool(self.github_token)

    return self.is_authenticated

def create_github_loader(self):
    """Create a GitHub loader with authentication."""
    from langchain_community.document_loaders import GitHubFileLoader

    # Headers for authentication
    headers = {}
    if hasattr(self, 'github_token') and self.github_token:
        headers["Authorization"] = f"token {self.github_token}"

    # Parse GitHub URL to get owner, repo, and path
    path_segments = self.url.path.split('/')
    if len(path_segments) >= 3:
        owner = path_segments[1]
        repo = path_segments[2]
        branch = 'main'  # Default branch

        return GitHubFileLoader(
            owner=owner,
            repo=repo,
            branch=branch,
            headers=headers
        )

    # Fallback to web loader if URL format is unexpected
    return self.create_web_base_loader()
```

## Rate Limiting and Politeness

Web scrapers need to be polite. We'll implement rate limiting:

```python
def apply_rate_limiting(self):
    """Apply rate limiting to be polite to the server."""
    import time
    import random
    from urllib.parse import urlparse

    # Static class dictionary to track last access time per domain
    if not hasattr(WebPageSource, '_last_access'):
        WebPageSource._last_access = {}

    # Get domain from URL
    domain = urlparse(str(self.url)).netloc

    # Check if we recently accessed this domain
    if domain in WebPageSource._last_access:
        last_time = WebPageSource._last_access[domain]
        current_time = time.time()
        elapsed = current_time - last_time

        # If less than 1 second has passed, wait
        if elapsed < 1:
            # Random delay between 1-2 seconds
            delay = 1 + random.random()
            time.sleep(delay)

    # Update last access time
    WebPageSource._last_access[domain] = time.time()
```

## Full Implementation

The complete web loader implementation will include:

1. Base `WebPageSource` class
2. Specialized sources for popular websites
3. Web page analysis capabilities
4. Auto-selection logic
5. Authentication handling
6. Rate limiting and politeness features

This provides a robust and flexible approach to web content loading that can adapt to different websites and user needs.

## Usage Examples

### Basic Usage

```python
from haive.document_loaders import WebPageSource

# Create a web page source
web_source = WebPageSource(url="https://example.com")

# Load the page with auto-selected strategy
documents = web_source.load_documents()
```

### With JavaScript Rendering

```python
# Specify that JavaScript is needed
web_source = WebPageSource(
    url="https://example.com/spa",
    javascript_needed=True
)

# Load with JavaScript rendering
documents = web_source.load_documents()
```

### Recursive Loading

```python
# Set depth for recursive loading
web_source = WebPageSource(
    url="https://example.com/docs",
    max_depth=3
)

# Load recursively
documents = web_source.load_documents()
```

### Specialized Sites

```python
from haive.document_loaders import GitHubSource, CredentialManager

# Create a credential manager
credential_manager = CredentialManager()

# Add GitHub token
credential_manager.store_credential(
    "github_token",
    {"type": "api_key", "value": "your-github-token"}
)

# Create GitHub source
github_source = GitHubSource(
    url="https://github.com/user/repo",
    include_issues=True
)

# Authenticate
github_source.authenticate(credential_manager)

# Load repository content
documents = github_source.load_documents()
```

## Conclusion

This implementation provides a comprehensive approach to web content loading that leverages all available LangChain loaders while adding intelligent selection, authentication, and analysis capabilities.

## Status

- ⬜ Core `WebPageSource` implementation
- ⬜ Specialized web sources
- ⬜ Web page analysis functions
- ⬜ Auto-selection logic
- ⬜ Authentication handling
- ⬜ Rate limiting implementation
- ⬜ Testing and validation
