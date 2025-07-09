"""Tests for IterativeGraphTransformer."""

from typing import Any, Dict, List
from unittest.mock import MagicMock, Mock, patch

import pytest
from langchain_community.graphs.graph_document import GraphDocument, Node, Relationship
from langchain_core.documents import Document

from haive.agents.document_modifiers.kg.kg_iterative_refinement.agent import (
    IterativeGraphTransformer,
)
from haive.agents.document_modifiers.kg.kg_iterative_refinement.config import (
    IterativeGraphTransformerConfig,
)
from haive.agents.document_modifiers.kg.kg_iterative_refinement.state import (
    IterativeGraphTransformerState,
)


class TestIterativeGraphTransformer:
    """Test suite for IterativeGraphTransformer functionality."""

    @pytest.fixture
    def agent_config(self) -> IterativeGraphTransformerConfig:
        """Create a test agent configuration."""
        return IterativeGraphTransformerConfig(name="test_graph_transformer")

    @pytest.fixture
    def graph_transformer_agent(
        self, agent_config: IterativeGraphTransformerConfig
    ) -> IterativeGraphTransformer:
        """Create a test IterativeGraphTransformer instance."""
        return IterativeGraphTransformer(agent_config)

    @pytest.fixture
    def mock_graph_document(self) -> GraphDocument:
        """Create a mock GraphDocument for testing."""
        nodes = [
            Node(id="1", type="Person", properties={"name": "Marie Curie"}),
            Node(id="2", type="Award", properties={"name": "Nobel Prize"}),
        ]
        relationships = [
            Relationship(
                source=Node(id="1", type="Person"),
                target=Node(id="2", type="Award"),
                type="WON",
            )
        ]
        return GraphDocument(
            nodes=nodes,
            relationships=relationships,
            source=Document(page_content="Test content"),
        )

    def test_agent_initialization(
        self, graph_transformer_agent: IterativeGraphTransformer
    ) -> None:
        """Test that agent initializes correctly."""
        assert graph_transformer_agent is not None
        assert graph_transformer_agent.llm_graph_transformer is not None

    def test_state_normalization(self) -> None:
        """Test state content normalization."""
        # Test string normalization
        state = IterativeGraphTransformerState(contents="Single string content")
        assert len(state.contents) == 1
        assert isinstance(state.contents[0], Document)
        assert state.contents[0].page_content == "Single string content"

        # Test list of strings normalization
        state = IterativeGraphTransformerState(contents=["Doc 1", "Doc 2"])
        assert len(state.contents) == 2
        assert all(isinstance(doc, Document) for doc in state.contents)

        # Test mixed content normalization
        state = IterativeGraphTransformerState(
            contents=[
                "String doc",
                Document(page_content="Document object"),
                {"page_content": "Dict doc"},
            ]
        )
        assert len(state.contents) == 3
        assert all(isinstance(doc, Document) for doc in state.contents)

    def test_should_refine_logic(self) -> None:
        """Test the should_refine decision logic."""
        state = IterativeGraphTransformerState(
            contents=["Doc 1", "Doc 2", "Doc 3"], index=1
        )

        # Should continue refining
        assert state.should_refine() == "refine_summary"

        # At last document
        state.index = 3
        assert state.should_refine() == "__end__"

    @patch(
        "haive.agents.document_modifiers.kg.kg_base.models.GraphTransformer.transform_documents"
    )
    def test_generate_initial_summary_success(
        self,
        mock_transform: Mock,
        graph_transformer_agent: IterativeGraphTransformer,
        mock_graph_document: GraphDocument,
    ) -> None:
        """Test successful initial graph generation."""
        # Setup mock
        mock_transform.return_value = [mock_graph_document]

        # Create state
        state = IterativeGraphTransformerState(
            contents=["Marie Curie was a physicist."]
        )
        config = MagicMock()

        # Execute
        command = graph_transformer_agent.generate_initial_summary(state, config)

        # Assert
        assert command.update["graph_doc"] == mock_graph_document
        assert command.update["index"] == 1
        mock_transform.assert_called_once()

    def test_generate_initial_summary_no_documents(
        self, graph_transformer_agent: IterativeGraphTransformer
    ) -> None:
        """Test initial summary with no documents."""
        state = IterativeGraphTransformerState(contents=[])
        config = MagicMock()

        with pytest.raises(ValueError, match="At least one document is required"):
            graph_transformer_agent.generate_initial_summary(state, config)

    @patch(
        "haive.agents.document_modifiers.kg.kg_base.models.GraphTransformer.transform_documents"
    )
    def test_generate_initial_summary_no_graph(
        self, mock_transform: Mock, graph_transformer_agent: IterativeGraphTransformer
    ) -> None:
        """Test handling when no graph is generated."""
        # Setup mock to return empty list
        mock_transform.return_value = []

        state = IterativeGraphTransformerState(contents=["Content"])
        config = MagicMock()

        command = graph_transformer_agent.generate_initial_summary(state, config)

        assert command.update["graph_doc"] is None
        assert command.update["index"] == 1

    @patch(
        "haive.agents.document_modifiers.kg.kg_base.models.GraphTransformer.transform_documents"
    )
    def test_refine_summary_success(
        self,
        mock_transform: Mock,
        graph_transformer_agent: IterativeGraphTransformer,
        mock_graph_document: GraphDocument,
    ) -> None:
        """Test successful graph refinement."""
        # Create refined graph with additional node
        refined_graph = GraphDocument(
            nodes=mock_graph_document.nodes
            + [Node(id="3", type="Country", properties={"name": "Poland"})],
            relationships=mock_graph_document.relationships,
            source=Document(page_content="Refined content"),
        )
        mock_transform.return_value = [refined_graph]

        # Create state with existing graph
        state = IterativeGraphTransformerState(
            contents=["First doc", "Second doc"], index=1, graph_doc=mock_graph_document
        )
        config = MagicMock()

        # Execute
        command = graph_transformer_agent.refine_summary(state, config)

        # Assert
        assert command.update["graph_doc"] == refined_graph
        assert command.update["index"] == 2
        assert len(command.update["graph_doc"].nodes) > len(mock_graph_document.nodes)

    def test_refine_summary_out_of_bounds(
        self, graph_transformer_agent: IterativeGraphTransformer
    ) -> None:
        """Test refinement with out of bounds index."""
        state = IterativeGraphTransformerState(
            contents=["Doc 1"], index=5, graph_doc=None  # Out of bounds
        )
        config = MagicMock()

        with pytest.raises(IndexError, match="Index 5 out of bounds"):
            graph_transformer_agent.refine_summary(state, config)

    @patch(
        "haive.agents.document_modifiers.kg.kg_base.models.GraphTransformer.transform_documents"
    )
    def test_refine_summary_error_handling(
        self,
        mock_transform: Mock,
        graph_transformer_agent: IterativeGraphTransformer,
        mock_graph_document: GraphDocument,
    ) -> None:
        """Test error handling during refinement."""
        # Setup mock to raise exception
        mock_transform.side_effect = Exception("Transform error")

        state = IterativeGraphTransformerState(
            contents=["First doc", "Second doc"], index=1, graph_doc=mock_graph_document
        )
        config = MagicMock()

        # Execute - should handle error gracefully
        command = graph_transformer_agent.refine_summary(state, config)

        # Should increment index but keep existing graph
        assert command.update["index"] == 2
        assert "graph_doc" not in command.update  # Keeps existing graph

    @patch(
        "haive.agents.document_modifiers.kg.kg_base.models.GraphTransformer.transform_documents"
    )
    def test_refine_summary_no_graph_generated(
        self,
        mock_transform: Mock,
        graph_transformer_agent: IterativeGraphTransformer,
        mock_graph_document: GraphDocument,
    ) -> None:
        """Test handling when refinement produces no graph."""
        mock_transform.return_value = []

        state = IterativeGraphTransformerState(
            contents=["First doc", "Second doc"], index=1, graph_doc=mock_graph_document
        )
        config = MagicMock()

        command = graph_transformer_agent.refine_summary(state, config)

        # Should increment index but not update graph
        assert command.update["index"] == 2
        assert "graph_doc" not in command.update

    def test_setup_workflow(
        self, graph_transformer_agent: IterativeGraphTransformer
    ) -> None:
        """Test workflow setup."""
        # Mock the graph object
        mock_graph = Mock()
        graph_transformer_agent.graph = mock_graph

        # Execute setup
        graph_transformer_agent.setup_workflow()

        # Verify nodes were added
        assert mock_graph.add_node.call_count == 2
        mock_graph.add_node.assert_any_call(
            "generate_initial_summary", graph_transformer_agent.generate_initial_summary
        )
        mock_graph.add_node.assert_any_call(
            "refine_summary", graph_transformer_agent.refine_summary
        )

        # Verify edges were added
        assert mock_graph.add_edge.call_count >= 1
        assert mock_graph.add_conditional_edges.call_count == 2

    @pytest.mark.integration
    @pytest.mark.skip(reason="Requires real LLM and GraphTransformer")
    async def test_real_graph_transformation(
        self, agent_config: IterativeGraphTransformerConfig
    ) -> None:
        """Integration test with real components."""
        agent = IterativeGraphTransformer(agent_config)

        documents = [
            "Marie Curie was born in Warsaw, Poland in 1867.",
            "She won the Nobel Prize in Physics in 1903 with her husband Pierre.",
            "Marie Curie also won the Nobel Prize in Chemistry in 1911.",
        ]

        result = agent.run({"contents": documents})

        assert "graph_doc" in result
        graph = result["graph_doc"]
        assert len(graph.nodes) > 0
        assert len(graph.relationships) > 0

        # Check for expected entities
        node_names = [node.properties.get("name", "") for node in graph.nodes]
        assert any("Marie Curie" in name for name in node_names)
        assert any("Nobel Prize" in name for name in node_names)
