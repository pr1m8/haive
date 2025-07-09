import os
from typing import ClassVar, List
from unittest.mock import ANY, MagicMock, patch

import pytest
from pydantic import Field

from haive.core.engine.agent.agent import Agent, register_agent
from haive.core.engine.agent.config import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.base import EngineType
from haive.core.graph.node.config import NodeConfig


# Configuration class for test agent - renamed to avoid pytest collection error
class AgentConfigForTests(AgentConfig):
    """Test agent configuration for tests."""

    # In Pydantic v2, we need to annotate the field even when overriding
    engine_type: ClassVar[EngineType] = EngineType.AGENT

    def create_runnable(self, runnable_config=None):
        """Create a runnable using the configured engine."""
        if self.engine:
            return self.engine.create_runnable(runnable_config)
        return None


# Agent implementation class - renamed to avoid pytest collection error
@register_agent(AgentConfigForTests)
class AgentForTests(Agent):
    """Test agent implementation for testing."""

    def setup_workflow(self):
        """Implement required abstract method with a simple workflow."""
        # Use mock implementation to avoid actual graph manipulation
        # This prevents the 'START' node error during testing
        pass


# Test fixtures
@pytest.fixture
def test_engine():
    """Create a test AugLLM engine instance."""
    return AugLLMConfig(
        name="test_engine",
        model="gpt-3.5-turbo",  # Use any model name, won't be called in tests
    )


@pytest.fixture
def node_engine():
    """Create a test AugLLM engine for node testing."""
    return AugLLMConfig(
        name="node_engine",
        model="gpt-4",  # Use any model name, won't be called in tests
    )


@pytest.fixture
def agent_config(test_engine):
    """Create a basic agent config for tests."""
    config = AgentConfigForTests(
        name="test_agent",
        engine=test_engine,
        visualize=False,  # Disable visualization for tests
        debug=True,
        output_dir="test_output",  # Use a test directory
        persistence=None,  # Disable persistence for tests
    )
    return config


@pytest.fixture
def setup_checkpointer_mock():
    """Mock the setup_checkpointer function."""
    with patch("haive.core.engine.agent.agent.setup_checkpointer") as mock:
        mock.return_value = MagicMock()
        yield mock


@pytest.fixture
def ensure_pool_open_mock():
    """Mock the ensure_pool_open function."""
    with patch("haive.core.engine.agent.agent.ensure_pool_open") as mock:
        mock.return_value = None
        yield mock


@pytest.fixture
def close_pool_if_needed_mock():
    """Mock the close_pool_if_needed function."""
    with patch("haive.core.engine.agent.agent.close_pool_if_needed") as mock:
        yield mock


@pytest.fixture
def register_thread_if_needed_mock():
    """Mock the register_thread_if_needed function."""
    with patch("haive.core.engine.agent.agent.register_thread_if_needed") as mock:
        yield mock


@pytest.fixture
def prepare_merged_input_mock():
    """Mock the prepare_merged_input function."""
    with patch("haive.core.engine.agent.agent.prepare_merged_input") as mock:
        mock.return_value = {"input": "processed"}
        yield mock


@pytest.fixture
def mock_derive_schema():
    """Mock the derive_schema method to avoid node_config issues."""
    with patch.object(AgentConfigForTests, "derive_schema") as mock:
        # Return a simple BaseModel class as the schema
        from pydantic import create_model

        mock.return_value = create_model("TestSchema", messages=(List, []))
        yield mock


# We need to create a proper mock for DynamicGraph to handle START/END constants
@pytest.fixture
def mock_dynamic_graph():
    """Create a comprehensive mock for DynamicGraph class."""
    mock_graph = MagicMock()

    # Create a properly configured mock that returns itself when instantiated
    mock_graph_instance = MagicMock()
    mock_graph_instance.add_node = MagicMock()
    mock_graph_instance.add_edge = MagicMock()
    mock_graph_instance.compile = MagicMock(return_value=MagicMock())
    mock_graph_instance.visualize_graph = MagicMock()

    # Configure the class mock to return the instance when called
    mock_graph.return_value = mock_graph_instance

    return mock_graph


# Mock for the setup_workflow method to avoid START/END node issues
@pytest.fixture
def mock_setup_workflow():
    with patch.object(AgentForTests, "setup_workflow") as mock:
        yield mock


class TestAgentClass:
    """Tests for the Agent base class."""

    def test_initialization(
        self,
        agent_config,
        setup_checkpointer_mock,
        mock_dynamic_graph,
        mock_setup_workflow,
        mock_derive_schema,
    ):
        """Test basic agent initialization."""
        # Mock DynamicGraph to prevent graph building issues
        with patch("haive.core.engine.agent.agent.DynamicGraph", mock_dynamic_graph):
            agent = AgentForTests(agent_config)

            # Check basic attributes
            assert agent.config == agent_config
            assert agent.engine_config is not None
            assert "main" in agent.engine_configs
            assert agent.runnable_config is not None

            # Check that schema initialization happened
            assert agent.state_schema is not None
            assert agent.input_schema is not None
            assert agent.output_schema is not None

            # Check checkpointer setup called
            setup_checkpointer_mock.assert_called_once_with(agent_config)

            # Check graph initialization happened
            mock_dynamic_graph.assert_called_once()

            # Check compile was called (via __init__)
            assert agent.app is not None

    def test_directory_creation(
        self,
        agent_config,
        setup_checkpointer_mock,
        mock_dynamic_graph,
        mock_setup_workflow,
        mock_derive_schema,
    ):
        """Test that necessary directories are created."""
        with patch("haive.core.engine.agent.agent.DynamicGraph", mock_dynamic_graph):
            with patch("os.makedirs") as mock_makedirs:
                AgentForTests(agent_config)

                # Should create output directory
                mock_makedirs.assert_any_call(agent_config.output_dir, exist_ok=True)

                # Should create state history directory
                state_history_dir = os.path.join(
                    agent_config.output_dir, "state_history"
                )
                mock_makedirs.assert_any_call(state_history_dir, exist_ok=True)

                # Should create graphs directory
                graphs_dir = os.path.join(agent_config.output_dir, "graphs")
                mock_makedirs.assert_any_call(graphs_dir, exist_ok=True)

    def test_build_engine(
        self,
        agent_config,
        setup_checkpointer_mock,
        mock_dynamic_graph,
        mock_setup_workflow,
        mock_derive_schema,
    ):
        """Test engine building logic."""
        with patch("haive.core.engine.agent.agent.DynamicGraph", mock_dynamic_graph):
            # Create a mock registry for engine lookup
            with patch("haive.core.engine.base.EngineRegistry") as mock_registry:
                registry_instance = MagicMock()
                mock_registry.get_instance.return_value = registry_instance

                # Mock get method to return a test engine for "string_engine"
                string_engine = AugLLMConfig(name="string_engine", model="gpt-4")

                def mock_get(engine_type, name):
                    if name == "string_engine":
                        return string_engine
                    return None

                registry_instance.get.side_effect = mock_get

                # Create agent with string engine reference
                string_config = AgentConfigForTests(
                    name="string_agent",
                    engine="string_engine",
                    visualize=False,
                    output_dir="test_output",
                )

                agent = AgentForTests(string_config)

                # Should have resolved the string reference to a config (not instantiated)
                assert agent.engine_config is not None
                assert agent.engine_config is string_engine

    def test_create_graph_builder(
        self,
        agent_config,
        setup_checkpointer_mock,
        mock_dynamic_graph,
        mock_setup_workflow,
        mock_derive_schema,
    ):
        """Test graph builder creation."""
        with patch("haive.core.engine.agent.agent.DynamicGraph", mock_dynamic_graph):
            AgentForTests(agent_config)

            # Check graph initialization called with appropriate parameters
            mock_dynamic_graph.assert_called_once()
            call_kwargs = mock_dynamic_graph.call_args[1]
            assert call_kwargs["name"] == agent_config.name
            assert "components" in call_kwargs
            assert "state_schema" in call_kwargs
            assert call_kwargs["visualize"] == agent_config.visualize

    def test_apply_node_configs(
        self,
        agent_config,
        node_engine,
        setup_checkpointer_mock,
        mock_dynamic_graph,
        mock_setup_workflow,
        mock_derive_schema,
    ):
        """Test that node configs are applied."""
        # Add a node config to the agent config using NodeConfig instead of dict
        # Create a proper NodeConfig instance
        node_config = NodeConfig(
            name="custom_node", engine=node_engine, command_goto="END"
        )

        # Assign the NodeConfig to the agent_config
        if hasattr(agent_config, "node_configs"):
            agent_config.node_configs = {"custom_node": node_config}

        with patch("haive.core.engine.agent.agent.DynamicGraph", mock_dynamic_graph):
            # Instead of patching the method at module level, we'll patch the method on the Agent class
            with patch.object(
                AgentForTests, "_apply_node_configs", MagicMock()
            ) as mock_apply:
                AgentForTests(agent_config)

                # Check that _apply_node_configs was called
                mock_apply.assert_called_once()

    def test_compile(
        self,
        agent_config,
        setup_checkpointer_mock,
        mock_dynamic_graph,
        mock_setup_workflow,
        mock_derive_schema,
    ):
        """Test graph compilation."""
        with patch("haive.core.engine.agent.agent.DynamicGraph", mock_dynamic_graph):
            agent = AgentForTests(agent_config)

            # Reset the mock to clear initialization calls
            graph_instance = mock_dynamic_graph.return_value
            graph_instance.compile.reset_mock()

            # Recompile to test the method
            agent.compile()

            # Check compile was called on the graph
            graph_instance.compile.assert_called_once()

    def test_prepare_runnable_config(
        self,
        agent_config,
        setup_checkpointer_mock,
        mock_dynamic_graph,
        mock_setup_workflow,
        mock_derive_schema,
    ):
        """Test preparation of runnable config."""
        with patch("haive.core.engine.agent.agent.DynamicGraph", mock_dynamic_graph):
            agent = AgentForTests(agent_config)

            # Test with thread_id
            config1 = agent._prepare_runnable_config(thread_id="test-thread")
            assert config1["configurable"]["thread_id"] == "test-thread"

            # Test with explicit config
            base_config = {"configurable": {"user_id": "test-user"}}
            config2 = agent._prepare_runnable_config(config=base_config)
            assert config2["configurable"]["user_id"] == "test-user"

    def test_save_state_history(
        self,
        agent_config,
        setup_checkpointer_mock,
        mock_dynamic_graph,
        mock_setup_workflow,
        mock_derive_schema,
    ):
        """Test saving state history."""
        # Create mock app that returns state
        mock_app = MagicMock()
        mock_app.get_state.return_value = {"state": "test"}

        with patch("haive.core.engine.agent.agent.DynamicGraph", mock_dynamic_graph):
            # Need to patch the ensure_json_serializable function which might be in a different module
            with patch(
                "haive.core.utils.pydantic_utils.ensure_json_serializable",
                return_value={"state": "test"},
            ):
                with patch("builtins.open", new_callable=MagicMock()) as mock_open:
                    with patch("json.dump") as mock_dump:
                        agent = AgentForTests(agent_config)
                        agent.app = mock_app

                        # Call save_state_history
                        agent.save_state_history()

                        # Check appropriate functions were called
                        mock_app.get_state.assert_called_once()
                        mock_open.assert_called_once()
                        mock_dump.assert_called_once()

    def test_run(
        self,
        agent_config,
        setup_checkpointer_mock,
        mock_dynamic_graph,
        ensure_pool_open_mock,
        close_pool_if_needed_mock,
        register_thread_if_needed_mock,
        prepare_merged_input_mock,
        mock_setup_workflow,
        mock_derive_schema,
    ):
        """Test agent run method."""
        # Create a mock app
        mock_app = MagicMock()
        mock_app.get_state.return_value = {"previous": "state"}
        mock_app.invoke.return_value = {"result": "success"}

        with patch("haive.core.engine.agent.agent.DynamicGraph", mock_dynamic_graph):
            agent = AgentForTests(agent_config)

            # Replace app with our mock
            agent.app = mock_app

            # Mock save_state_history
            agent.save_state_history = MagicMock()

            # Run the agent
            result = agent.run({"input": "test"}, thread_id="test-thread")

            # Check results
            assert result == {"result": "success"}

            # Check proper calls were made
            register_thread_if_needed_mock.assert_called_once()
            ensure_pool_open_mock.assert_called_once()
            prepare_merged_input_mock.assert_called_once()
            mock_app.invoke.assert_called_once()
            agent.save_state_history.assert_called_once()

    def test_stream(
        self,
        agent_config,
        setup_checkpointer_mock,
        mock_dynamic_graph,
        ensure_pool_open_mock,
        close_pool_if_needed_mock,
        register_thread_if_needed_mock,
        prepare_merged_input_mock,
        mock_setup_workflow,
        mock_derive_schema,
    ):
        """Test agent stream method."""
        # Create mock app with streaming capability
        mock_app = MagicMock()
        mock_app.get_state.return_value = {"previous": "state"}
        mock_app.stream.return_value = [{"step1": "data"}, {"step2": "data"}]

        with patch("haive.core.engine.agent.agent.DynamicGraph", mock_dynamic_graph):
            agent = AgentForTests(agent_config)
            agent.app = mock_app

            # Mock save_state_history
            agent.save_state_history = MagicMock()

            # Stream from the agent
            results = list(
                agent.stream(
                    {"input": "test"}, thread_id="test-thread", stream_mode="updates"
                )
            )

            # Check results
            assert len(results) == 2
            assert results[0] == {"step1": "data"}
            assert results[1] == {"step2": "data"}

            # Check proper calls were made
            register_thread_if_needed_mock.assert_called_once()
            ensure_pool_open_mock.assert_called_once()
            prepare_merged_input_mock.assert_called_once()
            mock_app.stream.assert_called_once_with(
                {"input": "processed"},
                stream_mode="updates",
                config=ANY,
                debug=agent_config.debug,
            )
            agent.save_state_history.assert_called_once()


# Simple test for the decorator without using any mocks
def test_register_agent_decorator():
    """Test the register_agent decorator."""

    # Define a test config class
    class CustomTestConfig(AgentConfig):
        engine_type: ClassVar[EngineType] = EngineType.AGENT

        def create_runnable(self, runnable_config=None):
            return MagicMock()

    # Define and register a test agent class
    @register_agent(CustomTestConfig)
    class CustomTestAgent(Agent):
        def setup_workflow(self):
            pass

    # Check that it was registered
    from haive.core.engine.agent.agent import AGENT_REGISTRY

    assert AGENT_REGISTRY[CustomTestConfig] == CustomTestAgent
