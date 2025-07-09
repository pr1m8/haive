"""Enhanced Multi-Agent RAG Workflows

Implements advanced RAG patterns like CRAG, Self-RAG, HYDE, and grading workflows
using the new multi-agent base with compatibility and enhanced state management.
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
from haive.agents.multi.base import ConditionalAgent, SequentialAgent
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


class CorrectiveRAGAgent(ConditionalAgent):
    """Corrective RAG (CRAG) with automatic requerying and web search fallback.

    Flow:
    1. Initial retrieval
    2. Grade documents
    3. If quality is poor -> requery or web search
    4. Generate answer with best available docs
    """

    def __init__(
        self,
        retrieval_agent: Optional[SimpleRAGAgent] = None,
        grading_agent: Optional[DocumentGradingAgent] = None,
        requery_agent: Optional[RequeryDecisionAgent] = None,
        answer_agent: Optional[SimpleAgent] = None,
        documents: Optional[list[Document]] = None,
        **kwargs,
    ):
        # Create default agents if not provided
        if not retrieval_agent:
            from haive.core.fixtures.documents import conversation_documents

            retrieval_agent = SimpleRAGAgent.from_documents(
                documents or conversation_documents, name="CRAG Retrieval Agent"
            )

        if not grading_agent:
            grading_agent = DocumentGradingAgent()

        if not requery_agent:
            requery_agent = RequeryDecisionAgent()

        if not answer_agent:
            answer_agent = SimpleAgent(name="CRAG Answer Agent", engine=AugLLMConfig())

        # Initialize with agents
        agents = [retrieval_agent, grading_agent, requery_agent, answer_agent]

        super().__init__(
            name="Corrective RAG Agent",
            agents=agents,
            state_schema=MultiAgentRAGState,
            **kwargs,
        )

        self.retrieval_agent = retrieval_agent
        self.grading_agent = grading_agent
        self.requery_agent = requery_agent
        self.answer_agent = answer_agent

        # Set up conditional routing
        self._setup_crag_routing()

    def _setup_crag_routing(self):
        """Set up CRAG conditional routing logic."""

        def crag_router(state: MultiAgentRAGState) -> str:
            """Route based on CRAG logic."""
            # Start with retrieval if no documents
            if not state.retrieved_documents:
                return self._get_agent_node_name(self.retrieval_agent)

            # Grade documents if not graded
            if not state.graded_documents:
                return self._get_agent_node_name(self.grading_agent)

            # Check if requerying is needed
            if not hasattr(state, "needs_requery"):
                return self._get_agent_node_name(self.requery_agent)

            # If requery needed and haven't hit limit
            if (
                getattr(state, "needs_requery", False)
                and state.retrieval_count < state.max_retrievals
            ):
                # Clear previous docs and requery
                state.retrieved_documents = []
                state.graded_documents = []
                state.retrieval_count += 1
                return self._get_agent_node_name(self.retrieval_agent)

            # Otherwise generate answer
            return self._get_agent_node_name(self.answer_agent)

        # Add conditional edges from each agent
        for agent in self.agents:
            self.add_conditional_edge(
                source_agent=agent,
                condition=crag_router,
                destinations={self._get_agent_node_name(a): a for a in self.agents},
                default=END,
            )


class HYDERAGAgent(SequentialAgent):
    """HYDE RAG agent that generates hypothetical documents before retrieval."""

    def __init__(
        self,
        hypothesis_agent: Optional[SimpleAgent] = None,
        retrieval_agent: Optional[SimpleRAGAgent] = None,
        answer_agent: Optional[SimpleAgent] = None,
        documents: Optional[list[Document]] = None,
        **kwargs,
    ):
        # Create hypothesis generator
        if not hypothesis_agent:
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

        # Create retrieval agent that will use hypothesis for similarity search
        if not retrieval_agent:
            from haive.core.fixtures.documents import conversation_documents

            retrieval_agent = SimpleRAGAgent.from_documents(
                documents or conversation_documents, name="HYDE Retrieval Agent"
            )

        if not answer_agent:
            answer_agent = SimpleAgent(name="HYDE Answer Agent", engine=AugLLMConfig())

        super().__init__(
            name="HYDE RAG Agent",
            agents=[hypothesis_agent, retrieval_agent, answer_agent],
            state_schema=MultiAgentRAGState,
            **kwargs,
        )


class SelfRAGAgent(ConditionalAgent):
    """Self-RAG agent with reflection tokens and adaptive retrieval."""

    def __init__(
        self,
        retrieval_decision_agent: Optional[SimpleAgent] = None,
        retrieval_agent: Optional[SimpleRAGAgent] = None,
        relevance_agent: Optional[SimpleAgent] = None,
        generation_agent: Optional[SimpleAgent] = None,
        documents: Optional[list[Document]] = None,
        **kwargs,
    ):
        # Create retrieval decision agent
        if not retrieval_decision_agent:
            from langchain_core.prompts import ChatPromptTemplate

            retrieval_prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """You decide if external knowledge retrieval is needed.
                Respond with exactly one of:
                - [Retrieval] if the question requires external knowledge
                - [No Retrieval] if you can answer with your internal knowledge""",
                    ),
                    ("human", "Question: {query}"),
                ]
            )

            retrieval_decision_agent = SimpleAgent(
                name="Self-RAG Retrieval Decision",
                engine=AugLLMConfig(prompt_template=retrieval_prompt),
            )

        # Create other agents with default configurations
        if not retrieval_agent:
            from haive.core.fixtures.documents import conversation_documents

            retrieval_agent = SimpleRAGAgent.from_documents(
                documents or conversation_documents, name="Self-RAG Retrieval Agent"
            )

        if not relevance_agent:
            relevance_agent = SimpleAgent(
                name="Self-RAG Relevance Checker", engine=AugLLMConfig()
            )

        if not generation_agent:
            generation_agent = SimpleAgent(
                name="Self-RAG Generator", engine=AugLLMConfig()
            )

        agents = [
            retrieval_decision_agent,
            retrieval_agent,
            relevance_agent,
            generation_agent,
        ]

        super().__init__(
            name="Self-RAG Agent",
            agents=agents,
            state_schema=MultiAgentRAGState,
            **kwargs,
        )

        self.retrieval_decision_agent = retrieval_decision_agent
        self.retrieval_agent = retrieval_agent
        self.relevance_agent = relevance_agent
        self.generation_agent = generation_agent

        self._setup_self_rag_routing()

    def _setup_self_rag_routing(self):
        """Set up Self-RAG routing with reflection tokens."""

        def self_rag_router(state: MultiAgentRAGState) -> str:
            """Route based on Self-RAG reflection logic."""

            # Check if we need retrieval decision
            if (
                not hasattr(state, "needs_retrieval_decision")
                or not state.needs_retrieval_decision
            ):
                return self._get_agent_node_name(self.retrieval_decision_agent)

            # If retrieval is needed and not done
            needs_retrieval = getattr(state, "needs_retrieval", True)
            if needs_retrieval and not state.retrieved_documents:
                return self._get_agent_node_name(self.retrieval_agent)

            # Check relevance if documents retrieved but not checked
            if state.retrieved_documents and not hasattr(state, "relevance_checked"):
                return self._get_agent_node_name(self.relevance_agent)

            # Generate final answer
            return self._get_agent_node_name(self.generation_agent)

        # Set up conditional routing
        for agent in self.agents:
            self.add_conditional_edge(
                source_agent=agent,
                condition=self_rag_router,
                destinations={self._get_agent_node_name(a): a for a in self.agents},
                default=END,
            )


def create_enhanced_rag_workflow(
    workflow_type: str = "crag", documents: Optional[list[Document]] = None, **kwargs
) -> Agent:
    """Factory function to create enhanced RAG workflows.

    Args:
        workflow_type: Type of workflow ("crag", "hyde", "self_rag")
        documents: Documents for retrieval
        **kwargs: Additional arguments

    Returns:
        Configured RAG agent
    """
    if workflow_type.lower() == "crag":
        return CorrectiveRAGAgent(documents=documents, **kwargs)
    elif workflow_type.lower() == "hyde":
        return HYDERAGAgent(documents=documents, **kwargs)
    elif workflow_type.lower() == "self_rag":
        return SelfRAGAgent(documents=documents, **kwargs)
    else:
        raise ValueError(f"Unknown workflow type: {workflow_type}")


__all__ = [
    "DocumentGradingAgent",
    "RequeryDecisionAgent",
    "CorrectiveRAGAgent",
    "HYDERAGAgent",
    "SelfRAGAgent",
    "create_enhanced_rag_workflow",
]
