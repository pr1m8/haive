"""Multi_Agent_Simple_Rag core module.

This module provides multi agent simple rag functionality for the Haive framework.

Classes:
    SimpleRAG: SimpleRAG implementation.
    QAResponse: QAResponse implementation.

Functions:
    validate_context_template: Validate Context Template functionality.
    setup_rag_agents: Setup Rag Agents functionality.
    from_documents: From Documents functionality.
"""

#!/usr/bin/env python3
"""SimpleRAG - Proper MultiAgent Implementation.

This is the CORRECT SimpleRAG implementation using the proper MultiAgent pattern:
    SimpleRAG extends MultiAgent with agents={"retriever": BaseRAGAgent, "generator": SimpleAgent}

The key insight is that SimpleRAG IS a MultiAgent that coordinates two specific agents:
1. BaseRAGAgent: Handles document retrieval
2. SimpleAgent: Generates answers from documents

This follows the MultiAgent[AgentsT] pattern where:
- SimpleRAG extends MultiAgent
- agents field contains the two agents
- execution_mode="sequence" for retrieval → generation flow

Examples:
    Basic usage::

        rag = SimpleRAG(
            name="qa_system",
            retriever_config=VectorStoreConfig(vector_store=vector_store),
            llm_config=AugLLMConfig(temperature=0.7),
            top_k=5
        )

        result = await rag.arun("What is machine learning?")

    From documents::

        rag = SimpleRAG.from_documents(
            documents=my_documents,
            embedding_config=embedding_config,
            llm_config=AugLLMConfig()
        )
"""

from __future__ import annotations

import logging
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.retriever import BaseRetrieverConfig
from haive.core.engine.vectorstore import VectorStoreConfig
from langchain_core.documents import Document
from pydantic import BaseModel, Field, field_validator, model_validator

# Import the proper MultiAgent base
from haive.agents.multi.multi_agent import MultiAgent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)


class SimpleRAG(MultiAgent):
    """SimpleRAG - MultiAgent coordinating BaseRAGAgent and SimpleAgent.

    This is the proper implementation of SimpleRAG following the MultiAgent pattern:

    Structure:
        SimpleRAG extends MultiAgent
        agents = {
            "retriever": BaseRAGAgent,  # Handles document retrieval
            "generator": SimpleAgent    # Generates answers from documents
        }
        execution_mode = "sequence"  # retriever → generator

    The MultiAgent pattern means:
    - SimpleRAG IS a MultiAgent
    - It contains other agents in its agents field
    - It coordinates their execution in sequence
    - It uses the proper graph building and state management

    This is much cleaner than custom composition because it leverages
    the existing MultiAgent infrastructure for routing, state management,
    and execution patterns.

    Examples:
        Basic RAG::

            rag = SimpleRAG(
                name="qa_assistant",
                retriever_config=VectorStoreConfig(vector_store=vector_store),
                llm_config=AugLLMConfig(temperature=0.7),
                top_k=5
            )

            result = await rag.arun("What is machine learning?")

        With structured output::

            class QAResponse(BaseModel):
                answer: str
                sources: List[str]
                confidence: float

            rag = SimpleRAG(
                name="structured_qa",
                retriever_config=retriever_config,
                llm_config=llm_config,
                structured_output_model=QAResponse
            )

        From documents::

            rag = SimpleRAG.from_documents(
                documents=my_documents,
                embedding_config=embedding_config,
                llm_config=AugLLMConfig()
            )
    """

    # =============================
    # RAG-Specific Configuration Fields
    # =============================

    retriever_config: BaseRetrieverConfig | VectorStoreConfig = Field(
        ...,
        description="Configuration for document retrieval (vector store or retriever)",
    )

    llm_config: AugLLMConfig = Field(
        ..., description="Configuration for answer generation LLM"
    )

    # Retrieval parameters
    top_k: int = Field(
        default=5,
        ge=1,
        le=50,
        description="Number of documents to retrieve from vector store",
    )

    similarity_threshold: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Minimum similarity score for retrieved documents",
    )

    # Generation parameters
    structured_output_model: type[BaseModel] | None = Field(
        default=None, description="Pydantic model for structured output formatting"
    )

    context_template: str = Field(
        default="Context:\n{context}\n\nQuestion: {query}\n\nAnswer:",
        min_length=10,
        description="Template for formatting context and query for LLM",
    )

    system_prompt_template: str = Field(
        default=(
            "You are a helpful assistant that answers questions based on the provided context. "
            "Use only the information in the context to answer the question. "
            "If the context doesn't contain enough information, say so clearly."
        ),
        min_length=10,
        description="System prompt template for answer generation",
    )

    # =============================
    # Validation and Setup
    # =============================

    @field_validator("context_template")
    @classmethod
    def validate_context_template(cls, v: str) -> str:
        """Validate context template has required placeholders."""
        required_placeholders = {"{context}", "{query}"}
        missing = required_placeholders - {
            ph for ph in required_placeholders if ph in v
        }
        if missing:
            raise ValueError(
                f"Context template missing required placeholders: {missing}"
            )
        return v

    @model_validator(mode="after")
    def setup_rag_agents(self) -> SimpleRAG:
        """Setup the retriever and generator agents after validation."""
        # Create retriever agent
        retriever_agent = BaseRAGAgent(
            name=f"{self.name}_retriever", engine=self.retriever_config
        )

        # Create generator agent with customized system prompt
        generator_config = self.llm_config.model_copy()
        if not generator_config.system_message:
            generator_config.system_message = self.system_prompt_template

        generator_agent = SimpleAgent(
            name=f"{self.name}_generatof",
            engine=generator_config,
            structured_output_model=self.structured_output_model,
        )

        # Set up the agents dictionary (required by MultiAgent)
        self.agents = {"retriever": retriever_agent, "generator": generator_agent}

        # Set execution mode to sequential (retriever → generator)
        self.execution_mode = "sequence"

        # Set up coordinator config (inherited from MultiAgent)
        # For sequential mode, we don't need coordinator but MultiAgent expects it
        if not hasattr(self, "coordinator_config") or self.coordinator_config is None:
            self.coordinator_config = self.llm_config

        return self

    # =============================
    # Class Methods for Creation
    # =============================

    @classmethod
    def from_documents(
        cls,
        documents: list[Document],
        embedding_config: Any,
        llm_config: AugLLMConfig,
        name: str = "SimpleRAG_from_docs",
        **kwargs,
    ) -> SimpleRAG:
        """Create SimpleRAG from a list of documents.

        Args:
            documents: List of documents to create vector store from
            embedding_config: Embedding configuration for vector store
            llm_config: LLM configuration for answer generation
            name: Name for the RAG agent
            **kwargs: Additional configuration parameters

        Returns:
            Configured SimpleRAG instance
        """
        # Use BaseRAGAgent's from_documents method to get retriever config
        retriever_agent = BaseRAGAgent.from_documents(
            documents=documents,
            embedding_model=embedding_config,
            name=f"{name}_retriever",
        )

        return cls(
            name=name,
            retriever_config=retriever_agent.engine,
            llm_config=llm_config,
            **kwargs,
        )

    @classmethod
    def from_vectorstore(
        cls,
        vector_store_config: VectorStoreConfig,
        llm_config: AugLLMConfig,
        name: str = "SimpleRAG_from_vs",
        **kwargs,
    ) -> SimpleRAG:
        """Create SimpleRAG from existing vector store configuration.

        Args:
            vector_store_config: Vector store configuration
            llm_config: LLM configuration for answer generation
            name: Name for the RAG agent
            **kwargs: Additional configuration parameters

        Returns:
            Configured SimpleRAG instance
        """
        return cls(
            name=name,
            retriever_config=vector_store_config,
            llm_config=llm_config,
            **kwargs,
        )

    # =============================
    # RAG-Specific Methods
    # =============================

    def get_retriever_agent(self) -> BaseRAGAgent:
        """Get the retriever agent."""
        return self.agents["retriever"]

    def get_generator_agent(self) -> SimpleAgent:
        """Get the generator agent."""
        return self.agents["generator"]

    async def retrieve_documents(
        self,
        query: str,
        k: int | None = None,
        score_threshold: float | None = None,
        **kwargs,
    ) -> list[Document]:
        """Retrieve documents using the retriever agent.

        Args:
            query: Query string for retrieval
            k: Number of documents to retrieve (defaults to self.top_k)
            score_threshold: Minimum similarity score (defaults to self.similarity_threshold)
            **kwargs: Additional retrieval parameters

        Returns:
            List of retrieved documents
        """
        retrieval_input = {
            "query": query,
            "k": k or self.top_k,
            "score_threshold": score_threshold or self.similarity_threshold,
            **kwargs,
        }

        retriever = self.get_retriever_agent()
        result = await retriever.arun(retrieval_input)

        # Extract documents from result
        if isinstance(result, list):
            return [doc for doc in result if isinstance(doc, Document)]
        if isinstance(result, dict) and "documents" in result:
            return result["documents"]
        if hasattr(result, "documents"):
            return list(result.documents)
        # Fallback: create document from string result
        return [
            Document(page_content=str(result), metadata={"source": "retrieval_result"})
        ]

    async def generate_answer(
        self, query: str, documents: list[Document], **kwargs
    ) -> Any:
        """Generate answer using the generator agent.

        Args:
            query: Original query
            documents: Retrieved documents for context
            **kwargs: Additional generation parameters

        Returns:
            Generated answer (format depends on structured_output_model)
        """
        # Prepare context from documents
        context_parts = []
        for i, doc in enumerate(documents):
            content = doc.page_content.strip()
            if content:
                source = doc.metadata.get("source", f"Document {i+1}")
                context_parts.append(f"Source: {source}\n{content}")

        context = "\n\n".join(context_parts)

        # Format with template
        formatted_input = self.context_template.format(context=context, query=query)

        # Generate answer
        generator = self.get_generator_agent()
        return await generator.arun(formatted_input, **kwargs)

    async def arun(
        self, input_data: str | dict[str, Any], debug: bool = False, **kwargs
    ) -> Any:
        """Execute RAG pipeline using MultiAgent sequential execution.

        This leverages the MultiAgent infrastructure but processes the results
        to provide RAG-specific functionality like document extraction and context formatting.

        Args:
            input_data: Query string or structured input dict with 'query' field
            debug: Enable debug logging and detailed output
            **kwargs: Additional execution parameters

        Returns:
            Generated response from the generator agent

        Raises:
            ValueError: If input validation fails
            RuntimeError: If pipeline execution fails
        """
        # Extract query from input
        if isinstance(input_data, str):
            query = input_data
        elif isinstance(input_data, dict) and "query" in input_data:
            query = input_data["query"]
        else:
            raise ValueError("Input must be a string or dict with 'query' field")

        if debug:
            logger.info(f"🔍 SimpleRAG processing query: {query}")
            logger.info(f"📋 Agents: {list(self.agents.keys())}")
            logger.info(f"⚙️ Execution mode: {self.execution_mode}")

        # Use MultiAgent's sequential execution
        # This will automatically run retriever → generator
        result = await super().arun(input_data, debug=debug, **kwargs)

        if debug:
            logger.info(f"✅ SimpleRAG completed: {type(result)}")

        return result

    # =============================
    # Utility Methods
    # =============================

    def get_rag_info(self) -> dict[str, Any]:
        """Get information about the RAG configuration."""
        return {
            "name": self.name,
            "retriever_agent": self.agents["retriever"].name,
            "generator_agent": self.agents["generator"].name,
            "execution_mode": self.execution_mode,
            "top_k": self.top_k,
            "similarity_threshold": self.similarity_threshold,
            "structured_output": self.structured_output_model is not None,
            "context_template": (
                self.context_template[:50] + "..."
                if len(self.context_template) > 50
                else self.context_template
            ),
        }

    def __repr__(self) -> str:
        """String representation showing MultiAgent structure."""
        return (
            f"SimpleRAG(MultiAgent)("
            f"name='{self.name}', "
            f"agents={list(self.agents.keys())}, "
            f"mode='{self.execution_mode}', "
            f"top_k={self.top_k}"
            f")"
        )


# ================================
# Legacy Compatibility
# ================================

# Alias for backward compatibility
SimpleRAGAgent = SimpleRAG


# ================================
# Export for Easy Import
# ================================

__all__ = ["SimpleRAG", "SimpleRAGAgent"]  # Legacy alias


# ================================
# Example Usage
# ================================

if __name__ == "__main__":
    from langchain_core.documents import Document

    async def demo():
        """Demonstrate proper MultiAgent SimpleRAG usage."""
        # Example documents
        [
            Document(
                page_content="Machine learning is a subset of AI that enables computers to learn without explicit programming.",
                metadata={"source": "ml_guide.pdf"},
            ),
            Document(
                page_content="Neural networks are computing systems inspired by biological neural networks.",
                metadata={"source": "nn_book.pdf"},
            ),
        ]

        # This would create a proper SimpleRAG with real configs
        # rag = SimpleRAG.from_documents(
        #     documents=docs,
        #     embedding_config=embedding_config,
        #     llm_config=AugLLMConfig(temperature=0.7)
        # )

        # print(f"📋 RAG Info: {rag.get_rag_info()}")
        # print(f"🏗️ Structure: {rag}")

        # result = await rag.arun("What is machine learning?", debug=True)
        # print(f"💬 Result: {result}")

    # Uncomment to run demo
    # asyncio.run(demo())
