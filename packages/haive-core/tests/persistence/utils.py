import logging
import os
import uuid
from typing import Any, Dict


# Configure detailed logging
def setup_test_logging():
    """Set up detailed logging for tests."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )

    # Set specific loggers to DEBUG level
    for logger_name in [
        "src.haive.core.engine.agent.persistence",
        "tests.persistence",
        "langgraph.checkpoint",
    ]:
        logging.getLogger(logger_name).setLevel(logging.DEBUG)

    return logging.getLogger("tests.persistence")


# Get database connection parameters from environment or use defaults
def get_db_params() -> dict[str, Any]:
    """Get database parameters from environment variables or defaults."""
    return {
        "db_host": os.environ.get("TEST_DB_HOST", "localhost"),
        "db_port": int(os.environ.get("TEST_DB_PORT", "5432")),
        "db_name": os.environ.get("TEST_DB_NAME", "postgres"),
        "db_user": os.environ.get("TEST_DB_USER", "postgres"),
        "db_pass": os.environ.get("TEST_DB_PASS", "postgres"),
        "ssl_mode": os.environ.get("TEST_DB_SSL_MODE", "disable"),
    }


# Generate a unique thread ID for testing
def generate_thread_id(prefix: str = "test") -> str:
    """Generate a unique thread ID for testing."""
    return f"{prefix}_{uuid.uuid4().hex}"


# Clean up test threads
def cleanup_threads(checkpointer: Any, thread_ids: list):
    """Clean up test threads from database."""
    for thread_id in thread_ids:
        try:
            checkpointer.delete_thread(thread_id)
        except Exception as e:
            logging.warning(f"Failed to delete thread {thread_id}: {e}")


async def cleanup_threads_async(checkpointer: Any, thread_ids: list):
    """Clean up test threads from database asynchronously."""
    for thread_id in thread_ids:
        try:
            await checkpointer.adelete_thread(thread_id)
        except Exception as e:
            logging.warning(f"Failed to delete thread {thread_id}: {e}")


# Simple state for testing
class SimpleState(dict):
    """Simple dictionary-based state for testing."""
