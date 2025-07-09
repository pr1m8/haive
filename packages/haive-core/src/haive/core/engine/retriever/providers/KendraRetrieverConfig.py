"""
Amazon Kendra Retriever implementation for the Haive framework.

This module provides a configuration class for the Amazon Kendra retriever,
which uses AWS Kendra's intelligent enterprise search service. Kendra provides
ML-powered search capabilities with natural language understanding and
enterprise document processing.

The KendraRetriever works by:
1. Connecting to an Amazon Kendra index
2. Executing natural language queries
3. Using ML to understand intent and context
4. Returning ranked results with confidence scores

This retriever is particularly useful when:
- Building enterprise search applications
- Need ML-powered query understanding
- Working with diverse document types (PDFs, Word, etc.)
- Want confidence scoring and result ranking
- Building knowledge management systems

The implementation integrates with LangChain's AmazonKendraRetriever while
providing a consistent Haive configuration interface with secure AWS credential management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.KENDRA)
class KendraRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    """
    Configuration for Amazon Kendra retriever in the Haive framework.

    This retriever uses AWS Kendra's intelligent search service to provide
    ML-powered enterprise search with natural language understanding.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always KENDRA).
        index_id (str): Amazon Kendra index ID.
        region_name (str): AWS region name.
        api_key (Optional[SecretStr]): AWS access key (auto-resolved from AWS_ACCESS_KEY_ID).
        secret_key (Optional[SecretStr]): AWS secret key (auto-resolved from AWS_SECRET_ACCESS_KEY).
        top_k (int): Number of documents to retrieve.
        attribute_filter (Optional[Dict]): Filters for document attributes.

    Examples:
        >>> from haive.core.engine.retriever import KendraRetrieverConfig
        >>>
        >>> # Create the Kendra retriever config
        >>> config = KendraRetrieverConfig(
        ...     name="kendra_retriever",
        ...     index_id="12345678-1234-1234-1234-123456789012",
        ...     region_name="us-east-1",
        ...     top_k=10
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("company policy on remote work")
        >>>
        >>> # Example with attribute filtering
        >>> filtered_config = KendraRetrieverConfig(
        ...     name="filtered_kendra_retriever",
        ...     index_id="12345678-1234-1234-1234-123456789012",
        ...     region_name="us-east-1",
        ...     attribute_filter={
        ...         "AndAllFilters": [
        ...             {"EqualsTo": {"Key": "Department", "Value": {"StringValue": "HR"}}}
        ...         ]
        ...     }
        ... )
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.KENDRA, description="The type of retriever"
    )

    # AWS configuration
    index_id: str = Field(..., description="Amazon Kendra index ID")

    region_name: str = Field(default="us-east-1", description="AWS region name")

    # API configuration with SecureConfigMixin
    api_key: Optional[SecretStr] = Field(
        default=None,
        description="AWS access key ID (auto-resolved from AWS_ACCESS_KEY_ID)",
    )

    secret_key: Optional[SecretStr] = Field(
        default=None,
        description="AWS secret access key (auto-resolved from AWS_SECRET_ACCESS_KEY)",
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="aws", description="Provider name for credential resolution"
    )

    # Search parameters
    top_k: int = Field(
        default=10, ge=1, le=100, description="Number of documents to retrieve"
    )

    attribute_filter: Optional[Dict[str, Any]] = Field(
        default=None, description="Kendra attribute filters for document filtering"
    )

    # Advanced Kendra parameters
    page_size: int = Field(
        default=10, ge=1, le=100, description="Number of results per page"
    )

    user_context: Optional[Dict[str, Any]] = Field(
        default=None, description="User context for personalized results"
    )

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Kendra retriever."""
        return {
            "query": (str, Field(description="Natural language query for Kendra")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Kendra retriever."""
        return {
            "documents": (
                List[Document],
                Field(
                    default_factory=list, description="Enterprise documents from Kendra"
                ),
            ),
        }

    def instantiate(self):
        """
        Create an Amazon Kendra retriever from this configuration.

        Returns:
            AmazonKendraRetriever: Instantiated retriever ready for enterprise search.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If AWS credentials or configuration is invalid.
        """
        try:
            import boto3
            from langchain_aws.retrievers import AmazonKendraRetriever
        except ImportError:
            raise ImportError(
                "KendraRetriever requires langchain-aws and boto3 packages. "
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
            kendra_client = session.client("kendra")
        else:
            # Use default credentials (IAM role, environment variables, etc.)
            kendra_client = boto3.client("kendra", region_name=self.region_name)

        # Prepare configuration
        config = {
            "index_id": self.index_id,
            "client": kendra_client,
            "top_k": self.top_k,
        }

        # Add optional parameters
        if self.attribute_filter:
            config["attribute_filter"] = self.attribute_filter

        if self.user_context:
            config["user_context"] = self.user_context

        return AmazonKendraRetriever(**config)
