"""Corrective RAG (CRAG) Agent V2.

Self-correcting retrieval with proper quality assessment.
Implements architecture from rag-architectures-flows.md:
Retrieval → Relevance Check → Knowledge Refinement/Web Search/Combine
"""

from collections.abc import Callable
from typing import Any, Dict, List, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import LLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from haive.agents.multi.base import ConditionalAgent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.rag.common.answer_generators.prompts import RAG_ANSWER_STANDARD
from haive.agents.rag.common.document_graders.binary_grader.prompt import (
    RAG_DOCUMENT_GRADE_BINARY,
)
from haive.agents.rag.common.document_graders.models import DocumentBinaryResponse
from haive.agents.simple.agent import SimpleAgent

# Web search prompt for when documents aren't relevant
WEB_SEARCH_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a web search query generator. Create effective search queries.",
        ),
        (
            "human",
            """The user's question could not be answered with the available documents.

Original question: {query}
Failed documents: {retrieved_documents}

Generate 2-3 web search queries that would help find relevant information.""",
        ),
    ]
)


# Document refinement prompt
REFINE_DOCS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a document refinement specialist. Extract and organize the most relevant information.",
        ),
        (
            "human",
            """Refine these partially relevant documents to focus on answering the query.

Query: {query}
Documents: {retrieved_documents}
Grading results: {document_decisions}

Extract and organize only the relevant portions that help answer the query.""",
        ),
    ]
)


class CorrectiveRAGAgentV2(ConditionalAgent):
    """Corrective RAG with proper self-correcting retrieval."""

    @classmethod
    def from_documents(
        cls,
        documents: list[Document],
        llm_config: LLMConfig | None = None,
        relevance_threshold: float = 0.7,
        **kwargs
    ):
        """Create Corrective RAG from documents.

        Args:
            documents: Documents to index
            llm_config: Optional LLM configuration
            relevance_threshold: Threshold for document relevance (0-1)
            **kwargs: Additional arguments

        Returns:
            CorrectiveRAGAgentV2 instance
        """
        # Create agents
        retrieval_agent = BaseRAGAgent.from_documents(
            documents=documents, name="CRAG Retriever"
        )

        grader_agent = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=RAG_DOCUMENT_GRADE_BINARY,
                structured_output_model=DocumentBinaryResponse,
            ),
            name="Document Grader",
        )

        # Web search agent (placeholder for now)
        web_search_agent = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config, prompt_template=WEB_SEARCH_PROMPT
            ),
            name="Web Search Query Generator",
        )

        # Document refiner agent
        refiner_agent = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config, prompt_template=REFINE_DOCS_PROMPT
            ),
            name="Document Refiner",
        )

        answer_agent = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config, prompt_template=RAG_ANSWER_STANDARD
            ),
            name="Answer Generator",
        )

        # Define conditional routing based on grading
        def grade_documents(state: dict[str, Any]) -> str:
            """Grade documents and determine next step."""
            # Check if we have grading results
            if state.get("document_decisions"):
                decisions = state["document_decisions"]

                # Count passing documents
                passing_docs = sum(
                    1 for decision in decisions if decision.decision == "pass"
                )
                total_docs = len(decisions)

                if total_docs == 0:
                    return "web_search"

                relevance_ratio = passing_docs / total_docs

                # Route based on relevance threshold
                if relevance_ratio >= relevance_threshold:
                    return "answer"  # All good, generate answer
                if relevance_ratio > 0.3:  # Some relevant docs
                    return "refiner"  # Refine partially relevant docs
                return "web_search"  # Need external search

            # No grading results yet, check if we have docs
            docs = state.get("retrieved_documents", [])
            if not docs:
                return "web_search"

            # Default: grade the documents first
            return "grader"

        # Define branches for conditional routing
        branches = {
            "retriever": {
                "condition": lambda s: "grader",  # Always go to grader after retrieval
                "mapping": {"grader": "grader"},
            },
            "grader": {
                "condition": grade_documents,
                "mapping": {
                    "answer": "answer",
                    "web_search": "web_search",
                    "refiner": "refiner",
                },
            },
            "refiner": {
                "condition": lambda s: "answer",  # After refinement, generate answer
                "mapping": {"answer": "answer"},
            },
            "web_search": {
                "condition": lambda s: "answer",  # After web search, generate answer
                "mapping": {"answer": "answer"},
            },
        }

        return cls(
            agents=[
                retrieval_agent,
                grader_agent,
                web_search_agent,
                refiner_agent,
                answer_agent,
            ],
            branches=branches,
            name=kwargs.get("name", "Corrective RAG Agent V2"),
            **kwargs
        )
