"""Tests for ComplexExtractionAgent."""

from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest
from haive.core.engine.aug_llm import AugLLMConfig
from pydantic import BaseModel, Field

from haive.agents.document_modifiers.complex_extraction.agent import (
    ComplexExtractionAgent,
)
from haive.agents.document_modifiers.complex_extraction.config import (
    ComplexExtractionAgentConfig,
)


class PersonInfo(BaseModel):
    """Test extraction model."""

    name: str
    age: int
    occupation: str


class TestComplexExtractionAgent:
    """Test suite for ComplexExtractionAgent functionality."""

    @pytest.fixture
    def agent_config(self) -> ComplexExtractionAgentConfig:
        """Create a test agent configuration."""
        return ComplexExtractionAgentConfig(
            name="test_extractor",
            extraction_model=PersonInfo,
            max_retries=3,
            llm_config=AugLLMConfig(temperature=0.0),
        )

    @pytest.fixture
    def extraction_agent(
        self, agent_config: ComplexExtractionAgentConfig
    ) -> ComplexExtractionAgent:
        """Create a test ComplexExtractionAgent instance."""
        return ComplexExtractionAgent(agent_config)

    def test_agent_initialization(
        self, extraction_agent: ComplexExtractionAgent
    ) -> None:
        """Test that agent initializes correctly."""
        assert extraction_agent is not None
        assert extraction_agent.extraction_model == PersonInfo
        assert extraction_agent.max_retries == 3
        assert extraction_agent.extraction_tool is not None

    def test_extraction_tool_setup(
        self, extraction_agent: ComplexExtractionAgent
    ) -> None:
        """Test extraction tool is set up correctly."""
        assert extraction_agent.extraction_tool.name == "extract_PersonInfo"
        assert extraction_agent.extraction_tool.args_schema == PersonInfo

    def test_agent_without_extraction_model(self) -> None:
        """Test agent can be created without extraction model."""
        config = ComplexExtractionAgentConfig(
            name="test_no_model", extraction_model=None
        )
        agent = ComplexExtractionAgent(config)
        assert agent.extraction_tool is None

    def test_message_preparation_from_string(
        self, extraction_agent: ComplexExtractionAgent
    ) -> None:
        """Test message preparation from string input."""
        text = "John Smith is a 35-year-old software engineer."
        messages = extraction_agent._prepare_extraction_messages(text)

        assert len(messages) == 1
        assert "Extract PersonInfo" in messages[0].content
        assert text in messages[0].content

    def test_message_preparation_from_list(
        self, extraction_agent: ComplexExtractionAgent
    ) -> None:
        """Test message preparation from list of strings."""
        texts = ["John Smith is 35.", "He is an engineer."]
        messages = extraction_agent._prepare_extraction_messages(texts)

        assert len(messages) == 1
        assert all(text in messages[0].content for text in texts)

    @patch("haive.core.engine.agent.agent.Agent.run")
    def test_run_extracts_data_from_tool_calls(
        self, mock_run: Mock, extraction_agent: ComplexExtractionAgent
    ) -> None:
        """Test that run method extracts data from tool calls."""
        # Arrange
        mock_message = Mock()
        mock_message.tool_calls = [
            {
                "name": "extract_PersonInfo",
                "args": {
                    "name": "John Smith",
                    "age": 35,
                    "occupation": "software engineer",
                },
            }
        ]
        mock_run.return_value = {"messages": [mock_message]}

        # Act
        result = extraction_agent.run("test input")

        # Assert
        assert "extracted_data" in result
        assert result["extracted_data"]["name"] == "John Smith"
        assert result["extracted_data"]["age"] == 35

    def test_jsonpatch_initialization(self) -> None:
        """Test agent initialization with JSONPatch enabled."""
        config = ComplexExtractionAgentConfig(
            name="test_jsonpatch", extraction_model=PersonInfo, use_jsonpatch=True
        )

        with patch("builtins.__import__", side_effect=ImportError):
            agent = ComplexExtractionAgent(config)
            assert not agent.use_jsonpatch  # Should fall back gracefully

    def test_extract_node_error_handling(
        self, extraction_agent: ComplexExtractionAgent
    ) -> None:
        """Test extract_node handles errors gracefully."""
        # Test with missing messages
        result = extraction_agent.extract_node({})
        assert "error" in result

        # Test pass-through when no runnable
        state = {"messages": ["test"]}
        result = extraction_agent.extract_node(state)
        assert result == state  # Should pass through

    def test_bind_validator_creates_graph(
        self, extraction_agent: ComplexExtractionAgent
    ) -> None:
        """Test validator binding creates proper graph."""
        mock_llm = Mock()
        tools = [extraction_agent.extraction_tool]

        graph = extraction_agent.bind_validator_with_retries(
            mock_llm, tools=tools, max_attempts=3
        )

        assert graph is not None
        assert hasattr(graph, "nodes")

    @pytest.mark.integration
    @pytest.mark.skip(reason="Requires real LLM")
    async def test_real_extraction(
        self, agent_config: ComplexExtractionAgentConfig
    ) -> None:
        """Integration test with real LLM."""
        agent = ComplexExtractionAgent(agent_config)

        text = "Dr. Sarah Johnson is a 42-year-old cardiologist."
        result = agent.run(text)

        assert "extracted_data" in result
        extracted = result["extracted_data"]
        assert "Sarah Johnson" in extracted["name"]
        assert extracted["age"] == 42
        assert "cardiologist" in extracted["occupation"]
