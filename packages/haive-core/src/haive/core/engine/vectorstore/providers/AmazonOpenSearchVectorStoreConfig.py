"""
Amazon OpenSearch Vector Store implementation for the Haive framework.

This module provides a configuration class for the Amazon OpenSearch Service vector store,
which is AWS's managed version of OpenSearch with enhanced features.

Amazon OpenSearch Service provides:
1. Fully managed OpenSearch clusters on AWS
2. AOSS (Amazon OpenSearch Service Serverless) support
3. AWS IAM authentication and security
4. Cross-region replication
5. Integration with other AWS services
6. Automatic scaling and high availability

This vector store is particularly useful when:
- You're building on AWS infrastructure
- Need a fully managed OpenSearch solution
- Require AWS IAM-based authentication
- Want serverless vector search with AOSS
- Need enterprise-grade security and compliance

The implementation extends the base OpenSearch configuration with AWS-specific features.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, validator

from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.AMAZON_OPENSEARCH)
class AmazonOpenSearchVectorStoreConfig(BaseVectorStoreConfig):
    """
    Configuration for Amazon OpenSearch Service vector store in the Haive framework.

    This vector store uses AWS's managed OpenSearch Service for scalable vector search
    with additional AWS-specific features and authentication options.

    Attributes:
        opensearch_url (str): Amazon OpenSearch Service endpoint URL.
        index_name (str): Name of the OpenSearch index.
        aws_region (str): AWS region where the OpenSearch domain is located.
        use_aws_auth (bool): Whether to use AWS IAM authentication.
        aws_access_key_id (Optional[str]): AWS access key ID (if not using default credentials).
        aws_secret_access_key (Optional[str]): AWS secret access key (if not using default credentials).
        is_aoss (bool): Whether this is an AOSS (serverless) deployment.

    Examples:
        >>> from haive.core.engine.vectorstore import AmazonOpenSearchVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create Amazon OpenSearch config (with IAM auth)
        >>> config = AmazonOpenSearchVectorStoreConfig(
        ...     name="aws_opensearch_vectors",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     opensearch_url="https://search-mydomain.us-east-1.es.amazonaws.com",
        ...     index_name="document_vectors",
        ...     aws_region="us-east-1",
        ...     use_aws_auth=True
        ... )
        >>>
        >>> # Create AOSS (serverless) config
        >>> config = AmazonOpenSearchVectorStoreConfig(
        ...     name="aoss_vectors",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     opensearch_url="https://abcdef.us-east-1.aoss.amazonaws.com",
        ...     index_name="vectors",
        ...     aws_region="us-east-1",
        ...     use_aws_auth=True,
        ...     is_aoss=True,
        ...     engine="faiss"  # AOSS only supports faiss and nmslib
        ... )
        >>>
        >>> # Instantiate and use
        >>> vectorstore = config.instantiate()
        >>> docs = [Document(page_content="Amazon OpenSearch Service provides managed vector search")]
        >>> vectorstore.add_documents(docs)
    """

    # Amazon OpenSearch connection configuration
    opensearch_url: str = Field(
        ..., description="Amazon OpenSearch Service endpoint URL (required)"
    )

    index_name: str = Field(..., description="Name of the OpenSearch index (required)")

    # AWS configuration
    aws_region: str = Field(
        default="us-east-1",
        description="AWS region where the OpenSearch domain is located",
    )

    use_aws_auth: bool = Field(
        default=True, description="Whether to use AWS IAM authentication"
    )

    aws_access_key_id: Optional[str] = Field(
        default=None,
        description="AWS access key ID (uses default credentials if not provided)",
    )

    aws_secret_access_key: Optional[str] = Field(
        default=None,
        description="AWS secret access key (uses default credentials if not provided)",
    )

    aws_session_token: Optional[str] = Field(
        default=None, description="AWS session token for temporary credentials"
    )

    # AOSS configuration
    is_aoss: bool = Field(
        default=False, description="Whether this is an AOSS (serverless) deployment"
    )

    # Engine configuration (inherited from OpenSearch but with AOSS constraints)
    engine: str = Field(
        default="nmslib",
        description="Vector engine: 'nmslib' or 'faiss' (lucene not supported on AOSS)",
    )

    space_type: str = Field(
        default="l2",
        description="Distance metric: 'l2', 'cosine', 'l1', 'linf', 'innerproduct'",
    )

    # Index configuration
    bulk_size: int = Field(
        default=500, ge=1, le=10000, description="Bulk operation size for indexing"
    )

    # Search configuration
    ef_search: int = Field(
        default=512,
        ge=1,
        le=10000,
        description="Size of dynamic list for k-NN searches",
    )

    ef_construction: int = Field(
        default=512,
        ge=1,
        le=10000,
        description="Size of dynamic list for k-NN graph creation",
    )

    m: int = Field(
        default=16,
        ge=2,
        le=100,
        description="Number of bidirectional links for each element",
    )

    # Field mapping
    vector_field: str = Field(
        default="vector_field", description="Document field name for storing embeddings"
    )

    text_field: str = Field(
        default="text", description="Document field name for storing text content"
    )

    metadata_field: str = Field(
        default="metadata", description="Document field name for storing metadata"
    )

    # Connection settings
    timeout: int = Field(
        default=30, ge=1, le=300, description="Connection timeout in seconds"
    )

    max_retries: int = Field(
        default=3, ge=0, le=10, description="Maximum number of connection retries"
    )

    # Performance settings
    max_chunk_bytes: int = Field(
        default=1024 * 1024,  # 1MB
        ge=1024,
        le=100 * 1024 * 1024,  # 100MB
        description="Maximum chunk size for bulk operations in bytes",
    )

    @validator("opensearch_url")
    def validate_opensearch_url(cls, v):
        """Validate Amazon OpenSearch URL format."""
        if not v.startswith("https://"):
            raise ValueError("Amazon OpenSearch URL must use HTTPS")
        if not any(
            domain in v for domain in [".es.amazonaws.com", ".aoss.amazonaws.com"]
        ):
            raise ValueError("URL must be an Amazon OpenSearch Service endpoint")
        return v

    @validator("engine")
    def validate_engine(cls, v, values):
        """Validate vector engine is supported, considering AOSS limitations."""
        is_aoss = values.get("is_aoss", False)
        if is_aoss:
            valid_engines = ["nmslib", "faiss"]
            if v not in valid_engines:
                raise ValueError(f"AOSS only supports {valid_engines}, got {v}")
        else:
            valid_engines = ["nmslib", "faiss", "lucene"]
            if v not in valid_engines:
                raise ValueError(f"engine must be one of {valid_engines}, got {v}")
        return v

    @validator("aws_region")
    def validate_aws_region(cls, v):
        """Validate AWS region format."""
        import re

        if not re.match(r"^[a-z]{2}-[a-z]+-\d+$", v):
            raise ValueError(f"Invalid AWS region format: {v}")
        return v

    @validator("index_name")
    def validate_index_name(cls, v):
        """Validate index name format."""
        if not v or len(v.strip()) == 0:
            raise ValueError("index_name cannot be empty")
        import re

        if not re.match(r"^[a-z0-9_.-]+$", v.lower()):
            raise ValueError(
                "index_name must contain only lowercase letters, numbers, dots, hyphens, and underscores"
            )
        return v

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Amazon OpenSearch vector store."""
        return {
            "documents": (
                List[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Amazon OpenSearch vector store."""
        return {
            "ids": (
                List[str],
                Field(description="IDs of the added documents in Amazon OpenSearch"),
            ),
        }

    def instantiate(self):
        """
        Create an Amazon OpenSearch Service vector store from this configuration.

        Returns:
            OpenSearchVectorSearch: Instantiated Amazon OpenSearch vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_community.vectorstores import OpenSearchVectorSearch
        except ImportError as e:
            raise ImportError(
                "Amazon OpenSearch requires opensearch-py package. "
                "Install with: pip install opensearch-py"
            ) from e

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Prepare authentication
        http_auth = None
        if self.use_aws_auth:
            try:
                import boto3
                from opensearchpy import RequestsAWSV4SignerAuth
            except ImportError as e:
                raise ImportError(
                    "AWS authentication requires boto3. "
                    "Install with: pip install boto3"
                ) from e

            # Create AWS credentials
            if self.aws_access_key_id and self.aws_secret_access_key:
                # Use provided credentials
                credentials = boto3.Session(
                    aws_access_key_id=self.aws_access_key_id,
                    aws_secret_access_key=self.aws_secret_access_key,
                    aws_session_token=self.aws_session_token,
                    region_name=self.aws_region,
                ).get_credentials()
            else:
                # Use default credentials
                credentials = boto3.Session(
                    region_name=self.aws_region
                ).get_credentials()

            # Determine service name
            service = "aoss" if self.is_aoss else "es"

            # Create AWS V4 signer
            http_auth = RequestsAWSV4SignerAuth(credentials, self.aws_region, service)

        # Prepare OpenSearch client configuration
        client_kwargs = {
            "http_auth": http_auth,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "use_ssl": True,
            "verify_certs": True,
            "ssl_show_warn": False,
        }

        # Prepare OpenSearch vector store configuration
        kwargs = {
            "engine": self.engine,
            "space_type": self.space_type,
            "ef_search": self.ef_search,
            "ef_construction": self.ef_construction,
            "m": self.m,
            "vector_field": self.vector_field,
            "text_field": self.text_field,
            "metadata_field": self.metadata_field,
            "is_appx_search": True,  # Always use approximate search
            "bulk_size": self.bulk_size,
            "max_chunk_bytes": self.max_chunk_bytes,
            **client_kwargs,
        }

        # Create Amazon OpenSearch vector store
        try:
            vectorstore = OpenSearchVectorSearch(
                opensearch_url=self.opensearch_url,
                index_name=self.index_name,
                embedding_function=embedding_function,
                **kwargs,
            )
        except Exception as e:
            raise ValueError(
                f"Failed to create Amazon OpenSearch vector store: {e}"
            ) from e

        return vectorstore
