"""Auto factory for creating document loaders.

This module provides the main interface for automatically creating
document loaders from paths. It ties together path analysis, source
detection, and loader creation.
"""

import logging
from typing import Any, Dict, List, Optional, Union

from langchain_core.document_loaders import BaseLoader

from haive.core.engine.document.config import (
    DocumentInput,
    DocumentOutput,
    LoaderPreference,
    ProcessedDocument,
)
from haive.core.engine.document.loaders.path_analyzer import analyze_path
from haive.core.engine.document.loaders.sources.registry import source_registry
from haive.core.engine.document.loaders.sources.source_base import BaseSource

logger = logging.getLogger(__name__)


class DocumentLoaderFactory:
    """Factory for creating document loaders automatically."""

    def __init__(self):
        self._loader_cache: Dict[str, BaseLoader] = {}

    def create_loader_from_path(
        self,
        path: str,
        source_type: Optional[str] = None,
        loader_name: Optional[str] = None,
        preference: LoaderPreference = LoaderPreference.BALANCED,
        **kwargs,
    ) -> Optional[BaseLoader]:
        """Create a document loader from a path.

        Args:
            path: Path to analyze and load from
            source_type: Force a specific source type
            loader_name: Force a specific loader
            preference: Loader selection preference
            **kwargs: Additional kwargs for source/loader

        Returns:
            Document loader instance or None
        """
        # Create source
        source = self.create_source(path, source_type, **kwargs)
        if not source:
            logger.error(f"Could not create source for path: {path}")
            return None

        # Create loader from source
        return self.create_loader_from_source(source, loader_name, preference)

    def create_source(
        self, path: str, source_type: Optional[str] = None, **kwargs
    ) -> Optional[BaseSource]:
        """Create a source instance from a path.

        Args:
            path: Path to create source for
            source_type: Force a specific source type
            **kwargs: Additional source configuration

        Returns:
            Source instance or None
        """
        return source_registry.create_source(path, source_type, **kwargs)

    def create_loader_from_source(
        self,
        source: BaseSource,
        loader_name: Optional[str] = None,
        preference: LoaderPreference = LoaderPreference.BALANCED,
    ) -> Optional[BaseLoader]:
        """Create a loader instance from a source.

        Args:
            source: Source to create loader for
            loader_name: Force a specific loader
            preference: Loader selection preference

        Returns:
            Loader instance or None
        """
        # Validate source
        if not source.validate_source():
            logger.warning(f"Source validation failed: {source}")

        # Get loader mapping
        loader_mapping = source_registry.get_loader_for_source(
            source, loader_name, preference
        )

        if not loader_mapping:
            logger.error(f"No loader found for source type: {source.source_type}")
            return None

        # Create loader
        try:
            # Import loader class
            module = __import__(loader_mapping.module, fromlist=[loader_mapping.name])
            loader_class = getattr(module, loader_mapping.name)

            # Get loader kwargs from source
            loader_kwargs = source.get_loader_kwargs()

            # Create loader instance
            return loader_class(**loader_kwargs)

        except ImportError as e:
            packages = ", ".join(loader_mapping.requires_packages)
            logger.error(
                f"Failed to import {loader_mapping.name}: {e}\n"
                f"Required packages: {packages}"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create loader {loader_mapping.name}: {e}")
            return None

    def load_documents(
        self,
        input_data: Union[str, BaseSource, DocumentInput],
        preference: LoaderPreference = LoaderPreference.BALANCED,
    ) -> DocumentOutput:
        """Load documents from various input types.

        Args:
            input_data: Path, source, or DocumentInput
            preference: Loader selection preference

        Returns:
            DocumentOutput with loaded documents
        """
        # Handle DocumentInput
        if isinstance(input_data, DocumentInput):
            path = str(input_data.source)
            loader_name = input_data.loader_name
            source_type = (
                input_data.source_type.value if input_data.source_type else None
            )
        else:
            path = str(input_data) if not isinstance(input_data, BaseSource) else None
            loader_name = None
            source_type = None

        # Create source if needed
        if isinstance(input_data, BaseSource):
            source = input_data
        else:
            source = self.create_source(path, source_type)
            if not source:
                return DocumentOutput(
                    documents=[],
                    original_source=path,
                    source_type=source_type or "unknown",
                    processing_strategy="simple",
                    errors=[{"error": f"Could not create source for: {path}"}],
                )

        # Create loader
        loader = self.create_loader_from_source(source, loader_name, preference)
        if not loader:
            return DocumentOutput(
                documents=[],
                original_source=source.source_id or path,
                source_type=source.source_type or "unknown",
                processing_strategy="simple",
                errors=[
                    {
                        "error": f"Could not create loader for source: {source.source_type}"
                    }
                ],
            )

        # Load documents
        try:
            docs = loader.load()

            # Convert to ProcessedDocument
            processed_docs = []
            for doc in docs:
                processed = ProcessedDocument(
                    source=source.source_id or path,
                    source_type=source.source_type or "unknown",
                    format="unknown",  # Would need detection
                    content=doc.page_content,
                    chunks=[],  # Would need chunking
                    metadata=doc.metadata,
                    loader_name=loader.__class__.__name__,
                    processing_time=0.0,  # Would need timing
                )
                processed_docs.append(processed)

            return DocumentOutput(
                documents=processed_docs,
                original_source=source.source_id or path,
                source_type=source.source_type or "unknown",
                loader_names=[loader.__class__.__name__],
                processing_strategy="simple",
            )

        except Exception as e:
            logger.error(f"Failed to load documents: {e}")
            return DocumentOutput(
                documents=[],
                original_source=source.source_id or path,
                source_type=source.source_type or "unknown",
                processing_strategy="simple",
                errors=[{"error": str(e)}],
            )

    def find_available_loaders(self, path: str) -> List[str]:
        """Find all available loaders for a path.

        Args:
            path: Path to check

        Returns:
            List of available loader names
        """
        # Find source
        source_reg = source_registry.find_source_for_path(path)
        if not source_reg:
            return []

        return list(source_reg.loaders.keys())

    def analyze_path_with_sources(self, path: str) -> Dict[str, Any]:
        """Analyze a path and return detailed information.

        Args:
            path: Path to analyze

        Returns:
            Dictionary with analysis results and available sources/loaders
        """
        # Analyze path
        analysis = analyze_path(path)

        # Find matching source
        source_reg = source_registry.find_source_for_path(path, analysis)

        result = {
            "path": path,
            "analysis": {
                "path_type": analysis.path_type,
                "is_local": analysis.is_local,
                "is_remote": analysis.is_remote,
                "file_extension": analysis.file_extension,
                "file_category": analysis.file_category,
                "mime_type": analysis.mime_type,
            },
        }

        if source_reg:
            result["source"] = {
                "name": source_reg.name,
                "class": source_reg.source_class.__name__,
                "priority": source_reg.priority,
            }
            result["loaders"] = {
                name: {
                    "class": loader.name,
                    "speed": loader.speed,
                    "quality": loader.quality,
                    "requires_auth": loader.requires_auth,
                    "packages": loader.requires_packages,
                }
                for name, loader in source_reg.loaders.items()
            }
        else:
            result["source"] = None
            result["loaders"] = {}

        return result


# Global factory instance
document_loader_factory = DocumentLoaderFactory()


# Convenience functions
def create_loader(
    path: str,
    source_type: Optional[str] = None,
    loader_name: Optional[str] = None,
    preference: LoaderPreference = LoaderPreference.BALANCED,
    **kwargs,
) -> Optional[BaseLoader]:
    """Create a document loader from a path."""
    return document_loader_factory.create_loader_from_path(
        path, source_type, loader_name, preference, **kwargs
    )


def load_documents(
    input_data: Union[str, BaseSource, DocumentInput],
    preference: LoaderPreference = LoaderPreference.BALANCED,
) -> DocumentOutput:
    """Load documents from various input types."""
    return document_loader_factory.load_documents(input_data, preference)


def analyze_document_source(path: str) -> Dict[str, Any]:
    """Analyze a path and return source/loader information."""
    return document_loader_factory.analyze_path_with_sources(path)


__all__ = [
    "DocumentLoaderFactory",
    "document_loader_factory",
    "create_loader",
    "load_documents",
    "analyze_document_source",
]
