"""Document Grading RAG Agent.

from typing import Any
Iterative document grading with structured output.
Uses CallableNodeConfig to iterate over retrieved documents.
"""

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.callable_node import (
    create_document_grader,
)
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START
from pydantic import BaseModel, Field

from haive.agents.base.agent import Agent
from haive.agents.multi.base import SequentialAgent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.simple.agent import SimpleAgent


# Simple grading model for single document
class SingleDocumentGrade(BaseModel):
    """Grade for a single document."""

    relevance_score: float = Field(ge=0.0, le=1.0, description="Relevance score 0-1")
    is_relevant: bool = Field(description="Whether document is relevant")
    reasoning: str = Field(description="Explanation for the grade")


SINGLE_DOC_GRADING_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert document grader. Assess this document's relevance to the query.

Provide:
1. A relevance score (0.0-1.0)
2. Whether it's relevant (true/false)
3. Clear reasoning for your assessment""",
        ),
        (
            "human",
            """Grade this document for relevance.

Query: {query}

Document:
{document}

Provide your assessment.""",
        ),
    ]
)


class DocumentGradingAgent(Agent):
    """Agent that iterates over documents and grades each one."""

    name: str = "Document Grader"
    relevance_threshold: float = 0.7
    llm_config: LLMConfig | None = None

    def __init__(self, llm_config: LLMConfig | None = None, **kwargs):
        """Initialize with LLM config."""
        self.llm_config = llm_config or AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )
        super().__init__(**kwargs)

    def build_graph(self) -> BaseGraph:
        """Build graph with document grading using CallableNode iteration."""
        graph = BaseGraph(name="DocumentGradingGraph")

        # Create grading engine
        grading_engine = AugLLMConfig(
            llm_config=self.llm_config,
            prompt_template=SINGLE_DOC_GRADING_PROMPT,
            structured_output_model=SingleDocumentGrade,
        )

        # Function to grade a single document
        def grade_single_document(input_data: dict) -> dict:
            """Grade one document using structured output."""
            document = input_data["current_item"]
            state = input_data["state"]
            item_index = input_data["item_index"]

            query = getattr(state, "query", "")

            # Get structured grade
            grade = grading_engine.invoke(
                {"query": query, "document": document.page_content}
            )

            # Return in format expected by CallableNode
            return {
                "document_id": f"doc_{item_index}",
                "relevance_score": grade.relevance_score,
                "is_relevant": grade.is_relevant,
                "reasoning": grade.reasoning,
            }

        # Create document grader node that loops over retrieved_documents
        grading_node = create_document_grader(
            grading_func=grade_single_document, name="grade_documents"
        )

        graph.add_node("grade", grading_node)
        graph.add_edge(START, "grade")
        graph.add_edge("grade", END)

        return graph


class DocumentGradingRAGAgent(SequentialAgent):
    """RAG with document grading and filtering."""

    @classmethod
    def from_documents(
        cls,
        documents: list[Document],
        llm_config: LLMConfig | None = None,
        relevance_threshold: float = 0.7,
        **kwargs,
    ):
        """Create Document Grading RAG from documents."""
        if not llm_config:
            llm_config = AzureLLMConfig(
                deployment_name="gpt-4",
                azure_endpoint="${AZURE_OPENAI_API_BASE}",
                api_key="${AZURE_OPENAI_API_KEY}",
            )

        # Retrieval
        retrieval_agent = BaseRAGAgent.from_documents(
            documents=documents, name="Grading RAG Retriever"
        )

        # Grading with structured output
        grading_agent = DocumentGradingAgent(
            llm_config=llm_config, relevance_threshold=relevance_threshold
        )

        # Answer generation based on relevant docs
        answer_agent = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=ChatPromptTemplate.from_messages(
                    [
                        (
                            "system",
                            "Answer based only on relevant documents that passed grading.",
                        ),
                        (
                            "human",
                            """Answer the query using these relevant documents.

Query: {query}
Relevant Documents: {graded_documents}""",
                        ),
                    ]
                ),
            ),
            name="Graded Answer Generator",
        )

        return cls(
            agents=[retrieval_agent, grading_agent, answer_agent],
            name=kwargs.get("name", "Document Grading RAG Agent"),
            **kwargs,
        )
