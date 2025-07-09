"""
Retriever provider implementations for the Haive framework.

This package contains implementations of various retriever providers that extend
the core retriever functionality. These implementations are automatically registered
with the BaseRetrieverConfig registry system through the @BaseRetrieverConfig.register
decorator, making them available for use through the common retriever interface.

Available retriever types include:
- VectorStoreRetriever: Basic retriever using vector similarity search
- MultiQueryRetriever: Generates multiple query variations using an LLM
- TimeWeightedRetriever: Considers document recency in retrieval
- EnsembleRetriever: Combines results from multiple retrievers
- Various sparse retrievers: BM25, TFIDF, KNN, SVM

To create a new retriever provider:
1. Create a new file in this directory
2. Implement a class that extends BaseRetrieverConfig and uses the @BaseRetrieverConfig.register decorator
3. Implement the instantiate() method to create the appropriate retriever

The retriever system uses dynamic loading, so new providers are automatically discovered
without needing to manually update import statements or registries.

Examples:
    ```python
    # In my_custom_retriever.py
    from haive.core.engine.retriever.retriever import BaseRetrieverConfig
    from haive.core.engine.retriever.types import RetrieverType

    @BaseRetrieverConfig.register(RetrieverType.MY_CUSTOM)
    class MyCustomRetrieverConfig(BaseRetrieverConfig):
        # Configuration fields...

        def instantiate(self):
            # Create and return a retriever instance
            return MyCustomRetriever(...)
    ```
"""

# The package relies on dynamic importing, so explicit imports are not needed here
