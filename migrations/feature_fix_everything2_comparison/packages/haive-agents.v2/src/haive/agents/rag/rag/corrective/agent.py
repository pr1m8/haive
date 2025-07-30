"""Corrective RAG (CRAG) Agent.

from typing import Any, Dict
Self-correcting retrieval with quality assessment.
Implements architecture from rag-architectures-flows.md:
Retrieval → Relevance Check → Knowledge Refinement/Web Search/Combine
"""

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from haive.agents.multi.base import ConditionalAgent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.rag.common.document_graders.models import DocumentGrade
from haive.agents.simple.agent import SimpleAgent

DOCUMENT_GRADER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a grader assessing relevance of retrieved documents to a user question.",
        ),
        (
            "human",
            """Grade the relevance of this document to the question.

Question: {query}
Document: {document}

Give a binary score 'yes' or 'no' to indicate whether the document is relevant to the question.""",
        ),
    ]
)


ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert assistant. Answer based only on the provided context.",
        ),
        (
            "human",
            """Answer the question based on the context.

Question: {query}
Context: {retrieved_documents}""",
        ),
    ]
)


class CorrectiveRAGAgent(ConditionalAgent):
    """Corrective RAG with self-correcting retrieval."""

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
            relevance_threshold: Threshold for document relevance
            **kwargs: Additional arguments

        Returns:
            CorrectiveRAGAgent instance
        """
        if not llm_config:
            llm_config = AzureLLMConfig(
                deployment_name="gpt-4",
                azure_endpoint="${AZURE_OPENAI_API_BASE}",
                api_key="${AZURE_OPENAI_API_KEY}",
            )

        # Create agents
        retrieval_agent = BaseRAGAgent.from_documents(
            documents=documents, name="CRAG Retriever"
        )

        grader_agent = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=DOCUMENT_GRADER_PROMPT,
                structured_output_model=DocumentGrade,
            ),
            name="Document Grader",
        )

        answer_agent = SimpleAgent(
            engine=AugLLMConfig(llm_config=llm_config, prompt_template=ANSWER_PROMPT),
            name="Answer Generator",
        )

        # Define conditional routing based on grading
        def grade_documents(state: Dict[str, Any]):
            """Grade documents and determine next step."""
            docs = state.get("retrieved_documents", [])
            if not docs:
                return "web_search"  # No docs, need web search

            # In real implementation, would grade each doc
            # For now, assume docs are relevant if we have them
            return "generate_answef"

        branches = {
            "grader": {
                "condition": grade_documents,
                "mapping": {
                    "generate_answer": "answer",
                    "web_search": "web_search",  # Would add web search agent
                    "refine": "refiner",  # Would add refinement agent
                },
            }
        }

        return cls(
            agents=[retrieval_agent, grader_agent, answer_agent],
            branches=branches,
            name=kwargs.get("name", "Corrective RAG Agent"),
            **kwargs
        )
