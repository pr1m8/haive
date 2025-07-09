import re
from typing import Any, ClassVar, Dict, List, Optional, Union
from urllib.parse import parse_qs, urlparse

from pydantic import Field, HttpUrl, computed_field, model_validator

from haive.core.engine.loaders.sources.base import BaseSource
from haive.core.engine.loaders.sources.types import SourceType


class WebSource(BaseSource):
    """
    Base class for all web-based sources.
    """

    url: HttpUrl = Field(description="URL of the resource")
    headers: Dict[str, str] = Field(default_factory=dict, description="HTTP headers")
    timeout: int = Field(default=30, description="Timeout in seconds")
    verify_ssl: bool = Field(
        default=True, description="Whether to verify SSL certificates"
    )

    # Class variable for domain-based source type mapping
    DOMAIN_PATTERNS: ClassVar[Dict[str, SourceType]] = {
        r"github\.com": SourceType.GITHUB,
        r"arxiv\.org": SourceType.ARXIV,
        r"reddit\.com": SourceType.REDDIT,
        r"twitter\.com": SourceType.TWITTER,
        r"youtube\.com": SourceType.YOUTUBE,
        r"youtu\.be": SourceType.YOUTUBE,
        r"wikipedia\.org": SourceType.WIKIPEDIA,
        r"news\.ycombinator\.com": SourceType.HACKER_NEWS,
        r"collegeconfidential\.com": SourceType.COLLEGE_CONFIDENTIAL,
    }

    @model_validator(mode="after")
    def validate_source_type(self):
        """Automatically set more specific source type based on URL domain."""
        url_str = str(self.url)
        parsed = urlparse(url_str)
        domain = parsed.netloc

        # Check for specific domain matches
        for pattern, source_type in self.DOMAIN_PATTERNS.items():
            if re.search(pattern, domain, re.IGNORECASE):
                self.source_type = source_type
                break

        return self

    def get_source_value(self) -> HttpUrl:
        """Get the URL as the source value."""
        return self.url

    def validate(self) -> bool:
        """
        Basic validation of URL format.
        Note: This doesn't check if the URL is accessible.
        """
        return True  # URL is already validated by Pydantic

    @computed_field
    def domain(self) -> str:
        """Get the domain from the URL."""
        parsed = urlparse(str(self.url))
        return parsed.netloc

    @computed_field
    def scheme(self) -> str:
        """Get the scheme from the URL."""
        parsed = urlparse(str(self.url))
        return parsed.scheme

    @computed_field
    def path(self) -> str:
        """Get the path from the URL."""
        parsed = urlparse(str(self.url))
        return parsed.path

    @computed_field
    def query_params(self) -> Dict[str, List[str]]:
        """Get the query parameters from the URL."""
        parsed = urlparse(str(self.url))
        return parse_qs(parsed.query)

    def get_metadata(self) -> Dict[str, Any]:
        """Get URL metadata."""
        metadata = super().get_metadata()
        metadata.update(
            {
                "url": str(self.url),
                "domain": self.domain,
                "scheme": self.scheme,
                "path": self.path,
                "headers": {
                    k: v
                    for k, v in self.headers.items()
                    if k.lower() != "authorization"
                },
            }
        )
        return metadata

    @classmethod
    def from_url(cls, url: Union[str, HttpUrl], **kwargs) -> "WebSource":
        """Create a WebSource from a URL."""
        # Set default name from domain if not provided
        if "name" not in kwargs:
            parsed = urlparse(str(url))
            kwargs["name"] = parsed.netloc

        return cls(url=url, **kwargs)


class ApiSource(WebSource):
    """Source for API endpoints."""

    source_type: SourceType = Field(default=SourceType.API)
    method: str = Field(default="GET", description="HTTP method")
    params: Dict[str, Any] = Field(default_factory=dict, description="Query parameters")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Request data")
    auth: Optional[Dict[str, str]] = Field(
        default=None, description="Authentication credentials"
    )

    def get_metadata(self) -> Dict[str, Any]:
        """Get API metadata."""
        metadata = super().get_metadata()
        metadata.update({"method": self.method, "params": self.params})
        return metadata
