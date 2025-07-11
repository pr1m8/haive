"""HyDE (Hypothetical Document Embeddings) RAG Agent V2.

Bridges query-document semantic gap by generating hypothetical documents.
This version properly embeds the hypothetical document for retrieval.
"""

from typing import Any, Dict, List, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.agent_node import AgentNodeConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import LLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START
from pydantic import Field

from haive.agents.base.agent import Agent
from haive.agents.multi.base import SequentialAgent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.simple.agent import SimpleAgent

HYDE_GENERATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at generating hypothetical documents that would answer questions.
Your task is to write a detailed, informative document that contains the information needed to answer the given question.

Guidelines:
- Write as if you are creating an authoritative reference document
- Include specific details, examples, and explanations
- Use clear, factual language
- Make the document comprehensive enough to fully answer the question
- Do not mention that this is hypothetical - write as if stating facts

Please provide your response in the following format:
{format_instructions}""",
        ),
        (
            "human",
            """Write a detailed document that would contain the answer to this question:

Question: {query}""",
        ),
    ]
)


HYDE_RETRIEVAL_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Transform the hypothetical document into an effective search query.",
        ),
        (
            "human",
            """Based on this hypothetical answer document, create a search query to find similar real documents:

Hypothetical Document:
{hypothetical_doc}

Original Question: {query}

Search Query:""",
        ),
    ]
)


class HyDERetrieverAgent(Agent):
    """Custom retriever that uses hypothetical document for enhanced retrieval."""

    name: str = "HyDE Retriever"
    base_retriever: BaseRAGAgent = Field(..., description="Base retriever to use")

    def build_graph(self) -> BaseGraph:
        """Build graph that passes hypothetical doc as query."""
        graph = BaseGraph(name="HyDERetriever")

        # Transform node that uses hypothetical_doc as the query
        def transform_to_query(state: dict[str, Any]) -> dict[str, Any]:
            """Use hypothetical document as the retrieval query."""
            # Get the structured HyDE result from state
            hyde_result = state.get("hyde_result", {})

            # Extract hypothetical document or fall back to refined query
            if isinstance(hyde_result, dict):
                hyp_doc = hyde_result.get(
                    "hypothetical_doc",
                    hyde_result.get("refined_query", state.get("query", "")),
                )
            else:
                # If it's a HyDEResult object
                hyp_doc = getattr(
                    hyde_result, "hypothetical_doc", state.get("query", "")
                )

            # Use it as the query for retrieval
            return {
                "query": hyp_doc,
                "original_query": state.get("query", ""),
                "hyde_result": hyde_result,
            }

        # Add transform node
        graph.add_node("transform", transform_to_query)

        # Add the base retriever's graph as a subgraph
        retriever_node = EngineNodeConfig(
            engine=self.base_retriever.engine, name="retriever"
        )
        graph.add_node("retriever", retriever_node)

        # Connect: START -> transform -> retriever -> END
        graph.add_edge(START, "transform")
        graph.add_edge("transform", "retriever")
        graph.add_edge("retriever", END)

        return graph


class HyDERAGAgentV2(SequentialAgent):
    """HyDE RAG using hypothetical document generation for better retrieval.

    This version properly uses the hypothetical document as the basis for retrieval.
    """

    @classmethod
    def from_documents(
        cls,
        documents: list[Document],
        llm_config: LLMConfig | None = None,
        embedding_model: str | None = None,
        **kwargs
    ):
        """Create HyDE RAG from documents.

        Args:
            documents: Documents to index
            llm_config: Optional LLM configuration
            embedding_model: Optional embedding model for vector store
            **kwargs: Additional arguments

        Returns:
            HyDERAGAgentV2 instance
        """
        # Step 1: Generate hypothetical document with structured output
        from haive.agents.rag.models import HyDEResult

        hyde_generator = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=HYDE_GENERATION_PROMPT,
                structured_output_model=HyDEResult,
                structured_output_version="v1",  # Use parser-based approach
                output_key="hyde_result",
            ),
            name="HyDE Generator",
        )

        # Step 2: Create base retriever
        base_retriever = BaseRAGAgent.from_documents(
            documents=documents, embedding_model=embedding_model, name="Base Retriever"
        )

        # Step 3: Create HyDE retriever that uses hypothetical doc
        hyde_retriever = HyDERetrieverAgent(
            base_retriever=base_retriever, name="HyDE Retriever"
        )

        # Step 4: Generate final answer using standard RAG prompt
        from haive.agents.rag.common.answer_generators.prompts import (
            RAG_ANSWER_STANDARD,
        )

        answer_agent = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config, prompt_template=RAG_ANSWER_STANDARD
            ),
            name="Answer Generator",
        )

        return cls(
            agents=[hyde_generator, hyde_retriever, answer_agent],
            name=kwargs.get("name", "HyDE RAG Agent V2"),
            **kwargs
        )
