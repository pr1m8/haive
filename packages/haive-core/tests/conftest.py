"""Configuration file for pytest with rich logging and test setup."""

import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest
from langchain_core.runnables import RunnableConfig
from pydantic import Field
from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install

# Install rich traceback handler
install(show_locals=True)

# Create rich console
console = Console()

# Import Haive core components
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.base import (
    Engine,
    EngineType,
    InvokableEngine,
    NonInvokableEngine,
)
from haive.core.engine.embeddings import EmbeddingsEngineConfig
from haive.core.engine.retriever import BaseRetrieverConfig, RetrieverType
from haive.core.engine.vectorstore.vectorstore import (
    VectorStoreConfig,
    VectorStoreProvider,
)
from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig
from haive.core.models.llm.base import AzureLLMConfig


# Configure root logger with rich handler
def setup_logging():
    """Configure root logger with rich formatting."""
    # Create a rich handler
    rich_handler = RichHandler(
        rich_tracebacks=True, markup=True, show_path=False, enable_link_path=True
    )

    # Instead of configuring the root logger, create a specific logger for conftest
    conftest_logger = logging.getLogger("conftest")
    conftest_logger.setLevel(logging.DEBUG)
    conftest_logger.addHandler(rich_handler)

    # By default, a logger propagates its logs to the root logger.
    # Disable this to prevent affecting other loggers
    conftest_logger.propagate = False

    return conftest_logger


# Get logger for conftest
conftest_logger = setup_logging()


def pytest_configure(config):
    """Set up test session configuration."""
    # Create logs directory structure
    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = Path("logs/runs") / run_timestamp
    run_dir.mkdir(parents=True, exist_ok=True)

    # Store run directory in config for later use
    config.run_dir = run_dir

    # Update latest symlink
    latest_link = Path("logs/latest")
    try:
        if latest_link.exists():
            latest_link.unlink()
        latest_link.symlink_to(run_dir, target_is_directory=True)
    except (OSError, NotImplementedError):
        conftest_logger.warning("Failed to create 'latest' symlink")


@pytest.fixture(scope="session")
def run_dir(pytestconfig):
    """Provide access to the run directory."""
    return pytestconfig.run_dir


def generate_test_id(prefix: str) -> str:
    """Generate a unique test identifier."""
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


import asyncio
import sys

import pytest

# Configure pytest-asyncio
pytest_plugins = ["pytest_asyncio"]


@pytest.fixture(scope="session")
def event_loop_policy():
    """Configure the event loop policy for the test session."""
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    return asyncio.get_event_loop_policy()


@pytest.fixture
def event_loop(event_loop_policy):
    """Create an instance of the default event loop for each test case."""
    loop = event_loop_policy.new_event_loop()
    yield loop
    # Close the loop
    if loop.is_running():
        loop.call_soon_threadsafe(loop.stop)
    loop.close()


# Helper for creating proper async mock returns
@pytest.fixture
def async_return():
    """Creates proper async return values for mocks."""

    def _async_return(return_value):
        async def _async_result(*args, **kwargs):
            return return_value

        return _async_result()

    return _async_return


# --------------------------------------------------------------------
# Mock Engine Classes
# --------------------------------------------------------------------


class MockEngine(Engine):
    """Mock engine for testing."""

    engine_type: EngineType = EngineType.LLM
    id: str = Field(default_factory=lambda: generate_test_id("mock-engine"))
    name: str = Field(default_factory=lambda: f"mock_engine_{uuid.uuid4().hex[:4]}")

    def create_runnable(self, runnable_config: RunnableConfig | None = None) -> Any:
        conftest_logger.debug(
            f"[blue]MockEngine[/blue] '{self.name}' create_runnable called"
        )
        return lambda x: x


class MockInvokableEngine(InvokableEngine):
    """Mock invokable engine for testing."""

    engine_type: EngineType = EngineType.LLM
    id: str = Field(default_factory=lambda: generate_test_id("mock-invokable"))
    name: str = Field(
        default_factory=lambda: f"mock_invokable_engine_{uuid.uuid4().hex[:4]}"
    )

    def create_runnable(self, runnable_config: RunnableConfig | None = None) -> Any:
        conftest_logger.debug(
            f"[green]MockInvokableEngine[/green] '{self.name}' create_runnable called"
        )
        return self

    def invoke(
        self, input_data: Any, runnable_config: RunnableConfig | None = None
    ) -> Any:
        conftest_logger.debug(
            f"[green]MockInvokableEngine[/green] '{self.name}' invoke called"
        )
        if isinstance(input_data, dict):
            return {**input_data, "invoked_by": self.name}
        return {"result": input_data, "invoked_by": self.name}

    async def ainvoke(
        self, input_data: Any, runnable_config: RunnableConfig | None = None
    ) -> Any:
        conftest_logger.debug(
            f"[green]MockInvokableEngine[/green] '{self.name}' ainvoke called"
        )
        return self.invoke(input_data, runnable_config)


class MockNonInvokableEngine(NonInvokableEngine):
    """Mock non-invokable engine for testing."""

    engine_type: EngineType = EngineType.EMBEDDINGS
    id: str = Field(default_factory=lambda: generate_test_id("mock-non-invokable"))
    name: str = Field(
        default_factory=lambda: f"mock_non_invokable_engine_{uuid.uuid4().hex[:4]}"
    )

    def create_runnable(self, runnable_config: RunnableConfig | None = None) -> Any:
        conftest_logger.debug(
            f"[yellow]MockNonInvokableEngine[/yellow] '{self.name}' create_runnable called"
        )
        return {"instance_created_by": self.name}


# --------------------------------------------------------------------
# Engine Fixtures
# --------------------------------------------------------------------


@pytest.fixture
def mock_engine() -> MockEngine:
    """Provide a basic mock engine instance."""
    instance = MockEngine()
    conftest_logger.debug(f"Created [blue]mock_engine[/blue]: {instance.id}")
    return instance


@pytest.fixture
def mock_invokable_engine() -> MockInvokableEngine:
    """Provide a mock invokable engine instance."""
    instance = MockInvokableEngine()
    conftest_logger.debug(
        f"Created [green]mock_invokable_engine[/green]: {instance.id}"
    )
    return instance


@pytest.fixture
def mock_non_invokable_engine() -> MockNonInvokableEngine:
    """Provide a mock non-invokable engine instance."""
    instance = MockNonInvokableEngine()
    conftest_logger.debug(
        f"Created [yellow]mock_non_invokable_engine[/yellow]: {instance.id}"
    )
    return instance


@pytest.fixture
def real_llm_engine():
    """Provide a real LLM engine configuration."""
    return AugLLMConfig(name="test_llm", model="gpt-35")


@pytest.fixture
def real_aug_llm_engine() -> AugLLMConfig:
    """Provide a real augmented LLM engine configuration."""
    return AugLLMConfig(
        name="test_aug_llm", llm_config=AzureLLMConfig(name="base_llm", model="gpt-4o")
    )


@pytest.fixture
def real_embeddings_engine() -> EmbeddingsEngineConfig:
    """Provide a real embeddings engine configuration."""
    return EmbeddingsEngineConfig(
        name="test_embeddings",
        embedding_config=HuggingFaceEmbeddingConfig(
            model="sentence-transformers/all-mpnet-base-v2"
        ),
    )


@pytest.fixture
def real_vectorstore_engine(
    real_embeddings_engine: EmbeddingsEngineConfig,
) -> VectorStoreConfig:
    """Provide a real vector store engine configuration."""
    return VectorStoreConfig(
        name="test_vectorstore",
        vector_store_provider=VectorStoreProvider.FAISS,
        embedding_model=real_embeddings_engine.embedding_config,
    )


@pytest.fixture
def real_retriever_engine(
    real_vectorstore_engine: VectorStoreConfig,
) -> BaseRetrieverConfig:
    """Provide a real retriever engine configuration."""
    return BaseRetrieverConfig(
        name="test_retriever",
        retriever_type=RetrieverType.VECTOR_STORE,
        vector_store_config=real_vectorstore_engine,
    )
