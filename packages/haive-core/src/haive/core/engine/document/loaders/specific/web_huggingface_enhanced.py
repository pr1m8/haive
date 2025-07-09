"""Enhanced HuggingFace Loaders with Additional Features.

This module contains enhanced HuggingFace loaders for papers, collections,
organizations, and extended dataset/model features.
"""

import logging
from typing import List, Optional

from langchain_core.document_loaders.base import BaseLoader
from langchain_core.documents import Document

from haive.core.engine.document.loaders.sources.implementation import WebSource

logger = logging.getLogger(__name__)


class HuggingFacePapersSource(WebSource):
    """HuggingFace Papers loader for academic papers linked to models/datasets."""

    def __init__(
        self,
        model_id: Optional[str] = None,
        dataset_id: Optional[str] = None,
        paper_id: Optional[str] = None,
        include_abstract: bool = True,
        include_authors: bool = True,
        include_citations: bool = False,
        **kwargs,
    ):
        source_path = "huggingface://papers"
        if paper_id:
            source_path = f"huggingface://papers/{paper_id}"
        elif model_id:
            source_path = f"huggingface://models/{model_id}/papers"
        elif dataset_id:
            source_path = f"huggingface://datasets/{dataset_id}/papers"

        super().__init__(source_path=source_path, **kwargs)
        self.model_id = model_id
        self.dataset_id = dataset_id
        self.paper_id = paper_id
        self.include_abstract = include_abstract
        self.include_authors = include_authors
        self.include_citations = include_citations

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a HuggingFace Papers loader."""
        try:
            return HuggingFacePapersLoader(
                model_id=self.model_id,
                dataset_id=self.dataset_id,
                paper_id=self.paper_id,
                include_abstract=self.include_abstract,
                include_authors=self.include_authors,
                include_citations=self.include_citations,
            )

        except Exception as e:
            logger.error(f"Failed to create HuggingFace Papers loader: {e}")
            return None


class HuggingFaceCollectionsSource(WebSource):
    """HuggingFace Collections loader for curated model/dataset collections."""

    def __init__(
        self,
        collection_id: Optional[str] = None,
        username: Optional[str] = None,
        include_models: bool = True,
        include_datasets: bool = True,
        include_spaces: bool = True,
        **kwargs,
    ):
        if collection_id:
            source_path = f"huggingface://collections/{collection_id}"
        elif username:
            source_path = f"huggingface://users/{username}/collections"
        else:
            source_path = "huggingface://collections"

        super().__init__(source_path=source_path, **kwargs)
        self.collection_id = collection_id
        self.username = username
        self.include_models = include_models
        self.include_datasets = include_datasets
        self.include_spaces = include_spaces

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a HuggingFace Collections loader."""
        try:
            return HuggingFaceCollectionsLoader(
                collection_id=self.collection_id,
                username=self.username,
                include_models=self.include_models,
                include_datasets=self.include_datasets,
                include_spaces=self.include_spaces,
            )

        except Exception as e:
            logger.error(f"Failed to create HuggingFace Collections loader: {e}")
            return None


class HuggingFaceOrganizationsSource(WebSource):
    """HuggingFace Organizations loader for organization profiles and resources."""

    def __init__(
        self,
        org_name: str,
        include_members: bool = True,
        include_models: bool = True,
        include_datasets: bool = True,
        include_spaces: bool = True,
        **kwargs,
    ):
        source_path = f"huggingface://organizations/{org_name}"
        super().__init__(source_path=source_path, **kwargs)
        self.org_name = org_name
        self.include_members = include_members
        self.include_models = include_models
        self.include_datasets = include_datasets
        self.include_spaces = include_spaces

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a HuggingFace Organizations loader."""
        try:
            return HuggingFaceOrganizationsLoader(
                org_name=self.org_name,
                include_members=self.include_members,
                include_models=self.include_models,
                include_datasets=self.include_datasets,
                include_spaces=self.include_spaces,
            )

        except Exception as e:
            logger.error(f"Failed to create HuggingFace Organizations loader: {e}")
            return None


class HuggingFaceExtendedDatasetSource(WebSource):
    """Extended HuggingFace Dataset loader with additional features."""

    def __init__(
        self,
        dataset_name: str,
        config_name: Optional[str] = None,
        split: Optional[str] = None,
        streaming: bool = False,
        num_examples: Optional[int] = None,
        include_dataset_info: bool = True,
        include_feature_info: bool = True,
        cache_dir: Optional[str] = None,
        **kwargs,
    ):
        source_path = f"huggingface://datasets/{dataset_name}"
        super().__init__(source_path=source_path, **kwargs)
        self.dataset_name = dataset_name
        self.config_name = config_name
        self.split = split
        self.streaming = streaming
        self.num_examples = num_examples
        self.include_dataset_info = include_dataset_info
        self.include_feature_info = include_feature_info
        self.cache_dir = cache_dir

    def create_loader(self) -> Optional[BaseLoader]:
        """Create an extended HuggingFace Dataset loader."""
        try:
            from langchain_community.document_loaders import HuggingFaceDatasetLoader

            # Enhanced loader with additional options
            loader = HuggingFaceDatasetLoader(
                dataset_name=self.dataset_name,
                name=self.config_name,
                page_content_column="text",  # Default column
                cache_dir=self.cache_dir,
            )

            # Wrap with extended functionality
            return ExtendedHuggingFaceDatasetLoader(
                base_loader=loader,
                dataset_name=self.dataset_name,
                config_name=self.config_name,
                split=self.split,
                streaming=self.streaming,
                num_examples=self.num_examples,
                include_dataset_info=self.include_dataset_info,
                include_feature_info=self.include_feature_info,
            )

        except ImportError:
            logger.warning(
                "HuggingFaceDatasetLoader not available. Install with: pip install datasets"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create extended HuggingFace Dataset loader: {e}")
            return None


class HuggingFaceModelCardSource(WebSource):
    """HuggingFace Model Card loader with extended information."""

    def __init__(
        self,
        model_id: str,
        include_readme: bool = True,
        include_config: bool = True,
        include_tokenizer_config: bool = True,
        include_training_args: bool = True,
        include_carbon_footprint: bool = True,
        **kwargs,
    ):
        source_path = f"huggingface://models/{model_id}"
        super().__init__(source_path=source_path, **kwargs)
        self.model_id = model_id
        self.include_readme = include_readme
        self.include_config = include_config
        self.include_tokenizer_config = include_tokenizer_config
        self.include_training_args = include_training_args
        self.include_carbon_footprint = include_carbon_footprint

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a HuggingFace Model Card loader."""
        try:
            return HuggingFaceModelCardLoader(
                model_id=self.model_id,
                include_readme=self.include_readme,
                include_config=self.include_config,
                include_tokenizer_config=self.include_tokenizer_config,
                include_training_args=self.include_training_args,
                include_carbon_footprint=self.include_carbon_footprint,
            )

        except Exception as e:
            logger.error(f"Failed to create HuggingFace Model Card loader: {e}")
            return None


# Custom loader implementations


class HuggingFacePapersLoader(BaseLoader):
    """Custom loader for HuggingFace Papers."""

    def __init__(
        self,
        model_id: Optional[str] = None,
        dataset_id: Optional[str] = None,
        paper_id: Optional[str] = None,
        include_abstract: bool = True,
        include_authors: bool = True,
        include_citations: bool = False,
    ):
        self.model_id = model_id
        self.dataset_id = dataset_id
        self.paper_id = paper_id
        self.include_abstract = include_abstract
        self.include_authors = include_authors
        self.include_citations = include_citations

    def load(self) -> List[Document]:
        """Load papers from HuggingFace."""
        try:
            from huggingface_hub import HfApi

            api = HfApi()
            documents = []

            if self.paper_id:
                # Load specific paper
                # Note: HuggingFace API doesn't directly expose papers endpoint
                # This is a placeholder for when the API supports it
                content = f"# Paper: {self.paper_id}\n\n"
                content += "Note: Direct paper loading from HuggingFace requires API support.\n"

                metadata = {
                    "source": f"huggingface://papers/{self.paper_id}",
                    "type": "huggingface_paper",
                    "paper_id": self.paper_id,
                }

                documents.append(Document(page_content=content, metadata=metadata))

            elif self.model_id:
                # Load papers associated with a model
                try:
                    model_info = api.model_info(self.model_id)
                    if hasattr(model_info, "paper_url") and model_info.paper_url:
                        content = f"# Papers for Model: {self.model_id}\n\n"
                        content += f"**Paper URL:** {model_info.paper_url}\n"

                        metadata = {
                            "source": f"huggingface://models/{self.model_id}/papers",
                            "type": "huggingface_model_paper",
                            "model_id": self.model_id,
                            "paper_url": model_info.paper_url,
                        }

                        documents.append(
                            Document(page_content=content, metadata=metadata)
                        )
                except Exception as e:
                    logger.error(f"Failed to get model papers: {e}")

            elif self.dataset_id:
                # Load papers associated with a dataset
                try:
                    dataset_info = api.dataset_info(self.dataset_id)
                    if hasattr(dataset_info, "citation") and dataset_info.citation:
                        content = f"# Citation for Dataset: {self.dataset_id}\n\n"
                        content += f"```bibtex\n{dataset_info.citation}\n```\n"

                        metadata = {
                            "source": f"huggingface://datasets/{self.dataset_id}/papers",
                            "type": "huggingface_dataset_citation",
                            "dataset_id": self.dataset_id,
                        }

                        documents.append(
                            Document(page_content=content, metadata=metadata)
                        )
                except Exception as e:
                    logger.error(f"Failed to get dataset papers: {e}")

            return documents

        except ImportError:
            logger.warning(
                "huggingface_hub not available. Install with: pip install huggingface_hub"
            )
            return []
        except Exception as e:
            logger.error(f"Failed to load HuggingFace papers: {e}")
            return []


class HuggingFaceCollectionsLoader(BaseLoader):
    """Custom loader for HuggingFace Collections."""

    def __init__(
        self,
        collection_id: Optional[str] = None,
        username: Optional[str] = None,
        include_models: bool = True,
        include_datasets: bool = True,
        include_spaces: bool = True,
    ):
        self.collection_id = collection_id
        self.username = username
        self.include_models = include_models
        self.include_datasets = include_datasets
        self.include_spaces = include_spaces

    def load(self) -> List[Document]:
        """Load collections from HuggingFace."""
        try:
            from huggingface_hub import HfApi

            HfApi()
            documents = []

            # Note: HuggingFace Collections API is evolving
            # This is a placeholder implementation
            content = "# HuggingFace Collections\n\n"

            if self.collection_id:
                content += f"**Collection ID:** {self.collection_id}\n"
            elif self.username:
                content += f"**User Collections:** {self.username}\n"

            content += "\nNote: Collections API support is limited. "
            content += "Visit HuggingFace website for full collections browsing.\n"

            metadata = {
                "source": "huggingface://collections",
                "type": "huggingface_collection",
            }

            if self.collection_id:
                metadata["collection_id"] = self.collection_id
            if self.username:
                metadata["username"] = self.username

            documents.append(Document(page_content=content, metadata=metadata))

            return documents

        except ImportError:
            logger.warning(
                "huggingface_hub not available. Install with: pip install huggingface_hub"
            )
            return []
        except Exception as e:
            logger.error(f"Failed to load HuggingFace collections: {e}")
            return []


class HuggingFaceOrganizationsLoader(BaseLoader):
    """Custom loader for HuggingFace Organizations."""

    def __init__(
        self,
        org_name: str,
        include_members: bool = True,
        include_models: bool = True,
        include_datasets: bool = True,
        include_spaces: bool = True,
    ):
        self.org_name = org_name
        self.include_members = include_members
        self.include_models = include_models
        self.include_datasets = include_datasets
        self.include_spaces = include_spaces

    def load(self) -> List[Document]:
        """Load organization data from HuggingFace."""
        try:
            from huggingface_hub import HfApi

            api = HfApi()
            documents = []

            content = f"# HuggingFace Organization: {self.org_name}\n\n"

            # Get organization models
            if self.include_models:
                try:
                    models = api.list_models(author=self.org_name, limit=10)
                    content += "## Models\n\n"
                    for model in models:
                        content += f"- [{model.modelId}](https://huggingface.co/{model.modelId})\n"
                        if hasattr(model, "downloads"):
                            content += f"  - Downloads: {model.downloads}\n"
                        if hasattr(model, "likes"):
                            content += f"  - Likes: {model.likes}\n"
                    content += "\n"
                except Exception as e:
                    logger.error(f"Failed to get organization models: {e}")

            # Get organization datasets
            if self.include_datasets:
                try:
                    datasets = api.list_datasets(author=self.org_name, limit=10)
                    content += "## Datasets\n\n"
                    for dataset in datasets:
                        content += f"- [{dataset.id}](https://huggingface.co/datasets/{dataset.id})\n"
                        if hasattr(dataset, "downloads"):
                            content += f"  - Downloads: {dataset.downloads}\n"
                        if hasattr(dataset, "likes"):
                            content += f"  - Likes: {dataset.likes}\n"
                    content += "\n"
                except Exception as e:
                    logger.error(f"Failed to get organization datasets: {e}")

            # Get organization spaces
            if self.include_spaces:
                try:
                    spaces = api.list_spaces(author=self.org_name, limit=10)
                    content += "## Spaces\n\n"
                    for space in spaces:
                        content += f"- [{space.id}](https://huggingface.co/spaces/{space.id})\n"
                        if hasattr(space, "likes"):
                            content += f"  - Likes: {space.likes}\n"
                    content += "\n"
                except Exception as e:
                    logger.error(f"Failed to get organization spaces: {e}")

            metadata = {
                "source": f"huggingface://organizations/{self.org_name}",
                "type": "huggingface_organization",
                "org_name": self.org_name,
            }

            documents.append(Document(page_content=content, metadata=metadata))

            return documents

        except ImportError:
            logger.warning(
                "huggingface_hub not available. Install with: pip install huggingface_hub"
            )
            return []
        except Exception as e:
            logger.error(f"Failed to load HuggingFace organization: {e}")
            return []


class ExtendedHuggingFaceDatasetLoader(BaseLoader):
    """Extended wrapper for HuggingFace Dataset loader."""

    def __init__(
        self,
        base_loader: BaseLoader,
        dataset_name: str,
        config_name: Optional[str] = None,
        split: Optional[str] = None,
        streaming: bool = False,
        num_examples: Optional[int] = None,
        include_dataset_info: bool = True,
        include_feature_info: bool = True,
    ):
        self.base_loader = base_loader
        self.dataset_name = dataset_name
        self.config_name = config_name
        self.split = split
        self.streaming = streaming
        self.num_examples = num_examples
        self.include_dataset_info = include_dataset_info
        self.include_feature_info = include_feature_info

    def load(self) -> List[Document]:
        """Load dataset with extended information."""
        documents = []

        try:
            # Load base documents
            base_docs = self.base_loader.load()

            # Add extended information
            if self.include_dataset_info:
                from datasets import load_dataset_builder

                builder = load_dataset_builder(self.dataset_name, self.config_name)
                info_content = f"# Dataset Info: {self.dataset_name}\n\n"
                info_content += f"**Description:** {builder.info.description}\n"
                info_content += f"**Version:** {builder.info.version}\n"
                info_content += f"**License:** {builder.info.license}\n"

                if builder.info.features:
                    info_content += "\n## Features\n\n"
                    for feature_name, feature_type in builder.info.features.items():
                        info_content += f"- **{feature_name}:** {feature_type}\n"

                metadata = {
                    "source": f"huggingface://datasets/{self.dataset_name}/info",
                    "type": "huggingface_dataset_info",
                    "dataset_name": self.dataset_name,
                }

                documents.append(Document(page_content=info_content, metadata=metadata))

            # Add base documents with limited examples
            if self.num_examples and base_docs:
                base_docs = base_docs[: self.num_examples]

            documents.extend(base_docs)

        except Exception as e:
            logger.error(f"Failed to load extended dataset info: {e}")
            # Fallback to base loader
            try:
                documents = self.base_loader.load()
            except Exception as e2:
                logger.error(f"Failed to load base dataset: {e2}")

        return documents


class HuggingFaceModelCardLoader(BaseLoader):
    """Custom loader for HuggingFace Model Cards with extended info."""

    def __init__(
        self,
        model_id: str,
        include_readme: bool = True,
        include_config: bool = True,
        include_tokenizer_config: bool = True,
        include_training_args: bool = True,
        include_carbon_footprint: bool = True,
    ):
        self.model_id = model_id
        self.include_readme = include_readme
        self.include_config = include_config
        self.include_tokenizer_config = include_tokenizer_config
        self.include_training_args = include_training_args
        self.include_carbon_footprint = include_carbon_footprint

    def load(self) -> List[Document]:
        """Load model card and extended information."""
        try:
            from huggingface_hub import HfApi, hf_hub_download

            api = HfApi()
            documents = []

            # Get model info
            model_info = api.model_info(self.model_id)

            content = f"# Model Card: {self.model_id}\n\n"

            # Basic info
            content += f"**Author:** {model_info.author}\n"
            if hasattr(model_info, "downloads"):
                content += f"**Downloads:** {model_info.downloads}\n"
            if hasattr(model_info, "likes"):
                content += f"**Likes:** {model_info.likes}\n"
            if hasattr(model_info, "tags") and model_info.tags:
                content += f"**Tags:** {', '.join(model_info.tags)}\n"
            content += "\n"

            # Model card content
            if self.include_readme:
                try:
                    readme_path = hf_hub_download(
                        repo_id=self.model_id,
                        filename="README.md",
                        repo_type="model",
                    )
                    with open(readme_path, "r") as f:
                        readme_content = f.read()
                    content += "## Model Card\n\n"
                    content += readme_content + "\n\n"
                except Exception as e:
                    logger.warning(f"Could not load README: {e}")

            # Config files
            if self.include_config:
                try:
                    config_path = hf_hub_download(
                        repo_id=self.model_id,
                        filename="config.json",
                        repo_type="model",
                    )
                    with open(config_path, "r") as f:
                        config_content = f.read()
                    content += "## Model Config\n\n```json\n"
                    content += config_content + "\n```\n\n"
                except Exception as e:
                    logger.warning(f"Could not load config: {e}")

            metadata = {
                "source": f"huggingface://models/{self.model_id}",
                "type": "huggingface_model_card",
                "model_id": self.model_id,
                "author": model_info.author,
            }

            if hasattr(model_info, "pipeline_tag"):
                metadata["pipeline_tag"] = model_info.pipeline_tag

            documents.append(Document(page_content=content, metadata=metadata))

            return documents

        except ImportError:
            logger.warning(
                "huggingface_hub not available. Install with: pip install huggingface_hub"
            )
            return []
        except Exception as e:
            logger.error(f"Failed to load model card: {e}")
            return []


# Export enhanced HuggingFace sources
__all__ = [
    "HuggingFacePapersSource",
    "HuggingFaceCollectionsSource",
    "HuggingFaceOrganizationsSource",
    "HuggingFaceExtendedDatasetSource",
    "HuggingFaceModelCardSource",
    "HuggingFacePapersLoader",
    "HuggingFaceCollectionsLoader",
    "HuggingFaceOrganizationsLoader",
    "ExtendedHuggingFaceDatasetLoader",
    "HuggingFaceModelCardLoader",
]
