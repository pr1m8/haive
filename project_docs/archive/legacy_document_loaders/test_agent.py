"""Tests for the Document Loader Agent.

This module provides tests for the DocumentLoaderAgent and its specialized variants,
demonstrating how to use them in different scenarios.
"""

from pathlib import Path
import tempfile
import unittest
from unittest import mock

# Import document loader agent
from agent import (
    DirectoryLoaderAgent,
    DocumentLoaderAgent,
    FileLoaderAgent,
    WebLoaderAgent,
)

# Import document loader engine
from engine import DocumentLoaderEngine

# Import configuration models
from engine_config import DocumentLoaderOutput

from haive.core.engine.base import EngineType
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
        self.assertEqual(agent.name, "Document Loader Agent")
        self.assertEqual(agent.engine_type, EngineType.AGENT)
        self.assertIsInstance(agent.engine, DocumentLoaderEngine)

        # Check engine is registered
        self.assertIn("document_loader", agent.engines)
        self.assertEqual(agent.engines["document_loader"], agent.engine)

    def test_graph_building(self):
        """Test that the agent builds a proper graph."""
        agent = DocumentLoaderAgent()

        # Build the graph
        graph = agent.build_graph()

        # Check graph structure
        self.assertIsInstance(graph, BaseGraph)
        self.assertEqual(graph.name, "DocumentLoaderGraph")

        # Check nodes
        self.assertIn("document_loader", graph.nodes)

        # Check edges
        self.assertEqual(len(graph.edges), 2)  # START->loader, loader->END

    def test_file_loader_agent(self):
        """Test specialized file loader agent."""
        # Create a file loader agent
        agent = FileLoaderAgent(file_path=self.text_file, include_metadata=True)

        # Check agent configuration
        self.assertEqual(agent.name, "File Loader Agent")
        self.assertEqual(agent.file_path, self.text_file)

        # Check engine registration
        self.assertIn("file_loader", agent.engines)

    def test_web_loader_agent(self):
        """Test specialized web loader agent."""
        # Create a web loader agent
        agent = WebLoaderAgent(
            url="https://example.com",
            dynamic_loading=True,
            headers={"User-Agent": "Test Agent"},
        )

        # Check agent configuration
        self.assertEqual(agent.name, "Web Loader Agent")
        self.assertEqual(agent.url, "https://example.com")
        self.assertTrue(agent.dynamic_loading)

        # Check engine registration
        self.assertIn("web_loader", agent.engines)

    def test_directory_loader_agent(self):
        """Test specialized directory loader agent."""
        # Create a directory loader agent
        agent = DirectoryLoaderAgent(
            directory_path=self.test_dir,
            recursive=True,
            include_extensions=[".txt", ".md"],
        )

        # Check agent configuration
        self.assertEqual(agent.name, "Directory Loader Agent")
        self.assertEqual(agent.directory_path, self.test_dir)
        self.assertTrue(agent.recursive)
        self.assertEqual(agent.include_extensions, [".txt", ".md"])

        # Check engine registration
        self.assertIn("directory_loader", agent.engines)

    def test_agent_invocation(self):
        """Test agent invocation with mocked engine."""
        # Create agent with mocked engine
        agent = DocumentLoaderAgent()

        # Mock the engine's invoke method
        mock_output = DocumentLoaderOutput(
            documents=[
                {"page_content": "Test content", "metadata": {"source": "test.txt"}}
            ],
            total_documents=1,
            operation_time=0.1,
            source_type="file",
            loader_name="text_loader",
            original_source="test.txt",
        )

        # Replace the engine's invoke with a mock
        agent.engine.invoke = mock.MagicMock(return_value=mock_output)

        # Compile the agent graph
        compiled_agent = agent.compile()

        # Create a mock for the compiled agent
        with mock.patch.object(
            compiled_agent,
            "invoke",
            return_value={
                "documents": [
                    {"page_content": "Test content", "metadata": {"source": "test.txt"}}
                ],
                "total_documents": 1,
                "operation_time": 0.1,
                "source_type": "file",
                "loader_name": "text_loader",
                "original_source": "test.txt",
            },
        ):
            # Invoke the agent
            result = agent.invoke("test.txt")

            # Check result
            self.assertIn("documents", result)
            self.assertEqual(result["total_documents"], 1)
            self.assertEqual(result["source_type"], "file")

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
        self.assertIn("documents", result)
        self.assertEqual(len(result["documents"]), 2)
        self.assertIn("metadata", result["documents"][0])

        # Test with include_content=False
        agent.include_content = False
        result = agent.process_output(output)
        self.assertNotIn("documents", result)
        self.assertEqual(result["document_count"], 2)

        # Test with include_metadata=False
        agent.include_content = True
        agent.include_metadata = False
        result = agent.process_output(output)
        self.assertIn("documents", result)
        self.assertNotIn("metadata", result["documents"][0])
        self.assertEqual(result["documents"][0]["page_content"], "Test content 1")


if __name__ == "__main__":
    unittest.main()
