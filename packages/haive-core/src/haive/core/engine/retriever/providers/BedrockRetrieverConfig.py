"""Amazon Bedrock Retriever implementation for the Haive framework.

This module provides a configuration class for the Amazon Bedrock retriever,
which uses AWS Bedrock's foundation models for retrieval tasks. Bedrock provides
access to foundation models from various providers (Anthropic, AI21, etc.) and
can be used for retrieval-augmented generation workflows.

The BedrockRetriever works by:
1. Connecting to Amazon Bedrock service
2. Using foundation models for embedding generation
3. Performing semantic search using model-generated embeddings
4. Supporting various foundation model providers

This retriever is particularly useful when:
- Building RAG applications with AWS Bedrock
- Need access to multiple foundation model providers
- Want managed AI model infrastructure
- Building enterprise applications on AWS
- Need consistent API across different model providers

The implementation integrates with LangChain's BedrockRetriever while
providing a consistent Haive configuration interface with secure AWS credential management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType
from haive.core.engine.vectorstore.vectorstore import VectorStoreConfig


@BaseRetrieverConfig.register(RetrieverType.BEDROCK)
class BedrockRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    """Configuration for Amazon Bedrock retriever in the Haive framework.

    This retriever uses AWS Bedrock foundation models for embedding generation
    and retrieval tasks within RAG workflows.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always BEDROCK).
        vectorstore_config (VectorStoreConfig): Vector store for document storage.
        model_id (str): Bedrock foundation model ID for embeddings.
        region_name (str): AWS region name.
        api_key (Optional[SecretStr]): AWS access key (auto-resolved from AWS_ACCESS_KEY_ID).
        secret_key (Optional[SecretStr]): AWS secret key (auto-resolved from AWS_SECRET_ACCESS_KEY).
        k (int): Number of documents to retrieve.

    Examples:
        >>> from haive.core.engine.retriever import BedrockRetrieverConfig
        >>> from haive.core.engine.vectorstore.providers.FAISSVectorStoreConfig import FAISSVectorStoreConfig
        >>>
        >>> # Configure vector store
        >>> vectorstore_config = FAISSVectorStoreConfig(
        ...     name="bedrock_faiss_store",
        ...     index_name="bedrock_index"
        ... )
        >>>
        >>> # Create the Bedrock retriever config
        >>> config = BedrockRetrieverConfig(
        ...     name="bedrock_retriever",
        ...     vectorstore_config=vectorstore_config,
        ...     model_id="amazon.titan-embed-text-v1",
        ...     region_name="us-east-1",
        ...     k=10
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("cloud computing best practices")
        >>>
        >>> # Example with different embedding model
        >>> anthropic_config = BedrockRetrieverConfig(
        ...     name="anthropic_bedrock_retriever",
        ...     vectorstore_config=vectorstore_config,
        ...     model_id="anthropic.claude-instant-v1",
        ...     region_name="us-west-2"
        ... )
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.BEDROCK, description="The type of retriever"
    )

    # Vector store configuration
    vectorstore_config: VectorStoreConfig = Field(
        ..., description="Vector store configuration for document storage"
    )

    # Bedrock model configuration
    model_id: str = Field(
        default="amazon.titan-embed-text-v1",
        description="Bedrock foundation model ID for embeddings",
    )

    region_name: str = Field(default="us-east-1", description="AWS region name")

    # API configuration with SecureConfigMixin
    api_key: SecretStr | None = Field(
        default=None,
        description="AWS access key ID (auto-resolved from AWS_ACCESS_KEY_ID)",
    )

    secret_key: SecretStr | None = Field(
        default=None,
        description="AWS secret access key (auto-resolved from AWS_SECRET_ACCESS_KEY)",
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="aws", description="Provider name for credential resolution"
    )

    # Search parameters
    k: int = Field(
        default=10, ge=1, le=100, description="Number of documents to retrieve"
    )

    # Bedrock specific parameters
    model_kwargs: dict[str, Any] | None = Field(
        default=None, description="Additional model parameters for Bedrock calls"
    )

    endpoint_url: str | None = Field(
        default=None, description="Custom Bedrock endpoint URL (for VPC endpoints)"
    )

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for Bedrock retriever."""
        return {
            "query": (
                str,
                Field(description="Search query for Bedrock-powered retrieval"),
            ),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for Bedrock retriever."""
        return {
            "documents": (
                list[Document],
                Field(
                    default_factory=list,
                    description="Documents from Bedrock-powered search",
                ),
            ),
        }

    def instantiate(self):
        """Create an Amazon Bedrock retriever from this configuration.

        Returns:
            BedrockRetriever: Instantiated retriever ready for foundation model-powered search.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If AWS credentials or configuration is invalid.
        """
        try:
            import boto3
            from langchain_aws.embeddings import BedrockEmbeddings
        except ImportError:
            raise ImportError(
                "BedrockRetriever requires langchain-aws and boto3 packages. "
                "Install with: pip install langchain-aws boto3"
            )

        # Get AWS credentials using SecureConfigMixin approach
        access_key = self.get_api_key()
        secret_key = self.secret_key.get_secret_value() if self.secret_key else None

        # Configure AWS session
        session_kwargs = {"region_name": self.region_name}
        if access_key and secret_key:
            session_kwargs.update(
                {"aws_access_key_id": access_key, "aws_secret_access_key": secret_key}
            )

        session = boto3.Session(**session_kwargs)

        # Create Bedrock client
        bedrock_kwargs = {"region_name": self.region_name}
        if self.endpoint_url:
            bedrock_kwargs["endpoint_url"] = self.endpoint_url

        bedrock_client = session.client("bedrock-runtime", **bedrock_kwargs)

        # Create Bedrock embeddings
        embedding_kwargs = {"client": bedrock_client, "model_id": self.model_id}

        if self.model_kwargs:
            embedding_kwargs["model_kwargs"] = self.model_kwargs

        BedrockEmbeddings(**embedding_kwargs)

        # Instantiate vector store with Bedrock embeddings
        vectorstore = self.vectorstore_config.instantiate()

        # Configure retriever
        search_kwargs = {"k": self.k}

        # Return the vector store as retriever with Bedrock embeddings
        return vectorstore.as_retriever(search_kwargs=search_kwargs)
