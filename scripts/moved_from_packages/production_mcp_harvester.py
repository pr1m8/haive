#!/usr/bin/env python3
"""Production MCP Server Harvester.

Downloads and parses MCP servers from all major sources in standardized format.
Keeps track of sources, deduplicates, and maintains data quality.

Usage:
    poetry run python examples/production_mcp_harvester.py
"""

import asyncio
import base64
import json
import logging
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import aiohttp

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class MCPServerRecord:
    """Standardized MCP server record."""

    # Core identifiers
    name: str
    source: str
    source_url: str

    # Repository info
    repository_url: str | None = None
    repository_owner: str | None = None
    repository_name: str | None = None

    # Metadata
    description: str | None = None
    category: str | None = None
    tags: list[str] = None

    # Installation
    npm_package: str | None = None
    install_command: str | None = None
    setup_instructions: str | None = None

    # Technical details
    transport_types: list[str] = None
    capabilities: list[str] = None
    dependencies: list[str] = None

    # Quality indicators
    stars: int | None = None
    last_updated: str | None = None
    has_documentation: bool = False
    is_official: bool = False

    # Tracking
    discovered_at: str = None
    last_checked: str = None
    source_metadata: dict[str, Any] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.transport_types is None:
            self.transport_types = []
        if self.capabilities is None:
            self.capabilities = []
        if self.dependencies is None:
            self.dependencies = []
        if self.source_metadata is None:
            self.source_metadata = {}
        if self.discovered_at is None:
            self.discovered_at = datetime.now(UTC).isoformat()


class MCPSourceHarvester:
    """Base class for MCP source harvesters."""

    def __init__(self, source_name: str, session: aiohttp.ClientSession):
        self.source_name = source_name
        self.session = session
        self.harvested_servers: list[MCPServerRecord] = []

    async def harvest(self) -> list[MCPServerRecord]:
        """Override in subclasses."""
        raise NotImplementedError

    def _extract_github_info(self, url: str) -> dict[str, str]:
        """Extract owner and repo from GitHub URL."""
        if not url or "github.com" not in url:
            return {}

        match = re.search(r"github\.com/([^/]+)/([^/]+)", url)
        if match:
            owner, repo = match.groups()
            # Clean repo name
            repo = repo.replace(".git", "").split("/")[0].split("?")[0].split("#")[0]
            return {
                "repository_owner": owner,
                "repository_name": repo,
                "repository_url": f"https://github.com/{owner}/{repo}",
            }
        return {}

    def _categorize_server(self, name: str, description: str = "") -> str:
        """Categorize server based on name and description."""
        text = f"{name} {description}".lower()

        categories = {
            "filesystem": ["file", "filesystem", "storage", "disk", "directory"],
            "database": [
                "database",
                "sql",
                "mongo",
                "redis",
                "postgres",
                "mysql",
                "sqlite",
            ],
            "version_control": ["git", "github", "gitlab", "version", "commit"],
            "communication": ["slack", "discord", "teams", "chat", "message"],
            "api_integration": ["api", "rest", "graphql", "webhook", "http"],
            "search": ["search", "elastic", "solr", "index", "query"],
            "cloud": ["aws", "azure", "gcp", "cloud", "docker", "kubernetes"],
            "security": ["auth", "security", "vault", "secret", "token"],
            "monitoring": ["monitor", "log", "metric", "alert", "health"],
            "ai_ml": ["ai", "ml", "model", "embedding", "vector"],
            "productivity": ["notion", "calendar", "task", "todo", "project"],
            "finance": ["payment", "stripe", "paypal", "finance", "crypto"],
            "media": ["image", "video", "audio", "media", "photo"],
        }

        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category

        return "utility"


class GitHubRepoHarvester(MCPSourceHarvester):
    """Harvests MCP servers from GitHub repositories."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        repo_url: str,
        github_token: str | None = None,
    ):
        owner_repo = repo_url.replace("https://github.com/", "").strip("/")
        super().__init__(f"github:{owner_repo}", session)
        self.repo_url = repo_url
        self.owner, self.repo = owner_repo.split("/")
        self.github_token = github_token
        self.api_base = "https://api.github.com"

    def _get_headers(self) -> dict[str, str]:
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"
        return headers

    async def harvest(self) -> list[MCPServerRecord]:
        """Harvest servers from a GitHub repository."""
        logger.info(f"🔍 Harvesting {self.repo_url}")

        try:
            # Get repository info
            repo_info = await self._get_repo_info()

            # Get README content
            readme_content = await self._get_readme()

            # Parse servers based on repo type
            if "awesome" in self.repo.lower():
                servers = await self._parse_awesome_list(readme_content, repo_info)
            elif self.owner == "modelcontextprotocol":
                servers = await self._parse_official_repo(repo_info)
            else:
                servers = await self._parse_generic_repo(readme_content, repo_info)

            self.harvested_servers.extend(servers)
            logger.info(f"✅ Found {len(servers)} servers in {self.repo_url}")
            return servers

        except Exception as e:
            logger.exception(f"❌ Failed to harvest {self.repo_url}: {e}")
            return []

    async def _get_repo_info(self) -> dict[str, Any]:
        """Get repository information from GitHub API."""
        url = f"{self.api_base}/repos/{self.owner}/{self.repo}"
        async with self.session.get(url, headers=self._get_headers()) as response:
            if response.status == 200:
                return await response.json()
            logger.warning(
                f"Failed to get repo info for {self.owner}/{self.repo}: {response.status}"
            )
            return {}

    async def _get_readme(self) -> str:
        """Get README content from repository."""
        url = f"{self.api_base}/repos/{self.owner}/{self.repo}/readme"
        async with self.session.get(url, headers=self._get_headers()) as response:
            if response.status == 200:
                data = await response.json()
                content = base64.b64decode(data["content"]).decode("utf-8")
                return content
            logger.warning(f"No README found for {self.owner}/{self.repo}")
            return ""

    async def _parse_awesome_list(
        self, readme_content: str, repo_info: dict[str, Any]
    ) -> list[MCPServerRecord]:
        """Parse awesome-mcp-servers list format."""
        servers = []

        # Look for GitHub links in markdown
        github_pattern = r"\[([^\]]+)\]\((https://github\.com/[^)]+)\)"
        matches = re.findall(github_pattern, readme_content)

        for name, url in matches:
            if "mcp" in name.lower() or "mcp" in url.lower():
                github_info = self._extract_github_info(url)

                # Extract description from surrounding context
                description = self._extract_description_from_context(
                    readme_content, url
                )

                server = MCPServerRecord(
                    name=name.strip(),
                    source=self.source_name,
                    source_url=self.repo_url,
                    description=description,
                    category=self._categorize_server(name, description),
                    is_official=False,
                    has_documentation=True,
                    source_metadata={
                        "readme_source": True,
                        "awesome_list": True,
                        "repo_stars": repo_info.get("stargazers_count", 0),
                    },
                    **github_info,
                )
                servers.append(server)

        return servers

    def _extract_description_from_context(self, content: str, url: str) -> str:
        """Extract description from surrounding markdown context."""
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if url in line:
                # Look for description in same line or next line
                desc_match = re.search(r"\)\s*[-–]\s*(.+)", line)
                if desc_match:
                    return desc_match.group(1).strip()
                # Check next line
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line and not next_line.startswith(("*", "-", "#", "[")):
                        return next_line
        return ""

    async def _parse_official_repo(
        self, repo_info: dict[str, Any]
    ) -> list[MCPServerRecord]:
        """Parse official MCP repository structure."""
        servers = []

        # Get directory listing for official servers
        url = f"{self.api_base}/repos/{self.owner}/{self.repo}/contents"
        async with self.session.get(url, headers=self._get_headers()) as response:
            if response.status == 200:
                contents = await response.json()

                for item in contents:
                    if item["type"] == "dir" or (
                        item["name"].endswith(".js") or item["name"].endswith(".ts")
                    ):
                        server_name = item["name"].replace(".js", "").replace(".ts", "")

                        if (
                            "server" in server_name.lower()
                            or "mcp" in server_name.lower()
                        ):
                            server = MCPServerRecord(
                                name=f"@modelcontextprotocol/server-{server_name}",
                                source=self.source_name,
                                source_url=self.repo_url,
                                repository_url=self.repo_url,
                                repository_owner=self.owner,
                                repository_name=self.repo,
                                description=f"Official {server_name} MCP server",
                                category=self._categorize_server(server_name),
                                npm_package=f"@modelcontextprotocol/server-{server_name}",
                                install_command=f"npm install @modelcontextprotocol/server-{server_name}",
                                is_official=True,
                                has_documentation=True,
                                stars=repo_info.get("stargazers_count", 0),
                                last_updated=repo_info.get("updated_at"),
                                source_metadata={
                                    "official_repo": True,
                                    "repo_stars": repo_info.get("stargazers_count", 0),
                                },
                            )
                            servers.append(server)

        return servers

    async def _parse_generic_repo(
        self, readme_content: str, repo_info: dict[str, Any]
    ) -> list[MCPServerRecord]:
        """Parse a generic MCP repository."""
        # Create single server record for the repository itself
        github_info = self._extract_github_info(self.repo_url)

        server = MCPServerRecord(
            name=f"{self.owner}/{self.repo}",
            source=self.source_name,
            source_url=self.repo_url,
            description=repo_info.get("description", ""),
            category=self._categorize_server(
                self.repo, repo_info.get("description", "")
            ),
            has_documentation=bool(readme_content),
            stars=repo_info.get("stargazers_count", 0),
            last_updated=repo_info.get("updated_at"),
            source_metadata={
                "direct_repo": True,
                "repo_stars": repo_info.get("stargazers_count", 0),
                "language": repo_info.get("language"),
                "size": repo_info.get("size"),
            },
            **github_info,
        )

        return [server]


class GitHubTopicHarvester(MCPSourceHarvester):
    """Harvests MCP servers from GitHub topic search."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        topic: str,
        github_token: str | None = None,
    ):
        super().__init__(f"github-topic:{topic}", session)
        self.topic = topic
        self.github_token = github_token
        self.api_base = "https://api.github.com"

    def _get_headers(self) -> dict[str, str]:
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"
        return headers

    async def harvest(self) -> list[MCPServerRecord]:
        """Harvest servers from GitHub topic search."""
        logger.info(f"🔍 Searching GitHub topic: {self.topic}")

        try:
            servers = []
            page = 1
            per_page = 30

            while page <= 5:  # Limit to first 5 pages (150 repos)
                url = f"{self.api_base}/search/repositories"
                params = {
                    "q": f"topic:{self.topic}",
                    "sort": "stars",
                    "order": "desc",
                    "per_page": per_page,
                    "page": page,
                }

                async with self.session.get(
                    url, headers=self._get_headers(), params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        items = data.get("items", [])

                        if not items:
                            break

                        for repo in items:
                            github_info = self._extract_github_info(repo["html_url"])

                            server = MCPServerRecord(
                                name=repo["full_name"],
                                source=self.source_name,
                                source_url=f"https://github.com/topics/{self.topic}",
                                description=repo.get("description", ""),
                                category=self._categorize_server(
                                    repo["name"], repo.get("description", "")
                                ),
                                tags=[self.topic],
                                has_documentation=bool(repo.get("description")),
                                stars=repo.get("stargazers_count", 0),
                                last_updated=repo.get("updated_at"),
                                source_metadata={
                                    "topic_search": True,
                                    "topic": self.topic,
                                    "repo_stars": repo.get("stargazers_count", 0),
                                    "language": repo.get("language"),
                                    "forks": repo.get("forks_count", 0),
                                },
                                **github_info,
                            )
                            servers.append(server)

                        page += 1
                    else:
                        logger.warning(f"GitHub topic search failed: {response.status}")
                        break

            self.harvested_servers.extend(servers)
            logger.info(f"✅ Found {len(servers)} repos for topic '{self.topic}'")
            return servers

        except Exception as e:
            logger.exception(f"❌ Failed to search topic {self.topic}: {e}")
            return []


class RegistryWebHarvester(MCPSourceHarvester):
    """Harvests MCP servers from web registries."""

    def __init__(
        self, session: aiohttp.ClientSession, registry_name: str, base_url: str
    ):
        super().__init__(f"registry:{registry_name}", session)
        self.registry_name = registry_name
        self.base_url = base_url

    async def harvest(self) -> list[MCPServerRecord]:
        """Harvest servers from web registry."""
        logger.info(f"🔍 Harvesting {self.registry_name} registry")

        try:
            if self.registry_name.lower() == "pulsemcp":
                return await self._harvest_pulsemcp()
            if self.registry_name.lower() == "smithery":
                return await self._harvest_smithery()
            if self.registry_name.lower() == "mcpregistry":
                return await self._harvest_mcpregistry()
            return await self._harvest_generic_registry()

        except Exception as e:
            logger.exception(f"❌ Failed to harvest {self.registry_name}: {e}")
            return []

    async def _harvest_pulsemcp(self) -> list[MCPServerRecord]:
        """Harvest from PulseMCP registry."""
        servers = []

        # Try different API endpoints
        endpoints = [
            f"{self.base_url}/api/servers",
            f"{self.base_url}/servers.json",
            f"{self.base_url}/api/v1/servers",
        ]

        for endpoint in endpoints:
            try:
                async with self.session.get(endpoint) as response:
                    if response.status == 200:
                        data = await response.json()
                        servers = self._parse_pulsemcp_data(data)
                        break
            except:
                continue

        # If API fails, try web scraping
        if not servers:
            servers = await self._scrape_pulsemcp_web()

        self.harvested_servers.extend(servers)
        logger.info(f"✅ Found {len(servers)} servers from PulseMCP")
        return servers

    def _parse_pulsemcp_data(self, data: Any) -> list[MCPServerRecord]:
        """Parse PulseMCP API response."""
        servers = []

        # Handle different response formats
        if isinstance(data, dict):
            items = data.get("servers", data.get("data", data.get("items", [])))
        elif isinstance(data, list):
            items = data
        else:
            return servers

        for item in items:
            if isinstance(item, dict):
                github_info = self._extract_github_info(
                    item.get("repository", item.get("url", ""))
                )

                server = MCPServerRecord(
                    name=item.get("name", item.get("title", "Unknown")),
                    source=self.source_name,
                    source_url=self.base_url,
                    description=item.get("description", ""),
                    category=self._categorize_server(
                        item.get("name", ""), item.get("description", "")
                    ),
                    npm_package=item.get("package"),
                    has_documentation=bool(item.get("description")),
                    source_metadata={"registry": "PulseMCP", "registry_data": item},
                    **github_info,
                )
                servers.append(server)

        return servers

    async def _scrape_pulsemcp_web(self) -> list[MCPServerRecord]:
        """Scrape PulseMCP website for server listings."""
        servers = []

        try:
            async with self.session.get(f"{self.base_url}/servers") as response:
                if response.status == 200:
                    html = await response.text()

                    # Parse HTML for server listings
                    # This would need actual HTML parsing - using regex for demo
                    github_pattern = r'href="(https://github\.com/[^"]+)"[^>]*>([^<]+)'
                    matches = re.findall(github_pattern, html)

                    for url, name in matches[:50]:  # Limit to first 50
                        github_info = self._extract_github_info(url)

                        server = MCPServerRecord(
                            name=name.strip(),
                            source=self.source_name,
                            source_url=self.base_url,
                            category=self._categorize_server(name),
                            has_documentation=True,
                            source_metadata={
                                "registry": "PulseMCP",
                                "scraped_web": True,
                            },
                            **github_info,
                        )
                        servers.append(server)

        except Exception as e:
            logger.warning(f"Failed to scrape PulseMCP web: {e}")

        return servers

    async def _harvest_smithery(self) -> list[MCPServerRecord]:
        """Harvest from Smithery registry."""
        servers = []

        # Try Smithery API endpoints
        endpoints = [f"{self.base_url}/api/servers", f"{self.base_url}/registry.json"]

        for endpoint in endpoints:
            try:
                async with self.session.get(endpoint) as response:
                    if response.status == 200:
                        data = await response.json()
                        servers = self._parse_smithery_data(data)
                        break
            except:
                continue

        # If API fails, try web scraping
        if not servers:
            servers = await self._scrape_smithery_web()

        self.harvested_servers.extend(servers)
        logger.info(f"✅ Found {len(servers)} servers from Smithery")
        return servers

    def _parse_smithery_data(self, data: Any) -> list[MCPServerRecord]:
        """Parse Smithery API response."""
        # Similar to PulseMCP parsing
        return self._parse_pulsemcp_data(data)  # Reuse logic

    async def _scrape_smithery_web(self) -> list[MCPServerRecord]:
        """Scrape Smithery website."""
        # Similar to PulseMCP scraping
        return await self._scrape_pulsemcp_web()  # Reuse logic

    async def _harvest_mcpregistry(self) -> list[MCPServerRecord]:
        """Harvest from mcpregistry.click."""
        # Similar pattern to other registries
        return await self._harvest_pulsemcp()  # Reuse logic

    async def _harvest_generic_registry(self) -> list[MCPServerRecord]:
        """Harvest from a generic registry."""
        return []


class ProductionMCPHarvester:
    """Production MCP server harvester coordinator."""

    def __init__(self, github_token: str | None = None):
        self.github_token = github_token
        self.session: aiohttp.ClientSession | None = None
        self.all_servers: list[MCPServerRecord] = []
        self.sources_processed = 0
        self.total_sources = 0

        # Data directory
        self.data_dir = Path(__file__).parent.parent / "data" / "mcp_servers"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    async def harvest_all(self) -> dict[str, Any]:
        """Harvest from all sources."""
        logger.info("🚀 Starting production MCP server harvest")

        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30)
        ) as session:
            self.session = session

            # Define all sources
            sources = self._define_sources()
            self.total_sources = len(sources)

            logger.info(f"📊 Harvesting from {self.total_sources} sources")

            # Harvest from each source
            for source in sources:
                try:
                    await self._harvest_source(source)
                    self.sources_processed += 1
                except Exception as e:
                    logger.exception(
                        f"❌ Failed to harvest {source.__class__.__name__}: {e}"
                    )

        # Deduplicate and process
        unique_servers = self._deduplicate_servers(self.all_servers)

        # Save results
        results = await self._save_results(unique_servers)

        logger.info(
            f"✅ Harvest complete! {len(unique_servers)} unique servers from {self.sources_processed}/{self.total_sources} sources"
        )

        return results

    def _define_sources(self) -> list[MCPSourceHarvester]:
        """Define all harvest sources."""
        sources = []

        # GitHub repositories
        github_repos = [
            "https://github.com/modelcontextprotocol/servers",
            "https://github.com/modelcontextprotocol/registry",
            "https://github.com/wong2/awesome-mcp-servers",
            "https://github.com/punkpeye/awesome-mcp-servers",
            "https://github.com/appcypher/awesome-mcp-servers",
            "https://github.com/TensorBlock/awesome-mcp-servers",
            "https://github.com/docker/mcp-servers",
            "https://github.com/smithery-ai/reference-servers",
            "https://github.com/cyanheads/model-context-protocol-resources",
        ]

        for repo_url in github_repos:
            sources.append(
                GitHubRepoHarvester(self.session, repo_url, self.github_token)
            )

        # GitHub topics
        topics = ["mcp-server", "model-context-protocol"]
        for topic in topics:
            sources.append(GitHubTopicHarvester(self.session, topic, self.github_token))

        # Web registries
        registries = [
            ("PulseMCP", "https://www.pulsemcp.com"),
            ("Smithery", "https://smithery.ai"),
            ("MCPRegistry", "https://mcpregistry.click"),
        ]

        for name, url in registries:
            sources.append(RegistryWebHarvester(self.session, name, url))

        return sources

    async def _harvest_source(self, harvester: MCPSourceHarvester):
        """Harvest from a single source."""
        try:
            servers = await harvester.harvest()
            self.all_servers.extend(servers)
            logger.info(
                f"📊 Progress: {self.sources_processed + 1}/{self.total_sources} sources"
            )
        except Exception as e:
            logger.exception(f"❌ Source {harvester.source_name} failed: {e}")

    def _deduplicate_servers(
        self, servers: list[MCPServerRecord]
    ) -> list[MCPServerRecord]:
        """Deduplicate servers based on repository URL and name."""
        logger.info(f"🔄 Deduplicating {len(servers)} servers...")

        seen_repos: set[str] = set()
        seen_names: set[str] = set()
        unique_servers = []

        for server in servers:
            # Create deduplication keys
            repo_key = server.repository_url if server.repository_url else ""
            name_key = server.name.lower().strip()

            # Skip if we've seen this repository or name
            if repo_key and repo_key in seen_repos:
                continue
            if name_key in seen_names:
                continue

            # Add to unique list
            unique_servers.append(server)
            if repo_key:
                seen_repos.add(repo_key)
            seen_names.add(name_key)

        logger.info(f"✅ Deduplicated to {len(unique_servers)} unique servers")
        return unique_servers

    async def _save_results(self, servers: list[MCPServerRecord]) -> dict[str, Any]:
        """Save harvest results."""
        logger.info("💾 Saving harvest results...")

        timestamp = datetime.now(UTC).isoformat()

        # Convert to dictionaries
        servers_data = [asdict(server) for server in servers]

        # Save raw harvest data
        harvest_file = self.data_dir / f"harvest_{timestamp.split('T')[0]}.json"
        with open(harvest_file, "w") as f:
            json.dump(
                {
                    "timestamp": timestamp,
                    "total_servers": len(servers),
                    "sources_processed": self.sources_processed,
                    "total_sources": self.total_sources,
                    "servers": servers_data,
                },
                f,
                indent=2,
            )

        # Update main database
        main_file = self.data_dir / "production_mcp_database.json"
        with open(main_file, "w") as f:
            json.dump(
                {
                    "last_updated": timestamp,
                    "total_servers": len(servers),
                    "servers": {server.name: asdict(server) for server in servers},
                },
                f,
                indent=2,
            )

        # Generate analytics
        analytics = self._generate_analytics(servers)
        analytics_file = self.data_dir / "harvest_analytics.json"
        with open(analytics_file, "w") as f:
            json.dump(analytics, f, indent=2)

        logger.info(f"📄 Saved harvest to {harvest_file}")
        logger.info(f"📄 Updated database at {main_file}")
        logger.info(f"📄 Generated analytics at {analytics_file}")

        return {
            "timestamp": timestamp,
            "total_servers": len(servers),
            "sources_processed": self.sources_processed,
            "analytics": analytics,
            "files": {
                "harvest": str(harvest_file),
                "database": str(main_file),
                "analytics": str(analytics_file),
            },
        }

    def _generate_analytics(self, servers: list[MCPServerRecord]) -> dict[str, Any]:
        """Generate analytics from harvested data."""
        analytics = {
            "total_servers": len(servers),
            "by_source": {},
            "by_category": {},
            "by_owner": {},
            "quality_metrics": {
                "has_documentation": 0,
                "is_official": 0,
                "has_stars": 0,
                "has_npm_package": 0,
            },
            "top_repositories": [],
            "recent_updates": [],
        }

        # Analyze by source
        for server in servers:
            source = server.source
            analytics["by_source"][source] = analytics["by_source"].get(source, 0) + 1

            # Analyze by category
            category = server.category or "unknown"
            analytics["by_category"][category] = (
                analytics["by_category"].get(category, 0) + 1
            )

            # Analyze by owner
            if server.repository_owner:
                owner = server.repository_owner
                analytics["by_owner"][owner] = analytics["by_owner"].get(owner, 0) + 1

            # Quality metrics
            if server.has_documentation:
                analytics["quality_metrics"]["has_documentation"] += 1
            if server.is_official:
                analytics["quality_metrics"]["is_official"] += 1
            if server.stars and server.stars > 0:
                analytics["quality_metrics"]["has_stars"] += 1
            if server.npm_package:
                analytics["quality_metrics"]["has_npm_package"] += 1

        # Top repositories by stars
        starred_servers = [s for s in servers if s.stars and s.stars > 0]
        starred_servers.sort(key=lambda x: x.stars, reverse=True)
        analytics["top_repositories"] = [
            {"name": s.name, "stars": s.stars, "repository_url": s.repository_url}
            for s in starred_servers[:20]
        ]

        # Recent updates
        recent_servers = [s for s in servers if s.last_updated]
        recent_servers.sort(key=lambda x: x.last_updated, reverse=True)
        analytics["recent_updates"] = [
            {
                "name": s.name,
                "last_updated": s.last_updated,
                "repository_url": s.repository_url,
            }
            for s in recent_servers[:20]
        ]

        return analytics


async def main():
    """Run production MCP harvest."""
    import os

    # Get GitHub token from environment
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        pass

    # Create harvester
    harvester = ProductionMCPHarvester(github_token=github_token)

    # Run harvest
    results = await harvester.harvest_all()

    # Print summary

    results["analytics"]

    for _file_type, _path in results["files"].items():
        pass


if __name__ == "__main__":
    asyncio.run(main())
