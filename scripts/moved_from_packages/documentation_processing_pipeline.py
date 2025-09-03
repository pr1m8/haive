#!/usr/bin/env python3
"""Documentation Processing Pipeline.

Processes discovered MCP servers to extract README content and convert to
the same format as our original all_mcp_documents.json database.

Usage:
    poetry run python examples/documentation_processing_pipeline.py
"""

import asyncio
import base64
import json
import logging
import os
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import aiohttp

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DocumentationProcessor:
    """Processes MCP servers to extract and format documentation."""

    def __init__(self, max_servers: int = 100):
        self.max_servers = max_servers
        self.session: aiohttp.ClientSession | None = None
        self.github_token = os.environ.get("GITHUB_TOKEN")

        # Setup directories
        self.data_dir = Path(__file__).parent.parent / "data"
        self.servers_dir = self.data_dir / "mcp_servers"
        self.processed_docs = []

        # GitHub API base
        self.api_base = "https://api.github.com"

    def _get_headers(self) -> dict[str, str]:
        """Get GitHub API headers."""
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"
        return headers

    async def process_all_servers(self) -> dict[str, Any]:
        """Process all discovered servers and extract documentation."""
        logger.info("🚀 Starting Documentation Processing Pipeline")

        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30)
        ) as session:
            self.session = session

            # 1. Load discovered servers
            servers = self._load_production_servers()
            logger.info(f"📦 Loaded {len(servers)} discovered servers")

            # 2. Select servers for processing
            selected_servers = self._select_servers_for_processing(servers)
            logger.info(
                f"🎯 Selected {len(selected_servers)} servers for documentation processing"
            )

            # 3. Extract documentation
            documented_servers = await self._extract_all_documentation(selected_servers)
            logger.info(
                f"📚 Extracted documentation for {len(documented_servers)} servers"
            )

            # 4. Convert to standard format
            formatted_docs = self._convert_to_standard_format(documented_servers)

            # 5. Save results
            results = await self._save_documentation_database(formatted_docs)

        logger.info("✅ Documentation Processing Pipeline Complete!")
        return results

    def _load_production_servers(self) -> list[dict[str, Any]]:
        """Load servers from production database."""
        db_file = self.servers_dir / "production_mcp_database.json"

        if not db_file.exists():
            logger.warning("No production database found, using empty list")
            return []

        with open(db_file) as f:
            data = json.load(f)
            servers = list(data.get("servers", {}).values())

        return servers

    def _select_servers_for_processing(
        self, servers: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Select servers for documentation processing based on quality."""

        # Filter and score servers
        def score_server(server: dict[str, Any]) -> float:
            score = 0.0

            # Must have repository URL
            if not server.get("repository_url"):
                return -1.0

            # High priority for starred repositories
            stars = server.get("stars", 0) or 0
            if stars > 100:
                score += 10.0
            elif stars > 10:
                score += 5.0
            elif stars > 0:
                score += 2.0

            # High priority for official servers
            if server.get("is_official", False):
                score += 15.0

            # Priority for documented servers
            if server.get("has_documentation", False):
                score += 5.0

            # Priority for certain categories
            category = server.get("category", "").lower()
            high_value_categories = [
                "ai_ml",
                "database",
                "api_integration",
                "search",
                "cloud",
                "version_control",
            ]
            if category in high_value_categories:
                score += 3.0

            # Priority for recent updates
            last_updated = server.get("last_updated")
            if last_updated:
                try:
                    update_date = datetime.fromisoformat(
                        last_updated.replace("Z", "+00:00")
                    )
                    days_old = (datetime.now(UTC) - update_date).days
                    if days_old < 30:
                        score += 2.0
                    elif days_old < 90:
                        score += 1.0
                except:
                    pass

            # Penalty for utility category (often simple)
            if category == "utility":
                score -= 1.0

            return score

        # Score and filter servers
        valid_servers = []
        for server in servers:
            score = score_server(server)
            if score >= 0:  # Only include servers with valid repository URLs
                valid_servers.append((server, score))

        # Sort by score and take top servers
        valid_servers.sort(key=lambda x: x[1], reverse=True)
        selected = [server for server, score in valid_servers[: self.max_servers]]

        logger.info("🎯 Top server scores:")
        for i, (server, score) in enumerate(valid_servers[:10]):
            logger.info(
                f"   {i + 1}. {server.get('name', 'Unknown')} (score: {score:.1f})"
            )

        return selected

    async def _extract_all_documentation(
        self, servers: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Extract documentation for all selected servers."""
        documented_servers = []

        for i, server in enumerate(servers):
            server_name = server.get("name", "Unknown")
            logger.info(f"📚 Processing {i + 1}/{len(servers)}: {server_name}")

            try:
                # Extract GitHub info
                repo_url = server.get("repository_url", "")
                github_info = self._extract_github_info(repo_url)

                if not github_info:
                    logger.warning(f"Skipping {server_name}: Not a GitHub repository")
                    continue

                # Get repository documentation
                documentation = await self._get_repository_documentation(
                    github_info["owner"], github_info["repo"]
                )

                if documentation:
                    documented_server = {
                        **server,
                        "documentation": documentation,
                        "github_info": github_info,
                        "processed_at": datetime.now(UTC).isoformat(),
                    }
                    documented_servers.append(documented_server)
                    logger.info(f"✅ Extracted documentation for {server_name}")
                else:
                    logger.warning(f"⚠️  No documentation found for {server_name}")

                # Rate limiting delay
                await asyncio.sleep(0.5)

            except Exception as e:
                logger.exception(f"❌ Failed to process {server_name}: {e}")
                continue

        return documented_servers

    def _extract_github_info(self, repo_url: str) -> dict[str, str] | None:
        """Extract owner and repo from GitHub URL."""
        if not repo_url or "github.com" not in repo_url:
            return None

        # Handle different GitHub URL formats
        patterns = [
            r"github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$",
            r"github\.com/([^/]+)/([^/]+)/tree/[^/]+/(.+)",
            r"github\.com/([^/]+)/([^/]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, repo_url)
            if match:
                owner, repo = match.groups()[:2]
                # Clean repo name
                repo = (
                    repo.replace(".git", "").split("/")[0].split("?")[0].split("#")[0]
                )
                return {
                    "owner": owner,
                    "repo": repo,
                    "full_name": f"{owner}/{repo}",
                    "url": f"https://github.com/{owner}/{repo}",
                }

        return None

    async def _get_repository_documentation(self, owner: str, repo: str) -> str | None:
        """Get documentation from GitHub repository."""
        try:
            # Try to get README
            readme_content = await self._get_readme_content(owner, repo)
            if readme_content:
                return readme_content

            # If no README, try to get repository description
            repo_info = await self._get_repository_info(owner, repo)
            if repo_info and repo_info.get("description"):
                return f"# {repo}\n\n{repo_info['description']}"

            return None

        except Exception as e:
            logger.exception(f"Failed to get documentation for {owner}/{repo}: {e}")
            return None

    async def _get_readme_content(self, owner: str, repo: str) -> str | None:
        """Get README content from GitHub API."""
        url = f"{self.api_base}/repos/{owner}/{repo}/readme"

        try:
            async with self.session.get(url, headers=self._get_headers()) as response:
                if response.status == 200:
                    data = await response.json()
                    # Decode base64 content
                    content = base64.b64decode(data["content"]).decode("utf-8")
                    return content
                if response.status == 404:
                    logger.debug(f"No README found for {owner}/{repo}")
                    return None
                logger.warning(
                    f"Failed to get README for {owner}/{repo}: {response.status}"
                )
                return None
        except Exception as e:
            logger.exception(f"Error getting README for {owner}/{repo}: {e}")
            return None

    async def _get_repository_info(
        self, owner: str, repo: str
    ) -> dict[str, Any] | None:
        """Get repository information from GitHub API."""
        url = f"{self.api_base}/repos/{owner}/{repo}"

        try:
            async with self.session.get(url, headers=self._get_headers()) as response:
                if response.status == 200:
                    return await response.json()
                logger.warning(
                    f"Failed to get repo info for {owner}/{repo}: {response.status}"
                )
                return None
        except Exception as e:
            logger.exception(f"Error getting repo info for {owner}/{repo}: {e}")
            return None

    def _convert_to_standard_format(
        self, documented_servers: list[dict[str, Any]]
    ) -> dict[str, dict[str, Any]]:
        """Convert to the same format as all_mcp_documents.json."""
        formatted_docs = {}

        for server in documented_servers:
            # Create unique key (similar to original format)
            key = server.get("name", "").replace("/", "_").replace(" ", "_")
            if not key:
                key = server.get("repository_url", "").split("/")[-1]

            # Ensure unique key
            original_key = key
            counter = 1
            while key in formatted_docs:
                key = f"{original_key}_{counter}"
                counter += 1

            # Format similar to original all_mcp_documents.json
            formatted_docs[key] = {
                "name": server.get("name", ""),
                "description": server.get("description", ""),
                "repository": server.get("repository_url", ""),
                "category": server.get("category", ""),
                "source": server.get("source", ""),
                "documentation": server.get("documentation", ""),
                "github_info": server.get("github_info", {}),
                "metadata": {
                    "stars": server.get("stars"),
                    "last_updated": server.get("last_updated"),
                    "is_official": server.get("is_official", False),
                    "has_documentation": server.get("has_documentation", False),
                    "npm_package": server.get("npm_package"),
                    "install_command": server.get("install_command"),
                    "setup_instructions": server.get("setup_instructions"),
                    "transport_types": server.get("transport_types", []),
                    "capabilities": server.get("capabilities", []),
                    "dependencies": server.get("dependencies", []),
                    "source_metadata": server.get("source_metadata", {}),
                    "processed_at": server.get("processed_at"),
                },
            }

        return formatted_docs

    async def _save_documentation_database(
        self, formatted_docs: dict[str, dict[str, Any]]
    ) -> dict[str, Any]:
        """Save documentation database in standard format."""
        timestamp = datetime.now(UTC).isoformat()

        # Create the database in the same format as all_mcp_documents.json
        database = {
            "metadata": {
                "last_updated": timestamp,
                "total_servers": len(formatted_docs),
                "processing_method": "documentation_processing_pipeline",
                "source": "production_mcp_database",
            },
            "servers": formatted_docs,
        }

        # Save as new all_mcp_documents.json (backup original if exists)
        main_docs_file = self.servers_dir / "all_mcp_documents.json"
        if main_docs_file.exists():
            backup_file = (
                self.servers_dir
                / f"all_mcp_documents_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            main_docs_file.rename(backup_file)
            logger.info(f"📦 Backed up original to {backup_file}")

        # Save new documentation database
        with open(main_docs_file, "w") as f:
            json.dump(database, f, indent=2)

        # Also save timestamped version
        timestamped_file = (
            self.servers_dir
            / f"processed_mcp_documents_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(timestamped_file, "w") as f:
            json.dump(database, f, indent=2)

        # Create summary report
        categories = {}
        sources = {}
        with_docs = 0

        for server_data in formatted_docs.values():
            # Count categories
            category = server_data.get("category", "unknown")
            categories[category] = categories.get(category, 0) + 1

            # Count sources
            source = server_data.get("source", "unknown")
            sources[source] = sources.get(source, 0) + 1

            # Count documented
            if server_data.get("documentation"):
                with_docs += 1

        results = {
            "timestamp": timestamp,
            "summary": {
                "total_servers": len(formatted_docs),
                "servers_with_documentation": with_docs,
                "documentation_rate": (
                    (with_docs / len(formatted_docs) * 100) if formatted_docs else 0
                ),
                "categories": len(categories),
                "sources": len(sources),
            },
            "by_category": categories,
            "by_source": sources,
            "files": {
                "main_database": str(main_docs_file),
                "timestamped_backup": str(timestamped_file),
            },
        }

        # Save processing report
        report_file = self.servers_dir / "documentation_processing_report.json"
        with open(report_file, "w") as f:
            json.dump(results, f, indent=2)

        logger.info(f"📄 Saved main database to {main_docs_file}")
        logger.info(f"📄 Saved timestamped version to {timestamped_file}")
        logger.info(f"📄 Saved processing report to {report_file}")

        return results


async def main():
    """Run the documentation processing pipeline."""
    # Create processor with configurable max servers
    max_servers = int(os.environ.get("MAX_SERVERS", "100"))
    processor = DocumentationProcessor(max_servers=max_servers)

    # Check GitHub token
    if not processor.github_token:
        pass

    # Run processing pipeline
    results = await processor.process_all_servers()

    # Print summary

    for _category, _count in sorted(
        results["by_category"].items(), key=lambda x: x[1], reverse=True
    )[:10]:
        pass

    for _source, _count in sorted(
        results["by_source"].items(), key=lambda x: x[1], reverse=True
    )[:5]:
        pass

    for _file_type, _path in results["files"].items():
        pass


if __name__ == "__main__":
    asyncio.run(main())
