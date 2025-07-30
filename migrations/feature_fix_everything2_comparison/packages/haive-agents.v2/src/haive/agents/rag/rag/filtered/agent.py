"""Agent core module.

This module provides agent functionality for the Haive framework.

Classes:
    FilteredRAGAgent: FilteredRAGAgent implementation.

Functions:
    retriever: Retriever functionality.
"""

import logging
from typing import Any

from haive.core.engine.agent.agent import Agent, register_agent
from langgraph.graph import END, START
from langgraph.types import Command

from haive.agents.rag.filtered.config import FilteredRAGConfig
from haive.agents.rag.filtered.state import FilteredRAGState

logger = logging.getLogger(__name__)


@register_agent(FilteredRAGConfig)
class FilteredRAGAgent(Agent[FilteredRAGConfig]):
    """RAG agent with document filtering capabilities.

    This agent implements a workflow that:
    1. Retrieves relevant documents for a query
    2. Filters documents based on relevance to the query
    3. Generates an answer based on the filtered documents
    """

    def __init__(self, config: FilteredRAGConfig):
        """Initialize the agent with document filtering capabilities."""
        self._initialize_components(config)
        super().__init__(config)

    def _initialize_components(self, config):
        """Initialize all components for the agent."""
        try:
            # Initialize retriever
            if hasattr(config.retriever_config, "create_runnable"):
                self._retriever = config.retriever_config.create_runnable()
            else:
                self._retriever = config.retriever_config

            # Initialize document filter
            self.document_filter = None
            if config.document_filter_config:
                self.document_filter = config.document_filter_config.create_runnable()

            # Initialize answer generator
            self.answer_generator = None
            if config.llm_config:
                self.answer_generator = config.llm_config.create_runnable()
            elif config.answer_generator_config:
                self.answer_generator = config.answer_generator_config.create_runnable()

            logger.info("Filtered RAG agent components initialized successfully")
        except Exception as e:
            logger.exception(f"Error initializing Filtered RAG components: {e}")
            raise

    @property
    def retriever(self) -> Any:
        """Lazy-loaded retriever property."""
        return self._retriever

    def retrieve_documents(self, state: FilteredRAGState) -> Command:
        """Retrieve documents based on the query.

        Args:
            state: Current state with query

        Returns:
            Command with retrieved documents
        """
        logger.info(f"Retrieving documents for query: {state.query}")

        try:
            # Use retriever to get documents
            documents = self.retriever.invoke(state.query)

            logger.info(f"Retrieved {len(documents)} documents")

            return Command(update={"retrieved_documents": documents})

        except Exception as e:
            logger.exception(f"Error retrieving documents: {e!s}")
            return Command(
                update={
                    "error": f"Error retrieving documents: {e!s}",
                    "retrieved_documents": [],
                }
            )

    def filter_documents(self, state: FilteredRAGState) -> Command:
        """Filter documents based on relevance to the query.

        Args:
            state: Current state with query and retrieved documents

        Returns:
            Command with filtered documents
        """
        query = state.query
        documents = state.retrieved_documents

        logger.info(f"Filtering {len(documents)} documents")

        try:
            if not documents:
                return Command(update={"filtered_documents": []})

            if not self.document_filter:
                # No filter configured, use all documents
                return Command(update={"filtered_documents": documents})

            relevance_scores = {}
            filtered_docs = []

            for doc in documents:
                doc_id = doc.metadata.get("id", str(hash(doc.page_content)))

                try:
                    score = self.document_filter.invoke(
                        {"query": query, "document": doc.page_content}
                    )

                    # Try to convert the score to a float
                    if isinstance(score, dict) and "score" in score:
                        score_value = float(score["score"])
                    else:
                        score_value = float(score)

                    relevance_scores[doc_id] = score_value

                    if score_value >= self.config.relevance_threshold:
                        filtered_docs.append(doc)
                except Exception as e:
                    logger.warning(f"Error filtering document {doc_id}: {e}")
                    # If conversion fails, include the document by default
                    filtered_docs.append(doc)

            logger.info(f"Filtered to {len(filtered_docs)} relevant documents")

            return Command(
                update={
                    "filtered_documents": filtered_docs,
                    "relevance_scores": relevance_scores,
                }
            )

        except Exception as e:
            logger.exception(f"Error in document filtering: {e!s}")
            return Command(
                update={
                    "error": f"Error filtering documents: {e!s}",
                    "filtered_documents": documents,  # Fall back to all documents
                }
            )

    def generate_answer(self, state: FilteredRAGState) -> Command:
        """Generate an answer based on filtered documents.

        Args:
            state: Current state with query and filtered documents

        Returns:
            Command with generated answer
        """
        query = state.query
        documents = state.filtered_documents

        logger.info(f"Generating answer based on {len(documents)} documents")

        try:
            if not documents:
                return Command(
                    update={
                        "answer": "I couldn't find any relevant documents to answer your query."
                    }
                )

            if not self.answer_generator:
                return Command(
                    update={
                        "answer": f"Found {len(documents)} relevant documents, but no answer generator is configured."
                    }
                )

            # Prepare context from documents
            context = "\n\n".join([doc.page_content for doc in documents])

            # Generate answer
            answer = self.answer_generator.invoke({"query": query, "context": context})

            # Extract string answer if needed
            if hasattr(answer, "content"):
                answer = answer.content
            elif isinstance(answer, dict) and "answer" in answer:
                answer = answer["answer"]

            logger.info("Answer generated successfully")

            return Command(update={"answer": answer})

        except Exception as e:
            logger.exception(f"Error generating answer: {e!s}")
            return Command(
                update={
                    "error": f"Error generating answer: {e!s}",
                    "answer": "I encountered an error while trying to generate an answer.",
                }
            )

    def setup_workflow(self) -> None:
        """Set up the filtered RAG workflow.

        Workflow:
        START → retrieve_documents → filter_documents → generate_answer → END
        """
        # Add nodes for the workflow
        self.graph.add_node("retrieve_documents", self.retrieve_documents)
        self.graph.add_node("filter_documents", self.filter_documents)
        self.graph.add_node("generate_answer", self.generate_answer)

        # Connect nodes in the workflow
        self.graph.add_edge(START, "retrieve_documents")
        self.graph.add_edge("retrieve_documents", "filter_documents")
        self.graph.add_edge("filter_documents", "generate_answer")
        self.graph.add_edge("generate_answer", END)

        logger.info("Filtered RAG workflow setup complete")
