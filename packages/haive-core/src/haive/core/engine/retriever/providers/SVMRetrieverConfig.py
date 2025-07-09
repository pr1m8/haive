"""
Support Vector Machine Retriever implementation for the Haive framework.

This module provides a configuration class for the SVM (Support Vector Machine) retriever,
which uses Support Vector Machine algorithm for document retrieval. SVM retriever treats
document retrieval as a binary classification problem where the query represents the
positive class and retrieves documents most similar to this positive class.

The SVMRetriever works by:
1. Training an SVM classifier using the query as positive examples
2. Using the SVM decision function to score documents
3. Ranking documents by their SVM scores
4. Returning the top-k highest scoring documents

This retriever is particularly useful when:
- Working with text classification-style retrieval
- Need margin-based similarity scoring
- Want robust retrieval with outlier resistance
- Building retrieval systems with limited training data
- Combining with other ML-based retrieval approaches

The implementation integrates with LangChain's SVMRetriever while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field

from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.SVM)
class SVMRetrieverConfig(BaseRetrieverConfig):
    """
    Configuration for Support Vector Machine retriever in the Haive framework.

    This retriever uses SVM classification to score and rank documents based on
    their similarity to the query, treating retrieval as a classification problem.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always SVM).
        documents (List[Document]): Documents to index for retrieval.
        k (int): Number of documents to retrieve (default: 4).
        kernel (str): SVM kernel type ("linear", "rbf", "poly", "sigmoid").
        C (float): SVM regularization parameter.
        gamma (str): Kernel coefficient for RBF, poly and sigmoid kernels.

    Examples:
        >>> from haive.core.engine.retriever import SVMRetrieverConfig
        >>> from langchain_core.documents import Document
        >>>
        >>> # Create documents
        >>> docs = [
        ...     Document(page_content="Machine learning optimizes model parameters"),
        ...     Document(page_content="Deep learning networks minimize loss functions"),
        ...     Document(page_content="Natural language processing tokenizes text inputs")
        ... ]
        >>>
        >>> # Create the SVM retriever config
        >>> config = SVMRetrieverConfig(
        ...     name="svm_retriever",
        ...     documents=docs,
        ...     k=2,
        ...     kernel="rbf",
        ...     C=1.0,
        ...     gamma="scale"
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("machine learning optimization methods")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.SVM, description="The type of retriever"
    )

    # Documents to index
    documents: List[Document] = Field(
        default_factory=list, description="Documents to index for SVM retrieval"
    )

    # Retrieval parameters
    k: int = Field(
        default=4, ge=1, le=100, description="Number of documents to retrieve"
    )

    # SVM algorithm parameters
    kernel: str = Field(
        default="rbf", description="SVM kernel type: 'linear', 'rbf', 'poly', 'sigmoid'"
    )

    C: float = Field(
        default=1.0, ge=0.001, le=1000.0, description="SVM regularization parameter"
    )

    gamma: str = Field(
        default="scale",
        description="Kernel coefficient: 'scale', 'auto', or float value",
    )

    # Additional SVM parameters
    degree: int = Field(
        default=3, ge=1, le=10, description="Degree for polynomial kernel"
    )

    coef0: float = Field(
        default=0.0, description="Independent term in kernel function for poly/sigmoid"
    )

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for SVM retriever."""
        return {
            "query": (str, Field(description="Text query for SVM-based ranking")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for SVM retriever."""
        return {
            "documents": (
                List[Document],
                Field(
                    default_factory=list, description="Documents ranked by SVM scores"
                ),
            ),
        }

    def instantiate(self):
        """
        Create an SVM retriever from this configuration.

        Returns:
            SVMRetriever: Instantiated retriever ready for classification-based retrieval.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If documents list is empty.
        """
        try:
            from langchain_community.retrievers import SVMRetriever
        except ImportError:
            raise ImportError(
                "SVMRetriever requires langchain-community and scikit-learn packages. "
                "Install with: pip install langchain-community scikit-learn"
            )

        if not self.documents:
            raise ValueError(
                "SVMRetriever requires a non-empty list of documents. "
                "Provide documents in the configuration."
            )

        # Prepare SVM parameters
        svm_params = {
            "kernel": self.kernel,
            "C": self.C,
            "gamma": self.gamma,
            "degree": self.degree,
            "coef0": self.coef0,
        }

        return SVMRetriever.from_documents(
            documents=self.documents, k=self.k, **svm_params
        )
