#!/usr/bin/env python3
"""
Example script that demonstrates running the KYC agent,
saving state history, and visualizing results.
"""

import os
import sys
import logging
import time
import traceback
from datetime import datetime
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent.parent.parent))

from src.haive.prebuilt.priv.kyc.agent import KYCReportAgent
from src.haive.prebuilt.priv.kyc.config import KYCReportConfig

# Set up logging to both console and file
log_file = "kyc_example_run.log"
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_file, mode='w')  # Overwrite the log file
    ]
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def run_example():
    """Run a complete example of the KYC agent with visualization."""
    try:
        logger.debug("Starting run_example() function")
        
        # Create output directories if they don't exist
        try:
            script_dir = Path(__file__).resolve().parent
            output_dir = script_dir / "outputs"
            output_dir.mkdir(exist_ok=True)
            logger.debug(f"Created output directory: {output_dir}")
        except Exception as e:
            logger.error(f"Error creating output directory: {e}")
            return False
        
        # Generate timestamp for file naming
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Example input text
        input_text = """
        We need to perform a KYC assessment for Crypto Exchange Ltd, a cryptocurrency exchange 
        based in Singapore. They were founded in 2019 and offer trading services for Bitcoin, 
        Ethereum, and various altcoins. The company claims to have implemented KYC/AML procedures 
        and operates with proper licensing in Singapore.
        Their website is https://example.com/crypto-exchange
        """
        
        logger.info("Creating KYC agent...")
        try:
            # Create a configuration for the KYC agent
            config = KYCReportConfig()
            agent = KYCReportAgent(config=config)
            logger.debug("KYC agent created successfully")
        except Exception as e:
            logger.error(f"Error creating KYC agent: {e}")
            logger.error(traceback.format_exc())
            return False
        
        # File paths for outputs
        state_history_path = str(output_dir / f"state_history_{timestamp}.json")
        report_path = str(output_dir / f"report_{timestamp}.md")
        logger.debug(f"State history will be saved to: {state_history_path}")
        logger.debug(f"Report will be saved to: {report_path}")
        
        # Run the agent
        logger.info("Running KYC assessment...")
        start_time = time.time()
        
        # Step 1: Run the agent
        try:
            logger.info("Starting agent.run()")
            final_state = agent.run({"input_text": input_text})
            logger.info("agent.run() completed successfully")
            logger.debug(f"Final state keys: {final_state.keys() if isinstance(final_state, dict) else 'Not a dict'}")
        except Exception as e:
            logger.error(f"Error running KYC agent: {e}")
            logger.error(traceback.format_exc())
            return False
        
        # Step 2: Save state history
        try:
            logger.info("Attempting to save state history...")
            history_path = agent.save_state_history(state_history_path)
            logger.info(f"State history saved to {history_path}")
        except Exception as e:
            logger.error(f"Error saving state history: {e}")
            logger.error(traceback.format_exc())
            # Continue even if saving state history fails
        
        # Step 3: Generate markdown report
        try:
            logger.info("Generating markdown report...")
            report = agent.generate_markdown_report(final_state)
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(report)
            logger.info(f"Markdown report saved to {report_path}")
        except Exception as e:
            logger.error(f"Error generating markdown report: {e}")
            logger.error(traceback.format_exc())
            # Continue even if generating report fails
        
        # Step 4: Visualize the final state
        try:
            logger.info("\nVisualizing final state:")
            agent.visualize_state(final_state)
            logger.info("State visualization completed")
        except Exception as e:
            logger.error(f"Error visualizing state: {e}")
            logger.error(traceback.format_exc())
            # Continue even if visualization fails
        
        # Display execution information
        execution_time = time.time() - start_time
        logger.info(f"\nExecution completed in {execution_time:.2f} seconds")
        logger.info(f"State history saved to: {state_history_path}")
        logger.info(f"Markdown report saved to: {report_path}")
        logger.info(f"Log file: {log_file}")
        
        # Show how to use the CLI to visualize this state later
        logger.info("\nTo visualize this state later, run:")
        logger.info(f"python -m src.haive.prebuilt.priv.kyc.cli visualize {state_history_path}")
        logger.info("\nTo generate a markdown report from this state, run:")
        logger.info(f"python -m src.haive.prebuilt.priv.kyc.cli visualize {state_history_path} -m output.md")
        
        return True
    except Exception as e:
        logger.error(f"Unexpected error in run_example: {e}")
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    try:
        success = run_example()
        if success:
            logger.info("Example completed successfully")
        else:
            logger.error("Example failed")
            sys.exit(1)
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        logger.critical(traceback.format_exc())
        sys.exit(1) 