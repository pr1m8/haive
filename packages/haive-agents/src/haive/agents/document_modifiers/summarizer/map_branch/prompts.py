"""Prompts for the summarizer agent - The mapping and reducing prompts."""

from langchain_core.prompts import ChatPromptTemplate

MAP_PROMPT = ChatPromptTemplate.from_messages(
    [("human", "Write a concise summary of the following:\\n\\n{context}")]
)
reduce_prompt_str = """
The following is a set of summaries:
{docs}
Take these and distill it into a final, consolidated summary
of the main themes.
"""
REDUCE_PROMPT = ChatPromptTemplate.from_messages([("human", reduce_prompt_str.strip())])
