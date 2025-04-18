#!/usr/bin/env python3
"""
Test script for MonopolyAgentConfig validation
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.haive.games.monopoly.config import MonopolyAgentConfig
from src.haive.core.engine.aug_llm import AugLLMConfig

def main():
    """Test MonopolyAgentConfig instantiation."""
    try:
        print("Creating default MonopolyAgentConfig...")
        config = MonopolyAgentConfig()
        print("Success! MonopolyAgentConfig created.")
        print(f"Number of engines: {len(config.engines)}")
        
        # Test MonopolyAgent creation
        from src.haive.games.monopoly.agent import MonopolyAgent
        agent = MonopolyAgent(config=config)
        print("Success! MonopolyAgent created.")
        
        return 0
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 