"""Amazon Knowledge Bases Retriever implementation for the Haive framework.

This module provides a configuration class for the Amazon Knowledge Bases retriever,
which uses AWS Bedrock Knowledge Bases for retrieval-augmented generation (RAG).
Knowledge Bases provides a fully managed service that enables RAG workflows
using foundation models with your data sources.

The AmazonKnowledgeBasesRetriever works by:
1. Connecting to an Amazon Bedrock Knowledge Base
2. Performing semantic search using embeddings
3. Retrieving relevant document chunks with metadata
4. Supporting various data sources (S3, web crawling, etc.)

This retriever is particularly useful when:
- Building RAG applications with AWS Bedrock
- Need managed vector storage and retrieval
- Working with diverse data sources
- Want serverless RAG infrastructure
- Building enterprise AI applications on AWS

The implementation integrates with LangChain's AmazonKnowledgeBasesRetriever while
providing a consistent Haive configuration interface with secure AWS credential management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.AMAZON_KNOWLEDGE_BASES)
class AmazonKnowledgeBasesRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    """Configuration for Amazon Knowledge Bases retriever in the Haive framework.

    This retriever uses AWS Bedrock Knowledge Bases to provide managed
    RAG capabilities with semantic search and various data source integrations.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always AMAZON_KNOWLEDGE_BASES).
        knowledge_base_id (str): Amazon Knowledge Base ID.
        region_name (str): AWS region name.
        api_key (Optional[SecretStr]): AWS access key (auto-resolved from AWS_ACCESS_KEY_ID).
        secret_key (Optional[SecretStr]): AWS secret key (auto-resolved from AWS_SECRET_ACCESS_KEY).
        number_of_results (int): Number of results to retrieve.
        search_type (str): Type of search to perform.

    Examples:
        >>> from haive.core.engine.retriever import AmazonKnowledgeBasesRetrieverConfig
        >>>
        >>> # Create the Knowledge Bases retriever config
        >>> config = AmazonKnowledgeBasesRetrieverConfig(
        ...     name="kb_retriever",
        ...     knowledge_base_id="ABCDEFGHIJ",
        ...     region_name="us-east-1",
        ...     number_of_results=10,
        ...     search_type="SEMANTIC"
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("machine learning best practices")
        >>>
        >>> # Example with hybrid search
        >>> hybrid_config = AmazonKnowledgeBasesRetrieverConfig(
        ...     name="hybrid_kb_retriever",
        ...     knowledge_base_id="ABCDEFGHIJ",
        ...     region_name="us-east-1",
        ...     search_type="HYBRID"
        ... )
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.AMAZON_KNOWLEDGE_BASES,
        description="The type of retriever",
    )

    # AWS Knowledge Base configuration
    knowledge_base_id: str = Field(..., description="Amazon Knowledge Base ID")

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
    number_of_results: int = Field(
        default=10, ge=1, le=100, description="Number of results to retrieve"
    )

    search_type: str = Field(
        default="SEMANTIC", description="Search type: 'SEMANTIC', 'HYBRID'"
    )

    # Advanced filtering
    filter: dict[str, Any] | None = Field(
        default=None, description="Metadata filters for search results"
    )

    # Knowledge Base specific parameters
    retrieval_configuration: dict[str, Any] | None = Field(
        default=None,
        description="Advanced retrieval configuration for the knowledge base",
    )

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for Amazon Knowledge Bases retriever."""
        return {
            "query": (str, Field(description="Search query for Knowledge Bases")),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for Amazon Knowledge Bases retriever."""
        return {
            "documents": (
                list[Document],
                Field(
                    default_factory=list, description="Documents from Knowledge Bases"
                ),
            ),
        }

    def instantiate(self):
        """Create an Amazon Knowledge Bases retriever from this configuration.

        Returns:
            AmazonKnowledgeBasesRetriever: Instantiated retriever ready for RAG.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If AWS credentials or configuration is invalid.
        """
        try:
            import boto3
            from langchain_aws.retrievers import AmazonKnowledgeBasesRetriever
        except ImportError:
            raise ImportError(
                "AmazonKnowledgeBasesRetriever requires langchain-aws and boto3 packages. "
                "Install with: pip install langchain-aws boto3"
            )

        # Get AWS credentials using SecureConfigMixin approach
        access_key = self.get_api_key()
        secret_key = self.secret_key.get_secret_value() if self.secret_key else None

        # Configure AWS session
        if access_key and secret_key:
            session = boto3.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=self.region_name,
            )
            bedrock_client = session.client("bedrock-agent-runtime")
        else:
            # Use default credentials (IAM role, environment variables, etc.)
            bedrock_client = boto3.client(
                "bedrock-agent-runtime", region_name=self.region_name
            )

        # Prepare configuration
        config = {
            "knowledge_base_id": self.knowledge_base_id,
            "client": bedrock_client,
            "retrieval_config": {
                "vectorSearchConfiguration": {"numberOfResults": self.number_of_results}
            },
        }

        # Add search type configuration
        if self.search_type == "HYBRID":
            config["retrieval_config"]["vectorSearchConfiguration"][
                "overrideSearchType"
            ] = "HYBRID"
        else:
            config["retrieval_config"]["vectorSearchConfiguration"][
                "overrideSearchType"
            ] = "SEMANTIC"

        # Add filters if specified
        if self.filter:
            config["retrieval_config"]["vectorSearchConfiguration"][
                "filter"
            ] = self.filter

        # Override with custom retrieval configuration if provided
        if self.retrieval_configuration:
            config["retrieval_config"].update(self.retrieval_configuration)

        return AmazonKnowledgeBasesRetriever(**config)
