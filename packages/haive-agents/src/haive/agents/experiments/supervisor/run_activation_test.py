"""Simple runner for the activation test."""

import asyncio
import sys
from pathlib import Path

# Add package to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from three_agent_inactive_test import test_dynamic_activation

if __name__ == "__main__":
    asyncio.run(test_dynamic_activation())
