"""Multi-Agent RAG System Components.

This module provides specialized RAG agents that can be composed into complex workflows
using the multi-agent framework. Each agent focuses on a specific aspect of the RAG process.
"""

from collections.abc import Callable
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.fixtures.documents import conversation_documents
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from haive.agents.rag.common.answer_generators.prompts import (
    RAG_ANSWER_STANDARD,
    RAG_ANSWER_WITH_CITATIONS,
)
from haive.agents.rag.common.document_graders.binary_grader.prompt import (
    RAG_DOCUMENT_GRADE_BINARY,
)
from haive.agents.rag.common.document_graders.models import DocumentBinaryResponse
from haive.agents.simple.agent import SimpleAgent

from .state import DocumentGradingResult, MultiAgentRAGState, RAGOperationType

# ============================================================================
# PROMPT TEMPLATES
# ============================================================================

RAG_ANSWER_BASE_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are part of a RAG workflow where your job is to answer whether the documents
retrieved answers the original query.
""",
        ),
        (
            "human",
            """
Query: {query}
Retrieved Documents: {retrieved_documents}
""",
        ),
    ]
)

RAG_DOCUMENT_ITERATOR_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a document grading specialist. Your job is to evaluate each document individually
for relevance to the given query. You will receive one document at a time and must
provide a detailed assessment.

For each document, provide:
1. Relevance score (0.0 to 1.0)
2. Binary decision (relevant/not relevant)
3. Detailed justification
4. Key information that supports the query
""",
        ),
        (
            "human",
            """
Query: {query}
Document to evaluate: {document}

Provide your assessment of this document's relevance to the query.
""",
        ),
    ]
)

RAG_RETRIEVAL_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a document retrieval specialist. Your job is to identify and select the most
relevant documents from a collection that can help answer the given query.

Return a list of document indices (0-based) that are most relevant to the query.
""",
        ),
        (
            "human",
            """
Query: {query}
Available Documents: {available_documents}

Select the most relevant documents by returning their indices.
""",
        ),
    ]
)


# ============================================================================
# SPECIALIZED RAG AGENTS
# ============================================================================


class SimpleRAGAgent(SimpleAgent):
    """Simple RAG agent that retrieves documents and provides basic answers.

    This agent provides fundamental RAG functionality using conversation documents
    as the knowledge base. It can be composed with other agents for more complex workflows.
    """

    def __init__(
        self, documents: list[Document] | None = None, max_documents: int = 5, **kwargs
    ):
        # Set up default engine if none provided
        if "engine" not in kwargs:
            kwargs["engine"] = AugLLMConfig(
                prompt_template=RAG_ANSWER_BASE_PROMPT_TEMPLATE,
                name="simple_rag_engine",
            )

        # Set default name
        if "name" not in kwargs:
            kwargs["name"] = "Simple RAG Agent"

        super().__init__(**kwargs)

        # Store documents and config as private attributes (not Pydantic fields)
        self._documents = documents or conversation_documents
        self._max_documents = max_documents

    @property
    def documents(self) -> list[Document]:
        """Get the documents for this RAG agent."""
        return self._documents

    @documents.setter
    def documents(self, value: list[Document]):
        """Set the documents for this RAG agent."""
        self._documents = value

    @property
    def max_documents(self) -> int:
        """Get the maximum number of documents to retrieve."""
        return self._max_documents

    @max_documents.setter
    def max_documents(self, value: int):
        """Set the maximum number of documents to retrieve."""
        self._max_documents = value

    @classmethod
    def from_documents(
        cls,
        documents: list[Document],
        prompt_template: ChatPromptTemplate | None = None,
        **kwargs,
    ) -> "SimpleRAGAgent":
        """Create SimpleRAGAgent from a document collection."""
        engine_config = AugLLMConfig(
            prompt_template=prompt_template or RAG_ANSWER_BASE_PROMPT_TEMPLATE,
            name="simple_rag_engine",
        )

        return cls(engine=engine_config, documents=documents, **kwargs)

    def retrieve_documents(
        self, query: str, top_k: int | None = None
    ) -> list[Document]:
        """Simple document retrieval based on text matching."""
        top_k = top_k or self.max_documents

        # Simple retrieval - in a real implementation, you'd use embeddings
        relevant_docs = []
        query_lower = query.lower()

        for doc in self.documents:
            content_lower = doc.page_content.lower()
            # Simple keyword matching
            if any(word in content_lower for word in query_lower.split()):
                relevant_docs.append(doc)

        return relevant_docs[:top_k]

    def run_retrieval(self, state: MultiAgentRAGState) -> dict[str, Any]:
        """Run document retrieval and update state."""
        retrieved = self.retrieve_documents(state.query)

        return {
            "retrieved_documents": retrieved,
            "current_operation": RAGOperationType.RETRIEVE,
            "retrieval_confidence": min(
                1.0, len(retrieved) / 3.0
            ),  # Simple confidence measure
        }


class SimpleRAGAnswerAgent(SimpleAgent):
    """RAG answer generation agent that creates responses from retrieved documents.

    This agent focuses specifically on generating high-quality answers from
    retrieved documents using structured prompts.
    """

    def __init__(self, use_citations: bool = False, **kwargs):
        # Choose appropriate prompt template
        prompt_template = (
            RAG_ANSWER_WITH_CITATIONS if use_citations else RAG_ANSWER_STANDARD
        )

        # Set up default engine if none provided
        if "engine" not in kwargs:
            kwargs["engine"] = AugLLMConfig(
                prompt_template=prompt_template, name="rag_answer_engine"
            )

        # Set default name
        if "name" not in kwargs:
            kwargs["name"] = "RAG Answer Agent"

        super().__init__(**kwargs)

        # Store as private attribute (not Pydantic field)
        self._use_citations = use_citations

    @property
    def use_citations(self) -> bool:
        """Get whether to use citations in answers."""
        return self._use_citations

    @use_citations.setter
    def use_citations(self, value: bool):
        """Set whether to use citations in answers."""
        self._use_citations = value

    def generate_answer(self, query: str, documents: list[Document]) -> str:
        """Generate answer from query and documents."""
        # Format documents for the prompt
        doc_text = "\n\n".join(
            [f"Document {i+1}: {doc.page_content}" for i, doc in enumerate(documents)]
        )

        # Use the engine to generate response
        response = self.engine.invoke({"query": query, "retrieved_documents": doc_text})

        return response.get("answer", str(response))

    def run_generation(self, state: MultiAgentRAGState) -> dict[str, Any]:
        """Run answer generation and update state."""
        # Use filtered documents if available, otherwise retrieved documents
        docs_to_use = state.filtered_documents or state.retrieved_documents

        if not docs_to_use:
            return {
                "generated_answer": "No relevant documents found to answer the query.",
                "generation_confidence": 0.0,
                "errors": ["No documents available for answer generation"],
            }

        answer = self.generate_answer(state.query, docs_to_use)

        return {
            "generated_answer": answer,
            "current_operation": RAGOperationType.GENERATE,
            "generation_confidence": 0.8,  # Could be more sophisticated
        }


class DocumentGradingAgent(SimpleAgent):
    """Document grading agent that evaluates document relevance.

    This agent can iterate over retrieved documents and grade each one for
    relevance to the query using configurable grading strategies.
    """

    def __init__(
        self,
        grading_mode: str = "binary",
        min_relevance_threshold: float = 0.5,
        **kwargs,
    ):
        # Set up structured output for grading results
        if grading_mode == "binary":
            kwargs["structured_output_model"] = DocumentBinaryResponse
            prompt_template = RAG_DOCUMENT_GRADE_BINARY
        else:
            # For more detailed grading, we could use comprehensive grader
            prompt_template = RAG_DOCUMENT_ITERATOR_PROMPT_TEMPLATE

        # Set up default engine if none provided
        if "engine" not in kwargs:
            kwargs["engine"] = AugLLMConfig(
                prompt_template=prompt_template,
                structured_output_model=kwargs.get("structured_output_model"),
                name="document_grading_engine",
            )

        # Set default name
        if "name" not in kwargs:
            kwargs["name"] = "Document Grading Agent"

        super().__init__(**kwargs)

        # Store as private attributes (not Pydantic fields)
        self._grading_mode = grading_mode
        self._min_relevance_threshold = min_relevance_threshold

    @property
    def grading_mode(self) -> str:
        """Get the grading mode."""
        return self._grading_mode

    @grading_mode.setter
    def grading_mode(self, value: str):
        """Set the grading mode."""
        self._grading_mode = value

    @property
    def min_relevance_threshold(self) -> float:
        """Get the minimum relevance threshold."""
        return self._min_relevance_threshold

    @min_relevance_threshold.setter
    def min_relevance_threshold(self, value: float):
        """Set the minimum relevance threshold."""
        self._min_relevance_threshold = value

    def grade_document(self, query: str, document: Document) -> DocumentGradingResult:
        """Grade a single document for relevance."""
        # Format the document for evaluation
        doc_text = f"Title: {document.metadata.get('title', 'N/A')}\nContent: {document.page_content}"

        if self.grading_mode == "binary":
            # Use binary grading
            response = self.engine.invoke(
                {"query": query, "retrieved_documents": doc_text}
            )

            # Extract grading decision (this would be more sophisticated in practice)
            is_relevant = "pass" in str(response).lower()
            score = 1.0 if is_relevant else 0.0
            reason = str(response)

        else:
            # Use detailed grading
            response = self.engine.invoke({"query": query, "document": doc_text})

            # Parse response for score and reasoning (simplified)
            score = 0.7  # Would extract from response
            is_relevant = score >= self.min_relevance_threshold
            reason = str(response)

        return DocumentGradingResult(
            document_id=str(hash(document.page_content))[:8],
            document=document,
            relevance_score=score,
            is_relevant=is_relevant,
            grading_reason=reason,
            grader_type=self.grading_mode,
        )

    def grade_documents(
        self, query: str, documents: list[Document]
    ) -> list[DocumentGradingResult]:
        """Grade multiple documents."""
        results = []
        for doc in documents:
            result = self.grade_document(query, doc)
            results.append(result)
        return results

    def run_grading(self, state: MultiAgentRAGState) -> dict[str, Any]:
        """Run document grading and update state."""
        documents_to_grade = state.retrieved_documents

        if not documents_to_grade:
            return {
                "errors": ["No documents to grade"],
                "current_operation": RAGOperationType.GRADE,
            }

        grading_results = self.grade_documents(state.query, documents_to_grade)

        # Filter relevant documents
        relevant_docs = [
            result.document
            for result in grading_results
            if result.is_relevant
            and result.relevance_score >= self.min_relevance_threshold
        ]

        return {
            "graded_documents": grading_results,
            "filtered_documents": relevant_docs,
            "current_operation": RAGOperationType.GRADE,
        }


class IterativeDocumentGradingAgent(DocumentGradingAgent):
    """Specialized grading agent that processes documents one by one.

    This agent demonstrates the capability to iterate over retrieved documents
    and process each one individually with custom callables.
    """

    def __init__(self, custom_grader: Callable | None = None, **kwargs):
        super().__init__(**kwargs)
        self.custom_grader = custom_grader

    def run_iterative_grading(self, state: MultiAgentRAGState) -> dict[str, Any]:
        """Run iterative document grading with custom processing."""
        documents_to_grade = state.retrieved_documents

        if not documents_to_grade:
            return {
                "errors": ["No documents to grade iteratively"],
                "current_operation": RAGOperationType.GRADE,
            }

        grading_results = []

        # Process each document individually
        for i, doc in enumerate(documents_to_grade):
            if self.custom_grader:
                # Use custom grader callable
                try:
                    custom_result = self.custom_grader(state.query, doc)
                    # Convert custom result to standard format
                    result = DocumentGradingResult(
                        document_id=f"doc_{i}",
                        document=doc,
                        relevance_score=custom_result.get("score", 0.5),
                        is_relevant=custom_result.get("relevant", True),
                        grading_reason=custom_result.get(
                            "reason", "Custom grader result"
                        ),
                        grader_type="custom",
                    )
                except Exception as e:
                    # Fallback to standard grading
                    result = self.grade_document(state.query, doc)
                    result.grading_reason += f" (Custom grader failed: {e!s})"
            else:
                # Use standard grading
                result = self.grade_document(state.query, doc)

            grading_results.append(result)

            # Add step tracking for each document processed
            state.add_workflow_step(
                operation_type=RAGOperationType.GRADE,
                agent_name=self.name,
                input_data={"document_id": result.document_id},
                output_data={
                    "relevance_score": result.relevance_score,
                    "is_relevant": result.is_relevant,
                },
            )

        # Filter relevant documents
        relevant_docs = [
            result.document
            for result in grading_results
            if result.is_relevant
            and result.relevance_score >= self.min_relevance_threshold
        ]

        return {
            "graded_documents": grading_results,
            "filtered_documents": relevant_docs,
            "current_operation": RAGOperationType.GRADE,
        }


# ============================================================================
# CONVENIENCE FACTORY FUNCTIONS
# ============================================================================


def create_simple_rag_agent(
    documents: list[Document] | None = None, **kwargs
) -> SimpleRAGAgent:
    """Create a simple RAG agent with default configuration."""
    return SimpleRAGAgent.from_documents(
        documents=documents or conversation_documents, **kwargs
    )


def create_rag_answer_agent(
    use_citations: bool = False, **kwargs
) -> SimpleRAGAnswerAgent:
    """Create a RAG answer agent with default configuration."""
    return SimpleRAGAnswerAgent(use_citations=use_citations, **kwargs)


def create_document_grading_agent(
    grading_mode: str = "binary", min_threshold: float = 0.5, **kwargs
) -> DocumentGradingAgent:
    """Create a document grading agent with default configuration."""
    return DocumentGradingAgent(
        grading_mode=grading_mode, min_relevance_threshold=min_threshold, **kwargs
    )


def create_iterative_grading_agent(
    custom_grader: Callable | None = None, **kwargs
) -> IterativeDocumentGradingAgent:
    """Create an iterative document grading agent."""
    return IterativeDocumentGradingAgent(custom_grader=custom_grader, **kwargs)


# ============================================================================
# PREDEFINED AGENT INSTANCES (as requested in the prompt)
# ============================================================================

# Simple RAG Agent using conversation documents
SIMPLE_RAG_AGENT = SimpleRAGAgent.from_documents(conversation_documents)

# Simple RAG Answer Agent with the exact template from the prompt
SIMPLE_RAG_ANSWER_AGENT = SimpleRAGAnswerAgent(
    engine=AugLLMConfig(prompt_template=RAG_ANSWER_BASE_PROMPT_TEMPLATE)
)
