#!/usr/bin/env python
"""
CLI tool for running KYC reports and utilities
"""

import argparse
import logging
import sys
import time
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from src.haive.prebuilt.priv.kyc.config import KYCReportConfig
from src.haive.prebuilt.priv.kyc.agent import KYCReportAgent
from langchain_core.messages import HumanMessage

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("kyc-cli")

def run_kyc_report(file_path: str, **kwargs) -> None:
    """
    Run a KYC report generation on the text from the specified file.
    
    Args:
        file_path: Path to a text file containing data to analyze
        **kwargs: Additional arguments to pass to the agent
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Create a configuration for the KYC agent
    config = KYCReportConfig()
    agent = KYCReportAgent(config=config)
    final_state = agent.run({"input_text": text})
    
    # Save state history
    state_history_path = kwargs.get('save_state_path')
    if state_history_path:
        agent.save_state_history(state_history_path)
        logging.info(f"State history saved to {state_history_path}")
    
    # Generate report
    report = agent.generate_markdown_report(final_state)
    
    # Save report
    output_path = kwargs.get('output')
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        logging.info(f"Report saved to {output_path}")
    else:
        print(report)

def convert_state_to_markdown(state_path: str, output_path: Optional[str] = None) -> None:
    """
    Convert a saved state JSON file to a markdown report
    
    Args:
        state_path: Path to a saved state JSON file
        output_path: Path to save the markdown report (optional)
    """
    # Load the state
    with open(state_path, 'r', encoding='utf-8') as f:
        try:
            state_data = json.load(f)
            
            # If this is a state history file, use the last state
            if isinstance(state_data, list) and len(state_data) > 0:
                state = state_data[-1]
            else:
                state = state_data
                
        except json.JSONDecodeError:
            logging.error(f"Failed to parse JSON from {state_path}")
            return
    
    # Generate markdown report
    config = KYCReportConfig()
    agent = KYCReportAgent(config=config)
    report = agent.generate_markdown_report(state)
    
    # Save or print the report
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        logging.info(f"Report saved to {output_path}")
    else:
        print(report)

def visualize_state(state_path: str, step: Optional[int] = None, output_md: Optional[str] = None) -> None:
    """
    Visualize a specific state from a saved state history file
    
    Args:
        state_path: Path to a saved state history JSON file
        step: Index of the state to visualize (default: last state)
        output_md: Path to save the markdown report (optional)
    """
    # Load the state history
    with open(state_path, 'r', encoding='utf-8') as f:
        try:
            state_data = json.load(f)
            
            # Check if this is a state history file (list of states)
            if isinstance(state_data, list):
                if not state_data:
                    logging.error(f"State history file is empty: {state_path}")
                    return
                
                # If step is specified, use that state
                if step is not None:
                    if step < 0 or step >= len(state_data):
                        logging.error(f"Invalid step {step}, file contains {len(state_data)} states")
                        return
                    state = state_data[step]
                    print(f"Visualizing state at step {step} of {len(state_data)-1}")
                else:
                    # Default to the last state
                    state = state_data[-1]
                    print(f"Visualizing final state (step {len(state_data)-1})")
            else:
                # Single state
                state = state_data
                print("Visualizing single state")
                
        except json.JSONDecodeError:
            logging.error(f"Failed to parse JSON from {state_path}")
            return
    
    # Visualize the state
    config = KYCReportConfig()
    agent = KYCReportAgent(config=config)
    agent.visualize_state(state)
    
    # Generate markdown report if requested
    if output_md:
        report = agent.generate_markdown_report(state)
        with open(output_md, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\nMarkdown report saved to {output_md}")

def main():
    """
    CLI entry point for the KYC reporting tool
    """
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Create the argument parser
    parser = argparse.ArgumentParser(description='KYC report generation tool')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Report generation command
    report_parser = subparsers.add_parser('report', help='Generate a KYC report from a text file')
    report_parser.add_argument('file', help='Path to text file with data to analyze')
    report_parser.add_argument('-o', '--output', help='Path to save the generated report')
    report_parser.add_argument('-s', '--save-state', dest='save_state_path', 
                             help='Path to save the state history for later visualization')
    
    # Convert state to markdown command
    convert_parser = subparsers.add_parser('convert-state', help='Convert a saved state to a markdown report')
    convert_parser.add_argument('state_file', help='Path to saved state JSON file')
    convert_parser.add_argument('-o', '--output', help='Path to save the generated report')
    
    # Visualize state command
    visualize_parser = subparsers.add_parser('visualize', help='Visualize a state from a state history file')
    visualize_parser.add_argument('state_file', help='Path to saved state history JSON file')
    visualize_parser.add_argument('-s', '--step', type=int, help='Index of state to visualize (default: last state)')
    visualize_parser.add_argument('-m', '--markdown', dest='output_md', help='Generate and save markdown report to specified path')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute the appropriate command
    if args.command == 'report':
        run_kyc_report(args.file, output=args.output, save_state_path=args.save_state_path)
    elif args.command == 'convert-state':
        convert_state_to_markdown(args.state_file, args.output)
    elif args.command == 'visualize':
        visualize_state(args.state_file, args.step, args.output_md)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main() 