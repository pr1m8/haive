"""Agent core module.

This module provides agent functionality for the Haive framework.

Classes:
    TypedRAGAgent: TypedRAGAgent implementation.

Functions:
    classify_query: Classify Query functionality.
"""

import logging

# Set up logging
from typing import Any

from haive.core.engine.agent.agent import register_agent
from haive.core.graph.GraphBuilder import DynamicGraph
from langgraph.graph import END, START

from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.rag.typed.config import TypedRAGConfig
from haive.agents.rag.typed.query_types import QueryCategory

logger = logging.getLogger(__name__)


@register_agent(TypedRAGConfig)
class TypedRAGAgent(BaseRAGAgent):
    """Implements Typed-RAG that classifies queries and routes to specialized handlers."""

    def __init__(self, config: TypedRAGConfig):
        """Initialize with TypedRAGConfig."""
        super().__init__(config)
        self.config = config
        self._init_components()

    def _init_components(self):
        """Initialize all components."""
        # Initialize query classifier
        self.query_classifier = self.config.query_classifier_config.create_runnable()

        # Initialize type handlers
        self.type_handlers = {}
        for handler_type, handler_config in self.config.type_handlers.items():
            self.type_handlers[handler_type] = handler_config.create_runnable()

        # Initialize retrievers for different query types
        self.type_retrievers = {}
        for query_type, retriever_config in self.config.retriever_mapping.items():
            # Check if it's a VectorStoreConfig or RetrieverConfig
            if hasattr(retriever_config, "create_retriever"):
                self.type_retrievers[query_type] = retriever_config.create_retriever()
            else:
                # Assuming it's already a retriever instance
                self.type_retrievers[query_type] = retriever_config

        # Default retriever
        if hasattr(self.config.retriever_config, "create_retriever"):
            self.retriever = self.config.retriever_config.create_retriever()
        else:
            self.retriever = self.config.retriever_config

    def classify_query(self, state: dict[str, Any]):
        """Classify the query into a category."""
        query = state["query"]

        try:
            classification = self.query_classifier.invoke({"query": query})

            if isinstance(classification, str):
                # Try to extract category and metadata
                if classification.lower() in [c.lower() for c in QueryCategory]:
                    return {
                        "query_category": classification.lower(),
                        "query_metadata": {},
                    }

                # Try to parse as JSON
                try:
                    import json

                    parsed = json.loads(classification)
                    if isinstance(parsed, dict):
                        category = parsed.get("category", "factoid").lower()
                        metadata = {k: v for k, v in parsed.items() if k != "category"}
                        return {"query_category": category, "query_metadata": metadata}
                except:
                    pass

                # Default to factoid
                return {"query_category": "factoid", "query_metadata": {}}

            if isinstance(classification, dict):
                category = classification.get("category", "factoid").lower()
                metadata = {k: v for k, v in classification.items() if k != "category"}
                return {"query_category": category, "query_metadata": metadata}

            # Default case
            return {"query_category": "factoid", "query_metadata": {}}

        except Exception as e:
            logger.exception(f"Error classifying query: {e}")
            return {"query_category": "factoid", "query_metadata": {}}

    def generate_subqueries(self, state: dict[str, Any]):
        """Generate specialized subqueries based on query category."""
        query = state["query"]
        category = state["query_category"]
        metadata = state["query_metadata"]

        if not self.config.enable_subqueries:
            return {"subqueries": {category: query}}

        # Get handler for this category
        handler = self.type_handlers.get(category)
        if not handler:
            return {"subqueries": {category: query}}

        try:
            subquery_result = handler.invoke(
                {"query": query, "category": category, "metadata": metadata}
            )

            if isinstance(subquery_result, str):
                # Single subquery
                return {"subqueries": {category: subquery_result}}

            if isinstance(subquery_result, list):
                # List of subqueries - create a mapping
                subqueries = {}
                for i, sq in enumerate(subquery_result):
                    subqueries[f"{category}_{i+1}"] = sq
                return {"subqueries": subqueries}

            if isinstance(subquery_result, dict):
                # Dict mapping of subqueries - use directly
                if "subqueries" in subquery_result:
                    return {"subqueries": subquery_result["subqueries"]}
                return {"subqueries": subquery_result}

            # Default case
            return {"subqueries": {category: query}}

        except Exception as e:
            logger.exception(f"Error generating subqueries: {e}")
            return {"subqueries": {category: query}}

    def retrieve_for_subqueries(self, state: dict[str, Any]):
        """Retrieve documents for each subquery."""
        category = state["query_category"]
        subqueries = state["subqueries"]

        subquery_results = {}

        for subquery_key, subquery in subqueries.items():
            # Get the retriever for this category
            retriever = self.type_retrievers.get(category, self.retriever)

            try:
                docs = retriever.invoke(subquery)
                subquery_results[subquery_key] = docs
            except Exception as e:
                logger.exception(f"Error retrieving for subquery {subquery_key}: {e}")
                subquery_results[subquery_key] = []

        # Combine all documents for standard processing
        all_docs = []
        for docs in subquery_results.values():
            all_docs.extend(docs)

        return {"subquery_results": subquery_results, "retrieved_documents": all_docs}

    def filter_documents(self, state: dict[str, Any]):
        """Filter documents for relevance."""
        # This is a placeholder - implement your actual filtering logic
        documents = state.get("retrieved_documents", [])
        # In a real implementation, you would filter based on relevance scores
        # For now, we'll just pass through all documents
        return {"filtered_documents": documents}

    def aggregate_answers(self, state: dict[str, Any]):
        """Aggregate information from different subqueries."""
        query = state["query"]
        category = state["query_category"]
        subqueries = state["subqueries"]
        subquery_results = state["subquery_results"]
        filtered_documents = state["filtered_documents"]

        # Get handler for this category
        handler = self.type_handlers.get(category)
        if not handler:
            # Fall back to standard answer generation
            return self.generate_answer(state)

        try:
            # Prepare subquery results for the handler
            formatted_results = {}
            for key, docs in subquery_results.items():
                subquery = subqueries.get(key, "")
                doc_contents = "\n\n".join([doc.page_content for doc in docs])
                formatted_results[key] = {"query": subquery, "documents": doc_contents}

            aggregation_result = handler.invoke(
                {
                    "main_query": query,
                    "category": category,
                    "subquery_results": formatted_results,
                    "filtered_documents": [
                        doc.page_content for doc in filtered_documents
                    ],
                }
            )

            if isinstance(aggregation_result, str):
                aggregated_answer = aggregation_result
            elif (
                isinstance(aggregation_result, dict) and "answer" in aggregation_result
            ):
                aggregated_answer = aggregation_result["answef"]
            else:
                aggregated_answer = str(aggregation_result)

            return {"aggregated_answer": aggregated_answer, "answer": aggregated_answer}

        except Exception as e:
            logger.exception(f"Error aggregating answers: {e}")
            # Fall back to standard answer generation
            return self.generate_answer(state)

    def generate_answer(self, state: dict[str, Any]):
        """Generate an answer from the documents."""
        query = state["query"]
        documents = state["filtered_documents"]

        if not documents:
            return {
                "answer": "I couldn't find any relevant information to answer your question."
            }

        # Use the answer generation component from src.config
        answer_generator = self.config.answer_generation_config.create_runnable()

        try:
            result = answer_generator.invoke({"query": query, "documents": documents})

            if isinstance(result, str):
                answer = result
            elif isinstance(result, dict) and "answer" in result:
                answer = result["answef"]
            else:
                answer = str(result)

            return {"answer": answer}

        except Exception as e:
            logger.exception(f"Error generating answer: {e}")
            return {
                "answer": "I encountered an error while generating an answer to your question."
            }

    def setup_workflow(self) -> None:
        """Set up the Typed-RAG workflow."""
        gb = DynamicGraph(state_schema=self.state_schema)

        # Add nodes
        gb.add_node("classify_query", self.classify_query)
        gb.add_node("generate_subqueries", self.generate_subqueries)
        gb.add_node("retrieve_for_subqueries", self.retrieve_for_subqueries)
        gb.add_node("filter_documents", self.filter_documents)
        gb.add_node("aggregate_answers", self.aggregate_answers)

        # Connect nodes
        gb.add_edge(START, "classify_query")
        gb.add_edge("classify_query", "generate_subqueries")
        gb.add_edge("generate_subqueries", "retrieve_for_subqueries")
        gb.add_edge("retrieve_for_subqueries", "filter_documents")
        gb.add_edge("filter_documents", "aggregate_answers")
        gb.add_edge("aggregate_answers", END)

        # Build the graph
        self.graph = gb.build()
