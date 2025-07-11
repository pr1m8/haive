"""Enhanced GitHub Loaders with Additional Features.

This module contains enhanced GitHub loaders for discussions, gists, releases,
actions, and wiki pages.
"""

import logging
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from langchain_core.document_loaders.base import BaseLoader
from langchain_core.documents import Document

from haive.core.engine.document.loaders.sources.implementation import (
    CredentialType,
    WebUrlSource,
)

logger = logging.getLogger(__name__)


class GitHubDiscussionsSource(WebUrlSource):
    """GitHub Discussions loader."""

    def __init__(
        self,
        repo_url: str,
        discussion_number: Optional[int] = None,
        category: Optional[str] = None,
        answered_only: bool = False,
        max_discussions: int = 100,
        include_comments: bool = True,
        **kwargs,
    ):
        super().__init__(source_path=repo_url, **kwargs)
        self.repo_url = repo_url
        self.discussion_number = discussion_number
        self.category = category
        self.answered_only = answered_only
        self.max_discussions = max_discussions
        self.include_comments = include_comments

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a GitHub Discussions loader using GraphQL API."""
        try:
            # Since LangChain doesn't have a native discussions loader,
            # we'll create a custom implementation
            return GitHubDiscussionsLoader(
                repo_url=self.repo_url,
                discussion_number=self.discussion_number,
                category=self.category,
                answered_only=self.answered_only,
                max_discussions=self.max_discussions,
                include_comments=self.include_comments,
                access_token=self._get_github_token(),
            )

        except Exception as e:
            logger.error(f"Failed to create GitHub Discussions loader: {e}")
            return None

    def _get_github_token(self) -> Optional[str]:
        """Get GitHub token from credential manager."""
        if self.credential_manager:
            cred = self.credential_manager.get_credential("github")
            if cred and cred.credential_type in [
                CredentialType.ACCESS_TOKEN,
                CredentialType.API_KEY,
            ]:
                return cred.value
        return None


class GitHubGistsSource(WebUrlSource):
    """GitHub Gists loader."""

    def __init__(
        self,
        username: Optional[str] = None,
        gist_id: Optional[str] = None,
        public_only: bool = True,
        max_gists: int = 100,
        **kwargs,
    ):
        source_path = f"https://gist.github.com/{username or gist_id}"
        super().__init__(source_path=source_path, **kwargs)
        self.username = username
        self.gist_id = gist_id
        self.public_only = public_only
        self.max_gists = max_gists

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a GitHub Gists loader."""
        try:
            return GitHubGistsLoader(
                username=self.username,
                gist_id=self.gist_id,
                public_only=self.public_only,
                max_gists=self.max_gists,
                access_token=self._get_github_token(),
            )

        except Exception as e:
            logger.error(f"Failed to create GitHub Gists loader: {e}")
            return None

    def _get_github_token(self) -> Optional[str]:
        """Get GitHub token from credential manager."""
        if self.credential_manager:
            cred = self.credential_manager.get_credential("github")
            if cred and cred.credential_type in [
                CredentialType.ACCESS_TOKEN,
                CredentialType.API_KEY,
            ]:
                return cred.value
        return None


class GitHubReleasesSource(WebUrlSource):
    """GitHub Releases loader."""

    def __init__(
        self,
        repo_url: str,
        include_prereleases: bool = False,
        include_drafts: bool = False,
        max_releases: int = 50,
        include_release_notes: bool = True,
        include_assets: bool = True,
        **kwargs,
    ):
        super().__init__(source_path=repo_url, **kwargs)
        self.repo_url = repo_url
        self.include_prereleases = include_prereleases
        self.include_drafts = include_drafts
        self.max_releases = max_releases
        self.include_release_notes = include_release_notes
        self.include_assets = include_assets

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a GitHub Releases loader."""
        try:
            return GitHubReleasesLoader(
                repo_url=self.repo_url,
                include_prereleases=self.include_prereleases,
                include_drafts=self.include_drafts,
                max_releases=self.max_releases,
                include_release_notes=self.include_release_notes,
                include_assets=self.include_assets,
                access_token=self._get_github_token(),
            )

        except Exception as e:
            logger.error(f"Failed to create GitHub Releases loader: {e}")
            return None

    def _get_github_token(self) -> Optional[str]:
        """Get GitHub token from credential manager."""
        if self.credential_manager:
            cred = self.credential_manager.get_credential("github")
            if cred and cred.credential_type in [
                CredentialType.ACCESS_TOKEN,
                CredentialType.API_KEY,
            ]:
                return cred.value
        return None


class GitHubActionsSource(WebUrlSource):
    """GitHub Actions workflows and runs loader."""

    def __init__(
        self,
        repo_url: str,
        workflow_name: Optional[str] = None,
        status: Optional[str] = None,  # completed, in_progress, queued
        include_logs: bool = False,
        max_runs: int = 50,
        **kwargs,
    ):
        super().__init__(source_path=repo_url, **kwargs)
        self.repo_url = repo_url
        self.workflow_name = workflow_name
        self.status = status
        self.include_logs = include_logs
        self.max_runs = max_runs

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a GitHub Actions loader."""
        try:
            return GitHubActionsLoader(
                repo_url=self.repo_url,
                workflow_name=self.workflow_name,
                status=self.status,
                include_logs=self.include_logs,
                max_runs=self.max_runs,
                access_token=self._get_github_token(),
            )

        except Exception as e:
            logger.error(f"Failed to create GitHub Actions loader: {e}")
            return None

    def _get_github_token(self) -> Optional[str]:
        """Get GitHub token from credential manager."""
        if self.credential_manager:
            cred = self.credential_manager.get_credential("github")
            if cred and cred.credential_type in [
                CredentialType.ACCESS_TOKEN,
                CredentialType.API_KEY,
            ]:
                return cred.value
        return None


class GitHubWikiSource(WebUrlSource):
    """GitHub Wiki pages loader."""

    def __init__(
        self,
        repo_url: str,
        page_name: Optional[str] = None,
        include_history: bool = False,
        **kwargs,
    ):
        super().__init__(source_path=repo_url, **kwargs)
        self.repo_url = repo_url
        self.page_name = page_name
        self.include_history = include_history

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a GitHub Wiki loader."""
        try:
            return GitHubWikiLoader(
                repo_url=self.repo_url,
                page_name=self.page_name,
                include_history=self.include_history,
                access_token=self._get_github_token(),
            )

        except Exception as e:
            logger.error(f"Failed to create GitHub Wiki loader: {e}")
            return None

    def _get_github_token(self) -> Optional[str]:
        """Get GitHub token from credential manager."""
        if self.credential_manager:
            cred = self.credential_manager.get_credential("github")
            if cred and cred.credential_type in [
                CredentialType.ACCESS_TOKEN,
                CredentialType.API_KEY,
            ]:
                return cred.value
        return None


# Custom loader implementations since LangChain doesn't have these built-in


class GitHubDiscussionsLoader(BaseLoader):
    """Custom loader for GitHub Discussions."""

    def __init__(
        self,
        repo_url: str,
        discussion_number: Optional[int] = None,
        category: Optional[str] = None,
        answered_only: bool = False,
        max_discussions: int = 100,
        include_comments: bool = True,
        access_token: Optional[str] = None,
    ):
        self.repo_url = repo_url
        self.discussion_number = discussion_number
        self.category = category
        self.answered_only = answered_only
        self.max_discussions = max_discussions
        self.include_comments = include_comments
        self.access_token = access_token

        # Parse repo info
        parsed = urlparse(repo_url)
        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) >= 2:
            self.owner = path_parts[0]
            self.repo = path_parts[1]
        else:
            raise ValueError(f"Invalid GitHub URL: {repo_url}")

    def load(self) -> List[Document]:
        """Load GitHub discussions."""
        try:
            import requests

            documents = []

            # GitHub GraphQL endpoint
            url = "https://api.github.com/graphql"
            headers = {
                "Authorization": (
                    f"bearer {self.access_token}" if self.access_token else ""
                ),
                "Accept": "application/vnd.github.v3+json",
            }

            # GraphQL query for discussions
            query = """
            query($owner: String!, $repo: String!, $first: Int!) {
                repository(owner: $owner, name: $repo) {
                    discussions(first: $first) {
                        nodes {
                            title
                            body
                            number
                            category { name }
                            isAnswered
                            createdAt
                            author { login }
                            comments(first: 10) {
                                nodes {
                                    body
                                    author { login }
                                    createdAt
                                }
                            }
                        }
                    }
                }
            }
            """

            variables = {
                "owner": self.owner,
                "repo": self.repo,
                "first": self.max_discussions,
            }

            response = requests.post(
                url,
                json={"query": query, "variables": variables},
                headers=headers,
            )

            if response.status_code == 200:
                data = response.json()
                discussions = (
                    data.get("data", {})
                    .get("repository", {})
                    .get("discussions", {})
                    .get("nodes", [])
                )

                for discussion in discussions:
                    if self.answered_only and not discussion.get("isAnswered"):
                        continue
                    if (
                        self.category
                        and discussion.get("category", {}).get("name") != self.category
                    ):
                        continue
                    if (
                        self.discussion_number
                        and discussion.get("number") != self.discussion_number
                    ):
                        continue

                    content = f"# {discussion['title']}\n\n"
                    content += f"**Author:** {discussion['author']['login']}\n"
                    content += f"**Category:** {discussion['category']['name']}\n"
                    content += f"**Created:** {discussion['createdAt']}\n"
                    content += f"**Answered:** {discussion['isAnswered']}\n\n"
                    content += discussion["body"]

                    if self.include_comments and discussion.get("comments", {}).get(
                        "nodes"
                    ):
                        content += "\n\n## Comments\n\n"
                        for comment in discussion["comments"]["nodes"]:
                            content += f"**{comment['author']['login']}** ({comment['createdAt']}):\n"
                            content += f"{comment['body']}\n\n"

                    metadata = {
                        "source": f"{self.repo_url}/discussions/{discussion['number']}",
                        "type": "github_discussion",
                        "number": discussion["number"],
                        "category": discussion["category"]["name"],
                        "is_answered": discussion["isAnswered"],
                        "created_at": discussion["createdAt"],
                        "author": discussion["author"]["login"],
                    }

                    documents.append(Document(page_content=content, metadata=metadata))

            return documents

        except Exception as e:
            logger.error(f"Failed to load GitHub discussions: {e}")
            return []


class GitHubGistsLoader(BaseLoader):
    """Custom loader for GitHub Gists."""

    def __init__(
        self,
        username: Optional[str] = None,
        gist_id: Optional[str] = None,
        public_only: bool = True,
        max_gists: int = 100,
        access_token: Optional[str] = None,
    ):
        self.username = username
        self.gist_id = gist_id
        self.public_only = public_only
        self.max_gists = max_gists
        self.access_token = access_token

    def load(self) -> List[Document]:
        """Load GitHub gists."""
        try:
            import requests

            documents = []
            headers = {"Accept": "application/vnd.github.v3+json"}
            if self.access_token:
                headers["Authorization"] = f"token {self.access_token}"

            if self.gist_id:
                # Load specific gist
                url = f"https://api.github.com/gists/{self.gist_id}"
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    gist = response.json()
                    documents.extend(self._process_gist(gist))

            elif self.username:
                # Load user's gists
                url = f"https://api.github.com/users/{self.username}/gists"
                params = {"per_page": min(self.max_gists, 100)}

                response = requests.get(url, headers=headers, params=params)

                if response.status_code == 200:
                    gists = response.json()
                    for gist in gists[: self.max_gists]:
                        if self.public_only and not gist.get("public"):
                            continue
                        documents.extend(self._process_gist(gist))

            return documents

        except Exception as e:
            logger.error(f"Failed to load GitHub gists: {e}")
            return []

    def _process_gist(self, gist: Dict[str, Any]) -> List[Document]:
        """Process a single gist into documents."""
        documents = []

        for filename, file_info in gist.get("files", {}).items():
            content = f"# Gist: {gist['description'] or 'Untitled'}\n"
            content += f"**File:** {filename}\n"
            content += f"**Language:** {file_info.get('language', 'Unknown')}\n"
            content += f"**Size:** {file_info.get('size', 0)} bytes\n\n"
            content += "```" + (file_info.get("language", "").lower() or "") + "\n"
            content += file_info.get("content", "")
            content += "\n```"

            metadata = {
                "source": gist["html_url"],
                "type": "github_gist",
                "gist_id": gist["id"],
                "filename": filename,
                "language": file_info.get("language"),
                "size": file_info.get("size"),
                "public": gist.get("public", True),
                "created_at": gist.get("created_at"),
                "updated_at": gist.get("updated_at"),
            }

            documents.append(Document(page_content=content, metadata=metadata))

        return documents


class GitHubReleasesLoader(BaseLoader):
    """Custom loader for GitHub Releases."""

    def __init__(
        self,
        repo_url: str,
        include_prereleases: bool = False,
        include_drafts: bool = False,
        max_releases: int = 50,
        include_release_notes: bool = True,
        include_assets: bool = True,
        access_token: Optional[str] = None,
    ):
        self.repo_url = repo_url
        self.include_prereleases = include_prereleases
        self.include_drafts = include_drafts
        self.max_releases = max_releases
        self.include_release_notes = include_release_notes
        self.include_assets = include_assets
        self.access_token = access_token

        # Parse repo info
        parsed = urlparse(repo_url)
        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) >= 2:
            self.owner = path_parts[0]
            self.repo = path_parts[1]
        else:
            raise ValueError(f"Invalid GitHub URL: {repo_url}")

    def load(self) -> List[Document]:
        """Load GitHub releases."""
        try:
            import requests

            documents = []
            headers = {"Accept": "application/vnd.github.v3+json"}
            if self.access_token:
                headers["Authorization"] = f"token {self.access_token}"

            url = f"https://api.github.com/repos/{self.owner}/{self.repo}/releases"
            params = {"per_page": min(self.max_releases, 100)}

            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                releases = response.json()

                for release in releases[: self.max_releases]:
                    if not self.include_drafts and release.get("draft"):
                        continue
                    if not self.include_prereleases and release.get("prerelease"):
                        continue

                    content = f"# Release: {release['name'] or release['tag_name']}\n"
                    content += f"**Tag:** {release['tag_name']}\n"
                    content += f"**Published:** {release['published_at']}\n"
                    content += f"**Author:** {release['author']['login']}\n"
                    content += f"**Draft:** {release['draft']}\n"
                    content += f"**Pre-release:** {release['prerelease']}\n\n"

                    if self.include_release_notes:
                        content += f"## Release Notes\n\n{release['body']}\n\n"

                    if self.include_assets and release.get("assets"):
                        content += "## Assets\n\n"
                        for asset in release["assets"]:
                            content += (
                                f"- **{asset['name']}** ({asset['size']} bytes)\n"
                            )
                            content += f"  - Downloads: {asset['download_count']}\n"
                            content += f"  - URL: {asset['browser_download_url']}\n\n"

                    metadata = {
                        "source": release["html_url"],
                        "type": "github_release",
                        "tag_name": release["tag_name"],
                        "name": release["name"],
                        "draft": release["draft"],
                        "prerelease": release["prerelease"],
                        "published_at": release["published_at"],
                        "author": release["author"]["login"],
                    }

                    documents.append(Document(page_content=content, metadata=metadata))

            return documents

        except Exception as e:
            logger.error(f"Failed to load GitHub releases: {e}")
            return []


class GitHubActionsLoader(BaseLoader):
    """Custom loader for GitHub Actions workflows and runs."""

    def __init__(
        self,
        repo_url: str,
        workflow_name: Optional[str] = None,
        status: Optional[str] = None,
        include_logs: bool = False,
        max_runs: int = 50,
        access_token: Optional[str] = None,
    ):
        self.repo_url = repo_url
        self.workflow_name = workflow_name
        self.status = status
        self.include_logs = include_logs
        self.max_runs = max_runs
        self.access_token = access_token

        # Parse repo info
        parsed = urlparse(repo_url)
        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) >= 2:
            self.owner = path_parts[0]
            self.repo = path_parts[1]
        else:
            raise ValueError(f"Invalid GitHub URL: {repo_url}")

    def load(self) -> List[Document]:
        """Load GitHub Actions data."""
        try:
            import requests

            documents = []
            headers = {"Accept": "application/vnd.github.v3+json"}
            if self.access_token:
                headers["Authorization"] = f"token {self.access_token}"

            # First get workflows
            url = f"https://api.github.com/repos/{self.owner}/{self.repo}/actions/workflows"
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                workflows = response.json().get("workflows", [])

                for workflow in workflows:
                    if self.workflow_name and workflow["name"] != self.workflow_name:
                        continue

                    # Get runs for this workflow
                    runs_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/actions/workflows/{workflow['id']}/runs"
                    params = {"per_page": min(self.max_runs, 100)}
                    if self.status:
                        params["status"] = self.status

                    runs_response = requests.get(
                        runs_url, headers=headers, params=params
                    )

                    if runs_response.status_code == 200:
                        runs = runs_response.json().get("workflow_runs", [])

                        for run in runs[: self.max_runs]:
                            content = f"# Workflow Run: {workflow['name']}\n"
                            content += f"**Run Number:** {run['run_number']}\n"
                            content += f"**Status:** {run['status']}\n"
                            content += f"**Conclusion:** {run['conclusion']}\n"
                            content += f"**Branch:** {run['head_branch']}\n"
                            content += f"**Commit:** {run['head_sha'][:8]}\n"
                            content += f"**Started:** {run['run_started_at']}\n"
                            content += f"**Event:** {run['event']}\n\n"

                            metadata = {
                                "source": run["html_url"],
                                "type": "github_action_run",
                                "workflow_name": workflow["name"],
                                "run_number": run["run_number"],
                                "status": run["status"],
                                "conclusion": run["conclusion"],
                                "branch": run["head_branch"],
                                "commit": run["head_sha"],
                                "event": run["event"],
                            }

                            documents.append(
                                Document(page_content=content, metadata=metadata)
                            )

            return documents

        except Exception as e:
            logger.error(f"Failed to load GitHub Actions: {e}")
            return []


class GitHubWikiLoader(BaseLoader):
    """Custom loader for GitHub Wiki pages."""

    def __init__(
        self,
        repo_url: str,
        page_name: Optional[str] = None,
        include_history: bool = False,
        access_token: Optional[str] = None,
    ):
        self.repo_url = repo_url
        self.page_name = page_name
        self.include_history = include_history
        self.access_token = access_token

        # Parse repo info
        parsed = urlparse(repo_url)
        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) >= 2:
            self.owner = path_parts[0]
            self.repo = path_parts[1]
        else:
            raise ValueError(f"Invalid GitHub URL: {repo_url}")

    def load(self) -> List[Document]:
        """Load GitHub Wiki pages."""
        try:
            # GitHub Wiki pages are typically accessed via git clone
            # For simplicity, we'll use the web scraping approach
            documents = []

            # Wiki URL format
            wiki_url = f"https://github.com/{self.owner}/{self.repo}/wiki"

            if self.page_name:
                # Load specific page
                page_url = f"{wiki_url}/{self.page_name.replace(' ', '-')}"
                content = f"# Wiki Page: {self.page_name}\n\n"
                content += f"Source: {page_url}\n\n"
                content += "Note: Full wiki content loading requires web scraping or git clone of wiki repository."

                metadata = {
                    "source": page_url,
                    "type": "github_wiki_page",
                    "page_name": self.page_name,
                }

                documents.append(Document(page_content=content, metadata=metadata))
            else:
                # List all wiki pages
                content = f"# GitHub Wiki: {self.owner}/{self.repo}\n\n"
                content += f"Wiki URL: {wiki_url}\n\n"
                content += "Note: Full wiki content loading requires web scraping or git clone of wiki repository."

                metadata = {
                    "source": wiki_url,
                    "type": "github_wiki",
                }

                documents.append(Document(page_content=content, metadata=metadata))

            return documents

        except Exception as e:
            logger.error(f"Failed to load GitHub Wiki: {e}")
            return []


# Export enhanced GitHub sources
__all__ = [
    "GitHubDiscussionsSource",
    "GitHubGistsSource",
    "GitHubReleasesSource",
    "GitHubActionsSource",
    "GitHubWikiSource",
    "GitHubDiscussionsLoader",
    "GitHubGistsLoader",
    "GitHubReleasesLoader",
    "GitHubActionsLoader",
    "GitHubWikiLoader",
]
