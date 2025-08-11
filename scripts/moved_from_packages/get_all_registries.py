#!/usr/bin/env python3
"""Get ALL MCP servers from major registries - AGGRESSIVE MODE."""

import asyncio
import json
import re
from datetime import UTC, datetime
from pathlib import Path

import aiohttp

data_dir = Path("data/mcp_servers")


async def fetch_pulsemcp_servers(session: aiohttp.ClientSession) -> list[dict]:
    """Fetch all servers from PulseMCP (4890+ servers)."""
    servers = []

    # PulseMCP has a public API
    try:
        # Try multiple endpoints
        endpoints = [
            "https://www.pulsemcp.com/api/servers",
            "https://www.pulsemcp.com/servers.json",
            "https://raw.githubusercontent.com/pulsemcp/servers/main/servers.json",
            "https://pulsemcp.com/api/v1/servers",
        ]

        for url in endpoints:
            try:
                async with session.get(url, timeout=30) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if isinstance(data, list):
                            servers = data
                        elif isinstance(data, dict) and "servers" in data:
                            servers = data["servers"]
                        break
            except:
                continue

        if not servers:
            # Try scraping the website
            async with session.get(
                "https://www.pulsemcp.com/servers", timeout=30
            ) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    # Extract server data from HTML/JS
                    match = re.search(
                        r"window\.__INITIAL_DATA__\s*=\s*({.*?});", html, re.DOTALL
                    )
                    if match:
                        data = json.loads(match.group(1))
                        if "servers" in data:
                            servers = data["servers"]
    except Exception:
        pass

    return servers


async def fetch_smithery_servers(session: aiohttp.ClientSession) -> list[dict]:
    """Fetch all servers from Smithery (2211+ servers)."""
    servers = []

    try:
        # Smithery API endpoints
        endpoints = [
            "https://smithery.ai/api/servers",
            "https://api.smithery.ai/v1/servers",
            "https://smithery.ai/api/mcp/servers",
            "https://smithery.ai/servers.json",
        ]

        for url in endpoints:
            try:
                async with session.get(url, timeout=30) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if isinstance(data, list):
                            servers = data
                        elif isinstance(data, dict) and "servers" in data:
                            servers = data["servers"]
                        break
            except:
                continue
    except Exception:
        pass

    return servers


async def fetch_mcp_registry(session: aiohttp.ClientSession) -> list[dict]:
    """Fetch all servers from MCP Registry (1000+ servers)."""
    servers = []

    try:
        # MCP Registry endpoints
        endpoints = [
            "https://mcpregistry.click/api/servers",
            "https://api.mcpregistry.click/servers",
            "https://mcpregistry.click/servers.json",
            "https://mcpregistry.click/api/v1/registry",
        ]

        for url in endpoints:
            try:
                async with session.get(url, timeout=30) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if isinstance(data, list):
                            servers = data
                        elif isinstance(data, dict) and "servers" in data:
                            servers = data["servers"]
                        break
            except:
                continue
    except Exception:
        pass

    return servers


async def fetch_github_topic_servers(
    session: aiohttp.ClientSession, topic: str
) -> list[dict]:
    """Fetch servers from GitHub topic."""
    servers = []

    try:
        # GitHub API - get repos with topic
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "MCP-Server-Harvester",
        }

        # Add GitHub token if available
        import os

        if os.getenv("GITHUB_TOKEN"):
            headers["Authorization"] = f"token {os.getenv('GITHUB_TOKEN')}"

        page = 1
        while page <= 10:  # Limit to 10 pages
            url = f"https://api.github.com/search/repositories?q=topic:{topic}&per_page=100&page={page}"

            async with session.get(url, headers=headers, timeout=30) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    repos = data.get("items", [])

                    for repo in repos:
                        server = {
                            "name": repo["name"],
                            "repository_url": repo["html_url"],
                            "description": repo["description"],
                            "stars": repo["stargazers_count"],
                            "source": f"github-topic:{topic}",
                            "owner": repo["owner"]["login"],
                        }
                        servers.append(server)

                    if len(repos) < 100:
                        break
                    page += 1
                else:
                    break

    except Exception:
        pass

    return servers


async def fetch_tensorblock_servers(session: aiohttp.ClientSession) -> list[dict]:
    """Fetch servers from TensorBlock's awesome list (7260+ servers)."""
    servers = []

    try:
        # Get the README
        url = "https://raw.githubusercontent.com/TensorBlock/awesome-mcp-servers/main/README.md"
        async with session.get(url, timeout=30) as resp:
            if resp.status == 200:
                content = await resp.text()

                # Parse servers from markdown
                # Look for patterns like [name](url) - description
                pattern = r"\[([^\]]+)\]\(([^)]+)\)\s*-\s*([^\n]+)"
                matches = re.findall(pattern, content)

                for name, url, desc in matches:
                    if "github.com" in url:
                        server = {
                            "name": name,
                            "repository_url": url,
                            "description": desc.strip(),
                            "source": "github:TensorBlock/awesome-mcp-servers",
                        }
                        servers.append(server)

    except Exception:
        pass

    return servers


async def main():
    """Fetch all servers from all major registries."""
    all_servers = {}

    async with aiohttp.ClientSession() as session:
        # Fetch from all sources in parallel
        tasks = [
            fetch_pulsemcp_servers(session),
            fetch_smithery_servers(session),
            fetch_mcp_registry(session),
            fetch_github_topic_servers(session, "mcp-server"),
            fetch_github_topic_servers(session, "model-context-protocol"),
            fetch_tensorblock_servers(session),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        sources = [
            "PulseMCP",
            "Smithery",
            "MCP Registry",
            "GitHub:mcp-server",
            "GitHub:model-context-protocol",
            "TensorBlock",
        ]

        for _source, result in zip(sources, results, strict=False):
            if isinstance(result, Exception):
                pass
            elif result:
                for server in result:
                    # Use repository URL as unique key
                    key = server.get("repository_url", server.get("name", ""))
                    if key:
                        all_servers[key] = server

    # Load existing servers
    existing_file = data_dir / "production_mcp_database.json"
    if existing_file.exists():
        with open(existing_file) as f:
            existing_data = json.load(f)
            existing_servers = existing_data.get("servers", {})
    else:
        existing_servers = {}

    # Merge new servers
    new_count = 0
    for key, server in all_servers.items():
        if key not in existing_servers:
            new_count += 1

    # Save all fetched servers
    output_file = data_dir / "ALL_REGISTRY_SERVERS.json"
    output = {
        "metadata": {
            "fetched_at": datetime.now(UTC).isoformat(),
            "total_servers": len(all_servers),
            "new_servers": new_count,
            "sources": {
                "PulseMCP": len(
                    [
                        s
                        for s in all_servers.values()
                        if "pulsemcp" in s.get("source", "").lower()
                    ]
                ),
                "Smithery": len(
                    [
                        s
                        for s in all_servers.values()
                        if "smithery" in s.get("source", "").lower()
                    ]
                ),
                "MCP Registry": len(
                    [
                        s
                        for s in all_servers.values()
                        if "mcpregistry" in s.get("source", "").lower()
                    ]
                ),
                "GitHub Topics": len(
                    [
                        s
                        for s in all_servers.values()
                        if "github-topic" in s.get("source", "").lower()
                    ]
                ),
                "TensorBlock": len(
                    [
                        s
                        for s in all_servers.values()
                        if "TensorBlock" in s.get("source", "")
                    ]
                ),
            },
        },
        "servers": list(all_servers.values()),
    }

    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)


if __name__ == "__main__":
    asyncio.run(main())
