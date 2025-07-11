from langchain_core.retrievers import BaseRetriever
from pydantic import Field

from haive.core.models.retriever.base import RetrieverConfig, RetrieverType


@RetrieverConfig.register(RetrieverType.ENSEMBLE)
class EnsembleRetrieverConfig(RetrieverConfig):
    """Configuration for ensemble retrievers."""

    retriever_configs: list[RetrieverConfig] = Field(
        default_factory=list, description="Configurations for the component retrievers"
    )
    weights: list[float] | None = Field(
        default=None, description="Optional weights for the retrievers"
    )

    def instantiate(self) -> BaseRetriever:
        """Create the ensemble retriever."""
        if not self.retriever_configs or len(self.retriever_configs) < 2:
            raise ValueError("At least two retriever_configs are required")

        # Import the specific retriever class
        from langchain_community.retrievers import EnsembleRetriever

        # Create the component retrievers
        retrievers = [config.instantiate() for config in self.retriever_configs]

        # Create and return the retriever
        return EnsembleRetriever(retrievers=retrievers, weights=self.weights)
