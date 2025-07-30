"""Prompts core module.

This module provides prompts functionality for the Haive framework.
"""

#!/usr/bin/env python3
"""Prompt templates for RAG answer generation."""

from langchain_core.prompts import ChatPromptTemplate

# Chat prompt template for RAG answer generation
RAG_CHAT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful assistant that answers questions based on provided context.

Instructions:
- Use ONLY the information in the provided context to answer the question
- If the context doesn't contain enough information, say so clearly
- Provide source references when possible
- Be concise but comprehensive
- Indicate your confidence level in the answer

Format your response as structured output with:
- answer: The main answer to the question
- sources: List of source identifiers or filenames mentioned
- confidence: Your confidence score (0.0 to 1.0)
- reasoning: Brief explanation of how you derived the answer""",
        ),
        (
            "human",
            """Context:
{context}

Question: {query}

Please provide a structured answer based on the context above.""",
        ),
    ]
)


__all__ = ["RAG_CHAT_TEMPLATE"]
