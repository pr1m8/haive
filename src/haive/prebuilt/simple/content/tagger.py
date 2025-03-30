# Document-oriented Simple Agents

# src/haive/prebuilt/simple/tagger.py
"""
Agent Name: DocumentTagger
Description: Tags a document or passage with relevant keywords, topics, or semantic tags.
"""
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.core.agents.base import AugLLMConfig

SYSTEM_PROMPT = """
You are a smart document tagger. Your task is to read the input content and output a list of relevant tags that summarize the key topics, entities, or themes.
Use common, meaningful tags that would help categorize or retrieve the content in a larger collection.
Avoid over-tagging. Use 5–10 precise, informative tags only.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "Content: {input}")
])

class TagOutput(BaseModel):
    tags: List[str] = Field(..., description="List of concise, high-level tags representing the document content.")

config = AugLLMConfig(
    name="document_tagger",
    llm_config=AzureLLMConfig(),
    prompt_template=prompt,
    structured_output_model=TagOutput,
)
