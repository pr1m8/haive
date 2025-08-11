#!/usr/bin/env python3
"""Background MCP Server Processing Service.

A continuous background service that discovers, downloads, processes, and organizes
MCP servers with comprehensive documentation, categorization, and quality assessment.

This service runs in the background and can be monitored through log files and status
endpoints. It preserves metadata, categorizes servers, generates Sphinx documentation,
and maintains quality rankings.

Usage:
    # Run in background with nohup
    nohup poetry run python examples/background_mcp_processor.py > logs/processor.log 2>&1 &

    # Monitor progress
    tail -f logs/processor.log

    # Check status
    cat data/mcp_servers/processing_status.json

Classes:
    BackgroundMCPProcessor: Main background processing service
    ServerQualityAssessor: Quality assessment and ranking system
    DocumentationGenerator: Sphinx documentation generation
    CategoryOrganizer: Smart categorization and organization

Examples:
    Basic usage::

        from background_mcp_processor import BackgroundMCPProcessor

        # Start background processor
        processor = BackgroundMCPProcessor(
            batch_size=10,
            sleep_interval=300,  # 5 minutes
            max_servers=1000
        )

        # Run continuously
        await processor.run_continuous()

    Monitor progress::

        # Check processing status
        status = processor.get_status()
        print(f"Processed: {status['total_processed']}")
        print(f"Success rate: {status['success_rate']:.1f}%")

        # Get quality rankings
        rankings = processor.get_quality_rankings()
        for server in rankings[:10]:
            print(f"{server['name']}: {server['quality_score']:.2f}")

Note:
    The processor automatically handles rate limiting, error recovery, and maintains
    comprehensive logs for monitoring and debugging.
"""

import asyncio
import json
import logging
import signal
import sys
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime

# Configure logging with rotation
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

import aiohttp

# Set up comprehensive logging
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_formatter)

# File handler with rotation
file_handler = RotatingFileHandler(
    log_dir / "background_processor.log",
    maxBytes=10 * 1024 * 1024,  # 10MB
    backupCount=5,
)
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
)
file_handler.setFormatter(file_formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


@dataclass
class ServerQualityMetrics:
    """Comprehensive quality metrics for MCP servers.

    Attributes:
        name: Server name
        repository_url: GitHub repository URL
        quality_score: Overall quality score (0-100)
        documentation_score: Documentation quality score (0-100)
        popularity_score: Popularity score based on stars, forks (0-100)
        maintenance_score: Maintenance score based on recent activity (0-100)
        completeness_score: Completeness score based on metadata (0-100)
        category: Primary category
        subcategories: Additional categorizations
        tags: Relevant tags
        install_method: Primary installation method
        setup_complexity: Setup complexity rating (1-5)
        error_count: Number of processing errors encountered
        last_updated: Last update timestamp
        processing_time: Time taken to process

    Example:
        Creating quality metrics::

            metrics = ServerQualityMetrics(
                name="server-filesystem",
                repository_url="https://github.com/modelcontextprotocol/servers",
                quality_score=95.5,
                documentation_score=98.0,
                popularity_score=87.0,
                maintenance_score=100.0,
                completeness_score=92.0,
                category="filesystem",
                subcategories=["file_operations", "security"],
                tags=["official", "secure", "configurable"],
                install_method="npm",
                setup_complexity=2,
                error_count=0,
                last_updated="2025-07-03T12:00:00Z",
                processing_time=15.5
            )
    """

    name: str
    repository_url: str
    quality_score: float
    documentation_score: float
    popularity_score: float
    maintenance_score: float
    completeness_score: float
    category: str
    subcategories: list[str]
    tags: list[str]
    install_method: str
    setup_complexity: int
    error_count: int
    last_updated: str
    processing_time: float

    def __post_init__(self):
        if self.subcategories is None:
            self.subcategories = []
        if self.tags is None:
            self.tags = []

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


class ServerQualityAssessor:
    """Advanced quality assessment system for MCP servers.

    Provides comprehensive quality scoring based on multiple factors including
    documentation quality, popularity metrics, maintenance activity, and
    completeness of metadata.

    Methods:
        assess_server: Perform comprehensive quality assessment
        calculate_documentation_score: Assess documentation quality
        calculate_popularity_score: Assess popularity metrics
        calculate_maintenance_score: Assess maintenance activity
        calculate_completeness_score: Assess metadata completeness

    Example:
        Assessing server quality::

            assessor = ServerQualityAssessor()
            metrics = await assessor.assess_server(server_data)
            print(f"Quality Score: {metrics.quality_score:.1f}")
            print(f"Category: {metrics.category}")
            print(f"Install Method: {metrics.install_method}")
    """

    def __init__(self):
        """Initialize the quality assessor."""
        self.github_token = None

    async def assess_server(
        self, server_data: dict[str, Any], session: aiohttp.ClientSession
    ) -> ServerQualityMetrics:
        """Perform comprehensive quality assessment of an MCP server.

        Args:
            server_data: Server data dictionary
            session: HTTP session for API calls

        Returns:
            ServerQualityMetrics: Comprehensive quality assessment

        Raises:
            ValueError: If server data is incomplete

        Example:
            Assessing a server::

                async with aiohttp.ClientSession() as session:
                    metrics = await assessor.assess_server(server_data, session)
                    if metrics.quality_score > 80:
                        print(f"High quality server: {metrics.name}")
        """
        start_time = time.time()

        try:
            # Extract basic info
            name = server_data.get("name", "Unknown")
            repo_url = server_data.get("repository_url", "")

            # Calculate individual scores
            doc_score = self._calculate_documentation_score(server_data)
            pop_score = await self._calculate_popularity_score(server_data, session)
            maint_score = self._calculate_maintenance_score(server_data)
            comp_score = self._calculate_completeness_score(server_data)

            # Calculate overall quality score (weighted average)
            quality_score = (
                doc_score * 0.35
                + pop_score * 0.25
                + maint_score * 0.25
                + comp_score * 0.15
            )

            # Determine category and subcategories
            category, subcategories = self._categorize_server(server_data)

            # Extract tags
            tags = self._extract_tags(server_data)

            # Determine installation method
            install_method = self._determine_install_method(server_data)

            # Assess setup complexity
            setup_complexity = self._assess_setup_complexity(server_data)

            processing_time = time.time() - start_time

            metrics = ServerQualityMetrics(
                name=name,
                repository_url=repo_url,
                quality_score=quality_score,
                documentation_score=doc_score,
                popularity_score=pop_score,
                maintenance_score=maint_score,
                completeness_score=comp_score,
                category=category,
                subcategories=subcategories,
                tags=tags,
                install_method=install_method,
                setup_complexity=setup_complexity,
                error_count=0,
                last_updated=datetime.now(UTC).isoformat(),
                processing_time=processing_time,
            )

            logger.debug(
                f"Assessed {name}: quality={quality_score:.1f}, "
                f"category={category}, method={install_method}"
            )

            return metrics

        except Exception as e:
            logger.exception(f"Error assessing server {name}: {e}")
            return ServerQualityMetrics(
                name=name,
                repository_url=repo_url,
                quality_score=0.0,
                documentation_score=0.0,
                popularity_score=0.0,
                maintenance_score=0.0,
                completeness_score=0.0,
                category="unknown",
                subcategories=[],
                tags=["error"],
                install_method="unknown",
                setup_complexity=5,
                error_count=1,
                last_updated=datetime.now(UTC).isoformat(),
                processing_time=time.time() - start_time,
            )

    def _calculate_documentation_score(self, server_data: dict[str, Any]) -> float:
        """Calculate documentation quality score (0-100).

        Args:
            server_data: Server data dictionary

        Returns:
            Documentation quality score
        """
        score = 0.0

        # Check for documentation presence
        doc = server_data.get("documentation", "")
        description = server_data.get("description", "")

        if doc:
            score += 40.0  # Base score for having documentation

            # Length-based scoring
            doc_length = len(doc)
            if doc_length > 5000:
                score += 20.0
            elif doc_length > 2000:
                score += 15.0
            elif doc_length > 500:
                score += 10.0

            # Content quality indicators
            doc_lower = doc.lower()

            # Installation instructions
            if any(
                keyword in doc_lower
                for keyword in ["install", "setup", "npm install", "pip install"]
            ):
                score += 10.0

            # Usage examples
            if any(
                keyword in doc_lower
                for keyword in ["example", "usage", "```", "how to"]
            ):
                score += 10.0

            # Configuration documentation
            if any(
                keyword in doc_lower
                for keyword in ["config", "configure", "environment"]
            ):
                score += 5.0

            # API documentation
            if any(
                keyword in doc_lower
                for keyword in ["api", "methods", "functions", "tools"]
            ):
                score += 5.0

        # Description quality
        if description:
            if len(description) > 100:
                score += 5.0
            if len(description) > 50:
                score += 5.0

        return min(score, 100.0)

    async def _calculate_popularity_score(
        self, server_data: dict[str, Any], session: aiohttp.ClientSession
    ) -> float:
        """Calculate popularity score based on GitHub metrics.

        Args:
            server_data: Server data dictionary
            session: HTTP session for API calls

        Returns:
            Popularity score (0-100)
        """
        score = 0.0

        # Stars-based scoring
        stars = server_data.get("stars", 0) or 0
        if stars > 1000:
            score += 50.0
        elif stars > 100:
            score += 40.0
        elif stars > 50:
            score += 30.0
        elif stars > 10:
            score += 20.0
        elif stars > 0:
            score += 10.0

        # Official status
        if server_data.get("is_official", False):
            score += 25.0

        # Source reputation
        source = server_data.get("source", "")
        if "modelcontextprotocol" in source:
            score += 20.0
        elif any(org in source for org in ["docker", "microsoft", "google"]):
            score += 15.0

        # Recent activity
        last_updated = server_data.get("last_updated")
        if last_updated:
            try:
                update_date = datetime.fromisoformat(
                    last_updated.replace("Z", "+00:00")
                )
                days_old = (datetime.now(UTC) - update_date).days
                if days_old < 30:
                    score += 5.0
                elif days_old < 90:
                    score += 3.0
            except:
                pass

        return min(score, 100.0)

    def _calculate_maintenance_score(self, server_data: dict[str, Any]) -> float:
        """Calculate maintenance score based on activity indicators.

        Args:
            server_data: Server data dictionary

        Returns:
            Maintenance score (0-100)
        """
        score = 50.0  # Base score

        # Recent updates
        last_updated = server_data.get("last_updated")
        if last_updated:
            try:
                update_date = datetime.fromisoformat(
                    last_updated.replace("Z", "+00:00")
                )
                days_old = (datetime.now(UTC) - update_date).days

                if days_old < 7:
                    score += 50.0
                elif days_old < 30:
                    score += 30.0
                elif days_old < 90:
                    score += 10.0
                elif days_old > 365:
                    score -= 30.0
                elif days_old > 180:
                    score -= 15.0
            except:
                score -= 10.0

        # Version indicators in documentation
        doc = server_data.get("documentation", "")
        if doc and any(
            keyword in doc.lower() for keyword in ["version", "v1.", "v2.", "changelog"]
        ):
            score += 10.0

        return max(min(score, 100.0), 0.0)

    def _calculate_completeness_score(self, server_data: dict[str, Any]) -> float:
        """Calculate metadata completeness score.

        Args:
            server_data: Server data dictionary

        Returns:
            Completeness score (0-100)
        """
        score = 0.0
        total_fields = 0
        present_fields = 0

        # Required fields
        required_fields = [
            "name",
            "repository_url",
            "description",
            "category",
            "documentation",
            "source",
        ]

        for field in required_fields:
            total_fields += 1
            if server_data.get(field):
                present_fields += 1
                score += 15.0

        # Optional but valuable fields
        optional_fields = [
            "install_command",
            "setup_instructions",
            "npm_package",
            "transport_types",
            "capabilities",
            "dependencies",
        ]

        for field in optional_fields:
            total_fields += 1
            value = (
                server_data.get("metadata", {}).get(field)
                if "metadata" in server_data
                else server_data.get(field)
            )
            if value:
                present_fields += 1
                score += 5.0

        return min(score, 100.0)

    def _categorize_server(self, server_data: dict[str, Any]) -> tuple[str, list[str]]:
        """Intelligently categorize server and identify subcategories.

        Args:
            server_data: Server data dictionary

        Returns:
            Tuple of (primary_category, subcategories)
        """
        name = server_data.get("name", "").lower()
        description = server_data.get("description", "").lower()
        doc = server_data.get("documentation", "").lower()

        text = f"{name} {description} {doc}"

        # Enhanced categorization
        categories = {
            "ai_ml": {
                "keywords": [
                    "ai",
                    "ml",
                    "machine learning",
                    "artificial intelligence",
                    "llm",
                    "gpt",
                    "model",
                    "embedding",
                    "vector",
                    "semantic",
                ],
                "subcategories": [
                    "language_models",
                    "embeddings",
                    "vector_search",
                    "semantic_search",
                ],
            },
            "database": {
                "keywords": [
                    "database",
                    "sql",
                    "postgres",
                    "mysql",
                    "sqlite",
                    "mongo",
                    "redis",
                    "db",
                    "query",
                    "schema",
                ],
                "subcategories": ["relational", "nosql", "cache", "analytics"],
            },
            "filesystem": {
                "keywords": [
                    "file",
                    "filesystem",
                    "directory",
                    "folder",
                    "path",
                    "storage",
                    "disk",
                ],
                "subcategories": ["file_operations", "storage", "backup"],
            },
            "api_integration": {
                "keywords": [
                    "api",
                    "rest",
                    "graphql",
                    "webhook",
                    "http",
                    "endpoint",
                    "service",
                    "integration",
                ],
                "subcategories": ["rest_api", "webhooks", "microservices"],
            },
            "version_control": {
                "keywords": [
                    "git",
                    "github",
                    "gitlab",
                    "version",
                    "commit",
                    "repository",
                    "repo",
                ],
                "subcategories": ["git_operations", "collaboration", "code_review"],
            },
            "communication": {
                "keywords": [
                    "slack",
                    "discord",
                    "teams",
                    "chat",
                    "message",
                    "notification",
                    "email",
                ],
                "subcategories": ["messaging", "notifications", "collaboration"],
            },
            "cloud": {
                "keywords": [
                    "aws",
                    "azure",
                    "gcp",
                    "cloud",
                    "docker",
                    "kubernetes",
                    "container",
                ],
                "subcategories": ["infrastructure", "containers", "serverless"],
            },
            "search": {
                "keywords": ["search", "elastic", "solr", "index", "query", "find"],
                "subcategories": ["full_text", "elasticsearch", "indexing"],
            },
            "security": {
                "keywords": [
                    "auth",
                    "security",
                    "vault",
                    "secret",
                    "token",
                    "encryption",
                    "ssl",
                ],
                "subcategories": ["authentication", "encryption", "secrets_management"],
            },
            "productivity": {
                "keywords": [
                    "notion",
                    "calendar",
                    "task",
                    "todo",
                    "project",
                    "management",
                ],
                "subcategories": [
                    "task_management",
                    "project_management",
                    "scheduling",
                ],
            },
            "finance": {
                "keywords": [
                    "payment",
                    "stripe",
                    "paypal",
                    "finance",
                    "crypto",
                    "billing",
                ],
                "subcategories": ["payments", "cryptocurrency", "billing"],
            },
            "media": {
                "keywords": ["image", "video", "audio", "media", "photo", "stream"],
                "subcategories": ["image_processing", "video_processing", "streaming"],
            },
            "monitoring": {
                "keywords": [
                    "monitor",
                    "log",
                    "metric",
                    "alert",
                    "health",
                    "observability",
                ],
                "subcategories": ["logging", "metrics", "alerting"],
            },
        }

        # Find primary category
        primary_category = "utility"
        category_scores = {}

        for category, config in categories.items():
            score = sum(1 for keyword in config["keywords"] if keyword in text)
            if score > 0:
                category_scores[category] = score

        if category_scores:
            primary_category = max(category_scores, key=category_scores.get)

        # Find subcategories
        subcategories = []
        if primary_category in categories:
            for subcat in categories[primary_category]["subcategories"]:
                subcat_keywords = subcat.replace("_", " ").split()
                if any(keyword in text for keyword in subcat_keywords):
                    subcategories.append(subcat)

        return primary_category, subcategories

    def _extract_tags(self, server_data: dict[str, Any]) -> list[str]:
        """Extract relevant tags from server data.

        Args:
            server_data: Server data dictionary

        Returns:
            List of relevant tags
        """
        tags = []

        # Official status
        if server_data.get("is_official", False):
            tags.append("official")

        # Quality indicators
        stars = server_data.get("stars", 0) or 0
        if stars > 100:
            tags.append("popular")
        if stars > 1000:
            tags.append("trending")

        # Documentation quality
        doc = server_data.get("documentation", "")
        if doc and len(doc) > 2000:
            tags.append("well_documented")

        # Installation method
        metadata = server_data.get("metadata", {})
        if metadata.get("npm_package"):
            tags.append("npm")
        if metadata.get("install_command"):
            if "pip" in metadata["install_command"]:
                tags.append("python")
            if "npm" in metadata["install_command"]:
                tags.append("nodejs")

        # Recent activity
        last_updated = server_data.get("last_updated")
        if last_updated:
            try:
                update_date = datetime.fromisoformat(
                    last_updated.replace("Z", "+00:00")
                )
                days_old = (datetime.now(UTC) - update_date).days
                if days_old < 30:
                    tags.append("recently_updated")
            except:
                pass

        # Transport types
        transport_types = metadata.get("transport_types", [])
        if transport_types:
            tags.extend([f"transport_{t}" for t in transport_types])

        return list(set(tags))  # Remove duplicates

    def _determine_install_method(self, server_data: dict[str, Any]) -> str:
        """Determine the primary installation method.

        Args:
            server_data: Server data dictionary

        Returns:
            Primary installation method
        """
        metadata = server_data.get("metadata", {})
        install_cmd = metadata.get("install_command", "")
        npm_package = metadata.get("npm_package")

        if npm_package or "npm install" in install_cmd:
            return "npm"
        if "pip install" in install_cmd:
            return "pip"
        if "docker" in install_cmd.lower():
            return "docker"
        if "git clone" in install_cmd.lower():
            return "source"
        if "cargo install" in install_cmd:
            return "cargo"
        if "go install" in install_cmd:
            return "go"
        return "manual"

    def _assess_setup_complexity(self, server_data: dict[str, Any]) -> int:
        """Assess setup complexity on a scale of 1-5.

        Args:
            server_data: Server data dictionary

        Returns:
            Setup complexity rating (1=simple, 5=complex)
        """
        complexity = 3  # Default medium complexity

        metadata = server_data.get("metadata", {})
        install_cmd = metadata.get("install_command", "")
        setup_instructions = metadata.get("setup_instructions", "")
        dependencies = metadata.get("dependencies", [])

        # Simple indicators
        if install_cmd and (
            "npm install" in install_cmd or "pip install" in install_cmd
        ):
            complexity -= 1

        # Complex indicators
        if len(dependencies) > 5:
            complexity += 1
        if setup_instructions and len(setup_instructions) > 1000:
            complexity += 1
        if "docker" in install_cmd.lower():
            complexity += 1
        if not install_cmd:
            complexity += 1

        return max(1, min(complexity, 5))


class DocumentationGenerator:
    """Sphinx documentation generator for MCP servers.

    Generates comprehensive Sphinx documentation with Google-style docstrings,
    examples, and automated API documentation.

    Methods:
        generate_server_docs: Generate documentation for a single server
        generate_category_docs: Generate category overview documentation
        generate_master_index: Generate master documentation index

    Example:
        Generating documentation::

            generator = DocumentationGenerator()
            await generator.generate_server_docs(server_data, quality_metrics)
            await generator.generate_master_index(all_servers)
    """

    def __init__(self, docs_dir: Path):
        """Initialize documentation generator.

        Args:
            docs_dir: Directory for generated documentation
        """
        self.docs_dir = docs_dir
        self.docs_dir.mkdir(parents=True, exist_ok=True)

    async def generate_server_docs(
        self, server_data: dict[str, Any], metrics: ServerQualityMetrics
    ) -> Path:
        """Generate comprehensive documentation for a single server.

        Args:
            server_data: Server data dictionary
            metrics: Quality metrics for the server

        Returns:
            Path to generated documentation file

        Example:
            Generating server documentation::

                doc_path = await generator.generate_server_docs(
                    server_data, quality_metrics
                )
                print(f"Documentation generated: {doc_path}")
        """
        # Create server-specific directory
        server_name = metrics.name.replace("/", "_").replace(" ", "_")
        server_dir = self.docs_dir / "servers" / metrics.category / server_name
        server_dir.mkdir(parents=True, exist_ok=True)

        # Generate main documentation file
        doc_path = server_dir / "index.rst"

        doc_content = self._generate_server_rst(server_data, metrics)

        with open(doc_path, "w") as f:
            f.write(doc_content)

        # Generate examples file if available
        examples = self._extract_examples(server_data)
        if examples:
            examples_path = server_dir / "examples.rst"
            examples_content = self._generate_examples_rst(examples, metrics.name)
            with open(examples_path, "w") as f:
                f.write(examples_content)

        # Generate configuration file
        config_path = server_dir / "configuration.rst"
        config_content = self._generate_config_rst(server_data, metrics)
        with open(config_path, "w") as f:
            f.write(config_content)

        logger.debug(f"Generated documentation for {metrics.name} at {doc_path}")

        return doc_path

    def _generate_server_rst(
        self, server_data: dict[str, Any], metrics: ServerQualityMetrics
    ) -> str:
        """Generate RST content for server documentation.

        Args:
            server_data: Server data dictionary
            metrics: Quality metrics

        Returns:
            RST content string
        """
        name = metrics.name
        title_underline = "=" * len(name)

        # Quality badges
        quality_badge = self._get_quality_badge(metrics.quality_score)
        category_badge = f".. badge:: Category: {metrics.category}"

        # Installation section
        install_section = self._generate_install_section(server_data, metrics)

        # Features section
        features_section = self._generate_features_section(server_data)

        # API documentation
        api_section = self._generate_api_section(server_data)

        return f"""
{name}
{title_underline}

{quality_badge}
{category_badge}

.. contents:: Table of Contents
   :depth: 2
   :local:

Overview
--------

{server_data.get("description", "No description available.")}

**Quality Score:** {metrics.quality_score:.1f}/100

**Category:** {metrics.category}

**Installation Method:** {metrics.install_method}

**Setup Complexity:** {metrics.setup_complexity}/5

Repository
~~~~~~~~~~

**URL:** {metrics.repository_url}

**Source:** {server_data.get("source", "Unknown")}

**Last Updated:** {metrics.last_updated}

Quality Metrics
~~~~~~~~~~~~~~~

* **Documentation Score:** {metrics.documentation_score:.1f}/100
* **Popularity Score:** {metrics.popularity_score:.1f}/100
* **Maintenance Score:** {metrics.maintenance_score:.1f}/100
* **Completeness Score:** {metrics.completeness_score:.1f}/100

Tags
~~~~

{", ".join(f"``{tag}``" for tag in metrics.tags)}

{install_section}

{features_section}

{api_section}

Configuration
-------------

See :doc:`configuration` for detailed configuration options.

Examples
--------

See :doc:`examples` for usage examples and code samples.

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

For installation issues, check:

1. Ensure all dependencies are installed
2. Verify environment variables are set correctly
3. Check network connectivity for remote resources

See Also
--------

* :doc:`../index` - Category overview
* :doc:`../../index` - All MCP servers
* :doc:`configuration` - Configuration reference
* :doc:`examples` - Usage examples

.. note::
   This documentation was automatically generated from the MCP server metadata
   and repository information. For the most up-to-date information, please
   refer to the official repository.
""".strip()

    def _get_quality_badge(self, score: float) -> str:
        """Generate quality badge based on score.

        Args:
            score: Quality score (0-100)

        Returns:
            RST badge directive
        """
        if score >= 90:
            return ".. badge:: Quality: Excellent (90+)"
        if score >= 80:
            return ".. badge:: Quality: Good (80+)"
        if score >= 70:
            return ".. badge:: Quality: Fair (70+)"
        return ".. badge:: Quality: Needs Improvement (<70)"

    def _generate_install_section(
        self, server_data: dict[str, Any], metrics: ServerQualityMetrics
    ) -> str:
        """Generate installation section.

        Args:
            server_data: Server data dictionary
            metrics: Quality metrics

        Returns:
            RST installation section
        """
        metadata = server_data.get("metadata", {})
        install_cmd = metadata.get("install_command", "")
        setup_instructions = metadata.get("setup_instructions", "")

        section = """
Installation
------------

Quick Install
~~~~~~~~~~~~~
"""

        if install_cmd:
            section += f"""
.. code-block:: bash

   {install_cmd}
"""
        else:
            section += f"""
.. code-block:: bash

   # Installation method: {metrics.install_method}
   # Please refer to the repository for installation instructions
   git clone {metrics.repository_url}
"""

        if setup_instructions:
            section += f"""

Setup Instructions
~~~~~~~~~~~~~~~~~~

{setup_instructions}
"""

        # Dependencies
        dependencies = metadata.get("dependencies", [])
        if dependencies:
            section += f"""

Dependencies
~~~~~~~~~~~~

This server requires the following dependencies:

{chr(10).join(f"* ``{dep}``" for dep in dependencies)}
"""

        return section

    def _generate_features_section(self, server_data: dict[str, Any]) -> str:
        """Generate features section from documentation.

        Args:
            server_data: Server data dictionary

        Returns:
            RST features section
        """
        doc = server_data.get("documentation", "")
        metadata = server_data.get("metadata", {})

        section = """
Features
--------
"""

        # Extract capabilities
        capabilities = metadata.get("capabilities", [])
        if capabilities:
            section += f"""
Capabilities
~~~~~~~~~~~~

{chr(10).join(f"* {cap.replace('_', ' ').title()}" for cap in capabilities)}
"""

        # Transport types
        transport_types = metadata.get("transport_types", [])
        if transport_types:
            section += f"""

Transport Types
~~~~~~~~~~~~~~~

{chr(10).join(f"* ``{transport}``" for transport in transport_types)}
"""

        # Extract features from documentation
        if doc:
            features = self._extract_features_from_doc(doc)
            if features:
                section += f"""

Key Features
~~~~~~~~~~~~

{chr(10).join(f"* {feature}" for feature in features)}
"""

        return section

    def _extract_features_from_doc(self, doc: str) -> list[str]:
        """Extract feature list from documentation.

        Args:
            doc: Documentation text

        Returns:
            List of extracted features
        """
        features = []
        lines = doc.split("\n")

        in_features_section = False
        for line in lines:
            line = line.strip()

            # Look for features section
            if any(
                header in line.lower()
                for header in ["features", "capabilities", "what it does"]
            ):
                in_features_section = True
                continue

            # End of features section
            if in_features_section and line.startswith("#"):
                break

            # Extract bullet points
            if in_features_section and (line.startswith(("*", "-"))):
                feature = line.lstrip("*- ").strip()
                if feature and len(feature) > 10:  # Filter out short items
                    features.append(feature)

        return features[:10]  # Limit to 10 features

    def _generate_api_section(self, server_data: dict[str, Any]) -> str:
        """Generate API documentation section.

        Args:
            server_data: Server data dictionary

        Returns:
            RST API section
        """
        doc = server_data.get("documentation", "")

        section = """
API Reference
-------------
"""

        # Try to extract API information from documentation
        if doc:
            api_info = self._extract_api_info(doc)
            if api_info:
                section += api_info
            else:
                section += """
Please refer to the repository documentation for detailed API information.

.. code-block:: bash

   # For MCP servers, typical usage involves:
   # 1. Starting the server
   # 2. Connecting via MCP client
   # 3. Using available tools and resources
"""

        return section

    def _extract_api_info(self, doc: str) -> str:
        """Extract API information from documentation.

        Args:
            doc: Documentation text

        Returns:
            Formatted API information
        """
        # Look for code blocks and API examples
        api_blocks = []
        lines = doc.split("\n")

        in_code_block = False
        current_block = []
        code_type = None

        for line in lines:
            if line.strip().startswith("```"):
                if in_code_block:
                    # End of code block
                    if current_block and code_type:
                        api_blocks.append((code_type, "\n".join(current_block)))
                    current_block = []
                    in_code_block = False
                    code_type = None
                else:
                    # Start of code block
                    in_code_block = True
                    code_type = line.strip().replace("```", "").strip() or "text"
                continue

            if in_code_block:
                current_block.append(line)

        # Format API blocks
        if api_blocks:
            result = "Code Examples\n~~~~~~~~~~~~~\n\n"
            for code_type, code in api_blocks[:3]:  # Limit to 3 examples
                result += f".. code-block:: {code_type}\n\n"
                for line in code.split("\n"):
                    result += f"   {line}\n"
                result += "\n"
            return result

        return ""

    def _extract_examples(self, server_data: dict[str, Any]) -> list[dict[str, str]]:
        """Extract code examples from server documentation.

        Args:
            server_data: Server data dictionary

        Returns:
            List of example dictionaries
        """
        doc = server_data.get("documentation", "")
        examples = []

        if not doc:
            return examples

        # Extract examples from documentation
        lines = doc.split("\n")
        in_example_section = False
        in_code_block = False
        current_example = {"title": "", "code": "", "language": "bash"}

        for line in lines:
            line_lower = line.lower().strip()

            # Look for example sections
            if any(keyword in line_lower for keyword in ["example", "usage", "how to"]):
                if line.startswith("#"):
                    in_example_section = True
                    current_example["title"] = line.strip("# ").strip()
                    continue

            if in_example_section:
                if line.strip().startswith("```"):
                    if in_code_block:
                        # End of code block
                        if current_example["code"].strip():
                            examples.append(current_example.copy())
                        current_example = {"title": "", "code": "", "language": "bash"}
                        in_code_block = False
                    else:
                        # Start of code block
                        in_code_block = True
                        lang = line.strip().replace("```", "").strip()
                        if lang:
                            current_example["language"] = lang
                    continue

                if in_code_block:
                    current_example["code"] += line + "\n"

                # End of section
                if line.startswith("#") and not line_lower.startswith("###"):
                    in_example_section = False

        return examples[:5]  # Limit to 5 examples

    def _generate_examples_rst(
        self, examples: list[dict[str, str]], server_name: str
    ) -> str:
        """Generate examples RST file.

        Args:
            examples: List of example dictionaries
            server_name: Name of the server

        Returns:
            RST content for examples
        """
        title = f"Examples for {server_name}"
        title_underline = "=" * len(title)

        content = f"""
{title}
{title_underline}

This page contains usage examples for the {server_name} MCP server.

.. contents:: Table of Contents
   :depth: 2
   :local:

"""

        for i, example in enumerate(examples, 1):
            title = example.get("title", f"Example {i}")
            code = example.get("code", "").strip()
            language = example.get("language", "bash")

            content += f"""
{title}
{"-" * len(title)}

.. code-block:: {language}

"""
            for line in code.split("\n"):
                content += f"   {line}\n"
            content += "\n"

        return content.strip()

    def _generate_config_rst(
        self, server_data: dict[str, Any], metrics: ServerQualityMetrics
    ) -> str:
        """Generate configuration RST file.

        Args:
            server_data: Server data dictionary
            metrics: Quality metrics

        Returns:
            RST content for configuration
        """
        title = f"Configuration for {metrics.name}"
        title_underline = "=" * len(title)

        metadata = server_data.get("metadata", {})

        content = f"""
{title}
{title_underline}

This page contains configuration information for the {metrics.name} MCP server.

.. contents:: Table of Contents
   :depth: 2
   :local:

Basic Configuration
-------------------

**Installation Method:** {metrics.install_method}

**Setup Complexity:** {metrics.setup_complexity}/5

**Transport Types:** {", ".join(metadata.get("transport_types", ["stdio"]))}

Environment Variables
---------------------

.. note::
   Environment variables may be required for this server to function properly.
   Check the repository documentation for specific requirements.

"""

        # Add transport configuration
        transport_types = metadata.get("transport_types", ["stdio"])
        if transport_types:
            content += f"""
Transport Configuration
-----------------------

This server supports the following transport types:

{chr(10).join(f"* ``{transport}``" for transport in transport_types)}

For Claude Desktop configuration:

.. code-block:: json

   {{
     "mcpServers": {{
       "{metrics.name.replace("/", "_")}": {{
         "command": "npx",
         "args": ["{metrics.name}"]
       }}
     }}
   }}

"""

        return content.strip()


class CategoryOrganizer:
    """Smart categorization and organization system for MCP servers.

    Organizes servers by category, quality, and other criteria for easy
    discovery and documentation generation.

    Methods:
        organize_servers: Organize servers into categories
        generate_category_summaries: Generate category overview information
        create_quality_rankings: Create quality-based rankings

    Example:
        Organizing servers::

            organizer = CategoryOrganizer()
            organized = organizer.organize_servers(all_servers)
            rankings = organizer.create_quality_rankings(organized)
    """

    def __init__(self):
        """Initialize the category organizer."""

    def organize_servers(
        self, servers_with_metrics: list[tuple[dict[str, Any], ServerQualityMetrics]]
    ) -> dict[str, Any]:
        """Organize servers by various criteria.

        Args:
            servers_with_metrics: List of (server_data, metrics) tuples

        Returns:
            Organized server data structure

        Example:
            Organizing servers by category::

                organized = organizer.organize_servers(servers_data)
                print(f"Categories: {list(organized['by_category'].keys())}")
                print(f"Top quality: {organized['by_quality'][0]['name']}")
        """
        organized = {
            "by_category": {},
            "by_quality": [],
            "by_popularity": [],
            "by_install_method": {},
            "by_tags": {},
            "summary": {
                "total_servers": len(servers_with_metrics),
                "categories": set(),
                "install_methods": set(),
                "tags": set(),
                "average_quality": 0.0,
            },
        }

        total_quality = 0.0

        for server_data, metrics in servers_with_metrics:
            # By category
            category = metrics.category
            if category not in organized["by_category"]:
                organized["by_category"][category] = []
            organized["by_category"][category].append((server_data, metrics))
            organized["summary"]["categories"].add(category)

            # By install method
            install_method = metrics.install_method
            if install_method not in organized["by_install_method"]:
                organized["by_install_method"][install_method] = []
            organized["by_install_method"][install_method].append(
                (server_data, metrics)
            )
            organized["summary"]["install_methods"].add(install_method)

            # By tags
            for tag in metrics.tags:
                if tag not in organized["by_tags"]:
                    organized["by_tags"][tag] = []
                organized["by_tags"][tag].append((server_data, metrics))
                organized["summary"]["tags"].add(tag)

            # For quality and popularity rankings
            organized["by_quality"].append((server_data, metrics))
            organized["by_popularity"].append((server_data, metrics))

            total_quality += metrics.quality_score

        # Sort rankings
        organized["by_quality"].sort(key=lambda x: x[1].quality_score, reverse=True)
        organized["by_popularity"].sort(
            key=lambda x: x[1].popularity_score, reverse=True
        )

        # Sort categories by quality
        for category in organized["by_category"]:
            organized["by_category"][category].sort(
                key=lambda x: x[1].quality_score, reverse=True
            )

        # Calculate summary statistics
        organized["summary"]["categories"] = list(organized["summary"]["categories"])
        organized["summary"]["install_methods"] = list(
            organized["summary"]["install_methods"]
        )
        organized["summary"]["tags"] = list(organized["summary"]["tags"])
        if servers_with_metrics:
            organized["summary"]["average_quality"] = total_quality / len(
                servers_with_metrics
            )

        logger.info(
            f"Organized {len(servers_with_metrics)} servers into "
            f"{len(organized['summary']['categories'])} categories"
        )

        return organized

    def generate_category_summaries(
        self, organized_data: dict[str, Any]
    ) -> dict[str, dict[str, Any]]:
        """Generate summary information for each category.

        Args:
            organized_data: Organized server data

        Returns:
            Category summaries with statistics and top servers
        """
        summaries = {}

        for category, servers in organized_data["by_category"].items():
            if not servers:
                continue

            metrics_list = [metrics for _, metrics in servers]

            summary = {
                "name": category,
                "total_servers": len(servers),
                "average_quality": sum(m.quality_score for m in metrics_list)
                / len(metrics_list),
                "average_documentation": sum(
                    m.documentation_score for m in metrics_list
                )
                / len(metrics_list),
                "average_popularity": sum(m.popularity_score for m in metrics_list)
                / len(metrics_list),
                "top_servers": [
                    {"server": server, "metrics": metrics.to_dict()}
                    for server, metrics in servers[:5]
                ],  # Top 5 by quality
                "install_methods": list({m.install_method for m in metrics_list}),
                "common_tags": self._get_common_tags([m.tags for m in metrics_list]),
                "complexity_distribution": self._get_complexity_distribution(
                    metrics_list
                ),
            }

            summaries[category] = summary

        return summaries

    def _get_common_tags(self, tag_lists: list[list[str]]) -> list[str]:
        """Get most common tags across servers.

        Args:
            tag_lists: List of tag lists

        Returns:
            Most common tags
        """
        tag_counts = {}
        for tags in tag_lists:
            for tag in tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        # Return tags that appear in at least 20% of servers
        min_count = max(1, len(tag_lists) * 0.2)
        common_tags = [tag for tag, count in tag_counts.items() if count >= min_count]

        return sorted(common_tags, key=lambda t: tag_counts[t], reverse=True)[:10]

    def _get_complexity_distribution(
        self, metrics_list: list[ServerQualityMetrics]
    ) -> dict[int, int]:
        """Get distribution of setup complexity ratings.

        Args:
            metrics_list: List of server metrics

        Returns:
            Complexity distribution
        """
        distribution = {}
        for metrics in metrics_list:
            complexity = metrics.setup_complexity
            distribution[complexity] = distribution.get(complexity, 0) + 1

        return distribution

    def create_quality_rankings(
        self, organized_data: dict[str, Any]
    ) -> dict[str, list]:
        """Create various quality-based rankings.

        Args:
            organized_data: Organized server data

        Returns:
            Quality rankings
        """
        rankings = {
            "overall_top": organized_data["by_quality"][:20],
            "category_champions": {},
            "rising_stars": [],
            "well_documented": [],
            "easy_to_install": [],
        }

        # Category champions (top server in each category)
        for category, servers in organized_data["by_category"].items():
            if servers:
                rankings["category_champions"][category] = servers[0]

        # Rising stars (high quality, recently updated)
        all_servers = organized_data["by_quality"]
        for server_data, metrics in all_servers:
            if (
                metrics.quality_score > 70
                and "recently_updated" in metrics.tags
                and len(rankings["rising_stars"]) < 10
            ):
                rankings["rising_stars"].append((server_data, metrics))

        # Well documented servers
        well_documented = [
            (server_data, metrics)
            for server_data, metrics in all_servers
            if metrics.documentation_score > 80
        ]
        rankings["well_documented"] = well_documented[:15]

        # Easy to install servers
        easy_install = [
            (server_data, metrics)
            for server_data, metrics in all_servers
            if metrics.setup_complexity <= 2
            and metrics.install_method in ["npm", "pip"]
        ]
        rankings["easy_to_install"] = easy_install[:15]

        return rankings


class BackgroundMCPProcessor:
    """Main background processing service for MCP servers.

    Continuously discovers, processes, and organizes MCP servers with
    comprehensive quality assessment, documentation generation, and
    categorization.

    Attributes:
        batch_size: Number of servers to process in each batch
        sleep_interval: Sleep time between processing cycles (seconds)
        max_servers: Maximum number of servers to process
        data_dir: Directory for data storage
        docs_dir: Directory for generated documentation

    Methods:
        run_continuous: Run continuous background processing
        process_batch: Process a batch of servers
        get_status: Get current processing status
        get_quality_rankings: Get quality rankings

    Example:
        Running background processor::

            processor = BackgroundMCPProcessor(
                batch_size=10,
                sleep_interval=300,
                max_servers=1000
            )

            # Run continuously
            await processor.run_continuous()

        Monitoring progress::

            status = processor.get_status()
            print(f"Processed: {status['total_processed']}")
            print(f"Success rate: {status['success_rate']:.1f}%")
    """

    def __init__(
        self, batch_size: int = 10, sleep_interval: int = 300, max_servers: int = 1000
    ):
        """Initialize the background processor.

        Args:
            batch_size: Number of servers to process per batch
            sleep_interval: Sleep time between cycles in seconds
            max_servers: Maximum servers to process

        Example:
            Creating processor with custom settings::

                processor = BackgroundMCPProcessor(
                    batch_size=20,      # Process 20 servers at a time
                    sleep_interval=600, # Wait 10 minutes between cycles
                    max_servers=2000    # Process up to 2000 servers
                )
        """
        self.batch_size = batch_size
        self.sleep_interval = sleep_interval
        self.max_servers = max_servers

        # Setup directories
        self.data_dir = Path(__file__).parent.parent / "data"
        self.docs_dir = self.data_dir / "documentation"
        self.servers_dir = self.data_dir / "mcp_servers"

        # Create directories
        for dir_path in [self.data_dir, self.docs_dir, self.servers_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.quality_assessor = ServerQualityAssessor()
        self.doc_generator = DocumentationGenerator(self.docs_dir)
        self.category_organizer = CategoryOrganizer()

        # Processing state
        self.processed_servers: set[str] = set()
        self.failed_servers: set[str] = set()
        self.processing_stats = {
            "total_processed": 0,
            "successful": 0,
            "failed": 0,
            "start_time": None,
            "last_update": None,
            "current_batch": 0,
            "estimated_completion": None,
        }

        # Graceful shutdown handling
        self.running = False
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        logger.info(
            f"Initialized BackgroundMCPProcessor: batch_size={batch_size}, "
            f"sleep_interval={sleep_interval}s, max_servers={max_servers}"
        )

    def _signal_handler(self, signum, frame):
        """Handle graceful shutdown signals.

        Args:
            signum: Signal number
            frame: Current stack frame
        """
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        self.running = False

    async def run_continuous(self) -> None:
        """Run continuous background processing.

        This method runs indefinitely, processing MCP servers in batches
        with configurable sleep intervals. It handles graceful shutdown
        and maintains comprehensive processing statistics.

        Raises:
            KeyboardInterrupt: When graceful shutdown is requested

        Example:
            Running with monitoring::

                processor = BackgroundMCPProcessor()

                # Start background task
                task = asyncio.create_task(processor.run_continuous())

                # Monitor progress
                while not task.done():
                    status = processor.get_status()
                    logger.info(f"Progress: {status['progress']:.1f}%")
                    await asyncio.sleep(60)
        """
        logger.info("🚀 Starting continuous MCP server processing")

        self.running = True
        self.processing_stats["start_time"] = datetime.now(UTC).isoformat()

        try:
            while self.running:
                cycle_start = time.time()

                # Load source data
                source_servers = await self._load_source_servers()

                if not source_servers:
                    logger.warning("No source servers found, waiting for next cycle")
                    await asyncio.sleep(self.sleep_interval)
                    continue

                # Filter unprocessed servers
                unprocessed = [
                    server
                    for server in source_servers
                    if self._get_server_id(server) not in self.processed_servers
                ]

                if not unprocessed:
                    logger.info(
                        "All servers processed, starting new cycle with updated data"
                    )
                    # Reset for fresh processing cycle
                    self.processed_servers.clear()
                    await asyncio.sleep(self.sleep_interval)
                    continue

                # Limit to max_servers
                if len(self.processed_servers) >= self.max_servers:
                    logger.info(f"Reached maximum server limit ({self.max_servers})")
                    break

                # Process batch
                batch = unprocessed[: self.batch_size]
                remaining_slots = self.max_servers - len(self.processed_servers)
                batch = batch[:remaining_slots]

                logger.info(
                    f"Processing batch {self.processing_stats['current_batch'] + 1}: "
                    f"{len(batch)} servers"
                )

                await self._process_batch(batch)

                # Update statistics
                self.processing_stats["current_batch"] += 1
                self.processing_stats["last_update"] = datetime.now(UTC).isoformat()

                # Save status
                await self._save_status()

                # Generate documentation for this batch
                try:
                    await self._generate_batch_documentation()
                except Exception as e:
                    logger.exception(f"Failed to generate documentation: {e}")

                # Sleep before next cycle
                cycle_time = time.time() - cycle_start
                sleep_time = max(0, self.sleep_interval - cycle_time)

                if sleep_time > 0:
                    logger.info(
                        f"Cycle completed in {cycle_time:.1f}s, sleeping for {sleep_time:.1f}s"
                    )
                    await asyncio.sleep(sleep_time)
                else:
                    logger.warning(
                        f"Cycle took {cycle_time:.1f}s, longer than interval {self.sleep_interval}s"
                    )

        except KeyboardInterrupt:
            logger.info("Graceful shutdown requested")
        except Exception as e:
            logger.exception(f"Unexpected error in processing loop: {e}")
            raise
        finally:
            await self._cleanup()
            logger.info("Background processing stopped")

    async def _load_source_servers(self) -> list[dict[str, Any]]:
        """Load source server data from production database.

        Returns:
            List of server data dictionaries

        Raises:
            FileNotFoundError: If source data file not found
        """
        try:
            # Try multiple source files
            source_files = [
                self.servers_dir / "production_mcp_database.json",
                self.servers_dir / "all_mcp_documents.json",
                self.servers_dir / "harvest_2025-07-03.json",
            ]

            for source_file in source_files:
                if source_file.exists():
                    logger.debug(f"Loading servers from {source_file}")

                    with open(source_file) as f:
                        data = json.load(f)

                    # Handle different data formats
                    if isinstance(data, dict):
                        if "servers" in data:
                            servers = list(data["servers"].values())
                        elif "data" in data:
                            servers = data["data"]
                        else:
                            servers = [data]  # Single server
                    elif isinstance(data, list):
                        servers = data
                    else:
                        continue

                    logger.info(f"Loaded {len(servers)} servers from {source_file}")
                    return servers

            logger.error("No valid source data files found")
            return []

        except Exception as e:
            logger.exception(f"Failed to load source servers: {e}")
            return []

    def _get_server_id(self, server_data: dict[str, Any]) -> str:
        """Get unique identifier for a server.

        Args:
            server_data: Server data dictionary

        Returns:
            Unique server identifier
        """
        # Try multiple ID sources
        for key in ["repository_url", "name", "repository"]:
            value = server_data.get(key)
            if value:
                return str(value)

        # Fallback to hash of server data
        import hashlib

        content = json.dumps(server_data, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()

    async def _process_batch(self, batch: list[dict[str, Any]]) -> None:
        """Process a batch of servers.

        Args:
            batch: List of server data dictionaries
        """
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30)
        ) as session:
            tasks = []
            for server_data in batch:
                task = self._process_single_server(server_data, session)
                tasks.append(task)

            # Process servers concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Update statistics
            for i, result in enumerate(results):
                server_id = self._get_server_id(batch[i])

                if isinstance(result, Exception):
                    logger.error(f"Failed to process {server_id}: {result}")
                    self.failed_servers.add(server_id)
                    self.processing_stats["failed"] += 1
                else:
                    self.processed_servers.add(server_id)
                    self.processing_stats["successful"] += 1

                self.processing_stats["total_processed"] += 1

    async def _process_single_server(
        self, server_data: dict[str, Any], session: aiohttp.ClientSession
    ) -> ServerQualityMetrics:
        """Process a single MCP server.

        Args:
            server_data: Server data dictionary
            session: HTTP session for API calls

        Returns:
            Server quality metrics

        Raises:
            Exception: If processing fails
        """
        server_name = server_data.get("name", "Unknown")
        logger.debug(f"Processing server: {server_name}")

        try:
            # Assess quality
            metrics = await self.quality_assessor.assess_server(server_data, session)

            # Generate documentation
            await self.doc_generator.generate_server_docs(server_data, metrics)

            # Save individual server data
            await self._save_server_data(server_data, metrics)

            logger.info(
                f"✅ Processed {server_name}: quality={metrics.quality_score:.1f}"
            )

            return metrics

        except Exception as e:
            logger.exception(f"❌ Failed to process {server_name}: {e}")
            raise

    async def _save_server_data(
        self, server_data: dict[str, Any], metrics: ServerQualityMetrics
    ) -> None:
        """Save processed server data and metrics.

        Args:
            server_data: Original server data
            metrics: Quality assessment metrics
        """
        # Create processed data structure
        processed_data = {
            "server_data": server_data,
            "quality_metrics": asdict(metrics),
            "processed_at": datetime.now(UTC).isoformat(),
            "processor_version": "1.0.0",
        }

        # Save to individual file
        server_file = (
            self.servers_dir / "processed" / f"{metrics.name.replace('/', '_')}.json"
        )
        server_file.parent.mkdir(exist_ok=True)

        with open(server_file, "w") as f:
            json.dump(processed_data, f, indent=2)

    async def _generate_batch_documentation(self) -> None:
        """Generate documentation for the current batch of processed servers."""
        try:
            # Load all processed servers
            processed_servers = []
            processed_dir = self.servers_dir / "processed"

            if processed_dir.exists():
                for server_file in processed_dir.glob("*.json"):
                    try:
                        with open(server_file) as f:
                            data = json.load(f)
                        processed_servers.append(
                            (
                                data["server_data"],
                                ServerQualityMetrics(**data["quality_metrics"]),
                            )
                        )
                    except Exception as e:
                        logger.warning(f"Failed to load {server_file}: {e}")

            if not processed_servers:
                return

            # Organize servers
            organized = self.category_organizer.organize_servers(processed_servers)

            # Generate category summaries
            summaries = self.category_organizer.generate_category_summaries(organized)

            # Create quality rankings
            rankings = self.category_organizer.create_quality_rankings(organized)

            # Save organized data
            organized_file = self.servers_dir / "organized_servers.json"
            with open(organized_file, "w") as f:
                json.dump(
                    {
                        "organized": self._serialize_organized_data(organized),
                        "summaries": summaries,
                        "rankings": self._serialize_organized_data(rankings),
                        "generated_at": datetime.now(UTC).isoformat(),
                    },
                    f,
                    indent=2,
                )

            logger.info(f"Generated documentation for {len(processed_servers)} servers")

        except Exception as e:
            logger.exception(f"Failed to generate batch documentation: {e}")

    def _serialize_organized_data(self, data: Any) -> Any:
        """Serialize organized data for JSON storage.

        Args:
            data: Data structure to serialize

        Returns:
            JSON-serializable data
        """
        if isinstance(data, dict):
            return {k: self._serialize_organized_data(v) for k, v in data.items()}
        if isinstance(data, list):
            return [self._serialize_organized_data(item) for item in data]
        if isinstance(data, tuple) and len(data) == 2:
            # (server_data, metrics) tuple
            server_data, metrics = data
            return {
                "server_data": server_data,
                "metrics": (
                    metrics.to_dict()
                    if isinstance(metrics, ServerQualityMetrics)
                    else metrics
                ),
            }
        if isinstance(data, ServerQualityMetrics):
            # Convert ServerQualityMetrics object to dict
            return data.to_dict()
        return data

    async def _save_status(self) -> None:
        """Save current processing status."""
        status_file = self.servers_dir / "processing_status.json"

        # Calculate additional statistics
        total = self.processing_stats["total_processed"]
        success_rate = (
            (self.processing_stats["successful"] / total * 100) if total > 0 else 0
        )

        # Estimate completion time
        if self.processing_stats["start_time"] and total > 0:
            start_time = datetime.fromisoformat(self.processing_stats["start_time"])
            elapsed = (datetime.now(UTC) - start_time).total_seconds()
            rate = total / elapsed if elapsed > 0 else 0

            remaining = self.max_servers - total
            if rate > 0 and remaining > 0:
                eta_seconds = remaining / rate
                eta = datetime.now(UTC) + timedelta(seconds=eta_seconds)
                self.processing_stats["estimated_completion"] = eta.isoformat()

        status = {
            **self.processing_stats,
            "success_rate": success_rate,
            "progress": (total / self.max_servers * 100) if self.max_servers > 0 else 0,
            "processed_server_ids": list(self.processed_servers),
            "failed_server_ids": list(self.failed_servers),
            "running": self.running,
        }

        with open(status_file, "w") as f:
            json.dump(status, f, indent=2)

    async def _cleanup(self) -> None:
        """Cleanup resources and save final status."""
        logger.info("Performing cleanup...")

        # Save final status
        await self._save_status()

        # Generate final documentation
        try:
            await self._generate_batch_documentation()
        except Exception as e:
            logger.exception(f"Failed to generate final documentation: {e}")

        logger.info("Cleanup completed")

    def get_status(self) -> dict[str, Any]:
        """Get current processing status.

        Returns:
            Current processing status dictionary

        Example:
            Checking processing status::

                status = processor.get_status()
                print(f"Progress: {status['progress']:.1f}%")
                print(f"Success rate: {status['success_rate']:.1f}%")
                print(f"ETA: {status.get('estimated_completion', 'Unknown')}")
        """
        total = self.processing_stats["total_processed"]
        success_rate = (
            (self.processing_stats["successful"] / total * 100) if total > 0 else 0
        )

        return {
            **self.processing_stats,
            "success_rate": success_rate,
            "progress": (total / self.max_servers * 100) if self.max_servers > 0 else 0,
            "running": self.running,
            "servers_processed": len(self.processed_servers),
            "servers_failed": len(self.failed_servers),
        }

    def get_quality_rankings(self, limit: int = 20) -> list[dict[str, Any]]:
        """Get quality rankings of processed servers.

        Args:
            limit: Maximum number of servers to return

        Returns:
            List of top-quality servers with metrics

        Example:
            Getting top quality servers::

                rankings = processor.get_quality_rankings(10)
                for i, server in enumerate(rankings, 1):
                    print(f"{i}. {server['name']}: {server['quality_score']:.1f}")
        """
        try:
            organized_file = self.servers_dir / "organized_servers.json"
            if not organized_file.exists():
                return []

            with open(organized_file) as f:
                data = json.load(f)

            rankings = data.get("rankings", {}).get("overall_top", [])

            result = []
            for item in rankings[:limit]:
                if isinstance(item, dict) and "metrics" in item:
                    metrics = item["metrics"]
                    result.append(
                        {
                            "name": metrics.get("name", "Unknown"),
                            "quality_score": metrics.get("quality_score", 0),
                            "category": metrics.get("category", "unknown"),
                            "install_method": metrics.get("install_method", "unknown"),
                        }
                    )

            return result

        except Exception as e:
            logger.exception(f"Failed to get quality rankings: {e}")
            return []


async def main():
    """Main entry point for background MCP processor.

    Example:
        Running the background processor::

            # Default settings
            python background_mcp_processor.py

            # Custom settings via environment variables
            BATCH_SIZE=20 SLEEP_INTERVAL=600 MAX_SERVERS=2000 python background_mcp_processor.py
    """
    # Configuration from environment
    batch_size = int(os.environ.get("BATCH_SIZE", "10"))
    sleep_interval = int(os.environ.get("SLEEP_INTERVAL", "300"))  # 5 minutes
    max_servers = int(os.environ.get("MAX_SERVERS", "1000"))

    # Create processor
    processor = BackgroundMCPProcessor(
        batch_size=batch_size, sleep_interval=sleep_interval, max_servers=max_servers
    )

    # Run continuously
    try:
        await processor.run_continuous()
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user")
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import os
    from datetime import timedelta

    asyncio.run(main())
