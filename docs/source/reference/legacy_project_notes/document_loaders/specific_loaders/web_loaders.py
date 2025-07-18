"""
Web-based Document Loaders for Haive Framework

This module implements various web-based document loaders including AsyncHtmlLoader,
SeleniumURLLoader, PlaywrightURLLoader, and specialized web source loaders.
"""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

from pydantic import Field, HttpUrl

from ..source_implementation import (
    BaseSource,
    CredentialManager,
    RemoteSource,
    auto_source,
)


@auto_source
class WebPageSource(RemoteSource):
    """General web page source."""
    url: HttpUrl
    max_depth: int = 1
    javascript_needed: bool = False
    headers: Optional[Dict[str, str]] = None

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
            'selenium': {
                'class': 'SeleniumURLLoader',
                'speed': 'slow',
                'quality': 'medium',
                'best_for': ['javascript_heavy']
            },
            'recursive': {
                'class': 'RecursiveUrlLoader',
                'speed': 'slow',
                'quality': 'high',
                'best_for': ['documentation', 'wikis']
            },
            'sitemap': {
                'class': 'SitemapLoader',
                'speed': 'medium',
                'quality': 'medium',
                'best_for': ['websites', 'blogs']
            }
        }

    def create_basic_loader(self):
        """Create a WebBaseLoader instance."""
        try:
            from langchain_community.document_loaders import WebBaseLoader
            return WebBaseLoader(
                web_path=str(self.url),
                header_template=self.headers or {}
            )
        except ImportError:
            # Fallback to requests + BeautifulSoup if available
            try:
                import requests
                from bs4 import BeautifulSoup

                response = requests.get(
                    str(self.url),
                    headers=self.headers or {"User-Agent": "Mozilla/5.0"}
                )
                soup = BeautifulSoup(response.text, "html.parser")

                # Extract text content
                text = soup.get_text(separator='\n')

                # Create document
                from langchain_core.documents import Document
                return [Document(
                    page_content=text,
                    metadata={"source": str(self.url)}
                )]
            except ImportError:
                # If all else fails, return empty document
                from langchain_core.documents import Document
                return [Document(
                    page_content="[Unable to load web page: missing dependencies]",
                    metadata={"source": str(self.url)}
                )]

    def create_async_loader(self):
        """Create an AsyncHtmlLoader for faster loading of multiple pages."""
        try:
            from langchain_community.document_loaders import (
                AsyncChromiumLoader,
                AsyncHtmlLoader,
            )
            from langchain_community.document_transformers import (
                BeautifulSoupTransformer,
            )

            # Create loader
            loader = AsyncHtmlLoader([str(self.url)])

            # Load documents
            docs = loader.load()

            # Transform with BeautifulSoup
            bs_transformer = BeautifulSoupTransformer()
            docs_transformed = bs_transformer.transform_documents(docs)

            return docs_transformed
        except ImportError:
            # Fallback to basic loader
            return self.create_basic_loader()

    def create_javascript_loader(self):
        """Create a PlaywrightURLLoader for JavaScript-heavy sites."""
        try:
            from langchain_community.document_loaders import PlaywrightURLLoader

            # Default configuration for most sites
            return PlaywrightURLLoader(
                urls=[str(self.url)],
                remove_selectors=["nav", "header", "footer"],
                wait_until="domcontentloaded",
                wait_for=5000  # 5 seconds
            )
        except ImportError:
            # Try Selenium as fallback
            try:
                return self.create_selenium_loader()
            except ImportError:
                # If both fail, use basic loader
                return self.create_basic_loader()

    def create_selenium_loader(self):
        """Create a SeleniumURLLoader for JavaScript-rendered content."""
        try:
            from langchain_community.document_loaders import SeleniumURLLoader

            return SeleniumURLLoader(
                urls=[str(self.url)],
                continue_on_failure=True
            )
        except ImportError:
            # Fallback to basic loader
            return self.create_basic_loader()

    def create_recursive_loader(self):
        """Create a RecursiveUrlLoader for documentation sites."""
        try:
            from bs4 import BeautifulSoup
            from langchain_community.document_loaders import RecursiveUrlLoader

            # Extract text from HTML
            def extract_text(html):
                soup = BeautifulSoup(html, "html.parser")
                return soup.get_text(separator='\n')

            return RecursiveUrlLoader(
                url=str(self.url),
                max_depth=self.max_depth,
                extractor=extract_text,
                prevent_outside=True  # Stay within the same domain
            )
        except ImportError:
            # Fallback to basic loader
            return self.create_basic_loader()

    def create_sitemap_loader(self):
        """Create a SitemapLoader to process websites with sitemaps."""
        try:
            from langchain_community.document_loaders import SitemapLoader

            # Parse the domain from URL
            parsed_url = urlparse(str(self.url))
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

            # Try to determine sitemap URL
            sitemap_url = f"{base_url}/sitemap.xml"

            return SitemapLoader(
                sitemap_url=sitemap_url,
                filter_urls=[base_url],  # Only process URLs from the same domain
                parsing_function=None  # Use default
            )
        except ImportError:
            # Fallback to basic loader
            return self.create_basic_loader()

    def analyze_webpage(self):
        """Analyze the web page to determine its characteristics."""
        try:
            import re

            import requests
            from bs4 import BeautifulSoup

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

            # Fetch the page with a timeout
            headers = self.headers or {"User-Agent": "Mozilla/5.0"}
            response = requests.get(str(self.url), headers=headers, timeout=10)
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
                parsed_url = urlparse(str(self.url))
                base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                sitemap_response = requests.head(f"{base_url}/sitemap.xml", timeout=5)
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
            return {"error": str(e)}

    def select_best_loader(self, criteria=None):
        """Select the best loader based on web page analysis and criteria."""
        criteria = criteria or {}
        prefer_speed = criteria.get("prefer_speed", False)
        prefer_quality = criteria.get("prefer_quality", False)

        # For general web pages, analyze first
        analysis = self.analyze_webpage()

        # Select loader based on analysis
        if self.javascript_needed or analysis.get("is_javascript_heavy") or analysis.get("likely_spa"):
            return 'javascript'  # Use PlaywrightURLLoader for JS-heavy sites

        elif analysis.get("has_sitemap") and analysis.get("link_count", 0) > 10:
            return 'sitemap'  # Use SitemapLoader for sites with sitemaps

        elif analysis.get("likely_documentation") and self.max_depth > 1:
            return 'recursive'  # Use RecursiveUrlLoader for documentation

        elif prefer_speed:
            return 'basic'  # Use WebBaseLoader for speed

        elif prefer_quality:
            if analysis.get("link_count", 0) > 20:  # Many links suggest documentation
                return 'recursive'
            else:
                return 'javascript'  # Best quality for most sites

        # Default to basic loader
        return 'basic'

    def apply_rate_limiting(self):
        """Apply rate limiting to be polite to the server."""
        import random
        import time
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

    def create_loader(self, strategy_name=None):
        """Override to apply rate limiting and auto-select strategy if needed."""
        # Apply rate limiting
        self.apply_rate_limiting()

        # Auto-select strategy if not specified
        if strategy_name is None:
            strategy_name = self.select_best_loader()

        # Create loader with selected strategy
        return super().create_loader(strategy_name)


@auto_source(domain_patterns=["github.com"])
class GitHubSource(RemoteSource):
    """GitHub source for repositories, issues, files, commits, and pull requests."""
    url: HttpUrl
    include_issues: bool = True
    include_pull_requests: bool = True
    include_code: bool = True
    include_commits: bool = False
    branch: str = "main"

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
            },
            'repo': {
                'class': 'GitHubRepoLoader',
                'speed': 'slow',
                'quality': 'high',
                'best_for': ['repository', 'codebase'],
                'requires_auth': True,
                'required_credentials': ['github_token']
            },
            'pulls': {
                'class': 'GitHubPRLoader',
                'speed': 'medium',
                'quality': 'high',
                'best_for': ['pull_requests', 'code_reviews'],
                'requires_auth': True,
                'required_credentials': ['github_token']
            },
            'commits': {
                'class': 'GitHubCommitLoader',
                'speed': 'medium',
                'quality': 'high',
                'best_for': ['commits', 'history'],
                'requires_auth': True,
                'required_credentials': ['github_token']
            }
        }
        required_credentials = ['github_token']

    def authenticate(self, credential_manager: Optional[CredentialManager] = None) -> bool:
        """Authenticate for GitHub API access."""
        if not credential_manager:
            return False

        github_token = credential_manager.get_credential('github_token')
        if not github_token:
            return False

        self.github_token = github_token.get('value')
        self.is_authenticated = bool(self.github_token)

        return self.is_authenticated

    def _parse_github_url(self):
        """Parse GitHub URL to extract owner, repo, and path."""
        parsed_url = urlparse(str(self.url))
        path_segments = parsed_url.path.strip('/').split('/')

        if len(path_segments) >= 2:
            owner = path_segments[0]
            repo = path_segments[1]

            # Extract additional path components
            path = '/'.join(path_segments[2:]) if len(path_segments) > 2 else None

            return {
                'owner': owner,
                'repo': repo,
                'path': path
            }
        return None

    def create_issues_loader(self):
        """Create a GitHubIssuesLoader."""
        try:
            from langchain_community.document_loaders import GitHubIssuesLoader

            # Parse GitHub URL
            url_info = self._parse_github_url()
            if not url_info:
                raise ValueError(f"Invalid GitHub URL: {self.url}")

            # Headers for authentication
            headers = {}
            if hasattr(self, 'github_token') and self.github_token:
                headers["Authorization"] = f"token {self.github_token}"

            return GitHubIssuesLoader(
                repo=url_info['repo'],
                owner=url_info['owner'],
                headers=headers
            )
        except ImportError:
            # Fallback to using GitHub API directly
            try:
                import json

                import requests

                url_info = self._parse_github_url()
                if not url_info:
                    raise ValueError(f"Invalid GitHub URL: {self.url}")

                # Set up authentication
                headers = {"Accept": "application/vnd.github.v3+json"}
                if hasattr(self, 'github_token') and self.github_token:
                    headers["Authorization"] = f"token {self.github_token}"

                # Fetch issues
                issues_url = f"https://api.github.com/repos/{url_info['owner']}/{url_info['repo']}/issues"
                response = requests.get(issues_url, headers=headers)
                response.raise_for_status()

                issues = response.json()

                # Create documents
                from langchain_core.documents import Document
                documents = []

                for issue in issues:
                    # Skip pull requests (they have different fields)
                    if "pull_request" in issue:
                        continue

                    # Format issue content
                    content = f"Issue #{issue['number']}: {issue['title']}\n\n"
                    content += f"State: {issue['state']}\n"
                    content += f"Created by: {issue['user']['login']}\n"
                    content += f"Created at: {issue['created_at']}\n"
                    if issue['body']:
                        content += f"\nDescription:\n{issue['body']}\n"

                    documents.append(Document(
                        page_content=content,
                        metadata={
                            "source": issue['html_url'],
                            "issue_number": issue['number'],
                            "state": issue['state'],
                            "creator": issue['user']['login'],
                            "created_at": issue['created_at']
                        }
                    ))

                return documents
            except Exception as e:
                # Return document with error message
                from langchain_core.documents import Document
                return [Document(
                    page_content=f"[Error loading GitHub issues: {str(e)}]",
                    metadata={"source": str(self.url)}
                )]

    def create_file_loader(self):
        """Create a GitHubFileLoader."""
        try:
            from langchain_community.document_loaders import GitHubFileLoader

            # Parse GitHub URL
            url_info = self._parse_github_url()
            if not url_info:
                raise ValueError(f"Invalid GitHub URL: {self.url}")

            # Headers for authentication
            headers = {}
            if hasattr(self, 'github_token') and self.github_token:
                headers["Authorization"] = f"token {self.github_token}"

            return GitHubFileLoader(
                owner=url_info['owner'],
                repo=url_info['repo'],
                path=url_info['path'] or "",
                branch=self.branch,
                headers=headers
            )
        except ImportError:
            # Fallback to using GitHub API directly
            try:
                import base64

                import requests

                url_info = self._parse_github_url()
                if not url_info:
                    raise ValueError(f"Invalid GitHub URL: {self.url}")

                # Set up authentication
                headers = {"Accept": "application/vnd.github.v3+json"}
                if hasattr(self, 'github_token') and self.github_token:
                    headers["Authorization"] = f"token {self.github_token}"

                # Fetch file content
                path = url_info['path'] or ""
                content_url = f"https://api.github.com/repos/{url_info['owner']}/{url_info['repo']}/contents/{path}"
                if self.branch:
                    content_url += f"?ref={self.branch}"

                response = requests.get(content_url, headers=headers)
                response.raise_for_status()

                # Process response
                content_data = response.json()

                # Handle directory listing
                if isinstance(content_data, list):
                    # Return directory listing
                    content = "Directory listing:\n\n"
                    for item in content_data:
                        content += f"- {item['name']} ({item['type']})\n"

                    from langchain_core.documents import Document
                    return [Document(
                        page_content=content,
                        metadata={
                            "source": str(self.url),
                            "type": "directory",
                            "path": path
                        }
                    )]

                # Handle file content
                if "content" in content_data and content_data.get("encoding") == "base64":
                    # Decode content
                    file_content = base64.b64decode(content_data["content"]).decode("utf-8")

                    from langchain_core.documents import Document
                    return [Document(
                        page_content=file_content,
                        metadata={
                            "source": content_data["html_url"],
                            "type": "file",
                            "path": content_data["path"],
                            "sha": content_data["sha"]
                        }
                    )]

                # Fallback for unexpected response
                from langchain_core.documents import Document
                return [Document(
                    page_content="[Could not parse GitHub response]",
                    metadata={"source": str(self.url)}
                )]
            except Exception as e:
                # Return document with error message
                from langchain_core.documents import Document
                return [Document(
                    page_content=f"[Error loading GitHub file: {str(e)}]",
                    metadata={"source": str(self.url)}
                )]

    def create_repo_loader(self):
        """Create a custom GitHub repository loader."""
        try:
            # Parse GitHub URL
            url_info = self._parse_github_url()
            if not url_info:
                raise ValueError(f"Invalid GitHub URL: {self.url}")

            # Headers for authentication
            headers = {"Accept": "application/vnd.github.v3+json"}
            if hasattr(self, 'github_token') and self.github_token:
                headers["Authorization"] = f"token {self.github_token}"

            # Use GitHubFileLoader for the root directory
            try:
                from langchain_community.document_loaders import GitHubFileLoader
                return GitHubFileLoader(
                    owner=url_info['owner'],
                    repo=url_info['repo'],
                    path="",  # Root directory
                    branch=self.branch,
                    headers=headers
                )
            except ImportError:
                # Implement repository overview manually
                import requests

                # Fetch repository information
                repo_url = f"https://api.github.com/repos/{url_info['owner']}/{url_info['repo']}"
                response = requests.get(repo_url, headers=headers)
                response.raise_for_status()

                repo_data = response.json()

                # Create repository overview
                content = f"# {repo_data['full_name']}\n\n"
                content += f"{repo_data.get('description', 'No description')}\n\n"
                content += f"Stars: {repo_data['stargazers_count']} | "
                content += f"Forks: {repo_data['forks_count']} | "
                content += f"Watchers: {repo_data['watchers_count']} | "
                content += f"Open Issues: {repo_data['open_issues_count']}\n\n"
                content += f"Default Branch: {repo_data['default_branch']}\n"
                content += f"Created: {repo_data['created_at']}\n"
                content += f"Last Updated: {repo_data['updated_at']}\n\n"

                # Get main README if available
                try:
                    readme_url = f"https://api.github.com/repos/{url_info['owner']}/{url_info['repo']}/readme"
                    readme_response = requests.get(readme_url, headers=headers)
                    if readme_response.status_code == 200:
                        import base64
                        readme_data = readme_response.json()
                        if "content" in readme_data and readme_data.get("encoding") == "base64":
                            readme_content = base64.b64decode(readme_data["content"]).decode("utf-8")
                            content += "## README\n\n"
                            content += readme_content
                except Exception:
                    pass

                # Create document
                from langchain_core.documents import Document
                return [Document(
                    page_content=content,
                    metadata={
                        "source": repo_data["html_url"],
                        "type": "repository",
                        "owner": url_info['owner'],
                        "repo": url_info['repo'],
                        "stars": repo_data['stargazers_count'],
                        "forks": repo_data['forks_count']
                    }
                )]
        except Exception as e:
            # Return document with error message
            from langchain_core.documents import Document
            return [Document(
                page_content=f"[Error loading GitHub repository: {str(e)}]",
                metadata={"source": str(self.url)}
            )]

    def create_pulls_loader(self):
        """Create a custom GitHub PR loader."""
        try:
            # Parse GitHub URL
            url_info = self._parse_github_url()
            if not url_info:
                raise ValueError(f"Invalid GitHub URL: {self.url}")

            # Headers for authentication
            headers = {"Accept": "application/vnd.github.v3+json"}
            if hasattr(self, 'github_token') and self.github_token:
                headers["Authorization"] = f"token {self.github_token}"

            import requests

            # Fetch pull requests
            pulls_url = f"https://api.github.com/repos/{url_info['owner']}/{url_info['repo']}/pulls"
            response = requests.get(pulls_url, headers=headers)
            response.raise_for_status()

            pulls = response.json()

            # Create documents
            from langchain_core.documents import Document
            documents = []

            for pull in pulls:
                # Format PR content
                content = f"Pull Request #{pull['number']}: {pull['title']}\n\n"
                content += f"State: {pull['state']}\n"
                content += f"Created by: {pull['user']['login']}\n"
                content += f"Created at: {pull['created_at']}\n"
                if pull.get('merged_at'):
                    content += f"Merged at: {pull['merged_at']}\n"
                content += f"Base branch: {pull['base']['ref']} → Head branch: {pull['head']['ref']}\n"
                if pull['body']:
                    content += f"\nDescription:\n{pull['body']}\n"

                # Fetch PR diff if not too large
                try:
                    diff_response = requests.get(
                        pull['url'],
                        headers={**headers, "Accept": "application/vnd.github.v3.diff"}
                    )
                    if diff_response.status_code == 200 and len(diff_response.text) < 50000:
                        content += f"\nDiff:\n```diff\n{diff_response.text[:50000]}```\n"
                        if len(diff_response.text) >= 50000:
                            content += "\n[Diff truncated due to size]\n"
                except Exception:
                    pass

                documents.append(Document(
                    page_content=content,
                    metadata={
                        "source": pull['html_url'],
                        "pr_number": pull['number'],
                        "state": pull['state'],
                        "creator": pull['user']['login'],
                        "created_at": pull['created_at'],
                        "base_branch": pull['base']['ref'],
                        "head_branch": pull['head']['ref']
                    }
                ))

            return documents
        except Exception as e:
            # Return document with error message
            from langchain_core.documents import Document
            return [Document(
                page_content=f"[Error loading GitHub pull requests: {str(e)}]",
                metadata={"source": str(self.url)}
            )]

    def create_commits_loader(self):
        """Create a custom GitHub commit loader."""
        try:
            # Parse GitHub URL
            url_info = self._parse_github_url()
            if not url_info:
                raise ValueError(f"Invalid GitHub URL: {self.url}")

            # Headers for authentication
            headers = {"Accept": "application/vnd.github.v3+json"}
            if hasattr(self, 'github_token') and self.github_token:
                headers["Authorization"] = f"token {self.github_token}"

            import requests

            # Fetch commits
            commits_url = f"https://api.github.com/repos/{url_info['owner']}/{url_info['repo']}/commits"
            if self.branch:
                commits_url += f"?sha={self.branch}"

            response = requests.get(commits_url, headers=headers)
            response.raise_for_status()

            commits = response.json()

            # Create documents
            from langchain_core.documents import Document
            documents = []

            for commit in commits:
                # Get commit details
                sha = commit['sha']

                # Get full commit info
                commit_url = f"https://api.github.com/repos/{url_info['owner']}/{url_info['repo']}/commits/{sha}"
                commit_response = requests.get(commit_url, headers=headers)
                if commit_response.status_code == 200:
                    commit_data = commit_response.json()

                    # Format commit content
                    commit_info = commit_data['commit']
                    content = f"Commit: {sha[:7]}\n\n"
                    content += f"Author: {commit_info['author']['name']} <{commit_info['author']['email']}>\n"
                    content += f"Date: {commit_info['author']['date']}\n\n"
                    content += f"Message: {commit_info['message']}\n\n"

                    # Include diff stats
                    if 'stats' in commit_data:
                        stats = commit_data['stats']
                        content += f"Changes: +{stats['additions']} -{stats['deletions']} ({stats['total']} total)\n\n"

                    # Include file changes
                    if 'files' in commit_data:
                        content += "Files changed:\n"
                        for file in commit_data['files'][:10]:  # Limit to 10 files
                            status = file['status']
                            filename = file['filename']
                            changes = f"+{file['additions']} -{file['deletions']}"
                            content += f"- [{status}] {filename} ({changes})\n"

                        if len(commit_data['files']) > 10:
                            content += f"... and {len(commit_data['files']) - 10} more files\n"

                    documents.append(Document(
                        page_content=content,
                        metadata={
                            "source": commit_data['html_url'],
                            "sha": sha,
                            "author": commit_info['author']['name'],
                            "email": commit_info['author']['email'],
                            "date": commit_info['author']['date']
                        }
                    ))

            return documents
        except Exception as e:
            # Return document with error message
            from langchain_core.documents import Document
            return [Document(
                page_content=f"[Error loading GitHub commits: {str(e)}]",
                metadata={"source": str(self.url)}
            )]


@auto_source(domain_patterns=["huggingface.co"])
class HuggingFaceSource(RemoteSource):
    """HuggingFace source for models, datasets, and spaces."""
    url: HttpUrl

    class Config:
        loader_strategies = {
            'dataset': {
                'class': 'HuggingFaceDatasetLoader',
                'speed': 'medium',
                'quality': 'high',
                'best_for': ['datasets', 'data_files']
            },
            'model': {
                'class': 'HuggingFaceModelLoader',
                'speed': 'medium',
                'quality': 'high',
                'best_for': ['models', 'code']
            },
            'space': {
                'class': 'HuggingFaceSpaceLoader',
                'speed': 'medium',
                'quality': 'high',
                'best_for': ['demos', 'applications']
            }
        }
        optional_credentials = ['hf_token']

    def authenticate(self, credential_manager: Optional[CredentialManager] = None) -> bool:
        """Authenticate for HuggingFace API access."""
        if not credential_manager:
            self.is_authenticated = False
            return False

        hf_token = credential_manager.get_credential('hf_token')
        if not hf_token:
            self.is_authenticated = False
            return False

        self.hf_token = hf_token.get('value')
        self.is_authenticated = bool(self.hf_token)

        return self.is_authenticated

    def _parse_huggingface_url(self):
        """Parse HuggingFace URL to extract repository type and name."""
        parsed_url = urlparse(str(self.url))
        path_segments = parsed_url.path.strip('/').split('/')

        if len(path_segments) >= 2:
            repo_type = path_segments[0]  # 'datasets', 'models', or 'spaces'
            author = path_segments[1]
            name = path_segments[2] if len(path_segments) > 2 else None

            # If URL format is /author/name, then assume it's a model
            if repo_type not in ['datasets', 'spaces'] and name is None:
                name = author
                author = repo_type
                repo_type = 'models'

            return {
                'type': repo_type,
                'author': author,
                'name': name,
                'full_name': f"{author}/{name}" if name else author
            }
        return None

    def create_dataset_loader(self):
        """Create a HuggingFaceDatasetLoader."""
        try:
            from langchain_community.document_loaders import HuggingFaceDatasetLoader

            # Parse HuggingFace URL
            url_info = self._parse_huggingface_url()
            if not url_info:
                raise ValueError(f"Invalid HuggingFace URL: {self.url}")

            # Determine dataset name
            dataset_name = url_info['full_name']

            # Set up authentication if available
            if hasattr(self, 'hf_token') and self.hf_token:
                import os
                os.environ['HUGGINGFACE_TOKEN'] = self.hf_token

            return HuggingFaceDatasetLoader(
                repo_id=dataset_name,
                split="train"  # Default to train split
            )
        except ImportError:
            # Fallback to using HuggingFace API directly
            try:
                import requests

                url_info = self._parse_huggingface_url()
                if not url_info:
                    raise ValueError(f"Invalid HuggingFace URL: {self.url}")

                # Set up authentication
                headers = {}
                if hasattr(self, 'hf_token') and self.hf_token:
                    headers["Authorization"] = f"Bearer {self.hf_token}"

                # Fetch dataset information
                dataset_id = url_info['full_name']
                api_url = f"https://huggingface.co/api/datasets/{dataset_id}"

                response = requests.get(api_url, headers=headers)
                response.raise_for_status()

                dataset_info = response.json()

                # Create document with dataset info
                content = f"# {dataset_info['id']}\n\n"
                if 'card_data' in dataset_info and dataset_info['card_data']:
                    if 'description' in dataset_info['card_data']:
                        content += f"{dataset_info['card_data']['description']}\n\n"

                content += f"Author: {dataset_info.get('author', 'Unknown')}\n"
                content += f"Last Modified: {dataset_info.get('lastModified', 'Unknown')}\n"

                # Include tags if available
                if 'tags' in dataset_info and dataset_info['tags']:
                    content += f"Tags: {', '.join(dataset_info['tags'])}\n\n"

                # Include dataset structure if available
                try:
                    structure_url = f"https://huggingface.co/api/datasets/{dataset_id}/info"
                    structure_response = requests.get(structure_url, headers=headers)
                    if structure_response.status_code == 200:
                        structure_data = structure_response.json()
                        if 'splits' in structure_data:
                            content += "## Dataset Structure\n\n"
                            for split_name, split_info in structure_data['splits'].items():
                                content += f"- {split_name}: {split_info.get('num_examples', 'Unknown')} examples\n"
                except Exception:
                    pass

                # Create document
                from langchain_core.documents import Document
                return [Document(
                    page_content=content,
                    metadata={
                        "source": f"https://huggingface.co/datasets/{dataset_id}",
                        "type": "dataset",
                        "dataset_id": dataset_id,
                        "author": dataset_info.get('author', 'Unknown')
                    }
                )]
            except Exception as e:
                # Return document with error message
                from langchain_core.documents import Document
                return [Document(
                    page_content=f"[Error loading HuggingFace dataset: {str(e)}]",
                    metadata={"source": str(self.url)}
                )]

    def create_model_loader(self):
        """Create a custom HuggingFace model loader."""
        try:
            # Parse HuggingFace URL
            url_info = self._parse_huggingface_url()
            if not url_info:
                raise ValueError(f"Invalid HuggingFace URL: {self.url}")

            # Set up authentication
            headers = {}
            if hasattr(self, 'hf_token') and self.hf_token:
                headers["Authorization"] = f"Bearer {self.hf_token}"

            import requests

            # Fetch model information
            model_id = url_info['full_name']
            api_url = f"https://huggingface.co/api/models/{model_id}"

            response = requests.get(api_url, headers=headers)
            response.raise_for_status()

            model_info = response.json()

            # Create document with model info
            content = f"# {model_info['id']}\n\n"
            if 'card_data' in model_info and model_info['card_data']:
                if 'description' in model_info['card_data']:
                    content += f"{model_info['card_data']['description']}\n\n"

            # Include model details
            content += f"Author: {model_info.get('author', 'Unknown')}\n"
            content += f"Last Modified: {model_info.get('lastModified', 'Unknown')}\n"
            if 'downloads' in model_info:
                content += f"Downloads: {model_info['downloads']:,}\n"
            if 'likes' in model_info:
                content += f"Likes: {model_info['likes']:,}\n"

            # Include pipeline tags if available
            if 'pipeline_tag' in model_info:
                content += f"Pipeline: {model_info['pipeline_tag']}\n"

            # Include tags if available
            if 'tags' in model_info and model_info['tags']:
                content += f"Tags: {', '.join(model_info['tags'])}\n\n"

            # Try to get model architecture and size
            if 'config' in model_info:
                content += "## Model Configuration\n\n"
                config = model_info['config']

                if 'architectures' in config:
                    content += f"Architecture: {', '.join(config['architectures'])}\n"

                if 'model_type' in config:
                    content += f"Model Type: {config['model_type']}\n"

                # Extract parameters information if available
                params = []
                if 'n_params' in config:
                    params.append(f"{config['n_params']:,} parameters")
                elif 'num_parameters' in config:
                    params.append(f"{config['num_parameters']:,} parameters")

                if params:
                    content += f"Size: {', '.join(params)}\n"

            # Create document
            from langchain_core.documents import Document
            return [Document(
                page_content=content,
                metadata={
                    "source": f"https://huggingface.co/{model_id}",
                    "type": "model",
                    "model_id": model_id,
                    "author": model_info.get('author', 'Unknown'),
                    "pipeline": model_info.get('pipeline_tag', None)
                }
            )]
        except Exception as e:
            # Return document with error message
            from langchain_core.documents import Document
            return [Document(
                page_content=f"[Error loading HuggingFace model: {str(e)}]",
                metadata={"source": str(self.url)}
            )]

    def create_space_loader(self):
        """Create a custom HuggingFace space loader."""
        try:
            # Parse HuggingFace URL
            url_info = self._parse_huggingface_url()
            if not url_info:
                raise ValueError(f"Invalid HuggingFace URL: {self.url}")

            # Set up authentication
            headers = {}
            if hasattr(self, 'hf_token') and self.hf_token:
                headers["Authorization"] = f"Bearer {self.hf_token}"

            import requests

            # Fetch space information
            space_id = url_info['full_name']
            api_url = f"https://huggingface.co/api/spaces/{space_id}"

            response = requests.get(api_url, headers=headers)
            response.raise_for_status()

            space_info = response.json()

            # Create document with space info
            content = f"# {space_info['id']}\n\n"
            if 'card_data' in space_info and space_info['card_data']:
                if 'description' in space_info['card_data']:
                    content += f"{space_info['card_data']['description']}\n\n"

            # Include space details
            content += f"Author: {space_info.get('author', 'Unknown')}\n"
            content += f"Last Modified: {space_info.get('lastModified', 'Unknown')}\n"
            if 'likes' in space_info:
                content += f"Likes: {space_info['likes']:,}\n"

            # Include space SDK
            if 'sdk' in space_info:
                content += f"SDK: {space_info['sdk']}\n"

            # Include runtime if available
            if 'runtime' in space_info:
                content += f"Runtime: {space_info['runtime']['name']}"
                if 'version' in space_info['runtime']:
                    content += f" v{space_info['runtime']['version']}"
                content += "\n"

            # Include tags if available
            if 'tags' in space_info and space_info['tags']:
                content += f"Tags: {', '.join(space_info['tags'])}\n\n"

            # Try to get model or dataset dependencies
            if 'models' in space_info and space_info['models']:
                content += "## Model Dependencies\n\n"
                for model in space_info['models']:
                    content += f"- {model}\n"
                content += "\n"

            if 'datasets' in space_info and space_info['datasets']:
                content += "## Dataset Dependencies\n\n"
                for dataset in space_info['datasets']:
                    content += f"- {dataset}\n"
                content += "\n"

            # Create document
            from langchain_core.documents import Document
            return [Document(
                page_content=content,
                metadata={
                    "source": f"https://huggingface.co/spaces/{space_id}",
                    "type": "space",
                    "space_id": space_id,
                    "author": space_info.get('author', 'Unknown'),
                    "sdk": space_info.get('sdk', None)
                }
            )]
        except Exception as e:
            # Return document with error message
            from langchain_core.documents import Document
            return [Document(
                page_content=f"[Error loading HuggingFace space: {str(e)}]",
                metadata={"source": str(self.url)}
            )]"""
Additional Web-based Document Loaders for Haive Framework

This module implements specialized web source loaders including ArxivLoader,
PubMedLoader, RSSFeedLoader, and NewsURLLoader.
"""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

from pydantic import Field, HttpUrl

from ..source_implementation import (
    BaseSource,
    CredentialManager,
    RemoteSource,
    auto_source,
)


@auto_source(domain_patterns=["arxiv.org"])
class ArxivSource(RemoteSource):
    """ArXiv paper source."""
    url: HttpUrl
    load_all_available_pdfs: bool = False
    max_results: int = 5

    class Config:
        loader_strategies = {
            'arxiv': {
                'class': 'ArxivLoader',
                'speed': 'medium',
                'quality': 'high',
                'best_for': ['scientific_papers', 'research']
            }
        }

    def create_arxiv_loader(self):
        """Create an ArxivLoader."""
        try:
            from langchain_community.document_loaders import ArxivLoader

            # Extract paper ID from URL
            arxiv_id = None

            # Try different URL patterns
            import re
            patterns = [
                r'arxiv\.org/abs/([^/]+)',  # https://arxiv.org/abs/1234.5678
                r'arxiv\.org/pdf/([^/]+)',  # https://arxiv.org/pdf/1234.5678.pdf
                r'arxiv\.org/ps/([^/]+)'    # https://arxiv.org/ps/1234.5678
            ]

            for pattern in patterns:
                match = re.search(pattern, str(self.url))
                if match:
                    arxiv_id = match.group(1)
                    break

            # If ID not found in URL, treat as search query
            if not arxiv_id:
                # Use the last part of the URL as a search query
                query = str(self.url).split('/')[-1]
                return ArxivLoader(
                    query=query,
                    load_all_available_pdfs=self.load_all_available_pdfs,
                    max_results=self.max_results
                )
            else:
                return ArxivLoader(
                    query=f"id:{arxiv_id}",
                    load_all_available_pdfs=self.load_all_available_pdfs,
                    max_results=1
                )
        except ImportError:
            # Fallback to using arxiv API directly if available
            try:
                import re

                import arxiv

                # Extract paper ID from URL
                arxiv_id = None

                patterns = [
                    r'arxiv\.org/abs/([^/]+)',  # https://arxiv.org/abs/1234.5678
                    r'arxiv\.org/pdf/([^/]+)',  # https://arxiv.org/pdf/1234.5678.pdf
                    r'arxiv\.org/ps/([^/]+)'    # https://arxiv.org/ps/1234.5678
                ]

                for pattern in patterns:
                    match = re.search(pattern, str(self.url))
                    if match:
                        arxiv_id = match.group(1)
                        # Remove version suffix if present
                        arxiv_id = arxiv_id.split('v')[0]
                        break

                # Search for the paper
                if arxiv_id:
                    search = arxiv.Search(id_list=[arxiv_id])
                else:
                    # Use the last part of the URL as a search query
                    query = str(self.url).split('/')[-1]
                    search = arxiv.Search(query=query, max_results=self.max_results)

                results = list(search.results())

                from langchain_core.documents import Document
                documents = []

                for result in results:
                    # Format paper information
                    content = f"# {result.title}\n\n"
                    content += f"Authors: {', '.join(author.name for author in result.authors)}\n"
                    content += f"Published: {result.published}\n"
                    if result.updated:
                        content += f"Updated: {result.updated}\n"
                    content += f"Categories: {', '.join(result.categories)}\n\n"
                    content += f"DOI: {result.doi}\n" if result.doi else ""
                    content += f"Journal Ref: {result.journal_ref}\n" if result.journal_ref else ""
                    content += "\n"
                    content += f"## Abstract\n\n{result.summary}\n"

                    documents.append(Document(
                        page_content=content,
                        metadata={
                            "source": result.entry_id,
                            "title": result.title,
                            "authors": [author.name for author in result.authors],
                            "published": str(result.published),
                            "categories": result.categories,
                            "id": result.entry_id.split('/')[-1]
                        }
                    ))

                    # Load PDF content if requested
                    if self.load_all_available_pdfs:
                        try:
                            from io import BytesIO

                            import requests

                            # Download PDF
                            pdf_url = result.pdf_url
                            response = requests.get(pdf_url)
                            response.raise_for_status()

                            # Extract text from PDF
                            try:
                                from pypdf import PdfReader
                                pdf = PdfReader(BytesIO(response.content))
                                pdf_text = ""
                                for page in pdf.pages:
                                    pdf_text += page.extract_text() + "\n\n"

                                documents.append(Document(
                                    page_content=pdf_text,
                                    metadata={
                                        "source": pdf_url,
                                        "title": result.title,
                                        "type": "pdf",
                                        "id": result.entry_id.split('/')[-1]
                                    }
                                ))
                            except ImportError:
                                pass
                        except Exception:
                            # Skip PDF if any error occurs
                            pass

                return documents
            except ImportError:
                # Return document with error message
                from langchain_core.documents import Document
                return [Document(
                    page_content="[ArXiv loader dependencies not installed. Please install 'arxiv' and 'pypdf' packages.]",
                    metadata={"source": str(self.url)}
                )]
            except Exception as e:
                # Return document with error message
                from langchain_core.documents import Document
                return [Document(
                    page_content=f"[Error loading ArXiv paper: {str(e)}]",
                    metadata={"source": str(self.url)}
                )]


@auto_source(domain_patterns=["pubmed.ncbi.nlm.nih.gov"])
class PubMedSource(RemoteSource):
    """PubMed medical paper source."""
    url: HttpUrl
    max_results: int = 5

    class Config:
        loader_strategies = {
            'pubmed': {
                'class': 'PubMedLoader',
                'speed': 'medium',
                'quality': 'high',
                'best_for': ['medical_papers', 'biomedical_research']
            }
        }

    def create_pubmed_loader(self):
        """Create a PubMedLoader."""
        try:
            from langchain_community.document_loaders import PubMedLoader

            # Extract PMID from URL
            pmid = None

            # Try different URL patterns
            import re
            match = re.search(r'pubmed/(\d+)', str(self.url))
            if match:
                pmid = match.group(1)

            # If PMID not found in URL, treat as search query
            if not pmid:
                # Use the last part of the URL as a search query
                query = str(self.url).split('/')[-1]
                return PubMedLoader(
                    query=query,
                    max_results=self.max_results
                )
            else:
                return PubMedLoader(
                    query=f"{pmid}[pmid]",
                    max_results=1
                )
        except ImportError:
            # Fallback to using PubMed API directly if available
            try:
                import re
                import xml.etree.ElementTree as ET

                import requests

                # Extract PMID from URL
                pmid = None
                match = re.search(r'pubmed/(\d+)', str(self.url))
                if match:
                    pmid = match.group(1)

                # Set up query
                if pmid:
                    search_query = f"{pmid}[pmid]"
                else:
                    # Use the last part of the URL as a search query
                    search_query = str(self.url).split('/')[-1]

                # Use PubMed E-utilities API
                base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
                esearch_url = f"{base_url}/esearch.fcgi?db=pubmed&term={search_query}&retmax={self.max_results}"

                # Search for articles
                response = requests.get(esearch_url)
                response.raise_for_status()

                # Parse XML
                root = ET.fromstring(response.content)
                id_list = root.findall(".//Id")
                pmids = [id_elem.text for id_elem in id_list]

                # If no results found, return message
                if not pmids:
                    from langchain_core.documents import Document
                    return [Document(
                        page_content=f"[No PubMed articles found for query: {search_query}]",
                        metadata={"source": str(self.url)}
                    )]

                # Fetch article details
                from langchain_core.documents import Document
                documents = []

                # Batch fetch for efficiency
                ids_param = ",".join(pmids)
                efetch_url = f"{base_url}/efetch.fcgi?db=pubmed&id={ids_param}&retmode=xml"
                fetch_response = requests.get(efetch_url)
                fetch_response.raise_for_status()

                # Parse article details
                articles_root = ET.fromstring(fetch_response.content)
                articles = articles_root.findall(".//PubmedArticle")

                for article in articles:
                    try:
                        # Extract title
                        title_elem = article.find(".//ArticleTitle")
                        title = title_elem.text if title_elem is not None else "Untitled"

                        # Extract abstract
                        abstract_parts = article.findall(".//AbstractText")
                        abstract = " ".join([part.text for part in abstract_parts if part.text])

                        # Extract authors
                        author_list = article.findall(".//Author")
                        authors = []
                        for author in author_list:
                            last_name = author.find("LastName")
                            fore_name = author.find("ForeName")
                            if last_name is not None and fore_name is not None:
                                authors.append(f"{last_name.text} {fore_name.text}")
                            elif last_name is not None:
                                authors.append(last_name.text)

                        # Extract journal info
                        journal_elem = article.find(".//Journal/Title")
                        journal = journal_elem.text if journal_elem is not None else "Unknown Journal"

                        # Extract publication date
                        year_elem = article.find(".//PubDate/Year")
                        month_elem = article.find(".//PubDate/Month")
                        day_elem = article.find(".//PubDate/Day")

                        pub_date = ""
                        if year_elem is not None:
                            pub_date = year_elem.text
                            if month_elem is not None:
                                pub_date = f"{month_elem.text} {pub_date}"
                                if day_elem is not None:
                                    pub_date = f"{day_elem.text} {pub_date}"

                        # Extract PMID
                        pmid_elem = article.find(".//PMID")
                        pmid = pmid_elem.text if pmid_elem is not None else "Unknown"

                        # Format article content
                        content = f"# {title}\n\n"
                        content += f"Authors: {', '.join(authors)}\n" if authors else ""
                        content += f"Journal: {journal}\n"
                        content += f"Published: {pub_date}\n" if pub_date else ""
                        content += f"PMID: {pmid}\n\n"
                        content += f"## Abstract\n\n{abstract}\n" if abstract else ""

                        documents.append(Document(
                            page_content=content,
                            metadata={
                                "source": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                                "title": title,
                                "authors": authors,
                                "journal": journal,
                                "publication_date": pub_date,
                                "pmid": pmid
                            }
                        ))
                    except Exception as e:
                        # Skip articles with parsing errors
                        continue

                return documents
            except Exception as e:
                # Return document with error message
                from langchain_core.documents import Document
                return [Document(
                    page_content=f"[Error loading PubMed article: {str(e)}]",
                    metadata={"source": str(self.url)}
                )]


@auto_source
class RSSFeedSource(RemoteSource):
    """RSS feed source."""
    url: HttpUrl
    max_items: int = 10

    class Config:
        loader_strategies = {
            'rss': {
                'class': 'RSSFeedLoader',
                'speed': 'fast',
                'quality': 'medium',
                'best_for': ['news', 'blogs', 'feeds']
            }
        }

    def create_rss_loader(self):
        """Create an RSSFeedLoader."""
        try:
            from langchain_community.document_loaders import RSSFeedLoader
            return RSSFeedLoader(
                urls=[str(self.url)],
                limit=self.max_items
            )
        except ImportError:
            # Fallback to using feedparser directly
            try:
                import feedparser

                # Parse feed
                feed = feedparser.parse(str(self.url))

                # Create documents from entries
                from langchain_core.documents import Document
                documents = []

                for entry in feed.entries[:self.max_items]:
                    # Extract content
                    title = entry.get('title', 'Untitled')

                    # Try different content fields
                    content = ""
                    if 'content' in entry and entry.content:
                        content = entry.content[0].value
                    elif 'summary' in entry:
                        content = entry.summary
                    elif 'description' in entry:
                        content = entry.description

                    # Remove HTML tags if present
                    try:
                        from bs4 import BeautifulSoup
                        content = BeautifulSoup(content, "html.parser").get_text()
                    except ImportError:
                        # Simple HTML tag removal
                        import re
                        content = re.sub(r'<[^>]+>', ' ', content)

                    # Format entry
                    formatted_content = f"# {title}\n\n"

                    # Add author if available
                    if 'author' in entry:
                        formatted_content += f"Author: {entry.author}\n"

                    # Add publication date if available
                    if 'published' in entry:
                        formatted_content += f"Published: {entry.published}\n"

                    formatted_content += f"Link: {entry.link}\n\n"
                    formatted_content += content

                    # Create metadata
                    metadata = {
                        "source": entry.link,
                        "title": title,
                        "feed_url": str(self.url)
                    }

                    # Add additional metadata if available
                    if 'author' in entry:
                        metadata["author"] = entry.author
                    if 'published' in entry:
                        metadata["published"] = entry.published
                    if 'tags' in entry:
                        metadata["tags"] = [tag.term for tag in entry.tags] if hasattr(entry.tags, '__iter__') else [entry.tags.term]

                    documents.append(Document(
                        page_content=formatted_content,
                        metadata=metadata
                    ))

                return documents
            except Exception as e:
                # Return document with error message
                from langchain_core.documents import Document
                return [Document(
                    page_content=f"[Error loading RSS feed: {str(e)}]",
                    metadata={"source": str(self.url)}
                )]


@auto_source(domain_patterns=["news.google.com", "reuters.com", "nytimes.com", "washingtonpost.com", "theguardian.com", "bbc.com", "cnn.com"])
class NewsURLSource(RemoteSource):
    """News article source."""
    url: HttpUrl
    use_nlp: bool = True

    class Config:
        loader_strategies = {
            'news': {
                'class': 'NewsURLLoader',
                'speed': 'medium',
                'quality': 'high',
                'best_for': ['news', 'articles']
            }
        }

    def create_news_loader(self):
        """Create a NewsURLLoader."""
        try:
            from langchain_community.document_loaders import NewsURLLoader
            return NewsURLLoader(
                urls=[str(self.url)],
                nlp=self.use_nlp
            )
        except ImportError:
            # Fallback to using newspaper3k directly
            try:
                import newspaper
                from newspaper import Article

                # Download and parse article
                article = Article(str(self.url))
                article.download()
                article.parse()

                # Perform NLP analysis if requested
                if self.use_nlp:
                    try:
                        article.nlp()
                    except Exception:
                        # Skip NLP if it fails
                        pass

                # Create formatted content
                content = f"# {article.title}\n\n"

                # Add authors if available
                if article.authors:
                    content += f"Authors: {', '.join(article.authors)}\n"

                # Add publication date if available
                if article.publish_date:
                    content += f"Published: {article.publish_date}\n"

                content += "\n"

                # Add summary if available (requires NLP)
                if hasattr(article, 'summary') and article.summary:
                    content += f"## Summary\n\n{article.summary}\n\n"

                # Add keywords if available (requires NLP)
                if hasattr(article, 'keywords') and article.keywords:
                    content += f"Keywords: {', '.join(article.keywords)}\n\n"

                # Add main article text
                content += f"## Article\n\n{article.text}\n"

                # Create metadata
                metadata = {
                    "source": str(self.url),
                    "title": article.title
                }

                # Add additional metadata if available
                if article.authors:
                    metadata["authors"] = article.authors
                if article.publish_date:
                    metadata["published"] = str(article.publish_date)
                if hasattr(article, 'keywords') and article.keywords:
                    metadata["keywords"] = article.keywords

                from langchain_core.documents import Document
                return [Document(
                    page_content=content,
                    metadata=metadata
                )]
            except Exception as e:
                # Return document with error message
                from langchain_core.documents import Document
                return [Document(
                    page_content=f"[Error loading news article: {str(e)}]",
                    metadata={"source": str(self.url)}
                )]


# Convenience function to create a web loader for a URL
def create_web_loader(url: str, **kwargs) -> Any:
    """
    Create the appropriate web loader for a given URL.

    Args:
        url: The URL to load
        **kwargs: Additional arguments for specific loaders

    Returns:
        A document loader instance
    """
    # Create HttpUrl from string
    from pydantic import HttpUrl
    http_url = HttpUrl(url)

    # Extract domain
    domain = urlparse(url).netloc

    # Create appropriate source based on domain
    if "github.com" in domain:
        source = GitHubSource(url=http_url, **kwargs)
    elif "huggingface.co" in domain:
        source = HuggingFaceSource(url=http_url, **kwargs)
    elif "arxiv.org" in domain:
        source = ArxivSource(url=http_url, **kwargs)
    elif "pubmed.ncbi.nlm.nih.gov" in domain:
        source = PubMedSource(url=http_url, **kwargs)
    elif any(news_domain in domain for news_domain in ["news.google.com", "reuters.com", "nytimes.com", "washingtonpost.com", "theguardian.com", "bbc.com", "cnn.com"]):
        source = NewsURLSource(url=http_url, **kwargs)
    elif "wikipedia.org" in domain:
        from ..source_implementation import registry
        source_class = registry.source_classes.get("wikipedia")
        if source_class:
            source = source_class(url=http_url, **kwargs)
        else:
            source = WebPageSource(url=http_url, **kwargs)
    elif "youtube.com" in domain or "youtu.be" in domain:
        from ..source_implementation import registry
        source_class = registry.source_classes.get("youtube")
        if source_class:
            source = source_class(url=http_url, **kwargs)
        else:
            source = WebPageSource(url=http_url, **kwargs)
    else:
        # Check if it's an RSS feed
        try:
            import feedparser
            feed = feedparser.parse(url)
            if feed.entries and not feed.bozo:
                source = RSSFeedSource(url=http_url, **kwargs)
            else:
                source = WebPageSource(url=http_url, **kwargs)
        except (ImportError, Exception):
            source = WebPageSource(url=http_url, **kwargs)

    # Get strategy if specified
    strategy = kwargs.get('strategy', None)

    # Create loader with specified or auto-selected strategy
    return source.create_loader(strategy)
