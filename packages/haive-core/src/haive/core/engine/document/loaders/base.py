import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Type, Union

from langchain_core.documents import Document
from langchain_core.runnables import RunnableConfig
from pydantic import Field, computed_field

from haive.core.engine.base import EngineType, InvokableEngine
from haive.core.engine.loaders.base import BaseDocumentLoader
from haive.core.engine.loaders.source_factory import SourceFactory
from haive.core.engine.loaders.sources.base import BaseSource
from haive.core.engine.loaders.sources.types import SourceType


class DocumentLoaderEngine(
    InvokableEngine[Union[BaseSource, str, Path, Dict[str, Any]], List[Document]]
):
    """
    Engine for loading documents from various sources.

    This engine handles:
    1. Auto-detection and creation of source objects
    2. Subsource finding for complex sources
    3. Document loading from sources
    4. Enriching documents with source metadata
    """

    engine_type: EngineType = Field(default=EngineType.DOCUMENT_LOADER)

    # Loader configuration
    loader_name: str = Field(description="Name of the document loader to use")
    supported_source_types: List[SourceType] = Field(
        default_factory=list,
        description="Source types this loader supports (empty list = all types)",
    )

    # Loading behavior
    use_subsources: bool = Field(
        default=False, description="Whether to use subsource finding if available"
    )
    recursive: bool = Field(
        default=False, description="Whether to recursively load from directory sources"
    )
    max_documents: Optional[int] = Field(
        default=None, description="Maximum number of documents to load"
    )

    # Source handling
    auto_detect_source: bool = Field(
        default=True, description="Whether to auto-detect source type if not provided"
    )

    # Loader-specific options
    loader_options: Dict[str, Any] = Field(
        default_factory=dict, description="Additional options for the loader"
    )

    # Track loaded sources
    _loaded_sources: Dict[str, int] = Field(
        default_factory=dict,
        description="Sources loaded and document count",
        exclude=True,
    )

    # Execution logs
    _execution_log: List[Dict[str, Any]] = Field(
        default_factory=list, description="Log of loading operations", exclude=True
    )

    model_config = {"arbitrary_types_allowed": True}

    @computed_field
    def supported_source_types_names(self) -> List[str]:
        """Get supported source type names."""
        return [t.value for t in self.supported_source_types]

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Define input field requirements."""
        from pydantic import Field

        return {
            "source": (
                Union[BaseSource, str, Path, Dict[str, Any]],
                Field(description="Source to load documents from"),
            ),
            "recursive": (
                bool,
                Field(
                    default=self.recursive,
                    description="Whether to recursively load from directory sources",
                ),
            ),
            "use_subsources": (
                bool,
                Field(
                    default=self.use_subsources,
                    description="Whether to use subsource finding if available",
                ),
            ),
            "max_documents": (
                Optional[int],
                Field(
                    default=self.max_documents,
                    description="Maximum number of documents to load",
                ),
            ),
            "loader_options": (
                Dict[str, Any],
                Field(
                    default_factory=dict,
                    description="Additional options for the loader",
                ),
            ),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Define output field requirements."""
        from pydantic import Field

        return {
            "documents": (List[Document], Field(description="Loaded documents")),
            "metadata": (
                Dict[str, Any],
                Field(
                    default_factory=dict,
                    description="Metadata about the loading process",
                ),
            ),
        }

    def create_runnable(
        self, runnable_config: Optional[RunnableConfig] = None
    ) -> BaseDocumentLoader:
        """Create a document loader instance."""
        from haive.core.registry.base import LoaderRegistry

        # Get loader class from registry
        loader_cls = LoaderRegistry.get_instance().get_loader(self.loader_name)
        if not loader_cls:
            raise ValueError(f"No loader found with name: {self.loader_name}")

        # Extract config parameters
        params = self.apply_runnable_config(runnable_config) or {}

        # Merge loader options from parameters and instance
        loader_options = self.loader_options.copy()
        if "loader_options" in params:
            loader_options.update(params["loader_options"])

        # Create loader instance
        return loader_cls(
            name=self.loader_name,
            supported_source_types=self.supported_source_types,
            **loader_options,
        )

    def _prepare_source(
        self, input_data: Union[BaseSource, str, Path, Dict[str, Any]]
    ) -> BaseSource:
        """
        Prepare source from input data.

        Args:
            input_data: Input data to prepare source from

        Returns:
            Prepared source

        Raises:
            ValueError: If source cannot be prepared
        """
        # Already a BaseSource
        if isinstance(input_data, BaseSource):
            return input_data

        # Dictionary with source configuration
        if isinstance(input_data, dict):
            # Use explicit source_type if provided
            source_type = None
            if "source_type" in input_data:
                source_type_value = input_data["source_type"]
                if isinstance(source_type_value, SourceType):
                    source_type = source_type_value
                elif isinstance(source_type_value, str):
                    try:
                        source_type = SourceType(source_type_value)
                    except ValueError:
                        pass

            # Create source
            source = SourceFactory.create_source(input_data, source_type=source_type)
            if not source:
                raise ValueError(f"Could not create source from input: {input_data}")
            return source

        # Auto-detect from string or Path
        source = SourceFactory.create_source(input_data)
        if not source:
            raise ValueError(f"Could not detect source type for: {input_data}")

        return source

    def _validate_source(self, source: BaseSource) -> None:
        """
        Validate that the source is supported by this loader.

        Args:
            source: Source to validate

        Raises:
            ValueError: If source is not supported
        """
        # Check if the source type is supported
        if (
            self.supported_source_types
            and source.source_type not in self.supported_source_types
        ):
            raise ValueError(
                f"Source type {source.source_type} not supported by {self.loader_name}. "
                f"Supported types: {', '.join(self.supported_source_types_names)}"
            )

    def invoke(
        self,
        input_data: Union[BaseSource, str, Path, Dict[str, Any]],
        runnable_config: Optional[RunnableConfig] = None,
    ) -> List[Document]:
        """
        Load documents from a source.

        Args:
            input_data: Source to load documents from
            runnable_config: Optional runtime configuration

        Returns:
            List of loaded documents
        """
        # Extract config parameters
        params = self.apply_runnable_config(runnable_config) or {}

        # Get loading options
        params.get("recursive", self.recursive)
        use_subsources = params.get("use_subsources", self.use_subsources)
        max_documents = params.get("max_documents", self.max_documents)

        # Prepare and validate source
        source = self._prepare_source(input_data)
        self._validate_source(source)

        # Create loader
        loader = self.create_runnable(runnable_config)

        # Initialize execution metadata
        exec_metadata = {
            "source_id": source.source_id,
            "source_type": str(source.source_type),
            "loader": self.loader_name,
            "start_time": datetime.now().isoformat(),
        }

        # Check if loader supports subsources and we want to use them
        if use_subsources and hasattr(loader, "find_subsources"):
            # Find subsources
            try:
                subsources = loader.find_subsources(source)
                exec_metadata["subsource_count"] = len(subsources)

                # Load documents from each subsource
                all_documents = []
                for subsource in subsources:
                    sub_docs = loader.load(subsource)
                    all_documents.extend(sub_docs)

                    # Track loaded source
                    self._loaded_sources[subsource.source_id] = len(sub_docs)

                    # Check max documents
                    if max_documents and len(all_documents) >= max_documents:
                        all_documents = all_documents[:max_documents]
                        break

                # Update execution metadata
                exec_metadata["document_count"] = len(all_documents)
                exec_metadata["end_time"] = datetime.now().isoformat()
                self._execution_log.append(exec_metadata)

                return all_documents
            except Exception as e:
                # Fall back to direct loading if subsource finding fails
                logging.warning(
                    f"Subsource finding failed, falling back to direct loading: {e}"
                )

        # Direct loading
        try:
            documents = loader.load(source)

            # Track loaded source
            self._loaded_sources[source.source_id] = len(documents)

            # Apply max documents limit
            if max_documents and len(documents) > max_documents:
                documents = documents[:max_documents]

            # Update execution metadata
            exec_metadata["document_count"] = len(documents)
            exec_metadata["end_time"] = datetime.now().isoformat()
            self._execution_log.append(exec_metadata)

            return documents
        except Exception as e:
            # Update execution metadata with error
            exec_metadata["error"] = str(e)
            exec_metadata["end_time"] = datetime.now().isoformat()
            self._execution_log.append(exec_metadata)

            raise ValueError(f"Error loading documents: {e}")

    @property
    def execution_log(self) -> List[Dict[str, Any]]:
        """Get the execution log."""
        return self._execution_log

    @property
    def loaded_sources(self) -> Dict[str, int]:
        """Get the loaded sources and document counts."""
        return self._loaded_sources
