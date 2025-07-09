# src/haive.core/utils/logging.py

import logging
from pathlib import Path


def setup_test_logger(
    test_file_path: str | Path,
    test_name: str | None = None,
    log_dir: str = "logs/tests",
) -> logging.Logger:
    """Set up a logger for tests with file-specific log files.

    Args:
        test_file_path: Path to the test file
        test_name: Optional specific test name
        log_dir: Base directory for log files

    Returns:
        Configured logger
    """
    # Create logs directory structure
    log_base_dir = Path(log_dir)
    log_base_dir.mkdir(parents=True, exist_ok=True)

    # Convert path to Path object if it's a string
    file_path = Path(test_file_path)

    # Get project root (up from tests directory)
    try:
        rel_path = file_path.relative_to(Path.cwd())
    except ValueError:
        rel_path = file_path

    # Create directory structure matching test file hierarchy
    test_log_dir = log_base_dir / rel_path.parent
    test_log_dir.mkdir(parents=True, exist_ok=True)

    # Create log file name
    base_name = file_path.stem
    if test_name:
        log_file_name = f"{base_name}.{test_name}.log"
    else:
        log_file_name = f"{base_name}.log"

    log_file_path = test_log_dir / log_file_name

    # Create logger
    logger_name = f"test.{base_name}"
    if test_name:
        logger_name = f"{logger_name}.{test_name}"

    logger = logging.getLogger(logger_name)

    # Clear previous handlers
    for handler in list(logger.handlers):
        logger.removeHandler(handler)

    # Set up file handler
    file_handler = logging.FileHandler(log_file_path, mode="w")
    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)8s] %(name)s: %(message)s (%(filename)s:%(lineno)s)"
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    # Set logger level
    logger.setLevel(logging.DEBUG)

    logger.debug(f"Logger initialized for {logger_name}")

    return logger
