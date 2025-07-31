"""Sequential_Agent core module.

This module provides sequential agent functionality for the Haive framework.

Classes:
    QAResponse: QAResponse implementation.
    RAGResponse: RAGResponse implementation.
    SimpleRAG: SimpleRAG implementation.

Functions:
    validate_context_template: Validate Context Template functionality.
    setup_agents: Setup Agents functionality.
    from_documents: From Documents functionality.
"""

#!/usr/bin/env python3
"""SimpleRAG - Sequential MultiAgent Implementation (BaseRAG → SimpleAgent).

This is the correct SimpleRAG implementation following the sequential multi-agent pattern:
    SimpleRAG = Sequential[BaseRAGAgent, SimpleAgent]

Architecture:
1. **BaseRAGAgent**: Performs document retrieval from vector store
2. **SimpleAgent**: Generates structured answers from retrieved documents
3. **Sequential Execution**: BaseRAG output → SimpleAgent input

Key Features:
- **Sequential Multi-Agent Pattern**: Proper composition of specialized agents
- **Pydantic Best Practices**: No __init__ overrides, field validation, inheritance
- **Type Safety**: Full type hints and proper agent composition
- **Real Component Integration**: Uses actual BaseRAGAgent and SimpleAgent
- **Structured Output**: Support for custom response models
- **Comprehensive Documentation**: Google-style docstrings with examples

Design Philosophy:
- **Composition over Monolith**: Uses existing proven agents
- **Clear Separation of Concerns**: Retrieval vs Generation
- **Reusable Components**: Each agent can be used independently
- **Testable Architecture**: Easy to test each component separately

Examples:
    Basic usage::

        from haive.agents.rag.simple import SimpleRAG
        from haive.core.engine.aug_llm import AugLLMConfig
        from haive.core.engine.vectorstore import VectorStoreConfig

        rag = SimpleRAG(
            name="qa_assistant",
            retriever_config=VectorStoreConfig(vector_store=your_vector_store),
            llm_config=AugLLMConfig(temperature=0.7),
            top_k=5
        )

        result = await rag.arun("What is machine learning?")

    With structured output::

        class QAResponse(BaseModel):
            answer: str
            sources: list[str]
            confidence: float

        rag = SimpleRAG(
            name="structured_qa",
            retriever_config=retriever_config,
            llm_config=AugLLMConfig(),
            structured_output_model=QAResponse
        )
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.retriever import BaseRetrieverConfig
from haive.core.engine.vectorstore import VectorStoreConfig
from langchain_core.documents import Document
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

# Import existing agents for composition
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)


# ================================
# Response Models
# ================================


class RAGResponse(BaseModel):
    """Comprehensive RAG response model.

    Contains the generated answer along with comprehensive metadata about
    the retrieval and generation process, including sources, confidence
    scores, and execution metrics.
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
        arbitrary_types_allowed=True,  # For Document objects
    )

    query: str = Field(..., min_length=1, description="Original user query")
    answer: str = Field(
        ..., min_length=1, description="Generated answer to the user's query"
    )
    sources: list[str] = Field(
        default_factory=list,
        description="List of source document identifiers or filenames",
    )
    retrieved_documents: list[Document] = Field(
        default_factory=list, description="Full retrieved documents used for generation"
    )
    confidence_score: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence in answer quality (0.0=low, 1.0=high)",
    )
    retrieval_metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Metadata about the retrieval and generation process",
    )


# ================================
# SimpleRAG Sequential Implementation
# ================================


class SimpleRAG(BaseModel):
    """SimpleRAG - Sequential composition of BaseRAGAgent and SimpleAgent.

    This implementation properly composes two specialized agents:
    1. BaseRAGAgent: Handles document retrieval from vector stores
    2. SimpleAgent: Generates answers from retrieved documents

    The sequential flow is: Query → BaseRAG → Documents → SimpleAgent → Answer

    This follows the multi-agent pattern established in the Haive framework
    where complex capabilities are built by composing simpler, focused agents.

    Examples:
        Basic usage::

            rag = SimpleRAG(
                name="qa_system",
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

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        extra="forbid",
    )

    # =============================
    # Core Configuration
    # =============================

    name: str = Field(
        default="Simple RAG Agent",
        min_length=1,
        max_length=100,
        description="Agent identifier",
    )

    retriever_config: BaseRetrieverConfig | VectorStoreConfig = Field(
        ...,
        description="Configuration for document retrieval (vector store or retriever)",
    )

    llm_config: AugLLMConfig = Field(
        ..., description="Configuration for answer generation LLM"
    )

    # =============================
    # Retrieval Parameters
    # =============================

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

    # =============================
    # Generation Parameters
    # =============================

    structured_output_model: type[BaseModel] | None = Field(
        default=None, description="Pydantic model for structured output formatting"
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

    context_template: str = Field(
        default="Context:\n{context}\n\nQuestion: {query}\n\nAnswer:",
        min_length=10,
        description="Template for formatting context and query for LLM",
    )

    # =============================
    # Agent Instances (Private)
    # =============================

    _retriever_agent: BaseRAGAgent | None = Field(
        default=None, exclude=True, description="Internal BaseRAGAgent instance"
    )

    _generator_agent: SimpleAgent | None = Field(
        default=None, exclude=True, description="Internal SimpleAgent instance"
    )

    # =============================
    # Validation
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
    def setup_agents(self) -> SimpleRAG:
        """Setup internal agent instances after validation."""
        # Create retriever agent
        self._retriever_agent = BaseRAGAgent(
            name=f"{self.name}_retriever", engine=self.retriever_config
        )

        # Create generator agent with customized system prompt
        generator_config = self.llm_config.model_copy()
        if not generator_config.system_message:
            generator_config.system_message = self.system_prompt_template

        self._generator_agent = SimpleAgent(
            name=f"{self.name}_generator",
            engine=generator_config,
            structured_output_model=self.structured_output_model,
        )

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
        # Use BaseRAGAgent's from_documents method
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
    # Execution Methods
    # =============================

    async def arun(
        self, input_data: str | dict[str, Any], debug: bool = False, **kwargs
    ) -> str | RAGResponse | BaseModel:
        """Execute RAG pipeline with sequential agent composition.

        Flow:
        1. Extract query from input
        2. Use BaseRAGAgent to retrieve relevant documents
        3. Format documents as context
        4. Use SimpleAgent to generate answer from context
        5. Return formatted response

        Args:
            input_data: Query string or structured input dict with 'query' field
            debug: Enable debug logging and detailed output
            **kwargs: Additional execution parameters

        Returns:
            Generated response - format depends on structured_output_model:
            - str: Simple answer string (default)
            - RAGResponse: Full response with metadata (if debug=True)
            - BaseModel: Custom structured output (if structured_output_model set)

        Raises:
            ValueError: If input validation fails
            RuntimeError: If critical pipeline components fail
        """
        import time

        start_time = time.time()

        try:
            # 1. Process Input
            query = self._extract_query(input_data)
            if debug:
                logger.info(f"🔍 Processing query: {query}")

            # 2. Retrieve Documents (BaseRAGAgent)
            if debug:
                logger.info("📚 Retrieving documents with BaseRAGAgent...")

            retrieval_input = {
                "query": query,
                "k": self.top_k,
                "score_threshold": self.similarity_threshold,
            }

            retrieval_result = await self._retriever_agent.arun(
                retrieval_input, debug=debug
            )
            documents = self._extract_documents(retrieval_result)

            if debug:
                logger.info(f"📄 Retrieved {len(documents)} documents")

            # 3. Prepare Context
            context = self._prepare_context(documents, query)
            if debug:
                logger.info(f"📝 Prepared context: {len(context)} characters")

            # 4. Generate Answer (SimpleAgent)
            if debug:
                logger.info("🤖 Generating answer with SimpleAgent...")

            generation_input = context
            answer_result = await self._generator_agent.arun(
                generation_input, debug=debug
            )

            # 5. Format Response
            response = self._format_response(
                query=query,
                answer=answer_result,
                documents=documents,
                execution_time=time.time() - start_time,
                debug=debug,
            )

            if debug:
                execution_time = time.time() - start_time
                logger.info(f"✅ RAG pipeline completed in {execution_time:.2f}s")

            return response

        except Exception as e:
            logger.exception(f"❌ RAG pipeline failed: {e}")
            raise RuntimeError(f"RAG execution failed: {e}")

    def run(
        self, input_data: str | dict[str, Any], debug: bool = False, **kwargs
    ) -> str | RAGResponse | BaseModel:
        """Synchronous execution wrapper."""
        return asyncio.run(self.arun(input_data, debug=debug, **kwargs))

    # =============================
    # Helper Methods
    # =============================

    def _extract_query(self, input_data: str | dict[str, Any]) -> str:
        """Extract query string from input data."""
        if isinstance(input_data, str):
            if not input_data.strip():
                raise ValueError("Query cannot be empty")
            return input_data.strip()

        if isinstance(input_data, dict):
            if "query" not in input_data:
                raise ValueError("Dict input must contain 'query' field")
            query = input_data["query"]
            if not isinstance(query, str) or not query.strip():
                raise ValueError("Query must be a non-empty string")
            return query.strip()

        raise ValueError(f"Unsupported input type: {type(input_data)}")

    def _extract_documents(self, retrieval_result: Any) -> list[Document]:
        """Extract documents from retrieval result."""
        if isinstance(retrieval_result, list):
            return [doc for doc in retrieval_result if isinstance(doc, Document)]

        if isinstance(retrieval_result, dict):
            if "documents" in retrieval_result:
                docs = retrieval_result["documents"]
                return [doc for doc in docs if isinstance(doc, Document)]
            if "retrieved_documents" in retrieval_result:
                docs = retrieval_result["retrieved_documents"]
                return [doc for doc in docs if isinstance(doc, Document)]

        # If result has documents attribute
        if hasattr(retrieval_result, "documents"):
            return list(retrieval_result.documents)

        # Fallback: try to convert result to string and create mock documents
        logger.warning(
            "Could not extract documents from retrieval result, using fallback"
        )
        content = str(retrieval_result)
        return [Document(page_content=content, metadata={"source": "retrieval_result"})]

    def _prepare_context(self, documents: list[Document], query: str) -> str:
        """Prepare context from retrieved documents."""
        if not documents:
            return "No relevant documents found."

        # Combine document content
        context_parts = []
        for i, doc in enumerate(documents):
            content = doc.page_content.strip()
            if not content:
                continue

            # Add source information if available
            source = doc.metadata.get("source", f"Document {i+1}")
            formatted_content = f"Source: {source}\n{content}"
            context_parts.append(formatted_content)

        context = "\n\n".join(context_parts)

        # Format with template
        formatted_context = self.context_template.format(context=context, query=query)

        return formatted_context

    def _format_response(
        self,
        query: str,
        answer: Any,
        documents: list[Document],
        execution_time: float,
        debug: bool = False,
    ) -> str | RAGResponse | BaseModel:
        """Format the final response."""
        # Extract answer string
        answer_text = str(answer)
        if hasattr(answer, "content"):
            answer_text = answer.content
        elif isinstance(answer, BaseModel):
            answer_text = answer.answer if hasattr(answer, "answer") else str(answer)

        # Extract sources
        sources = []
        for doc in documents:
            source = doc.metadata.get("source", "Unknown")
            if source not in sources:
                sources.append(source)

        # Calculate confidence (simple heuristic)
        confidence = min(len(documents) / max(self.top_k, 1), 1.0)
        if len(answer_text) > 50:
            confidence *= 1.1
        confidence = min(confidence, 1.0)

        # Create response metadata
        retrieval_metadata = {
            "execution_time": execution_time,
            "documents_retrieved": len(documents),
            "sources_used": len(sources),
            "retriever_agent": (
                self._retriever_agent.name if self._retriever_agent else None
            ),
            "generator_agent": (
                self._generator_agent.name if self._generator_agent else None
            ),
        }

        # Create full response object
        rag_response = RAGResponse(
            query=query,
            answer=answer_text,
            sources=sources,
            retrieved_documents=documents,
            confidence_score=confidence,
            retrieval_metadata=retrieval_metadata,
        )

        # Return based on configuration
        if self.structured_output_model and isinstance(answer, BaseModel):
            return answer  # SimpleAgent already returned structured output

        if debug:
            return rag_response

        return rag_response.answer

    # =============================
    # Utility Methods
    # =============================

    def get_agent_info(self) -> dict[str, Any]:
        """Get information about the composed agents."""
        return {
            "name": self.name,
            "retriever_agent": {
                "name": self._retriever_agent.name if self._retriever_agent else None,
                "type": (
                    type(self._retriever_agent).__name__
                    if self._retriever_agent
                    else None
                ),
            },
            "generator_agent": {
                "name": self._generator_agent.name if self._generator_agent else None,
                "type": (
                    type(self._generator_agent).__name__
                    if self._generator_agent
                    else None
                ),
            },
            "retrieval_config": {
                "top_k": self.top_k,
                "similarity_threshold": self.similarity_threshold,
            },
            "structured_output": self.structured_output_model is not None,
        }

    def __repr__(self) -> str:
        """String representation showing composition."""
        return (
            f"SimpleRAG("
            f"name='{self.name}', "
            f"retriever={type(self._retriever_agent).__name__ if self._retriever_agent else 'None'}, "
            f"generator={type(self._generator_agent).__name__ if self._generator_agent else 'None'}, "
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

__all__ = ["RAGResponse", "SimpleRAG", "SimpleRAGAgent"]  # Legacy alias


# ================================
# Example Usage
# ================================

if __name__ == "__main__":
    import asyncio

    from haive.core.engine.aug_llm import AugLLMConfig
    from haive.core.engine.vectorstore import VectorStoreConfig
    from langchain_core.documents import Document

    # Example documents
    example_docs = [
        Document(
            page_content="Machine learning is a subset of artificial intelligence that enables computers to learn without being explicitly programmed.",
            metadata={"source": "ml_basics.pdf"},
        ),
        Document(
            page_content="Neural networks are computing systems inspired by biological neural networks, consisting of layers of interconnected nodes.",
            metadata={"source": "neural_networks.pdf"},
        ),
    ]

    async def demo():
        """Demonstrate SimpleRAG usage."""
        # Create from documents (this would use real vector store in practice)

        # In a real implementation, you'd have proper embedding and vector store configs
        # This is just for demonstration

        SimpleRAG(
            name="demo_rag",
            # retriever_config would be real VectorStoreConfig
            # llm_config would be real AugLLMConfig
            # This is just a demo structure
        )

    # Uncomment to run demo
    # asyncio.run(demo())
