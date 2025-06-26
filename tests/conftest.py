"""Base configuration and fixtures for pytest with modern rich integration."""

from datetime import UTC, datetime
import logging
from pathlib import Path
import uuid

import pytest
from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install as install_rich_traceback


# Install rich traceback handler
install_rich_traceback(show_locals=True)

# Create rich console for shared use
console = Console()


def setup_logging() -> logging.Logger:
    """Configure root logger with rich formatting."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                rich_tracebacks=True,
                markup=True,
                show_path=False,
                enable_link_path=True,
            )
        ],
    )
    return logging.getLogger("conftest")


# Get logger for conftest
conftest_logger = setup_logging()


def pytest_configure(config: pytest.Config) -> None:
    """Set up test session configuration."""
    # Create logs directory structure
    run_timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    run_dir = Path("logs/runs") / run_timestamp
    run_dir.mkdir(parents=True, exist_ok=True)

    # Store run directory in config for later use
    config.run_dir = run_dir  # type: ignore

    # Update latest symlink
    latest_link = Path("logs/latest")
    try:
        if latest_link.exists():
            latest_link.unlink()
        latest_link.symlink_to(run_dir, target_is_directory=True)
    except (OSError, NotImplementedError):
        conftest_logger.warning("Failed to create 'latest' symlink")


@pytest.fixture(scope="session")
def run_dir(pytestconfig: pytest.Config) -> Path:
    """Provide access to the run directory."""
    return pytestconfig.run_dir  # type: ignore


@pytest.fixture(scope="session")
def workspace_root() -> Path:
    """Provide the workspace root directory."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def package_root() -> Path:
    """Provide the current package root directory."""
    return Path.cwd()


@pytest.fixture(scope="session")
def logs_dir() -> Path:
    """Provide the logs directory."""
    logs = Path("logs")
    logs.mkdir(exist_ok=True)
    return logs


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """Provide the test data directory for the current package."""
    data_dir = Path("tests/data")
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def generate_test_id(prefix: str) -> str:
    """Generate a unique test identifier."""
    return f"{prefix}-{uuid.uuid4().hex[:8]}"
