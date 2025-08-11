#!/usr/bin/env python3
"""Get ALL MCP servers with complete processing."""

import json
from datetime import UTC, datetime
from pathlib import Path

# Paths
data_dir = Path("data/mcp_servers")
production_db = data_dir / "production_mcp_database.json"
output_file = data_dir / "ALL_MCP_SERVERS_COMPLETE.json"


# Load all servers
with open(production_db) as f:
    data = json.load(f)

servers_dict = data.get("servers", {})
servers = list(servers_dict.values())
total = len(servers)


# Organize by category
by_category = {}
by_source = {}
by_language = {}
official_servers = []
npm_servers = []
pip_servers = []

for server in servers:
    # By category
    category = server.get("category", "uncategorized")
    if category not in by_category:
        by_category[category] = []
    by_category[category].append(server)

    # By source
    source = server.get("source", "unknown")
    if source not in by_source:
        by_source[source] = []
    by_source[source].append(server)

    # Official servers
    if server.get("is_official", False):
        official_servers.append(server)

    # NPM packages
    if server.get("npm_package"):
        npm_servers.append(server)

    # Python packages
    if "pip install" in str(server.get("install_command", "")):
        pip_servers.append(server)

# Create comprehensive output
output = {
    "metadata": {
        "generated_at": datetime.now(UTC).isoformat(),
        "total_servers": total,
        "categories": len(by_category),
        "sources": len(by_source),
        "official_servers": len(official_servers),
        "npm_packages": len(npm_servers),
        "pip_packages": len(pip_servers),
    },
    "all_servers": servers,
    "by_category": by_category,
    "by_source": by_source,
    "official_servers": official_servers,
    "npm_servers": npm_servers,
    "pip_servers": pip_servers,
    "statistics": {
        "category_distribution": {cat: len(srvs) for cat, srvs in by_category.items()},
        "source_distribution": {src: len(srvs) for src, srvs in by_source.items()},
    },
}

# Save comprehensive file
with open(output_file, "w") as f:
    json.dump(output, f, indent=2)

for cat, _count in sorted(
    output["statistics"]["category_distribution"].items(),
    key=lambda x: x[1],
    reverse=True,
):
    pass

for _src, _count in sorted(
    output["statistics"]["source_distribution"].items(),
    key=lambda x: x[1],
    reverse=True,
)[:10]:
    pass


# Also create a simple list file
simple_list = data_dir / "ALL_SERVERS_LIST.txt"
with open(simple_list, "w") as f:
    f.write(f"ALL {total} MCP SERVERS\n")
    f.write("=" * 60 + "\n\n")

    for cat, servers in sorted(by_category.items()):
        f.write(f"\n{cat.upper()} ({len(servers)} servers)\n")
        f.write("-" * 40 + "\n")
        for server in sorted(servers, key=lambda x: x.get("name", "")):
            name = server.get("name", "Unknown")
            repo = server.get("repository_url", "")
            f.write(f"- {name}: {repo}\n")
