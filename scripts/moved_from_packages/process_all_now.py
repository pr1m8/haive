#!/usr/bin/env python3
"""Process ALL MCP servers immediately in one batch."""

import asyncio
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from background_mcp_processor import BackgroundMCPProcessor


async def main():
    """Process all servers immediately."""
    # Create processor with maximum settings
    processor = BackgroundMCPProcessor(
        batch_size=5000,  # Process all at once
        sleep_interval=1,  # No waiting
        max_servers=10000,  # No limit
    )

    # Load the production database directly
    production_db = processor.servers_dir / "production_mcp_database.json"

    with open(production_db) as f:
        data = json.load(f)

    all_servers = data.get("servers", [])
    total = len(all_servers)

    start_time = datetime.now(UTC)

    # Process all servers
    processed = []
    failed = []

    for i, server in enumerate(all_servers):
        try:
            # Process each server
            metrics = await processor.quality_assessor.assess_server(server)
            processed.append((server, metrics))

            if (i + 1) % 100 == 0:
                pass

        except Exception:
            failed.append(server)

    # Organize all servers
    organized = processor.category_organizer.organize_servers(processed)

    # Generate category summaries
    summaries = processor.doc_generator.generate_category_summaries(organized)

    # Generate quality rankings
    rankings = processor.doc_generator.generate_quality_rankings(processed)

    # Save everything

    # Save organized servers
    organized_file = processor.servers_dir / "all_servers_organized.json"
    with open(organized_file, "w") as f:
        json.dump(
            {
                "organized": processor._serialize_organized_data(organized),
                "summaries": processor._serialize_organized_data(summaries),
                "rankings": processor._serialize_organized_data(rankings),
                "generated_at": datetime.now(UTC).isoformat(),
                "total_servers": total,
                "processed": len(processed),
                "failed": len(failed),
            },
            f,
            indent=2,
        )

    # Generate documentation
    await processor._generate_batch_documentation(
        processed, organized, summaries, rankings
    )

    # Calculate statistics
    end_time = datetime.now(UTC)
    (end_time - start_time).total_seconds()

    # Show category distribution
    for _category, _servers in sorted(
        organized["by_category"].items(), key=lambda x: len(x[1]), reverse=True
    ):
        pass

    # Show top 20 servers
    top_servers = sorted(processed, key=lambda x: x[1].quality_score, reverse=True)[:20]
    for i, (server, metrics) in enumerate(top_servers, 1):
        pass


if __name__ == "__main__":
    asyncio.run(main())
