"""Tests for Document Loader Agents.

This module provides tests for the document loader agents and their specialized variants.
"""

from pathlib import Path
import tempfile
import unittest

from haive.agents.document_loader import (
    DirectoryLoaderAgent,
    DocumentLoaderAgent,
    FileLoaderAgent,
    WebLoaderAgent,
)
from haive.core.engine.base import EngineType
from haive.core.engine.document_loader import DocumentLoaderOutput
from haive.core.graph.state_graph.base_graph2 import BaseGraph


class DocumentLoaderAgentTest(unittest.TestCase):
    """Test case for DocumentLoaderAgent."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        # Create temporary test files
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.test_dir = Path(cls.temp_dir.name)

        # Create test text file
        cls.text_file = cls.test_dir / "test.txt"
        with open(cls.text_file, "w") as f:
            f.write("This is a test document.\nIt has multiple lines.\nThis is line 3.")

        # Create test markdown file
        cls.md_file = cls.test_dir / "test.md"
        with open(cls.md_file, "w") as f:
            f.write(
                "# Test Markdown\n\nThis is a *markdown* document with **formatting**."
            )

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        cls.temp_dir.cleanup()

    def test_agent_creation(self):
        """Test document loader agent creation."""
        # Create a basic agent
        agent = DocumentLoaderAgent()

        # Check basic properties
        assert agent.name == "Document Loader Agent"
        assert agent.engine_type == EngineType.AGENT

        # Check engine is registered
        assert "document_loader" in agent.engines

    def test_graph_building(self):
        """Test that the agent builds a proper graph."""
        agent = DocumentLoaderAgent()

        # Build the graph
        graph = agent.build_graph()

        # Check graph structure
        assert isinstance(graph, BaseGraph)
        assert graph.name == "DocumentLoaderGraph"

        # Check nodes
        assert "document_loader" in graph.nodes

    def test_file_loader_agent(self):
        """Test specialized file loader agent."""
        # Create a file loader agent
        agent = FileLoaderAgent(file_path=self.text_file, include_metadata=True)

        # Check agent configuration
        assert agent.name == "File Loader Agent"
        assert agent.file_path == self.text_file

        # Check engine registration
        assert "file_loader" in agent.engines

    def test_web_loader_agent(self):
        """Test specialized web loader agent."""
        # Create a web loader agent
        agent = WebLoaderAgent(
            url="https://example.com",
            dynamic_loading=True,
            headers={"User-Agent": "Test Agent"},
        )

        # Check agent configuration
        assert agent.name == "Web Loader Agent"
        assert agent.url == "https://example.com"
        assert agent.dynamic_loading

        # Check engine registration
        assert "web_loader" in agent.engines

    def test_directory_loader_agent(self):
        """Test specialized directory loader agent."""
        # Create a directory loader agent
        agent = DirectoryLoaderAgent(
            directory_path=self.test_dir,
            recursive=True,
            include_extensions=[".txt", ".md"],
        )

        # Check agent configuration
        assert agent.name == "Directory Loader Agent"
        assert agent.directory_path == self.test_dir
        assert agent.recursive
        assert agent.include_extensions == [".txt", ".md"]

        # Check engine registration
        assert "directory_loader" in agent.engines

    def test_process_output(self):
        """Test the process_output method with different configurations."""
        agent = DocumentLoaderAgent()

        # Create test output
        output = DocumentLoaderOutput(
            documents=[
                {"page_content": "Test content 1", "metadata": {"source": "test1.txt"}},
                {"page_content": "Test content 2", "metadata": {"source": "test2.txt"}},
            ],
            total_documents=2,
            operation_time=0.5,
            source_type="file",
            loader_name="text_loader",
            original_source="test_dir",
        )

        # Test with default settings (include content and metadata)
        result = agent.process_output(output)
        assert "documents" in result
        assert len(result["documents"]) == 2
        assert "metadata" in result["documents"][0]

        # Test with include_content=False
        agent.include_content = False
        result = agent.process_output(output)
        assert "documents" not in result
        assert result["document_count"] == 2

        # Test with include_metadata=False
        agent.include_content = True
        agent.include_metadata = False
        result = agent.process_output(output)
        assert "documents" in result
        assert "metadata" not in result["documents"][0]
        assert result["documents"][0]["page_content"] == "Test content 1"


if __name__ == "__main__":
    unittest.main()
