"""Auto Loader Factory for Document Engine.

This module provides a comprehensive factory interface that can analyze any path or URL
and automatically select the appropriate document source and loader.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from langchain_core.document_loaders.base import BaseLoader

from haive.core.engine.document.loaders.sources.implementation import (
    CredentialManager,
    EnhancedSource,
    SourceType,
    source_registry,
)
from haive.core.engine.document.loaders.strategy import (
    create_loader as create_strategy_loader,
)
from haive.core.engine.document.loaders.strategy import (
    strategy_registry,
)
from haive.core.engine.document.path_analysis import (
    PathAnalysisResult,
    analyze_path_comprehensive,
)

logger = logging.getLogger(__name__)


class AutoLoaderFactory:
    """Factory for automatically creating document loaders."""

    def __init__(self, credential_manager: Optional[CredentialManager] = None):
        """Initialize the factory.

        Args:
            credential_manager: Optional credential manager for authenticated sources
        """
        self.credential_manager = credential_manager or CredentialManager()

    def create_loader(
        self,
        path: str,
        strategy: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        preferences: Optional[Dict[str, Any]] = None,
    ) -> Optional[BaseLoader]:
        """Create the appropriate document loader for any path or URL.

        This factory function analyzes the given path to determine its nature (file, URL,
        database URI, etc.) and returns the appropriate loader instance.

        Args:
            path: File path, URL, or URI to load
            strategy: Optional specific strategy to use (e.g., 'pdf_pymupdf', 'playwright')
            options: Optional loader-specific options
            preferences: Optional preferences for loader selection

        Returns:
            DocumentLoader instance appropriate for the given path

        Examples:
            >>> factory = AutoLoaderFactory()
            >>>
            >>> # Load a PDF file with OCR
            >>> loader = factory.create_loader("path/to/document.pdf", strategy="pdf_pymupdf")
            >>>
            >>> # Load a webpage with JavaScript support
            >>> loader = factory.create_loader("https://example.com", strategy="playwright")
            >>>
            >>> # Auto-select best loader for any source
            >>> loader = factory.create_loader("path/to/document.docx")
        """
        if options is None:
            options = {}
        if preferences is None:
            preferences = {}

        try:
            # Find the best source for this path
            source = source_registry.find_best_source(path)
            if not source:
                logger.error(f"No suitable source found for path: {path}")
                return self._create_fallback_loader(path, options)

            # Add credential manager to source
            source.credential_manager = self.credential_manager

            # Create loader using strategy system
            loader = create_strategy_loader(
                source=source,
                strategy_name=strategy,
                options=options,
                preferences=preferences,
            )

            if loader:
                logger.info(
                    f"Created loader for {path} using source {source.source_type}"
                )
                return loader
            else:
                logger.warning(f"Failed to create loader for {path}, trying fallback")
                return self._create_fallback_loader(path, options)

        except Exception as e:
            logger.error(f"Error creating loader for {path}: {e}")
            return self._create_fallback_loader(path, options)

    def _create_fallback_loader(
        self, path: str, options: Dict[str, Any]
    ) -> Optional[BaseLoader]:
        """Create a fallback loader when auto-detection fails."""
        try:
            # Try to determine type from file extension
            path_obj = Path(path)
            ext = path_obj.suffix.lower()

            fallback_strategies = {
                ".pdf": "pdf_pymupdf",
                ".docx": "docx",
                ".txt": "text_file",
                ".csv": "csv",
                ".html": "web_base",
                ".htm": "web_base",
            }

            if ext in fallback_strategies:
                strategy = strategy_registry.get_strategy(fallback_strategies[ext])
                if strategy and strategy.is_available:
                    from haive.core.engine.document.loaders.sources.implementation import (
                        LocalFileSource,
                    )

                    source = LocalFileSource(source_path=path)
                    return strategy.create_loader(source, options)

            # Last resort: try text loader
            strategy = strategy_registry.get_strategy("text_file")
            if strategy and strategy.is_available:
                from haive.core.engine.document.loaders.sources.implementation import (
                    LocalFileSource,
                )

                source = LocalFileSource(source_path=path)
                return strategy.create_loader(source, options)

            logger.error(f"No fallback loader available for {path}")
            return None

        except Exception as e:
            logger.error(f"Fallback loader creation failed for {path}: {e}")
            return None

    def analyze_path(self, path: str) -> Optional[PathAnalysisResult]:
        """Analyze a path to understand its properties."""
        try:
            return analyze_path_comprehensive(path)
        except Exception as e:
            logger.error(f"Path analysis failed for {path}: {e}")
            return None

    def get_available_strategies(self) -> List[str]:
        """Get list of available loader strategies."""
        strategies = strategy_registry.list_strategies(available_only=True)
        return [s.strategy_name for s in strategies]

    def get_supported_sources(self) -> List[SourceType]:
        """Get list of supported source types."""
        return list(SourceType)


def create_document_loader(
    path: str,
    strategy: Optional[str] = None,
    credential_manager: Optional[CredentialManager] = None,
    options: Optional[Dict[str, Any]] = None,
    preferences: Optional[Dict[str, Any]] = None,
) -> Optional[BaseLoader]:
    """Convenience function to create a document loader.

    Args:
        path: File path, URL, or URI to load
        strategy: Optional specific strategy to use
        credential_manager: Optional credential manager
        options: Optional loader-specific options
        preferences: Optional preferences for loader selection

    Returns:
        DocumentLoader instance or None if creation failed
    """
    factory = AutoLoaderFactory(credential_manager)
    return factory.create_loader(path, strategy, options, preferences)


def analyze_source(path: str) -> Optional[Dict[str, Any]]:
    """Analyze a source path and return detailed information.

    Args:
        path: Path to analyze

    Returns:
        Dictionary with analysis results or None if analysis failed
    """
    factory = AutoLoaderFactory()

    # Get path analysis
    path_analysis = factory.analyze_path(path)
    if not path_analysis:
        return None

    # Find best source
    source = source_registry.find_best_source(path)
    if not source:
        return None

    # Find suitable strategies
    strategies = strategy_registry.find_strategies_for_source(source)

    return {
        "path": path,
        "path_analysis": (
            path_analysis.model_dump()
            if hasattr(path_analysis, "model_dump")
            else str(path_analysis)
        ),
        "source_type": source.source_type.value,
        "requires_authentication": source.requires_authentication(),
        "available_strategies": [s.strategy_name for s in strategies],
        "recommended_strategy": strategies[0].strategy_name if strategies else None,
        "source_confidence": source.get_confidence_score(path),
    }


# Export key components
__all__ = [
    "AutoLoaderFactory",
    "create_document_loader",
    "analyze_source",
]
