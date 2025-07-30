"""Summarizer core module.

This module provides summarizer functionality for the Haive framework.
"""

from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that summarizes text."),
        ("user", "{text}"),
    ]
)
