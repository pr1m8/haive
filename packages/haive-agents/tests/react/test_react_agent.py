# tests/agents/react/test_react_agent.py

import unittest
from unittest.mock import MagicMock, patch

from agents.react.agent import ReactAgent
from agents.react.config import ReactAgentConfig
from haive.core.config.runnable import RunnableConfigManager
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import StructuredTool


# Define tool functions (outside of test class to avoid fixture errors)
def calc_add(a: int, b: int) -> str:
    """Add two numbers."""
    return str(a + b)


def echo_message(message: str) -> str:
    """Echo back the input message."""
    return f"Echo: {message}"


class TestReactAgent(unittest.TestCase):
    """Test suite for the ReactAgent implementation."""

    def setUp(self):
        """Set up test tools and configurations."""
        # Create test tools
        self.tools = [
            StructuredTool.from_function(calc_add),
            StructuredTool.from_function(echo_message),
        ]

        # Create mock LLM
        self.mock_llm = MagicMock()
        self.mock_llm.invoke.return_value = AIMessage(
            content="I'll help you with that."
        )

        # Create mock AugLLMConfig with required attributes
        self.mock_aug_llm = MagicMock(spec=AugLLMConfig)
        self.mock_aug_llm.create_runnable.return_value = self.mock_llm
        self.mock_aug_llm.name = "mock_llm"
        self.mock_aug_llm.tools = []
        self.mock_aug_llm.bind_tools_kwargs = {}

        # IMPORTANT: Add the missing engine_type attribute
        from haive.core.engine.base import EngineType

        self.mock_aug_llm.engine_type = EngineType.LLM

        # Create ReactAgentConfig
        self.agent_config = ReactAgentConfig(
            name="test_react_agent",
            engine=self.mock_aug_llm,
            tools=self.tools,
            system_prompt="You are a helpful AI assistant that can use tools.",
            max_iterations=3,
            version="v1",
        )

        # Patch the setup_workflow to prevent actual graph compilation
        self.original_setup_workflow = ReactAgent.setup_workflow

        # Store and patch the compile method
        self.compile_patcher = patch("haive.agents.react.agent.ReactAgent.compile")
        self.mock_compile = self.compile_patcher.start()

        # Create mock graph
        self.mock_graph = MagicMock()
        self.mock_graph.nodes = [
            "init",
            "add_system",
            "agent",
            "execute_tools",
            "iteration_check",
        ]

    def tearDown(self):
        """Clean up after tests."""
        # Stop patchers
        self.compile_patcher.stop()

    def test_initialization(self):
        """Test proper initialization of ReactAgent."""
        with patch("haive.agents.react.agent.ReactAgent.setup_workflow"):
            agent = ReactAgent(self.agent_config)

            # Verify tools were prepared
            assert len(agent.tools) == 2

            # Verify tool mapping was created
            assert "calc_add" in agent.tool_mapping
            assert "echo_message" in agent.tool_mapping

            # Verify version
            assert agent.version == "v1"

    def test_setup_workflow(self):
        """Test workflow setup."""
        from haive.core.graph.dynamic_graph_builder import DynamicGraph

        # Create the agent with a patched compile method
        with patch("haive.agents.react.agent.ReactAgent.compile"):
            # Create agent with workflow setup
            agent = ReactAgent(self.agent_config)

            # Spy on the graph builder
            with patch.object(DynamicGraph, "add_node") as mock_add_node, patch.object(
                DynamicGraph, "build", return_value=self.mock_graph
            ), patch.object(DynamicGraph, "set_entry_point"):

                # Print out complete mock call details
                for i, call in enumerate(mock_add_node.call_args_list):

                # Call setup workflow
                try:
                    agent.setup_workflow()
                except Exception as e:
                    import traceback

                    traceback.print_exc()
                    raise

                # Print out call count and args
                for call in mock_add_node.call_args_list:
                    pass

                # Capture node names with safe extraction
                node_names = []
                for call in mock_add_node.call_args_list:
                    try:
                        # Try different ways of extracting node name

                        # Try different extraction methods
                        if call.args:
                            if isinstance(call.args[0], str):
                                node_names.append(call.args[0])
                            elif hasattr(call.args[0], "name"):
                                node_names.append(call.args[0].name)
                            else:
                                pass

                        if call.kwargs and "name" in call.kwargs:
                            node_names.append(call.kwargs["name"])

                    except Exception as e:
                        pass

                # Verify calls were made
                assert mock_add_node.called, "No nodes were added to the graph"

                # Check that necessary nodes were added
                expected_nodes = [
                    "init",
                    "add_system",
                    self.agent_config.llm_node_name,
                    self.agent_config.tool_node_name,
                    "iteration_check",
                ]


                for node in expected_nodes:
                    assert node in node_names, f"Node {node} not found in graph"

    def test_run_with_string_input(self):
        """Test running the agent with a string input."""
        # Patch ReactAgent.run to avoid actual execution
        with patch("haive.agents.simple.agent.SimpleAgent.run") as mock_run:
            # Set up the mock return
            mock_run.return_value = {
                "messages": [
                    SystemMessage(
                        content="You are a helpful AI assistant that can use tools."
                    ),
                    HumanMessage(content="What is 2+2?"),
                    AIMessage(content="I'll calculate that for you."),
                ]
            }

            # Create agent with init patched
            with patch("haive.agents.react.agent.ReactAgent.setup_workflow"):
                agent = ReactAgent(self.agent_config)

                # Run with string input
                result = agent.run("What is 2+2?")

                # Verify run was called with properly formatted input
                args, kwargs = mock_run.call_args
                assert isinstance(args[0], dict)
                assert "messages" in args[0]
                assert isinstance(args[0]["messages"][0], HumanMessage)

                # Check result
                assert "messages" in result
                assert len(result["messages"]) == 3

    def test_arun(self):
        """Test asynchronous running of the agent."""
        # Patch ReactAgent.arun to avoid actual execution
        with patch("haive.agents.simple.agent.SimpleAgent.arun") as mock_arun:
            # Set up the mock return
            mock_arun.return_value = {
                "messages": [
                    SystemMessage(
                        content="You are a helpful AI assistant that can use tools."
                    ),
                    HumanMessage(content="What is 2+2?"),
                    AIMessage(content="I'll calculate that for you."),
                ]
            }

            # Create agent with init patched
            with patch("haive.agents.react.agent.ReactAgent.setup_workflow"):
                agent = ReactAgent(self.agent_config)

                # Run async with string input
                import asyncio

                async def run_async_test():
                    result = await agent.arun("What is 2+2?")
                    return result

                # Run the async test
                result = asyncio.run(run_async_test())

                # Verify arun was called
                mock_arun.assert_called_once()

                # Check result
                assert "messages" in result

    def test_runnable_config_integration(self):
        """Test integration with RunnableConfigManager."""
        # Create a runnable config
        runnable_config = RunnableConfigManager.create(
            thread_id="test_thread_1", user_id="test_user_1", temperature=0.5
        )

        # Create agent with init patched
        with patch("haive.agents.react.agent.ReactAgent.setup_workflow"):
            agent = ReactAgent(self.agent_config)

            # Update agent's runnable config
            agent.runnable_config = runnable_config

            # Verify the config is properly set
            assert agent.runnable_config["configurable"]["thread_id"] == "test_thread_1"
            assert agent.runnable_config["configurable"]["user_id"] == "test_user_1"
            assert agent.runnable_config["configurable"]["temperature"] == 0.5

    def test_tool_execution(self):
        """Test tool execution logic."""
        from agents.react.tool_utils import create_tool_executor

        # Create a tool executor
        executor = create_tool_executor(self.tools)

        # Create a test state with a tool call
        state = {
            "messages": [
                AIMessage(
                    content="I'll help you calculate that.",
                    tool_calls=[
                        {"name": "calc_add", "id": "call123", "args": {"a": 5, "b": 3}}
                    ],
                )
            ],
            "tool_results": [],
        }

        # Execute the tool
        result = executor(state)

        # Verify results
        assert len(result["messages"]) == 1
        assert len(result["tool_results"]) == 1
        assert result["tool_results"][0]["result"] == "8"
        assert result["current_iteration"] == 1


if __name__ == "__main__":
    unittest.main()
