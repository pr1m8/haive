"""Simple Enhanced Multi-Agent RAG Workflows

Clean implementation of advanced RAG patterns without complex dependencies.
"""

from typing import Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.callable_node import (
    CallableNodeConfig,
    create_document_grader,
    requery_decision,
    simple_document_grader,
)
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.prebuilt.rag_state import MultiAgentRAGState
from langchain_core.documents import Document
from langgraph.graph import END, START

from haive.agents.base.agent import Agent
from haive.agents.multi.base import SequentialAgent
from haive.agents.rag.base.agent import SimpleRAGAgent
from haive.agents.simple.agent import SimpleAgent


class DocumentGradingAgent(Agent):
    """Agent that grades retrieved documents for relevance."""

    name: str = "Document Grading Agent"

    def build_graph(self) -> BaseGraph:
        """Build graph that grades each retrieved document."""
        graph = BaseGraph(name="DocumentGradingAgent")

        # Add document grader node
        grader_node = create_document_grader(
            grading_func=simple_document_grader, name="grade_documents"
        )
        graph.add_node("grade_documents", grader_node)

        # Simple flow: START -> grade -> END
        graph.add_edge(START, "grade_documents")
        graph.add_edge("grade_documents", END)

        return graph


class RequeryDecisionAgent(Agent):
    """Agent that decides if requerying is needed based on document grades."""

    name: str = "Requery Decision Agent"

    def build_graph(self) -> BaseGraph:
        """Build graph that analyzes grades and decides on requerying."""
        graph = BaseGraph(name="RequeryDecisionAgent")

        # Add requery decision node
        decision_node = CallableNodeConfig(
            name="requery_decision", callable_func=requery_decision, pass_state=True
        )
        graph.add_node("requery_decision", decision_node)

        graph.add_edge(START, "requery_decision")
        graph.add_edge("requery_decision", END)

        return graph


class SimpleCorrectiveRAGAgent(SequentialAgent):
    """Simple Corrective RAG implementation using sequential processing."""

    def __init__(self, documents: Optional[list[Document]] = None, **kwargs):
        # Create retrieval agent
        from haive.core.fixtures.documents import conversation_documents

        retrieval_agent = SimpleRAGAgent.from_documents(
            documents or conversation_documents, name="CRAG Retrieval Agent"
        )

        # Create grading agent
        grading_agent = DocumentGradingAgent()

        # Create answer agent
        answer_agent = SimpleAgent(name="CRAG Answer Agent", engine=AugLLMConfig())

        super().__init__(
            name="Simple Corrective RAG Agent",
            agents=[retrieval_agent, grading_agent, answer_agent],
            state_schema=MultiAgentRAGState,
            **kwargs,
        )


class SimpleHYDERAGAgent(SequentialAgent):
    """Simple HYDE RAG agent that generates hypothetical documents before retrieval."""

    def __init__(self, documents: Optional[list[Document]] = None, **kwargs):
        # Create hypothesis generator
        from langchain_core.prompts import ChatPromptTemplate

        hyde_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert that generates detailed, accurate responses to questions. Write a comprehensive paragraph that would perfectly answer the given question.",
                ),
                ("human", "Question: {query}\n\nDetailed Answer:"),
            ]
        )

        hypothesis_agent = SimpleAgent(
            name="HYDE Hypothesis Generator",
            engine=AugLLMConfig(prompt_template=hyde_prompt),
        )

        # Create retrieval agent
        from haive.core.fixtures.documents import conversation_documents

        retrieval_agent = SimpleRAGAgent.from_documents(
            documents or conversation_documents, name="HYDE Retrieval Agent"
        )

        # Create answer agent
        answer_agent = SimpleAgent(name="HYDE Answer Agent", engine=AugLLMConfig())

        super().__init__(
            name="Simple HYDE RAG Agent",
            agents=[hypothesis_agent, retrieval_agent, answer_agent],
            state_schema=MultiAgentRAGState,
            **kwargs,
        )


def create_simple_rag_workflow(
    workflow_type: str = "crag", documents: Optional[list[Document]] = None, **kwargs
) -> Agent:
    """Factory function to create simple RAG workflows.

    Args:
        workflow_type: Type of workflow ("crag", "hyde")
        documents: Documents for retrieval
        **kwargs: Additional arguments

    Returns:
        Configured RAG agent
    """
    if workflow_type.lower() == "crag":
        return SimpleCorrectiveRAGAgent(documents=documents, **kwargs)
    elif workflow_type.lower() == "hyde":
        return SimpleHYDERAGAgent(documents=documents, **kwargs)
    else:
        raise ValueError(f"Unknown workflow type: {workflow_type}")


__all__ = [
    "DocumentGradingAgent",
    "RequeryDecisionAgent",
    "SimpleCorrectiveRAGAgent",
    "SimpleHYDERAGAgent",
    "create_simple_rag_workflow",
]
