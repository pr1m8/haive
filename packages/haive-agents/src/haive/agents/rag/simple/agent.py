"""Simple RAG Agent

Uses SequentialAgent to compose BaseRAG with answer generation.
"""

from typing import List, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage

from haive.agents.multi.base import SequentialAgent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.rag.common.answer_generators.prompts import RAG_ANSWER_STANDARD
from haive.agents.simple.agent import SimpleAgent


class SimpleRAGAgent(SequentialAgent):
    """Simple RAG workflow: Retrieval → Answer Generation"""

    @classmethod
    def from_documents(
        cls, documents: List[Document], llm_config: Optional[LLMConfig] = None, **kwargs
    ):
        """Create SimpleRAG from documents."""
        # Create retrieval agent
        retrieval_agent = BaseRAGAgent.from_documents(
            documents=documents, name="Retriever"
        )

        # Create answer agent with RAG prompt
        if not llm_config:
            llm_config = AzureLLMConfig(
                deployment_name="gpt-4",
                azure_endpoint="${AZURE_OPENAI_API_BASE}",
                api_key="${AZURE_OPENAI_API_KEY}",
            )

        answer_agent = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config, prompt_template=RAG_ANSWER_STANDARD
            ),
            name="Answer Agent",
        )

        # Create sequential multi-agent
        return cls(
            agents=[retrieval_agent, answer_agent],
            name=kwargs.get("name", "Simple RAG Agent"),
            **kwargs
        )
