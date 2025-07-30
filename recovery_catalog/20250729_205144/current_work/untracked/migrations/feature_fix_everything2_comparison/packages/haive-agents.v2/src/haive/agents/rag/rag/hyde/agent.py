"""HyDE (Hypothetical Document Embeddings) RAG Agent.

from typing import Any
Bridges query-document semantic gap by generating hypothetical documents.
Implements architecture from rag-architectures-flows.md:
Query -> Generate Hypothetical Doc -> Embed -> Retrieve Real Docs -> Generate
"""

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from haive.agents.multi import MultiAgent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.simple.agent import SimpleAgent

HYDE_GENERATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at generating hypothetical documents that would answer questions.
Your task is to write a detailed, informative paragraph that would perfectly answer the given question.""",
        ),
        (
            "human",
            """Write a detailed paragraph that would answer this question:
Question: {query}

Paragraph:""",
        ),
    ]
)


HYDE_ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert assistant. Answer based on the retrieved documents.",
        ),
        (
            "human",
            """Answer the question using the retrieved documents.

Original Question: {query}

Retrieved Documents:
{retrieved_documents}

Provide a comprehensive answer:""",
        ),
    ]
)


class HyDERAGAgent(MultiAgent):
    """HyDE RAG using hypothetical document generation for better retrieval."""

    @classmethod
    def from_documents(
        cls, documents: list[Document], llm_config: LLMConfig | None = None, **kwargs
    ):
        """Create HyDE RAG from documents.

        Args:
            documents: Documents to index
            llm_config: Optional LLM configuration
            **kwargs: Additional arguments

        Returns:
            HyDERAGAgent instance
        """
        if not llm_config:
            llm_config = AzureLLMConfig(
                deployment_name="gpt-4",
                azure_endpoint="${AZURE_OPENAI_API_BASE}",
                api_key="${AZURE_OPENAI_API_KEY}",
            )

        # Step 1: Generate hypothetical document
        hyde_generator = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config, prompt_template=HYDE_GENERATION_PROMPT
            ),
            name="hyde_generator",
        )

        # Step 2: Use hypothetical doc for retrieval
        # In a full implementation, we'd embed the hypothetical doc
        # For now, we'll use it as the query
        retrieval_agent = BaseRAGAgent.from_documents(
            documents=documents, name="hyde_retriever"
        )

        # Step 3: Generate final answer
        answer_agent = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config, prompt_template=HYDE_ANSWER_PROMPT
            ),
            name="hyde_answer_generator",
        )

        # Use the clean MultiAgent.create() method
        # Remove name from kwargs to avoid conflict
        agent_name = kwargs.pop("name", "hyde_rag_agent")
        return cls.create(
            agents=[hyde_generator, retrieval_agent, answer_agent],
            name=agent_name,
            execution_mode="sequential",
            **kwargs
        )
