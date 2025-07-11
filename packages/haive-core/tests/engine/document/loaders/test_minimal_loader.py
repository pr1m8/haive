"""Minimal test focused on the loader selection fix."""

import importlib.util
import sys
from enum import Enum
from pathlib import Path


# Create minimal LoaderPreference enum for testing
class LoaderPreference(str, Enum):
    """Loader preference for selection."""

    SPEED = "speed"
    QUALITY = "quality"
    BALANCED = "balanced"


# Direct file imports
def import_module_from_file(module_name, file_path):
    """Import a module directly from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)

    # Handle missing dependencies by mocking them
    if "config" in module_name:
        # Mock the config module
        mock_config = type(sys)("mock_config")
        mock_config.LoaderPreference = LoaderPreference
        sys.modules[module_name] = mock_config
        return mock_config

    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


# Import base path
base_path = Path(
    "/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core"
)

# Import modules
config_module = import_module_from_file(
    "haive.core.engine.document.config", base_path / "engine" / "document" / "config.py"
)

source_base_module = import_module_from_file(
    "haive.core.engine.document.loaders.sources.source_base",
    base_path / "engine" / "document" / "loaders" / "sources" / "source_base.py",
)

registry_module = import_module_from_file(
    "haive.core.engine.document.loaders.sources.registry",
    base_path / "engine" / "document" / "loaders" / "sources" / "registry.py",
)


def test_loader_selection_fix():
    """Test the specific loader selection fix."""
    register_source = registry_module.register_source
    source_registry = registry_module.source_registry
    LocalSource = source_base_module.LocalSource


    # Clear the global registry
    source_registry._sources.clear()
    source_registry._extension_index.clear()
    source_registry._url_pattern_index.clear()
    source_registry._scheme_index.clear()
    source_registry._mime_index.clear()

    # Register a PDF source with explicit speed/quality settings
    @register_source(
        name="pdf",
        file_extensions=[".pdf"],
        loaders={
            "fast": {"class": "PyPDFLoader", "speed": "fast", "quality": "medium"},
            "quality": {
                "class": "UnstructuredPDFLoader",
                "quality": "high",
                "speed": "slow",
            },
        },
        default_loader="fast",
        priority=10,
    )
    class PDFSource(LocalSource):
        """PDF source for testing."""



    # Create a source
    source = source_registry.create_source("/path/to/document.pdf")

    # Test loader selection with different preferences
    fast_loader = source_registry.get_loader_for_source(
        source, preference=LoaderPreference.SPEED
    )
    quality_loader = source_registry.get_loader_for_source(
        source, preference=LoaderPreference.QUALITY
    )
    default_loader = source_registry.get_loader_for_source(source)  # No preference


    # Verify the fix worked
    assert (
        fast_loader.name == "PyPDFLoader"
    ), f"Expected PyPDFLoader for speed, got {fast_loader.name}"
    assert fast_loader.speed == "fast", f"Expected fast speed, got {fast_loader.speed}"

    assert (
        quality_loader.name == "UnstructuredPDFLoader"
    ), f"Expected UnstructuredPDFLoader for quality, got {quality_loader.name}"
    assert (
        quality_loader.quality == "high"
    ), f"Expected high quality, got {quality_loader.quality}"

    assert (
        default_loader.name == "PyPDFLoader"
    ), f"Expected default PyPDFLoader, got {default_loader.name}"


    return True


def main():
    """Run the test."""

    try:
        success = test_loader_selection_fix()

        if success:

        return success

    except Exception as e:
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
