#!/usr/bin/env python3
"""Process ALL MCP servers immediately without waiting.

This script processes all available MCP servers in one go, generating
documentation, quality assessments, and categorization for everything.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from background_mcp_processor import BackgroundMCPProcessor


async def process_all_servers():
    """Process all servers immediately."""
    print("🚀 Processing ALL MCP servers...")

    # Initialize processor with maximum batch size
    processor = BackgroundMCPProcessor(
        batch_size=2000,  # Process all at once
        sleep_interval=1,  # Minimal sleep
        max_servers=10000,  # No limit
    )

    try:
        # Load all servers
        await processor._load_servers()
        total = len(processor.all_servers)
        print(f"📊 Found {total} servers to process")

        # Process everything in one batch
        if processor.unprocessed_servers:
            print(
                f"⚡ Processing {len(processor.unprocessed_servers)} unprocessed servers..."
            )
            await processor._process_batch(processor.unprocessed_servers)

        # Generate final documentation
        print("📚 Generating comprehensive documentation...")
        await processor._generate_batch_documentation(
            processor.processed_servers,
            processor.organized_servers,
            processor.category_summaries,
            processor.quality_rankings,
        )

        # Save final status
        await processor._save_status()

        # Generate summary report
        print("\n✅ PROCESSING COMPLETE!")
        print(f"📊 Total servers: {total}")
        print(f"✅ Successfully processed: {len(processor.processed_servers)}")
        print(f"❌ Failed: {len(processor.failed_servers)}")
        print(f"📁 Categories: {len(processor.organized_servers['by_category'])}")
        print(
            f"⭐ Average quality score: {sum(m.quality_score for _, m in processor.processed_servers) / len(processor.processed_servers):.1f}"
        )

        # Top 10 servers by quality
        print("\n🏆 Top 10 servers by quality:")
        top_servers = sorted(
            processor.processed_servers, key=lambda x: x[1].quality_score, reverse=True
        )[:10]
        for i, (server, metrics) in enumerate(top_servers, 1):
            print(f"{i}. {server['name']} - Quality: {metrics.quality_score:.1f}")

        # Category summary
        print("\n📊 Category distribution:")
        for category, servers in processor.organized_servers["by_category"].items():
            print(f"  {category}: {len(servers)} servers")

    except KeyboardInterrupt:
        print("\n⚠️ Processing interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        processor.running = False


if __name__ == "__main__":
    print("=" * 60)
    print("MCP SERVER BATCH PROCESSOR - PROCESS ALL")
    print("=" * 60)

    asyncio.run(process_all_servers())
