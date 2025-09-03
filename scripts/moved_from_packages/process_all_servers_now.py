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
    # Initialize processor with maximum batch size
    processor = BackgroundMCPProcessor(
        batch_size=2000,  # Process all at once
        sleep_interval=1,  # Minimal sleep
        max_servers=10000,  # No limit
    )

    try:
        # Load all servers
        await processor._load_servers()
        len(processor.all_servers)

        # Process everything in one batch
        if processor.unprocessed_servers:
            await processor._process_batch(processor.unprocessed_servers)

        # Generate final documentation
        await processor._generate_batch_documentation(
            processor.processed_servers,
            processor.organized_servers,
            processor.category_summaries,
            processor.quality_rankings,
        )

        # Save final status
        await processor._save_status()

        # Generate summary report

        # Top 10 servers by quality
        top_servers = sorted(
            processor.processed_servers, key=lambda x: x[1].quality_score, reverse=True
        )[:10]
        for _i, (_server, _metrics) in enumerate(top_servers, 1):
            pass

        # Category summary
        for _category, _servers in processor.organized_servers["by_category"].items():
            pass

    except KeyboardInterrupt:
        pass
    except Exception:
        import traceback

        traceback.print_exc()
    finally:
        processor.running = False


if __name__ == "__main__":
    asyncio.run(process_all_servers())
