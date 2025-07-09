import logging
import os
import re
from datetime import datetime
from functools import lru_cache
from typing import Any, Dict, List, Optional, Tuple

import httpx
from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    PrivateAttr,
    SecretStr,
    field_validator,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class GithubSettings(BaseSettings):
    """GitHub-related environment settings."""

    github_token: Optional[SecretStr] = Field(
        default=None,
        description="GitHub personal access token from environment",
        alias="GITHUB_TOKEN",
    )

    github_api_token: Optional[SecretStr] = Field(
        default=None,
        description="Alternative GitHub API token",
        alias="GITHUB_API_TOKEN",
    )

    github_pat: Optional[SecretStr] = Field(
        default=None, description="GitHub Personal Access Token", alias="GITHUB_PAT"
    )

    github_default_branch: str = Field(
        default="main",
        description="Default branch name to try first",
        alias="GITHUB_DEFAULT_BRANCH",
    )

    github_fallback_branches: List[str] = Field(
        default=["main", "master", "develop", "development", "prod", "production"],
        description="Branches to try if default fails",
        alias="GITHUB_FALLBACK_BRANCHES",
    )

    github_api_timeout: int = Field(
        default=10,
        description="Timeout for GitHub API calls in seconds",
        alias="GITHUB_API_TIMEOUT",
    )

    github_auto_retry_branches: bool = Field(
        default=True,
        description="Automatically try fallback branches if specified branch doesn't exist",
        alias="GITHUB_AUTO_RETRY_BRANCHES",
    )

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    @property
    def active_token(self) -> Optional[SecretStr]:
        """Get the first available token."""
        return self.github_token or self.github_api_token or self.github_pat


@lru_cache(maxsize=1)
def get_github_settings() -> GithubSettings:
    """Get cached GitHub settings."""
    return GithubSettings()


class GithubRepo(BaseModel):
    """Configuration for a GitHub repository with automatic validation and discovery.

    Features:
    - Automatic branch discovery with fallback (main -> master -> develop -> etc.)
    - Smart URL parsing from any GitHub URL format
    - Environment variable support
    - Automatic validation of repository existence
    - Token management with environment fallback
    """

    # Core identification fields
    owner: Optional[str] = Field(
        default=None,
        description="GitHub username or organization that owns the repository",
        min_length=1,
        max_length=39,
        examples=["microsoft", "facebook", "openai"],
    )

    name: Optional[str] = Field(
        default=None,
        description="Repository name",
        min_length=1,
        max_length=100,
        examples=["vscode", "react", "langchain"],
    )

    # URL input (can be provided instead of owner/name)
    url: Optional[HttpUrl] = Field(
        default=None,
        description="Any GitHub URL (repo, file, API, etc.) - will be parsed to extract owner/name",
        examples=[
            "https://github.com/microsoft/vscode",
            "https://github.com/langchain-ai/langchain/blob/main/README.md",
            "https://api.github.com/repos/openai/gpt-3",
        ],
    )

    # Access configuration
    is_private: Optional[bool] = Field(
        default=None,
        description="Whether the repository is private (auto-detected if not specified)",
    )

    branch: Optional[str] = Field(
        default=None,
        description="Preferred branch (will fallback to main/master if not found)",
        min_length=1,
    )

    # Authentication
    access_token: Optional[SecretStr] = Field(
        default=None,
        description="GitHub personal access token (falls back to environment variables)",
    )

    # Auto-populated fields
    api_url: Optional[HttpUrl] = Field(
        default=None, description="GitHub API URL (auto-generated)", exclude=True
    )

    clone_url: Optional[HttpUrl] = Field(
        default=None, description="Git clone URL (auto-generated)", exclude=True
    )

    default_branch: Optional[str] = Field(
        default=None,
        description="The actual default branch from GitHub (auto-discovered)",
    )

    discovered_branch: Optional[str] = Field(
        default=None, description="The branch that was actually found and validated"
    )

    available_branches: List[str] = Field(
        default_factory=list,
        description="List of available branches discovered during validation",
    )

    # Validation state
    is_valid: bool = Field(
        default=False, description="Whether the repository has been validated to exist"
    )

    validation_error: Optional[str] = Field(
        default=None, description="Error message if validation failed"
    )

    validation_warnings: List[str] = Field(
        default_factory=list,
        description="Warnings from validation (e.g., branch fallback used)",
    )

    # Additional metadata
    description: Optional[str] = Field(default=None)
    topics: List[str] = Field(default_factory=list)
    stars: Optional[int] = Field(default=None, ge=0)
    forks: Optional[int] = Field(default=None, ge=0)
    last_updated: Optional[datetime] = Field(default=None)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # Branch fallback configuration
    auto_retry_branches: bool = Field(
        default=True,
        description="Automatically try fallback branches if specified branch doesn't exist",
    )

    fallback_branches: List[str] = Field(
        default_factory=lambda: ["main", "master"],
        description="Branches to try if the specified branch doesn't exist",
    )

    # Private attributes
    _settings: Optional[GithubSettings] = PrivateAttr(default=None)
    _http_client: Optional[httpx.Client] = PrivateAttr(default=None)
    _branch_cache: Dict[str, bool] = PrivateAttr(default_factory=dict)

    model_config = {"arbitrary_types_allowed": True, "validate_assignment": True}

    @property
    def settings(self) -> GithubSettings:
        """Lazy-load settings."""
        if self._settings is None:
            self._settings = get_github_settings()
        return self._settings

    @property
    def http_client(self) -> httpx.Client:
        """Lazy-load HTTP client."""
        if self._http_client is None:
            self._http_client = httpx.Client(timeout=self.settings.github_api_timeout)
        return self._http_client

    def __del__(self):
        """Cleanup HTTP client."""
        if self._http_client is not None:
            self._http_client.close()

    @field_validator("owner", "name")
    @classmethod
    def validate_github_identifier(cls, v: Optional[str]) -> Optional[str]:
        """Validate GitHub username/repo name format."""
        if v is None:
            return v
        if not re.match(r"^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$", v):
            raise ValueError(
                f"Invalid GitHub identifier format: '{v}'. "
                "Must start with alphanumeric, can contain hyphens, "
                "and must end with alphanumeric."
            )
        return v

    @model_validator(mode="after")
    def extract_from_url_and_validate(self) -> "GithubRepo":
        """Extract owner/name from URL if provided and validate the repository."""
        # Step 1: Extract owner/name from URL if needed
        if self.url and (not self.owner or not self.name):
            owner, name = self._parse_github_url(str(self.url))
            if owner and name:
                self.owner = self.owner or owner
                self.name = self.name or name

        # Validate we have owner and name
        if not self.owner or not self.name:
            raise ValueError(
                "Either provide 'owner' and 'name', or a valid GitHub 'url' to parse"
            )

        # Step 2: Get access token from env if not provided
        if not self.access_token and self.settings.active_token:
            self.access_token = self.settings.active_token

        # Step 3: Generate URLs
        self.api_url = HttpUrl(f"https://api.github.com/repos/{self.owner}/{self.name}")
        self.clone_url = HttpUrl(f"https://github.com/{self.owner}/{self.name}.git")
        self.url = self.url or HttpUrl(f"https://github.com/{self.owner}/{self.name}")

        # Step 4: Configure fallback branches
        if self.auto_retry_branches and self.settings.github_auto_retry_branches:
            # Merge user fallbacks with system fallbacks
            all_fallbacks = []
            if self.branch and self.branch not in self.fallback_branches:
                all_fallbacks.append(self.branch)
            all_fallbacks.extend(self.fallback_branches)
            all_fallbacks.extend(self.settings.github_fallback_branches)
            # Remove duplicates while preserving order
            self.fallback_branches = list(dict.fromkeys(all_fallbacks))

        # Step 5: Validate repository exists and discover branch
        try:
            self._validate_and_discover()
            self.is_valid = True
            self.validation_error = None
        except Exception as e:
            self.is_valid = False
            self.validation_error = str(e)
            logger.error(
                f"Repository validation failed for {self.owner}/{self.name}: {e}"
            )

        return self

    def _parse_github_url(self, url: str) -> Tuple[Optional[str], Optional[str]]:
        """Parse various GitHub URL formats to extract owner and repository name."""
        patterns = [
            # Standard repo URLs
            r"github\.com/([^/]+)/([^/\s]+?)(?:\.git)?/?$",
            # File/folder URLs
            r"github\.com/([^/]+)/([^/]+)/(?:blob|tree|commit|pulls|issues)",
            # API URLs
            r"api\.github\.com/repos/([^/]+)/([^/\s]+)",
            # Gist URLs (special case)
            r"gist\.github\.com/([^/]+)/([a-f0-9]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                owner, name = match.groups()
                # Clean up the name (remove .git suffix if present)
                name = name.rstrip("/").replace(".git", "")
                return owner, name

        return None, None

    def _validate_and_discover(self) -> None:
        """Validate repository exists and discover default branch."""
        headers = self.get_api_headers()

        try:
            # Try to get repository info
            response = self.http_client.get(
                str(self.api_url), headers=headers, follow_redirects=True
            )

            if response.status_code == 404:
                raise ValueError(f"Repository {self.owner}/{self.name} not found")
            elif response.status_code == 403:
                # Rate limited or forbidden
                if not self.access_token:
                    raise ValueError(
                        "GitHub API rate limit exceeded or repository is private. "
                        "Please provide an access token."
                    )
                else:
                    raise ValueError("Access forbidden - check your token permissions")
            elif response.status_code != 200:
                raise ValueError(
                    f"GitHub API error: {response.status_code} - {response.text}"
                )

            # Parse repository data
            data = response.json()

            # Update metadata
            self.default_branch = data.get("default_branch", "main")
            self.is_private = data.get("private", False)
            self.description = data.get("description")
            self.stars = data.get("stargazers_count", 0)
            self.forks = data.get("forks_count", 0)

            if data.get("updated_at"):
                self.last_updated = datetime.fromisoformat(
                    data["updated_at"].replace("Z", "+00:00")
                )

            # Discover and validate branch
            self._discover_and_validate_branch()

        except httpx.RequestError as e:
            raise ValueError(f"Failed to connect to GitHub API: {e}")

    def _discover_and_validate_branch(self) -> None:
        """Discover available branches and validate/select the appropriate one."""
        headers = self.get_api_headers()

        # First, try to get all branches
        try:
            response = self.http_client.get(f"{self.api_url}/branches", headers=headers)
            if response.status_code == 200:
                branches_data = response.json()
                self.available_branches = [b["name"] for b in branches_data]
                logger.info(
                    f"Found {len(self.available_branches)} branches for {self.full_name}"
                )
        except Exception as e:
            logger.warning(f"Could not fetch branch list: {e}")
            self.available_branches = []

        # Now find the best branch to use
        if self.auto_retry_branches:
            # Build list of branches to try
            branches_to_try = []

            # 1. User-specified branch (if any)
            if self.branch:
                branches_to_try.append(self.branch)

            # 2. Default branch from repo
            if self.default_branch and self.default_branch not in branches_to_try:
                branches_to_try.append(self.default_branch)

            # 3. Fallback branches
            for fb in self.fallback_branches:
                if fb not in branches_to_try:
                    branches_to_try.append(fb)

            # Try each branch
            valid_branch = None
            for branch in branches_to_try:
                if self._check_branch_exists(branch):
                    valid_branch = branch
                    if branch != self.branch and self.branch:
                        self.validation_warnings.append(
                            f"Specified branch '{self.branch}' not found, using '{branch}' instead"
                        )
                    break

            if valid_branch:
                self.discovered_branch = valid_branch
                # Update branch to the one we're actually using
                if not self.branch:
                    self.branch = valid_branch
                logger.info(f"Using branch '{valid_branch}' for {self.full_name}")
            else:
                # No valid branch found
                tried_branches = ", ".join(branches_to_try[:5])
                if len(branches_to_try) > 5:
                    tried_branches += f" and {len(branches_to_try) - 5} more"

                available_msg = ""
                if self.available_branches:
                    available_msg = (
                        f" Available branches: {', '.join(self.available_branches[:5])}"
                    )
                    if len(self.available_branches) > 5:
                        available_msg += f" and {len(self.available_branches) - 5} more"

                raise ValueError(
                    f"No valid branch found. Tried: {tried_branches}.{available_msg}"
                )
        else:
            # No auto-retry, just validate the specified branch
            if self.branch:
                if not self._check_branch_exists(self.branch):
                    raise ValueError(
                        f"Branch '{self.branch}' not found and auto-retry is disabled"
                    )
                self.discovered_branch = self.branch
            else:
                # Use default branch
                self.branch = self.default_branch
                self.discovered_branch = self.default_branch

    def _check_branch_exists(self, branch: str) -> bool:
        """Check if a specific branch exists (with caching)."""
        # Check cache first
        if branch in self._branch_cache:
            return self._branch_cache[branch]

        # Check available branches if we have them
        if self.available_branches:
            exists = branch in self.available_branches
            self._branch_cache[branch] = exists
            return exists

        # Otherwise make API call
        headers = self.get_api_headers()
        try:
            response = self.http_client.get(
                f"{self.api_url}/branches/{branch}", headers=headers
            )
            exists = response.status_code == 200
            self._branch_cache[branch] = exists
            return exists
        except Exception:
            self._branch_cache[branch] = False
            return False

    def get_api_headers(self) -> Dict[str, str]:
        """Get headers for GitHub API requests."""
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": f"Haive-Framework/{self.full_name}",
        }

        token = self.access_token or self.settings.active_token
        if token:
            headers["Authorization"] = f"token {token.get_secret_value()}"

        return headers

    @property
    def full_name(self) -> str:
        """Get the full repository name in 'owner/name' format."""
        return f"{self.owner}/{self.name}"

    @property
    def working_branch(self) -> str:
        """Get the actual working branch (discovered or specified)."""
        return self.discovered_branch or self.branch or self.default_branch or "main"

    @property
    def ssh_url(self) -> str:
        """Get the SSH clone URL for the repository."""
        return f"git@github.com:{self.owner}/{self.name}.git"

    @property
    def requires_auth(self) -> bool:
        """Check if authentication is required."""
        return self.is_private or bool(self.access_token)

    def get_file_url(self, file_path: str, raw: bool = False) -> str:
        """Get URL for a specific file in the repository."""
        file_path = file_path.lstrip("/")
        branch = self.working_branch

        if raw:
            return f"https://raw.githubusercontent.com/{self.owner}/{self.name}/{branch}/{file_path}"
        else:
            return f"{self.url}/blob/{branch}/{file_path}"

    def switch_branch(self, new_branch: str, validate: bool = True) -> None:
        """Switch to a different branch."""
        old_branch = self.branch
        self.branch = new_branch

        if validate:
            try:
                self._discover_and_validate_branch()
            except Exception as e:
                # Revert on failure
                self.branch = old_branch
                raise e

    def refresh(self) -> None:
        """Refresh repository metadata from GitHub."""
        self._validate_and_discover()

    def to_safe_dict(self) -> Dict[str, Any]:
        """Convert to dictionary excluding sensitive fields."""
        data = self.model_dump(
            exclude={
                "access_token",
                "api_url",
                "clone_url",
                "_settings",
                "_http_client",
                "_branch_cache",
            }
        )
        data["has_token"] = bool(self.access_token)
        data["working_branch"] = self.working_branch
        return data

    @classmethod
    def from_url(cls, url: str, **kwargs) -> "GithubRepo":
        """Create GithubRepo from any GitHub URL."""
        return cls(url=url, **kwargs)
