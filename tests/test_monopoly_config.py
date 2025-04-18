#!/usr/bin/env python3
"""
Test script for MonopolyAgentConfig validation
"""

import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.haive.games.monopoly.config import MonopolyAgentConfig


def main():
    """Test MonopolyAgentConfig instantiation."""
    try:
        config = MonopolyAgentConfig()

        # Test MonopolyAgent creation
        from src.haive.games.monopoly.agent import MonopolyAgent

        MonopolyAgent(config=config)

        return 0
    except Exception:
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
