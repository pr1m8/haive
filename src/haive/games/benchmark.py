#!/usr/bin/env python3
"""
Benchmark script for testing game agents.

This script runs benchmarks for the Monopoly and Poker agents
to test their performance and identify issues.
"""

import sys
import os
import logging
import time
import argparse
import traceback
from pathlib import Path

# Add the project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.haive.games.monopoly.test import MonopolyAgentTester
from src.haive.games.poker.test import PokerAgentTester

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("benchmark.log", mode="w")
    ]
)

logger = logging.getLogger(__name__)

def run_monopoly_benchmark():
    """Run benchmark tests for the Monopoly agent."""
    print("\n" + "="*50)
    print("MONOPOLY AGENT BENCHMARK")
    print("="*50)
    
    try:
        start_time = time.time()
        tester = MonopolyAgentTester(model="gpt-4o", temperature=0.7)
        success, fails, issues = tester.run_all_tests()
        duration = time.time() - start_time
        
        print(f"Benchmark completed in {duration:.2f}s")
        print(f"Successful tests: {success}")
        print(f"Failed tests: {fails}")
        
        return success, fails, issues
    
    except Exception as e:
        logger.error(f"Error running Monopoly benchmark: {e}")
        logger.error(traceback.format_exc())
        print(f"Error running Monopoly benchmark: {e}")
        return 0, 1, [{"test": "benchmark_setup", "error": str(e)}]

def run_poker_benchmark():
    """Run benchmark tests for the Poker agent."""
    print("\n" + "="*50)
    print("POKER AGENT BENCHMARK")
    print("="*50)
    
    try:
        start_time = time.time()
        tester = PokerAgentTester(use_default_engines=True)
        success, fails, issues = tester.run_all_tests()
        duration = time.time() - start_time
        
        print(f"Benchmark completed in {duration:.2f}s")
        print(f"Successful tests: {success}")
        print(f"Failed tests: {fails}")
        
        return success, fails, issues
    
    except Exception as e:
        logger.error(f"Error running Poker benchmark: {e}")
        logger.error(traceback.format_exc())
        print(f"Error running Poker benchmark: {e}")
        return 0, 1, [{"test": "benchmark_setup", "error": str(e)}]

def main():
    """Run all benchmarks based on command line arguments."""
    parser = argparse.ArgumentParser(description="Benchmark game agents")
    
    parser.add_argument(
        "--monopoly", 
        action="store_true",
        help="Run Monopoly agent benchmark"
    )
    
    parser.add_argument(
        "--poker", 
        action="store_true",
        help="Run Poker agent benchmark"
    )
    
    parser.add_argument(
        "--all", 
        action="store_true",
        help="Run all benchmarks"
    )
    
    args = parser.parse_args()
    
    # Default to all if no specific agents selected
    run_all = args.all or not (args.monopoly or args.poker)
    
    start_time = time.time()
    total_success = 0
    total_fails = 0
    
    # Run monopoly benchmark
    if args.monopoly or run_all:
        m_success, m_fails, m_issues = run_monopoly_benchmark()
        total_success += m_success
        total_fails += m_fails
    
    # Run poker benchmark
    if args.poker or run_all:
        p_success, p_fails, p_issues = run_poker_benchmark()
        total_success += p_success
        total_fails += p_fails
    
    # Print summary
    total_duration = time.time() - start_time
    print("\n" + "="*50)
    print("BENCHMARK SUMMARY")
    print("="*50)
    print(f"Total benchmarks completed in {total_duration:.2f}s")
    print(f"Total successful tests: {total_success}")
    print(f"Total failed tests: {total_fails}")
    print("="*50)
    
    # Return exit code based on success/failure
    return 0 if total_fails == 0 else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 