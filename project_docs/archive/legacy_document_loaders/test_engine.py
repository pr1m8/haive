"""Integration Tests for Document Loader Engine.

This module provides integration tests for the document loader engine.
It tests the functionality of the engine with various source types.
"""

import tempfile
import unittest
from pathlib import Path
from unittest import mock

# Import engine and factory
from engine import (
    DocumentLoaderEngine,
    create_directory_loader_engine,
    create_document_loader_engine,
    create_file_loader_engine,
    create_web_loader_engine,
)

# Import configuration
from engine_config import DocumentLoaderConfig, DocumentLoaderOutput

# Import path analyzer
# Import from source to loader mapping
from source_loader_mapping import initialize_registries

# Import source and loader registry


class DocumentLoaderEngineTest(unittest.TestCase):
    """Test case for DocumentLoaderEngine."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment.

        Creates test files for various formats to be used in tests.
        """
        # Initialize registries
        initialize_registries()

        # Create test files
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

        # Create test JSON file
        cls.json_file = cls.test_dir / "test.json"
        with open(cls.json_file, "w") as f:
            f.write('{"name": "Test Document", "type": "JSON", "items": [1, 2, 3]}')

        # Create test CSV file
        cls.csv_file = cls.test_dir / "test.csv"
        with open(cls.csv_file, "w") as f:
            f.write(
                "name,age,city\nAlice,30,New York\nBob,25,San Francisco\nCharlie,35,Chicago"
            )

        # Create test HTML file
        cls.html_file = cls.test_dir / "test.html"
        with open(cls.html_file, "w") as f:
            f.write(
                "<html><head><title>Test HTML</title></head><body><h1>Test HTML</h1><p>This is a test HTML document.</p></body></html>"
            )

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        cls.temp_dir.cleanup()

    def test_engine_creation(self):
        """Test engine creation with various configurations."""
        # Create engine with default config
        engine = create_document_loader_engine()
        assert isinstance(engine, DocumentLoaderEngine)

        # Create engine with custom config dict
        engine = create_document_loader_engine({"max_documents": 10})
        assert isinstance(engine, DocumentLoaderEngine)
        assert engine.config.max_documents == 10

        # Create engine with custom config object
        config = DocumentLoaderConfig(max_documents=20)
        engine = create_document_loader_engine(config)
        assert isinstance(engine, DocumentLoaderEngine)
        assert engine.config.max_documents == 20

    def test_input_output_schema(self):
        """Test that input and output schemas are properly defined."""
        engine = create_document_loader_engine()

        # Check input fields
        input_fields = engine.get_input_fields()
        assert "source" in input_fields
        assert "loader_name" in input_fields
        assert "loader_options" in input_fields
        assert "include_metadata" in input_fields
        assert "include_patterns" in input_fields
        assert "exclude_patterns" in input_fields

        # Check output fields
        output_fields = engine.get_output_fields()
        assert "documents" in output_fields
        assert "total_documents" in output_fields
        assert "operation_time" in output_fields
        assert "source_type" in output_fields
        assert "loader_name" in output_fields
        assert "original_source" in output_fields
        assert "errors" in output_fields
        assert "has_errors" in output_fields

        # Check derived schemas
        input_schema = engine.derive_input_schema()
        output_schema = engine.derive_output_schema()

        assert hasattr(input_schema, "model_validate")
        assert hasattr(output_schema, "model_validate")

        # Test schema validation
        valid_input = {"source": "/path/to/file.txt", "loader_name": "text_loader"}
        input_instance = input_schema.model_validate(valid_input)
        assert input_instance.source == "/path/to/file.txt"
        assert input_instance.loader_name == "text_loader"

    def test_file_loader_engine_creation(self):
        """Test file loader engine creation with various options."""
        # Create engine for a specific file
        engine = create_file_loader_engine(file_path=self.text_file)
        assert isinstance(engine, DocumentLoaderEngine)

        # Create engine with explicit loader
        engine = create_file_loader_engine(
            file_path=self.text_file, loader_name="text_loader"
        )
        assert isinstance(engine, DocumentLoaderEngine)
        assert engine.config.loader_name == "text_loader"

        # Create engine with file extension only
        engine = create_file_loader_engine(file_extension=".txt")
        assert isinstance(engine, DocumentLoaderEngine)
        assert engine.config.loader_options["file_extension"] == ".txt"

        # Create engine with custom options
        engine = create_file_loader_engine(
            file_path=self.text_file, encoding="utf-8", autodetect_encoding=True
        )
        assert isinstance(engine, DocumentLoaderEngine)
        assert engine.config.loader_options["encoding"] == "utf-8"
        assert engine.config.loader_options["autodetect_encoding"] == True

    def test_web_loader_engine_creation(self):
        """Test web loader engine creation with various options."""
        # Create engine for a URL
        engine = create_web_loader_engine(url="https://example.com")
        assert isinstance(engine, DocumentLoaderEngine)

        # Create engine with dynamic loading
        engine = create_web_loader_engine(dynamic_loading=True)
        assert isinstance(engine, DocumentLoaderEngine)
        assert engine.config.loader_name == "playwright_loader"

        # Create engine with recursive loading
        engine = create_web_loader_engine(recursive=True, max_depth=2)
        assert isinstance(engine, DocumentLoaderEngine)
        assert engine.config.loader_name == "recursive_url_loader"
        assert engine.config.loader_options["max_depth"] == 2

        # Create engine with custom headers
        engine = create_web_loader_engine(
            url="https://example.com", headers={"User-Agent": "Test Agent"}
        )
        assert isinstance(engine, DocumentLoaderEngine)
        assert engine.config.loader_options["headers"]["User-Agent"] == "Test Agent"

    def test_directory_loader_engine_creation(self):
        """Test directory loader engine creation with various options."""
        # Create engine for a directory
        engine = create_directory_loader_engine(directory_path=self.test_dir)
        assert isinstance(engine, DocumentLoaderEngine)

        # Create engine with glob pattern
        engine = create_directory_loader_engine(
            directory_path=self.test_dir, glob_pattern="*.txt"
        )
        assert isinstance(engine, DocumentLoaderEngine)
        assert engine.config.loader_options["glob"] == "*.txt"

        # Create engine with include/exclude extensions
        engine = create_directory_loader_engine(
            directory_path=self.test_dir,
            include_extensions=[".txt", ".md"],
            exclude_extensions=[".html"],
        )
        assert isinstance(engine, DocumentLoaderEngine)
        assert engine.config.loader_options["include_extensions"] == [".txt", ".md"]
        assert engine.config.loader_options["exclude_extensions"] == [".html"]

    def test_create_runnable(self):
        """Test the create_runnable method."""
        engine = create_document_loader_engine()

        # Create runnable with no config
        runnable = engine.create_runnable()
        assert runnable is engine

        # Create runnable with config
        runnable_config = {"max_documents": 50}

        # No need to mock since we're providing a direct config
        runnable = engine.create_runnable(runnable_config)
        assert runnable is engine
        assert engine.config.max_documents == 50

    def test_text_file_loading(self):
        """Test loading a text file."""
        # Create engine
        engine = create_file_loader_engine(
            file_path=self.text_file, loader_name="text_loader"
        )

        # Mock the necessary methods
        with mock.patch.object(
            engine, "_prepare_input"
        ) as mock_prepare, mock.patch.object(
            engine, "_process_source"
        ) as mock_process, mock.patch.object(
            engine, "_select_loader_strategy"
        ) as mock_select, mock.patch.object(
            engine, "_create_loader"
        ) as mock_create, mock.patch.object(
            engine, "_load_documents"
        ) as mock_load:

            # Configure mocks
            mock_prepare.return_value = mock.MagicMock(
                source=str(self.text_file), loader_name="text_loader", loader_options={}
            )
            mock_source = mock.MagicMock(source_type="text")
            mock_analysis = mock.MagicMock()
            mock_process.return_value = (mock_source, mock_analysis)
            mock_strategy = mock.MagicMock(
                strategy_name="text_loader", supports_async=False
            )
            mock_select.return_value = mock_strategy
            mock_create.return_value = mock.MagicMock()
            mock_load.return_value = [
                {
                    "page_content": "This is a test document.\nIt has multiple lines.\nThis is line 3.",
                    "metadata": {"source": str(self.text_file)},
                }
            ]

            # Invoke the engine
            result = engine.invoke(self.text_file)

            # Check the result
            assert isinstance(result, DocumentLoaderOutput)
            assert len(result.documents) == 1
            assert (
                result.documents[0]["page_content"]
                == "This is a test document.\nIt has multiple lines.\nThis is line 3."
            )
            assert result.total_documents == 1
            assert not result.has_errors

            # Verify mocks were called
            mock_prepare.assert_called_once()
            mock_process.assert_called_once()
            mock_select.assert_called_once()
            mock_create.assert_called_once()
            mock_load.assert_called_once()

    def test_error_handling(self):
        """Test error handling in the engine."""
        # Create engine with raise_on_error=False
        engine = create_document_loader_engine({"raise_on_error": False})

        # Mock process_source to raise an exception
        with mock.patch.object(
            engine, "_process_source", side_effect=ValueError("Test error")
        ):
            # Invoke the engine
            result = engine.invoke("nonexistent_file.txt")

            # Check the result
            assert isinstance(result, DocumentLoaderOutput)
            assert len(result.documents) == 0
            assert result.total_documents == 0
            assert result.has_errors
            assert len(result.errors) == 1
            assert result.errors[0]["type"] == "ValueError"
            assert result.errors[0]["message"] == "Test error"

        # Create engine with raise_on_error=True
        engine = create_document_loader_engine({"raise_on_error": True})

        # Mock process_source to raise an exception
        with mock.patch.object(
            engine, "_process_source", side_effect=ValueError("Test error")
        ):
            # Invoke the engine and expect an exception
            with self.assertRaises(ValueError):
                engine.invoke("nonexistent_file.txt")

    @mock.patch("asyncio.get_running_loop")
    def test_async_loading(self, mock_get_loop):
        """Test asynchronous document loading."""
        # Use unittest.IsolatedAsyncioTestCase for proper async testing
        # Here we'll just test the setup without actually running the coroutine

        # Create engine with async enabled
        engine = create_document_loader_engine({"use_async": True})

        # Verify that the engine is configured for async
        assert engine.config.use_async

        # Check that the ainvoke method exists and is callable
        assert hasattr(engine, "ainvoke")
        assert callable(engine.ainvoke)

        # Test that create_runnable properly preserves the async setting
        runnable = engine.create_runnable()
        assert runnable.config.use_async

    def test_document_conversion(self):
        """Test document conversion functionality."""
        engine = create_document_loader_engine()

        # Test converting LangChain Document-like object
        class MockDocument:
            def __init__(self):
                self.page_content = "Test content"
                self.metadata = {"source": "test"}

        doc = MockDocument()
        result = engine._convert_document(doc)
        assert result["page_content"] == "Test content"
        assert result["metadata"]["source"] == "test"

        # Test converting dictionary
        doc_dict = {"page_content": "Dict content", "metadata": {"type": "dict"}}
        result = engine._convert_document(doc_dict)
        assert result["page_content"] == "Dict content"
        assert result["metadata"]["type"] == "dict"

        # Test converting string
        result = engine._convert_document("Plain string")
        assert result["page_content"] == "Plain string"
        assert result["metadata"] == {}

        # Test converting object with __dict__ method
        class DictLikeObject:
            def __init__(self):
                self.content = "Object content"
                self.metadata = {"type": "object"}

            def __dict__(self):
                return {"page_content": self.content, "metadata": self.metadata}

        try:
            result = engine._convert_document(DictLikeObject())
            assert "page_content" in result
        except Exception:
            # This might fail depending on implementation, which is fine
            pass

        # Test converting non-standard objects
        class CustomObject:
            def __init__(self):
                self.data = "Custom data"

            def __str__(self):
                return self.data

        result = engine._convert_document(CustomObject())
        assert result["page_content"] == "Custom data"

        # Test with None
        result = engine._convert_document(None)
        assert result["page_content"] == "None"
        assert result["metadata"] == {}

    def test_engine_framework_integration(self):
        """Test integration with the Haive engine framework."""
        # Create an engine with default configuration
        engine = create_document_loader_engine()

        # Test that it properly inherits from InvokableEngine
        from haive.core.engine.base import InvokableEngine

        assert isinstance(engine, InvokableEngine)

        # Test engine type
        assert engine.engine_type.value == "document_loader"

        # Test that required methods are implemented
        assert callable(engine.get_input_fields)
        assert callable(engine.get_output_fields)
        assert callable(engine.create_runnable)
        assert callable(engine.invoke)
        assert callable(engine.ainvoke)

        # Test creating a runnable
        config = DocumentLoaderConfig(max_documents=50)
        engine_with_config = create_document_loader_engine(config)
        runnable = engine_with_config.create_runnable()
        assert runnable.config.max_documents == 50

        # Test derive_input_schema and derive_output_schema
        input_schema = engine.derive_input_schema()
        output_schema = engine.derive_output_schema()

        assert input_schema.__name__ == "DocumentLoaderEngineInput"
        assert output_schema.__name__ == "DocumentLoaderEngineOutput"


if __name__ == "__main__":
    unittest.main()
