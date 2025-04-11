"""
KYC Report Test for Bitfinex with Detailed Logging and Traceback Handling

This script runs a KYC report generation for Bitfinex cryptocurrency exchange,
capturing detailed logs and traceback information throughout the process.
"""

import logging
import traceback
import sys
import json
import time
import psutil
import threading
from pathlib import Path
from datetime import datetime
from langchain_core.messages import HumanMessage

# Configure detailed logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Create timestamp for log files
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = log_dir / f"kyc_bitfinex_test_{timestamp}.log"

# Configure logger with both file and console output
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

# Create a specific logger for this test
logger = logging.getLogger("kyc_bitfinex_test")
logger.info(f"Starting KYC report test for Bitfinex - Log file: {log_file}")

# Global monitoring variables
system_metrics = []
monitoring_active = True

def monitor_system_resources():
    """Monitor system resources during test execution"""
    process = psutil.Process()
    
    while monitoring_active:
        try:
            # Collect memory usage
            mem_info = process.memory_info()
            cpu_percent = process.cpu_percent(interval=0.1)
            
            # Record metrics
            system_metrics.append({
                'timestamp': datetime.now().isoformat(),
                'memory_rss_mb': mem_info.rss / (1024 * 1024),  # RSS in MB
                'memory_vms_mb': mem_info.vms / (1024 * 1024),  # VMS in MB
                'cpu_percent': cpu_percent,
                'thread_count': len(process.threads())
            })
            
        except Exception as e:
            logger.error(f"Error in resource monitoring: {str(e)}")
        
        # Sleep for monitoring interval
        time.sleep(1)

try:
    # Start resource monitoring in a background thread
    monitor_thread = threading.Thread(target=monitor_system_resources)
    monitor_thread.daemon = True
    monitor_thread.start()
    logger.info("System resource monitoring started")
    
    # Import the agent configuration and modules
    logger.info("Importing required modules")
    
    from src.haive.prebuilt.priv.kyc.config import KYCReportConfig
    from src.haive.prebuilt.priv.kyc.agent import KYCReportAgent  # Import the agent class to ensure it's registered
    from src.haive.core.models.vectorstore.base import VectorStoreConfig
    from src.haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig
    
    # Check if the agent is properly registered
    from src.haive.core.engine.agent.agent import AGENT_REGISTRY
    logger.info(f"Agent registry contents: {list(AGENT_REGISTRY.keys())}")
    
    # Define a function to ensure agent registration
    def ensure_agent_registration():
        """Ensure the KYCReportAgent is registered for KYCReportConfig"""
        if KYCReportConfig not in AGENT_REGISTRY:
            logger.warning("KYCReportConfig not found in registry, registering it manually")
            # Re-import to ensure decorator is processed
            from src.haive.prebuilt.priv.kyc.agent import KYCReportAgent
            # Force registration if needed
            AGENT_REGISTRY[KYCReportConfig] = KYCReportAgent
        
        logger.info(f"KYCReportConfig registration status: {KYCReportConfig in AGENT_REGISTRY}")
        logger.info(f"Registered agent class: {AGENT_REGISTRY.get(KYCReportConfig)}")
    
    # Function to log agent state during execution
    def log_state_update(step_name, state_update):
        """Log a simplified view of state updates for debugging"""
        logger.debug(f"State update after {step_name}:")
        # Only log certain keys to avoid excessive output
        keys_to_log = ['current_step', 'current_section_index', 'error', 'query']
        logged_state = {k: v for k, v in state_update.items() if k in keys_to_log}
        logger.debug(json.dumps(logged_state, default=str))
    
    # Create a function to run the test with detailed logging
    def run_kyc_test_for_bitfinex():
        """Run KYC Report generation for Bitfinex with detailed logging"""
        logger.info("Setting up embedding and vector store configurations")
        
        # Create embedding configuration
        embedding_config = HuggingFaceEmbeddingConfig(
            model="sentence-transformers/all-mpnet-base-v2"
        )
        
        # Create vector store configuration
        vectorstore_config = VectorStoreConfig(
            embedding_model=embedding_config,
            vector_store_path="kyc_bitfinex_vector_store"
        )
        
        # Create the KYC report agent configuration with debugging enabled
        logger.info("Creating KYC agent configuration")
        kyc_config = KYCReportConfig.from_scratch(
            name="bitfinex_kyc_agent",
            llm_model="gpt-4o",
            vectorstore_config=vectorstore_config,
            debug=True  # Enable verbose debug logs
        )
        
        # Ensure agent registration right before building
        ensure_agent_registration()
        
        # Build the agent with logging callback
        logger.info("Building KYC agent")
        start_time = time.time()
        kyc_agent = kyc_config.build_agent()
        logger.info(f"Agent built in {time.time() - start_time:.2f} seconds")
        
        # Prepare input about Bitfinex
        bitfinex_input = """
        I need to do a KYC risk assessment for Bitfinex.
        
        Bitfinex is a cryptocurrency exchange headquartered in Hong Kong and registered in the British Virgin Islands.
        Their website is https://www.bitfinex.com/
        
        They offer trading of cryptocurrencies including Bitcoin, Ethereum, and others. They also offer margin trading
        and lending services. I need to determine their risk level according to our compliance standards, especially
        regarding cryptocurrency exchanges and their regulatory compliance.
        
        Please research their business thoroughly including any regulatory issues, legal problems, or compliance concerns.
        """
        
        # Create input message and additional context
        input_message = HumanMessage(content=bitfinex_input)
        additional_context = """
        Pay special attention to anti-money laundering (AML) compliance, know-your-customer (KYC) practices, 
        and any past regulatory actions or concerns. Cryptocurrency exchanges are considered high-risk entities
        in our risk framework.
        """
        
        # Log input details
        logger.info(f"Input message length: {len(bitfinex_input)} characters")
        logger.info(f"Additional context length: {len(additional_context)} characters")
        
        # Add custom exception handler to capture detailed errors
        original_run = kyc_agent.run
        
        def run_with_logging(*args, **kwargs):
            """Wrapper to add logging to agent.run method"""
            logger.info("Starting agent execution")
            try:
                step_start = time.time()
                result = original_run(*args, **kwargs)
                logger.info(f"Agent execution completed in {time.time() - step_start:.2f} seconds")
                return result
            except Exception as e:
                logger.error(f"Error during agent execution: {str(e)}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                raise
        
        # Replace run method with logging version
        kyc_agent.run = run_with_logging
        
        # Run the agent with timing
        logger.info("Running KYC report generation")
        overall_start = time.time()
        
        # Create progress tracking callback
        def progress_callback(state):
            """Callback to track progress during agent execution"""
            current_step = state.get("current_step", "unknown")
            section_index = state.get("current_section_index")
            
            section_name = "N/A"
            if section_index is not None and hasattr(state, "report_sections") and len(state.report_sections) > section_index:
                section_name = state.report_sections[section_index].name
            
            logger.info(f"Progress update - Step: {current_step}, Section: {section_name}")
            
            # Log any errors
            if "error" in state and state["error"]:
                logger.error(f"Error in state: {state['error']}")
            
            return state
        
        try:
            result = kyc_agent.run(
                {
                    "messages": [input_message],
                    "input_context": additional_context
                }
            )
            
            # Log success details
            overall_time = time.time() - overall_start
            logger.info(f"KYC report generation completed successfully in {overall_time:.2f} seconds")
            
            # Log key results
            if hasattr(result, "risk_category"):
                logger.info(f"Risk Category: {result.risk_category}")
            
            if hasattr(result, "kyc_decision") and hasattr(result.kyc_decision, "proceed"):
                logger.info(f"KYC Decision: {'Proceed' if result.kyc_decision.proceed else 'Do Not Proceed'}")
            
            # Save the final report
            if hasattr(result, "final_report") and result.final_report:
                report_path = Path(f"bitfinex_kyc_report_{timestamp}.md")
                with open(report_path, "w") as f:
                    f.write(result.final_report)
                logger.info(f"Final report saved to {report_path}")
            
            # Save full result state for detailed analysis
            state_path = Path(f"bitfinex_kyc_state_{timestamp}.json")
            with open(state_path, "w") as f:
                # Convert to dict for serialization
                result_dict = result.dict() if hasattr(result, "dict") else {
                    k: str(v) for k, v in result.__dict__.items() 
                    if not k.startswith("_")
                }
                
                # Remove messages for cleaner output
                if "messages" in result_dict:
                    result_dict["messages"] = f"[{len(result_dict['messages'])} messages removed for brevity]"
                    
                json.dump(result_dict, f, indent=2, default=str)
            
            logger.info(f"Complete result state saved to {state_path}")
            
            return result
            
        except Exception as e:
            logger.critical(f"KYC report generation failed: {str(e)}")
            logger.critical(f"Detailed traceback: {traceback.format_exc()}")
            raise
    
    # Run the test
    result = run_kyc_test_for_bitfinex()
    logger.info("Test completed successfully")
    
except ImportError as e:
    logger.critical(f"Module import error: {str(e)}")
    logger.critical(f"This may indicate the Haive framework is not properly installed or set up")
    logger.critical(f"Traceback: {traceback.format_exc()}")
    sys.exit(1)
    
except Exception as e:
    logger.critical(f"Unexpected error in test script: {str(e)}")
    logger.critical(f"Traceback: {traceback.format_exc()}")
    sys.exit(1)
    
finally:
    # Log test completion regardless of outcome
    logger.info(f"Test script execution finished. See log file for details: {log_file}")
    
    # Analyze logs and provide test metrics
    def analyze_logs(log_file_path):
        """Analyze log file and extract useful metrics about the test run"""
        logger.info("Analyzing log file for test metrics")
        
        try:
            with open(log_file_path, 'r') as f:
                log_lines = f.readlines()
            
            # Initialize metrics
            metrics = {
                'total_lines': len(log_lines),
                'error_count': 0,
                'warning_count': 0,
                'debug_count': 0,
                'info_count': 0,
                'critical_count': 0,
                'execution_times': [],
                'steps_executed': set(),
                'errors': []
            }
            
            # Process logs
            for line in log_lines:
                # Count log levels
                if ' - ERROR - ' in line:
                    metrics['error_count'] += 1
                    # Extract error message
                    error_msg = line.split(' - ERROR - ')[-1].strip()
                    metrics['errors'].append(error_msg)
                elif ' - WARNING - ' in line:
                    metrics['warning_count'] += 1
                elif ' - DEBUG - ' in line:
                    metrics['debug_count'] += 1
                elif ' - INFO - ' in line:
                    metrics['info_count'] += 1
                elif ' - CRITICAL - ' in line:
                    metrics['critical_count'] += 1
                
                # Extract execution times
                if 'completed in ' in line:
                    try:
                        time_str = line.split('completed in ')[-1].split(' seconds')[0]
                        metrics['execution_times'].append(float(time_str))
                    except (ValueError, IndexError):
                        pass
                
                # Extract steps
                if 'State update after ' in line:
                    try:
                        step = line.split('State update after ')[1].split(':')[0]
                        metrics['steps_executed'].add(step)
                    except (IndexError, ValueError):
                        pass
            
            # Calculate additional metrics
            metrics['total_execution_time'] = sum(metrics['execution_times'])
            metrics['average_step_time'] = (metrics['total_execution_time'] / 
                                           len(metrics['execution_times'])) if metrics['execution_times'] else 0
            metrics['steps_count'] = len(metrics['steps_executed'])
            
            # Print summary report
            print("\n" + "="*50)
            print("TEST EXECUTION SUMMARY")
            print("="*50)
            print(f"Total log lines: {metrics['total_lines']}")
            print(f"Log breakdown: {metrics['info_count']} INFO, {metrics['debug_count']} DEBUG, "
                  f"{metrics['warning_count']} WARNING, {metrics['error_count']} ERROR, "
                  f"{metrics['critical_count']} CRITICAL")
            print(f"Steps executed: {metrics['steps_count']}")
            print(f"Total execution time: {metrics['total_execution_time']:.2f} seconds")
            print(f"Average step time: {metrics['average_step_time']:.2f} seconds")
            
            if metrics['errors']:
                print("\nERRORS ENCOUNTERED:")
                for i, error in enumerate(metrics['errors'][:5]):  # Show first 5 errors
                    print(f"{i+1}. {error}")
                if len(metrics['errors']) > 5:
                    print(f"...and {len(metrics['errors'])-5} more errors (see log file)")
            
            print("="*50)
            print(f"Detailed logs available at: {log_file_path}")
            print("="*50 + "\n")
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error analyzing logs: {str(e)}")
            print(f"Error analyzing logs: {str(e)}")
            return None
    
    # Analyze logs if test completed
    analyze_logs(log_file)

# If script runs directly
if __name__ == "__main__":
    print(f"KYC test for Bitfinex completed. See log file for details: {log_file}")