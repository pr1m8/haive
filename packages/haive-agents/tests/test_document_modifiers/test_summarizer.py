"""Tests for SummarizerAgent."""

from typing import Any, Dict, List
from unittest.mock import AsyncMock, Mock, patch

import pytest
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.documents import Document

from haive.agents.document_modifiers.summarizer.map_branch.agent import SummarizerAgent
from haive.agents.document_modifiers.summarizer.map_branch.config import (
    SummarizerAgentConfig,
)
from haive.agents.document_modifiers.summarizer.map_branch.state import SummaryState


class TestSummarizerAgent:
    """Test suite for SummarizerAgent functionality."""

    @pytest.fixture
    def agent_config(self) -> SummarizerAgentConfig:
        """Create a test agent configuration."""
        return SummarizerAgentConfig(
            name="test_summarizer",
            token_max=1000,
            engines={
                "map_chain": AugLLMConfig(temperature=0.0),
                "reduce_chain": AugLLMConfig(temperature=0.0),
            },
        )

    @pytest.fixture
    def summarizer_agent(self, agent_config: SummarizerAgentConfig) -> SummarizerAgent:
        """Create a test SummarizerAgent instance."""
        return SummarizerAgent(agent_config)

    def test_agent_initialization(self, summarizer_agent: SummarizerAgent) -> None:
        """Test that agent initializes correctly."""
        assert summarizer_agent is not None
        assert summarizer_agent.token_max == 1000
        assert summarizer_agent.map_chain is not None
        assert summarizer_agent.reduce_chain is not None
        assert summarizer_agent.text_splitter is not None

    def test_token_limit_error_detection(
        self, summarizer_agent: SummarizerAgent
    ) -> None:
        """Test token limit error detection."""
        assert summarizer_agent._is_token_limit_error("string too long")
        assert summarizer_agent._is_token_limit_error("Token limit exceeded")
        assert summarizer_agent._is_token_limit_error("maximum context length")
        assert not summarizer_agent._is_token_limit_error("general error")

    def test_map_summaries_creates_send_commands(
        self, summarizer_agent: SummarizerAgent
    ) -> None:
        """Test map_summaries creates appropriate Send commands."""
        state = {"contents": ["doc1", "doc2", "doc3"]}
        sends = summarizer_agent.map_summaries(state)

        assert len(sends) == 3
        for i, send in enumerate(sends):
            assert send.node == "generate_summary"
            assert send.arg["content"] == f"doc{i+1}"

    def test_collect_summaries_creates_documents(
        self, summarizer_agent: SummarizerAgent
    ) -> None:
        """Test collect_summaries converts to Document objects."""
        state = SummaryState(summaries=["summary1", "summary2"])
        command = summarizer_agent.collect_summaries(state)

        docs = command.update["collapsed_summaries"]
        assert len(docs) == 2
        assert all(isinstance(doc, Document) for doc in docs)
        assert docs[0].page_content == "summary1"
        assert docs[1].page_content == "summary2"

    def test_should_collapse_logic(self, summarizer_agent: SummarizerAgent) -> None:
        """Test should_collapse decision logic."""
        # Under token limit - should proceed to final
        state = SummaryState(collapsed_summaries=[Document(page_content="short")])
        with patch.object(summarizer_agent, "length_function", return_value=500):
            assert summarizer_agent.should_collapse(state) == "generate_final_summary"

        # Over token limit - should collapse
        with patch.object(summarizer_agent, "length_function", return_value=1500):
            assert summarizer_agent.should_collapse(state) == "collapse_summaries"

    def test_length_function_calculation(
        self, summarizer_agent: SummarizerAgent
    ) -> None:
        """Test token counting for documents."""
        # Mock the LLM's get_num_tokens method
        mock_llm = Mock()
        mock_llm.get_num_tokens.side_effect = [10, 20, 30]

        with patch.object(
            summarizer_agent.config.engines["reduce_chain"].llm_config,
            "instantiate",
            return_value=mock_llm,
        ):
            docs = [
                Document(page_content="doc1"),
                Document(page_content="doc2"),
                Document(page_content="doc3"),
            ]
            total = summarizer_agent.length_function(docs)
            assert total == 60

    def test_length_function_empty_list(
        self, summarizer_agent: SummarizerAgent
    ) -> None:
        """Test length function with empty document list."""
        assert summarizer_agent.length_function([]) == 0

    @patch(
        "haive.agents.document_modifiers.summarizer.map_branch.agent.compose_runnable"
    )
    async def test_generate_summary_success(
        self, mock_compose: Mock, summarizer_agent: SummarizerAgent
    ) -> None:
        """Test successful summary generation."""
        # Setup mock
        mock_chain = AsyncMock()
        mock_chain.ainvoke.return_value = "Generated summary"
        summarizer_agent.map_chain = mock_chain

        # Execute
        state = {"content": "Test document content"}
        result = await summarizer_agent.generate_summary(state)

        # Assert
        assert result["summaries"] == ["Generated summary"]
        mock_chain.ainvoke.assert_called_once_with("Test document content")

    @patch(
        "haive.agents.document_modifiers.summarizer.map_branch.agent.compose_runnable"
    )
    async def test_generate_summary_handles_oversized_document(
        self, mock_compose: Mock, summarizer_agent: SummarizerAgent
    ) -> None:
        """Test handling of oversized documents."""
        # Setup mocks
        mock_map_chain = AsyncMock()
        mock_reduce_chain = AsyncMock()

        # First call fails with token error, subsequent calls succeed
        mock_map_chain.ainvoke.side_effect = [
            Exception("string too long"),
            "Chunk 1 summary",
            "Chunk 2 summary",
        ]
        mock_reduce_chain.ainvoke.return_value = "Combined summary"

        summarizer_agent.map_chain = mock_map_chain
        summarizer_agent.reduce_chain = mock_reduce_chain

        # Mock text splitter
        with patch.object(
            summarizer_agent.text_splitter,
            "split_text",
            return_value=["chunk1", "chunk2"],
        ):
            state = {"content": "Very long document " * 1000}
            result = await summarizer_agent.generate_summary(state)

            assert result["summaries"] == ["Combined summary"]

    async def test_generate_summary_handles_general_error(
        self, summarizer_agent: SummarizerAgent
    ) -> None:
        """Test handling of general errors."""
        # Setup mock that raises non-token error
        mock_chain = AsyncMock()
        mock_chain.ainvoke.side_effect = Exception("Network error")
        summarizer_agent.map_chain = mock_chain

        state = {"content": "Test content"}
        result = await summarizer_agent.generate_summary(state)

        assert "Error generating summary" in result["summaries"][0]

    async def test_collapse_summaries_operation(
        self, summarizer_agent: SummarizerAgent
    ) -> None:
        """Test collapse summaries functionality."""
        # Setup state
        docs = [Document(page_content="Summary 1"), Document(page_content="Summary 2")]
        state = {"collapsed_summaries": docs}

        # Mock the collapse operation
        with patch(
            "haive.agents.document_modifiers.summarizer.map_branch.agent.split_list_of_docs",
            return_value=[docs],
        ):
            with patch(
                "haive.agents.document_modifiers.summarizer.map_branch.agent.acollapse_docs",
                return_value=Document(page_content="Collapsed summary"),
            ) as mock_collapse:
                result = await summarizer_agent.collapse_summaries(state)

                assert len(result.update["collapsed_summaries"]) == 1
                assert (
                    result.update["collapsed_summaries"][0].page_content
                    == "Collapsed summary"
                )

    async def test_generate_final_summary_success(
        self, summarizer_agent: SummarizerAgent
    ) -> None:
        """Test final summary generation."""
        # Setup
        mock_chain = AsyncMock()
        mock_chain.ainvoke.return_value = "Final comprehensive summary"
        summarizer_agent.reduce_chain = mock_chain

        docs = [Document(page_content="Summary 1")]
        state = {"collapsed_summaries": docs}

        # Execute
        result = await summarizer_agent.generate_final_summary(state)

        # Assert
        assert result.update["final_summary"] == "Final comprehensive summary"

    async def test_generate_final_summary_error_handling(
        self, summarizer_agent: SummarizerAgent
    ) -> None:
        """Test final summary error handling."""
        # Setup mock that raises error
        mock_chain = AsyncMock()
        mock_chain.ainvoke.side_effect = Exception("API error")
        summarizer_agent.reduce_chain = mock_chain

        state = {"collapsed_summaries": [Document(page_content="Summary")]}
        result = await summarizer_agent.generate_final_summary(state)

        assert (
            "Error: Failed to generate final summary" in result.update["final_summary"]
        )

    async def test_handle_oversized_document_single_chunk(
        self, summarizer_agent: SummarizerAgent
    ) -> None:
        """Test handling oversized document that splits into single chunk."""
        # Mock text splitter to return single chunk
        with patch.object(
            summarizer_agent.text_splitter, "split_text", return_value=["single chunk"]
        ):
            mock_chain = AsyncMock()
            mock_chain.ainvoke.return_value = "Single chunk summary"
            summarizer_agent.map_chain = mock_chain

            result = await summarizer_agent._handle_oversized_document("content")
            assert result["summaries"] == ["Single chunk summary"]

    async def test_handle_oversized_document_no_chunks(
        self, summarizer_agent: SummarizerAgent
    ) -> None:
        """Test handling oversized document with no valid chunks."""
        # Mock text splitter to return empty list
        with patch.object(
            summarizer_agent.text_splitter, "split_text", return_value=[]
        ):
            result = await summarizer_agent._handle_oversized_document("content")
            assert result["summaries"] == ["Document could not be processed"]

    def test_get_token_count(self, summarizer_agent: SummarizerAgent) -> None:
        """Test single text token counting."""
        mock_llm = Mock()
        mock_llm.get_num_tokens.return_value = 42

        with patch.object(
            summarizer_agent.config.engines.get("map_chain", Mock()).llm_config,
            "instantiate",
            return_value=mock_llm,
        ):
            count = summarizer_agent._get_token_count("test text")
            assert count == 42

    @pytest.mark.integration
    @pytest.mark.skip(reason="Requires real LLM")
    async def test_real_summarization(
        self, agent_config: SummarizerAgentConfig
    ) -> None:
        """Integration test with real LLM."""
        agent = SummarizerAgent(agent_config)

        documents = [
            "This is a long document about artificial intelligence...",
            "Another document discussing machine learning concepts...",
        ]

        result = await agent.run({"contents": documents})

        assert "final_summary" in result
        assert len(result["final_summary"]) > 0
        assert isinstance(result["final_summary"], str)
