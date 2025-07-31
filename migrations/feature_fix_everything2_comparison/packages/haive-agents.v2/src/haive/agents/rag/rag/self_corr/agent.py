"""Agent core module.

This module provides agent functionality for the Haive framework.

Classes:
    SelfCorrectiveRAGAgent: SelfCorrectiveRAGAgent implementation.

Functions:
    retriever: Retriever functionality.
"""

import logging
from typing import Any

from haive.core.engine.agent.agent import Agent, register_agent
from haive.core.graph.branches import Branch
from langgraph.graph import END, START
from langgraph.types import Command

from haive.agents.rag.self_corr.config import SelfCorrectiveRAGConfig
from haive.agents.rag.self_corr.state import SelfCorrectiveRAGState

logger = logging.getLogger(__name__)


@register_agent(SelfCorrectiveRAGConfig)
class SelfCorrectiveRAGAgent(Agent[SelfCorrectiveRAGConfig]):
    """RAG agent with self-correction capabilities.

    This agent implements a workflow that:
    1. Retrieves relevant documents for a query
    2. Filters documents based on relevance
    3. Generates an initial answer
    4. Evaluates the answer quality and checks for hallucinations
    5. Corrects the answer if issues are found
    6. Iterates until quality threshold is met or max iterations reached
    """

    def __init__(self, config: SelfCorrectiveRAGConfig):
        """Initialize the agent with self-correction capabilities."""
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

            # Initialize evaluation and correction components
            self.answer_evaluator = None
            if config.answer_evaluator_config:
                self.answer_evaluator = config.answer_evaluator_config.create_runnable()

            self.answer_corrector = None
            if config.answer_corrector_config:
                self.answer_corrector = config.answer_corrector_config.create_runnable()

            logger.info("Self-corrective RAG agent components initialized successfully")
        except Exception as e:
            logger.exception(f"Error initializing Self-corrective RAG components: {e}")
            raise

    @property
    def retriever(self) -> Any:
        """Lazy-loaded retriever property."""
        return self._retriever

    def retrieve_documents(self, state: SelfCorrectiveRAGState) -> Command:
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

    def filter_documents(self, state: SelfCorrectiveRAGState) -> Command:
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

    def generate_answer(self, state: SelfCorrectiveRAGState) -> Command:
        """Generate an initial answer based on filtered documents.

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
                        "answer": "I couldn't find any relevant documents to answer your query.",
                        "correction_iterations": 0,
                    }
                )

            if not self.answer_generator:
                return Command(
                    update={
                        "answer": f"Found {len(documents)} relevant documents, but no answer generator is configured.",
                        "correction_iterations": 0,
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

            return Command(
                update={
                    "answer": answer,
                    "correction_iterations": 0,  # Initialize correction counter
                }
            )

        except Exception as e:
            logger.exception(f"Error generating answer: {e!s}")
            return Command(
                update={
                    "error": f"Error generating answer: {e!s}",
                    "answer": "I encountered an error while trying to generate an answer.",
                    "correction_iterations": 0,
                }
            )

    def evaluate_answer(self, state: SelfCorrectiveRAGState) -> Command:
        """Evaluate the quality of the generated answer and check for hallucinations.

        Args:
            state: Current state with query, answer, and documents

        Returns:
            Command with evaluation results
        """
        query = state.query
        answer = state.answer
        documents = state.filtered_documents

        logger.info(
            f"Evaluating answer quality (iteration {state.correction_iterations})"
        )

        try:
            # If no evaluator is configured, assume the answer is good
            if not self.answer_evaluator:
                return Command(
                    update={
                        "answer_score": 1.0,
                        "hallucination_assessment": {},
                        "final_answer": True,
                    }
                )

            # Prepare context from documents
            context = "\n\n".join([doc.page_content for doc in documents])

            # Invoke the evaluator
            evaluation = self.answer_evaluator.invoke(
                {"query": query, "answer": answer, "context": context}
            )

            # Process the evaluation result
            if isinstance(evaluation, dict):
                score = evaluation.get("score", 0.0)
                assessment = evaluation.get("assessment", {})
            else:
                # Try to parse a numeric score from the text
                try:
                    score = float(evaluation)
                    assessment = {}
                except:
                    logger.warning(f"Could not parse evaluation result: {evaluation}")
                    score = 0.5
                    assessment = {}

            # Determine if this should be the final answer
            final_answer = (
                score >= self.config.minimum_answer_score
                or state.correction_iterations >= self.config.max_correction_iterations
            )

            logger.info(f"Evaluation score: {score}, final_answer: {final_answer}")

            return Command(
                update={
                    "answer_score": score,
                    "hallucination_assessment": assessment,
                    "final_answer": final_answer,
                }
            )

        except Exception as e:
            logger.exception(f"Error evaluating answer: {e!s}")
            return Command(
                update={
                    "error": f"Error evaluating answer: {e!s}",
                    "answer_score": 0.5,  # Default to middle score
                    "hallucination_assessment": {"error": str(e)},
                    "final_answer": True,  # Force final to avoid infinite loops on errors
                }
            )

    def correct_answer(self, state: SelfCorrectiveRAGState) -> Command:
        """Correct the answer based on evaluation feedback.

        Args:
            state: Current state with query, answer, evaluation, and documents

        Returns:
            Command with corrected answer
        """
        query = state.query
        answer = state.answer
        assessment = state.hallucination_assessment
        documents = state.filtered_documents
        iterations = state.correction_iterations

        logger.info(f"Correcting answer (iteration {iterations})")

        try:
            # If no corrector is configured, just increment the counter
            if not self.answer_corrector:
                return Command(
                    update={
                        "answer": answer,  # Keep the same answer
                        "correction_iterations": iterations + 1,
                    }
                )

            # Prepare context from documents
            context = "\n\n".join([doc.page_content for doc in documents])

            # Invoke the corrector
            corrected_answer = self.answer_corrector.invoke(
                {
                    "query": query,
                    "current_answer": answer,
                    "assessment": assessment,
                    "context": context,
                }
            )

            # Extract string answer if needed
            if hasattr(corrected_answer, "content"):
                corrected_answer = corrected_answer.content
            elif isinstance(corrected_answer, dict) and "answer" in corrected_answer:
                corrected_answer = corrected_answer["answer"]

            logger.info("Answer corrected successfully")

            return Command(
                update={
                    "answer": corrected_answer,
                    "correction_iterations": iterations + 1,
                }
            )

        except Exception as e:
            logger.exception(f"Error correcting answer: {e!s}")
            return Command(
                update={
                    "error": f"Error correcting answer: {e!s}",
                    "answer": answer,  # Keep the original answer
                    "correction_iterations": iterations + 1,
                }
            )

    def finalize_answer(self, state: SelfCorrectiveRAGState) -> Command:
        """Prepare the final answer, possibly adding citations or formatting.

        Args:
            state: Current state with final answer

        Returns:
            Command with finalized answer
        """
        answer = state.answer
        score = state.answer_score if hasattr(state, "answer_score") else None
        iterations = state.correction_iterations

        logger.info(f"Finalizing answer after {iterations} iterations")

        try:
            # Add confidence information if available
            final_answer = answer

            if score is not None:
                confidence_level = (
                    "high" if score > 0.8 else "medium" if score > 0.5 else "low"
                )
                logger.info(f"Answer confidence level: {confidence_level} ({score})")

                # Optionally add confidence information to the answer

            return Command(update={"answer": final_answer, "final_confidence": score})

        except Exception as e:
            logger.exception(f"Error finalizing answer: {e!s}")
            return Command(
                update={
                    "error": f"Error finalizing answer: {e!s}",
                    "answer": answer,  # Return the unmodified answer
                }
            )

    def correction_router(self, state: SelfCorrectiveRAGState) -> str:
        """Route based on evaluation results."""
        if state.final_answer:
            return "finalize_answer"
        return "correct_answer"

    def setup_workflow(self) -> None:
        """Set up the self-corrective RAG workflow.

        Workflow:
        START → retrieve_documents → filter_documents → generate_answer → evaluate_answer
             → [correct_answer → evaluate_answer] (loop) → finalize_answer → END
        """
        # Add nodes for the workflow
        self.graph.add_node("retrieve_documents", self.retrieve_documents)
        self.graph.add_node("filter_documents", self.filter_documents)
        self.graph.add_node("generate_answer", self.generate_answer)
        self.graph.add_node("evaluate_answer", self.evaluate_answer)
        self.graph.add_node("correct_answer", self.correct_answer)
        self.graph.add_node("finalize_answer", self.finalize_answer)

        # Connect nodes in the workflow
        self.graph.add_edge(START, "retrieve_documents")
        self.graph.add_edge("retrieve_documents", "filter_documents")
        self.graph.add_edge("filter_documents", "generate_answer")
        self.graph.add_edge("generate_answer", "evaluate_answef")

        # Add conditional branch based on evaluation
        correction_branch = Branch.from_dict(
            {"finalize_answer": "finalize_answer", "default": "correct_answer"}
        )
        self.graph.add_conditional_edges(
            "evaluate_answer", correction_branch, self.correction_router
        )

        # Connect the correction loop back to evaluation
        self.graph.add_edge("correct_answer", "evaluate_answer")

        # Connect to the end
        self.graph.add_edge("finalize_answer", END)

        logger.info("Self-corrective RAG workflow setup complete")
