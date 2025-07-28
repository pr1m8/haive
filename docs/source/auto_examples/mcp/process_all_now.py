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
    print("🚀 PROCESSING ALL MCP SERVERS NOW!")
    print("=" * 60)

    # Create processor with maximum settings
    processor = BackgroundMCPProcessor(
        batch_size=5000,  # Process all at once
        sleep_interval=1,  # No waiting
        max_servers=10000,  # No limit
    )

    # Load the production database directly
    production_db = processor.servers_dir / "production_mcp_database.json"

    print(f"📂 Loading servers from: {production_db}")

    with open(production_db) as f:
        data = json.load(f)

    all_servers = data.get("servers", [])
    total = len(all_servers)

    print(f"📊 Found {total} servers to process!")
    print("⚡ Starting batch processing...")

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
                print(
                    f"  Processed {i + 1}/{total} servers ({(i + 1) / total * 100:.1f}%)"
                )

        except Exception as e:
            failed.append(server)
            print(f"  ❌ Failed: {server.get('name', 'Unknown')} - {e!s}")

    # Organize all servers
    print("\n📁 Organizing servers by category...")
    organized = processor.category_organizer.organize_servers(processed)

    # Generate category summaries
    print("📊 Generating category summaries...")
    summaries = processor.doc_generator.generate_category_summaries(organized)

    # Generate quality rankings
    print("⭐ Creating quality rankings...")
    rankings = processor.doc_generator.generate_quality_rankings(processed)

    # Save everything
    print("\n💾 Saving results...")

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
    print("📚 Generating Sphinx documentation...")
    await processor._generate_batch_documentation(
        processed, organized, summaries, rankings
    )

    # Calculate statistics
    end_time = datetime.now(UTC)
    duration = (end_time - start_time).total_seconds()

    print("\n" + "=" * 60)
    print("✅ PROCESSING COMPLETE!")
    print("=" * 60)
    print(f"📊 Total servers: {total}")
    print(f"✅ Successfully processed: {len(processed)}")
    print(f"❌ Failed: {len(failed)}")
    print(f"⏱️  Time taken: {duration:.1f} seconds")
    print(f"📁 Categories: {len(organized['by_category'])}")

    # Show category distribution
    print("\n📊 Category Distribution:")
    for category, servers in sorted(
        organized["by_category"].items(), key=lambda x: len(x[1]), reverse=True
    ):
        print(f"  {category}: {len(servers)} servers")

    # Show top 20 servers
    print("\n🏆 Top 20 Servers by Quality:")
    top_servers = sorted(processed, key=lambda x: x[1].quality_score, reverse=True)[:20]
    for i, (server, metrics) in enumerate(top_servers, 1):
        print(f"{i:2d}. {server['name'][:40]:<40} Quality: {metrics.quality_score:.1f}")

    print(f"\n📁 Results saved to: {organized_file}")
    print("✨ All done!")


if __name__ == "__main__":
    asyncio.run(main())
