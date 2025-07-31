"""Specialized Answer Generator Agent for SimpleRAG V3.

This module provides a specialized answer generation agent that extends SimpleAgent
with enhanced features for generating answers from retrieved documents.
"""

import logging
import time
from typing import Any

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from pydantic import Field

from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)


# RAG Answer Generation Prompt Template
RAG_ANSWER_GENERATION = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful AI assistant that answers questions based on retrieved documents. 
Your responses should be accurate, well-sourced, and acknowledge any limitations 
in the available information. Always cite specific sources when possible.""",
        ),
        (
            "human",
            """Based on the following retrieved documents, please answer the question.

Retrieved Documents:
{retrieved_documents}

Question: {query}

Instructions:
- Use only the information provided in the retrieved documents
- If the retrieved documents don't contain enough information, say so clearly
- Include source references where appropriate
- Be concise but comprehensive

Answer:""",
        ),
    ]
)


class SimpleAnswerAgent(SimpleAgent):
    """Specialized answer generation agent for SimpleRAG V3.

    This agent extends SimpleAgent with RAG-specific features:
    - Document-aware prompt templates
    - Context formatting and processing
    - Source citation and attribution
    - Answer quality scoring
    - Enhanced metadata collection

    Designed to work as the second agent in Enhanced MultiAgent V3 sequential pattern:
    RetrieverAgent → SimpleAnswerAgent

    The agent expects input from RetrieverAgent containing:
    - documents: List of retrieved documents
    - query: Original user query
    - metadata: Retrieval metadata

    Examples:
        Basic usage::

            answer_agent = SimpleAnswerAgent(
                name="answer_generator",
                engine=AugLLMConfig(temperature=0.7),
                max_context_length=4000
            )

        With structured output::

            class QAResponse(BaseModel):
                answer: str
                sources: List[str]
                confidence: float

            answer_agent = SimpleAnswerAgent(
                name="structured_answer",
                engine=AugLLMConfig(),
                structured_output_model=QAResponse
            )
    """

    # Context processing configuration
    max_context_length: int = Field(
        default=4000,
        ge=500,
        le=32000,
        description="Maximum context length in characters",
    )

    # Use ChatPromptTemplate instead of string template
    use_chat_prompt_template: bool = Field(
        default=True, description="Use ChatPromptTemplate for formatting prompts"
    )

    system_prompt_template: str = Field(
        default=(
            "You are a helpful AI assistant that answers questions based on provided documents. "
            "Your responses should be accurate, well-sourced, and acknowledge any limitations "
            "in the available information. Always cite specific sources when possible."
        ),
        description="System prompt for answer generation",
    )

    # Source handling
    include_citations: bool = Field(
        default=True, description="Include source citations in answers"
    )

    citation_style: str = Field(
        default="inline",
        description="Citation style: 'inline', 'footnote', or 'numbered'",
    )

    # Quality configuration
    require_source_support: bool = Field(
        default=True, description="Require answers to be supported by sources"
    )

    min_confidence_threshold: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Minimum confidence threshold for answers",
    )

    # Enhanced features
    performance_mode: bool = Field(
        default=False, description="Enable performance tracking"
    )

    debug_mode: bool = Field(
        default=False, description="Enable debug information collection"
    )

    async def arun(
        self, input_data: str | dict[str, Any], debug: bool = False, **kwargs
    ) -> dict[str, Any] | str:
        """Enhanced answer generation with document processing.

        Args:
            input_data: Input from RetrieverAgent or direct query
            debug: Enable debug output
            **kwargs: Additional generation parameters

        Returns:
            Generated answer (format depends on structured_output_model)
        """
        start_time = time.time()

        # Parse input from RetrieverAgent
        parsed_input = self._parse_retriever_input(input_data)
        query = parsed_input["query"]
        documents = parsed_input["documents"]
        retrieval_metadata = parsed_input.get("metadata", {})

        if debug or self.debug_mode:
            logger.info(f"🎯 SimpleAnswerAgent '{self.name}' generating answer")
            logger.info(f"📄 Processing {len(documents)} documents for query: {query}")

        try:
            # Process documents and build context
            context_info = self._build_context_from_documents(
                documents, query, debug or self.debug_mode
            )

            # Format prompt with context
            formatted_prompt = self._format_prompt_with_context(
                query, context_info, debug or self.debug_mode
            )

            # Generate answer using parent SimpleAgent
            generation_result = await super().arun(
                formatted_prompt, debug=debug, **kwargs
            )

            # Calculate timing
            generation_time = time.time() - start_time

            # Process and enhance the result
            enhanced_result = self._enhance_generation_result(
                generation_result,
                context_info,
                query,
                documents,
                generation_time,
                retrieval_metadata,
                debug or self.debug_mode,
            )

            if debug or self.debug_mode:
                logger.info(f"✅ Generated answer in {generation_time:.3f}s")

            return enhanced_result

        except Exception as e:
            logger.error(f"❌ SimpleAnswerAgent error: {e}")
            error_result = {
                "answer": f"I apologize, but I encountered an error while generating the answer: {e!s}",
                "error": str(e),
                "query": query,
                "generation_time": time.time() - start_time,
                "documents_processed": len(documents),
            }

            # Return in expected format
            if self.structured_output_model:
                return error_result
            return error_result["answer"]

    def _parse_retriever_input(self, input_data: Any) -> dict[str, Any]:
        """Parse input from RetrieverAgent, BaseRAGAgent, or direct query.

        Handles multiple input formats:
        - BaseRAGAgent: Uses 'retrieved_documents' field
        - RetrieverAgent: Uses 'documents' field
        - Direct string: Creates empty document list
        """
        if isinstance(input_data, str):
            # Direct query string
            return {"query": input_data, "documents": [], "metadata": {}}

        if isinstance(input_data, dict):
            # Input from RetrieverAgent or BaseRAGAgent
            # Check for 'retrieved_documents' first (BaseRAG format)
            documents = input_data.get(
                "retrieved_documents", input_data.get("documents", [])
            )

            return {
                "query": input_data.get("query", ""),
                "documents": documents,
                "metadata": input_data.get("metadata", {}),
            }

        # Try to extract from object attributes (e.g., RetrieverOutput)
        # Check for 'retrieved_documents' attribute first
        if hasattr(input_data, "retrieved_documents"):
            documents = getattr(input_data, "retrieved_documents", [])
        else:
            documents = getattr(input_data, "documents", [])

        return {
            "query": getattr(input_data, "query", ""),
            "documents": documents,
            "metadata": getattr(input_data, "metadata", {}),
        }

    def _build_context_from_documents(
        self, documents: list[Document], query: str, debug: bool = False
    ) -> dict[str, Any]:
        """Build formatted context from retrieved documents."""
        if not documents:
            return {
                "formatted_context": "No relevant documents were found.",
                "sources": [],
                "total_length": 0,
                "document_count": 0,
            }

        context_parts = []
        sources = []
        total_length = 0

        for i, doc in enumerate(documents):
            # Get document content
            content = doc.page_content.strip()
            if not content:
                continue

            # Get source information
            source = doc.metadata.get("source", f"Document {i+1}")
            sources.append(source)

            # Format document for context
            if self.include_citations:
                if self.citation_style == "inline":
                    doc_text = f"[Source: {source}]\n{content}"
                elif self.citation_style == "numbered":
                    doc_text = f"[{i+1}] {content}\n(Source: {source})"
                else:  # footnote
                    doc_text = f"{content} [{i+1}]"
            else:
                doc_text = content

            # Check length constraints
            if total_length + len(doc_text) > self.max_context_length:
                if debug:
                    logger.info(
                        f"📏 Context length limit reached, truncating at document {i}"
                    )
                break

            context_parts.append(doc_text)
            total_length += len(doc_text)

        # Build final context
        formatted_context = "\n\n".join(context_parts)

        if debug:
            logger.info(
                f"📝 Built context: {len(context_parts)} docs, {total_length} chars"
            )

        return {
            "formatted_context": formatted_context,
            "sources": sources[: len(context_parts)],  # Only include sources we used
            "total_length": total_length,
            "document_count": len(context_parts),
            "truncated": len(context_parts) < len(documents),
        }

    def _format_prompt_with_context(
        self, query: str, context_info: dict[str, Any], debug: bool = False
    ) -> str:
        """Format the prompt with context and query."""
        formatted_prompt = self.context_template.format(
            context=context_info["formatted_context"], query=query
        )

        if debug:
            logger.info(f"📋 Formatted prompt: {len(formatted_prompt)} chars")

        return formatted_prompt

    def _enhance_generation_result(
        self,
        generation_result: Any,
        context_info: dict[str, Any],
        query: str,
        documents: list[Document],
        generation_time: float,
        retrieval_metadata: dict[str, Any],
        debug: bool = False,
    ) -> dict[str, Any] | str:
        """Enhance generation result with metadata and citations."""
        # Extract the answer text
        if isinstance(generation_result, str):
            answer_text = generation_result
        elif isinstance(generation_result, dict) and "answer" in generation_result:
            answer_text = generation_result["answer"]
        elif hasattr(generation_result, "content"):
            answer_text = generation_result.content
        else:
            answer_text = str(generation_result)

        # Build enhanced result
        enhanced_result = {
            "answer": answer_text,
            "query": query,
            "sources": context_info["sources"],
            "generation_time": generation_time,
            "documents_processed": context_info["document_count"],
            "context_length": context_info["total_length"],
            "context_truncated": context_info.get("truncated", False),
        }

        # Add performance metrics if enabled
        if self.performance_mode:
            enhanced_result["performance_metrics"] = {
                "generation_time": generation_time,
                "answer_length": len(answer_text),
                "context_length": context_info["total_length"],
                "words_per_second": len(answer_text.split())
                / max(generation_time, 0.001),
                "compression_ratio": len(answer_text)
                / max(context_info["total_length"], 1),
            }

        # Add debug information if enabled
        if debug or self.debug_mode:
            enhanced_result["debug_info"] = {
                "agent_name": self.name,
                "context_template": self.context_template[:100] + "...",
                "citation_style": self.citation_style,
                "include_citations": self.include_citations,
                "max_context_length": self.max_context_length,
                "documents_available": len(documents),
                "documents_used": context_info["document_count"],
                "retrieval_metadata": retrieval_metadata,
            }

        # Add citations if enabled
        if self.include_citations and context_info["sources"]:
            if self.citation_style == "footnote":
                # Add footnote references
                footnotes = [
                    f"[{i+1}] {source}"
                    for i, source in enumerate(context_info["sources"])
                ]
                enhanced_result["citations"] = footnotes
                enhanced_result["answer"] += "\n\nSources:\n" + "\n".join(footnotes)

        # Return in appropriate format
        if self.structured_output_model:
            # For structured output, return the dict (will be processed by SimpleAgent)
            return enhanced_result
        # For simple text output, return just the answer
        return enhanced_result["answer"]

    def get_generation_summary(self) -> dict[str, Any]:
        """Get summary of answer generator configuration."""
        return {
            "name": self.name,
            "max_context_length": self.max_context_length,
            "include_citations": self.include_citations,
            "citation_style": self.citation_style,
            "require_source_support": self.require_source_support,
            "performance_mode": self.performance_mode,
            "debug_mode": self.debug_mode,
            "has_structured_output": self.structured_output_model is not None,
            "structured_output_model": (
                self.structured_output_model.__name__
                if self.structured_output_model
                else None
            ),
            "engine_config": {
                "temperature": getattr(self.engine, "temperature", None),
                "max_tokens": getattr(self.engine, "max_tokens", None),
                "model": getattr(self.engine, "model", None),
            },
        }


__all__ = ["SimpleAnswerAgent"]
