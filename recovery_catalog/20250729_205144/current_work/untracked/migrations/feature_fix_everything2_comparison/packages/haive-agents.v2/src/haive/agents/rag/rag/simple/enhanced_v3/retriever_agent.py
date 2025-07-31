"""Specialized Retriever Agent for SimpleRAG V3.

This module provides a specialized retriever agent that extends BaseRAGAgent
with enhanced features for use in Enhanced MultiAgent V3 workflows.
"""

import logging
import time
from typing import Any

from langchain_core.documents import Document
from pydantic import Field

from haive.agents.rag.base.agent import BaseRAGAgent

logger = logging.getLogger(__name__)


class RetrieverAgent(BaseRAGAgent):
    """Specialized retriever agent for SimpleRAG V3.

    This agent extends BaseRAGAgent with enhanced features:
    - Performance tracking and timing
    - Debug information collection
    - Enhanced document metadata
    - Quality scoring for retrieved documents
    - Configurable retrieval parameters

    Designed to work as the first agent in Enhanced MultiAgent V3 sequential pattern:
    RetrieverAgent → SimpleAnswerAgent

    Examples:
        Basic usage::

            retriever = RetrieverAgent(
                name="document_retriever",
                engine=vector_store_config,
                top_k=5,
                score_threshold=0.7
            )

            result = await retriever.arun("What is machine learning?")

        With performance tracking::

            retriever = RetrieverAgent(
                name="enhanced_retriever",
                engine=vector_store_config,
                performance_mode=True,
                debug_mode=True
            )
    """

    # Retrieval configuration
    top_k: int = Field(
        default=5, ge=1, le=50, description="Number of documents to retrieve"
    )

    score_threshold: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Minimum similarity score threshold"
    )

    # Enhanced features
    performance_mode: bool = Field(
        default=False, description="Enable performance tracking and metrics"
    )

    debug_mode: bool = Field(
        default=False, description="Enable debug information collection"
    )

    include_metadata: bool = Field(
        default=True, description="Include document metadata in results"
    )

    quality_scoring: bool = Field(
        default=False, description="Calculate quality scores for retrieved documents"
    )

    async def arun(
        self, input_data: str | dict[str, Any], debug: bool = False, **kwargs
    ) -> dict[str, Any]:
        """Enhanced retrieval with performance tracking and debug info.

        Args:
            input_data: Query string or dict with 'query' field
            debug: Enable debug output
            **kwargs: Additional retrieval parameters

        Returns:
            Dict containing:
                - documents: List of retrieved documents
                - metadata: Retrieval metadata (if performance_mode)
                - debug_info: Debug information (if debug_mode)
                - performance_metrics: Timing and quality metrics
        """
        # Extract query
        if isinstance(input_data, str):
            query = input_data
        elif isinstance(input_data, dict) and "query" in input_data:
            query = input_data["query"]
        else:
            raise ValueError("Input must be string or dict with 'query' field")

        if debug or self.debug_mode:
            logger.info(f"🔍 RetrieverAgent '{self.name}' processing query: {query}")

        # Start timing
        start_time = time.time()

        try:
            # Use parent's retrieval functionality
            retrieval_result = await super().arun(input_data, debug=debug, **kwargs)

            # Extract documents from result
            documents = self._extract_documents(retrieval_result)

            # Apply filtering and scoring
            filtered_documents = self._filter_and_score_documents(
                documents, query, debug or self.debug_mode
            )

            # Calculate timing
            retrieval_time = time.time() - start_time

            # Build enhanced result
            result = {
                "documents": filtered_documents,
                "query": query,
                "retrieval_time": retrieval_time,
                "document_count": len(filtered_documents),
            }

            # Add performance metrics if enabled
            if self.performance_mode:
                result["performance_metrics"] = self._calculate_performance_metrics(
                    filtered_documents, retrieval_time, query
                )

            # Add debug information if enabled
            if debug or self.debug_mode:
                result["debug_info"] = self._collect_debug_info(
                    filtered_documents, retrieval_time, query
                )
                logger.info(
                    f"✅ Retrieved {len(filtered_documents)} documents in {retrieval_time:.3f}s"
                )

            # Add metadata if enabled
            if self.include_metadata:
                result["metadata"] = self._build_metadata(
                    filtered_documents, query, retrieval_time
                )

            return result

        except Exception as e:
            logger.error(f"❌ RetrieverAgent error: {e}")
            return {
                "documents": [],
                "query": query,
                "error": str(e),
                "retrieval_time": time.time() - start_time,
                "document_count": 0,
            }

    def _extract_documents(self, retrieval_result: Any) -> list[Document]:
        """Extract documents from various result formats."""
        if isinstance(retrieval_result, list):
            # Direct list of documents
            return [doc for doc in retrieval_result if isinstance(doc, Document)]

        if isinstance(retrieval_result, dict):
            # Result dictionary
            if "documents" in retrieval_result:
                return retrieval_result["documents"]
            if "retrieved_documents" in retrieval_result:
                return retrieval_result["retrieved_documents"]

        if hasattr(retrieval_result, "documents"):
            # Object with documents attribute
            return list(retrieval_result.documents)

        if hasattr(retrieval_result, "retrieved_documents"):
            # Object with retrieved_documents attribute
            return list(retrieval_result.retrieved_documents)

        # Fallback: create document from string
        if isinstance(retrieval_result, str):
            return [
                Document(
                    page_content=retrieval_result,
                    metadata={"source": "retrieval_result", "generated": True},
                )
            ]

        return []

    def _filter_and_score_documents(
        self, documents: list[Document], query: str, debug: bool = False
    ) -> list[Document]:
        """Filter documents by score threshold and apply quality scoring."""
        if not documents:
            return documents

        filtered_docs = []

        for doc in documents[: self.top_k]:  # Limit to top_k
            # Check similarity score if available
            score = doc.metadata.get("score", 1.0)

            if score >= self.score_threshold:
                # Add quality scoring if enabled
                if self.quality_scoring:
                    quality_score = self._calculate_quality_score(doc, query)
                    doc.metadata["quality_score"] = quality_score

                # Add retrieval metadata
                doc.metadata["retrieval_agent"] = self.name
                doc.metadata["retrieval_timestamp"] = time.time()

                filtered_docs.append(doc)

        if debug:
            logger.info(f"📊 Filtered {len(filtered_docs)}/{len(documents)} documents")
            if self.quality_scoring:
                avg_quality = (
                    sum(doc.metadata.get("quality_score", 0.0) for doc in filtered_docs)
                    / len(filtered_docs)
                    if filtered_docs
                    else 0.0
                )
                logger.info(f"📈 Average quality score: {avg_quality:.3f}")

        return filtered_docs

    def _calculate_quality_score(self, document: Document, query: str) -> float:
        """Calculate quality score for a document relative to query."""
        # Simple quality scoring based on:
        # - Document length (not too short, not too long)
        # - Presence of query terms
        # - Metadata richness

        content = document.page_content.lower()
        query_lower = query.lower()

        # Length score (optimal around 200-500 chars)
        length = len(content)
        if length < 50:
            length_score = length / 50.0  # Penalty for very short
        elif length > 1000:
            length_score = max(0.5, 1000 / length)  # Penalty for very long
        else:
            length_score = 1.0

        # Query term presence
        query_terms = set(query_lower.split())
        content_terms = set(content.split())
        term_overlap = len(query_terms.intersection(content_terms))
        term_score = min(1.0, term_overlap / len(query_terms)) if query_terms else 0.5

        # Metadata richness
        metadata_score = min(1.0, len(document.metadata) / 3.0)

        # Combined score
        quality_score = length_score * 0.3 + term_score * 0.5 + metadata_score * 0.2

        return round(quality_score, 3)

    def _calculate_performance_metrics(
        self, documents: list[Document], retrieval_time: float, query: str
    ) -> dict[str, float]:
        """Calculate performance metrics for retrieval operation."""
        metrics = {
            "retrieval_time": retrieval_time,
            "documents_per_second": len(documents) / max(retrieval_time, 0.001),
            "avg_document_length": (
                sum(len(doc.page_content) for doc in documents) / len(documents)
                if documents
                else 0.0
            ),
            "query_length": len(query),
        }

        if self.quality_scoring and documents:
            quality_scores = [
                doc.metadata.get("quality_score", 0.0) for doc in documents
            ]
            metrics.update(
                {
                    "avg_quality_score": sum(quality_scores) / len(quality_scores),
                    "min_quality_score": min(quality_scores),
                    "max_quality_score": max(quality_scores),
                }
            )

        # Add similarity scores if available
        similarity_scores = [doc.metadata.get("score", 0.0) for doc in documents]
        if any(score > 0 for score in similarity_scores):
            metrics.update(
                {
                    "avg_similarity_score": sum(similarity_scores)
                    / len(similarity_scores),
                    "min_similarity_score": min(similarity_scores),
                    "max_similarity_score": max(similarity_scores),
                }
            )

        return metrics

    def _collect_debug_info(
        self, documents: list[Document], retrieval_time: float, query: str
    ) -> dict[str, Any]:
        """Collect debug information for retrieval operation."""
        debug_info = {
            "agent_name": self.name,
            "query": query,
            "query_length": len(query),
            "retrieval_time": retrieval_time,
            "documents_found": len(documents),
            "top_k_limit": self.top_k,
            "score_threshold": self.score_threshold,
            "retrieval_config": {
                "performance_mode": self.performance_mode,
                "quality_scoring": self.quality_scoring,
                "include_metadata": self.include_metadata,
            },
        }

        if documents:
            debug_info["document_info"] = []
            for i, doc in enumerate(documents):
                doc_info = {
                    "index": i,
                    "content_length": len(doc.page_content),
                    "content_preview": (
                        doc.page_content[:100] + "..."
                        if len(doc.page_content) > 100
                        else doc.page_content
                    ),
                    "metadata_keys": list(doc.metadata.keys()),
                    "similarity_score": doc.metadata.get("score"),
                    "quality_score": doc.metadata.get("quality_score"),
                    "source": doc.metadata.get("source", "unknown"),
                }
                debug_info["document_info"].append(doc_info)

        return debug_info

    def _build_metadata(
        self, documents: list[Document], query: str, retrieval_time: float
    ) -> dict[str, Any]:
        """Build metadata for retrieval operation."""
        return {
            "retrieval_agent": self.name,
            "query": query,
            "retrieval_time": retrieval_time,
            "document_count": len(documents),
            "sources": list(
                set(doc.metadata.get("source", "unknown") for doc in documents)
            ),
            "retrieval_config": {
                "top_k": self.top_k,
                "score_threshold": self.score_threshold,
                "performance_mode": self.performance_mode,
                "quality_scoring": self.quality_scoring,
            },
        }

    def get_retrieval_summary(self) -> dict[str, Any]:
        """Get summary of retriever configuration."""
        return {
            "name": self.name,
            "top_k": self.top_k,
            "score_threshold": self.score_threshold,
            "performance_mode": self.performance_mode,
            "debug_mode": self.debug_mode,
            "quality_scoring": self.quality_scoring,
            "include_metadata": self.include_metadata,
            "engine_type": type(self.engine).__name__,
        }


__all__ = ["RetrieverAgent"]
