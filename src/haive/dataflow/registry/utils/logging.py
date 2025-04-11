"""
Logging utilities for the Haive Registry System.

This module provides logging utilities for the registry system,
including setup functions for various log types.
"""

import logging
import os
from pathlib import Path
from typing import Optional, Dict, Any

# Default log directory
DEFAULT_LOG_DIR = Path.cwd() / "logs" / "registry"


def setup_logger(
    name: str,
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    format_str: Optional[str] = None,
    log_to_console: bool = True
) -> logging.Logger:
    """
    Set up a logger with file and optional console handlers.
    
    Args:
        name: Logger name
        log_file: Optional path to log file
        level: Logging level
        format_str: Optional format string for log messages
        log_to_console: Whether to log to console
        
    Returns:
        Configured logger
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Set format
    if format_str is None:
        format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(format_str)
    
    # Add file handler if log_file is provided
    if log_file:
        # Create directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Add console handler if requested
    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger


def setup_discovery_logger(subtype: Optional[str] = None) -> logging.Logger:
    """
    Set up a logger for discovery operations.
    
    Args:
        subtype: Optional subtype (e.g., 'agents', 'tools')
        
    Returns:
        Configured logger
    """
    # Set up base dir
    log_dir = DEFAULT_LOG_DIR / "discovery"
    os.makedirs(log_dir, exist_ok=True)
    
    # Create log file path
    if subtype:
        log_file = log_dir / f"{subtype}.log"
        logger_name = f"haive.registry.discovery.{subtype}"
    else:
        log_file = log_dir / "discovery.log"
        logger_name = "haive.registry.discovery"
    
    # Set up and return logger
    return setup_logger(
        name=logger_name,
        log_file=str(log_file),
        level=logging.DEBUG,
        log_to_console=False
    )


def setup_import_logger() -> logging.Logger:
    """
    Set up a logger for import operations.
    
    Returns:
        Configured logger
    """
    # Set up base dir
    log_dir = DEFAULT_LOG_DIR / "import"
    os.makedirs(log_dir, exist_ok=True)
    
    # Create log file path
    log_file = log_dir / "import.log"
    
    # Set up and return logger
    return setup_logger(
        name="haive.registry.import",
        log_file=str(log_file),
        level=logging.DEBUG,
        log_to_console=False
    )


def setup_operation_logger() -> logging.Logger:
    """
    Set up a logger for registry operations.
    
    Returns:
        Configured logger
    """
    # Set up base dir
    log_dir = DEFAULT_LOG_DIR / "operations"
    os.makedirs(log_dir, exist_ok=True)
    
    # Create log file path
    log_file = log_dir / "operations.log"
    
    # Set up and return logger
    return setup_logger(
        name="haive.registry.operations",
        log_file=str(log_file),
        level=logging.INFO,
        log_to_console=True
    )


def log_entity_operation(
    logger: logging.Logger,
    operation: str,
    entity_type: str,
    entity_name: str,
    entity_id: Optional[str] = None,
    status: str = "success",
    details: Optional[Dict[str, Any]] = None,
    error: Optional[Exception] = None
) -> None:
    """
    Log an entity operation with standardized format.
    
    Args:
        logger: Logger to use
        operation: Operation being performed (e.g., 'register', 'update')
        entity_type: Type of entity
        entity_name: Name of entity
        entity_id: Optional ID of entity
        status: Operation status ('success' or 'failure')
        details: Optional additional details
        error: Optional exception if operation failed
    """
    log_entry = {
        "operation": operation,
        "entity_type": entity_type,
        "entity_name": entity_name,
        "status": status
    }
    
    if entity_id:
        log_entry["entity_id"] = entity_id
    
    if details:
        log_entry["details"] = details
    
    if error:
        log_entry["error"] = str(error)
        if hasattr(error, "__traceback__"):
            import traceback
            log_entry["traceback"] = traceback.format_exc()
    
    # Format message
    message = f"{operation.upper()} {entity_type} '{entity_name}'"
    if entity_id:
        message += f" (ID: {entity_id})"
    message += f" - {status.upper()}"
    
    if error:
        message += f": {str(error)}"
    
    # Log with appropriate level
    if status == "success":
        logger.info(message, extra={"log_entry": log_entry})
    else:
        logger.error(message, extra={"log_entry": log_entry})